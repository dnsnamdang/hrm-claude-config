<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceRegistration;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\Setting\RiceSetting;

class UpdateRiceRegularNotEat extends Command
{
    protected $signature = 'rice:update-regular-not-eat';

    protected $description = 'Cập nhật trạng thái không ăn cơm suất ăn thường';

    public function handle()
    {
        $now = Carbon::now('Asia/Ho_Chi_Minh');
        $today = $now->toDateString();

        // Lấy thời gian cấu hình để so sánh
        $regularTimeCheckInFaceId = RiceSetting::where('column_name', 'regular_time_check_in_face_id')
            ->value('column_value_time') ?? '23:59:59';

        $regularTime = Carbon::parse($regularTimeCheckInFaceId)->format('H:i');

        // Nếu đúng giờ thì cập nhật status_regular của hôm nay
        if ($now->format('H:i') === $regularTime) {
            RiceRegistration::where('status_regular', 1)
                ->where('date', $today)
                ->update(['status_regular' => 4]);

            $this->info("Updated regular status for {$today}");
            Log::info("Updated regular status for {$today}");
        }

        return 0;
    }
}
