# Tắt chuông thông báo (web + app) (không có số Redmine) — @cuong61n

Người dùng tự tắt chuông có hẹn giờ để đỡ phiền: không push về app, không toast/âm báo/số đỏ trên web, nhưng thông báo vẫn vào danh sách.
Chốt 17/11/2026: tắt có hẹn giờ (1 giờ · hết hôm nay · 8:00 sáng mai · đến khi bật lại) · 1 cài đặt theo tài khoản dùng chung web + app.

## Phase 0 — Thiết kế
- [x] 17/11/2026 — Vẽ thiết kế trên Pencil `~/Downloads/meeting-mobile_v2.pen` (cuối file): W1–W3 (web: dropdown chuông bình thường / chọn giờ / đang tắt), N1–N4 (app: màn Cài đặt chỉ còn 1 dòng "Thông báo" → trang Cài đặt › Thông báo gom Tắt chuông + Theo loại [Nhắc việc, Thông báo cơm] / sheet chọn giờ / đang tắt) + S4 (dải nhắc ở màn Thông báo, tuỳ chọn). Không gộp Thông báo cơm vào Nhắc việc (khác bản chất), gom chung 1 trang Thông báo. Ban đầu để nút ở header Thông báo, user chọn chuyển sang Cài đặt 17/11/2026 → đã bỏ khung cũ. Chờ user duyệt thiết kế.

## Phase 1 — BE (hrm-api, nhánh gop_db)
- [x] 17/11/2026 — Bảng `notification_mutes` (employee_info_id unique · muted_until · is_indefinite) + `App\Models\NotificationMute` + `App\Support\NotificationMuteService` (4 mốc `1h/today/tomorrow/forever`, `state()` trả `muted`/`until_text`).
- [x] 17/11/2026 — API chính chủ, không cần quyền: `GET|POST|DELETE timesheet/notifications/mute` (`NotificationsController::muteState/mute/unmute`).
- [x] 17/11/2026 — Chặn ở 3 cổng chung: `NotificationSocket::publish` (web), job `Timesheet\SendNotification` + `Rice\SendMobileNotification` (FCM). Dòng `notifications` vẫn ghi → danh sách đủ. Lỗi tra cứu coi như KHÔNG tắt.
- Kiểm: script PHP gọi service + controller với 4 mốc/hết hạn/bật lại/preset sai (422) — đúng. Migrate local OK. Chưa commit.
## Phase 2 — Web (hrm-client, nhánh gop_db)
- [x] 17/11/2026 — `components/BasicSubsystem.vue`: nút "Tắt chuông ▾" ở chân dropdown + menu 4 mốc, chuông đổi bell-off + ẩn số đỏ, dải hổ phách + Bật lại, tự đồng bộ khi hết hạn. Kiểm Playwright thật (tắt → bật lại → trạng thái/biểu tượng đúng). Chưa commit.
## Phase 3 — App (TPE_APP, nhánh tpe)
- [x] 17/11/2026 — Code: `NotificationSettingsPage` mới (Chuông + Theo loại: Nhắc việc, Thông báo cơm), màn Cài đặt chỉ còn 1 dòng "Thông báo", API ext `fetch/mute/unmuteNotification`, route + `make gen`. `flutter analyze` sạch. Chọn mốc dùng `showAppPickSheet` chung (chạm là áp dụng) thay vì sheet có nút Hủy/Tắt chuông trong thiết kế N3.
- [x] 17/11/2026 — Test simulator iOS (iPhone 15 Pro, `--dart-define=APP_API_BASE_URL=http://127.0.0.1:8003/api/` = worktree gop_db-api): Cài đặt → Thông báo → Tắt chuông (mốc 08:00 sáng mai) → dòng Cài đặt tóm tắt "Đang tắt chuông đến 08:00 ngày mai" → Bật lại. Log không lỗi Flutter. Chưa test Android; chưa test push FCM thật (chỉ kiểm logic chặn ở job).
- Trạng thái: sửa ở 3 nơi, CHƯA commit/push (hrm-api worktree gop_db · hrm-client worktree gop_db · TPE_APP nhánh tpe).

## Phát hành 17/11/2026
- [x] Commit + push: hrm-api `5c386cd41` · hrm-client `51b0f6e92` (tắt chuông) + `0c8fbc614` (HDSD) trên `gop_db`; TPE_APP `02b9550` trên `tpe` (develop vốn đã nằm trong tpe → đẩy FF `tpe:develop`).
- [x] Web prod (hrm.eteksofts.com): `~/build_tpe.sh` — BE pull + migrate `notification_mutes` + route:cache + queue:restart; FE build xong, trang login 200.
- [x] App HRM TPE (tpeProd) 2.4.0 build 109: Android AAB (ký đúng SHA-1) gửi duyệt Play kênh production 100%; iOS IPA upload TestFlight thành công (Delivery a8abd752…), chờ Apple xử lý.
- [x] iOS: build 109 gán nhóm external "Tân Phát" + gửi duyệt beta (API ASC, 17/11/2026). App Store thật chưa làm: app chưa từng phát hành, bản nháp 1.0 thiếu ảnh/URL/độ tuổi — chờ user quyết.
