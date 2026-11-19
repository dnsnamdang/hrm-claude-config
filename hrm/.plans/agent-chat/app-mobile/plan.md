# Chat + TPE SMART AGENT trên app mobile — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **CHƯA ĐƯỢC PHÉP CODE.** Plan này chỉ là tài liệu. Trước mỗi giai đoạn phải hỏi user riêng, nêu repo · nhánh · file sẽ đụng
> (CLAUDE.md gốc — "Đụng source code phải được user cho phép RÕ RÀNG"). Không commit / push khi chưa được yêu cầu.

**Goal:** Đưa Chat (nhóm trao đổi + chat 1–1) và TPE SMART AGENT lên app TPE_APP, dùng lại toàn bộ API / socket của web
`origin/gop_db`, theo bộ mockup đã chốt 17/11/2026.

**Architecture:** App chỉ là một client mới của API `v1/assign/chat/*`, `v1/assign/workspaces/*`, `v1/agent/*` và socket
`server_node` (socket.io 2.x) — **không đổi BE** cho phần lõi. Chat là một khu độc lập trong app (`lib/ui/chat/`), mở bằng icon 💬
trên `PrimaryAppBar` ở mọi màn; một `ChatHub` (singleton) giữ kết nối socket + số chưa đọc và phát sự kiện cho các màn.
Màn nhiều trạng thái dùng BLoC; danh sách gọn dùng StatefulWidget + ApiService (đúng copilot-instructions của TPE_APP).

**Tech Stack:** Flutter 3.41.7 (FVM) · flutter_bloc 8.0.1 · dio 4 (`authAppServerClient`) · injectable · firebase_messaging 15 ·
image_picker / file_picker / photo_view / cached_network_image (đã có) · **mới: `socket_io_client` 1.0.2** (dòng 1.x dành cho
server socket.io 2.x — server_node đang `socket.io ^2.3.0`; Task 2 kiểm kết nối thật trước khi làm tiếp).

**Spec:** `HRM/.plans/agent-chat/app-mobile/design.md` (quyết định đã chốt + bảng icon + phong cách) ·
`phan-tich-app-web.md` (bảng App / Web) · mockup `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen`, khu
"CHAT + AGENT (APP)" x 30600 (CH-01…30, G-01…08, M-01…02, V-01…02, AG-01…06; mỗi màn có chú thích nghiệp vụ ngay trên).

## Global Constraints

- Repo `TPE_APP`, nhánh mới `feature/chat-agent-app` tách từ `origin/develop`; chỉ build flavor `tpeDev` / `tpeProd` (chỉ làm cổng TPE trước).
- Flutter / Dart luôn qua `fvm`; chạy từ `TPE_APP/app/`. **Không `dart format` file đang sửa dở** — chỉ format file mới.
- `fvm dart analyze lib/ui/chat lib/ui/agent` không thêm lỗi / cảnh báo so với mức chuẩn (0 lỗi, 0 cảnh báo).
- Mọi nút có icon kèm chữ (`PrimaryButton` / `SecondaryButton` / `DangerButton`, `appButtonIcon()`); Huỷ / Đóng luôn đứng CUỐI.
- Điều hướng bằng `navigator.push(XxxRoute())`; text tiếng Việt viết thẳng trong code; rung chỉ `HapticFeedback.selectionClick()`.
- Sửa widget dùng chung (`custom_view/`, `common_view/`, `base/`) phải hỏi trước — Task 3 (`PrimaryAppBar`) là chỗ duy nhất, đã nêu ở đây.
- Màu: xanh thương hiệu `#225AA6`, navy `#193463`, cam `#E77D00`, nền chat `#EDF2F9`, bong bóng mình dải `#3473CF → #225AA6`;
  header `HeaderBg` dải chéo `#3473CF → #225AA6 → #193463` + 2 quầng sáng + 2 vòng + icon chìm (`forum` / `smart_toy`).
- Icon đối tượng (design.md "Bộ icon dùng chung"): Nhiệm vụ giao `user-check` → làm `user-round`, hạn `alarm-clock`, ưu tiên `flag`
  (Bình thường `#64748B` · Cao `#F97316` · Khẩn cấp `#DC2626`); Vấn đề báo `user-plus` → phụ trách `user-round`; Meeting `calendar` · `map-pin`/`video` · chủ trì `user-round`.
- Trạng thái / màu / nhãn do BE trả (`status_text`, `status_color`, `next_action_label`, `allowed_next_statuses`) — app không tự map.
- Không hiện mã nhiệm vụ / vấn đề trên thẻ; không hiện dòng chi phí token của Agent.
- Giới hạn lấy từ BE, app chỉ báo: tin ≤ 5,000 ký tự (đếm từ 4,500) · ≤ 10 tệp / tin, 25 MB / tệp · @ ≤ 200 người · ghim ≤ 20 ·
  chia sẻ ≤ 20 hội thoại · sửa / thu hồi trong 24 giờ · Agent câu hỏi ≤ 1,000 ký tự, 20 câu / phút, chờ tối đa 150 giây.
- Chỉ web (app KHÔNG làm): thống kê / hạn mức / model Agent, gắn Dự án KH, đóng / mở lại nhóm, thêm theo phòng ban / cả công ty,
  thao tác hàng loạt, YC hỗ trợ, gọi thoại / video.
- Kiểm xong mỗi task giao diện = bấm thử đúng luồng trên simulator `tpeLocal`/`tpeDev` (skill `app-simulator-test`), không chỉ test xanh.

## Review Focus

1. **Mất socket / ngủ máy rồi mở lại** — tin đến trong lúc mất kết nối không được thiếu: khi `connect` lại phải gọi
   `messages?after=<id tin cuối>` cho hội thoại đang mở và nạp lại danh sách (test ở Task 2 + Task 7).
