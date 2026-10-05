> ## ⚠️ NƠI LÀM VIỆC — WORKTREE (chốt 17/09/2026, user yêu cầu)
>
> Nhánh `gop_db` đang được một phiên làm việc khác dùng → mọi thay đổi code của plan này làm trong
> **worktree riêng**, nhánh `feat/quan-ly-phong-hop`:
>
> | Thứ | Đường dẫn |
> |---|---|
> | Repo BE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` |
> | Repo FE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client` |
> | Bộ e2e | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (DÙNG CHUNG, không có worktree) |
> | Tài liệu (plan, ledger) | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/` |
>
> - API của worktree chạy ở **`http://127.0.0.1:8001`**, Nuxt của worktree ở **`http://127.0.0.1:3001`**.
>   Cổng 8000/3000 là server của phiên khác — **KHÔNG đụng, KHÔNG tắt, KHÔNG `pkill`**.
> - Chạy e2e phải truyền cả 2 biến: `BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`.
> - Phiên đăng nhập của Playwright gắn theo ORIGIN. `.auth/user.json` chỉ dùng được cho `:3000` → đã tạo sẵn
>   **`.auth/user-wt.json`** (admin) và **`.auth/user-nocost-wt.json`** (tài khoản thiếu quyền) với origin
>   đổi sang `:3001`. Spec UI phải khai `test.use({ storageState: '.auth/user-wt.json' })`, KHÔNG dùng
>   `user.json` (dùng nhầm là bị đẩy về `/login`, rất dễ tưởng lỗi đăng nhập).
> - TUYỆT ĐỐI KHÔNG `git commit` / `push` / `stash` / `checkout` file.
> - Worktree KHÔNG có `.plans`, `.claude`, `docs`, `CLAUDE.md` (là symlink ngoài repo) — tài liệu ghi về
>   đường dẫn tài liệu ở bảng trên.
> - Đường dẫn trong phần dưới ghi `hrm-api/...` hay `hrm-client/...` thì hiểu là **thư mục tương ứng trong
>   worktree**, không phải checkout gốc.

## Task 4: Thêm 5 quyền vào seeder

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

**Interfaces:**
- Produces: 5 quyền — `Quản lý danh mục phòng họp`, `Xem danh mục phòng họp`,
  `Quản lý danh mục tiện nghi phòng họp`, `Xem danh mục tiện nghi phòng họp`,
  `Xem báo cáo hiệu quả sử dụng phòng họp` (id 1574–1578)

> ⚠️ Seeder **truncate cả bảng** rồi tạo lại → id mới phải nối tiếp id lớn nhất hiện tại là **1573**.
> Quyền `Xem tất cả phiếu đặt phòng họp` và `Duyệt phiếu đặt phòng họp` thuộc **Phase 2**, không thêm ở đây.

- [ ] **Bước 1: Thêm 5 dòng vào nhóm `Danh mục`** (đặt ngay dưới dòng id 1185 — quyền danh mục lý do hủy cuộc họp)

```php
// Quản lý phòng họp (phân hệ Meeting) — id nối tiếp 1573 là id lớn nhất đang có
Permission::create(['id' => 1574, 'guard_name' => 'api', 'name' => 'Quản lý danh mục phòng họp', 'display_name' => 'Quản lý danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1575, 'guard_name' => 'api', 'name' => 'Xem danh mục phòng họp', 'display_name' => 'Xem danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1576, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tiện nghi phòng họp', 'display_name' => 'Quản lý danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1577, 'guard_name' => 'api', 'name' => 'Xem danh mục tiện nghi phòng họp', 'display_name' => 'Xem danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1578, 'guard_name' => 'api', 'name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'display_name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'group' => 'Báo cáo phòng họp', 'type' => 4]);
```

- [ ] **Bước 2: Kiểm trùng id / trùng tên TRƯỚC khi chạy seeder**

```bash
grep -oE "'id' => 15[0-9]{2}" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort | uniq -d
grep -c "Quản lý danh mục phòng họp" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: lệnh 1 không in gì (không id trùng); lệnh 2 in `1`.

- [ ] **Bước 3: Chạy seeder**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```
Kỳ vọng: chạy xong không lỗi khóa trùng.

- [ ] **Bước 4: Cấp quyền cho role admin để test được**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" hrm_erp -e \
"SELECT id,name FROM permissions WHERE id BETWEEN 1574 AND 1578;"
```
Rồi gán vào `role_has_permissions` với **`company_id = 1`** (thiếu cột này quyền không ăn).

---
