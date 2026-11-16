# PI trong nước: sửa được ngày giao hàng ở màn sửa (@junfoke)

Báo lỗi: PI `inland_purchase_invoice/4480` bị không duyệt, vào sửa không đổi được "Thời gian giao" ở tab Giao hàng - Thanh toán nên không gửi duyệt lại được (server chặn ngày giao trước hôm nay).
Repo `TanPhatDev`, nhánh `gop_db`.

## Ngày 16/11/2026 (@junfoke)
- [x] 16/11/2026 — Xử lý: ô ngày ở tab Giao hàng bị khoá cứng từ 2022 (ngày gom từ "Ngày DK giao" của dòng hàng tab Hàng hóa; đổi ở tab đó thì địa chỉ giao hàng bị xoá trắng). Mở khoá ô ngày ở màn sửa (màn tạo vẫn khoá); đổi ngày ở tab Giao hàng tự cập nhật "Ngày DK giao" các dòng hàng của đợt đó; chọn ngày đã qua báo "Ngày dự kiến giao phải chọn ngày tương lai" và giữ ngày cũ; địa chỉ không mất khi đổi ngày; 2 dòng hàng cùng ngày gộp chung 1 đợt (trước bị tách vì ngày DB kèm giờ). File: `orders/inland_purchase_invoice/form.blade.php`, `partials/classes/order/InlandPurchaseInvoice.blade.php`, `InlandPurchaseInvoiceDelivery.blade.php`. Thử local PI 4188 (ngày giao đã qua) lưu đúng. `8d106db793` (gop_db, đã push).
