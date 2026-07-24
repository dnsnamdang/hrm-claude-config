# Plan — Sao chép / Export / Import Báo giá

> Design tóm tắt: `.plans/baogia-copy-export-import/design.md`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-16-baogia-copy-export-import-design.md`

- **Phụ trách**: @manhcuong
- **Worktree**: `/Users/manhcuong/Desktop/dns/HRM-worktree-baogia/{hrm-api,hrm-client}` — nhánh `baogia_copy_export_import` (từ `origin/tpe`)
- **Màn**: QLDA TKT → Quản lý báo giá · Chi tiết dự án → Tab Báo giá · Xem chi tiết BG · Cập nhật BG

## Ràng buộc chung (áp cho mọi task)

- PHP 7.4 — lint bằng `/opt/homebrew/opt/php@7.4/bin/php -l`, KHÔNG dùng `php -l` (máy mặc định 8.1)
- Vue 2 / Nuxt 2.14 — **không có `@vue/composition-api`**, chỉ mixin/component
- DB **không strict mode** → chuỗi dài hơn cột bị cắt âm thầm ⇒ validate độ dài ở tầng ứng dụng là lớp bảo vệ duy nhất
- Không bọc DDL (addColumn) trong `DB::transaction`
- Element form FE dùng `V2Base*`; select trong modal dùng `V2BaseSelectInModal`
- Không commit/push git khi chưa có yêu cầu
- Bẫy: `product_type` HRM = **số** (1=Hàng hoá/2=Dịch vụ); `product_type` ERP = **chuỗi** enum — khác nhau hoàn toàn

---

## Phase 1: Sao chép báo giá

### BE

- [x] Task 1: Migration `quotations` + `copied_from_quotation_id` (unsignedBigInteger nullable, after `type`); không bọc DDL trong transaction
- [x] Task 2: `QuotationService::getCopyPreview(Quotation)` — quét dòng `erp_product_id != null`, so `estimated_price`/`quoted_price` (qua `TpProductUnitPrice::getUnitPrice()`, chia `exchange_rate`) + `vat_percent` với ERP; trả mảng `changes[{type,code,name,old,new,action}]` với `type ∈ {price, vat, structure}`; `structure` (Rule 4) = BOM trên ERP có thêm vật tư con so với cây V1 → action "(Bỏ qua) — Giữ nguyên cấu trúc V1"; chừa sẵn nhánh `type=discontinued` cho Rule 1 (hoãn)
- [x] Task 3: `QuotationService::copy()` phần header — gate quyền lặp logic `store()` (`QuotationController:138-161`: YCBG → `Xây dựng giá bán theo công ty/phòng` theo `implementation_type`; tự lập → `main_sale_employee_id`); copy whitelist header; reset `code`/`status=1`/`created_by`/`copied_from_quotation_id` + null 9 field erp_*/tmp_* + 6 field duyệt; `exchange_rate` lấy tỷ giá ERP hiện tại; `validity_date` tính lại
- [x] Task 4: `copy()` phần `quotation_product_prices` — Rule 4 copy cây V1 y nguyên + remap `parent_id` qua map `[old=>new]`, giữ `sort_order`/`show_children`; Rule 2&3 dòng ERP lấy lại giá+VAT đè V1; Rule 5 hàng tạm bê nguyên; Rule 6 dòng: `amount` giữ tiền tính lại %, `percent` giữ % tính lại tiền
- [x] Task 5: `copy()` phần phụ — copy `quotation_groups` + remap `quotation_group_id`; copy `quotation_service_items` (sinh lại `code` theo `getNextCode($newCode)`, giữ `cost_id`); copy `quotation_discounts` Rule 6 (`amount` giữ `amount_value`; `percent` giữ `percent_value` **tính lại `amount_value` SAU khi products clone xong + recomputeTotals lần 1**)
- [x] Task 6: `copy()` kết thúc — `enforceErpProductVat()` → `enforceServiceCostsFromRate()` → `recomputeTotals()` → `logHistory(ACTION_CREATE, null, 1, meta:{copied_from, copied_from_code})`; trả `{id, code}`
- [x] Task 7: `QuotationController::copyPreview()` + `copy()` + 2 route `GET /{id}/copy-preview`, `POST /{id}/copy`; không gắn middleware checkPermission (gate trong controller)
- [x] Task 8: `QuotationService::update()` cho đổi dự án — gate `copied_from_quotation_id != null` + status 1 + `project_id` đổi thật; xoá `customer_*` cũ nạp lại từ dự án mới; ngắt BOM (`bom_list_id=null`, `type=2`) + **set `bom_list_product_id=null` toàn bộ dòng** (tránh mồ côi ở `upsertDirectProducts`); thêm `project_id` vào whitelist `:582` + `QuotationUpdateRequest`

### FE

- [x] Task 9: `QuotationCopyPreviewModal.vue` (mới) — popup "Phát hiện thay đổi dữ liệu từ ERP", bảng 5 cột (Loại thay đổi/Mã-Tên vật tư/Thông tin cũ/Thông tin mới/Hành động hệ thống), nút `[Hủy bỏ]` `[Xác nhận Sao chép báo giá]`
- [x] Task 10: `_id/index.vue` nút Sao chép (footer) — gọi `copy-preview`; `changes` rỗng → gọi thẳng `copy`; có → mở modal; xong `$router.push('/assign/quotations/{newId}/edit')`; computed `canCopy` lặp gate `store()`
- [x] Task 11: `index.vue` (danh sách) nút Sao chép vào slot `#actions` của `V2BaseTitleSubInfo` (cột `code_name`), dùng chung modal + logic Task 10
- [x] Task 12: `ProspectiveProjectQuotationsTab.vue` nút Sao chép cùng vị trí `#actions`, dùng chung modal + logic
- [x] Task 13: `edit.vue` cho đổi dự án khi `item.copied_from_quotation_id` — hiện select Dự án (đang readonly), chọn lại → xoá thông tin KH cũ + nạp từ dự án mới + xoá BOM tổng hợp; gửi `project_id` trong payload PUT

---

## Phase 2: Export báo giá

### BE

- [x] Task 14: Blade `resources/views/exports/assign/quotation_excel.blade.php` — khu vực 1 CẤU HÌNH GIẢM GIÁ TỔNG (5 cột, chỉ khi `discount_method=2`) + khu vực 2 KHAI BÁO HÀNG HOÁ 24 cột đúng file mẫu; 7 cột công thức (14/18/20/21/23/24 + Thành tiền GG) ghi **công thức Excel**; cột 18 theo `discount_method` (1: `IF(GG(đ)>0, ...)`; 2: `Đơn Giá bán - IFERROR(Phân bổ GG/SL,0)`; null: `= Đơn Giá bán`)
- [x] Task 15: `Modules/Assign/Export/QuotationExcelExport.php` — `FromView` + `ShouldAutoSize` + `Exportable` + `forData()`; sinh STT từ cây (cha 1,2,3; con X.1); dòng "Chi phí vận chuyển" từ 5 field header nếu `shipping_cost > 0`; gate cột 13/14/21 theo `Xem giá vốn hàng hoá || $isCreator` (đúng `exportExcel:790-792`)
- [x] Task 16: `QuotationController::exportQuotationData()` (tên file `{code}_{d-m-Y}.xlsx`) + `exportBlankTemplate()` (data rỗng, tên `Mau_import_bao_gia.xlsx`) + 2 route — ⚠️ `GET /export-blank-template` **PHẢI đặt TRƯỚC `GET /{id}`** (`api.php:459`), cùng 1 segment sẽ bị wildcard nuốt

### FE

- [x] Task 17: `_id/index.vue` gộp 3 nút export vào 1 dropdown `V2BaseButton` + `b-dropdown`: "Xuất Excel" (giữ `handleExportExcel` cũ), "Export báo giá trống", "Export báo giá hiện tại"

---

## Phase 3: Import báo giá

### BE

- [x] Task 18: `Modules/Assign/Services/QuotationImportService.php` (class mới, KHÔNG nhét vào `QuotationService` 2742 dòng) — `parseSttTree()`: STT duy nhất toàn file, parse cây 2 cấp, **tối đa 2 cấp** báo lỗi rõ (không làm phẳng ngầm), suy `parent_temp_id`
- [x] Task 19: `validateDiscountSection()` — chỉ quét khi `discount_method=2`; Loại GG đối chiếu `discount_types` theo `code` → fallback `name` (loại `status=2`); Kiểu chỉ `%`/`đ`; Giá trị > 0; Thành tiền GG > 0; map `amount_value`="Thành tiền GG" (nguồn sự thật), `percent_value`="Giá trị" khi Kiểu=`%` else null
- [x] Task 20: `validateProductRows()` nhánh **BG độc lập** — Loại ∈ 3 giá trị; Tên/Mã/ĐVT/SL/Đơn Giá bán/VAT theo luật §7.4; resolve ERP theo Mã hàng (thấy → đè name/model/brand/origin/unit/TSKT/giá/VAT từ master; không thấy → hàng tạm); Master Data lạ → **chặn + báo lỗi** (KHÔNG auto-insert, ngược URD theo quyết định #3 BOM); max `note`=500, `Nhóm hàng`=255; SL > 0 tối đa 3 số lẻ
- [x] Task 21: `validateProductRows()` — bộ công thức GG theo `discount_method`: `=1` quét GG(đ) trước >0 thì phớt lờ GG(%); `=2` Blind Ignore xoá sạch GG(%)/GG(đ) chỉ dùng Phân bổ GG; `=null` phớt lờ cả 3; + Rule chặn lỗ cha-con (chỉ hàng tự xây): giá cha ≥ Σ giá con
- [x] Task 22: `validateProductRows()` nhánh **BG từ BOM** — chỉ map giá/VAT/GG vào dòng BOM sẵn có (đối chiếu Mã hàng ↔ `bom_list_products.code`); **báo lỗi rõ thay vì nuốt im lặng**: thiếu mã BOM / mã lạ / sửa SL / sửa Tên-Nhóm-TSKT của hàng BOM
- [x] Task 23: Dòng "Chi phí vận chuyển" → 5 field header (`shipping_cost`←Đơn Giá bán, `shipping_import_price`←Đơn Giá nhập, `shipping_vat_percent`←VAT, `shipping_discount`←GG(đ), `shipping_allocated_discount`←Phân bổ GG); **>1 dòng → báo lỗi**
- [x] Task 24: `QuotationController::validateImportExcel()` + route `POST /{id}/import-excel/validate`; chặn status ≠ 1 (422); response OK trả `{hasErrors:false, products, groups, serviceItems, discounts, shipping}` (rows chuẩn hoá sẵn cho lưới, **không sinh mã HH- ở đây** — `saveDirectProduct:1102-1113` tự sinh khi lưu); response lỗi **all-or-nothing 422** `{hasErrors:true, errorCount, errors[{no,excelRow,column,message}]}`

### FE

- [x] Task 25: `QuotationImportModal.vue` (mới) — tự chứa logic, **KHÔNG dùng `V2BaseImportModal`** (13 màn khác dùng chung); chọn file (.xlsx/.xls) → popup confirm ghi đè ("Dữ liệu từ file Excel sẽ xóa và thay thế toàn bộ danh sách hàng hóa...") → parse XLSX bằng `utils/import-helper.js` → loading → gọi API validate
- [x] Task 26: `QuotationImportModal.vue` popup lỗi — tiêu đề `❌ Import thất bại: Phát hiện [X] lỗi dữ liệu`; lưới cuộn 4 cột (STT / Dòng Excel / Tên cột sai / Mô tả chi tiết); nút `Sao chép lỗi` (clipboard) · `Tải File lỗi` (.xlsx) · `Đóng`; giữ popup mở để user sửa file rồi Import lại
- [x] Task 27: `QuotationImportModal.vue` thành công → emit `import-applied({products, groups, serviceItems, discounts, shipping})`; `edit.vue` nhúng modal + `onImportApplied` gán **thay nguyên cục** (không merge) + toast "Đã nạp dữ liệu từ file Excel. Kiểm tra lại rồi bấm Lưu báo giá để chốt."
- [x] Task 28: Dọn code cũ FE `edit.vue` — gỡ nút Import Excel (`:246`), `V2BaseImportModal` (`:1026-1058`), `importColumns`/`importRequiredFields` (`:1723-1770`), `openImportModal` (`:3811`), `handleValidateImport` (`:3837`), `handleImportData`, `handleDownloadImportTemplate`, `importHeaderRow`, `isImportGroupRow`
- [x] Task 29: Dọn code cũ BE — gỡ `validateImportPrices` (`:1147`), `importPrices` (`:1422`), `exportImportTemplate` (`:1045`) + 3 route (`api.php:477,478,480`); **kiểm tra trước khi gỡ**: `BomListExport::withTemplateMode()`/`withServiceItems()` còn nơi nào gọi không → nếu chỉ dùng ở đây thì thành code chết, ghi lại vào checkpoint (không xoá sang file BOM khi chưa chắc)

---

## Verify (sau khi code)

- [x] Lint sạch toàn bộ file BE sửa — `/opt/homebrew/opt/php@7.4/bin/php -l`
- [x] **AC1** — Sao chép ở cả 3 màn (danh sách / tab dự án / chi tiết) → V2 tạo thành công, điều hướng đúng; `code` mới, `status=1`, `copied_from_quotation_id` đúng, các field duyệt/erp/tmp đều null
- [x] AC1b — BG có hàng ERP đổi giá/VAT → popup diff hiện đúng dòng; BG không đổi gì → **bỏ popup**, vào thẳng màn sửa
- [x] AC1c — Rule 4: cây cha-con V2 giống hệt V1 (kể cả khi BOM trên ERP đã đổi cấu trúc); Rule 5: hàng tạm giữ nguyên tên/giá/SL; Rule 6: GG `amount` giữ số tiền, GG `percent` giữ % và **tiền nhảy theo tổng mới**
- [x] **AC2** — "Export báo giá trống" → file chỉ có 2 khối header, không dòng dữ liệu
- [x] **AC3** — "Export báo giá hiện tại" → mở bằng PhpSpreadsheet đọc lại: đủ 24 cột đúng thứ tự + khu vực GG tổng + dòng vận chuyển (nếu có)
- [x] **AC4** — status ≠ Đang tạo → không có nút Import (đã đạt sẵn `edit.vue:246`, chỉ cần regression)
- [x] **AC5** — status Đang tạo + file hợp lệ → confirm ghi đè → dữ liệu lên lưới; bấm Lưu → DB đúng
- [x] **AC6** — file lỗi → popup lỗi dạng lưới, **không đổ dữ liệu lên lưới** (all-or-nothing); nút Sao chép lỗi + Tải file lỗi chạy
- [x] **AC7** — Round-trip: Export hiện tại → Import lại chính file đó → **không lỗi** (KHÔNG đòi byte-identical: STT chuẩn hoá `1,3`→`1,2`, 7 cột công thức tính lại)
- [x] Edge: STT `2.1.3` → báo lỗi 2 cấp; STT trùng → lỗi; Model lạ → "không khớp Master Data"; >1 dòng vận chuyển → lỗi; file rỗng hàng hoá → lỗi
- [x] Edge: BG từ BOM import file thiếu mã BOM → lỗi chốt chặn; mã lạ → lỗi (KHÔNG nuốt im lặng như code cũ)
- [x] Edge: đổi dự án trên bản sao chép → KH nạp lại từ dự án mới, `bom_list_id=null`, `type=2`, **`bom_list_product_id=null` toàn bộ dòng**; lưu lại không mất dòng
- [x] Regression: BG thường (không phải bản sao chép) **không** đổi được dự án
- [x] Regression: 13 màn dùng `V2BaseImportModal` không bị ảnh hưởng (không sửa file đó)
- [x] Regression: nút "Xuất Excel" cũ trong dropdown vẫn ra đúng file như trước
- [x] Lưu ý test quyền: `isCurrentEmployeeHasPermission` check qua **ROLE** (`role_has_permissions` theo `role_id` + `current_company_role`), KHÔNG qua quyền gán trực tiếp cho nhân viên

---

## Checkpoint

### Checkpoint — 2026-07-16 (khởi tạo)
Vừa hoàn thành: Tạo worktree (`HRM-worktree-baogia`, nhánh `baogia_copy_export_import` từ `origin/tpe`, cả 2 repo). Đọc URD + file mẫu Excel Google. Khảo sát BE báo giá / BE import-export / FE báo giá / 3 ẩn số kỹ thuật (4 agent). Brainstorming 6 câu chốt → 9 quyết định. Viết spec đầy đủ + design tóm tắt + plan 29 task. User đã duyệt design.
Đang làm dở: Chưa code dòng nào.
Bước tiếp theo: Task 1 — migration `quotations.copied_from_quotation_id`.
Blocked (2 việc user cần làm song song, KHÔNG chặn Phase 1-3 vì đã cắt khỏi scope):
- **Rule 1** — cần ERP trả lời: (a) enum `product_types` có mục "ngừng kinh doanh" không, (b) mapping `products.status` 0/1/2/5, (c) bổ sung `status` vào response `/api/v1/hrm/products/search`. Thiết kế đã chừa chỗ ở `getCopyPreview()` (Task 2).
- **Chèn dòng vào BG kế thừa BOM** — cần BA làm rõ; hiện giữ khoá (quyết định #6).

### Checkpoint — 2026-07-16 (wrap up phiên 1)

**Vừa hoàn thành: 10/29 task — TẤT CẢ đã qua review độc lập và Approved.**

| Phase | Task | Trạng thái |
|---|---|---|
| 1 — Sao chép (BE) | 1,2,3,4,5,6,7,8 | ✅ **HOÀN TẤT**, review Approved |
| 2 — Export (BE) | 14,15 | ✅ **Approved** (sau fix 1 Critical) |
| 2 — Export | 16,17 | 🔄 đang chạy dở (Controller + FE dropdown) |
| 1 — Sao chép (FE) | 9,10,11,12,13 | ⬜ chưa làm |
| 3 — Import | 18–29 | ⬜ chưa làm |

**Sao chép báo giá đã chạy được đầu-cuối ở backend**: `GET /{id}/copy-preview` + `POST /{id}/copy` + đổi dự án. Chỉ thiếu FE.

**KHÔNG commit** (theo CLAUDE.md). Toàn bộ thay đổi đang ở working tree của worktree.

**Đang làm dở**: Task 16+17 (agent chạy nền, có thể đã xong — kiểm `scratchpad/sdd/task-16-17-report.md`).

**Bước tiếp theo**: Task 9-13 (FE Sao chép) → 16/17 (nếu chưa xong) → Phase 3 Import (18-29).

**⚠️ ĐỌC TRƯỚC KHI LÀM TIẾP**: `hrm-api/.superpowers/sdd/progress.md` — ledger ghi đủ quyết định phát sinh, 6 luật round-trip bắt buộc cho Import, và các mìn đã gỡ. Không đọc là lặp lại lỗi đã sửa.

**Blocked (cần user, KHÔNG chặn Task 9-29)**:
- Rule 1 (hàng ngừng KD) — chờ ERP xác nhận mapping `products.status` + bổ sung field vào API search
- Chèn dòng vào BG kế thừa BOM — chờ BA
- BA chốt: reallocate vs giữ phân bổ tay; `solution_id`/`pricing_request_id` sau đổi dự án

**Chưa test được (không có dữ liệu thật)**: báo giá ngoại tệ (8/8 BG đều VNĐ rate=1); `discount_method=2` (0 BG); `pricing_requests` (0 row). Mọi test 3 nhánh này dùng data ép trong transaction.

---

## Phase 4: Nâng UX Import modal giống BomImportModal (hướng B — user yêu cầu 2026-07-16)

> Chốt: giống TRẢI NGHIỆM BomImportModal, KHÔNG đổi BE (giữ all-or-nothing + đổ-lưới). Chỉ sửa `QuotationImportModal.vue`.

- [x] Task 30: Thêm stepper 3 bước (Chọn file → Kiểm tra dữ liệu → Áp vào lưới) + bảng preview inline dựng từ `result.products/groups/serviceItems/discounts/shipping` (BE success đã trả sẵn resolved); ô lấy từ ERP đánh dấu "chuẩn hệ thống" (dùng `*_name` có sẵn), `plainText()` cho TSKT; thống kê 4 nhóm (hàng hoá/dịch vụ/GG/shipping); nút "Áp vào lưới báo giá" mới emit `import-applied` (chuyển confirm ghi đè sang bước này); GIỮ popup lỗi 422 hiện có; mượn `_validateSeq` guard. Style bám BomImportModal, scoped, tránh `.text-muted` đỏ.
- [x] Task 31/32: Làm QuotationImportModal thành CLONE LAYOUT BomImportModal (fullscreen 98vw×98vh + header/subtitle + stepper 3 bước + toolbar 3 nhóm gồm "Tải file mẫu" + bảng luôn hiện có cột Trạng thái + ô ERP khoá 🔒 + footer Bỏ qua dòng lỗi/Import/Làm mới/Đóng). Logic báo giá (BE all-or-nothing giữ nguyên; 422 map excelRow→dòng đỏ trên bảng). Test render thật OK, flow trọn: Tải mẫu ✓, Load lên bảng ✓, Validate ✓ (41 Hợp lệ), Import ✓ (lưới 41 SP giữ giá).


- [x] Feature: Import báo giá tự tạo Master Data (Model/Thương hiệu/Xuất xứ) khi hàng tạm có giá trị chưa có trong danh mục — parity với BOM (đảo quyết định spec §7.5). Kiến trúc KHÁC BOM: báo giá không có endpoint ghi DB, `validate` cố ý không ghi. Isolate theo yêu cầu "chỉ khi import, KHÔNG đụng đường Lưu chung":
  - BE `QuotationImportService`: property `autoCreateMaster`; `resolveMasterId` model/brand/origin không khớp → preview: CẢNH BÁO (id null, trả `warning`), import: tự tạo (`resolveOrCreateMasterId` dedup LOWER(TRIM) + `generateBrandCode` + lọc cột Schema, mysql2) → id thật; ĐVT vẫn lỗi đỏ, TH/XX rỗng vẫn bắt buộc. Gắn `warnings` vào từng product (giữ qua stripInternalKeys). `validate($autoCreate=false)`.
  - BE controller/route: `POST /import-excel/import` → `importExcel()` 2 lượt (validate false chặn lỗi trước để không tạo rác → validate true tạo master data + trả id thật). `validate` preview giữ nguyên (không ghi DB).
  - FE `QuotationImportModal`: `__warnings`+`hasWarn`+trạng thái vàng "Hợp lệ (tạo mới)"+dòng note+pill "Tạo mới danh mục"+`warnCount`; CSS vàng; `handleImport` gọi endpoint import mới (thay vì emit cache) → nhận id thật → emit lưới. Đường Lưu (PUT) KHÔNG đổi.
  - Test: BE tinker q66 — preview cảnh báo/không ghi DB, import tạo model/brand(code)/origin + link đúng, ĐVT bịa→lỗi, TH/XX rỗng→lỗi, dedup=1. Browser E2E q81 (owner 13): validate "Hợp lệ (tạo mới)"/warnCount=1/canImport=true; Import gọi endpoint → product id thật (37692/1336/115) + warnings clear; master data tạo đúng + khớp id lưới. Dọn q81 + master test.

- [x] Fix bug: Import báo giá — sau Validate lỗi (bật "Chỉ dòng lỗi"), sửa ô làm mất dòng. Nguyên nhân: `onCellEdit` đặt `__status=''` → không còn 'invalid' → `filteredRows` (lọc invalid khi `onlyErrors`) rớt dòng. Fix (`QuotationImportModal`): thêm cờ `__edited` (makeRow) — `onCellEdit` set true, `filteredRows` giữ dòng `invalid || __edited`, `applyErrors` reset false khi Validate lại. Verify browser: sửa ô dòng lỗi → dòng còn hiện (filtered=1, stillVisible=true).

- [x] Fix bug: Import báo giá bằng chính file mẫu → báo "[Thuế VAT]/[Đơn Giá nhập]/[Đơn Giá bán] không hợp lệ" dòng 1. Nguyên nhân: ô ví dụ trong file mẫu lưu dạng TEXT có định dạng ("250,000,000" phẩy phân cách nghìn, "10.00%" có %) → BE `number()` dùng `is_numeric()` thẳng → reject. Fix (`QuotationImportService::number()`): giữ đường nhanh số thuần; nếu không, bỏ %/ký hiệu tiền/space + chuẩn hoá phân cách nghìn↔thập phân cả 2 kiểu vi-VN & EN-US (dấu sau cùng = thập phân; chỉ 1 loại dấu → regex nhóm nghìn \d{1,3}(sep\d{3})+). Áp cho mọi cột số import (VAT/giá/SL/GG). Test: number() đúng cho "250,000,000"→250000000, "10.00%"→10, "1.500.000"→1500000, "1.234,56"→1234.56, "2,5"→2.5; validate dòng ví dụ file mẫu hasErrors=false, giá/VAT parse đúng. LƯU Ý: cần deploy lên dev (lỗi user gặp là do dev đang chạy code cũ).

- [x] Mở rộng fix số định dạng cho cả GG Tổng & GG Mặt hàng: `positiveNumber()` cũng qua `number()` khoan dung (trước chỉ `is_numeric` khắt khe) → khối GG tổng ("Giá trị"/"Thành tiền GG" text định dạng) + cột GG(%)/GG(đ) + Số lượng đều nhận. Test tinker: GG mặt hàng (dm=1) hasErrors=false giá/GG parse đúng; GG tổng (dm=2) hasErrors=false, khối GG (5%/5.000.000) + Phân bổ GG parse đúng. Lưu ý: "Loại GG" trong khối GG tổng phải khớp tên danh mục thật (không auto-create).

- [x] Fix dữ liệu file mẫu import (3 file import_baogia_*.xlsx, cả root + hrm-client/static): dòng ví dụ có nhiều lỗi dữ liệu khiến import file mẫu bị chặn. Đã sửa: (1) dòng con cùng Nhóm cha/con với dòng cha (luật nối Mã hàng cha yêu cầu CÙNG nhóm lá — export cũng ghi con cùng nhóm cha); (2) ĐVT "Cụm" không có master → đổi "Bộ"; (3) fill VAT rỗng ở dòng con (VAT bắt buộc từng dòng); (4) GG Tổng: xoá khối "Giảm giá tổng" ví dụ (Loại GG "Giảm giá khách hàng VIP"/"Voucher..." không có trong danh mục, loại GG không auto-create + khác nhau theo hệ thống) → để trống ("Nhập nếu có"). Verify E2E: cả 3 file mẫu validated=true, 5/5 hợp lệ, canImport=true (còn cảnh báo vàng brand/origin/model ví dụ → auto-create, không chặn). CẦN redeploy static hrm-client để dev phục vụ file mẫu đã sửa.

- [x] Fix UX: Validate lỗi khiến dòng không lỗi thành "Chưa validate" và bị ẩn. Nguyên nhân: all-or-nothing → server chỉ trả lỗi, applyErrors reset mọi dòng về "" + TỰ bật onlyErrors=true → lọc "Chỉ dòng lỗi" ẩn các dòng "". Fix: bỏ `this.onlyErrors = true` trong applyErrors → sau Validate lỗi HIỆN TẤT CẢ dòng (lỗi tô đỏ, còn lại "Chưa validate"), user tự bật lọc nếu muốn. Verify E2E: 3 dòng (2 tốt + 1 lỗi) → onlyErrors=false, filteredRows=3, không dòng nào bị ẩn.

- [x] Fix bug: Import báo giá — sau Validate, các cột công thức (Thành tiền nhập/bán, Tỷ suất lợi nhuận, Giá trị VAT, Thành tiền sau VAT, Đơn giá sau GG, Phân bổ GG) bị TRỐNG. Nguyên nhân: BE validate chỉ trả field gốc; buildResolvedRows không điền cột công thức (lúc Load raw thì lấy từ file nên có). Fix (QuotationImportModal.buildResolvedRows): tự tính cột công thức từ số đã resolve theo ĐÚNG công thức lưới thật edit.vue (lineImportTotal, lineSaleAfterDiscount: dm=1 trừ GG(đ)×qty / dm=2 trừ Phân bổ / không GG giữ nguyên; lineVatAmount; lineAfterVat; margin=(sale-imp)/imp). Áp cho cả dòng hàng hoá & dịch vụ. Verify E2E không GG: sau Validate các cột hiện đủ (250M/320M/28%/32M/352M...), khớp lưới sau import.

- [x] Sửa số liệu file mẫu import cho hợp lý (3 file, root + static): trước đây tiền dòng cha ≠ tổng dòng con. Đặt lại: cha STT1 = tổng 2 con (nhập 200tr=150+50, bán 240tr=180+60), mọi cột Thành tiền nhập/bán/Giá trị VAT/Thành tiền sau VAT/Tỷ suất tính đúng công thức từng dòng; GG Mặt hàng demo GG(đ) 5tr ở dòng đứng riêng (bán 110tr, tỷ suất 37.5%) giữ cha-con sạch; GG Tổng Phân bổ GG=0 (khối GG để trống). Verify: python cha=tổng con True cả 3 file; E2E validate không GG pass 5/5, sau Validate cha=tổng con (nhập 200tr, bán 240tr). CẦN redeploy static hrm-client.

- [x] Sửa 3 điểm import báo giá theo nghiệp vụ:
  1) VAT hàng hoá CON không validate (lưới không có VAT cho con). BE validateDirectRows: nếu $isChild → vat=0, KHÔNG gọi requireVat. Verify: con VAT rỗng/rác→không lỗi, cha VAT rỗng→vẫn lỗi (theo STT).
  2) Quy tắc VAT đã đúng (không sửa): ERP đè %VAT từ Master Data ($erp->vat_percent), tạm đọc Excel (requireVat), lỗi "Thuế VAT tại dòng [STT] không hợp lệ".
  3) Dịch vụ & chi phí khác KHÔNG có Mã hàng → không load lên lưới. FE: buildResolvedRows (preview) + onImportApplied (edit.vue) service code=''; template 3 file bỏ Mã hàng dòng dịch vụ + bỏ VAT/Giá trị VAT dòng con (sau VAT=thành tiền bán). Verify E2E: dịch vụ code='' preview+lưới, con vat=0.
  CẦN deploy BE+FE + redeploy static template.

