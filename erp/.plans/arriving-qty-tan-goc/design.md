# Trị tận gốc "Hàng đang về" (arriving_qty) — Design Phase 0

> Trạng thái: **Phase 0 (design thuần, CHƯA code, CHƯA ghi DB)** — chờ user review.
> DB điều tra: `hrm_erp_gop` (prod gộp, erp.eteksofts.com). Repo `TanPhatDev`, nhánh `gop_db`.
> Ngày: 2026-10-12.

---

## 1. Triệu chứng gốc (ca 48475)

SP `product_id=48475`, `company_id=1`: user báo "hàng đang về = 25" nhưng **báo cáo luân
chuyển kho không hiện** (`/admin/stock-transfer/report`). HĐ mua user chỉ: buy_contract2 998.

### Truy vết đầy đủ ca 48475 (2 chuỗi tách bạch)

**Chuỗi A — các dòng ĐẶT CHO KHÁCH** (orderable_type `OrderRequestProductDetail2` 5757/5856/5857
+ `OrderSummaryProduct2` 14807): PI 1158 → BC 886 → Invoice2 764 → CustomDeclaration 787 →
`ProductImportRequest 14212`. **Mọi dòng `order_stock_progress.qty = 0`** → đã nhập về hết.
Thực tế đã nhập: PNH-14352 (type 11, cty 1, 25) rồi điều chuyển sang cty 4 (PNH-14816/27/34/43,
type 7, Σ25).

**Chuỗi B — dòng ĐẶT TỒN KHO** (orderable_type `OrderRequestProduct2` **8097**, order đơn qty=0,
PDHNK-03649): PI 1218 **(−25)**, BC 933 (0), Invoice2 797/800/804/806 (0), BC 998 (0),
CustomDeclaration 824 **(+25, duyệt hôm nay 2026-10-12)**. **Σprogress = −25 + 25 = 0.**

### Cơ chế lỗi (đã xác định chắc chắn)

`order_stock_progress` là **sổ cái từng bước**: mỗi dòng = SL đang nằm ở 1 chứng từ. Tiến 1 bước =
`+qty` bước sau, `−qty` bước trước. Với 1 dòng bình thường, chuỗi bắt đầu bằng **mầm +N** lúc tạo
đơn, nên `Σprogress = N` khi chưa về, `= 0` khi về hết.

Dòng 8097 có **order đơn qty = 0** (đặt thuần cho tồn kho) ⇒ **mầm +25 lúc tạo đơn KHÔNG bao giờ
được ghi**. Nhưng bước lùi `PI −= 25` vẫn chạy ⇒ PI 1218 kẹt **−25**, CD 824 **+25**, Σ = 0.

Hệ quả: fix reconcile ngày 2026-10-07 (`reconcileArrivingFromProgress`) set
`order_request_product2.arriving_qty = Σprogress = 0`; còn `root_order_request_products` giữ 25.
Báo cáo đọc cột phẳng `order_request_product2.arriving_qty = 0` ⇒ **không hiện**. **Sự thật nghiệp
vụ = 25** (đã lên tờ khai hải quan, chưa nhập kho).

---

## 2. Chẩn đoán gốc rễ — tại sao "cứ nay lỗi mai lỗi"

Không phải 1 bug. Vấn đề là **kiến trúc không có nguồn sự thật duy nhất**. "Hàng đang về" được lưu
thành **cột phẳng denormalized `arriving_qty`** trên **~10 bảng** (ngoại + inland + root + summary),
được bảo trì bằng **~40 phép `+=`/`−=` rải rác ở 12 cụm controller/model** (mục 5A). Song song là
sổ cái `order_stock_progress` cũng bị mutate tại chỗ ở 12 cụm khác (mục 5D). **Hai nguồn này phải
tự đồng bộ bằng tay** — mỗi lần thêm/sửa luồng là một cơ hội lệch.

Từ 5 lần fix trước (mục 6), lệch đến từ **3 lớp khác bản chất**:

| Lớp | Bản chất | Ví dụ đã gặp | Vá được bằng |
|---|---|---|---|
| **(a) Bug cộng/trừ sổ cái** | Typo/sai cột/sai id khi `+=`/`−=` | `objectable_id` thay `objectable_type` (2 nơi); `buy_contract2_id` trên bảng inland không có cột đó; không gom phụ lục HĐ | **Code** — đã có helper `OrderStockProgress::subtractQty/addQty/capToQty/contractFamilyIds` chuẩn hóa (vụ #3, **chưa commit**) |
| **(b) Mầm thiếu** | Dòng qty=0 (đặt tồn kho) không có mầm +N ⇒ Σ sai nền | **Ca 48475 chính là lớp này** | **Code** (ghi mầm đúng) + **reconcile** (dựng lại nền) |
| **(c) Desync cấu trúc** | Hàng về qua **chuỗi PI song song** không link lại dòng đặt gốc | vụ #2 orp2#6789 (phantom 54) | **Không có dòng code đơn lẻ.** Chỉ reconcile ở **grain sản phẩm+công ty** hoặc kỷ luật quy trình |

> Lớp (c) là lý do phương án "compute per-line thuần" KHÔNG đủ: arrival bị book sang dòng khác thì
> tính riêng từng dòng vẫn lệch. **Phải chốt grain = sản phẩm + công ty** thì mới bền với (c).

### Quy mô drift hiện tại (đo trên prod 2026-10-12)

- `order_request_product2` (ngoại): **428** dòng có arriving≠0 hoặc Σprogress≠0 → **81 dòng
  (≈19%) lệch** giữa cột phẳng và sổ cái (vi phạm chính invariant của hệ).
- **Σprogress < 0** (bất khả thi): **30 dòng** = 14 `OrderRequestProduct2` + 8
  `InlandOrderRequestNewProductDetail` + 1 `InlandOrderRequestNewProduct` + 7
  `OrderRequestProductDetail2`.

Đây là **lệch hệ thống**, không phải ca lẻ.

---

## 3. Công thức canonical (ĐÃ VALIDATE trên prod)

**Định nghĩa nghiệp vụ:** `đang về = (đã lên chứng từ mua với NCC) − (đã nhập về kho) − (đã hủy)`.

Chốt grain **(product_id, company_id)**:

```
đang_về(product, company)
  = PIPELINE NGOẠI:  Σ purchase_invoice_product_delivery_customers.qty         -- đã đặt NCC (ngoại)
                   − Σ product_import_details.qty WHERE product_imports.type = 11
  + PIPELINE NỘI:    Σ inland_purchase_invoice_product_delivery_customers.qty  -- đã đặt NCC (nội)
                   − Σ product_import_details.qty WHERE product_imports.type = 15
  − Σ (đã hủy, gộp qua bộ lọc status)
```

**Điểm chốt quan trọng:**
- Anchor "đã đặt NCC" lấy ở **điểm cam kết mua bất biến sớm nhất = PurchaseInvoice** (qua bảng tách
  khách `*purchase_invoice_product_delivery_customers.qty`), đếm **1 lần/đơn vị** — KHÔNG cộng dồn
  qua PI+BC+Invoice+CD (1 đơn vị xuất hiện ở cả 4 bước → double-count).
- **"Đã nhập" = CHỈ `product_imports.type IN (11, 15)`** — đây là tập AUTHORITATIVE, suy từ
  **single writer `ProductImport::updateWarehouse()`**: quét đủ mọi nhánh `if ($this->type == ...)`
  trong hàm, **chỉ** 2 nhánh giảm `arriving_qty`:
  - **type 11** `MUA_HANG_NUOC_NGOAI_MOI` (nhập khẩu mới) → pipeline NGOẠI, trừ bằng
    `purchase_invoice_product_delivery_customers`.
  - **type 15** `MUA_HANG_TRONG_NUOC_TU_DO` (mua trong nước tự do + hãng) → pipeline NỘI, trừ bằng
    `inland_purchase_invoice_product_delivery_customers`.
  - MỌI type còn lại KHÔNG đụng arriving: trả lại 3/4/9, điều chuyển 5/6/7/17, gửi 14, ghép/tách
    8/10, zitec 16, khác 99, **và cả type 2 `MUA_HANG_TRONG_NUOC` cũ** (nhánh ở dòng ~1515 không
    giảm arriving — luồng legacy, không dùng cơ chế đang-về). Đây là lý do **không** được trừ các
    type này: arriving chỉ được BƠM VÀO bởi 2 luồng mua mới (11/15), nên chỉ 2 loại nhập đó rút ra.
- ⚠️ `product_imports` **KHÔNG có cột `company_id`** (đính chính giả định cũ) — grain công ty của
  phiếu nhập phải suy qua `warehouse_imports`/`warehouses.company_id` (hoặc created_by).
- Inland dùng đúng bộ bảng `inland_*` ở cả 2 vế (+/−), không trộn với pipeline ngoại.

**Validate ca 48475 / cty 1:**

| Thành phần | Giá trị |
|---|---|
| ΣPI_qty ngoại (PI 1158 = 25 + PI 1218 = 25) | **50** |
| Σ nhập type 11 (PNH-14352) | **25** |
| Σ nhập type 15 (nội, ca này 0) | **0** |
| Σ hủy | 0 |
| **⇒ đang về** | **50 − 25 = 25** ✓ (khớp user) |

Đối chiếu per-line: Chuỗi A đã nhập hết (đang về 0) + Chuỗi B ở hải quan chưa nhập (đang về 25) =
**25**. Grain sản phẩm+công ty cho kết quả đúng kể cả khi arrival book sang dòng khác (bền với lớp c).

---

## 4. Kiến trúc trị tận gốc (ĐỀ XUẤT) — tối thiểu regression

> Mục tiêu user: **sửa được lỗi hiện tại** + **KHÔNG đẻ lỗi mới cho phiếu dở dang & phiếu mới.**

### Nguyên tắc

1. **Nguồn sự thật duy nhất = chứng từ bất biến** (PI / product_import / hủy). `arriving_qty` (cột
   phẳng) **và** `order_stock_progress` **đều chỉ là CACHE** của phép suy ra ở mục 3.
2. **GIỮ `order_stock_progress` làm sổ cái** (KHÔNG gỡ bỏ). Lý do: báo cáo popup + 25+ điểm ghi đã
   wire sâu vào nó; gỡ ra = đúng kịch bản "lòi lỗi mới" user sợ. Thay vào đó biến nó thành cache
   **dựng lại được 100% từ chứng từ**.
3. **Self-heal:** 1 lệnh `arriving:reconcile` dựng lại cache từ chứng từ, **idempotent**, chạy được
   bất kỳ lúc nào → mọi drift (a)(b)(c) tự lành. Đây là "van an toàn" thay cho việc đi vá từng ca.
4. **Single-writer:** mọi luồng khi đổi chứng từ chỉ gọi **1 hàm recompute** cho (product, company)
   liên quan, thay cho `+=`/`−=` rải rác. Hàm này = chính logic reconcile thu hẹp phạm vi.
5. **Guard bất biến:** sau mỗi ghi, chặn `arriving_qty < 0` và `arriving_qty > đã_đặt − đã_nhập`
   (log cảnh báo, không cho âm).

### Vì sao đây là phương án tốt nhất cho yêu cầu "không đẻ lỗi mới"

- **Phiếu dở dang & mới:** single-writer recompute = luôn tính lại từ chứng từ hiện có ⇒ không phụ
  thuộc thứ tự thao tác, không tích lũy lệch. Phiếu đang làm dở chỉ cần đi qua luồng là tự đúng.
- **Phiếu cũ đã lệch:** `reconcile` quét 1 lần, chữa cả 81 dòng + 30 dòng âm mà **không cần vá tay
  từng ca** (khác hẳn 5 lần fix trước — mỗi lần chỉ nắn 1 ca).
- **Nền có sẵn:** đã tồn tại `UpdateArrivingQtyToRootOrderRequestsSeeder` +
  `UpdateArrivingQtyProductSeeder` (tính lại arriving từ chứng từ, mirror logic ghi) và helper
  `OrderStockProgress::*` (vụ #3). Ta **chuẩn hóa & hợp nhất** chúng thành 1 service, không viết mới
  từ đầu.
- **Rủi ro có kiểm soát:** mọi ghi DB đều **dry-run trước, review, rồi mới apply** (xin phép riêng).

---

## 5. Bản đồ nơi GHI / ĐỌC / GATE (blast radius)

### 5A. Ghi `arriving_qty` (cột phẳng) — 12 cụm
`OrderRequest2::addCustomerStockEntry` (391/419/431/436/441/499…653) · `InlandOrderRequestNew::
addCustomerStockEntry` (350…538) · `PurchaseInvoice::syncProducts` (521/549/561/585/590) ·
`InlandPurchaseInvoice::syncProducts` (527…593) · `InlandProductArrivedNew::syncDetails`
(359/384/499) · `BuyContract2Controller::reOrder` (1459/1495) · `InlandBuyContractNewController::
reOrder` (1167/1200) · `PurchaseInvoiceController::reject` (284/300/312) ·
`InlandPurchaseInvoiceController::reject` (284/300/312) · `ProductImport::updateWarehouse`
(1336…1509) · `ProductImportRequest::approve` (1621/1626) · 3 seeder data-fix.

### 5B. Đọc để HIỂN THỊ / báo cáo
`StockTransferReportService::getData` → `display_stock_order` tổng từ **6 cột arriving** (1979 &
bản sao 3981) · `Product::stockIncoming` popup (2651) · `Product::stockCompaniesSearchData` /
`stockSearchData` (display_stock_order 5798/8185) · `ProductTemplate` bản sao (5369/7512) ·
`RootOrderRequestController::stockIncoming` popup (968) · `InlandBuyContractNew::getDataForEdit`
(324/362).

### 5C. Đọc để GATE NGHIỆP VỤ (⚠️ rủi ro regression cao nhất — phải test kỹ khi đổi nghĩa)
- `InlandBuyContractNew::canProductArrived` @1020: `whereRaw('qty - arrived_qty - arriving_qty > 0')`
  — chặn tạo "báo hàng về" inland.
- `RootOrderRequestController::getListOrderCompany` @918: `havingRaw('SUM(qty - (arrived+arriving)
  - annex) >= ?')` — chặn chọn HĐ mua không đủ lượng.
- `ProductImport::updateWarehouse` @1460/1473/1481: `min($qty_available_for_stock, $customer->qty)`
  — SL nhập kho phụ thuộc arriving.

### 5D. `order_stock_progress` (sổ cái) — ghi ở 12 cụm (Invoice2, PurchaseInvoice, OrderRequest2,
BuyContract2Controller, CustomDeclarationController approve/cancel, OrderImportRequest,
ProductImport, + bộ inland), đọc để popup chi tiết ở `StockTransferReportService::getStockTranfer`
(4266) + `getEmpStockTranfer` (5438) qua `capToQty`.

---

## 6. Kế thừa từ 5 plan cũ (không làm lại)

- **fix-so-cai-hang-dang-ve-lech-popup** — đã dựng helper `OrderStockProgress::subtractQty/addQty/
  capToQty/contractFamilyIds` (gom "họ hợp đồng" gốc+phụ lục, log khi tra hụt thay vì nuốt). Code
  **CHƯA commit** (6 file). → **Tái dùng/mở rộng, đừng viết lại.**
- **fix-bao-cao-luan-chuyen-hang-dang-ve-phantom** — chốt invariant thực tế `arriving_qty ==
  Σorder_stock_progress.qty`; lớp (c) desync parallel-chain; data fix 1 ca (fix54.php). Hướng chống
  tái diễn (reconcile khi nhập / job rà) **vẫn chờ user chốt** — Phase này chính là câu trả lời.
- **fix-ton-kho-dang-ve-gop-nham-dong-ton-kho** — arriving ghi ở **2 cấp** (sản phẩm cho dòng tồn
  kho vs detail cho dòng khách); typo `objectable_id`. Code đã push master.
- **chan-nhap-ton-kho-dang-ve-hang-dat-cong-ty** — guard FE+BE chặn chọn "nhập tồn kho đang về" cho
  item thuần đặt công ty. Liên quan trực tiếp dòng qty=0 (lớp b).
- **fix-stock-transfer-report-wer-prepick** — bug SQL thiếu cột, không liên quan drift.

---

## 7. Roadmap (chia task, trị tận gốc)

- **Phase 0 (ĐANG — design thuần):** chốt công thức + bản đồ + quy mô drift. **← tài liệu này.**
- **Phase 1 (read-only):** `ArrivingQtyService::compute(product, company)` (và breakdown per-line)
  từ chứng từ + lệnh `php artisan arriving:reconcile --dry-run` in bảng diff (current vs computed)
  toàn hệ. **Không ghi DB.** Hợp nhất 2 seeder cũ + helper OrderStockProgress.
- **Phase 2 (heal data):** `reconcile` apply (idempotent, backup trước, dry-run review THEN write).
  **Cần user duyệt riêng + chọn phạm vi** (toàn hệ hay từng công ty). Chữa 81 + 30 dòng.
- **Phase 3 (single-writer):** thay `+=`/`−=` ở 12 cụm (5A) bằng recompute per-flow. Làm
  **flow-by-flow** (ngoại trước: PI→BC→Invoice→CD→import; rồi inland; rồi điều chuyển), mỗi flow 1
  sub-task + regression test. **Fix mầm thiếu** (lớp b) tại gốc ghi mầm.
- **Phase 4 (chống tái phát):** cron `arriving:reconcile --dry-run` cảnh báo lệch hằng đêm + guard
  bất biến `0 ≤ arriving ≤ đã_đặt − đã_nhập` sau mỗi ghi.
- **Phase 5:** ghi chú kỷ luật port sang HRM (HRM bê logic kho ERP — phải bê cả single-writer).

---

## 8. Câu hỏi chờ user chốt trước khi sang Phase 1

1. **Grain chốt ở (product, company)** — đồng ý? (cần để bền với lớp c desync parallel-chain).
2. **Giữ `order_stock_progress` làm cache dựng-lại-được** (không gỡ bỏ) — đồng ý hướng này thay vì
   thay bằng view compute-on-read?
3. ~~**"Đã nhập" = chỉ `product_imports.type = 11`**~~ — **ĐÃ TỰ GIẢI (2026-10-12):** tập đúng =
   **`type IN (11, 15)`**, suy từ single writer `ProductImport::updateWarehouse()` (chỉ 2 nhánh này
   giảm `arriving_qty`; type 11 = ngoại, type 15 = nội; mọi type khác kể cả type 2 legacy không
   đụng arriving). Xem mục 3. **Không cần user chốt.**
4. **"Đã hủy"** lấy ở đâu là chuẩn? (hủy PI / hủy tờ khai `CustomDeclarationController::cancel` /
   reOrder). Hướng tự giải: gộp vào **bộ lọc status** trên PI (`purchase_invoices.status` active)
   và trên import (chỉ đếm phiếu nhập đã duyệt) — xác nhận lại khi chạy drift map đầy đủ.
5. Phase 2 chữa data: **toàn hệ 1 lần** hay **từng công ty** (giảm blast radius)?
