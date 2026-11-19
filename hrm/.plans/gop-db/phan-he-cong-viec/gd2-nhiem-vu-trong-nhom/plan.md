# GĐ2 — Nhiệm vụ trong Nhóm trao đổi + nối chat (web) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **Trạng thái: CODE XONG 12/11/2026 (Task 1–11 `[x]`), chưa merge, chưa push.** Nhánh `gop_db-nhom-trao-doi` (worktree `websites/wt-nhom-trao-doi/`).
> Phụ trách: @namdangit

**Goal:** Thành viên Nhóm trao đổi tạo / giao / theo dõi Nhiệm vụ ngay trong nhóm (tab Nhiệm vụ theo mockup 03, từ 1 tin nhắn, thẻ `#` trong chat), người ngoài nhóm không đọc được gì của nhóm kể cả qua API Task.

**Architecture:** `tasks` thêm `workspace_id` + `source_message_id`. Một lớp quyền `TaskAccess` (xem = đúng query danh sách hiện có + thành viên nhóm) chặn mọi route `/assign/tasks/{task}`. Luật gắn nhóm nằm ở `WorkspaceTaskRules` gọi từ `TaskService`. Chat thêm tin `card` (`attachable_type='task'`) hydrate trạng thái lúc đọc. FE: `V2BaseMiniTab` đầu nhóm, component danh sách gom nhóm mới `components/assign/task/group-list/`, ô Nhóm trong `TaskForm`, `#` + "Tạo nhiệm vụ" trong chat.

**Tech Stack:** Laravel 8 / PHP 7.4 (`Modules/Assign`), PHPUnit Feature test; Nuxt 2 / Vue 2 (`V2Base*`); Playwright (e2e Node 20).

**Spec:** `docs/superpowers/specs/gop-db/2026-11-11-gd2-nhiem-vu-trong-nhom-design.md` (đọc kèm spec gốc `2026-11-02-phan-he-cong-viec-design.md` §3.11, §3.12, §5.1) · tóm tắt `design.md` cùng folder · mockup `../gd0-mockup/screens/03-phong-nhiem-vu.html`, `21-phong-cau-hinh.html`, `04-phong-trao-doi.html`.

## Global Constraints
- Code ở worktree `websites/wt-nhom-trao-doi/{hrm-api,hrm-client}`, nhánh `gop_db-nhom-trao-doi` (hoặc nhánh con — hỏi khi bắt đầu). API `:8080`, Nuxt `:3080`, socket `:8895`. Kill đúng PID.
- DB `db_gop_6_11` dùng chung: migration chạy lẻ `--path`, `--force` (`.env` worktree `APP_ENV=production`), hỏi trước.
- Model mới `extends BaseModel`; `auth()->id()` = `employees.id`. Không dùng `mysql2`.
- Không sửa `app/Http/Kernel.php` (middleware gắn bằng tên class như core chat).
- FormRequest chỉ `rules()`; câu nghiệp vụ trả `errors.<field>` (422). Nhóm đóng ⇒ 423.
- FE màn mới: chỉ `V2Base*`, popup `V2BaseModal` (import tường minh từ `components/modal/`), xác nhận `$confirm`, badge `status_text`+`status_color` do BE trả, nút không dùng được thì ẩn, cụm nút `mr-2 mb-2`, toast `$toasted.global.*`, xám `#6b7280` (không `.text-muted`), số `toLocaleString('en-US')`.
- Sửa component dùng chung (`V2BaseMiniTab` mới, `TaskForm.vue`, `TaskPanel.vue`, `ChatComposer.vue`) — hỏi trước khi đụng (HRM/CLAUDE.md).
- Vấn đề (Issue), tin tự báo, tab Meeting / File: KHÔNG làm đợt này.

## Review Focus
1. **Người đang thấy việc ở danh sách Nhiệm vụ chung mở chi tiết bị 403 sau khi siết `show`** → không được xảy ra; test `test_every_listed_task_is_showable` (Task 2) duyệt mọi NV có việc trên DB thử.
2. **Thẻ `#` của việc đã xoá / việc vừa chuyển sang nhóm khác** → thẻ hiện "Nhiệm vụ đã bị xoá" / vẫn mở được nếu còn quyền xem; test `test_card_of_deleted_task_renders_placeholder` (Task 6).
3. **Tạo từ tin đã bị thu hồi / tin hệ thống / tin của hội thoại 1–1** → 422, không tạo việc; test `test_create_from_recalled_or_system_message_rejected` (Task 6).
4. **Đổi nhóm của việc nhiều người làm khi 1 trong các người làm không thuộc nhóm mới** → 422, cả lô không đổi; test `test_change_workspace_batch_all_or_nothing` (Task 3).
5. **Tắt tab Nhiệm vụ rồi gửi `#` / tạo từ tin / gắn qua form bằng API trực tiếp** → 422; test `test_disabled_tasks_tab_blocks_all_entry_points` (Task 3 + Task 6).

---

## Phase 1 — BE

### Task 1: Migration `tasks.workspace_id`, `tasks.source_message_id`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_14_000001_add_workspace_to_tasks.php`
- Modify: `hrm-api/Modules/Assign/Entities/Task/Task.php` (`$fillable` + `workspace()` belongsTo `Workspace`)

**Interfaces:**
- Produces: cột `tasks.workspace_id` (unsignedBigInteger nullable, index `(workspace_id, status)`), `tasks.source_message_id` (unsignedBigInteger nullable, index); `Task::workspace()`.

- [x] Step 1: Viết migration (có `down()` drop index + cột). `migrate --pretend --path=...` xem SQL.
- [x] Step 2: **Hỏi user** rồi chạy đúng file này vào `db_gop_6_11` (`--path`, `--force`). Kiểm `SHOW INDEX FROM tasks`.
- [x] Step 3: Commit.

### Task 2: `TaskAccess` + bịt lỗ hổng mọi route `/assign/tasks/{task}`

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Task/TaskAccess.php`
- Modify: `hrm-api/Modules/Assign/Services/TaskService.php:190` (tách điều kiện của `applyPermissionScope` + lọc Nháp `:33-42` thành `public function visibleQuery(): Builder` dùng lại — KHÔNG đổi kết quả danh sách)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/TaskController.php` (`show`, `update`, `updateField`, `watch`, `requestExtension`, `destroy`, `updateStatus`) + `TaskCommentController` (index/store/…) + 3 action extension (`approve/reject/cancel` kiểm qua `$extension->task`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/TaskAccessTest.php`

**Interfaces:**
- Consumes: `WorkspaceAccess::roleOf(int $workspaceId, ?int $employeeId): ?int`, `Workspace::STATUS_CLOSED`.
- Produces: `TaskAccess::canView(Task $task, int $employeeId): bool` · `TaskAccess::assertView(Task $task): void` (abort 403 "Bạn không có quyền xem nhiệm vụ này.") · `TaskAccess::assertWritable(Task $task): void` (assertView + nhóm đã đóng ⇒ abort 423 "Nhóm đã đóng, chỉ xem."). Luật thao tác giữ nguyên code hiện có (Q7).

- [x] Step 1: Test lỗi trước:
  - `test_outsider_gets_403_on_workspace_task` — NV 25 ngoài nhóm, `GET /api/v1/assign/tasks/{id}` ⇒ 403; cả `comments`, `field`, `watch`.
  - `test_member_with_role_view_can_show_but_not_needed_role` — thành viên vai trò Xem ⇒ 200.
  - `test_every_listed_task_is_showable` — với mỗi NV có việc trong DB thử (giới hạn 30 NV), mọi id trả về ở `GET /assign/tasks` đều `show` 200 (chứng minh không ai mất quyền).
  - `test_closed_workspace_task_write_is_423` — `PATCH field` việc của nhóm đóng ⇒ 423, `GET` ⇒ 200.
- [x] Step 2: Chạy `php artisan test Modules/Assign/Tests/Feature/Workspace/TaskAccessTest.php` ⇒ FAIL (show trả 200 cho người ngoài).
- [x] Step 3: `TaskService::visibleQuery()` (scope cũ) ; `TaskAccess::canView` = `visibleQuery()->whereKey($task->id)->exists()` HOẶC (`workspace_id` && `roleOf` != null). Gọi `assertView` / `assertWritable` ở đầu từng action.
- [x] Step 4: Chạy test mới + `WorkspaceApiTest`, `ChatApiTest`, `ChatRealtimeTest` ⇒ PASS.
- [x] Step 5: Đối chiếu dữ liệu: tinker đếm `visibleQuery` trước / sau tách hàm cho 5 NV (khác quyền) phải bằng nhau — ghi số vào Ghi chú.
- [x] Step 6: Commit.

### Task 3: Gắn nhiệm vụ vào nhóm (tạo / sửa / con / lô / rời Nháp / tab tắt)

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Workspace/WorkspaceTaskRules.php`
- Modify: `TaskService::store` (`:363`), `TaskService::update` (`:474`), xử lý `updateField` (trường `workspace_id`), `createChildrenAsTasks` (`:1034-1069`), chỗ rời Nháp; `Http/Requests/Task/TaskStoreRequest.php`, `TaskUpdateRequest.php`, `TaskFieldUpdateRequest.php` (rules `workspace_id` nullable integer, `source_message_id` nullable integer)
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/WorkspaceTaskTest.php`

**Interfaces:**
- Produces: `WorkspaceTaskRules::validateAttach(?int $workspaceId, array $assigneeIds, int $actorId, ?int $solutionId, ?int $projectId): void` — ném `ValidationException` với khoá `workspace_id` (không phải Quản lý/Thành viên · nhóm không bật `'tasks'` trong `enabled_tabs` · đang có Giải pháp/Dự án: "Nhiệm vụ đã gắn Giải pháp / Dự án, không gắn nhóm được.") hoặc `assignee_id` / `children.N.assignee_id` ("X không phải thành viên nhóm (hoặc chỉ có quyền Xem)."); nhóm đóng ⇒ abort 423. `WorkspaceTaskRules::assignableIds(int $workspaceId): array` (employee_id vai trò 1, 2).

- [x] Step 1: Test lỗi trước:
  - `test_create_task_in_workspace_requires_member_assignee` — người làm ngoài nhóm ⇒ 422 `errors.assignee_id`; vai trò Xem ⇒ 422; thành viên ⇒ 201, `workspace_id` lưu.
  - `test_disabled_tasks_tab_blocks_all_entry_points` (phần form) — `enabled_tabs=[]` ⇒ 422 `errors.workspace_id` cho POST, PUT, PATCH field.
  - `test_workspace_and_solution_are_exclusive` — gửi cả `workspace_id` + `solution_id` ⇒ 422.
  - `test_children_inherit_workspace_and_need_member_assignee` — con có người làm ngoài nhóm ⇒ 422 `errors.children.0.assignee_id`; hợp lệ ⇒ con sinh ra có cùng `workspace_id`.
  - `test_change_workspace_batch_all_or_nothing` — lô 3 bản sao, 1 người làm không thuộc nhóm mới ⇒ 422, cả 3 giữ nhóm cũ; hợp lệ ⇒ cả 3 đổi, có dòng lịch sử "Nhóm: A → B".
  - `test_draft_leaving_checks_assignee_membership` — Nháp có người làm đã bị bớt (dữ liệu dựng tay) chuyển giao ⇒ 422.
  - `test_closed_workspace_attach_is_423`.
- [x] Step 2: Chạy ⇒ FAIL.
- [x] Step 3: Cài `WorkspaceTaskRules`; gọi trong store / update / updateField / rời Nháp; `createChildrenAsTasks` chép `workspace_id`; đổi nhóm ở 1 bản sao ⇒ áp mọi task cùng `batch_id` trong 1 transaction; ghi `TaskHistory`.
- [x] Step 4: Chạy file test + toàn bộ `Tests/Feature/Workspace` ⇒ PASS.
- [x] Step 5: Commit.

### Task 4: Thành viên ↔ việc · Đóng / tự lưu trữ huỷ việc dở · tin bật/tắt tab

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Workspace/WorkspaceTaskCanceller.php`
- Modify: `Services/Workspace/WorkspaceMemberService.php` (`remove` `:190`, `changeRole` `:166`, `promoteWhenManagersLeft` `:~240`), `Services/Workspace/WorkspaceService.php` (`close` `:150`, `update` `:112`), `Listeners/Chat/SyncWorkspaceChat.php` (nhánh `updated` `:110-125`), `Http/Controllers/.../WorkspaceController.php` (`show` trả thêm `open_task_count`)
- Test: thêm vào `Tests/Feature/Workspace/WorkspaceTaskTest.php`

**Interfaces:**
- Produces: `WorkspaceTaskCanceller::openTaskQuery(Workspace $ws): Builder` (status ∉ {8, 9}, gồm Nháp) · `WorkspaceTaskCanceller::cancelAll(Workspace $ws, string $reason, ?int $actorId): int` (→ status 9, `TaskHistory` "Tự huỷ do …", 1 thông báo / người giao + người làm đang làm việc, theo `notification-convention`, prefix nhóm Nhiệm vụ) · `WorkspaceMemberService::openTasksOf(Workspace $ws, int $employeeId): int` (không tính Nháp). Chi tiết nhóm trả `open_task_count` (cho popup Đóng + popup tắt tab).

- [x] Step 1: Test lỗi trước:
  - `test_remove_member_with_open_tasks_is_blocked` — 422 `errors.member` "X đang làm 2 nhiệm vụ chưa xong của nhóm — chuyển người làm trước."; có `meta.assignee_id` để FE dựng link; chỉ có Nháp ⇒ cho bớt.
  - `test_demote_to_view_with_open_tasks_is_blocked`.
  - `test_close_cancels_open_tasks_reopen_does_not_restore` — 3 việc (Nháp, Đang làm, Hoàn thành - Chờ duyệt) ⇒ 9; việc Hoàn thành giữ 8; mở lại vẫn 9.
  - `test_auto_archive_cancels_open_tasks`.
  - `test_toggle_tasks_tab_posts_system_message` — tin "X đã bật tab Nhiệm vụ" / "đã tắt".
- [x] Step 2: Chạy ⇒ FAIL.
- [x] Step 3: Cài; `close()` và nhánh tự lưu trữ cùng gọi `cancelAll` trong transaction của chúng.
- [x] Step 4: Chạy toàn bộ `Tests/Feature/Workspace` ⇒ PASS.
- [x] Step 5: Commit.

### Task 5: API tab Nhiệm vụ của nhóm + gợi ý `#` + nhóm gán được

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Workspace/WorkspaceTaskListService.php`, `Http/Controllers/Api/V1/Workspace/WorkspaceTaskController.php`, `Transformers/Workspace/WorkspaceTaskItemResource.php`
- Modify: `hrm-api/Modules/Assign/Routes/Chat/api.php` (nhóm `v1/assign/workspaces`)
- Test: `Tests/Feature/Workspace/WorkspaceTaskListTest.php`

**Interfaces:**
- Produces (route, đều middleware `$wsMember` trừ `assignable`):
  - `GET workspaces/{id}/tasks?group_by=status|assignee|due&quick=all|mine|overdue|waiting_my_approval&q=&assignee_ids[]&creator_ids[]&statuses[]&priorities[]&due_from&due_to&view=list|table&sort_by&sort_dir&page&per_page` ⇒ `{ groups:[{key,label,color,count,overdue_count,hint}], quick_counts:{all,mine,overdue,waiting_my_approval}, items:[WorkspaceTaskItemResource], meta }`. Nhóm gom Hạn: `overdue · next_7_days · later · no_due · waiting_review · done` (định nghĩa spec gốc §5.1). Quá hạn theo L2 (nộp trước hạn không tính). Nháp: chỉ của người xem.
  - `WorkspaceTaskItemResource`: `id, code, title, priority, tags, status, status_text, status_color, assignee{id,name,department_code,code}, creator{…}, approver{…}, progress_pct, checklist_done, checklist_total, start_date, due_date, due_time, deadline_state_text, comment_count, updated_at, allowed_next_statuses, can_edit, can_delete, next_action`.
  - `GET workspaces/{id}/tasks/suggest?q=` ⇒ ≤ 10 `{id, code, title, status_text, status_color}` (việc dở trước).
  - `GET workspaces/assignable?include_ids[]=` ⇒ `[{id,name,is_locked}]` nhóm đang chạy + bật `'tasks'` + tôi là Quản lý/Thành viên; `include_ids` trả kèm (cờ `is_locked` nếu đã đóng / tắt tab).
  - `GET workspaces/{id}/members?assignable=1` ⇒ chỉ vai trò 1, 2.
- [x] Step 1: Test lỗi trước: `test_outsider_403_on_workspace_task_list` · `test_group_by_status_counts_match_items` · `test_quick_counts_follow_search_and_filters` · `test_overdue_ignores_submitted_before_due` · `test_draft_of_others_hidden` · `test_suggest_returns_only_this_workspace` · `test_assignable_excludes_closed_and_disabled_but_includes_ids` · `test_list_query_count_bounded` (đếm `DB::getQueryLog()` ≤ 8 với 40 việc — chống N+1).
- [x] Step 2: Chạy ⇒ FAIL. Step 3: Cài (eager load `with([...])`, đếm bằng `selectRaw`/`withCount`). Step 4: PASS + toàn bộ thư mục. Step 5: Commit.

### Task 6: Chat — thẻ nhiệm vụ + Tạo nhiệm vụ từ tin

**Files:**
- Modify: `Services/Chat/MessageService.php` (`send` `:74` nhận `card`; `list` `:30` hydrate thẻ 1 query; nhãn "đã tạo nhiệm vụ" trên tin gốc), `Services/Chat/ChatPresenter.php`, `TaskService::store` (khi có `source_message_id`), request gửi tin của `ChatController`
- Test: `Tests/Feature/Workspace/ChatTaskCardTest.php`

**Interfaces:**
- Consumes: `TaskAccess::canView`, `WorkspaceTaskRules`.
- Produces:
  - `POST chat/conversations/{id}/messages` nhận `card: {type: 'task', id: int}` (+ `body` tuỳ chọn) ⇒ tin `type='card'`, `attachable_type='task'`. Kiểm: hội thoại `space`, việc thuộc đúng `workspace_id` của hội thoại, nhóm bật `'tasks'` ⇒ sai 422 `errors.card`.
  - Tin trả về có `card: {type:'task', id, code, title, status_text, status_color, assignee{name}, due_date, deadline_state_text, progress_pct, deleted: bool}` đọc **lúc list** (`whereIn` 1 query). Việc đã xoá ⇒ `deleted: true`.
  - Tin gốc có `created_tasks: [{id, code}]` (từ `tasks.source_message_id`, 1 query).
  - `POST assign/tasks` nhận `source_message_id`: tin phải thuộc hội thoại `space` của đúng `workspace_id`, không phải `system`, chưa thu hồi; lưu xong **cùng transaction** gửi tin `card` `reply_to_id = source_message_id`, `sender_id = actor` (lô nhiều người: thẻ bản đầu, `body` "và n người khác").
- [x] Step 1: Test lỗi trước: `test_send_task_card_in_own_workspace` · `test_card_of_other_workspace_rejected` · `test_card_in_direct_conversation_rejected` · `test_card_hydrates_latest_status` (đổi status sau khi gửi ⇒ list trả status mới) · `test_card_of_deleted_task_renders_placeholder` · `test_create_from_message_posts_reply_card` · `test_create_from_recalled_or_system_message_rejected` · `test_disabled_tasks_tab_blocks_all_entry_points` (phần chat) · `test_card_message_still_no_notification_row` (không ghi `notifications`).
- [x] Step 2: FAIL. Step 3: Cài. Step 4: PASS + toàn bộ `Tests/Feature/Workspace` (kỳ vọng ≥ 24 cũ + mới, 0 fail). Step 5: Commit.

---

## Phase 2 — FE (hrm-client)

### Task 7: `V2BaseMiniTab` + nút Nhiệm vụ đầu nhóm + "Tab sử dụng"

**Files:**
- Create: `hrm-client/components/V2BaseMiniTab.vue` (**hỏi trước — component dùng chung mới**), cập nhật skill `.claude/skills/segmented-control/SKILL.md` (bảng "Khi nào dùng" thêm MINITAB)
- Modify: `pages/assign/workspaces/_id/index.vue` (đầu nhóm: MiniTab `[{key:'tasks',label:'Nhiệm vụ',icon:'ri-task-line',color:'#2563EB',count}]` chỉ khi `enabled_tabs` có `'tasks'`; `?panel=tasks`; tự thu cột hội thoại 68px), `components/chat/workspace/SettingsPanel.vue` (mục "Tab sử dụng": dòng Trao đổi luôn bật + công tắc Nhiệm vụ; tắt khi `open_task_count > 0` ⇒ `$confirm` nêu số việc), `components/chat/workspace/CreateWorkspaceModal.vue` (ô tick Nhiệm vụ, mặc định bỏ tick)
- Copy pattern: thông số chuyển động từ `components/V2BaseSegmented.vue` / `V2BaseTabNavigation.vue`; giao diện từ mockup `_build/dm.js` `miniTab()` + `dm.css` `.mtab*`.

**Interfaces:**
- Produces: `<V2BaseMiniTab :tabs="[{key,label,icon,color,count}]" :active-tab="key|null" @tab-change="fn(key)">`.
- [x] Step 1: Dựng component (viên chọn + viên hover 2 lớp; giãn 160ms ease-out → lò xo `cubic-bezier(.34,1.36,.64,1)` 400ms; hover nở 2px bằng width; `prefers-reduced-motion`).
- [x] Step 2: Gắn vào đầu nhóm + Cấu hình + popup tạo.
- [x] Step 3: Playwright MCP 1366 + 1440: đầu nhóm cao 64px 1 hàng; viên chọn lệch mục < 0.5px; tắt tab ⇒ nút biến mất ngay; popup tạo không tick ⇒ nhóm mới không có nút.
- [x] Step 4: Commit.

### Task 8: Tab Nhiệm vụ — danh sách gom nhóm (mockup 03) + Bảng

**Files:**
- Create: `hrm-client/components/assign/task/group-list/TaskGroupListView.vue` (khung: toolbar + chế độ), `TaskGroupToolbar.vue` (ô tìm debounce 300ms + huỷ request cũ, ô chọn Lọc nhanh có số + màu, nút Lọc (n) + popover 2 cột cố định, công tắc Danh sách | Bảng nhớ `localStorage` try/catch, Tạo mới, Cấu hình cột), `TaskGroupBlock.vue` (tiêu đề nhóm + ⓘ `info-popover` + "+ Thêm"), `TaskGroupRow.vue` (dòng 2 tầng 58px, nút bước tiếp, ⇄ Đổi trạng thái, bình luận badge, ⋯), `TaskStatusMenu.vue`; `utils/assign/workspaceTaskApi.js`
- Modify: `pages/assign/workspaces/_id/index.vue` (`panel=tasks` ⇒ `TaskGroupListView`), bảng dùng `V2BaseDataTable` (sort server)
- Copy pattern: lọc nhanh màu theo spec gốc §5.1 "Khung tab danh sách gọn"; dòng/khối từ mockup 03 (`_build/` khối style `/*st-act*/`); Đổi trạng thái gọi API có sẵn (`updateStatus` / `TaskPanel` luồng Tạm dừng hỏi lý do).

**Interfaces:**
- Consumes: API Task 5; `TaskPanel` (`open(id)`, `create({workspace_id, lock:{workspace_id:true}})`).
- [x] Step 1: Dựng component theo mockup 03; nhóm "Đã xong" thu sẵn; Gom theo Người làm / Hạn ⇒ nhãn trạng thái cạnh tên; Tạo mới + "+ Thêm" ẩn với vai trò Xem / nhóm đóng.
- [x] Step 2: Playwright MCP 1366 + 1440 (đo DOM): toolbar ≤ 46px; dòng 58px; không tràn ngang; số trong ô Lọc nhanh = số dòng sau khi chọn; mở tab bắn ≤ 2 request; bảng có thanh cuộn trên + dưới khi tràn.
- [x] Step 3: Commit.

### Task 9: Ô Nhóm trong `TaskPanel` / `TaskForm`

**Files:**
- Modify: `hrm-client/components/assign/task/panel/TaskForm.vue` (ô "Nhóm trao đổi" `V2BaseSelect` cạnh khối Giải pháp/Dự án `:9-27`; loại trừ; options lazy từ `workspaces/assignable` khi mở select, `include_ids` giá trị đang có; đổi nhóm ⇒ ô Người làm + dòng con lấy từ `members?assignable=1`, người làm không hợp lệ báo đỏ dưới ô, KHÔNG xoá), `TaskDetailTab.vue` + `TaskFieldPopover.vue` (trường Nhóm bấm-để-sửa, PATCH field), `TaskPanel.vue` (dòng "Tạo từ tin nhắn của X · dd/mm hh:mm" ⇒ `$router.push('/assign/workspaces/<id>?message=<msgId>')`)
- Modify: `components/chat/ChatPane.vue` (nhận `?message=` ⇒ tải `around=`, cuộn + tô sáng 2s)

- [x] Step 1: Cài. Step 2: Playwright MCP: mở panel ở màn Nhiệm vụ chung không bắn thêm request khi chưa bấm ô Nhóm; chọn nhóm ⇒ ô Giải pháp/Dự án khoá; người làm ngoài nhóm ⇒ lỗi đỏ dưới ô sau khi Lưu; màn GP: ô Nhóm khoá. Step 3: Chạy `e2e/tests/assign/task-panel-v2.spec.ts` ⇒ PASS. Step 4: Commit.

### Task 10: Chat — `#`, thẻ, Tạo nhiệm vụ từ tin, chặn bớt người, popup Đóng

**Files:**
- Create: `hrm-client/components/chat/TaskCard.vue`, `components/chat/TaskMentionSuggest.vue`
- Modify: `components/chat/ChatComposer.vue` (`#` chỉ khi hội thoại `space` + tab bật + có quyền gửi; gợi ý debounce 300ms; chọn ⇒ khối thẻ đính kèm phía trên ô nhập, ✕ bỏ; gửi ⇒ `card`), `components/chat/ChatMessageItem.vue` (render `type='card'`; nhãn `created_tasks` "📋 <code>"; mục "Tạo nhiệm vụ" trong thanh ⋯ ⇒ `TaskPanel.create({workspace_id, source_message_id, title: 80 ký tự cắt theo từ, description: toàn văn + "— Từ tin nhắn của X lúc hh:mm dd/mm"})`), `components/chat/workspace/MembersPanel.vue` (422 bớt / hạ Xem ⇒ hiện câu lỗi + link mở `?panel=tasks&assignee=<id>`), `components/chat/workspace/CloseWorkspaceModal.vue` ("n nhiệm vụ đang dở sẽ bị huỷ (kể cả Hoàn thành - Chờ duyệt)" + link xem)

- [x] Step 1: Cài. Step 2: Playwright MCP 2 tài khoản (NV 13 Quản lý, NV 24 Thành viên, NV 25 ngoài nhóm, 1 tài khoản vai trò Xem): `#` gợi ý đúng nhóm, gửi thẻ ⇒ bên kia nhận realtime, bấm thẻ mở panel; tạo từ tin ⇒ thẻ trả lời tin gốc + nhãn 📋; vai trò Xem không có `#` / "Tạo nhiệm vụ"; chat 1–1 không có `#`; bớt người còn việc ⇒ thấy lỗi + link lọc đúng. Step 3: Commit.

### Task 11: E2E + hồi quy + bàn giao

**Files:**
- Create: `HRM/e2e/tests/assign/workspace-tasks.spec.ts` (BASE_URL :3080, token qua env, `--no-deps`, KHÔNG chạy project `setup`)
- Modify: `HRM/.plans/gop-db/phan-he-cong-viec/gd2-nhiem-vu-trong-nhom/{plan,design}.md`, spec GĐ2 (mục "Đã triển khai"), `.plans/gop-db/STATUS.md`

- [x] Step 1: Ca có quyền + không quyền: Quản lý bật tab → tạo việc trong tab → giao Thành viên → `#` → tạo từ tin; người ngoài 403 trang + API; vai trò Xem chỉ đọc; tắt tab ẩn mọi lối.
- [x] Step 2: Chạy `workspace-tasks.spec.ts` + `chat-core.spec.ts` + `task-panel-v2.spec.ts` — đọc dòng tổng kết (serial: "did not run" ≠ passed). PHPUnit toàn `Tests/Feature/Workspace`.
- [x] Step 3: Xoá dữ liệu thử (giữ demo nhóm 93, 94), cập nhật tài liệu, STATUS. Không commit/push khi user chưa bảo.

## Ghi chú

**Commit từng task** (nhánh `gop_db-nhom-trao-doi`, chưa push; start hrm-api `fd1c2f1e7` · hrm-client `d0644d95d`):

| Task | hrm-api | hrm-client |
|---|---|---|
| 1 | `a7d2f521e` | — |
| 2 | `bf5d7e59e` | — |
| 3 | `633862590` | — |
| 4 | `7f795bf8a` | — |
| 5 | `fce22d5b2`, fix `9f828b016` | — |
| 6 | `3c5129d18` | — |
| 7 | — | `139dc871b` |
| 8 | fix BE `4bcf23bb4` | `01290d072`, fix `47f2dfc7f` |
| 9 | `3ce6d2789` | `e3858571e`, fix `e7ae1f7d8` |
| 10 | `73d20fa0b`, `ef87152cb` | `9f896411d`, fix `b6b9e4c6f` |
| 11 | — (e2e nằm ngoài git: `HRM/e2e/tests/assign/workspace-tasks.spec.ts`) | — |

**Đối chiếu dữ liệu Task 2** (DB `db_gop_6_11`, trước = BASE `a7d2f521e`, sau = code mới; so số dòng + md5 danh sách id): NV 13 (Tổng công ty + Duyệt triển khai) 43 = 43; NV 179 (Phòng ban) 0 = 0; NV 110 (Bộ phận) 0 = 0; NV 224 (Không có + Duyệt triển khai theo phòng) 39 = 39; NV 149 (chỉ vai trò cá nhân) 1 = 1 — md5 trùng cả 5. `test_every_listed_task_is_showable`: 30 NV có vai trò trên việc, mọi việc trong danh sách đều `show` được. Bảng `tasks` lúc đó 48 dòng; DB dev không có NV mức Công ty (3).

**Kiểm cuối (Task 11, 12/11):** e2e `workspace-tasks.spec.ts` 9 passed · `chat-core.spec.ts` 8 passed · `task-panel-v2.spec.ts` chỉ chạy ca 6, 8 (passed) + ca 7 (FAIL có sẵn, xem dưới) — ca 1–5 KHÔNG chạy vì giao việc thật cho NV có token FCM + queue sync ⇒ push thật · PHPUnit `Tests/Feature/Workspace` 69 passed.

**Bẫy / tồn cần nhớ:**
- task-panel-v2 ca 7 fail có sẵn (403 hiện 2 toast: "Bạn không có quyền xem nhiệm vụ này!" + "Không tải được chi tiết nhiệm vụ") — giống hệt ở BASE, fix #6 chưa có trên nhánh này.
- Deploy: `ROW_NUMBER() OVER` (phân trang theo nhóm) cần MySQL ≥ 8 — kiểm prod trước khi lên.
- Tồn quyết định chờ user: chữ nút "+ Thêm" → "Tạo mới" (button-convention thắng spec); ⇄ ẩn thay vì mờ; Tạm dừng không hỏi lý do; tab Nhiệm vụ GP/Hạng mục (`getTaskListForSolution` không lọc quyền) nay có thể 403 khi mở chi tiết; nhãn "Dự án / Nhóm" cạnh "Nhóm trao đổi".
- Ngoài luồng (ghi lại, fix trước merge prod): HandoverService đổi người làm không qua WorkspaceTaskRules; `deleteByIds` không qua TaskAccess; nhóm xoá mềm ⇒ không chặn ghi; cancelAll gửi thông báo trong transaction. Chi tiết minor hoãn: `.superpowers/sdd/plan/progress.md` của worktree.
- E2E: công tắc "Tab sử dụng" là `input.custom-control-input` ẩn (data-testid nằm trên input) — click bằng `evaluate(e => e.click())`; nút Nhiệm vụ đầu nhóm là `ws-tool-tasks`, không phải `mtab-tasks`; API tạo việc cần `task_type`.

## Checkpoint
### Checkpoint — 11/11/2026 (plan viết xong)
Vừa hoàn thành: spec GĐ2 user duyệt; plan 11 task (6 BE, 5 FE).
Đang làm dở: —
Bước tiếp theo: user review plan + chọn cách chạy (subagent / native); xin phép code riêng (repo · nhánh · migration Task 1 vào `db_gop_6_11`).
Blocked: —

### Checkpoint — 12/11/2026 (GĐ2 CODE XONG)
Vừa hoàn thành: Task 1–11 (6 BE + 5 FE) trên nhánh `gop_db-nhom-trao-doi`, commit từng task, review sạch; e2e workspace-tasks 9/9, chat-core 8/8, PHPUnit Workspace 69/69; dọn dữ liệu thử, nhóm demo 93/94 `enabled_tabs=[]`.
Đang làm dở: —
Bước tiếp theo: user duyệt các điểm tồn (chữ "Tạo mới", GP tab 403, MySQL 8 prod) → hỏi merge về `gop_db` / push nhánh; chạy lại task-panel-v2 ca 1–5 với chặn push khi được phép.
Blocked: task-panel-v2 ca 7 fail có sẵn (không do GĐ2).

### Checkpoint — 12/11/2026 (review toàn nhánh + đợt sửa cuối)
Vừa hoàn thành: review toàn nhánh (opus) → sửa 6 điểm (thẻ việc đã rời nhóm ⇒ `moved`, cờ chỉ xem khi nhóm đóng, thông báo huỷ `afterCommit` + không báo người đóng, test Q8, `source_message.can_open`) + hồi quy hideActions. Head: hrm-api `505724758`, hrm-client `ba84b2753` (nhánh `gop_db-nhom-trao-doi`, CHƯA push, CHƯA merge). PHPUnit Workspace 74/74; e2e workspace-tasks + chat-core 20/20 (chạy `--workers=1 --retries=0`). Ledger đầy đủ: `sdd-ledger.md` cùng folder.
Đang làm dở: —
Bước tiếp theo: user trả lời Câu 9 (tab GP + đối chiếu các màn khác mở TaskPanel) và Câu 10 (chạy task-panel-v2 ca 1–5 khi push thật) → rồi mới merge.
Blocked: Câu 9, Câu 10. Trước prod: kiểm MySQL ≥ 8 (ROW_NUMBER), HandoverService bỏ qua luật nhóm, push thật đã gửi trong lượt e2e Task 9 (24 thông báo).


### Checkpoint — 12/11/2026 (Câu 9 + Câu 10 xong)
- **Câu 10 = 1:** tạm `QUEUE_CONNECTION=database` ở `.env` worktree hrm-api → chạy toàn bộ `task-panel-v2`: ca 1–6 pass, ca 7 fail (có sẵn, 403 hai toast), ca 8 pass (chạy riêng vì serial). 12 job (6 SendNotification + 6 BroadcastNotificationCreated) bị giữ trong `jobs`, KHÔNG worker nào chạy ⇒ không push thật; đã xoá 12 job + 6 thông báo (NV 6, 47); `notifications` về 660,640; `.env` trả lại `sync`.
- **Câu 9 = 1:** hrm-api `627cb889a` — `TaskAccess::canView` thêm (d) việc gắn giải pháp người đó xem được (`Solution::visibleIdsQuery()` mới, bản sao luật `SolutionService::index`, test đối chiếu `SolutionVisibleIdsTest`) và (e) việc gắn dự án TKT xem được (`ProspectiveProject::visibleIdsQuery()` có sẵn). Nháp vẫn chỉ người tạo. Tác dụng phụ: người này bình luận / theo dõi được (assertWritable = xem được + nhóm chưa đóng).
  - Đo DB local trước sửa: NV 36 (GP tổng công ty) thấy 19 việc ở tab GP mà mở đều 403; NV 144/224/883 mỗi người 2 việc.
  - Test: `TaskAccessSolutionProjectTest` (đỏ với TaskAccess cũ, xanh với bản mới), Workspace 76/76, Task 31/31. Trait test mới `Tests/Feature/Concerns/ActsWithScopedPermission` (fixture `ActsAsProductUser::actAs` vỡ trên DB này — roles.company_id NOT NULL, role_has_permissions bỏ company_id).
  - Playwright (script, JWT NV 36, chặn request ghi): `/assign/solutions/1/manager?active_tab=tasks` → bấm Xem TPE.TASK.NB.26.0001 → show 200, panel 660×840 đúng mã, 0 toast.
- Còn trước merge/prod: MySQL ≥ 8, HandoverService bỏ luật nhóm, xác nhận các điểm lệch UI + sửa file dùng chung (Task.php N+1, CommentThread readonly). Merge / push chỉ khi user báo.

### Checkpoint — 12/11/2026 (đóng phiên GĐ2)
- Phiên AGENT đã gộp nhánh này vào `gop_db-tpe-smart-agent`: hrm-client `601e76370`, hrm-api `3621a8c66` (gồm `ba84b2753` / `627cb889a`).
- Ghim "TPE SMART AGENT" trên cùng khối "Đã ghim" (mockup sb2.js 11/11, màn 33): CHƯA làm — user làm tiếp ở phiên AGENT, trên nhánh agent.
- Tồn trước merge `gop_db` / prod (không đổi): sửa các minor trong `sdd-ledger.md`, HandoverService bỏ luật nhóm, MySQL ≥ 8, xác nhận điểm lệch UI + sửa file dùng chung.

### Checkpoint — 12/11/2026 (phiên CHAT: dọn tồn trước merge — BE xong)
User cho phép (12/11): làm hết B1–B9 + F1–F5 trên `wt-nhom-trao-doi`, nhánh `gop_db-nhom-trao-doi`, không migration, không push.
- Câu A = 1 (bàn giao: tự thêm người nhận vào nhóm làm Thành viên), A2 = 1 (đang Xem ⇒ nâng Thành viên). Khác công ty / nghỉ việc ⇒ vẫn giao, log cảnh báo (Claude tự chốt, đã báo user).
- Kiểm lại: `cancelAll` đã afterCommit (bỏ); Workspace KHÔNG SoftDeletes, không có route xoá nhóm (bỏ "nhóm xoá mềm"); can_edit/can_delete đã xét nhóm đóng từ đợt I2 + có test (bỏ B3); `source_message_id` đã có rule + MessageService kiểm.
- hrm-api commit: B1 `6d5c9c17d` · B2 `9980e0a3f` (chốt phòng thủ delete_by_ids) · B4 `cc50f4525` (duyệt Chờ phê duyệt kiểm người làm dòng con; đổi nhóm lô kiểm dòng con bản sao; tách `validateMove`) · B5 `08e6e20cf` (thu hồi ẩn created_tasks; xem trước "[Nhiệm vụ MÃ]") · B6 `989608807` (lockForUpdate ↔ sharedLock, đo 2 kết nối) · B7 `82b1062f4` ("Hệ thống") · B8 `70e649afb` (`Workspace::tasksEnabled()`) · B9 `ad4447420` (test).
- PHPUnit Workspace 92/92, Task 31/31; mỗi test mới đã kiểm đỏ trên code cũ.
- Còn: F1–F5 (FE). F1 nhớ: `store/chat.js` + `ChatPane.vue` tự dựng xem trước "[Nhiệm vụ] …" ⇒ thêm mã `card.code` cho khớp BE. Câu B (MySQL prod ≥ 8) chờ user.

### Checkpoint — 12/11/2026 ~16:10 (phiên CHAT: dọn tồn trước merge — FE xong)
Vừa hoàn thành: F1–F5 trên hrm-client nhánh `gop_db-nhom-trao-doi` — `6716c13fe` (fix) + `7c586f6bc` (prettier, chỉ định dạng; KHÔNG áp ChatShell / ConversationList / trang Tin nhắn vì nhánh agent có sửa, KHÔNG áp TaskDetailTab / TaskForm vì dùng chung ~19 màn). Repo không có prettier/eslint cài sẵn — dùng prettier 2.8.8 tạm ở scratchpad với `--end-of-line lf` (`.editorconfig` khiến prettier xuất CRLF). Không có eslint config ⇒ eslint không chạy.
- F4 (một phần không đổi): "form sửa việc có nhóm gọi members ngay lúc mở" GIỮ NGUYÊN — cần để lọc người làm / báo người ngoài nhóm.
- e2e mới `HRM/e2e/tests/assign/chat-gd2-polish.spec.ts` (7 ca): mỗi ca đã tái hiện ĐỎ trên code cũ (F1a "[Nhiệm vụ]" thiếu mã · F1b thẻ còn hiện khi sửa · F1c tên rỗng · F1d phản hồi cũ ghi 77 · F2 URL giữ panel=tasks · F3 2 toast · F4 408 option lúc tải) → 7/7 XANH sau sửa (2 lượt, lượt 2 ở load 44).
- Hồi quy `workspace-tasks` (12 ca) + `chat-core` (8 ca): CHẬP CHỜN do máy quá tải (load 10–44: Nuxt + php :8070 phiên Agent + Chrome headless khác) — trang tải 11–14s, `php -S` 1 luồng; mỗi lượt hỏng 1 ca khác nhau (ca 9 / 6b / 7, chat-core Đóng nhóm / GĐ2 thẻ #). Đối chứng: đưa client về HEAD cũ cùng điều kiện cũng hỏng (ca 1, rồi ca 7) ⇒ không do F1–F5. Không có truy vấn / transaction MySQL > 2s trong lúc hỏng (đã theo dõi processlist) ⇒ không do khoá B6. Notifications không tăng (660,696).
- Đã dọn: nhóm thử 2366 (probe) + 2363, 2371 (chat-core không tự dọn).
Bước tiếp theo: chạy lại `workspace-tasks` + `chat-core` khi máy nhàn để có lượt xanh trọn; rồi mục 3 (điểm UI chờ user) → mục 1 (màn danh sách nhóm). Câu B (MySQL prod ≥ 8) chờ user. Chưa push.
Blocked: —

### Checkpoint — 12/11/2026 ~16:20 (WRAP UP — user khởi động lại máy)
Vừa hoàn thành: mục 2 "dọn tồn trước merge" — BE B1–B9 (8 commit hrm-api) + FE F1–F5 (2 commit hrm-client), nhánh `gop_db-nhom-trao-doi`, worktree `websites/wt-nhom-trao-doi/` sạch (không file dở). Chưa push.
Đang làm dở: — (không file nào đang sửa dở)
Bước tiếp theo:
1. Sau khi máy khởi động lại, 3 server demo ĐÃ MẤT (PID 14177/14178/14179 cũ) — bật lại (kiểm cổng trống trước bằng `lsof -nP -iTCP:<cổng> -sTCP:LISTEN`):
   - API :8080: `cd websites/wt-nhom-trao-doi/hrm-api/public && php -S 127.0.0.1:8080 ../server.php` (chạy nền)
   - Socket :8895: `cd websites/wt-nhom-trao-doi/hrm-api && SOCKET_PORT=8895 node server_node/server.js` (Node 20)
   - Nuxt :3080: `cd websites/wt-nhom-trao-doi/hrm-client && npx nuxt` (Node 12 mặc định; `.env` đã có DEV_SERVER_PORT=3080, BASE_API_URL=:8080, SOCKET_URL=:8895)
2. Chạy lại e2e khi máy nhàn: `workspace-tasks` (12 ca) + `chat-core` (8 ca) + `chat-gd2-polish` (7 ca) — `--no-deps --workers=1 --retries=0`, token JWT mới qua tinker (NV 13 / 24 / 25), đọc dòng tổng kết (serial: "did not run" ≠ passed). chat-core KHÔNG tự dọn nhóm "[e2e] Nhóm chat …" — xoá tay sau khi chạy.
3. Hỏi user: Câu B (MySQL prod ≥ 8) · mục 3 (chữ "Tạo mới", ⇄ ẩn thay mờ, Tạm dừng không hỏi lý do, nhãn "Dự án / Nhóm") · mục 1 (màn danh sách nhóm, mockup 01).
4. Push / gộp lại vào nhánh agent / merge gop_db: chỉ khi user báo.
Blocked: —

### Checkpoint — 12/11/2026 ~17:20 (phiên CHAT: hồi quy e2e XANH trọn)
Vừa hoàn thành: bật lại 3 server demo (:8080 php -S, :8895 socket, :3080 Nuxt — Nuxt Node 12 sập "heap out of memory" khi build ngay sau khởi động máy ⇒ chạy bằng `NODE_OPTIONS=--max-old-space-size=8192 npx nuxt`). Chạy e2e lúc tải ~5: `workspace-tasks` 12/12 passed (2.9m) · `chat-core` 8/8 + `chat-gd2-polish` 7/7 = 15/15 passed (2.7m), `--workers=1 --retries=0`. Notifications giữ nguyên 660,696 (không push thật). Đã dọn nhóm thử 2376 (chat-core); không còn nhóm "[e2e]".
Đang làm dở: —
Bước tiếp theo: hỏi user Câu B (MySQL prod ≥ 8) · mục 3 điểm UI · mục 1 màn danh sách nhóm (mockup 01, cần cho phép code). Push / gộp vào nhánh agent / merge gop_db chỉ khi user báo.
Blocked: —
- 12/11 ~17:30 **Câu B CHỐT:** user kiểm trên máy DB prod: `mysqld --version` = 8.0.46-0ubuntu0.22.04.4 ⇒ `ROW_NUMBER() OVER` chạy được, bỏ khỏi danh sách tồn trước prod.
- 12/11 ~17:40 **User chốt:** mục 3 "đổi" cả 4 điểm UI theo spec — (1) "Tạo mới" → "+ Thêm" (user thắng button-convention); (2) ⇄ không đổi được ⇒ hiện MỜ + lý do (user thắng quy tắc "ẩn hẳn" của CLAUDE.md — ngoại lệ riêng tab Nhiệm vụ nhóm); (3) Tạm dừng có ô lý do (tuỳ chọn); (4) nhãn "Dự án / Nhóm" — đổi thành gì: CHƯA rõ, đang hỏi. **Mục 1 (màn danh sách nhóm, mockup 01): BỎ, không làm.**
- 12/11 ~17:40 **Việc mới (user: "cần làm ngay"):** thanh thao tác tin nhắn kiểu Zalo — biểu cảm ra khỏi toolbar; toolbar chỉ Trả lời · Chia sẻ · Tạo nhiệm vụ · Tạo vấn đề, có tooltip. Rà code: toolbar ở `components/chat/ChatMessageItem.vue:77-121` (6 emoji + Trả lời, Tạo nhiệm vụ, Ghim/Bỏ ghim, Sao chép, Sửa, Thu hồi; mở bằng bấm ⋯; tooltip = `title` thuần). BE CHƯA có chuyển tiếp tin (route Chat/api.php không có forward). Bảng `issues` KHÔNG có `workspace_id` / `source_message_id`; tạo vấn đề hiện gắn GP/dự án (`solutionMemberActive`). Chưa có lệnh code — đang hỏi phạm vi.
- 12/11 **Câu 1 toolbar = 1:** rê vào tin hiện ngay toolbar Trả lời · Chia sẻ · Tạo nhiệm vụ · Tạo vấn đề · ⋯ (menu Ghim/Bỏ ghim · Sao chép · Sửa · Thu hồi); biểu cảm = nút 👍 nhỏ góc bong bóng, rê ⇒ hàng emoji, bấm thẳng = 👍.
- 12/11 **Câu 2 Chia sẻ = 1:** chuyển tiếp tới mọi hội thoại mình gửi được (nhóm + 1–1), chọn nhiều, kèm lời nhắn; tin hiện "Chia sẻ từ <người gửi gốc>", giữ tệp (không copy file). Cần API mới + có thể 1 cột đánh dấu (migration — nêu tên trước khi code).
- 12/11 **Câu 3 Tạo vấn đề = HOÃN** (làm giai đoạn sau). Đợt này: toolbar + biểu cảm kiểu Zalo + Chia sẻ + 4 điểm UI mục 3.
- 12/11 **Câu 4 = 1:** nhãn "Dự án / Nhóm" ở `TaskForm.vue:34` → "Dự án" (form dùng chung ~19 màn — user đã biết).

## Đợt Z — Toolbar tin kiểu Zalo + Chia sẻ + 4 điểm UI (user cho phép "làm" 12/11 ~18:00)
Phạm vi: wt-nhom-trao-doi, nhánh gop_db-nhom-trao-doi, api + client; KHÔNG migration/seeder/push.
- [x] Z1 BE: POST chat/messages/{id}/forward (conversation_ids[], note) — quyền đọc tin gốc + gửi từng đích; meta.forwarded_from; nhân dòng files (cùng path); realtime như tin thường; PHPUnit có/không quyền
- [x] Z2 FE ChatMessageItem: hover hiện toolbar (Trả lời · Chia sẻ · Tạo nhiệm vụ · ⋯ menu Ghim/Bỏ ghim/Sao chép/Sửa/Thu hồi), nút 👍 góc bong bóng (rê ⇒ hàng emoji), tooltip v-b-tooltip; hiển thị "Chia sẻ từ …"
- [x] Z3 FE popup Chia sẻ (V2BaseModal: tìm + chọn nhiều hội thoại + lời nhắn) nối ChatPane
- [x] Z4 FE tab Nhiệm vụ nhóm: "Tạo mới" → "+ Thêm"; ⇄ mờ + lý do; Tạm dừng có ô lý do (tuỳ chọn)
- [x] Z5 FE TaskForm nhãn "Dự án / Nhóm" → "Dự án"
- [x] Z6 e2e: thêm/sửa ca, chạy lại chat-core + chat-gd2-polish + workspace-tasks; dọn dữ liệu

### Checkpoint — 12/11/2026 ~18:25 (Đợt Z CODE XONG, chưa commit)
Vừa hoàn thành: Z1–Z6 trên wt-nhom-trao-doi nhánh gop_db-nhom-trao-doi (CHƯA commit, theo quy tắc không tự commit).
- BE: `POST chat/messages/{id}/forward` (middleware read; ForwardMessageRequest; MessageService::forward — đích phải gửi được, 422 cả lô; meta.forwarded_from giữ người gửi GỐC qua nhiều lần chia sẻ; tệp = dòng files mới cùng path; lời nhắn = tin riêng; chặn tin hệ thống / thẻ / đã thu hồi / trước mốc xoá lịch sử); ChatPresenter `forwarded_from` {sender_name}; tin chia sẻ `can_edit=false` + edit() 422. PHPUnit ChatForwardTest 7 ca, Workspace 99/99.
- FE: ChatMessageItem — rê ⇒ thanh Trả lời · Chia sẻ · Tạo nhiệm vụ · ⋯ (menu Ghim/Bỏ ghim · Sao chép · Sửa · Thu hồi, position fixed), v-b-tooltip; nút 👍 góc bong bóng + hàng 6 emoji; nhãn "Chia sẻ từ …". ForwardModal mới (V2BaseModal, chọn nhiều, tìm debounce, lời nhắn, chưa chọn ⇒ lỗi inline). Tab nhóm: "+ Thêm" (TaskGroupBlock), ⇄ mờ + lý do (`statusLockReason` = bản sao luật Task::getAllowedNextStatuses; nhóm đóng vẫn ẩn), Tạm dừng hỏi lý do tuỳ chọn ⇒ `status_note`. TaskForm nhãn "Dự án".
- Lỗi bắt được khi đo DOM (đã sửa): (1) cha `.cm__actions` có transform ⇒ menu fixed văng x=2419; (2) V2BaseCheckbox @input ↔ toggle lặp vô hạn treo trang; (3) V2BaseButton không có prop `disabled` ⇒ nút Chia sẻ vẫn bấm được; (4) V2BaseIconButton disabled có pointer-events:none + opacity ⇒ không rê đọc được lý do.
- e2e: MỚI `HRM/e2e/tests/assign/chat-toolbar-zalo.spec.ts` 7 ca (có/không quyền: vai trò Xem); sửa 3 spec cũ theo thanh rê; ca 9 workspace-tasks setTimeout 60s (3 lần nạp trang, đo 31.7s ở tải 6). Lượt cuối 4 bộ 34/34 passed. Dọn: 0 nhóm [e2e], 0 việc ZZE2E; notifications 660,696 không đổi.
Đang làm dở: —
Bước tiếp theo: user xem thử trên :3080 → hỏi (a) Tạm dừng trong TaskPanel dùng chung (~19 màn) có hỏi lý do luôn không; (b) nhãn lịch sử BE "Dự án/Nhóm" (TaskHistoryService::snapshot) có đổi theo không. Commit / push khi user báo.
Blocked: —
Ghi chú: Playwright MCP (trình duyệt isolated) bị treo từ lúc tái hiện lỗi (2) — không pkill; khởi động lại phiên Claude là hết.

### Checkpoint — 12/11/2026 ~18:40 (Đợt Z ĐÃ COMMIT, chưa push)
Vừa hoàn thành: user chốt Câu 1 = 1 (Tạm dừng ở TaskPanel dùng chung cũng hỏi lý do tuỳ chọn ⇒ `status_note`), Câu 2 = 1 (nhãn lịch sử BE "Dự án/Nhóm" → "Dự án" ở TaskHistoryService). Commit: hrm-api `4749f0165`, hrm-client `26cd19d42` (nhánh gop_db-nhom-trao-doi). Kiểm: PHPUnit Workspace 99/99 + Task 31/31; e2e thêm Z8 (Tạm dừng ở panel) ⇒ 4 bộ workspace-tasks + chat-core + chat-gd2-polish + chat-toolbar-zalo **35/35**; dọn sạch [e2e]/ZZE2E; notifications 660,696.
Đang làm dở: —
Bước tiếp theo: push / gộp lại vào nhánh agent (gop_db-tpe-smart-agent) / merge gop_db — chỉ khi user báo. Tạo vấn đề từ tin: giai đoạn sau.
Blocked: —
Ghi chú: Vấn đề (Issue) vẫn ghi "Dự án/Nhóm" (IssueHistoryService:58, CreateIssueModal.vue:88) — ngoài phạm vi đợt này. Các file FE mới/sửa chưa chạy prettier (repo không cài sẵn).

### Checkpoint — 12/11/2026 ~19:00 (PUSH + gộp nhánh agent + MERGE gop_db — user cho phép "làm 1 2 3")
Vừa hoàn thành:
1. Push `gop_db-nhom-trao-doi`: hrm-api `4749f0165`, hrm-client `26cd19d42` (origin = local).
2. Gộp vào `gop_db-tpe-smart-agent` (worktree wt-tpe-agent, merge tự động không xung đột): api `e598c9a81`, client `3b1a2aa4c`. CHƯA push nhánh agent (còn commit chưa push của phiên AGENT; user không yêu cầu). File sửa dở `components/agent/AgentWorkspace.vue` của phiên AGENT để nguyên. ChatPane/ChatMessageItem sau merge = nhánh chat; ConversationList/ChatShell/trang Tin nhắn/server.js giữ phần agent. PHPUnit Workspace 99/99 (không chạy bộ Agent — nó xoá agent-eval-*.csv).
3. Merge vào `gop_db` qua worktree tạm từ origin/gop_db (không đụng thư mục chính đang checkout gop_db): tự động, file 2 bên cùng sửa chỉ TaskForm.vue (gop_db thêm `key` cho 2 select Người thực hiện — giữ cả 2 phía). PHPUnit Workspace 99/99 + Task 31/31 trên bản merge. ĐÃ PUSH origin/gop_db: api `174892532`, client `72b7a3bb3`. Worktree tạm đã gỡ.
Deploy cần: 5 migration Modules/Assign `2026_11_13_000001..000004` + `2026_11_14_000001` (workspaces, workspace_members, chat_*, mô tả nhóm, tasks.workspace_id/source_message_id) · server_node/server.js (+12 dòng, phòng socket chat) phải restart node · MySQL prod 8.0.46 ok.
Đang làm dở: —
Bước tiếp theo: thư mục chính ERP-HRM/HRM/hrm-* local gop_db đang tụt origin (pull khi user muốn); push nhánh agent do phiên AGENT; deploy theo ghi chú trên khi user báo.
Blocked: —
