# Plan — Fix phantom "Hàng đang về"

> ⬇️ HƯỚNG CHỐT 2026-10-12 (document-truth) ở ngay dưới. Mọi mục Oct-7 (Fix A/B/C, reconcile
> ledger, B' sửa write-path) GIỮ LÀM LỊCH SỬ — đã bị thay thế, KHÔNG thực thi tiếp. Xem design.md.

## HƯỚNG CHỐT — tính TẬN GỐC từ chứng từ (user "ok" 2026-10-12)

### Verify còn lại (chỉ SELECT prod, DB chậm → chạy nền, lọc toàn bảng không lọc product_id)
- [x] Cột `type` PI-giao: 1=khách(KD), 2=tồn(Tồn kho) — verify ca 48475 (15 / 35).
- [x] `completed_qty` không đáng tin (=0 dù nhập 25) → trừ từ product_import_details, không dùng.
- [ ] Toàn bảng PI-giao (ngoại+nội) có `type` nào khác 1/2 không → quyết xử lý "khác".
- [ ] product_import_details có truy về dòng PI-giao/nhánh khách-tồn không
      (pi_product_delivery_id / order_request2_id / order_request_detail2_id) → chọn (a) trừ đúng
      nhánh vs (b) fallback ưu tiên Tồn kho.
- [ ] Inland grain + cột `type` của inland_purchase_invoice_product_delivery_customers.
- [ ] Phiếu nhập chờ duyệt (chưa status=1): tính hay không vào "đang về".
- [ ] Sanity 1 SP "sạch": KD/Tồn/Tổng mới khớp report hiện tại.

### Code — plan chi tiết: xem "## PLAN TRIỂN KHAI CHI TIẾT" bên dưới.

### Phiếu cũ cần rà (yêu cầu user "rà phiếu cũ xoá/sửa") — RIÊNG, sau khi fix hiển thị
- [ ] Quét PI treo lâu không về (vd SP 26687 cty1 31,692 / 0 phiếu nhập ~1 năm) → danh sách.
- [ ] HỎI USER điều kiện đóng/hủy PI treo; xử qua UpdateDB, dry-run trước. KHÔNG tự quyết xóa.

### Checkpoint — 2026-10-12
Vừa hoàn thành: design.md document-truth; verify prod ca 48475 (type1=15/type2=35, nhập type11=25
  → 25 đúng); loại completed_qty + detail_type (luôn=1); USER DUYỆT SPEC + chốt 2 mặc định (phiếu
  nhập chờ duyệt vẫn tính đang về; rà phiếu cũ tách riêng). Viết plan triển khai chi tiết.
Đang làm dở: chưa viết code, chưa ghi data. .env trỏ hrm_erp_gop = PROD (chỉ SELECT).
Bước tiếp theo: Task 0 (probe truy vết import↔pidc + ca 5384) → code ArrivingQtyService.
Blocked: để trống.

---

## PLAN TRIỂN KHAI CHI TIẾT (document-truth)

**Spec:** `.plans/fix-bao-cao-luan-chuyen-hang-dang-ve-phantom/design.md`

### Ràng buộc chung (áp cho MỌI task)
- DB `.env` = `hrm_erp_gop` (PROD). Giai đoạn code/test: **chỉ SELECT trên prod**; chạy test ghi
  (nếu có) trên **DB test**, KHÔNG prod. Trước mỗi lần tinker: `grep -E '^DB_' .env`.
- "Đã nhập" = `product_imports.type IN (11 ngoại, 15 nội) AND status = 1`. Phiếu nhập **chờ duyệt
  (status≠1) VẪN tính đang về** (không trừ).
- Addend "NCC đã giao" = PI còn hiệu lực: `purchase_invoices.status = 1` (ngoại) /
  `inland_purchase_invoices.status = 1` (nội).
- Tách KD/Tồn ở **addend** theo `type` dòng PI-giao: **1 = khách (KD), 2 = tồn (Tồn kho)**.
- grain = (company_id, product_id). company của phiếu nhập theo `warehouse_imports.company_id`
  (join qua `product_imports.warehouse_import_id`); company PI theo `purchase_invoices.company_id`.
- Truy vấn **gộp toàn bảng rồi GROUP BY**, KHÔNG lọc theo `product_id` trong WHERE (optimizer chọn
  plan tệ → treo). Lọc product_id (nếu cần) làm ở PHP sau khi gộp.
- **KHÔNG** sửa ~40 chỗ `+=`/`-=`, `ProductImport::updateWarehouse()`, `ProductTemplate.php` (code
  chết); **KHÔNG** backfill `arriving_qty`. Chỉ đổi NGUỒN ĐỌC ở reader live.
- Không commit/push khi chưa có yêu cầu. Không sửa hàm dùng chung ngoài danh sách này khi chưa hỏi.
- ERP = Laravel 8 / PHP 7.4 / AngularJS. UpdateDB chạy qua tinker.
- "Test" của fix này = **probe script đối chiếu giá trị đã biết** (ca 48475 = 25; ca 5384 hết ảo)
  + verify trình duyệt — ERP không có harness unit-test cho data. Mỗi task kết thúc bằng 1 lần đối
  chiếu như vậy.

---

### Task 0 — Probe ground-truth, chốt cơ chế tách số-trừ KD/Tồn  ✅ XONG 2026-10-12
**Files:** scratchpad (read-only): t0_trace.php, t0_5384_inland.php.

- [x] **B1/B2:** ca 48475: PI-giao active KD(type1)=15, Tồn(type2)=10+25=35; import pid#45451 qty=25
      có `order_import_detail_id` RỖNG + pidc type2 cũng rỗng `order_request_detail2_id` ⇒ **cơ chế
      (a) KHÔNG khả thi** (link đã mất). → **CHỐT cơ chế (b): trừ Tồn kho trước, tràn sang KD**
      (nhập kho = bổ sung tồn vật lý). ca 48475 → KD=15, Tồn=10, Tổng=25.
- [x] **B3:** ca 5384 document-truth = **144** (addend 426 − nhập 282), KHÔNG tự hết "54 ảo". Cái 54
      là **dòng PI còn status=1** (pidc#15070 PO bị thay thế) ⇒ **PI treo, xử ở phần rà phiếu cũ**,
      không phải lỗi công thức. Đóng dòng đó → 90. ĐÃ đính chính design.md.
- [x] **B4:** inland `type`: chỉ {1,2} (type1 n=6083, type2 n=1010) — KHÔNG có giá trị lạ. OK.
- [x] **B5:** design.md đã cập nhật §Tách (cơ chế b), §Cần verify (tick), §Phiếu cũ (thêm 5384),
      §Phụ lục (đính chính "5384 không tự hết").

---

### Task 1 — `ArrivingQtyService` (ngoại trước), validate ca 48475  ✅ XONG 2026-10-12
Đã tạo `app/Services/Warehouse/ArrivingQtyService.php`. php -l sạch. ca 48475 cty1 →
KD=15 Ton=10 Tong=25 ✓; ca 5384 → Tong=144 (PI treo, đúng). build toàn bảng ~0.6s.

**Files:**
- Create: `app/Services/Warehouse/ArrivingQtyService.php`
- Test: `scratchpad/t1_service.php` (probe đối chiếu)

**Interfaces — Produces:**
```php
namespace App\Services\Warehouse;
class ArrivingQtyService {
    /** @return array map "{company_id}|{product_id}" => ['kd'=>float,'ton'=>float,'tong'=>float]
     *  Nơi đang dùng: StockTransferReportService (getData/getDataExport/getStockTranfer/
     *  getEmpStockTranfer), Product (stockIncoming/stockCompaniesSearchData/stockSearchData),
     *  RootOrderRequestController::stockIncoming. */
    public function byProductCompany(?array $productIds = null): array
    /** Tổng đang về 1 (company, product) — tiện cho reader cần 1 số. */
    public function tongFor(int $companyId, int $productId): float
}
```

- [ ] **B1:** Viết `t1_service.php`: gọi `(new \App\Services\Warehouse\ArrivingQtyService)
      ->byProductCompany([48475])` rồi in `['1|48475']`. Chạy trước khi tạo service → FAIL
      (class not found). (bước "test đỏ")
- [ ] **B2:** Tạo service. `byProductCompany`:
      - **addend ngoại**: 1 query gộp
        `purchase_invoice_product_delivery_customers pidc JOIN purchase_invoice_products pip
         ON pidc.pi_product_id=pip.id JOIN purchase_invoices pi ON pi.id=pidc.purchase_invoice_id
         AND pi.status=1`, `GROUP BY pi.company_id, pip.product_id, pidc.type`,
        `SUM(pidc.qty)`. → gom thành kd (type=1) / ton (type=2) theo (company|product).
      - **trừ ngoại**: 1 query gộp
        `product_import_details pid JOIN product_imports pim ON pid.parent_id=pim.id
         AND pim.type=11 AND pim.status=1 JOIN warehouse_imports wi
         ON wi.id=pim.warehouse_import_id`, `GROUP BY wi.company_id, pid.product_id`,
        `SUM(pid.qty)`. ⚠️ xác nhận FK `product_import_details.parent_id = product_imports.id` ở B2
        Task0 (cột `parent_id` có trong schema).
      - Áp cơ chế (a)/(b) từ Task 0 để trừ vào kd/ton; `tong = max(0, kd) + max(0, ton)` (hoặc
        `max(0, addend_tong − tru_tong)` nếu (b)). Mỗi nhánh bọc `GREATEST(0, …)`.
      - `$productIds` != null → lọc Ở PHP sau khi gộp (không nhét vào WHERE).
- [ ] **B3:** `php -l app/Services/Warehouse/ArrivingQtyService.php` → sạch.
- [ ] **B4:** Chạy `t1_service.php` → kỳ vọng `['kd'=>?, 'ton'=>?, 'tong'=>25]` cho 1|48475
      (Tổng = 25 khớp user; kd/ton theo cơ chế đã chọn).
- [ ] **B5:** (không commit — chờ yêu cầu).

---

### Task 2 — Thêm nhánh INLAND vào service  ✅ XONG 2026-10-12
Nhánh inland viết chung trong service (addend ngoại+nội, trừ type 11+15). Validate SP 26687 cty1
(inland lớn nhất) → Tong=31.692 khớp tính tay. Bảng/cột: inland_purchase_invoice_products
(product_id), join ipidc.inland_pi_product_id=ipip.id, invoice qua inland_purchase_invoice_id.

**Files:** Modify `app/Services/Warehouse/ArrivingQtyService.php`; Test `scratchpad/t2_inland.php`.

- [ ] **B1:** Viết `t2_inland.php`: chọn 1 SP có cả addend inland (từ B4 Task0) → in kết quả service,
      so với query thủ công inland. Chạy → giá trị inland hiện = 0 (chưa cài) → "đỏ".
- [ ] **B2:** Thêm vào `byProductCompany`:
      - **addend nội**: `inland_purchase_invoice_product_delivery_customers ipidc
        JOIN inland_pi_products ... JOIN inland_purchase_invoices ipi ON ipi.status=1`,
        `GROUP BY ipi.company_id, product_id, ipidc.type`, `SUM(ipidc.qty)` → cộng vào kd/ton.
        (xác nhận tên bảng `inland_pi_product`/cột `inland_pi_product_id` ở B2.)
      - **trừ nội**: `product_import_details` của `product_imports.type=15 status=1`, cùng pattern
        join `warehouse_imports` → trừ. (nếu trừ ngoại+nội chung 1 query `type IN (11,15)` được thì
        gộp — nhưng company/nhánh phải tách đúng; an toàn thì 2 query.)
      - type nội ∉ {1,2}: xử theo B4 Task0.
- [ ] **B3:** `php -l` sạch.
- [ ] **B4:** Chạy `t2_inland.php` → inland khớp query thủ công; ca 48475 (ngoại) vẫn = 25.

---

### Task 3 — Đổi nguồn cụm cột "Hàng đang về" trong `StockTransferReportService`

**ĐÍNH CHÍNH 2026-10-12 (khi mở report ra): cơ chế trong plan cũ ("chạy xong rồi gán ở PHP")
KHÔNG khớp cấu trúc thật. Chốt lại:**
- `getData`/`getDataExport` trả về **query builder** (controller phân trang), `display_stock_order`
  (Tồn) + `display_employee_order` (KD) là **alias SQL** cộng từ 7+3 mảnh ledger (dòng 1978-1988),
  rồi lại dùng trong SQL để tính tồn tối thiểu (dòng 2016). ⇒ phải nối bằng **SQL (leftJoin)**,
  không post-process PHP (nếu gán PHP sau, cột min-stock tính trong SQL vẫn đọc số cũ).
- `getStockTranfer`/`getEmpStockTranfer` = **popup CHI TIẾT** liệt kê từng dòng chứng từ + ngày về
  (StockTransferReportController 255/268, getTableArrivedPrint cho bản in). Document-truth là số
  GỘP → không dựng lại dòng chi tiết. **USER CHỐT hướng (B)**: dựng lại chi tiết từ **dòng PI-giao
  thật** để popup khớp cột chính. **Tách Task 3b riêng**, làm sau khi cột chính verified.
- **Single-source**: `ArrivingQtyService` sở hữu luôn SQL (perCompanySql / perProductSql); cả
  byProductCompany (Product.php/controller) lẫn report dùng chung SQL đó → KHÔNG đẻ bản SQL thứ 2.

**Files:** Modify `app/Services/Warehouse/ArrivingQtyService.php` (thêm perCompanySql/perProductSql,
refactor buildFullMap dùng chung SQL) + `app/Services/OrderReports/StockTransferReportService.php`
(getData, getDataExport); Test `scratchpad/t3_report.php`.

- [x] **B0 (service):** ✅ 2026-10-12 Refactor xong: perCompanySql()/perProductSql()/buildFullMap
      dùng chung SQL. Verify: 48475 cty1 kd=15/ton=10/tong=25 (không đổi), perProductSql(1,48475)=
      ton10/kd15, 5384=144, 26687=31692, build 0.45s, php -l sạch.
- [x] **B1:** ✅ 2026-10-12 `scratchpad/t3_report.php` gọi getData/getDataExport cho 48475/5384.
- [x] **B2:** ✅ 2026-10-12 getData + getDataExport (replace_all, 2 hàm cùng lúc): leftJoin
      `(SELECT product_id AS arriving_product_id, kd AS arriving_kd, ton AS arriving_ton FROM
      (perProductSql(companyId,productId)) arriving_pp) as arriving_dt` ON `sub.id = arriving_product_id`;
      `display_stock_order = COALESCE(arriving_dt.arriving_ton,0)`,
      `display_employee_order = COALESCE(arriving_dt.arriving_kd,0)`. Bỏ cụm 7 mảnh + 3 mảnh cũ.
      companyId/productId lấy từ `$request->company_id/product_id` (null = gộp). Alias riêng tránh
      đụng `['*']`. Min-stock (2016) auto đúng. GIỮ LẠI leaf subquery arriving cũ vì còn nuôi mảng
      *_ary cho popup (Task 3b).
- [x] **B2b:** ✅ 2026-10-12 getDataExport dùng CHUNG edit replace_all (thân giống hệt getData).
- [x] **B3:** ✅ `php -l` sạch.
- [x] **B4:** ✅ 2026-10-12 t3_report.php: 48475 cty1 Tồn=10/KD=15/Tổng=25; gộp mọi cty y hệt;
      5384 cty1 Tổng=144 (KD144/Tồn0, hết phantom 90); getDataExport 48475 Tồn=10/KD=15. 5384
      stock_setting_stock tự tính lại = 37.

### Task 3b — Dựng lại popup CHI TIẾT từ dòng PI-giao (hướng B, sau Task 3)
**Files:** `StockTransferReportService::getStockTranfer` (4290) + `getEmpStockTranfer` (5462) +
`getTableArrivedPrint` (4252, bản in) + `StockTransferReportServiceExcel` (xuất excel chi tiết) +
3 blade mở popup (orders/reports/stock_transfer/index 839/858; common/warehouse_warnings/reports/js 92;
warehouse/warehouse_reports/stock_companies_product 626).

**Chốt với user 2026-10-12:** popup liệt kê gộp từng dòng PI-giao + 1 dòng trừ "đã nhập kho"; bản in
thể hiện nhất quán (có dòng trừ, tổng khớp cột chính). ✅

**Thiết kế đã chốt:**
- Nguồn record = từng dòng `purchase_invoice_product_delivery_customers` (ngoại) / `inland_...` (nội)
  của PI status=1, lọc `type` theo popup: Tồn (getStockTranfer) = type≠1, KD (getEmpStockTranfer) = type=1.
  Mỗi record: link PI, link_contract (HĐ mua), qty (SL trên phiếu) + qty_base (×unit_coefficient),
  warehouse_date = expected_time, name = người lập PI, name_department (popup KD/print).
- Dòng điều chỉnh: **adjustment = Σ dòng gross − net** (net = ArrivingQtyService kd/ton của
  (company,product)). Vì net = GREATEST(0, gross − …) ≤ gross nên adjustment ≥ 0. Hiện 1 dòng
  "Đã nhập kho" qty = −adjustment (link/contract rỗng) → **Σ hiển thị = net = cột chính**. KHÔNG cần
  lặp lại logic ton-first trong popup (gross−net tự đúng cho cả 2 popup).
- Service dùng chung: thêm `ArrivingQtyService::deliveryLines(?companyId, productId, $scope='ton'|'kd')`
  trả raw dòng PI-giao (doc-truth: dòng nào tính); report resolve code/link/creator/unit.

**Phát hiện mới cần user chốt phạm vi (vượt ngoài "popup+in" đã ok):**
- (a) **company_id chưa được thread** vào 3 popup opener (chỉ gửi product_id + *_ary). Hướng B query
  theo product → PHẢI thêm `company_id` (lấy từ `$scope.form.company_id`) để khớp khi report lọc 1 cty;
  rỗng = gộp mọi cty. Sửa 3 blade.
- (b) **Có nút Xuất Excel chi tiết** (`stock_transfer_report.export` type=customer →
  StockTransferReportServiceExcel) đang đọc nguồn cũ → nên dựng lại đồng bộ.
- (c) unit_coefficient của dòng PI-giao: cần resolve để ra qty_base.

- [x] **B0:** ✅ 2026-10-12 User "ok" full package (a)+(b)+(c); company_id lấy từ bộ lọc công ty report.
- [x] **B1:** ✅ 2026-10-12 `ArrivingQtyService::deliveryLines(?companyId, productId, scope)` (UNION ngoại+nội,
      lọc type theo scope, resolve contract_code qua buy_contract2 / inland_buy_contract_news bằng
      GROUP_CONCAT, qty_base = qty×unit_coefficient). Probe `scratchpad/t3b_lines.php`: 48475 cty1
      ton Σgross35−adj25=10 ✓, kd 15−0=15 ✓; gộp mọi cty y hệt; 5384 ton 267→0, kd 159−15=144 ✓.
- [x] **B2:** ✅ 2026-10-12 Thay THÂN getStockTranfer(ton)/getEmpStockTranfer(kd) = `buildArrivingDetail($request,$scope)`
      (helper private dùng chung). Record: code=pi_number, link PI (purchaseInvoice/inlandPurchaseInvoice.show),
      contract_code, name/name_department (Employee::with info.department), warehouse_date=expected_time,
      qty + qty_base; +1 dòng "Đã nhập kho" = −(Σgross−net), qty_base theo tỉ lệ net/gross. Giữ lọc
      code/contract_code/name_department + return ['title','result']. Xoá ~1670 dòng logic OrderStockProgress cũ.
      Probe `scratchpad/t3b_popup.php`: cả 4 ca foot đúng net, đơn vị set/Bộ & piece/Cái, lọc code OK. `php -l` sạch.
- [x] **B2b:** ✅ 2026-10-12 Print (print/printEmp) + Excel chi tiết (export/exportEmp) đều gọi
      getStockTranfer/getEmpStockTranfer → `getTableArrivedPrint($result)`; record shape khớp sẵn
      (code/contract_code/qty/warehouse_date/name_department/name) → tự đồng bộ, KHÔNG sửa thêm.
- [x] **B3 (code):** ✅ 2026-10-12 Thread company_id vào opener 3 blade (phủ cả popup + in + xuất vì
      `.print-button-detail` dùng `$.param($scope.warning)`): stock_transfer/index (form.company_id,
      cả openWarningWarehouse + openEmpWarningWarehouse), warehouse_warnings/reports/js (openWarningArriving,
      form.company_id), stock_companies_product (openWarningWarehouse, user_company_id). Rỗng = gộp mọi cty.
- [ ] **B3 (verify):** Mở trình duyệt popup + in + excel foot đúng cột chính (gộp vào Task 5 B2).

---

### Task 4 — Mở rộng ArrivingQtyService = nguồn DUY NHẤT đủ 2 kênh "đang về"
**Files:** Modify `app/Services/Warehouse/ArrivingQtyService.php`; Test `scratchpad/t4_service.php`.

**QUYẾT ĐỊNH NGHIỆP VỤ (user "có" 2026-10-12):** kênh **điều chuyển / nhập theo phiếu** LÀ
hàng đang về, song song với kênh **mua (PI)**. Service phải tính ĐỦ 2 kênh:
- **KD** = purchase_kd (PI-giao type 1, doc-truth) + `product_import_buy_employee` (import **type=2**).
- **Tồn** = purchase_ton (PI-giao type≠1 − đã nhập, doc-truth) + `product_import_employee_order`
  (import type∉[1,2,11,14,15]) + `warehouse_product_import_rd` (wir type 10) + `warehouse_product_import_r`
  (wil type 8).
- Grain (company_id, product_id), qty THÔ cross-unit (khớp report cũ). Company = parent.company_id.
- Kênh import TỰ net qua `status` (phiếu xong rời khỏi SUM) → KHÔNG trừ riêng; KHÔNG trùng purchase
  (khác type/bảng). Phần trừ "đã nhập kho" (type 11/15) CHỈ áp cho purchase → tách purchase floored
  TRƯỚC rồi mới UNION import (additive, luôn ≥0).

- [x] **B0:** ✅ 2026-10-12 User chốt "có" — gộp kênh điều chuyển vào định nghĩa đang về.
- [x] **B1:** ✅ Tách `purchaseCompanySql()` (floored kd/ton) + `importCompanySql()` (4 nhánh,
      SELECT company_id parent, product_id, kd, ton). `perCompanySql()` = SUM(A UNION ALL B)
      GROUP BY company,product. Thêm hằng `IMPORT_SINCE`. php -l sạch.
- [x] **B2:** ✅ Mở rộng `deliveryLines()` + `importDeliveryLinesSql()`: scope kd→pir_buy; scope
      ton→pir_emp+wir+wil, cột khớp kênh A, filter khớp importCompanySql. buildArrivingDetail
      thêm `$routeMap` source→route (productImportRequest/warehouseImportRequest/warehouseImport.show).
- [x] **B3:** ✅ php -l sạch cả 2 file.
- [x] **B4:** ✅ `t4_service.php`: 48475 giữ kd15/ton10/tong25; kênh B 289 ô khớp 100% 4-truy-vấn-rời;
      kênh A 48475 cty1 = kd15/ton10 (import=0). `t4b_popup.php`: SP có kênh B gross==net adj=0 foot OK;
      48475 ton gross35/net10/adj25/total10, kd gross15/net15/total15 — khớp benchmark.

---

### Task 4b — Swap 4 reader sang service (report Task 3 tự đồng bộ)
**Files:** Modify `app/Product.php` (stockCompaniesSearchData:~5352, stockSearchData:~7685,
stockIncoming:~2651); `app/Http/Controllers/Order/RootOrderRequestController.php` (stockIncoming:~968);
Test `scratchpad/t4_readers.php`.

- [x] **B1 (Nhóm A — report tồn):** ✅ 2026-10-12. Cả 2 hàm: chèn `leftJoin(DB::raw('(SELECT product_id
      AS arriving_product_id, kd AS arriving_kd, ton AS arriving_ton FROM (perProductSql) ...)'))` sau
      khi chuỗi leftJoinSub kết thúc; đổi `display_employee_order = COALESCE(arriving_dt.arriving_kd,0)`
      + `display_stock_order = COALESCE(arriving_dt.arriving_ton,0)`. Giữ leftJoinSub cũ (còn feed *_ary).
      **Quyết định company-scope theo từng hàm (đọc đầu hàm + nhánh arriving cũ):**
      - `stockCompaniesSearchData` (đa kho, group theo product, KHÔNG scope 1 cty) → `perProductSql(null,null)`
        = all-company, khớp nhánh arriving cũ vốn không lọc cty.
      - `stockSearchData` (báo cáo 1 cty, có `$request->company_id`) → `perProductSql($request->company_id,null)`.
        Việc này SỬA LUÔN bug tiềm ẩn cũ: nhánh arriving cũ ở hàm này là all-company (lệch scope), và cột
        display cũ nhét `product_import_employee_order` (pier) vào CẢ KD lẫn Tồn (double-count) — swap sang
        nguồn-duy-nhất tự hết.
      - ✅ **DEVIATION — ĐÃ XỬ LÝ 2026-10-12 (user đồng ý "ok làm"):** `whereRaw` ngưỡng tồn-tối-thiểu
        của `stockSearchData` (dòng 8137) trước tham chiếu cột arriving CŨ (`inland_stock_order +
        stock_order + product_import_employee_order`) → mất đồng bộ với cột hiển thị (nguồn-duy-nhất).
        Hệ quả: SP bị cache ảo thổi phồng → bộ lọc tưởng "sắp về đủ" → GIẤU cảnh báo cần đặt hàng.
        **FIX:** thay bằng `COALESCE(arriving_dt.arriving_ton, 0)` — CHỈ phần đang về NHẬP KHO (không
        cộng KD = hàng giao thẳng khách, vì không vào kho). Join `arriving_dt` đã có sẵn trong hàm
        (dòng 8078-8079) nên hợp lệ. Dấu ngoặc cân, `php -l` cần chạy lại ở B3 verify.
- [x] **B2 (report Task 3):** ✅ 2026-10-12 (verify, KHÔNG sửa code). getData/getDataExport gọi chính
      `perProductSql` — mà sau Task 4 `perProductSql` đã gộp `purchaseCompanySql` + `importCompanySql`
      (kênh B). Popup gọi `deliveryLines` (UNION ngoại+nội). → report + popup TỰ có kênh import, chứng
      minh theo cấu trúc; `t4_service.php` (Task 4 B4) đã khớp 289 ô kênh B với 4-truy-vấn-rời.
- [x] **B3 (Nhóm B — in phiếu ĐH):** ✅ 2026-10-12. `Product::stockIncoming($pid,$unit=null)` → bỏ thân
      UNION 7-nhánh, thay = `DB::selectOne(perProductSql(null,$pid))` trả `kd+ton` (all-company).
      `RootOrderRequestController::stockIncoming` (theo cty login) = `tongFor($companyId,$productId)`.
      **per-unit → per-product:** `t4b_multiunit.php` (phiên trước) xác nhận 1/5325 SP có >1 đơn-vị-đặt
      → immaterial, KHÔNG cần hỏi user. Consumer in: `RootOrderRequestPrintService:199`.
- [x] **B4:** ✅ 2026-10-12. `php -l` sạch cả 3 file. `t4b_readers.php`: SP 48475 CẢ 4 reader = **25**
      (KD=15, Tồn=10, Tổng=25 — khớp mốc). byProductCompany xác nhận 48475 chỉ "đang về" ở cty1 nên
      reader all-company (#1,#3) = reader cty1 (#2,#4) = 25.

---

### Task 5 — Verify toàn cục trên trình duyệt + chốt KD/Tồn với user
**Files:** không sửa code; `scratchpad/t5_sanity.php`.

- [x] **B1:** ✅ 2026-10-12 `t5_sanity.php`: mốc khớp — **48475 KD=15/Tồn=10/Tổng=25**; **5384 Tổng=144**
      (ĐÚNG chứng từ, chưa đóng PI treo); **26687 Tồn=31,692** (PI treo). Quét 25 SP + toàn cty1
      (2995 SP có đang-về, Σ=305,092) → **0 dòng âm, 0 bất nhất** (floor GREATEST(0,…) đảm bảo).
- [x] **B2:** ✅ 2026-10-12. User restart server (nạp `.env` PROD `hrm_erp_gop`) + tự đăng nhập.
      Mở `admin/stock-transfer/report`, set company=1 + product=48475 + năm 2026 qua Angular scope,
      gọi `filter()`. Kết quả render: nhóm cột **"Hàng đang về" KD=15 · Tồn kho=10 · Tổng=25** (đúng mốc,
      hết "-"/phantom); scope.datas[0]._products[0]: display_employee_order=15, display_stock_order=10,
      sum_display_stock_qty=25. Ảnh: `scratchpad/report-48475-dangve-clean.png`.
- [ ] **B3:** Trình user cách chia KD/Tồn cho ca 48475 (từ cơ chế Task 0) để user xác nhận đúng ý;
      nếu user muốn đổi quy tắc chia → chỉnh service (chỉ phần attribution).
- [ ] **B4:** Báo cáo user: xong hiển thị. Hỏi chuyển sang việc **rà phiếu cũ (PI treo)** — làm
      riêng, hỏi điều kiện đóng/hủy trước khi đụng data.

---

# LỊCH SỬ (Oct-7, ĐÃ BỊ THAY THẾ bởi hướng document-truth ở trên)

## Điều tra (xong)
- [x] Xác định report SUM Sổ B gộp nhiều chặng (StockTransferReportService::getData, display_stock_order).
- [x] Trace ca 54 ảo: pidc#15070 available=54, PO phục vụ bị thay thế (PNH-13030/13841).
- [x] Quét toàn cty 1: 2 chữ ký phantom (over-book 5 root/151đv; dạng PO chết như ca 54).
- [x] Xác nhận arriving âm chỉ nhiễu (6 dòng/-14); số 15438/6722 lần đầu là sai.

## Fix A — merge under/over-serve (code, ĐÃ LÀM)
- [x] OrderRequest2::addCustomerStockEntry 3 nhánh: trừ remain_qty theo $detail->qty / $customer->qty; amount theo $detail->qty (dòng 387, 494, 590, 600).
- [x] php -l sạch.
- [ ] Verify lại trên trình duyệt sau khi user chốt hướng.

## Fix B — Sổ A đa chặng (HÀM DÙNG CHUNG, chờ xác nhận)
- [ ] CHỜ USER: có sửa OrderStockProgress::subtractQty để trừ cả progress "bóng" ở các chặng khác không?

## Fix C — teardown PO/PI "chết" (CHỜ USER chốt điều kiện)
- [ ] HỎI USER: điều kiện nào coi một PO/PI (còn active) là "đã chết / bị thay thế" để giảm arriving?
- [ ] Sau khi chốt: viết detector + hàm giảm arriving (code) + backfill data (UpdateDB).

## Dữ liệu
- [ ] 5 root over-book cty1 (sau khi chốt luật): nắn arriving về đúng.
- [ ] Các ca dạng-2 (PO chết): xử lý theo luật đã chốt.

## Checkpoint — 2026-10-07 (cũ)
Vừa hoàn thành: điều tra xong, chốt 2 chữ ký phantom, xác nhận Fix A còn trong code.
Đang làm dở: chờ user chốt điều kiện teardown (Fix C) + có cho sửa hàm dùng chung subtractQty (Fix B).
Bước tiếp theo: báo cáo user + hỏi 1 câu điều kiện "PO/PI coi như chết".
Blocked: cần user trả lời trước khi ghi data / sửa hàm dùng chung.

---

## NGUYÊN NHÂN THẬT + FIX ĐÃ GHI PROD (2026-10-07, thay cho hiểu nhầm over-book phía trên)

### Bất biến đúng (đã chứng minh toàn hệ thống)
`arriving_qty` đúng = **GREATEST(0, Σ order_stock_progress − arrived_qty)**
= (lượng ĐẶT về) − (lượng ĐÃ nhập kho).
- Sổ A (`order_stock_progress`) chốt lượng đặt về 1 lần ở chặng **BuyContract2** (các chặng khác
  ghi qty=0 đánh dấu chuyển chặng), và chỉ TRỪ khi **gộp cho khách**; **KHÔNG trừ khi nhập kho**.
- Cột phẳng `arriving_qty` mới là nơi trừ lúc nhập kho → nhưng bị drift (teardown/gộp/nhập kho
  quên trừ hoặc trừ sai). Report chỉ đọc cột phẳng → thừa/thiếu "hàng đang về".
- Kiểm: KHỚP 1723/1748 dòng; 25 dòng lệch = dòng lỗi.

### Bẫy đã tránh (dry-run cứu)
Công thức sai `max(0, ΣA)` (quên `− arrived_qty`) định BƠM +5646 đơn vị phantom vào 62 dòng đã
nhập kho xong (ΣA còn lượng đặt về, flat đã về 0 đúng). Dry-run lộ → sửa công thức.

### Data fix — ĐÃ COMMIT PROD
- [x] `UpdateDB::reconcileArrivingFromProgress_20261007($dry=true)` (database/seeds/UpdateDB.php,
      cuối class) — nắn `arriving_qty := GREATEST(0, ΣA − arrived_qty)` cho MỌI dòng có bút toán
      sổ chặng, cả order_request_product2 (DEPT) + order_summary_product2 (PO).
- [x] Dry-run duyệt 25 dòng → user chốt "ok ghi".
- [x] Chạy `(false)` COMMIT: **25 dòng DEPT nắn, 0 dòng PO, net report −93 đv**. Gồm cả 7 ca gốc.
- [x] Xác nhận sau ghi: dry-run lại = 0 dòng lệch toàn hệ thống.
- [x] Kiểm "vá hết": 0 dòng report-visible (arriving>0) nào thiếu bút toán → bao phủ 100%.

### Còn lại (chờ user chọn hướng)
- [ ] Chống tái phát: (1) cron sentinel chạy reconcile định kỳ (dòng crontab RIÊNG); HOẶC
      (2) sửa đúng write-path làm lệch flat lúc nhập kho/teardown; HOẶC (3) report đọc thẳng công
      thức `max(0, ΣA − arrived)` thay vì cột phẳng (bỏ hẳn cột cache).
- [ ] Verify lại trên trình duyệt report stock-transfer.

## PHÁT HIỆN 2026-10-07 (chạy lại v27 + v28) — bất biến KHÔNG áp được cho 3 bảng còn lại

Chạy v27 (bất biến 6 bảng) + v28 (phân rã chặng 10 dòng lệch/bảng):

- 2 bảng DOMESTIC cha ĐÃ VÁ vẫn sạch: DEPT 1748 khớp/0 lệch, PO 180/0. INLAND PO 3/0 sạch.
- **INLAND DEPT** (feed cột chính report) 965 khớp / **36 lệch** (Σflat 353 → Σđúng 114).
  Chặng đặt KHÔNG cố định ở 1 chặng: lúc InlandProductArrivedNew, lúc InlandPurchaseInvoice,
  lúc InlandBuyContractNew; có dòng ΣA ÂM (id770 BuyContract −35). → ΣA inland KHÔNG = "lượng đặt"
  sạch như BuyContract2 domestic ⇒ recompute `max(0,ΣA−arrived)` CHƯA chứng minh đúng cho inland.
- **DETAIL domestic** (order_request_product_detail2, feed cột employee_order) 6661 khớp /
  **106 lệch**. BẪY CHẾT: rất nhiều dòng **ΣA=0** (progress chỉ là MỐC chặng qty=0) nhưng flat>0
  là số THẬT (id912 flat=360 ΣA=0 arrived=0 → recompute sẽ ZERO 360 đv hợp lệ). ⇒ ở bảng detail,
  order_stock_progress KHÔNG phải nguồn sự thật cho lượng ⇒ **recompute SẼ PHÁ DATA**.
- **INLAND DETAIL** 5983 khớp / **36 lệch** — cùng kiểu detail (mix ΣA=0 và ΣA có số).

KẾT LUẬN: KHÔNG được chạy reconcile recompute cho 3 bảng này như 2 bảng domestic cha.
Detail: recompute phá data (ΣA=0 ≠ không có hàng về). Inland cha: ΣA không sạch, cần soi write-path
inland (InlandProductArrived/InlandPurchaseInvoice ghi arriving thế nào) trước khi quyết.
CHƯA GHI DATA, CHƯA SỬA CODE INLAND. Chờ user chốt hướng (xem câu hỏi cuối chat).

## ĐÀO INLAND 2026-10-07 (v29+v30) — 36 "lệch" phần lớn LÀ BÁO ĐỘNG GIẢ

- Báo cáo đọc inland: `inland_stock_order = SUM(io.arriving_qty)` từ `inland_order_request_new_products`
  (StockTransferReportService:1423-1431), filter: `or.status=DA_DUYET(1)` + `p.created_at>'2024-07-01'`
  + `p.arriving_qty>0`. Báo cáo dùng **CỘT PHẲNG làm sự thật**, KHÔNG đọc sổ chặng ΣA.
- Write-path inland ghi `arriving_qty` bằng `+=/-=` tích luỹ rải 6 file (InlandOrderRequestNew,
  InlandProductArrivedNew, InlandPurchaseInvoice, InlandBuyContractNewController,
  InlandPurchaseInvoiceController) → non-idempotent (rủi ro drift tiềm ẩn như lost-update domestic).
- QUAN TRỌNG: sổ chặng inland đã `+=/-=` nên **ĐÃ là số đang-về ròng** ⇒ bất biến đúng của inland là
  `arriving == ΣA` (H1/H2), KHÔNG phải `max(0, ΣA − arrived)` (H3 = công thức domestic).
  Kiểm trên tập report-visible 132 dòng INLAND DEPT: H1/H2 khớp 125/132, H3 chỉ 99/132.
  ⇒ 36 "lệch" ở v27 phần lớn là ÁP NHẦM CÔNG THỨC (báo động giả). INLAND PO visible 2/2 sạch.
- Còn lại **7/132 dòng nghi vấn thật** (flat>0 nhưng ΣA=0/âm): id 767,768,770,771,773,775 (CÙNG
  giây 2025-09-30 14:18:39 ⇒ 1 phiếu/1 thao tác) + 902 (2025-10-08). Tổng tối đa ~76 đv.
  CHƯA kết luận các dòng này SAI: ở inland cột phẳng là nguồn chính, sổ chặng là phụ → phải truy
  chứng từ gốc (HĐ mua inland qty đặt vs lượng đã nhận) mới biết flat hay progress đúng.
- CHƯA GHI DATA. KHÔNG chạy reconcile recompute cho inland (sẽ phá 125 dòng đang đúng).

## Checkpoint — 2026-10-07 (mới nhất) — TẠM DỪNG, xử lý việc khác
Vừa hoàn thành: tìm ra bất biến thật, viết + chạy reconcile, GHI PROD 25 dòng, xác nhận sạch.
USER ĐÃ CHỐT HƯỚNG: **B'** = sửa write-path `ProductImport::updateWarehouse()` làm `arriving_qty`
  thành ĐẠI LƯỢNG DẪN XUẤT idempotent: `arriving = max(0, ΣA − arrived)` thay cho phép trừ tích lũy
  `arriving_qty -= ...` (không idempotent → drift khi SỬA/DUYỆT LẠI phiếu nhập đã duyệt;
  ProductImportsController:1398 gọi lại updateWarehouse khi status==1). Nhánh ngoại còn lỗi
  `arrived_qty =` (gán đè) thay vì `+=` như nhánh nội địa.

PHÁT HIỆN QUAN TRỌNG trước khi dừng (cần xử khi quay lại): report "Hàng đang về"
  (`ProductTemplate.php` display_stock_order dòng 5364-5372, nhân bản ở `Product.php`) đọc
  `arriving_qty` từ **4 BẢNG**, reconcile cũ mới phủ 2/4:
    1. order_request_product2        (stock_order)            ✓ ĐÃ VÁ 25 dòng
    2. order_summary_product2        (stock_po_arriving_qty)  ✓ 0 drift
    3. inland_order_request_new_products   (inland_stock_order)      ✗ CHƯA kiểm/vá
    4. inland_order_summary_new_products   (stock_po_tn_arriving_qty)✗ CHƯA kiểm/vá
  Cột RIÊNG display_employee_order (5360) đọc thêm order_request_product_detail2 +
  inland_order_request_new_product_details (DETAIL) — chưa kiểm.
  Probe read-only đã soạn: scratchpad/v27.php (kiểm bất biến 6 bảng) — CHƯA CHẠY.
  Đã xác nhận: ΣA = lượng đặt, chặng ProductImportRequest KHÔNG trừ (0 âm/1352) ⇒ recompute idempotent.

Đang làm dở: chưa sửa dòng code nào của updateWarehouse. .env trỏ hrm_erp_gop = PROD (chỉ SELECT).
Bước tiếp theo khi quay lại: chạy v27 kiểm bất biến 4+2 bảng → vá recompute idempotent ở nhánh
  nhập của updateWarehouse (cả MUA_HANG_NUOC_NGOAI_MOI + MUA_HANG_TRONG_NUOC_TU_DO) cho các cột
  đã chứng minh → php -l → test re-run trên DB test (KHÔNG phải prod) → bàn deploy.
Blocked: để trống (tạm dừng theo yêu cầu user để xử lý việc công tác phí HRM).

## Ngày 29/10/2026 (@junfoke)
- [x] 29/10/2026 — BC luân chuyển hàng hoá: cột Hàng đang về ra số lẻ (PI 25WHGC123). Nguyên nhân: PNH không trỏ tới dòng HĐ mà tới phiếu THCPNK / dòng phụ lục, `ArrivingQtyService` chia số đã về theo tỉ lệ cho các dòng HĐ; dòng HĐ 16 bộ đã huỷ vẫn được tính. Sửa: bỏ dòng HĐ đã huỷ (`1f2c64885a`), chia theo FIFO — dòng lập trước nhận đủ trước (`a573797942`), gop_db.
- [x] 29/10/2026 — Prod ra 0 hết dù local đúng → nhờ user chạy SQL prod (MySQL 8.0.46) để đối chiếu. FIFO chỉ ảnh hưởng 5 phiếu THCPNK thiếu lẻ 1–2 cái (phần còn về dồn vào dòng HĐ lập sau cùng, tổng cột vẫn đúng) → giữ FIFO. Soạn câu giải thích ngắn cho người dùng. Kiểm sau deploy: GC-GC-40PRO-A:06 Hàng đang về KD 20 / Tồn 40.
