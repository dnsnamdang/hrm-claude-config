# Task 8 report — Đóng màn cũ (hrm-client, hrm-api, ERP)

Status: DONE_WITH_CONCERNS. Không commit, không migration, không seeder.

## hrm-client (wt-rbac/hrm-client)
- `pages/timesheet/setting/employees/index.vue` → trang chuyển hướng 301 `/admin/employee-roles` (khuôn Task 5 `pages/human/employee/*`). Code chết dòng 290 (`apiDelete timesheet/roles/{id}`) mất theo.
- `pages/timesheet/setting/employees/_id/index.vue` → chuyển hướng 301 `/admin/employee-roles/:id`.
- `store/actions.js`: bỏ action `saveEmployee` (POST `timesheet/employees`) — nơi gọi duy nhất là trang cũ `_id/index.vue:500`.
- `components/timesheet/setting/roles/BulkPermission*`: không còn (GĐ2 đã gỡ) — không phải làm gì.
- Grep (bỏ node_modules/.nuxt*/log): `timesheet/employees|timesheet/roles|bulk-permissions|timesheet/setting/employees` chỉ còn trong 2 comment (`components/subsystem-menu/admin.js:52`, `pages/admin/employee-roles/index.vue:185`). Không menu/link nào trỏ `/timesheet/setting/employees`. Các component trang cũ import (SystemInfoSection, SettingHistoryModal, ConfirmDeleteTimeshift, mixin) là dùng chung, giữ.
- Playwright MCP (127.0.0.1:3011, JWT NV 13): `/timesheet/setting/employees` → `location.pathname = /admin/employee-roles` (bảng render); `/timesheet/setting/employees/13` → `/admin/employee-roles/13` (title "Vai trò nhân viên: DNS01"); console 0 lỗi. Tab đã đóng.
- nuxt3011.log: không có `ERROR/Failed to compile/Module not found` (log không ghi lượt HMR mới; trang mới biên dịch và chạy được qua Playwright).

## hrm-api (wt-rbac/hrm-api)
Route gỡ khỏi `Modules/Timesheet/Routes/api.php` (thay bằng 1 comment) + bỏ 3 `use`:
- `GET timesheet/roles/list`
- `timesheet/bulk-permissions/{preview-employees,eligible-additional-employees,apply,export-employees}`
- `timesheet/employees` GET `/`, POST `/`, GET `/export`, GET `/histories`, GET `/{id}`

Bằng chứng không còn nơi gọi: grep hrm-client (trên); grep `*.php|*.js|*.ts` trong hrm-api + TanPhatDev: chỉ còn comment + test (đã sửa); `HRM/e2e/**/*.ts`: 0 kết quả.

File chết xoá (chỉ được route/controller cũ dùng, đã grep):
- `Modules/Timesheet/Http/Controllers/Api/V1/{RoleController,BulkPermissionController,EmployeeController}.php`
- `Modules/Timesheet/Http/Requests/{BulkPermissionApplyRequest,EmployeeRoleStoreRequest}.php`
- `Modules/Timesheet/Transformers/EmployeeResource/{ListResource,DetailResource}.php`, `Transformers/RoleResource/RoleListResource.php` (+ 2 thư mục rỗng)
Giữ: `BulkPermissionService` (route mới dùng), `BulkPermissionPreviewRequest` (EmployeeRoleBulkRequest kế thừa), `Timesheet\Services\RoleService` (test HrmGateSideEffects gọi), `Timesheet\Services\EmployeeService` (JobAssignment*, adapter dùng).

Sửa khác:
- `app/Services/SettingHistory/Adapters/EmployeePermissionAdapter.php`: comment quyền không còn trỏ route cũ.
- `app/Support/Permissions/Catalog/admin.php`: comment NGỪNG DÙNG trên `admin.tai_khoan.manage` (xem concern 1) — không đổi dữ liệu catalog.

Test:
- `tests/Feature/Rbac/HrmGateSideEffectsTest::test_man_vai_tro_cu_da_go_route`: `timesheet/roles/list` 200 → 404; thêm 404 cho 5 route `timesheet/employees*` và 4 route `bulk-permissions/*`. RED trước khi gỡ (`Expected 404 but received 200`), GREEN sau.
- `tests/Feature/Rbac/BulkRoleGrantTest.php`: chuyển 4 ca sang `POST /api/v1/admin/employee-roles/bulk/apply` (C = current_company_role, bỏ claim JWT): vai trò công ty khác ⇒ 422 `role_ids.1` không ghi; cấp lặp ⇒ 1 dòng; người không làm ở C ⇒ 422 `additional_employee_ids.1`; vai trò chưa chuyển đổi (company_id NULL) ⇒ màn mới 422 `role_ids.0`. Các ca gọi thẳng `Employee::grantRoles` giữ nguyên. Giữ vì phần `grantRoles` không có ở AdminEmployeeRoleBulkTest.
- `tests/Feature/Rbac` ⇒ **OK (235 tests, 6368 assertions)**.

## ERP (wt-rbac/TanPhatDev — trước task cây sạch)
`routes/web.php` nhóm `employees`:
- Gỡ: `employeeCreate`, `employeeStore`, `employeeDelete`, `employeeUpdate`, `employee.doimatkhau`, `employee.searchEmployeeForFilter` (chỉ index.blade gọi), `employee.exportList` (chỉ index.blade gọi).
- `employeeIndex` = `Route::redirect('/', HRM/admin/accounts)`, `employeeEdit` = `Route::redirect('/{id}/edit', HRM/admin/accounts)` — đích `rtrim(config('app.hrm_url_FE'), '/') . '/admin/accounts'` y khuôn redirect `roleIndex` GĐ2. Giữ tên route vì `searchData`/`searchDataEmployee` còn render `route('employeeEdit', id)` trong cột thao tác. Route::redirect nhận mọi method ⇒ POST /admin/employees cũng chỉ chuyển hướng.
- Giữ (còn nơi gọi): `employee.searchData` (BillIncomeRequestDetail.blade:234, BillPaymentRequestDetail.blade:463 — vẫn `checkPermission:Quản lý tài khoản`), `searchDataEmployee` (HandOverWorkDetailEmployee, BusinessTargetForEmployee), `searchEmployeeByKeyword` (~7 màn kế toán), `{id}/getDataEmployee` (income_expenditure/bill_payment_requests/formJs.blade:92), `checkHasPermission` (7 màn duyệt), `employee.history` (searchData còn render link).
- Gỡ thêm `employee_infos/{id}/basic` (`employeeInfoBasic`, gate "Quản lý tài khoản"): nơi gọi duy nhất là `common/employees/{create,edit}.blade.php` đã xoá. Method `EmployeeInfosController@basic` để nguyên (chết).
- `app/Http/Controllers/Common/EmployeesController.php`: xoá method chết index/create/edit/store/update/delete/rejectRolesOfOtherCompany/sortRolesToSync/searchEmployeeForFilter/doimatkhau/exportList (không class nào khác gọi; `php -l` OK). Giữ getEmployeeInfoIdsByPosition, sortRolesByCompanyOrder (searchData dùng).
- Xoá view `resources/views/common/employees/{index,create,edit}.blade.php` (không còn `view()`/`@include` nào trỏ tới; còn history + change_profile_info).
- Menu: `layouts/topmenubar.blade.php` (layout đang dùng, app.blade:86): "Quản lý tài khoản người dùng" → HRM `/admin/accounts`, chỉ hiện khi có 1 trong 5 quyền Màn 1 (design Q1) — tra `auth()->user()->permissionChecker()->hasLegacy(tên, 'api')` trong khối `@php` (không closure, không @json); thêm "Vai trò nhân viên" → HRM `/admin/employee-roles` ngay sau "Vai trò", không gate như mục "Vai trò" GĐ2. `layouts/sidebar.blade.php` (Thêm mới → `/admin/accounts/add`, Danh sách → `/admin/accounts`, + Vai trò nhân viên) và `layouts/topmenubar_old.blade.php` (Danh sách người dùng → `/admin/accounts`, + Vai trò nhân viên) cùng cách gate. 2 file này không được include ở đâu.
- `app/Http/Controllers/HomeController.php:916` widget "Tài khoản chưa phân quyền": link → HRM `/admin/accounts` (bỏ `?status=2`, HRM chưa có lọc này).
- `tests/Unit/Rbac/RawPermissionLookupGuardTest.php`: bỏ mục allowlist của EmployeesController (code đã xoá — test báo "mục thừa").

