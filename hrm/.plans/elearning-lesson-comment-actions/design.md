# Design — Thích / Trả lời / Xóa cho bình luận bài học (elearning)

Owner: @junfoke — 2026-07-16

## Mục tiêu
Tab "Thảo luận" trong màn học bài (LessonMetaTabs.vue) hiện chỉ hiển thị tên/ngày/nội dung,
không có tương tác. Bổ sung **Thích, Trả lời (reply lồng), Xóa** dùng chung UI như màn thảo luận
khóa học/lộ trình. KHÔNG có Báo cáo, KHÔNG có đánh giá sao (bài học không chấm điểm).

## Quyết định chính
- Tái sử dụng component `CommentNode` (đồng nhất UI, ít lặp code).
- BE không cần code mới: `LessonCommentController` đã dùng trait `HandlesComments`
  (store/update/destroy/like + reply qua parent_id). Route đã trong nhóm `elearning.auth`.
  Route GET index đã fix middleware `elearning.auth.optional` ở bước trước.
- Phân trang: load 5 đầu + nút "Xem thêm" load thêm 5 (dùng `loadMore` sẵn có), **inline** —
  KHÔNG trỏ sang màn thảo luận riêng như màn ngoài.
- `CommentNode` thêm prop `allowReport` (default `true`, additive) để ẩn nút Báo cáo cho lesson.

## Thay đổi
- FE `useDiscussion.js`: thêm `entityType='lesson'` → basePath
  `/api/v1/elearning/subjects/{slug}/lessons/{subjectLessonId}/comments`. Chữ ký thêm `opts`.
- FE `CommentNode.vue`: prop `allowReport`, bọc nút Báo cáo `v-if`, truyền xuống node con.
- FE `LessonMetaTabs.vue`: thay logic bình luận thủ công bằng `useDiscussion` + `CommentNode`;
  tạo lại composable khi đổi `subject_lesson_id` (pattern SubjectDiscussionView); nút "Xem thêm".

## Spec chi tiết
Xem `docs/superpowers/specs/2026-07-16-elearning-lesson-comment-actions-design.md`.
