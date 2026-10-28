# Final-review fix GĐ2b — báo cáo

Status: DONE_WITH_CONCERNS (không commit, không migration; ERP không đụng)

## 1. [Important] Gỡ route ghi cũ `human/employee`
Rà nơi gọi (grep `human/employee` ngoài `-` / `_`):
- wt-rbac/hrm-client: chỉ GET (`CompanyDepartmentFilter` getEmployeesForFilter, `AddEmployeeSingleModal` apiGet x3); store `addEmployee`/`updateEmployee` không có dispatch nào.
- wt-rbac/TanPhatDev: 0. ERP-HRM/HRM/e2e: chỉ goto trang redirect `/human/employee`.
- TPE_APP: brief ghi `ERP-HRM/TPE_APP/lib` — thư mục này KHÔNG tồn tại; app nằm ở `TPE_APP/app/lib/...`. Grep cả `TPE_APP/` (bỏ .git/build/.dart_tool/.fvm): 1 chỗ, GET `v1/human/employee/getEmployeesForFilter` ⇒ không gọi route ghi.
⇒ Gỡ hẳn:
- `Modules/Human/Routes/api.php`: bỏ POST `/`, PUT `/{id}`, POST `/{id}/updateStatus`, DELETE `/{id}` (để comment). GET giữ.
- `EmployeeController`: xoá store/update/updateStatus/delete + import 2 request. Xoá file `Modules/Human/Http/Requests/CreateEmployeeRequest.php`, `UpdateEmployeeRequest.php` (chỉ controller dùng).
- `Modules/Human/Services/EmployeeService.php`: xoá `deleteEmployee`, `syncCompany` (0 caller); `updateEmployee` bỏ nhánh `companies()->sync(company_ids)`. `createEmployee` GIỮ nhánh `company_ids` (EmployeeInfoController tạo hồ sơ kèm tài khoản gửi `[company_id]`), `changeStatus`, `historyRows`, `accountQuery`… giữ.
- hrm-client `store/actions.js`: xoá `addEmployee`, `updateEmployee`.
- `AccountRequest` comment cập nhật.
- Test: `AdminAccountApiTest::test_route_cu_khong_quyen_403` → `test_route_ghi_cu_da_go` (có cả quyền quản lý: POST/PUT/DELETE 405, POST updateStatus 404; DB không đổi; GET 200). Bỏ đoạn "route cũ vẫn sync company_ids" trong `test_sua_khong_dong_den_company_employees`. HrmGateSideEffectsTest không có ca route cũ human/employee ⇒ không đổi.
- `php artisan route:list` hỏng sẵn (`Modules\Rice\Http\Controllers\RiceController` không tồn tại — không liên quan), nên kiểm route bằng test.

SQL chỉ đọc — dòng employee_has_roles mồ côi (công ty không có company_employees của NV đó):
```sql
SELECT COUNT(*) AS orphan_rows, COUNT(DISTINCT ehr.employee_id) AS employees
FROM employee_has_roles ehr
LEFT JOIN company_employees ce ON ce.employee_id = ehr.employee_id AND ce.company_id = ehr.company_id
WHERE ehr.company_id IS NOT NULL AND ce.id IS NULL;
```
Rehearsal 27/10: **12 dòng / 11 nhân viên** (company_id NULL: 0). Chưa dọn (để user quyết).

## 2. [Important] `company_ids.*` chỉ chặn công ty ngưng khi THÊM MỚI
`app/Http/Requests/Admin/EmployeeRoleSaveRequest.php`: rule còn `exists:companies,id` (không lọc status); `withValidator` tính `company_ids − company_employees(E,·)` rồi báo `company_ids.<i>` "Công ty X đang ngừng hoạt động, không thêm mới được." cho công ty status≠1. Test mới `AdminEmployeeRoleApiTest::test_cong_ty_ngung_dang_lam_thi_giu_duoc`: NV đang làm ở công ty ngưng ⇒ lưu 200, giữ đủ 3 công ty; thêm 1 công ty ngưng mới ⇒ 422 `company_ids.3`, không có lỗi `company_ids.2`, DB không thêm. Ca cũ `test_khong_go_duoc_cong_ty_chinh_422` (thêm mới công ty ngưng ⇒ 422 `company_ids.1`) vẫn xanh.

