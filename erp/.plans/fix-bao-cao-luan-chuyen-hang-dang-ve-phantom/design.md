# Fix báo cáo "Hàng đang về" — tính TẬN GỐC từ chứng từ (KD / Tồn kho / Tổng)

> Cập nhật 2026-10-12. Thay thế hoàn toàn hướng "sửa cache / reconcile ledger" của 07/10
> (giữ lại phần điều tra cũ ở mục **Phụ lục — Lịch sử điều tra** cuối file làm bối cảnh).

## Mục tiêu

Báo cáo `admin/stock-transfer/report`, nhóm cột **"Hàng đang về"** gồm 3 cột **KD · Tồn kho · Tổng**,
đang hiển thị SAI cả 2 chiều:
- **Phồng (phantom)**: ca SP 5384 (JONN-T21200N) cty 1 từng hiện 144 = 90 thật + 54 ảo.
- **Thiếu / bằng 0**: ca SP 48475 cty 1 hiện `-` (0) trong khi thực tế đang về **25**.

Yêu cầu user (nguyên văn): *"lên 1 phương án xử lý mục tiêu duy nhất để về sau các phiếu mới ko lỗi
nữa. phiếu cũ thì phải rà soát dữ liệu cẩn thận để xoá và chỉnh sửa cho đúng"*.

## Hiện trạng: 3 cột = tổng của ~10 "bộ đếm cache" nhiều chặng

`StockTransferReportService` ghép nhóm "Hàng đang về" từ nhiều mảnh, mỗi mảnh `SUM(arriving_qty)`
với `arriving_qty > 0` trên một bảng chặng khác nhau (dòng 1978 & 1986):

- **KD** = `display_employee_order` (dòng 1986) = `employee_order` + `inland_employee_order`
  + `product_import_buy_employee`
  → nguồn: `order_request_product_detail2` + `inland_order_request_new_product_details` (allocation khách).
- **Tồn kho** = `display_stock_order` (dòng 1978) = `stock_order` + `inland_stock_order`
  + `product_import_employee_order` + `warehouse_product_import_rd/_r` + `stock_po_arriving_qty/_tn`
  → nguồn: `order_request_product2` + `order_summary_product2` + inland tương đương + phiếu nhập + PO.
- **Tổng** = KD + Tồn kho.

`arriving_qty` là **cache (bộ đếm chạy)**: ~40 chỗ code `+=`/`-=` nó mỗi khi hàng chuyển chặng
(đặt → PI → HĐ mua → invoice → nhập kho → teardown/gộp khách). Thiết kế kỳ vọng các chặng **loại trừ
nhau** và tổng luôn = lượng thực đang về. **Chỉ cần sót/sai MỘT lần trừ là drift** — và đã drift thật,
cả lên (phantom) lẫn xuống (về 0).

### Vì sao hướng "sửa cache" (07/10) bế tắc — và đây là lời giải

Phiên 07/10 thử sửa theo bất biến ledger `arriving = GREATEST(0, Σ order_stock_progress − arrived)`:
- Chạy được cho **2 bảng cha domestic** (reconcile 25 dòng, đã commit prod) **nhưng bế tắc** ở
  bảng **DETAIL** và **INLAND**: rất nhiều dòng có **ΣA = 0** mà `flat > 0` là số THẬT
  (progress chỉ là mốc chặng qty=0) → recompute sẽ **ZERO hoá hàng thật**.
- **Ca 48475 chính là lớp này**: dòng order qty=0 (đặt thuần tồn kho) → mầm "+N" không bao giờ ghi
  vào Sổ A → `ΣA = 0` → mọi công thức dựa Sổ A đều ra **0**, dù hàng thật đang về 25.

⇒ **Sổ A (`order_stock_progress`) KHÔNG phải nguồn sự thật về lượng.** Cả nó lẫn cột `arriving_qty`
đều chỉ là cache phái sinh, không đầy đủ. Phải bỏ cả hai khỏi đường tính của báo cáo.

## Quyết định: nguồn sự thật = CHỨNG TỪ GỐC, tính trực tiếp (derive-on-read)

"Đang về" = hàng NCC **đã cam kết giao** (phiếu PI còn hiệu lực) **trừ** hàng **đã nhập kho**.
Hai vế đều là chứng từ, không ai `+=`/`-=` tay → **không drift**. Tính tại thời điểm xem báo cáo.

