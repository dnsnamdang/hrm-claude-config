# PXL — Tab "Đơn giá quy đổi" (so sánh giá trị hàng trước/sau đổi)

> @khoipv — Bắt đầu 02/10/2026
> Spec chi tiết: [docs/superpowers/specs/2026-10-02-pxl-tab-don-gia-quy-doi-design.md](../../docs/superpowers/specs/2026-10-02-pxl-tab-don-gia-quy-doi-design.md)

## Mục tiêu
PXL có đổi hàng → tab "Đơn giá quy đổi" so sánh giá trị hàng gốc (trước đổi) với hàng thay thế (sau đổi) để biết đổi đã tương xứng chưa. Chỉ tham khảo, không chặn lưu.

## Quyết định lớn
- Nguồn giá: **NK** → giá public (PLT). **PPL** → đơn mua/HĐ mua đã duyệt gần nhất (`price` gồm VAT, trước CK) → báo giá mới nhất (`price` gồm VAT) → giá vốn bảng giá. Không có → "Chưa có giá".
- Giá quy về ĐVT của dòng (A theo `unit_id`, B theo `swap_unit_id`).
- **Chụp giá lúc lưu**: 4 cột mới `swap_origin_price(_source)`, `swap_price(_source)` ở `supply_handling_products`; BE tự tính; cặp (A,ĐVT,B,ĐVT) không đổi khi sửa phiếu thì giữ giá đã chụp.
- So sánh **từng cặp** (SL thay × giá A vs SL B × giá B) + **cộng khối** khi 1 A → nhiều B + 3 ô tổng đầu tab. Cột **Đơn giá quy đổi** = giá trị sau ÷ SL thay (giá hàng thay thế trên 1 ĐVT hàng gốc).
- Màu đỏ ▲ khi sau đắt hơn, xanh ▼ khi rẻ hơn; chưa có ngưỡng %.
- Phiếu cũ chưa snapshot → hiện giá hiện tại kèm nhãn tham khảo.
