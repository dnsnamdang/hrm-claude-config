<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Modules\Payroll\Entities\EmployeeSalaryHistory;
use Modules\Human\Entities\EmployeeInfo as HumanEmployeeInfo;
use Modules\Timesheet\Entities\Attendance;
use Modules\Timesheet\Enums\AttendanceStatus;
use Modules\Timesheet\Enums\LeaveTypeCode;

class RestoreInsuranceAfterMaternity extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'timesheet:restore-after-maternity';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Khôi phục BHXH/Công đoàn sau khi kết thúc nghỉ thai sản';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $today = Carbon::today()->toDateString();

        // Lấy danh sách nhân sự có lịch sử lương đang đánh dấu is_maternity = 1
        $employeeInfoIds = EmployeeSalaryHistory::where('is_maternity', 1)
            ->pluck('employee_info_id')
            ->unique()
            ->values();

        $restored = 0;
        foreach ($employeeInfoIds as $employeeInfoId) {
            $employeeInfo = HumanEmployeeInfo::find($employeeInfoId);
            if (!$employeeInfo) continue;

            $salary = $employeeInfo->getSalaryHistoryEffectiveAttribute();
            if (!$salary || (int)($salary->is_maternity ?? 0) !== 1) continue;

            // Kiểm tra còn đang trong kỳ nghỉ thai sản tại thời điểm hiện tại không
            $isActiveMaternity = Attendance::select('attendances.id')
                ->join('leave_types', 'leave_types.id', '=', 'attendances.leave_type_id')
                ->where('leave_types.code', LeaveTypeCode::getKey(LeaveTypeCode::LT_NTS))
                ->where('attendances.attendance_status', AttendanceStatus::Approved)
                ->where('attendances.employee_id', $employeeInfoId)
                ->whereDate('attendances.attendance_start_at', '<=', $today)
                ->whereDate('attendances.attendance_end_at', '>=', $today)
                ->exists();

            if ($isActiveMaternity) {
                continue;
            }

            // Không còn kỳ nghỉ thai sản => Khôi phục trạng thái BHXH/CĐ
            $salary->has_insurance = $salary->has_insurance_maternity;
            $salary->has_union = $salary->has_union_maternity;
            $salary->save();

            $salary->has_insurance_maternity = 0;
            $salary->has_union_maternity = 0;
            $salary->is_maternity = 0;
            $salary->save();

            $restored++;
        }

        $this->info("Đã khôi phục BHXH/CĐ cho {$restored} nhân sự.");
        return 0;
    }
}
