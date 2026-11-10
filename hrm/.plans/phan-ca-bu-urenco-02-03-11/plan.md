# Bù phân ca 02–03/11/2026 cho 3 NV Phòng Dự án trọng điểm (ca CT Urenco) — @cuong61n

Redmine: chưa có số (người phụ trách phòng nhờ trực tiếp, 10/11/2026: "thêm hộ chị ca 2 ngày này của 3 bạn này").

## Bối cảnh
3 NV (employee_info_id): 1769 Sầm Văn Linh (12611198), 1770 Nguyễn Thế Huấn (12611199), 1771 Nguyễn Quang Tuyến (12611200), phòng 95. Ca CT Urenco (working_shift 74, chi tiết ca 65) chỉ được gán từ 04/11 → bảng công ngày 02, 03/11 trống. Ngày vào làm của cả 3 đều trước 02/11 (12/10, 20/10, 14/10).

## Task
- [x] 10/11/2026 Điều tra: không có dòng phân ca nào trước 04/11; không có dòng quẹt nào trong `timesheets`; công 04/11 đến từ "yêu cầu cập nhật công" đã duyệt.
- [x] 10/11/2026 Chèn 6 dòng `shift_detail_employee_dates` (ca 74, chi tiết ca 65) cho 3 NV × 02, 03/11 trên prod (`hrm_erp_gop`).
- [x] 10/11/2026 Tạo dòng công ngày + tính lại (`createTimesheetDetailEmployeeByDate` + `calcTimesheetEmployee`) chỉ riêng 3 NV × 2 ngày. Kết quả: có dòng công ca 74 nhưng labour_day = 0 (không có giờ quẹt).
- [ ] Chờ xác nhận: 02–03/11 có tính 1 công không? Nếu có → 3 NV tạo "Yêu cầu cập nhật công" (như 04/11) hoặc nhờ ghi công trực tiếp.
- [ ] Chưa ghi lịch sử phân ca (`shift_assignment_history`) — bù bằng SQL.

## Trạng thái
Đã sửa dữ liệu prod 10/11/2026 (không có commit code).
