# Import hàng hóa công ty — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm nút Import trên màn Dữ liệu hàng hoá công ty để thêm mới và cập nhật hàng hóa từ file Excel 79 cột, giao diện và cách làm theo import BOM.

**Architecture:** FE parse Excel rồi gửi JSON. `ProductImportService` điều phối: `ProductImportCatalog` tra danh mục theo lô, `ProductImportValidator` trả trạng thái từng dòng, `ProductImportWriter` ghi từng dòng trong một transaction qua `ProductWriteService`, `ProductPriceWriter::applyImported` và `ProductLifecycleService::tradeWithoutPrice`. FE là modal riêng clone layout `BomImportModal`.

**Tech Stack:** Laravel + nwidart Modules, PHPUnit (`DatabaseTransactions`, DB dev), Nuxt 2, Vue 2, XLSX, Playwright MCP.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/import-hang-hoa-cong-ty/design.md`

## Global Constraints

- Mọi quyết định U1–U9, C1–C20 trong design là bắt buộc; lệch thì dừng và hỏi.
- Không commit, không push khi user chưa yêu cầu (CLAUDE.md HRM). Plan này không có bước commit.
- Không đụng các file đang sửa dở của người khác trên `develop`: nhóm `Modules/Finance/*`, `pages/finance/*`, `DeliveryQuotationForm.vue`.
- Không sửa `V2BaseImportModal.vue`, `utils/import-helper.js` (11 màn dùng chung).
- Quyền: `Xây dựng thông tin hàng hoá` + `dueConfig:Cập nhật hàng hóa`; ghi giá cần thêm `Cập nhật giá bán hàng hoá`.
- Tối đa 500 dòng dữ liệu mỗi file; phân trang 50 dòng/trang.
- Công ty luôn lấy từ `auth()->user()->current_company_role`, không nhận từ request.
- Thông báo cố định: `Sản phẩm đã tồn tại trên hệ thống`; `Hàng hóa đang bị khóa bởi phiếu YCHG [Mã_Phiếu] ở trạng thái [Tên_Trạng_thái], không được phép cập nhật.`
- Lệnh test chạy trong `hrm-api`: `vendor/bin/phpunit Modules/MasterData/Tests/Feature/<File>.php`.

## Review Focus

1. Ô số `0` đến dưới dạng number hoặc chuỗi `"0"`: phải coi là có dữ liệu, không phải ô trống (test: Task 5).
2. Khoảng trắng và dấu `;` thừa: `A ; B;` cho ra đúng 2 phần tử (test: Task 2).
3. Số kiểu Việt `1,25` trong file mẫu: đọc thành `1.25`; `1.000.000` đọc thành `1000000`; chữ thì báo lỗi (test: Task 2).
4. Trạng thái đổi giữa Validate và Import (có YCHG mới, đổi trạng thái): `import` phải bắt được (test: Task 3).
5. Mã tham chiếu trong lưới 1-N trỏ chính hàng đang sửa, hàng tạm hoặc hàng đã xóa: báo lỗi, không ghi (test: Task 3).

---

## Hợp đồng dữ liệu

File mẫu: dòng 1 nhóm cột, dòng 2 header, dòng 3 đánh số, dòng 4 ghi chú, dữ liệu từ dòng 5. Dòng dữ liệu Excel = `index + 5`.

**Bẫy parser:** `parseExcelFile` chỉ lấy dòng đầu của header (`normKey`), nên header xuống dòng như `Giá bán lẻ⏎Hệ số` sẽ đè lên nhau. File mẫu tĩnh phải dùng header một dòng, duy nhất, ví dụ `Giá bán lẻ - Hệ số`.

Key JSON, theo thứ tự cột (khai một lần ở `hrm-client/utils/product-import-columns.js`, kèm `header`):

```
stt code action name model common_name english_name barcode note characteristic product_type brand origin manufacture
barcode_code unit is_base unit_coefficient unit_conversion attr_names attr_values attr_units attr_print norm
standard_accessories product_attributes recipe_codes recipe_names recipe_units recipe_qtys recipe_mains
accessory_codes accessory_names accessory_units accessory_qtys install_codes install_names install_units install_qtys
repair_codes repair_names customs_name hs_code min_buy_qty vat import_tax import_tax_co antidump environment_coef
machine_groups machine_codes machine_names suppliers business_policy min_stock_qty guarantee guarantee_type
tech_coefficient catalog_scopes catalog_chapters catalog_groups catalog_clusters trade_flag cost_price
retail_coef retail_price retail_sale lot_coef lot_price lot_sale d1_coef d1_price d1_sale d2_coef d2_price d2_sale
d3_coef d3_price d3_sale
```

Loại giá: retail=1, lot=5, d1=2, d2=3, d3=4. `guarantee_type`: Ngày/Tháng/Năm → `ngay/thang/nam`. Danh mục catalog: `internal_business_scopes` → `chapters` → `job_groups` → `job_clusters`.

Request: `{ rows: [{ excel_row: int, ...keys }], skip_invalid?: bool }`.

Response validate:

```json
{ "rows": [{ "excel_row": 5, "action": "add|update", "valid": true, "ignored": ["model"], "errors": [{ "excelRow": "Dòng 5", "column": "Model", "message": "..." }] }],
  "summary": { "total": 1, "valid": 1, "error": 0 } }
```

Response import: `{ "created": n, "updated": n, "failed": n, "errors": [...] }`.

---

### Task 1: API khung, quyền và tra danh mục

**Files:**
- Create: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/ProductImportController.php`
- Create: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportService.php`
- Create: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportCatalog.php`
- Modify: `hrm-api/Modules/MasterData/Routes/api.php` (cạnh `POST /take`, trước các route `/{product}`)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportApiTest.php`

**Interfaces:**
- Produces: `ProductImportService::validate(array $rows): array`, `import(array $rows, bool $skipInvalid): array`.
- Produces: `ProductImportCatalog::load(array $rows): self`; `find(string $type, ?string $name): array` trả danh sách id khớp; `barcode(?string $name, ?int $manufactureId): array`. `$type` là một trong `model, product_type, brand, origin, manufacture, unit, unittech, attribute, characteristic, tax_rate, business_policy, supplier, machine_group`.

- [ ] **Step 1: Viết test đỏ**

`test_requires_build_permission` (403), `test_rejects_more_than_500_rows` (422, không ghi gì), `test_rejects_empty_rows` (422), `test_catalog_lookup_is_case_insensitive_and_trimmed`, `test_catalog_returns_all_matches_for_duplicate_name`, `test_catalog_ignores_inactive_entries`, `test_barcode_lookup_is_scoped_by_manufacture`.

Dùng `Concerns\ActsAsProductUser`, `DatabaseTransactions`, công ty 6 như `ProductWriteApiTest`.

- [ ] **Step 2: Chạy test, xác nhận FAIL do chưa có route**

- [ ] **Step 3: Thêm 2 route và controller**

```php
Route::post('/import/validate', 'V1\\Product\\ProductImportController@validateRows')->middleware(['checkPermission:' . $build, 'dueConfig:Cập nhật hàng hóa']);
Route::post('/import', 'V1\\Product\\ProductImportController@import')->middleware(['checkPermission:' . $build, 'dueConfig:Cập nhật hàng hóa']);
```

Controller kiểm `rows` là mảng 1–500 phần tử, gọi `assertCanWrite()`. Trả bằng `responseJson` như `BomListController::validateImport`.

- [ ] **Step 4: Viết `ProductImportCatalog`**

Mỗi loại danh mục một truy vấn `whereIn` trên tên đã chuẩn hóa (trim, lowercase) cho cả file. Không query theo ô.

- [ ] **Step 5: Chạy test, xác nhận PASS**

### Task 2: Validate chung và THÊM MỚI

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportCells.php`
- Create: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportValidator.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportValidateAddTest.php`

**Interfaces:**
- Consumes: `ProductImportCatalog` (Task 1).
- Produces: `ProductImportCells::isBlank($v): bool` (chỉ null và chuỗi rỗng sau trim), `list($v): array` (tách `;`, trim, bỏ phần tử rỗng), `number($v): ?float` (ném `InvalidArgumentException` nếu không phải số), `yesNo($v): ?bool`.
- Produces: `ProductImportValidator::validate(array $rows): array` trả shape response validate; mỗi dòng hợp lệ có thêm khóa nội bộ `resolved` (id đã tra) để Task 4 dùng. `ProductImportService::validate` bỏ `resolved` trước khi trả FE.

- [ ] **Step 1: Viết test đỏ**

Test đơn vị của Cells: `list('A ; B;') === ['A','B']`, `number('1,25') === 1.25`, `number('1.000.000') === 1000000.0`, `number(0) === 0.0`, `isBlank(0) === false`, `isBlank('0') === false`, `isBlank('  ') === true`.

Test validator, mỗi test assert đúng `column` và `message`:
- `test_action_must_be_add_or_update`, chấp nhận `thêm mới` viết thường.
- `test_required_columns_for_add` gồm Tên, Model, Loại SP, Thương hiệu, Xuất xứ, Hãng SX, Đơn vị, % VAT.
- `test_unknown_catalog_value_rejected`, `test_ambiguous_catalog_value_rejected`.
- `test_grid_lengths_must_match` cho thuộc tính, 3 lưới Mã–Tên–ĐVT–SL, CT lắp ráp (thêm Thành phần chính), lưới sửa chữa Mã–Tên, Mã máy–Tên máy, 4 cột Catalog.
- `test_grid_name_must_match_code`, `test_catalog_branch_must_be_real_path`.
- `test_machine_group_requires_machine`.
- `test_duplicate_in_file_ticket_rule_marks_all_rows`, `test_duplicate_in_file_form_rule_marks_all_rows`.
- `test_duplicate_in_db_ticket_rule`, `test_duplicate_in_db_form_rule`, cả hai ra `Sản phẩm đã tồn tại trên hệ thống`; barcode trống so với barcode trống; không lọc công ty; bỏ qua hàng `status = 0`.
- `test_price_cell_requires_1657`, không có ô giá thì không cần quyền.
- `test_price_limits` (`MONEY_MAX`, hệ số `< 100`, % 0–100), `test_code_column_is_ignored_on_add`.
- `test_collects_all_errors_of_a_row`.

- [ ] **Step 2: Chạy test, xác nhận FAIL**

- [ ] **Step 3: Viết `ProductImportCells`, `ProductImportValidator` (nhánh chung + add)**

Giới hạn độ dài và số lấy đúng theo `ProductRequest::commonRules()`/`adminRules()`. Hàng tham chiếu trong lưới tra `products` theo `code`, `status = 1`, không phải hàng tạm; phụ kiện phải có dòng ĐVT khai trong file. Quy tắc form trùng lấy từ `ProductRequest::checkUniqueName` (`where status <> 0`).

- [ ] **Step 4: Chạy test, xác nhận PASS**

### Task 3: Validate CẬP NHẬT

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportValidator.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportValidateUpdateTest.php`

**Interfaces:**
- Produces: dòng update có `resolved.product_id`, `resolved.status`; `ignored` gồm `model, manufacture, brand`, thêm `barcode_code` khi hàng đã có Code, thêm `trade_flag` và các cột giá khi status 3.

- [ ] **Step 1: Viết test đỏ**

- `test_code_required_and_must_exist`.
- `test_other_company_product_rejected`, kể cả công ty mình đã lấy về.
- `test_locked_product_rejected`.
- `test_ychg_open_status_blocks` với data provider `[3, 2, 10, 1, 5, 7]`; assert đúng câu thông báo, mã phiếu, tên từ `STATUS_TEXT`.
- `test_ychg_closed_status_allows` với `[8, 4, 9, 11, 6]`.
- `test_ychg_reports_newest_request`, `test_ychg_from_other_company_blocks`.
- `test_status_other_than_1_and_3_rejected` với `[2, 4, 5, 6, 7, 8, 9]`, và hàng chưa có dòng ở công ty mình.
- `test_trading_ignores_flag_and_price_columns`, không đòi quyền 1657.
- `test_same_code_twice_in_file_errors_both`.
- `test_rename_checks_form_duplicate`.
- `test_filling_blank_barcode_that_creates_duplicate_rejected`.
- `test_only_file_cells_are_validated`: hàng cũ thiếu Loại SP vẫn sửa được Ghi chú.
- `test_new_unit_requires_coefficient`.
- `test_grid_code_cannot_be_self`, `test_grid_code_cannot_be_temp_or_deleted`.
- `test_import_revalidates`: validate pass, tạo YCHG mở, gọi `/import` thì dòng bị từ chối.

- [ ] **Step 2: Chạy test, xác nhận FAIL**

- [ ] **Step 3: Viết nhánh update theo đúng thứ tự mục 6 của design**

Bước chặn (1–5) dừng ở lỗi đầu. Tra YCHG cho cả file bằng một truy vấn: `price_asking_request_products.group_id → price_asking_request_groups.price_asking_request_id → price_asking_requests`, lọc status mở, lấy phiếu `id` lớn nhất mỗi hàng. Thêm hằng `PriceAskingRequest::OPEN_STATUSES`. Không dùng `assertOwner` (ném lỗi); đọc cùng điều kiện rồi đẩy vào `errors`.

- [ ] **Step 4: Chạy test, xác nhận PASS**

### Task 4: Ghi THÊM MỚI

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportWriter.php`
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductWriteService.php:126,423` (thêm ghi chú lịch sử)
- Modify: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportService.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportWriteAddTest.php`

**Interfaces:**
- Consumes: `resolved` (Task 2).
- Produces: `ProductImportWriter::write(array $row): int` trả product id, chạy trong `DB::transaction`, ném exception thì dòng rollback.
- Produces: `ProductWriteService::withHistoryNote(?string $note): self`; ghi chú dùng cho `logCreate` và `logUpdate`. Writer đặt `'Import Excel'` rồi trả về `null` trong `finally`.

- [ ] **Step 1: Viết test đỏ**

- `test_add_creates_product_with_generated_code`: mã đúng `ProductCodeGenerator`, `product_company_coefficients.status = 1`, `info_entered_at` khác null, không có ảnh.
- `test_add_writes_all_grids`: thuộc tính, 4 bảng kit, `product_suppliers`, `product_business_catalogs`, `productables`.
- `test_add_multiple_suppliers_and_catalogs`.
- `test_skip_invalid_true_writes_only_valid_rows`, `test_skip_invalid_false_writes_nothing_when_any_error`.
- `test_write_failure_is_reported_and_other_rows_stay`: mock lỗi ở dòng 2, dòng 1 và 3 còn, `failed = 1`.
- `test_history_note_is_import_excel`.

- [ ] **Step 2: Chạy test, xác nhận FAIL**

- [ ] **Step 3: Viết `write` nhánh add và `ProductImportService::import`**

`$data` đúng shape `ProductRequest`: `units` một dòng `is_base=1`, `unit_coefficient=1`; kit dùng `product_id, unit_id, qty`; `repair_accessories` chỉ `product_id`; `admin` luôn có. Gọi `store($data, ProductCompany::STATUS_ENTERING_INFO)`. `import` validate lại; `skip_invalid=false` mà có lỗi thì trả lỗi, không ghi.

- [ ] **Step 4: Chạy test, xác nhận PASS**

### Task 5: Ghi CẬP NHẬT một phần

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportWriter.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportWriteUpdateTest.php`

**Interfaces:**
- Consumes: `ProductFormResource::RELATIONS`, `ProductWriteService::update(Product, array $data)`.

- [ ] **Step 1: Viết test đỏ**

- `test_blank_cells_keep_every_field`: hàng đủ dữ liệu (ảnh, video, tài liệu, đời xe, 4 kit, NCC, catalog, nhóm máy); import chỉ đổi Ghi chú; so snapshot toàn bộ bảng con trước và sau.
- `test_zero_overwrites`: `min_buy_qty`/`min_stock_qty`/`guarantee` nhận `0` cả dạng number và chuỗi.
- `test_grid_with_data_replaces_all`, `test_blank_grid_keeps`, áp cho từng lưới.
- `test_suppliers_catalog_replace_only_current_company`.
- `test_model_manufacture_brand_ignored`.
- `test_blank_barcode_filled_keeps_product_code`, `test_existing_barcode_ignored`.
- `test_new_unit_added_old_unit_id_unchanged`, `test_existing_unit_not_duplicated`.
- `test_no_price_columns_touched_for_trading`.

- [ ] **Step 2: Chạy test, xác nhận FAIL**

- [ ] **Step 3: Viết nhánh update**

Dựng dữ liệu nền từ DB theo đúng shape `ProductRequest` (dùng `ProductFormResource`, đổi key khi cần), trộn ô có dữ liệu lên trên, rồi gọi `update()` kèm `admin`. Dòng ĐVT cũ giữ `id` để `writeUnits` bỏ qua. `assertCodeSourceKept` chỉ ở controller nên không cần tham số. Test `test_blank_cells_keep_every_field` là chốt chặn chính của bước này.

- [ ] **Step 4: Chạy test, xác nhận PASS**

### Task 6: Ghi giá và chuyển kinh doanh

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/ProductPrice/ProductPriceWriter.php`
- Modify: `hrm-api/Modules/MasterData/Services/Product/Import/ProductImportWriter.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductImportPriceTest.php`

**Interfaces:**
- Produces: `ProductPriceWriter::applyImported(int $productId, int $productUnitId, int $companyId, array $cells, ?float $cost, int $by): void`. `$cells = [priceTypeId => ['price'?, 'coefficient'?, 'sale_max_percent'?]]`; chỉ key có mặt mới ghi.

- [ ] **Step 1: Viết test đỏ**

- `test_add_flag_no_saves_prices_status_1`, `test_add_flag_yes_saves_prices_status_3`.
- `test_add_flag_yes_logs_status_history` (note của `TRADE_NOTE`).
- `test_update_entering_flag_yes_moves_to_trading`, `test_update_entering_flag_no_keeps`, cả hai ghi giá (C17).
- `test_blank_price_cell_keeps_value`, `test_zero_price_is_written`.
- `test_price_goes_to_row_unit`, `test_blank_unit_uses_base_unit`.
- `test_online_price_follows_retail_when_not_manual`, `test_online_price_kept_when_manual`.
- `test_company_with_price_approval_writes_directly`: bật `is_company_price` trong test.
- `test_keeps_expected_prices_and_pending_approvals`: giá hẹn, `price_wait_approve`, `pa`/`pap` còn nguyên.
- `test_trade_blocked_rolls_back_row`: `tradeWithoutPrice` trả `skipped` thì dòng rollback, báo lỗi.
- `test_inherited_sync_called`.

- [ ] **Step 2: Chạy test, xác nhận FAIL**

- [ ] **Step 3: Viết `applyImported`**

Gọi `sets->ensureUnitSet`, khóa dòng `product_company_units`, update đúng cột của `product_unit_prices`. Không dùng `writePrices`, `writeExpected`, `writeCompanyUnit`, `dropPendingApprovals`. `cost_price` update riêng một cột. Loại 6 tính lại theo `resolvePrices` khi Bán lẻ đổi và cờ sửa tay tắt. Cuối cùng gọi `InheritedPriceSync::propagate([$productUnitId], $companyId, $by)`.

- [ ] **Step 4: Nối vào writer**

Thứ tự trong transaction của dòng: ghi hàng → `applyImported` → nếu cờ Có thì `tradeWithoutPrice([$id])`; `skipped` khác rỗng thì ném exception kèm `message`.

- [ ] **Step 5: Chạy toàn bộ test import và test hàng hóa liên quan**

Run: `vendor/bin/phpunit --filter 'ProductImport|ProductWriteApiTest|ProductLifecycleApiTest' `
Expected: PASS, trừ lỗi đã có trước khi làm (đối chiếu bằng cách chạy trên `develop`).

### Task 7: Popup Import và file mẫu

**Files:**
- Create: `hrm-client/utils/product-import-columns.js`
- Create: `hrm-client/components/product/ProductImportModal.vue`
- Create: `hrm-client/static/Mau_import_hang_hoa.xlsx`
- Modify: `hrm-client/components/product/ProductListPage.vue` (nút cạnh Xuất Excel, dòng ~175; computed cạnh `canTradeWithoutPrice` ~994)
- Modify: `hrm-client/utils/product-list-screens.js` (cờ `import: true` ở màn `company`)

**Interfaces:**
- Consumes: 2 API và hợp đồng dữ liệu ở trên.
- Produces: `PRODUCT_IMPORT_COLUMNS: Array<{key, header, group, width}>`; `ProductImportModal` phát event `imported`.

- [ ] **Step 1: Sinh file mẫu**

Từ file Google Sheet: giữ 4 dòng đầu, header thành một dòng và duy nhất theo `PRODUCT_IMPORT_COLUMNS`, sửa mọi ghi chú và dữ liệu mẫu dùng dấu phẩy thành `;`, ghi rõ NCC và Catalog nhập nhiều bằng `;` và thay toàn bộ (U9), ghi `Đơn vị` là một giá trị. Sheet tên `Data`. Kiểm: đọc lại bằng `parseExcelFile` ra đúng 79 cột, không key trùng sau `normKey`.

- [ ] **Step 2: Viết modal**

Copy pattern từ `pages/assign/quotations/components/QuotationImportModal.vue` (prefix `.pim-`), logic validate từ `BomImportModal.vue:969`. Gọi `parseExcelFile(file, PRODUCT_IMPORT_COLUMNS, 2, 1)`. Thiếu header thì báo sai mẫu. Giữ `_validateSeq`, toggle "Bỏ qua dòng lỗi", bảng lỗi với Sao chép lỗi và Tải File lỗi.

Khác BOM: phân trang 50 dòng, ô là text và chỉ đổi thành input khi bấm (C14); ô trong `ignored` tô xám, không sửa được; sửa ô đánh dấu dòng cần validate lại và khóa Import; quá 500 dòng thì báo và không load.

- [ ] **Step 3: Thêm nút**

`v-if="screen.import && canBuildProduct"`, nhãn `Import`, icon `ri-file-upload-line`. Sau `imported` tải lại danh sách.

- [ ] **Step 4: Kiểm tra bằng lint**

Run: `npx eslint components/product/ProductImportModal.vue utils/product-import-columns.js components/product/ProductListPage.vue`
Expected: không lỗi mới.

### Task 8: Kiểm tra trên trình duyệt

**Files:** không tạo file code. Ảnh chụp để ở scratchpad.

- [ ] **Step 1: Chạy app bằng skill run-hrm, mở `http://127.0.0.1:3000/master-data/products/company`**

- [ ] **Step 2: Chạy luồng với file có đủ loại dòng**

File gồm: thêm mới hợp lệ cờ Có; thêm mới hợp lệ cờ Không; trùng trong file; danh mục sai; cập nhật hợp lệ; cập nhật bị khóa YCHG; cập nhật hàng công ty khác. Kiểm: tải mẫu, load, pill đúng, chỉ dòng lỗi, sửa ô rồi validate lại, Sao chép lỗi, Tải File lỗi, bật bỏ qua dòng lỗi, import, danh sách tải lại, mở chi tiết hàng vừa tạo.

- [ ] **Step 3: Đối chiếu ảnh chụp với popup BOM**

Layout, stepper, toolbar, pill, modal lỗi phải cùng khuôn. Kiểm tra màn 1366px.

- [ ] **Step 4: Kiểm hiệu năng 500 dòng**

Load, cuộn, chuyển trang, validate: không treo; console không có lỗi mới.

- [ ] **Step 5: Kiểm người không có quyền**

Không có `$build`: không thấy nút. Có `$build`, không có 1657: dòng có giá báo lỗi, dòng không giá import được.
