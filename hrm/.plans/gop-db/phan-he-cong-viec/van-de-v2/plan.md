# Vấn đề v2 (web panel) + tab Vấn đề trong Nhóm trao đổi — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay popup `CreateIssueModal` bằng `IssuePanel` theo khuôn `TaskPanel` (nút hành động theo vai trò, sửa 1 trường, gia hạn, theo dõi, thông báo các bước), rồi thêm tab Vấn đề vào Nhóm trao đổi.

**Architecture:** BE thêm 1 cửa kiểm truy cập `IssueAccess`, mở rộng `PATCH /issues/{id}/status` thành điểm đổi trạng thái duy nhất (kèm dữ liệu từng bước), thêm PATCH 1 trường / watch / tệp / gia hạn theo đúng khuôn route + service của Nhiệm vụ v2. FE dựng `components/assign/issue/panel/*` bám `components/assign/task/panel/*`, giữ chữ ký `open(...)` của popup cũ để 13 chỗ gọi chỉ đổi import. Phase 3 gắn `issues.workspace_id` + dựng danh sách gom nhóm theo khuôn `TaskGroupListView`.

**Tech Stack:** Laravel 8 (PHP 8.1 local: `/opt/homebrew/opt/php@8.1/bin/php`), PHPUnit; Nuxt 2 / Vue 2, bootstrap-vue, V2Base*; Playwright (Node 20).

**Spec:** `.plans/gop-db/phan-he-cong-viec/van-de-v2/design.md` (đọc kèm; mã quyết định V1–V17, mục §4.x).

## Global Constraints

- Code ở worktree `websites/wt-nhom-trao-doi`, nhánh mới `gop_db-van-de-v2` tách từ `origin/gop_db` ở **cả** `hrm-api` và `hrm-client`. Không tự merge gop_db. **Chưa được phép code — phải hỏi user phạm vi trước (CLAUDE.md root).**
- Migration chạy vào DB local `db_gop_6_11` chỉ khi user cho phép, chạy lẻ bằng `--path`, `.env` worktree `APP_ENV=production` ⇒ cần `--force`.
- PHPUnit Assign: `php -d memory_limit=1G vendor/bin/phpunit Modules/Assign/Tests/Feature/Issue` (php 8.1).
- Model mới `extends BaseModel`; message validate theo lang file (không khai `messages()` cho rule phổ biến); `created_by`/`updated_by` = `auth()->id()`.
- Nhãn hiển thị "Vấn đề"; mã/API giữ chữ `issue`. Màu trạng thái/ưu tiên do BE trả (`Issue::STATUS_DATA`, `PRIORITY_DATA`), FE không map.
- Thông báo theo skill `notification-convention`, dựng bằng `IssueService::issueNotification()` có sẵn; url `/assign/issues?open_issue={id}`.
- FE: mọi ô form `V2Base*` (select trong panel/modal ⇒ `V2BaseSelectInModal`), nút theo `button-convention`, nút không dùng được thì **ẩn** (không disable), select nhân viên dùng `employeeOptionText`, xác nhận dùng `$confirm`.
- Mọi bước FE kiểm bằng Playwright MCP đo DOM (`http://127.0.0.1:3080`, API `:8080` của worktree) trước khi báo xong; e2e `serial` đọc dòng tổng kết.
- Không đổi API danh sách / export / cấu hình cột của `/assign/issues` (V3). `PATCH /status` với body cũ `{status, reason}` phải chạy như cũ.
- Hằng nhân viên test (giống `TaskV2ApiTest`): CREATOR = 13, ASSIGNEE = 50, OTHER = 34; thêm LEAD = trưởng của 1 bộ phận có thật trong `db_gop_6_11` (Task 1 tra và ghi lại id).

## Review Focus

1. **Người tạo đồng thời là người phụ trách / trưởng đơn vị** — nút không nhân đôi, không tự gửi thông báo cho chính mình, đề nghị gia hạn không gửi được cho chính mình (người tạo = người phụ trách ⇒ đổi hạn trực tiếp). Test ở Task 3, 5, 6.
2. **Vấn đề cũ có `status` lệch luật** (vd `resolved` mà không có người duyệt, `new` đã có người phụ trách) — panel vẫn mở, hiện đúng nút BE trả, không lỗi JS. Test ở Task 3 (`test_resolved_khong_nguoi_duyet_van_tra_buoc_hop_le`) + Task 9 (mở vấn đề stub status lạ).
3. **Mở panel từ trong b-modal** (`IssueUpcomingModal`, `WorkDrillModal`, màn bàn giao) — panel nằm trên modal, bấm nền không đóng nhầm modal cha. Đo z-index ở Task 11.
4. **Sửa vấn đề có tệp chứng cứ** — Lưu form Sửa không xoá tệp `issue_resolutions`. Test ở Task 5.
5. **Người ngoài phạm vi gọi API mới** (watch, field, status, tệp, gia hạn) ⇒ 403, không ghi gì. Test ở Task 2.

---

## Phase 1 — BE `hrm-api`

### Task 1: Migration + model gia hạn + `IssueAccess`

