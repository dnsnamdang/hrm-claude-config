# Task 6 report: FE Màn 2 "Vai trò nhân viên" (/admin/employee-roles)

Status: DONE_WITH_CONCERNS. Nothing committed, no migration, no seeder, no writes to the DB.

## Files (hrm-client wt-rbac, all LF)
- New `pages/admin/employee-roles/index.vue`: the list page. Its header comment records the list-page exception (no Người tạo/Ngày tạo columns).
- New `pages/admin/employee-roles/components/GrantedPermissionsModal.vue`: `open(employeeId)`, built on V2BaseModal (xl) + V2BaseTabNavigation + V2BaseDataTable.
- New `pages/admin/employee-roles/components/EmployeeRoleHistoryModal.vue`: wraps CatalogHistoryModal with `endpoint-base="setting-histories"` and type `employee_permission`. It calls `open(id, label)`.
- Restored from `25824b310^:components/timesheet/setting/roles/` with `git show` (no checkout) into `pages/admin/employee-roles/components/`:
  - `BulkPermissionModal.vue`, `BulkPermissionFilter.vue`, `BulkPermissionEmployeeList.vue`, `BulkPermissionBanner.vue` (Banner unchanged).
- Modified `components/subsystem-menu/admin.js`: "Danh sách người dùng" (/timesheet/setting/employees) becomes "Vai trò nhân viên" → `/admin/employee-roles`, isShow `['Quản lý phân quyền']`.

## What was built
- **List**
  - Columns STT · Mã NV (link `/admin/employee-roles/:id`) · Email · Tên · Phòng ban · Vai trò tại công ty này · Loại · Người cập nhật · Cập nhật lúc · Hành động.
  - Hidden by default: Bộ phận, Công ty chính, Công ty làm việc, Trạng thái tài khoản (V2BaseBadge using BE `status_color`).
  - Filters: quick search plus Phòng ban, Bộ phận (follows the chosen Phòng ban), Vai trò (multiple), Loại, Trạng thái tài khoản, Chưa có vai trò nào.
  - Filter options come from `bulk/options`, so they only list company C.
  - `role_ids` is sent as `role_ids[]=` because buildQueryString repeats the key and PHP would otherwise keep only the last value.
  - Toolbar: Phân quyền hàng loạt · Xuất Excel (ExportFieldsModal, keys match `ExportColumnRegistry['admin_employee_roles']`) · Tuỳ chỉnh cột.
  - Row actions: Sửa (link to the Task 7 page) · Quyền đang được cấp · Lịch sử.
  - A 403 on the list redirects to `/pages/extras/404`.
  - Mixins: filterStateMixin, columnCustomizationMixin (key `admin_employee_roles`), exportFieldsMixin, DedupeLoadMixin.
- **Role chips**
  - Up to 3 chips, then "+n" with a `v-b-tooltip` that lists all names (`roles_text`).
  - Clicking a chip opens `RolePermissionsViewModal.open({id, base_name})`. That GĐ2 file is unchanged.
- **GrantedPermissionsModal**
  - Subtitle: `Mã - Tên · Vai trò tại <C> (công ty đang làm)`.
  - One tab per role. The tab label is the role name plus " · n trùng" when n > 0; the tab count shows the number of permissions.
  - The last tab is "Phòng ban đang quản lý", with one block per company: "Công ty chính — <mã>" and "Kiêm nhiệm — <mã>". A block with all departments shows a single row; a block with nothing assigned shows "Chưa phân công phòng ban nào."; a row with no parts shows "Tất cả bộ phận".
  - Role tabs group permissions by phân hệ, with columns Quyền · Mã quyền · Loại · Phạm vi.
  - Duplicate permissions get a red row, red name and a "Trùng: …" tag, plus a warning bar with the count. This is the user-approved exception to the red rule.
  - A locked role shows a grey note.
- **Bulk popup**
  - Same UI as before: b-modal xl, max-width 1450px.
  - Endpoints moved to `admin/employee-roles/bulk/{options,eligible,preview,export,apply}`.
  - The parent loads `bulk/options` once per open and passes it to both child components. The old 6 global catalog endpoints and `timesheet/employees?limit=9999` are gone.
  - The "Nhân viên" sub-filter uses `bulk/eligible` with an empty filter, which returns every employee of C.
  - The header shows "Công ty: <code> — <name>", and there is a one-line scope note.
  - "Chọn quyền" is now "Chọn vai trò", and the messages say "vai trò".
  - Only grant mode exists (the selector stays hidden, as before).
  - Apply errors use `apiErrorMessage` so 422 messages are readable. After a successful apply the popup emits `applied` and the list reloads.

## Playwright on rehearsal (8011/3011), DOM measurements
namdangit (id 13), C = TPE (id 1):
- **List rows**
  - 10 rows; their codes match the API page 1 codes one for one.
  - Footer "Hiển thị 1–10 / 830" against API `meta.total` 830.
  - Header: "Danh sách vai trò nhân viên — TPE". 10 `th` cells in the right order.
- **Chips**
  - Employee 195 has 7 roles: 3 chips plus "+4". The tooltip shows all 7 names.
  - Chip style: 11px, radius 999px, background rgba(100,116,139,0.1), cursor pointer.
  - Clicking a chip opened "Quyền đang có — Quản lý_TPE" with 103 `.perm-row`.
- **Row actions:** titles are [Sửa, Quyền đang được cấp, Lịch sử].
- **Filters through the UI state**
  - kind=concurrent: 35, all "Kiêm nhiệm".
  - role_ids=[8,31]: 42; the request was `role_ids[]=8&role_ids[]=31`.
  - no_role=1: 66.
  - keyword "Cao Thị Thùy Linh": 1.
  - All four equal the API totals.
- **Granted popup for 195**
  - Tab labels and counts equal the API: 103/5 trùng, 1, 93/4, 66/62, 174/125, 215/196, 203/189, plus "Phòng ban đang quản lý".
  - Quản lý_TPE tab: 103 rows, 5 `tr.gp-dup` (API 5).
  - Kiểm soát tab: 215 rows, 196 dup (API 196).
  - Colors: duplicate name and tag `rgb(220, 38, 38)`, normal name `rgb(52, 58, 64)`.
  - Department tab: TPE main with 2 rows, TPHP and TPV concurrent, each "Chưa phân công phòng ban nào." This matches the API.
  - Dialog width is 1140px at a 1440px viewport.
  - Bug found and fixed: there were 2 nested scrollbars, because V2BaseDataTable's `.table-wrapper` has max-height 640px inside a 680px modal body. A scoped override fixed it. Measured after the fix: wrapper max-height none, wrapper height equals table height (688px), card padding and border 0.
- **Concurrent employee 407** (Cao Thị Thùy Linh, TPE+TPV, kiêm nhiệm at TPE)
  - 1 tab "Nhân viên kinh doanh 15", 15 rows, no dup bar.
  - Department blocks: "Công ty chính — TPV" with 3 rows, each "Tất cả bộ phận"; "Kiêm nhiệm — TPE" empty.
- **History:** title "Lịch sử thay đổi: 10310003 - Nguyễn Thị Mỹ Dung". `setting-histories/employee_permission/195` and its filter-options returned 200; the body says "Chưa có lịch sử thao tác nào." and the dialog is 800px wide.
- **Bulk popup**
  - Dialog 1440px wide at a 1440px viewport, computed max-width 1450px, class `modal-xl`. This is the same as the old file: `size="xl"` + `/deep/ .modal-xl { max-width: 1450px }`.
  - Header "Công ty: TPE — CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT". Section titles [Đối tượng phân quyền *, Chọn vai trò *].
  - Option counts: Khối 4, PB 25, BP 11, CV 113, CD 142, NV bổ sung 425, Vai trò 101. These equal `bulk/options` and `eligible`.
  - Checked against the DB (tinker on rehearsal), the DOM option ids belonging to another company or inactive were: departments 0, parts 0, khối 0, roles 0 (inactive roles also 0).
  - For comparison: C has 25 active departments out of 78 in total, and 101 active roles out of 283.
  - Ticking "Tất cả" on Phòng ban gave preview totals of 400, 10 rows, and footer "Tổng SL NV sẽ cập nhật: 400".
  - **Áp dụng was not clicked.**
- **Menu:** the admin rail shows `/admin/employee-roles` "Vai trò nhân viên", and `/timesheet/setting/employees` no longer has a link.
- **No-permission user** (employee id 789, taipg.cshn@tanphat.com: works at TPE, no roles at TPE, no direct "Quản lý phân quyền")
  - API returns 403 for `admin/employee-roles`, `bulk/options` and `195/effective-permissions` (curl).
  - The browser ended up on `/pages/extras/404` with no chips rendered. The redirect happened before the page's own API call (route guard).
- Tabs: one tab was used and then closed (`browser_close`). Nuxt log after line 8470: no ERROR and no employee-roles warnings.

## Test data and cleanup
- No DB writes. Apply was not run.
- I only issued JWTs through tinker for ids 13 and 789; the tokens are in scratchpad `t6_jwt13.txt` and `t6_noperm_jwt.txt`.

## Self-check
- `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/admin/employee-roles/ | grep -v V2Base` returns nothing.
  - The old `<label class="col-form-label">` tags became `<div class="col-lg-2 col-form-label">`, which looks the same.
  - The raw close `<button>` became `<b-button-close>`, which renders the same `button.close`.
- No `vi-VN` number formats; numbers use `toLocaleString('en-US')`. No `.text-muted`; grey is #6b7280. No CRLF.

## Concerns
1. **The bulk popup stays on b-modal**, not V2BaseModal, and the restored files keep raw `b-form-checkbox`, `b-form-radio-group`, `b-table`, `b-form-select` and `b-pagination`. Design 4.5 says to keep the popup UI unchanged, and the width must match the old one. They pass the project grep, but they are not V2Base* components.
2. **"Loại" column and "Loại" in the popup are plain text**, where the mockup shows badges. The BE returns only `kind_text`, without a color, and the CLAUDE.md rule forbids the FE choosing badge colors. Adding `kind_color` to EmployeeRoleResource (BE Task 2) would allow the mockup badges.
3. **Row actions:** 3 actions with V2BaseRowActions `maxInline=3` all render inline, so the mockup's "⋮ Lịch sử" menu does not appear. This is the same as Màn 1 (deferred note in T5).
4. **The duplicate count sits inside the tab label** as text (" · n trùng"), not a separate red pill. V2BaseTabNavigation has a single `count` slot and no label slot, and I did not modify that shared component.
5. **A part-less manage row is shown as "Tất cả bộ phận"**, following the mockup and the old semantics (empty `part_ids` means the whole department). The BE returns `part_names: []` with no explicit flag.
6. **The Sửa link and the Mã NV link go to `/admin/employee-roles/:id`**, which is Nuxt's 404 until Task 7 creates `_id/index.vue`.
7. **The bulk export still uses the old blob + `<a download>` code**, with the filename `phan_quyen_hang_loat.xlsx`. This is the known Safari pattern; it is kept to leave the popup unchanged.

## Fix round 1

Nothing committed. No DB writes; the rehearsal data was only read.

