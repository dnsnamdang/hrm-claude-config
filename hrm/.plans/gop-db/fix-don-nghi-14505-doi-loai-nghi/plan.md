# Sửa dữ liệu PROD: đơn xin nghỉ 14505 đổi "Nghỉ ốm hưởng BHXH" → "Nghỉ phép" và trừ phép — @cuong61n

Không có số Redmine. Yêu cầu qua chat 29/10/2026: nhân viên chọn nhầm loại nghỉ (đã báo HCNS, sửa lần này rồi sau họ tự chịu trách nhiệm). Đơn https://hrm.eteksofts.com/timesheet/attendance/14505 — Lý Quốc Nam (11210082), nghỉ 28–30/10/2026, 3 ngày, đã duyệt.

- [x] Tra cách hệ thống trừ phép: số phép đã dùng lấy từ `timesheet_summaries.work_day_phep` (do `calc:employee_timesheet` tính khi duyệt đơn), số phép còn lại `employee_attendances.remaining_leave_days` do cron `update:attendance` 12:00 hằng ngày tính lại. Lưu ý `attendances.employee_id` là id hồ sơ (`employee_infos`), không phải `employees` — 29/10/2026
- [x] Kiểm số dư trước khi sửa: phép 2026 có 19, đã dùng 6,5, bị trừ 4, còn 8,5 → đủ trừ 3 ngày (còn 5,5) — 29/10/2026
- [x] PROD: `attendances` 14505 `leave_type_id` 18 → 3 (giữ nguyên trạng thái Đã duyệt, người duyệt) — 29/10/2026
- [x] PROD: chạy `calc:employee_timesheet 327 2026-10-28 2026-10-29` → công 28, 29/10 từ `work_day_huong_bhxh = 1` thành `labour_day 1 / work_day_phep 1` (giống 26–27/10). Ngày 30/10 chưa tới, cron tính công hằng ngày tự tính theo loại mới — 29/10/2026
- [ ] Sau 12:00 29/10 kiểm `remaining_leave_days` đã giảm (cron `update:attendance`); sau 30/10 phải còn 5,5

### Checkpoint — 2026-10-29
Vừa hoàn thành: đổi loại nghỉ đơn 14505 + tính lại công 28–29/10
Đang làm dở: —
Bước tiếp theo: kiểm số phép còn lại sau cron 12:00
Blocked:
