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
### Checkpoint — ②a "Phân bổ hàng giữ" (loại 2/15) XONG + VERIFY end-to-end (09/10/2026)
Vừa hoàn thành: mini-feature ②a (mirror FORM ERP, KHÔNG đụng pool hàng giữ). BE + FE đã code từ phiên trước;
phiên này **verify trọn vòng lưu** qua pipeline HTTP thật (mint JWT emp13 + curl, vì replay qua axios trình duyệt
bị 401→logout; FormRequest của PUT không parse multipart nên dùng POST `_method=PUT` như FE).
- **Render (đã verify phiên trước):** tab hiện đúng loại 2/15; nhãn lấy CHÍNH XÁC từ ERP (loại 15: "SL nhập"/"SL báo hàng về";
  loại 2: "SL"/"SL yêu cầu"); rowspan nhiều khách; "SL giữ" disabled + cột "Hạn giữ"/"Cần giữ" ẩn khi is_import_direct=1.
- **Store (POST):** phiếu nguồn hợp lệ phải `status=2 (CHO_DUYET)` + `is_import_direct=1` + loại 2/15 + cùng company người đăng nhập
  (bẫy: req 12208 có is_import_direct=0 → `canProductImport()` false → "Không đủ quyền!"; đổi sang req 12204). Tạo PNH-12353:
  `product_import_detail_customers` 12215→12217 (+2 khách), parent_id=detail mới, đủ 3 FK inland (bc/orq/arr), allocation/expire đúng.
- **Update (POST _method=PUT):** xoá+dựng lại dòng khách (12229/30→12231/32); khách allocation=0 → expire_prepick_date tự NULL;
  khách allocation=1 → lưu ngày mới. Tổng giữ 12217 (xoá 2 + chèn 2).
- **②b KHÔNG kích hoạt:** lưu nháp (status 3) nên `handleCompleted()` không chạy; `prepick_details`=0 cho dòng khách mới.
- **Dọn test:** đã xoá sạch PNH-12353 + con (detail_customers/accountings/details/import) → baseline khôi phục (det_cust=12215, max import=12345).
Đang làm dở: (không) — ②a hoàn tất, CHƯA commit/push (chờ user yêu cầu).
Bước tiếp theo: chờ user nghiệm thu ②a; ②b (ghi pool hàng giữ) vẫn GATE RIÊNG, cần user duyệt riêng.
Blocked: (không)

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

##### (3.2-②a) Tab "Phân bổ hàng giữ" loại 2/15 — USER CHỌN Hướng A phân-kỳ 09/10/2026 (ĐANG LÀM)
**Bối cảnh:** mini-feature "Cụm hàng cần giữ" (mục 3.2 phân tích ở trên). User chốt phân kỳ: **làm ②a NGAY**
(mirror FORM: nhập SL giữ + Hạn giữ, lưu `product_import_detail_customers`), **GATE ②b riêng** (ghi prepick
hold lúc hoàn thành — chưa duyệt). ②a **TUYỆT ĐỐI không đụng pool hàng giữ** (`prepick_details`/`prepick_logs`).

**Phát hiện cốt lõi (ĐÃ xác minh session này):**
- Dòng "hàng cần giữ" của ERP là **construct CLIENT-SIDE** (`need_allocation_products`/`customer_allocations`
  trong AngularJS), KHÔNG phải bảng server. `customer_allocations` = `lot.customers` lọc `type∈{1,3}` khi
  `!is_import_direct`, chỉ cho loại {11,15,2}. `rowspan = customer_allocations.length`.
- Nguồn dòng khách: đường B qua `ProductImportRequestDetail::details` (bảng `product_import_request_detail_customers`);
  đường A qua `WarehouseImport...->details`. Cả 2 ERP loader alias **`qty as order_qty`** → `order_qty` = `qty` nguồn.
- Ngữ nghĩa cột-khách: `order_qty`=SL khách yêu cầu (chỉ đọc); `qty`/`_qty`=**SL giữ** (sửa được, mặc định = order_qty,
  clamp ≤ min(order_qty, SL khả dụng)); `allocation`=checkbox "Cần giữ" (mặc định true nếu qty>0 — **DISPLAY-ONLY** trong form);
  `expire_prepick_date`=Hạn giữ (mặc định `now + max_prepick_date` ngày, config mặc định 10; disabled khi !allocation; ẩn khi is_import_direct).
- **Dữ liệu `allocation`/`expire_prepick_date` KHÔNG có trên `product_import_request_detail_customers`** (bảng nguồn thiếu
  4 cột order_qty/customer_code/allocation/expire_prepick_date) → create: FE tự tính default; edit: ĐỌC từ
  `product_import_detail_customers` (bảng NÀY có đủ order_qty/qty/allocation/expire_prepick_date/customer_code + FK pass-through).
- **Giảm có chủ đích (KHÔNG bịa):** cột "Kinh doanh" ERP hiện chuỗi inland sâu (order_request/NV/phòng + expand
  Tên khách/Ngày cần/Ghi chú) — các entity inland đó CHƯA port sang HRM Finance → HRM chỉ hiện `customer_code + customer_name`.

**Nhãn NGUYÊN VĂN ERP (form.blade.php type-15 :1913, type-2 :2034) — KHÁC NHAU theo loại:**
- Loại 2: STT · Tên hàng hóa · ĐVT · **SL** · Kinh doanh · **SL yêu cầu** · SL giữ · Hạn giữ (*) · [Cần giữ]
- Loại 15: STT · Tên hàng hóa · ĐVT · **SL nhập** · Kinh doanh · **SL báo hàng về** · SL giữ · Hạn giữ (*) · [Cần giữ]
  (cột "SL" loại 2 / "SL nhập" loại 15 = SL dòng hàng CHÍNH; "SL yêu cầu"/"SL báo hàng về" = `order_qty` dòng khách)

**Tasks ②a:**
- [x] BE: entity `Modules/Finance/Entities/ProductImport/ProductImportDetailCustomer.php` (table `product_import_detail_customers`,
  extends Model, $fillable đủ cột persist, `parent()` belongsTo(ProductImportDetail,'parent_id'), `customer()` belongsTo(Supplier,'customer_id')).
- [x] BE: `ProductImportDetail` +`customers()` hasMany(ProductImportDetailCustomer,'parent_id','id').
- [x] BE: `ProductImportRequestDetailCustomer` +`customer()` belongsTo(Supplier,'customer_id') (lấy `code`).
- [x] BE: EDIT resource `ProductImportDetailResource` +khối `customers` mỗi SP (id, customer_id, customer_name,
  customer_code, order_qty, qty, allocation, expire_prepick_date format Y-m-d, type); +`'products.customers'` vào `loadDetail()`.
- [x] BE: đường-B resource `ProductImportRequestDetailResource` khối `customers` (:148-160) +order_qty(=`$customer->qty`),
  +customer_code(=`optional($customer->customer)->code`), +product_id, +3 FK inland pass-through; đảm bảo eager `details.customer`.
- [x] BE: đường-A `getWarehouseImportSource()` +dòng khách (mirror `qty as order_qty`), gate `$canViewCostPrice`.
- [x] BE: Store/Update validate +`lots.*.customers` (customers=nullable|array; customers.*.qty=required|numeric;
  customers.*.expire_prepick_date=required_if customers.*.allocation,1|nullable|date|after:today) mirror ERP store :293 / update :1029.
- [x] BE: lưu `lots[].customers[]` vào `product_import_detail_customers` trong `buildDetailsFromSource` sau :2373
  (mirror ERP :696-726), CHỈ loại 2/15; +xoá dòng khách cũ theo product_import_id lúc update gần :308 (mirror ERP :1283). KHÔNG ghi pool.
- [x] FE: `importTypeConfig.js` +tab key `holdAllocation` + nhãn theo loại; `ProductImportForm.vue` +`<b-tab title="Phân bổ hàng giữ">`
  + component mới (layout rowspan nhiều khách, nhãn đúng loại, "Cần giữ" display-only, "Hạn giữ" sửa được disabled khi !allocation)
  + prefill 3 path + `buildFormData` append `lots[].customers[]`.
- [x] Verify Playwright 127.0.0.1:3000. KHÔNG commit/push.

**②b (CHƯA DUYỆT — GATE RIÊNG):** ghi prepick hold lúc `handleCompleted()`, mở rộng `PrepickStockService.addLot()` cho
objectable `App\Model\Warehouse\ProductImportDetailCustomer`, dry-run trước. Cần confirm riêng của user.
→ ②b XONG + dry-run PASS 09/10/2026 (xem block "Regression màn Phiếu xuất giữ" ở trên). CHƯA commit/push.

##### (3.2-③) Cụm loại 11 — tab chi phí NGOẠI (READ-ONLY) — USER CHỌN "chi phí trước" 09/10/2026 (ĐANG LÀM)
**Bối cảnh:** loại 11 phần hàng-hóa + money (`buildDetailsForeignPurchase`/`recomputeMoneyForeign`) + hạch toán
ForeignPurchase + tab bốc-hạ (`pickupCost`) ĐÃ xong ở "Cụm 3". Còn lại = 4 tab chi phí **chỉ-đọc** mà BE
CỐ Ý chưa serialize (`ProductImportService::COST_TYPE_QUOC_TE`; ghi chú "QUOC_TE/NCC chưa port"). User chốt
thứ tự: **4 tab chi phí TRƯỚC**, "Tính giá thành nhập kho" (landed cost, đọc `order_import_requests.sum_*`) LÀM SAU.

**Nguồn dữ liệu đã xác minh trên `erp_hrm_check`:** chuỗi `product_imports(type=11)` → `product_import_requests.order_import_request_id`
→ `order_import_requests` (có `invoice2_id`, `sum_supplier_cost`, `sum_foreign_cost_with_tax`, `sum_foreign_cost_not_tax`,
`sum_inland_cost`, `exchange_rate`). 628 phiếu loại 11; 128 OIR có `invoice_cost2`. Mẫu: PNH-12255→PIR12193→OIR644→invoice2#683→invoice_cost2#555.
- `invoice2.costs` = bảng **`invoice_cost2`** {invoice2_id, cost_id, name, value, annex_addition_json, attachment}.
- `fast_deliveries` (bảng cùng tên) có `purchase_invoice_id` — nguồn thật cho loại 11 CHỜ agent xác nhận (nhiều biến thể *_fast_deliveries).
- `foreign_costs` / `foreign_costs_not_tax`: KHÔNG có bảng cùng tên — CHỜ agent map (có thể treo trên invoice2/order_import_request).

**Nhãn + cột NGUYÊN VĂN ERP (form.blade.php, 4 pane đều `disabled`=read-only):**
- Nav (`ng-if="form.is_foreign"`): "Chi phí HĐ" (:600, dùng chung id `#chi_phi_HD` nhưng pane RIÊNG cho foreign :1027) ·
  "Chi phí quốc tế có tính thuế nhập khẩu" (:606) · "Chi phí quốc tế không tính thuế nhập khẩu" (:612) · "Giao hàng nhanh" (:1845).
- **Chi phí HĐ (foreign, :1027)** — 3 cột: STT · **Tên chi phí** · **Giá trị** (value + dòng "Hợp đồng: {contract_value|number}"
  + mỗi phụ lục "**Phụ lục {code}:** {value|number}"). Nguồn `order_import_request.invoice2.costs[]`. Empty "Không có chi phí".
- **Chi phí quốc tế có tính thuế nhập khẩu (:1115)** — 8 cột: STT · **Tên chi phí** · **Giá trị** · **Đơn vị tiền** ·
  **Tỉ giá** · **Giá trị (VNĐ)** · **Nhà cung cấp** · **File đính kèm**. Nguồn `foreign_costs[]`
  {cost_id→name, value, currency, exchange_rate, exchanged_value, supplier_id, attachment}. Empty "Không có chi phí".
- **Chi phí quốc tế không tính thuế nhập khẩu (:1168)** — 11 cột: STT · **Tên chi phí** · **Giá trị** · **Đơn vị tiền** ·
  **Tỉ giá** · **Giá trị (VNĐ)** · **VAT**[**%** | **Số tiền**] · **Giá trị sau VAT (VNĐ)** · **Nhà cung cấp** · **File đính kèm**.
  Nguồn `foreign_costs_not_tax[]` {cost_id→name, value_before_vat, currency_id, exchange_rate, exchanged_value, vat_percent, vat_cost, value, supplier_id, attachment}. Empty "Không có chi phí".
- **Giao hàng nhanh (:1845)** — bảng rowspan lồng, 8 cột: STT · **Người chịu phí** ({employee_code} - {employee_name}) ·
  **Khách hàng** ({customer_code} - {customer_name}) · **Chi phí theo khách hàng** · **File đính kèm** · **Hàng hóa**
  ({product_code} - {product_name}) · **Phương thức giao hàng** (shipping_methods) · **Tổng chi phí ({currency})**.
  Nguồn `fast_deliveries[]{amount, employee_*, customers[]{customer_*, amount, attachment, products[]{product_*, method}}}`. Empty "Không có chi phí".

**Tasks ③ (chi phí trước):**
- [x] BE: xác định nguồn `invoice_contract_costs`/`foreign_costs`/`foreign_costs_not_tax`/`fast_deliveries` loại 11 → 4 reader trên Entity `ProductImportRequest` (09/10/2026). Nguồn CHỐT: `invoice_contract_costs`=`invoice_cost2` (qua OIR.invoice2_id, `contract_value=value−Σannex`); `foreign_costs`=`import_costs` type1 calc_tax1 (exchanged=value×rate); `foreign_costs_not_tax`=`import_costs` type1 calc_tax0 (exchanged/vat/value tính lại); `fast_deliveries`=`buy_contract2_fast_deliveries`→`_customers`→`_customer_products` (qua OIR.buy_contract2_id + phụ lục đầu, lọc theo product_id nhập). ⚠️ `import_costs` dùng FK `product_import_request_id` (KHÔNG `order_import_request_id` như ERP). Verify tinker DB thật: PIR9760 (3 foreign+1 notax+1 invoice cost), PIR9889 (2 fast_deliveries, filter product_id drop đúng).
- [x] BE: serialize 4 khối vào nguồn form — `getWarehouseImportSource:1790` (đường A) + `ProductImportRequestDetailResource` (đường B, thêm `use ChecksEmployeePermission`) + `ProductImportDetailResource` (Edit, đọc LIVE từ source PIR), gate `canViewCostPrice && type===11` fail-close. `php -l` sạch cả 4 file.
- [x] FE: `importTypeConfig.js` loại 11 thêm tab keys chi phí ngoại (đúng thứ tự nav ERP: `invoiceContractCost`→`foreignCostTax`→`foreignCostNotTax`→`inlandCost`→`pickupCost`→`fastDelivery`); `ProductImportForm.vue` 4 `<b-tab>` read-only (V2BaseTableScroll + table bordered) render 4 bảng nhãn NGUYÊN VĂN ERP, gate `canViewCostPrice`; wiring qua `setForeignCostBlocks()` ở cả 3 load path (WarehouseImport/Request/Edit); helper `shippingMethodName`+`fastDeliveryRowSpan`.
- [x] Verify Playwright 127.0.0.1:3000 trên phiếu loại 11 có dữ liệu thật (09/10/2026, KHÔNG commit/push): PIR 9760 — tab "Chi phí HĐ" (Phí đóng gói 2 + "Hợp đồng: 2"), "Chi phí quốc tế có tính thuế NK" (3 dòng, 8 cột, `61,305,600` chuẩn QT), "Chi phí quốc tế không tính thuế NK" (header gộp VAT %/Số tiền rowspan/colspan, Phí tại cảng 8,042,240→VAT 8%→8,685,619, scroll 2 chiều). PIR 9889 — fastDelivery "Không có chi phí" (ĐÚNG: product nhập 5022/43731 không khớp product fast-delivery 8315/37550 → filter `filterFastDeliveriesByProductIds` loại hết). PIR 2306 — fastDelivery 8 cột đủ, rowspan NV/KH/Tổng chi phí qua 3 dòng hàng hoá, `Hàng không` (method=1), `21,775` formatMoney. Nhãn tab khớp ERP `form.blade.php:650` verbatim. Dev-mode console "errors" chỉ là HMR reexport warnings (vô hại).
**Tasks ④ (Tab A — "Tính giá thành nhập kho" / landed cost, ERP `#phan_bo` type 11, CHỈ-ĐỌC) — 09/10/2026:**
- [x] BE: `ProductImportRequest::landedCostSummary()` — 4 ô tổng OIR (exchange_rate, sum_supplier_cost, sum_foreign_cost_with_tax, sum_foreign_cost_not_tax) từ `order_import_requests`, `[]` nếu không có `order_import_request_id`.
- [x] BE: serialize `landed_cost_summary` ở CẢ 3 load path — `ProductImportDetailResource` (Edit, :330) + `ProductImportRequestDetailResource` (đường B) + `getWarehouseImportSource()` (đường A), gate `$isForeign && $canViewCostPrice` fail-close. Per-SP (`amount_after_vat`/`foreign_cost_not_tax`/`inland_allocation`/`pick_up_cost`/`total`/`import_price`) đã serialize sẵn trong Edit path (tính lúc store, LƯU trên `product_import_details`); đường A/B chưa có → chỉ summary + empty-state. `php -l` sạch 4 file BE.
- [x] FE: `importTypeConfig.js` loại 11 thêm key `landedCost` (sau `pickupCost`, trước `fastDelivery`); `ProductImportForm.vue` thêm `<b-tab>` read-only: 6 ô tổng hợp (4 từ `landedSummary` + `totalInlandCostBeforeVat()`/`sumPickUpCost()` LIVE) + bảng 15 cột (STT·Model·Code đặt hàng·Hàng hóa·ĐVT·SL·Đơn giá·Thành tiền·GT sau thuế NK·VAT[%|Giá trị]·CP quốc tế không thuế·CP nội địa·CP tại kho·GT nhập kho·Đơn giá nhập kho) từ `landedRows`, + totals row (colspan5 "Tổng cộng", Đơn giá/Thành tiền/VAT% blank) + empty-state. Nhãn nguyên văn ERP `form.blade.php:1487-1604`. Data: `landedSummary`/`landedRows`/`landedTotals()`/`formatNum4()`; wiring `landedSummary` ở `setForeignCostBlocks()` (3 path), `landedRows` map trong `loadForEdit()` gate `canViewCostPrice` (exchanged_price=supplier_price×rate, total_exchanged_price=×qty×rate; all_barcodes HRM chưa serialize → blank). CSS `.landed-sum__label/__value/.landed-sub`. Template compile sạch (vue-template-compiler).
- [x] Verify Playwright 127.0.0.1:3000 phiếu loại 11 có data thật (09/10/2026, KHÔNG commit/push): PNH-12178 (32 SP, foreign_cost_not_tax>0). Edit view bị `canEdit()` chặn (status≠DANG_TAO) → toggle tạm status=3+created_by=13 trên DEV DB, verify, ĐÃ REVERT về 1/207. BE contract xác thực qua `GET show` (cùng Resource) với token thật: landed_cost_summary 4 giá trị, 32 SP đủ field landed, all_barcodes vắng (→blank ĐÚNG). UI: 6 ô tổng đúng (26,111 / 1,305,550 / 1,362,786 / 7,152,080 / 10,057,504 / 0), 15 cột render chuẩn QT, VAT colspan header, "Mã hàng:" xám không đậm, Code đặt hàng trống, totals row SL 363 / GT sau thuế 379,576,631.22 / VAT 30,382,476.13 / CP QT 7,152,080.03 / nội địa 10,057,504 / nhập kho 396,786,215.19 / đơn giá nhập 114,684,874.25 (CP-QT & nội-địa khớp summary), V2BaseTableScroll cuộn 2 chiều (sw 1693 > cw 906).

**Tasks ⑤ (Tab B — "Vận chuyển" / delivery, ERP `#van_chuyen` loại NỘI ĐỊA, CHỈ-ĐỌC) — 09/10/2026:**
- Khảo sát (survey subagent + truy DB `erp_hrm_check`): cột VC tồn tại VẬT LÝ trên `product_imports` (total_cost_transition/delivery_tax/payer_employee_amount/payer_company_amount/payer_employee_id/payer_company_id/warehouse_import_id), `warehouse_imports` (total_km_expected/total_km_actual), `activity_has_delivery_trips` (warehouse_import_id/delivery_trip_id/total_cost_transition/payer_employee_amount/payer_company_amount), `delivery_trips.name`. Entity HRM `ProductImport`/`WarehouseImport` KHÔNG khai các cột/quan hệ này → phải tự serialize. Dữ liệu thật: loại 15 (32 phiếu có chi phí VC), loại 2 (2), loại 3 (10), loại 99 (3); 51 dòng trip gắn warehouse_import_id. ⇒ Tab B là **CHỈ-ĐỌC** (ERP `#van_chuyen` toàn `disabled`), KHÔNG port khối tính lúc store — khớp Tab A. Phiếu HRM tạo mới chưa populate (store HRM chưa chạy khối VC của ERP) → tab rỗng cho phiếu HRM-tạo, có data cho phiếu ERP-tạo (đúng hành vi read-only ERP). Verify phiếu: PNH-09200 (loại 15, wi=6455, km 20/58, cost 2,662,000, tax 212,960, 1 trip "29TPHXNA-10...").
- [x] BE: `ProductImport::buildDeliveryData($type, $warehouseImportId, $overrides)` static — `[]` nếu type ∉ DELIVERY_TYPES; đọc km từ `warehouse_imports`, trips từ `activity_has_delivery_trips` LEFT JOIN `delivery_trips` theo warehouse_import_id (trip_id/trip_name/payer_employee_amount/payer_company_amount); 4 ô own-column áp qua `$overrides`. KHÔNG gate `canViewCostPrice` (ERP `#van_chuyen` chỉ gate `has_delivery` type-based — chi phí VC ≠ giá vốn hàng hoá).
- [x] BE: serialize key `delivery` ở CẢ 3 load path — `ProductImportDetailResource` (Edit, full: own 4 cột + WI km + trips), `getWarehouseImportSource()` (đường A: WI km + trips, own cột null→empty), `ProductImportRequestDetailResource` (đường B: km_expected từ PIR, không WI → trips rỗng). `php -l` sạch.
- [x] FE: `importTypeConfig.js` thêm key `delivery` (TRAILING) vào tabs của loại NỘI ĐỊA DELIVERY_TYPES = 2, 3, 4, 9, 15, 99 (KHÔNG 11/14); `ProductImportForm.vue` thêm `<b-tab v-if="hasTab('delivery')" title="Vận chuyển">` read-only: 6 ô tổng hợp (Số Km dự kiến·Số Km chốt·Chi phí vận chuyển thực tế·Thuế·Nhân viên chịu phí·Công ty chịu phí) + `<hr>` + "Chi tiết" + v-for trips (Chuyến xe link + Nhân viên/Công ty chịu phí). Nhãn NGUYÊN VĂN ERP `form.blade.php:311-384`. Data `deliverySummary` wiring ở `setForeignCostBlocks()` (3 path). Helper mới `deliveryVal(n,money)` (null/''→blank, mirror `| number`/`| my_number`) + `deliveryTripUrl(id)` dùng `utils/erp-link.erpUrl()` (thiếu ERP_URL → tên trơn). KHÔNG gate `canViewCostPrice`. Template compile sạch (vue-template-compiler).
- [x] Verify Playwright 127.0.0.1:3000 trên phiếu nội địa có data thật (PNH-09200 loại 15) + BE contract qua `GET show`. KHÔNG commit/push.

### Checkpoint — Tab B "Vận chuyển" (#van_chuyen) VERIFY XONG — 09/10/2026
Vừa hoàn thành: Tab B read-only loại NỘI ĐỊA DELIVERY_TYPES (2,3,4,9,15,99) — 6 ô tổng hợp (km dự kiến/chốt từ `warehouse_imports`; chi phí/thuế/người-công ty chịu phí từ cột phiếu) + `<hr>` "Chi tiết" + danh sách chuyến xe (`activity_has_delivery_trips`). Nhãn nguyên văn ERP `form.blade.php:311-384`; số chuẩn quốc tế; km null→trống; "Chuyến xe" là link sang ERP qua `erpUrl()` (fallback tên trơn khi thiếu ERP_URL). KHÔNG gate `canViewCostPrice` (chi phí VC ≠ giá vốn — ERP chỉ gate `has_delivery` type-based). BE: `ProductImport::buildDeliveryData()` static + serialize `delivery` ở 3 load path (DetailResource/getWarehouseImportSource/RequestDetailResource), `php -l` 4 file sạch. FE: `importTypeConfig` + `<b-tab>` + `deliverySummary`/`deliveryVal`/`deliveryTripUrl` + wiring `setForeignCostBlocks`. Verify: BE contract qua `GET /api/v1/finance/product-imports/9200` token thật (delivery đầy đủ, km "20.00"/"58.00", cost 2,662,000, tax 212,960, 1 trip 3256) + Playwright Edit view PNH-09200 loại 15 (toggle DEV DB status/created_by tạm rồi REVERT về status=1/created_by=200) → panel render đủ 6 ô + trip, link trip = `http://127.0.0.1:8001/admin/warehouse/delivery_trips/3256/show`. Console chỉ còn warning Nuxt dev (không liên quan).
Đang làm dở: (không) — Tab B đóng.
Bước tiếp theo: CHỜ USER NGHIỆM THU Tab A + Tab B. Kế tiếp theo thứ tự user "A trước, B sau, C tách riêng" → **Tab C "Bốc xếp"** (ERP `#boc_xep`, tính năng TÁCH RIÊNG — editable, không gộp vào cụm này).
Blocked: (không). Lưu ý: phiếu nội địa hiện là status=1 (DA_HOAN_THANH) → Edit view chỉ mở được bằng toggle DEV DB tạm; đã revert.
KHÔNG commit/push.

### Checkpoint — Cụm loại 11 CHI PHÍ (4 tab read-only) VERIFY XONG — 09/10/2026
Vừa hoàn thành: 4 tab chi phí ngoại loại 11 (Chi phí HĐ · Chi phí quốc tế có/không tính thuế NK · Phân bổ chi phí vận chuyển nhanh) render read-only, nhãn nguyên văn ERP, số chuẩn quốc tế, ô rỗng để trống, gate `canViewCostPrice`. Playwright verify trên PIR 9760 (3 tab đầu) + PIR 2306 (fastDelivery có data, rowspan đúng) + PIR 9889 (empty-state filter đúng). FE wiring qua `setForeignCostBlocks()` ở 3 load path.
Đang làm dở: (không) — cụm chi phí đóng.
Bước tiếp theo: CHỜ USER NGHIỆM THU. Sau đó → tab "Tính giá thành nhập kho" (landed cost #phan_bo) còn hoãn.
Blocked: (không). Lưu ý môi trường: Playwright MCP config `--isolated` KHÔNG tự nạp `e2e/.auth/user.json` → phải inject `access_token` vào localStorage tay; đã tạo symlink `chromium-1246→1247` cho MCP; Node 20 là `v20.20.2` (không phải v20.20.1).
KHÔNG commit/push.

### Checkpoint — Tab A "Tính giá thành nhập kho" (landed cost) VERIFY XONG — 09/10/2026
Vừa hoàn thành: Tab A read-only loại 11 (`#phan_bo`) — 6 ô tổng hợp + bảng 15 cột giá thành nhập kho + totals row, nhãn nguyên văn ERP, số chuẩn quốc tế, "Mã hàng:" xám không đậm, ô rỗng để trống, gate `canViewCostPrice` fail-close. BE: `landedCostSummary()` + serialize `landed_cost_summary` 3 load path. FE: `<b-tab>` + `landedSummary/landedRows/landedTotals/formatNum4` + wiring `setForeignCostBlocks`/`loadForEdit`. Playwright verify PNH-12178 (32 SP) qua Edit view (toggle DEV DB tạm rồi REVERT) + BE contract qua `GET show` token thật; totals cross-match summary.
Đang làm dở: (không) — Tab A đóng.
Bước tiếp theo: CHỜ USER NGHIỆM THU Tab A. Kế tiếp theo thứ tự user "A trước, B sau, C tách riêng" → **Tab B "Vận chuyển"** (ERP `#van_chuyen`, gate `has_delivery`).
Blocked: (không). Lưu ý: KHÔNG tồn tại phiếu loại 11 trạng thái DANG_TAO (3) nên Edit view không mở được với data thật → đã toggle tạm DEV DB (status/created_by) rồi revert; mọi phiếu loại 11 hiện là status=1.
KHÔNG commit/push.

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

---

## ②b — Ghi POOL hàng giữ + arrived/arriving khi HOÀN THÀNH phiếu loại 2/15 (ĐANG MỞ — 09/10/2026)

**Bối cảnh:** ②a chỉ ghi FORM (`product_import_detail_customers`), KHÔNG đụng pool hàng giữ. Khi phiếu
loại 2/15 chuyển `DA_HOAN_THANH` (qua `handleCompleted()` → `updateWarehouse()`), ERP còn: (b1) GIỮ
HÀNG cho khách (đường A `prepick_details`/`prepick_logs`, đường B `product_import_direct_details`), và
(b2 — chỉ loại 15) cập nhật `arrived_qty`/`arriving_qty` + `order_stock_progress` trên chuỗi bảng
inland. HRM hiện KHÔNG làm cả hai → hàng giữ không sinh, "hàng đang về" không trừ.

**Scope user đã chốt:** ①(b) parity đầy đủ cả 2 pool + arrived/arriving · ② **ghi y ERP** (invariant
fix `arriving = GREATEST(0, Σprogress − arrived)` để TASK RIÊNG sau). Nguồn chân lý = ERP
`App\Model\Warehouse\ProductImport::updateWarehouse()` loại 15 (:1396-1513) + loại 2 (:1515-1533) +
helper `prepick()` (:1923-1963) + `productImportDirectDetail()` (:1965-2001).

**PHÁT HIỆN khi khảo sát (báo user lúc nghiệm thu):** HRM **chưa port 7/8 entity inland** mà effect-2
cần (`OrderStockProgress`, `InlandOrderRequestNewProduct(+Detail)`, `InlandBuyContractNewProductDetail`,
`InlandPurchaseInvoiceProduct`, `InlandOrderSummaryNewProduct`, `InlandBuyContractNewPromotion`; chỉ
`InlandProductArrivedNew` có). → ②b phải ghi bằng **raw `DB::table`** y khuôn khối type-14 `hold_details`
(`ProductImport.php:582-637`), objectable_type lưu FQN ERP (P2.1). **Không có nguy cơ trừ hai lần**
(HRM chưa ghi arrived/arriving/progress ở đâu — đó là lý do "đang về" phồng). **Không backfill**
(0 phiếu loại 2/15 hoàn thành qua luồng HRM có allocation).

**Quyết định sequencing (toàn quyền, báo user nghiệm thu):** b1 trước (bounded, dry-run được), b2 ngay
sau (map chính xác FK inland từ ERP rồi mới viết — không viết mù vùng drift). Cả hai cùng feature ②b.

### b1 — Giữ hàng cả 2 pool (loại 2 + 15)
- [x] Nới `PrepickStockService::addLot()` THÊM (optional `?string $objectableType=null, ?int $objectableId=null`):
      null → giữ nguyên hành vi WarehousePrepick (callers cũ không đổi); có giá trị → ghi objectable cho
      CẢ `prepick_details` (+root) lẫn `prepick_logs` = (FQN, id) — mirror ERP `prepick()` dùng
      `get_class($customer)` + `$customer->id` cho detail/root/log. Re-test màn "Phiếu xuất giữ".
- [x] `ProductImport::updateWarehouse()` thêm khối loại 15 + loại 2 giữ hàng, chạy sau khối type-14:
      mỗi `$p->customers` có `allocation` → đường A (`!is_import_direct`): loại 15 guard `type∈{1,3}`,
      loại 2 KHÔNG guard → `PrepickStockService::addLot(...)` objectable = `App\Model\Warehouse\ProductImportDetailCustomer`
      + customer->id, qty = `customer->qty * customer->unit_coefficient`, company = `$this->company_id`,
      employee = (loại 15: inland_contract_detail_new→order_request.created_by, fallback type2:
      inland_product_arrived_new→inland_buy_contract_new.created_by; loại 2: inland_order_request.created_by);
      đường B (`is_import_direct`): `productImportDirectDetail(customer, employeeId)`.
- [x] Port helper `productImportDirectDetail()` vào HRM (Eloquent `ProductImportDirectDetail`+`Log`):
      employee_id, company_id=`$this->company_id`, department_id=employee.info.department_id, part_id=null,
      objectable=(FQN ProductImportDetailCustomer, customer->id), qty base-unit, +log before/after.
- [x] Resolve `employee_id` qua raw `DB::table` — helper `resolveType15EmployeeId()` + `inlandContractCreatedByFromArrived()`;
      loại 2 đọc `inland_order_requests` (bảng CŨ). Dry-run xác nhận emp/dept resolve non-null (60/31/159/590/1142).
- [x] Dry-run (transaction + rollback) TRƯỚC khi ghi pool thật. `grep DB_ .env` = `erp_hrm_check` (DB gộp dev).
      ĐÃ chạy ĐÚNG `updateWarehouse()` compiled trên 12254(A)/12290(B)/12344(promo) → prepick/direct sinh đúng qty,
      objectable_type=`App\Model\Warehouse\ProductImportDetailCustomer` (P2.1), rollback sạch, 0 ghi prod.

### b2 — effect-2 arrived/arriving (CHỈ loại 15), raw DB, ghi y ERP
- [x] reset `inland_buy_contract_new_product_details.arriving_qty=0` cho các contract_detail_id của phiếu.
- [x] customer type==1: `inland_order_request_new_product_details` arrived+=/arriving-=qty · `order_stock_progress`
      qty-= (orderable=detail, objectable=inland_product_arrived_new) · root_detail arrived+=/arriving-= ·
      contract_detail arrived+=/arriving=0. Dry-run 12254: iorn_detail#4179-4183 + root#14253-14257 + osp#44652-44656 trừ đúng.
- [x] customer type==2: `inland_order_request_new_products` (hoặc fallback qua `inland_purchase_invoice_customer`
      → `inland_purchase_invoice_products` → `inland_order_summary_new_products`) arrived+=/arriving-=
      `min(qty_available_for_stock, customer.qty)` · order_stock_progress · root_order_request_product ·
      contract_detail arrived+=/arriving=0 · trừ dần `qty_available_for_stock`. Dry-run 12230/12223: order_request_product
      resolve đúng (fallback KHÔNG kích hoạt vì primary luôn tìm thấy — port trung thành, có guard).
- [x] promotion (count(customers)==0): đường B productImportDirectDetail + `inland_buy_contract_new_promotions`
      arrived+=qty/arriving=0. Dry-run 12344: direct_detail sinh qty=2, promo guard `if($promo)` bỏ qua đúng khi SP không có dòng KM.
- [x] Dry-run như b1 — arrived+= và osp qty-= di chuyển cùng nhau (khớp bất biến GREATEST(0,Σprogress−arrived)); không double-count.

### Verify ②b — dry-run live-code (transaction rollback, 0 ghi prod); user nghiệm thu UI
- [x] Phiếu loại 15 đường A (12254, 5 khách type=1): 5 lô prepick qty 1/5/1/1/1 + arrived/arriving/progress trừ đúng.
- [x] Phiếu loại 15 đường B (12290): product_import_direct_details sinh qty=2 + effect-2 đủ chuỗi.
- [x] Phiếu loại 2 đường B (12238): chỉ giữ hàng (direct_detail), KHÔNG effect-2 (arrivedNewId=NULL, ERP loại 2 comment out) ✓.
- [x] Wiring: `handleCompleted()` (ProductImportService :213 store / :322 update) → `updateWarehouse()` khi status=DA_HOAN_THANH.
- [x] Regression màn "Phiếu xuất giữ" (addLot thêm 2 param optional): caller cũ `WarehousePrepickRequestService:482`
  truyền 8 tham số → objectable=null → nhánh mặc định `WAREHOUSE_PREPICK` với documentId/detailId Y NHƯ TRƯỚC
  (code-proof, thân `addLot` 905-910). Playwright 127.0.0.1:3000: list `/finance/warehouse-prepick-requests`
  tải đủ 10 phiếu thật (PXG-02188→02179), phân trang 1–10/2056, không lỗi liên quan prepick. ✅
- [ ] (user) Bấm thật HOÀN THÀNH 1 phiếu loại 2/15 mới qua UI → ghi pool prepick + arrived/arriving thật trên dev
  (dành cho user nghiệm thu; logic đã cover bằng dry-run live-code transaction+rollback + wiring code-read).

---

## Tab C — "Bốc xếp" (#boc_xep) EDITABLE — ĐANG LÀM (09/10/2026)

**Bối cảnh + phê duyệt:** User chốt "ok" (phiên trước) cho thiết kế Tab C = **port trung thực đầy đủ**
(gồm `syncPickUp`), **bật cho MỌI loại phiếu như ERP** (hiện tab với 2,3,4,9,15,99,11), gate sửa bằng
`canEdit()`. Phân biệt rõ với tab `pickupCost` hiện có ("Chi phí bốc hạ hàng tại kho", `import_costs`
type BOC_XEP, foreign-only) — Tab C là **phiếu bốc xếp** (`arrange_delivery` + `executors`), EDITABLE.

**Nguồn chân lý ERP (đọc verbatim phiên trước):**
- `#boc_xep` bind `form.arrange_delivery` (object) + `form.executors` (array).
- `create.blade.php` `changeArrangeDelivery(value)`: set `arrange_delivery.price` từ `arrangeDeliveries.find(id)`:
  rent_type==2 → delivery.price (nặng) / delivery.price_hour (giờ); else → company_price / company_price_hour;
  không thấy → 0. Rồi gọi `form.syncPickUp()`.
- `formJs.blade.php` `$watch('form.arrange_delivery.total_money'|'.vat')`: total_money>0 && type≠11 → upsert
  `InlandImportCost` cost_id=192 vào `form._inland_costs` (xoá+đẩy lại). `changeRentType()`: rent_type truthy →
  **account=1561, work=29** (import; export là 6428); else account=null.
- `ProductImport.blade.php` `syncPickUp()` (782-802): arrange_delivery.price → tìm cost en_name=='arrange_cost'
  (cost_id 192) → upsert PickUpCost {cost_id, value_before_vat=total_money, vat_percent=vat, supplier_id,
  disabled=true} vào `_pick_up_costs` (chạy MỌI loại, không guard).
- Hạch toán (getDataCreateDept, đã phân tích): Foreign(11) → pick_up (rent_type==1 skip cost192; rent_type==2
  post 1541/1331/3311 WITH contractable=warehouse_import + supplier; no-arrange post không contractable);
  Domestic(2,15) → inland NOI_DIA với supplier (rent_type==1 null supplier KHÔNG post — tự khớp); else(3,4,9,14,99)
  → pick_up CHỈ rent_type==2 WITH contractable. Executors = data-only (không hạch toán).
- **Quyết định routing (toàn quyền, báo nghiệm thu):** dòng chi phí bốc xếp (cost_id 192) đẩy vào ĐÚNG mảng mà
  accounting của loại đó tiêu thụ (domestic→inland_costs; foreign+else→pick_up_costs), TRÁNH ERP tạo 2 dòng chết
  (BOC_XEP + NOI_DIA) trùng. Documented là quyết định có chủ đích.

### C1 — BE hạ tầng (type-independent) — XONG 09/10/2026
- [x] `ProductImport` entity: quan hệ `arrange_delivery()` hasOne(ProductImportExportArrangeDelivery,'parent_id','id')
  ->where('type',TYPE_IMPORT=1); `executors()` hasMany(...Executor,'parent_id','id')->where('type',1).
- [x] `ProductImportService::saveArrangeDelivery()` port verbatim từ `ProductExportService` (655-726), adapt:
  TYPE_IMPORT(1), type_name='import', parent_id=product_import.id, request_id=product_import_request_id,
  rent_type_name 'Công ty'/'Thuê ngoài'; **xoá-sạch-dựng-lại** (convention HRM) delivery+executors theo parent_id.
  + `syncArrangeCost()`: ghi dòng ImportCost (cost_id=arrange_cost=192) theo loại — domestic(2,15)→NOI_DIA, còn lại→BOC_XEP.
- [x] Wire `saveArrangeDelivery()` vào store()/update() — NGAY SAU `syncCosts()`, TRƯỚC `recomputeMoneyServerSide`
  (để recompute cộng/phân bổ được dòng 192; sau syncCosts để delete-by-type không xoá mất dòng 192).
- [x] Store/UpdateRequest: `arrange_delivery.*` + `executors.*` conditional + decode JSON (FormData).
- [x] Route dòng chi phí cost_id=192: domestic(2,15)→NOI_DIA; foreign(11)+else(3,4,9,14,99)→BOC_XEP
  (server-side từ arrange_delivery; `syncCosts` strip dòng 192 do FE gửi — defense-in-depth).
- [x] Resource: `ProductImportDetailResource` trả `arrange_delivery` + `executors` (UNGATED canViewCostPrice — bốc xếp do
  người lập tự nhập, không phải giá vốn; gate sửa bằng `is_can_edit`). `loadDetail()` eager-load 'arrange_delivery','executors'.
  (ĐÃ QUYẾT: BỎ `ProductImportRequestDetailResource` — ĐNNK nguồn không có tab bốc xếp, đây là tab mới trên phiếu.)
- [x] Endpoint `GET /product-imports/arrange-form-options` — accounts/cost_debts/works + arrange_goods(scope company người
  lập, status Hoạt động). UNGATED quyền quản lý danh mục (khuôn `BillAdjustDeptController::formOptions`). Smoke-test 200:
  308 accounts / 22 cost_debts / 21 works / 7 arrange_goods. NCC + nhân viên vẫn tìm server-side qua endpoint sẵn có
  (`assign/customers/manager/suppliers` + employee search) — KHÔNG nhúng, mirror export create.vue.

### C2 — BE hạch toán delta — [x] XONG + VERIFIED (09/10/2026, audit trực tiếp — subagent drift bỏ)
Audit đối chiếu từng dòng ERP `ProductImport::getDataCreateDept()` ↔ HRM services. KẾT LUẬN: C2 đã implement
đầy đủ & trung thực từ C1, chỉ checkbox cũ còn sót. Bằng chứng:
- [x] **ForeignPurchase (11)** `ForeignPurchaseProductImportAccountingService` = port ĐÚNG 3 nhánh ERP
  (`ProductImport.php:2321-2335`): rent_type==1 → skip cost192 (`continue`) + dòng pick_up khác KHÔNG ghi;
  rent_type==2 → 1541/1331/3311 WITH contractable(warehouse_import)+supplier; không arrange (else) → 1541/1331/3311
  KHÔNG contractable. Sau đó kết chuyển giá vốn 1561/1541. Docblock ghi rõ 1541 lệch cân-đối CỐ Ý theo ERP
  (giá trị hàng NN đã ghi Nợ 1541 ở chứng từ thượng nguồn) — KHÔNG bù.
- [x] **Helper chung `arrangePickUpAccounting()`** (base `ProductImportAccountingService:357-384`) = port EXACT ERP
  nhánh `else` catch-all (`ProductImport.php:2381-2390`): `$group+=1` TRƯỚC check; rent_type==2 → 1541/1331/3311
  WITH contractable(warehouse_import)+supplier; else → `continue` (không ghi). Đọc `import_costs` type=5 (BOC_XEP).
  Gọi bởi: **SaleReturn(4)** (nhánh không-HĐ, dòng 34), **BorrowSellReturn(9)** (dòng 39), **Other(99/3/14)** (dòng 27).
- [x] **Domestic (2,15)** `DomesticPurchaseProductImportAccountingService`: block chi phí nội địa riêng (đọc
  `import_costs` type=2 NOI_DIA, mỗi dòng có NCC = 1 group → 1541/1331/3311 NCC chi phí; bỏ dòng không NCC =
  mirror ERP `if(isset($inland_cost->supplier))`). Dòng bốc xếp cty 2,15 route → NOI_DIA(2); rent_type==1 không NCC
  → tự bị bỏ (khớp ERP, không cần nhánh riêng).
- [x] **Dispatcher** `ProductImportService::resolveAccountingService()` (1347-1381) wire đủ: 4→SaleReturn ·
  2/15→Domestic · 99/3/14→Other · 9→BorrowSellReturn · 11→ForeignPurchase. Chỉ chạy ở `handleCompleted()`
  (status DA_HOAN_THANH) — khớp ERP ghi bút toán lúc hoàn thành, KHÔNG ở "Đang tạo".
- NOTE: loại 3 (MUON_TRA_LAI) + 14 (NHAP_GUI) qua Other = no-op hạch toán (ERP không có nhánh bút toán riêng,
  chỉ cập nhật kho/giữ) — trung thực. Loại 14 cũng KHÔNG mở tab Bốc xếp ở FE (xem C3).

### C3 — FE tab editable — [x] XONG (09/10/2026)
- [x] `importTypeConfig.js`: thêm tab key `arrangeDelivery` (tab CUỐI) cho loại 2,3,4,9,15,99,11.
  **Loại 14 CỐ Ý loại trừ** (dòng 236 comment) — ERP `#boc_xep` không mở cho điều chuyển nội bộ type 14.
- [x] `ProductImportForm.vue` (Edits 1-10): tab editable "Bốc xếp" port trung thực từ export `create.vue` arrange tab.
  - **MÀN MỚI → dùng `V2Base*`, KHÔNG HTML thô** (khác export cũ dùng `form-control-sm`): is_weight=`V2BaseRadio`,
    rent_type=`V2BaseSelect` (`:value`+`@change`, component KHÔNG có prop `disabled` → engage grid bằng
    `v-if="arrangeEngaged"`), account/cost_debt/work/employees=`V2BaseSelectRemote` (local-filter từ catalog),
    supplier=`V2BaseSelectRemote` (remote `assign/customers/manager/suppliers`), tiền=`V2BaseCurrencyInput`.
  - **Catalog UNGATED**: GET `finance/product-imports/arrange-form-options` (accounts/cost_debts/works/arrange_goods
    scoped company+HOẠT ĐỘNG) + `assign/tasks/employees`; lazy-load qua `ensureArrangeOptions()` ở tab `@click`.
  - **KHÔNG canViewCostPrice gate** trên tab (bốc xếp = chi phí người lập tự nhập, không phải giá vốn); gate SỬA
    bằng `is_can_edit` của phiếu.
  - **RESOLVED — KHÔNG auto-default account/work** (khác export mặc định account='6428'): ERP import `change()`
    CLEAR account/work về null (formJs:80-81); 1561/29 là dòng hạch toán BE (cost_id arrange_cost / syncArrangeCost +
    syncPickUp `ProductImport.blade.php`:782-802), KHÔNG phải field form → `onRentTypeChange` để trống, user tự chọn.
  - **RESOLVED — KHÔNG quick-add Mã phí/Vụ việc**: ERP `#boc_xep` không có nút quick-add; POST tạo nhanh sẽ 403
    (endpoint gated) → bỏ hẳn, chỉ chọn từ catalog.
  - Computeds khớp export: arrangePrice (rt2→price/price_hour, rt1→company_price/company_price_hour theo is_weight),
    arrangeTotal=price×weight, arrangeVatPrice, arrangeAfter; executorSum + executorMatched (so khớp 2 chữ số thập phân).
  - `validateArrange`: arrange_type req · account req · weight>0 · '642*'→cost_debt req · '154*'→work req ·
    rt2→supplier_id req · rt1→≥1 executor (employee_id + price>0) & executorMatched.
  - `buildArrangePayload`: arrange_delivery=null & executors=[] khi !engaged; account=identify_number, arrange_type=id,
    cost_debt/work=id; executors chỉ khi rt1. `loadForEdit` map ngược từ `d.arrange_delivery`/`d.executors`.

### Verify — Playwright 127.0.0.1:3000 (KHÔNG commit/push)
- [x] FE verified (PNH-12343, type 4, Đang tạo): tab render đủ label ERP (Cách tính/Hình thức thuê/Loại bốc xếp/
  Khối lượng (Tấn)/Đơn giá bốc xếp/Số tiền/VAT (%)/Tiền VAT/Số tiền sau VAT/Tài khoản nợ/Mã phí/Vụ việc);
  catalog load (7 arrange_goods, 308 accounts, 22 cost_debts, 21 works, 392 employees); rt1 engage→grid+executors,
  computeds đúng (29000×10=290000, VAT8%=23200, after=313200, executorMatched); rt2 clear executors + supplier-required;
  validate gates (account/supplier) fire đúng; payload/deselect shapes đúng. Round-trip save→BE chưa chạy LIVE
  (tránh mutate phiếu thật bằng FK giả) — BE mapping đã confirm qua code (saveArrangeDelivery) + chờ audit C2.
- [x] Hạch toán theo loại — verify bằng ĐỐI CHIẾU CODE ERP↔HRM (xem C2): mỗi loại post đúng cụm ERP.
  Round-trip LIVE (save phiếu thật → bút toán AccountDetail) hoãn chủ đích: tránh tạo bút toán rác trên phiếu
  DEV bằng FK giả; logic 2 phía đã khớp từng dòng. Khi cần nghiệm thu bút toán thật → lập 1 phiếu nhập test đủ
  điều kiện hoàn thành cho từng loại rồi so AccountDetail (việc nghiệm thu của user).

### Checkpoint — 2026-10-09
Vừa hoàn thành: C3 FE tab "Bốc xếp" (Edits 1-10) + verify Playwright (render/catalog/rt1/rt2/validate/payload);
C2 BE audit TRỰC TIẾP (subagent drift → tự đối chiếu) — xác nhận ForeignPurchase 3 nhánh, helper
arrangePickUpAccounting (port EXACT ERP else 2381-2390), Domestic inland, dispatcher wire đủ. plan.md C2+C3 → [x].
Đang làm dở: (không) — C2+C3 đã khép ở mức đối chiếu code + verify FE.
Bước tiếp theo: CHỜ USER NGHIỆM THU. Nếu user muốn bút toán LIVE → lập phiếu test từng loại, so AccountDetail.
Blocked: (không)
