<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Rice\Entities\RiceRegistration;
use Modules\Rice\Entities\RiceRegistrationHistory;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\RiceEmployeeInfo;

class UpdateCloseWaitingRegisterRiceRegular extends Command
{
    protected $signature = 'rice:update-close-waiting-register-rice-regular {date?}';
    protected $description = 'Cập nhật thông tin ăn cơm gián tiếp';

    public function handle()
    {
        try {
            $date = $this->argument('date') ?? now()->toDateString();

            $riceRegistrations = RiceRegistration::where('status_regular', 6)
                ->where('date', $date)
                ->get();

            foreach ($riceRegistrations as $riceRegistration) {
                $riceRegistration->update(['status_regular' => 2, 'queue_regular' => null]);
                $this->syncHistory($riceRegistration, RiceRegistrationHistory::STATUS_REGULAR_WAITING_RICE_CANCEL);
                $riceEmployeeInfo = RiceEmployeeInfo::find($riceRegistration->rice_employee_info_id);

                $domains = config('rice.register_domains');
                $client = new Client();

                foreach ($domains as $domain) {
                    try {
                        $response = $client->post("$domain/api/v1/rice/notification/close-waiting-rice-cancel", [
                            'json' => [
                                'date' => $date,
                                'rice_employee_info' => $riceEmployeeInfo
                            ]
                        ]);
                    } catch (\Exception $e) {
                        Log::error($e);
                    }
                }
            }
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }


    public function syncHistory($riceRegistration, $status)
    {
        RiceRegistrationHistory::create([
            'rice_registration_id' => $riceRegistration->id,
            'status' => $status,
        ]);
    }
}
