# Plan — Fix báo cáo Tổng hợp bán hàng: cột "SL trả lại"

## Tasks
- [x] Điều tra root cause (returned_qty hard-code 0 trong `getData`)
- [x] Tìm reference netting trả lại (`SaleProductReportService` type 4|9)
- [x] Xác nhận nghiệp vụ với user (4 điểm: nguồn, real_qty, lọc ngày, netting tiền)
- [x] Thêm nhánh union `$return` trong `SummarySaleReportService::getData()` (path non-detail)
  - [x] Build subquery `product_import_details` JOIN `product_imports` (type 4|9, status 1) JOIN `product_export_details` (oped) định giá
  - [x] 12 cột đúng thứ tự, real_qty/amount âm, returned_qty dương, group `oped.product_id`
  - [x] Áp `filter()` lọc ngày + product
  - [x] Phân quyền theo `em_info` (mirror nhánh borrow) + guard buy_type=2 (KM không trừ) + warehouse filter
  - [x] `->union($return)` trước khi bọc `DB::table(...'result')`
- [x] `php -l` sạch
- [ ] Test UI `summary_sale?type=all`: 1 mã có trả lại → cột SL trả lại hiện, SL thực tế & tiền trừ đúng
- [ ] Verify đơn vị `pid.qty` + coverage type 9

## Phase 2 — Fix đơn giá khi real_qty=0 + thành tiền net âm

### Triệu chứng (user)
- Khi SL bán thực tế (real_qty) = 0 → đơn giá bán/net bị ẩn (do chia NULLIF(real_qty,0)).
- Thành tiền net ÂM ở một số mã.

### Root cause
- Đơn giá ÷ real_qty → real_qty=0 ra NULL.
- Thành tiền net âm: nhánh trả lại tự định giá net bằng salemax riêng (correlated subquery firm_contract_tab_products) lệch với salemax lúc bán (ped→fctp/wrsci). Phiếu trả `firm_contract_id=null` hoặc HĐ dịch vụ (wrsci) → salemax_return=0 → net_return > net_export → khi trả hết, thành tiền net = net_bán − net_trả < 0.

### Fix
- [x] Nhánh `$return`: bỏ đóng góp tiền (allocated/net/export = 0), bỏ subquery salemax; chỉ trừ vào real_qty + cộng returned_qty.
- [x] Aggregate: đơn giá = SUM(tiền)/NULLIF(SUM(exported_qty),0) (gross, ổn định); thành tiền = đơn giá × real_qty; diff/profit_loss tính theo cùng nguyên tắc.
- [x] Fix công thức net: COALESCE(fctp/wrsci salemax, **0**) ở cả 6 vị trí (export/borrow × non-detail/detail) → net = price khi không có chiết khấu (trước đó NULL → đơn giá net=0/blank ~1110 mã).
- [x] php -l sạch.
- [x] Verify dữ liệu thật (window 05/2026, 1502 mã): donGiaNet=0(alloc>0) còn **0**; net_amt<-0.5 còn **2** mã (đều real_qty<0 = trả>bán trong kỳ, hợp lệ); real_qty=0 hiện cả đơn giá bán & net (vd 14338, 22501); mã không trả lại thành tiền = gross như cũ.

## Phase 3 — Chỉ tính trả lại khi phiếu XUẤT GỐC cũng trong kỳ

### Yêu cầu (user)
Phiếu nhập trả lại chỉ tính khi: (a) phiếu nhập trả lại trong kỳ (đã có), VÀ (b) phiếu xuất bán gốc tương ứng cũng trong kỳ.

### Link tìm được
- `product_imports.product_import_request_id` → `product_import_requests (pir)`.
- type 4 (bán trả lại): `pir.product_export_request_id` → `product_exports` (cùng request).
- type 9 (bán-mượn trả lại): `pir.borrow_sell_request_id` → `borrow_sells` (cùng request).
- `product_export_detail_id` trên pid đã bị drop → không dùng được.

### Fix
- [x] Join `product_import_requests as pir` vào nhánh `$return`.
- [x] Thêm `whereExists`: tồn tại product_exports (status=1, type bán/KM/BĐSC) cùng `product_export_request_id` với `created_at` trong [date_from, date_to]; HOẶC borrow_sells (status 1,12,13) cùng `borrow_sell_request_id` trong kỳ.
- [x] Date range parse như filter() (d/m/Y → Y-m-d, 00:00:00 / 23:59:59). Không có date → không ràng buộc ngày (chỉ cần có phiếu xuất gốc hợp lệ).
- [x] php -l sạch; verify: real_qty<0 = **0**, net_amt<0 = **0**, mã có trả lại = 70 (chỉ return có xuất gốc cùng kỳ).

### Checkpoint — 2026-06-11 (v2)
Vừa hoàn thành:
- Sửa lỗi `pid.product_export_detail_id` (cột đã bị drop) → định giá trực tiếp từ pid
- Calibrate đơn vị: `ped.export_qty = qty*coef` (base) → returned_qty = `pid.qty*coef`; tiền = `price*pid.qty` (không chia coef); giá vốn = `pid.import_price*pid.qty`
- Verify scale export vs return khớp (SL base-unit, giá vốn ~cùng đơn giá), php -l sạch, SQL chạy thật OK
Đang làm dở:
Bước tiếp theo: user test UI `summary_sale?type=all`
Blocked:
Ghi chú edge: (1) mã có `allocated_price` null bên xuất → "Thành tiền bán" có thể lệch (data nguồn); (2) type 9 bán mượn trả lại cần verify cột giá pid populate đúng
