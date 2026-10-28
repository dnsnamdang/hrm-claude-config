# Design — Báo cáo tồn kho tổng hợp theo mặt hàng

> Phụ trách: @khoipv · Tạo 23/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-23-bao-cao-ton-kho-tong-hop-mat-hang-design.md`

## Mục tiêu

Port màn ERP *Kho › Báo cáo kho › Báo cáo tồn kho tổng hợp theo mặt hàng* (`warehouseReport.stockGeneralProduct`) sang HRM
`/warehouse/stock-general-product`. Màn chỉ đọc: tồn của từng mặt hàng TÍNH ĐẾN NGÀY trên 1 hoặc nhiều kho của 1 công ty,
chia cột theo công ty thuê kho.

## Quyết định chính

| Vấn đề | Chốt |
|---|---|
| Hàm tính tồn | Tách service dùng chung `WarehouseStockReportService` (user chốt 23/10/2026) — màn Chi tiết và màn Tổng hợp cùng gọi |
| Quyền | Dùng lại 3 quyền TÊN Y ERP như màn Chi tiết: "Xem báo cáo tồn kho theo tổng công ty / công ty / kho" (type 21) |
| Giao diện | Khuôn báo cáo (report-styles): khối tổng hợp + bảng `rsum-tb` PHẲNG, tiêu đề 2 tầng nhóm "Chi tiết" theo công ty thuê như ERP |
| Cột Chi tiết | Như ERP: chỉ hiện trên màn với quyền tổng công ty (ERP `status`); Excel/In kiểu Đầy đủ luôn có |
| Số liệu | Giữ y ERP |
| In / Excel | Excel Đầy đủ / Rút gọn tải thẳng (bỏ gửi mail ≥ 500 dòng); THÊM In xem trước (ERP comment nút In). ĐVT theo lựa chọn từng hàng như ERP |

## Code

- BE: `Modules/Finance/Services/WarehouseStockReportService.php` (chung), `StockGeneralProductReportService.php`,
  `StockGeneralProductPrintService.php`, `Http/Controllers/V1/StockGeneralProductController.php`, `Exports/StockGeneralProductExport.php`,
  views `exports/stock_general_product` + `prints/stock-general-product`, route `/v1/finance/stock-general-product`
- FE: `pages/warehouse/stock-general-product/index.vue` + `components/` (Summary, Table); dùng lại `ExportModeModal` / `format.js` của Thẻ kho