2. **Bấm push khi app đã tắt hẳn** — mở app phải vào thẳng hội thoại `data.id`, nút ‹ về danh sách chat, không kẹt màn trắng (Task 4).
3. **Tin gửi đi bị nhân đôi** — tin tạm (optimistic) và gói `message.created` của chính mình phải gộp làm một theo `id` mà `POST messages`
   trả về, kể cả khi gói socket tới TRƯỚC response (Task 7).
4. **Bị mời ra / nhóm bị đóng khi đang xem** — API trả 403 / 423 thì đổi sang chế độ chỉ đọc hoặc rời màn kèm câu báo, không crash (Task 9, 11).
5. **Đổi công ty đang làm giữa chừng** — danh bạ / Agent theo công ty mới; lượt Agent đang chạy bị huỷ phải hiện câu BE trả
   ("Bạn vừa đổi công ty…"), không quay vô hạn (Task 15).

---

## Giai đoạn A — Nền (socket, API, lối vào, push)

### Task 1: Gói API chat + model

**Files:**
- Create: `TPE_APP/app/lib/data/lib/src/repository/source/remote/api/api_services/app_server/chat_api_service.dart`
- Create: `TPE_APP/app/lib/ui/chat/model/chat_models.dart`
- Test: `TPE_APP/app/test/ui/chat/chat_models_test.dart`

**Interfaces:**
- Produces: `@LazySingleton() class ChatApiService` (khuôn `WorkApiService`: `_raw`, `getMap`, `post`, `put`, `patch`) với
  `conversations({String filter='all', String? q, String? before})`, `unreadCount()`, `directory({String? q, int? companyId, int page})`,
  `profile(int employeeId)`, `conversation(int id)`, `messages(int id, {int? before, int? after, int? around})`, `send(int id, ChatDraft d)`,
  `sendDirect(int employeeId, ChatDraft d)`, `markRead(int id, int messageId)`, `patchMe(int id, Map patch)`, `pins(int id)`,
  `search(int id, String q)`, `resources(int id, String kind, {String? cursor})`, `typing(int id)`, `forward(int messageId, List<int> ids, String? note)`,
  `edit(int messageId, String body)`, `recall(int messageId)`, `hide(int messageId)`, `react(int messageId, String emoji)`,
  `pin(int messageId)`, `unpin(int messageId)`, `upload(File f)` → `String url`.
- Produces: model `ChatConversation`, `ChatMessage`, `ChatMember`, `ChatDraft {String body; int? replyToId; List<int> mentionIds; bool mentionAll; List<String> files; ({String type,int id})? card; String? sticker}` (BE KHÔNG có client_key — đã kiểm `origin/gop_db`)
  — mỗi model có `fromJson(Map)`; tên trường đúng JSON API web (đọc `components/chat/*` trên `origin/gop_db` khi viết).

- [ ] **Step 1: Viết test `chat_models_test.dart`**: parse 1 JSON hội thoại nhóm (có `company_code`, `unread_count`, `muted`, `pinned`,
  `draft` bỏ qua), 1 JSON 1–1, 1 tin `system`, 1 tin `card` (type task), 1 tin đã thu hồi → assert từng trường; `ChatDraft.toJson()` có
  `mention_all`, `files`, `card{type,id}` đúng khoá API.
- [ ] **Step 2:** `cd TPE_APP/app && fvm flutter test test/ui/chat/chat_models_test.dart` → FAIL (chưa có model).
- [ ] **Step 3:** Viết model + `ChatApiService` (prefix `assign/chat/`, upload dùng `POST files/upload` multipart như web).
- [ ] **Step 4:** Chạy lại test → PASS; `fvm dart analyze lib/ui/chat lib/data` sạch.
- [ ] **Step 5:** Commit `feat(chat): api service + model`.

### Task 2: `ChatHub` — kết nối socket + số chưa đọc

**Files:**
- Modify: `TPE_APP/app/pubspec.yaml` (thêm `socket_io_client: 1.0.2`)
- Modify: `TPE_APP/app/lib/shared/lib/src/build_config/build_config.dart` — thêm getter `String? get socketUrl` cạnh `apiDomain` (URL server app nằm ở đây, KHÔNG ở `env/*.env`): `tpeProd => 'https://hrm.eteksofts.com'` (đã thử bắt tay socket.io EIO=3 → 200, 17/11) · `tpeLocal => 'http://127.0.0.1:8895'` (socket worktree chat) · `tpeDev => null` (dev-hrm.eteksofts.com/socket.io trả 404, VPS dev không chạy server_node cho bộ tpe — 17/11) · flavor khác `null`
- Create: `TPE_APP/app/lib/ui/chat/hub/chat_hub.dart`, `chat_event.dart`
- Test: `TPE_APP/app/test/ui/chat/chat_event_test.dart`

**Interfaces:**
- Consumes: `ChatApiService.unreadCount()`.
- Produces: `@LazySingleton() class ChatHub` — `connect(String jwt)`, `disconnect()`, `Stream<ChatEvent> events`,
  `ValueListenable<int> unread`, `Stream<bool> connected`, `pingPresence()` (timer 50 giây emit `presence_ping`),
  `sendTyping(int conversationId)` (gọi API, chặn lặp < 3 giây).
- Produces: `sealed class ChatEvent` với `MessageCreated`, `MessageUpdated`, `MessagePinned`, `MessageUnpinned`, `ConversationRead`,
  `ConversationUpdated`, `Typing`, `TaskUpdated`, `Presence`, `AgentStep/AgentDelta/AgentDone` — `ChatEvent.parse(String socketEvent, dynamic payload)`.
- Hợp đồng socket (server_node): kết nối `io(SOCKET_URL, query: {token})`; sự kiện `chat` (payload `{type, ...}` với type
  `message.created|message.updated|message.pinned|message.unpinned|conversation.read|conversation.updated|typing|task.updated`),
  `presence` (`{employee_id, online, last_seen_ms}`), `agent` (`{kind:'agent', turn_id, type:'step'|'delta'|'done', data}`).

- [ ] **Step 1: Test `chat_event_test.dart`**: `ChatEvent.parse('chat', {'type':'message.created', ...})` → `MessageCreated` có
  `conversationId`; `parse('presence', {...})` → `Presence(online:false, lastSeen)`; `parse('agent', {...,'type':'delta'})` → `AgentDelta`;
  type lạ → `null` (không ném lỗi).
- [ ] **Step 2:** Chạy test → FAIL.
- [ ] **Step 1b: Test chế độ dự phòng**: `socketUrl == null` hoặc kết nối lỗi ⇒ `ChatHub` chuyển sang hỏi lại API (`unread-count` 30 giây; hội thoại đang mở `messages?after=` 5 giây) và `connected` phát `false`; có socket lại ⇒ dừng hỏi lại.
- [ ] **Step 3:** Viết `ChatEvent.parse` + `ChatHub` (tự kết nối lại; khi `connect` lại phát `Reconnected` để màn đang mở nạp bù;
  `unread` = `unreadCount()` lúc khởi động + cộng / trừ theo `MessageCreated` / `ConversationRead` của hội thoại không tắt thông báo).
- [ ] **Step 4:** Test PASS; `fvm flutter pub get` sạch; analyze sạch.
- [ ] **Step 5:** Commit `feat(chat): socket hub`.

### Task 3: Icon 💬 trên `PrimaryAppBar` (widget dùng chung — đã nêu, vẫn hỏi lại khi bắt tay)

**Files:**
- Create: `TPE_APP/app/lib/custom_view/chat_shortcut_button.dart`
- Modify: `TPE_APP/app/lib/custom_view/primary_app_bar.dart` (cạnh `NotificationBellButton`, cùng điều kiện `showNotificationBell`)
- Test: `TPE_APP/app/test/custom_view/chat_shortcut_button_test.dart`

**Interfaces:**
- Consumes: `ChatHub.unread`.
- Produces: `ChatShortcutButton` — bấm `navigator.push(ChatListRoute())`; badge đỏ `99+`; ẩn khi user không có quyền dùng Tin nhắn
  (key Cài đặt phân hệ "Tin nhắn" bị ẩn — đọc giống web `effectiveMenuHiddenKeys`).

- [ ] **Step 1: Widget test**: unread 0 → không badge; 12 → "12"; 150 → "99+"; có nút trong `PrimaryAppBar` khi `showNotificationBell: true`.
- [ ] **Step 2:** Chạy → FAIL. **Step 3:** Viết widget + gắn vào AppBar. **Step 4:** PASS + simulator: mở 3 phân hệ thấy 💬 cạnh chuông (CH-01).
- [ ] **Step 5:** Commit `feat(chat): app bar shortcut`.

### Task 4: Push `chat_message` mở thẳng hội thoại

**Files:**
- Modify: `TPE_APP/app/lib/ui/notification/notification_router.dart` (thêm `case 'chat_message'`)
- Create: `TPE_APP/app/lib/ui/chat/chat_routes.dart` (route `ChatListRoute`, `ChatRoomRoute(int conversationId, {int? messageId})`)
- Test: `TPE_APP/app/test/ui/notification/notification_router_chat_test.dart`

**Interfaces:**
- Consumes: payload push `data = {type:'chat_message', id:'<conversation_id>', message_id:'<id>'}` (đã có ở `PushChatMessage`, không đổi BE).
- Produces: `openNotificationTarget` với `chat_message` ⇒ push `ChatListRoute` rồi `ChatRoomRoute(id)` (để ‹ về danh sách).

- [ ] **Step 1: Test**: notification type `chat_message`, id `"42"` ⇒ navigator mock nhận đúng 2 route theo thứ tự; id rỗng ⇒ chỉ `ChatListRoute`.
- [ ] **Step 2–4:** FAIL → viết → PASS; simulator: tắt hẳn app, gửi tin từ web bằng tài khoản khác, đợi 20 giây, bấm push ⇒ vào đúng hội thoại (Review Focus 2).
- [ ] **Step 5:** Commit `feat(chat): open conversation from push`.

## Giai đoạn B — Danh sách, danh bạ, tạo / sửa nhóm

### Task 5: Danh sách hội thoại (CH-02, CH-03, CH-30)

**Files:** Create `lib/ui/chat/list/chat_list_page.dart`, `chat_list_bloc.dart`, `widget/conversation_row.dart`, `widget/chat_header_bg.dart`
(header dùng chung cho MỌI màn chat — tham số `watermark: forum|smart_toy`), `widget/conversation_actions_sheet.dart`.
Test `test/ui/chat/chat_list_bloc_test.dart`.

**Interfaces:**
- Produces: `ChatHeaderBg({required Widget child, IconData watermark, bool roundedBottom=false})` — dùng lại ở mọi task sau.
- Produces: `ChatListBloc` sự kiện `Load(filter)`, `LoadMore`, `Search(q)`, `Apply(ChatEvent)`; trạng thái giữ `pinned`, `recent`, `cursor`.

- [ ] **Step 1: Bloc test**: `MessageCreated` của hội thoại B đưa B lên đầu khối Gần đây + tăng `unread`; hội thoại đã ghim giữ ở khối Đã ghim;
  `ConversationRead` đưa `unread` về 0; filter `unread` gọi API `filter=unread`.
- [ ] **Step 2–4:** FAIL → viết bloc + màn đúng CH-02 (header 52 = ‹ · ô tìm · ✎; chip 36 ẩn khi cuộn xuống; dòng 72; dòng Agent ghim trên cùng khi
  `canUseAgent`; nút ⋮ hiện sẵn + nhấn giữ → sheet CH-03; số chưa đọc cam `#E77D00`, xám khi tắt TB; dải "Đang kết nối lại…" theo `ChatHub.connected` — CH-30)
  → PASS + simulator.
- [ ] **Step 5:** Commit.

### Task 6: Danh bạ, Tạo nhóm, Sửa nhóm (CH-04, CH-05, CH-05b, CH-05c)

**Files:** Create `lib/ui/chat/directory/directory_page.dart`, `lib/ui/chat/workspace/workspace_form_page.dart` (1 form 2 chế độ tạo / sửa).
Test `test/ui/chat/workspace_form_test.dart`.

**Interfaces:** `WorkspaceFormPage({int? workspaceId})`; gọi `POST workspaces` `{name, description, member_ids, enabled_tabs ⊂ [tasks,meetings,issues]}` /
`PUT workspaces/{id}` `{name, description, enabled_tabs}`.

- [ ] **Step 1: Widget test**: bấm Tạo khi Tên trống ⇒ viền đỏ + "Bắt buộc phải nhập", không gọi API; bật Nhiệm vụ + Meeting ⇒ body có
  `enabled_tabs:['tasks','meetings']`; 422 từ BE ⇒ lỗi hiện dưới đúng ô.
- [ ] **Step 2–4:** FAIL → viết (danh bạ mọi công ty, lọc công ty, gom phòng ban; chạm người ⇒ `ChatRoomRoute` qua `direct/{emp}`) → PASS + simulator.
- [ ] **Step 5:** Commit.

## Giai đoạn C — Màn chat

### Task 7: Khung chat + gửi / nhận (CH-06, CH-07, CH-17)

**Files:** Create `lib/ui/chat/room/chat_room_page.dart`, `chat_room_bloc.dart`, `widget/message_bubble.dart`, `widget/system_pill.dart`,
`widget/task_card.dart`, `widget/composer.dart`, `widget/pin_bar.dart`. Test `test/ui/chat/chat_room_bloc_test.dart`.

**Interfaces:**
- Produces: `ChatRoomBloc(conversationId)` — `Open`, `LoadOlder`, `Send(ChatDraft)`, `Apply(ChatEvent)`, `Reconnected`; state có
  `messages`, `unreadMarkerId` (chốt lúc mở), `readOnlyReason` (`role_view|closed|resigned|null`).
- Produces: `TaskCard(Map task)` — dùng lại ở Task 12, 13.

- [ ] **Step 1: Bloc test**:
  - `Send` thêm tin tạm (id âm); POST trả `id=900` ⇒ tin tạm thành 900; `MessageCreated(id=900)` tới SAU ⇒ không thêm dòng; tới TRƯỚC response ⇒
    khi response về thì bỏ tin tạm, chỉ còn 1 dòng 900 (Review Focus 3).
  - `Reconnected` gọi `messages(after: lastId)` và nối đúng thứ tự (Review Focus 1).
  - `MessageUpdated` recall ⇒ bubble "Tin nhắn đã thu hồi"; `TaskUpdated` cập nhật thẻ cùng id.
  - API 403 khi mở ⇒ state `left` (Review Focus 4); nhóm `status==2` ⇒ `readOnlyReason=closed`.
- [ ] **Step 2–4:** FAIL → viết đúng CH-07 (header ‹ · avatar · tên/số TV · 📋 n · ⓘ, không dải tab; dải ghim 32; mốc "Tin chưa đọc"; tin hệ
  thống viên xám; bong bóng mình dải xanh chữ trắng; "Đã xem" chỉ 1–1; ô soạn 1 hàng; dải trả lời 40; bộ đếm từ 4,500 ký tự; chỉ đọc CH-17)
  → PASS + simulator 2 máy ảo nhắn qua lại.
- [ ] **Step 5:** Commit.

### Task 8: Thao tác trên tin + soạn nâng cao (CH-08…11, CH-20, CH-23, CH-24, CH-24b)

**Files:** Create `lib/ui/chat/room/widget/message_actions_sheet.dart`, `attach_sheet.dart`, `mention_suggest.dart`, `task_suggest.dart`,
`emoji_sticker_panel.dart`, `image_send_preview_page.dart`, `forward_sheet.dart`. Test `test/ui/chat/message_actions_test.dart`.

**Interfaces:** `MessageActions.of(ChatMessage m, ChatMember me, ChatConversation c) -> List<MessageAction>` (hàm thuần, quyết định mục nào hiện).

- [ ] **Step 1: Test hàm thuần `MessageActions.of`**: tin mình < 24 giờ ⇒ có Sửa + Thu hồi; > 24 giờ ⇒ không; tin chia sẻ ⇒ không Sửa;
  vai trò Xem ⇒ chỉ Sao chép, Chia sẻ, Nhắc việc, Xoá phía tôi; tin thẻ nhiệm vụ ⇒ không Chia sẻ; nhóm chưa bật Nhiệm vụ ⇒ không Tạo nhiệm vụ.
- [ ] **Step 2–4:** FAIL → viết (sheet lưới 4 cột + hàng biểu cảm; @ có @all, ≤ 200; # gợi ý `tasks/suggest` hàng 1 giao → làm · hàng 2 tên ·
  hàng 3 hạn · ưu tiên · trạng thái; ảnh nén + Cắt / Xoay, ≤ 10; chia sẻ ≤ 20; sửa = dải vàng; thu hồi = hộp xác nhận) → PASS + simulator.
- [ ] **Step 5:** Commit.

### Task 9: Tìm tin, tin ghim, xem ảnh, ảnh / tệp / link (CH-18, CH-19, CH-21, CH-22)

**Files:** Create `lib/ui/chat/room/search_page.dart`, `pins_page.dart`, `image_viewer_page.dart`, `resources_page.dart`. Test `test/ui/chat/search_page_test.dart`.

- [ ] **Step 1: Widget test**: kết quả tô nền vàng đúng từ khoá (không phân biệt hoa thường, có dấu); bấm kết quả ⇒ pop với `messageId`;
  `ChatRoomBloc` nhận `JumpTo(messageId)` gọi `messages(around:)`.
- [ ] **Step 2–4:** FAIL → viết → PASS + simulator. **Step 5:** Commit.

## Giai đoạn D — Nhóm, thành viên, hồ sơ

### Task 10: Thông tin nhóm / 1–1, hồ sơ (CH-15, CH-16, CH-25)

**Files:** Create `lib/ui/chat/info/workspace_info_page.dart`, `direct_info_page.dart`, `profile_sheet.dart`.

- [ ] **Step 1: Widget test**: Quản lý thấy nút Sửa + "+ Thêm" + ⋮ ở mọi dòng trừ mình; Thành viên không thấy Sửa / Thêm; nhóm Dự án KH không có Rời nhóm.
- [ ] **Step 2–4:** FAIL → viết (khối Top nối `ChatHeaderBg(roundedBottom:true)`; Gọi = `tel:`; Email = `mailto:`) → PASS + simulator. **Step 5:** Commit.

### Task 11: Quản lý thành viên + rời nhóm (CH-15b, CH-26, CH-27, CH-27b)

**Files:** Create `lib/ui/chat/info/member_actions_sheet.dart`, `add_members_page.dart`. Test `test/ui/chat/member_actions_test.dart`.

**Interfaces:** gọi `PUT workspaces/{id}/members/{mid}` (đổi vai trò), `DELETE …/members/{mid}`, `POST …/members`, `POST workspaces/{id}/leave`.

- [ ] **Step 1: Test**: 422 "còn việc dở" ⇒ khối đỏ trong sheet + nút "Xem việc của người này" mở `GroupWorkRoute(tab: tasks, assigneeId: mid)`;
  Quản lý cuối ⇒ câu "Nhóm cần ít nhất 1 Quản lý"; rời nhóm thành công ⇒ pop về danh sách và hội thoại biến mất.
- [ ] **Step 2–4:** FAIL → viết → PASS + simulator. **Step 5:** Commit.

## Giai đoạn E — Việc của nhóm (3 tab)

### Task 12: Khung "Việc của nhóm" + tab Nhiệm vụ (CH-12, G-01…08, CH-28)

**Files:** Create `lib/ui/chat/work/group_work_page.dart`, `group_tasks_view.dart`, `group_tasks_bloc.dart`, `task_view_prefs.dart`,
`sheets/{quick_sheet,view_sheet,advanced_filter_sheet,status_sheet}.dart`. Test `test/ui/chat/group_tasks_bloc_test.dart`.

**Interfaces:**
- `GroupWorkRoute(int workspaceId, {String tab='tasks', int? assigneeId})`; thanh chuyển chỉ hiện tab có trong `enabled_tabs`.
- API `GET workspaces/{id}/tasks` với `quick ∈ {all,mine,overdue,waiting_my_approval}`, `group_by ∈ {status,assignee,due}`, `q`,
  `assignee_ids[]`, `creator_ids[]`, `statuses[]`, `priorities[]`, `due_from`, `due_to`, `sort_by`, `sort_dir`, `per_group` (≤ 100); đọc `groups`, `quick_counts`, `items`.
- `TaskViewPrefs` lưu Cách xem (group_by, sort) **trên máy** (`SharedPreferences`, khoá theo workspace) — giống web đang lưu localStorage.

- [ ] **Step 1: Bloc test**: đổi Lọc nhanh gửi đúng `quick`; `assigneeId` từ route ⇒ `assignee_ids=[id]` + dải lọc; group_by `due` giữ thứ tự nhóm BE trả
  (Quá hạn · 7 ngày tới · Sau đó · Không có hạn · Chờ duyệt · Đã xong); nhóm `done` thu gọn mặc định; `TaskUpdated` nạp lại (gom 800 ms như web GĐ27).
- [ ] **Step 2–4:** FAIL → viết. Thẻ: giao → làm · hạn · ưu tiên · tiến độ; hàng nút hiện sẵn: `next_action_label` (gọi đúng hành động màn chi tiết
  nhiệm vụ có sẵn) hoặc dòng khoá, ⇄ (sheet chỉ `allowed_next_statuses`), 💬 (màn bình luận có sẵn), ⋯. Bấm thẻ ⇒ chi tiết nhiệm vụ đã có
  (`work_task_detail_page`). "+ Giao việc" và "Tạo nhiệm vụ" từ tin (CH-28) dùng LẠI `work_task_form_page` + tham số điền sẵn (workspace, tên, người làm, khối "Tạo từ tin nhắn")
  — thêm tham số mới, không đổi hành vi cũ → PASS + simulator.
- [ ] **Step 5:** Commit.

### Task 13: Tab Meeting (CH-13, M-01, M-02)

**Files:** Create `lib/ui/chat/work/group_meetings_view.dart`. Test `test/ui/chat/group_meetings_view_test.dart`.

- [ ] **Step 1: Widget test**: chip `upcoming|done|cancelled|all` gửi `bucket`; meeting hôm nay có nhãn "Hôm nay"; `place` rỗng + offline ⇒
  "Chưa chọn phòng" cam; `result_pending` ⇒ "Chưa cập nhật kết quả"; `has_minutes` ⇒ "Có biên bản".
- [ ] **Step 2–4:** FAIL → viết (bấm ⇒ Hub meeting có sẵn; "+ Tạo meeting" ⇒ form meeting có sẵn + workspace) → PASS + simulator. **Step 5:** Commit.

### Task 14: Tab Vấn đề (CH-14, V-01, V-02) — web tab Vấn đề ĐÃ merge gop_db (18/11, origin 5eba99ce1) ⇒ hết chờ; nhóm TKT không có tab Vấn đề, nhóm GP có

**Files:** Create `lib/ui/chat/work/group_issues_view.dart`.

- [ ] **Step 0:** Kiểm `origin/gop_db` đã có API vấn đề theo nhóm chưa (Vấn đề v2 Phase 3). Chưa có ⇒ dừng task này, tab Vấn đề không hiện (BE chưa trả `issues` trong `enabled_tabs` có dữ liệu), báo user.
- [ ] **Step 1–5:** như Task 13: lọc nhanh `Tất cả · Tôi phụ trách xử lý · Tôi phát hiện · Tôi theo dõi · Tôi duyệt đóng · Quá hạn`; gom trạng thái;
  nút Nhận xử lý / Báo đã xử lý / Xác nhận đóng dùng lại hành động màn chi tiết vấn đề có sẵn.

## Giai đoạn F — TPE SMART AGENT

### Task 15: Agent (AG-01…06)

**Files:** Create `lib/ui/agent/agent_page.dart`, `agent_bloc.dart`, `agent_api_service.dart`, `widget/{result_block,pick_card,deny_card,steps_chip,quota_sheet,history_sheet}.dart`.
Test `test/ui/agent/agent_bloc_test.dart`.

**Interfaces:** API `GET agent/conversations`, `POST agent/conversations`, `GET agent/conversations/{id}/turns`, `POST agent/conversations/{id}/ask {question, pick_*_id?}`,
`GET agent/me/panel`; nhận kết quả bằng `ChatHub.events` (`AgentStep/Delta/Done`) **và** hỏi lại `turns` mỗi 1 giây, dừng ở 150 giây.
Điều kiện hiện: quyền `assign.tpe_agent.use` + key `assign::TPE SMART AGENT` không ẩn.

- [ ] **Step 1: Bloc test**: hỏi khi panel báo hết hạn mức ⇒ không gọi API, hiện thẻ xám; 429 ⇒ dải "Bạn hỏi hơi nhanh…"; quá 150 giây ⇒ thẻ "Chưa nhận được kết quả"
  + Hỏi lại; `kind=quota` ⇒ thẻ xám; turn huỷ do đổi công ty ⇒ hiện câu BE trả, dừng hỏi lại (Review Focus 5); thẻ chọn chỉ bấm được ở lượt cuối.
- [ ] **Step 2–4:** FAIL → viết. 12 loại khối kết quả dạng thẻ dọc (`timesheet` 3 ô / hàng); định dạng chữ chỉ `- `, `**đậm**`, `==nổi bật==`;
  thẻ mở Nhiệm vụ / Vấn đề / Meeting / Phiếu / Nhắc việc ⇒ màn có sẵn của app, KH / TKT / Giải pháp / đơn ⇒ "Xem trên web"; không hiện chi phí token → PASS + simulator với `AGENT_FAKE` (hỏi user trước khi đổi :8070).
- [ ] **Step 5:** Commit.

## Giai đoạn G — Thông báo trong app & hoàn thiện

### Task 16: Banner tin mới trong app (CH-29b)

**Files:** Create `lib/ui/chat/hub/chat_banner_overlay.dart`. Test `test/ui/chat/chat_banner_rules_test.dart`.

- [ ] **Step 1: Test hàm thuần `shouldBanner(MessageCreated e, {int? openConversationId, bool muted, bool mentioned})`**: tin mình / tin hệ thống /
  đang mở đúng hội thoại / tắt TB không bị @ ⇒ false; bị @ dù tắt TB ⇒ true.
- [ ] **Step 2–4:** FAIL → viết (1 banner, tự ẩn 4 giây, bấm ⇒ `ChatRoomRoute`) → PASS + simulator. **Step 5:** Commit.

### Task 17: Kiểm toàn luồng + review

- [ ] `fvm flutter test test/ui/chat test/ui/agent test/custom_view` → toàn bộ PASS (đọc dòng tổng kết).
- [ ] Simulator `tpeDev`, 2 máy ảo + web: nhắn 1–1, nhóm, @, #, ảnh, sửa / thu hồi, ghim, chia sẻ, mất mạng 1 phút rồi bật lại, push khi app tắt,
  Việc của nhóm 3 tab, Agent hỏi 3 câu (có thẻ chọn, thẻ thiếu quyền). Đối chiếu từng màn với mockup.
- [ ] Ghi checkpoint vào cuối plan này + `HRM/.plans/STATUS.md` (mục AGENT + CHAT).

## Ngoài plan app (việc riêng, hỏi user)

- **Web** `hrm-client` `components/chat/workspace/CreateWorkspaceModal.vue` chỉ có checkbox Nhiệm vụ (`enabled_tabs: tab_tasks ? ['tasks'] : []`) ⇒ thêm Meeting
  (+ Vấn đề khi xong v2) cho khớp app. BE đã nhận đủ.
- Đồng bộ bản nháp + "Cách xem" web ↔ app qua BE: hiện cả 2 bên lưu trên máy — để đợt sau nếu user cần.

### Checkpoint — 17/11/2026
Vừa hoàn thành: viết plan (chưa code).
Đang làm dở: —
User 17/11 chọn thực thi SUBAGENT-DRIVEN (mỗi task 1 agent con + reviewer). Bước tiếp theo: hỏi phép code Giai đoạn A (repo TPE_APP, nhánh `feature/chat-agent-app` từ `origin/develop`, thêm gói `socket_io_client`, thêm `SOCKET_URL` vào env TPE, sửa `primary_app_bar.dart` + `notification_router.dart`).
Blocked: socket dev chưa chạy (dev-hrm.eteksofts.com/socket.io 404) — app tpeDev chạy chế độ hỏi lại; muốn realtime trên dev phải bật server_node + proxy nginx cho bộ tpe trên VPS dev (việc server, hỏi user). Tab Vấn đề chờ web Vấn đề v2 Phase 3.

### Checkpoint — 17/11/2026 tối (Giai đoạn A XONG, CHƯA commit)
Vừa hoàn thành: Task 1–4 (subagent-driven, mỗi task có soát riêng + soát tổng giai đoạn + 1 đợt sửa). Worktree `websites/wt-tpe-app-chat`, nhánh `feature/chat-agent-app` (từ origin/develop 4ee0561, đã bỏ upstream), KHÔNG commit (theo user). Sổ theo dõi: `wt-tpe-app-chat/.superpowers/sdd/plan/progress.md`.
Đã kiểm máy ảo iPhone 18 Pro bản tpeLocal (API :8080, socket :8895): socket kết nối, 💬 đứng trước chuông, bấm mở màn Tin nhắn (tạm), tin 1–1 từ NV 25 → badge 1 tức thời, đánh dấu đọc → mất badge. Test 39/39, analyze sạch (1 info có sẵn).
Lưu ý chạy: phải `--dart-define-from-file=../env/tpeLocal.env --dart-define=APP_API_BASE_URL=http://127.0.0.1:8080/api/` (thiếu FLAVOR ⇒ app tự nhận tpeDev, gọi dev-hrm).
Đổi so với plan: gói chat dùng khoá `event` (không phải `type`); route tạm `ChatListPage`/`ChatRoomPage` (@RoutePage) thay `chat_routes.dart`; upload KHÔNG gửi `temporary`; `socketUrl` ở build_config.dart.
Dữ liệu thử để lại DB local db_gop_6_11: tin 31845 (hội thoại 99, NV 25 → NV 13).
Bước tiếp theo: hỏi phép code Giai đoạn B (Task 5–6). Việc phải mang theo: Task 7 thêm hook mở lại app (onResume: nạp lại số chưa đọc + Reconnected), dừng presence_ping khi app nền, dựng lại socket khi kẹt dự phòng; Task 8: gửi tệp kèm name/type/size + test ChatApiService.
Blocked: socket dev chưa bật (dev-hrm 404); gating "Tin nhắn" theo Cài đặt phân hệ chưa có trên app.

### Checkpoint — 17/11/2026 khuya (Giai đoạn B XONG, CHƯA commit)
Vừa hoàn thành: Task 5 (danh sách hội thoại CH-02/03/30) + Task 6 (danh bạ, tạo / sửa nhóm CH-04/05/05b/05c), soát từng task + soát tổng GĐ B + 1 đợt sửa nhỏ. 85 test xanh, analyze sạch.
Kiểm máy ảo tpeLocal: danh sách dữ liệu thật (mã công ty, giờ căn phải, chip ẩn khi vuốt); danh bạ gom phòng ban; form tạo nhóm đúng mockup, báo lỗi thiếu Tên; tạo nhóm → 1 request, mở thẳng phòng, quay lại về danh sách.
Lỗi đã bắt và sửa: tìm kiếm sau khi cuộn lẫn dòng cũ; chip không ẩn lần vuốt đầu; tạo nhóm thành công vẫn hiện hộp "chưa lưu" (bấm Lưu sẽ tạo trùng nhóm).
Quyết định R8–R20 ở sổ SDD. Dữ liệu thử DB local: nhóm "[Test app] Nhom tao tu app", "[Test app] Nhom thu 2".
Bước tiếp theo: hỏi phép Giai đoạn C (Task 7–9: màn chat). Mang theo: onResume hook + dừng presence_ping khi app nền + dựng lại socket khi kẹt dự phòng; ChatHub theo dõi phòng đang mở (không cộng chưa đọc); gửi tệp kèm name/type/size + test ChatApiService.

