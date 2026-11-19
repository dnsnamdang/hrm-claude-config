# Đóng màn Lịch sử chỉnh sửa hàng hoá ở ERP — Plan

> 29/10/2026 · nhánh `gop_db` (checkout chính ERP/TanPhatDev) · user cho phép "làm chặn route + ẩn link".
> Đảo quyết định H4 (`HRM/.plans/gop-db/quan-ly-hang-hoa/lich-su-hang-hoa/design.md`): log ERP trước 21/10
> KHÔNG còn xem được ở đâu (user chấp nhận). Không migration / seeder / DB.

- [x] `routes/web.php` — route `productHistory` (`GET admin/products/{id}/history`) gắn `productMovedToHrm:product-show`
      ⇒ trang "Chức năng đã chuyển sang HRM" (403), link sang `/master-data/products/{id}` của HRM.
- [x] `ProductsController.php` — bỏ mục "Xem lịch sử chỉnh sửa" ở menu dòng 2 danh sách hàng hoá (searchData + bản status 1).
- [x] Giữ nguyên: `Product2Controller.php:214` (chuỗi không gán vào `$data` — code chết, chưa từng hiện),
      `products/show.blade.php` (màn show đã bị chặn, nút không tới được).
- [x] Kiểm Playwright (ERP local :8097, NV 13): trước 200 + bảng "LỊCH SỬ THAY ĐỔI", 10/10 menu dòng có mục lịch sử;
      sau 403 "Chức năng đã chuyển sang HRM", 0 link `/history`, 10/10 menu dòng còn "In barcode" (không menu rỗng).

### Checkpoint — 29/10/2026
Vừa hoàn thành: chặn route + ẩn link, đã kiểm trình duyệt.
Đang làm dở: —
Bước tiếp theo: đã commit + push origin/gop_db `a58d3e8c1f` (29/10). Khi deploy prod: không cần lệnh gì thêm (không route cache trên local; prod nếu có `route:cache` thì chạy lại).
Blocked:
