<?php

namespace App\Console\Commands\Decision;

use Illuminate\Console\Command;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\Decision;
use Modules\Decision\Services\DecisionRegulationSalary\DecisionRegulationSalaryService;
use Modules\Decision\Services\DepartmentChange\DepartmentChangeService;
use Modules\Decision\Services\DepartmentEstablishment\DepartmentEstablishmentService;
use Modules\Decision\Services\ManpowerPlanning\ManpowerPlanningService;
use Modules\Decision\Services\Regulation\RegulationGeneralService;
use Modules\Decision\Services\EmployeeDiscipline\EmployeeDisciplineService;
use Modules\Decision\Services\DepartmentDissolution\DepartmentDissolutionService;
use Modules\Decision\Services\TerminationLaborContract\TerminationLaborContractService;

class ProcessDecisionsCommand extends Command
{
    protected $signature = 'decision:process-decisions {date?} {type?}';
    protected $description = 'Xử lý các quyết định có hiệu lực trong ngày hôm nay hoặc theo ngày và loại quyết định được chỉ định';


    public function __construct()
    {
        parent::__construct();
    }


    public function handle()
    {
        try {
            $date = $this->argument('date') ? Carbon::parse($this->argument('date')) : Carbon::today();
            $type = $this->argument('type');

            $query = Decision::whereDate('effective_date', $date)
                ->where('status', Decision::STATUS_APPROVED);

            if ($type) {
                $query->where('type', $type);
            }

            $decisions = $query->get();

            foreach ($decisions as $decision) {
                switch ($decision->type) {
                    case Decision::TYPE_MANPOWER_PLANNING:
                        ManpowerPlanningService::syncDepartmentManpowerPlanning($decision);
                        break;

                    case Decision::TYPE_DEPARTMENT_ESTABLISHMENT:
                        DepartmentEstablishmentService::syncCreateDepartment($decision->departmentEstablishment);
                        break;

                    case Decision::TYPE_DEPARTMENT_CHANGE:
                        DepartmentChangeService::syncUpdateDepartment($decision);
                        break;

                    case Decision::TYPE_REGULATION_GENERAL_ALL:
                        RegulationGeneralService::syncUpdateUsingRegulationGeneral($decision);
                        break;

                    case Decision::TYPE_REGULATION_SALARY:
                        DecisionRegulationSalaryService::syncUpdateUsingDecisionRegulationSalary($decision);
                        break;

                    case Decision::TYPE_EMPLOYEE_DISCIPLINE:
                        EmployeeDisciplineService::syncLockEmployee($decision);
                        break;

                    case Decision::TYPE_DEPARTMENT_DISSOLUTION:
                        DepartmentDissolutionService::syncLockDepartment($decision);
                        break;

                    default:
                        $this->info("Loại quyết định không xác định: {$decision->type}");
                        break;
                }
            }

            if ($decisions->count() > 0) {
                $this->info('Đã xử lý xong các quyết định cho ngày ' . $date->format('d/m/Y'));
            } else {
                $this->info('Không có quyết định nào có hiệu lực vào ngày ' . $date->format('d/m/Y'));
            }
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi xử lý các quyết định.');
        }
    }
}
