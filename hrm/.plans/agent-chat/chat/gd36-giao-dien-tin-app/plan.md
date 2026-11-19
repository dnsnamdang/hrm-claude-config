# GĐ36 — Giao diện tin nhắn app (18/11/2026)

- Thử 2 vòng phương án: `mockup.html` (A xanh thương hiệu / B bạc hà Inter / C gradient) và `mockup-v2.html` (tham khảo Telegram · iMessage · Teams · Slack). User chốt: **giữ như hiện tại, chỉ chữ rõ + đậm hơn chút**.
- Đã sửa (TPE_APP, nhánh `feature/chat-chu-ro-dam` từ origin/develop 98ec972, worktree wt-tpe-app-chat, CHƯA commit theo thói quen user):
  - `app/lib/ui/chat/chat_theme.dart`: bỏ `mineText`, thêm `messageText = #0F172A`.
  - `app/lib/ui/chat/widget/message_bubble.dart` `_text()`: thân tin w500, màu `messageText` cho cả tin mình lẫn người khác (trước w400, #1F2937 / #111827). `ChatColors.text` dùng chung các màn khác giữ nguyên.
- Kiểm: flutter test test/ui/chat 370 OK, analyze lib/ui/chat 0; máy ảo iPhone 18 Pro ảnh trước/sau `chu-truoc-sau.png`.
- Web không đổi.

## Đợt 2 — Header ưu tiên Chat, Bình luận thành tab (user chốt 1A + nhúng thật, 18/11/2026; mockup `mockup-v3-binh-luan.html`)
Nhánh `feature/chat-chu-ro-dam` (TPE_APP, wt-tpe-app-chat), không commit.
- [x] T1 icon Chat `forum_outlined` (chat_shortcut_button.dart) + test
- [x] T2 TaskCommentsPage `embedded` (không Scaffold / header / dải Xem nhiệm vụ) + `onCountChanged`
- [x] T3 Chi tiết nhiệm vụ: header [Chat, ⋮]; tab Chi tiết · Tiến độ · Bình luận (n) · Lịch sử; tab Bình luận = bình luận nhúng, ẩn thanh nút đáy
- [x] T4 Chi tiết vấn đề: header [Chat, ⋮]; dải tab Chi tiết · Bình luận (n) (+ Lịch sử nếu có API)
- [x] T5 gỡ WorkCommentHeaderButton nếu hết chỗ dùng; test widget; flutter test toàn app + analyze
- [x] T6 máy ảo: header, tab bình luận gửi được, mở từ thông báo vẫn màn riêng; ảnh trước/sau

### Checkpoint — 18/11/2026 19:15 (đợt 2 code xong, CHƯA commit)
Vừa hoàn thành: icon Chat `forum_outlined` mọi màn; màn Chi tiết nhiệm vụ / vấn đề header [Chat · ⋮] (bỏ chip bình luận, gỡ `WorkCommentHeaderButton`); tab "Bình luận (n)" nhúng `TaskCommentsPage(embedded: true, onChanged)` — tab nhiệm vụ: Chi tiết · Tiến độ · Bình luận · Lịch sử; tab vấn đề: Chi tiết · Bình luận ("Lịch sử" vẫn là nút mở màn riêng trong tab Chi tiết). Ở tab Bình luận thanh nút đáy ẩn, ô soạn ở đáy. Màn Bình luận riêng (thông báo / số 💬 ở danh sách) giữ nguyên.
Kiểm: flutter test 628 OK (+3 ca `test/ui/work/work_detail_comments_tab_test.dart`, + chat_shortcut_button_test icon mới); analyze chỉ còn 1 info có sẵn ở task_list_page.dart:416. Máy ảo: gửi bình luận trong tab nhiệm vụ (số 1→2) + vấn đề (0→1); nút Chat mở danh sách hội thoại; màn Bình luận riêng + "Xem nhiệm vụ" vẫn chạy. Ảnh: nv-chi-tiet-truoc.png · nv-tab-binh-luan-sau.png · vd-tab-binh-luan-sau.png.
Ghi chú: ở tab Bình luận khối đầu màn (trạng thái, tên, dải "Hoàn thành…") giữ nguyên nên vùng bình luận còn ~55% màn khi nhiệm vụ có dải trạng thái dài.
Bước tiếp theo: user xem máy ảo; user báo commit / push (nhánh feature/chat-chu-ro-dam, gồm cả chữ đậm đợt 1). Pen: vẽ lại khi pen.dev mở hạn mức.

### Checkpoint — 18/11/2026 19:25 (ĐÃ MERGE develop)
TPE_APP commit `231b2ce` (chữ tin đậm) + `1cf5872` (header ưu tiên Chat, tab Bình luận) trên `feature/chat-chu-ro-dam` ⇒ đã push nhánh + fast-forward `develop` 98ec972..1cf5872 (local = origin/develop = origin/feature). Chưa phát hành store.
