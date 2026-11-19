# GĐ12 — Nhóm trao đổi gắn Dự án KH — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nhóm trao đổi gắn được với 1 Dự án TKT hoặc 1 GP: lúc tạo nhóm tự thêm nhân sự từ màn manager (1 lần), nhiệm vụ / meeting tạo trong nhóm về màn manager; mọi nhóm nhận thành viên khác công ty.

**Architecture:** Giữ `workspaces.type = TYPE_GROUP` (không dùng type 2/3 — 15 chỗ đang gate bằng `isGroup()`), đánh dấu nhóm dự án KH bằng `source_type` (`prospective_project` | `solution`) + `source_id` đã có sẵn. Một service nguồn nhân sự tính danh sách người + nhãn chức vụ từ dữ liệu manager — dùng 1 lần lúc tạo nhóm để thêm thành viên, và lúc đọc để hiện cột chức vụ. Không đồng bộ sau tạo (user chốt 14/11). Tab Nhiệm vụ / Meeting của nhóm KH lọc theo dự án / GP thay vì `workspace_id`.

**Tech Stack:** Laravel 8 (PHP 7.4 local / 8.1 prod — code phải chạy được 7.4), Nuxt 2 / Vue 2 / bootstrap-vue, PHPUnit feature test, Playwright e2e (`HRM/e2e`).

**Spec:** `HRM/.plans/agent-chat/chat/gd12-nhom-du-an-kh/design.md` (Q1–Q15, §4.1–4.6, §7).

## Global Constraints

- Code đọc từ `origin/gop_db` (checkout `HRM/hrm-api`, `HRM/hrm-client` local đang chậm ~205 commit — **pull / chọn worktree trước**, hỏi user nhánh).
- **Chưa được code.** Trước khi bắt tay phải hỏi user câu riêng kèm phạm vi (repo · nhánh · file · migration) và nhận "làm".
- Migration duy nhất của GĐ12: `Modules/Assign/Database/Migrations/2026_11_20_000001_add_source_unique_to_workspaces.php` — chạy lẻ bằng `--path` vào DB local sau khi user cho phép.
- Không thêm quyền mới (không đụng Catalog).
- `source_type` chỉ nhận đúng 2 chuỗi: `prospective_project`, `solution`.
- `WorkspaceMember::ADDED_FROM_PROJECT = 4`, text "Từ dự án".
- Câu chữ: công tắc **"Là dự án KH"**; loại **"Dự án TKT"** / **"Xây dựng GP"**; cột **"Chức vụ ở màn manager"**; nút manager **"Nhóm trao đổi"**.
- Nhãn chức vụ TKT: `NVKD chính`, `Phụ trách GP`, `Hỗ trợ – <tên bộ phận>`; GP: `project_role_name` (nhiều ⇒ nối `, `; hạng mục ⇒ `<chức vụ> (<tên hạng mục>)`); PM GP không có dòng thành viên ⇒ `PM`.
- Tin hệ thống đóng / mở: `Dự án TKT <mã> đã đóng[ – <lý do>]`, `Dự án TKT <mã> đã mở lại`; GP: `Giải pháp <mã> đã đóng`, `Giải pháp <mã> đã mở lại`. (Không có tin hạ vai trò — bỏ đồng bộ liên tục.)
- FE: chỉ dùng `V2Base*`, popup `V2BaseModal`, select trong modal `V2BaseSelectInModal`, segmented `V2BaseSegmented`; nút ẩn hẳn khi không dùng được.
- Mọi task FE: kiểm bằng Playwright (đo DOM) trước khi báo xong; e2e chạy `--project=chromium --no-deps --workers=1`, đọc dòng tổng kết.
- Không đụng tin nhắn 12859 (nhóm 1612).

## Review Focus

