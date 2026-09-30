# Design (tóm tắt) — HĐ mua: Đơn giá trước VAT + Chiết khấu (%) + Tổng tiền trước VAT

**Người phụ trách:** @khoipv
**Bắt đầu:** 29/09/2026
**Màn:** `supply/purchase_contracts/add` (+ sửa / xem — dùng chung `ProductsTab.vue`)
**Spec chi tiết:** [docs/superpowers/specs/2026-09-29-hop-dong-mua-gia-truoc-vat-chiet-khau-design.md](../../docs/superpowers/specs/2026-09-29-hop-dong-mua-gia-truoc-vat-chiet-khau-design.md)

## Mục tiêu
Bảng hàng hóa HĐ mua tách giá trước VAT, cho nhập **chiết khấu %**, tính **Tổng tiền trước VAT** và hiện khối
tổng 3 dòng (Thành tiền trước VAT / VAT / Thành tiền sau VAT) dưới bảng như `plan/quotation/add`.

## Quyết định lớn (user chốt 29/09/2026)
1. Thứ tự cột: `Đơn giá có VAT | VAT (%) | Đơn giá trước VAT | Chiết khấu (%) | Đơn giá sau CK (VNĐ) | Tổng tiền (VNĐ)`.
2. **VAT lấy từ danh mục hàng hóa** (`products.tax`), không còn lấy theo HĐ bán / gói thầu. 1 dòng hàng = 1 mức VAT.
   BE snapshot lại `vat_percent` từ `products.tax` mỗi lần lưu (giống Phiếu xử lý cung ứng).
3. **Chiết khấu (%) nhập theo KHÁCH HÀNG** — cùng khuôn với Đơn giá có VAT (mỗi khách 1 ô, lưu `purposes[].discount_percent`).
   Cột Chiết khấu (VNĐ) tự tính cũ bị thay thế.
4. Công thức:
   - Đơn giá trước VAT = Đơn giá có VAT / (1 + VAT%)
   - Đơn giá sau CK = Đơn giá trước VAT − Đơn giá trước VAT × CK%
   - **Tổng tiền = SL × Đơn giá sau CK** (TRƯỚC VAT, đúng công thức user đưa)
   - Dưới bảng: Thành tiền trước VAT = Σ Tổng tiền; VAT = Σ Tổng tiền × VAT%; Thành tiền sau VAT = trước + VAT.
5. Giữ **3 chữ số thập phân** như báo giá (đơn giá trước VAT, sau CK, tổng tiền, các dòng tổng).
6. HĐ **Nguyên tắc**: có Đơn giá trước VAT, CK%, Đơn giá sau CK; KHÔNG có Tổng tiền / khối tổng (không có SL).
7. `purchase_contracts.total_amount` (Tổng giá trị HĐ) = **Thành tiền sau VAT** (đã trừ CK) → tab Điều khoản thanh toán tính % theo số này.

## Ngoài phạm vi
- Đơn mua hàng (`purchase_orders`) không đổi. Trait dùng chung `CalculatesPurchaseLineTotals` không sửa.
- Tab In (`PrintTab.vue`) chưa đổi — chờ user xác nhận mẫu in.
