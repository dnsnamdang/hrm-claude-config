# Spec — Đồng nhất predicate "task trễ" trong module Giao việc

**Ngày:** 2026-04-21
**Người phụ trách:** @manhcuong
**Feature folder:** `.plans/overdue-task-unified-predicate/`

---

## 1. Bối cảnh & vấn đề

Tại màn `/assign/solutions/{id}/manager` tab **Tổng quan**, popup "Hạng mục nhiều task trễ" và "Nhân sự nhiều task trễ" đang đếm số task trễ (`late_tasks_count`) theo một logic **khác** với logic `overdue_total` ở tab **Task**. Hệ quả: số hạng mục/nhân sự trên card Overview lệch với số task trễ hiển thị ở tab Task, gây khó hiểu.

Tương tự tồn tại ở màn `/assign/solution-modules/{id}` (popup "Nhân sự nhiều task trễ").

### So sánh 2 logic

| Tiêu chí | Tab Task (`overdue_total`) — đúng | Popup late tasks — sai |
|---|---|---|
| Status loại trừ | `NOT IN [1, 8, 9]` → gồm `[2,3,4,5,6,7,10]` | `IN Task::listInProgress()` = `[2,3,4,5,6,7]` — **thiếu status 10 (Từ chối triển khai)** |
| So sánh deadline | `CONCAT(due_date, ' ', COALESCE(due_time, '23:59:59')) < NOW()` | `due_date < NOW()` — **bỏ qua `due_time`** |
| Null due_date | `whereNotNull('due_date')` tường minh | Ngầm loại bởi `<` |

### Constant status (Task)

```
DRAFT = 1, PENDING_APPROVAL = 2, TODO = 3, IN_PROGRESS = 4,
PAUSED = 5, REVIEW = 6, REJECTED = 7, DONE = 8, CANCELLED = 9, REJECTED_START = 10
```

---

## 2. Mục tiêu

Có **1 định nghĩa duy nhất** cho "task trễ" trong module Giao việc, dùng lại ở mọi nơi cần đếm/lọc task trễ. Áp dụng đồng bộ cho cả Solution và Solution Module.

---

## 3. Giải pháp

### 3.1 Thêm local scope `overdue` trên `Task` entity

**File:** `hrm-api/Modules/Assign/Entities/Task/Task.php`

Vị trí: đặt gần `public static function listInProgress()` (gần dòng 464).

```php
/**
 * Scope: task đang quá hạn
 * Đồng nhất với logic overdue_total ở tab Task (TaskController::index)
 * - due_date NOT NULL
 * - status NOT IN (Nháp, Hoàn thành, Huỷ) → bao gồm cả REJECTED_START
 * - CONCAT(due_date, due_time) < now() với due_time fallback 23:59:59
 */
public function scopeOverdue($query)
{
    return $query->whereNotNull('tasks.due_date')
        ->whereNotIn('tasks.status', [self::DRAFT, self::DONE, self::CANCELLED])
        ->whereRaw(
            "CONCAT(tasks.due_date, ' ', COALESCE(tasks.due_time, '23:59:59')) < ?",
            [now()->toDateTimeString()]
        );
}
```

**Lưu ý:** dùng prefix `tasks.` để tránh ambiguous khi scope được gọi trong closure `withCount` (Eloquent giữ alias bảng là `tasks`). Khi gọi trực tiếp `Task::overdue()` không join bảng khác vẫn chạy đúng vì bảng gốc là `tasks`.

### 3.2 Refactor TaskController::index

**File:** `hrm-api/Modules/Assign/Http/Controllers/Api/V1/TaskController.php` (dòng 35-39)

**Trước:**
```php
$overdueTotal = (clone $result)
    ->whereNotNull('tasks.due_date')
    ->whereNotIn('tasks.status', [1, 8, 9])
    ->whereRaw("CONCAT(tasks.due_date, ' ', COALESCE(tasks.due_time, '23:59:59')) < ?", [now()->toDateTimeString()])
    ->count();
```

**Sau:**
```php
$overdueTotal = (clone $result)->overdue()->count();
```

### 3.3 Áp scope trong SolutionService

**File:** `hrm-api/Modules/Assign/Services/SolutionService.php`

#### 3.3.1 `getCategoriesWithLateTasks` (dòng ~957)

- Thay closure `withCount['tasks as late_tasks_count']` (dòng 972-975): chỉ còn `$q->overdue()`
- Thay closure `with('tasks' => ...)` (dòng 983-986): chỉ còn `$q->overdue()`
- Bỏ biến `$now = Carbon::now()` nếu không còn ref khác (kiểm tra trong hàm)

#### 3.3.2 `getPeopleWithLateTasks` (dòng ~1031)

- Thay closure `withCount` (dòng 1043-1047): giữ `->where('solution_id', $solution->id)` + `->overdue()`
- Thay closure `with('tasks' => ...)` (dòng 1060-1064): giữ `->where('solution_id', $solution->id)` + `->overdue()`
- Bỏ biến `$now` nếu không còn ref

