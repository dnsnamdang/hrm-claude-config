<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\Timesheet;
use Modules\Timesheet\Services\TimesheetSummaryService;
use DB;

class RemoveDupplicate extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'remove:dupplicate';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $timesheetSummaryService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(TimesheetSummaryService $timesheetSummaryService)
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $not_removes = Timesheet::selectRaw('min(id) as id, employee_info_id, verify_date, type, conn_info_id')
            ->groupBy(['employee_info_id', 'verify_date', 'type', 'conn_info_id'])
            ->where('type', '=', 0)
            ->paginate(1000, '', 'page', 1);
        $totalPage = ceil($not_removes->total() / $not_removes->perPage());

        for ($i = 1; $i < $totalPage; $i++) {
            $list_not_remove = Timesheet::selectRaw('min(id) as id, employee_info_id, verify_date, type, conn_info_id')
                ->groupBy(['employee_info_id', 'verify_date', 'type', 'conn_info_id'])
                ->where('type', '=', 0)
                ->paginate(1000, '', 'page', $i);
            foreach ($list_not_remove as $item) {
                $deleted = Timesheet::where('id', '!=', $item->id)
                    ->where('employee_info_id', $item->employee_info_id)
                    ->where('verify_date', $item->verify_date)
                    ->where('conn_info_id', $item->conn_info_id)
                    ->where('type', 0)
                    ->delete();
            }
        }

        $this->info('Cập nhật thành công');
    }
}
