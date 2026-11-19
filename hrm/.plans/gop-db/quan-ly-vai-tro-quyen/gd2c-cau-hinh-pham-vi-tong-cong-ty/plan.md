# GĐ2c — Cấu hình công ty được cấp phạm vi "Tổng công ty" · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans. Steps dùng `- [ ]`.

**Goal:** Chỉ công ty được bật `companies.allow_group_scope` mới cấp được phạm vi Tổng công ty; công ty bị tắt thì phạm vi
này tính như Công ty lúc kiểm quyền (HRM + ERP), dữ liệu giữ nguyên. Chỉ tài khoản trong `RBAC_GROUP_SCOPE_ADMINS` được
bật/tắt, qua màn mới `/admin/group-scope-companies`.

**Architecture:** 1 lớp `GroupScopeConfig` (bản giống hệt ở hrm-api + ERP) đọc cột `companies.allow_group_scope`, nhớ trong
request. Chặn ở **một chỗ** là `PermissionChecker::loadGrants()` + `holdersQuery()` của 2 repo — mọi đường đọc phạm vi đều đi
qua đây (đã soát 01/11). Màn sửa quyền vai trò ẩn lựa chọn + BE 422 khi cấp mới. Màn cấu hình gate bằng danh sách `.env`,
không phải mã quyền.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Laravel 6 (ERP TanPhatDev), Nuxt 2.14 / Vue 2 (hrm-client), PHPUnit, Playwright MCP.

**Spec:** `design.md` cùng folder (chốt 01/11/2026, hết câu hỏi tồn); nền `../design.md` §5.

## Global Constraints

- Repo/nhánh: `wt-rbac/hrm-api`, `wt-rbac/TanPhatDev`, `wt-rbac/hrm-client` — nhánh `rbac`. **Code chỉ bắt đầu khi user
  nói "làm" kèm phạm vi** (CLAUDE.md). Không commit khi user chưa bảo; không push; không merge `gop_db` khi chưa yêu cầu.
- **Đúng 1 migration**: `hrm-api/database/migrations/2026_11_02_000010_add_allow_group_scope_to_companies.php`
  (`tinyInteger('allow_group_scope')->default(1)` sau `branch_order`; không UPDATE dữ liệu). Chạy vào DB nào cũng phải
  liệt kê + hỏi riêng, chạy lẻ `--path`. Không seeder.
- DB PHPUnit: `hrm_erp_rbac_test`. Kiểm UI: `hrm_erp_rbac_rehearsal` — chỉ đọc; muốn tắt thử 1 công ty để kiểm thì hỏi trước,
  kiểm xong trả lại 1.
- API worktree chạy UI: `php -S 127.0.0.1:8012 -t public server.php` kèm env `DB_DATABASE*` **và** `DB_CONNECTION_TPE`,
  `DB_HOST_TPE`, `DB_PORT_TPE`, `DB_USERNAME_TPE`, `DB_PASSWORD_TPE`, `DB_DATABASE_TPE` (.env worktree thiếu ⇒ màn Tài khoản
  500 "Unsupported driver []"). Nuxt: `NUXT_BUILD_DIR=.nuxt-rbac DEV_SERVER_PORT=3012 BASE_API_URL=http://127.0.0.1:8012`, node 12,
  heap 8192. Đăng nhập Playwright: `localStorage.access_token` = JWT NV13 lấy qua tinker. Xong thì kill đúng PID.
- Test hrm-api: `DB_DATABASE=hrm_erp_rbac_test DB_DATABASE_SECOND=… DB_DATABASE_TPE=… php vendor/bin/phpunit tests/Feature/Rbac`.
  Test ERP: `DB_CONNECTION=mysql DB_DATABASE=hrm_erp_rbac_test php -d variables_order=EGPCS vendor/bin/phpunit tests/Feature/Rbac`.
  ⚠️ Mốc giờ trong test ≤ 2037 (cột TIMESTAMP — 2999 lưu thành 0 im lặng).
- Không có ngoại lệ Super Admin. Danh sách `.env` rỗng ⇒ fail-closed (403 mọi tài khoản).
- Sau mọi lần bật/tắt: `GroupScopeConfig::flush()` + `PermissionChecker::flush()`. ERP: chỉ nhớ trong request; nếu thấy cache
  ngoài request thì xoá đúng khoá, KHÔNG `cache:clear` (redis chung).
- FE: `V2Base*`, `$confirm` (base-confirm-modal), badge màu do BE trả, cờ quyền mặc định `false`, sắp danh sách cập nhật
  mới nhất lên đầu.

## Review Focus

1. Công ty bị tắt: mọi đường đọc phạm vi (DataScope, CurrentPermission, `allows`, alias `min_scope = 4`, ERP `Employee::1662`)
   đều ra 3 — không còn đường nào đọc thẳng `rhp.scope` mà bỏ qua chặn. → Task 2, Task 3.
2. `holders(…, minScope 4)` không trả người ở công ty bị tắt (người duyệt / nhận thông báo cấp Tổng công ty). → Task 2, 3.
3. Lưu màn quyền vai trò: giữ nguyên dòng 4 cũ thì qua, cấp mới / nâng lên 4 thì 422 báo đủ mọi mã. → Task 4.
4. Tài khoản có "Quản lý phân quyền" nhưng ngoài danh sách `.env` ⇒ 403 ở cả GET/PUT; không có đường tự cấp. → Task 5.

---

### Task 1: Nền — cấu hình + cột + `GroupScopeConfig` (hrm-api)

**Files:** Create `config/rbac.php` (hoặc thêm khoá nếu đã có), `app/Support/Permissions/GroupScopeConfig.php`,
migration ở Global Constraints; Test `tests/Feature/Rbac/GroupScopeConfigTest.php`.

- [x] `config/rbac.php`: `'group_scope_admins'` đọc `env('RBAC_GROUP_SCOPE_ADMINS', '')`, tách dấu phẩy, ép int, bỏ ≤ 0.
- [x] `GroupScopeConfig`: `canManage(int $employeeId): bool`, `allows(int $companyId): bool` (static cache theo request,
      công ty không tồn tại ⇒ false), `flush()`. Đầu file ghi "bản giống hệt ở ERP".
- [x] Migration thêm cột (hỏi trước khi chạy vào `hrm_erp_rbac_test`).
- [x] Test: danh sách rỗng ⇒ `canManage` false; `"13, x,0"` ⇒ chỉ 13; `allows` đọc đúng cột, `flush` làm mới.

### Task 2: Chặn lúc kiểm quyền — hrm-api

**Files:** Modify `app/Support/Permissions/PermissionChecker.php` (`loadGrants`, `holdersQuery`, `flush`),
`app/Services/Admin/EmployeeRoleService.php` (~dòng 300–320 bảng tổng hợp quyền); Test `tests/Feature/Rbac/GroupScopeCheckTest.php`.

- [x] `loadGrants()`: `!GroupScopeConfig::allows($this->companyId)` ⇒ `scope 4 → 3`.
- [x] `holdersQuery()`: `$min >= 4` ⇒ join `companies` lọc `allow_group_scope = 1` theo `r.company_id`.
- [x] `flush()` gọi kèm `GroupScopeConfig::flush()`.
- [x] `EmployeeRoleService` tổng hợp quyền: trả phạm vi hiệu lực + cờ `scope_capped` (FE hiện "đang tính như Công ty").
- [x] Test: tắt ⇒ `scope()` 3, `allows(code, 4)` false, DataScope lọc công ty mình; bật lại ⇒ 4 ngay sau `flush`;
      `holders(minScope 4)` loại người công ty bị tắt; alias `min_scope 4` trượt; không quyền vẫn null.
- [x] Chạy cả `tests/Feature/Rbac` — xanh hết.

### Task 3: Chặn lúc kiểm quyền — ERP TanPhatDev

**Files:** Create `app/Support/Permissions/GroupScopeConfig.php` (chép y hệt, bỏ `canManage` nếu ERP không cần — giữ
file giống hệt thì để nguyên); Modify `app/Support/Permissions/PermissionChecker.php`; Test `tests/Feature/Rbac/GroupScopeCheckTest.php`.

- [x] Cùng 3 thay đổi như Task 2 (`loadGrants`, `holdersQuery`, `flush`).
- [x] `diff` 2 bản `GroupScopeConfig.php` rỗng.
- [x] Test như Task 2 phía ERP (gồm `Employee` helper dòng ~1662). Chạy cả `tests/Feature/Rbac` ERP.

### Task 4: Màn sửa quyền vai trò — BE (hrm-api)

**Files:** Modify `app/Services/Admin/RoleManagementService.php` (`permissionsData`, `updatePermissions` ~dòng 308–350,
`create` sao chép ~dòng 182); Test `tests/Feature/Rbac/AdminRolePermissionsApiTest.php` + `AdminRoleApiTest.php`.

- [x] `permissionsData` trả `role.allow_group_scope` (bool).
- [x] `updatePermissions`: công ty bị tắt + scope 4 mà dòng cũ không phải 4 ⇒ gom lỗi theo mã, 422 một lần
      (`errors.grants.<code>` = "Công ty chưa được cấp phạm vi Tổng công ty"). Dòng cũ đúng 4 giữ nguyên ⇒ qua.
