# Bình luận kiểu Facebook — Nhiệm vụ & Vấn đề (web + app) — @cuong61n

Phạm vi: bình luận của Nhiệm vụ (task) và Vấn đề (issue). Web `hrm-client/components/comments/*`, app `TPE_APP/app/lib/ui/task/task_comments_page.dart`, BE `Modules/Assign/.../{Task,Issue}CommentController`. Nhánh `develop`.
Đối chiếu hiện trạng (31/10/2026): BE đã có thông báo reply/mention/react và giới hạn 3 cấp; chỉ chủ bình luận được sửa/xoá; chưa có `is_edited`, chưa phân trang.

## Đợt 1 — BE nhỏ + web
- [x] (31/10) BE: thêm `is_edited` vào `formatComment` (Task + Issue)
- [x] (31/10) Web: giờ tương đối ("5 phút trước"), rê chuột hiện giờ đầy đủ
- [x] (31/10) Web: nhãn "Đã chỉnh sửa"
- [x] (31/10) Web: gom Sửa/Xóa vào menu ⋯; dòng hành động gọn (giờ · Thích · Trả lời)
- Web: Enter gửi/Shift+Enter đã có sẵn từ trước — bỏ. Ô soạn gọn: chưa làm
- [x] (31/10) Web: xóa bình luận con tại chỗ (không tải lại cả cây) + đồng bộ reaction khi load lại; thêm nút icon 👍 một chạm (kèm số lượt, thay chip 👍)
- [ ] Web: thumbnail ảnh đính kèm

## Đợt 2 — App
- [x] (31/10) App: nhãn "Đã chỉnh sửa"
- [x] (31/10) App: icon 👍 một chạm kèm số lượt (bỏ nút chữ "Thả cảm xúc", chọn cảm xúc bằng nhấn giữ icon 👍; ⋯ Sửa/Xóa chuyển xuống cuối dòng hành động)
- [x] (31/10) App: giờ tương đối ("Vừa xong", "5 phút trước", "2 giờ trước"), chạm vào giờ hiện giờ đầy đủ
- [x] (31/10) App: nhấn giữ icon 👍 mở bảng chọn cảm xúc; chạm số lượt / nhấn giữ chip → bảng "Cảm xúc" liệt kê ai đã thả
- [x] (31/10) App: "Xem N phản hồi" thu gọn nhánh con
- [ ] App: màn chi tiết task dùng `comments_count` thay vì tải cả cây để đếm

## Đợt 3 — App chuyên nghiệp hơn + ghim/đã giải quyết/phân trang (31/10/2026, bỏ "tự cập nhật")
- [x] (31/10) App: ảnh đính kèm thumbnail trong bong bóng (1 ảnh to, nhiều ảnh lưới) + thumbnail ở ô soạn (có ✕)
- [x] (31/10) App: gửi tức thì (đang gửi / lỗi → Thử lại · Xóa). Sửa kèm: thiếu header `Accept: application/json` làm BE trả 302 khi 422 và app tưởng gửi thành công (bình luận biến mất không báo lỗi) — đã thêm cho tạo + sửa bình luận
- [x] (31/10) App: nhấn giữ bong bóng và nút ⋯ dùng chung 1 menu (Sao chép · Trả lời · Sửa · Ghim · Đã giải quyết · Xóa theo quyền)
- [x] (31/10) App: cụm cảm xúc ở góc bong bóng
- [x] (31/10) App: bình luận dài "Xem thêm" (link bấm được: chưa làm — app chưa có gói url_launcher)
- [x] (31/10) App: lưu nháp khi thoát (trong phiên chạy app, chưa lưu qua lần mở app sau)
- [x] (31/10) App: vuốt phải để trả lời
- [x] (31/10) BE: migration `2026_10_31_000001_add_pin_resolve_to_comments_table` (is_pinned/pinned_by/pinned_at/is_resolved/resolved_by/resolved_at), trait `CommentModeration`, API `POST .../comments/{id}/pin|resolve`, xóa bởi người tạo/phụ trách (`can_delete`, `can_manage`), phân trang `?limit=&before_id=` (trả `total`, `count_all`, `meta`)
- [x] (31/10) Web + App: ghim (tối đa 3, chỉ bình luận gốc) · "Đã giải quyết" · quản lý xóa · phân trang "Xem bình luận cũ hơn"
- [x] (31/10) App: mở màn bình luận dừng ở bình luận mới nhất; màn chi tiết task dùng `comments_count`
- [x] (31/10) Sửa chung: `action_menu_sheet.dart` đáy trắng liền (SafeArea vào trong khối trắng)

