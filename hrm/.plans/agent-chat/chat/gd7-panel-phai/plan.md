# GĐ7 Chat — plan

> Design: `design.md` (cùng thư mục) · Nhánh `gop_db-chat-panel-phai` (hrm-api + hrm-client, tách origin/gop_db 13/11) ·
> worktree `wt-nhom-trao-doi` · API :8080 · Nuxt :3080. User cho phép code 13/11 ("làm"). Không chạy e2e tới khi user yêu cầu;
> xong mỗi lượt mở app cho user check.

## Phase A — 2 sửa nhỏ (hrm-client)

- [x] A1 Nút Đính kèm thẳng hàng + cùng kiểu `.v2-icon-btn--md` (`ChatComposer.vue` CSS: label margin 0, viền/bo/màu/icon/hover; `.cc__tools > *` flex-shrink 0)
- [x] A2 Panel trái 288 → 360px + placeholder "Tìm nhóm, tên, mã NV" (139px vừa ô 146px; "Tìm theo nhóm, tên, mã NV" cần 165px nên bỏ chữ "theo") (`ConversationList.vue`) — phương án 1 (user "làm", Claude chọn theo đề xuất)
- [x] A3 Đo lại DOM bằng Playwright (top các nút bằng nhau, rộng 30; panel 360, 0 tên bị cắt) + mở app cho user check
- [x] A4 Ghi ca e2e cần cập nhật (chưa chạy): ca nào phụ thuộc độ rộng 288 / placeholder cũ

Kết quả đo A3 (13/11, 1440×860, conv 99): 3 nút cùng top 819, 30×30, viền #e2e8f0, bo 8px, icon 14px; khối bọc 30px (trước 38).
Panel trái 360px, 0 tên bị cắt (trước 4), khung chat 1022px. A4: grep e2e/ không có ca nào bám 288px / placeholder cũ.

- [x] A5 (user check 13/11 "4 button cách xa nút đính kèm") — lỗi do A1: `flex-shrink:0` làm lộ `.v2-file__wrapper { width:100% }`
  của V2BaseFile, khối bọc ra 138px ⇒ ép `.cc__attach { width:30px }`. Đo lại: nhóm 3564 (4 nút) và 1–1 conv 99 (3 nút) đều
  cách đều 6px, cùng top 819, 30×30. (Nhóm 3537 user nêu không có trong db_gop_6_11.)

## Phase B — Panel phải: Ảnh · Tệp · Link · Nhiệm vụ

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (hoặc subagent-driven-development). Checkbox `- [ ]`.

**Goal:** cột phải cạnh khung chat hiện 5 ảnh / tệp / link mới nhất của hội thoại (+ 5 nhiệm vụ chưa đóng mới nhất ở nhóm bật
tab Nhiệm vụ), "Xem thêm" đúng đích đã chốt, cập nhật trực tiếp qua socket `chat` có sẵn.

**Architecture:** BE thêm bảng `chat_message_links` (ghi lúc gửi / sửa / chuyển tiếp) + 1 service đọc tài nguyên theo hội thoại
(lọc giống `MessageService::list`) + 2 API dưới `v1/assign/chat/conversations/{id}`. FE thêm `ChatSidePanel.vue` gắn trong
`ChatPane` (dùng chung cho Tin nhắn 1–1 và nhóm), nghe `$root` `chat-event` như ChatPane.

**Tech Stack:** Laravel 8 (PHP 8.1 local) · PHPUnit · Nuxt 2 / Vue 2 · V2Base*.

**Spec:** `design.md` (cùng thư mục) — mục 6 "Quyết định đã chốt" là chuẩn khi lệch chỗ khác.

### Global Constraints

- Nhánh `gop_db-chat-panel-phai` ở `wt-nhom-trao-doi/{hrm-api,hrm-client}`. KHÔNG commit (user tự báo).
- Chạy migration vào DB local `db_gop_6_11` chỉ sau khi hỏi user, nêu đúng tên file, chạy lẻ `--path`.
- Không chạy e2e tới khi user yêu cầu; xong mỗi Task FE đo DOM bằng Playwright rồi `open` app cho user check.
- Model mới `extends BaseModel`, bảng có `created_by`/`updated_by` + `timestamps()`.
- Không thêm sự kiện socket; không query trong vòng lặp; mỗi mục panel = 1 query `LIMIT 6` (6 để biết `has_more`), không COUNT.
- Ảnh = `file_type` bắt đầu `image/` HOẶC tên/đường dẫn khớp `\.(png|jpe?g|gif|webp|bmp|svg)(\?|$)` (giống `IMAGE_EXT` ở `utils/chat/chatFormat.js:89`).
- Regex link BE khớp FE `/(https?:\/\/[^\s<]+)/g` (`components/chat/ChatMessageItem.vue:326`); tối đa 20 link / tin, url ≤ 2000 ký tự.
- Nhiệm vụ = `WorkspaceTaskCanceller::openTaskQuery($ws)` + `(status != Nháp OR created_by = tôi)` (đúng tập `my_open_task_count`,
  `WorkspaceController.php:145`), sắp `tasks.id` giảm dần; chữ/màu trạng thái `Task::resolveStatusName/Color`.
- Thu gọn panel lưu `localStorage` key `chat.sidePanel.collapsed` (bọc try/catch); màn `< 1280px` mặc định thu gọn (không ghi).
- PHPUnit: `/opt/homebrew/opt/php@8.1/bin/php -d memory_limit=1G vendor/bin/phpunit <file>`.

### Review Focus

1. Tin **đã thu hồi / Xóa phía tôi / trước mốc xoá lịch sử** không được lộ trong panel — kể cả qua "Xem thêm" (test ở Task B2).
2. Người **không phải thành viên** gọi 2 API ⇒ 403 (middleware `$chatRead`) (test ở Task B3).
3. **Sửa tin** bỏ link ⇒ link biến khỏi panel; sửa thêm link ⇒ hiện (test B1 + xử lý `message.updated` ở B5).
4. **Chuyển tiếp** tin có link / tệp sang hội thoại khác ⇒ hiện ở panel hội thoại đích (test B1).
5. **Nháp nhiệm vụ của người khác** và việc Hoàn thành / Huỷ không hiện trong mục Nhiệm vụ (test B2).

---

### Task B1: Bảng `chat_message_links` + ghi link khi gửi / sửa / chuyển tiếp

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_17_000001_create_chat_message_links_table.php`
- Create: `hrm-api/Modules/Assign/Entities/Chat/ChatMessageLink.php`
- Create: `hrm-api/Modules/Assign/Services/Chat/ChatResourceService.php`
- Modify: `hrm-api/Modules/Assign/Services/Chat/MessageService.php` — `send()` :79, `forward()` :210, `edit()` :287
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/ChatSidePanelTest.php` (khung theo `ChatForwardTest.php`: `DatabaseTransactions`, setUp lấy 2–3 NV thật cùng công ty)

**Interfaces — Produces:**
- Bảng `chat_message_links`: `id`, `conversation_id` ubig, `message_id` ubig, `url` varchar(2000), `host` varchar(255),
  `created_by`, `updated_by`, `timestamps`; index `(conversation_id, id)` tên `chat_links_conv_id_index`, index `message_id`.
- `ChatResourceService::extractUrls(?string $body): array` — mảng url duy nhất, giữ thứ tự, ≤ 20.
- `ChatResourceService::syncLinks(ChatMessage $message): void` — xoá link cũ của tin rồi chèn lại 1 lệnh `insert` (tin hệ thống / sticker ⇒ chỉ xoá).

- [x] **Step 1–5 B1 xong** — `test_extract_urls_matches_fe_regex` (`"xem https://a.vn/x?y=1, và http://b.com<br>"` ⇒ `['https://a.vn/x?y=1,', 'http://b.com']` — giữ đúng hành vi regex FE, dấu phẩy dính url) · `test_send_records_links` · `test_edit_replaces_links` (sửa bỏ link ⇒ 0 dòng; thêm link mới ⇒ 1 dòng url mới) · `test_forward_records_links_in_target`.
- [ ] **Step 2:** chạy file test ⇒ FAIL (bảng / class chưa có).
- [ ] **Step 3:** HỎI user chạy migration `2026_11_17_000001_create_chat_message_links_table.php` vào `db_gop_6_11` (`migrate --pretend --path` trước). Được phép mới chạy `--path`.
- [ ] **Step 4:** code migration + model + 2 hàm; gọi `syncLinks` trong transaction của `send()`, `edit()`, và mỗi tin tạo ở `forward()`.
- [ ] **Step 5:** chạy file test ⇒ PASS; chạy lại `ChatApiTest` + `ChatForwardTest` ⇒ không vỡ.

### Task B2: Đọc tài nguyên theo hội thoại (service)

**Files:** Modify `ChatResourceService.php` · Test `ChatSidePanelTest.php`

**Interfaces — Produces:**
- `sidePanel(ChatConversation $c, int $me): array` ⇒ `['images'=>['items'=>[...≤5], 'has_more'=>bool], 'files'=>…, 'links'=>…, 'tasks'=>…|null]`
  (`tasks` = null nếu hội thoại không phải nhóm hoặc nhóm chưa bật `tasks` trong `enabled_tabs`).
- `resources(ChatConversation $c, int $me, string $kind, ?int $beforeId, int $limit = 30): array` ⇒ `['data'=>[…], 'has_more'=>bool]`;
  `$kind ∈ images|files|links`, sai ⇒ `InvalidArgumentException`; `$limit` kẹp 1..50; con trỏ = `id` của bảng nguồn (`files.id` / `chat_message_links.id`).
- Phần tử ảnh/tệp: `{id, message_id, name, url, type, size, sender_name, created_at}` · link: `{id, message_id, url, host, sender_name, created_at}`
  · nhiệm vụ: `{id, code, title, status_text, status_color, due_date}`. Ngày dạng `Y-m-d H:i:s`.

- [ ] **Step 1: Test hỏng** — `test_panel_excludes_recalled_hidden_and_cleared` (tạo 3 tin có ảnh: 1 thu hồi, 1 người xem đã hide, 1 trước `cleared_before_message_id` + 1 tin hợp lệ ⇒ `images.items` chỉ 1) · `test_images_and_files_are_split` (1 png + 1 pdf ⇒ mỗi mục 1) · `test_has_more_when_six` (6 link ⇒ 5 item, `has_more=true`) · `test_resources_cursor_pages_newest_first` · `test_tasks_open_only_and_hide_others_drafts` (Nháp người khác, Hoàn thành, Huỷ không ra; Nháp của tôi ra) · `test_tasks_null_for_direct_and_tasks_tab_off`.
- [ ] **Step 2:** chạy ⇒ FAIL.
- [ ] **Step 3:** code. Lọc chung 1 hàm `private scopeVisible($query, ChatConversation $c, int $me, string $msgAlias)`: join `chat_messages`, `conversation_id`, `id > cleared_before`, `recalled_at IS NULL`, `ChatMessageHide::excludeFor($q, $me, $msgAlias)`. Tên người gửi lấy 1 lần cho cả lô (cùng nguồn `ChatPresenter` dùng cho `sender`) — không query theo dòng.
- [ ] **Step 4:** chạy ⇒ PASS.

### Task B3: API + quyền

**Files:** Modify `hrm-api/Modules/Assign/Routes/Chat/api.php` (nhóm `conversations/{id}`, cạnh `/pins` dòng 67) · `Http/Controllers/Api/V1/Chat/ChatController.php` · Test `ChatSidePanelTest.php`

**Interfaces — Produces:** `GET /api/v1/assign/chat/conversations/{id}/side-panel` ⇒ `{data: sidePanel(...)}` ·
`GET …/{id}/resources?kind=&before_id=&limit=` ⇒ `{data:[…], has_more}`; `kind` sai ⇒ 422. Cả 2 middleware `$chatRead`.

- [ ] **Step 1: Test hỏng** — `test_side_panel_api_member_ok` · `test_side_panel_api_outsider_403` · `test_resources_api_bad_kind_422`.
- [ ] **Step 2:** chạy ⇒ FAIL. **Step 3:** code 2 action mỏng gọi service. **Step 4:** PASS; chạy cả thư mục `Modules/Assign/Tests/Feature/Workspace` (2 ca `WorkspaceTaskTest` fail sẵn trên gop_db — ghi nhận, không tính).

### Task B4: Lệnh bổ sung link cho tin cũ

**Files:** Create `hrm-api/Modules/Assign/Console/ChatBackfillLinksCommand.php` (đăng ký như command khác của module) · Test `ChatSidePanelTest.php`

**Interfaces:** `php artisan assign:chat-backfill-links {--chunk=1000} {--dry-run}` — duyệt `chat_messages` type text có `body LIKE '%http%'` theo `chunkById`, gọi `syncLinks`; in số tin / số link. Chạy lại không nhân đôi (syncLinks xoá trước).

- [ ] **Step 1:** test `test_backfill_is_idempotent` (chạy 2 lần ⇒ cùng số dòng). **Step 2:** FAIL. **Step 3:** code. **Step 4:** PASS. Chạy thật trên local chỉ khi user cho (ghi DB).

### Task B5: `ChatSidePanel.vue` + gắn vào ChatPane

**Files:**
- Create: `hrm-client/components/chat/ChatSidePanel.vue`
- Modify: `hrm-client/components/chat/ChatPane.vue` (bọc thân khung tin + composer và panel trong 1 hàng flex; truyền `conversationId`, `tasksWorkspaceId` đang có)
- Modify: `hrm-client/pages/assign/workspaces/_id/index.vue` — nghe `@open-tasks` ⇒ `panel = 'tasks'` (ChatPane chuyển tiếp emit)

**Interfaces:**
- Props `conversationId: Number`, `tasksWorkspaceId: Number|null` · emits `open-tasks`, `open-task(id)`, `jump(messageId)`.
- ChatPane: `open-task` ⇒ `openTask(id)` có sẵn (:651); `jump` ⇒ cơ chế nhảy tin của tìm kiếm (`list` cursor `around`); `open-tasks` emit lên trang.
- Gọi API bằng `chatApi(this.$axios).get('chat/conversations/' + id + '/side-panel')` / `…/resources`.

- [ ] **Step 1:** dựng khung theo `components/agent/AgentSidePanel.vue` (`.agp`: nền `#fcfdfe`, viền `#e5e7eb`, bo 8px, thanh cuộn mảnh), rộng 300px; 4 mục: Ảnh (lưới 3 cột, bấm ⇒ `ChatImageViewer` qua ChatPane), Tệp (`fileIcon` + tên + dung lượng + người gửi · ngày), Link (host + đường dẫn rút gọn, `target=_blank rel=noopener`, nút "Tới tin nhắn"), Nhiệm vụ (mã · tên · `V2BaseBadge :color="status_color"` · hạn). Mục rỗng ⇒ 1 dòng xám `#6b7280` "Chưa có …". Mọi nút `V2BaseIconButton`/`V2BaseButton`.
- [ ] **Step 2:** "Xem thêm": Ảnh/Tệp/Link ⇒ panel chuyển chế độ danh sách đủ của mục đó (nút ← quay lại, cuộn chạm đáy tải `before_id`); Nhiệm vụ ⇒ emit `open-tasks`. Chỉ hiện "Xem thêm" khi `has_more`.
- [ ] **Step 3:** thu gọn: nút trên đầu panel; thu gọn = dải 36px có nút mở. Key + ngưỡng theo Global Constraints. Không hiện panel khi ChatPane đang ở khung Agent.
- [ ] **Step 4:** cập nhật trực tiếp (`$root.$on('chat-event')`, gỡ ở `beforeDestroy`): `message.created` có `files`/link ⇒ chèn đầu mục (tách link bằng đúng regex FE, `id` tạm âm), tin `system` hoặc `card` ⇒ nạp lại riêng mục Nhiệm vụ (gọi lại side-panel, lấy `tasks`); `message.updated` CHỈ nạp lại side-panel (1 request) khi tin đó đang có trong panel (`message_id` trùng) hoặc thân tin mới có
  link — `message.updated` còn bắn cho cảm xúc / ghim, nạp lại mọi lần là bão request ở nhóm đông; `message_hidden` ⇒ bỏ các dòng
  có `message_id` đó tại chỗ (không gọi API). Đổi hội thoại ⇒ nạp lại.
