# Danh mục kho — Tóm tắt

**Spec chi tiết:** `docs/superpowers/specs/2026-05-13-danh-muc-kho-design.md`
**Người thực hiện:** @namdangit
**Trạng thái:** Đang triển khai

## Mục tiêu

Bổ sung 2 loại kho vào module Category (menu nằm giữa hàng hóa và khách hàng):
1. **Kho Vật Lý** (`/category/warehouses`) — quản lý địa điểm thực tế, có thủ kho (multi-select), số nhà kho
2. **Kho Kế Toán** (`/category/accounting_warehouses`) — theo dõi tồn kho kế toán, có chế độ nhập/xuất thẳng, kế toán (multi-select)

## Scope

- FE: Menu + Danh sách + Modal tạo/sửa + Xóa cho cả 2 loại kho
- BE: Module Category, prefix API `category/warehouses` và `category/accounting_warehouses`
- UI: Modal (popup) theo pattern CategoryBankModal hiện có

## Quyết định lớn

- Form tạo/sửa dùng modal (không dùng trang riêng)
- `num_houses` chỉ hiển thị khi tạo mới kho vật lý, ẩn khi sửa
- `warehouse_id` bắt buộc khi `is_import_export_direct = 0`, ẩn khi = 1

## Cập nhật 09/11/2026 — chuyển V2 (@khoipv)

- Màn hiện nằm ở phân hệ Kho: `pages/warehouse/warehouses`, `pages/warehouse/accounting_warehouses` (API `warehouse/warehouses`, `warehouse/accounting_warehouses`)
- List V2: `V2BaseSmartFilterPanel` (lọc mọi cột) + `V2BaseDataTable` + `V2BaseRowActions` (Sửa · Khóa/Mở khóa · Xóa) + Xuất Excel + Cấu hình cột (`column_customizations.warehouse_warehouses` / `warehouse_accounting_warehouses`)
- Không phân quyền theo cấp
- `is_can_delete`: Kho vật lý chỉ xóa khi chưa có kho kế toán nào trỏ tới; Kho kế toán luôn xóa được
- Cột Người tạo / Ngày tạo hiện; Người cập nhật / Ngày cập nhật ẩn mặc định
- Popup tạo/sửa: `WarehouseFormModal.vue`, `AccountingWarehouseFormModal.vue` (V2BaseModal + formValidateMixin); BE bắt buộc `stocker_ids` / `accountant_ids`
- Chuẩn popup danh mục: skill `.claude/skills/catalog-popup/SKILL.md` (2 popup kho chưa áp — chờ user)
