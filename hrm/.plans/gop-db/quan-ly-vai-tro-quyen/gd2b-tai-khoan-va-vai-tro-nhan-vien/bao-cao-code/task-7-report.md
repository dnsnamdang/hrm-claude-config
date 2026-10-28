# Task 7 report: FE Màn 2, chi tiết 2 panel (/admin/employee-roles/:id)

Status: DONE_WITH_CONCERNS. Nothing committed. No migration, no seeder, no BE changes. The Zz data written to rehearsal has been cleaned up.

## Files (hrm-client wt-rbac, new, LF)
- `pages/admin/employee-roles/_id/index.vue`: the page.
  - Layout: `row`, then `col-lg-8` (main) and `col-lg-4` (side). `SystemInfoSection` sits outside the row at full width. `V2Footer` has Lưu and Quay lại.
  - Mixins: PageTitleMixin, unsavedChangesMixin (snapshot = `form`), formValidateMixin (422 errors shown inline).
  - Loads `GET admin/employee-roles/{id}` and `GET admin/employee-roles/bulk/options` in parallel. bulk/options gives the C code/name and C's active departments/parts.
  - 403/404 go to `/pages/extras/404`.
  - **Main panel, Vai trò tại C**
    - Search box (accent-insensitive, `normalizeText`) and an "x/y vai trò đang chọn" counter.
    - Role list as checkboxes, scrolling at max-height 460px, with name, description and a "n quyền" link. The link opens `RolePermissionsViewModal.open({id, base_name})`; that GĐ2 file is unchanged.
    - Locked role not held: 🔒 and no checkbox. Locked role held at load: checkbox plus 🔒, and it can be unticked and ticked again (matches BE: only a new tick of a locked role is rejected).
  - **Main panel, Phân công quản lý phòng ban tại C**: the `EmployeeRoleManageDepartments` component.
  - **Side panel**
    - Nhân viên card: avatar, name, "mã · email", department, a muted badge "Công ty chính/Kiêm nhiệm tại C", and a "Quyền đang được cấp" button that opens `GrantedPermissionsModal.open(id)`.
    - `EmployeeRoleCompanies` component.
    - Tổng hợp quyền hiệu lực, using the `rp-summary` pattern. It is recomputed in the FE as the union of `permission_ids` of the ticked roles, counted by `permission_meta` kind and subsystem. Subsystems are sorted by count, descending.
  - **PUT body**
    - Always: `role_ids`, `all_department`, `manage_departments`. `manage_departments` is `[]` when "tất cả" is ticked.
    - `company_ids` is sent **only when `is_main_company`**. For a concurrent employee the key is omitted entirely.
    - On success: `markFormSaved()`, then `router.push('/admin/employee-roles')`.
- `pages/admin/employee-roles/components/EmployeeRoleCompanies.vue`
  - Vertical list. The main company has a green border, a "Công ty chính" tag and no ×.
  - Editable only when `editable` (C is the main company). Read-only shows the hint "Chỉ quản trị viên công ty chính (X) thêm/gỡ được."
  - × opens `$confirm` "Gỡ công ty làm việc". It lists the roles that will be lost, taken from `companies[].role_names`, plus "Mọi phân công quản lý phòng ban ở công ty này". Names are HTML-escaped. Accept button: "Gỡ công ty" (danger).
  - Thêm opens a V2BaseModal with a V2BaseSelect of `$store.state.companies` (the same source the old screen used). The BE fills it with `Company::where('status',1)`. Companies already present are filtered out.
  - Nothing is written until Lưu.
