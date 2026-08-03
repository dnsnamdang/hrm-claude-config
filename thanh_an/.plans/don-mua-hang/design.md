# Design tóm tắt — Đơn mua hàng (build thật)

> Spec đầy đủ: `docs/superpowers/specs/2026-07-30-don-mua-hang-design.md`
> Người phụ trách: @khoipv · Bắt đầu: 2026-07-30

## Mục tiêu
Build thật full-stack màn "Đơn mua hàng" (DMH) trong phân hệ Cung ứng, bám demo `demos/demo-tao-don-mua-hang.html`, nhân bản khuôn **HĐ mua** (`purchase_contracts` / `Modules/Supply`).

## Scope
- 4 màn: danh sách / thêm / xem-duyệt / sửa. Menu đặt ngay dưới "Hợp đồng mua".
- Luồng duyệt như HĐ mua (Nháp→Chờ duyệt→Duyệt/Từ chối/Hủy).

## Quyết định lớn (chốt với user)
1. Full-stack như HĐ mua (BE+FE+duyệt).
2. **KHÔNG phân cấp** (giống HĐ mua thật): quyền "Xem đơn mua hàng" cấp tổng → thấy tất cả.
3. Con trỏ nguồn = JSON `purposes`, **KHÔNG trừ SL nhu cầu** (TODO module nhập hàng).
4. `is_can_delete` = người tạo + Nháp/Từ chối.
5. Chỉ loại **"Theo phiếu đề xuất"** đầy đủ; **"Mua dự trù"** placeholder.
6. Khối **Dư nợ NCC** = placeholder, nối sau.
7. **"Cty thực hiện mua"** bắt buộc mỗi dòng.

## Khác HĐ mua
- Bỏ: loại NT/TM, snapshot Bên A/B, ngày ký/KT, `condition` rich-text, tab In.
- Thêm: `order_type`, khối NCC (liên hệ/SĐT/địa chỉ sửa được), `ship_method`, Dư nợ NCC (placeholder); bảng hàng thêm `buyer_company_id` (Cty thực hiện mua, bắt buộc) + `need_date` + hiển thị Cty thực hiện bán.
- Giữ: điều khoản TT (đợt/đơn 4 loại), popup nhu cầu mua, gộp 1 mã nhiều phiếu, cảnh báo SL đỏ/vàng, đơn giá gồm VAT + tổng realtime.

## DB — 4 bảng mới (index, không FK)
`purchase_orders`, `purchase_order_products` (+`buyer_company_id`,`need_date`), `purchase_order_payment_terms`, `purchase_order_progress`.

## Quyền mới (group 'Cung ứng', type 7)
`Xem đơn mua hàng`, `Lập đơn mua hàng`, `Duyệt đơn mua hàng` — id kế tiếp còn trống (dự kiến 521/522/523, kiểm tra khi seed).

## Ngoài scope
Mua dự trù, tab In, trừ nhu cầu ở nguồn, công nợ NCC thật, Phiếu giao hàng/Đề nghị thanh toán.
