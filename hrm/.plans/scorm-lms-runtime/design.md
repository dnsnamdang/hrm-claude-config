# SCORM LMS Runtime — Tóm tắt Design

**Owner:** @junfoke
**Date:** 2026-05-30
**Spec chi tiết:** `docs/superpowers/specs/2026-05-30-scorm-lms-runtime-design.md`

## Mục tiêu

Học bài SCORM (type=4) trên màn elearning `SubjectLearnView`. Hoàn thiện phần "chạy/đọc" gói SCORM còn thiếu (feature `scorm-upload` đã làm phần upload). Bắt completion + score để auto mark done, lưu resume (location + suspend_data) để học tiếp. Hỗ trợ SCORM 1.2 + 2004.

## Ràng buộc cốt lõi

SCORM tìm runtime qua `window.parent.API` (truy cập DOM) → CORS vô dụng → nội dung phải **cùng origin**. Giải pháp: **reverse-proxy** S3 về `/scorm-proxy/...` (vite dev + nginx prod).

## Scope

- **DB:** thêm cột scorm_* vào `enrollment_lesson_progress` (Training)
- **BE:** `LearningSessionResource` (content/completion_rule/scorm_state cho type=4) + endpoint mới `POST /learn/scorm-commit` + `ScormCommitRequest` + `processScormCommit`/`checkScormCompletion`
- **FE:** dependency `scorm-again` + `ScormPlayer.vue` + nhánh trong `LessonViewer` + `useScormCommit` + sửa `SubjectLearnView` + vite proxy + env

## Quyết định chốt (brainstorming 2026-05-30)

1. Tracking = Completion + Resume
2. Serve = reverse-proxy S3
3. Hỗ trợ 1.2 + 2004
4. Adapter = scorm-again
5. Endpoint tách riêng scorm-commit
6. cmi state lưu cột thêm vào enrollment_lesson_progress
7. Completion theo cấu hình bài (scorm_completion + scorm_min_score), default completed_or_passed

## Liên quan

- Tiếp nối: `scorm-upload` (done 2026-04-22), `learning-session-api` (done 2026-05-28), `elearning-lesson-viewer` (done 2026-05-28)
