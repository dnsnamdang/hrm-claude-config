<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Carbon\Carbon;

class UpdateEmployeeLeaveStatusCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'human:update-leave-status';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Cập nhật trạng thái 3 cho nhân sự có status = 3 và leave_date <= hôm nay (có đủ leave_date, return_date)';

    /**
     * Execute the console command.
     */
    public function handle(): int
    {
        $today = Carbon::today();

        $employees = EmployeeInfo::query()
            ->where('status', 1)
            ->whereNotNull('leave_date')
            ->whereNotNull('return_date')
            ->whereDate('leave_date', '<=', $today)
            ->whereDate('return_date', '>', $today)
            ->get();

        $affected = 0;
        foreach ($employees as $employee) {
            $employee->status = 3;
            $employee->save();
            $affected++;
        }

        $this->info("Updated {$affected} employee(s) with status 3 based on leave_date <= today.");
        return Command::SUCCESS;
    }
}
