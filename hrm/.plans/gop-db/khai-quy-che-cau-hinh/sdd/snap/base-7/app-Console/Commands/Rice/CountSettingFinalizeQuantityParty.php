<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;
use Modules\Rice\Entities\RiceRegistration;
use Modules\Rice\Entities\Setting\RiceSetting;
use Modules\Rice\Entities\Setting\RiceSettingFinalizeQuantity;

class CountSettingFinalizeQuantityParty extends Command
{
    protected $signature = 'rice:count-setting-finalize-quantity-party {date?}';
    protected $description = 'Tính toán số lượng đăng ký liên hoan';

    public function handle()
    {
        try {
            DB::connection('mysql_tpe')->transaction(function () {
                $date = $this->argument('date') ?? now()->addDay(1)->format('Y-m-d');

                $riceMenuDay = RiceMenuDay::where('date', $date)->first();
                if (!$riceMenuDay || !$riceMenuDay->menu_party_id) {
                    $this->info("Ngày $date không có suất ăn liên hoan");
                    return;
                }

                // $regularTimeRegisterEmployeeBefore = RiceSetting::where('column_name', 'regular_time_register_employee_before')->value('column_value_time') ?? null;

                $partyCancelledOnDay = RiceSetting::where('column_name', 'party_cancelled_on_day')->value('column_value_integer') ?? null;
                $partyAddOnDay = RiceSetting::where('column_name', 'party_add_on_day')->value('column_value_integer') ?? null;

                $riceRegistration = RiceRegistration::where('date', $date)
                    ->where('status_party', 1)
                    ->count();

                RiceSettingFinalizeQuantity::where('date', $date)->where(function ($query) {
                    $query->where('type', RiceSettingFinalizeQuantity::TYPE['party_cancelled_on_day'])
                        ->orWhere('type', RiceSettingFinalizeQuantity::TYPE['party_add_on_day']);
                })->delete();

                if ($partyCancelledOnDay) {
                    RiceSettingFinalizeQuantity::create([
                        'type' => RiceSettingFinalizeQuantity::TYPE['party_cancelled_on_day'],
                        'date' => $date,
                        'quantity_min' => ($riceRegistration - $partyCancelledOnDay > 0) ? ($riceRegistration - $partyCancelledOnDay) : 0,
                        'quantity_max' => null,
                        'quantity' => $riceRegistration,
                    ]);
                }

                if ($partyAddOnDay) {
                    RiceSettingFinalizeQuantity::create([
                        'type' => RiceSettingFinalizeQuantity::TYPE['party_add_on_day'],
                        'date' => $date,
                        'quantity_min' => null,
                        'quantity_max' => $riceRegistration + $partyAddOnDay,
                        'quantity' => $riceRegistration,
                    ]);
                }

                $this->info("Tính toán số lượng đăng ký liên hoan thành công");
            });
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
            Log::error("Lỗi: " . $e->getMessage());
        }
    }
}
