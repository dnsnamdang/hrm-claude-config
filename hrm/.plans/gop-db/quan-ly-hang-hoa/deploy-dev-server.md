# Deploy CHUẨN nhánh Chuyển đổi hàng hoá — DB CHƯA TỪNG chạy (dev server / VPS test)

> Cập nhật 15/10/2026 (luật chép giá mới: nhóm chia sẻ 1·3·4, tự quản 2·7). Bản đầy đủ cho production: `gia-theo-cong-ty/runbook-trien-khai.md`.
> ERP và HRM dùng **chung 1 DB gộp** ⇒ migration/backfill chạy MỘT lần ở hrm-api, ERP chỉ cần code + `.env` + 1 lệnh dọn giá.
> ⚠️ KHÔNG merge vào `gop_db`: server checkout thẳng nhánh feature.
> Nhãn mỗi bước: **[HRM-API]** chạy trong thư mục hrm-api · **[HRM-CLIENT]** · **[ERP]** · **[DB]** chạy SQL trực tiếp.

| Repo | Nhánh | Commit (đã push 15/10) |
|---|---|---|
| hrm-api | `feat/chuyen-doi-hang-hoa` | `5ab7ab2ac` |
| hrm-client | `feat/chuyen-doi-hang-hoa` | `baa5a3563` |
| ERP | `feat/2d1-erp-khong-loi` | `7bfe798a9f` |

## 0. [DB] Xác nhận DB chưa từng chạy (sai ⇒ KHÔNG dùng hướng dẫn này)
```sql
SHOW TABLES LIKE 'product_company_units';                         -- chưa có bảng, hoặc có nhưng 0 dòng
SELECT COUNT(*) FROM product_unit_prices WHERE company_id IS NOT NULL;   -- lỗi "Unknown column" hoặc = 0
```
Đã có dữ liệu ⇒ DB đã backfill (có thể theo luật cũ 1-2-3-4): nạp lại DB từ bản chưa backfill rồi làm từ đầu.

## 1. [DB] Sao lưu + tạm dừng
```bash
mysqldump --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF <db> | gzip > backup_<db>_$(date +%F_%H%M).sql.gz
```
- **[ERP]** tắt 2 cron `product:update_price` (01:00) và `product:reset_price_when_zero_inventory` (14:30) tới hết bước 9.
- **[ERP] + [HRM-API]** `php artisan down` (nếu có người đang dùng).

## 2. Lấy code
```bash
# [HRM-API]
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull
composer install --no-dev -o
php artisan config:clear

# [HRM-CLIENT]  (node 12)
git fetch origin && git checkout feat/chuyen-doi-hang-hoa && git pull
npm ci && NODE_OPTIONS=--max-old-space-size=8192 npm run build
# restart Nuxt (pm2 …)

# [ERP]
git fetch origin && git checkout feat/2d1-erp-khong-loi && git pull
composer install --no-dev -o
```

## 3. [ERP] `.env` rồi clear cache
```
HRM_URL_FE=<url hrm-client>        # link "Chức năng đã chuyển sang HRM", xem chi tiết hàng hoá
HRM_URL_BE=<url hrm-api>
HRM_API_BASE_URL=<url hrm-api>     # popup chọn hàng ERP gọi API HRM
```
```bash
php artisan config:clear && php artisan route:clear && php artisan view:clear
```

## 4. [HRM-API] Migration lượt 1 — PHẢI dừng ở M3
```bash
php artisan migrate:status | grep "| No"
php artisan migrate --force
```
Đúng khi dừng ở `2026_10_09_000004_enforce_company_id_on_product_unit_prices_table` với lỗi "còn N dòng company_id NULL…"
(migration tự chặn, không đổi gì). **Chạy qua luôn ⇒ DB không phải DB mới — DỪNG, xem bước 0.**

## 5. [HRM-API] Backfill giá theo công ty (luật 15/10)
```bash
php -d memory_limit=4G artisan product-price:backfill-company --dry-run
php -d memory_limit=4G artisan product-price:backfill-company
php -d memory_limit=4G artisan product-price:compare
```
| Kiểm | Đạt khi |
|---|---|
| dry-run, dòng "B0 kiểm trước" | toàn 0 (≠ 0 ⇒ DỪNG báo dev) |
| dry-run, cột Cty 2 / Cty 7 | Cty 2 chỉ phần hàng HP làm chủ (đo `hrm_erp` 15/10: 24 dòng) · Cty 7 = 0 |
| dry-run, TỔNG GHI | cỡ **810 nghìn** (đo `hrm_erp` 15/10: 810.016; luật cũ ra ~1,04 triệu ⇒ sai code) |
| chạy thật | bảng in = dry-run, dòng cuối "B6 kiểm sau: đạt" (~1–2 phút) |
| compare | dòng cuối **`0 lệch.`** |

Luật (config `hrm-api/config/price.php`): **1 Tân Phát · 3 Vinh · 4 Sài Gòn** chép giá lẫn nhau mọi hàng đang bán (giá × hệ số công ty
nhận, không có hệ số ⇒ giá bằng). **2 Hải Phòng · 7 ETEK Green** chỉ có hàng mình làm chủ, không nhận / không cho. **5·6·8** bỏ qua.

## 6. [HRM-API] Migration lượt 2
```bash
php artisan migrate --force                       # M3 + 12 migration luồng tính giá + 2026_10_13 (cờ dịch vụ) + 2026_10_15 (index)
php artisan migrate:status | grep -c "| No"       # = 0
```

## 7. Quyền
**[HRM-API]** — KHÔNG chạy `PermissionsTableSeeder` (truncate cả bảng):
```bash
php artisan db:seed --force --class="Modules\MasterData\Database\Seeders\ProductPricePermissionSeeder"          # 1657, 1658
php artisan db:seed --force --class="Modules\MasterData\Database\Seeders\ProductExportPermissionSeeder"         # 1654
php artisan db:seed --force --class="Modules\MasterData\Database\Seeders\InternalPricePolicyPermissionSeeder"   # 1656
php artisan db:seed --force --class="Modules\MasterData\Database\Seeders\PriceCalculationPermissionSeeder"      # 1662–1664
```
**[DB]** — quyền không có seeder riêng (11 quyền). Kiểm trước, id đã bị quyền KHÁC chiếm ⇒ DỪNG báo dev:
```sql
SELECT id, name FROM permissions WHERE id IN (1652,1653,1655,1720,1721,1722,1723,1724,1725,1726,1727);

INSERT INTO permissions (id,name,guard_name,display_name,`group`,type,created_at,updated_at) VALUES
(1652,'Xây dựng thông tin hàng hoá','api','Xây dựng thông tin hàng hoá','Hàng hoá',9,NOW(),NOW()),
(1653,'Xem dữ liệu hàng hoá công ty','api','Xem dữ liệu hàng hoá công ty','Hàng hoá',9,NOW(),NOW()),
(1655,'Xây dựng catalog kinh doanh','api','Xây dựng catalog kinh doanh','Hàng hoá',9,NOW(),NOW()),
(1720,'Xem danh mục biển số xe','api','Xem danh mục biển số xe','Danh mục hàng hóa',9,NOW(),NOW()),
(1721,'Quản lý danh mục biển số xe','api','Quản lý danh mục biển số xe','Danh mục hàng hóa',9,NOW(),NOW()),
(1722,'Xem danh mục lái xe ngoài','api','Xem danh mục lái xe ngoài','Danh mục hàng hóa',9,NOW(),NOW()),
(1723,'Quản lý danh mục lái xe ngoài','api','Quản lý danh mục lái xe ngoài','Danh mục hàng hóa',9,NOW(),NOW()),
(1724,'Xem danh mục xe','api','Xem danh mục xe','Danh mục hàng hóa',9,NOW(),NOW()),
(1725,'Quản lý danh mục xe','api','Quản lý danh mục xe','Danh mục hàng hóa',9,NOW(),NOW()),
(1726,'Xem danh mục nhiên liệu','api','Xem danh mục nhiên liệu','Danh mục hàng hóa',9,NOW(),NOW()),
(1727,'Quản lý danh mục nhiên liệu','api','Quản lý danh mục nhiên liệu','Danh mục hàng hóa',9,NOW(),NOW());
```
Dùng INSERT **thường** (không IGNORE): vướng trùng là báo lỗi + không chèn dòng nào; id nào đã có đúng tên thì bỏ dòng đó khỏi câu. (VPS test 15/10: dùng IGNORE thì 11 dòng 1652/1653/1655/1720–1727 bị bỏ qua im lặng, chỉ phát hiện nhờ câu đếm.)
Kiểm cuối — **phải = 18**:
```sql
SELECT COUNT(*) FROM permissions WHERE id IN (1652,1653,1654,1655,1656,1657,1658,1662,1663,1664,1720,1721,1722,1723,1724,1725,1726,1727);
```
**Kiểm đủ quyền cả luồng** (73 quyền theo TÊN — gồm quyền đã đi theo `gop_db`: phân loại hàng hoá, danh mục hàng hoá, xe 2b, catalog Chương/Mục/Tiểu mục, lĩnh vực Công ty KD, Xem giá vốn hàng hoá). **Rỗng = đủ**; ra tên nào ⇒ thiếu, báo dev:
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
> 15/10: 2 quyền "Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty / theo công ty" (1660/1661) KHÔNG thuộc luồng này — là feature báo cáo nhu cầu dịch vụ đi theo `gop_db` (commit `5140783e3`), lọt vào danh sách vì soạn từ diff seeder. Đã bỏ.

Quyền 6 danh mục xe 2b (1640–1651) đi theo `gop_db`; DB đang mang 1620–1631 thì xem N104.

## 8. [HRM-API] Backfill luồng tính giá
```bash
php artisan price-asking:backfill-groups --dry-run
php artisan price-asking:backfill-groups
php artisan price-asking:backfill-groups --dry-run     # lần 2 phải 0 mọi dòng
php artisan permission:cache-reset   # báo "Unable to flush cache." khi chưa có khoá cache quyền ⇒ vô hại; KHÔNG cache:clear (redis chung ERP)
```
(Tuỳ chọn) đóng nhóm cũ dở: `php artisan price-asking:close-stale --before=2026-06-01 --dry-run`, rồi chạy thật kèm `--by=<employees.id người chạy>`.

## 9. [ERP] Dọn giá ERP — xong TRƯỚC 01:00
```sql
-- [DB] N26: chỉ khi (B) <= (A)
SELECT MAX(product_version_id) FROM product_histories;                                                            -- (A)
SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'product_versions';  -- (B)
-- ALTER TABLE product_versions AUTO_INCREMENT = <(A) + 1>;
```
```bash
php artisan price:cleanup-stale --dry-run
php artisan price:cleanup-stale
php artisan price:cleanup-stale --dry-run     # mọi nhóm = 0
```
Chạy trong thư mục **ERP** (không phải hrm-api). Lệnh ghi CSV vào `storage/app/price-cleanup/` (cả dry-run) ⇒ `storage/app` thuộc `www-data` thì chạy `sudo -u www-data php artisan …` (VPS test 15/10: `mkdir(): Permission denied` với user deploy). Đo VPS test 15/10: 13.949 giá hiệu lực quá ngày + 5/6/6 cờ chờ duyệt mồ côi ⇒ lượt 2 = 0.
Bật lại 2 cron ERP; `php artisan up` cả 2 app.

## 10. [HRM] Gán quyền cho tester, rồi **[HRM-API]** `php artisan permission:cache-reset`
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

- Nhóm **"Hàng hoá" có ở 2 phân hệ** (danh mục chung + tài chính) — tick đủ cả 2. "Danh mục hàng hóa" (dấu "hóa") là nhóm khác.
- Menu "Kho dữ liệu hàng hoá", "Hàng đang kinh doanh", "Hàng tạm", "YC hỏi giá" không gate quyền riêng.
- Super admin KHÔNG tự có các quyền này — cũng phải tick.

## 11. Dữ liệu tối thiểu (nhập trên HRM) — thiếu thì không tạo được hàng
- Cây phân loại Tính chất › Nhóm chức năng › Nhóm SP › Loại SP + danh mục **Đặc tính** (hàng tạm bắt buộc).
- Cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất.
- Phân công XNK theo công ty (thiếu ⇒ không gửi được Yêu cầu hỏi giá).

## 12. Khói (5 phút)
- **[HRM]** `/master-data/products/company` (danh sách + Xuất Excel) · `/finance/product-prices` (lọc 1 mã: Cty 1/3/4 có giá, Cty 2 không có trừ hàng HP) · `/sale/price-asking-requests` · `/master-data/vehicles`.
- **[ERP]** `/admin/products/{id}/show` ⇒ trang "Chức năng đã chuyển sang HRM" có link đúng hàng · báo giá: popup chọn hàng ra giá đúng công ty · tài khoản Hải Phòng chỉ thấy hàng HP làm chủ (N128).

## Lui
Không có đường lui bằng code: khôi phục bản sao lưu bước 1 + checkout lại nhánh cũ ở cả 3 repo.
