# Etek Power — xoá ca 10/10 + tính lại công định mức tháng 10/2026 (hỗ trợ dữ liệu PROD, chưa có số Redmine) — @cuong61n

Yêu cầu (29/10/2026): Etek Power đổi lịch — đi làm thứ 7 03/10, nghỉ thứ 7 10/10. HCNS đã thêm ca 03/10 nhưng quên xoá ca 10/10 → công định mức tháng 10 sai. Xoá ca 10/10 và tính lại công định mức tháng 10.

## Tasks

- [x] (29/10/2026) Điều tra — PROD `hrm-prod` `/var/www/etekpower` (nhánh `tpe`), DB `hrm_power`. Nghiệp vụ: ca Văn phòng (shift_detail 1, 31 NV) + Kinh doanh (shift_detail 2, 20 NV) chỉ làm thứ 7 lẻ (10, 24); tháng 10 đang có 3 thứ 7 (03, 10, 24) → công định mức 25, đúng phải 24. Ca 10/10 không ai chấm công → 28 người bị ghi "nghỉ không lý do", 10 người miễn chấm công vẫn được cộng 1 công. Ca Công trường (shift_detail 3, 5 NV) vốn làm mọi thứ 7 → user chốt GIỮ.
- [x] (29/10/2026) Sao lưu trước khi xoá (máy Cường, scratchpad phiên): `shift_detail_employee_dates` 10/10 ca 1,2 · `timesheet_summaries` + `timesheet_details` 10/10 của các NV đó · `timesheet_month_summary_detail` + header của bảng tổng hợp id 34.
- [x] (29/10/2026) Xoá trên PROD trong 1 transaction: 51 dòng `shift_detail_employee_dates` (10/10, shift_detail_id 1,2) + 34 dòng `timesheet_details` + 34 dòng `timesheet_summaries` ngày 10/10 của 51 NV đó (không có chấm công, không có overtime_details). Lý do xoá công ngày: màn xoá ca (`ShiftDetailEmployeeDateService::deleteEmployeeByDate`) không dọn công của ngày đã qua. Kiểm: còn lại đúng 5 ca + 5 dòng công của Công trường.
- [x] (29/10/2026) Tính lại bảng tổng hợp tháng 10 (`timesheet_month_summaries` id 34, nháp, HCNS id 278 tạo 15:33) bằng chính job `CreateTimesheetSummary::dispatchSync` cho 46 NV đang có trong bảng; header `standard` 25 → 24 (đúng giá trị save() sẽ tính cho người tạo). Kết quả: 27 NV 25→24 và nghỉ không lý do −1; 1 NV mới vào 24→23 (−1 KLD); 5 NV miễn chấm công 25→24 và tổng công −1 (bỏ công "ảo" ngày nghỉ); 2 NV 25→24; Công trường giữ nguyên 26/27. Log không lỗi.
- [ ] Lưu ý báo HCNS: 3 NV không được phân ca nào trong tháng 10 (Nguyễn Thị Mỹ Dung #73, Bùi Thị Loan #79, Đặng Phương Thảo #80) vẫn 25 công theo cách tính dự phòng (không thuộc phạm vi việc này). Lần sau đổi ngày làm/nghỉ: thêm ca ngày đi làm VÀ xoá ca ngày nghỉ trước khi tạo bảng tổng hợp.

Trạng thái: đã sửa dữ liệu PROD 29/10/2026, không đổi code.
