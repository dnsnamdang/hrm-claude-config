# Danh mục kho — Plan

## Phase 1: Menu + Kho Vật Lý

### FE
- [x] Thêm mục "Danh mục kho" vào `utils/MenuCategory.js`
- [x] Tạo `pages/category/warehouses/index.vue` (danh sách + bộ lọc + phân trang)
- [x] Tạo `components/modal/CategoryWarehouseModal.vue` (form tạo/sửa)
- [x] Kết nối API GET list, POST, PUT, DELETE cho kho vật lý

### BE
- [x] Migration tạo bảng `warehouses` và `warehouse_stockers`
- [x] Model + Resource `Warehouse`
- [x] Controller + routes `category/warehouses`
- [x] Validation: code unique, name unique, num_houses >= 1
- [x] Auto-tạo N nhà kho trong transaction khi POST (num_houses lưu field, chưa có bảng sub-structure)

## Phase 2: Kho Kế Toán

### FE
- [x] Tạo `pages/category/accounting_warehouses/index.vue`
- [x] Tạo `components/modal/CategoryAccountingWarehouseModal.vue`
- [x] Logic toggle `is_import_export_direct` → show/hide kho vật lý
- [x] Kết nối API GET list, POST, PUT, DELETE cho kho kế toán

### BE
- [x] Migration tạo bảng `accounting_warehouses` và `accounting_warehouse_accountants`
- [x] Model + Resource `AccountingWarehouse`
- [x] Controller + routes `category/accounting_warehouses`
- [x] Validation: warehouse_id required khi is_import_export_direct=0
- [x] Block đổi warehouse_id nếu đã có phát sinh tồn kho (set null khi is_import_export_direct=1)

### Checkpoint — 2026-05-13
Vừa hoàn thành: Toàn bộ FE + BE cho cả 2 loại kho (Vật Lý + Kế Toán)
Đang làm dở: Không có
Bước tiếp theo: Test end-to-end trên browser, kiểm tra API responses
Blocked:
