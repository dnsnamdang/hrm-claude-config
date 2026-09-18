<?php

namespace App\Console\Commands;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Services\TimesheetSummaryService;
use Modules\Timesheet\Services\EmployeeAttendanceService;
use Modules\Timesheet\Services\AttendanceService;
use Modules\Timesheet\Entities\TimesheetSummary;
use Modules\Timesheet\Entities\EmployeeAttendance;

class UpdateTruncatedDay extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'update:truncated_day';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $timesheetSummaryService;
    private $employeeAttendanceService;
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
        $employeeInfos = EmployeeInfo::where('company_id', 1)->get();
        foreach($employeeInfos as $employeeInfo) {
          $timesheetSummary = TimesheetSummary::where('employee_info_id', $employeeInfo->id)
                                              ->where('day', '2022-12-31')->first();
          if($timesheetSummary && $employeeInfo->id != 192 && $timesheetSummary->work_day_phep > 0) {
            $employeeAttendance = EmployeeAttendance::where('employee_info_id', $employeeInfo->id )->where('current_year', 2022)->first();
            $newData = $employeeAttendance->truncated_day + $timesheetSummary->work_day_phep;
            if($newData > 1) {
              $this->info($employeeInfo->id);
            }
            $employeeAttendance->truncated_day = $newData;
            $employeeAttendance->save();
          }
        }
    }
}
