# Lập HĐ ERP từ báo giá HRM — phần HRM (tóm tắt)

> **Spec đầy đủ (authoritative)**: `ERP/.plans/hrm-quotation-to-erp-contract/design.md`.
> Đây là cặp HRM, chỉ ghi phần việc bên HRM (Phase 3 + migration).

## Bối cảnh
Lập hợp đồng bên ERP trực tiếp từ báo giá Assign (HRM) khi: `status=7` (trúng thầu) + `tmp_sync_status='synced'` (đồng bộ hết hàng tạm) + tiền **VND**. KHÔNG tạo firm_quotation ERP. ERP đọc báo giá HRM qua connection `hrm`, prefill form HĐ; NV ERP nhập nốt.

## Phần việc HRM
1. **Migration**: thêm `quotations.erp_firm_contract_id` (unsignedBigInteger, nullable) — ERP ghi ngược id HĐ sau khi lập (chống trùng).
2. **FE** (`pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue` hoặc màn báo giá liên quan): nút **"Lập hợp đồng ERP"** trên báo giá đủ điều kiện (`status=7` + `tmp_sync_status='synced'` + VND + chưa có `erp_firm_contract_id`) → mở tab mới URL ERP `/admin/sale/firm-contracts/create?hrm_quotation_id={id}` (base ERP lấy từ config HRM). Ẩn nút khi đã có `erp_firm_contract_id`.
3. **BE (nếu cần)**: trả `erp_firm_contract_id` + cờ đủ điều kiện trong resource báo giá để FE hiện/ẩn nút.

## Lưu ý
- Việc ghi `quotations.erp_firm_contract_id` do **ERP** thực hiện (qua connection `hrm`), HRM chỉ cần migration cột + đọc.
- Resolve KH, đọc sản phẩm, tạo HĐ: toàn bộ ở ERP (xem spec ERP).
