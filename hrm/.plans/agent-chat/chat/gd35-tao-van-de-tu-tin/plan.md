# GĐ35 — Tạo nhanh Vấn đề từ tin nhắn — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trong nhóm chat có nút "Tạo vấn đề" trên tin (web + app); lưu xong có thẻ vấn đề trả lời tin gốc, nhãn mã vấn đề trên tin gốc, dòng "Tạo từ tin nhắn" trong panel, thẻ đổi realtime.

**Architecture:** Tổng quát hoá luồng thẻ chat theo `chat_messages.attachable_type` (`task` | `issue`): BE thêm `issues.source_message_id`, gửi thẻ `issue` khi tạo vấn đề từ tin, dựng thẻ / nhãn / xem trước theo loại, phát `issue.updated`. Web + app chọn khuôn thẻ theo `card.type`, thêm nút tạo vấn đề theo đúng khuôn "Tạo nhiệm vụ".

**Tech Stack:** Laravel 8 (PHP 8.1 local) · Nuxt 2 / Vue 2 · Flutter (fvm) · PHPUnit · Playwright · flutter test.

**Spec:** `HRM/.plans/agent-chat/chat/gd35-tao-van-de-tu-tin/design.md` (duyệt 18/11/2026 — đọc kèm, nhất là §5 và C1–C8).

## Global Constraints

- Repo / nhánh: hrm-api + hrm-client tách nhánh từ `origin/gop_db`; TPE_APP tách từ `origin/develop`. Nhánh, worktree, DB local: HỎI user trước khi code (CLAUDE.md gốc) — chưa có lệnh code.
- Migration chỉ chạy đúng 1 file của GĐ này, chạy lẻ bằng `--path`, sau khi user cho phép.
- `card.type` cho vấn đề = `'issue'` (hằng `ChatMessage::ATTACH_ISSUE`); thẻ nhiệm vụ giữ nguyên `'task'` — KHÔNG đổi dữ liệu/hành vi thẻ nhiệm vụ.
- Chữ: nút "Tạo vấn đề"; xem trước / ghim / sao chép "[Vấn đề <mã>] <lời nhắn>" (mã chỉ khi thẻ chưa xoá); dòng nguồn "Tạo từ tin nhắn của <tên> · dd/mm hh:mm"; mô tả điền sẵn kết bằng "— Từ tin nhắn của <tên> lúc hh:mm dd/mm".
- Lỗi 422 trường `source_message_id` cho vấn đề: "Tin nhắn không tồn tại." · "Tin nhắn không thuộc nhóm trao đổi của vấn đề." · "Không tạo được vấn đề từ tin hệ thống." · "Không tạo được vấn đề từ tin thẻ." · "Tin đã bị thu hồi." · "Bạn không có quyền gửi tin trong nhóm này." · "Nhóm chưa bật tab Vấn đề."
- Không truy vấn trong vòng lặp; thẻ vấn đề + `created_issues` mỗi loại 1 `whereIn` mỗi trang tin.
- Hạn trên thẻ: luật `WorkspaceIssueItemResource` (C6). Trạng thái / màu từ `Issue::STATUS_DATA`, ưu tiên từ `Issue::PRIORITY_DATA`.
- Không commit / push khi user chưa cho (memory: sửa xong để nguyên, user tự báo). Bước "Commit" dưới đây chỉ chạy khi user đã cho commit trên nhánh tính năng.

## Review Focus

1. Tin gốc bị thu hồi SAU khi đã tạo vấn đề ⇒ nhãn `created_issues` rỗng, thẻ vẫn còn (như nhiệm vụ) — Task 2 có ca.
2. Vấn đề bị xoá ⇒ thẻ `deleted: true`, không lộ mã ở thẻ, nhãn, xem trước, push — Task 2 có ca.
3. Tin gốc vừa sinh nhiệm vụ vừa sinh vấn đề ⇒ 2 nhãn cùng hiện, bấm mở đúng panel — Task 5 e2e + Task 7 test.
4. App: task id 5 và issue id 5 cùng trong 1 phòng ⇒ `task.updated` 5 không đè thẻ vấn đề 5 và ngược lại — Task 7 test.
5. Người vai trò Xem / nhóm đã đóng / nhóm tắt tab Vấn đề ⇒ không thấy nút (web + app) và BE 422 nếu gọi thẳng — Task 1 + Task 5 + Task 8.

---

## Phần A — hrm-api

### Task 1: Cột nguồn + kiểm tin gốc + gửi thẻ khi tạo vấn đề

**Files:**
- Create: `Modules/Assign/Database/Migrations/2026_11_25_000001_add_source_message_id_to_issues_table.php`
- Modify: `Modules/Assign/Entities/Issue.php` (fillable + `sourceMessage()` belongsTo `ChatMessage`)
- Modify: `Modules/Assign/Entities/Chat/ChatMessage.php` (`const ATTACH_ISSUE = 'issue'`)
- Modify: `Modules/Assign/Http/Requests/Issue/IssueStoreRequest.php` (`'source_message_id' => 'nullable|integer'`)
- Modify: `Modules/Assign/Services/Chat/MessageService.php` (`taskSource` :159 → hàm chung; `postIssueCard`)
- Modify: `Modules/Assign/Services/IssueService.php::store` (:426)
- Test: `Modules/Assign/Tests/Feature/Workspace/ChatIssueCardTest.php` (mới — khuôn `ChatTaskCardTest.php`)

**Interfaces:**
- Produces: `MessageService::sourceMessage(int $sourceId, ?int $workspaceId, int $actorId, string $kind): ChatMessage` (`$kind` = `'task'|'issue'`; `taskSource()` giữ lại, gọi `sourceMessage(..., 'task')`, câu lỗi task không đổi). Kind `issue` thêm 2 luật: tin `card` ⇒ lỗi; nhóm không bật tab `issues` (`Workspace.enabled_tabs`) ⇒ lỗi.
- Produces: `MessageService::postIssueCard(ChatMessage $source, Issue $issue, int $actorId): ChatMessage` — như `postTaskCard` (:190) nhưng `attachable_type = ATTACH_ISSUE`, body null.
- Produces: cột `issues.source_message_id` (unsignedBigInteger nullable, index `issues_source_message_index`).

- [x] **Step 1: Viết test fail** — `ChatIssueCardTest`:
  - `test_tao_van_de_tu_tin_gui_the_tra_loi_tin_goc`: POST tạo vấn đề `{workspace_id, source_message_id, ...}` ⇒ 200; `issues.source_message_id` = tin gốc; có 1 `chat_messages` type `card`, `attachable_type='issue'`, `attachable_id`=issue, `reply_to_id`=tin gốc, `sender_id`=người tạo.
  - `test_tin_goc_sai_tra_422` (data provider 7 ca: tin không tồn tại, tin nhóm khác, tin hệ thống, tin thẻ, tin thu hồi, người vai trò Xem, nhóm tắt tab Vấn đề) ⇒ 422 lỗi ở `source_message_id` đúng câu Global Constraints; KHÔNG có dòng `issues` mới và KHÔNG có thông báo mới (đếm `notifications` trước/sau).
  - `test_khong_co_source_message_id_chay_nhu_cu`: tạo vấn đề có `workspace_id`, không `source_message_id` ⇒ không có tin thẻ.
  - `test_task_source_giu_cau_loi_cu`: tạo nhiệm vụ từ tin hệ thống vẫn ra "Không tạo được nhiệm vụ từ tin hệ thống.".
- [x] **Step 2: Chạy, xác nhận fail** — `php -d memory_limit=2G vendor/bin/phpunit Modules/Assign/Tests/Feature/Workspace/ChatIssueCardTest.php` ⇒ FAIL (cột / hằng chưa có).
- [x] **Step 3: Code** — migration + entity + request + `sourceMessage` + `postIssueCard`. `IssueService::store` theo C7: kiểm tin gốc TRƯỚC mọi ghi (lỗi gộp cùng lỗi validate khác nếu có, như `TaskService` :407–416); `DB::transaction` chỉ bọc `Issue::create` + gán `source_message_id` + `postIssueCard`; `notifyHandlingDepartmentLead` / `notifyAssigned` để nguyên SAU transaction. Chạy migration (chỉ khi user đã cho): `php artisan migrate --path=Modules/Assign/Database/Migrations/2026_11_25_000001_add_source_message_id_to_issues_table.php`.
- [x] **Step 4: Chạy lại** — test trên PASS; thêm `vendor/bin/phpunit Modules/Assign/Tests/Feature/Issue` + `ChatTaskCardTest` + `WorkspaceTaskTest` PASS.
- [x] **Step 5: Commit** `feat(chat): tạo vấn đề từ tin nhắn — cột nguồn + thẻ trả lời tin gốc`

### Task 2: Dựng thẻ vấn đề, nhãn `created_issues`, xem trước / push theo loại

**Files:**
- Modify: `Modules/Assign/Services/Chat/ChatPresenter.php` (:44–60 nạp thẻ, :78–83 nhãn, :174 `card`, :288 `preview`, :324 `cardCodes`)
- Modify: `Modules/Assign/Transformers/IssueResource/DetailIssueResource.php` (`source_message_id`, `source_message`)
- Modify: `Modules/Assign/Services/IssueService.php` (chỗ nạp chi tiết vấn đề: `->load('sourceMessage.conversation')`)
- Test: `ChatIssueCardTest.php` (thêm ca)

**Interfaces:**
- Consumes: Task 1 (`ATTACH_ISSUE`, cột nguồn, `Issue::sourceMessage`).
- Produces: `ChatPresenter::issueCardFor(Issue $i): array` — khoá: `type`('issue'), `id`, `code`(=`issue_code`), `title`, `status_text`, `status_color`, `assignee{id,name}|null`, `priority`, `priority_text`, `priority_color`, `due_date`, `due_time`, `is_overdue`, `due_state_text`, `due_state_color`, `deleted`(bool), `moved`(luôn false), `progress_pct`(luôn null). Vấn đề xoá ⇒ chỉ `type`, `id`, `deleted:true`, còn lại null/false.
- Produces: mỗi tin trả `created_issues: [{id, code}]` (tin thu hồi ⇒ `[]`).
- Produces: `DetailIssueResource` trả `source_message_id`, `source_message{id, workspace_id, conversation_id, sender_name, created_at, can_open}` — chép đúng luật `DetailTaskResource::sourceMessagePayload` (:182), tách helper dùng chung nếu gọn.

- [x] **Step 1: Test fail** — `test_the_van_de_trong_danh_sach_tin` (GET tin: `card.type='issue'`, `code`, `status_text`='Mới ghi nhận', `due_state_text` khớp `WorkspaceIssueItemResource` cùng vấn đề) · `test_the_van_de_da_xoa_khong_lo_ma` (card.deleted true, code null; preview hội thoại "[Vấn đề] …" không mã) · `test_nhan_created_issues_va_tin_thu_hoi` · `test_preview_va_push_ghi_van_de` (`ChatPresenter::preview` ⇒ "[Vấn đề VD-…] "; `PushChatMessage` :127 dùng cùng preview) · `test_chi_tiet_van_de_co_dong_nguon` (thành viên ⇒ can_open true + sender_name; người ngoài nhóm ⇒ can_open false, sender_name null) · `test_so_truy_van_khong_tang_theo_so_the` (10 thẻ vấn đề vs 1 thẻ: số query bằng nhau, `DB::enableQueryLog`).
- [x] **Step 2: Chạy, fail.**
- [x] **Step 3: Code** — `cardCodes` trả mã cho cả 2 loại (issue: không xét `moved`); `preview` chữ "[Nhiệm vụ" / "[Vấn đề" theo `attachable_type`.
- [x] **Step 4: Chạy** `ChatIssueCardTest` + `ChatTaskCardTest` + `ChatApiTest` + `ChatPushStickerTest` PASS.
- [x] **Step 5: Commit** `feat(chat): thẻ vấn đề + nhãn created_issues + xem trước theo loại thẻ`

### Task 3: Realtime `issue.updated` (sửa vấn đề + đóng nhóm)

**Files:**
- Create: `Modules/Assign/Services/Chat/IssueChatSync.php` (khuôn `TaskChatSync.php`)
- Modify: `Modules/Assign/Entities/Issue.php` (`booted()` → `static::updated` gọi `IssueChatSync::changed`)
- Modify: `WorkspaceIssueCanceller` (:57, sau `update`) gọi `IssueChatSync::flushMany(array $ids)`
- Test: `Modules/Assign/Tests/Feature/Workspace/IssueChatRealtimeTest.php` (khuôn `TaskChatRealtimeTest.php`)

**Interfaces:**
- Consumes: `ChatPresenter::issueCardFor` (Task 2).
- Produces: `IssueChatSync::FIELDS = ['status','title','assignee_id','due_date','due_time','priority']`; `changed(Issue)`, `flush(int)`, `flushMany(int[] $ids)`. Gói socket `issue.updated` `{issue_id, card}` vào hội thoại `space` của `issues.workspace_id`, người nhận = thành viên chưa rời. Chỉ khi `workspace_id` khác null. Nuốt lỗi + `Log::warning('[Chat] không phát được issue.updated: …')`.

- [x] **Step 1: Test fail** — `test_doi_trang_thai_phat_issue_updated` (Event::fake ChatActivity; đổi status ⇒ 1 lần, card.status_text mới) · `test_doi_truong_khac_khong_phat` (đổi `description`) · `test_van_de_khong_thuoc_nhom_khong_phat` · `test_dong_nhom_phat_cho_van_de_bi_huy` (đóng nhóm có 2 vấn đề mở ⇒ 2 sự kiện, card.status_text 'Đã đóng') · `test_rollback_khong_phat` (sửa trong transaction rồi rollback ⇒ 0).
- [x] **Step 2: Chạy, fail.** **Step 3: Code.** **Step 4:** test trên + `WorkspaceIssueListTest` + `Modules/Assign/Tests/Feature/Issue` PASS.
- [x] **Step 5: Commit** `feat(chat): phát issue.updated để thẻ vấn đề tự đổi`

## Phần B — hrm-client

### Task 4: Thẻ vấn đề + nhãn + chữ theo loại thẻ + nghe `issue.updated`

**Files:**
- Create: `components/chat/IssueCard.vue` (cùng khuôn `components/chat/TaskCard.vue`: mã · tên · `V2BaseBadge :color="card.status_color"` · người phụ trách · hạn `due_state_*` · ưu tiên; `deleted` ⇒ "Vấn đề đã bị xoá")
- Modify: `components/chat/ChatMessageItem.vue` (:110 chọn `TaskCard`/`IssueCard` theo `m.card.type`; :420 thêm `createdIssues`; nhãn issue cạnh nhãn 📋; emit `open-issue(id)`)
- Modify: `utils/chat/chatFormat.js` (:148–150), `utils/chat/chatDrafts.js` (:76) — chữ theo `card.type`
- Modify: `components/chat/ChatPane.vue` — gắn `<IssuePanel ref="issuePanel">` cạnh `TaskPanel` (:176); `openIssue(id)`; :718 thêm `issue.updated` ⇒ `onIssueUpdated` (thay card khớp `card.type==='issue' && id`); `onTaskUpdated` (:801) chỉ thay thẻ `card.type==='task'`
- Modify: `components/chat/workspace/WorkspaceView.vue` (:379 — tab Vấn đề đang mở nghe `issue.updated` / tin thẻ issue ⇒ nạp lại gom 800ms)
- Test: unit nếu có cho `chatFormat` (`utils/chat/__tests__` — nếu thư mục không có thì kiểm ở Task 5 e2e)

**Interfaces:**
- Consumes: payload Task 2/3.
- Produces: `ChatPane.openIssue(id: number)`; sự kiện `open-issue` từ `ChatMessageItem`.

- [x] **Step 1:** Tái hiện trước trên :3080 (Playwright MCP): tạo thẻ issue bằng API (Task 1) ⇒ web hiện SAI thành thẻ nhiệm vụ — chụp số đo / text DOM làm mốc.
- [x] **Step 2: Code.**
- [x] **Step 3: Đo lại** bằng Playwright: thẻ có `data-testid="chat-issue-card"`, text mã + trạng thái đúng; bấm ⇒ IssuePanel mở đúng id; đổi trạng thái vấn đề ở tab khác ⇒ thẻ đổi không tải lại trang.
- [x] **Step 4: Commit** `feat(chat): thẻ vấn đề trong chat + nhãn + realtime`

### Task 5: Nút "Tạo vấn đề" từ tin + dòng nguồn trong IssuePanel

**Files:**
- Modify: `components/chat/ChatMessageItem.vue` (:210 — thêm nút cạnh "Tạo nhiệm vụ", prop `canCreateIssue`, emit `create-issue`, `data-testid="msg-create-issue"`)
- Modify: `components/chat/ChatPane.vue` (prop `issuesWorkspaceId`; computed `issueTools` = `issuesWorkspaceId && detail.type==='space' && detail.can_send`; `createIssueFrom(m)` khuôn `createTaskFrom` :828 — tách phần dựng tên/mô tả thành hàm dùng chung `messagePrefill(m)` trong `utils/chat/chatFormat.js`)
- Modify: `components/chat/workspace/WorkspaceView.vue` (:114 truyền `:issues-workspace-id="issuesEnabled ? workspace.id : null"` + thông tin GP của nhóm như `IssueGroupListView` :259–269)
- Modify: `components/assign/issue/panel/IssuePanel.vue` + form tạo (gửi `source_message_id` khi `defaults.source_message_id`; dòng nguồn + `jumpToSource` chép khuôn `TaskPanel.vue` :86, :223, :417)
- Test: `HRM/e2e/tests/assign/workspace-issues.spec.ts` (thêm ca)

**Interfaces:**
- Consumes: `IssuePanel.create(defaults)` có sẵn; `messagePrefill(m): {title, description}` (mới, dùng cho cả task lẫn issue — `createTaskFrom` đổi sang gọi hàm này, kết quả không đổi).

- [x] **Step 1: e2e fail** — ca: thành viên bấm `msg-create-issue` ⇒ panel mở, Nhóm khoá, Tên/Mô tả đúng; lưu ⇒ thẻ `chat-issue-card` trả lời tin gốc + nhãn mã dưới tin gốc; panel vấn đề có dòng "Tạo từ tin nhắn của" bấm nhảy về tin · người vai trò Xem: không có nút (đếm = 0) · nhóm tắt tab Vấn đề: không có nút · tin vừa có nhiệm vụ vừa có vấn đề: 2 nhãn, bấm từng nhãn mở đúng panel.
- [x] **Step 2: Code.** **Step 3:** chạy cả bộ `workspace-issues`, `workspace-tasks`, `chat-core`, `chat-drawer`, `issue-panel-v2`, `task-panel-v2` (đọc dòng tổng kết — serial "did not run" ≠ passed).
- [x] **Step 4: Commit** `feat(chat): tạo vấn đề từ tin nhắn trên web`

## Phần C — TPE_APP

### Task 6: Model + hub hiểu thẻ vấn đề

**Files:**
- Modify: `app/lib/ui/chat/model/chat_models.dart` (`ChatCard` thêm `bool get isIssue => type == 'issue'`, `isTask`, `dueTime`, `dueStateText`, `dueStateColor`; `ChatMessage` thêm `createdIssues`)
- Modify: `app/lib/ui/chat/hub/chat_event.dart` (:79 thêm `issue.updated` ⇒ `IssueUpdated{conversationId, issueId, card}`)
- Modify: `app/lib/ui/chat/room/chat_room_bloc.dart` (:1307 cập nhật thẻ khớp `type` + `id`; xử lý `IssueUpdated`)
- Modify: chữ theo loại: `chat_list_bloc.dart` :426, `chat_banner_overlay.dart` :116, `pin_bar.dart` :24, `message_actions_sheet.dart` :101
- Test: `app/test/ui/chat/chat_models_test.dart`, `chat_event_test.dart`, `chat_room_bloc_test.dart`, `chat_list_bloc_test.dart`

- [x] **Step 1: Test fail** — parse card issue · `created_issues` · `issue.updated` ra `IssueUpdated` · task 5 và issue 5 cùng phòng: `TaskUpdated(5)` chỉ đổi thẻ task, `IssueUpdated(5)` chỉ đổi thẻ issue · chữ xem trước "[Vấn đề VD-1] …".
- [x] **Step 2:** `cd app && fvm flutter test test/ui/chat` fail. **Step 3: Code.** **Step 4:** PASS.
- [x] **Step 5: Commit** `feat(chat): app hiểu thẻ vấn đề`

### Task 7: Bong bóng thẻ vấn đề + nhãn + loại thẻ lạ

**Files:**
- Modify: `app/lib/ui/chat/widget/message_bubble.dart` (:254 — `isIssue` ⇒ widget thẻ vấn đề mới cùng file khuôn thẻ task, bấm mở `WorkIssueDetailPage`; loại khác `task`/`issue` ⇒ thẻ trung tính không bấm (C4); nhãn `createdIssues` cạnh nhãn task)
- Test: `app/test/ui/chat/chat_room_widgets_test.dart`

- [x] **Step 1: Test fail** (widget: thẻ issue hiện mã + trạng thái, bấm gọi điều hướng chi tiết vấn đề; card type 'xyz' không có `onTap`; tin có cả 2 nhãn). **Step 2–4:** fail → code → PASS.
- [x] **Step 5: Commit** `feat(chat): app vẽ thẻ vấn đề + nhãn trên tin gốc`

### Task 8: "Tạo vấn đề" trong menu nhấn giữ

**Files:**
- Modify: `app/lib/ui/chat/room/widget/message_actions_sheet.dart` (:57 thêm `MessageAction.createIssue` khi `c.isSpace && issuesEnabled && canSend && live && !m.isCard`; :126 nhãn "Tạo vấn đề" + icon)
- Modify: `app/lib/ui/chat/room/chat_room_page.dart` (:906 truyền `issuesEnabled: enabledTabs.contains('issues') && canCreateTask`; :933 xử lý ⇒ mở `WorkIssueFormPage(prefill: …)`)
- Modify: `app/lib/ui/work/issue/work_issue_form_page.dart` (`WorkIssuePrefill` thêm `title`, `description`, `source`; gửi `source_message_id` 1 lần — cờ `_sourceSent` như `work_task_form_page.dart` :191)
- Test: `app/test/ui/chat/chat_room_page_actions_test.dart`, test form vấn đề

- [x] **Step 1: Test fail** — có/không `createIssue` theo 5 điều kiện (không phải nhóm, tab tắt, vai trò Xem, tin thu hồi, tin thẻ) · prefill điền tên/mô tả + body gửi `source_message_id`.
- [x] **Step 2–4:** fail → code → PASS; `fvm flutter test` toàn app + `fvm flutter analyze lib/ui/chat lib/ui/work` 0 lỗi mới.
- [x] **Step 5:** chạy máy ảo tpeLocal (Mobile MCP): nhấn giữ tin ⇒ Tạo vấn đề ⇒ lưu ⇒ thẻ vấn đề hiện trong phòng, bấm mở chi tiết.
- [x] **Step 6: Commit** `feat(chat): app tạo vấn đề từ tin nhắn`

## Phần D — Kiểm cuối

- [x] PHPUnit `Modules/Assign/Tests/Feature/Workspace` + `Issue` + `Task` (`-d memory_limit=2G`) PASS.
- [x] Bộ e2e Task 5 chạy lại toàn bộ, đọc dòng tổng kết.
- [x] Cập nhật checkpoint cuối file này + README §3 + memory `agent-chat-trang-thai`.

### Checkpoint — 18/11/2026
Vừa hoàn thành: design duyệt + plan viết xong.
Đang làm dở: —
Bước tiếp theo: user soát plan, chọn cách chạy; hỏi riêng phạm vi code (nhánh/worktree 3 repo, migration 2026_11_25_000001 vào DB local nào).
Blocked: chưa có lệnh code.

### Checkpoint — 18/11/2026 (code xong, CHƯA push)
Vừa hoàn thành: 8 task + soát từng task + soát toàn nhánh (opus) + 1 lượt sửa (F1 ẩn "Tạo vấn đề" trên tin thẻ, F2 thẻ loại lạ trung tính trên web, F3 vùng bấm nhãn app). Commit:
- hrm-api `gop_db-chat-tao-van-de-tu-tin` (wt-nhom-trao-doi): ef137add9 · 91bbd35c5 · f20b8f47e (base ffa4742cd). Migration 2026_11_25_000001 ĐÃ chạy db_gop_6_11 (--path --force, APP_ENV local=production).
- hrm-client cùng tên nhánh: be40b338c · fafbcae9f · f5507eff1 (base d1e0979c7).
- TPE_APP `feature/chat-tao-van-de-tu-tin` (wt-tpe-app-chat): aee4f59 · 3dfc38f · 81dd147 · 27b7d51 (base origin/develop c0a7f6b).
- e2e `HRM/e2e/tests/assign/workspace-issues.spec.ts` (ngoài git): thêm ca 6a–6d + hover tin thẻ = 0 nút.
Kiểm: PHPUnit Workspace 313 · Issue 67 · Task 34 OK; e2e workspace-issues 12 · chat-core 8 · chat-drawer 10 · issue-panel-v2 11 · task-panel-v2 8 · workspace-tasks 12 (lần 1 có 1 ca chờ hết giờ, chạy lại xanh); flutter test 623 OK, analyze 0.
Đang làm dở: —
Bước tiếp theo: (1) chạy thử app trên máy ảo tpeLocal trỏ :8080 (`--dart-define=APP_API_BASE_URL=http://127.0.0.1:8080/api/`) — đo vùng bấm nhãn ≥36px (ước tính ~35px theme thật useMaterial3:false; sửa 1 dòng ConstrainedBox minHeight 36 nếu thiếu) + luồng nhấn giữ → Tạo vấn đề → thẻ → chi tiết; (2) user báo push / merge gop_db + develop; deploy thứ tự api → client → app (migration chỉ thêm cột + index; tab trình duyệt cũ chưa tải lại sẽ vẽ thẻ vấn đề thành thẻ nhiệm vụ tới khi F5).
Ngoài luồng ghi lại: TaskChatSync/IssueChatSync `$pending` kẹt sau rollback (worker sống lâu mất 1 lần phát); xoá vấn đề/nhiệm vụ không phát realtime (thẻ cũ tới khi tải lại); ~59 nhóm "[e2e]" tồn từ trước; chưa có e2e nhóm GP cho "Tạo vấn đề".
Blocked: —

### Checkpoint — 18/11/2026 17:30 (chạy thử máy ảo)
Vừa hoàn thành: máy ảo iPhone 18 Pro, tpeLocal trỏ :8080 — menu nhấn giữ có "Tạo vấn đề", form điền sẵn đúng, thẻ vấn đề hiện realtime, nhãn căn phải, dòng xem trước "[Vấn đề ISS-…]", bấm nhãn/thẻ mở đúng chi tiết. Vùng bấm nhãn đo ~33px ⇒ sửa đệm 10 + test dùng theme thật: app `9b964e4`; đo lại chạm ±18px quanh tâm đều mở ⇒ ≥36px.
Phát hiện thêm (chưa sửa): thẻ vấn đề trên app — chip trạng thái bị cắt "Đã …" khi đứng cạnh nhãn ưu tiên.
Dữ liệu thử: nhóm "[e2e] GĐ35 máy ảo" (ws 17769, conv 14058), vấn đề 7157 tạo qua API (lưu form trên máy ảo khó thao tác do cuộn trôi — chưa bấm Lưu thật trên app).
Bước tiếp theo: user chọn sửa chip trạng thái; user báo push / merge.

### Checkpoint — 18/11/2026 17:40 (sửa chip trạng thái)
Vừa hoàn thành: thẻ vấn đề app — hàng 1 bỏ mã (như TaskCard, góp ý 17/11) + spaceBetween thay Spacer (Spacer + Flexible chia đôi chỗ ⇒ chip bị cắt). Test khổ 402px theme thật (đỏ trước, xanh sau); test chat 369 OK; analyze 0; máy ảo hiện đủ "Đã phân công" · "Cao". App `7ccd000`.
Ngoài luồng (đã sửa sau, user chọn 1): TaskCard cùng mẫu Spacer + Flexible.
Bước tiếp theo: user báo push / merge (api + client → gop_db, app → develop); deploy api → client → app.

### Checkpoint — 18/11/2026 17:50 (sửa thẻ nhiệm vụ app)
Vừa hoàn thành: TaskCard 2 hàng (trạng thái · ưu tiên; hạn · %) dùng spaceBetween, không hạn thì % vẫn bên phải. Test khổ 402px (font test mỗi ký tự = cỡ chữ ⇒ chọn chuỗi vừa đủ phân biệt): đỏ trên code cũ, xanh code mới. flutter test 625 OK, analyze lib/ui/chat 0. Máy ảo xem thẻ TPE.TASK.NB.26.0047 đúng. App `6f54884`.
Bước tiếp theo: user báo push / merge.

### Checkpoint — 18/11/2026 18:00 (chip lọc panel trái — user yêu cầu, đi cùng nhánh GĐ35)
Vừa hoàn thành: `ChatFilterChips.vue` chữ 11px · icon 11.5px · cao 26px · đệm 10px · khoảng chip 3px · viên số 9.5px. Đo Playwright :3080: cách viền 8.8–9.1px (trước ~6px), có số ~7px, không cắt, không tràn. Client `017f7af5a`.
Bước tiếp theo: user xem :3080; user báo push / merge.

### Checkpoint — 18/11/2026 18:30 (ĐÃ MERGE, CHƯA DEPLOY)
Vừa hoàn thành: merge origin vào 3 nhánh (không xung đột) ⇒ push nhánh + fast-forward: hrm-api gop_db `e395dc12d` · hrm-client gop_db `623f7ece8` · TPE_APP develop `98ec972`. Test trên bản merge: e2e workspace-issues 12/12; PHPUnit Issue 67 · Task 34 OK, Workspace 316 có 1 đỏ `WorkspaceTaskListTest::test_start_approval_matches_detail_when_assignee_company_inactive` — do commit đồng nghiệp `6e3f146af` (Thu hồi về Nháp, status 1) chưa cập nhật test, KHÔNG do GĐ35 (GĐ35 không đụng Task.php/TaskService) ⇒ ngoài luồng; flutter test 625 OK, analyze 0.
Bước tiếp theo: deploy TPE khi user báo — thứ tự api (migration 2026_11_25_000001 chỉ thêm cột + index) → client → app (chưa phát hành store). Lưu ý: gop_db nay mang cả commit người khác (Thu hồi/Hủy nhiệm vụ, push chat song song, agent thống kê nghỉ, seeder DisablePriceNotificationForEmployeesSeeder) ⇒ kiểm khi deploy.
Ngoài luồng: test WorkspaceTaskListTest đỏ (người làm Thu hồi/Hủy); TaskChatSync/IssueChatSync $pending sau rollback; xoá vấn đề/nhiệm vụ không phát realtime; ~59 nhóm "[e2e]" tồn; chưa e2e nhóm GP cho Tạo vấn đề.
