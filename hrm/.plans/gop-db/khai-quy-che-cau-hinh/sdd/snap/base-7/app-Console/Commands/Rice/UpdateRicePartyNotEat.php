<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceRegistration;
use Carbon\Carbon;
use Modules\Rice\Entities\Setting\RiceSetting;

class UpdateRicePartyNotEat extends Command
{
    protected $signature = 'rice:update-party-not-eat';

    protected $description = 'Cập nhật trạng thái không ăn cơm liên hoan';

    public function handle()
    {
        $now = Carbon::now('Asia/Ho_Chi_Minh');
        $today = $now->toDateString();

        RiceRegistration::where('status_party', 1)
            ->where('date', $today)
            ->update(['status_party' => 4]);

        $this->info("Updated party status for {$today}");


        return 0;
    }
}
