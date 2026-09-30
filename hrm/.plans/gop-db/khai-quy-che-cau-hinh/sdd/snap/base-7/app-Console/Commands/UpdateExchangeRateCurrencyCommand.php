<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Finance\Entities\Currency\Currency;
use Modules\Finance\Http\Requests\Currency\CurrencyRequest;

/**
 * Cập nhật tỷ giá ngoại tệ hằng ngày từ Vietcombank — chuyển từ ERP
 * (`app/Console/Commands/UpdateExchangeRateCurrency.php`, signature `currency:update_exchange_rate`).
 *
 * Ghi vào bảng `currencies` dùng chung trên DB gộp, nên nếu cron bên ERP còn bật thì cả hai cùng
 * ghi 1 giá trị từ 1 nguồn — không sai dữ liệu nhưng thừa. Tắt bên nào là quyết định vận hành.
 *
 * Khác bản ERP (đều là sửa lỗi, xem chi tiết trong `.plans/finance-currency-catalog/design.md`):
 *  1. `array_search` trả index 0 cho phần tử ĐẦU tiên; bản ERP kiểm tra `if ($searchResultKey)` nên
 *     đồng tiền đứng đầu file XML không bao giờ được cập nhật. Ở đây so `!== false`.
 *  2. Bản ERP có dòng `$currencies->exchange_rate = ...` gán vào COLLECTION (thừa, không tác dụng).
 *  3. Bản ERP không xử lý khi curl lỗi / XML hỏng -> chạy tiếp và im lặng. Ở đây dừng + ghi log.
 *  4. Chặn giá trị vượt trần cột `double(8,2)` để không bị MySQL cắt số.
 */
class UpdateExchangeRateCurrencyCommand extends Command
{
    protected $signature = 'finance:update-exchange-rate';

    protected $description = 'Cập nhật tỷ giá ngoại tệ (nguồn: Vietcombank), bỏ qua VNĐ';

    /**
     * Nguồn tỷ giá — giữ nguyên endpoint đang dùng ở ERP.
     */
    const SOURCE_URL = 'https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx?b=10';

    /**
     * Mã tiền tệ không đồng bộ (tiền tệ gốc).
     */
    const SKIP_CODES = ['VNĐ', 'VND'];

    public function handle(): int
    {
        $xml = $this->fetchSource();
        if ($xml === null) {
            return self::FAILURE;
        }

        $rates = $this->parseRates($xml);
        if (empty($rates)) {
            $this->error('Không đọc được tỷ giá nào từ nguồn.');
            Log::error('[finance:update-exchange-rate] Nguồn trả về không có tỷ giá nào');

            return self::FAILURE;
        }

        $currencies = Currency::query()->whereNotIn('code', self::SKIP_CODES)->get();

        $updated = 0;
        $skipped = 0;

        foreach ($currencies as $currency) {
            $code = strtoupper(trim((string) $currency->code));

            if (!isset($rates[$code])) {
                $skipped++;
                continue;
            }

            $rate = $rates[$code];

            if ($rate <= 0 || $rate > CurrencyRequest::MAX_EXCHANGE_RATE) {
                $this->warn("Bỏ qua {$code}: tỷ giá {$rate} nằm ngoài khoảng cho phép");
                Log::warning("[finance:update-exchange-rate] {$code} có tỷ giá ngoài khoảng: {$rate}");
                $skipped++;
                continue;
            }

            // So sánh theo 2 chữ số thập phân đúng như độ chính xác của cột.
            if (round((float) $currency->exchange_rate, 2) === round($rate, 2)) {
                $skipped++;
                continue;
            }

            $currency->exchange_rate = $rate;
            $currency->save();
            $updated++;
        }

        $this->info("Đã cập nhật {$updated} tiền tệ, bỏ qua {$skipped}.");

        return self::SUCCESS;
    }

    /**
     * Tải XML tỷ giá. Trả null nếu hỏng.
     *
     * @return \SimpleXMLElement|null
     */
    private function fetchSource()
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, self::SOURCE_URL);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_USERAGENT, 'spider');

        $body = curl_exec($ch);
        $error = curl_error($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($body === false || $error !== '') {
            $this->error("Không gọi được nguồn tỷ giá: {$error}");
            Log::error("[finance:update-exchange-rate] curl lỗi: {$error}");

            return null;
        }

        if ($httpCode !== 200) {
            $this->error("Nguồn tỷ giá trả HTTP {$httpCode}");
            Log::error("[finance:update-exchange-rate] HTTP {$httpCode}");

            return null;
        }

        $xml = @simplexml_load_string($body);
        if ($xml === false) {
            $this->error('Nội dung trả về không phải XML hợp lệ.');
            Log::error('[finance:update-exchange-rate] XML không hợp lệ');

            return null;
        }

        return $xml;
    }

    /**
     * Đổi XML sang map [MÃ TIỀN TỆ => tỷ giá bán].
     *
     * @param  \SimpleXMLElement $xml
     * @return array<string, float>
     */
    private function parseRates($xml): array
    {
        $rows = json_decode(json_encode($xml), true)['Exrate'] ?? [];

        // Nguồn chỉ có 1 dòng thì json trả về object chứ không phải mảng các dòng.
        if (isset($rows['@attributes'])) {
            $rows = [$rows];
        }

        $rates = [];

        foreach ($rows as $row) {
            $attributes = $row['@attributes'] ?? null;
            if (!$attributes || !isset($attributes['CurrencyCode'], $attributes['Sell'])) {
                continue;
            }

            $code = strtoupper(trim((string) $attributes['CurrencyCode']));
            // Giá bán ở dạng "26,520.00" -> bỏ dấu phân cách nghìn trước khi ép số.
            $value = (float) str_replace(',', '', (string) $attributes['Sell']);

            if ($code !== '' && $value > 0) {
                $rates[$code] = $value;
            }
        }

        return $rates;
    }
}
