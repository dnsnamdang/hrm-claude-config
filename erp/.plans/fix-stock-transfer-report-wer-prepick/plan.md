# Fix: báo cáo stock-transfer lỗi "Unknown column 'wer_prepick_total'"

**Mục tiêu:** Báo cáo `admin/stock-transfer/report` không lỗi SQL khi lọc (đặc biệt check_in_stock) ở nhánh không có warehouses.

## Root cause
`StockTransferReportService` có 2 nhánh build subquery `werd`:
- **Nhánh `if` inline** (dòng 1171-1173 / 3164-3166): select đủ `wer_total`, `wer_prepick_total`, `wer_hold_total`.
- **Nhánh `else`** dùng `buildWarehouseExportRequestSubQuery` (dòng 6350): **chỉ select `wer_total`** — thiếu `wer_prepick_total` + `wer_hold_total`.

Report tham chiếu cả 3 trong biểu thức tồn kho `(wer_total - wer_km_total - wer_prepick_total - wer_hold_total)` (dòng 1947/1954 + 3937/3944). Khi nhánh else chạy → cột `wer_prepick_total` không tồn tại → `SQLSTATE[42S22] 1054`.

## Fix
`buildWarehouseExportRequestSubQuery` (dùng ở cả 2 path: dòng 1185 + 3178): thêm 2 cột vào cả select trong (per-company, từ `werd.export_prepick_qty` / `werd.export_hold_qty`) lẫn select ngoài (`SUM(...)`), mirror `wer_total`.

## Tasks
- [x] Thêm `wer_prepick_total` + `wer_hold_total` vào 2 select của `buildWarehouseExportRequestSubQuery`.
- [x] Verify: `php -l` sạch; cột `export_prepick_qty`/`export_hold_qty` tồn tại trên `warehouse_export_request_details`; builder dùng ở cả 2 report path.

### Checkpoint — 2026-06-16
Vừa hoàn thành: bổ sung cột thiếu trong builder werd → hết lỗi 1054.
Bước tiếp theo: user reload báo cáo với payload cũ (year_stock=2025, check_in_stock) để xác nhận.
Blocked:
