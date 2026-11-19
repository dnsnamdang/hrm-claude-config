# Điều tra phiếu phân công / đăng ký làm thêm trùng giờ — @cuong61n

Nguồn: chị Huyền báo (29/10/2026) — NV Nguyễn Thị Thu (10710029) ngày 10/01/2026 có cả PLT-3584 (tự đăng ký 08:30–19:49) và PCLT-3586 (phân công 08:00–23:00), báo cáo làm thêm chi tiết bị nhân đôi giờ.

## Phase 1 — Điều tra

- [x] Đọc luồng (29/10/2026): 3 màn dùng chung bảng `overtime_assignments` — Yêu cầu làm thêm (`overtime_requirements`), Đăng ký (`assignment_type=0`, 1 người, `employee_id`), Phân công (`assignment_type=1`, nhiều người ở `overtime_assignment_employees`).
- [x] Màn Đăng ký làm thêm không gửi `assignment_type` lên API → danh sách trả cả phiếu phân công (PCLT-…) → hiện nhiều người. Phiếu 3678 là phiếu phân công 14 người (P. Kế toán tài vụ), mở qua URL màn đăng ký.
- [x] Kiểm chặn trùng (29/10/2026): `OvertimeAssignmentRequest` đã kiểm trùng giờ cả 2 loại phiếu (join `overtime_assignment_employees`) từ commit `0bb1064f7` ngày 21/03/2026. Prod (`hrm_erp_gop`) còn 22 cặp trùng, phiếu mới nhất tạo 25/01/2026 — đều là dữ liệu cũ trước khi có chặn.
- [x] Quét lại toàn bộ (29/10/2026, mọi kiểu trùng, phiếu chờ duyệt/đã duyệt): 84 cặp / 55 NV / 73 lượt NV-ngày — 62 cặp đăng ký–đăng ký + 22 cặp đăng ký–phân công, từ 06/05/2023 tới 25/01/2026. Từ 26/01/2026 tới nay 0 cặp, dù mỗi tháng vẫn có 300–500 phiếu (khoảng 26/01–21/03 không phát sinh trùng). Đối chiếu `timesheet_summaries`: ngày trùng bị cộng đôi giờ (vd NV 189 ngày 10/01 lưu 19.0h). Cron `calc:many_timesheet` chỉ tính lại tháng hiện tại → sửa phiếu xong phải tính lại công cho riêng các NV-ngày bị trùng.
- [ ] Chờ chốt với chị Huyền: xử lý 22 cặp dữ liệu cũ (huỷ phiếu trùng hay để báo cáo bỏ trùng) + có tách danh sách Đăng ký chỉ hiện phiếu type 0 không.
