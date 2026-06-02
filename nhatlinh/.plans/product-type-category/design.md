# Danh mục Loại hàng hoá (ProductType)

**Module:** Category
**Pattern:** Clone từ Hãng sản xuất (Manufacturer)
**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-manufacturer-category-design.md` (cùng pattern)

## Scope

- CRUD danh mục Loại hàng hoá với code `LHH.XXXX`
- Import/Export Excel
- Lock/Unlock
- Không có quan hệ many-to-many
- Permission: Quản lý/Xem danh mục loại hàng hoá (id 1091, 1092)

## Quyết định

- Table name: `product_types`
- Code prefix: LHH (8 ký tự tổng)
- isCanDelete luôn true (chưa có liên kết)
