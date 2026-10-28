# Bảng giá bán hàng hoá hiện hành — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> Người phụ trách: @dnsnamdang · Repo: `hrm-api` + `hrm-client`, nhánh `gop_db` (hoặc nhánh con checkout từ `gop_db` — hỏi user lúc bắt đầu)
> ⛔ **Chưa được phép code.** Duyệt plan ≠ lệnh code. Trước Task 1 phải hỏi riêng: repo · nhánh · file sẽ đụng · có chạy seeder vào DB nào không — chờ câu "làm".
> ⛔ Không commit / push — user tự báo (memory `khong-hoi-commit-user-tu-bao`). Các bước "Checkpoint" chỉ là điểm dừng kiểm.

**Goal:** Màn chỉ-đọc "Bảng giá bán hiện hành" (Tài chính › Quản lý giá - CTKM › Giá bán) liệt kê hàng Đang kinh doanh của 1 công ty với 6 loại giá đang áp dụng, giá sắp áp dụng, giá vốn (có quyền), kèm In / Xuất Excel.

**Architecture:** BE thêm service đọc riêng `ProductPriceBoardService` (KHÔNG sửa `ProductPriceListService` dùng chung — chỉ gọi lại `ProductPriceSql` + copy điều kiện lọc), controller + 4 route `product-price-board`. FE thêm 1 page dựng trên `V2BaseSmartFilterPanel` + `V2BaseDataTable` + `columnCustomizationMixin` + `exportFieldsMixin` + `reportPrintPreviewMixin`; mở rộng `export-fields-modal.vue` bằng 1 slot + 2 prop (user đã duyệt phương án 1).

**Tech Stack:** Laravel 8 / PHP 7.4 (Modules/MasterData), PHPUnit; Nuxt 2 / Vue 2, Bootstrap-Vue, ExcelJS (qua `utils/export/listExportFile.js`), Playwright.

**Spec:** `docs/superpowers/specs/gop-db/2026-10-28-bang-gia-ban-hien-hanh-design.md` · Tóm tắt + quyết định: `design.md` (cùng thư mục) · **Mockup chốt:** `mockup-bang-gia.html` (cùng thư mục — đọc ghi chú đầu file).

## Global Constraints

- Hàng: chỉ `product_company_coefficients.status = 3` (`ProductCompany::STATUS_TRADING`) tại công ty xem, `products.status <> 0` (`Product::STATUS_DELETED`).
- Thứ tự loại giá: `[1, 5, 2, 3, 4, 6]` = Bán lẻ · Giá bán theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · TMĐT (lấy `ProductPriceListService::TYPE_ORDER`, không chép số).
- **Giá ≤ 1 đ = chưa có giá** ⇒ trả `null`, ô trống; áp cho giá đang áp dụng, giá sắp áp dụng, sort, lọc, in, Excel.
- Giá sắp áp dụng: `product_expected_prices.status = 2`, `effect_date > CURDATE()`, `(flag IS NULL OR flag <> 1)`, `price > 1`; nhiều bản ⇒ lấy `effect_date` sớm nhất.
- Giá đang áp dụng = giá đang chạy, KHÔNG phải giá đề xuất chờ duyệt (tra `ProductPriceListService::priceRow` để lấy đúng cột).
- Quyền (tên chính xác): `Xem bảng giá bán theo tổng công ty` · `In/Xuất Excel bảng giá bán` (mới, `group 'Hàng hoá'`, `type 8`) · `Xem giá vốn hàng hoá` (có sẵn) — **xét TẠI CÔNG TY ĐANG XEM**, không dùng `isCurrentEmployeeHasPermission` nguyên trạng.
- Không có quyền giá vốn ⇒ `cost_price = null` ở MỌI endpoint, `cost` bị bỏ khỏi whitelist sort + fields.
- Số: FE `toLocaleString('en-US')`, BE trả số thuần; Excel ô số thật `#,##0`, ngày `dd/mm/yyyy`.
- Dòng phụ giá sắp áp dụng: chữ `#2563EB`, `→ {giá} · {dd/mm/yyyy}` (icon `ri-arrow-right-line`). KHÔNG đỏ.
- Không migration, không seeder ngoài 2 dòng quyền. Không cột Người tạo/Ngày tạo. Cột mặc định hiện đủ.
- Menu: không `isShow`, không key ẩn ở Cài đặt phân hệ (deploy hiện ngay).
- Mọi phần tử form FE dùng `V2Base*`; nút cách nhau 12px; nút không dùng được thì ẨN (không disable) — riêng nút "Xuất file" trong popup chung giữ hành vi sẵn có.

## Review Focus

1. **Xem công ty khác khi quyền giá vốn chỉ có ở công ty đang làm** ⇒ cột Giá vốn phải biến mất (BE `null`, FE ẩn cột + bỏ khỏi popup) — ca `test_cost_permission_checked_at_viewed_company` (Task 1) + Playwright Task 4/6.
2. **Hàng có ĐVT phụ nhưng ĐVT cơ bản thiếu dòng giá / giá ≤ 1** ⇒ sort theo giá vẫn chạy, hàng đó xếp cuối cả 2 chiều — ca `test_sort_price_nulls_last_both_directions` (Task 1).
3. **Đổi công ty khi đang lọc catalog** ⇒ 4 ô catalog reset, options nạp lại theo công ty mới, không lọc nhầm catalog công ty cũ — ca `test_catalog_filter_uses_viewed_company` (Task 1) + bước Playwright Task 4.
4. **Danh sách in vượt trần 2.000 dòng** ⇒ không in, hiện câu nhắc thu hẹp bộ lọc (khuôn `LimitsPrintListRows`) — ca `test_print_list_data_over_limit_returns_notice_payload` (Task 2).
5. **Màn khác đang dùng `export-fields-modal`** không truyền slot/prop mới ⇒ y như cũ (tiêu đề, nút "Xuất file", không có vùng tuỳ chọn) — bước Playwright đo `/assign/customers` (Task 3).

