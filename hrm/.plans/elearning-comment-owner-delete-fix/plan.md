# Plan — Fix nút Xoá bình luận biến mất sau khi tải lại (elearning)

Owner: @junfoke

## Bối cảnh
Nút "Xoá" bình luận chỉ hiện khi `is_own=true`. Route GET (index) bình luận không gắn
middleware auth nào → khi tải lại danh sách, BE không nhận diện learner đang đăng nhập →
`is_own=false` cho mọi comment → nút Xoá biến mất. (Chi tiết root cause đã phân tích trong session.)

## Tasks
- [x] BE: gắn `elearning.auth.optional` vào 3 route GET comment index trong `Modules/Elearning/Routes/api.php`
  - [x] `subjects/{subject}/comments`
  - [x] `subjects/{slug}/lessons/{subjectLessonId}/comments`
  - [x] `learning-paths/{slug}/comments`
- [ ] Verify: learner tải lại danh sách bình luận của mình → `is_own=true`, nút Xoá vẫn hiện; `liked` đúng
