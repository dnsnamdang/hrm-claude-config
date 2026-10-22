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
