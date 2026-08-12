# Lập HĐ ERP từ báo giá HRM — Plan (HRM / Phase 3)

> Spec: `design.md` (cặp) + authoritative `ERP/.plans/hrm-quotation-to-erp-contract/design.md`.

## Tasks (HRM)
- [ ] Migration: `quotations.erp_firm_contract_id` unsignedBigInteger nullable
- [ ] BE: resource báo giá trả `erp_firm_contract_id` + cờ đủ điều kiện lập HĐ (status=7 + synced + VND)
- [ ] FE: nút "Lập hợp đồng ERP" trên báo giá đủ điều kiện → deep-link ERP `?hrm_quotation_id=`; ẩn khi đã có `erp_firm_contract_id`
- [ ] Verify: nút hiện đúng điều kiện, deep-link mở ERP, ẩn sau khi đã lập HĐ
- [x] Siết điều kiện eligible: chỉ báo giá KHÔNG có cha-con (`parent_id` null) + tiền VND mới cho lập HĐ ERP (`erpEligibleQuery` trong `QuotationController`)
- [x] Fix SL=0 với báo giá lập từ BOM: `erpContractData` đọc `qty_needed` từ `bom_list_products` (blp) qua `COALESCE(blp.qty_needed, qpp.qty_needed)` thay vì chỉ `qpp.qty_needed` (overlay không sync qty). Verify trên hrm_dev_1 báo giá 191: 0→1; báo giá trực tiếp 32: 1→1 (không đổi)

### Checkpoint — 2026-07-17
Vừa hoàn thành: Fix bug "HRM SL 1 → ERP HĐ SL 0" cho báo giá lập từ BOM (type=1). Nguyên nhân: `QuotationService::upsertBomProducts()` sync overlay `quotation_product_prices` từ `bom_list_products` nhưng bỏ sót `qty_needed` → `qpp.qty_needed=0`; còn `erpContractData` (QuotationController ~L674) đọc thẳng `qpp.qty_needed`. Sửa theo Cách A (đọc): LEFT JOIN `bom_list_products` + `COALESCE(blp.qty_needed, qpp.qty_needed) as quantity` — fix mọi báo giá cũ, không cần re-sync. KHÔNG làm Cách B (thêm qty vào overlay) để tránh nhân đôi/lệch dữ liệu (blp là canonical). Nhánh `hrm-api`: `sync_quotation`.
Đang làm dở: (không)
Bước tiếp theo: user test lại lập HĐ ERP từ báo giá 191 trên dev-erp → SL phải ra 1.
Blocked: (không)

### Checkpoint — 2026-06-15
Vừa hoàn thành: Brainstorm + design (cặp HRM)
Đang làm dở: chưa code
Bước tiếp theo: writing-plans chung (ERP-primary); phần HRM Phase 3
Blocked: phụ thuộc ERP ghi ngược `erp_firm_contract_id`

### Checkpoint — 2026-07-14
Vừa hoàn thành: Chặn báo giá có hàng hóa cấp cha-con khỏi luồng lập HĐ ERP. Thêm `->whereDoesntHave('productPrices', fn => whereNotNull('parent_id'))` vào `erpEligibleQuery` (Modules/Assign/Http/Controllers/Api/V1/QuotationController.php ~L508) → áp dụng cho cả `erpEligible` (list) và `erpContractData` (detail 422). VND đã enforce sẵn qua `erpIsVnd`. Cập nhật message lỗi 422 cho rõ lý do.
Đang làm dở: (không)
Bước tiếp theo: khi bật lại cha-con phải hoàn thiện ERP `syncTabsFromHrm` (con total_cost=0, không cộng tổng, lưu child_parent_id/child_ratio) rồi mới gỡ điều kiện chặn này.
Blocked: (không)
