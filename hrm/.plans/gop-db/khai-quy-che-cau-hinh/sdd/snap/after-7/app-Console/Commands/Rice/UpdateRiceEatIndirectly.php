<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceRegistration;

class UpdateRiceEatIndirectly extends Command
{
    protected $signature = 'rice:update-rice-eat-indirectly {date?}';
    protected $description = 'Cập nhật thông tin ăn cơm gián tiếp';

    public function handle()
    {
        try {
            $date = $this->argument('date') ?? now()->toDateString();

            RiceRegistration::where('status_regular', 1)
                ->where('date', $date)
                ->where('receiving_meal', 2) // gián tiếp
                ->update(['status_regular' => 3]);
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }
}
