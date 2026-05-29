# Nhóm lĩnh vực khách hàng — Plan

**Owner:** @manhcuong
**Spec:** [docs/superpowers/specs/2026-05-28-customer-scope-group-design.md](../../docs/superpowers/specs/2026-05-28-customer-scope-group-design.md)

---

## Phase 1 — Database & Migration

### BE

- [x] Migration tạo bảng `customer_scope_groups` (copy cấu trúc `customer_scopes`)
- [x] Migration tạo pivot `customer_scope_group_members` (customer_scope_group_id, customer_scope_id, timestamps, unique pair)
- [x] Migration tạo pivot `application_customer_scope_groups` (application_id, customer_scope_group_id, timestamps, unique pair)
- [x] Migration thêm cột `customer_scope_group_id` nullable vào `prospective_projects`
- [x] Migration backfill: mỗi customer_scope có application → tạo 1 nhóm, gắn member + application, backfill `customer_scope_group_id` cho prospective_projects; rồi `dropIfExists('application_customer_scopes')`
- [x] Viết `down()` cho migration backfill (tạo lại pivot cũ, backfill ngược)

---

## Phase 2 — Backend: danh mục Nhóm (mới)

### BE

- [x] Entity `CustomerScopeGroup` (fillable, constants status, `customerScopes()`, `applications()`, `createdByEmployee`, `updatedByEmployee`, `getNextCode()`, `isCanEdit`, `isCanLockUpdate`)
- [x] `CustomerScopeGroupRequest` (name/code unique + regex NLVKH, customer_scope_ids required min:1 exists, code prohibited khi có application — rethrow ValidationException)
- [x] `CustomerScopeGroupService` (index + groups/scopes count + filter, getAll kèm customerScopes:id, updateOrCreate/update sync members, destroy detach, validateImportData + import)
- [x] `CustomerScopeGroupResource` (list) + `DetailCustomerScopeGroupResource` (show + customer_scopes + ids)
- [x] `CustomerScopeGroupController` (index, getAll, updateOrCreate, update, show, delete, lock, unlock, export, validateImport, import)
- [x] Export class + blade cho import/export (copy CustomerScope)
- [x] Routes `/v1/assign/customer-scope-groups/*` + middleware checkPermission
- [x] Thêm 2 permission ("Quản lý/Xem danh mục nhóm lĩnh vực khách hàng") vào `PermissionsTableSeeder` (id 1093/1094)

---

## Phase 3 — Backend: sửa CustomerScope + Application

### BE

- [x] `CustomerScope`: bỏ `applications()`, thêm `groups()`; `isCanLockUpdate()` theo nhóm active
- [x] `CustomerScopeService`: `applications_count` → `groups_count`; `show()` load `groups`
- [x] `CustomerScopeResource` + Detail: trường `applications_count` → `groups_count`; thêm `groups`
- [x] `Applications`: bỏ `customerScopes()`, thêm `customerScopeGroups()`; `isCanUnlockUpdate()` check groups active
- [x] `ApplicationService`: index eager load + filter `customer_scope_group_id`; getAll load groups; updateOrCreate sync `customerScopeGroups`; destroy detach; import resolve mã nhóm (cột `groupCode`)
- [x] `ApplicationsRequest`: `customer_scope_ids` → `customer_scope_group_ids` (exists customer_scope_groups)
- [x] `ApplicationsResource` + Detail + Controller show: khối `customer_scopes*` → `customer_scope_groups*`
- [x] `CustomerScopeRequest`: rule chặn sửa mã dùng `groups()`

---

## Phase 4 — Backend: Dự án tiềm năng (downstream)

### BE

- [ ] `ProspectiveProject`: thêm quan hệ `customerScopeGroup()` belongsTo (giữ `customerScope()`)
- [ ] `ProspectiveProjectService::autoFillFromApplication()`: đổi nguồn sang `customerScopeGroups`, set group đầu tiên theo luồng; giữ auto-fill scope/industry
- [ ] `ProspectiveProjectService::index()`: thêm filter `customer_scope_group_id`
- [ ] `ProspectiveProjectRequest`: validate `customer_scope_group_id` (cả 2 selection_mode)
- [ ] `ProspectiveProjectResource` + `DetailProspectiveProjectResource`: thêm `customer_scope_group_id` + `customer_scope_group_name`

---

## Phase 5 — Frontend: màn Nhóm mới + store

### FE

- [x] `pages/assign/customer-scope-groups/index.vue` (copy customer-scopes: list + filter + import/export, cột Số ứng dụng + Số lĩnh vực)
- [x] Modal `AddGroupModal.vue` (copy AddScopeModal + multi-select Lĩnh vực thành viên, validate inline required)
- [x] `store/optionsSelect.js`: thêm state/mutation/getter + action `fetchCustomerScopeGroups` (map customer_scope_ids thành viên)
- [x] `store/optionsSelect.js`: sửa `fetchApplications` map `customer_scope_group_ids`
- [x] Thêm menu (menu-sidebar.js) — route tự sinh từ file pages/
- [ ] (Phụ) Tạo file mẫu `public/Mau_import_NLVKH.xlsx`

---

## Phase 6 — Frontend: sửa màn Ứng dụng + Lĩnh vực

### FE

- [ ] `application/index.vue`: cột + filter Lĩnh vực → Nhóm (`customer_scope_group_names`, `customer_scope_group_id`); cột import GroupCode
- [ ] `components/modal/application-modal.vue`: multi-select `customer_scope_ids` → `customer_scope_group_ids` (label, options, payload, load detail)
- [ ] `customer-scopes/index.vue`: cột "Số ứng dụng" → "Số nhóm" (`groups_count`); logic disable khóa/xóa + thông báo ràng buộc
- [ ] `customer-scopes/AddScopeModal.vue`: ô "Số ứng dụng" (view) → "Số nhóm"

---

## Phase 7 — Frontend: Dự án tiềm năng (downstream)

### FE

- [x] `ProjectInfoSection.vue`: luồng xuôi — thêm dropdown Nhóm (lọc theo application) → Lĩnh vực (lọc theo member nhóm)
- [x] `ProjectInfoSection.vue`: luồng ngược — Lĩnh vực → Nhóm (chứa lĩnh vực) → Ứng dụng (theo nhóm) → suy ngành/giải pháp
- [x] `ProjectInfoSection.vue`: computed mới (filteredGroupsByApplication, filteredCustomerScopesByGroup, filteredGroupsByCustomerScope, filteredApplicationsByGroup) + watchers reset cascade + `autoFillFromApplication` đổi nguồn + `loadSelectOptions` thêm fetchCustomerScopeGroups
- [x] `prospective-projects/index.vue`: thêm filter `customer_scope_group_id` + cột "Nhóm lĩnh vực khách hàng"
- [x] `add.vue` + `_id/edit.vue`: thêm field `customer_scope_group_id` vào form
- [x] (Downstream phát sinh) `meeting/components/MeetingProject.vue`: resolve customer scope qua nhóm (filteredCustomerScopesByApplication + onApplicationChange + getCustomerScopeIdsByApplication)

## Phase 9 — Tinh chỉnh sau test (2026-05-28)

### Validate
- [x] Chuyển validate hoàn toàn về BE cho form feature này: AddGroupModal bỏ check JS (touched/validateForm), submit thẳng → hiển thị 422; add/edit Dự án tiềm năng bỏ gate local (contact/email) + xóa validateRequired chết
- [x] Thêm `attributes()` vào ProspectiveProjectRequest (tên field tiếng Việt cho message BE)

### Cascade filter & form
- [x] Màn danh sách: cascade 2 chiều đầy đủ 5 filter (scope/industry/application/group/customer_scope) — chọn bất kỳ → các filter khác thu hẹp theo mapping (app-join + thành viên nhóm)
- [x] Form add/edit (ProjectInfoSection): giữ 2 radio nhưng nới thứ tự — options 2 chiều dùng chung + auto-fill field còn trống + prune giá trị không hợp lệ, bỏ ép tuần tự; auto-fill cả Lĩnh vực ở luồng xuôi

## Phase 10 — ĐỔI MÔ HÌNH: Nhóm là CHA của Lĩnh vực (2026-05-29)

User chỉnh lại: **Nhóm LVKH là cha của Lĩnh vực (1-n)**; tạo Lĩnh vực phải chọn Nhóm cha (bắt buộc). **Ứng dụng ↔ Lĩnh vực giữ n-n trực tiếp** như cũ (Nhóm không gắn Ứng dụng). Dự án tiềm năng vẫn hiện Nhóm, chọn tự do, sắp xếp cha-trước-con.

### DB (R1)
- [x] Migration `2026_05_29_000001`: thêm `customer_scopes.customer_scope_group_id` (backfill từ members), khôi phục `application_customer_scopes` (backfill từ app_csg ⋈ members), drop `customer_scope_group_members` + `application_customer_scope_groups`. Giữ `prospective_projects.customer_scope_group_id`. Đã chạy + verify.

### BE
- [x] (R2) CustomerScope `group()` belongsTo + `applications()` n-n; isCanLockUpdate theo applications; fillable + Request required group_id; Service lưu group_id + index eager `group` + import thêm cột `groupCode`; Resource trả `customer_scope_group_id/name`
- [x] (R2) CustomerScopeGroup `customerScopes()` hasMany (1-n), bỏ `applications()`; isCanLockUpdate theo lĩnh vực con; Service bỏ sync members, count children, import bỏ member; Request bỏ customer_scope_ids; Resource bỏ applications_count/members
- [x] (R3) Applications `customerScopes()` n-n (revert); ApplicationService/Request/Resource/Controller revert customer_scope_id(s)/customerScopeCode; ProspectiveProjectService autofill: scope→group cha

### FE
- [x] (R4) store: app map `customer_scope_ids`, customerScopes mang `customer_scope_group_id`, groups bỏ members; AddScopeModal thêm dropdown Nhóm cha (required); customer-scopes index cột "Nhóm LVKH"; AddGroupModal bỏ multi-select members; groups index bỏ "Số ứng dụng"
- [x] (R5) application index/modal + MeetingProject revert về Lĩnh vực
- [x] (R6) ProjectInfoSection viết lại cascade theo mô hình mới (app↔scope n-n, scope→group cha) + reorder luồng ngược (Nhóm trước Lĩnh vực); prospective index filter cascade; add/edit giữ field group_id
- [x] (R7) Verify: migration OK, quan hệ Eloquent OK, API getAll đúng shape, FE compile 200

---

## Phase 8 — Migration & Test

### Test

- [x] Chạy migration trên DB dev (qua --path từng file) → 3 bảng + cột mới OK, backfill: 59 nhóm / 59 member / 653 app-link / 6 prospective set group, `application_customer_scopes` đã drop
- [x] Verify quan hệ Eloquent (group↔members, app↔groups, scope↔groups), backfill prospective nhất quán 0 lỗi
- [x] Verify resource: ApplicationsResource trả customer_scope_group_* (không còn key cũ), DetailCustomerScopeGroupResource trả members + count
- [x] Seed 2 permission (1093/1094) + gán cho role đang có quyền Lĩnh vực
- [x] HTTP API thực: route `/customer-scope-groups` 403 (có middleware), getAll 200 trả members; applications/getAll trả customer_scope_groups
- [x] FE 3 trang (customer-scope-groups, application, prospective add) compile OK, HTTP 200, không lỗi biên dịch
- [ ] (Cần click-through người dùng) Màn Nhóm: tạo/sửa/xem/xóa, khóa/mở khóa, import/export, validate inline
- [ ] (Cần click-through) Ứng dụng: form chọn Nhóm + list/filter; Lĩnh vực: cột "Số nhóm" + chặn khóa/xóa
- [ ] (Cần click-through) Dự án tiềm năng 2 luồng cascade + edit dự án cũ; Họp chọn ứng dụng→lĩnh vực
