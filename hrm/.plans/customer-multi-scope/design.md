# customer-multi-scope — Design (tóm tắt)

@manhcuong — 2026-06-15

## Mục tiêu
Đổi Khách hàng ↔ Lĩnh vực KH từ **1-1** sang **n-n** (1 khách nhiều lĩnh vực), ở **cả 3 codebase**: HRM API, HRM Client, ERP (TanPhatDev). Giữ **Nhóm đơn** làm bộ lọc — mọi lĩnh vực của 1 khách cùng 1 nhóm.

## Quyết định chính
- Pivot riêng `customer_customer_scopes` ở **cả HRM DB và ERP DB**. **Drop** cột `customers.customer_scope_id` cả 2. Giữ `customer_scope_group_id`.
- Form KH (HRM `/human/customers` + ERP `/sale/customers` + CRM + modal): ô Lĩnh vực → **multi-select** trong nhóm. Bắt buộc ≥1.
- **Dự án tiền khả thi**: chọn KH → 1 lĩnh vực auto-fill, nhiều thì cho chọn 1. Dự án vẫn lưu 1 lĩnh vực.
- **Gộp fix `CustomerScopeReader` (ERP)**: vốn JOIN `customer_scope_group_members` (đã drop ở feature trước) → đổi đọc cột `customer_scopes.customer_scope_group_id`.

## Phạm vi (đều sửa)
- **HRM API**: migration pivot; Human Customer (entity/service/2 request/resource); Assign CustomerService (ghi/đọc ERP pivot, getScopeByCode trả mảng, filter pivot), 2 request, CustomerDetailResource.
- **HRM Client**: CustomerScopeSelect, human+assign CustomerForm, customers filter, prospective-projects (add/edit/CustomerInfoSection).
- **ERP**: migration pivot; Customer model (scopes + searchByFilter pivot); CustomersController (validate ids + sync pivot + history); CustomerScopeReader (FIX); blade (customerForm, customerScopeJs, classes/Customer submit_data, init create/edit/search modal×2/CRM, edit map scopes).

## Rủi ro
- Drop cột ở DB ERP production — phải deploy hết code ERP rồi mới migrate, phối hợp thời điểm.

## Spec chi tiết
`docs/superpowers/specs/2026-06-15-customer-multi-scope-design.md`
