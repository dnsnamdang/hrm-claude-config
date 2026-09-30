<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Modules\Human\Entities\Employee;
use Modules\Human\Entities\CompanyEmployee;

class SyncDataEmployeeCompany extends Command
{
    protected $signature = 'sync:data_employee_company';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    public function handle()
    {
        $employees = Employee::all();
        foreach ($employees as $employee) {
            $employee_info = EmployeeInfo::find($employee->employee_info_id);
            if ($employee_info) {
                $company_employee = CompanyEmployee::where('employee_id', $employee->id)
                    ->where('company_id', $employee_info->company_id)->first();
                if (!$company_employee) {
                    $company_employee = new CompanyEmployee();
                    $company_employee->company_id = $employee_info->company_id;
                    $company_employee->employee_id = $employee->id;
                    $company_employee->save();
                }
            }
        }
    }
}
