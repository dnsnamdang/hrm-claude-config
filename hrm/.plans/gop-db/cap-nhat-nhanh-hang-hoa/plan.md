# Cập nhật nhanh hàng hoá (#12191) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn HRM "Cập nhật nhanh hàng hoá" sửa hàng loạt thông tin nhiều mã hàng trong 1 bảng, port từ màn ERP ẩn "Sửa nhanh hàng hóa".

**Architecture:**
- BE: thêm 2 API trong nhóm `products`.
  - `rows` tải các dòng, kèm quyền sửa của từng dòng.
  - `quick-update` lưu cả lô trong 1 transaction, mỗi dòng gọi lại `ProductWriteService::updatePartial` /
    `updateAdminPartial` (đường Import Excel).
- Hàm dùng chung `fillCommon` + snapshot lịch sử được mở rộng thêm `product_cate`, `max_stock_qty`.
- FE: 1 trang Nuxt gồm bảng sửa, phân trang 20 dòng, và popup chọn hàng `ProductPickerPanel` cấu hình như màn Báo giá.

**Tech Stack:** Laravel 8 (nwidart modules, PHPUnit `DatabaseTransactions`) · Nuxt 2 / Vue 2, V2Base*, vee-validate · Playwright.

**Spec:** `HRM/.plans/gop-db/cap-nhat-nhanh-hang-hoa/design.md` (user duyệt 17/11/2026)

## Global Constraints

**Nhánh và worktree:**
- Làm trên worktree, KHÔNG đổi nhánh repo chính.
  - api: `git -C HRM/hrm-api worktree add ../wt-quick-update-api -b feature/cap-nhat-nhanh-hang-hoa develop`
  - client: `git -C HRM/hrm-client worktree add ../wt-quick-update-client -b feature/cap-nhat-nhanh-hang-hoa develop`
- Không push, không merge khi user chưa cho.

**Quyền:**
- Mã quyền gate route + menu: `master_data.thong_tin_hang_hoa.manage`.
- Route lưu gắn thêm `dueConfig:Cập nhật hàng hóa`.

**Ghi dữ liệu:**
- Ghi chú lịch sử: `Cập nhật nhanh`.
- Trần id mỗi lượt: 200. FE phân trang 20 dòng.
- Trường sửa được (key gửi lên):
  - Chữ: `name`, `english_name`, `customs_name`, `hs_code`, `note`.
  - Chọn: `product_type_id`, `product_cate` (mảng key), `origin_id`.
  - Số lượng: `min_stock_qty`, `max_stock_qty`, `min_buy_qty`.
  - Thuế: `vat_percent_tax_rate_id`, `import_tax_has_co_tax_rate_id`, `import_tax_tax_rate_id`,
    `antidump_duty_tax_rate_id`.
  - Không có `barcode_id`, `brand_id`, `manufacture_id`, `model_id`, `product_characteristic_id`. Đây là các cột chỉ đọc
    hoặc ERP không có.
- `min_stock_qty` ⇒ khối quản trị công ty (`$data['admin']['min_stock_qty']`). `max_stock_qty` ⇒ `products.max_stock_qty`.
- `origin_id` của dòng có trong `locked_fields` (đang tính giá) thì BE bỏ qua, FE khoá ô.

**Câu chữ cố định:**
- Trùng tên: `Đã tồn tại trên hệ thống`.
- Lô không đổi gì: `Không có thay đổi nào để cập nhật`.
- `readonly_reason`:
  - `admin`: `Hàng do công ty khác tạo — chỉ sửa được SL tồn tối thiểu.`
  - `none`: lấy message 403/423 của `assertOwner`.

**Quy ước code:**
- FormRequest chỉ khai `rules()`, không khai `messages()`.
- FE dùng `V2Base*`, nút lưu đặt trong `V2Footer` slot `#custom-actions`, có `unsavedChangesMixin`, nút toolbar
  `mr-2 mb-2`.
- Chữ ghi chú xám dùng `#6b7280`, không dùng `.text-muted`.
- Commit kết thúc bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Dữ liệu `product_cate` cũ** ở dạng chuỗi JSON, `null`, `''` hoặc `"[]"` ⇒ màn đọc được và không sinh dòng lịch sử
   giả khi user không đổi gì. Test: `test_rows_reads_legacy_product_cate_formats`, `test_unchanged_cate_order_no_history` (Task 1, 3).
