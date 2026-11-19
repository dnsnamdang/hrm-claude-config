# GĐ33 Rời nhóm trao đổi — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Steps dùng checkbox (`- [ ]`).

**Goal:** Mọi thành viên nhóm trao đổi thường tự rời được nhóm (kể cả nhóm đã đóng); nhóm gắn Dự án KH chưa hỗ trợ.

**Architecture:** API riêng `POST workspaces/{id}/leave` (middleware thành viên, KHÔNG `open`) gọi `WorkspaceMemberService::leave()`
⇒ dùng lại `remove()` (chốt Quản lý cuối + việc dở + sự kiện `member_removed` ⇒ tin "X đã rời nhóm" + `conversation.updated`
removed_ids). FE: 1 helper dùng chung gọi từ 3 lối vào.

**Tech Stack:** Laravel 8 (php 8.1 local), Nuxt 2 / Vue 2, PHPUnit, Playwright.

**Spec:** `.plans/agent-chat/chat/gd33-roi-nhom/design.md` (user duyệt 17/11).

**Nhánh:** `gop_db-chat-roi-nhom` (api + client, worktree `wt-nhom-trao-doi`, tách từ `gop_db-chat-tin-nhiem-vu-gon` hay
`origin/gop_db` — HỎI user vì GĐ32 chưa commit). Không migration, không quyền mới.

## Global Constraints
- Nhóm gắn Dự án KH = `workspaces.source_type` khác NULL ⇒ API 422 "Nhóm gắn Dự án KH chưa hỗ trợ tự rời nhóm."; FE không hiện nút.
- Câu lỗi chặn giữ nguyên của service: `WorkspaceMemberService::MSG_KEEP_MANAGER` = "Nhóm phải còn ít nhất 1 Quản lý"; việc dở = "<Tên> đang làm n nhiệm vụ chưa xong của nhóm — chuyển người làm trước." (`WorkspaceMemberBlockedException`, meta assignee_id).
- Popup xác nhận: `$confirm({ title: 'Rời nhóm', message: 'Bạn sẽ không còn xem được chat của nhóm <tên>. Quản lý thêm lại sau vẫn được.', textAccept: 'Rời nhóm', danger: true })`.
- Nút/mục menu: chữ "Rời nhóm", icon `ri-logout-box-r-line`, nhóm nguy hiểm (`danger: true`).
- Không đổi API `DELETE members/{id}` (Mời ra của Quản lý).

## Review Focus
1. Quản lý (không phải cuối) rời nhóm đã đóng ⇒ được; Quản lý cuối nhóm đóng ⇒ 422 — PHPUnit ca 4.
2. Người vai trò Xem (không gửi tin được) vẫn rời được — PHPUnit ca 1b + e2e R1.
3. Rời khi đang mở chính nhóm đó trong ngăn trượt ⇒ ngăn không kẹt hội thoại "câm" (GĐ20) — e2e R2 kiểm ngăn về danh sách.
4. Bấm Rời 2 lần nhanh / 2 tab ⇒ lần 2 nhận 403 (không còn thành viên) và FE không báo lỗi lặp — e2e R3 gọi API 2 lần.
5. Socket local không chạy ⇒ hội thoại vẫn biến mất ngay ở máy người rời (FE tự `commit('chat/remove')`, không chờ socket) — e2e R1.

---

### Task 1: BE — API rời nhóm + cờ can_leave + source_type trong danh sách hội thoại

**Files:**
- Modify: `Modules/Assign/Services/Workspace/WorkspaceMemberService.php` (thêm `leave`)
- Modify: `Modules/Assign/Http/Controllers/Api/V1/Workspace/WorkspaceMemberController.php` (thêm `leave`)
- Modify: `Modules/Assign/Routes/Chat/api.php` (route sau dòng `members/{memberId}` delete)
- Modify: `Modules/Assign/Services/Workspace/WorkspaceAccess.php::abilities` (thêm `can_leave`)
- Modify: `Modules/Assign/Services/Chat/ConversationService.php` (2 câu select dòng ~151, ~223 thêm `w.source_type as workspace_source_type`; payload `workspace.source_type`)
- Test: `Modules/Assign/Tests/Feature/Workspace/WorkspaceLeaveTest.php` (copy khung dựng nhóm/việc từ `TaskStatusWorkspaceMessageTest`)

**Interfaces:**
- Produces: `WorkspaceMemberService::leave(Workspace $workspace, int $employeeId): void` (ném `ValidationException` 422 khi KH / chặn);
  `POST v1/assign/workspaces/{id}/leave` ⇒ 200 `{data: {left: true}}`, 422 `{message, meta?}`, 403 người ngoài;
  `abilities.can_leave` = là thành viên && `source_type` NULL; hội thoại `workspace.source_type`.

- [x] Step 1: Viết test (thất bại): `test_thanh_vien_roi_nhom` (200, mất dòng workspace_members, tin system body "<tên> đã rời nhóm", chat_conversation_members.left_at có giá trị) · `test_vai_tro_xem_roi_duoc` · `test_quan_ly_cuoi_bi_chan` (422 message MSG_KEEP_MANAGER, còn dòng) · `test_con_viec_do_bi_chan` (422, meta.assignee_id) · `test_nhom_dong_roi_duoc_quan_ly_cuoi_van_chan` (status đóng: Thành viên 200; Quản lý cuối 422) · `test_nhom_du_an_kh_422` (source_type set) · `test_nguoi_ngoai_403` · `test_abilities_can_leave` (show nhóm thường true, nhóm KH false).
- [x] Step 2: Chạy `php -d memory_limit=2G vendor/bin/phpunit Modules/Assign/Tests/Feature/Workspace/WorkspaceLeaveTest.php` ⇒ FAIL (404 route).
- [x] Step 3: Code `leave()` (tìm dòng thành viên của chính mình; KH ⇒ `ValidationException::withMessages(['workspace' => '…'])`; gọi `remove($workspace, $member, $employeeId)`), controller (catch như `destroy`), route `$wsMember`, `can_leave`, `source_type`.
- [x] Step 4: Chạy lại test ⇒ PASS; chạy cả `Modules/Assign/Tests/Feature/Workspace` ⇒ xanh.

### Task 2: FE — helper dùng chung + 3 lối vào

**Files:**
- Create: `utils/chat/workspaceLeave.js`
- Modify: `components/chat/ConversationRow.vue` (`actions`: thêm `leave` khi `c.type === 'space' && c.workspace && !c.workspace.source_type`)
- Modify: `components/chat/ConversationList.vue::onAction` (key `leave`)
- Modify: `components/chat/workspace/SettingsPanel.vue` (nút `V2BaseButton` "Rời nhóm" trong khối trạng thái, `v-if="abilities.can_leave"`, testid `ws-leave`)
- Modify: `components/chat/workspace/MembersPanel.vue` (dòng của mình hiện "Rời nhóm" cho MỌI vai trò khi `can_leave`; key `remove` của mình ⇒ gọi helper; Quản lý mời người khác giữ nguyên)
- Modify (nếu cần): `components/chat/workspace/WorkspaceView.vue` (SettingsPanel `@left="onRemoved"`)

**Interfaces:**
- Consumes: Task 1 API + `can_leave` + `workspace.source_type`.
- Produces: `leaveWorkspace(vm, { id, name }): Promise<boolean>` — `$confirm` ⇒ `POST workspaces/{id}/leave` ⇒ thành công: `vm.$store.commit('chat/remove', conversationId nếu biết)` + `dispatch('chat/fetchUnread')` + toast "Đã rời nhóm" ⇒ true; 422 ⇒ toast `message` (việc dở kèm link mở danh sách việc như `MembersPanel.showBlocked` nếu tách được, không thì toast) ⇒ false; huỷ ⇒ false.
  Hội thoại đang mở là nhóm vừa rời ⇒ trang Tin nhắn bỏ chọn (`$router.replace('/assign/messages')`), ngăn trượt về danh sách.

- [x] Step 1: Viết e2e (Task 3) trước, chạy ⇒ FAIL (chưa có nút).
- [x] Step 2: Code helper + 3 lối vào.
- [x] Step 3: Playwright đo: 3 lối vào hiện đúng vai trò; nhóm KH không có mục; sau rời dòng biến mất, URL về /assign/messages.

### Task 3: e2e `tests/assign/chat-roi-nhom.spec.ts` + hồi quy

