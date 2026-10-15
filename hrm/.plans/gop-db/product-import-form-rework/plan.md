# Plan — Rework form Phiếu nhập hàng (HRM Finance)

Feature: `product-import-form-rework` · @namdangit · nhánh `gop_db`.
Màn: `pages/finance/product-imports/` (FE) + `Modules/Finance` (BE).
Design tổng: `design.md` · Design Cụm 1: `design-phase1.md`.

Phạm vi = 8 loại tạo tay (2,3,4,9,11,14,15,99). Chia 3 cụm, verify từng cụm.

---

## Cụm 1 — Khung động + loại 4 (Bán trả lại)  — ✅ XONG + VERIFY (08/10/2026)

### FE — khung cấu hình động
- [x] Tạo `pages/finance/product-imports/constants/importTypeConfig.js` (`IMPORT_TYPE_CONFIG` +
      `getTypeConfig`), khai đủ loại 4; placeholder loại khác (chỉ loại 4 `supported:true`).
- [x] `ProductImportForm.vue`: render tab theo `cfg.tabs` (`hasTab()` — bỏ 3 tab cứng).
- [x] Render cột bảng hàng hoá theo `cfg.columns` (gate kép `canViewCostPrice && cfg.columns[group]`).
- [x] Tiêu đề tab hàng hoá lấy theo `cfg`. (Dòng gợi ý hạch toán đã GỠ 08/10/2026 — ERP không có.)
- [x] Loại chưa khai config → callout "chưa được hỗ trợ" (dòng 303) + ẩn Lưu/Duyệt (computed `cfg.supported`, khớp BE 422).

### FE — đổi phiếu nguồn
- [x] Thêm nút "Đổi phiếu nhập kho" (V2BaseIconButton) cạnh mã PNK — `v-if="canChangeSource"` (computed: chỉ create + Đang tạo).
- [x] Bấm → `$confirm()` cảnh báo nạp lại → mở `WarehouseImportSearchModal` → `loadFromWarehouseImport(newId)`.
- [x] Nạp lại dòng hàng + gọi lại `loadAccountingWarehouses()` theo nguồn mới.
- [x] Nhánh ĐNNK: nút đổi phiếu YC tương tự (`changeRequestSource`). Edit mode: KHÔNG hiện nút đổi nguồn (verify: `changeSourceBtn:false`).

### FE — chuyển component HRM (Hướng A)
- [x] `<select>` kho kế toán → `V2BaseSelect`; SL → `V2BaseCurrencyInput` (disabled tới khi chọn kho).
- [x] Thanh nút `.export-actionbar` → `V2Footer` + slot `#custom-actions` (Lưu nháp/Lưu và tiếp tục/Duyệt).
- [x] Bọc nhóm bằng `V2BaseFormSection`; bảng hàng hoá bọc `V2BaseTableScroll`.
- [x] Số/tiền `1,234,567.89` (`toLocaleString('en-US')`); Duyệt + confirm popup (base-confirm-modal).
- [x] Lưu xong → `markFormSaved()` + `$router.push('/finance/product-imports')`.
- [x] Grep tự kiểm HTML thô RỖNG (xác nhận 08/10).
- [x] Dọn `|| '—'` → `|| ''` (ô rỗng để trống hẳn) ở `ProductImportForm.vue` (7 chỗ) +
      `WarehouseImportSearchModal.vue` (4) + `ProductImportRequestSearchModal.vue` (3).

### BE — tối thiểu
- [x] API edit/source trả `import_type` để FE chọn config (resource Sửa trả `type`+`import_type_name`;
      phiếu YC trả `type`/`type_name`; map trong loadForEdit/loadFromRequest).
- [x] KHÔNG mở `buildDetailsByType`/`store()` cho loại ≠ 4 (giữ nguyên, loại khác BE ném 422).
- [x] **FIX display gap**: `loadForEdit()` đọc thẳng `supplier_price` BE trả (gate `canViewCostPrice`),
      bỏ hard-code `supplier_price: 0` + comment cũ sai. store ghi (ProductImportService:1921),
      Resource trả (ProductImportDetailResource:180). Màn Sửa nay khớp màn Tạo (844,586 / 1,689,172).
- [x] **FIX hạ tầng**: chạy migration thêm cột `companies.consignment_warehouse_ids` (thiếu → endpoint
      `accounting-warehouses` 500). Sau fix: request trả 200, select kho đổ đúng option.

### Verify Cụm 1  — ✅ bấm thật trên 127.0.0.1:3000 (08/10/2026)
- [x] B1 Tạo nháp loại 4 từ PNK-08872 → config đúng (tab/cột/tiêu đề), chọn kho, Lưu nháp POST 200,
      vào danh sách hiện "Đang tạo" (PNH-12343).
- [x] B2 Cấu hình động đúng loại 4 (tab Hàng hoá nhập trả lại + Chi phí nội địa + bốc xếp).
- [x] B3 Chọn kho kế toán (V2BaseSelect) → SL mở nhập.
- [x] B4 Duyệt có popup xác nhận `$confirm` ("Xác nhận duyệt… sinh bút toán và không sửa được" +
      Duyệt/Hủy) — bấm Hủy, KHÔNG duyệt thật.
- [x] B5 Catalog `accounting-warehouses?warehouse_import_id=8872` → 200, đổ 2 option (Hàng bán / Hàng khuyến mại).
- [x] B6 Edit mode: KHÔNG có nút đổi nguồn; data load đúng (giá 844,586 / 1,689,172); edit-save POST 200;
      console sạch (chỉ socket.io:8891 + menu-settings 400 — pre-existing, không liên quan).
- [x] Anomaly "Không có kho kế toán phù hợp" ở lần snapshot đầu = ARTIFACT do catalog fetch async
      chưa xong; chờ 2s thì kho đổ "Liên Ninh - Hàng bán" + callout biến mất. KHÔNG phải regression.

---

## Rà soát nhãn (label) theo ERP — ✅ XONG + VERIFY (08/10/2026)

User yêu cầu: **nhãn phải LẤY ĐÚNG ERP, không bịa/không sáng tạo** (nghi ERP sai thì sửa theo ngữ
cảnh phiếu). Nguồn chân lý nhãn = `ERP .../product_imports/form.blade.php`. Đã đối chiếu từng nhãn
và sửa trên `ProductImportForm.vue` + `CostTable.vue` + `importTypeConfig.js`:

- Section header: "Hàng hoá & chi phí" → **"Chi tiết"** (ERP `<h4>Chi tiết</h4>`).
- Tab hàng hoá: tiêu đề động/bịa (`goodsTabTitle`) → cố định **"Hàng hóa"** cho MỌI loại
  (gỡ hẳn `goodsTabTitle` khỏi config + docblock).
- Tab chi phí nội địa: "Chi phí nội địa" → **"Chi phí giao nhận hàng nội địa"** (#chi_phi_noi_dia).
- Tab bốc xếp: "Chi phí bốc xếp" → **"Chi phí bốc hạ hàng tại kho"** (#chi_phi_boc_ha_hang_tai_kho).
- Cột bảng hàng hoá (8 nhãn khớp ERP): Tên hàng→**Tên hàng hóa**, Mã hàng→**Mã hàng hóa**,
  ĐVT→**Đơn vị tính**, Giá nhập kho→**Giá nhập kho (VNĐ)**, Thành tiền nhập kho→**Thành tiền giá
  nhập kho (VNĐ)**, Đơn giá bán→**Giá bán**, Thành tiền bán→**Thành tiền giá bán**, VAT %→**VAT**.
- Field thông tin chung: "Phiếu YC nhập hàng" → **"Phiếu yêu cầu nhập hàng"** (gỡ viết tắt).
- CostTable: "Loại chi phí"→**Chi phí**, thêm **(VNĐ) (\*)** cho "Giá trị trước VAT",
  "Thành tiền"→**Giá trị sau VAT (VNĐ)**, placeholder "Chọn loại chi phí"→**"Chọn chi phí"**.
- Totals + nhãn còn lại (Tổng tiền bán / Tổng giảm giá / Tổng tiền trước thuế / Tiền VAT / Tổng
  tiền sau thuế; Nhập thẳng; Kho nhập; Thủ kho; Khách hàng; Người giao hàng; Không trả hóa đơn;
  Ghi chú; nút picker nguồn) — **đã khớp sẵn ERP**, không đổi.
- Verify: mở `/finance/product-imports/12343/edit` (loại 4) trên 127.0.0.1:3000, snapshot xác nhận
  mọi nhãn hiển thị đúng ERP; form render sạch (console error còn lại = socket.io + menu-settings
  400 pre-existing).

### ⚠️ Phát hiện LỆCH CẤU TRÚC khi rà nhãn (chờ user chốt — KHÔNG tự dựng vì vượt scope "nhãn")
1. ✅ **ĐÃ XỬ LÝ (user duyệt 08/10/2026)** — Tab bốc hạ sai điều kiện cho loại 4. Đã dựng tab
   "Phân bổ chi phí" + gate pickup foreign-only. Xem mục 'Tab "Phân bổ chi phí" (loại 4)' ở trên.
2. ✅ **ĐÃ XỬ LÝ (user duyệt 08/10/2026)** — CostTable thiếu cột so ERP. Đã bổ sung 3 cột
   **Nhà cung cấp (\*)** / **Ghi chú** / **File đính kèm (\*)** end-to-end. Xem mục 'CostTable —
   3 cột NCC/Ghi chú/File' ở dưới.
3. ✅ **ĐÃ XỬ LÝ — GỠ (user chốt 08/10/2026)** — Dòng "gợi ý hạch toán" (`accountingHint`) là
   phần HRM tự thêm, ERP KHÔNG có → đã gỡ sạch: xoá field `accountingHint` khỏi 8 entry +
   docblock trong `importTypeConfig.js`, xoá block hiển thị `<div class="acc-hint">` + comment
   trong `ProductImportForm.vue`. (Class `.acc-hint` giữ lại — còn dùng cho callout "chưa tải
   danh mục kho kế toán".) Verify live PNH-12343: dòng gợi ý đã biến mất, form loại 4 render
   đúng 3 tab, không lỗi console mới.

---

## Tab "Phân bổ chi phí" (loại 4) + gate pickup foreign-only — ✅ XONG + VERIFY (08/10/2026)

User duyệt phát hiện #1 → DỰNG tab "Phân bổ chi phí" cho loại không-ngoại + gate tab bốc-hạ về
foreign-only (bám ERP `form.blade.php` #phan_bo_chi_phi `ng-if="!is_foreign"` / #chi_phi_boc_ha_hang_tai_kho
`ng-if="is_foreign"`).

### Cấu hình tab (importTypeConfig.js)
- [x] Docblock `tabs`: khoá quy tắc gate — inlandCost=has_inland_cost(type≠3) · allocation=!is_foreign ·
      pickupCost=is_foreign(1,11). Loại không-ngoại hiện 'allocation', KHÔNG 'pickupCost'.
- [x] Loại 4: `['products','inlandCost','allocation']` (bỏ `pickupCost`). Tương tự 2,15,99,9,14.
- [x] Loại 3: `['products','allocation']` (has_inland_cost=false → không inlandCost; non-foreign → vẫn allocation).
- [x] Loại 11 (ngoại): giữ `['products','inlandCost','pickupCost']` (allocation/#phan_bo_hang_giu = Cụm 3).

### FE — tab Phân bổ chi phí (ProductImportForm.vue)
- [x] b-tab mới "Phân bổ chi phí" (sau inlandCost, trước pickup) gate `hasTab('allocation') && canViewCostPrice`.
- [x] Header: "Tổng chi phí nội địa (VNĐ)" = `totalInlandCostBeforeVat()`; status "Đã phân bổ X"
      (xanh `#16a34a` khi `allocatedComplete()`, đỏ `#dc2626` khi lệch).
- [x] Radio Số lượng/Giá trị (`V2BaseRadio`, value '1'/'2' khớp ERP) + nút "Phân bổ".
- [x] Bảng 9 cột ERP (#phan_bo_chi_phi): STT · Hàng hóa · ĐVT · SL · Đơn giá · Thành tiền · Chi phí
      nội địa (input `V2BaseCurrencyInput`) · Giá trị nhập kho · Đơn giá nhập kho.
- [x] `allocateCost()` port verbatim ERP: type '1' chia theo SL (`qty*ΣInland/Σqty`), type '2' chia
      theo giá trị (`rowAmount*ΣInland/Σprice`). `inland_allocation` = STORED (nút set), KHÔNG auto-split.
- [x] `rowInlandAllocation` trả `Number(row.inland_allocation)||0`; chảy vào `rowTotal`/`rowImportPrice`
      + `buildLotsPayload` (inland_allocation/total/vat_cost/amount_after_vat).
- [x] `mapSourceRow` + `loadForEdit` khai `inland_allocation` (Vue2 reactivity; edit gate canViewCostPrice).
      `unsavedSnapshotSource` thêm `ia`. data() thêm `allocate_type:'1'`.
- [x] pickup b-tab giữ lại, nay gate `hasTab('pickupCost')` (foreign-only); gỡ comment "chưa port".
- [x] Grep HTML thô RỖNG.

### Verify  — ✅ bấm thật trên 127.0.0.1:3000 (PNH-12343 loại 4)
- [x] Tab order: Hàng hóa → Chi phí giao nhận hàng nội địa → Phân bổ chi phí (KHÔNG có bốc-hạ cho loại 4).
- [x] Header đủ "Tổng chi phí nội địa (VNĐ)" + radio Số lượng/Giá trị + nút Phân bổ.
- [x] Thêm chi phí nội địa 300,000 ở tab Chi phí → Tổng reactively = 300,000.
- [x] Bấm Phân bổ (Số lượng): Chi phí nội địa dòng = 300,000; Giá trị nhập kho 1,689,172 → 1,989,172;
      Đơn giá nhập kho → 994,586; status "Đã phân bổ 300,000" chuyển XANH (allocatedComplete).
- [x] Input "Chi phí nội địa" editable, ghi vào row.

---

## CostTable — 3 cột NCC/Ghi chú/File — ✅ XONG + VERIFY (08/10/2026)

User duyệt phát hiện #2 → thêm **Nhà cung cấp (\*)** / **Ghi chú** / **File đính kèm (\*)** vào
CostTable (mirror ERP `#chi_phi_noi_dia` + `#chi_phi_boc_ha_hang_tai_kho`). Nhãn nguyên văn ERP
`form.blade.php:1272-1277` ("Ghi chú" KHÔNG có `*`; NCC placeholder "Chọn NCC"; file "Chọn file").

### FE — CostTable.vue
- [x] thead 7→10 cột: thêm "Nhà cung cấp (\*)" / "Ghi chú" / "File đính kèm (\*)"; empty colspan 7→10.
- [x] NCC: `V2BaseSelectRemote` (fetchFn `finance/bill-income-requests/search-suppliers`, map
      `{id, name:'<code> - <fullname>'}`, `initialOption` giữ nhãn edit, `minimumInputLength=2`,
      `height=32px`) — copy pattern BuyServiceDetailTable.vue.
- [x] Ghi chú: `V2BaseInput v-model="row.note"`.
- [x] File: `V2BaseFile :auto-upload` accept `.pdf,.png,.jpg,.docx,.doc,.xls,.xlsx` → trả URL S3 (string).
- [x] Nhánh read-only "chi phí sắp xếp giao hàng" (ERP `Cost::findCostArrange`) KHÔNG port —
      chỉ phát sinh ở Cụm 3, không reachable loại 4 (ghi docblock).

### FE — ProductImportForm.vue (data model)
- [x] `mapCostRow` + `emptyCostRow` thêm `supplier_code/supplier_name` (chỉ để dựng nhãn edit) +
      `attachment`. `buildCostsPayload` thêm `attachment` (null→'').

### BE
- [x] `ImportCost` $fillable += `attachment`.
- [x] `ProductImportService::syncCostsByType` set `$cost->attachment = $row['attachment'] ?? ''`
      (cột `import_costs.attachment` varchar(255) **NOT NULL không default** → PHẢI '' khi trống,
      ghi NULL sẽ nổ single-row insert). Cập nhật docblock (bỏ "skip attachment").
- [x] `ProductImportDetailResource` costs block: thêm `attachment` + `supplier_code`/`supplier_name`
      (leftJoin `customers` 1 lần, tránh N+1) để màn Sửa dựng lại nhãn ô NCC.
- [x] `ProductImportStoreRequest`: `inland/pick_up/contract_costs.*.note` = nullable|max:255 +
      `.attachment` = nullable|string|max:1000. Giữ `supplier_id` nullable (khớp ERP inland attachment
      optional — rule attachment ERP đang comment).

### Verify — ✅ bấm thật 127.0.0.1:3000 (PNH-12343 loại 4)
- [x] 10 header render đúng; "(\*)" đỏ ở NCC + File; empty "Chưa có chi phí".
- [x] Thêm chi phí: ô NCC (select2 "Chọn NCC") + Ghi chú (input) + File ("Chọn file") render.
- [x] Nhập value 1,000,000 + VAT 10% → VAT cell 100,000, total 1,100,000 (model reactive).
- [x] Endpoint search-suppliers trả `{id,code,fullname}` (10 kết quả 'cong').
- [x] Lưu nháp → về list; reload edit → cost_id/value/VAT **+ supplier_id 11720 + supplier_code
      + supplier_name + note "Ghi chú test NCC"** round-trip; attachment '' → null (graceful).
- [x] Edit-mode ô NCC hiện lại "0104509916 - CÔNG TY CỔ PHẦN CÔNG NGHỆ HỢP LONG" (initialSupplier).
- [x] Revert: xoá dòng test + lưu lại (12343 về trạng thái không có chi phí nội địa).

---

## Cụm 2 — Nhóm mua trong nước: 2, 15, 99  (ĐANG MỞ — 08/10/2026)

**Nguồn chân lý hạch toán (ERP đọc verbatim session này):**
- Loại 2/15 → `ProductImport.php::getDataCreateDept` dòng **2248-2304** (nhánh `in_array(type,[2,15,16])`):
  hàng hoá `Nợ1541/Nợ1331/Có3311(supplier)` → chi phí NCC (costs type 4) `Nợ1541/Nợ1331/Có3311(supplier)`
  → chi phí nội địa (costs type 2) **mỗi dòng CÓ supplier** `Nợ1541/Nợ1331/Có3311(inland supplier)`
  → giá vốn: mỗi SP `Nợ1561 = product->total [ref 1541] product_id`, `Có1541 = Σ product->total`.
- Loại 99 → nhánh else **2369-2378**: chỉ lặp pick_up_costs, CHỈ post khi `arrange_delivery->rent_type==2`.
  HRM tạo tay loại 99 KHÔNG có tab bốc-hạ / quan hệ arrange_delivery → **[] (no-op trung thực)**.
- `getSupplierAttribute` 193-199: `warehouse_import->supplier` OR `product_import_request->supplier`.
- Display loại 2/15 (bảng biến thể B, form.blade 731-814): cột SL·Đơn giá·Thành tiền VND·VAT%·VAT tiền;
  footer `vat_cost = Σ(supplier_price×qty×vat%/100)` (per-line) — KHÁC công thức header-vat loại 4.

### BE — `ProductImportService.php`
- [x] (1) Nới gate `update()` (242-246) từ `!== BAN_TRA_LAI` → cho phép {BAN_TRA_LAI(4), MUA_HANG_TRONG_NUOC(2),
      MUA_HANG_TRONG_NUOC_TU_DO(15), KHAC(99)}; loại khác vẫn 422. → ĐÃ CÓ (246-248).
- [x] (2) Tổng quát hoá builder: đổi tên `buildDetailsForSaleReturn()` → builder chung; buildDetailsByType
      route cases 2/15/99 vào builder; **KHÔNG ép `contract_cost_allocation = 0` cho 2/15** (chỉ ép 0 cho
      loại 4 — loại 4 UI không có chi phí type 4 nên tự khắc 0). → ĐÃ CÓ (1049-1051 route về builder chung 1881+).
- [x] (3) `accumulateReturnedQtyByType`: GIỮ default no-op cho 2/15/99 (không phải is_return 3/4/9).
- [x] (4) `resolveAccountingService`: thêm case 2,15 → DomesticPurchase; case 99 → Other. → ĐÃ CÓ (1178-1185).
- [x] (5) `recomputeMoneyServerSide`: tính `contract_cost_allocation` qty-tỉ lệ từ costs type 4
      (`Σ = Σ value_before_vat` costs type 4) → `total = exchanged + inland_allocation + contract_cost_allocation`;
      header `vat_cost` loại {2,15} = Σ per-line `supplier_price×qty×lineVat/100` (loại 4 giữ công thức cũ). → ĐÃ CÓ (domesticVatTypes 2173).
- [x] (6) `fillHeader`: cập nhật comment currency VNĐ/1 đúng cho cả 2/15/99 (không đổi logic).

### BE — service hạch toán mới (mirror ERP trực tiếp, KHÔNG dùng helper revenue 632/1561/1562 của base)
- [x] `DomesticPurchaseProductImportAccountingService` (loại 2/15): mirror ERP 2248-2304 verbatim
      (hàng hoá → chi phí NCC type4 → nội địa type2 per-supplier → giá vốn 1561/1541). → FILE ĐÃ CÓ; prior-session tinker: PI#12238 (type 2) + PI#12294 (type 15) `build()` ra 7 dòng mỗi phiếu.
- [x] `OtherProductImportAccountingService` (loại 99): pickup-only → `build()` trả `[]` cho tạo-tay. → FILE ĐÃ CÓ; tinker xác nhận `build()`=[] cho tạo-tay (không arrange_delivery).
- [x] `ProductImportAccountingService` (base): thêm `resolveSupplierId(ProductImport $obj): ?int`
      (mirror getSupplierAttribute: `warehouse_imports.supplier_id` OR `product_import_request->supplier_id`).

### BE — validation (nếu cần)
- [x] Rà `ProductImportStoreRequest`/`UpdateRequest` cho nhập tay loại 99 (bảng biến thể C: giá bán/giảm/VAT).
      → Store/Update đã nhận `lots.*.acc_warehouses` + cột giá (mirror ERP, không thêm rule riêng loại 99).

### FE
- [x] `importTypeConfig.js`: bật `supported: true` cho 2, 15, 99 (sau khi BE mở). → ĐÃ CÓ (2:86, 15:101, 99:116).

### Verify — bấm thật 127.0.0.1:3000 (KHÔNG commit/push)
- [x] Loại 2 (Mua trong nước): tạo tay → Lưu nháp → reload edit round-trip; bảng biến thể B đúng cột.
      → Nguồn PYCNH-12183 → **PNH-12345** (type 2, status 3, is_import_direct=1, company 1, warehouse_id=NULL):
      POST 200, 1 dòng chi tiết (product 47894, qty 2) + 1 dòng `product_import_detail_accountings` (kho 29
      "Hà Nội - Nhập xuất thẳng", qty 2), **0 dòng journal** (draft). Mở lại /12345/edit: loại/kho/SL=2 (2/2) reload đúng.
- [x] Loại 15 (Mua trong nước tự do): như loại 2. → prior session: draft PNH-12344 (status 3) 0 journal; PI 12294 (duyệt) 7 dòng journal. Label "Nhập hàng mua trong nước (TỰ DO + HÃNG)" khớp ERP.
- [x] Loại 99 (Khác): bảng biến thể C (giá bán/giảm/VAT); duyệt → KHÔNG post journal (no-op).
      → Nguồn PYCNH-12104 render: label "Nhập hàng khác"; đủ cột biến thể C (Giá bán · Thành tiền giá bán · Giảm giá ·
      Đơn giá sau giảm · Thành tiền sau giảm · VAT · Tiền VAT · Thành tiền sau VAT) — khớp ERP form.blade 825-841 verbatim;
      footer Tổng tiền bán/trước thuế/VAT/sau thuế. `OtherProductImportAccountingService::build()`=[] (no-op). Render-only (nguồn công ty 4).
- [x] Draft status 3 KHÔNG post journal (handleCompleted chỉ chạy khi DA_HOAN_THANH).
      → PNH-12345 (type 2) + PNH-12344 (type 15) đều status 3, 0 dòng journal.

---

## Cụm 3 — Nhóm nước ngoài & mượn/gửi: 11, 3, 9, 14  (ĐÃ MỞ — 08/10/2026)

**BE**
- [x] Builder chung `buildDetailsByType` nhận loại 11 (FOREIGN → `buildDetailsForeignPurchase`) + 3/9/14 (`buildDetailsFromSource`).
- [x] Loại 11 money **Option A — server-side dựng từ `order_import_request_products`** (không tin FE): `recomputeMoneyForeign` + phân bổ `pick_up_cost` theo tỉ lệ `amount_after_vat` của ĐƠN. Dry-run PIR 12193 + 12228 (8 dòng, đa dòng + bốc xếp) → total/import_price/inland_col/pickup khớp công thức, ledger CÂN.
- [x] `resolveAccountingService`: 11 → ForeignPurchase; 9 → BorrowSellReturn; 3/14 → Other (no-op). Dry-run 3/9/14 (verify_domestic.php): 9 ledger CÂN; 3/14 no-op đúng.
- [x] Pin id dòng nguồn trong `buildDetailsForeignPurchase` + `buildDetailsFromSource` (regression-free — dry-run domestic 3/9/14 xác nhận).
- [x] **Fix type 14 "Hạn gửi"**: `lots.*.expire_prepick_date` = `nullable|date|after:today` ở `ProductImportStoreRequest` + `ProductImportUpdateRequest` (bỏ `required_if:lots.*.allocation` của ERP vì payload HRM không có cờ `allocation` theo dòng); `ProductImportDetailResource` trả `expire_prepick_date` (Y-m-d, KHÔNG gate giá vốn) để prefill màn Sửa. `buildDetailsFromSource` đọc `$l['expire_prepick_date']` (sẵn có) → ghi kho GIỮ.

**FE (importTypeConfig.js + ProductImportForm.vue)**
- [x] Config 11 = FOREIGN variant: tabs[products,inlandCost,pickupCost], isForeign/hasInlandCost/allocationAll. Config 3 = DEFAULT tabs[products,allocation]. Config 9 = DEFAULT tabs[products,inlandCost,allocation] listedPrice. Config 14 = DEFAULT tabs[products,inlandCost,allocation] consignmentDeadline.
- [x] `supported: true` cho 11/3/9/14 (sau khi BE mở).
- [x] **Fix type 14 "Hạn gửi"**: thêm `<th>Hạn gửi</th>` (nhãn đúng ERP `form.blade.php:839`, trước "Kho kế toán") + body `<td>` `V2BaseDatePicker`; **un-gate** `consignmentDeadline` khỏi `canViewCostPrice` trong `cols()` (là NGÀY hẹn giữ, không phải giá — ERP chỉ gate `type==14`); wire `expire_prepick_date` qua `mapSourceRow` + edit-load + `buildLotsPayload`.
- [x] **Fix checkbox "Không trả hóa đơn"** (user báo 09/10): ERP `form.blade.php:189` gate `ng-if="form.type == 4 || form.type == 9"` → thêm cờ `flags.hasNotPayingBill` (chỉ loại 4,9) vào `importTypeConfig.js`, gate checkbox bằng `cfg.flags.hasNotPayingBill` (trước đó hiện ở MỌI loại). Thêm `:disabled="mode !== 'create'"` bám `ng-disabled="form.id"` của ERP. Playwright: loại 14 ẩn, loại 9 hiện.

**Verify từng loại (Playwright 127.0.0.1:3000 + dry-run BE)**
- [x] Render 11/3/9: guard `supported` gỡ, tab/cột khớp importTypeConfig.
- [x] Loại 14 (PYCNH-12226): cột "Hạn gửi" render giữa "Thành tiền sau VAT" và "Kho kế toán", body là `V2BaseDatePicker` ("Chọn ngày..."); không runtime error/Vue warn/404/500 (13 "errors" chỉ là HMR dev-mode export-not-found noise, không liên quan).
- [x] `php -l` 3 file BE đổi → sạch.

---

## Checkpoint
### Checkpoint — Fix checkbox "Không trả hóa đơn" chỉ loại 4,9 (user báo 09/10/2026)
Vừa hoàn thành: user phát hiện checkbox **"Không trả hóa đơn"** hiện ở MỌI loại khi tạo phiếu nhập
hàng, trong khi ERP `form.blade.php:189` chỉ cho loại 4 (Bán trả lại) & 9 (Nhập bán mượn trả lại)
(`ng-if="form.type == 4 || form.type == 9"`). Sửa theo pattern config động: thêm cờ
`flags.hasNotPayingBill: true` cho type 4 & 9 trong `importTypeConfig.js` (+ docblock), gate checkbox
trong `ProductImportForm.vue` bằng `v-if="cfg && cfg.flags && cfg.flags.hasNotPayingBill"`; thêm
`:disabled="mode !== 'create'"` bám `ng-disabled="form.id"` của ERP (khóa sau khi phiếu đã lưu).
Playwright: loại 14 (PYCNH-12226) checkbox ẩn; loại 9 (PYCNH-11689) checkbox hiện.
Đang làm dở: (không).
Bước tiếp theo: CHỜ USER NGHIỆM THU. KHÔNG commit/push khi user chưa yêu cầu.
Blocked: (không).

### Checkpoint — Cụm 3 (loại 11,3,9,14) VERIFY XONG + fix type-14 "Hạn gửi" (08/10/2026)
Vừa hoàn thành: **Cụm 3 verify đầy đủ (Playwright 127.0.0.1:3000 + dry-run BE) — PASS cả 4 loại**,
và **sửa 1 lỗi thật phát hiện qua Playwright**: loại 14 (Nhập gửi) có `consignmentDeadline:true`
trong config + đếm trong `prodColCount` NHƯNG thiếu `<th>`/`<td>` → cột "Hạn gửi" không bao giờ
render + colspan lệch 1. Thêm nữa, cờ `consignmentDeadline` bị gate nhầm theo `canViewCostPrice`
(nó là NGÀY hẹn giữ, không phải giá — ERP `form.blade.php:839` chỉ gate `type==14`).
- BE dry-run: loại 11 (PIR 12193 + 12228 đa dòng + bốc xếp) total/import_price/inland_col/pickup khớp công thức, ledger CÂN; loại 9 ledger CÂN; 3/14 Other no-op đúng. Pin id dòng nguồn regression-free.
- Fix FE `ProductImportForm.vue`: import + register `V2BaseDatePicker`; `<th>Hạn gửi</th>` (nhãn đúng ERP, trước "Kho kế toán") + body `<td>` datepicker (rowspan); un-gate `consignmentDeadline` khỏi `canViewCostPrice` trong `cols()`; wire `expire_prepick_date` qua `mapSourceRow` + edit-load map + `buildLotsPayload`.
- Fix BE: `lots.*.expire_prepick_date` = `nullable|date|after:today` ở Store+Update request (bỏ `required_if:lots.*.allocation` của ERP — payload HRM không có cờ theo dòng); `ProductImportDetailResource` trả `expire_prepick_date` (Y-m-d, KHÔNG gate giá vốn) để prefill Sửa. `php -l` 3 file sạch.
- Playwright loại 14 (PYCNH-12226): cột "Hạn gửi" render đúng vị trí, body là `V2BaseDatePicker` ("Chọn ngày..."); không runtime error/Vue warn/404/500 (13 "errors" console chỉ là HMR dev export-not-found noise).
Đang làm dở: (không) — Cụm 3 đóng.
Bước tiếp theo: **CHỜ USER NGHIỆM THU Cụm 3** (toàn bộ 8 loại tạo tay đã xong). KHÔNG commit/push khi user chưa yêu cầu.
Blocked: (không).

### Checkpoint — Gỡ dòng gợi ý hạch toán (accountingHint) XONG + VERIFY (08/10/2026)
Vừa hoàn thành: **Gỡ phát hiện #3 — dòng "gợi ý hạch toán" (HRM tự thêm, ERP không có)**, user chốt
GỠ. Xoá field `accountingHint` ở 8 entry + 2 dòng docblock trong `importTypeConfig.js`; xoá block
`<div class="acc-hint">…accountingHint…</div>` + sửa comment `cfg()` trong `ProductImportForm.vue`.
Class `.acc-hint` + callout "chưa tải danh mục kho" GIỮ lại (không liên quan). Verify live
PNH-12343: dòng gợi ý biến mất, form loại 4 render đúng 3 tab (Hàng hóa · Chi phí giao nhận hàng
nội địa · Phân bổ chi phí), bảng chi phí nguyên vẹn; console chỉ còn 2 lỗi CŨ (socket.io 8891 +
V2BaseTextarea rows) — không lỗi mới.
Đang làm dở: (không).
Bước tiếp theo: cả 3 phát hiện lệch cấu trúc (#1 tab Phân bổ · #2 cột NCC/Ghi chú/File · #3 gỡ gợi
ý hạch toán) ĐÃ XONG. **CHỜ USER NGHIỆM THU Cụm 1**. Sau đó mở Cụm 2 (loại 2,15,99).
Blocked: (không) — CHƯA commit/push (chờ user yêu cầu).

### Checkpoint — CostTable 3 cột NCC/Ghi chú/File XONG + VERIFY (08/10/2026)
Vừa hoàn thành: **Thêm 3 cột Nhà cung cấp (\*) / Ghi chú / File đính kèm (\*) vào CostTable**
(phát hiện lệch #2, user duyệt). FE: `CostTable.vue` (thead 7→10, V2BaseSelectRemote NCC +
V2BaseInput note + V2BaseFile autoUpload; empty colspan 10), `ProductImportForm.vue`
(mapCostRow/emptyCostRow/buildCostsPayload += attachment + supplier_code/supplier_name). BE:
`ImportCost` $fillable += attachment; `syncCostsByType` set attachment (''—NOT NULL no default);
`ProductImportDetailResource` costs += attachment/supplier_code/supplier_name (leftJoin 1 lần);
`ProductImportStoreRequest` += note/attachment nullable (3 nhóm). Verify live PNH-12343: 10 header
đúng, NCC/Ghi chú/File render, save→reload round-trip supplier_id 11720 + code + name + note;
ô NCC edit-mode hiện "0104509916 - CÔNG TY CỔ PHẦN CÔNG NGHỆ HỢP LONG"; đã revert test về sạch.
Đang làm dở: (không).
Bước tiếp theo: **CHỜ USER NGHIỆM THU**. Còn phát hiện #3 (gỡ/giữ dòng gợi ý hạch toán
`accountingHint` — HRM tự thêm, ERP không có) chờ user quyết. Sau đó mở Cụm 2 (loại 2,15,99).
Blocked: (không) — CHƯA commit/push (chờ user yêu cầu).

### Checkpoint — Tab "Phân bổ chi phí" + gate pickup foreign-only XONG + VERIFY (08/10/2026)
Vừa hoàn thành: **Dựng tab "Phân bổ chi phí" cho loại 4 + gate tab bốc-hạ về foreign-only** (user
duyệt phát hiện lệch #1). Sửa `importTypeConfig.js` (tabs loại 4/2/15/99/9/14/3 sang 'allocation',
giữ 'pickupCost' loại 11; docblock khoá quy tắc gate) + `ProductImportForm.vue` (b-tab mới với header
"Tổng chi phí nội địa (VNĐ)" + status Đã phân bổ xanh/đỏ + radio Số lượng/Giá trị + nút Phân bổ +
bảng 9 cột ERP; `allocateCost()` port verbatim; `inland_allocation` STORED; khai reactivity ở
mapSourceRow/loadForEdit/snapshot; import+register V2BaseRadio; styles .alloc-*).
Verify live PNH-12343: tab order đúng (không bốc-hạ), thêm chi phí 300,000 → Tổng reactively,
bấm Phân bổ → dòng 300,000 + Giá trị nhập kho 1,989,172 + Đơn giá 994,586 + status XANH.
Đang làm dở: (không).
Bước tiếp theo: **CHỜ USER NGHIỆM THU**. Phát hiện lệch #2 (CostTable thêm cột NCC/Ghi chú/File) và
#3 (gỡ/giữ dòng gợi ý hạch toán) VẪN chờ user duyệt — chưa tự dựng. Sau đó mở Cụm 2 (loại 2,15,99).
Blocked: (không) — CHƯA commit/push (chờ user yêu cầu).

### Checkpoint — Rà soát nhãn theo ERP XONG + VERIFY (08/10/2026)
Vừa hoàn thành: **Rà soát & sửa toàn bộ nhãn form loại 4 cho khớp ERP** (theo yêu cầu user "nhãn
lấy đúng ERP, không bịa"). Sửa `ProductImportForm.vue` (section header + 3 tiêu đề tab + 8 cột bảng
hàng hoá + 1 field thông tin chung), `CostTable.vue` (3 header + placeholder), `importTypeConfig.js`
(gỡ `goodsTabTitle` bịa). Verify live trên 127.0.0.1:3000 (phiếu PNH-12343 loại 4): mọi nhãn khớp
ERP, form render sạch.
Đang làm dở: (không).
Bước tiếp theo: **CHỜ USER NGHIỆM THU** phần nhãn + **quyết 3 phát hiện lệch cấu trúc** (xem mục
"⚠️ Phát hiện LỆCH CẤU TRÚC" ở trên): (1) loại 4 nên thay tab bốc-hạ bằng "Phân bổ chi phí" +
gate pickup foreign-only; (2) CostTable bổ sung cột Nhà cung cấp/Ghi chú/File; (3) giữ/gỡ dòng gợi
ý hạch toán. 3 việc này vượt scope "nhãn" nên KHÔNG tự dựng, chờ user duyệt.
Blocked: (không) — CHƯA commit/push (chờ user yêu cầu).

### Checkpoint — Cụm 1 XONG + VERIFY (08/10/2026)
Vừa hoàn thành: **Cụm 1 (khung động + loại 4) hoàn tất và verify đầy đủ** trên 127.0.0.1:3000.
- `importTypeConfig.js` (8 loại, chỉ 4 `supported:true`) + `ProductImportForm.vue` reworked xong:
  tab/cột/tiêu đề/gợi ý hạch toán ĐỘNG theo `cfg`; nút đổi phiếu nguồn (create-only); V2Footer +
  V2Base; số quốc tế; Duyệt + confirm popup; redirect về danh sách sau lưu.
- 2 fix quan trọng session này: (1) **supplier_price edit-mapping** — loadForEdit đọc thẳng BE value
  (gate canViewCostPrice), bỏ hard-code 0 → màn Sửa khớp màn Tạo (844,586 / 1,689,172);
  (2) **migration `companies.consignment_warehouse_ids`** — thiếu cột làm endpoint accounting-warehouses 500.
- Dọn em-dash `|| '—'` → `|| ''` ở form + 2 modal picker (ô rỗng để trống hẳn).
- 6 bước verify design-phase1.md §7 PASS; anomaly kho rỗng = artifact async, đã loại trừ.
Đang làm dở: (không) — Cụm 1 đóng.
Bước tiếp theo: **CHỜ USER NGHIỆM THU Cụm 1**. Sau khi OK → mở Cụm 2 (loại 2,15,99): BE
`buildDetailsByType`/`accumulateReturnedQtyByType`/`store()` + FE config 2,15,99 (bảng VAT biến thể B).
Blocked: (không) — đã có toàn quyền; CHƯA commit/push (chờ user yêu cầu).

### Checkpoint — Cụm 2 (loại 2,15,99) VERIFY XONG (08/10/2026)
Vừa hoàn thành: **Cụm 2 verify đầy đủ trên 127.0.0.1:3000 — PASS cả 3 loại.** BE đã có SẴN trọn bộ
từ trước (session này chỉ xác minh code + verify live, KHÔNG sửa BE):
- Gate `update()` (246-248) nhận 4/2/15/99; `buildDetailsByType` (1049-1051) route 2/15/99 về builder
  chung; `resolveAccountingService` (1178-1185) 2/15→DomesticPurchase, 99→Other; `domesticVatTypes` (2173)
  tính VAT per-line cho 2/15. FE `importTypeConfig.js` đã `supported:true` cho 2/15/99.
- **Loại 2 (Nhập hàng mua ngoài):** nguồn PYCNH-12183 → tạo nháp **PNH-12345** (type 2, status 3,
  is_import_direct=1, company 1, warehouse_id=NULL, product_import_request_id=12183, created_by=13):
  POST 200; 1 dòng `product_import_details` (product 47894, qty 2, FK `parent_id`); 1 dòng
  `product_import_detail_accountings` (detail 39545, accounting_warehouse_id 29 "Hà Nội - Nhập xuất thẳng",
  qty 2); **0 dòng journal** (nháp đúng). Mở lại /finance/product-imports/12345/edit: label/kho/SL "2 (2/2)"
  reload đúng (round-trip khép kín).
- **Loại 15 (Nhập hàng mua trong nước (TỰ DO + HÃNG)):** draft PNH-12344 (status 3) 0 journal; PI 12294
  (đã duyệt) `DomesticPurchaseProductImportAccountingService::build()` ra 7 dòng journal. Label khớp ERP.
- **Loại 99 (Nhập hàng khác):** render biến thể C đủ cột (Giá bán · Thành tiền giá bán · Giảm giá · Đơn giá
  sau giảm · Thành tiền sau giảm · VAT · Tiền VAT · Thành tiền sau VAT) + footer (Tổng tiền bán/trước thuế/
  VAT/sau thuế) khớp ERP `form.blade.php` 825-841 verbatim; `OtherProductImportAccountingService::build()`=[]
  (no-op tạo-tay). Render-only vì mọi nguồn đường-B loại 99 thuộc công ty 4 (user company 1 không lưu được).
- Nhãn 3 loại lấy đúng ERP, không bịa (yêu cầu label-fidelity).
Đang làm dở: (không) — Cụm 2 đóng.
Bước tiếp theo: **CHỜ USER NGHIỆM THU Cụm 2**. Sau khi OK → mở Cụm 3 (loại 11,3,9,14). KHÔNG tự bắt
đầu Cụm 3 khi user chưa xác nhận.
Blocked: (không) — đã có toàn quyền tự verify; CHƯA commit/push (chờ user yêu cầu).

---

## Rà soát ẩn/hiện toàn form (brainstorm lại theo ERP) — 09/10/2026

Sau khi user phản ánh "ẩn/hiện đơn giản vẫn sai", đã rà SOÁT TOÀN BỘ điều kiện show/hide của form
đối chiếu nguồn chân lý ERP (`ProductImport.blade.php` getters + `form.blade.php`). Kết quả chia 3
nhóm: (2) lỗi chắc chắn · (3) gap cần user quyết scope · (4) đúng. User duyệt sửa **nhóm (2)** trước.

### Nhóm (2) — Lỗi cột thừa + ô giá nhập tay (ĐÃ SỬA, chờ verify)
- [x] **Cột Giá bán/Giảm giá/VAT thừa ở loại 3, 14, 99** — ERP bảng mặc định (form.blade.php:829-836)
  gate toàn bộ nhóm này bằng `showListedPrice = type ∈ {4,9,13}`. Loại 3/14/99 ∉ → phải ẩn. Trước đây
  `importTypeConfig.js` để `sellingPrice/discount/vat = true` → sai. FIX: set cả 3 = false cho loại
  3, 14, 99 (loại 14 giữ `consignmentDeadline: true`).
- [x] **Ô "Giá nhập kho" loại 99 phải nhập tay** — ERP: 99 ∉ price_setted → form.blade.php:854
  `ng-if="!form.price_setted"` là `<input ng-model="product.supplier_price">`; BE store() nhánh else
  :648 lưu `$l['supplier_price']`. HRM trước đây hiển thị read-only + BE `buildDetailsFromSource`:2136
  luôn ghi đè từ nguồn. FIX:
  - BE `ProductImportService::buildDetailsFromSource()` — nhánh `type==KHAC(99)` lấy
    `$l['supplier_price'] ?? $reqProduct->supplier_price ?? 0`; loại khác giữ nguyên lấy-từ-nguồn.
  - FE `importTypeConfig.js` loại 99 thêm cờ cột `supplierPriceEditable: true`;
    `ProductImportForm.vue` thêm `cols.supplierPriceEditable` (gate kèm canViewCostPrice) + render
    `V2BaseCurrencyInput` thay ô read-only.
- [x] Verify Playwright 127.0.0.1:3000: loại 3/14/99 KHÔNG còn cột Giá bán/Giảm giá/VAT; loại 99 ô
  Giá nhập kho nhập tay được + Thành tiền nhập kho đổi theo. → PASS cả 3 loại (09/10):
  - Loại 99 (src 8914 "Nhập hàng khác"): headers = STT·Tên·Model·Mã·ĐVT·SL nhập kho·**Giá nhập kho·Thành tiền giá nhập kho**·Kho kế toán·Số lượng (KHÔNG Giá bán/Giảm giá/VAT); ô Giá nhập kho `hasInput=true` (V2BaseCurrencyInput), Thành tiền read-only.
  - Loại 3 (src 8900 "Nhập hàng mượn trả lại"): bảng Hàng hóa chỉ còn Giá nhập kho + Thành tiền (KHÔNG Giá bán/Giảm giá/VAT, KHÔNG Hạn gửi); tab = Hàng hóa + Phân bổ chi phí (đúng: KHÔNG có Chi phí nội địa vì has_inland_cost=false).
  - Loại 14 (src 8785 "Nhập hàng gửi"): headers giữ **Hạn gửi** đúng vị trí, KHÔNG Giá bán/Giảm giá/VAT; tab = Hàng hóa + Chi phí giao nhận hàng nội địa + Phân bổ chi phí.

### Nhóm (3) — Gap chờ user quyết scope

#### (3.1) Cờ-theo-bản-ghi của bảng DEFAULT — USER DUYỆT option 2 (làm cả 3) 09/10/2026
Nguồn chân lý ERP `ProductImport.blade.php`: `has_rebate_price` (dòng 70-72) · `is_settlement`
(74-76) · `showListedPrice` (374-377). Cả 3 phụ thuộc quan hệ phiếu NGUỒN
(`product_import_request.product_export_request.type/settlement` + `borrow_sell_request.contractable_type/settlement`).
Dựng CHUNG 1 đường ống BE phơi thuộc tính nguồn, rồi 3 cột gate theo bản ghi.

- [x] **BE đường ống**: helper CHUNG `ProductImportService::deriveRecordFlags($pir)` (service:1514) trả
  `has_rebate_price` / `is_settlement` / `source_export_type`. Gắn vào CẢ 3 source path:
  `getWarehouseImportSource` (đường A, service:1659-1661) · `ProductImportRequestDetailResource` (đường B,
  :81-83) · `ProductImportDetailResource` (Edit, :128-130). `settlement` tính từ firm_contract.status ==
  `FIRM_CONTRACT_DA_QUYET_TOAN(10)` (KHÔNG phải cột DB); `has_rebate_price` = per.type ==
  `XUAT_BD_SC(17)` HOẶC borrow_sell `contractable_type == CONTRACT_WR_SERVICE`. ⚠️ PHP 7.4 không
  spread mảng string-key → tính ra biến `$recordFlags` rồi liệt kê 3 key tường minh.
- [x] **FE cột Chiết khấu** (`has_rebate_price`): cột MỚI `rebate_price` sau "Giá niêm yết", trước
  "Giá bán". Gate `cols.rebatePrice = canViewCostPrice && header.has_rebate_price`. Label "Chiết khấu"
  (ERP :828/:872). ✅ Playwright: PYCNH-00176 (per.type 17) hiện cột, is_settlement=false nên KHÔNG
  hiện mua duyệt.
- [x] **FE 2 cột mua duyệt** (`is_settlement`): "Đơn giá mua duyệt" (`price_buy`) + "Thành tiền mua
  duyệt" (`amount_price_buy`) sau nhóm VAT, trước "Hạn gửi". Gate `cols.settlementPrices`. Label ERP
  :837-838/:881-882. ✅ Playwright: PYCNH-00087 (fc.status 10) hiện 2 cột, per.type 14≠17 nên KHÔNG
  hiện Chiết khấu.
- [x] **FE tinh chỉnh `showListedPrice`**: `cols()` thêm `narrowListed` — loại 4/9 chỉ hiện nhóm Giá
  bán/Giảm giá/VAT khi `source_export_type ∉ {2,8}`; loại khác → true (không ảnh hưởng). ⚠️ Không có
  dữ liệu thật loại 4/9 nguồn-xuất ∈{2,8} (query rỗng) → port phòng thủ đúng ERP, hiện tại luôn trơ
  (mọi bản ghi 4/9 có per.type ∉{2,8} → nhóm vẫn hiện, đã xác nhận ở 176/87/213).
- [x] **Verify Playwright** 127.0.0.1:3000: PYCNH-00176 (Chiết khấu) · PYCNH-00087 (2 cột mua duyệt) ·
  PYCNH-00213 (cả 2 cờ false → regression: nhóm Giá bán nguyên vẹn, không cột mới). Edit: form chặn
  bởi gate status/ownership (status=1, không phải DANG_TAO=3) nên không render được form với dữ liệu
  có cờ; đã xác minh RESOURCE Edit `ProductImportDetailResource(12165)` trả đúng
  `{has_rebate_price:true, is_settlement:false, source_export_type:17}` = input mà `loadForEdit` đọc
  (cùng cols()/template chung đã verify ở Tạo).

#### (3.2) Còn lại — KHẢO SÁT 09/10/2026 (khác hẳn 3.4: MỌI tab đều cần BE mới + quyết định nghiệp vụ)
- [x] ~~Field header có điều kiện (mã/ngày HĐ quyết toán cho 4/9; field riêng loại 11)~~ → làm ở (3.3)
  (trừ field riêng loại 11 + nút mở rộng vẫn chờ, gộp cùng tab chi phí ngoại loại 11).

**Khảo sát ERP (6 pane) + BE/FE HRM — vì sao 3.2 ≠ 3.4:** 3.4 chạy được vì BE đã serialize sẵn
`tabs` (chỉ-đọc). 3.2 thì BE port CỐ Ý dừng ở MỌI tab:
- **"Chi phí HĐ" loại 2/15** (ERP pane :1055, EDITABLE, cột: STT · Chi phí(select `available_types`) ·
  Giá trị trước VAT(VNĐ)(*) · %VAT · VAT · Giá trị sau VAT(VNĐ) · xoá; **KHÔNG** NCC/Ghi chú/File,
  **KHÔNG nút Thêm**; rows pre-fill `form.contract_costs` + per-row `can_edit`).
  - BE lưu/validate/recompute ĐÃ có (`syncCostsByType(HOP_DONG_MUA=4)` :2157; `contract_costs.*`
    :94-98; `recomputeMoneyServerSide` phân bổ type 4 → `contract_cost_allocation` :2661-2729).
  - **THIẾU**: builder create KHÔNG pre-fill `contract_costs` (chỉ đặt allocation=0 tạm); không có
    nguồn `available_types`/`can_edit` từ HĐ mua. Làm ĐÚNG ERP ⇒ cần BE build contract_costs từ
    HĐ nguồn. Nếu cho user tự Thêm dòng ⇒ lệch ERP ("không bịa") → **quyết định nghiệp vụ**.
  - FE `CostTable` có sẵn nhưng dư 3 cột (NCC/Ghi chú/File) + cần biến thể ẩn chúng cho tab này.
- **"Phân bổ hàng giữ" loại 2/15/11** (ERP pane :1715/1913/2034, EDITABLE: SL giữ `d.qty` + Hạn giữ
  `d.expire_prepick_date`, checkbox `allocation` disabled; nguồn `form.need_allocation_products` +
  nested `customer_allocations`). **BE KHÔNG có** `need_allocation_products`/`customer_allocations`;
  validate chỉ có `lots.*.expire_prepick_date` (1 mức/lô, loại 14). ⇒ cần subsystem BE mới (tính
  hàng cần giữ theo YC khách + ghi prepick hold lúc hoàn thành) = mini-feature riêng.
- **Cụm loại 11 (5 tab)**: Chi phí HĐ ngoại(:1027 RO, `invoice2.costs`) · Chi phí quốc tế có/không
  thuế(:1115/:1168 RO, `foreign_costs`/`foreign_costs_not_tax`) · Tính giá thành nhập kho(:1487 RO,
  loạt `order_import_request.*`) · Giao hàng nhanh(:1845 RO, `fast_deliveries`). BE docblock ghi rõ
  **QUOC_TE/NCC CHƯA port**; không serialize `order_import_request`/foreign/landed-cost/fast-delivery.
  ⇒ cần BE serialize toàn bộ khối này (+quyết định có port QUOC_TE không) = mini-feature lớn nhất.
  (Chi phí bốc hạ :1377 thì HRM ĐÃ render qua tab `pickupCost`.)

→ KẾT LUẬN: 3.2 không phải "thêm tab FE" mà là 3 mini-feature BE+FE, mỗi cái cần quyết định nghiệp
vụ. ĐÃ báo user 09/10/2026, chờ chọn hướng/thứ tự. KHÔNG tự dựng UI rỗng (fail-closed, không bịa).

##### (3.2-①) Tab "Chi phí HĐ" loại 2/15 — USER CHỌN Hướng A 09/10/2026 (XONG ✅ — chờ nghiệm thu)
**Hướng A** (user chốt "A"): BE tự DỰNG `contract_costs` từ HĐ mua nguồn = các dòng `ImportCost`
type=4 (HOP_DONG_MUA) của chính Phiếu YC nhập hàng nguồn — ĐÚNG ERP (`set product_import_request`
tách `costs` → `contract_costs` theo type 4; pane :1055 rows editable, `can_edit`=true, KHÔNG nút Thêm).
Nguồn dữ liệu ĐÃ XÁC NHẬN có thật: `erp_hrm_check` có 43 dòng `import_costs` type=4 trên các YCNH loại 2/15.
- BE lưu/validate/recompute ĐÃ có từ Cụm 2 (Store+Update validate `contract_costs.*`; `syncCostsByType(HOP_DONG_MUA=4)` :2157; recompute :2661). Chỉ còn phần ĐỌC/PRE-FILL:
- [x] BE: `ProductImportRequest::contractCosts()` — reader type=4, mirror `inlandCosts()` (:364) (join customers lấy supplier_name).
- [x] BE: `ProductImportRequestDetailResource` +`'contract_costs'` (đường B — `finance/product-import-requests/{id}` dùng ở create + applyHeaderDisplayFromSource). Ungated giống `inland_costs` sibling; FE fail-close.
- [x] BE: `getWarehouseImportSource()` (đường A) +`'contract_costs'` từ `$sourcePir->contractCosts()`, gate `$canViewCostPrice` (giống cột giá SP trong method này).
- [x] FE `importTypeConfig.js`: thêm `'contractCost'` vào `tabs` loại 2/15 — ĐỨNG TRƯỚC `inlandCost` (ERP nav :597 "Chi phí HĐ" trước "Chi phí giao nhận hàng nội địa").
- [x] FE `CostTable.vue`: prop `variant` ('full' mặc định | 'contract'); 'contract' ẩn 3 cột NCC/Ghi chú/File (header + ô + colspan empty-row). Giữ nút xoá dòng (ERP `can_edit`=true).
- [x] FE `ProductImportForm.vue`: data `contractCosts:[]`; tab `<b-tab v-if="hasTab('contractCost') && canViewCostPrice" title="Chi phí HĐ">` (KHÔNG nút Thêm) + `<CostTable variant="contract" :rows="contractCosts" @remove="removeCostRow('contract',$event)"/>`; prefill 3 path (loadFromRequest/loadFromWarehouseImport `src.contract_costs`; loadForEdit `d.costs` type===4); `addCostRow`/`removeCostRow` nhận 'contract'; `buildFormData` append `contract_costs[]`; `unsavedSnapshotSource` +contractCosts.
- [x] Nhãn NGUYÊN VĂN ERP: tab "Chi phí HĐ"; cột STT · Chi phí · Giá trị trước VAT (VNĐ) (*) · %VAT · VAT · Giá trị sau VAT (VNĐ).
- [x] Verify Playwright 127.0.0.1:3000 ✅ (KHÔNG commit/push):
  - **Create đường B** (PNH-create `?product_import_request_id=12031`, loại 2): tab "Chi phí HĐ" ĐỨNG TRƯỚC
    "Chi phí giao nhận hàng nội địa"; pre-fill 1 dòng từ YCNH nguồn: Chi phí=Vật tư lắp đặt thiết bị (cost_id 43),
    Giá trị trước VAT=19,200,000, %VAT=8, VAT=1,536,000, Giá trị sau VAT=20,736,000; cột đúng 7 cột ERP
    (KHÔNG NCC/Ghi chú/File); CÓ nút xoá dòng; KHÔNG nút "Thêm chi phí". Khớp reader tinker.
  - **Edit** (PNH-12345 loại 2, draft status=3 của chính user): tab "Chi phí HĐ" render đúng cột + empty-row
    "Chưa có chi phí" (phiếu này chưa có cost type 4), KHÔNG nút Thêm — loadForEdit `d.costs` type===4 chạy.
  - **Payload** (POST product-imports, bắt Network): `contract_costs[0][cost_id]=43`,
    `[value_before_vat]=19200000`, `[vat_percent]=8`, `[supplier_id]/[note]/[attachment]` rỗng → buildFormData đúng.
    422 chỉ do `lots.0.acc_warehouses` (nguồn 12031 thiếu kho kế toán, KHÔNG liên quan contract_costs) → validation
    `contract_costs.*` PASS sạch; không ghi bản ghi nào (422 rollback).

#### (3.3) Field header ẩn/hiện của "Thông tin chung" — USER DUYỆT "làm cả" 09/10/2026
Nguồn ERP: `warehouse/product_imports/form.blade.php` tab `#chung` (dòng 34–309). User báo header
HRM thiếu nhiều field ẩn/hiện, ví dụ loại 4/9 phải hiện khối Tài khoản hạch toán. Scope = 3 cụm:
(a) khối Tài khoản hạch toán (read-only, số TK cứng); (b) Hợp đồng + Ngày xuất khi quyết toán
(type∈{4,9} && is_settlement); (c) trường Nhà cung cấp. **Loại 11 vẫn để ở 3.2** (kéo theo tab chi phí ngoại).
- [x] BE `deriveRecordFlags()` +2 khóa `settlement_contract_code`/`settlement_export_date`
  (type4: firm_contracts.code + product_exports.approved_time; type9: firm_contracts.code + bsr.created_at, d/m/Y).
- [x] BE `getWarehouseImportSource()` (đường A): +`supplier_name` (wi.supplier_id) +2 khóa settlement.
- [x] BE `ProductImportRequestDetailResource` (đường B): +2 khóa settlement (supplier_name đã có :35).
- [x] BE `ProductImportDetailResource` (Sửa): +`supplier_name` (sourcePir/wi) +2 khóa settlement.
- [x] FE header default +3 field; 3 load path gán (loadFromWarehouseImport/loadFromRequest/loadForEdit +
  applyHeaderDisplayFromSource cho supplier_name); kv-grid +Nhà cung cấp/Hợp đồng/Ngày xuất (nhãn nguyên văn ERP).
- [x] FE computed `isSettlementHeader` + `accountRows` theo type (2/4/9/11) + render khối `.acc-block` sau Ghi chú.
- [x] Verify Playwright 127.0.0.1:3000 ✅:
  - Loại 4 quyết toán (pir#11328): Hợp đồng=HĐ_TPE_HN_KD1_26_0631_MitsuBacGiang, Ngày xuất=24/06/2026,
    khối TK 5212/1561/632/5211/5213/33311.
  - Loại 9 quyết toán (pir#11689): Hợp đồng, Ngày xuất=06/07/2026, TK kho=157 (khác loại 4).
  - Loại 2 (pir#12220): Nhà cung cấp hiện, khối TK 4 dòng 3311/1561/1331/1562, KHÔNG Hợp đồng/Ngày xuất.
  - Loại 3 (pir#12213, loại thường): ẩn hết khối TK + Hợp đồng/Ngày xuất + NCC.

#### (3.4) Tab "nhóm HĐ hãng" (firm_contract tabs) cho loại 4/9 — USER yêu cầu 09/10/2026
User: "ở loại 4,9 hình như bên erp sẽ có tab nhóm đối với hd hãng cái này tôi không thấy có".
ERP `form.blade.php`: sau tab "Hàng hóa" render `ng-repeat="tab in form.tabs"` (nav :591-596) +
tab-pane bảng CHỈ-ĐỌC (:983-1026, `ng-if type∉{1,2,11,12}`). 1 phiếu gom hàng từ nhiều HĐ hãng →
mỗi HĐ/nhóm 1 tab. `contract_product` = getter FE khớp dòng hàng CHÍNH theo (product_id, unit_id).
Cột (nhãn NGUYÊN VĂN ERP): STT · Tên hàng hóa · Model · Mã hàng hóa · Đơn vị tính · SL nhập kho ·
Giá nhập kho (VNĐ) · Thành tiền giá nhập kho (VNĐ) · [showListedPrice] Giá niêm yết · Giảm giá ·
Giá bán · Thành tiền giá bán · [is_settlement] Đơn giá mua duyệt · Thành tiền mua duyệt.
- [x] BE: entity `ProductImportRequestTab`(+TabProduct), `WarehouseImportTab`(+TabProduct),
  `ProductImportTab`(+TabProduct) đã có sẵn (extends Model, $timestamps=false, $guarded=['*']).
- [x] BE: `ProductImportRequest::tabs()` (:455) + `WarehouseImport::tabs()` + `ProductImport::tabs()` (:202) — hasMany parent_id.
- [x] BE: helper `ProductImportService::serializeTabsForForm()` (name + products[product_id,unit_id,qty] qty>0;
  `->values()->all()` để products ra PLAIN array, filter tab rỗng).
- [x] BE đường B: `findForShow` eager `tabs.products` + `ProductImportRequestDetailResource` trả `tabs` (:173-177).
- [x] BE đường A: `getWarehouseImportSource()` trả `tabs` (wi.tabs()->with('products')).
- [x] BE Sửa: `ProductImportDetailResource` trả `tabs` (service `getData` đã load `tabs.products` :1026).
- [x] FE: `tabs:[]` data + 3 load path gán (loadFromWarehouseImport/loadFromRequest/loadForEdit);
  computed `visibleTabs` (ẩn type 1/2/11/12) + `tabShowListed` (canViewCostPrice + type∈{4,9,13} +
  source_export_type∉{2,8}) + `tabSettlement` (canViewCostPrice + is_settlement) + `tabColCount`;
  methods `tabContractProduct(tp)` (khớp rows pid+unit) / `tabDiscountPrice` / `tabTotalAmountAfterExtra`;
  render `<b-tab v-for="fcTab in visibleTabs">` sau "Hàng hóa" bảng chỉ-đọc nhãn nguyên văn ERP
  (cột cost gate `cols.supplierPrice`, listed gate `tabShowListed`, settlement gate `tabSettlement`).
- [x] Verify Playwright 127.0.0.1:3000 ✅:
  - đường B PIR 12230 (loại 4): tab "Nhóm 1" render 3 dòng, cột đúng thứ tự ERP (Giá niêm yết→Giảm
    giá→Giá bán→Thành tiền giá bán), giá trị khớp dòng CHÍNH theo (pid,unit) — KEG-500 SL2 Giá nhập
    59,634,465 / TT 119,268,929 / niêm yết 105,000,000 / giảm 15,750,000 / bán 105,000,000 / TT bán 210,000,000.
  - đường A WI 8902 (loại 4): tab "Nhóm 1" render 3 dòng, giá trị khớp dòng CHÍNH (32,464,837 / 211,156 / 219,602).
  - Sửa PI 12308: form chặn bởi gate `canEdit` (status=1 Đã hoàn thành ≠ DANG_TAO=3; MỌI phiếu có
    tab đều status 1) → không render được form. Đã xác minh RESOURCE Sửa `ProductImportDetailResource(12308)`
    trả `tabs:[{firm_contract_tab_id:34450,name:"Nhóm 1",products:[{product_id:5300,unit_id:41,qty:"2.00"}]}]`
    = input `loadForEdit` đọc (cùng visibleTabs/template đã verify ở A/B).
