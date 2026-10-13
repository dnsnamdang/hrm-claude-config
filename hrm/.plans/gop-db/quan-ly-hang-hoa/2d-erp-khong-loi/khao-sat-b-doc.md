# Đợt 2-D — ERP không lỗi · PHẦN B: ERP ĐỌC hàng hoá do HRM tạo/ghi

> 09/10/2026 · CHỈ ĐỌC: không sửa source, không commit, không ghi DB.
> - **ERP** = `ERP/TanPhatDev`, đọc theo **`origin/gop_db` @ `04b61efc24`** (bản chụp `git archive`, không checkout —
>   checkout local đang ở `develop_01`, `SearchController` lệch gop_db 292 dòng ⇒ số dòng trong file này là của gop_db,
>   khác số dòng trong `sua-erp-de-khong-loi.md` cũ (vd `:787` cũ = `:824` nay)). PHP `^7.4` (platform 7.4.33), Laravel `^6.2`
>   ⇒ **không có `?->`**; notice "Trying to get property of non-object" bị `HandleExceptions` đổi thành `ErrorException` ⇒ **500**
>   (không có chỗ nào hạ `error_reporting`).
> - **HRM** = worktree `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/chuyen-doi-hang-hoa` @ `488269eed`.
> - **DB** = `hrm_erp` (SELECT), 09/10/2026. Hiện **0 hàng HRM tạo** trong DB (e2e đã dọn) ⇒ suy từ code `ProductWriteService`.
> - Phần A (chặn route ghi, N2–N4) không thuộc file này.

---

## 0. Tóm tắt

| # | Kết luận |
|---|---|
| 1 | **Khung đúng để soát**: so mỗi cột HRM để trống với **dữ liệu ERP đang có**. Cột mà ERP cũ đã có hàng NULL (guarantee 2.005 · product_template_id 16.077 · rate_liquidation 7.689 · avatar 442 · product_cate 204) ⇒ ERP đã chạy quen, **không nổ**. Hai cột **chưa từng NULL** là `group_id` (0/45.890) và `product_type` (0/45.890) ⇒ đúng 2 chỗ vỡ: **N7 nổ 500**, **N9 biến mất** |
| 2 | **N7 rộng hơn SearchController**: còn `Product::getDataAttribute/getData` (route `products/{id}/getData` — **71 file view / 93 lần gọi**, chạy ngay sau khi chọn hàng ở popup), **in tem** `ProductsController@barcode` (11 dòng), **bàn giao nghiệm thu** (`isRequiredSeri` + 2 Request), 1 export, 2 JS. Tổng **28 dòng PHP + 6 dòng JS** phải sửa, ở **9 file PHP + 2 file view** |
| 3 | `DeviceErrorController` (8 chỗ, doc cũ xếp 🔴) **đã an toàn** — viết `$product->group->name ?? ''`, `??` của PHP nuốt cả chuỗi null. Cùng loại: `LiquidationQuotation`, `CostFixingQuotation`, `ProductSettingMailJob`, `ExportLargeProductList`, 4/11 chỗ SearchController |
| 4 | **N9 có cách sửa 0 hệ quả**: `whereNull(product_type) OR != 'service_product'` giữ nguyên việc loại 30 hàng dịch vụ (DB hiện 0 hàng NULL) ⇒ **không cần khách xác nhận "30 hàng dịch vụ lọt popup"** như phương án (a) cũ |
| 5 | Thuộc tính nghiệp vụ của nhóm mà ERP đọc qua `->group`: đo DB thì `must_serial` = 0/893 nhóm, `rate_liquidation` > 0 = 0/893 ⇒ thay bằng 0/false **không đổi hành vi**. Riêng **`barcode_template_type`** (340 nhóm = 2, 49 nhóm = 3) có nghĩa thật ⇒ cần chốt giá trị cho hàng HRM (câu hỏi Q2) |
| 6 | G2 (1 ĐVT cơ bản + 6 dòng giá/ĐVT) **đủ** cho mọi `firstOrFail` đơn vị/giá: đếm lại **53 lệnh / 27 file** gọi trực tiếp, điều kiện chỉ có `is_base`, `unit_id` của chính hàng, `price_type_id` 1–6 (bảng `price_types` có đúng 6) |
| 7 | N1 (bảo hành/tồn tối thiểu), N5 (cron), N6 (CRM), N8 (khoá theo công ty) **không nổ** — đều là sai nghiệp vụ im lặng |

---

## 1. Hàng HRM tạo ghi gì vào `products` (suy từ code)

`ProductWriteService::store()` (`Modules/MasterData/Services/Product/ProductWriteService.php:65-93`) + `fillCommon()` `:274-305`:

| Cột | Giá trị hàng HRM tạo | ERP cũ có NULL không (`hrm_erp`, 45.890 hàng) | Kết luận |
|---|---|---|---|
| `status` | **1** (`:72`, G1) | — | hiện ngay trong popup ERP (G1 đã chấp nhận) |
| `company_id` | `current_company_role` (`:73`) | 1 hàng NULL | không nổ; ⚠️ ERP lấy công ty từ `info->company_id` (1.751 chỗ), HRM từ `company_role` — **3/1.119** nhân viên lệch hai giá trị |
| `group_id` | **NULL** (không có trong danh sách `fillCommon :276-280`) | **0** | 🔴 **N7 — nổ** |
| `product_type` (chuỗi) | **NULL** (A1/§6) | **0** | 🔴 **N9 — biến mất khỏi popup** |
| `product_cate` | NULL (§3 đóng băng) | 204 (98 hàng status 1) | không nổ (mục 4.2) |
| `product_template_id` | NULL | 16.077 (2.385 status 1) | không nổ, chỉ không sang CRM (N6) |
| `guarantee`, `guarantee_type` | NULL (G5 không ghi cột chung) | 2.005 / 461 | không nổ; bảo hành = 0 ngày (N1) |
| `min_stock_qty` | 0 (default cột) | — | không nổ; không bao giờ "dưới tồn tối thiểu" (N1) |
| `rate_liquidation` | NULL | 7.689 | ERP lùi về `group->rate_liquidation` ⇒ dính N7 |
| `vat_percent` | % suy từ `tax_rates` (`:290`), `vat_percent_tax_rate_id` **required** (`ProductRequest.php:109`) | 368 | ⚠️ thuế suất **0%** (`tax_rates.id=3`) ⇒ `vat_percent = 0` falsy ⇒ ERP lùi về `group->vat_percent` ⇒ nổ (mục 2.1) |
| `avatar` | ảnh đầu hoặc NULL (`:432-434`) | 442 | không nổ (`getImageAttribute` → `/images/noimage.png`) |
| `model_id`, `brand_id`, `manufacture_id`, `origin_id` | bắt buộc | — | ERP `->model->name`, `->brand->name` không null-safe nhưng HRM luôn có |
| Bảng con | 1 ĐVT cơ bản (hệ số 1) + **6 dòng `product_unit_prices` giá 0/hệ số 0 mỗi ĐVT** (`:322-339`); dòng `product_company_coefficients` coef 1 status 1 (`:569-574`) | | G2 đủ — mục 3.1 |

---

## 2. N7 — `->group->` không null-safe

Toàn ERP (gop_db): **109 dòng `->group->` / 28 file** (`app` + `resources`). Phân loại:

### 2.1 🔴/🟠 Nổ khi gặp hàng HRM — PHẢI SỬA (28 dòng PHP · 6 dòng JS)

| # | File:dòng | Số dòng | Chạy ở đâu | Mức |
|---|---|---|---|---|
| A | `app/Http/Controllers/Common/SearchController.php` **:824, :1235, :1678, :2042** (`addColumn('group_id', … $product->group->name)`) | 4 | 4 hàm popup tìm hàng: `searchProduct` :383 · `searchProductStockBuyer` :883 · `searchProductStockBuyerApi` :1289 · `searchProduct2` :1734 — callback DataTables chạy **từng dòng** ⇒ 1 hàng HRM lọt trang là **cả trang kết quả lỗi**. Route `modal_data/searchProduct*` (`routes/web.php:5487-5509`), 159 file view tham chiếu (doc cũ: 338 màn) | 🔴 |
| A' | cùng file **:856, :1703, :2065** (`vat_percent ? … : floatval($product->group->vat_percent)`) | 3 | như trên, nổ khi hàng HRM có VAT **0%** | 🔴 |
| B | `app/Product.php` **:1247, :1248, :1261** (`getDataAttribute`) · **:1317, :1318, :1331** (`getData($company_id)`) | 6 | `ProductsController@getData` (`ProductsController.php:3153` `$json->data = $product->data`, route `products/{id}/getData` `web.php:599`) — gọi từ **71 file view / 93 lần** (`/admin/products/${product.id}/getData`), tức là **ngay sau khi chọn hàng** ở báo giá / hợp đồng / xuất nhập kho…; + `getDataForPriceAsking` (`web.php:600`) + 29 dòng `$product->data` ở 24 file PHP + `ComboCampaign.php:147` | 🔴 (nặng ngang A) |
| C | `app/Http/Controllers/ProductsController.php` **:586-589, :662-665, :688, :692** (hàm `barcode` :555) | 11 | route `proBarcode` `web.php:576` — **in tem mã vạch**, gọi từ `warehouse_imports/barcode.blade.php:251-252` (in tem phiếu nhập kho), `products/list`, `products/show`, `product_templates/list`. Đọc 4 thuộc tính nhóm: `barcode_template_type`, `ingredient`, `warning`, `user_manual` | 🔴 |
| C-js | `resources/views/warehouse/warehouse_imports/barcode.blade.php` **:195, :213** (`warehouseImportLot.product.group.barcode_template_type`) | 2 | JS TypeError ⇒ hỏng màn in tem phiếu nhập. (`:77, :84` là biểu thức `ng-if` — Angular nuốt null, không nổ) | 🔴 |
| C-sql | `app/Model/Warehouse/WarehouseImport.php` **:652, :662** (`join('groups as g' …)` trong `has_barcode_template_1/2`) | 2 | INNER JOIN ⇒ phiếu nhập **chỉ có hàng HRM** thì cả 2 cờ = false ⇒ **không hiện nút in tem nào** (`barcode.blade.php:118-147`) — im lặng | 🟡 |
| D | `app/BaseProduct.php` **:101** (`isRequiredSeri`: `$product->group->must_serial`) | 1 | `Customercare/HandoverAcceptanceRecordsController.php:502, :511` — biên bản bàn giao nghiệm thu | 🟠 |
| D' | `app/Http/Requests/CustomerCare/HandoverAcceptanceRecordStoreRequest.php` **:84→:86** · `…UpdateRequest.php` **:93→:95** (`$group = Group::find($product_->group_id); if($group->must_serial)`) | 2 | lưu biên bản bàn giao nghiệm thu có hàng HRM ⇒ 500 | 🟠 |
| E | `resources/views/analytics/exports/revenue_by_product.blade.php` **:35** (`{{ $product->group->name }}`) | 1 | xuất PDF/Excel *Doanh thu theo hàng hoá* (`RevenueByProductController:54`, `ExcelExports/RevenueByProduct.php:42`) | 🟠 |
| F-js | `resources/views/partials/classes/sale/Service.blade.php` **:96, :98, :100, :101** (`addProduct`: `product.group.id/name`) | 4 | màn **Dịch vụ** `sale/services/create|edit` (`formJs.blade.php:6`) — thêm hàng HRM vào dịch vụ ⇒ TypeError | 🟠 |

**Cộng: 28 dòng PHP (A 4 + A' 3 + B 6 + C 11 + D 1 + D' 2 + E 1) · 6 dòng JS (C-js 2 + F-js 4)** · 9 file PHP + 2 file view JS.

### 2.2 ✅ Đã an toàn — KHÔNG sửa (đính chính doc cũ)

| File:dòng | Vì sao an toàn |
|---|---|
| `Sale/DeviceErrorController.php` :253, :261, :302, :310, :478, :486, :522, :530 (8) | `$product->group->name ?? ''` — `??` nuốt cả chuỗi null (doc cũ xếp 🔴, sai) |
| `SearchController.php` :862, :1271, :1709, :2071 (4) | `$product->group ? … : 0` |
| `Model/Sale/LiquidationQuotation.php:51`, `CostFixingQuotation.php:51` | `$real_product->group && …` |
| `Jobs/ProductSettingMailJob.php:183`, `Console/Commands/ExportLargeProductList.php:267`, `ProductsController.php:4183` | `$p->group_id ? … : ''` |
| `ProductsController.php:179` (`searchData` — danh sách hàng hoá ERP) | `if($product->group_id)` → `'Chưa xác định'` |
| `products/pdf.blade.php:25`, `product_templates/pdf.blade.php:25`, `tmp_products/pdf.blade.php:30`, `products/exports/product_export.blade.php:62`, `product_templates/exports/product_export.blade.php:62` | đã kiểm `group_id`/`group` |
| `Sale/TmpProductsController.php:178, :194` | đã kiểm |
| `quotations/formJs.blade.php:18`, `tech/InstallSummaryProduct.blade.php:96-109` (JS) | `product.group && …`; `:102/:109` sau guard `has_checksheet` |

### 2.3 ⚪ Không liên quan / chết

| File:dòng | Lý do |
|---|---|
| `Product.php:6612` (`Product::exportExcel`) | không ai gọi (`Jobs/ProductMailJob.php:41` đã comment) |
| `ProductsController.php:384` (`searchDataProductApprover`) | không có route |
| `ProductsController.php:541` | comment |
| `sale/customers/show.blade.php:61`, `sale/suppliers/show.blade.php:61` | nhóm KHÁCH HÀNG |
| `Model/Product/JobCluster.php:21-22` | cây catalog cũ (Phase 5) |
| `TmpProductsController.php:68`, `MyTmpProductsController.php:75`, `Model/Product/TmpProduct.php:115` | bảng `tmp_products` (hàng tạm, có nhóm riêng) |
| `ProductInfo*`, `ProductTemplate*`, `Product2Controller`, `SyncProductInfoService.php:211` | bảng khác / bị chặn / bỏ qua (§1.4 doc cũ) |

### 2.4 🟡 Im lặng: INNER JOIN `groups` ⇒ hàng HRM biến mất khỏi báo cáo

| File:dòng | Ảnh hưởng |
|---|---|
| `Model/Warehouse/ProductExportDetail.php:266` (`marketAnalysisProductGroupQuery`, gọi :272, :290, :305) | báo cáo phân tích thị trường theo nhóm thiếu hàng HRM |
| `Services/OrderReports/StockTransferReportService.php:301, :355, :2313, :2367` | báo cáo chuyển kho thiếu hàng HRM |
| `MarketCommodity*ReportService` (~30 chỗ) | ✅ chỉ JOIN khi người dùng **lọc theo nhóm** (`case 5`) — đúng nghĩa |
| 34 `leftJoin('groups' …)` / 11 file | cột nhóm hiện trống — chấp nhận |

### 2.5 Đề xuất sửa N7

PHP 7.4 ⇒ không dùng `?->`. Hai khuôn, đều đã có tiền lệ trong chính ERP:

| Chỗ | Khuôn | Lý do |
|---|---|---|
| A, B (tên nhóm) | `$product->group->name ?? 'Chưa xác định'` | khuôn `ProductsController:179` + `Product2Controller searchData`; `??` ngắn hơn `optional()` |
| A', B (VAT, `rate_liquidation`) | `floatval($product->group->vat_percent ?? 0)` · `($this->group->rate_liquidation ?? 0) ?: 0` | đo: 0/893 nhóm có `rate_liquidation` > 0 ⇒ hành vi không đổi; VAT 0% ⇒ trả 0 là đúng |
| C (in tem) | `$product->group->barcode_template_type ?? <mặc định Q2>`, 3 cột chữ `?? ''` | xem Q2 |
| C-js, F-js | `(x.product.group \|\| {}).barcode_template_type`; Service: nhóm giả `{id: 0, name: 'Chưa xác định'}` | |
| C-sql | `leftJoin` + điều kiện `COALESCE(g.barcode_template_type, <mặc định>)` | |
| D, D' | `optional($product->group)->must_serial` / `$group && $group->must_serial` | 0/893 nhóm bật `must_serial` ⇒ không đổi hành vi |
| E | `?? ''` | |
| 2.4 INNER JOIN | đổi `leftJoin` (6 chỗ, 2 file) | ⏸ đề xuất để sau (báo cáo, không nổ) |

Phương án gom (`sua-erp-de-khong-loi.md` §2.2: accessor `group_name`, `group_vat_percent`… trong `Product.php`) vẫn dùng được cho B, nhưng A/C gọi trên đối tượng trả từ query builder riêng — **đề xuất `??` tại chỗ cho cả 28 dòng**, ít rủi ro hơn.

Kiểm tĩnh sau sửa: `grep -rn -- '->group->' <9 file> | grep -v -E '\?\?|optional\(|->group \?|group_id \?|->group &&'` phải **rỗng**.

---

## 3. N9 — lọc `product_type != 'service_product'` loại mất dòng NULL

### 3.1 Vị trí

| File:dòng | Hàm |
|---|---|
| `SearchController.php:573` | `searchProduct` |
| `SearchController.php:1012` | `searchProductStockBuyer` |
| `SearchController.php:1455` | `searchProductStockBuyerApi` |
| `SearchController.php:1851` | `searchProduct2` |

Toàn ERP chỉ có **4 chỗ** `!=`/`<>` trên `product_type` (grep `app resources routes`). SQL `NULL != 'x'` → NULL → loại dòng ⇒ hàng HRM **không hiện ở popup** (không lỗi gì).

### 3.2 Đề xuất — 0 hệ quả với dữ liệu cũ

```php
// Loại bỏ hàng hoá làm dịch vụ (giữ hàng chưa có loại cũ — hàng tạo từ HRM)
$products = $products->where(function ($q) {
    $q->whereNull('products.product_type')->orWhere('products.product_type', '!=', 'service_product');
});
```

- **30 hàng dịch vụ (16 status 1) vẫn bị loại như cũ**; DB hiện **0** hàng `product_type IS NULL` ⇒ kết quả popup với dữ liệu cũ **không đổi một dòng**.
- Thay phương án (a) cũ "bỏ hẳn điều kiện" (`hop-dong-tuong-thich-erp.md` BB-6) — phương án đó mới cần khách xác nhận 30 hàng dịch vụ lọt popup. **Đề xuất bỏ câu hỏi đó.**
- Ghi thêm tiền tố `products.` (bản gốc viết trần `product_type` — an toàn hiện nay vì không JOIN bảng nào khác có cột trùng tên, nhưng nhánh `price_type` có JOIN 4 bảng).

