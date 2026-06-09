# Plan — Sắp xếp & đổi label quyền nhóm Báo giá

## Phase 1 — Đổi label + sắp xếp thứ tự hiển thị (chỉ giao diện cấu hình phân quyền)

### BE
- [x] Đổi `display_name` permission id 1083 từ "Xem tất cả danh sách Báo giá" → "Xem danh sách Báo giá theo tổng công ty", GIỮ NGUYÊN `name` (logic check quyền không đổi) — `PermissionsTableSeeder.php:1018` (php -l PASS)

- [x] Migration thêm cột `sort_order` (int nullable) vào bảng `permissions` — `database/migrations/2026_06_18_000000_add_sort_order_to_permissions_table.php`
- [x] Seeder set `sort_order` 1–9 cho 9 quyền nhóm "Báo giá" theo thứ tự yêu cầu; quyền/nhóm khác để null → theo id mặc định — `PermissionsTableSeeder.php`
- [x] Thêm hằng `GROUP_ORDER` (map `type` => mảng tên nhóm) vào seeder — để trống mặc định; khai báo theo từng phân hệ vì FE chia tab theo type — `PermissionsTableSeeder.php`
- [x] `PermissionService::getLists()` sắp xếp (`sortByDisplayOrder`): theo `type` trước, trong type nhóm có trong GROUP_ORDER[type] lên trước theo thứ tự khai báo (ngoài list theo id nhỏ nhất), trong nhóm theo `sort_order` (null → id) — `Services/PermissionService.php` (php -l PASS)

### FE
- [x] Bỏ hàm `sortBaoGiaPermissions` đã thêm trước đó — FE render thuần theo thứ tự API trả về — `components/setting/Permission.vue`

### Kiểm thử (AC)
- [ ] AC1: label đổi thành "Xem danh sách Báo giá theo tổng công ty"
- [ ] AC2: thứ tự 9 quyền đúng yêu cầu
- [ ] AC3: gán quyền + nghiệp vụ check quyền vẫn chạy đúng (name không đổi)

### Ghi chú
- KHÔNG đổi `id` (truncate + tạo lại, `role_has_permissions` tham chiếu `permission_id` → đổi id sẽ hỏng phân quyền đã gán).
- Logic check quyền dùng `name` ở 3 nơi: `QuotationService.php:2048`, `quotations/index.vue:554` → giữ nguyên.
- Thứ tự lưu ở cột `sort_order` trên bảng `permissions` (set khi seed). Tái sử dụng cho mọi nhóm khác: chỉ cần thêm `'sort_order' => N` vào quyền tương ứng. Tên cột `sort_order` (KHÔNG dùng `order` vì là từ khoá SQL reserved).
- Cần chạy migration + re-seed dev để cột + thứ tự + label mới có hiệu lực:
  - `php artisan migrate`
  - `php artisan db:seed --class="Modules\\Timesheet\\Database\\Seeders\\PermissionsTableSeeder"`
