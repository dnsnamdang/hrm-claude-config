<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Services\MeetingService;

/**
 * Redmine #11014 — Quy tắc bắt buộc nhập biên bản meeting.
 *
 * Cuộc họp đã kết thúc mà chưa Hoàn thành (chưa chốt biên bản):
 *  - Trước hạn X giờ (cấu hình động, mặc định 3) -> nhắc người tạo meeting 1 lần
 *  - Quá hạn (kết thúc + N ngày, cấu hình động, mặc định 1) -> tự động chuyển trạng thái Hủy
 *    và báo cho người tạo + thành viên nội bộ
 *
 * Chạy định kỳ 15 phút/lần (xem App\Console\Kernel) vì mốc hạn của mỗi cuộc họp
 * rơi vào giờ khác nhau, không thể gom về 1 mốc cố định trong ngày.
 */
class MeetingReportDeadlineCommand extends Command
{
    protected $signature = 'assign:meeting-report-deadline';
    protected $description = 'Nhắc nhập biên bản meeting và tự động hủy cuộc họp quá hạn nhập biên bản';

    public function handle()
    {
        $now = Carbon::now();

        // Chỉ xét meeting đã kết thúc và còn đang chờ biên bản (Lên lịch / Chốt lịch).
        // Nháp và Hoàn thành / Hủy nằm ngoài phạm vi.
        $meetings = Meeting::whereIn('status', [Meeting::LEN_LICH, Meeting::CHOT_LICH])
            ->whereNotNull('end_date')
            ->where('end_date', '<=', $now)
            ->get();

        if ($meetings->isEmpty()) {
            $this->info('Không có cuộc họp nào cần xử lý hạn biên bản.');
            return 0;
        }

        $service = app(MeetingService::class);
        $notified = 0;
        $cancelled = 0;

        foreach ($meetings as $meeting) {
            try {
                $deadline = $meeting->reportDeadline();
                if (!$deadline) {
                    continue;
                }

                // Quá hạn -> hủy luôn, không nhắc nữa
                if ($now->greaterThan($deadline)) {
                    if ($service->autoCancelOverdueMeeting($meeting)) {
                        $cancelled++;
                    }
                    continue;
                }

                $warningAt = $deadline->copy()->subHours($meeting->reportConfig()['warning_hours']);
                if ($now->greaterThanOrEqualTo($warningAt)) {
                    if ($service->notifyReportReminder($meeting)) {
                        $notified++;
                    }
                }
            } catch (\Exception $e) {
                Log::error("Lỗi xử lý hạn biên bản meeting #{$meeting->id}: " . $e->getMessage());
            }
        }

        $this->info("Đã nhắc {$notified} cuộc họp, tự động hủy {$cancelled} cuộc họp quá hạn biên bản.");

        return 0;
    }
}
