# Giá theo công ty (Hướng B) — Khảo sát phía ERP (09/10/2026)

> **Khảo sát CHỈ ĐỌC**: không sửa source, DB chỉ SELECT, không artisan, không checkout/stash/commit.
> **Mã ERP:** worktree `websites/wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi` (= `gop_db` + 2-D1), HEAD `b2f1761789`.
> Mọi `file:dòng` dưới đây theo worktree này. PHP 7.4.33, Laravel ^6.2 (`composer.json`).
> **DB:** `hrm_erp` local (bản chụp ERP tới 15/09/2026). "6 tháng" = 15/03 → 15/09/2026, "12 tháng" = từ 15/09/2025.
> **Đọc trước:** `../2d-erp-khong-loi/khao-sat-c-gia.md` (L1–L10, §2.2, HĐ1–HĐ10), `../2d-erp-khong-loi/d2-khao-sat-be.md`,
> `../man-danh-muc-hang-hoa/design.md` §19 §24 §25, `../man-danh-muc-hang-hoa/ton-chot-truoc-code.md` A4/A5, `../2d-erp-khong-loi/d1-plan.md`.
> **Phạm vi:** chỉ ERP. Phía HRM có file riêng `khao-sat-du-lieu-hrm.md` (agent khác).
> Ký hiệu: `PC` = `app/Http/Controllers/ProductsController.php` · `SC` = `app/Http/Controllers/Common/SearchController.php` ·
> `P` = `app/Product.php` · `web` = `routes/web.php` · `pcc` = `product_company_coefficients` · `upp` = `product_unit_prices`.

---

## 0. Tóm tắt

1. 🔴 **Chốt A4 "dữ liệu cũ gán về công ty tạo" sẽ làm chi nhánh mất giá ngay ngày bật.** Chi nhánh/công ty con gần như
   chỉ bán hàng do Cty 1 tạo. Trong 6 tháng, các công ty dùng **8.097 cặp (mã × công ty) thuộc mã của công ty khác** (Cty 4
   có 5.069/5.644 mã, Cty 3 có 1.875/1.888, Cty 8 có 566/566, Cty 2 có 411/411). Riêng dòng hàng của chứng từ công ty 4: báo giá
   40.802 dòng, HĐ 7.069 dòng, đề nghị xuất 20.778 dòng, tất cả trên mã của công ty khác. Nếu chỉ gán về công ty tạo thì Cty
   2/3/4/8 có **0 dòng giá** cho các mã này: popup hiện giá trống, còn `getPriceByUnitAndType` ném `firstOrFail` (404/500) ở **69 chỗ
   gọi**. ⇒ câu **G1/G2**. ⭐ Đề xuất: **nhân bản có chọn lọc**. Gán cho công ty tạo, rồi nhân thêm cho mỗi cặp (mã × công ty)
   đang dùng: **12.574 cặp, ≈ 78.399 dòng giá** (+30%, so với 2,1 triệu dòng nếu nhân đủ 8 công ty). Giá chép sang = giá chung ×
   hệ số `pcc`, làm tròn giống hệt `getData`. Như vậy ngày bật không ai thấy giá đổi, và **hệ số được "nướng" sẵn vào giá**, bỏ
   được ngay.
2. **Kiểm kê đọc giá ERP (ngoài màn hàng hoá/hàng gốc/ProductInfo)** gom được vào **6 đường chung**:
   - (R1) `getData`/`units_info`: **1 hàm lõi** phủ 93 lời gọi AJAX / 71 view + 61 chỗ `->data` / 37 file + 31 chỗ `units_info` / 20 file.
   - (R2) `getPriceByUnitAndType`: 69 chỗ / 42 file (26 lấy `.price`, 37 lấy `.sale_max_percent`).
   - (R3) `base_price`: 13 chỗ / 9 file.
   - (R4) `getPriceOfProducts`: 1 endpoint / 13 view.
   - (R5) popup `SearchController`: 7 khối join trong 1 file, có cả API mà HRM đang gọi.
   - (R6) hệ số `pcc` nhân lúc đọc: **17 chỗ code** (nằm trong R1/R4/R5 + 6 chỗ "kiểm lệch giá").

   Ngoài 6 đường đó còn **15 file SQL/quan hệ đọc thẳng** `upp` và **12 file đọc giá vốn/giá mua ngoài** trên `product_units`.
   ⇒ Sửa **3 hàm lõi trong `P` + `SC` + `getPriceOfProducts`** là phủ được ~90% số màn. Phần còn lại là ~30 file đọc lẻ. Ước
   lượng ERP **≈ 55–65 file**, phần lớn mỗi file 1–5 dòng (mục 6.3).
3. 🔴 **"Công ty nào" là chỗ dễ sai nhất.** Hôm nay mọi đường đọc lấy công ty của **người đang đăng nhập**
   (`Auth::user()->info->company_id`). Có **3 loại ngữ cảnh lệch** giữa công ty người dùng và công ty chứng từ:
   - (a) Load lại chứng từ để sửa/duyệt/hạch toán (vd Ban điều hành Cty 1 duyệt HĐ của SG).
   - (b) Cron/queue: không có `Auth`.
   - (c) 5 bảng chứng từ **không có `company_id`**: `contracts`, `project_quotations`, `order_requests`, `combo_campaigns`,
     `tmp_products`. Phải suy ra từ người lập.

   Cần hàm phân giải công ty **tường minh**, không dùng global scope (mục 5).
4. 🔴 **Phiếu tính giá đang ghi giá CHUNG từ phiếu của công ty khác.** Trong 6 tháng có **546 phiếu Cty 4, 113 phiếu Cty 3, 8 phiếu
   Cty 8, 2 phiếu Cty 2** tính giá cho hàng Cty 1. Gần như toàn bộ do NV 1027 (Cty 1) lập (`price_calculates.company_id` = công ty
   yêu cầu, `PriceCalculateController.php:149`). Hôm nay các phiếu này **ghi đè giá TPE**. `PriceCalculate::updatePriceWithApproval`
   chọn công ty theo `products.company_id` (`app/Model/Order/PriceCalculate.php:384`), không theo phiếu. ⇒ câu **G3**.
5. ✅ **Giá vốn kho (hạch toán 632/156) KHÔNG đọc `product_units.cost_price`.** Giá xuất = chênh `value_before − value_after`
   của sổ kho kế toán (`app/Model/Warehouse/ProductExportDetail.php:50-70`, `ProductTransfer.php:280-282`). Nhập kho cập nhật giá vốn
   đã tắt sẵn (`app/Model/Warehouse/ProductImport.php:1189, 1199-1210`).
   ⚠️ Nhưng **"Hạch toán hỗ trợ" / hiệu quả hợp đồng dự án & đại lý** đọc giá vốn **sống** từ `product_units.cost_price` lúc mở/duyệt
   (`ProjectQuotationGroupProduct:24-31`, `ProjectQuotation:1848, 1864-1890`, `ProjectAnalysis:472, 500`, `ProjectAnalysisService:33`,
   `FirmContractTabProduct:263`), rồi **lưu số** vào `support_accounting`/`project_analysis_*`. Báo cáo lợi nhuận dùng nó làm giá
   nhập dự phòng. ⇒ câu **G5**.
6. ⚠️ **Lệch sẵn có:** `getPriceByUnitAndType` **không nhân hệ số** (`P:1441-1452`), trong khi `getData`/popup có nhân. Do đó 26 chỗ
   lấy `.price` (khuyến mại trên báo giá/HĐ, đơn mua, chuyển kho, xuất ghép/tách…) hôm nay đang trả **giá TPE thô** cho HP/Vinh/SG.
   Sau khi giá đã nướng hệ số, các chỗ này **đổi số** với 846 mã có hệ số ≠ 1 ⇒ câu **G9**.
7. **Chiến lược đề xuất (mục 5):**
   - Lớp truy cập giá tập trung, nhận `companyId` tường minh.
   - Bật **theo cờ, từng công ty**.
   - Seed chọn lọc theo công thức hệ số, kèm **lệnh so khớp chỉ đọc**.
   - Đọc cũ vẫn lọc "công ty tạo" khi cờ tắt, nên trật tự bắt buộc là **sửa HẾT đường đọc (ERP + HRM) TRƯỚC khi seed dòng thứ 2**.
     Còn sót 1 reader thì nó đọc trùng dòng / `first()` ngẫu nhiên, sai mà không báo.

---

## 1. Kiểm kê ĐỌC giá

> Đã **lọc bỏ cột trùng tên**: grep thô `cost_price|buy_price` ra **102 file `app/` + 83 view**, nhưng 24 bảng có cột trùng tên
> (`firm_support_accounting`, `service_*`, `wr_*`, `price_calculate_products`, `product_template_units`, `product_info_units`,
> `tmp_product_units`, `inventory_audit_report_details`…, đo `information_schema` 09/10). Chỉ **12 file** ngoài màn hàng hoá thật sự đọc
> `product_units.cost_price/buy_price` (R8). Cũng loại khỏi đếm các file **thuộc diện chặn/giữ nguyên ở 2-D1**: `ProductsController`
> (trừ các route còn mở), `Product2Controller`, `ProductTemplatesController`, `ProductInfoController`, `ProductApprovesController`
> (đường GHI, xem mục 2), `ExcelImports/*`, `Jobs/{GenerateProduct,CreateTemplateProductMissing,CreateProductUnitsAfterMapping,createTemplateProduct}`,
> `ProductTemplate.php`, `ProductInfo.php`, `TmpProduct*`.
>
> Cột **Công ty nên dùng**: **CT** = công ty của chứng từ (cột `company_id` của chứng từ, hoặc suy từ người lập nếu bảng không có cột) ·
> **ND** = công ty người dùng đang thao tác · **Tham số** = đã nhận `company_id` từ ngoài. Cột **Biến**: có sẵn biến công ty tại chỗ không.
> **Mức sửa**: S = đổi 1–3 dòng · M = đổi chữ ký/truyền thêm tham số · L = viết lại query.

### R1 — `getData` / `units_info` (đường chính khi CHỌN hàng vào chứng từ)

| # | Chỗ | Nghiệp vụ | Công ty nên dùng | Biến | Mức |
|---|---|---|---|---|---|
| R1.1 | `P:1404-1420` `getUnitsInfoAttribute` | mọi ĐVT + `prices` (6 giá) + `expected_prices` > hôm nay; **kèm luôn `product_units.*` ⇒ lộ `cost_price`/`buy_price` cho mọi màn** | theo tham số | ❌ (accessor không nhận tham số) | **M**: thêm `unitsInfoFor(int $companyId)`, accessor cũ gọi với công ty ND |
| R1.2 | `P:1242-1310` `getDataAttribute` | nhân hệ số `pcc` của **ND**, làm tròn nghìn (`:1244-1258`) | ND khi lập mới; CT khi load lại | `Auth` | **M** |
| R1.3 | `P:1312-1376` `getData($company_id)` | như trên, nhận công ty (mặc định ND) | Tham số | ✅ | S |
| R1.4 | `PC:3145-3200` `getData` (web `:599`) | **93 lời gọi / 71 view** (`/admin/products/${id}/getData`): báo giá, HĐ, đơn hàng, phụ lục, khuyến mại, combo, kho… | ND (= CT khi lập) | `Auth` | 0 (đi qua R1.2) |
| R1.5 | `->data` phía server: **61 chỗ / 37 file**. Vd `Model/Sale/QuotationProduct.php:43-47`, `BaseQuotationProduct.php:99`, `RootContractProduct.php:147`, `ContractPromotion.php:95`, `Firm/Contract/FirmContractPromotion.php:95`, `Firm/Quotation/FirmQuotationPromotion.php:95`, `Firm/Contract/FirmContractInformationOrder.php:40`, `Order/RootOrderRequestProduct.php:66`, `Order/{InlandOrderRequestProduct,InlandOrderRequestProduct2,InlandOrderRequestNewProduct,OrderRequestProduct2}.php`, `Warehouse/{ProductExportRequestDetail:168, ProductTransferRequestProductDetail:14}`, `Order/{InlandBuyContract,InlandBuyContractNew,InlandBuyContractAnnex(2),BuyContract2}.php` (hàng KM), `Controllers/Order/{PurchaseInvoiceController:660, InlandPurchaseInvoiceController:639, FirmWarrantyConfirmController:552}`, `Warehouse/ProductTransfersController:335`, `CustomerManagerController:580`, `Customercare/WarrantyRepairInformationRequestsController:282`, `Customers/WarrantyRepairHandleRequestProduct:96,176`, `Sale/QuotationTemplate:78`, `PC:3347` (`getDataForPriceAsking`) | **LOAD LẠI chứng từ** để hiện form sửa/xem: đổ lại `units` + giá hiện hành | **CT** | ✅ hầu hết (`$this->parent`/`$object`) | S–M: `->getData($ct)` thay `->data` (~37 file) |
| R1.6 | `Model/Sale/ComboCampaign.php:147` `getData($company_id)` | combo | Tham số | ✅ | 0 |
| R1.7 | `units_info` trực tiếp: **31 chỗ / 20 file** (`Order/{RootOrderRequest:215,311, OrderRequest:62,84, OrderRequest2:165, InlandOrderRequest:121, InlandOrderRequestNew:147, InlandOrderRequest2:127}`, `Warehouse/{ProductExportRequest:1418, PrepickCancelRequest:55, JoinExportRequest:323}`, `Customers/WrServiceQuotation` ×9, `Target/TargetDevelopProduct:139`, `PositionInventoryResultsController:699`, `SelfInventoriesController:577`, `TargetDevelopProductController:429`, `CustomerManagerController:547`, `getDataForInventory/ForJoin` `P:6501-6560, 1379-1400`) | phần lớn chỉ cần **danh sách ĐVT**; WrServiceQuotation lấy giá (`units[0]->prices[0]`) | CT nếu dùng giá; không cần nếu chỉ lấy ĐVT | ✅ | S. Nên tách `unitsOnly()` không kèm giá |

**Phía FE (Angular trong Blade):** 40 view/class JS đọc `units[].prices[]`, 13 view đọc `expected_prices`. Tất cả **ăn JSON của R1**
⇒ **không phải sửa view nào** nếu giữ nguyên hình dạng JSON (`units[].prices[].{price_type_id,price,coefficient,sale_max_percent,expected_prices[]}`).
Không view chứng từ nào đọc `units[].cost_price` (đã grep, chỉ màn hàng hoá/PTG).

### R2 — `Product::getPriceByUnitAndType($pid, $uid, $type)` (`P:1441-1452`, `firstOrFail` cả ĐVT lẫn dòng giá)

**69 chỗ / 42 file**: 26 chỗ lấy `.price`, 37 chỗ lấy `.sale_max_percent` (ĐMGG). **Không nhân hệ số.**

| Nhóm | Chỗ (file:dòng) | Nghiệp vụ | Công ty nên dùng | Biến |
|---|---|---|---|---|
| R2a ĐMGG lúc **lập/sửa** chứng từ bán | `Contract.php:2566,2619`; `Sale/{ContractAdditionAnnex:196,388, ServiceContractAdditionAnnex:240, ServiceContract:967, ProjectContract:745,774, RuleContract:106, RuleContractAnnex:79, ProjectQuotationTab:84, ProjectQuotationGroup:58, ProjectAnalysis/ProjectAnalysisGroup:71}`; `Firm/{Quotation/FirmQuotation:630, Contract/FirmContract:1495}`; `Services/Sale/Firm/{Contract/FirmContractService:704,846,958, Contract/ZTFirmContractService:659,741, Order/PrincipleOrderService:287, Order/ZTPrincipleOrderService:285}`; `Customers/{WrServiceQuotation ×8, WrServiceContract:3001}`; `Firm/HrmQuotationContractController:90` | chép `sale_max_percent` vào dòng chứng từ | **CT** | ✅ (`$this`, `$contract`, `$firm_contract`) |
| R2b ĐMGG lúc **hạch toán / quyết toán** (đọc SỐNG) | `Services/Sale/SupportAccountingService:175,434`; `Services/Sale/SettlementContractService:860` | tính chiết khấu vượt định mức khi hạch toán hỗ trợ / quyết toán HĐ | **CT** (đọc sống ⇒ số đổi khi giá đổi, xem mục 3) | ✅ |
| R2c Giá bán chép vào dòng **hàng khuyến mại** | `Contract.php:2546`; `Sale/ContractAdditionAnnex:176`; `Firm/Quotation/FirmQuotation:609,664`; `Firm/Contract/FirmContract:1474` | KM: giá = giá loại `price_type` của chứng từ, 100% giảm | **CT** | ✅ |
| R2d **Kiểm lệch giá** (có nhân hệ số tay) | `Requests/Sale/Firm/Order/PrincipleOrderStoreRequest:117-118`; `ZTPrincipleOrderStoreRequest:68-69`; `Services/Sale/Firm/Order/PrincipleOrderService:397-404`; `Warehouse/ProductExportRequestsController:2183-2188`; `CRM/Warehouse/ProductExportRequestsController:1053-1054`; `Warehouse/BorrowSellRequestsController:676-677` | đơn hàng nguyên tắc / đề nghị xuất / mượn bán: chặn nếu giá dòng ≠ giá niêm yết × hệ số **của ND** | **CT** (`$parent->company_id`, `$firmContract->company_id`) | ✅ |
| R2e Giá niêm yết cho **mua hàng / kho** (loại 1) | `Order/{OrderRequest:182, OrderRequest2:298, InlandOrderRequest:542, InlandOrderRequest2:232, InlandOrderRequestNew:261, RootOrderRequest:516, OrderSummary:399, OrderSummary2:205,881, InlandOrderSummary2:644, PriceAskingRequest:721}`; `Services/RootOrderRequests/RootOrderRequestService:56,352`; `Order/InlandOrderSummaryNewController:429`; `Warehouse/ProductTransferRequest:294`; `Warehouse/ProductExportsController:766` (xuất ghép/tách; ⚠️ truyền nhầm `unit_coefficient` làm `unit_id`, lỗi sẵn) | tham khảo / chép `price`, `listed_price` | **CT** (đề nghị mua của công ty nào) | ✅ phần lớn (`root_order_requests`, `product_transfer_requests` có `company_id`; `order_requests` **không có** ⇒ suy từ người lập) |

⇒ Đổi chữ ký thành `getPriceByUnitAndType($pid, $uid, $type, ?int $companyId = null)`. `null` = công ty ND, nên **0 file phải sửa
để chạy được**. Nhưng **~25 chỗ R2b/R2c/R2d + phần R2a ở luồng duyệt** cần truyền **CT** thì mới đúng khi người thao tác khác công ty.

### R3 — `base_price` (`P:1431-1439`, `firstOrFail`, KHÔNG nhân hệ số) — 13 chỗ / 9 file

`CustomerManagerController:584`, `Customercare/WarrantyRepairInformationRequestsController:286`, `Customers/WarrantyRepairHandleRequestProduct:100,180`
(giá bán gợi ý khi bảo hành/sửa chữa) · `Warehouse/SelfInventoriesController:624`, `Warehouse/SelfInventory:688` (kiểm kê tự làm: `sell_price`) ·
`Warehouse/PrepickTransfer2Controller:471`, `Warehouse/PrepickTransfer2:424`, `Warehouse/PrepickExtendRequest:228` (tổng tiền giữ hàng ⇒ hạn mức) ·
`Sale/QuotationTemplate:234,243,309,318` · `P:6640` (Excel danh sách HH) + 2 lần trong `getData` (`P:1298, 1368`).
Công ty: **CT** (giữ hàng/kiểm kê có `company_id`); bảo hành: công ty của phiếu. Mức S (accessor → hàm có tham số).

### R4 — `PC@getPriceOfProducts` (`PC:3569-3597`, web `:46`)

13 view: `orders/{inland_buy_contract2,inland_order_request2,inland_order_request_new,order_request2,order_requests}/{formJs,show}`,
`orders/root_order_requests/formJs`, `orders/price_asking_requests/show`, `warehouse/product_transfer_requests/formJs`. Gọi R2, rồi nhân hệ số
**ND**, làm tròn nghìn **chỉ khi ≥ 1.000** (khác `getData` luôn làm tròn). Công ty: ND (lúc lập), có thể nhận thêm `company_id` từ request. Mức S.

### R5 — Popup chọn hàng `SearchController` (338 màn) + API HRM

| Khối | Dòng | Ghi chú |
|---|---|---|
| `searchProduct` có `price_type` | `SC:444-462` | join `pu.is_base=1` + `pp.price_type_id=?` + `pcc` của **ND**; `CASE pcc… ROUND(pp.price*pcc.coefficient/1000)*1000` |
| `searchProduct` `for_update_list_products` | `SC:465-478` | giá loại 1 |
| `searchProductStockBuyer` | `SC:967-985`, `:990-1001` | như trên |
| `searchProductStockBuyerApi` | `SC:1335-1444` (`:1410-1427`, `:1433-1444`) | nhận **`company_id` tham số** (bắt buộc). Được gọi bởi `apiSearchProductStockBuyer` (`routes/api.php:35`) **và** `Api/HrmProductSearchController@search` (`routes/api.php:80-81`, `:86`) — **popup báo giá HRM đang lấy giá qua đường này** |
| `searchProduct2` | `SC:1798-1816` | |
| Hiển thị cột giá | `SC:904-915`, `:1314`, `:1753`, `:2116` | `formatCurrency($product->price) / unit` (chỉ đọc kết quả) |
| Lọc trạng thái (2-D1) | `SC:109-129` `excludeCompanyUnavailableProducts` | đọc `pcc.status`, **không** phải giá ⇒ giữ |

Công ty: ND / tham số. Mức **M, chỉ trong 1 file**: thay join `pcc` bằng điều kiện `pp.company_id = ?` trên join `upp`; bỏ `CASE` hệ số
khi công ty đã bật cờ. ⚠️ Join `upp` **không có điều kiện công ty** thì ngay khi có dòng giá thứ 2 sẽ **nhân đôi dòng popup**.

### R6 — Hệ số `pcc.coefficient` nhân lúc đọc (17 chỗ code ERP)

`P:1244-1258` (getData) · `P:1315-1328` (getData($cid)) · `P:1689, 1761-1763` (`searchByFilter`, màn DS hàng hoá ERP) · `PC:3581-3589` (R4) ·
`SC` 7 khối (R5) · 6 chỗ kiểm lệch giá (R2d). (Khảo sát cũ nói "19 chỗ" vì đếm thêm form hàng hoá + thẻ hệ số Hãng SX, mà 2 chỗ này
đã chặn ở 2-D1.) Ngoài ra còn 4 view JS cấu hình/hiển thị hệ số ở màn hàng hoá/Hãng SX (`partials/classes/sale/{Product,Manufacture,ProductCompanyCoefficient,product_info/Product}.blade.php`), các màn này đã chặn.
**Cách làm tròn không thống nhất**: `getData` luôn `round(x/1000)*1000`, R4 chỉ làm tròn khi ≥ 1.000, SQL `ROUND()`, còn R2d làm tròn
như `getData`. Seed giá nướng hệ số phải chọn **đúng công thức `getData`**, vì đó là số người dùng nhìn thấy trên chứng từ.

### R7 — SQL / quan hệ đọc thẳng `upp` (ngoài R1–R6) — 15 file

| Chỗ | Nghiệp vụ | Công ty nên dùng | Biến | Mức |
|---|---|---|---|---|
| `Services/Sale/Firm/Contract/FirmSupportAccountingService.php:355-361` | `getProductsUnderNetPrice`: ĐMGG để phát hiện bán dưới giá net **lúc hạch toán hỗ trợ HĐ đại lý** | CT (`$contract->company_id`) | ✅ | S |
| `Services/Sale/Firm/Contract/ZTFirmSupportAccountingService.php:339-345` | như trên (ZT) | CT | ✅ | S |
| `Services/Sale/Firm/Quotation/FirmQuotationService.php:714-716` | `pp.sale_max_percent` khi load báo giá đại lý | CT | ✅ | S |
| `Services/Reports/SummarySaleReportService.php:458-465` | báo cáo tổng hợp bán hàng: giá niêm yết loại 1 | ⚠️ báo cáo nhiều công ty ⇒ **công ty của dòng doanh thu** | có trong `result` | M |
| `Services/OrderReports/ProductByManufactureReportService.php:41-55` | báo cáo hàng theo hãng: giá loại 1 + ĐMGG | `$filter_company_id` (có sẵn `:30`) | ✅ | S |
| `Http/Controllers/HomeController.php:599-689` | đếm "Hàng không được duyệt giá bán" ở trang chủ (`flag_*_wait_approve = 2`) | ND | `$logged_user` | S |
| `Contract.php:711` (`units.prices`) | HĐ cũ | CT | ✅ | S |
| `Sale/DeviceErrorController.php:277, 454` (`units.prices`) | danh mục lỗi thiết bị (kèm giá) | ND | `Auth` | S |
| `Warehouse/WarehouseReportsController.php:2570` | báo cáo kho: giá loại 1 | công ty kho / lọc báo cáo | xem lại | S |
| `Sale/QuotationTemplate.php:236, 311` (`prices->filter`) | mẫu báo giá | ND | `Auth` | S |
| `Customers/WrServiceQuotation.php:1017,1080,1096,1223,1324,1350` (`units[0]->prices[0]->price`) | BG dịch vụ BH/SC: giá bán lẻ ĐVT đầu (**không theo `price_type_id`, dựa thứ tự**) | CT (`wr_service_quotations.company_id`) | ✅ | S |
| `Order/InlandOrderSummaryNew.php:233` (`units.prices`) | tổng hợp đặt hàng nội địa | CT | ✅ | S |
| `CustomerManagerController.php:322-323, 543` (`baseUnitCondition.unit_price`) + `Sale/Customer.php:1865-1866` | thiết bị của KH: giá bán | ND | `Auth` | S |
| `Order/PriceCalculateRequest.php:135-147` | **form Phiếu tính giá**: giá hiện hành + giá hiệu lực của ĐVT | **công ty của yêu cầu** (`price_calculate_requests.company_id`) | ✅ | S |
| `P:1618-1680` `getDataWithPricesAttribute`, `P:1686-1770` `searchByFilter` | màn DS hàng hoá ERP (menu đã ẩn ở 2-D1, route `searchData`/`exportExcel/CSV/PDF` web `:577-581` **vẫn mở**) | ND | `Auth` | S (hoặc chặn route) |

Thêm các màn giá ERP **còn mở sau 2-D1** (chuyển HRM ở 2-D2): `PC@getProductsAndPrices :2313`, `@priceUpdating :2307`, `@expectedPrices :2234`
(web `:594-595, :608`). Cần lọc theo công ty ND nếu còn chạy song song.

### R8 — Giá vốn / giá mua ngoài trên `product_units` (sẽ sang `product_company_units`) — 12 file

| Chỗ | Đọc | Nghiệp vụ | Công ty | Rủi ro |
|---|---|---|---|---|
| `Sale/ProjectQuotationGroupProduct.php:24-31`, `Sale/ProjectAnalysis/ProjectAnalysisGroupProduct.php:56-63`, `Sale/Firm/Quotation/FirmQuotationGroupProduct.php:71-78` | accessor `cost_price` = `ProductUnit…firstOrFail()->cost_price` | giá vốn dòng BG dự án/phân tích/BG đại lý | CT | 🔴 hạch toán hỗ trợ |
| `Sale/ProjectQuotation.php:1846-1849, 1864-1890` | `import_price` + tổng `cost_price`/`vat_cost_price` | dự toán giá vốn BG dự án → `ProjectContractsController:339-340`, `ProjectAnalysisController:187-188,216-217` | CT | 🔴 |
| `Sale/ProjectAnalysis/ProjectAnalysis.php:471-472, 499-500` | **chép** `import_price` từ `pu.cost_price` vào `project_analysis_*_products` | phân tích dự án | CT | 🔴 đóng băng |
| `Services/Sale/ProjectAnalysisService.php:30-34, 50` | `import_price` + `capital_cost` | phân tích dự án | CT | 🔴 |
| `Sale/Firm/Contract/FirmContractTabProduct.php:236-264` | giá nhập kho gần nhất, **dự phòng** `units_info[0]->cost_price` | `FirmContract::getCostPriceAttribute :1426-1435` → `FirmSupportAccountingService:187-189` → lưu `firm_support_accounting.cost_price` | CT | 🔴 |
| `Services/Reports/AnalysisProfitContractService.php:67-68, 129-130, 253, 405-406` | `pu.cost_price` làm giá nhập **dự phòng** khi chưa có giá nhập | báo cáo phân tích lợi nhuận HĐ | CT (`fc.company_id`) | 🟠 báo cáo |
| `Services/Reports/RevenueStandardContractService.php:623, 773` | `$collection->cost_price` (accessor FirmContractTabProduct) | báo cáo doanh thu chuẩn | CT | 🟠 |
| `Tech/InstallSummary.php:123-127`, `Tech/InstallPlan.php:144-148` | **`pu.buy_price`** của phụ kiện lắp đặt → chép vào `install_summary_install_accessories.buy_price` (`InstallSummary:661`) | tổng hợp/kế hoạch lắp đặt | CT (`install_summaries.company_id`) | 🟠 chép |
| `Services/CRM/CRMImportProductToCrm.php:76` | `standard_price` = cost_price ĐVT cơ bản | đẩy CRM (job `SyncImportProductToCrm`) | công ty chủ | thấp |
| `Console/Commands/ExportLargeProductList.php:343` | Excel giá vốn | cron đã **comment** (`Kernel.php:113-115`) | — | chết |
| `HomeController.php:607` | `COALESCE(price_wait_approve, cost_price)` | đếm hàng chờ duyệt | ND | thấp |

Không có view chứng từ nào đọc `units[].cost_price` từ JSON R1. `Jobs/ProductSettingMailJob.php:254` chỉ được dispatch từ màn hàng gốc
(`ProductTemplatesController:3196`), còn `Jobs/SyncProductUnitPricesToCrm.php` **không được dispatch ở đâu** (code chết).

### 1.9 Bảng gom — sửa tập trung phủ được bao nhiêu

| Đường đọc | Sửa ở | Phủ | Chỗ phải truyền CT riêng |
|---|---|---|---|
| R1 `units_info`/`getData` | `P` (3 hàm) | 93 AJAX / 71 view + 61 chỗ server | ~37 file `->data` ở luồng load lại chứng từ (nếu muốn đúng khi người duyệt khác công ty) |
| R2 `getPriceByUnitAndType` | `P` (1 hàm, thêm tham số) | 69 chỗ / 42 file chạy được ngay | ~25 chỗ (R2b, R2c, R2d) |
| R3 `base_price` | `P` | 13 chỗ | 5–6 chỗ |
| R4 `getPriceOfProducts` | `PC` 1 hàm | 13 view | 0 |
| R5 popup | `SC` 7 khối | 338 màn + popup báo giá HRM | 0 (đã có tham số / ND) |
| R6 hệ số | bỏ theo cờ trong R1/R4/R5 + 6 file R2d | — | — |
| R7 SQL lẻ | 15 file | — | từng file |
| R8 giá vốn | 12 file (bỏ 2 file chết) | — | từng file |

⇒ **Lõi (P + SC + PC) ≈ 3 file phủ ~90% màn**. Phần đuôi ≈ **35 file đọc lẻ + ~30 file truyền CT** (nhiều file trùng nhau) ⇒ ~55–65 file.

---

## 2. Chỗ ERP còn GHI giá sau 2-D1

| # | Đường | file:dòng | Ghi gì | Công ty nên ghi | Đề xuất |
|---|---|---|---|---|---|
| W1 | **Phiếu tính giá** (giữ tới Phase 7) | `app/Model/Order/PriceCalculate.php:332-374` → `updatePriceWithApproval :376-760` (`upp` `:421-425`, `product_expected_prices :479-510`, `product_units.cost_price :541-554`, `product_approves :584, 672, 728`) | 6 giá + giá hiệu lực + giá vốn | ⚠️ hôm nay `products.company_id` (`:384`). Đề xuất **`price_calculates.company_id`** (công ty yêu cầu) | sửa ~6 chỗ trong 1 file: tìm/sinh dòng `upp` theo (ĐVT, loại, **công ty phiếu**), giá vốn ghi `product_company_units`. Câu **G3** |
| W2 | **Duyệt hàng tạm** (giữ tới Phase 6) | `Sale/TmpProductsController.php:567` → `P::createRecord` (`P:6929+`, công ty `:6980`, quy chế duyệt `:7112-7130`, bản ghi duyệt `:7179, :7306, :7341`) | tạo mã + ĐVT + 6 giá + giá vốn | `products.company_id` = công ty tạo (đúng là công ty lập hàng tạm). 6 tháng: Cty 1 767 mã, Cty 4 194 mã | sửa trong `createRecord`: gắn `company_id` cho `upp` + sinh `product_company_units` |
| W3 | **Cron 01:00** `product:update_price` | `Console/Commands/UpdateProductPrice.php:54-80` | áp `product_expected_prices` (status 2) vào `upp` qua `unit_price_id` | **kế thừa** từ dòng `upp` cha | **0 sửa** về công ty (đi theo id). Nhật ký `:85` nên in thêm công ty |
| W4 | **Cron 14:30** reset giá khi hết tồn (N5) | `Console/Commands/ResetProductPriceWhenZeroInventoryCommand.php:61-140` | `upp.price/sale_max_percent/coefficient = 0` (`:117-126`), `product_units.cost_price/sale_max_percent_coefficient = 0` (`:128-136`) | đã lặp theo công ty (`:61`), nhưng chọn hàng theo **`products.company_id`** (`:82`) và reset **mọi** dòng giá của mã | sửa: chọn hàng theo **công ty có dòng giá** (không chỉ hàng tự tạo) + reset **chỉ dòng của công ty đó**. Câu **G7**. (`Jobs/ResetProductPriceWhenZeroInventory.php` không được dispatch: chết) |
| W5 | **Cập nhật giá nhanh** (sang HRM ở 2-D2) | `PC@updatePrice :2550-3135` (web `:596`) | 6 giá + giá hiệu lực + giá vốn + `norm`/`note` | công ty ND | ⭐ **không sửa ERP**: làm màn HRM theo công ty, xong chặn route (đúng kế hoạch 2-D2). Nếu Hướng B lên **trước** màn HRM thì phải sửa tạm (~30 chỗ trong `:2669-3135`) ⇒ câu **G8** |
| W6 | Cập nhật giá thủ công | `PC@manualUpdatePrices :2240-2295` (web `:609`, GET có ghi) | áp giá hiệu lực hôm nay | kế thừa `unit_price_id` | 0 sửa (như W3) hoặc chặn ở 2-D2 |
| W7 | **Duyệt giá** | `ProductApprovesController.php:188-498` (`upp` `:234, 313, 375, 470`; `cost_price :253, 489`; `products.status`) | áp bản chờ duyệt | `product_approves.company_id` (có sẵn); `upp` qua `product_unit_price_id` (kế thừa) | giá vốn `:253, :489` phải ghi `product_company_units` của `product_approves.company_id`. 0 lần dùng 6 tháng; QC-6 đề xuất bỏ |
| W8 | Cập nhật giá theo hãng | `Model/Product/ManufactureExpectPrice.php:69-205` ← `Sale/ManufactureExpectPriceController:116` | sinh giá hiệu lực hàng loạt | — | **đã chặn tạo/lưu ở 2-D1** ⇒ 0 |
| W9 | Nhập kho cập nhật giá vốn | `Model/Warehouse/ProductImport.php:1199-1210` | `cost_price` | — | **đã tắt** (`:1189 return false`) ⇒ 0 (nhớ đổi đích nếu ai bật lại) |
| W10 | Form/Import/Hàng gốc/Product2… | (khảo sát A) | | | đã chặn 2-D1 ⇒ 0 |
| W11 | Observer log 2-D1 | `Observers/ProductWriteAuditObserver.php` (`AppServiceProvider:153-154`) | chỉ ghi log | — | nên thêm `company_id` vào log để bắt ghi thiếu công ty trong thời gian song song |

**Ngoài ERP** (ghi chú, chi tiết ở file HRM): HRM `ProductWriteService` sinh 6 dòng giá 0/ĐVT khi tạo hàng (G2 cũ). Sau Hướng B nó phải
gắn `company_id` = công ty tạo, và khi công ty B "lấy hàng về" (§26d) thì sinh bộ giá của B.

---

## 3. Chứng từ chép giá — rủi ro kế toán

| Loại | Chép gì | Lúc nào | Đóng băng? | Nguồn sau Hướng B |
|---|---|---|---|---|
| Báo giá/HĐ/đơn/phụ lục/đề nghị xuất (FE) | `price`, `sale_max_percent`, giá hiệu lực theo ngày | khi chọn hàng (R1) | ✅ lưu vào dòng chứng từ | R1 theo **CT** = ND khi lập mới |
| Hàng KM (server) | `price` (R2c) | khi lưu | ✅ | CT |
| ĐMGG khi **hạch toán hỗ trợ / quyết toán** | đọc **sống** R2b, R7 (`FirmSupportAccountingService:355`, `ZT…:339`) | lúc mở/duyệt hạch toán | ❌ (đọc lại mỗi lần) | CT. ⚠️ Đổi bảng giá làm **số hạch toán của HĐ đang dở thay đổi** |
| **Giá vốn dự toán** dự án/đại lý | R8 accessor + `import_price` | mở BG/phân tích, duyệt HĐ | lưu vào `support_accounting`, `project_analysis_*_products.import_price` khi duyệt/sync; trước đó **sống** | CT. 🔴 Bật cờ giữa chừng ⇒ hiệu quả HĐ đang chờ duyệt đổi số |
| Giá mua ngoài phụ kiện lắp đặt | `pu.buy_price` → `install_summary_install_accessories.buy_price` | lập tổng hợp lắp đặt | ✅ | CT |
| **Giá vốn kho (632/156)** | — | — | — | **KHÔNG dùng `product_units.cost_price`**: giá xuất từ sổ kho kế toán (`ProductExportDetail.php:50-70`, `ProductTransfer.php:280-282`); kiểm kê dùng giá nhập/xuất thực (`InventoryAuditReport.php:687`) ⇒ không rủi ro |
| Xuất ghép/tách | `price` loại 1 (`ProductExportsController:766`) | lập phiếu | ✅ | CT. Chưa thấy dùng để hạch toán (giá trị nhập ghép đi theo sổ kho). Cần kiểm thêm khi làm |

**Kết luận:** không chỗ nào **hạch toán sổ cái** bằng `product_units.cost_price`. Rủi ro là ở **hạch toán hỗ trợ / hiệu quả HĐ /
báo cáo lợi nhuận** (số quản trị, dùng để duyệt HĐ và tính thưởng), và 2 bảng ghi số đó lại. Hiện các chỗ này đọc giá vốn **chung**.
Sau Hướng B, công ty chưa có dòng `product_company_units` sẽ thấy giá vốn = 0 ⇒ lợi nhuận ảo 100%. Phải seed (mục 4) **và** cho dự
phòng tường minh (câu G5).

---

## 4. Dữ liệu (đo `hrm_erp`, SELECT 09/10)

| Chỉ số | Số |
|---|---:|
| `product_units` / `upp` | 46.560 / 264.646. **0** dòng `upp` mồ côi, **0** cặp trùng (ĐVT × loại). **Không có unique index** (chỉ index thường `product_unit_prices_unit_price_type_index`) |
| `upp` theo công ty tạo hàng | Cty 1: 258.270 · Cty 4: 6.215 · Cty 3: 138 · Cty 2: 18 · NULL: **5** |
| `product_units` có giá trị ≠ 0 | `cost_price` 24.877 · `buy_price` 1.091 · `sale_max_percent_coefficient` 23.360 · `liquidation_sale_max_percent` 5.678 · cờ chờ duyệt 24 |
| `pcc` | Cty 2: 538 (411 ≠ 1) · Cty 3: 516 (408 ≠ 1) · Cty 4: 50 (27 ≠ 1) · Cty 1: 1 |
| `product_expected_prices` status 2 (chờ áp) | 15.969 |
| Cặp (mã × công ty) **dùng trong 6 tháng** (BG đại lý + HĐ đại lý + đề nghị xuất) | Cty 1: 9.963 (176 mã cty khác) · Cty 4: 5.644 (**5.069**) · Cty 3: 1.888 (**1.875**) · Cty 8: 566 (**566**) · Cty 2: 411 (**411**). Tổng cặp khác công ty tạo: **8.097** |
| Cặp cần seed (12 tháng chứng từ ∪ tồn `stock_of_companies` > 0 ∪ có dòng `pcc`), khác công ty tạo | **12.574 cặp**: Cty 4 7.868 mã · Cty 3 2.700 · Cty 2 1.007 · Cty 8 748 · Cty 1 251 ⇒ **78.399 dòng `upp`** + ~12,6k dòng `product_company_units` |
| PTG theo công ty phiếu × công ty tạo hàng (6 tháng) | Cty 1×1: 1.837 phiếu · **4×1: 546** · **3×1: 113** · 8×1: 8 · 2×1: 2 · 1×4: 3 · 3×4: 1. Người lập: NV 1027 (Cty 1) 2.503/2.510 |
| Bảng chứng từ **không có `company_id`** | `contracts`, `project_quotations`, `order_requests`, `combo_campaigns`, `tmp_products` (có: `firm_quotations`, `firm_contracts`, `product_export_requests`, `product_exports`, `quotations`, `root_order_requests`, `inland_order_requests`, `product_transfer_requests`, `borrow_sell_requests`, `service_quotations`, `wr_service_quotations`, `install_summaries`, `project_contracts`, `price_*`, `product_approves`) |

---

## 5. Chiến lược triển khai giảm rủi ro

### 5.1 Các phương án, đánh giá trên code thật

| # | Phương án | Ưu | Nhược trên code ERP | Kết luận |
|---|---|---|---|---|
| S1 | **Lớp truy cập giá tập trung, tường minh**: `App\Services\Product\ProductPriceService` (hoặc static trên `Product`): `unitsInfoFor($pid,$cid)`, `priceOf($pid,$uid,$type,$cid)`, `costOf($pid,$uid,$cid)` + scope `ProductUnitPrice::scopeForCompany($q,$cid)` + model `ProductCompanyUnit`; giữ accessor cũ làm vỏ (gọi với công ty ND) | gom R1–R4 vào 1 chỗ; PHP 7.4/L6 làm được (scope, relation có `where`); dễ test | phải tự truyền CT ở ~30 chỗ; accessor không nhận tham số | ⭐ **nền** |
| S2 | Global scope `ProductUnitPrice` lọc theo `Auth` | 0 file gọi phải sửa | cron/queue **không có Auth** (W3, W4); không phủ **SQL join thô** (R5, R7: phần lớn đường đọc là `leftJoin('product_unit_prices as pp')`); che mất ngữ cảnh CT ≠ ND; tiền lệ `app/BusinessUnit/BusinessUnitScope.php:26` lấy `?? 1` khi không đăng nhập ⇒ sai im lặng | ❌ |
| S3 | **Cờ bật theo công ty** (config/env `PRICE_PER_COMPANY_IDS=2,3` hoặc cột cấu hình công ty) | rollout từng công ty, lùi nhanh (đổi cờ, không migrate lại) | khi cờ tắt resolver phải lọc **công ty tạo** (vì có thể đã có dòng thứ 2) + nhân hệ số như cũ ⇒ 2 nhánh code sống song song 1 thời gian | ⭐ dùng; ưu tiên **env/config** (không cần migration, không cần màn) |
| S4 | Ghi song song (cũ + mới) | reader chưa sửa vẫn đúng | **giá bán**: cũ và mới là **cùng bảng `upp`** ⇒ "song song" chỉ là: dòng công ty tạo = giá cũ. **Giá vốn**: `product_units.cost_price` (cũ) + `product_company_units` (mới). Luật: cột cũ **chỉ phản chiếu công ty tạo**. SG ghi giá vốn SG thì **không** đè cột cũ, nếu không reader chưa sửa thấy giá vốn SG | ⭐ cho giá vốn, tới khi R8 sửa xong |
| S5 | **Seed chọn lọc nướng hệ số** | ngày bật số liệu không đổi; bỏ được hệ số ngay; 78k dòng thay vì 2,1 triệu | phải chốt danh sách cặp (12 tháng? tồn? `pcc`?) + công thức làm tròn của `getData` | ⭐ |
| S6 | **So khớp chỉ đọc**: lệnh `price:compare --company=` duyệt các cặp seed, so "giá cũ hiệu dụng" (`upp` công ty tạo × `pcc`, làm tròn `getData`) với "dòng mới" cho 6 loại + giá hiệu lực; xuất CSV lệch | bằng chứng bằng số, chạy lại được sau mỗi bước | thêm 1 command | ⭐ bắt buộc trước khi bật cờ từng công ty |
| S7 | Shadow-read: trong `getData` tính cả 2, log lệch | bắt được ngữ cảnh thật | ×2 truy vấn trên đường nóng nhất (93 lời gọi) | chỉ bật theo % mẫu, ngắn ngày; S6 là chính |
| S8 | Đổi tên bảng + MySQL VIEW `product_unit_prices` lọc công ty tạo | reader cũ không sửa | Eloquent insert/update qua view dễ vỡ; migration HRM/ERP phức tạp; vẫn phải sửa reader để đọc công ty khác | ❌ |

### 5.2 Trình tự đề xuất (mỗi bước nghiệm thu riêng, lùi được)

| Bước | Việc | Hành vi người dùng | Lùi |
|---|---|---|---|
| **B0** Migration không đổi hành vi | `upp.company_id` **nullable** + index (`product_unit_id, price_type_id, company_id`); backfill = `products.company_id` (xử lý tay **5 dòng** hàng NULL). Tạo `product_company_units` (`product_unit_id, company_id, cost_price, buy_price, sale_max_percent_coefficient, liquidation_sale_max_percent` + cột chờ duyệt, tuỳ G4) + backfill 46.560 dòng công ty tạo | không đổi (vẫn 1 dòng/ĐVT/loại) | drop cột/bảng |
| **B1** Sửa đọc ERP + HRM, cờ TẮT | S1 cho R1–R8; cờ tắt ⇒ lọc công ty tạo + nhân `pcc` như cũ. Test snapshot: JSON `getData` của N mã × 4 công ty **giống hệt** trước khi sửa; popup không nhân dòng | không đổi | revert code |
| **B2** Sửa ghi | W1, W2, W4, W7 ghi theo công ty (G3, G7); giá vốn ghi song song (S4); observer log thêm `company_id` | PTG ghi về công ty phiếu (nếu G3 = ⭐) | revert |
| **B3** Seed chọn lọc | S5: 12.574 cặp / 78.399 dòng, giá = giá chung × `pcc` làm tròn `getData`; giá hiệu lực tương lai (status 2) cũng nhân bản theo (có `unit_price_id` mới) | không đổi (cờ tắt vẫn đọc công ty tạo) | xoá dòng `company_id ≠ products.company_id` |
| **B4** Bật cờ từng công ty | S6 so khớp = 0 lệch ⇒ bật Cty 2 (ít dữ liệu) → 3 → 4 → 8 → 1. Công ty đã bật: đọc dòng của mình, **không nhân `pcc`** | bắt đầu "mỗi công ty một bảng giá" | tắt cờ |
| **B5** Dọn | `upp.company_id` NOT NULL + **unique** (ĐVT, loại, công ty); bỏ đọc `pcc.coefficient` (cột giữ cho 2-A status); ngừng ghi `product_units.cost_price/buy_price`, rồi xoá cột **sau cùng** khi R8 + HRM sạch (`git grep` = 0) | — | khó lùi: làm cuối |

🔴 **Điều kiện cứng giữa B1 và B3:** mọi reader `upp` (ERP **và HRM** ~16 file theo khảo sát C §2.3) phải có điều kiện công ty.
Kiểm bằng test "danh sách trắng": grep `product_unit_prices|ProductUnitPrice` trong `app/`, mọi file phải nằm trong danh sách đã duyệt.
Thêm 1 file mới mà không duyệt thì test đỏ. Không có chốt này thì 1 reader sót sẽ nhân dòng / `first()` lấy ngẫu nhiên công ty, sai mà không báo.

### 5.3 Điểm kỹ thuật tự quyết (không hỏi user)

- Phân giải công ty: **tham số tường minh > công ty chứng từ > `Auth`**. Cron/queue luôn truyền tay. Bảng chứng từ không có `company_id`
  (5 bảng) thì suy từ `created_by → employee_infos.company_id` qua 1 helper chung.
- `getPriceByUnitAndType`: thêm tham số cuối `?int $companyId = null` (không vỡ 69 chỗ gọi). Thay `firstOrFail` bằng exception có
  kiểu `PriceNotFoundForCompany` (mã/công ty/loại giá) để thông báo đúng thay cho 404/500 câm. Cách xử lý khi thiếu giá do **G1** quyết.
- Giữ nguyên hình dạng JSON `getData` (`units[].prices[].expected_prices[]`) ⇒ 0 view FE phải sửa. Nhân tiện **bỏ `cost_price`/`buy_price` khỏi JSON** công khai (R1.1 đang lộ cho mọi màn chứng từ).
- `product_expected_prices` **không** thêm `company_id` (kế thừa qua `unit_price_id`, đúng §25a). Cron W3 không phải đổi.
- Unique index chỉ thêm ở B5 (khi đã NOT NULL). Trước đó dùng index thường + test trùng.
- Seed bằng lệnh artisan **idempotent** (bỏ qua cặp đã có), chạy theo lô, có `--dry-run` in số dòng. Không chạy trong migration.
- Làm tròn khi nướng hệ số: dùng đúng `round(price * coef / 1000) * 1000` của `getData` (`P:1252`), vì đó là số đã lên chứng từ.

---

## 6. Câu hỏi nghiệp vụ, ước lượng

