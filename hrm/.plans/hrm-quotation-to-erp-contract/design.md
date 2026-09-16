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

## ⚠️ ĐÃ BỊ THAY THẾ (quyết định 13/09/2026)

Hướng **lập HĐ ERP từ báo giá HRM** ở tài liệu này **KHÔNG còn được dùng**. User đã chốt hướng khác:
làm **hợp đồng HRM lập thẳng từ báo giá HRM** (hợp đồng bán nằm trong chính hệ thống HRM, không đẩy
sang lập HĐ ERP nữa). Quyết định này phát sinh trong khi làm feature
`.plans/gop-db/bao-cao-ket-qua-du-an-tkt/` (báo cáo kết quả Dự án TKT) — báo cáo đó cần nguồn "giá
trị hợp đồng" của dự án Thành công nhưng khảo sát cho thấy chưa có entity hợp đồng bán nào trong
`Modules/Assign/Entities/` và HĐ ERP `buy_contract2` không có cột nào trỏ về dự án TKT, nên user chốt
luôn hướng nguồn tiền tương lai là hợp đồng HRM, không phải HĐ ERP theo tài liệu này.

Hệ quả:
- Cột `quotations.erp_firm_contract_id` (nếu đã có migration) coi như không dùng tới nữa.
- Nút "Lập hợp đồng ERP" ở `ProspectiveProjectQuotationsTab.vue` (nếu đã làm) nên gỡ/không phát triển tiếp.
- Báo cáo kết quả Dự án TKT tạm để cột `Giá trị HĐ` trống (`—`) ở phase 1, chờ hợp đồng HRM xong thì
  nối vào đúng 1 điểm (`contractAmountFor()` trong `ProspectiveProjectResultReportService.php`).
- Tài liệu này **giữ lại để tham khảo lịch sử**, không triển khai tiếp trừ khi user đảo quyết định lần nữa.
