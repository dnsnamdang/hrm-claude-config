# Khách "không bắt buộc VAT" ⇒ VAT 0% trên BG/HĐ hãng (ERP)

**Người phụ trách:** @junfoke — 2026-09-24

**Mục tiêu:** khách thuộc nhóm có cờ `customer_groups.no_require_vat` ⇒ mọi % VAT (hàng hoá, dịch vụ,
chi phí, vận chuyển) trên báo giá hãng + hợp đồng hãng = 0%, khoá không cho sửa; xuất hàng tự 0%.

**Đợt 1:** ERP `firm_quotations` + `firm_contracts`. **Đợt 2:** BG dự án TKT (HRM Assign) + đường đồng bộ
HRM→ERP `saveDataApi`.

**Quyết định chính:** ép 0 + khoá; BE là nguồn sự thật (helper `FirmVatExemption` + `Customer::isNoRequireVat`);
chứng từ cũ về 0 khi mở sửa & lưu lại (không script); không sửa `searchCustomer` dùng chung.

Spec đầy đủ: `erp/docs/superpowers/specs/2026-09-24-vat-khach-khong-bat-buoc-design.md`
