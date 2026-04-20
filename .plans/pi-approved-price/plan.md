# Plan: Đơn giá duyệt + chênh lệch + thông báo cho PI nhập khẩu / trong nước

## Trạng thái
- Bắt đầu: 2026-04-13
- Tiến độ: 11/11 task code ✅ (uncommitted), chờ chạy migration + manual test

## Phase 1: Migration

- [x] Task 1: Tạo migration thêm `price_suggest float(16,4) default 0` cho 3 bảng: `purchase_invoice_product_deliveries`, `purchase_invoice_promotions`, `inland_purchase_invoice_promotions`

## Phase 2: JS Classes — thêm price_suggest + price_diff

- [x] Task 2: `PurchaseInvoiceProductDelivery.blade.php` — setter `price` thêm `if (status != 2) { price_suggest = price }`. Thêm getter `price_diff`. Thêm `price_suggest` vào `submit_data`
- [x] Task 3: `InlandPurchaseInvoiceProductDelivery.blade.php` — thêm getter `price_diff` (đã có price_suggest)
- [x] Task 4: `PurchaseInvoicePromotion.blade.php` — setter `price` thêm `if (status != 2) { price_suggest = price }`. Thêm `price_diff` + `price_suggest` vào `submit_data`
- [x] Task 5: `InlandPurchaseInvoicePromotion.blade.php` — setter `price` thêm `if (status != 2) { price_suggest = price }`. Thêm `price_diff` + `price_suggest` vào `submit_data`

## Phase 3: Views — show.blade.php thêm cột

- [x] Task 6: `purchase_invoice/show.blade.php` — thêm header "Giá đề xuất" + "Chênh lệch" vào bảng hàng hoá + bảng khuyến mại. Thêm data cells `price_suggest`, `price_diff` (text-danger khi != 0). Fix colspan
- [x] Task 7: `inland_purchase_invoice/show.blade.php` — tương tự Task 6. Fix colspan

## Phase 4: Model sync — lưu price_suggest

- [x] Task 8: `PurchaseInvoice::syncProducts()` — thêm `$delivery->price_suggest = $d['price_suggest'] ?? $d['price']`
- [x] Task 9: `PurchaseInvoice::syncPromotions()` — thêm `$p->price_suggest`
- [x] Task 10: `InlandPurchaseInvoice::syncPromotions()` — thêm `$p->price_suggest`

## Phase 5: Controller approve — notification

- [x] Task 11: `PurchaseInvoiceController::approve()` + `InlandPurchaseInvoiceController::approve()` — sau khi sync, load lại products.deliveries + promotions, so sánh `price != price_suggest`. Nếu có khác → `NotificationHelper::sendNotify` "PI <code> của bạn có sự thay đổi đơn giá duyệt"

## Phase 6: Manual test

- [ ] Chạy migration `php artisan migrate`
- [ ] PI nhập khẩu: tạo mới → price_suggest = price. Duyệt, sửa đơn giá khác → cột "Chênh lệch" hiện số, đỏ. Save → notification gửi đến creator
- [ ] PI nhập khẩu: duyệt không đổi giá → chênh lệch = 0, không notification
- [ ] PI trong nước theo hãng: tương tự test trên
- [ ] PI trong nước tự do: tương tự test trên
- [ ] Bảng khuyến mại: test cột giá đề xuất + chênh lệch hiện đúng
- [ ] Xem chi tiết PI đã duyệt: cột giá đề xuất + chênh lệch hiện đúng, read-only

## Checkpoint

### Checkpoint — 2026-04-13
Vừa hoàn thành: 11/11 task code — 11 files (10 modified + 1 migration mới), 109 insertions
- Migration: thêm price_suggest cho 3 bảng
- JS: 4 class thêm price_suggest sync + price_diff getter
- View: 2 show.blade.php thêm 2 cột (Giá đề xuất, Chênh lệch) cho bảng hàng hoá + bảng khuyến mại
- Model: 3 sync methods lưu price_suggest
- Controller: 2 approve() thêm notification khi giá thay đổi
Đang làm dở: Chờ user chạy migration + manual test + tự commit
Bước tiếp theo: User test → commit → báo lại
Blocked: không