## Kết quả test (31/10/2026)
BE (curl, Task + Issue): danh sách đủ/phân trang/ghim đầu trang; ghim tối đa 3 (422 khi thứ 4); ghim bình luận con → 422; ghim không đổi `updated_at` (không hiện nhầm "Đã chỉnh sửa"); người ngoài 403 khi ghim/giải quyết/xóa; người tạo xóa được bình luận người khác; người phụ trách ghim được.
App (simulator iPhone 15, ~60 bước, log không có lỗi Flutter mới): phân trang 20 + "Xem bình luận cũ hơn"; ghim/bỏ ghim; đã giải quyết; gửi tức thì; gửi lỗi 422 → Thử lại/Xóa; vuốt phải trả lời; phản hồi tự mở; nhấn giữ 👍 chọn cảm xúc; bảng "Cảm xúc" ai đã thả; xóa bình luận người khác (người tạo) có hỏi + DB mất; menu người không phải quản lý (không có Ghim/Đã giải quyết); sửa → "Đã chỉnh sửa"; nháp giữ khi vào lại; ảnh thumbnail 1/nhiều + xem toàn màn; chọn ảnh từ thư viện → thumbnail ô soạn → gửi chỉ ảnh.
Web (Playwright): thread phân trang 22→31 không trùng; ghim/đã giải quyết hiển thị; menu ⋯ đủ mục; ghim qua menu; tiêu đề đếm đúng 31.
Bổ sung cùng ngày (31/10): App màn Vấn đề (ghim · đã giải quyết · xóa bình luận người khác, API `issues`) — chạy đúng. Web: người tạo xóa bình luận người khác (hộp xác nhận → mất khỏi giao diện và DB); tài khoản không phải quản lý (bình luận người khác không có ⋯, của mình chỉ Sửa/Xóa); hồ sơ thẩm định giải pháp (API cũ không có trường mới: không phân trang, không hiện Ghim, chủ bình luận vẫn Sửa/Xóa).
CHƯA test: Android (user chốt không cần, chỉ test local); mất mạng thật (chỉ thử lỗi 422); link bấm được trong bình luận (chưa làm).
Triển khai: cần chạy migration trên dev/prod.

## Đã đẩy (31/10/2026) — nhánh develop
- hrm-api `ff1ccbaed` (đã gộp origin → `eea87c38b`), hrm-client `84c49fc81` (→ `bee1f06f6`), TPE_APP `7b7670c` (App 2.2.6 build 158 tpeDev)
- TestFlight: Tân Phát ERP-HRM (tpeDev) 2.2.6 (158) — build trong worktree sạch `~/.tpe-release-tpedev` ở commit `7b7670c` (thư mục chính đang có file Meeting dở của người khác nên không build từ đó)
- CHƯA làm: chạy migration + deploy BE lên server dev; merge develop → tpe (theo skill app-build-release)

## Để sau (cần chốt)
- Phân trang bình luận (BE + web + app), cập nhật gần thời gian thực, ghim, "Đã giải quyết", quyền xoá của quản lý.

## Trạng thái (31/10/2026)
Chưa test trình duyệt / simulator, chưa commit. Web: eslint sạch. App: `dart analyze` sạch. Cần test: sửa bình luận → hiện "Đã chỉnh sửa"; thu gọn/mở phản hồi; mở từ thông báo vào bình luận con.

