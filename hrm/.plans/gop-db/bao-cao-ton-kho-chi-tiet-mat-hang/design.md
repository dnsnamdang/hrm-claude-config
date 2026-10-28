# Design — Báo cáo tồn kho chi tiết theo mặt hàng

> Phụ trách: @khoipv · Tạo 22/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-22-bao-cao-ton-kho-chi-tiet-mat-hang-design.md`

## Mục tiêu

Port màn ERP *Kho › Báo cáo kho › Báo cáo tồn kho chi tiết theo mặt hàng* (`warehouseReport.stockCardDetail`) sang HRM
`/warehouse/stock-detail-by-product` (phân hệ Kho). Màn chỉ đọc: tồn của từng mặt hàng TÍNH ĐẾN NGÀY tại 1 kho,
chi tiết theo công ty thuê kho ▸ lô (hợp đồng) ▸ vị trí.

## Quyết định chính (user 22/10/2026)

| Vấn đề | Chốt |
|---|---|
| Quyền | 3 quyền TÊN Y ERP (như Thẻ kho), type 21: "Xem báo cáo tồn kho theo tổng công ty" (mọi công ty, mọi kho) · "… theo công ty" (công ty mình, kho của công ty mình) · "… theo kho" (công ty mình, chỉ kho mình là thủ kho) |
| Giao diện | Khuôn báo cáo (skill report-styles) như Thẻ kho: khối tổng hợp + bảng cây 4 cấp Hàng hóa ▸ Công ty ▸ Lô ▸ Vị trí |
| Số liệu | GIỮ Y ERP — kể cả SL theo lô/vị trí lấy số mới nhất (không cắt theo "Tính đến ngày") |
| In / Excel | Excel 2 kiểu Đầy đủ / Rút gọn (tải thẳng, bỏ gửi mail ≥150 dòng) + THÊM In xem trước (ERP đang ẩn nút In) |

## Code

- BE: `Modules/Finance/Services/StockDetailByProductReportService.php`, `StockDetailByProductPrintService.php`,
  `Http/Controllers/V1/StockDetailByProductController.php`, `Exports/StockDetailByProductExport.php`,
  views `exports/stock_detail_by_product` + `prints/stock-detail-by-product`, route `/v1/finance/stock-detail-by-product`
- FE: `pages/warehouse/stock-detail-by-product/index.vue` + `components/` (Summary, Table); dùng lại `ExportModeModal` / `format.js` của Thẻ kho
