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

## Fix #11890 — UI phiếu xuất lại / nhập lại (28/10/2026)

User chốt: BỎ nút "Lưu và tiếp tục" (cả màn Nhập lại lẫn Xuất lại); màn Tạo phiếu xuất lại chỉ thêm dòng người tạo + giờ (CreatorInfoLine, góc phải như mọi form).

- [x] FE danh sách: tiêu đề "Danh sách phiếu xuất lại" (ERP `all/index.blade.php`)
- [x] FE danh sách: bấm sort cột Ngày tạo vỡ layout
- [x] FE Tạo phiếu xuất lại: dòng người tạo + giờ (CreatorInfoLine)
- [x] BE: tạo phiếu xuất lại (Chờ nhập lại) chưa ghi lịch sử
- [x] FE Nhập lại: khoá ô Người giao hàng (ERP `form.blade.php` input disabled)
- [x] FE+BE Nhập lại: Ghi chú trống → lấy ghi chú của Đề nghị nhập kho (ERP getter `WarehouseImport.note`)
- [x] FE Nhập lại: placeholder ô SL nhập (LotEditor)
- [ ] FE Nhập lại › Bốc xếp: chọn NCC xong các ô lệch hàng — CSS
- [x] FE Nhập lại › Bốc xếp: viền đỏ ô đang báo lỗi (Khối lượng…)
- [x] Verify: compile FE + API

### Checkpoint — 28/10/2026 16:00
Vừa hoàn thành: #11890 — BE `WarehouseReExportService::historyLogs()` dựng mốc "Tạo mới" cho phiếu cũ lập bên ERP (khuôn #11847; phiếu tạo ở HRM đã có log thật — test tạo trong transaction OK); `detail()` + `createData()` trả ghi chú ĐNNK. FE: tiêu đề danh sách, width cột (khuôn #11763), CreatorInfoLine màn Tạo phiếu xuất lại, khoá Người giao hàng ở Nhập lại, Ghi chú điền sẵn ghi chú ĐNNK (Tạo / Sửa / Nhập lại — y ERP getter), placeholder SL nhập, viền đỏ + tự gỡ lỗi tab Bốc xếp. Compile 5 file sạch.
Đang làm dở: mục "Bốc xếp chọn NCC xong vỡ font/lệch ô" — chưa tái hiện được bằng đọc code (V2BaseSelect và V2BaseSelectRemote dùng chung CSS `.v2-select`, cùng size sm 32px), cần mở trình duyệt.
Bước tiếp theo: user mở trình duyệt kiểm các mục + quyết cách xử lý mục Bốc xếp.
Blocked:

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: fix #11890 ĐÃ PUSH `develop` 28/10 (hrm-api tới `ddd23d04c`, hrm-client tới `f8f362a51`).
Đang làm dở: —
Bước tiếp theo: QA kiểm lại trên dev, đóng issue Redmine.
Còn treo: #11890 mục "Bốc xếp chọn NCC xong vỡ font/lệch ô" (màn Nhập lại) — chưa tái hiện được bằng đọc code, cần mở trình duyệt; sửa ở V2BaseSelectRemote (dùng chung) phải hỏi trước.
Blocked:

## Fix #11919 — Nhập lại › tab Bốc xếp (30/10/2026)

Nguyên nhân lệch ô (mục còn treo của #11890): `V2BaseLabel` — chữ nhãn `line-height: 1.2` nhưng dấu `*` kế thừa line-height 1.5 của trang → nhãn có `*` cao hơn ~3.6px, ô bên dưới tụt xuống. Chọn "Thuê ngoài" làm NCC/Loại bốc xếp/Khối lượng hiện `*`, riêng "Loại hình thuê" không có → ô đó lệch lên. Đo bằng HTML tĩnh + bootstrap: 22.4 vs 26.0px → sau fix 80.4 vs 80.4.

- [x] FE `components/V2BaseLabel.vue` (dùng chung — user đồng ý 30/10): `.v2-label__required { line-height: 1.2 }` → sửa cho mọi màn; đã bỏ style cục bộ tạm ở ArrangeDeliveryForm
- [x] FE `ArrangeDeliveryForm.vue`: placeholder ô Khối lượng hàng / Số giờ, VAT (%), Số tiền người nhận việc
- [x] Verify: compile template
