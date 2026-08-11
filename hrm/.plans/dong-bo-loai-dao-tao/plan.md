# Plan — Đồng bộ loại đào tạo

Owner: @junfoke · Spec: `docs/superpowers/specs/2026-07-28-dong-bo-loai-dao-tao-design.md`

## Phase 1 — Khóa học (Subject) ↔ Bài học (Lesson)

### BE
- [x] T1. `SubjectDetailResource.php`: thêm `'training_type_id' => $lesson->training_type_id` vào sub-object `lesson` (dòng ~153)
- [x] T2. `SubjectBuilderRequest::withValidator`: thêm `after()` gom lesson_ids (subject_lessons + chapters.*.subject_lessons), chặn mismatch loại đào tạo → lỗi `mismatched_lessons` (skip khi chưa có training_type_id)
- [x] T1b. **(PHÁT SINH khi verify)** `LessonService::getAllForSelect`: thêm `training_type_id` vào `select(...)`. Picker khóa học dùng endpoint này (KHÔNG phải LessonListResource) — thiếu field khiến filter FE ẩn sạch bài học. `subjects/getAll` trả full model nên không cần sửa.

### FE
- [x] T3. `subjects/tabs/TabInfo.vue` — `filteredLessonBank`: lọc chỉ bài học cùng `training_type_id`
- [x] T4. `subjects/tabs/TabInfo.vue` — `openLessonPicker`: guard chưa chọn loại → toast + return
- [x] T5. `subjects/tabs/TabInfo.vue` — `isMismatchedLesson()` + `mismatchedLessonCount` + banner cảnh báo + tô đỏ dòng (dùng `lesson-row--broken`) + ẩn nút info/mapping cho bài lẫn loại
- [x] T6. `SubjectBuilderForm.vue` — `countMismatchedSubjectLessons()` + chèn chặn vào `validate()` và `saveDraft()`

## Phase 2 — Lộ trình (LearningPath) ↔ Khóa học (Subject)

### BE
- [x] T7. `LearningPathRequest::withValidator`: thêm `after()` chặn subjects khác loại → lỗi `subjects` (skip khi chưa có training_type_id)

### FE
- [x] T8. `learning-path/TabInfo.vue` — `filteredBank`: ràng buộc cứng chỉ khóa cùng `training_type_id` của lộ trình
- [x] T9. `learning-path/TabInfo.vue` — `openPickerModal`: guard chưa chọn loại → toast + return
- [x] T10. `learning-path/TabInfo.vue` — `mismatchedTypeSubjects` + banner cảnh báo + badge đỏ "Khác loại đào tạo" trên card
- [x] T11. `LearningPathForm.vue` — `validate()`: chặn khi có subjects khác loại (chỉ khi đã chọn loại)

## Verify (Playwright, tài khoản dev, 2026-07-28)
- [x] V1. Khóa học: chưa chọn loại → popup KHÔNG mở (guard OK). Chọn loại "Đào tạo phát triển bản thân" (id1) → popup hiện đúng **6 bài, tất cả loại 1** (cross-check lessonBank)
- [x] V2. Thêm bài loại 1 → đổi loại sang "Đào tạo kỹ thuật" → banner đỏ "Có 1 bài học khác loại đào tạo" + dòng LESS-0008 tô đỏ + ẩn nút info/mapping + bấm Lưu bị chặn (vẫn ở /add, lỗi `mismatched_lessons`)
- [~] V3. Mở sửa khóa cũ lẫn loại: dùng CHUNG cơ chế reactive với V2 (isMismatchedLesson) — đã verify qua luồng tạo+đổi loại (cùng code path). Chưa test riêng luồng edit data cũ.
- [x] V4. Lộ trình: chưa chọn loại → popup KHÔNG mở. Chọn "Chuyên môn nghiệp vụ" (id13) → picker đúng **3 khóa loại 13**. Thêm 1 khóa → đổi loại sang "Kỹ năng mềm" → banner + badge "Khác loại đào tạo" + `validate()` trả false với lỗi `subjects`
- [~] V5. BE reject: php -l sạch 3 file, logic mirror pattern locked-lesson/public-subject sẵn có. FE đã chặn nên chưa test bypass trực tiếp API.

---

### Checkpoint — 2026-07-28
Vừa hoàn thành: CODE DONE cả 2 phase (11 task + 1 task BE phát sinh T1b) + VERIFIED bằng Playwright (khóa học + lộ trình: guard, filter, cảnh báo mismatch, chặn lưu đều PASS). php -l sạch. 8 file thay đổi (thêm T1b so với plan gốc).
Đang làm dở: —
Bước tiếp theo: User verify lại bằng mắt trên browser (hard-refresh) + quyết định có test riêng luồng edit data cũ (V3) / bypass API (V5) không. KHÔNG commit git (theo quy tắc).
Blocked:
