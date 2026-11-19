# Import hàng hoá 10 sheet (#12174) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay mẫu import 1 sheet 79 cột bằng mẫu nghiệp vụ 10 sheet (Thêm mới + Cập nhật), từ chối trọn hàng khi có lỗi ở bất kỳ sheet nào.

**Architecture:** BE nhận payload theo **hàng** (`products[]` = dòng Sheet 1 + dòng con các sheet 2–10, `orphans[]`, `created_keys{}`). Validator Sheet 1 cũ giữ lại (đổi nguồn ô), lưới con tách ra 4 class theo sheet; một bước gộp lỗi theo hàng (V1) + sắp thứ tự ghi theo tham chiếu mã tạm (D8). Writer dựng `$data` form như cũ rồi gọi `ProductWriteService`. FE đọc 10 sheet, popup 10 tab, chia lô giữ nhóm tham chiếu, sinh file lỗi `.xlsx` bằng `exceljs`.

**Tech Stack:** Laravel 8 / PHP 7.4 (phpunit feature test, `DatabaseTransactions`), Nuxt 2 / Vue 2, `exceljs ^4.4`, Playwright (`e2e/`, Node 20).

**Spec:** `HRM/.plans/import-hang-hoa-12174/design.md` (cột chính xác: `cot-va-huong-dan-10-sheet.txt`, mẫu: `Mau_nghiep_vu_10_sheet.xlsx`). Thiết kế cũ còn hiệu lực ở những gì spec không đổi: `HRM/.plans/import-hang-hoa-cong-ty/design.md`.

## Global Constraints

- Nhánh `develop` cả `hrm-api` lẫn `hrm-client`. **KHÔNG commit/push** (HRM CLAUDE.md) — bước "Commit" của mỗi task thay bằng `git status` liệt kê file đã đổi; user tự quyết commit.
- Chạy test BE: `cd HRM/hrm-api && php artisan test Modules/MasterData/Tests/Feature/<File>.php` (DB local `erp_hrm_check`, xem skill `run-hrm`).
- Giới hạn: **500 hàng/file**, **tổng dòng mọi sheet ≤ 20.000**, lô ghi **50 hàng**, lock cache `'product-import'` 600s, 409 khi bận (giữ nguyên).
- File mẫu: dòng 1 header, dòng 2 hướng dẫn, dữ liệu **từ dòng 3**; header khớp nguyên văn `cot-va-huong-dan-10-sheet.txt` (bỏ khoảng trắng thừa đầu/cuối).
- Tên sheet theo đúng thứ tự: `1. Thông tin chung`, `2. ĐVT & Bảng giá`, `3. Thuộc tính kỹ thuật`, `4. Công thức lắp ráp`, `5. Phụ kiện mua thêm`, `6. Vật tư lắp đặt`, `7. Vật tư sửa chữa`, `8. Phân loại xe`, `9. Nhóm máy`, `10. Catalog kinh doanh`.
- Câu lỗi nguyên văn (D22 + các mục khác), copy đúng chữ:
  - `Mã hàng hóa không tồn tại`
  - `Từ chối: Hàng hóa đang bị khóa bởi phiếu YCHG <mã> (Trạng thái: <tên>)`
  - `Trùng Tên + Model + Hãng SX + Code đặt hàng + Thương hiệu với dòng <N>`
  - `Đã có hàng hoá cùng Tên, Model, Hãng SX, Code đặt hàng và Thương hiệu: <mã>`
  - `Không tìm thấy mã ở Sheet 1`
  - `Có lỗi ở Sheet <N>`
  - `Chỉ tạo được hàng cho công ty đang đăng nhập`
  - `Tính chất không khớp Loại sản phẩm (<tính chất đúng>)`
  - `Không đổi được ĐVT cơ bản`
  - `Hàng công ty khác tạo, không thêm được ĐVT`
  - `Hàng <mã tạm> ở Sheet 1 bị lỗi`
  - `Loại sản phẩm không thuộc phụ tùng ô tô – xe máy, không nhập được Phân loại xe`
- Lỗi trả FE: `{sheet: int 1..10, excelRow: int, column: string (header nguyên văn), message: string, level: 'error'|'warning'}`.
- Số hiển thị `toLocaleString('en-US')`; chữ đỏ chỉ cho lỗi; cảnh báo vàng dùng token màu sẵn có (`#F59E0B`); popup giữ khung `ProductImportModal.vue` (V2BaseModal, V2Base*, `$confirm` cho hỏi xoá dòng con).
- File mẫu tĩnh `hrm-client/static/Mau_import_hang_hoa.xlsx` = bản copy `Mau_nghiep_vu_10_sheet.xlsx` (V8, ngoại lệ có chủ đích với `buildImportTemplate`).

## Review Focus

