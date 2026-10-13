# Đợt 2-D — Khảo sát PHẦN C: LUỒNG GIÁ HÀNG HOÁ (09/10/2026)

> Khảo sát CHỈ ĐỌC: không sửa source, không ghi DB, không chạy artisan, không checkout.
> **Mã ERP:** bản `origin/gop_db` (`04b61efc24`, 03/10/2026), giải nén bằng `git archive` vào scratchpad. Số dòng dưới đây
> theo `gop_db` (lệch khoảng −8 dòng so với `develop_01` mà khảo sát A dùng).
> **Mã HRM:** worktree `wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`, nhánh `feat/chuyen-doi-hang-hoa`.
> **Số đo:** DB `hrm_erp` (DB gộp; bản chụp ERP mới nhất 15/09/2026), chạy SELECT ngày 09/10/2026. "6 tháng" = **15/03 → 15/09/2026**.
> **Đọc trước:** `ton.md` (Q1b), `khao-sat-a-chan-ghi.md` §1.4/§2, `khao-sat-b-doc.md`, `../2c-ghi/chot.md`,
> `../man-danh-muc-hang-hoa/design.md` §9 §18–§20 §24–§25 §28–§29, `ton-chot-truoc-code.md` (A4/A5, C1–C7).

---

## 0. Tóm tắt

1. ⚠️ **Tiền đề của Q1b chỉ đúng một phần.** ERP có **menu riêng cho giá**: *Kế toán → Quản lý giá - CTKM → Giá bán*
   (`resources/views/layouts/topmenubar.blade.php:936-950`). Menu này gồm 7 mục: Phiếu tính giá, Cập nhật giá nhanh, Cập nhật giá
   theo hãng, Nhật ký cập nhật giá, Trạng thái cập nhật giá, Hàng sắp điều chỉnh tăng giá, Cập nhật nhanh giá dịch vụ. Nó
   **không nằm** trong menu Danh mục hàng hoá. Duyệt giá cũng có lối vào riêng (`topmenubar:2235-2236`). Vậy bỏ menu Danh mục hàng
   hoá ERP (Q1) chỉ làm mất **2 nút** trên màn danh sách hàng hoá: *Cập nhật giá* (`products/list.blade.php:39`, trùng màn với menu
   Kế toán) và *Hàng chưa có công khoán* (`:57`, xuất Excel). Xem câu **QC-0**.
2. **Ai đang ghi giá, và nhiều tới đâu** (đo theo lịch sử ĐVT `product_histories.column_name='units'`, 6 tháng):
   | Luồng | Lần ghi | Mã | Người | Ghi chú |
   |---|---:|---:|---:|---|
   | **Phiếu tính giá** (Lưu & duyệt) | **4.008** | 3.753 | 3 | 2.140 + 648 + 138 + … phiếu; **99,8% do 1 người** (NV 1027, Ban điều hành Cty 1) lập cho 5 công ty |
   | **Cập nhật giá nhanh** (`updatePrice`) | **≈ 2.868** | 2.069 | **12** | 4 công ty (1, 3, 4, 8); khoảng 160–780 lần/tháng |
   | **Cron 01:00** áp giá hiệu lực | 1.176 | 1.087 | — | `price_logs` 38 lần chạy có đổi giá (03–09/2026) |
   | **Cron 14:30** đưa giá về 0 (N5) | **89.626 dòng** ngày 01/03/2026 + 1.731 dòng 01/08 | — | — | đã **chạy thật** ở production. Local: cấu hình NULL cả 8 công ty |
   | Duyệt giá | **0** | — | — | `product_approves` AUTO_INCREMENT = 1 (chưa từng có dòng); `is_company_price = 0` ở cả 8 công ty |
   | Cập nhật giá theo hãng | **0** | — | — | 87 phiếu, phiếu mới nhất 21/12/2022 |
3. **Mô hình dữ liệu:** cả hệ thống có **MỘT bảng giá chung**: `product_units` → `product_unit_prices` (6 loại giá) →
   `product_expected_prices`. Chiều "công ty" chỉ đi vào ở 2 chỗ: **(a)** hệ số giá `product_company_coefficients.coefficient`,
   được **nhân lúc ĐỌC** theo công ty người dùng (HP 538 dòng, Vinh 516, SG 50; hệ số 1,00–1,29); **(b)** cổng khi SỬA: chỉ sửa
   được hàng có hãng SX **và** chủ hàng thuộc công ty mình. Trên thực tế 1.065/1.071 hãng thuộc Cty 1.
4. 🔴 **Sau 2-D1, hệ số giá bị ĐÓNG BĂNG.** Hai màn ghi hệ số là form hàng hoá và thẻ "Hệ số giá theo công ty" của màn Hãng SX
   (N2), cả hai đều bị chặn/gỡ ở 2-D1. Thế nhưng tháng 07–08/2026 màn Hãng SX vừa sinh **722 dòng** hệ số cho HP/Vinh/SG (3 hãng).
   Từ lúc đó hàng mới của các hãng này ở chi nhánh sẽ bán bằng giá TPE. Xem **QC-3**.
5. **"Cấu hình chính sách giá bán nội bộ" mới có MOCKUP**: design §28, mockup `mockup-luong-xay-dung-hang-hoa.html`, quyền 1656 giữ
   chỗ. **Không có code, không có bảng** (`information_schema` không có bảng nào khớp, grep `hrm-api`/`hrm-client` = 0). Theo
   chốt §28a-4 nó là **SỐ GỢI Ý**, không ghi vào bảng giá. Vì vậy nó **không thay được** hệ số giá và **không phải** nơi lưu giá
   theo công ty (mục 3).
6. **Giá theo công ty CHƯA có chỗ lưu.** `ton-chot-truoc-code.md` A4/A5 (30/09) đã chốt Hướng B: `product_unit_prices.company_id`
   NOT NULL, bảng mới `product_company_units`, sửa **34 file ERP**, gán 264.646 dòng giá. Thêm vào đó **~16 file HRM** cũng đọc
   thẳng bảng giá (mục 2.3). Kéo phần này vào 2-D thì 2-D thành phase lớn nhất của cả feature.
7. **Đề xuất:** tách **2-D1** (chặn ghi + đọc không lỗi, phần không phải giá; là điều kiện lên production) và **2-D2** (màn
   "Cập nhật giá nhanh" HRM, port 1–1 trên **bảng giá chung**, giữ nguyên hợp đồng dữ liệu nên phía ERP đọc giá không phải sửa
   file nào; xong mới chặn các đường ghi giá thủ công của ERP). Phiếu tính giá (Phase 7), duyệt hàng tạm (Phase 6) và 2 cron giữ
   ở ERP. Giá theo công ty để thành phase riêng (Phase 8). Mục 4.

---

## 1. Kiểm kê luồng giá ERP

Ký hiệu: **R** = route `routes/web.php` (gop_db) · **C** = controller/model:dòng · đo trên `hrm_erp`.

### 1.1 Bảng tổng

| # | Luồng / màn (lối vào) | R | C | Đọc | Ghi | Quyền (guard `web`, số role) | Dùng thật (6 tháng) |
|---|---|---|---|---|---|---|---|
| **L1** | **Cập nhật giá nhanh** (`topmenubar:944`; nút "Cập nhật giá" `products/list.blade.php:39`) | GET `products/editPrices` **:586** · GET `getProductsAndPrices` **:595** · POST `{id}/updatePrice` **:596** | `ProductsController@editPrices` :2298 · `@getProductsAndPrices` :2315 · `@updatePrice` :2552–~2990 | `products`, `product_units`, `product_unit_prices`, `product_expected_prices` (> hôm nay), tồn kho (`warehouseInfo.stockOfProducts`) | 6 dòng `product_unit_prices` của **1 ĐVT/lượt** (giá, hệ số, ĐMGG, 3 cờ "sửa tay" TMĐT; cờ chờ duyệt về 0) · `product_expected_prices` (tối đa 1 dòng tương lai/loại giá, xoá dòng tương lai không còn gửi lên) · `product_units.cost_price`, `liquidation_sale_max_percent` · **`products.norm` + `products.note`** (:2901-2902) · `product_versions`/`product_histories` | `Cập nhật nhanh giá hàng hóa` (100063, **18 role**); cổng thêm: hãng SX của hàng phải thuộc công ty người dùng (:2627-2632, list :2479-2485) **và** `Product::canEdit()` (`app/Product.php:6925`: `products.company_id` = công ty người dùng hoặc NULL) | **≈ 2.868 lần / 2.069 mã / 12 người** (Cty 1: NV 1027 1.186, NV 148 749, NV 215 67…; Cty 4: NV 433 564; Cty 8: NV 1060 232; Cty 3: NV 407 25). Theo tháng: 03 162 · 04 780 · 05 738 · 06 417 · 07 419 · 08 184 · 09 (nửa tháng) 168 |
| **L2** | **Trạng thái cập nhật giá** (`topmenubar:947`) + nút cập nhật thủ công | GET `expectedPrices` **:608** · **GET** `manualUpdatePrices` **:609** | `@expectedPrices` :2236 (giá hiệu lực **hôm nay**) · `@manualUpdatePrices` :2242-2295 | `product_expected_prices` (effect_date = hôm nay) | áp `product_expected_prices` (status 2) hôm nay vào `product_unit_prices`, đặt status 1, ghi version/history | `Quản lý giá` (100127, 23 role) | không tách được với cron (cùng kiểu ghi); dùng khi cron chưa chạy. ⚠️ N30: GET mà có ghi |
| **L3** | **Hàng sắp điều chỉnh tăng giá** (`topmenubar:848, :948`) | GET `priceUpdating` **:594** | `@priceUpdating` :2309 → view `products/price_updating.blade.php` (216 dòng) | giá hiệu lực tương lai | — | không gate | chỉ đọc |
| **L4** | **Nhật ký cập nhật giá** (`topmenubar:946`) | `price_logs` **:4349-4352** | `Sale/PriceLogsController` (31 dòng) | `price_logs` + **file HTML** `public/price_logs/<ngày>-log.html` trên máy chủ ERP | — | không gate | 38 bản log 03–09/2026 |
| **L5** | **Duyệt giá** (`topmenubar:2235-2236`, chỉ hiện khi có quyền) | GET `approvePrices` **:587** (quyền) · `approvePricesSearchData` :588 · POST `{id}/approveSubmit`, `notApproveSubmit`, `approvesSubmit`, `notApprovesSubmit` **:589-592** (**không gate**, N29) · `approveExportExcel` :593 | `ProductApprovesController` 562 dòng (:188-498) | `product_approves`, `product_approve_prices` | giá + giá hiệu lực + `product_units.cost_price/unit_coefficient` + **`products.status = 1`** (:259) | `Duyệt giá hàng hoá` (100983, 12 role) | **0**: `product_approves` AUTO_INCREMENT = 1, `product_approve_prices` = 5 (chưa từng có dòng hợp lệ). Chỉ kích hoạt khi `companies.is_company_price = 1`, mà cả 8 công ty đều = 0. Còn **6 ĐVT** mang cờ chờ duyệt mồ côi (5 từ 13/08/2025, 1 từ 01/03/2026) |
| **L6** | **Phiếu tính giá** (`topmenubar:943`; chuỗi *Hàng tạm - Hỏi giá* `:1545-1547`) | `price_asking_requests/*` :2253-2268 · `price_calculate_requests/*` :2271-2282 · **`price_calculates/*` :2285-2294** · `price_calculate_results/*` :2297-2301 | `Order/PriceCalculateController` :160-165, :226-227 → `Model/Order/PriceCalculate.php@approve` :332-374 → `updatePriceWithApproval` :376-760 | yêu cầu tính giá, giá đang có | 6 giá + giá hiệu lực + `product_units.cost_price` + **`products.note`** (:368) + version/history (:567); nếu bật quy chế thì đẩy sang `product_approves` | lập yêu cầu: `Lập yêu cầu tính giá` (101005, 12 role); duyệt yêu cầu: `Kế toán mua hàng` (100144, 9 role) — `PriceCalculateRequest::canApprove`; phiếu: chỉ người lập sửa (`canEdit` :321); xem: 4 quyền `Xem DS tính giá bán theo …` (101010–101013, 101035) | **4.008 lần ghi / 3.753 mã**. Phiếu theo tháng tạo: 03 804 · 04 528 · 05 419 · 06 396 · 07 322 · 08 329 · 09 147 (100% "Đã duyệt"); dòng hàng 1.342 → 194/tháng. **100% yêu cầu tính giá đi từ Yêu cầu hỏi giá** (3.147/3.147). Hàng trong phiếu: 1.299/4.029 dòng là hàng mới tạo ≤ 7 ngày, 475 dòng từ hàng tạm ⇒ phần lớn là **định giá lại hàng cũ** |
| **L7** | **Cập nhật giá theo hãng** (`topmenubar:945`) | `manufacture_expect_prices/*` **:3653-3658** (quyền nhóm `Cập nhật nhanh giá hàng hóa`) | `Sale/ManufactureExpectPriceController` :116 → `Model/Product/ManufactureExpectPrice.php@updateProducts` :69-205 | mọi hàng status 1 của hãng (trừ danh sách loại trừ) | sinh `product_expected_prices` = giá × (1 + %) làm tròn trăm, version/history | như trên | **0** — 87 phiếu, mới nhất **21/12/2022** |
| **L8** | **Công khoán** | POST `importExcelInstallWork` **:584** ("Import công lắp đặt" `products/list:51`) · GET `exportExcelNorm` **:633** ("Hàng chưa có công khoán" `products/list:57`) | `@importExcelInstallWork` :2163 → `ExcelImports/InstallWorkImport.php:50-52` · `@exportExcelNorm` :3983 | `products.norm` | **`products.norm` + `products.tech_coefficient`** (hàng loạt, không version) | `Thêm hàng hóa` / `Xuất dữ liệu hàng hóa` | `norm` đổi qua lịch sử (form + L1) 5–27 mã/tháng; import không để lại vết. ⚠️ **Đây KHÔNG phải giá**: `norm` là công khoán lắp đặt, `tech_coefficient` là hệ số công nghệ (T6, dùng chung). **HRM form đã ghi cả 2 cột** (`ProductWriteService.php:278`, `ProductRequest.php:81`, `components/product/form/ProductFormSpecs.vue`) |
| **L9** | **Cron `product:update_price`** 01:00 | `Console/Kernel.php:47-55` (gửi email `PRICE_EMAIL_1..3`, ghi file log) | `Console/Commands/UpdateProductPrice.php:45-117` | `product_expected_prices` effect_date = hôm nay, `status = 2`, `flag` ≠ 1 | áp vào `product_unit_prices`, đưa cờ chờ duyệt về 0, status 1, `price_logs`, version/history | — | 1.176 lần / 1.087 mã; `price_logs` 10·10·5·6·5·1·1 lần/tháng (03→09) |
| **L10** | **Cron `product:reset_price_when_zero_inventory`** 14:30 (N5) | `Kernel.php:107-110` | `Commands/ResetProductPriceWhenZeroInventoryCommand.php` (175 dòng) | công ty có cấu hình loại hàng, hàng `products.company_id` + `product_cate`, tồn `accounting_stocks` | `product_unit_prices.price = 0`, `product_units.cost_price = 0` (query builder) | — | **01/03/2026 14:30–14:32: 89.626 dòng giá về 0**; 01/08/2026: 1.731. Hiện **147.504/264.646 dòng giá = 0** (56%); 10.853 hàng status 1 có giá bán lẻ ĐVT cơ bản = 0. ⚠️ Bản chụp local có cấu hình NULL nhưng production **đang bật** (hoặc bật theo đợt) |