1. Người tạo nhóm cũng có tên ở nguồn ⇒ vẫn là Quản lý, không bị thêm lại thành Thành viên / không 2 dòng (test ở Task 3).
2. Đổi nhân sự ở manager SAU khi tạo nhóm ⇒ nhóm không đổi, nhưng cột chức vụ hiện theo dữ liệu mới (test ở Task 3).
3. Nhân viên khác công ty được thêm vào nhóm vẫn mở được nhóm, nhiệm vụ, meeting khi **công ty đang chọn trong session là công ty của họ** (test ở Task 1 + e2e Task 10).
4. Nhiệm vụ tạo từ nhóm KH mà payload gửi `project_id` / `solution_id` **khác** đối tượng của nhóm ⇒ 422, không lặng lẽ ghi đè (test ở Task 4).
5. Dự án / GP đã đóng ⇒ tạo nhiệm vụ / meeting từ nhóm bị chặn 422, nhưng gửi tin nhắn vẫn được (test ở Task 4, Task 5).

---

### Task 1: Thành viên khác công ty (mọi loại nhóm) — BE

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Workspace/WorkspaceMemberService.php` (`eligibleIds`, `previewFromDepartments`)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/Workspace/WorkspaceMemberController.php` (`preview` nhận `company_id`)
- Modify: resource danh sách thành viên `Transformers/WorkspaceResource/WorkspaceMemberResource.php` — thêm `company_name` khi khác công ty nhóm
- Test: `Modules/Assign/Tests/Feature/Workspace/WorkspaceCrossCompanyTest.php` (mới) + sửa ca cũ trong `WorkspaceApiTest.php`, `HandoverWorkspaceAssigneeTest.php` đang khẳng định "khác công ty bị loại"

**Interfaces:**
- Produces: `eligibleIds(array $employeeIds): array` (bỏ tham số công ty — chỉ lọc đang làm việc); `previewFromDepartments(int $companyId, …)` giữ chữ ký, `$companyId` giờ là công ty user chọn ở popup (mặc định công ty nhóm).

- [x] Viết test: `test_add_member_from_other_company_succeeds`, `test_inactive_employee_still_rejected`, `test_preview_departments_of_other_company`, `test_other_company_member_can_open_workspace_and_task` (đăng nhập NV công ty B, nhóm công ty A, GET `/v1/assign/workspaces/{id}` + task của nhóm ⇒ 200).
- [x] Chạy ⇒ FAIL.
- [x] Sửa `eligibleIds` + mọi chỗ gọi (`add`, `previewFromDepartments`, `ensureAssigneeForHandover`); controller `preview` validate `company_id` nullable integer.
- [x] Rà `WorkspaceAccess`, `CheckWorkspaceAccess`, `TaskAccess`, `WorkspaceMeetingService::visibleQuery` xem có lọc theo công ty session không; có thì nới cho thành viên nhóm. Ghi kết quả rà vào report.
- [x] Chạy cả thư mục `Tests/Feature/Workspace` ⇒ PASS.

### Task 2: Tạo nhóm "Là dự án KH" + API chọn đối tượng + nút manager — BE

**Files:**
- Create: migration `2026_11_20_000001_add_source_unique_to_workspaces.php` — unique `(source_type, source_id)` (MySQL cho nhiều NULL).
- Modify: `Entities/Workspace/Workspace.php` — hằng `SOURCE_PROSPECTIVE_PROJECT = 'prospective_project'`, `SOURCE_SOLUTION = 'solution'`, `isKhProject(): bool`, quan hệ `sourceProject()`, `sourceSolution()`.
- Modify: `Entities/Workspace/WorkspaceMember.php` — `ADDED_FROM_PROJECT = 4` + text.
- Modify: `Http/Requests/Workspace/StoreWorkspaceRequest.php` — `kh_source_type` nullable `in:prospective_project,solution`, `kh_source_id` `required_with:kh_source_type|integer`; `enabled_tabs.*` không nhận `issues` khi có `kh_source_type`.
- Create: `Services/Workspace/KhProjectSourceService.php`.
- Modify: `Services/Workspace/WorkspaceService.php::create` — có nguồn ⇒ kiểm qua `KhProjectSourceService::assertLinkable`, `company_id` = công ty của đối tượng, lưu `source_*`, rồi gọi `KhProjectMemberSource::seed` (Task 3) trong cùng transaction.
- Modify: `Routes/Chat/api.php` (nhóm `v1/assign/workspaces`) — `GET /kh-sources`, `GET /kh-group`.
- Modify: `WorkspaceResource` — trả `source_type`, `source_id`, `source_code`, `source_name`, `source_url`.
- Test: `Tests/Feature/Workspace/WorkspaceKhSourceTest.php`.

