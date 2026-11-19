# Design (tóm tắt) — Xuất Excel Danh mục tài khoản nhân viên

> @khoipv — 29/10/2026 · Spec chi tiết: [docs/superpowers/specs/2026-10-29-xuat-excel-tai-khoan-nhan-vien-design.md](../../docs/superpowers/specs/2026-10-29-xuat-excel-tai-khoan-nhan-vien-design.md)

## Mục tiêu
Màn `/human/employee` (Danh mục tài khoản nhân viên) có nút **Xuất excel**, làm theo khuôn xuất Excel màn Hồ sơ nhân sự.

## Scope
- FE: nút Xuất excel → `export-modal` dùng chung (chọn trường + Chọn tất cả) → tải `danh_sach_tai_khoan_nhan_vien.xls`.
- BE: API `GET /api/v1/human/employee/export` trả file `.xls` (Maatwebsite FromView + blade).
- Không đổi hàm dùng chung (`export-modal`, `EmployeeService::getEmployees` giữ nguyên).

## Quyết định lớn
- **Dữ liệu = bộ lọc đang áp dụng**, không phân trang; dùng lại `EmployeeService::getEmployees` để kết quả khớp màn danh sách.
- **10 trường**: Mã NV · Tên NV · Email · SĐT công ty · Công ty · Phòng ban · Vị trí công việc · Ngày tạo · Ngày cập nhật · Trạng thái. Thứ tự cột cố định, không theo thứ tự chọn.
- **Công ty** = công ty kê khai trong tài khoản (`company_employees`), **Phòng ban** = nhóm quyền `is_department = 1` — khớp bộ lọc và cột bảng của màn.
- **Quyền**: như API danh sách — `Quản lý tài khoản nhân viên` (ai vào được màn là xuất được).
- **Token**: FE gọi `$axios` thô để nhận `arraybuffer` → phải gắn tay `Authorization: Bearer <access_token>` (như màn gói thầu), nếu không BE trả 403.

## Còn treo
- API xuất HSNS `getEmployeeByField` không check quyền (gọi không token vẫn tải được) — chưa sửa, chờ user quyết.
