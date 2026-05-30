# Thêm cột "Sale phụ trách" — Tóm tắt

**Người phụ trách:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-05-22-sale-person-charge-column-design.md`

## Mục tiêu
Thêm cột "Sale phụ trách" vào màn danh sách khách hàng, hiển thị tên Sale (department_id = 83) + mảng hàng hoá họ phụ trách.

## Scope
- Sửa 3 file: CustomerService, CategoryCustomerResource, index.vue
- Không migration, không API mới, không filter mới

## Quyết định lớn
- **Phương án:** Eager load trong query chính (không API riêng, không subquery)
- **Join path:** `person_charge_business.employee_id` → `employees.id` → `employee_infos.id` (qua `employee_info_id`)
- **Format:** "Tên Sale (Mảng A, Mảng B)", nhiều sale xuống dòng
