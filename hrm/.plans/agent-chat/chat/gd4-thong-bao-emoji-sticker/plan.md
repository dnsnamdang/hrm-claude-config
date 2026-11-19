# GĐ4 chat — Thông báo tin nhắn + Emoji + Sticker

> 13/11/2026. User: "Hoàn thiện thêm 1 số tính năng rồi deploy cùng: 1/ đẩy thông báo tin nhắn 2/ thư viện Emoji, sticker".
> Chốt (AskUserQuestion 13/11): **Web + push app** (không ghi chuông) · **tự dựng bảng emoji** (không thêm gói npm) · **bộ sticker tự host** (loại tin mới `sticker`).
> Deploy CÙNG đợt với chat bổ sung (`2026_11_15_000001`) + Agent cache 1h đang chờ trên gop_db.

## Hiện trạng (đã kiểm code origin/gop_db 13/11)

- Chat chỉ có socket realtime (`ChatSocket` → kênh `user_notification_{employees.id}` + `kind: 'chat'`) và badge số hội thoại chưa đọc ở topbar. Không toast, không âm thanh, không FCM. Bảng `chat_conversation_members.muted` đã có (tắt thông báo theo hội thoại) nhưng chưa dùng cho thông báo.
- FCM: `Modules/Timesheet/Jobs/SendNotification` → topic `FCM_TOPIC_PREFIX{employee_info_id}`, có `setCollapseKey`. Badge icon app = số chuông chưa đọc (`NotificationBadge`).
- App TPE chưa có màn chat; `notification_router.dart` loại lạ rơi vào `default`.
- Ô soạn tin không có emoji picker; reaction có 6 emoji cố định (`REACTION_EMOJIS`). `chat_messages.type`: text · system · card (varchar 20, không enum ⇒ thêm `sticker` không cần migration).

## Phạm vi

### 1. Thông báo tin nhắn
**BE (hrm-api, Modules/Assign)**
- Payload `message.created` thêm `notify`: `{ muted_ids: [...], mention_ids: [...] }` để web tự quyết có toast/âm thanh (tin mình gửi, hội thoại tắt thông báo ⇒ im; bị @ ⇒ vẫn báo dù tắt).
- Job mới `Jobs/Chat/PushChatMessage` (queue, **trễ 20 giây**): với mỗi người nhận chưa rời nhóm, không phải người gửi, không tắt thông báo (trừ khi bị @), **chưa đọc tới tin đó** (`last_read_message_id < id`) ⇒ bắn FCM qua `FCMService` tới topic `employee_info_id`:
  - Tiêu đề: 1–1 = tên người gửi; nhóm = tên nhóm. Nội dung: "Tên: nội dung (cắt 100 ký tự)" / "[Sticker]" / "[Tệp] tên" / "Tên đã nhắc bạn: …".
  - `collapseKey = chat_{conversation_id}` (nhiều tin ⇒ 1 thông báo trên máy). Data `type: 'chat_message'`, `id: conversation_id`. Không ghi bảng `notifications` (không vào chuông, không đổi badge icon).
  - Đọc trên web trong 20 giây ⇒ không push điện thoại. Tin hệ thống không push. Người nghỉ việc không push.
- Không đụng `SendNotification` / `EmployeeInfoService` dùng chung.

**FE (hrm-client)**
- Plugin/listener toàn cục (BasicSubsystem đang nghe socket `chat`): khi `message.created` của người khác, không bị tắt (hoặc bị @), và **không** đang mở đúng hội thoại đó với tab đang hiện ⇒
  - Toast góc màn (avatar + tên + nội dung ngắn, bấm ⇒ mở `/assign/messages?c=…`), tối đa 3 toast, gộp theo hội thoại.
  - Âm "ting" bằng WebAudio (không thêm file).
  - Tab ẩn ⇒ thông báo trình duyệt (`Notification` API) nếu đã cho phép.
- Tiêu đề tab: `(N) …` theo số hội thoại chưa đọc.
- Màn Tin nhắn: menu cài đặt nhỏ "Âm thanh thông báo" (bật/tắt, lưu localStorage) + "Bật thông báo trên trình duyệt" (xin quyền khi bấm).

### 2. Emoji
- `utils/chat/emojiData.js` sinh từ `emoji-test.txt` Unicode 15.1 (fully-qualified, ≤ E13.0 cho Windows 10, bỏ biến thể màu da + nhóm Cờ) — 8 nhóm, 1.536 emoji, 42 KB, tên tiếng Anh + từ khoá tiếng Việt ~100 emoji phổ biến. Sinh lại: `gen_emoji.py` (cùng folder).
- `ChatEmojiPicker.vue`: nút 😊 cạnh ô soạn ⇒ popup tab nhóm + "Dùng gần đây" (localStorage, 24 cái) + ô tìm. Chèn vào vị trí con trỏ của ô soạn. Popup dùng chung cho tab Sticker (2 tab: Emoji | Sticker).
- Reaction: thêm nút "+" ở hàng 6 emoji ⇒ mở picker chọn emoji bất kỳ (cột `emoji` varchar(16) utf8mb4_bin đủ chỗ; validate `ReactionRequest` max 16).

### 3. Sticker
- Nguồn: **Noto Animated Emoji (Google, CC BY 4.0)** — ảnh động webp; ghi công "Noto Emoji © Google, CC BY 4.0" ở chân tab Sticker. Dự phòng nếu tải không được/nặng: Fluent Emoji 3D (Microsoft, MIT, ảnh tĩnh).
- 3 bộ × ~16 sticker (Cảm xúc · Cử chỉ · Công việc/chúc mừng) tải về `hrm-client/static/stickers/{bo}/{ma}.webp`; danh mục `utils/chat/stickers.js` (KHÔNG để file .js dữ liệu trong `components/` — Nuxt tự đăng ký thành component, báo warning).
- Gửi: tin `type = 'sticker'`, `meta = {sticker: 'bo/ma'}`, body null. BE validate mã nằm trong danh mục (`Config/chat_stickers.php`). Hiển thị ảnh 120px, không bong bóng; trả lời / chuyển tiếp / thu hồi / ghim chạy như tin thường; xem trước ở danh sách hội thoại "[Sticker]".

## Không làm
GIF online · admin tải sticker · màn chat trên app (bấm push mở app trang chủ) · ghi chuông · đổi badge icon app.

## Kiểm
- PHPUnit: job push (bỏ qua người gửi / đã đọc / tắt thông báo / @ khi tắt / người rời nhóm; collapse key), sticker hợp lệ/không hợp lệ, reaction emoji ngoài 6 cái.
- E2E Playwright (`e2e/tests/assign/chat-*`): picker chèn emoji đúng con trỏ, tìm, gần đây; gửi sticker 2 phía; toast hiện khi ở trang khác / không hiện khi đang mở hội thoại / không hiện khi tắt thông báo; tiêu đề tab. Đo DOM. Chạy lại toàn bộ bộ chat.
- FCM: kiểm bằng stub (không bắn push thật — [[rehearsal-gui-push-that]]); push thật chỉ khi user cho phép, tới máy của user.

## Deploy (thêm vào đợt đang chờ)
Không migration mới. Prod TPE `QUEUE_CONNECTION=database` + worker `tpe-worker` (queue mặc định) ⇒ job `PushChatMessage` trễ 20 giây chạy được. Sau `build_tpe.sh`:
- `sudo supervisorctl restart tpe-worker:*` (BẮT BUỘC — worker giữ code cũ, không biết class job mới) + `tpe-agent-worker:*` (đợt Agent cache 1h) · `pm2 restart hrm-tpe-socket`.
- `.env` không cần thêm gì: `CHAT_PUSH_ENABLED` mặc định bật. Muốn tắt push điện thoại khẩn: đặt `CHAT_PUSH_ENABLED=false` + `php artisan config:clear` (nếu có cache).
- Kiểm sau deploy: gửi 1 tin cho NV khác rồi KHÔNG mở ⇒ sau ~20 giây máy họ nhận push; `SELECT COUNT(*) FROM jobs WHERE payload LIKE '%PushChatMessage%'` không tồn đọng.


## Checkpoint — 13/11/2026 ~15:30 (CODE XONG, CHƯA COMMIT)

Vừa hoàn thành: GĐ4 trên nhánh `gop_db-chat-thong-bao-emoji` (tách `origin/gop_db` 91b2cb8db / bb918e470), worktree `wt-nhom-trao-doi`.
- hrm-api: `ChatMessage::TYPE_STICKER` · `Services/Chat/ChatStickers.php` · `MessageService` (gửi / chia sẻ / thu hồi sticker) · `ChatPresenter` (`sticker`, `can_recall`, xem trước + trích dẫn "[Sticker]") · `SendMessageRequest.sticker` · `Jobs/Chat/PushChatMessage.php` · `PublishChatActivity` (muted_ids + conversation{type,name} + hẹn job) · `Config/config.php` `chat_push` · test `ChatPushStickerTest` (8). `.env` local thêm `CHAT_PUSH_ENABLED=false` (không commit).
- hrm-client: `utils/chat/chatNotifier.js` (toast gộp tại chỗ, âm thanh dùng `assets/audio/notification.mp3` thay WebAudio, thông báo trình duyệt khi tab ẩn, tiêu đề tab) · `BasicSubsystem.vue` (gọi notifier + `head().titleTemplate`) · `ConversationList.vue` (menu ⋮ cài đặt thông báo) · `components/chat/emoji/ChatEmojiPicker.vue` (tải lười) · `ChatComposer` (nút 😊, chèn tại con trỏ, gửi sticker giữ bản nháp) · `ChatMessageItem` (sticker 120px, nút "+" cảm xúc) · `ChatPane` (bảng emoji cảm xúc position fixed, `can_recall` sticker) · `utils/chat/{emojiData,stickers}.js` · `static/stickers/` (48 động ~2,35 MB + 48 thumb 136 KB + LICENSE.txt).
- Kiểm: PHPUnit Workspace 115 (2 fail CÓ SẴN trên origin/gop_db — `WorkspaceTaskTest::test_workspace_and_solution_are_exclusive`, `test_patch_field_enforces_workspace_rules`, đã chạy trên worktree tạm gop_db sạch cùng fail) + Task 31 OK. E2E mới `e2e/tests/assign/chat-thong-bao-emoji.spec.ts` 6/6; chạy lại chat-core + chat-bo-sung + chat-toolbar-zalo (sửa Z2: hàng emoji 6 → 7 nút) + chat-gd2-polish: 22 + 15 đạt.
- Lỗi bắt được nhờ Playwright: bảng emoji đè ô soạn (neo lại vào `.cc`); toast gộp bằng goAway+show để lại 2 toast trong DOM (đổi sang sửa chữ tại chỗ); `toast.text()` xoá mất nút × (chỉ sửa 2 span); `V2BaseInput` nuốt `data-testid` (inheritAttrs false).
- Chưa kiểm: `agent-chat-pin` (chạy trên :3070 worktree Agent, chưa có code này — ConversationList đổi phần đầu cột); push FCM thật tới máy (local tắt).
Bước tiếp theo: user xem thử :3080 → báo commit / merge gop_db → deploy cùng đợt (chat bổ sung + Agent cache 1h + GĐ4).

## Bổ sung 13/11 — Phím tắt emoji kiểu Zalo (user chọn "tự đổi khi gõ cách/Enter", cho phép "làm")
- [x] `hrm-client/utils/chat/emojiShortcuts.js`: 21 ký hiệu (:) :( :D :P ;) :o :'( :* <3 </3 :v -_- :3 ^^ :| >:( 8) :y :n :ok :hi), không phân biệt hoa thường; chỉ đổi khi ký hiệu đứng riêng ngay trước con trỏ (không đụng link, giờ 10:30, "a:)").
- [x] `ChatComposer`: Space / Shift+Enter / Enter (gửi) ⇒ đổi; Ctrl/Cmd+Z ngay sau đó ⇒ trả ký hiệu gốc (gõ tiếp thì không đổi lại). Không đổi cả đoạn lúc gửi (tôn trọng Ctrl+Z).
- [x] `ChatEmojiPicker`: tooltip emoji có "gõ :)", dòng "Gõ nhanh: …" ở chân tab Emoji (rê xem đủ bảng). `ChatPane` H bảng cảm xúc 300 → 330.
- [x] E2E E7 + E4/E5 setTimeout 180s: bộ `chat-thong-bao-emoji` 7/7; chạy lại chat-core/bo-sung/toolbar-zalo/gd2: đạt (lần 1 chat-bo-sung B3 gặp trang 404 khi B mở nhóm, chạy lại 21/21 đạt — chập chờn, chưa rõ nguyên nhân).

