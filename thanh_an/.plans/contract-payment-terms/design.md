# Design — Điều khoản thanh toán trên hợp đồng

**Trạng thái:** Đã chốt design
**Phụ trách:** @khoipv
**Ngày:** 2026-05-18
**Mock tham khảo:** `hrm-thanhan-client/pages/timesheet/setting/debt-limit/canh-bao-cong-no-v4.html` (section 3)
**Spec chi tiết:** `docs/superpowers/specs/2026-05-18-contract-payment-terms-design.md`

---

## Mục tiêu

Thêm bảng điều khoản thanh toán vào tab "Cài đặt công nợ thanh toán" trong form hợp đồng. Mỗi HĐ có 4 loại điều khoản cố định, user tick bật/tắt + nhập ngưỡng cho từng loại.

## Scope

- BE: 1 migration (`contract_payment_terms`), 1 model, validate + sync trong flow store/update contract hiện có.
- FE: 1 component `PaymentTermsTab.vue` render bảng trong tab đang trống của `GeneralComponent.vue`.
- Không tạo API riêng — gắn vào flow contract.

## Các quyết định lớn

| | |
|---|---|
| 4 loại cố định, hardcode | `100PCT`, `TIME`, `VALUE`, `ROLLING` |
| Approach A — 4 row per HĐ | Tạo HĐ = insert 4 row `enabled=false`, luôn có đủ 4 row |
| Bảng riêng | `contract_payment_terms` với FK → contracts |
| Logic exclusive | `100PCT` bật → 3 row còn lại bắt buộc `enabled=false` |
| Default khi tạo HĐ mới | Tất cả tắt |

## Out of scope

- Check rule công nợ khi tạo phiếu giao dịch (tích hợp với section 4 + 5 mock).
- Lịch sử thay đổi điều khoản (có thể thêm sau).
