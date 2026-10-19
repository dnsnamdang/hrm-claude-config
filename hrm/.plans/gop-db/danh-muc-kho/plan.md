# Danh mục kho — Plan

> Design: `.plans/gop-db/danh-muc-kho/design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-19-danh-muc-kho-design.md`

## Phase 0 — Khảo sát (xong 19/10)

- [x] Khảo sát 8 màn ERP, đếm dữ liệu, chốt phạm vi 7 màn + thứ tự + 1 quyền "Quản lý kho"

## Phase 1 — Nhà kho

Khuôn: BE `Modules/MasterData/*/BusinessCatalog/JobGroup*` (danh mục có cha), FE `pages/master-data/job-groups/`.

- [x] Migration thêm `houses.status` (đã chạy trên gop_db local)
- [x] Quyền "Quản lý kho" (type 9, group "Danh mục kho") cuối `PermissionsTableSeeder` (đã `permission:sync` local)
- [x] BE: Entity `House`, Request, Resource, Service, Controller, route — `Modules/MasterData/*/Warehouse/`
- [x] Lớp phạm vi dùng chung cho cả nhóm: `Modules/MasterData/Services/Warehouse/WarehouseCatalogScope.php`
- [x] Đăng ký `CatalogHistoryService::TABLES['houses']`, `ExportColumnRegistry::COLUMNS['houses']`
- [x] FE: `pages/master-data/houses/index.vue` + `AddHouseModal.vue` (copy pattern `pages/master-data/job-groups/`)
- [x] Menu `master-data.js` nhóm "Kho" (7 mục, 6 mục chưa có link)
- [x] Kiểm: script HTTP kernel có rollback (quyền, phạm vi, validate, sinh dãy, khoá/mở/xoá, lịch sử, export, chéo công ty) + bấm thật Playwright

## Phase 2 — Dãy (xong 19/10)

- [x] Migration `rows.status`; Nhà kho đổi sang đếm dãy ĐANG HOẠT ĐỘNG khi khoá
- [x] BE `Row`, `RowRequest`, `RowResource`, `RowService`, `RowController` + route / export / lịch sử
- [x] Tách dùng chung: `WarehouseTreeCatalogController`, `Concerns\BuildsWarehouseTreeSql`, `WarehouseCatalogScope::houseOptions()`
- [x] FE `pages/master-data/rows/` (index + `AddRowModal.vue`), menu "Dãy" có link
- [x] Kiểm API (2 góc nhìn, validate trùng mã vị trí / vượt 10.000, khoá cha-con 2 chiều) + bấm thật Playwright

## Phase 3 — Khoang (xong 19/10)

- [x] Migration `spaces.status`; Dãy đổi sang đếm khoang ĐANG HOẠT ĐỘNG khi khoá; khoang sinh từ Dãy có `status = 1`
- [x] BE `Space`, `SpaceRequest`, `SpaceResource`, `SpaceService`, `SpaceController` + route / export / lịch sử
- [x] `WarehouseCatalogScope::rowOptions()`
- [x] FE `pages/master-data/spaces/` (index + `AddSpaceModal.vue`, dây chuyền 3 cấp), menu "Khoang" có link
- [x] Kiểm API (2 góc nhìn, khoá cha-con 2 chiều, chặn khoá/xoá khi còn vị trí) + bấm thật Playwright

## Phase 4 — Vị trí (xong 19/10)

- [x] Migration `positions.status`; Khoang đổi sang đếm vị trí ĐANG HOẠT ĐỘNG; vị trí sinh từ Dãy có `status = 1`
- [x] BE `Position` (29 cặp bảng tham chiếu, 4 bảng không index chỉ đếm khi xoá), Request (2 loại, kho theo khoang),
      Resource, Service, Controller + route / export / lịch sử; `WarehouseCatalogScope::spaceOptions()`
- [x] FE `pages/master-data/positions/` (index + `AddPositionModal.vue`), menu "Vị trí" có link
- [x] Ẩn bản ghi khoá ở Kế hoạch kiểm kê (`structure` + `PositionInventoryForm`) và popup chọn vị trí Phiếu nhập kho
- [x] Kiểm API (2 góc nhìn, cờ xoá khớp 200/200, đo export) + bấm thật Playwright (2 loại vị trí, form kiểm kê)

## Phase 5 — Kho vật lý (xong 19/10)

- [x] BE `PhysicalWarehouse` (global scope status 2, 53 cặp tham chiếu), Request, Resource, Service (sinh nhà + vị
      trí tách ghép, thủ kho, xoá kèm dữ liệu của chính kho), Controller (câu "Kho có tồn không thể khóa.")
- [x] FE `pages/master-data/warehouses/` (Thủ kho chọn nhiều), menu có link
- [x] Kiểm API 2 góc nhìn + bấm thật (tạo kho thật, xem DB sinh đúng)

## Phase 6 — Kho kế toán (xong 19/10)

- [x] BE `AccountingWarehouseCatalog` (phạm vi theo `company_id`, 12 cặp tham chiếu + 2 cột JSON công ty), Request
      (khoá đổi kho vật lý khi đã tồn, kể cả chuyển Nhập xuất thẳng), Resource, Service, Controller
- [x] FE `pages/master-data/accounting-warehouses/` (Nhập xuất thẳng ẩn Kho vật lý/Địa chỉ, khoá ô khi đã tồn), menu
- [x] Kiểm API (cờ xoá 48/48) + bấm thật

## Phase 7 — Kiện (xong 19/10)

- [x] BE `Package` + Request/Resource/Service/Controller; FE `pages/master-data/packages/`; menu
- [x] Kiểm API + bấm thật (tạo, xoá)

## Checkpoint — 2026-10-19

- **Vừa hoàn thành:** ĐỦ 7 màn (Nhà kho, Dãy, Khoang, Vị trí, Kho vật lý, Kho kế toán, Kiện) + ẩn bản ghi khoá ở
  Kế hoạch kiểm kê / Phiếu nhập kho; verify API + bấm thật local; DB local đã dọn về số ban đầu.
- **Đang làm dở:** —
- **Đã chuyển code (19/10):** toàn bộ sang nhánh `feat/chuyen-doi-hang-hoa` (user chỉ định), gộp 2 xung đột (seeder quyền,
  menu `master-data.js`); đổi tiền tố 4 migration thành `2026_10_19_10000{1..4}` vì nhánh có sẵn
  `2026_10_19_000001_create_company_product_natures_table`. Kiểm lại API + giao diện trên nhánh mới: đạt.
- **Bước tiếp theo:** user review → commit (2 repo, nhánh `feat/chuyen-doi-hang-hoa`); deploy chạy 4 migration
  `2026_10_19_10000{1..4}` + `PermissionsTableSeeder`; admin gán "Quản lý kho" vào VAI TRÒ (FE chỉ đọc quyền qua vai trò
  theo công ty); viết TC/HDSD nếu cần.
- **Còn ngỏ:** ô chọn kho ở màn HRM khác — đã kiểm 3 nguồn chính (`ProductTransferService::warehouseOptions`,
  `ProductImportRequestService::warehouseOptions`, `ProductExportRequestController::warehouses`) lọc sẵn `status = 1`
  nên kho khoá ở HRM tự ẩn; các nguồn còn lại chưa rà. Chưa chặn ở BE khi lưu phiếu (chỉ ẩn ở ô chọn). ERP không đọc
  `status` mới của nhà/dãy/khoang/vị trí.
- **Blocked / chờ user:** —
- **Ghi chú test:** quyền FE lấy QUA VAI TRÒ theo công ty (`role_has_permissions.company_id`), không lấy quyền
  gán thẳng — admin phải gán "Quản lý kho" vào vai trò mới thấy menu.
