# Chặn "Nhập tồn kho đang về" cho hàng đặt công ty (đặt tồn kho)

## Bối cảnh (từ ca debug root_order_request 5489 / PI DSEN_0526.01)
Yêu cầu đặt hàng có item **thuần đặt công ty** (`order_company_qty>0`, SL khách=0, không detail khách) vẫn **chọn được** "Nhập tồn kho đang về" (type_order_request=5). Luồng allocate vào PI (`InlandOrderRequestNew::addCustomerStockEntry`) chỉ chạy theo **detail khách hàng** → hàng đặt công ty không có detail → KHÔNG được insert vào PI → "tìm không thấy trong PI" (mà không báo lỗi).

Kết luận đã thống nhất: logic chỉ cho nhập tồn kho đang về với **khách hàng** là đúng. Cần **chặn** item thuần đặt công ty chọn type 5. Trước fix: KHÔNG có guard nào (FE liệt kê đủ option; BE approve validate `in:1,2,3,5,6` cho mọi item).

## Định nghĩa "thuần đặt công ty"
`customer_qty <= 0 && order_company_qty > 0`, với `customer_qty = sum_qty - order_company_qty`.

## Fix (cả FE + BE)
### BE — `RootOrderRequestController@approve`
- [x] Trong vòng validate (status=DA_DUYET), nhánh cùng hãng: nếu item thuần đặt công ty → rule `type_order_request in:1,2,3,6` (bỏ 5) + message "Hàng đặt tồn kho không được chọn nhập tồn kho đang về"; ngược lại giữ `in:1,2,3,5,6`.

### FE — `root_order_requests/show.blade.php` + `RootOrderRequestProduct.blade.php`
- [x] Thêm getter `is_order_company_only` = `(sum_qty - order_company_qty) <= 0 && order_company_qty > 0`.
- [x] Ẩn option type 5 trong select khi `product.is_order_company_only` (`ng-if="!(t.id == 5 && product.is_order_company_only)"`).
- [x] `php -l` controller sạch.

## Lưu ý
- Item LẪN (có cả SL khách + đặt công ty) vẫn cho type 5 (phần khách vẫn nhập tồn được; phần công ty của item lẫn nằm ngoài phạm vi chặn này — nếu sau này cần xử lý phần công ty trong item lẫn thì bàn riêng).
- Ca dữ liệu cũ (root 5489 / inland 3403 đã tạo) vẫn kẹt — chặn này chỉ ngăn phát sinh mới; ca cũ cần xử lý dữ liệu riêng.

## Kiểm thử (user)
- [ ] Item thuần đặt công ty → select KHÔNG còn option "Nhập tồn kho đang về"; nếu cố submit type 5 → BE báo lỗi.
- [ ] Item có SL khách → vẫn chọn được "Nhập tồn kho đang về" bình thường.
- [ ] Item lẫn (khách + công ty) → vẫn cho type 5.

### Checkpoint — 2026-06-10
Vừa hoàn thành: chặn type 5 cho hàng thuần đặt công ty ở FE (ẩn option) + BE (validate in:1,2,3,6)
Bước tiếp theo: user test
Blocked:
