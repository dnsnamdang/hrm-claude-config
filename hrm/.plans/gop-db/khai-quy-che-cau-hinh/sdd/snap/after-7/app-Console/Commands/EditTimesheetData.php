<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\Timesheet;
use Modules\Timesheet\Services\TimesheetSummaryService;
use DB;

class EditTimesheetData extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'edit:timesheet_data';

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
        $query = DB::select("select * from (select count(*) as count, images,
          GROUP_CONCAT(employee_info_id order by verify_date asc) as ssns,
          GROUP_CONCAT(id order by verify_date asc) as ids
         from timesheets where images is not null group by images) tmp where tmp.count > 1");
        $count = 0;
        foreach ($query as $item) {
            if ($item->images) {
                $arr_ssn = explode(",", $item->ssns);
                $arr_id = explode(",", $item->ids);

                $check = array_unique($arr_ssn);
                if (count($check) > 1) {
                    for ($i = 0; $i < count($arr_ssn) - 1; $i++) {
                        $ssn = $arr_ssn[$i];
                        $id = $arr_id[$i];

                        $timesheet_update = Timesheet::find($id);
                        $timesheet = Timesheet::where('id', '<', $id)
                            ->where('type', '=', 1)
                            ->where('employee_info_id', '=', $ssn)
                            ->orderBy('id', 'desc')->first();
                        $count++;
                        if ($timesheet) {
                            $timesheet_update->images = $timesheet->images;
                            $timesheet_update->save();
                            // $this->info($timesheet->images);
                        } else {
                            $timesheet_update->images = null;
                            $timesheet_update->save();
                        }
                        $this->info('------------------');
                    }
                }
            }
        }


        $this->info('Cập nhật thành công');
    }
}
