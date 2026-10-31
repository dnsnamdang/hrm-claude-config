# Phiếu xuất hàng điều chỉnh kiểm kê — Plan

Người phụ trách: @khoipv
Màn: `hrm-client/pages/finance/inventory-exports/` · BE: `Modules/Finance` (`InventoryExportController`,
`Services/InventoryExport/InventoryExportService` + `InventoryExportWriteService`, `Entities/InventoryExport/InventoryExport`)

## Phase 1 — Port màn (2026-10-30) — chép khuôn màn Phiếu nhập hàng ĐCKK

### BE
- [x] Quyền: 2 quyền xem tên y ERP vào `PermissionsTableSeeder` (type 8, group "Phiếu xuất hàng điều chỉnh kiểm kê")
- [x] Entity `InventoryExport` (STATUSES, scopedQuery, canView, canEdit, generateCode `PXHĐCKK-`)
- [x] `AccountingStockWriter::export()` — trừ tồn kế toán + log FIFO (type 1, FQN `InventoryExportDetailAccWarehouse`) +
      `stocks.accounting_qty`; trả value_before/after để tính đơn giá vốn. Thiếu tồn kế toán ⇒ 422 (ERP 500)
- [x] `InventoryExportService`: danh sách / lọc (ERP có lọc mã/tên hàng thật) / sort, chi tiết, nguồn (phiếu xuất kho Chờ duyệt +
      Kế toán kho; công ty dòng = công ty lô nhập), kho kế toán, `availableStocks()` = "SL được xuất" (gọi `AccountingStockService::detail`,
      công ty + nhân viên = người đăng nhập như ERP), xuất Excel, in phiếu (mẫu 300, cột Đơn giá vốn / Thành tiền vốn) / danh sách (mẫu 299)
- [x] `InventoryExportWriteService`: store / update y ERP — validate tổng SL = SL xuất + gom (hàng, kho kế toán, ĐVT) so "SL được
      xuất"; syncDetails (+ handled_qty, `price` FE gửi, `company_id` dòng, `export_qty` dòng = 0 như ERP); Lưu và duyệt: trừ tồn +
      đơn giá vốn dòng phân bổ + dòng hàng; **KHÔNG bút toán**; trạng thái phiếu xuất kho + phiếu kiểm kê có log; file; lịch sử
      (đăng ký `CatalogHistoryService::TABLES`). Sửa phiếu không còn Đang tạo ⇒ 409 TRƯỚC validate
- [x] Controller `InventoryExportController` + route `finance/inventory-exports`
- [x] Phiếu xuất kho ĐCKK: `product_export_erp_path` → `product_export_path` (`/finance/inventory-exports/create?warehouse_inventory_export_id=`),
      sửa assert trong `WarehouseInventoryExportApiTest`

### FE
- [x] `pages/finance/inventory-exports/` index / create / _id/index / _id/edit + `InventoryExportForm.vue` + constants + row-actions
      (chép khuôn `pages/finance/inventory-imports`). Bảng: SL xuất · Đơn giá (sửa được) · Thành tiền · [Chi tiết] Đơn giá vốn /
      Thành tiền vốn · Kho kế toán · Số lượng · [Form] SL được xuất; chọn kho ô đầu dòng đầu ⇒ điền kho + SL mọi dòng (ERP autoFill)
- [x] Menu `components/subsystem-menu/finance.js` gắn link (giữ nhãn)
- [x] Màn Phiếu xuất kho ĐCKK: nút "Tạo phiếu xuất hàng" (row-actions + form) mở màn HRM, bỏ `openErp`

### Verify
- [x] `php -l` 7 file BE · `permission:sync --dry-run` nhận 2 quyền mới
- [x] Smoke API (Super admin 13): danh sách / filter-options / chi tiết + in phiếu ERP id 1 / in danh sách / export-rows (thứ tự theo
      tick) / lọc mã hàng / histories / source-options → 200; source phiếu đã hạch toán → 404
- [x] Luồng ghi trong transaction ROLLBACK (tạm đặt PXKĐCKK-00016 Chờ duyệt): lệch tổng → 422 "Số lượng xuất kho kế toán không
      khớp!"; vượt tồn → 422 "Kho …: Số lượng xuất không được vượt quá số lượng được xuất!" (hàng 10975 tồn 0 bị chặn); Lưu → phiếu
      xuất kho 2; Sửa + Lưu và duyệt → 4, tồn kế toán 11→8 / 1→0, log FIFO, **đơn giá vốn 25,001 / 150,000 = đúng số phiếu ERP thật
      PXHĐCKK-00001**, 0 dòng `account_details`; lịch sử ghi đủ mốc; sửa lại → 409. Rollback xong DB nguyên trạng
- [x] `WarehouseInventoryExportApiTest`: 11/12 pass. 1 fail CÓ TỪ TRƯỚC (`test_store_validates_note_attachment_and_warehouse` dòng
      275 đòi Ghi chú bắt buộc khi lưu nháp — commit `ddd23d04c` 28/10 đã nới, test chưa sửa theo), không do thay đổi lần này
- [x] FE compile (vue-template-compiler + @babel/parser) 10 file + grep checklist skill sạch; khoá cấu hình cột/bộ lọc không trùng
- [ ] Mở trình duyệt bấm thật (user tự test): Thêm từ nút ở phiếu xuất kho, SL được xuất, phân bổ nhiều kho, Lưu và tiếp tục, Sửa,
      Lưu và duyệt, Chi tiết (Đơn giá vốn), In, Xuất Excel, Lịch sử
- [ ] Chạy seeder quyền trên môi trường

