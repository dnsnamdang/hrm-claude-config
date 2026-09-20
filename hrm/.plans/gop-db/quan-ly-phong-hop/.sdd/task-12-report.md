# Task 12 — 2 quyền mới (đặt/duyệt phòng họp) — Báo cáo

**Status: HOÀN THÀNH**

## (A) Sửa file seeder

File: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
(worktree: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api`)

Thêm 2 dòng ngay dưới 5 dòng quyền phòng họp Phase 1 (id 1574-1578), trước dòng id 1006:

```php
// Đặt phòng họp (Task 12, Phase 2) — id nối tiếp 1578 là id lớn nhất đang có
Permission::create(['id' => 1579, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đặt phòng họp', 'display_name' => 'Xem tất cả phiếu đặt phòng họp', 'group' => 'Quản lý phòng họp', 'type' => 4]);
Permission::create(['id' => 1580, 'guard_name' => 'api', 'name' => 'Duyệt phiếu đặt phòng họp', 'display_name' => 'Duyệt phiếu đặt phòng họp', 'group' => 'Quản lý phòng họp', 'type' => 4]);
```

### Kiểm trùng (trước khi chạy SQL)

```bash
grep -oE "'id' => 15[0-9]{2}" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort | uniq -d
```
→ rỗng (không trùng id trong dải 15xx).

```bash
grep -c "Xem tất cả phiếu đặt phòng họp" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php   # → 1
grep -c "Duyệt phiếu đặt phòng họp" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php          # → 1
```

**KHÔNG chạy** `artisan db:seed` (Ruling R7 vẫn hiệu lực).

## (B) Áp trực tiếp vào DB bằng SQL

Kết nối: `mysql -h127.0.0.1 -uroot -p"$(grep -m1 '^DB_PASSWORD=' .env | cut -d= -f2-)" hrm_erp`
(chạy trong `hrm-worktrees/phong-hop-api`).

### Baseline (trước khi sửa)
```sql
SELECT COUNT(*) FROM permissions WHERE guard_name='api';       -- 745
SELECT id,name FROM permissions WHERE id IN (1579,1580);        -- rỗng
SELECT id,name,guard_name FROM roles WHERE id=18;                -- 18 | Super admin | api
```

### SQL 1 — INSERT 2 quyền (idempotent)
```sql
INSERT INTO permissions (id, guard_name, name, display_name, `group`, type, created_at, updated_at) VALUES
(1579, 'api', 'Xem tất cả phiếu đặt phòng họp', 'Xem tất cả phiếu đặt phòng họp', 'Quản lý phòng họp', 4, NOW(), NOW()),
(1580, 'api', 'Duyệt phiếu đặt phòng họp', 'Duyệt phiếu đặt phòng họp', 'Quản lý phòng họp', 4, NOW(), NOW())
ON DUPLICATE KEY UPDATE name=VALUES(name), display_name=VALUES(display_name), `group`=VALUES(`group`), type=VALUES(type);
```

### SQL 2 — Cấp quyền cho role Super admin (id 18), company_id=1 (idempotent)
```sql
INSERT INTO role_has_permissions (permission_id, role_id, company_id) VALUES
(1579, 18, 1),
(1580, 18, 1)
ON DUPLICATE KEY UPDATE permission_id=VALUES(permission_id);
```

Cả 2 câu SQL được chạy **2 lần** (lần 2 để chứng minh idempotent). Không có lệnh `DELETE`/`TRUNCATE` nào
được chạy trong toàn bộ task.

## Kết quả kiểm chứng

```sql
SELECT id,name,`group`,type FROM permissions WHERE id IN (1579,1580);
```
```
id    name                              group               type
1579  Xem tất cả phiếu đặt phòng họp     Quản lý phòng họp   4
1580  Duyệt phiếu đặt phòng họp          Quản lý phòng họp   4
```

```sql
SELECT permission_id,company_id FROM role_has_permissions WHERE role_id=18 AND permission_id IN (1579,1580);
```
```
permission_id  company_id
1579           1
1580           1
```

```sql
SELECT COUNT(*) FROM permissions WHERE guard_name='api';
```
```
747
```
→ đúng 745 (baseline) + 2 (mới) = **747**. Không có dữ liệu của phiên khác bị mất.

### Kiểm idempotency (chạy lại SQL 1 + SQL 2 lần 2)
- `COUNT(*) WHERE guard_name='api'` → vẫn **747**.
- `COUNT(*) role_has_permissions WHERE role_id=18 AND permission_id IN (1579,1580)` → vẫn **2**.
- Không lỗi, không sinh dòng trùng.

## Định nghĩa hoàn thành — đối chiếu
1. ✅ Seeder có đủ 2 dòng mới, không trùng id, không trùng tên (2 grep sạch).
2. ✅ `permissions` có đúng 2 dòng id 1579, 1580 đúng group/type.
3. ✅ `role_has_permissions` có đúng 2 dòng cho role_id=18, company_id=1.
4. ✅ `COUNT(*) permissions WHERE guard_name='api'` = **747** (745 + 2, đúng kỳ vọng brief).
5. ✅ SQL nguyên văn đã ghi ở trên.

## Ràng buộc đã tuân thủ
- Không `git commit`/`push`/`stash`/`checkout`.
- Chỉ sửa đúng 1 file: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- Không dispatch subagent nào khác, không tự gọi reviewer.

## Concerns
- Không có concern nào phát sinh. Baseline đúng 745 (khớp báo cáo Task 4: 740 + 5), sau khi thêm 2
  quyền ra đúng 747 — không có dấu hiệu mất dữ liệu của phiên làm việc khác.
- Luật "nhìn thấy phiếu" mô tả ở Bước 4 của brief (không có quyền 1579 → chỉ thấy phiếu mình đặt/được
  mời/phòng mình quản lý) thuộc phạm vi Task 14, KHÔNG xử lý trong task này — chỉ ghi nhận lại để tránh
  quên khi làm Task 14.
