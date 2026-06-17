# Plan — Fix báo cáo "Hàng có thể bán theo công ty" trừ trùng SL phiếu xuất đã prepick

## Bối cảnh
- Báo cáo `warehouseReport.stockCompanies` hiển thị **SL tồn có thể bán = 0** trong khi popup tìm hàng (`searchProductStockBuyer`) hiển thị **TPSG:2** cho cùng product 31913, công ty 4, kho [2,4,5,12].
- Root cause: trong `Product::stockCompaniesSearchData()`, khoản trừ phiếu xuất `wer_total` dùng `SUM(export_total_qty)` (toàn bộ), trong khi popup dùng `SUM(export_total_qty - export_prepick_qty - export_hold_qty)`.
- Phần đã prepick của phiếu xuất đã được trừ qua `total_prepick` rồi → báo cáo trừ trùng phần này một lần nữa qua `wer_total`.
- Minh chứng số liệu thật: tồn 20 − prepick 17 − wer(báo cáo 3) = 0; còn 20 − 17 − wer(popup 1) = 2. Chênh lệch 2 = `export_prepick_qty` của phiếu #25945.

## Tasks
- [x] Điều tra root cause bằng số liệu DB thật (product 31913)
- [x] Sửa subquery `werd` trong `Product::stockCompaniesSearchData()`:
  - [x] Dòng 5348: `wer_$acc` → trừ `export_prepick_qty` + `export_hold_qty`
  - [x] Dòng 5360: `wer_total` → trừ `export_prepick_qty` + `export_hold_qty`
  - [x] GIỮ NGUYÊN nhánh `wer_km` (dòng 5378, 5385) — vì stock KM (`stock_can_export`) KHÔNG trừ prepick/hold ở chỗ khác nên không trùng (đồng bộ với popup: promotion_qty dùng full export_total_qty)
- [x] Verify lại bằng query: stock_can_sale = 2.00 cho product 31913 ✅
- [x] php -l: No syntax errors

## Phạm vi ảnh hưởng
- Hàm `Product::stockCompaniesSearchData()` dùng chung cho cả màn báo cáo (`stockCompaniesSearchData`) và export Excel (`stockCompaniesExport`) → cả 2 đều được fix đồng thời.

### Checkpoint — 2026-06-05
Vừa hoàn thành: fix Product.php (wer_$acc + wer_total trừ thêm export_prepick_qty/export_hold_qty), verify stock_can_sale=2, php -l sạch
Đang làm dở:
Bước tiếp theo: test trên UI báo cáo + theo dõi các product khác; cân nhắc viết SRS/testcase nếu cần
Blocked:
