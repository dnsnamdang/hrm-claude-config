<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Services\TimesheetSummaryService;

class CalcEmployeeTimesheet extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'calc:employee_timesheet {employee_info_id=-1} {from_date=-1} {to_date=-1}';

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
        $this->timesheetSummaryService = $timesheetSummaryService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $employeeInfoId = $this->argument('employee_info_id');
        $from_date = $this->argument('from_date');
        $to_date = $this->argument('to_date');
        if ($from_date == -1) {
            $from_date = Carbon::now()->startOfMonth()->format('Y-m-d');
        }
        if ($to_date == -1) {
            $to_date = Carbon::now()->format('Y-m-d');
        }
        $diff = Carbon::parse($to_date)->diff($from_date);
        $diffDay = $diff->days;
        $start = Carbon::parse($from_date);
        for ($i = 0; $i <= $diffDay; $i++) {
            $date = $start->format('Y-m-d');
            $employeeInfo = EmployeeInfo::where('id', '=', $employeeInfoId)->first();
            if ($employeeInfo) {
                $this->timesheetSummaryService->calcTimesheetEmployee($employeeInfo, $date);
            }
            $start->addDays();
        }

        $this->info('Cập nhật thành công');
    }
}
