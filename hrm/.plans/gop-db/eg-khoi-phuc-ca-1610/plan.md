# Khôi phục ca bị xoá nhầm ngày 16/10/2026 của công ty EG (chưa có số Redmine) — @cuong61n

## Bối cảnh
Ngày 16/10/2026 lúc 18:18–18:19, tài khoản Vũ Tiến Hoà (employee_info 1192) dùng chức năng "Gỡ ca khỏi ngày làm việc" nên cả công ty EG (company_id=9) bị xoá ca từ 16/10 (lịch sử `shift_assignment_history` id 870–873). Nhân viên đã làm đơn xin nghỉ cho ngày đó (VD Nguyễn Thanh Hùng 90611058) nhưng màn Tổng hợp phân ca trống.

## Task
- [x] 04/11/2026 — Tra nguyên nhân qua `shift_assignment_history` (prod, chỉ đọc); xác nhận 16/10 có 0 người có ca, 19/10 trở đi đã được gán lại.
- [x] 04/11/2026 — Khôi phục ca ngày 16/10 cho 100 NV EG (90 Hành chính, 9 Kinh doanh, 1 Tạp vụ) vào `shift_detail_employee_dates`, lấy danh sách từ cột `employees` của lịch sử 870/871/873, đúng ca + shift_detail cũ; chạy trong transaction, bỏ qua người đã có ca. Kết quả: EG có 100 NV có ca ngày 16/10. Chỉ ngày 16/10 (không khôi phục thứ 7 17/10 theo yêu cầu).
- [x] 04/11/2026 — Theo file EG.xlsx: bổ sung ca 19–22/10 và 24/10 cho 10 NV (Miền, Chương, Hoàng KD1, Trang, Quỳnh, Lan, Linh, Quang, Liên, Kiên [21,22,24]) = 48 dòng; thứ 7 24/10 dùng ca thứ 7 (KD → ca 65, Tạp vụ → ca 66). Tạ Quang Hào và Nguyễn Thanh Hùng (16/10) đã có ca từ bước trên.
- [x] 04/11/2026 — Chạy lại công trên prod (`/var/www/tpe/hrm-api`, nhánh gop_db): `create:many_timesheet_detail_by_employee` + `calc:employee_timesheet` cho 10 NV (19–24/10) và Hùng, Hào (16/10).

## Kiểm tra / lưu ý
- Công 19–24/10 đã sinh đủ dòng; còn vài ngày 0 công "nghỉ không lý do" (Chương 20/10; Lan 19, 21/10 và nửa ngày 24/10; Quang 19–22 và 24/10; Trang, Linh 24/10; Liên nửa ngày 24/10) do không có dữ liệu quẹt trong `timesheets` — cần xác nhận lại với EG.
- Khôi phục ca ghi trực tiếp DB nên màn Lịch sử phân ca không có dòng cho lần này.
- Trạng thái: đã chạy trên PROD ngày 04/11/2026.
