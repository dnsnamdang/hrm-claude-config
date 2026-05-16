# My To Do — Spec Chi Tiet

## 1. Tong quan

**Muc tieu:** Tao trang "My To Do" giup user quan ly cong viec ca nhan theo thoi gian, tich hop du lieu tu nhieu module trong HRM.

**Vi tri:** `/assign/my-todo` trong module Assign, menu sidebar dat o vi tri dau tien.

**Phan quyen:** Khong can. Moi user deu truy cap duoc, chi thay du lieu cua chinh minh.

**Co che du lieu:** Query truc tiep (real-time) — khong luu ban sao, khong sync. Khi user mo trang, BE query song song vao cac bang goc roi normalize ket qua tra ve.

---

## 2. Database

Chi tao **2 bang moi** cho Todo ca nhan. Entity he thong (Task, Issue, Meeting...) su dung bang da co.

### 2.1. Bang `personal_todo_lists`

| Cot | Kieu | Ghi chu |
|-----|------|---------|
| id | bigint PK auto | |
| user_id | unsignedBigInteger | Chu so huu |
| name | varchar(255) | Ten danh sach |
| description | text nullable | Mo ta danh sach |
| sort_order | int default 0 | Thu tu sap xep |
| company_id | unsignedBigInteger nullable | Convention DB |
| created_at, updated_at | timestamps | |
| created_by, updated_by | unsignedBigInteger nullable | Audit |

### 2.2. Bang `personal_todos`

| Cot | Kieu | Ghi chu |
|-----|------|---------|
| id | bigint PK auto | |
| list_id | unsignedBigInteger FK | -> personal_todo_lists.id |
| parent_id | unsignedBigInteger nullable | NULL = todo goc, co gia tri = sub-task (chi 1 cap) |
| user_id | unsignedBigInteger | Chu so huu |
| title | varchar(500) | Tieu de |
| description | text nullable | Mo ta ngan |
| due_date | date nullable | Ngay het han |
| due_time | time nullable | Gio het han |
| is_completed | tinyint default 0 | 0 = chua xong, 1 = da xong |
| completed_at | datetime nullable | Thoi diem hoan thanh |
| sort_order | int default 0 | Thu tu trong list |
| company_id | unsignedBigInteger nullable | Convention DB |
| created_at, updated_at | timestamps | |
| created_by, updated_by | unsignedBigInteger nullable | Audit |

**Ghi chu DB:**
- `parent_id` self-reference chi 1 cap (sub-task khong co sub-task con)
- Khong dung SoftDeletes theo convention
- Khong tao bang pivot file — dung bang `files` chung neu can dinh kem
- Khi user truy cap My Todo lan dau, tu dong tao 1 list "Mac dinh"

---

## 3. Backend Architecture

### 3.1. File Structure

```
Modules/Assign/
├── Entities/MyTodo/
│   ├── PersonalTodoList.php
│   └── PersonalTodo.php
├── Http/Controllers/
│   └── MyTodoController.php
├── Http/Requests/
│   ├── StorePersonalTodoListRequest.php
│   ├── UpdatePersonalTodoListRequest.php
│   ├── StorePersonalTodoRequest.php
│   └── UpdatePersonalTodoRequest.php
├── Http/Resources/
│   ├── MyTodoItemResource.php
│   ├── PersonalTodoListResource.php
│   └── PersonalTodoResource.php
├── Services/MyTodo/
│   └── MyTodoService.php
```

### 3.2. MyTodoService

```
MyTodoService.php
├── getAll(filters)              -> danh sach unified, co paginate
├── getCalendarSummary(month)    -> badge count theo ngay
├── getPersonalTodos(userId)
├── getAssignedTasks(userId)     -> task duoc giao + theo doi + can duyet
├── getAssignedIssues(userId)    -> issue duoc giao + theo doi + can duyet
├── getUpcomingMeetings(userId)  -> meeting user tham gia
├── getPendingApprovals(userId)  -> phieu can duyet (AssignRequest, JobRequest)
└── normalizeItem(entity, type, source) -> chuan hoa ve format chung
```

**Logic `getAll()`:**
1. Goi tat ca method con song song (hoac tuan tu)
2. Merge ket qua vao 1 collection
3. Ap filter (type, source, date_range, is_completed, is_overdue, list_id)
4. Sort theo `due_date` ASC (null cuoi cung)
5. Paginate tren collection (cursor-based hoac simple paginate)
6. Tra ve kem `calendar_summary` va `lists`

### 3.3. API Endpoints

#### Unified list
| Method | URI | Mo ta |
|--------|-----|-------|
| GET | `/assign/my-todo` | Danh sach unified + calendar + lists |

**Query params:**

| Param | Kieu | Mo ta |
|-------|------|-------|
| type | string nullable | `task,issue,meeting,request,personal` |
| source | string nullable | `assigned,watching,approver,personal` |
| date_from | date nullable | Tu ngay |
| date_to | date nullable | Den ngay |
| is_completed | boolean nullable | Loc hoan thanh/chua |
| is_overdue | boolean nullable | Loc qua han |
| list_id | int nullable | Loc theo danh sach todo ca nhan |
| month | string nullable | `YYYY-MM` — lay calendar summary |

#### CRUD Personal Todo Lists
| Method | URI | Mo ta |
|--------|-----|-------|
| GET | `/assign/my-todo/lists` | Danh sach tat ca lists |
| POST | `/assign/my-todo/lists` | Tao list moi |
| PUT | `/assign/my-todo/lists/{id}` | Sua list |
| DELETE | `/assign/my-todo/lists/{id}` | Xoa list (xoa ca todos ben trong) |

#### CRUD Personal Todos
| Method | URI | Mo ta |
|--------|-----|-------|
| GET | `/assign/my-todo/lists/{listId}/todos` | Todos trong 1 list |
| POST | `/assign/my-todo/todos` | Tao todo moi |
| PUT | `/assign/my-todo/todos/{id}` | Sua todo |
| PATCH | `/assign/my-todo/todos/{id}/toggle` | Toggle hoan thanh |
| DELETE | `/assign/my-todo/todos/{id}` | Xoa todo |
| PATCH | `/assign/my-todo/todos/reorder` | Sap xep lai thu tu |

### 3.4. Response Format — GET /assign/my-todo

```json
{
  "items": [
    {
      "type": "task",
      "id": 123,
      "title": "Hoan thanh bao cao tien do Q1",
      "due_date": "2026-05-01",
      "due_time": "17:00",
      "status_text": "Dang lam",
      "status_color": "warning",
      "source": "assigned",
      "source_text": "Duoc giao",
      "url": "/assign/task/123",
      "priority": 2,
      "priority_text": "Cao",
      "project_name": "DA Nha may ABC",
      "assignee_name": "Nguyen Van A"
    },
    {
      "type": "personal",
      "id": 67,
      "title": "Goi dien nha cung cap thep",
      "due_date": "2026-05-01",
      "due_time": null,
      "status_text": "Chua xong",
      "status_color": "secondary",
      "source": "personal",
      "source_text": "Ca nhan",
      "url": null,
      "list_id": 1,
      "list_name": "Viec can lam",
      "sub_items": [
        { "id": 68, "title": "Hoi gia", "is_completed": false },
        { "id": 69, "title": "Gui email", "is_completed": true }
      ]
    }
  ],
  "calendar_summary": {
    "2026-05-01": 3,
    "2026-05-02": 1,
    "2026-05-05": 5
  },
  "lists": [
    { "id": 1, "name": "Viec can lam", "description": "...", "todo_count": 5 },
    { "id": 2, "name": "Follow up", "description": "...", "todo_count": 2 }
  ]
}
```

### 3.5. Response Format — GET /assign/my-todo/lists/{listId}/todos

```json
{
  "list": {
    "id": 1,
    "name": "Viec can lam",
    "description": "viec hang ngay, goi NCC, gui bao gia, check email..."
  },
  "todos": [
    {
      "id": 67,
      "title": "Goi dien nha cung cap thep",
      "description": null,
      "due_date": "2026-05-01",
      "due_time": null,
      "is_completed": false,
      "completed_at": null,
      "sort_order": 0,
      "sub_items": [
        { "id": 68, "title": "Hoi bao gia thep cuon", "is_completed": true, "completed_at": "2026-04-30 10:00:00" },
        { "id": 69, "title": "Gui email xac nhan don hang", "is_completed": false },
        { "id": 70, "title": "Lich hen gap mat 03/05", "is_completed": false }
      ]
    }
  ],
  "stats": {
    "total": 7,
    "completed": 2,
    "pending": 5
  }
}
```

---

## 4. Scope — Dieu kien query tung entity

### 4.1. Task (Modules/Assign)

| Vai tro | Dieu kien |
|---------|-----------|
| Duoc giao | `assignee_id = auth_user_id` |
| Theo doi | `task_watchers` pivot co `employee_id = auth_user_id` |
| Can duyet | `approver_id = auth_user_id` AND `status = PENDING_APPROVAL (2)` |

**Loai tru status:** DONE (8), CANCELLED (9), DRAFT (1)

### 4.2. Issue (Modules/Assign)

| Vai tro | Dieu kien |
|---------|-----------|
| Duoc giao | `assignee_id = auth_user_id` |
| Theo doi | `issue_watchers` pivot co `employee_id = auth_user_id` |
| Can duyet | `approver_id = auth_user_id` AND status cho duyet |

**Loai tru status:** closed, completed, rejected

### 4.3. Meeting (Modules/Assign)

| Vai tro | Dieu kien |
|---------|-----------|
| Tham gia | `meeting_employees` co `employee_id = auth_user_id` |

**Loai tru status:** DANG_TAO (0), HOAN_THANH (3), HUY (4)
**Chi hien:** status LEN_LICH (1) va CHOT_LICH (2), tu hom nay tro di

### 4.4. AssignRequest — Phieu de xuat + Phieu cong tac (Modules/Assign)

| Vai tro | Dieu kien |
|---------|-----------|
| Can duyet | `approver = auth_user_id` AND `status = CHO_DUYET (2)` |

**Loai tru:** DANG_TAO (1), cac status da ket thuc

### 4.5. JobRequest — Phieu de xuat cong viec (Modules/Assign)

| Vai tro | Dieu kien |
|---------|-----------|
| Can duyet | `approver = auth_user_id` AND `status = CHO_DUYET (2)` |

**Loai tru:** DANG_TAO (1), cac status da ket thuc

### 4.6. Personal Todo

| Vai tro | Dieu kien |
|---------|-----------|
| Ca nhan | `user_id = auth_user_id` |

---

## 5. Normalize Mapping

| Truong chung | Task | Issue | Meeting | AssignRequest | PersonalTodo |
|-------------|------|-------|---------|---------------|-------------|
| type | "task" | "issue" | "meeting" | "request" | "personal" |
| title | name | title | name | code + " — " + title | title |
| due_date | due_date | due_date | start_date | deadline | due_date |
| due_time | due_time | due_time | start_time | null | due_time |
| status_text | map tu status | map tu status | map tu status | map tu status | Chua xong/Da xong |
| source | assigned/watching/approver | assigned/watching/approver | participant | approver | personal |
| url | /assign/task/{id} | /assign/issue/{id} | /assign/meeting/{id} | /assign/request/{id} | null |

---

## 6. Frontend Architecture

### 6.1. File Structure

```
pages/assign/my-todo/
├── index.vue                         -> Trang chinh
├── components/
│   ├── TodoMainList.vue              -> Danh sach chinh (cot trai)
│   ├── TodoItem.vue                  -> 1 item (system + personal)
│   ├── TodoSubItem.vue               -> Sub-task cua personal todo
│   ├── TodoCalendarSidebar.vue       -> Mini calendar (cot phai)
│   ├── TodoFilterBar.vue             -> Thanh filter
│   ├── TodoListManager.vue           -> Quan ly danh sach ca nhan
│   ├── TodoListDetail.vue            -> Man chi tiet 1 danh sach
│   ├── TodoFormModal.vue             -> Modal tao/sua todo ca nhan
│   ├── TodoListFormModal.vue         -> Modal tao/sua danh sach
│   └── TodoGroupHeader.vue           -> Header nhom (Hom nay, Ngay mai...)
```

### 6.2. Layout — Man chinh (index.vue)

```
+----------------------------------------------------------+
| Topbar: My To Do                        [Tim kiem] [+ Tao todo] |
+----------------------------------------------------------+
| Stats: 2 qua han | 5 hom nay | 8 tuan nay | 3 can duyet |
| Filter: [Loai v] [Vai tro v] [Trang thai v]              |
+--------------------------------------+-------------------+
|                                      | Calendar thang 5  |
| QUA HAN (2)                          | [<] Thang 5 [>]   |
| | Task: Bao cao tien do Q1   28/04   | [lich voi dot]    |
| | Issue: Bug #45             29/04   |                   |
|                                      | DANH SACH CA NHAN |
| HOM NAY (5)                          | * Viec can lam (5)|
| | Task: Review PR            17:00   | * Follow up    (2)|
| | Meeting: Hop dong bo       14:00   | * Y tuong      (3)|
| | Phieu: PCT-2026-00123      Hom nay | [+ Tao danh sach] |
| | Task: Cap nhat tai lieu    30/04   |                   |
| | Todo: Goi dien NCC         30/04   |                   |
|   [x] Hoi bao gia                   |                   |
|   [ ] Gui email xac nhan            |                   |
|   [ ] Lich hen gap mat 03/05        |                   |
|                                      |                   |
| NGAY MAI (2)                         |                   |
| ...                                  |                   |
+--------------------------------------+-------------------+
```

### 6.3. Layout — Man chi tiet danh sach (TodoListDetail.vue)

Khi click vao 1 danh sach ca nhan (vd: "Viec can lam"):

```
+----------------------------------------------------------+
| Topbar: My To Do > Viec can lam           [Xoa list] [+ Tao todo] |
+----------------------------------------------------------+
| Viec can lam                                             |
| Mo ta: viec hang ngay, goi NCC, gui bao gia...    [Sua] |
+--------------------------------------+-------------------+
| DANH SACH VIEC        [Bo loc] [Them]| Calendar thang 5  |
|                                      |                   |
| [x] Check email sang              -- | [lich]            |
| [ ] Goi NCC thep — hoi bao gia  29/04|                   |
|   * Da lien lac                      |                   |
| [ ] Gui bao gia cho KH Minh Phat -- |                   |
| [ ] Kiem tra tien kho vat tu     -- |                   |
| [ ] Cap nhat bang chien cong tuan 20/04|                  |
| [ ] Gui email xac nhan don hang  23/04|                   |
|   * Dang xuong                       |                   |
|                                      |                   |
| + Them viec moi vao danh sach...     |                   |
+--------------------------------------+-------------------+
```

### 6.4. Nhom thoi gian (man chinh)

| Thu tu | Nhom | Dieu kien |
|--------|------|-----------|
| 1 | Qua han | `due_date < today` AND `is_completed = false` — highlight do |
| 2 | Hom nay | `due_date = today` |
| 3 | Ngay mai | `due_date = tomorrow` |
| 4 | Tuan nay | `due_date` trong tuan hien tai (tru hom nay/mai) |
| 5 | Tuan sau | tuan ke tiep |
| 6 | Sap toi | xa hon tuan sau |
| 7 | Khong co deadline | `due_date = null` |

### 6.5. Phan biet visual theo loai

| Loai | Mau thanh trai | Tag text |
|------|---------------|----------|
| Task | #4A7CFB (xanh duong) | "Task" |
| Issue | #E25C5C (do) | "Issue" |
| Meeting | #5BBFCF (xanh lam) | "Cuoc hop" |
| Phieu duyet | #D4A03C (vang) | "Phieu duyet" |
| Todo ca nhan | #B0B8C1 (xam) | "Ca nhan" |

### 6.6. Tuong tac

| Hanh dong | Loai | Cach hoat dong |
|-----------|------|----------------|
| Click item he thong | Task/Issue/Meeting/Request | Navigate sang URL chi tiet |
| Click todo ca nhan | Personal | Mo inline edit |
| Check/uncheck todo | Personal | PATCH toggle, animation strike-through |
| Check/uncheck sub-item | Personal | PATCH toggle, cap nhat progress parent |
| Click ngay tren calendar | Calendar | Filter danh sach theo ngay do |
| Click ngay trong tren calendar | Calendar | Mo modal tao todo voi deadline = ngay do |
| Click danh sach ca nhan | Sidebar | Chuyen sang man chi tiet danh sach (TodoListDetail) |
| Drag & drop todo | Personal | Reorder, PATCH reorder API |

---

## 7. UI Mockup

Thiet ke chi tiet da duoc tao tren Pencil:
- Man 1: "My To Do - Redesign" — trang chinh
- Man 2: "Viec can lam - List View" — man chi tiet danh sach ca nhan

---

## 8. Edge Cases

1. **User chua co danh sach nao** — tu dong tao 1 list "Mac dinh" khi user truy cap My Todo lan dau
2. **Xoa danh sach** — xoa ca todos ben trong, hien confirm dialog truoc khi xoa
3. **Todo khong co deadline** — xep vao nhom "Khong co deadline" cuoi danh sach
4. **Entity he thong bi xoa** — khong hien tren My Todo (vi query truc tiep, tu dong bien mat)
5. **Nhieu vai tro** — neu user vua la assignee vua la watcher cua 1 task, chi hien 1 lan voi source uu tien: assigned > approver > watching
6. **Performance** — su dung eager loading, chi SELECT cac truong can thiet, cache Redis 1-2 phut cho calendar_summary
7. **Sub-task chi 1 cap** — khong cho tao sub-task cua sub-task
