# Task Status Notification — Implementation Plan

**Goal:** Gửi thông báo khi task đổi trạng thái, theo spec `docs/superpowers/specs/2026-05-07-task-status-notification-design.md`

**Phụ trách:** @khoipv

---

## Phase 1: Backend — Đã có sẵn

Code đã implement trong `TaskService.php`:

- `sendTaskNotification()` (line 1052): gửi push notification qua `EmployeeInfoService::sendToAllNotification`
- `handleStatusNotification()` (line 1068): xử lý 8 case theo spec
- `getEmployeeInfoId()` (line 1045): lấy employee_info_id từ employee_id

### Task 1: 8 case thông báo

- [x] Case TODO (từ PENDING_APPROVAL): gửi cho assignee
- [x] Case TODO (tạo mới, created_by ≠ assignee): gửi cho assignee
- [x] Case PENDING_APPROVAL: gửi cho tất cả user có quyền 'Duyệt triển khai task'
- [x] Case REJECTED_START từ PENDING_APPROVAL: gửi cho created_by
- [x] Case REJECTED_START từ TODO: gửi cho created_by + users có quyền 'Duyệt triển khai task'
- [x] Case REVIEW: gửi cho approver_id
- [x] Case DONE (từ REVIEW): gửi cho assignee
- [x] Case REJECTED (từ REVIEW): gửi cho assignee

### Task 2: Loại trừ actor

- [x] Loại trừ người thực hiện hành động khỏi danh sách người nhận (line 1057)

## Kết luận

Dùng hệ thống push notification (Redis + FCM) hiện có, không cần thêm SelfNotification.
