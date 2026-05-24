# Plan — Phương án triển khai dự án

**Spec:** `docs/superpowers/specs/2026-05-23-project-implementation-types-design.md`
**Design:** `design.md`

---

## Phase 1 — DB & Model ✅ DONE 2026-05-23

### BE
- [x] Migration: thêm `prospective_projects.implementation_type` (tinyint NOT NULL default 3) — `2026_05_23_000001_add_implementation_type_to_prospective_projects_table.php`
- [x] Migration: đổi `solutions.request_solution_id` sang nullable — `2026_05_23_000002_make_request_solution_id_nullable_on_solutions.php`
- [x] Cập nhật `ProspectiveProject` entity: const `IMPLEMENTATION_TYPE_SELF=1, BY_DEPT=2, CROSS_DEPT=3` + mảng `IMPLEMENTATION_TYPES` + thêm vào `$fillable`.
- [x] Helper `ProspectiveProject::isLockedImplementationType()` + accessor `is_locked_implementation_type`.
- [x] Transformer: `DetailProspectiveProjectResource` + `ProspectiveProjectResource` trả về `implementation_type` (+ `is_locked_implementation_type` cho detail).
- [x] `ProspectiveProjectRequest`: thêm rule `implementation_type|nullable|integer|in:1,2,3`.
- [x] `ProspectiveProjectService::update()`: throw `ValidationException` khi đổi type lúc đã locked.

### FE
- [x] `pages/assign/prospective-projects/constants.js` — export `IMPL_TYPE_*`, `IMPLEMENTATION_TYPES`, các `STATUS_*`.
- [x] `ProjectInfoSection.vue`: thêm V2BaseSelect "Cách triển khai dự án" (default=3), disable khi locked + helper text.
- [x] `add.vue` + `_id/edit.vue`: thêm `implementation_type: 3` + `is_locked_implementation_type: false` vào `formSubmit`.

### Checkpoint — 2026-05-23
Vừa hoàn thành: Phase 1 (Migration + Entity + FormRequest + Service guard + Transformer + FE form). Chưa chạy migration + chưa test browser.
Đang làm dở: không
Bước tiếp theo: User chạy 2 migrations + smoke test màn `/assign/prospective-projects/add` (xem dropdown hiện đủ 3 option, default=3) + edit dự án cũ (dropdown vẫn = 3, không lock). Sau đó tiếp Phase 2.
Blocked: không

## Phase 2 — Type=1 luồng tạo Solution không qua RequestSolution ✅ DONE 2026-05-23

### BE
- [x] `SolutionService::normalizePayload()` — branch type=1 (ép has_modules=false, pm_id=auth, request_solution_id=null, status=DANG_TRIEN_KHAI)
- [x] `SolutionService::create()` — end_date ưu tiên payload `internal_need_gp_date`
- [x] `SolutionService::updateRequestSolution()` — null-guard đầu hàm
- [x] `SolutionRequest` — `request_solution_id` nullable khi type=1
- [x] Null-safe `Solution::isCanManage()` (line 158)
- [x] `ProspectiveProjectService::syncStatusBySolution()` — branch type=1 (chỉ 2 trạng thái DANG_TRIEN_KHAI/DA_DUYET_GIAI_PHAP)

