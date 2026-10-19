# Runbook triển khai — Giá theo công ty (một lần, cùng đợt lên production của cả feature)

> Viết 10/10/2026 (G6) sau khi **chạy thử trọn** trên bản sao tạm `hrm_erp_runbook` (dump `--single-transaction` từ `hrm_erp` local,
> code nhánh chung hrm-api `feat/chuyen-doi-hang-hoa` + G6, MySQL 8.0.43, MacBook local). Bản sao đã DROP sau khi chạy.
> Không cờ, không đường lui bằng code (design "Đổi 10/10/2026 — BỎ CỜ"): **cách lui duy nhất = khôi phục bản sao lưu bước 1**.
> Bối cảnh 10/10: PTG (Phase 7) + hàng tạm (Phase 6) cũng chuyển HRM trong cùng lần cập nhật ⇒ lên cùng lúc, không giai đoạn tạm.
>
> ⚠️ **Đổi 15/10/2026 — luật chép giá mới** (mục 3.0): nhóm chia sẻ **1·3·4**, công ty tự quản **2·7**. Mọi số đo 10/10–12/10 trong
> file này (bảng 3a cũ, mục 4, mục 5, 2 nhật ký) là của **luật cũ 1-2-3-4**; số dùng để đối chiếu từ nay là bảng 3a mới.
>
> ⚠️ **Đổi 15/10 (lần 2, N128): HP vào nhóm chia sẻ 1·2·3·4; tự quản chỉ còn 7.** Luật hiện hành
> TRÙNG luật cũ 1-2-3-4 (Cty 7 chỉ B1–B4) ⇒ đối chiếu lại bảng **luật cũ** (TỔNG ~1,04 triệu); bảng "luật mới" 810.016 ở 3a là của
> luật lần 1, ĐÃ CŨ.

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
### 3.0 Luật chép (đổi 15/10/2026 — lần 2 cùng ngày, N128)

> **Đổi 15/10 (lần 2, N128): HP vào nhóm chia sẻ 1·2·3·4; tự quản chỉ còn 7.** Lý do: `n128-do-chung-tu-hp.md` (HP 668 chứng từ dở, 100% có hàng
> chủ 1/3/4; tự quản ⇒ HP còn 0/408 mã có giá).

Config `hrm-api/config/price.php` (thay khoá cũ `cluster_company_ids` [1,2,3,4]):
- `shared_price_company_ids` = **[1, 2, 3, 4]** — Tân Phát · Hải Phòng · Vinh · Sài Gòn chép LẪN NHAU mọi hàng đang bán (B5): giá × hệ số của công
  ty NHẬN, không có hệ số ⇒ 1 (giá bằng).
- `self_managed_company_ids` = **[7]** — ETEK Green chỉ dùng hàng mình LÀM CHỦ: vẫn qua B1–B4 (gán chủ dòng giá, pcu
  chủ, bù loại giá, Đang kinh doanh). KHÔNG nhận hàng chép, KHÔNG cho hàng của mình sang nhóm.
- 5 · 6 · 8: không dùng phần mềm ⇒ không chép, không so khớp. Hàng chủ 5/6/8 (nếu có — đo 15/10: **0 mã**) vẫn qua B1–B4 như cũ,
  vì B1 phải gán công ty cho mọi dòng giá thì M3 NOT NULL mới chạy. Hàng `company_id` NULL vẫn gán theo tiền tố (`SG-` ⇒ 4), không
  xác định được ⇒ B0 `owner_unknown` dừng (như cũ).
- Vẫn backfill MỘT lần ngày chuyển đổi (T2 không đổi). Bảng in của lệnh luôn có cột Cty 1·2·3·4·7.

