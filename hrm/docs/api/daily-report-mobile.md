# API Documentation — Nhập báo cáo tiến độ task (Mobile App)

> Tài liệu này dành cho **team mobile** triển khai chức năng nhập tiến độ task hằng ngày trong app native (iOS / Android).
> Phần FCM Push Notification cho web đã có riêng — mobile tự dùng FCM topic riêng theo cơ chế của app.

---

## 1. Tổng quan

### 1.1. Mục đích
Cho phép nhân viên (assignee) xem danh sách task đang thực hiện cần báo cáo tiến độ trong ngày và nhập kết quả hàng loạt từ app mobile.

### 1.2. Luồng tổng quan

```
┌──────────────┐     1. GET danh sách      ┌─────────────────┐
│  Mobile App  │ ────────────────────────→ │   Backend API   │
│              │ ←──────────────────────── │   (Laravel)     │
└──────────────┘   tasks + progress_rows   └─────────────────┘
        │
        │ 2. User nhập hours + % + note
        │    (chỉ dòng today)
        ▼
┌──────────────┐     3. POST save batch    ┌─────────────────┐
│  Mobile App  │ ────────────────────────→ │   Backend API   │
│              │ ←──────────────────────── │                 │
└──────────────┘     {success, errors}     └─────────────────┘
        │
        │ 4. Refresh count badge
        ▼
┌──────────────┐     GET count             ┌─────────────────┐
│  Mobile App  │ ────────────────────────→ │   Backend API   │
└──────────────┘ ←──────────────────────── └─────────────────┘
```

### 1.3. Base URL & Auth

| | |
|---|---|
| **Base URL** | `https://<api-host>/api/v1` |
| **Auth** | `Authorization: Bearer {JWT_TOKEN}` |
| **Content-Type** | `application/json` |

User đã login → đã có JWT từ luồng auth chung. Không có gì khác biệt cho daily-report.

---

## 2. API Endpoints

### 2.1. Lấy danh sách task cần báo cáo hôm nay

Trả về tất cả task `IN_PROGRESS` của user, có rule báo cáo định kỳ active, đến lịch hôm nay; kèm `progress_rows` (lịch sử các ngày báo cáo).

```
GET /api/v1/assign/tasks/daily-report
```

**Headers:**
```
Authorization: Bearer {JWT_TOKEN}
```

**Query params:** Không có.

**Response 200:**
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
      "status_color": "#2563eb",
      "priority": 2,
      "priority_name": "Trung bình",
      "due_date": "2026-04-30",
      "due_time": "17:00:00",
      "start_date": "2026-04-15",
      "progress_pct": 30,
      "total_progress_pct": 50,
      "is_reported_today": false,
      "project_name": "Dự án ABC",
      "assignee_name": "Nguyễn Văn A",
      "report_rule": {
        "cycle_type": 1,
        "send_time": "08:00:00"
      },
      "progress_rows": [
        {
          "report_date": "2026-04-16",
          "hours": 8,
          "progress_pct": 30,
          "note": "Hoàn thành wireframe",
          "is_today": false,
          "is_past": true,
          "is_future": false,
          "is_editable": false
        },
        {
          "report_date": "2026-04-17",
          "hours": 4,
          "progress_pct": 20,
          "note": "Pixel-perfect mockup",
          "is_today": false,
          "is_past": true,
          "is_future": false,
          "is_editable": false
        },
        {
          "report_date": "2026-04-18",
          "hours": null,
          "progress_pct": null,
          "note": null,
          "is_today": true,
          "is_past": false,
          "is_future": false,
          "is_editable": true
        },
        {
          "report_date": "2026-04-19",
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

#### Giải thích các trường task

| Field | Type | Mô tả |
|-------|------|-------|
| `id` | int | ID task — dùng làm `task_id` khi save |
| `code` | string | Mã task (display) |
| `title` | string | Tên task |
| `status` | int | 4 = IN_PROGRESS (luôn = 4 ở endpoint này) |
| `status_name` | string | Tên hiển thị: "Đang thực hiện" |
| `status_color` | string | Mã màu hex để render badge |
| `priority` | int | 1=Thấp, 2=Trung bình, 3=Cao |
| `priority_name` | string | Tên hiển thị priority |
| `due_date` | string\|null | Ngày hạn (YYYY-MM-DD) |
| `due_time` | string\|null | Giờ hạn (HH:mm:ss) |
| `start_date` | string\|null | Ngày bắt đầu |
| `progress_pct` | int | % tiến độ hiện tại của task (lấy từ log có `report_date` mới nhất) |
| `total_progress_pct` | int | Tổng % đã báo cáo qua tất cả các ngày (cumulative) |
| `is_reported_today` | bool | `true` nếu hôm nay đã có log với `progress_pct > 0` |
| `project_name` | string\|null | Tên dự án |
| `assignee_name` | string\|null | Tên người được giao |
| `report_rule.cycle_type` | int | 1=Daily, 2=Weekly, 3=Monthly |
| `report_rule.send_time` | string | Giờ yêu cầu báo cáo (HH:mm:ss) — chỉ để display |
| `progress_rows` | array | Lịch các ngày báo cáo (xem dưới) |

#### Giải thích `progress_rows`

Mỗi phần tử là 1 ngày trong lịch báo cáo của task (past + today + future).

| Field | Type | Mô tả |
|-------|------|-------|
| `report_date` | string | Ngày báo cáo (YYYY-MM-DD) |
| `hours` | float\|null | Số giờ làm — `null` nếu chưa nhập |
| `progress_pct` | int\|null | % tiến độ ngày đó (0-100) |
| `note` | string\|null | Ghi chú |
| `is_today` | bool | `true` nếu là hôm nay |
| `is_past` | bool | `true` nếu là ngày quá khứ |
| `is_future` | bool | `true` nếu là ngày tương lai |
| `is_editable` | bool | **Chỉ `true` khi `is_today = true`** |

#### Quy tắc render UI

| Trường hợp | UI gợi ý |
|------------|---------|
| `is_editable = true` (today) | Hiện input cho `hours`, `progress_pct`, `note`. Highlight nền xanh lá hoặc viền nổi bật |
| `is_past = true` | Read-only. Hiển thị giá trị đã có (nếu null thì hiện "—") |
| `is_future = true` | Disabled. Hiển thị "Chưa đến ngày báo cáo" |

#### Sort order

BE trả về task đã sort sẵn:
1. **Task chưa nhập** (`is_reported_today = false`) lên trước
2. Trong cùng nhóm → sort theo `report_rule.send_time` tăng dần

→ Mobile **không cần sort lại**.

#### Trường hợp empty

```json
{
  "message": "success",
  "status": 200,
  "data": []
}
```

Khi `data` rỗng → hiển thị empty state: "Không có task cần báo cáo tiến độ hôm nay" (kèm icon ✓).

---

### 2.2. Lưu báo cáo tiến độ hàng loạt

Lưu/update tiến độ cho nhiều task cùng lúc. Chỉ chấp nhận log có `report_date = today`.

```
POST /api/v1/assign/tasks/daily-report/save
```

**Headers:**
```
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json
```

**Request body:**
```json
{
  "tasks": [
    {
      "task_id": 123,
      "progress_logs": [
        {
          "report_date": "2026-04-18",
          "hours": 6.5,
          "progress_pct": 25,
          "note": "Xong phần header"
        }
      ]
    },
    {
      "task_id": 456,
      "progress_logs": [
        {
          "report_date": "2026-04-18",
          "hours": 2,
          "progress_pct": 10,
          "note": ""
        }
      ]
    }
  ]
}
```

#### Field rules

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| `tasks` | array | **Yes** | Danh sách task cần lưu, không rỗng |
| `tasks[].task_id` | int | **Yes** | ID task — phải là task của auth user |
| `tasks[].progress_logs` | array | **Yes** | Mảng log; chỉ chấp nhận 1 log có `report_date = today` |
| `progress_logs[].report_date` | string | **Yes** | YYYY-MM-DD; **phải = ngày hôm nay** (server check) |
| `progress_logs[].hours` | float | No | Số giờ làm (vd 6.5) |
| `progress_logs[].progress_pct` | int | **Yes** | 0-100 |
| `progress_logs[].note` | string | No | Ghi chú, có thể rỗng |

#### Validate rules (server-side)

1. `tasks` phải là array, không rỗng → nếu sai trả 400.
2. `task_id` phải thuộc user (`assignee_id == auth()->id()`) → nếu không khớp, **silent skip** (không lỗi, chỉ không lưu).
3. `report_date` phải = today (`Carbon::today()->toDateString()`) → khác sẽ silent skip.
4. **Tổng `progress_pct` của tất cả log cho task ≤ 100%**:
   - BE tính `existingTotal = SUM(progress_pct của các log của task này, loại trừ today)`
   - Nếu `existingTotal + new_progress_pct > 100` → task đó bị skip + thêm vào `errors[]`
5. Sau lưu, BE update `task.progress_pct = log có report_date lớn nhất`.

#### Response 200 — Success

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

#### Response 200 — Có errors (partial success)

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

→ Mobile cần **show toast warning** liệt kê task nào bị lỗi (dùng `task_id` để map ngược ra `title`).

#### Response 400 — Bad request

```json
{
  "message": "Dữ liệu rỗng",
  "status": 400
}
```

Trả khi `tasks` rỗng hoặc không phải array.

#### Validate trên client (gợi ý)

Trước khi gọi API, mobile **nên validate trước** để UX mượt:

| Rule | Cách check |
|------|-----------|
| Tổng past + today ≤ 100% | Sum tất cả `progress_pct` trong `progress_rows` (kể cả today user vừa nhập) ≤ 100. Nếu vượt → highlight đỏ + toast, không submit |
| `hours` ≥ 0, ≤ 24 | Range input |
| `progress_pct` 0-100 | Range input |
| `report_date` = today | Lấy trực tiếp từ `progress_rows` không cần user chọn |

---

### 2.3. Đếm task chưa nhập (Badge count)

Dùng để hiển thị badge đỏ trên icon menu/tab "Báo cáo tiến độ task".

```
GET /api/v1/assign/tasks/daily-report/count
```

**Headers:**
```
Authorization: Bearer {JWT_TOKEN}
```

**Response 200:**
```json
{
  "message": "success",
  "status": 200,
  "data": {
    "count": 3
  }
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| `count` | int | Số task IN_PROGRESS due today **chưa có log với `progress_pct > 0`** |

#### Khi nào nên gọi

- App vừa mở (warm start / cold start)
- Sau khi user lưu thành công ở 2.2
- Khi nhận push notification từ FCM mobile (refresh count)
- Pull to refresh trên màn task

---

## 3. Data Structure & Enum

### 3.1. Bảng dữ liệu (chỉ tham khảo)

Mobile không cần biết chi tiết schema — đây chỉ để hiểu thuật ngữ.

| Bảng | Mô tả |
|------|-------|
| `tasks` | Task gốc; `assignee_id`, `status`, `progress_pct` |
| `task_progress_report_rules` | 1-1 với task; `cycle_type`, `send_time`, `week_days`, `month_day`, `is_active` |
| `task_result_progress_logs` | N-1 với task; `report_date` + `progress_pct` + `hours` + `note` |

### 3.2. Enum — Task Status

Mobile chỉ cần quan tâm **status = 4 (IN_PROGRESS)** vì endpoint daily-report chỉ trả task này.

| Value | Constant | Tên | Màu |
|-------|----------|-----|-----|
| 4 | IN_PROGRESS | Đang thực hiện | `#2563eb` |

(Các status khác xem doc đầy đủ ở `docs/srs/notify-task-report.html`.)

### 3.3. Enum — Cycle Type

| Value | Tên | Logic due today |
|-------|-----|----------------|
| 1 | Daily | Luôn due |
| 2 | Weekly | Due nếu hôm nay là 1 trong các thứ trong `week_days` |
| 3 | Monthly | Due nếu hôm nay là `month_day` |

→ Mobile **không cần tự tính** due/not due — BE đã filter sẵn ở 2.1, chỉ trả task đã đến lịch.

### 3.4. Enum — Priority

| Value | Tên | Màu gợi ý |
|-------|-----|-----------|
| 1 | Thấp | `#64748b` (xám) |
| 2 | Trung bình | `#f59e0b` (cam) |
| 3 | Cao | `#ef4444` (đỏ) |

---

## 4. Business Rules (mobile cần nhớ)

| ID | Rule | Tác động trên mobile |
|----|------|---------------------|
| BR-01 | Chỉ hiển thị task `IN_PROGRESS` | Endpoint 2.1 đã filter, mobile không cần check |
| BR-02 | Chỉ ngày `today` editable | Render input chỉ cho row có `is_editable = true` |
| BR-03 | Tổng progress_pct ≤ 100% | Validate client trước khi submit |
| BR-04 | Task đã nhập hôm nay → `is_reported_today = true` | Hiển thị icon ✓ + style "đã hoàn thành" |
| BR-05 | Permission ownership | Endpoint chỉ trả task của user — mobile không cần lo |
| BR-06 | Sort: chưa nhập trước | Hiển thị theo thứ tự BE trả về, không sort lại |

---

## 5. Gợi ý UI Mobile

### 5.1. Màn Daily Report

```
┌─────────────────────────────────────┐
│ ← Báo cáo tiến độ task        [💾] │  ← Header + nút Lưu
│ Hôm nay: 18/04/2026                 │
├─────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐         │
│ │ Tổng │ │ Chờ  │ │Hoàn t│         │  ← 3 summary card
│ │   5  │ │   3  │ │ 2/5  │         │
│ └──────┘ └──────┘ └──────┘         │
├─────────────────────────────────────┤
│                                     │
│ ▶ TASK-001: Thiết kế UI            │  ← Accordion collapse
│   Dự án ABC | Hạn: 30/04           │
│   Tiến độ: 30%      [Đang TH] [TB] │
│                                     │
│ ▼ TASK-002: API integration         │  ← Mở rộng
│   Dự án XYZ | Hạn: 25/04           │
│   ┌─────────────────────────────┐  │
│   │ NGÀY  | GIỜ | %   | NOTE    │  │
│   │ 16/04 | 8h  | 30% | xong A  │  │  ← past, readonly
│   │ 17/04 | 6h  | 20% | test    │  │
│   │ 18/04 | [_] |[_]% |[______] │  │  ← today, EDITABLE
│   │ 19/04 |  -  |  -  |   -     │  │  ← future, disabled
│   └─────────────────────────────┘  │
│   ⚠ Tổng vượt 100% (nếu có)        │
│                                     │
│ ✓ TASK-003: Standup [Đã báo cáo]   │  ← is_reported_today
│                                     │
├─────────────────────────────────────┤
│ Tổng giờ hôm nay: 4h/8h            │  ← Footer sticky
│ Tiến độ TB: 25%                    │
│         [   💾 Lưu tất cả     ]    │
└─────────────────────────────────────┘
```

### 5.2. Empty state

Khi `data = []`:
```
        ✓ (icon checkmark xanh lớn)
   Không có task cần báo cáo
        tiến độ hôm nay
```

### 5.3. Badge count

- Hiển thị số đỏ tròn trên icon menu/tab "Báo cáo tiến độ"
- Ẩn nếu `count = 0`
- Refresh sau mỗi lần save thành công

### 5.4. Confirm khi back

Nếu user đã edit nhưng chưa save → khi back, hiện confirm:
> "Bạn có thay đổi chưa lưu. Lưu trước khi thoát?"
> [Huỷ] [Bỏ thay đổi] [Lưu & thoát]

---

## 6. Error Handling

| HTTP | Trường hợp | Mobile xử lý |
|------|-----------|--------------|
| 200 + `errors=[]` | Lưu thành công hết | Toast "Lưu thành công" + reload data |
| 200 + `errors!=[]` | Có task bị skip do vượt 100% | Toast warning + liệt kê task lỗi (map từ `task_id` ra `title`) |
| 400 | Payload sai (rỗng, không phải array) | Toast "Dữ liệu không hợp lệ" + log để debug |
| 401 | Token hết hạn | Logout user, navigate về màn login |
| 403 | Không có quyền | Toast "Không có quyền truy cập" |
| 500 | Server error | Toast "Có lỗi hệ thống, thử lại sau" |
| Timeout / network error | Mất mạng | Toast "Mất kết nối" + button retry; có thể cache payload local để retry sau |

---

## 7. Sample code (pseudo)

### 7.1. Load & render

```typescript
// Pseudo TypeScript / React Native style
async function loadDailyReport() {
  const res = await api.get('/assign/tasks/daily-report');
  const tasks = res.data.data; // đã sort sẵn

  setState({ tasks: tasks.map(t => ({
    ...t,
    expanded: false,
    edited: false,
  }))});
}
```

### 7.2. Validate + Save

```typescript
async function saveAll() {
  // 1. Build payload (chỉ task có row today được edit)
  const payload = {
    tasks: tasks
      .map(t => {
        const todayRow = t.progress_rows.find(r => r.is_today);
        if (!todayRow || todayRow.progress_pct == null) return null;

        return {
          task_id: t.id,
          progress_logs: [{
            report_date: todayRow.report_date,
            hours: Number(todayRow.hours) || 0,
            progress_pct: Number(todayRow.progress_pct),
            note: todayRow.note || '',
          }],
        };
      })
      .filter(Boolean),
  };

  if (payload.tasks.length === 0) {
    toast.warning('Chưa có dữ liệu để lưu');
    return;
  }

  // 2. Validate client: tổng past + today ≤ 100%
  for (const t of tasks) {
    const totalPast = t.progress_rows
      .filter(r => r.is_past && r.progress_pct)
      .reduce((s, r) => s + Number(r.progress_pct), 0);
    const todayPct = t.progress_rows.find(r => r.is_today)?.progress_pct || 0;
    if (totalPast + Number(todayPct) > 100) {
      toast.error(`Task "${t.title}" vượt 100% tiến độ`);
      return;
    }
  }

  // 3. Submit
  try {
    const res = await api.post('/assign/tasks/daily-report/save', payload);
    const { success, errors } = res.data.data;

    if (errors.length > 0) {
      const failedTitles = errors
        .map(e => tasks.find(t => t.id === e.task_id)?.title)
        .filter(Boolean)
        .join(', ');
      toast.warning(`Lưu được ${success} task. Lỗi: ${failedTitles}`);
    } else {
      toast.success(`Đã lưu ${success} task`);
    }

    await loadDailyReport();
    await refreshBadgeCount();
  } catch (err) {
    if (err.status === 401) navigateToLogin();
    else toast.error('Lỗi khi lưu');
  }
}
```

### 7.3. Badge count

```typescript
async function refreshBadgeCount() {
  const res = await api.get('/assign/tasks/daily-report/count');
  setBadge(res.data.data.count);
}
```

---

## 8. Checklist triển khai mobile

### Màn Daily Report
- [ ] Gọi `GET /assign/tasks/daily-report` khi mount màn + pull-to-refresh
- [ ] Hiển thị 3 summary card: Tổng / Chờ báo cáo / Đã hoàn thành
- [ ] Render danh sách task dạng accordion (collapse mặc định)
- [ ] Mỗi task: hiển thị title, code, project, due_date, status badge, priority badge
- [ ] Bảng `progress_rows`:
  - [ ] Past row: readonly, màu xám
  - [ ] Today row: input cho hours/progress_pct/note, highlight viền xanh
  - [ ] Future row: disabled, hiện "Chưa đến ngày báo cáo"
- [ ] Icon ✓ cho task có `is_reported_today = true`
- [ ] Validate client: sum past + today ≤ 100%, hiện error inline
- [ ] Empty state khi `data = []`
- [ ] Footer sticky: tổng giờ today, tiến độ TB, count chưa nhập, button "Lưu tất cả"

### Save flow
- [ ] Build payload chỉ task có row today được edit + có data
- [ ] Validate tổng % trước khi submit
- [ ] Gọi `POST /save`
- [ ] Xử lý response: success vs partial errors
- [ ] Toast result + reload data + refresh badge

### Badge
- [ ] Gọi `GET /count` khi: app mở, sau save thành công, sau nhận push (nếu mobile có FCM riêng)
- [ ] Hiển thị badge đỏ trên menu/tab item
- [ ] Ẩn badge khi `count = 0`

### Error handling
- [ ] Token expired (401) → logout + navigate login
- [ ] Network error → toast + retry button
- [ ] Server 500 → toast generic + log

### UX
- [ ] Confirm khi back nếu có thay đổi chưa lưu
- [ ] Loading state khi gọi API
- [ ] Disable button "Lưu" khi đang submit
- [ ] Format date: hiện DD/MM/YYYY (input vẫn YYYY-MM-DD)

---

## 9. Tham chiếu

| Tài liệu | Nội dung |
|---------|---------|
| `docs/srs/notify-task-report.html` | SRS đầy đủ — sơ đồ use case, swimlane, ER diagram |
| `docs/notify-task-report-mobile.md` | Doc cũ về push notification (web FCM) — bỏ qua nếu mobile dùng FCM riêng |
| `docs/srs/notify-task-report-user-guide.html` | Hướng dẫn người dùng cuối |

---

**Câu hỏi / cần hỗ trợ?** Liên hệ team BE qua channel `#erp-tpe-backend` trên Slack.