### Checkpoint — 17/11/2026 (Giai đoạn C XONG, CHƯA commit)
Vừa hoàn thành: Task 7 (khung chat, gửi/nhận, realtime, chống mất tin), Task 8 (menu giữ tin, sửa/thu hồi/chia sẻ/cảm xúc, @ #, emoji/sticker, gửi ảnh/tệp, Nhắc việc từ tin), Task 9 (tìm tin, tin ghim, xem ảnh, ảnh/tệp/link, link bấm được). App 207/207 test, analyze 0. Đã kiểm máy ảo.
API bổ sung (hrm-api, worktree `wt-chat-app-api`, nhánh `gop_db-chat-danh-ba-chuc-vu`, CHƯA commit): danh bạ `work_position_name`; thẻ nhiệm vụ `creator` + `priority*`; `TaskChatSync` phát khi đổi ưu tiên; `tasks/suggest` thêm người giao/làm, hạn, ưu tiên. PHPUnit Workspace 269 OK.
Đang làm dở: —
Bước tiếp theo: Giai đoạn D (Task 10 Thông tin nhóm/1–1/hồ sơ — thay sheet ⓘ tạm; Task 11 Quản lý thành viên) — chờ user cho phép. Task 12 kiểm thẻ nhiệm vụ + gợi ý # trên máy ảo.
Blocked: —

### Checkpoint — 18/11/2026 (Giai đoạn D XONG, CHƯA commit)
- Task 10 (Thông tin nhóm / 1–1 / hồ sơ) + Task 11 (thành viên: ⋮ đổi vai trò / mời ra, thêm thành viên, rời nhóm) xong; 238 test; đã kiểm máy ảo (tpeLocal, API :8080).
- Thông tin nhóm thay bảng ⓘ tạm; Sửa nhóm dùng lại form tạo nhóm; nhóm TKT không có tab Vấn đề, nhóm GP có (luật gop_db mới).
- BE không phân trang thành viên hội thoại ⇒ app chia trang phía máy. "Xem việc của người này" đang là toast chờ Task 12.
- Web tab Vấn đề đã merge gop_db (18/11) ⇒ Task 14 hết chờ; nhánh API app `gop_db-chat-danh-ba-chuc-vu` cần kéo gop_db mới trước Task 14.
- Dữ liệu thử: nhóm "[Test app] Nhom tao tu app" đổi tên thành "… (sua)".

### Checkpoint — 18/11/2026 (Task 12 XONG, CHƯA commit)
- Việc của nhóm + tab Nhiệm vụ, tạo nhiệm vụ từ tin (dùng lại form Công việc), nối "Xem việc của người này"; 285 test; kiểm máy ảo + thẻ/# qua API nhánh app (:8081).
- User chốt 18/11: Cách xem lưu trên máy như web; bảng trạng thái đích + dòng khoá giữ phía app như web — việc sau: BE trả `next_action_to` + `lock_reason`, sửa web + app cùng lúc.
- Ghi nhận: báo kết quả 100% nhưng tasks.progress_pct vẫn 0 (BE); nhãn "Báo kết quả" trên thẻ bị cắt (Task 17).
- Dữ liệu thử: nhiệm vụ 42170 trong nhóm "[Test app] Nhom tao tu app (sua)".

### Checkpoint — 18/11/2026 (Task 13 XONG, CHƯA commit)
- Tab Meeting (Sắp họp / Đã họp / Đã huỷ / Tất cả, Hôm nay, Chưa chọn phòng, mã + nháp, số trên tab), tạo meeting dùng lại form có sẵn + workspace_id, bấm mở Chi tiết meeting; chuyển tab giữ bộ lọc Nhiệm vụ; 407 test; kiểm máy ảo.
- Dữ liệu thử: nhóm 12977 bật tab Meeting; meeting nháp TPE.MET.NB.26.2978.

### Checkpoint — 18/11/2026 (Giai đoạn E XONG + sửa 2 lỗi có sẵn, CHƯA commit)
- Task 14 tab Vấn đề (4 lọc nhanh theo BE, nút Nhận xử lý / Báo đã xử lý / Xác nhận đóng suy theo Issue::nextStatusTransitions, Báo vấn đề điền sẵn nhóm/GP); bật tab bằng Sửa nay cập nhật ngay.
- Sửa lỗi có sẵn (user chọn 2+3, "làm"): A — bảng Báo đã xử lý thêm Cách xử lý + Nhóm nguyên nhân (BE bắt buộc); B — mọi request gửi Accept: application/json ⇒ app hiện đúng câu lỗi 422; kèm sửa 401 không có `code` = hết phiên (nếu không sẽ mất tự đăng xuất).
- ⚠️ Ghi chú phát hành: trước đây 422 bị trả 302 ⇒ app coi như lưu thành công; từ nay báo lỗi đúng ⇒ bấm thử các luồng lưu chính (chấm công, đơn từ, báo kết quả) ở Task 17.
- 483 test toàn app. Dữ liệu thử: nhóm 12977 bật Meeting + Vấn đề; ISS-202611-0008 Hoàn thành.

### Checkpoint — 18/11/2026 (Task 15 Agent XONG, CHƯA commit)
- Màn TPE SMART AGENT (chào, hỏi đáp, bước, khối kết quả, thẻ chọn/thiếu quyền, hạn mức, lịch sử); hỏi thật 4 câu trên máy ảo; 552 test.
- Sửa khi bấm thử: dòng Agent kiểm quyền theo `permission_codes` (không theo tên quyền cũ); `**` trong `==…==`; ô ngày bảng công; sheet Hạn mức/Lịch sử cao 85%; tự cuộn; Lịch sử nạp lại khi mở.
- Ghi chú ngoài app: API Agent — lượt chọn người trả khối việc của chính người hỏi; web `AgentResultBlock.vue` dayOfMonth hiện "26".

### Checkpoint — 18/11/2026 (Task 16 banner XONG, CHƯA commit)
- Banner tin mới trong app (1 banner, tự ẩn 4 giây, bấm mở phòng, ‹ về danh sách chat; không hiện tin mình/hệ thống/phòng đang mở/tắt TB không bị @); 577 test; kiểm máy ảo bằng 3 tin thử emp 25 → hội thoại 99.

### Checkpoint — 18/11/2026 (TẤT CẢ 17 TASK XONG + soát toàn nhánh, CHƯA commit)
- Task 17: sửa 14 lỗi nhỏ tồn đọng; thử lưu thật đơn từ (chặn push bằng queue database, đã dọn + trả .env); kiểm chạy nền 1 phút không mất tin; push khi app tắt hẳn: user thử OK trên iPhone tpeDev release.
- Soát toàn nhánh: sẵn sàng sau 1 lượt sửa (mất tin khi kết nối lại trong lúc đang bắt kịp; mở tệp chỉ http/https; dừng hỏi lại khi chạy nền; 401 chỉ áp API của mình; cache quyền Agent theo phiên) — đã sửa, soát lại đạt. 595 test.
- User 18/11: Tin nhắn mặc định public, KHÔNG xét Cài đặt phân hệ.
- Tổng kết + toàn bộ quyết định: `tong-ket-app.md`.

### Checkpoint — 18/11/2026 (ĐÃ COMMIT + PUSH, chưa merge)
- TPE_APP `feature/chat-agent-app` 242dfcd · hrm-api `gop_db-chat-danh-ba-chuc-vu` 93c609a70 · hrm-client `gop_db-chat-tin-chua-doc` 128658916.
- Góp ý sau tổng kết đã làm: cụm tin như web, nút ✎, mục "Trao đổi công việc", tab Nhiệm vụ nhóm theo khuôn màn Nhiệm vụ, bong bóng mình #e6f5ef, tên người gửi #0F172A, ô nhập 1 dòng, dải "Tin chưa đọc" tự mất (app + web), push chat có "💬 ".

### Checkpoint — 18/11/2026 ĐÃ MERGE + DEPLOY
- TPE_APP `develop` a46dcd4 (chưa phát hành store) · hrm-api `gop_db` 50c02c5d8 · hrm-client `gop_db` 128658916 — ĐÃ DEPLOY prod TPE (không migration mới; worker chat-push đã restart).
