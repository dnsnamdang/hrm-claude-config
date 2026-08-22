# Plan — Tách mã máy chấm công / máy chấm cơm khi đồng bộ khuôn mặt

## Phase 1 — BE
- [x] `EmployeeInfoService`: tách khối đồng bộ mặt thành `syncFaceToDevices()` + `syncFaceToTimekeepingDevices()` (dùng `employee_infos.ssn`) + `syncFaceToRiceDevices()` (dùng `rice_employee_infos.rice_ssn`, thiếu thì trả 422 chặn lưu)
- [x] `EmployeeInfoController@store`: ca tạo mới gọi `syncFaceToDevices()` sau khi tạo tài khoản nhân viên (để hook `Employee::saved` kịp điền `rice_ssn`)

### Checkpoint — 2026-08-18
Vừa hoàn thành: tách 2 loại mã máy, đảo thứ tự sync ở ca tạo mới
Đang làm dở: (không)
Bước tiếp theo: test thực tế màn /human/employee_info/add
Blocked:

## Phase 2 — Kiểm thử (không đụng máy thật)
- [x] Test bằng `Http::fake()` chặn toàn bộ HTTP đi ra + transaction rollback — 0 gói tin tới máy thật
- [x] CA1 đủ 2 mã khác nhau: 12 req máy chấm công đều mang `ssn`, 3 req máy chấm cơm đều mang `rice_ssn`, không lẫn — PASS
- [x] CA2 thiếu mã chấm cơm: trả 422, chặn trước khi gọi máy — PASS (kiểm riêng)
- [x] CA3 thiếu mã chấm công: bỏ qua máy chấm công, máy cơm vẫn chạy đúng mã — PASS
- [x] CA4 không tick checkbox: 0 request — PASS
- [x] **Đã chốt 2026-08-18 — GIỮ NGUYÊN fallback** `Employee.php:103` (`rice_ssn = $employee->rice_ssn ?? $employee->info->ssn`) và `EmployeeService::createEmployee` (`rice_ssn = $employeeInfoDetail->ssn`). Lý do user: phần lớn 2 mã vốn trùng nhau, trùng hay khác đều được — yêu cầu duy nhất là lúc upload ảnh phải đọc đúng cột tương ứng (máy chấm công → `ssn`, máy chấm cơm → `rice_ssn`), việc này đã xong và test PASS. KHÔNG tách nguồn dữ liệu của 2 mã.

### Checkpoint — 2026-08-18
Vừa hoàn thành: test 4 ca bằng Http::fake, 3 PASS + 1 PASS khi kiểm riêng
Đang làm dở: (không)
Bước tiếp theo: (không) — user đã chốt giữ nguyên fallback, phần việc kết thúc
Blocked: không
