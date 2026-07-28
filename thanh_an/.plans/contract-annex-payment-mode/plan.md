# Plan — Phụ lục điều khoản thanh toán hỗ trợ mode/đợt/block

**Phụ trách:** @namdangit
**Design:** `.plans/contract-annex-payment-mode/design.md`
**Spec:** `docs/superpowers/specs/2026-07-24-contract-annex-payment-mode-design.md`
**Plan chi tiết (TDD, dùng để thực thi):** `docs/superpowers/plans/2026-07-24-contract-annex-payment-mode.md`

## Phase 1 — BE prefill + validate
- [x] Task 1: getDataForAnnexPaymentTerms trả mode/installments/terms(block)/has_kpi
- [x] Task 2: StoreContractAnnexPaymentTermsRequest thêm rule mode/installments/block

## Phase 2 — BE service (store/update/approve)
- [x] Task 3: cleanTerms + cleanInstallments block-aware
- [x] Task 4: snapshot block-aware (terms/installments/modes)
- [x] Task 5: store/update lưu data mode/installments
- [x] Task 6: approve — log gọn + nhúng snapshot + apply live (tái dùng ContractService)

## Phase 3 — BE resource + print
- [x] Task 7: ContractAnnexPaymentTermsDetailResource trả field mới (new+old)
- [x] Task 8: In phụ lục block-aware + biến mode/đợt (+ blade mới)
- [x] Task 9: In HĐ bổ sung biến điều khoản/đợt (+ 2 blade mới)

## Phase 4 — FE
- [x] Task 10: GeneralComponent nhúng 2 PaymentBlockCard + base totals + submit payload (add + _id/edit + _id/index)

## Phase 5 — Verify
- [ ] Task 11: Live-verify BE (thường/đơn/KPI) + tương thích ngược + E2E UI (cần user chạy dev server)

## Checkpoint — 2026-07-24
Vừa hoàn thành: Toàn bộ Task 1–10. BE lint sạch 5 file; FE compile template OK. FE annex đã thay PaymentTermsTab đơn bằng 2 PaymentBlockCard (main + kpi nếu has_kpi==1), thêm mainBaseTotal/kpiBaseTotal, handler onTermsUpdate/onInstallmentsUpdate; nạp mode/installments/group_kpis/has_kpi trong getContractDetail (add), _id/edit.vue, _id/index.vue; payload submit add.vue + _id/edit.vue thêm payment_mode_main/kpi + payment_installments.
Đang làm dở: Task 11 verify — cần chạy dev server (user) để E2E; BE live-verify tinker chưa chạy.
Bước tiếp theo: User bật BE+FE dev → tạo phụ lục HĐ thường (mode đơn/đợt) và HĐ áp KPI (2 khối khác mode), kiểm tra lưu/duyệt/in + tương thích ngược phụ lục cũ.
Blocked:
