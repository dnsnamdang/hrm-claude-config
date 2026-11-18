# Push tin nhắn chat realtime trên app (không số Redmine) — @cuong61n

Nhánh: `gop_db` (worktree `worktrees/gop_db-api`). Người phụ trách: @cuong61n.

## Nghiệp vụ
Nhắn tin xong, người nhận phải thấy thông báo trên app ngay, không chờ 15–20s như trước.

## Task
- [x] 18/11/2026 — Điều tra prod TPE: worker `tpe-chat-push-worker` chạy bình thường, 0 job lỗi, `PushChatMessage` median 0s. Nguyên nhân độ trễ là `PushChatMessage::DELAY_SECONDS = 20` (cố ý, để gộp tin dồn + bỏ push khi đã đọc trên web). Nhóm >50 người còn chịu thêm ~17s/lô do `SendChatPushBatch` gửi FCM tuần tự (350 lần đo: median 17s).
- [x] 18/11/2026 — Đặt `DELAY_SECONDS = 0`, listener `PublishChatActivity` chỉ gọi `->delay()` khi >0; sửa test `listener_hen_job_tre…` thành khẳng định không trễ. Gộp tin dồn vẫn còn nhờ collapse key (iOS/Android gộp theo hội thoại) và "N tin mới".
- [x] 18/11/2026 — Kiểm: `php -l` OK; `ChatPushStickerTest` 7 pass / 4 fail, 4 fail giống hệt trước khi sửa (thiếu cột `mention_all` ở DB local chưa migrate), test liên quan push đều pass.
- [x] 18/11/2026 — Giữ hành vi "đã đọc trên web thì không push": `PushChatMessage` tách người nhận theo `ChatPresence` (Redis `chat_online`). Không mở web → push ngay; đang mở web → hẹn job trễ 5s (`WEB_READ_GRACE_SECONDS`) chỉ cho nhóm này, job đó đọc lại `last_read` nên đã đọc thì bỏ. Redis hỏng → coi như không ai online → push ngay. Thêm tham số `onlyEmployeeIds` cho job.
- [x] 18/11/2026 — Kiểm: thêm 2 test (người online web được hẹn job trễ; job trễ chỉ xét đúng người được giao và bỏ người đã đọc) đều pass; test nhóm đông chia lô vẫn pass; 4 test fail cũ do DB local thiếu cột `mention_all`, không liên quan.
- [ ] Chờ commit + deploy prod (`~/build_tpe.sh`) rồi đo lại độ trễ thực tế bằng tin nhắn thật.
- [x] 18/11/2026 — Nhóm đông (mục 1): gửi FCM SONG SONG 10 request/lần qua HTTP v1 (`app/Infrastructure/NotifyService/FcmConcurrentSender.php`, `FCMService::sendMany`, `SendChatPushBatch::sendAll`). Thân message vẫn do kreait `CloudMessage` dựng nên giống cách gửi tuần tự cũ; token OAuth từ FIREBASE_CREDENTIALS cache 50 phút, 401 thì làm mới + gửi lại đúng cái bị 401; lỗi từng message chỉ ghi log. Giữ nguyên chặn push cho tài khoản tắt chuông (`NotificationMuteService`, commit 0dff9a0ce của phiên khác).
- [x] 18/11/2026 — Nhóm đông (mục 2): lô `SendChatPushBatch` vào hàng riêng `chat-push-bulk` (env `CHAT_PUSH_BULK_QUEUE`, config `assign.chat_push_bulk_queue`; trống → rơi về hàng chat-push) để chat 1-1 không chờ sau nhóm đông.
- [x] 18/11/2026 — Kiểm local: 5 test mới `Modules/Assign/Tests/Unit/FcmConcurrentSenderTest.php` (MockHandler: gửi đủ không trùng/sót, lỗi từng message, 401 làm mới token, rỗng, thân message sendMany) + test hàng bulk đều pass. Chưa kiểm với Google thật (local không có file credentials).
- [x] 18/11/2026 — PROD: thêm supervisor `/etc/supervisor/conf.d/tpe-chat-push-bulk-worker.conf` (1 tiến trình, queue chat-push-bulk), đã `reread/update`, RUNNING; worker chat-push cũ không bị đụng. Chưa đặt `CHAT_PUSH_BULK_QUEUE` trong .env (đặt SAU khi deploy code).
- [x] 18/11/2026 — Đã commit + push `gop_db` (`04c93d945`) và deploy backend prod (pull, route:cache, queue:restart; không migration, FE không đổi). Chạy thử `validate_only` với Google thật: 30/30 thành công trong 1,5s (≈ 2,5s cho lô 50, trước ≈ 17s).
- [x] 18/11/2026 — PROD `.env`: thêm `CHAT_PUSH_BULK_QUEUE=chat-push-bulk` (bản sao `.env.bak_bulkqueue_20261118`), queue:restart, config đã nạp, 2 worker chat-push + chat-push-bulk RUNNING.
- [ ] Đo thực tế bằng tin nhắn thật: nhắn 1-1 (kỳ vọng push ngay) và nhóm >50 người (kỳ vọng `SendChatPushBatch` vài giây) trong /var/log/laravel/chat-push-worker.log + chat-push-bulk-worker.log.

## Trạng thái
Đã push `gop_db` (04c93d945) + deploy prod 18/11/2026. Chờ đo bằng tin nhắn thật.

- Ghi chú: `chat_online` chỉ biết có socket, không biết tab hiện/ẩn ⇒ web mở nền vẫn trễ 5s. Muốn chính xác hơn phải thêm trạng thái "đang xem hội thoại" ở FE + `server_node/server.js` — chưa làm.
