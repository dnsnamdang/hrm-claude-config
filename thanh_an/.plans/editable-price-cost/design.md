# Editable Price Cost — Tóm tắt

**Người phụ trách:** @khoipv  
**Ngày:** 2026-04-23  
**Spec chi tiết:** `docs/superpowers/specs/2026-04-23-editable-price-cost-design.md`

---

## Mục tiêu

Cho phép user nhập tay giá trị `price_cost` (Giá vốn) trong bảng sản phẩm báo giá, và tự động tính lại `price_difference_coefficient` khi thay đổi.

## Scope

- Chỉ thay đổi `hrm-thanhan-client/pages/plan/quotation/components/ProductComponent.vue`
- Không thay đổi API, không thay đổi schema DB

## Quyết định lớn

- Dùng `currency-input` luôn hiển thị (như `price`, `qty`) thay vì pattern toggle "Sửa"
- Khi đổi unit → `updatePrice()` override `price_cost` từ bảng giá, user có thể sửa tiếp
- Chỉ tính lại `price_difference_coefficient` cho `import_type_id == 2` (phân phối lại)
