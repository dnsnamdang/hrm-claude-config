# Báo cáo làm dịch vụ Bảo hành - Sửa chữa - Bảo dưỡng (ERP → HRM)

**Người phụ trách:** @khoipv — 2026-11-25
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-25-bao-cao-lam-dich-vu-bh-sc-bd-design.md`

## Mục tiêu
Port `report.warrantyRepairService` sang `/sale/warranty-repair-service-report` (Bán hàng › Báo cáo › Tổng hợp & so sánh):
SL + giá trị Bảo hành / Sửa chữa / Bảo dưỡng theo hàng hóa, gom nhóm theo "Báo cáo theo". Khuôn report-styles.

## Quyết định (user 25/11/2026)
| Vấn đề | Chốt |
|---|---|
| Ô lọc | Bỏ Nhóm hàng hóa, thêm Loại sản phẩm, xếp lại (spec mục 3) |
| Báo cáo theo | "Nhóm hàng hóa" → "Loại sản phẩm" |
| Lỗi tính ERP | Sửa cả HRM lẫn code ERP (spec mục 5) |
| Ngày lọc kỳ | Ngày cập nhật chứng từ như ERP |
| Cây | 2 cấp: Nhóm ▸ Hàng hóa |
| Popup bấm số | Số chứng từ (HĐ / phiếu BH) · Khách hàng · SL · Giá trị + In / Excel |

## Code
- BE `Modules/Sale`: `Services/WarrantyRepairServiceReportService.php`, `…PrintService.php`, `Http/Controllers/V1/WarrantyRepairServiceReportController.php`, route.
- FE `pages/sale/warranty-repair-service-report/` + menu `sale-hub.js`.
- ERP `app/Services/Reports/WarrantyRepairService.php` + `ReportController` (không commit).
