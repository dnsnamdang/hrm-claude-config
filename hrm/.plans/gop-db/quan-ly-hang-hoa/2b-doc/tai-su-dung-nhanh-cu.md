# 2-B Đọc — kiểm kê tái sử dụng code nhánh cũ `feat/p1-danh-muc-hang-hoa`

> Lập 04/10/2026 · chỉ đọc git (`git show` / `git diff`), không checkout, không sửa repo.
> Nhánh đích: `feat/chuyen-doi-hang-hoa` (api `15610ea2a`, client cùng tên). Nhánh cũ **đóng băng, KHÔNG merge** (E1).
> Merge-base api: `0833f1a41` · client: `bee1c02d3`.
> Phạm vi: chỉ phần **hàng hoá** (Product*). 11 danh mục P1 + 6 danh mục Xe đã lên nhánh chung qua cherry-pick 02/10 → không kiểm lại.

---

## 0. Tóm tắt một màn hình

| Nhóm | Kết luận |
|---|---|
| Entity `Product` + 13 bảng con | **Tái sử dụng có sửa** — docblock bẫy rất giá trị; phải đổi `extends BaseModel`, gỡ 2 cột phân loại, thay `ProductCompanyCoefficient` bằng `ProductCompany` đã có |
| `ProductService` (index/show) | **Tái sử dụng có sửa nhiều** — khung query tốt (subquery tên NV, EXISTS, không N+1) nhưng lọc theo `products.status` / `products.company_id` / `product_type_id` là sai mô hình mới |
| `ProductListResource` / `ProductDetailResource` | **Viết lại trên khung cũ** — trạng thái, tab Giá bán, Dữ liệu quản trị, `rate_liquidation` đều lệch quyết định |
| `ProductPricePermission` (gate giá vốn) | **Tái sử dụng nguyên** (sau khi đo lại DB) — đây là chỗ đáng lấy nhất |
| `ProductOptionService` + Controller | **Tái sử dụng có sửa** — 14 khoá, `include_ids`, `option-search`, `vehicle-options` dùng được; bỏ `price_types`, thêm catalog/nhóm máy |
| Route `products` + quyền 1616–1619 | **BỎ** — id đã thuộc *Công nợ đầu kỳ*; 9/15 route trỏ method không tồn tại |
| 4 migration | **BỎ cả 4** khỏi 2-B (2 cái cần quyết định riêng — xem §6) |
| `ProductCodeGenerator` + test, `ProductRequest` | Không thuộc 2-B → để 2-C |
| FE (mockup Vue 21/09, Loại sản phẩm 2 ô tick, utils, menu) | **BỎ** — mockup lỗi thời; utils/menu nhánh chung MỚI HƠN nhánh cũ |

---

## 1. Kiểm kê file — hrm-api

Cột *Biên dịch trên nhánh chung*: ✅ chạy được nếu chép sang · ⚠️ chạy được nhưng sai/lệch dữ liệu · ❌ lỗi.

