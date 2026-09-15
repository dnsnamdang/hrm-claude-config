<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\Category\RiceConnInfo;
use Modules\Rice\Entities\RiceEmployeeInfo;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;
use Modules\Rice\Entities\Setting\RiceSetting;
use GuzzleHttp\Client;

class UpdateMealCheckinParty extends Command
{
    protected $signature = 'rice:update-meal-checkin-party {date?}';
    protected $description = 'Cập nhật danh sách nhân sự có thể check-in để ăn liên hoan';

    public function handle()
    {

        $date = $this->argument('date') ?? now()->format('Y-m-d');
        $riceMenuDay = RiceMenuDay::where('date', $date)->whereNotNull('menu_party_id')
            ->where('receiving_meal_party', RiceMenuDay::RECEIVING_MEAL_PARTY_CHECKIN)->first();

        if (!$riceMenuDay) {
            $this->info('Không tìm thấy ngày ăn liên hoan hợp lệ.');
            return;
        }

        $partyTimeStart = RiceSetting::where('column_name', 'party_time_start')->value('column_value_time') ?? '00:00:00';
        $partyTimeCheckInFaceId = RiceSetting::where('column_name', 'party_time_checkin_face_id')->value('column_value_time') ?? '23:59:59';
        $connInfos = RiceConnInfo::where('status', 1)->get();

        $beginTime = Carbon::parse($date . ' ' . $partyTimeStart);
        $endTime = Carbon::parse($date . ' ' . $partyTimeCheckInFaceId);

        // Lấy danh sách nhân sự đủ điều kiện check-in ăn liên hoan
        $eligibleEmployees = $this->getRiceSsnEligibleEmployees($date);
        foreach ($eligibleEmployees as $employee) {
            // Kiểm tra nhân sự này có trong danh sách đủ điều kiện không
            $isEligible = $employee->rice_registration_id;

            foreach ($connInfos as $connInfo) {
                // Cập nhật trạng thái trên máy chấm công
                $this->updateMealCheckinMachine($employee, $isEligible, $beginTime, $endTime, $connInfo);
            }
        }

        $this->info('Danh sách check-in ăn liên hoan đã được cập nhật.');
    }

    /**
     * Lấy danh sách nhân sự hợp lệ trong hệ thống
     */
    private function getRiceSsnEligibleEmployees($date)
    {
        return RiceEmployeeInfo::select('rice_employee_infos.rice_ssn', 'rice_registrations.id as rice_registration_id')
            ->where('rice_employee_infos.status', 1)
            ->whereNotNull('rice_employee_infos.rice_ssn')
            ->join('rice_registrations', function ($join) use ($date) {
                $join->on('rice_employee_infos.id', '=', 'rice_registrations.rice_employee_info_id')
                    ->where('rice_registrations.status_party', 1)
                    ->where('rice_registrations.date', $date);
            })
            ->get();
    }

    /**
     * Cập nhật trạng thái check-in trên máy chấm công
     */
    private function updateMealCheckinMachine($employee, $isEligible, $beginTime, $endTime, $connInfo)
    {
        $payload = [
            "UserInfo" => [
                "employeeNo" => (string) $employee['rice_ssn'],
                "valid" => [
                    "enable" => true,
                    "beginTime" => $isEligible ? $beginTime->format('Y-m-d H:i:s') : $beginTime->subDay()->format('Y-m-d H:i:s'),
                    "endTime" => $isEligible ? $endTime->format('Y-m-d H:i:s') : $endTime->subDay()->format('Y-m-d H:i:s')
                ]
            ]
        ];

        $response = Http::withDigestAuth($connInfo->user_name, $connInfo->password)
            ->put('http://' . $connInfo->ip . ':' . $connInfo->port . '/ISAPI/AccessControl/UserInfo/Modify?format=json', $payload);

        if ($response->successful()) {
            $status = $isEligible ? "được phép check-in" : "bị vô hiệu hóa";
            $this->info("Cập nhật thành công: {$employee['rice_ssn']} - $status");
        } else {
            $this->error($response);
            Log::error([
                'error' => $response,
                'employee' => $employee['rice_ssn']
            ]);
        }
    }
}
