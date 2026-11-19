# Hướng dẫn chạy trên VPS — Kế thừa giá theo hãng ĐỢT 2 (hệ số kế thừa + Lưu chạy nền)

> Soạn 30/10/2026 · @namdangit · bản **gõ lệnh từng bước** (copy–paste). Giải thích + lý do: `deploy.md` mục "ĐỢT 2".
> Code đã push `gop_db` 30/10: hrm-api **`27384672c`** · hrm-client **`7e127ac53`**. ERP KHÔNG đổi.
> Đợt 2 KHÔNG có quyền mới, KHÔNG sửa dữ liệu cũ, KHÔNG đổi `.env`. Deploy xong giá **không tự đổi** — chỉ đổi khi có người bấm Lưu.
>
> ⚠️ **Pull `gop_db` kéo theo việc của người khác** (tính từ tip 26/10 `4ce76d0df`: +184 commit api, +122 commit client — có merge
> `develop`): 14 migration khác, ~30 quyền mới, 2 lịch cron mới (`assign:send-work-reminders` 5 phút/lần, `assign:send-work-digest`
> 07:30). Đợt 2 KHÔNG tách riêng được (code mới cần cột/bảng mới của họ). ⇒ **Trước giờ G phải có người phụ trách từng phần
> đó đồng ý lên prod** (bước 1 in đúng danh sách theo prod thật). Thiếu đồng ý ⇒ DỪNG, không deploy nửa vời.
>
> ✅ **Cập nhật 30/10 (kiểm trên prod):** prod đã đứng sẵn ở `e0f6e694f` (api) / `8a5304470` (client) = đúng commit cha của đợt 2
> ⇒ `HEAD..origin/gop_db` = **1 commit** mỗi repo, chỉ có đợt 2. Cảnh báo kéo theo việc người khác ở trên KHÔNG còn áp dụng:
> không composer.lock, không PermissionsTableSeeder, không Kernel.php, không package.json — chỉ 2 migration đợt 2.
>
> Quy ước: dòng `# KỲ VỌNG` là kết quả phải thấy. Lệch ⇒ **DỪNG**, chụp màn hình gửi dev, không làm tiếp.

---

## 0. Đăng nhập + biến (mở 1 phiên, dùng suốt)

```bash
ssh -p 2225 erp_tpe@124.158.4.24
export API=/var/www/tpe/hrm-api
export CLI=/var/www/tpe/hrm-client
alias M='mysql -h 192.168.122.103 -u hrm_tpe -p --table hrm_erp_gop'
# artisan chạy bằng user erp_tpe (đang đăng nhập) ⇒ gọi thẳng php artisan, KHÔNG sudo -u www-data
# CHỈ đụng bộ /var/www/tpe — máy có 5 bộ HRM (etekpower · tpe · etek · etekgreen · toyota)
```

## 1. Kiểm trước — CHỈ ĐỌC (làm trước giờ G, gửi kết quả cho dev)

```bash
cd $API && git status -sb | head -1 && git log --oneline -1          # ghi lại: HASH_API_CU = ________
cd $CLI && git status -sb | head -1 && git log --oneline -1          # ghi lại: HASH_CLI_CU = ________
# KỲ VỌNG: "## gop_db...origin/gop_db", KHÔNG có file sửa tay (git status --short rỗng)

cd $API && git fetch origin
git log --oneline HEAD..origin/gop_db | wc -l                        # số commit sẽ kéo về
git diff --name-only --diff-filter=A HEAD origin/gop_db | grep -i migrations/    # migration MỚI sẽ kéo về
git diff --stat HEAD origin/gop_db -- composer.lock Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php app/Console/Kernel.php
php artisan migrate:status | grep "| No"                             # đang chờ TRƯỚC khi pull (thường rỗng)

cd $CLI && git fetch origin && git diff --stat HEAD origin/gop_db -- package.json package-lock.json nuxt.config.js

which supervisorctl && sudo supervisorctl status                     # có supervisor không, đang chạy gì
ps aux | grep "queue:work" | grep -v grep                            # đã có worker nào chưa
php -v | head -1                                                     # KỲ VỌNG: PHP 7.4.x
M -e "SELECT COUNT(*) FROM jobs; SELECT COUNT(*) FROM failed_jobs;"  # KỲ VỌNG: 2 bảng có sẵn (ghi lại số)
```
- Danh sách migration ở lệnh thứ 4 **phải có** `2026_10_29_000001_create_manufacture_price_mode_runs_table` và
  `2026_10_29_000002_create_inherited_price_factors_table` (của đợt này). Bản KHÁC ⇒ ghi tên, hỏi người phụ trách trước giờ G.
- `composer.lock` có đổi ⇒ thêm `composer install --no-dev --optimize-autoloader` ở bước 3.
- Không có `supervisorctl` ⇒ bước 6 dùng **Phương án B (cron)**.

## 2. Sao lưu DB (≈ 5 phút, 12 GB)

```bash
df -h ~                                                              # KỲ VỌNG: trống ≥ 3 GB (file nén ~1 GB)
F=~/backup_hrm_erp_gop_$(date +%F_%H%M).sql.gz
mysqldump -h 192.168.122.103 -u hrm_tpe -p --single-transaction --quick --routines --triggers --no-tablespaces \
  --set-gtid-purged=OFF hrm_erp_gop | gzip > $F
ls -lh $F                                                            # KỲ VỌNG: ~1 GB (20/10: 986 MB)
gzip -t $F && zcat $F | tail -1                                      # KỲ VỌNG: "-- Dump completed on …"
echo $F                                                              # ghi lại tên file
```

## 3. Kéo code

```bash
cd $API && git pull origin gop_db && git log --oneline -1
# KỲ VỌNG: 27384672c (hoặc mới hơn nếu có người push thêm — khi đó báo dev xem lại bước 1)
# composer.lock đổi ở bước 1 thì chạy thêm: composer install --no-dev --optimize-autoloader
cd $CLI && git pull origin gop_db && git log --oneline -1
# KỲ VỌNG: 7e127ac53
```

## 4. Migration — chạy LẺ từng bản

```bash
cd $API
php artisan migrate:status | grep "| No"
# KỲ VỌNG: đúng danh sách đã duyệt ở bước 1 (2 bản đợt 2 + các bản người khác đã đồng ý)
```
**4a. 2 bản của đợt 2** (chỉ CREATE TABLE rỗng, không đụng bảng cũ):
```bash
php artisan migrate --force --pretend --path=Modules/MasterData/Database/Migrations/2026_10_29_000001_create_manufacture_price_mode_runs_table.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_29_000001_create_manufacture_price_mode_runs_table.php
php artisan migrate --force --pretend --path=Modules/MasterData/Database/Migrations/2026_10_29_000002_create_inherited_price_factors_table.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_29_000002_create_inherited_price_factors_table.php
php artisan migrate:status | grep 2026_10_29_00000[12]_create      # KỲ VỌNG: 2 dòng "Yes"
```
**4b. Bản của người khác** — theo đúng danh sách + thứ tự người phụ trách đưa, mỗi bản `--pretend` rồi chạy bằng `--path`.
KHÔNG chạy `php artisan migrate` trần (kéo theo cả bản chưa duyệt).
```bash
php artisan migrate:status | grep "| No"                            # KỲ VỌNG: rỗng
```

## 5. Quyền (chỉ khi bước 1 thấy PermissionsTableSeeder đổi — đợt 2 KHÔNG có quyền mới)

```bash
cd $API && php artisan permission:sync --dry-run
# Đối chiếu từng dòng "thêm/sửa/đổi tên/gỡ" với người phụ trách. Đúng hết mới chạy:
php artisan permission:sync
php artisan permission:sync --dry-run                               # KỲ VỌNG: thêm 0 · sửa 0 · đổi tên 0 · gỡ 0
```

## 6. Worker chạy nền — BẮT BUỘC cho đợt 2

> Thiếu worker ⇒ bấm Lưu kẹt dải "Đang áp", 30 phút sau tự báo lỗi, giá không đổi. Chỉ chạy **1 tiến trình**.
> `.env` KHÔNG đổi `QUEUE_CONNECTION` — Job đợt 2 tự dùng connection `database`, queue riêng `price-inherit`.

**Phương án A — có supervisor (khuyến nghị; prod TPE dùng cách này 30/10):**
> Theo đúng khuôn `/etc/supervisor/conf.d/tpe-worker.conf` có sẵn trên prod: `user=root`, log ở `/var/log/laravel/`.
> KHÔNG dùng `user=erp_tpe`: worker khác chạy root ⇒ file `laravel-<ngày>.log` có thể do root tạo, erp_tpe ghi không được ⇒ job lỗi.
```bash
sudo tee /etc/supervisor/conf.d/tpe-price-inherit.conf >/dev/null <<'EOF'
[program:tpe-price-inherit]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/tpe/hrm-api/artisan queue:work database --queue=price-inherit --sleep=3 --tries=1 --timeout=900 --max-time=3600
startsecs=0
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=root
numprocs=1
redirect_stderr=true
stdout_logfile=/var/log/laravel/price-inherit-worker.log
stopwaitsecs=960
EOF
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl status | grep price-inherit                      # KỲ VỌNG: tpe-price-inherit:tpe-price-inherit_00 RUNNING
```
- `--timeout=900` < `stopwaitsecs=960`: dừng worker thì job đang áp được chạy nốt. `--max-time=3600`: 1 giờ tự khởi động lại.
- Log worker: `/var/log/laravel/price-inherit-worker.log`.

**Phương án B — không có supervisor:** `crontab -e` (user erp_tpe), thêm 1 dòng:
```cron
* * * * * cd /var/www/tpe/hrm-api && flock -n /tmp/hrm-tpe-price-inherit.lock php artisan queue:work database --queue=price-inherit --stop-when-empty --timeout=900 --tries=1 >> storage/logs/price-inherit-worker.log 2>&1
```
```bash
crontab -l | grep -n "price-inherit\|schedule:run"                  # KỲ VỌNG: 2 dòng (schedule:run có sẵn + dòng mới)
```
Bấm Lưu chờ tối đa ~1 phút mới bắt đầu áp.

## 7. Cache + khởi động lại

```bash
cd $API
php artisan config:clear && php artisan route:clear
php artisan route:cache                                              # prod hrm-api BẬT route cache từ 25/09 — clear xong phải cache lại
php artisan cache:clear                                              # chỉ cần khi bước 5 có sync quyền (cache quyền 24h)
sudo systemctl reload php7.4-fpm                                     # bộ tpe dùng php7.4-fpm.sock (kiểm 30/10); máy có cả 8.3
php artisan queue:restart                                            # worker nạp code mới — MỌI lần deploy api sau này đều chạy
cd $CLI && npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build      # node 12, ~5–10 phút
sudo /etc/init.d/hrm-client-tpe start                                # KHÔNG pm2 restart trần (socket ⇒ 502)
curl -s -o /dev/null -w "%{http_code}\n" https://hrm.eteksofts.com/   # KỲ VỌNG: 200
```

## 8. Kiểm khói (10 phút — tài khoản có quyền "Cài đặt giá bán theo hãng")

1. Tài chính › Giá bán theo hãng sx:
   - 2 lựa chọn tên mới: "Tự xây dựng giá bán riêng theo công ty" / "Kế thừa giá bán theo công ty quản lý hàng".
   - Hướng dẫn ẩn (bấm mới mở) · khối "Khai báo ngoại lệ" 3 tab.
   - Công ty đã cài từ đợt 1 (vd TPHP) vẫn đúng cách cài + đúng danh sách hãng cũ.
2. Thử Lưu ở 1 công ty ÍT hàng (thêm 1 hãng không có mã rồi Lưu; xong bỏ hãng đó, Lưu lại):
   - dải "Đang áp cài đặt…" hiện ⇒ vài giây (B: ≤ 1 phút) tự tắt ⇒ chuông "[GIA] Cập nhật: …".
   ```bash
   M -e "SELECT id, company_id, status, total, done, summary, error, created_at, finished_at FROM manufacture_price_mode_runs ORDER BY id DESC LIMIT 3;"
   # KỲ VỌNG: status 3 (Đã áp). Kẹt 1 quá 1 phút ⇒ worker chưa chạy (bước 6) · status 4 ⇒ đọc cột error + log dưới
   sudo tail -50 /var/log/laravel/price-inherit-worker.log; tail -50 $API/storage/logs/laravel-$(date +%F).log
   ```
3. So khớp (chỉ đọc):
   ```bash
   cd $API && php artisan product-price:compare-inherited --company=TPSG,TPHP,TPV
   # KỲ VỌNG: "0 lệch." Còn lệch ⇒ thêm --csv=/tmp/lech.csv gửi dev, KHÔNG sửa tay giá
   ```
4. Màn Cập nhật giá bán ở công ty kế thừa: hàng kế thừa vẫn khoá, nhãn "Kế thừa · TPE" (chưa khai hệ số thì không có "× k").
5. Phần của người khác kéo theo (bước 1): nhờ người phụ trách tự kiểm màn của họ.

## 9. Khai hệ số / lưu lớn lần đầu (khi nghiệp vụ sẵn sàng — không cần cùng lúc deploy)

1. Sao lưu riêng bảng giá (điểm lui cho GIÁ):
   ```bash
   mysqldump -h 192.168.122.103 -u hrm_tpe -p --single-transaction hrm_erp_gop \
     product_unit_prices product_expected_prices product_approves product_approve_prices product_company_units \
     | gzip > ~/backup-gia-truoc-he-so-$(date +%Y%m%d-%H%M).sql.gz
   ```
2. Chụp giá TRƯỚC → bấm Lưu → chờ dải "Đang áp" tắt → chụp giá SAU → ra Excel giá cũ / giá mới (mỗi công ty 1 tab):
   làm theo **`kiem-gia/README.md`** (chép `chup-gia.sql` lên VPS 1 lần).
3. Chạy lại bước 8.3.

---

## LUI (nếu lỗi sau deploy)

1. Dừng worker: A `sudo supervisorctl stop tpe-price-inherit:*` · B xoá dòng cron `price-inherit`.
2. Code về bản cũ (hash ghi ở bước 1):
   ```bash
   cd $API && git checkout <HASH_API_CU> && php artisan config:clear && php artisan route:clear && sudo systemctl reload php*-fpm
   cd $CLI && git checkout <HASH_CLI_CU> && npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build && sudo /etc/init.d/hrm-client-tpe start
   ```
3. 2 bảng mới của đợt 2 để nguyên vô hại. Migration của người khác: hỏi người phụ trách trước khi rollback (có bản sửa dữ liệu).
4. Giá đã áp theo hệ số đã ghi đè — lui code KHÔNG trả giá cũ. Muốn trả: nạp lại bản sao lưu bước 9.1 **cùng dev**, không tự nạp cả bảng.
5. Hỏng nặng cả hệ thống: nạp lại bản sao lưu toàn DB ở bước 2 — chỉ làm khi dev xác nhận.
