<?php

namespace App\Console\Commands\Decision;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\AppendixLaborContract\AppendixLaborContract;
use Modules\Decision\Services\AppendixLaborContract\AppendixLaborContractService;

class SyncDataAppendixLaborContract extends Command
{
    protected $signature = 'decision:sync-data-appendix-labor-contract {date?}';
    protected $description = 'Gán dữ liệu cho phụ lục hợp đồng lao động';

    protected $appendixLaborContractService;
    public function __construct(AppendixLaborContractService $appendixLaborContractService)
    {
        parent::__construct();
        $this->appendixLaborContractService = $appendixLaborContractService;
    }


    public function handle()
    {
        try {
            $date = $this->argument('date') ? Carbon::parse($this->argument('date')) : Carbon::today();

            $appendixLaborContracts = AppendixLaborContract::where('effective_date', $date)->where('status', AppendixLaborContract::STATUS_APPROVED)->get();

            foreach ($appendixLaborContracts as $appendixLaborContract) {
                $this->appendixLaborContractService->syncDataAppendixLaborContract($appendixLaborContract);
            }

            $this->info('Đã gán dữ liệu cho phụ lục hợp đồng lao động cho ngày ' . $date->format('d/m/Y'));
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi gán dữ liệu cho phụ lục hợp đồng lao động.');
        }
    }
}
