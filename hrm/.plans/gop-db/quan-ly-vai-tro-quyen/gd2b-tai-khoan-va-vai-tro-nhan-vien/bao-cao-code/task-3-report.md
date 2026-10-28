# Task 3 report — API Màn 2: quyền đang được cấp + phân quyền hàng loạt

Status: DONE_WITH_CONCERNS (no commit, no migration, no seeder)

## Implemented
- `GET /admin/employee-roles/{id}/effective-permissions`: roles E holds at C with each role's permissions, from the GĐ2 catalog. `kind`, `scope` and `subsystem` are raw values, the same as `/admin/roles/{id}/permissions`, so FE maps them with SCOPE_LABELS / kind labels. Also returns `departments` for every working company of E (read only). It 404s when E does not work at C.
- Bulk actions: `GET /bulk/options` and `POST /bulk/preview|eligible|apply|export`, inside the `admin/employee-roles` group (`auth:api` + `checkPermission:Quản lý phân quyền`).
- `BulkPermissionService`: the company is now an explicit parameter of `preview`, `eligibleAdditionalEmployees`, `exportEmployees`, `apply` and `resolveAffectedEmployeesQuery`. Nothing reads the claim inside any more. A new `bool $byWorkingCompany` flag (default false = old behaviour) changes two things:
  - Employees come from `company_employees(·, C)` instead of `employee_infos.company_id`, so concurrent staff are included and staff whose profile says C but who do not work at C are excluded.
  - The `all_*` flags only match C's khối, phòng ban, bộ phận, chức vụ and chức danh.
  - The old `BulkPermissionController` passes the JWT claim through `claimCompanyId()`, so the old routes behave as before until Task 8. `BulkPermissionApplyRequest` is unchanged (positional call, flag defaults to false).
- Company scoping found in the DB:
  - Khối = `hrm_groups.company_id`.
  - `departments.company_id`.
  - Bộ phận is checked through `parts.department_id → departments.company_id`, because `parts.company_id` is null on 5 test rows.
  - Chức vụ = `working_positions.company_id`.
  - Chức danh = `titles.company_id`.
  - All five catalogs are company-scoped, so all of them are validated.
- New requests:
  - `EmployeeRoleBulkRequest` extends the old `BulkPermissionPreviewRequest` and adds `exists ... company_id = C` checks for each element of `filter.*_ids.*`, `additional_employee_ids.*`, `excluded_employee_ids.*` and every `sub_filter.*` id. Employees must be in `company_employees(·, C)`. Any mismatch is a 422 on that key.
  - `EmployeeRoleBulkApplyRequest` adds: `action` nullable, `in:grant` only (revoke ⇒ 422); `role_ids` required, each role must have `company_id = C` and `status = 1`; at least one object; at least one employee left after exclusions.
- `EmployeeRoleService::bulkGrant`:
  - Resolves the employee set through `BulkPermissionService::resolveAffectedEmployeesQuery(..., C, true)`.
  - An employee counts as "changing" when they lack at least one of the chosen roles. Inside one transaction it takes a before snapshot, calls `Employee::grantRoles` in chunks of 100, takes an after snapshot and calls `writeHistory` (company_id = C).
  - It flushes `PermissionChecker`, `RequestCache` and `spatie.permission.cache` once, after the transaction.
  - Employees who already hold every chosen role get no history row.
  - Apply does not reuse `BulkPermissionService::apply`, because history needs per-employee snapshots.
- `bulkOptions` returns only C's active items, which replaces the 6 old option endpoints. Those endpoints are not all company-scoped: `timesheet/roles/list` and departments return every company.

## TDD
- RED, `phpunit tests/Feature/Rbac/AdminEmployeeRoleBulkTest.php`: `Tests: 5, Assertions: 5, Failures: 5`. Every case got "Expected response status code [200|422] but received 404" because the routes did not exist yet. The first run errored inside the fixture because the DB has no bộ phận at C2, so the test now creates one.
- GREEN, same file: `OK (5 tests, 106 assertions)`.
- Full suite, `phpunit tests/Feature/Rbac`: `OK (222 tests, 6184 assertions)` (217 + 5). That includes `BulkRoleGrantTest`, which covers the old `timesheet/bulk-permissions/apply` route. No other test touches BulkPermissionService.
- Tests:
  - `test_effective_permissions_danh_dau_trung`: also checks 404 and 403.
  - `test_effective_departments_chia_chinh_kiem_nhiem`: main company first; the row flag at the concurrent company; the overall flag at the main company of a concurrent employee.
  - `test_bulk_chi_nhan_vien_C`: preview, eligible, `all_department`, export and options; also 403. The JWT claim is set to C2 to prove the company comes from `current_company_role`.
  - `test_bulk_id_cong_ty_khac_422`: department, part, foreign role, locked role, additional, excluded, group, chức vụ, chức danh, preview and `action=revoke`; nothing is written.
  - `test_bulk_ghi_lich_su_moi_nguoi_company_id_C`: 1 row with company_id C1; none for the employee who already had the role; none on a repeat apply.

