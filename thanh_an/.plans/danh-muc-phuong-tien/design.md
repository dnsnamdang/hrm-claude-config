# Danh mục phương tiện (phân hệ Chấm công) — Design (tóm tắt)

> Người phụ trách: @khoipv · Bắt đầu: 11/11/2026
> Spec chi tiết: [docs/superpowers/specs/2026-11-11-danh-muc-phuong-tien-design.md](../../docs/superpowers/specs/2026-11-11-danh-muc-phuong-tien-design.md)

## Mục tiêu
Danh mục **xe cụ thể** (Hãng xe, Biển kiểm soát, Phòng phụ trách chọn nhiều) trong phân hệ Chấm công,
menu **Giao việc/Công tác → Danh mục phương tiện**. Chưa nối vào phiếu nào.

## Scope
- BE `Modules/Timesheet`: bảng `vehicles` + `vehicle_departments`, CRUD + Khóa/Mở khóa + Xóa mềm,
  quyền mới **"Quản lý phương tiện"** (id 526).
- FE `pages/timesheet/vehicles`: màn danh sách **kiểu cũ** của Chấm công + 1 popup Tạo/Sửa/Xem.

## Quyết định lớn
- Danh mục mới, độc lập; không đụng "Danh mục phương tiện đi lại" cũ của phân hệ Giao việc (đã ẩn).
- Không phân quyền theo cấp: có quyền "Quản lý phương tiện" là thấy toàn bộ + làm mọi thao tác.
- Xóa: chỉ khi xe chưa được dùng (`Vehicle::isUsed()` — hiện luôn `false`, bổ sung khi nối vào phiếu).
- Biển kiểm soát không trùng, so bỏ qua hoa/thường, khoảng trắng, `-`, `.` (call của builder).
- Khóa/Mở khóa chỉ qua nút ở danh sách; popup Sửa không có ô trạng thái (call của builder).

## Non-goals
- Không nối vào Phiếu đi công tác hay phiếu nào khác.
- Không lên giao diện V2, không xuất Excel.
