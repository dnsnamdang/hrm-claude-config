# Plan: Nhóm hàng 2 cấp + kéo-thả cho BÁO GIÁ (Quotation)

> Design tóm tắt: `.plans/baogia-multilevel-groups/design.md`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-baogia-multilevel-groups-design.md`

## Trạng thái
- Bắt đầu: 2026-07-17
- Phụ trách: @manhcuong
- Tiến độ: 19/19 task ✅ (code xong + verify; chờ review tổng cuối)
- Code pushed: ❌

## Ràng buộc chung (mọi task)
- BE **PHP 7.4** — lint `/opt/homebrew/opt/php@7.4/bin/php -l` (KHÔNG `php -l`, máy mặc định 8.1). Không cú pháp PHP 8.
- FE **Vue 2 / Node 14.21.3** — gọi đúng binary (node mặc định máy là 12.x). Không cú pháp Vue 3.
- KHÔNG commit git. KHÔNG viết file test (dự án không dùng PHPUnit). Verify: `php -l` + tinker data thật (bọc `DB::beginTransaction`/`rollBack` khi ghi) + Playwright UI.
- **CHỈ localhost:3000** khi test UI; KHÔNG đụng tab remote. Tạo báo giá test riêng, dọn sau.
- **KHÔNG đụng** `bom_list.blade.php` · `App\ExcelExport\BomListExport` (dùng chung BOM) · luồng BOM · `exportExcel` (bản trình bày khách) · logic tính tiền/GG/VAT/tổng-theo-loại hiện có của báo giá · `V2BaseImportModal`/`import-helper.js`.
- Đúng **2 cấp nhóm**. Nhóm cũ phẳng → tự thành Cấp 1 (backward-compat). Migration: không FK, không transaction.
- Cha-con SẢN PHẨM nối bằng **Mã hàng cha** (nearest-above cùng nhóm lá); STT giữ làm **toạ độ/thứ tự**, không nối cha-con.

---

## Phase 1: DB + Model

### BE — Schema
- [x] Task 1: Migration `2026_07_18_100000_add_parent_id_to_quotation_groups.php` — `parent_id` unsignedBigInteger nullable, sau `quotation_id`, không FK, không transaction. Migrate local, verify cột + nhóm cũ đều NULL. (`sort_order` đã có sẵn.)
- [x] Task 2: `DetailQuotationResource` — trả thêm `parent_id` cho groups ở **cả 2 nhánh**: nhánh Tự nhập đọc `QuotationGroup` (~:71-73, thêm `parent_id` vào `get([...])`) + nhánh Từ BOM đọc `bom_list_groups` (~:123-126, thêm `parent_id`; bảng này đã có sẵn cột từ feature BOM).

## Phase 2: BE — Nhóm 2 cấp luồng Tạo/Sửa + Từ BOM

- [x] Task 3: `QuotationService::syncDirectGroups()` (~:2484) — nâng **2 pass**: PASS 1 tạo Cấp 1 (`parent_client_id` rỗng → `parent_id` null) + ghi `clientToDbId`; PASS 2 Cấp 2 resolve `parent_id = clientToDbId[parent_client_id]` (không thấy → null, không throw), **chỉ resolve từ tập id Cấp 1** (guard depth=2). `sort_order` per-sibling. Giữ chữ ký + `idMap` cho `upsertDirectProducts` gắn `quotation_group_id`. Backward-compat payload cũ → mọi nhóm Cấp 1.
- [x] Task 4: `materializeBomGroupsIntoQuotation()` (~:2033) — bổ sung copy `parent_id`: map id nhóm BOM → id nhóm báo giá (tạo Cấp 1 trước, Cấp 2 resolve qua map). BOM 2 cấp → báo giá 2 cấp; BOM phẳng → Cấp 1. Không đổi copy sản phẩm.

## Phase 3: BE — Import 26 cột + Export round-trip

- [x] Task 5-7: `QuotationImportService` — header **26 cột** (mục 5 spec); đọc `group_parent`/`group_child` (nhóm lá = con nếu có else cha) + luật `Nhóm hàng con phải có Nhóm hàng cha.`; helper `resolveImportParentLinks()` nối cha-con SP qua **Mã hàng cha** nearest-above cùng nhóm lá (lỗi `Không tìm thấy Mã hàng cha [X] ở phía trên cùng nhóm.`); STT giữ validate định dạng + không trùng nhưng **bỏ suy cha-con từ STT**; Thương hiệu/Xuất xứ bắt buộc cho hàng tạm. GIỮ 3 nhánh classify erp/tạm/pending, khối GG tổng, 3 case Loại GG + Blind-ignore, qty>0, độ dài chuỗi, replace-all.
- [x] Task 8-9: `importProducts`/upsert — tạo nhóm 2 cấp (Cấp 1 trước) + gắn `quotation_group_id` nhóm lá + nối `parent_id` SP qua map file-index (nhất quán cả khi skip_invalid). Bỏ mọi parse STT để suy cha-con.
- [x] Task 10-11: template import 26 cột (`QuotationImportService` template/controller + sheet Hướng dẫn) + Export round-trip 26 cột: `resources/views/exports/assign/quotation_excel.blade.php` (+ `Modules/Assign/Export/QuotationExcelExport.php`) — sinh cặp Nhóm cha/con theo tổ tiên, **dòng con SP LẶP** nhóm cha/con + Mã hàng cha = mã cha, STT toạ độ cây (giữ `orderByGroupTree()`), cột giá/GG/VAT giữ nguyên. Round-trip verify: export → import lại khôi phục đúng nhóm 2 cấp + cha-con SP + giá.

## Phase 4: FE — cây nhóm + kéo-thả + modal + in

- [x] Task 12: `edit.vue` + `create.vue` — model nhóm mang `parent_client_id`; loadDetail map `parent_id`→`parent_client_id`; buildSavePayload (~:2907) gửi `parent_client_id` + `sort_order` per-sibling; `addGroup(parentClientId)` + saveGroupModal sort_order per-sibling. Backward-compat nhóm phẳng cũ → Cấp 1.
- [x] Task 13-14: `edit.vue`/`create.vue` render `groupedRows` (~:1390) phẳng → **cây 2 cấp**: Cấp 1 La Mã (I) / Cấp 2 thụt lề (I.1) / sản phẩm (cha-con giữ markup) dưới nhóm lá / orphan → Cấp 1 đầu; nút **"Thêm nhóm con"** trên header Cấp 1. Giữ nguyên markup dòng sản phẩm + cha-con SP.
- [x] Task 15: Kéo-thả header nhóm — thêm handle `.q-drag-group` + group-sortable (mở rộng `initQuotationSortables()` ~:2310), `onMove: () => true` (header xen kẽ tbody SP — rút kinh nghiệm BOM), `onEnd` đọc thứ tự header cùng cấp cùng cha → cập nhật `sort_order`; cascade xoá Cấp 1 → xoá Cấp 2 con, sản phẩm thành orphan. Giữ nguyên kéo SP `.q-drag-parent/child/service`.
- [x] Task 16: `QuotationImportModal.vue` — `columns()` (~:331) 13 → **26 cột** khớp header template (label khớp `parseExcelFile`); tách nhóm cha/con + Mã hàng cha; điền xuôi **cặp** group_parent+group_child. Giữ wizard/trạng thái dòng/khối GG/race guard.
- [x] Task 17: `QuotationPrintPreview.vue` (client-side In) — render group header 2 cấp: Cấp 1 La Mã (I) + Cấp 2 thụt lề (I.1), cha-con SP giữ nguyên; `QuotationPrintConfigModal` giữ cấu hình cột/ẩn con.

## Phase 5: Verify E2E

- [x] Task 18: Migration production-safe + regression: Từ BOM (BOM 2 cấp → báo giá 2 cấp; BOM phẳng → Cấp 1), 3 nhánh classify, khối GG tổng, 3 case Loại GG, tính tiền/tổng theo loại, kéo SP cha/con/dịch vụ — không vỡ; nhóm phẳng cũ vẫn load.
- [x] Task 19: E2E Playwright 5 AC trên báo giá test riêng: AC1 tạo nhóm con (Tự nhập) · AC2 export round-trip 26 cột + In 2 cấp + round-trip import lại · AC3 import nhóm cha-con · AC4 kéo-thả + Lưu→reload · AC5 tạo báo giá Từ BOM 2 cấp giữ phân cấp.

---

## Verify (sau khi code)
- [x] Lint BE 7.4 sạch + compile FE Node 14.21.3 sạch
- [x] AC1 — tạo nhóm con (Tự nhập), UI 2 cấp, Lưu→reload giữ
- [x] AC2 — Export round-trip 26 cột đúng phân cấp + Mã hàng cha; In hiện 2 cấp thụt lề; round-trip import lại khôi phục nhóm + cha-con SP + giá
- [x] AC3 — Import nhóm cha-con → lưới đúng phân cấp, hàng con nối đúng Mã hàng cha
- [x] AC4 — kéo nhóm UI đổi ngay; Lưu→reload giữ thứ tự (con theo cha)
- [x] AC5 — báo giá Từ BOM 2 cấp giữ phân cấp
- [x] Regression: classify/GG tổng/3 case Loại GG/tính tiền/kéo SP không vỡ; nhóm phẳng cũ load thành Cấp 1
- [x] Query import validate hằng số; đường ghi không N+1

---

## Checkpoint

### Checkpoint — 2026-07-17
Vừa hoàn thành: Brainstorming (6 quyết định) + đọc template Google Sheet 26 cột + spec đầy đủ + design tóm tắt + plan 19 task/5 phase.
Đang làm dở: Chưa code.
Bước tiếp theo: chọn cách thực thi (subagent-driven / inline) → Task 1 migration.
Blocked: (không có)

### Checkpoint — 2026-07-17 (CODE DONE + REVIEW TỔNG READY)
Vừa hoàn thành: TẤT CẢ 19 task (subagent-driven; BE Task 5-7 + toàn bộ FE làm inline do agent timeout trên file lớn). Review tổng whole-branch = **READY, 0 finding chặn merge**.
Kết quả verify: BE round-trip export→import 26 cột byte-exact + cây 2 cấp dựng lại đúng (Task 18); materialize Từ BOM parent_id đúng; AC1 tạo nhóm con render I/I.1/II runtime PASS; AC4 reorderQuotationGroups + con-theo-cha runtime PASS (kéo chuột pixel là test-artifact do bảng 3400px, sortable config giống pattern BOM đã chạy); AC2/AC3/AC5 BE-verified + FE compile-clean. Compile Node 14 sạch 3 SFC. Dọn BG test 66.
FIX QUAN TRỌNG trong lúc làm: BE COL_GROUP_PARENT/CHILD đổi thành 'Nhóm hàng cha (Cấp 1)'/'Nhóm hàng con (Cấp 2)' khớp byte-exact export → round-trip không đọc rỗng.
MINOR chấp nhận (2): validateBomRows so nhóm theo tên lá (false-match nếu 2 nhóm con trùng tên khác cha, From-BOM re-import); edit.vue render header Cấp 1 rỗng nếu con toàn rỗng (cosmetic màn Sửa).
Bước tiếp theo: user nghiệm thu browser (login user tạo báo giá direct → tạo nhóm 2 cấp/kéo-thả/import/export/in) → commit + chạy migration production.
Blocked: (không có)

## Bổ sung sau nghiệm thu (2026-07-17)
- [x] Template import có DỮ LIỆU MẪU: `QuotationExcelExport::forBlank()` chèn `buildSampleProductRows()` (5 dòng minh hoạ: nhóm 2 cấp Dây chuyền sơn>Vật tư điện, cha-con TB-001→CB-001 qua Mã hàng cha, Cấp-1-đơn Cơ khí, dịch vụ, vận chuyển — dùng Master Data THẬT KOISU/AOK/DML + Japan/Taiwan/Korea + Bộ/Cái/Gói) + 2 dòng giảm giá mẫu (%/đ). Round-trip verify: import chính template mẫu → 5 SP / 3 nhóm 2 cấp / 1 dịch vụ / **0 lỗi**.
- [x] Xác nhận khu vực "CẤU HÌNH GIẢM GIÁ TỔNG" >10 dòng CHẠY ĐÚNG: export layout động (`productTitleRow = discountStart + discountCount + 1`), import parseFile tìm header khối 2 theo NỘI DUNG ('Tên hàng'+'Mã hàng') không theo dòng cố định, validateDiscountSection lặp hết mọi dòng (test 12 dòng OK). KHÔNG có cap 10 dòng.

## Bổ sung theo Loại GG (2026-07-18, user yêu cầu)
- [x] E1 (BE): `QuotationExcelExport` cột ĐỘNG theo discount_method (Không GG / GG Mặt hàng / GG Tổng) — template + round-trip export; công thức Excel remap letter theo layout (map header→letter); dữ liệu mẫu per loại GG; forBlank($discountMethod) + controller export-blank-template nhận discount_method.
- [x] E2 (FE): `QuotationImportModal` columns() ĐỘNG theo discount_method của báo giá (fill ĐỦ mọi cột kể cả cột công thức: Thành tiền nhập/Đơn giá sau GG/Phân bổ GG/Thành tiền bán/Tỷ suất/Giá trị VAT/Thành tiền sau VAT); buildRawRows+makeRow đọc đủ; tải template truyền discount_method.
- [x] E3 (FE): `QuotationProductEditModal` thêm trường Ghi chú (textarea) + lưu form.note.

## Bổ sung Ghi chú BOM→Báo giá→In (2026-07-18, user yêu cầu)
- [x] E4a (BE): DetailBomListResource trả 'note' per sản phẩm (grid load lại được).
- [x] E4b (FE): BomBuilderTableCard thêm cột "Ghi chú" ô nhập inline per dòng (cạnh Thông số kỹ thuật, cả 2 khối render) + BomBuilderEditor visibleColumns note:true + columnOptions. Verify browser BOM 25: header đúng vị trí (sau TSKT), 2 ô input inline bind product.note, note DB cũ load lên OK.
- [x] E5 (BE): Verify From-BOM quotation resource trả note (DetailQuotationResource:122 $blp->note) → note BOM tự chảy sang báo giá. Direct: $qpp->note. Verify BG From-BOM #78 (nguồn BOM #8): 2 SP có note chảy đúng từ BOM.
- [x] E6 (FE): QuotationPrintConfigModal thêm cột note (mặc định HIỆN, không vào defaultUncheckedColumns) + **QuotationPrintPreview: bổ sung định nghĩa cột note trong `filteredColumns.allCols` (thiếu → cột bị lọc mất dù config chọn)** + render note (parent/child/service). Verify browser: print BG 66 (trực tiếp) + BG 78 (From-BOM) đều hiện cột Ghi chú vị trí 7, render đúng note thực từng SP, 0 lỗi console.

### Checkpoint — 2026-07-18 (E4b/E5/E6 xong + test hết browser)
Vừa hoàn thành: E4b (subagent) + fix E6 gap `QuotationPrintPreview.filteredColumns.allCols` thiếu note → thêm `{ key: 'note', label: 'Ghi chú' }` sau specification. E2E browser toàn bộ nhóm Ghi chú: E4b BOM 25 PASS, E6 print BG66 direct PASS, E5+E6 print BG78 From-BOM PASS (note từ BOM #8 chảy ra bản in). Dọn data: BOM 36 created_by=78.
Bước tiếp theo: Toàn bộ E1-E6 DONE + verified browser. Chờ user review/merge.

## E7 — Gộp dropdown Export còn 1 nút "Xuất Excel" (2026-07-18, user yêu cầu)
- [x] E7 (FE `_id/index.vue`): Bỏ `<b-dropdown>` 3 mục (Xuất Excel/Export báo giá trống/Export báo giá hiện tại) → 1 nút "Xuất Excel" gọi thẳng `/export-quotation-data` (user chọn: bản round-trip theo cột GG, KHÔNG phải /export-excel). BE `forData()` tự lấy `$quotation->discount_method` → bộ cột động 22/25/24 (Không GG/GG Mặt hàng/GG Tổng). Gỡ 3 method thừa `handleExportBlankTemplate`/`handleExportQuotationData`/`downloadExportFile`; wire `exporting` vào handleExportExcel; tên file `{code}_{DD-MM-YYYY}.xlsx`.
  - **Phát hiện bug SẴN CÓ (chưa fix)**: `/export-excel` (bản gửi khách, `BomListExport`→`bom_list.blade.php`) crash HTTP 400 `Undefined property: stdClass::$show_children` với **báo giá trực tiếp** (virtualProducts stdClass không set show_children); From-BOM 200 OK. User chọn dùng `/export-quotation-data` nên né được bug — nhưng /export-excel vẫn hỏng cho direct nếu còn nơi khác gọi.
  - Verify browser: BG66 direct (Không GG) + BG2 (GG Mặt hàng, method 1) + BG78 From-BOM đều 200 binary; UI chỉ còn 1 nút "Xuất Excel", dropdown biến mất; tải `BG-2026-00066_18-07-2026.xlsx`; productColumns 22/25/24 xác nhận qua reflection; 0 lỗi console. Print (E6) đã truyền `:discountMethod` sẵn (dòng 736).

### Checkpoint — 2026-07-18 (E7 gộp nút Export)
Vừa hoàn thành: E7 — 1 nút "Xuất Excel" → /export-quotation-data (cột theo GG), gỡ dropdown + 3 method. Verify browser 3 loại GG PASS.
Blocked: (none). Lưu ý tồn: bug /export-excel show_children cho báo giá trực tiếp CHƯA fix (user chưa yêu cầu) — nếu sau này cần bản gửi khách thì phải fix blade.
Bước tiếp theo: Chờ user review/merge toàn bộ E1-E7.

## E8 — Đồng nhất nút "Xuất Excel" màn Sửa với màn Xem (2026-07-18, user phát hiện)
- [x] E8 (FE `_id/edit.vue` `exportExcel()` ~3990): Đổi `/export-excel` (BomListExport gửi khách — crash `show_children` với báo giá trực tiếp, tải ngầm bản sai) → `/export-quotation-data` (QuotationExcelExport::forData, cột động theo GG). Tên file `{code}_{DD-MM-YYYY}.xlsx` (native Date, không thêm import dayjs); giữ `$nuxt.$loading` báo hiệu; revokeObjectURL.
  - Verify browser: BG66 trực tiếp (trước 400) → nay 200 tải `BG-2026-00066_18-07-2026.xlsx`; BG78 từ BOM → 200 tải `BG-2026-00067_18-07-2026.xlsx`. 0 lỗi console. Đồng nhất với nút màn Xem (E7).
  - Import template theo GG (E1/E2) verify lại file thật BG2 (method 1): `/export-blank-template?discount_method=1` → 200, file 25 cột đúng cụm GG Mặt hàng (GG(%),GG(đ),Đơn giá sau GG), có Ghi chú, không có Phân bổ GG.
  - Bug `/export-excel` show_children (báo giá trực tiếp) VẪN chưa fix — nhưng giờ KHÔNG còn nút nào (Xem/Sửa) gọi tới nó. Chỉ cần fix nếu sau này khôi phục bản gửi khách.

### Checkpoint — 2026-07-18 (E8 đồng nhất export màn Sửa)
Vừa hoàn thành: E8 — nút Xuất Excel màn Sửa trỏ /export-quotation-data giống màn Xem. Test BG66 direct + BG78 from-BOM đều 200. Import template theo GG verify file thật (25 cột method 1).
Bước tiếp theo: Chờ user review/merge E1-E8.

## E9 — Sắp lại layout form Thông tin chung (2026-07-18, user yêu cầu)
- [x] E9 (FE `_id/edit.vue` bảng Thông tin chung): MST bỏ colspan=3 → 1 ô (ghép cặp Email khách hàng) để cột phải tịnh tiến lên 1 hàng; Bảng giá bỏ dòng riêng colspan=3 → đặt ô phải ngay dưới Loại tiền tệ. Cặp hàng mới: MST|Email · Địa chỉ|SĐT · Người liên hệ|Giao hàng · Hiệu lực|Loại tiền tệ · Bảo hành|Bảng giá. Verify browser BG66: đúng vị trí, 0 lỗi console.

## Fix mẫu import/export theo GG (2026-07-20, user: file GG đang sai)
- [x] So mẫu chuẩn task 10790 (Google Sheet 3 tab KGG/GG mặt hàng/GG tổng) với `QuotationExcelExport::productColumns`. Sai: thừa 2 cột **Hình ảnh + Thời gian bảo hành** (ra 24/27/26). Fix: bỏ 2 cột khỏi $suffix → **22/25/24** đúng mẫu (đúng doc comment sẵn có); drawings()/style có isset guard nên tự tắt an toàn. Verify file thật forBlank(0/1/2) = 22/25/24, không Hình ảnh/Bảo hành, không lỗi.
- [x] User quyết: DỪNG ở cấu trúc. GIỮ header hiện tại ('Nhóm hàng cha (Cấp 1)', không dấu *). KHÔNG đổi text header (thêm */bỏ Cấp) vì header là key nội bộ dùng khắp BE export + BE import service + FE parseFile → rủi ro vỡ import cho phần trang trí. Thứ tự 3 tab thống nhất (KGG order trong mẫu coi như nhầm).
- [x] Fix khối GG tổng theo GG: mẫu chuẩn CHỈ tab GG Tổng mới có "KHU VỰC CẤU HÌNH GIẢM GIÁ TỔNG"; Không GG + GG Mặt hàng KHÔNG có (header hàng hoá ở dòng 1). Trước đây layout() luôn dành khối này (discountCount=5 kể cả Không GG). Fix: layout() chỉ dựng khối khi discount_method===TỔNG (else productHeaderRow=1, productDataStart=2, discountRows=[]); blade @if($hasDiscountBlock) bọc khối GG tổng + tiêu đề khối 2. Verify file: Không GG/GG mặt hàng header dòng 1 không khối GG; GG tổng có khối. Round-trip browser Không GG: import lại 5 SP + 0 GG, không lỗi.

## Tải file mẫu import tĩnh + bỏ dòng note (2026-07-20, user yêu cầu)
- [x] Tải file mẫu import báo giá = **file TĨNH theo Loại GG** (như /assign/application), KHÔNG gọi BE. Copy 3 file user cấp vào `hrm-client/static/` (import_baogia_khong_gg / _gg_mat_hang / _gg_tong .xlsx). `handleDownloadTemplate` chọn file theo discountMethod → tải `/<file>.xlsx`.
- [x] Import bỏ dòng NOTE + map header decorated: file mẫu 10790 có header 'Loại (*)','STT*','Nhóm hàng cha'... khác key BE. Thêm `canonHeader` (bỏ '(*)'/'*' cuối + 'Nhóm hàng cha/con'→'... (Cấp 1)/(Cấp 2)') áp ở buildColMap + detection; `isTemplateNote` bỏ 2 dòng hướng dẫn dưới header ('Bắt buộc','Chọn 1 giá trị...','(...')  ở cả vòng discount + product. BE/buildRawRows GIỮ NGUYÊN (nhận key canonical).
- [x] Verify browser: tải 3 file static status 200; upload 3 file → parse đúng (Không GG 0 GG, GG tổng 5 GG), noteLeak=0, header decorated map chuẩn (loai/name/qty đọc đúng), 0 lỗi.
- [x] Fix STT file mẫu: STT "1.1"/"1.2" bị Excel tự đổi thành NGÀY (datetime format d.m) → XLSX.js đọc ra ngày. Sửa 3 file: value ngày → "day.month" text + ép cột STT format text ('@') để user gõ "1.1" sau này không bị đổi ngày. Verify parse 3 file: STT = 1/1.1/1.2/2/3 đúng. Cột số (Đơn giá, VAT) trong data mẫu là text nhưng format General → user gõ số thật vẫn OK; data mẫu dùng master data giả nên vốn để minh hoạ (user xoá nhập thật).
- [x] Header lưới preview import báo giá hiện dấu `*` đỏ đúng cột bắt buộc khớp file mẫu (Loại/STT/Mã hàng/Tên hàng/Thương hiệu/Xuất xứ/ĐVT/Số lượng) — thêm `required:true` vào columns() + render `<span *>` khi col.required. Verify browser: 8 cột có *, còn lại không. Validate bắt buộc đã có ở BE.

## Fix kéo-thả nhóm sang khác cấp (2026-07-20, user báo bug)
- [x] BomBuilderTableCard.vue `groupSortable`: `onMove:()=>true` cho thả nhóm sang khác cấp/khác cha (UI hiện chỉ báo cho thả) nhưng onEnd + reorderGroups chỉ đổi sort_order cùng parent → save rollback, hiểu lầm có hỗ trợ. Fix: onMove chỉ cho khi related header CÙNG cấp CÙNG cha (khác → false + hiện no-drop); dead-zone (tbody sản phẩm) cho đi qua tự do tránh ghim header. Thêm class body `bom-group-drop-forbidden` (cursor no-drop) toggle trong onMove, clear ở onEnd + destroySortables. Thêm 1 `<style>` KHÔNG scoped target body.
- [x] Màn BÁO GIÁ (`quotations/_id/edit.vue`, `create.vue` reuse) có code kéo-thả RIÊNG `initQuotationSortables()` (KHÔNG dùng chung BomBuilderTableCard) → cũng còn `onMove:()=>true` ở group `q-group-head-tbody`. Fix y hệt: onMove cùng cấp cùng cha (class `q-group-drop-forbidden` + no-drop), clear onEnd + destroyQuotationSortables, thêm `<style>` không scoped. → 2 file: BomBuilderTableCard.vue (BOM) + quotations/_id/edit.vue (Báo giá).
