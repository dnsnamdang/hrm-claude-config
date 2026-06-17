# Danh mục Nước sản xuất (CountryOfOrigin)

**Module:** Category
**Pattern:** Clone từ Hãng sản xuất (Manufacturer)
**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-manufacturer-category-design.md` (cùng pattern)

## Scope

- CRUD danh mục Nước sản xuất với code `NSX.XXXX`
- Import/Export Excel
- Lock/Unlock
- Không có quan hệ many-to-many
- Permission: Quản lý/Xem danh mục nước sản xuất (id 1089, 1090)

## Quyết định

- Table name: `country_of_origins`
- Code prefix: NSX (8 ký tự tổng)
- isCanDelete luôn true (chưa có liên kết)