**Files:**
- Create: `Modules/Assign/Database/Migrations/2026_11_23_000001_issue_v2_resolution_text_and_extension_requests.php` — `issues.resolution` → `text` nullable; tạo `issue_extension_requests` (cột như `task_extension_requests` thay `task_id` ⇒ `issue_id`; index `(issue_id, status)`).
- Create: `Modules/Assign/Entities/IssueExtensionRequest.php` (copy khuôn `Entities/Task/TaskExtensionRequest.php`: hằng `STATUS_PENDING=1 … STATUS_CANCELLED=4`, `STATUSES` màu chuẩn, quan hệ `issue()`, `requester()` theo `created_by`).
- Create: `Modules/Assign/Services/Issue/IssueAccess.php`
- Modify: `Modules/Assign/Services/IssueService.php` — tách `public function visibleQuery(): Builder` (query danh sách + `applyPermissionScope`, dùng lại trong `index`).
- Modify: `Modules/Assign/Entities/Issue.php` — `extensionRequests()` hasMany, `pendingExtension()` hasOne status=1, `resolutionFiles()` hasMany `File` `table='issue_resolutions'`.
- Test: `Modules/Assign/Tests/Feature/Issue/IssueV2ApiTest.php` (tạo mới, `DatabaseTransactions` + `GrantsLeaderSchedulePermission::actAs`, helper `makeIssue(array $over = []): int` chèn thẳng `issues` như `TaskV2ApiTest::makeTask`).

**Interfaces:**
- Produces: `IssueAccess::canView(Issue $issue, int $employeeId): bool` (chỉ cho người đang đăng nhập, như `TaskAccess::canView`) = `IssueService::visibleQuery()->whereKey($id)->exists()` OR (vấn đề gắn GP mà `Solution::visibleIdsQuery()` chứa) OR (vấn đề gắn TKT mà `ProspectiveProject::visibleIdsQuery()` chứa) OR (Phase 3: thành viên nhóm). `IssueAccess::assertView(?Issue)` ⇒ `abort(403, 'Bạn không có quyền xem vấn đề này.')`. `IssueAccess::assertWritable(?Issue)` = `assertView` (Phase 3 thêm 423 nhóm đóng).
- Produces: `Issue::handlingLeadId(): ?int` — `employees.id` trưởng bộ phận (`parts.part_lead_id`), không có thì trưởng phòng (`departments.department_lead_id`); `Issue::isHandlingLead(): bool` so với `auth()->id()`.

- [ ] Step 1: Tra `db_gop_6_11` 1 bộ phận có `part_lead_id` ≠ 13/50/34 (script php bootstrap), ghi id vào hằng `LEAD` + `LEAD_PART`, `LEAD_DEPT` của test.
- [ ] Step 2: Viết test `test_nguoi_ngoai_pham_vi_khong_xem_duoc_qua_issue_access` (vấn đề của CREATOR giao ASSIGNEE, `actAs(OTHER)` không quyền xem cấp ⇒ `canView` false; `actAs(ASSIGNEE)` ⇒ true) và `test_truong_don_vi_xu_ly_tra_dung_nguoi` (`handling_part_id = LEAD_PART` ⇒ `handlingLeadId() === LEAD`; bộ phận không trưởng ⇒ lùi trưởng phòng).
- [ ] Step 3: Chạy ⇒ FAIL (class chưa có).
- [ ] Step 4: Viết migration, model, `visibleQuery`, `IssueAccess`, 2 hàm trên `Issue`.
- [ ] Step 5: **Hỏi user cho chạy migration `2026_11_23_000001` vào `db_gop_6_11`** (liệt kê `migrate:status` + `--pretend`), được phép thì chạy `--path … --force`.
- [ ] Step 6: Chạy test ⇒ PASS. Commit `feat(issue): IssueAccess + bảng đề nghị gia hạn vấn đề + resolution text`.

### Task 2: Vá store / PUT + chặn API mới theo `IssueAccess`

**Files:**
- Modify: `Modules/Assign/Http/Requests/Issue/IssueStoreRequest.php` — `status` `nullable|in:new,assigned`; `assigned` ⇒ `assignee_id` required; thêm `due_date|date`, `detected_at|date`, `approver_id|exists:employees,id`, `watcher_ids.*`/`supporter_ids.*` `exists:employees,id`.
- Modify: `Modules/Assign/Services/IssueService.php::store` — chỉ `create` từ whitelist `Issue::$fillable` trừ `completed_at, resolved_at, closed_at, rejected_at, rejected_reason, closed_reason, resolution, root_cause_group`; status suy theo người nhận khi trống (U36: có `assignee_id` ⇒ `assigned`, không ⇒ `new`).
- Modify: `IssueService::update` + `IssueController::update` — chỉ người `canEdit()` (khác ⇒ 403 `abort` ngoài try/catch); bỏ `status`, `assignee_id` khỏi dữ liệu ghi (đổi trạng thái/người chỉ qua Task 3); `syncForTable('issues', …)` giữ nguyên (không đụng `issue_resolutions`).
- Modify: `Modules/Assign/Entities/Issue.php::canHandle` — người phụ trách ở `new`; người `isHandlingLead()` ở `new` / `reopened`.
- Test: `IssueV2ApiTest.php`

