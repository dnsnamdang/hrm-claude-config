# Task 4 report — API Màn 1 "Quản lý tài khoản" + vá route cũ human/employee

Status: DONE_WITH_CONCERNS (không commit, không migration, không seeder)

## Đã làm
- Nhóm route `admin/accounts` (`routes/api.php`, sau `admin/employee-roles`), `auth:api`:
  - Đọc — `checkPermission:Quản lý tài khoản nhân viên|Xem danh sách tài khoản nhân viên theo tổng công ty|… theo công ty|… theo phòng ban|… theo bộ phận`
    (middleware tách `|`, đạt 1 tên là qua): `GET /` · `GET /export` · `GET /{id}` · `GET /histories/{id}` · `GET /histories/{id}/filter-options`.
  - Ghi — `checkPermission:Quản lý tài khoản nhân viên`: `POST /` · `PUT /{id}` · `POST /{id}/lock` · `POST /{id}/unlock`.
  - **Lệch brief có chủ đích:** lịch sử là `/histories/{id}` (không phải `/{id}/histories`) vì `SystemInfoSection` dựng URL
    `${endpointBase}/${entityType}/${entityId}` (+ `/filter-options`) — khuôn y như `master-data/products/histories/{id}`.
    FE: `<SystemInfoSection endpoint-base="admin/accounts" entity-type="histories" :entity-id="id" />`.
- `app/Services/Admin/AccountService.php` — lớp mỏng trên `Modules\Human\Services\EmployeeService` (không copy logic):
  index/attachListData/findInScope (404)/detail/create/update/setStatus/historyLogs/historyFilterOptions.
- `EmployeeService` (tách hàm, route cũ giữ hành vi):
  - `accountQuery(array $filters, bool $applyScope)` = phần join + bộ lọc của `getEmployees` cũ; thêm lọc `keyword`
    (mã/tên/email — khoá mới, route cũ không gửi). `getEmployees` gọi `accountQuery($f, !isset($f['is_all']))` + select/sắp
    xếp/paginate cũ nguyên văn ⇒ route cũ vẫn nhận `is_all`. API mới luôn `applyScope = true`, không đọc `is_all`.
  - `applyAccountViewScope($q)` = `checkPermissionList($q, [4 tên, true], 'employee_infos')` (hằng `ACCOUNT_VIEW_PERMISSIONS`).
  - `createEmployee`: `company_ids` có ⇒ `sync` như cũ (route cũ + EmployeeInfoController tự tạo TK); không có ⇒
    `attachMainCompany()` = `insertOrIgnore company_employees(employee, employee_infos.company_id)` (unique
    `company_employees_employee_company_unique`). Thêm ghi `created_by/updated_by = Auth::id()` (trước đây nhánh tạo mới bỏ sót).
  - `updateEmployee`: `companies()->sync(company_ids)` chỉ chạy khi có khoá `company_ids` (route cũ luôn gửi — `UpdateEmployeeRequest`
    bắt buộc — nên y như cũ); API mới không bao giờ truyền ⇒ không đụng company_employees. Thêm `updated_by = Auth::id()`.
    Đổi mật khẩu vẫn tăng `token_version` (code cũ, không đổi).
  - `changeStatus(Employee, $status)` = thân `EmployeeController::updateStatus` cũ (ghi `employee_history change_status` khi đổi,
    đồng bộ `employee_infos.status`) + `updated_by = Auth::id()`. Route cũ `updateStatus` gọi hàm này.
  - `historyRows($id)` = `formatHistories` + `resolveSnapshot` chuyển nguyên từ `EmployeeController` (route cũ `/{id}/histories`
    gọi lại hàm này, khuôn trả giữ nguyên; thêm 2 khoá phụ `changed_by_department`, `changed_at_full` + sắp phụ `id desc`).
- `Modules/Human/Routes/api.php`: `POST /`, `PUT /{id}`, `POST /{id}/updateStatus`, `DELETE /{id}` của `human/employee` bọc
  `checkPermission:Quản lý tài khoản nhân viên`. Mọi GET giữ nguyên.
