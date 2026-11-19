# Plan code — CORE CHAT: Nhóm trao đổi + chat 1–1 (web) — viết 11/11/2026

> Bàn giao: `../ban-giao-phien-chat.md` · Spec: `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md`
> (§3.0–3.5, §3.11, §3.12, §4.1–4.6, §4.4b, §5.1) · Mockup chốt: `.plans/gop-db/phan-he-cong-viec/gd0-mockup/` màn 01, 04, 05, 08, 11–13, 21, 31, 32.
> Plan này thay mục **GĐ1** (viết theo mô hình cũ) + phần chat của **GĐ3** trong `.plans/gop-db/phan-he-cong-viec/plan.md` cho đợt "core chat" (việc C1).
> **Trạng thái: CHỜ USER DUYỆT. Chưa có lệnh code.** Duyệt plan ≠ cho phép code (CLAUDE.md gốc).
> Phụ trách: @namdangit

## 0. Phạm vi đợt này

**LÀM (core chat, web):**
1. Nhóm trao đổi: tạo (có / không thời hạn), sửa tên + thời hạn, đóng / mở lại, danh sách nhóm của tôi.
2. Thành viên: thêm từng người + lấy cả phòng ban / bộ phận (chép 1 lần, soát tick, bỏ trùng), đổi vai trò Quản lý / Thành viên / Xem, bớt người, luật "luôn ≥ 1 Quản lý", Quản lý cuối nghỉ việc ⇒ tự nâng người vào sớm nhất.
3. Hội thoại (`space` = chat nhóm, `direct` = 1–1, để sẵn `group`): tin chữ, file / ảnh, @nhắc tên, trả lời, cảm xúc, ghim tin (≤ 20), sửa / thu hồi trong 24h, đã xem + đếm chưa đọc, ghim / tắt thông báo / đánh dấu chưa đọc hội thoại, tìm tin.
4. Chat 1–1 với mọi NV đang làm việc của mọi công ty; popup Danh bạ (tìm, lọc công ty, nhóm theo phòng ban).
5. Realtime qua `server_node/server.js` (sự kiện `chat` tách khỏi `notification` — không bật chuông / toast).
6. FE: khung kiểu Teams — cột Hội thoại + khung chat; màn **Tin nhắn**; màn nhóm (chat + Thành viên + Cấu hình); icon Tin nhắn topbar + mục menu.

**CHƯA LÀM đợt này (ghi để khỏi sót):**
- Dự án KH (TKT / GP / HĐ) tự sinh không gian — N2p, làm sau.
- Tab Nhiệm vụ / Meeting / Vấn đề / File trong nhóm, thẻ `#` việc, tạo việc từ tin, tin hệ thống theo sự kiện việc + cấu hình 9 sự kiện (GĐ2 + chat đợt 2). Cột `enabled_tabs` vẫn tạo sẵn; mục "Tab sử dụng" ẩn tới GĐ2.
- Bịt lỗ hổng `TaskController::show` / `TaskService::update` (đi cùng GĐ2 khi Task có cột không gian; đã ghi ở `va-lo-hong-quyen-doc`).
- Xin tham gia (vai trò Xem) — cần bảng yêu cầu, làm sau.
- Nhắc "Đóng hoặc gia hạn" hằng tuần cho nhóm quá hạn — làm sau (job nhỏ).
- App (FCM push chat, màn chat app) — GĐ4. Đợt này KHÔNG bắn FCM cho tin chat.
- Ghim TPE SMART AGENT đầu danh sách — chỉ chừa chỗ "hội thoại hệ thống" trong API/FE (bàn giao §6).
- Đang soạn tin / trạng thái trực tuyến — xem câu hỏi Q4.

## 1. Môi trường (bàn giao §2, §3)

- Nhánh `gop_db-nhom-trao-doi` (cả 2 repo) tách từ `origin/gop_db` (`5d13365e3`), worktree `websites/wt-nhom-trao-doi/{hrm-api,hrm-client}` — **user chốt 11/11**.
- Cổng: API `:8080`, Nuxt `:3080`; socket thử nghiệm (nếu cần chạy riêng) `:8895`. Kiểm `lsof` trước. Kill đúng PID.
- DB `db_gop_6_11` dùng chung với phiên Agent: chỉ chạy migration của chat, lẻ bằng `--path`, hỏi trước.
- Tài liệu ghi về `HRM/.plans/agent-chat/chat/gd1-core-chat/`.

## 2. Dữ liệu (migration `Modules/Assign/Database/Migrations/2026_11_1x_*`)

Mọi model `extends BaseModel`, có `created_by/updated_by` trong `$fillable`.

| Bảng | Cột chính | Index |
|---|---|---|
| `workspaces` | id · `type` tinyint (1 = Nhóm trao đổi; 2/3/4 để dành Dự án KH) · `name` · `company_id` · `has_deadline` · `start_date` · `end_date` nullable · `status` (1 Đang chạy / 2 Đã đóng) · `close_result` (1 Hoàn thành / 2 Dừng) · `close_reason` · `closed_at` · `closed_by` · `enabled_tabs` json · `source_type` / `source_id` nullable (để dành Dự án KH) · timestamps · created_by/updated_by | (company_id), (status), (source_type, source_id) |
| `workspace_members` | id · `workspace_id` · `employee_id` (= `employees.id`, = `auth()->id()`) · `role` (1 Quản lý / 2 Thành viên / 3 Xem) · `added_via` (1 tay / 2 từ phòng ban) · `joined_at` · timestamps · audit | unique (workspace_id, employee_id), (employee_id) |
| `chat_conversations` | id · `type` (`space` / `direct` / `group`) · `workspace_id` nullable (unique khi `space`) · `direct_key` nullable unique (`"{minId}_{maxId}"`) · `name` nullable (cho `group` sau) · `last_message_id` · `last_message_at` · timestamps · audit | unique(workspace_id), unique(direct_key), (last_message_at) |
| `chat_conversation_members` | id · `conversation_id` · `employee_id` · `can_send` bool (Xem / người nghỉ việc = 0) · `last_read_message_id` · `marked_unread` · `pinned_at` · `muted` · `cleared_before_message_id` (xoá lịch sử phía mình) · `left_at` nullable · timestamps | unique(conversation_id, employee_id), (employee_id, left_at) |
| `chat_messages` | id · `conversation_id` · `sender_id` nullable (null = hệ thống) · `type` (`text` / `system` / `card`) · `body` text · `reply_to_id` · `attachable_type` / `attachable_id` (thẻ — đợt sau) · `meta` json (tin hệ thống) · `edited_at` · `recalled_at` · timestamps | (conversation_id, id) |
| `chat_message_mentions` | message_id · employee_id | (employee_id, message_id) |
| `chat_message_reactions` | message_id · employee_id · `emoji` varchar(16) | unique(message_id, employee_id, emoji) |
| `chat_message_pins` | conversation_id · message_id · pinned_by · pinned_at | unique(conversation_id, message_id) |
| File đính kèm | bảng `files` chung, `table = 'chat_messages'`, `table_id = message.id` (CLAUDE.md — không tạo bảng file riêng) | — |

Đếm chưa đọc = số tin `id > last_read_message_id` không phải của mình, tính bằng 1 query gom (`selectRaw` / subquery), không loop.

## 3. Luật nghiệp vụ / quyền (1 nơi: `WorkspaceAccess` + `ConversationAccess`)

- **Không cần mã quyền để tạo nhóm** (spec §3.5). Mọi API đều chỉ dựa vai trò trong nhóm / hội thoại.
- Xem nhóm + chat nhóm: chỉ thành viên (`workspace_members`), vai trò bất kỳ. Người ngoài ⇒ **403** cho mọi API nhóm / tin / file (Review Focus #1).
- Gửi tin / ghim / cảm xúc: Quản lý + Thành viên đang làm việc; Xem chỉ đọc. Nhóm đã đóng ⇒ **423** (middleware `workspaceNotClosed`, khuôn `CheckCustomerNotLocked`); chat 1–1 không bị ảnh hưởng.
- Quản lý: sửa tên / thời hạn, thêm / bớt / đổi vai trò, đóng / mở lại. Không bớt / hạ vai trò Quản lý cuối cùng (422 câu nghiệp vụ).
- Nhóm thuộc 1 công ty = công ty đang chọn lúc tạo; ô chọn người / phòng ban chỉ liệt kê công ty đó (BE kiểm lại khi thêm).
- Lấy từ phòng ban: NV `status = 1` thuộc phòng ban đó **kể cả bộ phận con**, trong công ty nhóm; chọn bộ phận ⇒ chỉ bộ phận đó. Kiêm nhiệm: **kiểm dữ liệu khi code (T1.4)** — chưa xác định bảng.
- Chat 1–1: với mọi NV đang làm việc mọi công ty; hội thoại tạo **khi gửi tin đầu tiên** (`direct_key` chống trùng). Người nghỉ việc ⇒ hội thoại chỉ đọc.
- Sửa / thu hồi: tin của mình, trong 24h (BE kiểm). Thu hồi không xoá cứng, ẩn file kèm.
- Đóng nhóm: chỉ đọc mọi người, tin hệ thống "X đã đóng nhóm · Kết quả", dải trên cùng + nút Mở lại cho Quản lý; mở lại ⇒ tin hệ thống. (Việc dở tự huỷ chưa áp — chưa có việc trong nhóm.)
- Đồng bộ thành viên chat nhóm = thành viên nhóm, ghi đồng thời trong `WorkspaceMemberService` (1 transaction), `can_send = role != Xem`.
- Lịch sử: thêm / bớt / đổi vai trò / đóng / mở / đổi tên ghi theo `entity-history` + tin hệ thống "X đã thêm 12 người từ phòng ban Hành chính".

## 4. Realtime

- Redis kênh có sẵn `user_notification_{employees.id}`, payload thêm `kind: 'chat'`; `server.js` thêm nhánh: `kind === 'chat'` ⇒ `socket.emit('chat', …)`, còn lại giữ `notification` (cùng kiểu nhánh `kind: 'agent'` của phiên Agent ⇒ khi merge chỉ cộng 2 nhánh).
- Sự kiện: `message.created` · `message.updated` (sửa / thu hồi / cảm xúc) · `message.pinned` · `conversation.read` (đã xem) · `conversation.updated` (đổi tên, thành viên, đóng / mở).
- Publish qua job queue theo lô khi hội thoại > 20 người; ≤ 20 publish đồng bộ sau commit (`DB::afterCommit`).
- FE: `utils/chatSocket.js` nghe sự kiện `chat` trên socket sẵn có của `BasicSubsystem.vue` (chỉ thêm 1 dòng `this.socket.on('chat', …)` cạnh dòng `agent` — không viết lại khối socket), phát `$root.$emit('chat-event')`.

## 5. API (`/v1/assign/…`, route file mới `Modules/Assign/Routes/Chat/api.php`)

| Nhóm | Endpoint |
|---|---|
| Nhóm | `GET workspaces` (của tôi, lọc Đang chạy / Lưu trữ) · `POST workspaces` · `GET workspaces/{id}` · `PUT workspaces/{id}` · `POST workspaces/{id}/close` · `POST workspaces/{id}/reopen` |
| Thành viên | `GET workspaces/{id}/members` · `POST workspaces/{id}/members` (employee_ids[]) · `POST workspaces/{id}/members/preview-departments` (department_ids[], part_ids[] ⇒ danh sách sẽ thêm, đánh dấu đã có) · `PUT workspaces/{id}/members/{memberId}` (role) · `DELETE workspaces/{id}/members/{memberId}` |
| Hội thoại | `GET chat/conversations` (cursor theo `last_message_at`, lọc all / unread / group / direct, tìm) · `GET chat/conversations/{id}` · `POST chat/direct/{employeeId}` (tìm hội thoại, chưa có trả `null` + thông tin người) · `PATCH chat/conversations/{id}/me` (pinned / muted / marked_unread / clear history) · `POST chat/conversations/{id}/read` · `GET chat/unread-count` |
| Tin | `GET chat/conversations/{id}/messages?before=&after=&around=` (cursor, 30 tin/lượt) · `POST chat/conversations/{id}/messages` (body, reply_to_id, mentions[], files[]) · `POST chat/direct/{employeeId}/messages` (tin đầu tiên tạo hội thoại) · `PUT chat/messages/{id}` · `POST chat/messages/{id}/recall` · `POST chat/messages/{id}/reactions` (toggle) · `POST/DELETE chat/messages/{id}/pin` · `GET chat/conversations/{id}/pins` · `GET chat/conversations/{id}/search?q=` |
| Danh bạ | `GET chat/directory?q=&company_id=&page=` (NV đang làm việc, label `Tên - Mã phòng - Mã NV`, có `department_code`, `company_name`, phân trang) |

Validate: FormRequest chỉ khai `rules()`. Quyền: middleware `workspaceMember` / `workspaceManager` / `workspaceNotClosed` / `conversationMember`.

## 6. FE (`hrm-client`, màn mới — chỉ `V2Base*`, popup `V2BaseModal`, xác nhận `base-confirm-modal`)

- `pages/assign/messages/index.vue` — màn **Tin nhắn** (mockup 31, 32: `?to=<employeeId>` mở sẵn 1–1).
- `pages/assign/workspaces/index.vue` — danh sách nhóm của tôi (mockup 01, chỉ phần Nhóm trao đổi + Lưu trữ).
- `pages/assign/workspaces/_id/index.vue` — nhóm: đầu nhóm 64px + chat (04, 08); `?panel=members|settings` ⇒ Thành viên (05) / Cấu hình (21: Tên, Thời hạn, Công ty chỉ đọc, Đóng / Mở lại).
- `components/chat/`: `ConversationList.vue` (288 ↔ 68px, khối Đã ghim, chip lọc, ⋯ hội thoại) · `ChatPane.vue` (danh sách tin cuộn ngược, gom cụm theo người, dải ghim, ⋯ → thanh thao tác, trả lời trích dẫn, Đã xem) · `ChatComposer.vue` (ô nhập + @ gợi ý thành viên, đính kèm / kéo thả / dán ảnh qua `V2BaseFile` logic upload sẵn có, Enter gửi / Shift+Enter) · `DirectoryModal.vue` (Danh bạ) · `CreateWorkspaceModal.vue` (11 / 13) · `AddMembersModal.vue` (12: chọn người + lấy từ phòng ban, soát tick) · `CloseWorkspaceModal.vue`.
- `store/chat.js` (Vuex): danh sách hội thoại + tổng chưa đọc, cập nhật theo socket.
- Topbar: icon `fe-message-square` + badge trong `BasicSubsystem.vue` (giữa Phóng to và chọn phân hệ — THÊM cạnh icon Agent, không viết lại `<ul>`). Menu `menu-sidebar.js` thêm dòng "Tin nhắn", "Nhóm trao đổi" (chèn dòng mới). Key Cài đặt phân hệ để ẩn trên prod.
- Rà trước khi dựng (CLAUDE.md "rà project"): avatar, upload file, emoji picker, `employeeOptionText`, khuôn `V2BaseSegmented`. `V2BaseMiniTab` (N2v) chưa cần đợt này.

## 7. Task

### Phase 1 — BE nền nhóm + thành viên
- [x] T1.1 Migration `workspaces`, `workspace_members` + Entity (BaseModel) + hằng số trạng thái / vai trò / `status_text` + `status_color` (9 màu chuẩn).
- [x] T1.2 `WorkspaceAccess` (isMember / role / canManage / canSend) + 4 middleware + đăng ký alias.
- [x] T1.3 `WorkspaceService` + Controller + Request: danh sách của tôi, tạo (người tạo = Quản lý, công ty đang chọn), sửa, đóng / mở lại (+ entity-history).
- [x] T1.4 Khảo sát kiêm nhiệm + cây phòng ban / bộ phận bằng dữ liệu (tinker); `WorkspaceMemberService`: thêm người, preview phòng ban, đổi vai trò, bớt, luật Quản lý cuối.
- [x] T1.5 Job hằng ngày: Quản lý cuối nghỉ việc ⇒ nâng người vào sớm nhất; không còn ai ⇒ Lưu trữ (Kernel: THÊM dòng).
- [x] T1.6 (`Tests/Feature/Workspace/WorkspaceApiTest.php` — **10/10 passed, 65 assertions** 11/11; sau test `workspaces`/`workspace_members` = 0 dòng, NV 13 không đổi) PHPUnit: người ngoài 403 · Xem không gửi · nhóm đóng 423 · lấy phòng ban bỏ trùng, không đổi vai trò · NV chuyển phòng không tự ra · Quản lý cuối.

### Ghi chú Phase 1 (code 11/11, worktree `wt-nhom-trao-doi`, chưa commit)
- Khảo sát T1.4 (DB `db_gop_6_11`): công ty của NV = bảng `company_employees` (nguồn ô chọn công ty, 650 NV đang làm có đủ dòng, 72 dòng kiêm công ty khác) ⇒ "thuộc công ty nhóm" xét bảng này. Bộ phận = bảng `parts` (`employee_infos.part_id`); chọn phòng ban = `employee_infos.department_id` (đã gồm mọi bộ phận bên dưới). `employee_concurrently_departments` **rỗng** ⇒ chưa xét kiêm nhiệm phòng ban. Cây `departments.parent_id` (khối) **không** bung xuống phòng con.
- Công ty nhóm = `auth()->user()->current_company_role` (công ty đang chọn).
- Middleware 1 class `CheckWorkspaceAccess:member|manager[,open]` gắn bằng tên class ở route — KHÔNG thêm alias vào `app/Http/Kernel.php` (file dùng chung).
- Sự kiện `Events/Workspace/WorkspaceActivity` (created / updated / members_added / member_removed / role_changed / closed / reopened / archived_no_active_member) phát trong transaction — Phase 2 nghe để đồng bộ hội thoại + tin hệ thống + báo người được nâng Quản lý (chưa bắn thông báo ở Phase 1).
- Chưa có bảng lịch sử riêng cho nhóm (tin hệ thống trong chat sẽ là nhật ký nhìn thấy) — hỏi user nếu cần popup Lịch sử theo skill entity-history.
- `.env` worktree có `APP_ENV=production` (copy từ checkout chính) ⇒ artisan migrate cần `--force`.

### Phase 2 — BE hội thoại + tin
- [x] T2.1 Migration 6 bảng `chat_*` + Entity.
- [x] T2.2 `ConversationService`: tạo hội thoại `space` khi tạo nhóm, đồng bộ thành viên; `direct` theo `direct_key`; danh sách của tôi (1–2 query, có chưa đọc + tin cuối + người kia).
- [x] T2.3 `MessageService`: gửi (mention, reply, file), sửa / thu hồi 24h, cảm xúc, ghim ≤ 20, đọc, tìm, tin hệ thống (thêm người, đóng / mở, đổi vai trò).
- [x] T2.4 Danh bạ API (mọi công ty, phân trang, `department_code`).
- [x] T2.5 (`ChatApiTest.php` 10 ca + `WorkspaceApiTest.php` 10 ca — **20/20 passed, 166 assertions** 11/11; sau test 8 bảng mới = 0 dòng, `files` không tăng) PHPUnit: 1–1 duy nhất / cặp · thu hồi sau 24h bị chặn · chưa đọc đúng · người ngoài 403 cả tin, file, ghim.

### Ghi chú Phase 2 (code 11/11, chưa commit)
- 1 migration `2026_11_13_000003_create_chat_tables.php` tạo 6 bảng (thay vì 6 file). Cột `emoji` collation `utf8mb4_bin`.
- File đính kèm: FE upload S3 bằng action `uploadImage` có sẵn (như `V2BaseFile`), gửi `files[{url,name,type,size}]`; BE chỉ ghi bảng `files` (`table='chat_messages'`).
- Thành viên chat nhóm đồng bộ TOÀN PHẦN theo `workspace_members` qua listener `Listeners/Chat/SyncWorkspaceChat` (đăng ký trong `AssignServiceProvider::boot`) — bị bớt ⇒ `left_at` ⇒ 403 ngay; vào lại ⇒ đọc từ tin hiện tại. Listener cũng ghi tin hệ thống (tạo nhóm, thêm / bớt, đổi vai trò, tự nâng Quản lý, đổi tên / thời hạn, đóng / mở, tự lưu trữ).
- `Events/Chat/ChatActivity` phát SAU COMMIT (`DB::afterCommit`) cho người còn trong hội thoại — Phase 3 nghe để đẩy socket.
- Danh sách hội thoại: con trỏ `before = "last_message_at|id"`; hội thoại ghim luôn ở trang đầu; lọc `unread` lọc sau phân trang (trang có thể ít hơn limit). Badge = số hội thoại có tin chưa đọc, bỏ hội thoại tắt thông báo + nhóm đã đóng.
- Luật theo tin (của mình, 24h, chưa thu hồi, ≤ 20 ghim, không ghim tin hệ thống) ⇒ 422 `{errors: {message: …}}`.
- Bẫy đã gặp: `files.file_size` NOT NULL (cùng `name`, `file_name`, `file_path`, `table`, `table_id`) ⇒ thiếu size ghi `0`.
- Chưa đọc: tin hệ thống "X đã thêm Y" tính là chưa đọc với Y (cố ý).
- Chưa làm: thông báo (chuông/push) cho người được @ và người được tự nâng Quản lý — để Phase 3 (realtime) / GĐ4 (FCM).

### Phase 3 — Realtime
- [x] T3.1 `ChatSocket::publish` (kind `chat`) + job publish theo lô.
- [x] T3.2 `server.js` nhánh `kind === 'chat'` ⇒ emit `chat`. Thử bằng socket chạy cổng riêng, không tắt socket đang chạy.
- [x] T3.3 Kiểm: tin chat KHÔNG vào `notifications`, không bật chuông / toast (Review Focus #5).

### Ghi chú Phase 3 (code 11/11, chưa commit)
- `Services/Chat/ChatSocket` publish kênh có sẵn `user_notification_{employees.id}` + `kind:'chat'`; listener `Listeners/Chat/PublishChatActivity` (≤ 20 người đẩy ngay, đông hơn chia lô 50 qua job `Jobs/Chat/PublishChatBatch`, queue mặc định). Gói: `{kind, event, conversation_id, data}`; tin nhắn dựng ở góc nhìn trung lập (viewer 0) — FE tự tính `is_mine` / `can_edit` / cảm xúc của mình (`reactions[].employee_ids`).
- `conversation.updated` gửi cả người VỪA bị bớt (để FE gỡ hội thoại ngay) — `syncSpaceMembers($ws, &$removedIds)`.
- `server_node/server.js`: thêm nhánh parse JSON, `kind === 'chat'` ⇒ `socket.emit('chat', parsed)`; còn lại giữ `notification` như cũ. Merge với nhánh Agent (`kind:'agent'`) sẽ đụng đúng khối này — gộp 2 nhánh `if`.
- PHPUnit `ChatRealtimeTest` 3 ca (kênh + kind + không ghi notifications · chia lô 120 người = 3 job · Redis lỗi không vỡ luồng) ⇒ cả bộ **23/23**.
- Kiểm đầu-cuối thật 11/11: API worktree `php -S :8080` + socket `node server_node/server.js` cổng 8895 (`npm install` trong `server_node/` — đã gitignore) + client socket.io 2 (scratchpad) cho NV 13 và 24: cả 2 nhận `chat` (message.created / conversation.updated / conversation.read), **0 sự kiện `notification`**; API chat 0,24–0,29s. Dữ liệu thử (conv 55, 56, nhóm 59) đã xoá; đã tắt 2 tiến trình.

### Phase 4 — FE
- [x] T4.1 Store + `chatSocket` + icon topbar + menu.
- [x] T4.2 `ConversationList` + màn Tin nhắn + Danh bạ + 1–1.
- [x] T4.3 `ChatPane` + `ChatComposer` (đủ tính năng mục 0.3).
- [~] T4.4 Popup tạo nhóm (11/13) + màn nhóm — XONG; **màn danh sách nhóm (mockup 01): user chốt 11/11 "chưa làm màn này"** — cột Hội thoại (lọc Nhóm) là lối vào nhóm; xét lại khi làm GĐ2 (lúc đó đủ cột Việc của tôi / Quá hạn / Dự án KH).
- [x] T4.5 Thành viên (05) + popup thêm (12) + Cấu hình (21) + Đóng / Mở lại.
- [x] T4.6 Playwright MCP đo DOM theo mockup (1366 + 1440): 64px đầu, 288/68px cột, không tràn ngang, 2 tài khoản nhắn qua lại realtime.
- [x] T4.7 E2E `e2e/` (BASE_URL :3080, file auth riêng — KHÔNG chạy project `setup` mặc định): có quyền + không quyền (người ngoài nhóm 403, Xem chỉ đọc).

### Ghi chú Phase 4 (code 11/11, worktree `wt-nhom-trao-doi/hrm-client`, chưa commit)
- File: `store/chat.js` · `utils/chat/{chatApi,chatFormat,workspaceOptions}.js` · `components/chat/{ChatShell,ConversationList,ConversationRow,ChatPane,ChatMessageItem,ChatComposer,ChatAvatar,DirectoryModal}.vue` · `components/chat/workspace/{CreateWorkspaceModal,DepartmentPickModal,AddMembersModal,CloseWorkspaceModal,MembersPanel,SettingsPanel}.vue` · `pages/assign/messages/index.vue` · `pages/assign/workspaces/_id/index.vue` · sửa `components/BasicSubsystem.vue` (THÊM 1 `<li>` icon Tin nhắn + `socket.on('chat')` + style vạch) · `components/menu-sidebar.js` (THÊM mục "Tin nhắn").
- BE bổ sung trong Phase 4 (user chốt "làm đủ"): migration `2026_11_13_000004_add_description_to_workspaces` (ĐÃ CHẠY db_gop_6_11), `manager_ids` lúc tạo, `part_name` ở hồ sơ NV, `conversation_id` ở chi tiết nhóm, gộp tin hệ thống khi sửa nhiều trường.
- **Icon topbar ẩn khi key Cài đặt phân hệ `assign::Tin nhắn` bị tắt** ⇒ deploy prod: tắt key này nếu chưa bàn giao.
- Bẫy gặp + đã sửa: (1) `V2BaseModal` ở `components/modal/` phải import tường minh (auto-import đặt tên `ModalV2BaseModal` ⇒ thẻ trần bày nội dung popup ra trang); (2) app KHÔNG có `$toast` — dùng `$toasted.global.*` (helper `notify`/`notifyError`, bỏ qua mã interceptor axios đã báo: mất mạng/401/403/500/504); (3) `b-form-checkbox` phát `input` khi prop đổi ⇒ ô "chọn tất cả" bỏ tick hết khi bỏ 1 người — setter chỉ xử lý khi khác trạng thái; (4) đổi `:key` ChatPane: pane cũ `beforeDestroy` xoá `activeId` của pane mới; (5) `list_employee_infos` của phân hệ assign lọc bỏ NV phòng cộng tác viên ⇒ ô Quản lý thiếu chính người tạo — `withSelfOption`; (6) theme `body min-height 1550` + `.content-page` đệm 70/5/5 ⇒ khung chat `margin:-10px -10px 0; height: calc(100vh-60px)`, body class `chat-fullheight`; (7) click ⋯ nổi bọt lên `.cp` đóng ngay thanh thao tác.
- Kiểm Playwright MCP (đo DOM) 1440×900 + 1366×768: khung sát topbar/đáy, trang không cuộn/không tràn, đầu khung 64px, cột 288↔68, dải ghim y=124 sát đầu nhóm, menu ⋮ trong khung; realtime 2 chiều qua socket :8895 (không toast); chưa đọc đúng khi hội thoại đang mở / không mở; vai trò Xem chỉ đọc (nút ẩn hẳn); người ngoài 403 + chuyển về Tin nhắn, 1 toast.
- e2e `HRM/e2e/tests/assign/chat-core.spec.ts` **7/7 passed** (token qua env, `--no-deps`, KHÔNG chạy `setup`). PHPUnit 24/24.
- Còn lại / để sau: màn danh sách nhóm 01 (user chốt chưa làm, xét lại ở GĐ2) · tiêu đề tab trình duyệt màn nhóm vẫn "Tân phát_HRM" (PageTitleMixin chỉ đặt tiêu đề topbar — như mọi màn) · ô Danh bạ tìm không phân biệt dấu (collation unicode_ci: "Cần" ra cả "Cẩn") · ảnh đại diện dùng chữ cái đầu (chưa dùng `employee_infos.image`) · đang soạn tin / trực tuyến (Q4 để sau) · upload file chưa thử thật lên S3 (chỉ thử luồng gửi URL qua API).
- Dữ liệu demo giữ lại trong db_gop_6_11: nhóm 93 "[thử] Phòng Hành chính 2027", 94 "[thử] Mua sắm đồng phục 2027", 1–1 với NV 24 (97) và NV 25 (99). Dữ liệu e2e đã xoá.

### Phase 5 — Bàn giao
- [x] T5.1 (11/11 — spec §11, design.md, STATUS) Cập nhật spec (tên bảng thật, API), design.md, STATUS; ghi chỗ nối Agent.

## 8. Quyết định đã chốt (user 11/11/2026)

- Q1. Phạm vi mục 0 — **đồng ý** (việc / thẻ `#` / Dự án KH / Xin tham gia / FCM để đợt sau).
- Q2. Nhánh **`gop_db-nhom-trao-doi`** (cả 2 repo, từ `origin/gop_db`), worktree `websites/wt-nhom-trao-doi/`, API `:8080`, Nuxt `:3080`.
- Q3. Danh sách nhóm của tôi **không lọc theo công ty đang chọn** (có nhãn công ty).
- Q4. Đang soạn tin + trạng thái trực tuyến **để sau**.

## Checkpoint
### Checkpoint — 11/11/2026 tối (wrap up — hết context)
Vừa hoàn thành: core chat Phase 1–5 XONG. Commit + push nhánh `gop_db-nhom-trao-doi`: hrm-api `fd1c2f1e7`, hrm-client `d0644d95d` (origin khớp local). Chưa merge `gop_db`. PHPUnit 24/24, e2e 7/7 (`HRM/e2e/tests/assign/chat-core.spec.ts`, không thuộc git). Màn 01 user chốt chưa làm.
Đang làm dở: — (user đang tự xem demo trên :3080)
Bước tiếp theo:
1. Hỏi user kết quả xem demo → sửa góp ý (nếu có) trên worktree `websites/wt-nhom-trao-doi/` (KHÔNG làm thẳng checkout chính).
2. Merge về `gop_db` CHỈ khi user báo — nhớ gộp tay `server_node/server.js` với nhánh Agent (`kind:'agent'`).
3. Hướng kế: GĐ2 (Nhiệm vụ / Vấn đề trong nhóm, thẻ `#`, tạo việc từ tin, tin hệ thống theo sự kiện việc) hoặc nối TPE SMART AGENT vào danh sách hội thoại — user chọn.
Server demo còn chạy (tắt khi user báo, kill ĐÚNG PID): API :8080 PID 14177 (`php -S` trong `wt-nhom-trao-doi/hrm-api/public`), socket :8895 PID 14178 (`node server_node/server.js`, SOCKET_PORT=8895), Nuxt :3080 PID 14179. Client `.env` worktree: DEV_SERVER_PORT=3080, BASE_API_URL=:8080, SOCKET_URL=http://127.0.0.1:8895. Chạy lại: xem lệnh trong phần "Ghi chú Phase 3/4".
Token thử (JWT local, cấp bằng tinker `JWTAuth::fromUser(TpEmployee::find(id))`): NV 13 Quản lý · NV 24 thành viên · NV 25 ngoài nhóm. Dữ liệu demo: nhóm 93, 94; 1–1 hội thoại 97 (13–24), 99 (13–25).
Blocked: —
