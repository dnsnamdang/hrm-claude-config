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

## Phase 3: Chuyển màn Kho vật lý / Kho kế toán sang V2 — @khoipv

> Quyết định 09/11/2026: không phân quyền theo cấp (giữ nguyên) · `is_can_delete`: Kho vật lý chỉ xóa khi
> chưa có kho kế toán nào trỏ tới (mọi trạng thái — khớp `WarehouseService::delete`), Kho kế toán luôn xóa được ·
> thêm cột Người tạo/Ngày tạo (hiện), Người cập nhật/Ngày cập nhật (ẩn mặc định).

### BE
- [x] Resource Kho vật lý + Kho kế toán: thêm `is_can_delete`, `created_by_name`, `created_at` (d/m/Y H:i), `status_text`
- [x] Service: lọc theo mọi cột (code, name, address, stocker/accountant, kho vật lý, nhập xuất thẳng, người tạo, ngày tạo, người cập nhật, ngày cập nhật) + sort whitelist (`id desc` cuối)
- [x] Migration thêm cột `warehouse_warehouses`, `warehouse_accounting_warehouses` vào `column_customizations` + casts
- [x] Route `GET filter-options` (2 nhóm) cho option bộ lọc Thủ kho / Kế toán kho / Người tạo / Người cập nhật / Kho vật lý
- [x] Request: `stocker_ids` / `accountant_ids` thành `required|array|min:1` (FE có dấu * nhưng BE trước đây không bắt)

### FE
- [x] `pages/warehouse/warehouses/index.vue` → V2 (SmartFilterPanel, DataTable, RowActions, Excel, Cấu hình cột, BaseConfirmModal)
- [x] `pages/warehouse/accounting_warehouses/index.vue` → V2
- [x] Modal Kho vật lý → V2BaseModal + formValidateMixin (`pages/warehouse/warehouses/components/WarehouseFormModal.vue`)
- [x] Modal Kho kế toán → V2BaseModal + formValidateMixin (`pages/warehouse/accounting_warehouses/components/AccountingWarehouseFormModal.vue`)
- [x] Compile check + scss check + test BE bằng script tạm
- [ ] Hỏi user: xóa 2 modal cũ không còn dùng `components/modal/WarehouseModal.vue`, `AccountingWarehouseModal.vue`
- [ ] Môi trường khác: chạy migration `2026_11_09_000001_add_warehouse_catalog_lists_to_column_customizations_table`

## Phase 4: Skill popup màn danh mục (port từ hrm) — @khoipv

> Nguồn hrm: `pages/master-data/product-natures/AddProductNatureModal.vue` + `index.vue`, skill hrm
> `list-page` mục 3a, `modal-popup` mục 0/3c. dns không có `SystemInfoSection`/`catalog_histories`.

- [x] Tạo `.claude/skills/catalog-popup/SKILL.md` (1 popup cho Tạo mới/Sửa/Xem, mã mở popup Xem, footer theo chế độ, Lưu và tiếp tục, ô Trạng thái khoá theo `can_lock`, tải chi tiết trước khi mở, reset ở `@hidden`)
- [x] Gắn skill vào bảng "Skill bắt buộc đọc theo ngữ cảnh" của CLAUDE.md + trỏ chéo từ `modal-popup`, `list-page`
- [x] (Chờ user → đã chốt làm, xem Phase 5) Áp khuôn `catalog-popup` cho 2 popup kho: chế độ Xem khi bấm mã, `open({ id, view })`, Lưu và tiếp tục, khoá ô Trạng thái theo `can_lock`, toast Tạo mới/Cập nhật

### Checkpoint — 09/11/2026 (wrap up)
Vừa hoàn thành: Phase 3 — 2 màn Kho vật lý / Kho kế toán lên V2 (BE lọc mọi cột + filter-options + is_can_delete + migration column_customizations; FE list V2 + 2 popup V2BaseModal); Phase 4 — skill `catalog-popup` (gắn CLAUDE.md, modal-popup, list-page)
Đang làm dở: —
Bước tiếp theo: user test tay 2 màn `/warehouse/warehouses`, `/warehouse/accounting_warehouses`; trả lời 2 câu treo: (a) xóa 2 modal cũ `components/modal/WarehouseModal.vue`, `AccountingWarehouseModal.vue`? (b) áp khuôn `catalog-popup` cho 2 popup kho?
Blocked: môi trường khác cần chạy migration `2026_11_09_000001_add_warehouse_catalog_lists_to_column_customizations_table`

## Phase 5: Áp khuôn `catalog-popup` cho 2 popup kho — @khoipv (09/11/2026)
- [x] FE `WarehouseFormModal.vue`: `open({ id, view })` tải chi tiết trước khi mở, chế độ Xem (mọi ô disabled, không `*`, footer Đóng), Lưu và tiếp tục (chỉ Tạo mới), ô Trạng thái khoá theo `can_lock`, toast Tạo mới/Cập nhật, 404/403, icon `ri-store-2-line`
- [x] FE `AccountingWarehouseFormModal.vue`: như trên (kho kế toán không có ràng buộc khoá → ô Trạng thái không khoá)
- [x] FE 2 màn danh sách: Mã → `openView`, Sửa → `openEdit`, Tạo mới → `openCreate`, `<XFormModal ref="formModal" @saved="loadData" />`, bỏ `editingId`/`formModalId`
- [x] BE `WarehouseService::updateOrCreate`: chặn đổi Hoạt động → Khóa khi còn kho kế toán đang hoạt động trỏ tới (cùng luật `toggleStatus`)
- [x] Compile check + cập nhật skill `catalog-popup` mục 8 (2 popup kho đã theo khuôn)
  - Đã chạy: compile check 4 file OK; script BE (transaction rollback): khóa qua Sửa khi còn KT hoạt động → chặn, giữ Hoạt động → OK, KT đã khóa → khóa được

- [x] Commit + push `thanhan-dev` (09/11/2026, theo yêu cầu user): API `e0d8dbad`, Client `3a17c37b` — gồm cả bảng MISA, PGH chờ nhập kho, danh mục kho V2
