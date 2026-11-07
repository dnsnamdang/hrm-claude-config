---
name: permission-seeder
description: Use when thêm / sửa / đổi tên / bỏ quyền (permission) ở hrm-api, hrm-client hoặc ERP TanPhatDev trên nhánh gop_db, khi gắn checkPermission hay kiểm quyền trong code, khi port màn ERP cần quyền, hoặc khi gặp UnknownPermissionCode, API 403 do thiếu quyền, tên quyền cũ luôn false. Cơ chế hiện hành là Catalog + mã quyền; seeder quyền đã gỡ từ 06/11/2026, KHÔNG khai vào PermissionsTableSeeder.
---

# Khai và kiểm quyền (Catalog + mã quyền)

Từ 06/11/2026 phân quyền mới đã lên prod. **`PermissionsTableSeeder` ở cả 2 repo đã gỡ, `permission:sync` không còn dùng.**
Tài liệu đầy đủ cho dev: `hrm-api/docs/huong-dan-phan-quyen.md`. Đọc file đó khi cần code mẫu đủ 3 repo.

## Nguyên tắc

- Quyền khai ở `hrm-api/app/Support/Permissions/Catalog/<phan_he>.php`. ERP dùng chung, không khai ở repo ERP.
- Mã dạng `phan_he.doi_tuong.hanh_dong`. Code mới kiểm theo **mã**, không theo tên tiếng Việt, không theo tên Vai trò.
- `kind`: `view` có `scopes` (1 Bộ phận, 2 Phòng ban, 3 Công ty, 4 Tổng công ty). `action`, `approve` để `scopes => []`.
- Một chức năng Xem là **một mã có phạm vi**, không tạo mã riêng cho từng mức. Mỗi bước duyệt một mã riêng.
- Quyền tính ở công ty đang làm. So phạm vi bằng `>=`.
- **Không bypass Super Admin** dưới mọi hình thức. Không `hasRole`, không kiểm role id.
- Port màn ERP: dùng lại mã ERP đã có trong Catalog và thêm `platforms` `hrm`; chỉ tạo mã mới khi chức năng chưa có mã.

## Thêm quyền

1. Thêm mục vào Catalog, cạnh quyền cùng chức năng, giữ đúng chữ `subsystem_group`, `subsystem`, `feature`:
   ```php
   [
       'code' => 'accounting.quyet_toan_thuong_nam.view',
       'name' => 'Xem quyết toán thưởng năm',
       'subsystem_group' => 'Kinh doanh - Tài chính',
       'subsystem' => 'Kế toán',
       'feature' => 'Quyết toán thưởng năm',
       'kind' => 'view',
       'scopes' => [2, 3, 4],
       'depends_on' => [],
       'platforms' => ['hrm'],
       'legacy' => [],
   ],
   ```
2. `php artisan permission:catalog-sync --dry-run` rồi chạy thật. Chạy vào DB là việc phải hỏi user như migration.
3. Mã mới **chưa ai có, kể cả Super Admin**: cấp ở `/admin/roles`.
4. Ghi vào ghi chú deploy: `~/build_tpe.sh` trên VPS HRM tự chạy `permission:catalog-sync`; chạy script **trước khi push ERP** nếu ERP dùng mã mới.

## Kiểm quyền

| Nơi | Cách dùng |
|---|---|
| Route hrm-api, ERP | `->middleware('checkPermission:ma.a.b')`, nhiều mã nối `\|` là có 1 mã là qua |
| hrm-api | `isCurrentEmployeeHasPermission($ma)`, `CurrentPermission::scope($ma)`, `PermissionLookup::holders($ma, $companyId)` |
| ERP | `Auth::user()->can($ma)`, `canInCompany($ma, $id)`, `permissionScope($ma)`, `@can($ma)` |
| hrm-client | `hasAPermission($ma)`, `permissionScope($ma)`, `hasAnyPermission([...])`, menu khai `codes: [...]` |

Không query thẳng `role_has_permissions`, `employee_has_roles` để hỏi quyền. `role_has_permissions` không còn `company_id`.

## Lọc dữ liệu danh sách theo phạm vi

Màn danh sách có quyền Xem theo cấp: **1 mã `.view` có `scopes`**, BE lọc bằng `HrmScopeContext::applyCurrent()`
(bọc `DataScope::apply`, ERP dùng bản giống hệt qua `ErpScopeContext`). KHÔNG tự viết chuỗi `if ($scope >= …)` ở từng màn.

```php
use App\Support\Permissions\HrmScopeContext;

HrmScopeContext::applyCurrent($query, 'sale.hop_dong.view', [
    'company' => 'contracts.company_id',
    'department' => 'contracts.department_id', // bảng không có cột thì bỏ dòng
    'part' => 'contracts.part_id',
    'owner' => 'contracts.created_by',
    'mode' => 'record_unit',                   // bắt buộc, xem bảng dưới
]);
```

| Phạm vi được cấp | `record_unit` (bản ghi có phòng ban / bộ phận) | `owner_members` (lọc theo người tạo, kiểu ERP) |
|---|---|---|
| 4 Tổng công ty | không lọc | không lọc |
| 3 Công ty | `company` = công ty đang làm | người tạo thuộc công ty (+ tôi) |
| 2 Phòng ban | phòng ban ∈ phòng tôi quản lý OR bộ phận ∈ bộ phận tôi quản lý OR tôi tạo | người tạo cùng phòng (+ tôi) |
| 1 Bộ phận | bộ phận ∈ bộ phận tôi quản lý OR tôi tạo | người tạo cùng bộ phận (+ tôi) |
| Có mã nhưng mã không phạm vi | chỉ bản ghi tôi tạo | như trái |
| Không có mã / chưa đăng nhập | không thấy gì (`1 = 0`) | như trái |

- Báo cáo / dashboard tổng hợp truyền `$aggregate = true`: không có phạm vi thì không thấy gì (không rơi về "tôi tạo").
- Kiểm 1 bản ghi (màn chi tiết, sửa, xoá) dùng `DataScope::allowsRecord($ma, $record, $cols, HrmScopeContext::current())` (context `null` ⇒ coi là không có quyền) — cùng bộ điều kiện với `apply()`.
- Tổng công ty bị tắt ở `/admin/group-scope-companies` thì hệ thống tự hạ về mức Công ty, đừng tự xử lý.
- Hàm cũ `checkPermissionList($query, [tên tất cả, tên công ty, tên phòng, tên bộ phận…])` chỉ để code cũ chạy qua bí danh.
  **KHÔNG truyền mã vào đó**: nó coi "có mã" là có quyền ở vị trí đó, cấp Bộ phận cũng thấy toàn bộ.
- FE: `permissionScope('<mã>')` (1..4 hoặc `null`) để quyết định hiện ô lọc Công ty / Phòng ban; dữ liệu vẫn do BE lọc.
- Mẫu test đủ mọi nhánh: `hrm-api/tests/Feature/Rbac/DataScopeTest.php`.

## Đưa DB local lên kiểu mới

Code `gop_db` từ 06/11 kiểm theo mã. DB local chưa chuyển thì **mọi** quyền đều false, kể cả Super Admin.

**Cách khuyên dùng: lấy dump prod `hrm_erp_gop`** (đã chuyển sẵn). Muốn tự chuyển DB local thì làm ĐÚNG thứ tự:

1. `php artisan migrate` — thêm cột `permissions.code`, bảng `permission_aliases`, `roles.company_id`…
2. `php -d memory_limit=2G artisan rbac:convert --dry-run` → đọc báo cáo ở `storage/app/rbac-convert/<giờ>_dry-run/`.
3. `php artisan down` → `php -d memory_limit=2G artisan rbac:convert --erp-da-bao-tri` → `php artisan up`.
4. `php artisan permission:catalog-sync`.

Chỉ migrate + `catalog-sync` là CHƯA đủ: vai trò cũ chưa gắn công ty, chưa ai có mã nào. Lỗi hay gặp khi tự chuyển:

| Lỗi | Xử lý |
|---|---|
| `permission_aliases đã có dữ liệu` | Đã lỡ chạy `catalog-sync` trước. Nếu chưa ai được gán mã: xoá `permissions` có `code` + làm rỗng `permission_aliases`, chạy lại |
| `Có N quyền cũ trong DB không thuộc danh mục…` | Tên rác chỉ có ở DB local (nhánh cũ seed vào). Grep code `gop_db`, không còn dùng thì xoá quyền đó + dòng gán. Code còn dùng thì phải khai vào Catalog |
| `Bảng bak_rbac_… đã tồn tại` | Lần chạy thật trước bị rollback. Kiểm `roles.company_id` vẫn NULL hết (dữ liệu chưa đổi) rồi DROP các `bak_rbac_*` |
| `Có N chênh lệch không giải thích được… đã rollback` | Xem `chenh-lech-khac.csv`. Toàn chiều `them` của vài tài khoản admin thì là lệch dữ liệu local; đây là chốt an toàn, KHÔNG sửa code để bỏ qua mà lấy dump prod |

## Sửa, bỏ quyền

- Đổi tên hiển thị: sửa `name`, sync.
- **Không đổi `code`** của mã đã lên prod.
- Bỏ quyền: gỡ khỏi Catalog và mọi chỗ kiểm, sync. Mã chuyển `deprecated_at`, không xoá.
- Code cũ còn gọi tên tiếng Việt: thêm `legacy` `['api'|'web', 'tên cũ', phạm_vi|null]`. Tên phải đúng từng ký tự; `api` là HRM, `web` là ERP.

## Merge nhánh cũ còn seeder

Conflict `PermissionsTableSeeder` (modify/delete): **giữ đã xoá**. Lấy các tên quyền nhánh đó thêm, khai vào Catalog. Sót tên thì `rbac:convert` hoặc chỗ kiểm quyền sẽ không nhận.

## Lỗi hay gặp

- `catalog-sync` lỗi `Unknown column 'code'`: DB local chưa migrate, xem mục "Đưa DB local lên kiểu mới".
- Local mọi quyền đều false, kể cả Super Admin: DB chưa `rbac:convert`.
- `UnknownPermissionCode` ở local: mã sai hoặc chưa sync. Prod không văng lỗi mà trả false và log kênh `permission`.
- Đã sync vẫn 403: Vai trò chưa được cấp, hoặc đang ở công ty khác.
- API 500 thiếu `permission_aliases`: DB chưa chuyển đổi.
