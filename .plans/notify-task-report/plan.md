# Plan: Notify Task Report

## Trạng thái
- Bắt đầu: 2026-03-31
- Tiến độ: 37/37 task done

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

### Phase 11: Bugfix (2026-04-09)
[x] Task 25: Fix lỗi không lưu được task_report_notify_time — thiếu trong $fillable của GeneralRegulation model
[x] Task 26: Fix UI daily-report — giảm khoảng trắng thừa khi expanded, giảm khoảng cách giữa các task

### Phase 12: Bỏ cấu hình giờ gửi — chạy mặc định 8h30→18h30 mỗi 30p (2026-04-17)
[x] Task 27: BE Migration — drop column `task_report_notify_time` khỏi `general_regulations`
[x] Task 28: BE GeneralRegulation model — bỏ `task_report_notify_time` khỏi `$fillable`
[x] Task 29: BE NotifyTaskReport command — refactor:
      - Bỏ logic match company time + fallback global
      - Check `now` ∈ [08:30, 18:30] mới gửi (gồm cả 2 mốc)
      - Logic lấy task không thay đổi (giữ skip task `progress_pct > 0`, dùng `isReportDueToday`)
[x] Task 30: BE Kernel.php — đổi schedule `everyFifteenMinutes` → `everyThirtyMinutes`
[x] Task 31: BE MyJobService — bỏ `task_report_notify_time` khỏi `getDeadlineConfig` + `saveDeadlineConfig`
[x] Task 32: FE settings/index.vue — bỏ sub-tab "Cài đặt khác" + data `otherSettings.task_report_notify_time` + `notifyTimeOptions` + `saveOtherSettings` + dòng load từ deadline-config
[x] Task 33: Cập nhật design.md + docs/notify-task-report-mobile.md — phản ánh logic mới (bỏ giờ cấu hình, chạy 8:30-18:30 mỗi 30p)

### Phase 13: Review follow-up — giảm spam + tăng an toàn (2026-04-17)
[x] Task 34: BE NotifyTaskReport — chỉ gửi đúng 4 mốc cố định: 08:30, 11:30, 14:30, 17:30 (thay vì 21 mốc/ngày)
[x] Task 35: BE Kernel — thêm `->withoutOverlapping()` cho cron `assign:notify-task-report` để tránh double-send khi instance treo
[x] Task 36: BE NotifyTaskReport — fix N+1 query: eager load `progressLogs` đã filter theo today + `progress_pct > 0` thay vì query per task
[x] Task 37: Cập nhật design.md + docs/notify-task-report-mobile.md — note thứ tự deploy (code BE+FE trước, migrate sau)

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

### Checkpoint — 2026-04-09
Vừa hoàn thành: Phase 11 — 2 bugfix: (1) task_report_notify_time thiếu $fillable trong GeneralRegulation model, (2) UI daily-report giảm khoảng trắng thừa + giảm khoảng cách giữa task + bỏ min-height table-responsive
Đang làm dở: không có
Bước tiếp theo: Dev server cần HTTPS để FCM hoạt động (Notification + ServiceWorker API yêu cầu HTTPS, trừ localhost)
Blocked: FCM push notification không hoạt động trên dev server HTTP — cần cấu hình SSL

### Checkpoint — 2026-04-17
Vừa hoàn thành: Phase 12 — 7 task. Bỏ hoàn toàn cấu hình giờ gửi per company:
- BE: migration drop `task_report_notify_time`, model GeneralRegulation bỏ $fillable, NotifyTaskReport command refactor (chỉ chạy `now ∈ [08:30, 18:30]`, bỏ logic match per company + fallback), Kernel đổi sang `everyThirtyMinutes()`, MyJobService bỏ field khỏi getDeadlineConfig/saveDeadlineConfig
- FE: bỏ sub-tab "Cài đặt khác" + data `otherSettings` + `notifyTimeOptions` + `saveOtherSettings` + dòng load `task_report_notify_time` trong loadDeadlineConfig
- Docs: cập nhật design.md + docs/notify-task-report-mobile.md
Đang làm dở: không có
Bước tiếp theo: User chạy `php artisan migrate` để drop column. Test cron `php artisan assign:notify-task-report` trong/ngoài khoảng 08:30-18:30
Blocked: không có

### Checkpoint — 2026-04-17 (Phase 13)
Vừa hoàn thành: Phase 13 — 4 task review follow-up:
- Đổi window `[08:30, 18:30]` (21 mốc/ngày) → 4 mốc cố định 08:30/11:30/14:30/17:30 để tránh spam push
- Thêm `->withoutOverlapping()` vào schedule Kernel để chống double-send khi instance treo
- Fix N+1: eager load `progressLogs` đã filter today + `progress_pct > 0` thay vì query per task
- Bổ sung mục "Deploy order" trong design.md (code BE+FE trước → `php artisan migrate` sau) + cập nhật docs mobile sang 4 mốc
Đang làm dở: không có
Bước tiếp theo:
  1. Deploy code BE + FE
  2. Chạy `php artisan migrate` (drop column `task_report_notify_time`)
  3. Test cron: `php artisan assign:notify-task-report` đúng phút 8:30/11:30/14:30/17:30 thì gửi, các phút khác trả "Không phải mốc gửi"
  4. Test fallback: chạy 1 task → kiểm tra chỉ chạy 1 instance (không overlap)
Blocked: không có
