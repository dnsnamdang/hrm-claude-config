<?php

namespace App\Console\Commands;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\Task\Task;
use Modules\Assign\Entities\Task\TaskProgressReportRule;
use Modules\Timesheet\Entities\Employee;
use Modules\Timesheet\Services\EmployeeInfoService;

class NotifyTaskReport extends Command
{
    protected $signature = 'assign:notify-task-report';
    protected $description = 'Gửi notification nhắc báo cáo tiến độ task (4 mốc: 08:30, 11:30, 14:30, 17:30)';

    public function handle()
    {
        $today = Carbon::today();

        $tasks = Task::with([
            'progressReportRule',
            'progressLogs' => function ($q) use ($today) {
                $q->where('report_date', $today->toDateString())
                    ->where('progress_pct', '>', 0);
            },
        ])
            ->where('status', Task::IN_PROGRESS)
            ->whereHas('progressReportRule', function ($q) {
                $q->where('is_active', true);
            })
            ->get();

        $userTaskCounts = [];
        foreach ($tasks as $task) {
            if (!$this->isReportDueToday($task->progressReportRule, $today)) continue;
            if ($task->progressLogs->isNotEmpty()) continue;

            $assigneeId = $task->assignee_id;
            if (!$assigneeId) continue;

            $userTaskCounts[$assigneeId] = ($userTaskCounts[$assigneeId] ?? 0) + 1;
        }

        if (empty($userTaskCounts)) {
            return 0;
        }

        $this->sendInAppNotifications($userTaskCounts);

        return 0;
    }

    private function sendInAppNotifications(array $userTaskCounts)
    {
        $employees = Employee::whereIn('id', array_keys($userTaskCounts))
            ->get(['id', 'employee_info_id']);

        foreach ($employees as $employee) {
            if (!$employee->employee_info_id) continue;

            $taskCount = $userTaskCounts[$employee->id] ?? 0;

            try {
                EmployeeInfoService::sendNotification($employee->employee_info_id, [
                    'url'   => '/assign/tasks/daily-report',
                    'title' => "Bạn có <b>{$taskCount}</b> task cần báo cáo tiến độ hôm nay",
                    'type'  => 'task_progress_report_reminder',
                    'id'    => null,
                ], true);
            } catch (\Throwable $e) {
                Log::error("NotifyTaskReport: lỗi gửi cho employee_info_id={$employee->employee_info_id}: " . $e->getMessage());
            }
        }
    }

    private function isReportDueToday($rule, Carbon $today)
    {
        if (!$rule || !$rule->is_active) return false;

        switch ($rule->cycle_type) {
            case TaskProgressReportRule::CYCLE_DAILY:
                return true;
            case TaskProgressReportRule::CYCLE_WEEKLY:
                return in_array($today->dayOfWeek, $rule->week_days ?? []);
            case TaskProgressReportRule::CYCLE_MONTHLY:
                return $today->day == ($rule->month_day ?? 1);
            default:
                return false;
        }
    }
}
