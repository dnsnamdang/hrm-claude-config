# Chặn thêm nhân sự có lịch sử lương hết hiệu lực vào bảng lương

Phụ trách: @namdangit

## Mục tiêu
Khi thêm nhân sự vào bảng lương (màn `/payroll/salary/{id}`), nếu bản ghi lương áp dụng gần nhất của nhân sự đã **hết hiệu lực** thì không cho thêm.

## Định nghĩa "hết hiệu lực"
Xét bản ghi `employee_salary_histories` **áp dụng gần nhất** = bản ghi có `start_date <= salary.apply_date` với `start_date` lớn nhất (đúng bản ghi mà `CreateEmployeePayroll` dùng để tính lương).
- CHẶN nếu bản ghi đó có `end_date` khác rỗng **và** `end_date < apply_date`.
- CHO THÊM nếu: `end_date` rỗng, hoặc `end_date >= apply_date`, hoặc nhân sự chưa có bản ghi lương nào.

## Phạm vi thay đổi (chỉ Backend)
1. **Ẩn khỏi modal**: `Modules/Timesheet/Services/EmployeeInfoService.php` — nhánh lọc theo `salary_id` (dòng ~119-138) loại thêm `$blockedIds`.
2. **Chốt chặn khi lưu**: helper mới trong `SalaryService`, gọi trong `SalaryController::saveEmployee` trước khi đổi status/dispatch → throw `ValidationException` liệt kê nhân sự vi phạm (chặn toàn bộ, không lưu ai).

## Quyết định
- Lúc lưu phát hiện nhân sự hết hiệu lực → báo lỗi chặn toàn bộ (không lưu phần còn lại).
- FE không sửa: danh sách modal đã được BE lọc sẵn.

Spec chi tiết: `docs/superpowers/specs/2026-07-01-payroll-chan-luong-het-hieu-luc-design.md`
