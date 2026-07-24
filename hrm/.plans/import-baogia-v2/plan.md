# Plan — Import báo giá v2

> Design: `.plans/import-baogia-v2/design.md` · Spec: `docs/superpowers/specs/2026-07-23-import-baogia-v2-design.md`
> Trạng thái: **Đang lập plan / chờ rà chi tiết từng cột** (chưa code)

## Phase 1 — Cột ẩn định danh (nền tảng)
### BE
- [x] Export ghi 3 cột ẩn: Line ID (id dòng), ID Báo Giá nguồn, BOMList ID nguồn vào `QuotationExcelExport` — thêm 3 const HEADER_*, append cuối productColumns, helper lineIdOf (đọc `_id`), renderRow ghi 3 cell, AfterSheet setVisible(false); verify q66: Line ID=qpp.id thật, cột ẩn, công thức letter không đổi
- [x] Import parse đọc 3 cột ẩn: thêm const COL_LINE_ID/COL_SRC_QUOTATION_ID/COL_SRC_BOMLIST_ID (khớp export), helper readImportSourceMeta đọc file-level src meta, KHÔNG đưa vào READ_PRODUCT_COLUMNS (tự loại khỏi detect dòng trống). Validate "ID không tồn tại DB→lỗi" = Phase 2 (cần routing). Verify: constants khớp export, readImportSourceMeta đúng
### FE
- [x] Import modal đọc cột ẩn — KHÔNG cần sửa: buildColMap map MỌI header → 3 cột ẩn tự vào parsedPayload (key khớp BE); XLSX.js đọc cả cột ẩn; onCellEdit sync theo header không rớt ID
### Template
- [ ] (tùy) 3 file static thêm cột ẩn — HOÃN (thiếu ID = all-insert, đúng cho file trống)

## Phase 2 — Phân luồng import + popup chọn phương thức
### BE
- [x] Pre-check: đọc ID Báo Giá ẩn → `importIsUpdate` (Update nếu = BG đích); chặn cứng BOM cross-import khác bom_list_id. TEST: khác BOM→chặn ✓, cùng BOM→không chặn ✓, Update→không chặn ✓
- [x] Direct branch mang `price_id` (Line ID) khi Update; null khi cross-import; validate "ID không thuộc BG → lỗi". TEST round-trip q66: 41 dòng, 0 lỗi, price_id khớp qpp DB; cross-import(ID 99999)→price_id=0 hết ✓
- [x] BOM branch: update theo `bom_list_product_id` (đã ổn sẵn, không cần price_id). Service: chỉ reuse id cũ khi Update; cross-import → id null (tránh reuse nhầm BG đích). Lint OK
- [x] Save: FE gộp lưới (Phase 3 clarify) — BE upsert giữ nguyên
### FE (subagent Opus implement, compile-check PASS Node 14; E2E browser account 48)
- [x] Popup chọn phương thức: độc lập (từng phần / thay thế) — BOM mặc định từng phần. **E2E q66: popup hiện đúng 2 lựa chọn** ✓
- [x] Popup cross-import (cảnh báo + chọn) khi ID Báo Giá file ≠ quotationId
- [x] applyImportDirect: GỘP lưới theo price_id (partial) / replace. **E2E q66 round-trip: import từng phần → 41 SP gộp giữ nguyên, tổng đúng** ✓
- [x] **FIX BUG (2026-07-23, user báo)**: partial import append nhóm TRÙNG RỖNG (III/III.1/IV/IV.1 = bản sao I/I.1/II/II.1) vì append MỌI nhóm preview kể cả nhóm của dòng đã khớp. Sửa `applyImportDirectPartial`: chỉ append nhóm mà dòng MỚI (chưa khớp) tham chiếu (kèm nhóm cha, hàm markGroupChain). Round-trip → newRows rỗng → không append. E2E q116: sau fix chỉ còn 4 nhóm gốc, hết III/IV rỗng ✓
- [x] Bỏ confirm "xóa & thay thế toàn bộ" cứng; subtitle/footer đổi thành "chọn phương thức"
- [x] **Làm đẹp UI popup** (2026-07-23): đổi từ b-form-radio phẳng → card chọn (icon bo tròn + title/mô tả + highlight active + check góc phải), content-class `qim-method-content`. Partial=xanh, Replace=đỏ (danger). Compile-check PASS + E2E browser xác nhận 2 state đẹp
- [x] E2E TOÀN BỘ (11 luồng): Update, popup độc lập 2 lựa chọn, partial merge, cross-import (popup+clone), BOM popup (partial only), BOM partial import, phân quyền, popup lỗi Phase 6, thay-thế-hoàn-toàn, copy (V2 tạo + skip popup khi rỗng), file trống (no-ID → popup thường). BOM-block-khác-cấu-trúc: tinker ✓

## 🐛 Bug phát hiện khi E2E (pre-existing, cần fix)
- [ ] **Export dịch vụ ghi "Có tính doanh thu" RỖNG** khi cost_id null / cost thiếu revenue_calculation → re-import lỗi "Có tính doanh thu không tồn tại". `quotation_service_items` KHÔNG có cột revenue_calculation (chỉ suy từ costs). Fix: export dịch vụ default "Không" hoặc lưu cờ; HOẶC import default null service revenue. (q91 gặp, q66 không vì 0 dịch vụ)

## Phase 3 — Mã hàng tạm → Hàng hóa dự án (báo giá độc lập) — subagent A, TEST OK
### BE
- [x] Rule 1 (best-effort): `resolveProjectGoodsByCode` query view union Hàng hóa dự án theo project_id → `applyProjectGoodsMapping` map data giữ mã
- [x] Rule 2: giữ nguyên (save sinh HHBG+id — đã có)
- [x] Rule 3 (làm chắc): `assertDuplicateTempCodes` + `tempIdentitySignature` (6 định danh + giá nhập/bán + VAT). TEST: lệch→chặn ✓, giống→không chặn ✓
- [x] **VỨT mã nhập + gom chung 1 mã (chốt 2026-07-23, user)**: `saveDirectProduct` vứt mã user nhập (chỉ là nhãn), tự sinh HHBG; dòng cùng nhãn dùng chung 1 mã qua `$gomMap` (upsertDirectProducts truyền qua 2 pass). TEST DB: 2 dòng SP-DUP2 → cùng HHBG002222, vứt SP-DUP2 ✓. Update giữ mã cũ; mã trống → HHBG riêng

## Phase 4 — Báo giá kế thừa BOM (partial import) — subagent A, TEST OK
### BE
- [x] Bỏ lỗi "thiếu mã BOM" (dòng vắng giữ nguyên — chỉ còn comment). TEST round-trip q78 0 lỗi ✓
- [x] Khóa Model + ĐVT (thêm assertMatchesBom, resolve id→tên; round-trip an toàn); Tên/TSKT đã có
- [x] Dịch vụ nhánh BOM: ép SL=1
- [x] Chặn Hàng hóa mới + cho thêm Dịch vụ (đã có sẵn)

## Phase 5 — Sao chép báo giá (đã có sẵn phần lớn; verify)
### BE
- [x] copy-preview: 3 loại (price/vat/structure) đã có (L1052/1077/1097). 🔴 Ngừng KD HOÃN (ERP không có status — TODO L1108)
- [x] Đổi dự án → detach BOM (isProjectChange/TYPE_SELF_BUILT) + nạp KH mới; tỷ giá ERP; hiệu lực auto-calc — đã có
### FE
- [x] Popup review (`QuotationCopyPreviewModal.vue`) tồn tại; khóa Gửi duyệt Ngừng KD → HOÃN cùng 🔴
- [x] E2E UI copy preview: ép sửa giá/VAT SP q66 lệch ERP → Sao chép → popup "Phát hiện thay đổi dữ liệu từ ERP" hiện đúng grid 5 cột: 🟡 Thay đổi giá (99999→119tr), 🟡 Thay đổi VAT (3→8), nút "Xác nhận Sao chép"/"Hủy bỏ". Hủy không tạo V2, đã khôi phục data ✓

## Phase 6 — Popup lỗi import — subagent B, compile-check PASS (cần E2E UI)
### FE
- [x] Grid lỗi cuộn 3 cột (Dòng Excel/Cột sai/Mô tả) + 3 nút: Sao chép lỗi (TSV clipboard) / Tải File lỗi (CSV client-side) / Đóng + link "Xem chi tiết N lỗi". Giữ song song inline. Compile-check PASS Node 14
### BE
- [x] Không cần endpoint (tải file lỗi client-side)

## Bug dịch vụ round-trip — subagent C, TEST OK
- [x] Export dịch vụ `_revenue_calculation` null → default "Không" (chỉ dòng dịch vụ). TEST q91 round-trip: svc="Không", 0 lỗi ✓

## Phase 7 — Export + file mẫu
### BE
- [x] Tên file export `[Mã_BG]_[DDMMYYYY]` (đổi date('d-m-Y')→date('dmY')), lint OK
- [ ] (tùy) Tên sheet file mẫu `import_10790_*` + `huong_dan_10790` — file mẫu FE tải static; chỉ đổi nếu bắt buộc
### FE
- [x] Nút "Xuất file trắng": FE đã chỉ có 1 nút "Xuất Excel" (export-quotation-data) — đạt sẵn. (Route BE export-blank-template còn nhưng không nút gọi → vô hại)

## Phase 8 — Dịch vụ giá vốn (trigger lúc lưu)
### BE
- [ ] Dịch vụ chưa có % giá vốn: khi Lưu tính `%=giá nhập/giá bán` cập nhật ngược Master Data ERP

## Phase 10 — Mirror gom mã hàng tạm sang BOM-list (user chốt 2026-07-23: "mirror y hệt báo giá")
> Chỉ mirror 1 nhóm: "1 hàng tạm → nhiều dòng chung 1 mã HHB" (nút Nhân bản + gom). Import v2 / vứt-mã-nhập / copy-popup / che-giá KHÔNG áp cho BOM (khác luồng / BOM không quản lý giá).
### BE — BomListService::syncProducts (lint OK, tinker PASS)
- [x] Thêm `$gomMap` + 2 helper `applyGomToPayload`/`seedGom`: hàng tạm cùng nhãn `gom_key` dùng CHUNG mã HHB (fresh: dòng đầu sinh HHB→seed→dòng sau tái dùng; có mã sẵn: giữ+seed). Dòng không gom_key → HHB riêng. Áp cho cả parent lẫn child. TINKER PASS 4/4: A1==A2, solo riêng, B1 giữ HHB000999, B2 tái dùng.
- [x] Reconcile dedupe (xem FE): gom chỉ khi có `gom_key` chủ ý; dedupe merge sub-BOM giữ nguyên.
### FE — BomBuilderEditor.vue + BomBuilderTableCard.vue (compile-check Node 14 PASS)
- [x] Nút "Nhân bản" (icon ri-file-copy) trên dòng hàng tạm không-ERP, không con — cả 2 layout table card (grouped + ungrouped); emit `duplicate-parent`
- [x] `nhanBanTempGood(parent)`: gán `_gom` nếu chưa có, clone thành group mới (rowId mới, dbId null, code+_gom giữ), splice sau group gốc, cùng group_id
- [x] `mapGroupRowForSave`: map `gom_key: row._gom || null`
- [x] `dedupeTempGoodsCodes` bỏ qua dòng có `_gom` (không strip mã nhân bản chủ ý)
- [x] **E2E UI PASS (2026-07-23, acct 48/BOM 40)**: nút Nhân bản chỉ hiện đúng 1 dòng hàng tạm HHB001728 (không ERP/con) → bấm → 2 dòng "hàng hoá test" chung mã; đổi SL clone=7 → Lưu → DB 2 dòng (id mới 1741/1742 = recreate), **chung mã HHB001728**, SL 1&7 độc lập. BOM 40 khôi phục nguyên trạng (snapshot→restore, created_by=13).

