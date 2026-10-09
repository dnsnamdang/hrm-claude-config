# Gộp SHARE tables — Engine tổng quát + batch 1 (2 pivot tổ chức)

> Thuộc dự án Gộp DB ERP+HRM. Nhánh `gop_db`. Ngày: 2026-07-31.
> **Mục tiêu chung:** promote các bảng TÁCH `hrm_*` (đã có employees unify) về SHARE 1 bảng, bằng 1 **engine re-runnable** dùng lại cho mọi bảng SHARE sau.

## 1. Scope

- **Batch 1 (task này):** gộp 2 pivot tổ chức từ TÁCH → SHARE:
  - `company_employees` (ERP) ⟵ union ⟵ `hrm_company_employees`
  - `employee_manage_departments` (ERP) ⟵ union ⟵ `hrm_employee_manage_departments`
- **Ngoài scope:** 3 pivot auth (`company_roles`, `employee_has_roles`, `employee_has_permissions`) — trỏ `role_id`/`permission_id` sang `roles`/`permissions` VẪN đang tách → để **task gộp Auth** riêng (làm cùng lúc gộp roles/permissions).

## 2. Hiện trạng (DB `erp_hrm_check`, bản gộp local — 2026-07-31)

| Pivot | ERP rows/cols | hrm_ rows/cols | Trùng key | Chỉ-ERP | Chỉ-HRM | id đụng |
|---|---|---|---|---|---|---|
| company_employees | 1008 · id,company_id,employee_id,ts | 1104 · +`type`,`all_department` | 958 | 68 | 146 | 1000 |
| employee_manage_departments | 126 · id,employee_id,department_id,company_id,ts | 235 · +`part_ids` | 52 | 74 | 183 | 15 |

- `employee_id` trong cả 2 pivot **ĐÃ được `reconcile_employees.php` remap** sang `employees` chuẩn (base ERP id). Task này KHÔNG remap lại employee_id.
- HRM structure là **superset** ERP (thêm cột HRM-only). id 2 hệ **đụng nhau** → không bê id hrm_ vào base.
- Pivot là **leaf** (id không bị bảng khác FK) → cấp id mới cho dòng chỉ-HRM an toàn (có bước verify).

## 3. Quyết định đã chốt (brainstorm 2026-07-31)

| # | Quyết định |
|---|---|
| Kiến trúc | 2 phần tách bạch: **(A) DATA merge = engine re-runnable**, **(B) CODE revert HRM = commit 1 lần** |
| Engine | **Tổng quát, config-driven** (`$TABLES` = mảng `{base, hrm, key[]}`); batch sau chỉ thêm config |
| Cấu trúc đích | Giữ bảng ERP tên gốc + ALTER thêm cột HRM-only (nullable), tự phát hiện bằng diff SHOW COLUMNS |
| Data | **UNION + dedup theo key tự nhiên**; cặp trùng → **HRM thắng cột HRM-only** |
| Dòng chỉ-HRM | INSERT vào base với **id mới** (không bê id hrm_) |
| Idempotent | `hrm_*` không tồn tại → skip; có `$DRY_RUN` |
| Pipeline | `merge_prod.php` → `reconcile_employees.php` → **`merge_share_tables.php`** |

## 4. (A) DATA merge engine — `merge_share_tables.php`

**Vị trí:** `ERP/.plans/merge-share-tables/merge_share_tables.php` (nối pipeline sau reconcile_employees.php).

**Config:**
```php
$DB = 'erp_hrm_check';   // đổi theo schema gộp trên môi trường chạy
$DRY_RUN = true;
$TABLES = [
  ['base' => 'company_employees',            'hrm' => 'hrm_company_employees',            'key' => ['company_id','employee_id']],
  ['base' => 'employee_manage_departments',  'hrm' => 'hrm_employee_manage_departments',  'key' => ['employee_id','department_id','company_id']],
];
```

**Thuật toán mỗi bảng (idempotent):**
1. **Guard:** nếu bảng `hrm` không tồn tại → skip (đã gộp lần trước).
2. **Cột HRM-only:** `$hrmOnly = SHOW COLUMNS(hrm) − SHOW COLUMNS(base)` (bỏ `id`). ALTER base ADD từng cột (copy đúng định nghĩa từ hrm, ép NULL-able).
3. **Cặp trùng key → HRM thắng cột riêng:**
   `UPDATE base b JOIN (SELECT <key>, <hrm_only...> FROM hrm GROUP BY <key> pick MAX(id)) h ON <b.key=h.key> SET b.<hrm_only> = h.<hrm_only>`
   (mỗi key lấy 1 dòng hrm — MAX(id) — tránh nhân bản.)
