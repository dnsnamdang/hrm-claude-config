# Etek Power — bổ sung ca Công trường thiếu (Đạt 01/10, Huấn 20/10) + kiểm phép của Giang (hỗ trợ dữ liệu PROD, chưa có số Redmine) — @cuong61n

Yêu cầu (03/11/2026, HCNS Etek Power báo qua chat): Nguyễn Thế Huấn thiếu phân ca 20/10, Bùi Tiến Đạt thiếu phân ca 01/10 (ca Công trường); phép của bạn Giang tối qua đã cập nhật nhưng sáng nay chưa thấy lên.

## Tasks

- [x] (03/11/2026) Điều tra — PROD `hrm-prod` `/var/www/etekpower/hrm-api` (nhánh `tpe`), DB `hrm_power`. Bùi Tiến Đạt (#99): có ca Công trường từ 02/10, thiếu đúng 01/10. Nguyễn Thế Huấn (#105): chỉ có ca từ 21/10 đến 31/12, thiếu 20/10. Các NV Công trường khác (#32, #36, #82, #83, #103) đều có ca 2 ngày này → đúng là sót.
- [x] (03/11/2026) Sao lưu trước khi ghi: `timesheet_summaries` + `timesheet_month_summary_detail` (bảng id 34) của #99, #105 → `/tmp/bk_etekpower_20261103.txt` trên server hrm-prod.
- [x] (03/11/2026) Thêm ca bằng lệnh có sẵn `php artisan add:employee_timesheet` (không `--with-attendance`, không tự tạo dữ liệu chấm công): #99 ngày 01/10 và #105 ngày 20/10, ca Công trường (working_shift 7, shift_detail 3). Kiểm: 2 dòng `shift_detail_employee_dates` mới (id 376742, 376743), công ngày 1.00, không nghỉ không lý do.
- [x] (03/11/2026) Tính lại bảng tổng hợp tháng 10 (`timesheet_month_summaries` id 34, nháp) cho #99, #105 bằng `CreateTimesheetSummary::dispatchSync`. Kết quả: Huấn 7.96 → 10.96 công (chuẩn 27); Đạt 22.92 → 25.92 công, nghỉ không lý do 1 → 0 (chuẩn 27). Lưu ý: lần chạy đầu bằng `tinker <file>` bị treo vì tinker mở shell tương tác, đã kill, chạy lại bằng `tinker --execute`.
- [ ] Phép của Phạm Thị Hương Giang (#84): chưa tìm thấy đơn phép mới. Đơn bổ sung công 30/10 (#1738) bị từ chối 31/10 với lý do "yêu cầu tạo đơn nghỉ phép". DB không có bảng đơn nghỉ phép riêng → chờ HCNS cho biết ngày phép + màn đã nhập.

Trạng thái: đã sửa dữ liệu PROD 03/11/2026, không đổi code.
