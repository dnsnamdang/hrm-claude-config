# GĐ13 — @all nhắc tất cả thành viên nhóm — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> Phụ trách: @namdangit · 15/11/2026 · trạng thái: CODE XONG 15/11 (user cho "làm" — phương án a: nhánh tách từ GĐ12), CHƯA commit.

**Goal:** Gõ `@all` trong nhóm ⇒ mọi thành viên (trừ người gửi) thấy dấu @ ở dòng hội thoại; ai bật thông báo nhận push / toast "đã nhắc đến mọi người".

**Architecture:** 1 cờ `chat_messages.mention_all` (không ghi 1 dòng/người). BE đọc cờ ở 3 chỗ: đếm `mentioned` danh sách hội thoại, job `PushChatMessage`, `ChatPresenter`. FE: gợi ý `@all` trong `ChatComposer`, gửi `mention_all`, tô `@all`, store + notifier xét cờ.

**Tech Stack:** Laravel 8 (PHP 8.1 local), PHPUnit; Nuxt 2 / Vue 2; Playwright MCP.

**Spec:** `.plans/agent-chat/chat/gd13-mention-all/design.md`

## Global Constraints

- Repo / nhánh: `hrm-api` + `hrm-client`, nhánh mới `gop_db-chat-mention-all` tách từ `origin/gop_db` (worktree hỏi user khi xin lệnh code — `wt-nhom-trao-doi` đang có GĐ12 chưa commit).
- Ai cũng @all được (người có quyền gửi tin); chat 1–1 (`direct`) ⇒ cờ luôn false.
- @all KHÔNG vượt tắt thông báo (`muted`); @Tên vẫn vượt như cũ.
- Câu push / toast: `"<Tên người gửi> đã nhắc đến mọi người: <nội dung>"` (push) · `"Đã nhắc đến mọi người: <nội dung>"` (toast web). Bị @Tên trong cùng tin ⇒ ưu tiên câu "nhắc đến bạn".
- Token `@all`: không phân biệt hoa thường, đứng đầu chuỗi hoặc sau khoảng trắng, sau nó là hết chuỗi / khoảng trắng / dấu câu — regex FE `/(^|\s)@all(?=$|[\s.,!?:;])/i`.
- PHPUnit: `php -d memory_limit=1G vendor/bin/phpunit Modules/Assign/Tests/Feature/Workspace` (php 8.1).
- Không chạy toàn bộ e2e cho tới khi user yêu cầu; đo DOM bằng Playwright MCP + mở app cho user check.

## Review Focus

1. Người gửi @all KHÔNG tự thấy dấu @ ở hội thoại của mình (query đã loại `sender_id = me` — có test ở Task 2).
2. Sửa tin bỏ chữ `@all` ⇒ cờ về false, dấu @ biến mất (Task 1 test + Task 4 FE gửi cờ khi sửa).
3. Tin @all đã thu hồi / đã "Xoá ở phía tôi" / nằm trước mốc đã đọc ⇒ không tính (Task 2 test).
4. Người tắt thông báo + tin vừa @all vừa @Tên mình ⇒ vẫn được push "nhắc đến bạn" (Task 3 test).
5. Chữ `@allan` / `email@all.vn` không bị coi là @all (Task 4 — regex + kiểm tay ở Task 5).

---

### Task 1: Cột `mention_all` + lưu khi gửi / sửa + trả ra presenter (BE)

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_21_000001_add_mention_all_to_chat_messages_table.php` — `boolean('mention_all')->default(false)->after('meta')`; down drop.
- Modify: `Modules/Assign/Entities/Chat/ChatMessage.php` — thêm `mention_all` vào `$fillable`, `$casts` `'mention_all' => 'boolean'`.
- Modify: `Http/Requests/Chat/SendMessageRequest.php`, `EditMessageRequest.php` — `'mention_all' => 'nullable|boolean'`.
- Modify: `Services/Chat/MessageService.php` — `send()` (dòng ~116 `ChatMessage::create`) ghi `mention_all`; `edit()` thêm tham số; helper `private function mentionAllFlag(ChatConversation $c, $value): bool` (false nếu `direct`).
- Modify: `Http/Controllers/Api/V1/Chat/ChatController.php::edit` — truyền `(bool) $request->input('mention_all', false)`.
- Modify: `Services/Chat/ChatPresenter.php` (~dòng 164 cạnh `mention_ids`) — `'mention_all' => !$recalled && (bool) $m->mention_all`.
- Test: `Modules/Assign/Tests/Feature/Workspace/ChatApiTest.php`.

**Interfaces:**
- Produces: cột `chat_messages.mention_all`; `MessageService::edit(ChatMessage $message, int $me, string $body, array $mentionIds = [], bool $mentionAll = false): ChatMessage`; JSON tin có `mention_all: bool`.

- [x] **Step 1: Viết test `test_nhac_tat_ca_luu_co_sua_tin_va_1_1_bo_qua`**
  - gửi vào nhóm `['body' => '@all họp nhé', 'mention_all' => true]` ⇒ tin cuối `mention_all === true`, `mention_ids === []`.
  - sửa tin đó `['body' => 'họp nhé', 'mention_all' => false]` ⇒ `mention_all === false`.
  - thu hồi 1 tin @all khác ⇒ JSON `mention_all === false`.
  - chat 1–1 gửi `mention_all => true` ⇒ lưu `false` (đọc DB `chat_messages.mention_all`).
- [x] **Step 2:** chạy `--filter test_nhac_tat_ca_luu_co` ⇒ FAIL (cột chưa có).
- [x] **Step 3:** viết migration + code như Files. Chạy migration CHỈ file này: `php artisan migrate --path=Modules/Assign/Database/Migrations/2026_11_21_000001_add_mention_all_to_chat_messages_table.php --force` (DB `db_gop_6_11` — chỉ chạy khi user đã cho phép).
- [x] **Step 4:** chạy lại test ⇒ PASS; chạy cả `ChatApiTest` ⇒ PASS.

### Task 2: Dấu @ ở danh sách hội thoại tính tin @all (BE)

**Files:**
- Modify: `Services/Chat/ConversationService.php` (~dòng 458) — `'mentioned'` = `COUNT(mm.id) + COALESCE(SUM(m.mention_all), 0)`; giữ nguyên các điều kiện join (đã loại tin của mình, tin ẩn, tin thu hồi, tin ≤ last_read / cleared_before).
- Test: `ChatApiTest.php`.

**Interfaces:** Consumes cột Task 1. `mentioned` vẫn là bool ở API (dòng ~421 không đổi).

- [x] **Step 1: Viết test `test_nhac_tat_ca_bat_dau_at_cho_nguoi_khac`**
  - ME gửi `@all` ⇒ others[0] thấy `mentioned === true`; ME thấy hội thoại `mentioned === false`.
  - others[0] đọc (`/read`) ⇒ `mentioned === false`.
  - ME gửi `@all` rồi thu hồi ⇒ others[0] `mentioned === false`.
  - ME gửi `@all`, others[0] "Xoá ở phía tôi" tin đó ⇒ `mentioned === false`.
- [x] **Step 2:** chạy ⇒ FAIL.
- [x] **Step 3:** sửa select như Files.
- [x] **Step 4:** chạy ⇒ PASS; cả thư mục `Tests/Feature/Workspace` ⇒ PASS (trừ 2 ca `WorkspaceTaskTest` fail sẵn trên origin/gop_db — ghi lại nếu còn).

### Task 3: Push — @all theo tắt thông báo, câu "nhắc đến mọi người" (BE)

**Files:**
- Modify: `Jobs/Chat/PushChatMessage.php` — lấy thêm `mention_all` ở query `$unread` (dòng ~99 `get(['id','sender_id','mention_all'])`); điều kiện bỏ qua người `muted` GIỮ NGUYÊN (chỉ @Tên mới vượt); dòng `$line`: bị @Tên ở tin này ⇒ "đã nhắc đến bạn"; else tin này `mention_all` ⇒ `$senderName . ' đã nhắc đến mọi người: ' . $text`; else như cũ.
- Test: `Tests/Feature/Workspace/ChatPushStickerTest.php`.

- [x] **Step 1: Viết test `test_nhac_tat_ca_push_theo_tat_thong_bao`**
  - nhóm ME, a, b, c; b muted; c muted; tin ME `@all @C` với `mention_all = true` + `ChatMessageMention` cho c.
  - pushes keys = `[a, c]` (b muted không nhận).
  - body của a chứa `'đã nhắc đến mọi người: @all @C'`; body của c chứa `'đã nhắc đến bạn: '`.
- [x] **Step 2:** chạy ⇒ FAIL. **Step 3:** sửa. **Step 4:** cả `ChatPushStickerTest` ⇒ PASS.

### Task 4: FE — gợi ý @all, gửi cờ, tô chữ, store + toast

**Files:**
- Modify: `hrm-client/components/chat/ChatComposer.vue`
  - `mentionItems`: thêm mục đầu `{ all: true, fullname: 'all', count: members.length }` khi `query` rỗng hoặc `fold('all')`/`fold('tat ca')` bắt đầu bằng `fold(query)`; chỉ khi `members.length > 0` (tức hội thoại space). Tổng vẫn ≤ 8 dòng.
  - Template dòng gợi ý: mục all hiện `@all` + chữ xám "Nhắc tất cả (N thành viên)", icon `ri-group-line`, `data-testid="chat-mention-all"`; style theo `cc__mention-item`.
  - `pickMention(u)`: `u.all` ⇒ chèn `@all `, không push vào `mentioned`.
  - Gửi (dòng ~541) và sửa: `mention_all: MENTION_ALL_RE.test(body)` với hằng `MENTION_ALL_RE = /(^|\s)@all(?=$|[\s.,!?:;])/i` (đặt trong `utils/chat/mentionAll.js`, export `hasMentionAll(body)`).
- Modify: `components/chat/ChatPane.vue` (~772) — chuyển `mention_all: payload.mention_all` lên API (gửi + sửa).
- Modify: `components/chat/ChatMessageItem.vue::html` — `m.mention_all` ⇒ bọc token `@all` bằng `<span class="cm__mention">` (sau escape, cùng regex, giữ khoảng trắng đầu).
- Modify: `store/chat.js` (~293) — `if ((m.mention_ids || []).includes(me) || (m.mention_all && m.sender_id !== me)) changes.mentioned = true`.
- Modify: `utils/chat/chatNotifier.js` (~64–78) — điều kiện vượt muted giữ chỉ `mention_ids`; tiền tố: `mention_ids` có me ⇒ "Đã nhắc đến bạn: "; else `mention_all` ⇒ "Đã nhắc đến mọi người: ".

- [x] **Step 1:** sửa theo Files.
- [x] **Step 2:** Nuxt :3080 biên dịch không lỗi (log `Compiled with` / `Waiting for file changes`, không `ERROR`).

### Task 5: Kiểm bằng Playwright MCP (đo DOM) + mở app cho user

- [x] Nhóm có ≥ 3 thành viên, NV 13: gõ `@` ⇒ đếm `[data-testid=chat-mention-all]` = 1, chữ chứa đúng số thành viên trừ mình; gõ `@ta` ⇒ vẫn có; gõ `@nguyen` ⇒ không có.
- [x] Chọn ⇒ ô soạn có `@all `; gửi ⇒ request POST body `mention_all: true` (bắt network); tin hiện `.cm__mention` text `@all`.
- [x] Gõ tay `email@all.vn` gửi ⇒ request `mention_all: false`, không có `.cm__mention`.
- [x] Tài khoản thứ 2 (JWT tinker) mở danh sách ⇒ dòng nhóm có `.cr__badge--at`; NV 13 (người gửi) không có.
- [x] Sửa tin bỏ `@all` ⇒ `.cm__mention` biến mất, request `mention_all: false`.
- [x] Ghi các ca e2e cần thêm vào `chat-core` (chạy khi user yêu cầu); `open http://127.0.0.1:3080/assign/messages` cho user check.

---

### Checkpoint — 15/11/2026
Vừa hoàn thành: design.md (user duyệt 15/11) + plan.md.
Đang làm dở: —
Bước tiếp theo: user xem plan → hỏi "làm" kèm phạm vi (repo · nhánh · worktree · migration `2026_11_21_000001` vào `db_gop_6_11`).
Blocked: chưa có lệnh code; worktree `wt-nhom-trao-doi` đang có GĐ12 chưa commit.

### Checkpoint — 15/11/2026 ~07:30
Vừa hoàn thành: Task 1–5. Nhánh `gop_db-chat-mention-all` (api + client, wt-nhom-trao-doi) tách từ `gop_db-chat-nhom-du-an-kh` ⇒ MANG THEO GĐ12 chưa commit. CHƯA commit.
Migration `2026_11_21_000001_add_mention_all_to_chat_messages_table` ĐÃ chạy db_gop_6_11 (chạy lẻ --path --force). Deploy prod cần chạy migration này.
Kiểm: PHPUnit `Tests/Feature/Workspace` 229/229 OK (3 ca mới: 2 ChatApiTest + 1 ChatPushStickerTest) · Playwright MCP :3080 nhóm 96 (12 TV): gõ `@` ⇒ 8 dòng, dòng 1 `chat-mention-all` "Nhắc tất cả (11 thành viên)"; `@ta` còn, `@nguyen` mất; chọn + gửi ⇒ request `mention_all:true`, `.cm__mention` "@all"; NV 24 dòng nhóm có `.cr__badge--at`, API NV 13 `mentioned:false`; `email@all.vn` ⇒ `mention_all:false`; sửa bỏ @all ⇒ PUT `mention_all:false`, NV 24 hết @ · Node: regex 8 ca + chatNotifier (muted không toast @all, vẫn toast @Tên, câu "Đã nhắc đến mọi người"). Tin thử 21533/21534 đã thu hồi.
E2E cần thêm khi user yêu cầu chạy: ca @all trong `chat-core.spec.ts` (gợi ý + gửi + dấu @ tài khoản 2 + sửa bỏ @all).
Bước tiếp theo: user thử :3080 → báo commit / gộp cùng GĐ12 lên gop_db → deploy TPE (migration 2026_11_20_000001 + 2026_11_21_000001).
Blocked: —

### Task 6 (bổ sung 15/11, user "1 - làm"): tô nền @all / @Tên NGAY TRONG Ô SOẠN

User: gõ @all trên ô soạn phải highlight để phân biệt với nội dung. Chốt: tô cả `@all` lẫn `@Tên` đã chọn từ gợi ý, cùng màu khung tin (#eef4fc / #1a5aa0). Cách: lớp `.cc__hl` nằm DƯỚI `V2BaseTextarea` (textarea chữ trong suốt + `caret-color`), không chuyển sang contenteditable.
- [x] `utils/chat/mentionAll.js::composerHighlightHtml(text, names, cls)` — escape + bọc span, không padding/đậm (khớp ký tự), dòng cuối trống thêm ký tự rỗng.
- [x] `ChatComposer.vue`: `highlightHtml` computed (chat 1–1 không tô), `syncHl()` chép font/padding/viền/kích thước + bù bề rộng thanh cuộn, đồng bộ `scrollTop`, `ResizeObserver`; CSS `.cc__ta` trong suốt, `.cc__hl` màu chữ #0f172a.
- [x] Playwright :3080 nhóm 96: hộp textarea = lớp dưới (435,602.5,704×53); font/padding giống; `@all` + `@Bùi Huyền Diệu` có span đúng màu; text lớp dưới == value; 15 dòng: offsetHeight 160/160, scrollHeight 599/599, scrollTop 439/439, padding phải lớp dưới 26px (= 12 + thanh cuộn 14); chồng chữ đỏ textarea lên lớp dưới — khít, không bóng lệch; placeholder vẫn hiện #9ca3af. Bắt được + sửa 1 lỗi: lớp dưới chép nhầm màu chữ trong suốt ⇒ đặt cứng #0f172a.

### Checkpoint — 15/11/2026 (commit + push)
Vừa hoàn thành: user "check ok ⇒ commit và push lên gop_db". 1 commit/repo gồm GĐ12 + GĐ13: api `72f929f76` · client `9f5014f3b`, fast-forward lên origin/gop_db.
Bước tiếp theo: deploy TPE — chạy migration `2026_11_20_000001_add_source_unique_to_workspaces` + `2026_11_21_000001_add_mention_all_to_chat_messages_table`; build client.
Blocked: —

### Checkpoint — 15/11/2026 (DEPLOY TPE)
Vừa hoàn thành: `build_tpe.sh` EXIT 0 — prod api `72f929f76` · client `9f5014f3b`; migration `2026_11_20_000001` + `2026_11_21_000001` chạy batch 478; route cache + queue:restart; client build + tráo; site 200. GĐ12 + GĐ13 ĐÃ lên prod TPE.
Bước tiếp theo: user thử @all trên prod; GĐ12 còn 6 ruling chờ user soát.
