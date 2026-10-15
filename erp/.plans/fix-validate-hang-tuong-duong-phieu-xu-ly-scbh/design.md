# Design — Fix validate hàng hóa tương đương ở phiếu xử lý YC SC-BH

## Mục tiêu
Ở phiếu YC kiểm tra SC-BH, thiết bị có thể nhập tay tên (không có trong danh mục hàng hóa).
Sang bước **phiếu xử lý**, mỗi thiết bị như vậy BẮT BUỘC phải chọn 1 hàng hóa tương đương có
trong danh mục (`product_id`). Nếu không chọn → chặn Lưu, báo "Cần chọn hàng hóa tương đương cho
thiết bị [tên]".

## Hiện trạng dữ liệu (đã xác minh qua YC 196, thiết bị "abc")
Thiết bị nhập tay ở YC được thêm bằng `addNewProduct()` → `{ type: 'new', product_name: '<tên gõ tay>' }`,
KHÔNG có `product_id`, và `product_no_sale_name` RỖNG (khác nhánh "hàng công ty không bán").
Ở phiếu xử lý các thiết bị này render ở nhánh `type == "new"` (có nút bút chì mở `searchProduct` để chọn hàng).

## Root cause
`WarrantyRepairHandleStoreRequest` bắt buộc `product_id` chỉ khi `!empty(product_no_sale_name)`.
Thiết bị nhập tay dạng `type=="new"` có `product_no_sale_name` rỗng → rule không được thêm → pass.
(Bản thân rule `required|exists` hoạt động đúng — đã kiểm chứng bằng chạy validator thật; chỉ điều kiện kích hoạt sai field.)

## Quyết định fix
Chuyển điều kiện kích hoạt validate sang **`empty($product['product_id'])`** — bao trùm cả 2 dạng thiết bị
chưa gắn hàng danh mục (`type=="new"` gõ tay và "hàng công ty không bán" thiếu tương đương). Thiết bị đã
có `product_id` hợp lệ vẫn pass.

- BE: `WarrantyRepairHandleStoreRequest::rules()` + `messages()` — điều kiện `empty(product_id)`,
  tên thiết bị lấy `product_no_sale_name ?: product_name`. Áp dụng cả store lẫn update (dùng chung request).
- FE: `warranty_repair_handle_requests/form.blade.php` — thêm `<span invalid-feedback>` cho
  `products.$index.product_id` vào nhánh `type == "new"` (nhánh `type != "new"` đã có sẵn). Nút chọn hàng
  đã có sẵn, không thêm mới.

## Không đổi
- Không đụng luồng thêm "hàng công ty không bán" (`AddExternalEquipmentRequest` vẫn required product_id).
- Không đổi schema, không đụng `syncProduct`, không đụng logic duplicate device_error.

## Edge cases
- `product_id` = "0"/0 → `exists:products,id` chặn (không có product id 0).
- Thiết bị chọn từ thiết bị của khách (đã có product_id) → pass.
