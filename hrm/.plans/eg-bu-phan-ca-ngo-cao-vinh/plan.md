# Bù phân ca & công T10–đầu T11/2026 cho anh Ngô Cao Vinh (EG) — @cuong61n

Redmine: chưa có số (EG nhờ trực tiếp, 09/11/2026).

## Bối cảnh
EG (Etek Green, công ty 9) quên phân ca cho anh Ngô Cao Vinh (employee_info_id 1619) từ 20/10 đến 08/11/2026, nên không có công để làm lương.
Cổng EG riêng (`hrm_green`) đã tắt từ 30/09/2026 → dữ liệu thật nằm ở DB TPE `hrm_erp_gop` (không sửa `hrm_green`).
Lưu ý có 2 người trùng tên: id 451 (công ty 7 "Etek Green (cũ)", không có ca) và id 1619 (công ty 9) — chỉ sửa 1619.

## Task
- [x] 09/11/2026 Điều tra: ca của anh có đến 19/10 và từ 09/11 (EG tự thêm từng ngày hôm nay), hổng 16 ngày làm việc: 20–24/10, 26–30/10, 02–07/11. Mẫu T10 1–19 khớp đồng nghiệp cùng ca HC.
- [x] 09/11/2026 Bù 16 dòng `shift_detail_employee_dates` (ca HC id 60, chi tiết ca 56) cho 1619 trên prod (id 18379376–18379391). Kết quả: T10 = 24 ngày ca, T11 = 23 ngày ca (khớp đồng nghiệp).
- [x] 09/11/2026 Tạo dòng công ngày + tính lại cho 1619, 20/10–08/11, chỉ riêng 1 người (`createTimesheetDetail` + `calcAllTimesheet`; KHÔNG chạy `calc:many_timesheet` vì tính cả hệ thống). Kết quả: T10 = 24 dòng / 24.00 công, T11 (đến 09/11) = 7 dòng / 7.00 công, không đi trễ/phạt. Anh không có giờ quẹt (giống T9: 21 ngày/21.00 công).
- [ ] Chưa làm: ghi lịch sử phân ca (`shift_assignment_history`) cho 16 ngày bù — bù bằng script nên không có dòng lịch sử.
- [ ] Chưa làm: bảng chấm công tổng hợp T10/2026 của công ty 9 chưa tồn tại (bảng cuối là T04/2026) — EG tự tạo trên màn bảng công tổng hợp để làm lương.

## Phát hiện thêm (chưa sửa, chờ xác nhận)
- Hoàng Ngọc Điệp (EG-104, id 1753, vào 01/10): chỉ có ca 01–19/10, không có ca từ 20/10 trở đi — cùng kiểu hổng.
- Đỗ Trung Kiên (id 1642): T10 có 23 ngày, đồng nghiệp 24 — thiếu 1 ngày chưa rõ nguyên nhân (có thể nghỉ).

## Trạng thái
Đã sửa dữ liệu prod 09/11/2026 (không có commit code). Chờ EG kiểm tra lại bảng công anh Vinh.