2. **Dữ liệu đổi giữa lúc tải và lúc lưu**: hàng vừa bị khoá hoặc vừa vào luồng tính giá ⇒ cả lô rollback, lỗi `_row`
   gắn đúng dòng. Test: `test_locked_between_load_and_save_rolls_back` (Task 3).
3. **Hai dòng trong cùng lô đặt trùng tên** (cùng model/brand/hãng) ⇒ đỏ cả 2 dòng. Test:
   `test_duplicate_name_within_batch` (Task 3).
4. **Form sửa đầy đủ không gửi 2 cột mới** ⇒ không bị xoá trắng. Test: `test_full_update_keeps_cate_and_max_stock` (Task 1).
5. **Trang có dòng lỗi không phải trang đang xem** ⇒ FE tự chuyển tới trang chứa dòng lỗi đầu tiên. Kiểm ở Playwright
   (Task 6).

---

## File Structure

**hrm-api** (worktree `HRM/wt-quick-update-api`):

| File | Thao tác |
|---|---|
| `Modules/MasterData/Entities/Product/Product.php` | Sửa: thêm `catesFromRaw()`, `catesToRaw()` |
| `Modules/MasterData/Services/Product/ProductWriteService.php` | Sửa: `fillCommon` thêm 2 cột |
| `Modules/MasterData/Services/Product/ProductHistoryService.php` | Sửa: `common()` thêm 2 khoá |
| `app/Services/CatalogHistoryService.php` | Sửa: thêm nhãn 2 cột, khoảng dòng 1152 |
| `Modules/MasterData/Services/Product/ProductQuickUpdateService.php` | Tạo: `rows()` + `save()` |
| `Modules/MasterData/Http/Requests/Product/ProductQuickUpdateRequest.php` | Tạo |
| `Modules/MasterData/Http/Controllers/V1/Product/ProductQuickUpdateController.php` | Tạo |
| `Modules/MasterData/Routes/api.php` | Sửa: nhóm `products`, đặt TRƯỚC `/{product}` |

Tests:
- `Modules/MasterData/Tests/Feature/ProductQuickUpdateFieldsTest.php` (Task 1)
- `Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php` (Task 2, 3)
- Cả 2 dùng `DatabaseTransactions` + `Concerns\ActsAsProductUser` (`actAs($companyId, $perms)`, `productTypeFixture()`).

**hrm-client** (worktree `HRM/wt-quick-update-client`):

| File | Thao tác |
|---|---|
| `pages/master-data/products/quick-update.vue` | Tạo: trang, toolbar, phân trang, lưu |
| `components/product/quick-update/QuickUpdateTable.vue` | Tạo: bảng sửa, ô theo `edit_scope` |
| `components/product/quick-update/QuickUpdatePickerModal.vue` | Tạo: popup bọc `ProductPickerPanel` |
| `components/product/quick-update/quickUpdateModel.js` | Tạo: hàm thuần — dựng dòng, so dirty, dựng payload, map lỗi |
| `components/subsystem-menu/master-data.js` | Sửa: thêm mục sau "Hàng đang kinh doanh" |

**E2E** (repo riêng `HRM/e2e`): `tests/product-quick-update.spec.ts` (Tạo)

---

### Task 1: Hàm dùng chung ghi + lịch sử `product_cate`, `max_stock_qty`

**Files:**
- Modify:
  - `Modules/MasterData/Entities/Product/Product.php`
  - `Modules/MasterData/Services/Product/ProductWriteService.php:602-640`
  - `Modules/MasterData/Services/Product/ProductHistoryService.php:73-120`
  - `app/Services/CatalogHistoryService.php:1147-1160`
- Test: `Modules/MasterData/Tests/Feature/ProductQuickUpdateFieldsTest.php`

**Interfaces:**
- Produces:
  - `Product::catesFromRaw($raw): array`
    - Nhận chuỗi JSON / mảng / `null` / `''`.
    - Trả mảng key hợp lệ của `PRODUCT_CATES`, sắp theo thứ tự khai báo trong `PRODUCT_CATES`, đã bỏ trùng.
  - `Product::catesToRaw(array $keys): ?string`
    - Rỗng ⇒ `null`.
    - Còn lại ⇒ `json_encode` mảng đã chuẩn hoá qua `catesFromRaw`.
  - `fillCommon` nhận `$d['product_cate']` (mảng key) và `$d['max_stock_qty']`.
    - Chỉ ghi khi `array_key_exists`, kể cả lúc `$partial=false`.
  - Snapshot lịch sử có 2 khoá mới:
    - `product_cate`: tên các loại nối bằng `, `.
    - `max_stock_qty`: `self::number()`.
  - Nhãn lịch sử: `'product_cate' => 'Loại hàng hoá'`, `'max_stock_qty' => 'Số lượng tồn kho tối đa'`.

- [ ] **Step 1: Write the failing tests**

```php
public function test_cates_from_raw_normalizes_legacy_formats(): void
{
    $keys = array_keys(Product::PRODUCT_CATES);
    $this->assertSame([], Product::catesFromRaw(null));
    $this->assertSame([], Product::catesFromRaw(''));
    $this->assertSame([], Product::catesFromRaw('[]'));
    $this->assertSame([$keys[0], $keys[1]], Product::catesFromRaw(json_encode([$keys[1], $keys[0], $keys[1], 'xx'])));
    $this->assertNull(Product::catesToRaw([]));
}

public function test_partial_update_writes_cate_and_max_stock_with_history(): void
// actAs(cty chủ hàng, ['master_data.thong_tin_hang_hoa.manage']);
// withHistoryNote('Cập nhật nhanh')->updatePartial($p, ['product_cate' => [$k1], 'max_stock_qty' => 50])
// assert products.product_cate == catesToRaw([$k1]), max_stock_qty == 50
// assert lịch sử mới nhất của sản phẩm có cột "Loại hàng hoá" và "Số lượng tồn kho tối đa", ghi chú 'Cập nhật nhanh'

public function test_full_update_keeps_cate_and_max_stock(): void
// hàng có product_cate=[k1], max_stock_qty=50; gọi PUT products/{id} bằng payload form đầy đủ KHÔNG có 2 khoá ⇒ 2 cột giữ nguyên

public function test_unchanged_cate_order_no_history(): void
// DB lưu catesToRaw([k1,k2]); updatePartial với ['product_cate' => [k2,k1]] ⇒ không sinh dòng lịch sử mới
```

- [ ] **Step 2: Chạy test, kiểm tra FAIL**

Run: `cd HRM/wt-quick-update-api && php artisan test Modules/MasterData/Tests/Feature/ProductQuickUpdateFieldsTest.php`

Expected: FAIL — `Call to undefined method ...Product::catesFromRaw()`.

- [ ] **Step 3: Implement**

- Viết 2 hàm static trong `Product`.
- `fillCommon`: thêm `product_cate` + `max_stock_qty` ở một vòng riêng sau foreach chung, điều kiện `array_key_exists`.
  `product_cate` ghi qua `catesToRaw()`.
- `ProductHistoryService::common()`: `product_cate` ⇒ map `catesFromRaw($p->product_cate)` sang tên `PRODUCT_CATES`,
  nối `, `, rỗng ⇒ `null`.
- Thêm 2 nhãn vào `columns` của `products` trong `CatalogHistoryService`.

- [ ] **Step 4: Chạy test, kiểm tra PASS (kèm test Import để không vỡ)**

Run: `php artisan test Modules/MasterData/Tests/Feature/ProductQuickUpdateFieldsTest.php Modules/MasterData/Tests/Feature/ProductImportWriteUpdateTest.php Modules/MasterData/Tests/Feature/ProductWriteApiTest.php`

Expected: PASS hết.

- [ ] **Step 5: Commit**

`git commit -m "feat(products): fillCommon + lịch sử ghi Loại hàng hoá, SL tồn tối đa (#12191)"`

---

### Task 2: API tải dòng `POST products/quick-update/rows`

**Files:**
- Create:
  - `Modules/MasterData/Services/Product/ProductQuickUpdateService.php` (hàm `rows`)
  - `Modules/MasterData/Http/Controllers/V1/Product/ProductQuickUpdateController.php` (hàm `rows`)
- Modify: `Modules/MasterData/Routes/api.php` — trong nhóm `products`, đặt cạnh `/import` và trước `/{product}`:
  `Route::post('/quick-update/rows', 'V1\\Product\\ProductQuickUpdateController@rows')->middleware('checkPermission:' . $build);`
