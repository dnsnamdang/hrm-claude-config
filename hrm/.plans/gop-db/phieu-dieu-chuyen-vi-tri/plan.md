# Phiếu điều chuyển vị trí — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-19-phieu-dieu-chuyen-vi-tri-design.md`

## Phase 0 — Khảo sát
- [x] Đọc controller/model/blade/JS class ERP `position_transfers` + API phụ (vị trí, lô, hàng) + mẫu in 54
- [x] Chốt với user 19/10: làm như ERP; 4 quyền tên y ERP type 21; thêm `PhysicalStockWriter::transferLot()`; giữ lỗi canEdit của ERP

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 4 quyền trong `PermissionsTableSeeder` + `permission:sync --dry-run`
- [x] B2. `PhysicalStockWriter::transferLot()` + `WarehouseInventoryLockService` (hàng/vị trí đang kiểm kho)
- [x] B3. Entity `PositionTransfer` (phạm vi, cờ, mã PĐCVT)
- [x] B4. `PositionTransferService` (danh sách, lọc, sort, export-rows, filter-options, form-options, chi tiết, popup hàng/vị trí/lô, nguồn phiếu kiểm kê)
- [x] B5. `PositionTransferWriteService` (lưu nháp, điều chuyển, sửa, xóa, file, lịch sử, cập nhật phiếu kiểm kê nguồn)
- [x] B6. `PositionTransferPrintService` (mẫu 54: in phiếu + in dự kiến) + AttachmentService
- [x] B7. FormRequest + Controller + routes + đăng ký `catalog_histories`
- [x] B8. Phiếu kiểm kê theo vị trí: `erp_transfer_url` → link HRM
- [x] B9. Smoke test HTTP kernel (rollback)

## Phase 2 — FE
- [x] F1. Menu Kho › Điều chuyển › Phiếu điều chuyển vị trí
- [x] F2. Danh sách `pages/warehouse/position-transfers/index.vue` + row-actions + export-excel
- [x] F3. Form dùng chung (Thêm/Sửa/Chi tiết) + popup hàng/vị trí/lô + In dự kiến + file
- [x] F4. create / _id/edit / _id/index + lịch sử + 404
- [x] F5. Phiếu kiểm kê theo vị trí: nút Tạo phiếu điều chuyển → màn HRM
- [x] F6. Checklist skill erp-to-hrm-screen (grep) + compile

### Checkpoint — 2026-10-19
Vừa hoàn thành: B1–B9 + F1–F6.
- BE: 4 quyền (dry-run: thêm 4), `PhysicalStockWriter::transferLot()` (mới, không đụng hàm cũ), `WarehouseInventoryLockService` (mới),
  entity `PositionTransfer`, `PositionTransferService` / `WriteService` / `PrintService` (mẫu 54) / `AttachmentService`, FormRequest,
  controller + 19 route `finance/position-transfers`, lịch sử bảng GATED `position_transfers`. Màn Kiểm kê: `erp_transfer_url` → `transfer_create_path` (HRM).
- Smoke test HTTP kernel (rollback, DB sạch): 30/30 luồng chính + 7/7 lập từ phiếu KK (TPV-KKVT-00106 → Hoàn thành) + 4/4 tài khoản 0 quyền.
- FE: `pages/warehouse/position-transfers` (index/create/_id/_id/edit + Form + row-actions + export-excel), menu Kho › Điều chuyển.
  Bám màn `warehouse/position-inventory-results` (card section-header, CreatorInfoLine, AttachmentSection, SystemInfoSection, CatalogHistoryModal,
  Xuất Excel ExcelJS); popup chọn hàng/vị trí/lô dùng lại `warehouse-imports/components/RecordPickerModal.vue`.
- Verify FE: vue-template-compiler + babel parse 9 file OK, grep checklist sạch. CHƯA mở trình duyệt.
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt test: tạo tay (chọn kho → thêm hàng → ĐVT → vị trí xuất → lô → vị trí nhập → SL → file) Lưu / Điều chuyển, In dự kiến, In phiếu, sửa/xóa nháp, lập từ Phiếu kiểm kê (Chờ xử lý). Gán 4 quyền mới (`permission:sync`) cho tài khoản test.
Blocked:

## Phase 3 — Test Playwright + sửa theo user (19/10)
- [x] T1. Test Playwright toàn màn (Super admin id 13, token): danh sách (sort 5 cột, tìm nhanh, 5 ô lọc khớp DB, phân trang 1 request, giữ lọc khi quay lại, Cấu hình cột, Xuất Excel, In, Lịch sử), Tạo (validate nháp/điều chuyển, đổi kho hỏi, popup hàng/vị trí/lô, chặn SL vượt tồn, In dự kiến, Lưu, Lưu và tiếp tục), Chi tiết, Sửa (cảnh báo chưa lưu), Điều chuyển (ghi tồn đúng), Xóa, lập từ phiếu KK 106 (→ Hoàn thành). Dọn sạch theo baseline + xoá 2 file S3
- [x] Fix: bảng Chi tiết tràn ngang (cột SL bị cắt) → min-width chỉ áp màn Thêm/Sửa
- [x] Fix: số lô hiển thị thống nhất có tiền tố mã công ty (`PositionTransferService::lotLabel`, cả popup / chi tiết / in)
- [x] User: popup Thêm hàng → popup DÙNG CHUNG `V2ProductPickerModal`; thêm param tuỳ chọn `stock_warehouse_id` vào `ProductPickerService` + `ProductPickerRequest` (user OK sửa hàm chung; PHPUnit ProductPicker 37/37); bỏ endpoint `/products` tự dựng, thêm `/product-units`
- [x] User: 3 ô Vị trí xuất / Lô xuất / Vị trí nhập → `V2BasePickerField` (viền đỏ lỗi gắn class `is-invalid` từ ngoài)
- [x] User: Kho + Ghi chú cùng 1 dòng (Ghi chú ô 1 dòng như ERP)

### Checkpoint — 2026-10-19 (sau test Playwright)
Vừa hoàn thành: Phase 3. Ảnh test ở scratchpad phiên (không đưa vào repo).
Đang làm dở: không
Bước tiếp theo: user duyệt giao diện; chạy `permission:sync` khi deploy.
Blocked:

## Phase 4 — SL tồn khi lập từ phiếu kiểm kê như ERP (21/10)
- [x] S1. Lập từ phiếu KK theo vị trí / theo hàng hóa: `stock_qty` = tồn CẢ LÔ (`warehouse_import_lots.qty`) như ERP `getDataForPositionTransfer` (`import_lot = WarehouseImportLot::find`) — VD lô TONDAUKHO-9114 ở phiếu TPE-KKVT-00138: 374 (ERP) thay vì 357 (tồn tại PTT-N1-KV1). Màn Sửa/Chi tiết + popup chọn lô giữ tồn theo vị trí (ERP `updateStock` / `getLotsInPosition`)
  - `PositionTransferService::decorateRows($rows, $lotTotal)` + `lotTotals()`; `sourceData` / `selfSourceData` truyền `true`. Verify tinker: lô 9114 → 357 (vị trí) / 374 (cả lô). Chưa mở trình duyệt.

## Phase 5 — Redmine #11789 Danh sách (21/10)
- [x] R1. Công ty → khối chuẩn `V2BaseCompanyDepartmentFilter` (xem được cả công ty đã khoá) + lọc `department_id` ở BE (khuôn #11770 Kế hoạch kiểm kê)
- [x] R2. Người tạo = toàn bộ nhân viên (`$store.state.employeeOptions`); `filter-options` bỏ `creators` / `companies`
- [x] R3. Bỏ sort cột Ngày tạo / Trạng thái / Người tạo; sort mặc định trống (BE tự `created_at desc`)
  - BE `PositionTransferService`: SORT_MAP chỉ còn code/warehouse, lọc `department_id`, filterOptions bỏ creators/companies, xoá `employeeOptions()` (không còn chỗ gọi). FE `position-transfers/index.vue`: slot `#field-org` + `creatorOptions` + bỏ sortable 3 cột.
  - Verify: vue-template-compiler + babel OK; HTTP kernel 4/4 (filter-options, sort status bị bỏ qua → mặc định, department_id lọc, sort code). Chưa mở trình duyệt.

## Phase 6 — Redmine #11815 In dự kiến (21/10)
- [x] P1. In dự kiến hiện Số phiếu + Ngày kiểm kê: FE gửi `id` (màn Sửa); BE tra phiếu trong `scopedQuery` → SO_PHIEU = mã, NGAY_KIEM_KE = ngày tạo (phiếu mới: chưa có số, ngày = hôm nay). In phiếu cũng điền NGAY_KIEM_KE
- [x] P2. Tăng khoảng cách khối ký tên (chèn khoảng trống trước tên người lập — KHÔNG sửa mẫu 54 dùng chung ERP)
- [x] P3. Bảng dự kiến: thu cột SL, nới cột Ghi chú
  - BE `PositionTransferPrintService` (expectHtml nhận `?PositionTransfer`, điền NGAY_KIEM_KE, đệm 70px trước NGUOI_LAP, cột dự kiến 5/29/7/12/12/12/6/17) + `PositionTransferController::printExpect` (nhận `id`, tra `scopedQuery`). FE `PositionTransferForm.vue` gửi `id: recordId`.
  - Verify: compile FE OK; HTTP kernel print-expect 3/3 (có id → PĐCVT-00436 + 13/11/2025; không id / id ngoài phạm vi → trống số + hôm nay). Chưa mở trình duyệt.

## Phase 7 — Redmine #11791 Form (22/10)
- [x] F1. Ghi chú đổi sang textarea (`V2BaseTextarea`, 2 dòng, vẫn tối đa 255) — thay quyết định 19/10 "ô 1 dòng như ERP"
- [x] F2. Câu lỗi inline bỏ tiền tố tên ô ("Kho – Vui lòng chọn kho." → "Vui lòng chọn kho."), áp cho mọi lỗi FE của form (22 câu)
- [x] F3. Câu lỗi theo `hrm-client/locales/vi.json` (skill `form-validate` §3 sửa cùng ngày): bỏ trống = `Bắt buộc phải nhập` (cả bảng Chi tiết trống, File đính kèm), quá dài = `Vui lòng nhập tối đa 255 ký tự.`, SL vượt trần = `Giá trị nhập vào không được vượt quá 999,999,999.`, sai chung = `Không hợp lệ`; lỗi nghiệp vụ giữ câu riêng, bỏ tiền tố
  - FE `PositionTransferForm.vue`; BE `PositionTransferStoreRequest::messages()`, `PositionTransferController::printExpect`, `PositionTransferWriteService` (5 câu ValidationException)
  - 422 khi Lưu: lỗi đều có ô hiện → toast nhắc chung "Vui lòng kiểm tra lại thông tin đã nhập."; có khoá không có ô (`products.N.position_inventory_result_id`, `products.N.product_id`…) → toast câu đó (hằng `INLINE_ERROR_KEY`). In dự kiến 422 → popup nhắc chung.
  - Verify: vue-template-compiler + babel OK; php -l OK; HTTP kernel 3/3 (store nháp, store điều chuyển, print-expect → câu mới). Chưa mở trình duyệt.

## Phase 8 — Redmine #11808 Tạo mới (23/10)
- [x] T1. Ẩn tooltip ⓘ cạnh nhãn Kho (bỏ `:hint` + computed `warehouseHint`) — `PositionTransferForm.vue`
- [x] T2. Ghi chú dạng textarea — đã làm ở Phase 7 F1 (#11791), ảnh tester chụp 20/10 trước khi sửa
- [x] T3. Bỏ tiền tố "Kho –" / "Chi tiết –" trong câu lỗi — đã làm ở Phase 7 F2/F3 theo skill `form-validate` §3 (`Bắt buộc phải nhập`)
- [x] T4. Danh sách Phiếu kiểm kê theo vị trí: phiếu còn dòng cần điều chuyển → nút sang THẲNG màn Tạo phiếu điều chuyển vị trí, icon `ri-arrow-left-right-line` + tên "Tạo phiếu điều chuyển vị trí" như footer chi tiết; phiếu Chờ xử lý không cần điều chuyển vẫn "Xử lý" → Chi tiết
  - BE `PositionInventoryResultService::listFlags()` thêm `is_can_transfer` + `transfer_create_path` (needTransfer chỉ chạy khi canHandle); `actionFlags()` dùng lại; export danh sách lọc bỏ `transfer_create_path`
  - FE `position-inventory-results/components/row-actions.js`: action `transfer`
  - Verify: php -l OK; tinker listFlags phiếu 106 → transfer=1 + path đúng, complete=0; vue-template-compiler + babel OK. Chưa mở trình duyệt.
- [x] T5. Bỏ cột "Bấm để chọn" ở popup dùng chung `RecordPickerModal` (user chốt: bỏ ở CẢ 6 màn dùng popup). Dòng không chọn được (`disabledFn`) → chữ xám, con trỏ cấm, rê chuột hiện lý do (gắn `title` cho `<tr>` lúc mouseover vì V2BaseDataTable không có prop title dòng)
  - Verify: vue-template-compiler + babel OK. Chưa mở trình duyệt.

### Checkpoint — 2026-10-23
Vừa hoàn thành: Phase 8 (#11808).
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm: form Tạo (không còn ⓘ ở Kho), danh sách Phiếu kiểm kê theo vị trí (nút ⇄ sang thẳng màn tạo điều chuyển). Kiểm popup Chọn vị trí xuất / nhập / lô: không còn cột "Bấm để chọn", vị trí đang kiểm kho xám + tooltip.
Blocked:

## Phase 9 — Redmine #11811 Popup chọn vị trí (23/10)
- [x] V1. Sort cột Tồn (server, `sort_by=unit_qty` → `sp.qty`)
- [x] V2. Lọc Nhà / Dãy / Khoang: 3 dropdown theo kho đang chọn, phân cấp Nhà → Dãy → Khoang (user chốt dropdown). BE: API `position-transfers/position-filter-options` + lọc `house_id`/`row_id`/`space_id` ở `positionsQuery`
- [x] V3. RecordPickerModal (dùng chung, user cho phép 23/10): thêm slot `#filters` + phát sự kiện `reset` — màn khác không truyền slot thì không đổi
- [x] V4. Ô Vị trí không mở link → chữ thường (bỏ `link: true` ở positionColumns)
- Ghi chú: ô đỏ "Bấm để chọn" trong ảnh đã bỏ ở Phase 8 T5 (#11808)
  - BE `PositionTransferService::positionsQuery` lọc `house_id`/`row_id`/`space_id` + `positionFilterOptions()`; `PositionTransferController::positionFilterOptions`; route `GET position-transfers/position-filter-options`
  - FE `RecordPickerModal.vue` (slot `#filters`, ô tìm co về col-md-3 khi có slot, emit `reset`); `PositionTransferForm.vue` (3 `V2BaseSelectInModal`, mở popup thì xoá lọc, danh mục nhớ theo kho, cột Tồn `unit_qty` sortable + format `qty_text`, bỏ `link` ô Vị trí)
  - Verify: php -l OK; vue-template-compiler + babel OK; HTTP kernel kho 1 / hàng 7462: options 200 (1 nhà / 23 dãy / 133 khoang), sort Tồn asc/desc đúng, lọc nhà 15→13, dãy →8, khoang →1. Chưa mở trình duyệt.

### Checkpoint — 2026-10-23
Vừa hoàn thành: Phase 9 (#11811).
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm popup Chọn vị trí xuất / nhập: 3 ô lọc Nhà/Dãy/Khoang (phân cấp), sort cột Tồn, ô Vị trí chữ thường; kiểm 5 màn khác dùng RecordPickerModal không đổi giao diện (ô tìm + nút như cũ).
Blocked:

## Phase 10 — Redmine #11812 Popup chọn vị trí nhập + popup lô (23/10)
- [x] N1. Lọc Nhà/Dãy/Khoang + sort Tồn ở popup vị trí nhập — đã có từ Phase 9 (#11811, cùng 1 popup cho xuất/nhập)
- [x] N2. Bỏ "Bấm để chọn", bấm bất kỳ đâu trong dòng để chọn — đã có từ Phase 8 T5 (#11808)
- [x] N3. Ô tìm vị trí chỉ tìm theo MÃ (user chốt 23/10; tên vị trí trong DB là tầng "Tầng 1", bảng không hiện) → placeholder "Mã vị trí", BE bỏ `positions.name`. Màu ô Vị trí giữ chữ thường như #11811 (user chốt, "để lại màu" coi là gõ nhầm)
- [x] N4. Popup chọn lô: ô tìm không chạy (BE `lots()` bỏ qua `keyword`) → lọc theo số lô đang hiển thị (gồm tiền tố công ty), không phân biệt hoa thường
  - BE `PositionTransferService::positionsQuery` (keyword chỉ `positions.code`), `lots()` (lọc `keyword` bằng `mb_stripos` trên nhãn lô); FE `PositionTransferForm.vue` placeholder "Mã vị trí"
  - Verify: php -l OK; compile FE OK; HTTP kernel: lô không từ khoá 36 → "6-49" 8 → "dhsjkjs" 0; vị trí "Tầng 1" 0, "SG-N1-D2" 20. Chưa mở trình duyệt.

### Checkpoint — 2026-10-23
Vừa hoàn thành: Phase 10 (#11812).
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm popup vị trí nhập (lọc / sort / placeholder "Mã vị trí") và ô tìm ở popup Chọn lô xuất.
Blocked:

## Phase 11 — Redmine #11813 Sửa phiếu (23/10)
- [x] S1. Nút "Lưu" → "Lưu nháp" (+ "Lưu nháp và tiếp tục"); nháp CHỈ bắt Kho (user chốt 23/10 — lệch ERP: ERP bắt cả Ghi chú + ≥1 hàng). Ghi chú / ≥1 hàng / đủ cột dòng chỉ bắt khi Điều chuyển. `note` NOT NULL → nháp trống ghi ''
- [x] S2. Vượt tồn: ĐỐI CHIẾU ERP, KHÔNG đổi — ERP Lưu cho qua (chỉ tô đỏ SL tồn), Điều chuyển khoá nút (`form.is_invalid`); HRM Lưu nháp cho qua, Điều chuyển chặn → giống ERP
- [x] S3. Bỏ tiền tố tên cột trong câu lỗi — đã làm Phase 7 F2/F3 (#11791), ảnh tester chụp 21/10 trước khi sửa
- [x] S4. Lịch sử dòng hàng sửa: "Tên hàng: trường cũ → mới" — bỏ phụ chú (Vị trí xuất; Lô; Vị trí nhập) (`__brief = true`)
- [x] S5. Ẩn ⓘ cạnh Kho — đã làm Phase 8 T1 (#11808)
- [x] S6. Lịch sử: xoá 1 dòng giữa bảng → chỉ 1 dòng "đã xóa" (`__key` = product_id#lần xuất hiện, thay chỉ số dòng)
- [x] S7. Báo lỗi theo skill `form-validate`: FE chỉ chặn định dạng (ghi chú ≤255, SL ≤ trần), required + nghiệp vụ để BE 422; toast nhắc chung "Vui lòng kiểm tra lại thông tin đã nhập."; lỗi đang kiểm kho / vị trí khác kho / vượt tồn của BE gắn về ĐÚNG DÒNG (khoá `products.N.*`) thay vì khoá chung `products` ở cuối bảng; lỗi dòng hàng (`product_id`, dòng kiểm kê đã xử lý) hiện dưới ô Tên hàng hóa
  - BE `PositionTransferStoreRequest` (nháp: `note`/`products` nullable; Điều chuyển: required + kiểm file trong `withValidator` để báo cùng lượt), `PositionTransferWriteService` (note `''` khi trống; `guardInventory` / `validateStock` gắn lỗi `products.N.product_id|from_position_id|to_position_id|qty`; `__key` = `product_id#n`, `__brief = true`)
  - FE `PositionTransferForm.vue`: nút "Lưu nháp" / "Lưu nháp và tiếp tục"; `validateAll` → `validateFormat` (chỉ định dạng); `rowError()` dưới ô Tên hàng hóa; toast "Vui lòng kiểm tra lại thông tin đã nhập."
  - Verify: php -l OK; compile FE OK; HTTP kernel (rollback): nháp chỉ kho 200 · thiếu kho 422 warehouse_id · Điều chuyển trống 422 đủ 4 khoá (note/products/warehouse_id/attachments) · ghi chú 256 ký tự 422; lịch sử: xoá dòng 2/4 → 1 dòng "đã xóa", sửa SL → "Tên: SL 1 → 2", lưu lại không đổi → 0 log; reflection: vượt tồn dòng 3 → `products.2.qty`, vị trí kiểm kho / khác kho → đúng ô từng dòng. Chưa mở trình duyệt.
  - Lưu ý: log cũ (khoá theo chỉ số dòng) → lần sửa đầu tiên sau deploy của phiếu nháp cũ có thể nhiễu 1 lần (skill entity-history §6).

### Checkpoint — 2026-10-23
Vừa hoàn thành: Phase 11 (#11813).
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm form Sửa: nút Lưu nháp (chỉ bắt Kho), Điều chuyển thiếu dữ liệu → đỏ đủ ô 1 lượt + toast chung, lỗi đang kiểm kho / vượt tồn hiện ở đúng dòng; lịch sử xoá 1 dòng giữa bảng.
Blocked:

## Phase 12 — Redmine #11855 File đính kèm thêm dấu (*) (26/10)
- [x] R1. Khối File đính kèm hiện dấu (*) bắt buộc ở form Tạo/Sửa (cùng khuôn Ghi chú / Chi tiết: `!isShow`). BE đã chặn sẵn khi Điều chuyển mà chưa có file (Phase 11) → không đổi BE
  - FE `PositionTransferForm.vue`: `AttachmentSection` thêm `:required-file="!isShow"` (prop có sẵn → `<Required>` ở tiêu đề + cột "Upload / File")
  - Verify: compile FE. Chưa mở trình duyệt.

### Checkpoint — 2026-10-26
Vừa hoàn thành: Phase 12 (#11855).
Đang làm dở: không
Bước tiếp theo: user mở /warehouse/position-transfers/create kiểm dấu (*) cạnh "File đính kèm".
Blocked:

## Phase 13 — Redmine #11812 phản hồi: nút Tìm kiếm / Làm mới xuống dòng ở màn nhỏ (26/10)
- [x] S1. Popup Chọn vị trí nhập/xuất: chữ "Tìm kiếm", "Làm mới" bị bẻ 2 dòng khi màn hẹp → để cả 2 nút trên 1 dòng
  - FE `RecordPickerModal.vue`: cột nút `col-md` → `col-md-auto` (lấy đúng bề rộng nút), nút `white-space: nowrap; flex-shrink: 0`
  - FE `PositionTransferForm.vue`: 3 ô lọc Nhà/Dãy/Khoang `col-md-2` → `col-md` (tự co nhường chỗ cho nút)
  - Verify: compile FE. Chưa mở trình duyệt.

### Checkpoint — 2026-10-26
Vừa hoàn thành: Phase 13 (#11812 phản hồi).
Đang làm dở: không
Bước tiếp theo: user thu nhỏ cửa sổ, mở popup Chọn vị trí nhập kiểm 2 nút không xuống dòng.
Blocked:

## Phase 14 — Redmine #11813 phản hồi 23/10 (26/10)
- [x] P1. Nút "Lưu nháp và tiếp tục" → "Lưu và tiếp tục" (hành vi giữ nguyên: lưu nháp rồi ở lại tạo tiếp)
- [x] P2. "Bỏ chỗ trống" (user chốt: khoảng hở giữa icon ⓘ và chữ "Bắt buộc phải nhập") — ô SL canh phải nên câu lỗi dạt phải, bẻ dòng thì hở → `.pt-table ::v-deep .v2-error { text-align: left }`
  - FE `PositionTransferForm.vue`. Verify: compile FE. Chưa mở trình duyệt.

### Checkpoint — 2026-10-26
Vừa hoàn thành: Phase 14 (#11813 phản hồi).
Đang làm dở: không
Bước tiếp theo: user kiểm nút "Lưu và tiếp tục" + câu lỗi ô SL sát icon.
Blocked:

## Fix #11875 — Lưu nháp chỉ validate 1 trường bắt buộc + thông báo validate theo skill (2026-10-26)

- [x] Rà lại: luồng Lưu nháp đã có từ #11813 (BE `PositionTransferStoreRequest` nháp chỉ bắt Kho, commit api dd3ebabe0 / client 5d7ab14ba đã lên `origin/gop_db` 23/10) — ảnh tester là bản cũ trên hrm-crm (câu "Ghi chú – Vui lòng nhập ghi chú." trước #11791) → cần deploy
- [x] FE: toast lỗi validate đổi về câu chuẩn skill `form-validate` §1/§3d "Bạn chưa nhập đầy đủ thông tin." (lưu: lỗi định dạng + 422; In dự kiến 422)
- [x] Kiểm FormRequest: nháp trống → chỉ đỏ Kho; nháp chỉ Kho → qua; nháp ghi chú 300 ký tự → chặn định dạng; Điều chuyển chỉ Kho → đỏ Ghi chú + Chi tiết + File cùng lượt

### Checkpoint — 2026-10-26
Vừa hoàn thành: fix #11875
Đang làm dở: —
Bước tiếp theo: deploy hrm-crm (api + client) rồi QA test lại
Blocked:
