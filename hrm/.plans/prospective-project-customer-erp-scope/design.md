# prospective-project-customer-erp-scope — Design (tóm tắt)

@dnsnamdang · 2026-06-09

## Mục tiêu
Sửa form Thêm/Cập nhật **Dự án tiền khả thi** (`/assign/prospective-projects/add|_id/edit`) để Nhóm lĩnh vực KH + Lĩnh vực KH **tự suy ra từ Khách hàng (ERP)** thay vì chọn tay, và thêm "Thêm nhanh khách hàng".

## Scope
- **Bỏ** radio "Chọn theo Nhóm ngành / Chọn theo Lĩnh vực KH" → luôn dùng luồng Nhóm ngành (`selection_mode='scope'` cố định).
- **Bỏ** 2 dropdown chọn tay Nhóm LVKH + Lĩnh vực KH khỏi `ProjectInfoSection`.
- **Thêm** 3 trường read-only trong `CustomerInfoSection`, auto-fill khi chọn KH:
  - Nhóm lĩnh vực khách hàng * (read-only)
  - Đối tượng tổ chức (read-only — `customer_type_text`, MỚI)
  - Lĩnh vực khách hàng * (droplist disabled, 1 option = scope của KH)
- **Thêm** icon `+` "Thêm nhanh khách hàng" → popup form rút gọn tạo KH sang ERP rồi auto-select.

## Quyết định chốt (đã hỏi user)
1. Giữ nguyên modal `AddCustomer` dùng chung (không sửa) để chọn KH; đảm bảo list tương ứng ERP (list HRM đã sync từ ERP).
2. Thêm nhanh = form **rút gọn** chỉ trường bắt buộc cốt lõi, lưu sang ERP (tái dùng `POST assign/customers`).
3. KH thiếu Nhóm/Lĩnh vực KH → để trống read-only, **BE báo required khi lưu**.

## Điểm kỹ thuật mấu chốt
- HRM `customers` đã có `customer_type`, `customer_scope_group_id`, `customer_scope_id` (sync từ ERP). **id catalog scope HRM ≡ ERP** → dùng thẳng cho `prospective_projects.customer_scope_*`.
- `prospective_projects.customer_id` = **HRM customer id** (relation `Modules\Human\Customer`), KHÔNG phải ERP id → sau quick-add phải tra HRM theo `code` để lấy HRM id.
- API tra cứu scope từ ERP theo `code` (không theo id, vì modal trả HRM id; `code` dùng chung 2 hệ).

## Tài liệu
- Spec chi tiết: `docs/superpowers/specs/2026-06-09-prospective-project-customer-erp-scope-design.md`
- Plan: `.plans/prospective-project-customer-erp-scope/plan.md`