**Điểm dừng 3a — dry-run** — **Đổi 15/10 (lần 2, N128): HP vào nhóm chia sẻ 1·2·3·4; tự quản chỉ còn 7.** Bảng ngay dưới là **luật lần 1 (1·3·4 / 2·7), ĐÃ CŨ**; luật hiện hành
= luật cũ 1-2-3-4 ⇒ dry-run phải khớp số **luật cũ đo 15/10: TỔNG 1.042.371** (cột Cty 2 ≈ 232 nghìn; chi tiết từng việc như bảng
10/10 trong khung "Bảng 3a cũ" bên dưới, chênh vài dòng `pep.copy` do ngày chạy). `hrm_erp_giacty` (đã backfill luật cũ) đo 15/10
bằng code lần 2: dry-run **TỔNG GHI 0**.

*Bảng luật lần 1 (ĐÃ CŨ — chỉ tra lịch sử)* (đo `hrm_erp` local 15/10 — DB chưa backfill, chỉ dry-run, không ghi;
production đo lại, chênh do dữ liệu mới thì đối chiếu §3.4 design):

| Việc | Cty 1 | Cty 2 | Cty 3 | Cty 4 | Cty 7 | Tổng |
|---|---:|---:|---:|---:|---:|---:|
| B0 kiểm trước | `orphan_upp 0, owner_unknown 0, duplicates 0, pcu_foreign 0` | | | | | |
| upp.assign (B1) | 258.270 | 18 | 138 | 6.220 | 0 | 264.646 |
| pcu.owner (B2) | 45.477 | 3 | 23 | 1.057 | 0 | 46.560 |
| upp.fill (B3) | 5.765 | 0 | 0 | 108 | 0 | 5.873 |
| pcc.owner insert/update (B4) | 27.370 | 3 | 14 | 980 + 4 | 0 | 28.371 |
| pcu.copy (B5) | 1.007 | 0 | 28.821 | 27.860 | 0 | 57.688 |
| upp.copy (B5) | 6.042 | 0 | 172.926 | 167.160 | 0 | 346.128 |
| pep.copy (B5) | 32 | 0 | 2.007 | 1.975 | 0 | 4.014 |
| pcc.recv insert/update (B5) | 998 | 0 | 27.972 + 382 | 27.361 + 23 | 0 | 56.736 |
| **TỔNG GHI** | 344.961 | **24** | 232.283 | 232.748 | 0 | **810.016** |
| info: giá đổi số vì hệ số ≠ 1 | 0 | 0 | 1.332 | 90 | 0 | 1.422 |

So với luật cũ đo cùng ngày 15/10 (code cũ, cùng DB: TỔNG 1.042.371): bớt 232.355 dòng (toàn bộ phần chép VÀO Cty 2 + 3 mã HP chép ra 1/3/4: pcu 3 · upp 18 mỗi công ty nhận). `pep.copy`
lệch 1–3 dòng so với 10/10 vì phụ thuộc ngày chạy (chỉ chép giá hiệu lực > hôm nay). Số sau backfill dự kiến (= trước + ghi):
`upp` **616.647** · `pcu` **104.248** · `pcc` có status **85.107** · `pep` ≈ **99.280**.

<details><summary>Bảng 3a cũ — <b>luật cũ 1-2-3-4</b> (số local 10/10, chỉ để tra lịch sử)</summary>

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

</details>

B0 ≠ 0 ⇒ DỪNG (không chạy thật), báo dev.

**Điểm dừng 3b — chạy thật**: bảng in ra = dry-run, dòng cuối "B6 kiểm sau: đạt". Lỗi giữa chừng ⇒ lô đang chạy tự rollback; chạy lại lệnh
(idempotent — đã thử: dry-run lần 2 = **0 dòng**, 21,6 s).

## 4. So khớp (chỉ đọc)

```bash
php -d memory_limit=4G artisan product-price:compare --csv=/tmp/compare.csv     # 11 s
```
**Điểm dừng 4** — bắt buộc dòng cuối **`0 lệch.`** Luật hiện hành (Đổi 15/10 (lần 2, N128): HP vào nhóm chia sẻ 1·2·3·4; tự quản chỉ còn 7.): cặp cần có giá = (hàng × chủ)
cho chủ thuộc 1·2·3·4·7 + (hàng × công ty nhận) khi chủ và nhận cùng thuộc 1·2·3·4; ETEK Green thiếu hàng chép KHÔNG phải lệch. Đo
15/10 (lần 2) trên `hrm_erp_giacty` (chỉ đọc): **113.484 cặp, 0 lệch**, T4 = 449, §3.3 = 23.492, cặp HRM = 0, `owner_not_ready` = 0
— đúng bằng số luật cũ 10/10. *(Luật lần 1, ĐÃ CŨ: 85.107 cặp, T4 = 229, §3.3 = 17.619.)*
*Luật cũ 1-2-3-4 (10/10):* 113.484 cặp; nhóm đã chấp nhận (không tính lệch) T4 = 449,
§3.3 bù giá 0 = 23.492; "cặp HRM sinh" = 0; `owner_not_ready` = 0. ≠ 0 lệch ⇒ DỪNG, KHÔNG chạy M3, mở `compare.csv` báo dev
(quyết lui bằng bước 7 hay sửa dữ liệu rồi chạy lại 3–4).

## 5. M3 — ép NOT NULL + UNIQUE

```bash
php artisan migrate --force          # chỉ còn M3 đang chờ — 20,5 s (lệnh 21,7 s)
```
**Kiểm schema (điểm dừng 5):**
- `product_unit_prices.company_id bigint unsigned NOT NULL`, `UNIQUE product_unit_prices_unit_company_type_unique (product_unit_id, company_id, price_type_id)`, FK `companies`.
- `product_company_units`: UNIQUE `(product_unit_id, company_id)`, index `(company_id, product_id)`, 3 FK.
- Số dòng sau (local, **luật cũ 1-2-3-4**; luật mới xem cuối mục 3a): `upp` **789.765** (0 NULL) · `pcu` **133.101** · `pcc` có status **113.484** · `pep` **101.290** — trùng y hệt
  `hrm_erp_giacty` (bản dev dùng suốt G3–G6).
- `php artisan migrate:status | grep -c "| No"` = 0.

## 6. Quyền + mở lại

> ⚠️ **Đổi 15/10 (N138) — đoạn quyền dưới đây ĐÃ CŨ.** Seeder gộp nay đồng bộ theo TÊN, không truncate; mọi quyền của luồng đã khai trong `PermissionsTableSeeder` ⇒ thay toàn bộ các lệnh seeder riêng / INSERT theo id bằng `php artisan permission:sync --dry-run` rồi `php artisan permission:sync` (chi tiết `../deploy-dev-server.md` §7). Chạy seeder riêng cũ trên DB đã sync sẽ DỪNG "tên đã có ở id khác".

1. Quyền HRM — **KHÔNG chạy `PermissionsTableSeeder`** (truncate cả bảng). Chạy seeder riêng (hrm-api, commit `5b327e085`):
   ```bash
   php artisan db:seed --class="Modules\MasterData\Database\Seeders\ProductPricePermissionSeeder" --force
   ```
   Chèn đúng 2 dòng `permissions` **1657** "Cập nhật giá bán hàng hoá" + **1658** "Duyệt giá bán hàng hoá" (guard api, nhóm Hàng hoá,
   **type 8**). Idempotent: đã có đúng tên ⇒ "chèn 0 dòng" (thử trên `hrm_erp_giacty`: 0 dòng, 0,7 s, checksum 3 bảng quyền không đổi;
   DB thiếu quyền: PHPUnit trong transaction chèn đúng 2, chạy lại 0). id hoặc tên đã bị quyền khác chiếm ⇒ lỗi, KHÔNG ghi gì ⇒ DỪNG báo dev.
   **Không gán role nào** (kể cả Super admin 18 — không có quyền mặc định): sau triển khai quản trị gán cho role nghiệp vụ theo công ty.
   **Đợt 2-E (Excel hàng hoá)** — thêm 1 seeder riêng cùng khuôn, chạy ngay sau seeder giá:
   ```bash
   php artisan db:seed --class="Modules\MasterData\Database\Seeders\ProductExportPermissionSeeder" --force
   ```
   Chèn đúng 1 dòng **1654** "Xuất excel danh sách hàng hoá" (guard api, nhóm Hàng hoá, **type 9** như 1652/1653/1655). Idempotent
   (đã có đúng tên ⇒ "chèn 0 dòng"; thử trên `hrm_erp_giacty` 14/10: lượt 1 chèn 1654, lượt 2 chèn 0, 0 dòng `role_has_permissions`).
   id/tên bị quyền khác chiếm ⇒ lỗi, không ghi gì ⇒ DỪNG báo dev. **Không gán role nào** — quản trị gán cho role cần xuất Excel
   (mọi nút Xuất Excel 5 màn hàng hoá dùng chung quyền này, thiếu là nút ẩn + API 403).
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
| dry-run | | 6,2 s | bảng mục 3 (luật cũ 1-2-3-4), TỔNG 1.042.374 |
| backfill | | 71,4 s | = dry-run, B6 đạt |
| compare | | 11,3 s | **0 lệch** (T4 449 · §3.3 23.492) |
| dry-run lần 2 | | 21,6 s | 0 dòng (idempotent) |
| M3 | `migrate` | 21,7 s | schema + số dòng = `hrm_erp_giacty` |
| Dọn | `DROP DATABASE hrm_erp_runbook` | | `hrm_erp` gốc không đổi (batch max 431, pcu 0) |

---

# Phần 2 — Luồng tính giá (Phase 7) — chạy NGAY SAU bước 6.1 ở trên, trong cùng cửa sổ bảo trì

> Viết 12/10/2026 (T7, `luong-tinh-gia/design.md` §11) sau khi **chạy thử trọn cả 2 phần** trên bản sao tạm `hrm_erp_runbook7`
> (sao từ `hrm_erp` local, code nhánh chung hrm-api `1e194fe5c`; ERP `feat/2d1-erp-khong-loi` `443c812553`). Bản sao đã DROP.
> Lui: như mục 7 (khôi phục bản sao lưu bước 1 — cùng điểm lui với phần 1).

## 8. Trước 7 ngày (T-7) — dọn phiếu dở ở ERP

Chạy trên production (chỉ đọc), gửi danh sách cho PTKD / XNK / Kế toán mua hàng xử lý xong **ở ERP** (duyệt nốt, tính nốt, huỷ, không có giá):
```sql
-- phiếu dở theo trạng thái (YCHG · YCTG · PTG · chéo công ty)
SELECT a.status ychg, r.status yctg, c.status ptg, (a.company_id<>a.send_company_id) cheo, COUNT(*)
FROM price_asking_requests a
LEFT JOIN price_calculate_requests r ON r.price_asking_request_id=a.id
LEFT JOIN price_calculates c ON c.price_calculate_request_id=r.id
WHERE a.status NOT IN (4) GROUP BY 1,2,3,4;
-- (D1) phiếu hỏi CHÉO công ty còn dở — PHẢI = 0 mới deploy
SELECT COUNT(DISTINCT a.id) FROM price_asking_requests a
WHERE a.status IN (1,2,5,7) AND a.send_company_id IS NOT NULL AND a.company_id<>a.send_company_id;
```
Đo local 12/10: chéo dở **30** (dữ liệu local chưa dọn — production phải về 0).

## 9. Ngày triển khai (sau bước 6.1 phần 1)

| # | Việc | Lệnh | Đạt khi | Đo local 12/10 |
|---|---|---|---|---|
| 9.1 | Kiểm trùng trước UNIQUE (chỉ đọc) | `SELECT COUNT(*) FROM (SELECT price_calculate_request_id FROM price_calculates GROUP BY 1 HAVING COUNT(*)>1) x;` · tương tự `price_calculate_results` theo `price_calculate_id` · lại SQL D1 ở mục 8 | trùng = **0**, chéo dở = **0** | trùng 0 / 0 · phiếu thiếu hãng 20 (backfill tự lấy hãng dòng đầu) |
| 9.2 | 12 migration Phase 7 (theo thứ tự tên file) | `php artisan migrate --force` (lúc này chỉ còn 12 file `2026_10_11_*` đang chờ — kiểm `migrate:status` trước) | `migrate:status \| grep "\| No"` rỗng | mỗi file 0,4–0,7 s; tổng ≈ 6 s. M6/M8 tự kiểm trùng, có trùng thì dừng kèm danh sách id |
| 9.3 | Quyền — ⚠️ CŨ, thay bằng `php artisan permission:sync` (N138, xem §7 deploy-dev-server.md) | `php artisan db:seed --force --class="Modules\MasterData\Database\Seeders\InternalPricePolicyPermissionSeeder"` rồi `…\PriceCalculationPermissionSeeder` | chèn **1656** + **1662 · 1663 · 1664**; chạy lại "chèn 0 dòng" | 0,4 s mỗi lệnh; chạy lại 0 dòng |
| 9.4 | Backfill nhóm YCHG — dry-run | `php artisan price-asking:backfill-groups --dry-run` | số khớp bảng dưới (production đo lại) | 1,8 s |
| 9.5 | Backfill nhóm — chạy thật | `php artisan price-asking:backfill-groups` | = dry-run | 5,8 s |
| 9.6 | Kiểm idempotent | `php artisan price-asking:backfill-groups --dry-run` | **0** mọi dòng | 0 |
| 9.7 | Đóng nhóm cũ dở — dry-run | `php artisan price-asking:close-stale --before=2026-06-01 --dry-run` | xem số, "CHƯA backfill nhóm" = 0 | 45 nhóm / 45 phiếu (st1 10 · st5 13 · st7 22); 22 nhóm có YCTG, 1 có PTG nháp (giữ nguyên) |
| 9.8 | Đóng nhóm cũ — chạy thật (`--by` bắt buộc = employees.id người chạy, T3-Q6) | `php artisan price-asking:close-stale --before=2026-06-01 --by=13` | = dry-run; chạy lại dry-run = 0 | 0,4 s; lại = 0 |
| 9.9 | Deploy ERP chặn luồng tính giá (cùng lần deploy ERP của phần 1) | ERP nhánh release có commit T7 · `php artisan config:clear && route:clear && view:clear` | `/admin/orders/price_asking_requests` ⇒ trang "Chức năng đã chuyển sang HRM" 1 link HRM | — |
| 9.10 | Gán quyền 1656 / 1662 / 1663 / 1664 cho vai trò nghiệp vụ theo công ty (quản trị) + `permission:cache-reset` | màn phân quyền HRM | PTKD / XNK / KTMH thấy menu | — |
| 9.11 | Nhắc nghiệp vụ | công ty **2 / 5 / 6 / 7 / 8 chưa có phân công XNK** ⇒ không gửi được YCHG tới khi khai phân công | — | — |

Bảng số dry-run 9.4 (local 12/10 — trùng T2 trên giacty 11/10):

| Mục | Số |
|---|---:|
| Phiếu xử lý = nhóm sinh ra | 4.029 |
| Dòng hàng gán group_id | 6.729 |
| YCTG gán group_id | 3.147 |
| Log gán group_id | 10.029 |
| YCTG bị Kế toán trả 3 ⇒ 5 | 21 |
| Hãng lấy theo dòng hàng đầu | 20 |
| Phiếu st1 đã có YCTG ⇒ nhóm 7 | 6 |
| XNK = người XNK đã duyệt / phân công công ty gửi tới / phân công công ty phiếu / không xác định | 3.530 / 435 / 26 / 38 |
| Trạng thái nhóm | NULL 548 · 1: 67 · 4: 3.119 · 5: 41 · 6: 155 · 7: 28 · 9: 71 |

**Khói phần 2 (5 phút):** HRM `/sale/price-asking-requests` (danh sách có nhóm) · `/sale/price-calculate-requests` · `/finance/price-calculates` mở được;
1 YCHG cũ đã tính giá ⇒ nhóm "Đã tính giá", bấm "In kết quả" ra KQ · ERP `/admin/orders/price_calculates` ⇒ trang báo 1 link HRM ·
trang chủ ERP không còn 3 thẻ Yêu cầu hỏi giá / tính giá chờ duyệt.

**Thời gian kỹ thuật phần 2 (local): ≈ 15 s** (migrate 6 s · seed 1 s · backfill nhóm 8 s · close-stale 1 s). Tổng 2 phần ≈ 2,5 phút + sao lưu.

## Nhật ký chạy thử phần 1 + 2 (12/10/2026, local, `hrm_erp_runbook7`)

| Bước | Thời gian | Kết quả |
|---|---:|---|
| Sao chép `hrm_erp` ⇒ `hrm_erp_runbook7` (`mysqldump --single-transaction … \| mysql`) | 505 s | 1.869 / 1.869 bảng |
| (chỉ local) `migrate:rollback --step=2` | 1,5 s | còn chờ đúng 15 migration của feature (M1–M3 + 12 Phase 7) |
| M1 / M2 | 0,5 s / 2,2 s | |
| backfill giá dry-run / thật | 5,9 s / 46,4 s | **TỔNG GHI 1.042.374** (luật cũ 1-2-3-4) = dry-run = lần 10/10; B0 = 0; B6 đạt |
| compare | 13,1 s | **0 lệch** (§3.3 23.492) |
| M3 | 13,7 s | |
| seed 1657/1658 | 1,7 s | chèn 2 |
| kiểm 9.1 | 0,5 s | trùng 0 / 0 · chéo dở 30 (local) · thiếu hãng 20 |
| 12 migration Phase 7 (`--path` từng file) | ≈ 6 s | đều đạt |
| seed 1656 / 1662–1664 / chạy lại | 0,4 / 0,4 / 0,3 s | 1 / 3 / 0 dòng |
| backfill nhóm dry / thật / dry lại | 2,2 / 6,2 / 0,4 s | 4.029 nhóm = bảng 9.4; lại 0 |
| close-stale dry / thật `--by=13` / dry lại | 0,4 × 3 s | 45 / 45 / 0 |
| Cuối | | `migrate:status` 0 chờ · batch 444 · `upp` 789.765 · `pcu` 133.101 · nhóm 4.029 · đủ 6 quyền |
| Dọn | | `DROP DATABASE hrm_erp_runbook7`; `hrm_erp` gốc không đổi (batch 431, `upp` 264.646, `pcu` 0, chưa có bảng nhóm) |

---

# Phần 3 — Hàng tạm (Phase 6) — cùng cửa sổ bảo trì

- **Không migration, không seeder, không quyền mới.** Trạng thái hàng tạm 6/7/8 nằm ở cột `product_company_coefficients.status` có sẵn.
- **ĐIỀU KIỆN CHẶN GO-LIVE (nghiệp vụ):** nhập cây phân loại (Tính chất · Nhóm chức năng · Nhóm SP · Loại SP) + danh mục **Đặc tính** — local đo 12/10: Loại SP 0, Đặc tính 0 ⇒ không tạo được hàng hoá/hàng tạm (`viec-con-lai.md` B5, B6).
- Trước ngày chuyển: dọn hàng tạm ERP đang **chờ duyệt** (`tmp_products.status = 2`, local 1 dòng) ở ERP (duyệt nốt hoặc từ chối).
- Deploy ERP chặn hàng tạm (Phase 6 T8) cùng lần deploy ERP của phần 1–2; `config:clear && route:clear && view:clear`.
- Gán quyền PTKD duyệt YCHG (1662) như phần 2 — PTKD duyệt hàng tạm bằng chính quyền này.
- Khói: HRM `/master-data/products/temp` mở được; YCHG có nút "Thêm hàng tạm"; ERP `/admin/tmp_products/{id}/edit` ⇒ trang "Chức năng đã chuyển sang HRM".

---

> 🆕 17/10/2026: cron áp giá hiệu lực CHUYỂN SANG HRM (`product-price:apply-expected`, chốt chặn theo công ty) — ERP bỏ lịch `product:update_price`.
> Các bước kiểm cron 4.3 dưới đây thay bằng `cron-gia-hieu-luc/design.md` §7.

# Phần 4 — Dữ liệu cũ ERP (C-f: N65 giá hiệu lực quá hạn + cờ mồ côi, N26 AUTO_INCREMENT) — cùng cửa sổ bảo trì

> ⛔ **THỨ TỰ BẮT BUỘC:** cron `product:update_price` bản mới áp `effect_date <= hôm nay`. Chưa dọn mà cron chạy thì nó sẽ áp
> **13.909** giá cũ (đo giacty 13/10, có dòng giá 1,00 đ). Cron đã có **chốt chặn**: còn dòng chờ quá 30 ngày ⇒ dừng, không áp gì,
> log "chạy price:cleanup-stale trước" — nhưng vẫn phải làm 4.2 NGAY sau deploy ERP, trước 01:00.

### 4.1 N26 — `product_versions` AUTO_INCREMENT (chỉ đọc + chỉnh nếu cần)
```sql
SELECT MAX(product_version_id) FROM product_histories;                     -- (A) local 175.610 (59.710 dòng mồ côi — GIỮ, Q-N26)
SELECT AUTO_INCREMENT FROM information_schema.tables
 WHERE table_schema = DATABASE() AND table_name = 'product_versions';      -- (B) local 176.616
-- Chỉ khi (B) <= (A):
ALTER TABLE product_versions AUTO_INCREMENT = <(A) + 1>;
```
Lý do: `product_histories` có `product_version_id` trỏ version đã xoá; nếu AI của `product_versions` cấp lại đúng id đó thì lịch sử cũ
dính vào version mới (sai lặng lẽ).

### 4.2 N65 — dọn giá hiệu lực quá hạn + cờ chờ duyệt mồ côi (ERP, Q-N65 user chốt 13/10)
```bash
php artisan price:cleanup-stale --dry-run      # đếm + xuất storage/app/price-cleanup/<ts>-dry-run/gia-qua-han-<năm>.csv
# ⇒ gửi gia-qua-han-<năm>.csv cho nghiệp vụ soát (dòng năm hiện tại; local 2.067)
php artisan price:cleanup-stale                # sao lưu CSV từng bảng TRƯỚC khi ghi, rồi ghi trong 1 transaction
php artisan price:cleanup-stale --dry-run      # kiểm: mọi nhóm = 0
```
- Giá hiệu lực `status 2` quá ngày ⇒ `status 3` (đóng, KHÔNG áp, giá không đổi). Local: 13.915 dòng.
- Cờ chờ duyệt không còn yêu cầu duyệt nào ⇒ cờ 0, số đề nghị = số đang chạy. Local: `product_unit_prices` 5 · `product_company_units` 6 · `product_units` 6.
- Lui: cập nhật lại từ `backup-*.csv` theo `id` (file nằm cùng thư mục, giữ ít nhất 30 ngày).

### 4.3 Kiểm cron
- `php artisan product:update_price <hôm nay>` (hoặc chờ 01:00) ⇒ log không có dòng "Dừng: còn … chưa dọn"; `price_logs` có bản ghi nếu có giá tới hạn.

### Nhật ký chạy thử (13/10/2026, local — bản sao `hrm_erp_cf_tmp` 13 bảng chép từ giacty, đã DROP)
| Bước | Kết quả |
|---|---|
| dry-run | 13.915 quá hạn (2026: 2.067) · cờ mồ côi 5 / 6 / 6 |
| thật | sao lưu 13.915 / 5 / 6 / 6 dòng + `gia-qua-han-2026.csv` 2.067 dòng; status 3 = 13.915, 2 = 8.078 (tương lai), 1 = 79.297 |
| dry-run lại | 0 / 0 / 0 / 0 |
| cron 13/10 trên bản sao | "Đã chạy cron và không có thay đổi giá!" (chốt chặn 0) |
| chốt chặn trên giacty CHƯA dọn | 13.468 dòng chờ quá 30 ngày ⇒ cron dừng |
| giacty | không ghi (status 2 vẫn 21.993) |
