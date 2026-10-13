# Đợt 2-D "ERP không lỗi" — Khảo sát PHẦN A: CHẶN GHI hàng hoá phía ERP (09/10/2026)

> Đây là khảo sát CHỈ ĐỌC: đọc code và chạy SELECT, không sửa source, không ghi DB, không chạy artisan.
> Mã nguồn: `ERP/TanPhatDev`, nhánh đang checkout **`develop_01`** (`46ab7152e5`, working tree sạch). Số dòng trích dưới đây
> lấy theo `develop_01`. ⚠️ Nhánh `gop_db` của ERP lệch **359/222 commit** so với `develop_01`. Nhóm route `products` ở
> `gop_db` nằm ở dòng **563** thay vì **571** (`git show gop_db:routes/web.php`), tức lệch khoảng −8 dòng. Nội dung route
> hàng hoá hai nhánh gần như giống nhau, `gop_db` chỉ có thêm `download-export-file`.
> Số đo: DB `hrm_erp` (DB gộp mà HRM đang dùng; bản chụp dữ liệu ERP mới nhất là **15/09/2026**). "6 tháng" ở dưới
> nghĩa là khoảng **15/03 → 15/09/2026**.
> Tiền đề: QĐ §10 (ERP chỉ ĐỌC hàng hoá), QĐ §13 (chặn route ERP), tiền đề #9 (việc ngoài luồng thì note lại), G10
> (phạm vi 2-D chốt khi lập plan), N2/N3/N4 (`2c-ghi/chot.md`). Bản đồ ghi gốc ở `2c-ghi/erp-ghi-hang-hoa.md` §1. Tài liệu này
> **bổ sung và đính chính** bản đồ đó (xem mục 8).

---

## 0. Tóm tắt

1. ERP có **5 nhóm đường ghi** vào `products` + bảng con: (A) **66 route** trong nhóm `products/*` (+3 ở `web.php:45-49`). Trong đó
   **23 route GHI cần chặn**, **9 route GHI phải giữ** (mua hàng, giá, duyệt giá) và **34 route CHỈ ĐỌC** mà các màn khác đang
   gọi (riêng `getData` có khoảng **93 chỗ gọi**). (B) các màn danh mục ghi lan:
   Hãng SX, Thương hiệu, Thuế suất, Nhóm. (C) các màn hàng hoá song song: hàng gốc, Product2, hàng có sẵn/đồng bộ, hàng tạm.
   (D) luồng giá: Phiếu tính giá, Duyệt giá, Cập nhật giá nhanh, giá theo hãng, 2 cron giá. (E) 9 bộ import Excel + 5 job nền.
2. ⇒ **Không chặn được bằng tiền tố `products/*`.** Phải chặn **theo từng route**: 23 route ở `products/*` + 9 ở
   `product_templates/*` + 12 ở `product2/*` + 6 ở `product-infos`/đồng bộ.
3. 🔴 **Đường lách mới phát hiện: Danh mục hàng hoá GỐC.** 29.813 hàng (65%) có hàng gốc 1–1, sinh ra từ job
   `CreateTemplateProductMissing`. Sửa hàng gốc sẽ bắn `UpdateGenerateProduct` **ghi đè toàn bộ hàng hoá** (tên, hãng, nhóm,
   `company_id`, `status=1`, NCC, phụ kiện, hệ số công ty, xe…). Hàng gốc không biết các thay đổi HRM đã làm ⇒ dữ liệu cũ đè lên
   dữ liệu mới. Phải chặn cùng đợt.
4. 🔴 **N2 (Hãng SX) đang chạy thật.** Mỗi lần Lưu sửa hãng là ghi đè `products.company_id` của **mọi hàng status 1 của hãng**,
   vô điều kiện. Nếu người dùng nhập bảng "Hệ số giá theo công ty" thì còn **xoá sạch rồi ghi lại** `product_company_coefficients`
   của từng hàng, làm mất dòng trạng thái theo công ty mà HRM tạo. Đo được: hãng sửa ~10–20 lần/tháng; `product_company_coefficients`
   sinh **571 dòng tháng 7** + **151 dòng tháng 8/2026**. Đề xuất: **bỏ hẳn khối lặp `products`** ở `update()` và **ẩn thẻ "Hệ số giá
   theo công ty"**.
5. 🟢 **N3 (Thương hiệu) thực tế đã chết.** Ô tick "Cập nhật sản phẩm" ở form sửa đã bị comment
   (`catalogs/brands/edit.blade.php:71-76`). Lúc tạo mới thì hãng mới chưa có hàng nào nên không ghi gì. Đề xuất vẫn gỡ 2 lời gọi
   cho chắc (rủi ro ~0).
6. **Danh sách trắng (N4) phải giữ:** `updateEnglishName` (**214** lần sửa riêng tên TA trong 6 tháng, từ **14 màn mua hàng**),
   `updateHSCode` (2 màn), `addEquipment` (không ghi `products`), cùng toàn bộ route đọc. Luồng **giá** (Cập nhật giá nhanh,
   Duyệt giá, Phiếu tính giá, cron) và **hàng tạm** (18% hàng mới) giữ lại ERP tới Phase 8/7/6.
7. **Cách chặn đề xuất:** middleware route mới (gắn **từng route**, trả trang/JSON "Đã chuyển sang HRM" + link), ẩn menu/nút.
   **KHÔNG gỡ quyền** vì `Thêm/Sửa/Xóa hàng hóa` dùng chung với 4 màn khác và còn chặn cả route đọc. Có thể thêm observer
   **chỉ ghi log** để bắt đường sót.
8. Phát hiện phụ (ghi vào việc ngoài luồng, KHÔNG vá trong 2-D): `GET products/change` **không gate quyền** mà ghi hàng loạt;
   3 route `view-import*` không gate quyền; 4 route `approve*Submit` không gate quyền; `manualUpdatePrices` là GET nhưng có ghi;
   trùng tên route `productDelete`; HRM Thuế suất không lan thuế xuống `products` như ERP; **1.290 hàng** có công ty của Thương
   hiệu ≠ công ty của Hãng SX.

---

## 1. Kiểm kê đường GHI

Ký hiệu cột "Đo": số trong 6 tháng 15/03–15/09/2026 trên `hrm_erp`.

### 1.1 Nhóm route `admin/products/*` — `routes/web.php:571-645` (+ `:45-49`)

Middleware chung của cả nhóm: `sso.check`, `userLogin`, `PreventDuplicateSubmission` (`routes/web.php:72`). Quyền gắn **trên
từng route** bằng `checkPermission:<tên quyền>`, xem `app/Http/Middleware/CheckPermission.php:17-27`. Khi không có quyền: POST/PUT
trả JSON 403, GET trả view `not_found`.

**a) Route GHI** (method nằm trong `app/Http/Controllers/ProductsController.php`)

| Dòng route | Route | Method :dòng | Ghi gì | Quyền | Ai gọi | Đo |
|---|---|---|---|---|---|---|
| 572 | GET `create` | `create` :723 | (mở form) | Thêm hàng hóa | nút "Thêm mới" `products/list.blade.php:47` | — |
| 573 | POST `/` | `store` :909 | `Product::createRecord()` → `products` + 14 bảng con + job hàng gốc (`app/Product.php:6827-7213`) | Thêm hàng hóa | form tạo, form sao chép | ~4.242 hàng tạo **không qua** hàng tạm (5.203 tổng − 961 từ hàng tạm) |
| 574 | POST `storeService` | `storeService` :743 | tạo nhóm "Hàng hoá làm dịch vụ" + `createRecord` | **Thêm báo giá** | `partials/serviceProduct/createServiceProductJs.blade.php` (báo giá dịch vụ) | **0** (36 hàng, mới nhất 17/07/2023) |
| 576 | GET `{id}/edit` | `edit` :1020 | (mở form) | Sửa hàng hóa | menu dòng, nút ở show | — |
| 578 | GET `{id}/copy` | `copy` :1084 | (mở form, post về `store`) | Thêm hàng hóa | menu dòng | — |
| 579 | POST `{id}/update` | `update` :1117 | gán lại mọi cột, **`status=1`**, **`company_id`=request**, xoá rồi ghi lại 11 bảng con, `product_versions/histories` | Sửa hàng hóa | form sửa | (lịch sử: `name` 1.743, `vat_percent` 1.683, `note` 1.576…) |
| 580 | GET `{id}/delete` | `delete` :1999 | `status=0`, `deleted_at` | Xóa hàng hóa | menu dòng, show | — |
| 581 | POST `bulkDelete` | `bulkDelete` :4588 | `status=0` | Xóa hàng hóa | `products/list.blade.php:727` | — |
| 606 | GET `{id}/restore` | `restore` :2020 | `status=1` | Khôi phục hàng hóa | menu dòng tab "Đã xoá" | — |
| 590 | POST `importExcel` | `importExcel` :2033 | `ProductsImport` (`new Product`) | Thêm hàng hóa | (không còn view nào gọi) | — |
| 591 | POST `importExcelNew` | :2079 | `ProductsImportNew` (tạo + sửa hàng cũ :239) | Thêm hàng hóa | `products/list.blade.php:839` | — |
| 592 | POST `importExcelInstallWork` | :2163 → `Jobs/InstallWorkImportJob` → `ExcelImports/InstallWorkImport.php:50-52` | `products.norm`, `tech_coefficient` | Thêm hàng hóa | `products/list.blade.php:753` + `product_templates/list` | — |
| 593 | POST `importExcelAttribute` | :2200 → `Jobs/ImportProductAttributeJob` → `ExcelImports/ImportProductAttribute.php:63,92` | xoá rồi ghi `attribute_products` | Thêm hàng hóa | `products/list.blade.php:796`, `catalogs/brands/list.blade.php` | — |
| 640 | **GET** `importExcelZitecProduct` | :2125 | `ProductsImportZitec` từ file cứng trong `public/excel_product_zitec/` | Thêm hàng hóa | (lệnh tay 2024) | — |
| 621 | POST `{id}/deleteFile` | :3659 | `products.tech_attachments`, version/history | Sửa hàng hóa | (không view nào gọi) | — |
| 627 | **GET** `change` | :3762 | `product_type='product'`, `product_cate='hang_khong_ban_duoc'` cho mọi hàng `no_sale` | 🔴 **không có quyền nào** | lệnh sửa dữ liệu một lần | — |
| 628/630 | GET `update-products` / POST `start-update-products` | :3878 / :3884 | "Cập nhật nhanh hàng hoá": tên, tên TA, `product_type`, `product_cate`, tồn min/max, xuất xứ, 4 loại thuế, HS, barcode, ghi chú + version/history | Sửa hàng hóa | menu `topmenubar.blade.php:22` | — |
| 632-634 | GET `view-import`, POST `view-import/import-vat-10`, `import-beta-product` | :3787/:3796/:3824 → `ExcelImports/UpdateVat10PercentProduct.php:47`, `UpdateVatProductBeta.php:49` | `products.vat_*` | 🔴 **không có quyền nào** | `products/view_import.blade.php` (không có menu) | — |
| 636-637 | GET `viewImportProductExtend`, POST `view-import-product-extend` | :3847/:3852 → `ExcelImports/ImportProduct160223.php:117-130` | tạo `products` + đơn vị + giá | 🔴 **không có quyền nào** | `products/view_import_product_extend.blade.php` (không có menu) | — |

**b) Route GHI nhưng phải giữ — DANH SÁCH TRẮNG có ghi**

