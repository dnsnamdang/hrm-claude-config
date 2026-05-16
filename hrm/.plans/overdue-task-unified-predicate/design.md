# Overdue Task — Unified Predicate

**Người phụ trách:** @manhcuong
**Spec chi tiết:** [docs/superpowers/specs/2026-04-21-overdue-task-unified-predicate-design.md](../../docs/superpowers/specs/2026-04-21-overdue-task-unified-predicate-design.md)

## Mục tiêu

Đồng nhất định nghĩa "task trễ" trong module Giao việc — chỉ dùng 1 predicate (scope Eloquent `Task::scopeOverdue`) dùng lại ở tab Task, popup "Hạng mục nhiều task trễ" và "Nhân sự nhiều task trễ" ở cả Solution và Solution Module.

## Scope

**BE (4 file):**
- `Entities/Task/Task.php` — thêm `scopeOverdue`
- `Http/Controllers/Api/V1/TaskController.php::index` — refactor dùng scope
- `Services/SolutionService.php` — `getCategoriesWithLateTasks` + `getPeopleWithLateTasks`
- `Services/SolutionModuleService.php` — `getPeopleWithLateTasks`

**FE:** không đổi (card Overview lấy `meta.total` → tự sync).

**Không trong scope:** IssueController (bảng riêng, status string), `getTaskUpcomingSchedule` (nghiệp vụ "sắp tới hạn" khác), notify cron, báo cáo.

## Quyết định lớn

- Dùng **local scope Eloquent** (`scopeOverdue`) thay vì helper static — idiom Laravel chuẩn, gọi `->overdue()` gọn, phù hợp pattern `listInProgress()` sẵn có.
- Prefix `tasks.` trong scope để an toàn khi gọi trong closure `withCount`.
- Áp đồng thời ở cả `withCount` closure và preload `with('tasks' => ...)` closure → `late_tasks_count` và danh sách task preload luôn khớp.

## Hệ quả user-visible

- Task status 10 (Từ chối triển khai) quá hạn giờ được đếm.
- Task due_date=hôm nay, due_time đã qua giờ → đếm là trễ (trước đây chỉ đếm từ ngày kế).
- Số trên card Overview và popup có thể tăng so với trước — là bug fix, không phải feature mới.
