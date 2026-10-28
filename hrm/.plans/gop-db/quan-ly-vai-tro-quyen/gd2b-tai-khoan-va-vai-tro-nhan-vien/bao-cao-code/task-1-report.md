# Task 1 report — Lịch sử vai trò NV tách theo công ty

Status: DONE (không commit)

## Implemented
- Migration `database/migrations/2026_11_02_000001_add_company_id_to_employee_permission_history.php`: cột `company_id` unsigned bigint nullable (after employee_id), index `eph_company_idx`; guard Schema::hasColumn (up/down), PHPDoc.
- `EmployeePermissionAdapter`: `authorize` = có dòng company_employees(employee_id, C) (C = current_company_role; null => false; 403 qua SettingHistoryController::guard "Bạn không có quyền xem lịch sử của bản ghi này"). `fetchRows` = company_id = C, OR company_id IS NULL khi employee_infos.company_id của NV == C. mapRow không đổi (không cần). performerCompanyId giữ nguyên.
- Test `tests/Feature/Rbac/EmployeeRoleHistoryTest.php`: test_lich_su_tach_theo_cong_ty (C1 => 2 dòng NULL+C1; C2 => 1 dòng), test_nhan_vien_khong_lam_o_cong_ty_hien_tai_bi_403.

## TDD
- RED 1 (chưa có cột): `phpunit tests/Feature/Rbac/EmployeeRoleHistoryTest.php` => Errors: 2, "Unknown column 'company_id'".
- Migrate --pretend: `alter table employee_permission_history add company_id bigint unsigned null comment ... after employee_id` ; `add index eph_company_idx(company_id)` (+ select information_schema.columns cho hasColumn). Sau đó chạy `migrate --path=...` => Migrated 101ms (chỉ file này, DB hrm_erp_rbac_test).
- RED 2 (có cột, adapter cũ): Failures 1 — "actual size 3 matches expected size 2".
- GREEN: EmployeeRoleHistoryTest OK (2 tests, 9 assertions). Full `tests/Feature/Rbac`: OK (204 tests, 5949 assertions).

## Files
- new: migration, tests/Feature/Rbac/EmployeeRoleHistoryTest.php
- modified: app/Services/SettingHistory/Adapters/EmployeePermissionAdapter.php (authorize, fetchRows, docblock)

## Writers của employee_permission_history (Task 2 cần)
- Chỉ `Modules/Timesheet/Services/EmployeeService.php:264` `EmployeePermissionHistory::create([...])` (entity Modules/Timesheet/Entities/EmployeePermissionHistory.php, kiểm $fillable/guarded có `company_id` chưa — KHÔNG sửa ở task này). Reader cũ cùng file dòng ~279 (`/histories` cũ, không lọc company_id). Seeder ReconcileEmployeesSeeder chỉ remap employee_id.
- Writer hiện tại không điền company_id => log mới vẫn NULL => chỉ hiện ở công ty chính cho tới khi Task 2 ghi company_id = C.

## Concerns
- Hành vi đổi: NV kiêm nhiệm (không phải công ty chính) trước đây bị 403 vì authorize theo employee_infos.company_id; nay theo company_employees (đúng brief).
- Chưa kiểm Entity $fillable. Test C2 dựng vai trò phụ trong test (role R2b ở C2 có manage perm) vì fixture chỉ cấp quyền ở C1.
