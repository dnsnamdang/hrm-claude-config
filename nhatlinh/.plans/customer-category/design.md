# Danh mục Khách hàng (Category) — Tóm tắt

**Ngày:** 2026-06-05 · @manhcuong · Spec: `docs/superpowers/specs/2026-06-05-customer-category-design.md`
**Thuộc:** MODULE 1 (DM-05)

## Scope
Tạo danh mục Khách hàng MỚI trong module Category (`/category/customers`) — KH chính thức ERP (Hợp đồng tham chiếu). Pattern gần giống `suppliers`: CRUD + nhiều liên hệ + địa chỉ Tỉnh/Phường + phân loại trường học. **Cấm xóa, chỉ Khóa.**

## Quyết định chính
- 2 bảng: `customers`, `customer_category_contacts`. Mã `KH.xxxx`.
- school_type enum: 1=TH,2=THCS,3=THPT,4=MN,5=Khác.
- Địa chỉ Tỉnh→Phường cascading + số nhà/đường. Nhiều liên hệ (bảng con).
- Cấm xóa. Import phẳng (không liên hệ). 2 permission mới.
