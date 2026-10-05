# Popup chọn hàng HĐ mua — tách bộ lọc

- **Mục tiêu:** popup "Chọn hàng hóa" ở màn lập HĐ mua lọc được riêng theo Mã/Tên hàng, Khách hàng, Số HĐ (bán); popup rộng hơn.
- **Scope:** chỉ FE `GoodsPickerModal.vue` (purchase_contracts). Không sửa BE — goods-pool đã trả `customer_id/customer_name/contract_id/contract_code/sale_contract_code` trong `lines`.
- **Quyết định:**
  - Lọc ở FE (goods-pool trả 1 lần toàn bộ, như cũ).
  - Option Khách hàng / Số HĐ dựng từ dữ liệu popup đang có (chỉ hiện giá trị có hàng).
  - "Số HĐ" = `contract_code` (number ?: code của HĐ bán), kèm mã HD-xxx nếu khác.
  - Một hàng khớp khi có ít nhất 1 dòng phiếu thỏa đồng thời KH + Số HĐ.
  - Ô Mã/Tên không còn tìm theo hãng / phiếu đề xuất.
- Spec: [docs/superpowers/specs/2026-09-30-popup-chon-hang-hd-mua-bo-loc-design.md](../../docs/superpowers/specs/2026-09-30-popup-chon-hang-hd-mua-bo-loc-design.md)
