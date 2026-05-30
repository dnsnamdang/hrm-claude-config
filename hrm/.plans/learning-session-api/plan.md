# Learning Session API — Plan

**Owner:** @junfoke
**Date:** 2026-05-28

> Plan chi tiết đầy đủ (code, test, commit): `docs/superpowers/plans/2026-05-28-learning-session-api.md`

## Tổng quan

13 tasks, 4 phases — BE (Laravel 8, module Training + Elearning) + FE (Vue 3 elearning).

## Phase 1: Database + Entity (Task 1-2)
- [x] Task 1: Migration — `enrollment_lesson_progress`
- [x] Task 2: Entity `EnrollmentLessonProgress` + relation `SubjectEnrollment.lessonProgress()`

## Phase 2: Service + Resource (Task 3-4)
- [x] Task 3: `LearningSessionService` — getSessionData + processHeartbeat + checkCompletion
- [x] Task 4: `LearningSessionResource` — format response cho GET /learn

## Phase 3: Controller + Routes (Task 5-8)
- [x] Task 5: `HeartbeatRequest` — validation
- [x] Task 6: `LearningSessionController` — show + heartbeat
- [x] Task 7: `LessonCommentController` — CRUD + like (dùng HandlesComments trait)
- [x] Task 8: Routes — thêm 7 endpoints vào api.php

## Phase 4: FE Integration (Task 9-13)
- [x] Task 9: `useHeartbeat` composable — debounce 30s + flush
- [x] Task 10: Refactor `learningSession.js` store — API thật, bỏ mock, bỏ markDone
- [x] Task 11: `YoutubePlayer.vue` — elapsed += 1 (real-time)
- [x] Task 12: `SubjectLearnView.vue` — bỏ nút Hoàn thành, integrate heartbeat, auto-complete toast
- [x] Task 13: `LessonMetaTabs.vue` — comment API thật + attachments từ API

### Checkpoint — 2026-05-28 #2
Vừa hoàn thành: 13/13 tasks implement xong (subagent-driven-development)
Đang làm dở: (không có)
Bước tiếp theo: Chạy migration + test API thật trên browser
Blocked: (không có)
