<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

/**
 * Khôi phục ảnh đại diện nhân sự bị mất do bug sync khuôn mặt xóa nhầm file S3.
 *
 * Bối cảnh: khi tạo nhân sự bật face_recognition, face_image_url được gán = URL avatar.
 * Job sync mặt (ConnInfoService/RiceConnInfoService::deleteS3ByUrl) xóa face_image_url cũ
 * trên S3 -> xóa luôn file avatar, còn cột image vẫn trỏ tới file đã mất (HTTP 403/404).
 * Nhưng face_image_url mới (ảnh máy chấm công) chính là ảnh avatar đã được tải lại -> dùng
 * để khôi phục: set image = face_image_url cho những nhân sự image hỏng + face_image_url còn sống.
 *
 * Mặc định chạy DRY-RUN (chỉ liệt kê + xuất CSV, KHÔNG đổi DB). Thêm --apply để update thật.
 * Update qua query builder (KHÔNG dùng Eloquent save) để né side-effect đồng bộ sang DB ERP.
 *
 * BẮT BUỘC: deploy fix guard trong deleteS3ByUrl lên production TRƯỚC khi/khi chạy lệnh này,
 * nếu không sync vẫn tiếp tục xóa avatar.
 */
class RecoverEmployeeAvatar extends Command
{
    protected $signature = 'human:recover-employee-avatar {--apply : Thực thi update DB (mặc định chỉ dry-run)}';

    protected $description = 'Khôi phục ảnh đại diện nhân sự bị mất (set image = face_image_url khi image hỏng và face_image_url còn sống)';

    public function handle()
    {
        $apply = (bool) $this->option('apply');
        $this->info($apply ? '>>> CHẾ ĐỘ APPLY: sẽ cập nhật DB.' : '>>> DRY-RUN: chỉ liệt kê, KHÔNG đổi DB. Thêm --apply để chạy thật.');

        // Ứng viên: có image, có face_image_url, và face_image_url khác image (sync đã thay)
        $candidates = DB::table('employee_infos')
            ->whereNotNull('image')->where('image', '!=', '')
            ->whereNotNull('face_image_url')->where('face_image_url', '!=', '')
            ->whereColumn('face_image_url', '!=', 'image')
            ->select('id', 'code', 'fullname', 'enter_date', 'image', 'face_image_url')
            ->get();

        $this->info('Số ứng viên (face_image_url != image): ' . $candidates->count());

        $recover = [];
        $bar = $this->output->createProgressBar($candidates->count());
        foreach ($candidates as $e) {
            // image phải hỏng rõ ràng (403/404), face_image_url phải còn sống (200)
            if (in_array($this->httpStatus($e->image), [403, 404], true) && $this->httpStatus($e->face_image_url) === 200) {
                $recover[] = $e;
            }
            $bar->advance();
        }
        $bar->finish();
        $this->newLine();

        $this->info('Số khôi phục được (image 403/404 + face_image_url 200): ' . count($recover));

        // Phân bố theo tháng vào làm
        $byMonth = [];
        foreach ($recover as $e) {
            $m = substr((string) $e->enter_date, 0, 7);
            $byMonth[$m] = ($byMonth[$m] ?? 0) + 1;
        }
        ksort($byMonth);
        foreach ($byMonth as $m => $c) {
            $this->line('  ' . $m . ': ' . $c);
        }

        // Xuất CSV backup (luôn xuất, cả dry-run lẫn apply)
        $csvPath = storage_path('app/avatar-recover-' . now()->format('Ymd-His') . '.csv');
        $fp = fopen($csvPath, 'w');
        fwrite($fp, "\xEF\xBB\xBF");
        fputcsv($fp, ['id', 'code', 'fullname', 'enter_date', 'image_hong', 'face_image_url_thay_the']);
        foreach ($recover as $e) {
            fputcsv($fp, [$e->id, $e->code, $e->fullname, (string) $e->enter_date, $e->image, $e->face_image_url]);
        }
        fclose($fp);
        $this->info('Đã xuất CSV backup: ' . $csvPath);

        if (!$apply) {
            $this->warn('DRY-RUN xong. Kiểm tra CSV rồi chạy lại với --apply để cập nhật.');
            return 0;
        }

        // APPLY: update qua query builder (KHÔNG dùng Eloquent save -> né đồng bộ ERP)
        $updated = 0;
        foreach ($recover as $e) {
            DB::table('employee_infos')->where('id', $e->id)->update(['image' => $e->face_image_url]);
            $updated++;
        }
        Log::info('human:recover-employee-avatar đã khôi phục ' . $updated . ' avatar', ['csv' => $csvPath]);
        $this->info('Đã cập nhật image = face_image_url cho ' . $updated . ' nhân sự.');

        return 0;
    }

    /**
     * Trả về HTTP status code khi GET (HEAD) một URL, 0 nếu lỗi/timeout.
     */
    private function httpStatus(?string $url): int
    {
        if (empty($url)) {
            return 0;
        }
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_NOBODY => true,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_SSL_VERIFYPEER => false,
        ]);
        curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return $code;
    }
}
