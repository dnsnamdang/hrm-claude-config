<?php

namespace App\Console\Commands\CustomerCare;

use Illuminate\Console\Command;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation;
use Modules\CustomerCare\Services\WrQuotationService;

/**
 * Đánh dấu BÁO GIÁ DỊCH VỤ đã quá hạn hiệu lực -> trạng thái "Hết hiệu lực".
 *
 * Port từ ERP `update:quotations-expried` (chạy 00:30 hằng ngày). Điều kiện giữ nguyên ERP:
 * báo giá đang ở trạng thái **Duyệt** mà `ngày lập + số ngày hiệu lực` đã qua.
 *
 * ⚠️ KHÁC ERP MỘT ĐIỂM CÓ CHỦ Ý: ERP đổi hàng loạt bằng một câu `update()`, nên không ghi lịch
 * sử và không đóng dấu người cập nhật — người dùng mở phiếu thấy trạng thái tự nhảy mà không có
 * dòng nào giải thích. HRM đi từng phiếu để **ghi lịch sử thay đổi trạng thái** như mọi thao tác
 * khác (quy ước bắt buộc của HRM, xem skill `entity-history`). Số phiếu mỗi ngày rất nhỏ nên
 * chi phí không đáng kể.
 *
 * ERP còn xử lý cả Báo giá hãng (`FirmQuotation`) trong cùng lệnh — phần đó thuộc phân hệ khác,
 * chưa port sang HRM nên không đụng tới.
 */
class ExpireQuotationsCommand extends Command
{
    protected $signature = 'customer-care:expire-quotations {--dry-run : Chỉ liệt kê phiếu sẽ đổi, KHÔNG ghi gì}';

    protected $description = 'Chuyển báo giá dịch vụ đã quá hạn hiệu lực sang trạng thái Hết hiệu lực';

    public function handle(WrQuotationService $service)
    {
        $chayThu = (bool) $this->option('dry-run');

        $quotations = WrServiceQuotation::query()
            ->where('type', WrServiceQuotation::TYPE_QUOTATION)
            ->where('status', WrServiceQuotation::STATUS_QT_APPROVED)
            // Số ngày hiệu lực để trống = không đặt hạn -> KHÔNG bao giờ hết hiệu lực.
            // `IFNULL` cho chắc: cột cho phép null, mà `DATE_ADD(..., NULL)` trả null nên phép so
            // sánh ra `false` một cách im lặng — viết rõ ra để người đọc sau không phải đoán.
            ->whereNotNull('date_of_entering')
            ->where('date_of_entering', '>', 0)
            ->whereRaw('DATE(DATE_ADD(created_at, INTERVAL date_of_entering DAY)) < ?', [now()->toDateString()])
            ->orderBy('id')
            ->get();

        if ($quotations->isEmpty()) {
            $this->info('Không có báo giá nào quá hạn.');

            return 0;
        }

        $this->info(sprintf('%s %d báo giá quá hạn hiệu lực:', $chayThu ? '[CHẠY THỬ] Sẽ đổi' : 'Đang đổi', $quotations->count()));

        $xong = 0;
        foreach ($quotations as $quotation) {
            $hetHan = $quotation->created_at->copy()->addDays((int) $quotation->date_of_entering)->format('d/m/Y');
            $this->line(sprintf('  %s — lập %s, hiệu lực %d ngày, hết hạn %s',
                $quotation->code, $quotation->created_at->format('d/m/Y'), (int) $quotation->date_of_entering, $hetHan));

            if ($chayThu) {
                continue;
            }

            try {
                $service->expire($quotation);
                $xong++;
            } catch (\Exception $e) {
                // Một phiếu lỗi KHÔNG được chặn những phiếu còn lại: lệnh chạy nền mà dừng giữa
                // chừng thì hôm sau vẫn còn tồn đúng đống đó, không ai biết.
                $this->error(sprintf('  ! %s: %s', $quotation->code, $e->getMessage()));
            }
        }

        $this->info($chayThu ? 'Chạy thử, chưa ghi gì.' : sprintf('Đã chuyển %d/%d báo giá sang Hết hiệu lực.', $xong, $quotations->count()));

        return 0;
    }
}
