<?php

namespace App\Console\Commands\Assign;

use Illuminate\Console\Command;
use Modules\Assign\Entities\Solution;
use Modules\Assign\Entities\SolutionModule;
use Modules\Assign\Helpers\ProgressCalculator;

class CalculateProgressCommand extends Command
{
    protected $signature = 'assign:calculate-progress';

    protected $description = 'Tính lại tiến độ cho tất cả giải pháp và hạng mục đang hoạt động';

    public function handle()
    {
        $solutions = Solution::whereNotIn('status', [
            Solution::STATUS_TAO_NHAP,
            // Solution::STATUS_DA_LAM_GP,
        ])->get();

        $moduleCount = 0;

        foreach ($solutions as $solution) {
            if ($solution->has_modules) {
                $modules = SolutionModule::where('solution_id', $solution->id)->get();
                foreach ($modules as $module) {
                    ProgressCalculator::recalculateModuleProgress($module->id);
                    $moduleCount++;
                }
            }

            ProgressCalculator::recalculateSolutionProgress($solution->id);
        }

        $this->info("Đã tính lại tiến độ cho {$solutions->count()} giải pháp, {$moduleCount} hạng mục.");
    }
}
