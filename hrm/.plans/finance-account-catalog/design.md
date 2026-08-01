# Chuyển "Danh mục tài khoản" + "Danh mục loại tài khoản" từ ERP sang HRM (phân hệ Tài chính)

> Owner: @junfoke — Bắt đầu 2026-07-30
> Spec chi tiết: `docs/superpowers/specs/2026-07-30-finance-account-catalog-design.md`

## Mục tiêu

Dịch chuyển 2 màn danh mục kế toán từ ERP (Laravel Blade + AngularJS + DATATABLE) sang HRM
(Laravel API `Modules/Finance` + Nuxt2 `pages/finance`), đặt trong phân hệ **Tài chính**
(`finance`, nhóm `4. KINH DOANH - TÀI CHÍNH`) dưới menu **Danh mục**.

Đây là feature mở màn cho phân hệ Tài chính — hiện `Modules/Finance` và
`components/subsystem-menu/finance.js` đều chưa có gì.

## Hiện trạng ERP

| Màn | Route ERP | Controller | Đặc điểm |
|---|---|---|---|
| Danh mục tài khoản | `admin/accounting/account` | `Accounting\AccountController` (327 dòng) | List + **màn create/edit riêng**, lock/unlock/delete, history, In (template DB **459**), Export, Import |
| Danh mục loại tài khoản | `admin/accounting/type_accounts` | `Accounting\TypeAccountsController` (262 dòng) | List + **modal CRUD tại chỗ**, delete, history, Export, Import |

Cả 2 màn **không gate quyền nào** bên ERP (menu `topmenubar.blade.php` không `@can`,
route không middleware).

## DB gộp `gop_db` — nền tảng của cách làm

Trong DB gộp, bảng **trùng tên ưu tiên ERP**, bảng HRM đổi tên `hrm_*` (24 bảng).
`hrm-api` đã bám đúng quy ước này (`app/Models/Employee.php` → `hrm_employees`).

| Bảng | Rows | Ghi chú |
|---|---|---|
| `accounts` | 308 | **KHÔNG có `company_id`, KHÔNG có `note`** |
| `type_accounts` | 7 | code / name / note / status |
| `account_versions` / `account_histories` | 0 / 0 | |
| `type_account_versions` / `type_account_histories` | 0 / 0 | |
| `account_details` | 965.017 | dùng cho `canDelete()` của tài khoản |
| `employees` | 1.085 | **của ERP** (HRM là `hrm_employees`) |
| `permissions` | 965 | **của ERP** (HRM là `hrm_permissions`) |

→ `accounts` + `type_accounts` nằm ngay trên **connection `mysql` (default)** → dùng
Entity Eloquent thuần, **KHÔNG cần** `mysql2` / model `TpXxx` như màn Khách hàng đã port.

## Quyết định đã chốt (user 2026-07-30)

1. **Phân quyền: tạo quyền HRM mới** (không dùng `erpPermission` vì ERP không có quyền tương ứng).
   Thêm vào `hrm_permissions` 4 quyền, dùng `middleware('checkPermission:...')` như `customer-scopes`:
   - `Quản lý danh mục tài khoản` / `Xem danh mục tài khoản`
   - `Quản lý danh mục loại tài khoản` / `Xem danh mục loại tài khoản`
2. **`created_by` / `updated_by` ghi `employees.id` (ERP)** — map từ HRM user qua
   `ErpPermissionHelper::erpEmployeeId()` (cầu nối `employee_info_id`, bảng `employee_infos`
   dùng chung không prefix). Giữ tương thích 2 chiều: ERP vẫn hiện đúng tên người tạo và
   `canLock/canDelete` (điều kiện `created_by == user hiện tại`) vẫn chạy.
3. **Port trọn bộ**: CRUD + khóa/mở + Lịch sử (version/history) + Xuất Excel + Import Excel
   + In danh sách (template 459). Không để phase sau.
4. **"Loại tài khoản" giữ nguyên như ERP**: hằng `Account::TYPES` (7 loại hardcode) dùng cho
   bộ lọc + ghi lịch sử; dropdown ở form đọc bảng `type_accounts`. (Tôi đã nêu rủi ro sai khi
   phát sinh loại thứ 8 — user quyết giữ nguyên để đồng nhất 2 cổng.)
5. **KHÔNG phân quyền theo cấp** (tổng công ty / công ty / phòng ban / bộ phận). Cả 2 bảng đều
   không có `company_id` / `department_id` / `part_id` và đã chốt không đổi schema → danh mục
   toàn hệ thống, ai có quyền thì thấy hết, giống ERP.
6. **`is_can_delete` giữ nguyên điều kiện ERP**:
   - Tài khoản: `created_by == user hiện tại` **và** không có tài khoản con
     (`identify_number_parent = identify_number`) **và** chưa dùng trong `account_details`.
   - Loại tài khoản: không tồn tại `accounts.type = id`.
   - `canLock` / `canUnlock` cũng giữ điều kiện `created_by == user hiện tại` + đúng `status`.

## Phạm vi

- **Phase 1 — BE `Modules/Finance`**: Entity + Service + Controller + Request + Resource +
  Route cho `type-accounts` rồi `accounts`; ExcelExport + Import; endpoint In.
- **Phase 2 — Quyền**: seeder/migration 4 quyền HRM + gắn middleware.
- **Phase 3 — FE menu**: `components/subsystem-menu/finance.js` + trỏ lại trong `subsystems.js`.
- **Phase 4 — FE màn Loại tài khoản**: list + modal CRUD + lịch sử + Excel.
- **Phase 5 — FE màn Tài khoản**: list + màn add/edit riêng + lịch sử + Excel + In.

Thứ tự: `type-accounts` **trước** (nhỏ, 4 field, dựng sẵn service/menu/helper), `accounts` sau
(phụ thuộc dropdown loại tài khoản).

**Style FE — chốt 2026-07-30:** toàn bộ dùng bộ **V2Base**, dựng giao diện mới theo chuẩn HRM,
**KHÔNG** port markup/DATATABLE/AngularJS của ERP (chỉ port nghiệp vụ). Select **trong modal**
bắt buộc `V2BaseSelectInModal` thay `V2BaseSelect`. Skill phải đọc trước khi code FE:
`list-page`, `modal-popup`, `button-convention`, `entity-history`, `import-excel`, `print-page`.
Bảng component đầy đủ ở spec §4.6.

## Ngoài phạm vi

- **KHÔNG đổi schema** `accounts` / `type_accounts` — là master data dùng chung, được **97 file**
  ERP tham chiếu `Account::` và **9 file** tham chiếu `TypeAccount`.
- **KHÔNG tắt/xóa 2 màn ERP** — chạy song song đến khi HRM ổn.
- Không thêm `company_id` (danh mục toàn hệ thống, không phân theo công ty).

## ⚠️ GOTCHA phát hiện trong code ERP (không port nguyên trạng)

1. **`form.note` ở màn tài khoản ERP là field chết** — `accounts` không có cột `note`, cũng
   không nằm trong `$fillable`. Nhập vào là mất. → HRM **bỏ field này**.
2. **`Account::canEdit()` luôn `return true`** — thực chất không có kiểm soát sửa.
3. `AccountController::update` còn **`dd($e)` trong `catch`** ([dòng 161](../../TanPhatDev/app/Http/Controllers/Accounting/AccountController.php#L161)) → không port.
4. `accounts.type` **gần như trống**: 308 dòng chỉ có `NULL` hoặc `1`.
5. Bộ lọc `name` ERP dùng `like "%$name"` (thiếu `%` cuối) → chỉ khớp hậu tố. → HRM sửa thành `%name%`.
6. **Drift quyền ERP**: `ErpPermissionHelper` đọc qua `mysql2` → `DB_DATABASE_SECOND=erp_dev_24_09`,
   **không phải `gop_db`**. Cả 2 DB còn tồn tại local nên chạy được nhưng đọc từ DB cũ.
   Feature này chỉ dùng helper để **lấy `erpEmployeeId()`** (quyền dùng `checkPermission` HRM),
   nên ảnh hưởng giới hạn ở việc map employee — vẫn cần theo dõi.

## Tham chiếu code mẫu

- BE: `Modules/Assign/Http/Controllers/Api/V1/CustomerScopeGroupController.php` + Service + Resource + Request.
- FE: `pages/assign/customer-scope-groups/index.vue` (V2BaseFilterPanel + V2BaseDataTable) + `AddGroupModal.vue`.
- Map HRM user → ERP employee: `Modules/Assign/Services/CustomerService.php` (dùng `ErpPermissionHelper::erpEmployeeId()`).