## Files
- New: `app/Http/Requests/Admin/EmployeeRoleBulkRequest.php`, `app/Http/Requests/Admin/EmployeeRoleBulkApplyRequest.php`, `tests/Feature/Rbac/AdminEmployeeRoleBulkTest.php`.
- Modified: `app/Services/Admin/EmployeeRoleService.php` (+effectivePermissions, departmentsAllCompanies, bulkOptions, bulkGrant), `app/Http/Controllers/Api/V1/Admin/EmployeeRoleController.php` (+6 actions), `routes/api.php` (+6 routes), `Modules/Timesheet/Services/BulkPermissionService.php`, `Modules/Timesheet/Http/Controllers/Api/V1/BulkPermissionController.php` (passes the claim explicitly). All files are LF.

## JSON shapes (for Task 6/7)

### GET /admin/employee-roles/{id}/effective-permissions
`{code:200, message:"success", data:{...}}`
```
{ "employee": {"id","code","fullname"},
  "company": {"id","code","name"},                       // C, for the subtitle "Vai trò tại <C>"
  "roles": [{ "id", "base_name", "status": 1|0,           // E's roles at C (locked role: status 0, no duplicates counted)
              "permission_count", "duplicate_count",      // for the tab label
              "permissions": [{ "code","name","subsystem_group","subsystem" /* null ⇒ "(Khác)" */,"feature",
                                "kind": "view|action|approve", "scope": int|null,
                                "duplicated_in": ["<base_name of another active role>", ...] }] }],  // ordered by permissions.id
  "departments": [{ "company_id","company_code","company_name","is_main": bool, "all_department": bool,
                    "rows": [{"department_name","part_names":[...]}] }] }  // main first; all_department=true ⇒ rows []
```

### GET /admin/employee-roles/bulk/options
`{code, message, data:{ company:{id,code,name}, groups:[{id,code,name}], departments:[{id,code,name,group_id}],
parts:[{id,code,name,department_id}], working_positions:[{id,code,name}], titles:[{id,code,name}], roles:[{id,name}] }}`.
Only C's rows with status 1 (roles: active only). FE: `formatCodeName` works unchanged; filtering departments by `group_id` and parts by `department_id` works as before.

### POST /admin/employee-roles/bulk/preview
Body is the same as the old route: `filter{group_ids,department_ids,part_ids,working_position_ids,employee_role_ids,all_*}, additional_employee_ids, excluded_employee_ids, sub_filter{employee_id,department_id,part_id,working_position_id,employee_role_id,keyword,email}, view(all|selected|excluded), page, limit(<=100)`.
Response is the same as the old route (not wrapped): `{data:[{id,code,fullname,email,department_id,department_name,part_id,part_name,working_position_id,working_position_name,employee_role_id,employee_role_name}], pagination:{current_page,per_page,total,last_page}, totals:{all,selected,excluded}}`.

### POST /admin/employee-roles/bulk/eligible
Body `{filter}` ⇒ `{data:[{id,code,fullname,name}]}`. The list includes C's concurrent employees.

### POST /admin/employee-roles/bulk/export
Same body as preview ⇒ xlsx `phan_quyen_hang_loat_YmdHis.xlsx` (same columns as the old export).

### POST /admin/employee-roles/bulk/apply
Body: preview body + `role_ids:[int]` (required). `action` may be left out; only `grant` is accepted.
OK: `{message:"Đã cập nhật vai trò cho N nhân viên", affected:N, granted:M, action:"grant", role_ids:[...]}`.
422 keys:
- `filter.department_ids.N`, `filter.part_ids.N`, `filter.group_ids.N`, `filter.working_position_ids.N`, `filter.employee_role_ids.N`
- `additional_employee_ids.N`, `excluded_employee_ids.N` (also the "no employee left" error), `sub_filter.*`
- `role_ids.N` (role of another company or locked), `role_ids`, `action`, `filter` (no object)

422 also applies to the ids in preview, eligible and export.

## Self-review
- C always comes from `current_company_role`. Nothing reads the JWT claim on the new routes, and the test proves it with a stale claim (C2).
- Every id is validated before any query or write. Apply writes in one transaction, then flushes the caches once.
- The old routes keep their behaviour: the employee set, `all_*` and the claim are unchanged. One cosmetic change: the extra `employee_infos.company_id` condition in the "bổ sung" branch was removed because the outer query already applies it.
- No N+1 in effective-permissions: 1 query for roles, 1 for permissions, 1 for companies, 1 for departments, 1 for parts.

## Concerns
1. **The bulk popup FE no longer exists in wt-rbac/hrm-client.** The GĐ2 commit `25824b310` deleted `components/timesheet/setting/roles/BulkPermission{Modal,Filter,EmployeeList,Banner}.vue`. Copies are still in the parent commit (`git show 25824b310^:components/timesheet/setting/roles/BulkPermissionModal.vue`) and in ERP-HRM/HRM/hrm-client (gop_db). Task 6 has to restore them from there, not move them (Ruling 2 assumed they still existed).
2. bulkGrant takes about 5 queries per snapshot for each employee who changes (before + after). A batch of 1,000 people is therefore roughly 10k queries in one transaction: acceptable but slow. Employees with nothing to change are skipped.
3. Concurrent employees at C still have `employee_infos.department_id` and `part_id` pointing at their main company's org. They are never matched by C's khối/phòng ban/bộ phận filters and can only be included as "NV bổ sung". This comes from the data model; same as before.
4. effective-permissions lists locked roles with `status:0` and their permissions, but they never count as duplicates because they grant nothing. FE should mark them as locked.
5. Sub-filter ids from another company are now 422. If the sub-filter options in the restored FE list come from `bulk/options`, this cannot happen.
