# GĐ3b — Đổi kiểm theo tên Vai trò sang mã quyền · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 169 chỗ kiểm `isRole('<tên Vai trò>')` / so tên Vai trò (ERP 161, hrm-api 6, hrm-client 2) đổi sang 17 mã quyền mới; lúc go-live cấp các mã đó vào đúng các Vai trò đang mang tên tương ứng để người được phép giữ nguyên (trừ các chỗ nguyên tắc chung buộc đổi, design 4.4).

**Architecture:** Một bảng ánh xạ duy nhất `RoleNameCodeMap` (hrm-api) khai "mã → [phạm vi ⇐ tên Vai trò]". Lệnh `rbac:grant-role-name-codes` đọc bảng đó để cấp `role_has_permissions` sau `rbac:convert` và để đối chiếu cũ/mới. Code ERP/HRM/FE thay điều kiện bằng `can()` / `permissionScope()` / `CurrentPermission` / `hasCode` theo luật quy đổi design 4.2.

**Tech Stack:** hrm-api Laravel 8 (PHP 7.4 `/opt/homebrew/opt/php@7.4/bin/php`), ERP TanPhatDev Laravel 6 + Blade/AngularJS, hrm-client Nuxt 2 (node 12, heap 8192).

**Spec:** `./design.md` (cùng thư mục). Nguồn từng chỗ: `../gd3-kiem-quyen-theo-ma/has-role-chua-co-ma.csv` (lọc `xu_ly = chua_co_ma`, số thứ tự trong design 4.1 là thứ tự sau khi lọc).

## Global Constraints

- Repo/nhánh: `websites/wt-rbac/{hrm-api,TanPhatDev,hrm-client}` nhánh `rbac`. Không push. Commit chỉ khi user cho phép (CLAUDE.md).
- **Mỗi task đụng source phải được user cho phép riêng** (repo · nhánh · file · DB). Plan duyệt ≠ lệnh code.
- DB: test `hrm_erp_rbac_test`, đối chiếu `hrm_erp_rbac_rehearsal`. Không chạy 2 bộ phpunit song song (cùng DB ⇒ lock wait).
- Lệnh test hrm-api: `DB_DATABASE=hrm_erp_rbac_test DB_DATABASE_SECOND=hrm_erp_rbac_test DB_DATABASE_TPE=hrm_erp_rbac_test php vendor/bin/phpunit tests/Feature/Rbac`. ERP: `DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test php -d variables_order=EGPCS vendor/bin/phpunit tests/Feature/Rbac`.
- Phạm vi: `PermissionScope::PART=1, DEPARTMENT=2, COMPANY=3, GROUP=4`. Chỗ kiểm một bậc luôn `>=` bậc đó, KHÔNG `==` (Q5).
- Công ty kiểm: ERP dùng mặc định của `can()` / `permissionScope()` (= công ty đang chọn trong session qua `EmployeeInfo::getCompanyIdAttribute`); hrm-api dùng `current_company_role` (Q4). Không truyền công ty khác.
- Nhánh không đạt **fail-closed**: không có mã ⇒ chỉ của mình / không có gì; cấm rơi vào truy vấn không lọc.
- Blade ERP: tính biến PHP trước rồi `@json($bien)`; không đặt biểu thức `||` / gọi hàm dài trong `@json(...)` (memory erp-blade-json-directive-gotcha).
- Không đổi dòng CSV `giu_khong_phai_kiem_quyen` / `bo_dac_quyen`. Không đổi logic bên trong nhánh, chỉ đổi điều kiện.
- Tên mã, kiểu, phạm vi, nền tảng: đúng bảng design 4.1 (F1–F15b).
- Kiểm code tới tận gốc trước khi kết luận (CLAUDE.md gốc): mỗi chỗ đổi phải đọc biến/hàm được dùng tới nơi nó được đọc.

## Review Focus

1. **Vai trò khoá (`roles.status = 0`) hoặc đổi tên sau khi cấp** — lệnh cấp vẫn cấp cho Vai trò khoá (mở khoá thì có quyền lại, PermissionChecker tự bỏ qua Vai trò khoá); đổi tên Vai trò sau khi cấp vẫn giữ quyền. Test ở Task 2.
2. **Tên Vai trò khác hoa/thường** ("Ban giám đốc" / "Ban Giám đốc" cùng có trong code) — bảng ánh xạ so không phân biệt hoa thường, giống collation MySQL đang làm cho `hasRole`. Test ở Task 2.
3. **Người không có mã rơi vào truy vấn không lọc** (vd `ServiceQuotation::searchByFilter` `type=department`) — mọi nhánh mới fail-closed. Test ở Task 8 + rà ở mọi task ERP.
4. **Công ty bị tắt `allow_group_scope`** — phạm vi 4 của TGĐ tính như 3; F4–F6 (chỉ phạm vi 4) ⇒ như người không có mã. Test ở Task 6 và Task 7.
5. **Code mới lên mà chưa chạy lệnh cấp** — mọi đặc quyền mất. Runbook phải có bước cấp + cổng kiểm số dòng; lệnh báo lỗi (exit 1) nếu mã chưa có trong `permissions`. Test ở Task 2, tài liệu ở Task 12.

---

### Task 1: Catalog — 17 mã mới + phạm vi Công ty cho 4 mã chỉ-Tổng-công-ty; bảng ánh xạ

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Catalog/{human,sale,warehouse,purchase,customer_care,training}.php`
- Modify: `hrm-api/app/Support/Permissions/Catalog/{meeting,sale,customer_care}.php` (4 mã thêm phạm vi 3)
- Create: `hrm-api/app/Support/Permissions/RoleNameCodeMap.php`
- Test: `hrm-api/tests/Feature/Rbac/RoleNameCodeMapTest.php`

**Interfaces:**
- Produces: `RoleNameCodeMap::all(): array` — mỗi phần tử `['code' => string, 'grants' => [['roles' => string[], 'scope' => ?int], ...]]`; `scope = null` cho mã cờ (kind approve/action). Đúng bảng design 4.3 (đã sửa theo Q6: F15a ⇐ Quản lý + Quản lý đào tạo + Trưởng phòng; F15b ⇐ Quản lý + Trưởng phòng). Trưởng phòng KHÔNG có trong bất kỳ `roles` nào ngoài F15a/F15b (Q1: không cấp — F15 giữ vì code cũ của Dashboard có liệt kê, 0 người).
- Produces: `RoleNameCodeMap::codes(): string[]`.

- [x] **Step 1: Test** — `test_moi_ma_trong_map_co_trong_catalog_va_dung_kind_scope`: mọi `code` có trong `PermissionCatalog::load()`, `scope` của grant nằm trong `scopes` của mã (null ⇔ mã không có scopes); `test_map_dung_17_ma` (đếm = 17, khớp danh sách F1–F15b); `test_4_ma_chi_tong_cong_ty_nay_co_pham_vi_3` (4 mã design mục 2 có `3` trong `scopes`); `test_khong_cap_truong_phong_ngoai_dashboard`.
- [x] **Step 2: Chạy, xác nhận đỏ** (class chưa có).
- [x] **Step 3: Khai 17 mục Catalog** (kind/scopes/platforms theo design 4.1; mã cờ dùng kind `approve` hoặc `action` để không mang scopes; `depends_on` = mã Xem của màn nếu có; `legacy = []`) + thêm `3` vào `scopes` 4 mã; viết `RoleNameCodeMap`.
- [x] **Step 4: Rà code đọc 4 mã** (`grep -rn` cả 3 repo) — nhánh `permissionScope >= COMPANY` có xử lý đúng chưa; chưa có thì thêm nhánh lọc công ty đang làm (cùng task). Ghi file:dòng vào checkpoint.
- [x] **Step 5: Chạy** `RoleNameCodeMapTest` + `CatalogContentTest` + `PermissionCatalogTest` + `php artisan permission:catalog-sync --dry-run` (chỉ thêm 17 mã + đổi scopes 4 mã). Xanh.
- [ ] **Step 6: Commit** (khi user cho phép) — CHƯA commit.

### Task 1b: Chỗ đọc 4 mã chỉ-Tổng-công-ty phải có nhánh phạm vi Công ty (CHẶN go-live — phát hiện ở Task 1)

Mọi chỗ đọc 4 mã so `>= GROUP`, nhánh còn lại = "chỉ của mình". `PermissionChecker` (cả 2 repo) hạ 4 ⇒ 3 ở công ty tắt `allow_group_scope` ⇒ sau khi tắt 6 công ty (Q7), người ở đó tụt xuống "chỉ của mình" thay vì "cả công ty".

**Files (implementer Task 1 liệt kê, controller kiểm lại 3 chỗ hrm-api + 4 controller ERP):**
- hrm-api: `Modules/Meeting/Services/MeetingRoomBookingService.php:204,228`, `Modules/Finance/Services/PrepickTracking/PrepickTrackingScope.php:23`
- hrm-client: `pages/meeting/bookings/index.vue:599`, `pages/sale/prepick-tracking/index.vue:500`
- ERP: `app/Http/Controllers/Sale/DeviceErrorController.php:55`, `app/Http/Controllers/Customercare/{CustomerCareBill,BillAssign,CustomerCareQuestion}Controller.php`, `app/Model/…/BillAssign.php:94`, `DeviceErrorHasGroup.php:17`, `AssemblyRequest.php:156,247`, `WrServiceContract.php:912`

**Interfaces:** `>= GROUP` ⇒ mọi công ty (giữ); thêm `>= COMPANY` ⇒ lọc công ty đang làm; còn lại giữ nhánh cũ. Chỗ chặn cả trang (`return view('not_found')` khi `< GROUP`) đổi thành `< COMPANY`.

- [x] Test có/không quyền mỗi repo (phạm vi 4, 3, không mã; công ty tắt `allow_group_scope` + phạm vi 4 ⇒ lọc công ty). Playwright 2 màn hrm-client. Cần user cho phép riêng (3 repo).

### Task 2: Lệnh `rbac:grant-role-name-codes` (cấp + đối chiếu)

**Files:**
- Create: `hrm-api/app/Console/Commands/RbacGrantRoleNameCodesCommand.php`
- Test: `hrm-api/tests/Feature/Rbac/RbacGrantRoleNameCodesTest.php`

**Interfaces:**
- Consumes: `RoleNameCodeMap::all()`, `RoleManagementService::log(int $roleId, string $action, array $old, array $new)`, `RoleManagementService::afterWrite()`.
- Produces: `php artisan rbac:grant-role-name-codes {--dry-run} {--report-dir=} {--verify}`.
  - Chọn Vai trò: `LOWER(COALESCE(NULLIF(base_name,''), name)) = LOWER(tên)` trong `roles`, **mọi công ty, mọi status**.
  - Ghi `role_has_permissions (role_id, permission_id, scope)`: chưa có ⇒ insert; có với scope thấp hơn ⇒ nâng; bằng/cao hơn ⇒ bỏ qua. Không bao giờ hạ, không xoá. Ghi `role_permission_history` qua `log()` (action theo khuôn hiện có của màn Phân quyền), `changed_by = null`.
  - Mã chưa có trong `permissions.code` ⇒ in lỗi, exit 1, không ghi gì.
  - Báo cáo `<report-dir>/cap-ma-vai-tro.csv`: `role_id,company_code,role_name,code,scope,so_nguoi_giu,hanh_dong(insert|raise|skip)`.
  - `--verify` (chỉ đọc): `<report-dir>/doi-chieu-vai-tro-ma.csv` các dòng lệch `code,muc_scope,employee_id,company_id,cu,moi` — "cũ" = có Vai trò tên trong grant ở công ty đó (Vai trò status 1), "mới" = `PermissionChecker::for(emp, company)->scope(code) >= muc_scope` (mã cờ: `->has(code)`); in tổng số dòng lệch, exit 0.

- [x] **Step 1: Test** — `test_dry_run_khong_ghi`, `test_cap_dung_vai_tro_moi_cong_ty_va_bao_cao`, `test_chay_lai_khong_nhan_ban` (lần 2 toàn `skip`), `test_khong_ha_scope_cao_hon_san_co`, `test_cap_ca_vai_tro_khoa`, `test_ten_khac_hoa_thuong_van_khop` (Ban Giám đốc), `test_doi_ten_vai_tro_sau_khi_cap_van_giu_quyen`, `test_ma_chua_sync_exit_1_khong_ghi`, `test_ghi_lich_su_role_permission_history`, `test_verify_khop_sau_khi_cap_0_dong_lech`.
- [x] **Step 2: Chạy, đỏ.**
- [x] **Step 3: Viết command** theo Interfaces; `afterWrite()` sau khi ghi.
- [x] **Step 4: Chạy test + toàn `tests/Feature/Rbac` hrm-api. Xanh.**
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 3: hrm-api — duyệt vượt hạn mức HĐ dự án TKT + phạm vi xoá liên hệ KH (F10, F12)

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ContractService.php:1120-1139`
- Modify: `hrm-api/Modules/Assign/Services/CustomerService.php:2504-2562`
- Modify (nếu hết chỗ dùng): `hrm-api/app/Support/Permissions/PermissionLookup.php` (`employeeHasRoleBaseName`, `roleBaseNamesOf`) + `tests/Feature/Rbac/HrmPermissionLookupTest.php`
- Test: `hrm-api/tests/Feature/Rbac/RoleNameCodesHrmTest.php`

**Interfaces:**
- Consumes: `CurrentPermission::has(string $code): bool`, `CurrentPermission::scope(string $code): ?int` (công ty = `current_company_role`).
- 1139: `currentEmployeeHasRole('Giám đốc')` ⇒ `CurrentPermission::has('sale.hop_dong_vuot_han_muc.approve')`.
- 2504: đọc kỹ `$erpEmployeeId` là ai (người đăng nhập hay người khác) **trước khi đổi**; tầng GĐ ⇒ `scope('sale.khach_hang_pham_vi.view') >= 3`, TP ⇒ `>= 2`, còn lại giữ nhánh "liên hệ có báo giá mình tạo". Nếu `$erpEmployeeId` không phải người đăng nhập thì dùng `PermissionChecker::for($erpEmployeeId, current_company_role)`.

- [x] **Step 1: Test** — mỗi chỗ: có mã ở công ty đang làm ⇒ qua; có mã ở công ty KHÁC ⇒ không qua (Q4); không mã ⇒ nhánh cũ "của mình"; phạm vi 2 ⇒ nhánh phòng.
- [x] **Step 2: Chạy, đỏ.**
- [x] **Step 3: Đổi điều kiện; gỡ helper nếu không còn chỗ gọi (`grep -rn` cả `app/` `Modules/`).**
- [x] **Step 4: Đếm trên rehearsal số người hết qua do Q4** (giữ Vai trò Giám đốc ở công ty ≠ `company_role`) — ghi vào design 4.4.
- [x] **Step 5: Chạy test + toàn Rbac hrm-api + test Assign liên quan (`Modules/Assign/Tests` grep `ContractService|CustomerService`). Xanh.**
- [ ] **Step 6: Commit** (khi user cho phép).

### Task 4: hrm-client — Dashboard Đào tạo (F15a, F15b)

**Files:**
- Modify: `hrm-client/pages/training/dashboard/index.vue:633-655`
- Test e2e: `HRM/e2e/tests/training/training-dashboard-blocks.spec.ts` (mới)

**Interfaces:**
- Consumes: `hasCode(this.$store.state.permissionCodes, code)` từ `@/utils/permissionCode`.
- 642 ⇒ `!hasCode(…, 'training.dashboard_khoi_quan_tri.view')`; 651 ⇒ `!hasCode(…, 'training.dashboard_khoi_quan_ly.view')`. Bỏ so `roles[].name`.

- [x] **Step 1: Tái hiện lỗi bằng Playwright** (CLAUDE.md): NV 138 (giữ "Quản lý đào tạo" TPE) trên rehearsal — đếm số khối quản lý trong DOM = 0 trước khi sửa.
- [x] **Step 2: Sửa computed.**
- [x] **Step 3: Playwright đo lại**: sau khi chạy lệnh cấp trên rehearsal (Task 12) hoặc cấp tạm mã cho role 3 — NV 138 thấy khối 1, không thấy khối 2; 1 NV giữ "Quản lý" (EG) thấy cả 2; NV 663 thấy 0. Đếm phần tử, không nhìn ảnh.
- [x] **Step 4: Viết spec e2e** 3 ca trên (có quyền khối 1 / cả 2 / không quyền). Không tự chạy cả bộ (memory) — chạy spec này 1 lần `--workers=1`.
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 5: ERP — F1 cơ cấu tổ chức, F2 báo cáo kinh doanh, F3 trang chủ (bậc thang)

**Files (theo CSV, design 4.1):** `TanPhatDev/app/Http/Controllers/Common/{Departments,Parts,Team}Controller.php`, `app/Model/Common/{Department,Part,Team,EmployeeInfo}.php`, `resources/views/common/employee_infos/create.blade.php:34`, `resources/views/partials/components/department-filter.blade.php:27,35`, `app/Http/Controllers/ReportController.php` (6 chỗ), `resources/views/reports/{customer_care_frequency,marketAnalysisLocation,marketAnalysisProductGroup,multiFilterJs}.blade.php`, `app/Http/Controllers/HomeController.php:2555-2574`
- Test: `TanPhatDev/tests/Feature/Rbac/ErpRoleNameCodesTierTest.php`

**Interfaces:**
- Consumes: `Auth::user()->permissionScope(string $code): ?int`, `PermissionScope::{DEPARTMENT,COMPANY,GROUP}`.
- Mã: F1 `human.co_cau_to_chuc_pham_vi.view`, F2 `sale.bao_cao_kinh_doanh_pham_vi.view`, F3 `sale.trang_chu_so_lieu_pham_vi.view`. Mỗi file/hàm đọc `permissionScope` **một lần** vào biến rồi so.

- [x] **Step 1: Test** — với từng mã: phạm vi 4 ⇒ nhánh TGĐ; 3 ⇒ nhánh GĐ; 2 ⇒ nhánh TP; không mã ⇒ nhánh còn lại; `department-filter`: phạm vi 4 thấy cả ô Công ty + ô Phòng ban (Q5), 3 chỉ ô Phòng ban, không mã không thấy; công ty `allow_group_scope = 0` + phạm vi 4 ⇒ như 3. Test render view bằng `view(...)->render()` + đếm phần tử, hoặc gọi hàm model/controller trả query.
- [x] **Step 2: Chạy, đỏ.**
- [x] **Step 3: Đổi điều kiện theo design 4.2.**
- [x] **Step 4: Chạy test mới + toàn `tests/Feature/Rbac` ERP (golden phải xanh; lệch do truy vấn mới ⇒ cập nhật bộ lọc regex như GĐ2c, KHÔNG chụp lại golden). Chạy `php artisan view:cache` để bắt lỗi Blade biên dịch.**
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 6: ERP — F4 kho, F5 giữ hàng, F6 yêu cầu đặt hàng nội địa (chỉ phạm vi 4)

**Files:** `app/Http/Controllers/Warehouse/{WarehouseInfos,WarehouseReports}Controller.php`, `app/Model/Warehouse/{AccountingWarehouse,PrepickDetail,StockPosition,Warehouse}.php`, `app/{Product,ProductInfo,ProductTemplate}.php` (3 chỗ), `resources/views/warehouse/{accounting_warehouses,warehouses}/prepickIndex.blade.php`, `app/Http/Controllers/Order/InlandOrderRequestsController.php` (4 chỗ), `app/Http/Controllers/Sale/Firm/FirmContractController.php:1954`
- Test: `TanPhatDev/tests/Feature/Rbac/ErpRoleNameCodesAllCompanyTest.php`

**Interfaces:**
- `isRole('Tổng giám đốc')` ⇒ `permissionScope(mã) >= PermissionScope::GROUP`. Mã: F4 `warehouse.kho_moi_cong_ty.view`, F5 `warehouse.giu_hang_moi_cong_ty.view`, F6 `purchase.yeu_cau_dat_hang_noi_dia_moi_cong_ty.view`.
- `FirmContractController:1954`: đọc hàm — cùng chức năng F6 thì dùng F6; khác thì DỪNG, báo user trước khi tách mã (design mục 6).

- [x] **Step 1: Test** — phạm vi 4 ⇒ không lọc công ty; không mã ⇒ lọc công ty đang làm; công ty tắt `allow_group_scope` ⇒ lọc công ty (Review Focus 4).
- [x] **Step 2–4:** đỏ → đổi → xanh + toàn Rbac ERP + `view:cache`.
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 7: ERP — F7 chứng từ bán hàng theo phòng/công ty + vá fail-open

**Files:** `app/Contract.php:2106`, `app/Datatables/Sale/ContractDatatable.php:29`, `app/Datatables/Sale/Firm/{FirmContract,FirmQuotation,ZTFirmContract}Datatable.php`, `app/Datatables/Sale/ProjectQuotationDatatable.php:275`, `app/Http/Controllers/Sale/{ServiceContract,ServiceQuotation}Controller.php`, `app/Model/Sale/{ContractAnnex,ContractTermAnnex,ProjectContract,ServiceContract,ServiceContractAnnex,ServiceQuotation}.php`, `app/Quotation.php:878`, 4 view approve (`$scope.isManager`: `sale/{contract_addition_annexes,liquidation_contracts,liquidation_orders,service_contracts}/approve.blade.php`)
- Test: `TanPhatDev/tests/Feature/Rbac/ErpRoleNameCodesSaleDocTest.php`

**Interfaces:**
- Mã `sale.chung_tu_ban_hang_pham_vi.view`. TP-only ⇒ `>= DEPARTMENT`; GĐ ⇒ `>= COMPANY`.
- `ServiceQuotation::searchByFilter` `type=department`: không đạt `>= DEPARTMENT` ⇒ `where('created_by', mình)` (fail-closed). Rà mọi Datatable/Model trong danh sách trên có nhánh "không đạt ⇒ không lọc" và vá cùng kiểu; ghi file:dòng vào checkpoint.

- [x] **Step 1: Test** — `test_service_quotation_type_department_khong_ma_chi_thay_cua_minh` (seed 2 phiếu 2 công ty, NV không mã ⇒ chỉ phiếu mình tạo); phạm vi 2 ⇒ phiếu nhân viên phòng; phạm vi 3 (GĐ) ⇒ cũng qua nhánh phòng (Q5) và các nhánh GĐ; `ofDepartment` không mã ⇒ view `not_found`.
- [x] **Step 2–4:** đỏ → đổi → xanh + toàn Rbac ERP + `view:cache`.
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 8: ERP — F8 Ban giám đốc trên màn duyệt, F9 hỗ trợ hạch toán / quyết toán

**Files:** ~45 view theo CSV (design 4.1 dòng F8, F9: `contracts/{approve,valid_approve}`, `customercare/warranty_repair_contracts/accounting/*`, `insurance/**/approve` ×7, `partials/classes/sale/**`, `partials/contracts/validApprove`, `partials/sale/support_accounting/index`, `sale/**/{approve,valid_approve,show,edit}` …), `app/Services/Sale/{PrintSupportAccountingService,PrintWrSupportAccountingService,SettlementContractService}.php`, `app/Services/Sale/Firm/Contract/PrintSupportAccountingService.php`
- Test: `TanPhatDev/tests/Feature/Rbac/ErpRoleNameCodesBoardTest.php`

**Interfaces:**
- `isRole('Giám đốc') || isRole('Ban giám đốc'|'Ban Giám đốc')` ⇒ `Auth::user()->can('sale.ban_giam_doc_chung_tu.approve')` (F8) / `can('sale.ho_tro_hach_toan_ban_giam_doc.view')` (F9). Phủ định `!GĐ && !BGĐ` ⇒ `!can(...)`.
- `sale/rule_contracts/approve.blade.php:264-265` (`is_giamdoc`, `is_bgd`): cả 2 ⇒ F8 (đọc JS dùng 2 biến để chắc chắn nghĩa trước khi gộp).
- Blade: `@php $isBigBoss = Auth::user()->can('…'); @endphp` rồi `@json($isBigBoss)`.

- [x] **Step 1: Test** — có mã ⇒ biến `isBigBoss` render `true` / khối BGĐ có; không mã ⇒ `false` / khối không có; lấy mẫu ≥ 1 view mỗi thư mục (contracts, insurance, sale/firm, sale/liquidation_*, settlement) + 3 service in.
- [x] **Step 2–4:** đỏ → đổi → xanh + toàn Rbac ERP + `view:cache` (bắt buộc — sửa nhiều Blade nhất).
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 9: ERP — F10, F11, F12, F13a/b, F14

**Files:** `app/Services/Sale/ContractService.php:21`, `app/Services/Sale/Firm/Contract/{FirmContractService.php:1492,ZTFirmContractService.php:1141}`, `partials/classes/sale/ContractValidApprove.blade.php:117` (đọc: F8 hay F10), `app/Model/Sale/ProjectQuotation.php:1965-1992`, `app/Http/Controllers/CustomerManagerController.php:97-98`, `app/Model/Sale/Customer.php:509-511`, `app/Model/Customers/{WarrantyRequest,WarrantyReport,WarrantyWork,WarrantyPaymentRequest}.php`, `resources/views/customercare/{warranty_requests,warranty_reports,warranty_works,warranty_payment_requests}/show.blade.php`, `app/Helpers/NotificationHelper.php`
- Test: `TanPhatDev/tests/Feature/Rbac/ErpRoleNameCodesMiscTest.php`

**Interfaces:**
- F10 `sale.hop_dong_vuot_han_muc.approve` (cờ); F11 `sale.bao_gia_du_an_ban_giam_doc.approve` thay **vế Vai trò** (giữ vế mã cũ: `can(mã cũ) || can(F11)`); F12 `sale.khach_hang_pham_vi.view` (3/2); F13a `customer_care.phieu_bao_hanh_pham_vi.view` (`>= COMPANY`); F13b `customer_care.phieu_bao_hanh_xu_ly.approve`; F14 `customer_care.de_nghi_thanh_toan_bao_hanh_ke_toan.approve`.
- Thông báo F14: thêm `NotificationHelper::sendNotifyWithCode(string $code, string $url, string $content, int $companyId)` — người nhận = `PermissionChecker::holders($code, Employee::LEGACY_GUARD, $companyId)`; gọi với `company_id` của phiếu đề nghị. Đọc `holders()` tới tận truy vấn trước khi dùng (guard, phạm vi null).
- `Customer.php:509-511` và hrm-api `CustomerService:2504` (Task 3) cùng logic — đối chiếu 2 bên trước khi đóng task.

- [x] **Step 1: Test** — mỗi mã: có/không; F11 người chỉ có mã cũ vẫn qua; F14 thông báo tới đúng người giữ mã ở công ty phiếu, không tới người công ty khác.
- [x] **Step 2–4:** đỏ → đổi → xanh + toàn Rbac ERP + `view:cache`.
- [ ] **Step 5: Commit** (khi user cho phép).

### Task 10: Quét lại — không còn kiểm theo tên Vai trò

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Scan/CallSiteScanner.php:66` (`ROLE_RE` thêm `isRole`, `sendNotifyWithRole`, `roles.find(… .name)` FE)
- Test: `hrm-api/tests/Feature/Rbac/PermissionScanTest.php`
- Modify: `../gd3-kiem-quyen-theo-ma/has-role-chua-co-ma.csv` (cột `xu_ly` 169 dòng ⇒ `doi_sang_ma`, `ma_moi`)

- [x] **Step 1: Test** — fixture có `isRole('Giám đốc')` ⇒ scanner bắt.
- [x] **Step 2: Chạy `permission:scan` trên 3 repo** ⇒ chỉ còn dòng `giu_khong_phai_kiem_quyen`; ghi số vào checkpoint.
- [ ] **Step 3: Commit** (khi user cho phép).

### Task 11: Merge sang `gop_db` local (chỉ khi user ra lệnh riêng)

- [x] Merge `rbac` → `gop_db` local 3 repo như các đợt trước; chạy lại bộ Rbac 2 repo trên `gop_db`. Không push. (03/11 — xem checkpoint cuối)

### Task 12: Rehearsal + tài liệu go-live

**Files:** `../gd1-nen-du-lieu/cua-so-go-live-nhanh.md`, `../gd1-nen-du-lieu/runbook-go-live.md`, `./design.md` (4.4 số liệu thật)

- [x] **Step 1 (cần user cho phép chạy vào `hrm_erp_rbac_rehearsal`):** `permission:catalog-sync` ⇒ `rbac:grant-role-name-codes --dry-run --report-dir=…` ⇒ chạy thật ⇒ `--verify`. Kỳ vọng: dòng lệch chỉ thuộc các mục design 4.4 (Q4, Q5, Q7); khác ⇒ dừng, báo user.
- [x] **Step 2: Playwright ERP** (tài khoản Giám đốc + tài khoản thường, đo DOM) ≥ 1 màn mỗi F1–F14; hrm-client Dashboard (Task 4 Step 3).
- [x] **Step 3: Cửa sổ go-live:** thêm khối "cấp mã GĐ3b" ngay sau `rbac:convert` (lệnh dry-run → thật → cổng `--verify` số dòng lệch = số đã duyệt), trước bước tắt 6 công ty GĐ2c; thêm vào phần Lui. Ghi thời gian chạy trên rehearsal.
- [x] **Step 4: Cập nhật checkpoint, STATUS, memory `thiet-ke-lai-vai-tro-quyen.md`.**

---

### Checkpoint — 2026-11-01 (wrap up)
Vừa hoàn thành: Task 1 (subagent-driven, review sạch sau 1 vòng sửa) — hrm-api `wt-rbac` nhánh `rbac`, **CHƯA commit**: 7 file Catalog (17 mã mới + 4 mã thêm phạm vi 3), `app/Support/Permissions/RoleNameCodeMap.php` (mới), `tests/Feature/Rbac/RoleNameCodeMapTest.php` (mới, 6 ca), `tests/Feature/Rbac/CatalogContentTest.php` (miễn 9 mã mới không tên cũ; 4 mã cũ so chính xác mins ∪ {3}). Rbac hrm-api 422 OK. Ledger SDD: `wt-rbac/hrm-api/.superpowers/sdd/plan-gd3b-doi-vai-tro-sang-ma/progress.md` (rulings 1–4, minor hoãn).
Đang làm dở: —
Bước tiếp theo: xin user cho phép Task 1b (3 repo — CHẶN go-live: chỗ đọc 4 mã chỉ so `>= GROUP`, công ty tắt Tổng công ty ⇒ tụt về "chỉ của mình"/not_found) rồi Task 2 (`rbac:grant-role-name-codes`). Chạy tiếp bằng superpowers:subagent-driven-development, đọc ledger trước để không chạy lại Task 1.
Blocked: mỗi task cần user cho phép riêng (repo · nhánh · file · DB). Commit Task 1 chờ user.

### Checkpoint — 2026-11-01 (Task 1b)
Vừa hoàn thành: Task 1b (subagent-driven, review Approved, 0 Critical/Important) — 3 repo wt-rbac nhánh `rbac`, **CHƯA commit**. hrm-api: MeetingRoomBookingService (phạm vi 3 = luật cũ OR phòng thuộc công ty đang làm `current_company_role`), test mới `tests/Feature/Rbac/GroupOnlyCodesCompanyScopeTest.php` 7/7, Rbac 429 OK; PrepickTrackingScope không đổi (dưới 4 vốn ép công ty mình). ERP: 4 controller `not_found` khi `< COMPANY`; BillAssign phạm vi 3 lọc theo công ty người yêu cầu, type=all không đủ ⇒ `1 = 0`; DeviceErrorHasGroup dưới 4 ⇒ rỗng; AssemblyRequest + WrServiceContract nhánh `>= COMPANY`; golden customer_care 2 khoá `.all`; test `tests/Feature/Rbac/ErpGroupOnlyCodesCompanyScopeTest.php` 3/3, Rbac 116 (1 đỏ = golden Purchase ngày có sẵn). Client: `pages/meeting/bookings/index.vue` defaultOnlyMine `>= 3`; prepick giữ `>= 4` (ô chọn công ty bất kỳ). Playwright đo DOM: 4/3 ⇒ công tắc TẮT, không mã ⇒ BẬT. Thêm ca e2e A4b (meeting-room-booking.spec.ts, chưa chạy). Rulings 5–10 + minor hoãn ở ledger.
Đang làm dở: —
Bước tiếp theo: xin user cho phép Task 2 (`rbac:grant-role-name-codes`, hrm-api). Vấn đề ngoài luồng ghi nhận: (1) hrm-api PrepickTrackingScope lấy công ty hồ sơ (info->company_id, không accessor session) còn FE dùng company_role; (2) trang "Tất cả" CustomerCareBill/Question/DeviceError không lọc công ty (có sẵn).
Blocked: Task 2+ cần user cho phép riêng. Commit Task 1 + 1b chờ user.

### Checkpoint — 2026-11-01 (Task 2)
Vừa hoàn thành: Task 2 — `app/Console/Commands/RbacGrantRoleNameCodesCommand.php` + `tests/Feature/Rbac/RbacGrantRoleNameCodesTest.php` (11/11, Rbac hrm-api 440 OK), review Approved, **CHƯA commit**. Rulings 11–14 ở ledger (so tên phân biệt dấu — đo rehearsal không đổi người; verify theo `>=`; dòng lệch GĐ2c tách riêng ở dòng tổng; verify cũng exit 1 khi thiếu mã).
Đang làm dở: —
Bước tiếp theo: xin user cho phép Task 3 (hrm-api ContractService F10 + CustomerService F12). Task 12 phải đo: NV còn Vai trò ở công ty đã thôi làm (không còn company_employees) hiện lệch ở --verify.
Blocked: Task 3+ cần user cho phép riêng. Commit Task 1/1b/2 chờ user.

### Checkpoint — 2026-11-01 (Task 3)
Vừa hoàn thành: Task 3 — ContractService F10 (`CurrentPermission::has('sale.hop_dong_vuot_han_muc.approve')`), CustomerService F12 (`scope('sale.khach_hang_pham_vi.view')` >=3 xoá hết / >=2 nhánh phòng / còn lại của mình); gỡ `currentEmployeeHasRole`, `erpEmployeeRoleNames`, `PermissionLookup::{employeeHasRoleBaseName,roleBaseNamesOf}`; test `tests/Feature/Rbac/RoleNameCodesHrmTest.php` 7/7, Feature/Rbac 446 OK; review Approved, **CHƯA commit**. Q4: 1 NV (197) hết qua — ghi design 4.4.
Đang làm dở: — (Task 2 fix round 1 xong: guard ALLOWLIST + mkdir sau pre-check + test mã ngừng dùng; Feature/Rbac 447 OK).
Bước tiếp theo: xong fix Task 2 ⇒ xin phép Task 4 (hrm-client Dashboard Đào tạo). Vấn đề tồn: RawPermissionLookupGuardTest đỏ sẵn 10 dòng ở base (PermissionCode, CallSiteScanner, EmployeeRoleService ×3, GroupScopeCompanyService ×2, PermissionScan ×2) — chờ user quyết.
Blocked: Task 4+ cần user cho phép riêng. Commit chờ user.

### Checkpoint — 2026-11-01 (Task 4)
Vừa hoàn thành: Task 4 — `hrm-client/pages/training/dashboard/index.vue` kiểm `hasCode` F15a/F15b (code cũ so `roles[].name` trần ⇒ sau convert không ai khớp, khối ẩn với mọi người). Đo DOM (giả lập permission_codes, không ghi DB): trước NV138 0/0; sau NV138 6/0, NV1189 7/1, NV663 0/0. Spec mới `HRM/e2e/tests/training/training-dashboard-blocks.spec.ts` 3 passed. Review Approved, **CHƯA commit**.
Đang làm dở: — (Task G xong: 10 vi phạm guard có sẵn ⇒ ALLOWLIST 5 mục kèm lý do; Unit/Rbac + Feature/Rbac 447 xanh, chưa commit).
Bước tiếp theo: xong Task G ⇒ xin phép Task 5 (ERP F1–F3).
Blocked: Task 5+ cần user cho phép riêng. Commit chờ user.

### Checkpoint — 2026-11-01 (Task 5)
Vừa hoàn thành: Task 5 ERP F1–F3 — 36 chỗ CSV (F1 10, F2 20, F3 6) sang `permissionScope(mã) >=`; test `tests/Feature/Rbac/ErpRoleNameCodesTierTest.php` 8/8 (+ layout giả `tests/Feature/Rbac/fixtures/views/layouts/app.blade.php`); view:cache OK; Rbac ERP 124 (1 đỏ = golden Purchase ngày có sẵn); không đổi golden. Review Approved, **CHƯA commit**.
Đang làm dở: —
Bước tiếp theo: xin phép Task 6 (ERP F4–F6 kho/giữ hàng/YC đặt hàng nội địa). Go-live: catalog-sync PHẢI chạy trước khi bật code (ERP permissionScope mã chưa có ⇒ 500). Ngoài luồng ghi ở ledger: Team::searchByFilter cột teams.status; saleByYear GĐ lọc nhầm $quotations; $userIsBoss 6 job mail không đọc; ô lọc marketAnalysis nằm trong comment; tạo hồ sơ NV not_found đầu hàm; department-filter không được include.
Blocked: Task 6+ cần user cho phép riêng. Commit chờ user.

### Checkpoint — 2026-11-01 (Task 6)
Xong: Task 6 — 26 chỗ F4 (15) / F5 (7, gồm getPrepickDetails:368 đổi sang F5 — Ruling 18) / F6 (4); FirmContractController:1954 dòng chết đã xoá (user chọn). ErpRoleNameCodesAllCompanyTest 9/9; view:cache OK; Rbac ERP 133 / 1 fail có sẵn (golden Purchase ngày); FinanceScopeConversionTest vá danh sách quét mã fixture. Review Approved. Chưa commit.
Đang làm dở: —
Bước tiếp theo: xin phép Task 7 (ERP F7 chứng từ bán hàng theo phòng/công ty + sửa fail-open).

### Checkpoint — 2026-11-02 (Task 7)
Xong: Task 7 ERP F7 — 20 chỗ sang `sale.chung_tu_ban_hang_pham_vi.view` (TP ⇒ >= 2, GĐ ⇒ >= 3). Vá fail-open type=department (không đạt ⇒ created_by = mình): Contract:2106, FirmContractDatatable:369, ZTFirmContractDatatable:349, ProjectContract:533, ContractAnnex:268, ContractTermAnnex:143, ServiceContractAnnex:301, ServiceContract:750, ServiceQuotation:266, Quotation:878 (q.created_by); FirmQuotationDatatable:127 + ProjectQuotationDatatable:275 vốn đã rơi về của mình. ErpRoleNameCodesSaleDocTest 6/6; view:cache OK; Rbac ERP 139 / 1 fail có sẵn (Purchase golden ngày). SaleScopeConversionTest: INTENDED_T7 (12 ca department, lệch có chủ đích) + RESULT_ONLY thêm 2 ca nhiễu (permissionScope nạp info+địa chỉ sớm hơn). Review Approved. Chưa commit.
Đang làm dở: —
Bước tiếp theo: xin phép Task 8 (ERP F8 Ban giám đốc màn duyệt, F9 hỗ trợ hạch toán/quyết toán, ~45 view).

### Checkpoint — 2026-11-02 (Task 8)
Xong: Task 8 ERP F8/F9 — 57 chỗ/47 file (49 F8 `sale.ban_giam_doc_chung_tu.approve`, 8 F9 `sale.ho_tro_hach_toan_ban_giam_doc.view`: 3 service in + SettlementContractService:1130 + support_accounting/index ×2 + settlement_info ×2). rule_contracts/approve is_giamdoc/is_bgd chỉ khai báo, không đọc ⇒ cả 2 F8 dạng chuỗi "1"/"". ErpRoleNameCodesBoardTest đỏ 7/8 → xanh 8/8 (27 view render có/không mã; 4 service kiểm tĩnh); view:cache OK; Rbac ERP 147 / 1 fail có sẵn (Purchase golden ngày). Review Approved, 0 Critical/Important. Chưa commit.
Ghi chú: ContractService:21, FirmContractService:1492, ZTFirmContractService:1141 còn isRole('Giám đốc') = F10 (CSV 73/74/76) ⇒ Task 9.
Đang làm dở: —
Bước tiếp theo: xin phép Task 9 (F10–F14).

### Checkpoint — 2026-11-02 (Task 9)
Xong: Task 9 ERP F10–F14 — F10 ContractService:21/FirmContractService:1492/ZTFirmContractService:1141; F11 ProjectQuotation canApprove/canApproveValid (giữ approver + mã cũ `sale.bao_gia_du_an.approve`); F12 Customer.php + CustomerManagerController (scope >= 3 / >= 2, khớp hrm-api CustomerService:2504); F13a WarrantyRequest GĐ ⇒ scope >= 3; F13b 3 model + 3 view show CSKH; F14 WarrantyPaymentRequest + view + `NotificationHelper::sendNotifyWithCode` (holders mã ở company_id phiếu). ContractValidApprove:117 giữ F8 (Ruling 20, % phát triển thị trường). ErpRoleNameCodesMiscTest đỏ 11/11 → xanh 11; CustomerCareScopeConversionTest: dựng dòng 3 mã CSKH (không cấp) + RESULT_ONLY 3 ca chỉ mất câu isRole (Ruling 21, không chụp lại golden). view:cache OK; Rbac ERP 158 / 1 fail có sẵn (Purchase golden ngày). Review PASS, 0 Critical/Important. Chưa commit.
Đang làm dở: —
Bước tiếp theo: xin phép Task 10 (quét lại — không còn kiểm theo tên Vai trò, permission:scan 3 repo).

### Checkpoint — 2026-11-02 (Task 10)
Xong: Task 10 — CallSiteScanner ROLE_RE bắt thêm isRole( / sendNotifyWithRole( / FE roles.find|some(… .name) (định nghĩa function bị loại); PermissionScanTest 11/11; hrm-api Rbac 448 OK. permission:scan (DB hrm_erp_rbac_test) nhóm has_role: hrm-api 0, hrm-client 0, ERP 7 — cả 7 là dòng giu_khong_phai_kiem_quyen (Employee 761/963/1479/1503, CheckRole:19, topmenubar_old:1947). CSV has-role-chua-co-ma.csv: doi_sang_ma 168, xoa_dong_chet 1, giu 64, bo_dac_quyen 11. Nhóm legacy_or_unknown không đánh giá được trên DB test (permission_aliases rỗng, thiếu mã mới) ⇒ quét lại trên rehearsal sau catalog-sync ở Task 12. Chưa commit.
Đang làm dở: —
Bước tiếp theo: Task 11 (merge sang gop_db local) CHỈ khi user ra lệnh riêng; hoặc Task 12 (rehearsal: lệnh cấp mã + đối chiếu + runbook) — xin phép.

### Checkpoint — 2026-11-02 (Task 12)
Xong: rehearsal `hrm_erp_rbac_rehearsal` (sao lưu 4 bảng quyền trước ở scratchpad t12): catalog-sync thêm 17 / sửa 846 (sort_order + 4 mã [3,4]) / ngừng `admin.tai_khoan.manage`; grant 18 Vai trò · thêm 85 (0,67 s) đúng design 4.2; verify lệch thật 0 (20 dòng của 2 id mồ côi 21, 23); Q4 theo mã: chỉ NV 197. Quét lại: has_role chỉ còn 7 dòng giữ; legacy_or_unknown tồn GĐ3 không dính dòng GĐ3b. Playwright PASS 14 / FAIL 0 / SKIP 3 (F6 nhánh mail, F10 POST ghi DB, F11 không có báo giá chờ duyệt — tinker thay). Tài liệu: cua-so-go-live-nhanh.md (A3b, khối 5b, Lui), runbook-go-live.md (B.5b, D), design.md 4.4. Chưa commit (Task 1–10 cũng chưa).
Ngoài luồng (có sẵn, ghi để sửa trước merge prod): marketAnalysisLocation khối lọc trong comment; quotations/searchData 1054 q.payed_cost trên rehearsal; warranty_reports/searchData 500 NV không quyền (whereHas employees); saleByYear lọc nhầm $quotations; department-filter không ai include; legacy_or_unknown tồn GĐ3 (WarehouseReportsController:1323… tên không có bí danh).
Đang làm dở: —
Bước tiếp theo: GĐ3b xong phần code + rehearsal. Còn: commit (user báo), Task 11 merge gop_db (chỉ khi user ra lệnh), final review toàn nhánh.

### Checkpoint — 2026-11-02 (final review)
Final review toàn nhánh (chỉ đọc): Ready with fixes, 0 Critical. I1: bảng SHA cua-so-go-live-nhanh.md chưa gồm GĐ3b ⇒ đã thêm cảnh báo, cập nhật SHA sau khi commit + Task 11. I2 (user chọn vá): WarrantyRequest / WarrantyPaymentRequest searchByFilter type=all không mã ⇒ nay chỉ phiếu mình tạo (trước cả bảng mọi công ty); MiscTest 11/11; golden CSKH INTENDED_I2 (6 mức không đạt Công ty của warranty_payment_request.all, Ruling 23); Rbac ERP 158 / 1 fail có sẵn; view:cache OK. Minor M1–M9 trong final-review.md (ledger SDD). Chưa commit.
Bước tiếp theo: user commit GĐ3b (3 repo, bỏ hrm-client .nuxt-rbac/) ⇒ Task 11 merge gop_db khi user ra lệnh ⇒ cập nhật SHA tài liệu go-live + chạy lại A3b.

### Checkpoint — 2026-11-03 (commit + Task 11)
Vừa hoàn thành: vá 2 lỗi có sẵn (danh sách báo cáo bảo hành 500 khi không mã ⇒ mình tạo + việc được giao; saleByYear nhánh Công ty lọc hợp đồng); commit GĐ3b trên `rbac` (hrm-api 837696fb7 · client d663e7ac9 · ERP b4f666abe1); Task 11 pull origin + merge `rbac` → `gop_db` LOCAL 3 repo (7a466818b · e14f605c0 · c649fd90c7), gỡ 2 xung đột (Catalog/warehouse.php, BuyContract2 CHUC_VU_NGUOI_KY); SHA tài liệu go-live đã cập nhật.
Đang làm dở: —
Bước tiếp theo: chạy lại A3b trên rehearsal bằng code gop_db; push `gop_db` CHỈ khi user ra lệnh (hook chặn push rbac).
Blocked: DB test thiếu bảng inherited_price_factors (1 test hrm-api đỏ) — cần user cho chạy migration Kế thừa giá đợt 2 vào hrm_erp_rbac_test nếu muốn xanh hết.

### Checkpoint — 2026-11-03 (ảnh hưởng app mobile)
Vừa hoàn thành: đánh giá ảnh hưởng tới TPE_APP (`../app-mobile/danh-gia-anh-huong.md`) — app không cần sửa, server trả tên cũ;
kiểm app thật trên rehearsal (NV 36 không khối duyệt, NV 34 đủ 4 mục duyệt + danh sách 10 đơn) — mật khẩu tạm đã trả lại;
plan chuyển app sang `permission_codes` (`../app-mobile/plan-chuyen-sang-ma.md`, 3 câu hỏi tồn); gom danh sách ngoài luồng
(`../viec-ngoai-luong.md`, 15 mục, 2 đã sửa).
Đang làm dở: —
Bước tiếp theo: hỏi Q1–Q3 của plan app khi user muốn làm; A3b rehearsal bằng code gop_db; push gop_db chỉ khi user ra lệnh.
Blocked:

### Checkpoint — 2026-11-03 (wrap up)
Vừa hoàn thành: GĐ3b đã commit `rbac` (hrm-api `837696fb7` · client `d663e7ac9` · ERP `b4f666abe1`) + Task 11 merge gop_db LOCAL
(`7a466818b` · `e14f605c0` · `c649fd90c7`, chưa push); đánh giá + thử app mobile, plan app (Q1–Q3 chốt); `../viec-ngoai-luong.md`;
danh sách cấp lại quyền `../gd1-nen-du-lieu/danh-sach-cap-lai-quyen/danh-sach-cap-lai-quyen.xlsx`.
Đang làm dở: —
Bước tiếp theo: push gop_db khi user ra lệnh; A3b lại trên rehearsal (xin phép); code TPE_APP permission_codes (xin "làm").
Blocked:
