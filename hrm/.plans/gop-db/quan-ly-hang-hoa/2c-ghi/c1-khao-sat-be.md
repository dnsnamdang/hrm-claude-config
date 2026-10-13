# Đợt 2-C1 — Tạo + sửa hàng hoá do công ty tạo: khảo sát BE (07/10/2026)

> CHỈ ĐỌC: không sửa source, không ghi DB. Code HRM = worktree `websites/wt-chuyen-doi-hang-hoa/hrm-api`
> nhánh `feat/chuyen-doi-hang-hoa` (api `626113419`); đường dẫn dưới đây tính từ `hrm-api/`. ERP = `ERP/TanPhatDev`
> (nhánh `develop_01`, đối chiếu `origin/gop_db` khi khác). Số đo: DB local `hrm_erp` (SELECT), 07/10/2026.
> Luật ưu tiên: `chot.md` (G1–G11, T6, H1', H1'') > `yeu-cau-ghi.md` / `erp-ghi-hang-hoa.md` (04/10).

---

## 0. Tóm tắt

| # | Kết luận |
|---|---|
| 1 | Nền đọc của 2-B đủ dùng lại (entity, quan hệ, `show`, form-options). Còn **thiếu 2 entity**: `ProductUnitPrice` (quan hệ `ProductUnit::prices()` đang trỏ tới class KHÔNG tồn tại — `Entities/Product/ProductUnit.php:56-59`) và bảng `product_vehicle_model_has_life` (chưa có model) |
| 2 | `BaseModel::boot` (`app/Models/BaseModel.php:104-157`) tự gán `created_by/updated_by = Auth::user()->id` = **`employees.id`** (auth model `TpEmployee`, `$table='employees'` — `config/auth.php:70`, `app/Models/TpEmployee.php:15`) ⇒ FK `products.created_by→employees` OK. Nhưng `company_id` tự gán = `info->company_id` (KHÔNG phải `company_role`) ⇒ **gán tay** ở `products`, `product_company_coefficients`, `product_suppliers`, `product_business_catalogs` |
| 3 | `ProductCodeGenerator` + test 9 ca: **lấy nguyên** (đổi test sang `DatabaseTransactions` + `ActsAsProductUser` theo khuôn nhánh chung). `ProductRequest` cũ: lấy khung, sửa ~14 điểm (mục 2.2) |
| 4 | Ghi tối thiểu khi TẠO: `products` (7 cột NOT NULL) → mã → `product_units` (`cost_price=0` tường minh) → **6 dòng `product_unit_prices` giá 0/hệ số 0 mỗi ĐVT** (G2) → dòng `product_company_coefficients` (coef 1, status 1) → bảng con. Tất cả trong 1 transaction |
| 5 | Tệp: ERP lưu **URL S3 tuyệt đối** (bucket `tanphat`, endpoint CMC). Ảnh ở `erp_products/` + 2 bản `-thumbnail`/`-large` (ERP dựng URL thumbnail từ avatar — `app/Product.php:891-897`). Tài liệu kỹ thuật ở bảng **`files` khuôn HRM** (`table='product_tech_attachments'`, `table_id`). HRM đã có `CmcS3Helper::putFileProduct` cùng bucket ⇒ ERP đọc được |
| 6 | **Bẫy mới**: (a) `product_types` = **0 dòng** trên local + cột `can_retail` đã bị drop nhưng code nhánh chung vẫn ghi ⇒ không tạo được Loại SP qua màn ⇒ test/e2e phải tự chèn fixture; (b) 45.890/45.890 hàng cũ `product_type_id = NULL`; (c) `products.product_type` (chuỗi) NULL ⇒ hàng HRM tạo **biến mất khỏi popup 338 màn ERP** — trái kỳ vọng G1, chưa có trong N1–N8; (d) chủ sửa hàng CŨ cũng chạm luật G4 ngay ở 2-C1 |

---

## 1. Hiện trạng BE trên nhánh chung

### 1.1 Entity (`Modules/MasterData/Entities/Product/`)

| Entity | Bảng | Ghi chú cho đường ghi |
|---|---|---|
| `Product.php` | `products` | `extends BaseModel`; `boot()` :74-88 **ném lỗi nếu `code` dirty khi updating**; `$fillable` :90-165 còn `code`, `status`, `company_id`, `rate_liquidation` (:158), `created_by` ⇒ **cấm `fill($request->all())`**, gán từng cột; `casts` promotion/need_environment_tax boolean :167-170; KHÔNG `SoftDeletes` (docblock :27-32). Quan hệ: `productType` :177, `characteristic` :183, `brand/manufacturer/origin/productModel/orderCode` :192-217, `units` :224, `productAttributes` :230, `suppliers` :236, `techAttachments` :242, `galleries` :247, `videos` :252, `companies` :258, `businessCatalogs` :264, 4 bảng kèm theo (khoá `base_product_id`) :275-296, `vehicle*Links` :306-324, `machineGroupLinks/machineLinks` :331-341. `scopeWithCompanyStatus` :360-372 (luật suy ra @TODO-BACKFILL) |
| `ProductCompany.php` | `product_company_coefficients` | hằng status 1–4 :23-26, `NEUTRAL_COEFFICIENT=1` :44, fillable :48-59 (có 4 cột quản trị, KHÔNG có `tech_coefficient` — đúng T6), `$attributes coefficient=1` :61-63 |
| `ProductUnit.php` | `product_units` | fillable :21-39 đủ; `prices()` :56-59 → `ProductUnitPrice::class` **không tồn tại** (gọi là fatal) |
| `ProductSupplier.php` | `product_suppliers` | fillable `product_id, supplier_id, company_id` :21-25; `supplier_id` → `customers` |
| `ProductBusinessCatalog.php` | `product_business_catalogs` | fillable :17-23 |
| `AttributeProduct.php` | `attribute_products` | fillable :22-30 |
| `Productable.php` | `productables` | `extends Model` (không BaseModel, có timestamps); hằng 5 loại :34-45; KHÔNG `morphedByMany` |
| `ProductGallery.php` / `ProductVideo.php` | `product_galleries` / `product_videos` | fillable có `status`, `position` |
| `ProductTechAttachment.php` | `product_tech_attachments` | chỉ `product_id, attachment_type_id`; file nằm ở bảng `files` (mục 5) |
| `RecipeProduct`, `ProductHasAccessory`, `ProductHasInstallAccessory`, `ProductHasRepairAccessory` | 4 bảng kèm theo | repair KHÔNG có `unit_id/qty` |
| *(thiếu)* | `product_unit_prices`, `product_vehicle_model_has_life` | phải tạo entity |

### 1.2 Route khối products (`Modules/MasterData/Routes/api.php:253-279`)

| Route | Gate | Dùng cho 2-C1 |
|---|---|---|
| `GET /form-options` :259 | không | đổ 14 danh mục (loại SP kèm path 3 cấp cha, brands, manufacturers, origins, units+`can_be_base`, attribute_units, business_policies, tax_rates, companies, model/order_code/supplier chỉ theo `include_ids`) — `ProductOptionService::formOptions` :65-91 |
| `GET /catalog-options` :260 | không | cây catalog 4 cấp (`catalogOptions` :283) |
| `GET /vehicle-options` :261 | không | hãng/loại/model xe — **thiếu Đời xe (`vehicle_life`)** (`vehicleOptions` :242-250) |
| `GET /option-search` :262 | không | tìm `product_models`/`order_codes`/`suppliers` (`search` :98-121) |
| `GET /entering` :268 | 1652 | màn Nhập thông tin |
| `GET /company` :267 | 1652\|1653 | |
| `/catalogs/*` :271-275 | 1655 | 2-C3 |
| `GET /{product}` :277 | không | chi tiết |

Chưa có: POST/PUT ghi, attributes-by-type, nhóm máy (bảng `groups`), tìm hàng hoá cho bảng kèm theo/máy, upload ảnh.

### 1.3 Đọc chi tiết (đường sửa phải đọc lại khớp)

`ProductService::show` (`Services/Product/ProductService.php:116-167`) + `Transformers/Product/ProductDetailResource.php`:
- Trả đủ lớp chung: định danh, phân loại + `classification_path` (:48-55), ĐVT **chỉ cấu trúc** `id, unit_id, is_base, unit_coefficient` (:82-90), galleries/videos qua `ErpAsset::url` (:92-98), attributes (:101-111), `product_attributes` (= *Đặc điểm* rich text — ERP `form.blade.php:875-880`), `special_feature`, `standard_accessories`, tech_attachments (**chỉ loại, không có tệp** :117-123), 4 bảng kèm theo (:125-136), thuế (:139-151), suppliers của công ty hiện tại (:153-160), `admin_data` (:163-172), xe chỉ 3 mảng id (:177-179), nhóm máy/máy dạng tên (:182-183).
- **Thiếu cho form sửa**: `guarantee` + `guarantee_type` tách rời (hiện chỉ `guarantee_text`), Đời xe theo model (`product_vehicle_model_has_life`), danh sách tệp của từng tài liệu kỹ thuật, `machine_group_ids`/`machine_ids` dạng id (đang là tên), cờ Tính chất "Phụ tùng ô tô" (G11), cờ quyền sửa (`can_edit_common` = chủ; `can_edit_admin`; ẩn khi status 4). `owner_company_id` đã có (:40) ⇒ FE tự suy được "công ty tạo".
- `AdminData` (`Transformers/Product/AdminData.php:17-40`) lùi về cột chung khi chưa có dòng — đúng cho hàng cũ; sau G5 chỉ đọc, không ghi kép.

### 1.4 Helper công ty + quyền

- `auth()->user()->current_company_role` (`app/Models/TpEmployee.php:97-117`, đệm theo request); `ProductService::currentCompanyId()` :56-59 dùng lại.
- Quyền 1652 `Xây dựng thông tin hàng hoá` seed ở `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1582`, có trong DB local (cùng 1653, 1655). Gate route bằng `checkPermission:Xây dựng thông tin hàng hoá` như `/entering`.
- Kiểm "đúng công ty" (chủ = `products.company_id == current_company_role`) **chưa có ở đâu** — viết trong Service, trả 403.

### 1.5 Tái dùng từ 2-C3

`ProductCatalogService::checkClustersOpen` (`Services/Product/ProductCatalogService.php:158-186`, **private**) kiểm Tiểu mục thuộc cây mới + 4 cấp đang mở (B2) — tab Quản trị của form cần đúng luật này ⇒ tách ra public/trait. Lưu ý đường SỬA: nhánh đã lưu trước đó nay bị khoá thì **giữ**, chỉ kiểm nhánh THÊM mới (chưa chốt chữ, đề xuất theo B2).

---

## 2. Nhánh cũ `feat/p1-danh-muc-hang-hoa`

### 2.1 `ProductCodeGenerator` + test

| File | Kết luận |
|---|---|
| `Modules/MasterData/Services/Product/ProductCodeGenerator.php` (184 dòng) | **Lấy nguyên**. `generate(manufactureId, barcodeId, modelId, ignoreId)` :54-75 trả chuỗi (không save), khuôn `<mã hãng>-<tên code đặt hàng ?: tên model>` :78-99, cắt 32, hậu tố `:01–:99` :62-70, bảng bỏ dấu cố định :156-183 (né bẫy iconv), ném `RuntimeException` khi thiếu nguồn :87-91. Khớp ERP `generateCode()` `app/Product.php:2207-2248` |
| Bổ sung ở Service (không sửa generator) | bắt `QueryException` 23000 trên `products_code_unique` ⇒ sinh lại (2–3 lần); bắt `RuntimeException` ⇒ 422. ERP ghi `randomString(20)` rồi sinh mã (:6836, :6897) — HRM sinh TRƯỚC khi insert là đủ, không cần mã tạm |
| `Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php` (9 ca) | Lấy nguyên nội dung 9 ca; **đổi khung**: bản cũ ghi thật + dọn ở `tearDown` theo token `PCGT` (:30-51) — nhánh chung dùng `DatabaseTransactions` + `Concerns\ActsAsProductUser` (`ProductCatalogApiTest.php:15-19`). 2 ca khoá mã (:177, :194) dựa `Product::boot()` — đã có |

### 2.2 `ProductRequest.php` cũ (220 dòng) → tách 2 request

Cập nhật bảng `yeu-cau-ghi.md` §3 theo chốt G1–G11:

| Rule cũ (dòng) | Việc ở 2-C1 |
|---|---|
| `name` unique (model×brand×manufacture) :68-76 | Giữ khuôn ERP **store** (`app/Product.php:279-284`) cho cả tạo + sửa, `ignore($id)`. ⚠️ 30 nhóm trùng sẵn ⇒ xem Q6 |
| `product_type_id` required :81 | Giữ (Loại SP `*`) — xem Q4 cho hàng cũ |
| `model_id` `required_without:barcode_id` :90 | Đổi **`required`** (ERP `getRules` + mockup `*`) |
| `company_id` required :95 | **Bỏ** — server gán `current_company_role` |
| `business_policy_id`, `guarantee` :96-98, `min_stock_qty` :110 | **Chuyển sang request tab Quản trị** (ghi dòng công ty), thêm `guarantee_type in:ngay,thang,nam`. G5: KHÔNG ghi `products.guarantee/min_stock_qty` |
| `tech_coefficient` `min:1` :100 | Giữ ở **lớp chung** (T6, chỉ chủ sửa) nhưng 11.156 hàng = 0 ⇒ xem Q2 |
| `avatar` required :102 (docblock :20-21 lại nói "không bắt buộc" — tự mâu thuẫn) | Xem Q1 |
| `import_tax`/`import_tax_has_co`/`antidump_duty` nhận số % :106-108 | **Thay** bằng `vat_percent_tax_rate_id` **required**, 3 `*_tax_rate_id` nullable `exists:tax_rates,id`; BE suy % từ `tax_rates.tax_rate` (ERP `:6866-6882`, `ProductsController:1883-1896`) |
| (thiếu) BVMT | Thêm `environment_tax_coefficient nullable|numeric|min:1|max:999.999`; BE tự suy `need_environment_tax` (F7); trống ⇒ cờ 0 + hệ số 1.00 (cột NOT NULL DEFAULT 1.00) |
| `units.*` :130-133 + `withValidator` đúng 1 cơ bản :197-219 | Giữ; thêm luật ERP: cơ bản hệ số = 1, phụ `not_in:0,1` (`app/Product.php:389-397`); `unit_id` có `can_be_base` cho đơn vị cơ bản (cột có thật) — chưa kiểm ERP có xét cờ này không |
| `attributes.*` :141-145 | Giữ; ⚠️ ý nghĩa ERP của ô **"Bắt buộc"** = chỉ dòng tick mới được LƯU + bắt value/đơn vị (`createRecord :6923-6950`, `update :1438-1454`), không lưu cờ nào. `value` NOT NULL |
| `suppliers.*` :147-148 | Chuyển sang request tab Quản trị (theo công ty) |
| `videos.*` :150-152, `galleries`, `tech_attachments` :153-154 | Giữ; `galleries max:10`; tech: `*.attachment_type_id` + `*.files[]` |
| 4 bảng kèm theo :156-174 | Giữ; ⚠️ `repair_accessories.*.unit_id/qty` :172-174 **sai** — bảng không có 2 cột ⇒ bỏ. Thêm: không chứa chính nó (ERP `validateRecipe/validateAccessory` `ProductsController:3619-3635`); phụ kiện/lắp đặt phải có `product_units(product_id,unit_id)` (ERP `firstOrFail` :6279-6281) |
| `company_coefficients.*` :176-178 | **Bỏ** (K0) |
| `vehicle_*_ids` :181-186 | Giữ, không `required` (G11); thêm `vehicle_models.*.id` + `vehicle_life_ids[]` (khuôn ERP `syncVehicleModelLife :7560`) |
| (thiếu) Nhóm máy | Thêm `group_ids_use[]` (exists `groups`) + `product_ids_use[]` (exists `products`) |
| (thiếu) catalog | `job_cluster_ids required|array|min:1|distinct` ở request tab Quản trị (C5-a — xem Q5) |
| Lưu nháp | **Bỏ** (G3) — 1 bộ rule; báo lỗi đồng thời (FormRequest đã gom) |
| `rate_liquidation` | Không rule, không ghi (F8) |

---

## 3. Schema thật `hrm_erp` (information_schema, 07/10)

"NN" = NOT NULL không default (bỏ PK).

| Bảng (dòng) | NN | UNIQUE | `company_id` | Default đáng nhớ |
|---|---|---|---|---|
| `products` (45.890) | `status` int, `code`, `name`, `brand_id`, `manufacture_id`, `origin_id`, `created_by` | `products_code_unique(code)` | có, nullable, FK companies | `norm 0`, `promotion 0`, `min_stock_qty 0`, `max_stock_qty 0`, `need_environment_tax 0`, `environment_tax_coefficient 1.00`, `tech_coefficient 1.00`. FK: barcode/brand/company/created_by→employees/group/manufacture/model/origin/tmp_product/updated_by |
| `product_units` (46.560) | `unit_id`, `product_id`, `is_base`, `unit_coefficient` dec(12,2), **`cost_price`** dec(16,2) | — | — | `sale_max_percent_coefficient 1.00`, `liquidation_sale_max_percent 0`, `according_base_price 0`; `buy_price` nullable |
| `product_unit_prices` (264.646) | `price_type_id`, `product_unit_id`, `price` dec(16,2), `coefficient` dec(5,2) | **không** có UNIQUE(unit,type) | — | `sale_max_percent` nullable; 3 cờ `is_manual_*` = 0 |
| `price_types` (6) | — | — | — | **1 Bán lẻ · 2 Đại lý cấp 1 · 3 Đại lý cấp 2 · 4 Đại lý cấp 3 · 5 Giá bán theo lô · 6 Giá bán TMĐT (online)**. `configs.coefficient_ecommerce_price = 1.3` |
| `product_company_coefficients` (1.105) | `product_id`, `company_id`, `coefficient` dec(10,4) | `(product_id, company_id)` | NN | `status` NULL ở **cả 1.105** dòng; **5 dòng thuộc chính công ty chủ** ⇒ ghi dòng chủ phải UPSERT (giữ `coefficient`) |
| `product_suppliers` (1.741) | `product_id`, `supplier_id` | — | **DEFAULT 1** | — |
| `product_business_catalogs` (0) | `product_id`, `company_id`, `job_cluster_id` | `(product_id, company_id, job_cluster_id)` | NN | — |
| `attribute_products` (51.128) | `product_id`, `attribute_id`, **`value`**, **`created_by`** | — | — | `need_print 1`; `unittech_id` nullable |
| `recipe_products` (6.438) | `base_product_id`, `product_id`, `unit_id`, `qty` | — | — | `is_main 0` |
| `product_has_accessories` (989) / `_install_` (28) | `base_product_id`, `product_id`, `qty`, `unit_id` | — | — | — |
| `product_has_repair_accessories` (5) | `base_product_id`, `product_id` | — | — | — |
| `productables` (45.549) | `product_id`, `productable_id`, `productable_type` | — | — | không FK |
| `product_vehicle_model_has_life` (48.736) | `product_id` int, `model_id` int, `life_id` int | — | — | không FK, kiểu `int` (không unsigned bigint) |
| `product_tech_attachments` (35) | `product_id`, `attachment_type_id` | — | — | — |
| `product_galleries` (1.548) | **`status`**, **`url`**, **`created_by`** | — | — | `position` nullable (ERP không gán) |
| `product_videos` (2) | `status`, `url`, `position`, `product_id`, `created_by` | — | — | — |
| `files` (9.020, khuôn HRM) | `table`, `table_id`, `name`, `file_name`, `file_path` | — | — | 10 dòng `table='product_tech_attachments'` |
| `product_natures` (**1 dòng rác** id 133) | `code`, `name`, `barcode_template_type` | code, name | — | `status 1`. **Chưa migration nào thêm cột** ngoài create (`Database/Migrations/2026_09_18_000001_create_product_natures_table.php`) |
| `product_types` (**0 dòng**) | `code`, `name`, `product_family_id` | code, name | — | DB có `declare_vehicle`, `declare_machine_group` (migration lỡ `2026_09_24_000001`, batch 414 — chỉ trên nhánh cũ `b833d7677`) và **không có `can_retail`** (drop batch 411) |
| `product_type_attributes` (0) | `product_type_id`, `attribute_id` | `(product_type_id, attribute_id)` | — | không có cờ bắt buộc/in tem |

**Loại SP → Tính chất**: `product_types.product_family_id → product_families.product_function_group_id → product_function_groups.product_nature_id` (3 FK NOT NULL). `ProductOptionService::productTypes` :134-169 đã join sẵn và trả `path.nature_id` ⇒ G11 chỉ cần trả thêm cờ của nature trong cùng query.

**G11 — đề xuất cột**: `product_natures.is_auto_parts` `unsignedTinyInteger` NOT NULL DEFAULT 0 (migration mới trong `Modules/MasterData/Database/Migrations/`; 2 cột `declare_*` lỡ chạy trên `product_types` để nguyên, không dùng). Sửa kèm: `ProductNature` fillable, `ProductNatureRequest`, service/resource màn Tính chất (ô tick).

---

## 4. ERP ghi thế nào — HRM bám thứ tự này

### 4.1 Tạo — `Product::createRecord()` (`app/Product.php:6827-7213`)

| # | Bảng | ERP (dòng) | HRM 2-C1 |
|---|---|---|---|
| 1 | `products` INSERT | `status=1` :6833; `code=randomString(20)` :6836; `guarantee_type ?: 'thang'`; `tech_coefficient ?? 1` :6847; `need_environment_tax` từ request :6849; `environment_tax_coefficient ?: 1`; `product_cate=json_encode([])` :6853; `min_stock_qty ?: 0` :6860; VAT + 3 thuế suy từ `tax_rates` :6866-6882; `save` :6895 | `status=1` (G1), `company_id=company_role`, mã sinh trước insert, `tech_coefficient` mặc định 1, `need_environment_tax` suy (F7), `product_cate` để NULL (đóng băng — `design.md` §3), KHÔNG ghi `guarantee*/min_stock_qty` (G5, để default) |
| 2 | mã | `generateCode()` :6897 | `ProductCodeGenerator` |
| 3 | `product_suppliers` | `sync` :6899 (company_id → default 1) | ghi theo công ty hiện tại |
| 4 | `product_videos` | `syncVideos` :832-852 (`position=1,status=1`, sync giữ id) | như ERP |
| 5–7 | 3 bảng phụ kiện | xoá + ghi :6904-6906 | như ERP |
| 8 | `recipe_products` | :6907 — `unit_id` = **ĐVT cơ bản của hàng thành phần**, không lấy từ request (:6251-6266) | như ERP |
| 9 | `product_tech_attachments` + `files` | :6908 → `syncTechAttachments` :6334-6355: xoá PTA rồi **tạo lại GIỮ `id` cũ**, tệp gắn theo `table_id = PTA.id` | phải giữ id PTA (xoá+chèn mất id ⇒ tệp mồ côi) |
| 10 | `product_company_coefficients` | :6909 chỉ khi mảng (form ERP gửi hệ số) | 1 dòng công ty chủ `coefficient=1, status=1` + 4 cột quản trị |
| 11 | `productables` | `morphedByMany()->sync()` :6911-6915 (theo từng type) | xoá+chèn **kẹp `productable_type`** (5 hằng `Productable`) |
| 12 | `product_vehicle_model_has_life` | :6918-6920 → :7560-7575 xoá + ghi | như ERP |
| 13 | `attribute_products` | chỉ dòng `require==='true'` :6922-6950, `created_by` tay | như ERP |
| 14 | `product_galleries` | insert `name='', status=1, url, created_by` :6952-6965 | thêm `position` theo thứ tự (ERP để NULL) |
| 15 | duyệt giá công ty 8 | :6975-6993 (`status=2`) | KHÔNG (giá ngoài HRM) |
| 16 | `product_units` | :7008-7049 (`cost_price` từ request) | `cost_price=0`, `buy_price=0` tường minh (G2); cơ bản `unit_coefficient=1` |
| 17 | `product_unit_prices` | loại FE gửi; loại 6 = bán lẻ × 1.3 :7063-7096 | **6 dòng/ĐVT, `price=0, coefficient=0, sale_max_percent=0`** (G2) |
| 18–19 | `product_expected_prices`, `product_approves` | :7097-7209 | KHÔNG |
| 20 | job `CreateTemplateProductMissing` | :7211 | KHÔNG (N6) |

### 4.2 Sửa — `ProductsController@update` (`:1117-1997`)

| Bảng | ERP | HRM lớp chung (chỉ chủ) |
|---|---|---|
| ĐVT | `validUnits` :1391 — phải gửi đủ id cũ; dòng cũ **không đụng** (khối sửa giá comment :1563-1644); thêm mới chỉ khi `Quản lý giá` :1547 | dòng cũ giữ nguyên (không xoá, không đổi hệ số — Q3); ĐVT mới ⇒ thêm + bù 6 dòng giá 0 (G2) |
| `product_videos` | sync giữ id :1428 | như ERP |
| `attribute_products` | xoá hết + create :1438-1454 | như ERP |
| `product_suppliers` | `sync` :1463 (mọi công ty!) | tab Quản trị, chỉ dòng `company_id` của mình |
| `product_barcodes` | `sync(null)` :1470 ⇒ xoá sạch | KHÔNG đụng |
| `product_galleries` | xoá hết + insert :1479-1492 | như ERP |
| 3 phụ kiện, công thức, tech | xoá + ghi :1497-1525 | như ERP (tech giữ id PTA) |
| `product_company_coefficients` | xoá hết dòng mọi công ty + ghi :1532 | KHÔNG xoá; chỉ upsert dòng của mình ở tab Quản trị |
| `products` | gán lại toàn bộ :1858-1896, **`status=1`** :1861, **`company_id=request`** :1870 | không đổi `status`, `company_id`, `code`; không ghi `product_cate`, `rate_liquidation`, `guarantee*`, `min_stock_qty` |
| `productables` + đời xe | sync theo type :1904-1908, :1912 | như tạo |
| Lịch sử | `product_versions/histories` | KHÔNG (§14b) |

Tab Quản trị (chủ ở 2-C1, lấy về ở 2-C2): upsert `product_company_coefficients(product_id, company_id)` — có dòng ⇒ UPDATE 4 cột (+ `status` nếu NULL), giữ `coefficient`; chưa có ⇒ INSERT `coefficient=1`, `status` = 1 (hàng tạo mới) hoặc **3 (hàng cũ — G4)**; NCC + catalog xoá+chèn trong phạm vi `company_id` của mình.

---

## 5. Tệp / ảnh / video

| Loại | ERP lưu | Đường upload ERP |
|---|---|---|
| Ảnh đại diện `products.avatar`, ảnh `product_galleries.url` | URL S3 tuyệt đối `https://s3.cloud.cmctelecom.vn/tanphat/erp_products/<slug>-<time>-<rand>.<ext>` + 2 bản `-thumbnail` (75px) / `-large` (200px). Dữ liệu cũ còn `/uploads/products/...` tương đối | `POST /uploadProductImg` (`routes/web.php:5993`) → `UploadController::uploadProductImg` :17-55 → `CmcS3Helper::putFileProduct` (ép folder `erp_products`) trả URL bản chính; form gửi URL vào `avatar`/`galleries[]` |
| ERP đọc thumbnail | accessor `image` dựng `<avatar>-thumbnail.<ext>` (`app/Product.php:891-897`) ⇒ **thiếu bản thumbnail là ảnh vỡ ở danh sách ERP** | |
| Tài liệu kỹ thuật | `files` khuôn HRM: `table='product_tech_attachments'`, `table_id=PTA.id`, `file_path` = URL S3 `tanphat/products/...` (ERP gop_db `FileHelper::saveFile` + `getTableOfClass`) | `FileHelper::uploadFiles($a['attachments'],'products',…)` trong `syncTechAttachments` |
| Video | chỉ URL do người dùng nhập (2 dòng, đều rỗng) | không upload |

**HRM đã có**: `app/Helper/CmcS3Helper.php` cùng bucket `tanphat`, endpoint CMC — `putFile` :59, `putFileProduct($file,$folder)` :116-158 (sinh đủ 3 bản), `TEMPORARY_FOLDER='tanphat_hrm/tmp'` :17 + `promoteTemporary` :207-230; route chung `POST files/upload` (`Modules/Human/Routes/api.php:258-261` → `FileController::uploadImage` :27-44, `?temporary=1`); `app/Helper/TableFileHelper.php` ghi bảng `files` khuôn table/table_id (`createForTable` :10, `syncForTable` :22, `normalizePayload` :64).

**Đề xuất**:
- Ảnh: endpoint riêng `POST master-data/products/upload-images` (gate 1652) gọi `putFileProduct($file, 'erp_products')` ⇒ đúng khuôn ERP (có thumbnail). Validate `image|max` + ≤10 ảnh. File lẻ khi bỏ form: chấp nhận như ERP (chưa kiểm có cần dọn).
- Tài liệu kỹ thuật: FE upload `files/upload?temporary=1`; lúc Lưu Service `promoteTemporary(url,'products')` rồi `TableFileHelper::createForTable('product_tech_attachments', $pta->id, …)`; xoá tệp = xoá dòng `files` theo id (ERP chỉ gỡ gắn). Khuôn này đã chạy ở `MeetingService:887-888`.
- Local `.env`: `FILESYSTEM_DRIVER=local`, `AWS_BUCKET=` trống — chưa kiểm `CmcS3Helper` lấy khoá từ đâu ⇒ upload thật trên máy dev **chưa kiểm**; test PHPUnit nên giả lập S3.

---

## 6. Bản đồ file BE đề xuất cho 2-C1

### 6.1 Endpoint

| Method · path (`master-data/products`) | Gate | Việc |
|---|---|---|
| `POST /` | 1652 | tạo (lớp chung + tab Quản trị của công ty hiện tại), 1 transaction |
| `PUT /{product}` | 1652 + **chủ** (403 nếu không) | sửa lớp chung (5 tab con + `tech_coefficient` T6) |
| `PUT /{product}/admin-data` | 1652 + chủ (2-C2 mở cho công ty lấy về) + status ≠ 4 | 4 cột quản trị + NCC + catalog của công ty mình; G4 cho hàng cũ |
| `GET /{product}` (mở rộng) hoặc `GET /{product}/edit` | 1652 | thêm các trường thiếu ở mục 1.3 |
| `GET /attributes-by-type/{productType}` | không | thuộc tính theo `product_type_attributes` (nhánh cũ khai route nhưng **chưa viết** method) |
| `POST /upload-images` | 1652 | mục 5 |
| `GET /vehicle-options` (sửa) | — | thêm `vehicle_lives` |
| `GET /machine-options` hoặc thêm vào form-options | — | `groups` (Nhóm máy, bảng ERP) |
| tìm hàng cho 4 bảng kèm theo + Máy | — | tái dùng `GET /warehouse?keyword` hoặc thêm `option-search?type=products` trả kèm ĐVT của hàng (phụ kiện cần `unit_id` thuộc hàng đó) |
| Thêm nhanh Model / Code đặt hàng | — | đã có `POST product-models`, `POST order-codes` (gate `Quản lý danh mục model/code đặt hàng`) — xem Q7 |

### 6.2 File

| Loại | File |
|---|---|
| Create | `Services/Product/ProductCodeGenerator.php` (nguyên nhánh cũ) · `Services/Product/ProductWriteService.php` (store / updateCommon / updateAdminData, sinh 6 dòng giá, upsert dòng công ty, retry 1062) · `Http/Requests/Product/ProductCommonRequest.php` + `ProductAdminDataRequest.php` (POST dùng gộp 2 bộ) · `Http/Controllers/V1/Product/ProductWriteController.php` (hoặc thêm vào `ProductController`) · `Entities/Product/ProductUnitPrice.php` · `Entities/Product/ProductVehicleModelLife.php` · migration `add_is_auto_parts_to_product_natures_table` · `Tests/Feature/ProductCodeGeneratorTest.php` · `Tests/Feature/ProductWriteApiTest.php` |
| Modify | `Routes/api.php` (khối :253-279, route tĩnh trước `/{product}`) · `ProductOptionService.php` (vehicle lives, nature cờ G11 trong `productTypes`, groups, attributesByType) · `ProductOptionController.php` · `ProductCatalogService.php` (tách `checkClustersOpen`) · `ProductDetailResource.php` + `ProductService::show` (trường cho form sửa) · `Entities/Product/Product.php` (quan hệ đời xe; cân nhắc bỏ `rate_liquidation`, `code`, `status`, `company_id` khỏi fillable) · `ProductNature` entity/request/service/resource (cờ G11) |
| DB local (hỏi riêng) | chạy 1 migration `product_natures` |

### 6.3 PHPUnit tối thiểu

Tạo (đủ 7 cột, mã, 1 ĐVT cơ bản, 6 dòng giá 0/ĐVT, dòng công ty coef 1 status 1, `company_id = company_role` khác `company_id` của info) · sửa lớp chung (mã không đổi, `status/company_id` không đổi, ĐVT cũ + giá cũ không đổi, bù giá cho ĐVT mới) · 403 công ty khác / không quyền 1652 · bất biến `productables` (loại không thuộc tab không đổi số dòng) · upsert dòng chủ đã có hệ số cũ (giữ coefficient) · hàng cũ chưa có dòng ⇒ status 3 (G4) · tech attachment giữ id PTA · fixture Loại SP chèn bằng `DB::table` (bảng rỗng).

---

## 7. Rủi ro / bẫy mới

| # | Bẫy | Đo / nguồn | Hệ quả |
|---|---|---|---|
| R1 | `ProductUnit::prices()` trỏ class không tồn tại | `ProductUnit.php:56-59`, `git grep` 0 kết quả | gọi là fatal — phải tạo entity trước |
| R2 | `product_types` 0 dòng + DB thiếu `can_retail` mà `ProductTypeService:78` luôn ghi | information_schema | màn Loại SP lưu lỗi 1054 trên local ⇒ không có Loại SP để tạo hàng thủ công / e2e; test phải chèn fixture. Thuộc tồn E1 (sổ chốt) |
| R3 | `products.product_type` (chuỗi) NULL ở hàng HRM tạo | ERP `SearchController` lọc `!= 'service_product'` 4 hàm (`man-danh-muc-hang-hoa/design.md` §6a) | hàng **không hiện ở popup 338 màn ERP** (G1 kỳ vọng hiện) + `getDataAttribute` `PRODUCT_TYPES[null]` lỗi. Chưa có trong N1–N8 ⇒ Q3 |
| R4 | `tech_coefficient` = 0 ở **11.156** hàng (8.867 status 1) vs `min:1` | SELECT | sửa hàng cũ bấm Lưu lỗi dù không đụng ô ⇒ Q2 |
| R5 | `avatar` trống ở 356 hàng status 1; ERP `required` | SELECT, `app/Product.php:301` | bắt buộc ⇒ hàng cũ sửa bị chặn ⇒ Q1 |
| R6 | 45.890/45.890 hàng cũ `product_type_id NULL` | SELECT | Loại SP `required` ⇒ mọi lần sửa lớp chung hàng cũ đều buộc chọn Loại SP (cây đang rỗng!) ⇒ Q4 |
| R7 | 30 nhóm trùng (tên×model×thương hiệu×hãng) | SELECT | sửa 1 hàng trong nhóm trùng ⇒ lỗi unique dù không đổi tên ⇒ Q6 |
| R8 | Chủ sửa tab Quản trị hàng CŨ = luật G4 rơi vào 2-C1 (không phải chỉ 2-C2) | 44.816 hàng của Cty 1 | dòng coef 1 ⇒ giá popup ERP làm tròn nghìn (đã chấp nhận ở G4) |
| R9 | 5 dòng hệ số cũ thuộc chính công ty chủ, `status NULL` | SELECT | INSERT mù nổ 1062 ⇒ upsert |
| R10 | Xoá+chèn `product_tech_attachments` mất id | ERP giữ id `:6340` | tệp ở `files` mồ côi |
| R11 | Thiếu bản `-thumbnail` khi HRM upload ảnh bằng `putFile` thường | `app/Product.php:891-897` | ảnh vỡ ở danh sách ERP ⇒ dùng `putFileProduct` |
| R12 | `repair_accessories` rule cũ đòi `unit_id/qty` | `ProductRequest` cũ :171-174 vs schema | lưu không được phụ kiện sửa chữa |
| R13 | `product_vehicle_model_has_life` cột `int`, không FK | schema | phải `exists` ở request |
| R14 | `BaseModel` dùng `LogsActivity` (`logFillable`) | `BaseModel.php:17-23`, bảng `activity_log` có | mỗi lần lưu sinh dòng `activity_log` — khác "không ghi lịch sử" §14b nhưng vô hại (chưa kiểm khối lượng) |
| R15 | Hàng `products.status = 0` (ERP đã xoá) vẫn mở được `show` | `ProductService::show` không lọc | có thể sửa hàng đã xoá ⇒ đề xuất chặn sửa (tự chốt nếu user không phản đối) |
| R16 | Công ty 8 bật duyệt giá ERP | `companies.is_new_company=1` | HRM tạo hàng Cty 8 ghi `status=1` + giá 0 thẳng, không qua `product_approves` — theo G1/G2, ghi nhận |

---

## 8. Câu hỏi nghiệp vụ còn mở (hỏi lần lượt, ⭐ = đề xuất)

| # | Câu | Phương án |
|---|---|---|
| Q1 | Ảnh đại diện bắt buộc? | ⭐ không bắt buộc (mockup không `*`, 356 hàng cũ trống) · hay bắt buộc như ERP |
| Q2 | `tech_coefficient` hàng cũ = 0 | ⭐ rule `nullable|min:0|max:1000`, tạo mới mặc định 1 · hay `min:1` chỉ khi ô bị đổi |
| Q3 | `products.product_type` của hàng HRM tạo (R3) | (a) ghi giá trị cố định (vd `product`) cho tới khi ERP bỏ lọc · ⭐ (b) để NULL + thêm việc ngoài luồng **N9** (bỏ lọc `!= 'service_product'` ở `SearchController`, `design.md` §6b) — chấp nhận hàng HRM tạo chưa chọn được ở ERP tới lúc đó |
| Q4 | Sửa hàng cũ (`product_type_id NULL`) có buộc chọn Loại SP? | ⭐ buộc (mockup `*`, cũng là đường gán dần cây mới) · hay chỉ buộc khi tạo |
| Q5 | Catalog ≥ 1 nhánh (C5-a) còn bắt buộc khi Lưu? (plan 2-C1 không nhắc, G3 chỉ nói "đủ trường bắt buộc") | ⭐ còn, cả tạo lẫn sửa tab Quản trị |
| Q6 | Rule trùng tên | ⭐ khuôn ERP store, chỉ kiểm khi 1 trong 4 cột (tên, model, thương hiệu, hãng) đổi · hay kiểm mọi lần |
| Q7 | Nút "+" thêm nhanh Model / Code đặt hàng | ⭐ gọi route danh mục sẵn có, ẩn "+" khi thiếu quyền `Quản lý danh mục model/code đặt hàng` · hay endpoint riêng gate 1652 |
| Q8 | ĐVT đã lưu khi sửa: cho xoá / đổi hệ số / đổi đơn vị cơ bản? | ⭐ bám ERP — khoá dòng đã lưu, chỉ thêm dòng mới (chứng từ cũ trỏ `unit_id`) |
