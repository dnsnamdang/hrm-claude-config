# Plan — Biểu đồ gói thầu theo trạng thái trên từng nhân viên: đếm theo NV thực hiện

> @khoipv — Bắt đầu 08/10/2026
> Màn: `/bid_package/dashboard` — biểu đồ cột "Biểu đồ số lượng gói thầu theo trạng thái trên từng nhân viên"

## Vấn đề
Biểu đồ đếm gói thầu theo `bid_packages.created_by` (người tạo), còn màn danh sách lọc "Nhân viên thực hiện" theo `bid_packages.employee_id` → số liệu của NV (vd Nguyễn Thị Phương Linh) lệch, gói được giao nhưng người khác tạo không được tính.

## Phase 1 — BE
- [x] `CategoryDashboardService::getBidPackageColumnChart`: lấy danh sách NV + đếm theo `bid_packages.employee_id` thay cho `created_by`
- [x] Verify DB local: tổng chart 315 = đếm trực tiếp theo `employee_id`, từng NV khớp

### Checkpoint — 08/10/2026
Vừa hoàn thành: Phase 1
Đang làm dở:
Bước tiếp theo: deploy BE lên demo, user kiểm tra NV Nguyễn Thị Phương Linh so với màn danh sách
Blocked:
