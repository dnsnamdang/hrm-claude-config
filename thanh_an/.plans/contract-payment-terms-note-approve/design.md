# Design — Ghi chú + Lưu-sau-duyệt cho tab Điều khoản thanh toán

**Trạng thái:** Đã chốt design
**Phụ trách:** @khoipv
**Ngày:** 2026-06-09
**Spec chi tiết:** `docs/superpowers/specs/2026-06-09-contract-payment-terms-note-approve-design.md`
**Feature gốc:** `.plans/contract-payment-terms/` (tab Điều khoản thanh toán)

---

## Mục tiêu

Mở rộng tab **Điều khoản thanh toán** trong form hợp đồng (`contract/contract`):
1. Thêm **1 ô ghi chú chung** cho cả tab.
2. Cho phép **lưu lại cả bảng + ghi chú khi hợp đồng đã duyệt** (status=3), giống cơ chế nút Lưu của khối Thông tin hợp đồng.

## Scope

- Chỉ form hợp đồng gốc `contract/contract`. Không đụng phụ lục.
- Không thêm phân quyền mới — dùng điều kiện `status === 3` sẵn có.

## Các quyết định lớn

| | |
|---|---|
| Phạm vi ghi chú | 1 ghi chú chung/HĐ (không phải từng dòng) |
| Lưu ghi chú ở đâu | Cột mới `payment_terms_note` (text) trên bảng `contracts` |
| Nút Lưu khi đã duyệt | Mở khóa + lưu cả bảng + ghi chú |
| Endpoint lưu-sau-duyệt | Tách riêng `updatePaymentTermsAfterApprove`, tái dùng `syncPaymentTerms` |
| Đồng bộ ContractVersion | KHÔNG (payment terms đọc live, không đọc theo snapshot) |
