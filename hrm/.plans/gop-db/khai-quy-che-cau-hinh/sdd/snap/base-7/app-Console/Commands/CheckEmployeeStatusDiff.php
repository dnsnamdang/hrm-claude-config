<?php

namespace App\Console\Commands;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class CheckEmployeeStatusDiff extends Command
{
    protected $signature = 'check:employee-status-diff';
    protected $description = 'Kiểm tra khác biệt status nhân sự giữa HRM và ERP';

    private const EMPLOYEE_INFO_STATUS_MAP = [
        0 => 'Nghỉ việc',
        1 => 'Đang làm',
        2 => 'Ứng viên',
        3 => 'Tạm nghỉ',
    ];

    private const EMPLOYEE_STATUS_MAP = [
        0 => 'Inactive',
        1 => 'Active',
    ];

    public function handle()
    {
        try {
            $infoResult = $this->compareEmployeeInfo();
            $employeeResult = $this->compareEmployee();

            $this->newLine();
            $this->info('=== Tổng kết ===');
            $this->info("EmployeeInfo khác status: {$infoResult['diff']} | Đã đồng bộ: {$infoResult['synced']}");
            $this->info("Employee khác status: {$employeeResult['diff']} | Đã đồng bộ: {$employeeResult['synced']}");

            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error($e->getMessage());

            return 1;
        }
    }

    private function compareEmployeeInfo(): array
    {
        $hrmRecords = DB::table('employee_infos')
            ->select('id', 'code', 'fullname', 'email', 'status', 'created_at', 'updated_at')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $tpRecords = DB::connection('mysql2')->table('employee_infos')
            ->select('id', 'code', 'email', 'status')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $diffs = [];
        $syncEmails = [];
        foreach ($hrmRecords as $email => $hrm) {
            $tp = $tpRecords->get($email);
            if (!$tp || $hrm->status == $tp->status) continue;

            $note = '';
            if ($hrm->code != $tp->code) {
                $note = "Code khác: HRM={$hrm->code}, Tp={$tp->code}";
            }

            $diffs[] = [
                $hrm->id,
                $hrm->code,
                $hrm->fullname,
                $hrm->email,
                $this->formatInfoStatus($hrm->status),
                $this->formatInfoStatus($tp->status),
                $hrm->created_at,
                $hrm->updated_at,
                $note,
            ];

            $syncEmails[$email] = $hrm->status;
        }

        if (empty($diffs)) {
            return ['diff' => 0, 'synced' => 0];
        }

        $this->newLine();
        $this->info('=== So sánh EmployeeInfo ↔ TpEmployeeInfo ===');
        $this->table(['ID', 'Mã NV', 'Họ tên', 'Email', 'Status HRM', 'Status Tp', 'Ngày tạo', 'Ngày update', 'Ghi chú'], $diffs);
        $this->info("Tổng: " . count($diffs) . " nhân sự khác status");

        $synced = 0;
        foreach ($syncEmails as $email => $status) {
            DB::connection('mysql2')->table('employee_infos')
                ->where('email', $email)
                ->update(['status' => $status]);
            $synced++;
        }
        $this->info("Đã đồng bộ {$synced} bản ghi EmployeeInfo sang ERP");

        return ['diff' => count($diffs), 'synced' => $synced];
    }

    private function compareEmployee(): array
    {
        $hrmRecords = DB::table('employees')
            ->join('employee_infos', 'employees.employee_info_id', '=', 'employee_infos.id')
            ->select('employees.id', 'employee_infos.code', 'employee_infos.fullname', 'employee_infos.email', 'employees.status', 'employees.created_at', 'employees.updated_at')
            ->whereNotNull('employee_infos.email')
            ->where('employee_infos.email', '!=', '')
            ->get()
            ->keyBy('email');

        $tpRecords = DB::connection('mysql2')->table('employees')
            ->select('id', 'email', 'status')
            ->whereNotNull('email')
            ->where('email', '!=', '')
            ->get()
            ->keyBy('email');

        $diffs = [];
        $syncEmails = [];
        foreach ($hrmRecords as $email => $hrm) {
            $tp = $tpRecords->get($email);
            if ($tp && $hrm->status != $tp->status) {
                $diffs[] = [
                    $hrm->id,
                    $hrm->code,
                    $hrm->fullname,
                    $email,
                    $this->formatEmployeeStatus($hrm->status),
                    $this->formatEmployeeStatus($tp->status),
                    $hrm->created_at,
                    $hrm->updated_at,
                ];

                $syncEmails[$email] = $hrm->status;
            }
        }

        if (empty($diffs)) {
            return ['diff' => 0, 'synced' => 0];
        }

        $this->newLine();
        $this->info('=== So sánh Employee ↔ TpEmployee ===');
        $this->table(['ID', 'Mã NV', 'Họ tên', 'Email', 'Status HRM', 'Status Tp', 'Ngày tạo', 'Ngày update'], $diffs);
        $this->info("Tổng: " . count($diffs) . " nhân sự khác status");

        $synced = 0;
        foreach ($syncEmails as $email => $status) {
            DB::connection('mysql2')->table('employees')
                ->where('email', $email)
                ->update(['status' => $status]);
            $synced++;
        }
        $this->info("Đã đồng bộ {$synced} bản ghi Employee sang ERP");

        return ['diff' => count($diffs), 'synced' => $synced];
    }

    private function formatInfoStatus($status): string
    {
        $name = self::EMPLOYEE_INFO_STATUS_MAP[$status] ?? 'Unknown';
        return "{$name}({$status})";
    }

    private function formatEmployeeStatus($status): string
    {
        $name = self::EMPLOYEE_STATUS_MAP[$status] ?? 'Unknown';
        return "{$name}({$status})";
    }
}
