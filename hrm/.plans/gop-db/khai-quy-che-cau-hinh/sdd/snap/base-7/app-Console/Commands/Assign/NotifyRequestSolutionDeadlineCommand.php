<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\RequestSolution;
use Modules\Assign\Services\RequestSolutionService;
use Modules\Timesheet\Services\EmployeeInfoService;

class NotifyRequestSolutionDeadlineCommand extends Command
{
    protected $signature = 'assign:notify-request-solution-deadline';
    protected $description = 'Gửi cảnh báo yêu cầu làm giải pháp sắp đến hạn tiếp nhận';

    public function handle()
    {
        $requestSolutions = RequestSolution::where('status', RequestSolution::STATUS_CHO_TIEP_NHAN)
            ->whereNotNull('need_receive_date')
            ->whereDate('need_receive_date', '>=', now()->toDateString())
            ->whereNull('deadline_notified_at')
            ->get();


        if ($requestSolutions->isEmpty()) {
            $this->info('Không có yêu cầu nào cần cảnh báo.');
            return 0;
        }

        $service = app(RequestSolutionService::class);
        $notifiedCount = 0;

        foreach ($requestSolutions as $requestSolution) {
            try {
                $warningDate = $service->calculateWarningDate($requestSolution);
                if (!$warningDate) continue;

                if (now()->gte($warningDate)) {
                    $this->sendDeadlineNotification($requestSolution);
                    $requestSolution->update(['deadline_notified_at' => now()]);
                    $notifiedCount++;
                }
            } catch (\Exception $e) {
                Log::error("Lỗi cảnh báo deadline request solution #{$requestSolution->id}: " . $e->getMessage());
            }
        }

        $this->info("Đã gửi cảnh báo cho {$notifiedCount} yêu cầu.");
        return 0;
    }

    private function sendDeadlineNotification(RequestSolution $requestSolution)
    {
        $departmentId = $requestSolution->receive_dept;
        $companyId = $requestSolution->company_id;

        $infoIdsInDept = \Modules\Timesheet\Entities\EmployeeInfo::where('department_id', $departmentId)->pluck('id')->toArray();
        $employeeIdsInDept = \Modules\Timesheet\Entities\Employee::whereIn('employee_info_id', $infoIdsInDept)->pluck('id')->toArray();

        $employeeIds = array_merge(
            // Người quản lý phòng ban (gồm cả cờ "quản lý tất cả phòng ban" tổng lẫn theo từng công ty)
            employeeIdsManagingDepartment($departmentId, $companyId),
            $employeeIdsInDept
        );

        $permission = \App\Models\Permission::where('name', 'Tiếp nhận yêu cầu làm giải pháp')->first();
        if (!$permission) return;

        $roleIds = DB::table('role_has_permissions')
            ->where('company_id', $companyId)
            ->where('permission_id', $permission->id)
            ->pluck('role_id');

        $finalEmployeeIds = DB::table('employee_has_roles')
            ->where('company_id', $companyId)
            ->whereIn('role_id', $roleIds)
            ->whereIn('employee_id', $employeeIds)
            ->pluck('employee_id');

        $employeeInfoIds = \Modules\Timesheet\Entities\Employee::whereIn('id', $finalEmployeeIds)
            ->pluck('employee_info_id')
            ->unique()
            ->toArray();

        if (empty($employeeInfoIds)) return;

        $deadline = Carbon::parse($requestSolution->need_receive_date)->format('d/m/Y H:i');

        $data = [
            'url' => '/assign/request-solution/' . $requestSolution->id,
            'title' => 'Cảnh báo yêu cầu làm giải pháp sắp đến hạn',
            'content' => "Yêu cầu {$requestSolution->code} - {$requestSolution->title} sắp đến hạn tiếp nhận ({$deadline})",
            'type' => 'request_solution_deadline',
            'id' => $requestSolution->id,
        ];

        foreach ($employeeInfoIds as $employeeInfoId) {
            EmployeeInfoService::sendNotification($employeeInfoId, $data, true);
        }
    }
}
