# Plan — Thích / Trả lời / Xóa cho bình luận bài học (elearning)

Owner: @junfoke

## Phase 1 — FE

### Composable
- [x] `useDiscussion.js`: thêm hỗ trợ `entityType='lesson'` + param `opts.subjectLessonId`
  - [x] basePath lesson = `/api/v1/elearning/subjects/{slug}/lessons/{subjectLessonId}/comments`
  - [x] Giữ nguyên hành vi subject/learning_path

### Shared component
- [x] `CommentNode.vue`: thêm prop `allowReport` (default true), bọc nút Báo cáo `v-if`, truyền xuống node con đệ quy

### Lesson viewer
- [x] `LessonMetaTabs.vue`: thay phần bình luận thủ công bằng `useDiscussion('lesson')` + `CommentNode`
  - [x] Tạo lại composable khi đổi `subject_lesson_id` (shallowRef + watch), rồi load()
  - [x] Render CommentNode với @like/@delete/@reply/@require-login, `:allow-report="false"`
  - [x] Ô soạn thảo: postComment({ comment }) (không rating)
  - [x] Nút "Xem thêm" gọi loadMore() khi `hasMore` (inline, không trỏ màn riêng)

### Verify
- [ ] Đăng nhập học viên → vào bài học → tab Thảo luận: gửi, thích, trả lời, xóa hoạt động; tải lại vẫn thấy nút Xóa của mình; "Xem thêm" load thêm 5

## Phase 2 — Fix UX empty input (bình luận/reply)
- [x] `CommentNode.vue` `onReply`: khi rỗng → toast "Vui lòng nhập nội dung trả lời" thay vì return im lặng (áp cho reply ở tất cả màn thảo luận: lộ trình/khóa học/bài học)
- [x] `LessonMetaTabs.vue` `submitComment`: khi rỗng → toast "Vui lòng nhập nội dung bình luận"
