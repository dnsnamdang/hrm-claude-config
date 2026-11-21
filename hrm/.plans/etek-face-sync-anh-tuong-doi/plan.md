# Đồng bộ khuôn mặt lên máy chấm công khi ảnh hồ sơ là đường dẫn tương đối (ETEK, nhánh tpe) — @cuong61n

Redmine: chưa có số.

## Nghiệp vụ
Ở hồ sơ nhân sự, tick "Tạo nhân sự trên máy chấm công/chấm cơm khuôn mặt" rồi Lưu thì hệ thống phải tạo user và đẩy khuôn mặt lên các máy chấm công/chấm cơm còn thiếu.

## Điều tra (21/11/2026)
- [x] 21/11 Thử trên cổng ETEK: lưu hồ sơ 315 (Trần Hoàng Diệu, mã CC 1128) → báo thành công nhưng "Máy chấm cônG HCM 2" (conn_infos.id 16, Hikvision, status 2) không có user 1128; `face_last_synced_at` vẫn NULL. Kiểm trực tiếp trên giao diện máy (Person Management): máy chỉ có 1 user `quantri`.
- [x] 21/11 Nguyên nhân: `EmployeeInfoService::syncFaceToDevices` chỉ chạy khi `employee_infos.image` bắt đầu bằng http(s). Ảnh của 315 là `/uploads/1712912109tran-hoang-dieu.jpg` (đường dẫn tương đối) → hàm thoát im lặng, không lỗi, không log. Đã đối chiếu code + DB `hrm_etek` + file thật trên server.

## Sửa
- [x] 21/11 `loadFaceImageBinary()` trong `Modules/Human/Services/EmployeeInfoService.php`: link http(s) tải qua HTTP; đường dẫn tương đối đọc thẳng file trong `public/` (prod có APP_URL=http://localhost nên không ghép được từ config), không có file thì ghép host request rồi tải. Chặn `..`.
- [x] 21/11 Commit `5af85c586`, push nhánh `fix-face-sync-relative-image` rồi push fast-forward lên `tpe`.
- [x] 21/11 Deploy ETEK: `git pull origin tpe` ở `/var/www/etek/hrm-api` (chỉ backend, không chạy build_etek.sh vì script gọi PermissionsTableSeeder đã gỡ). Kèm theo commit `0e236c878` (sửa báo cáo lương) mà ETEK chưa có.
- [x] 21/11 Test lại trên ETEK: lưu hồ sơ 315 → log `Upload face success` cho SSN 1128 trên 5 máy (gồm 14.241.235.143:4371), `face_last_synced_at` có giá trị, `has_face=1` ở máy 11,12,14,15,16; giao diện máy HCM 2 (Person Management) hiện user 1128 Trần Hoàng Diệu kèm khuôn mặt.
- Trạng thái: ĐÃ DEPLOY ETEK 21/11/2026, đã test đạt.

## Còn lại
- [ ] Đếm số nhân sự ETEK có `image` tương đối để biết quy mô.
- [ ] Lưu ý: máy đã có mặt thì không ghi đè khi đổi ảnh (`deviceUserAlreadyExistFace` → bỏ qua) — chưa sửa.
