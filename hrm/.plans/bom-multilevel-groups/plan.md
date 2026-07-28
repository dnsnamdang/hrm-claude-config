# Plan: Nhóm hàng 2 cấp + kéo-thả cho BOM

> Design tóm tắt: `.plans/bom-multilevel-groups/design.md`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-bom-multilevel-groups-design.md`

## Trạng thái
- Bắt đầu: 2026-07-17
- Phụ trách: @manhcuong
- Tiến độ: 18/18 task ✅ CODE DONE + E2E 4 AC PASS + REVIEW TỔNG = READY (0 finding chặn merge; 4 Minor chấp nhận sau merge)
- Code pushed: ❌ (chưa commit — CLAUDE.md cấm tự commit)

## Ràng buộc chung (mọi task)
- BE **PHP 7.4** — lint `/opt/homebrew/opt/php@7.4/bin/php -l` (KHÔNG `php -l`, máy mặc định 8.1). Không cú pháp PHP 8.
- FE **Vue 2 / Node 14.21.3** — gọi đúng binary (node mặc định máy là 12.x). Không cú pháp Vue 3.
- KHÔNG commit git. KHÔNG viết file test (dự án không dùng PHPUnit). Verify: `php -l` + tinker data thật (bọc `DB::beginTransaction`/`rollBack` khi ghi) + Playwright UI.
- Đo query: `Event::listen(QueryExecuted)` đăng ký ĐÚNG 1 LẦN (theo connection sẽ đếm đúp).
- **CHỈ localhost:3000** khi test UI; KHÔNG đụng tab remote `dev-hrm.eteksofts.com`. BOM 1/2/3/8/25 là data user — tạo BOM test riêng, dọn sau.
- KHÔNG đụng `bom_list.blade.php` (Quotation dùng chung) · KHÔNG đụng Quotation · KHÔNG đụng `V2BaseImportModal`/`import-helper.js`.

---

## Phase 1: DB + Model

### BE — Schema ✅ (review clean 2026-07-17)
- [x] Task 1: Migration `2026_07_17_100000_add_parent_id_to_bom_list_groups.php` — `parent_id` unsignedBigInteger nullable, after `bom_list_id`, không FK, không transaction; đã migrate local, verify `parent_id | bigint unsigned | Null=YES`, 6 nhóm cũ đều NULL
- [x] Task 2: `DetailBomListResource` — groups trả thêm `parent_id`

## Phase 2: BE — syncGroups 2 cấp (luồng Tạo/Sửa) ✅ (review clean 2026-07-17)

- [x] Task 3: `syncGroups()` 2 pass — PASS 1 Cấp 1 (parent_client_id rỗng, parent_id null) trước; PASS 2 Cấp 2 resolve `parent_id` qua `clientToDbId[parent_client_id]` (không thấy → null, không throw); `sort_order` từ payload fallback index; groupMap giữ 3 key cho cả 2 cấp. Backward-compat: payload cũ → mọi nhóm Cấp 1 (verify). Chữ ký giữ nguyên.
- [x] Task 4: getCopyData **KHÔNG cần sửa** — `DetailBomListResource` (Task 2) đã trả groups có `id`+`parent_id`+`sort_order`; getCopyData chỉ strip id của `service_items`, không đụng groups → quan hệ cha-con bảo toàn qua copy.
  - **Minor → review tổng**: syncGroups không enforce depth=2 (giả lập 3 cấp tạo được chuỗi 3 tầng); FE kiểm soát payload nên không xảy ra thực tế, nhưng thiếu guard phòng thủ.

## Phase 3: BE — Import 14 cột ✅ (review clean 2026-07-17)

- [x] Task 5-7: `validateImportData()` 14 cột (Nhóm cha/con + Mã hàng cha, ĐVT bắt buộc, Mã trước Tên); STT rút gọn (bỏ cha-con/nhảy-bậc/2-cấp, **STT không bắt buộc**); luật `Nhóm hàng con phải có Nhóm hàng cha.`; helper `resolveImportParentLinks()` nối cha-con **nearest-above cùng nhóm lá** (mã KHÔNG duy nhất trong BOM). Row thêm `group_parent`/`group_child`/`parent_index`. Regression 3 nhánh Mã hàng/Master Data/dịch vụ/pending giữ nguyên. N+1 hằng số.
- [x] Task 8-9: `importProducts()` tạo nhóm 2 cấp (Cấp 1 trước, Cấp 2 sau) + gắn nhóm lá + nối `parent_id` qua `parent_index` (file index → db id, nhất quán cả khi skip_invalid). Bỏ hết parse STT. Replace-all giữ.
- [x] Task 10-11: `importTemplate()` 14 cột (tham chiếu thẳng `FLAT_HEADERS` — gỡ nợ header 3 nơi) + 3 dòng mẫu import được thật + sheet Hướng dẫn; export blade 14 cột, **dòng con LẶP nhóm cha/con + Mã hàng cha=mã cha** (bắt buộc để re-import nối được cha-con). Round-trip verify: import→export→re-import khôi phục đúng nhóm 2 cấp + cha-con.

## Phase 4: FE — cây nhóm + kéo-thả ✅ (review clean 2026-07-17)

- [x] Task 12: `BomBuilderEditor.vue` — `bomGroups` + `parent_client_id`; loadDetail map `parent_id`; `addGroup(parentClientId)`; saveGroupModal sort_order per-sibling; buildSavePayload gửi `parent_client_id` + `sort_order: g.sort_order`. Backward-compat nhóm phẳng cũ → Cấp 1.
- [x] Task 13-14: `BomBuilderTableCard.vue` — computed `groupTree` (Cấp 1 + children, node giữ `flatIndex`); render Cấp 1 số La Mã / Cấp 2 thụt lề I.1/I.2 / sản phẩm dưới nhóm lá; nút "Thêm nhóm con" trên Cấp 1 (emit add-group+client_id). Markup dòng sản phẩm giữ nguyên. Backward-compat.
- [x] Task 15: Kéo-thả nhóm — **SortableJS SẴN CÓ** (không vuedraggable), handle `.drag-group` tách khỏi `.drag-parent`; `groupSortable` onMove chặn kéo chéo cha/cấp, emit `reorder-groups {parentClientId, orderedClientIds}`; editor `reorderGroups` cập nhật sort_order cùng cha; **cascade** `confirmRemoveGroup` xoá Cấp 1 → xoá Cấp 2 con, sản phẩm thành orphan không biến mất. ⚠️ **Browser drag E2E hoãn Task 18** (Chrome profile khoá lúc code).
- [x] Task 16: `BomImportModal.vue` — 14 cột (14 label khớp `FLAT_HEADERS` qua normKey, kể cả `(Cấp 1)`); `applyGroupForwardFill` điền xuôi **cặp** group_parent+group_child.

## Phase 5: Verify E2E ✅

- [x] Task 17: Migration production-safe + regression Copy (Cấp 1 parent_id null / Cấp 2 parent_id = Cấp 1 id, verify trong transaction+rollback) + luồng Sửa BOM nhóm phẳng cũ → load thành Cấp 1.
- [x] QuotationImportModal: THÊM sửa inline (user yêu cầu) — ô lưới read-only `<span>` → `V2BaseInput` sửa được; dòng hợp lệ khoá cả dòng (isRowLocked status='valid') + ô master-data ERP khoá (isLocked). onCellEdit đồng bộ giá trị sửa về `parsedPayload.products[i][header Excel]` (map QIM_HEADER_BY_KEY, bỏ định dạng số vi-VN cho cột số), xoá status/errors dòng + `validated=false` → buộc Validate lại (handleValidate GIỮ NGUYÊN gửi parsedPayload nên tự nhận dữ liệu mới). Gỡ CSS qim-cell-locked. Verify browser: invalid 25/25 sửa được, valid 25/25 khoá, sửa qty→parsedPayload cập nhật=12 + validated=false + status cleared.
- [x] Port UI sang QuotationImportModal (Import báo giá): gỡ wizard steps + gộp toolbar/stats vào card sticky (giống V2Base) + gỡ checkbox "Bỏ qua dòng lỗi" disabled (báo giá import all-or-nothing) → thay bằng dòng note. Verify browser: hết steps, toolbar card, không checkbox. KHÔNG port: khoá-dòng/disable-input (preview quotation read-only, không có input), nút "Xoá trạng thái validate" (không có sửa inline), "#"-từ-1 (quotation dùng số dòng Excel để khớp message lỗi 422 "Dòng N"), required-* (cột quotation chưa mark, header dùng {{}} không v-html — chờ xác nhận trường bắt buộc).
- [x] Fix: cột "#" preview import bắt đầu từ 2 (parseExcelFile gán __row = số dòng Excel thật, header=1). File import-helper dùng chung/cấm sửa → đánh lại `__row = idx+1` (1-based) trong map handleLoadExcel. Ánh xạ BE dùng index mảng nên không ảnh hưởng.
- [x] UI: BomImportModal khoá DÒNG HỢP LỆ sau Validate (nguyên tắc V2BaseImportModal) — bỏ ô-khoá phức tạp (lock-div + icon + CSS `.bom-import-cell-locked`), thay bằng **input disabled** đơn giản. isRowLocked (status='valid') khoá cả dòng; ô master-data vẫn hiện dữ liệu chuẩn hệ thống (cellLockedValue lấy __resolved). Dòng lỗi/pending vẫn sửa được. Verify browser: valid 14/14 disabled (model hiện resolved), invalid 14/14 editable.
- [x] Fix regression: thêm `*` vào label Thương hiệu/Xuất xứ làm hỏng khớp header import (normKey không bỏ '*', header template không có '*', key/alias không dấu ≠ header có dấu) → "Cấu trúc file không hợp lệ". Fix: thêm alias CÓ DẤU 'Thương hiệu'/'Xuất xứ' cho brand/origin. Sim khớp 14/14 cột. (STT không lỗi vì key 'stt' khớp.)
- [x] UI+Validate BomImportModal: (1) "Bỏ qua dòng lỗi" checkbox → NÚT toggle (giữ cờ skip_invalid + cascade BE, KHÔNG xoá dòng FE) + thêm nút "Xoá trạng thái validate" (handleClearValidation, reset validated không xoá dòng) — hàng nút dưới bảng giống V2BaseImportTable. (2) Model KHÔNG bắt buộc (bỏ khỏi validateNewTempMasterDataRequired BE); Thương hiệu/Xuất xứ/STT bắt buộc → thêm `*` đỏ header preview (đã có Loại/Mã hàng/Tên hàng/ĐVT/Số lượng). Verify browser: header * đúng (Model không *), footer hết checkbox, 2 nút hiện, clear-validate reset giữ đủ dòng.
- [x] UI: BomImportModal đồng bộ V2BaseImportModal (giữ kích thước compact) — gỡ khối wizard `bom-import-steps` (+ CSS + mảng `steps`); gộp toolbar + thống kê vào 1 card sticky bo góc/shadow, nhóm dashed nền trắng, stats full-width trong card (giống `.modal-toolbar`). Verify browser: hết steps, toolbar card sticky radius 0.95rem + shadow, 3 nhóm. Không đụng logic import (per-cell readonly, pending, bỏ qua lỗi giữ nguyên).
- [x] Fix: validate STT khi import BOM theo spec 2.4 (giữ Mã hàng cha nối cha-con). Bổ sung `validateSttStructure`: (1) STT bắt buộc, (2) format số+chấm + không trùng [đã có], (3) cha-con — dòng con STT phải có STT cha ở phía trên, (4) tịnh tiến — không nhảy bậc (thiếu 1.2 mà có 1.3 → lỗi). Thêm cross-check STT↔Mã hàng cha. Lý do: STT nhảy bậc/rỗng đang pass validate (lệch spec doc mục 2.4). Model/Master Data đã đúng spec (không sửa).
- [x] Fix: ẩn ô "Mã BOM" ở màn Tạo mới (BomBuilderInfoCard) khi `bomForm.code` rỗng — mã do BE tự sinh lúc Lưu, chỉ hiện khi đã có mã (sau lưu/xem/sửa). Thêm `v-if="bomForm.code"`.
- [x] Fix: định dạng cột file Xuất Excel BOM (flat 14 cột) — wrap TOÀN BỘ A..N (trước chỉ G,M) + nới Nhóm cha/con (18→22), Ghi chú (22→32), Tên hàng/TSKT; header bold + auto row height. Không còn cột nào bị cắt chữ khi mở lần đầu.
- [x] Fix: tên file Xuất Excel BOM bỏ prefix thừa `BOM_` (mã đã có `BOM-`) → `BOM-2026-000xx.xlsx`. Sửa FE `_id/edit.vue`, `_id/index.vue` + BE `BomListController::export` cho nhất quán.
- [x] Testcase: `.plans/bom-multilevel-groups/testcase.xlsx` — 36 TC (8 section, P0=50%) cho Import/Export/Sao chép BOM + cột Ghi chú (AC1-4 + Lưu ý), góc nhìn người dùng cuối, không freeze.
- [x] Task 18: E2E Playwright 4 AC trên BOM test 39 (đã dọn). AC1 tạo nhóm con render "I.1" thụt lề PASS; AC2 Xuất Excel qua UI tải `BOM_BOM-2026-00037.xlsx` 14 cột + phân cấp + dòng con lặp nhóm cha/con + Mã hàng cha PASS; AC3 import file 2 cấp tạo đúng cây + nối cha-con PASS; AC4 kéo nhóm đổi thứ tự → UI cập nhật ngay + Lưu → reload giữ thứ tự PASS.
  - **Fix Task 15 (nợ browser E2E)**: `onMove` gốc trả `false` khi header bị kéo qua tbody sản phẩm/header khác cấp (xen kẽ trong cùng `<table>`) → ghim phần tử, SortableJS không reorder được. Sửa `onMove: () => true` (cho đi qua tự do); tính đúng đắn giữ nguyên ở `onEnd` (chỉ đọc header cùng cấp cùng cha) + groupTree re-render (nắn lại cấu trúc 2 cấp theo sort_order). Verify kéo Cơ khí→vị trí 1, Lưu, reload: Cơ khí=0/Dây chuyền sơn=1, nhóm con Cấp 2 đi theo cha xuống II.1/II.2.

### Minor tích luỹ → review tổng cuối triage
- syncGroups không enforce depth=2 (FE kiểm soát payload); recompute type trong `resolveImportParentLinks` (0 query); `'||'` leaf-key không escape (tên nhóm không chứa `||`); sub-BOM merge `mergedBomGroups` phẳng về Cấp 1 (aggregate BOM, ngoài scope); double watcher init SortableJS (vô hại).

---

## Verify (sau khi code)
- [x] Lint BE 7.4 sạch + compile FE Node 14.21.3 sạch
- [x] AC1 — tạo nhóm con dưới nhóm đã có, UI hiện đúng 2 cấp (render "I.1" thụt lề)
- [x] AC2 — Export qua UI → đọc lại file: 14 cột đúng FLAT_HEADERS, Nhóm cha/con điền đúng theo phân cấp, dòng con lặp nhóm + Mã hàng cha; round-trip BE verify import lại 0 lỗi
- [x] AC3 — Import file có nhóm cha-con → thành công, lưới hiện đúng phân cấp, hàng con nối đúng Mã hàng cha
- [x] AC4 — kéo nhóm đổi vị trí UI đổi ngay; Lưu → reload giữ thứ tự (nhóm con Cấp 2 đi theo cha)
- [x] Regression: Copy giữ nhóm 2 cấp (verify transaction+rollback); nhóm phẳng cũ vẫn load (thành Cấp 1)
- [ ] Regression còn lại → **review tổng cuối**: 3 nhánh Mã hàng/dịch vụ/pending/Master Data không vỡ; query import validate hằng số; đường ghi không N+1

---

## Checkpoint

### Checkpoint — 2026-07-17
Vừa hoàn thành: Brainstorming (6 quyết định) + spec đầy đủ + design tóm tắt + plan 18 task/5 phase.
Đang làm dở: Chưa code.
Bước tiếp theo: chọn cách thực thi (subagent-driven / inline) → Task 1 migration.
Blocked: (không có)

### Checkpoint — 2026-07-17 (E2E xong)
Vừa hoàn thành: Toàn bộ 18 task. Fix cuối AC4 kéo-thả nhóm — `BomBuilderTableCard.vue` `onMove: () => true` (onMove gốc ghim header khi đi qua tbody sản phẩm/header khác cấp). E2E 4 AC PASS trên BOM test 39. Dọn BOM 39 + file test.
Đang làm dở: (không) — chờ review tổng cuối whole-branch.
Bước tiếp theo: Review tổng cuối triage các Minor tích luỹ (syncGroups depth=2, sub-BOM merge phẳng, `'||'` leaf-key, double watcher init) + regression 3 nhánh Mã hàng/dịch vụ/pending/Master Data + đo query.
Blocked: (không có)

- [x] Fix bug: Import BOM báo "Tên hàng là bắt buộc" cho hàng ERP (Mã khớp ERP) dù tên tự điền từ hệ thống. Nguyên nhân: validateImportData check tên trên FILE (rỗng với hàng ERP) TRƯỚC classify. Fix (BomListService:~584): chỉ bắt buộc Tên hàng khi KHÔNG lấy được tên từ hệ thống — hàng hoá có Mã khớp ERP/hàng-tạm-cũ (lookupErp/lookupTemp) thì bỏ qua; giữ bắt buộc cho dịch vụ + hàng tạm mới. Verify tinker mã ERP thật 2Q-GIADEPHUTUNG: ERP+tên rỗng→valid; tạm mới+tên rỗng→lỗi.

- [x] Feature: Import BOM tự tạo Master Data (Model/Thương hiệu/Xuất xứ) khi giá trị chưa có trong danh mục. Validate → cảnh báo dòng vàng "Hợp lệ (tạo mới)" (không chặn, Import vẫn active); Import → tự insert master data (mysql2) + map id vào dòng BOM. ĐVT KHÔNG auto-create (vẫn lỗi đỏ). BE (`BomListService`): classify sinh `warnings`+`*_new_name`; `importProducts` gọi `autoCreateResolvedMasterData` trước map; helper `resolveOrCreateMasterId` (dedup LOWER(TRIM), lọc cột theo Schema) + `generateBrandCode`. FE (`BomImportModal`): `__warnings`, `hasWarn`, trạng thái vàng, dòng note cảnh báo. E2E PASS 4 AC trên BOM test 41: AC1 dòng vàng/Import active, AC2 import OK, AC3 master data tạo (Model/Brand+code/Origin), AC4 product link đúng id; dedup lần 2 cùng id (không trùng). Dọn BOM 41 + master test.
