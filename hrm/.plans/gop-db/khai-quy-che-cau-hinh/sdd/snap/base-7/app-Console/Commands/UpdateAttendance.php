<?php

namespace App\Console\Commands;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Services\TimesheetSummaryService;
use Modules\Timesheet\Services\EmployeeAttendanceService;
use Modules\Timesheet\Services\AttendanceService;

class UpdateAttendance extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'update:attendance';

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
        $this->employeeAttendanceService->updateDataAll(null, $this->attendanceService);
        $this->info('Cập nhật thành công');
    }
}
