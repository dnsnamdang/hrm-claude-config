# GĐ14 — Popup thông tin cá nhân trong chat — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [x]`) syntax.

> Phụ trách: @namdangit · 15/11/2026 · trạng thái: ĐÃ lên origin/gop_db 15/11 (api `a5290628e` · client `85a2a590d`), CHƯA deploy.

**Goal:** Bấm vào người trong chat ⇒ `V2BaseModal` thông tin cá nhân (kèm chức vụ, SĐT, email) + nút Nhắn tin 1–1.

**Architecture:** 1 API `GET chat/profile/{id}` (EmployeeProfiles + working_positions + ChatPresence); FE 1 component
`ChatProfileModal` gắn 1 lần ở `ChatShell` / `ChatDrawer`, mở qua store `chat` (`openProfile(id)`), cache theo phiên.

**Spec:** `.plans/agent-chat/chat/gd14-ho-so-nguoi-dung/design.md`

## Global Constraints

- Nhánh mới `gop_db-chat-ho-so` (api + client) tách từ `origin/gop_db` (= `72f929f76` / `9f5014f3b`), worktree `wt-nhom-trao-doi`.
- Không migration, không quyền mới. SĐT = `telephone`, email = `email`; KHÔNG trả `personal_*`.
- Popup dựng trên `components/modal/V2BaseModal.vue`; nút theo `button-convention` (Nhắn tin primary + icon, Đóng cuối).
- Chữ xám cho nhãn (`#6b7280`), không chữ đỏ; ô trống "—".
- Không chạy toàn bộ e2e tới khi user yêu cầu; đo DOM bằng Playwright MCP, mở app cho user.

## Review Focus

1. Người đã nghỉ việc / không có chức vụ ⇒ popup vẫn mở, ô trống "—", không nút Nhắn tin.
2. Bấm chính mình ⇒ không nút Nhắn tin.
3. Bấm avatar trong tin của nhóm KHÔNG làm mất thanh thao tác tin / không mở menu tin (chặn lan sự kiện).
4. Nhắn tin khi đã có 1–1 ⇒ mở đúng hội thoại cũ, không tạo mới.
5. Tin hệ thống / tin đã thu hồi không có người gửi ⇒ không lỗi.

---

### Task 1: API `GET chat/profile/{employeeId}` (BE)

**Files:**
- Modify: `Modules/Assign/Routes/Chat/api.php` — cạnh `/directory`: `Route::get('/profile/{employeeId}', [ChatController::class, 'profile'])->where('employeeId', '[0-9]+');`
- Modify: `Http/Controllers/Api/V1/Chat/ChatController.php` — `profile($employeeId)`.
- Create: `Services/Chat/ChatProfileService.php` — `public function show(int $me, int $employeeId): ?array`.
- Test: `Tests/Feature/Workspace/ChatProfileTest.php`.

**Interfaces — Produces:** JSON `data` = `{employee_id, fullname, code, image, company_name, department_name, part_name, work_position_name, telephone, email, is_active, online, last_seen_at, is_me, conversation_id}`.

- [x] Test `test_ho_so_tra_du_truong_va_chuc_vu`: NV 13 xem NV 24 ⇒ 200, `telephone`/`email` = `employee_infos` của 24, `work_position_name` = `working_positions.name` theo `employee_work_position_id`, không có khoá `personal_telephone`/`personal_email`, `is_me=false`.
- [x] Test `test_ho_so_khac_cong_ty_xem_duoc`: NV công ty khác (company_role khác) ⇒ 200.
- [x] Test `test_ho_so_cua_minh_va_khong_ton_tai`: xem 13 ⇒ `is_me=true`; id 99999999 ⇒ 404; có hội thoại 1–1 ⇒ `conversation_id` đúng.
- [x] Chạy ⇒ FAIL; viết code; chạy ⇒ PASS; cả `Tests/Feature/Workspace` ⇒ PASS.

### Task 2: `ChatProfileModal` + store (FE)

**Files:**
- Create: `hrm-client/components/chat/ChatProfileModal.vue` (V2BaseModal sm, `data-testid="chat-profile-modal"`, nút `chat-profile-message`).
- Modify: `store/chat.js` — state `profile: { open: false, employeeId: null }`, cache `profiles: {}`; mutation `openProfile(id)` / `closeProfile`; action `fetchProfile(id)` (cache hit ⇒ không gọi).
- Modify: `components/chat/ChatShell.vue`, `components/chat/ChatDrawer.vue` — gắn `<ChatProfileModal>` 1 lần; nút Nhắn tin gọi lại `openDirect({employee_id})` sẵn có của mỗi vỏ.

- [x] Nuxt biên dịch không lỗi.

### Task 3: Gắn chỗ bấm (FE)

**Files:**
- `components/chat/ChatMessageItem.vue` — avatar + `.cm__name-text` ⇒ `@click.stop="$store.commit('chat/openProfile', m.sender_id)"`; `html()` bọc `@Tên` thêm `data-emp="<id>"`, `.cm__text` click delegation ⇒ mở popup.
- `components/chat/workspace/MembersPanel.vue` — avatar + tên dòng thành viên.
- CSS `cursor: pointer`.

### Task 4: Kiểm Playwright + mở app

- [x] Bấm avatar / tên / `@Tên` / dòng thành viên ⇒ `[data-testid=chat-profile-modal]` hiện đúng tên; đếm request `chat/profile/` = 1 sau 2 lần mở cùng người.
- [x] Đọc đủ trường; người không có chức vụ ⇒ "—".
- [x] Bấm mình ⇒ 0 nút `chat-profile-message`; bấm NV 24 ⇒ Nhắn tin mở ngăn/pane 1–1 đúng `conversation_id`.
- [x] Footer ghim đáy, 2 nút cách 12px; ghi ca e2e cần thêm; `open` app cho user.

---

### Checkpoint — 15/11/2026
Vừa hoàn thành: design (user duyệt) + plan.
Bước tiếp theo: hỏi "làm" kèm phạm vi.
Blocked: chưa có lệnh code.

### Checkpoint — 15/11/2026 ~08:55
Vừa hoàn thành: Task 1–4. Nhánh `gop_db-chat-ho-so` (api + client, wt-nhom-trao-doi) tách từ origin/gop_db. CHƯA commit. Không migration.
Lệch plan (đã cân nhắc): KHÔNG dùng store — mỗi vỏ (ChatShell `chat-profile-page` / ChatDrawer `chat-profile-drawer`) gắn 1 `ChatProfileModal` + `provide('openChatProfile')`, con `inject` ⇒ ngăn + trang cùng tồn tại vẫn chỉ 1 popup; cache = biến module trong ChatProfileModal. Popup size `md` (500px) thay `sm` (300px: email bẻ dòng, công ty 2 dòng — đo ảnh).
Kiểm: PHPUnit `Tests/Feature/Workspace` 232/232 (3 ca mới ChatProfileTest) · Playwright :3080: bấm tên NV 24 ⇒ popup đủ 6 dòng (chức vụ "TP Kinh doanh"), mỗi dòng 30px; mở lại cùng người 0 request thêm; `@Nguyễn Đức Tuân` mở đúng; tab Thành viên bấm mình ⇒ 0 nút Nhắn tin; Nhắn tin ⇒ /assign/messages?c=97 (hội thoại cũ); ngăn trượt (trang my-todo) ⇒ 1 popup `chat-profile-drawer` nằm trên ngăn, Nhắn tin ⇒ ngăn chuyển conversation 97, không đổi trang. Footer 2 nút cách 16px = khuôn V2BaseModal chung (bootstrap `.modal-footer > *` margin 4px, popup Chia sẻ cũng vậy) — không sửa component chung.
Tin của chính mình (bong bóng phải GĐ10) không có avatar/tên ⇒ bấm mình chỉ từ tab Thành viên / @Tên.
E2E cần thêm khi user yêu cầu: ca popup hồ sơ trong `chat-core.spec.ts`.
Bước tiếp theo: user thử :3080 → báo commit/push gop_db → deploy (không migration).

### Task 5 (15/11, user "Đã đúng nhưng style chưa đẹp" ⇒ chọn C mockup + dải màu = popup báo cáo, "làm")
- [x] `mockup.html` 3 phương án (B phẳng · C dải bìa · D lưới 2 cột) — user chọn C, sửa dải màu theo `V2BaseReportModal` (135deg #0a1c3d → #06b6d4, nút × tròn trắng 15%).
- [x] `ChatProfileModal.vue` viết lại giao diện: slot `header` = dải bìa + × + avatar 80px; footer chung ẩn qua `dialog-class="chat-profile-dialog"` (style không-scoped); 3 nút nhanh Nhắn tin (gradient) · Gọi `tel:` · Email `mailto:` (ẩn khi thiếu dữ liệu / Nhắn tin ẩn khi là mình hoặc đã nghỉ); khối thông tin nền #f8fafc; chip trạng thái.
- [x] Playwright: tái hiện lỗi avatar bị `.v2-modal-body` (overflow) cắt nửa trên (ảnh) ⇒ chuyển avatar vào dải bìa, định vị tuyệt đối bottom −44px ⇒ đo lại: điểm ảnh đầu avatar thuộc avatar, tâm avatar = tâm popup (600/600), cách tên 8px; popup 420×433, thân không cuộn; dải bìa đúng gradient; mình ⇒ chỉ Gọi · Email; Nhắn tin ⇒ /assign/messages?c=97.

### Checkpoint — 15/11/2026 (wrap up)
Vừa hoàn thành: GĐ14 Task 1–5 + giao diện phương án C; commit + push fast-forward origin/gop_db (api `a5290628e` · client `85a2a590d`).
Đang làm dở: —
Bước tiếp theo: deploy TPE khi user báo (không migration) — skill `deploy-hrm`; e2e popup hồ sơ + @all chờ user yêu cầu.
Blocked: —
