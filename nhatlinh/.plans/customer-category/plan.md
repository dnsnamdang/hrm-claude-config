# Danh mục Khách hàng (Category) — Plan

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit). BE smoke-test pass (school_type_name, isCanDelete=false, syncContacts). Bảng dùng `category_customers` (bảng `customers` đã thuộc Human). Permission 1101-1102. Còn: user test UI + tạo file mẫu import.

> Thực thi qua subagent-driven. Copy pattern `suppliers`. KHÔNG commit.
**Spec:** `docs/superpowers/specs/2026-06-05-customer-category-design.md`

## Phase 1 — BE (copy supplier, bỏ group, thêm school_type, cấm xóa)
- [ ] Migrations `customers` + `customer_category_contacts`
- [ ] Entities CustomerCategory + CustomerCategoryContact (isCanDelete=false, school_type)
- [ ] Request (school_type in:1-5, contacts)
- [ ] Service (filter school_type, syncContacts, import)
- [ ] Transformers (school_type_name, contacts)
- [ ] Controller (no delete) + Routes `/customers` + 2 permission (seeder+DB)
- [ ] Export

## Phase 2 — FE (copy suppliers)
- [ ] Menu "Khách hàng"
- [ ] index.vue (no delete, filter loại trường)
- [ ] AddCustomerModal (loại trường + địa chỉ cascading + liên hệ động)

## Phase 3 — Test
- [ ] CRUD, sync contacts, cascading, lock, cấm xóa, phân quyền
