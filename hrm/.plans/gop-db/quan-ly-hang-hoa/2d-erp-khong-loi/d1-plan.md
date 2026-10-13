# Đợt 2-D1 — ERP không lỗi (chặn ghi hàng hoá ERP + ERP đọc hàng HRM không lỗi + mẫu tem theo Loại SP) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (hoặc executing-plans). Bước dùng checkbox `- [ ]`.
> 09/10/2026 · @namdangit · CHỈ là tài liệu — chưa đụng source. Code chỉ bắt đầu khi user trả lời **"làm"** cho mục 0 (CLAUDE.md root), mỗi PHA xin riêng.

**Goal:** Sau 2-D1, ERP (1) **không còn đường ghi thông tin hàng hoá** ngoài danh sách trắng (route ghi bị chặn theo từng route, menu/nút ẩn, 7 route sửa-1-lần bị gỡ, ghi lan N2/N3 bị bỏ), (2) **đọc hàng HRM tạo không lỗi** (M1–M7 null-safe, N9 popup thấy hàng HRM, N8 popup ẩn hàng công ty đã khoá), (3) in tem theo **mẫu của Loại SP** (cột mới `product_types.barcode_template_type` ở HRM).

**Spec / luật (thứ tự ưu tiên):** `ton.md` cột "Trả lời" + "Phạm vi chốt" (2-D1) + bổ sung 09/10 (QC-7 / N36: **khoá "Cập nhật giá theo hãng"** ở ERP ngay trong 2-D1) > `../2c-ghi/chot.md` (N1–N36, G1–G11) > `SO-CHOT-VA-TON.md` > `khao-sat-a-chan-ghi.md` > `khao-sat-b-doc.md` > `khao-sat-c-gia.md` (chỉ phần L7/L8, hệ số).

**Mã nguồn đã kiểm (09/10):** ERP `origin/gop_db` @ `04b61efc24` (03/10/2026; `git fetch --dry-run` 09/10 không thấy gop_db đổi), bản `git archive` ở scratchpad. **Mọi số dòng ERP trong file này là của gop_db** (khảo sát A lệch −8 ở nhóm `products`; khảo sát B/C đã theo gop_db). ERP thật là **Laravel ^6.2, PHP 7.4.33** (`composer.json`; CLAUDE.md ERP ghi "Laravel 8" là sai) ⇒ không `?->`, không `match`, không named args. HRM: worktree `wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`, nhánh `feat/chuyen-doi-hang-hoa`.

---

## 0. Phạm vi xin phép *(chi tiết ở mục 9 — đọc mục 9 trước khi cho "làm")*

3 pha, xin "làm" riêng từng pha:

| Pha | Repo · nhánh | Nội dung |
|---|---|---|
| **P1 — HRM mẫu tem** | `hrm-api` + `hrm-client` · nhánh con `feat/p2d1-mau-tem` từ `feat/chuyen-doi-hang-hoa` (worktree) | migration `product_types.barcode_template_type` + validate BE + ô chọn ở form Loại SP (làm TRƯỚC vì ERP P2 đọc cột này) |
| **P2 — ERP chặn ghi + đọc không lỗi** | ERP `TanPhatDev` · nhánh mới `feat/2d1-erp-khong-loi` từ `origin/gop_db` (worktree riêng, KHÔNG checkout repo chính đang ở `develop_01`) | middleware + trang báo + route + menu/nút + N2/N3 + observer log + M1–M7 + N8/N9 + tem theo Loại SP + khoá Cập nhật giá theo hãng |
| **P3 — Kiểm ERP trên DB `hrm_erp`** | ERP worktree trỏ `.env` sang `hrm_erp` (hỏi riêng) + tạo dữ liệu kiểm (hỏi riêng) | Playwright MCP đo DOM K1–K14, SQL N2 |

---

## 1. Global Constraints

- **Chặn THEO TỪNG ROUTE**, không chặn theo tiền tố `products/*`, không chặn theo động từ HTTP (có POST chỉ đọc `getPriceOfProducts`/`checkNeedVat`/`getListDataForAccountingInventory`, có GET ghi `change`/`importExcelZitecProduct`/`manualUpdatePrices`). Không chặn ở model (khảo sát A §3).
- Middleware mới `productMovedToHrm` (alias) — **GET (không AJAX)** ⇒ trang `errors/moved_to_hrm.blade.php` HTTP 403 + link `config('app.hrm_url_FE')`; **POST/PUT/AJAX/`expectsJson`** ⇒ **403** JSON `{success:false, message:'Chức năng đã chuyển sang HRM…', redirect_url}` (Q6). Middleware đứng **trước** `checkPermission`/`checkDueConfigs` để người không quyền cũng nhận đúng câu (không lộ gì vì không ghi).
- Middleware chỉ có tham số "đích" (vd `productMovedToHrm:product-edit`) để dựng link HRM; dựng URL **trong middleware**, truyền biến sang Blade — KHÔNG `@json()` closure (memory *erp-blade-json-directive-gotcha*).
- **Danh sách trắng không bao giờ gắn middleware**: `updateEnglishName`, `updateHSCode`, `addEquipment`, mọi route ĐỌC, **toàn bộ luồng GIÁ** (thuộc 2-D2: `editPrices`, `getProductsAndPrices`, `updatePrice`, `expectedPrices`, `manualUpdatePrices`, `priceUpdating`, `approve*`, Phiếu tính giá, cron, `price_logs`), **duyệt hàng tạm** (`tmp_products/*`, Phase 6). **Ngoại lệ duy nhất của luồng giá bị chặn ở 2-D1: tạo/lưu phiếu "Cập nhật giá theo hãng"** (QC-7 đổi 09/10 / N36) — giữ màn xem danh sách/chi tiết phiếu cũ.
- **Không gỡ quyền ERP** (Q8), không đổi tên quyền (CheckPermission so chuỗi tên). Không migration ERP, không seeder ERP.
- **7 dòng route sửa-dữ-liệu-một-lần bị GỠ** (Q5 — xoá dòng route, giữ method controller chết để diff nhỏ; 2 view `view_import*` chỉ render từ chính route bị gỡ nên không vỡ).
- `productDelete` khai trùng (`web.php:572` và `:666`) ⇒ cả 2 route đều gắn middleware (N31). Không đổi tên route (ngoài phạm vi).
- Null-safe bằng `??` / toán tử 3 ngôi (PHP 7.4). N9: `whereNull OR != 'service_product'` kèm tiền tố `products.`.
- Observer **chỉ ghi log** (Q7), không chặn, không ném lỗi; lỗi trong observer bị nuốt (try/catch) để không bao giờ làm vỡ giao dịch.
- Mẫu tem: ERP đọc `product_types.barcode_template_type` qua `products.product_type_id`; **chưa có giá trị ⇒ mẫu 1**. **Chỉ theo Loại SP, KHÔNG rơi về `groups`** (T1 chốt 09/10 — user gắn Loại SP cho dữ liệu cũ xong rồi mới cập nhật product) — xem mục 5.
- Việc ngoài luồng phát hiện thêm ⇒ ghi `chot.md` (N37+), KHÔNG vá trong 2-D1.
- Kiểm FE bắt buộc Playwright MCP đo DOM (CLAUDE.md root). Không tự chạy e2e (memory *khong-tu-chay-e2e-moi-task*), `--workers=1` khi được chạy.
- ⚠️ ERP local: trước MỌI lệnh `php artisan`/phpunit phải `ls bootstrap/cache/config.php` (không được tồn tại) + `php artisan config:clear` (memory *erp-local-config-cache-tro-production*). `.env` repo chính trỏ `erp2326`.

---

## 2. Danh sách route ERP (gop_db `routes/web.php`) — CHẶN / GỠ / TRẮNG

Ký hiệu: **MW** = gắn middleware `productMovedToHrm` · **GỠ** = xoá dòng route · **TRẮNG** = không đụng (test khẳng định KHÔNG có MW).

### 2.1 Nhóm `admin/products/*` (`web.php:563-635`)

