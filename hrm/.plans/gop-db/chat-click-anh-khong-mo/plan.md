# Chat nhóm: bấm vào ảnh nhiều lúc không mở được (chưa có số Redmine) — @cuong61n

Nhánh `gop_db` · phản hồi từ người dùng: "click vào ảnh trong nhóm chat nhiều lúc click không được".

- [x] 23/11/2026 — Điều tra WEB (`hrm-client` `components/chat/ChatMessageItem.vue` → `ChatPane.vue` → `ChatImageViewer.vue`), Playwright :3002 nhóm [TEST-ISSUECHAT]:
  bấm ảnh mở được khung xem; đo 121 điểm trên 1 ảnh khi rê chuột (thanh thao tác nổi hiện) — 0 điểm bị che. Chưa tái hiện được lỗi ở trường hợp bình thường.
  Điểm yếu đọc từ code (CHƯA tái hiện): `onImageClick` luôn `preventDefault` rồi chỉ emit; `ChatImageViewer` nạp lười (`() => import`) nên `$refs.imageViewer` rỗng nếu chunk chưa nạp / nạp lỗi (tab cũ sau deploy) ⇒ bấm không có gì xảy ra, không báo lỗi.
- [x] 23/11/2026 — Điều tra APP (`TPE_APP` `ui/chat/room/chat_room_page.dart:641` `_openViewer`): ĐƯỜNG LỖI IM LẶNG CÓ THẬT (đọc code, chưa chạy app).
  Bubble vẽ ảnh + cho bấm cả với tin TẠM (id âm, đang gửi, ảnh đọc từ máy), nhưng `ChatViewerImage.fromMessages` (image_viewer_page.dart:29) loại tin tạm và ảnh không phải http ⇒ `index < 0` ⇒ `return` không làm gì. Vừa gửi ảnh / mạng chậm / gửi lỗi (tin tạm kẹt) thì bấm ảnh không mở.
- [ ] Chờ user chốt: lỗi báo từ web hay app; cách sửa.
