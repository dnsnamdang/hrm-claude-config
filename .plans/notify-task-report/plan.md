# Plan: Notify Task Report

## Trạng thái
- Bắt đầu: 2026-03-31
- Tiến độ: 24/24 task done

## Danh sách task

### Phase 1: Cài đặt giờ gửi thông báo
[x] Task 1: Migration thêm task_report_notify_time vào general_regulations
[x] Task 2: BE endpoint lưu/đọc giờ cài đặt
[x] Task 3: FE settings — sub-tab "Cài đặt khác" + dropdown giờ chẵn/lẻ 30p

### Phase 2: FCM Token management
[x] Task 4: Migration tạo bảng fcm_tokens
[x] Task 5: FcmToken model + controller + routes

### Phase 3: FCM registration + Service Worker
[x] Task 6: static/firebase-messaging-sw.js
[x] Task 7: Plugin FE đăng ký FCM + xin permission (plugins/fcm-push.js)

### Phase 4: API daily report
[x] Task 8: GET /assign/tasks/daily-report
[x] Task 9: POST /assign/tasks/daily-report/save
[x] Task 10: GET /assign/tasks/daily-report/count

### Phase 5: Cron job gửi push
[x] Task 11: Artisan command assign:notify-task-report
[x] Task 12: Đăng ký trong Kernel.php (everyThirtyMinutes)

### Phase 6: Sửa canImportResult
[x] Task 13: Chỉ IN_PROGRESS mới nhập được

### Phase 7: Trang nhập tiến độ hàng loạt
[x] Task 14: daily-report.vue (UI theo demo)
[x] Task 15: Logic save + validate (tổng ≤ 100%, chỉ today editable)

### Phase 8: Notification + menu
[x] Task 16: Badge count trên sidebar menu
[x] Task 17: Menu sidebar item "Báo cáo tiến độ task"

### Phase 9: Fix FCM push notification background + click
[x] Task 18: Fix SW không nhận push khi minimize (thêm skipWaiting + clients.claim)
[x] Task 19: Fix background push — chuyển từ data-only sang notification + data + webpush config
[x] Task 20: Fix click notification không navigate — custom notificationclick trước Firebase + stopImmediatePropagation
[x] Task 21: Thêm FRONTEND_URL env cho fcm_options.link (full URL)

### Phase 10: Cập nhật logic (2026-04-03)
[x] Task 22: Fallback nhắc 2 lần lúc 08:30 và 17:30 khi không có cấu hình
[x] Task 23: Sắp xếp daily-report: ưu tiên task chưa nhập + theo send_time, thêm is_reported_today
[x] Task 24: Mặc định collapse tất cả task khi mở daily-report

## Checkpoint
- 2026-03-31: All 17 tasks done. Chờ test + cấu hình Firebase credentials
- 2026-04-01: Phase 9 done (4 task fix FCM). Push background + click navigate hoạt động đúng

### Checkpoint — 2026-04-02
Vừa hoàn thành: Commit + push code lên GitHub (BE: notify_task_report, FE: tpe-develop-assign)
Đang làm dở: không có
Bước tiếp theo: Test trên production, cần sửa FRONTEND_URL trong .env BE thành URL thật
Blocked: không có

### Checkpoint — 2026-04-03
Vừa hoàn thành: Phase 10 — cập nhật logic fallback, sắp xếp, collapse mặc định. Merge notify_task_report vào tpe-develop-assign (BE). Pushed cả BE + FE. Tạo tài liệu mobile (docs/notify-task-report-mobile.md)
Đang làm dở: không có
Bước tiếp theo: Test trên local/production. Gửi tài liệu mobile cho dev mobile
Blocked: không có