- Test: `Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php`

**Interfaces:**
- Consumes:
  - `Product::catesFromRaw()` (Task 1).
  - `ProductWriteService::editScope(Product): string` (`full`|`admin`).
  - `ProductWriteService::assertOwner`, dùng để lấy message 403/423 cho scope `none`.
  - `PRICING_LOCKED_FIELDS`.
- Produces: `ProductQuickUpdateService::rows(int[] $ids): array`. Cùng shape với response `data`:

```json
{ "rows": [{
    "id": 1, "code": "...", "model_name": "...", "brand_name": "...", "manufacture_name": "...", "barcode_name": "...",
    "type_path": "Tính chất / Nhóm chức năng / Nhóm SP / Loại SP",
    "edit_scope": "full|admin|none", "readonly_reason": null, "locked_fields": ["origin_id"],
    "values": { "name": "", "english_name": "", "product_type_id": 1, "product_cate": ["k"], "min_stock_qty": 0,
                "max_stock_qty": 0, "origin_id": 1, "customs_name": "", "hs_code": "", "vat_percent_tax_rate_id": 1,
                "import_tax_has_co_tax_rate_id": null, "import_tax_tax_rate_id": null, "antidump_duty_tax_rate_id": null,
                "min_buy_qty": 0, "note": "" } }],
  "options": { "product_types": [{"id":1,"name":"...","path":"..."}], "origins": [{"id":1,"name":"...","status":1}] } }
```

  - Thứ tự `rows` theo thứ tự `ids` gửi lên. Id không tồn tại hoặc là hàng tạm thì bỏ khỏi kết quả.
  - `options` chỉ chứa danh mục mà các dòng đang dùng, kể cả danh mục đã khoá.

- [ ] **Step 1: Write the failing tests**

```php
public function test_rows_requires_build_permission(): void        // actAs(c, []) ⇒ 403
public function test_rows_rejects_more_than_200_ids(): void         // 201 id ⇒ 422 lỗi 'ids'
public function test_rows_returns_scope_full_for_owner(): void      // edit_scope 'full', readonly_reason null, values.name đúng
public function test_rows_returns_scope_admin_for_foreign_product(): void
// edit_scope 'admin', readonly_reason === 'Hàng do công ty khác tạo — chỉ sửa được SL tồn tối thiểu.'
// values.min_stock_qty lấy theo công ty đang làm việc
public function test_rows_returns_scope_none_for_locked_product(): void   // edit_scope 'none', readonly_reason không rỗng
public function test_rows_marks_pricing_locked_origin(): void       // hàng đang tính giá ⇒ locked_fields chứa 'origin_id'
public function test_rows_reads_legacy_product_cate_formats(): void // product_cate '' và '["k2","k1"]' ⇒ [] và [k1,k2]
public function test_rows_keeps_request_order(): void
```

- [ ] **Step 2: Chạy, kiểm tra FAIL**

Run: `php artisan test Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php`

Expected: FAIL 404 (chưa có route).

- [ ] **Step 3: Implement**

- Controller validate inline: `ids` required|array|max:200, `ids.*` integer.
- Service:
  - Nạp hàng bằng 1 query, eager load model / brand / hãng / code / type path.
  - `min_stock_qty` lấy từ khối quản trị công ty đang làm việc, cùng nguồn `ProductHistoryService::company()` đang đọc.
  - Scope `none` khi `assertOwner` / `assertCanEditAdmin` ném 403/423: bắt `HttpException`, lấy `getMessage()`.

- [ ] **Step 4: Chạy, kiểm tra PASS**

Run: như Step 2. Expected: PASS.

- [ ] **Step 5: Commit**

`git commit -m "feat(products): API tải dòng cập nhật nhanh hàng hoá (#12191)"`

---

### Task 3: API lưu `PUT products/quick-update`

**Files:**
- Create: `Modules/MasterData/Http/Requests/Product/ProductQuickUpdateRequest.php`
- Modify:
  - `ProductQuickUpdateService.php` (thêm `save`)
  - `ProductQuickUpdateController.php` (thêm `update`)
  - `Routes/api.php`:
    `Route::put('/quick-update', '...ProductQuickUpdateController@update')->middleware('checkPermission:' . $build)->middleware('dueConfig:Cập nhật hàng hóa');`
- Test: `ProductQuickUpdateApiTest.php` (viết tiếp)

**Interfaces:**
- Consumes: `rows()` (Task 2, dùng để biết scope / locked_fields), `updatePartial`, `updateAdminPartial`, `withHistoryNote`.
- Request body: `{ "rows": { "<productId>": { ...các key ở Global Constraints } } }`. Dạng object có khoá là id, nên lỗi
  của FormRequest và của service đều có dạng `rows.<id>.<field>`.
- FormRequest rules:
  - `rows` required|array|max:200.
  - `rows.*.name` required|string|max:255.
  - `rows.*.product_type_id` required|integer|exists:product_types,id.
  - `rows.*.origin_id` required|integer|exists:origins,id.
  - `rows.*.product_cate` nullable|array; `rows.*.product_cate.*` in: các key của `PRODUCT_CATES`.
  - `rows.*.{min_stock_qty,max_stock_qty,min_buy_qty}` nullable|numeric|min:0.
  - 4 ô thuế nullable|exists:tax_rates,id.
  - `rows.*.{english_name,customs_name,hs_code}` nullable|string|max:255.
  - `rows.*.note` nullable|string.
  - Cách áp rule cho dòng `admin`: trong `prepareForValidation`, dòng `admin` chỉ giữ lại `min_stock_qty`, các khoá
    khác bị loại trước khi chạy rule. Rule `required` chỉ chạy với dòng `full`.
- Produces: `ProductQuickUpdateService::save(array $rows): array`, trả `['updated' => int, 'skipped' => int]`.
  - `skipped` là số dòng không có khoá nào thay đổi.
  - Không ghi gì thì vẫn trả 200, FE tự lo thông báo.
- Lỗi nghiệp vụ: `ValidationException::withMessages([...])` với khoá `rows.<id>.name` / `rows.<id>._row`.

- [ ] **Step 1: Write the failing tests**

```php
public function test_save_requires_permission(): void                 // 403
public function test_save_two_owner_rows_writes_and_logs_history(): void
// 2 hàng chủ, đổi name + max_stock_qty + product_cate ⇒ DB đổi; mỗi hàng 1 dòng lịch sử ghi chú 'Cập nhật nhanh'
// response data == ['updated' => 2, 'skipped' => 0]
public function test_save_foreign_row_only_writes_min_stock(): void
// dòng admin gửi name mới + min_stock_qty=7 ⇒ name KHÔNG đổi, admin.min_stock_qty == 7
public function test_save_duplicate_name_like_erp_rejects_whole_batch(): void
// dòng A trùng name+model+brand+manufacture với hàng khác ⇒ 422 errors['rows.A.name'][0] == 'Đã tồn tại trên hệ thống'; dòng B không ghi
public function test_duplicate_name_within_batch(): void              // A,B cùng khoá trùng ⇒ lỗi ở cả rows.A.name và rows.B.name
public function test_save_requires_type_and_origin_for_full_rows(): void  // thiếu ⇒ rows.<id>.product_type_id, rows.<id>.origin_id
public function test_save_ignores_pricing_locked_origin(): void       // hàng đang tính giá, gửi origin khác ⇒ origin giữ nguyên, không lỗi
public function test_locked_between_load_and_save_rolls_back(): void
// hàng B bị khoá (status ngừng KD) trước khi lưu ⇒ 422 'rows.B._row', hàng A không đổi
public function test_save_skips_unchanged_rows(): void                // gửi y giá trị cũ ⇒ updated 0, skipped 1, không lịch sử mới
```

- [ ] **Step 2: Chạy, kiểm tra FAIL**

Run: `php artisan test Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php`

Expected: các test `save_*` FAIL 404/405.

- [ ] **Step 3: Implement `save()`**

Thứ tự xử lý:
1. Nạp scope, locked_fields và giá trị hiện tại bằng `rows(array_keys($rows))`.
2. Bỏ các khoá trong `locked_fields`.
3. Chỉ giữ khoá có thay đổi: so sau chuẩn hoá, `product_cate` so theo `catesFromRaw`, số so theo float.
4. Kiểm trùng tên:
   - Với DB: so toàn bảng `products`, không lọc công ty và `status`, loại chính id đó.
   - Trong lô: gom các dòng theo khoá `mb_strtolower(trim(name))|model|brand|manufacture`, khoá nào ≥2 dòng thì mọi
     dòng đó đều lỗi.
   - Chỉ kiểm khi dòng đổi `name`.
5. Có lỗi ⇒ ném 1 `ValidationException` gộp lỗi mọi dòng.
6. `DB::transaction` cho cả lô:
   - scope `full` ⇒ `updatePartial($p, $changed + ['admin' => ['min_stock_qty' => …]])`. Khoá `admin` chỉ có khi đổi
     min_stock.
   - scope `admin` ⇒ `updateAdminPartial`.
   - Bắt `HttpException` 403/423 ⇒ rollback, ném lại `ValidationException` `rows.<id>._row` kèm message.

- [ ] **Step 4: Chạy toàn bộ test module hàng hoá**

Run: `php artisan test Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php Modules/MasterData/Tests/Feature/ProductQuickUpdateFieldsTest.php Modules/MasterData/Tests/Feature/ProductImportWriteUpdateTest.php`

Expected: PASS.

- [ ] **Step 5: Commit**

`git commit -m "feat(products): API lưu cập nhật nhanh hàng hoá (#12191)"`

---

### Task 4: FE model thuần + bảng sửa

**Files:**
- Create:
  - `components/product/quick-update/quickUpdateModel.js`
  - `components/product/quick-update/QuickUpdateTable.vue`
- Test: hrm-client không có jest ⇒ không viết unit test; hành vi của `quickUpdateModel.js` được kiểm qua Playwright ở
  Task 6.

**Interfaces:**
- Consumes: response `rows()` (Task 2).
- Produces:
  - `quickUpdateModel.js`:
    - `buildRow(apiRow) -> { ...apiRow, form: {...values}, original: {...values}, checked: apiRow.edit_scope !== 'none' }`
    - `changedKeys(row) -> string[]`: `product_cate` so theo tập hợp; dòng `admin` chỉ xét `min_stock_qty`.
    - `buildPayload(rows) -> { rows: { [id]: changedValues } }`: chỉ gồm dòng `checked` và có thay đổi.
      Dòng `full` gửi đủ `name`, `product_type_id`, `origin_id` để BE validate required.
    - `mapErrors(errors422) -> { [id]: { [field]: msg } }`
  - `<QuickUpdateTable :rows :options :errors @toggle>`:
    - Cột theo thứ tự ERP: tick, STT, Mã, Tên, Tên tiếng Anh, Model, Thương hiệu, Hãng SX, Nhóm hàng hoá (`type_path`),
      Tính chất (Loại SP), Loại hàng hoá, SL tồn tối thiểu, SL tồn tối đa, Code đặt hàng (chỉ đọc `barcode_name`),
      Xuất xứ, Tên khai báo HQ, HS code, % VAT, Thuế NK có CO, Thuế NK không CO, Thuế chống bán phá giá,
      SL tối thiểu nhập mua, Ghi chú.
    - Bọc trong `V2BaseTableScroll`. Select dùng `V2BaseSelect`. Ô khoá là `disabled`.
    - Dòng `none` không có checkbox.
    - Lỗi hiện đỏ dưới ô.
    - `readonly_reason` hiện dưới tên hàng, màu `#6b7280`.

- [ ] **Step 1:** Implement model + bảng. Các quy tắc phải đúng (Task 6 kiểm):
  - `cate [b,a]` so với `[a,b]` ⇒ không đổi.
  - Dòng admin đổi `name` ⇒ không đổi.
  - Dòng `none` không có trong payload.

   Options của select Tính chất / Xuất xứ / thuế:
  - Tải 1 lần qua `GET master-data/products/form-options`.
  - Gộp thêm `options` của API `rows` để danh mục đã khoá vẫn hiện tên.
- [ ] **Step 2:** Run `npx eslint components/product/quick-update`. Expected: sạch.
- [ ] **Step 3:** Commit `feat(products): bảng cập nhật nhanh hàng hoá (#12191)`.

---

### Task 5: Trang, popup Thêm hàng hoá, menu

**Files:**
- Create:
  - `pages/master-data/products/quick-update.vue`
  - `components/product/quick-update/QuickUpdatePickerModal.vue`
- Modify: `components/subsystem-menu/master-data.js`, thêm sau mục "Hàng đang kinh doanh" (khoảng dòng 104):

