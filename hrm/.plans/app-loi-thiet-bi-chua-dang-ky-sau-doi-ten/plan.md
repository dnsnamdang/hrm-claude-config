# App chấm công báo "Thiết bị chưa được đăng ký" sau khi đổi tên app (điều tra 2026-11-19) — @cuong61n

Phản ánh (Ngô Thị Lý / Đào Thị Thúy, 19/11 08:39): một số người chấm công báo chưa đăng ký thiết bị, chỉ một số người; tưởng do chuyển cổng ETPower.

## Đã điều tra (chỉ đọc, chưa sửa gì trên prod)
- [x] BE `TimekeeperController::checkTimesheet`: báo lỗi khi không có bản ghi `devices` khớp ĐỒNG THỜI `device_id` + `employee_info_id` + `status = 2`. Đăng ký thiết bị mới → tự duyệt nếu là thiết bị đầu tiên hoặc `DEVICE_AUTO_APPROVE=true`; duyệt 1 thiết bị thì MỌI thiết bị đã duyệt cũ của người đó chuyển "Hết hạn" (4)
- [x] Prod site `tpe` (DB gộp `hrm_erp_gop`): `DEVICE_AUTO_APPROVE=true`; các site etek/etekpower/toyota/etekgreen: tắt
- [x] App iOS lấy mã thiết bị bằng `flutter_udid` 4.0.0: khóa Keychain = (`CFBundleName`, bundle id); không thấy khóa thì sinh mã mới từ IDFV. `CFBundleName = $(APP_DISPLAY_NAME)` ⇒ ĐỔI TÊN HIỂN THỊ APP = ĐỔI KHÓA KEYCHAIN = có thể đổi mã thiết bị. Android dùng `AndroidId` nên không ảnh hưởng
- [x] Mốc thời gian: build 111 (đổi tên HRM TPE → ETEKSOFT, commit `bc3fda4`) lên TestFlight 18/11 22:52 ngoài ý muốn; build 112 (ETEK SOFTS) 19/11 07:56. Hôm nay 06:44–08:39 có 15 người đăng ký lại thiết bị (14 iPhone, đều đã có thiết bị đã duyệt từ 2023–2025; công ty Tân Phát/Vinh/Hải Phòng/Etek Green — KHÔNG phải ETEKPOWER). Ngày 17/11 có 24 người ETEKPOWER đăng ký thiết bị = đợt chuyển cổng ETPower, tách biệt
- [x] Đỗ Mạnh Sơn (info 174, ssn 11910223): chỉ có 1 thiết bị Đã duyệt từ 2023-04-01 (mã `B03FE917-3…`) ⇒ mã app gửi lên khác mã này
- Chưa kiểm trên máy thật: giả thuyết "đổi CFBundleName ⇒ đổi mã" dựa trên mã nguồn thư viện + dữ liệu, chưa tái hiện

## Việc tiếp theo (chờ user quyết)
- [ ] Người bị lỗi: mở app → màn Đăng ký thiết bị (site tpe tự duyệt ngay)
- [ ] Chốt `CFBundleName` cố định (tách khỏi `APP_DISPLAY_NAME`) ở bản build sau để đổi tên hiển thị không làm đổi mã thiết bị
- [ ] Không đổi `APP_DISPLAY_NAME` / `CFBundleName` của app nào đang dùng thiết bị để chấm công mà chưa tính tới việc này
