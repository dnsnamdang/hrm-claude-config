# Fix lỗi "Column 'company_id' in where clause is ambiguous" khi vào ERP

## Nguyên nhân
Gộp DB thêm cột `company_id` vào bảng SHARE `roles` (từ HRM). Các query ERP chain
`->where('company_id', ...)` trên quan hệ `roles()`/`permissions()` render thành
`company_id = X` trần → sau gộp bị mơ hồ giữa `roles.company_id` và
`employee_has_roles.company_id` (hoặc `role_has_permissions.company_id`).
Trước gộp không lỗi vì `roles`/`permissions` chưa có cột `company_id`.

Fix: chỉ rõ prefix bảng pivot (khôi phục đúng hành vi trước gộp, KHÔNG đổi logic).

## Tasks
- [x] Employee.php:1193 — `roles()->where('company_id'` → `employee_has_roles.company_id`
- [x] Employee.php:1346-1347 — `roles()->where('company_id'` → `employee_has_roles.company_id` (chỗ chạy khi vào ERP)
- [x] RolesController.php:77 — `permissions()->where('company_id'` → `role_has_permissions.company_id`
- [x] RolesController.php:260 — `permissions()->where('company_id'` → `role_has_permissions.company_id`
- [x] Permission.php:28 — `Permission->roles()->where('company_id'` → `role_has_permissions.company_id` (chỗ lỗi lần 2: spatie getPermissions → hasPermissionTo → approveList)
- [x] Xác nhận: chỉ bảng `roles` có `company_id` (gộp thêm), `permissions` KHÔNG → chỉ query JOIN `roles` mới ambiguous; đã cover hết
- [ ] User verify: vào ERP / màn approveList không còn lỗi 1052
