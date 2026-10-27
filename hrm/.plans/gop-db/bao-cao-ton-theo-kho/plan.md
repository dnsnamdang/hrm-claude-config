# Plan — Báo cáo tồn theo kho

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseReport.stockWareshouseProduct` (Kho › Báo cáo kho › "Báo cáo tồn theo kho") → HRM `/warehouse/stock-warehouse-product`.
> Khuôn: màn anh em "Báo cáo tồn kho tổng hợp theo mặt hàng" (`/warehouse/stock-general-product`) — khác ở: nhóm cột "Chi tiết" theo KHO
> (không theo công ty thuê), thêm ô lọc Model (LIKE) + cột Hãng sản xuất.

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP: route / controller / `Product::stockWareshouseProductSearchData` / blade / JS class `WarehouseReportProduct` / Excel `StockWareshouseProductExcel`
- [x] `WarehouseStockReportService::aggregateByWarehouse()` (hàm MỚI, không sửa hàm cũ) — cộng `stock_logs` chia cột theo kho
- [x] `StockWarehouseProductReportService` (options / context / report)
- [x] `StockWarehouseProductPrintService` + `StockWarehouseProductExport` + 2 blade (export + print)
- [x] Controller + route `/v1/finance/stock-warehouse-product` (`/`, `/options`, `/print-list-data`, `/export`)
- [x] Đối chiếu số với hàm ERP gốc trên cùng DB `gop_db` — 6 ca (cty 1 cả 7 kho hôm nay 6.256 hàng · LN 31/03 · LN thương hiệu · 7 kho lọc Model · LN 1 công ty thuê · LN lọc Hợp đồng): tập hàng + SL tồn + SL từng kho + Hãng SX khớp 100%;
      thứ tự chỉ lệch giữa các hàng MySQL coi là TRÙNG tên (collation bỏ dấu: "ác quy" = "ắc quy") — ERP chỉ `ORDER BY name`, HRM thêm `id`
- [x] Smoke HTTP kernel: options / index (trang 2, lọc Model) / 422 thiếu ngày+kho / In 2 kiểu + chọn cột (logo, khối ký) / Excel 2 kiểu (đọc lại xlsx: tiêu đề, Kho, 2 tầng, logo) / 403 tài khoản không quyền (emp 24, 4 endpoint)
      Đo: màn 1,7s (6.256 hàng × 7 kho); Excel Đầy đủ toàn bộ 6.256 hàng ~70s (ERP gửi mail khi ≥ 500 — HRM tải thẳng như màn Tổng hợp); In > 2.000 dòng báo vượt trần

### FE
- [x] `pages/warehouse/stock-warehouse-product/index.vue` + `components/StockWarehouseSummary.vue`, `StockWarehouseTable.vue`
- [x] Menu Kho › Báo cáo kho: gắn link mục "Báo cáo tồn theo kho"
- [x] Parse template/script + grep tự kiểm skill erp-to-hrm-screen
- [x] Playwright MCP 24/10 (user yêu cầu, tài khoản DNS Admin, local 3000/8000): vào màn tự chọn công ty + 7 kho + 5 công ty thuê, tổng hợp 6.256 / 7 / 4 kho có tồn;
      bảng 2 tầng 7 kho, dòng 1 khớp API · lọc Model Enter 25 hàng · trang 2 STT 21–25 · bỏ tick Xem toàn bộ kho → xoá kho, Tìm kiếm báo đỏ
      "Vui lòng chọn kho" không gọi API · tick lại đủ kho + công ty thuê · đổi ĐVT Túi (x20) 1.290 → 64,5, bản in theo ĐVT đã chọn (`units`) · In xem trước
      (letterhead, khối ký) · Xuất Excel Đầy đủ tải file (logo, 2 tầng, `#,##0`) · Xóa lọc về 6.256 · mỗi thao tác đúng 1 request · console 0 lỗi
      Ghi nhận nhỏ: Model toàn chữ số (vd "44700") Excel đọc thành SỐ (maatwebsite FromView) — như màn Tổng hợp / ERP

### Checkpoint — 24/10/2026
Vừa hoàn thành: Phase 1 BE + FE (khuôn màn Tổng hợp theo mặt hàng); thêm hàm MỚI `aggregateByWarehouse()` vào service dùng chung (không sửa hàm cũ); đối chiếu ERP 6/6 ca khớp
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/stock-warehouse-product` kiểm giao diện; cân nhắc Excel toàn bộ (~70s) có cần chạy nền / gửi mail như ERP không
Blocked:

ĐÃ PUSH 24/10/2026 lên `develop`: api `f637713a6` (merge `11e921aeb`), client `612fede85` (merge `d12262082`).
