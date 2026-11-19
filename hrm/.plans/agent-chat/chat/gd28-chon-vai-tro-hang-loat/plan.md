# GĐ28 Chọn thành viên theo vai trò — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo / thêm thành viên nhóm theo 3 vai trò (người lẻ + phòng ban + cả công ty) và đổi vai trò / mời ra hàng loạt ở tab Thành viên.

**Architecture:** BE thêm 1 service gộp nguồn theo vai trò (`WorkspaceRoleGroupResolver`) dùng chung cho Tạo nhóm + Thêm thành viên, và 2 hàm lô trong `WorkspaceMemberService` (đổi vai trò / mời ra) với 1 sự kiện `members_bulk`. FE thêm component `RoleMemberPicker` thay 2 ô cũ ở 2 popup, `DepartmentPickModal` nhận `role`, `MembersPanel` thêm chọn nhiều.

**Tech Stack:** Laravel 8 (Modules/Assign), PHPUnit; Nuxt 2 / Vue 2, V2Base*, select2; Playwright e2e.

**Spec:** `design.md` cùng thư mục (+ `mockup.html` bản v2 đã duyệt).

**Repo / nhánh:** hrm-api + hrm-client, worktree `websites/wt-nhom-trao-doi`. Nhánh: hỏi user trước khi code (client đang có GĐ27 chưa commit trên `gop_db-chat-cot-lien-he-hep`). Không migration.
PHP: `/opt/homebrew/opt/php@8.1/bin/php -d memory_limit=1G vendor/bin/phpunit`. E2E: Node 20, BASE_URL :3080, CHAT_API :8080 (lệnh mẫu đầu `e2e/tests/assign/workspace-tasks.spec.ts`).

## Global Constraints
- Vai trò: `WorkspaceMember::ROLE_MANAGER=1 > ROLE_MEMBER=2 > ROLE_VIEWER=3`; trùng ⇒ giữ vai trò cao hơn (số nhỏ hơn).
- Người tạo nhóm luôn Quản lý. Nhóm KH (GĐ12): `KhProjectMemberSource::seed` vẫn chạy SAU lựa chọn tường minh.
- Thêm vào nhóm có sẵn: người đã là thành viên ⇒ bỏ qua (`skipped`), không đổi vai trò.
- "Cả công ty" = nhân sự đang làm việc của **công ty của nhóm** (`workspaces.company_id`; khi tạo = `company_id` form gửi / công ty đang chọn), BE tự truy vấn, không tin danh sách FE.
- Trần: mỗi nhóm vai trò `member_ids` ≤ 500, `department_member_ids` ≤ 3000; API lô `member_ids` ≤ 3000.
- Đổi / mời ra lô: đổi phần được, trả `blocked[]` (`member_id, employee_id, name, reason, open_task_count?`). Luật từng người như `changeRole` / `remove` hiện nay (hạ xuống Xem / mời ra khi còn việc dở ⇒ chặn).
- Lô chứa mọi Quản lý ⇒ **giữ người thao tác** (vào `blocked`, lý do "Nhóm phải còn ít nhất 1 Quản lý"); người thao tác chỉ tự hạ / tự rời khi ngoài lô còn Quản lý khác.
- 1 lượt lô = 1 `WorkspaceActivity('members_bulk')` ⇒ 1 tin hệ thống + 1 `conversation.updated`; thao tác 1 người giữ loại sự kiện cũ.
- Tin hệ thống: thêm "X đã thêm N người: a Quản lý · b Thành viên · c Xem" (bỏ vế = 0); đổi "X đã đổi vai trò N người sang <vai trò>" (N ≤ 3 ⇒ nêu tên); mời "X đã mời N người ra khỏi nhóm" (N ≤ 3 ⇒ nêu tên).
- UI theo skill: `modal-popup`, `button-convention` (`mr-2 mb-2`), `info-icon-tooltip` (b-popover `info-popover`), `$confirm`; badge vai trò màu `ROLE_COLORS` MembersPanel. Trường cũ API (`manager_ids`, `member_ids`, `department_member_ids`) vẫn nhận.

## Review Focus
- Người tạo nhóm cũng nằm trong thẻ phòng ở dòng Xem ⇒ vẫn là Quản lý (Task 1 test `creator_stays_manager_even_if_in_viewer_department`).
- Nhân viên đã nghỉ việc nằm trong `member_ids` gửi lên ⇒ bị bỏ qua, không lỗi (Task 1 test `inactive_employee_skipped`).
- Người thao tác chọn chính mình trong lô hạ xuống Xem khi chỉ mình là Quản lý ⇒ giữ, vào blocked (Task 3 test `actor_kept_when_batch_holds_all_managers`).
- Đổi bộ lọc ở tab Thành viên sau khi đã tích ⇒ bỏ chọn, không gửi người ngoài bộ lọc (Task 6 e2e bước G4).
- Gửi `member_ids` của nhóm khác vào API lô ⇒ bị bỏ qua (Task 3 test `foreign_member_ids_ignored`).

---

### Task 1: BE — gộp nguồn theo vai trò + Tạo nhóm / Thêm thành viên nhận `role_groups`

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Workspace/WorkspaceRoleGroupResolver.php`
- Modify: `Modules/Assign/Services/Workspace/WorkspaceService.php` (khối thêm thành viên ~dòng 144–163), `Modules/Assign/Http/Controllers/Api/V1/Workspace/WorkspaceMemberController.php::store`, `Modules/Assign/Services/Workspace/WorkspaceMemberService.php::add` (thêm tham số `bool $emitEvent = true`), request tạo nhóm + `AddWorkspaceMembersRequest`, `Listeners/Chat/SyncWorkspaceChat.php` (case `members_bulk`)
- Test: `Modules/Assign/Tests/Feature/Workspace/WorkspaceRoleGroupTest.php`

**Interfaces:**
- Produces: `WorkspaceRoleGroupResolver::resolve(array $roleGroups, int $companyId, ?int $actorId): array` ⇒ `[employee_id => ['role' => int, 'via' => int, 'department_names' => string[]]]` (chỉ NV đang làm việc; `via` = ADDED_MANUAL nếu người được chọn lẻ ở dòng thắng, ngược lại ADDED_FROM_DEPARTMENT; actor ép role 1).
- Produces: `WorkspaceRoleGroupResolver::companyEmployeeIds(int $companyId): int[]` (dùng lại truy vấn `EmployeeProfiles::baseQuery()` + `ACTIVE_STATUS` như `previewFromDepartments`, lọc `employee_infos.company_id`).
- Produces: `WorkspaceMemberService::addResolved(Workspace $ws, array $resolved, ?int $actorId): array{added:int[], skipped:int[], role_counts: array<int,int>}` — gọi `add(..., emitEvent:false)` theo (role, via) rồi phát 1 `WorkspaceActivity('members_bulk', ['action'=>'add','role_counts'=>…, 'employee_ids'=>…])`.
- Request: `role_groups` `nullable|array|max:3`; `role_groups.*.role` `required|in:1,2,3|distinct`; `.member_ids` `array|max:500`; `.department_member_ids` `array|max:3000`; `.department_names` `array|max:50`; `.whole_company` `boolean`.

- [x] **Step 1: Viết test** `WorkspaceRoleGroupTest`: `create_with_three_role_groups_assigns_highest_role` (NV A ở dòng 1 + dòng 3 ⇒ role 1; B ở dòng 2 + 3 ⇒ 2; C chỉ dòng 3 ⇒ 3; đếm `role_counts` [1=>2(gồm actor),2=>1,3=>1]) · `creator_stays_manager_even_if_in_viewer_department` · `whole_company_adds_all_active_of_workspace_company` (đếm = số NV đang làm việc công ty, BE bỏ qua id FE gửi kèm) · `inactive_employee_skipped` · `add_to_existing_skips_members_without_role_change` · `one_system_message_per_request` (đếm `chat_messages` type system tăng đúng 1, nội dung "đã thêm 4 người: 2 Quản lý · 1 Thành viên · 1 Xem") · `legacy_fields_still_work` (gửi `manager_ids`/`member_ids` như cũ ⇒ kết quả như trước).
- [x] **Step 2:** Chạy `--filter WorkspaceRoleGroupTest` ⇒ FAIL.
- [x] **Step 3:** Cài resolver + `addResolved` + nối vào `WorkspaceService::create` (role_groups có ⇒ dùng; không ⇒ nhánh cũ) và `store` (trả thêm `role_counts`) + listener case `members_bulk` action add.
- [x] **Step 4:** Chạy lại test mới + `WorkspaceApiTest`, `KhProjectMemberSourceTest`, `WorkspaceCrossCompanyTest` ⇒ PASS.

### Task 2: BE — xem trước "Cả công ty"

**Files:**
- Modify: `PreviewDepartmentMembersRequest` (thêm `whole_company` boolean), `WorkspaceMemberService::previewFromDepartments` (nhánh whole_company dùng `companyEmployeeIds`), `WorkspaceMemberController::preview`
- Test: `WorkspaceRoleGroupTest::preview_whole_company_returns_ids_and_names`

**Interfaces:**
- Produces: `POST workspaces/preview-departments` và `POST workspaces/{id}/members/preview-departments` với `whole_company=1` ⇒ `{employees:[…format + already_member], department_names:['Cả công ty']}`.

- [x] **Step 1:** Test: gọi với `whole_company=1` không kèm phòng ⇒ 200, `count(employees)` = số NV đang làm việc công ty nhóm, `department_names == ['Cả công ty']`.
- [x] **Step 2:** Chạy ⇒ FAIL. **Step 3:** Cài. **Step 4:** Chạy ⇒ PASS.

### Task 3: BE — đổi vai trò / mời ra hàng loạt

**Files:**
- Modify: `WorkspaceMemberService.php` (thêm 2 hàm), `WorkspaceMemberController.php` (2 action), `Modules/Assign/Routes/Chat/api.php` (sau dòng 43, middleware `$wsManagerOpen`), `SyncWorkspaceChat.php` (action role / remove)
- Create: `Http/Requests/Workspace/BulkWorkspaceMembersRequest.php` (`member_ids required|array|min:1|max:3000`, `member_ids.* integer`, `role` `in:1,2,3` — bắt buộc ở route roles)
- Test: `Modules/Assign/Tests/Feature/Workspace/WorkspaceMemberBulkTest.php`

**Interfaces:**
- Produces: `bulkChangeRole(Workspace $ws, array $memberIds, int $role, int $actorId): array{changed:int[], blocked:array}` · `bulkRemove(Workspace $ws, array $memberIds, int $actorId): array{removed:int[], blocked:array}`. Mỗi phần tử `blocked`: `['member_id','employee_id','name','reason','open_task_count'?]`.
- Routes: `PUT /{id}/members/roles` ⇒ `bulkUpdate` · `POST /{id}/members/bulk-remove` ⇒ `bulkDestroy`. Trả `{changed_count|removed_count, blocked, members}`.
- Thuật toán giữ Quản lý: tính tập Quản lý còn lại sau lô; rỗng ⇒ bỏ người thao tác khỏi lô (nếu có) vào blocked; người thao tác không phải Quản lý trong lô ⇒ giữ Quản lý vào trước nhất theo `joined_at` còn trong lô. Khoá dòng (`lockForUpdate`) như `changeRole` trước khi đếm việc dở.

- [x] **Step 1: Viết test**: `bulk_role_changes_all_eligible` (96 Xem ⇒ Thành viên, 1 tin "đã đổi vai trò 96 người sang Thành viên") · `viewer_demotion_blocked_for_open_tasks` (1 người còn việc ⇒ blocked có `open_task_count`, người khác vẫn đổi) · `actor_kept_when_batch_holds_all_managers` · `actor_can_demote_self_when_other_manager_outside_batch` · `bulk_remove_respects_same_rules` · `foreign_member_ids_ignored` · `non_manager_gets_403` (thành viên thường gọi ⇒ 403 qua middleware).
- [x] **Step 2:** Chạy ⇒ FAIL. **Step 3:** Cài. **Step 4:** Chạy test mới + toàn bộ `Tests/Feature/Workspace` ⇒ PASS.

### Task 4: FE — `RoleMemberPicker` + DepartmentPickModal theo vai trò

**Files:**
- Create: `hrm-client/components/chat/workspace/RoleMemberPicker.vue`
- Modify: `components/chat/workspace/DepartmentPickModal.vue` (prop `role`, `higherIds`), `utils/chat/workspaceOptions.js` nếu cần hàm đếm

**Interfaces:**
- Produces: `<RoleMemberPicker v-model="groups" :company-id :company-name :workspace-id :locked-ids="[me]" :existing-ids />`; `groups` = `[{ role, member_ids:[], sources:[{key, kind:'dept'|'company', label, employee_ids:[], department_names:[]}] }]` ×3. Method `payload()` ⇒ `role_groups` đúng hợp đồng Task 1 (`whole_company:true` khi có nguồn company, `department_member_ids` = hợp các nguồn dept). Computed `summary` ⇒ `{total, counts:{1,2,3}, dupCount, dupList}` theo luật vai trò cao hơn.
- `DepartmentPickModal`: prop `role` (null = như cũ) ⇒ tiêu đề "Lấy người làm <badge> từ phòng ban / bộ phận", ghi chú + nút "Thêm n người làm <vai trò>"; prop `higherIds` ⇒ dòng "Đã là <vai trò> — giữ" bỏ tick sẵn. Emit `picked` không đổi dạng.
- Dòng theo mockup v2: badge (tooltip quyền) + số · ô chọn trộn chip người + thẻ nguồn (icon `ri-building-line` / `ri-community-line` + số, ×) · link "Phòng ban" · "Cả công ty" (mờ khi đã có). Nhiều chip người ⇒ gom "+n người". ⓘ cạnh nhãn theo `info-icon-tooltip`. Dòng tổng + "k người có ở nhiều dòng ⇒ giữ vai trò cao hơn · Xem" (popover danh sách).

- [x] **Step 1:** Dựng component + sửa DepartmentPickModal.
- [x] **Step 2:** Kiểm tạm trên :3080 bằng Playwright khi Task 5 nối xong (component chưa có chỗ gắn).

### Task 5: FE — gắn vào Tạo nhóm + Thêm thành viên

**Files:** Modify `components/chat/workspace/CreateWorkspaceModal.vue` (bỏ ô Quản lý/Thành viên + `deptPicked`, gửi `role_groups`; validate: nhóm phải có ≥ 1 Quản lý = người tạo, luôn đúng), `AddMembersModal.vue` (thay ô chọn, nút "Thêm N người", toast dùng `role_counts`).

**Interfaces:** Consumes `RoleMemberPicker.payload()` / `summary` (Task 4), API Task 1–2.

- [x] **Step 1:** Sửa 2 popup. **Step 2:** Playwright :3080: tạo nhóm 3 dòng (BGĐ ⇒ Quản lý, 1 phòng ⇒ Thành viên, Cả công ty ⇒ Xem) ⇒ tab Thành viên đếm đúng theo vai trò; đo DOM: 3 `.rr__row` cùng cột x của ô chọn, popup không tràn ngang (`scrollWidth - clientWidth == 0`), nút footer cách 12px.

### Task 6: FE — tab Thành viên chọn nhiều + đổi vai trò / mời ra

**Files:** Modify `components/chat/workspace/MembersPanel.vue`.

**Interfaces:** Consumes routes Task 3.
- Cột ô tích + tích đầu cột (chỉ `canManage`), ô lọc Phòng ban / Bộ phận (từ `department_name`/`part_name` của danh sách thành viên), đổi lọc ⇒ bỏ chọn. Tích đầu cột = mọi người đang lọc (không chỉ trang). Có chọn ⇒ dòng "Đã chọn **n** người đang lọc · Bỏ chọn" + `Đổi vai trò ▾` (menu vai trò đích) + `Mời ra khỏi nhóm`; `$confirm` nêu số người; kết quả: toast + `blocked` hiện danh sách trong khối báo lỗi sẵn có.

- [x] **Step 1:** Sửa MembersPanel. **Step 2:** Playwright đo DOM như mockup ④.

### Task 7: E2E + chạy lại bộ liên quan

**Files:** Create `HRM/e2e/tests/assign/workspace-role-groups.spec.ts` (khuôn chạy + dọn dữ liệu như `workspace-tasks.spec.ts`).

- [x] **Step 1:** Viết ca: G1 tạo nhóm 3 dòng ⇒ số theo vai trò đúng, 1 tin hệ thống · G2 trùng dòng ⇒ dòng tổng báo k người, tab Thành viên ra vai trò cao hơn · G3 Thêm thành viên vào nhóm có sẵn theo vai trò, người đã có bị bỏ qua · G4 lọc phòng + tích đầu cột ⇒ đổi sang Thành viên; đổi lọc sau khi tích ⇒ bỏ chọn · G5 lô có người còn việc dở ⇒ báo bị chặn, còn lại đổi · G6 Thành viên thường (CHAT_TOKEN_B) không thấy ô tích / API 403.
- [x] **Step 2:** Chạy `workspace-role-groups` + `workspace-tasks`, `workspace-kh-project`, `chat-members-paging`, `chat-drawer` ⇒ đọc dòng tổng (serial: "did not run" ≠ passed).
- [x] **Step 3:** Cập nhật plan/README/STATUS; hỏi user commit (user tự báo).

## Checkpoint
### Checkpoint — 16/11/2026 khuya (wrap up) — ĐÃ DEPLOY TPE
Vừa hoàn thành: commit + fast-forward origin/gop_db (api `a33a6963e` · client `97c97a86f` GĐ27 + `12a065598` GĐ28, cùng GĐ26 `067de626b`), deploy TPE: build_tpe EXIT 0, Nothing to migrate, prod api a33a6963e · client 12a065598, site 200.
Bước tiếp theo: user thử prod (tạo nhóm 3 vai trò, tab Thành viên đổi vai trò hàng loạt). Minor hoãn + ngoài luồng xem dưới.

### Checkpoint — 16/11/2026 khuya
Vừa hoàn thành: 7 task + review cuối (0 Critical; 3 Important đã sửa). PHPUnit Workspace 259/259; e2e workspace-role-groups 6/6, workspace-tasks 12, chat-members-paging 3, chat-drawer 10, chat-task-status 3. Nhánh api + client `gop_db-chat-vai-tro-hang-loat` (wt-nhom-trao-doi) CHƯA commit (client mang theo GĐ27).
Đang làm dở: —
Bước tiếp theo: user thử :3080 → user báo commit → push gop_db + deploy TPE (api + client, không migration).
Blocked: —
Ngoài luồng: e2e workspace-kh-project K1 đỏ cả với client gốc (API :8080 4 worker kẹt sau khi tải lại) — ghi lại, chưa sửa. Minor hoãn: xem ledger-sdd.md "Final: minor".
