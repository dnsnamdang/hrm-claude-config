<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceRegistration;
use Carbon\Carbon;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;
use Modules\Rice\Entities\Setting\RiceSetting;

class ClearRiceRegistrationWhenNotMenu extends Command
{
    protected $signature = 'rice:clear-rice-registration-when-not-menu {date?}';
    protected $description = 'Xóa thông tin ăn cơm khi không có thực đơn';

    public function handle()
    {
        try {
            $tomorrow = $this->argument('date') ?? Carbon::tomorrow()->format('Y-m-d');

            $riceCreateMenuTime = RiceSetting::where('column_name', 'regular_time_create_menu')->first()->column_value_time ?? null;

            if (!$riceCreateMenuTime) {
                $this->info("Không có thời gian tạo thực đơn.");
                return 0;
            }

            $menu = RiceMenuDay::where('date', $tomorrow)->first();

            if (!$menu) {
                RiceRegistration::where('date', $tomorrow)->delete();
                $this->info("Xóa tất cả thông tin ăn cơm khi không có thực đơn ngày $tomorrow.");
                return 0;
            }

            if (!empty($menu->menu_party_id) && empty($menu->menu_regular_id)) {
                RiceRegistration::where('date', $tomorrow)
                    ->where('date', $tomorrow)
                    ->whereNull('status_party')
                    ->delete();

                RiceRegistration::where('date', $tomorrow)
                    ->where('date', $tomorrow)
                    ->whereNotNull('status_party')
                    ->update(['status_regular' => null]);

                $this->info("Xóa thông tin ăn cơm khi có thực đơn liên hoan ngày $tomorrow.");
                return 0;
            }

            $this->info("Có thực đơn cơm thường ngày $tomorrow.");
            return 0;
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }
}