| Dòng | Method · URI | Tên route | Controller `ProductsController` :dòng | Xử lý | Đích link HRM |
|---|---|---|---|---|---|
| 564 | GET `create` | `productCreate` | `create` :723 | **MW** | `/master-data/products/create` |
| 565 | POST `/` | `productStore` | `store` :909 | **MW** | — |
| 566 | POST `storeService` | `productStoreService` | `storeService` :743 | **MW** (Q4) | — |
| 568 | GET `{id}/edit` | `productEdit` | `edit` :1020 | **MW** | `/master-data/products/{id}/edit` |
| 570 | GET `{id}/copy` | `product.copy` | `copy` :1084 | **MW** | `/master-data/products/create` |
| 571 | POST `{id}/update` | `productUpdate` | `update` :1117 | **MW** | — |
| 572 | GET `{id}/delete` | `productDelete` (trùng tên, bị :666 đè) | `delete` :1999 | **MW** (N31) | `/master-data/products/{id}` |
| 573 | POST `bulkDelete` | `products.bulkDelete` | `bulkDelete` :4625 | **MW** | — |
| 582 | POST `importExcel` | `products.importExcel` | :2033 | **MW** | — |
| 583 | POST `importExcelNew` | `products.importExcelNew` | :2079 | **MW** | — |
| 584 | POST `importExcelInstallWork` | `products.importExcelInstallWork` | :2163 | **MW** ("Import công lắp đặt", QC-8) | — |
| 585 | POST `importExcelAttribute` | `products.importExcelAttribute` | :2200 | **MW** (gọi từ `products/list:801` + `catalogs/brands/list:95`) | — |
| 598 | GET `{id}/restore` | `products.restore` | `restore` :2020 | **MW** | `/master-data/products/{id}` |
| 613 | POST `{id}/deleteFile` | `product.deleteFile` | :3659 | **MW** | — |
| 620 | GET `update-products` | `product.updateListProducts` | :3878 | **MW** (Q3) | `/master-data/products/company` |
| 622 | POST `start-update-products` | `product.startUpdateListProducts` | :3884 | **MW** (Q3) | — |
| 619 | GET `change` | `product.change` | :3762 | **GỠ** (Q5, N28) | — |
| 624 | GET `view-import` | `product.viewImport` | :3787 | **GỠ** | — |
| 625 | POST `view-import/import-vat-10` | `product.updateVat10percent` | :3796 | **GỠ** | — |
| 626 | POST `view-import/import-beta-product` | `product.updateVatBetaProduct` | :3824 | **GỠ** | — |
| 628 | GET `viewImportProductExtend` | `product.viewImportProductExtend` | :3847 | **GỠ** | — |
| 629 | POST `view-import-product-extend` | `product.importProductExtend` | :3852 | **GỠ** | — |
| 632 | GET `importExcelZitecProduct` | `products.importExcelZitecProduct` | :2125 | **GỠ** | — |

⇒ **16 MW + 7 GỠ** (khảo sát A ghi "6 route sửa một lần" = `change` + 3 `view-import*` + 2 `…ProductExtend`; cộng `importExcelZitecProduct` = **7 dòng**). Đã soát: tên route của 7 dòng gỡ chỉ được tham chiếu ở `products/view_import*.blade.php` + `product_templates/view_import*.blade.php` (4 view chỉ render từ chính các route bị gỡ / đã comment) ⇒ không có `route()` nào khác vỡ.

**TRẮNG trong nhóm** (34 dòng): `:567` addEquipment (POST, ghi bảng báo giá) · `:569` show · `:574` history · `:575` index · `:576` barcode · `:577` searchData · `:578` importLogLink · `:579-581` export · **giá (2-D2):** `:586` editPrices · `:587` approvePrices · `:588` approvePricesSearchData · `:589-592` approve*Submit · `:593` approveExportExcel · `:594` priceUpdating · `:595` getProductsAndPrices · `:596` updatePrice · `:608` expectedPrices · `:609` manualUpdatePrices · đọc: `:597` deleted · `:599` getData · `:600` getDataForPriceAsking · `:601` getDataForInventory · `:602` getDataForAccountingInventory · `:603` POST getListDataForAccountingInventory · **`:604` POST updateEnglishName** · **`:605` POST updateHSCode** · `:606` getDataForJoin · `:607` getRecipe · `:610` getAccessories · `:611` validateLanguage · `:612` longStock · `:614` getListForReport · `:615` POST checkNeedVat · `:616` searchProductsByKeyword · `:617` getDropdownData · `:630` getCustomerPrepickByEmployee · `:633` exportExcelNorm (giữ, link sang menu Kế toán) · `:634` exportProduct. Nhóm đầu file `:46` POST getPriceOfProducts · `:47` download-file · `:48` download-export-file · `:49` download-stock-zip.

### 2.2 Hàng gốc `product_templates/*` (`web.php:498-521`)

| Dòng | Route | Xử lý |
|---|---|---|
| 499 GET `create` `productTemCreate` · 500 POST `/` `productTemStore` · 501 GET `{id}/edit` `productTemEdit` · 503 GET `{id}/copy` `productTem.copy` · 504 POST `{id}/update` `productTemUpdate` (🔴 `UpdateGenerateProduct`) · 505 GET `{id}/delete` `productTemDelete` | **MW** ×6 (đích HRM `/master-data/products/company`) |
| 502 show · 506 history · 507 index · 509 searchData · 510 attributeValue/suggestions · 521 deleted | TRẮNG (menu bị ẩn, URL còn xem được) |

### 2.3 Product2 / Hàng có sẵn / Đồng bộ

| Dòng | Route | Xử lý |
|---|---|---|
| `product-infos` 642 GET create · 643 POST `/` · 644 GET edit · 646 POST update · 647 GET delete · **653 GET `{id}/syncInfo`** (không gate quyền) | **MW** ×6 |
| `product-infos` 645 show · 648 index · 649 searchData · 650 searchData2 · 651 getData | TRẮNG |
| `product2` 659 GET create · 660 POST store1 · 661 GET edit · 663/664/665 POST update/2/3 · **666 GET delete (`productDelete` — bản thắng)** · 670 POST syncInfo · 671 POST syncCategoryInfo | **MW** ×9 |
| `product2` 662 show · 667 index · 668 searchData | TRẮNG |
| `sync-category-info` 677 POST sync · `sync-products-info` 682 POST syncInfo · 683 POST syncCategoryInfo | **MW** ×3 |
| `sync-category-info` 675, 676 · `sync-products-info` 681 | TRẮNG |

### 2.4 Hãng SX `manufactures/*` (`web.php:161-189`) + Thương hiệu `brands/*` (`:228-242`) — Q2

| Dòng | Route | Xử lý | Đích HRM |
|---|---|---|---|
| 164 GET create `manufacCreate` · 165 POST `/` `manufacStore` · 166 POST `fast` `manufacFastStore` · 167 GET edit `manufacEdit` · 168 POST update `manufacUpdate` · 169 GET delete `manufacDelete` · 174 POST importExcel `manufactures.importExcel` | **MW** ×7 | `/master-data/manufacturers` |
| 162 index · 163 getAll · 170 searchData · 171-173 export · 175 getBuyer · 176 getDeputy · **178-180 kpiOrder (+searchData, POST update)** · **182-184 kpiSale** · **186-188 configEmployee** | TRẮNG (3 màn con KPI XNK / KPI PTKD / Nhân viên hãng — ghi `manufacture_kpi_orders/kpi_sales/config_employees`, không ghi `manufactures`/`products`) | — |
| 231 GET create `brandCreate` · 232 POST `/` `brandStore` · 233 POST `fast` `brandFastStore` · 234 GET edit `brandEdit` · 235 PUT `{id}` `brandUpdate` · 236 GET `delete/{id}` `brandDelete` · 241 POST importExcel `brands.importExcel` | **MW** ×7 | `/master-data/brands` |
| 229 index · 230 getAll · 237 searchData · 238-240 export | TRẮNG | — |

- `pi-manufactures/*` (:192-207), `pi-brands/*` (:245-258) — danh mục của "Hàng hoá có sẵn" (0 dữ liệu, chỉ ghi `product_infos`), **không thuộc** chốt Q2 ⇒ không đụng; menu giữ nguyên (T4).
- Đã soát `manufacFastStore`/`brandFastStore`: modal thêm nhanh `partials/sale/createManufactureModal|createBrandModal` chỉ được include ở form hàng hoá/hàng gốc/product2/product-infos (bị chặn) và `quotations/form.blade.php:722,724` (include nhưng không có nút mở). Nút "+" ở `sale/tmp_products/form.blade.php:1169,1211` (hàng tạm) trỏ `#createBrand/#createManufacture` nhưng `tmp_products/edit.blade.php` **không include** modal ⇒ nút đã chết sẵn từ trước — Playwright đo xác nhận (K14-g).

### 2.5 Cập nhật giá theo hãng `manufacture_expect_prices/*` (`web.php:3653-3658`) — bổ sung 09/10 (QC-7 / N36)

| Dòng | Route | Xử lý |
|---|---|---|
| 3655 GET `create` `manufactureExpectPrice.create` | **MW** (đích: trang báo "Chức năng Cập nhật giá theo hãng đã ngừng sử dụng" — KHÔNG link HRM vì không port) |
| 3656 POST `/` `manufactureExpectPrice.store` (`ManufactureExpectPriceController@store` :71 → `ManufactureExpectPrice::updateProducts`) | **MW** 403 JSON |
| 3654 index · 3657 searchData · 3658 `{id}/show` | TRẮNG (xem 87 phiếu cũ) |

Nhóm có middleware `checkPermission:Cập nhật nhanh giá hàng hóa` ở cấp group ⇒ MW gắn ở từng route vẫn chạy SAU middleware group — chấp nhận (người không quyền nhận `not_found` như cũ; chỉ người có quyền thấy trang báo). Ghi rõ trong test.

### 2.6 Tổng

| | Số dòng route |
|---|---|
| **MW (chặn)** | products 16 · product_templates 6 · product-infos 6 · product2 9 · sync 3 · manufactures 7 · brands 7 · manufacture_expect_prices 2 = **56** |
| **GỠ** | **7** |
| **TRẮNG test khẳng định** | toàn bộ route còn lại của 9 nhóm trên (~70) + `tmp_products/*` `:688-699` + `PriceCalculate*`, `price_logs` (giá 2-D2) |

---

## 3. Menu / nút ERP (ẩn bề mặt — luôn kèm MW)

| File gop_db :dòng | Hiện tại | Sau 2-D1 |
|---|---|---|
| `layouts/topmenubar.blade.php:19` | Danh mục hàng hóa gốc | **xoá dòng** |
| `:20` | Danh mục hàng hóa → `route('proList')` | **đổi** thành `<a href="{{ $hrmProductUrl }}" target="_blank">Danh mục hàng hóa (HRM)</a>` — URL dựng sẵn (`config('app.hrm_url_FE').'/master-data/products/company'`), không `@json` (Q1) |
| `:22` | Cập nhật nhanh hàng hóa | **xoá dòng** (Q3) |
| `:46-60` cột "Hàng hóa có sẵn" (`:49` + 9 danh mục `pi-*`) | | **giữ nguyên cả cột** (T4 chốt: giữ menu) |
| `:61-70` cột "Đồng bộ hàng hoá" (`:64-68`) | | **xoá cả cột** |
| `:29`, `:30` Thương hiệu / Hãng SX | | **giữ** (vào list xem + 3 màn con KPI) |
| `:945` (Kế toán → Giá bán) Cập nhật giá theo hãng | | **giữ** (vào list xem phiếu cũ) |
| `:942-948` Kế toán → Giá bán | | **thêm** dòng "Hàng chưa có công khoán" → `route('products.exportExcelNorm')` (QC-8) ngay sau `:944` |
| `products/list.blade.php:47-50, :53` | Xóa sản phẩm · Thêm mới · Import Excel · Import công lắp đặt · Import thuộc tính | **xoá 5 nút** + 3 modal import + JS gọi `importExcelNew/InstallWork/Attribute` (:758, :801, :844) và bulk-delete (:715-740) + ô tick chọn hàng loạt nếu chỉ phục vụ xoá |
| `products/list.blade.php:39, :42, :51-52, :57` | Cập nhật giá · Đã xoá · Tùy chỉnh cột · Xuất Excel · Hàng chưa có công khoán | **giữ** (màn còn vào được bằng URL; giá thuộc 2-D2) |
| `products/show.blade.php:32-37` | Sửa · Xóa · Sao chép (+ Xem lịch sử) | **xoá 3 nút ghi**, giữ Xem lịch sử |
| `ProductsController.php:334-337, :340` (`searchData` cột action) và `:487-492` (`searchDataProductApprover`, không route — sửa cho đồng bộ) | Sửa / Xóa / Sao chép / Khôi phục | **bỏ 4 link**, giữ Lịch sử + Xem sản phẩm tạm |
| `product_templates/list.blade.php:47` + `ProductTemplatesController.php:285-288` | Thêm mới / Sửa / Xóa / Sao chép | **bỏ** |
| `catalogs/manufactures/list.blade.php:19-20` + `ManufacturesController.php:81-84` (cột action Sửa/Xóa) | Thêm mới · Import · Sửa · Xóa | **bỏ**; cột `config` (3 màn con, `:70-78`) **giữ** |
| `catalogs/brands/list.blade.php:21-22` + `BrandsController.php:46-48` | Thêm mới · Import · Sửa · Xóa | **bỏ** (kèm khối import thuộc tính `:95`) |
| `sale/manufacture_expect_prices/index.blade.php:18` | Tạo phiếu | **bỏ nút** |
| `partials/serviceProduct/createServiceProductForm.blade.php` (modal `#addNewServiceProduct`) + nút `sale/service_quotations/form.blade.php:266` (`addNewServiceProduct(i)`) + JS `formJs.blade.php:162-190` | "+" thêm nhanh hàng dịch vụ | **xoá nút `:266`** (giữ include modal để không phải sửa JS; JS không còn đường mở) (Q4) |
| `layouts/sidebar.blade.php`, `topmenubar_old.blade.php` | — | **không sửa** (không được include ở đâu — khảo sát A) |

---

## 4. ERP đọc hàng HRM không lỗi — M1–M7, N8, N9 (đã kiểm dòng gop_db)

| # | File :dòng (gop_db) | Sửa |
|---|---|---|
| **M1** | `app/Http/Controllers/Common/SearchController.php` `:824, :1235, :1678, :2042` (`$product->group->name`) | `$product->group->name ?? 'Chưa xác định'` |
| M1' | cùng file `:856, :1703, :2065` (VAT lùi về nhóm) | `floatval($product->group->vat_percent ?? 0)` (hàng VAT 0% HRM ⇒ 0) |
| **M2** | `app/Product.php` `:1247, :1248, :1317, :1318` (`'group' => $this->group->name`) · `:1261, :1331` (`$this->group->rate_liquidation ?: 0`) | `?? 'Chưa xác định'` · `($this->group->rate_liquidation ?? 0) ?: 0` |
| **M3 (N9)** | `SearchController.php` `:573, :1012, :1455, :1851` | `where(function($q){ $q->whereNull('products.product_type')->orWhere('products.product_type','!=','service_product'); })` |
| **M4** in tem | `ProductsController.php` `:586-589, :662-665` (mảng info: 4 thuộc tính nhóm) · `:688, :692` (`barcode_template_type == / !== 2`) | dùng helper mẫu tem mục 5 (`Product::barcodeInfoOf($product)`) |
| M4-js | `resources/views/warehouse/warehouse_imports/barcode.blade.php` `:195, :213` (+ `:77, :84` ng-if) | đọc `warehouseImportLot.product.barcode_template_type_effective` (trường nạp sẵn ở `WarehouseImport::getDataForBarcode` `app/Model/Warehouse/WarehouseImport.php:299-320`) |
| M4-sql | `WarehouseImport.php` `:648-666` (`getHasBarcodeTemplate1/2Attribute`, INNER JOIN `groups` `:652, :662`) | bỏ INNER JOIN `groups`; `leftJoin product_types` + `COALESCE(pt.barcode_template_type, 1)` (T1: chỉ Loại SP) |
| **M4b (MỚI — khảo sát B sót)** | `app/Http/Controllers/Warehouse/WarehouseImportsController.php:194-196` (`getWareHouseImportLot`: `Group::join(products)…->first()` rồi `$group->barcode_template_type`) — route `warehouse_imports/{product_id}/warehouse_import_lots` `web.php:1456`, gọi từ modal "In tem" của `products/list` + `product_templates/list` | hàng HRM `group_id` NULL ⇒ `$group` null ⇒ **500**; sửa dùng helper mục 5 |
| **M5** | `app/BaseProduct.php:101` · `app/Http/Requests/CustomerCare/HandoverAcceptanceRecordStoreRequest.php:84-86` · `…UpdateRequest.php:93-95` | `optional($product->group)->must_serial` · `$group && $group->must_serial` (`:63`/`:72` đã có `if (!empty(group_id))` — an toàn) |
| **M6** | `resources/views/analytics/exports/revenue_by_product.blade.php:35` | `{{ $product->group->name ?? '' }}` |
| **M7** | `resources/views/partials/classes/sale/Service.blade.php:96-101` (`addProduct`: `product.group.id/name`) | `const g = product.group || {id: 0, name: 'Chưa xác định'};` |
| **N8** | `SearchController.php` sau `:396, :899, :1341, :1747` (`products.status != 0`) | `->whereNotExists(function($q){ $q->select(DB::raw(1))->from('product_company_coefficients as pcc4')->whereColumn('pcc4.product_id','products.id')->where('pcc4.company_id', Auth::user()->info->company_id)->where('pcc4.status', 4); })` — chỉ 4 popup (Q11), không chặn `getData` |

Kiểm tĩnh (K1): `grep -n -- '->group->' <11 file trên> | grep -v -E '\?\?|optional\(|->group \?|group_id \?|->group &&'` = **rỗng**; JS `grep -n "product.group\." Service.blade.php barcode.blade.php` = rỗng.

---

## 5. Mẫu tem theo Loại SP (Q10)

**DB thật (`hrm_erp`, SELECT 09/10):** `product_types` đã có `ingredient`, `warning`, `user_manual` (varchar 500) nhưng **chưa có** `barcode_template_type`; **0 dòng** `product_types` (cả `product_natures` 1 dòng rác, `product_families`/`product_function_groups` 0) ⇒ mọi hàng hiện có `products.product_type_id` NULL (0/45.890), `group_id` NOT NULL (0 NULL). `groups.barcode_template_type`: 1 = 486, 2 = 340, 3 = 49, **4 = 15, 6 = 2, 5 = 1** (khảo sát B chỉ nêu 2/3 — thực tế dùng đủ 6 mẫu; ERP `resources/views/barcode.blade.php` rẽ nhánh theo 2/3/4/6). Bảng mẫu = `catalogs/groups/form.blade.php:134-141` = hằng HRM `ProductNature::BARCODE_TEMPLATES` (`Entities/ProductClassification/ProductNature.php:16-23`) = FE `utils/product-classification.js:12-19`.

**Luật mẫu tem hiệu lực** (T1 chốt 09/10): **chỉ** `product_types.barcode_template_type` (qua `products.product_type_id`); không có ⇒ **1**. 3 cột chữ (`ingredient`/`warning`/`user_manual`) đọc từ Loại SP, không có ⇒ `''`. Không đọc `groups`.

**ERP:** 1 helper tĩnh trong `app/Product.php` (cạnh `group()` `:741`): `public static function barcodeInfoOf($product): array` — đọc `DB::table('product_types')->where('id', $product->product_type_id)->first()` (ERP không có model ProductType) + `$product->group`; trả `['barcode_template_type','ingredient','warning','user_manual']`. Dùng ở M4, M4-js (gán thuộc tính khi nạp), M4b. M4-sql dùng COALESCE tương đương.

**HRM (P1):**

| File (worktree `hrm-api`) | Việc |
|---|---|
| `Modules/MasterData/Database/Migrations/2026_10_09_000001_add_barcode_template_type_to_product_types_table.php` *(mới)* | `unsignedTinyInteger('barcode_template_type')->nullable()->after('long_stock_days')` + comment "6 mẫu = ProductNature::BARCODE_TEMPLATES; NULL ⇒ ERP in mẫu 1"; `down` drop. `Schema::hasColumn` guard (DB gộp dùng chung `migrations` với ERP) |
| `Entities/ProductClassification/ProductType.php:20-37` | thêm `barcode_template_type` vào `$fillable`; cast `integer` |
| `Http/Requests/ProductClassification/ProductTypeRequest.php:29-52` | `'barcode_template_type' => ['nullable', 'in:'.implode(',', array_keys(ProductNature::BARCODE_TEMPLATES))]` (T1: không bắt buộc, trống ⇒ mẫu 1); không thêm message (lang chuẩn), thêm `attributes()` "Mẫu in tem" |
| `Services/ProductClassification/ProductTypeService.php:74-86` (`fillableFrom`) + `:94-106` (`catalogColumns` — lịch sử) + `catalogDisplay` | ghi cột; lịch sử hiển thị nhãn mẫu |
| `Transformers/ProductClassification/ProductTypeResource.php:28-36` | `barcode_template_type` + `barcode_template_text` |
| `Tests/Feature/ProductClassificationCatalogTest.php` | thêm ca: lưu 1–6 OK · 9 ⇒ 422 · bỏ trống ⇒ NULL · sửa đổi mẫu ghi lịch sử |

| File (`hrm-client`) | Việc |
|---|---|
| `pages/master-data/product-types/AddProductTypeModal.vue` (620 dòng) — khối "3 trường in tem" (comment `:174`, 3 × `col-md-4` `:176-195`) | đổi thành 4 × `col-md-3`: **Mẫu in tem** (`V2BaseSelectInModal`, options `BARCODE_TEMPLATE_OPTIONS`, `allowClear`, placeholder "Mặc định: Máy móc, thiết bị") + 3 textarea — đủ 12 cột (memory *form-modal-bo-cuc-hang-day-du*); `data` mặc định `barcode_template_type: null`; gửi lên ở payload |
| `pages/master-data/product-types/index.vue` | (tuỳ ⭐T3) cột "Mẫu in tem" ẩn mặc định trong cấu hình cột |

⚠️ **N11 chặn P1 trên `hrm_erp`:** DB `hrm_erp` đã DROP `product_types.can_retail` (SHOW COLUMNS 09/10 không có cột) nhưng nhánh feature còn `can_retail` ở entity `$fillable` `:25`, request `:43`, service `:77`, form `:158-172` ⇒ **POST/PUT product-types đang 500** trên DB này ⇒ không kiểm được ô mới. Xem ⭐T2.

---

## 6. Observer chỉ ghi log (Q7)

- `app/Observers/ProductWriteAuditObserver.php` *(mới — ERP chưa có thư mục Observers)*: `saved`/`deleted` trên `App\Product`, `App\Model\Product\ProductUnit`, `ProductUnitPrice`, `ProductCompanyCoefficient`; bỏ qua khi `request()->route()` có tên ∈ **danh sách trắng ghi** (`product.updateEnglishName`, `product.updateHSCode`, `products.updatePrice`, `product.manualUpdatePrices`, `products.approve*Submit` ×4, `PriceCalculate.*`, `tmpProductApprove`, `productAddEquipment`) hoặc chạy console với lệnh giá (`product:update_price`, `product:reset_price_when_zero_inventory`); còn lại ghi 1 dòng JSON: model, id, `getDirty()` keys (không ghi giá trị), route name/URI, user id, `app()->runningInConsole()`. Bọc `try/catch(\Throwable)` — không bao giờ ném.
- Kênh log riêng `product_write_audit` (daily, 30 ngày) ở `config/logging.php`.
- Đăng ký ở `AppServiceProvider::boot` (4 dòng `::observe`).
- ⚠️ Query builder (`Brand::updateProducts`, 2 job thuế E7/E8, cron reset giá) **không** qua observer — đã ghi trong khảo sát A; E7/E8 là đường giữ.

---

## 7. Task theo thứ tự (TDD / kiểm)

### PHA 1 — HRM mẫu tem (worktree, nhánh `feat/p2d1-mau-tem`)
- [ ] H1 Viết test đỏ (`ProductClassificationCatalogTest`): 4 ca mục 5. Chạy `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php` ⇒ đỏ.
- [ ] H2 Migration + entity + request + service + resource ⇒ xanh. Migration CHỈ chạy vào `hrm_erp` khi user cho (mục 9) — PHPUnit `DatabaseTransactions` cần cột thật ⇒ chạy migrate trước H2.
- [ ] H3 (tuỳ ⭐T2) xử lý `can_retail`.
- [ ] H4 FE form + Playwright MCP (`http://127.0.0.1:3000`): đo hàng ô (4 ô `col-md-3` cùng `offsetTop`, tổng rộng ≈ hàng), select có 6 option + bỏ trống được, Lưu ⇒ đúng 1 request `PUT/POST product-types` payload có `barcode_template_type`, mở lại hiện đúng nhãn; không quyền (role tạm) ⇒ không thấy nút Thêm/Sửa (memory *always-test-permission-cases*).
- [ ] H5 Hồi quy toàn bộ `ProductClassificationCatalogTest` + `ProductNatureAutoPartsTest`; sửa spec e2e `product-catalog-ui.spec.ts` (ca Loại SP có ô mới) — chỉ `--list`, chạy khi user yêu cầu.

### PHA 2 — ERP (worktree `wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi` từ `origin/gop_db`)
- [ ] E0 Môi trường (hỏi riêng): `git worktree add ../wt-erp-2d1 -b feat/2d1-erp-khong-loi origin/gop_db`; `composer install` trong worktree (KHÔNG symlink vendor — memory *worktree-vendor-symlink-autoload-bug*); `.env` sao từ repo chính, đổi `DB_DATABASE=hrm_erp`, `HRM_URL_FE=http://127.0.0.1:3000` (+ `JWT_SECRET` = hrm-api, vì `sso.check` `CheckSSOTokenMiddleware.php:23-48` đẩy về HRM login); `ls bootstrap/cache/config.php` phải KHÔNG có, `php artisan config:clear`; `php -m | grep sqlite` (test route dùng sqlite `:memory:` của `phpunit.xml`).
- [ ] E1 **Test đỏ** `tests/Feature/ProductMovedToHrmRoutesTest.php` (không cần DB: `AppServiceProvider` chỉ gọi `Schema::hasTable` ⇒ false trên sqlite): duyệt `Route::getRoutes()`, khẳng định **đúng 56 route** mục 2.6 có `productMovedToHrm` (so theo tên route + method + URI, `productDelete` theo URI vì trùng tên), **7 URI gỡ** không còn, mọi route TRẮNG liệt kê ở 2.1–2.5 **không** có MW; ca hành vi: gọi GET `admin/products/1/edit` với user giả (`actingAs` + bỏ middleware `sso.check`/`userLogin` bằng `withoutMiddleware([...])`) ⇒ 403 + view chứa link `/master-data/products/1/edit`; POST `admin/products/1/update` + AJAX ⇒ 403 JSON `success=false`. Đối chứng: tạm bỏ MW 1 route ⇒ test đỏ.
- [ ] E2 Middleware `app/Http/Middleware/ProductMovedToHrm.php` + alias `app/Http/Kernel.php:58-76` + view `resources/views/errors/moved_to_hrm.blade.php` (`@extends('layouts.app')`) ⇒ E1 xanh.
- [ ] E3 `routes/web.php`: gắn MW 56 dòng (đặt MW **đầu** danh sách middleware của route), xoá 7 dòng ⇒ E1 xanh.
- [ ] E4 Menu/nút mục 3.
- [ ] E5 N2: `ManufacturesController.php` bỏ `:186-190` (store) + `:270-275` (update) + validate `:228-230`; ẩn thẻ "Hệ số giá theo công ty" `catalogs/manufactures/form.blade.php` (khối từ `:85`, bảng `:104`) + bỏ gửi `company_coefficients` ở `partials/classes/sale/Manufacture.blade.php:92`. N3: `BrandsController.php:138, :215` gỡ 2 lời gọi `updateProducts()`. (Màn sửa đã bị MW chặn — sửa code vẫn làm để phòng ai mở lại route.)
- [ ] E6 M1–M7 + M4b + N8 + N9 mục 4; kiểm tĩnh K1.
- [ ] E7 Helper mẫu tem mục 5 + M4/M4-js/M4-sql/M4b.
- [ ] E8 Observer mục 6.
- [ ] E9 `php -l` mọi file sửa; `php artisan route:list --name=product` (đếm) ; `php artisan view:cache` KHÔNG tính là lint Blade (memory *erp-blade-json-directive-gotcha*) ⇒ mở thật từng view sửa ở PHA 3.

### PHA 3 — Kiểm trên `hrm_erp` (Playwright MCP, đo DOM) — xem mục 8.

---

## 8. Bộ nghiệm thu (K1–K11 cập nhật theo chốt + K12–K20 mới)

**Dữ liệu kiểm cần tạo (GHI DB — hỏi user riêng, ghi id, xoá đúng id sau khi đo):**
- **D0** Cây phân loại HRM: 1 Tính chất (`barcode_template_type` 3) → 1 Nhóm chức năng → 1 Nhóm SP → **2 Loại SP**: `LT3` (mẫu tem 3, có Thành phần/Cảnh báo) và `LTN` (mẫu tem trống) — qua API HRM (cần P1 + ⭐T2).
- **H1** hàng HRM tạo qua `POST master-data/products` (Cty 1), Loại SP `LT3`, **VAT 0%** (`tax_rates.id=3`), 2 ĐVT. **H2** hàng HRM, Loại SP `LTN`, VAT 10%.
- **H3** = H1 sau khi Cty khác lấy về rồi **khoá (status 4)** ở công ty đó (dùng chức năng 2-C2/2-C4).
- **P1** phiếu nhập kho ERP chỉ có H1 (in tem). **P2** biên bản bàn giao nghiệm thu có H1. (Tạo qua giao diện ERP worktree; nếu không đủ dữ liệu chứng từ nguồn thì báo user — không INSERT tay.)
- **N2-fixture** chọn 1 hãng nhiều hàng status 1 có `products.company_id` ≠ `manufactures.company_id` (đo trước: 367 hàng như vậy).

| # | Kiểm | Đạt khi | Cách |
|---|---|---|---|
| K1 | grep tĩnh `->group->` 11 file + JS | rỗng | shell |
| K2 | SQL mô phỏng WHERE popup (N9 + N8) | H1, H2 có; 30 hàng dịch vụ không; số dòng hàng cũ **không đổi** (so trước/sau theo từng id, không GROUP_CONCAT — memory *group-concat-cat-checksum-gia*); H3 không có với user Cty khoá, có với Cty 1 | SQL |
| K3 | bất biến G2 H1/H2 (đủ 6 dòng giá/ĐVT, 1 `is_base`) | đúng | SQL |
| K4 | `GET modal_data/searchProduct`, `searchProductStockBuyer`, `searchProductStockBuyerApi`, `searchProduct2` (có/không `price_type`, từ khoá mã H1) | 200; cột Nhóm "Chưa xác định"; `vat_percent` = 0 (H1) | Playwright `request` trong phiên ERP |
| K5 | `GET products/{H1}/getData`, `getDataForPriceAsking` | 200, `group` = "Chưa xác định" | như K4 |
| K6 | In tem: `products/barcode?…` H1 + màn in tem P1 + modal "In tem" ở `products/list` (gọi `warehouse_import_lots`, M4b) | 200; nút in mẫu đúng (H1 ⇒ mẫu 3: ô NSX/HSD hiện; H2 ⇒ mẫu 1); 0 lỗi console; hàng ERP cũ chưa có Loại SP ⇒ mẫu 1 (T1 chốt, chủ đích) | Playwright UI, đo số `input.date` theo dòng |
| K7 | Lưu/sửa P2 + mở danh sách sản phẩm bàn giao | không 500 | Playwright UI |
| K8 | Xuất *Doanh thu theo hàng hoá* có H1 | file ra (HTTP 200, content-type xlsx/pdf) | bán tự động |
| K9 | Màn Dịch vụ thêm H1 | nhóm "Chưa xác định", 0 lỗi console | Playwright UI |
| K10 | 3 màn đại diện chọn H1 trong popup (báo giá, phiếu xuất kho, hợp đồng) | chọn được, 0 lỗi console | Playwright UI |
| K11 | Đếm bảng con H1/H2, mã rỗng/trùng (bước 11–13 hợp đồng cũ) | như hợp đồng | SQL |
| **K12** | PHPUnit route (E1) | 56 MW · 7 gỡ · trắng không MW | phpunit |
| **K13** | Gõ thẳng URL (GET) mỗi nhóm: `products/create`, `products/{id}/edit`, `products/{id}/delete`, `product2/{id}/delete`, `product_templates/{id}/edit`, `product-infos/{id}/syncInfo`, `products/update-products`, `manufactures/create`, `brands/{id}/edit`, `manufacture_expect_prices/create` | HTTP 403; DOM có đúng 1 thẻ `a[href]` = `hrm_url_FE` + đường đích mục 2 (đúng `{id}`); Cập nhật giá theo hãng: câu "đã ngừng sử dụng", không link | Playwright UI |
| **K14** | POST/PUT bằng `fetch` (kèm CSRF) vào `productUpdate`, `productStore`, `bulkDelete`, `importExcelInstallWork`, `startUpdateListProducts`, `productTemUpdate`, `manufacUpdate`, `manufacFastStore`, `brandUpdate` (PUT), `manufactureExpectPrice.store`, `productStoreService` | 403 JSON `success:false`, message đúng; SQL: 0 dòng `products/manufactures/brands/product_expected_prices` đổi `updated_at` | Playwright + SQL |
| K14-g | 7 URI gỡ | 404 | Playwright |
| K14-m | Menu/nút (đo DOM): link "Danh mục hàng hóa gốc", "Cập nhật nhanh hàng hóa", cột "Đồng bộ hàng hoá" = 0; link Danh mục hàng hóa `href` bắt đầu bằng `hrm_url_FE`, `target=_blank`; Kế toán → Giá bán có "Hàng chưa có công khoán" (1) và "Cập nhật giá theo hãng" (1); `products/list` 0 nút Thêm mới/Import/Xóa sản phẩm, còn Cập nhật giá + Xuất Excel; menu dòng 0 Sửa/Xóa/Sao chép/Khôi phục; `products/{id}/show` footer 0 Sửa/Xóa/Sao chép; `manufactures` 0 Thêm mới/Import/Sửa/Xóa, menu ⚙ còn 3 mục; `brands` tương tự; `manufacture_expect_prices` 0 nút tạo, chi tiết phiếu cũ mở 200; Báo giá dịch vụ 0 nút "+" thêm hàng; hàng tạm "+" thương hiệu/hãng (đã chết sẵn) ghi số đo trước/sau | Playwright UI |
| **K15** | **Danh sách trắng còn sống**: sửa tên TA ở `purchase_invoice/create` (`updateEnglishName` 200, SQL `english_name` đổi rồi trả lại) · HS code ở `buy_requests` (`updateHSCode` 200) · `addEquipment` ở báo giá dịch vụ · Cập nhật giá nhanh `updatePrice` 200 (rồi trả lại giá) · duyệt 1 hàng tạm (`tmpProductApprove`) · `getPriceOfProducts` 200 · KPI XNK của 1 hãng lưu 200 · xuất "Hàng chưa có công khoán" từ menu Kế toán 200 | đúng | Playwright UI + SQL (ghi id, trả lại giá trị cũ — hỏi riêng) |
| **K16** | **Không quyền**: tài khoản thiếu `Tổng hợp đặt hàng` ⇒ `updateEnglishName` 403 "Không có quyền!" (CheckPermission vẫn chạy); tài khoản thiếu `Sửa hàng hóa` gõ `products/{id}/edit` ⇒ trang "đã chuyển sang HRM" (MW đứng trước — không lộ dữ liệu); tài khoản thiếu `Cập nhật nhanh giá hàng hóa` vào `manufacture_expect_prices/create` ⇒ `not_found` (MW group chạy trước) | đúng | Playwright (role tạm — hỏi riêng; memory *e2e-cap-quyen-sql-phai-xoa-cache*) |
| **K17** | **N2 SQL từng dòng**: chụp `products(id, company_id, updated_at, updated_by)` + `product_company_coefficients(id, product_id, company_id, coefficient, status)` của hãng fixture; Lưu KPI/Cấu hình NV của hãng (route còn sống) và gọi thẳng `manufacUpdate` (bị 403) | 0 dòng khác (so từng dòng bằng `JOIN … WHERE NOT (a<=>b)`), kể cả khi đổi công ty | SQL |
| **K18** | N8 popup: user Cty khoá H3 | H3 không có ở 4 popup; user Cty 1 vẫn có | Playwright `request` |
| **K19** | Observer: thao tác K15 ⇒ log `product_write_audit` **không** có dòng nào; gọi 1 đường ngoài danh sách trắng còn mở (vd tinker `Product::find(H2)->touch()` — hỏi riêng) ⇒ đúng 1 dòng | đúng | đọc log |
| **K20** | HRM mẫu tem (P1): mục 7 H4 | đúng | Playwright MCP HRM |

Dọn: xoá H1/H2/H3/D0 qua chức năng xoá 2-C4 (hàng chưa có chứng từ ⇒ P1/P2 phải xoá trước — hỏi user cách dọn P1/P2), checkpoint ghi "đã dọn: 0 dòng còn".

---

## 9. Phạm vi xin phép (đưa user duyệt "làm" — mỗi PHA xin riêng)

| | PHA 1 — HRM | PHA 2 — ERP code | PHA 3 — kiểm |
|---|---|---|---|
| Repo | `hrm-api` + `hrm-client` (worktree `websites/wt-chuyen-doi-hang-hoa/`) | `ERP/TanPhatDev` — **worktree mới** `websites/wt-erp-2d1` (repo chính đang `develop_01`, không checkout) | ERP worktree + HRM worktree |
| Nhánh | `feat/p2d1-mau-tem` từ `feat/chuyen-doi-hang-hoa` (api `488269eed`, client `07e829014`); xong: merge `--no-ff` về nhánh chung (hỏi riêng). ⛔ KHÔNG merge `gop_db` (memory *khong-merge-vao-gop-db*) | `feat/2d1-erp-khong-loi` từ `origin/gop_db` `04b61efc24`. Commit/push/merge vào `gop_db` — hỏi riêng | — |
| File tạo | migration `2026_10_09_000001_add_barcode_template_type_to_product_types_table.php` | `app/Http/Middleware/ProductMovedToHrm.php` · `resources/views/errors/moved_to_hrm.blade.php` · `app/Observers/ProductWriteAuditObserver.php` · `tests/Feature/ProductMovedToHrmRoutesTest.php` | — |
| File sửa | api: `ProductType.php`, `ProductTypeRequest.php`, `ProductTypeService.php`, `ProductTypeResource.php`, `ProductClassificationCatalogTest.php` (+ T2: gỡ `can_retail`) · client: `AddProductTypeModal.vue` (+ ⭐T3 `index.vue`) · e2e: `product-catalog-ui.spec.ts` | `routes/web.php` · `app/Http/Kernel.php` · `config/logging.php` · `app/Providers/AppServiceProvider.php` · `app/Product.php` · `app/BaseProduct.php` · `ProductsController.php` · `ProductTemplatesController.php` · `Common/SearchController.php` · `Sale/ManufacturesController.php` · `Sale/BrandsController.php` · `Warehouse/WarehouseImportsController.php` · `Model/Warehouse/WarehouseImport.php` · `Requests/CustomerCare/HandoverAcceptanceRecord{Store,Update}Request.php` · view: `layouts/topmenubar`, `products/list`, `products/show`, `product_templates/list`, `catalogs/manufactures/{list,form}`, `partials/classes/sale/Manufacture`, `catalogs/brands/list`, `sale/manufacture_expect_prices/index`, `sale/service_quotations/form`, `warehouse/warehouse_imports/barcode`, `analytics/exports/revenue_by_product`, `partials/classes/sale/Service` — **≈ 30 file** | — |
| Migration / seeder | **1 migration HRM chạy vào `hrm_erp`** (`php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_10_09_000001_…` — chỉ file này). Không seeder, không quyền mới | **KHÔNG** migration, KHÔNG seeder, KHÔNG gỡ quyền | — |
| Môi trường | — | `git worktree add`, `composer install` trong worktree, `.env` worktree trỏ `hrm_erp` + `HRM_URL_FE` + `JWT_SECRET`; `config:clear` | chạy `php artisan serve` ERP worktree ở cổng riêng (vd 8090) |
| Ghi DB `hrm_erp` | PHPUnit `DatabaseTransactions` (rollback) | không | **tạo D0, H1–H3, P1, P2, role tạm; sửa-rồi-trả-lại ở K15; tinker K19** — liệt kê id, dọn sau; hỏi riêng trước khi ghi |

---

## 10. Rủi ro

| # | Rủi ro | Né |
|---|---|---|
| R1 | Chặn nhầm route đọc ⇒ vỡ ~150 chỗ gọi (getData, getPriceOfProducts) | test E1 khẳng định danh sách trắng; không gắn MW cấp group |
| R2 | Sót đường ghi (job, query builder, màn lạ) | observer log 2–4 tuần (chỉ bắt Eloquent); E7/E8 thuế giữ chủ đích |
| R3 | ERP gop_db login qua SSO HRM ⇒ không đăng nhập local được | E0 cấu hình `HRM_URL_FE` + `JWT_SECRET`; nếu vẫn không được báo user trước khi làm PHA 3 |
| R4 | `hrm_erp` không có dữ liệu phân loại (0 Loại SP) + N11 `can_retail` ⇒ không tạo được Loại SP/hàng HRM để kiểm | T2 (gỡ `can_retail`); D0 tạo qua API sau khi P1 xong |
| R5 | Đổi luật mẫu tem làm hàng ERP cũ đổi mẫu | T1 chốt: chỉ theo Loại SP — hàng chưa gắn Loại SP in mẫu 1; user gắn Loại SP cho dữ liệu cũ xong rồi mới cập nhật product lên production |
| R6 | Trang 403 GET làm "người dùng tưởng lỗi" khi bấm link cũ đã lưu | câu rõ + nút sang HRM |
| R7 | Tab ERP cũ đang mở bấm Lưu ⇒ "Đã có lỗi xảy ra" (403 rơi vào nhánh `error`) | chấp nhận (Q6) |
| R8 | `productDelete` trùng tên: sửa sai bản | MW cả 2; test theo URI |
| R9 | Blade lỗi chỉ lộ khi mở trang (view:cache không lint) | PHA 3 mở thật mọi view sửa, đo console |
| R10 | Mất lối "In tem từ danh mục hàng hoá" khi menu chuyển HRM | T5: giữ route `proList` qua URL, backlog in tem HRM |
| R11 | Hệ số giá đóng băng (N35) do bỏ thẻ hệ số Hãng SX | đã chấp nhận QC-3 |
| R12 | Observer log nhiều ở luồng giá | danh sách trắng route giá + lệnh cron |

