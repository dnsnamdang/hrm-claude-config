# SRS: My To Do

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Assign (Giao việc) |
| Phiên bản | 1.0 |
| Ngày tạo | 2026-05-02 |
| Người tạo | @dnsnamdang |
| Trạng thái | Draft |

---

## 1. Giới thiệu

### 1.1. Mục đích

Tạo trang "My To Do" giúp user quản lý tổng hợp công việc cá nhân theo thời gian. Trang tích hợp dữ liệu từ nhiều đối tượng trong HRM (Task, Issue, Phiếu giao việc, Phiếu giao công tác, Meeting) cùng CRUD Todo cá nhân với danh sách và sub-task.

Cơ chế dữ liệu: **Query trực tiếp (real-time)** — không lưu bản sao, không sync. Khi user mở trang, BE query song song vào các bảng gốc rồi normalize kết quả trả về.

### 1.2. Phạm vi

**Trong scope:**
- Hiển thị tổng hợp (unified view) công việc từ Task, Issue, Meeting, AssignJob, AssignRequest
- CRUD danh sách cá nhân (PersonalTodoList) + kéo thả sắp xếp
- CRUD todo cá nhân (PersonalTodo) + sub-task 1 cấp + toggle hoàn thành
- Mini calendar hiển thị tổng quan theo tháng
- Lọc theo loại, trạng thái, ngày
- Nhóm items theo thời hạn (Quá hạn, Hôm nay, Ngày mai, Tuần này, Tuần sau...)
- Action buttons cho Task/Issue (Xem, Sửa, Nhập kết quả, Duyệt, Xử lý, Lịch sử)

**Ngoài scope:**
- Phân quyền theo role (mọi user đều truy cập được, chỉ thấy dữ liệu của chính mình)
- Notification / nhắc nhở deadline
- Drag-drop sắp xếp todo items trong danh sách chính
- Export / Import dữ liệu

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| Unified view | Tổng hợp nhiều loại entity (Task, Issue, Meeting...) vào 1 danh sách chung |
| Personal Todo | Việc cần làm do user tự tạo, không liên kết entity hệ thống |
| Sub-task | Bước con của 1 Personal Todo (tối đa 1 cấp) |
| Source / Vai trò | Mối quan hệ giữa user và item: Được giao, Tham gia, Cần duyệt, Theo dõi, Cá nhân |
| Normalize | Chuyển đổi các entity khác loại về 1 format chung để hiển thị thống nhất |

---

## 2. Actors & Permissions

| Actor | Mô tả | Permissions |
|-------|-------|-------------|
| User (bất kỳ) | Nhân viên đã đăng nhập hệ thống | Xem/tạo/sửa/xóa todo cá nhân của chính mình. Xem thông tin tổng hợp từ các entity hệ thống mà mình có liên quan |

Không yêu cầu phân quyền đặc biệt. Dữ liệu được cô lập theo `user_id` — user chỉ thấy dữ liệu của chính mình.

---

## 3. Use Cases

### UC-01: Xem tổng hợp công việc

| | |
|---|---|
| **Actor** | User |
| **Precondition** | User đã đăng nhập, truy cập `/assign/my-todo` |
| **Main Flow** | |
| 1 | Hệ thống query song song: Tasks, Issues, AssignJobs, AssignRequests, Meetings, Personal Todos |
| 2 | Normalize tất cả về format chung, deduplicate (ưu tiên source cao nhất) |
| 3 | Nhóm items theo thời hạn: Hôm nay → Ngày mai → Tuần này → Tuần sau → Sắp tới → Không hạn → Quá hạn |
| 4 | Hiển thị stats (quá hạn, hôm nay, tuần này, tổng), calendar sidebar, danh sách cá nhân |
| **Postcondition** | User thấy danh sách tổng hợp tất cả công việc liên quan |
| **Alternative Flow** | Nếu user chưa có danh sách cá nhân → tự tạo list "Mac dinh" |

### UC-02: Lọc danh sách

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Đang ở trang My To Do |
| **Main Flow** | |
| 1 | User chọn bộ lọc: Loại (Task/Issue/Meeting/...), Trạng thái (Chưa xong/Đã xong/Tất cả) |
| 2 | Hệ thống gọi lại API với filter params |
| 3 | Danh sách cập nhật theo bộ lọc |
| **Postcondition** | Danh sách chỉ hiển thị items khớp với bộ lọc |
| **Alternative Flow** | Tìm kiếm text → filter client-side trên title |

### UC-03: Xem theo ngày trên calendar

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Đang ở trang My To Do |
| **Main Flow** | |
| 1 | User click 1 ngày trên mini calendar |
| 2 | Danh sách chuyển sang flat mode (không nhóm), chỉ hiển thị items có due_date = ngày đó |
| 3 | Click lại cùng ngày → bỏ chọn, quay về grouped mode |
| **Postcondition** | Danh sách hiển thị items của ngày đã chọn |

### UC-04: Tạo todo cá nhân

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Đang ở trang My To Do |
| **Main Flow** | |
| 1 | User click nút "Tạo todo" trên filter bar |
| 2 | Modal TodoFormModal hiển thị: title (bắt buộc), description, danh sách, ngày hạn, giờ hạn |
| 3 | User điền thông tin, nhấn Lưu |
| 4 | API POST `/assign/my-todo/todos` |
| 5 | Todo mới xuất hiện trong danh sách |
| **Postcondition** | Todo cá nhân được tạo thành công |
| **Exception** | Title rỗng → hiện thông báo lỗi validation |

### UC-05: Toggle hoàn thành todo / sub-task

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Có todo cá nhân trong danh sách |
| **Main Flow** | |
| 1 | User click checkbox của todo cá nhân |
| 2 | API PATCH `/assign/my-todo/todos/{id}/toggle` |
| 3 | Toggle `is_completed` (0↔1), ghi `completed_at` khi đánh hoàn thành |
| 4 | UI cập nhật (gạch ngang title nếu hoàn thành) |
| **Postcondition** | Trạng thái hoàn thành được toggle |

### UC-06: Tạo / Sửa / Xóa danh sách cá nhân

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Đang ở trang My To Do |
| **Main Flow (Tạo)** | |
| 1 | Click "Tạo danh sách mới" trên sidebar |
| 2 | Modal TodoListFormModal: name (bắt buộc), description |
| 3 | API POST `/assign/my-todo/lists` |
| **Main Flow (Xóa)** | |
| 1 | Click nút xóa → confirm dialog "Xóa danh sách? Tất cả việc sẽ bị xóa." |
| 2 | API DELETE `/assign/my-todo/lists/{id}` |
| 3 | Cascade xóa tất cả todos bên trong |
| **Postcondition** | Danh sách được tạo/sửa/xóa |

### UC-07: Kéo thả sắp xếp danh sách cá nhân

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Có ít nhất 2 danh sách cá nhân |
| **Main Flow** | |
| 1 | User hover vào dòng list → icon drag handle xuất hiện |
| 2 | Kéo thả list đến vị trí mới |
| 3 | UI cập nhật ngay (optimistic update) |
| 4 | API POST `/assign/my-todo/lists/reorder` với `{ items: [{id, sort_order}] }` |
| **Postcondition** | Thứ tự danh sách được lưu lại |
| **Exception** | API lỗi → reload lại danh sách từ server |

### UC-08: Xem chi tiết danh sách cá nhân

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Đang ở trang My To Do, có ít nhất 1 danh sách |
| **Main Flow** | |
| 1 | Click vào tên danh sách trên sidebar |
| 2 | Vùng chính chuyển sang TodoListDetail (thay cho TodoMainList) |
| 3 | Hiển thị: header (tên + mô tả + nút sửa/xóa), danh sách todos (pending + completed), input thêm mới |
| 4 | User có thể thêm todo inline (Enter), thêm sub-task inline, toggle, xóa từng item |
| **Postcondition** | User thấy chi tiết 1 danh sách cá nhân |
| **Alternative Flow** | Click lại cùng list → quay về trang chính (toggle) |

### UC-09: Tương tác với item hệ thống (Task/Issue)

| | |
|---|---|
| **Actor** | User |
| **Precondition** | Có item hệ thống trong danh sách |
| **Main Flow (Task)** | |
| 1 | Hover vào item → action buttons xuất hiện: Xem, Sửa (nếu can_edit), Nhập KQ (nếu can_import_result), Duyệt (nếu can_approve), Lịch sử |
| 2a | Click "Xem" → mở CreateTaskModal (status 1-3,10) hoặc ImportResultModal (status 4-9) ở chế độ view |
| 2b | Click "Sửa" → mở CreateTaskModal chế độ edit |
| 2c | Click "Nhập KQ" / "Duyệt" → mở ImportResultModal |
| 2d | Click "Lịch sử" → mở TaskHistoryModal |
| **Main Flow (Issue)** | |
| 1 | Action buttons: Xem, Sửa (nếu can_edit), Xử lý (nếu can_handle), Lịch sử |
| 2 | Click → mở CreateIssueModal hoặc IssueHistoryModal tương ứng |
| **Main Flow (AssignJob / AssignBusiness / Meeting)** | |
| 1 | Click item → `window.open(item.url, '_blank')` — mở tab mới |
| **Postcondition** | User có thể thao tác nhanh trên item mà không rời trang My To Do |

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | Sub-task 1 cấp | Sub-task chỉ được gắn vào todo cha (parent.parent_id phải NULL). Không cho tạo sub-task của sub-task | `MyTodoService::storeTodo()` |
| BR-02 | List mặc định tự tạo | Khi user truy cập My Todo lần đầu, hệ thống tự tạo 1 list "Mac dinh" nếu chưa có list nào | `MyTodoService::getOrCreateDefaultList()` |
| BR-03 | Xóa list cascade | Xóa danh sách → xóa tất cả todos bên trong (cả sub-tasks) | `MyTodoService::destroyList()` |
| BR-04 | Xóa todo cascade | Xóa todo cha → xóa tất cả sub-tasks | `MyTodoService::destroyTodo()` |
| BR-05 | Cô lập dữ liệu | Mọi query đều filter `user_id = auth_user_id`. User chỉ thao tác dữ liệu của chính mình | Tất cả methods trong Service |
| BR-06 | Deduplicate | Nếu user vừa là assignee vừa là watcher cùng 1 entity → chỉ hiện 1 lần, ưu tiên: assigned(1) > approver(2) > watching(3) > participant(4) > personal(5) | `MyTodoService::deduplicateItems()` |
| BR-07 | Toggle completed | Đánh dấu hoàn thành → ghi `completed_at = now()`. Bỏ đánh dấu → set `completed_at = null` | `MyTodoService::toggleTodo()` |
| BR-08 | Sort order tự tăng | Khi tạo mới list hoặc todo, `sort_order = max(sort_order) + 1` trong cùng scope | `storeList()`, `storeTodo()` |
| BR-09 | Stats chỉ đếm cấp 1 | `todo_count` và `completed_count` của list chỉ đếm todos cấp 1 (không tính sub-tasks) | `PersonalTodoListResource` |
| BR-10 | Filter status done | Khi filter `status=done` → bỏ qua entity hệ thống, chỉ lấy personal todos đã hoàn thành | `MyTodoService::getAll()` |

---

## 5. Data Model

### 5.1. Entity Relationship Diagram

```
[User] 1──N [PersonalTodoList]
[PersonalTodoList] 1──N [PersonalTodo] (via list_id, ON DELETE CASCADE)
[PersonalTodo] 1──N [PersonalTodo] (self-ref via parent_id, max 1 cấp)

--- Entity hệ thống (chỉ query, không tạo mới) ---
[Task] ──── assignee_id = user_id
[Issue] ──── assignee_id = user_id
[AssignJob] ──── employees.employee_info_id = user.employee_info_id
[AssignRequest] ──── employees.employee_id = user_id
[Meeting] ──── company_members.employee_id = employee.id (qua employee_info_id)
```

### 5.2. Bảng dữ liệu

#### Bảng: `personal_todo_lists`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint unsigned PK | No | auto | |
| user_id | bigint unsigned | No | — | Chủ sở hữu |
| name | varchar(255) | No | — | Tên danh sách |
| description | text | Yes | null | Mô tả |
| sort_order | integer | No | 0 | Thứ tự hiển thị |
| company_id | bigint unsigned | Yes | null | Cấp tổ chức |
| created_at | timestamp | Yes | auto | |
| updated_at | timestamp | Yes | auto | |
| created_by | bigint unsigned | Yes | null | Audit |
| updated_by | bigint unsigned | Yes | null | Audit |

**Index:** `user_id`, `company_id`

#### Bảng: `personal_todos`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint unsigned PK | No | auto | |
| list_id | bigint unsigned FK | No | — | → personal_todo_lists.id CASCADE |
| parent_id | bigint unsigned | Yes | null | NULL = todo gốc, có giá trị = sub-task |
| user_id | bigint unsigned | No | — | Chủ sở hữu |
| title | varchar(500) | No | — | Tiêu đề |
| description | text | Yes | null | Mô tả |
| due_date | date | Yes | null | Ngày hạn |
| due_time | time | Yes | null | Giờ hạn |
| is_completed | tinyint | No | 0 | 0 = chưa xong, 1 = hoàn thành |
| completed_at | datetime | Yes | null | Thời điểm đánh hoàn thành |
| sort_order | integer | No | 0 | Thứ tự trong list |
| company_id | bigint unsigned | Yes | null | Cấp tổ chức |
| created_at | timestamp | Yes | auto | |
| updated_at | timestamp | Yes | auto | |
| created_by | bigint unsigned | Yes | null | Audit |
| updated_by | bigint unsigned | Yes | null | Audit |

**Index:** `user_id`, `list_id`, `parent_id`, `due_date`, `company_id`
**FK:** `list_id` → `personal_todo_lists.id` ON DELETE CASCADE

---

## 6. API Specification

### 6.1. Lấy danh sách tổng hợp

```
GET /api/v1/assign/my-todo
Auth: Bearer Token (JWT)
```

**Request (Query params):**

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| type | string | No | `task`, `issue`, `assign_job`, `assign_business`, `meeting`, `personal` |
| status | string | No | `pending` (mặc định), `done`, rỗng = tất cả |
| date | date | No | Lọc chính xác theo ngày (YYYY-MM-DD) |
| date_from | date | No | Từ ngày |
| date_to | date | No | Đến ngày |
| is_overdue | boolean | No | Chỉ lấy quá hạn |
| list_id | integer | No | Lọc theo danh sách cá nhân |
| month | string | No | `YYYY-MM` cho calendar summary |

**Response (200):**
```json
{
  "message": "success",
  "status": 200,
  "data": {
    "items": [
      {
        "type": "task",
        "id": 123,
        "title": "Hoàn thành báo cáo tiến độ Q1",
        "due_date": "2026-05-01",
        "due_time": "17:00",
        "status_text": "Đang làm",
        "status_color": "primary",
        "source": "assigned",
        "source_text": "Được giao",
        "role_text": "Được giao",
        "role_color": "#4a7cfb",
        "role_bg": "#EFF6FF",
        "url": "/assign/task/123",
        "priority": 2,
        "project_name": "DA Nhà máy ABC",
        "assignee_name": "Nguyễn Văn A",
        "status": 4,
        "can_edit": true,
        "can_delete": false,
        "can_import_result": true,
        "can_approve": false,
        "can_view_result": false
      },
      {
        "type": "meeting",
        "id": 45,
        "title": "Họp đồng bộ tiến độ",
        "due_date": "2026-05-02",
        "due_time": "14:00",
        "status_text": "Chốt lịch",
        "status_color": "success",
        "source": "participant",
        "source_text": "Tham gia",
        "role_text": "Tham gia",
        "role_color": "#22c55e",
        "role_bg": "#F0FDF4",
        "url": "/assign/meeting/45/show",
        "member_count": 8,
        "location": "Phòng họp 3A"
      },
      {
        "type": "personal",
        "id": 67,
        "title": "Gọi điện nhà cung cấp thép",
        "due_date": "2026-05-01",
        "due_time": null,
        "status_text": "Việc cần làm",
        "status_color": "secondary",
        "source": "personal",
        "source_text": "Cá nhân",
        "role_text": "Cá nhân",
        "role_color": "#6b7280",
        "role_bg": "#F3F4F6",
        "url": null,
        "list_id": 1,
        "list_name": "Việc cần làm",
        "sub_items": [
          { "id": 68, "title": "Hỏi báo giá thép cuộn", "is_completed": true },
          { "id": 69, "title": "Gửi email xác nhận đơn hàng", "is_completed": false }
        ]
      }
    ],
    "calendar_summary": {
      "2026-05-01": 3,
      "2026-05-02": 1
    },
    "lists": [
      { "id": 1, "name": "Việc cần làm", "sort_order": 0, "todo_count": 5, "completed_count": 2 }
    ]
  }
}
```

### 6.2. Lấy danh sách cá nhân (lists)

```
GET /api/v1/assign/my-todo/lists
Auth: Bearer Token (JWT)
```

**Response (200):**
```json
{
  "message": "success",
  "status": 200,
  "data": [
    { "id": 1, "name": "Việc cần làm", "description": null, "sort_order": 0, "todo_count": 5, "completed_count": 2 }
  ]
}
```

### 6.3. Tạo danh sách

```
POST /api/v1/assign/my-todo/lists
Auth: Bearer Token (JWT)
```

**Request:**

| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| name | string | Yes | max:255 | Tên danh sách |
| description | string | No | — | Mô tả |

**Response (200):** `PersonalTodoListResource`

### 6.4. Cập nhật danh sách

```
PUT /api/v1/assign/my-todo/lists/{id}
Auth: Bearer Token (JWT)
```

**Request:** Giống UC tạo (name required, description optional)

### 6.5. Xóa danh sách

```
DELETE /api/v1/assign/my-todo/lists/{id}
Auth: Bearer Token (JWT)
```

**Response (200):** `{ "message": "success", "status": 200 }`

**Side effect:** Cascade xóa tất cả todos trong list

### 6.6. Sắp xếp danh sách

```
POST /api/v1/assign/my-todo/lists/reorder
Auth: Bearer Token (JWT)
```

**Request:**

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| items | array | Yes | `[{ "id": 1, "sort_order": 0 }, { "id": 2, "sort_order": 1 }]` |

### 6.7. Lấy todos theo list

```
GET /api/v1/assign/my-todo/lists/{listId}/todos
Auth: Bearer Token (JWT)
```

**Response (200):**
```json
{
  "data": {
    "list": { "id": 1, "name": "Việc cần làm", "description": null, "sort_order": 0, "todo_count": 5, "completed_count": 2 },
    "todos": [
      {
        "id": 67, "list_id": 1, "parent_id": null, "title": "Gọi NCC", "description": null,
        "due_date": "2026-05-01", "due_time": null, "is_completed": 0, "completed_at": null, "sort_order": 0,
        "sub_items": [
          { "id": 68, "list_id": 1, "parent_id": 67, "title": "Hỏi báo giá", "is_completed": 1, "sort_order": 0 }
        ]
      }
    ],
    "stats": { "total": 5, "completed": 2, "pending": 3 }
  }
}
```

### 6.8. Tạo todo

```
POST /api/v1/assign/my-todo/todos
Auth: Bearer Token (JWT)
```

**Request:**

| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| list_id | integer | Yes | exists:personal_todo_lists,id | Danh sách chứa |
| parent_id | integer | No | exists:personal_todos,id | Nếu có → tạo sub-task |
| title | string | Yes | max:500 | Tiêu đề |
| description | string | No | — | Mô tả |
| due_date | date | No | format:Y-m-d | Ngày hạn |
| due_time | string | No | format:H:i | Giờ hạn |

**Error cases:**

| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 400 | parent_id trỏ tới 1 sub-task (parent.parent_id != null) | Không cho tạo sub-task cấp 2 |
| 422 | Validation failed | Chi tiết theo field |

### 6.9. Cập nhật todo

```
PUT /api/v1/assign/my-todo/todos/{id}
Auth: Bearer Token (JWT)
```

**Request:** Giống tạo nhưng `list_id` là nullable (cho phép chuyển list)

### 6.10. Toggle hoàn thành todo

```
PATCH /api/v1/assign/my-todo/todos/{id}/toggle
Auth: Bearer Token (JWT)
```

**Response (200):** `PersonalTodoResource` với `is_completed` đã toggle

### 6.11. Xóa todo

```
DELETE /api/v1/assign/my-todo/todos/{id}
Auth: Bearer Token (JWT)
```

**Side effect:** Cascade xóa sub-tasks

### 6.12. Sắp xếp todos

```
PATCH /api/v1/assign/my-todo/todos/reorder
Auth: Bearer Token (JWT)
```

**Request:**

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| items | array | Yes | `[{ "id": 1, "sort_order": 0 }, ...]` |

---

## 7. UI Specification

### 7.1. Màn hình chính — Tổng hợp công việc

- **Route:** `/assign/my-todo`
- **Layout:** 2 cột — cột trái (flex:1) + cột phải (300px fixed)

**Wireframe:**
```
┌───────────────────────────────────────────────────────────────┐
│  Stats: [Quá hạn: N] [Hôm nay: N] [Tuần này: N] [Tổng: N]  │
│  Filter: [Loại ▼] [Trạng thái ▼] [Tìm kiếm...] [Tạo todo]  │
├────────────────────────────────────┬──────────────────────────┤
│                                    │  ◀ Tháng 5 2026 ▶       │
│  ■ HÔM NAY — 02/05 (5)           │  T2 T3 T4 T5 T6 T7 CN   │
│  │ Task: Review PR         17:00  │  [lịch tháng + dot]      │
│  │ Meeting: Họp đồng bộ   14:00  │                          │
│  │ Phiếu: PCT-2026-00123  Hôm nay│  DANH SÁCH CÁ NHÂN      │
│  │ Todo: Gọi điện NCC     02/05  │  ≡ ● Việc cần làm  2/5  │
│  │   ☑ Hỏi báo giá               │  ≡ ● Follow up     0/2  │
│  │   ☐ Gửi email xác nhận        │  [+ Tạo danh sách mới]  │
│                                    │                          │
│  ▶ NGÀY MAI — 03/05 (2)          │                          │
│  ▶ TUẦN NÀY (3)                   │                          │
│  ▶ QUÁ HẠN (1)                    │                          │
├────────────────────────────────────┴──────────────────────────┤
```

**User interactions:**

| Action | Behavior | API call |
|--------|----------|----------|
| Click dropdown Loại | Chọn type filter → reload data | `GET /assign/my-todo?type=task` |
| Click dropdown Trạng thái | Chọn status filter → reload | `GET /assign/my-todo?status=pending` |
| Gõ ô tìm kiếm | Filter client-side trên `title` | Không gọi API |
| Click nút Tạo todo | Mở TodoFormModal | — |
| Click ngày trên calendar | Chuyển flat mode, lọc theo ngày | `GET /assign/my-todo?date=2026-05-03` |
| Click group header | Toggle collapse/expand nhóm | Không gọi API |
| Click item Task | Mở CreateTaskModal (view) | — |
| Click item Issue | Mở CreateIssueModal (view) | — |
| Click item AssignJob/Business/Meeting | `window.open(url, '_blank')` | — |
| Click checkbox todo cá nhân | Toggle hoàn thành | `PATCH .../toggle` |
| Hover item Task/Issue | Hiện action buttons (Xem/Sửa/Nhập KQ/Duyệt/Xử lý/Lịch sử) | — |
| Click list trên sidebar | Chuyển sang TodoListDetail | `GET .../lists/{id}/todos` |
| Kéo thả list trên sidebar | Sắp xếp lại thứ tự (optimistic update) | `POST .../lists/reorder` |

### 7.2. Màn hình chi tiết danh sách

- **Route:** `/assign/my-todo` (cùng trang, thay đổi nội dung cột trái)
- **Điều kiện:** Khi `selectedListId != null`

**Wireframe:**
```
┌───────────────────────────────────────────────────────────────┐
│  My To Do > Việc cần làm                       [Sửa] [Xóa]  │
│  Tổng: 5 việc | Hoàn thành: 2                                │
├────────────────────────────────────┬──────────────────────────┤
│                                    │  Calendar + Lists        │
│  ☐ Gọi NCC thép            29/04  │  (giống màn chính)       │
│    ☑ Đã liên lạc                   │                          │
│    ☐ Hỏi giá thép cuộn            │                          │
│    [+ Thêm bước con...]           │                          │
│  ☐ Gửi báo giá             23/04  │                          │
│  ☑ Check email sáng         —     │                          │
│  ☑ Kiểm tra tiến kho       —     │                          │
│                                    │                          │
│  [+ Thêm việc mới...]             │                          │
├────────────────────────────────────┴──────────────────────────┤
```

**User interactions:**

| Action | Behavior | API call |
|--------|----------|----------|
| Enter ở input "Thêm việc mới" | Tạo todo inline | `POST .../todos` |
| Enter ở input "Thêm bước con" | Tạo sub-task inline | `POST .../todos` (có parent_id) |
| Click checkbox todo | Toggle hoàn thành | `PATCH .../toggle` |
| Hover + click nút xóa | Xóa todo (confirm) | `DELETE .../todos/{id}` |
| Click "Sửa" header | Mở TodoListFormModal | — |
| Click "Xóa" header | Confirm → xóa list | `DELETE .../lists/{id}` |

### 7.3. Hiển thị item

Mỗi item hiển thị:

| Vùng | Nội dung |
|------|----------|
| Viền trái (3px) | Màu theo type: Task=#4a7cfb, Issue=#e25c5c, AssignJob=#22c55e, AssignBusiness=#d4a03c, Meeting=#0ea5e9, Personal=#8e99a4 |
| Icon trái | Icon loại (hoặc checkbox cho personal) |
| Dòng 1 | Title + **Role badge** (pill: Được giao/Tham gia/Cần duyệt/Theo dõi/Cá nhân với màu tương ứng) |
| Dòng 2 | **Status badge** (border+background theo Bootstrap color) · project_name · assignee_name/member_count · location |
| Góc phải | Ngày hạn (DD/MM) hoặc giờ (HH:mm nếu hôm nay). Đỏ nếu quá hạn |
| Hover | Action buttons (chỉ Task/Issue) |

### 7.4. Nhóm thời gian

| Thứ tự | Nhóm | Điều kiện | Màu | Mặc định |
|--------|------|-----------|-----|----------|
| 1 | Hôm nay | `due_date == today` | Xanh #4a7cfb | Mở |
| 2 | Ngày mai | `due_date == tomorrow` | Vàng #d4a03c | Thu gọn |
| 3 | Tuần này | `due_date` còn lại trong tuần | Teal #14b8a6 | Thu gọn |
| 4 | Tuần sau | `due_date` tuần kế tiếp | Xám #8e99a4 | Thu gọn |
| 5 | Sắp tới | `due_date` xa hơn | Xám | Thu gọn |
| 6 | Không hạn | `due_date == null` | Xám | Thu gọn |
| 7 | Quá hạn | `due_date < today` | Đỏ #e25c5c | Thu gọn |

Nhóm luôn hiển thị (dù rỗng): Hôm nay, Ngày mai, Tuần này, Quá hạn.

---

## 8. Scope query entity hệ thống

| Entity | Điều kiện lọc | Source | Loại trừ status |
|--------|---------------|--------|-----------------|
| Task | `assignee_id = user_id` | assigned | DRAFT(1), DONE(8), CANCELLED(9) |
| Issue | `assignee_id = user_id` | assigned | closed, completed, rejected |
| AssignJob | status = DA_DUYET, user là thành viên qua `employee_info_id` | assigned | — |
| AssignRequest | type = PHIEU_CONG_TAC, status = DA_LAP_PHIEU_CONG_TAC, user là thành viên | assigned | — |
| Meeting | status IN [LEN_LICH, CHOT_LICH], user là `company_members` (qua Employee.id) | participant | DANG_TAO, HOAN_THANH, HUY |
| Personal Todo | `user_id = auth_user_id`, `parent_id IS NULL` | personal | — |

### Status mapping

#### Task

| Status | Text | Color |
|--------|------|-------|
| 1 | Nháp | secondary |
| 2 | Chờ duyệt | warning |
| 3 | Cần làm | info |
| 4 | Đang làm | primary |
| 5 | Tạm dừng | secondary |
| 6 | Review | info |
| 7 | Từ chối | danger |
| 8 | Hoàn thành | success |
| 9 | Huỷ | secondary |
| 10 | Từ chối bắt đầu | danger |

#### Issue

| Status | Text | Color |
|--------|------|-------|
| new | Mới | info |
| assigned | Đã giao | primary |
| in_progress | Đang xử lý | warning |
| resolved | Đã xử lý | success |
| closed | Đã đóng | secondary |
| reopened | Mở lại | warning |
| completed | Hoàn thành | success |
| rejected | Từ chối | danger |

#### Meeting

| Status | Text | Color |
|--------|------|-------|
| DANG_TAO | Đang tạo | secondary |
| LEN_LICH | Lên lịch | success |
| CHOT_LICH | Chốt lịch | success |
| HOAN_THANH | Hoàn thành | success |
| HUY | Hủy | secondary |

#### AssignJob

| Status | Text | Color |
|--------|------|-------|
| DANG_TAO | Đang tạo | secondary |
| CHO_DUYET | Chờ duyệt | warning |
| DA_DUYET | Đã duyệt | success |
| TU_CHOI | Từ chối | danger |
| DA_NHAP_KET_QUA | Đã nhập KQ | info |
| DA_DUYET_KET_QUA | Đã duyệt KQ | success |

