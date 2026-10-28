# Hướng dẫn chạy trên VPS production — Chuyển đổi hàng hoá — 20/10/2026

> Bản **gõ lệnh từng bước** (copy–paste). Giải thích, số đo, lý do từng bước: `TRIEN-KHAI-PROD-2010.md`.
> Đã chạy tập trọn trên bản sao prod `hrm_erp_20_10` (20/10) — cột **"Kỳ vọng"** là số thật của bản sao đó; prod thật lệch NHẸ (dữ liệu
> phát sinh sau lúc dump) là bình thường, lệch XA ⇒ **DỪNG**, không làm tiếp, báo dev.
> Code đã push: `gop_db` = nhánh chung — hrm-api `c4d835b49` · hrm-client `37f3e0ef6` · ERP `5bdd056d4e`.

## ✅ ĐÃ CHẠY TRÊN PROD 20/10/2026 (~21:30–23:20) — mọi điểm dừng đạt, số khớp bản chạy tập
Thực tế VPS (dùng cho lần sau): HRM `erp_tpe@hrm-tpe` (SSH -p 2225 124.158.4.24) — bộ **`/var/www/tpe`** (máy có 5 bộ HRM: etekpower · tpe · etek ·
etekgreen · toyota — CHỈ đụng tpe); MySQL ở **192.168.122.103**, DB `hrm_erp_gop`, user `hrm_tpe`; artisan chạy bằng **`erp_tpe`** (storage thuộc erp_tpe,
KHÔNG `sudo -u www-data`); remote git `minhth1905/hrm-*` = cùng repo `DNS-Media/hrm-*`. ERP ở VPS riêng `erp_tpe@erptpe` `/var/www/html/TanPhatDev`,
PHP chạy trong **Apache** (`sudo systemctl reload apache2`, không có php-fpm), prod dùng `config:cache`. Client: pm2 của **root** tên `hrm-client-tpe`,
nghe unix socket `/var/run/hrm-client-tpe.sock` ⇒ khởi động lại bằng **`sudo /etc/init.d/hrm-client-tpe start`** (chờ socket + quyền); `pm2 restart` trần ⇒ 502.
Đã thêm `HRM_API_BASE_URL=https://hrm.eteksofts.com` vào `.env` ERP (trước đó thiếu). Sao lưu: `~/backup_hrm_erp_gop_2026-10-20_2157.sql.gz` (986 MB, 1.878 bảng)
trên VPS HRM; CSV dọn giá ERP `storage/app/price-cleanup/20261020-225503`. N26 đo lại với `information_schema_stats_expiry = 0` (số cũ trong cache báo nhầm B < A).
Cron HRM: crontab user `erp_tpe` dòng 35 — apply-expected lần đầu 21/10 01:00.

## 0. Chuẩn bị (máy dev, trước giờ G)

1. Chép gói SQL lên VPS (thư mục `.plans` không nằm trong git):
   ```bash
   scp HRM/.plans/gop-db/quan-ly-hang-hoa/catalog-import/golive-2010/golive-2010-sql.tar.gz <user>@<vps>:/tmp/
   ```
2. **Người chạy = `employees.id` 13 (DNS Admin)** — user chốt 20/10. Đã điền SẴN `SET @nguoi_chay = 13;` trong 3 file SQL của gói (phiếu chéo · cây · catalog) + `--by=13` ở close-stale.

## 1. Khai báo biến (VPS — mở 1 phiên shell, dùng suốt)

```bash
export ERP=/đường/dẫn/ERP            # thư mục code ERP
export API=/đường/dẫn/hrm-api        # thư mục hrm-api
export CLI=/đường/dẫn/hrm-client     # thư mục hrm-client
export DB=<tên DB production>
export NGUOI_CHAY=13                            # DNS Admin
export PM2_CLI=hrm-client-tpe                   # sudo pm2 list (pm2 của root)
export A="sudo -u www-data php"                 # artisan chạy bằng user web (storage/log thuộc www-data)
export SQLDIR=/tmp/golive-2010-sql
alias M='mysql -h <host> -u <user> -p --table $DB'   # MySQL client (sql_mode strict, dừng ở lỗi đầu tiên)

cd /tmp && tar xzf golive-2010-sql.tar.gz && cd $SQLDIR && sha256sum -c SHA256SUMS     # 5 dòng OK
grep -H "^SET @nguoi_chay" $SQLDIR/*.sql      # 3 file đều "SET @nguoi_chay = 13;"
M -e "SELECT id, email FROM employees WHERE id = 13;"   # phải ra namdangit@gmail.com (DNS Admin)
```

## 2. Kiểm trước (app vẫn chạy — chỉ đọc)

```bash
df -h                                                   # trống ≥ 2 × DB (~12 GB)
sudo crontab -l; sudo crontab -u www-data -l            # giờ job backup KHÔNG trùng cửa sổ
M -e "SELECT COUNT(*) cheo_do FROM price_asking_requests a WHERE a.status IN (1,2,5,7) AND a.send_company_id IS NOT NULL AND a.company_id<>a.send_company_id;
      SELECT COUNT(*) tam_cho_duyet FROM tmp_products WHERE status=2;
      SELECT COUNT(*) kq_trung FROM (SELECT price_calculate_id FROM price_calculate_results GROUP BY 1 HAVING COUNT(*)>1) x;"
```
| Kiểm | Kỳ vọng | Ghi chú |
|---|---|---|
| `cheo_do` | ≈ 36 | xử lý ở bước 8.4 |
| `tam_cho_duyet` | 0 | ≠ 0 ⇒ duyệt / từ chối nốt ở ERP |
| `kq_trung` | ≈ 2 | xử lý ở bước 3.5 |

## 3. Đóng app + sao lưu + code

```bash
# 3.1 đóng app (giữ MySQL + cron)
cd $ERP && $A artisan down --message="Đang nâng cấp hệ thống" --allow=<IP dev>
cd $API && $A artisan down --secret="<chuoi-bi-mat>"
pm2 stop $PM2_CLI

# 3.2 sao lưu — ĐIỂM LUI DUY NHẤT
mysqldump -h <host> -u <user> -p --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF $DB \
  | gzip > ~/backup_${DB}_$(date +%F_%H%M).sql.gz
zcat ~/backup_${DB}_*.sql.gz | tail -1            # PHẢI: -- Dump completed

# 3.3 code (3 repo đều nhánh gop_db)
cd $ERP && git fetch origin && git checkout gop_db && git pull && git rev-parse --short HEAD   # 5bdd056d4e
composer install --no-dev -o
cd $API && git fetch origin && git checkout gop_db && git pull && git rev-parse --short HEAD   # c4d835b49
composer install --no-dev -o
cd $CLI && git fetch origin && git checkout gop_db && git pull && git rev-parse --short HEAD   # 37f3e0ef6
```
**3.4 `.env` ERP** — thêm/kiểm: `HRM_URL_FE` · `HRM_URL_BE` · `HRM_API_BASE_URL` (url HRM) · `IS_USE_SSO=true` (giữ) · `JWT_SECRET` **giống HRM**.
```bash
cd $ERP && $A artisan config:clear && $A artisan route:clear && $A artisan view:clear
cd $API && $A artisan config:clear && $A artisan route:clear
cd $API && $A artisan tinker --execute="echo DB::connection()->getDatabaseName();"     # PHẢI = $DB
cd $ERP && $A artisan tinker --execute="echo DB::connection()->getDatabaseName();"     # PHẢI = $DB
sudo systemctl reload php*-fpm                                                          # nạp code mới (opcache)
grep -n "product:update_price" $ERP/app/Console/Kernel.php                              # chỉ còn dòng chú thích
```
**3.5 Dọn KQ tính giá trùng (TRƯỚC migration):**
```bash
M < $SQLDIR/0_kq_tinh_gia_trung_2010.sql
```
Kỳ vọng: liệt kê PTG-03422 / PTG-03425 · `kq 2 · sp 13 · gia 78 · du_kien 13` · dòng cuối **`ptg_con_trung_PHAI_0 = 0`**.

## 4. Migration lượt 1 — PHẢI DỪNG Ở M3

```bash
cd $API && $A artisan migrate:status | grep "| No" | wc -l      # 32
$A artisan migrate --force
```
Kỳ vọng: chạy 9 bản rồi **báo lỗi** `2026_10_09_000004_enforce_company_id…`: "còn ~275772 dòng company_id NULL… Không có thay đổi nào được áp" ⇒ **ĐÚNG**.
Không báo lỗi ⇒ **DỪNG**.
```bash
cd $ERP && $A artisan migrate:status | grep "| No"               # ERP: thường rỗng; có ⇒ chạy lẻ --path từng file
```

## 5. Backfill giá theo công ty

```bash
cd $API
$A -d memory_limit=4G artisan product-price:backfill-company --dry-run
```
Kỳ vọng: `B0 kiểm trước: {"orphan_upp":0,"owner_unknown":0,"duplicates":0,"pcu_foreign":0}` · **TỔNG GHI ≈ 1.057.680**
(Cty 1 ≈ 344.949 · 2 ≈ 232.141 · 3 ≈ 232.141 · 4 ≈ 232.576 · 8 ≈ 7 · 9 ≈ 15.866). B0 ≠ 0 ⇒ **DỪNG**.
```bash
$A -d memory_limit=4G artisan product-price:backfill-company          # ~1 phút
$A -d memory_limit=4G artisan product-price:compare --csv=/tmp/compare.csv
```
Kỳ vọng: bảng = dry-run · **"B6 kiểm sau: đạt"** · compare dòng cuối **`0 lệch.`** (≈ 115.199 cặp). ≠ 0 lệch ⇒ **DỪNG**, gửi `/tmp/compare.csv`.

## 6. Migration lượt 2 + seeder

```bash
$A artisan migrate --force                          # 23 bản, ~25 s
$A artisan migrate:status | grep -c "| No"          # 0
$A artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder" --force
```

## 7. Quyền

```bash
$A artisan permission:sync --dry-run      # kỳ vọng: "thêm 30 · sửa 0 · đổi tên 0 · gỡ 0 · gộp trùng 0 · … · không khai báo 0"
$A artisan permission:sync
$A artisan permission:sync --dry-run      # "thêm 0 … 0"
$A artisan permission:cache-reset
```
Dry-run có "tên đã có ở id khác" / lỗi / "không khai báo" ≠ 0 ⇒ **DỪNG**.

## 8. Luồng tính giá + dữ liệu cũ ERP

```bash
# 8.1 nhóm YCHG
$A artisan price-asking:backfill-groups --dry-run       # "Phiếu xử lý = nhóm sinh ra" ≈ 4.404
$A artisan price-asking:backfill-groups
$A artisan price-asking:backfill-groups --dry-run       # mọi dòng 0
# 8.2 đóng nhóm cũ trước 01/06
$A artisan price-asking:close-stale --before=2026-06-01 --dry-run      # "Nhóm đóng" ≈ 45 · "CHƯA backfill" = 0
$A artisan price-asking:close-stale --before=2026-06-01 --by=$NGUOI_CHAY
$A artisan price-asking:close-stale --before=2026-06-01 --dry-run      # 0
# 8.3 N26 (chỉ đọc)
M -e "SELECT (SELECT MAX(product_version_id) FROM product_histories) A,
      (SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name='product_versions') B;"
#   bản sao: A 177200 < B 177201 ⇒ không làm gì. CHỈ KHI B <= A: M -e "ALTER TABLE product_versions AUTO_INCREMENT = <A+1>;"
# 8.4 đóng YCHG chéo công ty còn dở
M < $SQLDIR/8_dong_phieu_hoi_cheo_2010.sql          # @nguoi_chay = 13 đã điền sẵn
```
Kỳ vọng 8.4: `ok_PHAI_1 = 1` · `nhom_se_dong ≈ 28` · câu kiểm cuối **rỗng** (0 phiếu chéo còn dở).
```bash
# 8.5 ERP dọn giá hiệu lực quá hạn
cd $ERP
$A artisan price:cleanup-stale --dry-run      # ≈ 13.953 quá hạn (2026 ≈ 2.105) · cờ mồ côi 5 / 6 / 6 · ghi ra storage/app/price-cleanup/…
$A artisan price:cleanup-stale
$A artisan price:cleanup-stale --dry-run      # mọi nhóm 0
M -e "SELECT upp.company_id, COUNT(*) FROM product_expected_prices pep JOIN product_unit_prices upp ON upp.id=pep.unit_price_id
      WHERE pep.status=2 AND (pep.flag<>1 OR pep.flag IS NULL) AND pep.effect_date < CURDATE() - INTERVAL 30 DAY GROUP BY 1;"   # RỖNG
```

## 9. Dữ liệu hàng hoá (thứ tự BẮT BUỘC 9.1 → 9.2 → 9.3)

```bash
# 9.1 cây phân loại 4 cấp — THAY cây cũ (prod có cây nhập 15/10, cùng dãy mã khác tên)
M < $SQLDIR/cay_4_cap_2010.sql
```
Kỳ vọng: K0 `6 · 48 · 270 · 959` · **`hang_va_thuoc_tinh_dang_dung_cay_PHAI_0 = 0` · `ok_PHAI_1 = 1` · `se_thay_cay_cu = 1`** ·
sao lưu 959 Loại cũ · K1 rỗng · K2 `0 · 0 · 0 · 0` · tổng `6 · 48 · 282 · 968` · TCHH.0005 `is_auto_parts = 1`. `ok = 0` ⇒ **DỪNG** (không đổi gì).
```bash
# 9.2 gán Loại SP, VAT, tồn lâu, thuộc tính
M < $SQLDIR/golive_bo_nhom_2010.sql
```
Kỳ vọng: `loai_lsp_phai_968 = 968` · câu "mã Loại không có trên DB" **rỗng** · `hang_dang_dung_co_loai_sau ≈ 11.959` ·
`hang_dang_dung_vat_null_sau ≈ 17` · `loai_ton_lau_180 = 968` · `thuoc_tinh_loai_sau ≈ 957, so_loai ≈ 234`.
```bash
# 9.3 catalog Dịch vụ ô tô cho Cty 1·2·3·4
M < $SQLDIR/catalog_dich_vu_o_to_2010.sql          # @nguoi_chay = 13 đã điền sẵn
```
Kỳ vọng: C0 ra `7 · LVCTKD.0007 · Dịch vụ ô tô · 1` (mã khác ⇒ sửa dòng `SET @scope_code` rồi chạy lại) · **`ok_PHAI_1 = 1`** ·
tạo thêm ≈ 14 Tiểu mục · "đường không ra Tiểu mục" **rỗng** · C5 ≈ 32 dòng "không có mã trên DB" · cuối: mỗi Cty 1·2·3·4 ≈ **814** liên kết.

## 10. Mở lại

```bash
cd $CLI && npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build      # node 12
cd $API && $A artisan queue:restart && $A artisan up
cd $ERP && $A artisan config:clear && $A artisan route:clear && $A artisan view:clear
#   prod vốn dùng config cache thì thêm: $A artisan config:cache   (cả ERP + API)
cd $ERP && $A artisan up
sudo /etc/init.d/hrm-client-tpe start         # KHÔNG pm2 restart trần (socket ⇒ 502)
sudo crontab -u www-data -l | grep schedule:run                 # có dòng trỏ $API (thiếu thì thêm: * * * * * cd $API && php artisan schedule:run >> /dev/null 2>&1)
cd $API && $A artisan schedule:list | grep apply-expected       # 0 1 * * *
```
⚠️ **KHÔNG** bật lại `product:update_price` ở ERP.

## 11. Kiểm khói (15 phút) — chi tiết `TRIEN-KHAI-PROD-2010.md` bước 12
HRM: `/master-data/products/company` (1 hàng có Loại SP) · `/finance/product-prices` (Cty 1·2·3·4 có giá) · Nhật ký áp giá · `/sale/price-asking-requests` ·
`/master-data/products/temp` · danh mục Loại SP = 968 · Chương lĩnh vực Dịch vụ ô tô. ERP: trang "Chức năng đã chuyển sang HRM" ở hàng hoá / giá / hỏi giá /
hàng tạm · popup chọn hàng báo giá ra giá đúng công ty · trang chủ không còn 3 thẻ hỏi / tính giá.

## 12. Sau khi mở (cùng tối)
- Gán quyền theo `TRIEN-KHAI-PROD-2010.md` bước 11 (danh mục xe 2c cho 8 người đang dùng · PTKD thêm "Xây dựng thông tin hàng hoá" · bảng §B10) ⇒ `$A artisan permission:cache-reset`.
- Nhập danh mục **Đặc tính sản phẩm** (đang 0 ⇒ không tạo được hàng tạm) · phân công XNK Cty 2/5/6/7/8.
- Gửi nghiệp vụ `golive-2010/ds-gui-nghiep-vu-prod-2010.xlsx` + `gia-qua-han-<năm>.csv`; soát giá chờ ≤ 1 đ trước 01:00.
- Sáng 21/10: Nhật ký áp giá + chuông thông báo.

## LUI (điểm dừng hỏng, không sửa được trong cửa sổ)
```bash
cd $ERP && $A artisan down; cd $API && $A artisan down; pm2 stop $PM2_CLI
gunzip < ~/backup_${DB}_<giờ>.sql.gz | mysql -h <host> -u <user> -p $DB
# checkout commit TRƯỚC đợt ở CẢ 3 repo (gop_db cũ): hrm-api f808edbeb · hrm-client 79d642ab9 · ERP 4009791fa8
#   rồi composer install / npm ci + build / reload php-fpm; ERP bật lại lịch product:update_price (code cũ)
cd $ERP && $A artisan up; cd $API && $A artisan up; pm2 restart $PM2_CLI
```
Luôn lui CẢ HAI app. Dữ liệu ghi sau lúc mở lại sẽ mất khi khôi phục.
