<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Human\Entities\Company;
use Modules\Rice\Entities\RiceEmployeeInfo;
use Modules\Rice\Entities\RiceRegistration;
use Modules\Rice\Entities\RiceRegistrationRiceSupport;
use Modules\Rice\Entities\Setting\RiceSetting;
use Modules\Timesheet\Entities\ShiftDetailEmployeeDate;
use Carbon\CarbonPeriod;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;
use Modules\Timesheet\Entities\BusinessTripAssign;
use Modules\Timesheet\Entities\TimesheetSummary;
use Modules\Timesheet\Enums\BusinessTripAssignStatus;
use Modules\Timesheet\Enums\JobAssignmentNoteStatus;
use Modules\Assign\Entities\AssignRequest;

class StoreRiceSubsidy extends Command
{
    protected $signature = 'rice:store-rice-subsidy {from?} {to?} {rice_employee_info_id?}';
    protected $description = 'Lưu thông tin trợ cấp cơm';

    public function handle()
    {
        try {
            return DB::connection('mysql_tpe')->transaction(
                function () {
                    $from = $this->argument('from') ?? now()->subDay(1)->toDateString();
                    $to = $this->argument('to') ?? now()->subDay(1)->toDateString();
                    $riceEmployeeInfoId = $this->argument('rice_employee_info_id') ?? null;
                    $period = CarbonPeriod::create($from, $to);
                    foreach ($period as $date) {
                        $date = $date->toDateString();
                        $riceCompanyIds = [];

                        $companies = Company::where('status', 1)->get();
                        foreach ($companies as $company) {
                            $riceCompanyIds[] = findRiceCompany($company->id)->id;
                        }

                        $shiftDetailEmployeeDate = ShiftDetailEmployeeDate::select(
                            'shift_detail_employee_dates.employee_info_id',
                            'shift_detail_employee_dates.date'
                        )
                            ->join('working_shifts', function ($join) use ($date) {
                                $join->on('shift_detail_employee_dates.working_shift_id', '=', 'working_shifts.id')
                                    ->whereDate('shift_detail_employee_dates.date', $date)
                                    ->where('working_shifts.no_meal_allowance', 0)
                                    // Ca chỉ ghi nhận chấm công không phát sinh suất cơm.
                                    ->where('working_shifts.is_attendance_only', 0);
                            })
                            ->get()->groupBy('employee_info_id');

                        $riceEmployeeInfoNotRegister = RiceEmployeeInfo::select(
                            'rice_employee_infos.id',
                            'rice_employee_infos.employee_info_id',
                            'rice_employee_infos.employee_id',
                            'rice_employee_infos.rice_company_id',
                            'rice_employee_infos.rice_department_id',
                            'rice_setting_not_ate_working_positions.id as rice_setting_not_ate_working_position_id',
                            'rice_setting_not_ate_companies.id as rice_setting_not_ate_company_id',
                            'rice_setting_not_ate_companies.is_all_working_position',
                        )
                            ->whereIn('rice_employee_infos.rice_company_id', $riceCompanyIds)
                            ->when($riceEmployeeInfoId, function ($query) use ($riceEmployeeInfoId) {
                                $query->where('rice_employee_infos.id', $riceEmployeeInfoId);
                            })
                            ->where('rice_employee_infos.status', 1)
                            ->whereHas('riceCompany', function ($query) {
                                $query->where('status', 1);
                            })
                            ->whereHas('riceDepartment', function ($query) {
                                $query->where('status', 1);
                            })
                            ->leftJoin('rice_registrations', function ($join) use ($date) {
                                $join->on('rice_employee_infos.id', '=', 'rice_registrations.rice_employee_info_id')
                                    ->where('rice_registrations.date', $date);
                            })
                            ->leftJoin(
                                'rice_setting_not_ate_working_positions',
                                'rice_employee_infos.rice_working_position_id',
                                '=',
                                'rice_setting_not_ate_working_positions.rice_working_position_id'
                            )
                            ->leftJoin(
                                'attendances',
                                function ($join) use ($date) {
                                    $join->on('rice_employee_infos.employee_info_id', '=', 'attendances.employee_id')
                                        ->whereDate('attendances.attendance_start_at', '<=', $date)
                                        ->whereDate('attendances.attendance_end_at', '>=', $date)
                                        ->where('attendances.attendance_status', 2);
                                }
                            )
                            ->leftJoin(
                                'rice_setting_not_ate_companies',
                                'rice_employee_infos.rice_company_id',
                                '=',
                                'rice_setting_not_ate_companies.rice_company_id'
                            )

                            ->where(function ($query) use ($date) {
                                $query->whereNull('rice_registrations.id')
                                    ->orWhereIn('rice_registrations.status_regular', [2, 5]);
                            })
                            ->whereNull('attendances.id')
                            ->get();

                        // tiền xử lý dữ liệu tọa độ theo nhân viên trong ngày để tối ưu hiệu suất
                        $employeeInfoIds = $riceEmployeeInfoNotRegister->pluck('employee_info_id')->unique()->toArray();
                        $employeeIds = $riceEmployeeInfoNotRegister->pluck('employee_id')->unique()->toArray();

                        // Map phiếu công tác: employee_id => danh sách [lat,lng]
                        $btaRaw = DB::table('business_trip_assigns')
                            ->join('business_trip_employees', 'business_trip_employees.business_trip_assign_id', '=', 'business_trip_assigns.id')
                            ->whereIn('business_trip_employees.employee_id', $employeeInfoIds)
                            ->where('business_trip_assigns.status', BusinessTripAssignStatus::Approved)
                            ->whereDate('business_trip_assigns.from_time', '<=', $date)
                            ->whereDate('business_trip_assigns.to_time', '>=', $date)
                            ->select('business_trip_employees.employee_id as employee_id', 'business_trip_assigns.place_lat', 'business_trip_assigns.place_lng', 'business_trip_assigns.places')
                            ->get()
                            ->groupBy('employee_id');

                        $btaPositionsByEmp = [];
                        foreach ($btaRaw as $empId => $rows) {
                            $positions = [];
                            foreach ($rows as $row) {
                                if (!empty($row->place_lat) && !empty($row->place_lng)) {
                                    $positions[] = ['lat' => (float) $row->place_lat, 'lng' => (float) $row->place_lng];
                                }
                                if (!empty($row->places)) {
                                    $added = json_decode($row->places, true) ?: [];
                                    foreach ($added as $p) {
                                        if (!empty($p['place_lat']) && !empty($p['place_lng'])) {
                                            $positions[] = ['lat' => (float) $p['place_lat'], 'lng' => (float) $p['place_lng']];
                                        }
                                    }
                                }
                            }
                            if (!empty($positions)) {
                                $btaPositionsByEmp[$empId] = $positions;
                            }
                        }

                        // Map phiếu giao việc: employee_id => danh sách [lat,lng]
                        $jobNoteRaw = DB::table('job_assignment_note_details')
                            ->join('job_assignment_notes', 'job_assignment_notes.id', '=', 'job_assignment_note_details.job_assignment_note_id')
                            ->join('job_assignment_employees', 'job_assignment_employees.job_assignment_note_id', '=', 'job_assignment_notes.id')
                            ->whereIn('job_assignment_employees.employee_id', $employeeInfoIds)
                            ->whereDate('job_assignment_note_details.intend_start_at', '<=', $date)
                            ->whereDate('job_assignment_note_details.intend_end_at', '>=', $date)
                            ->where('job_assignment_notes.status', JobAssignmentNoteStatus::Approved)
                            ->select('job_assignment_employees.employee_id as employee_id', 'job_assignment_note_details.place_lat', 'job_assignment_note_details.place_lng')
                            ->get()
                            ->groupBy('employee_id');

                        $jobNotePositionsByEmp = [];
                        foreach ($jobNoteRaw as $empId => $rows) {
                            $positions = [];
                            foreach ($rows as $row) {
                                if (!empty($row->place_lat) && !empty($row->place_lng)) {
                                    $positions[] = ['lat' => (float) $row->place_lat, 'lng' => (float) $row->place_lng];
                                }
                            }
                            if (!empty($positions)) {
                                $jobNotePositionsByEmp[$empId] = $positions;
                            }
                        }

                        // Map phiếu giao công tác (AssignRequest business_type=2): employee_id => danh sách [lat,lng]
                        $assignReqRaw = DB::table('assign_requests')
                            ->join('assign_request_employees', 'assign_request_employees.assign_request_id', '=', 'assign_requests.id')
                            ->whereIn('assign_request_employees.employee_id', $employeeIds)
                            ->where('assign_requests.type', AssignRequest::PHIEU_CONG_TAC)
                            ->where('assign_requests.status', AssignRequest::DA_DUYET)
                            ->where('assign_requests.business_type', 2)
                            ->whereDate('assign_requests.from_time', '<=', $date)
                            ->whereDate('assign_requests.to_time', '>=', $date)
                            ->select('assign_request_employees.employee_id as employee_id', 'assign_requests.place_lat', 'assign_requests.place_lng', 'assign_requests.places')
                            ->get()
                            ->groupBy('employee_id');

                        $assignReqPositionsByEmp = [];
                        foreach ($assignReqRaw as $empId => $rows) {
                            $positions = [];
                            foreach ($rows as $row) {
                                if (!empty($row->place_lat) && !empty($row->place_lng)) {
                                    $positions[] = ['lat' => (float) $row->place_lat, 'lng' => (float) $row->place_lng];
                                }
                                if (!empty($row->places)) {
                                    $added = json_decode($row->places, true) ?: [];
                                    foreach ($added as $p) {
                                        if (!empty($p['place_lat']) && !empty($p['place_lng'])) {
                                            $positions[] = ['lat' => (float) $p['place_lat'], 'lng' => (float) $p['place_lng']];
                                        }
                                    }
                                }
                            }
                            if (!empty($positions)) {
                                $assignReqPositionsByEmp[$empId] = $positions;
                            }
                        }

                        $isAllCompany = RiceSetting::where('column_name', 'not_eating_is_all_company')->where('category', 'not_eating')->value('column_value_boolean');

                        $riceEmployeeCheckNotPass = [];

                        $riceEmployeeInfoNotRegister = $riceEmployeeInfoNotRegister->filter(function ($riceEmployeeInfo) use ($isAllCompany, &$riceEmployeeCheckNotPass, $date, $btaPositionsByEmp, $jobNotePositionsByEmp, $assignReqPositionsByEmp) {

                            $isPass = true;
                            if (!$riceEmployeeInfo->rice_setting_not_ate_working_position_id && !$riceEmployeeInfo->is_all_working_position && !$isAllCompany) {
                                $isPass = false;
                            }



                            //phiếu công tác (dùng dữ liệu đã tiền xử lý)
                            $empInfoId = $riceEmployeeInfo->employee_info_id;
                            $empId = $riceEmployeeInfo->employee_id;
                            if (!empty($btaPositionsByEmp[$empInfoId])) {
                                foreach ($btaPositionsByEmp[$empInfoId] as $pos) {
                                    $distance = $this->calculateDistance($pos['lat'], $pos['lng']);
                                    if ($distance > 40) {
                                        $isPass = false;
                                        $riceEmployeeCheckNotPass[] = $riceEmployeeInfo->id;
                                        break;
                                    }
                                }
                            }

                            //phiếu giao việc (dùng dữ liệu đã tiền xử lý)
                            if (!empty($jobNotePositionsByEmp[$empInfoId])) {
                                foreach ($jobNotePositionsByEmp[$empInfoId] as $pos) {
                                    $distance = $this->calculateDistance($pos['lat'], $pos['lng']);
                                    if ($distance > 40) {
                                        $isPass = false;
                                        $riceEmployeeCheckNotPass[] = $riceEmployeeInfo->id;
                                        break;
                                    }
                                }
                            }

                            //phiếu giao công tác (AssignRequest business_type = 2) (dùng dữ liệu đã tiền xử lý)
                            if (!empty($assignReqPositionsByEmp[$empId])) {
                                foreach ($assignReqPositionsByEmp[$empId] as $pos) {
                                    $distance = $this->calculateDistance($pos['lat'], $pos['lng']);
                                    if ($distance > 40) {
                                        $isPass = false;
                                        $riceEmployeeCheckNotPass[] = $riceEmployeeInfo->id;
                                        break;
                                    }
                                }
                            }

                            //phiếu giao công tác

                            return $isPass;
                        });

                        $priceRegular = RiceSetting::where('column_name', 'not_eating_price_regular')->where('category', 'not_eating')->value('column_value_integer') ?? 0;

                        $dataInsert = [];

                        $riceEmployeeInfoNotRegister = $riceEmployeeInfoNotRegister->filter(function ($riceEmployeeInfo) use ($riceEmployeeCheckNotPass) {
                            return !in_array($riceEmployeeInfo->id, $riceEmployeeCheckNotPass);
                        });

                        foreach ($riceEmployeeInfoNotRegister as $riceEmployeeInfo) {
                            if (isset($shiftDetailEmployeeDate[$riceEmployeeInfo->employee_info_id])) {
                                $dateRejectCompany = RiceMenuDay::leftJoin(
                                    'rice_menu_day_reject_companies',
                                    'rice_menu_days.id',
                                    '=',
                                    'rice_menu_day_reject_companies.rice_menu_day_id'
                                )
                                    ->where(function ($query) use ($riceEmployeeInfo) {
                                        $query->where('rice_menu_day_reject_companies.rice_company_id', $riceEmployeeInfo->rice_company_id)
                                            ->orWhere('rice_menu_days.reject_all_company_regular', 1);
                                    })
                                    ->where('rice_menu_days.date', $date)
                                    ->get();


                                if ($dateRejectCompany->count() > 0) {
                                    continue;
                                }

                                $timeSheetSummary = TimesheetSummary::where('day', $date)->where('employee_info_id', $riceEmployeeInfo->employee_info_id)->first();

                                if (!$timeSheetSummary || $timeSheetSummary && $timeSheetSummary->labour_day <= 0) {
                                    continue;
                                }


                                $dataInsert[] = [
                                    'rice_company_id' => $riceEmployeeInfo->rice_company_id,
                                    'rice_department_id' => $riceEmployeeInfo->rice_department_id,
                                    'rice_employee_info_id' => $riceEmployeeInfo->id,
                                    'date' => $date,
                                    'support_money' => $priceRegular,
                                    'status_regular' => 1,
                                ];
                            }
                        }


                        RiceRegistrationRiceSupport::where('date', $date)
                            ->where('status_regular', 1)
                            // ->whereIn('rice_employee_info_id', $riceEmployeeInfoNotRegister->pluck('id'))
                            ->when($riceEmployeeInfoId, function ($query) use ($riceEmployeeInfoId) {
                                $query->where('rice_employee_info_id', $riceEmployeeInfoId);
                            })
                            ->delete();


                        RiceRegistrationRiceSupport::insert(collect($dataInsert)->unique()->toArray());

                        Log::info('Lưu thông tin trợ cấp cơm thành công');
                        $this->info('Lưu thông tin trợ cấp cơm thành công');
                    }
                }
            );
        } catch (\Exception $e) {
            $this->error("Lỗi: " . $e->getMessage());
        }
    }

    private function calculateDistance($lat2, $lng2)
    {
        $earthRadius = 6371; // Bán kính Trái Đất (km)

        $dLat = deg2rad($lat2 - config('rice.place_lat_tpe'));
        $dLng = deg2rad($lng2 - config('rice.place_lng_tpe'));

        $a = sin($dLat / 2) * sin($dLat / 2) +
            cos(deg2rad(config('rice.place_lat_tpe'))) * cos(deg2rad($lat2)) *
            sin($dLng / 2) * sin($dLng / 2);

        $c = 2 * atan2(sqrt($a), sqrt(1 - $a));

        return $earthRadius * $c;
    }
}
