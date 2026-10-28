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
cd $API && git pull origin gop_db && git log --oneline -1         # >= 326374069
composer install --no-dev --optimize-autoloader                   # chỉ cần nếu composer.lock đổi (đợt này không đổi)
cd $CLI && git pull origin gop_db && git log --oneline -1         # >= 094e72fc6
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
