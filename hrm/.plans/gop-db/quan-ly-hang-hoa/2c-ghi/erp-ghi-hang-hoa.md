# ERP ghi hàng hoá thế nào — khảo sát cho đợt 2-C (04/10/2026)

> Khảo sát CHỈ ĐỌC. Mã nguồn ERP: `ERP/TanPhatDev` (đường dẫn dưới đây tính từ thư mục này).
> Số đo: DB local `hrm_erp` (SELECT), ngày 04/10/2026. Bổ sung cho `man-danh-muc-hang-hoa/hop-dong-tuong-thich-erp.md`
> (6 bất biến BB-1…BB-6) và `2a-nen-csdl/khao-sat.md` (K1/K2 về `product_company_coefficients`).
> Chỗ nào tài liệu cũ nói khác, ghi rõ ở mục 8.

---

## 0. Tóm tắt 10 dòng

1. ERP có **6 đường TẠO hàng hoá** (form chính, copy, tạo nhanh từ báo giá dịch vụ, hàng tạm, hàng có sẵn, hàng gốc→sinh biến thể bằng queue) + 5 bộ import Excel. Tất cả đi qua `Product::createRecord()` hoặc bản chép của nó.
2. Mã `code` sinh 2 bước: ghi tạm `randomString(20)` → `save()` → `generateCode()` ghi đè `HÃNG-BARCODE|MODEL` (≤32 ký tự, hậu tố `:01…`). DB có `UNIQUE(code)`; ERP **không** retry khi đua.
3. **Bất biến cứng nhất**: mỗi hàng có **đúng 1 đơn vị cơ bản** (`is_base=1`, hệ số 1), và đơn vị cơ bản **phải có dòng giá `price_type_id=1`**. Thiếu ⇒ hàng **biến mất** khỏi danh sách ERP và **văng 404/500** ở popup chọn hàng (`firstOrFail`). DB đang sạch: 0 hàng hoạt động vi phạm.
4. ERP ghi **6 dòng giá / đơn vị** (1 dòng / `price_types`), giá loại 6 (TMĐT) tự tính = bán lẻ × `configs.coefficient_ecommerce_price` (=1,3).
5. **SỬA** ở ERP: đơn vị/giá cũ **không đụng** (khối sửa giá đã comment tắt); chỉ thêm đơn vị mới (cần quyền `Quản lý giá`). Mọi bảng vệ tinh khác **xoá sạch rồi ghi lại**. Lưu là ép `status = 1` (mở khoá ngầm) và cho đổi `company_id`.
6. **XOÁ = KHOÁ**: cùng một giá trị `status = 0` (+`deleted_at` ở đường xoá đơn; bulk xoá thì không). Không xoá cứng, không đụng bảng con. Khôi phục chỉ `status = 1`, **không** xoá `deleted_at`.
7. Side-effect khi tạo: 1 job queue `CreateTemplateProductMissing` (sinh `product_templates` + gán `products.product_template_id`) — job này là cửa để hàng được **đẩy sang CRM** ở cron `sync:crm` production. CRM hook theo model đang tắt (`MATE_API_USE_CRM` không khai ⇒ `false`).
8. Luồng duyệt giá (`*_wait_approve` + `product_approves`) chỉ bật khi công ty `is_new_company=1` — hiện chỉ **công ty #8 (ETEK)**, 0 phiếu.
9. **Đường ghi NGOÀI màn hàng hoá vẫn chạy sau khi chặn route**: lưu Hãng SX (ghi đè `company_id` + xoá sạch `product_company_coefficients` của mọi hàng của hãng), lưu Thương hiệu (ghi đè `company_id`), Phiếu tính giá, Giá dự kiến theo hãng, 2 cron giá, đổi thuế suất/nhóm, sửa tên TA/HS code từ màn mua hàng, Duyệt giá, Hàng tạm…
10. HRM tạo hàng phải tự gán `created_by` (NOT NULL, FK `employees`) — ERP có `BaseModel` tự gán, HRM thì không.

---

## 1. Bản đồ đường GHI của ERP

### 1.1 Route ghi trên màn hàng hoá (sẽ bị chặn ở 2-D)

