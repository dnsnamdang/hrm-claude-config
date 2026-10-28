# Design — Theo dõi theo kho

> Phụ trách: @khoipv · Tạo 27/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-27-theo-doi-theo-kho-design.md`

## Mục tiêu

Port màn ERP *Kho › Theo dõi theo kho* sang HRM. Màn chỉ để xem:
1. `/warehouse/warehouse-tracking`: danh sách kho (ERP `warehouse.forActivities`);
2. `/warehouse/warehouse-tracking/{id}`: bảng hoạt động nhập / xuất của 1 kho (ERP `warehouse.activities`). Dùng cùng bảng với
   màn *Hoạt động kho* (`/warehouse/activities`), chỉ khác phạm vi kho.

## Quyết định chính (user chốt 27/10/2026)

| Vấn đề | Chốt |
|---|---|
| Quyền | Dùng lại quyền HRM **"Quản lý kho"** (y ERP), BE gắn `checkPermission:Quản lý kho`, menu `isShow` cùng quyền |
| Phạm vi | Y ERP: người thường chỉ thấy kho của công ty mình; Super Admin thấy mọi công ty và có thêm ô lọc Công ty (`WarehouseCatalogScope`). Kho ngoài phạm vi → 404 |
| Dùng chung | Tách `WarehouseActivityService::listForWarehouses()`; dời `ActivitySummary` + `export-excel` sang `components/warehouse/activity/` + thêm `activity-table.js`. Màn Hoạt động kho giữ nguyên hành vi |
| Bố cục | 2 trang như ERP; bấm Mã/Tên mở cùng tab, có nút Quay lại, bộ lọc danh sách được giữ |
| HRM thêm vào | Ô tìm nhanh, Cấu hình cột, Xuất Excel ở cả 2 trang; danh sách có phân trang |
