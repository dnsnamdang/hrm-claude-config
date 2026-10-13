# Plan — Fix validate hàng hóa tương đương ở phiếu xử lý YC SC-BH

## Bối cảnh
Phiếu YC kiểm tra SC-BH cho phép thêm thiết bị **nhập tay tên** (`type == "new"`, có `product_name`,
KHÔNG có `product_id`, `product_no_sale_name` rỗng). Sang phiếu xử lý phải chọn lại 1 hàng hóa có
trong danh mục. Hiện chưa bắt buộc → user không chọn vẫn Lưu được.

## Root cause (đã xác minh)
- BE `WarrantyRepairHandleStoreRequest` bắt buộc `product_id` **chỉ khi** `!empty(product_no_sale_name)`.
  Thiết bị nhập tay ở màn này có `product_no_sale_name` RỖNG (tên nằm ở `product_name`) → rule không fire → pass.
  (Kiểm chứng bằng chạy validator thật: null/''/thiếu product_id → fail; nhưng điều kiện product_no_sale_name không bao giờ đúng.)
- FE `form.blade.php`: nhánh `type == "new"` (dòng 114-118) **thiếu ô hiển thị lỗi** inline cho `product_id`.
- FE đã có sẵn nút chọn hàng (bút chì → `searchProduct` → `addProduct` set `product_id`), không cần thêm picker.

## Tasks
- [x] BE: đổi điều kiện validate từ `!empty(product_no_sale_name)` → `empty(product_id)` (rules + messages),
      message dùng `product_no_sale_name ?: product_name`.
- [x] FE: thêm `<span invalid-feedback>` cho `products.$index.product_id` vào nhánh `type == "new"` trong `form.blade.php`.
- [ ] User verify trên dev với YC 196 (thiết bị "abc"): không chọn hàng → chặn + báo "Cần chọn hàng hóa tương đương cho thiết bị abc".

## Files
- `app/Http/Requests/WarrantyRepairHandleStoreRequest.php`
- `resources/views/customercare/warranty_repair_handle_requests/form.blade.php`
