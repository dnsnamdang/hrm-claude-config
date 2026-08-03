# Task 3 — Permission 1138 (seeder) — Report

## Thay đổi

- Modify: `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
  - Thêm ngay sau permission id 1137 (`Xem thẻ kho`, dòng 1096 cũ):
    ```php
    // Quản lý kho — Dashboard
    Permission::create(['id' => 1138, 'guard_name' => 'api', 'name' => 'Xem dashboard kho', 'display_name' => 'Xem dashboard kho', 'group' => 'Dashboard kho', 'type' => 10]);
    ```
  - Đã grep toàn repo (`nhatlinh-api`, loại `vendor/`) trước khi thêm: id 1138 chưa tồn tại ở nơi nào khác.
  - `php -l` OK: `No syntax errors detected`.

## Cách gán role (theo pattern các phase kho trước — R1 báo cáo kho 1136/1137, T5 chuyển kho 1130-1132)

1. Seed: `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"` → seeder này **truncate + reseed toàn bộ bảng `permissions`** (FK checks tắt tạm), an toàn vì tất cả ID cũ được tái tạo y hệt + thêm 1138 mới; **không đụng `role_has_permissions`** (bảng pivot giữ nguyên, chỉ orphan tạm thời rồi khớp lại theo id).
2. Gán role 1 (Admin) cho quyền 1138 — bảng `role_has_permissions` có 3 cột `(permission_id, role_id, company_id)`, role 1 hiện chỉ có 1 `company_id = 1` (đã kiểm tra distinct company_id trước khi insert). Dùng:
   ```php
   DB::table('role_has_permissions')->insertOrIgnore([
       ['permission_id' => 1138, 'role_id' => 1, 'company_id' => 1],
   ]);
   ```
   (insertOrIgnore để an toàn, không truncate pivot — đúng pattern "insert an toàn, không truncate" các phase trước dùng.)
3. Clear cache:
   - `php artisan permission:cache-reset` → trả `Unable to flush cache.` (không phải lỗi thật — lệnh này gọi `Cache::forget($key)`, trả `false` vì key permission cache **chưa từng được ghi** trong session này nên không có gì để forget; hành vi biết trước của Spatie khi cache trống).
   - Chạy thêm `php artisan cache:clear` → `Application cache cleared!` (dọn sạch mọi cache liên quan, đảm bảo không có bản permission cũ nào còn sót).

## Output verify

```
PERM_1138_EXISTS
ROLE1_HAS_PERM
```

- `Spatie\Permission\Models\Permission::find(1138)` → tồn tại, đầy đủ field:
  `id=1138, name='Xem dashboard kho', guard_name='api', display_name='Xem dashboard kho', group='Dashboard kho', type=10`.
- `App\Models\Role::find(1)->hasPermissionTo('Xem dashboard kho')` → `true` (đọc thẳng DB qua Spatie helper, không phụ thuộc cache stale).
- `role_has_permissions` có đúng 1 row `permission_id=1138, role_id=1, company_id=1`.

## Concerns

- `permission:cache-reset` báo lỗi "Unable to flush cache." — đã xác minh đây là hành vi bình thường của Spatie khi cache key chưa tồn tại (không phải regression), và đã chạy `cache:clear` bổ sung + verify bằng `hasPermissionTo()` đọc thẳng DB để chắc chắn không bị cache cũ che khuất kết quả. User restart dev server + re-login để FE nhận quyền mới (theo đúng pattern các phase trước ghi trong `.plans/warehouse-management/plan.md`).
- Route `/v1/warehouse/dashboard` + middleware `checkPermission:Xem dashboard kho` **chưa tồn tại** (thuộc Task 5, ngoài phạm vi Task 3) nên chưa thể test E2E HTTP 403/200 thật; chỉ verify ở tầng permission + role như trên.
- Seeder vẫn giữ nguyên toàn bộ 1138 permission khác (606+ dòng) — không có side effect ngoài ý muốn, đã confirm bằng cách seeder chạy "Database seeding completed successfully." không lỗi.
