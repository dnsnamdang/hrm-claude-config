# RUNBOOK PRODUCTION — Di trú công ty thành viên vào cổng TPE

> Server TPE: `/var/www/tpe/hrm-api`. **DB đích nay là `hrm_erp_gop`** (từ 24/09/2026, sau khi gộp ERP+HRM —
> trước đó là `hrm_production`, DB đó vẫn còn trên máy nhưng KHÔNG dùng nữa). Cơm (`mysql_tpe`) cùng DB.
> Mỗi công ty: đổi DB nguồn + nhãn run + chạy. **Bắt buộc: backup + cửa sổ bảo trì + chạy thử trên COPY trước.**
>
> 🔴 **TRƯỚC KHI GỘP CỔNG KẾ TIẾP (etekpower): ĐỌC [PHẦN F](#phần-f--bài-học-từ-etek-green-bắt-buộc-đọc-trước-cổng-kế-tiếp) ở cuối file.**
> Đó là 14 lỗi đã trả giá thật khi gộp ETEK GREEN 24–25/09/2026, phần lớn **không báo lỗi gì** —
> chạy xong tưởng xong, vài ngày sau người dùng mới phát hiện mất dữ liệu.

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

---

## ⭐ CHẠY GỌN — 1 LỆNH DUY NHẤT (cập nhật 05/09/2026)

Từ nay không cần sửa `.env` cho từng công ty nữa. Một lệnh làm đủ 6 bước:
di trú HR → cơm (re-link + enroll) → **đưa ảnh lên S3** → đánh lại mã → đẩy ERP.

### Bước 1 — backup (bắt buộc)
```bash
mysqldump -h<host> -u<user> -p hrm_production > /backup/hrm_production_$(date +%F_%H%M).sql
```

### Bước 2 — chạy THỬ (không ghi gì)
```bash
php artisan company:migrate-full \
  --source-db=hrm_green \
  --run=etekgreen \
  --rice-parent=2 \
  --asset-dir=/backup/etekgreen/public \
  --timesheet-from=2026-01-01 \
  --dry-run
```

### Bước 3 — chạy THẬT
```bash
php artisan company:migrate-full \
  --source-db=hrm_green \
  --run=etekgreen \
  --rice-parent=2 \
  --asset-dir=/backup/etekgreen/public \
  --timesheet-from=2026-01-01 \
  --confirm
```
→ Ghi lại **company_id MỚI** lệnh in ra, rồi thêm vào `config/company_migration.php`:
`'leave_recompute_skip' => [ <id mới> => 2026 ]`

### Giải thích tham số
| Tham số | Ý nghĩa |
|---|---|
| `--source-db` | DB nhân sự của cổng thành viên |
| `--run` | nhãn riêng mỗi công ty (etekgreen / etekpower / etek) |
| `--rice-parent` | parent_id cơm cũ của cổng: GREEN=2, POWER=3, ETEK=4. Bỏ trống = không xử lý cơm |
| `--timesheet-from` | MỐC lấy dữ liệu CHẤM CÔNG (vd `2026-01-01`) → Bảng chấm công chi tiết/tổng hợp, Báo cáo tổng hợp chấm công và Báo cáo phép hiển thị đúng như cổng cũ. Bỏ trống = không lấy chấm công (phép đã nghỉ dồn vào ô "nghỉ ngoài PM") |
| `--cutover-date` | NGÀY chuyển cổng (yyyy-mm-dd). Đơn xin nghỉ ĐÃ DUYỆT có ngày nghỉ từ mốc này trở đi mới đưa sang. Mặc định = ngày chạy lệnh — khai khi chạy di trú TRƯỚC ngày cutover |
| `--asset-dir` | thư mục sao lưu ảnh của cổng cũ (chứa `/uploads/...`) → bật bước đưa ảnh lên S3 |
| `--asset-url` | dùng THAY `--asset-dir` khi cổng cũ CÒN CHẠY, vd `https://hrm-etekgreen...` |
| `--no-assets` | bỏ qua bước ảnh |
| `--no-erp` | không đẩy sang ERP |
| `--no-recode` | không đánh lại mã nhân viên |

### Nếu bước ảnh lỗi mạng / chưa có thư mục ảnh lúc chạy
Chạy lại RIÊNG phần ảnh, không phải di trú lại (chạy nhiều lần không đẩy trùng):
```bash
php artisan company:upload-assets --run=etekgreen --dir=/backup/etekgreen/public --dry-run
php artisan company:upload-assets --run=etekgreen --dir=/backup/etekgreen/public
```

⚠️ Ảnh của cổng thành viên lưu dạng đường dẫn nội bộ. **Phải lấy được file** (thư mục sao lưu,
hoặc chạy khi cổng cũ chưa tắt), nếu không ảnh nhân sự sẽ hỏng sau khi cổng cũ ngừng hoạt động.


---

## PHẦN F — BÀI HỌC TỪ ETEK GREEN (bắt buộc đọc trước cổng kế tiếp)

> Gộp ETEK GREEN (company_id 9, run `etekgreen`) ngày 24–25/09/2026. Tất cả mục dưới đây là lỗi
> **đã xảy ra thật**, kèm cách phát hiện và câu lệnh xử lý. Đặc điểm chung: **đa số không có
> exception, không có log lỗi** — hệ thống chạy bình thường, chỉ sai/mất dữ liệu âm thầm.
> Cổng kế tiếp dự kiến **etekpower** (DB nguồn `hrm_power`, rice `parent_id = 3`).

### F.0 Checklist rút gọn — dán ra giấy khi chạy

**Trước khi chạy**
- [ ] Backup DB đích. Tắt cron + queue worker của CẢ cổng đích lẫn cổng nguồn (F.1).
- [ ] `php artisan company:migrate-check-schema` — lệch cột là dừng.
- [ ] Rà `skip` trong catalog: bảng con của cha đã `owned` thì phải gỡ khỏi skip (F.4), và
      tách rõ CẤU HÌNH theo công ty (phải đưa) với giao dịch theo kỳ (bỏ được) — F.18.

**Chạy**
- [ ] Chạy 1 lượt duy nhất, có `--rice-parent` (F.3).

**Sau khi chạy — 7 việc hay bị bỏ sót**
- [ ] `php artisan migrate` (khoá ngoại liên-database) rồi kiểm còn 0 khoá trỏ ra ngoài (F.2).
- [ ] Đổi mã trên máy chấm công + **kiểm bằng danh sách user đọc từ máy** (F.6).
- [ ] Lấy bù lượt quẹt bị mất trong khoảng giữa recode và đổi mã máy (F.7).
- [ ] Bù roster phân ca kỳ cũ nếu nghiệp vụ cần (F.9).
- [ ] Bỏ domain cổng vừa hạ khỏi `RICE_REGISTER_DOMAINS` của **cả 3 cổng còn lại** (F.10).
- [ ] Hạ cổng nguồn cho trọn: cron + supervisor + `autostart=false` (F.11).
- [ ] **Đổi mã trên MÁY QUÉT CƠM** (`rice_conn_infos`) — bảng RIÊNG, `hikvision:recode`
      không chạm; chạy `rice:recode` 2 lượt rồi lấy bù `rice:fetch-checkin` (F.17).
- [ ] Phòng ban trùng tên với TPE → gắn tiền tố vào MÃ phòng (F.16).
- [ ] Chạy đủ mục **F.14 — verify sau cùng**.

---

### F.1 Cron/queue chèn chiếm dải id → `1062 Duplicate entry`
Engine đặt trước dải id sát `max(id)`. Cron TPE chèn 522 dòng lúc 01:00 chiếm đúng dải đó →
`1062 Duplicate entry '619524' for key 'timesheet_summaries.PRIMARY'`, phải rollback cả lượt.

- Đã vá bằng `CompanyMigrationService::reserveIdRanges()` (đẩy `AUTO_INCREMENT` = `max(id)` +
  số dòng nguồn + **1000** dư, gọi TRƯỚC `beginTransaction()`).
- Vẫn **phải tắt cron + queue worker** trong cửa sổ chạy. Cron của các cổng nằm CHUNG một
  `crontab -l` của user `erp_tpe` (~96 dòng) — lọc theo đường dẫn `/var/www/<cổng>/`.
- ⚠️ `information_schema.TABLES.AUTO_INCREMENT` bị **cache** với InnoDB → đọc bằng
  `SHOW CREATE TABLE`, đừng tin `information_schema`.

### F.2 Khoá ngoại liên-database → mọi bản ghi MỚI bị chặn `1452`
Sau khi gộp, **50 khoá ngoại trên 19 bảng** vẫn trỏ sang DB cũ (`hrm_production`, `erp_new`).
MySQL cho phép khoá liên-database nên lúc gộp **không lỗi gì**, nhưng bản ghi mới bị chặn vì id
chỉ tồn tại ở DB gộp. Trả giá thật: nhân sự ETEK GREEN **không đăng ký được thiết bị chấm công**
(10 lần thử đều 1452), và nhóm **Lương** (`salary_employees.employee_id`) sẽ chặn tính lương.

Đã đóng gói thành migration `2026_09_25_000001_fix_cross_database_foreign_keys` (tự dò
`information_schema`, giữ nguyên tên khoá/cột/`ON DELETE`-`ON UPDATE`, đếm mồ côi trước khi sửa).

⚠️ **Bẫy đắt nhất**: `ALTER TABLE ... ADD CONSTRAINT` làm MySQL dựng bảng tạm và **kiểm lại MỌI
khoá ngoại đang có của bảng đó**. Cùng bảng còn một khoá khác trỏ DB cũ và có mồ côi → câu `ADD`
hỏng **vì khoá KHÁC**, mà `DROP` đã chạy xong → khoá bị xoá mà không dựng lại được. Lần đầu:
37/50 sửa được, **13 khoá của 6 bảng nhóm Lương mất ràng buộc âm thầm**, phải dựng lại tay.
→ Phải xử lý **theo từng BẢNG**: đếm mồ côi cho toàn bộ khoá của bảng trước, chỉ cần 1 khoá
không sửa được thì **bỏ qua cả bảng**. Bản trong repo đã làm đúng vậy.

Kiểm còn sót: (⚠️ `.env` prod dùng **cổng 33062**, không phải 3306)
```sql
SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
WHERE CONSTRAINT_SCHEMA='hrm_erp_gop'
  AND REFERENCED_TABLE_SCHEMA IS NOT NULL AND REFERENCED_TABLE_SCHEMA<>'hrm_erp_gop';
```

### F.3 Sai thứ tự recode ↔ cơm → mã cơm lệch
Chạy phần cơm SAU `company:recode-unified` thì mã chấm công cơm lệch **125/130** người.
→ Phải chạy **cùng một lượt** (`company:migrate-full ... --rice-parent=<parent cũ>`). Chạy đúng
thứ tự thì lệch 0.

### F.4 Bảng con còn trong `skip` dù cha đã `owned` → màn chi tiết RỖNG
`overtime_report_detail` trả `details: []` vì 4 bảng con vẫn nằm ở `skip`. Không có lỗi nào báo ra.
→ Sau khi thêm bảng vào catalog, **rà lại cả nhóm cha–con**. Bù sau bằng
`php artisan company:migrate-tables --source=<id> --run=<run> --tables=<a,b,c>`.

### F.5 Bốn cái bẫy trong chính catalog
- **Filter đặt sai cột**: `admin_request_update_workings` lọc theo `to_date` (NULL 416/416) → di trú
  **0/416** dòng. Đổi sang `from_date`.
- **Cột đảo nhau ở cả nguồn lẫn đích**: `conn_info_overtime_assignments` → ánh xạ theo **nội dung**,
  KHÔNG sửa model.
- **Cột tên giống khoá ngoại nhưng KHÔNG phải khoá ngoại**: `timesheets.employee_info_id` thực chất
  lưu **MÃ CHẤM CÔNG** (`TimeWorkingService` ghi `(int)$ssn` vào đó, dòng 448/456/479). Dịch như
  khoá ngoại là gán sang **người khác**. Đã thêm directive `SSN:employee_infos`.
  → Đừng join `timesheets.employee_info_id` sang `employee_infos.id`; phải join `employee_infos.ssn`.
- **Bảng bị đổi tên khi gộp**: bản HRM của 13 bảng trùng tên đã thành `hrm_*` → thiếu
  `target_table_alias` là ghi nhầm vào **bảng của ERP** (`groups`, `scopes`).

### F.6 Máy chấm công Hikvision — 2 bẫy, cả hai đều im lặng
**(a) Mã trên máy có số 0 ở đầu.** DB lưu `92`, trên máy là `"092"`. Tra ISAPI với `"92"` trả
`NO MATCH` → `hikvision:recode` báo "Không thấy mã cũ trên máy" rồi **bỏ qua người đó**. Đo thật:
**15 mã** kiểu này trên 2 máy, **8 người chưa được đổi mã** (4 người vẫn đang đi làm, vừa quẹt máy
tuần trước). Đã vá bằng `HikvisionSyncService::timMaCuTrenMay()` (thử nguyên văn → bỏ 0 đầu → thêm
dần 0 tới 9 ký tự). **Luôn đối chiếu HỌ TÊN lưu trên máy** trước khi kết luận `092` là ai.

**(b) Mã mới đã có nhưng mã cũ còn sót.** Bản cũ thấy mã mới tồn tại là `return` luôn, để lại
entry mang mã cũ — mã đó không còn khớp ai trong `employee_infos.ssn` nên **người quẹt vào entry
đó là mất trắng lượt**. Nay `--delete-old` dọn cả trường hợp này.

Đừng tin số báo của lệnh — **đọc danh sách user trực tiếp từ máy** rồi đối chiếu:
```bash
curl -s --digest -u "$UN:$PW" -X POST "http://$IP:$PT/ISAPI/AccessControl/UserInfo/Search?format=json" \
  -H "Content-Type: application/json" \
  -d '{"UserInfoSearchCond":{"searchID":"ls","searchResultPosition":0,"maxResults":30}}'
```
Kết quả đúng khi gộp GREEN: máy 36 còn 94 user / máy 37 còn 93 user, **91 mã mới, 0 mã cũ**, mọi mã
tra ra người của công ty 9.

### F.7 `attendance:fetch` bỏ IM LẶNG lượt quẹt mang mã cũ → mất lượt chấm công
Máy **giữ mã CŨ trong log đã quẹt** kể cả sau khi đã đổi mã trên máy (bản ghi lịch sử không được
viết lại). Lệnh hút log tra `employee_infos.ssn` không thấy ai thì `continue` lặng lẽ.
**Kết quả: ETEK GREEN mất toàn bộ lượt quẹt máy từ lúc recode (24/09) tới khi đổi mã máy xong (25/09).**

**Dấu hiệu nhận biết:** công ty vừa gộp có **0 lượt chấm máy trong ngày** trong khi công ty khác
vẫn bình thường:
```sql
SELECT company_id, MAX(DATE(verify_date)) lan_cuoi, COUNT(*) FROM timesheets
WHERE conn_info_id IS NOT NULL GROUP BY 1 ORDER BY lan_cuoi DESC;
```
Đã vá: tra thêm `employee_code_mappings` (`old_ssn → new_ssn`), **lọc theo `company_id` của chính
máy** vì `old_ssn` là số nhỏ rất dễ trùng giữa công ty; tra vẫn không ra thì **ghi log cảnh báo**.

Lấy bù dữ liệu đã mất (**bắt buộc `--conn=`**, vì lệnh vốn hút MỌI máy Hikvision → khoảng ngày rộng
sẽ dựng lại bản ghi cũ của các công ty khác):
```bash
php artisan attendance:fetch "24/09/2026 00:00" "25/09/2026 09:50" --conn=36,37
```
Kết quả thật: 24/09 từ 47 → 94 lượt, 25/09 từ 0 → 14 lượt.

### F.8 Chỉ thiết bị ĐẦU TIÊN được tự duyệt → người cũ đăng ký lại bị kẹt "Gửi duyệt"
`DeviceService::store()` chỉ gọi `approve()` khi `$count == 0`. Nhân sự đã từng có thiết bị ở cổng
cũ, sang cổng mới đăng ký lại → phiếu nằm ở "Gửi duyệt", `TimekeeperController` đòi `status = 2`
nên **không chấm công được trên app**. Đã bỏ điều kiện đó (đăng ký xong là dùng được ngay).

### F.9 Phân ca chỉ có TỪ NGÀY CUTOVER → màn tổng hợp phân ca trắng
Catalog khai `shift_detail_employee_dates` với `'date_from_today'` (chủ ý: bỏ kỳ cũ). Nhưng màn
`/timesheet/timeworking/shift-detail/general` mặc định lấy **cả tháng hiện tại** → mọi ngày trước
cutover trắng trơn, người dùng báo "không có phân ca". Đo thật: 72/72 nhân sự có ca ở 25–30/09
nhưng **0/72 ở 01–24/09**.

Nếu nghiệp vụ cần lịch sử → bù bằng lệnh riêng (KHÔNG dùng `company:migrate-tables`: lệnh đó có
guard chống chạy lại, muốn dùng phải xoá hết roster đã có đi làm lại):
```bash
php artisan company:backfill-shift-roster --run=etekgreen --from=2026-01-01            # thử
php artisan company:backfill-shift-roster --run=etekgreen --from=2026-01-01 --confirm  # thật
```
**Mốc `--from` nên lấy đúng mốc đã dùng cho bảng công** (`timesheet_summaries` của công ty đó —
với GREEN là `2026-01-01`), để hai bên khớp nhau.

⚠️ **Công định mức được tính LIVE theo ngày phân ca** (`TimesheetSummaryService::calcStandardWithCache`,
không đọc bảng lưu) → bù roster kỳ cũ **làm bảng công các tháng đã qua thay đổi**. Phải được chốt
trước khi chạy. Gỡ lại: xoá các dòng có id trong `migration_id_map` với `run_id = '<run>-backfill'`.

### F.10 `RICE_REGISTER_DOMAINS` — phải sửa ở CẢ 3 cổng còn lại
Biến này là danh sách cổng được gọi vòng để bắn thông báo cơm (10 chỗ trong `Modules/Rice`). Để
nguyên domain cổng vừa hạ thì **mỗi lượt thông báo cơm treo timeout rồi ghi log 503**.

Bẫy: mỗi cổng ghi domain ETEK GREEN bằng **tên khác nhau** — cổng `tpe` dùng `hrm.etekgreen.com`,
còn `etek` và `etekpower` dùng `hrm.wetek.vn`. Sửa 1 chỗ là chưa xong.
→ Đo thật từng domain trước khi cắt: `curl -o /dev/null -w "%{http_code}"` (400 = app còn sống,
503/000 = đã chết). Prod **không** bật `config:cache` nên sửa `.env` có hiệu lực ngay.

### F.11 Hạ cổng nguồn cho trọn — cron + supervisor
Hạ web thôi là chưa đủ. Cổng ETEK GREEN vẫn còn **11 dòng cron** (`attendance:fetch` 5 phút/lần,
`calc:timesheet`, `rice:*`, app python) ghi vào DB cũ, và **3 supervisor worker** đang **khởi động
lại liên tục (uptime 0–3 giây)** — vòng lặp lỗi đốt CPU.
→ Ghi chú (comment) 11 dòng cron; `supervisorctl stop` 3 program **và** đặt `autostart=false` trong
`/etc/supervisor/conf.d/<cổng>-*.conf` rồi `reread` + `update`, nếu không supervisor khởi động lại
là bật lên. Sao lưu trước: `crontab -l > ~/crontab.bak_<ts>`, `cp <conf> <conf>.bak_<ts>`.

**MỞ LẠI cổng nguồn** (30/09/2026 đã làm thật với etekgreen — khách cần vào đối chiếu dữ liệu). Phải
mở đủ **4 thứ**, thiếu 1 là thấy lỗi mà không hiểu vì sao:
```bash
sudo pm2 start hrm-client-<cong>                  # 1) giao diện Nuxt (pm2, chạy bằng root)
sudo chmod 757 /var/run/hrm-client-<cong>.sock    # 2) ⚠ BẮT BUỘC — xem ghi chú dưới
cd /var/www/<cong>/hrm-api && php artisan up      # 3) tắt chế độ bảo trì của API
# 4) cron: bỏ dấu # ở các dòng của cổng đó; supervisor: autostart=true + supervisorctl start
```
⚠️ **Bẫy socket**: pm2 tạo lại socket MỖI LẦN khởi động với quyền `srwxr-xr-x`, mà nginx chạy bằng
`www-data` cần quyền **ghi** → nginx trả **502 Bad Gateway** dù pm2 báo `online` và log Nuxt ghi
"Listening on: unix+http://...". Các cổng đang chạy đều là `srwxr-xrwx` (757) vì đã được chmod từ
lần khởi động trước. Dấu hiệu xác nhận: `/var/log/nginx/error.log` ghi
`connect() to unix:/var/run/hrm-client-<cong>.sock failed (13: Permission denied)`.
→ Cứ `pm2 restart` cổng nào thì phải chmod lại socket của cổng đó.

Khi mở lại, cron/queue của cổng nguồn **an toàn** vì mọi lệnh chỉ ghi vào DB riêng của nó
(`hrm_green`) và `DB_DATABASE_TPE` của cổng đó trỏ `hrm_production` (DB TPE CŨ, không còn dùng) —
đã kiểm: 2 lệnh `rice:delete-old-notification` / `rice:store-rice-subsidy` **không** có HTTP client
nên không bắn thông báo sang cổng đang chạy thật, dù `RICE_REGISTER_DOMAINS` của nó vẫn liệt kê
`hrm.eteksofts.com`. Nhưng **dữ liệu nhập mới trên cổng nguồn sẽ KHÔNG chảy sang cổng TPE** — chỉ
nên mở để ĐỌC/đối chiếu, xong thì đóng lại.

### F.12 Thông báo đẩy: app cổng cũ dùng tiền tố topic RIÊNG
`TPE_APP/.../build_config.dart`: bản `wetek` (ETEK GREEN) đăng ký `wetek_production_`, bản
`production` (TPE) dùng `topics_development_`, mà cổng TPE bắn `FCM_TOPIC_PREFIX=topics_development_`.
→ Nhân sự cổng cũ **phải chuyển hẳn sang app TPE** mới nhận được thông báo. Không sửa được bằng
`.env`, phải phát hành/hướng dẫn cài app. Nói trước với họ, đừng để phát hiện sau.

Liên quan: `device_id` do app tự sinh (iOS `FlutterUdid` theo bundle id, Android `ANDROID_ID` theo
khoá ký) → **đổi app là đổi device_id**, nên người dùng buộc phải đăng ký lại thiết bị (xem F.8).

### F.13 Quyền ERP prod và UAT khác nhau → lấy nguyên theo prod
Khi đối chiếu phân quyền, UAT lệch prod (966 quyền). Đã đồng bộ `permissions` UAT theo prod, lệch 0.
Ngoài ra ERP có lỗi **thêm quyền bị `1062 Duplicate entry`** do UI vẽ trùng checkbox
(`$scope.groupRoles` khoá chỉ theo `group`, không theo `group_category`) — sửa 2 lớp: khoá theo
chuyên-mục + nhóm ở blade, và `array_unique` trong `Role::syncPermissionsByCompany()`.

### F.14 VERIFY SAU CÙNG — làm đủ, đừng bỏ bước nào
```sql
-- 1) Không còn khoá ngoại trỏ ra ngoài DB gộp  => phải = 0
SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
 WHERE CONSTRAINT_SCHEMA='hrm_erp_gop' AND REFERENCED_TABLE_SCHEMA IS NOT NULL
   AND REFERENCED_TABLE_SCHEMA<>'hrm_erp_gop';

-- 2) Ghi thử bản ghi MỚI cho 1 nhân sự của công ty vừa gộp, rồi ROLLBACK
--    (đây là phép thử duy nhất bắt được lỗi 1452 F.2)
START TRANSACTION;
INSERT INTO devices (device_id,name,employee_info_id,status,created_by,updated_by,company_id,created_at,updated_at)
 VALUES (CONCAT('kt-',UUID()),'kiem tra',<employee_info_id>,2,<employee_id>,<employee_id>,<cty>,NOW(),NOW());
INSERT INTO salary_employees (salary_id,employee_id,company_id,created_by,updated_by,created_at,updated_at)
 VALUES (<salary_id>,<employee_info_id>,<cty>,<employee_id>,<employee_id>,NOW(),NOW());
ROLLBACK;

-- 3) Có lượt chấm MÁY trong ngày, và mọi mã tra ra người
SELECT company_id, MAX(DATE(verify_date)) lan_cuoi FROM timesheets
 WHERE conn_info_id IS NOT NULL GROUP BY 1;

-- 4) Phân ca đủ cả tháng (nếu đã bù F.9)
SELECT COUNT(*), MIN(s.date), MAX(s.date) FROM shift_detail_employee_dates s
 JOIN employee_infos ei ON ei.id=s.employee_info_id WHERE ei.company_id=<cty>;
```
```bash
# 5) Log: 0 lỗi 1452 và 0 lỗi gọi domain cổng đã hạ
grep -a "^\[$(date +%F)" storage/logs/laravel.log | grep -cE "1452|etekgreen|wetek\.vn"

# 6) Đăng nhập THẬT bằng 1 tài khoản của công ty vừa gộp rồi gọi API màn nghi ngờ —
#    nhanh và chắc hơn đoán qua SQL (xem cách làm ở mục F.7/F.9)
```

**Cách tự kiểm hiệu quả nhất, rút ra từ lần này:** phần lớn lỗi ở đây **không** lộ qua SQL đếm
dòng (dòng vẫn đủ, chỉ sai nghĩa hoặc sai người). Cứ **đăng nhập bằng tài khoản thật của công ty
vừa gộp**, mở đúng màn nghiệp vụ, và **đọc trực tiếp từ thiết bị/máy chấm công** thay vì tin số
báo của lệnh.

---

### F.16 Phòng ban TRÙNG TÊN với TPE → gắn tiền tố vào MÃ phòng

Trên DB gộp, phòng ban của mọi công ty nằm chung một bảng và **nhiều màn chỉ hiện TÊN phòng**, nên
phòng trùng tên là người dùng không biết của công ty nào. ETEK GREEN có **3 phòng trùng tên** với
TPE: "Ban Điều hành" (`BĐH` vs `BDH`), "Hội đồng quản trị" (`HĐQT` vs `HDQT`), "Phòng Kỹ thuật Công
nghệ" (`KTCN` vs `HN_KTCN`). Mã phòng thì **không trùng cái nào** — phải đo chứ đừng đoán.

Quy ước sẵn có: **8/9 công ty đã gắn tiền tố vào mã phòng** (`HN_` cty 1, `HP_` cty 2, `MT_` cty 3,
`SG_` cty 4, `TPA_` cty 5, `_TDETEK` cty 8) — cổng mới gộp vào thường là cổng DUY NHẤT chưa có tiền
tố. Mã phòng hiện trong nhãn chọn nhân viên ở **mọi select toàn hệ thống**
(`Tên NV - Mã phòng - Mã NV`, `utils/employeeOptionText.js`) nên gắn tiền tố là đủ để phân biệt.

TPE chốt 28/09/2026: **chỉ đổi MÃ, giữ nguyên TÊN phòng** (tên còn in trên quyết định/bản in), và
tiền tố **ngắn 2-3 ký tự** cho khớp `HN_`/`HP_`/`SG_` — dùng `EG_`, không dùng `ETEKGREEN_`.

```bash
php artisan company:prefix-department-code --company=9 --prefix=EG_            # thử
php artisan company:prefix-department-code --company=9 --prefix=EG_ --confirm  # thật
```
Lệnh tự bỏ qua mã đã có tiền tố (chạy lại vô hại), bỏ qua + cảnh báo nếu mã mới trùng bất kỳ phòng
nào, và **đồng bộ luôn `rice_departments.department_code`** — bản sao ĐANG DÙNG của phân hệ Cơm, khớp
theo `department_id` chứ không theo mã. Các bảng chứng từ khác chỉ lưu **ảnh chụp lịch sử**
(`department_name`/`department_code` lúc lập phiếu) → KHÔNG sửa.

Kết quả thật với ETEK GREEN: 16/16 mã đổi, 16/16 dòng `rice_departments` đồng bộ, 8 công ty còn lại
không bị đụng, API `user-profile` trả đúng `EG_*`.

⚠️ **Sau khi đổi mã**: `Modules/Payroll/ExcelImports/DepartmentImport.php` khớp phòng ban theo **MÃ**
và **KHÔNG lọc công ty**; không thấy mã là nó **TẠO phòng mới**. File Excel cũ mang mã cũ mà import
lại sẽ sinh phòng trùng → **phát lại file mẫu theo mã mới** cho người dùng.

**Bộ phận (`parts`)**: kiểm riêng. Với ETEK GREEN 66 bộ phận **0 tên trùng** nên không phải đụng —
đừng đổi cho đủ bộ.

---
### F.17 MÁY QUÉT CƠM là bảng RIÊNG — `hikvision:recode` không chạm tới

Đây là chỗ bị bỏ sót hoàn toàn khi gộp ETEK GREEN, người dùng phát hiện sau 4 ngày.

`hikvision:recode` chỉ chạy trên **`conn_infos`** (máy CHẤM CÔNG). Máy quét cơm nằm ở bảng
**`rice_conn_infos`** (màn *Cơm > Danh mục > Máy check-in*) nên **không được đổi mã**. Trong khi đó
`company:recode-unified` **có** đổi mã cơm trong DB (`employees.rice_ssn` +
`rice_employee_infos.rice_ssn` + `code`) → DB mang mã mới, máy còn mã cũ.

Đo trên prod 29/09/2026, máy cơm `14.248.82.176:4382` (1.050 người — **cùng IP với cụm máy chấm
công của TPE**, và `rice_conn_infos.company_id = 1` dù người quẹt thuộc công ty 9):

| | Trước | Sau khi sửa |
|---|---|---|
| GREEN mang mã MỚI | **1 / 133** | **99 / 133** |
| GREEN mang mã CŨ | **93** | **0** |
| Suất ghi nhận "đã ăn" 29/09 | 4/14 | 10/14, "không ăn" 6 → **0** |

**Cơ chế mất suất**: `PersonalRegistrationService::checkInMachine()` tra
`RiceEmployeeInfo::where('rice_ssn', <mã máy gửi>)`, không thấy thì `return` **lặng lẽ** — rồi cuối
ngày cron `UpdateRiceRegularNotEat` đánh luôn suất đó thành **"không ăn"** (`status_regular = 4`).
Nhân viên có quét, có ăn, mà báo cáo ghi là không ăn.

⚠️ **Nút "Đồng bộ khuôn mặt" trên màn máy check-in KHÔNG chữa được**: `riceSyncFaceForDeviceSsn()`
chỉ **đọc từ máy xuống** (tìm theo mã → tải khuôn mặt về S3 → ghi `has_face`), **không đẩy mã lên
máy**. Tìm theo mã mới không thấy nên nó còn kết luận là "chưa có khuôn mặt".

**Cách xử — 3 bước theo đúng thứ tự:**
```bash
# 1) Đổi mã trên máy cơm (giữ nguyên khuôn mặt; chỉ xoá mã cũ sau khi đọc lại OK)
php artisan rice:recode --company=9                                   # thử
php artisan rice:recode --company=9 --only-ssn=<mã cơm mới> --confirm --delete-old   # 1 người
php artisan rice:recode --company=9 --confirm --delete-old            # toàn bộ

# 2) CHẠY LẠI LẦN 2 — dọn mã cũ dạng CÓ 0 Ở ĐẦU còn sót (lượt 1 để lại 6 mã: 084 085 086 087 093 096)
php artisan rice:recode --company=9 --confirm --delete-old

# 3) Lấy bù suất bị đánh oan "không ăn" (lệnh này KHÔNG có trong cron, phải chạy tay)
php artisan rice:fetch-checkin "25/09/2026 00:00" "29/09/2026 17:00"
```
`rice:recode` dùng lại nguyên `HikvisionSyncService` qua **một `ConnInfo` tạm không lưu DB** (service
type-hint `ConnInfo`, cố ý không nới type-hint của file dùng chung).

**Mã cơm KHÁC mã chấm công** — đừng lấy `old_ssn` dùng cho cơm: Nguyễn Văn Kha có mã chấm công cũ
`43` nhưng mã cơm cũ là `30024`. Phải dùng `old_rice_ssn` / `new_rice_ssn` (bảng
`employee_code_mappings` có sẵn 2 cột này).

**Tra mã cũ ở luồng cơm KHÔNG lọc theo công ty của máy** (`app/Support/RiceCodeMapping`): máy cơm
dùng CHUNG nhiều công ty nên `rice_conn_infos.company_id` không phải công ty người quẹt. Bù lại phải
yêu cầu mã cũ khớp **duy nhất 1 dòng** — bảng có 920 dòng của 5 công ty và **1 mã cũ bị trùng**;
nhập nhằng thì thà bỏ qua còn hơn ghi nhận cho người khác.

Đã vá thêm: `checkInMachine()` và `rice:fetch-checkin` tra thêm bảng ánh xạ rồi **ghi log cảnh báo**
nếu vẫn không ra người (trước đây im lặng); `rice:fetch-checkin` còn đọc thẳng
`$riceEmployeeInfo->id` nên gặp mã lạ là **fatal, chết giữa lượt** — đã thêm guard.

Kiểm sau cùng: đọc lại danh sách user từ máy cơm (`UserInfo/Search`) và đối chiếu — phải **0 mã cũ,
kể cả dạng có 0 ở đầu**.

---
### F.18 `overtime_hours` (khung giờ làm thêm) bị để ở `skip` — sai VĨNH VIỄN, không chỉ dữ liệu cũ

Khác mọi mục trên: các lỗi kia chỉ ảnh hưởng dữ liệu ĐÃ di trú, còn lỗi này làm **mọi ngày phát
sinh SAU cutover cũng sai**, nên không tự hết.

`overtime_hours` giữ **khung giờ làm thêm + hệ số** theo công ty (vd ETEK GREEN có 3 khung:
17:00–22:00 = 1.5 ngày thường / 2.0 ngày nghỉ / 3.0 ngày lễ · 22:00–06:00 = 1.8/2.5/3.0 ·
06:00–17:00 = 0/2.0/3.0). Đây là **CẤU HÌNH theo công ty**, không phải giao dịch theo kỳ — để ở
`skip` là sai. `TimesheetSummaryService` lặp qua chính bảng này để sinh `overtime_details`; công ty
không có dòng nào thì **không bao giờ sinh được chi tiết**.

Hai hậu quả nhìn thấy trên màn *Chấm công > Báo cáo > Làm thêm giờ chi tiết*:
1. Bung dòng ra **không có khung giờ nào** (`details = []`).
2. Cột **giờ quy đổi = 0** cho toàn bộ công ty đó — ảnh hưởng tính lương làm thêm.

Đo trên prod 03/10/2026 (công ty 9): 1.317 dòng công có giờ làm thêm, **0 khung giờ**, 170 dòng
thiếu chi tiết; riêng tháng 09 là **155/155 dòng thiếu + tổng quy đổi 0,0** trong khi nguồn
`hrm_green` tháng đó có **1.475,9 giờ** quy đổi. Công ty 1/3/4 có 4–5 khung giờ, thiếu 0–1 dòng.

⚠️ **Vì sao tháng 09 ở đích mất cả giá trị đã di trú**: `calc:timesheet` của cổng TPE chạy **mỗi
giờ** và tính lại tháng hiện tại — nó ghi đè `hour_after_converting` của các dòng vừa di trú thành
**0** (vì thiếu khung giờ). Nên càng để lâu càng hỏng thêm, không phải chỉ "thiếu dữ liệu cũ".

**Cách xử:**
```bash
# 1) Catalog: overtime_hours chuyển từ 'skip' sang 'owned' (đã sửa trong repo, filter company_id=1)
php artisan company:migrate-tables --source=1 --run=etekgreen --tables=overtime_hours --dry-run
php artisan company:migrate-tables --source=1 --run=etekgreen --tables=overtime_hours

# 2) Sinh lại chi tiết cho khoảng đã hỏng — lệnh này CHỈ chạy 1 công ty
php artisan calc:company_timesheet 9 2026-09-01 2026-09-30
```
**Thời gian thật**: 1 ngày ≈ **18 giây**, cả tháng (30 ngày, 131 nhân sự công ty 9) ≈ **7 phút**.
`calc:company_timesheet {company_id} {from} {to}` **chỉ tính công ty được truyền vào** — đã kiểm
chứng: công ty 1 (227 dòng / 1.920,6 h) và công ty 4 (74 dòng / 704,9 h) không đổi.

**Kết quả tháng 09 công ty 9**: giờ làm thêm **958,6 h giữ nguyên**; quy đổi **0,0 → 1.719,3 h**;
thiếu chi tiết **155 → 9**. 9 dòng còn lại khớp đúng 12 dòng quy đổi = 0 ở NGUỒN (không có phiếu
phân công hoặc không có lượt quẹt trong khung) → đúng nghiệp vụ, không phải lỗi.

**Tự kiểm — tìm MỌI công ty bị lỗi này trong 1 câu:**
```sql
SELECT ei.company_id, COUNT(*) dong_co_OT,
       (SELECT COUNT(*) FROM overtime_hours oh WHERE oh.company_id=ei.company_id) so_khung_gio,
       SUM(NOT EXISTS(SELECT 1 FROM overtime_details od WHERE od.timesheet_summary_id=ts.id)) thieu
FROM timesheet_summaries ts JOIN employee_infos ei ON ei.id=ts.employee_info_id
WHERE ts.overtime_hour>0 AND ts.day>='2026-01-01' GROUP BY ei.company_id;
```
`so_khung_gio = 0` mà `dong_co_OT > 0` là đang bị lỗi này.

**Bài học chung**: trước khi chạy cổng mới, rà lại danh sách `skip` và tách rõ **CẤU HÌNH theo công
ty** (phải đưa) với **giao dịch theo kỳ** (bỏ được). Bảng cấu hình bị bỏ sót thì không chỉ thiếu dữ
liệu cũ — nó làm tính toán sai mãi mãi.

---
### F.15 Riêng cho cổng KẾ TIẾP — etekpower (khảo sát 25/09/2026, **chưa chạy gì**)

| | |
|---|---|
| DB nguồn | `hrm_power` @ `192.168.122.103:3306`, user `hrm_power` |
| Quy mô | **80 hồ sơ NV / 80 tài khoản**, 18 phòng ban, 6 bộ phận, **2 máy chấm công**, 26.513 dòng phân ca, 57.844 lượt chấm |
| Cơm | tenant `parent_id = 3`, có **2 rice_companies**: id 3 (`ETEK POWER`, company_id 1, đang bật) và id 8 (`Tân Phát 686 tmp`, company_id 2, `status = 0`) |
| Cron | 10 dòng trong `crontab -l` của `erp_tpe`, lọc theo `/var/www/etekpower/` |
| Supervisor | 3 program: `etekpower-worker`, `etekpower-rice_notifications`, `etekpower_sync_faces-worker` |

**Lưu ý riêng của cổng này:**
1. **Tenant cơm có 2 công ty con, không phải 1** → `company:relink-rice --rice-parent=3` phải xử cả
   id 3 và id 8. Đừng giả định 1 cổng = 1 rice_company như ETEK GREEN.
2. `company_id` trong DB nguồn của etekpower là **1** (mỗi cổng tự đánh số từ 1) — trùng số với TPE
   ở DB đích. Luôn truyền `--source=1` (id ở NGUỒN) và `--new-company=<id mới>` cho rõ.
3. **`.env` của cổng TPE đang có `DB_*_TARGET` trỏ `hrm_power`** (connection `mysql_target`, dùng bởi
   `assign:sync-assign-catalogs` đẩy danh mục Giao việc sang etekpower). Gộp xong thì khối đó **hết
   ý nghĩa** → rà lại, đừng để đẩy danh mục sang một DB không ai dùng.
4. `RICE_REGISTER_DOMAINS` của cổng `tpe` và `etek` đang còn `http://hrm.etekpower.com.vn` → sau khi
   hạ cổng etekpower phải bỏ ở **cả hai** (xem F.10; chính cổng etekpower thì không cần quan tâm nữa).
5. **2 máy chấm công** → phải làm đủ F.6 + F.7 cho cả hai, và nhớ `--conn=<2 id máy>` khi lấy bù.
6. Phân ca 26.513 dòng: quyết trước xem có bù kỳ cũ hay không (F.9), và nếu bù thì lấy **cùng mốc**
   với `timesheet_summaries` của công ty đó.
