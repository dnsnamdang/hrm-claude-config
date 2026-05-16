# Overdue Task Unified Predicate — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng nhất định nghĩa "task trễ" trong module Giao việc bằng cách giới thiệu local scope `Task::scopeOverdue` và áp dụng ở tất cả chỗ đếm/lọc task trễ.

**Architecture:** Thêm 1 local scope Eloquent trên `Task` entity, sau đó refactor 1 controller + 3 hàm service để cùng dùng scope này. Không thay đổi API contract, DB schema, hay FE.

**Tech Stack:** PHP 7.4, Laravel 8, Eloquent query builder.

**Spec:** `docs/superpowers/specs/2026-04-21-overdue-task-unified-predicate-design.md`

**Testing note:** Dự án không có unit test tự động. Kiểm thử bằng manual UI testing theo góc nhìn người dùng cuối (task cuối plan).

---

## File Structure

**Modify only (4 file):**
- `hrm-api/Modules/Assign/Entities/Task/Task.php` — thêm method `scopeOverdue`
- `hrm-api/Modules/Assign/Http/Controllers/Api/V1/TaskController.php` — rút gọn `index`
- `hrm-api/Modules/Assign/Services/SolutionService.php` — 2 hàm `getCategoriesWithLateTasks`, `getPeopleWithLateTasks`
- `hrm-api/Modules/Assign/Services/SolutionModuleService.php` — 1 hàm `getPeopleWithLateTasks`

---

### Task 1: Thêm scope `overdue` vào Task entity

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/Task/Task.php` (đặt ngay sau method `listInProgress` quanh dòng 467)

- [ ] **Step 1: Mở file và xác định vị trí chèn**

Chạy để xác định dòng của `listInProgress`:
```
grep -n "public static function listInProgress" hrm-api/Modules/Assign/Entities/Task/Task.php
```
Expected: khớp dòng ~464. Chèn scope mới vào sau khối `return [self::PENDING_APPROVAL, ...];` và dấu `}` đóng của `listInProgress`.

- [ ] **Step 2: Thêm method `scopeOverdue`**

Chèn ngay sau `}` đóng của `listInProgress()`:

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

- [ ] **Step 3: Kiểm tra cú pháp PHP**

Run:
```
php -l hrm-api/Modules/Assign/Entities/Task/Task.php
```
Expected: `No syntax errors detected in ...Task.php`

- [ ] **Step 4: Smoke test scope qua tinker (tuỳ chọn)**

Run:
```
cd hrm-api && php artisan tinker --execute="echo \Modules\Assign\Entities\Task\Task::overdue()->toSql();"
```
Expected: in ra chuỗi SQL chứa `where "tasks"."due_date" is not null` và `CONCAT(tasks.due_date` — nếu không có tinker thì bỏ qua.

- [ ] **Step 5: Commit**

```
git -C hrm-api add Modules/Assign/Entities/Task/Task.php
git -C hrm-api commit -m "feat(assign): add Task::scopeOverdue for unified overdue predicate"
```

---

### Task 2: Refactor `TaskController::index`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/TaskController.php:35-39`

- [ ] **Step 1: Thay khối tính `$overdueTotal`**

Tìm đoạn hiện tại (quanh dòng 35-39):

```php
        $overdueTotal = (clone $result)
            ->whereNotNull('tasks.due_date')
            ->whereNotIn('tasks.status', [1, 8, 9])
            ->whereRaw("CONCAT(tasks.due_date, ' ', COALESCE(tasks.due_time, '23:59:59')) < ?", [now()->toDateTimeString()])
            ->count();
```

Thay bằng:

```php
        $overdueTotal = (clone $result)->overdue()->count();
```

- [ ] **Step 2: Kiểm tra cú pháp**

Run:
```
php -l hrm-api/Modules/Assign/Http/Controllers/Api/V1/TaskController.php
```
Expected: `No syntax errors detected`.

- [ ] **Step 3: Commit**

```
git -C hrm-api add Modules/Assign/Http/Controllers/Api/V1/TaskController.php
git -C hrm-api commit -m "refactor(assign): TaskController::index use Task scopeOverdue"
```

---

### Task 3: Refactor `SolutionService::getCategoriesWithLateTasks`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionService.php` (quanh dòng 957-1023)

- [ ] **Step 1: Thay closure `withCount`**

Tìm khối (quanh dòng 972-975):

```php
        // Đếm số task trễ cho mỗi module (loại bỏ task đang tạo)
        $query->withCount(['tasks as late_tasks_count' => function ($q) use ($now) {
            $q->whereIn('status', Task::listInProgress())
                ->where('due_date', '<', $now);
        }]);
```

Thay bằng:

```php
        // Đếm số task trễ cho mỗi module (dùng scope Task::overdue)
        $query->withCount(['tasks as late_tasks_count' => function ($q) {
            $q->overdue();
        }]);
```

- [ ] **Step 2: Thay closure preload `with('tasks')`**

Tìm khối (quanh dòng 981-987):

```php
        // Load relationships
        $query->with([
            'leader.info',
            'tasks' => function ($q) use ($now) {
                $q->whereIn('status', Task::listInProgress())
                    ->where('due_date', '<', $now);
            },
        ]);
```

Thay bằng:

```php
        // Load relationships
        $query->with([
            'leader.info',
            'tasks' => function ($q) {
                $q->overdue();
            },
        ]);
```

- [ ] **Step 3: Dọn biến `$now` nếu không còn dùng**

Tìm dòng `$now = Carbon::now();` ở đầu hàm `getCategoriesWithLateTasks` (quanh dòng 959).

Kiểm tra trong thân hàm này còn chỗ nào dùng `$now` không:
```
grep -nE "\\\$now" hrm-api/Modules/Assign/Services/SolutionService.php
```

Nếu trong phạm vi hàm `getCategoriesWithLateTasks` không còn ref `$now` khác → xóa dòng `$now = Carbon::now();`. Nếu còn ref (ví dụ các hàm khác trong cùng file vẫn dùng) → chỉ xóa ref trong hàm này.

- [ ] **Step 4: Kiểm tra cú pháp**

Run:
```
php -l hrm-api/Modules/Assign/Services/SolutionService.php
```
Expected: `No syntax errors detected`.

- [ ] **Step 5: Commit**

```
git -C hrm-api add Modules/Assign/Services/SolutionService.php
git -C hrm-api commit -m "refactor(assign): SolutionService::getCategoriesWithLateTasks use scopeOverdue"
```

---

### Task 4: Refactor `SolutionService::getPeopleWithLateTasks`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionService.php` (quanh dòng 1031-1095)

- [ ] **Step 1: Thay closure `withCount`**

Tìm khối (quanh dòng 1043-1047):

```php
        // Đếm số task trễ của mỗi nhân viên trong solution này (loại bỏ task đang tạo)
        $query->withCount(['tasks as late_tasks_count' => function ($q) use ($now, $solution) {
            $q->where('solution_id', $solution->id)
                ->whereIn('status', Task::listInProgress())
                ->where('due_date', '<', $now);
        }]);
```

Thay bằng:

```php
        // Đếm số task trễ của mỗi nhân viên trong solution này
        $query->withCount(['tasks as late_tasks_count' => function ($q) use ($solution) {
            $q->where('solution_id', $solution->id)->overdue();
        }]);
```

- [ ] **Step 2: Thay closure preload `with('tasks')`**

Tìm khối (quanh dòng 1058-1065):

```php
        // Load relationships
        $query->with([
            'info.department',
            'tasks' => function ($q) use ($now, $solution) {
                $q->where('solution_id', $solution->id)
                    ->whereIn('status', Task::listInProgress())
                    ->where('due_date', '<', $now);
            },
        ]);
```

Thay bằng:

```php
        // Load relationships
        $query->with([
            'info.department',
            'tasks' => function ($q) use ($solution) {
                $q->where('solution_id', $solution->id)->overdue();
            },
        ]);
```

- [ ] **Step 3: Dọn biến `$now`**

Tìm `$now = Carbon::now();` ở đầu hàm `getPeopleWithLateTasks` (quanh dòng 1033). Nếu trong thân hàm này không còn dùng `$now` → xóa dòng đó.

- [ ] **Step 4: Kiểm tra cú pháp**

Run:
```
php -l hrm-api/Modules/Assign/Services/SolutionService.php
```
Expected: `No syntax errors detected`.

- [ ] **Step 5: Commit**

```
git -C hrm-api add Modules/Assign/Services/SolutionService.php
git -C hrm-api commit -m "refactor(assign): SolutionService::getPeopleWithLateTasks use scopeOverdue"
```

---

### Task 5: Refactor `SolutionModuleService::getPeopleWithLateTasks`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionModuleService.php` (quanh dòng 363-430)

- [ ] **Step 1: Thay closure `withCount`**

Tìm khối (quanh dòng 374-379):

```php
        // Đếm số task trễ của mỗi nhân viên trong hạng mục này
        $query->withCount(['tasks as late_tasks_count' => function ($q) use ($now, $solutionModule) {
            $q->where('solution_module_id', $solutionModule->id)
                ->whereIn('status', Task::listInProgress())
                ->where('due_date', '<', $now);
        }]);
```

Thay bằng:

```php
        // Đếm số task trễ của mỗi nhân viên trong hạng mục này
        $query->withCount(['tasks as late_tasks_count' => function ($q) use ($solutionModule) {
            $q->where('solution_module_id', $solutionModule->id)->overdue();
        }]);
```

- [ ] **Step 2: Thay closure preload `with('tasks')`**

Tìm khối (quanh dòng 390-397):

```php
        // Load relationships
        $query->with([
            'info.department',
            'tasks' => function ($q) use ($now, $solutionModule) {
                $q->where('solution_module_id', $solutionModule->id)
                    ->whereIn('status', Task::listInProgress())
                    ->where('due_date', '<', $now);
            },
        ]);
```

Thay bằng:

```php
        // Load relationships
        $query->with([
            'info.department',
            'tasks' => function ($q) use ($solutionModule) {
                $q->where('solution_module_id', $solutionModule->id)->overdue();
            },
        ]);
```

- [ ] **Step 3: Dọn biến `$now`**

Tìm `$now = Carbon::now();` ở đầu hàm `getPeopleWithLateTasks` (quanh dòng 365). Nếu không còn dùng trong thân hàm → xóa. **Cẩn thận:** hàm khác `getTaskUpcomingSchedule` cùng file vẫn dùng `$now` của riêng nó — không đụng tới.

- [ ] **Step 4: Kiểm tra cú pháp**

Run:
```
php -l hrm-api/Modules/Assign/Services/SolutionModuleService.php
```
Expected: `No syntax errors detected`.

- [ ] **Step 5: Commit**

```
git -C hrm-api add Modules/Assign/Services/SolutionModuleService.php
git -C hrm-api commit -m "refactor(assign): SolutionModuleService::getPeopleWithLateTasks use scopeOverdue"
```

---

### Task 6: Verify không còn chỗ nào dùng predicate cũ

**Files:** toàn bộ `hrm-api/Modules/Assign`

- [ ] **Step 1: Grep tìm pattern cũ còn sót**

Run:
```
grep -rnE "listInProgress\(\).*due_date.*<|due_date.*<.*\\\$now" hrm-api/Modules/Assign --include="*.php"
```

Expected output: chỉ còn 1 match duy nhất là `getTaskUpcomingSchedule` (dùng `due_date >= $now && <= $daysLater` — khác nghiệp vụ, ngoài scope). Nếu còn match khác liên quan "task trễ" → báo lại, không tự ý sửa.

- [ ] **Step 2: Grep tìm ref scope mới**

Run:
```
grep -rn "->overdue()" hrm-api/Modules/Assign --include="*.php"
```

Expected: đúng 5 match (1 TaskController + 2 closure SolutionService::getCategoriesWithLateTasks + 2 closure SolutionService::getPeopleWithLateTasks + 2 closure SolutionModuleService::getPeopleWithLateTasks = **7 match**). Nếu ≠ 7 → review lại tasks 2-5.

*(Sửa lại Step 2: đếm đúng là 7 lần gọi `->overdue()`: Task 2 × 1, Task 3 × 2, Task 4 × 2, Task 5 × 2.)*

---

### Task 7: Manual UI testing (user thực hiện)

**Môi trường:** `http://127.0.0.1:3000` + BE hrm-api local + DB có dữ liệu test.

**Chuẩn bị dữ liệu (trên 1 solution bất kỳ, ghi nhận solution_id = X, solution_module_id = Y):**

- Task A: status=10 (REJECTED_START), due_date = hôm qua, assignee = NV1
- Task B: status=4 (IN_PROGRESS), due_date = hôm nay, due_time = "10:00:00", assignee = NV1
- Task C: status=4, due_date = hôm nay, due_time = NULL, assignee = NV2
- Task D: status=4, due_date = NULL, assignee = NV2
- Task E: status=1 (DRAFT), due_date = hôm qua, assignee = NV3
- Task F: status=8 (DONE), due_date = hôm qua, assignee = NV3

**Thực hiện test sau thời điểm 10:01 trong ngày.**

- [ ] **Test 1: Task tab `overdue_total` bao gồm Task A và B, loại C/D/E/F**
  - Mở `/assign/solutions/X/manager` tab **Task**
  - Đọc số `overdue_total` ở badge / header

- [ ] **Test 2: Popup "Hạng mục nhiều task trễ" khớp logic**
  - Mở tab **Tổng quan** → click card "Hạng mục nhiều task trễ"
  - Hạng mục chứa Task A và B có `late_tasks_count` bao gồm cả A (status 10) và B (due_time đã qua)
  - Không đếm C (null due_time của hôm nay), D (null due_date), E (DRAFT), F (DONE)

- [ ] **Test 3: Popup "Nhân sự nhiều task trễ" khớp logic**
  - Click card "Nhân sự nhiều task trễ"
  - NV1 có `late_tasks_count` = 2 (gồm A + B)
  - NV2 không xuất hiện (hoặc `late_tasks_count` = 0 theo threshold)

- [ ] **Test 4: Card Overview khớp `meta.total` popup**
  - Số trên card "Hạng mục nhiều task trễ" ở Overview = `meta.total` của popup tương ứng
  - Số trên card "Nhân sự nhiều task trễ" = `meta.total` của popup nhân sự

- [ ] **Test 5: Màn Solution Module — popup "Nhân sự nhiều task trễ"**
  - Mở `/assign/solution-modules/Y/manager` → tab Tổng quan → popup "Nhân sự nhiều task trễ"
  - Áp dụng logic tương tự Test 3 nhưng scope theo `solution_module_id`

- [ ] **Test 6: Task C (cùng ngày, null due_time) — sau 00:00 ngày hôm sau đếm là trễ**
  - Quan sát lại popup vào ngày kế: Task C giờ xuất hiện trong `late_tasks_count`

- [ ] **Test 7: Edge case — task với `due_time = "23:59:59"` hôm nay**
  - Thêm task G: status=4, due_date=hôm nay, due_time="23:59:59"
  - Kiểm trong ngày: không đếm trễ. Sau 00:00 ngày mai: đếm trễ.

---

## Self-Review

- [x] Spec coverage: 7 task ↔ scope spec section 3 (3.1-3.4) + test section 6. 3.5 không tạo task vì là "KHÔNG đổi".
- [x] Placeholder scan: không có "TBD/TODO/handle edge cases" rời rạc; mọi step có code/command cụ thể.
- [x] Type consistency: tên scope `overdue()` dùng nhất quán xuyên suốt Task 2-6. Biến đóng (`$solution`, `$solutionModule`) giữ đúng tên theo hàm gốc.
- [x] Lưu ý Task 6 Step 2 ghi chú lại số match đúng (7 lần gọi `->overdue()`).

---

## Execution Handoff

Plan saved to `docs/superpowers/plans/2026-04-21-overdue-task-unified-predicate.md`.