### FE
- [x] `index.vue` — action icon "Tạo giải pháp" cho type=1 + status=THU_THAP_TT (đã làm task #6)
- [x] `SolutionForm.vue` — nhận query `prospective_project_id`, capture `implementation_type` từ project, preset has_modules=false, pm_id=auth khi type=1
- [x] `InfoTab.vue` — ẩn checkbox has_modules, hiện helper text "KD trực tiếp làm GP" cho type=1
- [x] `manager.vue` — không cần sửa (nút PM/Leader duyệt đã gate bằng status, không xuất hiện khi type=1)

## Phase 3 — Type=1 Hồ sơ trình duyệt auto-approve ✅ DONE 2026-05-23

### BE
- [x] `SolutionService::storeSolutionReviewProfile()` — branch $isSelf: status='approved' ngay, approved_at, Solution=DA_DUYET_GIAI_PHAP, SolutionVersion approved_at, BOM 'approved', skip notification
- [x] `SolutionService::reviewSolutionProfileDecision()` — throw 422 khi type=1
- [x] `DetailSolutionResource` — trả về `implementation_type`

### FE
- [x] `SolutionApprovalModal.vue` — ẩn block "Người phê duyệt", ẩn footer dept_head action, đổi text "Lưu & Trình duyệt" → "Lưu & Duyệt" khi isSelfImplementation
- [x] Cột "Trạng thái duyệt" — type=1 hiển thị "approved" tự nhiên (BE trả về status đúng)

## Phase 4 — Type=2 (Triển khai theo Phòng) ✅ DONE 2026-05-23

### BE
- [x] `RequestSolutionService::store()` — type=2 lock `receive_dept = project.main_sale_department_id`, throw 422 nếu type=1 cố tạo YC
- [x] `RequestSolutionService::update()` — type=2 lock receive_dept tương tự
- [x] `RequestSolutionService::pending()` — filter mở rộng: type=3 (departmentsManager + backward compat null), type=2 (receive_dept = phòng user hiện tại)
- [x] `Solution::isCanManage()` — branch type=2 (check `receive_dept == auth.dept_id` thay vì departmentsManager)

### FE
- [x] `RequestTab.vue` — computed `isByDept` + watcher autoReceiveDept, auto-set + disable select + helper text cho type=2

## Phase 5 — QA (CHỜ USER TEST)

- [ ] Chạy 2 migrations: `php artisan migrate`
- [ ] Test type=1 end-to-end: tạo dự án (chọn Tự triển khai) → submit để chuyển status=2 → bấm icon "Tạo giải pháp" trên list → form Solution preset đúng (ẩn YC làm GP, KD=PM, không hạng mục) → lưu → kiểm tra Solution=`7 Đang triển khai`, Project=`4 Đang làm GP` → vào manager → tạo BOM tổng hợp Hoàn thành cho version → tạo Hồ sơ trình duyệt → bấm "Lưu & Duyệt" → kiểm tra Solution=`11 Đã duyệt GP`, Project=`5 Đã duyệt GP`, profile=`approved`
- [ ] Test type=2 end-to-end: tạo dự án (chọn Theo Phòng) → tạo YC làm GP → kiểm tra receive_dept auto-lock = phòng KD → submit YC → user có permission ở phòng KD đó vào `/assign/request-solution/pending` thấy YC → tiếp nhận → flow giống type=3
- [ ] Test type=3: tạo dự án mặc định Liên phòng ban → toàn bộ luồng cũ vẫn hoạt động (không regression)
- [ ] Edge: dự án đã có Solution → đổi implementation_type → bị chặn 422
- [ ] Edge: dự án type=1 → cố gọi API tạo RequestSolution → bị chặn 422
- [ ] Edge: dự án cũ default type=3 sau migration → list/edit không vỡ

### Checkpoint — 2026-05-23
Vừa hoàn thành: Phase 1+2+3+4 — toàn bộ BE + FE cho type=1 (Tự triển khai) + type=2 (Theo phòng) + bảo toàn type=3.
Đang làm dở: không
Bước tiếp theo: User chạy migration + test theo checklist Phase 5.
Blocked: không

### Checkpoint — 2026-05-24 (HOÀN THÀNH)
User test xong type=1 và type=2 → OK. Các fix bổ sung trong quá trình test:
- Null-safe `DetailSolutionResource::project_internal_need_gp_date` + `request_solution_status` cho type=1
- Sửa `normalizePayload` để Lưu nháp giữ TAO_NHAP, chỉ Lưu & gửi mới nhảy DANG_TRIEN_KHAI (type=1)
- Chặn tạo Solution thứ 2 cho dự án đã có Solution (BE + FE ẩn icon "Tạo giải pháp")
- Ẩn nút "Lưu và duyệt hạng mục" trong edit.vue khi type=1
- Ẩn block "Yêu cầu làm GP" trong InfoTab + ProjectInfoTab + list solutions cho type=1
- Disable PM select + helper "KD là PM" cho type=1
- Ẩn field "Hạn duyệt" trong modal review profile cho type=1
- Bỏ filter `bom_list_type=TYPE_AGGREGATE` ban đầu rồi revert lại (vẫn yêu cầu BOM tổng hợp)
- `handleReviewProfileSaved` redirect sang manager page sau Lưu & Duyệt type=1 (tránh toast can_edit=false)
- Thêm `implementation_type: 3` vào tktForm init để Vue 2 reactive khi populate từ project
- Filter BE: loại dự án type=1 ra khỏi dropdown chọn dự án trong form tạo YC làm GP

Trạng thái: ✅ Hoàn thành, đã chuyển sang "Hoàn thành" trong STATUS.md.
