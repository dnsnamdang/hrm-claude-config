<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Services\WorkShiftDetailService;

class CreateManyTimesheetDetail extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'create:many_timesheet_detail {from_date=-1} {to_date=-1}';

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
        $from_date = $this->argument('from_date');
        $to_date = $this->argument('to_date');
        $diff = Carbon::parse($to_date)->diff($from_date);
        $diffDay = $diff->days;
        $start = Carbon::parse($from_date);
        for ($i = 0; $i <= $diffDay; $i++) {
            $date = $start->format('Y-m-d');
            $this->workShiftDetailService->createTimesheetDetail($date);
            $start->addDays();
        }
        $this->info('Cập nhật thành công');
    }
}
