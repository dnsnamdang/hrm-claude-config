# Elearning Lesson Viewer — Plan

**Owner:** @junfoke
**Date:** 2026-05-28

> Plan chi tiết đầy đủ (code, test, commit): `docs/superpowers/plans/2026-05-28-elearning-lesson-viewer.md`

## Tổng quan

14 tasks, 6 phases — FE only (Vue 3 + Tailwind), mock data, 3 loại viewer.

## Phase 1: Foundation (Task 1-3)
- [x] Task 1: Mock Data + Constants — `src/constants/learningMock.js`, sửa `LESSON_TYPE_MAP`
- [x] Task 2: Learning Session Store — `src/stores/learningSession.js`
- [x] Task 3: Route Update — sửa `src/router/index.js` thêm `:lessonId?`

## Phase 2: Viewers (Task 4-6)
- [x] Task 4: YoutubePlayer — `src/components/learning/viewers/YoutubePlayer.vue`
- [x] Task 5: ArticleViewer — `src/components/learning/viewers/ArticleViewer.vue`
- [x] Task 6: DocumentViewer — `src/components/learning/viewers/DocumentViewer.vue`

## Phase 3: Core Components (Task 7-8)
- [x] Task 7: LessonViewer — `src/components/learning/LessonViewer.vue` (dynamic component + locked overlay)
- [x] Task 8: LessonItem — `src/components/learning/LessonItem.vue`

## Phase 4: Sidebar + Stats (Task 9-10)
- [x] Task 9: LearningOutline — `src/components/learning/LearningOutline.vue`
- [x] Task 10: LearningStats — `src/components/learning/LearningStats.vue`

## Phase 5: Navigation + Tabs (Task 11-12)
- [x] Task 11: LessonNavBar — `src/components/learning/LessonNavBar.vue`
- [x] Task 12: LessonMetaTabs — `src/components/learning/LessonMetaTabs.vue`

## Phase 6: Orchestrator + Polish (Task 13-14)
- [x] Task 13: SubjectLearnView — `src/views/subject/SubjectLearnView.vue` (full rewrite)
- [x] Task 14: Integration Test + Polish

### Checkpoint — 2026-05-28T11:00
Vừa hoàn thành: Toàn bộ 14/14 task. Browser test passed.
Đang làm dở: (không có)
Bước tiếp theo: Kết nối API thật thay mock data khi BE sẵn sàng. Mở rộng SCORM viewer.
Blocked: (không có)

## Fix: chuyển bài học nháy spinner toàn màn (2026-06-16)
- [x] Task F1: Sửa `src/App.vue` — `<router-view :key>` không còn dùng `route.path` cho route `subject-learn`

### Checkpoint — 2026-06-16
Vừa hoàn thành: Fix bug chuyển bài học load lại toàn màn (spinner full-screen, mất mượt).
Nguyên nhân: `App.vue` dùng `<router-view :key="route.path">`. `lessonId` là path param (`/khoa-hoc/:slug/hoc/:lessonId`) → đổi bài làm `route.path` đổi → key đổi → Vue remount cả `SubjectLearnView` → `onMounted(initCourse)` → `fetchCourseData()` bật `store.loading` → spinner toàn màn. Trong khi view đã có sẵn watcher `route.params.lessonId` → `selectLesson` (local, không fetch) để đổi bài mượt, nhưng bị remount vô hiệu hoá.
Fix: thêm computed `routeKey` trong `App.vue` — route `subject-learn` trả key cố định `'subject-learn'` (không gồm lessonId/slug → đổi bài/đổi khoá trong lộ trình do watcher xử lý), các route khác giữ `route.path`. 1 file: `elearning/src/App.vue`.
Đang làm dở: không.
Bước tiếp theo: User rebuild elearning (Docker) + verify browser 4 case: (1) đổi bài ở sidebar không nháy spinner, (2) nút Trước/Sau mượt, (3) "Học khoá tiếp theo" trong lộ trình (đổi slug) vẫn nạp đúng khoá mới, (4) chuyển giữa trang chi tiết khoá ↔ lộ trình vẫn remount/refetch đúng.
Blocked: không.

#### Ghi chú fix trong quá trình test
- YouTube mock URL đổi sang `dQw4w9WgXcQ` (embeddable)
- Focus mode CSS: target `header.sticky` + `footer` + `.max-w-container`, đổi `<main>` → `<section>` tránh xung đột selector
- Padding content block: tăng `p-6`, tách header bar khỏi body
- Tracking x15: 1s real = 15s simulated (đạt 80% trong ~22s cho video 7p)
- PDF mock URL đổi sang public URL (Google Docs Viewer cần URL public)
- Sidebar width: 380px thay vì 420px
