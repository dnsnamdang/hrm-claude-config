<?php

namespace App\Console\Commands\Decision;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\Decision;
use Modules\Decision\Entities\DecisionLaborContract\DecisionLaborContract;
use Modules\Decision\Entities\TerminationLaborContract\TerminationLaborContract;
use Modules\Decision\Services\DecisionLaborContract\DecisionLaborContractService;
use Modules\Decision\Services\TerminationLaborContract\TerminationLaborContractService;

class SyncDataTerminationLaborContract extends Command
{
    protected $signature = 'decision:sync-data-termination-labor-contract {date?}';
    protected $description = 'Gán dữ liệu cho quyết định chấm dứt hợp đồng lao động';

    protected $terminationLaborContractService;
    public function __construct(TerminationLaborContractService $terminationLaborContractService)
    {
        parent::__construct();
        $this->terminationLaborContractService = $terminationLaborContractService;
    }

    public function handle()
    {
        try {
            $date = $this->argument('date') ? Carbon::parse($this->argument('date')) : Carbon::today();

            $terminationLaborContracts = TerminationLaborContract::where('termination_date_start', $date)->whereHas('decision', function ($query) {
                $query->where('status', Decision::STATUS_APPROVED);
            })->get();

            foreach ($terminationLaborContracts as $terminationLaborContract) {
                $this->terminationLaborContractService->syncTerminationLaborContract($terminationLaborContract);
            }

            $this->info('Đã gán dữ liệu quyết định chấm dứt hợp đồng lao động cho ngày ' . $date->format('d/m/Y'));
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi gán dữ liệu cho quyết định chấm dứt hợp đồng lao động.');
        }
    }
}
