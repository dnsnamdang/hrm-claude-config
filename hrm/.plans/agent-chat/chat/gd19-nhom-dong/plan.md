# GĐ19 — Chat nhóm đông: plan

Design: `design.md` (cùng folder). User duyệt + "làm cả 4, không cần đo" 15/11/2026.
Nhánh: `gop_db-chat-nhom-dong` (hrm-api + hrm-client, tách từ origin/gop_db 3fefb0545 / 37dcfc173).

- [x] 1. BE `ConversationService::readRecipients()` — nhóm/không gian ⇒ chỉ người đọc; 1–1 ⇒ cả 2. `markRead()` dùng nó.
- [x] 2. BE `PushChatMessage::handle()` chia lô 50 ⇒ job mới `SendChatPushBatch` (`timeout 120`, `tries 1`); ≤ 50 gửi luôn.
- [x] 3. BE hàng riêng: `config('assign.chat_push_queue')` ← env `CHAT_PUSH_QUEUE` (trống = như cũ);
      `PushChatMessage::onChatQueue()` dùng cho job trễ (listener) + các lô.
- [x] 4. FE `store/chat.js`: `countsUnread()` (khớp BE `unreadSummary`); `message.created` ⇒ +1 tại máy khi hội thoại
      chuyển sang có chưa đọc, bỏ gọi `unread-count`; `conversation.read` của mình ⇒ −1 tại máy; `scheduleRefresh` lệch 0–3s.
- [x] PHPUnit: `ChatRealtimeTest::test_da_doc_nhom_chi_bao_nguoi_doc_1_1_bao_ca_hai`,
      `ChatPushStickerTest::test_nhom_dong_chia_lo_push_50_nguoi_vao_hang_rieng`, `…test_khong_dat_hang_rieng_thi_giu_hang_mac_dinh`.
      Toàn bộ test Chat: 114/114.
- [x] e2e `chat-drawer.spec.ts` N9 (số đỏ +1 tại máy, 0 request unread-count, đọc nơi khác −1, 1–1 vẫn "Đã xem"): 9/9.
- [x] e2e chat còn lại: core 8 · thong-bao-emoji 10 · bo-sung 6 · giao-dien 5 · zalo 9 — xanh hết.
- [x] Commit + merge gop_db + push cả 2 nhánh: api `4d694d95a` · client `bb1340929` (fast-forward).
- [x] 15/11 ĐÃ DEPLOY TPE code (api `4d694d95a` · client `bb1340929`, EXIT 0, Nothing to migrate, site 200; `assign.chat_push_queue` = NULL ⇒ push chạy hàng `hrm`, đã chia lô).
- [x] 15/11 ĐÃ BẬT hàng `chat-push` trên prod TPE: supervisor `tpe-chat-push-worker` (1 tiến trình, user erp_tpe, log `/var/log/laravel/chat-push-worker.log`) RUNNING ⇒ thêm `CHAT_PUSH_QUEUE=chat-push` vào .env (sao lưu `.env.bak_truoc_chat_push_20261115`) ⇒ queue:restart. config = "chat-push", 0 job kẹt. Gỡ: xoá dòng env ⇒ queue:restart ⇒ chờ hàng trống ⇒ xoá file supervisor. Trình tự đã làm:
      1. deploy code (env chưa đặt ⇒ push vẫn chạy hàng mặc định `hrm`, chỉ khác là đã chia lô);
      2. tạo `/etc/supervisor/conf.d/tpe-chat-push-worker.conf` (khuôn tpe-agent-worker):
         `php /var/www/tpe/hrm-api/artisan queue:work database --queue=chat-push --sleep=1 --tries=1 --timeout=150 --max-time=3600`,
         `user=erp_tpe`, **numprocs=1** (connection database `retry_after = 1` ⇒ 2 tiến trình có thể gửi trùng);
         `supervisorctl reread && update`;
      3. thêm `CHAT_PUSH_QUEUE=chat-push` vào `/var/www/tpe/hrm-api/.env` ⇒ `php artisan queue:restart`.
      Thứ tự bắt buộc 2 trước 3 (đặt env khi chưa có worker ⇒ push nằm chờ mãi).

## Ngoài luồng (ghi lại, chưa sửa)

- **Đóng ngăn chat sớm ⇒ nhóm vừa mở bị "câm"** (có sẵn từ GĐ10/15): ngăn mở hội thoại NHÓM (`WorkspaceView`) chỉ dựng
  `ChatPane` sau khi API nhóm trả về; đóng ngăn trước lúc đó ⇒ pane dựng muộn gọi `setActive(convId)` khi ngăn đã đóng ⇒
  `activeId` kẹt ⇒ tin tới nhóm đó không toast, không cộng chưa đọc cho tới khi mở lại ngăn. Tái hiện: e2e N9 lần đầu
  (DBG `activeId: 6291, open: false`). Hướng sửa: ChatPane trong ngăn chỉ `setActive` khi `drawer.open`.
