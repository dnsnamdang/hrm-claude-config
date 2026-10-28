# #10413 — [PL08-App TPE] Thay logo app mới — @cuong61n

TPE_APP `develop`. User chốt 19/10/2026: logo màn đăng nhập lấy từ API BE (không đóng gói), áp cho Tân Phát (develop/production/erp) + Etek (staging), Etek Power (tanphat), Wetek — BE có logo thì dùng, không thì ảnh đóng gói. Flavor khác giữ nguyên.
Logo trong task = logo đang cấu hình ở BE (`master-settings` category logo, …/logo-2025jpg-1730970778-U6l6.jpg) — không phải upload gì thêm.

## App
- [x] `GET v1/master-settings?category=logo` (công khai, client không token) → `UserApiServiceV2.fetchLoginLogoUrl()`
- [x] Widget `custom_view/login_logo.dart`: URL lưu SharedPreferences (`loginLogoUrl`) → lần sau hiện ngay/offline; CachedNetworkImage, lỗi/đang tải → `env.loginLogo`
- [x] `Flavor.useServerLoginLogo`; màn đăng nhập dùng `LoginLogo`
- [x] Kiểm BE thật (chỉ đọc): TPE prod/dev trả logo mới; Etek, Etek Power trả logo riêng; Wetek đang 503 → app dùng ảnh đóng gói
- [x] Test simulator: màn đăng nhập hiện logo "Tân Phát Etek – Hội tụ tinh hoa…" lấy từ API
- [ ] Icon app ngoài màn hình + splash: KHÔNG lấy từ API được (OS bắt đóng gói) — cần file logo vuông nếu muốn đổi
