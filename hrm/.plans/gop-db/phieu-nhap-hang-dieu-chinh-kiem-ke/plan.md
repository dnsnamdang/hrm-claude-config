# Phiếu nhập hàng điều chỉnh kiểm kê — Plan

Người phụ trách: @khoipv
Màn: `hrm-client/pages/finance/inventory-imports/` · BE: `Modules/Finance` (`InventoryImportController`,
`Services/InventoryImport/InventoryImportService` + `InventoryImportWriteService`, `Entities/InventoryImport/InventoryImport`)

## Phase 1 — Port màn (2026-10-30)

### BE
- [x] Quyền: 2 quyền xem tên y ERP vào `PermissionsTableSeeder` (type 8, group "Phiếu nhập hàng điều chỉnh kiểm kê")
- [x] Entity `InventoryImport` (STATUSES, scopedQuery, canView, canEdit, generateCode `PNHĐCKK-`)
- [x] Hàm chung giá nhập gần nhất — service MỚI `Finance/Services/ProductImportPriceReader::latestPrices()` (ERP
      `ProductImport::getImportPriceLatest`); không sửa `ProductPriceReader` (lớp giá bán theo công ty)
- [x] Hàm chung ghi nhập tồn kế toán — service MỚI `Finance/Services/AccountingStockWriter::import()` (tồn kế toán + log FIFO +
      `stocks.accounting_qty`). ⚠️ `ProductTransferAccountingService::addImportWarehouse()` (private) cùng logic — CHƯA chuyển
      sang dùng (màn đang chạy, chờ user đồng ý)
- [x] Service đọc `InventoryImportService`: danh sách / lọc / sort, chi tiết, nguồn (phiếu nhập kho Chờ duyệt + Kế toán kho),
      kho kế toán, nhân viên, xuất Excel, in phiếu (mẫu 296) / in danh sách (mẫu 295)
- [x] Service ghi `InventoryImportWriteService`: store / update y ERP (syncDetails + handled_qty, updateWarehouse, saveAccounting
      1561/3381, trạng thái phiếu nhập kho + phiếu kiểm kê có log), file đính kèm, lịch sử (đăng ký `CatalogHistoryService::TABLES`)
- [x] Controller `InventoryImportController` + route `finance/inventory-imports`
- [x] Phiếu nhập kho ĐCKK: cờ `product_import_erp_path` → `product_import_path` trỏ `/finance/inventory-imports/create?...`
      (sửa cả assert trong `WarehouseInventoryImportApiTest`)

### FE
- [x] `pages/finance/inventory-imports/` index / create / _id/index / _id/edit + `InventoryImportForm.vue` + constants + row-actions
      (danh sách dựng từ khuôn `pages/warehouse/inventory-imports/index.vue`; toolbar In trước Xuất theo chuẩn 28/10)
- [x] Menu `components/subsystem-menu/finance.js` gắn link (giữ nguyên nhãn)
- [x] Màn Phiếu nhập kho ĐCKK: nút "Tạo phiếu nhập hàng" mở màn HRM (row-actions + form), bỏ `openErp`

### Verify
- [x] `php -l` 9 file BE
- [x] Smoke API qua HTTP kernel (Super admin 13): danh sách / filter-options / chi tiết + in phiếu ERP id 1 / in danh sách /
      export-rows (thứ tự cột theo tick) / source-options / search-employees / histories → 200; source phiếu đã hạch toán → 404
- [x] Luồng ghi trong transaction ROLLBACK (không để lại dữ liệu): lệch SL kho kế toán → 422 "Số lượng nhập kho kế toán không
      khớp!"; Lưu → phiếu nhập kho 2 Đang hạch toán; Sửa + Lưu và duyệt → 4 Đã hạch toán, log tồn kế toán FIFO
      (`InventoryImportDetailAccWarehouse`), bút toán Nợ 1561 (product_id, group 1) / Có 3381 (employee 597 + tổ chức NV) khớp
      bản ghi ERP thật; sửa lần 2 → 409; lịch sử ghi đủ mốc
- [x] FE compile (vue-template-compiler + @babel/parser) 10 file + grep checklist skill sạch
- [x] Mở trình duyệt bấm thật: Playwright + user tự test OK (30/10)
- [ ] Chạy seeder quyền trên môi trường (`permission:sync --dry-run` trước)

### Ghi chú lệch ERP có chủ ý
- Trạng thái Đang tạo màu xám (ERP đỏ); nhãn "Người tạo/Ngày tạo"; câu lỗi tiếng Việt từng ô; thư mục S3 khi sửa
  `inventory_imports` (ERP ghi nhầm `inventory_exports`); ô lọc Mã/Tên hàng lọc thật (ERP có ô nhưng không lọc).
- Giữ y ERP theo user chốt 30/10: cộng `handled_qty` mỗi lần lưu (kể cả sửa), không chặn lập trùng, nhận dòng hàng FE gửi.

### Checkpoint — 2026-10-30
Vừa hoàn thành: Phase 1 BE + FE + verify API/compile
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt test luồng; quyết định có chuyển `ProductTransferAccountingService` sang `AccountingStockWriter`
và đổi link "Phiếu xử lý" ở Biên bản xử lý thừa thiếu (`InventoryAuditReportDetail::erpHandlePath` nhánh nhập) sang màn HRM không
Blocked:

## Chỉnh UI (2026-10-30)
- [x] Bỏ icon ⓘ ở nhãn "Kho" ("Kho lấy theo phiếu nhập kho, không đổi được.") và "Thủ kho" ("Người tạo phiếu nhập kho, không đổi được.") — `InventoryImportForm.vue`
- [x] Ô "Ghi chú" lên cùng dòng "Nhân viên" (col-md-3 + col-md-9, textarea 2 dòng giữ nguyên)

## Test Playwright local (2026-10-30, Super admin id 13)
- [x] Danh sách: 9 cột đúng, dòng PNHĐCKK-00001, bộ lọc nâng cao 8 ô (Mã phiếu · Kho · Trạng thái · Người tạo · Mã/Tên hàng · Ngày tạo · Công ty · Phòng ban), popup Lịch sử, In phiếu (mẫu 296 đủ bảng Kho kế toán), In danh sách (mẫu 295), Xuất Excel (popup 7/7 trường → tải `danh_sach_phieu_nhap_hang_dieu_chinh_kiem_ke.xlsx`)
- [x] Chi tiết phiếu ERP id 1: đủ ô + bảng, nút In / Quay lại
- [x] Phiếu nhập kho ĐCKK (tạm Chờ duyệt) → nút "Tạo phiếu nhập hàng" mở `/finance/inventory-imports/create?warehouse_inventory_import_id=1`, nạp sẵn dòng hàng + kho kế toán
- [x] Validate: Lưu trống → toast "Bạn chưa nhập đầy đủ thông tin." + báo đỏ Nhân viên / Kho kế toán cùng lúc; "Thêm kho" SL lệch → "Số lượng nhập kho kế toán không khớp!"; nút xoá dòng kho
- [x] Lưu (nháp) → PNHĐCKK-00004 Đang tạo, kèm file phiếu nhập kho, phiếu nhập kho → Đang hạch toán
- [x] Sửa → nạp lại Nhân viên + Kho kế toán; đổi đơn giá 2.000 → Lưu và duyệt (popup xác nhận) → Đã hạch toán: bút toán 1561/3381 = 2.000, log FIFO 2.600.000 → 2.602.000; vào lại /edit bị đá về Chi tiết; Lịch sử 3 mốc (đơn giá 1,000 → 2,000)
- [x] Sửa trong lúc test: bỏ `*` bắt buộc ở File đính kèm màn Chi tiết (chỉ màn Sửa); ô Số lượng kho kế toán căn phải
- [x] Dọn dữ liệu theo id + khôi phục snapshot (phiếu nhập kho 1, phiếu kiểm kê 575, kết quả 2063, tồn kế toán 4381, stocks) — kiểm lại khớp snapshot, 0 log sót
- [x] Bản in (mẫu 296 + 295): bỏ `<div style="height: 70px">` trước tên Người lập (cộng dồn với `.signature-space` 56px của `markSignatureSpace` → ~126px), tên in đậm — đo popup: khoảng "Người lập" → tên = 56px chuẩn print-page §8b
- [ ] Hỏi user: màn Phiếu nhập kho ĐCKK (`WarehouseInventoryImportService`) cũng chèn div 70px y hệt → có sửa theo không

### Checkpoint — 2026-10-30
Vừa hoàn thành: test Playwright toàn luồng + sửa 3 lỗi phát hiện (dấu * file ở Chi tiết, căn phải SL, khoảng ký bản in); dữ liệu test đã dọn, DB khớp snapshot
Đang làm dở: —
Bước tiếp theo: user xác nhận; chạy seeder quyền trên môi trường
Blocked:

## Fix bản in theo ảnh user (2026-10-30)
- [x] Khoảng "Người lập" → tên: 56px → **15px** theo print-page §8b (#11918) — `InventoryImportService::narrowSignatureSpace()` thay dòng trống của mẫu bằng `.signature-space` inline `15px !important` lúc render (áp cả mẫu 295 + 296). Đo popup: 15px
- [x] Dòng thông tin đầu phiếu lệch hàng (ô Kho xuống 3 dòng kéo cả hàng căn giữa dọc) — `alignInfoCellsTop()` chèn `vertical-align: top !important` vào `<td>` bao PHIEU_NHAP_KHO / PHIEU_KIEM_KE / KHO / THU_KHO / GHI_CHU. Đo popup: 4 nhãn cùng top 304px
- [ ] Hỏi user: thêm quy tắc "ô thông tin đầu phiếu căn đỉnh" vào skill print-page (skill chưa có); màn Phiếu nhập kho ĐCKK cùng mẫu lỗi (div 70px) có sửa theo không
- [x] Bỏ icon ⓘ "Chỉ liệt kê phiếu nhập kho điều chỉnh kiểm kê đang Chờ duyệt." ở ô Phiếu nhập kho (màn Thêm)
- [x] Check (không sửa): ô Nhân viên phải gõ ≥ 1 ký tự mới tìm (`minimum-input-length="1"`); ERP select2 nạp sẵn toàn bộ nhân viên. Lỡ sửa thành bấm là hiện rồi đã HOÀN TÁC theo user — chờ user quyết
- [x] Ô Nhân viên đổi về chuẩn project (user yêu cầu 30/10): `V2BaseSelect` + store `employeeOptions` (khuôn `AccountingPrepickCancelForm.vue:29`) thay `V2BaseSelectRemote` bắt gõ ≥ 1 ký tự; phiếu gắn NV đã nghỉ vẫn giữ tên (computed `employeeOptions` chèn NV đang gắn). Gỡ BE route `search-employees` + `InventoryImportController::searchEmployees` + `InventoryImportService::searchEmployees`. Playwright: bấm vào hiện 555 NV, gõ "Thuỳ Trang" lọc đúng, Chi tiết id 1 hiện đúng tên
- [x] Card lệch chuẩn (user báo 30/10) — đo so màn chuẩn `ProductExportRequestForm` (YCXH 35765): khoảng cách card 36px → 24px (bỏ `class="mb-4"` đè margin sẵn của `V2BaseFormCard`); AttachmentSection thêm `class="v2-attach-card mb-3"` (header nền #f9fafb, bo 8px, tiêu đề 12px in hoa như khuôn trong `V2BaseFormCard.vue`); Lịch sử `mt-3`. Đo lại Playwright: 3 khoảng cách đều 24px, header 4 khối cùng nền #f9fafb
- [ ] Hỏi user: màn Phiếu nhập kho ĐCKK (`pages/warehouse/inventory-imports`, khuôn tôi đã chép) cũng dính y 3 lỗi card này
- [x] Header card vẫn lệch (user báo 30/10, mẫu `finance/bill-incomes/create`, `customer-care/warranty-repair-requests/create`): đổi `V2BaseFormCard` (khuôn K1 nhóm kho, nền #f9fafb) → `V2BaseFormSection` (khuôn chung nhóm khác: `.card` + `.section-header`, nền rgba(100,116,139,.07), padding 2px 10px, cao 36px, tiêu đề 14px/700, bo 4px); AttachmentSection bỏ `v2-attach-card` (về `.card` gốc). Đo Playwright: 3 card khớp số đo 2 màn mẫu, cách nhau 24px như bill-incomes

### Checkpoint — 2026-10-30 (wrap up)
Vừa hoàn thành: port màn Phiếu nhập hàng điều chỉnh kiểm kê BE + FE; Playwright toàn luồng + chỉnh UI theo user (bỏ ⓘ, Ghi chú
cùng hàng Nhân viên, ô Nhân viên theo chuẩn store, card `V2BaseFormSection`, bản in ký 15px + căn đỉnh). User test OK.
Đang làm dở: —
Bước tiếp theo: chạy seeder quyền trên môi trường (`permission:sync --dry-run` trước); commit khi user yêu cầu. Việc treo chờ
user quyết: (1) gộp `ProductTransferAccountingService::addImportWarehouse` sang `AccountingStockWriter`; (2) link "Phiếu xử lý" ở
Biên bản xử lý thừa thiếu sang màn HRM; (3) màn Phiếu nhập kho ĐCKK cùng lỗi (khoảng ký 70px, card); (4) thêm quy tắc "ô thông tin
đầu phiếu căn đỉnh" vào skill print-page.
Blocked:

## Push (2026-10-30, user yêu cầu)
- [x] Commit CHỈ phần màn nhập hàng ĐCKK (file dùng chung api.php / seeder / CatalogHistoryService / AccountingStockWriter /
      finance.js đang lẫn việc dở của màn Phiếu xuất hàng ĐCKK — session khác — tách bằng hash-object + update-index, file trên
      đĩa giữ nguyên): hrm-api `470a03b1f`, hrm-client `49c54185c`
- [x] Merge với origin/develop trong worktree tạm (repo chính có file chưa commit trùng file origin đổi ⇒ không pull tại chỗ được);
      conflict `CatalogHistoryService` (khối Chuyến xe khác vs Phiếu nhập hàng ĐCKK) giữ cả 2. Push: hrm-api `ef113e688`,
      hrm-client `f242fa9d6` lên `develop`
- [ ] Repo chính 2 bên đang SAU origin/develop (local chỉ có commit của mình + việc dở màn xuất): pull khi màn xuất commit xong
