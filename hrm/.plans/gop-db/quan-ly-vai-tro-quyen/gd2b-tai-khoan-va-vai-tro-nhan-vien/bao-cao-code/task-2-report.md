# Task 2 report — API Màn 2 "Quản lý vai trò nhân viên" (danh sách, chi tiết, lưu, xuất)

Status: DONE_WITH_CONCERNS (không commit, không migration, không seeder)

## Đã làm
- Nhóm route `admin/employee-roles` (`auth:api`, `checkPermission:Quản lý phân quyền`), ngay sau `admin/roles`:
  `GET /` · `GET /export` · `GET /{id}` · `PUT /{id}` (id = employees.id, `[0-9]+`).
- `EmployeeRoleService`: `index` (query + lọc), `attachListData` (nạp hàng loạt vai trò/số quyền, công ty làm việc, dòng
  lịch sử mới nhất ở C — không N+1), `findWorking` (404), `isMainCompany`, `detail`, `save` (gọi trong transaction ở
  controller), `snapshot` (ghi lịch sử), `roleIdsAt`, `allDepartmentAt`, `manageDepartmentsAt`.
- `EmployeeRoleSaveRequest`: thứ tự lỗi 404 (authorize → findWorking) → 403 (`company_ids` có trong body khi C không phải
  công ty chính) → 422 (rules + after-hook: vai trò khoá tick mới, gỡ công ty chính, bộ phận không thuộc phòng ban).
- `EmployeeRoleResource` (dòng danh sách + xuất), `ExportColumnRegistry['admin_employee_roles']`.
- Export theo khuôn `LevelController::export` (DynamicExport + ExportColumnRegistry::resolve, nhận `fields`). Lưu ý:
  `/admin/roles` GĐ2 KHÔNG có export nên không có mẫu ở đó.
- `EmployeePermissionHistory::$fillable` thêm `company_id`.
- `EmployeePermissionAdapter::mapRow`: thêm thay đổi "Công ty làm việc" khi snapshot có key `companies` (dòng cũ không có
  key ⇒ không đổi hành vi) + docblock.

### Luật ghi (save)
1. Snapshot cũ tại C.
2. `company_ids !== null` (chỉ công ty chính): mỗi X bị gỡ ⇒ `Employee::syncRolesInCompany(E, X, [])` + xoá
   `employee_manage_departments(E, X)` + xoá `company_employees(E, X)`; công ty mới ⇒ chèn `company_employees`.
3. `Employee::syncRolesInCompany(E, C, role_ids)`.
4. Phân công chỉ dòng của C: xoá `employee_manage_departments(E, C)`; C chính ⇒ `company_employees(E,C).all_department`
   = cờ; C kiêm nhiệm + cờ ⇒ 1 dòng `(department_id NULL, part_ids NULL, all_department 1)`; không cờ ⇒ 1 dòng/phòng ban,
   `part_ids` dạng `"1, 2"` như màn cũ.
5. Snapshot mới; khác cũ ⇒ 1 dòng `employee_permission_history` (`company_id = C`, action `update`, changed_by/at).
6. `PermissionChecker::flush()` + `RequestCache::flush()` + `forget('spatie.permission.cache')`.

Khuôn snapshot (tương thích adapter): `{"all_department":0|1, "roles":["base_name",...] (sort), "manager_departments":
[{"company":"<tên C>","department":"<tên>","parts":["<tên>",...]}] (chỉ dòng C), "companies":["MÃ - Tên",...]}`.

## TDD
- RED: `php vendor/bin/phpunit tests/Feature/Rbac/AdminEmployeeRoleApiTest.php` ⇒ `Tests: 13, Assertions: 15,
  Failures: 12` — mọi ca "Expected response status code [200|403|422] but received 404" (route chưa có).
  Ca `test_khong_lam_viec_o_C_404` xanh sẵn ở RED (404 do chưa có route) — sau cài đặt vẫn xanh vì findWorking.
- GREEN: cùng lệnh ⇒ `OK (13 tests, 124 assertions)`.
- Toàn bộ: `php vendor/bin/phpunit tests/Feature/Rbac` ⇒ `OK (217 tests, 6073 assertions)` (204 cũ + 13 mới).
- Ca test: 11 ca brief + `test_chi_tiet_tra_vai_tro_cong_ty_va_tong_hop` + `test_xuat_excel`.

## File
- Mới: `app/Http/Controllers/Api/V1/Admin/EmployeeRoleController.php`, `app/Services/Admin/EmployeeRoleService.php`,
  `app/Http/Requests/Admin/EmployeeRoleSaveRequest.php`, `app/Http/Resources/Admin/EmployeeRoleResource.php`,
  `tests/Feature/Rbac/AdminEmployeeRoleApiTest.php`.
- Sửa: `routes/api.php` (+import `AdminEmployeeRoleController`, +nhóm route), `app/ExcelExport/ExportColumnRegistry.php`
  (+key `admin_employee_roles`), `Modules/Timesheet/Entities/EmployeePermissionHistory.php` (+fillable `company_id`),
  `app/Services/SettingHistory/Adapters/EmployeePermissionAdapter.php` (+companies trong mapRow, docblock).
- Tất cả LF (file sửa vốn LF).

## Shape API (Task 6/7 dùng)

### GET /admin/employee-roles
Query: `keyword` (mã NV / tên / employees.email, LIKE), `department_id`, `part_id` (employee_infos), `role_ids[]`
(EXISTS gán ở C), `kind` = `main|concurrent`, `status` (employees.status: 1 hoạt động, 0 khoá), `no_role` = `1|0`,
`per_page` (mặc định 10), `page`. Sắp theo mã NV.
Response = khuôn `apiGetList` như `/admin/roles`: `{code, message, data:[...], links, meta:{total, per_page, current_page, ...}}`.
Mỗi dòng:
```
{ "id", "code", "email", "fullname", "department_name", "part_name",
  "roles": [{"id","name","permission_count"}],      // name = base_name; vai trò gán ở C
  "roles_text", "kind": "main|concurrent", "kind_text": "Công ty chính|Kiêm nhiệm",
  "main_company_name", "companies_text": "TPE, TPHP",
  "status": 1|0, "status_text": "Hoạt động|Đã khoá", "status_color",
  "updated_by_name", "updated_at": "d/m/Y H:i" }    // dòng lịch sử mới nhất company_id = C; null nếu chưa có
```

### GET /admin/employee-roles/export
Cùng query + `fields=code,email,...` (key ở `ExportColumnRegistry['admin_employee_roles']`: code, email, fullname,
department_name, roles_text, kind_text, updated_by_name, updated_at, part_name, main_company_name, companies_text,
status_text). Trả file `vai_tro_nhan_vien.xlsx`.

### GET /admin/employee-roles/{id}
`{code, message, data:{...}}`, data:
```
{ "employee": {"id","code","fullname","email","image","department_name","part_name","status","kind"},
  "is_main_company": bool,
  "companies": [{"id","code","name","is_main", "role_names":[...] /* CHỈ khi is_main_company: vai trò E ở công ty đó (để confirm gỡ) */}],
  "roles": [{"id","base_name","description","status":1|0,"permission_count","permission_ids":[int],"checked":bool}], // mọi vai trò của C
  "all_department": bool,
  "manage_departments": [{"department_id", "part_ids":[int]}],   // dòng của C, bỏ dòng cờ NULL
  "summary": {"total", "kinds":{"view","action","approve"}, "subsystems":[{"key","label","count"}]}, // hợp vai trò đang giữ
  "permission_meta": {"<permission_id>": {"kind","subsystem"}} }  // subsystem null ⇒ "(Khác)"
```
FE tính lại tổng hợp khi đổi tick: hợp `permission_ids` của các vai trò đang tick, tra `permission_meta` để đếm theo
kind + subsystem (đúng khuôn `rp-summary`). Thứ tự `subsystems` = thứ tự permissions.id, không theo cây catalog.

### PUT /admin/employee-roles/{id}
Body: `{"role_ids":[int] (bắt buộc, có thể rỗng), "company_ids":[int] (CHỈ gửi khi is_main_company — có key là 403 với
kiêm nhiệm, kể cả null), "all_department": bool, "manage_departments":[{"department_id", "part_ids":[int]}]}`.
Lỗi: 404 không làm ở C; 403 company_ids khi kiêm nhiệm; 422 `role_ids.N` (vai trò không thuộc C), `role_ids` (vai trò
khoá tick mới), `company_ids` (gỡ công ty chính), `company_ids.N` (công ty không tồn tại/ngừng hoạt động),
`manage_departments.N.department_id` (phòng ban khác C), `manage_departments.N.part_ids.M` / `.part_ids`.
OK: `{code:200, message:"Cập nhật thành công.", data:null}`.

## Self-review
- C luôn từ `current_company_role`; không nhận company_id. Không bypass super admin.
- Kiêm nhiệm không đọc/ghi vai trò công ty khác; `role_names` công ty khác chỉ trả cho quản trị viên công ty chính.
- Không N+1 ở danh sách: 3 truy vấn nạp sau phân trang (vai trò+đếm quyền, công ty, lịch sử), lịch sử mới nhất bằng
  subquery MAX(id).
- `permission_count` cùng điều kiện `permissions_count` GĐ2 (code not null, chưa deprecated).

## Concerns
1. `role_names` của công ty khác trong `companies` (chỉ khi C là công ty chính) — cần cho confirm "liệt kê vai trò sẽ
   mất" (design 4.1) nhưng chạm nguyên tắc "không ai thấy vai trò công ty khác". Bỏ được nếu user muốn chỉ báo số.
2. Không khoá dòng (lockForUpdate) khi lưu: 2 quản trị viên lưu cùng lúc ⇒ người sau thắng, lịch sử vẫn ghi đủ.
3. "Người cập nhật" ở danh sách chỉ lấy dòng `company_id = C` (theo brief); 50 dòng cũ NULL không tính, kể cả ở công ty chính.
4. Adapter vẫn gắn nhãn thay đổi vai trò là "Quyền" (code Task 1/cũ) — trái nhãn chuẩn "Vai trò"; không đổi vì ngoài brief.
5. Cờ `all_department` ở công ty chính: lưu xoá cả dòng cờ `(department_id NULL)` cũ ở C nếu có (màn cũ có thể tạo) —
   đúng ý "chỉ 1 nguồn theo loại", nhưng là thay đổi dữ liệu nếu tồn tại dòng như vậy.
6. FormRequest và controller resolve service 2 lần (không singleton) ⇒ `findWorking` chạy 2–3 truy vấn trùng; vô hại.

## Fix round 1

Changes:
1. `EmployeeRoleService::save()` now opens its own `DB::transaction` (when nested it becomes a savepoint). The cache flush runs after the transaction. The controller no longer wraps the call, and its `DB` import was removed. Docblock updated.
2. `EmployeePermissionAdapter::mapRow` now labels role changes "Vai trò" instead of "Quyền" (both the field and the item label). No test asserted the old label.
3. Removing company X now also writes one `employee_permission_history` row with `company_id = X`. Before = snapshot of E at X taken before the removal (roles + manage departments + companies). After = snapshot after the removal (empty roles/manage departments). It is in the same transaction and uses the shared helper `writeHistory()`. Assertion added to `test_go_cong_ty_go_luon_vai_tro_va_phan_cong`: exactly 1 row at C2, old.roles = ['Zz ER RC2'], 1 manager department, new roles and manager departments empty. The C1 row is now selected with `company_id = C1`.
4. Tests: `otherActiveCompany()` queries an active company other than C1/C2 and creates one (`ZZER_ACT`) if none exists. The inactive-company case now creates `ZZER_OFF` (status 0) with `makeCompany()` instead of relying on existing data.
5. `snapshot()`: parts are loaded with a single `whereIn(...)->pluck('name','id')` over all rows, then mapped per department.

Commands / output:
- `php vendor/bin/phpunit tests/Feature/Rbac/AdminEmployeeRoleApiTest.php` ⇒ `OK (13 tests, 129 assertions)`
- `php vendor/bin/phpunit tests/Feature/Rbac/EmployeeRoleHistoryTest.php` ⇒ `OK (2 tests, 9 assertions)`
- `php vendor/bin/phpunit tests/Feature/Rbac` ⇒ `OK (217 tests, 6078 assertions)`
- `php -l` is clean on the service and the controller.

Concern 4 of the first report is resolved by change 2.