- `AccountRequest` (chỉ `rules()`, 404 ở `authorize()` khi sửa ngoài phạm vi trước 422), `AccountResource`,
  `ExportColumnRegistry['admin_accounts']`, export theo khuôn `EmployeeRoleController::export` (DynamicExport + `fields`).

## TDD
- RED: `php vendor/bin/phpunit tests/Feature/Rbac/AdminAccountApiTest.php` ⇒ `Tests: 10, Assertions: 10, Failures: 10` — 9 ca
  "Expected [200|403] but received 404" (route chưa có); `test_route_cu_khong_quyen_403` "Expected [403] but received 200"
  (chứng minh lỗ hổng: POST /human/employee không quyền vẫn 200).
- GREEN: cùng lệnh ⇒ `OK (10 tests, 151 assertions)` (1 lần đỏ giữa chừng do payload test route cũ thiếu khoá `password` —
  FE cũ luôn gửi `password: null`; sửa test, không sửa code).
- Toàn bộ: `php vendor/bin/phpunit tests/Feature/Rbac` ⇒ `OK (232 tests, 6335 assertions)` (222 + 10).
- Test Human hiện có: `grep -rl "human/employee" Modules/*/Tests tests` ⇒ không có file nào (Modules/Human/Tests chỉ có 4 test
  Unit import danh mục, không đụng EmployeeService) ⇒ không có gì để chạy thêm.
- Ca: 9 ca brief + `test_chi_tiet_tai_khoan`. Fixture trỏ `mysql_tpe` về DB mặc định (hook cơm của model Employee đọc kết nối
  này, `.env` test không khai `DB_*_TPE`); 5 tên quyền trỏ 5 mã thử qua `permission_aliases` (DB test không có alias thật).

## File
- Mới: `app/Http/Controllers/Api/V1/Admin/AccountController.php`, `app/Services/Admin/AccountService.php`,
  `app/Http/Requests/Admin/AccountRequest.php`, `app/Http/Resources/Admin/AccountResource.php`,
  `tests/Feature/Rbac/AdminAccountApiTest.php`.
- Sửa: `routes/api.php` (+import, +nhóm), `Modules/Human/Routes/api.php`, `Modules/Human/Services/EmployeeService.php`,
  `Modules/Human/Http/Controllers/Api/V1/EmployeeController.php` (histories/updateStatus gọi service; bỏ 2 hàm private đã chuyển),
  `app/ExcelExport/ExportColumnRegistry.php` (+`admin_accounts`). Tất cả LF.

## Shape API (Task 5 dùng)

### GET /admin/accounts
Query: `keyword` (mã NV / tên / email, LIKE), `company_id`, `department_id`, `part_id` (theo employee_infos), `status` (`1` hoạt
động / `0` khoá), `rice_setting_location_id`, `per_page` (mặc định 10), `page`. `is_all` bị bỏ qua. Sắp theo khuôn
`Helper::applyDefaultEmployeeOrdering` (vị trí phòng ban → phòng ban → position_order_index) rồi id.
Response = khuôn `apiGetList` (như `/admin/employee-roles`): `{code, message, permissions:{can_manage:bool}, data:[...], links, meta:{total, per_page, current_page, ...}}`.
Mỗi dòng:
```
{ "id", "employee_info_id", "code", "fullname", "email",
  "company_id", "company_name",            // công ty chính (employee_infos.company_id)
  "department_id", "department_name", "part_id", "part_name",
  "rice_ssn": int|null, "rice_setting_location_id": int|null, "rice_setting_location_name": string|null,
  "limit_export_debt": float|null,           // FE tự toLocaleString('en-US')
  "status": 1|0, "status_text": "Hoạt động|Khoá", "status_color": "#16A34A|#DC2626",
  "created_by_name", "created_at": "d/m/Y H:i",          // employees.created_by / created_at (cũ: ~50% created_by NULL ⇒ null)
  "updated_by_name", "updated_at": "d/m/Y H:i" }         // dòng employee_history mới nhất; chưa có ⇒ employees.updated_by/updated_at
```
`permissions.can_manage` = có "Quản lý tài khoản nhân viên" (link Mã NV, nút Thêm/Sửa/Khoá).

### GET /admin/accounts/export
Cùng query + `fields=code,fullname,...` (key `ExportColumnRegistry['admin_accounts']`: code, fullname, email, created_by_name,
created_at, updated_by_name, updated_at, status_text, department_name, part_name, company_name, rice_ssn,
rice_setting_location_name, limit_export_debt). File `tai_khoan_nhan_vien.xlsx`.

### GET /admin/accounts/{id}
`{code, message, data:{...}}` — 404 ngoài phạm vi. Không trả password / company_ids.
```
{ "id", "employee_info_id", "email", "status", "status_text", "status_color",
  "image" (employee_infos.image, đường dẫn thô), "domain" (scheme+host như API cũ),
  "rice_setting_location_id", "rice_ssn": int|null, "is_rice_ssn": bool,   // chưa có mã ⇒ rice_ssn = max+1 gợi ý, is_rice_ssn=false (như form cũ)
  "limit_export_debt": float|null,
  "info": {"id","code","fullname","email","company_id","company_name","department_id","department_name","part_id","part_name"},
  "created_by_name", "created_at", "updated_by_name", "updated_at" }   // d/m/Y H:i
```

### POST /admin/accounts
Body: `employee_info_id`* (tồn tại, chưa có tài khoản), `email`* (email, unique), `status`* (0|1), `password`* (≥6, regex cũ),
`password_confirm`* (same), `rice_setting_location_id`, `limit_export_debt` (numeric ≥0 — gửi SỐ, không gửi chuỗi có dấu phẩy).
`company_ids` gửi lên bị bỏ. Mã check in cơm lấy từ `employee_infos.ssn` (như cũ). OK: `{code:200, message:"Tạo tài khoản thành công.", data:{id}}`.
422 Laravel chuẩn `{message, errors:{field:[...]}}`, báo hết lỗi một lần.

### PUT /admin/accounts/{id}
Body: `email`*, `status`*, `change_pass` (0|1|bool), `password` + `password_confirm` (bắt buộc khi change_pass), `rice_ssn`
(nullable integer, UniqueRiceSSN), `rice_setting_location_id`, `limit_export_debt`. Khoá không gửi ⇒ giữ giá trị đang có.
`employee_info_id` / `company_ids` bỏ qua. Thứ tự lỗi: 403 (không quyền quản lý) → 404 (ngoài phạm vi) → 422.
OK: `{code:200, message:"Cập nhật thành công.", data:null}`.

### POST /admin/accounts/{id}/lock | /unlock
Không body. OK `{code:200, message:"Đã khoá tài khoản."|"Đã mở khoá tài khoản."}`. Trạng thái không đổi ⇒ vẫn 200, không ghi lịch sử.

### GET /admin/accounts/histories/{id} (+ /filter-options)
Mảng DTO `SystemInfoSection`, mới → cũ:
```
{ "id", "action": "create|update|change_status",
  "action_label": "Tạo mới|Thay đổi thông tin|Khóa|Mở khóa",   // CatalogHistoryService::ACTION_LABELS
  "action_group": "create|update|status", "action_color",
  "actor_id", "actor_name", "actor_label" (Tên - Mã phòng - Mã NV), "department_name",
  "changes": [{"field","old","new"}],   // update: Email / Trạng thái / Công ty (tên, nối ", ") / Địa điểm nhận suất ăn /
                                         // Hạn mức công nợ xuất hàng (định dạng en) / Mật khẩu ("(trống)" → "Đã đặt lại (quản trị)"…)
                                         // change_status: [{field:"Trạng thái", old:"Hoạt động", new:"Khoá"}]; create: []
  "created_at": "d/m/Y H:i", "created_at_raw": "Y-m-d H:i:s" }
```
filter-options: `{actions:[{value:create,text:"Tạo mới"},{update,"Thay đổi thông tin"},{status,"Thay đổi trạng thái"}],
performers: HistoryPerformerOptions::forCompany(công ty người tạo tài khoản, không suy được ⇒ công ty chính của tài khoản)}`.

