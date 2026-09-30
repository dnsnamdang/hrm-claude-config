<?php

namespace App\Console\Commands\Decision;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\DecisionLaborContract\DecisionLaborContract;
use Modules\Decision\Services\DecisionLaborContract\DecisionLaborContractService;

class SyncDataLaborContract extends Command
{
    protected $signature = 'decision:sync-data-labor-contract {date?}';
    protected $description = 'Gán dữ liệu cho hợp đồng lao động';

    protected $decisionLaborContractService;
    public function __construct(DecisionLaborContractService $decisionLaborContractService)
    {
        parent::__construct();
        $this->decisionLaborContractService = $decisionLaborContractService;
    }

    public function handle()
    {
        try {
            $date = $this->argument('date') ? Carbon::parse($this->argument('date')) : Carbon::today();

            $decisionLaborContracts = DecisionLaborContract::where('start_date', $date)->where('status', DecisionLaborContract::STATUS_APPROVED)->get();

            foreach ($decisionLaborContracts as $decisionLaborContract) {
                $this->decisionLaborContractService->storeEmployeeSalaryHistory($decisionLaborContract);
            }

            $this->info('Đã gán dữ liệu cho hợp đồng lao động cho ngày ' . $date->format('d/m/Y'));
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi gán dữ liệu cho hợp đồng lao động.');
        }
    }
}
