# Chạy gộp khách hàng trùng MST trên PRODUCTION

Phụ trách: @khoipv — Cập nhật: 2026-09-21

> Toàn bộ thao tác gói trong 1 command, **không phải chạy SQL tay**.
> Command: `php artisan customers:merge-duplicate`
> File: `hrm-thanhan-api/app/Console/Commands/MergeDuplicateCustomer.php`
> Export Excel: `hrm-thanhan-api/app/ExcelExport/DuplicateCustomerExport.php`

---

## Tóm tắt: 4 bước

```bash
# 1. Deploy code (đã xong)
git pull && php artisan clear-compiled

# 2. Quét + xuất Excel danh sách trùng
php artisan customers:merge-duplicate --scan

# 3. Tải file về, đánh dấu cột GIỮ, đưa lại lên server, chạy thử
php artisan customers:merge-duplicate --file=storage/app/gop-khach-hang/<ten-file>.xlsx --dry-run

# 4. Chạy thật (tự backup, tự hỏi xác nhận, tự đồng bộ, tự kiểm tra)
php artisan customers:merge-duplicate --file=storage/app/gop-khach-hang/<ten-file>.xlsx
```

### Đợt dọn dẹp 21/09/2026 — dùng danh sách chốt sẵn trong code

39 cặp anh @khoipv đã đánh dấu được nhúng thẳng vào command
(property `$presetPairs`), khỏi phải đưa file lên server:

```bash
php artisan customers:merge-duplicate --preset --dry-run
php artisan customers:merge-duplicate --preset
```

Chỉ dùng cho đợt này. Lần sau trùng MST mới → chạy `--scan` để xuất danh sách mới,
**không sửa `$presetPairs`**.

---

## Chi tiết

### Bước 1 — Deploy code

- [x] Pull code lên server `/var/www/thanhan2/hrm-api`
- [ ] `php artisan clear-compiled`
- [ ] Kiểm tra: `php artisan list | grep merge-duplicate`

> **Cùng 1 bản code chạy được cho cả dev lẫn production.** Command tự dò schema
> của DB đang kết nối: bảng không có thì bỏ qua, cột snapshot không có thì bỏ qua,
> và in ra "Môi trường này thiếu..." để biết nó đã bỏ qua những gì.

### Bước 2 — Quét

```bash
php artisan customers:merge-duplicate --scan
```

Command tự làm:

1. In **báo cáo môi trường**: bảng / cột command khai báo mà DB này không có (tự bỏ qua).
2. Kiểm tra DB có bảng tham chiếu khách hàng nào command **chưa biết** → **in cảnh báo**.
   Nếu có dòng lạ → **gửi danh sách đó cho dev, chưa được chạy bước 4**.
3. Tìm tất cả MST bị trùng.
4. Đếm cho từng bản ghi: báo giá, gói thầu, hợp đồng, dự án, sale phụ trách,
   địa chỉ giao hàng, TK ngân hàng, người đại diện.
5. **Điền sẵn gợi ý GIỮ** = bản ghi nhiều chứng từ nhất (hòa thì lấy bản tạo trước).
6. Cảnh báo nhóm mà cả 2 bản ghi đều đang có chứng từ.
7. Xuất file `storage/app/gop-khach-hang/danh-sach-trung-mst-<ngày-giờ>.xlsx`.

### Bước 3 — Đánh dấu và chạy thử

- [ ] Tải file .xlsx về máy, mở bằng Excel
- [ ] Cột **GIỮ** (cột P) đã có sẵn chữ `Giữ` theo gợi ý — sửa lại nếu muốn giữ bản khác
- [ ] **Mỗi nhóm (cột Cặp) phải có ĐÚNG 1 dòng ghi chữ `Giữ`** — sai thì command báo lỗi và dừng
- [ ] Đọc cột "Ghi chú của hệ thống" để biết bỏ dòng nào thì bao nhiêu chứng từ sẽ chuyển
- [ ] Lưu file, đưa lên lại server
- [ ] Chạy dry-run, phải ra **0 lỗi** mới đi tiếp

> Command cũng nhận file CSV 2 cột `keep_code,drop_code` nếu muốn tự soạn tay.

### Bước 4 — Chạy thật

```bash
php artisan customers:merge-duplicate --file=<file>.xlsx
```

Command tự làm theo thứ tự:

1. In số liệu **trước khi gộp** (khách hàng / báo giá / gói thầu / hợp đồng / dự án / sale)
2. **Tự `mysqldump` backup** vào `storage/app/gop-khach-hang/backup-<db>-<ngày-giờ>.sql`
   — backup lỗi thì **dừng**, không gộp
3. Hỏi xác nhận `yes/no`
4. Gộp từng cặp, mỗi cặp 1 transaction riêng
5. **Tự đồng bộ snapshot** cho các khách được giữ (không cần chạy `--resync` nữa)
6. **Tự kiểm tra**: số liệu trước/sau, còn MST trùng không, còn tham chiếu mồ côi không

- [ ] Chọn giờ thấp điểm, báo trước team kinh doanh
- [ ] `php artisan down` (nếu được)
- [ ] Chạy lệnh, lưu lại toàn bộ log output
- [ ] `php artisan up`
- [ ] `php artisan cache:clear && php artisan config:clear`
- [ ] Mở giao diện kiểm tra tay: danh sách khách hàng + báo giá/hợp đồng/dự án của vài khách được giữ

### Nếu có sự cố

- Restore từ file backup ở `storage/app/gop-khach-hang/`
- Mỗi cặp 1 transaction riêng → lỗi cặp nào chỉ rollback cặp đó, cặp trước đã commit.
  Muốn quay lại toàn bộ thì phải restore dump.

---

## Các option khác

| Option | Dùng khi nào |
|---|---|
| `--scan` | Quét trùng MST, xuất Excel |
| `--file=` | File .xlsx (từ `--scan`) hoặc .csv `keep_code,drop_code` |
| `--preset` | Dùng 39 cặp chốt sẵn trong code (đợt 21/09/2026) |
| `--keep= --drop=` | Gộp tay 1 cặp |
| `--dry-run` | Chạy thử, không ghi DB |
| `--resync --file=` | Chỉ đồng bộ lại snapshot, không gộp không xóa |
| `--resync --all` | Đồng bộ toàn bộ DB — **user đã chốt KHÔNG chạy** |
| `--skip-backup` | Bỏ qua backup — **không khuyến khích** |

---

## Lưu ý còn nguyên giá trị

1. **Xóa hẳn, không hồi phục được.** `category_customers` không có `deleted_at`.
2. **Không dùng lại `cap-gop.csv` của local** — mã khách trên production khác. Luôn chạy `--scan` lại.
3. **Sale phụ trách / địa chỉ giao hàng / TK ngân hàng / người đại diện của bên bị bỏ sẽ mất.**
   Cột tương ứng trong file Excel cho biết bên bỏ đang có bao nhiêu — khác 0 thì cân nhắc,
   hoặc chuyển tay sang bên giữ trước khi gộp.
4. Nhóm trùng có **nhiều hơn 2 bản ghi**: command gộp 1 cặp mỗi lần.
   Chạy `--scan` lại lần nữa để xử lý phần còn lại (bước kiểm tra cuối sẽ báo).

## Chạy được ở mọi môi trường

Cùng 1 bản code, không cần sửa gì khi đổi server:

| Tình huống | Command xử lý thế nào |
|---|---|
| Môi trường không có bảng (vd module Supply) | Tự bỏ qua, in ra ở báo cáo môi trường |
| Bảng có nhưng thiếu cột snapshot | Chỉ ghi đè những cột có thật |
| `category_customers` thiếu cột nguồn | Bỏ qua cột snapshot tương ứng |
| Thiếu `customer_last_used_id` / `_name` | Chỉ cập nhật cột nào có |
| Thiếu cột `status` / `created_at` | Ô tương ứng trong Excel để trống |
| Môi trường có bảng tham chiếu **lạ** | **DỪNG**, in danh sách để dev bổ sung |
| `mysqldump` không nằm trong PATH | Tự dò `/usr/bin`, `/usr/local/bin`, `mariadb-dump`... |
| Gõ `--file=` bằng tên file ngắn | Tự tìm ở thư mục hiện tại → gốc project → `storage/app/gop-khach-hang` |

Đã kiểm thử trên 3 DB khác schema: có Supply, không có Supply, và 1 DB giả lập
thiếu 20 bảng + 14 cột snapshot — cả 3 đều chạy đúng.
