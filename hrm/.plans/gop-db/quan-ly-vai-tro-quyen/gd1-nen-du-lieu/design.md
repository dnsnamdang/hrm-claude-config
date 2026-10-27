# Giai đoạn 1 — Nền dữ liệu + kiểm quyền theo công ty

> Thuộc `../design.md` (đã duyệt 25/10/2026). File này chốt **cách làm** của giai đoạn 1. Đây là phần
> tài liệu tổng quan để builder tự quyết (mục 10 của design tổng). Những điểm đánh dấu **[Claude chốt]**
> là quyết định của Claude, user soát khi đọc.

## 1. Kết quả của giai đoạn

Sau giai đoạn 1:
- Mỗi quyền có **một mã**. Quyền trùng nghĩa giữa ERP và HRM đã nhập làm một. Các biến thể "Xem … theo X"
  đã gộp thành một mã kèm phạm vi.
- Mỗi vai trò thuộc **một công ty**, tên dạng `TPE_Kế toán`.
- Danh sách công ty làm việc của từng người nằm ở một chỗ.
- **Mọi đường kiểm quyền hiện có** ở ERP và hrm-api, dù vẫn gọi bằng **tên cũ**, đều đi qua một bộ kiểm
  chung và luôn lọc theo công ty đang làm việc. Tên cũ được dịch sang mã qua bảng bí danh. Code gọi quyền
  chưa phải sửa: đó là việc của giai đoạn 3.
- Có lệnh chuyển đổi chạy lại được nhiều lần trên bản sao DB, kèm báo cáo chênh lệch quyền.

Giao diện **không đổi** ở giai đoạn này. Màn phân quyền cũ của ERP và HRM sẽ hỏng sau khi chuyển đổi
(chúng ghi theo `company_id` trên dòng quyền). Chấp nhận được vì cả 4 giai đoạn lên prod cùng lúc và
giai đoạn 2 gỡ hai màn này. **[Claude chốt]**

## 2. Cấu trúc dữ liệu

Chung một DB. Migration đặt ở **hrm-api** (theo các migration vai trò gần đây, ví dụ `2026_10_22_*`).
ERP không có migration cho phần này. **[Claude chốt]**

### 2.1 `permissions` (sửa tại chỗ)
| Cột | Ghi chú |
|---|---|
| `code` | `varchar(150)`, **UNIQUE một mình** (bỏ unique `(code, guard_name)`). DB local đã có cột này từ nhánh huỷ → migration phải `hasColumn` |
| `name` | tên hiển thị tiếng Việt. **Bỏ unique `(name, guard_name)`** |
| `subsystem_group`, `subsystem`, `feature` | Nhóm phân hệ, Phân hệ, Chức năng (varchar) |
| `kind` | `view` / `action` / `approve` |
| `allowed_scopes` | JSON mảng số con của `[1,2,3,4]`. NULL = quyền không có phạm vi |
| `depends_on` | JSON mảng mã. Chỉ dùng cho giao diện (phương án C) |
| `on_erp`, `on_hrm` | tinyint, nền tảng áp dụng |
| `deprecated_at` | timestamp NULL. Quyền ngừng dùng thì không xoá |
| `guard_name` | mọi dòng = `api` (spatie còn đòi cột này, giá trị không còn ý nghĩa) |

Cột cũ `group`, `group_category`, `type`, `display_name`, `seed_order` **giữ nguyên ở giai đoạn 1**,
giai đoạn 2 mới dọn.

### 2.2 `permission_aliases` (mới)
`id, legacy_name varchar(255) COLLATE utf8mb4_bin, legacy_guard varchar(10), permission_id FK, min_scope tinyint NULL`
· UNIQUE `(legacy_name, legacy_guard)`. Dùng collation `utf8mb4_bin` vì cột `name` cũ là unicode_ci
("mục" = "mức"), xem ghi chú trong `PermissionSync.php`.

### 2.3 Phạm vi
`1 = Bộ phận · 2 = Phòng ban · 3 = Công ty · 4 = Tổng công ty`. Số lớn bao số nhỏ.

### 2.4 `roles` (sửa tại chỗ)
Thêm `company_id` (FK `companies`, NOT NULL sau chuyển đổi) và `base_name`. UNIQUE `(company_id, base_name)`.
`name` = `{companies.code}_{base_name}`, ví dụ `TPE_Kế toán`. `guard_name` = `api` cho mọi dòng.

### 2.5 `role_has_permissions` (dựng lại)
Migration thêm cột `scope` trước, chưa đổi khoá chính. Lúc `rbac:convert` chạy, bảng cũ được đổi tên thành
`bak_rbac_role_has_permissions` và dựng bảng mới:
`role_id, permission_id, scope tinyint NULL`, PK `(role_id, permission_id)`. Tên bảng giữ nguyên để
quan hệ spatie `$role->permissions` vẫn đọc được.

### 2.6 `employee_has_roles` (dựng lại)
Bảng cũ thành `bak_rbac_employee_has_roles`. Bảng mới:
`employee_id, role_id, company_id, model_type, position`, PK `(employee_id, role_id)`.
- `company_id` luôn bằng `roles.company_id`, giữ lại để các truy vấn đang lọc theo cột này không phải sửa.
- `model_type` mặc định `App\Employee` cho mọi dòng **[Claude chốt]**, để quan hệ spatie của ERP vẫn
  thấy. Bên HRM thì `Employee::roles()` được ghi đè thành `belongsToMany` không lọc morph.

### 2.7 Công ty làm việc = `company_employees` (dùng lại) **[Claude chốt]**
Bảng này ERP đang dùng làm danh sách công ty của nhân viên (`App\Employee::companies()`, 43 file đụng tới).
Không tạo bảng mới:
- Dọn trùng `(employee_id, company_id)`, thêm UNIQUE.
- Bổ sung các cặp còn thiếu theo quy tắc ở mục 8.1 của design tổng: công ty đang có vai trò ∪
  `employee_infos.company_id`. Local thiếu 14 cặp.
- Công ty chính = `employee_infos.company_id`, không thêm cột.

### 2.8 Bảng phụ của lần chuyển đổi
`rbac_role_map(old_role_id, company_id, new_role_id)` và `bak_rbac_*` (sao lưu nguyên trạng `permissions`,
`roles`, `company_roles`). `company_roles` bị bỏ: vai trò đã mang `company_id`. Bảng chỉ được giữ dạng bản sao.

## 3. Bộ kiểm quyền chung

`App\Support\Permissions\PermissionChecker`, kèm `PermissionScope` cho các hằng phạm vi.
- **Bản giống hệt ở cả 2 repo**, theo đúng cách đang làm với `PermissionSync.php`.
- Viết cho PHP 7.4 + Laravel 6 (ERP) và chạy được trên Laravel 8. Chỉ dùng facade `DB`, không dùng spatie.

Quyền hiệu lực của `(employee_id, company_id)`:
```
company_employees có (employee_id, company_id)        -- không làm việc ở công ty này ⇒ rỗng
employee_has_roles ehr JOIN roles r ON r.id = ehr.role_id AND r.company_id = :company
JOIN role_has_permissions rhp ON rhp.role_id = r.id
JOIN permissions p ON p.id = rhp.permission_id AND p.deprecated_at IS NULL
WHERE ehr.employee_id = :employee
→ mỗi mã lấy MAX(scope)
```
- **Không** lọc `roles.status`, giữ đúng hành vi hiện tại. Vai trò ngừng hoạt động mà vẫn đang cấp quyền
  thì liệt kê ra cho user. **[Claude chốt]**
- Tên cũ → mã: tra `permission_aliases (legacy_name, guard)`. Có quyền khi người đó có mã đó và
  `scope >= min_scope`, hoặc khi `min_scope` NULL.
- Đệm trong một request theo `employee|company`, có `PermissionChecker::flush()` cho test và queue.

Nơi nối vào:
- **hrm-api:** cả 4 bản `isCurrentEmployeeHasPermission` (`app/Helper/PermissionHelper.php:20`,
  `app/CommonServices/PermissionService.php:20`, `app/Models/BaseModel.php:204`, `app/Http/Controllers/ApiController.php:159`),
  middleware `CheckPermission`, `Employee::getAllPermissions()` / `getPermissionsViaRoles()` (69 chỗ gọi),
  `Employee::permissionRoles()` / `manageCompanyIds()`, và API profile `AuthNewController` (khoảng dòng 460).
  Công ty = `auth()->user()->current_company_role`.
- **ERP:** `App\Employee::can()`, `hasAnyPermission()`, `hasPermissionTo()`, `checkPermissionTo()`,
  `canInCompany()`, `getAllPermissions()`, claim JWT `permissions`. Gỡ `Gate::before`
  (`app/Providers/AuthServiceProvider.php:28`). `hasRole()` so theo `base_name`, để `hasRole('Kế toán')` vẫn
  khớp `TPE_Kế toán`. Công ty = `$this->info->company_id`.
- Bỏ qua mặc định của `hasRole()` khi có Super Admin (`app/Employee.php:1400`) **chưa gỡ ở giai đoạn 1**.
  Gỡ ở giai đoạn 3, cùng lúc đổi 224 chỗ `hasRole('Super Admin')`. **[Claude chốt]**

## 4. Danh mục quyền khai trong code

- Đặt ở **hrm-api** `app/Support/Permissions/Catalog/*.php`, mỗi phân hệ một file trả mảng.
- Chỉ hrm-api chạy đồng bộ, ERP chỉ đọc DB. **[Claude chốt]**

Mỗi phần tử:
```php
[
  'code' => 'sale.quotation.view', 'name' => 'Xem báo giá',
  'subsystem_group' => 'Kinh doanh', 'subsystem' => 'Báo giá', 'feature' => 'Báo giá dự án',
  'kind' => 'view', 'scopes' => [1, 2, 3, 4], 'depends_on' => [], 'platforms' => ['erp', 'hrm'],
  'legacy' => [['web', 'Xem báo giá bộ phận', 1], ['web', 'Xem báo giá phòng', 2], ['api', 'Xem báo giá', null]],
]
```
Luật kiểm hợp lệ:
- mã khớp `^[a-z0-9_]+(\.[a-z0-9_]+){2,}$`, không trùng;
- `kind` hợp lệ; `action` không có `scopes`;
- `scopes` là tập con của 1..4; `min_scope` của legacy phải nằm trong `scopes`;
- `depends_on` trỏ tới mã có thật;
- một cặp `(guard, tên cũ)` chỉ thuộc một mã;
- `platforms` không rỗng.

Lệnh `permission:catalog-sync {--dry-run}` (hrm-api):
- upsert theo `code`;
- đặt `deprecated_at` cho mã có trong DB mà không còn trong danh mục;
- dựng lại `permission_aliases` từ trường `legacy`;
- một transaction;
- chạy lại lần 2 không đổi gì.

`permission:sync` và hai `PermissionsTableSeeder` cũ ở cả 2 repo được gỡ. Lệnh cũ in thông báo trỏ sang
lệnh mới rồi thoát với mã lỗi.

**Bản nháp danh mục** do lệnh `rbac:draft-catalog` sinh ra từ DB hiện tại:
- nhóm biến thể phạm vi theo mẫu tên ("theo tổng công ty / công ty / phòng ban / bộ phận", "Xem tất cả / … công ty / phòng / bộ phận",
  đuôi mã HRM `.view.all_company / .company / .department / .part`, và "theo nhân viên / cá nhân / của mình", loại này sẽ bỏ);
- ghép cặp ERP/HRM cùng tên (local có 175 cặp);
- gợi ý mã.

Sau đó Claude chỉnh tay từng phân hệ. Xuất ra file Excel để user duyệt. **User duyệt xong mới chạy chuyển đổi.**

## 5. Lệnh chuyển đổi `rbac:convert {--dry-run} {--report-dir=}`

Chạy trên DB đã migrate schema. **Không chạy hai lần trên cùng DB.** Muốn chạy lại thì dùng bản sao mới
(chặn bằng dấu trong `rbac_role_map`). Các bước:

1. Sao lưu `bak_rbac_*`.
2. **Chụp mốc trước** cho mọi `(nhân viên, công ty làm việc)`:
   - (a) *đúng công ty*: vai trò của người đó gán ở công ty C, nhân với quyền của vai trò tại C, theo đúng cách
     `canInCompany` đang làm;
   - (b) *thực tế đang chạy*: tái hiện cách tính rò hiện nay của HRM (`getAllPermissions`) và ERP (`hasAnyPermission`).
   - Kết quả là các dòng `(employee, company, guard, tên cũ)`.
3. Nhập quyền theo danh mục:
   - mỗi mã giữ id của một dòng cũ (ưu tiên dòng `api`), các dòng cũ khác của cùng mã chuyển lượt gán sang id đó rồi xoá;
   - ghi `permission_aliases`;
   - các tên "… của mình" bị bỏ;
   - quyền cũ không có trong danh mục thì **dừng** và liệt kê ra.
4. Tách vai trò theo công ty, cho mỗi cặp `(role, công ty)` lấy từ `role_has_permissions ∪ employee_has_roles ∪ company_roles`:
   - cặp có nhiều lượt gán nhất **giữ id cũ**, các cặp khác tạo vai trò mới. Ghi `rbac_role_map`;
   - quyền của vai trò mới = quyền của role cũ tại công ty đó, mỗi mã lấy **phạm vi lớn nhất** trong các biến thể;
   - với quyền Xem không có biến thể "theo …": lấy phạm vi theo **file quyết định**
     `scope-decisions.csv` do user duyệt (mục 7 của design tổng). Thiếu dòng nào thì dừng và liệt kê;
   - đặt tên có tiền tố; trùng `base_name` trong một công ty thì thêm ` (2)` và liệt kê.
5. Super Admin: vai trò tên đúng `Super Admin` (local: id 100002 web, 100125 api) được gán **mọi mã**,
   phạm vi lớn nhất cho phép. **[Claude chốt]** Vai trò `Super admin (DNS DÙNG)` (id 18) **không** tính là
   Super Admin, vì ERP chỉ khớp đúng tên `Super Admin`.
6. Chuyển hướng dữ liệu đang trỏ tới role id: danh sách cột lấy từ bước dò ở Task 9. Mỗi dòng trỏ sang vai
   trò mới của đúng công ty của dòng đó.
7. Bổ sung `company_employees`.
8. **Chụp mốc sau** bằng `PermissionChecker` dịch ngược ra tên cũ, rồi so với mốc trước. Báo cáo CSV
   trong `--report-dir`:
   - `mat-do-bit-ro.csv` = (b) − (a)
   - `them-do-gop-nen-tang.csv`
   - `them-do-super-admin.csv`
   - `them-do-cap-cao-bao-cap-thap.csv`
   - `theo-quyet-dinh-pham-vi.csv`
   - **`chenh-lech-khac.csv` phải rỗng**
   - `thieu-quyen-xem.csv` (phương án C)
   - `vai-tro-ngung-van-cap-quyen.csv`
   - `trung-ten-vai-tro.csv`
   - `vai-tro-khong-chuyen.csv`
   - `du-lieu-tro-role-id.csv`

`--dry-run`: chạy hết trong transaction, ghi báo cáo, rồi rollback. Bước sao lưu là DDL nên bỏ qua khi dry-run.

## 6. Test

- Test chạy trên **DB test riêng** `hrm_erp_rbac_test`, nhân bản từ DB local và đã migrate. Không chạy trên
  DB của `.env`, vì đã từng để lại rác (memory `phpunit-chay-tren-db-env-de-lai-rac`).
- Việc tạo DB này và chạy migrate vào nó phải hỏi user trước.
- Mỗi test dùng `DatabaseTransactions` và fixture id lớn (`9999999xx`), theo kiểu `tests/Feature/PermissionSyncTest.php`.
- Mọi test về quyền có đủ 3 ca: **có quyền / không quyền / có quyền ở công ty khác**.

## 7. Nhánh

Nhánh mới `rbac` tạo từ `gop_db` ở hrm-api và ERP. Làm trong worktree riêng có `composer install` riêng,
**không symlink vendor** (memory `worktree-vendor-symlink-autoload-bug`).

Mỗi lần merge `gop_db` vào `rbac`:
- chạy lại `rbac:draft-catalog --diff`, để bắt quyền mới mà các feature khác thêm vào seeder cũ;
- soát `uniq -d` id quyền.

Tạo nhánh và worktree phải hỏi user.
