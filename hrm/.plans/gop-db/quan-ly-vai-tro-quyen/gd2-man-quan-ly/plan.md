# GĐ2 — Màn quản lý Vai trò & Quyền · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (user giao Claude tự làm, chạy native). Steps dùng `- [x]`.

**Goal:** Màn Vai trò (danh sách, thêm/sửa, khoá, xoá, phân quyền theo mã + phạm vi, lịch sử) ở phân hệ Quản trị HRM, phục vụ cả ERP và HRM; gỡ màn phân quyền cũ ở 2 nền tảng.

**Architecture:** API mới `/admin/roles` trong `app/` của hrm-api, luôn bó theo công ty đang làm việc (`current_company_role`), ghi log vào `role_permission_history` qua adapter có sẵn. FE Nuxt 2 khuôn `pages/admin/benefit-rates` (V2BaseSmartFilterPanel + V2BaseDataTable + popup V2BaseModal); màn phân quyền tải 1 lần catalog + quyền đã gán, dựng cây và lọc ở FE. `PermissionChecker` (2 repo, giống từng byte) thêm điều kiện vai trò đang hoạt động.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Laravel 6 (ERP), Nuxt 2.14 / Vue 2 / Bootstrap-Vue (hrm-client), PHPUnit, Playwright MCP.

**Spec:** `gd2-man-quan-ly/design.md` (+ `../design.md`, `../gd1-nen-du-lieu/design.md`).

## Global Constraints

- Repo/nhánh: `wt-rbac/hrm-api` (`rbac`), `wt-rbac/TanPhatDev` (`rbac`), `wt-rbac/hrm-client` (worktree mới, nhánh `rbac` từ `gop_db` `cdbdc223b`). Không migration, không seeder, không commit (user tự báo).
- DB test: `hrm_erp_rbac_test` (`.env` của wt-rbac/hrm-api). PHP: `/opt/homebrew/opt/php@7.4/bin/php`. Test ERP: `php -d variables_order=EGPCS vendor/bin/phpunit`.
- Gate mọi API + màn: `checkPermission:Quản lý phân quyền` (alias → `admin.phan_quyen.manage`).
- `company_id` luôn lấy từ `auth()->user()->current_company_role`; vai trò khác công ty ⇒ **404**.
- Nhãn màn hình: **"Vai trò"**, cấm chữ "chức vụ" trong code/nhãn mới.
- `name` = `"{companies.code}_{base_name}"` (quy tắc `RoleSplitter`); trùng `base_name` cùng công ty ⇒ 422 `Đã tồn tại trên hệ thống`. `base_name` max 150, `description` max 500.
- Phạm vi: `PermissionScope` 1 Bộ phận · 2 Phòng ban · 3 Công ty · 4 Tổng công ty; quyền `allowed_scopes` NULL/rỗng ⇒ `scope` null.
- Vai trò khoá (`status = 0`): sửa/phân quyền/xoá ⇒ 423 `Vai trò đang bị khoá, vui lòng mở khoá trước khi cập nhật.`
- Sau mọi ghi: `PermissionChecker::flush()` + `app('cache')->forget('spatie.permission.cache')`.
- FE: chỉ `V2Base*`, `BaseConfirmModal`/`$confirm`, `V2Footer`, `unsavedChangesMixin`/`unsavedModalMixin`, badge màu do BE trả (`#16A34A` Hoạt động, `#DC2626` Đã khoá), số `toLocaleString('en-US')`, chữ đỏ chỉ cho lỗi.
- Cờ quyền FE mặc định `false`.

## Review Focus