**Interfaces:**
- `KhProjectSourceService::assertLinkable(string $type, int $id, int $actorId): array` ⇒ `['company_id'=>int,'code'=>string,'name'=>string]`; 422 trên `kh_source_id` với các câu: `Chỉ NVKD chính của dự án được gắn nhóm.` / `Chỉ PM của giải pháp được gắn nhóm.` / `Dự án cha không gắn nhóm được.` / `Đối tượng đã đóng.` / `Đối tượng này đã có nhóm trao đổi.` (báo đồng thời).
- `KhProjectSourceService::linkable(string $type, int $actorId, int $companyId, ?string $q): array` — tối đa 20, `{id, code, name}`, chỉ đối tượng actor phụ trách, chưa có nhóm, chưa đóng, TKT không phải dự án cha.
- `KhProjectSourceService::isClosed(string $type, int $id): bool` — TKT: `closed_at` not null hoặc status ∈ {`STATUS_DONG_DU_AN`, `STATUS_KET_THUC_VA_LUU_TRU`}; GP: `Solution::STATUS_DONG`.
- `GET /kh-group?source_type=&source_id=` ⇒ `{workspace_id|null, is_member: bool, can_create: bool}` (`can_create` = chưa có nhóm && actor là người phụ trách && linkable).

- [x] Viết test cho: tạo hợp lệ (TKT, GP); người không phụ trách ⇒ 422; dự án cha ⇒ 422; đã có nhóm ⇒ 422; đã đóng ⇒ 422; `kh-sources` chỉ trả đối tượng đúng điều kiện; `kh-group` 3 trạng thái.
- [x] FAIL → code → PASS. Migration chỉ chạy sau khi user cho phép (`migrate --path=…2026_11_20_000001…`).

### Task 3: Nguồn nhân sự — thêm 1 lần lúc tạo + cột chức vụ — BE

**Files:**
- Create: `Services/Workspace/KhProjectMemberSource.php`
- Modify: `WorkspaceMemberService::list` / `WorkspaceMemberResource` — thêm `manager_role_label` (tính lúc đọc, gom 1 lần cho cả danh sách — không N+1; null với nhóm thường / người không ở nguồn).
- Test: `Tests/Feature/Workspace/KhProjectMemberSourceTest.php`.

**Interfaces:**
- `KhProjectMemberSource::members(string $type, int $id): array` ⇒ `[employee_id => label]` theo bảng nhãn ở Global Constraints; GP chỉ lấy dòng thành viên đang hiệu lực (đọc hằng trong `SolutionMember` / `SolutionModuleMember` để chốt điều kiện `status`, `end_date`).
- `KhProjectMemberSource::seed(Workspace $ws, int $actorId): int[]` — thêm mọi người ở nguồn (trừ người đã có trong nhóm, gồm người tạo) qua `WorkspaceMemberService::add($ws, $ids, WorkspaceMember::ADDED_FROM_PROJECT, $actorId, [], ROLE_MEMBER)`; trả id đã thêm. Chỉ gọi từ `WorkspaceService::create`.

- [x] Test: tạo nhóm TKT ⇒ NVKD chính, phụ trách GP, NV hỗ trợ vào nhóm vai trò Thành viên, `added_via = 4`; nhóm GP ⇒ thành viên GP + hạng mục đang hiệu lực + PM, người hết hiệu lực không vào; người tạo có tên ở nguồn ⇒ vẫn Quản lý, 1 dòng; NV nghỉ việc ở nguồn ⇒ bỏ qua; đổi `SolutionMember` sau khi tạo ⇒ thành viên nhóm không đổi nhưng `manager_role_label` đổi theo; nhãn đúng cho TKT / GP / hạng mục / PM.
- [x] FAIL → code → PASS.

### Task 4: Nhiệm vụ của nhóm KH — BE

**Files:**
- Modify: `Services/Workspace/WorkspaceTaskRules.php` — `MSG_EXCLUSIVE` không áp khi nhóm `isKhProject()` và `project_id`/`solution_id` khớp nguồn; lệch nguồn ⇒ 422 `workspace_id`: `Nhiệm vụ phải thuộc đúng dự án / giải pháp của nhóm.`; nguồn đã đóng ⇒ 422 `Dự án / giải pháp của nhóm đã đóng, không tạo nhiệm vụ mới.`
- Modify: `Services/TaskService.php` — tạo có `workspace_id` của nhóm KH mà không gửi `project_id`/`solution_id` ⇒ tự điền: TKT ⇒ `project_id`; GP ⇒ `solution_id`, `project_id` = `solutions.prospective_project_id`, `solution_version_id`/`code` = version hiện hành.
- Modify: `Services/Workspace/WorkspaceTaskListService.php::baseQuery` — nhóm KH: TKT ⇒ cùng điều kiện tab Nhiệm vụ manager TKT (`GET assign/tasks` với `project_id`, đọc filter đó trong `TaskService` và dùng lại, không viết lại); GP ⇒ `tasks.solution_id`. Giữ luật ẩn Nháp của người khác. `suggest` cũng theo phạm vi này.
- Modify: `Services/Task/TaskAccess.php::canView` — thêm: là thành viên nhóm KH có nguồn khớp `task.project_id` (TKT) / `task.solution_id` (GP) ⇒ xem được (đặt trước nhánh `solution`/`project`).
- Test: `Tests/Feature/Workspace/WorkspaceKhTaskTest.php`.

- [x] Test: tạo từ nhóm TKT ⇒ `project_id` tự điền, hiện ở `GET assign/tasks?project_id=`; tạo từ nhóm GP ⇒ `solution_id`+version tự điền; gửi `project_id` khác ⇒ 422; nguồn đóng ⇒ 422; nhiệm vụ tạo ở manager (không `workspace_id`) hiện ở tab nhóm; thành viên nhóm thêm tay xem được chi tiết nhiệm vụ dự án; nhóm thường vẫn giữ `MSG_EXCLUSIVE`.
- [x] FAIL → code → PASS.

### Task 5: Meeting của nhóm KH — BE

**Files:**
- Modify: `Services/Workspace/WorkspaceMeetingService.php` — `assertCanCreateIn` chặn khi nguồn đóng (câu như Task 4, chữ "meeting"); `visibleQuery` nhóm KH: meeting có dòng `prospective_project_meetings` khớp (TKT: `prospective_project_id`; GP: `solution_id`) HOẶC `meetings.workspace_id` = nhóm.
- Modify: `Services/MeetingService.php` — tạo meeting có `workspace_id` nhóm KH ⇒ bảo đảm có dòng liên kết qua `createProspectiveProjectMeeting` (TKT: dự án; GP: dự án của GP + `solution_id`), kể cả khi payload không gửi khối dự án.
- Rà quyền xem chi tiết meeting (service/policy đang dùng cho `meetings/{id}`) — thành viên nhóm KH xem được meeting thuộc nguồn; ghi kết quả rà vào report.
- Test: `Tests/Feature/Workspace/WorkspaceKhMeetingTest.php`.

- [x] Test: tạo từ nhóm TKT ⇒ có dòng `prospective_project_meetings`, hiện ở tab Meeting manager TKT; nhóm GP ⇒ dòng có `solution_id`; meeting tạo ở manager hiện trong nhóm; nguồn đóng ⇒ 422; nhóm thường không đổi hành vi.
- [x] FAIL → code → PASS.

### Task 6: Tin hệ thống khi dự án / GP đóng – mở lại — BE

**Files:**
- Create: `Observers/Workspace/KhProjectStatusObserver.php` — đăng ký trên `ProspectiveProject`, `Solution`: `ProspectiveProject` / `Solution` chuyển trạng thái đóng ↔ mở (`KhProjectSourceService::isClosed` trước/sau) ⇒ gửi tin `system` vào nhóm KH qua cơ chế tin hệ thống đang dùng cho `WorkspaceActivity`.
- Test: `Tests/Feature/Workspace/KhProjectStatusMessageTest.php`.

- [x] Test: đóng TKT có lý do ⇒ 1 tin đúng câu; lưu lại TKT đã đóng mà không đổi trạng thái ⇒ không tin mới; mở lại ⇒ tin "mở lại"; nhóm không tự đóng.
- [x] FAIL → code → PASS.

### Task 7: Chọn người khác công ty — FE

**Files:**
- Modify: `hrm-client/utils/chat/workspaceOptions.js::employeeOptions` — nguồn NV mọi công ty (đọc API / store đang cấp dữ liệu, nếu store chỉ có công ty hiện tại thì chuyển sang search server-side có `limit`); NV khác công ty nhóm ⇒ hậu tố ` · <tên công ty>` sau khuôn `Tên - Mã phòng - Mã NV`.
- Modify: `components/chat/workspace/DepartmentPickModal.vue` — thêm `V2BaseSelectInModal` "Công ty" (mặc định công ty nhóm), gửi `company_id` lên preview.
- Modify: `AddMembersModal.vue`, `CreateWorkspaceModal.vue` — dùng options mới.

- [x] Playwright: thêm NV công ty khác vào nhóm qua 2 đường (chọn người, lấy từ phòng ban) — đếm option có hậu tố công ty, đọc lại danh sách thành viên.

### Task 8: Form tạo nhóm "Là dự án KH" — FE

**Files:**
- Modify: `components/chat/workspace/CreateWorkspaceModal.vue` — công tắc "Là dự án KH"; bật ⇒ `V2BaseSegmented` Dự án TKT / Xây dựng GP + `V2BaseSelectInModal` gọi `GET /v1/assign/workspaces/kh-sources` (debounce 300ms); chọn xong gợi ý tên `<mã> – <tên>` nếu ô tên đang trống; ẩn lựa chọn tab Vấn đề; prop `presetSource {type,id,code,name}` để mở từ manager (khoá công tắc + đối tượng). Lỗi 422 hiện tại ô.
- Modify: `components/chat/workspace/SettingsPanel.vue` / header nhóm — hiện "Dự án KH: <mã – tên>" dạng link tới manager (không sửa được).

- [x] Playwright: tạo nhóm TKT + GP bằng tài khoản phụ trách; tài khoản không phụ trách ⇒ danh sách đối tượng rỗng; đo không ô lẻ hàng (bố cục 12 cột).

### Task 9: Cột chức vụ + tab Nhiệm vụ / Meeting nhóm KH — FE

**Files:**
- Modify: `components/chat/workspace/MembersPanel.vue` — cột "Chức vụ ở màn manager" (`manager_role_label`, trống thì để trống), chỉ hiện ở nhóm KH; nhãn "Từ dự án" cho `added_via = 4`.
- Modify: form tạo nhiệm vụ / meeting khi mở từ nhóm KH (`TaskPanel.vue` nhận `workspace_id`; khối dự án / GP hiện sẵn đối tượng của nhóm, khoá) — không đổi luồng 19 màn cũ.
- `WorkspaceView.vue`: không thêm panel Vấn đề.

- [x] Playwright: tab Nhiệm vụ nhóm TKT có cả việc tạo ở manager; tạo nhiệm vụ trong nhóm ⇒ mở manager TKT thấy dòng mới; cột chức vụ đúng nhãn.

### Task 10: Nút "Nhóm trao đổi" ở màn manager + e2e — FE

**Files:**
- Modify: `pages/assign/prospective-projects/_id/manager.vue`, `pages/assign/solutions/_id/manager.vue` — gọi `GET /kh-group` (lazy, 1 request); `workspace_id` + `is_member` ⇒ nút mở nhóm trong ngăn chat; `can_create` ⇒ nút mở `CreateWorkspaceModal` với `presetSource`; còn lại ẩn nút.
- Create: `HRM/e2e/tests/assign/workspace-kh-project.spec.ts` — ca: K1 tạo nhóm TKT từ manager; K2 tạo nhóm GP ⇒ thành viên GP vào nhóm, cột chức vụ đúng; K3 Quản lý gỡ / thêm tay thành viên nhóm KH; K4 tạo nhiệm vụ trong nhóm hiện ở manager; K5 người không phụ trách không thấy nút; K6 NV công ty khác vào nhóm mở được; K7 đóng TKT ⇒ tin hệ thống + không tạo nhiệm vụ được. `afterAll` dọn nhóm test.

- [x] Chạy TOÀN BỘ e2e chat liên quan (`bug-report`, workspace spec cũ, spec mới) — đọc dòng tổng kết.

---

### Checkpoint — 14/11/2026
Vừa hoàn thành: design.md chốt Q1–Q15; plan.md viết xong; 14/11 đổi Q2 ⇒ chỉ thêm nhân sự 1 lần lúc tạo (bỏ observer + lệnh định kỳ).
Đang làm dở: —
Bước tiếp theo: user duyệt plan + chọn cách chạy; hỏi "làm" kèm phạm vi (repo · nhánh · migration `2026_11_20_000001`).
Blocked: chưa có lệnh code.

### Checkpoint — 15/11/2026 rạng sáng (wrap up)
Vừa hoàn thành: GĐ12 CODE XONG cả 10 task (SDD: mỗi task 1 implementer + review, final review opus + 1 lượt sửa). Nhánh `gop_db-chat-nhom-du-an-kh` (worktree `wt-nhom-trao-doi`, api + client) — CHƯA commit. Migration `2026_11_20_000001_add_source_unique_to_workspaces` ĐÃ chạy db_gop_6_11 (batch 507).
Kiểm: PHPUnit `Tests/Feature/Workspace` 226 OK + `Tests/Feature/Task` 31 OK · e2e `workspace-kh-project` 7/7 (spec tự gán/trả NVKD chính #273 + PM GP#37) · `workspace-tasks` 12/12 · `workspace-meetings` 5/5 · `chat-core` 8/8 · `bug-report` 8/8 (cần role tạm cấp quyền assign.bao_loi_cai_dat.manage cho NV 13 — đã gỡ).
Ruling Claude cần user soát (chi tiết ledger-sdd.md):
  1. Nhóm KH đóng / tự lưu trữ KHÔNG huỷ việc của dự án; việc của nhóm KH đã đóng vẫn sửa được (không 423) — theo anti-goal §2.
  2. Tin đóng/mở Dự án TKT gửi cả nhóm TKT + nhóm GP (cascade đóng GP bằng update hàng loạt không bắn event; không sửa service dùng chung).
  3. Nhóm GP lọc meeting theo dự án của GP (như tab Meeting manager GP).
  4. Nhóm KH giữ type = Nhóm trao đổi, đánh dấu bằng source_type/source_id.
  5. Sửa file dùng chung `components/BasicSubsystem.vue` (+6 dòng watch mở ngăn chat từ trang khác).
  6. Manager GP (layout:false) ⇒ nút mở nhóm ở tab mới `/assign/workspaces/{id}`; manager TKT mở ngăn trượt.
Đang làm dở: —
Bước tiếp theo: user thử trên :3080 (worktree wt-nhom-trao-doi) → báo commit/push gop_db → deploy TPE (migration 2026_11_20_000001).
Blocked: —
Ngoài luồng (note, chưa sửa): `tasks.solution_id` không có index · `ProspectiveProjectVisibleIdsTest` lỗi FK roles có sẵn · link "Dự án KH" đầu nhóm có thể 403 với thành viên không có quyền xem dự án · NV công ty đã ngừng HĐ không có hậu tố tên công ty.
