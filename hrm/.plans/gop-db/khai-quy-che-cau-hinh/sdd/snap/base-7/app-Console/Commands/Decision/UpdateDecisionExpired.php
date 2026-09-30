<?php

namespace App\Console\Commands\Decision;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\Decision;
use Modules\Decision\Entities\DecisionLaborContract\DecisionLaborContract;
use Modules\Decision\Entities\DecisionAppointPersonnel\DecisionAppointPersonnel;
use Modules\Decision\Entities\DecisionTransferPersonnel\DecisionTransferPersonnel;
use Modules\Decision\Entities\SalaryChange\SalaryChange;

class UpdateDecisionExpired extends Command
{
    protected $signature = 'decision:update-decision-expired {date?}';
    protected $description = 'Cập nhật trạng thái hết hạn của quyết định';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $dateInput = $this->argument('date');
        $date = $dateInput ? Carbon::parse($dateInput) : Carbon::yesterday();

        Log::info("Bắt đầu cập nhật quyết định hết hạn cho ngày: {$date->toDateString()}");

        $decisionExpiredIds = [];

        // Lấy các quyết định lao động đã duyệt, kết thúc đúng ngày
        $decisionLaborContractsExpired = DecisionLaborContract::select('id')
            ->where('status', DecisionLaborContract::STATUS_APPROVED)
            ->whereDate('end_date', $date->toDateString())
            ->get()
            ->pluck('id')
            ->toArray();

        if (empty($decisionLaborContractsExpired)) {
            Log::info("Không có hợp đồng lao động nào hết hạn vào ngày {$date->toDateString()}.");
            return;
        }

        //Lấy các quyết định bổ nhiệm liên quan đến các hợp đồng đã hết hạn
        $decisionIdsInAppointPersonnel = DecisionAppointPersonnel::whereIn('decision_labor_contract_id', $decisionLaborContractsExpired)
            ->pluck('decision_id')
            ->toArray();

        //Lấy các quyết định điều chuyển nhân sự
        $decisionIdsTransferPersonnel = DecisionTransferPersonnel::whereIn('decision_labor_contract_id', $decisionLaborContractsExpired)
            ->pluck('decision_id')
            ->toArray();

        $decisionSalaryChangeIds = SalaryChange::whereIn('decision_labor_contract_id', $decisionLaborContractsExpired)
            ->pluck('decision_id')
            ->toArray();

        $decisionExpiredIds = array_unique(array_merge($decisionExpiredIds, $decisionIdsInAppointPersonnel, $decisionIdsTransferPersonnel, $decisionSalaryChangeIds));

        if (empty($decisionExpiredIds)) {
            Log::info("Không có quyết định nào liên quan đến hợp đồng hết hạn.");
            return;
        }

        // Cập nhật trạng thái của các quyết định
        foreach ($decisionExpiredIds as $decisionId) {
            try {
                $decision = Decision::find($decisionId);

                if (!$decision) {
                    Log::warning("Không tìm thấy quyết định ID: {$decisionId}");
                    continue;
                }

                $decision->update([
                    'status' => Decision::STATUS_EXPIRED,
                ]);

                Log::info("Cập nhật trạng thái hết hạn cho quyết định ID {$decisionId}");
            } catch (Exception $e) {
                Log::error("Lỗi khi cập nhật quyết định ID {$decisionId}: " . $e->getMessage());
            }
        }

        Log::info(" Đã hoàn tất cập nhật trạng thái hết hạn của quyết định.");
    }
}
