# Plan — Overdue Task Unified Predicate

Spec: [docs/superpowers/specs/2026-04-21-overdue-task-unified-predicate-design.md](../../docs/superpowers/specs/2026-04-21-overdue-task-unified-predicate-design.md)

## Phase 1 — BE: Helper

- [x] Thêm `scopeOverdue` vào `Modules/Assign/Entities/Task/Task.php` (gần `listInProgress`)

## Phase 2 — BE: Áp scope

- [x] Refactor `TaskController::index` — thay khối count bằng `->overdue()->count()`
- [x] Sửa `SolutionService::getCategoriesWithLateTasks` — `withCount` closure + preload `with('tasks')` closure dùng `->overdue()`
- [x] Sửa `SolutionService::getPeopleWithLateTasks` — giữ filter `solution_id` + `->overdue()` ở 2 closure
- [x] Sửa `SolutionModuleService::getPeopleWithLateTasks` — giữ filter `solution_module_id` + `->overdue()` ở 2 closure
- [x] Dọn biến `$now` không còn dùng trong từng hàm

### Checkpoint — 2026-04-21
Vừa hoàn thành: Phase 1 + 2 code DONE (5 file Edit + lint pass). Verify grep: 7 lần gọi `->overdue()` đúng spec; các chỗ còn `listInProgress` đều ngoài scope (đếm task đang làm/upcoming).
Đang làm dở: chờ review-dns + Phase 3 manual test.
Bước tiếp theo: Dispatch review-dns → user test UI theo 7 case Phase 3.
Blocked: không.

## Phase 3 — Manual test (user)

- [ ] Task status=10 quá hạn được đếm ở popup + card Overview
- [ ] Task due_date=hôm nay + due_time quá → đếm trễ
- [ ] Task due_date=hôm nay + due_time=null → không trễ trong ngày
- [ ] Task due_date=null / status=1,8,9 → không đếm
- [ ] Card Overview khớp `meta.total` popup
- [ ] Màn Solution Module kiểm popup Nhân sự nhiều task trễ tương tự
