# Phiếu xuất kho điều chỉnh kiểm kê — Plan

Người phụ trách: @khoipv · Nhánh `develop` (cả 2 repo, nhánh con `gop_db`)
Màn: `hrm-client/pages/warehouse/inventory-exports/` · BE: `Modules/Finance` (`WarehouseInventoryExportController`,
`InventoryExport/WarehouseInventoryExport{,Write}Service`). Khuôn: màn đối xứng Phiếu nhập kho điều chỉnh kiểm kê
(`pages/warehouse/inventory-imports`, `InventoryImport/*`) — copy pattern, khác ở chiều tồn (trừ lô) + cột Lô / Đơn giá / Thành tiền.

## User chốt 27/10/2026
1. Quyền **y ERP**: 2 quyền xem "Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty / - theo công ty" (guard api, type 21)
   + "Kế toán kho" (thấy phiếu Chờ duyệt, nút Tạo phiếu xuất hàng). KHÔNG thêm quyền Tạo — lập phiếu theo điều kiện ERP của phiếu
   kiểm kê (`SelfInventory::canInventoryExport()` = quyền "Xử lý phiếu kiểm kê hàng hóa" + còn hàng THIẾU + chưa có phiếu).
2. Ghi tồn **giống ERP** → mở rộng hàm chung `PhysicalStockWriter::exportLot()` bằng khoá ctx tuỳ chọn (log chi tiết type 3,
   qty_before theo log gần nhất mọi loại); nơi gọi cũ không đổi hành vi.
3. Giá cơ sở: dùng hàm chung. Thực tế đã có sẵn `ProductPriceReader::retailPrices($ids, 1, $companyId)` ⇒ không tạo service mới,
   `SelfInventoryWriteService::basePrices()` chuyển sang gọi hàm này (đối chiếu 11.423 mã × 5 công ty: 0 lệch).

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP (controller / model / blade / menu / SelfInventory::getForWarehouseInventoryExport)
- [x] Giá cơ sở: `SelfInventoryWriteService::basePrices()` → `ProductPriceReader::retailPrices()` (giữ trần SELL_PRICE_MAX ở chỗ cũ)
- [x] `PhysicalStockWriter::exportLot()`: ctx `detail_log_type`, `detail_log_before_any_type` (mặc định = hành vi cũ; ReExportTest 3/3, Type6 2/2 vẫn qua)
- [x] Entity `WarehouseInventoryExport` (STATUSES màu SRS, scopedQuery, canView/canEdit/canCreateProductExport)
- [x] `WarehouseInventoryExportService` (list/filter/detail/source THIẾU + lô + giá/export rows/in mẫu 297–298)
- [x] `WarehouseInventoryExportWriteService` (store/update, kiểm tồn kế toán qua AccountingStockService, Gửi duyệt trừ tồn, file, thông báo, lịch sử)
- [x] Controller + routes `finance/warehouse-inventory-exports`
- [x] Seeder 2 quyền xem (`permission:sync --dry-run` OK); đăng ký `warehouse_inventory_exports` trong CatalogHistoryService::TABLES
- [x] SelfInventoryService: `inventory_export_create_path` trỏ màn HRM (bỏ `ERP_INVENTORY_EXPORT_PATH` / `erp_inventory_export_path`)
- [x] Feature test `WarehouseInventoryExportApiTest` — 10/10, 75 assertion

### FE
- [x] `pages/warehouse/inventory-exports/` index / create / _id/index / _id/edit + components (Form, constants, row-actions)
- [x] Menu Kho › Xuất kho; nút "Tạo phiếu xuất kho điều chuyển" ở Chi tiết phiếu kiểm kê → màn HRM; Thẻ kho link sang HRM
- [x] Verify: vue-template-compiler + babel 10 file OK; grep checklist sạch; smoke API Super admin trên PXKĐCKK-00016 (9 endpoint 200)
- [x] Test Playwright (user yêu cầu 27/10, tài khoản DNS Admin, local): danh sách + 8 ô lọc + tìm nhanh/Làm mới/sort/số dòng (1 request/thao tác), In phiếu, In danh sách, Xuất Excel (file đủ logo/khối ký), Cấu hình cột, Lịch sử popup; Chi tiết (trạng thái trên tiêu đề, 10 cột ERP); 404 không toast; Thêm không nguồn / nguồn không hợp lệ; luồng thật từ Chi tiết phiếu kiểm kê → validate → cảnh báo chưa lưu → Lưu nháp → Sửa → Lịch sử 2 mốc; Gửi duyệt chỉ tới popup (không trừ tồn thật). Dữ liệu test dọn theo id, tồn lô không đổi.
- [ ] Chưa test qua UI: tải file thật lên S3, Gửi duyệt thật (trừ tồn — đã có PHPUnit), ô lọc Ngày tạo, tài khoản không phải Super admin

## Phase 2 — Chọn phiếu kiểm kê ngay trên màn Thêm (user yêu cầu 27/10/2026)

ERP mở form rỗng từ nút "Tạo mới" nhưng không lập được (chọn kho → `self_inventories/undefined/...` → lỗi 500
`canInventoryExport() on null`, SelfInventoriesController:619). HRM thêm ô chọn Phiếu kiểm kê (ERP không có — user chốt).

- [x] BE: `GET /source-options` — phiếu kiểm kê lập được (y `canInventoryExport`: trạng thái Chờ xử lý / Đang xử lý + quyền "Xử lý
      phiếu kiểm kê hàng hóa" + còn hàng thiếu + chưa có phiếu xuất điều chỉnh), tính bằng 1 câu SQL (không N+1, ~35ms trên 16.588 dòng kết quả). Không bó `SelfInventory::scopedQuery()` — người có quyền Xử lý xem được mọi phiếu Chờ/Đang xử lý (`canView` → `canHandle`)
- [x] FE: bỏ khối chỉ dẫn; màn Thêm luôn hiện form, ô Phiếu kiểm kê (select, bắt buộc) → chọn thì nạp kho + hàng thiếu; Kho khoá kèm ⓘ
      khi chưa chọn phiếu; validate FE + câu lỗi chuẩn; vào từ Chi tiết phiếu kiểm kê (`?self_inventory_id=`) vẫn chọn sẵn; phiếu không còn lập được ⇒ báo dưới ô
- [x] Fix khi test: ô select kẹt khoá sau khi nạp — `v-select2-component` không theo dõi `disabled` ⇒ `:key` theo trạng thái khoá
- [x] Test BE 12/12 (thêm 2 ca source-options); Playwright: Tạo mới → validate 3 ô → chọn / bỏ chọn / chọn lại phiếu → Lưu nháp → phiếu biến khỏi danh sách chọn → URL phiếu đã dùng báo lỗi dưới ô. Dữ liệu test dọn theo id

- [x] User 27/10: Ghi chú lên cùng hàng Phiếu kiểm kê / Kho — `col-md-6` + `V2BaseTextarea` 2 dòng (user đổi lại từ ô 1 dòng); Người duyệt / Ngày duyệt xuống hàng 2 ở Chi tiết. Playwright: 3 ô cùng hàng, Ghi chú cao 53px, viền đỏ khi lỗi

### Checkpoint — 2026-10-27
Vừa hoàn thành: Phase 1 BE + FE, test BE 10/10, smoke API, compile FE
Đang làm dở: —
Đã push 27/10: hrm-api `ddeda3326`, hrm-client `015c39a1c` (develop).
Bước tiếp theo: khi deploy cần chạy seeder quyền + admin gán 2 quyền xem
Blocked:
