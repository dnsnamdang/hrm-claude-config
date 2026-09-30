<?php

namespace App\Console\Commands\Rice;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Modules\Rice\Entities\RiceEmployeeInfo;

class SyncRiceEmployeeStatusFromEmployeeInfo extends Command
{
    protected $signature = 'rice:sync-employee-status';
    protected $description = 'Đồng bộ status của rice_employee_infos theo employee_infos';

    public function handle()
    {
        try {
            $updatedCount = 0;
            $checkedCount = 0;
            $companyRiceMap = [];

            EmployeeInfo::query()
                ->select('id', 'company_id', 'status', 'leave_date')
                ->orderBy('id')
                ->chunkById(500, function ($employeeInfos) use (&$updatedCount, &$checkedCount, &$companyRiceMap) {
                    foreach ($employeeInfos as $employeeInfo) {
                        $checkedCount++;

                        if (!array_key_exists($employeeInfo->company_id, $companyRiceMap)) {
                            $riceCompany = findRiceCompany($employeeInfo->company_id);
                            $companyRiceMap[$employeeInfo->company_id] = $riceCompany ? $riceCompany->id : null;
                        }

                        $riceCompanyId = $companyRiceMap[$employeeInfo->company_id];
                        if (!$riceCompanyId) {
                            continue;
                        }

                        $riceEmployeeInfo = RiceEmployeeInfo::query()
                            ->select('id', 'status')
                            ->where('employee_info_id', $employeeInfo->id)
                            ->where('rice_company_id', $riceCompanyId)
                            ->first();

                        if (!$riceEmployeeInfo) {
                            continue;
                        }

                        if ((int) $riceEmployeeInfo->status !== (int) $employeeInfo->status) {
                            $riceEmployeeInfo->update([
                                'status' => $employeeInfo->status,
                                'leave_date' => $employeeInfo->leave_date,
                            ]);
                            $updatedCount++;
                        }
                    }
                });

            $this->info('Đồng bộ status hoàn tất.');
            $this->line('checked_count: ' . $checkedCount);
            $this->line('updated_count: ' . $updatedCount);
        } catch (\Throwable $throwable) {
            $this->error('Lỗi đồng bộ status rice_employee_infos: ' . $throwable->getMessage());
        }
    }
}
