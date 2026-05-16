# Giá bán HĐ trước — Tóm tắt

**Người phụ trách:** @khoipv
**Ngày tạo:** 2026-05-13

## Mục tiêu
Populate cột "Giá bán HĐ trước" (`price_pre_contract`) trong bảng hàng hóa của 3 màn: báo giá, gói thầu, hợp đồng — lấy từ đơn giá bán (cột `price`) của hợp đồng gần nhất theo `created_at`.

## Scope
- Áp dụng cho cả 3 màn: Quotation, BidPackage, Contract
- Logic giống nhau cả 3 màn
- Tính và lưu khi tạo/sửa + tính lại realtime khi đổi khách hàng trên FE

## Logic ưu tiên
1. Cùng khách hàng → HĐ gần nhất (created_at DESC) có cùng product_id
2. Fallback: cùng tỉnh → HĐ gần nhất của KH khác cùng province_id

## Quyết định lớn
- **Approach:** API riêng + gọi khi đổi KH (không reload form)
- **Cột giá:** Dùng `contract_products.price` trực tiếp (đã gồm VAT)
- **Xác định HĐ gần nhất:** Theo `contracts.created_at DESC`
- **Migration:** Thêm cột `price_pre_contract` cho cả 3 bảng products

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-13-previous-contract-price-design.md`
