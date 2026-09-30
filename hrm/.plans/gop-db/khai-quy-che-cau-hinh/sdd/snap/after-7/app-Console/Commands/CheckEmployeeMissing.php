<?php

namespace App\Console\Commands;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class CheckEmployeeMissing extends Command
{
    protected $signature = 'check:employee-missing';
    protected $description = 'Tìm nhân sự có trong HRM nhưng không có trong ERP (so sánh bảng employees theo email)';

    public function handle()
    {
        try {
            $hrmEmails = DB::table('employees')
                ->select('id', 'email', 'status')
                ->get()
                ->keyBy('email');

            $tpEmails = DB::connection('mysql2')->table('employees')
                ->select('id', 'email')
                ->get()
                ->keyBy('email');

            $onlyHrm = [];
            foreach ($hrmEmails as $email => $hrm) {
                if (!$tpEmails->has($email)) {
                    $onlyHrm[] = [$hrm->id, $email ?: '(trống)', $hrm->status];
                }
            }

            $onlyErp = [];
            foreach ($tpEmails as $email => $tp) {
                if (!$hrmEmails->has($email)) {
                    $onlyErp[] = [$tp->id, $email ?: '(trống)'];
                }
            }

            $this->info('=== Employees có trong HRM nhưng KHÔNG có trong ERP ===');
            if (empty($onlyHrm)) {
                $this->info('Không có');
            } else {
                $this->table(['ID HRM', 'Email', 'Status'], $onlyHrm);
                $this->info("Tổng: " . count($onlyHrm));
            }

            $this->newLine();
            $this->info('=== Employees có trong ERP nhưng KHÔNG có trong HRM ===');
            if (empty($onlyErp)) {
                $this->info('Không có');
            } else {
                $this->table(['ID ERP', 'Email'], $onlyErp);
                $this->info("Tổng: " . count($onlyErp));
            }

            $this->newLine();
            $this->info("Tổng HRM: {$hrmEmails->count()} | Tổng ERP: {$tpEmails->count()} | Chênh lệch: " . abs($hrmEmails->count() - $tpEmails->count()));

            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error($e->getMessage());

            return 1;
        }
    }
}
