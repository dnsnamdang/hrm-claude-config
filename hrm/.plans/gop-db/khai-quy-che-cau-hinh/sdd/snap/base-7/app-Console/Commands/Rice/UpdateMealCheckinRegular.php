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
use Modules\Rice\Entities\RiceRegistration;

class UpdateMealCheckinRegular extends Command
{
    protected $signature = 'rice:update-meal-checkin-regular {date?}';
    protected $description = 'Cập nhật danh sách nhân sự có thể check-in để ăn cơm';

    public function handle()
    {

        $date = $this->argument('date') ?? now()->format('Y-m-d');
        $riceMenuDayAll = RiceMenuDay::where('date', $date)->first();

        if (!$riceMenuDayAll) {
            RiceRegistration::where('date', $date)->delete();
            $this->info("Xóa tất cả thông tin ăn cơm khi không có thực đơn ngày $date.");
            Log::info("Xóa tất cả thông tin ăn cơm khi không có thực đơn ngày $date.");
            return;
        }


        $riceMenuDay = RiceMenuDay::where('date', $date)->whereNotNull('menu_regular_id')->first();

        if (!$riceMenuDay) {
            $this->info('Không tìm thấy ngày ăn cơm hợp lệ.');
            Log::info('Không tìm thấy ngày ăn cơm hợp lệ.');

            RiceRegistration::where('date', $date)
                ->where('date', $date)
                ->whereNull('status_party')
                ->delete();

            RiceRegistration::where('date', $date)
                ->where('date', $date)
                ->whereNotNull('status_party')
                ->update(['status_regular' => null]);


            return;
        }

        $regularTime = RiceSetting::where('column_name', 'regular_time_register_employee')->value('column_value_time') ?? '00:00:00';
        $regularTimeCheckInFaceId = RiceSetting::where('column_name', 'regular_time_check_in_face_id')->value('column_value_time') ?? '23:59:59';
        $connInfos = RiceConnInfo::where('status', 1)->get();

        $beginTime = Carbon::parse($date . ' ' . $regularTime);
        $endTime = Carbon::parse($date . ' ' . $regularTimeCheckInFaceId);

        // Lấy danh sách nhân sự đủ điều kiện check-in ăn cơm
        $eligibleEmployees = $this->getRiceSsnEligibleEmployees($date);
        foreach ($eligibleEmployees as $employee) {
            // Kiểm tra nhân sự này có trong danh sách đủ điều kiện không
            $isEligible = $employee->rice_registration_id;

            foreach ($connInfos as $connInfo) {
                // Cập nhật trạng thái trên máy chấm công
                $this->updateMealCheckinMachine($employee, $isEligible, $beginTime, $endTime, $connInfo);
            }
        }

        $this->info('Danh sách check-in ăn cơm đã được cập nhật.');
    }

    /**
     * Lấy danh sách nhân sự hợp lệ trong hệ thống
     */
    private function getRiceSsnEligibleEmployees($date)
    {
        // $riceMenuDayParty = RiceMenuDay::where('date', $date)->whereNotNull('menu_party_id')->first();

        // if (!$riceMenuDayParty) {
        //     return RiceEmployeeInfo::select('rice_employee_infos.rice_ssn', 'rice_registrations.id as rice_registration_id')
        //         ->where('rice_employee_infos.status', 1)
        //         ->whereNotNull('rice_employee_infos.rice_ssn')
        //         ->leftJoin('rice_registrations', function ($join) use ($date) {
        //             $join->on('rice_employee_infos.id', '=', 'rice_registrations.rice_employee_info_id')
        //                 ->where('rice_registrations.date', $date)
        //                 ->where('rice_registrations.receiving_meal', 1)
        //                 ->where('rice_registrations.status_regular', 1);
        //         })
        //         ->get();
        // }

        return RiceEmployeeInfo::select('rice_employee_infos.rice_ssn', 'rice_registrations.id as rice_registration_id')
            ->where('rice_employee_infos.status', 1)
            ->whereNotNull('rice_employee_infos.rice_ssn')
            ->join('rice_registrations', function ($join) use ($date) {
                $join->on('rice_employee_infos.id', '=', 'rice_registrations.rice_employee_info_id')
                    ->where('rice_registrations.date', $date)
                    ->where('rice_registrations.receiving_meal', 1)
                    ->where('rice_registrations.status_regular', 1);
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
                    "beginTime" => $isEligible ? $beginTime->format('Y-m-d\TH:i:s') : $beginTime->subDay()->format('Y-m-d\TH:i:s'),
                    "endTime" => $isEligible ? $endTime->format('Y-m-d\TH:i:s') : $endTime->subDay()->format('Y-m-d\TH:i:s'),
                ]
            ]
        ];

        $response = Http::withDigestAuth($connInfo->user_name, $connInfo->password)
            ->put('http://' . $connInfo->ip . ':' . $connInfo->port . '/ISAPI/AccessControl/UserInfo/Modify?format=json', $payload);

        if ($response->successful()) {
            $status = $isEligible ? "được phép check-in" : "bị vô hiệu hóa";
            $this->info("Cập nhật thành công: {$employee['rice_ssn']} - $status");
            Log::info("Cập nhật thành công: {$employee['rice_ssn']} - $status");
        } else {
            $this->error($response);
            Log::error($response);
        }
    }
}
