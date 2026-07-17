# Plan — Màn học player (elearning học viên)

## Bug fixes

### [x] Fix: Trạng thái khoá kẹt "Đã tham gia" dù đang học
- **Triệu chứng:** Bài học hiển thị "Đang học" nhưng chi tiết khoá vẫn "Đã tham gia".
- **Root cause:** `enrollment.status` chỉ chuyển `enrolled → learning` bên trong `recalculateCourseProgress()`, mà hàm này chỉ chạy khi bài VỪA `done` (`$justCompleted`); điều kiện `$progress > 0` cũng chỉ đếm bài `done`. Đang xem dở (0 bài done) → khoá kẹt ở `enrolled`.
- **Fix:** [LearningSessionService.php](../../../hrm-api/Modules/Elearning/Services/LearningSessionService.php)
  - Thêm helper `markEnrollmentLearning()` (idempotent, chỉ đổi khi đang `enrolled`).
  - Gọi mỗi heartbeat khi lesson đang `learning` (cả video/doc `handleHeartbeat` lẫn SCORM commit) → tự chữa cả enrollment cũ đang kẹt.
  - FE không cần sửa (đã nghe `enrollment_status` từ response heartbeat).

### Checkpoint — 2026-07-14
Vừa hoàn thành: Fix trạng thái khoá kẹt "Đã tham gia" dù đang học (BE LearningSessionService).
Đang làm dở: (không có)
Bước tiếp theo: Verify thực tế — mở 1 bài, xem heartbeat, kiểm tra chi tiết khoá đổi sang "Đang học".
Blocked:
