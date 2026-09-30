<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\TimesheetMonthSummaryDetail;
use Modules\Timesheet\Services\TimesheetMonthSummaryService;

class SendMail extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'send:send_mail {summary_id=-1}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $timesheetMonthSummaryService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(TimesheetMonthSummaryService $timesheetMonthSummaryService)
    {
        $this->timesheetMonthSummaryService = $timesheetMonthSummaryService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $summary_id = $this->argument('summary_id');
        $timesheet_month_summary_details = TimesheetMonthSummaryDetail::where('timesheet_month_summary_id', '=', $summary_id)->get();
        foreach ($timesheet_month_summary_details as $timesheet_month_summary_detail) {
            $this->timesheetMonthSummaryService->sendOneMail($timesheet_month_summary_detail->id);
        }
        $this->info('Cập nhật thành công');
    }
}
