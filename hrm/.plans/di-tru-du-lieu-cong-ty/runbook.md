# RUNBOOK — Di trú 1 công ty thành viên vào cổng TPE (chạy lại từ đầu)

> Áp dụng cho ETEK GREEN (ví dụ) hoặc bất kỳ công ty thành viên nào. Thay giá trị theo công ty thực tế.

## Hiểu nhanh có gì TỰ ĐỘNG, gì CHẠY TAY
- 1 lệnh **seeder** lo toàn bộ HR + tự động: bù phép, hạ quyền, danh mục KH/Ngành, phân ca.
- Cơm là DB riêng → **2 lệnh tay** sau seeder.
- (Các lệnh lẻ `company:fold-used-leave`, `company:downgrade-permissions`, `company:migrate-tables` CHỈ dùng để vá công ty đã lỡ di trú TRƯỚC khi có các tính năng này — **chạy mới thì KHÔNG cần**.)

---

## PHẦN 0 — CHUẨN BỊ (1 lần)

### 0.1 Backup DB đích (bắt buộc)
```bash
mysqldump -h<host> -u<user> -p <DB_HR_DICH> > backup_truoc_di_tru_$(date +%F_%H%M).sql
```

### 0.2 Sửa `.env` (hrm-api)
```dotenv
# --- DB NGUỒN (DB nhân sự của cổng thành viên) ---
DB_CONNECTION_SOURCE=mysql
DB_HOST_SOURCE=...
DB_PORT_SOURCE=3306
DB_DATABASE_SOURCE=local_hrm_green     # đổi theo công ty
DB_USERNAME_SOURCE=...
DB_PASSWORD_SOURCE=...

# --- Tham số lần chạy ---
MIGRATION_DRY_RUN=true                  # true=chỉ kiểm tra; false=ghi thật
MIGRATION_SOURCE_COMPANY_ID=            # để trống nếu nguồn chỉ 1 công ty
MIGRATION_RUN_ID=etekgreen              # NHÃN DUY NHẤT mỗi công ty (vd etekpower)
MIGRATION_CONFIRM=                      # phải =YES khi chạy thật

# --- Cờ module (đưa hay không) ---
MIGRATE_CRM=true                        # danh mục Khách hàng/Ngành
MIGRATE_TRAINING=true                   # danh mục Đào tạo
MIGRATE_SMALL_CATALOGS=true

# --- DB CƠM (DB hrm_production của TPE) ---
DB_CONNECTION_TPE=mysql
DB_HOST_TPE=...
DB_PORT_TPE=3306
DB_DATABASE_TPE=hrm_production          # local: hrm_dev_local
DB_USERNAME_TPE=...
DB_PASSWORD_TPE=...
PARENT_COMPANY_ID=1                     # TPE=1 (tenant đích)
```

### 0.3 Sửa `config/company_migration.php`
Thêm 1 dòng vào `leave_recompute_skip` (chống cron `update:attendance` đạp số dư phép):
```php
'leave_recompute_skip' => [
    9 => 2026,   // <company_id MỚI sẽ cấp> => <năm cutover>. Cập nhật SAU khi biết id mới (xem 1.2).
],
```
> Nếu công ty này KHÔNG dùng CRM/Training → đặt cờ tương ứng `=false` ở 0.2.

---

## PHẦN 1 — DI TRÚ HR (1 lệnh, làm 2 lần: thử rồi thật)

### 1.1 Chạy THỬ (dry-run — không ghi gì)
```bash
# .env: MIGRATION_DRY_RUN=true
php artisan db:seed --class=CompanyMigrationSeeder
```
→ Đọc báo cáo: số dòng mỗi bảng, FK chưa dịch, đụng unique... Nếu hợp lý mới chạy thật.

### 1.2 Chạy THẬT
```bash
# .env: MIGRATION_DRY_RUN=false  +  MIGRATION_CONFIRM=YES
php artisan db:seed --class=CompanyMigrationSeeder
```
**Lệnh này tự động làm hết:**
- Hồ sơ NS + tổ chức + cấu hình + số dư + phân quyền (94 bảng)
- Danh mục Khách hàng/Ngành (nếu MIGRATE_CRM=true)
- Phân ca: membership + roster TƯƠNG LAI
- **Bù phép đã dùng** (số NP còn lại đúng)
- **Hạ quyền "tổng công ty" → "theo công ty"** (chống xem chéo công ty)

→ Ghi lại **company_id MỚI** mà lệnh in ra (vd 9). Cập nhật lại `leave_recompute_skip` ở 0.3 với id này (rồi không cần chạy lại seeder).

---

## PHẦN 2 — CƠM (1 lệnh, KHÔNG cần truyền id)

### 2.0 Khai báo 1 lần trong `config/company_migration.php`
Mỗi công ty thêm 1 dòng `run_id => parent_id cũ` (parent cũ: ETEK GREEN=2, POWER=3, ETEK=4):
```php
'rice_relink_map' => [
    'etekgreen' => 2,
    'etekpower' => 3,
    'etek'      => 4,
],
```

### 2.1 Chạy cơm cho TẤT CẢ công ty (tự suy company_id từ migration_id_map)
```bash
php artisan company:finalize-rice --dry-run     # thử tất cả
php artisan company:finalize-rice               # chạy thật tất cả
php artisan company:finalize-rice --run=etekpower   # chỉ 1 công ty
```
Lệnh này tự: suy `company_id` mới + chạy **relink-rice** (đưa cơm cũ về tenant TPE) + **enroll-rice** (tạo hồ sơ cơm NV thiếu) cho từng công ty. **Idempotent** — chạy lại bỏ qua công ty đã xong.

> (Vẫn còn 2 lệnh lẻ `company:relink-rice` / `company:enroll-rice` nếu muốn chạy tay 1 công ty.)

---

## PHẦN 3 — KIỂM TRA NHANH
- Đăng nhập 1 NV của công ty mới → màn Dashboard, Hồ sơ NS, Phân ca, /rice/personal-registration không lỗi.
- Số NV ở "Danh sách tài khoản" = đúng công ty mới (không thấy công ty khác).
- "Số NP còn lại" ở màn nghỉ phép khớp hệ thống cũ.

---

## CHẠY LẠI TỪ ĐẦU CHO CÙNG 1 CÔNG TY (làm lại ETEK GREEN)
Vì data đã ghi + có chốt chống-trùng, KHÔNG chạy đè được. Phải:
1. **Khôi phục DB đích** từ backup (0.1) → về trạng thái trước di trú.
2. (Cơm) xóa dữ liệu cơm đã re-tag/enroll của công ty đó, hoặc khôi phục DB cơm từ backup.
3. Chạy lại từ PHẦN 1.

> Mỗi công ty mới chỉ cần đổi: `DB_DATABASE_SOURCE`, `MIGRATION_RUN_ID`, `--rice-parent`, cờ `MIGRATE_*`, và thêm dòng `leave_recompute_skip`.

## VẬN HÀNH PRODUCTION
- Chạy trong cửa sổ bảo trì (id cấp sát max).
- Sau gộp: gỡ domain cổng thành viên khỏi `RICE_REGISTER_DOMAINS`.
- Đối soát trước: nếu nguồn có `suspend_labor_contracts`/`employee_disciplines`/`increase_seniority_employees` → màn thâm niên có thể tính dư (xử lý tay).
