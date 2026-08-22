# Fix: Tiếp nhận yêu cầu giải pháp báo "PM không tồn tại"

## Phase 1 — BE
- [x] `RequestSolutionReceiveRequest.php:19` — bỏ `exists:employee_infos,id` (sai bảng: FE gửi `employees.id` từ `employeeOptions`, quan hệ `pm()` cũng `belongsTo(Employee::class)`); rule hiện tại: `required|integer`

### Checkpoint — 2026-08-18
Vừa hoàn thành: sửa rule validate `pm_id`
Đang làm dở: không
Bước tiếp theo: test lại nút "Xác nhận tiếp nhận" ở /assign/request-solution với PM từng lỗi
Blocked:
