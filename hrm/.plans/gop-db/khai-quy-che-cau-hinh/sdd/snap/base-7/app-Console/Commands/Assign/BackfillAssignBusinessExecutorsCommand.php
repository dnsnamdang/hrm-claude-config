<?php

namespace App\Console\Commands\Assign;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\AssignRequest;
use Modules\Assign\Entities\TpWrAssignTask;
use Modules\Assign\Entities\TpWrAssignTaskExecutor;

class BackfillAssignBusinessExecutorsCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'assign:backfill-executors';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Đồng bộ lại executor bên ERP và cập nhật assign_task_progress cho các phiếu giao công tác đã duyệt (chạy mỗi 30 phút)';

    /**
     * Execute the console command.
     *
     * Mục đích:
     * - Đồng bộ lại executor bên ERP (bảng wr_assign_task_executors – mysql2)
     * - Cập nhật lại assign_task_progress + employee_assign_task_progress
     *   cho các phiếu giao công tác đã duyệt mà trước đây không chạy
     *   syncWrAssignTaskExecutors / updateWrAssignTask.
     */
    public function handle(): int
    {
        $totalRequests = 0;
        $totalHasWrTasks = 0;
        $totalUpdated = 0;

        $this->info('Bắt đầu đồng bộ executor cho các phiếu giao công tác...');

        AssignRequest::query()
            ->where('type', AssignRequest::PHIEU_CONG_TAC)
            ->where('status', AssignRequest::DA_DUYET)
            ->orderBy('id')
            ->chunk(200, function ($requests) use (&$totalRequests, &$totalHasWrTasks, &$totalUpdated) {
                /** @var AssignRequest $request */
                foreach ($requests as $request) {
                    $totalRequests++;

                    // chỉ xử lý những phiếu có wr_assign_task
                    if (! $request->hasWrTask()) {
                        continue;
                    }
                    $totalHasWrTasks++;

                    // lấy danh sách wr_assign_task_id gắn với phiếu này
                    $wrTaskIds = $request->assignBusinessTasks()
                        ->where('jobinvoiceable_type', TpWrAssignTask::class)
                        ->pluck('jobinvoiceable_id')
                        ->toArray();

                    if (empty($wrTaskIds)) {
                        continue;
                    }

                    // kiểm tra xem executor bên ERP đã tồn tại đầy đủ chưa
                    $executedTaskIds = TpWrAssignTaskExecutor::query()
                        ->whereIn('wr_assign_task_id', $wrTaskIds)
                        ->pluck('wr_assign_task_id')
                        ->unique()
                        ->toArray();

                    $missingTaskIds = array_diff($wrTaskIds, $executedTaskIds);

                    // nếu tất cả wr_assign_task đã có executor thì bỏ qua
                    if (empty($missingTaskIds)) {
                        continue;
                    }

                    // dùng hàm đã sửa trong model để đồng bộ lại:
                    // - tự build wr_assign_tasks + employees từ DB
                    // - gọi syncWrAssignTaskExecutors + updateWrAssignTask
                    try {
                        $request->syncAssignBusinessErp([]);
                        $totalUpdated++;
                    } catch (\Throwable $e) {
                        Log::error('BackfillAssignBusinessExecutorsCommand error for assign_request_id ' . $request->id . ': ' . $e->getMessage(), [
                            'exception' => $e,
                        ]);
                        $this->error('Lỗi khi xử lý assign_request_id ' . $request->id . ': ' . $e->getMessage());
                    }
                }
            });

        $message = sprintf(
            'Hoàn thành. Tổng số phiếu: %d, có wr_tasks: %d, đã cập nhật: %d',
            $totalRequests,
            $totalHasWrTasks,
            $totalUpdated
        );

        Log::info('BackfillAssignBusinessExecutorsCommand done. ' . $message);
        $this->info($message);

        return Command::SUCCESS;
    }
}