1. **File 79 cột cũ / file sai thứ tự sheet được upload** — phải báo "File không đúng mẫu" và không load gì (Task 8 Step 1 + Task 12 spec: upload `old-79-cols.xlsx`).
2. **Mã ở sheet con có khoảng trắng đầu/cuối hoặc khác hoa thường** — trim thì khớp, khác hoa thường thì là mồ côi (D3) (Task 1 test `test_child_key_trimmed_but_case_sensitive`).
3. **Một hàng Cập nhật chỉ có dòng ở Sheet 2/3 mà Sheet 1 chỉ điền Mã + Hành động** — các lưới khác + ô trống giữ nguyên DB (Task 7 test `test_update_only_attributes_keeps_everything_else`).
4. **Hàng được trỏ tới nằm ở lô 2 còn hàng trỏ nằm ở lô 1 do FE chia sai** — BE phải từ chối với câu D8, không ghi `product_id` rác (Task 6 test `test_reference_to_temp_key_not_in_batch_nor_created_keys`).
5. **Sửa ô Mã ở tab 1 trùng với mã của dòng Sheet 1 khác** — FE không được gộp dòng con của 2 hàng; BE báo trùng mã Sheet 1 ở cả 2 dòng (Task 1 test `test_duplicate_sheet1_key_errors_both_rows`, Task 9 Step 2 kiểm tay Playwright).

---

## Cấu trúc file

BE `hrm-api/Modules/MasterData/Services/Product/Import/`:
- `ProductImportSheets.php` (mới) — hằng số 10 sheet: số, tên, `COLUMNS[sheet] = [key => header]`, `label(sheet,key)`.
- `ProductImportProduct.php` (mới) — 1 hàng: `key`, `sheet1` (`ProductImportRow`), `children[sheet][] ProductImportChildRow`, `errors()`, `isValid()`, `resolved`.
- `ProductImportChildRow.php` (mới) — dòng con: `sheet`, `excelRow`, `raw`, `errors[]`, `warnings[]`, `error()`, `warn()`, `cell()`, `text()`.
- `ProductImportUnitSheet.php` (mới) — Sheet 2.
- `ProductImportGridSheets.php` (mới) — Sheet 3, 4–7, 9, 10.
- `ProductImportVehicleSheet.php` (mới) — Sheet 8.
- `ProductImportReferences.php` (mới) — D8: đồ thị mã tạm, vòng, thứ tự topo.
- Sửa: `ProductImportRow.php` (lỗi có `sheet`, `level`), `ProductImportValidator.php` (Sheet 1 mới, bỏ lưới `;`/ĐVT/giá khỏi dòng), `ProductImportUpdateChecks.php` (D22 câu lỗi, D27), `ProductImportService.php` (payload mới), `ProductImportWriter.php` (nhiều ĐVT, giá từng ĐVT, xe, created_keys), `ProductImportCatalog.php` (thêm tra công ty, tính chất, xe).
- Controller `Http/Controllers/V1/Product/ProductImportController.php`: validate request shape mới.

FE `hrm-client/`:
- `utils/product-import-columns.js` → viết lại thành định nghĩa 10 sheet + parse + build payload + batch.
- `utils/product-import-error-file.js` (mới) — file lỗi `.xlsx`.
- `components/product/ProductImportModal.vue` — tab, lọc, thêm/xoá dòng con, bảng lỗi.
- `static/Mau_import_hang_hoa.xlsx` — thay file.
- `e2e/tests/product-import-10-sheet.spec.ts` (mới) + fixture `e2e/fixtures/product-import/*.xlsx`.

Test BE mới ở `Modules/MasterData/Tests/Feature/`: `ProductImportBundleTest`, `ProductImportSheet1Test`, `ProductImportUnitSheetTest`, `ProductImportGridSheetsTest`, `ProductImportVehicleSheetTest`, `ProductImportReferencesTest`, `ProductImportWriteSheetsTest`. Helper dựng payload: `Concerns/BuildsImportPayload.php` (mới, trait).

---

### Task 1: Payload theo hàng + Sheet constants + mồ côi + giới hạn

**Files:**
- Create: `Services/Product/Import/ProductImportSheets.php`, `ProductImportProduct.php`, `ProductImportChildRow.php`, `Tests/Feature/Concerns/BuildsImportPayload.php`, `Tests/Feature/ProductImportBundleTest.php`
- Modify: `ProductImportService.php`, `ProductImportRow.php`, `Http/Controllers/V1/Product/ProductImportController.php`

