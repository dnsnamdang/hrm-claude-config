# GĐ20 — Đóng ngăn chat sớm ⇒ nhóm "câm" (15/11/2026)

**Lỗi** (có sẵn từ GĐ10/15, phát hiện khi làm e2e GĐ19): ngăn mở hội thoại NHÓM ⇒ `WorkspaceView` chỉ dựng `ChatPane` sau
khi API nhóm trả về. Đóng ngăn trước lúc đó ⇒ pane dựng muộn gọi `setActive(convId)` khi ngăn đã đóng ⇒ `activeId` kẹt ⇒
tin tới nhóm đó không toast (shouldNotifyChat coi đang xem) và không cộng chưa đọc, tới khi mở lại ngăn.

**Tái hiện** (`scratchpad/early.mjs`, chặn API `workspaces/{id}` trễ 3s, đóng ngăn sau 300ms): ngay sau đóng
`activeId null` ⇒ 5s sau `activeId 6293, open false`. Sau sửa: 5s sau vẫn `null`.

**Sửa** (hrm-client, nhánh `gop_db-chat-ngan-dong-som`):
- `components/chat/ChatDrawer.vue` provide thêm `chatInDrawer: true`.
- `components/chat/ChatPane.vue` `inject: { chatInDrawer: { default: false } }`; `reset()`: trong ngăn mà ngăn đóng ⇒ không
  `setActive` (mở lại ngăn thì `ChatDrawer.onOpened` tự đặt). Màn chat toàn trang không đổi (không có provide).

- [x] Tái hiện + đo trước/sau
- [x] e2e `chat-drawer.spec.ts`: thêm N10 (đóng sớm ⇒ activeId null, tin tới toast + unread 1, mở lại ⇒ đã đọc); bỏ đoạn chờ
      tạm ở N8 (N9 qua mà không cần) ⇒ 10/10. chat-giao-dien 5/5 · chat-core 8/8.
- [x] Commit `8ba077abb` ⇒ gop_db + nhánh gop_db-chat-ngan-dong-som ⇒ ĐÃ DEPLOY TPE 15/11 (client `8ba077abb`, api `4d694d95a`, EXIT 0, Nothing to migrate, site 200)