- [x] Áp mẫu import KGG mới + logic đỏ (doc 10790). Quyết định user: ĐVT giữ chặn lỗi (sửa template Cụm→Bộ); Tên dịch vụ PHẢI khớp danh mục chi phí (costs master), không→lỗi đỏ; VAT vận chuyển đọc file.
  - Template KGG (root+static): thay bằng file mới (2 sheet import_KGG+huong_dan, có dòng Chi phí vận chuyển STT4); sửa STT con bị Excel đổi thành ngày→text (1.1/1.2); ĐVT Cụm→Bộ; tên dịch vụ→cost thật "Phí kiểm định". 2 template GG cũng đổi tên dịch vụ.
  - BE QuotationImportService: (1) Dịch vụ tên khớp costs master (mysql2) → cost_id+tên chuẩn+VAT từ cost; không khớp→lỗi "Dịch vụ '[x]' không tồn tại trong danh mục chi phí"; helper resolveCostByName + cache costsByName. (2) Dịch vụ SL mặc định 1 (bỏ requireQty), bỏ validate ĐVT (unit_id=null), VAT từ cost không đọc file. (3) Nhóm con trống Nhóm cha → lỗi "Nhóm hàng cha không được trống" (đổi message theo doc). (4) VAT vận chuyển giữ đọc file.
  - Verify E2E template mới: validate 6/6 pass canImport; import thật dịch vụ cost_id=12/vat8/qty1, shipping cost45tr/vat8/nhập30tr, tổng 480tr; con vat=0; tên dịch vụ bịa→lỗi; Nhóm con thiếu cha→lỗi. CẦN deploy BE + redeploy static template.

- [x] Fix 2 lỗi lưới sau Validate: (1) dòng Chi phí vận chuyển mất cột công thức (Thành tiền nhập/bán, VAT, tỷ suất) — buildResolvedRows block shipping chỉ set price+vat → thêm tính đủ import_total/sale_total/vat_amount/after_vat/margin/after_gg/alloc_gg (SL ngầm=1). (2) Loại đổi text sau validate — sửa nhãn về đúng file/dropdown: 'Hàng hoá', 'Dịch vụ & Chi phí khác', 'Chi phí vận chuyển' (trước là 'Hàng hóa'/'Dịch vụ'/'Vận chuyển'). Verify E2E: Loại đúng + shipping cột công thức đầy đủ (30tr/45tr/3.6tr/48.6tr/50%).

- [x] VAT Chi phí vận chuyển cố định 8% + disable: (BE) buildShipping bỏ requireVat, shipping_vat_percent = SHIPPING_VAT_PERCENT(8) — bỏ qua giá trị file (dù nhập bao nhiêu cũng trả 8, VAT trống không còn báo lỗi). (FE edit.vue) 2 ô VAT vận chuyển (% + ₫) đổi :disabled="!canEdit" → :disabled="true" (luôn khoá). Verify E2E: file VAT=20 → preview 8, import → shippingVatPercent=8, 2 input disabled=true.

