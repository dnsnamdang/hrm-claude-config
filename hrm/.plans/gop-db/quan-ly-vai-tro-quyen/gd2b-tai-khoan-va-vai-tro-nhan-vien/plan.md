# GĐ2b — Màn Quản lý tài khoản + Màn Quản lý vai trò nhân viên · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans. Steps dùng `- [ ]`.

**Goal:** Tách 2 màn ở phân hệ Quản trị — Quản lý tài khoản `/admin/accounts` (thông tin tài khoản) và Quản lý vai trò nhân viên `/admin/employee-roles` (công ty làm việc, cấp/gỡ vai trò, phân công phòng ban, quyền đang được cấp, phân quyền hàng loạt) — đóng `/human/employee`, `/timesheet/setting/employees` và ERP `employees`, vá 2 lỗ hổng API tài khoản.

**Architecture:** hrm-api thêm 2 nhóm API trong `app/` cạnh `/admin/roles` (controller + service mỏng dùng lại `Modules\Human\Services\EmployeeService`, `Employee::syncRolesInCompany`, `BulkPermissionService`), mọi thao tác bó theo công ty đang làm việc `C = auth()->user()->current_company_role`. Lịch sử vai trò nhân viên tách theo công ty bằng cột `company_id` mới của `employee_permission_history`. hrm-client dựng 2 màn theo `list-page` + mockup đã duyệt, dùng lại `RolePermissionsViewModal` (GĐ2), `SystemInfoSection`, `BulkPermissionModal`. ERP chỉ gỡ màn + chuyển hướng.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Laravel 6 (ERP TanPhatDev), Nuxt 2.14 / Vue 2 / Bootstrap-Vue (hrm-client), PHPUnit, Playwright MCP.

**Spec:** `gd2b-tai-khoan-va-vai-tro-nhan-vien/design.md` + `mockup.html` (duyệt 27/10/2026); nền `../design.md`, `../gd2-man-quan-ly/design.md`.

## Global Constraints

- Repo/nhánh: `wt-rbac/hrm-api`, `wt-rbac/hrm-client`, `wt-rbac/TanPhatDev` — nhánh `rbac`. **Không commit** (user tự báo). Code chỉ bắt đầu khi user nói "làm" kèm phạm vi.
- **Đúng 1 migration**: `hrm-api/database/migrations/2026_11_02_000001_add_company_id_to_employee_permission_history.php` (thêm `company_id` unsignedBigInteger nullable + index, không đụng dữ liệu). Chỉ chạy vào `hrm_erp_rbac_test` bằng `--path`, sau khi user cho phép riêng. Không seeder.
- DB PHPUnit: `hrm_erp_rbac_test` (`.env` của wt-rbac/hrm-api). Kiểm UI: `hrm_erp_rbac_rehearsal` (API `php -S` cổng 8011 với `DB_DATABASE` env, Nuxt 3011) — chỉ đọc, trừ dữ liệu thử có tiền tố `Zz` và dọn sạch sau khi kiểm.
- PHP: `/opt/homebrew/opt/php@7.4/bin/php`. Test hrm-api: `php vendor/bin/phpunit tests/Feature/Rbac`. Test ERP: `php -d variables_order=EGPCS vendor/bin/phpunit tests/Feature/Rbac`.
- Gate: Màn 1 đọc = một trong 4 tên quyền "Xem danh sách tài khoản nhân viên theo …" hoặc "Quản lý tài khoản nhân viên"; ghi = `checkPermission:Quản lý tài khoản nhân viên`. Màn 2 mọi API = `checkPermission:Quản lý phân quyền`.
- `C` luôn lấy từ `current_company_role`, không nhận `company_id` từ request. Nhân viên không làm việc ở C (Màn 2) / tài khoản ngoài phạm vi xem (Màn 1) ⇒ **404**.
- Sau mọi ghi vai trò / phân công: `PermissionChecker::flush()` + `app('cache')->forget('spatie.permission.cache')`.
- Nhãn: "Vai trò" (cấm "chức vụ" trong nhãn mới), "Người tạo/Ngày tạo", "Người cập nhật gần nhất/Ngày cập nhật gần nhất" (Màn 1), "Người cập nhật/Cập nhật lúc" (Màn 2).
- FE: chỉ `V2Base*`, `V2BaseModal`, `$confirm`, `V2Footer`, `unsavedChangesMixin`; lịch sử theo skill `entity-history` (`SystemInfoSection` + popup `V2BaseModal` bọc nó); cờ quyền mặc định `false`; số `toLocaleString('en-US')`; chữ đỏ chỉ cho lỗi và quyền trùng (user chốt).
- Bố cục đúng `mockup.html`: Màn 2 chi tiết 2 panel `col-lg-8` / `col-lg-4`, lịch sử full ngang dưới.