## 3. [Important] e2e header + rà chuỗi
`admin-employee-roles.spec.ts`: 'Tên' → 'Tên nhân viên'. Đo live 3011/8011 (namdangit): header Màn 2 = `STT, Mã NV, Email, Tên nhân viên, Phòng ban, Vai trò tại công ty này, Loại, Người cập nhật, Cập nhật lúc, Hành động` (khớp spec sau sửa); Màn 1 = `STT, Mã NV, Tên nhân viên, Email, Người tạo, Ngày tạo, Người cập nhật gần nhất, Ngày cập nhật gần nhất, Trạng thái, Hành động` (spec đúng sẵn). Th cao 32px. Đo live khớp: ô tìm `Tìm theo mã nhân viên, tên, email` (2 màn), span[title] `Sửa/Khoá/Lịch sử` (M1) và `Sửa/Quyền đang được cấp/Lịch sử` (M2), `.er-role-chip` 3 + `.er-role-more` "+4", popup chip "Quyền đang có — …", `#admin-employee-granted-permissions` có "Vai trò tại TPE", "· n trùng", "Phòng ban đang quản lý", `.gp-dup-bar` 1, `tr.gp-dup .gp-pname` = rgb(220, 38, 38), `.gp-table .table-wrapper` max-height none, popup Lịch sử "Lịch sử thay đổi: …" + "Thay đổi thông tin", `.er-main`/`.er-side` 798/399 (2.0), `.er-person__name`, `.v2-footer`, `.bulk-hdr-company` "Công ty: TPE — …", "Chọn vai trò", "NV bổ sung". Placeholder form Màn 1 (`Gõ để tìm hồ sơ chưa có tài khoản`, `Nhập email`), `Quay lại`, `Ở lại`, "chưa lưu" đối chiếu code.
Thêm 2 lỗi selector tìm được khi đo, đã sửa:
- Ca popup hàng loạt tìm `BulkPermissionModal` qua `el.__vue__` của DOM ⇒ undefined (b-modal portal ra body). Đổi sang đi cây `$children` từ `#__nuxt` (đo: tìm thấy, options.company TPE, 25 phòng ban, 102 vai trò).
- Nút `/^\s*Lưu\s*$/` (3 chỗ M2, 2 chỗ M1) và `confirmDialog(/^\s*Khoá\s*$/)` — regex trượt với V2BaseButton (memory playwright-nut-v2basebutton). Đổi sang `saveButton()` lọc chuỗi `'Lưu'` + hasNotText 'Tiếp tục'; `confirmDialog(page, 'Khoá', 'Mở')` / `('Mở khoá')`.

## 4. [Important] click label 0×0
Tái hiện: `.er-role-check label` = 0×0 ở 1280 (input 16×18). Spec M2: helper `tickRole()` = `input[type=checkbox].click({ force: true })` (2 chỗ). Đo: force click đổi tick + class `is-checked`, bấm lại trả về; dispatchEvent('click') thì KHÔNG cập nhật Vue (không dùng). admin-accounts.spec.ts không có mẫu click label. Header admin-accounts.spec.ts ghi rõ tài khoản test cần thêm "Quản lý phân quyền" (workingCompany() gọi bulk/options).
`--list` (Node 20: `PATH=$HOME/.nvm/versions/node/v20.20.1/bin:$PATH npx playwright test tests/admin/admin-accounts.spec.ts tests/admin/admin-employee-roles.spec.ts --list`; node mặc định 12 bị Playwright từ chối) ⇒ "Total: 25 tests in 5 files". Spec chưa chạy (theo quy tắc).

## 5. rice_setting_location_id exists
Model `Modules\Rice\Entities\Setting\RiceSettingLocation::$table = 'rice_setting_locations'` (SHOW TABLES xác nhận). Rule `exists:rice_setting_locations,id` trên kết nối mặc định — model khai `mysql_tpe`, nhưng .env test không có DB_*_TPE (dùng mysql_tpe sẽ "Unsupported driver []"), sau gộp DB 2 kết nối cùng CSDL. Test `AdminAccountApiTest::test_dia_diem_suat_an_phai_ton_tai`: PUT + POST id không tồn tại ⇒ 422 key `rice_setting_location_id`; id có thật ⇒ 200 + lưu.

## 6. Tổng hợp quyền hiệu lực bỏ vai trò khoá
Bằng chứng: `app/Support/Permissions/PermissionChecker.php` — docblock dòng 16 "Vai trò bị khoá thì mất hiệu lực"; `loadGrants()` dòng 229-230 join roles `r.status = 1`; `holdersQuery` dòng 170 `r.status = 1` ⇒ vai trò khoá không cấp quyền.
- BE `EmployeeRoleService::detail`: `summary` chỉ lấy vai trò đang tick VÀ status = 1.
- FE `pages/admin/employee-roles/_id/index.vue` computed `summary`: bỏ vai trò `status !== 1`.
- Test `test_tong_hop_bo_vai_tro_khoa`: NV giữ RA (1 view) + RL khoá (1 action) ⇒ total 1, action 0; mở khoá RL ⇒ total 2, action 1.
- UI (8b): NV 789 giữ vai trò Zz (4 quyền) ⇒ ô tổng 4; khoá vai trò ⇒ BE summary 0, FE ô tổng "0", "Xem 0 Thao tác 0 Duyệt 0", dòng vai trò vẫn tick + `is-locked`.

