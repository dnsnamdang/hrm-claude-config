# GĐ18 — Xem ảnh trong ngăn kéo chat: tên người gửi bị che (15/11/2026)

**Lỗi:** mở ảnh trong ngăn kéo chat (icon topbar) ⇒ tên người gửi góc trên trái bị menu trái che (x 16→~95px), nút "‹ Ảnh trước" (left 20px) cũng bị che. Màn chat toàn trang không lỗi.

**Nguyên nhân (đo elementFromPoint):** `ChatImageViewer` dựng trong `.cdw` (fixed, z-index 1035 ⇒ stacking context) nên z-index 10000 của lớp xem ảnh chỉ có nghĩa bên trong ngăn; `body.chat-drawer-open .sale-cats/.left-side-menu` được đẩy lên 1038 ⇒ đè dải trái.

**Sửa:** `hrm-client/components/chat/ChatImageViewer.vue` — bọc `.civ-portal`, `mounted` đưa ra `<body>`, `beforeDestroy` gỡ. Không đổi giao diện.

- [x] Tái hiện + đo trước sửa (hit x=18 `cats-brand-ic`, x=56 `logo-box`)
- [x] Portal ra body; đo lại ngăn + toàn trang: mọi điểm trên tên + nút Ảnh trước là chính nó
- [x] e2e N8 `chat-drawer.spec.ts` (tên/nút trước không bị che, không nằm trong .cdw, 1 lớp portal, đổi hội thoại không cộng dồn)
- [x] Chạy lại: chat-drawer 8/8 · chat-thong-bao-emoji 10/10 (E8 xem ảnh) · chat-giao-dien 5/5
- [x] Commit + merge gop_db + push: `37dcfc173` (fast-forward)
- [ ] Deploy TPE — chờ user