## Review Focus

1. Quản trị viên công ty **kiêm nhiệm** gửi `company_ids` hoặc `role_ids` của công ty khác ⇒ 403 / 422, không đổi gì. → Task 2 test `test_kiem_nhiem_khong_sua_cong_ty_lam_viec`, `test_vai_tro_cong_ty_khac_422`.
2. Gỡ công ty X khỏi công ty làm việc khi nhân viên còn vai trò + phân công ở X ⇒ cả hai bị gỡ trong cùng transaction, lịch sử ghi đủ. → Task 2 test `test_go_cong_ty_go_luon_vai_tro_va_phan_cong`.
3. Phân quyền hàng loạt gửi `department_ids` / `employee_ids` / `role_ids` của công ty khác ⇒ 422 (hiện popup cũ cho chọn chéo công ty). → Task 3 test `test_bulk_id_cong_ty_khac_422`.
4. Route cũ `POST/PUT /human/employee`, `POST /human/employee/{id}/updateStatus` gọi bằng tài khoản không có "Quản lý tài khoản nhân viên" ⇒ 403; API mới bỏ qua tham số `is_all`. → Task 4 test `test_route_cu_khong_quyen_403`, `test_is_all_khong_bo_qua_pham_vi`.
5. Lịch sử: dòng cũ `company_id` NULL chỉ quản trị viên công ty chính xem; quản trị viên công ty kiêm nhiệm chỉ thấy dòng của mình. → Task 1 test `test_lich_su_tach_theo_cong_ty`.

---

### Task 1: Lịch sử vai trò nhân viên tách theo công ty

**Files:**
- Create: `hrm-api/database/migrations/2026_11_02_000001_add_company_id_to_employee_permission_history.php`
- Modify: `hrm-api/app/Services/SettingHistory/Adapters/EmployeePermissionAdapter.php` (`authorize`, `fetchRows`, `mapRow`)
- Test: `hrm-api/tests/Feature/Rbac/EmployeeRoleHistoryTest.php`

**Interfaces (Produces):**
- Cột `employee_permission_history.company_id` (nullable, index `eph_company_idx`).
- Adapter: `authorize($id)` = nhân viên làm việc ở C; `fetchRows($id)` = dòng `company_id = C`, cộng dòng `company_id IS NULL` khi C là công ty chính của nhân viên.

- [x] Hỏi user cho phép chạy migration (nêu tên file, DB `hrm_erp_rbac_test`, `migrate --pretend` output). Chưa có "làm" thì dừng task này.
- [x] Viết `test_lich_su_tach_theo_cong_ty`: fixture nhân viên E công ty chính C1, kiêm nhiệm C2; chèn 3 dòng (`NULL`, `C1`, `C2`); gọi `setting-histories/employee_permission/{E}` với `current_company_role = C1` ⇒ 2 dòng; `= C2` ⇒ 1 dòng (C2); E không làm việc ở C3 ⇒ 403/404 giữ đúng mã hiện tại của `SettingHistoryController` (ruling I2 GĐ2: 403).
- [x] Chạy ⇒ FAIL. Viết migration (PHPDoc `up/down`, không `DB::transaction`), chạy `--path` vào test DB. Sửa adapter. Chạy ⇒ PASS.

### Task 2: API Màn 2 — danh sách, chi tiết, lưu

**Files:**
- Create: `hrm-api/app/Http/Controllers/Api/V1/Admin/EmployeeRoleController.php`, `hrm-api/app/Services/Admin/EmployeeRoleService.php`, `hrm-api/app/Http/Requests/Admin/EmployeeRoleSaveRequest.php`, `hrm-api/app/Http/Resources/Admin/EmployeeRoleResource.php`
- Modify: `hrm-api/routes/api.php` (nhóm `admin/employee-roles`, cạnh `admin/roles`), `hrm-api/app/ExcelExport/ExportColumnRegistry.php` (key `admin_employee_roles`)
- Test: `hrm-api/tests/Feature/Rbac/AdminEmployeeRoleApiTest.php` (+ dùng `Concerns/AdminRoleFixture`)

**Interfaces (Produces):**
- Routes: `GET /admin/employee-roles` · `GET /export` · `GET /{id}` · `PUT /{id}` (id = `employees.id`).
- `EmployeeRoleService::findWorking(int $employeeId): Employee` — 404 nếu không có `company_employees(E, C)`.
- `EmployeeRoleService::isMainCompany(Employee $e): bool` — `employee_infos.company_id === C`.
- `EmployeeRoleService::save(Employee $e, array $roleIds, ?array $companyIds, array $manageDepartments): void` — 1 transaction: `Employee::syncRolesInCompany(E, C, roleIds)`; nếu `companyIds !== null` (chỉ công ty chính) đồng bộ `company_employees`, mỗi công ty bị gỡ X ⇒ `syncRolesInCompany(E, X, [])` + xoá `employee_manage_departments(E, X)`; ghi phân công **chỉ dòng của C** (cờ "tất cả" theo design 4.4); ghi 1 dòng `employee_permission_history` (`company_id = C`, snapshot vai trò/công ty làm việc/phân công tại C, giá trị hiển thị); flush cache.
- Danh sách trả: `id, code, email, fullname, department_name, roles[{id,name,permission_count}], kind (main|concurrent), status, updated_by_name, updated_at` (2 cột cuối = dòng lịch sử mới nhất `company_id = C`). Lọc: `keyword` (mã/tên/email, EXISTS), `department_id`, `part_id`, `role_ids[]`, `kind`, `status`, `no_role` (0/1).
- Chi tiết trả: thông tin nhân viên, `is_main_company`, `companies[{id,code,name,is_main}]`, `roles` (mọi vai trò của C: `id, base_name, description, status, permission_count, checked`), `all_department`, `manage_departments[{department_id, part_ids[]}]` tại C, `summary` (đếm quyền hiệu lực tại C theo kind + phân hệ).

- [x] Viết test: `test_danh_sach_chi_nhan_vien_lam_viec_o_C` (gồm kiêm nhiệm, gồm tài khoản khoá), `test_khong_lam_viec_o_C_404`, `test_luu_vai_tro_cong_ty_chinh`, `test_kiem_nhiem_khong_sua_cong_ty_lam_viec` (gửi `company_ids` ⇒ 403), `test_vai_tro_cong_ty_khac_422`, `test_tick_moi_vai_tro_khoa_422_giu_vai_tro_khoa_dang_co`, `test_khong_go_duoc_cong_ty_chinh_422`, `test_go_cong_ty_go_luon_vai_tro_va_phan_cong`, `test_phan_cong_chi_ghi_dong_cua_C` (dòng công ty khác giữ nguyên), `test_lich_su_ghi_company_id_C`, `test_khong_quyen_403`.
- [x] Chạy ⇒ FAIL. Cài đặt. Chạy `tests/Feature/Rbac` ⇒ PASS toàn bộ.

### Task 3: API Màn 2 — quyền đang được cấp + phân quyền hàng loạt

**Files:**
- Modify: `EmployeeRoleController.php`, `EmployeeRoleService.php`, `hrm-api/Modules/Timesheet/Services/BulkPermissionService.php`, `hrm-api/routes/api.php`
- Test: `hrm-api/tests/Feature/Rbac/AdminEmployeeRoleBulkTest.php`

**Interfaces (Produces):**
- `GET /admin/employee-roles/{id}/effective-permissions` ⇒ `roles[{id, base_name, permissions[{code,name,subsystem,feature,kind,scope,duplicated_in[]}]}]` (chỉ vai trò của C) + `departments[{company_id, company_code, company_name, is_main, all_department, rows[{department_name, part_names[]}]}]` (mọi công ty làm việc, chỉ đọc).
- `POST /admin/employee-roles/bulk/preview|eligible|apply|export` — bọc các hàm hiện có của `BulkPermissionService`; công ty = `current_company_role` (thay claim JWT); chỉ chế độ cấp (`grant`) như UI đang có.

- [x] Viết test: `test_effective_permissions_danh_dau_trung` (2 vai trò cùng mã ⇒ `duplicated_in` chứa tên vai trò kia), `test_effective_departments_chia_chinh_kiem_nhiem`, `test_bulk_chi_nhan_vien_C`, `test_bulk_id_cong_ty_khac_422` (department/part/role/employee), `test_bulk_ghi_lich_su_moi_nguoi_company_id_C`.
- [x] Chạy ⇒ FAIL. Cài đặt (validate mọi id thuộc C trước khi apply). Chạy Rbac ⇒ PASS.

