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

- [x] Chuẩn hoá cột % trong export/template Excel báo giá: cột "Tỷ suất lợi nhuận" đổi header → "Tỷ suất lợi nhuận (%)", ô chỉ ghi SỐ (bỏ hậu tố "%"). Sửa QuotationExcelExport: PRODUCT_COLUMNS superset + productColumns() suffix + NUMBER_HEADERS_PRODUCT + $cells key (renderRow) + 5 dòng sample ('40%'→40, '50%'→50, '66.67%'→66.67, '33.33%'→33.33). GG(%)/Thuế VAT(%) đã sẵn (%) ở header + ô số. Import không đổi (cột công thức bị bỏ qua; number() vốn strip %). Lint PASS.
  - Sửa 3 file mẫu tĩnh tải về (hrm-client/static/import_baogia_khong_gg.xlsx, import_baogia_gg_mat_hang.xlsx, import_baogia_gg_tong.xlsx) qua openpyxl: đổi ô % (GG(%)/Tỷ suất/Thuế VAT: "60.00%"→60, "39.31%"→39.31...) sang SỐ, header "Tỷ suất lợi nhuận"→"Tỷ suất lợi nhuận (%)". Tổng 28 ô + 3 header. Giữ nguyên style/merged/sheet hướng dẫn/dims. Verify: 0 ô % còn sót, header đủ (%).
  - Sửa lưới popup import (QuotationImportModal.vue) đồng bộ header mới: (1) buildRawRows đọc key 'Tỷ suất lợi nhuận (%)' (fallback tên cũ) → cột Tỷ suất load lên lưới lúc mở file (trước bị trống do lệch key); (2) header cột lưới + QIM_HEADER_BY_KEY đổi 'Tỷ suất lợi nhuận'→'... (%)'; (3) bỏ hậu tố "+ '%'" ở 3 chỗ tính margin trong buildResolvedRows (product/service/shipping) → sau Validate ô Tỷ suất chỉ hiện SỐ, không còn "%". VAT/GG(%) vốn đã đúng.
  - Fix "dấu phẩy sau số" cột % khi export (QuotationExcelExport): PhpSpreadsheet render format '#,##0.##' (và mọi '.#'/'.0') thành số lẻ CỐ ĐỊNH ("8"→"8.00"→locale VN "8,00"). Tách GG(%)/Tỷ suất/Thuế VAT khỏi NUMBER_HEADERS_PRODUCT sang PERCENT_HEADERS_PRODUCT dùng FORMAT_GENERAL (hiện "8", "66,67" sạch); bọc công thức Tỷ suất bằng ROUND(...,2) để General không hiện số lẻ dài. Verify tinker: forBlank(1) + export thật BG-148 → 3 cột % đều 'General', Tỷ suất =IFERROR(ROUND(...,2),""). Cột "Số lượng" giữ '#,##0.##' (chưa báo lỗi; có thousands grouping). Static template vốn đã 'General' nên không lỗi.

### Checkpoint — 2026-07-31: Testcase Export/Import/Sao chép
- [x] Viết testcase 184 TC (9 section) cho Export chi tiết / Import / Sao chép của Báo giá + BOM List → `.plans/baogia-copy-export-import/testcase.xlsx` (script sinh: `testcase-export-import-copy-generate.py`). Không bao gồm export màn danh sách.
- [x] Bổ sung 2 section nhóm hàng 2 cấp + kéo-thả (X: Báo giá 29 TC, XI: BOM 21 TC) + sửa 2 TC lệch code mới (export BG 22/25/24 cột động theo Loại GG; export BOM 15 cột FLAT_HEADERS). Tổng 235 TC.
- [x] 2026-07-31: Testcase TỔNG THỂ 2 màn → `.plans/testcase-bom-baogia/testcase-bao-gia.xlsx` (137 TC / 12 section) + `testcase-bom-list.xlsx` (79 TC / 9 section). Viết theo logic code mới nhất; export/import/sao chép trỏ sang testcase riêng.
- [x] 2026-07-31 (2): GỘP toàn bộ testcase Export/Import/Sao chép + nhóm 2 cấp vào 2 file tổng thể → testcase-bao-gia.xlsx 289 TC/17 section, testcase-bom-list.xlsx 155 TC/13 section. `.plans/baogia-copy-export-import/testcase.xlsx` giờ chỉ là nguồn dữ liệu, nội dung đã nằm trọn trong 2 file kia.

### Checkpoint — 2026-08-05: Fix đổi dự án trên báo giá sao chép
- [x] Fix fatal `Class 'Modules\Assign\Services\Customer' not found` (QuotationService.php:1636 — khối `$isProjectChange`): đổi `Customer::find()` → `TpCustomer::find()` cho khớp import dòng 20 + 3 chỗ dùng khác trong file.
- [x] Chốt quyết định treo #6 (`solution_id`/`pricing_request_id` sau khi đổi dự án) = **XOÁ TRẮNG**. Lý do: báo giá lấy giải pháp từ BOM (`create()` đọc `bomList->solution_id`), không từ dự án; đổi dự án đã ngắt BOM nên giữ `solution_*` = hiện giải pháp của DỰ ÁN CŨ trên màn edit (BG-2026-00233 ở dự án 41 vẫn hiện giải pháp của dự án 38). Không suy giải pháp từ dự án mới vì `solutions.prospective_project_id` chỉ có index thường (không unique).
- [x] Set null 7 field trong nhánh `$isProjectChange`: `solution_id`, `solution_version_id`, `solution_version_code`, `solution_module_id`, `solution_module_version_id`, `module_version_code`, `pricing_request_id`. FE không sửa (dòng Giải pháp/Hạng mục tự ẩn khi `item.solution` null).
- [x] Verify tinker 4 case (PASS hết): (A) BG thường gửi `project_id` vẫn bị bỏ qua, solution giữ nguyên, `note` vẫn lưu; (B) bản sao đổi dự án → solution_* + pricing_request_id null, BOM ngắt, type=2, 2 dòng hàng hoá giữ nguyên; (C) đổi tiếp sang dự án thứ 3 vẫn đúng; (D) gửi lại đúng dự án hiện tại không kích hoạt nhánh. Đã xoá BG test 236 + khôi phục `note` BG 65.

### Checkpoint — 2026-08-05 (2): Đổi dự án KHÔNG lưu ngay + reset như màn tạo
- [x] Bỏ hoàn toàn cơ chế "đổi dự án lưu ngay". FE `edit.vue`: `onEditProjectSelect()` giờ confirm rồi reset `products`/`directGroups`/`serviceItems`/`quotationDiscounts` + gọi `selectProject()` y như màn tạo, KHÔNG gọi API; xoá hẳn `changeProjectNow()`; hint dưới select viết lại theo sự thật mới.
- [x] `save()` gửi kèm `project_id` + `bom_list_id` khi dự án khác `serverProjectId` (biến mới, chụp ở `fetchData`). Nhánh silent (Gửi duyệt) `fetchData()` lại sau khi lưu vì BE vừa dựng lại toàn bộ dòng.
- [x] Thêm computed `pendingProjectChange` — đã đổi dự án nhưng chưa Lưu: hiện ô "BOM tổng hợp" (trước chỉ có ở màn tạo, dự án mới có >1 BOM thì không chọn được) và cho `isDirectQuotation` bám theo BOM đang chọn thay vì `type` cũ dưới server.
- [x] BE `QuotationService::update()` nhánh `$isProjectChange` viết lại: xoá sạch 4 nhóm chi tiết (prices, groups, service items, discounts) → nhận `bom_list_id` của dự án mới (validate BOM phải thuộc đúng dự án, sai thì throw) → `type` 1/2 + `solution_*` suy từ BOM mới y hệt `create()`. Bỏ `materializeBomStructureIntoPrices()` + `materializeBomGroupsIntoQuotation()` (đã thành code chết, xoá luôn ~200 dòng).
- [x] Tách `copyBomIntoQuotation()` từ `create()` để cả 2 luồng dùng chung (giá theo `price_type_id` + quy đổi `exchange_rate` rất dễ lệch nếu viết lại).
- [x] Thay `!$isProjectChange` bằng `$skipDetailSync` = đổi dự án SANG dự án CÓ BOM: bỏ qua products/groups/service_items/quotation_discounts (nguồn sự thật là BOM, giống create). Dự án mới KHÔNG BOM → payload ghi bình thường ⇒ đổi dự án + nhập hàng mới xong trong 1 lần bấm Lưu. Thêm guard shape: payload shape BOM (thiếu `price_id`/`name`) bị bỏ qua + `Log::warning` thay vì ghi ra bảng hàng hoá trắng.
- [x] Verify tinker 9 case PASS: (A) đổi sang dự án có BOM → 6 SP + solution của BOM mới, type=1; (B) dự án không BOM → sạch trơn, type=2, solution null; (C) đổi dự án + nhập hàng mới cùng lần Lưu → ghi đủ; (D) payload shape BOM → bỏ qua, không dòng trắng; (E) BOM sai dự án → chặn + rollback; (F) BG thường gửi `project_id` vẫn bị bỏ qua; (G) `create()` không đổi hành vi sau refactor; (H) BG có đủ nhóm/dịch vụ/GG → đổi dự án xoá sạch, không sót dòng cũ; (I) đổi dự án 2 lần liên tiếp. Đã xoá 7 BG test + khôi phục `note` BG 65.
- [x] Fix: sau khi chọn lại dự án, màn sửa vẫn hiện dòng chỉ-đọc "BOM / Giải pháp / Hạng mục" của dự án CŨ (màn tạo không có các dòng này). `selectProject()` dọn luôn `bom_list`, `solution`, `solution_version_code`, `solution_module`, `solution_module_version_code`, `pricing_request_id/code` trên `item`; 2 dòng `<tr>` Hạng mục + BOM thêm guard `!pendingProjectChange`.
- [x] Kèm theo: Tiền tệ + Bảng giá mở khoá khi `pendingProjectChange` (trước chỉ sửa được ở màn tạo). BE nhánh đổi dự án chốt `currency_id`/`price_type_id` theo dự án mới đúng luật create() (dự án CON kế thừa cứng) và TÍNH LẠI `exchange_rate` — `copyBomIntoQuotation()` quy đổi giá ERP bằng tỷ giá này, dùng tỷ giá tiền tệ cũ là sai tiền. Khối `currency_id` chung + `discount_method` thêm nhánh `$isProjectChange` (soi `$newProject`, không phải `$quotation->project` vốn còn là dự án cũ).
- [x] Verify: chạy lại đủ 9 case cũ (PASS) + case J (đổi dự án → tiền tệ/bảng giá/tỷ giá theo dự án mới, 6 dòng BOM giá quy đổi đúng). Xác nhận bằng `git diff` là luồng KHÔNG đổi dự án không bị chạm (whitelist `currency_id`/`price_type_id` giữ nguyên). Đã dọn 9 BG test.

### Checkpoint — 2026-08-19: Fix thứ tự nhóm hàng + round-trip export→import
Bối cảnh: khách báo BG-2026-00121 (sao chép từ BG-2026-00111) "sắp xếp linh tinh". Đã dựng lại `copy(111)` trong transaction rollback → **lệnh Sao chép ĐÚNG** (280 dòng, 24 nhóm, 22 nhóm giữ cha, sort_order 0–279 y hệt gốc). Dữ liệu BG 121 hỏng do một lần lưu lúc 18/8 17:04–17:05 dựng lại toàn bộ lưới (mọi `price_id` và id nhóm đều mới) — dấu hiệu của Import Excel chế độ "Thay thế".
- [x] BE `DetailQuotationResource`: thêm tie-break `orderBy('id')` cho cả `quotationGroups` và `quotationProductPrices`. `sort_order` nhóm con đánh riêng theo từng cha (cha A: 0,1,2… / cha B: 0,1,2…) ⇒ trùng số rất nhiều, thiếu tie-break thì MySQL trả thứ tự không xác định và thứ tự nhóm trên màn đổi giữa các lần load.
- [x] FE `pages/assign/quotations/_id/index.vue` — `groupedRows()` duyệt phẳng `item.groups` nên **màn chi tiết không dựng cây 2 cấp**: 2 nhóm cấp 1 ("DANH MỤC THIẾT BỊ SỬA CHỮA CHUNG/ĐỒNG SƠN") biến mất và 2 nhánh con xen kẽ nhau. Viết lại theo đúng thuật toán `edit.vue::groupedRows()` (cây 2 cấp, số La Mã I / I.1, nhóm cha rỗng vẫn hiện nếu còn nhóm con có hàng), template dùng `romanLabel` + thụt lề cấp 2.
- [x] BE `QuotationExcelExport`: thêm `orderedGroupIds()` — thứ tự nhóm trong file xuất duyệt theo CÂY (cha → các con của chính nó) thay cho `array_keys($groupNames)` phẳng theo `sort_order`; nhóm con mồ côi xếp cuối thay vì mất. Verify BG 111: 24 nhóm ra đúng I→XIV nhánh CHUNG rồi mới sang nhánh ĐỒNG SƠN.
- [x] BE `QuotationImportService::requireQty()`: **cho phép SL = 0** (chốt với user 19/8), bỏ `positiveNumber()`. Lưu nháp cho SL = 0 là hợp lệ (`qty_needed` => `numeric|min:0`, 306 dòng đang có SL=0) nhưng import ép > 0 ⇒ file do chính hệ thống xuất ra không import lại được (BG 111: 44/280 dòng lỗi, all-or-nothing chặn cả file). Ô trống / số âm / chữ vẫn báo lỗi.
- [x] Verify round-trip export→import (export thật → đọc lại bằng PhpSpreadsheet → `validate()`): BG 111, 145, 88, 92, 80, 61, 94, 95, 56, 59, 119 đều không lỗi; BG 111 giữ đủ 280 dòng + 22 nhóm (20 nhóm cấp 2). Trước khi sửa: 111 và 145 chặn 44 lỗi SL.
- [x] Verify copy (transaction rollback) BG 111, 94, 95, 119, 80, 88: hàng hoá khớp toàn bộ trường cấu trúc + vị trí cha-con, nhóm giữ đúng số cấp 2, không dòng/nhóm nào "mượn" id của báo giá gốc, dịch vụ sinh mã mới đúng.
- Không phải lỗi (đã loại trừ sau khi kiểm chứng): tên/VAT/giá hàng ERP lệch so với file là do import cố ý lấy dữ liệu ERP hiện tại (đồng nhất `copy()` Rule 2/3); `estimated_price` = NULL sau import là mask theo quyền "Xem giá vốn hàng hoá" (`gateCost`), không mất giá — hàng ERP do `enforceErpProductPrice()` set, hàng tạm chỉ người tạo sửa được và người tạo luôn thấy giá.
- [x] Bổ sung sau rà lại: tie-break `orderBy('id')` cho cả nhánh BOM của Resource (`bom_list_groups`) — cùng lý do trùng `sort_order`.
- [x] Test bổ sung: (a) trích NGUYÊN VĂN `groupedRows()` + `toRoman()` từ index.vue chạy bằng Node 14 với dữ liệu API thật của BG 111/121/48/12/95 → không mất dòng nào (206/206, 206/206, 4/4, 49/49, 87/87), BG 111 ra đúng cây I/I.1…II.9; (b) `vue-template-compiler.compile()` trên template → 0 lỗi; (c) nhánh BOM (type=1) màn chi tiết + export BG 48/12 chạy đúng; (d) export bản trống cả 3 Loại GG (0/1/2) đều OK.
- [ ] CHƯA làm: chạy thật trên trình duyệt (cần tài khoản dev đăng nhập).
- [x] Test trên trình duyệt thật (Playwright, tài khoản dev): BG 111 render đúng cây `I. DANH MỤC…CHUNG` → `I.1…I.11`, `II. DANH MỤC…ĐỒNG SƠN` → `II.1…II.9` (22 dòng tiêu đề nhóm, 206/206 dòng cha, thụt lề cấp 2 = 32px, 0 lỗi console); BG 48/12 (loại BOM) và BG 95 (không nhóm) không hồi quy.
- [x] **Lỗi #5 phát hiện khi bấm nút Xuất Excel thật — export báo giá lớn CHẾT TIMEOUT (bug có sẵn).** Trình duyệt báo "blocked by CORS policy" nhưng thật ra là `FatalError: Maximum execution time of 60 seconds exceeded` tại `QuotationExcelExport::fetchImageResource()` — `drawings()` tải ảnh TUẦN TỰ từng dòng. Đo BG-2026-00111: 280 lượt tải × ~1,8s ≈ 500s, `max_execution_time` 60s ⇒ không bao giờ ra file.
  - Fix 1: thêm `prefetchImages()` tải song song bằng `curl_multi` (20 kết nối), URL trùng chỉ tải 1 lần (280 lượt → 207 URL). Không có ext-curl thì tự rơi về nhánh `file_get_contents` cũ; ảnh lỗi cache `null` ⇒ ô trống, giữ nguyên hành vi.
  - Fix 2: `fetchImageResource()` đọc cache rồi rút khỏi cache ngay (không giữ ~30 MB ảnh trong RAM tới cuối request).
  - Fix 3: `QuotationController::exportQuotationData()` thêm `set_time_limit(300)` — xuất file có ảnh là tác vụ dài.
  - Đo lại: mạng 207 ảnh/30 MB còn ~30–57s (10 luồng: 57s), giải nén GD chỉ 0,5s.
  - Verify end-to-end: bấm nút Xuất Excel trên trình duyệt → tải về `BG-2026-00111_19-08-2026.xlsx` 8,3 MB, 281 dòng dữ liệu, 277 ảnh nhúng, nhóm cha gom liền mạch (hết nhánh CHUNG rồi mới sang ĐỒNG SƠN), 20 nhóm con không bị xé lẻ.
  - Verify round-trip trên chính file trình duyệt tải về: import lại KHÔNG lỗi — 280 dòng, 22 nhóm (20 nhóm cấp 2).

### Checkpoint — 2026-08-19 (2): Popup "Phát hiện thay đổi dữ liệu từ ERP" khó hiểu
Người dùng hỏi dòng "Thay đổi cấu trúc" hiện `3 → 3` để làm gì. Truy ra: cảnh báo ĐÚNG (combo trên ERP đã đổi công thức vật tư con, bản sao cố ý đóng băng cấu trúc V1 theo spec §5.3) nhưng **hiển thị làm mất sạch nội dung**: cột cũ/mới chỉ in SỐ ĐẾM con, trong khi so sánh theo TẬP `erp_product_id` ⇒ ERP thay 1-1 thì số không đổi. Ca thật BG-2026-00039 combo `ETGN-EG-EQ3204:02`: hiện "42 → 42" nhưng thực tế ERP thêm 2 (Khẩu đầu bít hoa thị T20/T25), bỏ 2 (Đầu hoa thị T20/T25 lắp chuôi khẩu 1/4").
- [x] `getCopyPreviewProductChanges()`: cột cũ/mới đổi thành `"42 vật tư con"` → `"42 vật tư con (thêm 2, bớt 2)"`. Luôn kèm phần thêm/bớt vì đó mới là nội dung thay đổi.
- [x] Thêm `dedupePreviewChanges()` — gộp cảnh báo TRÙNG HOÀN TOÀN (cùng loại + mã + tên + cũ + mới + hành động). Một mặt hàng nằm ở nhiều dòng báo giá sinh nhiều cảnh báo y hệt, người dùng đọc như popup lỗi (thật: SKYO-SBS-210A:01 hiện 2 lần). 2 dòng cùng mã nhưng giá cũ khác nhau vẫn giữ cả hai.
- [x] Verify: quét toàn bộ báo giá tự lập — 163 cảnh báo trước gộp → 158 sau gộp, chỉ 2 báo giá bị ảnh hưởng (BG-2026-00080: 27→25, BG-2026-00113: 6→3), không báo giá nào mất cảnh báo khác loại.
- [x] Verify qua HTTP thật (trình duyệt đã đăng nhập, GET copy-preview): BG 39/40/68 trả đúng chuỗi mới, `(Bỏ qua) — Giữ nguyên cấu trúc V1` giữ nguyên.
- FE `QuotationCopyPreviewModal.vue` KHÔNG phải sửa — nhãn/màu map theo `type`, nội dung lấy thẳng từ BE.

### Checkpoint — 2026-08-20: Đổi dự án trên bản sao chép làm MẤT dòng của báo giá nguồn (tester báo)
Tester: "copy báo giá từ BG độc lập sang BG độc lập, khi chọn dự án hệ thống không lấy báo giá nguồn đưa vào". Truy ra `onEditProjectSelect()` + `QuotationService::update()` đang **xoá sạch** hàng hoá/dịch vụ/nhóm/giảm giá rồi dựng lại theo BOM tổng hợp của dự án mới (hành vi chốt ở Checkpoint 2026-08-05 (2)). Dự án đích của BG độc lập thường KHÔNG có BOM ⇒ bảng trắng trơn ngay sau khi chọn dự án. Chốt với user 2026-08-20: **báo giá sao chép chỉ được chọn dự án CHƯA có BOM tổng hợp đã duyệt** (ẩn hẳn khỏi dropdown), và đổi dự án **giữ nguyên** toàn bộ chi tiết đã copy.
- [x] BE `ProspectiveProjectService::getAll()`: thêm filter `exclude_has_aggregate_bom=1` (`whereNotExists` bom_lists type=2 & status=4 & `solution_module_version_id` null).
- [x] BE `QuotationService::update()` nhánh `$isProjectChange`: guard `projectHasAggregateBom()` → throw nếu dự án đích có BOM đã duyệt; bỏ nhánh gắn BOM mới (`bom_list_id` luôn null, `type=2`, `solution_*` null); **bỏ hẳn khối xoá 4 bảng chi tiết + `copyBomIntoQuotation()`**; `$skipDetailSync` chỉ còn bật ở chốt chặn shape.
- [x] BE thêm `materializeBomRowsAsDirect()` — bản sao của BG TỪ BOM: bù `qty_needed`/`product_type`/`show_children`/mô tả từ `bom_list_products` xuống `quotation_product_prices` và **remap `parent_id`** (id BOM → `price_id`) trước khi cắt `bom_list_product_id`. Không bù thì cắt link xong ra dòng SL = 0, mất cha-con.
- [x] FE `edit.vue`: `loadMyProjects({ excludeHasAggregateBom: true })` cho bản sao chép; `onEditProjectSelect()` bỏ reset 4 mảng + đổi câu confirm; thêm `convertBomRowsToDirect()` (remap `parent_id`, bỏ nhóm BOM); `selectProject(project, { keepDetails: true })` không dò/nạp BOM dự án mới; hint dưới select + cột "BOM tổng hợp" (chỉ còn ở màn tạo) viết lại theo sự thật mới.
- [x] Seed dữ liệu test cho tài khoản `namdangit@gmail.com` (employee 13, DB `hrm_prod_6_6`): dự án `TEST-COPY-A` (203, nguồn) / `TEST-COPY-B` (204, đích, KH khác hẳn) / `TEST-COPY-C` (205, có BOM tổng hợp `BOM-2026-00025` đã duyệt) + báo giá `BG-2026-00155` (độc lập: 2 nhóm, 1 cha + 2 con ERP, 1 hàng lẻ, 1 hàng tạm, 1 dịch vụ, GG theo dòng, phí vận chuyển) và `BG-2026-00156` (từ BOM 26, 3 dòng có cha-con).
- [x] Verify bằng service thật (bọc transaction + rollback): (A) dropdown lọc BOM trả 204/203/199, ẩn 205; (B) copy BG 158 → đổi sang 204 giữ đủ 5 dòng + 2 nhóm + 1 dịch vụ, KH nạp lại theo dự án mới, `type=2`, `bom_list_id=null`; (C) đổi sang 205 bị chặn đúng message; (D) copy BG TỪ BOM 159 → đổi sang 204: `bom_list_product_id` null hết, SL/tên giữ đủ, `parent_id` remap sang id `quotation_product_prices`.
- [ ] CHƯA test bằng tay trên trình duyệt (chờ tester).

### Checkpoint — 2026-08-21: Bug tái xuất trên nhánh đang chạy (BG-2026-00169 mất sạch hàng hoá)
User copy BG-2026-00005 → đổi dự án → Lưu ⇒ 87 hàng hoá + 10 nhóm biến mất (BG-2026-00169). Truy ra **không phải bug mới**: fix ngày 2026-08-20 nằm ở commit `57fbfd0b8` chỉ trên nhánh `tpe`, nhánh API đang chạy (`tpe-develop-assign`, cổng 8000) chưa có ⇒ BE vẫn xoá sạch 4 bảng chi tiết rồi trông chờ payload dựng lại, trong khi FE (`tpe-develop-assign_fix`) đã là bản mới gửi kèm `price_id` ⇒ `saveDirectProduct()` đi nhánh UPDATE, trúng 0 dòng, không tạo lại gì.
- [x] Tái hiện bằng service thật (transaction + rollback): copy BG 5 → update `project_id=108` ⇒ 87 → **0** dòng.
- [x] Áp bản chính thức: `git cherry-pick -n 57fbfd0b8` vào `tpe-develop-assign` — tự động merge sạch, không conflict (2 file: `QuotationService`, `ProspectiveProjectService`). CHƯA commit.
- [x] Verify lại sau khi áp: 87 hàng hoá / 10 nhóm giữ nguyên, KH nạp lại theo dự án mới, `bom_list_id=null`, `type=2`, 0 dòng còn `bom_list_product_id`. Nhánh đổi sang dự án CÓ BOM vẫn reset + nạp từ BOM như cũ.
- [ ] Dữ liệu BG-2026-00169 đã mất (hard delete) — chờ user quyết: xoá bản này copy lại, hay bơm lại chi tiết từ BG-2026-00005.

### Checkpoint — 2026-08-21 (2): Nút Sao chép KHÔNG tạo bản ghi ngay nữa
User: "bấm copy là đã thấy bản ghi trong DB, tôi muốn bấm Lưu mới tạo". Chốt hướng: Copy = mở màn TẠO MỚI đã điền sẵn, báo giá chỉ ra đời khi bấm Lưu. Chốt kèm: bản sao **luôn là báo giá tự lập** (`type=2`, kể cả nguồn lập từ BOM); popup "thay đổi từ ERP" vẫn hiện ngay lúc bấm Copy; F5 mất nháp là chấp nhận được.
- [x] BE `QuotationService::buildCopyDraft()` — chạy chính `copy()` trong transaction rồi ném cờ ép rollback (pattern `previewSubmit()`), trả payload `DetailQuotationResource`. Nguồn từ BOM → `materializeBomRowsAsDirect()` + cắt `bom_list_id`/`solution_*` trước khi serialize. `id`/`code` trả null, kèm `copied_from_quotation_id/_code`.
- [x] BE `create()` nhận `copied_from_quotation_id` (ghi vết nguồn) + cờ `$keepTempProductCodes` → hàng tạm GIỮ mã của bản gốc thay vì sinh `HHBG…` mới.
- [x] BE route: thêm `GET /{id}/copy-draft`, **bỏ** `POST /{id}/copy` + action `copy()` ở controller (đổi thành `copyDraft()`). `QuotationStoreRequest` thêm rule `copied_from_quotation_id`.
- [x] FE `QuotationCopyMixin.runCopyQuotation()` → chỉ `$router.push('/assign/quotations/create?copy_from=<id>')`, không gọi API ghi.
- [x] FE `edit.vue`: tách `applyDetail()` khỏi `fetchData()` (dùng chung cho bản nháp); thêm `initCopyMode()` gỡ mọi id thật → `temp_id`/`parent_temp_id`/`groups[].temp_id`; gửi `copied_from_quotation_id` lúc POST; dòng "Sao chép từ BG-xxxxx" trên bảng thông tin.
- [x] FE `onProjectSelect()`: ở chế độ copy thì rẽ sang `onEditProjectSelect()` (keepDetails) — chọn lại dự án KHÔNG xoá hàng hoá, đúng nhu cầu "copy sang dự án khác".
- [x] Verify service thật (transaction + rollback), 3 ca: BG-5 (87 dòng/10 nhóm/27 dòng con), BG-61 (183 dòng, 55 hàng tạm — mã giữ nguyên ✓), BG-12 (nguồn TỪ BOM → nháp về type=2, 49 dòng, SL bù đủ, không còn dòng SL=0).
- [x] Verify HTTP thật `GET /assign/quotations/5/copy-draft`: 200, id/code null, 87 dòng, `quotations` count trước/sau **không đổi** ⇒ không ghi DB.
- [x] FE cảnh báo "chưa lưu": gắn `unsavedChangesMixin` vào `edit.vue` nhưng override `unsavedSnapshotSource()` trả `null` ở mọi chế độ TRỪ bản sao chép — màn Sửa / Tạo mới thường giữ nguyên hành vi cũ (form quá lớn, bật đại trà là cảnh báo giả). `markFormSaved()` gọi sau khi POST thành công.
- [ ] CHƯA test tay trên trình duyệt (chờ user duyệt chạy Playwright).

### Checkpoint — 2026-08-21 (3): Seed dữ liệu test + verify tay trên trình duyệt
- [x] Seed cho Sale **Nguyễn Bá Thắng (employee 33)**: dự án `TEST-CP-A` (206, nguồn) / `TEST-CP-B` (207, đích không BOM, KH PEPSICO khác hẳn) / `TEST-CP-C` (208, đích CÓ BOM tổng hợp `BOM-TEST-CP-C` đã duyệt, 3 dòng). Báo giá: `BG-2026-00177` (dự án A, Đã duyệt — 3 nhóm lồng, cha ERP + 2 con, 1 hàng ERP lẻ có GG 5%, 2 hàng tạm, 2 dịch vụ, phí VC), `BG-2026-00189` (dự án A, Đang tạo — bản y hệt để test copy từ nháp), `BG-2026-00190` (dự án C, lập TỪ BOM, Đã duyệt).
- [x] Verify Playwright: bấm Copy trên `BG-2026-00177` → popup ERP hiện như cũ → xác nhận → sang `/create?copy_from=188`, form điền đủ (3 nhóm, 6 dòng, cha-con, 2 dịch vụ), hiện "Mã báo giá (Chưa tạo)" + "Sao chép từ BG-2026-00177". **Đếm DB: 141 → 141, không sinh bản ghi nào.**
- [x] Verify đổi dự án trên bản nháp: chọn `TEST-CP-B` → popup "hàng hoá… được giữ nguyên" → Đồng ý → KH đổi sang PEPSICO, **hàng hoá 6 / nhóm 3 / dịch vụ 2 giữ nguyên**, DB vẫn 141. Bấm Lưu → tạo `BG-2026-00191` đủ 6 dòng / 3 nhóm (cha-con + nhóm lồng đúng) / 2 dịch vụ, `copied_from_quotation_id=188`, mã hàng tạm `HHBG010116/117` giữ nguyên, GG 5% giữ nguyên. (Bản test này đã xoá sau khi kiểm tra.)
- [x] Verify ca nguồn TỪ BOM (`BG-2026-00190`): bản nháp về `type=2`, `bom_list_id=null`, 3 dòng đủ SL/giá/mã.
- [x] Verify bỏ ngang: rời màn không Lưu → 142 báo giá / 5.255 dòng trước và sau **không đổi**.
- [x] Sửa kèm 2 lỗi lộ ra khi test:
  - `VatBulkApplyToolbar` prop `quotationId` để `required: true` nhưng KHÔNG dùng ở đâu trong component → bản sao chưa có id làm Vue nổi 6 warning. Đổi thành `default: null`.
  - `create()` KHÔNG cấp mã cho dòng dịch vụ (chỉ `update()` có) ⇒ dịch vụ nhập ở màn Tạo mới nằm dưới DB với mã rỗng vĩnh viễn (thực đo 8/18 dòng rỗng). Bổ sung `QuotationServiceItem::getNextCode()` vào `create()` — nếu không, luồng sao chép mới (đi qua create) sẽ làm MẤT mã dịch vụ so với luồng copy cũ.

### Checkpoint — 2026-08-21 (4): Luồng copy mới thiếu chốt "dự án đích không được có BOM"
User chỉ ra: bản sao chép không được chọn dự án đã có BOM tổng hợp đã duyệt (chốt 2026-08-20). Luồng copy mới đi qua màn TẠO MỚI nên thiếu CẢ 2 lớp — `update()` vẫn chặn nhưng `create()` thì không, và `initCopyMode()` gọi `loadMyProjects()` không kèm bộ lọc.
- [x] BE `create()`: thêm guard `projectHasAggregateBom()` khi payload có `copied_from_quotation_id`, cùng message với `update()`. **Chỉ chặn khi dự án đích KHÁC dự án gốc** — giữ nguyên dự án gốc phải được phép, nếu không báo giá lập từ BOM (nằm sẵn trên dự án có BOM) không tài nào sao chép được.
- [x] FE `initCopyMode()`: `loadMyProjects({ excludeHasAggregateBom: true })`, đồng thời **bù lại dự án gốc vào options** nếu nó bị bộ lọc loại (bẫy "select mất giá trị đã chọn").
- [x] Verify BE 5 ca: A→B tạo được · A→C **chặn** · C→giữ nguyên C tạo được · C→B tạo được · tạo mới thường trên C không ảnh hưởng.
- [x] Verify FE: copy BG dự án A → dropdown chỉ còn B/A/2 dự án khác, **ẩn TEST-CP-C**; copy BG dự án C → TEST-CP-C vẫn hiện và đang được chọn.

### Checkpoint — 2026-08-21 (5): Test sâu luồng copy mới, 3 lỗi nữa lộ ra
- [x] **YCBG**: chốt với user — bản sao **KHÔNG kế thừa** `pricing_request_id`. BE `buildCopyDraft()` null hoá `pricing_request_id`/`pricing_request_code` trong payload nháp; FE cố ý không gửi lên khi Lưu. Verify bằng YCBG dựng tạm (rollback): nguồn có YCBG → nháp NULL → bản sao NULL.
- [x] **Cảnh báo chưa lưu KHÔNG chạy** (phát hiện khi test tay): `unsavedSnapshotSource()` thiếu `customer_email` (trường này sống trên `item`, không nằm trong `form`) ⇒ sửa email rồi thoát không hỏi gì. Bổ sung `customer_email`, `rounding_mode`, 4 trường `shipping_*`, số dòng giảm giá. Verify: sửa email → bấm Quay lại **hiện popup "Bạn có thông tin chưa lưu"**; F5 → hiện cả `beforeunload`; màn **Sửa** vẫn thoát thẳng như cũ (đúng thiết kế).
- [x] Giảm giá theo TỔNG (`discount_method=2`): nguồn 2 dòng GG → nháp 2 dòng → bản sao 2 dòng, đúng `input_mode`/giá trị.
- [x] Gửi duyệt ngay từ bản sao: `preview-submit` 200 + **không ghi DB**; `create-and-submit` tạo báo giá `status=2` (Chờ duyệt) đúng, `copied_from` đúng (bản test đã xoá).
- [x] Copy từ **màn chi tiết báo giá** (`_id/index.vue`) — popup ERP → xác nhận → sang `/create?copy_from=189`. 2 tab dự án dùng cùng bộ API của mixin (`confirmCopyQuotation`/`quotationCopyModalProps`), đã đối chiếu code.
- [x] Quyền: người KHÔNG phải Sale phụ trách → `copy-draft` **403** và `create` **422**, cùng một message ⇒ không có ca "bấm Copy được rồi Lưu mới bị chặn".
- [ ] **CHƯA test**: copy báo giá TỔNG (`is_summary`) từ tab dự án cha; copy báo giá tiền tệ ngoại (`exchange_rate > 1`); ca báo giá lập từ YCBG trên dữ liệu thật (DB đang có 0 YCBG).
- [ ] **Cần user quyết**: báo giá lập từ YCBG — `copy-draft` gate theo quyền "Xây dựng giá bán" (người xây giá bấm được), nhưng `create` đòi Sale phụ trách ⇒ người xây giá điền xong bấm Lưu sẽ bị chặn. Chọn: (a) ẩn nút Copy với người không phải Sale, hay (b) cho `create` chấp nhận người có quyền xây giá.

### Checkpoint — 2026-08-21 (6): Chạy bộ test đầy đủ + tài liệu tổng hợp
- [x] Bộ test service-level 10 nhóm ca (bọc transaction + rollback, script `suite.php`): **35/35 đạt, 0 lỗi**. Bao gồm: nhóm lồng + combo cha-con + hàng tạm giữ mã; đổi dự án giữ chi tiết; BG từ BOM → Tự nhập; **tiền tệ USD lấy tỷ giá hiện hành (25.000 → 26.490) chứ không copy tỷ giá cũ**; **BG tổng → bản sao hết `is_summary`**; dịch vụ từ danh mục giữ `cost_id` + SL 1; copy từ nguồn ở **cả 5 trạng thái**; chặn dự án đích có BOM / cho phép giữ nguyên dự án gốc có BOM; ghi chú theo dòng; bỏ ngang không sinh bản ghi.
- [x] Ca lỗi/biên qua HTTP thật: báo giá không tồn tại → 404 · chưa đăng nhập → 401 · báo giá ngoài phạm vi xem → 404 · **route cũ `POST /{id}/copy` → 404 (đã gỡ)** · `copied_from` trỏ báo giá đã xoá → 422 kèm lỗi trường.
- [x] UI: nút Sao chép ở **tab Báo giá của màn quản lý dự án** cũng chạy đúng (popup ERP → sang `/create?copy_from=188`). Các lỗi console trên màn đó (`TktTab`, `SolutionApprovalModal`, `form-templates` 404) là lỗi sẵn có, không liên quan thay đổi này.
- [x] Tài liệu bàn giao: **`.plans/baogia-copy-export-import/Sao chep bao gia - cac truong hop xu ly.xlsx`** — 4 sheet: Luồng sao chép · 31 trường hợp & cách xử lý (kèm cột đã kiểm chứng) · Điểm còn cần chốt · Dữ liệu mẫu để thử.

### Checkpoint — 2026-08-21 (7): Làm rõ mục treo về quyền YCBG — KHÔNG cần sửa gì
User đặt đúng câu hỏi: nếu người đó vừa có quyền "Xây dựng giá bán" vừa là Sale phụ trách dự án ĐÍCH (sau khi đổi dự án) thì có chạy được không? → **CÓ**. Kiểm chứng bằng tài khoản thật (employee 13: có quyền xây giá theo công ty, là Sale dự án 204, KHÔNG phải Sale dự án 206), trên YCBG + báo giá dựng tạm rồi xoá sạch:
- Bấm Sao chép trên BG lập từ YCBG → **200** (gate theo quyền xây dựng giá).
- Lưu vào dự án 204 (là Sale phụ trách) → **200 Đã tạo báo giá**; bản sao `project_id=204`, `copied_from=290`, `pricing_request_id=NULL`, `created_by=13`.
- Lưu vào dự án 206 (không phải Sale phụ trách) → **422 "Bạn không phải Sale phụ trách dự án này"**.
⇒ Hai lớp gate bổ sung cho nhau đúng ý đồ, không phải lỗi: quyền xây giá quyết định được *đọc/sao chép*, Sale phụ trách quyết định được *ghi vào dự án nào*. **Chốt: giữ nguyên, không sửa.**
- [x] Dọn sạch dữ liệu kiểm thử (YCBG tạm + 2 báo giá).
- [x] Cập nhật Excel: thêm 2 trường hợp phân quyền (tổng **33 trường hợp**), sheet "Còn cần chốt" đổi mục này thành ĐÃ LÀM RÕ.

### Checkpoint — 2026-08-21 (8): Đã đẩy code lên nhánh tpe-develop-assign_fix
- [x] `hrm-api` commit `2eac3c1c7` (5 file) — gồm cả bản vá lỗi mất hàng hoá (nội dung 57fbfd0b8, nhánh này chưa có) lẫn luồng copy mới. Remote đã đi trước 3 commit (PR #677/#678) đụng `ProspectiveProjectService::update()` → **merge (`--no-rebase`), tự động sạch**, giữ đủ cả guard trạng thái dự án của remote lẫn `exclude_has_aggregate_bom` của mình. Merge commit `86787dffa`.
- [x] Chạy lại bộ 35 ca **sau merge**: 35/35 đạt, 0 lỗi.
- [x] `hrm-client` commit `2fddc1fed` (3 file), remote không có gì mới → push thẳng.
- [x] Đã push cả 2 repo lên `origin/tpe-develop-assign_fix`.
