# Hướng dẫn deploy — Kế thừa giá bán theo hãng sx (prod Tân Phát)

> Soạn 26/10/2026 · @namdangit · nhánh `gop_db` · chỉ **hrm-api + hrm-client**, ERP KHÔNG đổi.
> Hạ tầng prod: xem `../HUONG-DAN-VPS-PROD-2010.md` (VPS `ssh -p 2225 erp_tpe@124.158.4.24`, bộ Tân Phát `/var/www/tpe`,
> MySQL `192.168.122.103` DB `hrm_erp_gop`, client pm2 root `hrm-client-tpe`).

## Code đi kèm

| Repo | Commit | Nội dung |
|---|---|---|
| hrm-api | `7c943033c` (24/10) | Kế thừa giá + tách YCHG sang công ty quản lý — **2 migration + 1 quyền** |
| hrm-api | `326374069` (26/10) | Lệnh so khớp `product-price:compare-inherited` + preview trả số yêu cầu duyệt giá bị huỷ |
| hrm-client | `1ab0006b6` (24/10) | Màn Tài chính › Giá bán theo hãng sx, nút Chuyển KD kế thừa, YCHG tách phiếu |
| hrm-client | `094e72fc6` (26/10) | Hướng dẫn + cảnh báo khi lưu |

Pull `gop_db` cũng kéo theo (feature khác, không migration/quyền): khoá Hãng SX / Model / Code đặt hàng ở form Sửa hàng hoá —
api `38c7f68e5` · client `cdbdc223b` — và vá bảo mật api `4ce76d0df`.

Commit TRƯỚC feature (điểm lui code): hrm-api `17f76d1f9` · hrm-client `3940e0c1b`.

**Deploy xong mà chưa ai lưu cài đặt ⇒ hành vi giá KHÔNG đổi** (chưa cài = "Chọn hãng kế thừa" + danh sách rỗng = mọi hãng tự
xây dựng giá như cũ). Giá chỉ đổi khi một công ty bấm Lưu ở màn cài đặt (bước 5).

## 0. Biến (VPS, 1 phiên shell)

```bash
export API=/var/www/tpe/hrm-api
export CLI=/var/www/tpe/hrm-client
alias M='mysql -h 192.168.122.103 -u hrm_tpe -p --table hrm_erp_gop'
# artisan chạy bằng user erp_tpe (đang đăng nhập) ⇒ gọi thẳng php artisan
```

## 1. Kiểm trước (chỉ đọc)

```bash
cd $API && git fetch origin && git status -sb | head -1          # đang ở gop_db, không file sửa tay
php artisan migrate:status | grep "| No"                          # ghi lại danh sách đang chờ TRƯỚC khi pull
```

## 2. Code

```bash
cd $API && git pull origin gop_db && git log --oneline -1         # >= 326374069 (26/10 tip: 4ce76d0df)
composer install --no-dev --optimize-autoloader                   # chỉ cần nếu composer.lock đổi (đợt này không đổi)
cd $CLI && git pull origin gop_db && git log --oneline -1         # >= 094e72fc6 (26/10 tip: cdbdc223b)
```

## 3. Migration — chạy LẺ đúng 2 bản

```bash
cd $API
php artisan migrate:status | grep "| No"
#   Kỳ vọng có 2 bản của feature:
#     2026_10_24_000001_create_manufacture_price_modes_tables      — tạo 2 bảng RỖNG manufacture_price_modes, manufacture_price_mode_items
#     2026_10_24_000002_add_split_columns_to_price_asking_tables    — thêm cột nullable + index: price_asking_requests.origin_request_id,
#                                                                     price_asking_request_groups.transferred_request_id
#   Không UPDATE/DELETE dữ liệu. Danh sách còn bản KHÁC (vd meeting 2026_10_26_*) ⇒ KHÔNG chạy kèm, báo lại để quyết riêng.
php artisan migrate --force --pretend --path=Modules/MasterData/Database/Migrations/2026_10_24_000001_create_manufacture_price_modes_tables.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_24_000001_create_manufacture_price_modes_tables.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_24_000002_add_split_columns_to_price_asking_tables.php
php artisan migrate:status | grep 2026_10_24                      # 2 dòng "Yes"
```
`price_asking_requests` lớn cỡ nào thì ALTER thêm cột nullable cũng chỉ vài giây (MySQL 8 INSTANT/INPLACE).

## 4. Quyền + cache + khởi động lại

```bash
cd $API
php artisan permission:sync --dry-run     # kỳ vọng: thêm 1 ("Cài đặt giá bán theo hãng") · sửa 0 · đổi tên 0 · gỡ 0
#   dry-run báo thêm quyền KHÁC ⇒ dừng, đó là quyền của đợt khác chưa deploy — hỏi lại trước khi sync
php artisan permission:sync
php artisan permission:sync --dry-run     # thêm 0 … 0
php artisan cache:clear                   # cache quyền spatie 24 h
php artisan queue:restart

cd $CLI && npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build      # node 12
sudo /etc/init.d/hrm-client-tpe start     # KHÔNG pm2 restart trần (socket ⇒ 502)
```

Không có cron mới, không có `.env` mới, không đụng ERP.

## 5. Gán quyền + menu (trên giao diện, admin)

1. **Phân quyền** — gán "Cài đặt giá bán theo hãng" (nhóm Hàng hoá) cho vai trò người phụ trách giá ở **từng công ty** sẽ dùng
   (TPSG, TPHP, TPV + công ty nào kế thừa vài hãng). Super admin cũng KHÔNG tự có quyền này.
2. **Cài đặt phân hệ** — mục mới "Giá bán theo hãng sx" (Tài chính › Quản lý giá - CTKM › Giá bán) **không tự ẩn**. Chưa muốn mở
   cho user thì tắt mục này ở Cài đặt phân hệ ngay sau deploy.

## 6. Bật kế thừa cho từng công ty (khi nghiệp vụ sẵn sàng — KHÔNG bắt buộc cùng lúc deploy)

**6.1 Sao lưu giá trước lần lưu đầu** (điểm lui duy nhất cho GIÁ — lưu cài đặt ghi đè giá ngay, không qua duyệt):
```bash
mysqldump -h 192.168.122.103 -u hrm_tpe -p --single-transaction hrm_erp_gop \
  product_unit_prices product_expected_prices product_approves product_approve_prices product_company_units \
  | gzip > ~/backup-gia-truoc-ke-thua-$(date +%Y%m%d-%H%M).sql.gz
```

**6.2 Cài trên màn** Tài chính › Giá bán theo hãng sx (đổi "công ty đang làm việc" sang đúng công ty trước):

| Công ty | Cách cài | Danh sách |
|---|---|---|
| TPSG, TPHP, TPV | **Chọn hãng tự xây dựng giá bán** | **để TRỐNG** ⇒ toàn bộ hãng kế thừa (kể cả hãng mới sau này) |
| Công ty khác cần kế thừa vài hãng | Chọn hãng kế thừa giá theo công ty quản lý | Chọn hãng ⇒ đưa vài hãng vào |

- Nguồn giá = **công ty tạo mã** từng hàng (không cố định TPE): TPHP nhận giá TPSG cho mã TPSG tạo, giá EG cho mã EG tạo.
- Hộp xác nhận nêu: số mã đổi giá, số yêu cầu duyệt giá đang mở sẽ bị **huỷ**, số mã không sửa giá được nữa. Đọc kỹ rồi mới Lưu.
- **Bị chặn "hàng chuyển sang kế thừa đang trong yêu cầu hỏi giá đã gửi — PYCHG-…"** ⇒ xử lý xong / đóng các phiếu đó rồi lưu lại
  (trên dump prod 21/10, TPE có 4 phiếu như vậy; công ty con kiểm lúc lưu).
- 1 công ty ~30.000 mã ⇒ lưu mất khoảng 25–30 s, không đóng trang.

**6.3 So khớp sau mỗi lần lưu** (chỉ đọc):
```bash
cd $API && php artisan product-price:compare-inherited --company=TPSG,TPHP,TPV --csv=/tmp/lech-ke-thua.csv
#   Kỳ vọng: "0 lệch." (exit 0). Còn lệch ⇒ gửi file CSV cho dev, KHÔNG sửa tay giá.
```
Nên chạy lại định kỳ (vd sau mỗi đợt duyệt giá lớn ở công ty quản lý) để bắt đường ghi giá chưa đồng bộ.

## 7. Kiểm khói (10 phút)

1. Mở màn Giá bán theo hãng sx bằng tài khoản có quyền: thấy Hướng dẫn, 2 lựa chọn cách cài đặt, nút Chọn hãng / Lịch sử.
   Tài khoản KHÔNG quyền: menu không có mục, gõ URL ⇒ 404.
2. Sau khi 1 công ty lưu (bước 6): màn Cập nhật giá bán của công ty đó — hàng kế thừa không sửa được giá (báo "Hàng kế thừa giá
   từ TPE…"); Lịch sử giá 1 mã có dòng "Kế thừa giá — Kế thừa từ TPE (đổi cài đặt)".
3. Công ty quản lý sửa giá 1 mã đang được kế thừa ⇒ công ty kế thừa đổi theo ngay (chạy lại 6.3 cho chắc).
4. Lập YCHG ở công ty kế thừa có hàng kế thừa ⇒ Gửi ⇒ phiếu tách sang công ty quản lý.

## LUI

- **Chưa công ty nào lưu cài đặt:** checkout lại `17f76d1f9` (api) · `3940e0c1b` (client) + build client là đủ; 2 bảng/2 cột mới
  để nguyên vô hại (hoặc `migrate:rollback` đúng 2 bản bằng `--path`). Quyền mới để nguyên.
- **Đã có công ty lưu:** giá đã bị ghi đè — đổi cài đặt về như cũ trên màn KHÔNG trả giá cũ (chỉ "giữ giá cuối"). Muốn trả giá cũ
  phải nạp lại bản sao lưu 6.1 cho đúng công ty đó ⇒ làm cùng dev, không tự nạp cả bảng.

---

# ĐỢT 2 (29/10/2026) — Lưu chạy nền + 3 tab + hệ số kế thừa

> Soạn lại 30/10. Chỉ hrm-api + hrm-client (nhánh `gop_db`), ERP KHÔNG đổi. Không quyền mới, không cron mới, không sửa dữ liệu cũ.
> Cài đặt đang có trên prod giữ nguyên nghĩa (mode 1/2 không đổi giá trị, chỉ đổi tên hiển thị) ⇒ deploy xong giá KHÔNG tự đổi.
> **Đã push `gop_db` 30/10.** Bản gõ lệnh từng bước trên VPS: **`HUONG-DAN-VPS-DOT2.md`** (mục dưới là tham chiếu).

| Repo | Commit | Nội dung |
|---|---|---|
| hrm-api | `27384672c` (30/10, đã push) | 2 bảng mới, Job `ApplyManufacturePriceModeJob` (queue `price-inherit`), hệ số kế thừa, API 3 tab |
| hrm-client | `7e127ac53` (30/10, đã push) | Màn Giá bán theo hãng sx 3 tab + dải "Đang áp", badge "Kế thừa · CODE × k" |

Commit ngay trước (đã có trên origin): api `e0f6e694f` · client `8a5304470`. Điểm lui THẬT = HEAD đang chạy trên prod, ghi lại ở bước 1.

## 0. Biến (VPS `ssh -p 2225 erp_tpe@124.158.4.24`, 1 phiên shell)
```bash
export API=/var/www/tpe/hrm-api
export CLI=/var/www/tpe/hrm-client
alias M='mysql -h 192.168.122.103 -u hrm_tpe -p --table hrm_erp_gop'
# artisan chạy bằng user erp_tpe (đang đăng nhập) ⇒ gọi thẳng php artisan, KHÔNG sudo -u www-data
```

## 1. Kiểm trước (chỉ đọc)
```bash
cd $API && git fetch origin && git status -sb | head -1 && git log --oneline -1    # ghi hash = điểm lui api
cd $CLI && git status -sb | head -1 && git log --oneline -1                        # ghi hash = điểm lui client
cd $API && php artisan migrate:status | grep "| No"          # danh sách chờ TRƯỚC khi pull (để biết bản nào KHÔNG thuộc đợt này)
php artisan migrate:status | grep -E "create_jobs_table|create_failed_jobs_table"  # 2 dòng "Yes" (bảng queue có sẵn)
M -e "SELECT COUNT(*) jobs_dang_cho FROM jobs; SELECT queue, COUNT(*) FROM jobs GROUP BY queue;"   # ghi lại, thường 0
which supervisorctl; sudo supervisorctl status          # có supervisor chưa + đang chạy gì
ps aux | grep "queue:work" | grep -v grep               # đã có worker nào của bộ tpe chưa
```
- Không có `supervisorctl` ⇒ dùng **phương án B** ở bước 4 (cron), không tự cài gói lên VPS khi chưa hỏi quản trị máy.

## 2. Code
```bash
cd $API && git pull origin gop_db && git log --oneline -1      # = commit api đợt 2
#   composer.lock đợt này KHÔNG đổi ⇒ không cần composer install
cd $CLI && git pull origin gop_db && git log --oneline -1      # = commit client đợt 2
```

## 3. Migration — chạy LẺ đúng 2 bản
```bash
cd $API
php artisan migrate:status | grep "| No"
#   Kỳ vọng thêm đúng 2 bản của đợt này (ngoài danh sách đã ghi ở bước 1):
#     2026_10_29_000001_create_manufacture_price_mode_runs_table — bảng RỖNG manufacture_price_mode_runs (lượt áp cài đặt)
#     2026_10_29_000002_create_inherited_price_factors_table     — bảng RỖNG inherited_price_factors (hệ số theo hãng / mã)
#   Chỉ CREATE TABLE, không ALTER/UPDATE/DELETE bảng cũ. Bản pending KHÁC ⇒ KHÔNG chạy kèm, báo lại.
php artisan migrate --force --pretend --path=Modules/MasterData/Database/Migrations/2026_10_29_000001_create_manufacture_price_mode_runs_table.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_29_000001_create_manufacture_price_mode_runs_table.php
php artisan migrate --force --pretend --path=Modules/MasterData/Database/Migrations/2026_10_29_000002_create_inherited_price_factors_table.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_29_000002_create_inherited_price_factors_table.php
php artisan migrate:status | grep 2026_10_29                   # 2 dòng "Yes"
```

## 4. Queue worker — BẮT BUỘC (thiếu worker ⇒ bấm Lưu kẹt "Đang áp", 30 phút sau tự báo lỗi, giá không đổi)
- `.env` **KHÔNG** đổi `QUEUE_CONNECTION` (giữ `sync` cho Job cũ). Job đợt này tự dùng connection `database`
  (`config/queue.php` › `price_inherit_connection`, đổi được bằng env `PRICE_INHERIT_QUEUE_CONNECTION`), queue riêng `price-inherit`.
- Chỉ **1 tiến trình** (Job tự chặn 2 lượt áp cùng công ty; 1 worker đủ, tránh 2 lượt nặng cùng lúc).

**Phương án A — supervisor (khuyến nghị):** tạo `/etc/supervisor/conf.d/hrm-tpe-price-inherit.conf`
```ini
[program:hrm-tpe-price-inherit]
command=php /var/www/tpe/hrm-api/artisan queue:work database --queue=price-inherit --timeout=900 --tries=1 --sleep=3
directory=/var/www/tpe/hrm-api
user=erp_tpe
autostart=true
autorestart=true
stopwaitsecs=960
numprocs=1
redirect_stderr=true
stdout_logfile=/var/www/tpe/hrm-api/storage/logs/price-inherit-worker.log
```
```bash
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl status hrm-tpe-price-inherit          # RUNNING
```
- Tên program có tiền tố `hrm-tpe-` để không đụng 4 bộ HRM khác trên cùng máy.
- `php` trong `command` phải là PHP 7.4 mà bộ tpe đang dùng (`php -v` dưới user erp_tpe); khác thì ghi đường dẫn đầy đủ.

**Phương án B — chưa có supervisor:** crontab `erp_tpe` (`crontab -e`) thêm 1 dòng, mỗi phút vét queue rồi thoát, `flock` chặn chạy chồng:
```cron
* * * * * cd /var/www/tpe/hrm-api && flock -n /tmp/hrm-tpe-price-inherit.lock php artisan queue:work database --queue=price-inherit --stop-when-empty --timeout=900 --tries=1 >> storage/logs/price-inherit-worker.log 2>&1
```
  Bấm Lưu chờ tối đa ~1 phút mới bắt đầu áp (dải "Đang áp" vẫn hiện đúng). Có supervisor rồi thì xoá dòng này.

## 5. Cache + khởi động lại
```bash
cd $API
php artisan config:clear && php artisan route:clear       # key mới trong config/queue.php + 3 route mới
sudo systemctl reload php*-fpm                            # nạp code mới (opcache)
php artisan queue:restart                                 # worker đang chạy nạp code mới
cd $CLI && npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build      # node 12
sudo /etc/init.d/hrm-client-tpe start                     # KHÔNG pm2 restart trần (socket ⇒ 502)
```
- **Mọi lần deploy hrm-api sau này** đều phải `php artisan queue:restart` (worker giữ code cũ trong bộ nhớ).

## 6. Kiểm khói (10 phút, tài khoản có quyền "Cài đặt giá bán theo hãng")
1. Màn Tài chính › Giá bán theo hãng sx: 2 lựa chọn tên mới ("Tự xây dựng giá bán riêng theo công ty" / "Kế thừa giá bán theo
   công ty quản lý hàng"), Hướng dẫn ẩn, khối "Khai báo ngoại lệ" 3 tab. Công ty đã cài từ đợt 1 (vd TPHP) vẫn đúng cách cài + danh sách cũ.
2. Ở 1 công ty ÍT hàng (hoặc thêm 1 hãng 0 mã rồi bỏ lại): Lưu ⇒ dải "Đang áp cài đặt…" ⇒ vài giây (B: ≤ 1 phút) tự tắt ⇒ chuông
   "[GIA] Cập nhật: …". Kiểm DB:
   ```bash
   M -e "SELECT id, company_id, status, total, done, summary, error, started_at, finished_at FROM manufacture_price_mode_runs ORDER BY id DESC LIMIT 3;"
   #   status 3 = Đã áp. Kẹt status 1 quá 1 phút ⇒ worker không chạy (bước 4) · status 4 ⇒ đọc cột error + storage/logs/price-inherit-worker.log
   ```
3. `cd $API && php artisan product-price:compare-inherited --company=TPSG,TPHP,TPV` ⇒ "0 lệch." (lệnh đã so theo giá × hệ số).
4. (Khi nghiệp vụ khai hệ số đầu tiên) màn Cập nhật giá bán ở công ty đó: badge "Kế thừa · CODE × k", giá = giá nguồn × k làm tròn 1.000 đ.

## 7. Khai hệ số / lưu lớn (khi nghiệp vụ sẵn sàng — không bắt buộc cùng lúc deploy)
- Sao lưu giá trước lần lưu lớn đầu tiên — như **6.1 đợt 1** (`mysqldump … product_unit_prices product_expected_prices …`).
- **Kiểm giá cũ / giá mới bằng Excel** (mỗi công ty 1 tab): chụp TRƯỚC khi Lưu, chụp SAU khi áp xong, ghép ra Excel — `kiem-gia/README.md`.
- Lưu ~30.000 mã giờ chạy nền: đóng trang được, xong có thông báo. Trong lúc đang áp, Lưu lần nữa ở cùng công ty bị chặn
  ("Đang áp cài đặt do … lưu lúc … — chờ áp xong rồi lưu lại.").
- Hệ số phải > 1, tối đa 2 số thập phân; giá 1 đ giữ nguyên; giá sau nhân không thấp hơn giá nguồn.

## LUI đợt 2
1. Dừng worker: A `sudo supervisorctl stop hrm-tpe-price-inherit` · B xoá dòng cron.
2. `cd $API && git checkout <hash api bước 1>` · `cd $CLI && git checkout <hash client bước 1>` + build + `init.d start`
   + `config:clear` + reload php-fpm.
3. 2 bảng mới để nguyên vô hại (hoặc `migrate:rollback` đúng 2 bản bằng `--path`). Code cũ lưu đồng bộ ⇒ lưu lớn lại có thể 504.
4. Giá đã áp theo hệ số đã ghi đè — lui code KHÔNG trả giá cũ; muốn trả phải nạp lại bản sao lưu (mục 7) cùng dev.