---

## Phase 1 — Backend (hrm-api)

### Task 1: Quyền mới + service đọc + endpoint danh sách & form-options

**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — 2 dòng `$this->perm([...])` ngay sau dòng `Duyệt giá bán hàng hoá` (~dòng 1679), theo `.claude/skills/permission-seeder/SKILL.md` (không `id`, không `guard_name`).
- Create: `Modules/MasterData/Services/ProductPrice/ProductPriceBoardService.php`
- Create: `Modules/MasterData/Http/Controllers/V1/Product/ProductPriceBoardController.php`
- Create: `Modules/MasterData/Transformers/ProductPrice/ProductPriceBoardResource.php` (hoặc map trong service — theo khuôn `ProductPriceController@index`)
- Modify: `Modules/MasterData/Routes/api.php` — group `product-price-board` đặt ngay sau group `product-prices` (~dòng 313), KHÔNG middleware quyền ở group.
- Test: `Modules/MasterData/Tests/Feature/ProductPriceBoardApiTest.php` (khuôn `ProductPriceScreenApiTest.php`: `DatabaseTransactions` + `Concerns\ActsAsProductUser` + `Concerns\BuildsCompanyPrices`)
- Modify (test helper): `Modules/MasterData/Tests/Feature/Concerns/ActsAsProductUser.php` — thêm `grantAt(int $employeeId, int $companyId, array $permissions): void` (role tạm + `employee_has_roles.company_id` + `role_has_permissions.company_id` = `$companyId`, xoá cache spatie + `RequestCache::flush()`).

**Interfaces:**
- Produces (dùng ở Task 2):
  - `ProductPriceBoardService::resolveCompanyId(Request $r): int` — không truyền ⇒ `current_company_role`; khác công ty đang làm mà thiếu quyền tổng công ty ⇒ `abort(403)`.
  - `ProductPriceBoardService::canViewCost(int $companyId): bool` — quyền `Xem giá vốn hàng hoá` qua `Employee::permissionRoles($companyId)` + `role_has_permissions.company_id = $companyId` + guard `api` (chép truy vấn của `PermissionService::isCurrentEmployeeHasPermission`, thay công ty; KHÔNG sửa `PermissionService`).
  - `ProductPriceBoardService::query(Request $r, int $companyId, bool $canCost): Builder` — base + bộ lọc + sort, 1 dòng/hàng.
  - `ProductPriceBoardService::units(array $productIds, int $companyId, bool $canCost): array` — `[productId => [ ['id','name','is_base','cost_price','prices' => [['type_id','price','next_price','next_date'], …×6]] ]]`.
  - `ProductPriceBoardService::paginate(Request $r): LengthAwarePaginator` (per_page mặc định 20, trần 50).
  - `ProductPriceBoardService::formOptions(Request $r): array` — `{companies (chỉ khi có quyền tổng công ty, [{id, code, name}]), manufacturers, brands, product_types (path 4 cấp như ProductListPage), catalog: {business_scopes, chapters, job_groups, job_clusters} của công ty xem, can_view_cost, can_view_all, can_export, company: {id, code, name}}`.
  - Response `GET /api/v1/master-data/product-price-board`: `data[]` = `{id, code, name, manufacture_name, brand_name, model_name, units[]}`, `meta` = phân trang + `{company: {id, code, name}, can_view_cost}`.
- Tham số lọc: `company_id, keyword, manufacture_id, brand_id, model_id, product_nature_id, product_function_group_id, product_family_id, product_type_id, business_scope_id, chapter_id, job_group_id, job_cluster_id, only_next (0|1), sort_by, sort_desc`.
- Sort whitelist: `code, name, manufacture, brand, model, cost` (chỉ khi `canCost`), `price_1, price_5, price_2, price_3, price_4, price_6` — giá theo ĐVT cơ bản (`product_units.is_base = 1`) của công ty xem; giá ≤ 1 coi NULL; NULL luôn cuối (`ORDER BY x IS NULL, x {dir}`). Mặc định `code asc`.

- [x] **Step 1: Khai 2 quyền trong seeder** (`'Xem bảng giá bán theo tổng công ty'`, `'In/Xuất Excel bảng giá bán'`; `group 'Hàng hoá'`, `type 8`). Xem trước: `php artisan permission:sync --dry-run` ⇒ chỉ báo thêm đúng 2 quyền. **Không chạy seeder vào DB** khi chưa hỏi (memory `hrm-them-permission-moi`: DB local lệch thì chèn tay 1 dòng/quyền — hỏi user).
- [x] **Step 2: Viết test fail** trong `ProductPriceBoardApiTest` — fixture: hàng P1 chủ A, ĐVT gốc + phụ ×10, bộ giá A (Bán lẻ 1,000,000, giảm 1,000 mỗi loại) + B (2,000,000); hàng P2 Đang kinh doanh ở A có Bán lẻ = 1; hàng P3 ở A trạng thái khác 3; giá sắp áp dụng P1/A Bán lẻ 1,100,000 `effect_date` = mai, 1 bản `flag = 1`, 1 bản `price = 1` ngày 31/12, 1 bản `status = 3`. Các ca:
  - `test_lists_only_trading_products_of_current_company` — có P1, P2; không P3; P1 Bán lẻ ĐVT gốc = 1000000.
  - `test_price_le_one_is_null` — P2 Bán lẻ `price === null`.
  - `test_next_price_rules` — P1/A Bán lẻ `next_price = 1100000`, `next_date = mai`; các bản flag 1 / giá 1 / status 3 không lọt.
  - `test_only_next_filter` — `only_next=1` ⇒ chỉ P1; hàng chỉ có lịch 1 đ không lọt.
  - `test_other_company_without_view_all_is_403` / `test_other_company_with_view_all_returns_company_prices` (B ⇒ Bán lẻ 2000000, `meta.company.id = B`).
  - `test_cost_hidden_without_permission` — `cost_price === null`, `meta.can_view_cost = false`, `sort_by=cost` bị bỏ qua (thứ tự = mặc định `code`).
  - `test_cost_permission_checked_at_viewed_company` — có giá vốn ở A (`actAs`), có tổng công ty, xem B ⇒ `null`; `grantAt(B, giá vốn)` ⇒ xem B ra 1600000.
  - `test_sort_price_nulls_last_both_directions` — `sort_by=price_1` asc và desc: P2 (giá 1 ⇒ null) đều đứng cuối.
  - `test_catalog_filter_uses_viewed_company` — xếp P1 vào tiểu mục X **chỉ ở A**; xem B lọc `job_cluster_id = X` ⇒ rỗng; xem A ⇒ có P1.
  - `test_form_options_hides_companies_without_view_all`.
- [x] **Step 3: Chạy test, phải FAIL** — `cd hrm-api && vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductPriceBoardApiTest.php` ⇒ FAIL (route 404).
- [x] **Step 4: Cài service + controller + route + resource** theo Interfaces. Giá/giá vốn đọc qua `ProductPriceSql::joinPrices` / `joinCompanyUnits`; điều kiện lọc phân loại + keyword + hãng/thương hiệu copy từ `ProductPriceListService` (KHÔNG gọi/đổi nó); catalog copy điều kiện `businessCatalogs` (lọc `company_id` = công ty xem) từ `ProductService`; Model lọc `products.model_id`. Eager load / 1 query cho `units()` (không N+1).
- [x] **Step 5: Chạy lại, phải PASS** cùng lệnh trên ⇒ OK. Chạy thêm `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductPriceScreenApiTest.php` ⇒ vẫn xanh (không đụng màn Cập nhật giá).
- [x] **Step 6: Đo hiệu năng** trên DB local, công ty nhiều hàng nhất: `GET /product-price-board?per_page=50` < 2s, `sort_by=price_1` < 2s, `only_next=1` < 2s. Chậm ⇒ `EXPLAIN`, nêu index thiếu cho user (KHÔNG tự thêm migration).

### Task 2: Export-rows + bản in theo bộ lọc

**Files:**
- Modify: `ProductPriceBoardService.php` — thêm `exportRows(Request $r): array`, `printListData(Request $r): array`.
- Modify: `ProductPriceBoardController.php` — `exportRows`, `printListData`.
- Modify: `Modules/MasterData/Routes/api.php` — `GET export-rows`, `GET print-list-data`, cả 2 `->middleware('checkPermission:In/Xuất Excel bảng giá bán')`.
- Create: `Modules/MasterData/Resources/views/prints/product-price-board.blade.php` (A4 ngang, khung giấy theo `.claude/skills/print-page/SKILL.md`; KHÔNG dùng `report_templates` vì cần chèn dòng DB).
- Test: thêm ca vào `ProductPriceBoardApiTest.php`.

**Interfaces:**
- Consumes: `resolveCompanyId`, `canViewCost`, `query` (Task 1).
- Tham số thêm: `unit_mode=base|all` (mặc định `base`), `with_next=0|1` (mặc định 1), `fields` (csv, lọc qua whitelist `code,name,manufacture,brand,model,unit,cost,price_1,price_5,price_2,price_3,price_4,price_6`; `cost` bị loại khi không quyền), `page`, `limit` (mặc định 2000, trần 5000).
- `GET export-rows` trả đúng contract `utils/export/listExportFile.js`: `{ headings, widths, rows, total }` — `rows` phẳng, 1 dòng/hàng (`base`) hoặc 1 dòng/ĐVT (`all`, cột thông tin hàng lặp lại); STT luôn là cột đầu. `with_next=1` ⇒ mỗi `price_x` đã chọn thành 3 cột liền: `"<Loại> - Hiện tại"`, `"<Loại> - Sắp áp dụng"`, `"<Loại> - Từ ngày"` (tiêu đề 1 tầng ghép tên — **Claude chốt**, vì contract `listExportFile` chỉ có 1 hàng tiêu đề; spec ghi 2 tầng). Ô giá số thuần / `null`; ô ngày chuỗi `dd/mm/yyyy`.
- `GET print-list-data` trả contract `reportPrintPreviewMixin`: `{ template: '<html>', total, limit, landscape: true }` (dùng trait `Modules/CustomerCare/Services/Concerns/LimitsPrintListRows` hoặc helper `printListPayload` như `CustomerDebtCompareController@printListData`). Letterhead = `companies.header` của **công ty xem** (khuôn `BillIncomePrintService::headerUrl()`: URL tuyệt đối giữ nguyên, tương đối ghép `ERP_URL`, thiếu `ERP_URL` trả nguyên path). Tiêu đề `BẢNG GIÁ BÁN HÀNG HOÁ HIỆN HÀNH`; dòng phụ `Công ty: {code} - {name} · Ngày in: dd/mm/yyyy · Đơn vị tính: cơ bản|tất cả · Đơn vị tiền: VNĐ`. `with_next=1` ⇒ dòng phụ `→ giá · ngày` màu `#2563EB` trong ô giá.

- [x] **Step 1: Viết test fail**:
  - `test_export_rows_requires_permission` (403 không quyền).
  - `test_export_rows_base_vs_all_units` — `base` ⇒ P1 1 dòng; `all` ⇒ P1 2 dòng (ĐVT gốc + phụ), cột Mã lặp lại.
  - `test_export_rows_with_next_adds_three_columns` — `fields=code,price_1&with_next=1` ⇒ headings `['STT','Mã hàng','Bán lẻ - Hiện tại','Bán lẻ - Sắp áp dụng','Bán lẻ - Từ ngày']`; `with_next=0` ⇒ `['STT','Mã hàng','Bán lẻ']`.
  - `test_export_rows_drops_cost_without_permission` — `fields=code,cost` không quyền giá vốn ⇒ headings không có Giá vốn.
  - `test_export_rows_respects_fields_order` — `fields=price_1,code` ⇒ STT, Bán lẻ…, Mã hàng.
  - `test_print_list_data_uses_viewed_company_letterhead` — xem B ⇒ `template` chứa `companies.header` của B.
  - `test_print_list_data_over_limit_returns_notice_payload` — giả trần nhỏ (override hằng/config như khuôn trait) ⇒ `template = ''`, `total > limit`.
- [x] **Step 2: Chạy, phải FAIL** — `vendor/bin/phpunit --filter 'export_rows|print_list' Modules/MasterData/Tests/Feature/ProductPriceBoardApiTest.php`.
- [x] **Step 3: Cài** `exportRows` / `printListData` + blade + 2 route.
- [x] **Step 4: Chạy lại cả file test ⇒ PASS.** Đo `export-rows?limit=2000` < 2s/lượt.
- [x] **Checkpoint BE** — báo user kết quả PHPUnit + số đo; chưa sang FE nếu còn đỏ.

---

## Phase 2 — Frontend (hrm-client)

### Task 3: Mở rộng popup chung `export-fields-modal.vue`

**Files:**
- Modify: `components/modal/export-fields-modal.vue`

**Interfaces:**
- Produces: prop `submitText` (String, mặc định `'Xuất file'`), prop `submitIcon` (String, mặc định `'ri-download-line'`), prop `headerIcon` (String, mặc định `'ri-download-line'`), slot `#options` render giữa danh sách trường và footer, bọc khối có viền trên `1px solid #e5e7eb`, `margin-top/padding-top 10px` — chỉ render khi `$slots.options`. Prop `title` có sẵn.

