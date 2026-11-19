# #9867 — Đơn xin nghỉ: tính sai số ngày nghỉ dự kiến — @cuong61n

Phần app (khoá ô số ngày, tự tính, đổi thứ tự ô) đã xong từ commit TPE_APP 36462ef. Còn lỗi BE: `AttendanceTrait::sumDate` giữ giờ bắt đầu cho mọi ngày (11/05 17:37 → 13/05 17:37 ra 1, đúng là 2).
Quyết định 19/10/2026 (user chọn A): tính theo GIỜ CA của NV, chia ca thành 2 buổi (theo giờ nghỉ trưa, ca không nghỉ trưa thì chia đôi); mỗi buổi bị khoảng nghỉ phủ ≥ 1 giờ (hoặc cả buổi nếu buổi < 1 giờ) tính 0,5. Ngày không có ca = 0; ngày lễ giữ quy tắc is_calc_holiday. Hàm dùng chung: API calculate-intend-day + tổng hợp công.
Ngưỡng 1 giờ: user chốt "cứ làm như hiện tại, sau cần sửa sẽ bảo" (19/10/2026).

## Phase 1 — BE
- [x] sumDate tính theo ca (`leaveDayOfShift` + `overlapMinutes`), batch 1 query ca theo khoảng ngày
- [x] Kiểm 19 case (NV 13, ca 08:30–17:30 nghỉ trưa 12–13): sáng/chiều/<1h/chỉ giờ trưa/ngoài giờ/nhiều ngày/CN không ca/T7 có ca/lễ is_calc 0-1 → 19/19
- [x] So 2.459 đơn nghỉ 2026: 14 đơn đổi giá trị (VD phiếu 11953: 1 → 2); tốc độ 2,2s vs 1,9s. Số ngày lưu trên đơn cũ không tự đổi, Tổng hợp công tính lại theo cách mới
