# Cộng phép năm trong thời gian nghỉ thai sản — @cuong61n

## Điều tra 09/11/2026: NV nghỉ thai sản không được cộng phép (VD Nguyễn Thị Lan – KTCN, Trịnh Thị Lợi – QTTT)

- [x] 09/11/2026 Kiểm dữ liệu PROD (hrm_erp_gop, chỉ đọc): Lan (id 457) nghỉ thai sản 29/04–01/11/2026, phép tháng 5–11 = 0; Lợi (id 1214) nghỉ thai sản từ 01/07/2026 (loại nghỉ id 57), phép tháng 7–11 = 0. Các tháng trước nghỉ đều = 1.
- [x] Nguyên nhân 1 (cấu hình, đúng như đang cài): công ty 1 bật "Tính phép cho thời gian nghỉ thai sản" nhưng chọn kiểu 2 "Chỉ tính phép cho tháng có số ngày công ≥ 13" → tháng nghỉ trọn 0 công nên không được cộng. Muốn cộng đủ phải đổi sang kiểu 1 "Tất cả thời gian nghỉ đều được tính phép".
- [x] Nguyên nhân 2 (BUG code): `AttendanceService::getListAttendance` lọc nhóm loại nghỉ bằng `whereIn('id', $leave_type_ids)` (id đơn nghỉ) thay vì `leave_type_id` → `calcUsableLeaveDays` không bao giờ nhận ra đơn thai sản. Hệ quả: nếu công ty chọn kiểu 1 thì vẫn KHÔNG được cộng. Do commit "fix" đổi từ `where('group_id')`.
- [x] 09/11/2026 (a) Sửa `whereIn('leave_type_id', ...)` ở `AttendanceService::getListAttendance` (chỉ 1 nơi gọi có group_id). Đã đẩy `gop_db` (e64feddc2) và `tpe` (d48ac0a62); chạy `~/build_tpe.sh` lên PROD TPE (BE đã pull, migrate + route:cache + catalog-sync OK; FE build đang chạy lúc ghi).
- [ ] Còn chờ chốt: (b) có đổi cấu hình công ty 1 sang kiểu 1 không; (c) tính lại phép năm 2026 cho 2 người (job updateData).
- [x] 09/11/2026 Công ty 1 đã đổi cấu hình sang "Tất cả thời gian nghỉ đều được tính phép". FE+BE build xong PROD TPE. Tính lại phép năm 2026 (logic `updateDataAll`, qua tinker) cho 7 NV: Phương(624), Nga(521), Thúy(23), Mai(478), Lan(457), Ngoan(602), Ngọc(625). Chỉ đổi các tháng nghỉ thai sản 0→1 + tổng phép/còn lại; backup số cũ ở `/tmp/backup_phep_*.json` trên server hrm-prod. Trịnh Thị Lợi (1214) không có trong danh sách nên chưa tính lại.

## Sửa 09/11/2026: tháng quay lại sau thai sản bị +1 phép dù chưa đủ công (khách báo Lan: đang +2 phép ứng)

- [x] 09/11/2026 Tra PROD (chỉ đọc): Lan nghỉ thai sản đến 01/11 → tháng 11 bị coi là "tháng thai sản", cấu hình "tất cả thời gian nghỉ đều được tính phép" trả +1 ngay (mới làm 7 công) + phép ứng tháng 12 +1 = +2. Mong muốn: tháng 11 chỉ +1 khi đủ công (≥12), chỉ giữ +1 phép ứng tháng 12.
- [x] 09/11/2026 Sửa `EmployeeAttendanceService::calcUsableLeaveDays` (+ hàm mới `mergeMaternityRanges`): tháng chỉ là "tháng thai sản" khi kỳ nghỉ (gộp các đơn liền kề) phủ TRỌN tháng, hoặc chạm tháng mà không có ngày công nào. Tháng đầu/cuối kỳ còn đi làm → tính theo quy tắc thường (đủ công). Đã thử local (rollback) với config PROD: Lan Nov 7 công → 0, Nov 12 công → 1, tháng 5–10 vẫn 1.
- [x] Tìm hiểu: phép KHÔNG bị tính âm — `remaining_leave_days` chặn ở 0, `getRemainingLastYear` trả 0 nếu ≤0; thiếu công cả T11+T12 thì ngày ứng thành cho không (chưa có logic truy thu).
- [x] 09/11/2026 Đã đẩy `gop_db` (e6c44d01c) và `tpe` (96b2e5aee); pull lên PROD TPE bằng `build_tpe.sh` (BE đã pull; bước migrate bị huỷ vì hỏi yes/no ở môi trường production, không có migration chờ; đã chạy tay route:cache + catalog-sync OK).
- [x] 09/11/2026 Tính lại phép 2026 cho 7 NV (Lan 457 + 6 NV chạy sáng nay), backup số cũ `/tmp/backup_phep_20261109_135552_v2.json` trên hrm-prod. Kết quả: Lan T11 1→0 (còn 6,5); Phương(624) T6 1→0 (còn 10); Thúy(23) T4 1→0 (còn 4); Mai(478) T11 1→0 (tổng 12); Nga(521), Ngoan(602) không đổi; Ngọc(625) chỉ đổi định dạng. Các tháng bị trừ là tháng đầu/cuối kỳ thai sản chưa đủ 12 công — đúng quy tắc mới.