## Bổ sung 13/11 — Xem ảnh trong chat (user chọn "Lightbox đầy đủ", cho phép "làm")
- [x] `components/chat/ChatImageViewer.vue`: bọc `vue-easy-lightbox` 0.14.1 (đã có trong package.json, chưa màn nào dùng — tải lười). Nền tối 92% · cuộn phóng to/thu nhỏ · kéo · xoay · ← → lướt mọi ảnh đã tải của hội thoại · thanh trên: người gửi, giờ, "2/3", tên tệp, Tải xuống (fetch blob; S3 chặn CORS ⇒ mở tab), Mở ảnh gốc, Đóng · Esc chặn lan xuống ô soạn. Nút dùng V2BaseIconButton.
- [x] `ChatMessageItem`: bấm ảnh ⇒ `open-image` (Ctrl/Cmd/Shift/chuột giữa ⇒ mở tab như cũ). `ChatPane.openImage` gom ảnh chưa thu hồi theo thứ tự.
- [x] E2E E8; bộ `chat-thong-bao-emoji` 8/8 + chat-core/bo-sung/toolbar-zalo/gd2 29/29.
- Bẫy: khối bọc chỉ chứa phần tử fixed ⇒ Playwright báo "hidden" — đo `.vel-modal`; `.vel-img` dựng sau vòng tải.

## Rà theo nguyên tắc quy mô 1.000–2.000 người + app mobile/desktop (user nhắc 13/11) — CHƯA SỬA, chờ user chọn
1. Push FCM nhóm đông: `PushChatMessage` gửi tuần tự từng người trong 1 job (nhóm 2.000 ⇒ 2.000 lượt gọi FCM nối nhau, job chạy vài phút, chặn queue chung). Hướng: chia lô 500 người/job + gửi gộp (sendMulticast/sendAll theo topic không gộp được ⇒ chia job).
2. `muted_ids` trong gói socket: nhóm 2.000 người mà nhiều người tắt ⇒ mảng lớn phát tới cả 2.000 kênh. Hướng: thay bằng cờ theo người nhận (`notify: false`) — tách 2 lô người nhận (bật / tắt) khi publish.
3. Danh mục sticker khai 2 nơi (BE `ChatStickers` + FE `utils/chat/stickers.js`), ảnh nằm trong `hrm-client/static` ⇒ app mobile/desktop phải chép lại. Hướng: BE là nguồn duy nhất — `GET chat/stickers` trả bộ + URL tuyệt đối; web/app đều đọc API.
4. Cài đặt âm thanh / thông báo trình duyệt lưu localStorage (theo từng trình duyệt) — hợp lý cho thiết bị; nếu cần đồng bộ "tắt toàn bộ thông báo chat" giữa web/app thì cần cài đặt ở BE.
5. Phím tắt emoji + dữ liệu emoji chỉ ở web — app tự dùng bàn phím emoji của máy, desktop có thể dùng lại `utils/chat/*.js` (thuần JS).

## Checkpoint — 13/11/2026 ~16:30 (ĐÃ LÊN gop_db, chờ user deploy)
Vừa hoàn thành: commit + push nhánh `gop_db-chat-thong-bao-emoji` và fast-forward `origin/gop_db` — hrm-api `91b2cb8db..93c82d807`, hrm-client `bb918e470..d178b590c`.
Bước tiếp theo: user chạy deploy TPE (build_tpe.sh + restart tpe-worker / tpe-agent-worker / hrm-tpe-socket) → test push thật tới máy user → đợt sau: 3 điểm quy mô (chia lô push, cờ notify theo người, API sticker).
