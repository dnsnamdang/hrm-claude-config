# Elearning Notification Center — Tóm tắt thiết kế

- **Người phụ trách:** @junfoke
- **Spec chi tiết:** docs/superpowers/specs/2026-06-15-elearning-notification-center-design.md
- **Plan:** docs/superpowers/plans/2026-06-15-elearning-notification-center.md
- **Tiếp nối:** onboarding-auto-enroll (sinh noti đầu tiên).

## Mục tiêu
Biến icon chuông mock trên header elearning thành trung tâm thông báo THẬT, realtime.

## Quyết định (đã chốt với user)
- **Realtime** qua socket server có sẵn `hrm-api/server_node/server.js` (port 8891) — employee dùng cùng JWT (`elearning_token` = api JWT, sub=Employee.id) connect, nghe event `notification`. KHÔNG sửa backend socket.
- **Chỉ employee**; learner → list rỗng, không connect socket.
- **Lọc theo type**: chỉ hiện noti `data.type ∈ whitelist` (khởi đầu `['OnboardingAutoEnroll']`).

## Thành phần
**BE (Modules/Elearning):** `NotificationController` (index/markAsRead/markAllAsRead, lọc type, employee-only) + 3 route `/api/v1/elearning/notifications`.
**FE (elearning):** cài `socket.io-client@^2.3.0` + env `VITE_SOCKET_URL`; store Pinia `notification.js`; composable `useNotificationSocket.js`; thay chuông mock trong `AppHeader.vue` bằng dropdown thật (badge unread + list + mark-read + click router.push nội bộ).

## Ngoài scope
Noti cho learner, audio, trang "tất cả thông báo" riêng.
