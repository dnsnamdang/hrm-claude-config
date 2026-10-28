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

## Fix #11893 — Lưu nháp / Lưu và tiếp tục / link phiếu kiểm kê (28/10/2026)

User chốt 28/10: nút "Lưu" đổi thành "Lưu nháp", CHỈ bắt chọn Phiếu kiểm kê (kho tự điền theo phiếu); Gửi duyệt vẫn bắt đủ như ERP.

- [x] BE `WarehouseInventoryExportWriteService::validate()/update()`: Ghi chú + File đính kèm chỉ bắt khi Gửi duyệt (CHO_DUYET)
- [x] FE `InventoryExportForm`: nút "Lưu nháp" — validate chỉ Phiếu kiểm kê; Gửi duyệt giữ validate đủ
- [x] FE: nút "Lưu và tiếp tục" ở màn Thêm (lưu nháp → mở form trống)
- [x] FE: link mở phiếu kiểm kê (tab mới) ở màn Thêm khi đã chọn — như phiếu nhập kho điều chỉnh
- [x] Verify: compile FE + API (nháp thiếu ghi chú/file → 200 trong transaction rollback; gửi duyệt thiếu → 422)

### Checkpoint — 28/10/2026 17:00
Vừa hoàn thành: #11893 — BE `validate()`: Ghi chú + File chỉ bắt khi Gửi duyệt (CHO_DUYET=1), `update()` chỉ bắt file khi gửi duyệt, `note ?? null`. FE: nút "Lưu nháp" (đầu dãy, ri-save-3-line) chỉ bắt Phiếu kiểm kê; "Lưu và tiếp tục" (màn Thêm, sau Gửi duyệt) lưu nháp rồi `resetForNext()`; icon link mở phiếu kiểm kê cạnh nhãn ở màn Thêm. Test `validate()` 7 tình huống qua reflection đúng; compile FE sạch. Store đầu-cuối CHƯA test được: DB local không còn phiếu kiểm kê nào lập được phiếu xuất điều chỉnh.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm trên dev.
Blocked:

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: fix #11893 ĐÃ PUSH `develop` 28/10 (hrm-api tới `ddd23d04c`, hrm-client tới `f8f362a51`).
Đang làm dở: —
Bước tiếp theo: QA kiểm lại trên dev, đóng issue Redmine.
Blocked:
