<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Modules\Timesheet\Services\WorkShiftDetailService;

class CreateNewTimesheetDetail extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'create:new_timesheet_detail';

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
        $date = Carbon::now()->format('Y-m-d');
        $employeeInfo = EmployeeInfo::where('enter_date', '=', $date)->first();
        if ($employeeInfo) {
            $this->workShiftDetailService->createTimesheetDetail($date);
        }
        $this->info('Cập nhật thành công');
    }
}
