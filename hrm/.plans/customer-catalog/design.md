# Danh mục Khách hàng (Assign) — Design (tóm tắt)

## Mục tiêu
Thêm menu cấp 2 "Danh mục Khách hàng" trong menu "Danh mục" (module Giao việc / Assign),
ngay phía trên "Lĩnh vực khách hàng". Xem danh sách + thêm/sửa khách hàng (form đầy đủ như ERP),
khi Lưu ghi đồng thời vào DB ERP (TanPhatDev) và DB HRM.

## Quyết định lớn (đã chốt)
- **Cách ghi ERP**: A — ghi thẳng DB qua `mysql2` (model `TpCustomer`).
- **Nơi lưu**: cả 2 — ERP `dev_erp.customers` + HRM `customers`, link bằng `code`. Ghi ERP trước → HRM.
- **Danh sách**: đọc từ HRM. **Mã KH**: tự sinh giống ERP. **created_by**: `employee_info_id` (≡ ERP employees.id).
- **Dropdown**: tái dùng select HRM sẵn có; riêng Nhóm KH đọc từ ERP (HRM chưa có `customer_groups`).
- **UI**: list V2BaseFilterPanel + V2BaseDataTable; form trang riêng `/assign/customers/add` + `/edit`.
- **Phân quyền cấp**: không. **Xóa**: không. **Permission**: Quản lý / Xem danh mục khách hàng (Timesheet seeder).

## Ngoài phạm vi v1
Xóa KH; Import/Export Excel; phân quyền cấp; CRM sync/history/cascade của ERP; các bảng ERP phụ
(customer_accounts, delivery_places, vehicle_manufacts).

## Trạng thái
Spec done — chờ duyệt → lên plan.

## Link spec chi tiết
docs/superpowers/specs/2026-06-09-customer-catalog-design.md
