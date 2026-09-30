<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\GeneralRegulation;
use Modules\Timesheet\Services\TimesheetSummaryService;
use App\Models\MasterSetting;
use Illuminate\Support\Facades\Log;

class CalcManyTimesheet extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'calc:many_timesheet {from_date=-1} {to_date=-1}';

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
        $this->timesheetSummaryService = $timesheetSummaryService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $employeeInfos = EmployeeInfo::where('status', '=', 1)->get();
        $from_date = $this->argument('from_date');
        $to_date = $this->argument('to_date');
        if ($from_date == -1) {
            $from_date = Carbon::now()->startOfMonth()->format('Y-m-d');
            // $regulation = GeneralRegulation::query()->first();
            // if ($regulation->is_sub_month_before_date) {
            //     if (Carbon::now()->format('Y-m-d') < Carbon::now()->day($regulation->update_working_sub_month_before_date)->format('Y-m-d')) {
            //         $from_date = Carbon::now()->subMonth()->startOfMonth()->format('Y-m-d');
            //     }
            // }
            $isSubMonthBeforeDate = MasterSetting::where('category', 'is_sub_month_before_date')->first();
            $updateWorkingSubMonthBeforeDate = MasterSetting::where('category', 'update_working_sub_month_before_date')->first();
            if ($isSubMonthBeforeDate->content) {
                if (Carbon::now()->format('Y-m-d') < Carbon::now()->day($updateWorkingSubMonthBeforeDate->content)->format('Y-m-d')) {
                    $from_date = Carbon::now()->subMonth()->startOfMonth()->format('Y-m-d');
                }
            }
        }
        if ($to_date == -1) {
            $to_date = Carbon::now()->addDays()->format('Y-m-d');
        }

        Log::info('Tính toán công:  từ ngày ' . $from_date . ' đến ngày ' . $to_date);
        $diff = Carbon::parse($to_date)->diff($from_date);
        $diffDay = $diff->days;
        $start = Carbon::parse($from_date);
        for ($i = 0; $i <= $diffDay; $i++) {
            $date = $start->format('Y-m-d');
            if ($date >= '2023-06-12') {
                $this->timesheetSummaryService->calcAllTimesheet($employeeInfos, $date);
            }
            $start->addDays();
        }
        $this->info('Cập nhật thành công');
    }
}
