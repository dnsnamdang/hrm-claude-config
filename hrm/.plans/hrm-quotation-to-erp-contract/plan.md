# Lập HĐ ERP từ báo giá HRM — Plan (HRM / Phase 3)

> Spec: `design.md` (cặp) + authoritative `ERP/.plans/hrm-quotation-to-erp-contract/design.md`.

## Tasks (HRM)
- [ ] Migration: `quotations.erp_firm_contract_id` unsignedBigInteger nullable
- [ ] BE: resource báo giá trả `erp_firm_contract_id` + cờ đủ điều kiện lập HĐ (status=7 + synced + VND)
- [ ] FE: nút "Lập hợp đồng ERP" trên báo giá đủ điều kiện → deep-link ERP `?hrm_quotation_id=`; ẩn khi đã có `erp_firm_contract_id`
- [ ] Verify: nút hiện đúng điều kiện, deep-link mở ERP, ẩn sau khi đã lập HĐ

### Checkpoint — 2026-06-15
Vừa hoàn thành: Brainstorm + design (cặp HRM)
Đang làm dở: chưa code
Bước tiếp theo: writing-plans chung (ERP-primary); phần HRM Phase 3
Blocked: phụ thuộc ERP ghi ngược `erp_firm_contract_id`
