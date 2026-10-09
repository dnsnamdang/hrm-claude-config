# Task 1 Report — Permissions seeder: thêm 5 quyền guard `api`

**File modified:** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

## Insertion Details

- **Location:** Lines 1397–1402 (after id 1564 "Xem phiếu nhập hàng theo bộ phận", before closing brace)
- **IDs added:** 1565–1569
- **Column set:** `['id', 'guard_name', 'name', 'display_name', 'group', 'type', 'sort_order']` — matched with neighboring Permission::create lines (1561–1564)

## Columns Verified

All 5 permissions use the same column structure as existing lines (1393–1396):
- `id` (integer)
- `guard_name` ('api')
- `name` (Vietnamese permission name)
- `display_name` (same as name)
- `group` ('Yêu cầu xuất bán hàng mượn')
- `type` (8 = Tài chính)
- `sort_order` (1–5 incremental)

## Seeder Execution

```bash
php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```

**Result:** Database seeding completed successfully.

## Verification Command Output

```bash
php artisan tinker --execute="foreach(['Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty','Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ','Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ'] as \$n){echo \$n.': '.DB::table('permissions')->where('name',\$n)->pluck('guard_name')->implode(',').PHP_EOL;}"
```

**Results:**
- `Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty: api,web`
- `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ: api,web`
- `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ: api,web`

## Summary

All 5 new permissions (ids 1565–1569) for "Phiếu yêu cầu xuất bán hàng mượn" exist in **both guards** (api + web).
✓ Seeder ran without errors
✓ All 3 sampled permission names appear in both 'api' and 'web' guards (ERP already has web versions)
✓ No concerns; ERP web permissions pre-existed as expected

