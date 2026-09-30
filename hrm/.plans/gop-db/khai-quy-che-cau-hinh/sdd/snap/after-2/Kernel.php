<?php

namespace App\Console;

use App\Models\MasterSetting;
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Modules\Decision\Console\DecisionKernel;
use Modules\Rice\Console\RiceKernel;

class Kernel extends ConsoleKernel
{
    /**
     * The Artisan commands provided by your application.
     *
     * @var array
     */
    protected $commands = [
        //
    ];

    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        // Gọi Kernel của module Rice
        $useRice = MasterSetting::where('category', 'use_rice')->first() ?? null;
        if ($useRice && $useRice->content) {
            $riceKernel = new RiceKernel($this->app, $this->events);
            $riceKernel->schedule($schedule);
        }

        // Gọi Kernel của module Decision
        $useDecision = MasterSetting::where('category', 'use_decision')->first() ?? null;
        if ($useDecision && $useDecision->content) {
            $decisionKernel = new DecisionKernel($this->app, $this->events);
            $decisionKernel->schedule($schedule);
        }

        // Chạy cập nhật trạng thái tạm nghỉ lúc 01:00 hằng ngày
        $schedule->command('human:update-leave-status')->dailyAt('01:00');
        // Chạy cập nhật quay lại làm việc lúc 01:00 hằng ngày
        $schedule->command('human:update-return-status')->dailyAt('01:00');
        // Khôi phục BHXH/CĐ sau khi hết kỳ nghỉ thai sản lúc 01:10 hằng ngày
        $schedule->command('timesheet:restore-after-maternity')->dailyAt('01:10');
        // Đồng bộ executor cho các phiếu giao công tác mỗi 30 phút
        $schedule->command('assign:backfill-executors')->everyThirtyMinutes();
        // Nhắc báo cáo tiến độ task: cron chạy 30p/lần, command tự gate 4 mốc cố định 08:30/11:30/14:30/17:30
        $schedule->command('assign:notify-task-report')
            ->cron('30 8,11,14,17 * * *')
            ->timezone('Asia/Ho_Chi_Minh');

        // Tính lại tiến độ giải pháp và hạng mục mỗi 30 phút
        $schedule->command('assign:calculate-progress')->everyThirtyMinutes();

        // Báo giá dịch vụ quá hạn hiệu lực -> "Hết hiệu lực". Giữ đúng khung giờ của ERP
        // (`update:quotations-expried` chạy 00:30) để hai hệ thống không chuyển lệch nhau.
        $schedule->command('customer-care:expire-quotations')
            ->dailyAt('00:30')
            ->withoutOverlapping();

        // Đóng nhu cầu KH quá ngày dự kiến triển khai mà chưa lập được dự án TKT
        // (feature bao-cao-cskh-tiem-nang). Mốc là NGÀY nên chạy 1 lần/ngày là đủ.
        $schedule->command('assign:close-expired-customer-demands')
            ->dailyAt('01:20')
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping();

        // Nhắc nhập biên bản meeting + tự động hủy cuộc họp quá hạn biên bản (Redmine #11014).
        // 15 phút/lần vì hạn của mỗi cuộc họp rơi vào giờ khác nhau, không gom về 1 mốc cố định được.
        $schedule->command('assign:meeting-report-deadline')
            ->everyFifteenMinutes()
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping();

        // Cảnh báo yêu cầu làm giải pháp sắp đến hạn tiếp nhận — chạy lúc 08:00 hằng ngày
        $schedule->command('assign:notify-request-solution-deadline')
            ->dailyAt('08:00')
            ->timezone('Asia/Ho_Chi_Minh');

        // Thông báo HĐLĐ sắp hết hạn (3 lần: còn 15, 10, 5 ngày) — chạy lúc 08:00 hằng ngày
        $schedule->command('contracts:notify-expiring')
            ->dailyAt('08:00')
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping();

        // Đồng bộ trạng thái nhân sự HRM → ERP lúc 18:00 hằng ngày
        $schedule->command('check:employee-status-diff')->dailyAt('18:00');

        // Cập nhật tỷ giá ngoại tệ từ Vietcombank — chuyển từ ERP (`currency:update_exchange_rate`),
        // giữ nguyên mốc 03:00. Lịch bên ERP đã được TẮT 2026-08-03 (comment trong
        // TanPhatDev/app/Console/Kernel.php, nhánh gop_db) vì 2 hệ dùng chung bảng `currencies`.
        // => Đây là nơi DUY NHẤT còn chạy tự động.
        // `emailOutputTo` giữ y như bản ERP để vẫn nhận mail kết quả mỗi sáng.
        // ⚠️ HRM chưa khai `ADMIN_EMAIL` trong .env -> đang rơi về mặc định giống ERP.
        $schedule->command('finance:update-exchange-rate')
            ->dailyAt('03:00')
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping()
            ->emailOutputTo(env('ADMIN_EMAIL', 'namdangit@gmail.com'));
    }

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__ . '/Commands');

        require base_path('routes/console.php');
    }
}