```js
{
    label: 'Cập nhật nhanh hàng hoá',
    info: 'Sửa hàng loạt thông tin nhiều mã hàng trong một bảng.',
    link: '/master-data/products/quick-update',
    codes: ['master_data.thong_tin_hang_hoa.manage'],
},
```

  Field `isShow` / `codes` viết theo đúng cách các mục gate quyền khác trong file (vd "Hàng hoá nhập thông tin").

**Interfaces:**
- Consumes: Task 4 (`quickUpdateModel.js`, `QuickUpdateTable`), API Task 2 + 3.
- `QuickUpdatePickerModal` props: `show`, `existingIds: number[]`; emit `picked(ids: number[])`.
  - Bên trong là `ProductPickerPanel`, cấu hình giống `QuotationProductSearchModal.vue:82-104`:
    - `:company-id` = công ty đang làm việc.
    - `:price-type-id="1"`, `:existing-ids`, `stock-extra-columns`, `tree-max-height`, `table-max-height`.
    - Không có slot "Thêm hàng tạm", không có tab BOM.
  - Nút "Chọn" emit các id đã tick. `@quick-pick` (bấm tên hàng) emit 1 id ngay.

**Hành vi trang:**
- Thêm hàng:
  - Id đã có trong bảng thì bỏ qua.
  - Gọi `rows` theo từng cụm ≤200 id, nối thêm vào cuối bảng.
- Phân trang FE 20 dòng/trang. `form` của dòng nằm trong state trang nên giữ được khi chuyển trang.
- Nút "Xoá dòng đã chọn" chỉ bỏ dòng khỏi bảng.
- "Cập nhật" (`V2Footer` `#custom-actions`):
  - `buildPayload` rỗng ⇒ toast `Không có thay đổi nào để cập nhật`, không gọi API.
  - 422 ⇒ `mapErrors`, chuyển tới trang của dòng lỗi đầu tiên, giữ nguyên giá trị user nhập.
  - 200 ⇒ toast thành công, `markFormSaved()`, làm trống bảng.
- `unsavedChangesMixin`: coi là dirty khi có dòng mà `changedKeys` khác rỗng.

- [ ] **Step 1:** Implement trang + modal + menu.
- [ ] **Step 2:** `npx eslint pages/master-data/products/quick-update.vue components/product/quick-update`. Expected: sạch.
- [ ] **Step 3:** Chạy local (skill `run-hrm`), mở `/master-data/products/quick-update`:
  - Menu hiện mục mới.
  - Popup mở được, chọn 2 hàng ⇒ bảng có 2 dòng.
- [ ] **Step 4:** Commit `feat(products): màn Cập nhật nhanh hàng hoá + popup chọn hàng như Báo giá (#12191)`.

---

### Task 6: Playwright E2E

**Files:**
- Create: `HRM/e2e/tests/product-quick-update.spec.ts`
- Theo cấu trúc spec có sẵn, vd `tests/bonus-month-report.spec.ts`. KHÔNG ghi đè `e2e/.auth/user.json`.

- [ ] **Step 1:** Viết các test:
  - `thêm 2 hàng qua popup, sửa tên + Loại hàng hoá, lưu thành công, bảng trống`.
  - `để trống Xuất xứ ⇒ lỗi đỏ dưới ô Xuất xứ của đúng dòng, giá trị khác không mất`.
  - `dòng lỗi ở trang 2 ⇒ tự chuyển sang trang 2`. Cần 21 hàng trở lên.
  - `hàng công ty khác ⇒ chỉ ô SL tồn tối thiểu sửa được, có ghi chú xám`.
  - `bấm Cập nhật không đổi gì ⇒ toast "Không có thay đổi nào để cập nhật"`.
- [ ] **Step 2:** Run `cd HRM/e2e && npx playwright test tests/product-quick-update.spec.ts`. Expected: 5 passed.
- [ ] **Step 3:** Commit `test(e2e): cập nhật nhanh hàng hoá (#12191)`.

---

## Sau khi xong

- Deploy chỉ cần `php artisan route:cache`.
- Mã quyền `master_data.thong_tin_hang_hoa.manage` đã có sẵn, không cần `permission:catalog-sync`.
- Báo user. User cho phép thì merge worktree vào `develop` 2 repo rồi push.
- Redmine #12191: chuyển "Code xong chờ test".