- [x] Thay template GG Mặt hàng + GG Tổng theo mẫu mới (Google Sheet 10790, tab GG_mat_hang/GG_tong). Mỗi file 2 sheet (data + huong_dan_10790), có dòng Chi phí vận chuyển, mô hình "trọn gói" (con chỉ giá nhập/bán). Fix để import sạch: STT float/ngày→text (1/1.1/1.2/2/3/4); ĐVT Cụm→Bộ (GG mặt hàng); tên dịch vụ→cost thật "Phí kiểm định"; GG Mặt hàng điền Đơn Giá bán dòng con (thiếu trong mẫu); GG Tổng clear khối discount ví dụ (Loại GG hệ-thống-riêng) + Phân bổ GG + điền Đơn Giá bán dòng vận chuyển. Verify E2E: cả 2 validate 6/6 canImport, shipping VAT=8. Logic đỏ (doc) áp chung ở BE cho mọi loại GG (service khớp costs, con bỏ VAT, Nhóm con bắt buộc cha, shipping VAT 8, service/shipping bỏ Mã hàng). CẦN redeploy 3 static template.

- [x] Thêm cột "Có tính doanh thu" (Có/Không) — bắt buộc cho Dịch vụ (Có→II Doanh thu/rev=1, Không→III Chi phí/rev=0) + dịch vụ tên chưa có danh mục costs → CẢNH BÁO vàng + tự tạo (đảo quyết định "lỗi đỏ" trước đó theo yêu cầu). 
  - BE import: COL_REVENUE + READ_PRODUCT_COLUMNS; buildServiceItem validate Có/Không (bắt buộc), set revenue_calculation từ cột; cost không khớp → cảnh báo (preview)/resolveOrCreateCost (import, insert costs mysql2 name/vat file/revenue/kind_of) + warnings; trả revenue_calculation + rate_value_capital.
  - BE export QuotationExcelExport: thêm 'Có tính doanh thu' vào $common (vị trí 2, mọi loại GG → 23/26/25 cột); collectServiceItems batch revByCost; renderRow ghi Có/Không theo costs.revenue_calculation; sample service 'Có'.
  - FE QuotationImportModal: cột 'revenue' vào grid + QIM_HEADER_BY_KEY + buildRawRows/makeRow + buildResolvedRows (service Có/Không + warnings→dòng vàng). edit.vue onImportApplied: map revenue_calculation + rate_value_capital.
  - Template: KGG mới (2 dịch vụ Có/Không, tên tự do→auto-create) fix STT/ĐVT; 2 template GG chèn cột 'Có tính doanh thu' (product block).
  - Verify E2E: KGG validate 7/7 warn=2 (dịch vụ auto-create cost 574/575 rev 1/0), import cost_id map; export ghi Có/Không đúng theo cost; 2 template GG validate 6/6. CẦN redeploy 3 static template + BE + FE.

