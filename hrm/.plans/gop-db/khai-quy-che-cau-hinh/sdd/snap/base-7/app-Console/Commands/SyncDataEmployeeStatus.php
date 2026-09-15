<?php

namespace App\Console\Commands;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\TpEmployee;
use Modules\Human\Entities\Employee;

class SyncDataEmployeeStatus extends Command
{
  protected $signature = 'sync:employee_status';

    /**
     * The console command description.
     *
     * @var string
     */
  protected $description = 'Command description';
  public function handle()
  {
    $tp_employees = TpEmployee::all();
    foreach($tp_employees as $tp_employee) {
      $employee = Employee::where('employee_info_id', $tp_employee->employee_info_id)->first();
      if($employee) {
        
        if($tp_employee->status != $employee->status) {
          $this->info($tp_employee->email);
          $this->info($tp_employee->status);
          $this->info($employee->status);
          $this->info($employee->email);
          $this->info('--------------------');
        }
      }
    }
  }
}