Test ERP (`tests/Feature/Rbac/ErpGateSideEffectsTest.php`):
- Thay `test_man_tai_khoan_bao_loi_vai_tro_khong_thuoc_cong_ty` (đánh vào PUT cũ — RED sau khi gỡ: `Expected 200 but received 404`) bằng `test_man_tai_khoan_cu_da_go_chuyen_sang_hrm`: GET index/edit, POST store, GET route('employeeEdit') ⇒ redirect HRM; PUT/create/delete/doimatkhau/exportList/searchEmployeeForFilter/employee_infos basic ⇒ 404; route name đã gỡ không còn; view đã gỡ; employees + employee_has_roles không đổi; route tra cứu còn.
- `test_route_tai_khoan_cu_chuyen_huong_cache_duoc`: `employeeIndex`, `employeeEdit` không phải Closure + `prepareForSerialization()`.
- `test_menu_tai_khoan_tro_hrm`: 3 layout không còn `route('employeeIndex'|'employeeCreate'|'employeeEdit')`, có `/admin/employee-roles`; biên dịch Blade 3 layout + `php -l` bản biên dịch ⇒ 0; render thật `layouts.topmenubar`: NV không quyền ⇒ không có link `/admin/accounts`, có "Vai trò nhân viên"; NV có "Xem danh sách tài khoản nhân viên theo bộ phận" (alias api tạo trong transaction) ⇒ có link. sidebar/topmenubar_old không render được từ trước (gọi `route('proCreate')` không tồn tại) nên chỉ kiểm biên dịch.
- Lệnh: `DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test DB_DATABASE_SECOND=hrm_erp_rbac_test php -d variables_order=EGPCS vendor/bin/phpunit tests/Feature/Rbac` ⇒ **OK (25 tests, 238 assertions)**; `tests/Unit/Rbac` ⇒ **OK (3 tests)**. Lưu ý: chạy như common.md mà không có `DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test` thì phpunit.xml ép sqlite `:memory:` ⇒ 23/23 fail ở guard DB của fixture (không liên quan code).

## Concerns
1. **`admin.tai_khoan.manage` chưa thể ngừng dùng thật.** Trong danh mục không có cờ deprecated theo từng mục; cơ chế GĐ1 duy nhất là bỏ mục khỏi danh mục (CatalogSync đặt `deprecated_at`, xoá alias) + đưa tên cũ vào `dropped_legacy.php` — đổi luật chuyển đổi GĐ1 (brief cấm). Thêm nữa ERP còn `employee.searchData` gate bằng "Quản lý tài khoản" (bảng chọn nhân viên ở phiếu thu/phiếu chi): đặt `deprecated_at` là PermissionChecker bỏ mã ⇒ bảng chọn đó 403 với mọi người. Nên chỉ ghi comment NGỪNG DÙNG ở `Catalog/admin.php`. Cần user chốt: (a) đổi gate searchData sang quyền khác (vd. quyền xem phiếu thu/chi) rồi mới bỏ mã khỏi danh mục, hoặc (b) để như hiện tại.
2. **Báo cáo "có quyền ERP mà không có Quản lý tài khoản nhân viên"** chưa đưa vào `rbac:convert` (bước 8 đọc bảng `rbac_new_*` trong transaction — sửa lệnh GĐ1 không phải việc nhỏ). Câu SQL chạy sau chuyển đổi (chỉ đọc), trên rehearsal ra đúng 1 người: employee 258 Đỗ Văn Thao (thaodv.qttt@tanphat.com) @ TPE (company 1):
```sql
SELECT h.employee_id, h.company_id, c.code AS company_code, ei.fullname, e.email
FROM employee_has_roles h
JOIN roles r ON r.id = h.role_id AND r.company_id = h.company_id AND r.status = 1
JOIN role_has_permissions rhp ON rhp.role_id = r.id
JOIN permissions p ON p.id = rhp.permission_id AND p.code = 'admin.tai_khoan.manage'
JOIN company_employees ce ON ce.employee_id = h.employee_id AND ce.company_id = h.company_id
JOIN employees e ON e.id = h.employee_id
LEFT JOIN employee_infos ei ON ei.id = e.employee_info_id
LEFT JOIN companies c ON c.id = h.company_id
WHERE NOT EXISTS (
  SELECT 1 FROM employee_has_roles h2
  JOIN roles r2 ON r2.id = h2.role_id AND r2.company_id = h2.company_id AND r2.status = 1
  JOIN role_has_permissions rhp2 ON rhp2.role_id = r2.id
  JOIN permissions p2 ON p2.id = rhp2.permission_id AND p2.code = 'human.tai_khoan_nhan_vien.manage'
  WHERE h2.employee_id = h.employee_id AND h2.company_id = h.company_id)
GROUP BY h.employee_id, h.company_id, c.code, ei.fullname, e.email ORDER BY h.company_id, h.employee_id;
```
   Đề xuất đưa vào runbook deploy (chạy sau convert), hoặc thêm CSV vào rbac:convert ở một task riêng.
3. Gate menu ERP lấy công ty kiểm quyền của ERP (`info->company_id`, như mọi `can()` ở ERP), còn HRM Màn 1 lấy `company_role` ⇒ NV kiêm nhiệm có thể thấy/không thấy mục menu khác với quyền thực ở HRM (HRM vẫn chặn đúng). Mục "Vai trò nhân viên" không gate (như "Vai trò" GĐ2).
4. Ngoài brief (đã làm vì chỉ còn gọi từ view đã xoá): gỡ route ERP `employeeInfoBasic`; xoá method chết của ERP EmployeesController; xoá action `saveEmployee` hrm-client. `BulkPermissionService` còn nhánh `$byWorkingCompany = false` (hành vi cũ, nay không ai gọi) và `RoleService::list`/các hàm của Timesheet EmployeeService chỉ route cũ dùng — để nguyên, dọn ở lượt khác nếu muốn.
5. Widget trang chủ ERP mất bộ lọc "Chờ phân quyền" (HRM /admin/accounts không có `status=2`); link chỉ mở danh sách.
6. `php artisan route:list` ở hrm-api lỗi sẵn (`Modules\Rice\Http\Controllers\RiceController` không tồn tại) — không liên quan; đã kiểm route bằng test 404.

## Fix round 1 (review)
1. [Important] Gate menu ERP gom về 1 chỗ: `TanPhatDev/app/Employee.php` thêm hằng `HRM_ACCOUNT_SCREEN_PERMISSIONS` (5 tên quyền Màn 1) + `canOpenHrmAccountScreen()` (đặt cạnh `hasAnyPermission`, dùng `permissionChecker()->hasLegacy(tên, 'api')`, không có checker ⇒ false). 3 layout `sidebar` / `topmenubar` / `topmenubar_old` bỏ khối `@php` + danh sách cứng, chỉ còn `@if (auth()->user() && auth()->user()->canOpenHrmAccountScreen())` kèm 1 comment Blade.
2. [Minor] Comment cũ: `hrm-api/app/Services/Admin/EmployeeRoleService.php:428-429` (ghi `timesheet/roles/list` đã gỡ ở GĐ2b), `app/Services/SettingHistory/Adapters/RolePermissionAdapter.php:24` (trỏ nhóm route `/admin/roles`, route cũ `timesheet/roles/*` đã gỡ). Grep `timesheet/roles|timesheet/employees` trong app/Modules/routes chỉ còn các comment ghi "đã gỡ".
- Không đụng mục deprecate catalog / báo cáo chuyển đổi (controller đã chuyển lên user).
- Test: ERP `tests/Feature/Rbac` OK (25 tests, 238 assertions; gồm test_menu_tai_khoan_tro_hrm), ERP `tests/Unit/Rbac` OK (3), hrm-api `tests/Feature/Rbac` OK (235 tests, 6368 assertions).
