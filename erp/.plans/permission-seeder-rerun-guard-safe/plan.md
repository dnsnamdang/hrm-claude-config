# Plan — PermissionsTableSeeder chạy lại an toàn (không mất quyền HRM)

## Tasks
- [x] T1: Đổi dòng 16 `truncate()` → `where('guard_name', 'web')->delete()` (kèm comment giải thích).
- [x] T2: Thêm `const ID_OFFSET = 100000;` + private `createPermission(array $attributes)` (offset id
  +100000, gán `guard_name => 'web'`, gọi `Permission::create`). (dòng 8-27)
- [x] T3: Thay toàn bộ `Permission::create(['id'` → `$this->createPermission(['id'` (1004 chỗ: 957
  active + 47 comment). Helper giữ nguyên `Permission::create($attributes)` (không khớp pattern).
- [x] T4: `php -l` — No syntax errors detected.
- [x] T5: Verify read-only (tinker, KHÔNG ghi DB):
  - 957 active id (+100000) KHỚP 100% id web trong DB (comm -23 rỗng) → offset đúng tuyệt đối.
  - DB web 959 dòng, chỉ dư 2 dòng 100666/100667 ("khải quan" typo) — đã bị comment trong seeder
    vì team gộp sang 788/789 (100788/100789 active, 5/6 role link). Re-run DROP 100666/100667 =
    hội tụ về bản dedup, ĐÚNG ý đồ (giống hệt hành vi seeder gốc). Không phải mất mát ngoài ý muốn.
  - Câu delete chỉ chạm guard=web → 612 dòng guard=api (HRM) an toàn tuyệt đối.

### Checkpoint — 2026-10-05
Vừa hoàn thành: 3 sửa đổi (delete scoped + helper offset+guard + replace 1004 call) + php -l + verify tinker.
Đang làm dở: (không)
Bước tiếp theo: user review; chạy `php artisan db:seed --class=PermissionsTableSeeder` khi muốn. Chưa commit.
Blocked: (không)

## Ghi chú
- Mirror `HRM/hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- KHÔNG chạy seeder vào DB. KHÔNG commit/push khi chưa có yêu cầu. KHÔNG vá dữ liệu.
