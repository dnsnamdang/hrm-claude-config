# Design — Fix modal "Xem serials" rỗng

## Mục tiêu
Modal "Danh sách serial" (KH → tab Danh sách trang thiết bị → "Xem serials") phải hiển thị tất cả serial của thiết bị theo khách hàng, kể cả serial mồ côi (phiếu xuất gốc đã bị xóa).

## Hiện trạng / vấn đề
`CustomerCareReportService::getProductForReport()` load serial cho modal theo TỪNG phiếu xuất hiện tại (lọc `invoiceable_id = request_id`). Khi phiếu xuất gốc của serial bị xóa và hàng được xuất lại qua phiếu mới, serial trở nên "mồ côi" (invoiceable_id trỏ request không còn tồn tại) → không match → modal rỗng. Bug tái diễn mỗi lần phiếu xuất bị xóa/tái tạo.

## Quyết định
Build `$product_['serials']` (data feed modal) giống endpoint báo giá `getListProductOfCustomer`: gọi `Serial::getSerialForProductOfCustomer(product_id, product_name, 'tp', null, customer_id, null, is_used=false, invoice=null, getAllSerial=true)` → lấy toàn bộ serial của thiết bị theo customer, không phụ thuộc phiếu.

- Giữ nguyên `$product_['productExportAndBorrow']` (load per-phiếu) cho tính năng "Thêm serial cho phiếu xuất".
- Re-inject `$serial['product']` (ngay_ban_giao, thoi_gian_bao_hanh, thoi_gian_het_bao_hanh, parent_code, parent_id) từ `$product_` để các cột bảo hành trong modal vẫn hiển thị.
- KHÔNG sửa hàm dùng chung `Serial::getSerialForProductOfCustomer` (chỉ đổi cách gọi). KHÔNG sửa FE.

## Ngữ nghĩa mới
Modal "Xem serials" hiển thị tất cả serial của thiết bị (product_id) theo khách hàng — gộp mọi phiếu + thiết bị cũ, đồng nhất với popup chọn thiết bị bên báo giá dịch vụ.

## Không xử lý (tùy chọn sau)
Dọn data serial mồ côi (trỏ lại invoiceable_id) — không cần thiết vì fix logic đã đảm bảo hiển thị đúng.