**Việc ngoài luồng mới (thêm `chot.md` khi user duyệt):** N37 `WarehouseImportsController@getWareHouseImportLot` `:194-196` nổ với hàng không nhóm (đưa vào 2-D1 là M4b — chỉ ghi nhận khảo sát B sót) · N38 `groups.barcode_template_type` dùng cả mẫu 4/5/6 (khảo sát B chỉ nêu 2/3) · N39 ERP `CLAUDE.md` ghi Laravel 8, thực tế `^6.2` · N40 `brands/list` gọi `products.importExcelAttribute` (import thuộc tính hàng từ màn Thương hiệu) — chặn theo luôn.

---

## 11. Câu hỏi còn tồn (nghiệp vụ — chưa trả lời thì chưa code phần liên quan)

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **T1** | Mẫu tem khi hàng có **cả** Loại SP (có mẫu) **và** nhóm cũ (hàng ERP cũ đã được sửa ở HRM — C2 bắt chọn Loại SP), lấy cái nào? Ô mẫu tem ở Loại SP **bắt buộc** hay không? 3 cột chữ in tem (Thành phần/Cảnh báo/HDSD) có đọc theo Loại SP luôn không? | ⭐ **Loại SP (nếu đã chọn mẫu) → nhóm → mẫu 1**; ô **không bắt buộc** (trống ⇒ lùi nhóm/mẫu 1); 3 cột chữ cùng thứ tự | Ưu tiên Loại SP: đi đúng hướng bỏ `groups`, nhưng Loại SP điền sai thì hàng cũ đổi mẫu. Ưu tiên nhóm: hàng cũ không bao giờ đổi, Loại SP chỉ tác dụng với hàng HRM tạo. Bắt buộc: mọi Loại SP phải chọn khi lưu (kể cả sửa Loại SP cũ) |
| **T2** | N11: `hrm_erp` đã bỏ cột `product_types.can_retail` nhưng nhánh feature còn dùng ⇒ lưu Loại SP đang 500 trên DB này. Xử lý trong P1? | ⭐ **Có — trong P1 gỡ `can_retail`** khỏi entity/request/service/form Loại SP (như gop_db) | Có: kiểm được ô mẫu tem + tạo D0; +4 file. Không: P1 chỉ kiểm bằng PHPUnit trên DB có cột (không có DB nào như vậy) ⇒ không kiểm được UI |
| **T3** | Danh sách Loại SP có thêm cột "Mẫu in tem" không? | ⭐ Thêm, **ẩn mặc định** trong cấu hình cột | Thêm: tra cứu nhanh Loại SP nào chưa điền mẫu. Không: phải mở từng Loại SP |
| **T4** | Cột menu "Hàng hóa có sẵn" còn 9 danh mục `pi-*` (model/thương hiệu/hãng… của hàng có sẵn, 0 dữ liệu) — ẩn luôn? | ⭐ **Ẩn cả cột** (route giữ) | Ẩn: menu gọn, không ai dùng. Giữ: còn chỗ sửa danh mục `pi-*` (không ảnh hưởng `products`) |
| **T5** | Bỏ menu Danh mục HH ERP (Q1) làm mất lối **"In tem / In barcode" theo từng hàng** ở màn danh sách ERP (modal `products/list.blade.php:170-224`, HRM chưa có in tem); route `proList` vẫn vào được bằng URL | ⭐ Giữ route `proList` (chỉ xem + in tem), **không** có menu; in tem chủ yếu qua phiếu nhập kho; ghi backlog "in tem trên HRM" | Theo ⭐: ai in tem lẻ phải nhớ URL. Thêm link nhỏ "In tem hàng hoá (ERP)" trong menu Kho: đổi một phần Q1 |
| **T6** | Chặn xoá Hãng SX/Thương hiệu ở ERP (Q2 ghi "thêm/sửa") — gồm cả **Xóa** và **Import Excel** danh mục? | ⭐ **Chặn cả Xóa + Import** (CRUD đầy đủ chỉ ở HRM) | Chặn: 1 nguồn duy nhất. Để Xóa/Import ở ERP: còn đường ghi danh mục ngoài HRM |

### Trả lời user (09/10)

- **T1** 🔄 **Chỉ theo Loại SP** — nhóm (`groups`) sẽ bỏ khi chuyển đổi xong sang Loại SP ⇒ ERP in tem + 3 trường chữ (thành phần/cảnh báo/HDSD) đọc từ `product_types`, KHÔNG rơi về `groups`. Hàng chưa gắn Loại SP / Loại SP chưa chọn mẫu ⇒ mẫu 1 User: **xử lý xong dữ liệu (gắn Loại SP) rồi mới cập nhật product lên** ⇒ không cần nhánh dự phòng theo nhóm, chỉ làm theo Loại SP. Ô mẫu tem ở form Loại SP không bắt buộc (trống ⇒ mẫu 1).
- **T2** ✅ `can_retail` không dùng nữa ⇒ gỡ khỏi code nhánh feature trong P1 (entity/request/FE) cho khớp DB đã drop cột (đóng N11).
- **T3** ✅ thêm cột "Mẫu in tem" ở danh sách Loại SP, ẩn mặc định.
- **T4** 🔄 **giữ menu** cột "Hàng hóa có sẵn" (9 danh mục `pi-*`) — không ẩn; chỉ các route ghi hàng có sẵn/đồng bộ đã chặn như plan.
- **T5** ✅ giữ route `proList` vào bằng URL (không menu) để in tem từng hàng; backlog "in tem trên HRM".
- **T6** ✅ chặn cả Xoá + Import Excel Hãng SX/Thương hiệu ở ERP (giữ 3 màn con KPI/Cấu hình NV).

## Tiến độ

