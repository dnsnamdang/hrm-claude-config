# Danh mục Hãng sản xuất (Manufacturer)

**Module:** Assign
**Pattern:** Clone từ Nhóm ngành (Scope) — đơn giản hóa (không many-to-many)
**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-manufacturer-category-design.md`

## Scope

- CRUD danh mục Hãng sản xuất với code `HSX.XXXX`
- Import/Export Excel
- Lock/Unlock
- Không có quan hệ many-to-many
- Permission: Quản lý/Xem danh mục hãng sản xuất

## Quyết định

- Table name: `manufacturers`
- Code prefix: HSX (8 ký tự tổng)
- isCanDelete luôn true (chưa có liên kết)
- Clone pattern Scope, bỏ industries_count/applications_count
