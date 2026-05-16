# SRS: Notify Task Report — Nhắc báo cáo tiến độ task

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Assign (Giao việc) |
| Phiên bản | 2.0 (Phase 12 + 13) |
| Ngày tạo | 2026-04-17 |
| Người tạo | @dnsnamdang |
| Trạng thái | Approved |

---

## 1. Giới thiệu

### 1.1. Mục đích

Hệ thống nhắc nhở nhân viên (assignee) báo cáo tiến độ các task đang thực hiện thông qua **Web Push Notification (FCM)**, đồng thời cung cấp **trang nhập tiến độ hàng loạt** giúp user xử lý nhanh nhiều task cùng lúc trong ngày.

Đặc điểm:
- Nhắc tự động qua trình duyệt (kể cả khi không mở tab) tại **4 mốc cố định** trong ngày: 08:30, 11:30, 14:30, 17:30
- Áp dụng đồng nhất cho toàn hệ thống — không cần cấu hình per company
- Chỉ nhắc các task đang `IN_PROGRESS` có rule báo cáo định kỳ active và đến lịch hôm nay nhưng user **chưa nhập** tiến độ

### 1.2. Phạm vi

**Trong scope:**
- Đăng ký nhận push notification trên trình duyệt (FCM)
- Cron tự động phát hiện task chưa báo cáo và gửi push
- Trang nhập báo cáo tiến độ hàng loạt: `/assign/tasks/daily-report`
- Badge count trên sidebar menu hiển thị số task chưa nhập
- Click notification → tự navigate đến trang nhập

**Ngoài scope:**
- Push notification mobile (đã có FCM topic riêng cho ứng dụng mobile)
- Email notification
- Cấu hình giờ nhắc per company / per user
- Thay đổi cấu trúc `task_progress_report_rules`

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| FCM | Firebase Cloud Messaging — dịch vụ push notification của Google |
| Service Worker (SW) | Script chạy nền trong trình duyệt để nhận push khi tab đóng |
| Assignee | Nhân viên được giao thực hiện task |
| Progress Report Rule | Quy tắc báo cáo định kỳ của task (daily/weekly/monthly) |
| Progress Log | Bản ghi tiến độ task theo từng ngày báo cáo |
| Cycle Type | Chu kỳ báo cáo: 1=daily, 2=weekly, 3=monthly |

---

## 2. Actors & Permissions

| Actor | Mô tả | Quyền |
|-------|-------|-------|
| Nhân viên (Assignee) | Người được giao thực hiện task | Xem + nhập tiến độ task của bản thân; nhận push notification |
| Hệ thống (Cron) | Job tự động chạy mỗi 30 phút | Truy vấn task + gửi push qua FCM |
| FCM Service | Dịch vụ Google đẩy push tới browser | Nhận message từ BE và đẩy đến SW |
| Service Worker | Chạy nền trong browser của user | Hiển thị notification + xử lý click navigate |

Auth: Tất cả endpoint yêu cầu **Bearer JWT Token**.

---

## 3. Use Cases

### UC-01: Đăng ký nhận push notification (FCM Token)

| | |
|---|---|
| **Actor** | Nhân viên |
| **Precondition** | User đã login; trình duyệt hỗ trợ Notification + Service Worker (HTTPS bắt buộc, trừ localhost) |
| **Main Flow** | |
| 1 | User mở app web sau khi login |
| 2 | FE plugin `fcm-push.js` đăng ký Service Worker `firebase-messaging-sw.js` |
| 3 | FE gọi `Notification.requestPermission()` → user click "Cho phép" |
| 4 | FE gọi `firebase.messaging().getToken()` → nhận `fcm_token` |
| 5 | FE gửi `POST /assign/fcm-tokens` với `{ token, device_info }` |
| 6 | BE `updateOrCreate` token vào bảng `fcm_tokens` (key: `token`) |
| 7 | BE trả 200 success |
| **Postcondition** | Token được gắn với `employee_id` của user → cron có thể gửi push |
| **Alternative Flow** | User từ chối permission → không gửi token, không nhận push (FE silent skip) |
| **Exception** | Token đã tồn tại (do cùng device/login lại) → BE update `employee_id` mới (upsert) |

### UC-02: Hệ thống tự động gửi push notification (Cron)

| | |
|---|---|
| **Actor** | Hệ thống (Cron) |
| **Precondition** | `php artisan schedule:run` được system cron gọi mỗi phút; FCM credentials đã cấu hình trong `.env` (FIREBASE_CREDENTIALS) |
| **Main Flow** | |
| 1 | Schedule trigger `assign:notify-task-report` mỗi 30 phút |
| 2 | Command kiểm tra `now()` có thuộc 1 trong 4 mốc {08:30, 11:30, 14:30, 17:30} không. Nếu không → return 0 |
| 3 | Query: tất cả Task `status=IN_PROGRESS` có `progressReportRule.is_active=true`; eager load `progressLogs` đã filter `report_date=today + progress_pct>0` |
| 4 | Filter task **due today** theo `cycle_type`:<br/>- DAILY: luôn true<br/>- WEEKLY: `today.dayOfWeek IN week_days`<br/>- MONTHLY: `today.day == month_day` |
| 5 | Skip task có `progressLogs.isNotEmpty()` (đã nhập hôm nay) |
| 6 | Group còn lại theo `assignee_id` → đếm số task per user |
| 7 | Với mỗi user: lấy tất cả `fcm_tokens.token`; với mỗi token gửi message FCM gồm: `notification(title, body)` + `data(click_action, task_count)` + `webpush(notification.tag, fcm_options.link=FRONTEND_URL/assign/tasks/daily-report)` |
| 8 | Nếu FCM trả `NotFound` → xoá token khỏi bảng `fcm_tokens` |
| 9 | Log `Sent: X, Failed: Y, Users: Z` |
| **Postcondition** | User chưa nhập tiến độ nhận được push notification trên browser |
| **Alternative Flow** | Không có user nào cần nhắc → log "Không có user nào cần nhắc báo cáo" |
| **Exception** | Firebase messaging không khả dụng → log error, return 1; cron `withoutOverlapping()` đảm bảo không double-send khi instance treo |

### UC-03: User nhận và click vào notification

| | |
|---|---|
| **Actor** | Nhân viên |
| **Precondition** | UC-01 đã thành công, UC-02 đã gửi push |
| **Main Flow** | |
| 1 | FCM đẩy message tới browser của user |
| 2 | **Foreground (tab đang mở)**: `onMessage` handler hiển thị toast trong app |
| 3 | **Background (tab đóng/minimize)**: SW `firebase-messaging-sw.js` nhận push, browser hiển thị system notification (icon, title, body) |
| 4 | User click notification |
| 5 | SW custom `notificationclick` handler chạy **trước** Firebase default + `stopImmediatePropagation()` |
| 6 | SW dùng `clients.openWindow(fcm_options.link)` hoặc focus tab existing → navigate đến `/assign/tasks/daily-report` |
| **Postcondition** | User được đưa đến trang nhập báo cáo tiến độ |
| **Exception** | Token đã expired → BE auto-delete ở UC-02 step 8, lần sau không gửi nữa |

### UC-04: Xem danh sách task cần báo cáo hôm nay

| | |
|---|---|
| **Actor** | Nhân viên |
| **Precondition** | User đã login; truy cập `/assign/tasks/daily-report` |
| **Main Flow** | |
| 1 | FE gọi `GET /assign/tasks/daily-report` |
| 2 | BE lấy task của `auth()->id()` có `status=IN_PROGRESS` + rule active |
| 3 | BE filter task **due today** (DAILY/WEEKLY/MONTHLY) |
| 4 | Với mỗi task, BE generate `progress_rows`: lịch các ngày cần báo cáo (past + today + future), gắn log đã có nếu tồn tại |
| 5 | Set flag `is_reported_today` = `true` nếu hôm nay đã có log với `progress_pct > 0` |
| 6 | Sắp xếp: chưa nhập lên trước, sau đó theo `report_rule.send_time` tăng dần |
| 7 | FE render: 3 summary card (Tổng/Chờ báo cáo/Đã hoàn thành), accordion task (collapse mặc định), bảng `progress_rows` per task |
| **Postcondition** | User thấy danh sách task + có thể nhập tiến độ |
| **Alternative Flow** | Không có task nào → hiển thị empty state "Không có task cần báo cáo tiến độ hôm nay" |

### UC-05: Nhập và lưu báo cáo tiến độ hàng loạt

| | |
|---|---|
| **Actor** | Nhân viên |
| **Precondition** | UC-04 đã load được task; user có quyền nhập (chỉ task `IN_PROGRESS` của bản thân) |
| **Main Flow** | |
| 1 | User expand task → bảng `progress_rows` hiện ra |
| 2 | Chỉ dòng `is_today=true` cho phép edit (hours/progress_pct/note); past readonly; future disabled |
| 3 | User nhập số giờ, % tiến độ, ghi chú cho ≥ 1 task |
| 4 | Click "Lưu tất cả" |
| 5 | FE validate client: với mỗi task → tổng `progress_pct` past + today **≤ 100%**; nếu vượt → highlight đỏ + toast lỗi, dừng |
| 6 | FE build payload `{ tasks: [{task_id, progress_logs: [today]}] }`, chỉ gửi task có dòng today có dữ liệu |
| 7 | FE gọi `POST /assign/tasks/daily-report/save` |
| 8 | BE validate lại tổng ≤ 100% (server-side); chỉ chấp nhận `report_date == today` |
| 9 | BE `updateOrCreate` `task_result_progress_logs` (key: `task_id + report_date`) |
| 10 | BE sync `task.progress_pct = log mới nhất theo report_date` |
| 11 | BE trả `{ success: N, errors: [...] }` |
| 12 | FE toast success + reload data |
| **Postcondition** | Tiến độ task được lưu; user không nhận push lần kế (do `progress_pct > 0`) |
| **Alternative Flow** | User chỉ nhập 1 vài task → chỉ task có dữ liệu được gửi |
| **Exception** | Tổng vượt 100% → BE skip task đó, ghi vào `errors`, các task khác vẫn lưu |

### UC-06: Xem badge count trên sidebar

| | |
|---|---|
| **Actor** | Nhân viên |
| **Precondition** | Sidebar menu có item "Báo cáo tiến độ task" |
| **Main Flow** | |
| 1 | FE gọi `GET /assign/tasks/daily-report/count` (định kỳ hoặc on-mount) |
| 2 | BE đếm task `IN_PROGRESS` của user, due today, chưa có log `progress_pct > 0` |
| 3 | BE trả `{ count: N }` |
| 4 | FE hiển thị badge số `N` cạnh menu item; nếu N=0 không hiển thị |
| **Postcondition** | User biết còn bao nhiêu task chưa báo cáo |

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | Cửa sổ gửi push | Cron chỉ gửi tại 4 mốc cố định: 08:30, 11:30, 14:30, 17:30 (so sánh exact `now.hour*60 + now.minute`) | UC-02 / `NotifyTaskReport::handle()` |
| BR-02 | Chỉ task IN_PROGRESS | Chỉ task có `status = 4 (IN_PROGRESS)` mới được tính + cho phép nhập | UC-02, UC-04, UC-05 / `Task::canImportResult()` |
| BR-03 | Skip task đã nhập | Task có log `report_date=today AND progress_pct > 0` được coi là đã nhập → không nhắc lại trong các mốc kế | UC-02, UC-04, UC-06 |
| BR-04 | Tổng tiến độ ≤ 100% | Sum `progress_pct` các log của 1 task không vượt 100%; vượt → reject ở cả FE và BE | UC-05 / `TaskService::saveDailyReport()` |
| BR-05 | Chỉ today editable | Chỉ dòng `report_date = today` được edit; past readonly; future disabled | UC-04, UC-05 |
| BR-06 | Cycle weekly | Task weekly chỉ due nếu `today.dayOfWeek ∈ rule.week_days` (Carbon convention 0=Sunday…6=Saturday) | UC-02, UC-04 / `isReportDueToday()` |
| BR-07 | Cycle monthly | Task monthly chỉ due nếu `today.day == rule.month_day` | UC-02, UC-04 / `isReportDueToday()` |
| BR-08 | Auto-delete token expired | FCM trả `NotFound` → xoá token khỏi `fcm_tokens` để không retry | UC-02 |
| BR-09 | Cron không chạy chồng | `withoutOverlapping()` đảm bảo 1 instance tại 1 thời điểm | UC-02 / Kernel.php |
| BR-10 | FRONTEND_URL bắt buộc | `fcm_options.link` cần URL tuyệt đối — đọc từ `env('FRONTEND_URL')` | UC-02, UC-03 |
| BR-11 | Sync task progress | Sau khi lưu log → `task.progress_pct = log.progress_pct` của log có `report_date` lớn nhất | UC-05 |
| BR-12 | Permission ownership | Endpoint daily-report chỉ trả task của `auth()->id()`; save chỉ chấp nhận task có `assignee_id = auth()->id()` | UC-04, UC-05, UC-06 |

---

## 5. Data Model

### 5.1. Entity Relationship Diagram

```
employees 1 ──N fcm_tokens
employees 1 ──N tasks (assignee_id)
tasks     1 ──1 task_progress_report_rules
tasks     1 ──N task_result_progress_logs (qua task_result_id)
```

### 5.2. Bảng dữ liệu

#### Bảng: `fcm_tokens`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| employee_id | unsignedBigInteger | No | — | ID nhân viên (index) |
| token | string(500) UNIQUE | No | — | FCM registration token |
| device_info | string(255) | Yes | null | User-Agent / browser info |
| created_at | timestamp | Yes | null | |
| updated_at | timestamp | Yes | null | |

#### Bảng: `task_progress_report_rules`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| task_id | unsignedBigInteger UNIQUE | No | — | 1-1 với Task |
| cycle_type | tinyInteger | No | 1 | 1=daily, 2=weekly, 3=monthly |
| send_time | time | No | — | Giờ yêu cầu báo cáo (dùng để sort UI) |
| week_days | string(50) | Yes | null | CSV thứ trong tuần (vd "1,3,5") khi weekly |
| month_day | unsignedTinyInteger | Yes | null | Ngày trong tháng (1-31) khi monthly |
| next_send_at | dateTime | Yes | null | (Reserved) |
| is_active | tinyInteger | No | 1 | 1=active, 0=tắt |
| created_by | unsignedBigInteger | Yes | null | |
| created_at / updated_at | timestamps | | | |

#### Bảng: `task_result_progress_logs`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| task_result_id | unsignedBigInteger | No | — | FK đến task / task_result (index) |
| report_date | date | No | — | Ngày báo cáo (index) |
| hours | decimal(8,2) | Yes | null | Số giờ làm trong kỳ |
| progress_pct | unsignedTinyInteger | No | 0 | Tiến độ % (0-100) |
| note | text | Yes | null | Ghi chú |
| created_at / updated_at | timestamps | | | |

#### Bảng: `general_regulations` (lưu ý Phase 12)

> Cột `task_report_notify_time` đã bị **drop** trong migration `2026_04_17_100003`. Không còn cấu hình giờ per company — áp dụng đồng nhất 4 mốc cố định.

### 5.3. Enum Values

| Entity | Constant | Value | Meaning |
|--------|----------|-------|---------|
| Task | DRAFT | 1 | Nháp |
| Task | PENDING_APPROVAL | 2 | Chờ phê duyệt triển khai |
| Task | TODO | 3 | Chờ bắt đầu |
| Task | **IN_PROGRESS** | **4** | **Đang thực hiện (điều kiện để được nhắc + nhập)** |
| Task | PAUSED | 5 | Tạm dừng |
| Task | REVIEW | 6 | Hoàn thành - Chờ duyệt |
| Task | REJECTED | 7 | Từ chối kết quả |
| Task | DONE | 8 | Hoàn thành |
| Task | CANCELLED | 9 | Huỷ |
| Task | REJECTED_START | 10 | Từ chối triển khai |
| TaskProgressReportRule | CYCLE_DAILY | 1 | Báo cáo hàng ngày |
| TaskProgressReportRule | CYCLE_WEEKLY | 2 | Báo cáo theo tuần |
| TaskProgressReportRule | CYCLE_MONTHLY | 3 | Báo cáo theo tháng |

---

## 6. API Specification

Tất cả endpoint đều yêu cầu auth Bearer JWT.

### 6.1. POST `/api/v1/assign/fcm-tokens`

Đăng ký / cập nhật FCM token cho user hiện tại (upsert by token).

**Request:**

| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| token | string | Yes | non-empty | FCM registration token |
| device_info | string | No | — | Browser info (mặc định lấy User-Agent header) |

**Response 200:** `{ "message": "success", "status": 200 }`

**Error:** 400 nếu thiếu `token`.

### 6.2. DELETE `/api/v1/assign/fcm-tokens`

Xoá FCM token (gọi khi logout).

**Request:** `{ "token": "<fcm_token>" }`

**Response 200:** `{ "message": "success", "status": 200 }`

### 6.3. GET `/api/v1/assign/tasks/daily-report`

Lấy danh sách task của user, due today, kèm `progress_rows`.

**Response 200:**
```json
{
  "message": "success",
  "status": 200,
  "data": [
    {
      "id": 123,
      "title": "...",
      "status_name": "Đang thực hiện",
      "status_color": "#2563eb",
      "priority": 2,
      "project_name": "...",
      "due_date": "2026-04-30",
      "due_time": "17:00",
      "is_reported_today": false,
      "report_rule": {"cycle_type": 1, "send_time": "17:00"},
      "progress_rows": [
        {"report_date": "2026-04-15", "hours": 8, "progress_pct": 30, "note": "...", "is_today": false, "is_past": true, "is_future": false},
        {"report_date": "2026-04-17", "hours": null, "progress_pct": null, "note": null, "is_today": true, "is_past": false, "is_future": false},
        {"report_date": "2026-04-18", "hours": null, "progress_pct": null, "note": null, "is_today": false, "is_past": false, "is_future": true}
      ]
    }
  ]
}
```

**Sort**: chưa nhập lên trước; sau đó theo `report_rule.send_time` tăng dần.

### 6.4. POST `/api/v1/assign/tasks/daily-report/save`

Lưu hàng loạt log tiến độ — chỉ chấp nhận dòng today.

**Request:**
```json
{
  "tasks": [
    {
      "task_id": 123,
      "progress_logs": [
        {"report_date": "2026-04-17", "hours": 4, "progress_pct": 50, "note": "..."}
      ]
    }
  ]
}
```

**Validate (BE):**
- `task_id` phải là task của `auth()->id()`
- `report_date` phải = today, dòng khác bị skip silent
- Sum `progress_pct` (loại trừ today) + `progress_pct` mới ≤ 100% — vượt thì task đó bị skip + thêm vào `errors`

**Response 200:**
```json
{ "message": "Lưu tiến độ thành công", "status": 200, "data": { "success": 2, "errors": [] } }
```

**Error 400:** payload rỗng / `tasks` không phải array.

### 6.5. GET `/api/v1/assign/tasks/daily-report/count`

Đếm task chưa nhập (cho badge sidebar).

**Response 200:** `{ "message": "success", "status": 200, "data": { "count": 3 } }`

---

## 7. UI Specification

### 7.1. Trang `/assign/tasks/daily-report`

- **Layout**: `default-sidebar`
- **Mixin**: `PageTitleMixin` đẩy title "Nhập kết quả báo cáo tiến độ" lên topbar
- **Components**: `V2BaseButton`, `V2BaseBadge`

**Wireframe:**
```
┌──────────────────────────────────────────────────────────────┐
│ Trang chủ / Công việc / Nhập kết quả báo cáo tiến độ        │
│                                       📅 17/04/2026 [Lưu tất cả] │
├──────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                      │
│ │Tổng task │ │Chờ b.cáo │ │ Đã h.thành│                     │
│ │  N        │ │  N        │ │  N / Total │                  │
│ └──────────┘ └──────────┘ └──────────┘                      │
├──────────────────────────────────────────────────────────────┤
│ ▶ [1] Task A                  [Đang thực hiện] [Trung bình] │
│ ▶ [2] Task B                  [Đang thực hiện] [Cao]        │
│ ▼ [3] Task C                  [Đang thực hiện] [Thấp]       │
│   ┌─Hồ sơ task: Project, Hạn, Giờ hạn─────────────────────┐ │
│   │ Nhật ký tiến độ theo ngày                             │ │
│   │ ┌──────────────┬────────┬─────────┬────────────────┐ │ │
│   │ │ NGÀY B.CÁO   │ SỐ GIỜ │ TIẾN ĐỘ │ GHI CHÚ        │ │ │
│   │ │ 15/04 (past) │  8h    │  30%    │ ...            │ │ │
│   │ │ 17/04 today  │ [_]    │ [_]%    │ [____________] │ │ │ ← editable
│   │ │ 18/04 future │  —     │   —     │ Chưa đến ngày  │ │ │
│   │ └──────────────┴────────┴─────────┴────────────────┘ │ │
│   └────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│ Footer sticky: Tổng giờ: Xh/8h | TB: Y% | Z chưa nhập       │
│                                       [Đóng] [Lưu tất cả]   │
└──────────────────────────────────────────────────────────────┘
```

**Interactions:**

| Action | Behavior | API |
|--------|----------|-----|
| Mount page | Load data, accordion collapse mặc định | `GET /daily-report` |
| Click task header | Toggle expand / collapse | (client) |
| Edit dòng today | Cập nhật `hours`, `progress_pct`, `note` | (client) |
| Click "Lưu tất cả" | Validate + POST batch | `POST /daily-report/save` |
| Click "Đóng" | Quay về `/assign/tasks` | (router) |

**Validation client:**
- Tổng past + today ≤ 100% per task; vi phạm → highlight error message bên dưới task + toast, không gửi
- `hours`: 0-24, step 0.5
- `progress_pct`: 0-100

### 7.2. Sidebar menu — Badge count

- Item "Báo cáo tiến độ task" hiển thị badge số task chưa nhập
- Refresh badge: on-mount + (tuỳ FE) định kỳ

### 7.3. Plugin FCM — `plugins/fcm-push.js`

- Đăng ký `firebase-messaging-sw.js` từ `/static/`
- Xin permission Notification (silent skip nếu denied)
- Lấy token, gửi `POST /assign/fcm-tokens`
- Đăng ký `onMessage` để hiển thị toast khi foreground

### 7.4. Service Worker — `static/firebase-messaging-sw.js`

- `self.skipWaiting()` + `self.clients.claim()` để activate ngay khi update
- Đăng ký `notificationclick` handler **trước** khi import Firebase SDK + `event.stopImmediatePropagation()` để chặn Firebase default
- Click → `clients.openWindow(fcm_options.link)` hoặc focus tab existing rồi `postMessage` để FE navigate

---

## 8. Scheduled Jobs

| Command | Schedule | File | Logic |
|---------|----------|------|-------|
| `assign:notify-task-report` | `everyThirtyMinutes()->withoutOverlapping()` | `app/Console/Commands/NotifyTaskReport.php` | Gate 4 mốc cố định 08:30/11:30/14:30/17:30 → query task → push FCM |

Chi tiết flow xem UC-02 + Mục 9 (Swimlane).

---

## 9. Swimlane Diagrams

### 9.1. Swimlane — Đăng ký FCM Token (UC-01)

| Bước | User | FE Plugin (`fcm-push.js`) | Service Worker | BE FcmTokenController | DB `fcm_tokens` |
|------|------|---------------------------|----------------|----------------------|-----------------|
| 1 | Login + mở app | | | | |
| 2 | | Đăng ký SW `firebase-messaging-sw.js` | Active (skipWaiting + claim) | | |
| 3 | | `Notification.requestPermission()` | | | |
| 4 | Click "Cho phép" | Nhận `granted` | | | |
| 5 | | `messaging.getToken()` → fcm_token | | | |
| 6 | | `POST /assign/fcm-tokens {token, device_info}` | | Nhận request | |
| 7 | | | | `auth()->id()` | |
| 8 | | | | `updateOrCreate(['token'], [employee_id, device_info])` | INSERT/UPDATE |
| 9 | | Nhận 200 success | | Trả `{message:"success"}` | |

### 9.2. Swimlane — Cron gửi Push Notification (UC-02 + UC-03)

| Bước | System Cron | NotifyTaskReport Command | DB | FCM Service | Service Worker | User |
|------|-------------|--------------------------|-----|-------------|----------------|------|
| 1 | Trigger `schedule:run` mỗi phút | | | | | |
| 2 | | Laravel scheduler check `everyThirtyMinutes()` → chạy command tại phút 0/30 | | | | |
| 3 | | Check `now.hour*60 + now.minute ∈ {510,690,870,1050}`? Không → return 0 | | | | |
| 4 | | Query Task + eager load progressReportRule + progressLogs(today, pct>0) | SELECT | | | |
| 5 | | Loop: `isReportDueToday()` + skip nếu `progressLogs.isNotEmpty()` | | | | |
| 6 | | Group `[employee_id => count]` | | | | |
| 7 | | Query `fcm_tokens` per employee | SELECT | | | |
| 8 | | Build `CloudMessage::withTarget+Notification+Data+WebPushConfig(fcm_options.link)` | | | | |
| 9 | | `messaging->send($message)` | | Nhận và đẩy push tới browser | | |
| 10 | | | | | **Background**: SW nhận → browser hiện system notification | Thấy notification |
| 11 | | | | | **Foreground**: `onMessage` → toast trong app | Thấy toast |
| 12 | | NotFound exception → `FcmToken::delete($token)` | DELETE | | | |
| 13 | | Log `Sent: X, Failed: Y` | | | | |
| 14 | | | | | Click notification → `notificationclick` chạy trước Firebase + stopImmediatePropagation | Click |
| 15 | | | | | `clients.openWindow(fcm_options.link)` hoặc focus tab | Đến /assign/tasks/daily-report |

### 9.3. Swimlane — Nhập báo cáo tiến độ hàng loạt (UC-04 + UC-05)

| Bước | User | FE `daily-report.vue` | BE TaskController | TaskService | DB |
|------|------|----------------------|-------------------|-------------|-----|
| 1 | Truy cập `/assign/tasks/daily-report` | | | | |
| 2 | | `mounted()` → `GET /assign/tasks/daily-report` | `dailyReport()` | `getDailyReportTasks()` | |
| 3 | | | | Query Task + filter due today + flag `is_reported_today` | SELECT |
| 4 | | | | Sort: chưa nhập trước, theo `send_time` | |
| 5 | | | Trả `data: [tasks with progress_rows]` | | |
| 6 | | Render summary cards + accordion (collapse) | | | |
| 7 | Click expand task | Toggle `_expanded` | | | |
| 8 | Nhập hours/progress_pct/note dòng today | v-model update | | | |
| 9 | Click "Lưu tất cả" | Validate client: sum past+today ≤ 100% | | | |
| 10 | | Nếu vi phạm → toast error + dừng | | | |
| 11 | | Build payload `{tasks: [{task_id, progress_logs:[today]}]}` | | | |
| 12 | | `POST /assign/tasks/daily-report/save` | `saveDailyReport()` | `saveDailyReport($tasks)` | |
| 13 | | | | Loop tasks: validate ownership + report_date=today + sum ≤ 100% | |
| 14 | | | | `TaskResultProgressLog::updateOrCreate(['task_id','report_date'], [hours, pct, note])` | INSERT/UPDATE |
| 15 | | | | Sync `task.progress_pct = latestLog.progress_pct` | UPDATE tasks |
| 16 | | | Trả `{success:N, errors:[]}` | | |
| 17 | | Toast success + reload data | | | |

---

## 10. Non-functional Requirements

- **Performance**:
  - Eager load `progressLogs` (filtered today + pct>0) trong cron để tránh N+1
  - Cron `withoutOverlapping()` chống chạy chồng instance khi DB chậm
  - Window check (4 mốc) đặt **trước** query DB → ngoài giờ không tốn DB call
- **Security**:
  - Mọi endpoint yêu cầu Bearer JWT
  - `daily-report` + `save` chỉ trả/chấp nhận task của `auth()->id()`
  - FCM credentials lưu trong `.env` (`FIREBASE_CREDENTIALS`)
