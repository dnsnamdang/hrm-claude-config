<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;
use Modules\Rice\Entities\RiceRegistration;

class UpdateRiceEatIndirectlyParty extends Command
{
    protected $signature = 'rice:update-rice-eat-indirectly-party {date?}';
    protected $description = 'Cập nhật thông tin ăn cơm gián tiếp liên hoan';

    public function handle()
    {
        try {
            $date = $this->argument('date') ?? now()->toDateString();

            $riceMenuDay = RiceMenuDay::where('date', $date)->whereNotNull('menu_party_id')
                ->where('receiving_meal_party', RiceMenuDay::RECEIVING_MEAL_PARTY_INDIRECT)
                ->first();

            if (!$riceMenuDay) {
                return;
            }

            RiceRegistration::where('status_party', 1)
                ->where('date', $date)
                ->update(['status_party' => 3]);
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }
}