- [x] Fix style + layout 2 template GG sau khi chèn cột 'Có tính doanh thu': (1) copy style cột A→B mọi dòng (header xanh đậm chữ trắng + data chữ đỏ mẫu) + set width B; (2) GG Tổng: khối "CẤU HÌNH GIẢM GIÁ TỔNG" bị insert_cols đẩy dư 1 cột → tịnh tiến khối discount về lại A-E (STT/Loại GG/Kiểu/Giá trị/Thành tiền GG), chỉ product block giữ cột B. Verify: GG Tổng validate 6/6 canImport, style B khớp cột kề.

- [x] Verify đổi file không vỡ logic + audit doc đỏ: round-trip export q66 (41 SP, cột 'Có tính doanh thu' + layout dịch) → re-import 41/41 pass; công thức export tự chỉnh letter đúng (Thành tiền bán =O*R, VAT =S*U/100). Audit text đỏ: cột Có/Không (dropdown, bắt buộc dịch vụ, lỗi đúng chuẩn) ✓, auto-create dịch vụ+cảnh báo ✓, Có→II/Không→III ✓; SỬA kind_of=1→2 (theo ERP costs?kind_of=2). Rate cost=0 (giá nhập giữ file, sync submit — recalcSvcCost bỏ qua khi rate=0, không wipe). Link ảnh prnt.sc KHÔNG xem được (Lightshot chặn) → implement theo mô tả text.

- [x] Thêm cột "Ghi chú" vào bảng sản phẩm/dịch vụ form sửa báo giá (edit.vue) — parity với lưới import. Đặt sau "Thông số kỹ thuật" trong nhóm cột chi tiết (ẩn/hiện theo "Hiện cột chi tiết"). Ô input sửa được bind note cho dòng cha/con/dịch vụ; cập nhật 3 colspan section + tableColspan (+4→+5). note đã có sẵn trong data + save payload. Verify: thCount=21=prodRowTdCount (khớp cột), 5 ô Ghi chú (4 SP + 1 DV), hiện đúng dữ liệu import ("Vật tư con", "Độc lập").

- [x] Ẩn cột công thức cho HÀNG CON (giống file Excel mẫu): dòng con để trống Thành tiền bán, Tỷ suất lợi nhuận, Thuế VAT%, Giá trị VAT, Thành tiền sau VAT, Đơn giá sau GG, Phân bổ GG — giữ Đơn Giá nhập/Thành tiền nhập/Đơn Giá bán. Sửa 3 nơi: lưới import buildResolvedRows (isChildRow → '' cho các cột đó); edit.vue + index.vue child row (Thành tiền bán → —, các cột kia vốn đã —). Verify E2E: q91/edit con TTbán='—', lưới import con sale_total/margin/vat/vat_amount/after_vat=trống, giữ import_total+price.

- [x] Lưới popup import xử lý quyền "Xem giá vốn hàng hoá" (trước đây CHƯA — lộ giá vốn ERP + luôn hiện cột). BE QuotationImportService: thêm importCanViewCost (isCurrentEmployeeHasPermission) + importIsCreator + helper gateCost($value,$isErp) → ẩn (null) giá vốn nếu không quyền VÀ (hàng ERP HOẶC không phải người tạo); áp cho estimated_price 3 output (direct product + BOM product + service). Khớp logic DetailQuotationResource/canSeeCostOf. FE buildResolvedRows: khi estimated_price=null (noCost) → để trống Thành tiền nhập + Tỷ suất (cả product & service; Đơn Giá nhập vốn đã blank khi null). Verify reflection: có quyền thấy hết; không quyền+creator ẩn ERP giữ tạm; không quyền+không creator ẩn hết.