**Interfaces:**
- Produces:
  - `ProductImportSheets::NAMES` (int ⇒ tên sheet), `ProductImportSheets::COLUMNS` (int ⇒ [key ⇒ header nguyên văn]), `ProductImportSheets::label(int $sheet, string $key): string`.
  - Key sheet 1 (dùng cho Task 2): `code, action, name, model, company, common_name, english_name, barcode, note, characteristic, product_type, nature, brand, origin, manufacture, barcode_code, norm, standard_accessories, product_attributes, customs_name, hs_code, min_buy_qty, vat, import_tax, import_tax_co, antidump, environment_coef, suppliers, business_policy, min_stock_qty, guarantee, guarantee_type, tech_coefficient, trade_flag`.
  - Key sheet 2: `code, unit, is_base, unit_coefficient, cost_price, retail_coef, retail_price, retail_sale, lot_coef, lot_price, lot_sale, d1_coef, d1_price, d1_sale, d2_coef, d2_price, d2_sale, d3_coef, d3_price, d3_sale`.
  - Sheet 3: `code, attr_name, attr_value, attr_unit, attr_print`. Sheet 4: `code, child_code, child_name, child_unit, qty, is_main`. Sheet 5, 6: `code, child_code, child_name, child_unit, qty`. Sheet 7: `code, child_code, child_name`. Sheet 8: `code, manufacts, brands, models, all_lives, lives`. Sheet 9: `code, machine_group, machine_code, machine_name, machine_group_name`. Sheet 10: `code, cluster, group, chapter, scope`.
  - Payload: `{products: [{key, row:{excel_row,...sheet1}, units:[{excel_row,...}], attributes, kits, accessories, install_materials, repair_materials, vehicles, machines, catalogs}], orphans:[{sheet, excel_row, code}], created_keys:{<mã tạm>: product_id}}`. Map sheet ⇒ khoá: `2 units, 3 attributes, 4 kits, 5 accessories, 6 install_materials, 7 repair_materials, 8 vehicles, 9 machines, 10 catalogs` (`ProductImportSheets::PAYLOAD_KEYS`).
  - `ProductImportChildRow::__construct(int $sheet, int $excelRow, array $raw)`; `error(string $key, string $msg)`, `warn(string $key, string $msg)`, `hasErrors(): bool`, `cell($key)`, `text($key): string`, `toArray(): array` (`{sheet, excel_row, errors, warnings, ignored}`).
  - `ProductImportProduct::__construct(string $key, ProductImportRow $sheet1, array $children)`; `child rows by sheet`: `children(int $sheet): ProductImportChildRow[]`; `isValid(): bool` (không lỗi ở sheet1 lẫn mọi dòng con); `finalize()` thêm `Có lỗi ở Sheet N` (cột Mã, sheet 1) cho mỗi sheet con có lỗi (D23); `toArray()` ⇒ `{key, excel_row, action, valid, errors:[...gộp mọi sheet, mỗi lỗi {sheet, excelRow, column, message, level}], ignored:{sheet:[cột]}, resolved?}`.
  - `ProductImportService::validate(array $payload): array` ⇒ `{products: [...], orphans: [{sheet, excel_row, errors}], summary: {total, valid, error}}` (`error` = hàng lỗi + số mồ côi, D5).
  - `ProductImportService::import(array $payload, bool $skipInvalid): array` ⇒ `{created, updated, failed, errors, created_keys}`.
  - `ProductImportRow::error()` thêm `sheet => 1`, `level => 'error'` vào mỗi lỗi.

- [ ] **Step 1: Viết test fail** — `ProductImportBundleTest` (dùng trait `BuildsImportPayload` có `product(string $key, array $sheet1, array $children = [])`, `payload(array $products, array $orphans = [])`):
  - `test_orphan_child_row_reported_and_counted_as_error`: 1 hàng hợp lệ + orphan `{sheet:3, excel_row:7, code:'X9'}` ⇒ `orphans[0].errors[0].message === 'Không tìm thấy mã ở Sheet 1'`, `summary == {total:1, valid:1, error:1}`.
  - `test_import_rejected_while_orphans_exist_even_with_skip_invalid`: POST import `skip_invalid=1` có orphan ⇒ 422, không tạo hàng nào.
  - `test_duplicate_sheet1_key_errors_both_rows`: 2 hàng cùng key `T1` ⇒ cả 2 lỗi cột `Mã hàng hóa (*)`.
  - `test_blank_sheet1_key_is_required`: key `''` ⇒ lỗi `Bắt buộc phải nhập`.
  - `test_child_key_trimmed_but_case_sensitive`: (FE gom; BE kiểm) `ProductImportSheets::normalizeKey('  T1 ') === 'T1'` và `'t1' !== 'T1'`.
  - `test_child_error_rejects_whole_product_and_flags_sheet1`: hàng có 1 dòng Sheet 3 lỗi (thuộc tính không có trong danh mục) ⇒ `valid=false`, có lỗi `{sheet:1, column:'Mã hàng hóa (*)', message:'Có lỗi ở Sheet 3'}`.
  - `test_limits_500_products_and_20000_rows`: 501 hàng ⇒ 422 `Tối đa 500 hàng hoá mỗi lần import`; tổng dòng 20.001 ⇒ 422 `Tối đa 20.000 dòng (tất cả sheet) mỗi lần import`.