### 3.4 Áp scope trong SolutionModuleService

**File:** `hrm-api/Modules/Assign/Services/SolutionModuleService.php`

#### 3.4.1 `getPeopleWithLateTasks` (dòng ~363)

- Thay closure `withCount` (dòng 375-379): giữ `->where('solution_module_id', $solutionModule->id)` + `->overdue()`
- Thay closure `with('tasks' => ...)` (dòng 392-396): giữ `->where('solution_module_id', $solutionModule->id)` + `->overdue()`
- Bỏ biến `$now` nếu không còn ref (lưu ý `getTaskUpcomingSchedule` ở cùng file vẫn dùng `$now` → scope theo hàm)

### 3.5 Các file KHÔNG đổi

- `IssueController.php` — Issue có bảng riêng, status string (`'resolved'`, `'closed'`), logic sẵn đã đúng; scope `overdue` của Task không áp được.
- `SolutionModuleService::getTaskUpcomingSchedule` — nghiệp vụ "sắp tới hạn" dùng range `>= now && <= daysLater`, khác nghiệp vụ.
- FE: không đổi. Card Overview lấy `meta.total` từ list endpoint → tự động đồng bộ.

---

## 4. Thay đổi hành vi (user-visible)

Sau khi áp dụng:

1. **Task status 10 (Từ chối triển khai) quá hạn** → giờ được đếm vào `late_tasks_count`. Trước đây bị bỏ ở popup/card nhưng vẫn được đếm ở tab Task → là bug fix.
2. **Task `due_date = hôm nay`, `due_time = 17:00`** — khi chạy lúc 18:00 → đếm là trễ (trước đây chỉ đếm từ ngày kế tiếp).
3. **Task `due_date = hôm nay`, `due_time = NULL`** — fallback `23:59:59`, chỉ trễ sau khi qua ngày (giữ nguyên hành vi cũ).

**Hệ quả:** `late_tasks_count` và `meta.total` có thể tăng. Card Overview "Hạng mục nhiều task trễ" / "Nhân sự nhiều task trễ" có thể hiển thị nhiều mục hơn.

---

## 5. Edge case

- **Query alias trong withCount**: Laravel tạo subquery với alias `tasks` (tên bảng gốc). Prefix `tasks.` trong scope chạy đúng. Đã verify qua pattern hiện tại trong `TaskController::index` (dùng y hệt `tasks.due_date`, `tasks.status`).
- **Sort theo `late_tasks_count`**: alias sinh từ `withCount(['tasks as late_tasks_count'])` — scope chạy bên trong closure không ảnh hưởng alias ngoài, `orderBy('late_tasks_count', ...)` vẫn hoạt động.
- **`having` theo `late_tasks_count`**: tương tự trên, không ảnh hưởng.
- **Không cần migration, không đổi API contract (cùng shape response), không đổi FE.**

---

## 6. Test

**Tự động (không yêu cầu):** dự án hiện tại không có unit test, không bắt buộc viết thêm.

**Manual test (UI — end-user view):**

| # | Chuẩn bị dữ liệu | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| 1 | Tạo 1 task status=10 (REJECTED_START), due_date = hôm qua | Vào tab Task đếm `overdue_total` → ghi nhận N; mở popup "Hạng mục nhiều task trễ" | Số task trễ của hạng mục chứa task này tăng 1 so với trước fix |
| 2 | Task due_date=hôm nay, due_time=10:00, chạy test lúc sau 10:00 | Mở popup Category / People | Task được đếm là trễ |
| 3 | Task due_date=hôm nay, due_time=null | Mở popup | Không đếm là trễ (chỉ trễ sau 00:00 ngày mai) |
| 4 | Task due_date=null | Mở popup | Không đếm |
| 5 | Task status=1/8/9 (Nháp/Done/Cancelled) quá hạn | Mở popup | Không đếm |
| 6 | Vào card Overview, đọc số "Hạng mục nhiều task trễ" | So với `meta.total` của popup | Khớp nhau |
| 7 | Màn Solution Module: popup "Nhân sự nhiều task trễ" | Kiểm các case 1-5 tương tự | Khớp logic tab Task của module |

---

## 7. Downstream impact

- **Notify task report** (feature đã merged, `.plans/notify-task-report/`) — dùng logic riêng, không đụng tới file này.
- **Báo cáo QLDA_BC_*** — không gọi 3 hàm bị sửa, không đụng.
- Mọi chỗ khác gọi `Task::listInProgress()` + `due_date < $now` để đếm task trễ: **không tìm thấy thêm chỗ nào** (đã grep toàn bộ `Modules/Assign`). Nếu phát sinh trong tương lai → dùng `->overdue()`.

---

## 8. Rollout

- Deploy BE cùng 1 release, không cần feature flag.
- Không cần migration.
- Không cần thông báo user — thay đổi là bug fix đồng nhất số liệu.
