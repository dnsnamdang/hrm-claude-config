# Task Status Notification — Tóm tắt

## Mục tiêu
Bổ sung thông báo SelfNotification (module Human) khi task thay đổi trạng thái, gửi đúng đối tượng liên quan.

## Scope
- 7 loại trigger thông báo (8 case) theo bảng spec
- Dùng hệ thống SelfNotifications + SelfNotificationRecipient có sẵn
- Gửi ngay khi status thay đổi, không queue/cron
- Link điều hướng: `/assign/tasks?open_task={task_id}`

## Quyết định lớn
- **Kênh**: SelfNotification (bảng `self_notifications` + `self_notification_recipients`) — KHÔNG dùng `EmployeeInfoService::sendToAllNotification` (push realtime)
- **Vị trí code**: Bổ sung method mới trong `TaskService.php`, gọi từ `handleStatusNotification()`
- **Loại trừ actor**: Không gửi thông báo cho chính người thực hiện hành động

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-07-task-status-notification-design.md`

## Phụ trách
@khoipv
