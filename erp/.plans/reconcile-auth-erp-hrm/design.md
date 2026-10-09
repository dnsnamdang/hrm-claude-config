# Gộp Auth (roles/permissions + 3 pivot) ERP+HRM

> Thuộc dự án Gộp DB ERP+HRM. Nhánh `gop_db`. Ngày: 2026-07-31.
> **Mục tiêu:** hợp nhất hệ phân quyền 2 app về 1 bảng (giữ id HRM), bỏ `hrm_*`. Đây là nhóm TÁCH "tiên quyết" — sau khi xong mở khóa cho các bước gộp còn lại.

## 1. Scope

Gộp 6 bảng TÁCH của hệ auth về tên gốc, drop `hrm_*`:
- `roles`, `permissions`, `role_has_permissions`
- 3 pivot: `company_roles`, `employee_has_roles`, `employee_has_permissions`

## 2. Phát hiện nền (DB `erp_hrm_check`, 2026-07-31)

| Bảng | ERP (guard) | HRM (guard) | Trùng name+guard | id đụng | HRM-only cột / ERP-only cột |
|---|---|---|---|---|---|
| roles | 75 (`web`) | 44 (`api`) | **0** | 24 | HRM+: company_id,department_id,part_id / ERP+: position,created_by,updated_by,display_name |
| permissions | 965 (`web`) | 588 (`api`) | **0** | 478 | HRM+: type,sort_order / ERP+: group_category |
| role_has_permissions | 8254 | 6183 | — | (không id) | giống hệt (permission_id,role_id,company_id) |
| company_roles | 160 | 60 | — | có (leaf id) | giống hệt (id,company_id,role_id,ts) |
| employee_has_roles | 1252 | 424 | — | (không id) | ERP+: position (role_id,model_type,employee_id,company_id) |
| employee_has_permissions | 0 | 0 | — | — | giống hệt (rỗng) |

**Mấu chốt:**
- ERP `guard=web`, HRM `guard=api` → **2 namespace RỜI NHAU**, 0 role/permission "cùng là một" → **UNION, KHÔNG merge/dedup ngữ nghĩa**.
- `model_type` khác: ERP `App\Employee`, HRM `Modules\Timesheet\Entities\Employee` → **giữ nguyên cả 2** (spatie mỗi app query theo model_type+guard riêng).
- `employee_id` trong pivot HRM đã reconcile remap (0 mồ côi).
- Code runtime **KHÔNG hardcode id** (0 chỗ), chỉ SEEDER định nghĩa id tường minh (HRM 706 dòng). → Đổi id không phá runtime; chỉ ảnh hưởng re-run seeder.

## 3. Quyết định chốt (brainstorm 2026-07-31)

| # | Quyết định |
|---|---|
| Hướng | UNION theo guard (web+api cùng 1 bảng), KHÔNG dedup |
| id-space | **Base = HRM (api) GIỮ id**; **remap ERP (web)** ra ngoài dải HRM |
| Vì sao base=HRM | HRM là hệ auth chính (SSO/JWT) đi tiếp; seeder HRM 706 id tường minh phải giữ để re-runnable; ERP thoái nên remap ERP rủi ro thấp (ngoại lệ có chủ đích so với base=ERP) |
| Remap ERP | **OFFSET cố định** (vd 100000): erp_new_id = erp_old_id + OFFSET → deterministic, re-runnable |
| Tên bảng đích | tên gốc (`roles`,`permissions`,`role_has_permissions`,`company_roles`,`employee_has_roles`,`employee_has_permissions`); drop `hrm_*` |
| model_type | giữ cả 2 namespace |
| Seeder HRM | chuyển `truncate`→ `updateOrCreate/firstOrCreate` theo (name,guard=api) — KHÔNG xóa permission web ERP |
| Script | **bespoke `reconcile_auth.php`** re-runnable (như reconcile_employees), nối pipeline sau `merge_share_tables.php` |

## 4. (A) DATA reconcile — `reconcile_auth.php`

**Vị trí:** `ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php`. Chạy qua tinker (hrm-api). `$DB`, `$DRY_RUN`, `$OFFSET=100000`.

**Guard idempotent:** nếu `hrm_roles` không tồn tại → SKIP toàn bộ.

**Thuật toán:**
1. **ALTER** thêm cột HRM-only vào bảng gốc (tự diff): `roles(company_id,department_id,part_id)`, `permissions(type,sort_order)` — nullable.
2. **Remap id ERP tại chỗ (OFFSET):**
   - `UPDATE roles SET id=id+OFFSET` (chỉ dòng guard=web / id<OFFSET) ; tương tự `permissions`.
   - `UPDATE role_has_permissions SET role_id=role_id+OFFSET, permission_id=permission_id+OFFSET` cho dòng ERP (role_id/permission_id < OFFSET & thuộc web) — xem lưu ý dưới.
   - `UPDATE company_roles SET role_id=role_id+OFFSET` (ERP); `UPDATE employee_has_roles SET role_id=role_id+OFFSET WHERE model_type='App\\Employee'`; `employee_has_permissions` (rỗng).
   - *Lưu ý phân biệt ERP vs HRM trong pivot ERP-side:* các bảng pivot **gốc** (role_has_permissions, company_roles, employee_has_roles) hiện chỉ chứa dữ liệu ERP (web) — HRM ở bảng `hrm_*`. Nên UPDATE +OFFSET áp cho TOÀN BỘ bảng gốc là đúng (đều là ERP). Guard `id<OFFSET` để idempotent nếu chạy lại dở.
3. **Union HRM vào bảng gốc (giữ id HRM):**
   - `INSERT INTO roles (<cols chung+HRM-only>) SELECT ... FROM hrm_roles` (giữ id); tương tự `permissions`.
   - `INSERT INTO role_has_permissions SELECT permission_id,role_id,company_id FROM hrm_role_has_permissions` (id HRM giữ nguyên → khớp).
   - `INSERT INTO employee_has_roles (role_id,model_type,employee_id,company_id) SELECT ... FROM hrm_employee_has_roles` (position để null).
   - `INSERT INTO company_roles (company_id,role_id,created_at,updated_at) SELECT ... FROM hrm_company_roles` (id auto mới — leaf, disjoint theo role).
   - `employee_has_permissions`: rỗng → bỏ qua.
4. **DROP** 6 bảng `hrm_*`.
5. Bọc `SET FOREIGN_KEY_CHECKS=0/1`; `$DRY_RUN` in dự kiến; precheck FK trỏ roles/permissions.id (cảnh báo).

## 5. (B) CODE revert HRM (commit gop_db)

- **Spatie config** `config/permission.php`: `table_names` (roles/permissions/role_has_permissions/model_has_roles=employee_has_roles/model_has_permissions=employee_has_permissions) đang trỏ `hrm_*` → đổi về tên gốc. Giữ `guard` mặc định `api`.
- **Model** Role/Permission (nếu khai `$table='hrm_*'`) + các query đọc `hrm_roles/hrm_permissions/hrm_role_has_permissions/hrm_employee_has_roles/hrm_company_roles/hrm_employee_has_permissions` → tên gốc. (Enumerate chính xác khi lập plan; bỏ dòng `mysql2`.)
- HRM spatie vẫn lọc `guard=api` → chỉ thấy role/permission HRM. ERP lọc `guard=web`.

## 6. Seeder HRM

`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (+ RolesTableSeeder nếu có):
- Bỏ `truncate('hrm_permissions')`; chuyển từng `Permission::create([...])` → `Permission::updateOrCreate(['name'=>..,'guard_name'=>'api'], [...])` (giữ id tường minh trong phần attributes để id ổn định trên DB gộp).
- → Re-seed chỉ đụng permission `api`, không xóa permission `web` của ERP.

## 7. Verify

- **DATA:** `roles`/`permissions` = union (ERP web id≥OFFSET + HRM api id gốc); 0 name+guard trùng; pivot không mồ côi (`role_id`/`permission_id` trỏ đúng, `employee_id` trỏ employees); `hrm_*` drop; re-run → SKIP (idempotent).
- **CODE:** HRM login + phân quyền (spatie guard api) hoạt động: user HRM có đúng role/permission như trước gộp; màn Phân quyền hiển thị đúng. ERP (nếu chạy) auth web vẫn OK.
- **Seeder:** chạy PermissionsTableSeeder trên DB gộp → không xóa permission web, permission api đúng.

## 8. Edge cases / rủi ro

- **OFFSET đủ lớn:** max ERP id (roles 123, permissions 1037) + OFFSET không đụng dải HRM (max 1106). OFFSET=100000 an toàn.
- **company_roles.id** collision → INSERT HRM với id auto mới (leaf, không bị FK).
- **Spatie cache:** sau đổi bảng/ id, chạy `php artisan permission:cache-reset`.
- **model_has_roles vs employee_has_roles:** spatie config custom table + `model_morph_key=employee_id` — giữ đúng khi revert config.

## 9. Re-run / pipeline

```
merge_prod.php → reconcile_employees.php → merge_share_tables.php → reconcile_auth.php
```
Chạy lại trên bản gộp mới: đổi `$DB`, DRY-RUN trước, OFFSET cố định đảm bảo deterministic.
