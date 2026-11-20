# Fix mã thông báo nội bộ bị trùng, không gửi được (/human/self-notification) — @cuong61n

## Task
- [x] 20/11/2026 — Điều tra: thông báo #23 bấm gửi lỗi 500. Log prod: `Duplicate entry '009/2026/TB-TPE'` (unique `self_notifications_code_unique`). Nguyên nhân: `SelfNotifications::getNextCodeAttribute()` sinh mã bằng ĐẾM số dòng có mã trong năm + 1; dãy mã bị thủng (mất 008, #19 giữ 009) nên đếm 8 → sinh lại 009. Kiểm bằng log prod + đọc bảng.
- [x] 20/11/2026 — Sửa: lấy SỐ THỨ TỰ LỚN NHẤT trong năm + 1 (`Modules/Human/Entities/SelfNotifications.php`). Kiểm trên prod bằng tinker: hàm trả `010/2026/TB-TPE`.
- [x] 20/11/2026 — Đã push `gop_db` (commit 117e9ac4d) và deploy prod bằng `~/build_tpe.sh`. Thông báo #23 vẫn là nháp, người dùng bấm Gửi lại.
- Ghi chú: thông báo gửi tới "công ty" chốt người nhận lúc bấm gửi, nhân viên vào sau (vd hồ sơ tạo 16/11) không nhận — theo thiết kế hiện tại, chưa đổi.