| Route (routes/web.php) | Controller@method | Ghi gì |
|---|---|---|
| `POST products/` :573 | `ProductsController@store` :909 | `Product::createRecord()` |
| `GET products/{id}/copy` :578 | `ProductsController@copy` :1084 | chỉ mở form; form post về `productStore` (`resources/views/products/copy.blade.php:119`) ⇒ **copy = tạo mới**, giá các đơn vị bị set `price=1` khi nạp form (:1092-1096) |
| `POST products/storeService` :574 | `@storeService` :743 | tạo nhóm "Hàng hoá làm dịch vụ" nếu chưa có + `createRecord()` (company = công ty người dùng) |
| `POST products/{id}/update` :579 | `@update` :1117 | xem §3 |
| `GET products/{id}/delete` :580 · `POST bulkDelete` :581 | `@delete` :1999 · `@bulkDelete` :4588 | xem §4 |
| `GET products/{id}/restore` :606 | `@restore` :2020 | `status=1` |
| `POST products/{id}/updatePrice` :604 | `@updatePrice` :2552 | "Cập nhật nhanh giá" |
| `POST start-update-products` :630 | `@startUpdateListProducts` :3884 | "Cập nhật nhanh hàng hoá" (có `saveHistory`) |
| `POST importExcel*` :590-593, `view-import/*` :633-637 | import Excel / VAT / mở rộng | `app/ExcelImports/*` (5 lớp `new Product()`) |
| `POST {id}/updateEnglishName` :612 · `{id}/updateHSCode` :613 | gọi từ **màn mua hàng** (buy_requests, inland_buy_contract_new, purchase_invoice, order_notification2…) | `products.english_name`, `products.hs_code` |
| `POST {id}/deleteFile` :621 | xoá file đính kèm kỹ thuật | `files` |
| `approvePrices/*` :595-601 | `ProductApprovesController` | duyệt giá chờ (§5.3) |
| `product2/*` :667-679 | `Product2Controller` + `CreateProductService` | luồng 3 bước cũ (status 3/4). **0 hàng** đang ở status 3/4 |
| `product_templates/*` :507-530 | `ProductTemplatesController` | hàng gốc → sinh N hàng biến thể bằng queue (§2.6) |
| `tmp_products` → duyệt | `Sale/TmpProductsController:566` | `createRecord($request, $tmpProduct->id)` |
| `product-info` :650-661, `sync-product-info` :689-691 | `ProductInfoController:502`, `SyncProductController`, `Services/ProductInfo/SyncProductInfoService:37` | tạo/ghi `products` từ kho "hàng có sẵn" |

### 1.2 Đường ghi NGOÀI màn hàng hoá — vẫn chạy sau khi chặn route hàng hoá

| # | Đường | File:dòng | Ghi vào | Mức nguy |
|---|---|---|---|---|
| E1 | **Lưu Hãng sản xuất** (tạo + sửa) | `Sale/ManufacturesController.php:185-189` (store), `:270-274` (update) | mọi hàng `status=1` của hãng: `products.company_id = manufactures.company_id`; lúc **sửa** còn `syncCompanyCoefficients($request->company_coefficients)` ⇒ **xoá sạch** `product_company_coefficients` của từng hàng rồi ghi lại theo danh sách của hãng | 🔴 xoá dòng trạng thái công ty HRM tạo (K2 ở 2-A đã nêu) + đổi chủ hàng hoá |
| E2 | **Lưu Thương hiệu** (tạo luôn gọi; sửa khi tick `update_products`) | `Sale/BrandsController.php:138, :215` → `Model/Product/Brand.php:153-158` | `UPDATE products SET company_id=? WHERE status=1 AND brand_id=?` (query builder — **không** qua model, không `updated_by`) | 🔴 đổi chủ hàng hoá hàng loạt |
| E3 | **Duyệt Phiếu tính giá** | `Order/PriceCalculateController:160/162/227` → `Model/Order/PriceCalculate.php:332-372` (ghi `products.note`), `:376 updatePriceWithApproval` (ghi `product_units`, `product_unit_prices`, `product_expected_prices`, `product_versions/histories`, `product_approves` nếu duyệt) | 🟡 giá + ghi chú |
| E4 | **Giá dự kiến theo hãng** | `Sale/ManufactureExpectPriceController:116` → `Model/Product/ManufactureExpectPrice.php:71-205` | `product_expected_prices` (xoá + ghi), `product_versions` cho mọi hàng của hãng | 🟡 |
| E5 | Cron `product:update_price` **01:00 hằng ngày** | `Console/Kernel.php:47`, `Console/Commands/UpdateProductPrice.php` | áp `product_expected_prices` (effect_date=hôm nay, status 2, flag≠1) vào `product_unit_prices`, ghi `product_versions/histories`, `price_logs` | 🟡 |
| E6 | Cron `product:reset_price_when_zero_inventory` **14:30** | `Kernel.php:100`, `Commands/ResetProductPriceWhenZeroInventoryCommand.php` | với công ty có cấu hình: hàng có `products.company_id = công ty` **và** `product_cate` chứa loại cấu hình mà tồn kế toán = 0 ⇒ `UPDATE product_unit_prices SET price=0,coefficient=0,sale_max_percent=0` + `product_units.cost_price=0` | 🟡 phụ thuộc `company_id` + `product_cate` |
| E7 | Đổi thuế suất | `Common/TaxRatesController:184-209` → `Jobs/UpdateProductOrGroupTaxValueJob.php:46` | `DB::table('products')->update([vat_percent / import_tax… ])` | 🟢 |
| E8 | Đổi thuế của Nhóm | `Model/Product/Group.php:202` → `Jobs/UpdateProductFromGroupChangeTaxJob.php:49` | `DB::table('products')->update(...)` | 🟢 |
| E9 | Sửa tên TA / HS code từ màn mua hàng | `ProductsController@updateEnglishName :3449`, `@updateHSCode :3505` | `products.english_name`, `products.hs_code` | 🟢 — nhưng route nằm trong nhóm `products/*`, **chặn cả nhóm là vỡ màn mua hàng** |
| E10 | Duyệt / không duyệt giá | `ProductApprovesController:188-498` | `products.status` (1 hoặc 5), `product_units`, `product_unit_prices`, `product_expected_prices`, xoá `product_approves*` | 🟡 |
| E11 | Job tạo hàng gốc | `Jobs/CreateTemplateProductMissing.php:349`, `Jobs/createTemplateProduct.php:300` | `products.product_template_id` | 🟢 |
| E12 | Sửa hàng gốc → cập nhật biến thể | `ProductTemplatesController:1631` → `Jobs/UpdateGenerateProduct` | ghi đè `products` của mọi hàng sinh từ hàng gốc | 🔴 nếu màn hàng gốc không bị chặn cùng |

> Đường E1/E2 là thứ duy nhất "tự đổi `products.company_id`" ngoài form hàng hoá. HRM `ManufacturerService` đã chủ động **không** lặp `products` (comment `ManufacturerService.php:55`), nhưng **màn Hãng/Thương hiệu của ERP vẫn sống** thì vẫn ghi.

---

## 2. TẠO — `Product::createRecord()` (`app/Product.php:6827-7213`)

Gọi trong `DB::beginTransaction()` ở controller. Validate trước đó: `Product::getRules()` (:277-408) + 3 kiểm tra tay ở `ProductsController@store :928-959` (có đúng 1 đơn vị cơ bản; công thức/phụ kiện hợp lệ).

### 2.1 Thứ tự ghi

| Bước | Bảng | Dòng | Giá trị / mặc định |
|---|---|---|---|
| 1 | `products` INSERT | :6828-6891 | `status = 1` (HOAT_DONG), `code = randomString(20)` (tạm), `guarantee_type = request ?: 'thang'`, `tech_coefficient ?? 1`, `promotion/need_environment_tax` = `'true'?1:0`, `environment_tax_coefficient ?: 1`, `product_cate = json_encode(request ?? [])`, `min_stock_qty ?: 0`, `tmp_product_id`, `vat_percent` + `vat_percent_tax_rate_id` (tra `tax_rates`), `import_tax/import_tax_has_co/antidump_duty` = `tax_rates.tax_rate` của id tương ứng. `created_by/updated_by` do `BaseModel::boot` (`app/BaseModel.php:16-41`) gán = `Auth::id()` (hoặc `session current_employee`) |
| 2 | `products` UPDATE `code` | :6893 `generateCode()` (:2207-2248) | xem §2.2 |
| 3 | `product_suppliers` | `suppliers()->sync()` | pivot model `ProductSupplier`; **không ghi `company_id`** ⇒ cột nhận mặc định **1** |
| 4 | `product_videos` | `syncVideos` :832-852 | `position=1, status=1`; chỉ chạy khi `videos != null` |
| 5 | `product_has_accessories` | `syncAccessories` :6272 | xoá theo `base_product_id` rồi ghi; **bắt buộc** hàng phụ kiện có `product_units(product_id, unit_id)` (`firstOrFail`) |
| 6 | `product_has_install_accessories` | :6304 | như trên |
| 7 | `product_has_repair_accessories` | :6322 | xoá + ghi (không unit) |
| 8 | `recipe_products` | `syncRecipeProducts` :6251 | `unit_id = base_unit` của hàng thành phần (`firstOrFail`) |
| 9 | `product_tech_attachments` + `files` (morph `ProductTechAttachment`) | :6334 | xoá + ghi; upload file |
| 10 | `product_company_coefficients` | `syncCompanyCoefficients` :6290 | **chỉ khi `is_array`**: xoá hết dòng của hàng rồi ghi `(company_id, coefficient)` |
| 11 | `productables` | `groupsUse/productsUse/vehicleManufacts/vehicleBrands/vehicleModels()->sync()` (:745-771) | `productable_type` = **tên lớp ERP**: `App\Model\Product\Group` (3.968), `App\Product` (28.398), `App\Model\Common\VehicleManufact` (13.165), `…\VehicleBrand` (12), `…\VehicleModel` (6). Không `withTimestamps` |
| 12 | `product_vehicle_model_has_life` | `syncVehicleModelLife` :7560 | xoá + ghi `(product_id, model_id, life_id)` |
| 13 | `attribute_products` | :6922-6950 | chỉ thuộc tính có `require==='true'`; `INSERT` thô rồi **bắn tay** `eloquent.created` (hook CRM đã comment ⇒ hiện vô tác dụng) |
| 14 | `product_galleries` | :6952-6965 | `name='', status=1, url, created_by` |
| 15 | (tuỳ công ty) `products.status = 2` | :6975-6993 | khi `$is_approve` (§5.3) |
| 16 | `product_units` (mỗi đơn vị) | :7005-7048 | `is_base = ('true')`, `buy_price`, `liquidation_sale_max_percent`, `sale_max_percent_coefficient`; nhánh thường: `cost_price`, `unit_coefficient`; nhánh duyệt: `flag_price_wait_approve=1`, `price_wait_approve`, `coefficient_wait_approve`, `unit_coefficient` (không gán `cost_price` — cột NOT NULL không default; ERP chạy `'strict' => false` (`config/database.php:59`) nên MySQL ngầm ghi 0. ⚠️ HRM chạy strict thì phải ghi tường minh. Nhánh này chưa từng chạy: `product_approves` = 0) |
| 17 | `product_unit_prices` (mỗi loại giá FE gửi) | :7059-7096 | giá loại **6 tự tính**: `price = round(bán_lẻ × coef_ecommerce)`, `coefficient = hệ số bán lẻ × coef_ecommerce`, `sale_max_percent = bán lẻ` |
| 18 | `product_expected_prices` | :7097-7144 | `status = 2`, `effect_date` (> hôm nay), loại 6 tự tính theo bán lẻ; `created_by` do BaseModel |
| 19 | `product_approves` + `product_approve_prices` + `notifications` | :7147-7209 | chỉ khi duyệt giá |
| 20 | `dispatch(new CreateTemplateProductMissing($id))` | :7211 | queue `database` (§5.1) |

**Không ghi khi tạo:** `product_versions`, `product_histories` (lịch sử chỉ sinh khi SỬA), `stocks`/`stock_of_companies` (tồn sinh ở nhập kho), `product_barcodes` (đã comment :6895).

### 2.2 Sinh mã `code`

`generateCode()` `app/Product.php:2207-2248`:

```
prefix = SLUG(manufactures.code) + '-' + SLUG(barcodes.name nếu barcode_id có, ngược lại product_models.name)
prefix = substr(prefix, 0, 32)
while (exists code=? and id<>this) → prefix[0..32-len(':NN')] + ':NN'  (NN = 01, 02…)
SLUG = iconv UTF-8→ASCII//TRANSLIT//IGNORE, bỏ space, chỉ giữ [A-Za-z0-9_-], UPPER
```

- Đảm bảo duy nhất = vòng `while exists` + `UNIQUE products_code_unique`. **Không** khoá/retry ⇒ 2 người lưu cùng lúc cùng prefix có thể nổ `Duplicate entry` (rollback cả giao dịch).
- `manufacture` và `model` bị dùng `->code`/`->name` **không null-safe** ⇒ hàng không có `model_id` mà cũng không `barcode_id` ⇒ lỗi.
- Đo: **7.928** mã có hậu tố `:` (17%).
- Cạm bẫy đã biết: `iconv //TRANSLIT` khác giữa Linux và macOS (`SO-CHOT-VA-TON.md` §6).

### 2.3 Cột `products` NOT NULL không có default (information_schema)

| Cột | ERP lấy từ | Ghi chú cho HRM |
|---|---|---|
| `status` int | gán 1 | |
| `code` varchar UNIQUE | random → generateCode | ghi tạm phải duy nhất |
| `name` | request | ERP validate `UNIQUE(name, model_id, brand_id, manufacture_id)` (`getRules` :279-284; lúc sửa thêm `origin_id`). DB đang có **30** nhóm trùng (dữ liệu cũ) |
| `brand_id` FK `brands` | request (required) | |
| `manufacture_id` FK `manufactures` | request (required) | |
| `origin_id` FK `origins` | request (required) | |
| `created_by` FK **`employees`** | BaseModel | HRM phải tự gán `employees.id` |

Có default: `promotion`(0), `need_environment_tax`(0), `environment_tax_coefficient`(1), `min_stock_qty`(0), `max_stock_qty`(0), `tech_coefficient`(1), `norm`(0). FK khác: `group_id`, `model_id`, `barcode_id`, `company_id`, `tmp_product_id`, `updated_by`. **172 FK** trỏ vào `products`, đều `NO ACTION/RESTRICT` ⇒ không xoá cứng được hàng đã dùng.

`group_id` nullable ở DB nhưng ERP `required` và **mọi** chỗ đọc `->group->name` không null-safe (`sua-erp-de-khong-loi.md`). Đo: 0 hàng `group_id NULL`.

### 2.4 Bất biến đơn vị / giá (ERP kiểm + đo DB)

| Bất biến | ERP kiểm ở | DB ràng buộc? | Đo (45.890 hàng) |
|---|---|---|---|
| ≥1 đơn vị | `units required|min:1` | không | 1 hàng không có đơn vị (#42629, đã xoá) |
| **Đúng 1** `is_base=1` | `store :928-947` | **không** | 0 hàng nhiều đơn vị cơ bản; 1 hàng thiếu (đã xoá) |
| `unit_id` không trùng trong 1 hàng | `distinct` | không | — |
| Đơn vị cơ bản hệ số ≠0 (thực tế =1); đơn vị phụ hệ số ∉ {0,1} | rule động `getRules :389-397` | không | 0 vi phạm |
| Mỗi đơn vị có giá cho từng loại FE gửi | `units.*.prices required|min:1` | không có UNIQUE(product_unit_id, price_type_id) | 0 cặp trùng. Loại 1-4: đủ 46.560/46.560 đơn vị; **loại 5 thiếu 14.349 đơn vị**, loại 6 thiếu 365. Hàng hoạt động thiếu giá loại 5 trên đơn vị cơ bản: **5.436**, loại 6: **364** |
| `price_types` | — | — | 6 loại: 1 Bán lẻ · 2 ĐL1 · 3 ĐL2 · 4 ĐL3 · 5 Theo lô · 6 TMĐT |

### 2.5 Các biến thể tạo khác

| Đường | Khác `createRecord` ở đâu |
|---|---|
| `CreateProductService::create1` (product2) | `status` theo request (3/4), đơn vị chỉ có `unit_coefficient`, **giá giả**: 4 dòng loại 1-4 `price=1, coefficient=0` (`CreateProductService.php:115-160`); `create3` mới ghi giá thật + `status=1`. Không loại 5/6 |
| `GenerateProduct` (hàng gốc → biến thể, queue) | `Jobs/GenerateProduct.php:95-240`: tên = tên gốc + thuộc tính; **không ghi đơn vị/giá** — cất vào `Cache product_units_data_{id}` (1 giờ), `CreateProductUnitsAfterMapping` đọc cache mới tạo `product_units/prices`. Cache hết hạn/worker chết ⇒ **hàng không đơn vị** |
| Import Excel (`app/ExcelImports/*`) | khuôn riêng từng file, không qua `createRecord` |

---

## 3. SỬA — `ProductsController@update` (:1117-1997)

1. Validate (:1118-1328) gần như `getRules`; `canEdit()` (`Product.php:6823`: `!company_id || company_id == công ty người dùng`).
2. `validUnits()` (:885): số `units[].id` gửi lên phải khớp **đủ** số đơn vị hiện có ⇒ không xoá được đơn vị.
3. Tạo `product_versions` (snapshot JSON `getDataForVersion`) rồi lần lượt:

| Bảng | Cách | Lịch sử |
|---|---|---|
| `product_videos` | sync giữ id | `videos` |
| `attribute_products` | **xoá hết + create** | `attributes` |
| `product_suppliers` | `sync` | `suppliers` |
| `product_barcodes` | `sync($request->barcodes)` — form không gửi ⇒ **xoá hết** | `barcodes` |
| `product_galleries` | **xoá hết + insert** | — |
| 3 bảng phụ kiện, `recipe_products`, `product_tech_attachments` | xoá + ghi | có |
| `product_company_coefficients` | xoá + ghi (nếu mảng) | `company_coefficients` |
| `product_units` cũ | **KHÔNG đụng** — khối sửa giá đơn vị cũ đã comment (:1563-1644) | — |
| `product_units` mới (+ giá + giá dự kiến) | chỉ khi `can('Quản lý giá')` (:1547) | `units` |
| `products` | gán lại toàn bộ cột từ request, **`status = 1`** (:1861), **`company_id = request`** (:1870); `saveHistory()` so từng cột (bỏ `id, created_by, updated_by, created_at, updated_at, avatar` — :633) | từng cột |
| `productables`, `product_vehicle_model_has_life` | sync / xoá + ghi | — |
| `product_versions` | xoá nếu không phát sinh dòng lịch sử | — |

- **Không có** chặn sửa khi hàng đã phát sinh giao dịch (chỉ chặn khác công ty).
- Không dispatch job nào khi sửa (khác với tạo).
- `product_histories`: 319.303 dòng, `product_versions`: 113.768 dòng; `action=1, status=1, table_name='products'`, giá trị cũ/mới đã **dịch sang tên** (brand/manufacture/group… — `createHistoryRecord` :2130-2205, `findOrFail` ⇒ id rác là văng). HRM đã chốt **bỏ version/lịch sử kiểu ERP** (§11, §14b) ⇒ hàng sửa từ HRM sẽ **không có dòng mới** ở màn "Lịch sử" ERP.

---

## 4. XOÁ / KHOÁ / KHÔI PHỤC

| Thao tác | File:dòng | Ghi |
|---|---|---|
| Xoá 1 hàng | `ProductsController@delete :1999` (và `Product2Controller@delete :1512`) | `status=0`, `deleted_at=now()`, `save()` |
| Xoá nhiều | `@bulkDelete :4588` | `status=0` — **không** gán `deleted_at` |
| Khôi phục | `@restore :2020` | `status=1` — **không** xoá `deleted_at` |
| Khoá | **không có thao tác riêng** — `STATUSES` đặt tên `KHOA = 0` (`Product.php:124-161`), trùng giá trị với "đã xoá" |
| Sửa hàng | `status = 1` vô điều kiện | sửa 1 hàng đã khoá ⇒ **tự mở khoá** |

`canDelete()` (`Product.php:7215-7255`) — kiểm **đúng 5 điều kiện**:

1. `Auth::user()->info->company_id == products.company_id` (khác công ty ⇒ cấm).
2. `stocks.accounting_qty > 0` ⇒ "Hàng có tồn kho!".
3. `product_export_request_details` ⨝ `product_export_requests.type = 3` có `base_exported_qty > borrow_returned_qty` ⇒ "đang mượn chưa trả".
4. `product_has_accessories.product_id = id` (đang là phụ kiện của hàng khác).
5. `recipe_products.product_id = id` (đang là thành phần ghép bộ).

Không kiểm: phụ kiện lắp đặt/sửa chữa, đơn hàng/báo giá/hợp đồng đang mở, giữ hàng (prepick). Không đụng bảng con nào.

Đo: `status=0` 17.512 · `deleted_at NOT NULL` 16.206 · `status=0 AND deleted_at NULL` **1.482** (bulk xoá) · `status=1 AND deleted_at NOT NULL` **175** (đã khôi phục). ⇒ ERP **chỉ dựa vào `status`**; `deleted_at` không phải tín hiệu tin cậy.

Ai đọc `status` thế nào:
- Danh sách ERP (`Product::searchByFilter` :1754-1762): mặc định `status IN (1,2,5)`; tab "Đã xoá" `status=0`; `?type=approver` → 4; `creating` → 3.
- Popup chọn hàng `SearchController@searchProduct` :395 (và :855, :1271, :1683): `status != 0` (trừ `type=include_deleted`) ⇒ status 2/3/4/5 **vẫn chọn được**.
- `CreateTemplateProductMissing`: chỉ chạy khi `status = 1`.

---

## 5. Side effect

### 5.1 Queue / job

- `QUEUE_CONNECTION=database` (ERP `.env:23`). Tạo hàng ⇒ `CreateTemplateProductMissing` (`Jobs/CreateTemplateProductMissing.php`): clone hàng sang `product_templates` + bảng `product_template_*` (đơn vị, pivot, phụ kiện, ảnh, thuộc tính, file) rồi `UPDATE products SET product_template_id`. Đo: 16.077 hàng `product_template_id NULL` (job hay hỏng: 31 dòng `failed_jobs` của job này; 65.305 `failed_jobs` tổng, phần lớn job CRM).
- `products.product_template_id` chỉ được đọc ở màn CRM (`Warehouse/WarehouseInfosController:1026`, `CRM/...:49`) và hook CRM (`ProductUnit.php:70`, `ProductUnitPrice.php:114`).
- Production (`APP_ENV=TANPHATERP`) có cron **`sync:crm` 19:30** (`Kernel.php:130` → `database/seeds/SyncDataToCrmSeeder.php`) đẩy sang CRM Mate các `product_templates` / `products` **có `product_template_id`** / `product_units` / `product_unit_prices` chưa có trong `module_mappings` (229.358 dòng). ⇒ Hàng HRM tạo **không có `product_template_id` thì không bao giờ sang CRM**.

### 5.2 CRM theo model

`Product::boot` (:165-230), `ProductUnit::boot`, `ProductUnitPrice::boot`, `ProductTemplate::boot` chỉ đăng ký hook khi `config('services.mate.use_crm')` (`config/services.php:38`, `env('MATE_API_USE_CRM', false)`). ERP `.env` **không khai** ⇒ `false` ⇒ tắt. (`bootstrap/cache/config.php` không tồn tại ở máy này.) `AttributeProduct` hook đã comment.

### 5.3 Duyệt giá

`$is_approve = companies.is_new_company AND (is_new_brand OR manufacture_id ∈ new_brand_ids)` (`Product.php:6976-6989`, `ProductsController:1374-1388`). Đo: chỉ công ty **#8 ETEK** (`is_new_company=1, is_new_brand=1`) bật; 0 hàng thuộc công ty 8; `product_approves`=0; `product_units.flag_price_wait_approve=1`: 6 dòng; `product_unit_prices.flag_…=1`: 5 dòng. Khi bật: `status=2`, giá vào cột `*_wait_approve`, sinh `product_approves(+_prices)` và **thông báo** (`NotificationHelper::sendNotify`) cho người có quyền `Duyệt giá hàng hoá` của công ty.

### 5.4 Khác

- Email: không có khi tạo/sửa/xoá (`ProductSettingMailJob` là job **xuất Excel** hàng gốc, `ProductTemplatesController:3199`).
- Thông báo: chỉ nhánh duyệt giá; `Product2Controller@store1` báo quyền "Nhập thông tin quản lý bán/mua hàng".
- Cache: chỉ luồng hàng gốc (`product_units_data_{id}`, `product_creation_data_{id}`). Không cache danh sách hàng.

---

## 6. Thiếu dòng con thì ERP vỡ ở đâu

| Thiếu | Chỗ vỡ | Kiểu vỡ | Đo hiện tại |
|---|---|---|---|
| `product_units` hoặc đơn vị cơ bản | `Product::searchByFilter` :1750 (`WHERE pu.is_base=1 AND pp.price_type_id=1` trên LEFT JOIN = INNER) | hàng **biến mất** khỏi Danh mục hàng hoá ERP | 0 hàng hoạt động |
| | `getBaseUnitAttribute` :1388, `getBasePriceAttribute` :1397 (`firstOrFail`) — dùng trong `getDataAttribute` :1208 ⇒ route `product.getData` mà **popup chọn hàng của mọi phiếu gọi sau khi chọn** | **404 ModelNotFound** ⇒ chọn hàng không được | 77 chỗ `->base_unit`, 36 chỗ `->base_price` |
| | `recipe_products` / phụ kiện của hàng khác trỏ vào nó | `syncRecipeProducts`/`syncAccessories` `firstOrFail` ⇒ lưu hàng cha lỗi | |
| Dòng giá `price_type_id = X` trên đơn vị | `SearchController@searchProduct :398-416` khi FE gửi `price_type` | hàng **biến mất khỏi popup** của phiếu dùng loại giá đó | loại 5 thiếu ở **5.436** hàng hoạt động (đã như vậy từ trước) |
| | `Product::getPriceByUnitAndType` :1407 (`firstOrFail`) — **91** chỗ gọi (vd `Contract.php:2546, 2566`) | 404/500 khi lập chứng từ | |
| Dòng `product_units(product_id, unit_id)` cho đơn vị được chọn | `Product::getUnitCoefficient` :6521 (`firstOrFail`) — **88** chỗ (kho, chứng từ) | 404 khi nhập/xuất với đơn vị đó | |
| `model_id` / `brand_id` / `group_id` | `getDataAttribute`: `$this->model->name`, `brand->name`, `group->name`, `group->rate_liquidation` | 500 "property of non-object" | 0 hàng hoạt động thiếu |
| `product_type` NULL hoặc ngoài `PRODUCT_TYPES` | `SearchController :545/968/1386/1787` `product_type != 'service_product'` ⇒ NULL bị loại; `getDataAttribute` `BaseProduct::PRODUCT_TYPES[$this->product_type]` ⇒ khoá lạ ⇒ ErrorException | biến mất khỏi popup / 500 | 0 NULL; 15 giá trị đang dùng (đều có trong enum) |
| `product_cate` NULL/`[]` | `getProductCateName` an toàn; cron E6 bỏ qua hàng (không reset giá) | đổi hành vi im lặng | 98 hàng hoạt động |
| `product_company_coefficients` | **không bắt buộc** — 1.105 dòng / 45.890 hàng. Có dòng ⇒ popup lấy `ROUND(price × coef / 1000) × 1000` (`SearchController:415, 894, 1310, 1703`) — kể cả `coef = 1` ⇒ **giá bị làm tròn nghìn** (đã nêu ở 2-A K2) | đổi giá hiển thị | 7.282 hàng hoạt động có giá bán lẻ cơ bản lẻ nghìn |
| `attribute_products` | không bắt buộc | — | 17.792 hàng hoạt động không có thuộc tính |
| `product_templates` / `product_template_id` | không màn ERP lõi nào cần | chỉ mất đồng bộ CRM | 16.077 NULL |
| `stocks` | không cần lúc tạo | — | |

---

## 7. Bắt buộc HRM phải làm khi ghi

**Tạo / Copy / Lấy hàng về**

1. Ghi `products` đủ 7 cột NOT NULL: `status`, `code` (duy nhất), `name`, `brand_id`, `manufacture_id`, `origin_id`, **`created_by` = `employees.id`** (+ `updated_by`). Không để `model_id`, `group_id`, `product_type` trống chừng nào 2-D chưa sửa null-safe ERP (BB-6).
2. Sinh `code` theo đúng `generateCode()` (ghi tạm giá trị duy nhất → sinh mã → ghi), **bắt `Duplicate entry` 23000 và thử lại**; khuyến nghị chạy slug trên cùng 1 nền (Linux) để không lệch `iconv`.
3. Đơn vị: **≥1 dòng, đúng 1 `is_base=1` với `unit_coefficient=1`**, đơn vị phụ hệ số ∉ {0,1}, `unit_id` không trùng. Chặn ở BE (DB không có ràng buộc). `cost_price` NOT NULL ⇒ ghi 0 nếu chưa có giá.
4. Giá: mỗi `product_units` có **1 dòng / mỗi `price_types` (6 dòng)**, không trùng `(product_unit_id, price_type_id)`; tối thiểu đơn vị cơ bản có loại 1. Nếu giá để Phase 8: ghi dòng giá 0 (như `CreateProductService` ghi `price=1`) — **đừng bỏ trống bảng**. Loại 6 = bán lẻ × `configs.coefficient_ecommerce_price` khi có giá.
5. `product_expected_prices` (nếu có): `status=2`, `effect_date > hôm nay`, `created_by` NOT NULL.
6. `productables`: dùng **đúng chuỗi lớp ERP** ở `productable_type` (`App\Model\Product\Group`, `App\Product`, `App\Model\Common\VehicleManufact|VehicleBrand|VehicleModel`) — không dùng morph map/namespace HRM.
7. `attribute_products.created_by`, `product_galleries.status=1/created_by`, `product_videos.position/status/created_by` (NOT NULL).
8. `product_company_coefficients`: chỉ ghi khi cần (K2: `coefficient=1`); biết trước hệ quả làm tròn nghìn ở popup ERP của công ty đó.
9. `product_suppliers.company_id`: ghi tường minh (ERP để default 1).
10. Bọc toàn bộ trong 1 transaction.

**Sửa**

11. Không xoá/sửa `product_units` đã có (ERP không cho; chứng từ cũ tham chiếu `unit_id`); chỉ thêm. Sửa giá phải theo BB-1/BB-2 (nhánh duyệt + quyền `Quản lý giá`).
12. Không tự ép `status=1` khi lưu (khác ERP) — nếu cố ý giữ hành vi ERP thì phải ghi rõ.
13. Bảng con kiểu "xoá + ghi lại": giữ nguyên ngữ nghĩa nhưng **không xoá dòng `product_company_coefficients` của công ty khác** (cột `status` 2-A).

**Xoá / Khoá**

14. Port `canDelete()` đủ 5 điều kiện (§4). Xoá = `status=0` + `deleted_at=now()` + `updated_by`; không xoá cứng, không đụng bảng con.
15. Nếu HRM có "Khoá" khác "Xoá": ERP **không phân biệt** (cả hai `status=0`). Phải chốt (câu R1).

---

## 8. Đính chính tài liệu cũ

- `hop-dong-tuong-thich-erp.md` BB-5 viết "`Product` của ERP **không** `extends BaseModel`". Sai: `Product extends BaseProduct extends BaseModel` (`app/BaseProduct.php:7`) ⇒ ERP **tự gán** `created_by/updated_by` qua `BaseModel::boot`. Kết luận cho HRM không đổi (HRM vẫn phải tự gán), nhưng `Brand::updateProducts` (E2) và 2 job thuế (E7/E8) đi bằng query builder ⇒ **không** cập nhật `updated_by`.
- BB-1 ghi đường sửa giá trực tiếp đã comment ở "dòng 1565–1635" — đúng nội dung, số dòng hiện tại là **1563–1644**; cờ `Quản lý giá` ở **:1547**.

---

## 9. Rủi ro / câu cần user chốt

| # | Câu | Vì sao phải chốt |
|---|---|---|
| R1 | **"Khoá" của HRM ghi vào đâu?** ERP chỉ có `status=0` = vừa khoá vừa xoá (popup loại, tab "Đã xoá" hiện). Phương án: (a) khoá = `status 0` không `deleted_at`, xoá = `status 0` + `deleted_at` (ERP thấy như nhau); (b) khoá dùng trạng thái ở `product_company_coefficients.status` theo công ty, `products.status` giữ 1 | quyết định cả ERP có còn bán được hàng "bị khoá ở 1 công ty" hay không |
| R2 | **Chặn luôn màn Hãng SX + Thương hiệu ERP** (E1, E2) cùng đợt 2-D? Nếu không: mỗi lần lưu Hãng là **xoá sạch** dòng `product_company_coefficients` (mất trạng thái theo công ty của HRM) + đổi `products.company_id` của mọi hàng của hãng | 🔴 mất dữ liệu im lặng |
| R3 | Chặn nhóm route `products/*` thì **phải chừa** `updateEnglishName`, `updateHSCode`, `getData*`, `getPriceOfProducts`, `searchProductsByKeyword`… (màn mua hàng / popup dùng). Cần danh sách trắng thay vì chặn cả prefix | chặn nhầm là vỡ màn mua hàng |
| R4 | Màn **hàng gốc** (`product_templates`, E12), **hàng tạm**, **hàng có sẵn/đồng bộ**, **Product2**, **import Excel** của ERP: chặn cùng lúc? Chúng là đường TẠO/SỬA hàng hoá song song | không chặn = ERP vẫn sinh hàng ngoài HRM |
| R5 | HRM có tạo `product_templates` + `product_template_id` như job `CreateTemplateProductMissing` không? Không tạo ⇒ hàng mới **không sang CRM Mate** qua cron `sync:crm` production (QĐ §9 nói "bỏ đồng bộ CRM" — xác nhận áp cả việc này) | |
| R6 | **Production có bật `MATE_API_USE_CRM`?** Local tắt. Nếu prod bật thì ERP đang đẩy `status`/đơn vị/giá sang CRM mỗi lần sửa; HRM ghi thẳng DB **không chạy hook ERP** ⇒ CRM lệch dần | cần kiểm `.env` production |
| R7 | Giá khi tạo từ HRM (giá tách Phase 8): ghi 6 dòng giá **0** hay **1** (khuôn `CreateProductService`)? Ghi 0 ⇒ báo giá ERP ra giá 0 nếu người dùng chọn được hàng trước khi có giá. Có cần ẩn hàng chưa có giá khỏi popup ERP (vd dùng `status` ≠ 1)? | |
| R8 | Hàng HRM tạo có trạng thái theo công ty "Đang nhập thông tin" — ERP popup lọc `status != 0` ⇒ hàng đang nhập dở **đã chọn được ở 338 màn ERP** ngay khi tạo. Chấp nhận, hay ghi `products.status = 3` (DANG_NHAP_THONG_TIN_CHUNG — popup vẫn hiện vì ≠0) / cần sửa popup ở 2-D? | |
| R9 | Công ty #8 bật duyệt giá: hàng HRM tạo cho công ty 8 có phải đi `product_approves` như ERP (BB-1)? | |
| R10 | Cron E6 reset giá về 0 theo `products.company_id` + `product_cate`. HRM đóng băng `product_cate` (§3) và chuyển chủ sang `product_company_coefficients` ⇒ cron sẽ **bỏ sót** hàng mới. Có cần cron này tiếp tục chạy đúng? | đổi hành vi im lặng |
| R11 | "Lấy hàng về" ở ERP không có tương đương; với ERP, hàng luôn dùng chung mọi công ty (popup không lọc `company_id`). Xác nhận HRM chỉ thêm dòng `product_company_coefficients` (coef 1) và chấp nhận làm tròn nghìn ở popup ERP của công ty lấy về (7.282 hàng có giá lẻ nghìn) | đã nêu K2, nhắc lại vì 2-C là nơi phát sinh dòng |
| R12 | Copy hàng: ERP copy = tạo mới, giá bị reset `1`; HRM copy có mang theo giá/đơn vị/phụ kiện/thuộc tính không? | |