1. Gọi API với `id` vai trò công ty khác (sửa URL) ⇒ 404 ở MỌI endpoint, kể cả `permissions` và `setting-histories/role_permission/{id}`. → test ở Task 2, 3, 4.
2. Lưu quyền gửi mã đã `deprecated_at` mà vai trò đang giữ từ trước ⇒ không bị xoá ngầm, không 422 (FE không hiện nên không gửi lại). → Task 3 test `keeps_deprecated_grants`.
3. Sao chép quyền từ vai trò công ty khác qua API ⇒ 422 (`exists` lọc theo công ty). → Task 2 test.
4. Hai người cùng lưu quyền một vai trò ⇒ bản sau đè, lịch sử có cả 2 lượt, không lỗi khoá ngoại. → Task 3 transaction + test hai lần PUT liên tiếp.
5. Tìm nhanh bằng mã có dấu chấm / chữ hoa (`SALE.Quotation`) ⇒ vẫn khớp (so không phân biệt hoa thường). → Task 6 kiểm Playwright.

---

### Task 1: Checker bỏ qua vai trò đã khoá (2 repo)

**Files:**
- Modify: `wt-rbac/hrm-api/app/Support/Permissions/PermissionChecker.php` (`loadGrants`, `holders`, docblock dòng 16)
- Modify: `wt-rbac/TanPhatDev/app/Support/Permissions/PermissionChecker.php` (chép nguyên file từ hrm-api)
- Test: `wt-rbac/hrm-api/tests/Feature/Rbac/PermissionCheckerTest.php`, ERP `tests/Unit/Rbac/*Checker*` (bản ERP đang có)

- [x] Viết test `test_locked_role_grants_nothing` (fixture `GateFixture`: set `roles.status = 0` cho R1 ⇒ `PermissionChecker::for(E, C1)->has('zz.gate_test.view') === false`, `holders('zz.gate_test.view','api',C1) === []`); thêm `test_unlocked_role_grants_again`.
- [x] Chạy ⇒ FAIL.
- [x] Thêm `->where('r.status', 1)` vào 2 truy vấn; sửa docblock "lọc roles.status = 1".
- [x] Chạy test Rbac hrm-api ⇒ PASS. Chép file sang ERP, `diff` 2 file rỗng, chạy test Rbac ERP ⇒ PASS.

### Task 2: API vai trò — danh sách, thêm, sửa, khoá, xoá

**Files:**
- Create: `app/Http/Controllers/Api/Admin/RoleController.php`, `app/Services/Admin/RoleManagementService.php`, `app/Http/Requests/Admin/RoleStoreRequest.php`, `RoleUpdateRequest.php`, `app/Http/Resources/Admin/RoleResource.php`
- Modify: `routes/api.php` (nhóm `admin/roles`)
- Test: `tests/Feature/Rbac/AdminRoleApiTest.php`

**Interfaces (Produces):**
- `RoleManagementService::findOwned(int $id): Role` — `abort(404)` nếu `company_id ≠ current_company_role`.
- `RoleManagementService::assertUnlocked(Role $r): void` — `abort(423, msg)`.
- `RoleManagementService::log(int $roleId, string $action, array $old, array $new): void` — chèn `role_permission_history` (`changed_by = auth()->id()`).
- `RoleManagementService::afterWrite(): void` — flush 2 cache.
- `RoleResource` trả: `id, base_name, description, status, status_text, status_color, permissions_count, holders_count, is_can_edit, is_can_delete, updated_by_name, updated_at` (dd/mm/yyyy HH:mm).
- `is_can_delete` = `status == 1 && holders_count == 0 && !referenced` (tham chiếu tra `app/Support/Permissions/Convert/role-references.php`).

Routes: `GET /admin/roles` (`keyword`, `status`, `page`, `per_page`), `GET /admin/roles/options`, `POST /admin/roles` (`base_name`, `description`, `copy_from_role_id?`), `PUT /admin/roles/{id}`, `DELETE /admin/roles/{id}`, `POST /admin/roles/{id}/lock`, `POST /admin/roles/{id}/unlock`.

