# GĐ2c — Cấu hình công ty được cấp phạm vi "Tổng công ty"

> Hồ sơ con của `../design.md`. Ngày viết: 01/11/2026. Code trên `wt-rbac` nhánh `rbac` (hrm-api + hrm-client + ERP),
> cùng cửa sổ lên prod với GĐ1–4. **Chưa code** — code phải hỏi riêng kèm phạm vi (CLAUDE.md).
> **[user chốt 01/11]** = user nói trong hội thoại 01/11. **[Claude chốt]** = Claude tự quyết, user duyệt khi đọc hồ sơ.

## 1. Vì sao

`../design.md` §5 đang ghi: *"Quản trị viên công ty nào cũng cấp được mọi phạm vi, kể cả Tổng công ty"*. Phạm vi
Tổng công ty = **không lọc dữ liệu** (`DataScope`), nên quản trị viên một công ty con tự mở được dữ liệu gộp mọi công
ty cho người của mình. User đổi nguyên tắc này **[user chốt 01/11]**:

- Có cấu hình **công ty nào được phép cấp phạm vi Tổng công ty**. Chỉ vai trò của các công ty này mới thấy/được chọn
  phạm vi Tổng công ty.
- Chỉ **một số tài khoản cố định** được đổi cấu hình này.

⇒ Sửa `../design.md` §5 (dòng "Quản trị viên công ty nào cũng cấp được mọi phạm vi…") trỏ sang hồ sơ này.

### Hiện trạng dữ liệu (DB `hrm_erp_rbac_rehearsal`, đã `rbac:convert`, đếm 01/11)

| Công ty | Dòng gán phạm vi Tổng công ty | Số vai trò |
|---|---:|---:|
| TPE (1) | 1.785 | 51 |
| TPSG (4) | 766 | 22 |
| DTTDETEK (8) | 591 | 15 |
| TPV (3) | 515 | 19 |
| TPHP (2) | 513 | 15 |
| EG (9) | 332 | 14 |
| ETEK GREEN CU (7) | 2 | 2 |
| **Tổng** | **4.504** | **138** |

Công ty nào bị tắt thì người dùng ở công ty đó **thu hẹp từ "mọi công ty" xuống "công ty mình"** ở mọi quyền đang có
phạm vi Tổng công ty.

## 2. Chốt

| # | Nội dung | Nguồn |
|---|---|---|
| C1 | Ai được đổi cấu hình: **danh sách tài khoản cố định trong cấu hình máy chủ** (cách B). Không làm mã quyền gán qua vai trò — người có "Quản lý phân quyền" ở bất kỳ công ty nào sẽ tự gán được cho mình, cấu hình mất tác dụng | user chốt 01/11 |
| C2 | Công ty bị tắt: **giữ nguyên dữ liệu**, chỉ chặn lúc kiểm quyền (phạm vi Tổng công ty **tính như Công ty**). Bật lại là quyền cũ có hiệu lực ngay, không phải cấp lại | user chốt 01/11 (cách xử lý 1) |
| C3 | Cấu hình lưu ở cột `companies.allow_group_scope` (tinyint 0/1). DB dùng chung ⇒ ERP đọc thẳng, không đồng bộ | Claude chốt |
| C4 | Danh sách tài khoản rỗng/thiếu ⇒ **không ai** đổi được (fail-closed). Không có ngoại lệ theo Super Admin (xem memory `super-admin-khong-mac-dinh-co-quyen`) | Claude chốt |
| C5 | Vai trò ở công ty bị tắt đang giữ phạm vi Tổng công ty: **giữ nguyên dòng đó khi lưu** nếu người sửa không đổi; chỉ chặn *cấp mới* hoặc *nâng lên* Tổng công ty. Cùng khuôn "giữ vai trò khoá đang có" ở GĐ2b | Claude chốt |
| C6 | Sao chép quyền khi tạo vai trò mới ở công ty bị tắt: phạm vi Tổng công ty **hạ xuống Công ty** (vai trò mới là dữ liệu mới, không có gì để "giữ") | Claude chốt |

## 3. Thiết kế

### 3.1 Cấu hình danh sách tài khoản (hrm-api)

- `config/rbac.php` (mới hoặc thêm khoá): `'group_scope_admins' => ids(env('RBAC_GROUP_SCOPE_ADMINS', ''))` — chuỗi
  `employees.id` cách nhau dấu phẩy, ép int, bỏ giá trị rỗng/không phải số.
- Đổi danh sách = sửa `.env` máy chủ HRM + `config:cache`. Không có màn sửa danh sách.
- Chỉ hrm-api cần (màn cấu hình chỉ ở HRM). ERP **không** đọc danh sách này.
- Hàm dùng chung: `GroupScopeConfig::canManage(int $employeeId): bool`.

### 3.2 Cột dữ liệu (1 migration ở hrm-api)

`companies.allow_group_scope` tinyint NOT NULL DEFAULT 1, sau cột `branch_order`.

- **Mặc định 1 cho mọi công ty** ⇒ chạy migration xong hành vi **không đổi**; người trong danh sách tắt dần sau
  **[user chốt 01/11, Q1 = a]** — lúc go-live tắt 6 công ty ≠ 1, xem mục Q1 cuối file.
- Đọc bằng `GroupScopeConfig::allows(int $companyId): bool`, nhớ trong request (static array), `flush()` đi cùng
  `PermissionChecker::flush()`. File giống hệt ở 2 repo, như `PermissionScope.php`.

### 3.3 Chặn lúc kiểm quyền — cả hrm-api và ERP (điểm quan trọng nhất)

Mọi đường đọc phạm vi đều đi qua `PermissionChecker` (đã soát 01/11: `DataScope::121`, `CurrentPermission::83`,
ERP `Employee::1662` đều gọi `$checker->scope()`). Nên chặn **một chỗ**:

1. `PermissionChecker::loadGrants()` (2 repo): sau khi lấy `MAX(rhp.scope)`, nếu `!GroupScopeConfig::allows($this->companyId)`
   thì phạm vi `4 → 3`. Đủ cho `grants()`, `scope()`, `allows()`, `hasLegacy()` (alias có `min_scope = 4` sẽ trượt — đúng ý).
2. `PermissionChecker::holdersQuery()` (2 repo): khi `$min >= 4` thì loại vai trò thuộc công ty bị tắt
   (`join companies` + `allow_group_scope = 1`). Không có ⇒ danh sách người duyệt/nhận thông báo cấp Tổng công ty vẫn kéo
   người ở công ty bị tắt.
3. `EmployeeRoleService` (dòng ~306, chi tiết vai trò nhân viên — bảng tổng hợp quyền đang có) đọc thẳng `rhp.scope`
   ⇒ hiển thị phạm vi **hiệu lực** (đã hạ), kèm ghi chú "đang tính như Công ty" ở dòng bị hạ.

Phạm vi Công ty trong `DataScope` = lọc theo công ty của ngữ cảnh ⇒ người ở công ty bị tắt chỉ thấy công ty mình.

### 3.4 Màn sửa quyền của vai trò (`/admin/roles/:id/permissions`)

- API `permissionsData($role)` trả thêm `role.allow_group_scope`.
- FE `PermissionTree.vue` `scopeOptions()`: bỏ lựa chọn "Tổng công ty" khi `!allow_group_scope`, **trừ** dòng đang giữ
  phạm vi 4 (C5): dòng đó vẫn hiện "Tổng công ty", nhãn phụ màu cảnh báo *"đang tính như Công ty"*, hạ xuống được,
  không nâng lại được.
- BE `updatePermissions()`: công ty bị tắt mà phạm vi 4 là **mới** hoặc **đổi từ phạm vi khác lên** ⇒ 422, báo theo
  từng mã (báo đồng thời mọi dòng sai, memory `validate-form-bao-dong-thoi`). Không đổi ⇒ cho qua.
- Sao chép quyền khi tạo vai trò (`RoleManagementService::create`, dòng ~182): công ty đích bị tắt ⇒ hạ 4 → 3 (C6),
  ghi rõ trong lịch sử vai trò.
- Banner trên màn khi công ty bị tắt: *"Công ty này chưa được cấp phạm vi Tổng công ty. Các quyền đang để Tổng công ty
  được tính như Công ty."*

### 3.5 Màn cấu hình (hrm-client, phân hệ Quản trị)

- URL `/admin/group-scope-companies`, tên "Cấu hình phạm vi Tổng công ty". Layout đúng phân hệ Quản trị.
- Bảng: Mã công ty · Tên công ty · **Phạm vi Tổng công ty** (badge Được cấp / Không được cấp) · Số vai trò đang giữ phạm vi Tổng công ty
  · Người cập nhật · Cập nhật lúc. Sắp: cập nhật mới nhất lên đầu (cùng quy ước 3 màn phân quyền 01/11).
- **[Claude chốt 01/11 khi code]** Bật/tắt bằng hành động dòng "Cho phép cấp" / "Không cho cấp" (khuôn Khoá/Mở khoá màn Vai trò) — hệ thống chưa có component công tắc dùng chung, không tự chế.
- Không cho cấp ⇒ hộp xác nhận nêu số vai trò + số người bị thu hẹp ở công ty đó (đếm từ `role_has_permissions` +
  `employee_has_roles`), bấm xác nhận mới lưu. Tắt đúng công ty đang làm ⇒ thêm dòng cảnh báo (Q3).
- Menu: mục chỉ hiện khi API trả `can_manage_group_scope = true` (thêm vào payload `/auth/me` hoặc API riêng —
  builder chọn). Đây **không phải** mã quyền: không có trong Catalog, không gán được qua vai trò.
- API: `GET /api/v1/admin/group-scope-companies`, `PUT /api/v1/admin/group-scope-companies/{companyId}`
  `{allow_group_scope: 0|1}`. Cả 2 kiểm `GroupScopeConfig::canManage(auth id)`, sai ⇒ 403. Không theo công ty đang làm
  (người trong danh sách thấy mọi công ty).
- Lịch sử: ghi vào bảng chung `catalog_histories` (`table_name = company_group_scope`, `table_id` = công ty — không thêm bảng/migration), đọc qua adapter `GroupScopeCompanyAdapter` của khung `SettingHistory` (type `group_scope_company`).
- Đổi xong gọi `PermissionChecker::flush()`. Phía ERP: checker nhớ trong request nên request sau tự đọc giá trị mới;
  nếu ERP có cache ngoài request (redis) cho quyền thì builder phải xoá đúng khoá, KHÔNG `cache:clear` (redis chung).

## 4. Test bắt buộc (memory `always-test-permission-cases`)

| Ca | Kỳ vọng |
|---|---|
| Vai trò công ty bị tắt giữ phạm vi 4 | `scope()` = 3; danh sách dữ liệu chỉ công ty mình (hrm-api + ERP) |
| Bật lại | `scope()` = 4 ngay request sau, dữ liệu không đổi |
| `holders(..., minScope 4)` | không có người ở công ty bị tắt |
| Lưu màn quyền: cấp mới 4 ở công ty bị tắt | 422 báo đúng mã |
| Lưu màn quyền: giữ nguyên dòng 4 cũ | 200, dòng còn nguyên 4 |
| Sao chép quyền sang công ty bị tắt | dòng 4 thành 3 |
| API cấu hình: tài khoản ngoài danh sách | 403 cả GET/PUT; menu không hiện |
| Danh sách `.env` rỗng | 403 với mọi tài khoản |
| Tài khoản có "Quản lý phân quyền" nhưng ngoài danh sách | 403 (chống tự cấp) |

Playwright (CLAUDE.md): màn quyền vai trò công ty bị tắt — đếm lựa chọn trong ô phạm vi (không có "Tổng công ty"),
dòng 4 cũ có nhãn cảnh báo, banner hiện; màn cấu hình — công tắc, hộp xác nhận hiện đúng số; tài khoản ngoài danh sách
không thấy menu + vào URL ra 403/404.

## 5. Phạm vi code (để hỏi xin phép khi làm)

| Repo | File / bảng |
|---|---|
| hrm-api | migration `add_allow_group_scope_to_companies`; `config/rbac.php`; `GroupScopeConfig` mới; `PermissionChecker` (loadGrants, holdersQuery); `RoleManagementService` (permissionsData, updatePermissions, create); `EmployeeRoleService` (tổng hợp quyền); controller + route + adapter lịch sử mới; test `tests/Feature/Rbac/GroupScope*Test.php` |
| ERP TanPhatDev | `GroupScopeConfig` (bản giống hệt); `PermissionChecker` (loadGrants, holdersQuery); test `tests/Feature/Rbac` |
| hrm-client | `pages/admin/group-scope-companies/index.vue` mới; `PermissionTree.vue` + `pages/admin/roles/_id/permissions.vue`; menu Quản trị |
| DB | chạy 1 migration trên — phải liệt kê + hỏi trước khi chạy vào bất kỳ DB nào |

Runbook go-live (`../gd1-nen-du-lieu/runbook-go-live.md`): thêm bước đặt `RBAC_GROUP_SCOPE_ADMINS` vào `.env` HRM prod
**trước** khi mở màn; chạy migration này cùng loạt migration `rbac` (trước hay sau `rbac:convert` đều được — không đụng
`role_has_permissions`).

## 6. Câu hỏi tồn — đã chốt hết 01/11

- ~~**Q1.**~~ ~~Đã chốt 01/11: (a) — go-live mọi công ty = 1~~ **ĐỔI 01/11 tối:** go-live chỉ TPE (id 1) giữ = 1, **6 công ty còn lại tắt = 0** ngay trong cửa sổ go-live (phạm vi Tổng công ty của họ tính như Công ty; dữ liệu giữ nguyên, cấp lại sau bằng màn cấu hình). User chốt: "gỡ" = hạ xuống Công ty (không bỏ quyền), làm bằng cấu hình GĐ2c (không sửa dữ liệu `role_has_permissions`).
- ~~**Q2.**~~ **Đã chốt 01/11:** danh sách ban đầu chỉ `13` (namdangit@gmail.com) ⇒ `.env` prod: `RBAC_GROUP_SCOPE_ADMINS=13`.
  Đổi người = sửa `.env` + `config:cache`, không deploy.
- ~~**Q3.**~~ **Đã chốt 01/11: cho phép** tắt cả công ty mình đang làm. Hộp xác nhận thêm dòng: *"Bạn đang làm việc ở
  công ty này, quyền Tổng công ty của chính bạn cũng sẽ tính như Công ty."* Không tự khoá được vì quyền vào màn lấy từ `.env`.

**Hết câu hỏi tồn — sẵn sàng lên `plan.md`.**