- **Compatibility**: PHP 7.4 / Laravel 8 / MySQL / Nuxt 2.14 / Vue 2 / Bootstrap 4
- **Browser**: Chrome / Firefox / Edge (Safari hạn chế hỗ trợ Web Push). HTTPS bắt buộc cho Notification + Service Worker (trừ localhost)
- **Reliability**: Token expired (FCM `NotFound`) auto-cleanup → tránh retry vô hạn

---

## 11. Deploy & Cấu hình

### 11.1. Biến môi trường

| Key | Required | Mô tả |
|-----|----------|-------|
| `FIREBASE_CREDENTIALS` | Yes | Path tới Firebase service account JSON (BE) |
| `FRONTEND_URL` | Yes | URL tuyệt đối của FE (vd `https://erp.tpe.vn`) — dùng cho `fcm_options.link` |

### 11.2. Thứ tự deploy

1. Deploy code BE + FE (đã không còn reference `task_report_notify_time`)
2. Sau đó chạy `php artisan migrate` để drop column trên `general_regulations`
3. Restart queue / scheduler nếu cần

> **Cảnh báo**: Nếu chạy migrate trước khi deploy code, code cũ sẽ fatal vì query `whereNotNull('task_report_notify_time')` trên column không tồn tại.

### 11.3. Test

| Test case | Cách làm | Expected |
|-----------|----------|----------|
| Cron đúng mốc | `php artisan assign:notify-task-report` lúc 8:30 | Gửi push, log "Sent: X" |
| Cron sai mốc | Chạy lúc 9:00 / 12:00 / etc | Log "Không phải mốc gửi" và return 0 |
| Lưu vượt 100% | Nhập task có sum > 100% | BE skip task đó, errors có entry |
| Token expired | Token đã revoke trên Firebase | BE auto-delete row trong `fcm_tokens` |
| Click notification | Tap push notification trên browser | Mở/focus tab `/assign/tasks/daily-report` |

---

## 12. Phụ lục — File References

### Backend (`hrm-api`)

| Layer | File path |
|-------|-----------|
| Migration `fcm_tokens` | `database/migrations/2026_03_31_110000_create_fcm_tokens_table.php` |
| Migration `task_progress_report_rules` | `database/migrations/2026_02_07_092420_create_task_progress_report_rules_table.php` |
| Migration `task_result_progress_logs` | `database/migrations/2026_02_28_100001_create_task_result_progress_logs_table.php` |
| Migration drop column | `database/migrations/2026_04_17_100003_drop_task_report_notify_time_from_general_regulations_table.php` |
| Entity `FcmToken` | `Modules/Assign/Entities/FcmToken.php` |
| Entity `Task` (constants) | `Modules/Assign/Entities/Task/Task.php:70-132` |
| Entity `TaskProgressReportRule` | `Modules/Assign/Entities/Task/TaskProgressReportRule.php:38-40` |
| Cron command | `app/Console/Commands/NotifyTaskReport.php` |
| Schedule | `app/Console/Kernel.php:52-55` |
| Controller FCM | `Modules/Assign/Http/Controllers/Api/V1/FcmTokenController.php` |
| Controller daily-report | `Modules/Assign/Http/Controllers/Api/V1/TaskController.php:237-278` |
| Service daily-report | `Modules/Assign/Services/TaskService.php:760-924` |
| Routes | `Modules/Assign/Routes/api.php:499-509` |

### Frontend (`hrm-client`)

| Layer | File path |
|-------|-----------|
| Trang nhập tiến độ | `pages/assign/tasks/daily-report.vue` |
| Plugin FCM | `plugins/fcm-push.js` |
| Service Worker | `static/firebase-messaging-sw.js` |
| Sidebar menu | `components/menu-sidebar.js` |

### Plans

| File | Mục đích |
|------|---------|
| `.plans/notify-task-report/design.md` | Design quyết định kiến trúc |
| `.plans/notify-task-report/plan.md` | Danh sách 37 task (Phase 1-13) |
| `docs/notify-task-report-mobile.md` | Tài liệu cho dev mobile (FCM payload format) |
