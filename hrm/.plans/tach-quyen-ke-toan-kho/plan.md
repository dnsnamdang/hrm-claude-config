# Tách quyền "Kế toán kho" — Plan 1: Nền quyền (hrm-api) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khai 36 quyền mới trong Catalog dùng chung (ERP+HRM) thay cho quyền gộp `accounting.ke_toan_kho.manage`, và viết lệnh artisan cấp-lại-quyền để **mọi** Vai trò/nhân viên đang giữ quyền cũ nhận đủ 36 quyền mới — không ai mất quyền. Chạy & kiểm trên DB test. (Đây là Plan 1/3; re-point ERP = Plan 2, re-point HRM = Plan 3.)

**Architecture:** Catalog (`app/Support/Permissions/Catalog/accounting.php`) là nguồn sự thật duy nhất; `permission:catalog-sync` đồng bộ Catalog→bảng `permissions` (thêm/sửa/`deprecated_at`, không xoá cứng) và dựng lại `permission_aliases`. Một lệnh artisan **mới** (theo khuôn `RbacGrantRoleNameCodesCommand`) đọc **ai đang giữ** quyền cũ trên **cả hai** pivot `role_has_permissions` và `model_has_permissions` (= employee_has_permissions), nhân mỗi dòng grant thành 36 dòng cho 36 code mới — **sao y mọi cột**, chỉ đổi `permission_id` — idempotent, ghi lịch sử, có `--dry-run`/`--verify`/báo cáo CSV. Quyền cũ **giữ nguyên, chưa deprecate** trong Plan 1 (chỉ deprecate ở bước cuối §8.6, sau khi re-point ERP+HRM xong).

**Tech Stack:** PHP 7.4, Laravel 8, nwidart modules. Spatie permission (`role_has_permissions`, `model_has_permissions`/alias `employee_has_permissions`). PHPUnit với trait `DatabaseTransactions` + concern `Tests\Feature\Rbac\Concerns\GateFixture`. Catalog/CatalogSync/PermissionCatalog có sẵn.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/tach-quyen-ke-toan-kho/design.md` — plan này lập luận từ design đó; đọc cả hai. Trọng tâm Plan 1 = §3 (constraints), §5 (danh sách 36 code + kind/scope), §8.1–8.3 (Catalog → catalog-sync → lệnh cấp-lại copy 2 pivot 1:1), §9 (builder tự quyết).

## Global Constraints

- **PermissionsTableSeeder đã GỠ (từ 06/11/2026):** KHÔNG tạo seeder/migration cho quyền. Quyền chỉ khai trong Catalog, đồng bộ bằng `php artisan permission:catalog-sync`.
- **Code quyền cố định vĩnh viễn** một khi đã lên prod; không tái dùng/đổi code. 36 code mới dùng quy ước `accounting.ke_toan_kho_<slug>.<kind>`, `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `feature='Kế toán kho'`, `platforms=['erp','hrm']` (toàn bộ). Màn báo cáo (nhóm I #1–#5) `kind='view'`; còn lại `kind='action'`. **Mọi code đều là cờ: `scopes=[]`, `depends_on=[]`** (quyền cũ `scopes=[]` nên không có bậc phạm vi — design §8.3).
- **Catalog KHÔNG có trường `order`:** vị trí trong mảng quyết định thứ tự. Chèn 36 entry **ngay sau** entry `accounting.ke_toan_kho.manage` để đứng cạnh nhau.
- **Giữ quyền cũ `accounting.ke_toan_kho.manage` nguyên vẹn, CHƯA deprecate** trong Plan 1 (gồm cả `legacy` tên `'Kế toán kho'` api+web). 36 entry mới **không** khai `legacy` tên `'Kế toán kho'` (validator cấm một tên cũ thuộc nhiều code) → `legacy=[]`.
- **catalog-sync không xoá cứng:** chỉ set `deprecated_at`. Lệnh cấp-lại **chỉ thêm, không hạ, không xoá, chạy lại không nhân bản** (idempotent).
- **Fail-closed đã kiểm (design §7.5):** `PermissionCode.php:92` + `PermissionChecker.php:192,263` lọc `whereNull('deprecated_at')`. Sót re-point sau deprecate ⇒ chặn người dùng (ồn ào), không âm thầm mở. Nên quyền cũ phải sống suốt Plan 1–3.
- **DB test dùng chung, phpunit KHÔNG transactional-an-toàn khi chạy song song:** chạy test **một tiến trình** (không `--parallel`). Test dùng `DatabaseTransactions` nên tự rollback; KHÔNG để 2 process đụng cùng DB (gây lỗi giả). Lệnh chạy test: `php artisan test --filter=<Class> -p` **không** dùng; dùng `vendor/bin/phpunit --filter <Class>` đơn tiến trình.
- **Không commit/push/deploy khi chưa có yêu cầu.** Plan 1 chỉ chạy trên DB test local.

## Review Focus

- **Dòng grant trùng khoá chính khi chạy lại** (holder đã có code mới từ lần chạy trước): lệnh phải bỏ qua, không ném lỗi trùng PK, không nhân bản. → Task 2 test `test_chay_lai_khong_nhan_ban`.
- **Nhân viên được cấp THẲNG quyền cũ** (dòng ở `model_has_permissions`, không qua Vai trò): phải được nhân sang 36 code mới y như Vai trò — đây chính là lỗ hổng của khuôn mẫu (khuôn chỉ ghi `role_has_permissions`). → Task 2 test `test_cap_ca_nhan_vien_gan_thang`.
- **Sao cột không-permission_id phải y nguyên** (scope NULL, `company_id`/team nếu DB chưa chuyển đổi, `model_type` đúng của từng pivot): sai một cột ⇒ grant lệch công ty/không hiệu lực. → Task 2 test `test_sao_y_moi_cot_chi_doi_permission_id`.
- **Một trong 36 code chưa sync / đã deprecate** khi chạy lệnh: phải exit 1, KHÔNG ghi gì (nửa chừng = nguy hiểm). → Task 2 test `test_ma_chua_san_sang_exit_1_khong_ghi`.
- **`permission:catalog-sync` trên catalog có 36 entry mới**: phải `inserted` đúng 36 code, không `deprecated` nhầm code cũ, danh mục hợp lệ (validate=[]). → Task 1 test + Task 3 verify.

---

## File Structure

- `app/Support/Permissions/Catalog/accounting.php` — **sửa**: chèn 36 entry sau entry quyền cũ.
- `app/Support/Permissions/KeToanKhoSplitMap.php` — **tạo**: map tĩnh `oldCode()` + `newCodes()` (37 code), để lệnh và test dùng chung một nguồn (mô phỏng `RoleNameCodeMap`).
- `app/Console/Commands/RbacGrantKeToanKhoSplitCommand.php` — **tạo**: lệnh cấp-lại-quyền.
- `tests/Feature/Rbac/KeToanKhoCatalogTest.php` — **tạo**: test 36 entry Catalog + map.
- `tests/Feature/Rbac/RbacGrantKeToanKhoSplitTest.php` — **tạo**: test lệnh (khuôn theo `RbacGrantRoleNameCodesTest.php`).

---

### Task 1: 36 entry Catalog + KeToanKhoSplitMap

**Files:**
- Create: `app/Support/Permissions/KeToanKhoSplitMap.php`
- Modify: `app/Support/Permissions/Catalog/accounting.php` (chèn sau entry `accounting.ke_toan_kho.manage`, giữ entry cũ nguyên)
- Test: `tests/Feature/Rbac/KeToanKhoCatalogTest.php`

**Interfaces:**
- Produces:
  - `KeToanKhoSplitMap::oldCode(): string` → `'accounting.ke_toan_kho.manage'`
  - `KeToanKhoSplitMap::newCodes(): array` → 36 code (có prefix `accounting.`), đúng danh sách §5 dưới đây.
  - `KeToanKhoSplitMap::all(): array` → `array_merge([oldCode()], newCodes())` (37 code) — dùng cho `ensureCode` trong test Task 2.
- 36 code (suffix sau `accounting.` + nhãn `name`, `feature='Kế toán kho'`):
  - I báo cáo (`kind='view'`): `ke_toan_kho_the_kho.view` "Kế toán kho — Thẻ kho kế toán" · `ke_toan_kho_bc_ban_hang.view` "Kế toán kho — BC bán hàng (kế toán)" · `ke_toan_kho_bc_nhap_mua.view` "Kế toán kho — BC nhập mua (kế toán)" · `ke_toan_kho_bc_kho.view` "Kế toán kho — BC kho kế toán" · `ke_toan_kho_bc_ton_lau.view` "Kế toán kho — BC hàng tồn lâu"
  - còn lại (`kind='action'`): `ke_toan_kho_ton_dau_ky.manage` "Kế toán kho — Tồn kho đầu kỳ kế toán" · `ke_toan_kho_yc_nhap_hang.manage` "Kế toán kho — YC nhập hàng" · `ke_toan_kho_phieu_nhap_mua.manage` "Kế toán kho — Phiếu nhập mua" · `ke_toan_kho_phieu_nhap_kho.manage` "Kế toán kho — Phiếu nhập kho" · `ke_toan_kho_yc_nhap_theo_don.manage` "Kế toán kho — YC nhập theo đơn" · `ke_toan_kho_to_khai_hai_quan.manage` "Kế toán kho — Tờ khai hải quan" · `ke_toan_kho_de_nghi_xuat_kho.manage` "Kế toán kho — Đề nghị/YC xuất hàng" · `ke_toan_kho_phieu_xuat.manage` "Kế toán kho — Phiếu xuất" · `ke_toan_kho_phieu_xuat_kho.manage` "Kế toán kho — Phiếu xuất kho" · `ke_toan_kho_yc_tach_xuat.manage` "Kế toán kho — YC tách xuất" · `ke_toan_kho_yc_gop_xuat.manage` "Kế toán kho — YC gộp xuất" · `ke_toan_kho_yc_chuyen_hang.manage` "Kế toán kho — YC chuyển hàng" · `ke_toan_kho_dieu_chuyen_nhap_thang.manage` "Kế toán kho — Điều chuyển nhập thẳng" · `ke_toan_kho_phan_bo_hang.manage` "Kế toán kho — Phân bổ hàng" · `ke_toan_kho_phan_bo_noi_dia.manage` "Kế toán kho — Phân bổ nội địa" · `ke_toan_kho_phan_bo_dieu_chuyen.manage` "Kế toán kho — Phân bổ điều chuyển" · `ke_toan_kho_bien_ban_kiem_ke.manage` "Kế toán kho — Biên bản kiểm kê" · `ke_toan_kho_nhap_dieu_chinh_kiem_ke.manage` "Kế toán kho — Nhập kho điều chỉnh kiểm kê" · `ke_toan_kho_xuat_dieu_chinh_kiem_ke.manage` "Kế toán kho — Xuất kho điều chỉnh kiểm kê" · `ke_toan_kho_tu_kiem_ke.manage` "Kế toán kho — Tự kiểm kê" · `ke_toan_kho_yc_ban_hang_muon.manage` "Kế toán kho — YC bán hàng mượn" · `ke_toan_kho_ban_hang_muon.manage` "Kế toán kho — Bán hàng mượn" · `ke_toan_kho_yc_xuat_hang_muon.manage` "Kế toán kho — YC xuất hàng mượn" · `ke_toan_kho_xuat_hang_muon.manage` "Kế toán kho — Xuất hàng mượn" · `ke_toan_kho_yc_gia_han_hang_muon.manage` "Kế toán kho — YC gia hạn hàng mượn" · `ke_toan_kho_yc_thanh_toan_giao_hang.manage` "Kế toán kho — YC thanh toán giao hàng" · `ke_toan_kho_thanh_toan_giao_hang_nv.manage` "Kế toán kho — Thanh toán giao hàng nhân viên" · `ke_toan_kho_yc_thanh_toan_giao_hang_khac.manage` "Kế toán kho — YC thanh toán giao hàng khác" · `ke_toan_kho_ket_qua_giao_viec.manage` "Kế toán kho — Kết quả giao việc (hạch toán DV)" · `ke_toan_kho_yc_lam_dich_vu_ke_toan.manage` "Kế toán kho — YC làm dịch vụ kế toán" · `ke_toan_kho_yc_hach_toan_bo_sung.manage` "Kế toán kho — YC hạch toán bổ sung"
  - Mỗi entry: `'subsystem_group'=>'Kinh doanh - Tài chính'`, `'subsystem'=>'Kế toán'`, `'feature'=>'Kế toán kho'`, `'scopes'=>[]`, `'depends_on'=>[]`, `'platforms'=>['erp','hrm']`, `'legacy'=>[]`.

- [x] **Step 1: Viết test fail** `tests/Feature/Rbac/KeToanKhoCatalogTest.php` (class `extends TestCase`, `use DatabaseTransactions`), các method:
  - `test_map_co_1_ma_cu_va_36_ma_moi`: `assertSame('accounting.ke_toan_kho.manage', KeToanKhoSplitMap::oldCode())`; `assertCount(36, KeToanKhoSplitMap::newCodes())`; `assertCount(36, array_unique(KeToanKhoSplitMap::newCodes()))`; mọi code bắt đầu `accounting.ke_toan_kho_`; `assertCount(37, KeToanKhoSplitMap::all())`.
  - `test_36_entry_co_trong_catalog_dung_thuoc_tinh`: `$entries = PermissionCatalog::load();` → map theo code; với mỗi code trong `newCodes()`: tồn tại 1 entry; `platforms===['erp','hrm']`; `scopes===[]`; `depends_on===[]`; `feature==='Kế toán kho'`; `subsystem==='Kế toán'`; `legacy===[]`; `kind` khớp (`.view`→`'view'`, `.manage`→`'action'`).
  - `test_danh_muc_hop_le_va_khong_dung_ma_cu`: `assertSame([], PermissionCatalog::validate(PermissionCatalog::load()))`; entry `accounting.ke_toan_kho.manage` vẫn còn và `legacy` vẫn chứa `['api','Kế toán kho',null]` + `['web','Kế toán kho',null]`; không code mới nào khai legacy `'Kế toán kho'`.
  - `test_36_entry_dung_sau_ma_cu`: trong `array_column($entries,'code')`, chỉ số của 36 code mới đều `>` chỉ số của `accounting.ke_toan_kho.manage` và liền kề (36 vị trí liên tục ngay sau).
- [x] **Step 2: Chạy test → FAIL** `vendor/bin/phpunit --filter KeToanKhoCatalogTest`. Expected: FAIL (`KeToanKhoSplitMap` không tồn tại / thiếu entry).
- [x] **Step 3: Tạo `KeToanKhoSplitMap`** với `oldCode()`, `newCodes()` (36 code theo danh sách trên), `all()`.
- [x] **Step 4: Chèn 36 entry vào `accounting.php`** ngay sau entry `accounting.ke_toan_kho.manage` (dòng ~10–24 cũ), đúng thuộc tính Global Constraints. Giữ entry cũ y nguyên.
- [x] **Step 5: Chạy test → PASS** `vendor/bin/phpunit --filter KeToanKhoCatalogTest`. Expected: PASS. Chạy thêm `vendor/bin/phpunit --filter 'PermissionCatalogTest|CatalogContentTest'` → PASS (danh mục thật vẫn hợp lệ, phủ legacy không vỡ).
- [x] **Step 6: Commit** `git add app/Support/Permissions/KeToanKhoSplitMap.php app/Support/Permissions/Catalog/accounting.php tests/Feature/Rbac/KeToanKhoCatalogTest.php && git commit -m "feat(rbac): khai 36 quyền Kế toán kho tách nhỏ trong Catalog + KeToanKhoSplitMap"`

---

### Task 2: Lệnh `rbac:grant-ke-toan-kho-split` (cấp-lại-quyền, 2 pivot)

**Files:**
- Create: `app/Console/Commands/RbacGrantKeToanKhoSplitCommand.php`
- Test: `tests/Feature/Rbac/RbacGrantKeToanKhoSplitTest.php`

**Interfaces:**
- Consumes: `KeToanKhoSplitMap` (Task 1); `GateFixture` concern (`ensureCode`, `makeRole`, `grant($roleId,$permId,$scope)`, `makeEmployee`, `assignRole`, `resetCaches`); `App\Services\Admin\RoleManagementService` (`log()`, `afterWrite()`) — như khuôn mẫu.
- Produces (signature lệnh):
  - `protected $signature = 'rbac:grant-ke-toan-kho-split {--dry-run} {--verify} {--report-dir=}'`
  - `handle(): int` — 0 thành công, 1 khi tiền kiểm thất bại (một trong 37 code thiếu/deprecate) hoặc `--verify` phát hiện lệch.
- Hành vi:
  1. **Tiền kiểm (trước mọi ghi, trước cả tạo thư mục báo cáo):** nạp `permission_id` của `oldCode()` + 36 `newCodes()` qua `permissions` lọc `whereNull('deprecated_at')`. Thiếu bất kỳ code nào ⇒ in tên code + lý do (`chưa sync` / `ngừng dùng`), **exit 1, không ghi, không tạo thư mục báo cáo**.
  2. **Nguồn:** mọi dòng `role_has_permissions` có `permission_id = oldId`, và mọi dòng `model_has_permissions` (employee_has_permissions) có `permission_id = oldId`.
  3. **Nhân:** mỗi dòng nguồn × 36 → dòng đích **sao y toàn bộ cột**, chỉ đổi `permission_id` sang `newId`. Idempotent: bỏ qua nếu dòng đích đã tồn tại (so khoá chính đầy đủ của từng pivot). Ghi trong `DB::transaction`.
  4. **Lịch sử:** mỗi Vai trò được thêm code mới → `RoleManagementService::log($roleId,'permissions',[],['added'=>[...]])` + `afterWrite()` (parity khuôn). Mỗi nhân viên được cấp thẳng → ghi 1 bản ghi lịch sử qua cơ chế sẵn có cho đổi quyền trực tiếp nhân viên (`employee_permission_history` — builder dùng adapter/service hiện hữu; test chỉ chốt "có ≥1 bản ghi/ holder").
  5. **Báo cáo CSV** trong `--report-dir`: `cap-ma-ke-toan-kho.csv` cột `holder_type,holder_id,company,code,hanh_dong` (`insert`/`skip`); `--verify` xuất `doi-chieu-ke-toan-kho.csv` holder nào thiếu code nào.
  6. `--dry-run`: tính & ghi CSV, KHÔNG đụng DB. `--verify`: chỉ đọc, 0 lệch ⇒ exit 0.

- [x] **Step 1: Viết test fail** `tests/Feature/Rbac/RbacGrantKeToanKhoSplitTest.php` (`extends TestCase`, `use DatabaseTransactions, GateFixture`). `setUp`: `buildGateFixture()`; `foreach (KeToanKhoSplitMap::all() as $c) $this->perm[$c]=$this->ensureCode($c,'Zz KTK');`. Fixtures: `$roleHold = makeRole('TPV_Kế toán kho', C1)` được `grant($roleHold, perm[oldCode], null)` và `assignRole` cho `$this->e`; `$empDirect = makeEmployee('KTKDIRECT',C1)` được chèn thẳng 1 dòng `model_has_permissions` cho `perm[oldCode]` (chèn trực tiếp như `PermissionMergerTest.php:190`); `$roleNone = makeRole('TPV_Khac',C1)` KHÔNG giữ quyền cũ. `run_(opts)` gọi `Artisan::call('rbac:grant-ke-toan-kho-split', merge(['--report-dir'=>dir],opts))` + `resetCaches()`. Methods:
  - `test_dry_run_khong_ghi`: đếm `role_has_permissions`+`model_has_permissions`+`role_permission_history` trước/sau bằng nhau; `run_(['--dry-run'=>true])===0`; CSV mọi dòng `hanh_dong='insert'`.
  - `test_cap_vai_tro_du_36_ma`: `run_()===0`; `$roleHold` giờ có đúng 36 `permission_id` của `newCodes()` trong `role_has_permissions` (không thừa/thiếu); `$roleNone` không có code mới nào; `PermissionChecker::for($this->e,C1)->has('accounting.ke_toan_kho_phieu_xuat.manage')===true`.
  - `test_cap_ca_nhan_vien_gan_thang`: sau `run_()`, `$empDirect` có 36 dòng `model_has_permissions` cho 36 `newCodes()`; `PermissionChecker::for($empDirect,C1)->has('accounting.ke_toan_kho_the_kho.view')===true`.
  - `test_sao_y_moi_cot_chi_doi_permission_id`: lấy 1 dòng nguồn `role_has_permissions` (oldId) và 1 dòng đích bất kỳ → mọi cột trừ `permission_id` bằng nhau (scope NULL, `company_id`/team nếu cột tồn tại); tương tự cho 1 dòng `model_has_permissions` (`model_type`, morph key, company/team y nguyên).
  - `test_chay_lai_khong_nhan_ban`: `run_()` 2 lần; số dòng 2 pivot + lịch sử sau lần 2 = sau lần 1; CSV lần 2 mọi `hanh_dong='skip'`.
  - `test_ma_chua_san_sang_exit_1_khong_ghi`: xoá 1 trong 36 khỏi `permissions`; `run_()===1`; output chứa code đó; đếm 2 pivot không đổi; thư mục báo cáo không được tạo (`assertDirectoryDoesNotExist`).
  - `test_ma_ngung_dung_exit_1`: set `deprecated_at=now()` cho 1 trong 36; `run_()===1`; output chứa "ngừng dùng"; không ghi.
  - `test_ghi_lich_su`: sau `run_()`, `role_permission_history` có ≥1 bản ghi cho `$roleHold` với `new_value.added` chứa 36 code; `employee_permission_history` có ≥1 bản ghi cho `$empDirect`.
  - `test_verify_sau_cap_0_lech`: `run_()`; `run_(['--verify'=>true])===0`; CSV `doi-chieu-ke-toan-kho.csv` không có dòng cho `$roleHold`/`$empDirect`. Trước khi cấp: `run_(['--verify'=>true])===0` nhưng CSV có dòng lệch (cu=1,moi=0) cho holder cũ.
- [x] **Step 2: Chạy test → FAIL** `vendor/bin/phpunit --filter RbacGrantKeToanKhoSplitTest`. Expected: FAIL (lệnh chưa tồn tại — `Command "rbac:grant-ke-toan-kho-split" is not defined`).
- [x] **Step 3: Tạo lệnh** `RbacGrantKeToanKhoSplitCommand` theo khuôn `RbacGrantRoleNameCodesCommand.php` (tiền kiểm → `loadPermissions`; `grant()`/`verify()`; `writeCsv`), nhưng: nguồn = holder của `oldCode` trên **2 pivot**; nhân 1→36 **sao y cột** (đọc dòng nguồn thành mảng cột, set `permission_id`, insert nếu chưa có); lịch sử role qua `RoleManagementService`, lịch sử nhân viên qua cơ chế `employee_permission_history` sẵn có. Đăng ký lệnh (Kernel tự quét `app/Console/Commands`).
- [x] **Step 4: Chạy test → PASS** `vendor/bin/phpunit --filter RbacGrantKeToanKhoSplitTest`. Expected: PASS (đơn tiến trình; KHÔNG `-p`/`--parallel` — DB test dùng chung).
- [x] **Step 5: Commit** `git add app/Console/Commands/RbacGrantKeToanKhoSplitCommand.php tests/Feature/Rbac/RbacGrantKeToanKhoSplitTest.php && git commit -m "feat(rbac): lệnh rbac:grant-ke-toan-kho-split cấp-lại 36 quyền cho holder quyền cũ (2 pivot, idempotent)"`

---

### Task 3: Chạy & kiểm trên DB test (catalog-sync + lệnh cấp-lại)

**Files:** không tạo/sửa file sản phẩm — bước vận hành + kiểm chứng trên DB test. Ghi kết quả vào checkpoint plan.

**Interfaces:**
- Consumes: `permission:catalog-sync` (có `--dry-run`); `rbac:grant-ke-toan-kho-split` (Task 2).

- [x] **Step 1: Dry-run catalog-sync** `php artisan permission:catalog-sync --dry-run`. Expected: liệt kê `inserted` chứa đúng 36 code mới `accounting.ke_toan_kho_*`; **không** có code cũ `accounting.ke_toan_kho.manage` trong `deprecated`; không lỗi validate.
- [x] **Step 2: Sync thật** `php artisan permission:catalog-sync`. Expected: 36 code mới có trong bảng `permissions` (`whereNull('deprecated_at')`); `permission_aliases` dựng lại, tên `'Kế toán kho'` vẫn trỏ về code cũ. Kiểm nhanh: `php artisan tinker --execute="echo \DB::table('permissions')->where('code','like','accounting.ke_toan_kho\_%')->whereNull('deprecated_at')->count();"` → `36`.
- [x] **Step 3: Đếm holder quyền cũ (chuẩn so sánh)** qua tinker: số role ở `role_has_permissions` + số (model_type,employee) ở `model_has_permissions` có `permission_id` = id của `accounting.ke_toan_kho.manage`. Ghi lại con số.
- [x] **Step 4: Dry-run lệnh cấp-lại** `php artisan rbac:grant-ke-toan-kho-split --dry-run --report-dir=<scratchpad>/ktk-report`. Expected: exit 0; CSV cho thấy mỗi holder ở Step 3 có 36 dòng `insert`.
- [x] **Step 5: Chạy thật** `php artisan rbac:grant-ke-toan-kho-split --report-dir=<scratchpad>/ktk-report-run`. Expected: exit 0.
- [x] **Step 6: Verify** `php artisan rbac:grant-ke-toan-kho-split --verify --report-dir=<scratchpad>/ktk-verify`. Expected: exit 0; CSV `doi-chieu-ke-toan-kho.csv` rỗng (mọi holder quyền cũ đã có đủ 36 code mới). Chạy lại Step 5 lần nữa → mọi dòng CSV `skip` (idempotent).
- [x] **Step 7: Ghi checkpoint** vào plan.md (đã làm gì, số holder, số dòng cấp, exit code). KHÔNG commit gì (chỉ dữ liệu DB test). KHÔNG chạy bước deprecate quyền cũ (thuộc §8.6, sau Plan 2+3).

---

## Self-Review

**1. Spec coverage:** §8.1 (36 entry Catalog, giữ code cũ) → Task 1. §8.2 (catalog-sync) → Task 3 Step 1–2. §8.3 (lệnh cấp-lại copy 2 pivot 1:1, chỉ đổi permission_id, idempotent) → Task 2. §3 constraints (Catalog là nguồn sự thật, không seeder, không xoá cứng, scopes=[]) → Global Constraints + Task 1/2 tests. §5 danh sách 36 + kind → Task 1 Interfaces. §9 builder tự quyết (slug/nhãn, thứ tự cạnh nhau, số commit) → đã chốt trong Task 1. §10 (Plan 1 = nền quyền, chạy trên DB test) → đúng phạm vi 3 task. Bước deprecate (§8.6) **cố ý** nằm ngoài Plan 1 (sau re-point). Re-point ERP/HRM (§5 gate map, §6 OR gộp) **không** thuộc Plan 1 — là Plan 2/3.

**2. Step scan:** mỗi test step chốt tên test + assertion cụ thể; mỗi code step chốt signature/thuộc tính, để thân cho builder (idiomatic). Không có bước "xử lý edge case" trống.

**3. Type consistency:** `KeToanKhoSplitMap::oldCode()/newCodes()/all()` dùng nhất quán Task 1↔2. Lệnh `rbac:grant-ke-toan-kho-split` + `--dry-run/--verify/--report-dir` nhất quán Task 2↔3. `perm[$code]=>id`, `run_()` theo đúng khuôn `RbacGrantRoleNameCodesTest`.

**4. Review Focus:** 5 mục đều có test sở hữu (trùng PK→`test_chay_lai`; nhân viên gán thẳng→`test_cap_ca_nhan_vien_gan_thang`; sao y cột→`test_sao_y_moi_cot`; code chưa sẵn sàng→`test_ma_chua_san_sang`/`test_ma_ngung_dung`; catalog-sync→Task 1 `test_danh_muc_hop_le` + Task 3 Step 1–2).

**5. Proportion:** plan dài hơn code đôi chút vì liệt kê 36 code (dữ liệu bắt buộc, không suy ra được) + bộ test. Thân lệnh/entry để builder viết. Chấp nhận được.

---

## Execution Handoff

Native (executing-plans) — user chọn 26/11

---

## Checkpoint Task 3 (2026-11-26) — chạy & kiểm trên DB test

DB test `erp_hrm_check@127.0.0.1:3306` (local, KHÔNG phải prod). KHÔNG commit, KHÔNG deprecate quyền cũ (để §8.6 sau Plan 2+3).

- **catalog-sync**: `--dry-run` → 36 code mới `accounting.ke_toan_kho_*` = "Thêm", summary `thêm 40 · sửa 949 · ngừng dùng 0` (code cũ không bị deprecate), không lỗi validate. Sync thật → `new_live=36` (`whereNull('deprecated_at')`). Code cũ `accounting.ke_toan_kho.manage` (id **1208892**) còn, `deprecated_at=NULL`. Alias `legacy_name='Kế toán kho'` vẫn trỏ code cũ (guard api + web).
- **Holder quyền cũ**: `role_has_permissions` = **2 role** (id 100002, 18); `employee_has_permissions` = **0**.
- **grant `--dry-run`**: exit 0; CSV **72 insert** (mỗi role 36 dòng), 0 NV cấp thẳng.
- **grant thật**: exit 0; thêm 72 / bỏ qua 0.
- **`--verify`**: 0 dòng lệch, CSV `doi-chieu-ke-toan-kho.csv` rỗng, exit 0. Chạy lại grant → thêm 0 / bỏ qua 72 (idempotent), exit 0.
- **Kiểm gốc DB**: role 100002 & 18 mỗi role đúng **36** dòng mã mới trong `role_has_permissions`; `role_permission_history` mỗi role `added_count=36`.

→ Plan 1 (nền quyền 36 mã + lệnh cấp-lại) hoàn tất trên DB test. Bước tiếp: review toàn nhánh, rồi Plan 2 (re-point ERP) + Plan 3 (re-point HRM). Deprecate code cũ là bước CUỐI (§8.6), sau re-point.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: Plan 1 đủ 3 task — Task 1 `4772aff58` (36 entry Catalog + `KeToanKhoSplitMap`), Task 2 `78093712c` (lệnh `rbac:grant-ke-toan-kho-split`, 9 test / 374 assertion pass), Task 3 chạy trên DB test erp_hrm_check (không commit). Review toàn nhánh (reviewer mới, 16:44): **Ready to merge**, không Critical/Important, 3 Minor vô hại → không có fix pass. Nhánh hrm-api develop.
Đang làm dở: (không)
Bước tiếp theo: user chọn viết Plan 2 (re-point ERP) hay dừng để review Plan 1; sau Plan 2+3 mới deprecate mã cũ (§8.6).
Blocked: 2 commit `4772aff58`, `78093712c` **CHƯA PUSH** (local develop đi trước origin 2) — chờ user cho phép; CHƯA gop_db. Ghi chú: 3 test CatalogContentTest fail có sẵn từ trước, không do thay đổi này.
