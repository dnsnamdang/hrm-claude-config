# GĐ19 — Chat nhóm đông (~600 người): bỏ phát "đã đọc" thừa, chia lô push, gom đếm chưa đọc

> 15/11/2026 · Trạng thái: **THIẾT KẾ — chờ duyệt** (chưa code). Nguồn đọc: `origin/gop_db` hrm-api + hrm-client
> (prod api `3fefb0545`, client `37dcfc173` trên gop_db) + cấu hình worker prod đọc qua ssh (chỉ đọc).
> Số thời gian dưới đây là **ước tính, chưa đo**.

## 1. Vì sao

User hỏi: nhóm ~600 người gửi thông báo có chậm không. Lần code thấy:

| # | Chỗ | Hiện trạng | Hệ quả với 600 người |
|---|---|---|---|
| A | `ConversationService::markRead()` (dòng ~340) | Mỗi lần 1 người đọc ⇒ `ChatActivity('conversation.read')` tới **mọi thành viên** | 1 người đọc = 12 job `PublishChatBatch` (lô 50) + 600 lượt Redis. 200 người đang mở nhóm cùng đọc 1 tin ⇒ ~2.400 job + 120.000 publish/tin ⇒ hàng `hrm` ùn, tin realtime tiếp theo xếp sau |
| B | `PushChatMessage::handle()` | 1 job gửi FCM **tuần tự** cho mọi người chưa đọc (`messaging->send` từng topic) | ~600 × 0,1–0,3s ≈ 1–3 phút. Worker hàng `hrm` trên prod: **1 tiến trình**, không `--timeout` ⇒ mặc định 60s, `--tries=1` ⇒ quá 60s bị giết, người chưa tới lượt **mất push**; trong lúc chạy, mọi job HRM khác chờ |
| C | `store/chat.js` `applyEvent` `message.created` | Mỗi máy online (không mở hội thoại đó) gọi `GET chat/unread-count` **sau mỗi tin** | ~600 request dồn cùng 1 thời điểm cho mỗi tin |

Ai dùng `conversation.read` của NGƯỜI KHÁC: chỉ `ChatPane.vue:667` — và chỉ khi `detail.type === 'direct'` (hiện "Đã xem"
chat 1–1). `store/chat.js:310` chỉ xét sự kiện của CHÍNH MÌNH (đồng bộ tab khác). App mobile chưa có màn chat ⇒ không dùng.
⇒ Ở nhóm, phát "đã đọc" cho người khác là thừa hoàn toàn.

## 2. Mục tiêu / không làm

- Mục tiêu: nhóm 600 người — tin hiện trên web mọi người ≤ ~1–2s; push điện thoại tới **đủ** người chưa đọc; 1 tin không làm
  nghẽn job HRM khác; số request dồn về API mỗi tin giảm rõ.
- Không làm: tính năng "đã xem" cho nhóm (chưa có, không thêm); đổi cơ chế socket/Redis; đổi nội dung push; đổi luật ai
  được push (giữ nguyên `pushes()` — người chưa đọc, đang làm việc, không tắt thông báo trừ khi bị @).
- Chống mục tiêu: chat 1–1 mất "Đã xem"; tab khác của chính mình không tắt số chưa đọc khi đọc ở tab này; push gửi trùng.

## 3. Các phương án đã cân nhắc

**Push (B):**
1. **Chia lô job (đề xuất)** — job trễ 20s giữ nguyên phần tính `pushes()` (chỉ query, nhanh), rồi chia danh sách thành lô
   50 ⇒ mỗi lô 1 job `SendChatPushBatch` gửi tuần tự (~50 × 0,3s ≈ 15s < 60s). Ít đổi code, test `pushes()` giữ nguyên.
2. `sendAll` / `sendMulticast` của kreait — **loại**: dự án đang `kreait/firebase-php 5.19.0`, 2 hàm này đi qua endpoint
   batch cũ của FCM mà Google đã tắt (06/2024) ⇒ gửi hỏng im lặng. Nâng SDK vướng psr/http-message (xem memory
   sdk-claude-php-khong-cai-duoc-hrm-api).
3. Tự gọi FCM v1 song song bằng Guzzle pool — nhanh nhất nhưng phải tự lo OAuth token, mã lỗi; để dành khi nhóm > vài nghìn.

**Hàng đợi:** lô push + lô realtime vẫn chạy chung worker `hrm` (1 tiến trình) ⇒ nhóm 600: 12 lô push × ~15s ≈ 3 phút
chiếm worker. Đề xuất đưa **push chat** sang hàng riêng `chat-push` + 1 worker riêng trên VPS (`--timeout=120`). Đây là việc
**vận hành trên prod** (thêm tiến trình) ⇒ tách thành bước riêng, hỏi riêng.

**Đã đọc (A):** (đề xuất) nhóm/không gian ⇒ chỉ gửi cho chính người đọc; chat 1–1 ⇒ giữ gửi cả 2 người. Phương án khác
(giữ phát cho cả nhóm nhưng gộp theo thời gian) — loại vì không ai dùng dữ liệu đó.

**Đếm chưa đọc (C):** (đề xuất) tính tại máy khi hội thoại có trong danh sách: chỉ khi hội thoại đổi từ 0 ⇒ có chưa đọc
mới đổi tổng (+1), không gọi API; hội thoại không có trong danh sách ⇒ gọi API nhưng **gom + lệch ngẫu nhiên 1–3s**
(tránh 600 máy cùng gọi 1 lúc). Phương án gửi sẵn tổng chưa đọc trong gói socket — loại vì phải tính cho từng người ở BE.

## 4. Thiết kế chọn

### BE (hrm-api, nhánh mới từ origin/gop_db)
1. `ConversationService::markRead()`: `$recipients` = `[$me]` khi hội thoại không phải `direct`; `direct` giữ mọi thành viên.
2. `PushChatMessage::handle()`: `pushes()` giữ nguyên; kết quả `array_chunk(…, 50)` ⇒ `SendChatPushBatch::dispatch($chunk)`
   (job mới, `tries=1`, gửi tuần tự như cũ, `setCollapseKey('chat_'+conv)`). ≤ 50 người ⇒ gửi luôn trong job hiện tại
   (giữ hành vi nhóm nhỏ, không thêm job).
3. (Bước vận hành, hỏi riêng) `SendChatPushBatch` + `PushChatMessage` `onQueue(config('assign.chat_push_queue', 'hrm'))` —
   mặc định vẫn `hrm` ⇒ deploy code không đổi gì cho tới khi đặt env `ASSIGN_CHAT_PUSH_QUEUE=chat-push` VÀ đã có worker.

### FE (hrm-client)
4. `store/chat.js` `message.created`: hội thoại có trong danh sách ⇒ nếu `unread_count` cũ = 0 (và chưa `marked_unread`)
   thì `commit('setUnread', unread + 1)`, KHÔNG gọi API; ngược lại không đổi. Hội thoại chưa có trong danh sách ⇒ đã đi
   `scheduleRefresh` (giữ). `conversation.read` của chính mình ⇒ trừ tại máy khi hội thoại đang có chưa đọc; khác thường thì
   gọi `fetchUnread` có gom + lệch 1–3s.
   Luật phải khớp BE `ConversationService::unreadSummary()` (đã đọc): đếm số HỘI THOẠI có `marked_unread = 1` hoặc còn tin
   chưa đọc, **bỏ hội thoại đã tắt thông báo (`muted`) và nhóm đã đóng**. ⇒ FE chỉ +1 khi hội thoại không `muted`, không
   `workspace.is_closed`, trước đó `unread_count = 0` và chưa `marked_unread`. Mọi ca khác giữ nguyên tổng.

## 5. Kiểm chứng

- PHPUnit: `ChatRealtimeTest` thêm ca — nhóm 3 người: `markRead` chỉ publish 1 kênh (`user_notification_{me}`); 1–1: 2 kênh.
  `ChatPushStickerTest`/ca push: 120 người chưa đọc ⇒ 3 job `SendChatPushBatch` (50/50/20), không gửi trùng ai; ≤ 50 ⇒ 0 job.
- Đo local (script scratch, FCM giả lập trễ 0,2s): nhóm giả 600 người — đếm job + thời gian trước/sau cho 1 tin và 200 người đọc.
- e2e chat chạy lại toàn bộ (drawer, core, thong-bao-emoji, bo-sung, giao-dien, zalo); thêm ca: chat 1–1 vẫn hiện "Đã xem";
  đọc ở tab A ⇒ tab B tắt số chưa đọc; tin mới ở hội thoại không mở ⇒ số đỏ +1 mà không gọi `unread-count`.

## 6. Phạm vi đụng (khi được cho "làm")

- hrm-api: `Modules/Assign/Services/Chat/ConversationService.php`, `Modules/Assign/Jobs/Chat/PushChatMessage.php`,
  mới `Modules/Assign/Jobs/Chat/SendChatPushBatch.php`, (bước 3) `config/assign.php`; test `Modules/Assign/Tests/Feature/Workspace/*`.
- hrm-client: `store/chat.js`.
- Không migration, không quyền. Bước 3 thêm worker trên VPS = việc prod, hỏi riêng.

## 7. Câu hỏi còn mở (chờ user)

1. Có làm bước 3 (hàng `chat-push` + worker riêng trên VPS TPE) trong đợt này không, hay chỉ làm 1–2–4 trước?
2. Có muốn đo local (mục 5) TRƯỚC khi code để có số so sánh không?
