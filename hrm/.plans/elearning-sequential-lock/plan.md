# Plan — Elearning: Khoá bài học theo "Học tuần tự" + Prerequisite

Owner: @junfoke
Liên quan: `learning-session-api`, `elearning-tracking-fix`

## Bối cảnh
- Khoá học (Subject) có cấu hình "Học tuần tự" → cột `subjects.linear_required` (boolean).
- Mỗi mapping bài-môn (SubjectLesson) có "Điều kiện mở khoá (Prerequisite)": `prerequisite_enabled`, `prerequisite_mode` (ALL/ANY), `prerequisite_subject_lesson_ids`.
- Bug: cấu hình học tuần tự nhưng vào học bấm bài nào cũng được.
- Root cause: `LearningSessionResource::isLocked()` CHỈ check prerequisite tường minh, KHÔNG xét `linear_required`.
- FE đã xử lý đúng (store `selectLesson` chặn `locked`, `firstUnlockedId/nextLesson/prevLesson` skip locked, view toast khi locked).

## Tasks

### BE — `Modules/Elearning/Services/LessonLockResolver.php` (MỚI - nguồn chân lý chung)
- [x] Tạo resolver tính map [subject_lesson_id => locked] kết hợp linear + prerequisite
- [x] Linear: bài chưa xong đầu tiên = mở; mọi bài chưa xong phía sau = khoá
- [x] Prerequisite: enabled=1, mode ALL/ANY trên prerequisite_subject_lesson_ids

### BE — `Modules/Elearning/Transformers/LearningSessionResource.php`
- [x] Dùng `LessonLockResolver` để tính `locked` (gỡ logic trùng: isLocked/buildLinearLockedMap/buildDoneMap/collectAllSubjectLessons)
- [x] Trả thêm `linear_required` vào `course`

### BE — `Modules/Elearning/Services/LearningSessionService.php` (defense-in-depth)
- [x] Helper `isLessonLocked()` dùng chung resolver
- [x] Chặn heartbeat nếu bài đang bị khoá (code 423)
- [x] Chặn scorm-commit nếu bài đang bị khoá (code 423)

### FE — `elearning/src/components/learning/LessonItem.vue`
- [x] Sửa badge "tiền ĐK": dùng `prereq_subject_lesson_ids` thay vì `prereqId` (field sai)
- [x] Disable click khi bị khoá (không emit click) + style mờ + cursor-not-allowed

### FE — disable nút điều hướng
- [x] Store: thêm getter `hasNext`/`hasPrev` (còn bài mở kế/trước không)
- [x] `LessonNavBar.vue`: props `hasPrev`/`hasNext` → `:disabled` + style disabled cho nút Trước/Sau
- [x] `SubjectLearnView.vue`: truyền `:has-prev`/`:has-next` từ store

### Fix: hoàn thành bài không mở bài kế (phải reload)
- [x] BE transformer trả thêm `prereq_enabled`, `prereq_mode` cho FE
- [x] Store: action `recomputeLocks()` mirror logic resolver (linear + prerequisite)
- [x] Gọi `recomputeLocks()` trong `handleHeartbeatResponse` (áp dụng cả heartbeat lẫn scorm) → bài kế mở ngay khi hoàn thành, không cần F5

## Checkpoint — 2026-06-03
Vừa hoàn thành: Toàn bộ logic khoá bài học — Học tuần tự + Prerequisite (ALL/ANY) ở cả BE (LessonLockResolver dùng chung transformer + service guard 423) và FE (disable click + nút Trước/Sau + recomputeLocks live khi hoàn thành bài).
Đang làm dở: (không)
Bước tiếp theo: User verify trên browser (Docker, Node ≥18):
  - SUB-0044 (học tuần tự): chỉ bài đầu mở; xong bài 1 → bài 2 tự mở (không F5); nút Sau disable khi chưa có bài kế mở.
  - Khoá KHÔNG tuần tự + bài bật Prerequisite ALL: phải xong hết bài chọn mới mở.
  - Prerequisite ANY: xong 1 trong các bài chọn là mở.
Blocked: (không)
