# Task 4 — Thêm 5 quyền vào seeder — Báo cáo

**Status: HOÀN THÀNH**

## Bối cảnh / ruling áp dụng
Theo ruling R7 của người điều phối: KHÔNG chạy `artisan db:seed --class=PermissionsTableSeeder`
(seeder khai 856 quyền nhưng DB đang có 740 quyền `guard_name='api'`, trong đó 472 quyền không
được seeder khai — chạy sẽ xoá dữ liệu của phiên làm việc khác). Thay vào đó:
- (A) sửa file seeder làm nguồn chân lý cho lúc deploy.
- (B) áp trực tiếp 5 quyền vào DB bằng SQL thủ công, idempotent, không đụng dữ liệu khác.

## (A) Sửa file seeder

File: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
(worktree: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api`)

Thêm 5 dòng `Permission::create` ngay dưới dòng id 1185 (quyền `Xem danh mục lý do hủy cuộc họp`),
nguyên văn:

```php
// Quản lý phòng họp (phân hệ Meeting) — id nối tiếp 1573 là id lớn nhất đang có
Permission::create(['id' => 1574, 'guard_name' => 'api', 'name' => 'Quản lý danh mục phòng họp', 'display_name' => 'Quản lý danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1575, 'guard_name' => 'api', 'name' => 'Xem danh mục phòng họp', 'display_name' => 'Xem danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1576, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tiện nghi phòng họp', 'display_name' => 'Quản lý danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1577, 'guard_name' => 'api', 'name' => 'Xem danh mục tiện nghi phòng họp', 'display_name' => 'Xem danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1578, 'guard_name' => 'api', 'name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'display_name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'group' => 'Báo cáo phòng họp', 'type' => 4]);
```

### Kiểm Bước 2 (theo brief)

```bash
grep -oE "'id' => 15[0-9]{2}" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort | uniq -d
```
→ kết quả: **rỗng** (không có id trùng trong dải 15xx).

```bash
grep -c "Quản lý danh mục phòng họp" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
→ kết quả: **1** (đúng kỳ vọng).

**KHÔNG chạy** `php artisan db:seed --class=...PermissionsTableSeeder` (Bước 3 của brief bị bỏ qua
theo ruling R7).

## (B) Áp trực tiếp vào DB bằng SQL (không chạy seeder)

Kết nối: `mysql -h127.0.0.1 -uroot -p"$(grep -m1 '^DB_PASSWORD=' .env | cut -d= -f2-)" hrm_erp`
(chạy trong thư mục worktree `hrm-worktrees/phong-hop-api`).

### Kiểm tra trước khi sửa (baseline)
```sql
SELECT COUNT(*) FROM permissions WHERE guard_name='api';        -- 740
SELECT id,name FROM permissions WHERE id BETWEEN 1574 AND 1578; -- rỗng (chưa có)
SELECT id,name,guard_name FROM roles WHERE id=18;                -- 18 | Super admin | api
```

### SQL 1 — INSERT 5 quyền (idempotent)
```sql
INSERT INTO permissions (id, guard_name, name, display_name, `group`, type, created_at, updated_at) VALUES
(1574, 'api', 'Quản lý danh mục phòng họp', 'Quản lý danh mục phòng họp', 'Danh mục', 4, NOW(), NOW()),
(1575, 'api', 'Xem danh mục phòng họp', 'Xem danh mục phòng họp', 'Danh mục', 4, NOW(), NOW()),
(1576, 'api', 'Quản lý danh mục tiện nghi phòng họp', 'Quản lý danh mục tiện nghi phòng họp', 'Danh mục', 4, NOW(), NOW()),
(1577, 'api', 'Xem danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp', 'Danh mục', 4, NOW(), NOW()),
(1578, 'api', 'Xem báo cáo hiệu quả sử dụng phòng họp', 'Xem báo cáo hiệu quả sử dụng phòng họp', 'Báo cáo phòng họp', 4, NOW(), NOW())
ON DUPLICATE KEY UPDATE name=VALUES(name), display_name=VALUES(display_name), `group`=VALUES(`group`), type=VALUES(type);
```

### SQL 2 — Cấp quyền cho role Super admin (id 18), company_id=1 (idempotent)
```sql
INSERT INTO role_has_permissions (permission_id, role_id, company_id) VALUES
(1574, 18, 1),
(1575, 18, 1),
(1576, 18, 1),
(1577, 18, 1),
(1578, 18, 1)
ON DUPLICATE KEY UPDATE permission_id=VALUES(permission_id);
```
(Ghi chú: `role_has_permissions` có khoá chính composite `(permission_id, role_id, company_id)` —
`DESCRIBE role_has_permissions` xác nhận cả 3 cột đều `PRI`, nên `ON DUPLICATE KEY UPDATE` chạy lại
an toàn, không tạo dòng trùng.)

Không có lệnh `DELETE` / `TRUNCATE` nào được chạy trong toàn bộ task.

## Kết quả kiểm chứng sau khi áp SQL

```sql
SELECT id,name,`group`,type FROM permissions WHERE id BETWEEN 1574 AND 1578;
```
```
id    name                                            group               type
1574  Quản lý danh mục phòng họp                       Danh mục            4
1575  Xem danh mục phòng họp                           Danh mục            4
1576  Quản lý danh mục tiện nghi phòng họp              Danh mục            4
1577  Xem danh mục tiện nghi phòng họp                  Danh mục            4
1578  Xem báo cáo hiệu quả sử dụng phòng họp            Báo cáo phòng họp   4
```

```sql
SELECT permission_id, company_id FROM role_has_permissions WHERE role_id=18 AND permission_id BETWEEN 1574 AND 1578;
```
```
permission_id  company_id
1574           1
1575           1
1576           1
1577           1
1578           1
```

```sql
SELECT COUNT(*) FROM permissions WHERE guard_name='api';
```
```
745
```
→ đúng 740 (baseline) + 5 (mới) = **745**. Không có dữ liệu của phiên khác bị mất.

### Kiểm idempotency
Chạy lại nguyên văn SQL 1 và SQL 2 lần thứ 2: `COUNT(*) guard='api'` vẫn **745**, số dòng
`role_has_permissions` cho role 18 trong dải 1574–1578 vẫn **5** — không phát sinh lỗi, không
tạo dòng trùng.

## Định nghĩa hoàn thành — đối chiếu
1. ✅ Seeder có đủ 5 dòng mới, không trùng id (check 1 rỗng), không trùng tên (check 2 = 1).
2. ✅ `permissions` có đúng 5 dòng id 1574–1578 với group/type đúng brief.
3. ✅ `role_has_permissions` có đúng 5 dòng cho role_id=18, company_id=1.
4. ✅ `COUNT(*) permissions WHERE guard_name='api'` = 745 (740 cũ + 5 mới) — không có dấu hiệu mất dữ liệu.
5. ✅ Câu SQL nguyên văn đã ghi ở trên.

## Ràng buộc đã tuân thủ
- Không `git commit` / `push` / `stash` / `checkout`.
- Chỉ sửa đúng 1 file: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- Không dispatch subagent nào khác, không tự gọi reviewer.

## Concerns
- Không có concern nào phát sinh. `role_has_permissions` xác nhận là bảng khoá chính composite
  `(permission_id, role_id, company_id)` nên INSERT idempotent an toàn (không cần thêm điều kiện
  `NOT EXISTS`).
- File seeder đã sửa hiện chỉ tồn tại trong worktree `hrm-worktrees/phong-hop-api`, chưa merge vào
  nhánh `gop_db` chính — cần bước merge/PR riêng ở giai đoạn sau (ngoài phạm vi Task 4).
