# Phụ lục thay đổi điều khoản thanh toán — Design (tóm tắt)

**Người phụ trách:** @khoipv · **Ngày:** 2026-07-07
**Spec chi tiết:** `docs/superpowers/specs/2026-07-07-contract-annex-payment-terms-design.md`

## Mục tiêu
Thêm loại phụ lục HĐ thứ 7 — **"Phụ lục thay đổi điều khoản thanh toán"** (`annex_type='change_payment_terms'`): lập/duyệt/in chứng từ chính thức thay đổi bộ điều khoản thanh toán (bảng 4 điều khoản + ghi chú) của HĐ đã duyệt. Nhân bản slice `contract_annex_time`.

## Quyết định lớn
- Đổi **cả bảng 4 điều khoản + `payment_terms_note`**; khi duyệt ghi đè `contract_payment_terms` + note + nhúng vào snapshot version mới + ghi `ContractChange`.
- **Giữ nút sửa inline** sau duyệt (`updatePaymentTermsAfterApprove`) — phụ lục là luồng song song có duyệt/in/lưu vết (pattern như số HĐ/ngày ký).
- **Có In**, bảng điều khoản render động (Cũ→Mới) chèn vào mẫu print_template.
- Form **chỉ 1 bảng điều khoản mới** (prefill từ hiện tại), tái dùng `PaymentTermsTab.vue`.
- Chỉ cho lập phụ lục trên **HĐ đã duyệt** (status=3).
- **Không migration**; tái dùng quyền "Lập hợp đồng"/"Duyệt hợp đồng".
- Không đụng `syncPaymentTerms` gốc — ghi đè cục bộ trong Service phụ lục (an toàn).

## Phạm vi
- BE mới: Service + Controller + StoreRequest + DetailResource + nhóm route.
- BE sửa: `ANNEX_TYPE_LABELS` (1 chỗ).
- FE mới: bộ trang `contract_annex_payment_terms/`.
- FE sửa: 3× `ANNEX_TYPE_ROUTE_MAP` + `ANNEX_TYPE_API_MAP` + option filter (approve.vue) + menu.
