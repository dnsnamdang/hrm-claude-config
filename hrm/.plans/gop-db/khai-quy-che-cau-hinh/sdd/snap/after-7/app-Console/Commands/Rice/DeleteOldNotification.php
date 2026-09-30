<?php

namespace App\Console\Commands\Rice;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class DeleteOldNotification extends Command
{
    protected $signature = 'rice:delete-old-notification';
    protected $description = 'Xóa thông báo cũ';

    public function handle()
    {
        try {
            $cutoffDate = Carbon::now()->subDays(10)->toDateTimeString();

            DB::table('notifications')
                ->where('type', 'Modules\Rice\Notifications\BaseRiceNotification')
                ->where('created_at', '<', $cutoffDate)
                ->delete();
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }
}