### Task 4: API Màn 1 — tài khoản + vá lỗ hổng

**Files:**
- Create: `hrm-api/app/Http/Controllers/Api/V1/Admin/AccountController.php`, `hrm-api/app/Http/Requests/Admin/AccountRequest.php`, `hrm-api/app/Http/Resources/Admin/AccountResource.php`
- Modify: `hrm-api/routes/api.php` (nhóm `admin/accounts`), `hrm-api/Modules/Human/Routes/api.php` (gắn middleware quyền cho POST/PUT/updateStatus/DELETE `human/employee`), `hrm-api/Modules/Human/Services/EmployeeService.php` (tách: tạo ghi `company_employees` công ty chính; sửa không `companies()->sync`), `ExportColumnRegistry.php` (key `admin_accounts`)
- Test: `hrm-api/tests/Feature/Rbac/AdminAccountApiTest.php`

**Interfaces (Produces):**
- Routes: `GET /admin/accounts` · `GET /export` · `GET /{id}` · `POST /` · `PUT /{id}` · `POST /{id}/lock` · `POST /{id}/unlock` · `GET /{id}/histories` (+ `filter-options` theo chuẩn `SystemInfoSection`).
- Danh sách trả thêm `created_by_name, created_at, updated_by_name, updated_at` (`d/m/Y H:i`), `status_text`, `status_color` (`#16A34A` Hoạt động / `#DC2626` Khoá). Phạm vi = `checkPermissionList(…, true)` như hiện tại, không nhận `is_all`.
- Lock/unlock ghi `employee_histories` (`change_status`), `updated_by = auth()->id()`.

- [x] Viết test: `test_danh_sach_theo_pham_vi_xem` (4 cấp + chỉ hồ sơ do mình tạo khi không có cấp nào), `test_is_all_khong_bo_qua_pham_vi`, `test_ngoai_pham_vi_404` (show/update/lock), `test_tao_tai_khoan_gan_cong_ty_chinh`, `test_sua_khong_dong_den_company_employees`, `test_khoa_mo_khoa_ghi_lich_su`, `test_doi_mat_khau_tang_token_version`, `test_route_cu_khong_quyen_403`, `test_khong_quyen_quan_ly_403_khi_ghi`.
- [x] Chạy ⇒ FAIL. Cài đặt. Chạy Rbac + test Human hiện có (`grep -rl "human/employee" Modules/*/Tests`) ⇒ PASS.

### Task 5: FE Màn 1 — `/admin/accounts`

**Files:**
- Create: `hrm-client/pages/admin/accounts/index.vue`, `add.vue`, `_id/index.vue`, `components/AccountForm.vue`, `components/AccountHistoryModal.vue`
- Modify: `hrm-client/components/subsystem-menu/admin.js` (mục "Quản lý tài khoản" → `/admin/accounts`), `hrm-client/pages/human/employee/*` (thành trang chuyển hướng giữ `/:id`), `hrm-client/components/human-components/human-slidebar.vue` (gỡ mục)

**Interfaces (Consumes):** API Task 4.

- [x] Danh sách theo `list-page` + mockup: bộ lọc 1 hàng (Công ty → Phòng ban → Bộ phận, Trạng thái; "Địa điểm nhận suất ăn" ẩn mặc định), 10 cột mặc định, cột ẩn theo design 3.3, hành động Sửa · Khoá/Mở khoá · ⋮ Lịch sử, Thêm mới · Xuất Excel · Tuỳ chỉnh cột, `filterStateMixin` `admin_accounts`.
- [x] Form 3 khối theo mockup (Thông tin tài khoản có ảnh trái · Mật khẩu với ô "Đổi mật khẩu" ở tiêu đề · Suất ăn & công nợ), ⓘ thay chú thích, `form-validate` + `unsavedChangesMixin`, lưu xong về danh sách; màn sửa có `SystemInfoSection` ngoài card.
- [x] Kiểm Playwright (rehearsal, namdangit + 1 tài khoản không quyền): số dòng = API total, 4 ô lọc cùng hàng cao 32px, cột khớp, tạo/sửa/khoá trên tài khoản thử `Zz…` rồi dọn, không quyền ⇒ 404 + API 403, footer không đè.

### Task 6: FE Màn 2 — danh sách, popup quyền, lịch sử, hàng loạt

**Files:**
- Create: `hrm-client/pages/admin/employee-roles/index.vue`, `components/GrantedPermissionsModal.vue`, `components/EmployeeRoleHistoryModal.vue`, chuyển `components/timesheet/setting/roles/BulkPermission*.vue` → `pages/admin/employee-roles/components/`
- Modify: `admin.js` (mục "Vai trò nhân viên" → `/admin/employee-roles`, gate "Quản lý phân quyền")

**Interfaces (Consumes):** API Task 2–3. `GrantedPermissionsModal.open(employeeId)`.

- [x] Danh sách theo mockup: cột Email sau Mã NV, chip vai trò (≤3 + "+n", bấm chip mở `RolePermissionsViewModal`), cột Loại, hành động Sửa · Quyền đang được cấp · ⋮ Lịch sử, nút "Phân quyền hàng loạt".
- [x] `GrantedPermissionsModal`: `V2BaseTabNavigation` mỗi vai trò 1 tab + tab "Phòng ban đang quản lý" (khối Công ty chính / Kiêm nhiệm), quyền `duplicated_in` tô đỏ + nhãn "Trùng: …".
- [x] Bulk: giữ nguyên giao diện, đổi endpoint sang `/admin/employee-roles/bulk/*`, nhãn công ty ở tiêu đề + ghi chú phạm vi, "Chọn quyền" → "Chọn vai trò", options chỉ của C.
- [x] Kiểm Playwright: tab đếm đúng, dòng trùng có màu `rgb(220, 38, 38)`, options bulk không có phòng ban/vai trò công ty khác, popup rộng như bản cũ.

### Task 7: FE Màn 2 — chi tiết 2 panel

**Files:**
- Create: `hrm-client/pages/admin/employee-roles/_id/index.vue`, `components/EmployeeRoleCompanies.vue`, `components/EmployeeRoleManageDepartments.vue`
- Consumes: `pages/admin/roles/components/RolePermissionsViewModal.vue` (GĐ2, không sửa), khuôn `rp-summary` của `pages/admin/roles/_id/permissions.vue`

- [x] Bố cục `col-lg-8` (Vai trò tại C có số quyền là link mở `RolePermissionsViewModal` · Phân công quản lý phòng ban tại C) / `col-lg-4` (Nhân viên + nút Quyền đang được cấp · Công ty làm việc · Tổng hợp quyền hiệu lực, cập nhật khi đổi tick); `SystemInfoSection` full ngang; `V2Footer` Lưu · Quay lại.
- [x] Công ty làm việc chỉ sửa được khi `is_main_company`; gỡ công ty ⇒ `$confirm` liệt kê vai trò sẽ mất; vai trò khoá 🔒.
- [x] Kiểm Playwright: tỷ lệ panel 2:1, cả màn công ty chính và kiêm nhiệm, lưu trên nhân viên thử rồi trả lại, bấm số quyền mở đúng tiêu đề vai trò.

### Task 8: Đóng màn cũ (hrm-client, hrm-api, ERP)

**Files:**
- hrm-client: `pages/timesheet/setting/employees/*` → trang chuyển hướng `/admin/employee-roles[/:id]` (bỏ code chết dòng 290); gỡ `components/timesheet/setting/roles/BulkPermission*` (đã chuyển ở Task 6).
- hrm-api: gỡ route `timesheet/employees/*`, `timesheet/roles/list`, `timesheet/bulk-permissions/*` sau khi `grep` hrm-client không còn gọi.
- ERP: `routes/web.php` gỡ `employeeIndex/create/store/edit/update/delete/doimatkhau` + view `common/employees/{index,create,edit}.blade.php`; `Route::redirect` (không closure) `employees` & `employees/{id}/edit` → HRM `/admin/accounts`; `sidebar.blade.php`, `topmenubar.blade.php`, `topmenubar_old.blade.php` trỏ HRM + thêm "Vai trò nhân viên"; `HomeController.php:916` link HRM. Giữ các route tra cứu `employees/*` còn nơi gọi.
- Catalog: đánh dấu ngừng dùng `admin.tai_khoan.manage` theo cơ chế catalog GĐ1; báo cáo chuyển đổi liệt kê người có quyền ERP mà không có "Quản lý tài khoản nhân viên".

- [x] Test ERP `test_route_tai_khoan_cu_chuyen_huong_cache_duoc` (`prepareForSerialization`), menu không còn `route('employeeIndex')`; hrm-api Rbac + ERP Rbac ⇒ PASS.

### Task 9: e2e + chốt hồ sơ

- [x] Viết `HRM/e2e/tests/admin/admin-accounts.spec.ts`, `admin-employee-roles.spec.ts` (serial, có quyền + không quyền, dọn dữ liệu `E2E Zz`), kiểm biên dịch `--list`; chạy khi user yêu cầu.
- [x] Final review (reviewer mới), sửa Critical/Important, cập nhật design §, STATUS, memory.

---

### Checkpoint — 27/10/2026 (wrap up)
Vừa hoàn thành: thiết kế + mockup vòng 3 được user duyệt; plan 9 task viết xong, user "ok" plan.
Đang làm dở: — (chưa đụng code; user CHƯA nói "làm" kèm phạm vi, chưa chọn cách chạy)
Bước tiếp theo: mở PHIÊN MỚI (phiên cũ hết ~70% context), user gõ "làm GĐ2b theo plan …, subagent-driven — phạm vi: 3 repo wt-rbac nhánh rbac, không commit; chạy migration 2026_11_02_000001_add_company_id_to_employee_permission_history vào hrm_erp_rbac_test; kiểm UI trên rehearsal dữ liệu thử Zz" → bắt đầu Task 1 (hỏi chạy migration với output `migrate --pretend`).
Blocked: chờ lệnh "làm".

### Checkpoint — 27/10/2026 (code xong, subagent-driven)
Vừa hoàn thành: Task 1–9 + final review + 1 đợt sửa cuối (sạch). Không commit. Migration 2026_11_02_000001 chạy vào hrm_erp_rbac_test và hrm_erp_rbac_rehearsal (user cho phép thêm rehearsal). Review Focus 4 đổi: route ghi cũ `human/employee` đã GỠ hẳn (test `test_route_ghi_cu_da_go`), không còn gắn quyền. Báo cáo từng task + sổ cái rulings: `bao-cao-code/`.
Đang làm dở: —
Bước tiếp theo: user quyết 3 việc tồn (xem STATUS); chạy e2e `tests/admin/admin-accounts.spec.ts`, `admin-employee-roles.spec.ts` khi user yêu cầu; commit/push khi user cho phép.
Blocked: —

### Checkpoint — 27/10/2026 (đóng việc tồn GĐ2b)
Vừa hoàn thành:
- Gỡ ERP `employee.searchData` + popup chọn NV phiếu thu/chi khác (code chết: dropdown tạo không có loại 3/10, rehearsal 0 phiếu); test Rbac ERP 25/25 + Playwright form tạo/sửa phiếu.
- Bỏ `admin.tai_khoan.manage` khỏi catalog hrm-api, 3 tên cũ sang `dropped_legacy.php`; test Rbac hrm-api 238/238; dry-run catalog-sync: ngừng dùng 1 + 846 chỉ lệch sort_order.
- User chốt 1A·2A·3A: runbook `gd1-nen-du-lieu/runbook-go-live.md` mục B.4b (kiểm công ty chính · dọn employee_has_roles mồ côi · báo cáo mất quyền quản lý tài khoản — SQL mới, rehearsal 0 người).
- e2e 2 spec trên rehearsal (3011/8011): **22/22 passed** (quản lý = namdangit, chỉ xem = NV 24, không quyền = NV 663). Sửa spec/fixture: insertProfile thiếu 8 cột NOT NULL schema prod; "Phòng ban" nằm trong khối nâng cao đóng sẵn; chờ popup quyền hết "Đang tải"; helper search lọc theo từ khoá; bấm ô trước fill() (unsavedChangesMixin cần pointerdown/keydown). Dữ liệu thử dọn sạch.
- Chạy e2e cho worktree: runMysql đọc DB từ `.env` của API_REPO (hrm_erp_rbac_test) ≠ API 8011 (rehearsal) ⇒ dùng wrapper `mysql` ở PATH đổi tên DB; thêm `--no-deps` (không chạy api.setup).
Đang làm dở: — (đã commit nhánh rbac, CHƯA push: ERP `7433afc657`, hrm-api `af85813b1`; e2e ngoài git)
Bước tiếp theo: push 2 commit khi user cho phép; GĐ3 (kiểm quyền theo mã) — brainstorm/design trước, chờ user. KHÔNG merge gop_db.
Blocked: —
