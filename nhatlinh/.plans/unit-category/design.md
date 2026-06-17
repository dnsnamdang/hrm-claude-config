# Danh mục Đơn vị tính (Unit)

**Module:** Category
**Pattern:** Clone từ Hãng sản xuất (Manufacturer)
**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-manufacturer-category-design.md` (cùng pattern)

## Scope

- CRUD danh mục Đơn vị tính với code `DVT.XXXX`
- Import/Export Excel
- Lock/Unlock
- Không có quan hệ many-to-many
- Permission: Quản lý/Xem danh mục đơn vị tính (id 1093, 1094)

## Quyết định

- Table name: `units`
- Code prefix: DVT (8 ký tự tổng)
- isCanDelete luôn true (chưa có liên kết)
