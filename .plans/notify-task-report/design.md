# Design: Notify Task Report — Nhắc báo cáo tiến độ task

## Mục đích
Nhắc user lịch báo cáo tiến độ cho các task được giao + có yêu cầu báo cáo tiến độ theo lịch (daily/weekly/monthly). Hỗ trợ nhập tiến độ hàng loạt.

## Scope

### Làm:
- Sửa trạng thái nhập kết quả: chỉ IN_PROGRESS (4)
- Web Push Notification (FCM): nhắc user kể cả khi không mở tab
- Trang nhập tiến độ hàng loạt: /assign/tasks/daily-report
- Cài đặt giờ gửi: Settings → Quản lý dự án → Cài đặt khác

### Không làm:
- Push notification mobile (đã có FCM topic riêng)
- Email notification
- Thay đổi cấu trúc task_progress_report_rules

## Phương án kỹ thuật: FCM Web Push

### Hạ tầng có sẵn
- FE: `firebase` v7.19.1, `plugins/fireauth.js`
- BE: `kreait/laravel-firebase`, `FCMService.php`, `.env` FIREBASE_CREDENTIALS

### Thêm mới
- `static/firebase-messaging-sw.js` — Service Worker nhận push background
- `plugins/fcm-push.js` — đăng ký FCM token + xin permission
- `fcm_tokens` table — lưu token theo employee
- `assign:notify-task-report` command — cron mỗi 30p
- `task_report_notify_time` trên `general_regulations` — giờ cài đặt per company
- `FRONTEND_URL` trong `.env` BE — full URL frontend cho FCM click navigation

### Luồng
```
1. User mở app → FE xin permission → getToken() → POST /assign/fcm-tokens
2. Cron chạy mỗi 30p → check giờ cài đặt per company
3. Tìm user có task IN_PROGRESS + progressReportRule active + ngày báo cáo = today + chưa nhập
4. Gửi FCM: notification + data + webpush config (fcm_options.link = FRONTEND_URL)
5. Foreground: onMessage → toast trong app
6. Background: Firebase auto-show notification → click → custom notificationclick handler → focus + navigate tab
```

### Kỹ thuật FCM quan trọng
- BE gửi `withNotification()` + `withData()` + `withWebPushConfig()` (không chỉ data-only)
- SW đăng ký `notificationclick` TRƯỚC khi import Firebase SDK + `stopImmediatePropagation()` để chặn Firebase xử lý click (Firebase chỉ focus tab, không navigate)
- `fcm_options.link` cần full absolute URL (từ env FRONTEND_URL)
- SW cần `self.skipWaiting()` + `self.clients.claim()` để activate ngay

## Cấu trúc dữ liệu

### Bảng fcm_tokens (mới)
| Cột | Type | Mô tả |
|-----|------|-------|
| id | bigint PK | |
| employee_id | bigint | User sở hữu token |
| token | string(500) unique | FCM registration token |
| device_info | string nullable | Browser info |

### general_regulations (thêm cột)
| Cột | Type | Default | Mô tả |
|-----|------|---------|-------|
| task_report_notify_time | time nullable | 08:00:00 | Giờ gửi (chẵn/lẻ 30p) |

### Bảng có sẵn
- `task_progress_report_rules`: cycle_type (1=daily, 2=weekly, 3=monthly), send_time, week_days, month_day
- `task_result_progress_logs`: task_id, report_date, hours, progress_pct, note

## API Endpoints

| Method | Endpoint | Mục đích |
|--------|----------|----------|
| GET | /assign/tasks/daily-report | DS task cần báo cáo hôm nay + progress_rows |
| POST | /assign/tasks/daily-report/save | Lưu hàng loạt (chỉ today, validate ≤100%) |
| GET | /assign/tasks/daily-report/count | Count chưa nhập (cho badge) |
| POST | /assign/fcm-tokens | Lưu/update FCM token |
| DELETE | /assign/fcm-tokens | Xoá token (logout) |
| GET | /assign/my-job/deadline-config | Đọc cài đặt (+ task_report_notify_time) |
| POST | /assign/my-job/deadline-config | Lưu cài đặt |

## UI

### Trang daily-report.vue
- Header: breadcrumb + ngày + "Lưu tất cả"
- 3 summary cards: Tổng task | Chờ báo cáo | Đã hoàn thành
- Accordion: mỗi task expand/collapse
- Bảng progress_rows: past (readonly) | today (editable, highlight xanh) | future (disabled)
- Footer sticky: tổng giờ/8h | tiến độ TB | pending count | Đóng | Lưu tất cả

### Settings sub-tab "Cài đặt khác"
- Dropdown giờ: 06:00 → 22:00 (chẵn + lẻ 30p)

## Validate
- Tổng progress_pct per task ≤ 100%
- Chỉ editable dòng today
- canImportResult: chỉ IN_PROGRESS (4)
- Giờ cài đặt: chẵn hoặc lẻ 30p

## Cron
- Command: `assign:notify-task-report`
- Schedule: everyThirtyMinutes
- Logic: check giờ cài đặt per company → tìm user + task chưa nhập → gửi FCM push qua token
- Auto-delete token expired (NotFound exception)
