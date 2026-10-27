# Design — Báo cáo tồn kho theo vị trí

> Phụ trách: @khoipv · Tạo 23/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-23-bao-cao-ton-kho-theo-vi-tri-design.md`

## Mục tiêu

Port màn ERP *Kho › Báo cáo kho › Báo cáo tồn kho theo vị trí* (`warehouseReport.stockLocationProduct`) sang HRM
`/warehouse/stock-location-product`. Màn chỉ đọc: hàng đang nằm ở từng VỊ TRÍ của 1 kho TÍNH ĐẾN NGÀY, chi tiết theo mặt hàng ▸
công ty thuê kho ▸ lô (hợp đồng). Lọc được theo Nhà / Dãy / Khoang / Vị trí.

## Quyết định chính

| Vấn đề | Chốt |
|---|---|
| Hàm dùng chung | User chốt 23/10/2026: tách vào `WarehouseStockReportService` — `applyProductFilters()` (khỏi `aggregate()`), `positionIdsOf()` (khỏi Thẻ kho), `contractsOfImports()` (khỏi màn Chi tiết). Chụp số Thẻ kho + 2 màn tồn trước/sau tách: 15/15 ca khớp |
| Quyền | Dùng lại 3 quyền TÊN Y ERP như 2 màn tồn theo mặt hàng: "Xem báo cáo tồn kho theo tổng công ty / công ty / kho" — không thêm quyền mới |
| Giao diện | Khuôn báo cáo (report-styles) bám màn Chi tiết: khối tổng hợp + bảng cây 4 cấp **Vị trí ▸ Hàng hóa ▸ Công ty thuê ▸ Lô** (thứ tự gộp ô của ERP), cắt trang theo vị trí; ô Nhà/Dãy/Khoang/Vị trí dùng lại `ScopePicker` |
| Số liệu | Giữ y ERP — đối chiếu thẳng hàm ERP gốc trên cùng DB: khớp 100% (xem plan) |
| In / Excel | Excel Đầy đủ / Ngắn gọn tải thẳng (bỏ lệnh nền `stock:export-large` của ERP); THÊM In xem trước (user chốt — ERP comment nút In, hàm in ERP lỗi). Số theo ĐVT cơ sở như ERP; có dòng Tổng cộng |

## Code

- BE: `Modules/Finance/Services/StockLocationProductReportService.php`, `StockLocationProductPrintService.php`,
  `Http/Controllers/V1/StockLocationProductController.php`, `Exports/StockLocationProductExport.php`,
  views `exports/stock_location_product` + `prints/stock-location-product`, route `/v1/finance/stock-location-product`
  (`/`, `/options`, `/structure`, `/print-list-data`, `/export`)
- Sửa hàm chung: `WarehouseStockReportService` (+3 hàm), `StockCardReportService::positionIds()` và
  `StockDetailByProductReportService::contractsOfImports()` chuyển thành lời gọi hàm chung
- FE: `pages/warehouse/stock-location-product/index.vue` + `components/` (StockLocationSummary, StockLocationTable); menu Kho › Báo cáo kho
