# Phiếu giao việc CSKH (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-31-phieu-giao-viec-design.md`

## Mục tiêu
Port màn ERP `WrAssignTasks` (`/admin/customer-care/wr_assign_tasks?type=all`) — phiếu giao việc lập từ Hợp đồng /
Phiếu bảo hành / PL bổ sung / YC lắp đặt bàn giao / YC giao việc khác (nối tiếp màn Phiếu chờ giao việc).

## Quyết định (user chốt 31/10/2026)
- Trọn bộ như ERP: Danh sách · Chi tiết · Tạo (3 nguồn) · Xóa(Hủy) · In/Xuất. Màn chưa port (Nhập KQ, Duyệt KQ, HĐ bán, YC lắp đặt,
  YC giao việc khác) → link ERP tab mới.
- **Không có Sửa** (y ERP: ERP không có lối vào Sửa).
- Menu CSKH sau bán › Giao việc: "Phiếu giao việc" (`?type=all`) + "Phiếu giao việc được giao" (`?type=waiting_import_result`).
- 3 quyền mới type 24, tên nguyên văn ERP: `Xem phiếu giao việc theo tổng công ty / công ty / phòng ban`.
- Mã giữ format ERP `{cty}.PGV.{YYYY}{id 6 số}`.
- Sửa các lỗi ERP ở luồng lưu/xóa ở **cả HRM lẫn repo ERP** (spec mục 8).
- Nút "Tạo phiếu giao việc" ở màn Phiếu chờ giao việc chuyển sang mở form HRM.

## Phạm vi code
- BE `Modules/CustomerCare`: entity `WrAssignTask` + bảng con + tiến độ, `WrAssignTaskService` (list/show/delete/print/export),
  `WrAssignTaskSourceService` (dữ liệu nguồn + SL còn giao), `WrAssignTaskStoreService`, controller, FormRequest, resource, route
  `/v1/customer-care/wr-assign-tasks`, seeder quyền, `ExportColumnRegistry`, lịch sử `catalog_histories`.
- FE `pages/customer-care/wr-assign-tasks/` (index, create, `_id/index`) + `components/WrAssignTaskForm.vue` (+ bảng con), menu.
- ERP: vá các lỗi spec mục 8 trong `WrAssignTasksController` / `WrAssignTask` / class JS.