- [ ] **Step 2: Chạy** `php artisan test Modules/MasterData/Tests/Feature/ProductImportBundleTest.php` ⇒ FAIL (class chưa có).
- [ ] **Step 3: Cài** các class trên; `Service::validate` dựng `ProductImportProduct` từ payload, gọi `ProductImportValidator::validateProducts(ProductImportProduct[] $products)` (Task 2 tách nội dung), gắn lỗi mồ côi, `finalize()` mỗi hàng. Controller validate shape: `products` array required max 500, `products.*.key` string, `orphans` array, `created_keys` array. Tạm thời lưới con chưa có validator ⇒ để hook `ProductImportValidator::$sheetValidators` rỗng; test Sheet 3 trong bước này dùng `ProductImportGridSheets` stub chỉ kiểm thuộc tính tồn tại (hoàn thiện Task 4).
- [ ] **Step 4: Chạy lại** ⇒ PASS.
- [ ] **Step 5:** `git -C hrm-api status --short` ghi danh sách file vào báo cáo task (không commit).

### Task 2: Sheet 1 theo mẫu mới (V2, D10, D11, D12, D22, D27)

**Files:**
- Modify: `ProductImportValidator.php` (xoá `parseUnit`, `gridLists`, `attributes`, `kitGrid`, `checkPrices`… khỏi luồng dòng; giữ hàm dùng lại được bằng cách chuyển sang Task 3/4), `ProductImportUpdateChecks.php`, `ProductImportCatalog.php`
- Test: `Tests/Feature/ProductImportSheet1Test.php`; cập nhật `ProductImportValidateAddTest`, `ProductImportValidateUpdateTest`, `ProductImportForeignProductTest` sang payload mới (giữ nguyên các ca nghiệp vụ còn áp dụng, xoá ca chỉ thuộc lưới `;`)

**Interfaces:**
- Consumes: Task 1 `ProductImportProduct`, `ProductImportSheets::label(1, $key)`.
- Produces: `ProductImportValidator::validateProducts(array $products): void`; sau bước này `$product->resolved` (mảng cấp hàng, mọi task sau ghi tiếp vào đây) có `fields, admin, trade_flag, product_id, action, foreign, owner_status, nature_id, is_auto_parts`. `LABELS` cũ thay bằng `ProductImportSheets::COLUMNS[1]`.

- [ ] **Step 1: Test fail** (`ProductImportSheet1Test`):
  - `test_duplicate_5_fields_in_file`: 2 dòng THÊM MỚI cùng Tên+Model+Hãng SX+Code đặt hàng+Thương hiệu ⇒ dòng sau lỗi `Trùng Tên + Model + Hãng SX + Code đặt hàng + Thương hiệu với dòng 3`; đổi Code đặt hàng dòng sau ⇒ hợp lệ.
  - `test_duplicate_5_fields_in_db`: trùng hàng DB mã `HH-x` ⇒ `Đã có hàng hoá cùng Tên, Model, Hãng SX, Code đặt hàng và Thương hiệu: HH-x`.
  - `test_update_duplicate_checked_only_when_name_changed_or_code_filled`.
  - `test_company_other_than_login_rejected` ⇒ `Chỉ tạo được hàng cho công ty đang đăng nhập`; trống / đúng tên công ty ⇒ hợp lệ; CẬP NHẬT ⇒ cột `Công ty quản lý` trong `ignored`.
  - `test_nature_mismatch_with_product_type` ⇒ `Tính chất không khớp Loại sản phẩm (<tên tính chất của loại>)`; trống ⇒ hợp lệ.
  - `test_update_model_brand_ignored_manufacture_locked_barcode_code_only_when_empty` (D27).
  - `test_update_unknown_code` ⇒ `Mã hàng hóa không tồn tại`.
  - `test_update_blocked_by_open_price_request_each_open_status`: lặp `PriceAskingRequest::OPEN_STATUSES` ⇒ `Từ chối: Hàng hóa đang bị khóa bởi phiếu YCHG <mã> (Trạng thái: <tên>)`.
  - `test_renamed_columns_map` : `Barcode`⇒`barcode`, `Đặc tính sản phẩm`⇒`product_characteristic_id`, `Đặc điểm`⇒`product_attributes`, `Đơn vị bảo hành`⇒`guarantee_type`, `Chuyển kinh doanh không tính giá` Có ⇒ `resolved.trade_flag = true`.
- [ ] **Step 2: Chạy** ⇒ FAIL.
- [ ] **Step 3: Cài.** Kiểm trùng 5 trường thay `checkDuplicates` (khoá ghép chuẩn hoá: trim + lower, Code đặt hàng trống = `''`); tra trùng DB 1 query theo lô. Tra công ty theo tên (`companies.name`, so trim không phân biệt hoa thường). Tính chất suy từ `product_types → families → function_groups → natures` (cùng join như `ProductWriteService::writeVehicles`).
- [ ] **Step 4: Chạy** `ProductImportSheet1Test` + 3 file test cũ đã chuyển ⇒ PASS.
- [ ] **Step 5:** liệt kê file đổi.

### Task 3: Sheet 2 — ĐVT & giá từng ĐVT (D13, D14, D15, D24, D25, V4)

**Files:**
- Create: `ProductImportUnitSheet.php`; Test `ProductImportUnitSheetTest.php`
- Modify: `ProductImportValidator.php` (gọi Sheet 2), dời `canUpdatePrice` / logic giá từ `checkPrices` sang class mới; cập nhật `ProductImportPriceTest` sang payload mới.

**Interfaces:**
- Consumes: Task 2 `resolved.action, product_id, foreign, owner_status`; `ProductImportValidator::PRICE_TYPES`, `PRICE_PERMISSION`.
- Produces: `ProductImportUnitSheet::validate(ProductImportProduct $p, ProductImportCatalog $catalog, bool $canPrice): void` đặt `$p->resolved['units'] = [['unit_id', 'is_base', 'unit_coefficient', 'is_new' => bool, 'prices' => ['prices' => [typeId => ['coefficient','price','sale']], 'cost_price' => ?]]]`.

- [ ] **Step 1: Test fail:**
  - `test_add_requires_at_least_one_unit_row` ⇒ lỗi sheet 1 cột Mã `Bắt buộc có ít nhất 1 dòng ở Sheet 2`.
  - `test_add_exactly_one_base_with_coefficient_1`: 0 dòng Có ⇒ `Phải có đúng 1 ĐVT cơ bản`; 2 dòng Có ⇒ lỗi cả 2 dòng; Có + hệ số 2 ⇒ `ĐVT cơ bản phải có hệ số 1`; Có + trống ⇒ coi 1.
  - `test_add_non_base_requires_positive_coefficient`, `test_duplicate_unit_in_product`.
  - `test_update_base_unit_change_rejected` ⇒ `Không đổi được ĐVT cơ bản`.
  - `test_update_existing_unit_coefficient_differs_from_db` ⇒ lỗi cột `Hệ số quy đổi`.
  - `test_update_new_unit_added_missing_units_kept` (resolved units chỉ chứa dòng file; `is_new` đúng).
  - `test_trading_product_price_columns_ignored` (U3), `test_inherited_price_filled_is_error`, `test_no_price_permission_price_filled_is_error` (U6).
  - `test_foreign_product_new_unit_rejected_coefficient_ignored` ⇒ `Hàng công ty khác tạo, không thêm được ĐVT` (D24).
  - `test_prices_kept_per_unit_not_derived` (D25): ĐVT Hộp hệ số 10 giá lẻ 500 ⇒ resolved giá 500, không phải 10×giá cơ bản.
- [ ] **Step 2–4:** chạy FAIL → cài → PASS (`ProductImportUnitSheetTest`, `ProductImportPriceTest`).
- [ ] **Step 5:** liệt kê file đổi.

### Task 4: Sheet 3, 4–7, 9, 10 (D6, D7, D17, D18, D19, D20)

**Files:**
- Create: `ProductImportGridSheets.php`; Test `ProductImportGridSheetsTest.php`
- Modify: `ProductImportValidator.php` (dời `kitGrid`, `checkKitUnit`, `kitQty`, `catalogBranch`, `referenced` sang class mới, đổi đầu vào từ list `;` sang dòng con); `ProductImportUpdateChecks::checkSelfReference/checkMachines` đổi đầu vào tương ứng.

**Interfaces:**
- Consumes: Task 1 `ProductImportChildRow`; `ProductImportCatalog::find`.
- Produces: `ProductImportGridSheets::validate(ProductImportProduct $p, array $tempKeys): void` — `$tempKeys` = mã tạm hợp lệ trên Sheet 1 (string[]). Đặt `$p->resolved` các khoá form: `attributes`, `recipes`, `accessories`, `install_accessories`, `repair_accessories`, `machine_group_ids`, `machine_ids`, `catalog_cluster_ids` — **chỉ đặt khoá khi sheet đó có ≥ 1 dòng của hàng** (D16). Phần tử lưới kit trỏ mã tạm mang `['product_id' => null, 'temp_key' => 'T2', ...]`. `$p->resolved['temp_refs'] = string[]`.

- [ ] **Step 1: Test fail:**
  - `test_attribute_required_unknown_duplicate_and_print_flag`: In tem `có` ⇒ true; trống ⇒ false; trùng thuộc tính ⇒ lỗi dòng sau.
  - `test_kit_child_code_required_exists_or_temp_key`: mã không có ⇒ `Mã hàng hóa không tồn tại`; mã tạm Sheet 1 ⇒ hợp lệ, `temp_refs` chứa nó.
  - `test_kit_qty_positive_integer_on_sheets_4_5_6`; Sheet 7 không kiểm SL.
  - `test_kit_duplicate_child_and_self_reference` (mã con = mã hàng / = mã tạm của chính nó).
  - `test_child_name_mismatch_is_warning_not_error` (D6): `level=warning`, message chứa tên chuẩn, `valid=true`.
  - `test_child_unit_unknown_error_mismatch_warning` (D7).
  - `test_machine_group_from_machine_and_mismatch` (D19), nhóm máy gom unique.
  - `test_catalog_cluster_required_and_branch_checked` (D20).
  - `test_sheet_without_rows_sets_no_key` (D16).
- [ ] **Step 2–4:** FAIL → cài → PASS.
- [ ] **Step 5:** liệt kê file đổi.

### Task 5: Sheet 8 Phân loại xe (§6.8)

**Files:**
- Create: `ProductImportVehicleSheet.php`; Test `ProductImportVehicleSheetTest.php`
- Modify: `ProductImportCatalog.php` (tra theo lô `vehicle_manufacts`, `vehicle_brands`, `vehicle_models`, `vehicle_lives` — xác nhận tên bảng/cột từ `ProductWriteService::writeVehicles` + form request trước khi cài)

**Interfaces:**
- Consumes: Task 2 `resolved.is_auto_parts`.
- Produces: `ProductImportVehicleSheet::validate(ProductImportProduct $p): void` đặt (chỉ khi có dòng) `resolved.vehicle_manufact_ids`, `vehicle_brand_ids`, `vehicle_model_ids` (unique, int[]), `vehicle_lives = [['model_id' => int, 'life_ids' => int[]]]`.

- [ ] **Step 1: Test fail:**
  - `test_all_lives_yes_takes_every_life_of_model`; `test_all_lives_yes_with_lives_column_is_error`.
  - `test_lives_list_must_belong_to_model`.
  - `test_multiple_models_only_without_lives`: 2 model + có đời xe ⇒ lỗi; 2 model không đời xe ⇒ hợp lệ.
  - `test_model_must_belong_to_manufact_on_same_row`.
  - `test_unknown_names_error` (hãng/loại/model/đời).
  - `test_not_auto_parts_product_type_rejected` ⇒ `Loại sản phẩm không thuộc phụ tùng ô tô – xe máy, không nhập được Phân loại xe`.
- [ ] **Step 2–4:** FAIL → cài → PASS.
- [ ] **Step 5:** liệt kê file đổi.

### Task 6: Tham chiếu mã tạm cùng đợt (D8, D26)

**Files:**
- Create: `ProductImportReferences.php`; Test `ProductImportReferencesTest.php`
- Modify: `ProductImportService.php` (sau validate từng hàng: lan lỗi + sắp thứ tự ghi; import nhận `created_keys`)

**Interfaces:**
- Consumes: Task 4 `resolved.temp_refs`, payload `created_keys`.
- Produces: `ProductImportReferences::apply(ProductImportProduct[] $products, array $createdKeys): ProductImportProduct[]` — trả danh sách theo thứ tự ghi (hàng được trỏ tới trước); hàng trong vòng ⇒ lỗi `Trỏ vòng giữa các hàng mới: T1 → T2 → T1` (cột Mã, sheet 1); hàng trỏ tới hàng lỗi ⇒ `Hàng <mã tạm> ở Sheet 1 bị lỗi` (lan bắc cầu). Mã tạm có trong `$createdKeys` coi như hàng thật đã có. `ProductImportService::import` trả `created_keys` gồm các mã tạm ghi thành công lượt này `{key: {id, code}}`.

- [ ] **Step 1: Test fail:**
  - `test_writes_referenced_product_first_and_links_real_id`: T1 có công thức trỏ T2 ⇒ import ghi T2 trước, `product_recipes` của T1 trỏ đúng id T2; kết quả `created_keys.T2.id` có.
  - `test_cycle_rejects_all_in_cycle` (T1↔T2, và tự trỏ).
  - `test_referenced_product_invalid_rejects_referrer` (bắc cầu T1→T2→T3 lỗi ⇒ cả 3).
  - `test_created_keys_from_previous_batch_resolve`: lô 2 gửi `created_keys:{T2: id}` ⇒ T1 hợp lệ.
  - `test_reference_to_temp_key_not_in_batch_nor_created_keys` ⇒ `Hàng T2 ở Sheet 1 bị lỗi` (D26: hàng được trỏ đã lỗi lúc ghi lô trước).
  - `test_referenced_fails_at_write_time_rejects_referrer_same_batch`: T2 hợp lệ lúc validate nhưng ghi lỗi (giả lập bằng giá dưới sàn) ⇒ T1 không ghi, `errors` có câu D8.
- [ ] **Step 2–4:** FAIL → cài → PASS.
- [ ] **Step 5:** liệt kê file đổi.

### Task 7: Writer — nhiều ĐVT, giá từng ĐVT, thay trọn lưới, xe

**Files:**
- Modify: `ProductImportWriter.php`; có thể cần `ProductWriteService::writePresentChildren` thêm nhánh xe khi có khoá `vehicle_*` (hỏi user trước theo CLAUDE.md "sửa hàm dùng chung", nêu rõ thay đổi chỉ thêm `if (array_key_exists('vehicle_model_ids', $d))` gọi `writeVehicles`).
- Test: `ProductImportWriteSheetsTest.php`; cập nhật `ProductImportWriteAddTest`, `ProductImportWriteUpdateTest`, `ProductImportApiTest` sang payload mới.

**Interfaces:**
- Consumes: `resolved` từ Task 2–6; `ProductWriteService::store/updatePartial/updateAdminPartial`; `ProductPriceWriter::applyImported`; `OwnerPriceFloor`.
- Produces: `ProductImportWriter::write(array $resolved, array $idsByTempKey): int` — thay `temp_key` trong lưới kit bằng id; THÊM MỚI: `units` = toàn bộ dòng Sheet 2 theo thứ tự file; CẬP NHẬT: chỉ ĐVT `is_new`; giá ghi theo từng `product_unit_id` (lặp `applyPrices` mỗi ĐVT có giá, sàn so cùng ĐVT); hàng công ty khác ⇒ `updateAdminPartial` + giá ĐVT đã có.

- [ ] **Step 1: Test fail:**
  - `test_add_multi_units_with_own_prices`: 2 ĐVT, giá lẻ riêng ⇒ `product_unit_prices` mỗi `product_unit_id` đúng số; giá online (type 6) tính theo từng ĐVT.
  - `test_update_adds_new_unit_keeps_missing_units`.
  - `test_update_full_replace_each_grid_3_to_10` (data provider theo sheet): có dòng ⇒ thay trọn; không dòng ⇒ giữ.
  - `test_update_only_attributes_keeps_everything_else`.
  - `test_vehicles_written_and_replaced`.
  - `test_child_error_writes_nothing_of_that_product_other_products_written` (V1, gồm cả lưới khác của hàng lỗi).
  - `test_pending_and_scheduled_prices_untouched` (giữ test cũ).
- [ ] **Step 2–4:** FAIL → cài → PASS. Chạy cả thư mục: `php artisan test Modules/MasterData/Tests/Feature --filter=ProductImport` ⇒ PASS toàn bộ.
- [ ] **Step 5:** liệt kê file đổi.

### Task 8: FE — định nghĩa 10 sheet, đọc file, file mẫu

**Files:**
- Modify: `hrm-client/utils/product-import-columns.js` (viết lại), `hrm-client/static/Mau_import_hang_hoa.xlsx` (thay bằng `Mau_nghiep_vu_10_sheet.xlsx`)

**Interfaces:**
- Produces (dùng ở Task 9–11):
  - `PRODUCT_IMPORT_SHEETS: [{no, name, payloadKey, columns:[{key, header, width, required}]}]` — key trùng Task 1, header nguyên văn file `cot-va-huong-dan-10-sheet.txt`.
  - `PRODUCT_IMPORT_FIRST_DATA_ROW = 3`, `PRODUCT_IMPORT_MAX_PRODUCTS = 500`, `PRODUCT_IMPORT_MAX_TOTAL_ROWS = 20000`.
  - `async parseProductImportWorkbook(file): {sheets: {[no]: rows[]}, hints: {[no]: string[]}}` — mỗi row `{_uid, excel_row, ...keys}`; ném `Error('File không đúng mẫu: <lý do>')` khi thiếu sheet / sai tên / header lệch (D2). Bỏ dòng chỉ có STT.
  - `normalizeKey(v): string` (trim).
  - `buildProductImportPayload(sheets, createdKeys, productKeys?): {products, orphans, created_keys}`.
- [ ] **Step 1:** Copy file mẫu; kiểm `parseProductImportWorkbook` bằng script Node 20 ở scratchpad đọc `static/Mau_import_hang_hoa.xlsx` ⇒ in số dòng từng sheet, không ném lỗi; đọc 1 file 79 cột cũ (lấy từ `git show HEAD:hrm-client/static/Mau_import_hang_hoa.xlsx`) ⇒ ném `File không đúng mẫu`.
- [ ] **Step 2:** liệt kê file đổi.

### Task 9: FE — popup 10 tab, lọc theo mã, thêm/xoá dòng con, bảng lỗi

**Files:**
- Modify: `hrm-client/components/product/ProductImportModal.vue`

**Interfaces:**
- Consumes: Task 8; BE `validate` trả `{products, orphans, summary}`.
- Produces: state `sheets` (10 mảng dòng), `activeSheet`, `filterKey`, `errorsByCell` key `${sheet}:${_uid}:${columnKey}` ⇒ `{level, messages}`.

