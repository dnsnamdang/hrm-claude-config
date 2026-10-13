# Runbook triển khai — Giá theo công ty (một lần, cùng đợt lên production của cả feature)

> Viết 10/10/2026 (G6) sau khi **chạy thử trọn** trên bản sao tạm `hrm_erp_runbook` (dump `--single-transaction` từ `hrm_erp` local,
> code nhánh chung hrm-api `feat/chuyen-doi-hang-hoa` + G6, MySQL 8.0.43, MacBook local). Bản sao đã DROP sau khi chạy.
> Không cờ, không đường lui bằng code (design "Đổi 10/10/2026 — BỎ CỜ"): **cách lui duy nhất = khôi phục bản sao lưu bước 1**.
> Bối cảnh 10/10: PTG (Phase 7) + hàng tạm (Phase 6) cũng chuyển HRM trong cùng lần cập nhật ⇒ lên cùng lúc, không giai đoạn tạm.

## 0. Điều kiện trước

| # | Kiểm | Lệnh / cách | Đạt khi |
|---|---|---|---|
| 0.1 | Code HRM (hrm-api + hrm-client) và ERP đã deploy đúng nhánh của đợt | `git log -1` 3 repo | đúng commit release |
| 0.2 | Không ai thao tác giá trong lúc chạy: tạm dừng **cron ERP** `product:update_price` (01:00) + `product:reset_price_when_zero_inventory` (14:30); khoá bảo trì ERP + HRM | crontab / `php artisan down` cả 2 app | không còn request ghi |
| 0.3 | Cache config không trỏ nhầm DB | `php artisan config:clear` (cả 2 app) rồi `php artisan tinker --execute="echo DB::connection()->getDatabaseName();"` | đúng tên DB production |
| 0.4 | Dung lượng đĩa | `df -h` | ≥ 2 × dung lượng DB (local: DB 11 GB) |
| 0.5 | Migration đang chờ chỉ gồm của đợt | `php artisan migrate:status \| grep "\| No"` | thấy M1 `2026_10_09_000002_create_product_company_units_table`, M2 `…000003_add_company_id_to_product_unit_prices_table`, M3 `…000004_enforce_company_id_on_product_unit_prices_table` (+ migration khác của release nếu có — chạy ở bước 2 TRƯỚC M1 nếu tên file đứng trước) |

⚠️ Local `hrm_erp` đã có sẵn M1/M2 (batch 430/431) nên lần thử phải `migrate:rollback --step=2` trên bản sao trước; **production bắt đầu
thẳng từ bước 2 (M1)**.

## 1. Sao lưu (điểm lui)

```bash
mysqldump --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF <db> | gzip > backup_<db>_$(date +%F_%H%M).sql.gz
```
- Đo local (dump đổ thẳng sang DB khác, không nén): **750 s ≈ 12,5 phút** cho 10,95 GB / 1.869 bảng.
- Kiểm: file khác rỗng, `zcat … | tail -1` có `-- Dump completed`. Ghi lại số dòng 5 bảng giá để so khi lui:
  `product_unit_prices` 264.646 · `product_units` 46.560 · `product_company_units` 0 · `product_company_coefficients` 1.105 · `product_expected_prices` 95.266 (số local).

## 2. M1 → M2 (hrm-api)

```bash
cd hrm-api
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_09_000002_create_product_company_units_table.php
php artisan migrate --force --path=Modules/MasterData/Database/Migrations/2026_10_09_000003_add_company_id_to_product_unit_prices_table.php
```
| Bước | Đo local | Kiểm sau |
|---|---|---|
| M1 tạo `product_company_units` | 0,24 s (lệnh 1,1 s) | bảng có, 0 dòng |
| M2 `product_unit_prices.company_id` NULL + FK + index | 3,9 s (lệnh 5,3 s) | `SHOW COLUMNS … LIKE 'company_id'` = `bigint unsigned YES` |

- **KHÔNG** chạy `php artisan migrate` một lèo ở đây. Nếu lỡ chạy: M3 tự chặn (đã thử: `RuntimeException` "còn 264646 dòng company_id NULL…
  Không có thay đổi nào được áp", 0,6 s, M3 vẫn `No`) ⇒ chỉ cần đi tiếp bước 3.

## 3. Backfill (hrm-api)

```bash
php -d memory_limit=4G artisan product-price:backfill-company --dry-run     # 6,2 s, không ghi
php -d memory_limit=4G artisan product-price:backfill-company               # 71 s
```
**Điểm dừng 3a — dry-run** phải khớp bảng (số local 10/10; production đo lại, chênh do dữ liệu mới thì đối chiếu §3.4 design):

| Việc | Cty 1 | Cty 2 | Cty 3 | Cty 4 | Tổng |
|---|---:|---:|---:|---:|---:|
| B0 kiểm trước | `orphan_upp 0, owner_unknown 0, duplicates 0, pcu_foreign 0` | | | | |
| upp.assign (B1) | 258.270 | 18 | 138 | 6.220 | 264.646 |
| pcu.owner (B2) | 45.477 | 3 | 23 | 1.057 | 46.560 |
| upp.fill (B3) | 5.765 | 0 | 0 | 108 | 5.873 |
| pcc.owner insert/update (B4) | 27.370 | 3 | 14 | 980 + 4 | 28.371 |
| pcu.copy (B5) | 1.010 | 28.844 | 28.824 | 27.863 | 86.541 |
| upp.copy (B5) | 6.060 | 173.064 | 172.944 | 167.178 | 519.246 |
| pep.copy (B5) | 32 | 2.008 | 2.008 | 1.976 | 6.024 |
| pcc.recv insert/update (B5) | 1.001 | 27.970 + 398 | 27.975 + 382 | 27.364 + 23 | 85.113 |
| **TỔNG GHI** | 344.985 | 232.308 | 232.308 | 232.773 | **1.042.374** |

B0 ≠ 0 ⇒ DỪNG (không chạy thật), báo dev.

**Điểm dừng 3b — chạy thật**: bảng in ra = dry-run, dòng cuối "B6 kiểm sau: đạt". Lỗi giữa chừng ⇒ lô đang chạy tự rollback; chạy lại lệnh
(idempotent — đã thử: dry-run lần 2 = **0 dòng**, 21,6 s).

## 4. So khớp (chỉ đọc)

```bash
php -d memory_limit=4G artisan product-price:compare --csv=/tmp/compare.csv     # 11 s
```
**Điểm dừng 4** — bắt buộc dòng cuối **`0 lệch.`** Kết quả local: 113.484 cặp; nhóm đã chấp nhận (không tính lệch) T4 = 449,
§3.3 bù giá 0 = 23.492; "cặp HRM sinh" = 0; `owner_not_ready` = 0. ≠ 0 lệch ⇒ DỪNG, KHÔNG chạy M3, mở `compare.csv` báo dev
(quyết lui bằng bước 7 hay sửa dữ liệu rồi chạy lại 3–4).

## 5. M3 — ép NOT NULL + UNIQUE

```bash
php artisan migrate --force          # chỉ còn M3 đang chờ — 20,5 s (lệnh 21,7 s)
```
**Kiểm schema (điểm dừng 5):**
- `product_unit_prices.company_id bigint unsigned NOT NULL`, `UNIQUE product_unit_prices_unit_company_type_unique (product_unit_id, company_id, price_type_id)`, FK `companies`.
- `product_company_units`: UNIQUE `(product_unit_id, company_id)`, index `(company_id, product_id)`, 3 FK.
- Số dòng sau (local): `upp` **789.765** (0 NULL) · `pcu` **133.101** · `pcc` có status **113.484** · `pep` **101.290** — trùng y hệt
  `hrm_erp_giacty` (bản dev dùng suốt G3–G6).
- `php artisan migrate:status | grep -c "| No"` = 0.

## 6. Quyền + mở lại

1. Quyền HRM — **KHÔNG chạy `PermissionsTableSeeder`** (truncate cả bảng). Chạy seeder riêng (hrm-api, commit `5b327e085`):
   ```bash
   php artisan db:seed --class="Modules\MasterData\Database\Seeders\ProductPricePermissionSeeder" --force
   ```
   Chèn đúng 2 dòng `permissions` **1657** "Cập nhật giá bán hàng hoá" + **1658** "Duyệt giá bán hàng hoá" (guard api, nhóm Hàng hoá,
   **type 8**). Idempotent: đã có đúng tên ⇒ "chèn 0 dòng" (thử trên `hrm_erp_giacty`: 0 dòng, 0,7 s, checksum 3 bảng quyền không đổi;
   DB thiếu quyền: PHPUnit trong transaction chèn đúng 2, chạy lại 0). id hoặc tên đã bị quyền khác chiếm ⇒ lỗi, KHÔNG ghi gì ⇒ DỪNG báo dev.
   **Không gán role nào** (kể cả Super admin 18 — không có quyền mặc định): sau triển khai quản trị gán cho role nghiệp vụ theo công ty.
2. `php artisan permission:cache-reset` (HRM) + `php artisan cache:clear` nếu cần; ERP `php artisan config:clear && php artisan route:clear && php artisan view:clear`.
3. `php artisan up` cả 2 app; bật lại 2 cron ERP.
4. Khói (5 phút): HRM `/finance/product-prices` (lọc 1 mã, 4 công ty khác giá) · `/finance/product-price-approvals` mở được ·
   ERP `/admin/products/editPrices` + `/admin/products/approvePrices` ⇒ trang "Chức năng đã chuyển sang HRM" 1 link đúng ·
   popup chọn hàng ở 1 báo giá ERP ra giá đúng công ty người dùng.

**Tổng thời gian kỹ thuật (đo local, không tính sao lưu): ≈ 2 phút** (M1+M2 6 s · dry-run 6 s · backfill 71 s · compare 11 s · M3 22 s);
cộng sao lưu ~12,5 phút + khói ⇒ dự trù **cửa sổ bảo trì 30–45 phút** (production chậm hơn local thì nhân theo tỉ lệ đo bước 1).

## 7. Lui (rollback)

Không có lui bằng code (đã bỏ cờ). Khi bất kỳ điểm dừng 3a/3b/4/5 hỏng mà không sửa được trong cửa sổ, hoặc lỗi nghiêm trọng sau khi mở:
1. `php artisan down` 2 app, dừng cron.
2. Khôi phục bản sao lưu bước 1: `gunzip < backup_….sql.gz | mysql <db>` (thời gian ≈ thời gian dump; local 12,5 phút cho cả dump + nạp).
3. Deploy lại code release TRƯỚC (cả hrm-api, hrm-client, ERP — code mới bắt buộc có `company_id`, không chạy được trên DB cũ).
4. Kiểm 5 số dòng ở bước 1 khớp, mở lại.
⚠️ Mọi giá/ chứng từ ghi sau lúc mở lại (bước 6) sẽ mất khi khôi phục ⇒ chỉ lui trong cửa sổ bảo trì / ngay trong ngày.

## Nhật ký chạy thử (10/10/2026, local)

| Bước | Lệnh | Thời gian | Kết quả |
|---|---|---:|---|
| Sao chép | `mysqldump --single-transaction … hrm_erp \| mysql hrm_erp_runbook` | 750 s | 1.869 bảng, 5 bảng giá đếm khớp gốc |
| (chỉ local) lùi M2, M1 | `migrate:rollback --step=2` | 3,2 s | batch còn 429 |
| M1 / M2 | `migrate --path=…` | 1,1 s / 5,3 s | |
| M3 thử sớm | `migrate --path=…000004…` | 0,6 s | tự chặn, không đổi gì |
| dry-run | | 6,2 s | bảng mục 3, TỔNG 1.042.374 |
| backfill | | 71,4 s | = dry-run, B6 đạt |
| compare | | 11,3 s | **0 lệch** (T4 449 · §3.3 23.492) |
| dry-run lần 2 | | 21,6 s | 0 dòng (idempotent) |
| M3 | `migrate` | 21,7 s | schema + số dòng = `hrm_erp_giacty` |
| Dọn | `DROP DATABASE hrm_erp_runbook` | | `hrm_erp` gốc không đổi (batch max 431, pcu 0) |
