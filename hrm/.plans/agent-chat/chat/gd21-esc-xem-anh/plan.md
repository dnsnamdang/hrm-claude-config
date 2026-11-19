# GĐ21 — Esc khi xem ảnh trong ngăn chat đóng luôn ngăn

User báo 16/11/2026, cho "làm" 16/11. Nhánh `gop_db-chat-esc-xem-anh` (hrm-client, tách từ origin/gop_db 8ba077abb).

Nguyên nhân: `ChatDrawer` và `ChatImageViewer` cùng nghe `keydown` trên `document` pha capture; ngăn đăng ký trước
(lúc trang tải) nên nhận Esc trước. `stopPropagation()` của lớp ảnh không chặn listener cùng node; ngăn chỉ nhường
`.modal.show` (bootstrap) mà lớp ảnh portal ra body không phải modal ⇒ đóng cả ngăn. Có từ GĐ18.

- [x] Tái hiện Playwright (scratch esc.mjs): Esc ⇒ viewer đóng + `drawer.open=false`.
- [x] FE `components/chat/ChatDrawer.vue` `onKey`: có `[data-testid="chat-image-viewer"]` thì nhường.
- [x] Đo lại: Esc 1 ⇒ ảnh đóng, ngăn mở; Esc 2 ⇒ ngăn đóng.
- [x] e2e `chat-drawer.spec.ts` N8 thêm bước Esc khi xem ảnh ⇒ ngăn vẫn mở. Toàn bộ chat-drawer: 10/10.
- [x] 16/11 commit ddbcb7343 · merge gop_db (fast-forward) · push cả 2 nhánh · ĐÃ DEPLOY TPE (api 4d694d95a · client ddbcb7343, EXIT 0, Nothing to migrate, bundle có điều kiện mới, site 200).
