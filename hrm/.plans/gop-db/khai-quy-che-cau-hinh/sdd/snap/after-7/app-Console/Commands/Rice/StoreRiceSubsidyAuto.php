<?php

namespace App\Console\Commands\Rice;

use App\Models\MasterSetting;
use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class StoreRiceSubsidyAuto extends Command
{
    protected $signature = 'rice:auto-store-rice-subsidy';
    protected $description = 'Tự động chạy trợ cấp cơm từ đầu tháng (hoặc đầu tháng trước theo cấu hình) đến ngày hiện tại';

    public function handle()
    {
        $fromDate = Carbon::now()->startOfMonth()->format('Y-m-d');
        $toDate = Carbon::now()->format('Y-m-d');

        $isSubMonthBeforeDate = MasterSetting::where('category', 'is_sub_month_before_date')->first();
        $updateWorkingSubMonthBeforeDate = MasterSetting::where('category', 'update_working_sub_month_before_date')->first();

        if ($isSubMonthBeforeDate && $isSubMonthBeforeDate->content) {
            if ($updateWorkingSubMonthBeforeDate && $updateWorkingSubMonthBeforeDate->content) {
                if (Carbon::now()->format('Y-m-d') < Carbon::now()->day($updateWorkingSubMonthBeforeDate->content)->format('Y-m-d')) {
                    $fromDate = Carbon::now()->subMonth()->startOfMonth()->format('Y-m-d');
                }
            }
        }

        $this->info("Chạy rice:store-rice-subsidy từ {$fromDate} đến {$toDate}");
        Artisan::call('rice:store-rice-subsidy', [
            'from' => $fromDate,
            'to' => $toDate,
        ]);

        $this->info('Hoàn tất gọi rice:store-rice-subsidy');
    }
}
