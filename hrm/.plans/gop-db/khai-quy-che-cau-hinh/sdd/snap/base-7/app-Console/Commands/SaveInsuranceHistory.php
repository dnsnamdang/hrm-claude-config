<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Services\InsuranceConfigService;

class SaveInsuranceHistory extends Command
{
    // Task chay lưu lịch sử đóng bảo hiểm xã hội
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'create:insurance_history {date=-1}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $insuranceConfigService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(InsuranceConfigService $insuranceConfigService)
    {
        $this->insuranceConfigService = $insuranceConfigService;
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
        } else {
        }

        $this->workShiftDetailService->createTimesheetDetail($date);

        $this->info('Cập nhật thành công');
    }
}