- **PHA 1 HRM ✅ 09/10** — nhánh `feat/p2d1-mau-tem`: api `c53ba1bf5` (cherry-pick gỡ `can_retail` từ gop_db 259ad55cb) + `f73d733d0` (cột mẫu tem); client `ffcac1daf` (cherry-pick ca4b89f35) + `612f9735e`. Migration `2026_10_09_000001` đã chạy vào `hrm_erp`. PHPUnit MasterData (trừ Regulation — đỏ sẵn do `configs.company_id` thiếu ở DB local) 150/150. Playwright đo DOM đạt (4 ô 1 dòng 98%, 6 mẫu, cột ẩn mặc định, hết "bán lẻ"). e2e: thêm 2 ca `[UI] Loại sản phẩm — mẫu in tem (2-D1)` vào `product-catalog-ui.spec.ts` (chưa chạy — chờ user). Ngoài danh sách file xin phép: thêm `CatalogHistoryService.php` + `ExportColumnRegistry.php` (nhãn lịch sử/xuất Excel của cột mới, bỏ nhãn can_retail sót). Chưa merge nhánh chung, chưa push.
- **PHA 2 ERP ✅ 09/10** — worktree `websites/wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi` từ `origin/gop_db` @`c1577ff7b7` (số dòng plan vẫn khớp, không lệch đáng kể). 6 commit, **33 file** (+1043/−661): `aee443d738` middleware + 56 route chặn + 7 route gỡ + test route · `b5da550d9e` menu/nút · `2bbfd4554c` N2/N3 · `11f8e467d9` M1, M2, M5–M7, N8, N9 · `6165372610` mẫu tem theo Loại SP (helper `Product::barcodeInfoOf`, M4, M4b, M4-sql, M4-js) · `49848d4141` observer log + test. Chưa merge, chưa push. Không migration/seeder, không ghi DB.
  - **PHPUnit** (sqlite `:memory:`, không chạm DB thật): `ProductMovedToHrmRoutesTest` 13/13 (56 MW đúng đích + đứng trước checkPermission, `productDelete` cả 2 bản, 7 URI gỡ, ~110 route trắng + vùng trắng `tmp_products`/`PriceCalculate*`/`price_log`/`pi-*`/`warehouse_import_lots`, GET ⇒ 403 trang có đúng 1 link HRM theo `{id}`, POST/PUT/AJAX ⇒ 403 JSON, HTTP thật qua router, URI gỡ ⇒ 404); đối chứng bỏ MW `productEdit` ⇒ 3 ca đỏ. `ProductBarcodeAndAuditTest` 7/7 (mẫu tem chỉ theo Loại SP, không rơi về nhóm; observer ghi/không ghi; nuốt lỗi; đăng ký 4 model). Cả bộ: 31 ca, 1 đỏ sẵn `ExampleTest` (GET `/` qua `sso.check` ⇒ 302 — không liên quan). `php -l` mọi file PHP sửa; 13 blade sửa biên dịch bằng `Blade::compileString` + `php -l` (đã thử bộ lint bắt được lỗi cú pháp). `route:list` OK (56 dòng có `productMovedToHrm`). K1 grep `->group->` 11 file = rỗng (trừ 1 dòng comment), JS `product.group.` = rỗng.
  - **Lệch so với plan:** (1) trang `errors/moved_to_hrm` đứng riêng, KHÔNG `@extends('layouts.app')` (layout kéo menu + DB ⇒ không render được trong test, và trang báo không nên phụ thuộc menu). (2) Link khi route không có `{id}` lùi về `/master-data/products/company` — HRM KHÔNG có trang `/master-data/products` (chỉ `company|create|entering|trading|warehouse|_id`). Đích: `productUpdate`/`deleteFile` ⇒ trang sửa HRM; `productDelete`/`restore` ⇒ trang chi tiết HRM; hàng gốc/product2/hàng có sẵn/đồng bộ ⇒ danh sách HRM; Cập nhật giá theo hãng ⇒ câu "đã ngừng sử dụng", `redirect_url: null`. (3) Hàng gốc bỏ luôn link Khôi phục (trỏ route `product_templates.restore` không tồn tại — 500 sẵn). (4) Hãng SX/Thương hiệu bỏ hẳn cột "Hành động" (không để cột trống). (5) Thêm null-safe ngoài 11 điểm: `Product::exportExcel` cột Nhóm (để K1 sạch), `ProductsController@barcode` hãng/model/xuất xứ (`?? ''`, cho K6 với hàng HRM), `searchData` proList cột Nhóm. (6) `barcode` nhánh `twoCode=false`: GIỮ hành vi cũ — điều kiện cũ `groups.barcode_template_type !== 2` so chuỗi (PDO) với số nên luôn đúng ⇒ luôn in; sửa thành "loại mẫu 2" là việc ngoài luồng (N41). (7) N8 đặt trong nhánh `else` cùng `status != 0` (không áp khi `type=include_deleted`). (8) `BaseProduct::isRequiredSeri` trả `?? 0` (giữ kiểu số cho FE). (9) M4b nằm ở commit mẫu tem (dùng helper).
  - **Môi trường:** `composer install` KHÔNG chạy được — `composer.lock` không nằm trong git, bản lock của repo chính lệch `composer.json` (thiếu `setasign/fpdi`, `simple-qrcode`, `browsershot`) ⇒ đã **copy** (không symlink) `vendor/` từ repo chính (cùng `composer.json`) + `composer dump-autoload` trong worktree (autoload trỏ worktree). `.env` worktree: `DB_DATABASE=hrm_erp`, `HRM_URL_FE=http://127.0.0.1:3031`, `JWT_SECRET` = hrm-api; `config:clear`, `bootstrap/cache/config.php` không có. PHP 7.4 của herd nạp `imagick.so` không tồn tại (cảnh báo) ⇒ chạy với `PHP_INI_SCAN_DIR=/opt/homebrew/etc/php/7.4/conf.d`.
  - ⚠️ **Chặn PHA 3:** ERP boot trên `hrm_erp` **nổ** ở `AppServiceProvider::boot` → `Config::getConfig()` (`Unknown column 'company_id' in configs`) — mọi `php artisan` / request với `.env` thật đều lỗi (cùng nguyên nhân Regulation đỏ ở PHA 1). PHPUnit/route:list ở PHA 2 chạy bằng sqlite nên không bị. Cần user quyết cách xử lý DB trước PHA 3 (không sửa trong 2-D1).
  - **Ngoài luồng phát hiện (chưa làm, đề xuất N41–N45):** N41 `barcode` `twoCode=false` luôn in cả hàng mẫu 2 (bug cũ, xem trên). N42 `product_infos/list` còn nút "Thêm mới" (route đã chặn ⇒ ra trang báo; T4 giữ menu nên không ẩn). N43 `app/Model/ProductInfo/BaseProduct.php:76` `isRequiredSeri` cùng mẫu `->group->` (hàng có sẵn, 0 dữ liệu). N44 `Product::exportExcel` còn `$product->model->name`, `origin->name`, `base_unit->name` không null-safe. N45 `tests/Feature/ExampleTest` đỏ sẵn.
  - **PHA 3 cần đo bằng trình duyệt:** K13/K14/K14-g/K14-m như mục 8; thêm: `products` (proList) bảng không còn cột ô tick, tiêu đề/ô lọc thẳng cột, menu ⚙ chỉ Lịch sử/In barcode; modal "In tem" với hàng HRM (M4b) 200 + ô NSX/HSD theo mẫu Loại SP; màn in tem phiếu nhập (M4-js) và 2 nút in theo `has_barcode_template_1/2`; Hãng SX/Thương hiệu danh sách không còn cột Hành động, menu ⚙ Hãng SX còn 3 mục; form Báo giá dịch vụ ô "hàng hóa liên quan" không còn nút "+" và input-group không vỡ; trang báo 403 (bố cục, 1 link HRM mở tab mới); log `storage/logs/product_write_audit-*.log` (K19).
- 09/10 user: chấp nhận vendor ERP worktree = copy từ repo chính + dump-autoload. ERP gop_db không boot trên hrm_erp (thiếu `configs.company_id`) ⇒ user chọn **chạy toàn bộ 22 migration HRM đang chờ** vào hrm_erp. Đã sao lưu hrm_erp trước (scratchpad `hrm_erp-truoc-22-migration-20261009.sql.gz`, 1,2 GB). Lệnh migrate bị bộ phân loại an toàn chặn ⇒ chờ user tự chạy.
- 09/10 user cho chạy migrate ⇒ **đã chạy đủ 22 migration HRM chờ vào hrm_erp** (từ worktree hrm-api, không lỗi). ERP worktree boot được: `/login` 200 ở cổng 8090, route:list đếm 56 route gắn `productMovedToHrm`. TIẾP: xin "làm" PHA 3.
- **PHA 3 kiểm ✅ 09/10** — chi tiết `d1-kiem-p3.md`. ERP worktree 8090 trên `hrm_erp`, đăng nhập form `/login` (e2e_assign; ERP đọc quyền theo `App\Employee` ⇒ cấp role tạm 23 quyền, đã xoá). Đạt: K1, K2 (SQL từng id: Cty1 chỉ +H1/H2 −H3', Cty2 chỉ +H1/H2, 0 hàng dịch vụ), K3, K5, K6 (H1 mẫu 3: 2 ô NSX/HSD; H2 mẫu 1; M4b 200), K9, K10 (4 màn), K11, K12, **K13 24/24 GET ⇒ 403 + đúng 1 link HRM**, **K14 32/32 POST/PUT ⇒ 403 JSON**, K14-g 7×404, K14-m, K15, K16, K17 (1.076 dòng, 0 khác), K19 (route trắng 0 dòng log; tinker touch = 1 dòng). Một phần: K4 (API key route không gọi được), K7 (chỉ đường validate — không tạo được P2), K18 (H3' = hàng cũ 50066 Cty1 tự khoá; phía Cty khác chỉ SQL). Không kiểm được HTTP: K8 (xuất Excel/PDF doanh thu theo hàng hoá 500 — lỗi cũ 2020). **0 lỗi do 2-D1**; 6 lỗi cũ ghi trong file kiểm (đề xuất N46+: màn in tem phiếu nhập thiếu include `WarehouseImportArrangeDelivery`, export doanh thu, getCost báo giá DV, infdig báo giá mẫu, `$parse` formShow NCC). P1/P2 không tạo (chuỗi chứng từ + tồn kho). Dữ liệu test đã dọn hết, mốc 16 bảng khớp.
- 09/10 N53 + N52 ✅ ERP `b2f1761789` (popup ẩn hàng status 1/2/4 ở Cty người dùng + 1/2 ở Cty tạo; title trang ngừng sử dụng). PHPUnit 3/3 + 13/13 + 7/7; SQL 8 công ty 45.890 = trước; Playwright đo title 2 loại trang (trang ngừng sử dụng đo qua render view vì e2e thiếu quyền nhóm route giá theo hãng).
- 09/10 ✅ HRM merge `feat/p2d1-mau-tem` → `feat/chuyen-doi-hang-hoa` LOCAL (api `a862fbeef`, client `9b05f7b42`), chưa push. ERP giữ nhánh `feat/2d1-erp-khong-loi`, chưa push.