- [x] Viết test (JWT `claims(['current_company'=>C1])` như `BulkRoleGrantTest`):
  `test_list_only_current_company`, `test_requires_permission` (403), `test_other_company_role_404` (PUT/DELETE/lock),
  `test_store_prefixes_name` (`name === "{code C1}_Kế toán"`, `company_id = C1`, `guard_name = 'api'`), `test_store_duplicate_base_name_422`,
  `test_same_base_name_other_company_ok`, `test_store_copy_permissions` (rhp + scope giống nguồn), `test_copy_from_other_company_422`,
  `test_update_locked_423`, `test_lock_removes_effective_permission` (holder mất mã qua checker), `test_delete_with_holder_422`, `test_delete_ok_logs_history`.
- [x] Chạy ⇒ FAIL. Implement. Mỗi thao tác ghi log: `create` (`base_name, description, copy_from`), `update` (trường đổi), `lock`/`unlock`, `delete` (snapshot `base_name, description, permissions[]`).
- [x] Chạy `AdminRoleApiTest` + toàn bộ `tests/Feature/Rbac` ⇒ PASS.

### Task 3: API phân quyền cho vai trò

**Files:**
- Modify: `RoleController.php`, `RoleManagementService.php`
- Create: `app/Http/Requests/Admin/RolePermissionsRequest.php`
- Test: `tests/Feature/Rbac/AdminRolePermissionsApiTest.php`

**Interfaces:**
- `GET /admin/roles/{id}/permissions` ⇒ `{ role: RoleResource, catalog: [{code, name, subsystem_group, subsystem, feature, kind, allowed_scopes:int[], depends_on:string[], on_erp, on_hrm}], grants: [{code, scope}] }` — catalog bỏ `deprecated_at`, sắp theo thứ tự catalog (id).
- `PUT /admin/roles/{id}/permissions` body `{ grants: [{code, scope}] }` ⇒ 200 `{ added, removed, changed }`.

- [x] Viết test: `test_get_returns_catalog_and_grants`, `test_put_replaces_grants`, `test_put_unknown_code_422`, `test_put_invalid_scope_422` (scope ngoài `allowed_scopes`; scope ≠ null cho quyền không phạm vi), `test_keeps_deprecated_grants`, `test_put_locked_423`, `test_other_company_404`, `test_put_logs_diff` (action `permissions`, new_value có `added/removed/changed` kèm mã + tên), `test_put_twice_in_a_row`, `test_put_flushes_checker` (holder có quyền mới ngay).
- [x] Implement trong 1 transaction: xoá rhp của vai trò trừ quyền đã ngừng dùng, chèn lại `(permission_id, role_id, company_id = roles.company_id, scope)`.
- [x] Chạy ⇒ PASS.

### Task 4: Lịch sử + gỡ route cũ (hrm-api)

**Files:**
- Modify: `app/Services/SettingHistory/Adapters/RolePermissionAdapter.php`
- Modify: `Modules/Timesheet/Routes/api.php` (nhóm `timesheet/roles`)
- Test: `tests/Feature/Rbac/RoleHistoryAdapterTest.php`

- [x] Test: `authorize` theo `roles.company_id` (công ty khác false; vai trò đã xoá ⇒ đọc `company_id` trong snapshot log `delete`); `mapRow` hiển thị được log cũ (snapshot) và log mới `create/update/permissions/lock/unlock/delete`; nhãn không còn chữ "chức vụ".
- [x] Sửa adapter: `actionLabels` = Tạo mới vai trò / Cập nhật vai trò / Cập nhật phân quyền / Khoá vai trò / Mở khoá vai trò / Xoá vai trò; `fieldLabels` `base_name` Tên vai trò, `description` Mô tả; lock/unlock vào nhóm màu "Thay đổi trạng thái" (`colorOf`). Log `delete` mới ghi `company_id`.
- [x] Rà hrm-client: `grep -rn "timesheet/roles" pages components store utils`. Giữ `GET /timesheet/roles/list` nếu màn người dùng cũ còn gọi; gỡ `store`, `/`, `export`, `histories`, `{id}` show/delete khỏi route và `RoleController` cũ. Ghi lại route còn giữ vào design §10.
- [x] Chạy toàn bộ `tests/Feature/Rbac` + `tests/Unit/Rbac` ⇒ PASS.

### Task 5: FE — worktree, menu, danh sách, popup Thêm/Sửa, Quyền đang có, Lịch sử

**Files:**
- Worktree: `git -C HRM/hrm-client worktree add ../../../wt-rbac/hrm-client -b rbac gop_db`; `node_modules` cài riêng (không symlink từ checkout chính nếu Nuxt lỗi resolve — xem memory worktree).
- Create: `pages/admin/roles/index.vue` (khuôn `pages/admin/benefit-rates/index.vue`), `pages/admin/roles/components/RoleFormModal.vue`, `pages/admin/roles/components/RolePermissionsViewModal.vue`
- Modify: `components/subsystem-menu/admin.js` (mục "Vai trò" → `/admin/roles`, `isShow: ['Quản lý phân quyền']`)

- [x] Danh sách đúng design §3: cột, tìm nhanh `Tìm theo tên, mô tả vai trò`, lọc Trạng thái, hành động qua `V2BaseRowActions` (Phân quyền · Sửa · Lịch sử · Khoá/Mở khoá · Xoá; ẩn theo `is_can_edit`/`is_can_delete`/`status`), nút **Thêm mới**, không có Xuất Excel.
- [x] `RoleFormModal`: V2BaseModal + `unsavedModalMixin`, `V2BaseInput` Tên (required, max 150), `V2BaseTextarea` Mô tả (max 500), `V2BaseSelectInModal` "Sao chép quyền từ" (chỉ khi thêm, nguồn `/admin/roles/options`). Lưu xong: không sao chép ⇒ `$router.push('/admin/roles/{id}/permissions')`; có sao chép hoặc sửa ⇒ đóng + tải lại danh sách.
- [x] Khoá/Mở khoá/Xoá qua `$confirm` (khoá: "N người đang giữ vai trò này sẽ mất các quyền của vai trò").
- [x] Lịch sử: `SettingHistoryModal.open('role_permission', id, base_name)`.
- [x] `RolePermissionsViewModal`: gọi `GET /admin/roles/{id}/permissions`, hiện grants gom Phân hệ → Chức năng, mỗi dòng tên · mã · phạm vi; ô tìm; footer nút Phân quyền (ẩn khi khoá).
- [x] Playwright MCP (`http://127.0.0.1:<cổng client rbac>`, tài khoản namdangit): đo số dòng = `total` API, khoảng cách 2 nút toolbar 12px, popup footer ghim đáy, toast lỗi trùng tên hiện dưới ô (`.v2-error`), không phần tử nào chứa chữ "chức vụ".

### Task 6: FE — màn Phân quyền `/admin/roles/_id/permissions.vue`

**Files:**
- Create: `pages/admin/roles/_id/permissions.vue`, `pages/admin/roles/components/PermissionTree.vue`, `PermissionSummary.vue`, `utils/permissionTree.js` (dựng cây + lọc, hàm thuần)

**Interfaces:**
- `buildTree(catalog) => Group[]` (`{key,label,children}` 4 tầng, giữ thứ tự catalog).
- `filterTree(tree, {group, subsystem, feature, kind, platform, keyword, onlySelected}, selected) => Set<code>` mã hiển thị; `keyword` so `toLowerCase()` trên tên + mã.
- `defaultScope(perm) => max(allowed_scopes) | null`.
- `withDependencies(code, catalog) => string[]` mã cần tick kèm.

- [x] Băng tiêu đề, bộ lọc 5 ô + tìm nhanh + "Chỉ hiện quyền đã chọn", cây 4 tầng checkbox 3 trạng thái, Mở tất cả / Thu gọn, dòng quyền tên · mã (mono xám) · nhãn loại · nhãn nền tảng · ô phạm vi (`V2BaseSelect` chỉ cấp hợp lệ, mặc định cao nhất), tô vàng chữ khớp, tự mở nhánh có kết quả.
- [x] Quyền phụ thuộc: tick Thao tác ⇒ tick Xem; bỏ Xem khi còn phụ thuộc ⇒ `$confirm` bỏ luôn.
- [x] Bảng tổng hợp phải (sticky; lưu ý `.content-page overflow:hidden` — memory): tổng, theo loại, theo phân hệ (bấm cuộn tới), số thay đổi chưa lưu.
- [x] `V2Footer`: Lưu · Bỏ chọn tất cả (custom-actions) · Quay lại `/admin/roles`; `unsavedChangesMixin`; lưu xong `markFormSaved()` + về danh sách. Vai trò khoá vào bằng URL ⇒ về danh sách.
- [x] Playwright MCP: số dòng quyền render = số mã catalog sau lọc; tìm `admin.phan_quyen` mở đúng nhánh Quản trị và tô vàng; ô phạm vi của quyền Xem có phạm vi chỉ có các cấp trong `allowed_scopes`; tick 1 quyền Thao tác có `depends_on` ⇒ quyền Xem tương ứng được tick; số ở bảng tổng hợp = số ô đã tick; footer không đè dòng cuối (đo `getBoundingClientRect`); lưu xong `GET` lại khớp.

### Task 7: Gỡ màn cũ (hrm-client + ERP)

**Files:**
- Delete (hrm-client): `pages/timesheet/setting/roles/**`, `pages/human/roles/**`, component chỉ các màn đó dùng (rà `grep -rn` từng file: `components/setting/Permission.vue`, `components/timesheet/setting/roles/*`); xoá mục `/human/roles` khỏi `components/subsystems.js` nếu có.
- Create: `pages/timesheet/setting/roles/index.vue` chỉ `middleware` redirect → `/admin/roles` (route con `add/_id` cũng redirect).
- ERP: gỡ route `common/roles*` (`routes/web.php` hoặc file route phân hệ), view `resources/views/common/roles/*`, controller method chỉ màn đó dùng; mục menu ERP trỏ URL HRM `/admin/roles` (lấy base từ config HRM URL đang dùng ở ERP).

- [x] Grep trước khi xoá từng file; ghi danh sách đã xoá vào design §10.
- [x] `BulkPermissionModal` đi theo màn cũ — ghi vào design: cấp vai trò hàng loạt quay lại ở màn người dùng mới.
- [x] hrm-client build dev không lỗi resolve; ERP `php artisan route:list | grep roles` không còn route cũ; `view:cache` + mở 1 trang ERP có menu.

### Task 8: Spec e2e + chốt hồ sơ

**Files:**
- Create: `HRM/e2e/tests/admin-roles.spec.ts` (theo khuôn spec hiện có; ca có quyền / không quyền / khác công ty) — **không chạy** trừ khi user yêu cầu.
- Modify: `design.md` GĐ2 (§10 thực tế), `../design.md` bảng trạng thái, `.plans/gop-db/STATUS.md`.

- [x] Viết spec. Cập nhật hồ sơ + checkpoint.

---

### Checkpoint — 27/10/2026
Vừa hoàn thành: Task 1–8 (BE, FE, gỡ màn cũ, spec e2e chưa chạy); kiểm Playwright trên hrm_erp_rbac_rehearsal, sửa 3 lỗi phát hiện khi kiểm (ghi ở design §10).
Đang làm dở: — review cuối xong, sửa C1/I1/I3; rulings + minor hoãn ở ledger `wt-rbac/hrm-api/.superpowers/sdd/gd2-plan/progress.md`.
Bước tiếp theo: commit 27/10 (hrm-api `80de7580b`, hrm-client `25824b310`, ERP `f9b85744c5`), chưa push; e2e 9/9 xanh.
Blocked:
