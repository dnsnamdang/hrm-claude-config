# Design — customer-manager (TÓM TẮT)

@manhcuong · 2026-06-10

> Spec chi tiết: `docs/superpowers/specs/2026-06-10-customer-manager-design.md`

## Mục tiêu
Màn **Quản lý khách hàng** HRM (`/assign/customers/:id/manager`) tương đương ERP `admin/customers/{id}/manager`, full edit, 6 tab, chia 3 phase.

## Quyết định lớn (đã chốt)
1. Route mới `/:id/manager` (vỏ tab), giữ `/:id` readonly cũ.
2. Full edit như ERP.
3. 3 phase: P1 = Thông tin chung + Liên hệ + Thông tin khác; P2 = Báo giá + Hợp đồng; P3 = Danh sách trang thiết bị.
4. Tab 1/2 tách đúng ERP (refactor CustomerForm → section dùng chung, tái dùng API save).
5. Tab 6 đầy đủ: ảnh + tài liệu PDF + video (S3 + ghi ERP).

## Tái dùng
- Tab 1/2: `CustomerService::show/save` + `CustomerForm.vue` đã đủ (chỉ tách section + dựng tab).
- Tab 4: `TpContractService::index?customer_id=` khớp ERP.
- Tab 3: HRM `/assign/quotations` đọc bảng HRM-local → cần BE đọc ERP (P2).
- Tab 5 + Tab 6: chưa có, làm mới.

## Kiến trúc FE
- `pages/assign/customers/_id/manager/index.vue` (vỏ tab) + 6 component tab trong `components/assign-components/customer/manager/`.

## Link
- Spec: `docs/superpowers/specs/2026-06-10-customer-manager-design.md`
- Plan: `.plans/customer-manager/plan.md`