Khung copy `chat-giao-dien.spec.ts` (pageAs, call, tinker dọn `[e2e] Rời nhóm …`). Token: A = NV 13 (Quản lý tạo nhóm), B = NV 24, C = NV 25.
- R1 Thành viên B rời qua menu ⋮ dòng hội thoại (trang Tin nhắn) ⇒ popup đúng câu ⇒ dòng biến mất NGAY, A thấy tin "… đã rời nhóm"; vai trò Xem C rời qua ⚙ Cấu hình.
- R2 Rời từ ngăn trượt khi đang mở nhóm ⇒ ngăn về danh sách, không còn dòng nhóm.
- R3 Gọi API leave lần 2 ⇒ 403. Người ngoài ⇒ 403.
- R4 Chặn: A (Quản lý cuối) bấm Rời ở tab Thành viên ⇒ toast "Nhóm phải còn ít nhất 1 Quản lý", vẫn còn trong nhóm; B được giao 1 việc dở ⇒ Rời ⇒ báo "đang làm 1 nhiệm vụ chưa xong".
- R5 Nhóm đã đóng: B rời được. Nhóm gắn Dự án KH (tinker set source_type): không có mục "Rời nhóm" ở ⋮ / ⚙ / tab Thành viên; API 422.
- [x] Chạy spec mới ⇒ PASS; chạy lại chat-core · giao-dien · bo-sung · thong-bao-emoji · gd2-polish · workspace-tasks · chat-drawer · workspace-role-groups (đọc dòng tổng kết, N7 chat-drawer chập chờn có sẵn ⇒ chạy lại riêng nếu đỏ).
- [x] Cập nhật plan (kết quả + checkpoint), README §3b, memory.

## Kết quả (17/11)
- Nhánh `gop_db-chat-roi-nhom` (api + client, wt-nhom-trao-doi) tách từ GĐ32 đã commit (api 9b069c0b8 · client 28ce6e3fb). CHƯA commit GĐ33.
- Lệch plan: e2e không qua ⋯ ở dòng của mình khi chỉ có 1 thao tác (V2BaseRowActions hiện thẳng nút icon); lỗi chặn ra `errors.role` / `errors.member` / `errors.workspace` (khuôn controller), câu Quản lý cuối là câu có sẵn "Nhóm phải có ít nhất 1 Quản lý — hãy chỉ định Quản lý khác trước."; DS hội thoại trả `workspace.is_kh_project` (không phải source_type).
- PHPUnit WorkspaceLeaveTest 8/8 · Workspace 267/267. e2e chat-roi-nhom 4/4 (R3 gộp R2). Hồi quy 9 bộ 68/68; sau sửa review: roi-nhom + drawer + role-groups xanh (role-groups G5 lượt đầu timeout lúc Nuxt dựng lại, chạy lại 6/6).
- Review độc lập (subagent, đã tự kiểm lại): SỬA #2 rời 2 lần cùng lúc ⇒ 2 tin "đã rời nhóm" (`remove()` dừng khi khoá dòng ra null) · #3 lần tải danh sách cũ ghi đè nhóm vừa rời (helper nạp lại danh sách). CHƯA SỬA, chờ user: #1 nhóm Dự án KH vẫn tự ra được qua "Mời ra" chính mình (DELETE members/{id của mình} / mời ra hàng loạt có tick mình — hành vi cũ, Quản lý mới gọi được) · #4 đang ở trang nhóm X, rời X từ ngăn trượt ⇒ ngăn đóng hẳn (đổi trang), không hỏng dữ liệu.
- Deploy: BE + FE cùng lúc (build_tpe làm cả 2); không migration.

### Checkpoint — 17/11/2026
Vừa hoàn thành: GĐ33 code xong + kiểm + review. CHƯA commit.
Bước tiếp theo: user xem :3080 + chọn hướng #1/#4 → báo commit/deploy (mang theo GĐ32).
Blocked:

### Quyết định 17/11 (user "làm theo đề xuất")
- #1 nhóm Dự án KH tự ra qua "Mời ra" chính mình: ĐỂ NGUYÊN, tính khi làm phần rời nhóm Dự án KH.
- #4 rời nhóm X từ ngăn trượt khi đang ở trang nhóm X ⇒ ngăn đóng do đổi trang: ĐỂ NGUYÊN (trang sau là nhóm vừa rời).

### Checkpoint — 17/11/2026 — ĐÃ DEPLOY TPE
GĐ32 + GĐ33 lên prod: api `b796c8f86` · client `7394e4c47` (gộp origin/gop_db có develop + fix quyền hạng mục giải pháp của người khác — prod đã có sẵn phần đó). build_tpe EXIT 0, Nothing to migrate, site 200.