- [x] `create` sao chép quyền vào công ty bị tắt ⇒ 4 → 3, lịch sử vai trò ghi đúng phạm vi đã hạ.
- [x] Test: cấp mới 4 ⇒ 422 đủ mã; giữ 4 cũ ⇒ 200 còn 4; hạ 4 → 3 ⇒ 200; công ty được bật ⇒ cấp 4 bình thường; sao chép ⇒ 3.

### Task 5: API màn cấu hình + lịch sử (hrm-api)

**Files:** Create `app/Http/Controllers/Api/V1/Admin/GroupScopeCompanyController.php`, `app/Services/Admin/GroupScopeCompanyService.php`,
`app/Services/SettingHistory/Adapters/GroupScopeCompanyAdapter.php` (khuôn `RolePermissionAdapter`); Modify `routes/api.php`
(nhóm `admin/group-scope-companies`, `auth:api`, KHÔNG `checkPermission`), payload thông tin người đăng nhập (`can_manage_group_scope`);
Test `tests/Feature/Rbac/AdminGroupScopeCompanyApiTest.php`.

- [x] `GET` danh sách công ty: mã, tên, `allow_group_scope`, số vai trò đang giữ phạm vi 4, người/lúc cập nhật; sắp cập nhật mới nhất trước.
- [x] `GET {id}/impact`: số vai trò + số người bị thu hẹp nếu tắt; cờ `is_current_company`.
- [x] `PUT {id}` `{allow_group_scope: 0|1}`: validate, ghi `updated_by`, ghi lịch sử 0 → 1 / 1 → 0, flush 2 cache.
- [x] Mọi route kiểm `GroupScopeConfig::canManage(auth()->id())` ⇒ 403. Không theo công ty đang làm.
- [x] Thay payload `me` bằng endpoint riêng `GET admin/group-scope-companies/can-manage` (không sửa `AuthNewController::userProfile` dùng chung). Menu: xem Task 7 — chờ user chốt cách gate mục menu.
- [x] Test: ngoài danh sách 403 GET/PUT/impact; có "Quản lý phân quyền" nhưng ngoài danh sách 403; `.env` rỗng 403;
      trong danh sách bật/tắt được + lịch sử 1 dòng; tắt xong `PermissionChecker` ra 3 trong cùng test.

### Task 6: Màn sửa quyền vai trò — FE (hrm-client)

**Files:** Modify `pages/admin/roles/components/PermissionTree.vue` (`scopeOptions`, `scopeText`), `pages/admin/roles/_id/permissions.vue`
(banner), chi tiết vai trò nhân viên `pages/admin/employee-roles/_id/index.vue` (nhãn `scope_capped`).

- [x] `!allow_group_scope` ⇒ bỏ option 4, trừ dòng đang giữ 4: vẫn hiện "Tổng công ty" + nhãn phụ xám-cảnh báo "đang tính như
      Công ty" (không dùng chữ đỏ), chọn được 1–3, không nâng lại 4.
- [x] Banner đầu màn khi công ty bị tắt (câu ở design §3.4), lỗi 422 hiện tại đúng dòng.
- [x] Playwright (DOM): đếm option ô phạm vi ở công ty bật/tắt; đo nhãn phụ + banner; lưu giữ nguyên 4 cũ ⇒ không lỗi.

### Task 7: Màn cấu hình — FE (hrm-client)

**Files:** Create `pages/admin/group-scope-companies/index.vue`; Modify `components/subsystem-menu/admin.js` (mục mới, hiện theo
`can_manage_group_scope`, không theo `codes` quyền).

- [x] Bảng theo `list-page`: Mã · Tên · công tắc · Số vai trò giữ Tổng công ty · Người cập nhật · Cập nhật lúc.
- [x] Tắt ⇒ gọi `impact` rồi `$confirm` nêu số vai trò/người; `is_current_company` ⇒ thêm dòng cảnh báo (Q3). Bật ⇒ lưu luôn.
- [x] Vào URL khi không có cờ ⇒ chuyển 404/403 như màn quản trị khác; menu không hiện.
- [x] Playwright (DOM): NV13 thấy menu + bảng + hộp xác nhận đúng số; NV663 không thấy menu, URL bị chặn, API 403.
      Nếu cần tắt thử trên DB rehearsal ⇒ hỏi trước, kiểm xong bật lại.

### Task 8: e2e + tài liệu go-live

- [x] Cập nhật/thêm spec e2e `HRM/e2e/tests/admin/` cho 2 màn (không tự chạy cả bộ khi user chưa yêu cầu — memory `khong-tu-chay-e2e-moi-task`).
- [x] `../gd1-nen-du-lieu/runbook-go-live.md`: thêm bước đặt `RBAC_GROUP_SCOPE_ADMINS=13` vào `.env` HRM prod + `config:cache`
      trước khi mở màn; migration này chạy cùng loạt migration `rbac`.
- [ ] `../design.md` bảng giai đoạn: cập nhật trạng thái 2c.

---

### Checkpoint — 01/11/2026
Vừa hoàn thành: design.md chốt hết Q1–Q3 (bật hết lúc go-live, admin chỉ NV 13, được tắt công ty mình); viết plan.md này.
Đang làm dở: —
Bước tiếp theo: chờ user cho phép code (hỏi kèm phạm vi 3 repo + 1 migration + DB chạy migration), bắt đầu Task 1.
Blocked: —

### Checkpoint — 01/11/2026 (code)
Vừa hoàn thành: Task 1–5 BE (hrm-api + ERP), migration `2026_11_02_000010` đã chạy vào `hrm_erp_rbac_test`; Task 6 FE trang quyền
(ẩn option 4, nhãn "Đang tính như Công ty", banner, `defaultScope` trần 3); trang `pages/admin/group-scope-companies/index.vue`
(tự chặn bằng `can-manage`). Lịch sử dùng `catalog_histories` (không thêm migration). Bật/tắt = hành động dòng (không có component công tắc).
Test bản chụp (golden) 2 repo: thêm `allow_group_scope` vào regex lọc câu kiểm quyền.
Đang làm dở: mục menu Quản trị cho màn cấu hình (chờ user chốt — mục menu gate theo `codes` lấy từ `user-profile` dùng chung).
Bước tiếp theo: chạy lại toàn bộ Rbac 2 repo → Playwright (Task 6, 7) → e2e + runbook (Task 8).
Blocked: cách gate mục menu.

### Checkpoint — 01/11/2026 (Playwright xong)
Vừa hoàn thành: menu = mã giả `admin.pham_vi_tong_cong_ty.configure` thêm vào `permission_codes` ở `AuthNewController` (user chốt);
`GroupScopeConfig::ready()` — chưa có cột thì coi mọi công ty được phép (deploy lệch migration không hỏng kiểm quyền).
Migration chạy vào `hrm_erp_rbac_rehearsal` (user cho phép). Playwright NV13: 9 công ty, bảng vừa khung 1067px, hộp xác nhận đúng số
(TPE 51 vai trò / 520 người + dòng cảnh báo công ty đang làm), màn quyền vai trò Kiểm soát: banner + tag cạnh tên, dòng giữ 4 còn option
Tổng công ty, dòng chưa giữ không có; popup Quyền đang được cấp có nhãn; lịch sử 2 lần đổi. NV663: URL → 404, API 403. TPE đã bật lại = 1.
Spec e2e `HRM/e2e/tests/admin/admin-group-scope.spec.ts` (chưa chạy — chỉ chạy khi user yêu cầu). Runbook + mục D đã bổ sung.
Rehearsal còn 4 dòng lịch sử thử ở catalog_histories (table_name = company_group_scope).
Bước tiếp theo: chờ kết quả toàn bộ Rbac 2 repo; báo user; chưa commit.

### Checkpoint — 01/11/2026 (test đầy đủ)
Vừa hoàn thành: hrm-api `tests/Feature/Rbac` OK 416/416. ERP lần đầu 108/113 — 5 ca so bản chụp đường đọc (Purchase
warningProductDeliverySearch, Sale buy-service-request / buy-service-accounting / target/company / plan/market / plan/sale) đỏ cả ở mức
`none`: cùng băm SQL, cùng số dòng, khác băm nội dung dòng. Nguyên nhân (đã kiểm chứng): các API này trả kèm bản ghi công ty, cột mới
`companies.allow_group_scope` lọt vào nội dung dòng ⇒ băm đổi. (Nhận định ban đầu "do ngày chạy" là SAI.) Sửa test: thêm
`allow_group_scope` vào `GoldenRows::VOLATILE` (ERP) — cột cấu hình, không liên quan phạm vi lọc. Hệ quả thật: API nào trả `companies.*`
nay có thêm trường `allow_group_scope` (không nhạy cảm, chỉ thêm trường).
Sau sửa: Sale 11/11 OK. Purchase còn 1 ca `warningProductDeliverySearch` — lọc `delivery_expected_time < Carbon::now()`
(`WarningProductDeliveryService:77`), đỏ cả ở mức `none` nơi không nhánh kiểm quyền nào chạy; xanh 31/10, đỏ 01/11 ⇒ lệch theo ngày,
không do GĐ2c. Muốn xanh phải chụp lại golden (RBAC_SNAPSHOT_OUT + RBAC_LEGACY_SRC bản code cũ) — chưa làm.
Bước tiếp theo: user quyết commit.
