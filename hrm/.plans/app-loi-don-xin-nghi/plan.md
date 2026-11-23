# Lỗi app đơn xin nghỉ: lọc theo nhân viên + số ngày nghỉ (chưa có số Redmine) — @cuong61n

## Phase 1 — Điều tra + sửa (23/11/2026)
- [x] (23/11) Lọc theo nhân viên ở danh sách đơn xin nghỉ trên app ra 0 đơn, đơn mới tạo không thấy.
  - Nguyên nhân: BE lọc `employee_id` theo `attendances.created_by` (employees.id); ô chọn của app gửi employee_infos.id (VD chị Huyền: 867 vs 1258). Web dùng employees.id nên đúng, không đụng.
  - BE: thêm tham số `employee_info_id` lọc `attendances.employee_id` (`AttendanceService::filter`). App: `fetchAttendances` gửi `employee_info_id`.
  - Đã kiểm: tinker với tài khoản 867 — web employee_id=867 → 55 đơn, app employee_info_id=1258 → 55 đơn, sai loại id → 0. Chưa bấm thử trên simulator.
  - Trạng thái: BE đã đẩy `gop_db` (81e51f264), app đã đẩy `develop` (3841888). Chưa deploy dev/prod.
- [ ] Số ngày nghỉ dự kiến sai (30/11–01/12 ra 1 ngày): không phải lỗi app. Bảng `shift_detail_employee_dates` ngày 30/11 chỉ có 384 người (các ngày khác ~808), NV 1258 thiếu ca 30/11 nên BE tính 0 công. Chờ Nhân sự/Chấm công kiểm phân ca 30/11; chưa sửa dữ liệu prod.