## Điều tra 25/11/2026 — dán (paste) ảnh vào bình luận / mô tả không được, phải bấm Đính kèm (user báo, prod /assign/tasks + /assign/issues)
- [x] (25/11) Điều tra nguyên nhân (chưa sửa, chờ user chốt hướng):
  - Bình luận (Task + Issue dùng chung `hrm-client/components/comments/CommentEditor.vue`): ô soạn là `contenteditable` nhưng KHÔNG có handler `@paste`. Dán ảnh → trình duyệt chèn `<img src="data:…">` vào ô, nhưng `_getRawText()` chỉ lấy text/BR/chip @ nên ảnh bị bỏ qua → `hasContent=false`, nút Gửi mờ, không có gì gửi đi. Ảnh chỉ vào được qua `<input type="file">` "Đính kèm". BE (`TaskCommentController`/`IssueCommentController`) đã nhận `files[]` (`file|max:51200`, `comment` được rỗng khi có files) → chỉ thiếu FE. Bình luận render text thuần (`renderContent` escape HTML) nên không thể nhúng ảnh inline, ảnh phải đi theo `attachments`.
  - Khuôn có sẵn để copy: `components/chat/ChatComposer.vue:579 onPaste()` (lấy `e.clipboardData.files` → `addFiles`), `components/bug-report/BugReportModal.vue:406`.
  - Mô tả (TaskForm/TaskDetailTab/IssueForm/IssueDetailTab): là `V2BaseTextarea` = `<textarea>` text thuần, cột DB `text` → bản chất không nhận ảnh. Ảnh đi theo khối "Tệp đính kèm" (`V2BaseFile`) ngay dưới mô tả; cũng chưa có `@paste` để tự đẩy ảnh dán vào khối đó.
  - Phụ: FE chặn gửi khi ô chữ rỗng dù BE cho gửi chỉ file (`submit()` return khi `!content`, `hasContent` không tính files).
- [x] (25/11) User chốt "làm như phần chat" → đã code (worktree `HRM/worktrees/gop_db-client`, nhánh `gop_db`, cổng 3002 — user yêu cầu 25/11; đã gỡ khỏi `hrm-client` nhánh gop_db-main; chưa commit, chưa test trình duyệt):
  - Util dùng chung mới `utils/clipboardFiles.js`: lấy `clipboardData.files` (fallback `items`), ảnh dán tên mặc định `image.png` → đổi thành `anh-dan-YYYYMMDD-HHmmss.png` để dán nhiều ảnh không trùng tên.
  - `components/comments/CommentEditor.vue` (Task + Issue): `@paste` → tệp vào danh sách đính kèm (copy khuôn `ChatComposer.onPaste`), ô xem trước có thumbnail ảnh 28px + tên cắt `…` (khuôn `.cc__file/.cc__thumb`), `files` thành `[{key,file,name,thumb}]`, revoke objectURL khi bỏ/reset/destroy; `hasContent` tính cả tệp và `submit()` cho gửi chỉ có tệp (BE đã `required_without:files`). Tooltip nút Đính kèm nhắc "dán ảnh Ctrl+V".
  - Ô Mô tả (text thuần, không chứa được ảnh) → dán ảnh = thêm Tệp đính kèm: `TaskForm.vue` (push vào `f.attachments` qua `onPickFiles`), `TaskDetailTab.vue` popup sửa mô tả (tải lên + lưu ngay, chỉ khi `canEdit`), `IssueDetailTab.vue` popup sửa mô tả (chỉ `pop.key==='description'` và `canFiles`), `IssueForm.vue` (mở bảng `FileAttachmentTable` rồi gọi `addPickedFiles`).
  - `components/FileAttachmentTable.vue` (dùng chung): THÊM method `addPickedFiles(files)` (thêm dòng + đi qua `handleFileValidation` như bấm Chọn tệp, có `await $nextTick` vì `fileList` là prop v-model) — không đổi hàm cũ.
  - Đã kiểm: parse template + script 7 file bằng vue-template-compiler/acorn (lỗi `?.` dòng 449 CommentEditor là code cũ, acorn không hiểu). ESLint repo không cài sẵn trong node_modules.