## 7. Code chết
- `Modules/Timesheet/Services/EmployeeService.php`: grep `storeRole|logPermissionHistory|buildPermissionSnapshot|permissionHistories` 0 caller ⇒ xoá 4 hàm (cả `permissionHistories` — reader cũ cũng 0 caller) + import thừa (225 dòng). Lớp giữ (JobAssignment* còn inject). Comment adapter/EmployeeRoleService cập nhật.
- `Modules/Timesheet/Services/BulkPermissionService.php`: `apply()` 0 caller ngoài (BulkRoleGrantTest::apply là helper HTTP riêng) ⇒ xoá. Mọi caller đều truyền `$byWorkingCompany = true` ⇒ bỏ tham số + nhánh false (`employee_infos.company_id`, các whereNotNull "có gán bất kỳ"), `$scopeCompanyId` thành `int`. Cập nhật 5 caller (EmployeeRoleController x3, EmployeeRoleService::bulkGrant, EmployeeRoleBulkApplyRequest). Docblock lớp sửa ("chỉ đọc").

## 8. Kiểm Playwright (127.0.0.1:3011, API 8011 trực tiếp)
(a) /admin/accounts: request `http://127.0.0.1:8011/api/v1/admin/accounts?page=1&per_page=10`, meta.total 1244, 10 dòng tbody = min(total, per_page), DOM "Hiển thị 1–10 / 1244". /admin/employee-roles: total 830, 10 dòng.
(b) Bulk Áp dụng thật: tạo vai trò qua API `POST /admin/roles {base_name:'Zz GD2b bulk', copy_from_role_id:15}` ⇒ id 108564 (`TPE_Zz GD2b bulk`, 4 quyền, company 1). Popup: NV bổ sung = "Phạm Gia Tài - HN_CSKH - 12310426" (employee 789, chưa có vai trò ở TPE), chọn vai trò Zz ⇒ "Tổng SL NV sẽ cập nhật: 1", 1 dòng; bấm "Áp dụng" ⇒ popup đóng. DB: `employee_has_roles(789, 108564, company 1, App\Employee)`; `employee_permission_history` 1 dòng id 56, employee 789, **company_id 1**, action update, changed_by 13, old roles [] → new ["Zz GD2b bulk"]. Danh sách tìm 12310426: chip "Zz GD2b bulk"; popup Lịch sử: "27/10/2026 15:46 Thay đổi thông tin … Vai trò thêm mới: - Zz GD2b bulk". Sau đó khoá vai trò (POST lock) để kiểm mục 6.
Dọn (rehearsal):
```sql
DELETE FROM employee_has_roles WHERE role_id=108564 AND employee_id=789 AND company_id=1;
DELETE FROM employee_permission_history WHERE id=56 AND employee_id=789;
DELETE FROM role_permission_history WHERE role_id=108564;   -- 2 dòng (create, lock)
DELETE FROM role_has_permissions WHERE role_id=108564;      -- 4 dòng
DELETE FROM roles WHERE id=108564 AND name='TPE_Zz GD2b bulk';
```
Đã quét mọi bảng có cột role_id: chỉ 3 bảng trên dính 108564. Kiểm sau dọn: roles '%Zz GD2b%' 0, employee_has_roles(789) 0, employee_permission_history(789) 0. Đã forget `spatie.permission.cache`. Tick thử ở NV 195 (ca 4) không bấm Lưu. Đã đóng tab MCP.

## Test
- hrm-api `tests/Feature/Rbac`: **OK (238 tests, 6387 assertions)**. Riêng AdminAccountApiTest 11/11, AdminEmployeeRoleApiTest 18/18.
- ERP: không đụng ⇒ không chạy.
- nuxt3011.log: không có ERROR / Failed to compile (chỉ WARN favicon.ico có sẵn); hot reload đã nạp sửa FE (ô tổng ra 0 khi vai trò khoá).

## Concerns
1. 12 dòng employee_has_roles mồ côi trên rehearsal chưa dọn — cần user quyết (xoá hay thêm company_employees).
2. App mobile/client ngoài repo đã rà (nếu có) gọi route ghi cũ sẽ nhận 404/405 — đúng Ruling.
3. Exists địa điểm suất ăn dùng kết nối mặc định, không theo `mysql_tpe` của model (đúng sau gộp DB).
4. Dòng vai trò bulk ghi `model_type = App\Employee` (theo guard của vai trò qua Employee::grantRoles) — hành vi có sẵn, không đổi.
5. Selector nút xác nhận Khoá/Mở khoá ở admin-accounts.spec chỉ đối chiếu code, chưa bấm thật (không khoá tài khoản thật).

## Bổ sung (coordinator): exists địa điểm suất ăn theo kết nối model
`AccountRequest`: `Rule::exists(RiceSettingLocation::class, 'id')` (thêm import model). Laravel 8.83.29 resolve kết nối của model — tinker: `(string) Rule::exists(RiceSettingLocation::class,'id')` = `exists:mysql_tpe.rice_setting_locations,id`. Test: AdminAccountApiTest đã trỏ `database.connections.mysql_tpe` về kết nối mặc định ở setUp (.env test không có DB_*_TPE) ⇒ `test_dia_diem_suat_an_phai_ton_tai` đi qua mysql_tpe. Kết quả: AdminAccountApiTest OK (11 tests, 154 assertions). Concern 3 ở trên đã đóng.
