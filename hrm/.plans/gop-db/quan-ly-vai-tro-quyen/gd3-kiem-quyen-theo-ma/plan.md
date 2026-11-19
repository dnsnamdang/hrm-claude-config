# GĐ3 (gộp GĐ4) — Kiểm quyền theo mã + gộp phạm vi dữ liệu · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans. Steps dùng `- [x]`.

**Goal:** Mọi chỗ kiểm quyền ở ERP, hrm-api, hrm-client, TPE_APP gọi bằng **mã**; chuỗi `if/else` theo phạm vi ở đường đọc thay bằng `DataScope`; gọi sai thì local ném lỗi, prod chặn + ghi log; quy tắc vào CLAUDE.md.

**Architecture:** Thêm lớp nền dùng chung (bản giống hệt ở hrm-api + ERP như `PermissionChecker`): `PermissionCode` (kiểm mã hợp lệ, chặn/ghi log/ném lỗi), `DataScope` (áp phạm vi lên query và lên một bản ghi), lệnh `permission:scan`. Trong lúc chuyển, các cửa cũ (`isCurrentEmployeeHasPermission`, `->can`, middleware, `hasAPermission`) nhận **cả tên cũ lẫn mã**; mã đi đường chặt. Đổi từng phân hệ một (thí điểm: **warehouse**). Task cuối gỡ nhánh tên cũ khỏi mọi cửa ⇒ chỉ còn mã.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Laravel 6 / PHP 7.4 (ERP TanPhatDev), Nuxt 2.14 / Vue 2 (hrm-client), Flutter (TPE_APP), PHPUnit, Playwright MCP.

**Spec:** `gd3-kiem-quyen-theo-ma/design.md` (duyệt 27/10/2026, U1–U9); nền `../design.md`, `../gd1-nen-du-lieu/design.md`.

## Global Constraints

- Repo/nhánh: `wt-rbac/hrm-api`, `wt-rbac/hrm-client`, `wt-rbac/TanPhatDev` — nhánh `rbac`. TPE_APP: nhánh mới tách từ nhánh dev hiện tại của app (hỏi user tên nhánh trước Task 9). **Không commit** khi user chưa báo. Code chỉ bắt đầu khi user nói "làm" kèm phạm vi (repo · nhánh · file · DB).
- **KHÔNG merge `gop_db` vào `rbac` cho tới Task 13** (U5). Không đưa gì lên `gop_db`.
- PHP: `/opt/homebrew/opt/php@7.4/bin/php` (gọi là `$PHP`). Test hrm-api: `$PHP vendor/bin/phpunit tests/Feature/Rbac`. Test ERP: `$PHP -d variables_order=EGPCS vendor/bin/phpunit tests/Feature/Rbac`. DB PHPUnit: `hrm_erp_rbac_test`. Kiểm UI + so trước/sau: `hrm_erp_rbac_rehearsal` (API `php -S` cổng 8011, Nuxt 3011), chỉ đọc, dữ liệu thử tiền tố `Zz` dọn sau khi kiểm.
- File **giống hệt từng byte** ở 2 repo (kiểm bằng `cmp`): `app/Support/Permissions/PermissionChecker.php`, `PermissionScope.php`, `PermissionCode.php`, `DataScope.php`, `ScopeContext.php`. PHP 7.4: không `match`, enum, named args.
- Mã hợp lệ = khớp `^[a-z0-9_]+(\.[a-z0-9_]+){2,}$` **và** có dòng `permissions.code` với `deprecated_at IS NULL`.
- Phạm vi: `1 Bộ phận · 2 Phòng ban · 3 Công ty · 4 Tổng công ty` (`PermissionScope`).
- Chặn: **chỉ `APP_ENV` = `local` / `testing` mới ném** `UnknownPermissionCode`; mọi môi trường khác (kể cả ERP prod `TANPHATERP`) ⇒ trả không có quyền + log kênh `permission` (file `storage/logs/permission-*.log`, daily) — sửa 27/10 sau final review Phần A (ERP prod không phải `production`) (message `Mã quyền không tồn tại: <chuỗi>`). Không bao giờ 500 cho người dùng prod.
- Có mã Xem mới vào màn; có mã mà không phạm vi ⇒ chỉ `created_by = tôi`; báo cáo/dashboard tổng hợp không phạm vi ⇒ rỗng (U8). Ràng buộc ghi (ai sửa/xoá bản ghi nào) **không đụng**.
- `DataScope` giữ **đúng ngữ nghĩa hiện tại của từng màn** — phát hiện 27/10: hrm-api (`checkPermissionList`) lọc phòng/bộ phận theo **cột `department_id`/`part_id` của bản ghi ∈ phòng/bộ phận mình quản lý, OR `created_by = tôi`**; ERP lọc theo **`created_by` ∈ thành viên phòng/bộ phận** (`department_members`/`part_members`). Không ép 2 bên về một.
- Sau mọi đổi dữ liệu quyền trong test: `PermissionChecker::flush()` + xoá cache spatie.
- Test mỗi mã: có quyền / không quyền / khác công ty; đường đọc thêm từng mức phạm vi + "có mã không phạm vi chỉ thấy phiếu mình".

## Review Focus

1. Chuỗi rỗng / `null` / chuỗi có khoảng trắng đầu-cuối truyền vào cửa kiểm quyền ⇒ không có quyền, không 500 ở prod, ném lỗi ở local. → Task 1 test `test_chuoi_rong_va_null_khong_quyen`.
2. Middleware nhiều mã `a.b.c|x.y.z` trong đó một mã đã ngừng dùng ⇒ mã còn lại vẫn xét bình thường, mã ngừng dùng ghi log. → Task 2 test `test_middleware_mot_ma_ngung_dung`.
3. Người làm việc ở 2 công ty, đổi công ty đang làm việc giữa 2 request ⇒ `DataScope` dùng phạm vi của công ty mới (đệm checker theo `employee|company`). → Task 3 test `test_doi_cong_ty_doi_pham_vi`.
4. Người có mã ở phạm vi Phòng ban nhưng **không quản lý/không thuộc** phòng nào (danh sách phòng rỗng) ⇒ chỉ thấy phiếu mình (hrm-api) / rỗng trừ phiếu mình (ERP), không lọt `whereIn([])` thành toàn bảng. → Task 3 test `test_pham_vi_phong_danh_sach_rong`.
5. FE: `state.permissions` chưa tải xong (F5 trang sâu) mà menu/route kiểm mã ⇒ ẩn/chặn, không nháy hiện rồi ẩn sai, không redirect nhầm sang 403 sau khi đã tải. → Task 5 kiểm Playwright `F5 trang /warehouse/... đo menu sau khi profile về`.

---

## Phần A — Nền (làm trước phân hệ thí điểm)

### Task 1: `PermissionCode` — kiểm mã hợp lệ, chặn, ghi log (hrm-api + ERP)

**Files:**
- Create: `hrm-api/app/Support/Permissions/PermissionCode.php`, `hrm-api/app/Support/Permissions/UnknownPermissionCode.php` (extends `\RuntimeException`); chép nguyên byte sang `TanPhatDev/app/Support/Permissions/`
- Modify: `PermissionChecker.php` (2 repo): thêm `allows()`; `flush()` reset cả bộ mã hợp lệ
- Modify: `config/logging.php` (2 repo): kênh `permission` (daily)
- Test: `hrm-api/tests/Feature/Rbac/PermissionCodeTest.php`, `TanPhatDev/tests/Feature/Rbac/PermissionCodeTest.php`

**Interfaces (Produces):**
- `PermissionCode::isValid(string $code): bool` — đúng dạng + có trong `permissions` còn hiệu lực (tải 1 lần mỗi tiến trình).
- `PermissionCode::ensure($code): bool` — hợp lệ ⇒ true; không hợp lệ ⇒ local/test ném `UnknownPermissionCode`, prod ghi log `permission` (`code`, `employee_id`, `company_id`, `route`/`url`, file:dòng gọi đầu tiên ngoài `app/Support/Permissions`) rồi trả false.
- `PermissionChecker::allows(string $code, ?int $minScope = null): bool` — `has($code)` và (`$minScope` null hoặc `scope($code) >= $minScope`). **Không** tự gọi `ensure` (checker giữ thuần dữ liệu).

- [x] Viết test: `test_ma_hop_le` · `test_ma_ngung_dung_khong_hop_le` · `test_ten_tieng_viet_nem_loi_o_testing` · `test_prod_ghi_log_va_tra_false` (giả `app()->detectEnvironment(fn() => 'production')`, `Log::shouldReceive` kênh `permission`) · `test_chuoi_rong_va_null_khong_quyen` · `test_allows_min_scope` (scope 2: `allows(c,2)` true, `allows(c,3)` false, không có mã ⇒ false).
- [x] Chạy ⇒ FAIL. Viết 2 class + `allows()`. Chạy ⇒ PASS ở hrm-api; `cmp` 2 bản; chạy test ERP ⇒ PASS.

### Task 2: Cửa kiểm quyền BE nhận mã (hrm-api + ERP), chưa gỡ tên cũ

**Files:**
- Modify hrm-api: `app/Support/Permissions/CurrentPermission.php` (`has()` + mới `scope()`, `map()`), `app/Http/Middleware/CheckPermission.php`
- Modify ERP: `app/Employee.php` (`hasLegacyPermission` → tách nhánh mã; mới `permissionScope()`), `app/Http/Middleware/CheckPermission.php`
- Test: `hrm-api/tests/Feature/Rbac/CurrentPermissionCodeTest.php`, `TanPhatDev/tests/Feature/Rbac/EmployeeCodeCheckTest.php`

**Interfaces:**
- Consumes: Task 1.
- Produces:
  - Quy tắc chung cho mọi cửa (`isCurrentEmployeeHasPermission`, `CurrentPermission::has`, middleware `checkPermission:`, ERP `can`/`hasAnyPermission`/`hasPermissionTo`/`canInCompany`/`@can`): chuỗi **đúng dạng mã** ⇒ `PermissionCode::ensure` rồi `checker->has`; chuỗi khác ⇒ nhánh tên cũ `hasLegacy` như hiện nay (**tạm**, gỡ ở Task 12).
  - hrm-api `CurrentPermission::scope(string $code): ?int`, `CurrentPermission::map(): array` (`[code => ?int]`, = `checker->grants()`).
  - ERP `Employee::permissionScope(string $code, ?int $companyId = null): ?int`.

- [x] Viết test: `test_cua_nhan_ma` (middleware `checkPermission:t.doc.view` có mã ⇒ 200, không ⇒ 403) · `test_cua_van_nhan_ten_cu` · `test_middleware_mot_ma_ngung_dung` · `test_ma_sai_o_testing_nem_loi` · `test_khac_cong_ty_khong_quyen` · ERP: `test_can_nhan_ma`, `test_can_in_company_nhan_ma`.
- [x] FAIL → sửa → PASS cả 2 repo.

### Task 3: `DataScope` — áp phạm vi lên query và bản ghi (hrm-api + ERP)

**Files:**
- Create (giống hệt 2 repo): `app/Support/Permissions/DataScope.php`, `app/Support/Permissions/ScopeContext.php` (interface)
- Create hrm-api: `app/Support/Permissions/HrmScopeContext.php` (dùng `listManageDepartmentIds()`, `listManagePartIds()`, `current_company_role`)
- Create ERP: `app/Support/Permissions/ErpScopeContext.php` (dùng `department_members`, `part_members`, `info->company_id`)
- Test: `hrm-api/tests/Feature/Rbac/DataScopeTest.php`, `TanPhatDev/tests/Feature/Rbac/DataScopeTest.php`

**Interfaces:**
- Consumes: Task 1 (`PermissionCode::ensure`, `PermissionChecker::allows/scope/has`).
- Produces:
  - `interface ScopeContext { employeeId(): int; companyId(): int; checker(): PermissionChecker; departmentIds(): array; partIds(): array; departmentMemberIds(): array; partMemberIds(): array; }`
  - `DataScope::apply($query, string $code, array $cols, ScopeContext $ctx, bool $aggregate = false)` — `$cols` khoá: `company` (cột công ty), `owner` (cột người tạo, mặc định `created_by`), `department`, `part` (cột phòng/bộ phận của bản ghi), `mode` = `'record_unit'` (kiểu hrm-api: cột phòng/bộ phận bản ghi ∈ phòng/bộ phận mình quản lý **OR** owner = tôi) hoặc `'owner_members'` (kiểu ERP: owner ∈ thành viên phòng/bộ phận). Hành vi: không có mã ⇒ `whereRaw('1 = 0')`; có mã, scope null ⇒ owner = tôi (`$aggregate` ⇒ `1 = 0`); 4 ⇒ không lọc; 3 ⇒ `company = ctx->companyId()`; 2/1 theo `mode`. Danh sách rỗng ⇒ chỉ nhánh owner = tôi (không `whereIn([])` rỗng thành điều kiện bỏ qua).
  - `DataScope::allowsRecord(string $code, array $record, array $cols, ScopeContext $ctx): bool` — cùng luật cho một bản ghi (dùng cho Duyệt có phạm vi, xem chi tiết). `$record` = mảng cột → giá trị.
  - `DataScope::forCurrent(): ScopeContext` mỗi repo tự cài trong `HrmScopeContext::current()` / `ErpScopeContext::current()` (không nằm trong file giống hệt).
- [x] Viết test (fixture công ty 1/2, phòng D1 có bộ phận P1, nhân viên E quản lý D1 / thuộc D1, bản ghi của E, của người cùng phòng, của phòng khác, của công ty 2): mỗi mức 4/3/2/1/null × 2 `mode` ra đúng tập id; `test_pham_vi_phong_danh_sach_rong`; `test_doi_cong_ty_doi_pham_vi`; `test_aggregate_khong_pham_vi_rong`; `test_allows_record_khop_apply` (mọi bản ghi: `allowsRecord` ⇔ nằm trong `apply`).
- [x] FAIL → viết → PASS cả 2 repo; `cmp` 2 file chung.

### Task 4: `permission:scan` (hrm-api)

**Files:**
- Create: `hrm-api/app/Console/Commands/PermissionScan.php`, `hrm-api/app/Support/Permissions/Scan/CallSiteScanner.php`
- Test: `hrm-api/tests/Feature/Rbac/PermissionScanTest.php` (fixture thư mục trong `tests/fixtures/permission-scan/`)

**Interfaces (Produces):**
- `php artisan permission:scan {paths*} {--subsystem=} {--json}` — quét file `.php`, `.blade.php`, `.vue`, `.js`, `.dart`. Báo 4 nhóm (design 4.2): `legacy_or_unknown` (chuỗi literal truyền vào cửa kiểm quyền không phải mã hợp lệ), `scope_chain` (≥ 2 tên cũ cùng mã trong một hàm/khối), `has_role` (`hasRole(`/`@role(`/`'Super Admin'`), `seeder_without_code` (tên trong 2 `PermissionsTableSeeder` không có alias/mã). `--subsystem` lọc theo tiền tố mã (qua alias của tên cũ). Exit code 1 khi có dòng.
- Danh sách cửa quét: PHP `isCurrentEmployeeHasPermission`, `checkPermission:`, `checkPermissionList*`, `->can(`, `@can(`, `hasAnyPermission(`, `hasPermissionTo(`, `canInCompany(`, `holders(`, `holdersAnyCompany(`, `CurrentPermission::has(`; JS/Vue `hasAPermission(`, `hasMultiplePermission(`, `hasGroup(`, `isShow:`, `groups:`; Dart `.name ==`, `contains('`, `containsIgnoreCase(`.
- [x] Viết test trên fixture có đủ 4 nhóm + 1 file sạch ⇒ đúng số dòng từng nhóm, file sạch 0, exit code.
- [x] FAIL → viết → PASS. Chạy thật trên 3 repo, lưu mốc `gd3-kiem-quyen-theo-ma/scan-moc-0.json` (đếm theo phân hệ) để đo tiến độ.

### Task 5: Profile/JWT trả map mã → phạm vi + helper FE (hrm-api, ERP, hrm-client)

**Files:**
- Modify hrm-api: `app/Http/Controllers/Api/AuthNewController.php` (~dòng 406, 451 + `AuthController.php:149,225`): thêm khoá `permission_codes` = `CurrentPermission::map()` (giữ `permissions` cũ tới Task 12)
- Modify ERP: `app/Employee.php::getJWTCustomClaims` thêm `permission_codes` (map)
- Modify hrm-client: `store/state.js`, `store/actions.js:97,295` (`permissionCodes`), `utils/mixins/CheckPermission.js`, `components/Topbar.vue` (`showMenuChild`/`showMenuParent`), `middleware/checkPermission.js`, sidebar hub (`components/subsystems.js` nơi đọc `isShow`)
- Create hrm-client: `utils/permissionCode.js`
- Test: hrm-api `tests/Feature/Rbac/ProfilePermissionCodesTest.php`; FE kiểm Playwright

**Interfaces (Produces):**
- API: `permission_codes: { "<code>": <1..4|null> }`.
- `utils/permissionCode.js`: `isPermissionCode(s): boolean` (cùng regex), `hasCode(map, code): boolean` (dev: chuỗi không đúng dạng ⇒ `console.error('[permission] Mã quyền không hợp lệ: ' + s)`, trả false), `scopeOf(map, code): number|null`.
- Mixin: `hasAPermission(x)` — đúng dạng mã ⇒ `hasCode`; khác ⇒ nhánh tên cũ (tạm, gỡ Task 12). Mới: `permissionScope(code)`, `hasAnyPermission(codes[])`. Menu: thêm khoá `codes: [...]` (có 1 mã là hiện), thay dần `isShow: [tên]` / `groups:`.
- [x] Test API: map đúng mã + phạm vi, khác công ty ra map khác, không đăng nhập 401.
- [x] Kiểm Playwright trên rehearsal (tài khoản `namdangit`): mục menu khai `codes` hiện/ẩn đúng; Review Focus 5 (F5 trang sâu, đo menu sau khi profile về).

## Phần B — Gộp ~25 mã còn mang phạm vi trong tên (U9)

### Task 6: Bảng đối chiếu + sửa danh mục + chuyển đổi — ✅ XONG 27/10: rà xong, user chọn giữ tách cả 9 mã ⇒ không sửa Catalog/convert

**Files:**
- Create: `gd3-kiem-quyen-theo-ma/gop-ma-pham-vi.csv` (cột `ma_cu, ten, kind, ma_moi, pham_vi, so_vai_tro, ghi_chu`)
- Modify: `hrm-api/app/Support/Permissions/Catalog/*.php` (gộp vào mã có `scopes`, tên cũ chuyển thành `legacy` kèm `min_scope`; mã cũ để ngừng dùng)
- Modify: lệnh `rbac:convert` (`hrm-api/app/Support/Permissions/Convert/*`) — vai trò giữ nhiều biến thể nhận phạm vi cao nhất (như GĐ1)
- Test: `hrm-api/tests/Feature/Rbac/` (bổ sung ca chuyển đổi cho mã gộp)

- [ ] Liệt kê mã có `theo_phong_ban|theo_nhan_vien|theo_cong_ty|theo_bo_phan|theo_tong_cong_ty` trong mã hoặc tên (kỳ vọng ~25: 17 view, 5 action, 3 approve), điền CSV kèm số vai trò đang giữ (đọc rehearsal). **Dừng, gửi user duyệt CSV.**
- [ ] Sau khi duyệt: sửa Catalog + convert; test ca "vai trò giữ 2 biến thể ⇒ phạm vi cao nhất", "biến thể theo nhân viên ⇒ có mã, phạm vi null". PASS.
- [ ] Diễn tập lại `rbac:convert` + so quyền hiệu lực trước/sau trên bản sao prod theo runbook GĐ1 (hỏi user DB đích trước khi chạy). Chênh lệch = 0.

## Phần C — Thí điểm: phân hệ `warehouse`

Chọn `warehouse` [Claude chốt]: 58 mã, 20 có phạm vi, 12 mã chung 2 nền tảng, có màn ở cả ERP (80 tên cũ) và HRM (15 tên cũ).

### Task 7: Đổi phân hệ warehouse (khuôn cho mọi phân hệ)

**Files:** theo `php artisan permission:scan ../../ --subsystem=warehouse --json` (lưu `gd3-kiem-quyen-theo-ma/phan-he/warehouse.json`).

**Interfaces:** Consumes Task 1–5. Produces: ghi chú khuôn `gd3-kiem-quyen-theo-ma/khuon-phan-he.md` (cách đổi từng dạng gặp thực tế + `mode` đã dùng cho từng màn), dùng lại cho Task 8.

- [ ] **Chụp mốc trước**: trên rehearsal, với 4 tài khoản thử (phạm vi 4/3/2/1) + 1 tài khoản có mã không phạm vi + 1 không mã, gọi mọi API/route đọc của phân hệ (danh sách, chi tiết, báo cáo, export) ⇒ lưu `{route, tai_khoan, so_dong, ids_hash}` vào `phan-he/warehouse-truoc.json`. Script đặt ở `hrm-api/tests/Support/ScopeSnapshot.php` (dùng lại cho mọi phân hệ).
- [ ] Đổi gọi có/không sang mã (BE 2 repo, route middleware, FE + menu `codes`).
- [ ] Đổi chuỗi phạm vi đường đọc + Duyệt có phạm vi sang `DataScope::apply` / `allowsRecord`, chọn `mode` giữ đúng ngữ nghĩa cũ của màn. Không đụng ràng buộc ghi.
- [ ] Test BE mỗi mã: có quyền / không / khác công ty; đường đọc thêm mỗi mức + không phạm vi.
- [ ] **Chụp mốc sau** ⇒ so với trước: khác nhau chỉ được ở các dòng có lý do đã chốt (U8: tài khoản không phạm vi). Liệt kê chênh lệch cho user nếu có.
- [ ] Kiểm Playwright các màn warehouse (HRM 3011 + ERP) bằng các tài khoản trên: số dòng bảng khớp mốc, menu hiện/ẩn đúng.
- [ ] `permission:scan --subsystem=warehouse` ⇒ 0 ở cả 4 nhóm. Báo user, chờ duyệt khuôn trước khi sang Task 8.

## Phần D — Các phân hệ còn lại

### Task 8: Lặp khuôn Task 7 cho từng phân hệ

Mỗi phân hệ là **một task con** đi đủ các bước Task 7 (mốc trước → đổi → test → mốc sau → Playwright → scan 0). Thứ tự [Claude chốt] nhỏ → lớn, ERP-nặng xen HRM-nặng:

- [x] 8.1 `lookup` · [x] 8.2 `admin` (gồm gate các màn GĐ2/2b đang gác tên cũ) · [x] 8.3 `meeting` · [x] 8.4 `rice` · [x] 8.5 `timesheet` · [x] 8.6 `human` · [x] 8.7 `decision` · [x] 8.8 `presale` · [x] 8.9 `accounting` · [x] 8.10 `payroll` · [x] 8.11 `training` · [x] 8.12 `assign` · [x] 8.13 `customer_care` · [x] 8.14 `finance` · [x] 8.15 `purchase` · [x] 8.16 `sale` · [x] 8.17 `master_data`
- [x] 8.18 Super Admin + `hasRole` còn lại (design 4.3): chỗ không tìm được mã ⇒ liệt kê `gd3-kiem-quyen-theo-ma/has-role-chua-co-ma.csv`, **dừng hỏi user**.
- [ ] 8.19 Gỡ `checkPermissionList*` (hrm-api `app/Helper/PermissionHelper.php:244-470`) khi không còn chỗ gọi.

## Phần E — TPE_APP, chốt chặt, tài liệu, merge cuối

### Task 9: TPE_APP đọc mã

**Files:** `TPE_APP/app/lib/domain/lib/src/entity/employee_info.dart:20-45` (+ model `Permission`), `app/lib/ui/dashboard_nhan_vien/dashboard_nhan_vien_page.dart:177-294,456,466,763,765`, `bloc/dashboard_nhan_vien_state.dart:26-30`. Theo `TPE_APP/CLAUDE.md`.

- [ ] Hỏi user nhánh TPE_APP. Đổi entity đọc `permission_codes` (map); thay 5 so sánh tên + `containsIgnoreCase('giao công tác')` bằng danh sách mã tương ứng (tra Catalog qua alias, ghi bảng tên → mã vào đầu file plan khi làm).
- [ ] Kiểm trên máy ảo (Mobile MCP, flavor `tpeLocal`) với API rehearsal: menu Phê duyệt / Giao việc / Dashboard quản lý hiện đúng cho tài khoản có mã, ẩn cho tài khoản không mã.

### Task 10: CLAUDE.md + skill (bản nháp)

**Files:**
- Create: `gd3-kiem-quyen-theo-ma/nhap-claude-md.md` (đoạn thay mục **Permission** của `HRM/CLAUDE.md` + mục tương ứng `ERP/CLAUDE.md`), `gd3-kiem-quyen-theo-ma/nhap-skill-permission-catalog.md` (thay skill `permission-seeder`)
- [ ] Nội dung theo design 4.4: tạo quyền trong `Catalog/<phân_hệ>.php`, không seeder; kiểm chỉ bằng mã (BE/FE/middleware/menu `codes`); lọc theo phạm vi chỉ qua `DataScope`; cấm tên tiếng Việt và `hasRole`; lệnh tự kiểm `php artisan permission:scan <paths> --subsystem=<x>` phải 0. Grep `.claude/skills/` liệt kê skill đang ví dụ tên quyền ⇒ danh sách sửa kèm theo.
- [ ] Gửi user duyệt. Áp vào file thật chỉ ở Task 13 (cùng lúc merge).

### Task 11: Gỡ dùng `permission_aliases` khỏi code chạy (sau khi 8.x xong)

**Files:** `PermissionChecker.php` (2 repo: bỏ `hasLegacy`, `legacyNames`, `aliases()`, nhánh tên cũ của `resolve`), `CurrentPermission.php` (bỏ `names`, `listFor` dạng tên, `GUARD`), `PermissionHelper.php` (`getAllCurrentPermission`), ERP `Employee.php` (`hasLegacyPermission`, `legacyPermissionNames`, `HRM_ACCOUNT_SCREEN_PERMISSIONS` → mã), `holders()`/`holdersAnyCompany()` chỉ nhận mã.
- [ ] Đổi test GĐ1/2/2b đang gọi tên cũ sang mã. `rbac:convert` + `EffectiveSnapshot` vẫn đọc bảng alias trực tiếp (không qua checker).

### Task 12: Chốt chặt mọi cửa

**Files:** mọi cửa ở Task 2 + Task 5 (BE 2 repo, mixin FE, menu), API profile/JWT bỏ khoá `permissions` cũ (giữ `permission_codes`).
- [ ] Mọi cửa: chuỗi không phải mã hợp lệ ⇒ `PermissionCode::ensure` (local ném, prod log + chặn); FE ⇒ `console.error` + false. Gỡ `hasGroup`, `isShow: [tên]`, `groups:`.
- [ ] Test: `test_ten_cu_bi_chan_o_moi_cua` (mỗi cửa một ca) cả 2 repo. Toàn bộ `tests/Feature/Rbac` 2 repo PASS. `permission:scan` toàn 3 repo + TPE_APP ⇒ 0.

### Task 13: Merge `gop_db` → `rbac` một lần + dọn + diễn tập

- [ ] **Hỏi user** trước khi merge (nêu 3 repo, số commit `gop_db` mới). Merge, giải xung đột.
- [ ] `permission:scan` toàn bộ ⇒ đổi hết chỗ mới; quyền mới khai ở seeder cũ ⇒ thêm mã vào Catalog + alias để `rbac:convert` dịch dữ liệu. Lặp tới 0.
- [ ] Áp bản nháp Task 10 vào `HRM/CLAUDE.md`, `ERP/CLAUDE.md`, skill (theo cách user chọn: PR `hrm-claude-config`).
- [ ] Toàn bộ test Rbac 2 repo + e2e `admin-*` + diễn tập runbook GĐ1 trên bản sao prod (hỏi DB đích). Log kênh `permission` sau diễn tập = 0 dòng.
- [ ] Cập nhật `../gd1-nen-du-lieu/runbook-go-live.md`: phát hành TPE_APP cùng ngày; smoke test đổi `permissions[].name` → `permission_codes`.

---

### Checkpoint — 27/10/2026
Vừa hoàn thành: design GĐ3 (U1–U9) duyệt + plan này.
Đang làm dở: —
Bước tiếp theo: user duyệt plan + chọn cách chạy; hỏi "làm" cho Phần A (3 repo nhánh `rbac`, không migration).
Blocked: —

### Checkpoint — 27/10/2026 (Phần A xong)
Vừa hoàn thành: Phần A Task 1–5 (subagent-driven, mỗi task review + final review Phần A + 1 đợt sửa, re-review sạch). 3 repo `wt-rbac` nhánh `rbac`, CHƯA commit. hrm-api Rbac 289 OK, ERP Rbac 61 OK. Mốc quét `scan-moc-0.json`: legacy 6.688 (419 tên không có trong danh mục), scope_chain 933, has_role 13, local_override 8; warehouse: legacy 298, scope_chain 55, unattributed 217. Sổ cái + rulings: `wt-rbac/hrm-api/.superpowers/sdd/plan-gd3-kiem-quyen-theo-ma/progress.md`.
Đang làm dở: —
Bước tiếp theo: Phần B Task 6 (bảng đối chiếu ~25 mã gộp — dừng chờ user duyệt CSV); hỏi "làm" riêng.
Blocked: — · Cần user xem: 419 tên không có trong danh mục; JWT ERP ~145KB (claim mới +40KB); 8 override Modules đổi ở Task 8; thêm `queue:restart` sau catalog sync vào runbook.

### Checkpoint — 28/10/2026 (Phần B + C xong)
Vừa hoàn thành: Phần A commit (api 6a6389bbf, ERP 1a68ef6e7f, client dfd908b9e). Phần B: rà 27 mã, user giữ tách 9 mã ⇒ không đổi code. Phần C thí điểm warehouse (7a mốc trước · 7b đổi code 2 nhánh song song · 7c kiểm độc lập): 360/360 ô khớp mốc trước; Playwright HRM + ERP khớp; scan warehouse: legacy 8 (isShow menu hrm-client cố ý giữ), scope_chain 0, unattributed 217 (tên phân hệ khác/đã bỏ trong file dùng chung); Rbac api 299 OK, ERP 64 OK. CHƯA commit Phần C. Server ERP 8012 đã tắt.
Đang làm dở: —
Bước tiếp theo: user duyệt khuôn (`khuon-phan-he.md`, `phan-he/warehouse-so-sanh.md`) ⇒ Task 8 (17 phân hệ còn lại). Hỏi "làm" riêng.
Blocked: —

