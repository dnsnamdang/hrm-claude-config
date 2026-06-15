# Plan — Elearning Notification Center

> Plan chi tiết: docs/superpowers/plans/2026-06-15-elearning-notification-center.md
> Spec: docs/superpowers/specs/2026-06-15-elearning-notification-center-design.md

## Trạng thái

CODE DONE Task 1–3 (2026-06-15, subagent-driven). Lint BE sạch, review spec+chất lượng pass. Chờ user cài dep + verify trong Docker (Task 4).

## Tasks

### BE (Modules/Elearning)
- [x] Task 1: `NotificationController` (index/markAsRead/markAllAsRead, lọc type whitelist, employee-only) + 3 route

### FE (elearning)
- [x] Task 2: dep `socket.io-client@^2.3.0` + env `VITE_SOCKET_URL` + store `notification.js` + composable `useNotificationSocket.js`
- [x] Task 3: Chuông thật trong `AppHeader.vue` (badge unread + dropdown list + mark-read + click điều hướng)
- [x] Task 4: Verify thủ công — user xác nhận PASS (2026-06-15): chuông hiện thông báo onboarding thật, badge unread, click điều hướng góc học tập.

---

### Checkpoint — 2026-06-15 (VERIFIED + điều chỉnh)
Vừa hoàn thành: User verify PASS. Điều chỉnh trong session:
- Chuông hiện cho MỌI user đã đăng nhập (trước chỉ employee → learner bị mất icon); learner list rỗng, không connect socket.
- Trigger auto-enroll chuyển sang chạy ở `NotificationController::index` (chuông gọi ở mọi trang → noti hiện ngay sau đăng nhập, không cần mở góc học tập). Notification ghi DB ĐỒNG BỘ (BaseNotification, không phụ thuộc queue worker) + Redis publish realtime best-effort. Logic gom vào `OnboardingAutoEnrollService::runAndNotify()`.
- Fix Docker: socket.io-client thiếu trong anonymous volume → dùng `docker compose up -d --build --renew-anon-volumes elearning`.
Bước tiếp theo: (tùy chọn) review tổng + merge. Build FE trong Docker (Node≥18).

---

### Checkpoint — 2026-06-15
Vừa hoàn thành: Task 1–3 (BE controller+routes, FE store+socket+chuông). Review pass (xác nhận io.connect v2 an toàn, click-outside không đóng nhầm, query JSON scope theo employee đúng).
Đang làm dở: (không) — chờ user.
Bước tiếp theo: User cài `socket.io-client` trong container elearning + set `VITE_SOCKET_URL` + đảm bảo socket server (8891) + Redis + queue worker chạy, rồi verify 6 kịch bản. KHÔNG build được ở host (Node 14) — phải build trong Docker (Node≥18).
Blocked:

**File đã đụng:**
- Tạo: `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/NotificationController.php`
- Sửa: `hrm-api/Modules/Elearning/Routes/api.php` (3 route)
- Sửa: `elearning/package.json` (+socket.io-client) + `elearning/.env.example` (+VITE_SOCKET_URL)
- Tạo: `elearning/src/stores/notification.js`, `elearning/src/composables/useNotificationSocket.js`
- Sửa: `elearning/src/components/layout/AppHeader.vue`