### 6.1 Câu hỏi cho user (hỏi LẦN LƯỢT, theo thứ tự)

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **G1** | Công ty **chưa có giá** cho một mã (sau khi bật) thì chứng từ xử lý thế nào? | ⭐ **Chặn rõ ràng**: popup **ẩn** mã đó (hoặc hiện "Chưa có giá tại công ty") và không cho thêm vào chứng từ bán. Mua/kho (R2e) vẫn cho, với giá tham khảo 0 | Chặn: đúng tinh thần "mỗi công ty tự tính giá" (§26). Muốn bán mã mới thì phải qua PTG/màn giá. **Lấy giá công ty tạo làm dự phòng**: không ai bị chặn, nhưng quay về "giá chung" (Hướng A mà A4 đã bỏ), số trên chứng từ không phân biệt được giá thật hay dự phòng. **Giá 0**: chứng từ giá 0 lọt qua, sai mà không báo |
| **G2** | Dữ liệu cũ: chỉ gán về **công ty tạo** (đúng chữ A4) hay **nhân bản thêm cho công ty đang dùng**? | ⭐ **Gán công ty tạo + nhân bản chọn lọc** 12.574 cặp (chứng từ 12 tháng ∪ còn tồn ∪ có hệ số), giá = giá chung × hệ số (làm tròn như hiện tại) | Nhân bản: ngày bật **không ai thấy giá đổi**, bỏ hệ số được ngay, +78k dòng. Chỉ công ty tạo: Cty 2/3/4/8 mất giá **8.097 cặp đang bán** ⇒ phải nhập lại trước ngày bật (Cty 4 ≈ 5–8 nghìn mã × 6 loại giá). Nhân đủ 8 công ty: 2,1 triệu dòng, công ty 5/6/7 không bán vẫn có giá (trái §26) |
| **G3** | **Phiếu tính giá** của công ty khác (6 tháng: 546 phiếu Cty 4, 113 Cty 3… cho hàng Cty 1, do NV 1027 lập) ghi giá vào **công ty nào**? | ⭐ **Công ty của phiếu** (`price_calculates.company_id`, công ty yêu cầu tính giá) | Công ty phiếu: SG/Vinh có giá riêng do PTG tạo, TPE **thôi bị ghi đè** giá. Công ty tạo hàng (như hôm nay): PTG của SG vẫn đổi giá TPE, còn SG không có giá ⇒ mâu thuẫn với Hướng B. Cho chọn trên phiếu: linh hoạt nhưng sửa form PTG ERP (Phase 7 làm lại ở HRM) |
| **G4** | **Giá vốn theo công ty** gồm những cột nào? | ⭐ `cost_price`, `buy_price`, `sale_max_percent_coefficient` (đã có trong §25d) **+ `liquidation_sale_max_percent`** (ĐMGG thanh lý). Cột chờ duyệt đi theo | Đủ 4 cột: chính sách thanh lý mỗi công ty tự đặt. Bớt cột thanh lý: thanh lý dùng chung 8 công ty (5.678 ĐVT có giá trị) |
| **G5** | **Hạch toán hỗ trợ / hiệu quả HĐ / phân tích dự án** đang đọc giá vốn **sống**. Sau khi bật lấy giá vốn công ty nào, và khi công ty chưa có giá vốn thì sao? | ⭐ **Giá vốn công ty chứng từ**. Thiếu ⇒ **báo thiếu, không cho duyệt** hạch toán (không ngầm lấy 0). HĐ **đang chờ duyệt lúc bật cờ** chấp nhận đổi số (đã nướng hệ số nên chỉ lệch ở mã có giá vốn khác) | Báo thiếu: không có lợi nhuận ảo. Lấy 0: hiệu quả HĐ ảo 100% ⇒ duyệt nhầm, thưởng sai. Lấy giá vốn công ty tạo: số "đúng như cũ" nhưng trái Hướng B |
| **G6** | Khi **sửa/duyệt lại chứng từ cũ**, giá hiện hành hiển thị theo công ty nào? | ⭐ **Công ty của chứng từ** (không phải người đang mở) | CT: người Cty 1 duyệt HĐ SG thấy đúng giá SG. ND (như hôm nay): thấy giá TPE trên HĐ SG ⇒ báo "lệch giá" sai ở 6 chỗ kiểm lệch (R2d) |
| **G7** | Cron 14:30 "đưa giá về 0 khi hết tồn": phạm vi theo công ty thế nào? | ⭐ Mỗi công ty bật cấu hình ⇒ reset **dòng giá của chính công ty đó** với **mọi mã công ty có giá** (không chỉ mã tự tạo), tồn tính trên kho của công ty đó | Theo ⭐: SG hết tồn chỉ mất giá SG. Giữ như cũ (mã tự tạo, reset mọi dòng): SG bật là xoá giá TPE của mã SG tạo; mã TPE mà SG bán thì không bao giờ reset |
| **G8** | Hướng B lên **trước hay sau** màn "Cập nhật giá nhanh" HRM (2-D2)? | ⭐ **Sau** (hoặc cùng đợt): màn HRM viết thẳng theo công ty, ERP `updatePrice` bị chặn, **không sửa** 30 chỗ trong `PC:2669-3135` | Sau: ít sửa ERP nhất. Trước: phải sửa tạm `updatePrice` ERP theo công ty (~1 ngày + test) rồi vứt |
| **G9** | 26 chỗ ERP lấy giá qua `getPriceByUnitAndType` (KM trên BG/HĐ, đơn mua, chuyển kho, xuất ghép/tách…) hôm nay **không nhân hệ số** ⇒ HP/Vinh/SG đang ra **giá TPE thô** ở đó. Sau khi nướng hệ số, các chỗ này ra **giá có hệ số** | ⭐ **Chấp nhận** (coi như sửa lệch, thống nhất 1 giá/công ty) | Chấp nhận: 846 mã hệ số ≠ 1 ở 3 chi nhánh đổi số tại các màn đó. Giữ số thô: phải giữ thêm "giá chung" song song (quay lại Hướng A) |
| **G10** | Bật **theo từng công ty** (thử Cty 2 → 3 → 4 → 8 → 1) hay bật cùng lúc? | ⭐ **Từng công ty**, mỗi công ty sau khi so khớp = 0 lệch | Từng công ty: lùi được, rủi ro dồn ít. Cùng lúc: 1 ngày chuyển, sự cố ảnh hưởng 8 công ty |

### 6.2 Ước lượng ERP (chỉ ERP; HRM xem file riêng)

| Hạng mục | File | Độ lớn |
|---|---:|---|
| Lõi `P` (R1, R2, R3, `searchByFilter`, `exportExcel`) + `ProductUnit` relation + `ProductUnitPrice` scope + **mới** `ProductCompanyUnit`, `ProductPriceService`, helper công ty chứng từ | 3 sửa + 3 mới | M–L (đường nóng nhất, test kỹ) |
| `SC` popup 7 khối + `PC` (`getData`, `getPriceOfProducts`, `getDataForPriceAsking`, màn giá còn mở) | 2 | M |
| Truyền CT: R1.5 (~37 file `->data`) + R2b/c/d (~25 chỗ / ~20 file) + R3 (5–6) — trùng nhau nhiều | ~30–40 | S mỗi file |
| R7 SQL lẻ | 15 | S |
| R8 giá vốn | 10 (bỏ 2 file chết) | S–M |
| Ghi W1, W2, W4, W7 (+W5 nếu G8 = trước) | 4 (+1) | M |
| Lệnh seed + lệnh so khớp + test danh sách trắng reader | 3 mới | M |
| **Tổng** | **≈ 55–65 file sửa + ~6 file mới** | ~1,5–2 lần đợt 2-D1 (2-D1 = 33 file). Khớp con số "34 file" của A5 **cộng** đuôi truyền CT mà A5 chưa đếm |

PHPUnit ERP (sqlite `:memory:` như 2-D1 không đủ cho SQL MySQL): test resolver + seed/so khớp chạy trên DB local `hrm_erp`.
Nghiệm thu UI (Playwright, đo DOM): giá popup × 4 công ty, giá dòng chứng từ sau khi chọn hàng, hạch toán hỗ trợ 1 HĐ dự án + 1 HĐ đại lý trước/sau bật cờ.

### 6.3 Vấn đề ngoài luồng ghi lại (không vá trong đợt này)

- `ProductExportsController.php:766` truyền `unit_coefficient` vào vị trí `unit_id` của `getPriceByUnitAndType` (lỗi sẵn).
- `getData` trả cả `cost_price`/`buy_price` (`product_units.*`) cho mọi màn chứng từ, kể cả người không có quyền xem giá vốn (R1.1).
- `WrServiceQuotation` lấy `units[0]->prices[0]` theo **thứ tự**, không theo `price_type_id` (R7).
- `Jobs/SyncProductUnitPricesToCrm.php`, `Jobs/ResetProductPriceWhenZeroInventory.php`: không được dispatch (code chết).
