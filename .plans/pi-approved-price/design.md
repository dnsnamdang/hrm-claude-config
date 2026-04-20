# Design: Đơn giá duyệt + chênh lệch + thông báo cho PI nhập khẩu / trong nước

## Bối cảnh

3 loại PI: nhập khẩu (`purchase_invoice`), trong nước theo hãng + tự do (`inland_purchase_invoice`, phân biệt bằng `type`). Yêu cầu: trên màn duyệt/xem chi tiết, hiện thêm cột "Giá đề xuất" (read-only) + "Chênh lệch" (computed), gửi thông báo khi approver sửa giá khác giá đề xuất.

## Nguyên tắc

- `price` = giá cuối cùng (approver duyệt) — giữ nguyên, downstream logic dùng cột này
- `price_suggest` = giá đề xuất (creator nhập) — tự động copy từ `price` khi tạo, frozen khi duyệt (status == CHO_DUYET)
- Inland PI delivery đã có `price_suggest` + logic JS. Import PI + promotion tables chưa có → cần thêm

## Thay đổi

### Migration

Thêm `price_suggest float(16,4) default 0` cho 3 bảng:
- `purchase_invoice_product_deliveries`
- `purchase_invoice_promotions`
- `inland_purchase_invoice_promotions`

(`inland_purchase_invoice_product_deliveries` đã có — không đụng)

### JS Class

- `PurchaseInvoiceProductDelivery.blade.php`: thêm logic `if (status != 2) { this.price_suggest = this._price }` trong setter `price`. Thêm `price_suggest` vào `submit_data`
- Promotion JS classes (cả 2 loại PI): tương tự

### View — show.blade.php (duyệt/xem chi tiết)

Bảng hàng hoá (deliveries) + bảng khuyến mại (promotions): thêm 2 cột mới
- "Giá đề xuất" = `price_suggest` (read-only)
- "Chênh lệch" = `price - price_suggest` (computed JS, không lưu DB)
- Cột "Đơn giá" (`price`) giữ nguyên — approver sửa ở đây

### Controller — approve() + notification

Khi duyệt, nếu có bất kỳ sản phẩm/KM nào mà `price != price_suggest` → gửi notification:
```
NotificationHelper::sendNotify($pi->created_by, route(...), "PI <b>{code}</b> của bạn có sự thay đổi đơn giá duyệt", Auth::user()->id)
```

### Model — sync

Thêm lưu `price_suggest` khi syncProducts/syncPromotions (cả 2 loại PI)

## Không thay đổi

- Cột `price` — giữ nguyên là giá cuối cùng
- Form tạo/sửa (`form.blade.php`) — không hiện cột giá đề xuất/chênh lệch
- Danh sách PI (index), in phiếu — không đụng
- `inland_purchase_invoice_product_deliveries.price_suggest` — đã có, giữ nguyên
