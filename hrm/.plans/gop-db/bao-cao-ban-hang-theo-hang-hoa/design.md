# Design — Báo cáo bán hàng theo hàng hóa (ERP → HRM)

> Phụ trách: @khoipv · 23/11/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-23-bao-cao-ban-hang-theo-hang-hoa-design.md`

## Mục tiêu
Port ERP `report.saleProduct` sang HRM `/sale/sale-by-goods-report` (Bán hàng › Báo cáo › Tổng hợp & so sánh). Báo cáo chỉ đọc,
bảng cây: Nhóm (theo "Báo cáo theo") › Công ty › Phòng ban | Hãng SX | Tỉnh/TP; 3 cụm Bán / Nhập trả lại / Thực bán × (SL khách, SL, Giá trị hàng).

## Quyết định (user chốt 23/11/2026)
| Vấn đề | Chốt |
|---|---|
| Báo cáo theo | Tính chất HH · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Model (cây phân loại mới `product_natures` › … › `product_types`) |
| Ô lọc | Bỏ Nhóm HH, Loại HH; thêm Nhóm chức năng, Nhóm SP, Loại SP (chọn nhiều); Tính chất theo danh mục mới |
| Bắt buộc | Giữ ERP: chọn Báo cáo theo X thì ô lọc X phải có giá trị |
| Nguồn HĐ | Cộng thêm HĐ HRM (phiếu xuất 21, bán mượn / nhập trả gắn HĐ HRM) |
| Quyền | Mã `sale.bao_cao_ban_hang_theo_hang_hoa.view` 4 mức, thêm platform hrm, không có mã thì chặn |
| Popup | Thêm Số HĐ + Khách hàng (Mã - Tên), lọc, In, Xuất Excel |

## Code
- BE `Modules/Finance`: `Services/SaleByGoodsReportService.php`, `Services/SaleByGoodsReportPrintService.php`, `Services/ProductClassTree.php` (dùng chung lọc/option cây phân loại),
  `Http/Controllers/V1/SaleByGoodsReportController.php`, `Exports/SaleByGoodsReportExport.php`, views `prints/sale-by-goods-report` + `exports/sale_by_goods_report`, route `/v1/finance/sale-by-goods-report`
- FE `pages/sale/sale-by-goods-report/` (index + components Summary / Table / CustomerModal), menu `sale-hub.js`
