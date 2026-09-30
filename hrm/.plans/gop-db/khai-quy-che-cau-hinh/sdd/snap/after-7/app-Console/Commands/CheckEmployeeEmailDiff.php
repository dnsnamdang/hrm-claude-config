<?php

namespace App\Console\Commands;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class CheckEmployeeEmailDiff extends Command
{
    protected $signature = 'check:employee-email-diff';
    protected $description = 'Kiểm tra email nhân sự khác nhau giữa HRM và ERP';

    public function handle()
    {
        try {
            $this->checkEmployeeInfoEmails();
            $this->checkEmployeeEmails();

            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error($e->getMessage());

            return 1;
        }
    }

    private function checkEmployeeInfoEmails()
    {
        $hrmEmails = DB::table('employee_infos')
            ->select('id', 'code', 'fullname', 'email', 'status')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $tpEmails = DB::connection('mysql2')->table('employee_infos')
            ->select('id', 'code', 'email', 'status')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $onlyHrm = [];
        foreach ($hrmEmails as $email => $hrm) {
            if (!$tpEmails->has($email)) {
                $onlyHrm[] = [$hrm->id, $hrm->code, $hrm->fullname, $email, $hrm->status];
            }
        }

        $onlyErp = [];
        foreach ($tpEmails as $email => $tp) {
            if (!$hrmEmails->has($email)) {
                $onlyErp[] = [$tp->id, $tp->code, $email, $tp->status];
            }
        }

        $this->info('=== EmployeeInfo: Email chỉ có trong HRM ===');
        if (empty($onlyHrm)) {
            $this->info('Không có');
        } else {
            $this->table(['ID', 'Mã NV', 'Họ tên', 'Email', 'Status'], $onlyHrm);
            $this->info("Tổng: " . count($onlyHrm));
        }

        $this->newLine();
        $this->info('=== EmployeeInfo: Email chỉ có trong ERP ===');
        if (empty($onlyErp)) {
            $this->info('Không có');
        } else {
            $this->table(['ID', 'Mã NV', 'Email', 'Status'], $onlyErp);
            $this->info("Tổng: " . count($onlyErp));
        }
    }

    private function checkEmployeeEmails()
    {
        $hrmEmails = DB::table('employees')
            ->join('employee_infos', 'employees.employee_info_id', '=', 'employee_infos.id')
            ->select('employees.id', 'employee_infos.code', 'employee_infos.fullname', 'employee_infos.email', 'employees.status')
            ->whereNotNull('employee_infos.email')
            ->where('employee_infos.email', '!=', '')
            ->get()
            ->keyBy('email');

        $tpEmails = DB::connection('mysql2')->table('employees')
            ->select('id', 'email', 'status')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $onlyHrm = [];
        foreach ($hrmEmails as $email => $hrm) {
            if (!$tpEmails->has($email)) {
                $onlyHrm[] = [$hrm->id, $hrm->code, $hrm->fullname, $email, $hrm->status];
            }
        }

        $onlyErp = [];
        foreach ($tpEmails as $email => $tp) {
            if (!$hrmEmails->has($email)) {
                $onlyErp[] = [$tp->id, $email, $tp->status];
            }
        }

        $this->newLine();
        $this->info('=== Employee: Email chỉ có trong HRM ===');
        if (empty($onlyHrm)) {
            $this->info('Không có');
        } else {
            $this->table(['ID', 'Mã NV', 'Họ tên', 'Email', 'Status'], $onlyHrm);
            $this->info("Tổng: " . count($onlyHrm));
        }

        $this->newLine();
        $this->info('=== Employee: Email chỉ có trong ERP ===');
        if (empty($onlyErp)) {
            $this->info('Không có');
        } else {
            $this->table(['ID', 'Email', 'Status'], $onlyErp);
            $this->info("Tổng: " . count($onlyErp));
        }
    }
}
