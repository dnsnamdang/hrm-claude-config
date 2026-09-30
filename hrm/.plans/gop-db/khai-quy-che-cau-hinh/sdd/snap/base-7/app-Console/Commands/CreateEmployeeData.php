<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Services\TimesheetSummaryService;
use Modules\Payroll\Entities\EmployeeInsurance;
use DB;

class CreateEmployeeData extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'create:employee_insurance';

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
        $employee_infos = EmployeeInfo::query()->get();
        foreach ($employee_infos as $employee_info) {
            $employeeInsurance = EmployeeInsurance::where('employee_info_id', $employee_info->id)->first();
            if ($employeeInsurance) {
                $employeeInsurance->insurance_joined = true;
                $employeeInsurance->save();
            } else {
                $employeeInsurance = new EmployeeInsurance();
                $employeeInsurance->insurance_joined = true;
                $employeeInsurance->company_id = 1;
                $employeeInsurance->employee_info_id = $employee_info->id;
                $employeeInsurance->created_by = 13;
                $employeeInsurance->save();
            }
        }

        $this->info('Cập nhật thành công');
    }
}
