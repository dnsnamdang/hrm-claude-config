# Design — Báo cáo bán hàng theo từng mặt hàng (ERP → HRM)

> Phụ trách: @khoipv · 13/11/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-13-bao-cao-ban-hang-theo-mat-hang-design.md`

## Mục tiêu

Port ERP `report.summary_sale` (không tham số — Kinh doanh › Báo cáo › Tổng hợp & so sánh) sang HRM `/sale/sale-by-product-report`.
Báo cáo chỉ đọc: mỗi mặt hàng 1 dòng — SL bán / trả lại / thực tế, thành tiền bán / net, chênh lệch, tồn đầu / cuối kỳ.

## Quyết định (user chốt 13/11/2026)

| Vấn đề | Chốt |
|---|---|
| Nguồn hợp đồng | **Cộng thêm HĐ HRM** (`hrm_contracts`, YCXH/phiếu xuất loại 21, bán mượn + nhập trả gắn HĐ HRM) vào các nguồn cũ ERP (HĐ hãng 14/15, BH-SC 17) |
| Cột | Bỏ "Thời gian bảo hành (tháng)" + "ĐM đàm phán giá" |
| Quyền | Giữ y ERP: mã `accounting.bao_cao_ban_hang_theo_mat_hang.view` 4 mức, thêm platform `hrm`; ai cũng vào, không quyền = phiếu mình tạo |
| Popup chi tiết | Thêm cột NVKD (người tạo HĐ), lọc (tìm nhanh Số HĐ/KH + Khách hàng + NVKD, ngày kế thừa màn ngoài), In, Xuất Excel |
| Giao diện | Khuôn report-styles bảng phẳng (bám `warehouse/self-inventory-report`) |

## Code

- BE `Modules/Finance`: `Services/SaleByProductReportService.php`, `Services/SaleByProductReportPrintService.php`,
  `Http/Controllers/V1/SaleByProductReportController.php`, `Exports/SaleByProductReportExport.php`, views
  `exports/sale_by_product_report` + `prints/sale-by-product-report`, route `/v1/finance/sale-by-product-report`
- FE `pages/sale/sale-by-product-report/` (index + Summary + Table + DetailModal), menu `sale-hub.js`