- [x] **Step 1: Đo trước** bằng Playwright MCP trên `/assign/customers` (màn khuôn, http://127.0.0.1:3000): mở popup Xuất Excel, ghi lại tiêu đề, chữ nút, chiều cao popup, có/không vùng tuỳ chọn.
- [x] **Step 2: Sửa component** (thêm 3 prop + slot, không đổi gì khác).
- [x] **Step 3: Đo lại `/assign/customers`** ⇒ mọi số đo khớp Step 1. `grep -rln "ExportFieldsModal\|export-fields-modal" pages components | wc -l` ghi vào checkpoint (số màn bị ảnh hưởng tiềm năng).

### Task 4: Page + menu + bảng + bộ lọc + cấu hình cột + sort

**Files:**
- Create: `pages/finance/product-price-board/index.vue` (layout `default-sidebar`, tiêu đề "Bảng giá bán hiện hành")
- Create (nếu page > ~600 dòng): `components/product/price/ProductPriceBoardTable.vue` cho ô giá/ĐVT
- Modify: `components/subsystem-menu/finance.js` — `{ label: 'Bảng giá bán hiện hành', link: '/finance/product-price-board' }` ngay sau mục `Duyệt giá bán` (~dòng 461), KHÔNG `isShow`.

**Interfaces:**
- Consumes: `GET master-data/product-price-board`, `GET master-data/product-price-board/form-options` (Task 1).
- Produces cho Task 5: `filters` (object tham số lọc như Task 1), `sortBy/sortDesc`, `tableColumns` (từ `columnCustomizationMixin`), `companyMeta {id, code, name}`, `canViewCost`, `canViewAll`, `canExport` (đều từ BE theo công ty xem — **KHÔNG** đọc `$store.state.permissions` cho giá vốn; `canExport` / `canViewAll` có thể đọc store vì xét ở công ty đang làm, khởi tạo `false`).
- `columnScreenKey: 'master_data_product_price_board'`; `allColumns` khoá: `index` (STT, locked), `code` (locked), `name`, `manufacture`, `brand`, `model`, `unit`, `cost` (chỉ khi `canViewCost`), `price_1, price_5, price_2, price_3, price_4, price_6` — đều `isVisible: true`, `sortable: true` trừ `index`, `unit`.

- [x] **Step 1: Menu + page khung** — `V2BaseSmartFilterPanel floating` (khuôn `components/product/ProductListPage.vue` + skill list-page): quick search placeholder `Tìm theo mã, tên hàng, model`; slot `#quick-search-extra` = `V2BaseCheckbox switch` "Chỉ hàng có giá sắp áp dụng" (`only_next`); field `catalog` (4 ô, copy `#field-catalog` + `catalogLevels`, `resetKeys` 4 khoá, `inputCount: 4`), `classification` (copy `#field-classification` + `classificationLevels`, `inputCount: 4`), `manufacture_id`, `brand_id`, `model_id` (slot copy `#field-model_id` + `V2BaseSelectRemote`), `company_id` (`required: true`, chỉ khai khi `canViewAll`, ô cuối). Không `group` (không tiêu đề nhóm). Deep watcher `filters` (keyword trong `ignoredFields`).
- [x] **Step 2: Đổi công ty** ⇒ reset 4 khoá catalog + `sel ĐVT`, gọi lại `form-options?company_id=` (catalog + `can_view_cost`), rồi tải danh sách.
- [x] **Step 3: Bảng** `V2BaseDataTable` — tiêu đề thẻ `Bảng giá bán hiện hành · {code} - {name}`; slot `#cell-<key>` (memory `v2basedatatable-slot-cell-key`): `unit` = `V2BaseSelect` nhỏ khi ≥ 2 ĐVT (đổi chỉ đổi state `selectedUnit[productId]`, không gọi API), chữ khi 1 ĐVT; `price_x` = số `en-US` + `<span class="next-price">` `#2563EB` 11px `→ {next_price} · {next_date}` khi có; ô `null` để trống. Toolbar: `Xuất Excel` (secondary success, `ri-file-excel-2-line`) + `In danh sách` (secondary, `ri-printer-line`) chỉ khi `canExport`, rồi `Cấu hình cột hiển thị` (icon `ri-layout-column-line`, `btn-compact`, luôn có); `class="mr-2 mb-2"`, nút cuối `mb-2`.
- [x] **Step 4: Sort** — `@sort` ⇒ `sort_by`/`sort_desc` gửi BE (khoá cột = khoá sort Task 1, `cost` chỉ khi `canViewCost`); mặc định `code asc`.
- [x] **Step 5: Kiểm Playwright MCP** (http://127.0.0.1:3000, tài khoản `namdangit@gmail.com`, memory `test-bang-tai-khoan-namdangit`), đo DOM, ghi số vào checkpoint:
  - menu có mục ngay sau "Duyệt giá bán";
  - tiêu đề thẻ = `TPE - …` của công ty đang làm;
  - đếm `th` = 14 (có giá vốn) / 13 (không);
  - `getComputedStyle(.next-price).color = rgb(37, 99, 235)`;
  - đổi ĐVT ⇒ giá dòng đổi + **0 request** mới;
  - bấm tiêu đề Bán lẻ ⇒ 1 request `sort_by=price_1`;
  - mở nâng cao: hàng ô cách 18px, không có tiêu đề nhóm;
  - user không quyền tổng công ty ⇒ không có ô Công ty; có quyền ⇒ đổi sang công ty khác: tiêu đề đổi, 4 ô catalog rỗng;
  - khoảng cách 2 nút toolbar = 12px;
  - không lỗi console. Đóng tab sau khi đo (memory `tab-mcp-de-mo-lam-nghen-api`).

### Task 5: In / Xuất Excel

**Files:**
- Modify: `pages/finance/product-price-board/index.vue`

**Interfaces:**
- Consumes: `GET …/export-rows`, `GET …/print-list-data` (Task 2); prop/slot mới của `ExportFieldsModal` (Task 3); `exportFieldsMixin`, `reportPrintPreviewMixin`, `utils/export/listExportFile.js` (`exportListFile`, `fetchCompanyLetterhead` — truyền `company_id` công ty xem: endpoint `human/companies/letterhead?company_id=` đã nhận tham số).
- `exportFields` = `[{id:'code',name:'Mã hàng'}, {id:'name',name:'Tên hàng'}, {id:'manufacture',name:'Hãng SX'}, {id:'brand',name:'Thương hiệu'}, {id:'model',name:'Model'}, {id:'unit',name:'ĐVT'}, {id:'cost',name:'Giá vốn'} (khi canViewCost), {id:'price_1',name:'Bán lẻ'}, …]` — `id` trùng khoá cột bảng ⇒ `visibleExportFields` tick sẵn đúng cột đang hiện.
- 1 popup dùng chung cho cả 2 nút: `pendingExportType = 'excel' | 'print'`; Excel ⇒ `title` mặc định, `submitText 'Xuất file'`; In ⇒ `title 'Chọn trường in'`, `submitText 'Xem trước'`, `submitIcon 'ri-eye-line'`, `headerIcon 'ri-printer-line'`. Slot `#options`: `V2BaseRadio` (`[{value:'base',label:'Chỉ ĐVT cơ bản'},{value:'all',label:'Tất cả ĐVT'}]` — memory `v2baseradio-option-value-label`) + `V2BaseCheckbox` "Kèm giá sắp áp dụng" (mặc định `true`).

- [x] **Step 1: Xuất Excel** — `runExport('excel', fields)` ⇒ `exportListFile` với endpoint `master-data/product-price-board/export-rows`, params = bộ lọc + sort + `unit_mode` + `with_next` + `fields`; có dòng tiến độ; tên file `Bang-gia-ban-{code}-{dd-mm-yyyy}.xlsx`.
- [x] **Step 2: In** — `openPrintList('master-data/product-price-board', params, 'Xem trước bảng giá bán')` + `<ReportPrintPreviewModal>` khuôn `pages/sale/prepick-tracking/index.vue:198`.
- [x] **Step 3: Kiểm Playwright MCP**, đo DOM, ghi số:
  - ẩn cột Model ở bảng ⇒ mở Xuất Excel: popup tick sẵn đủ cột đang hiện (không Model), đúng thứ tự;
  - có vùng tuỳ chọn;
  - mở file tải về (đọc bằng ExcelJS trong Node 20): headings khớp, ô giá kiểu number, `numFmt '#,##0'`;
  - `with_next` bật ⇒ 3 cột/loại giá;
  - In ⇒ popup xem trước khổ ngang, letterhead đúng công ty xem, dòng phụ xanh;
  - không quyền In/Xuất ⇒ 2 nút không có trong DOM;
  - không quyền giá vốn ⇒ popup không có trường Giá vốn.
  - ⚠️ Không bấm nút **In** bên trong popup xem trước (memory `playwright-mcp-nut-in-popup-khoa-trinh-duyet`).

### Task 6: E2E + chốt

**Files:**
- Create: `e2e/tests/finance/product-price-board.spec.ts` (khuôn spec giá: `e2e/tests/**/product-prices*.spec.ts`; cấp quyền bằng SQL ⇒ xoá cache spatie — memory `e2e-cap-quyen-sql-phai-xoa-cache`; dữ liệu tự dựng + dọn).

- [x] **Step 1: Viết ca** (có quyền + không quyền cho cả 3 quyền — memory `always-test-permission-cases`):
  - danh sách + tiêu đề công ty;
  - dòng phụ xanh;
  - đổi ĐVT không request;
  - sort;
  - không quyền giá vốn ⇒ không cột;
  - quyền giá vốn chỉ ở công ty đang làm + xem công ty khác ⇒ không cột;
  - không quyền tổng công ty ⇒ không ô Công ty;
  - không quyền In/Xuất ⇒ không nút;
  - popup chọn trường tick đúng cột đang hiện + có vùng tuỳ chọn;
  - Excel 3 cột/loại giá;
  - `/assign/customers` popup xuất không đổi;
  - đo khuôn giao diện (memory `e2e-ui-phai-kiem-khuon-giao-dien`): toolbar 12px, hàng lọc 18px.
- [x] **Step 2: Chạy (chỉ khi user yêu cầu — memory `khong-tu-chay-e2e-moi-task`)**: `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test product-price-board --workers=1` ⇒ đọc dòng tổng kết (serial: "did not run" ≠ passed).
- [x] **Step 3: Cập nhật `plan.md` checkpoint + `.plans/gop-db/STATUS.md`**; dọn role tạm / dữ liệu test (memory `local-dev-duoc-cap-quyen-de-test`).

---

### Checkpoint — 28/10/2026 (tối)
Vừa hoàn thành: Task 1–6 (subagent-driven, mỗi task review sạch; Task 2/5 sửa 1 vòng, Task 6 sửa 2 vòng) + review cuối (opus) SẴN SÀNG, 0 Critical/Important. PHPUnit ProductPriceBoardApiTest 21/21 (DB bản sao hrm_erp_bang_gia_test). Đã COMMIT + PUSH origin/gop_db 28/10: hrm-api `36fb5d042`, hrm-client `0c3df9a58` (rebase trên 6 + 1 commit mới của remote, không xung đột). Spec e2e `HRM/e2e/tests/finance/product-price-board.spec.ts` (14 ca, ngoài git) — user cho chạy 28/10: **17/17 passed** (lượt 5). Sửa trong lúc chạy: 3 lỗi của spec (tách mã/tên công ty, bấm span sort, đo hàng ô lọc bọc display:contents) + 1 lỗi thật: nhãn loại giá 6 trên trang "TMĐT" lệch file Excel/bản in ⇒ đổi trang thành "Thương mại điện tử" (khớp màn Cập nhật/Duyệt giá). Spec tự dọn role tạm + trả company_role (đã đối chiếu bản sao DB). Sổ quyết định + minor hoãn: `sdd-ledger.md`.
Đang làm dở: —
Bước tiếp theo: user kiểm tay màn /finance/product-price-board; deploy cần chạy seeder quyền (2 quyền mới) → gỡ role tạm 108490 + DROP DB hrm_erp_bang_gia_test.
Blocked: chờ user
DB app hrm_erp_21_10_prod đã ghi: 2 quyền mới (101269, 101270 — giữ); role tạm 108490 TMP-BANG-GIA-28-10 (NV 13, cty 1, quyền 101269/101270/1092) — XOÁ khi xong.

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: Bảng giá bán hàng hoá hiện hành — 6 task + review cuối + e2e 17/17; COMMIT + PUSH origin/gop_db (hrm-api `36fb5d042`, hrm-client `0c3df9a58`). Spec e2e ngoài git.
Đang làm dở: —
Bước tiếp theo: user kiểm tay màn Tài chính › Quản lý giá - CTKM › Giá bán › Bảng giá bán hiện hành; sau đó gỡ role tạm 108490 (DB hrm_erp_21_10_prod) + DROP DB hrm_erp_bang_gia_test (chờ user cho). Deploy: chạy seeder quyền (2 quyền mới) + admin gán quyền cho vai trò.
Blocked: chờ user kiểm tay

---

## Phase 3 — Chỉnh bộ lọc theo góp ý user (28/10/2026, user cho "làm": hrm-client gop_db, 1 file + spec e2e)

- [x] Ô Công ty lên đầu bộ lọc: hàng 1 = Công ty · Hãng SX · Thương hiệu · Model (người không có quyền tổng công ty: hàng 1 = Hãng SX · Thương hiệu · Model, Catalog bắt đầu hàng mới), sau đó Catalog 4 cấp, Phân loại 4 cấp
- [x] Thu hẹp ô tìm nhanh để công tắc cạnh nó đủ chỗ (không xuống dòng / không bị cắt)
- [x] Đổi chữ công tắc "Chỉ hàng có giá sắp áp dụng" → "Chỉ hàng sắp thay đổi giá" (user chốt giữ chữ "Chỉ")
- [x] Kiểm Playwright (đo DOM: thứ tự ô hàng 1, 18px giữa hàng, độ rộng ô tìm / công tắc 1 dòng) + cập nhật spec e2e U5 (+ ca liên quan) rồi chạy lại toàn bộ spec
- [x] (user bổ sung giữa chừng, cho "làm" kèm sửa panel dùng chung) Cột mặc định STT · Mã · Tên · ĐVT · 6 cột giá; Hãng SX / Thương hiệu / Model / Giá vốn = tuỳ chọn (isVisible false). Bộ lọc mặc định: tìm nhanh + Công ty · Hãng · Thương hiệu · Model; Catalog / Phân loại = tuỳ chọn qua cờ mới `defaultHidden` của `V2BaseSmartFilterPanel` (opt-in, màn khác không đổi)
- [x] Xoá cấu hình cột test của NV 13 (user_column_settings id 149, do e2e tạo) để thấy bộ cột mặc định mới

### Checkpoint — 28/10/2026 (Phase 3)
Vừa hoàn thành: Phase 3 — đo Playwright: ô tìm nhanh 925→529px (40%), vùng công tắc 181→577px, chữ "Chỉ hàng sắp thay đổi giá" không cắt; bảng mặc định 10 cột; khối nâng cao 1 hàng Công ty·Hãng·Thương hiệu·Model; popup Cài đặt bộ lọc: Catalog/Phân loại bỏ tick. E2E cập nhật (helper columnChoices đọc popup Cấu hình cột để kiểm quyền giá vốn) ⇒ 17/17 passed.
Đang làm dở: —
Đã COMMIT + PUSH origin/gop_db: hrm-client `33d666104`.
Bước tiếp theo: user kiểm tay; gỡ role tạm 108490 + DROP hrm_erp_bang_gia_test khi user cho.
Blocked:

### Checkpoint — 28/10/2026 (wrap up 2)
Vừa hoàn thành: Phase 3 (bộ lọc + cột mặc định, ô tìm nhanh hẹp, chữ "Chỉ hàng sắp thay đổi giá", cờ `defaultHidden` ở V2BaseSmartFilterPanel) — e2e 17/17, PUSH origin/gop_db hrm-client `33d666104`. Toàn feature trên gop_db: hrm-api `36fb5d042`, hrm-client `0c3df9a58` + `33d666104`. Spec e2e ngoài git (đã cập nhật).
Đang làm dở: —
Bước tiếp theo: user kiểm tay màn Bảng giá bán hiện hành; gỡ role tạm 108490 (hrm_erp_21_10_prod) + DROP DB hrm_erp_bang_gia_test khi user cho. Deploy: seeder quyền (2 quyền mới) + admin gán quyền.
Blocked: chờ user kiểm tay

## Phase 4 — Hiện đủ chữ ở cột thông tin (28/10/2026, user cho "làm": hrm-client gop_db, 1 file + spec e2e)

- [x] Cột Mã / Tên hàng / Hãng SX / Thương hiệu / Model hiện ĐỦ nội dung, chữ dài xuống dòng — bỏ cắt "…" + tooltip
- [x] Kiểm Playwright (đo scrollWidth ≤ clientWidth, ô cao hơn khi tên dài, không còn text-overflow ellipsis) + cập nhật spec e2e + chạy lại toàn bộ

### Checkpoint — 28/10/2026 (Phase 4)
Vừa hoàn thành: 5 cột thông tin (Mã, Tên, Hãng SX, Thương hiệu, Model) hiện đủ chữ, xuống dòng — `cellClass: 'text-wrap board-info'` + CSS riêng màn gỡ ellipsis của fixed-layout, bỏ :title. Đo: 0/20 ô Tên bị cắt, white-space normal, text-overflow clip, cột giá vẫn nowrap. E2E 17/17 (U1 thêm assert không cắt chữ; spec cất tạm + trả lại cấu hình cột id 150 và cấu hình bộ lọc id 8 mà user tự lưu lúc 19:36–19:39).
Đang làm dở: —
Đã COMMIT + PUSH origin/gop_db: hrm-client `0b63506fb`.
Bước tiếp theo: user kiểm tay; gỡ role tạm 108490 + DROP hrm_erp_bang_gia_test khi user cho.
Blocked:

## Phase 5 — Nút xem lịch sử giá mỗi mã hàng (28/10/2026, user cho "làm": hrm-api + hrm-client gop_db + spec e2e)

Quyết định: icon `ri-history-line` (V2BaseIconButton + tooltip "Lịch sử giá", khuôn ProductPriceTable/ApprovalTable) đặt CẠNH Mã hàng (user chọn); dùng lại `ProductPriceHistoryModal` với `endpointBase = master-data/product-price-board/companies/{company}` (công ty xem nằm trong path ⇒ không sửa popup dùng chung). Ai vào bảng giá đều xem được lịch sử giá bán; dòng Giá vốn + cột Hệ số chỉ khi có quyền giá vốn TẠI công ty xem (`ProductPriceHistoryService::logs($rowId, $hideCost)` — khuôn màn Duyệt giá). Xem công ty khác cần quyền tổng công ty (403).

- [x] BE: route `product-price-board/companies/{company}/histories/{product}` + `/filter-options` · controller dùng `resolveCompanyId` + `canViewCost` · hàng không Đang KD ở công ty xem / không có dòng hàng × công ty ⇒ [] · PHPUnit (có/không quyền giá vốn, công ty khác 403, đúng công ty)
- [x] FE: icon cạnh Mã hàng mở `ProductPriceHistoryModal` (tên hàng làm nhãn) · kiểm Playwright (popup mở, request đúng path công ty, không quyền giá vốn ⇒ không dòng Giá vốn)
- [x] Spec e2e: ca mở lịch sử (có / không quyền giá vốn) + chạy lại toàn bộ

### Checkpoint — 28/10/2026 (Phase 5)
Vừa hoàn thành: nút Lịch sử giá cạnh Mã hàng. BE `ProductPriceBoardController@histories|historyFilterOptions` + 2 route `product-price-board/companies/{company}/histories/{product}[/filter-options]`; PHPUnit 24/24 (3 ca mới). FE icon `V2BaseIconButton ri-history-line` trong ô Mã + `ProductPriceHistoryModal` (endpointBase theo công ty xem). Playwright: 20 nút/20 dòng, nút 28px nằm gọn ô Mã 150px; popup "Lịch sử giá bán: <tên>"; công ty 1 (có quyền giá vốn) hiện Hệ số, công ty 2 (không) ẩn Hệ số; request đúng `companies/{1|2}/histories/{id}`. E2E thêm U10 + P6 ⇒ 19/19 passed.
Đang làm dở: — (đã push cùng Phase 6, xem checkpoint Phase 6)
Bước tiếp theo: —
Blocked:

## Phase 6 — Độ rộng cột (28/10/2026, user cho "làm": hrm-client gop_db 1 file + spec e2e)

Đo trước (1440px): cột giá 170px nhưng số chính cần ~82–95px; dòng phụ 1 dòng cần 157px; tiêu đề "Thương mại điện tử" 147px. Mã cần 229, Tên 299, Hãng 354 (1 hãng rất dài), Model 207. User chọn GIỮ dòng phụ 1 dòng.
- [x] Cột giá 170→160; Mã 150→230; Tên 280→320; Hãng SX 140→200; Model 140→210; Thương hiệu giữ 130; ĐVT 110→90
- [x] Playwright: không ô giá nào xuống dòng (số chính + dòng phụ), tiêu đề 1 dòng, ô ĐVT chứa vừa ô chọn; chạy lại e2e

### Checkpoint — 28/10/2026 (Phase 6)
Vừa hoàn thành: độ rộng cột (giá 160 · Mã 230 · Tên 320 · Hãng 200 · Model 210 · ĐVT 90; mixin cột lấy width từ khai báo nên cấu hình user đã lưu vẫn ăn width mới). Đo: tiêu đề mọi cột cao 32px (1 dòng), 0 ô tràn, dòng phụ dài nhất 17px (1 dòng), ô chọn ĐVT gọn trong 90px. E2E U2 thêm assert cột giá vừa đủ ⇒ 19/19.
Đang làm dở: —
Đã COMMIT + PUSH origin/gop_db: hrm-api `3a14fac44` (Phase 5 BE), hrm-client `5370d6620` (Phase 5 FE + Phase 6).
Bước tiếp theo: user kiểm tay; gỡ role tạm 108490 + DROP hrm_erp_bang_gia_test khi user cho.
Blocked:

### Checkpoint — 28/10/2026 (wrap up 3)
Vừa hoàn thành: Phase 4 (cột thông tin hiện đủ chữ) · Phase 5 (nút Lịch sử giá cạnh Mã hàng + API lịch sử theo công ty xem) · Phase 6 (độ rộng cột). Đã PUSH origin/gop_db — hrm-api `36fb5d042` `3a14fac44`; hrm-client `0c3df9a58` `33d666104` `0b63506fb` `5370d6620`. PHPUnit 24/24, e2e 19/19 (spec ngoài git).
Đang làm dở: —
Bước tiếp theo: user kiểm tay màn Bảng giá bán hiện hành; gỡ role tạm 108490 (hrm_erp_21_10_prod) + DROP DB hrm_erp_bang_gia_test khi user cho. Deploy: seeder quyền (2 quyền mới) + admin gán quyền.
Blocked: chờ user kiểm tay