#### AssignRequest (Phiếu công tác)

| Status | Text | Color |
|--------|------|-------|
| DANG_TAO | Đang tạo | secondary |
| CHO_DUYET | Chờ duyệt | warning |
| DA_DUYET | Đã duyệt | success |
| DA_LAP_PHIEU_CONG_TAC | Đã lập phiếu CT | info |
| DA_NHAP_KET_QUA | Đã nhập KQ | info |
| KHONG_DUYET | Không duyệt | danger |
| DA_DUYET_KET_QUA | Đã duyệt KQ | success |

#### Personal Todo

| Trạng thái | Text | Color |
|------------|------|-------|
| is_completed = 0 | Việc cần làm | secondary |
| is_completed = 1 | Hoàn thành | success |

### Role mapping

| Source | Text | Color | Background |
|--------|------|-------|-----------|
| assigned | Được giao | #4a7cfb | #EFF6FF |
| participant | Tham gia | #22c55e | #F0FDF4 |
| approver | Cần duyệt | #d4a03c | #FFFBEB |
| watching | Theo dõi | #8b5cf6 | #F5F3FF |
| personal | Cá nhân | #6b7280 | #F3F4F6 |

---

## 9. Non-functional Requirements

- **Performance:** Eager loading cho relationships, chỉ SELECT các trường cần thiết
- **Security:** JWT auth, dữ liệu cô lập theo `user_id`, không cần phân quyền đặc biệt
- **Compatibility:** PHP 7.4, Laravel 8, Nuxt 2, Vue 2, Bootstrap-Vue 2.15
- **Browser:** Chrome, Firefox, Safari, Edge
- **UX:** Optimistic update cho drag-drop (cập nhật UI ngay, rollback nếu API lỗi)

---

## 10. Phụ lục

### 10.1. File references

| Layer | File path |
|-------|-----------|
| Migration | `Modules/Assign/Database/Migrations/2026_04_30_000001_create_personal_todo_lists_table.php` |
| Migration | `Modules/Assign/Database/Migrations/2026_04_30_000002_create_personal_todos_table.php` |
| Entity | `Modules/Assign/Entities/MyTodo/PersonalTodoList.php` |
| Entity | `Modules/Assign/Entities/MyTodo/PersonalTodo.php` |
| Controller | `Modules/Assign/Http/Controllers/Api/V1/MyTodoController.php` |
| Service | `Modules/Assign/Services/MyTodo/MyTodoService.php` |
| Request | `Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoListRequest.php` |
| Request | `Modules/Assign/Http/Requests/MyTodo/UpdatePersonalTodoListRequest.php` |
| Request | `Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoRequest.php` |
| Request | `Modules/Assign/Http/Requests/MyTodo/UpdatePersonalTodoRequest.php` |
| Resource | `Modules/Assign/Transformers/MyTodoResource/PersonalTodoListResource.php` |
| Resource | `Modules/Assign/Transformers/MyTodoResource/PersonalTodoResource.php` |
| Resource | `Modules/Assign/Transformers/MyTodoResource/MyTodoItemResource.php` |
| Routes | `Modules/Assign/Routes/api.php` (group `/assign/my-todo`) |
| FE Page | `pages/assign/my-todo/index.vue` |
| FE Component | `pages/assign/my-todo/components/TodoFilterBar.vue` |
| FE Component | `pages/assign/my-todo/components/TodoGroupHeader.vue` |
| FE Component | `pages/assign/my-todo/components/TodoItem.vue` |
| FE Component | `pages/assign/my-todo/components/TodoSubItem.vue` |
| FE Component | `pages/assign/my-todo/components/TodoMainList.vue` |
| FE Component | `pages/assign/my-todo/components/TodoCalendarSidebar.vue` |
| FE Component | `pages/assign/my-todo/components/TodoFormModal.vue` |
| FE Component | `pages/assign/my-todo/components/TodoListDetail.vue` |
| FE Component | `pages/assign/my-todo/components/TodoListFormModal.vue` |
| Sidebar | `components/assign-components/assign-slidebar.vue` |
| Design | `pages/assign/my-todo/pencil-new.pen` |
