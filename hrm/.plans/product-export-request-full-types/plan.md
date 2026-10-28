# Plan — Port 6 loại xuất mới + căn dropdown (HRM)

Thứ tự thi công: **P0 dropdown/label → P1 (19) → P2 (4) → P3 (16/17) → P4 (14/15)**.
Mỗi phase test bằng trình duyệt (tạo phiếu thật) trước khi sang phase sau.

## P0 — Nhãn + hằng số + delivery (nền cho mọi phase) — ✅ DONE
- [x] `Assign/Entities/Warehouse/ProductExportRequest.php`:
  - [x] Sửa `TYPE_NAMES`: 14→"Xuất bán hàng", 15→"Xuất khuyến mại", 4→"Xuất trả nhà cung cấp", 17→"Xuất bán SC - BD" (khớp constant.js).
  - [x] Thêm const `XUAT_TRA_NCC=4, XUAT_BAN_HD_HANG=14, XUAT_KM_HD_HANG=15, XUAT_BAO_HANH=16, XUAT_BD_SC=17, XUAT_THUC_HIEN_HD=19`.
  - [x] `HAS_DELIVERY_TYPE_IDS` = khớp ERP getHasDeliveryTypes (mọi creatable trừ 16).
  - [x] Thêm relation `productImportRequest()` (type 4).
- **CHIẾN LƯỢC LỘ DẦN (an toàn, HRM không có git):** `CREATABLE_TYPE_IDS` chỉ khai loại ĐÃ
  dựng xong luồng Tạo (BE+FE). Mở khoá TỪNG loại khi hoàn tất phase của nó → dropdown chỉ giống
  hệt ERP khi cả 6 loại port xong. Hiện giữ nguyên 8 loại đang chạy (3,6,7,12,18,99,20,21).

## P1 — Type 19 (Xuất thực hiện hợp đồng)
- [ ] Verify ERP type 19: loại HĐ attach + có auto-load dòng không (form.blade has_parent / create.blade getParentInfo).
- [ ] BE `rulesForType(19)`: nhập tay (warehouse + products min:1) + `emplement_contract_id nullable|exists`.
- [ ] BE service: nhánh manual + set `emplement_contract_id/type`.
- [ ] FE `ProductExportRequestForm.vue`: thêm 19 vào MANUAL_TYPES-like + đính ContractSearchModal (KH read-only, không load dòng).
- [ ] Test: tạo phiếu 19, kiểm dữ liệu tab_products/details.

## P2 — Type 4 (Xuất trả nhà cung cấp)
- [ ] BE: `ProductImportRequest::canSupplierReturn($id)` + `getDataForSupplierReturn($id)` (port ERP getDataForReturn).
- [ ] BE endpoint Assign: `GET .../product-export-requests/import-request-lines/{id}` (nạp dòng trả NCC) + tái dùng list `finance/product-import-requests` cho modal.
- [ ] BE `rulesForType(4)`: `product_import_request_id required|exists` + re-check canSupplierReturn; service ghi `product_import_request_id` (cha) + dòng (allocated_price/inland_cost/vat).
- [ ] FE: modal chọn phiếu ĐNNK + bảng SL trả / allocated_price / inland_cost / vat.
- [ ] Test: tạo phiếu 4 từ ĐNNK đủ điều kiện; kiểm chặn khi không đủ điều kiện.

## P3 — Types 16/17 (nguồn HĐ SC-BH)
- [ ] BE: port `canProductExport()` cho WrServiceContract (CustomerCare).
- [ ] BE: mở rộng `BorrowSellRequestSourceService::loadWrService()` (hoặc service Assign mới) — nhánh `items.type=0` (loại 16, không rebate/vat) + giữ `type=1` (loại 17).
- [ ] BE endpoint Assign: search HĐ SC-BH + load dòng theo `type` (16→0 / 17→1).
- [ ] BE `rulesForType`: 17 require `wr_service_contract_id` + delivery; 16 không require, không delivery. Store ghi `wr_service_contract_id` cả 2 + snapshot KH + guard canProductExport.
- [ ] FE: modal chọn HĐ SC-BH + bảng (17 có rebate/vat/delivery, 16 không).
- [ ] Test: tạo phiếu 16 và 17 riêng.

## P4 — Types 14/15 (nguồn HĐ hãng)
- [ ] BE endpoint Assign: search HĐ hãng (bê `PrepickExportContractService::searchContracts`).
- [ ] BE endpoint load `getDataForWarehouseExport`: bước 1 vat_options+tabs; bước 2 dòng — 14 dùng `loadFirm`, 15 viết nhánh combo KM (`firm_contract_combo_group_option_products`, giá 0).
- [ ] BE endpoint `getPromoWarehouse` (kho KM, `promo_warehouse_ids`) cho loại 15.
- [ ] BE `rulesForType(14)`: firm_contract_id/firm_tab_vat_percent/tabs.*/need_repair; `rulesForType(15)`: firm_contract_id/promo_warehouse_id.
- [ ] BE store: ghi cha (firm_contract_id/firm_tab_vat_percent/need_repair/promo_warehouse_id) + snapshot KH + guard canProductExport(14)/canProductExportPromotion(15); dòng vào tab_products(firm_contract_tab_id)+details(giá, 15=0).
- [ ] FE: modal HĐ hãng → chọn tab/VAT → bảng giá (14 có/15=0) + "Cần lắp đặt"(14) + kho KM(15).
- [ ] Test: tạo phiếu 14 (theo tab+VAT, need_repair) và 15 (combo KM, kho KM).

## Ghi chú chung
- Không migration (DB đã đủ cột — verify ở design §3).
- Ghi dòng kép tab_products + details theo khuôn `writeContractLines` hiện có.
- Guard nghiệp vụ (canProductExport/canSupplierReturn/canProductExportPromotion) BẮT BUỘC port, không bỏ.
- Tuân skill `erp-to-hrm-screen`: UI theo chuẩn HRM; hàm nghiệp vụ dùng chung grep trước khi viết, ưu tiên tái dùng service Finance đã port.

## P4-UI — Bảng chi tiết loại 14 bám layout ERP (2026-10-13)
Yêu cầu user (ảnh chú thích): bảng hàng hóa loại 14 phải trông giống ERP.
- [x] Gom cột số lượng dưới header cha **"Số lượng"** (thead 2 tầng, colspan) — Cách 1A: `Tồn · Đang giữ · Hợp đồng · Đã xuất · Đang xuất · Đề nghị`. Tồn/Đang giữ HRM chưa có dữ liệu cho HĐ hãng → hiện `-` (đúng như ERP). **Bỏ** cột "Còn được xuất" (ERP không có; validate "vượt SL còn được xuất" vẫn giữ qua message lỗi).
- [x] Cột tiền bám ERP: `Giá niêm yết · Giá bán · Thành tiền bán · Đơn giá sau giảm(MỚI=allocated) · Thành tiền sau giảm(MỚI=allocAmount) · VAT · Thành tiền sau VAT(đổi tên từ "Sau VAT"=afterVat)`. **Bỏ** cột "Giảm"(discountAmount). Tất cả có sẵn trong `priceOf()`.
- [x] Thêm cột **Hình ảnh** cuối bảng (user đồng ý) — sửa BE `firmContractProductLines()` trả field `avatar` (URL ảnh sản phẩm, helper `buildProductAvatarUrl` tự ghép ERP_URL cho path tương đối, giữ URL tuyệt đối S3); FE bind `line.avatar`.
- [x] Cập nhật colspan dòng empty-state (17→20) + Playwright verify: nav tabs + 2 tầng header + 20 cột/dòng + ảnh render thật (4 `<img>` src S3) + cột tiền en-US. (`alt=""` nên ảnh ẩn khỏi a11y-tree, kiểm bằng DOM query.)

## P4-UI-2 — Modal "Chọn hợp đồng hãng" dựng lại theo khuôn loại 19 (2026-10-13)
Yêu cầu user: *"popup chọn hợp đồng hãng sửa lại cho giống bên erp hoặc giống modal chọn hợp đồng của loại xuất thực hiện hợp đồng"* → chốt **"theo khuyến nghị"**: dựng lại `FirmContractSearchModal` bám đúng `EmplementContractSearchModal` (loại 19), FE + BE; KHÔNG tách component dùng chung (để sau).
- [x] BE `firmContracts()` (`ProductExportRequestController.php` ~586): thêm phân trang + sort server-side (`page/per_page/sort_by/sort_desc`, lọc `code`/`customer`), trả khuôn `responseJson('success', 200, ['data'=>items, 'meta'=>{current_page,last_page,total,per_page}])` giống `emplementContracts`. `php -l` sạch.
- [x] FE `FirmContractSearchModal.vue`: viết lại trên `V2BaseModal` size xl + 2 ô lọc (Số HĐ / Khách hàng) + nút Tìm kiếm/Làm mới + `V2BaseDataTable` (cột STT/Mã HĐ link ERP/Khách hàng/Địa chỉ, sort + phân trang + đổi số dòng), click cả dòng = chọn (`onTableClick`). Giữ nguyên interface `:show`/`@close`/`@select` → cha không phải sửa.
- [x] Đọc response `res.data.data` / `res.data.meta` (apiGetMethod trả thẳng body, responseJson bọc dưới khoá `data`).
- [x] Playwright verify (1920×1080): mở loại 14 → "Chọn hợp đồng hãng" → modal hiện đủ lọc/bảng/phân trang/sort/link Mã HĐ (→ `:8001/admin/sale/firm-contracts/10627`); HĐ 10627 load; click dòng → chọn HĐ, auto điền VAT 8% + nhóm hàng + thông tin KH; số liệu en-US.

### Checkpoint — 2026-10-13
Vừa hoàn thành: P4-UI-2 — modal Chọn hợp đồng hãng dựng lại theo khuôn loại 19 (FE `FirmContractSearchModal.vue` + BE `firmContracts()`), đã Playwright-verify trên HĐ 10627 (lọc/bảng/sort/phân trang/link/chọn dòng OK).
Đang làm dở: không.
Bước tiếp theo: CHỜ user ủy quyền commit + chọn nhánh (develop vs gop_db). Revert data test `UPDATE firm_contracts SET created_by=158 WHERE id=10627` khi xong.
Blocked: cổng commit vẫn khóa — không commit/push khi chưa có yêu cầu.

## P4-UI-3 — Làm phẳng layout modal "Chọn hợp đồng hãng" (bỏ khung card lồng) (2026-10-13)
Yêu cầu user (ảnh): modal *"trông không được đẹp lắm, nhiều tầng layout chồng nhau quá"* — khung card "Danh sách" của `V2BaseDataTable` lồng thêm 1 lớp viền/bóng/bo bên trong body modal (modal đã có tiêu đề riêng).
- [x] FE `FirmContractSearchModal.vue`: thêm prop `hide-header` cho `V2BaseDataTable` (bỏ khung tiêu đề "Danh sách" lồng — đúng công dụng prop) + scoped CSS `::v-deep .firm-table.tp-card { border/box-shadow/border-radius: none; padding: 0 !important; background: transparent }` làm phẳng card chrome để bảng nằm thẳng trong body modal.
- [x] Playwright verify (loại 14 → "Chọn hợp đồng hãng"): khung card lồng đã biến mất, bảng phẳng ngay dưới hàng lọc; filter/bảng/sort/phân trang/link Mã HĐ vẫn hoạt động.
- [x] Commit loại 14: `8cce5ab29` → `origin/develop` (hrm-client).
- [x] Đồng bộ màn loại 19 (`EmplementContractSearchModal.vue`): áp cùng `hide-header` + flatten `.emplement-table.tp-card` (user chốt "2 ok" 2026-10-13). Playwright verify loại 19 → "Chọn hợp đồng / đơn hàng": khung card lồng mất, bảng phẳng, filter/sort/phân trang/link OK.
- Quyết định: data test `firm_contracts.created_by=158 (id 10627)` GIỮ NGUYÊN, user chốt "1 ko" (không revert) 2026-10-13.