- [ ] **Step 5:** Playwright (1440×860, namdangit): đo panel rộng 300, khung chat ≥ 700, 4 mục ở nhóm bật Nhiệm vụ / 3 mục ở 1–1; gửi tin có link ⇒ dòng link xuất hiện không reload; thu hồi ⇒ mất; thu gọn rồi F5 ⇒ vẫn thu gọn; viewport 1200 ⇒ mặc định thu gọn. `open` app cho user check.

### Task B6: Tài liệu

- [ ] README nhóm (`.plans/agent-chat/README.md` §1, §3) + `.plans/STATUS.md` mục AGENT + CHAT: GĐ7 xong / migration chờ deploy `2026_11_17_000001` + lệnh `assign:chat-backfill-links` chạy 1 lần trên prod (hỏi user).
- [ ] Ghi ca e2e cần thêm khi user cho chạy: panel 1–1 / nhóm, cập nhật trực tiếp, thu gọn; chạy cả `agent-chat` + `agent-chat-pin` vì sửa ChatPane.

## Ledger Phase B (executing-plans, làm tại chỗ, KHÔNG commit — user tự báo)

- Ruling: không commit / bỏ script task-start/task-done (chúng dựa trên commit) — user quy định tự commit — sai thì chỉ mất mốc review theo commit.
- 13/11 user cho chạy TOÀN BỘ migration chờ (16 bản) vào db_gop_6_11: đã liệt kê + soát `--pretend`, chạy lẻ từng `--path`, 0 còn chờ. Bản đổi dữ liệu: `move_machine_groups_to_product_types` (4.017 dòng productables kiểu Group → sao lưu `productables_group_backup_20261110`, chèn kiểu ProductType theo tên, xoá kiểu Group) · `backfill_updated_by_on_handover_acceptance_product_records` (UPDATE updated_by = created_by chỗ NULL).
- Task B1: complete (tests: ChatSidePanelTest 4/4 OK · ChatApiTest 10/10 · ChatForwardTest 7/7). Ghi link cả tin "lời nhắn" kèm chuyển tiếp.
- Task B2: complete (ChatSidePanelTest 10/10). Ruling: lọc ảnh bằng tham số ràng buộc + COALESCE — `?` trong regex viết thẳng bị PDO coi là placeholder; file_type NULL làm `NOT(...)` ra NULL ⇒ tệp mất khỏi cả 2 mục — sai thì chỉ lệch phân loại ảnh/tệp.
- Task B3: complete (ChatSidePanelTest 13/13; cả thư mục Workspace 128 ca: chỉ 2 ca `WorkspaceTaskTest` fail sẵn trên gop_db).
- Task B4: complete (14/14). Ruling: lệnh đặt ở `app/Console/Commands/Assign/ChatBackfillLinksCommand.php` (nơi mọi lệnh `assign:*` nằm, Kernel tự load) thay vì `Modules/Assign/Console` — sai thì chỉ đổi chỗ file. Dry-run local: 0 tin có link ⇒ không chạy thật.
- Task B5: complete — Playwright 1440×860 (namdangit): panel 320px, khung chat 702px (nhóm 3564 / 1–1 conv 99); nhóm 1612 bật Nhiệm vụ ⇒ 4 mục, 1–1 ⇒ 3 mục; gửi tin 2 link ⇒ hiện ngay, KHÔNG thêm request side-panel; thu hồi ⇒ mất cả 2 link của tin; thu gọn ⇒ dải 44px, chat 978px, F5 vẫn thu gọn, lúc thu gọn 0 request; "Xem thêm" Link ⇒ `resources?kind=links&limit=30`, nút ← quay lại; "Xem thêm" Nhiệm vụ ⇒ `?panel=tasks`; bấm dòng nhiệm vụ ⇒ TaskPanel 660px; viewport 1200 ⇒ mặc định thu gọn. Console: chỉ lỗi socket :8895 (local không chạy socket). API side-panel 0,27s (ngang pins 0,20 / messages 0,23); EXPLAIN đi index chat_messages (conversation_id,id).
  - Ruling: panel rộng 320px (đúng `.agent-side` Agent) thay vì ~300 — design ghi "~300, quyết định của Claude", bám khuôn có sẵn — sai thì đổi 1 số.
  - Ruling: nút thu gọn đặt TRONG panel (đầu panel + dải 44px) thay vì đầu khung chat — màn nhóm và 1–1 có 2 đầu khung khác nhau, đặt trong panel dùng chung 1 chỗ — sai thì dời nút.
  - Ruling: ChatPane gọi thẳng `onCreated/onUpdated/onHidden` của panel sau gửi / sửa / thu hồi / xoá phía tôi của CHÍNH MÌNH (không chờ socket) — phát hiện khi socket local tắt: tin mình gửi không lên panel; socket vẫn lo tin người khác, chống trùng theo id tin — sai thì thừa 1 lần gọi hàm.
  - Dữ liệu thử để lại trên db_gop_6_11: 2 tin có link trong nhóm 3564 (conv 2201, của namdangit). Việc tạm id 21349 nhóm 1612 đã xoá.
- Task B6: complete — README §1/§3 + STATUS checkpoint 13/11 ~21:00. Ca e2e cần thêm KHI user cho chạy (chưa viết/chạy): (1) 1–1 có 3 mục, nhóm bật Nhiệm vụ có 4 mục; (2) gửi tin có link/ảnh ⇒ lên panel không reload; (3) thu hồi / Xóa phía tôi ⇒ mất khỏi panel; (4) "Xem thêm" Link cuộn tải tiếp + ←; (5) thu gọn giữ sau F5; (6) người ngoài nhóm gọi API side-panel 403. Sửa ChatPane ⇒ chạy cả bộ chat + `agent-chat` + `agent-chat-pin`.

### Final review (reviewer opus, đọc cả working tree 2 repo) — 0 Critical · 6 Important · 6 Minor. Đã tự kiểm lại từng điểm trong code: đúng.
- Final: fixed #1 thu gọn rồi mở lại vẫn hiện dữ liệu cũ (kể cả tin đã thu hồi) — `setCollapsed(false)` luôn `load()`; Playwright: mở lại ⇒ 1 request side-panel.
- Final: fixed #2 Link không dùng index (conversation_id,id) — thêm `r.conversation_id`; EXPLAIN: `chat_links_conv_id_index` Backward index scan, không filesort. Suite 20/20.
- Final: fixed #3 Ảnh/Tệp quét cả hội thoại + filesort — 2 bước (tin có tệp qua EXISTS, quét ngược `chat_messages_conv_id_index`, dừng ở limit+1; rồi tệp của các tin đó); con trỏ Ảnh/Tệp = id TIN, API trả `next_before_id`. `test_files_page_by_message_cursor` + `test_links_cursor_returns_next_before_id` RED→GREEN; EXPLAIN: Backward index scan + FirstMatch, không filesort.
- Final: fixed #4 bão request — panel thôi tự nghe `chat-event`; ChatPane `notifySidePanel` chuyển xuống, `message.updated` chỉ báo khi thân tin đổi / thu hồi (so bản cũ trước replaceMessage); tin system/card chỉ nạp mục Nhiệm vụ qua `side-panel?only=tasks` và bỏ qua khi `tasks` null. `test_side_panel_only_tasks` RED→GREEN; Playwright: cảm xúc 0 request, sửa 1, system ở nhóm tắt Nhiệm vụ 0.
- Final: fixed #5 "Xem thêm" không cập nhật khi sửa tin — `onUpdated` gọi lại `openMore(expanded)`; Playwright: 1 request resources.
- Final: fixed #6 XSS `javascript:` qua đường dẫn tệp — `SendMessageRequest` `files.*.url` regex `^https?://` (khung tin + panel đều được che vì chặn từ nguồn); panel thêm `safeUrl` cho href/src. `test_file_url_must_be_http` RED→GREEN. Dữ liệu local: 0 tệp chat không phải http(s).
- Final: fixed (minor rẻ, cùng chỗ sửa) lỗi "Xem thêm" đè cả panel — biến `more.error` riêng; chống trùng `onCreated` bằng `seen` + `hasMessage` (ChatPane báo + socket báo lại).
- Final: thêm ca test thiếu: `test_resources_api_outsider_403`, `test_forward_files_show_in_target_panel`. Suite ChatSidePanelTest 20/20 · Workspace 135 (2 fail sẵn WorkspaceTaskTest).
- Final: minor (deferred): `isImageFile` FE xét `url || name`, BE xét path HOẶC name ⇒ tệp url không đuôi nhưng tên .png có thể nhảy từ Tệp sang Ảnh sau khi nạp lại.
- Final: minor (deferred): `dropMessage` làm mục tóm tắt hụt dưới 5 dòng dù còn `has_more`, không tự bù tới lần nạp sau.
- Final: minor (deferred): race hẹp — `load()` đang bay thì có tin bị thu hồi, kết quả cũ về sau ghi đè ⇒ dòng đã thu hồi hiện lại tới lần nạp sau.
- Final: minor (deferred): `ChatMessageItem.vue:71,80` vẫn gắn `f.url` thẳng vào href (đã chặn từ BE nên dữ liệu mới an toàn; FE chưa lọc).
- Final: Ruling: "Lộ tin trước mốc xoá lịch sử ở FE" (reviewer bỏ qua) — BE đã lọc `cleared_before_message_id` ở mọi đường đọc của panel; web chưa có nút xoá lịch sử — sai thì chỉ lộ tới lần nạp sau.
- Final: Ruling: "thành viên chat không phải thành viên nhóm thấy tên nhiệm vụ" (reviewer bỏ qua) — panel chỉ cho người qua `$chatRead` của hội thoại nhóm, cùng tập người đang thấy thẻ nhiệm vụ trong tin; không mở rộng phạm vi — sai thì cần gate thêm theo WorkspaceAccess.

### E2E 13/11 tối (user yêu cầu "Chạy e2e") — :3080 / :8080 (`AGENT_FAKE=1`) / socket :8895, NV 13 · 24 · 25, Node 20, `--workers=1`
- MỚI `e2e/tests/assign/chat-panel-phai.spec.ts` **6/6 passed** (P1 4 mục / 1–1 3 mục + đo 320/≥700 · P2 Xem thêm · P3 realtime B gửi/cảm xúc 0 request/thu hồi · P4 tự gửi + Xóa phía tôi · P5 thu gọn F5 + 1200 · P6 người ngoài 403).
- chat-gd2-polish 7/7 · chat-toolbar-zalo 8/8 · workspace-tasks 12/12 · agent-chat-pin 6/6 · agent-chat 19/19 (chạy trên :3080/:8080 để phủ ChatPane mới).
- chat-bo-sung 6/6 và chat-thong-bao-emoji 10/10 — lượt 1 fail vì hết giờ tải trang (test timeout 30s, ảnh chụp: trang còn vòng tải Nuxt; swap 7,4–8,2 GB); chạy lại với `--timeout=120000` thì đạt hết.
- chat-core 7/8 — ca "Đóng nhóm" FAIL 3 lần (cả chạy riêng): bước `expect(ws-reopen).toBeVisible()` (5s cứng trong test). Trace: POST close 200 sau 912ms; GET `unread-count` mất 3.679ms (curl lẻ 0,2s) ⇒ GET `workspaces/{id}` xếp hàng sau trên `php -S` 1 luồng, chưa trả về khi hết 5s. Luồng không đi qua code GĐ7 (tab Cấu hình, API close / unread-count không đổi). ~~CHƯA KIỂM XONG~~ → **ĐÃ CHỐT (user chọn 1)**: khởi động lại :8080 bằng `PHP_CLI_SERVER_WORKERS=4 AGENT_FAKE=1 php -S` ⇒ ca "Đóng nhóm" chạy riêng PASS (19,4s); cả bộ chat-core `--timeout=120000` **8/8 passed** (1,4 phút). Nguyên nhân = `php -S` 1 luồng xếp hàng request, không phải code GĐ7.
- Dữ liệu e2e để lại: nhóm "[e2e] Nhóm chat …" của chat-core (spec ghi dọn bằng SQL — chưa dọn, có cả nhóm từ các phiên trước). Spec mới tự dọn ở afterAll.
