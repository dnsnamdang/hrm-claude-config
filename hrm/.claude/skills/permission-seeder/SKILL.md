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

## Sửa, bỏ quyền

- Đổi tên hiển thị: sửa `name`, sync.
- **Không đổi `code`** của mã đã lên prod.
- Bỏ quyền: gỡ khỏi Catalog và mọi chỗ kiểm, sync. Mã chuyển `deprecated_at`, không xoá.
- Code cũ còn gọi tên tiếng Việt: thêm `legacy` `['api'|'web', 'tên cũ', phạm_vi|null]`. Tên phải đúng từng ký tự; `api` là HRM, `web` là ERP.

## Merge nhánh cũ còn seeder

Conflict `PermissionsTableSeeder` (modify/delete): **giữ đã xoá**. Lấy các tên quyền nhánh đó thêm, khai vào Catalog. Sót tên thì `rbac:convert` hoặc chỗ kiểm quyền sẽ không nhận.

## Lỗi hay gặp

- `UnknownPermissionCode` ở local: mã sai hoặc chưa sync. Prod không văng lỗi mà trả false và log kênh `permission`.
- Đã sync vẫn 403: Vai trò chưa được cấp, hoặc đang ở công ty khác.
- API 500 thiếu `permission_aliases`: DB chưa chuyển đổi.