### Checkpoint — 28/10/2026 (Task 8: xong 8.1 → 8.13, tạm dừng theo yêu cầu user)
Vừa hoàn thành: 13 phân hệ đổi sang mã, mỗi phân hệ khớp mốc + review Approved (0 Critical/0 Important) rồi commit trên nhánh `rbac` (CHƯA push). Commit cuối: hrm-api `26d1bc1f5`, TanPhatDev `17158a8c7d`, hrm-client `8a487f1a8`. Danh sách commit từng phân hệ + minor hoãn: sổ cái `wt-rbac/hrm-api/.superpowers/sdd/plan-gd3-kiem-quyen-theo-ma/progress.md`.
Đang làm dở: 8.14 `finance` — agent đã dừng trước khi sửa code (cây 3 repo sạch; chỉ có `scan-finance-0.json`). Không có server 8012 còn chạy.
Bước tiếp theo: dispatch lại 8.14 finance từ base `snap-8.13c.txt` (brief chung `task-8-brief.md` + ghi chú cộng dồn; gồm xử lý test Finance đỏ sẵn), rồi 8.15 purchase, 8.16 sale (sửa `sale.js::toLeaf` mất `codes`), 8.17 master_data; dừng ở 8.18 (has_role CSV) hỏi user. Phạm vi cho phép vẫn là câu "3" của user (8.1→8.17, commit sau mỗi phân hệ khớp mốc).
Cần hỏi user cuối đợt — tên quyền lạ (đang luôn false): kho 3 tên; 'Bảng chấm công chi tiết'; 'Duyệt thông báo nội bộ'; 'Quản lý thân nhân'; 4 tên RewardMode/RewardTitle; loại HĐLĐ (3); hạng mục dự án; 'Quản lý tài khoản'; hoa hồng (2); khảo sát "theo theo công ty", 'Duyệt đề xuất đào tạo', vị trí "phòng ban  "; 'Duyệt quyết toán hợp đồng'; 'Duyệt PL giảm HDDV'.
Checklist deploy: đồng bộ Catalog trước khi lên (ERP topmenubar/partial Datatable/middleware kiểm thẳng mã accounting.*, customer_care.phieu.view…); `queue:restart`; JWT ERP ~145KB. API đổi giá trị `isShow` tên→mã: training dashboard getData, assign dashboard.
Blocked: —

### Checkpoint — 29/10/2026 (Task 8: xong 8.14 → 8.17, commit local CHƯA push, dừng ở 8.18)

Commit local nhánh `rbac` (chưa push, chưa merge gop_db):
- 8.14 finance: hrm-api dd62184a3 · ERP e62a1448fe · client db0899edf
- 8.15 purchase: ERP e612efd1ce
- 8.16 sale: hrm-api ad06197aa · ERP 330d923022 · client c2f15713d
- 8.17 master_data: hrm-api 91eabc900 · ERP 83f96d0c69 · client 1fedbf942 — mốc `snap-8.17c.txt`

Mỗi phân hệ đều khớp mốc HTTP trước/sau và đã qua review độc lập. Riêng 8.17 có 7 ô device_errors lệch, chỉ ở khoá debug `queries` của yajra. Rbac ERP full xanh: 103 test, 26 phút. Golden sale/purchase đã bỏ khoá thời gian khi tính băm `dong` vì test MasterData hrm-api làm trôi `companies#1`.
Bước tiếp theo: 8.18 Super Admin + has_role — chờ user quyết. Đã thấy CustomerService.php:2504-2512. Cuối đợt cần hỏi user: danh sách tên lạ bị ép false (sổ cái + task-8.14..8.17-report), ngoại lệ Super admin ở `costPricePermission.js` (Task 12), checklist deploy (đồng bộ Catalog finance/purchase/sale/master_data, `queue:restart`, socket còn đọc claim tên cũ trong JWT).

### Checkpoint — 29/10/2026 (ngoài luồng GĐ3: dựng lại UI màn Phân quyền theo mockup)
Vừa hoàn thành: user báo `/admin/roles/:id/permissions` lệch mockup `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html`, cho "làm". Kết quả:
- Dựng lại `hrm-client/pages/admin/roles/_id/permissions.vue` + `components/PermissionTree.vue` (wt-rbac, nhánh rbac): băng tiêu đề có ô Công ty + nút Danh sách; bộ lọc có nhãn + Xoá lọc; thẻ "Cây quyền"; mỗi phân hệ 1 thẻ xanh mang nhãn nhóm; bảng Loại · Tên quyền · Phạm vi.
- Quyền có phạm vi chọn bằng ô cấp, option "— Không xem/duyệt —" có giá trị `'0'`; quyền không phạm vi dùng ô tick.
- Tổng hợp theo chức năng, có nhãn cấp. Footer chỉ còn "Lưu phân quyền".
- Giữ phần design thêm so với mockup: mã quyền, ERP/HRM, lọc Nền tảng, "Chỉ hiện quyền đã chọn", đếm theo loại, số thay đổi chưa lưu.
- Đã kiểm bằng Playwright (Super admin id 18 + tài khoản không quyền id 24). Spec `HRM/e2e/tests/admin/admin-roles.spec.ts` đã cập nhật nhưng CHƯA chạy.
Đang làm dở: —. CHƯA commit (để nguyên theo luật; khi commit 8.18 phải add theo path, KHÔNG kéo 2 file này vào).
Bước tiếp theo: user xem lại màn; chạy e2e admin-roles khi user yêu cầu.


### Checkpoint — 30/10/2026 (wrap up)
Vừa hoàn thành:
- 8.18: bỏ đặc quyền Super admin / Admin Role ở 11 chỗ; CSV `has-role-chua-co-ma.csv` 244 dòng (169 chưa có mã). Commit local ERP `a51bdd3def`, client `68c18bbbc`.
- Màn Vai trò theo mockup + tối ưu, popup Quyền đang có / Người giữ, sửa đếm "Số người giữ". Commit local hrm-api `d9359428f`, client `449cbd4ec`.
- Thêm 3 bộ lọc màn Vai trò; thẻ vai trò gọn ở Vai trò nhân viên (CHƯA commit). E2E admin-roles 14/14, admin-employee-roles 16/16, Rbac hrm-api 394 OK.
- Video HDSD phần phân quyền (`../video/huong-dan-phan-quyen.mp4`, 8'27", 79 bước) + skill `.claude/skills/video-creator-docs`.

Đang làm dở: thay đổi chưa commit — hrm-api `RoleController.php`, `RoleManagementService.php`, `routes/api.php`, `AdminRoleApiTest.php`; hrm-client `pages/admin/roles/index.vue`, `pages/admin/employee-roles/_id/index.vue`.
Bước tiếp theo: user quyết các mục trong `van-de-ton.md` (169 has_role theo nhóm, tên quyền lạ, push 4 commit local) → commit đợt bộ lọc → 8.19 gỡ `checkPermissionList*`.
Blocked: chờ user quyết has_role / push.

### Checkpoint — 30/10/2026 tối (chốt lịch go-live)
Vừa hoàn thành: chốt với user — go-live 31/10/2026 CHỈ TPE (etek/toyota để sau, đã ghi `../gd1-nen-du-lieu/runbook-go-live.md`). Việc tồn quyền/vai trò xử lý dần sau go-live.
Đang làm dở: đợt bộ lọc màn Vai trò + thẻ vai trò gọn (chưa commit); 4 commit local chưa push.
Bước tiếp theo: phiên mới — đo khối lượng (quyền mới trên `gop_db` từ 27/10 + thử merge worktree tạm) → xin "làm" merge `gop_db` → `rbac` 3 repo → khai mã/alias quyền mới + chạy Rbac → diễn tập dump prod mới (runbook A.2) → cửa sổ bảo trì (runbook B).
Ước tính: merge 2–4h, rà quyền mới 2–4h, diễn tập 1,5–3h, cửa sổ bảo trì 1–2h.
Blocked: cần user cho phép merge; cần người có quyền VPS cho cửa sổ bảo trì + dump prod mới.

### Checkpoint — 31/10/2026 (đo khối lượng merge gop_db → rbac, chỉ đọc)
Vừa hoàn thành: `git merge-tree` thử (không đụng worktree). rbac thiếu so với origin/gop_db: hrm-api 195 commit, client 122, ERP 49. File xung đột thật: hrm-api 25 (chủ yếu Timesheet/Assign/Finance controller + `PermissionsTableSeeder` + `AuthController`), client 4 (`V2BaseSmartFilterPanel`, `ProductFormQuickAdd`, `subsystem-menu/finance.js`, `manufacture-price-modes/index.vue`), ERP 8 (`routes/web.php`, `employees/create|edit.blade.php`, `ProductsController`…). File chưa commit của đợt bộ lọc KHÔNG trùng file gop_db sửa. Quyền mới trên gop_db chưa có trong Catalog: `quyen-moi-gop-db-31-10.txt` (vận chuyển, HDDV, BOM mẫu, nhắc hạn, điều chuyển kho, nhập/xuất lại…). Migration mới trên gop_db: hrm-api 18, ERP 5 (chỉ kéo code, chưa chạy).
Bước tiếp theo: xin "làm" merge 3 repo.

### Checkpoint — 31/10/2026 (merge rbac → gop_db LOCAL, CHƯA push)
Vừa hoàn thành: user yêu cầu "pull gop_db mới nhất rồi merge rbac vào, chưa push". Checkout chính 3 repo: hrm-api `d7b032a59`, hrm-client `4b2d5dacb`, ERP `af8341de79` (ERP ff 23 commit origin/gop_db trước). Gỡ 37 file xung đột; khai Catalog 57 tên quyền HRM mới (21 gắn mã ERP sẵn có + 20 mã mới, validate 0 lỗi); bỏ Super Admin ở 21 file code mới gop_db; middleware tên→mã 25 chỗ; ProductPriceBoardService::canViewCost + TransferProductAllocation kiểm qua PermissionChecker (code cũ query role_has_permissions.company_id ⇒ 500 sau convert). Test: Rbac hrm-api 388/389 (1 đỏ = DB test thiếu bảng inherited_price_factors), ERP Rbac 109/110 (1 lỗi = vendor classmap cũ còn RolesController), ProductPriceBoardApiTest 24/24. Playwright (API 8012 + Nuxt 3012, DB rehearsal, NV13 + NV663): bảng giá bán, bộ lọc defaultHidden/isVisible, nút thêm nhanh, 403 khi không quyền.
Còn lại: đợt bộ lọc màn Vai trò (wt-rbac) vẫn chưa commit nên KHÔNG có trong merge. Deploy: catalog-sync (20 mã mới), composer dump-autoload ERP, migration gop_db mới (hrm-api 18, ERP 5) chạy trước rbac:convert. Checkout chính :8000/:3000 đang chạy code rbac trên DB hrm_erp_21_10_prod CHƯA convert.
