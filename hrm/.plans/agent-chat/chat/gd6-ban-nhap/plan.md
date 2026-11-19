# GĐ6 chat — Bản nháp tin đang soạn theo hội thoại

> 13/11/2026. Lỗi: gõ dở ở nhóm A ⇒ sang nhóm B / 1–1 khác ⇒ quay lại mất chữ. Nguyên nhân: `pages/assign/messages` gắn
> `ChatPane :key` theo hội thoại ⇒ ô soạn bị huỷ/dựng lại. User chọn "Đầy đủ" + "làm". Chỉ hrm-client, nhánh
> `gop_db-chat-ban-nhap` (tách origin/gop_db 514bc3c67), worktree wt-nhom-trao-doi.

## Đã làm
- [x] `utils/chat/chatDrafts.js`: localStorage `chat_drafts_v1_{employees.id}`, khoá id hội thoại | `to-{employees.id}` (1–1 chưa nhắn); giữ 7 ngày, ≤ 50 hội thoại; chỉ giữ khi có chữ / tệp đã tải / thẻ #. Khuôn dữ liệu sẵn để đợt app thay bằng API (đồng bộ thiết bị).
- [x] `store/chat.js`: `drafts`, `initDrafts`, `saveDraft` (cột hội thoại đọc).
- [x] `ChatComposer`: prop `draftKey`; mở ⇒ khôi phục chữ, @, tệp đã tải (ảnh nhỏ = URL), thẻ #, khung trả lời (emit `restore-reply`), con trỏ cuối; mọi thay đổi ⇒ lưu (giãn 400ms) + lưu ngay khi rời; gửi xong (reset) ⇒ xoá nháp. Sticker / ảnh chụp gửi riêng giữ nháp. Bấm "Sửa" tin cũ: cất nháp, xong/huỷ sửa trả lại (trước đây mất).
- [x] `ChatPane`: `draftKey`, nhận `restore-reply`. `ConversationList` nạp nháp khi mở. `ConversationRow`: hội thoại KHÔNG đang mở có nháp ⇒ "Bản nháp: …" (nhãn cam #D97706; đang có người soạn thì ưu tiên dòng "đang soạn").
- [x] E2E E10 (chuyển 1–1 B ⇄ C trong phiên, F5, Sửa tin cũ, gửi xong hết nháp, màu nhãn) — chat-thong-bao-emoji 10/10 + chat-core/bo-sung/toolbar-zalo/gd2 29/29.
- Ghi chú hành vi sẵn có: Esc khi đang sửa tin huỷ luôn khung "Trả lời" (vào sửa cũng bỏ trả lời) — giữ nguyên.

### Checkpoint — 13/11/2026 ~20:00
Vừa hoàn thành: code + e2e; commit + push, gop_db fast-forward hrm-client 514bc3c67..a108b98e2.
Bước tiếp theo: deploy TPE (chỉ build client).
