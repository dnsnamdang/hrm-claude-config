# Plan — Reset prepick_details qty về 0 (company_id = 4)

Người phụ trách: @namdangit

## Bối cảnh
Data-fix: đưa toàn bộ bản ghi `prepick_details` có `company_id = 4` và `qty > 0` về `qty = 0`,
đồng thời tạo bản ghi log tương ứng trong `prepick_logs`. Chạy qua tinker theo Data Fix Pattern.

## Tasks
- [x] Thêm import `PrepickDetail` vào `database/seeds/UpdateDB.php`
- [x] Viết method `resetPrepickDetailQtyCompany4()` trong `UpdateDB.php`
  - Query `prepick_details` where `company_id = 4` AND `qty > 0`
  - Với mỗi bản ghi: tạo `PrepickLog` (qty_before, change = -qty, qty_after = 0) rồi set `qty = 0`
  - Bọc trong transaction, echo số bản ghi đã xử lý
- [x] Lint PHP OK (`php -l`)
- [x] Hướng dẫn user cách chạy qua tinker (xem mục Cách chạy)

## Cách chạy
```
php artisan tinker --execute="(new \UpdateDB)->resetPrepickDetailQtyCompany4();"
```
(Class `UpdateDB` ở global namespace — gọi `\UpdateDB`, KHÔNG phải `\Database\Seeds\UpdateDB`.)

## 🔴 CẢNH BÁO — CHƯA ĐƯỢC CHẠY SEEDER (nguy cơ đè production)

Trong lúc chuẩn bị chạy, phát hiện môi trường đang **kết nối nhầm lên production**:

- File **`bootstrap/cache/config.php`** (05/08/2025) chứa cứng DB production:
  `host=erp.eteksofts.com`, `port=33061`, `database=erp_new`.
- Khi config cache tồn tại, Laravel **bỏ qua `.env` hoàn toàn** (`env('DB_HOST')` trả rỗng) →
  mọi lệnh `artisan`/`tinker` chạy thẳng lên production `erp_new`.
- `.env` ghi `DB_DATABASE=erp_8825` nhưng DB này **không tồn tại** trên MySQL local.
  DB ERP local thật là **`erp2326`** (đã verify: 1.644 bản ghi company_id=4 qty>0, tổng qty 3.514).

**Seeder CHƯA từng chạy thật** — cả 3 lần thử đều dừng ở lỗi `Class not found` (method chưa thực thi),
nên production `erp_new` chưa bị hàm này đụng vào.

### Việc phải làm trước khi chạy seeder (theo thứ tự)
- [ ] `php artisan config:clear` — xóa `bootstrap/cache/config.php` để đọc lại `.env`
- [ ] Sửa `.env`: `DB_DATABASE=erp_8825` → `DB_DATABASE=erp2326` (DB local thật)
- [ ] Verify resolve đúng `127.0.0.1 / erp2326`:
      `php artisan tinker --execute="\$c=config('database.default'); echo config(\"database.connections.\$c.host\").' / '.config(\"database.connections.\$c.database\");"`
- [ ] Fix autoload `Class 'UpdateDB' not found` (có thể cần `composer dump-autoload`)
- [ ] TUYỆT ĐỐI **không** chạy lại `php artisan config:cache` (sẽ lặp lại tình trạng đè production)
- [ ] Sau khi 4 bước trên xong → chạy seeder, kỳ vọng: reset 1.644 bản ghi + tạo 1.644 prepick_logs

### Checkpoint — 2026-07-07
Vừa hoàn thành: Viết + lint method `resetPrepickDetailQtyCompany4()`; phát hiện & chẩn đoán lỗi
config cache trỏ production; xác minh DB local đúng là `erp2326` (1.644 bản ghi cần reset).
Đang làm dở: Chưa xử lý config cache / chưa chạy seeder — chờ user xác nhận đổi `.env` sang `erp2326`.
Bước tiếp theo: User (hoặc cho phép AI) chạy `config:clear` + sửa `.env` DB_DATABASE=erp2326 + verify,
rồi mới chạy seeder.
Blocked: Chờ user xác nhận DB local đích (`erp2326`) trước khi sửa `.env`.
