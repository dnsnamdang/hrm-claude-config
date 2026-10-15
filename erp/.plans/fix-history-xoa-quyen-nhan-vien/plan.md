# Fix: Lịch sử chỉnh sửa nhân viên không lưu việc XÓA quyền

## Bug
Trang `admin/employees/{id}/history` không ghi lịch sử khi XÓA quyền (phòng ban/bộ phận/chức vụ).
VD: Hà Thị Khánh Ly (emp 332, info_id 388) — xóa phòng "KD CN Hải Phòng" → version 42 có 0 dòng `employee_info_histories`.

## Root cause (app/Employee.php)
Phần ghi history trong 3 hàm chỉ duyệt danh sách MỚI → quyền bị xóa (không còn trong list mới) không được log:
- `syncDepartmentsByCompany` (~1261): `foreach ($departments...)` + so mảng-vs-scalar (sai)
- `syncPatsByCompany` (~1303): y hệt
- `syncRolesByCompany` (~1225): log nằm trong `if ($new_roles)` → chỉ ghi khi thêm

## Fix
Ghi history cả THÊM lẫn XÓA (diff old vs new), đặt ngoài block `if ($new_...)`.
Dòng xóa: `createEmployeeHistories(version, col, <tên cũ>, '', 'delete')` → hiển thị "tên cũ → (trống)".

## Tasks
- [x] Sửa `syncDepartmentsByCompany` — log xóa + thêm phòng ban
- [x] Sửa `syncPatsByCompany` — log xóa + thêm bộ phận
- [x] Sửa `syncRolesByCompany` — log xóa + thêm chức vụ
- [x] Test dev_128: simulate xóa quyền (transaction + rollback) → history có dòng 'delete'

### Checkpoint — 2026-07-14
Vừa hoàn thành: Fix xong 3 hàm trong app/Employee.php (log cả thêm+xóa quyền, đặt ngoài if($new_...)). Test dev_128 (transaction+rollback): xóa role/phòng ban/bộ phận đều tạo history action=delete "tên cũ → (trống)"; thêm phòng ban action=create. Lint sạch.
Đang làm dở: (không)
Bước tiếp theo: chờ user quyết commit/branch. Bug phụ phát hiện: createHistoryRecord(1,...) hardcode created_by=1 → FK fail trên dev_128 (employee id=1 không có) khi THÊM role — ngoài scope, đã báo user.
Blocked: (không)