## Phase 11 — Chọn lại hàng tạm dự án trên popup + import reuse theo mã (user chốt 2026-07-23)
> Scope: CẢ báo giá + BOM. Select chỉ HÀNG TẠM (view Hàng hóa dự án đã duyệt) + hàng tạm phiên. Chọn → dùng CHUNG mã, disable ô khác. Reuse = dòng mới RIÊNG chỉ trùng mã (như gom/Nhân bản), không FK tham chiếu.
### BE — data source + Rule 1 authoritative (lint OK, tinker PASS)
- [x] `ProductProjectController`: param `only_temp=1` cho index (whereNull erp_product_id) + bổ sung `*_id`+`vat_percent` vào transformItem/transformQuotationItem. Reuse endpoint `GET /assign/product-projects` (không cần route mới). Tinker: trả đúng hàng tạm + *_id
- [x] Rule 1 báo giá `saveDirectProduct`: property `$projectGoodCodes` + `collectProjectTempGoodCodes` (union bom duyệt + qtn duyệt theo project, whereNull erp) → mã trùng GIỮ, không sinh HHBG. TINKER PASS: TAM-TEST-001 giữ, mã lạ→HHBG002267
- [x] BOM `syncProducts`: vốn giữ mọi mã non-empty → reuse popup giữ mã sẵn (E2E xác nhận). Import BOM resolve master-data theo mã: **CHƯA làm** (BOM giữ code từ file, chưa remap data project-good — xem "còn lại")
- [x] Báo giá import: `resolveProjectGoodsByCode` (validate map data) + saveDirectProduct nay giữ mã → import reuse chạy (BE tinker chứng minh keep)
### FE — popup thêm hàng tạm (báo giá + BOM). LƯU Ý: popup thật = `QuotationProductSearchModal` (dùng chung), KHÔNG phải BomBuilderAddProductModal (code chết)
- [x] `QuotationProductSearchModal.vue` (BOM, gate `enableReuse`) + `QuotationProductEditModal.vue` (báo giá sửa): `V2BaseSelectInModal` "Dùng lại hàng tạm dự án" đầu form; options = API `only_temp` theo dự án (nhãn "(dự án)") + hàng tạm phiên (nhãn "(trong phiếu)")
- [x] Chọn 1 mục → fill toàn bộ + disable mọi ô + nút "Bỏ chọn"; validation bỏ qua brand/origin khi reuseLocked (hàng tạm cũ có thể thiếu master data); mục phiên chưa mã → `reuse_gom_source` → cha link `_gom`
- [x] Parent: `BomBuilderEditor` (enable-reuse + project-id + sessionTempGoods computed + handleAddProductApply link _gom); `quotations/_id/edit.vue` (ADD popup enable-reuse + directSessionTempGoods + onAddProductApply link _gom; EDIT modal cũng nối)
- [x] **FIX**: `loadReuseOptions` đọc sai `res.data.data` → sửa `res.data` (mảng paginated) — nhóm 1 mới hiện. **FIX**: reuseLocked bỏ qua validate brand/origin
- [x] Compile-check Node 14 PASS (4 file). **E2E UI BOM PASS**: picker liệt kê 4 (dự án)+2 (trong phiếu); chọn TAM-TEST-002 → fill+disable+Bỏ chọn; Lưu→lưới; Lưu BOM→DB dòng mới id=1746 GIỮ mã TAM-TEST-002 (không HHB mới). BOM 40 khôi phục.
- [x] **E2E UI báo giá PASS** (BG-66 tạm repoint project 5, acct 48): picker hiện 4 "(dự án)"; chọn TAM-TEST-002 → fill name + code + unit + disable 3 ô + Bỏ chọn. Không lưu phá dữ liệu (save-keep đã tinker PASS TAM-TEST-001). BG-66 khôi phục project 32, 41 SP nguyên.
- [x] **REWORK 2026-07-23 (user gửi spec chính thức): popup "Thêm hàng tạm" phải là 2 TAB, KHÔNG phải dropdown**. Đổi `QuotationProductSearchModal` overlay → `b-tabs`: Tab 1 "Chọn từ kho hàng tạm (Tái sử dụng)" = **bảng multi-select** (search + checkbox chọn nhiều + nút "Thêm N hàng hóa"), cột Mã/Tên/Model/TH/XX/ĐVT/Nguồn (Dự án|Trong phiếu); Tab 2 "Thêm mới thủ công" = form cũ (bỏ dropdown/reuseLocked). Gỡ reuse khỏi `QuotationProductEditModal` (modal Sửa = form thuần). Nguồn Tab 1 giữ đúng spec: hàng tạm dự án hiện tại + hàng tạm trong phiếu (KHÔNG nới ERP/dự án khác). Compile PASS 3 file. **E2E PASS cả BOM + báo giá**: AC1 (2 tab), AC2 (search TAM→3, tích 2 → "Thêm 2 hàng hóa" → vào lưới), AC3 (Tab 2 điền form → Lưu → HHB mới). Lưu BOM 40: 6 dòng, reused giữ mã TAM-TEST-001/HH000001, manual HHB001755. Khôi phục sạch.
- [x] **BOM import remap — ĐÃ CÓ SẴN**: `classifyImportRow` nhánh `product_project` (mã trùng hàng tạm dự án) map full master-data (name/model/TH/XX/ĐVT/TSKT) + giữ code + status `pending_confirm`. Reflection tinker PASS. Khác popup: match TOÀN CỤC theo mã (không lọc dự án) — behavior cũ, giữ nguyên.

## Phase 9 — Rà + vá validation table từng cột — subagent A, TEST OK
### BE
- [x] Giới hạn ký tự hàng tạm: Model/TH/XX ≤ 255, ĐVT ≤ 50 (`assertMasterLen`). TSKT giữ 65535 byte (user chốt). TEST Model>255→chặn ✓
- [x] GG(đ) ưu tiên / VAT ERP override / ĐVT bắt buộc khớp — đã có sẵn (rà xác nhận)

---

### Checkpoint — 2026-07-23 (2)
Vừa hoàn thành: chạy 4 subagent Opus rà đối chiếu code (Import/Export/Copy-Save/FE) + viết SPEC CHI TIẾT `docs/superpowers/specs/2026-07-23-import-baogia-v2-design.md` kèm bảng gap per-column chính xác.
Kết quả rà: (1) toàn bộ map theo Mã hàng, chưa có Line ID — thay đổi lớn nhất; (2) upsert hiện XÓA dòng vắng (ngược partial); (3) BOM dòng vắng báo lỗi (ngược); (4) mã hàng tạm chưa dedup Rule3, Rule1 đang tra ERP master thay vì view Hàng hóa dự án; (5) copy thiếu 🔴 Ngừng KD (ERP chưa có status); (6) canSeePrice hàng tạm còn phụ thuộc isCreator; (7) export thiếu cột ẩn ID + sai format tên file; (8) FE thiếu popup chọn phương thức + cross-import + popup lỗi 3 nút. Nhiều mục ĐÃ khớp (Có tính doanh thu, gate giá vốn import/export, copy header/tỷ giá/hiệu lực, service cost sync, nút export).
Đang làm dở: chờ user chốt 5 câu hỏi mở (mục 11 spec).
Bước tiếp theo: user duyệt spec + trả 5 câu hỏi mở → code từ Phase 1 (cột ẩn ID).
Blocked: câu hỏi mở #1 (nguồn ERP status Ngừng KD) có thể chặn Phase 5 phần 🔴.

### Checkpoint — 2026-07-23 (5): VERIFY SAVE→DB (đóng khoảng trống quan trọng)
Test Lưu→DB thật (browser + query DB): (1) Partial import q66 round-trip → Lưu → DB 41 dòng, **IDs giữ nguyên** (UPDATE in-place theo price_id, không delete+recreate), tổng khớp ✓. (2) Cross-import q66→V2(copy) → Sao chép từng phần → Lưu → V2 = 82 dòng (41 gốc giữ + 41 clone MỚI, 0 trùng id) ✓. V2 đã xóa. → Cơ chế price_id + clone chạy trọn tới DB. Còn (rủi ro thấp): BOM-block browser (tinker OK), copy-popup-render-changes (data-dependent, BE 3 loại OK), Rule 1 depth.

### Checkpoint — 2026-07-23 (4): CODE-COMPLETE + E2E TOÀN BỘ (trừ commit)
Vừa hoàn thành: TẤT CẢ 9 phase code xong + verify. 3 subagent Opus (BE Phase 3/4/9, FE Phase 6 popup lỗi, fix bug dịch vụ) — lint/compile PASS. BE tinker: round-trip 4 báo giá 0 lỗi, Rule 3 (lệch→chặn/giống→ok), Phase 9 (ký tự), Phase 4 (bỏ lỗi BOM), bug dịch vụ (svc="Không"). **E2E browser 11 luồng PASS** (account 48): Update/popup độc lập/partial/cross-import+clone/BOM popup+partial/phân quyền/popup lỗi Phase 6/thay-thế/copy V2/file-trống. Dữ liệu test khôi phục (q118 xóa, q91/q78 created_by→13).
Còn lại: 🔴 Ngừng KD HOÃN (ERP không status); static template thêm cột ẩn = TÙY (no-ID vẫn insert đúng); sheet naming file mẫu = tùy. **CHƯA COMMIT (user chỉ định trừ commit).**
Bước tiếp: user review → commit → deploy (BE 2 file + FE 2 file).

### Checkpoint — 2026-07-23 (3): PHASE 1 XONG + Phân quyền revert
Vừa hoàn thành:
- Phân quyền creator-based: REVERT import gateCost + export canSeeCostOf về `canViewCost || (!isErp && isCreator)` (lint + test 4 combo OK). View/sửa giữ nguyên.
- 5 câu hỏi mở đã chốt: (1) Ngừng KD HOÃN (ERP không có status); (2) creator-based; (3) import từng phần = FE gộp; (4) TSKT giữ 65535 byte; (5) VAT VC giữ 8%.
- **PHASE 1 (cột ẩn định danh) HOÀN THÀNH**: Export ghi 3 cột ẩn (Line ID=qpp.id thật/service bỏ svc-/shipping rỗng, ID Báo Giá, ID BOM) + ẩn cột + công thức letter không đổi; Import thêm 3 const + readImportSourceMeta; FE tự mang ID qua buildColMap (không sửa). Verify round-trip q66 + reflection OK.
Bước tiếp theo: Phase 2 — pre-check routing (so importSrcQuotationId vs quotation->id → Update/Cross-import) + đổi map Mã hàng→Line ID + popup chọn phương thức FE.
Blocked: không.

### Checkpoint — 2026-07-23 (6): Phase 10 — Mirror gom mã hàng tạm sang BOM-list
Vừa hoàn thành: mirror tính năng "1 hàng tạm → nhiều dòng chung 1 mã" sang bom-list (user chốt "mirror y hệt báo giá").
- BE `BomListService::syncProducts`: thêm `$gomMap` + helper `applyGomToPayload`/`seedGom`. Vì BOM xoá-sạch-recreate mỗi lần lưu (khác báo giá upsert theo price_id) → dùng `gom_key` (nhãn ẩn) làm khoá gom duy nhất, không cần directExistingTempCodes. Lint PASS. **Tinker 4/4 PASS** (fresh cùng nhãn chung mã / solo riêng / giữ mã có sẵn / fresh tái dùng mã có sẵn).
- FE `BomBuilderTableCard.vue`: nút "Nhân bản" (2 layout) trên hàng tạm không-ERP không-con → emit `duplicate-parent`. `BomBuilderEditor.vue`: `nhanBanTempGood` (clone thành group mới cùng group_id, gắn `_gom`), `mapGroupRowForSave` thêm `gom_key`, `dedupeTempGoodsCodes` bỏ qua dòng có `_gom`. Compile-check Node 14 PASS.
- KHÔNG áp cho BOM: import v2 (cột ẩn ID/cross-import/popup) — BOM import là replace-all, spec khác; vứt-mã-nhập (BOM builder không cho nhập mã); copy-popup/che-giá (BOM không quản lý giá).
Bước tiếp theo: user quyết có chạy E2E UI (bấm Nhân bản → Lưu → DB 2 dòng chung mã) không. CHƯA COMMIT.
Blocked: không.

### Checkpoint — 2026-07-23 (7): Phase 11 — Reuse hàng tạm dự án trên popup + import reuse
Vừa hoàn thành: tính năng "Dùng lại hàng tạm dự án" (select trên popup thêm hàng tạm) + import reuse theo mã, cho CẢ báo giá + BOM.
- BE: `ProductProjectController` param `only_temp` + *_id/vat trong 2 transform. Báo giá `QuotationService::saveDirectProduct` + `collectProjectTempGoodCodes` giữ mã project-good (Rule 1). Lint OK, tinker PASS.
- FE: reuse-picker `V2BaseSelectInModal` vào `QuotationProductSearchModal` (BOM, enableReuse) + `QuotationProductEditModal` (báo giá sửa) + 2 parent nối prop/handler. Fill+disable+Bỏ chọn; session-fresh link _gom; validation bỏ brand/origin khi reuse. Fix: đọc res.data (không res.data.data) cho nhóm 1. Compile-check 4 file PASS.
- Popup thật của BOM = QuotationProductSearchModal (BomBuilderAddProductModal là code chết — subagent phát hiện, khớp memory).
- E2E UI BOM PASS (BOM 40 tạm repoint project 5): picker 4 (dự án)+2 (trong phiếu); chọn → fill/disable; Lưu→DB dòng mới GIỮ mã TAM-TEST-002. BOM 40 khôi phục nguyên trạng.
Còn lại (chờ user quyết): (1) E2E UI báo giá (BE đã tinker PASS, FE compile OK, wiring symmetric); (2) BOM import remap master-data theo mã project-good (hiện chỉ giữ code từ file). CHƯA COMMIT.
Bước tiếp: user quyết có E2E báo giá + làm nốt BOM import remap không.
Blocked: không.

## Phase 12 — BOM import parity với báo giá v2 (user chốt 2026-07-23: "Có — làm từng phần" + cột ẩn Line ID + cross-import + popup lỗi 3 nút)
> QUYẾT ĐỊNH KIẾN TRÚC (quan trọng): BOM save hiện là **delete-recreate** (id đổi mỗi lần lưu, chỉ mã giữ) — KHÁC báo giá (upsert theo price_id, id ổn định). Để "từng phần" KHÔNG cần re-architect save: route BOM import QUA LƯỚI BUILDER (như báo giá onImportApplied) → merge FE theo Line ID (dbId, hợp lệ cho round-trip export→sửa→import ngay) + fallback theo CODE nếu Line ID stale → normal builder Save (delete-recreate cả lưới merged). syncProducts GIỮ NGUYÊN.
> Hiện BOM import = STANDALONE backend replace-all (BomImportModal→validate→importProducts). Đổi sang: validate (giữ) → apply vào builder grid (merge) → Save builder.
### BE (Task A — subagent Opus, lint OK + tinker round-trip PASS)
- [x] BOM export mode flat (`App\ExcelExport\BomListExport` + blade `exports/bom_list_import_format.blade.php`): thêm 2 cột ẩn `ID Hệ Thống` (=bom_list_products.id) + `ID BOM` (=bom_lists.id), append cuối FLAT_HEADERS (14→16), setVisible(false) cột O/P. Verify: BOM#1/#25 header 16 cột, O/P HIDDEN, line_id=id thật, dịch vụ O=service_item.id. importTemplate cũng ẩn 2 cột.
- [x] `validateImportData` trả `line_id`+`src_bom_list_id` mỗi dòng (đọc payload key `line_id`/`src_bom_list_id`); KHÔNG vào cột dữ liệu/detect trống. Tinker PASS (có→echo, thiếu→null không lỗi)
- [x] KHÔNG đổi syncProducts/importProducts (apply qua grid — Task B)
### FE (Task B — subagent Opus, compile-check Node 14 PASS, CẦN E2E)
- [x] BomImportModal: `extractHiddenIds` parse riêng 2 cột ẩn → gắn `__lineId`/`__srcBomListId` (không thêm vào columns để không vỡ file user); buildProducts gửi `line_id`/`src_bom_list_id`; applyValidation capture thêm line_id/group_parent/group_child/parent_index/product_type
- [x] Bỏ POST `/import` (replace-all) → `handleImport` mở **popup phương thức** (card Từng phần xanh/Thay thế đỏ, `bom-method-content`); `detectCrossImport` so src_bom_list_id vs bomId → popup cross-import (clone, ép line_id=null); `applyImportToGrid` emit `apply-import {rows,mode,crossImport}`
- [x] **Popup lỗi 3 nút** (`bom-err-content`): grid Dòng/Cột/Mô tả + Sao chép lỗi (TSV)/Tải file lỗi (CSV BOM UTF-8)/Đóng; link "Xem chi tiết N lỗi"
- [x] BomBuilderEditor `applyImportBom`: replace (xoá lưới+dựng lại 2 lượt cha/con+services) / partial (index theo dbId, khớp line_id→overlay tại chỗ giữ rowId/dbId; trống/không khớp→thêm mới; vắng→giữ; `findOrCreateBomGroupForImport` match tên+cha tránh nhóm rỗng); crossImport→line_id trống hết. `buildImportGridRow` đúng shape mapProductToRow. KHÔNG tự lưu (user bấm Lưu BOM)
- [x] **E2E UI PASS (2026-07-23, BOM 40 acct 48)**: export BOM 40 (16 cột, O/P ẩn = id thật) → Import Excel → Load → Validate (3 hợp lệ 0 lỗi) → nút Import mở **popup phương thức đúng 2 card** (Import từng phần / Thay thế hoàn toàn) → chọn Từng phần → Áp vào lưới: 1726/1728 khớp Line ID cập nhật tại chỗ, **con TEMP-BOM-0001 (không trong file, includeChildren=false) GIỮ**, không nhân đôi/nhóm rỗng → Lưu BOM → DB 3 dòng đúng mã, con nối đúng cha (parent_id), dịch vụ giữ. BOM 40 khôi phục.
- [x] **E2E bổ sung (2026-07-23, test kỹ theo yêu cầu user)**: (1) Thay thế hoàn toàn (file A) → lưới thay 4 dòng file, không nhân đôi ✓. (2) Thêm dòng mới + sửa SL (file B) → dòng mới thiếu TH/XX → **popup lỗi 3 nút** (Sao chép/Tải File/Đóng) + grid lỗi đúng ✓. (3) Nút Import chặn khi còn lỗi = CỐ Ý (toggle "Bỏ qua dòng lỗi"/`skipInvalid`, giống báo giá) ✓. (4) Cross-import (file BOM 25, ID BOM≠40) → **popup cảnh báo "Phát hiện dữ liệu thuộc BOM khác... sao chép, không giữ liên kết"** ✓; chọn replace + nút "**Sao chép vào lưới**" → grid = 3 dòng BOM 25, HHB001728 (BOM40 gốc, không trong file) bị xoá ✓. Không phát hiện bug.

### Checkpoint — 2026-07-23 (8): Phase 12 — BOM import parity (từng phần + cột ẩn Line ID + cross-import + popup lỗi)
Vừa hoàn thành: đưa BOM import lên parity với báo giá v2 (user chốt "Có — làm").
- Task A (BE, subagent Opus): BOM export flat thêm 2 cột ẩn ID Hệ Thống + ID BOM (setVisible false); validateImportData trả line_id/src_bom_list_id. Lint OK + tinker round-trip PASS.
- Task B (FE, subagent Opus): BomImportModal bỏ POST /import replace-all → popup phương thức (Từng phần/Thay thế) + cross-import + popup lỗi 3 nút; extractHiddenIds map 2 cột ẩn; emit apply-import. BomBuilderEditor applyImportBom (partial merge theo dbId/Line ID giữ dòng vắng, findOrCreateBomGroupForImport tránh nhóm rỗng / replace dựng lại). Compile-check PASS.
- Kiến trúc: KHÔNG đổi syncProducts/importProducts — apply vào lưới builder rồi Save builder (delete-recreate cả lưới merged).
- E2E UI PASS: round-trip BOM 40 export→import từng phần→Lưu→DB đúng (giữ con không trong file, không nhóm rỗng). BOM 40 khôi phục.
Còn lại (code xong, chưa E2E): thay thế hoàn toàn + cross-import BOM→BOM.
CHƯA COMMIT (toàn bộ Phase 10/11/12 uncommitted trên nhánh tpe-develop-assign 2 repo).
Bước tiếp: user quyết E2E nốt thay-thế/cross-import, hoặc review/commit.
Blocked: không.

### Checkpoint — 2026-07-23 (9): Fix 2 bug popup "Thêm hàng tạm" 2-tab (user báo)
- **BUG 1 — editor TSKT nhân bản mỗi lần chuyển sang Tab 2**: b-tabs mặc định giữ pane → `:visible` toggle destroy/recreate CKEditor nhưng DOM cũ không dọn (CKEditor destroy trên pane display:none để lại .cke mồ côi) → tích luỹ. FIX: thêm `lazy` cho `<b-tab title="Thêm mới thủ công">` → pane unmount khi rời tab → `beforeDestroy`→`destroyEditor` dọn sạch. E2E: count editor 1,1,1 qua 3 lần chuyển tab (trước 2,3,4).
- **BUG 2 — "chọn hàng tạm cũ phải lấy đủ thông tin"**: điều tra + dump dòng lưới HH000001 → FE ĐÃ carry đủ name/code/brand/origin/ĐVT/TSKT(product_attributes)/model_id. Blank chỉ do DATA: model_name null (model_id trỏ model đã xoá), giá=0 (HH000001 nguồn BOM — bom_list_products KHÔNG có cột quoted_price, estimated_price luôn 0). Vẫn FIX gap thật: nguồn "Trong phiếu" (session) hardcode giá=0 → nay carry estimated_price/quoted_price/vat/note (sửa directSessionTempGoods báo giá + sessionTempGoods BOM + loadReuseRows nhóm 1&2 + addSelectedReuse dùng row.note). Compile PASS 3 file.

### Checkpoint — 2026-07-24: FIX bug mã hàng tạm trùng giữa 2 báo giá (user báo trên dev q211/q212)
Bug: q212 import Excel từ q211 → giữ nguyên mã HHBG000701 của q211 (2 báo giá cùng mã). Nguyên tắc user: mã unique mỗi báo giá, TRỪ khi CHỦ ĐỘNG reuse hàng đã có ở product-project (picker "Dùng lại hàng tạm dự án").
Root cause: Rule 1 (Phase 11) tự GIỮ mã khi trùng project-good BẤT KỂ chủ ý → import/copy cũng bị giữ (sai).
Fix (gate keep sau cờ chủ ý):
- BE `QuotationService::saveDirectProduct`: chỉ giữ mã project-good khi có cờ `reuse_project` (picker gửi); import/copy/nhập tay không cờ → rơi xuống sinh HHBG mới. TINKER PASS.
- BE `createCopiedProductPrice` (copy): hàng tạm KHÔNG dùng lại mã nguồn → sinh HHBG mới theo id bản sao (giữ gom qua `$copiedTempCodeMap`). TINKER copy q116 PASS (mã bản sao đổi hết).
- FE `QuotationProductSearchModal.addSelectedReuse`: thêm `reuse_project: source==='project' && có mã`. `edit.vue`: carry `_reuseProject` vào dòng lưới + payload `reuse_project`.
Lưu ý: CHƯA deploy dev → dev còn code cũ (giữ mã vô điều kiện). Data q212 cũ là lịch sử, fix chỉ chặn phát sinh MỚI. BOM (syncProducts giữ mọi mã non-empty) có thể cùng loại lỗi — chưa đụng, chờ user.

### Checkpoint — 2026-07-24 (2): Đính chính rule mã hàng tạm + dedup product-project
User đính chính: **cùng dự án ĐƯỢC trùng mã** (như hiện tại), chỉ **khác dự án mới không được trùng**; màn product-project đang **bị lặp** (cùng mã cùng dự án hiện nhiều lần do copy/import).
- **REVERT** fix code-gen sai (cờ reuse_project + copy-regenerate) → về **Rule 1 gốc**: mã trùng "hàng hóa dự án" CỦA CHÍNH DỰ ÁN NÀY → giữ; khác dự án → sinh HHBG mới. TINKER PASS: cùng dự án 5 giữ TAM-TEST-001, khác dự án 999 → HHBG002295.
- **THÊM dedup** `ProductProjectController::index`: gộp theo (mã + dự án) — cùng mã CÙNG dự án chỉ 1 dòng; khác dự án hiện riêng. Thêm dedup_code/dedup_proj vào 2 key query + dedup PHP + LengthAwarePaginator (phân trang thủ công đúng sau gộp). TINKER PASS: 2 báo giá cùng dự án cùng mã → view 1 dòng.
- Data cũ trùng chéo dự án (HH000001 ×20, VH-TP...×69) là legacy do code CŨ (HH+đếm/báo giá); code mới HHBG+id toàn cục đã unique. Dedup (mã+dự án) vẫn hiện mỗi dự án 1 dòng (đúng — hàng của từng dự án).
- (tùy) export product-project cũng nên dedup tương tự — CHƯA làm. BOM cùng loại — chưa đụng.

### Checkpoint — 2026-07-24 (3): FIX same-project import từ báo giá NHÁP không giữ mã
Bug (user báo, local q125→q143): import file q125 (dự án 38, status 1 NHÁP) vào q143 (cùng dự án 38) → hàng tạm sinh mã MỚI thay vì giữ. Vì `collectProjectTempGoodCodes` chỉ lọc quotation status ĐÃ DUYỆT/TRÚNG THẦU (4/7) → hàng tạm của báo giá nháp chưa vào "Hàng hóa dự án" → Rule 1 không giữ.
Fix: BỎ filter status trong `collectProjectTempGoodCodes` (cả bom lẫn quotation) → mã hàng tạm ĐÃ TỒN TẠI trong CÙNG DỰ ÁN (bất kể trạng thái) → GIỮ; khác dự án → không tìm thấy → sinh HHBG mới. Đúng "cùng dự án được trùng, khác dự án không".
Verify:
- TINKER: import mã q125 (HHBG002270/71) vào dự án 38 (q125 nháp) → GIỮ; dự án 999 → HHBG002317/18 mới. PASS.
- Gom (Phase 10) không phá; export product-project status 200; dedup vẫn PASS.
- **E2E UI PASS**: export q125 (QuotationExcelExport) → import q143 (created_by tạm 48) → Sao chép (cross-import append) → Lưu nháp → DB q143: dòng clone GIỮ mã HHBG002270/71/72 (id mới 2319-2321). q143 khôi phục (snapshot + created_by=13).

### Checkpoint — 2026-07-24 (4): Ưu tiên dedup product-project (user chốt: trạng thái cao nhất → mới nhất)
Dedup cũ giữ dòng ĐẦU theo sort_created → phụ thuộc chiều sort (không ổn định). Sửa: quy tắc ưu tiên CỐ ĐỊNH độc lập sort hiển thị.
- Thêm `dedup_rank` vào 2 key query: quotation Trúng thầu(7)=3 > Đã duyệt(4)=2; BOM (đã duyệt)=2.
- `index()`: chọn dòng đại diện mỗi (mã+dự án) theo rank↓ → created_at↓ → row_id↓ (tất định), rồi mới sort hiển thị (asc/desc) + phân trang.
- TINKER PASS: Trúng thầu thắng Đã duyệt dù tạo cũ hơn; cùng status → mới nhất; dedup cơ bản + khác dự án tách + phân trang/shape vẫn đúng.

### Checkpoint — 2026-07-24 (5): Làm nốt — export dedup + BOM cùng-dự-án
1. **Export product-project dedup**: tách helper `dedupUnionRows($all,$sortDir)` dùng chung index()+export() (ưu tiên rank→mới nhất→id, độc lập sort). Export cũng gộp trùng. Lint OK; index total=4 + export status 200.
2. **BOM giữ mã cùng dự án** (mirror báo giá): `BomListService` + property `$syncKeepableTempCodes` + `collectSameProjectTempCodes` (mã hàng tạm CÙNG dự án, mọi trạng thái, cả cha lẫn con). store() set trước syncProducts; update() set TRƯỚC delete (để gồm mã của chính BOM → round-trip giữ mã). `applyGomToPayload` VỨT mã không thuộc dự án → sinh HHB mới.
   - TINKER PASS: round-trip giữ HHB001756; cross-project (FOREIGN) → HHB mới; import mã báo giá cùng dự án (TAM-TEST-001) → giữ; gom (nhân bản) vẫn chung mã.
   - **E2E UI PASS**: lưu BOM 40 bình thường → TEMP-BOM-0001/HHB001728 KHÔNG đổi (invariant round-trip). Khôi phục created_by=13.
=> Toàn bộ vấn đề mã hàng tạm: đồng nhất báo giá + BOM (cùng dự án giữ/trùng, khác dự án sinh mới) + product-project dedup (index + export).

### Checkpoint — 2026-07-24 (6): Product-project chỉ hiển thị HÀNG TẠM (chưa sync ERP)
User hỏi: sao có mã ERP `3M--T4DT135H:04` (q216) ở Hàng hóa dự án. Điều tra: đó là hàng TẠM đã ĐỒNG BỘ ERP (erp_product_id=40447 → mã ERP). Màn cũ cố ý lấy CẢ ERP + tạm. User chốt: **chỉ hàng tạm chưa sync ERP**.
Fix: thêm `whereNull('p.erp_product_id')` vào bomKeyQuery + quotationKeyQuery → chỉ hàng tạm (erp_product_id null); hàng đã sync ERP bị ẩn. Áp cho cả index + export (dùng chung 2 key query).
TINKER PASS: 5 item còn lại 100% "Chưa đồng bộ", 0 "Đã đồng bộ"; export status 200. Picker only_temp không ảnh hưởng (đã lọc sẵn).

### Checkpoint — 2026-07-24 (7): Product-project — giữ hàng tạm (kể cả đã sync ERP), ẩn ERP GỐC
Đính chính (6): user muốn hàng tạm ĐÃ SYNC ERP VẪN hiện; chỉ ẩn hàng ERP GỐC (chọn từ popup "Thêm hàng hóa").
- REVERT `whereNull(erp_product_id)` ở 2 key query. Thêm `erp_pid` (=erp_product_id) vào union.
- Marker phân biệt: `mysql2.products.tmp_product_id` != null ⇒ SP ERP tạo TỪ hàng tạm (temp-origin → GIỮ); null ⇒ ERP gốc (→ ẩn). 8501/43549 SP ERP là temp-origin.
- Helper `filterOutNativeErp($all)`: giữ erp_pid null (hàng tạm chưa sync) + erp_pid có tmp_product_id (temp-origin đã sync); ẩn native ERP. Gọi ở index + export TRƯỚC dedup.
- TINKER PASS: trước lọc 24 (16 erp) → sau 10 (2 erp, đều temp-origin, 0 native); hàng tạm không đụng. index total=10 (2 đã-sync giữ), export 200, picker only_temp=8 (0 đã-sync).
