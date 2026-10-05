# Plan — 5 danh mục Xe (ERP → HRM)

Nhánh `gop_db` · @namdangit · Khuôn copy: `.plans/gop-db/product-classification-catalogs`
(BE `Modules/MasterData/**/ProductClassification`, FE `pages/master-data/product-natures`)

## Phase 1 — Nền dữ liệu & quyền

### BE
- [x] Migration `add_code_status_to_vehicle_catalogs`: thêm `code` (unique) cho 5 bảng xe
- [x] Migration: thêm `status` (default 1) cho `vehicle_life`
- [x] ~~Migration đổi `status = 0` → `2`~~ → BỎ: giữ nguyên 1/0 của ERP, ánh xạ 0 ⇄ 2 ở Entity
- [x] Migration: backfill mã `HX./DX./PLX./MDX./DOX.` + 4 số theo thứ tự id
- [x] Migration: thêm index cho các cột khóa ngoại dùng kiểm tra "đang sử dụng"
- [x] `PermissionsTableSeeder`: 10 quyền id 1590–1599, group `Danh mục xe`, type 9

## Phase 2 — Backend 5 danh mục

### BE
- [x] 5 Entity `Vehicle/*.php` extends `BaseCatalogModel` (prefix mã, quan hệ cha–con, `description ⇄ note`)
- [x] `BaseVehicleCatalogModel`: `isCanDelete()` cộng thêm kiểm tra bảng nghiệp vụ đang tham chiếu
- [x] 5 Service extends `BaseCatalogService` (lọc riêng, cột lịch sử, cấu hình import cha)
- [x] 5 Request extends `BaseCatalogRequest` (+ `ChecksParentCatalog` cho Phân loại xe / Model xe)
- [x] 5 Resource extends `BaseCatalogResource` (tên + cờ khóa của danh mục cha)
- [x] 5 Controller extends `BaseCatalogController`
- [x] `Routes/api.php`: thêm 5 slug vào vòng lặp `$productCatalogs` (tách mảng riêng `$vehicleCatalogs`)
- [x] `CatalogHistoryService::TABLES`: khai 5 bảng + nhãn cột tiếng Việt
- [x] `ExportColumnRegistry::COLUMNS`: khai cột xuất Excel cho 5 màn

## Phase 3 — Frontend 5 màn

### FE
- [x] `utils/vehicle-catalog.js`: hằng dùng chung (trạng thái, tooltip, nạp option cha)
- [x] `pages/master-data/vehicle-manufacts/` — index.vue + AddVehicleManufactModal.vue
- [x] `pages/master-data/vehicle-categories/` — index.vue + modal
- [x] `pages/master-data/vehicle-brands/` — index.vue + modal (ô chọn Hãng xe)
- [x] `pages/master-data/vehicle-models/` — index.vue + modal (Hãng xe → Phân loại xe phụ thuộc)
- [x] `pages/master-data/vehicle-life/` — index.vue + modal
- [x] `components/subsystem-menu/master-data.js`: nhóm menu **Danh mục xe** (5 mục + `isShow` quyền)

## Phase 4 — Tự kiểm & verify

- [x] Chạy grep checklist của skill `erp-to-hrm-screen` trên 5 thư mục màn
- [x] Đối chiếu ngược ERP: đủ cột, đủ ô lọc, đủ hành động + điều kiện ẩn/hiện
- [ ] Verify trình duyệt (Playwright MCP, cổng 3002): CRUD + khóa/mở khóa + xuất + import 5 màn

## Việc phát sinh trong lúc làm

- [x] Thêm hook `duplicateNameScopeColumns()` vào trait dùng chung `ImportsCatalogRows`
      (user duyệt 22/09/2026) — ERP chỉ cấm trùng tên trong phạm vi cấp cha, 112 model xe đang
      trùng tên nhau. Mặc định rỗng nên 6 danh mục hàng hóa giữ nguyên hành vi;
      `ProductClassificationCatalogTest` 11/11 pass sau khi sửa.

### Checkpoint — 22/09/2026
Vừa hoàn thành: BE 5 danh mục (migration, quyền, entity/service/request/resource/controller, route,
lịch sử, cột xuất Excel) + FE 5 màn + nhóm menu "Danh mục xe". Đã test API thật trên cổng 8003:
danh sách/tạo/sửa/khóa/mở khóa/xóa, chặn sửa khi khóa, chặn xóa khi đang dùng, trùng tên theo phạm vi
cấp cha, phân loại lệch hãng, getAll theo cha, export .xlsx, import validate, API lịch sử.
Đang làm dở: chưa bấm thật trên trình duyệt (cổng 3002) — 5 route đã biên dịch trả 200.
Bước tiếp theo: verify UI bằng Playwright MCP theo checklist skill erp-to-hrm-screen mục 6.
Blocked:
