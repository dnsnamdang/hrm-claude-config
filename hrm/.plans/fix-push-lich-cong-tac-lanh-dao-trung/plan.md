# Fix push lịch công tác lãnh đạo hiện trùng nhiều lần (chưa có số Redmine) — @cuong61n

Người phụ trách: @cuong61n · Nhánh: `develop` (hrm-api)

## Phase 1 — Điều tra
- [x] 10/11/2026 — Nhân viên Hoàng Trung Hậu (employee_info 246) báo máy nhận 3 push giống hệt cho cùng 1 lần ông Phong sửa lịch (16:23 ngày 09/11).
  - Đã kiểm trên prod (chỉ đọc): mỗi người nhận chỉ có đúng 1 dòng `notifications`; không có job lỗi/retry; chỉ 1 chỗ trong code gửi loại này (`LeaderScheduleService::announce`) ⇒ server gửi 1 lần.
  - Đã loại: token cũ (Hậu đã cài bản mới + đăng nhập lại), topic môi trường khác (nội dung giống hệt), app tự hiện thêm thông báo (chỉ Android).
  - Chưa tìm được nguyên nhân gốc (nghi FCM/APNs giao lặp hoặc iOS hiển thị lặp). Chưa gửi push thử tới máy Hậu.

## Phase 2 — Giảm nhẹ triệu chứng
- [x] 10/11/2026 — Thêm khoá gộp push: các push cùng 1 lịch được hệ điều hành gộp thành 1 dòng dù bị giao lặp.
  - `FCMService::setCollapseKey()` → iOS `apns-collapse-id`, Android `notification.tag` (tối đa 64 byte, tự xoá sau mỗi lần gửi).
  - `SendNotification` chỉ đặt khoá cho type `leaderSchedule`: `leaderSchedule_{id lịch}`; loại thông báo khác giữ nguyên.
  - Đã kiểm: dựng payload bằng reflection — có khoá thì có đủ 2 trường, không khoá thì không có; `php -l` sạch.
  - Test (10/11/2026): thêm `Modules/Assign/Tests/Feature/LeaderSchedule/PushCollapseKeyTest.php` (3 test, 12 assertion, qua) chạy thật `SendNotification::handle()` + `FCMService` với Firebase giả: lịch lãnh đạo có khoá `leaderSchedule_{id}` ở `apns-collapse-id` + `tag`; loại khác không có khoá; khoá không rò sang push kế tiếp; tiêu đề/nội dung/priority/sound không đổi. `AnnounceLeaderScheduleJobTest` (3 test) qua.
  - Cả nhóm LeaderSchedule: 57 test, 23 failures + 5 errors NHƯNG trên code cũ cũng 23 failures (+6 errors) — do DB local thiếu bảng `leader_schedule_settings` + API trả 400/500, không liên quan push.
  - Trạng thái: đã commit `ed9a05b84` đẩy nhánh `gop_db`, đã kéo về prod `/var/www/tpe/hrm-api` ngày 10/11/2026 (11:05); commit `2b399fe73` trên `develop` (chỉ ở local, chưa push). Không có migration/route mới. Worker queue mặc định (`--max-time=360`) tự nạp code mới sau tối đa 6 phút.
- [x] 10/11/2026 — Deploy prod (chưa deploy dev).
- [ ] Nhờ Hậu xác nhận còn trùng không (khi lưu lịch thử, mỗi lịch chỉ còn 1 dòng).
- [ ] Nếu vẫn trùng: gửi push thử tới topic của Hậu để xác định nguồn trùng (cần được đồng ý vì gửi push thật).

### Checkpoint — 10/11/2026
Vừa hoàn thành: thêm khoá gộp push cho lịch công tác lãnh đạo (FCMService + SendNotification)
Đang làm dở: không
Bước tiếp theo: bạn duyệt commit/push + deploy; sau đó nhờ Hậu thử lại
Blocked: không