| File (dưới `Modules/MasterData/`) | Dòng | Commit | Mục đích | Biên dịch trên nhánh chung |
|---|---:|---|---|---|
| `Entities/Product/Product.php` | 323 | 799b117 · cf5c489 · a5c438d | Entity bảng `products` (57 cột), 18 quan hệ, chặn đổi `code` ở `boot()` | ⚠️ `$fillable` + `productType()`/`characteristic()` trỏ cột `product_type_id`, `product_characteristic_id` **không có trong migration của nhánh chung** → eager load sinh SQL `where id in (null)` vô hại, nhưng `select products.product_type_id` / lọc theo nó sẽ **lỗi cột không tồn tại trên DB sạch** (DB local `hrm_erp` thì có vì migration cũ đã chạy — lỗi chỉ lộ ở môi trường khác). Không `extends BaseModel` (vi phạm quy tắc mới) |
| `Entities/Product/ProductUnit.php` | 60 | 799b117 | `product_units` (ĐVT + giá vốn/giá mua + cột chờ duyệt) | ✅ |
| `Entities/Product/ProductUnitPrice.php` | 47 | 799b117 · cbcb359 | `product_unit_prices` (giá theo loại giá) + `expectedPrices()` | ✅ (2-B không cần — giá tách khỏi form) |
| `Entities/Product/ProductExpectedPrice.php` | 39 | cbcb359 | `product_expected_prices` | ✅ (không cần cho 2-B) |
| `Entities/Product/AttributeProduct.php` | 50 | 799b117 | `attribute_products` → `ErpAttribute`, `AttributeUnit(unittech_id)` | ✅ (`ErpAttribute`, `AttributeUnit` có trên nhánh chung) |
| `Entities/Product/ProductSupplier.php` | 32 | 799b117 | `product_suppliers` → `customers` | ⚠️ thiếu `company_id` trong `$fillable` (2-A đã thêm cột, NOT NULL DEFAULT 1) |
| `Entities/Product/ErpSupplier.php` | 16 | 799b117 | `customers` chỉ đọc | ✅ |
| `Entities/Product/ProductTechAttachment.php` | 31 | 799b117 | `product_tech_attachments` → `AttachmentType` | ✅ |
| `Entities/Product/ProductGallery.php` | 26 | 799b117 | `product_galleries` | ✅ |
| `Entities/Product/ProductVideo.php` | 26 | 799b117 | `product_videos` | ✅ |
| `Entities/Product/ProductCompanyCoefficient.php` | 26 | 799b117 | `product_company_coefficients` (chỉ 3 cột) | ⚠️ **trùng bảng** với `ProductCompany` của 2-A (đủ `status` + 4 cột quản trị) → BỎ |
| `Entities/Product/RecipeProduct.php` | 45 | 799b117 | `recipe_products` (định mức, `base_product_id`) | ✅ |
| `Entities/Product/ProductHasAccessory.php` | 39 | 799b117 | `product_has_accessories` | ✅ |
| `Entities/Product/ProductHasInstallAccessory.php` | 39 | 799b117 | `product_has_install_accessories` | ✅ |
| `Entities/Product/ProductHasRepairAccessory.php` | 32 | 799b117 | `product_has_repair_accessories` (không có `unit_id`/`qty`) | ✅ |
| `Entities/Product/PriceType.php` | 19 | 4f91847 | `price_types` (6 loại giá) | ✅ (2-B không cần) |
| `Entities/Product/Productable.php` | 59 | cf5c489 | `productables` | — **đã có y hệt trên nhánh chung** |
| `Services/Product/ProductService.php` | 203 | cbcb359 · cf5c489 | `index()` + `show()` | ⚠️ chạy được trên DB local, **sai mô hình** (xem §2) và lỗi cột trên DB sạch |
| `Services/Product/ProductPricePermission.php` | 78 | cbcb359 | Gate giá vốn đọc chéo guard `web` | ✅ |
| `Services/Product/ProductOptionService.php` | 371 | 4f91847 · cf5c489 | `/form-options` 14 khoá + `option-search` + `vehicle-options` | ✅ (mọi entity tham chiếu đều có trên nhánh chung, `App\Models\Company` có) |
| `Services/Product/ProductCodeGenerator.php` | 184 | 869a3bb · a5c438d | Sinh mã hàng hoá | ✅ — thuộc 2-C |
| `Http/Controllers/V1/Product/ProductController.php` | 38 | cbcb359 | `index` + `show` | ✅ |
| `Http/Controllers/V1/Product/ProductOptionController.php` | 60 | 4f91847 · cf5c489 | `formOptions`, `vehicleOptions`, `optionSearch` | ✅ |
| `Http/Requests/Product/ProductRequest.php` | 220 | b833d76 (đã gỡ khối giá) | Validate tạo/sửa | ⚠️ có rule `product_type_id`/`rate_liquidation`… — thuộc 2-C |
| `Transformers/Product/ProductListResource.php` | 67 | cbcb359 | 1 dòng danh sách (12 cột mockup 21/09) | ⚠️ đọc `product_type_id`; trạng thái lấy `products.status` |
| `Transformers/Product/ProductDetailResource.php` | 272 | cbcb359 · cf5c489 | Chi tiết 6 tab | ⚠️ còn tab Giá bán, admin_data từ cột chung `products`, `rate_liquidation` |
| `Routes/api.php` (khối `products`) | +45 | 6d5fa86 · 4f91847 · cf5c489 | 17 route | ❌ quyền 1616–1619 trùng *Công nợ đầu kỳ*; 9 route trỏ method chưa viết (`store/update/delete/copy/lock/unlock/export/exportRows/import/validateImport/bulkDelete/attributesByType`) |
| `Database/Seeders/PermissionsTableSeeder.php` (Timesheet) | +21 | 6d5fa86 | 4 quyền 1616–1619 | ❌ id đã thuộc *Công nợ đầu kỳ* trên nhánh chung (1615 *Quản lý công nợ đầu kỳ* · 1616–1619 *Xem tất cả công nợ đầu kỳ…*) |
| `Migrations/2026_09_22_000001_add_classification_to_products_table.php` | 49 | c59fc90 | + `product_type_id`, `product_characteristic_id` (nullable, index, không FK) | — đổi schema bảng ERP, cần duyệt (§6) |
| `Migrations/2026_09_22_000002_drop_can_retail_from_product_types_table.php` | 38 | 259ad55 | DROP `product_types.can_retail` | ❌ nhánh chung **vẫn đọc/ghi `can_retail`** (`ProductType` `$fillable` + `$casts`) |
| `Migrations/2026_09_22_000003_add_updated_at_index_to_products_table.php` | 38 | cbcb359 | index `(updated_at, id)` trên `products` | ✅ — đề xuất lấy lại (đổi schema → cần duyệt) |
| `Migrations/2026_09_24_000001_add_declare_flags_to_product_types_table.php` | 39 | b833d76 | + `declare_vehicle`, `declare_machine_group` (boolean) | ✅ nhưng không thuộc 2-B |
| `Entities/ProductClassification/ProductType.php` · `ProductTypeRequest/Service/Resource` · `ExportColumnRegistry` · `CatalogHistoryService` | nhỏ | 259ad55 · b833d76 | gỡ `can_retail`, thêm 2 cờ | không thuộc 2-B |
| `Tests/Feature/ProductCodeGeneratorTest.php` | 217 | 869a3bb · a5c438d | 9 ca sinh mã (ghi DB thật, dọn ở tearDown theo token `PCGT`) | thuộc 2-C |

⚠️ Bẫy DB local: theo sổ chốt, **4 migration cũ đã chạy vào `hrm_erp`** (batch 410–414): `products` ĐANG có 2 cột phân loại + index, `product_types` ĐÃ MẤT `can_retail` và ĐANG có 2 cờ. Hệ quả cho 2-B: test trên local sẽ "xanh" với code đọc `product_type_id` dù nhánh chung không có migration; còn màn Loại sản phẩm của nhánh chung đang ghi `can_retail` sẽ lỗi trên local. Phải xử lý trước khi đo/nghiệm thu 2-B.

## 2. Kiểm kê file — hrm-client

| File | Dòng (nhánh cũ) | Mục đích | Đánh giá |
|---|---:|---|---|
| `pages/master-data/mockup-hang-hoa/index.vue` | 241 | Mockup danh sách (dữ liệu tĩnh, không gọi API) — 10 ô lọc, 12 cột | Lỗi thời: bản 21/09, có cột/lọc *Công ty quản lý* (đã bỏ §35-1), không có 4 màn theo trạng thái |
| `pages/master-data/mockup-hang-hoa/form.vue` | 889 | Mockup form 5–6 tab, tĩnh | Lỗi thời: một tầng tab (nay 2 tầng §30g), còn dấu vết tab Giá, chưa có tab *Quản trị hàng hoá* 4 cột catalog |
| `pages/master-data/product-types/{index,AddProductTypeModal}.vue` | ±150 | Gỡ `can_retail`, thêm 2 ô tick | Không thuộc 2-B; đi cùng migration cờ |
| `utils/product-classification.js` | ±20 | Gỡ `CAN_RETAIL_OPTIONS` | Nhánh chung **mới hơn** (có `is_locked`, tooltip catalog) — lấy bản cũ là lùi |
| `components/subsystem-menu/master-data.js` | ±36 | — | Nhánh chung **mới hơn** (menu Catalog kinh doanh, Quy chế đã dời) — lấy bản cũ là mất menu |
| e2e / test FE cho hàng hoá | 0 | — | **Không có** ca e2e nào cho hàng hoá trên nhánh cũ |

Các màn danh mục P1/Xe (~22 file) đã có trên nhánh chung — không liên quan.

---

## 3. API danh sách + chi tiết trên nhánh cũ

### 3.1. Endpoint (đã khai 17, chỉ 5 có method thật)

| Route | Method | Middleware |
|---|---|---|
| `GET /products` | `ProductController@index` | `checkPermission:Quản lý danh mục hàng hoá\|Xem danh mục hàng hoá` |
| `GET /products/{product}` | `ProductController@show` | như trên |
| `GET /products/form-options` | `ProductOptionController@formOptions` | như trên |
| `GET /products/option-search?type=&keyword=&limit=` | `@optionSearch` | như trên |
| `GET /products/vehicle-options` | `@vehicleOptions` | như trên |

Response: `index` qua `apiGetList(ProductListResource::apiPaginate(...))`; các route khác `responseJson('success', 200, ...)`.

### 3.2. `index` — hình dạng query

- `Product::query()->select(15 cột products.*)` + `with(LIST_RELATIONS)`:
  `brand:id,name` · `productModel:id,name` · `productType:id,name,product_family_id` · `.family` · `.family.functionGroup` · `.family.functionGroup.nature`.
- 3 subquery trong SELECT (không join, để COUNT phân trang không phình): `creator_name`, `updater_name` (`employees` → `employee_infos.fullname`), `base_unit_name` (`product_units.is_base = 1` → `units.name`).
- Bộ lọc: `product_type_id` trực tiếp; `product_family_id` / `product_function_group_id` / `product_nature_id` bằng `whereIn(subquery product_types join …)`; `product_characteristic_id`; phẳng `brand_id, manufacture_id, origin_id, company_id, model_id`; `status` (chấp nhận 0); `unit_id` bằng `whereExists product_units`; `keyword` (đã `escapeLikeKeyword`) trên `code, name, barcode` + `EXISTS product_models.name`.
- Sắp xếp: whitelist `code/name/updated_at`, luôn chốt `id desc`; mặc định `updated_at desc, id desc` (dựa vào index migration 000003).
- Số đo trong commit: 20 và 100 dòng đều **5 query**; không index 119 ms → có index 0 ms.

### 3.3. `show` — eager load

`LIST_RELATIONS` + `characteristic, manufacturer, origin, orderCode, units.unit, units.prices, productAttributes.attribute, productAttributes.attributeUnit, suppliers.supplier, techAttachments.attachmentType, galleries, videos, companyCoefficients, recipeProducts.product/unit, accessories.product/unit, installAccessories.product/unit, repairAccessories.product, vehicleManufactLinks, vehicleBrandLinks, vehicleModelLinks` + `products.*` + 2 subquery tên NV → `findOrFail`. Đo: 22–27 query bất kể số dòng con.

### 3.4. Trường trả về

- **List (`ProductListResource`)**: `id, code, name, avatar, barcode, product_type_id, product_type_name, classification_path ("TC → NCN → NSP"), brand_id/name, model_id/name, unit_name, vat_percent, status, status_text ("Đang kinh doanh"/"Đã khoá" theo products.status), creator_name, updater_name, created_at, updated_at (d/m/Y H:i), is_can_edit, is_can_delete (= status==1)`.
- **Detail (`ProductDetailResource`)** theo 6 tab: Thông tin chung (phân loại + path object, tên, model, barcode/orderCode, serial, brand/manufacturer/origin, company_id, avatar, norm, weight, size, note, comment, units[], galleries[], videos[]) · Thông số (attributes[], 3 cột chuỗi mô tả, tech_attachments[], recipe_products[] có `is_main`, accessories[], install_accessories[], repair_accessories[]) · Mua hàng (customs_name, hs_code, 4 thuế + tax_rate_id, môi trường, min_buy_qty, **rate_liquidation**, suppliers[]) · Dữ liệu quản trị `admin_data` (**lấy từ cột chung `products`**: min/max_stock, guarantee, guarantee_type, tech_coefficient, promotion, company_coefficients[]) · **Giá bán** (`can_view_price`, `prices[]` theo ĐVT: cost_price, buy_price, %max, wait_approve, by_type[] 6 loại giá) · Phân loại xe (3 mảng id) · chân trang (is_can_edit/delete, creator/updater, thời gian).

### 3.5. Gate giá vốn — cách làm

