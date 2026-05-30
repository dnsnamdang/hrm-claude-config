# Elearning Lesson Viewer — Tóm tắt Design

**Owner:** @junfoke
**Date:** 2026-05-28 (v2)
**Spec chi tiết:** `docs/superpowers/specs/2026-05-28-elearning-lesson-viewer-design.md`

## Mục tiêu

Triển khai màn học đầy đủ cho elearning: 3 loại viewer (YouTube, Bài viết HTML, Tài liệu PDF/DOCX/XLSX/PPTX/ảnh), sidebar outline, tracking giả lập, prerequisite, focus mode, tabs. Mock data trước, SCORM mở rộng sau.

## 3 loại bài học

| BE type_text | FE type | Viewer component | Preview method |
|-------------|---------|------------------|----------------|
| VIDEO/YOUTUBE | video/youtube | YoutubePlayer.vue | YouTube iframe embed |
| TEXT | text | ArticleViewer.vue | Render HTML trực tiếp (v-html) |
| FILE | file | DocumentViewer.vue | PDF: Google Docs Viewer, DOCX/XLSX/PPTX: Office Online, Image: direct, Khác: download |

## Quyết định kiến trúc

- **Single View + Dynamic Component** — `SubjectLearnView.vue` orchestrator, dynamic component cho viewer
- **Route:** `/khoa-hoc/:slug/hoc/:lessonId?` — `router.push` khi chuyển bài (giống Udemy/Coursera)
- **Store:** `useLearningSession` — quản lý course data, current lesson, tracking, progress
- **11 component** mới trong `src/components/learning/`

## Cấu trúc component

```
src/components/learning/
├── viewers/
│   ├── YoutubePlayer.vue      # iframe embed + timer x15
│   ├── ArticleViewer.vue      # v-html + read timer
│   └── DocumentViewer.vue     # PDF/Office/Image preview + read timer
├── LessonViewer.vue           # Dynamic resolver + locked overlay
├── LessonItem.vue             # Lesson row (icon, title, status)
├── LearningOutline.vue        # Sidebar tree (subject→chapter→lesson)
├── LearningStats.vue          # 3 stat boxes + progress bar
├── LessonNavBar.vue           # Prev/Next + Focus toggle
└── LessonMetaTabs.vue         # Mô tả / Tài liệu / Thảo luận tabs
```

**Store:** `src/stores/learningSession.js` — course data, lesson selection, tracking, progress, prerequisite lock logic.

**Mock data:** `src/constants/learningMock.js` — 1 course, 3 subjects, 16 lessons.

## Tracking & Completion

- YouTube: timer mỗi 1s, +15s simulated → 80% = hoàn thành
- Text/File: timer mỗi 1s, +1s → 30s = hoàn thành
- Nút "Hoàn thành" chỉ để mock test, production sẽ auto-complete qua API

## Impact code hiện tại

- Đã tách `LESSON_TYPE_MAP`: `text` → `'text'`, `file` → `'file'` (bỏ gom vào `'doc'`)
- Route subject-learn: `/khoa-hoc/:slug/hoc/:lessonId?`
- SubjectOutline + PathOutline đã kiểm tra — không bị ảnh hưởng

## Bước tiếp theo

- Kết nối API thật thay mock data khi BE module Elearning sẵn sàng
- Mở rộng SCORM viewer (feature riêng)