- [x] (25/11) User bổ sung: "mở panel phải THẤY ảnh ngay, không phải bấm vào tệp" → user chốt hướng **thumbnail ở Tệp đính kèm** (không đổi Mô tả sang HTML):
  - `components/AttachmentImageThumb.vue` (mới, dùng chung): tệp là ảnh → ảnh thu nhỏ cao 72px (bình luận 96px), bấm mở toàn màn; Ctrl/Cmd+bấm mở tab mới.
  - `plugins/image-viewer.js` (mới) + đăng ký `nuxt.config.js` (mode client): `this.$viewImages(images, src)` mount 1 lần `ChatImageViewer` của khung chat (phóng to/thu nhỏ/xoay, ← →, Tải xuống, Esc) → toàn hệ thống 1 kiểu xem ảnh.
  - Gắn vào: `TaskDetailTab.vue`, `IssueDetailTab.vue`, `TaskForm.vue` (chip `.tkp-file--img`, CSS ở `task-panel.scss`), `CommentNode.vue` (`.cmt-file--img`: ảnh trên, tên + dung lượng dưới). Helper `isImg()` dùng `isImageFile` của `utils/chat/chatFormat.js`.
  - Bug phát hiện khi test: Esc trong trình xem ảnh đóng luôn panel Task/Issue (cả 2 nghe `keydown` capture trên document, panel đăng ký trước) → `TaskPanel.vue` + `IssuePanel.vue` `onKey` bỏ qua khi `[data-testid="chat-image-viewer"] .vel-modal` đang mở (cùng khuôn với bug-report / app-confirm).
  - Chưa làm: bảng `FileAttachmentTable` (form tạo Issue) chưa có thumbnail — là bảng dùng chung nhiều màn, chỉ sửa khi user yêu cầu. Tiêu đề trình xem ảnh hiện "· 1/2" (dư dấu · vì không có giờ gửi như chat) — sửa phải đụng `ChatImageViewer` dùng chung, để sau.
- [x] (25/11) Test Playwright trên worktree :3002 (API gop_db-api :8003, TK namdangit; phải `permission:catalog-sync` + `migrate` DB local — migration seed `2026_11_09_000003` kẹt do dữ liệu có sẵn, đã đánh dấu đã chạy):
  - Bình luận Task 1944: dán ảnh → chip thumbnail tên `anh-dan-20261125-104139.png` → Gửi → BE 200, attachment lên S3, hiện trong luồng. Chỉ dán 2 ảnh không chữ → gửi được (comment rỗng, 2 attachments). Bỏ chip → nút Gửi tắt. Dán chữ thường không bị chặn. Bình luận Issue 14: tương tự, 200 + 1 attachment.
  - Mô tả: popup sửa mô tả Task 1944 → upload 200 + PUT lưu, chip hiện ngay; popup sửa mô tả Issue 14 → vào Tệp đính kèm; form tạo Issue → bảng Tệp đính kèm tự mở, 2 ảnh = 2 dòng, 2 lượt upload. Form tạo Task chưa test qua UI (màn danh sách không có nút Tạo), nhưng đi cùng `onPickFiles` đã test ở popup.
  - Thumbnail: mở panel Task 1944 thấy ảnh ngay (2 tệp đều ra ảnh), bấm mở trình xem "1/2", Esc đóng viewer mà panel vẫn mở; bình luận ra ảnh 96px + tên, bấm mở viewer, Esc giữ panel.
- [x] (25/11) User báo tiếp (ảnh form Tạo nhiệm vụ, khối "Tệp đính kèm 0 tệp"): dán ảnh vào khối này phải hiện như bên Vấn đề. Nguyên nhân: 4 chỗ chỉ bắt `@paste` trên ô Mô tả — dán khi focus ở khối Tệp / chỗ trống của form thì không bắt; riêng `TaskForm` còn không mở khối Tệp (`open.file`) nên dán ở Mô tả lúc khối đang đóng cũng không thấy gì (Issue có `showFiles = true`). Sửa: chuyển `@paste` lên phần tử GỐC của `TaskForm` (`.tkp-form`), `IssueForm` (`.isp-form`), `TaskDetailTab` (`.tkp-detail`), `IssueDetailTab` (`.isp-detail`) → dán ảnh ở bất kỳ đâu trong form/tab đều thành Tệp đính kèm và tự mở khối Tệp (`open.file` / `showFiles` / `showAdd.file` / `addFile`); bỏ `e.defaultPrevented` (bình luận đã tự xử lý) và dán chữ không file thì bỏ qua. IssueDetailTab chỉ bỏ qua khi đang mở popup sửa ô KHÁC Mô tả.
  - Test Playwright :3002: form Tạo nhiệm vụ (mở qua `TaskPanel.create()`) dán 2 lượt ở chỗ trống → `POST files/upload` 200 (S3), khối Tệp tự mở "2 tệp" + 2 thumbnail; lượt đầu tưởng hỏng vì chờ 4s chưa đủ (S3 ~5s), không phải lỗi. Form Tạo vấn đề: dán ở gốc form → bảng Tệp tự mở, 1 dòng. Tab Chi tiết Issue 14: dán ở chỗ trống → tệp 1→2 (upload + PUT lưu). Tab Chi tiết Task 1944: tệp 2→3. Cả 4 nơi `defaultPrevented=true` (không chèn ảnh base64 vào ô chữ).
- [x] (25/11) Rà app TPE_APP (nhánh `develop`): bình luận app đã có thumbnail từ 31/10. Chi tiết Nhiệm vụ / chi tiết Vấn đề / form Tạo-Sửa (cả 2) / kết quả Nhiệm vụ: tệp ảnh chỉ là dòng ô chữ "IMG" + tên, bấm mới mở ảnh (trình xem riêng của Meeting) → cùng lỗi "vào màn không thấy ảnh" như web. User chốt làm, test trên simulator là đủ.
  - `lib/ui/work/widget/work_widgets.dart` (dùng chung 5 chỗ, chỉ THÊM): `WorkFileRow` thêm tham số tuỳ chọn `thumbUrl` → tệp ảnh thay ô "IMG" bằng ảnh thu nhỏ 44 bo 7 (`CachedNetworkImage`, spinner / ảnh hỏng như bình luận), nút phải 🔍 thay tải xuống; dòng không truyền `thumbUrl` giữ nguyên. Thêm helper `workFileName` / `workFileUrl` / `workFileIsImage` / `workViewFile(context, f, siblings)`: ảnh → `showAppPhotoViewer` (trình xem chung user duyệt 06/11, vuốt qua lại mọi ảnh cùng khối, mở đúng ảnh bấm), tệp khác → `MeetingFileActions.view` như cũ.
  - Gắn vào `work_task_detail_page.dart` (Tệp đính kèm + Kết quả thực hiện), `work_issue_detail_page.dart` (Tệp đính kèm + thẻ đã xử lý), `work_issue_form_page.dart`, `work_task_form_page.dart` (tệp vừa chọn cũng ra thumbnail, bấm xem được). Gỡ import `meeting_file_actions` thừa ở 3 file. `flutter analyze lib/ui/work` sạch.
  - Thêm: `workViewFile` chỉ ghi tên ảnh ở chân viewer khi có 1 ảnh (viewer chung nhận 1 caption cố định, nhiều ảnh mà ghi tên ảnh đầu là sai khi vuốt — thấy khi test). Sửa luôn lỗi có sẵn: hàng "Thêm vào nhiệm vụ: Checklist · Nhiệm vụ con" ở chi tiết Nhiệm vụ là `Row` tràn 6px trên màn 393 → `Wrap`.
  - Test simulator iPhone 15 (tpeLocal :8000, DB local_hrm_erp, TK namdangit, 39 bước `step.sh`, 1 lỗi Flutter = tràn 6px nói trên đã sửa): chi tiết Nhiệm vụ 1944 (3 tệp: 2 ảnh thật hiện thumbnail ngay, 1 ảnh hỏng hiện icon ảnh hỏng) → bấm ảnh mở viewer chung "1 / 3", vuốt sang ảnh 2 (ảnh hỏng báo "Không tải được ảnh"), ✕ về đúng màn; chi tiết Vấn đề 14 (khối Tệp đính kèm / chứng cứ) 2 tệp ra thumbnail, bấm mở "1 / 2"; form Sửa vấn đề mục 4 ra thumbnail; form Tạo nhiệm vụ → Tệp → Thư viện ảnh chọn ảnh → upload S3 200 → dòng tệp ra thumbnail ảnh thật, bấm mở viewer có tên ảnh ở chân. Ảnh dán ở web sáng nay (78 B) là PNG hỏng (PIL không đọc được) nên app hiện icon hỏng là đúng; đã đổi 3 dòng `files` của task 1944 / issue 14 sang ảnh thật tải lên S3 để test (DB local).
  - Phát hiện ngoài phạm vi, CHƯA sửa: form Tạo nhiệm vụ chọn 2 ảnh thư viện → app gửi đủ 2 file nhưng `POST files/upload` chỉ trả 1 URL (BE hoặc S3 rớt 1 file, curl 2 file PNG nhỏ thì trả đủ 2) → app ghép URL theo thứ tự nên dòng hiện TÊN ảnh 1 nhưng ẢNH là ảnh 2, không báo gì. Cần xem riêng (BE `files/upload` + cách ghép của `_attachFrom`).
  - Chưa test: Android, tài khoản không quyền, mất mạng.
- [x] (25/11) User yêu cầu tiếp (sau deploy): (a) UI tệp của Vấn đề phải giống Nhiệm vụ; (b) xem trước nhiều loại tệp, không chỉ ảnh, vì hệ thống đã có sẵn. Rà: khác nhau duy nhất là form Tạo/Sửa Vấn đề dùng bảng `FileAttachmentTable` (cột loại tài liệu), còn form Nhiệm vụ dùng khối chip; 2 tab Chi tiết đã cùng khuôn chip. Xem trước có sẵn: `components/modal/FilePreviewModal.vue` + `utils/file-preview.js` (ảnh · PDF iframe · Word/Excel/PowerPoint qua Office Online) — đang dùng ở V2BaseFile / FileAttachmentTable / V2BaseFileList. Đã làm (worktree gop_db-client, chưa commit):
  - `plugins/file-preview.js` (mới, đăng ký `nuxt.config.js`): `this.$previewFile({name,file_name,file_path,file_size})` mount `FilePreviewModal` 1 lần (z-index 1070 cao hơn panel), cùng khuôn `plugins/image-viewer.js`.
  - `utils/attachmentOpen.js` (mới, dùng chung): `isImageAttachment` / `imageAttachments` / `canPreviewAttachment` / `openAttachment(vm, f, siblings)` — ảnh → `$viewImages`, pdf/Office → `$previewFile`, khác → mở tab. Nhận cả khuôn `{file_name,file_path}` (Task/Issue) lẫn `{name,url}` (bình luận).
  - Chip tệp ở `TaskForm` / `TaskDetailTab` / `IssueDetailTab` / `IssueForm`: tên tệp xem trước được thành bấm được (`.nm-pv`, gạch chân khi rê), thêm icon 👁 "Xem trước" cho pdf/Office (ảnh đã có thumbnail), giữ Tải xuống / Xóa. `CommentNode`: bấm tên tệp pdf/Office mở xem trước, Ctrl/Cmd+bấm vẫn mở tab. CSS `.tkp-file > span.nm-pv` ở `task-panel.scss`.
  - `IssueForm.vue`: thay `FileAttachmentTable` bằng khối chip copy từ `TaskForm.vue` (tiêu đề "Tệp đính kèm / chứng cứ", đếm "n tệp", `V2BaseFile` Tải lên, `uploadTaskFiles` cùng đuôi + 50 MB như Nhiệm vụ, lỗi BE `attachments` hiện `V2BaseError`). Bỏ ô Loại tài liệu: BE `IssueAttachmentRequest` / `IssueUpdateStatusRequest` khai `attachment_type_id` nullable, gửi null. Dán ảnh → `onPickFiles` trực tiếp. **Trả `FileAttachmentTable.vue` về nguyên bản** (gỡ `addPickedFiles` vì không còn chỗ dùng).
  - `TaskPanel` / `IssuePanel` `onKey`: Esc khi `FilePreviewModal` đang mở thì không đóng panel (cùng khuôn guard trình xem ảnh).
  - Test Playwright :3002: form Tạo vấn đề dán ảnh → chip thumbnail; tải `tai-lieu-test.pdf` qua Tải lên → chip icon PDF + 👁, "2 tệp"; bấm 👁 → FilePreviewModal mở PDF (iframe, không lỗi), Esc đóng modal mà form còn; bấm thumbnail → trình xem ảnh, Esc giữ form. Tab Chi tiết Nhiệm vụ 1944: tải PDF → chip 👁, bấm tên → xem trước OK, Esc giữ panel. Bình luận Task 1944 kèm PDF → POST 200, bấm tên tệp → xem trước PDF OK, Esc giữ panel. Không có lỗi console liên quan.
  - App TPE_APP: Vấn đề và Nhiệm vụ đã cùng `WorkFileRow`; tệp không phải ảnh đang tải về rồi mở bằng app hệ thống (`MeetingFileActions.view`) — không sửa thêm.
  - User hỏi app có xem trước PDF/Office trong app được không: app chưa có trình xem trong app ở chỗ nào (chat/meeting/task đều tải về rồi `open_file` → iOS Quick Look, Android tuỳ máy). Đề xuất 2 mức (giữ nguyên / thêm màn WebView + gói PDF dùng chung cho 4 nơi, ~nửa ngày) — chờ user chọn.
  - (25/11) User chốt đẩy: web commit `f298bbd04` push `gop_db`; merge `gop_db` → `develop` không conflict, merge commit `199e77037` push `develop`. Build PROD + DEV bằng `~/build_tpe.sh` (log `~/build_tpe_20261125b.log` mỗi máy) → cả 2 "Hoàn tất build phía frontend"; PROD `last_deployed_client_commit` = f298bbd04, DEV = 199e77037; hrm.eteksofts.com + dev-hrm đều trả 200 (log có WARNING `favicon.ico` "Module parse failed" là cảnh báo cũ, build trước cũng có). **Đã deploy PROD + DEV 25/11/2026.**
- [x] (25/11) Đẩy code theo yêu cầu user: app → `develop` commit `ea382f0` (chưa build app); web → `gop_db` commit `35ddb007b` (rebase lên commit chat GĐ42 của người khác, không conflict). Build PROD: `~/build_tpe.sh` trên hrm-prod (log `~/build_tpe_20261125.log`) → backend pull + worker/socket restart OK, frontend build xong, pm2 `hrm-client-tpe` online, `last_deployed_client_commit` = 35ddb007b, https://hrm.eteksofts.com/login trả 200. **Đã deploy PROD 25/11/2026.**
- [x] (25/11) User yêu cầu thêm: merge `gop_db` → `develop` (hrm-client) để build cổng DEV. Làm trong worktree tạm, 1 conflict `TaskForm.vue` ô "Số giờ được giao": develop bỏ `required` (nghiệp vụ, commit 14038a832 "không bắt buộc") vs gop_db đổi bố cục (`key="hours"` + `workRowCol`) → giữ bố cục gop_db + nhãn không bắt buộc của develop. Merge commit `313ec4cad` đã push `develop`. Build DEV: `~/build_tpe.sh` trên hrm-dev (log `~/build_tpe_20261125.log`) → xong, `last_deployed_client_commit` = 313ec4cad, dev-hrm trả 200. **Đã deploy DEV 25/11/2026.**