- `pages/admin/employee-roles/components/EmployeeRoleManageDepartments.vue`
  - Checkbox "Quản lý tất cả phòng ban của C". When ticked, the table and the "Thêm phòng ban" button are hidden and an amber note warns if rows exist.
  - Otherwise a V2BaseDataTable: STT · Phòng ban (single select, departments of C, excluding those picked in other rows) · Bộ phận quản lý (multi-select of the row's department, placeholder "Chưa chọn bộ phận") · delete row.
  - A held but inactive department or part is kept as an option with `is_locked`, so it shows 🔒. Its name comes from `$store.state.departments/parts`.
  - 422 errors appear inline per row (`manage_departments.N.department_id`, `.part_ids[.M]`).

## Playwright (rehearsal 8011/3011, namdangit id 13, C = TPE, 1440x900, 1 tab, closed at the end)
- **Main-company employee 147** (Trần Thị Ngọc Mai, TPE main plus DTTDETEK)
  - Panel widths: `.er-main` 905px at x=68, `.er-side` 452px at x=973, so the ratio is 2.00.
  - History block: x=80, w=1333 (full width), below both panels.
  - Footer is fixed (z-index 1001, top 850). Scrolled to the bottom, the history bottom is at 309, so there is no overlap. The body has class `has-v2-footer`.
  - Roles: 103 rows (101 real plus 2 Zz test roles). 2 ticked ("Kế toán bán hàng", "Kế toán quản lý giá bán"). The Zz locked role row reads "🔒 Zz T7 Khoá · Vai trò đã khoá 0 quyền" and has no checkbox.
  - Summary at load: 221, Xem 150, Thao tác 54, Duyệt 17. The 9 subsystem counts are identical to the API `summary`.
  - Ticking "Zz T7 Thử" without saving changed the summary to 225, Xem 151, Thao tác 57, Duyệt 17, and the counter to 3/103.
  - Real mouse click on the checkbox (elementFromPoint returns `custom-control-label`) toggles it.
  - Clicking "196 quyền" on Kế toán bán hàng opened a modal titled "Quyền đang có — Kế toán bán hàng" with 196 rows.
  - Companies: TPE "Công ty chính" with no × (1 × in total). The badge reads "Công ty chính tại TPE".
  - × on DTTDETEK showed the confirm "Gỡ CÔNG TY CỔ PHẦN ĐẦU TƯ TẬP ĐOÀN ETEK (DTTDETEK) … Vai trò Kế toán trưởng | Mọi phân công…" with buttons [Gỡ công ty, Hủy]. Hủy kept 2 rows.
  - Add modal
    - It lists 4 companies; the store has 6 active companies and 2 are already present.
    - Thêm with nothing selected shows "Vui lòng chọn công ty."
    - Choosing TPHP added it with a "Mới thêm" tag.
    - Removing TPHP again showed the confirm with "Không có vai trò nào ở công ty này".
  - Unsaved guard: Quay lại while dirty showed "Thông tin chưa lưu / Bạn có thông tin chưa lưu…" with [Thoát, Ở lại]. Ở lại stayed on the page.
  - 422: adding an empty department row and pressing Lưu returned PUT 422, and the row showed the inline error "Bắt buộc phải nhập". The department dropdown has 25 options (C's active departments). Deleting the row brings back "Chưa phân công phòng ban nào.".
  - "Quyền đang được cấp" opened GrantedPermissionsModal with "11510124 - Trần Thị Ngọc Mai · Vai trò tại TPE".
  - Save tick: PUT `{"role_ids":[100004,100005,108562],"all_department":false,"manage_departments":[],"company_ids":[1,8]}`, then the toast "Cập nhật thành công.", then the page went to `/admin/employee-roles` with no unsaved prompt. The DB showed role 108562 at company 1 and history row 51.
  - Reopened: the history block expands to "1 · 27/10/2026 14:36 · Thay đổi thông tin · DNS Admin · Vai trò thêm mới: - Zz T7 Thử".
  - Save untick: PUT `role_ids [100004,100005]`, 200, back to the list.
- **Concurrent employee 407** (Cao Thị Thùy Linh, TPV main, TPE concurrent)
  - Widths: 905 and 452, ratio 2:1.
  - Badge "Kiêm nhiệm tại TPE". Companies: TPE, and TPV marked "Công ty chính". 0 × buttons and 0 buttons in the block; hint "Chỉ quản trị viên công ty chính (TPV) thêm/gỡ được."
  - Summary 15, Xem 8, Thao tác 7, Duyệt 0, which equals the API.
  - Saving with no change: PUT body `{"role_ids":[100007],"all_department":false,"manage_departments":[]}` with **no `company_ids` key**, response 200. No history row was written because the snapshot was unchanged.
- **Employee 13, "tất cả phòng ban" ticked, with 22 rows** (viewed only, not saved)
  - Table hidden, "Thêm phòng ban" hidden, note "Đang có 22 dòng phân công… sẽ được thay bằng "tất cả phòng ban" khi bấm Lưu."
  - Unticking shows the 22 rows and the button.
- Console: the only error was the expected 422 resource line.
- Self-check grep for raw form tags in `pages/admin/employee-roles/` returns nothing.
- No CRLF in the files, no `vi-VN`, no `.text-muted`.
- `nuxt3011.log` has no ERROR line and nothing mentioning the new files.

## Test data and cleanup (rehearsal)
Before: employee 147 had roles {1: 100004, 100005; 8: 108451}; `company_employees` {1: all_department 0, 8: null}; no manage rows. `employee_permission_history` max id was 50. No Zz roles existed.

Steps:
1. Created through the API `POST admin/roles`:
   - 108562 "Zz T7 Thử", copied from role 100001 (18 permissions).
   - 108563 "Zz T7 Khoá", then locked through `/lock`.
2. Ticked 108562 on employee 147 through the UI and saved, which wrote history 51. Unticked and saved, which wrote history 52.
3. Unlocked 108563 through the API, then deleted both roles through `DELETE admin/roles/{id}`. The roles, their role_has_permissions and employee_has_roles rows are 0.
4. SQL cleanup via tinker:
   - `DELETE FROM employee_permission_history WHERE id IN (51,52) AND employee_id=147;` (2 rows)
   - `DELETE FROM role_permission_history WHERE id IN (132,133,134,135,136,137) AND role_id IN (108562,108563);` (6 rows)

After: employee 147 roles, company_employees and manage rows are identical to before. `employee_permission_history` max is 50 again. Zz roles: 0. `catalog_histories` max is unchanged at 47664. Employee 407 is unchanged (12 role rows, 0 manage rows at TPE).

Residuals I did not revert:
- `company_employees(147,1).updated_at` and `(407,…)`: the BE save sets `updated_at` on the C row for a main employee (147); the 407 save is a delete+insert of 0 rows. The values themselves are unchanged.
- The `roles` and history auto-increment counters moved forward.

## Self-review
- C is never sent; everything is keyed off the BE. There is no super-admin bypass.
- `company_ids` is omitted for concurrent employees.
- The locked-role rule matches the BE `after` hook.
- `role_ids` is kept sorted, so untick-then-retick does not mark the form dirty.
- Data that arrives after a load (the detail) is followed by `markFormPristine` in `$nextTick`.
- The remove-company confirm runs at click time, before save, like the mockup.

## Concerns
1. **Saving with "tất cả phòng ban" ticked deletes that employee's per-department rows at C.** This is BE behaviour from Task 2 (`saveManageDepartments` deletes and inserts nothing when all is ticked). Rehearsal has employees in this state, for example 13 with 22 rows. The FE shows an amber warning, but an unchanged save of such an employee still removes the rows. A decision is needed on whether the BE should keep the rows.
2. The kind badge is `V2BaseBadge variant="muted"` (grey), not the mockup's green/blue, because the BE does not return a color (same as T6 concern 2).
3. The confirm says only "Mọi phân công quản lý phòng ban ở công ty này", because detail does not return department names at company X. The mockup lists them by name.
4. The summary counts held locked roles too, same as the BE `summary`, although a locked role grants nothing in effect. Rehearsal TPE has no locked real role, so this was only seen with Zz data.
5. Names of inactive departments/parts fall back to `$store.state.departments/parts`, then to "#id" if absent. Not exercised: no such row exists at TPE for the test employees.

## Fix round 1

Nothing committed. No migration, no seeder.

### Changes
1. **BE `hrm-api/app/Services/Admin/EmployeeRoleService.php`**
   - `saveManageDepartments`, when `all_department` is true: it now **only sets the flag**. Rows at C with `department_id NOT NULL` are not touched.
     - Main company: `company_employees(E,C).all_department = 1`.
     - Concurrent: inserts the row (department_id NULL, all_department 1) at C only if no such row exists, so there are no duplicates.
   - `saveManageDepartments`, when `all_department` is false: it clears **both** flag sources at C.
     - Sets `company_employees(E,C).all_department` from 1 to 0, regardless of company kind.
     - Deletes every row at C (the flag rows and the old department rows), then inserts the department rows from the payload.
   - `allDepartmentAt`: now reads exactly like `employeeManagesAllDepartmentsIn`. That is: any `employee_manage_departments(E,C)` row with `all_department=1`, OR (C is the main company AND `company_employees.all_department`). A main-company employee whose flag exists only as a NULL row now reports true.
   - The snapshot and detail both go through `allDepartmentAt`, so the history follows the same rule.
2. **Tests `tests/Feature/Rbac/AdminEmployeeRoleApiTest.php`**
   - `test_phan_cong_chi_ghi_dong_cua_C`: the main-company case with all=true now asserts the department row at C is **kept**. It previously asserted the row was deleted.
   - New `test_luu_khong_doi_co_tat_ca_giu_dong_phong_ban`:
     - Main company with the flag and 1 row: saving unchanged (all=true, the row sent) keeps the row and its part_ids, and the flag stays 1.
     - Concurrent: saving all=true twice leaves exactly 1 NULL flag row, and the department row is kept.
   - New `test_bo_co_tat_ca_xoa_ca_2_nguon_co`: a main-company employee with the `company_employees` flag plus a NULL row, saved with all=false and 1 department, ends with flag 0, only that 1 row (all_department 0), and detail `all_department` false.
   - New `test_cong_ty_chinh_chi_co_dong_co_NULL_bao_tat_ca`: a main-company employee with only the NULL-row flag gets detail `all_department` true, which agrees with `employeeManagesAllDepartmentsIn`.
3. **FE `EmployeeRoleManageDepartments.vue`**
   - When "Quản lý tất cả phòng ban" is ticked, the existing rows stay visible but **read-only**: the selects are disabled, there is no delete button and no "Thêm phòng ban".
   - New note: "Các dòng phân công cũ vẫn được giữ (N dòng, chỉ xem) — bỏ tick để sửa." The amber warning is removed.
   - `_id/index.vue` `buildPayload` now always sends `manage_departments` as they are, including when the flag is ticked.
4. **FE badge**
   - Main company: `variant="brand"` (green #15803d on #dcfce7).
   - Concurrent: `variant="status-draft"` (amber #b45309 on #fef9c3).
   - `status-ok` has the same color as `brand`, so it could not tell the two apart. I chose `status-draft` for that reason; this is noted in a template comment.

### Commands
- `php vendor/bin/phpunit tests/Feature/Rbac/AdminEmployeeRoleApiTest.php` ⇒ `OK (16 tests, 148 assertions)` (13 tests before, plus 3 new).
- `php vendor/bin/phpunit tests/Feature/Rbac` ⇒ `OK (235 tests, 6354 assertions)`.
- `php -l` is clean on the service.
- No CRLF in the touched files. The raw-tag grep is empty. `nuxt3011.log` has 0 ERROR lines.

### Rehearsal count from the review
`SELECT COUNT(*) FROM employee_manage_departments emd JOIN employees e ON e.id=emd.employee_id JOIN employee_infos ei ON ei.id=e.employee_info_id WHERE emd.department_id IS NULL AND emd.all_department=1 AND emd.company_id=ei.company_id` ⇒ **0**.

### Playwright (rehearsal, namdangit, 1 tab, closed at the end)
- **NV 13, opened only, NOT saved.**
  - Checkbox ticked; 22 rows shown; 44 `.select2-container--disabled` (2 per row); 0 delete buttons.
  - Note: "Nhân viên quản lý mọi phòng ban, bộ phận của TPE. / Các dòng phân công cũ vẫn được giữ (22 dòng, chỉ xem) — bỏ tick để sửa."
  - DB afterwards is unchanged: 22 rows at TPE, `company_employees` flag 1.
- **NV 147 test case, restored exactly afterwards**
  1. Added department 58 (BDH, no parts) and saved. PUT `manage_departments:[{58,[]}]`, all false ⇒ 200.
  2. Reopened, ticked "tất cả": 1 row shown, 2 disabled select2, 0 delete buttons, no Thêm button, note as above. Saved: PUT `all_department:true, manage_departments:[{58,[]}]` ⇒ 200. DB: `company_employees(147,1).all_department = 1`, and row 414 (department 58) is **kept**.
  3. Reopened: loads with the flag on and the row read-only (same numbers). Unticked, deleted the row, saved: PUT `all_department:false, manage_departments:[]` ⇒ 200.
- **Badge**
  - 147: class `v2-badge--brand`, color rgb(21,128,61) on rgb(220,252,231), text "Công ty chính tại TPE".
  - 407: class `v2-badge--status-draft`, color rgb(180,83,9) on rgb(254,249,195), text "Kiêm nhiệm tại TPE".

### Cleanup (rehearsal)
- The 3 saves wrote `employee_permission_history` 53, 54 and 55, which I deleted: `DELETE FROM employee_permission_history WHERE id IN (53,54,55) AND employee_id=147;` (3 rows).
- Row 414 was removed by the 3rd save in the UI.
- State after: `company_employees(147)` = {1: 0, 8: null}; `employee_manage_departments(147)` = 0; roles [100004, 100005, 108451]. History max id is 50 again. This equals the before state.
- Residual: `company_employees(147,1).updated_at` changed; its value is the same.
