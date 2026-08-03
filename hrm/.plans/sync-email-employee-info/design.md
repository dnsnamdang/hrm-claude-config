# Đồng bộ email employees ↔ employee_infos

@namdangit — 2026-06-19

## Mục tiêu
Email ở 2 bảng `employees` (tài khoản) và `employee_infos` (hồ sơ) **luôn giống nhau**.

## Hiện trạng
- Chiều **hồ sơ → tài khoản** ĐÃ có sẵn (2 lớp):
  - Boot hook `EmployeeInfo::updated` — `Entities/EmployeeInfo.php:137-140` (`$employee->email = $model->email`)
  - Service — `EmployeeInfoService.php:699-701` (`Employee::where('employee_info_id',...)->update(['email'=>...])`)
- Chiều **tài khoản → hồ sơ** CHƯA có: `EmployeeService::updateEmployee` chỉ ghi `employees.email`, đoạn sync `employee_infos` đang bị comment (`EmployeeService.php:274-278`).
- Dữ liệu cũ có thể đang lệch (tạo trước khi có boot hook).

## Quyết định
- **Nguồn chuẩn (source of truth) = `employee_infos`** (email công ty quản lý ở hồ sơ nhân sự).
- Phạm vi: **sync 2 chiều** + **fix data cũ một lần**.

## Giải pháp
1. Thêm sync chiều ngược trong `updateEmployee`: sau khi lưu, nếu `employee_infos.email` khác `employees.email` thì cập nhật lại bằng `saveQuietly()` (tránh bắn lại event → vòng lặp / dispatch ERP thừa).
2. Artisan command `human:sync-employee-email` (có `--dry-run`): set `employees.email = employee_infos.email` ở các bản ghi đang lệch. Bỏ qua + cảnh báo khi `employee_infos.email` rỗng (không xoá email tài khoản đang dùng để đăng nhập).

## Field
- `employees.email`, `employee_infos.email` — cùng tên cột `email`, quan hệ qua `employees.employee_info_id`.

## Không đụng tới
- Chiều hồ sơ → tài khoản (đã chạy đúng).
- Đồng bộ HRM ↔ ERP (mysql2) — command `check:employee-email-diff` riêng, không liên quan.
