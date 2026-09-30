<?php

namespace App\Console\Commands;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

/**
 * Đồng bộ email tài khoản (employees.email) theo hồ sơ nhân sự (employee_infos.email).
 * Nguồn chuẩn = employee_infos. Chỉ chuẩn hoá các bản ghi đang lệch.
 *
 * Dùng để fix dữ liệu cũ tạo trước khi có cơ chế đồng bộ.
 */
class SyncEmployeeEmailFromInfo extends Command
{
    protected $signature = 'human:sync-employee-email {--dry-run : Chỉ liệt kê bản ghi lệch, không cập nhật}';
    protected $description = 'Đồng bộ employees.email theo employee_infos.email (nguồn chuẩn = hồ sơ nhân sự)';

    public function handle()
    {
        try {
            $dryRun = (bool) $this->option('dry-run');

            // Lấy các bản ghi email lệch nhau (null-safe: bắt cả null vs giá trị).
            $diffs = DB::table('employees')
                ->join('employee_infos', 'employees.employee_info_id', '=', 'employee_infos.id')
                ->whereRaw('NOT (employees.email <=> employee_infos.email)')
                ->select(
                    'employees.id as employee_id',
                    'employee_infos.code',
                    'employee_infos.fullname',
                    'employees.email as account_email',
                    'employee_infos.email as info_email'
                )
                ->get();

            if ($diffs->isEmpty()) {
                $this->info('Không có bản ghi nào lệch. 2 bảng đã đồng bộ.');
                return 0;
            }

            $toFix = [];
            $skipped = [];
            foreach ($diffs as $row) {
                // Không ghi đè bằng email rỗng (tránh xoá email tài khoản đang dùng đăng nhập).
                if ($row->info_email === null || trim((string) $row->info_email) === '') {
                    $skipped[] = [$row->employee_id, $row->code, $row->fullname, $row->account_email, '(rỗng)'];
                    continue;
                }
                $toFix[] = $row;
            }

            $this->info('=== Bản ghi sẽ đồng bộ (employees.email <- employee_infos.email) ===');
            if (empty($toFix)) {
                $this->info('Không có');
            } else {
                $this->table(
                    ['Employee ID', 'Mã NV', 'Họ tên', 'Email tài khoản (cũ)', 'Email hồ sơ (mới)'],
                    array_map(function ($r) {
                        return [$r->employee_id, $r->code, $r->fullname, $r->account_email, $r->info_email];
                    }, $toFix)
                );
                $this->info('Tổng: ' . count($toFix));
            }

            if (!empty($skipped)) {
                $this->newLine();
                $this->warn('=== BỎ QUA: hồ sơ có email rỗng (không ghi đè để giữ email tài khoản) ===');
                $this->table(['Employee ID', 'Mã NV', 'Họ tên', 'Email tài khoản', 'Email hồ sơ'], $skipped);
                $this->warn('Tổng bỏ qua: ' . count($skipped));
            }

            if ($dryRun) {
                $this->newLine();
                $this->info('DRY-RUN: không cập nhật. Bỏ --dry-run để thực thi.');
                return 0;
            }

            $updated = 0;
            foreach ($toFix as $row) {
                DB::table('employees')
                    ->where('id', $row->employee_id)
                    ->update(['email' => $row->info_email]);
                $updated++;
            }

            $this->newLine();
            $this->info("Đã đồng bộ {$updated} bản ghi.");
            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error($e->getMessage());
            return 1;
        }
    }
}