### Công thức chuẩn (grain = sản phẩm × công ty)

```
Đang về = GREATEST(0,  PI_đã_giao(active)  −  đã_nhập_kho )

Ngoại:  addend = Σ purchase_invoice_product_delivery_customers.qty
                   (JOIN purchase_invoices status = 1)
        trừ    = Σ product_import_details.qty
                   (product_imports.status = 1 AND type = 11, cty theo warehouse_imports.company_id)

Nội:    addend = Σ inland_purchase_invoice_product_delivery_customers.qty
                   (JOIN inland_purchase_invoices status = 1)
        trừ    = Σ product_import_details.qty  (product_imports type = 15, status = 1)
```

- "Đã nhập" = **chỉ type 11 (ngoại) / type 15 (nội)** — user chốt 2026-10-12. Đây đúng là 2 nhánh
  duy nhất trong `ProductImport::updateWarehouse()` có trừ `arriving_qty` → nhất quán single-writer.
- Đã verify prod ca 48475: addend ngoại = 50 (PI 1158 + 1218), trừ type 11 = 25 ⇒ **đang về = 25 ✓**
  (khớp user). Công thức ledger cũ cho 0 ✗.

### Tách KD / Tồn kho — ngay tại nguồn, bằng cột phân loại của PI-giao

Bảng PI-giao có cột **`type`** phân loại allocation (design 07/10 §merge: type 1 = khách, type 2 = tồn)
và còn `type_order_company`, `customer_id`, link `order_request2_id` / `inland_order_request_new_id`.

```
Đang về KD      = GREATEST(0, Σ PI-giao (type = khách)  − phần đã nhập phục vụ khách)
Đang về Tồn kho = GREATEST(0, Σ PI-giao (type = tồn)    − phần đã nhập phục vụ tồn)
Tổng            = KD + Tồn kho
```

- Ánh xạ khớp hiện trạng: KD ≈ allocation khách (nay là `employee_order` từ detail), Tồn kho ≈
  allocation tồn (`stock_order` từ parent/summary).
- **Đã verify prod ca 48475 cty1** (2026-10-12): PI-giao active `type=1` (khách) = **15**,
  `type=2` (tồn) = **35** → addend 50; imports type 11 approved = **25** → đang về = **25 ✓**.
  ⇒ Giá trị cột `type`: **1 = khách (KD), 2 = tồn (Tồn kho)** — xác nhận.
- **`completed_qty` KHÔNG dùng làm số trừ** (đã loại): trên ca 48475 cả hai dòng PI-giao có
  `completed_qty = 0` DÙ đã nhập 25 ⇒ cột này không phản ánh "đã nhận". Phải trừ từ **phía phiếu
  nhập** (`product_import_details`, type 11/15, status 1), không dùng `qty − completed_qty`.
- **Phần trừ (đã nhập) tách KD/Tồn thế nào** — còn 1 điểm cần chốt khi code:
  (a) nếu `product_import_details`/phiếu nhập truy được về dòng PI-giao (qua `pi_product_delivery_id`
      / `order_request2_id` / `order_request_detail2_id`) thì trừ đúng nhánh khách/tồn → chính xác;
  (b) nếu KHÔNG truy được: trừ ở **Tổng** rồi phân bổ **ưu tiên Tồn kho trước, KD sau**
      (số trừ là hàng về nhập kho, mặc định phục vụ tồn) — tự quyết cho đúng nhất, không hỏi user.
  Dù chọn (a) hay (b), **Tổng luôn đúng** (= addend − trừ); chỉ ảnh hưởng cách chia 2 cột con.

## Phạm vi sửa code (CHỈ nơi báo cáo thực sự đọc — "chỉ sửa chỗ dùng")

1. **Thêm service dùng chung** `App\Services\...\ArrivingQtyService` (đặt theo chủ đề, không theo màn):
   - `byProductCompany(array $productIds = null): array` → map `"company|product" => ['kd'=>, 'ton'=>, 'tong'=>]`.
   - 1 truy vấn gộp cho addend ngoại + nội (GROUP BY company, product, type) + 1 cho phần trừ.
     Dùng pattern **gộp toàn bảng rồi lọc** (plan lọc theo product_id bị optimizer chọn tệ → treo).
   - Là nơi DUY NHẤT chứa định nghĩa "đang về". Docblock liệt kê "Nơi đang dùng".

2. **Đổi nguồn 3 cột** trong các **reader LIVE** (chỉ các hàm thực sự chạy trong PM):
   - `StockTransferReportService`: `getData` (68), `getDataExport` (2090), `getStockTranfer` (4266),
     `getEmpStockTranfer` (5438) — cụm leaf `arriving_qty` (1225–1314, 1365–1489…) + ghép
     `display_stock_order` (1978) / `display_employee_order` (1986).
   - `Product.php`: `stockIncoming` (2651), `stockCompaniesSearchData` (5352), `stockSearchData` (7685).
   - `RootOrderRequestController::stockIncoming` (968) — có truy vấn `arriving_qty` tự chứa (974–1052).
   - **KHÔNG đụng** `ProductTemplate.php` (lớp anh em, không reader nào gọi — DEAD) và
     `buy_contract_product_detail2.arriving_qty` (không có writer, luôn 0 — inert).

3. **KHÔNG sửa** ~40 chỗ `+=`/`-=`, **KHÔNG** sửa `ProductImport::updateWarehouse()`,
   **KHÔNG** backfill `arriving_qty`. Cột cache cũ để nguyên (vô hại vì báo cáo không còn đọc).
   Reconcile 25 dòng đã commit 07/10 ⇒ **nay vô hiệu** (không ai đọc cache đó cho báo cáo nữa),
   KHÔNG cần đụng lại.

### Ánh xạ ~10 thành phần cũ → 3 số mới

| Cột báo cáo | Thành phần cũ (cache) | Thay bằng |
|---|---|---|
| KD | employee_order, inland_employee_order, product_import_buy_employee | `ArrivingQtyService` nhánh **khách** |
| Tồn kho | stock_order, inland_stock_order, product_import_employee_order, warehouse_product_import_rd/_r, stock_po_arriving_qty/_tn | `ArrivingQtyService` nhánh **tồn** |
| Tổng | (tổng 2 nhóm trên) | KD + Tồn kho |

> Các mảnh "product_import_*" và "warehouse_product_import_*" (đang CỘNG lượng nhập/nhập-chờ vào
> đang về) là các hack bù trừ chặng — document-truth gộp hết thành một phép trừ sạch. Lưu ý ngữ nghĩa
> **phiếu nhập đang chờ duyệt** (import request chưa status=1): theo công thức, hàng đó vẫn tính
> "đang về" cho tới khi phiếu nhập được duyệt — cần xác nhận đây là hành vi mong muốn (xem "Cần verify").

## Cần verify trước khi code

- [x] Giá trị cột `type` PI-giao: **1 = khách, 2 = tồn** — verify prod ca 48475 (type1=15, type2=35).
      Còn cần quét xem có giá trị `type` khác 1/2 trên toàn bảng không (ngoại + nội) → xử lý "khác" về đâu.
- [x] `completed_qty` KHÔNG đáng tin (=0 dù đã nhập 25) ⇒ **không dùng**; trừ từ `product_import_details`.
- [ ] Phần trừ (đã nhập) có truy được về dòng PI-giao/nhánh khách-tồn không
      (`product_import_details` → `pi_product_delivery_id` / `order_request2_id` / `order_request_detail2_id`)?
      → quyết định (a) trừ đúng nhánh vs (b) fallback ưu tiên Tồn kho.
- [ ] Số KD/Tồn/Tổng mới của một SP "sạch" khớp số báo cáo hiện tại (sanity, tránh lệch toàn hệ thống).
- [ ] Hành vi phiếu nhập đang chờ duyệt (import request chưa status=1): tính hay không tính vào "đang về".
- [ ] Inland: xác nhận grain + cột `type` của `inland_purchase_invoice_product_delivery_customers`
      (schema đã có `type`, `inland_order_request_new_id`, `inland_order_request_new_detail_id`).

## Phiếu cũ cần rà (yêu cầu "rà soát phiếu cũ để xoá/chỉnh cho đúng")

Không backfill cache (số hiển thị tự đúng). Nhưng có **chứng từ thật cần user quyết** — các PI còn
`status=1` nhưng hàng sẽ không về (bị thay thế / treo lâu). Công thức tính đúng theo chứng từ nên
VẪN hiện số này; chỉ đóng/huỷ PI mới làm giảm:
- **SP 26687 cty 1**: 31,692 trên PI còn hiệu lực, **0 phiếu nhập ~1 năm** (09/2025→09/2026).
- **SP 5384 cty 1**: dòng pidc#15070 (54đv, PO phục vụ bị thay thế) còn active → Tổng hiện 144,
  đóng dòng này về **90**.
Cần user xác nhận điều kiện **đóng/hủy** (đổi status). Xử lý RIÊNG, sau khi fix hiển thị, qua
UpdateDB, dry-run trước. Danh sách đầy đủ sẽ quét khi DB rảnh.
- **SP 5384 cty 1 — cùng loại PI treo, KHÔNG tự hết** (verify 2026-10-12): document-truth ra Tổng =
  **144** (addend PI active 426 − nhập type11 282), ĐÚNG BẰNG giá trị "phantom" cũ. Cái "54 ảo"
  (pidc#15070, PO phục vụ bị thay thế) vẫn là **dòng PI đang status=1** nên công thức tính là đang
  về. Đóng/huỷ dòng PI đó → addend còn 372 → **90**. ⇒ xếp chung nhóm "PI treo cần rà", KHÔNG phải
  lỗi công thức.
- ⚠️ **Đính chính:** document-truth chỉ xoá **drift CACHE** (thiếu/thừa do +=/-= sai, như 48475
  under-count). Nó KHÔNG xoá **over-count do PI còn-hiệu-lực-nhưng-hàng-không-về** (5384, 26687) —
  loại này sửa bằng đóng phiếu cũ, không bằng công thức.

## Quyết định đã chốt với user

- "Đã nhập" = **chỉ type 11 (ngoại) / type 15 (nội)**.
- Giữ tách **KD / Tồn kho / Tổng** (user dùng cả 3 cột).
- Hướng **derive-on-read từ chứng từ**, **không ghi data** (1A), **chỉ sửa reader live**.
- Chi tiết "trừ vào KD hay Tồn" để tôi tự quyết cho đúng nhất.
- **Phiếu nhập đang chờ duyệt (chưa status=1): VẪN tính "đang về"** — user chốt 2026-10-12.
  Chỉ trừ khi phiếu nhập đã duyệt (type 11/15, status 1).
- **Rà phiếu cũ (PI treo) TÁCH RIÊNG**, làm sau khi sửa hiển thị, **hỏi điều kiện đóng/hủy trước khi
  đụng data** — user chốt 2026-10-12.

## Cảnh báo

- DB `hrm_erp_gop` = PROD → mọi ghi là ghi thật. Giai đoạn này **chỉ SELECT**.
- Không commit/push khi chưa có yêu cầu. Không tự sửa hàm dùng chung ngoài phạm vi trên khi chưa hỏi.

---

## Phụ lục — Lịch sử điều tra (07/10, giữ làm bối cảnh)

- Report "Hàng đang về" = tổng `arriving_qty>0` gộp nhiều chặng (Sổ B cột phẳng); Sổ A
  `order_stock_progress` là ledger per-chặng cho popup chi tiết.
- Bất biến domestic cha `arriving = GREATEST(0, ΣA − arrived)`: khớp 1723/1748; reconcile 25 dòng
  (`UpdateDB::reconcileArrivingFromProgress_20261007`) ĐÃ commit prod (net report −93). **Nay vô hiệu.**
- Bế tắc: bảng DETAIL (ΣA=0 ≠ không có hàng — id912 flat=360 ΣA=0) + INLAND (ΣA là số ròng, bất biến
  khác: `arriving == ΣA`; ΣA có thể âm). ⇒ ledger không đủ làm nguồn sự thật → chuyển sang document-truth.
- Hướng "B'" (07/10, sửa `updateWarehouse` thành idempotent-derive từ ΣA) **BỎ** — vì vẫn dựa ΣA,
  không giải được ca ΣA=0 (48475).
- Phantom cũ đã trace: ca 54 SP 5384 (pidc#15070 available=54, PO phục vụ bị PO khác thay thế);
  arriving âm toàn hệ thống chỉ nhiễu (6 dòng/−14).
