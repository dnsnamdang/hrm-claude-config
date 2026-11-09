# Mất lượt quẹt máy chấm công do mã cơm cũ trên máy (ETEK GREEN) — @cuong61n

## 09/11/2026: Nguyễn Thanh Bình (EG, employee_info 1651) ngày 6/11 chấm đủ nhưng bảng công = 0

- [x] Nguyên nhân: máy 36 (Máy chấm công ETEK GREEN tầng 2) có 2 bản ghi cho cùng người: 92211085 (mã mới) và 30032 (= `old_rice_ssn`, mã cơm cũ). Lượt quẹt ghi mã 30032 bị `attendance:fetch` bỏ vì chỉ tra `ssn` và `old_ssn` (old_ssn của anh Bình = 27). Log PROD: 17 lượt 2–7/11, chỉ riêng mã 30032 (không mã nào khác).
- [x] Bù 17 lượt vào `timesheets` (employee_info_id=92211085, conn 36, machine_type 2, company 9) bằng firstOrCreate như fetch; 12 dòng mới, 5 dòng đã có.
- [x] Tính lại công riêng anh Bình ngày 2–7/11 (`calcAllTimesheet` 1 người): 6/11 từ 0 → 1 công (đi muộn 32'); các ngày khác giữ nguyên.
- [x] Xoá bản ghi 30032 trên máy 36 qua ISAPI (UserInfo/Delete), giữ 92211085 (có 1 khuôn mặt).
- [ ] Chưa làm: sửa `attendance:fetch` tra thêm `old_rice_ssn`; chưa quét máy 36/37 xem còn ai mang mã cơm cũ (73/131 mapping ETEK GREEN có old_ssn ≠ old_rice_ssn).
- [x] 09/11/2026 Đối chiếu mã trên máy với `employee_infos.ssn` (chỉ đọc): máy 36 và 37 mỗi máy 121 người, 98 khớp ssn ETEK GREEN, 21 là NV công ty 1/8 dùng chung máy (hợp lệ), mồ côi thật: 01250135 Lê Danh Tiến (máy 36, trùng 92511150), 30032 Nguyễn Thanh Bình còn trên máy 37, 1345 DNS Admin. Máy 37 thiếu 3 NV đang làm (92511146, 92511152, 92511154). Máy 35 (mcc.etekgroup.vn:4381) không kết nối được. Chưa sửa gì trên máy.
- [x] 09/11/2026 Sửa máy theo đối chiếu: xoá 01250135 (Lê Danh Tiến, máy 36) và 30032 (Nguyễn Thanh Bình, máy 37) — mã đúng 92511150 / 92211085 đã có khuôn mặt cùng máy; thêm vào máy 37 Trần Văn Pháp (92511146), Nguyễn Quốc Huy (92511152), Nguyễn Mạnh Linh (92511154), khuôn mặt chép từ máy 36. Quét lại xác nhận.

## 09/11/2026: ETEK — máy THANG MÁY 2 (101.99.15.111:8882, conn 10) báo "Lỗi kết nối"

- [x] Nguyên nhân: cổng mở, `deviceInfo` trả 200 nhanh, nhưng `AcsEvent` (cron `attendance:fetch`) treo >30s → cURL 28 → status 3. Lỗi mỗi 5 phút từ 5/11 đến 10:05 ngày 9/11 (288 lần/ngày), tự hết từ 10:10. Trước đó lỗi rải rác từ 17/05 (1.603 lần). Máy KẾ TOÁN :8884 mất kết nối hẳn từ 02/2026 (>57.000 lỗi) — cần người ở VP kiểm tra.
- [x] Thiệt hại: ~2.340 lượt quẹt 5–8/11 chưa vào `timesheets` (6/11: 1.088 trên máy / 0 trong hệ thống; 7/11: 971 / 0).
- [x] Lấy bù từng ngày 5–9/11 bằng `attendance:fetch` trên PROD ETEK (bản này chưa có `--conn` nên hút mọi máy, firstOrCreate không trùng); đối chiếu sau bù: 6/11 1.067, 7/11 963 (thiếu ~21 và ~8 so với máy, chưa tra rõ).
- [x] Tính lại công 5–9/11 bằng `calc:many_timesheet 2026-11-05 2026-11-09` (10:53 → 11:01).
- [ ] Lưu ý: khi dò máy em lỡ dùng mật khẩu mặc định cổng 8881/8882, máy trả 401 vài lần nhưng không khoá; sau đó dùng đúng tài khoản trong DB.
