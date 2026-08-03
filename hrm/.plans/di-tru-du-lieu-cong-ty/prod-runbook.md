# RUNBOOK PRODUCTION — Di trú công ty thành viên vào cổng TPE

> Server TPE: `/var/www/tpe/hrm-api`. DB đích = `hrm_production`. Cơm (mysql_tpe) cũng = `hrm_production` (CÙNG DB trên prod).
> Mỗi công ty: đổi DB nguồn + nhãn run + chạy. **Bắt buộc: backup + cửa sổ bảo trì + chạy thử trên COPY trước.**

---

## ⚠️ NGUYÊN TẮC AN TOÀN (đọc trước)
1. **Backup `hrm_production`** trước mỗi công ty (DB này chứa data MỌI công ty TPE đang chạy thật).
2. **Chạy thử trên COPY** của `hrm_production` cho công ty đầu tiên, verify, rồi mới chạy prod thật.
3. **Cửa sổ bảo trì**: engine cấp id sát max — không cho ghi đồng thời.
4. Prod thường bật `config:cache` → sau khi sửa `.env` PHẢI `config:clear`, xong việc thì `config:cache` lại.

---

## PHẦN A — CHUẨN BỊ (1 lần)

### A.1 Backup
```bash
mysqldump -h192.168.122.103 -uhrm_tpe -p hrm_production > /backup/hrm_production_$(date +%F_%H%M).sql
```

### A.2 Kiểm tra parent_id cơm của các cổng (để khai rice_relink_map)
```bash
mysql -h192.168.122.103 -uhrm_tpe -p hrm_production -e "SELECT parent_id, COUNT(*) FROM rice_companies GROUP BY parent_id;"
```
→ Ghi nhận: TPE=1, ETEK GREEN=2, POWER=3, ETEK=4 (xác nhận đúng thực tế prod).

### A.3 Pull code mới (đã có engine + các command)
```bash
cd /var/www/tpe/hrm-api && git pull   # hoặc deploy theo quy trình của bạn
```

### A.4 Khai `config/company_migration.php` cho TẤT CẢ công ty sẽ gộp (1 lần)
```php
'leave_recompute_skip' => [
    // <company_id MỚI> => <năm cutover>  (cập nhật id sau khi seed mỗi công ty)
],
'rice_relink_map' => [
    'etekgreen' => 2,
    'etekpower' => 3,
    'etek'      => 4,
],
```

---

## PHẦN B — CHẠY CHO 1 CÔNG TY (lặp cho từng công ty)
> Ví dụ ETEK GREEN (source `hrm_green`, run `etekgreen`, parent cơm cũ 2).

### B.1 Sửa `.env` (TPE) — phần SOURCE + tham số
```dotenv
# DB nhân sự của cổng thành viên (cùng MySQL server 192.168.122.103)
DB_CONNECTION_SOURCE=mysql
DB_HOST_SOURCE=192.168.122.103
DB_PORT_SOURCE=3306
DB_DATABASE_SOURCE=hrm_green          # ĐỔI theo công ty (vd hrm_power)
DB_USERNAME_SOURCE=hrm_green
DB_PASSWORD_SOURCE=baWptZgXiCvAje5

# Tham số lần chạy
MIGRATION_RUN_ID=etekgreen            # NHÃN RIÊNG mỗi công ty
MIGRATE_CRM=true                      # tùy công ty
MIGRATE_TRAINING=true
MIGRATION_DRY_RUN=true                # thử trước
MIGRATION_CONFIRM=
```
> `DB_*_TPE` (cơm) trên prod đã trỏ `hrm_production` — giữ nguyên.

### B.2 Xóa cache config (sau khi sửa .env)
```bash
php artisan config:clear
```

### B.3 Di trú HR — CHẠY THỬ (không ghi)
```bash
php artisan db:seed --class=CompanyMigrationSeeder 2>&1 | tee /backup/dryrun_etekgreen.log
```
→ Đọc log: số dòng/bảng, FK chưa dịch, đụng unique. Hợp lý mới qua B.4.

### B.4 Di trú HR — CHẠY THẬT (trong bảo trì)
```dotenv
# sửa .env:
MIGRATION_DRY_RUN=false
MIGRATION_CONFIRM=YES
```
```bash
php artisan config:clear
php artisan db:seed --class=CompanyMigrationSeeder 2>&1 | tee /backup/real_etekgreen.log
```
→ **Ghi lại `company_id` MỚI** trong log (vd 9). Lệnh này tự làm: hồ sơ+tổ chức+lương+phân quyền + danh mục KH/Ngành + phân ca + **bù phép** + **hạ quyền tổng-công-ty**.

### B.5 Cập nhật `leave_recompute_skip` với id mới
```php
'leave_recompute_skip' => [
    9 => 2026,   // id mới vừa cấp => năm cutover
],
```

### B.6 Cơm (relink + enroll)
```bash
php artisan config:clear
php artisan company:finalize-rice --run=etekgreen --dry-run   # thử
php artisan company:finalize-rice --run=etekgreen             # thật
```

### B.7 Verify nhanh (xem PHẦN C) → mở lại hệ thống → lặp công ty kế tiếp (về B.1)

---

## PHẦN C — VERIFY (mỗi công ty)
```bash
# Đếm trên DB
mysql -h192.168.122.103 -uhrm_tpe -p hrm_production -e "
SELECT COUNT(*) nv FROM employee_infos WHERE company_id=9;
SELECT COUNT(*) rice_nv FROM rice_employee_infos rei JOIN rice_companies rc ON rc.id=rei.rice_company_id WHERE rc.company_id=9 AND rc.parent_id=1;"
```
- Đăng nhập 1 NV công ty mới: Dashboard, Hồ sơ NS, Phân ca, **/rice/personal-registration** không lỗi.
- "Danh sách tài khoản" chỉ thấy công ty mới (không xem chéo).
- "Số NP còn lại" khớp hệ thống cũ.

---

## PHẦN D — SAU KHI XONG TẤT CẢ
```bash
# Bật lại cache config (prod)
php artisan config:cache

# Gỡ domain các cổng thành viên khỏi .env (tránh notify cơm trùng)
# RICE_REGISTER_DOMAINS=... (bỏ domain etekgreen/power/etek)
php artisan config:clear && php artisan config:cache
```

---

## PHẦN E — ROLLBACK (nếu sai)
1. **Khôi phục `hrm_production`** từ backup PHẦN A.1 (cách chắc chắn nhất — về trước di trú).
2. Hoặc rollback theo run: xóa data đã chèn theo `migration_id_map` (run_id) — chỉ khi thành thạo; ưu tiên khôi phục backup.

---

## TÓM TẮT 1 CÔNG TY = 6 lệnh
```bash
# (sửa .env: DB_DATABASE_SOURCE + MIGRATION_RUN_ID; DRY_RUN=true)
php artisan config:clear
php artisan db:seed --class=CompanyMigrationSeeder            # thử
# (sửa .env: DRY_RUN=false + CONFIRM=YES; cập nhật config leave_recompute_skip + rice_relink_map)
php artisan config:clear
php artisan db:seed --class=CompanyMigrationSeeder            # thật  -> ghi id mới
php artisan company:finalize-rice --run=<run_id>             # cơm
```
> Hoặc sau khi seed HẾT các công ty: `php artisan company:finalize-rice` (không --run) để chạy cơm tất cả 1 lượt.