### Changes
1. **[Important] Text for departments with no parts in the "Phòng ban đang quản lý" tab**
   - BE `hrm-api/app/Services/Admin/EmployeeRoleService.php::departmentsAllCompanies`: every row now carries `part_ids` (int[] exactly as stored, including ids of deleted parts), next to `part_names`.
     - **Task 3 contract change:** `departments[].rows[]` = `{department_name, part_ids:[int], part_names:[...]}`.
   - FE `GrantedPermissionsModal.vue::departmentRows`:
     - No `part_names` and `part_ids` empty: shows "Chưa chọn bộ phận".
     - No `part_names` but `part_ids` present: shows "Bộ phận đã xoá".
     - Both are grey #6b7280 italic (class `.gp-part-none`). The text "Tất cả bộ phận" is removed.
     - Reason: `PermissionHelper::managePartIdsOf` gives no part ids for an empty row, so permissions scoped to parts see nothing there.
   - Test `tests/Feature/Rbac/AdminEmployeeRoleBulkTest.php::test_effective_departments_chia_chinh_kiem_nhiem`:
     - Added 2 rows at C1: `part_ids` NULL, and `part_ids` '987654321' (a part that does not exist).
     - Asserts the 3 rows `{department_name, part_ids:[part], part_names:[name]}`, `{…, part_ids:[], part_names:[]}`, `{…, part_ids:[987654321], part_names:[]}`.
2. **[Minor] Department filter change fired 2 list loads**
   - `index.vue`: removed the `filters.department_id` watcher.
   - `handleFilterChange` now clears `part_id` in the same change when it does not belong to the new department, so the deep watcher runs once.
   - `loadData` has a sequence guard (`loadSeq`): a late response from an older load is ignored, and only the latest load updates the data and `loading`.
3. **[Minor] `GrantedPermissionsModal.open()` stale responses and 404 message**
   - Added `requestToken`: every open and every reset (close) increments it, and a stale response or error is ignored.
   - A 404 shows the toast "Nhân viên không làm việc ở công ty này". The axios interceptor does not handle 404, so there is no duplicate toast.
4. **[Minor] Duplicate `bulk/eligible` request when opening the bulk popup**
   - `BulkPermissionModal.loadOptions` now calls only `bulk/options`.
   - `BulkPermissionFilter.loadEligibleAdditional` emits `company-employees` when the request was made with an empty main filter. The flag is read before the await. The popup keeps that list as the source for the "Nhân viên" sub-filter.

### Tests
- `php vendor/bin/phpunit tests/Feature/Rbac/AdminEmployeeRoleBulkTest.php` ⇒ `OK (5 tests, 106 assertions)`
- `php vendor/bin/phpunit tests/Feature/Rbac` ⇒ `OK (232 tests, 6335 assertions)`

### Playwright (rehearsal, namdangit; 1 tab, closed afterwards)
- **Rows without parts exist in rehearsal**
  - `employee_manage_departments` has 316 rows with a department and an empty `part_ids`. NV 195 at TPE has 2 of them (departments 66 and 57, `part_ids` NULL).
  - Department tab for 195: "BAN KIỂM SOÁT · Chưa chọn bộ phận" and "PHÒNG KIỂM SOÁT NỘI BỘ · Chưa chọn bộ phận", color `rgb(107, 114, 128)`, `font-style: italic`.
  - "Bộ phận đã xoá": there is 1 such row in rehearsal (NV 1296, company 9, `part_ids` "2"). That employee does not work at TPE, so I could not open it from TPE. This case is covered by the BE test only.
- **Department change**
  - Set department 36 and part 25, then switched to department 58.
  - Result: exactly 1 list request (`department_id=58&page=1&per_page=10`), and `part_id` went from '25' to ''.
- **Bulk popup open**
  - 1st open: requests `[options, preview, eligible]`, so 1 `eligible`.
  - 2nd open: `[options, preview, eligible]` again, so 1 `eligible`.
  - The "Nhân viên" sub-filter has 425 options both times (the employees of C, same as before).
- **Granted popup**
  - `open(1296)` (not at TPE): toast "Nhân viên không làm việc ở công ty này" and the popup closed.
  - Fast `open(407)` then `open(195)`: the popup shows 195 ("10310003 - Nguyễn Thị Mỹ Dung …", 8 tabs), not 407.
- Nuxt log after line 8470: no ERROR. The raw-tag grep returns nothing. All touched files are LF.