### 3.3 Lọc theo enum cũ khác — hàng HRM KHÔNG BAO GIỜ khớp (có chủ đích, để sau)

| File:dòng | Ảnh hưởng hàng HRM |
|---|---|
| `SearchController.php:557, :992, :1435` (`is_service_quotation == 'true'` ⇒ chỉ `accessories`, `lubricant`) | **không chọn được trong Báo giá dịch vụ** (14 file view truyền cờ) |
| `SearchController.php:916-917, :1358-1359` (phụ kiện theo thiết bị) | không hiện trong popup phụ kiện của thiết bị |
| `Jobs/ResetProductPriceWhenZeroInventory.php:67` (lọc `product_type`) | — job, xem N5 |
| `Services/Reports/MarketCommodity*ReportService` (~26 chỗ `where('p.product_type', $type)`) | chỉ khi người dùng lọc theo loại |
| `Product.php:1821, :7424` (`$filter->product_type(s)`) | chỉ khi lọc |

⇒ thuộc roadmap §5-4 (3 cờ nghiệp vụ thay `product_type`), **không thuộc 2-D**. Câu Q4 để user xác nhận.

---

## 4. Các giả định khác của ERP

### 4.1 `firstOrFail` đơn vị / giá — G2 đã đủ

- Đếm lại (multi-line, `ProductUnit|ProductUnitPrice::… ->firstOrFail|findOrFail`): **53 lệnh / 27 file** (48 `ProductUnit`, 5 `ProductUnitPrice`). Con số "~290" cũ gồm cả chỗ gọi gián tiếp (`getPriceByUnitAndType`, `base_unit`, `base_price`…).
- Điều kiện gặp: `is_base = true` (`Product.php:1389, :1400`), `unit_id` = ĐVT của chính hàng (vd `WarehouseImportsController.php:732`, `PriceCalculate.php:415`, `FirmContractTabProduct.php:221`), `price_type_id` = 1 hoặc `$type` (`Product.php:1403, :1415`). `price_types` có đúng **6 dòng** (1–6).
- Popup `SearchController:399-413` (`price_type`) INNER-lọc `pu.is_base = true AND pp.price_type_id = ?` ⇒ G2 6 dòng/ĐVT ⇒ đủ.
- ⇒ **G2 đủ, không cần thêm.** Lưu ý ngoài phạm vi: giá 0 hiện thẳng ở popup (H1'': chỉ bật HRM thật khi có Tính giá).

### 4.2 `product_cate` NULL — không nổ

- PHP: `RootOrderRequest::getProductCateName` `:469` `if (!$product_cate) return ''`; `Product.php:6611` `?? ''`; mọi bộ lọc bọc `if (!empty($request->product_cate…))`; `json_decode(null)` PHP 7.4 trả null không cảnh báo.
- JS: `ProductByManufactureDetail.blade.php:27`, `StockTransferGroupProductReport.blade.php:15` có kiểm `Array.isArray`. Riêng `products/editPrices.blade.php:661-662` (`JSON.parse(null).map`) ⇒ lỗi console + ô *Loại hàng hoá* trống ở màn **Cập nhật nhanh giá** (route sống `web.php:586`) — 🟡, màn ghi giá, chờ quyết định chặn (Phần A / Phase 8).

### 4.3 `product_template_id` NULL (N6) — không nổ

`ProductUnit.php:70`, `ProductUnitPrice.php:114` dùng toán tử 3 ngôi; 16.077 hàng cũ đã NULL. Chỉ ảnh hưởng: `Jobs/SyncProductUnitPricesToCrm.php:38, :57` `whereNotNull('product_template_id')` + cron `sync:crm` (`Console/Kernel.php:128`, 19:30) ⇒ hàng HRM **không sang CRM**. Để sau.

### 4.4 Cột chung `min_stock_qty` / `guarantee*` (N1) — không nổ, sai nghiệp vụ

- Grep thô: `min_stock_qty` 42 file (`app`+`resources`), `->guarantee_type` 47 file / 87 dòng; số đã lọc của §24 vẫn là **29 + 42 file**.
- Không nổ: accessor bảo hành đều kiểm rỗng (`Product.php:273`, `RootContractProduct.php:136`, `BaseQuotationProduct.php:107`…); `getGuaranteeDayAttribute` `Product.php:805-819` `default: return 0`; `HandoverAcceptanceRecord.php:804` tương tự. Chép sang chứng từ (23 lệnh `->guarantee = $product->guarantee`, vd `Quotation.php:1077`, `Contract.php:2563`, `FirmContract.php:1492`) — 2.005 hàng ERP cũ đã NULL nên đường này đã chạy quen; các phiếu mua hàng bắt nhập tay (`PIStoreRequest.php:41` `'products.*.guarantee' => 'required'`).
- Hệ quả thật: hàng HRM ⇒ **bảo hành 0 ngày** trên chứng từ (serial hết bảo hành ngay khi bàn giao), **không bao giờ vào danh sách dưới tồn tối thiểu** — dù công ty đã khai ở tab Quản trị (dòng `product_company_coefficients`).
- Đề xuất (khi làm): ERP đọc dòng (hàng × công ty của chứng từ) trước, lùi về cột chung — 1 accessor/helper dùng chung + sửa 29 + 42 file. **Khối lượng lớn ⇒ câu Q1.**

### 4.5 `company_id`

Không nổ. Lệch ngữ cảnh: HRM gán `company_role`, ERP lọc/nhân hệ số theo `Auth::user()->info->company_id` (vd `SearchController:403`, `Product.php:1210`). Đo: 3/1.119 nhân viên có `company_role ≠ company_id`. Ghi nhận, không xử lý ở 2-D.

### 4.6 Cron đưa giá về 0 (N5) — ⚠️ đính chính

- Lệnh theo lịch là **`ResetProductPriceWhenZeroInventoryCommand`** (`Console/Kernel.php:107`, 14:30 hằng ngày) — lọc `products.company_id` + **`product_cate` JSON** (`:79-85`) ⇒ hàng HRM (`product_cate` NULL) **bị bỏ qua**.
- Bản Job `Jobs/ResetProductPriceWhenZeroInventory.php:65-68` lọc theo **`product_type`** (không phải `product_cate`) — cũng bỏ qua hàng HRM.
- DB local: cấu hình `companies.reset_price_when_zero_inventory_product_types` **NULL ở cả 8 công ty** ⇒ local không chạy gì; production chưa đo.
- Hàng HRM hiện giá 0 (G2) tới Phase 8 ⇒ chưa có gì để đưa về 0. **Để sau (Phase 8).**

### 4.7 Khoá theo công ty status 4 (N8)

- ERP không biết `product_company_coefficients.status`: popup chỉ lọc `products.status != 0` (`SearchController:396`). Hàng công ty X *Ngừng kinh doanh* vẫn chọn được ở chứng từ ERP của X.
- Sửa tối thiểu: 4 hàm SearchController thêm `whereNotExists(pcc.product_id = products.id AND pcc.company_id = info->company_id AND pcc.status = 4)` ⇒ 4 chỗ / 1 file. Chưa chặn đường `getData` / các API khác ⇒ chỉ chặn ở bước chọn.
- Cùng loại, đã chấp nhận ở G1: hàng *Đang nhập thông tin* (status 1) chọn được ngay ở ERP.

### 4.8 Lặt vặt (🟡, không nổ)

| Chỗ | Ảnh hưởng |
|---|---|
| `Product.php:901-907` `getAttributeProductAttribute` INNER JOIN `unitteches` | thuộc tính HRM không có đơn vị (`ProductRequest.php:88` cho null) không hiện ở ERP (ERP cũ có 20/51.128 dòng như vậy; form ERP bắt `unittech_id` khi tick — `Product.php:327, :438` — HRM thì không) |
| `products/show.blade.php:145-148` | `group_id` null ⇒ gọi `/admin/attributes/byGroup/null` — trả rỗng (`AttributesController@getByGroupId :28`), không nổ |
| K2/G4 | dòng `coefficient = 1` ⇒ giá popup làm tròn nghìn — đã chấp nhận |

---

## 5. Ma trận

| # | Vấn đề | Mức | File · chỗ | Đề xuất | 2-D hay sau |
|---|---|---|---|---|---|
| M1 | N7-A/A' SearchController popup | 🔴 500 | 1 file · 7 dòng | `?? 'Chưa xác định'`, `?? 0` | **2-D** |
| M2 | N7-B `Product::getDataAttribute/getData` (route getData 71 view) | 🔴 500 | 1 file · 6 dòng | `??` | **2-D** |
| M3 | N9 lọc `!= service_product` | 🔴 vô hình | 1 file · 4 dòng | `whereNull OR !=` | **2-D** |
| M4 | N7-C in tem (`barcode` + JS + 2 INNER JOIN) | 🔴 500 / JS | 3 file · 11 + 2 + 2 dòng | `??` + mặc định Q2; `leftJoin` | **2-D** |
| M5 | N7-D bàn giao nghiệm thu | 🟠 500 | 3 file · 3 dòng | `optional()` / `$group &&` | **2-D** |
| M6 | N7-E export doanh thu theo hàng | 🟠 500 | 1 file · 1 dòng | `??` | **2-D** |
| M7 | N7-F màn Dịch vụ thêm hàng | 🟠 JS | 1 file · 4 dòng | nhóm giả "Chưa xác định" | **2-D** |
| M8 | INNER JOIN `groups` ở 2 báo cáo | 🟡 thiếu dòng | 2 file · 5 dòng | `leftJoin` | ⭐ sau (hoặc 2-D nếu rẻ) |
| M9 | N8 khoá status 4 không chặn ở ERP | 🟡 nghiệp vụ | 1 file · 4 chỗ | `whereNotExists` | **Q3** |
| M10 | N1 bảo hành / tồn tối thiểu theo công ty | 🟡 nghiệp vụ | 29 + 42 file | helper đọc dòng công ty | **Q1** (⭐ sau) |
| M11 | Enum `product_type` cũ (báo giá dịch vụ, phụ kiện thiết bị) | 🟡 không chọn được | 1 file · 5 chỗ | 3 cờ §5-4 | **Q4** (⭐ sau) |
| M12 | N5 cron reset giá | ⚪ (giá đang 0) | 2 file | lọc theo dòng công ty | sau — Phase 8 |
| M13 | N6 CRM | ⚪ | job `sync:crm` | | sau |
| M14 | `editPrices` JSON.parse(null) | 🟡 console | 2 file (products + product_templates) | `JSON.parse(x \|\| '[]')` | sau (màn giá — Phần A) |
| M15 | `firstOrFail` ĐVT/giá | ✅ | 27 file · 53 lệnh | G2 đã đủ | — |

**Phạm vi 2-D tối thiểu (M1–M7): 28 dòng PHP + 6 dòng JS + 4 dòng N9 = 38 dòng, 11 file ERP.** Không migration, không đụng DB.

---

## 6. Nghiệm thu "ERP không vỡ"

### 6.1 Rà lại 14 bước `hop-dong-tuong-thich-erp.md` §3

| Bước | Còn áp dụng? |
|---|---|
| 1 (danh sách ERP thấy hàng), 2 (popup tìm thấy), 4 (lập báo giá/xuất kho), 5 (người tạo/cập nhật) | ✅ giữ |
| 3 (mở màn Sửa ERP) | ❌ route sửa bị chặn (Phần A) |
| 6–10 (giá + duyệt giá + quyền `Quản lý giá`) | ❌ HRM không ghi giá (G2, H1'') — chuyển sang Phase 8 |
| 11–13 (đếm 12 bảng, mã rỗng, mã trùng) | ✅ giữ (SQL) |
| 14 (tạo đồng thời HRM + ERP) | ❌ ERP hết tạo hàng sau khi chặn route |

### 6.2 Bộ nghiệm thu đề xuất cho 2-D

**Dữ liệu cần** (tạo qua API HRM worktree :8031 trên `hrm_erp`, dọn sau khi kiểm):
- **H1**: hàng HRM tạo, VAT **0%**, 2 ĐVT, không xe — chạm A, A', B.
- **H2**: hàng HRM tạo, VAT 10% — đối chứng.
- **H3**: H1 được công ty khác lấy về rồi **khoá (status 4)** — chỉ khi làm N8.
- **P1**: 1 phiếu nhập kho ERP chỉ có H1 (in tem — M4); **P2**: 1 biên bản bàn giao nghiệm thu có H1 (M5).

| # | Kiểm | Đạt khi | Tự động? |
|---|---|---|---|
| K1 | grep tĩnh mục 2.5 trên 9 file | rỗng | ✅ shell |
| K2 | SQL mô phỏng WHERE popup: `status != 0 AND (product_type IS NULL OR product_type <> 'service_product')` | H1, H2 có; 30 hàng dịch vụ không có; số dòng hàng cũ không đổi | ✅ SQL |
| K3 | SQL bất biến G2: mỗi ĐVT của H1/H2 có đúng 6 dòng giá, đúng 1 ĐVT `is_base` | đúng | ✅ SQL |
| K4 | HTTP `GET modal_data/searchProduct`, `searchProductStockBuyer`, `searchProduct2` (có/không `price_type` 1–6, từ khoá = mã H1) | 200, có H1, cột Nhóm = "Chưa xác định", `vat_percent` = 0 | ✅ Playwright `request` (cần phiên đăng nhập ERP) |
| K5 | HTTP `GET products/{H1}/getData`, `getDataForPriceAsking` | 200 | ✅ như K4 |
| K6 | HTTP `GET products/barcode?…` cho H1 + mở màn in tem P1 | 200; nút in hiện; không lỗi console | ✅ Playwright UI |
| K7 | Lưu/sửa P2 + mở danh sách sản phẩm bàn giao | không 500 | ✅ Playwright UI |
| K8 | Xuất *Doanh thu theo hàng hoá* có H1 | file ra | 🟡 bán tự động |
| K9 | Màn Dịch vụ thêm H1 | không lỗi console | ✅ Playwright UI |
| K10 | 3 màn đại diện chọn H1 trong popup (báo giá, phiếu xuất kho, hợp đồng) | chọn được, không lỗi console | ✅ Playwright UI |
| K11 | Bước 11–13 cũ (đếm bảng, mã rỗng/trùng) | như hợp đồng | ✅ SQL |

**Điều kiện để tự động được** (đều cần hỏi riêng, không tự làm):
1. ERP local chạy **nhánh gop_db** (checkout hiện ở `develop_01`) — worktree riêng hoặc checkout.
2. ERP local trỏ DB **`hrm_erp`** — `.env` hiện `DB_DATABASE=erp2326`; `bootstrap/cache/config.php` hiện **không có** (memory cũ cảnh báo cache trỏ production ⇒ kiểm lại trước khi chạy).
3. Tài khoản ERP có quyền xem các màn trên + 1 tài khoản **không quyền** (memory: luôn test cả ca không quyền — ở đây chỉ cần chứng minh không 500).
4. Skill `playwright-setup` có mục ERP AngularJS/Blade — dùng khuôn đó.

---

## 7. Câu hỏi cho user (chỉ nghiệp vụ chưa chốt)

| # | Câu | Phương án · hệ quả |
|---|---|---|
| Q1 | **N1 (bảo hành / tồn tối thiểu theo công ty) làm ở 2-D hay để sau?** | ⭐ **(a) để sau, trước merge prod** (đúng chốt G5 + tiền đề #9): 2-D gọn (~38 dòng). Hệ quả tới lúc đó: chứng từ ERP của hàng HRM có **bảo hành 0 ngày**, hàng HRM không vào báo cáo dưới tồn tối thiểu. · (b) làm ở 2-D: thêm 29 + 42 file ERP, 2-D thành đợt lớn nhất |
| Q2 | **Mẫu tem mã vạch của hàng HRM tạo** (ERP lấy `groups.barcode_template_type`, hàng HRM không có nhóm) | ⭐ **(a) lấy theo Tính chất hàng hoá** (`product_natures.barcode_template_type` — cột đã có ở cây mới, suy qua Loại SP → Họ → Nhóm chức năng → Tính chất): đúng hướng bỏ `groups`; ERP phải JOIN thêm 3 bảng ở `barcode` + `WarehouseImport`. Lưu ý: local `product_natures` mới có 1 dòng rác (giá trị 1). · (b) mặc định **mẫu 1**: sửa ít nhất; hàng cần mẫu 2/3 (nhập ngày SX/HSD — 389/893 nhóm) in sai mẫu tới khi có cột thật. Ingredient/warning/user_manual để trống ở cả 2 cách |
| Q3 | **N8 (hàng Ngừng kinh doanh theo công ty vẫn chọn được ở ERP) làm ở 2-D hay để sau?** | ⭐ **(a) làm ở 2-D, chỉ ở popup** (4 chỗ / 1 file): rẻ; đường `getData`/API khác vẫn không chặn. Lưu ý ERP xác định công ty bằng `info->company_id` (3/1.119 nhân viên lệch `company_role`). · (b) để sau: tới lúc đó khoá ở HRM **không có tác dụng gì bên ERP** |
| Q4 | **Hàng HRM tạo không chọn được trong *Báo giá dịch vụ* và popup *phụ kiện theo thiết bị*** (ERP lọc cứng `product_type IN (accessories, lubricant, …)`, hàng HRM `product_type` NULL) | ⭐ **(a) chấp nhận, để tới đợt 3 cờ nghiệp vụ thay `product_type`** (sổ chốt §5-4): báo giá dịch vụ tạm chỉ chọn được hàng ERP cũ. · (b) xử lý ở 2-D: phải chốt luật mới "hàng nào được vào báo giá dịch vụ" — chưa có cờ để lọc |
| Q5 | **Hàng HRM có nằm trong diện "đưa giá về 0 khi hết tồn" (N5) và đồng bộ CRM (N6) không?** | ⭐ **(a) để Phase 8 (Quản lý giá)**: hiện giá hàng HRM = 0 nên N5 chưa có tác dụng; CRM chưa nhận hàng HRM. · (b) chốt ngay luật lọc theo dòng công ty — chưa có dữ liệu giá để kiểm |
