<?php

namespace App\Console\Commands;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\TpEmployee;
use Modules\Human\Entities\Employee;

use Modules\Human\Entities\TpWrAssignTask;
use Modules\Human\Entities\TpWrAssignTaskExecutor;
use Modules\Human\Entities\TpWrAssignTaskTimesheet;
use Modules\Timesheet\Entities\BusinessTripAssign;
use Modules\Timesheet\Entities\BusinessTripEmployee;

class SyncTaskAssign extends Command
{
  protected $signature = 'sync:wr_assign';

    /**
     * The console command description.
     *
     * @var string
     */
  protected $description = 'Command description';
  public function handle()
  {
    $tpWrAssignTasks = TpWrAssignTask::where('updated_at', '>=', Carbon::now()->subMinutes(600)->format('Y-m-d H:i:s'))
                                      ->whereNull('parent_id')->get();
    foreach($tpWrAssignTasks as $tpWrAssignTask) {
      $business_trip = BusinessTripAssign::firstOrNew([
        'erp_id' => $tpWrAssignTask->id
      ]);
      $this->info($tpWrAssignTask->id);
      BusinessTripEmployee::where('business_trip_assign_id', $business_trip->id)->delete();
      $business_trip->customer_id = $tpWrAssignTask->customer_id;
      $business_trip->customer_name = $tpWrAssignTask->customer_name;
      $business_trip->company_id = $tpWrAssignTask->company_id;
      $business_trip->status = 2;
      $from_time = Carbon::parse($tpWrAssignTask->expected_start_time)->format('Y-m-d') . ' ' . $tpWrAssignTask->shift_from;
      $to_time = Carbon::parse($tpWrAssignTask->expected_end_time)->format('Y-m-d') . ' ' . $tpWrAssignTask->shift_to;
      $places = json_decode($tpWrAssignTask->places);
      $place = $places[0];
      try {
        if($place && $place->place_lat && $place->place_lng) {
          $business_trip->place = $place->place;
          $business_trip->place_lat = $place->place_lat;
          $business_trip->place_lng = $place->place_lng;
          if(count($places) > 1) {
            array_shift($places);
            $business_trip->places = json_encode($places);
          } else {
            $business_trip->places = null;
          }

          $start_date = Carbon::parse($tpWrAssignTask->expected_start_time);
          $end_date = Carbon::parse($tpWrAssignTask->expected_end_time);
          while ($start_date->lte($end_date)) {
            $date = $start_date->toDateString();
            $tpWrAssignTaskTimesheet = TpWrAssignTaskTimesheet::firstOrNew([
                'wr_assign_task_id' => $tpWrAssignTask->id,
                'day' => $date
            ]);
            $tpWrAssignTaskTimesheet->save();
            $start_date->addDay();
          }
          
          $business_trip->from_time = $from_time;
          $business_trip->to_time = $to_time;
          $business_trip->timekeeping_begin_day = $tpWrAssignTask->shift_from;
          $business_trip->time_to_go = $tpWrAssignTask->time_to_go;
          $business_trip->timekeeping_begin_day = $tpWrAssignTask->timekeeping_begin_day;
          $business_trip->full_timekeeper = $tpWrAssignTask->full_timekeeper;
          $business_trip->fixed_position = $tpWrAssignTask->fixed_position;
          $business_trip->created_by = 13;
          $business_trip->updated_by = 13;
          $business_trip->save();

          $tpWrAssignTaskExecutors = TpWrAssignTaskExecutor::where('wr_assign_task_id', '=', $business_trip->erp_id)->get();
          foreach($tpWrAssignTaskExecutors as $tpWrAssignTaskExecutor) {
            $businessTripEmployee = new BusinessTripEmployee();
            $employee = TpEmployee::find($tpWrAssignTaskExecutor->employee_id);
            $businessTripEmployee->employee_id = $employee->employee_info_id;
            $businessTripEmployee->business_trip_assign_id = $business_trip->id;
            $businessTripEmployee->to_time_actual = $to_time;
            $businessTripEmployee->company_id = $business_trip->company_id;
            $businessTripEmployee->created_by = 13;
            $businessTripEmployee->updated_by = 13;
            $businessTripEmployee->save();

          }
        }
      } catch (\Exception $e) {
        $this->info($e->getMessage());
      }
    }
  }
}