### 1.2 Các đường ghi giá KHÁC (ngoài luồng giá)

| Đường | File:dòng | Ghi giá gì | Sau 2-D1 |
|---|---|---|---|
| Form tạo/sửa hàng hoá ERP | `Product::createRecord` (`app/Product.php:6929+`), `ProductsController@update` | đơn vị + 6 giá (form có tab giá, quyền `Quản lý giá` để sửa giá vốn `:1547`) | **chặn** (khảo sát A) |
| Import hàng hoá (`ProductsImportNew`, `ImportProduct160223`, `ProductsImportZitec`, `ImportProduct060123`) | `app/ExcelImports/*` | tạo đơn vị + giá | **chặn / gỡ** (A, Q5) |
| Hàng gốc / Product2 / Hàng có sẵn | `GenerateProduct`, `CreateProductUnitsAfterMapping`, `Product2Controller`, `ProductInfoController`, `SyncProductInfoService`, `CreateProductService` | tạo đơn vị + giá | **chặn** (A) |
| **Duyệt hàng tạm** | `Sale/TmpProductsController.php:566` → `Product::createRecord($request, $tmp->id)` | chép giá hàng tạm sang `product_unit_prices` | **GIỮ** tới Phase 6 ⇒ vẫn là đường ghi giá ở ERP (961/5.203 hàng mới) |
| Nhập kho cập nhật giá vốn | `Model/Warehouse/ProductImport.php:1199-1210` | `product_units.cost_price` | **đã tắt sẵn** (`canUpdateUnitCostPriceFromSupplierPrice` `return false` :1189) |
| HRM tạo hàng (2-C, G2) | `hrm-api/.../ProductWriteService` | 6 dòng giá 0 / ĐVT | giữ |

### 1.3 Ngoài phạm vi (không phải giá hàng hoá)

- **Cập nhật nhanh giá dịch vụ** (`topmenubar:942`, `service_config_price` R :3689-3690): ghi `services`/`service_levels`, không
  ghi bảng giá hàng hoá. HRM đã có màn tương đương `hrm-client/pages/customer-care/service-price-config`.
- `company_price_types` (31 dòng): tên + hệ số theo loại giá của từng công ty, dùng cho hợp đồng/đơn hàng nguyên tắc
  (`PrincipleOrderService`, `FirmContractService`…), cấu hình ở màn Công ty. Theo §28a-8 thì độc lập với chính sách nội bộ.
- Chương trình khuyến mại (`topmenubar:949`), giá vận chuyển, giá bốc xếp: không đụng.
- `hrm-client/pages/assign/settings/price-approval`: cấu hình duyệt **báo giá** (tỷ suất lợi nhuận), không phải duyệt giá hàng.

---

## 2. Mô hình dữ liệu giá hiện tại

### 2.1 Bảng + quan hệ

```
products (company_id = công ty TẠO; manufacture_id → manufactures.company_id)
 └─< product_units           46.560   (unit_id, is_base, unit_coefficient, cost_price, buy_price,
 │                                      sale_max_percent_coefficient, liquidation_sale_max_percent,
 │                                      price_wait_approve, flag_price_wait_approve, approve_comment, …)
 │    └─< product_unit_prices 264.646 (price_type_id 1–6, price, coefficient, sale_max_percent,
 │         │                           is_manual_{price,coefficient,sale_max_percent}_online,
 │         │                           {price,coefficient,sale_max_percent}_wait_approve + 3 cờ)
 │         └─< product_expected_prices 95.266 (unit_price_id, price, coefficient, sale_max_percent,
 │                                      effect_date, status 1=đã áp/2=chờ áp, *_wait_approve, flag)
 └─< product_company_coefficients 1.105 (product_id, company_id, coefficient NOT NULL
                                        + status/4 cột quản trị HRM thêm ở 2-A)
price_types 6 · price_logs · product_approves 0 · product_approve_prices 0 · manufacture_expect_prices 87 (+types, +except)
```

- **Không bảng nào trong chuỗi giá có `company_id`** (đo lại `information_schema` 09/10).
- `product_expected_prices`: status 2 = 15.969 dòng (chờ áp, có dòng tới 31/08/2027), status 1 = 79.297. **2.497 dòng hiệu lực sau
  15/09/2026** đang chờ cron áp.
- ⚠️ **Bất biến G2 "6 dòng giá/ĐVT" KHÔNG đúng với dữ liệu cũ:** loại 5 (*Giá bán theo lô*) chỉ có **32.211** dòng, loại 6 (TMĐT)
  có 46.195, trong khi có 46.560 ĐVT ⇒ ~14.349 ĐVT thiếu dòng loại 5 và 365 ĐVT thiếu loại 6. ERP `updatePrice` tự sinh dòng còn
  thiếu khi lưu (`if (!$price) new ProductUnitPrice()` :2724-2727). HRM phải làm y như vậy, không được giả định đủ 6 dòng.
- Loại 6 TMĐT = **bán lẻ × `configs.coefficient_ecommerce_price` (= 1,3)**, trừ khi bật cờ sửa tay (112 dòng đang bật).
- Giá 0: loại 1 có 22.853/46.560 dòng = 0, loại 6 có 38.403 dòng = 0 (phần lớn do L10).

### 2.2 Chứng từ ERP đọc giá thế nào

| Đường đọc | File:dòng | Đọc gì | Hệ số công ty |
|---|---|---|---|
| **`getData`** (~93 chỗ gọi / 71 view, ngay sau khi chọn hàng) | `ProductsController@getData` :3147 → `Product::getDataAttribute` `app/Product.php:1208-1275`; `getData($company_id)` :1278 | `units_info` (:`getUnitsInfoAttribute`) = mọi ĐVT + **6 giá** + **giá hiệu lực > hôm nay** (sắp xếp theo ngày); `base_price`, `base_unit`, `norm` | **nhân hệ số** của công ty người dùng (hoặc công ty truyền vào), làm tròn nghìn — cả giá hiện tại lẫn giá hiệu lực (:1210-1222, :1281-1293) |
| **`getPriceOfProducts`** (13 file) | `ProductsController.php:3571-3597` (R :46) | `getPriceByUnitAndType` (`Product.php:1407-1418`, **`firstOrFail`** ĐVT + loại giá) | nhân hệ số, làm tròn nghìn nếu ≥ 1.000 |
| **Popup chọn hàng** (338 màn) | `Common/SearchController.php:399-433, :921-955, :1363-1397, :1750-1767` (+ :859, :1268, :1706, :2068) | `pu.is_base = 1 AND pp.price_type_id = ?` | `CASE WHEN pcc.coefficient IS NOT NULL THEN ROUND(pp.price*pcc.coefficient/1000)*1000` |
| `base_price` / `base_unit` | `Product.php:1388-1405` | **`firstOrFail`** ĐVT cơ bản + giá loại 1 | không |
| Chỗ đọc khác | `ProductUnitPrice` 33 file / 123 dòng · `product_unit_prices` 11 file · `ProductExpectedPrice` 22 file · hệ số 15 file / 43 dòng (`PrincipleOrderStoreRequest`, `ZTPrincipleOrderStoreRequest`, `PrincipleOrderService`, 2 `ProductExportRequestsController`, `BorrowSellRequestsController`…) | | |

### 2.3 HRM cũng đọc thẳng bảng giá

Ngoài `MasterData`, có **~16 file HRM** đọc `product_unit_prices` / `product_units.cost_price` / hệ số. Assign: `QuotationService`,
`ErpProductSearchService`, `BomListService`, `QuotationImportService`, 2 controller. Finance: `ProductPrepickRequestController`,
`ProductImportRequestService`, `ProductTransferRequestService`, `BorrowSellRequestService`, `BorrowExportRequestService`,
`PrepickApprovalRouteService`. CustomerCare: `ServiceService`, `WrQuotationService`, `WrServiceQuotationService`. Human:
`TpProductUnitPrice`, `TpProductCompanyCoefficient` (`getRetailPrices` nhân hệ số y như ERP). ⇒ Đổi cấu trúc bảng giá (giá theo
công ty) là phải sửa cả ERP lẫn HRM.

### 2.4 Hệ số giá theo công ty đang tham gia ở đâu

- **Dữ liệu:** Cty 2 (HP) 538 dòng (127 dòng = 1), Cty 3 (Vinh) 516 (108 = 1), Cty 4 (SG) 50 (23 = 1), Cty 1: 1 dòng (= 2). Khoảng
  1,00–1,29. Sinh gần đây: 07/2026 571 dòng (2 hãng), 08/2026 151 dòng (1 hãng). Tức là **chi nhánh HP/Vinh bán hàng TPE theo giá
  TPE × 1,02–1,05**: đây là cơ chế "giá theo công ty" duy nhất đang chạy.
- **Ghi:** form hàng hoá ERP (`Product::syncCompanyCoefficients` :6395-6400, xoá rồi ghi lại), thẻ hệ số của màn Hãng SX (N2),
  hàng gốc, Product2. **Cả 4 đường này đều bị chặn/gỡ ở 2-D1** ⇒ sau 2-D1 **không còn màn nào sửa được hệ số**. HRM chỉ sinh
  dòng `coefficient = 1` (G4/V1/L1).
- **Đọc:** mục 2.2 (19 chỗ ERP) + HRM `TpProductCompanyCoefficient` + 4 file Finance + `ServiceService`.
- Tiền đề #8: hệ số sẽ bỏ **sau** khi xong chuyển đổi, mỗi công ty tự xây giá riêng. Nhưng chưa có chỗ lưu giá riêng (2.1), nên
  **chưa bỏ được** hệ số mà không làm HP/Vinh/SG mất giá chênh.

### 2.5 HỢP ĐỒNG DỮ LIỆU HRM phải giữ khi ghi giá (để ERP + HRM đọc vẫn đúng, không sửa file đọc nào)

| # | Bất biến | Vì sao |
|---|---|---|
| HĐ1 | Mỗi ĐVT đúng **1 dòng / loại giá 1–6**; **sửa tại chỗ, không xoá** dòng; thiếu dòng thì **sinh** khi lưu | `firstOrFail` ở `getPriceByUnitAndType`/`base_price`; popup INNER-lọc `price_type_id` |
| HĐ2 | Đúng 1 ĐVT `is_base = 1`; màn giá **không** đổi `unit_id`/`is_base`/`unit_coefficient` (thuộc form hàng hoá, C7) | §20: chia trách nhiệm `product_units` |
| HĐ3 | Ghi `price`, `coefficient`, `sale_max_percent`; đưa `*_wait_approve` = 0 và 3 cờ `flag_*_wait_approve` = 0 (như nhánh "không duyệt" của ERP :2733-2743) | `getProductsAndPrices` và form ERP hiển thị theo `CASE flag` |
| HĐ4 | Loại 6 TMĐT = `round(bán lẻ × configs.coefficient_ecommerce_price)` khi cờ sửa tay tắt; lưu 3 cờ `is_manual_*_online` (chỉ loại 6) | :2690-2722 |
| HĐ5 | `product_units.cost_price` (giá vốn), `liquidation_sale_max_percent`; **không** đụng `buy_price`, `sale_max_percent_coefficient`; reset `flag_price_wait_approve` = 0 | giá vốn đọc ở ~98 file (cột trùng tên ở chứng từ) |
| HĐ6 | Giá hiệu lực: **≤ 1 dòng tương lai / loại giá**, `effect_date > hôm nay`, **`status = 2`**, `flag` 0/NULL; xoá dòng tương lai không còn gửi lên; **không đụng** dòng đã áp (status 1) | cron 01:00 chỉ áp `status = 2 AND flag ≠ 1`; `getData` trả giá hiệu lực > hôm nay cho chứng từ |
| HĐ7 | **Không** đụng `product_company_coefficients.coefficient` (trừ khi chọn QC-3a, khi đó chỉ UPDATE/INSERT cột hệ số, **không xoá dòng**: dòng còn mang trạng thái + 4 ô quản trị HRM) | ERP nhân hệ số lúc đọc |
| HĐ8 | Lưu theo **từng ĐVT trong 1 transaction** (6 giá + giá hiệu lực + giá vốn) | ERP làm vậy; chứng từ đọc giữa chừng không thấy nửa bộ giá |
| HĐ9 | `product_approves`/`product_approve_prices` để trống | `PriceCalculate::approve` :334-358 chặn PTG nếu có dòng chờ duyệt |
| HĐ10 | Nếu vẫn ghi `product_versions`/`product_histories` (QC-9) thì nhớ N26: AUTO_INCREMENT `product_versions` thấp hơn id mồ côi | trùng id phiên bản |

---

## 3. Đối chiếu với "Cấu hình chính sách giá bán nội bộ"

**Hiện trạng HRM:** chỉ có spec + mockup (`man-danh-muc-hang-hoa/design.md` §28, màn `/master-data/internal-price-policies` trong
mockup luồng). Quyền 1656 "Cấu hình chính sách giá bán nội bộ" mới **giữ chỗ**, chưa seed (seeder `:1581`). **0 code, 0 bảng.**
Tồn C6/C7 (trần %, khai trước, ngừng hợp tác) gác lại "sang phase Tính giá" (04/10).

| Khía cạnh | Chính sách giá nội bộ (§28) | Luồng giá ERP hiện tại | Khớp / lệch |
|---|---|---|---|
| Mục đích | **số GỢI Ý** giá mua lại giữa 2 công ty (công ty bán → công ty mua) | giá BÁN ra khách của hàng hoá | **khác bài toán** |
| Ghi bảng giá? | **Không** (§28a-4) | có | chính sách không thay được màn giá |
| Khoá | chủ (công ty bán) × hãng SX × công ty mua | ĐVT × loại giá (không công ty) | lệch chiều |
| Gốc tính | giá vốn × (1+%) hoặc 6 giá bán × (1−%) của **công ty bán** | hệ số giá × giá vốn ra giá bán | dùng chung `price_types` 6 loại |
| Nguồn hàng | 2 tỷ lệ cứng: nhập khẩu nguyên lô / tồn kho | không có | — |
| Hiệu lực | không ngày hiệu lực, có lịch sử | có giá hiệu lực tương lai + cron | lệch |
| Nơi hiện | khối tham khảo trên **Phiếu tính giá** HRM (§29) + cảnh báo lúc lấy hàng về | — | phụ thuộc Phase 7 |
| Quan hệ hệ số giá `pcc` | **độc lập** (§28a-8 nêu độc lập với `manufacture_expect_prices` + `company_price_types`, không nhắc `pcc`) | `pcc` là cơ chế giá chi nhánh đang chạy | **chưa ai chốt** "bỏ hệ số thì HP/Vinh lấy giá ở đâu" |

**Giá theo công ty lưu ở đâu?** Theo chốt A4/A5 thì sẽ là `product_unit_prices.company_id` (NOT NULL) + bảng `product_company_units`
(giá vốn / giá mua ngoài theo công ty). **Chưa có migration, chưa có code đọc.** Chính sách giá nội bộ chỉ cho công ty mua một con số
tham khảo để tự nhập vào bảng giá của mình, nên nó **cần** bảng giá theo công ty đã tồn tại thì mới có ý nghĩa.
⇒ Màn giá làm ở 2-D **không** cần đợi chính sách nội bộ, và ngược lại.

---

## 4. Đề xuất phạm vi

### 4.1 Ba mức phạm vi cho "màn giá HRM trong 2-D"

| Mức | Gồm | ERP đọc phải sửa | Độ lớn (so với 1 đợt con 2-C, vd 2-C2) |
|---|---|---|---|
| **M1 ⭐ — Port "Cập nhật giá nhanh" trên bảng chung** | L1 sang HRM (+ QC-3a hệ số theo hãng nếu chọn); chặn ERP L1, L2 nút thủ công, L5, L7 tạo/lưu, 2 nút ở màn HH; L3/L4/L9/L10 giữ ERP | **0 file** | **≈ 1,5–2 đợt con** |
| M2 — M1 + Phiếu tính giá | + L6 = Phase 7: 4 controller 1.160 dòng, 3 model 2.271 dòng, 18 view 2.413 dòng ERP; mockup HRM (§29, §33o, §33p) **khác ERP** (gom nhóm hãng, 1–n, gắn trạng thái hàng × công ty, khối chính sách nội bộ) ⇒ không phải port mà là thiết kế mới; chuỗi Hỏi giá → Yêu cầu tính giá còn dính hàng tạm (Phase 6) | 0 (nếu vẫn bảng chung) | **+3–5 đợt con** |
| M3 — M1 + giá theo công ty (Hướng B) | migration `product_unit_prices.company_id` + `product_company_units` + gán 264.646 dòng + gỡ hệ số | **34 file ERP + ~16 file HRM + 19 chỗ hệ số** | **phase lớn nhất feature** (nhiều tuần), rủi ro 🔴 giá sai im lặng ở 338 màn |

### 4.2 M1 chi tiết

**Màn HRM "Cập nhật giá hàng hoá"** (1 màn, khuôn list-page + bảng nhập tại chỗ):
- **Danh sách:** mỗi hàng × ĐVT là 1 khối 6 dòng loại giá (rowspan). Cột: Tên · ĐVT (chọn ĐVT nếu hàng có nhiều) · Mã · Model ·
  Hãng SX · phân loại (Loại SP theo cây mới, thay `product_cate`/`product_type` cũ) · Tồn kho · **Giá vốn** · Loại giá · Giá hiện tại ·
  Hệ số · Giá công thức (chỉ đọc; §9: nguồn dữ liệu đứt từ 2020) · Giá mới · ĐMGG · Ngày hiệu lực (1 giá tương lai) · ĐMGG thanh lý ·
  Lưu theo dòng.
- **Lọc:** tên, mã, model, hãng SX (chỉ hãng thuộc công ty hiện tại, theo QC-4), thương hiệu, loại SP, còn tồn / hết tồn.
- **Lưu từng hàng × ĐVT** theo HĐ1–HĐ9, validate y ERP (`updatePrice` :2553-2600), báo lỗi đồng thời mọi ô.
- **BE** (`Modules/MasterData`): 1 controller (list, options, update), 1 service (~400–600 dòng: query list kèm tồn, cổng công ty,
  ghi trong transaction), 1 FormRequest, 1 Resource; tuỳ QC-3a thêm 1 endpoint hệ số theo hãng; tuỳ QC-9 ghi lịch sử. PHPUnit
  ~25–35 ca (HĐ1–HĐ9 + không quyền + sai công ty + ĐVT thiếu dòng loại 5).
- **FE** (`hrm-client`): 1 page + 1 component bảng nhập tại chỗ (chưa có sẵn trong repo, mockup §28 mới là HTML) + menu hub;
  e2e ~15 ca (có quyền / không quyền / khác công ty; đo DOM bảng rowspan).
- **Quyền HRM (guard `api`)**: 1 quyền ghi "Cập nhật giá hàng hoá" (gate cả vào màn lẫn xem giá vốn, như ERP chỉ trả `cost_price`
  khi có quyền :2331, :2512). Id còn trống: 1656 đã giữ cho chính sách nội bộ; **1657–1659, 1662–1669, 1679+** trống (DB local đã
  có 1676–1678 của nhánh khác) ⇒ chọn lúc plan, kiểm `uniq -d`.
- **Migration:** không (dùng bảng ERP sẵn có). Có thể +1 nếu QC-9 chọn bảng lịch sử riêng.
- **ERP (2-D2b, sau khi màn HRM chạy):** chặn bằng middleware 2-D1 các route `editPrices` :586, `updatePrice` :596,
  `manualUpdatePrices` :609, `approve*Submit` :589-592 + `approvePrices` :587, `manufacture_expect_prices` create/store :3655-3656;
  ẩn menu `topmenubar:944, :945, :2236` + nút `products/list:39`; trỏ link sang HRM. **Giữ** `getProductsAndPrices` (chỉ đọc),
  `expectedPrices`, `priceUpdating`, `price_logs`, `getPriceOfProducts`, `getData*`.
- **Sau M1, ERP vẫn còn ghi giá ở:** Phiếu tính giá (Phase 7), duyệt hàng tạm (Phase 6), cron 01:00, cron 14:30 (N5, để sau).
  Phải ghi rõ trong plan để không ai tưởng "ERP đã hết ghi giá".

### 4.3 Chia 2-D1 / 2-D2?

**Đề xuất: CÓ.**

| | 2-D1 — ERP không lỗi (phần không phải giá) | 2-D2 — Màn giá HRM rồi chặn giá ERP |
|---|---|---|
| Nội dung | toàn bộ khảo sát A (trừ luồng giá) + B M1–M7 + Q10 `barcode_template_type` + chặn CRUD Hãng SX/Thương hiệu (Q2) + bỏ menu HH ERP (Q1) | mục 4.2 |
| Repo | ERP (nhánh mới từ `gop_db`) + HRM (migration Q10) | HRM chủ yếu + ERP nhỏ |
| Điều kiện production | **Bắt buộc** (popup 338 màn, ghi đè hàng gốc…) | **Không bắt buộc**: luồng giá ERP ghi đúng bảng chung, không làm hỏng dữ liệu HRM |

Hệ quả nếu chia:
- 2-D1 lên trước, **luồng giá ERP chạy nguyên** trong menu Kế toán. Chỉ mất nút "Hàng chưa có công khoán" (nếu không đặt lại link) và
  nút "Cập nhật giá" trên màn HH (vẫn vào được từ menu Kế toán).
- Ngay khi 2-D1 lên, **hệ số giá đóng băng** (2.4). Nếu QC-3 chọn (a) thì phần hệ số theo hãng nên kéo **vào 2-D1** (nhỏ), không
  đợi 2-D2.
- Không chia: 2-D (bắt buộc trước production) phải đợi thêm 1,5–2 đợt con của màn giá. Và nếu phạm vi trượt sang M2/M3 thì
  production bị chặn theo.

---

## 5. Câu hỏi nghiệp vụ cho user (chỉ điều chưa chốt; hỏi LẦN LƯỢT)

> Tự quyết, không hỏi: bố cục bảng/lọc theo cây phân loại mới; port y validate ERP; HĐ1–HĐ9; cờ chờ duyệt mồ côi tự về 0 khi lưu
> (đúng nhánh "không duyệt" của ERP); id quyền; tên màn/menu.

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **QC-0** | Biết rằng giá ERP có **menu riêng ở Kế toán** (bỏ menu HH chỉ mất 2 nút), màn giá HRM có còn phải nằm **trong 2-D (chặn production)** không? | ⭐ **Tách 2-D1 / 2-D2**: 2-D1 là điều kiện production; 2-D2 (màn giá) làm **ngay sau**, không chặn go-live | Tách: production không đợi màn giá; người dùng tạm làm giá ở ERP menu Kế toán. Giữ gộp: go-live lùi thêm ~1,5–2 đợt con (hoặc lâu hơn nếu QC-1/QC-2 mở rộng). Bỏ hẳn màn giá khỏi 2-D (để Phase 8): ít việc nhất, giá ở ERP tới Phase 8 |
| **QC-1** | "Chuyển hết luồng giá" có gồm **Phiếu tính giá** (chuỗi Hỏi giá → Yêu cầu tính giá → Phiếu; 4.008 lần ghi/6 tháng, 99,8% do 1 người) không? | ⭐ **Không** — 2-D2 chỉ chuyển **Cập nhật giá nhanh** + chặn các đường ghi thủ công; Phiếu tính giá giữ ERP tới **Phase 7** (luồng mới §29/§33 đã thiết kế khác ERP) | Không: 2-D2 gọn (M1); kênh định giá chính vẫn ở ERP thêm một thời gian, ERP chưa "hết ghi giá". Có: phải chốt nốt C1/C3/C4 (§29f) + 33i, làm luồng mới 3–5 đợt con; dính hàng tạm (Phase 6) vì 100% yêu cầu tính giá đi từ Yêu cầu hỏi giá |
| **QC-2** | **Giá theo công ty** (A4/A5 Hướng B) làm trong 2-D2 hay để phase riêng? | ⭐ **Phase riêng (Phase 8)** — 2-D2 ghi **bảng giá chung** như ERP | Phase riêng: 0 file đọc ERP/HRM phải sửa, rủi ro thấp; màn giá HRM hôm nay = giá chung, chi nhánh vẫn ra giá bằng hệ số. Làm luôn: thêm 34 file ERP + ~16 file HRM + gán 264.646 dòng; 7 công ty không có dòng giá nào ngày bật (§25e) ⇒ phải chuẩn bị nhập liệu |
| **QC-3** | Sau 2-D1 **không còn màn nào sửa hệ số giá theo công ty** (form HH + thẻ của Hãng SX đều chặn), trong khi 07–08/2026 vừa sinh 722 dòng cho HP/Vinh. HRM có cần chỗ sửa hệ số **tạm** tới khi có giá theo công ty không? | ⭐ **(a) Có — khối "Hệ số giá theo công ty" theo HÃNG** trên HRM (port thẻ của màn Hãng SX: áp cho mọi hàng của hãng; chỉ UPDATE/INSERT cột hệ số, không xoá dòng), làm **ngay trong 2-D1** | (a) chi nhánh giữ được giá chênh cho hàng mới; thêm 1 endpoint + 1 khối UI (nhỏ); phải bỏ khi làm QC-2. (b) Đóng băng tới Phase 8: hàng mới của hãng ở HP/Vinh/SG bán **bằng giá TPE** (thấp hơn 2–5% so với cách hiện nay) cho tới khi có giá riêng. (c) Giữ thẻ hệ số ở màn Hãng SX ERP (trái N2/Q2 đã chốt — thẻ xoá sạch dòng trạng thái HRM) |
| **QC-4** | Màn giá HRM: **ai được sửa giá mã nào** khi bảng giá còn chung? | ⭐ **Giữ luật ERP**: hãng SX của hàng **và** công ty tạo hàng (`products.company_id`) đều phải = công ty đang làm việc (HRM lấy theo `company_role`) | Giữ luật ERP: không đổi thói quen; Cty 1 sửa ~gần hết. Chỉ theo công ty tạo hàng (luật chủ HRM): 367 hàng có hãng khác công ty tạo đổi người được sửa. Mọi công ty có quyền đều sửa: một công ty sửa là giá đổi cho **cả 8 công ty** (bảng chung) |
| **QC-5** | Hàng HRM tạo đang **"Đang nhập thông tin"** (giá 0, ERP popup đã thấy vì `status = 1`): màn giá có cho **nhập giá** không, nhập xong có **đổi trạng thái**? | ⭐ **Cho nhập giá, KHÔNG đổi trạng thái** (trạng thái chờ luồng Tính giá Phase 7) | Cho nhập, không đổi: hàng HRM bán được ở ERP với giá thật; HRM vẫn hiện "Đang nhập thông tin" (lệch nhãn tới Phase 7). Không cho: hàng HRM tạo giá 0 tới Phase 7 ⇒ chưa bật HRM tạo hàng thật được (H1''). Cho + chuyển "Đang kinh doanh": thành lối tắt bỏ qua Tính giá, trái §26/§29a-1 |
| **QC-6** | **Duyệt giá** (0 lần dùng, `is_company_price = 0` cả 8 công ty): port sang HRM hay bỏ? | ⭐ **Bỏ** — không port, chặn 5 route ERP + ẩn menu "Danh sách hàng hoá chờ duyệt giá bán" | Bỏ: gọn; nếu công ty muốn bật duyệt giá sau này phải làm mới. Port: thêm bảng duyệt + màn + thông báo, không ai đang dùng |
| **QC-7** | **Cập nhật giá theo hãng** (87 phiếu, dừng 12/2022): port hay bỏ? | ⭐ **Bỏ** — chặn tạo/lưu ERP, giữ màn xem lịch sử phiếu cũ | Bỏ: mất công cụ tăng giá hàng loạt theo % cho cả hãng (chưa ai dùng 3 năm). Port: +1 màn + logic sinh giá hiệu lực hàng loạt |
| **QC-8** | **Công khoán + ghi chú**: ERP `updatePrice` ghi luôn `products.norm` (công khoán) và `products.note` (ghi chú hàng hoá); PTG cũng ghi `products.note`. Màn giá HRM có cho sửa 2 ô này không? Còn "**Import công lắp đặt**" (ghi `norm` + `tech_coefficient` hàng loạt) và "**Hàng chưa có công khoán**" (xuất Excel) thì sao? | ⭐ Màn giá HRM **chỉ hiện, không sửa** `norm`/ghi chú (sửa ở form hàng hoá theo 3 mức quyền). Import công lắp đặt: **chặn** (2-D1), ghi backlog màn HRM. Xuất "Hàng chưa có công khoán": **giữ route ERP chỉ đọc**, đặt link ở menu Kế toán → Giá bán | Theo ⭐: thông tin chung chỉ một chủ. Nhưng người làm giá (Ban điều hành / kế toán) không có quyền 1652 của công ty tạo thì không sửa được công khoán, và phải sửa từng mã tới khi có import HRM. Cho sửa trên màn giá: tiện cho người làm giá nhưng lách luật chủ thông tin chung (§26c-bis, T6) |
| **QC-9** | **Lịch sử thay đổi giá**: ERP ghi `product_versions/product_histories` (xem ở tab Lịch sử của màn HH ERP, mà màn này bỏ menu ở Q1). HRM làm thế nào? | ⭐ **Ghi lịch sử kiểu HRM** (khuôn `entity-history`), có popup *Lịch sử giá* trên màn giá; ngừng ghi `product_versions` | HRM: tra được ai đổi giá gì, lúc nào; +1 bảng/khuôn lịch sử, cần thêm thời gian. Vẫn ghi `product_versions`: không ai xem được nữa (menu bỏ) và dính N26. Không ghi (hoãn như §14b): mất vết đổi giá trong thời gian chờ |
| **QC-10** | 2 cron giá + các màn chỉ xem (*Trạng thái cập nhật giá*, *Hàng sắp điều chỉnh tăng giá*, *Nhật ký cập nhật giá* đọc file log trên máy chủ ERP): chuyển HRM hay giữ ERP? | ⭐ **Giữ ERP**: cron 01:00 vẫn áp giá hiệu lực do HRM ghi (HĐ6), email + nhật ký giữ nguyên; chỉ chặn nút "cập nhật thủ công" (`manualUpdatePrices`, GET có ghi); N5 để sau như đã chốt | Giữ: 0 việc, chạy ổn; người dùng xem trạng thái/nhật ký ở ERP, sửa giá ở HRM (2 nơi). Chuyển: thêm scheduler HRM + 3 màn + chuyển chỗ lưu file log |

**Thứ tự hỏi đề xuất:** QC-0 → QC-1 → QC-2 → QC-3 → QC-4 → QC-5 → QC-8 → QC-9 → QC-6 → QC-7 → QC-10
(QC-0/1/2 quyết phạm vi; QC-3 có thể kéo việc vào 2-D1).
