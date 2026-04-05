# Tài liệu triển khai Mobile: Nhắc báo cáo tiến độ task

## 1. Tổng quan

Tính năng nhắc nhở user báo cáo tiến độ cho các task đang thực hiện (IN_PROGRESS) có yêu cầu báo cáo định kỳ (daily/weekly/monthly). Hệ thống gửi push notification qua **Firebase Cloud Messaging (FCM)** và cung cấp màn hình nhập tiến độ hàng loạt.

### Luồng hoạt động

```
1. User login → App đăng ký FCM token → POST /assign/fcm-tokens
2. Cron BE chạy mỗi 30 phút → check giờ cài đặt per company
3. Tìm user có task IN_PROGRESS + rule báo cáo active + ngày hôm nay match schedule + chưa nhập
4. Gửi FCM push notification tới các token đã lưu
5. User nhận notification → tap → mở màn nhập tiến độ
6. User nhập tiến độ → POST /assign/tasks/daily-report/save
7. User logout → DELETE /assign/fcm-tokens (xóa token)
```

---

## 2. API Endpoints

**Base URL:** `/api/v1`
**Auth:** Bearer token (JWT) trong header `Authorization`

---

### 2.1. Đăng ký FCM Token

Gọi sau khi login thành công + lấy được FCM token từ Firebase SDK.

```
POST /api/v1/assign/fcm-tokens
```

**Request body:**
```json
{
  "token": "fMx7v2...(FCM registration token)",
  "device_info": "iPhone 15 Pro / Android 14 - Samsung S24"
}
```

- `token` (string, **bắt buộc**): FCM registration token
- `device_info` (string, optional): Thông tin thiết bị. Nếu không gửi, BE tự lấy từ User-Agent header

**Response (200):**
```json
{
  "message": "success",
  "status": 200
}
```

**Logic BE:** Upsert theo `token` — nếu token đã tồn tại thì update `employee_id`, nếu chưa thì tạo mới.

---

### 2.2. Xóa FCM Token (Logout)

Gọi **trước khi logout** để ngừng nhận notification.

```
DELETE /api/v1/assign/fcm-tokens
```

**Request body:**
```json
{
  "token": "fMx7v2...(FCM registration token đã lưu)"
}
```

**Response (200):**
```json
{
  "message": "success",
  "status": 200
}
```

---

### 2.3. Lấy danh sách task cần báo cáo hôm nay

```
GET /api/v1/assign/tasks/daily-report
```

**Response (200):**
```json
{
  "message": "success",
  "status": 200,
  "data": [
    {
      "id": 123,
      "code": "TASK-001",
      "title": "Thiết kế UI màn login",
      "status": 4,
      "status_name": "Đang thực hiện",
      "status_color": "#2196F3",
      "priority": 2,
      "due_date": "2026-04-10",
      "due_time": "17:00:00",
      "start_date": "2026-04-01",
      "progress_pct": 30,
      "total_progress_pct": 45,
      "project_name": "Dự án ABC",
      "assignee_name": "Nguyễn Văn A",
      "report_rule": {
        "cycle_type": 1,
        "send_time": "08:00:00"
      },
      "progress_rows": [
        {
          "report_date": "2026-04-01",
          "hours": 6,
          "progress_pct": 15,
          "note": "Hoàn thành wireframe",
          "is_today": false,
          "is_past": true,
          "is_future": false,
          "is_editable": false
        },
        {
          "report_date": "2026-04-02",
          "hours": 8,
          "progress_pct": 30,
          "note": "Hoàn thành mockup",
          "is_today": false,
          "is_past": true,
          "is_future": false,
          "is_editable": false
        },
        {
          "report_date": "2026-04-03",
          "hours": null,
          "progress_pct": null,
          "note": null,
          "is_today": true,
          "is_past": false,
          "is_future": false,
          "is_editable": true
        },
        {
          "report_date": "2026-04-04",
          "hours": null,
          "progress_pct": null,
          "note": null,
          "is_today": false,
          "is_past": false,
          "is_future": true,
          "is_editable": false
        }
      ]
    }
  ]
}
```

**Giải thích các trường:**

| Trường | Type | Mô tả |
|--------|------|--------|
| `id` | int | ID task |
| `code` | string | Mã task |
| `title` | string | Tên task |
| `status` | int | Trạng thái (4 = IN_PROGRESS) |
| `status_name` | string | Tên trạng thái hiển thị |
| `status_color` | string | Mã màu hex |
| `priority` | int | Mức ưu tiên |
| `due_date` | string | Ngày hạn (YYYY-MM-DD) |
| `due_time` | string | Giờ hạn (HH:mm:ss) |
| `start_date` | string | Ngày bắt đầu (YYYY-MM-DD) |
| `progress_pct` | int | Tiến độ hiện tại của task (%) |
| `total_progress_pct` | int | Tổng % đã báo cáo qua tất cả các ngày |
| `project_name` | string\|null | Tên dự án |
| `assignee_name` | string\|null | Tên người được giao |
| `report_rule.cycle_type` | int | 1=Hàng ngày, 2=Hàng tuần, 3=Hàng tháng |
| `report_rule.send_time` | string | Giờ gửi nhắc (HH:mm:ss) |

**Giải thích `progress_rows`:**

| Trường | Type | Mô tả |
|--------|------|--------|
| `report_date` | string | Ngày báo cáo (YYYY-MM-DD) |
| `hours` | float\|null | Số giờ làm việc |
| `progress_pct` | int\|null | % tiến độ ngày đó |
| `note` | string\|null | Ghi chú |
| `is_today` | bool | Có phải hôm nay không |
| `is_past` | bool | Ngày quá khứ |
| `is_future` | bool | Ngày tương lai |
| `is_editable` | bool | Cho phép sửa (chỉ `true` khi `is_today = true`) |

---

### 2.4. Lưu báo cáo tiến độ

```
POST /api/v1/assign/tasks/daily-report/save
```

**Request body:**
```json
{
  "tasks": [
    {
      "task_id": 123,
      "progress_logs": [
        {
          "report_date": "2026-04-03",
          "hours": 6.5,
          "progress_pct": 20,
          "note": "Hoàn thành phần header"
        }
      ]
    },
    {
      "task_id": 456,
      "progress_logs": [
        {
          "report_date": "2026-04-03",
          "hours": 3,
          "progress_pct": 10,
          "note": ""
        }
      ]
    }
  ]
}
```

**Quy tắc validate:**
- `report_date` **phải là ngày hôm nay** — BE sẽ bỏ qua dòng có ngày khác
- Tổng `progress_pct` của tất cả các ngày (bao gồm ngày hôm nay) **không được vượt 100%**
- `hours`: số giờ làm, kiểu float (VD: 6.5)
- `progress_pct`: số nguyên từ 0-100
- `note`: ghi chú tùy chọn

**Response thành công (200):**
```json
{
  "message": "Lưu tiến độ thành công",
  "status": 200,
  "data": {
    "success": 2,
    "errors": []
  }
}
```

**Response có lỗi validate (200 nhưng có errors):**
```json
{
  "message": "Lưu tiến độ thành công",
  "status": 200,
  "data": {
    "success": 1,
    "errors": [
      {
        "task_id": 456,
        "error": "Tổng tiến độ vượt 100% (hiện tại: 85%, nhập thêm: 20%)"
      }
    ]
  }
}
```

---

### 2.5. Đếm task chưa báo cáo (Badge count)

Dùng để hiển thị badge đỏ trên menu/icon.

```
GET /api/v1/assign/tasks/daily-report/count
```

**Response (200):**
```json
{
  "message": "success",
  "status": 200,
  "data": {
    "count": 3
  }
}
```

`count` = số task cần báo cáo hôm nay mà **chưa nhập** (progress_pct = 0 hoặc chưa có log).

---

## 3. Push Notification (FCM)

### 3.1. Payload notification nhận được

```json
{
  "notification": {
    "title": "Nhắc báo cáo tiến độ",
    "body": "Bạn có 3 task cần báo cáo tiến độ hôm nay"
  },
  "data": {
    "click_action": "/assign/tasks/daily-report",
    "task_count": "3"
  }
}
```

| Trường | Mô tả |
|--------|--------|
| `notification.title` | Tiêu đề notification |
| `notification.body` | Nội dung, có kèm số lượng task |
| `data.click_action` | Deep link path — dùng để navigate khi tap notification |
| `data.task_count` | Số task cần báo cáo (string) |

### 3.2. Lịch gửi notification

- Cron BE chạy **mỗi 30 phút**
- Nếu company **có cấu hình** `task_report_notify_time` → gửi đúng giờ đó (match trong khoảng 15 phút)
- Nếu company **không có cấu hình** → gửi **2 lần** lúc **08:30** và **17:30**
- Chỉ gửi cho user có task chưa nhập tiến độ → nếu đã nhập rồi thì không nhận notification nữa

### 3.3. Xử lý trên Mobile

**Khi nhận notification:**
- App đang mở (foreground): Hiện in-app notification/toast
- App ở background/đã tắt: Hiện system notification

**Khi user tap notification:**
- Navigate tới màn hình nhập tiến độ (daily report)
- Dùng `data.click_action` để xác định route

---

## 4. Gợi ý UI Mobile

### 4.1. Màn danh sách báo cáo tiến độ

```
┌─────────────────────────────────────┐
│  ← Báo cáo tiến độ task     [Lưu]  │
│  Hôm nay: 03/04/2026               │
├─────────────────────────────────────┤
│  Tổng: 5  |  Chờ: 3  |  Xong: 2   │
├─────────────────────────────────────┤
│                                     │
│  ▼ TASK-001: Thiết kế UI login      │
│    Dự án ABC | Hạn: 10/04          │
│    Tiến độ hiện tại: 30%            │
│  ┌─────────────────────────────┐    │
│  │ 01/04 | 6h | 15% | wireframe│   │  ← readonly (past)
│  │ 02/04 | 8h | 30% | mockup   │   │  ← readonly (past)
│  │ 03/04 | [  ] [  ] [       ] │   │  ← editable (today) - highlight
│  │ 04/04 |  -  |  -  |    -    │   │  ← disabled (future)
│  └─────────────────────────────┘    │
│                                     │
│  ▶ TASK-002: API integration        │
│    Dự án XYZ | Hạn: 15/04          │
│                                     │
├─────────────────────────────────────┤
│  [         Lưu tất cả            ] │
└─────────────────────────────────────┘
```

### 4.2. Badge count

- Gọi `GET /daily-report/count` khi mở app hoặc sau khi nhận notification
- Hiển thị badge đỏ trên icon menu "Báo cáo tiến độ task"
- Ẩn badge khi `count = 0`

---

## 5. Checklist triển khai

### Firebase setup
- [ ] Tích hợp Firebase SDK (iOS: `FirebaseMessaging`, Android: `firebase-messaging`)
- [ ] Cấu hình `google-services.json` (Android) / `GoogleService-Info.plist` (iOS)
- [ ] Xin quyền notification từ user
- [ ] Lấy FCM token và gửi lên BE (`POST /assign/fcm-tokens`)
- [ ] Lưu FCM token local để xóa khi logout
- [ ] Xử lý token refresh → gửi token mới lên BE
- [ ] Xóa FCM token khi logout (`DELETE /assign/fcm-tokens`)

### Push notification
- [ ] Nhận và hiển thị notification (foreground + background)
- [ ] Xử lý tap notification → navigate tới màn daily report
- [ ] Parse `data.click_action` và `data.task_count`

### Màn daily report
- [ ] Gọi API lấy danh sách task (`GET /daily-report`)
- [ ] Hiển thị danh sách task dạng accordion/expandable
- [ ] Hiển thị progress_rows: past (readonly), today (editable, highlight), future (disabled)
- [ ] Input: hours (float), progress_pct (int 0-100), note (text)
- [ ] Validate client: tổng progress_pct <= 100%
- [ ] Gọi API lưu (`POST /daily-report/save`)
- [ ] Xử lý response errors (hiện thông báo task nào lỗi)
- [ ] Summary cards: Tổng task | Chờ báo cáo | Đã hoàn thành

### Badge
- [ ] Gọi `GET /daily-report/count` khi mở app
- [ ] Hiển thị badge trên menu item
- [ ] Refresh count sau khi lưu báo cáo thành công