- [ ] **Step 1: Cài** theo design §4 mục 1–8: tab `N. <tên> (<số dòng>)` + `V2BaseBadge` đỏ số dòng lỗi, tab rỗng mờ; ô đỏ/xám/vàng; nút "Xem dữ liệu con" ở tab 1 ⇒ `filterKey` + thanh `Đang lọc: <mã> ×`; đổi Mã tab 1 ⇒ đổi `code` mọi dòng con cùng mã cũ và `child_code` ở Sheet 4–7, 9 đang trỏ mã cũ; nếu mã mới trùng mã một dòng Sheet 1 khác thì **không** đổi dòng con (để BE báo trùng); "+ Thêm dòng" mang sẵn `filterKey`; xoá dòng tab 1 ⇒ `$confirm` "Xoá luôn N dòng con của mã này?"; bảng lỗi cột `Sheet | Dòng Excel | Tên cột | Mô tả`, bấm ⇒ chuyển tab, bỏ lọc nếu dòng không thuộc mã đang lọc, nhảy trang, tô ô; "Chỉ dòng lỗi" theo tab mở; pill đếm theo hàng + mồ côi.
- [ ] **Step 2:** Kiểm tay bằng Playwright MCP `http://127.0.0.1:3000/master-data/products/company` (load file mẫu, đủ 10 tab, Xem dữ liệu con, đổi mã lan tab con). Lệnh tự kiểm HTML thô: `grep -n '<input \|<button \|<select ' components/product/ProductImportModal.vue | grep -v V2Base` chỉ còn `<input type="file">` cũ.
- [ ] **Step 3:** liệt kê file đổi.

### Task 10: FE — validate/import theo lô, giữ nhóm tham chiếu, `created_keys`

**Files:**
- Modify: `hrm-client/utils/product-import-columns.js` (thay `productImportBatches`), `ProductImportModal.vue` (`handleValidate`, `handleImport`)

**Interfaces:**
- Produces: `productImportBatches(products, size = 50): products[][]` — sắp topo theo `child_code` trỏ mã tạm (Sheet 4–7, 9), hàng được trỏ ở cùng lô hoặc lô trước; nhóm liên thông > 50 vẫn đi theo thứ tự topo qua nhiều lô (BE dùng `created_keys`).
- [ ] **Step 1: Cài.** Import gửi `created_keys` tích luỹ từ kết quả các lô trước; "Bỏ qua dòng lỗi" chỉ gửi hàng `valid` và không gửi mồ côi; nút Import ẩn khi còn mồ côi (D4) — chỉ hiện lại khi đã xoá/sửa hết; hàng ghi xong rời lưới cùng dòng con.
- [ ] **Step 2:** Kiểm Playwright MCP với file 60 hàng, hàng 55 có công thức trỏ hàng 2 (mã tạm) ⇒ import xong, mở hàng 55 thấy công thức đúng mã thật.
- [ ] **Step 3:** liệt kê file đổi.

### Task 11: FE — file lỗi `.xlsx` (D21)

**Files:**
- Create: `hrm-client/utils/product-import-error-file.js`
- Modify: `ProductImportModal.vue` (thay xuất CSV)

**Interfaces:**
- Produces: `async buildProductImportErrorFile({sheets, hints, rejectedKeys, orphanUids, errorsByRow}): Blob` — `exceljs`; đủ 10 sheet theo `PRODUCT_IMPORT_SHEETS`; dòng 1–2 = header + hướng dẫn (lấy `hints` đọc từ file người dùng), giữ `width`; dữ liệu = mọi dòng của hàng bị từ chối (cả dòng con không lỗi) + dòng mồ côi; cột cuối `Chi tiết lỗi hệ thống` = lỗi `level=error` của dòng nối `; `; Sheet 1 thêm `Sheet N dòng M: <message>`. Tên file `Loi_import_hang_hoa_<dd-mm-yyyy_HHmm>.xlsx`.
- [ ] **Step 1: Cài.**
- [ ] **Step 2:** Kiểm: tải file lỗi trong Playwright MCP, đọc lại bằng `parseProductImportWorkbook` (bỏ cột cuối) không ném lỗi ⇒ upload lại được.
- [ ] **Step 3:** liệt kê file đổi.

### Task 12: E2E Playwright + rà cuối

**Files:**
- Create: `e2e/tests/product-import-10-sheet.spec.ts`, `e2e/fixtures/product-import/ok-add.xlsx`, `bad-mixed.xlsx`, `old-79-cols.xlsx` (sinh bằng script Node từ file mẫu, script để scratchpad)

- [ ] **Step 1: Viết spec** các ca: tải mẫu (tên file `Mau_import_hang_hoa.xlsx`, có 10 sheet); upload `old-79-cols.xlsx` ⇒ toast `File không đúng mẫu`; upload `bad-mixed.xlsx` ⇒ tab có badge, bấm lỗi nhảy đúng tab/ô, sửa ô ⇒ Validate lại hết lỗi; mồ côi ẩn nút Import; xoá dòng tab 1 hỏi xoá dòng con; tải file lỗi ⇒ upload lại load được; `ok-add.xlsx` import ⇒ danh sách có hàng mới.
- [ ] **Step 2: Chạy** `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test product-import-10-sheet` ⇒ PASS.
- [ ] **Step 3:** Chạy lại toàn bộ test BE import ⇒ PASS; `git -C hrm-api status`, `git -C hrm-client status` liệt kê để user duyệt commit.
