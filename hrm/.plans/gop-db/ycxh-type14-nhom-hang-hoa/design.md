# YCXH loại 14 — "Chọn nhóm hàng hóa" (tab theo nhóm) + field Thông tin chung

**Trạng thái:** Spec xong, chờ user review → writing-plans.
**Spec đầy đủ:** `../../../docs/superpowers/specs/gop-db/2026-10-13-ycxh-type14-nhom-hang-hoa-design.md`
**Nhánh:** `develop` (con của `gop_db`) — hrm-api + hrm-client.

## Một dòng
Port đầy đủ như ERP (Hướng A): loại 14 thêm **Nhóm VAT** (dropdown required), **Chọn nhóm hàng hóa** (multi-select required → mỗi nhóm = 1 tab chi tiết, lưu N bản ghi `product_export_request_tabs`), **Tên viết tắt** + **Địa chỉ giao hàng** (hiển thị). SĐT đã có. **Không migration.**

## Phạm vi
- BE: `ProductExportRequestController` (createData/editData trả `customer_unit`, `delivery_place`, `tabs[]`, `selected_tab_ids`; rules thêm `firm_tab_ids`), `ProductExportRequestService` (tạo/sửa lặp N tab theo nhóm).
- FE: `ProductExportRequestForm.vue` (panel 2 field; Nhóm VAT + Chọn nhóm hàng hóa; nav-tabs chi tiết; submit gom mọi nhóm).

## Ngoài phạm vi
Loại 15 khuyến mại; 3 check phụ (công nợ/lệch giá/support_accounting) — vẫn skip như đợt type-14.
