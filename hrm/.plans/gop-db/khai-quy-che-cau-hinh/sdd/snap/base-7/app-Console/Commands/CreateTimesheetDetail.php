<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Services\WorkShiftDetailService;

class CreateTimesheetDetail extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'create:timesheet_detail {date=-1} {employee_info_id=null}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $workShiftDetailService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(WorkShiftDetailService $workShiftDetailService)
    {
        $this->workShiftDetailService = $workShiftDetailService;
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
        if ($date == -1) {
            $date = Carbon::now()->addDays(1)->format('Y-m-d');
        }
        if ($date == 'all') {
            $date = Carbon::now()->format('Y-m-d');
        }
        $employeeInfoId = $this->argument('employee_info_id');
        $this->workShiftDetailService->createTimesheetDetail($date, $employeeInfoId);

        $this->info('Cập nhật thành công');
    }
}
