# Plan — Fix validate màn tạo/sửa bài học (Training)

Owner: @junfoke
Ngày: 2026-07-16

## Bối cảnh / Root cause
Màn `pages/training/lessons` (LessonForm.vue). Hàm `validateForm()` đã tồn tại nhưng
`add.vue` + `edit.vue` **không gọi** → submit thẳng API. BE `LessonRequest` chỉ có
`required_if` (check rỗng), không check định dạng → nhập rác vẫn lưu.

## Tasks

### FE — LessonForm.vue
- [x] Bug 5: `syncDuration` bỏ ép cứng phút/giây về 59; validate phút/giây ≥60 → báo lỗi inline (không tự sửa). Bỏ `max="59"`.
- [x] Bug 2: cải thiện check nội dung Text/HTML rỗng (strip tag, bỏ `<p><br></p>`), thêm helper `isHtmlEmpty`.
- [x] Bug 4: validate URL launch (type 4). SỬA LẠI (user test URL đúng định dạng vẫn pass): yêu cầu (1) đã upload gói `package_path`, (2) URL đúng http(s), (3) URL **chứa** `package_path` (trỏ vào gói đã upload) → chặn URL ngoài tùy ý.
- [x] Bug 1: check `extractYoutubeId` + rỗng — nay được gọi qua add/edit.
- [x] Bug 3a: giữ check `file_path` bắt buộc (đã có).
- [x] Bug 6 (mới): validate đuôi file khớp "Định dạng" (kind) khi type=3 — chọn PDF không cho upload .zip. FE chặn trong `onUploadContentFile` + `:accept` gợi ý; BE `withValidator` check `file_type` vs `kind` (helper `allowedExtsForKind`). Áp cả create + update (dùng chung LessonForm.vue + LessonRequest).
- [x] Bug 3b: PDF preview → Google gview (`getPdfViewerUrl`) + thanh action luôn hiện (Mở tab/Tải xuống).

### FE — add.vue + edit.vue
- [x] Gọi `this.$refs.lessonForm.validateForm()` trước khi submit; false → toast + dừng.

### FE — TabInfo.vue (màn Lộ trình học) — fix UI banner cảnh báo Public
- [x] Bug 7 (mới): banner `.public-warning` vỡ layout do `display:flex` + text không bọc trong 1 phần tử (mỗi text-node/`<b>` thành flex-item riêng, dàn ngang méo). Fix: bọc text vào `<span>` (cả 3 banner), `align-items:flex-start`, span `flex:1;min-width:0;word-break`. Rút gọn danh sách mã (đang "--" x26) bằng computed `violatingPublicLabel` (ưu tiên mã, thiếu thì tên, cắt còn 5 + "… và N khoá khác").

### FE — LessonForm.vue — đổi loại bài học không cập nhật khối nội dung
- [x] Bug 9 (mới, VERIFIED Playwright): sửa bài học SCORM/loại có `file_name` → đổi sang Tài liệu thì component **crash** (`data.content.kind.toUpperCase()` khi kind undefined) → Vue giữ DOM cũ (hiện tượng "khối vẫn của loại khác"). Fix: (1) guard `(data.content.kind || '').toUpperCase()`; (2) `onTypeChange` reset `data.content` về default (`getDefaultContent`) để khối mới sạch, không lẫn field loại cũ. Verify: SCORM→Tài liệu không crash, block đúng, content reset (kind=pdf, file_name rỗng).

### FE — Elearning (Vue 3) — đánh giá sao phần Thảo luận
- [x] Bug 8 (mới, enhancement): thay `<select>` "Đánh giá" bằng **5 sao click** (hover sáng, có nhãn "5 - Rất tốt"); hiển thị điểm ở mỗi bình luận thành **đủ 5 sao** (fill/empty) thay vì "⭐ 5/5". Đồng bộ 4 file: DetailDiscussion.vue, CommentNode.vue, SubjectDiscussionView.vue, LearningPathDiscussionView.vue. Tailwind + remix icon `ri-star-fill`/`ri-star-line`.

### BE — LessonRequest.php (defense in depth)
- [x] `withValidator`: type 1 check định dạng YouTube; type 4 check URL; type 2 check html rỗng thực chất. `php -l` sạch.

### Checkpoint — 2026-07-16
Vừa hoàn thành: toàn bộ code FE + BE cho 5 lỗi validate màn bài học.
Đang làm dở: —
Bước tiếp theo: user hard-refresh + verify UI (browser MCP đang khóa profile → Claude chưa tự test được).
Blocked: Playwright MCP profile bị khóa (Chrome session cũ chưa đóng).

## Ghi chú
- Root cause thật của Bug 3b nhiều khả năng là S3 upload không set `ContentType` (→ octet-stream)
  ở `CmcS3Helper::putFile` (HÀM DÙNG CHUNG — không tự sửa). Fix FE bằng gview để không đụng shared helper.
  Khuyến nghị follow-up: set ContentType theo extension trong CmcS3Helper (cần user duyệt).
- Chưa verify được UI qua Playwright do browser MCP profile đang bị khóa (session Chrome cũ).