### Endpoint có sẵn FE form gọi thêm
- Danh sách hồ sơ chưa có tài khoản (ô "Hồ sơ nhân viên", màn Thêm): `GET human/employee-infos/getEmptyInfos` (như EmployeeForm cũ;
  trả `{code, data:[{id, fullname, code, email, department_id, ...}]}`, nhãn `employeeOptionText`).
- Chi tiết hồ sơ khi chọn (email, công ty, phòng ban, ảnh): `GET human/employee-infos/{infoId}` (như cũ).
- Địa điểm nhận suất ăn: `GET rice/setting/location` (như cũ, dùng khi `$store.state.use_rice`).
- Bộ lọc danh sách Công ty/Phòng ban/Bộ phận: `V2BaseCompanyDepartmentFilter` (nguồn sẵn có của component).

## Nơi còn gọi `human/employee?is_all=1` (hrm-client wt-rbac)
- `components/modals/AddEmployeeSingleModal.vue:287-297` `getData()` gửi `is_all: 1` (2 hàm khác cùng file `resetSearch()` :318,
  `getDataByWorkPosition()` :347 gọi `human/employee` KHÔNG có is_all). Modal này được dùng bởi
  `pages/training/teachers/components/TeacherForm.vue` và `pages/training/examiners/components/ExamierForm.vue`.
- Không còn nơi nào khác gửi `is_all` tới `human/employee`. GET khác tới route cũ: `pages/human/employee/index.vue` (màn cũ — Task 5 gỡ),
  `components/human-components/employee/EmployeeForm.vue` (GET `/{id}`, POST updateStatus, store `addEmployee`/`updateEmployee` ⇒ giờ cần quyền quản lý).

## Self-review
- Không nhận `company_id`/`is_all` để mở phạm vi; mọi thao tác theo id đi qua `findInScope` ⇒ 404. Không bypass super admin.
- Ghi trong `DB::transaction` (service). Không N+1: tên người tạo/cập nhật + dòng lịch sử mới nhất nạp 2 truy vấn sau phân trang.
- Route cũ: POST/PUT/updateStatus/DELETE giữ đúng logic (chỉ thêm middleware + `created_by/updated_by`), GET không đổi;
  `getEmployees` vẫn select/ordering/paginate y nguyên.
- Khoá tài khoản ngoài phạm vi / không quyền: không ghi gì (test kiểm DB sau 403/404).

## Concerns
1. `changeStatus` (khoá/mở khoá, cả route cũ lẫn mới) vẫn đồng bộ `employee_infos.status = status` như code cũ — khoá tài khoản
   cũng đổi trạng thái HỒ SƠ. Giữ để đúng hành vi cũ; nếu không mong muốn ở Màn 1 thì cần user chốt.
2. Tạo tài khoản không kiểm hồ sơ có trong phạm vi xem của người gọi (form cũ cũng không; `getEmptyInfos` trả hồ sơ mọi công ty,
   không gate quyền). Người chỉ có cấp "bộ phận" có thể tạo tài khoản cho hồ sơ công ty khác rồi không thấy nó ở danh sách.
3. Người chỉ có "Quản lý tài khoản nhân viên" (không cấp xem) chỉ thấy/sửa tài khoản có hồ sơ do mình tạo (đúng design 3.2 /
   code cũ) — có thể làm admin thắc mắc "có quyền quản lý mà không sửa được ai".
4. Thêm ghi `employees.created_by/updated_by` ở `createEmployee`/`updateEmployee`/`changeStatus` (dùng chung route cũ +
   EmployeeInfoController tự tạo TK) — thuần thêm dữ liệu, không đổi luồng.
5. Route lịch sử là `/admin/accounts/histories/{id}` thay vì `/{id}/histories` (lý do ở trên).
6. Nhãn: action "Khóa/Mở khóa" (bộ chuẩn CatalogHistoryService) vs giá trị trạng thái "Khoá" (theo brief) — 2 cách viết dấu
   cùng hiện trên timeline.
7. `employees.created_by` NULL ở ~49% tài khoản (rehearsal 632/1244) ⇒ cột "Người tạo" trống cho tài khoản cũ; không suy từ
   dòng `create` của lịch sử (chỉ 41 dòng).