`ProductPricePermission::canManagePrice()`:
- **Không** dùng `isCurrentEmployeeHasPermission('Quản lý giá')` vì quyền này chỉ có ở guard `web` (ERP #100127); spatie lọc theo guard ⇒ gate bằng tên là **cổng chết** (không ai xem được, không lỗi).
- Đọc **chéo guard**: `employee_has_roles → role_has_permissions → permissions(name='Quản lý giá', guard_name='web')` HOẶC `employee_has_permissions` cấp thẳng. Nhớ trong request theo `auth()->id()` (`static $cache`, có `forgetCache()` cho test).
- Áp ở Resource: `cost_price`, `buy_price`, khối `wait_approve` của ĐVT ⇒ `null` khi không có quyền; trả `can_view_price` cho FE. ⚠️ Giá theo loại giá (`by_type[*].price` + `wait_approve` của nó) **không** bị gate — đúng tiền đề 5 (giá bán không bảo mật).
- Đo trong commit: NV #13 thấy 62.805/1.256.100, NV #144 nhận `null`. 133 NV đang giữ ≥1 trong 23 role có quyền.
- Nhánh chung: seeder **không có** quyền `api` tên `Quản lý giá` ⇒ lý do của lớp này vẫn còn nguyên.

### 3.6. Test

| Loại | Có gì | Kết quả |
|---|---|---|
| PHPUnit list/detail/options | **Không có ca nào** | — kiểm bằng tay qua HTTP/SQL thô, ghi trong commit message (cbcb359, 4f91847, cf5c489) |
| PHPUnit sinh mã | `ProductCodeGeneratorTest` 9 ca | commit báo **9/9 xanh** (a5c438d); `ProductClassificationCatalogTest 11/11` (b833d76) |
| PHPUnit gate giá | Không có | chỉ kiểm tay 2 NV |
| e2e Playwright | **Không có** cho hàng hoá (mockup không gọi API) | — |

⇒ 2-B phải tự viết test: list (4 màn × có/không quyền), detail không gate quyền xem, gate giá vốn có/không quyền `Quản lý giá` (memory *always-test-permission-cases*).

---

## 4. `/form-options` — 14 danh mục

Một request, đo 13 query / 163 ms / 179 KB. Quy tắc chung `whereActiveOrIncluded`: `status = hoạt động` **hoặc** id nằm trong `include_ids[<khoá>]` (nhận mảng hoặc chuỗi `6,7`), trả `is_locked` để FE gắn 🔒.

| # | Khoá | Nguồn | Ghi chú |
|---|---|---|---|
| 1 | `product_types` | `DB::table` join `product_families` → `product_function_groups` → `product_natures` (inner join, 1 query) | trả `family_id` + `path{nature, nature_id, function_group, function_group_id, family}`; sắp theo n→g→f→t |
| 2 | `product_characteristics` | `ProductCharacteristic` + `code` | bảng mới, khoá = 2 |
| 3 | `brands` | `Brand` + `code` | bảng ERP, khoá = 0 |
| 4 | `manufacturers` | `Manufacturer` (`manufactures`) + `code` | |
| 5 | `origins` | `Origin` | |
| 6 | `units` | `Unit` + `can_be_base` | |
| 7 | `attribute_units` | `AttributeUnit` (`unitteches`) | |
| 8 | `business_policies` | `BusinessPolicy` + `code` | |
| 9 | `tax_rates` | `TaxRate` cột `tax_rate`, `name` = "x%" | **không** lọc `is_sales_tax/is_purchases_tax` (0/40 dòng bật) |
| 10 | `companies` | `App\Models\Company` + `code`, active = 1 truyền tay | |
| 11 | `price_types` | `PriceType` sắp theo `order` | không có `status` |
| 12 | `product_models` | `ProductModel` — **chỉ trả id trong include_ids** | 39.796 dòng |
| 13 | `order_codes` | `OrderCode` (`barcodes`) — chỉ include_ids | 8.664 dòng |
| 14 | `suppliers` | `DB::table('customers') is_supplier=1, deleted_at null` — chỉ include_ids | 10.094 dòng |

Kèm: `GET /option-search` (3 danh mục lớn, `limit` mặc định 50, trần 200, `type` lạ → 400) và `GET /vehicle-options` (3 cấp xe ~1.660 dòng, 151 KB, tách riêng vì gộp vào làm payload 179→327 KB; trả hết + `is_locked`, không dùng include_ids).

Lưu ý: `is_locked = status !== active` — với bảng ERP khoá = 0 và bảng mới khoá = 2 đều đúng vì so với **hoạt động = 1** (không mắc bẫy `=== 2`).

---

## 5. Entity `Product` + 13 bảng con

| Entity | Bảng | Khoá nối về hàng hoá | Quan hệ đi ra |
|---|---|---|---|
| `Product` | `products` (45.890) | — | `productType(product_type_id)`, `characteristic(product_characteristic_id)`, `brand`, `manufacturer(manufacture_id)`, `origin`, `productModel(model_id)`, `orderCode(barcode_id → barcodes)`; hasMany bên dưới; 3 quan hệ xe lọc `productable_type`; `scopeActive` |
| `ProductUnit` | `product_units` (46.560) | `product_id` | `unit`, `prices` |
| `ProductUnitPrice` | `product_unit_prices` (264.646) | `product_unit_id` | `expectedPrices(unit_price_id)` |
| `AttributeProduct` | `attribute_products` (51.128) | `product_id` | `attribute → ErpAttribute`, `attributeUnit(unittech_id)` |
| `ProductSupplier` | `product_suppliers` (1.741) | `product_id` | `supplier → ErpSupplier (customers)` |
| `ErpSupplier` | `customers` | — | chỉ đọc |
| `ProductTechAttachment` | `product_tech_attachments` (35) | `product_id` | `attachmentType` |
| `ProductGallery` | `product_galleries` (1.548) | `product_id` | sắp `position` |
| `ProductVideo` | `product_videos` (2) | `product_id` | sắp `position` |
| `ProductCompanyCoefficient` | `product_company_coefficients` (1.105) | `product_id` | — |
| `RecipeProduct` | `recipe_products` (6.438) | **`base_product_id`** | `product` (thành phần), `unit`; `is_main` |
| `ProductHasAccessory` | `product_has_accessories` (989) | **`base_product_id`** | `product`, `unit` |
| `ProductHasInstallAccessory` | `product_has_install_accessories` (28) | **`base_product_id`** | `product`, `unit` |
| `ProductHasRepairAccessory` | `product_has_repair_accessories` (5) | **`base_product_id`** | `product` — **không có** `unit_id`, `qty` |

Bẫy ghi trong docblock (phải chép theo khi viết lại):
1. **Không `SoftDeletes`** dù `products` có `deleted_at`: 175 hàng `status = 1` vẫn có `deleted_at`; bật trait là mất 175 mã im lặng. `status` mới là trạng thái thật (trên `products`).
2. Quan hệ tên **`productType()`** (không `product_type()` — trùng cột chuỗi `products.product_type` enum cũ) và **`productAttributes()`** (không `attributes()` — trùng thuộc tính nội bộ Eloquent; còn có cột chuỗi `products.product_attributes`).
3. **`code` sinh một lần, không bao giờ đổi** — `boot()` ném `RuntimeException` khi `isDirty('code')` ở `updating` (231/45.890 mã lệch với nguồn hiện tại).
4. **Không extends BaseModel** — lý do cũ: hook tự gán `created_by/updated_by`. ⚠️ Mâu thuẫn quy tắc mới (xem §6-7).
5. 4 bảng phụ kiện/định mức nối bằng **`base_product_id`**; nối nhầm `product_id` là ra danh sách ngược.
6. `productables`: **không `morphedByMany()`** (cột lưu tên class ERP); 5 loại chung bảng, mọi thao tác kẹp `productable_type`, không bao giờ xoá theo mỗi `product_id` (32.366 dòng Nhóm máy/Máy sử dụng ERP vẫn đọc).
7. `ProductUnit` / `ProductUnitPrice`: nhóm cột `*_wait_approve` là luồng duyệt giá ERP — giữ nguyên.
8. `ProductExpectedPrice.unit_price_id` trỏ `product_unit_prices.id`, **không** phải `product_units.id`.
9. `manufacture_id` (thiếu chữ r) — cột ERP, không sửa.

---

## 6. Đề xuất theo từng file

### hrm-api

| File | Đề xuất | Việc phải sửa / lý do |
|---|---|---|
| `Entities/Product/Product.php` | **Tái sử dụng có sửa** | (1) `extends App\Models\BaseModel` theo quy tắc mới — 2-B chỉ đọc nên hook `creating` không chạy; ghi chú cho 2-C: hook `creating` của BaseModel tự gán `company_id = info->company_id` (**không** phải `company_role`) → đường tạo phải gán tay. (2) Gỡ `product_type_id`, `product_characteristic_id` khỏi `$fillable` và 2 quan hệ **cho tới khi** user duyệt migration phân loại. (3) Thay `companyCoefficients()` bằng `companies()` → `ProductCompany`; thêm `businessCatalogs()` → `ProductBusinessCatalog`; thêm quan hệ `companyRow()` (hasOne theo công ty hiện tại) cho màn công ty. (4) Giữ nguyên docblock 1–5, `boot()` chặn đổi `code`, 3 quan hệ xe. (5) `STATUS_ACTIVE/DELETED` giữ, nhưng ghi rõ: đây là trạng thái **bản ghi ERP**, không phải trạng thái quy trình |
| `ProductUnit`, `AttributeProduct`, `ErpSupplier`, `ProductTechAttachment`, `ProductGallery`, `ProductVideo`, `RecipeProduct`, `ProductHasAccessory`, `ProductHasInstallAccessory`, `ProductHasRepairAccessory` | **Tái sử dụng**, đổi `extends BaseModel` | Giữ docblock. `ErpSupplier` (bảng `customers`) — cân nhắc giữ `Model` vì chỉ đọc bảng ERP lớn; nếu bắt buộc BaseModel thì vô hại khi chỉ đọc |
| `ProductSupplier` | **Tái sử dụng có sửa** | thêm `company_id` vào `$fillable` + quan hệ `company`; chi tiết phải **lọc theo công ty hiện tại** |
| `ProductUnitPrice`, `ProductExpectedPrice`, `PriceType` | **Để lại** (không chép ở 2-B) | giá tách khỏi form (§18a/§20) → Phase 8 |
| `ProductCompanyCoefficient` | **BỎ** | trùng bảng với `ProductCompany` (2-A) — 2 entity một bảng là mầm lệch `$fillable` |
| `Services/Product/ProductService.php` | **Tái sử dụng có sửa nhiều** | Giữ: khung select + 3 subquery, `whereExists` ĐVT, ô tìm nhanh (`escapeLikeKeyword` có ở `app/Helper/FormatHelper.php`), whitelist sắp xếp, chốt `id desc`. Đổi: (a) tách 4 phạm vi màn — *Kho dữ liệu* (mọi công ty, không gate quyền xem, thêm cột *Công ty đang kinh doanh* = các `product_company_coefficients.status=3`), *Dữ liệu hàng hoá công ty* (`EXISTS pcc.company_id = current_company_role`, mọi status), *Nhập thông tin* (`status=1`), *Đang kinh doanh* (`status=3`, KHÔNG bắt buộc catalog — C5, kèm đếm "chưa xếp catalog" + lọc "Chưa xếp catalog" — C5-b); (b) công ty hiện tại = `auth()->user()->current_company_role` (đã có fallback `company_id` trong `TpEmployee`); (c) bỏ lọc `products.company_id`, `products.status` làm trạng thái; (d) gỡ/hoãn lọc cây phân loại cho tới khi có cột `product_type_id`; (e) thêm lọc 4 cấp catalog qua `product_business_catalogs` → `job_clusters` → `job_groups` → `chapters`; (f) `show()`: bỏ `units.prices`, `companyCoefficients`; thêm `companies` + `businessCatalogs.jobCluster.jobGroup.chapter` + `suppliers` lọc công ty |
| `Services/Product/ProductPricePermission.php` | **Tái sử dụng nguyên** | Trước khi dùng: đo lại DB gộp `permissions` xem đã có `Quản lý giá` guard `api` chưa; nếu vẫn chỉ `web` ⇒ giữ đọc chéo guard. Thêm PHPUnit có quyền / không quyền. Lưu ý `static $cache` sống qua nhiều request trong 1 tiến trình test → gọi `forgetCache()` ở `setUp` |
| `Services/Product/ProductOptionService.php` | **Tái sử dụng có sửa** | Giữ: khung `options()` / `whereActiveOrIncluded` / `includeIds`, 3 danh mục lớn + `search()`, `vehicleOptions()`. Bỏ: `price_types`. Cân nhắc bỏ `companies` (form không còn ô Công ty quản lý). Thêm: cây catalog (Chương/Mục/Tiểu mục chỉ nhánh gốc mới — H3) nếu form chỉ xem cần hiển thị tên; nguồn Nhóm máy (F1–F5) khi làm tab đó. `product_types` giữ nhưng chỉ có ý nghĩa khi có cột phân loại. 2-B chỉ đọc ⇒ `/form-options` có thể thu về đúng các khoá cần hiển thị tên (detail đã trả sẵn `*_name` thì không cần gọi) |
| `Http/Controllers/V1/Product/ProductController.php` | **Tái sử dụng có sửa** | tách `index` thành 4 action (hoặc 1 action + tham số `scope`), `show` giữ |
| `Http/Controllers/V1/Product/ProductOptionController.php` | **Tái sử dụng nguyên** | |
| `Transformers/Product/ProductListResource.php` | **Viết lại trên khung cũ** | `status`/`status_text` lấy từ dòng `product_company_coefficients` của công ty (1 Đang nhập thông tin · 2 Chờ tính giá · 3 Đang kinh doanh), không từ `products.status`; thêm cột catalog (Tiểu mục), cột *Công ty đang kinh doanh* cho màn Kho; bỏ `product_type_*` tới khi có cột; `is_can_edit/delete` phải theo §35 (quyền *Xây dựng thông tin*, công ty tạo, trạng thái 1) — 2-B chỉ đọc thì có thể trả `false`/bỏ |
| `Transformers/Product/ProductDetailResource.php` | **Viết lại trên khung cũ** | Bỏ cả khối **Giá bán** (`prices`, `by_type`) — nhưng giữ helper `soHoacNull` và gate nếu còn hiện giá vốn ở đâu; bỏ `rate_liquidation` (F8); `admin_data` đọc từ `ProductCompany` của công ty hiện tại (`business_policy_id`, `min_stock_qty`, `guarantee`, `guarantee_type`), không từ cột chung `products`; `suppliers` lọc theo công ty; thêm catalog nhánh; giữ `kemTheo()`, tab Phân loại xe (3 mảng id); thêm khối Nhóm máy (`productables` loại Group/Product) nếu form chỉ xem có tab đó — đọc thôi, không đụng ghi |
| Khối route `products` | **Viết lại** | chỉ khai 4 route đọc + `form-options` / `option-search` / `vehicle-options`; **detail không gate quyền xem** (§35-3); Kho dữ liệu + Đang kinh doanh không cần quyền; *Dữ liệu hàng hoá công ty* gate `Xây dựng thông tin hàng hoá\|Xem dữ liệu hàng hoá công ty`; route tĩnh đứng trước `/{product}` (giữ bài học cũ) |
| Seeder 4 quyền 1616–1619 | **BỎ** | thay bằng 1652–1656 (§35-5): 2-B cần 1652, 1653 (gate màn công ty); id nhánh chung đang dừng ở 1675 — kiểm `uniq -d` + DB local trước khi seed, KHÔNG chạy cả seeder |
| Migration `add_classification_to_products_table` | **Chưa lấy — hỏi user** | 2-A không thêm cột; không có nó thì 2-B không lọc/hiện được Loại sản phẩm + Đặc tính. Đổi schema bảng ERP ⇒ ngoại lệ tiền đề 1, phải duyệt riêng; DB local đã có sẵn cột (batch cũ) |
| Migration `drop_can_retail` | **BỎ** khỏi 2-B | nhánh chung vẫn dùng `can_retail` ⇒ cần đi cùng FE/BE gỡ can_retail như một việc riêng (E1); DB local đã drop ⇒ màn Loại sản phẩm local đang hỏng |
| Migration `add_updated_at_index_to_products_table` | **Đề xuất lấy lại (hỏi user)** | index thuần, không đổi dữ liệu; mặc định sắp `updated_at desc` trên 45.890 dòng cần nó (119 ms → 0 ms) |
| Migration `add_declare_flags_to_product_types_table` + sửa ProductType* | **Để 2-C / việc riêng** | form chỉ xem chỉ dùng cờ để ẩn/hiện tab Phân loại xe / Nhóm máy — nếu muốn bám đúng thì cần cờ này; hỏi user có kéo vào 2-B không |
| `ProductCodeGenerator` + test | **Để 2-C, tái sử dụng nguyên** | test ghi DB thật (không `RefreshDatabase`), dọn theo token |
| `ProductRequest` | **Để 2-C, sửa** | bỏ `rate_liquidation`, rule phân loại theo quyết định cột |

### hrm-client

| File | Đề xuất | Lý do |
|---|---|---|
| `mockup-hang-hoa/index.vue`, `form.vue` | **BỎ** | mockup tĩnh 21/09, đã lỗi thời so với bản chốt HTML 30/09 (§34). Có thể tra cứu cấu hình cột `V2BaseDataTable` + khung `V2BaseSmartFilterPanel` (đều là component thật) khi dựng 4 màn, nhưng bộ cột/lọc phải lấy từ `mockup-luong-xay-dung-hang-hoa.html` |
| `product-types/*` (2 ô tick) | **Để việc riêng** | đi cùng migration cờ + gỡ `can_retail` |
| `utils/product-classification.js`, `subsystem-menu/master-data.js` | **BỎ** | nhánh chung mới hơn; lấy bản cũ là lùi `is_locked` và mất menu Catalog kinh doanh |

---

## 7. Chỗ nhánh cũ xung đột với quyết định hiện hành

| # | Nhánh cũ | Quyết định hiện hành | Hệ quả khi tái sử dụng |
|---|---|---|---|
| 1 | Trạng thái = `products.status` (1 Đang kinh doanh / 0 Đã khoá), list/detail hiện "Đang kinh doanh"/"Đã khoá" | Trạng thái **theo từng công ty** ở `product_company_coefficients.status` (1 Đang nhập thông tin · 2 Chờ tính giá · 3 Đang kinh doanh; NULL = dòng hệ số cũ) — A1, §26 | Viết lại toàn bộ chỗ đọc trạng thái + lọc. ⚠️ 2-A **không backfill** ⇒ hiện tại 0 dòng có `status` → màn *Đang kinh doanh* / *Nhập thông tin* sẽ rỗng cho tới khi backfill (A3) — cần chốt với user |
| 2 | Tab **Giá bán** trong detail (`prices`, `by_type`, `wait_approve`) | Giá tách khỏi form → Phase 8 (§18a, §20) | Bỏ khối giá khỏi detail; gate giá vốn vẫn giữ cho chỗ nào còn hiện |
| 3 | Không có 2 cờ trên Loại sản phẩm ở nhánh chung; nhánh cũ có migration + FE | 2 cờ `declare_vehicle` / `declare_machine_group` đặt ở **Loại sản phẩm** (§18b) | Form chỉ xem cần cờ để quyết hiện tab Phân loại xe / Nhóm máy — nếu không kéo cờ vào thì hiện cả 2 tab (bản cũ hiện tab xe với mọi hàng) |
| 4 | `admin_data` đọc cột chung `products.min_stock_qty/guarantee/...`; tab có `company_coefficients[]` | Dữ liệu quản trị theo công ty trên `ProductCompany` (A4, §23 bỏ tab lồng) | Đọc dòng của công ty hiện tại |
| 5 | Lọc + cột *Công ty quản lý* (`products.company_id`) | Bỏ lọc/cột này (§35 rà mockup, mục 1); công ty hiện tại = `company_role` fallback `company_id` | Bỏ |
| 6 | `rate_liquidation` ở tab Mua hàng | F8: BỎ khỏi HRM, dùng % của Nhóm hàng | Bỏ khỏi detail |
| 7 | `Product` không extends BaseModel (cố ý) | Model mới phải extends `App\Models\BaseModel` | Đổi; lý do cũ (hook created_by) chỉ ảnh hưởng đường ghi; nhớ hook `company_id = info->company_id` cho 2-C |
| 8 | Quyền 1616–1619 *…danh mục hàng hoá* | 1652–1656; 1615–1619 thuộc *Công nợ đầu kỳ* | Không lấy seeder/route cũ |
| 9 | Detail/list gate bằng quyền xem | Kho dữ liệu + Đang kinh doanh + **chi tiết** không cần quyền; chỉ màn công ty gate 1652\|1653 | Middleware mới |
| 10 | `product_type_id` / `product_characteristic_id` trên `products` | 2-A không thêm; sổ chốt §5-1: thêm cột → nhập cây → quy đổi → mới bật lọc | **Tồn phải hỏi** trước khi plan 2-B: có thêm 2 cột ở 2-B không (DB local đã có) |
| 11 | Không có catalog kinh doanh | 4 cấp catalog (`product_business_catalogs`, chỉ Tiểu mục), C5 không bắt buộc ở màn Đang kinh doanh, C5-b dòng nhắc + lọc "Chưa xếp catalog", H3 chỉ nhánh gốc mới | Thêm mới hoàn toàn |
| 12 | Tab Nhóm máy không có trong detail | F1–F5: tab Nhóm máy quay về khuôn ERP (`group_ids_use` + `productables`) | Thêm đọc nếu form chỉ xem có tab này |
| 13 | `can_retail` đã drop ở DB local | Nhánh chung còn đọc/ghi `can_retail` | Môi trường local lệch code — xử lý trước khi nghiệm thu (E1) |

---

## 8. Tồn cần hỏi user trước khi plan 2-B

1. Có thêm 2 cột `products.product_type_id` / `product_characteristic_id` (migration cũ c59fc90) trong 2-B không? Không thêm ⇒ 4 màn không có cột/lọc Loại sản phẩm.
2. Có lấy lại index `products(updated_at, id)` không?
3. Backfill A3 (45.890 hàng → dòng trạng thái cho công ty tạo) chưa làm ⇒ 2-B ra màn rỗng; làm trong 2-B hay đợt riêng?
4. 2 cờ trên Loại sản phẩm (+ gỡ `can_retail`) có kéo vào 2-B để form chỉ xem ẩn/hiện tab đúng không?
5. DB local `hrm_erp` đã chạy 4 migration cũ — rollback hay giữ (ảnh hưởng màn Loại sản phẩm đang ghi `can_retail`)?
