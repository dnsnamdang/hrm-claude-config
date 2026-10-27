# Phiếu xuất điều chỉnh sai số liệu — Plan

**Người phụ trách:** @khoipv · Design: `design.md` · Nhánh `develop` (cả 2 repo)

User chốt 27/10/2026: 4 quyền xem theo cấp mới · chuẩn hoá luôn màn chi tiết đã có · làm đủ Lịch sử + In phiếu + màu trạng thái SRS.

## Phase 1 — Màn danh sách + chuẩn hoá chi tiết

### BE (hrm-api)
- [x] B1. Seeder: 4 quyền "Xem phiếu xuất lại theo tổng công ty / công ty / phòng ban / bộ phận" (type 21 Kho, group "Phiếu xuất điều chỉnh sai số liệu")
- [x] B2. `WarehouseReExportService`: màu "Chờ nhập lại" đỏ → vàng `#D97706`; `scopedQuery()` (checkPermissionListWithColumn 4 cấp + phiếu mình tạo); `listQuery/listRows/filterOptions`; `detail()` thêm cờ + creator_name thuần; `canView` = trong phạm vi HOẶC xem được PNK gốc
- [x] B3. Controller mới `WarehouseReExportController` (Finance): index · filter-options · export-rows · {id} · {id}/print-data · {id}/histories(+filter-options). Route cũ `/warehouse-reexports/{id}` chuyển sang controller mới, bỏ `WarehouseImportController::reExportShow`
- [x] B4. Bản in: blade `finance::prints.warehouse-reexport` (ERP gọi hằng `ReportTemplate::PHIEU_XUAT_LAI` KHÔNG tồn tại → In ERP lỗi; HRM tự dựng mẫu, không ghi `report_templates`), letterhead theo `company_id` phiếu
- [x] B5. Lịch sử: khai `warehouse_reexports` ở `CatalogHistoryService::GATED_TABLES`; ghi `create` khi tạo (`WarehouseReExportService::store`), `change_status` Chờ nhập lại → Đã nhập lại khi tạo phiếu nhập lại (`WarehouseImportWriteService::reImport`)
- [x] B6. Smoke test API (index / filter / sort / export-rows / show / print / histories, 2 góc nhìn quyền)

### FE (hrm-client)
- [x] F1. `pages/finance/warehouse-reexports/index.vue` — khuôn `pages/warehouse/inventory-imports/index.vue` (4 mixin, SmartFilterPanel floating, Công ty–Phòng ban, sort, Xuất Excel, Cấu hình cột, Lịch sử popup)
- [x] F2. `components/constants.js` + `row-actions.js` (Tạo phiếu nhập lại · In · Lịch sử) dùng chung danh sách + chi tiết
- [x] F3. Chuẩn hoá `_id/index.vue`: V2BaseFormCard + CreatorInfoLine, bảng "Chi tiết" no-body-padding, SystemInfoSection, V2Footer, 404 không toast, Quay lại → danh sách
- [x] F4. Menu Kho › Xuất kho: mục "Phiếu xuất điều chỉnh sai số liệu" → `/finance/warehouse-reexports`
- [x] F5. `warehouse-imports/_id/re-export.vue`: tạo xong về danh sách phiếu xuất lại (như ERP `warehouseReExport.index`)
- [x] F6. Compile check + grep checklist skill erp-to-hrm-screen
- [x] F7. (User 27/10) Màn chi tiết: bỏ ô Trạng thái trong khối Thông tin chung (trạng thái vẫn hiện trên tiêu đề trang)
- [x] F8. (User 27/10) Màn chi tiết: Ghi chú lên cùng hàng Người giao hàng (col-md-8, ô 1 dòng V2BaseInput)

### Checkpoint — 27/10/2026
Vừa hoàn thành: B1–B6 + F1–F6 (chưa commit — theo CLAUDE.md).
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/finance/warehouse-reexports` (danh sách, lọc, Cấu hình cột, Xuất Excel, Lịch sử, In) + màn chi tiết; deploy chạy `PermissionsTableSeeder` rồi admin gán 4 quyền xem.
Blocked:
