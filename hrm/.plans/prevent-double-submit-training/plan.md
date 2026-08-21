# Plan — Chặn double-submit khi lưu (Training builder)

Owner: @junfoke

## Bối cảnh
Sửa khoá học (subject) nhấn "Lưu" liên tục → BE nhận nhiều request song song → insert trùng `subject_exams` → lỗi `SQLSTATE[23000] 1062 Duplicate entry`. Nguyên nhân FE: các màn không có reentrancy guard, nút Lưu không bị khoá khi request đang bay.

## Phase 1 — FE reentrancy guard (chặn nhấn liên tục)
- [x] Subject builder `SubjectBuilderForm.vue`: guard bằng cờ `isSubmitSave` sẵn có ở đầu `save()` và `saveDraft()`
- [x] Lesson add `lessons/add.vue`: thêm cờ `isSubmitting`, guard đầu `submitForm()`, reset ở `finally`
- [x] Lesson edit `lessons/_id/edit.vue`: tương tự
- [x] Learning-path add `learning-path/add.vue`: tương tự
- [x] Learning-path edit `learning-path/_id/edit.vue`: guard ở `submitForm()` + `submitPayload()`, reset ở `finally` (giữ luồng confirm visibility)

## Phase 2 — Tối ưu tốc độ mở màn khoá học (builder chậm)
- [x] Chẩn đoán: BE `showBuilder`/`getDetailForBuilder` là 1 query eager-load gọn (không N+1). Chậm do FE `mounted` gọi 5 request TUẦN TỰ.
- [x] `SubjectBuilderForm.vue` mounted: gộp 4 fetch danh mục độc lập (trainingTypes, skills, lessonBank, examKits) vào `Promise.all` → còn 2 đợt (batch danh mục → loadBuilder).
- [ ] (Tuỳ chọn) Giảm payload `exams?limit=1000` và `lessons/getAll` nếu vẫn nặng — cần đo thực tế trước.
- [ ] (Tuỳ chọn) Áp cùng pattern Promise.all cho LessonForm / LearningPathForm nếu 2 màn này cũng chậm.

## Ghi chú
- Guard đặt đồng bộ TRƯỚC `await` đầu tiên → click thứ 2 bị bỏ qua chắc chắn (event loop xử lý từng click).
- Chưa đụng component dùng chung `V2Footer` (nếu muốn disable nút trực quan cần bổ sung prop → hỏi trước).
- BE (defense-in-depth): nên bọc transaction / idempotent cho `subjects/{id}/builder` — ngoài scope lần này, đề xuất riêng.

### Checkpoint — 2026-08-10
Vừa hoàn thành: xác định root cause + guard 5 màn
Đang làm dở: (không)
Bước tiếp theo: user verify trên UI
Blocked:
