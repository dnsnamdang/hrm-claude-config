<?php

namespace App\Console\Commands;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\TimesheetDetail;
use Modules\Timesheet\Entities\TimesheetSummary;

class DeleteEmployeeTimesheet extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'delete:employee_timesheet {employee_info_id} {from_date} {to_date?} {--force}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Xoá timesheet_summaries + timesheet_details của 1 nhân sự theo khoảng ngày';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $employeeInfoId = $this->argument('employee_info_id');
        $fromDate = $this->argument('from_date');
        $toDate = $this->argument('to_date') ?: $fromDate;

        try {
            $fromDate = Carbon::createFromFormat('Y-m-d', $fromDate)->format('Y-m-d');
            $toDate = Carbon::createFromFormat('Y-m-d', $toDate)->format('Y-m-d');
        } catch (\Exception $e) {
            $this->error('Ngày không hợp lệ, định dạng đúng: Y-m-d (VD: 2026-07-02)');
            return 1;
        }

        if ($fromDate > $toDate) {
            $this->error('from_date phải nhỏ hơn hoặc bằng to_date');
            return 1;
        }

        $employeeInfo = EmployeeInfo::where('id', '=', $employeeInfoId)->first();
        if (!$employeeInfo) {
            $this->error("Không tìm thấy nhân sự với employee_info_id = {$employeeInfoId}");
            return 1;
        }

        $summaryIds = TimesheetSummary::where('employee_info_id', '=', $employeeInfoId)
            ->whereBetween('day', [$fromDate, $toDate])
            ->pluck('id');

        if ($summaryIds->isEmpty()) {
            $this->info("Không có dữ liệu chấm công của nhân sự {$employeeInfo->fullname} (id={$employeeInfoId}) từ {$fromDate} đến {$toDate}");
            return 0;
        }

        $detailIds = TimesheetDetail::whereIn('timesheet_summary_id', $summaryIds)->pluck('id');

        $counts = [
            'timesheet_details' => $detailIds->count(),
            'timesheet_summaries' => $summaryIds->count(),
        ];

        $this->info("Nhân sự: {$employeeInfo->fullname} - {$employeeInfo->code} (employee_info_id={$employeeInfoId})");
        $this->info("Khoảng ngày: {$fromDate} → {$toDate}");
        $this->table(
            ['Bảng', 'Số bản ghi sẽ xoá'],
            collect($counts)->map(function ($count, $table) {
                return [$table, $count];
            })->values()->toArray()
        );

        if (!$this->option('force') && !$this->confirm('Xác nhận xoá toàn bộ dữ liệu trên?')) {
            $this->info('Đã huỷ, không xoá gì.');
            return 0;
        }

        DB::transaction(function () use ($summaryIds, $detailIds) {
            TimesheetDetail::whereIn('id', $detailIds)->delete();
            TimesheetSummary::whereIn('id', $summaryIds)->delete();
        });

        foreach ($counts as $table => $count) {
            $this->info("Đã xoá {$count} bản ghi {$table}");
        }

        return 0;
    }
}
