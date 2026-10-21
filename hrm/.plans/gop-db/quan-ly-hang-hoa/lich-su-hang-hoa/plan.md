# Plan — Lịch sử chỉnh sửa hàng hoá

> Design: `design.md` (cùng thư mục). Nhánh `gop_db` (checkout chính), không migration, không seeder. User cho "làm" 21/10/2026.

## BE (hrm-api)
- [x] `ProductHistoryService` (snapshot chung + phần công ty có tiền tố `c{id}|`, logCreate/logUpdate/logStatus/trackStatus/logDelete, logs lọc theo công ty, filterOptions)
- [x] `CatalogHistoryService::GATED_TABLES['products']` — nhãn cột
- [x] Gắn ghi: `ProductWriteService` (store / writeUpdate / updateAdmin / take)
- [x] Gắn ghi: `ProductLifecycleService` (lock / unlock / release / destroyTemp mềm; hardDelete xoá log)
- [x] Gắn ghi: `TempProductService::update` (7/8 → 6)
- [x] Gắn ghi: `PriceAskingRequestWriter` (moveProducts, setTempStatus + lý do Không duyệt)
- [x] Gắn ghi: `PriceCalculateWriter` (moveProducts, 5→2) · `PriceCalculateFinalizer` (releaseUnchosen, promoteProducts) · `ProductPriceApprovalService::markOwnerTrading`
- [x] Gắn ghi: `ProductCatalogService::sync`
- [x] Đọc: `GET master-data/products/histories/{id}` + `/histories/filter-options` (gate tại công ty đang làm — T3)
- [x] Script test TỪNG TRƯỜNG (transaction rollback) + PHPUnit có quyền / không quyền

## FE (hrm-client)
- [x] `ProductHistoryModal.vue` (khuôn `ProductPriceHistoryModal`)
- [x] `ProductListPage.vue` menu ⋮ "Lịch sử" (chỉ khi có quyền)
- [x] `_id/index.vue` khối Lịch sử ngoài card (khuôn meeting show)
- [x] Playwright MCP kiểm 2 nơi + spec e2e

## Phát sinh 21/10
- [x] Quyền ERP 101050 chỉ có guard `web` ⇒ HRM không dùng được. User chốt khai quyền HRM mới cùng tên (guard api, nhóm Hàng hoá, type 9)
  trong `PermissionsTableSeeder`; đã `permission:sync` vào `hrm_erp_20_10` (thêm 1, id 101130). Deploy prod phải chạy seeder quyền + admin gán.
- [x] Route đổi theo khuôn `SystemInfoSection`: `products/histories/{id}` (+ `/filter-options`).

### Checkpoint — 21/10/2026
Vừa hoàn thành: BE ghi + đọc, FE popup danh sách + khối chi tiết, script test từng trường (all đạt), PHPUnit 6/6 + 15 bộ liên quan xanh
(trừ `ProductReadApiTest::so_query_khong_tang_theo_so_dong` — N+1 màn danh sách, không đụng tới, chưa xác nhận có sẵn trên code gốc),
Playwright MCP 2 nơi + không quyền. Spec e2e mới `product-history-ui.spec.ts` + sửa `rowActionTitles` ở `products-lifecycle-ui` — CHƯA chạy.
Đang làm dở: —
Bước tiếp theo: user xem; chạy e2e khi user cho; commit/push khi user yêu cầu.
Blocked:
