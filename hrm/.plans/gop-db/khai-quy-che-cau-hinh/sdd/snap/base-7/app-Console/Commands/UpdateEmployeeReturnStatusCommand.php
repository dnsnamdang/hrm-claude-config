<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Carbon\Carbon;

class UpdateEmployeeReturnStatusCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'human:update-return-status';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Chuyển trạng thái nhân sự từ 3 -> 1 khi đến ngày quay lại, đồng thời xoá leave_date và return_date';

    /**
     * Execute the console command.
     */
    public function handle(): int
    {
        $today = Carbon::today();

        $employees = EmployeeInfo::query()
            ->where('status', 3)
            ->whereNotNull('leave_date')
            ->whereNotNull('return_date')
            ->whereDate('return_date', $today)
            ->get();

        $affected = 0;
        foreach ($employees as $employee) {
            $employee->status = 1;
            $employee->leave_date = null;
            $employee->return_date = null;
            $employee->save();
            $affected++;
        }

        $this->info("Updated {$affected} employee(s) back to status 1.");
        return Command::SUCCESS;
    }
}