4. **Dòng chỉ-HRM:** `INSERT INTO base (<all cols trừ id>) SELECT <cols trừ id> FROM hrm h WHERE NOT EXISTS (SELECT 1 FROM base b WHERE <b.key=h.key>) GROUP BY <key>` → id auto-increment mới.
5. **DROP TABLE hrm.**

- Bọc `SET FOREIGN_KEY_CHECKS=0` đầu, `=1` cuối; chạy trong transaction/nhóm.
- `$DRY_RUN=true`: chỉ IN dự kiến (cột sẽ ALTER, số cặp trùng sẽ UPDATE, số dòng chỉ-HRM sẽ INSERT) — không thực thi.
- **Precheck (in cảnh báo, không tự sửa):** với mỗi `hrm.id`, quét xem có cột nào ở bảng khác tham chiếu (theo tên `*_id` ước lượng) — pivot vốn leaf nên kỳ vọng rỗng; nếu có → dừng + báo.

## 5. (B) CODE revert HRM (commit trên `gop_db`)

Đổi HRM đọc `hrm_company_employees`/`hrm_employee_manage_departments` → tên gốc. **Bỏ qua dòng `mysql2`.**
- **4 model đổi `$table`:**
  - `app/Models/CompanyEmployee.php` → `company_employees`
  - `app/Models/EmployeeManageDepartment.php` → `employee_manage_departments`
  - `Modules/Human/Entities/CompanyEmployee.php` → `company_employees`
  - `Modules/Timesheet/Entities/EmployeeManageDepartment.php` → `employee_manage_departments`
- **~8 tham chiếu chuỗi** trong query/relation: `app/Models/Employee.php`, `Modules/Human/Entities/{Employee,EmployeeInfo,Department}.php`, `Modules/Assign/Services/QuotationService.php`, `Modules/Timesheet/Services/EmployeeService.php` → đổi `hrm_company_employees`/`hrm_employee_manage_departments` → tên gốc.
- `TpEmployee.php`: **mysql2 BỊ COMMENT → dùng conn HRM default** → line 86 (`hrm_employee_manage_departments`) CÓ đổi. (Đính chính: bản design ban đầu ghi "né TpEmployee" là SAI.)
- Verify: `php -l` sạch; `grep -rn "hrm_company_employees|hrm_employee_manage_departments" | grep -v mysql2` = rỗng.

## 6. Verify

- **DATA:** sau chạy thật (DB gộp): `hrm_*` đã drop; `company_employees` không còn cặp (company_id,employee_id) lặp; đếm ≈ union dedup (958 + 68 + 146 → ~1172 sau dedup, xác nhận số thực khi chạy); không dòng mồ côi (`employee_id` LEFT JOIN employees IS NULL = 0; `company_id`/`department_id` trỏ đúng).
- **CODE:** HRM login OK; màn dùng company_employees/manage_departments (phân cấp, quản lý phòng ban của NV) chạy đúng.
- **Idempotent:** chạy script lần 2 → skip sạch (hrm_* đã drop).

## 7. Edge cases

- Cột HRM-only để **null** cho dòng chỉ-ERP → kiểm code HRM chịu null (nếu cần default cho `type`/`all_department`/`part_ids` thì set trong ALTER — xác nhận khi đọc code HRM ở bước code revert).
- Trùng key nội bộ trong 1 hệ (>1 dòng cùng key): GROUP BY + MAX(id) đảm bảo 1 dòng/key khi update & insert.
- Nếu môi trường chạy đã gộp 1 phần (script chạy dở) → guard theo sự tồn tại bảng hrm_ đảm bảo an toàn.

## 8. Re-run / hệ thống

Engine `merge_share_tables.php` là **bước kế tiếp trong pipeline gộp DB**. Chạy lại toàn bộ trên 1 bản gộp mới:
```
merge_prod.php  (tách 58 bảng)
  → reconcile_employees.php  (gộp employees + remap FK)
  → merge_share_tables.php   (gộp SHARE: batch 1 = 2 pivot; batch sau thêm config)
```
Các bảng SHARE tương lai (CRM pivots, settlement, danh mục…) — sau khi hết phụ thuộc — chỉ **thêm 1 dòng vào `$TABLES`**, không viết lại engine.