| Dòng | Route | Method :dòng | Ghi gì | Quyền | Ai gọi | Đo |
|---|---|---|---|---|---|---|
| 612 | POST `{id}/updateEnglishName` | :3449 | `products.english_name` + version/history | Tổng hợp đặt hàng | **14 view mua hàng**: `orders/order_notification2/summary:164`, `inland_order_notification_new/summary:166`, `inland_purchase_invoice/{create:159,edit:185,show:1581}`, `purchase_invoice/{create:121,edit:142,show:1955}`, `inland_buy_contract_new/{create:105,edit:131}`, `import_records/edit:99`, `buy_contract2/edit:150`… | **214** version chỉ đổi `english_name` |
| 613 | POST `{id}/updateHSCode` | :3505 | `products.hs_code` + version/history | Mua hàng | `orders/buy_requests/formJs:76`, `inland_buy_contract_new/formJs:59` | 26 lần đổi `hs_code` (gồm cả form) |
| 575 | POST `addEquipment` | :792 | **không ghi `products`** — ghi `equipment_olds` / `external_equipments` / `service_has_products` | Thêm báo giá | `sale/service_quotations/formJs` | — |
| 604 | POST `{id}/updatePrice` | :2552 | `product_units`, `product_unit_prices` (+ version) | Cập nhật nhanh giá hàng hóa | `products/editPrices:634`, `price_updating:188` (+ 2 bản `product_templates/*`) | ⏸ luồng GIÁ — Phase 8 |
| 617 | **GET** `manualUpdatePrices` | :2242 | áp `product_expected_prices` hôm nay vào `product_unit_prices` + version/history | Quản lý giá | `products/expectedPrices.blade.php` | ⏸ luồng GIÁ |
| 597-600 | POST `approveSubmit` · `notApproveSubmit` · `approvesSubmit` · `notApprovesSubmit` | `ProductApprovesController:188-498` | `products.status` (1/5), đơn vị, giá, giá dự kiến | 🔴 **không có `checkPermission`** (chỉ `index` :595 có `Duyệt giá hàng hoá`) | màn Duyệt giá | `product_approves` = **0** dòng |

**c) Route CHỈ ĐỌC — DANH SÁCH TRẮNG** (34 route, không chặn; số trong ngoặc là số file gọi, đếm trong `resources/views` + `public/js`)

`show` 577 · `history` 582 · `index` 583 · `barcode` 584 (in tem; chỉ ghi `warehouse_import_lots` :630, không đụng `products`) ·
`searchData` 585 · `importLogLink` 586 · `exportExcel/CSV/PDF` 587-589 · `editPrices` 594 (chỉ mở màn) · `approvePrices` 595 ·
`approvePricesSearchData` 596 · `approveExportExcel` 601 · `priceUpdating` 602 · `getProductsAndPrices` 603 · `deleted` 605 ·
**`getData` 607 (~93 chỗ gọi: popup chọn hàng của mọi phiếu)** · `getDataForPriceAsking` 608 (1) · `getDataForInventory` 609 (3) ·
`getDataForAccountingInventory` 610 (3) · POST `getListDataForAccountingInventory` 611 (1) · `getDataForJoin` 614 (2) ·
`getRecipe` 615 (4) · `expectedPrices` 616 · `getAccessories` 618 (4) · `validateLanguage` 619 · `longStock` 620 (5) ·
`getListForReport` 622 (1) · POST `checkNeedVat` 623 (2) · `searchProductsByKeyword` 624 (1) · `getDropdownData` 625 ·
`getCustomerPrepickByEmployee` 638 (1) · `exportExcelNorm` 641 (2) · `exportProduct` 642 (3) · và nhóm đầu file
`:46` POST `getPriceOfProducts` (13 file) · `:47` `download-file` · `:48` `download-stock-zip`.

⇒ Có **3 route POST chỉ đọc** (`getPriceOfProducts`, `getListDataForAccountingInventory`, `checkNeedVat`), và lại có
route **GET có ghi** (`change`, `importExcelZitecProduct`, `manualUpdatePrices`). Vì vậy **không chặn theo động từ HTTP** được.

### 1.2 Màn danh mục ghi lan sang hàng hoá

| # | Màn (menu) | File:dòng | Ghi gì | Điều kiện kích hoạt | Đo |
|---|---|---|---|---|---|
| **N2** | **Danh mục hãng sản xuất** (`topmenubar:30`, route `manufactures/*` `web.php:169-199`) | `Sale/ManufacturesController.php:186-190` (store) · **`:270-275` (update)** → `app/Product.php:6290-6302` `syncCompanyCoefficients` | `products.company_id = manufactures.company_id` cho **mọi hàng `status=1` của hãng** (Eloquent `save()`, có `updated_by`) · sau đó, nếu request có mảng `company_coefficients`, thì **`DELETE` mọi dòng `product_company_coefficients` của hàng rồi INSERT lại** `(company_id, coefficient)` theo bảng của hãng | store: không làm gì thực tế (hãng mới chưa có hàng). **update: mỗi lần Lưu là ghi đè `company_id`.** Xoá hệ số chỉ khi người dùng thêm ≥1 dòng ở thẻ "Hệ số giá theo công ty" (`catalogs/manufactures/form.blade.php:83-140`; form sửa không nạp dòng cũ — `Manufacture::getDataForEdit` :155 không `with` hệ số; jQuery bỏ mảng rỗng ⇒ `is_array(null)` = false) | hãng `updated_at` ~7–21/tháng; `product_company_coefficients` tạo **571** dòng (07/2026) + **151** (08/2026); hiện có **367** hàng status 1 mà `company_id` ≠ công ty của hãng |
| **N3** | **Danh mục thương hiệu** (`topmenubar:29`, `brands/*` `web.php:236-250`) | `Sale/BrandsController.php:138` (store), `:215` (update, khi `update_products=='on'`) → `Model/Product/Brand.php:153-158` | `UPDATE products SET company_id=? WHERE status=1 AND brand_id=?` (query builder, không cập nhật `updated_by`) | store: thương hiệu mới chưa có hàng nên không ghi gì. update: ô tick `update_products` **đã bị comment** ở `catalogs/brands/edit.blade.php:71-76` ⇒ **không bao giờ gửi lên** | 0 lần chạy thật; **967** hàng status 1 mà `company_id` ≠ công ty của thương hiệu |
| — | Thương hiệu "hàng có sẵn" (`pi-brands`) | `Sale/ProductInfo/BrandsController.php:141,219` → `Model/ProductInfo/PIBrand.php:34-38` | chỉ ghi `product_infos`, **không** ghi `products` | — | `product_infos` = 0 |
| E7 | **Danh mục thuế suất** (`topmenubar:34`, PUT `tax-rates/{id}` `web.php:368`, quyền Sửa thuế suất) | `Common/TaxRatesController.php:170-215` → `Jobs/DispatchUpdateProductTaxRateChunkJob` → `Jobs/UpdateProductOrGroupTaxValueJob.php:46` | `DB::table('products')->update([vat_percent / import_tax / import_tax_has_co / antidump_duty])` cho mọi hàng trỏ mức thuế đó (queue) | đổi `tax_rate` | — |
| E8 | **Danh mục nhóm hàng hoá** (PUT `groups/{id}` `web.php:110`, quyền Sửa nhóm) | `Model/Product/Group.php:23-27` (event `updated`) → `:193-205` → `Jobs/UpdateProductFromGroupChangeTaxJob.php:49` | `products.vat_percent(_tax_rate_id)` của mọi hàng thuộc nhóm | đổi `vat_percent_tax_rate_id` của nhóm | — |

### 1.3 Màn hàng hoá song song (tạo/sửa `products` ngoài form chính)

| # | Màn (menu `topmenubar`) | Route | Ghi | Đo | Mức |
|---|---|---|---|---|---|
| C1 | **Danh mục hàng hoá gốc** (`:19`) | `product_templates/*` `web.php:507-533`: create/store/edit/copy/update/delete (quyền Thêm/Sửa/Xóa hàng hóa) | `store` :913 → `Jobs/GenerateProduct` (tạo **N hàng biến thể** + `CreateProductUnitsAfterMapping`); **`update` :1628-1632 → `UpdateGenerateProduct::dispatch` cho MỌI `products` có `product_template_id` = hàng gốc** → `Jobs/UpdateGenerateProduct.php:61-210`: ghi đè `name, english_name, status=1, product_type, model, brand, manufacture, origin, company_id, group_id, hs_code, thuế…`, sync NCC, barcode, xoá+ghi ảnh/phụ kiện/công thức/tài liệu, **`syncCompanyCoefficients`**, productables | **29.813/45.890** hàng có hàng gốc (1–1, sinh bởi `CreateTemplateProductMissing`); `product_templates` sửa sau khi tạo: **2** lần / 6 tháng | 🔴 |
| C2 | **Danh sách hàng chờ nhập giá / đang tạo** (`:65-66`) | `product2/*` `web.php:667-679` | `Product2Controller` (`createRecord` :506, update/2/3, `syncCompanyCoefficients` :1260), `CreateProductService` | `products.status IN (3,4)` = **0** | ⚪ chưa dùng |
| C3 | **Hàng hoá có sẵn / Đồng bộ hàng hoá** (`:49,64,67,68`) | `product-infos/*` `:650-661` (`syncInfo` :661 **không gate quyền**) · `sync-products-info/*` `:689-691` · `sync-category-info/*` `:683-685` | `ProductInfoController:1128-1235` (`$product->save()` + sync), `SyncProductController:85-104` → `Services/ProductInfo/SyncProductInfoService.php:37-124` (`new Product` status `CHO_NHAP_THONG_TIN_BAN_HANG`) | `product_infos` = **0** | ⚪ chưa dùng |
| C4 | **Danh mục hàng tạm** (`:21`, `:1551`, `:2271`) | `tmp_products/{id}/approve` `web.php:702` (chỉ `checkDueConfigs`) | `Sale/TmpProductsController.php:566` `Product::createRecord($request, $tmp->id)` | **961/5.203** hàng mới (18%) | 🟡 Phase 6 |

### 1.4 Luồng giá (ghi bảng con giá — ở lại ERP tới phase giá)

| # | Màn / cron | File:dòng | Ghi | Đo |
|---|---|---|---|---|
| E3 | Phiếu tính giá (`topmenubar:950`) — store/update khi `DA_DUYET` | `Order/PriceCalculateController.php:160-165, 224-230` → `Model/Order/PriceCalculate.php:332-372` (`products.note` :368), `:376+` (`product_units`, `product_unit_prices`, `product_expected_prices`, version/history; `:567` `$product->save()`) | 3.120 phiếu, mới nhất 14/09/2026 |
| E4 | Cập nhật giá theo hãng (`:952`) | `Sale/ManufactureExpectPriceController.php:116` → `Model/Product/ManufactureExpectPrice.php:71-205` | 87 dòng, mới nhất 21/12/2022 |
| E5 | Cron `product:update_price` 01:00 | `Console/Kernel.php:47-49`, `Console/Commands/UpdateProductPrice.php:83` | `price_logs` 1–10/tháng |
| E6 | Cron `product:reset_price_when_zero_inventory` 14:30 | `Kernel.php:100-102`, `Commands/ResetProductPriceWhenZeroInventoryCommand.php` | — |
| E10 | Duyệt giá | xem 1.1b | 0 |

### 1.5 Job nền / đồng bộ

| Job | Ai bắn | Ghi `products`? |
|---|---|---|
| `CreateTemplateProductMissing` | `app/Product.php:7211` (mọi `createRecord`) | `products.product_template_id` (`:349`) |
| `createTemplateProduct` | (rà tay) | `products.product_template_id` (`:300`) |
| `GenerateProduct`, `CreateProductUnitsAfterMapping` | hàng gốc store | tạo hàng + đơn vị/giá + `attribute_products` |
| `UpdateGenerateProduct` | hàng gốc update | ghi đè toàn bộ (C1) |
| `UpdateProductOrGroupTaxValueJob`, `UpdateProductFromGroupChangeTaxJob` | Thuế suất / Nhóm | cột thuế |
| `InstallWorkImportJob`, `ImportProductAttributeJob` | import trên màn hàng hoá | `norm`, `tech_coefficient` / `attribute_products` |
| Cron `sync:crm` 19:30 (chỉ prod) | `Kernel.php:130` | **chỉ đọc** `products` (ghi `module_mappings`) — không chặn |
| API `v1/tmp-product-requests/*` (HRM → ERP) | `Api/TmpProductRequestSyncController` → `Services/Sale/TmpProductRequestSyncService.php:160-166` | **chỉ đọc** `products` |
| API `v1/hrm/products/*` | `Api/HrmProductSearchController` | chỉ đọc |

Bảng `jobs` hiện **trống**, tức lúc chuyển không có job tồn đọng.

### 1.6 Đã rà và loại trừ (dương tính giả)

Bản quét "biến `$product` → `save()`" trả về khoảng 30 chỗ ở `Model/Order/*`, `Model/Warehouse/*`,
`Customers/HandoverAcceptanceRecord`. **Tất cả đều là biến tái dùng cho dòng chi tiết chứng từ**, không phải `App\Product`,
vd `InlandBuyContractNew.php:1196`, `ProductExportsController.php:782`. Ngoài ra:
`BeginningStocksImport`, `BeginningAccountingStocksImport`, `InventoryImport`, `PositionInvetoryImport` chỉ ĐỌC `products`.
`/admin/units/{id}/updateEnglishName` ghi bảng `units`, không phải `products`.

---

## 2. Phân loại + đề xuất xử lý

| Nhóm | Đường | Xử lý đề xuất | Lý do |
|---|---|---|---|
| **CHẶN HẲN** | `products`: create, store, edit, copy, update, delete, bulkDelete, restore, importExcel, importExcelNew, importExcelInstallWork, importExcelAttribute, importExcelZitecProduct, deleteFile, update-products, start-update-products | middleware chặn + ẩn nút/menu | QĐ §10/§13. HRM đã có tạo/sửa/xoá/khoá (2-C) |
| **CHẶN HẲN** | `products/change`, `view-import` + 2 POST, `viewImportProductExtend` + POST | chặn (hoặc gỡ route, xem câu ⭐Q6) | lệnh sửa dữ liệu một lần, không gate quyền — lỗ hổng sẵn có |
| **CHẶN HẲN** | `product_templates`: create, store, edit, copy, update, delete (+ `deleted`, chỉ đọc, tuỳ ý) | chặn + ẩn menu "Danh mục hàng hoá gốc" | 🔴 `UpdateGenerateProduct` ghi đè 29.813 hàng bằng dữ liệu cũ |
| **CHẶN HẲN** | `product2/*` ghi (create, store1, edit, update/2/3, delete, syncInfo, syncCategoryInfo) · `product-infos` ghi + `syncInfo` · `sync-products-info/*` POST | chặn + ẩn cụm menu "Đồng bộ hàng hoá"/"Hàng hoá có sẵn" | 0 dữ liệu, chưa dùng; còn để mở thì vẫn là cửa tạo hàng ngoài HRM |
| **CHẶN** (chờ ⭐Q3) | `products/storeService` (báo giá dịch vụ tạo hàng) | chặn + ẩn nút trong `createServiceProductJs` | 0 lần dùng từ 07/2023 |
| **DANH SÁCH TRẮNG (ghi)** | `updateEnglishName`, `updateHSCode` | giữ nguyên | màn mua hàng cần; chỉ 2 cột "phụ" phục vụ chứng từ nhập khẩu |
| **DANH SÁCH TRẮNG (ghi)** | `addEquipment` | giữ | không ghi `products` |
| **DANH SÁCH TRẮNG (đọc)** | 28 route ở 1.1c + `getPriceOfProducts`, `download-*` | giữ | ~150 chỗ gọi từ chứng từ |
| **GIỮ ERP tới phase giá (8/7)** | `editPrices`/`updatePrice`, `manualUpdatePrices`, `expectedPrices`, `approve*`, Phiếu tính giá, giá theo hãng, 2 cron giá | giữ | QĐ §11/§20: giá chuyển dần, chưa có màn HRM |
| **GIỮ ERP tới Phase 6** | duyệt hàng tạm `tmp_products/{id}/approve` | giữ | 18% hàng mới; HRM chưa có màn hàng tạm |
| **GIỮ** | Thuế suất / Nhóm lan thuế (E7/E8) | giữ | chỉ ghi cột thuế, nhất quán với danh mục thuế. ⚠️ HRM Thuế suất KHÔNG lan (xem 8.4) |
| **SỬA (N2)** | Hãng SX `update` | **bỏ khối `:270-275`** (cả ghi `company_id` lẫn `syncCompanyCoefficients`) + **ẩn thẻ "Hệ số giá theo công ty"** (`form.blade.php:83-140`) + bỏ validate `company_coefficients.*` (`:229-231`); khối `:186-190` ở `store` cũng bỏ cho gọn | `products.company_id` = **công ty TẠO / chủ thông tin chung** ở HRM (`ProductService.php:326-332`; 3 mức quyền §26c-bis). Ghi đè thì quyền sửa trên HRM đổi chủ âm thầm. Xoá hệ số thì mất dòng trạng thái theo công ty (status/4 ô quản trị) của HRM. Hệ số giá sẽ bỏ (tiền đề #8). HRM Phase 1 cũng đã chủ động không lan (`chuyen-danh-muc-lien-quan/design.md` QĐ8) |
| **SỬA (N3)** | Thương hiệu | gỡ 2 lời gọi `$brand->updateProducts()` (`BrandsController.php:138, 215`); giữ hàm trong model hoặc xoá | đã chết ở UI. Gỡ để không ai bật lại ô tick |

> Không đề xuất chặn **cả màn** Hãng SX/Thương hiệu ERP: Phase 1 chốt "giữ nguyên màn ERP cũ", và 3 màn con KPI/cấu hình
> nhân viên của Hãng SX chỉ có ở ERP. Chỉ gỡ phần ghi lan sang `products`. Nếu user muốn chặn ghi cả 2 màn danh mục (HRM đã có
> CRUD) thì xem ⭐Q2.

---

## 3. Cách chặn — so sánh

| Phương án | Ưu | Nhược / rủi ro chặn nhầm |
|---|---|---|
| **(1) Middleware route mới** (vd `productWriteMovedToHrm`), gắn **từng route** ở mục 2 | chính xác tới từng route; 1 file logic + 1 dòng/route; gỡ lại dễ; trả thông báo đẹp cho cả GET lẫn AJAX; không đụng model dùng chung | phải liệt kê đủ route. **Không bắt** được ghi ngoài HTTP (job, cron, model). Gắn nhầm vào cả group `products` là vỡ ~150 chỗ gọi `getData`/`getPriceOfProducts` |
| (2) Gỡ quyền `Thêm/Sửa/Xóa/Khôi phục hàng hóa` khỏi role | không sửa code | ❌ quyền dùng chung với `product_templates`, `product2`, `product-infos`. `Sửa hàng hóa` còn gate route ĐỌC `products.deleted`; `Thêm báo giá` gate `addEquipment`. Super admin/role mới cấp lại là mở. Không có thông báo "đã chuyển". **Không đề xuất** |
| (3) Chặn ở model: `Product::saving/deleting` ném lỗi trừ khi có cờ cho phép | bắt mọi đường Eloquent kể cả job | ❌ **không bắt** query builder (`Brand::updateProducts`, 2 job thuế, `DB::table`), cũng không bắt `Product::where()->update()`. Phải bật cờ cho mọi luồng hợp lệ (mua hàng, tính giá, duyệt giá, hàng tạm, cron, `CreateTemplateProductMissing`), sót một chỗ là **vỡ luồng đang chạy giữa giao dịch**. 14 bảng con phải gắn riêng. `Product::boot` (`app/Product.php:165`) + `BaseModel::boot` dùng chung |
| (3') Observer **chỉ ghi log** (không chặn) trên `Product`/`ProductUnit`/`ProductUnitPrice`/`ProductCompanyCoefficient` | phát hiện đường sót sau go-live mà không vỡ gì | thêm 1 file + đăng ký ở provider; log nhiều ở cron giá |
| (4) Ẩn menu/nút (Blade + cột `action` DataTables) | trải nghiệm sạch | chỉ là bề mặt — gõ URL vẫn vào được ⇒ chỉ dùng **kèm (1)** |

**Đề xuất: (1) + (4), cộng (3') nếu user đồng ý** (⭐Q5). Phác thảo (1):

- File mới `app/Http/Middleware/ProductWriteMovedToHrm.php`, alias ở `app/Http/Kernel.php:69-76`.
- GET (mở trang): trả view mới `errors/moved_to_hrm.blade.php` (kế thừa `layouts.app`). Trang có câu "Chức năng quản lý hàng hoá
  đã chuyển sang HRM" + nút mở `config('app.hrm_url_FE')` (`config/app.php:127`) + đường dẫn:
  - `create`/`copy` → `/master-data/products/create`
  - `{id}/edit` → `/master-data/products/{id}/edit` (trang có sẵn: `hrm-client/pages/master-data/products/_id/edit.vue`)
  - còn lại → `/master-data/products/company`
  - ⚠️ Blade gotcha: không dùng `@json()` với closure (memory `erp-blade-json-directive-gotcha`); dựng URL ở middleware rồi truyền biến.
- POST/PUT/AJAX: trả JSON theo khuôn `CheckPermission` (`{success:false, message:'Chức năng đã chuyển sang HRM…', redirect_url}`),
  HTTP **403**. Hệ quả: màn ERP nào đang mở sẵn (tab cũ) bấm Lưu sẽ rơi vào nhánh `error` → hiện "Đã có lỗi xảy ra". Chấp nhận
  được vì nút đã ẩn. Muốn hiện đúng câu thì trả 200 + `success:false` (⭐Q4).
- Đường vào tiềm ẩn: `route('productDelete')` hiện sinh ra **`/product2/{id}/delete`** vì tên route bị khai trùng ở `:580` và
  `:674` (Laravel lấy bản khai sau). Nên phải chặn **cả hai** route.
- Ẩn (4): menu `topmenubar.blade.php:19` (hàng gốc), `:20` (danh mục hàng hoá — giữ nếu cho xem, ⭐Q1), `:22` (cập nhật nhanh),
  `:49`, `:64-68` (hàng có sẵn/đồng bộ). Nút `products/list.blade.php:17-23` (Xoá hàng loạt, Thêm mới, 3 Import).
  `products/show.blade.php:31-35` (Sửa, Xoá, Sao chép). Cột action `ProductsController.php:327-345` và `:480-495`
  (`searchDataProductApprover`), giữ "Lịch sử" + "Xem sản phẩm tạm". Tương tự `product_templates/list|show` +
  `ProductTemplatesController` (cột action). Menu **không bọc `@can`**, nên mọi người đều thấy link.
  `layouts/sidebar.blade.php` và `topmenubar_old.blade.php` **không được include** ở đâu ⇒ không cần sửa.

---

## 4. Quyền ERP (bảng `permissions`, guard **`web`**)

| id | Quyền | Số role | Sau 2-D |
|---|---|---|---|
| 100034 | Thêm hàng hóa | 25 | chỉ còn gate route đã chặn (`products`, `product_templates`, `product2`, `product-infos`) ⇒ **vô hiệu**, giữ bản ghi |
| 100035 | Sửa hàng hóa | 26 | còn gate route ĐỌC `products.deleted` (:605), `product_templates.deleted` ⇒ **giữ** |
| 100036 | Xóa hàng hóa | 10 | vô hiệu, giữ bản ghi |
| 101002 | Khôi phục hàng hóa | 2 | vô hiệu, giữ bản ghi |
| 100033 | Xem hàng hóa | — | **giữ** (route đọc) |
| 100063 / 100127 / 100983 | Cập nhật nhanh giá / Quản lý giá / Duyệt giá hàng hoá | 11 / — / — | giữ (luồng giá) |
| 100071 / 100118 | Tổng hợp đặt hàng / Mua hàng | — | giữ (danh sách trắng) |
| 100010-11, 100014-15 | Thêm/Sửa hãng SX, Thương hiệu | — | giữ (màn còn sống, chỉ bỏ ghi lan) |

Đề xuất: **không xoá, không đổi tên** quyền. `CheckPermission` so khớp **chuỗi tên** (`can($permission)`), đổi tên là vỡ các
route còn dùng. Gỡ 3 quyền vô hiệu khỏi role thì để sau khi chạy ổn định (⭐Q7). HRM dùng guard `api`, quyền riêng
1652–1655 (2-C), không dính bộ `web`.

---

## 5. Danh sách file ERP dự kiến đụng

| File | Việc |
|---|---|
| `app/Http/Middleware/ProductWriteMovedToHrm.php` *(mới)* | middleware chặn |
| `app/Http/Kernel.php` (~:76) | đăng ký alias |
| `resources/views/errors/moved_to_hrm.blade.php` *(mới)* | trang thông báo + link HRM |
| `routes/web.php` | gắn middleware cho 16 route `products` + 6 route sửa dữ liệu một lần (hoặc gỡ, ⭐Q6) + 6–7 route `product_templates` + 10–12 route `product2` + 6 route `product-infos`/đồng bộ (+ `storeService` nếu ⭐Q3) |
| `resources/views/layouts/topmenubar.blade.php` | ẩn ~8 mục menu |
| `resources/views/products/list.blade.php`, `products/show.blade.php` | ẩn nút ghi |
| `app/Http/Controllers/ProductsController.php` (:327-345, :480-495) | bỏ link Sửa/Xoá/Sao chép/Khôi phục ở cột action |
| `resources/views/product_templates/list.blade.php`, `show.blade.php`, `ProductTemplatesController.php` (cột action) | như trên |
| `app/Http/Controllers/Sale/ManufacturesController.php` (:186-190, :229-231, :270-275) | **N2** |
| `resources/views/catalogs/manufactures/form.blade.php` (:83-140) + `partials/classes/sale/Manufacture.blade.php:92` | ẩn thẻ hệ số, bỏ gửi `company_coefficients` |
| `app/Http/Controllers/Sale/BrandsController.php` (:138, :215) | **N3** |
| *(tuỳ ⭐Q3)* `resources/views/partials/serviceProduct/createServiceProductJs.blade.php` | ẩn nút tạo hàng dịch vụ |
| *(tuỳ ⭐Q5)* `app/Observers/ProductWriteAuditObserver.php` *(mới)* + `AppServiceProvider` | log ghi ngoài danh sách trắng |

Không chạy migration, không seeder. Repo/nhánh ERP để chốt ở ⭐Q8.

---

## 6. Cách kiểm

ERP **không có bộ test dùng được**: `tests/` chỉ có 2 test đơn vị thuần (`TmpProductRetailCoefficientTest`,
`CustomerHandoverDocumentSyncTest`), `phpunit.xml:31-32` dùng `sqlite :memory:`, không có thư mục e2e. Skill `playwright-setup`
có mục riêng cho AngularJS/Blade (§"Nếu project dùng AngularJS/Blade").

1. **PHPUnit kiểm route** (không cần DB): duyệt `Route::getRoutes()`, khẳng định đúng danh sách route bị chặn có middleware mới
   và đúng danh sách trắng (getData, getPriceOfProducts, updateEnglishName, updateHSCode, addEquipment, updatePrice,
   checkNeedVat…) **không** có middleware đó. Đây là bài test chống chặn nhầm. ⚠️ Trước mọi lệnh `php artisan`/phpunit phải xác
   nhận DB thật (memory `erp-local-config-cache-tro-production`). Hiện `bootstrap/cache/` chưa có `config.php`, và `.env` local
   ERP trỏ `erp2326`, KHÔNG phải `hrm_erp`.
2. **Playwright MCP trên ERP local** (bắt buộc theo CLAUDE.md gốc vì có đụng giao diện), đo bằng DOM:
   - menu: đếm link "Danh mục hàng hoá gốc"/"Cập nhật nhanh hàng hoá" = 0;
   - list/show: số nút Thêm mới/Import/Sửa/Xoá = 0;
   - gõ thẳng URL `/admin/products/create`, `/{id}/edit`, `/product_templates/{id}/edit`: trang thông báo có link HRM đúng `{id}`;
   - POST `/{id}/update` bằng `fetch`: 403 + JSON đúng câu;
   - **danh sách trắng còn sống**: popup chọn hàng ở 1 màn bán + 1 màn kho (`getData` 200), sửa tên TA ở `purchase_invoice/create`,
     HS code ở `buy_requests`, Cập nhật giá nhanh `updatePrice`, duyệt 1 hàng tạm;
   - ca **không quyền** (memory `always-test-permission-cases`): tài khoản không có `Tổng hợp đặt hàng` vẫn bị 403 ở `updateEnglishName`.
3. **N2 bằng SQL** (so **từng dòng**, không dùng `MD5(GROUP_CONCAT)` — memory `group-concat-cat-checksum-gia`): chụp
   `products(id, company_id, updated_at)` + `product_company_coefficients` của 1 hãng nhiều hàng, rồi Lưu sửa hãng (kể cả đổi công
   ty). Đạt khi 0 dòng đổi.
4. **Chống ghi im lặng**: trước/sau 1 ngày chạy thử, đếm `products.updated_at > mốc` theo `updated_by`. Mọi dòng phải đến từ danh
   sách trắng/luồng giá/HRM. Nếu bật (3') thì đọc log.

---

## 7. Việc ngoài luồng phát hiện thêm (đề xuất bổ sung N28–N33 vào `2c-ghi/chot.md`, KHÔNG vá trong 2-D trừ khi user muốn)

| # | Việc | File:dòng |
|---|---|---|
| N28 | `GET products/change` **không gate quyền**, ai đăng nhập cũng chạy được ⇒ đổi hàng loạt `product_type`/`product_cate`. 3 route `view-import*` cũng không gate (import sửa VAT / tạo hàng) | `web.php:627, 632-637`; `ProductsController.php:3762, 3796, 3824, 3852` |
| N29 | 4 route duyệt giá `approve*Submit` không có `checkPermission` | `web.php:597-600` |
| N30 | `manualUpdatePrices` là **GET nhưng ghi giá** (trình duyệt prefetch/crawler có thể kích hoạt) | `web.php:617`, `ProductsController.php:2242` |
| N31 | Tên route `productDelete` khai trùng ⇒ nút Xoá ở màn hàng hoá chính đang trỏ `/product2/{id}/delete` | `web.php:580, 674` |
| N32 | HRM Thuế suất (`TaxRateService`) **không lan** giá trị thuế xuống `products`/`groups` như ERP (`TaxRatesController:170-215`); sửa thuế ở HRM thì `products.vat_percent` lệch | `hrm-api/Modules/MasterData/Services/ProductCatalog/TaxRateService.php` |
| N33 | Hàng HRM tạo **không có hàng gốc** (`product_template_id` NULL, vì job chỉ bắn từ ERP `createRecord`). Hàng ERP cũ có hàng gốc **lỗi thời** sau khi sửa ở HRM. Nếu sau này mở lại màn hàng gốc thì phải đồng bộ (gắn với R5/N6 CRM) | `app/Product.php:7211` |
| — | Dữ liệu: **1.290** hàng status 1 có công ty Thương hiệu ≠ công ty Hãng SX. Trước đây ai Lưu sau thì thắng; sau 2-D thì `products.company_id` đứng yên | SELECT 09/10 |

---

## 8. Đính chính `2c-ghi/erp-ghi-hang-hoa.md`

- E1 (Hãng SX): "xoá sạch `product_company_coefficients`" **chỉ xảy ra khi bảng hệ số trên form có ≥1 dòng**. Phần ghi đè
  `company_id` thì xảy ra **mỗi lần Lưu**, vô điều kiện. Lúc **tạo** hãng thì không ảnh hưởng (hãng mới chưa có hàng).
- E2 (Thương hiệu): ô tick đã bị comment, store không ảnh hưởng ⇒ **thực tế không chạy**.
- E12 (hàng gốc): không phải "nếu màn hàng gốc không bị chặn" — mà là **65% hàng hoá có hàng gốc 1–1**, nên mọi lần sửa hàng gốc
  đều ghi đè hàng thật.
- R3 danh sách trắng: thêm `addEquipment`, `checkNeedVat`, `getListDataForAccountingInventory` (POST chỉ đọc), `barcode`
  (ghi `warehouse_import_lots`, không ghi `products`). `searchProductsByKeyword` chỉ có 1 chỗ gọi.

---

## 9. Câu hỏi cho user (chỉ nghiệp vụ chưa chốt)

| # | Câu | Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **Q1** | Màn **Danh mục hàng hoá ERP** (list + xem chi tiết + lịch sử + xuất Excel) sau 2-D: **giữ chỉ-xem**, hay **đổi menu sang HRM**? | ⭐ **Giữ chỉ-xem** (ẩn mọi nút ghi), menu thêm link "Quản lý trên HRM" | Giữ: người dùng ERP tra cứu tại chỗ, tab "Lịch sử" ERP vẫn xem được 319k dòng cũ, và còn cần cho nút `editPrices`/import công khoán (luồng giá). Đổi hẳn: gọn hơn nhưng mất màn lịch sử cũ + phải chuyển "Hàng chưa có công khoán"/"Cập nhật giá nhanh" sang chỗ khác |
| **Q2** | Hãng SX / Thương hiệu ERP: chỉ **bỏ phần ghi lan sang `products`** (N2/N3), hay **chặn luôn thêm/sửa 2 danh mục này ở ERP** (HRM Phase 1 đã có CRUD)? | ⭐ **Chỉ bỏ ghi lan** | Chỉ bỏ: an toàn, 2 nơi cùng sửa danh mục như hiện nay (Phase 1 đã chấp nhận). Chặn luôn: 1 nguồn sửa duy nhất, nhưng 3 màn con KPI/Cấu hình NV của Hãng SX (chỉ có ở ERP) phải giữ route riêng, và Phase 1 chưa nghiệm thu |
| **Q3** | Nút "tạo hàng hoá dịch vụ" trong **Báo giá dịch vụ** (`storeService`, 0 lần dùng từ 07/2023): chặn? | ⭐ **Chặn + ẩn nút** | Chặn: hết đường tạo hàng ngoài HRM. Để lại: ERP vẫn sinh hàng có `group_id` mới, `product_type` theo enum cũ, không có dòng công ty — lệch luật 2-C |
| **Q4** | Bấm Lưu ở tab ERP cũ (nút đã ẩn): trả **403** (hiện "Đã có lỗi xảy ra") hay **200 + câu "đã chuyển sang HRM"**? | ⭐ **403** | 403: đúng ngữ nghĩa, log rõ; câu báo chung chung. 200: người dùng đọc được đúng lý do, nhưng log/giám sát coi là thành công |
| **Q5** | Có thêm **observer chỉ ghi log** mọi lần ghi `products` + 3 bảng giá/công ty ngoài danh sách trắng trong 2–4 tuần đầu? | ⭐ **Có** | Có: bắt được đường sót (job, import, màn lạ) mà không vỡ gì; tốn 1 file + log ở cron giá. Không: dựa vào rà tĩnh ở tài liệu này |
| **Q6** | 6 route sửa dữ liệu một lần (`change`, `view-import*`, `importExcelZitecProduct`): **chặn bằng middleware** hay **comment/gỡ route** (như bản `product_templates` đã làm)? | ⭐ **Gỡ route** | Gỡ: hết lỗ hổng không gate quyền, code gọn. Chặn: giữ được dấu vết, mở lại dễ |
| **Q7** | Có **gỡ quyền** `Thêm/Xóa/Khôi phục hàng hóa` khỏi 25/10/2 role sau khi chạy ổn định không? | ⭐ **Để nguyên** (đánh dấu vô hiệu trong tài liệu) | Gỡ: màn phân quyền ERP gọn. Nhưng nếu phải mở lại (rollback) thì phải cấp lại từng role |
| **Q8** | Code 2-D phía ERP đặt ở **nhánh nào**: tạo nhánh mới từ ERP **`gop_db`** (lệch `develop_01` 359/222 commit), hay `develop_01`? DB kiểm thử của ERP local là `erp2326` hay trỏ sang `hrm_erp` (DB gộp)? | ⭐ **nhánh mới từ ERP `gop_db`**, kiểm trên `hrm_erp` | Từ `gop_db`: khớp nhánh sẽ lên production, kiểm được cùng dữ liệu HRM ghi. Từ `develop_01`: số dòng khớp tài liệu này nhưng phải port lại sang `gop_db`; kiểm trên `erp2326` thì không có hàng HRM tạo để thử |
| **Q9** | "**Cập nhật nhanh hàng hoá**" (sửa hàng loạt tên/tên TA/thuế/HS/tồn min-max — `SO-CHOT` §5 #11 chưa chốt): chặn ở 2-D và **HRM có cần màn tương đương** không? | ⭐ **Chặn**, ghi việc "màn sửa nhanh HRM" vào backlog | Chặn mà HRM chưa có ⇒ người dùng phải sửa từng mã trên HRM tới khi có màn. Không chặn ⇒ ERP vẫn ghi lớp thông tin chung, vượt qua luật 3 mức quyền HRM |
