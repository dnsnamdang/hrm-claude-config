# Điều tra lỗi gọi thoại/video chat trên PROD (chưa có số Redmine) — @cuong61n

Chức năng gọi thoại/video 1–1 trong chat (LiveKit + CallKit/VoIP push) do dnsnamdang code, lên prod 27/11/2026
(api `420ce8e4f`, `31b105648`; app `b065c6d`, `e032589`). User báo 27/11 tối: huỷ rồi gọi lại thì bên nghe bấm Nghe
không được / bị tắt luôn; có lúc một bên đổ chuông bên kia không thấy. Việc này chỉ điều tra, chưa sửa code.

## Phase 1 — Điều tra trên prod (27/11/2026) — @cuong61n

- [x] 27/11 Đọc luồng BE (`CallService`, `ChatCallController`, `RingCallPush`, `ExpireRingingCall`, `CallSocket`), app
      (`call_controller.dart`, `call_kit_bridge.dart`, `call_push.dart`, `call_android_bridge.dart`, `AppDelegate.swift`),
      web (`store/call.js`, `utils/chat/callSession.js`, `BasicSubsystem.vue`) và plugin `flutter_callkit_incoming 3.1.6`.
- [x] 27/11 Soi prod: bảng `chat_calls` / `chat_call_participants` / `chat_call_devices` / `fcm_tokens`, `laravel.log`
      (dòng `APNs VoIP`), nginx access log (mã HTTP từng request `chat/calls/*`), worker supervisor, `failed_jobs`, `jobs`.
- [x] 27/11 Tìm đúng ca user tả: cuộc 173 (1349 → 13, 18:49:14) huỷ 18:49:28; cuộc 174 gọi lại 18:49:42. BE tạo
      cuộc 201, push VoIP `call.incoming` tới 2 token của 13 (18:49:43/44). **Không có request `accept` nào tới server**;
      điện thoại bên nghe chỉ gọi `GET calls/active` + `GET calls?limit=10` lúc 18:50:32 — đúng 50 s sau khi cuộc tạo
      = hạn chót đổ chuông của app (`ringDeadline = 50s` → `_reconcile`). Cuộc 174 bị job hết giờ chốt `missed` 18:50:28.
      ⇒ BE xử lý đúng; lỗi nằm ở app iOS (lớp CallKit), Nghe không bao giờ sinh request.

### Kết luận theo từng triệu chứng

1. **Bấm Nghe không được / tắt luôn (iOS)** — chưa chốt được nguyên nhân gốc vì không có log máy; từ code có 3 đường
   làm nút Nghe chết mà không gọi API, cần log thiết bị để biết đường nào:
   - `_onCallKitAccept`: uuid đang nằm trong `_ckGone` → `return` im lặng (CallKit đã fulfill nên hiện "đang kết nối"
     rồi đứng); hoặc rơi vào nhánh chờ 10 s (`callKitAcceptWait`) → `_failCallKitAccept(notify: true)` → CallKit tắt
     + toast "không kết nối được" = "bấm nghe thì bị tắt luôn".
   - `CallKitBridge.showIncoming()` không kiểm CallKit có hiện được không: plugin nuốt lỗi `reportNewIncomingCall`
     (`onError: nil`, method channel luôn trả `true`); `activeUuids()` không được gọi ở đâu. Nếu CallKit từ chối (uuid
     vừa dùng lại, còn cuộc chưa dọn xong của cuộc trước — đúng tình huống huỷ rồi gọi lại sau 14 s), Dart vẫn ở
     `incoming` với `callKitShowsIncoming == true` → app ẩn màn cuộc gọi đến của mình, không đổ chuông ⇒ máy im lìm.
   - Plugin dùng 1 cờ toàn cục `isFromPushKit` + `self.data`: push VoIP tới SAU gói socket (thực tế prod 1–2 s) ghi đè
     `self.data`; `endCall` / sự kiện DECLINE sau đó dùng `self.data` thay cho cuộc được yêu cầu kết thúc.
2. **Một bên đổ chuông, bên kia không thấy** — có số liệu:
   - Bên nghe dùng app chưa có chức năng gọi (không đăng ký token VoIP, Android bản cũ không có handler): 868 android
     2.3.7, 1264 ios 2.3.5, 734 android 2.3.5, 649 ios 2.3.5, 100/211/1356 không token app… Hôm nay 64 cuộc
     `cancelled`, phần lớn gọi tới nhóm này. Người gọi không được báo gì (BE `start()` chỉ kiểm `ChatCallAccess`).
   - Cuộc 177 (1063 → 990, 19:01:53): 990 chưa có token VoIP (bản 114) → không có push; 990 mở app bản 118 lúc
     19:01:56, `GET calls/active` trả về cuộc đang `ringing` nhưng app bỏ qua (`_restoreActive` chỉ xử lý `ongoing`;
     web `restoreActive` cũng vậy) → mở app giữa lúc đổ chuông vẫn không thấy gì; người gọi huỷ 19:02:14.
   - Cùng 1 iPhone đổi build (TestFlight → debug) để lại 2 dòng `chat_call_devices` (id 2 production + 127 sandbox) cho
     nhân viên 13; APNs vẫn trả 200 cho token cũ nên không tự dọn.
3. **Không phải lỗi**: web gọi `GET calls/active` ~212 lần/3 phút là tổng của nhiều user Windows, mỗi lần tải trang 1
   lần (`call-layer.client.js` → `restoreActive`). `hangup` 409 kép ở cuộc 179 vô hại (bấm 2 lần).
4. **Rủi ro**: push đổ chuông + job hết giờ 45 s đi chung hàng `chat-push` 1 worker với push tin nhắn; hôm nay trễ
   1–3 s, đông người sẽ trễ hơn (job chạy muộn khi cuộc đã huỷ thì bỏ qua → bên nghe không bao giờ đổ chuông).

### Đề xuất sửa (chưa làm, chờ user chốt)

- App iOS: sau `showIncoming` kiểm `activeUuids()`; không có uuid ⇒ bật màn cuộc gọi đến của app + chuông (không tin
  CallKit mù quáng). `_onCallKitAccept` gặp `_ckGone` ⇒ `_ckEnd` + báo lỗi, không `return` im lặng.
- App + web: `restoreActive` nhận cả `ringing` (mình là callee) ⇒ dựng màn cuộc gọi đến.
- BE `start()`: callee không có token VoIP, không có FCM app ≥ bản hỗ trợ gọi, không online socket ⇒ trả trạng thái
  riêng để người gọi thấy "Người này chưa cài bản app hỗ trợ gọi".
- Tách hàng đợi riêng cho `RingCallPush` / `ExpireRingingCall` (hoặc gửi push ngay trong request).
- Tái hiện có log: cắm iPhone (skill `iphone-local`, xem log Xcode/`idevicesyslog`) chạy đúng kịch bản huỷ → gọi lại.

### Checkpoint — 2026-11-27 19:40
Vừa hoàn thành: điều tra prod + đọc code, ghi kết luận ở trên.
Đang làm dở: không.
Bước tiếp theo: user chốt hướng sửa (app iOS / restoreActive / BE báo không gọi được) và cho số Redmine; tái hiện có
log thiết bị để chốt nguyên nhân mục 1.
Blocked: cần log máy iPhone bên nghe (không lấy được từ server).