- [ ] Step 1: Viết test: `test_post_khong_tao_thang_hoan_thanh` (status=completed ⇒ 422), `test_post_co_nguoi_phu_trach_thi_da_phan_cong` (không gửi status ⇒ `assigned`), `test_post_chi_phong_ban_thi_moi_ghi_nhan`, `test_put_nguoi_phu_trach_bi_chan_403` (ASSIGNEE PUT `title` ⇒ 403, title giữ nguyên, `watcher_ids` không đổi), `test_put_nguoi_tao_khong_doi_duoc_trang_thai` (CREATOR PUT `status=completed` ⇒ 200 nhưng status giữ), `test_nguoi_phu_trach_nhan_xu_ly_tu_moi_ghi_nhan` (`canHandle` true ở `new`).
- [ ] Step 2: Chạy ⇒ FAIL. Step 3: sửa code. Step 4: chạy cả `Modules/Assign/Tests` liên quan Issue ⇒ PASS.
- [ ] Step 5: Commit `fix(issue): store/PUT chỉ nhận đúng trạng thái + người được sửa (V10)`.

### Task 3: `PATCH /status` đủ bước + đổi người phụ trách + trả cờ cho panel

**Files:**
- Modify: `Modules/Assign/Http/Requests/Issue/IssueUpdateStatusRequest.php` — luật theo đích:
  - `assigned`: `assignee_id required|exists:employees,id`, `reason nullable|string|max:1000`
  - `resolved`/`completed` khi người phụ trách báo xong: `resolution required|string`, `root_cause_group required|in:<9 giá trị DetailIssueResource::ENUM_MAPS>`, `attachments nullable|array` (khuôn tệp như store)
  - `rejected`: `reason required`; `closed`, `reopened`: `reason nullable|string|max:1000`.
- Modify: `Modules/Assign/Entities/Issue.php::getAllowedNextStatuses` — `new`/`reopened` ⇒ `assigned` cho người tạo **hoặc** `isHandlingLead()`; thêm `assigned` (đổi người) ở `assigned/in_progress/rejected/reopened` cho người tạo, trưởng đơn vị, người phụ trách; giữ nguyên các nhánh khác.
- Modify: `IssueService::changeStatus(Issue $issue, string $status, array $data): Issue` (đổi chữ ký — sửa mọi chỗ gọi): kiểm `allowed_next_statuses`; `assigned` ⇒ ghi `assignee_id`, xoá `rejected_at/rejected_reason`, huỷ đề nghị gia hạn đang chờ; `resolved`/`completed` từ `in_progress` ⇒ ghi `resolution`, `root_cause_group`, `resolved_at`, tệp vào `table='issue_resolutions'`; `closed` ⇒ `closed_reason`; ghi lịch sử kèm `note = reason`; huỷ gia hạn đang chờ khi sang `resolved/completed/closed`; gọi thông báo Task 6.
- Modify: `IssueController::updateStatus` — `IssueAccess::assertWritable` đầu hàm.
- Modify: `Modules/Assign/Transformers/IssueResource/DetailIssueResource.php` — thêm `status_text`, `status_color`, `priority_color`, `is_watching`, `is_handling_lead`, `pending_extension` ({id, new_due_date, new_due_time, reason, requested_by_name, created_at}), `can_request_extension`, `can_decide_extension`, `resolution`, `root_cause_group(_text)`, `resolution_files[]`, `closed_reason`; `allowed_next_statuses[]` mỗi phần tử thêm `requires: 'assignee'|'resolution'|'reason'|'reason_optional'|null` (quyết §4.3 cuối: **BE trả `requires`**).
- Test: `IssueV2ApiTest.php`

- [ ] Step 1: Viết test (mỗi test 1 bước): `test_truong_don_vi_phan_cong_vay_moi_ghi_nhan`, `test_nguoi_ngoai_khong_phan_cong_duoc_422`, `test_bao_da_xu_ly_thieu_cach_xu_ly_422`, `test_bao_da_xu_ly_co_nguoi_duyet_sang_resolved_luu_tep_rieng` (assert `files.table='issue_resolutions'`), `test_bao_da_xu_ly_khong_nguoi_duyet_sang_completed`, `test_nguoi_phu_trach_tu_chuyen_viec_ve_da_phan_cong` (in_progress ⇒ assigned, assignee mới, gia hạn chờ ⇒ huỷ), `test_doi_nguoi_khi_da_hoan_thanh_bi_chan`, `test_dong_luu_ly_do`, `test_body_cu_status_reason_van_chay` (rejected + reason như trước), `test_resolved_khong_nguoi_duyet_van_tra_buoc_hop_le`, `test_chi_tiet_tra_requires_cho_tung_buoc`.
- [ ] Step 2: FAIL ⇒ Step 3: code ⇒ Step 4: PASS cả file.
- [ ] Step 5: Commit `feat(issue): PATCH status đủ bước (phân công, báo xử lý, đổi người, đóng) + cờ panel`.

### Task 4: PATCH 1 trường + theo dõi

**Files:**
- Create: `Modules/Assign/Http/Requests/Issue/IssueFieldUpdateRequest.php` — `FIELDS = ['title'=>['title'], 'description'=>['description'], 'issue_type'=>…, 'priority'=>…, 'impact_level'=>…, 'detected_from'=>…, 'due'=>['due_date','due_time','reason'], 'approver_id'=>…, 'handling_unit'=>['handling_department_id','handling_part_id'], 'link'=>['solution_id','project_id','module_id'], 'task_id'=>…, 'watchers'=>['watcher_ids'], 'supporters'=>['supporter_ids'], 'tags'=>…, 'sla'=>…, 'detected'=>['detected_by','detected_at'], 'impact'=>['affect_schedule','affect_quality','affect_customer','impact_note'], 'handle_plan'=>…, 'close_condition'=>…]` (không có `assignee_id`, `status`). Luật mỗi trường như Store.
- Create: `Modules/Assign/Http/Requests/Issue/IssueWatchRequest.php` (`watch required|boolean`).
- Modify: `IssueService` — `updateField(Issue $issue, Request $r): Issue` (chỉ `canEdit()`, ghi lịch sử từng trường; `handling_unit` khi chưa có người phụ trách ⇒ `notifyHandlingDepartmentLead`; `due` kèm `reason` vào ghi chú lịch sử), `toggleWatch(Issue $issue, bool $watch): void` (bảng `issue_watchers`, ghi lịch sử).
- Modify: `IssueController` — `updateField`, `watch` (đều `IssueAccess::assertWritable` đầu hàm, rethrow `ValidationException|HttpExceptionInterface`).
- Modify: `Modules/Assign/Routes/api.php` nhóm `/assign/issues`: thêm **trước** `/{issue}`: `Route::patch('/{issue}/field', …updateField)`, `Route::post('/{issue}/watch', …watch)`.
- Test: `IssueV2ApiTest.php`

- [ ] Step 1: Test `test_patch_nguoi_tao_doi_ten_ghi_lich_su`, `test_patch_nguoi_phu_trach_bi_chan_403`, `test_patch_truong_khong_ho_tro_422` (`field=assignee_id`), `test_patch_doi_han_kem_ly_do_vao_lich_su`, `test_tu_theo_doi_va_bo_theo_doi`, `test_nguoi_ngoai_pham_vi_khong_theo_doi_duoc_403`.
- [ ] Step 2–4: FAIL ⇒ code ⇒ PASS. Step 5: Commit `feat(issue): sửa 1 trường + tự theo dõi`.

### Task 5: Tệp sau khi tạo

**Files:**
- Modify: `IssueService` — `addAttachments(Issue $issue, array $files): Collection` (`table='issues'`, `created_by` = mình), `removeAttachment(Issue $issue, int $fileId): void` (người tạo xoá mọi tệp; người khác chỉ tệp `created_by` = mình; không xoá tệp `issue_resolutions`).
- Modify: `IssueController` — `storeAttachments`, `destroyAttachment`; quyền: người tạo / người phụ trách / trưởng đơn vị, vấn đề chưa `closed/completed`, + `IssueAccess::assertWritable`.
- Modify: routes: `Route::post('/{issue}/attachments', …)`, `Route::delete('/{issue}/attachments/{file}', …)`.
- Test: `IssueV2ApiTest.php`

- [ ] Step 1: Test `test_nguoi_phu_trach_them_tep_sau_khi_tao`, `test_nguoi_phu_trach_khong_xoa_tep_nguoi_khac_403`, `test_nguoi_ngoai_khong_them_tep_403`, `test_sua_form_khong_xoa_tep_chung_cu` (vấn đề có 1 tệp `issue_resolutions`, CREATOR PUT `attachments=[]` ⇒ tệp chứng cứ còn).
- [ ] Step 2–4. Step 5: Commit `feat(issue): thêm / xoá tệp sau khi tạo, tách tệp chứng cứ`.

### Task 6: Thông báo các bước (V14)

**Files:**
- Modify: `IssueService` — thêm `notifyAssigned(Issue $issue, ?string $reason)` (người phụ trách mới; gọi ở store có `assignee_id` và bước `assigned`), `notifyCreatorStarted(Issue)` (Nhận xử lý ⇒ người tạo), `notifyCompleted(Issue)` (⇒ người tạo + người phụ trách), `notifyClosedOrReopened(Issue, string $action, ?string $reason)` (⇒ người tạo + người phụ trách + người duyệt); helper `notifyEmployees(array $employeeIds, array $payload)` bỏ `auth()->id()` và trùng. Nhãn hành động (cột 2 của template): `Giao xử lý`, `Nhận xử lý`, `Hoàn thành`, `Đã đóng`, `Mở lại` — đối chiếu bảng nhóm hành động trong skill `notification-convention`, lệch thì theo skill.
- Test: `IssueV2ApiTest.php` — đếm bảng `notifications` (hoặc fake `EmployeeInfoService::sendNotification` nếu bảng đếm khó; xem cách test thông báo của Nhiệm vụ v2 gia hạn) — **stub push FCM trước khi chạy** ([[rehearsal-gui-push-that]]).

- [ ] Step 1: Test `test_giao_dich_danh_bao_nguoi_phu_trach`, `test_nhan_xu_ly_bao_nguoi_tao`, `test_hoan_thanh_bao_ca_hai_tru_nguoi_bam`, `test_nguoi_tao_tu_giao_minh_khong_tu_bao`.
- [ ] Step 2–4. Step 5: Commit `feat(issue): thông báo giao xử lý / nhận / hoàn thành / đóng / mở lại`.

### Task 7: Đề nghị gia hạn (V4/V11)

**Files:**
- Create: `Modules/Assign/Services/IssueExtensionService.php` — copy khuôn `TaskExtensionService` (`request(Issue, array): IssueExtensionRequest`, `approve`, `reject(ext, string)`, `cancel`, `cancelPending(Issue, string $note)` dùng ở Task 3).
- Create: `Modules/Assign/Http/Requests/Issue/IssueExtensionStoreRequest.php` (`new_due_date required|date|after_or_equal:today`, `new_due_time nullable`, `reason required|string|max:1000`; hạn mới phải sau hạn hiện tại), `IssueExtensionRejectRequest.php` (`reject_reason required`).
- Modify: `IssueController` — `requestExtension`, `approveExtension`, `rejectExtension`, `cancelExtension` (khuôn `TaskController::runExtension`).
- Modify: routes trước `/{issue}`: `post('/extension-requests/{extension}/approve|reject|cancel')`, `post('/{issue}/extension-requests')`.
- Luật (§4.5): gửi = người phụ trách, vấn đề có hạn, trạng thái ∈ {assigned, in_progress, rejected, reopened}, ≤1 chờ, người phụ trách ≠ người tạo; quyết = `canEdit()`; huỷ = người gửi; thông báo gửi ⇒ người tạo, quyết ⇒ người gửi.
- Test: `IssueV2ApiTest.php`

- [ ] Step 1: Test `test_nguoi_phu_trach_gui_de_nghi_nguoi_tao_thay_co_quyet`, `test_khong_co_han_khong_gui_duoc_422`, `test_dong_y_doi_han_ghi_lich_su`, `test_tu_choi_bat_buoc_ly_do`, `test_nguoi_gui_huy`, `test_dong_van_de_tu_huy_de_nghi_cho`, `test_nguoi_tao_trung_nguoi_phu_trach_khong_gui_duoc`.
- [ ] Step 2–4. Step 5: Chạy **cả** `Modules/Assign/Tests` (memory 3G) ⇒ không đỏ mới (3 test phòng họp đỏ có sẵn). Commit `feat(issue): đề nghị gia hạn`.

---

## Phase 2 — Web `hrm-client`

> Trước Task 8: đọc skill `button-convention`, `modal-popup`, `form-validate`, `select-and-input-state`, `notification-convention` (chữ hiển thị). Copy pattern từ `components/assign/task/panel/*` (ghi `file:dòng` khi copy).

### Task 8: Khung `IssuePanel` chế độ xem (Chi tiết · Kết quả xử lý · Bình luận · Lịch sử)

**Files:**
- Create: `components/assign/issue/panel/IssuePanel.vue` — khung/header/backdrop/`above-modal`/`Esc` như `TaskPanel.vue`; dùng lại CSS `components/assign/task/panel/task-panel.scss` (import, lớp `tkp-*`; chỗ khác thì thêm `issue-panel.scss` nhỏ). Tab bằng `V2BaseTabNavigation`, Bình luận = `CommentThread type="issue"`, Lịch sử = `SystemInfoSection entity-type="issue"`.
- Create: `components/assign/issue/panel/IssueDetailTab.vue` (khối theo §4.2; người `can_edit` bấm giá trị ⇒ `IssueFieldPopover` ⇒ `PATCH field`), `IssueResultTab.vue` (§4.1), `IssueFieldPopover.vue` (khuôn `TaskFieldPopover.vue`), `issuePanelHelpers.js` (icon theo trạng thái, nhãn nút theo đích — bảng §4.3).
- Interfaces — Produces (API công khai, giữ của popup cũ): `open(issue = null, readOnly = false, isHandling = false, initialData = {}, commentId = null, options = {})` · `view(issue, commentId = null)` · `create(defaults = {})`; prop `lockModule`, `lockSolution`, `lockProject` (**không ghi vào prop** — copy sang data); sự kiện `saved(detail)` sau mọi thay đổi + `created(detail)` khi tạo mới (một chỗ gọi đang nghe `@created`).
- [ ] Step 1: Dựng panel xem + 4 tab với dữ liệu `GET assign/issues/{id}`; deep link `?open_issue=&comment_id=` ở `issues/index.vue` mở panel và cuộn tới bình luận.
- [ ] Step 2: Playwright MCP: mở 1 vấn đề NV 13 ⇒ đo panel `getBoundingClientRect` (rộng = TaskPanel), 4 tab đếm đúng, pill màu = `status_color` BE; người không `can_edit` bấm giá trị không mở popover.
- [ ] Step 3: Commit `feat(issue): IssuePanel xem 4 tab`.

### Task 9: Dải nút hành động + hộp bước + đổi người phụ trách + gia hạn + theo dõi + tệp

**Files:**
- Create: `components/assign/issue/panel/IssueStepModal.vue` (V2BaseModal; nội dung theo `requires` BE trả: chọn người / Cách xử lý + Nhóm nguyên nhân + tệp / lý do bắt buộc / lý do tuỳ chọn), `IssueExtensionBox.vue` (khuôn khối gia hạn trong `TaskDetailTab.vue`).
- Modify: `IssuePanel.vue` — dải nút = `detail.allowed_next_statuses.filter(s => !s.is_current)` (**không** lọc theo `id !== status`: đang `assigned` có thêm bước `id='assigned'`, `requires='assignee'` = Đổi người phụ trách; mỗi phần tử `{id, name, color, requires, is_current}`), nút hiện theo bước BE trả, **không** dựa `can_handle` (trưởng đơn vị `can_handle=false` nhưng có bước) + nhãn §4.3; nút tệp theo cờ `can_manage_attachments` (đích `assigned` khi đã có người phụ trách ⇒ "Đổi người phụ trách", chưa có ⇒ "Phân công"); Đóng vấn đề nút đỏ cuối dải; không có nút nào ⇒ dòng lý do (VD2-09); 👁 Theo dõi; ⋯ (Lịch sử, Xoá khi `can_delete` qua `$confirm`).
- [ ] Step 1: Code. Step 2: Playwright MCP với role tạm theo [[local-dev-duoc-cap-quyen-de-test]] hoặc đổi `actAs` bằng JWT tinker 3 người (13 tạo · 50 phụ trách · LEAD): đi trọn luồng Tạo(phòng ban) → LEAD Phân công → 50 Nhận xử lý → 50 đề nghị gia hạn → 13 đồng ý → 50 Báo đã xử lý (thiếu trường ⇒ cả 2 ô đỏ cùng lúc) → người duyệt Từ chối → 50 Xử lý lại → Báo xong → Xác nhận → 13 Mở lại → Đóng. Mỗi bước đo số nút hiện ở dải bằng DOM. Stub 1 vấn đề `status` lạ ⇒ panel không lỗi console.
- [ ] Step 3: Commit `feat(issue): nút hành động, hộp bước, gia hạn, theo dõi`.

### Task 10: Form Tạo / Sửa (`IssueForm`)

**Files:**
- Create: `components/assign/issue/panel/IssueForm.vue` — bố cục §4.2 (Gắn với · Tên · Loại/Ảnh hưởng/Nguồn · chip ưu tiên · Người phụ trách + "Giao cho tôi" / Phòng ban + Bộ phận + dòng báo trước U36 · Người duyệt đóng / Người báo · Hạn + 17:30 + chọn nhanh · Mô tả · "+ Tệp" (`FileAttachmentTable`/`V2BaseFile` theo khối tệp popup cũ) · Thiết lập thu gọn "n mục đang dùng"). Danh mục: dùng lại nguồn popup cũ (`solutions/getAll`, `prospective-projects/getAll`, `tasks/getAll` — picker hiện `code – name`, tìm theo tên), nạp khi mở form. `detected_at` gửi giờ địa phương `YYYY-MM-DD HH:mm:ss`.
- Footer Tạo: [Gửi vấn đề] [Gửi & tạo tiếp] [Huỷ]; Sửa: [Lưu thay đổi] [Huỷ]; ô Người phụ trách ở Sửa chỉ đọc. Validate đồng thời, 422 gắn ô. Cảnh báo thoát khi chưa lưu theo skill `unsaved-changes` (panel = kiểu modal ⇒ `unsavedModalMixin`, kiểm mục 2b).
- [ ] Step 1: Code. Step 2: Playwright MCP: tạo từ `/assign/issues` (chỉ phòng ban ⇒ Mới ghi nhận; có người ⇒ Đã phân công), tạo từ tab GP (GP + dự án khoá), từ tab Hạng mục (khoá thêm hạng mục), "Gửi & tạo tiếp" giữ khối Gắn với; Sửa vấn đề cũ có đủ trường Thiết lập ⇒ không mất giá trị (so từng ô với `GET` trước–sau).
- [ ] Step 3: Commit `feat(issue): form Tạo / Sửa vấn đề v2`.

### Task 11: Thay 13 chỗ gọi + xoá popup cũ

**Files:** 13 file ở design §4.12 — đổi import `CreateIssueModal` ⇒ `@/components/assign/issue/panel/IssuePanel.vue` (giữ tên ref); xoá `pages/assign/issues/components/CreateIssueModal.vue`.
- [ ] Step 1: Đổi import từng file, `grep -rn "CreateIssueModal" pages components` ⇒ rỗng.
- [ ] Step 2: Playwright MCP từng chỗ (13): mở được, đúng chế độ (`open(item,true,true)` ⇒ xem + dải nút), lưu xong màn gọi nạp lại; 3 chỗ trong b-modal (`IssueUpcomingModal`, `WorkDrillModal`, bàn giao) đo `z-index` panel > modal và bấm nền chỉ đóng panel. `IssueUpcomingModal` bấm Xem không lỗi JS (KS #12).
- [ ] Step 3: Commit `refactor(issue): 13 màn dùng IssuePanel, xoá CreateIssueModal`.

### Task 12: e2e

**Files:**
- Create: `e2e/tests/assign/issue-panel-v2.spec.ts` (`serial`; dữ liệu tạo/xoá qua API; ca: tạo phòng ban/đích danh · phân công bởi trưởng đơn vị · trọn vòng đời · báo xử lý thiếu trường · gia hạn · đổi người phụ trách · người ngoài phạm vi không thấy nút/403 · sửa không mất trường).
- Modify: 6 spec đang dựa popup cũ — `issue-detail-access`, `work-calendar-grid`, `employee-work-performance`, `my-todo-list-drawer`, `work-calendar-popup`, `agent/agent-chat` (chỉ ca mở vấn đề).
- [ ] Step 1: Viết/sửa spec. Step 2: Chạy spec mới + 6 spec sửa (BASE_URL :3080 / API :8080), đọc dòng tổng kết. Step 3: Commit `test(e2e): issue panel v2`.

---

## Phase 3 — Tab Vấn đề trong Nhóm trao đổi

> Hồ sơ riêng `.plans/agent-chat/chat/gd34-tab-van-de/` (design ngắn chép §6 + plan chi tiết) — viết khi Phase 2 xong, hỏi lại phạm vi code (thêm migration `issues.workspace_id`).

### Task 13: BE tab Vấn đề nhóm
- Migration `2026_11_24_000001_add_workspace_id_to_issues_table` (nullable + index); store nhận `workspace_id` (thành viên nhóm, nhóm chưa đóng); `IssueAccess::canView` thêm thành viên nhóm (`WorkspaceAccess::roleOf`) + nhóm GP (`solution_id` trùng nguồn nhóm); `assertWritable` 423 khi nhóm thường đã đóng.
- `GET assign/workspaces/{id}/issues` theo khuôn `GET workspaces/{id}/tasks` (đếm nhóm + lọc nhanh; nhóm thường lọc `workspace_id`, nhóm GP lọc `solution_id`).
- Bỏ chặn `issues` cho nhóm GP ở `StoreWorkspaceRequest` / `UpdateWorkspaceRequest` (giữ chặn TKT). PHPUnit Workspace.

### Task 14: FE tab Vấn đề nhóm
- `components/assign/issue/group-list/IssueGroupListView.vue` theo khuôn `components/assign/task/group-list/*` (gom Trạng thái / Người xử lý / Hạn / Dự án); `WorkspaceView` + `WorkspaceTopicTabs` thêm tab `issues` (`?panel=issues`); `CreateWorkspaceModal` + `SettingsPanel` ô tick Vấn đề (ẩn với nhóm TKT); "+ Vấn đề" ⇒ `IssuePanel.create({workspace_id, solution_id?})`.
- Playwright MCP + e2e `workspace-issues.spec.ts` + chạy lại `workspace-tasks`, `chat-core`, `workspace-kh-project`.

---

### Checkpoint — 17/11/2026 (Phase 2 web xong)
Vừa hoàn thành: Task 8–12 + 1 đợt sửa sau soát cả nhánh — hrm-client nhánh `gop_db-van-de-v2` (wt-nhom-trao-doi, :3080 chạy nhánh này) 8 commit `823561986..eaa10b8a2`, CHƯA push. CreateIssueModal đã xoá, 13 màn dùng IssuePanel (kiểm Playwright từng màn). e2e (HRM/e2e, ngoài git): `issue-panel-v2.spec.ts` mới 11/11 ×2 (lượt Task 12, chạy khi tạm đặt QUEUE_CONNECTION=database rồi trả về sync); sau đợt sửa cuối CHƯA chạy lại. 5 spec cũ đã sửa (đỏ còn lại đều có sẵn: log [QUYEN_XEM_CHI_TIET] ở nhánh vá quyền, tiêu đề "Chỉnh sửa nhắc việc" 92ca3a93c, NV thường bị chặn "Tính năng đang phát triển"); agent-chat chỉ chạy ca mở thẻ (cần AGENT_FAKE).
Quyết định khi chạy (controller): R8 Sửa đổi Gắn với gọi PATCH link trước PUT · R11 select trong panel theo khuôn TaskDetailTab (V2BaseSelect + dropdownParent) · R12 open(item,true)=xem, chỉ hideActions mới khoá · R13 người không có bước vẫn thấy dòng lý do xám · R14 khối gia hạn đầu tab Chi tiết như Nhiệm vụ · R16 Loại/Ảnh hưởng/Nguồn để trống khi tạo (popup cũ mặc định bug/personal/self) · F4 khoảng cách nút hộp bước 16px, thanh gia hạn 22px theo CSS chung .tkp-ext.
Câu (1) XONG 17/11 (user chọn sửa ngay): hrm-api `394e216e4` cờ `attachments[].can_delete` / `can_watch` / `pending_extension.can_cancel` (luật 1 nguồn: Issue::canDeleteAttachment, IssueExtensionRequest::canCancel; test Issue 65/65) + hrm-client `bc916bd2e` panel đọc cờ (Playwright :3080: NV50 1 nút xoá + Huỷ đề nghị; NV13 2 nút xoá + Đồng ý/Từ chối). Lưu ý: kiểm lại thì `attachments[]` VỐN CÓ `created_by` (model File không ẩn) — kết luận "thiếu created_by" của reviewer là sai.
Câu (2) XONG 17/11 (user chọn API riêng): spec issue-panel-v2 tự bật API tạm :8089 (QUEUE_CONNECTION=null ⇒ NullQueue, kiểm trước khi chạy), route trình duyệt :8080→:8089, tắt cả nhóm tiến trình theo PGID; KHÔNG sửa .env. Chạy: 11 passed, 0 job push, :8080 không nhận request.
Câu (3) XONG 17/11 (user chọn sửa luôn): TaskPanel ra ngoài v-show ở my-todo (hrm-client commit sau bc916bd2e); Playwright: tab Lịch làm việc mở nhiệm vụ 457 ⇒ panel 660×840, bấm trúng panel.
Câu (4) XONG 17/11: user chốt GIỮ R16 — Loại / Mức độ ảnh hưởng / Nguồn phát hiện để trống khi tạo.
Câu (5) XONG 17/11: user chọn theo CLAUDE.md dòng 38 — ô bắt buộc validate ở CẢ FE lẫn BE: hrm-client `d13eabaa0` (IssueForm / IssueStepModal / hộp gia hạn; bộ required = đúng FormRequest BE; Playwright: Tạo trống 6 ô đỏ, 0 request; e2e issue-panel-v2 11 passed). Skill form-validate còn ghi "required chỉ ở BE" — lệch CLAUDE.md, cần team sửa skill (tài sản chung, chưa sửa).
Còn chờ user: R16 · (5) required FE vs BE (CLAUDE.md dòng 38 vs skill form-validate) · Phase 3 tab nhóm.
Ngoài luồng ghi nhận: my-job/index.vue không nghe @refresh (KS #15); handleSearch danh sách nạp 2 lượt khi ở trang ≠1.

### Checkpoint — 17/11/2026 (Phase 1 BE xong)
Vừa hoàn thành: Phase 1 Task 1–7 + 1 đợt sửa sau soát cả nhánh — hrm-api nhánh `gop_db-van-de-v2` (wt-nhom-trao-doi), 17 commit `0dff9a0ce..b6f2d6485`, CHƯA push. Migration `2026_11_23_000001` đã chạy `db_gop_6_11`. Test: `Tests/Feature/Issue` 62/62 (405 assertions), Agent `test_van_de` 5/5 (controller chạy lại). Cả suite Assign có 116F+36E ở Contract/Warehouse/Product… — nhánh chỉ đụng file Issue + route ⇒ lỗi môi trường DB local có sẵn.
Quyết định khi chạy (controller): R1 thông báo mới dồn Task 6 · R2 huỷ gia hạn chuyển sang IssueExtensionService::cancelPending · R5 trưởng đơn vị xử lý vào tầng 1 phạm vi xem (để Phân công được) · R6 trưởng phòng thấy vấn đề của bộ phận có trưởng riêng nhưng không Phân công · R7 tệp chứng cứ cộng dồn qua nhiều vòng (Phase 2 hiện kèm thời điểm) · PATCH sang đúng trạng thái hiện tại ⇒ 422 · nhãn thông báo theo skill (Tạo mới/Cập nhật/Đã duyệt/Tiếp tục/Chờ duyệt/Từ chối), chữ "Giao xử lý…" nằm trong ghi chú.
Để sau (ghi nhận): FormRequest status validate trước kiểm quyền (đợt vá quyền đọc) · gửi đề nghị gia hạn không khoá dòng (bấm đúp ra 2 đề nghị) · thông báo chạy trong transaction · endpoint ghi mới chưa gắn `solutionMemberActive` (PUT cũ cũng không) · xoá vấn đề để lại dòng mồ côi gia hạn/tệp chứng cứ · **PUT đổi GP/hạng mục không tự gán version** (PATCH `link` có) — Phase 2 form Sửa cần quyết · popup cũ `CreateIssueModal` sẽ hỏng (PUT không đổi trạng thái; 2 lựa chọn "Đã phân công") tới khi Phase 2 thay.
Bước tiếp theo: hỏi riêng phạm vi code Phase 2 (hrm-client, nhánh `gop_db-van-de-v2`, 13 màn + xoá popup cũ + e2e).
Blocked: chưa có lệnh code Phase 2.

### Checkpoint — 17/11/2026
Vừa hoàn thành: design (user duyệt 17/11) + plan.
Đang làm dở: —
Bước tiếp theo: user soát plan + chọn cách chạy; hỏi riêng phạm vi code Phase 1 (repo · nhánh · migration `2026_11_23_000001` vào `db_gop_6_11`).
Blocked: chưa có lệnh code.

### Checkpoint — 17/11/2026 khuya (ĐÃ DEPLOY TPE)
prod api `5eba99ce1` · client `21a383016` (build_tpe EXIT 0, 3 migration 2026_11_23_000001 / 2026_11_24_000001 / 2026_11_24_000002 chạy xong, site 200).
