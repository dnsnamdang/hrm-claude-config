# Issue Completion Flow — Plan

**Người phụ trách:** @khoipv

## Phase 1: Backend — Schema + Entity

- [x] Task 1: Migration thêm `completed_at`, `rejected_at`, `rejected_reason` vào bảng `issues`
- [x] Task 2: Thêm const `STATUS_COMPLETED`, `STATUS_REJECTED` + STATUS_DATA vào `Issue.php`
- [x] Task 3: Thêm `completed_at`, `rejected_at`, `rejected_reason` vào `$fillable` + `$casts`
- [x] Task 4: Thêm helper `isApprover()`, `hasApprover()`
- [x] Task 5: Cập nhật `canEdit()` — block khi status = completed
- [x] Task 6: Cập nhật `canHandle()` — cho phép approver ở status resolved

## Phase 2: Backend — Transition logic

- [x] Task 7: Cập nhật `getAllowedNextStatuses()` — branching logic theo has/no approver
- [x] Task 8: Cập nhật `IssueService::changeStatus()` — handle timestamp cho completed/rejected + clear rejected khi re-open
- [x] Task 9: Cập nhật `IssueService::update()` — status change detection + timestamp handling (vì FE dùng form save)
- [x] Task 10: Cập nhật `IssueUpdateStatusRequest` — validate reason required khi rejected

## Phase 3: Backend — Resource + Controller

- [x] Task 11: Cập nhật `DetailIssueResource` — thêm fields + ENUM_MAPS + DATE_FIELDS
- [x] Task 12: Cập nhật `IssueController::index()` — thêm completed vào overdue exclusion

## Phase 4: Backend — Notification

- [x] Task 13: Thêm `notifyApproverForReview()` — gửi thông báo cho approver khi issue resolved
- [x] Task 14: Thêm `notifyAssigneeRejected()` — gửi thông báo cho assignee khi bị từ chối
- [x] Task 15: Gọi notification từ cả `changeStatus()` và `update()`

## Phase 5: Frontend

- [x] Task 16: Cập nhật `index.vue` — thêm completed/rejected vào statusOptions, getStatusLabel, getStatusStyle, overdue exclusion
- [x] Task 17: Cập nhật `CreateIssueModal.vue` — thêm color/label, rejected_reason display/input, validation, payload

## Phase 6: Test thủ công

- [x] Task 18: Test flow KHÔNG có approver: `new` → `assigned` → `in_progress` → `completed` → `reopened`
- [x] Task 19: Test flow CÓ approver: `in_progress` → `resolved` → `completed`
- [x] Task 20: Test flow CÓ approver bị từ chối: `resolved` → `rejected` → `in_progress` → `resolved` → `completed`
- [x] Task 21: Test notification: approver nhận thông báo khi resolved, assignee nhận thông báo khi rejected
- [x] Task 22: Test creator đóng issue từ các trạng thái (closed), test reopened từ completed/closed

### Checkpoint — 2026-04-28
Hoàn thành: 22/22 task. Feature Issue Completion Flow đã test thủ công xong, hoạt động đúng.