## Test Playwright local (2026-10-30, Super admin id 13)
- [x] Danh sách: 9 cột, badge xanh, toolbar Tạo mới → In danh sách → Xuất Excel → Cấu hình cột; lọc Mã hàng (mã lạ → "Không có
      dữ liệu phù hợp.", mã thật → 1 dòng), Làm mới về đủ
- [x] Chi tiết PXHĐCKK-00001: đủ ô, bảng có Đơn giá vốn / Thành tiền vốn (25,001 / 39,296 / 150,000 khớp ERP), nút In / Quay lại;
      In mẫu 300 đúng cột; Lịch sử trống (phiếu ERP)
- [x] Phiếu xuất kho 16 (tạm Chờ duyệt) → nút "Tạo phiếu xuất hàng" mở `/finance/inventory-exports/create?warehouse_inventory_export_id=16`,
      nạp 3 dòng + đơn giá bán
- [x] Lưu trống → toast "Bạn chưa nhập đầy đủ thông tin." + báo đỏ mọi ô cùng lúc, không gọi API; chọn kho ô đầu ⇒ tự điền kho + SL
      3 dòng, SL được xuất 11 / 0 / 1; dòng tồn 0 → "Số lượng xuất không được vượt quá số lượng được xuất!", không gọi API
- [x] (tạm nâng tồn kế toán hàng 10975 lên 1) Lưu → PXHĐCKK-00003 Đang tạo, phiếu xuất kho → Đang hạch toán; Sửa nạp lại NV + kho;
      đổi đơn giá 50,000 → 60,000 → Lưu và duyệt (popup xác nhận) → Đã hạch toán: tồn kế toán 11→8 / 1→0 / 1→0, log FIFO, đơn giá
      vốn 25,001 / 39,295.67 / 150,000, 0 bút toán; vào lại /edit bị đá về Chi tiết; Lịch sử 3 mốc; popup "chưa lưu" khi rời form
- [x] Xuất Excel: popup 7/7 trường → file đúng tiêu đề / cột / khối ký
- [x] Sửa lỗi phát hiện: tên file + tiêu đề + sheet Excel còn "nhập hàng" (sót khi chép khuôn — sed không bắt chữ IN HOA) → đổi
      `danh_sach_phieu_xuat_hang_...` / "DANH SÁCH PHIẾU XUẤT HÀNG…"; rà lại cả BE không còn chữ "nhập hàng" sót
- [x] Dọn dữ liệu test theo id (phiếu 3, 3 dòng chi tiết, 3 dòng phân bổ, 3 log tồn, 5 log lịch sử) + khôi phục snapshot → khớp 100%
- [ ] Chưa bấm: Lưu và tiếp tục, File đính kèm (upload), Cấu hình cột, In danh sách

### Ghi chú lệch ERP có chủ ý
- Đang tạo màu xám (ERP đỏ); nhãn Người tạo/Ngày tạo; câu lỗi tiếng Việt từng ô; thiếu tồn kế toán ⇒ 422 thay 500; FE báo đỏ khi
  SL vượt "SL được xuất" (ERP tự kéo về trần); "SL được xuất" tính sẵn khi nạp form (ERP gọi API mỗi lần chọn kho).
- Giữ y ERP (user chốt 30/10): không bút toán; cộng `handled_qty` mỗi lần lưu (kể cả sửa); không chặn lập trùng; nhận dòng FE gửi.

### Checkpoint — 2026-10-30
Vừa hoàn thành: Phase 1 BE + FE + verify API/compile
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt test; quyết 2 việc treo chung với màn nhập: đổi link "Phiếu xử lý" ở Biên bản xử lý thừa thiếu
(`InventoryAuditReportDetail::erpHandlePath`) sang màn HRM; sửa test cũ `WarehouseInventoryExportApiTest` dòng 275
Blocked:

## Push (2026-10-30)
- [x] Commit + push `develop` (rebase lên origin, không conflict): hrm-api `caf2abf87` · hrm-client `7a2880d5f`. Chỉ đưa file của
      màn này; 8 file hrm-client đang dở việc khác (V2BaseDataTable, V2BaseLabel, toast.js…) để nguyên, chưa commit

## Fix lệch giao diện trên cổng dev (2026-10-31, user báo ảnh dev vs local)
- [x] Check: mở thẳng `/finance/inventory-exports/create` trên dev thì ô Phiếu kiểm kê mất khung, ô Kho / Thủ kho nền trắng. Nguyên
      nhân: `assets/scss/v2-styles.scss` (khai `.v2-linked-field`, nền ô khoá) KHÔNG global, chỉ `index.vue` import ⇒ đi từ danh
      sách sang thì có CSS, mở thẳng link thì không. Checklist skill có dòng `grep -L "v2-styles.scss" <Form>.vue` — lần đầu chỉ grep index
- [x] Sửa (user chốt "sửa cả"): thêm `@import '@/assets/scss/v2-styles.scss';` vào `<style scoped>` của 4 form dùng chung khuôn:
      `finance/inventory-exports`, `finance/inventory-imports`, `warehouse/inventory-exports`, `warehouse/inventory-imports`
- [x] Verify: mở thẳng link màn Thêm ở tab mới (không qua danh sách, trình duyệt sạch) — ô Phiếu kiểm kê có khung xám, ô Kho / Thủ
      kho nền xám như local (chụp 3/4 màn; màn còn lại chạy cùng script)
- [x] Push hrm-client `43e528f29` (chỉ 4 form)

## Nền ô khoá toàn cục (2026-10-31, user: "input nào disable thì để background disable, cập nhật vào skill")
- [x] Đưa rule nền ô khoá (#f1f5f9 / chữ #475569 / viền #e2e8f0, không opacity) ra `hrm-client/assets/scss/default.scss` (toàn cục,
      tiền tố `body`, `!important`) — trước chỉ ở `v2-styles.scss` lồng `.v2-styles` ⇒ màn không import ra nền trắng. Bản trong
      v2-styles giữ nguyên. node-sass biên dịch sạch
- [x] Skill `select-and-input-state` §3 + mục tự kiểm; skill `erp-to-hrm-screen` checklist D + dòng grep `v2-styles.scss` (grep cả form)
- [x] Verify trình duyệt (local, mở thẳng link tab mới): `/finance/inventory-exports/1` + `/warehouse/inventory-exports/16` có rule
      toàn cục `body .v2-input:disabled`, 4/4 ô khoá mỗi màn nền `rgb(241,245,249)`
- [x] Commit + push hrm-client `7dfbf6445` (chỉ `default.scss`)
