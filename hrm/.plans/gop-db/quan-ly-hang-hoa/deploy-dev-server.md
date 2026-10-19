# Deploy nhánh Chuyển đổi hàng hoá — VPS dev / dev server (viết lại 17/10/2026)

> 1 hướng dẫn duy nhất, theo commit nhánh chung mới nhất. Bản production đầy đủ: `gia-theo-cong-ty/runbook-trien-khai.md` + `cron-gia-hieu-luc/design.md` §7.
> ERP và HRM dùng **chung 1 DB gộp** ⇒ migration / backfill chạy MỘT lần ở hrm-api; ERP chỉ cần code + `.env` + 1 lệnh dọn giá.
> ⚠️ KHÔNG merge vào `gop_db`: server checkout thẳng nhánh feature.
> Nhãn: **[HRM-API]** thư mục hrm-api · **[HRM-CLIENT]** · **[ERP]** · **[DB]** SQL trực tiếp · **[CRON]** crontab máy chủ.

| Repo | Nhánh | Commit (đã push 17/10/2026) |
|---|---|---|
| hrm-api | `feat/chuyen-doi-hang-hoa` | `518cb1b62` (18/10: + người nhận thông báo theo quyền — không migration) |
| hrm-client | `feat/chuyen-doi-hang-hoa` | `963cd8887` |
| ERP | `feat/2d1-erp-khong-loi` | `226a62c0b7` |

Sau mỗi `git pull`: `git rev-parse --short HEAD` phải khớp bảng.

**Có gì mới so với bản 15/10:** luật chép giá lần 2 (Hải Phòng vào nhóm chia sẻ) · đợt lỗi SRS 16/10 · điều kiện thanh toán HĐ (merge `develop`) ·
tick bỏ mã ở YC tính giá / Phiếu tính giá · **cron áp giá hiệu lực chạy ở HRM** (ERP bỏ lịch `product:update_price`, khoá màn Nhật ký giá ERP) +
màn Tài chính › Nhật ký áp giá.

## 0. [DB] Chọn lối
```sql
SHOW TABLES LIKE 'product_company_units';
SELECT COUNT(*) FROM product_unit_prices WHERE company_id IS NOT NULL;
```
- Bảng có dữ liệu + COUNT > 0 ⇒ DB **đã backfill** (VPS test đã deploy 15/10) ⇒ **Lối A** (cập nhật).
- Chưa có bảng / 0 dòng / lỗi "Unknown column" ⇒ DB **chưa từng chạy** ⇒ **Lối B** (đầy đủ).
- Backfill theo luật CŨ (Cty 2 không có giá chép từ Cty 1/3/4) ⇒ nạp lại DB từ bản chưa backfill rồi đi Lối B.

---

# Lối A — VPS đã deploy bản 15/10 (cập nhật)

## A1. [DB] Sao lưu
```bash
mysqldump --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF <db> | gzip > backup_<db>_$(date +%F_%H%M).sql.gz
```

## A2. Lấy code
```bash
# [ERP]
git fetch origin && git checkout feat/2d1-erp-khong-loi && git pull
composer install --no-dev -o
php artisan config:clear && php artisan route:clear && php artisan view:clear

# [HRM-API]
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull
composer install --no-dev -o
php artisan config:clear && php artisan route:clear

# [HRM-CLIENT]  (node 12)
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull
npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build
# restart Nuxt (pm2 …)
```
Kiểm ERP: `grep -n "product:update_price" app/Console/Kernel.php` ⇒ chỉ còn dòng chú thích (lịch áp giá đã chuyển sang HRM).

## A3. [HRM-API] Migration + seeder
```bash
php artisan migrate:status | grep "| No"          # xem trước danh sách chờ
php artisan migrate --force
php artisan migrate:status | grep -c "| No"       # = 0
php artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder" --force   # 8 điều kiện thanh toán (chạy lại không nhân đôi)
php artisan queue:restart                          # thông báo app đi qua job SendNotification — bỏ qua nếu QUEUE_CONNECTION=sync
```
Trong danh sách chờ phải có (cùng các migration của `develop` / `gop_db` từ 15/10):
`2026_10_13_000001_rename_luong_p3_to_dinh_muc_thuong_p3` · `2026_10_16_000001/000002` (điều kiện thanh toán) ·
`2026_10_17_000001_add_unchosen_reason_to_price_calculate_lines` · `2026_10_17_100001_create_product_price_apply_logs_table`.

## A4. Quyền
```bash
php artisan permission:sync --dry-run      # đọc như mục B7; có "tên đã có ở id khác" / lỗi ⇒ DỪNG báo dev
php artisan permission:sync
php artisan permission:sync --dry-run      # = 0 thay đổi
php artisan permission:cache-reset         # KHÔNG cache:clear (redis chung ERP)
```
Gán thêm: **[ERP]** quyền "Xem phiếu yêu cầu đặt hàng trong nước theo tổng công ty" cho vai trò cần xem (N160 — Super Admin không còn được qua thẳng).
Màn "Nhật ký áp giá" dùng quyền có sẵn (bảng B10) — không gán gì mới.

## A5. [DB] Chốt chặn cron áp giá (công ty còn giá chờ > 30 ngày sẽ bị cron BỎ QUA)
```sql
SELECT upp.company_id, COUNT(*) FROM product_expected_prices pep
JOIN product_unit_prices upp ON upp.id = pep.unit_price_id
WHERE pep.status = 2 AND (pep.flag <> 1 OR pep.flag IS NULL) AND pep.effect_date < CURDATE() - INTERVAL 30 DAY
GROUP BY upp.company_id;
```
- Rỗng ⇒ sang A6 (VPS đã dọn N65 ngày 15/10).
- Có dòng ⇒ **[ERP]** chạy bước B9 (`price:cleanup-stale`), hoặc để nghiệp vụ xử lý ở HRM Tài chính › Nhật ký áp giá › tab "Giá quá hạn chưa áp".

## A6. [CRON] HRM có `schedule:run`
```bash
sudo crontab -u www-data -l | grep schedule:run      # cả crontab user deploy — phải có 1 dòng trỏ thư mục hrm-api
# thiếu thì thêm (user chạy web):
# * * * * * cd <HRM_API_DIR> && php artisan schedule:run >> /dev/null 2>&1
cd <HRM_API_DIR> && php artisan schedule:list | grep apply-expected     # 0 1 * * *  product-price:apply-expected
```
Crontab ERP giữ nguyên (`schedule:run` ERP vẫn chạy các cron khác).

## A7. Chạy thử cron áp giá (ghi DB thật — VPS dev chấp nhận)
```bash
cd <HRM_API_DIR> && sudo -u www-data php artisan product-price:apply-expected
```
In bảng theo công ty: "Đã áp" / "Bỏ qua — còn N giá chờ quá 30 ngày" / "LỖI …"; không có gì ⇒ "không có giá hiệu lực nào cần áp".
```sql
SELECT company_id, action, COUNT(*) FROM product_price_apply_logs GROUP BY company_id, action;   -- 1 Tự áp · 2 Áp ngay · 3 Đóng
SELECT upp.company_id, COUNT(*) FROM product_expected_prices pep JOIN product_unit_prices upp ON upp.id = pep.unit_price_id
WHERE pep.status = 2 AND pep.effect_date <= CURDATE() AND (pep.flag <> 1 OR pep.flag IS NULL) GROUP BY upp.company_id;
-- chỉ còn công ty bị chặn ở A5
```

## A8. Khói ⇒ mục "Khói chung" cuối file.

---

# Lối B — DB chưa từng chạy (đầy đủ)

## B1. [DB] Sao lưu + tạm dừng
- Sao lưu như A1.
- **[ERP]** tắt cron `product:reset_price_when_zero_inventory` (14:30) tới hết B9. **[CRON]** tạm comment dòng `schedule:run` của **HRM**
  (cron áp giá hiệu lực 01:00 ở HRM) tới hết B9 — hoặc làm trọn B1–B9 trước 01:00. (Lịch `product:update_price` ERP đã bỏ trong code.)
- **[ERP] + [HRM-API]** `php artisan down` (nếu có người đang dùng).

## B2. Lấy code — như A2.

## B3. [ERP] `.env` rồi clear cache
```
HRM_URL_FE=<url hrm-client>        # link "Chức năng đã chuyển sang HRM", xem chi tiết hàng hoá
HRM_URL_BE=<url hrm-api>
HRM_API_BASE_URL=<url hrm-api>     # popup chọn hàng ERP gọi API HRM
```
```bash
php artisan config:clear && php artisan route:clear && php artisan view:clear
```

## B4. [HRM-API] Migration lượt 1 — PHẢI dừng ở M3
```bash
php artisan migrate:status | grep "| No"
php artisan migrate --force
```
Đúng khi dừng ở `2026_10_09_000004_enforce_company_id_on_product_unit_prices_table` với lỗi "còn N dòng company_id NULL…"
(migration tự chặn, không đổi gì). **Chạy qua luôn ⇒ DB không phải DB mới — DỪNG, xem bước 0.**

## B5. [HRM-API] Backfill giá theo công ty
```bash
php -d memory_limit=4G artisan product-price:backfill-company --dry-run
php -d memory_limit=4G artisan product-price:backfill-company
php -d memory_limit=4G artisan product-price:compare
```
| Kiểm | Đạt khi |
|---|---|
| dry-run, dòng "B0 kiểm trước" | toàn 0 (≠ 0 ⇒ DỪNG báo dev) |
| dry-run, cột Cty 2 / Cty 7 | Cty 2 nhận chép như 3/4 (cỡ **232 nghìn** dòng, đo `hrm_erp` 15/10) · Cty 7 = 0 |
| dry-run, TỔNG GHI | cỡ **1,04 triệu** (đo `hrm_erp` 15/10: 1.042.371). Ra ~810 nghìn / Cty 2 chỉ 24 dòng ⇒ code luật cũ (HP tự quản) — DỪNG |
| chạy thật | bảng in = dry-run, dòng cuối "B6 kiểm sau: đạt" (~1–2 phút) |
| compare | dòng cuối **`0 lệch.`** |

Luật (`hrm-api/config/price.php`): **1 Tân Phát · 2 Hải Phòng · 3 Vinh · 4 Sài Gòn** chép giá lẫn nhau mọi hàng đang bán (giá × hệ số công ty nhận,
không có hệ số ⇒ giá bằng). **7 · 9** tự quản: chỉ có hàng mình làm chủ, không nhận / không cho. **5 · 6 · 8** bỏ qua.

## B6. [HRM-API] Migration lượt 2 + seeder
```bash
php artisan migrate --force
php artisan migrate:status | grep -c "| No"       # = 0
php artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder" --force
php artisan queue:restart                          # bỏ qua nếu QUEUE_CONNECTION=sync
```

## B7. Quyền
Seeder quyền gộp `PermissionsTableSeeder` **đồng bộ theo TÊN** (thêm mới, cập nhật tại chỗ, giữ id, không truncate) ⇒ **KHÔNG** chạy 4 seeder quyền riêng cũ
(`ProductPrice…`, `ProductExport…`, `InternalPricePolicy…`, `PriceCalculation…`) và **KHÔNG** INSERT tay theo id. Id trong tài liệu chỉ là nhãn — gán quyền tra theo TÊN.

**[HRM-API]**
```bash
php artisan permission:sync --dry-run   # xem trước THÊM / CẬP NHẬT; "tên đã có ở id khác" hay lỗi ⇒ DỪNG báo dev
php artisan permission:sync
php artisan permission:sync --dry-run   # = 0 thay đổi
```
**Đọc dry-run lượt đầu** — DỪNG báo dev nếu thấy:
- `Thêm: … định mức thưởng P3 …` **và** `⚠ … không khai báo: … lương P3 …` ⇒ migration `2026_10_13_000001_rename_luong_p3_to_dinh_muc_thuong_p3` CHƯA chạy (B6 chưa xong).
- `⚠ … không khai báo: Xem/Quản lý/Xoá/Xuất dữ liệu danh mục hàng hoá` ⇒ quyền rác chỉ có trên DB dev (id 1616–1619); trên prod xuất hiện ⇒ hỏi dev.

Bình thường: `Gộp trùng: … danh mục tiền tệ` · `Thêm … (giữ id cũ N)`. Id legacy bị chiếm ⇒ sync chèn id mới, không chuyển gán quyền — không sai.

**Kiểm đủ 73 quyền của luồng theo TÊN — rỗng = đủ:**
```sql
-- Quyền luồng Chuyển đổi hàng hoá CHƯA có trên DB (rỗng = đủ)
SELECT c.name FROM (
SELECT 'Xem giá vốn hàng hoá' AS name
UNION ALL SELECT 'Quản lý danh mục lĩnh vực Công ty kinh doanh'
UNION ALL SELECT 'Xem danh mục lĩnh vực Công ty kinh doanh'
UNION ALL SELECT 'Xem danh mục tính chất hàng hóa'
UNION ALL SELECT 'Quản lý danh mục tính chất hàng hóa'
UNION ALL SELECT 'Xem danh mục nhóm chức năng'
UNION ALL SELECT 'Quản lý danh mục nhóm chức năng'
UNION ALL SELECT 'Xem danh mục nhóm sản phẩm'
UNION ALL SELECT 'Quản lý danh mục nhóm sản phẩm'
UNION ALL SELECT 'Xem danh mục loại sản phẩm'
UNION ALL SELECT 'Quản lý danh mục loại sản phẩm'
UNION ALL SELECT 'Xem danh mục chính sách kinh doanh'
UNION ALL SELECT 'Quản lý danh mục chính sách kinh doanh'
UNION ALL SELECT 'Xem danh mục đặc tính sản phẩm'
UNION ALL SELECT 'Quản lý danh mục đặc tính sản phẩm'
UNION ALL SELECT 'Xem danh mục model'
UNION ALL SELECT 'Quản lý danh mục model'
UNION ALL SELECT 'Xem danh mục code đặt hàng'
UNION ALL SELECT 'Quản lý danh mục code đặt hàng'
UNION ALL SELECT 'Xem danh mục đơn vị tính'
UNION ALL SELECT 'Quản lý danh mục đơn vị tính'
UNION ALL SELECT 'Xem danh mục thuộc tính'
UNION ALL SELECT 'Quản lý danh mục thuộc tính'
UNION ALL SELECT 'Xem danh mục đơn vị thuộc tính'
UNION ALL SELECT 'Quản lý danh mục đơn vị thuộc tính'
UNION ALL SELECT 'Xem danh mục thương hiệu'
UNION ALL SELECT 'Quản lý danh mục thương hiệu'
UNION ALL SELECT 'Xem danh mục hãng sản xuất'
UNION ALL SELECT 'Quản lý danh mục hãng sản xuất'
UNION ALL SELECT 'Xem danh mục xuất xứ'
UNION ALL SELECT 'Quản lý danh mục xuất xứ'
UNION ALL SELECT 'Xem danh mục file đính kèm'
UNION ALL SELECT 'Quản lý danh mục file đính kèm'
UNION ALL SELECT 'Xem danh mục mã màu'
UNION ALL SELECT 'Quản lý danh mục mã màu'
UNION ALL SELECT 'Xem danh mục thuế suất'
UNION ALL SELECT 'Quản lý danh mục thuế suất'
UNION ALL SELECT 'Xem danh mục hãng xe'
UNION ALL SELECT 'Quản lý danh mục hãng xe'
UNION ALL SELECT 'Xem danh mục loại xe'
UNION ALL SELECT 'Quản lý danh mục loại xe'
UNION ALL SELECT 'Xem danh mục model xe'
UNION ALL SELECT 'Quản lý danh mục model xe'
UNION ALL SELECT 'Xem danh mục đời xe'
UNION ALL SELECT 'Quản lý danh mục đời xe'
UNION ALL SELECT 'Xem danh mục dòng xe'
UNION ALL SELECT 'Quản lý danh mục dòng xe'
UNION ALL SELECT 'Xem danh mục tải trọng xe'
UNION ALL SELECT 'Quản lý danh mục tải trọng xe'
UNION ALL SELECT 'Xây dựng thông tin hàng hoá'
UNION ALL SELECT 'Xem dữ liệu hàng hoá công ty'
UNION ALL SELECT 'Xuất excel danh sách hàng hoá'
UNION ALL SELECT 'Xây dựng catalog kinh doanh'
UNION ALL SELECT 'Cấu hình chính sách giá bán nội bộ'
UNION ALL SELECT 'Cập nhật giá bán hàng hoá'
UNION ALL SELECT 'Duyệt giá bán hàng hoá'
UNION ALL SELECT 'PTKD duyệt yêu cầu hỏi giá'
UNION ALL SELECT 'XNK xử lý yêu cầu hỏi giá'
UNION ALL SELECT 'Tính giá bán hàng hoá'
UNION ALL SELECT 'Xem danh mục chương'
UNION ALL SELECT 'Quản lý danh mục chương'
UNION ALL SELECT 'Xem danh mục mục'
UNION ALL SELECT 'Quản lý danh mục mục'
UNION ALL SELECT 'Xem danh mục tiểu mục'
UNION ALL SELECT 'Quản lý danh mục tiểu mục'
UNION ALL SELECT 'Xem danh mục biển số xe'
UNION ALL SELECT 'Quản lý danh mục biển số xe'
UNION ALL SELECT 'Xem danh mục lái xe ngoài'
UNION ALL SELECT 'Quản lý danh mục lái xe ngoài'
UNION ALL SELECT 'Xem danh mục xe'
UNION ALL SELECT 'Quản lý danh mục xe'
UNION ALL SELECT 'Xem danh mục nhiên liệu'
UNION ALL SELECT 'Quản lý danh mục nhiên liệu'
) c
LEFT JOIN permissions p ON p.name = c.name AND p.guard_name = 'api'
WHERE p.id IS NULL;
```

## B8. [HRM-API] Backfill luồng tính giá
```bash
php artisan price-asking:backfill-groups --dry-run
php artisan price-asking:backfill-groups
php artisan price-asking:backfill-groups --dry-run     # lần 2 = 0 mọi dòng
php artisan permission:cache-reset   # "Unable to flush cache." khi chưa có khoá ⇒ vô hại; KHÔNG cache:clear (redis chung ERP)
```
(Tuỳ chọn) đóng nhóm cũ dở: `php artisan price-asking:close-stale --before=2026-06-01 --dry-run`, rồi chạy thật kèm `--by=<employees.id người chạy>`.

## B9. [ERP] Dọn giá cũ, rồi bật cron
```sql
-- [DB] N26: chỉ khi (B) <= (A)
SELECT MAX(product_version_id) FROM product_histories;                                                            -- (A)
SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'product_versions';  -- (B)
-- ALTER TABLE product_versions AUTO_INCREMENT = <(A) + 1>;
```
```bash
# [ERP] — thư mục ERP, user www-data (storage/app thuộc www-data; VPS 15/10: mkdir() Permission denied với user deploy)
sudo -u www-data php artisan price:cleanup-stale --dry-run
sudo -u www-data php artisan price:cleanup-stale
sudo -u www-data php artisan price:cleanup-stale --dry-run     # mọi nhóm = 0
```
Rồi: kiểm chốt chặn = rỗng (SQL ở A5) ⇒ **[ERP]** bật lại cron `reset_price_when_zero_inventory` ⇒ **[CRON]** bỏ comment / thêm `schedule:run` HRM (A6)
⇒ chạy thử A7 ⇒ `php artisan up` cả 2 app.

## B10. [HRM] Gán quyền cho tester, rồi **[HRM-API]** `php artisan permission:cache-reset`
Đường vào: **Quản trị hệ thống › Người dùng & phân quyền › Danh sách phân quyền** › sửa vai trò › **chọn công ty** (quyền gán theo từng công ty) › mở khối phân hệ › mở nhóm › tick.

| Khối | Phân hệ | Nhóm | Tên quyền | Dùng cho |
|---|---|---|---|---|
| QUẢN TRỊ | Phân hệ danh mục chung | Hàng hoá | Xem dữ liệu hàng hoá công ty | Menu "Dữ liệu hàng hoá công ty" (xem) |
| QUẢN TRỊ | Phân hệ danh mục chung | Hàng hoá | Xây dựng thông tin hàng hoá | Tạo / sửa hàng, menu "Hàng hoá nhập thông tin" |
| QUẢN TRỊ | Phân hệ danh mục chung | Hàng hoá | Xây dựng catalog kinh doanh | Popup "Xây dựng catalog" |
| QUẢN TRỊ | Phân hệ danh mục chung | Hàng hoá | Xuất excel danh sách hàng hoá | Nút Xuất Excel 5 màn hàng hoá |
| QUẢN TRỊ | Phân hệ danh mục chung | Danh mục hàng hóa | Xem / Quản lý danh mục: tính chất hàng hóa · nhóm chức năng · nhóm sản phẩm · loại sản phẩm · chính sách kinh doanh · đặc tính sản phẩm | Cây phân loại (bước 11) |
| QUẢN TRỊ | Phân hệ danh mục chung | Danh mục hàng hóa | Xem / Quản lý danh mục: thuế suất · mã màu · file đính kèm · code đặt hàng · hãng sản xuất · thương hiệu · thuộc tính · đơn vị tính · model · đơn vị thuộc tính · xuất xứ | Danh mục dùng trong form hàng |
| QUẢN TRỊ | Phân hệ danh mục chung | Danh mục hàng hóa | Xem / Quản lý danh mục: chương · mục · tiểu mục | Cây catalog kinh doanh |
| QUẢN TRỊ | Phân hệ danh mục chung | Danh mục hàng hóa | Xem / Quản lý danh mục: hãng xe · loại xe · model xe · đời xe · dòng xe · tải trọng xe | Danh mục xe 2b |
| QUẢN TRỊ | Phân hệ danh mục chung | Danh mục hàng hóa | Xem / Quản lý danh mục: biển số xe · lái xe ngoài · xe · nhiên liệu | Danh mục xe 2c |
| 2. VĂN PHÒNG SỐ | Phân hệ giao việc | Danh mục | Xem / Quản lý danh mục lĩnh vực Công ty kinh doanh | Lĩnh vực cho catalog (quyền có sẵn) |
| 2. VĂN PHÒNG SỐ | Phân hệ giao việc | Báo giá | Xem giá vốn hàng hoá | Xem YC tính giá / Phiếu tính giá, cột giá vốn (quyền có sẵn) |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | Cập nhật giá bán hàng hoá | Menu "Cập nhật giá bán" |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | Duyệt giá bán hàng hoá | Menu "Duyệt giá bán" |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | Cấu hình chính sách giá bán nội bộ | Chính sách giá nội bộ |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | PTKD duyệt yêu cầu hỏi giá | YC hỏi giá — bước PTKD |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | XNK xử lý yêu cầu hỏi giá | YC hỏi giá — bước XNK; xem YCTG / PTG |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | Tính giá bán hàng hoá | YC tính giá / Phiếu tính giá |
| 4. KINH DOANH - TÀI CHÍNH | Phân hệ tài chính | Hàng hoá | Cập nhật giá bán hàng hoá / Duyệt giá bán hàng hoá | Menu "Nhật ký áp giá" (xem: 1 trong 2; nút Áp ngay / Đóng: Cập nhật) — không có quyền mới |

- Nhóm **"Hàng hoá" có ở 2 phân hệ** (danh mục chung + tài chính) — tick đủ cả 2. "Danh mục hàng hóa" (dấu "hóa") là nhóm khác.
- Menu "Kho dữ liệu hàng hoá", "Hàng đang kinh doanh", "Hàng tạm", "YC hỏi giá" không gate quyền riêng.
- Super admin KHÔNG tự có các quyền này — cũng phải tick.
- **[ERP]** gán "Xem phiếu yêu cầu đặt hàng trong nước theo tổng công ty" cho vai trò cần xem (N160).

## B11. Dữ liệu tối thiểu (nhập trên HRM) — thiếu thì không tạo được hàng
- Cây phân loại Tính chất › Nhóm chức năng › Nhóm SP › Loại SP + danh mục **Đặc tính** (hàng tạm bắt buộc).
- Cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất.
- Phân công XNK theo công ty (thiếu ⇒ không gửi được Yêu cầu hỏi giá).

## B12. Khói ⇒ mục "Khói chung".

---

# Khói chung (10 phút — cả Lối A và B)
**HRM**
- `/master-data/products/company`: danh sách + Xuất Excel.
- `/finance/product-prices`: lọc 1 mã đang bán ⇒ Cty 1 · 2 · 3 · 4 đều có giá (giá × hệ số công ty); Cty 7 / 9 chỉ có hàng mình làm chủ.
  Mở Lịch sử giá 1 mã vừa áp ở A7 ⇒ mục "Áp giá hiệu lực", người thực hiện "Hệ thống".
- Tài chính › Quản lý giá - CTKM › **Nhật ký áp giá**: tab Đã áp có dòng A7; tab "Giá quá hạn chưa áp" ⇒ thử "Đóng, không áp" 1 dòng (biến mất khỏi tab,
  sang tab Đã áp hành động "Đóng, không áp"). Tài khoản chỉ có "Duyệt giá bán hàng hoá" ⇒ xem được, KHÔNG có nút xử lý.
- `/sale/price-asking-requests` → lập YC tính giá từ 1 nhóm: cột "Tính giá" sau STT; bỏ tick 1 mã ⇒ bắt lý do; bỏ hết ⇒ "Phải chọn ít nhất 1 hàng hoá để tính giá".
  Phiếu tính giá chỉ nhận mã được tick; duyệt xong ⇒ YCHG dòng mã bỏ tick "Không tính giá (XNK / Kế toán mua hàng) — lý do …", mã về "Đang nhập thông tin".
- `/master-data/vehicles`.

**ERP**
- `/admin/products/{id}/show` ⇒ trang "Chức năng đã chuyển sang HRM" có link đúng hàng.
- `/admin/sale/price_logs` ⇒ trang "Chức năng đã chuyển sang HRM" + nút mở HRM Nhật ký áp giá.
- Báo giá: popup chọn hàng ra giá đúng công ty · tài khoản Hải Phòng thấy hàng nhóm chia sẻ.

**Sáng hôm sau 01:00:** Nhật ký áp giá có dòng mới nếu có giá tới hạn; không có ⇒ `php artisan schedule:list` + log hệ thống HRM.

# Lui
Không có đường lui bằng code: khôi phục bản sao lưu (A1 / B1) + checkout lại commit trước đợt ở **cả 3 repo**.
Lui ERP mà không lui HRM (hoặc ngược lại) ⇒ 2 cron cùng áp / không cron nào áp — luôn lui cả hai.
