# Giai đoạn 1 — Nền dữ liệu Vai trò & Quyền: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mỗi quyền có một mã chung cho ERP và HRM. Mỗi vai trò thuộc một công ty. Mọi đường kiểm quyền
hiện có (vẫn gọi bằng tên cũ) đi qua một bộ kiểm chung, luôn lọc theo công ty đang làm việc. Kèm lệnh
chuyển đổi dữ liệu có báo cáo chênh lệch.

**Architecture:**
- Schema mới đặt ở hrm-api.
- `PermissionChecker` là bản giống hệt ở hrm-api và ERP. Nó đọc thẳng các bảng, không qua spatie, và
  dịch tên cũ sang mã qua `permission_aliases`.
- Danh mục quyền là các file PHP trong hrm-api, đồng bộ theo mã.
- Lệnh `rbac:convert` tách vai trò theo công ty, nhập quyền theo danh mục, rồi so quyền hiệu lực trước và
  sau cho từng nhân viên × công ty.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Laravel 6 / PHP 7.4 (ERP TanPhatDev), MySQL 8, PHPUnit 9 / 8.

**Spec:** `../design.md` (tổng, đã duyệt) và `./design.md` (cách làm giai đoạn 1). Executor đọc cả hai.

## Global Constraints

- **Mọi bước đụng source** (tạo nhánh/worktree, sửa code, migration, chạy migrate/lệnh vào DB nào, commit)
  phải hỏi user và nhận câu "làm" riêng, nêu rõ repo, nhánh, file/bảng, DB đích. Chạy migrate thì liệt kê
  đúng tên file, chạy lẻ bằng `--path`. Không push.
- Thuật ngữ: **"Vai trò"**. Không dùng "chức vụ" cho role trong code mới, comment, message hay tên file.
- Phạm vi: `1 = Bộ phận · 2 = Phòng ban · 3 = Công ty · 4 = Tổng công ty`. Số lớn bao số nhỏ.
- Mã quyền khớp `^[a-z0-9_]+(\.[a-z0-9_]+){2,}$`. Không chứa phạm vi, không chứa nền tảng.
- Tên vai trò = `{companies.code}_{base_name}`. Chỉ kiểm trùng `base_name` trong cùng công ty.
- `PermissionChecker.php` và `PermissionScope.php` **giống hệt từng byte** ở hai repo. Phải chạy được trên PHP 7.4 (không `match`, không enum, không named args).
- Kiểm quyền không bao giờ fail-open: mã hoặc tên cũ không tra được thì trả `false`.
- Super Admin không còn bypass (gỡ `Gate::before`). Super Admin có quyền vì được gán đủ mã.
- PHP: `PHP=/opt/homebrew/opt/php@7.4/bin/php`. Test chạy trên DB `hrm_erp_rbac_test`, không chạy trên DB `.env`.
- Mọi test quyền có 3 ca: có quyền, không quyền, có quyền ở **công ty khác**.
- Không `git stash`. Không `pkill` theo tên. Giữ kiểu xuống dòng (CRLF/LF) của file đang sửa.

## Review Focus

1. **Người làm ở 2 công ty, có vai trò ở cả hai.** Đổi công ty đang làm việc thì quyền phải đổi theo ngay
   trong request kế tiếp: `RequestCache`/memo không được giữ quyền của công ty cũ. → Task 2, test `test_doi_cong_ty_khong_dung_cache_cong_ty_cu`.
2. **Tên cũ khác nhau một dấu tiếng Việt** ("mục" và "mức"). Alias phải so theo từng byte, không gộp nhầm. → Task 2, test `test_alias_so_khop_tung_byte`.
3. **Nhân viên có vai trò ở công ty C nhưng C không nằm trong `company_employees`.** Phải ra rỗng
   (không làm việc ở đó) và hiện trong báo cáo, không âm thầm mất. → Task 2 `test_khong_lam_viec_o_cong_ty_thi_rong` + Task 7 thêm cặp trước khi chụp mốc.
4. **Quyền cũ có trong DB nhưng thiếu trong danh mục** (feature khác vừa thêm vào seeder cũ trên `gop_db`).
   Chuyển đổi phải dừng và liệt kê, không lặng lẽ làm mất quyền. → Task 6 `test_quyen_cu_khong_co_trong_danh_muc_thi_dung`.
5. **Vai trò cũ không có công ty nào** (không có dòng ở `company_roles`/rhp/ehr). Không chuyển, không gây
   lỗi, có tên trong `vai-tro-khong-chuyen.csv`. → Task 7 `test_role_khong_cong_ty_khong_chuyen`.

---

### Task 0: Chuẩn bị môi trường (không phải code, nhưng cần user cho phép)

- [ ] **Step 1:** Hỏi user một câu, nêu phạm vi:
  - tạo nhánh `rbac` từ `origin/gop_db` ở `HRM/hrm-api` và `ERP/TanPhatDev`;
  - tạo worktree `../wt-rbac/hrm-api` và `../wt-rbac/TanPhatDev`, mỗi bên `composer install` riêng;
  - nhân bản DB local `hrm_erp_21_10_prod` sang `hrm_erp_rbac_test` bằng `mysqldump | mysql`.

  Chờ câu "làm".
- [ ] **Step 2:** Làm đúng 3 việc trên. Kiểm tra:
  - `git -C ../wt-rbac/hrm-api branch --show-current` ra `rbac`;
  - `SELECT COUNT(*) FROM hrm_erp_rbac_test.role_has_permissions` ra 20824 (số local 25/10).

---

### Task 1: Migration schema (hrm-api)

**Files:**
- Create: `database/migrations/2026_11_01_000001_add_catalog_columns_to_permissions_table.php` (cột mục 2.1, bỏ 2 unique cũ, unique `code`; `hasColumn` cho `code`)
- Create: `database/migrations/2026_11_01_000002_create_permission_aliases_table.php` (mục 2.2)
- Create: `database/migrations/2026_11_01_000003_add_company_id_and_base_name_to_roles_table.php` (nullable ở bước này; NOT NULL + unique `(company_id, base_name)` để Task 7 đặt sau chuyển đổi)
- Create: `database/migrations/2026_11_01_000004_add_unique_to_company_employees_table.php` (xoá dòng trùng, giữ id nhỏ nhất; dòng xoá chép vào `bak_rbac_company_employees_dups`)
- Create: `database/migrations/2026_11_01_000005_add_scope_to_role_has_permissions_table.php` (thêm `scope tinyint NULL`, chưa đổi PK. Checker không đọc `rhp.company_id` nên chạy được ngay)
- Test: `tests/Feature/Rbac/SchemaTest.php`

Dựng lại `role_has_permissions` / `employee_has_roles` **không** làm bằng migration. Việc đó thuộc `rbac:convert` (Task 7), vì cần dữ liệu cũ để chuyển.

**Interfaces:**
- Produces: các cột và bảng ở `./design.md` mục 2.1–2.4, 2.7, đúng tên.

- [ ] **Step 1:** Viết `SchemaTest`:
  - `test_permissions_co_cot_danh_muc`: `Schema::hasColumns('permissions', ['code','subsystem_group','subsystem','feature','kind','allowed_scopes','depends_on','on_erp','on_hrm','deprecated_at'])` === true.
  - `test_code_unique_mot_minh`: chèn 2 dòng cùng `code`, khác `guard_name`, thì ném `QueryException`.
  - `test_ten_khong_con_unique`: chèn 2 dòng cùng `name` + `guard_name`, khác `code`, thì không lỗi.
  - `test_alias_unique_theo_byte`: chèn alias `('Quản lý mục','web')` và `('Quản lý mức','web')` thì cả hai vào được. Chèn lại `('Quản lý mục','web')` thì lỗi.
  - `test_company_employees_unique`: chèn trùng `(employee_id, company_id)` thì lỗi.
  - `test_rhp_co_scope`: `Schema::hasColumn('role_has_permissions','scope')` === true.
- [ ] **Step 2:** `cd ../wt-rbac/hrm-api && DB_DATABASE=hrm_erp_rbac_test $PHP vendor/bin/phpunit tests/Feature/Rbac/SchemaTest.php`. Kỳ vọng: FAIL (thiếu cột).
- [ ] **Step 3:** Viết 5 migration, mỗi bản có `down()` trả lại đúng như cũ.
- [ ] **Step 4:** Hỏi user cho chạy đúng 5 migration này vào `hrm_erp_rbac_test` (liệt kê tên + `--pretend`). Được phép thì chạy từng bản: `DB_DATABASE=hrm_erp_rbac_test $PHP artisan migrate --path=database/migrations/<file>`.
- [ ] **Step 5:** Chạy lại test. Kỳ vọng: 6 passed.
- [ ] **Step 6:** Commit `feat(rbac): schema danh mục quyền, alias, vai trò theo công ty` (khi user cho phép commit).

---

### Task 2: `PermissionScope` + `PermissionChecker` (hrm-api)

**Files:**
- Create: `app/Support/Permissions/PermissionScope.php`
- Create: `app/Support/Permissions/PermissionChecker.php`
- Test: `tests/Feature/Rbac/PermissionCheckerTest.php`

**Interfaces:**
- Produces:
  - `PermissionScope::PART = 1, DEPARTMENT = 2, COMPANY = 3, GROUP = 4`; `PermissionScope::all(): array` → `[1,2,3,4]`; `PermissionScope::label(int): string` → `'Bộ phận'|'Phòng ban'|'Công ty'|'Tổng công ty'`.
  - `PermissionChecker::for(int $employeeId, int $companyId): PermissionChecker` (memo tĩnh theo `"$employeeId|$companyId"`)
  - `->grants(): array` dạng `[code => ?int scope]`
  - `->has(string $code): bool`
  - `->scope(string $code): ?int` (null khi không có quyền hoặc quyền không có phạm vi)
  - `->hasLegacy(string $legacyName, string $guard): bool`
  - `->legacyNames(string $guard): array` (danh sách tên cũ mà người này đang đạt, sắp xếp tăng)
  - `PermissionChecker::flush(): void`
- Truy vấn: `./design.md` mục 3.

- [ ] **Step 1:** Viết test với fixture: công ty 1 và 2, nhân viên E (`company_employees` có cả 1 và 2), vai trò R1 (công ty 1) có `t.doc.view` scope 2 và `t.doc.update`, vai trò R2 (công ty 2) có `t.doc.view` scope 4. Alias `('Xem tài liệu phòng','web') → t.doc.view min 2`, `('Xem tài liệu bộ phận','web') → min 1`, `('Xem tài liệu công ty','web') → min 3`.
  - `test_co_quyen_tai_cong_ty_dang_lam`: `for(E,1)->has('t.doc.update')` true.
  - `test_khong_co_quyen`: `for(E,1)->has('t.doc.delete')` false.
  - `test_quyen_cong_ty_khac_khong_lot`: `for(E,2)->has('t.doc.update')` false.
  - `test_scope_lay_lon_nhat`: thêm R3 (công ty 1) có `t.doc.view` scope 3 cho E. Kỳ vọng `for(E,1)->scope('t.doc.view')` === 3.
  - `test_legacy_cap_cao_bao_cap_thap`: `for(E,1)->hasLegacy('Xem tài liệu bộ phận','web')` true, `hasLegacy('Xem tài liệu công ty','web')` false.
  - `test_legacy_khong_tra_duoc_thi_false`: `hasLegacy('Không tồn tại','web')` false.
  - `test_alias_so_khop_tung_byte`: alias `'Quản lý mục'` có, gọi `hasLegacy('Quản lý mức','web')` thì false.
  - `test_khong_lam_viec_o_cong_ty_thi_rong`: xoá `company_employees(E,2)`. Kỳ vọng `for(E,2)->grants()` === [].
  - `test_quyen_ngung_dung_khong_tinh`: đặt `deprecated_at` cho `t.doc.update`, gọi `flush()`. Kỳ vọng `has` false.
  - `test_doi_cong_ty_khong_dung_cache_cong_ty_cu`: gọi `for(E,1)` rồi `for(E,2)` trong cùng tiến trình. Kỳ vọng `has('t.doc.update')` lần lượt true, false.
  - `test_legacy_names`: `for(E,1)->legacyNames('web')` === `['Xem tài liệu bộ phận','Xem tài liệu phòng']`.
- [ ] **Step 2:** Chạy `DB_DATABASE=hrm_erp_rbac_test $PHP vendor/bin/phpunit tests/Feature/Rbac/PermissionCheckerTest.php`. Kỳ vọng: FAIL (class chưa có).
- [ ] **Step 3:** Viết 2 class. Mỗi đối tượng truy vấn grants đúng 1 lần, alias tải 1 lần mỗi tiến trình, so tên bằng `===` trong PHP.
- [ ] **Step 4:** Chạy test. Kỳ vọng: 11 passed.
- [ ] **Step 5:** Commit `feat(rbac): PermissionChecker kiểm quyền theo mã và công ty`.

---

### Task 3: Danh mục quyền: định dạng, kiểm hợp lệ, đồng bộ (hrm-api)

**Files:**
- Create: `app/Support/Permissions/Catalog/` (thư mục, mỗi phân hệ một file `return [...]`)
- Create: `app/Support/Permissions/PermissionCatalog.php`
- Create: `app/Support/Permissions/CatalogSync.php`
- Create: `app/Console/Commands/PermissionCatalogSyncCommand.php` (`permission:catalog-sync {--dry-run}`)
- Test: `tests/Feature/Rbac/PermissionCatalogTest.php`, `tests/Feature/Rbac/CatalogSyncTest.php`

**Interfaces:**
- Produces:
  - `PermissionCatalog::load(?string $dir = null): array` (đọc mọi file, giữ thứ tự file theo tên rồi thứ tự trong file)
  - `PermissionCatalog::validate(array $entries): array` (mảng thông báo lỗi tiếng Việt, rỗng là hợp lệ, theo luật ở `./design.md` mục 4)
  - `CatalogSync::run(array $entries, bool $dryRun = false): array` (báo cáo `['inserted'=>[codes],'updated'=>[codes],'deprecated'=>[codes],'aliases'=>int]`, ném `RuntimeException` khi `validate` có lỗi)
  - `sort_order` = thứ tự trong danh mục. `on_erp`/`on_hrm` lấy từ `platforms`.
- Consumes: bảng của Task 1.

- [ ] **Step 1:** Viết test `PermissionCatalogTest`, mỗi luật một test, assert thông báo chứa mã bị lỗi:
  `test_ma_sai_dinh_dang`, `test_ma_trung`, `test_action_khong_duoc_co_scopes`, `test_scope_ngoai_1_4`,
  `test_min_scope_ngoai_scopes`, `test_depends_on_tro_ma_khong_co`, `test_ten_cu_thuoc_2_ma`,
  `test_platforms_rong`, `test_danh_muc_hop_le_khong_loi`.
- [ ] **Step 2:** Viết test `CatalogSyncTest`, dùng mã tiền tố `zz_test.`:
  - `test_them_moi_va_chay_lai_khong_doi_gi`: lần 2 có `inserted`/`updated`/`deprecated` rỗng.
  - `test_doi_ten_giu_id_va_luot_gan`: đổi `name`, id giữ nguyên, dòng `role_has_permissions` còn nguyên.
  - `test_bo_khoi_danh_muc_thi_ngung_khong_xoa`: dòng còn, `deprecated_at` khác null, lượt gán còn.
  - `test_alias_dung_lai_theo_legacy`: đổi `legacy` thì bảng alias đúng bộ mới.
  - `test_danh_muc_loi_thi_khong_ghi_gi`.
  - `test_dry_run_khong_ghi`.
- [ ] **Step 3:** Chạy cả 2 file test. Kỳ vọng: FAIL.
- [ ] **Step 4:** Viết `PermissionCatalog`, `CatalogSync` (một transaction) và command. Command in báo cáo, thoát với mã 1 khi có lỗi.
- [ ] **Step 5:** Chạy test. Kỳ vọng: 15 passed.
- [ ] **Step 6:** Commit `feat(rbac): danh mục quyền khai trong code + permission:catalog-sync`.

---

### Task 4: Gỡ cơ chế seeder cũ (hrm-api + ERP)

**Files:**
- Modify: `hrm-api/app/Console/Commands/` (lệnh `permission:sync`), `ERP/TanPhatDev/app/Console/Commands/PermissionSyncCommand.php`: `handle()` in "Đã chuyển sang `php artisan permission:catalog-sync` ở hrm-api (xem .plans/gop-db/quan-ly-vai-tro-quyen)" rồi `return 1`.
- Delete: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `ERP/TanPhatDev/database/seeds/PermissionsTableSeeder.php`, `permission_legacy_ids.php` ở cả 2 repo, `DeclaresPermissions.php` + `PermissionSync.php` ở cả 2 repo, `tests/Feature/PermissionSyncTest.php`. **Xoá ở bước này** vì Task 5 đã đọc chúng lúc sinh bản nháp. Bản trong git history là nguồn tra cứu.
- Modify: mọi chỗ gọi seeder này (`DatabaseSeeder`, `grep -rn PermissionsTableSeeder`), gỡ lời gọi.
- Modify: `HRM/.claude/skills/permission-seeder/SKILL.md`: thêm dòng đầu "ĐÃ THAY bằng danh mục quyền, xem .plans/gop-db/quan-ly-vai-tro-quyen".

**Thứ tự:** chạy **sau Task 6**, vì Task 5 và 6 còn đọc seeder cũ.

- [ ] **Step 1:** `grep -rn "PermissionsTableSeeder\|PermissionSync\|DeclaresPermissions" app Modules database tests` ở cả 2 repo. Mọi dòng kết quả phải nằm trong danh sách Modify/Delete ở trên. Dòng nào ngoài danh sách thì ghi lại và hỏi.
- [ ] **Step 2:** Sửa và xoá theo danh sách.
- [ ] **Step 3:** Ở mỗi repo, `$PHP artisan permission:sync; echo $?` in thông báo và ra `1`. `$PHP artisan list | grep catalog-sync` có ở hrm-api.
- [ ] **Step 4:** Commit ở mỗi repo `chore(rbac): gỡ seeder quyền cũ, trỏ sang permission:catalog-sync`.

---

### Task 5: Sinh bản nháp danh mục từ DB hiện tại (hrm-api)

**Files:**
- Create: `app/Support/Permissions/Draft/ScopeVariantDetector.php`
- Create: `app/Support/Permissions/Draft/CodeSuggester.php`
- Create: `app/Console/Commands/RbacDraftCatalogCommand.php` (`rbac:draft-catalog {--out=} {--diff}`)
- Test: `tests/Unit/Rbac/ScopeVariantDetectorTest.php`, `tests/Unit/Rbac/CodeSuggesterTest.php`

**Interfaces:**
- Produces:
  - `ScopeVariantDetector::detect(string $name, ?string $code): array` dạng `['base' => string, 'scope' => ?int, 'personal' => bool]`
  - `CodeSuggester::suggest(string $subsystemSlug, string $baseName, string $kind): string`
  - Lệnh ghi `Catalog/*.php` (nhóm theo `group_category` của ERP và `type` của HRM) và một file `catalog-review.csv`.
  - `--diff`: in các `(guard, tên)` có trong DB mà chưa có trong danh mục hiện tại.
- Consumes: `PermissionCatalog` (Task 3).

- [ ] **Step 1:** Viết test `ScopeVariantDetectorTest`, mỗi dòng một assert:
  - `'Hạch toán chi phí vận chuyển nhanh - Xem theo phòng ban'` ra `['base'=>'Hạch toán chi phí vận chuyển nhanh - Xem','scope'=>2,'personal'=>false]`
  - `'… - Xem theo tổng công ty'` ra scope 4; `'… theo công ty'` ra 3; `'… theo bộ phận'` ra 1
  - `'Xem tất cả báo giá'` ra `['base'=>'Xem báo giá','scope'=>4]`; `'Xem báo giá công ty'` ra 3; `'Xem báo giá phòng'` ra 2; `'Xem báo giá bộ phận'` ra 1
  - mã HRM đuôi `.view.all_company` ra 4; `.view.company` ra 3
  - `'Xem thống kê dashboard theo nhân viên'` ra `personal=true`
  - `'Xem báo giá'` ra `scope=null`
  - **`'Báo cáo công nợ công ty con'` ra `scope=null`** (chữ "công ty" nằm giữa tên, không phải đuôi phạm vi)
- [ ] **Step 2:** Viết test `CodeSuggesterTest`:
  - `suggest('sale','Xem báo giá','view')` === `'sale.bao_gia.view'`
  - `suggest('sale','Duyệt báo giá','approve')` === `'sale.bao_gia.approve'`
  - bỏ dấu tiếng Việt, `đ` thành `d`
- [ ] **Step 3:** Chạy. Kỳ vọng: FAIL.
- [ ] **Step 4:** Viết 2 class và lệnh. Ghép cặp ERP/HRM khi `base` trùng **từng byte**. Mỗi entry nháp ghi `legacy` đủ mọi biến thể.
- [ ] **Step 5:** Chạy test. Kỳ vọng: passed. Chạy `DB_DATABASE=hrm_erp_rbac_test $PHP artisan rbac:draft-catalog --out=storage/app/rbac-draft`. Kỳ vọng: `PermissionCatalog::validate` trên bản nháp ra 0 lỗi, và tổng số `legacy` bằng số dòng `permissions` (1862 trên DB local).
- [ ] **Step 6:** Commit `feat(rbac): rbac:draft-catalog sinh bản nháp danh mục`.

---

### Task 6: Hoàn thiện danh mục + user duyệt (tài liệu, có cổng user)

**Files:**
- Create/Modify: `hrm-api/app/Support/Permissions/Catalog/*.php` (từ bản nháp)
- Create: `.plans/gop-db/quan-ly-vai-tro-quyen/gd1-nen-du-lieu/doi-chieu-quyen.xlsx`, mỗi dòng: tên cũ · guard · mã mới · phạm vi · Nhóm phân hệ · Phân hệ · Chức năng · loại · nền tảng · ghi chú. Sheet riêng cho: cặp ERP/HRM đã ghép, quyền "… của mình" bị bỏ, quyền Xem không có biến thể (mục 7)
- Create: `.plans/gop-db/quan-ly-vai-tro-quyen/gd1-nen-du-lieu/scope-decisions.csv` (`ma,ten_cu,guard,pham_vi`). User điền cột `pham_vi`
- Test: `tests/Feature/Rbac/CatalogContentTest.php`

- [ ] **Step 1:** Viết `CatalogContentTest`:
  - `test_danh_muc_that_hop_le`: `validate(load())` === [].
  - `test_moi_quyen_cu_deu_co_dich`: mọi `(guard_name, name)` trong `bak_rbac_permissions`, hoặc `permissions` khi chưa chuyển đổi, đều nằm trong `legacy` của đúng một entry. Lỗi thì in danh sách thiếu.
  - `test_quyen_cu_khong_co_trong_danh_muc_thi_dung`: thêm 1 quyền giả vào DB rồi kiểm. Kỳ vọng test trên báo đúng tên đó.
- [ ] **Step 2:** Đi từng phân hệ, sửa mã gợi ý thành mã có nghĩa theo mục 5.3 của design tổng. Sửa Nhóm phân hệ, Phân hệ, Chức năng theo menu thật (`components/subsystems.js`, `components/subsystem-menu/*.js`, menu ERP). Không tự đặt nhãn, theo memory `mockup-khong-tu-dat-nhan-danh-muc`. Mỗi phân hệ xong thì chạy `CatalogContentTest`.
- [ ] **Step 3:** Xuất `doi-chieu-quyen.xlsx` và `scope-decisions.csv`. **Dừng, đưa user duyệt:**
  - các cặp ghép ERP/HRM;
  - danh sách quyền "… của mình" bị bỏ;
  - điền phạm vi cho từng dòng trong `scope-decisions.csv`.

  Chưa duyệt thì không sang Task 7.
- [ ] **Step 4:** Sửa danh mục theo ý user. Chạy `CatalogContentTest`. Kỳ vọng: 3 passed.
- [ ] **Step 5:** Commit `feat(rbac): danh mục quyền ERP + HRM (đã duyệt)`.

---

### Task 7: `rbac:convert`: nhập quyền + tách vai trò (hrm-api)

**Files:**
- Create: `app/Support/Permissions/Convert/PermissionMerger.php`
- Create: `app/Support/Permissions/Convert/RoleSplitter.php`
- Create: `app/Support/Permissions/Convert/WorkingCompanyBackfill.php`
- Create: `app/Console/Commands/RbacConvertCommand.php` (`rbac:convert {--dry-run} {--report-dir=} {--scope-decisions=}`)
- Test: `tests/Feature/Rbac/PermissionMergerTest.php`, `tests/Feature/Rbac/RoleSplitterTest.php`

**Interfaces:**
- Consumes: `PermissionCatalog::load()`, `CatalogSync::run()` (Task 3); `scope-decisions.csv` (Task 6).
- Produces:
  - `PermissionMerger::run(array $catalog, array $scopeDecisions): array` trả `['kept'=>[code=>id], 'merged'=>int, 'dropped_personal'=>[names], 'missing'=>[[guard,name]]]`. Ném `RuntimeException` khi `missing` khác rỗng.
  - `RoleSplitter::run(): array` trả `['map'=>[[old_role_id, company_id, new_role_id]], 'conflicts'=>[...], 'skipped'=>[role_ids], 'inactive_granting'=>[role_ids]]`. Ghi `rbac_role_map`.
  - `WorkingCompanyBackfill::run(): array` trả `['added'=>[[employee_id, company_id]]]`.
  - Command chạy theo thứ tự ở `./design.md` mục 5 (bước 1, 3, 4, 5, 7). Bước 2, 6, 8 nối ở Task 8–9.
  - Sau `RoleSplitter`: dựng lại `role_has_permissions` / `employee_has_roles` theo mục 2.5–2.6; `roles.company_id` NOT NULL + unique `(company_id, base_name)`; `guard_name='api'` cho mọi dòng `roles`/`permissions`; xoá cache spatie.

- [ ] **Step 1:** Viết `PermissionMergerTest`. Fixture: quyền `web 'Xem T bộ phận'`, `web 'Xem T phòng'`, `api 'Xem T'`. Catalog `zz.t.view` scopes [1,2,3,4], legacy cả 3 (`api` có min null). Vai trò X (rhp công ty 1) có cả 2 quyền web.
  - `test_gop_bien_the_giu_mot_id`: còn đúng 1 dòng `permissions` có code `zz.t.view`, id = id dòng `api`.
  - `test_luot_gan_lay_pham_vi_lon_nhat`: X có `zz.t.view` scope 2.
  - `test_quyen_ca_nhan_bi_bo`: legacy `web 'Xem T theo nhân viên'` (personal) không còn dòng nào trỏ, có tên trong `dropped_personal`.
  - `test_quyen_xem_khong_bien_the_lay_theo_quyet_dinh`: vai trò Y chỉ có `api 'Xem T'`, decisions `zz.t.view = 3`. Kỳ vọng Y scope 3.
  - `test_thieu_quyet_dinh_pham_vi_thi_dung`: decisions rỗng thì ném lỗi, thông báo có `'Xem T'`.
- [ ] **Step 2:** Viết `RoleSplitterTest`. Fixture: role R tên `Kế toán`, rhp ở công ty 1 (quyền A, B) và công ty 4 (quyền A). ehr: E1 ở 1, E2 ở 1, E3 ở 4. `company_roles` (R,1), (R,4).
  - `test_tach_moi_cong_ty_mot_vai_tro`: có 2 vai trò, `company_id` 1 và 4.
  - `test_cong_ty_nhieu_luot_gan_giu_id_cu`: vai trò công ty 1 có id = R.
  - `test_ten_co_tien_to`: tên `TPE_Kế toán` và `TPSG_Kế toán`, `base_name` = `Kế toán`.
  - `test_quyen_va_nguoi_dung_theo_dung_cong_ty`: vai trò công ty 4 có đúng quyền A và đúng người E3.
  - `test_trung_ten_trong_cong_ty_them_hau_to`: có sẵn vai trò công ty 1 `base_name='Kế toán'`. Kỳ vọng vai trò tách ra thành `Kế toán (2)`, có trong `conflicts`.
  - `test_role_khong_cong_ty_khong_chuyen`: role Z không có dòng nào thì nằm trong `skipped`, không lỗi.
  - `test_role_tron_2_guard_gop_mot`: R có cả quyền web lẫn api ở công ty 1, ra 1 vai trò mang đủ cả hai.
  - `test_super_admin_du_ma`: role `Super Admin` có đủ mọi code trong catalog, scope = max `allowed_scopes`. Role `Super admin (DNS DÙNG)` không được thêm mã.
- [ ] **Step 3:** Chạy cả 2 file. Kỳ vọng: FAIL.
- [ ] **Step 4:** Viết 3 class và command. Mỗi bước ghi số liệu ra `--report-dir`. `--dry-run` bọc transaction và rollback, bỏ qua bước sao lưu DDL. Chặn chạy lần 2 khi `rbac_role_map` đã có dữ liệu.
- [ ] **Step 5:** Chạy test. Kỳ vọng: 13 passed.
- [ ] **Step 6:** Commit `feat(rbac): rbac:convert nhập quyền theo danh mục, tách vai trò theo công ty`.

---

### Task 8: Chụp mốc + báo cáo chênh lệch (hrm-api)

**Files:**
- Create: `app/Support/Permissions/Convert/EffectiveSnapshot.php`
- Create: `app/Support/Permissions/Convert/SnapshotDiff.php`
- Modify: `app/Console/Commands/RbacConvertCommand.php` (bước 2 và 8)
- Test: `tests/Feature/Rbac/SnapshotDiffTest.php`

**Interfaces:**
- Produces:
  - `EffectiveSnapshot::beforeStrict(): array` và `beforeActual(): array`. Mỗi phần tử là `"employee|company|guard|tên cũ"`.
    - `beforeStrict` theo SQL của `canInCompany` (ERP `app/Employee.php:1492`) cho guard web, và tương đương cho api.
    - `beforeActual` tái hiện HRM `getPermissionsViaRoles` (vai trò HRM không lọc công ty, quyền không lọc `company_id`) và ERP `hasAnyPermission` (`app/Employee.php:1456`).
  - `EffectiveSnapshot::after(): array` lấy từ `PermissionChecker::legacyNames` cho mọi cặp trong `company_employees`.
  - `SnapshotDiff::classify(array $strict, array $actual, array $after, array $context): array` trả các khoá đúng tên file báo cáo ở `./design.md` mục 5.8 (bỏ đuôi `.csv`).
  - `$context` = `['platform_pairs'=>…, 'super_admin_employees'=>…, 'scope_decisions'=>…]`.

- [ ] **Step 1:** Viết test với mảng tay, không cần DB:
  - `test_mat_do_bit_ro`: actual có X, strict không có X. Kỳ vọng X vào `mat-do-bit-ro`.
  - `test_them_do_gop_nen_tang`: after có tên `api` mà strict chỉ có tên `web` cùng mã. Kỳ vọng vào `them-do-gop-nen-tang`.
  - `test_them_do_cap_cao_bao_cap_thap`: strict có "phòng", after có thêm "bộ phận". Kỳ vọng vào `them-do-cap-cao-bao-cap-thap`.
  - `test_them_do_super_admin`.
  - `test_chenh_lech_khac`: after mất một tên có ở strict mà không thuộc nhóm nào. Kỳ vọng vào `chenh-lech-khac`.
  - `test_khong_doi_thi_moi_nhom_rong`.
- [ ] **Step 2:** Chạy. Kỳ vọng: FAIL.
- [ ] **Step 3:** Viết. Command ghi mỗi khoá thành một CSV. **Thoát với mã 2 khi `chenh-lech-khac` khác rỗng** (dry-run vẫn ghi báo cáo). Ghi thêm `thieu-quyen-xem.csv`: vai trò có mã `action` mà thiếu mã trong `depends_on`.
- [ ] **Step 4:** Chạy test. Kỳ vọng: 6 passed.
- [ ] **Step 5:** Commit `feat(rbac): báo cáo chênh lệch quyền trước/sau chuyển đổi`.

---

### Task 9: Dò và chuyển hướng dữ liệu trỏ role id / tên quyền (hrm-api)

**Files:**
- Create: `app/Support/Permissions/Convert/RoleReferenceRemap.php`
- Create: `app/Support/Permissions/Convert/role-references.php`, danh sách `[table, column, company_column]` đã dò
- Test: `tests/Feature/Rbac/RoleReferenceRemapTest.php`

- [ ] **Step 1:** Dò. Chạy `SELECT TABLE_NAME, COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='hrm_erp_rbac_test' AND (COLUMN_NAME LIKE '%role%' OR COLUMN_NAME LIKE '%permission%')`, rồi `grep -rn "role_id\|roles\.id\|permission_name\|'permission'"` ở `app Modules` (hrm-api) và `app` (ERP), kèm cột JSON/text chứa tên quyền (ví dụ cấu hình người nhận thông báo theo quyền).
  - Bỏ qua `project_roles`, `payroll_roles`, `roles2` (khác khái niệm), sau khi xác nhận bằng đọc model.
  - Ghi kết quả vào `role-references.php` và `du-lieu-tro-role-id.csv`.
  - Kiểm thêm **nơi dùng ngoài 3 repo** (`TPE_APP`, SSO, `HELP`) có đọc claim JWT `roles`/`permissions` hay tên vai trò/quyền không: `grep -rn "permissions\|roles" TPE_APP/lib`, đọc chỗ khớp. Có thì ghi vào `du-lieu-tro-role-id.csv` mục "ngoài repo" và báo user.
- [ ] **Step 2:** Viết test:
  - `test_tro_sang_vai_tro_dung_cong_ty`: bảng giả `zz_steps(role_id, company_id)` có (R,4). Sau remap thành (R_tpsg, 4).
  - `test_khong_xac_dinh_duoc_cong_ty_thi_liet_ke`: dòng không có cột công ty thì không sửa, nằm trong báo cáo.
  - `test_ten_quyen_luu_trong_du_lieu_doi_sang_ma`: cột text chứa tên cũ thì đổi sang mã qua alias.
- [ ] **Step 3:** Chạy. Kỳ vọng: FAIL. Viết class, nối vào `RbacConvertCommand` ở bước 6. Chạy lại. Kỳ vọng: 3 passed.
- [ ] **Step 4:** Commit `feat(rbac): chuyển hướng dữ liệu trỏ vai trò cũ`.

---

### Task 10: Nối các đường kiểm quyền hrm-api vào `PermissionChecker`

**Files:**
- Modify: `app/Helper/PermissionHelper.php:20` (`isCurrentEmployeeHasPermission`), `app/CommonServices/PermissionService.php:20`, `app/Models/BaseModel.php:204`, `app/Http/Controllers/ApiController.php:159`. Cả 4 thành `PermissionChecker::for(auth id, current_company_role)->hasLegacy($permission, 'api')`.
- Modify: `app/Http/Middleware/CheckPermission.php`: mỗi tên trong `explode('|')` qua `hasLegacy(…,'api')`.
- Modify: `Modules/Timesheet/Entities/Employee.php`:
  - `roles()` ghi đè thành `belongsToMany` không lọc morph;
  - `permissionRoles($companyId)` = vai trò có `roles.company_id = $companyId`;
  - `manageCompanyIds()` = `company_employees`;
  - `getAllPermissions()` / `getPermissionsViaRoles()` trả `Collection` các `Fluent(['name'=>tên cũ api,'code'=>…])` từ `legacyNames('api')`. Đọc 69 chỗ gọi, chỗ nào dùng thuộc tính khác `name` thì ghi lại và xử lý riêng.
- Modify: `app/Http/Controllers/Api/AuthNewController.php` (khoảng dòng 413 và 460, 2 bản truy vấn profile): `permissions` trả danh sách `{name, code}` từ checker, để FE `hasAPermission` vẫn chạy.
- Modify: `app/Models/Role.php` (`syncPermissionsByCompany`): ném `LogicException('Đã thay bằng màn Vai trò mới (giai đoạn 2)')`.
- Test: `tests/Feature/Rbac/HrmGateTest.php`

- [ ] **Step 1:** Viết test. Fixture: người E làm ở công ty 1 và 2, vai trò công ty 1 có mã với alias `api 'Zz quyền A'`.
  Gọi qua `actingAs` + `current_company_role`:
  - `test_helper_co_quyen_cong_ty_1`: `isCurrentEmployeeHasPermission('Zz quyền A')` true.
  - `test_helper_khong_quyen`: tên khác thì false.
  - `test_helper_cong_ty_2_khong_lot`: đổi `current_company_role=2` thì false. Ca này đỏ trên code cũ của `BaseModel`.
  - `test_middleware_403_o_cong_ty_khac`: route giả `checkPermission:Zz quyền A` trả 403 ở công ty 2, 200 ở công ty 1.
  - `test_base_model_va_api_controller_cung_ket_qua`: cả 4 bản helper ra cùng kết quả ở cả 2 công ty.
  - `test_profile_tra_ten_cu_va_ma`: API profile có `{name:'Zz quyền A', code:…}` ở công ty 1, không có ở công ty 2.
  - `test_manage_company_ids_theo_company_employees`.
- [ ] **Step 2:** Chạy. Kỳ vọng: FAIL (ít nhất ca công ty 2 và profile).
- [ ] **Step 3:** Sửa theo danh sách file.
- [ ] **Step 4:** Chạy test. Kỳ vọng: 7 passed. Chạy thêm `tests/Feature/PermissionHolderAcrossCompanyTest.php` và các test có chữ `permission` (`grep -rl` trong `tests Modules/*/Tests`). Mọi test cũ còn đỏ thì ghi tên và lý do (giả định công ty trên dòng quyền), sửa fixture cho đúng mô hình mới. Không xoá test.
- [ ] **Step 5:** Commit `feat(rbac): hrm-api kiểm quyền qua PermissionChecker, lọc công ty mọi đường`.

---

### Task 11: Nối các đường kiểm quyền ERP vào `PermissionChecker`

**Files:**
- Create: `ERP/TanPhatDev/app/Support/Permissions/PermissionChecker.php`, `PermissionScope.php`. Chép **nguyên byte** từ hrm-api, kiểm bằng `cmp`.
- Modify: `app/Employee.php`:
  - `can()` (`:1442`), `hasAnyPermission()` (`:1456`), `canInCompany()` (`:1492`) và `hasPermissionTo()`/`checkPermissionTo()` (ghi đè thêm) thành `PermissionChecker::for($this->id, $companyId)->hasLegacy($name, 'web')`. `$companyId` = tham số của `canInCompany`, mặc định `$this->info->company_id`;
  - `hasRole()` (`:1377`): so `roles.base_name` thay cho `name`. **Giữ** nhánh Super Admin (gỡ ở giai đoạn 3);
  - `getJWTCustomClaims()` (`:533`): `permissions` = `legacyNames('web')`, `roles` = danh sách `base_name`;
  - `getAllPermissions()` ghi đè giống Task 10 với guard `web`.
- Modify: `app/Providers/AuthServiceProvider.php:28`: gỡ `Gate::before`.
- Modify: `app/Model/Common/Role.php:143` (`syncPermissionsByCompany`): ném `LogicException` như Task 10.
- Test: `ERP/TanPhatDev/tests/Feature/Rbac/ErpGateTest.php` (chạy với `DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test`, vì `phpunit.xml` mặc định dùng sqlite)

- [ ] **Step 1:** Viết test với fixture như Task 10, alias guard `web`:
  - `test_can_co_quyen`, `test_can_khong_quyen`, `test_can_cong_ty_khac_khong_lot` (ca này đỏ trên `hasAnyPermission` cũ);
  - `test_can_in_company_tham_so_cong_ty`;
  - `test_middleware_check_permission_403`;
  - `test_super_admin_khong_con_bypass_gate`: người chỉ có vai trò `Super Admin` mà vai trò thiếu mã M thì `can('tên cũ của M')` false;
  - `test_has_role_khop_base_name`: vai trò `TPE_Kế toán` thì `hasRole('Kế toán')` true;
  - `test_jwt_claim_ten_cu`.
- [ ] **Step 2:** `cd ../wt-rbac/TanPhatDev && DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test $PHP vendor/bin/phpunit tests/Feature/Rbac/ErpGateTest.php`. Kỳ vọng: FAIL.
- [ ] **Step 3:** Sửa theo danh sách file. `cmp` hai bản checker phải ra không khác.
- [ ] **Step 4:** Chạy test. Kỳ vọng: 8 passed. Chạy toàn bộ `tests/` của ERP, ghi lại test đỏ mới (so với lần chạy trên `gop_db`).
- [ ] **Step 5:** Commit ở ERP `feat(rbac): ERP kiểm quyền qua PermissionChecker, gỡ Gate::before Super Admin`.

---

### Task 12: Diễn tập trên bản sao prod + soát tay trên trình duyệt

- [ ] **Step 1:** Hỏi user, nêu phạm vi: lấy bản sao DB prod mới nhất thành `hrm_erp_rbac_rehearsal`, chạy mọi migration `gop_db` còn chờ rồi 5 migration Task 1 (`2026_11_01_000001`…`000005`) bằng `--path` — xem `runbook-go-live.md`, rồi `rbac:convert --dry-run`, rồi `rbac:convert`. Chờ câu "làm".
- [ ] **Step 2:** `$PHP artisan rbac:convert --dry-run --report-dir=storage/app/rbac-convert/<ngày> --scope-decisions=<đường dẫn csv>`. Kỳ vọng: `chenh-lech-khac.csv` chỉ có dòng tiêu đề, mã thoát 0.
- [ ] **Step 3:** Chạy thật. Chép toàn bộ CSV vào `.plans/.../gd1-nen-du-lieu/bao-cao-dien-tap/`. Đưa user xem `mat-do-bit-ro.csv`, `them-do-*.csv`, `thieu-quyen-xem.csv`, `trung-ten-vai-tro.csv`, `vai-tro-khong-chuyen.csv`, `vai-tro-ngung-van-cap-quyen.csv`, `du-lieu-tro-role-id.csv`.
- [ ] **Step 4:** Trỏ HRM (api + client) và ERP local vào DB diễn tập. Dùng Playwright đăng nhập 3 tài khoản: một người 1 công ty, một người 2 công ty, một Super Admin.
  - Với mỗi tài khoản, đếm số mục menu hiện ra và số nút thao tác trên 3 màn (báo giá, hàng hoá, chấm công), đo bằng số phần tử trong DOM.
  - So với cùng tài khoản trên DB local chưa chuyển đổi. Chênh lệch phải khớp báo cáo CSV.
  - Ghi số đo vào `bao-cao-dien-tap/playwright.md`.
- [ ] **Step 5:** Cập nhật bảng trạng thái giai đoạn 1 trong `../design.md`.

---

## Bảng trạng thái

| Task | Trạng thái |
|---|---|
| 0 Môi trường | chưa |
| 1 Schema | chưa |
| 2 Checker | chưa |
| 3 Danh mục + sync | chưa |
| 5 Bản nháp | chưa |
| 6 Danh mục duyệt (cổng user) | chưa |
| 4 Gỡ seeder cũ | chưa |
| 7 Convert: quyền + vai trò | chưa |
| 8 Báo cáo chênh lệch | chưa |
| 9 Dữ liệu trỏ role id | chưa |
| 10 Nối hrm-api | chưa |
| 11 Nối ERP | chưa |
| 12 Diễn tập | chưa |

Thứ tự chạy: 0 → 1 → 2 → 3 → 5 → 6 → 4 → 7 → 8 → 9 → 10 → 11 → 12.
