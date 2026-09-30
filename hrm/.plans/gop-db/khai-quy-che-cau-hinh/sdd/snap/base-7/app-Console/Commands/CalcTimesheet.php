<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Services\TimesheetSummaryService;
use Modules\Timesheet\Services\EmployeeAttendanceService;
use Modules\Timesheet\Services\AttendanceService;

class CalcTimesheet extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'calc:timesheet {date=-1}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $timesheetSummaryService;
    private $attendanceService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(TimesheetSummaryService $timesheetSummaryService, EmployeeAttendanceService $employeeAttendanceService, AttendanceService $attendanceService)
    {
        $this->timesheetSummaryService = $timesheetSummaryService;
        $this->employeeAttendanceService = $employeeAttendanceService;
        $this->attendanceService = $attendanceService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $date = $this->argument('date');
        // $this->employeeAttendanceService->updateDataAll(null, $this->attendanceService);
        if ($date == -1) {
            $date = Carbon::now()->format('Y-m-d');
        }
        $employeeInfos = EmployeeInfo::where('status', '=', 1)->get();
        $this->timesheetSummaryService->calcAllTimesheet($employeeInfos, $date);

        $this->info('Cập nhật thành công');
    }
}
