# Task 1 — Permissions seeder: thêm 5 quyền guard `api`

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db). Laravel 8, PHP 7.4, DB=erp_hrm_check.

**File modify:** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

## Bối cảnh
Phiếu YC xuất bán hàng mượn (Phase 1) cần 5 quyền guard `api`, đặt TÊN trùng verbatim với quyền guard `web` của ERP để cross-guard `whereIn` id khớp khi kiểm quyền và để hiển thị đúng tab phân hệ. `Kế toán kho` (api id 1136) ĐÃ CÓ — KHÔNG tạo lại.

## FACT đã chốt (dùng verbatim, KHÔNG tự đổi)
- Max permission id hiện có trong seeder = **1564**. Dùng ids **1565–1569** cho 5 quyền mới (KHÔNG dùng 1169-1173 — đã trùng).
- Seeder pattern: `run()` xoá `DB::table('permissions')->where('guard_name','api')->delete();` rồi `Permission::create([...])` (class `App\Models\Permission`). Idempotent.

## Việc cần làm

1. Mở file seeder, tìm khối `Permission::create` cuối cùng của phân hệ "Yêu cầu nhập hàng" (quanh id 1162-1168) hoặc bất kỳ vị trí hợp lý trong dãy `Permission::create` guard api. Thêm khối sau (đặt SAU khối liền trước, giữ thứ tự tăng dần id nếu tiện; nếu không, đặt cuối cùng của nhóm api trước dòng đóng):

```php
// ===== Phiếu yêu cầu xuất bán hàng mượn (BorrowSellRequest) — Phase 1 =====
// Trùng tên với quyền guard 'web' của ERP để hiện đúng tab phân hệ + cross-guard whereIn id khi check quyền.
Permission::create(['id' => 1565, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 1]);
Permission::create(['id' => 1566, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của công ty', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của công ty', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 2]);
Permission::create(['id' => 1567, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của phòng ban', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của phòng ban', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 3]);
Permission::create(['id' => 1568, 'guard_name' => 'api', 'name' => 'Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ', 'display_name' => 'Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 4]);
Permission::create(['id' => 1569, 'guard_name' => 'api', 'name' => 'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ', 'display_name' => 'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 5]);
```

**Lưu ý khớp cột:** trước khi thêm, ĐỌC 2-3 dòng `Permission::create` lân cận trong file để chắc chắn tập cột (`id, guard_name, name, display_name, group, type, sort_order`) khớp cách khối hiện có viết. Nếu file dùng thêm/bớt cột nào (vd không có `sort_order`, hoặc có `created_at`), CHỈNH khối trên cho khớp cột thực tế của các dòng lân cận. Đừng bịa cột.

2. Chạy seeder:
```
php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```
Kỳ vọng: chạy xong không lỗi.

3. Verify 5 quyền tồn tại cả 2 guard (web sẵn của ERP + api vừa tạo):
```
php artisan tinker --execute="foreach(['Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty','Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ','Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ'] as \$n){echo \$n.': '.DB::table('permissions')->where('name',\$n)->pluck('guard_name')->implode(',').PHP_EOL;}"
```
Kỳ vọng: mỗi tên in ra chứa `web` VÀ `api`. (Nếu tên nào chỉ có `api` mà không có `web` → OK vẫn được, nhưng ghi lại trong report để controller biết ERP chưa có tên web đó.)

## KHÔNG làm
- KHÔNG commit (controller quản lý commit).
- KHÔNG tạo lại `Kế toán kho`.
- KHÔNG sửa/xoá quyền guard `web`.
- KHÔNG dispatch subagent nào khác.
- KHÔNG đụng file ngoài seeder.

## Report
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-1-report.md`: vị trí chèn (số dòng), cột thực tế đã khớp, output lệnh seed, output lệnh verify (từng tên → guards). Trả về chỉ: status (DONE/BLOCKED/...), tóm tắt 1 dòng kết quả verify, concerns nếu có.
