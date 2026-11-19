# Phiếu chờ giao việc (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-31-phieu-cho-giao-viec-design.md`

## Mục tiêu
Port màn ERP `WrAssignTasks.wait` — hàng đợi điều phối: hợp đồng / phụ lục / phiếu bảo hành / yêu cầu lắp đặt /
yêu cầu giao việc khác **còn số lượng chưa giao việc**, để phòng tiếp nhận lập phiếu giao việc.

## Quyết định (user chốt 31/10/2026)
- Đủ **5 tab** như ERP (kể cả 2 tab nguồn chưa port: Lắp đặt bàn giao, Giao việc khác — đọc thẳng bảng ERP).
- Phạm vi dữ liệu **y hệt ERP** (tab BH và Giao việc khác không bó phạm vi).
- Hành động y ERP; màn đích chưa port → link ERP tab mới (Tạo phiếu giao việc, Quyết toán, In/Xuất lắp đặt...).
  Thao tác đã có API HRM (Từ chối tiếp nhận / Đóng / Hủy duyệt HĐ) chạy thẳng ở HRM.
- Menu: phân hệ **CSKH sau bán → nhóm "Giao việc"** (đúng vị trí ERP). Ban đầu chốt Công việc → Tiếp nhận công việc, user đổi lại 31/10.
- 2 quyền HRM mới type 24 (CSKH sau bán): "Xem danh sách phiếu chờ giao việc theo tổng công ty", "Tạo phiếu giao việc".

## Phạm vi code
- BE: `Modules/Assign/Services/WaitingAssignTaskService.php`, controller `WaitingAssignTaskController`, route
  `/assign/waiting-assign-tasks`, `ExportColumnRegistry`, seeder quyền.
- FE: `pages/customer-care/waiting-assign-tasks/` (khuôn `pages/lookup/product-arrived-notifies`), menu `components/subsystem-menu/customer-care.js`. API vẫn nằm ở `Modules/Assign` (`/assign/waiting-assign-tasks`).
