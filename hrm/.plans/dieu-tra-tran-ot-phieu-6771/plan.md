# Điều tra trần 38 giờ làm thêm/tháng — phiếu 6771 (chưa có số Redmine) — @cuong61n

## Task 1: Điều tra vì sao NV Nguyễn Hoàng Việt (11910225) bị báo "chỉ làm thêm được 2 tiếng" ngày 25/10
- Nghiệp vụ: NV phản ánh chưa vượt 38 giờ/tháng nhưng khi đăng ký làm thêm 25/10 chỉ được đăng ký 2 tiếng.
- Kết quả đối chiếu prod (đọc DB, không ghi): quy định công ty 1 trần 38 giờ/tháng. Tháng 10 NV có phiếu 6699 đã duyệt: 17/10 08:30 → 18/10 20:00 = 35,5 giờ (khung liên tục qua đêm, hệ thống cộng nguyên 35,5h). Còn lại 38 − 35,5 = 2,5 giờ → phiếu 6771 (25/10 08:30–10:30 = 2h) lọt, nhiều hơn thì bị chặn. Logic: `OvertimeAssignmentService::checkMonthlyOvertimeLimit`.
- Nguyên nhân: phiếu 6699 đăng ký 1 khung 34 tiếng liền thay vì từng ngày → ăn gần hết trần. Code chặn đúng theo dữ liệu, không phải lỗi tính.
- [x] 02/11/2026 Điều tra xong, chưa sửa code. Chờ user chốt hướng (sửa dữ liệu phiếu 6699 hay đổi cách tính).

## Task 1 — bổ sung (02/11/2026, sau phản hồi user)
- Đối chiếu báo cáo `overtime_report_detail` (nguồn `timesheet_summaries.overtime_hour`): tháng 10 NV chỉ làm thêm thực tế 17/10 = 9,6h · 18/10 = 11,3h · 25/10 = 1,8h (tổng 22,7h). Phiếu 6699 thực tế ~20,9h chứ không phải 35,5h.
- Nguyên nhân gốc: `checkMonthlyOvertimeLimit` cộng theo GIỜ ĐĂNG KÝ (kết thúc − bắt đầu), khung liền qua đêm 17→18/10 kéo theo ~12,5h không làm → còn lại 2,5h thay vì ~17,1h. Sai lệch giữa kiểm trần và báo cáo.
- Đề xuất: (1) ngày đã qua lấy giờ thực tế từ chấm công, ngày chưa tới lấy giờ đăng ký; hoặc (2) tách phiếu qua đêm theo từng ngày. Chờ user chốt (hàm dùng chung `OvertimeAssignmentService`).
