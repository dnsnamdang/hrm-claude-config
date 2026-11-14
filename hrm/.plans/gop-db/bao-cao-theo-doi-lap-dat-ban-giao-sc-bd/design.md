# Báo cáo theo dõi lắp đặt - bàn giao - SC - BD (ERP → HRM) — DESIGN (tóm tắt)

> Người phụ trách: @khoipv · tạo 2026-11-14 · nhánh `develop` (từ `gop_db`) cả hrm-api + hrm-client
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-14-bao-cao-theo-doi-lap-dat-ban-giao-sc-bd-design.md`

## Mục tiêu
Port màn ERP `customerCareReport.reportInstallDeliveryRepair` (CSKH › Báo cáo) sang HRM `/customer-care/report/install-delivery-repair`:
theo dõi mỗi hợp đồng / YC giao việc khác đi qua các bước Phiếu yêu cầu → Giao việc → Công tác → Nhập KQ → Duyệt KQ.

## Quyết định lớn (user chốt 14/11)
- **Không phân quyền** (y ERP) — ai đăng nhập cũng xem mọi công ty.
- Ô **Người yêu cầu** chạy thật; **bỏ ô Trạng thái** (ERP chết).
- Có **In + Xuất Excel**.
- Giao diện theo **khuôn báo cáo HRM rsum** (skill report-styles): khối tổng hợp (Chứng từ nguồn · Tiến độ xử lý) + bảng cây
  HĐ ▸ phiếu giao việc + popup drill.
- Lệch ERP có chủ ý: lọc ngày / người yêu cầu / nhân sự ở từng dòng con (ERP lọc trên 1 dòng đại diện tuỳ ý).

## Phạm vi code
- BE `Modules/CustomerCare`: `InstallDeliveryRepairReportController`, `Services/Report/InstallDeliveryRepairReportService` + `PrintService`,
  2 Export + blade in / excel.
- FE `pages/customer-care/report/install-delivery-repair/` (index + components theo template report-styles) + link menu.

## Phase 2 — màn CHI TIẾT (14/11/2026)
Port `customerCareReport.reportInstallDeliveryRepairDetail` → `/customer-care/report/install-delivery-repair-detail`: 3 tab Lắp đặt bàn giao
(mọi HĐ bán, phân trang) / Sửa chữa - Bảo dưỡng / Bảo hành (bắt buộc chọn 1 HĐ DV), bảng cây số lượng theo hàng / thiết bị / dịch vụ /
vật tư + popup phiếu. Chốt: không quyền, chọn HĐ từ ô tìm, có In + Excel, lỗi số liệu ERP giữ y ERP. Chi tiết: spec mục "Phase 2".
