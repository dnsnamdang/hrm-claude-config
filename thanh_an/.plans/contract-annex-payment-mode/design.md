# Design (tóm tắt) — Phụ lục điều khoản thanh toán hỗ trợ mode/đợt/block

**Phụ trách:** @namdangit
**Spec chi tiết:** `docs/superpowers/specs/2026-07-24-contract-annex-payment-mode-design.md`
**Liên quan:** mở rộng feature [[contract-payment-mode]] sang luồng phụ lục.

## Mục tiêu
Cho màn "Phụ lục thay đổi điều khoản thanh toán" (`contract_annex_payment_terms`) hỗ trợ đầy đủ như màn tạo HĐ: chọn hình thức theo đợt / theo đơn, bảng đợt thanh toán, theo cả 2 khối HĐ chính / hàng KPI.

## Hiện trạng (chỉ hiểu model cũ)
- Service chỉ map 4 điều khoản "theo đơn", không có `block`.
- `snapshotCurrentTerms` keyBy `term_code` → HĐ KPI bị gộp nhầm main+kpi.
- `applyTermsToContract` updateOrCreate theo `(contract_id, term_code)` thiếu `block`.
- Không đụng `payment_installments` và `payment_mode_*`.

## Phạm vi (user chốt: FULL PARITY — 2026-07-24)
BE: getDataForAnnexPaymentTerms, ContractAnnexPaymentTermsService (store/update/approve/snapshot/apply), Request, DetailResource.
FE: contract_annex_payment_terms/GeneralComponent.vue (nhúng PaymentBlockCard 2 khối).

## Quyết định lớn (đã chốt 2026-07-24)
1. **Change tracking installments**: chỉ nhúng snapshot Cũ→Mới vào ContractVersion + log ContractChange gọn ở mức khối, KHÔNG log từng đợt.
2. **Biến mẫu in cho đợt/mode**: LÀM LUÔN phase này (in phụ lục + in HĐ, block-aware).

## Điểm kiến trúc quan trọng
- Approve **tái sử dụng** `ContractService::syncPaymentTerms/syncPaymentInstallments/syncPaymentModeAndBlocks` (đã block-aware, tự tính amount + dọn data ẩn) thay vì viết lại → không sửa hàm dùng chung.
- Sửa bug tiềm ẩn: `snapshotCurrentTerms` và `buildTermsTable` đang `keyBy('term_code')` gộp nhầm main+kpi → chuyển keyBy `(block, term_code)`.

Chi tiết đầy đủ: xem spec.