## P4-UI-4 — Thống nhất ô chọn nguồn HĐ (Tạo = Sửa) theo quy ước `.picker-input` finance (2026-10-13)
Yêu cầu user (ảnh màn Sửa): *"ở màn sửa hiển thị hợp đồng và chọn lại hợp đồng hãng khác với ở màn tạo"* — form YCXH đang dùng **2 kiểu trigger khác nhau** cho cùng 1 việc chọn/đổi nguồn HĐ: màn Tạo dùng thẻ `.contract-card` / nút `.contract-choose`, màn Sửa dùng `SourcePicker` (span mã + nút Đổi). Hỏi "có quy ước input-chọn-từ-popup chưa" → rà project (Explore): KHÔNG có chuẩn hợp nhất; quy ước de-facto nhiều màn nhất là `.picker-input` (khối Finance, khuôn `BillIncomeForm.vue`, ~17 form). Chốt **Hướng C** (user "C. ok"): dựng `SourcePicker` thành ô `.picker-input` (V2BaseInput readonly, bấm mở popup, hiện "mã - tên KH" 1 dòng) dùng CHUNG cho **cả Tạo lẫn Sửa**, áp cho **cả 3 loại nguồn HĐ** (14 HĐ hãng / 19 HĐ-đơn hàng / 20-21 HĐ HRM) để không tái lập lệch. Loại 7 (điều chuyển) + loại 99 (HĐ chi phí) KHÔNG đụng (không dùng SourcePicker).
- [x] FE `SourcePicker.vue`: render `V2BaseInput` readonly `.picker-input` (copy khuôn `BillIncomeForm`), thêm prop `placeholder` + `invalid`, guard `onClick` không mở khi `disabled`, giữ nguyên `confirmChange`/props + CSS scoped `.picker-input`/`--readonly`.
- [x] FE `ProductExportRequestForm.vue`: 3 block (20/21, 14, 19) bỏ `v-if="isEdit"` + xoá nhánh `<template v-else>` thẻ card/choose; mỗi block 1 `<SourcePicker>` dùng chung + `:placeholder` + `:invalid` theo errorField. `pickSource` luôn qua `confirmChange` (ref luôn tồn tại) — bỏ tham số `direct`.
- [x] e2e: `source-change.spec.ts` đọc giá trị qua `.inputValue()`/`toHaveValue` thay cho `.innerText()`/`toHaveText` trên `[data-test="ycxh-source-code"]` (giờ là input); `ProductExportRequestPage.openSourcePicker` dùng 1 locator `[data-test="ycxh-source-picker"]` cho cả 2 mode.
- [x] Playwright verify Tạo + Sửa cho 3 loại; chạy lại `source-change.spec.ts` → **5 passed** (4 test + setup). Nới mọi assertion chờ dòng hàng lên 30s để hết flaky khi chạy song song (create-data gọi API thật).

### Checkpoint — 2026-10-13
Vừa hoàn thành: Hướng C — ô `.picker-input` dùng chung Tạo/Sửa cho cả 3 loại nguồn HĐ (14/19/20-21); e2e `source-change.spec.ts` 4 test xanh ổn định.
Đang làm dở: (không)
Bước tiếp theo: chờ user yêu cầu commit 3 file (SourcePicker.vue, ProductExportRequestForm.vue, e2e source-change.spec.ts) — hiện CHƯA commit.
Blocked:

## P4-ACCOUNTING — Bút toán + ghi ngược loại 14 (Xuất bán HĐ hãng) (2026-10-21)
Yêu cầu user: *"port đầy đủ giống hệt erp"* + *"ghi ngược giống ERP"* + *"phải chắc chắn dữ liệu được lưu đúng như erp làm"* + *"cứ làm giống erp"*. Scope = ĐỦ 8 cụm bút toán loại 14 + ghi ngược exported_qty về HĐ hãng, bám ERP 1:1; kèm sửa bug ẩn contractMeta loại 15.
- Spec: `docs/superpowers/specs/2026-10-21-pxk-phase4-type14-posting-design.md`
- Plan chi tiết (TDD từng task): `docs/superpowers/plans/2026-10-21-pxk-phase4-type14-posting.md`
- SDD ledger: `hrm-api/.superpowers/sdd/2026-10-21-pxk-phase4-type14-posting/progress.md`
- BASE sạch Phase 4: `f9fb1d36e` (sau khi tách commit base_unit creation-flow).
- [x] T1 — hằng `AccountDetail::CONTRACTABLE_FIRM_CONTRACT` (additive)
- [x] T2 — nhánh bút toán loại 14 (8 cụm, giá vốn Có **1561**) + `prepareDataFirmContract`, Contract "cầu", `$sa` qua morph FirmContract
- [x] T3 — contractMeta loại 14 + 15 về HĐ hãng (sửa bug ẩn loại 15 rơi vào CONTRACTABLE_HRM_CONTRACT)
- [x] T4 — `finalizeFirmContractExport` ghi ngược exported_qty 3 tầng + bridge + YCXH → Đã hạch toán (5); wire CẢ HAI path (A qua PXK, B xuất thẳng); commit 58d899ef5; review SPEC ✅ + QUALITY approved (3 finding minor không chặn)
- [x] T5 — regression bút toán cũ (21/3/19/4/17) PASS + verify loại 15 contractMeta (test THẬT, 3125 PXH đủ điều kiện); commit 9cb17dc83; review SPEC ✅ + QUALITY approved. Ruling lệch YCXH loại 15 KHÔNG về status 5 (ProductExportService.php:419-438) — giữ nguyên, nêu user chốt riêng.
- [x] Final whole-branch review (opus) trên `f9fb1d36e..9cb17dc83`: phần lớn CLEAN khớp ERP 1:1; raise 1 load-bearing **L1** — ghi ngược resolve theo ID (gate legacy `!$fctpId`) thay vì theo ROW như ERP → id mồ côi sẽ update 0 dòng im lặng (lệch "dữ liệu phải lưu đúng ERP"). Kèm M1 (bridge nhiều dòng) + M2 (need_repair chưa chuẩn 0/1).
- [x] Final fix round (bám ERP `ProductExport.php:1739-1761`): resolve `firm_contract_tab_products` theo **ROW** + rơi legacy khi id treo + bridge cộng đúng 1 dòng + need_repair 0/1; commit `56dc7cbdd`; test mới chứng minh fallback (id treo cả tier-1+bridge → dòng legacy thật tăng đúng qty), happy-path cũ vẫn PASS (2 test/7 assertion, 0 skip).
- [x] Scoped re-review (sonnet) `9cb17dc83..56dc7cbdd`: **APPROVED, 0 load-bearing** — 7 mục (a)-(g) PASS, 2 nit backlog (đã adjudicate).

### Checkpoint — 2026-10-21 (Phase 4 ACCOUNTING loại 14)
Vừa hoàn thành: **P4-ACCOUNTING XONG** — port đủ 8 cụm bút toán loại 14 (giá vốn Có 1561) + ghi ngược exported_qty 3 tầng về HĐ hãng (resolve theo ROW + rơi legacy khi id treo, bridge 1 dòng, need_repair 0/1, 2 wire path A+B) + sửa bug ẩn contractMeta loại 15. SDD full cycle (T1-T5 + final review opus + fix L1 + scoped re-review APPROVED). HEAD `56dc7cbdd`, chain 7 commit trên `develop`.
Đang làm dở: (không)
Bước tiếp theo: **GIỮ LOCAL — chờ user ủy quyền push**. User chốt: (1) YCXH loại 15 có cần tự về status 5 không (hiện KHÔNG, lệch quan sát so loại khác) · (2) phase kế: nhập/xuất lại, điều chuyển 5/6/7, ghép 9/tách 10, đóng gói, in biên bản, type-15 Path B write-back.
Blocked: cổng commit/push vẫn khóa — không push khi chưa có yêu cầu.

## P4-FIX-15 — YCXH loại 15 (Xuất khuyến mại HĐ hãng) tự về Đã hạch toán giống ERP (2026-10-21)
User hỏi "a. có giống erp không" → đối chiếu ERP xác nhận **LỆCH**: ERP đuôi chung `ProductExport::updateWarehouse:1876-1882` áp cho MỌI loại (trừ điều chuyển nội bộ) → YCXH `status=5 + is_completed=true`; loại 15 ERP cũng về 5. HRM hiện chỉ ghi ngược combo + `$req->is_complete` (cờ in-flight trên ĐNXK), KHÔNG đẩy YCXH về 5. Thêm: Path B (xuất thẳng) THIẾU HẲN loại 15 (không combo, không status) trong khi ERP xử lý loại 15 ở cả `is_export_direct` (`:1776`). User chốt "ok" → fix giống ERP, phủ 2 path, theo SDD (fix+test+review), GIỮ LOCAL.
- Ruling: KHÔNG ghi `product_export_request_details`/bridge cho loại 15 — nhất quán ruling loại 14 (firm-contract track qua combo/bridge, FK PERD = NULL ở DB chung). Chỉ: ghi ngược combo + đuôi YCXH→5.
- [x] Tách method `finalizeFirmContractPromotionExport(ProductExport $pxh, int $ycxhId)`: combo write-back + đuôi YCXH→5/is_completed/logStatusChanged (bám finalizeGenericExport).
- [x] Path A (createFromWarehouseExport): thay block inline bằng dispatch method mới + GIỮ `$req->is_complete=true` (nhả in-flight ĐNXK). YCXH id = `$req->product_export_request_id`.
- [x] Path B (createFromProductExportRequest): thêm dispatch method mới (khối 9, `(int)$per->id`, xuất thẳng → không set is_complete). Khớp ERP :1776 (is_export_direct lấy `$this->tabs`).
- [x] Test `Phase4Type15WritebackTest` PASS (3 assert, fixture thật): combo exported_qty +qty, YCXH ép về DANG_HACH_TOAN rồi lên 5 + is_completed. Regression loại 14 (2/7) + posting (3/21) vẫn PASS.
- [x] Review độc lập (sonnet, scoped) `56dc7cbdd..9034e912d`: **APPROVED, 0 load-bearing** — (a)-(h) PASS, 2 nit backlog (reflection không phủ wiring; đã grep `XUAT_KM_HD_HANG` chỉ 2 điểm set, không trùng). Commit LOCAL `9034e912d`, trailer Opus 4.8. CHƯA push.

### Checkpoint — 2026-10-21 (P4-FIX-15 YCXH loại 15 auto status-5)
Vừa hoàn thành: **P4-FIX-15 XONG** — YCXH loại 15 tự về Đã hạch toán (5) + is_completed giống ERP đuôi chung; tách `finalizeFirmContractPromotionExport` (combo write-back + YCXH tail) wire cả Path A+B; vá luôn gap Path B (trước đó thiếu hẳn loại 15). SDD full cycle (fix+test+review APPROVED). HEAD `9034e912d`.
Đang làm dở: (không)
Bước tiếp theo: **GIỮ LOCAL — chờ user ủy quyền push**. Quyết định (a) loại 15 YCXH status-5 đã CHỐT+XONG. Còn chờ (b) phase kế: nhập/xuất lại, điều chuyển 5/6/7, ghép 9/tách 10, đóng gói, in biên bản, legacy 1/2/11/13.
Blocked: cổng commit/push vẫn khóa — không push khi chưa có yêu cầu.
