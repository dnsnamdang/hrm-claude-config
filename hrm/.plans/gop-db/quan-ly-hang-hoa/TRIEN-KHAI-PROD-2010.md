# Triển khai production — Chuyển đổi hàng hoá (toàn bộ) — tối 20/10/2026

> 🚩 **Gõ lệnh trên VPS: theo `HUONG-DAN-VPS-PROD-2010.md`** (bản copy–paste). Đã push 20/10 ~20:15: `gop_db` = nhánh chung (hrm-api `c4d835b49` · hrm-client `37f3e0ef6` · ERP `5bdd056d4e`).

> Runbook TỔNG, chạy từ trên xuống. Gộp + rà lại từ: `deploy-dev-server.md` (Lối B), `gia-theo-cong-ty/runbook-trien-khai.md`
> (phần 1–4), `catalog-import/golive-2010/README.md`, `cron-gia-hieu-luc/design.md` §7, `viec-con-lai.md`, `chuyen-danh-muc-xe/plan-2c.md`,
> `danh-muc-hang-tam/design.md`. Soạn 20/10/2026 ~18:00.
>
> ✅ **ĐÃ CHẠY TẬP TRỌN bước 1–9 trên bản sao prod `hrm_erp_20_10` (20/10 ~19:45–20:15, code đã merge `gop_db`)** — số "prod" trong
> runbook là số THẬT đo được. Chạy tập lộ 6 chỗ đã sửa: KQ tính giá trùng (file mới `0_…`), 36 YCHG chéo dở (file mới `8_…`),
> prod ĐÃ CÓ cây phân loại cũ cùng dãy mã khác tên (file cây nay THAY cây cũ), `product_types` prod thiếu 2 cột cũ của giacty,
> catalog bắt buộc `@nguoi_chay` (created_by NOT NULL + FK), prod đã có sẵn phần lớn catalog Dịch vụ ô tô.
>
> **Nguyên tắc**
> - ERP + HRM dùng CHUNG 1 DB gộp ⇒ migration / backfill / dữ liệu chạy MỘT lần ở **hrm-api**; ERP chỉ code + `.env` + 2 lệnh dọn.
> - Không cờ, không đường lui bằng code. **Lui duy nhất = khôi phục bản sao lưu bước 2** + checkout lại commit cũ cả 3 repo.
> - Mỗi bước có **ĐIỂM DỪNG**: số không khớp ⇒ DỪNG, không làm tiếp, báo dev. Lệnh có `--dry-run` thì luôn chạy dry-run trước.
> - Không `cache:clear` ở HRM (redis dùng chung ERP) trừ khi ghi rõ. Không `pkill` theo tên tiến trình.
> - Nhãn: **[ERP]** thư mục ERP · **[API]** hrm-api · **[CLIENT]** hrm-client · **[DB]** SQL trên DB prod · **[OS]** máy chủ.

## Thông tin đợt

| Repo | Nhánh deploy | Commit (merge `origin/gop_db` vào nhánh chung, **ĐÃ PUSH 20/10** — `gop_db` fast-forward lên đây) |
|---|---|---|
| hrm-api | `gop_db` (fast-forward lên nhánh chung) | `c4d835b49` |
| hrm-client | `gop_db` | `37f3e0ef6` |
| ERP | `gop_db` | `5bdd056d4e` (xung đột `HomeController` — giữ bản nhánh chung: bỏ 3 thẻ hỏi/tính giá) |
Nhánh chung và `gop_db` trỏ cùng commit ⇒ server checkout `gop_db`. Commit `gop_db` TRƯỚC đợt (để lui): hrm-api `f808edbeb` · hrm-client `79d642ab9` · ERP `4009791fa8`.

- Bản sao prod 20/10 chờ **đúng 32 migration của feature** (Phụ lục A), không bản lạ. ERP không có migration mới.
- Thời gian đo TRÊN BẢN SAO PROD (12,3 GB): migrate lượt 1 4,5 s · backfill dry 7 s / thật 47 s · compare 8 s · migrate lượt 2 22 s ·
  quyền ~3 s · nhóm YCHG 7 s · close-stale 1 s · dọn giá ERP 1 s · 6 file SQL tổng ~4 s ⇒ **kỹ thuật ≈ 2 phút**; + sao lưu 12–40 phút ·
  build client 5–10 phút · khói 15 phút ⇒ **cửa sổ dự trù 1h–1h30**.
- 6 file SQL (thư mục `catalog-import/golive-2010/`): `0_kq_tinh_gia_trung_2010.sql` · `8_dong_phieu_hoi_cheo_2010.sql` ·
  `cay-4-cap/cay_4_cap_2010.sql` · `golive_bo_nhom_2010.sql` · `catalog-dich-vu-o-to/catalog_dich_vu_o_to_2010.sql`.
  Chạy bằng MySQL client (sql_mode strict) — ĐÃ chạy lại cả 5 ở strict trên bản sao: không lỗi. Giữ dòng đầu `SET NAMES … COLLATE utf8mb4_unicode_ci`.

---

## BƯỚC 0 — Trước giờ G (làm trước, app vẫn chạy)

| # | Việc | Cách | Đạt khi |
|---|---|---|---|
| 0.1 | Giờ chạy job backup DB không trùng cửa sổ | `sudo crontab -l` (mọi user) · `/etc/cron.d` · `systemctl list-timers` | backup không chạy giữa lúc migrate (dump chụp DB dở) |
| 0.2 | Dung lượng đĩa | `df -h` | trống ≥ 2 × DB (DB ~11–12 GB) |
| 0.3 | [DB] Phiếu hỏi giá CHÉO công ty còn dở | SQL dưới | prod 20/10: **36** ⇒ user chốt đóng bằng lệnh (file `8_…`, bước 8) — chỉ ghi số |
| 0.4 | [DB] Hàng tạm ERP chờ duyệt | `SELECT COUNT(*) FROM tmp_products WHERE status = 2;` | = 0 (duyệt / từ chối nốt ở ERP) |
| 0.5 | [DB] Trùng trước khi ép UNIQUE (luồng tính giá) | SQL dưới | prod 20/10: 0 / **2** (PTG-03422, PTG-03425) ⇒ file `0_…` ở bước 3.6 |
| 0.6 | Danh sách người dùng cần cấp quyền (bước 11) đã sẵn | xem 11.2 | có tên + vai trò |

```sql
-- 0.3 phiếu hỏi chéo công ty còn dở (PHẢI = 0)
SELECT COUNT(DISTINCT a.id) FROM price_asking_requests a
WHERE a.status IN (1,2,5,7) AND a.send_company_id IS NOT NULL AND a.company_id <> a.send_company_id;
-- 0.5 trùng
SELECT COUNT(*) FROM (SELECT price_calculate_request_id FROM price_calculates GROUP BY 1 HAVING COUNT(*) > 1) x;
SELECT COUNT(*) FROM (SELECT price_calculate_id FROM price_calculate_results GROUP BY 1 HAVING COUNT(*) > 1) x;
```

---

## BƯỚC 1 — Đóng app (giữ MySQL + cron để job backup vẫn chạy)

```bash
# [ERP] (Laravel 6)
php artisan down --message="Đang nâng cấp hệ thống" --allow=<IP dev>
# [API] (Laravel 8)
php artisan down --secret="<chuoi-bi-mat>"
# [CLIENT] dừng đúng tiến trình Nuxt của hrm-client
pm2 list                      # lấy đúng tên/id
pm2 stop <tên-hoặc-id-hrm-client>
```
- **KHÔNG** dừng MySQL, service `cron`, không comment crontab.
- Khi 2 app `down`: mọi tác vụ scheduler Laravel tự bỏ qua (không tác vụ nào `evenInMaintenanceMode`) — kể cả cron áp giá 01:00 HRM và
  `reset_price_when_zero_inventory` ERP; queue worker ngưng xử lý. Lệnh artisan chạy tay vẫn chạy bình thường.
- Nếu cửa sổ có thể kéo qua 01:00 mà phải `up` sớm 1 app: tạm comment dòng `schedule:run` của HRM tới hết bước 8.

## BƯỚC 2 — Sao lưu (điểm lui)

```bash
mysqldump --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF <db> \
  | gzip > backup_<db>_$(date +%F_%H%M).sql.gz
zcat backup_<db>_*.sql.gz | tail -1        # phải có "-- Dump completed"
```
Ghi lại số dòng để so khi lui:
```sql
SELECT 'upp', COUNT(*) FROM product_unit_prices UNION ALL SELECT 'pu', COUNT(*) FROM product_units
UNION ALL SELECT 'pcc', COUNT(*) FROM product_company_coefficients UNION ALL SELECT 'pep', COUNT(*) FROM product_expected_prices
UNION ALL SELECT 'products', COUNT(*) FROM products;
```
**ĐIỂM DỪNG 2:** file khác rỗng, có dòng "Dump completed".

## BƯỚC 3 — Lấy code + cấu hình

```bash
# [ERP]
git fetch origin && git checkout feat/2d1-erp-khong-loi && git pull && git rev-parse --short HEAD   # 72cf3142db
composer install --no-dev -o
# [API]
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull && git rev-parse --short HEAD # 0425cafb1
composer install --no-dev -o
# [CLIENT]
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull && git rev-parse --short HEAD # 6b27b9946
```

**3.1 [ERP] `.env`** — thêm/kiểm:
```
HRM_URL_FE=<url hrm-client>        # link "Chức năng đã chuyển sang HRM", xem chi tiết hàng hoá
HRM_URL_BE=<url hrm-api>
HRM_API_BASE_URL=<url hrm-api>     # popup chọn hàng ERP gọi API HRM
IS_USE_SSO=true                    # giữ như prod hiện tại (popup gọi HRM bằng cookie jwt_token)
JWT_SECRET=<GIỐNG HRM>             # ERP và HRM phải chung JWT_SECRET
```
Kiểm thêm: `MATE_API_USE_CRM` — nếu đang bật thì CRM sẽ lệch dần (HRM ghi hàng thẳng DB, không qua hook ERP) ⇒ báo dev.

**3.2 [API] `.env`** — không biến mới bắt buộc. Kiểm `ERP_URL` có khai (logo/letterhead Excel + bản in dùng đường dẫn tương đối).

**3.3 Xoá cache cấu hình + kiểm đúng DB** (cả ERP và API):
```bash
php artisan config:clear && php artisan route:clear && php artisan view:clear
php artisan tinker --execute="echo DB::connection()->getDatabaseName();"     # PHẢI ra tên DB production
```
Prod đang dùng `config:cache` thì chạy lại `php artisan config:cache` ở bước 10 (sau khi xong mọi lệnh).

**3.4 [OS] Nạp lại PHP** (ERP từng chạy code cũ do opcache — N192): `sudo systemctl reload php<phiên bản>-fpm`.

**3.5 [ERP] lịch giá đã bỏ:** `grep -n "product:update_price" app/Console/Kernel.php` ⇒ chỉ còn dòng chú thích.

**3.6 [DB] Dọn KQ tính giá trùng — TRƯỚC migration:** chạy `golive-2010/0_kq_tinh_gia_trung_2010.sql` (giữ KQ mới nhất — PTG đã sửa rồi
trả KQ lần 2; sao lưu `zz_golive2010_kq_trung_*`). Đạt khi dòng cuối `ptg_con_trung_PHAI_0 = 0`. Prod: xoá 2 KQ · 13 dòng hàng · 78 giá · 13 giá dự kiến.

## BƯỚC 4 — [API] Migration lượt 1 — PHẢI DỪNG Ở M3

```bash
php artisan migrate:status | grep "| No"       # đối chiếu Phụ lục A (+ migration gop_db prod chưa có, vd 2026_10_12_000000_change_exchange_rate…)
php artisan migrate --force
```
Prod: 9 migration (4,5 s) rồi dừng. **ĐIỂM DỪNG 4:** lệnh **báo lỗi** tại `2026_10_09_000004_enforce_company_id_on_product_unit_prices_table` (prod: "còn 275772 dòng"):
"còn N dòng company_id NULL… Không có thay đổi nào được áp" — ĐÚNG (M3 tự chặn, chờ backfill).
Chạy qua luôn không lỗi ⇒ DB không phải DB chưa chuyển đổi ⇒ **DỪNG**, báo dev.

**[ERP]** `php artisan migrate:status | grep "| No"` — có bản `gop_db` chưa chạy (vd `2026_10_14_000000_add_indexes_for_wr_assign_task_wait_list`,
chỉ thêm index, tự bỏ qua nếu có) ⇒ chạy lẻ: `php artisan migrate --force --path=database/migrations/<file>.php`.
Bảng `migrations` dùng chung ⇒ bản đã chạy bên HRM sẽ hiện "Yes" ở ERP.

## BƯỚC 5 — [API] Backfill giá theo công ty

```bash
php -d memory_limit=4G artisan product-price:backfill-company --dry-run
php -d memory_limit=4G artisan product-price:backfill-company
php -d memory_limit=4G artisan product-price:compare --csv=/tmp/compare.csv
```
| Kiểm | Đạt khi |
|---|---|
| dry-run dòng "B0 kiểm trước" | `orphan_upp 0, owner_unknown 0, duplicates 0, pcu_foreign 0` — ≠ 0 ⇒ DỪNG |
| dry-run TỔNG GHI | prod 20/10: **1.057.680** (Cty 1 344.949 · 2 232.141 · 3 232.141 · 4 232.576 · 8: 7 · 9: 15.866) — lệch xa ⇒ DỪNG |
| luật (`config/price.php`) | **1 · 2 · 3 · 4** chép giá lẫn nhau; **7 · 9** tự quản (chỉ hàng mình làm chủ, không nhận/không cho); 5 · 6 · 8 bỏ qua. Cty 9 chỉ có trên prod ⇒ cột Cty 9 chỉ có B1–B4 |
| chạy thật | bảng in = dry-run, dòng cuối **"B6 kiểm sau: đạt"** (~1–2 phút) |
| compare | dòng cuối **`0 lệch.`** (prod: 115.199 cặp · T4 443 · §3.3 24.208) — ≠ 0 ⇒ DỪNG, KHÔNG chạy M3, gửi `/tmp/compare.csv` cho dev |

Lỗi giữa chừng ⇒ lô tự rollback, chạy lại lệnh (idempotent; dry-run lần 2 = 0).

## BƯỚC 6 — [API] Migration lượt 2 + seeder

```bash
php artisan migrate --force                      # M3 + các migration sau nó (Phase 7, cron, kho…)
php artisan migrate:status | grep -c "| No"      # = 0
php artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder" --force   # 8 điều kiện thanh toán, chạy lại không nhân đôi
```
**ĐIỂM DỪNG 6:** `product_unit_prices.company_id` NOT NULL; `migrate:status` 0 chờ. Prod: 23 migration, 22 s (M3 15,6 s); sau: upp 800.347 ·
pcu 134.868 · pcc có status 115.199 · pep 103.122 · payment_conditions 8.

## BƯỚC 7 — [API] Quyền (đồng bộ theo TÊN — KHÔNG chạy seeder quyền riêng cũ, KHÔNG INSERT theo id)

```bash
php artisan permission:sync --dry-run       # đọc kỹ (dưới)
php artisan permission:sync
php artisan permission:sync --dry-run       # = 0 thay đổi
php artisan permission:cache-reset          # "Unable to flush cache" khi chưa có khoá ⇒ vô hại
```
DỪNG báo dev nếu dry-run lượt đầu có: "tên đã có ở id khác" / lỗi; hoặc `Thêm … định mức thưởng P3` kèm `⚠ … không khai báo: … lương P3`
(migration rename P3 chưa chạy); hoặc `⚠ … không khai báo: Xem/Quản lý/Xoá/Xuất dữ liệu danh mục hàng hoá` (quyền rác dev).
Bình thường: "Gộp trùng: … danh mục tiền tệ", "Thêm … (giữ id cũ N)". **Prod 20/10: "thêm 30 · sửa 0 · gỡ 0 · không khai báo 0"**
(8 quyền xe 2c, 10 quyền hàng hoá/giá, 12 quyền kho/kiểm kê) — lần 2 = 0.
Kiểm đủ 73 quyền của luồng: SQL ở `deploy-dev-server.md` §B7 (kết quả rỗng = đủ).

## BƯỚC 8 — Luồng tính giá + dữ liệu cũ ERP

```bash
# [API] nhóm YCHG
php artisan price-asking:backfill-groups --dry-run      # local: 4.029 nhóm
php artisan price-asking:backfill-groups
php artisan price-asking:backfill-groups --dry-run      # = 0 mọi dòng
php artisan price-asking:close-stale --before=2026-06-01 --dry-run    # xem số; "CHƯA backfill nhóm" = 0
php artisan price-asking:close-stale --before=2026-06-01 --by=<employees.id người chạy>
php artisan price-asking:close-stale --before=2026-06-01 --dry-run    # = 0
```
```sql
-- [DB] N26 — product_versions AUTO_INCREMENT
SELECT MAX(product_version_id) FROM product_histories;                                                            -- (A)
SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'product_versions';  -- (B)
-- CHỈ KHI (B) <= (A):  ALTER TABLE product_versions AUTO_INCREMENT = <(A) + 1>;
```
```bash
# [ERP] dọn giá hiệu lực quá hạn + cờ mồ côi — user web (storage/app thuộc www-data)
sudo -u www-data php artisan price:cleanup-stale --dry-run   # xuất storage/app/price-cleanup/<ts>-dry-run/gia-qua-han-<năm>.csv
sudo -u www-data php artisan price:cleanup-stale             # tự sao lưu CSV từng bảng trước khi ghi
sudo -u www-data php artisan price:cleanup-stale --dry-run   # mọi nhóm = 0
```
```sql
-- [DB] chốt chặn cron áp giá: PHẢI rỗng (công ty còn giá chờ > 30 ngày bị cron bỏ qua)
SELECT upp.company_id, COUNT(*) FROM product_expected_prices pep JOIN product_unit_prices upp ON upp.id = pep.unit_price_id
WHERE pep.status = 2 AND (pep.flag <> 1 OR pep.flag IS NULL) AND pep.effect_date < CURDATE() - INTERVAL 30 DAY
GROUP BY upp.company_id;
```
Gửi `gia-qua-han-<năm>.csv` cho nghiệp vụ soát.
Prod: backfill nhóm **4.404** nhóm (7 s) · close-stale **45** nhóm · N26 A 177.200 < B 177.201 ⇒ KHÔNG chỉnh · cleanup-stale **13.953** quá hạn
(2026: 2.105) + cờ mồ côi 5/6/6 · chốt chặn cron rỗng.

**8.x [DB] Đóng YCHG CHÉO công ty còn dở** — SAU backfill nhóm + close-stale: `golive-2010/8_dong_phieu_hoi_cheo_2010.sql`,
**sửa dòng `SET @nguoi_chay = <employees.id người chạy>`** (bắt buộc; NULL ⇒ `ok_PHAI_1 = 0`, không ghi gì). Như close-stale nhưng lọc phiếu chéo.
Prod: đóng **28** nhóm / 28 phiếu (8 phiếu chéo còn lại đã do close-stale đóng vì tạo trước 01/06); kiểm cuối rỗng = 0 phiếu chéo dở.

## BƯỚC 9 — [DB] Dữ liệu hàng hoá (gói `catalog-import/golive-2010/`)

Chạy bằng MySQL client / tool DB. **Giữ nguyên dòng đầu** `SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci` (thiếu ⇒ lỗi 1267).
Mỗi file tự in số kiểm; chạy lại lần 2 = 0 dòng (an toàn). Chi tiết + số kỳ vọng: `golive-2010/README.md`.

| # | File | Việc | Đạt khi (đo bản sao giacty) |
|---|---|---|---|
| 9.1 | `cay-4-cap/cay_4_cap_2010.sql` | **THAY** cây cũ prod (nhập 15/10, 6/48/270/959, mã trùng dãy khác tên) bằng cây 17/10 + lịch sử; TCHH.0005 "Là phụ tùng ô tô" | K0 prod 6·48·270·959 · K0b `hang_va_thuoc_tinh…_PHAI_0 = 0`, `ok_PHAI_1 = 1`, `se_thay_cay_cu = 1` · sao lưu `zz_golive2010_cay_cu_*` 959 Loại · K1 rỗng · K2 = 0·0·0·0 · tổng 6/48/282/968 |
| 9.2 | — | (cây cũ prod không có dòng rác — bỏ bước này) | — |
| 9.3 | `golive_bo_nhom_2010.sql` | Gán Loại SP (theo mã file + nhóm 1–1), chép VAT nhóm cho hàng VAT NULL, tồn lâu 180, thuộc tính nhóm 1–1 | prod: B0 968 · "mã Loại không có" rỗng · gán 7.992 + 8.034 dòng ⇒ **11.959** hàng đang dùng có Loại · VAT chép **1.290** dòng, còn NULL **17** · tồn lâu 968 · thuộc tính **957** / 234 Loại |
| 9.4 | `catalog-dich-vu-o-to/catalog_dich_vu_o_to_2010.sql` | Catalog Dịch vụ ô tô: tìm-hoặc-tạo cây 14/77/243 + gắn hàng Cty **1·2·3·4** | **sửa `SET @nguoi_chay = <employees.id>` — BẮT BUỘC** (created_by NOT NULL + FK; NULL ⇒ `ok_PHAI_1 = 0`, không ghi) · prod ĐÃ CÓ 14 Chương + 77 Mục + 229 Tiểu mục ⇒ tạo thêm **14 Tiểu mục** · gắn **814 / công ty** (716 hàng) · C5: 8 mã không có trên DB (×4 = 32 dòng) |

`@nguoi_chay` ở file cây 4 cấp: tuỳ chọn (cột người tạo cho phép NULL). Danh sách gửi nghiệp vụ lấy từ bản sao prod: `golive-2010/ds-gui-nghiep-vu-prod-2010.xlsx`.

## BƯỚC 10 — Mở lại

```bash
# [CLIENT] (node 12)
npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build
# [API]
php artisan queue:restart          # bỏ qua nếu QUEUE_CONNECTION=sync
php artisan up
# [ERP]
php artisan config:clear && php artisan route:clear && php artisan view:clear
php artisan config:cache           # CHỈ nếu prod vốn dùng config cache
php artisan up
# [CLIENT]
pm2 restart <tên-hoặc-id-hrm-client>
```
**[OS] Cron:**
```bash
sudo crontab -u www-data -l | grep schedule:run     # phải có dòng trỏ thư mục hrm-api (thiếu thì thêm, user chạy web):
# * * * * * cd <HRM_API_DIR> && php artisan schedule:run >> /dev/null 2>&1
cd <HRM_API_DIR> && php artisan schedule:list | grep apply-expected     # 0 1 * * *  product-price:apply-expected
```
⚠️ **KHÔNG bật lại** `product:update_price` ở ERP (2 hệ thống cùng áp giá ⇒ lịch sử đôi). Crontab ERP giữ nguyên (`schedule:run` ERP vẫn chạy cron khác).

## BƯỚC 11 — Quyền + dữ liệu nghiệp vụ tối thiểu (quản trị HRM)

**11.1** Đường vào: Quản trị hệ thống › Người dùng & phân quyền › Danh sách phân quyền › sửa vai trò › **chọn công ty** (quyền gán theo
từng công ty) › tick. Bảng quyền đầy đủ: `deploy-dev-server.md` §B10. Super admin KHÔNG tự có quyền — cũng phải tick.
Xong: `php artisan permission:cache-reset` (báo "Unable to flush cache" ⇒ `php artisan cache:clear` ở **API**).

**11.2 Bổ sung so với §B10 (dễ sót):**
- **Danh mục xe 2c** (biển số · lái xe ngoài · xe · nhiên liệu) — ERP đã chặn ghi ⇒ gán cho người đang dùng ở ERP (danh sách
  `chuyen-danh-muc-xe/plan-2c.md:38-50`: Thơm 311, Thúy 34, Lợi 787, Thịnh 408/1035, Ly 332, Dũng 917, Nhung 204, Hồng 336) + người có
  quyền ERP 100134/100135/100138. Người đang sửa 6 danh mục xe 2b ở ERP ⇒ quyền HRM 2b.
- **PTKD**: thêm "Xây dựng thông tin hàng hoá" — thiếu thì nút Sửa hàng tạm bị ẩn.
- **[ERP]** "Xem phiếu yêu cầu đặt hàng trong nước theo tổng công ty" cho vai trò cần xem (N160).

**11.3 Dữ liệu nghiệp vụ (thiếu ⇒ chức năng chết):**
- Danh mục **Đặc tính sản phẩm** — đang 0 dòng, KHÔNG có trong gói ⇒ không tạo được hàng tạm tới khi nhập.
- Cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất (đang tắt hết).
- Phân công XNK theo công ty — Cty 2/5/6/7/8 chưa có ⇒ không gửi được Yêu cầu hỏi giá.

## BƯỚC 12 — Khói (15 phút)

**HRM**
- `/master-data/products/company`: danh sách + Xuất Excel. Mở 1 hàng: có Loại SP (hàng thuộc 11.826), tab Thông số có thuộc tính (Loại có thuộc tính).
- `/finance/product-prices`: lọc 1 mã đang bán ⇒ Cty 1·2·3·4 đều có giá (× hệ số); Cty 7/9 chỉ hàng mình làm chủ.
- Tài chính › Quản lý giá - CTKM › **Nhật ký áp giá** mở được; tài khoản chỉ "Duyệt giá bán" xem được, không nút xử lý.
- `/sale/price-asking-requests`: danh sách có nhóm; YCHG cũ đã tính ⇒ nhóm "Đã tính giá", "In kết quả" ra KQ. `/finance/price-calculates` mở được.
- `/master-data/products/temp` mở được; YCHG có "Thêm hàng tạm".
- Danh mục: Tính chất 6 · Loại SP 968; Chương lĩnh vực Dịch vụ ô tô 14; popup "Xây dựng catalog" Cty 1 thấy hàng trong Tiểu mục.
- `/master-data/vehicles`.

**ERP**
- `/admin/products/{id}/show`, `/admin/products/editPrices`, `/admin/sale/price_logs`, `/admin/orders/price_asking_requests`,
  `/admin/orders/price_calculates`, `/admin/tmp_products/{id}/edit` ⇒ trang "Chức năng đã chuyển sang HRM" có link đúng.
- Báo giá: popup chọn hàng ra giá đúng công ty người dùng; tài khoản Hải Phòng thấy hàng nhóm chia sẻ.
- Trang chủ ERP không còn 3 thẻ Yêu cầu hỏi giá / tính giá chờ duyệt.

## BƯỚC 13 — Sau go-live

| Khi | Việc |
|---|---|
| Ngay | Gửi nghiệp vụ `golive-2010/ds-gui-nghiep-vu-prod-2010.xlsx` (17 hàng VAT trống · 8 mã catalog không có · 36 YCHG chéo đã đóng ⇒ người lập tạo lại trên HRM nếu cần) · `gia-qua-han-<năm>.csv` (bước 8). Đo lại trên prod thật nếu số lệch |
| Trước 01:00 đêm đầu | Soát giá hiệu lực đang chờ ≤ 1 đ / giảm sâu (lần cron HRM đầu áp mọi giá tới hạn trong 30 ngày; vd `LUTR-SL-4012` Cty 3 về 1 đ). Quy ước giá dự kiến 1 đ ngày 31/12 là cố ý |
| Sáng 21/10 | Tài chính › Nhật ký áp giá có dòng mới nếu có giá tới hạn + chuông thông báo; không có ⇒ `php artisan schedule:list` + log HRM |
| Trong tuần | Kiểm 2 màn chờ duyệt TN mới trên dữ liệu thật (N126) · N161 dọn quyền tiền tệ trùng 1117→1115, 1118→1116 (kiểm prod trước) · đo N151 (gói bảo dưỡng không file ⇒ Sửa 422) · Q3 (prod phải 0 nhóm dùng `rate_liquidation`/`checksheet_id`) · bộ lọc Đời xe chậm ⇒ index `(life_id, product_id)` (N113) |
| Sau nghiệm thu | `DROP TABLE` các bảng phụ `zz_golive2010_*` (lệnh ở cuối từng file SQL bước 9) |
| Đợt code sau | Bỏ Nhóm hàng phần CODE: Nhóm máy → Loại + picker ERP · ERP tồn lâu đọc theo Loại · ~30 INNER→LEFT JOIN · bỏ dự phòng VAT nhóm (`viec-con-lai.md` "⏰ NHẮC LÀM SAU") |

## LUI (chỉ khi điểm dừng hỏng không sửa được trong cửa sổ, hoặc lỗi nghiêm trọng ngay sau khi mở)

1. `php artisan down` ERP + API; `pm2 stop` client.
2. Khôi phục: `gunzip < backup_<db>_….sql.gz | mysql <db>` (≈ thời gian dump).
3. Checkout lại commit TRƯỚC đợt ở **cả 3 repo** (code mới bắt buộc `company_id`, không chạy trên DB cũ), `composer install`, build client, reload php-fpm.
4. ERP: bật lại lịch `product:update_price` (code cũ) — luôn lui CẢ HAI app (lui 1 bên ⇒ 2 cron cùng áp / không cron nào áp).
5. So số dòng bước 2, mở lại. ⚠️ Mọi dữ liệu ghi sau lúc mở lại sẽ mất ⇒ chỉ lui trong cửa sổ / trong ngày.
Lui riêng phần dữ liệu bước 9 (không cần khôi phục cả DB): khối "LUI" cuối từng file SQL (cây 4 cấp chỉ lui được TRƯỚC khi chạy 9.3).

---

## Phụ lục A — 32 migration hrm-api của feature (so `origin/gop_db`)
`2026_09_22_000001_add_classification_to_products_table` · `2026_09_22_000002_drop_can_retail_from_product_types_table` ·
`2026_10_04_000002_add_company_status_to_product_company_coefficients_table` · `2026_10_04_000003_add_company_id_to_product_suppliers_table` ·
`2026_10_04_000004_create_product_business_catalogs_table` · `2026_10_07_000001_add_is_auto_parts_to_product_natures_table` ·
`2026_10_09_000001_add_barcode_template_type_to_product_types_table` · **M1** `2026_10_09_000002_create_product_company_units_table` ·
**M2** `2026_10_09_000003_add_company_id_to_product_unit_prices_table` · **M3** `2026_10_09_000004_enforce_company_id_on_product_unit_prices_table` ·
`2026_10_11_000001…000003` (chính sách giá nội bộ ×3) · `2026_10_11_100001…100009` (luồng tính giá ×9) ·
`2026_10_13_000001_add_service_flags_to_product_natures_table` · `2026_10_15_000001_add_product_life_index_to_product_vehicle_model_has_life_table` ·
`2026_10_15_000001_make_group_id_nullable_on_service_has_products_table` · `2026_10_17_000001_add_unchosen_reason_to_price_calculate_lines` ·
`2026_10_17_100001_create_product_price_apply_logs_table` · `2026_10_19_000001_create_company_product_natures_table` ·
`2026_10_19_100001…100004_add_status_to_{houses,rows,spaces,positions}_table`.
Ngoài ra `migrate:status` prod có thể còn migration của `gop_db`/`develop` chưa từng lên prod (vd `2026_10_12_000000_change_exchange_rate…`,
`2026_10_13_000001_rename_luong_p3_to_dinh_muc_thuong_p3`, điều kiện thanh toán `2026_10_16_*`) — chạy cùng, bình thường.

## Phụ lục B — Lệnh artisan của đợt
| Lệnh | Repo | dry-run |
|---|---|---|
| `product-price:backfill-company` | API | có |
| `product-price:compare` | API | chỉ đọc |
| `product-price:apply-expected` | API | — (cron 01:00; không chạy tay trên prod nếu không cần) |
| `price-asking:backfill-groups` | API | có |
| `price-asking:close-stale --before= --by=` | API | có |
| `permission:sync` · `permission:cache-reset` | API | có / — |
| `price:cleanup-stale` | ERP | có |
| `price:snapshot` | ERP | chỉ đọc (nghiệm thu) |
| `product:update_price` | ERP | — (đã bỏ lịch, chỉ chạy tay khẩn cấp) |
