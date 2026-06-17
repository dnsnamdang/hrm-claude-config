# Quotation Shipping Cost + Redesign Tổng hợp giá trị báo giá — Tóm tắt

## Mục tiêu

1. **Thiết kế lại** section "Tổng hợp giá trị báo giá" thành **bảng nhóm chi phí 7 cột** (tách cột Chiết khấu).
2. Thêm **Chi phí vận chuyển** cấp phiếu = **row IV** của bảng, nhập trực tiếp (KHÔNG checkbox).
3. Bản in + Excel lấy **đúng theo bảng tổng hợp**.

## Bảng Tổng hợp (7 cột)

| STT | Nhóm chi phí | Thành tiền nhập | Thành tiền trước VAT | Chiết khấu | Thuế VAT | Thành tiền sau VAT |
|---|---|---|---|---|---|---|
| I | Hàng hoá | Σ nhập×SL | Σ bán×SL | CK phân bổ | (trướcVAT−CK)×vat% | trướcVAT−CK+VAT |
| II | Dịch vụ | Σ vốn×SL | Σ bán×SL | CK phân bổ | … | … |
| III | Chi phí | Σ vốn×SL | Σ bán×SL | CK phân bổ | … | … |
| IV | Chi phí vận chuyển | = trước VAT | **input** | input (per-item) / auto (CK tổng) | (trướcVAT−CK)×%VAT | trướcVAT−CK+VAT |
| V | Tổng giá trị báo giá | Σ cột | Σ cột | Σ cột | Σ cột | Σ cột |

- "Thành tiền trước VAT" = doanh thu GỐC (trước CK); VAT tính trên (trướcVAT − CK).
- VC: không markup (nhập = trước VAT), **chịu chiết khấu như Hàng hoá/Dịch vụ**, VAT mặc định 8%.
- II Dịch vụ vs III Chi phí tách theo `revenue_calculation` (1/null→DV, 0→CP).
- **Cột "Chiết khấu" ẩn khi không dùng CK** (`discount_method=null` → 6 cột); hiện khi CK theo mặt hàng/CK tổng (7 cột).

## Quyết định lớn

| Hạng mục | Quyết định |
|---|---|
| Chi phí VC | Field cấp phiếu (4 cột mới: `shipping_cost`, `shipping_vat_percent`, `shipping_discount`, `shipping_allocated_discount`), là row IV, không checkbox |
| Hiển thị CK | Phương án B — tách cột Chiết khấu |
| VC & CK | VC **chịu chiết khấu** như Hàng hoá/Dịch vụ (per-item: input ô CK row IV; CK tổng: vào base phân bổ) |
| Phạm vi | Cả BOM lẫn tự lập; edit/view/print/excel đều dựng từ bảng |
| Phân quyền | Không thêm permission |

## Spec chi tiết

- `docs/superpowers/specs/2026-06-06-quotation-shipping-cost-design.md`

## Liên quan

- Branch: `tpe-develop-assign`
- Liên quan: `erp-cost-catalog`, `quotation-redesign`, `Bomlist-Quotation`
- Người phụ trách: @dnsnamdang
