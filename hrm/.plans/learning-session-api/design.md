# Learning Session API — Tóm tắt Design

**Owner:** @junfoke
**Date:** 2026-05-28
**Spec chi tiết:** `docs/superpowers/specs/2026-05-28-learning-session-api-design.md`

## Mục tiêu

Xây dựng BE API thật cho màn học elearning, thay thế mock data FE. 3 nhóm: Learning session (load + heartbeat tracking), Lesson comment (thảo luận per-lesson), FE integration (sửa store + viewers).

## Scope

- **Migration:** `enrollment_lesson_progress` (module Training) — tracking tiến độ từng bài
- **BE:** LearningSessionService + LearningSessionController + LessonCommentController + HeartbeatRequest + LearningSessionResource
- **FE:** Sửa store learningSession.js, thêm useHeartbeat composable, sửa viewers bỏ x15, bỏ nút Hoàn thành

## Quyết định kiến trúc

- **Approach A:** Single endpoint load all + heartbeat periodic 30s + flush khi chuyển bài
- **BE auto-mark done** khi heartbeat đủ điều kiện completion (FE không có nút Hoàn thành)
- **Comment bài học** tách riêng khỏi comment khoá học (thảo luận, không rating)
- **Tracking chỉ tăng** (watched_percent, read_seconds không giảm) — chống gian lận
- **Locked logic** do BE quyết định dựa trên prerequisite + progress
