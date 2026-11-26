# Chat — GĐ44 Thanh định dạng văn bản khi soạn tin nhắn + bình luận (web & app) — design (tóm tắt) — @cuong61n

> Yêu cầu 26/11/2026 (chưa có số Redmine): thanh công cụ định dạng trong khung soạn tin Chat — đậm / nghiêng / gạch chân /
> gạch ngang / kiểu chữ / cỡ chữ / màu chữ / màu nền · danh sách • và 1. · tăng / giảm thụt lề · hoàn tác / làm lại ·
> mở rộng khung (phím tắt Ctrl + Shift + X) · bật / tắt thanh định dạng · gửi đi giữ nguyên định dạng · hiển thị thống nhất
> mọi thiết bị. Tham khảo Zalo. User bổ sung trong phiên: **áp cả cho khung BÌNH LUẬN** (Nhiệm vụ / Vấn đề).
> Thiết kế Pencil trước để user duyệt, rồi mới code.

## Hiện trạng (đã rà 26/11)
- **Web chat** `components/chat/ChatComposer.vue` (1.195 dòng): `V2BaseTextarea` + lớp tô nền @ (`cc__hl`); hàng công cụ
  (📎 @ # thăm dò chụp màn emoji) + nút Gửi nằm DƯỚI ô chữ trong khối bo 12px (GĐ8). Bong bóng `ChatMessageItem.html()`:
  escape → tô @Tên / @all → link → `\n` ⇒ `<br>`. `body` là chữ thuần, BE `SendMessageRequest` `max:5000`.
- **Web bình luận** `components/comments/CommentEditor.vue`: `contenteditable` + chip @; gửi `comment` chữ thuần;
  `CommentNode` đã `v-html="renderContent(...)"`. BE `TaskCommentController` `comment required|string|max:5000`.
- **App chat** `ui/chat/widget/composer.dart`: `TextField` 1–5 dòng + 😊 + nút gửi tròn; bong bóng `message_bubble.dart`
  vẽ `TextSpan` (tô @ + link). **App bình luận** `ui/task/task_comments_page.dart` (2.474 dòng).
- App ĐÃ có `flutter_quill` 11.5 + `flutter_quill_delta_from_html` + `vsc_quill_delta_to_html` + `flutter_widget_from_html`
  (dùng ở `meeting_rich_editor.dart` cho CKEditor của Meeting) ⇒ không thêm gói mới.
- Web có `quill` 2.0.2 + `vue-quill-editor` + CKEditor 5 trong package.json (dùng cho form khác).

## Thiết kế (Pencil `~/Downloads/meeting-mobile_v2.pen`, hàng y = 1600 / 2260 / 2900, x từ 18791)
- WEB 1 tắt (mặc định) · WEB 2 bật (hàng định dạng TRÊN ô chữ, nút Aa sáng) · WEB 3 mở rộng (⤢ / Ctrl+Shift+X, ô chữ ~300px) ·
  WEB 4 popover cỡ chữ + kiểu chữ, bảng 12 màu chữ, bảng 12 màu nền · WEB 5 tin đã gửi giữ định dạng ·
  WEB 6 khung bình luận Nhiệm vụ / Vấn đề dùng chung thanh.
- APP 1 nút Aa trong ô nhập · APP 2 thanh định dạng nằm trên bàn phím, cuộn ngang · APP 3 bảng màu thay bàn phím (tab Màu chữ /
  Màu nền) · APP 4 mở rộng toàn màn (đầu màn "Soạn tin nhắn" + Gửi) · APP 5 bong bóng giữ định dạng · APP 6 bình luận nhiệm vụ.
- Khung "Ghi chú logic & quyết định đề xuất" (8 mục) cạnh APP 6.

## Đề xuất kỹ thuật (chờ user duyệt)
1. Lưu `body` / `comment` là **HTML an toàn** (whitelist b i u s span[style: color|background-color|font-size|font-family] ul ol li p br a);
   sanitize ở BE (HTMLPurifier) + FE; tin cũ không thẻ hiển thị như cũ; 5.000 ký tự đếm theo chữ thuần; BE trả thêm `body_text`
   cho xem trước / trích dẫn / ghim / tìm kiếm / push / nháp.
2. Web: 1 component chung `components/chat/RichComposerToolbar.vue` + ô soạn `contenteditable` (đã có khuôn ở CommentEditor),
   thay `V2BaseTextarea` trong ChatComposer; giữ @ / # / emoji / dán ảnh / tô @all.
3. App: ô soạn `QuillEditor` + thanh tự dựng theo `app-components`; bong bóng `flutter_widget_from_html`; cùng bảng màu / 4 cỡ chữ.
4. Bật / tắt nhớ theo người dùng (localStorage / SharedPreferences), chung chat + bình luận.
5. Phím tắt web: Ctrl+B/I/U · Ctrl+Shift+S · Ctrl+Shift+7/8 · Tab/Shift+Tab (trong danh sách) · Ctrl+Z/Y · Ctrl+Shift+X · Esc.

## Quyết định đã chốt (user 26/11/2026)
(a) **Enter vẫn GỬI như cũ** kể cả đang ở trong danh sách; Shift+Enter xuống dòng (trong danh sách = mục mới, Shift+Enter ở mục rỗng = thoát danh sách).
(b) **Cỡ chữ 4 mức cố định** 12 / 14 / 18 / 22 — không nhập số.
(c) Sửa tin / bình luận: **chỉ tự mở thanh định dạng khi nội dung đang sửa CÓ định dạng** (body chứa thẻ); tin thuần giữ trạng thái bật/tắt người dùng đã chọn.
(d) **Chưa áp** cho ô Mô tả nhiệm vụ / vấn đề.
