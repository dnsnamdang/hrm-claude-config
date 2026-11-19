# Điều tra: Cao Sỹ Biên (ETEK, tự động hoá) đăng ký cơm nhưng không chấm được — @cuong61n

Nguồn: HCNS báo 30/10/2026 (không có số Redmine). Môi trường: PROD, DB `hrm_erp_gop`, máy quét cơm `rice_conn_infos.id=1` (14.248.82.176:4382). Chỉ đọc, không sửa dữ liệu.

## Tasks
- [x] (30/10/2026) Tra hồ sơ cơm: `rice_employee_infos.id=725`, mã cơm 70241, ETEK (rice_company_id=4), status=1; bản ghi cũ bên TPE (id=452, mã 12510534) đã nghỉ (status=0) nên không gây trùng
- [x] (30/10/2026) Tra đăng ký: đăng ký đủ các ngày 12→30/10. Ngày 12, 13, 21, 22/10 = Đã ăn (3). Từ 23/10 đến 29/10 cron 13:20 đều đánh Không ăn (4). Hôm nay 30/10 = Đã đăng ký (1)
- [x] (30/10/2026) Log cron `rice:update-meal-checkin-regular`: ngày nào mã 70241 cũng "Cập nhật thành công – được phép check-in" (10:14 / 10:44 / 11:14), kể cả 23→30/10 → phía HRM vẫn đẩy quyền lên máy đúng
- [x] (30/10/2026) Đọc người dùng trên máy qua ISAPI: có 70241 "Cao Sỹ Biên", có 1 khuôn mặt, khung hiệu lực hôm nay là 10:10→13:20 → đúng
- [x] (30/10/2026) Đọc log sự kiện trên máy (AcsEvent): 21/10 12:06 và 22/10 12:13 quét mặt thành công. Từ 23→29/10 KHÔNG có sự kiện nào mang mã 70241, kể cả lượt bị từ chối "ngoài khung giờ" (minor 8). Mỗi ngày chỉ có 1–3 lượt "không nhận ra mặt" (minor 76); đã xem ảnh chụp của 8 lượt đó, không thấy giống ảnh đăng ký của anh Biên
- [x] (30/10/2026) Kết luận: hệ thống và máy đều đúng. Từ 23/10 máy không ghi nhận lượt quét nào của anh Biên → cần hỏi anh ấy có quét ở máy này không / quét lúc mấy giờ, rồi cho anh ấy quét thử trưa nay để kiểm lại ngay
- [ ] Chờ HCNS phản hồi lượt quét thử hôm nay (30/10)
