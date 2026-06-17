# Quotation Shipping Cost + Redesign Tổng hợp giá trị báo giá — Plan

**Goal:** Thiết kế lại section "Tổng hợp giá trị báo giá" thành bảng nhóm chi phí (6/7 cột động) + thêm Chi phí vận chuyển cấp phiếu (chịu CK + VAT như Hàng hoá/Dịch vụ), đồng bộ edit/view/print/excel.

**Spec:** `docs/superpowers/specs/2026-06-06-quotation-shipping-cost-design.md`
**Branch:** `tpe-develop-assign` · **Phụ trách:** @dnsnamdang

> Quy ước: không commit/push (theo CLAUDE.md). Mỗi task xong đánh `[x]`. Verify BE bằng `php -l`, FE bằng compile dev server + E2E thủ công.

---

## Bản đồ file

**Backend** (`hrm-api/Modules/Assign`):
- `Database/Migrations/2026_06_05_000001_add_shipping_cost_to_quotations_table.php` *(tạo)*
- `Entities/Quotation.php` *(cast)*
- `Services/QuotationService.php` *(computeTotals + allocateDiscount + computeSummaryBreakdown + create/update persist + helper)*
- `Http/Requests/Quotation/QuotationStoreRequest.php` + `QuotationUpdateRequest.php` *(rules)*
- `Transformers|Http/Resources` `DetailQuotationResource.php` *(trả field VC + summary_breakdown)*
- `Http/Controllers/Api/V1/QuotationController.php` + `resources/views/exports/bom_list.blade.php` *(excel bảng tổng hợp)*

**Frontend** (`hrm-client`):
- `pages/assign/quotations/_id/edit.vue` *(bảng 6/7 cột + row VC input)*
- `components/assign/quotation/QuotationPrintPreview.vue` *(bảng tổng hợp khi in)*
- `pages/assign/quotations/index.vue` *(bảng tổng hợp khi xem)*

---

## Phase 1 — Backend: DB + tính toán

- [x] **B1. Migration thêm 4 cột VC**
  Tạo `2026_06_05_000001_add_shipping_cost_to_quotations_table.php`. Trong `up()` thêm sau `total_discount_amount`:
  - `shipping_cost` decimal(18,2) default 0
  - `shipping_vat_percent` decimal(5,2) default 0
  - `shipping_discount` decimal(18,2) default 0
  - `shipping_allocated_discount` decimal(18,2) default 0
  `down()` drop 4 cột. Verify: `php artisan migrate` (user chạy) hoặc `php -l`.

- [x] **B2. Entity cast**
  `Quotation.php` — thêm vào `$casts`: `shipping_cost`, `shipping_vat_percent`, `shipping_discount`, `shipping_allocated_discount` → `decimal:2`.

- [x] **B3. Helper `shippingDiscount()`**
  Trong `QuotationService.php`: thêm private method trả CK của VC theo `discount_method` (1 → `shipping_discount`; 2 → `shipping_allocated_discount`; null → 0). (Theo spec 5.2)

- [x] **B4. `computeTotals()` cộng VC (có CK)**
  Sau 2 vòng lặp products + serviceItems, trước `return` (≈ dòng 1054): nếu `shipping_cost > 0` thì `totalSale += shipping_cost`; `totalDiscount += shippingDiscount()`; `totalVat += (shipping_cost − shippingDiscount()) × shipping_vat_percent/100`. (Spec 5.3)

- [x] **B5. `allocateDiscount()` đưa VC vào base (CK tổng)**
  Tìm hàm phân bổ CK tổng trong `QuotationService.php`. Bổ sung `shipping_cost` vào tổng base value; tính phần CK của VC bằng cùng thuật toán (largest remainder) và ghi `shipping_allocated_discount`. Đảm bảo tổng allocated (products + service + VC) = CK tổng. (Spec 5.4)

- [x] **B6. `computeSummaryBreakdown()`**
  Thêm public method trả mảng 4 nhóm + tổng `{nhap, truoc_vat, chiet_khau, vat, sau_vat}`:
  - HH: lặp products cha (giá nhập, quoted_price, CK theo method, vat).
  - DV: serviceItems `revenue_calculation` ∈ {1, null}; CP: `= 0`.
  - VC: từ `shipping_cost/shipping_vat_percent/shippingDiscount()`.
  - tong: Σ cột; `sau_vat` tong = `total_after_vat`. (Spec 5.5, 2.3)

- [x] **B7. Persist field VC ở `create()` + `update()`** *(+ reset VC trong `clearDiscountData` khi đổi method)*
  Trước `recomputeTotals()`: set `shipping_cost`, `shipping_vat_percent` (ép 0 nếu cost=0), `shipping_discount` (chỉ khi method=1, else 0). `shipping_allocated_discount` để `allocateDiscount` lo. Đảm bảo gọi `allocateDiscount` (khi method=2) trước/đồng bộ `recomputeTotals`. (Spec 5.6)

- [x] **B8. Request validate** *(Store `nullable`, Update `sometimes|nullable`; +shipping_allocated_discount)*
  `QuotationStoreRequest` + `QuotationUpdateRequest` (Update `sometimes`): thêm rules `shipping_cost`, `shipping_vat_percent` (max 100), `shipping_discount` — đều `nullable|numeric|min:0`. Giữ rethrow `ValidationException` ở controller. (Spec 5.7)

- [x] **B9. Resource trả field VC + breakdown** *(DetailQuotationResource: 4 field + summary_breakdown)*
  `DetailQuotationResource.php`: thêm `shipping_cost`, `shipping_vat_percent`, `shipping_discount`, `shipping_allocated_discount`, và `summary_breakdown` = `computeSummaryBreakdown($quotation)`. (Spec 5.8)

- [x] **B10. Verify BE**
  `php -l` 6 file sửa → No syntax errors toàn bộ. ⏳ User chạy migrate + smoke test API.

## Phase 2 — FE: màn tạo/sửa (`_id/edit.vue`)

- [x] **F1. data + computed VC**
  Thêm data `shippingCost:0`, `shippingVatPercent:8`, `shippingDiscount:0`. Computed: `shippingCkValue` (theo `discountMethod`: 1→shippingDiscount, 2→từ allocated trả về, null→0), `shippingVatAmt = (shippingCost − shippingCkValue) × shippingVatPercent/100`, `shippingAfterVat = shippingCost − shippingCkValue + shippingVatAmt`.

- [x] **F2. Computed group rows**
  Thêm computed dựng 4 nhóm (HH/DV/CP/VC) + tổng theo đúng cột bảng (nhap/truocVat/ck/vat/sauVat), tách DV/CP theo `revenue_calculation` (1/null→DV, 0→CP), CK theo `discountMethod`. Tái dùng các computed total sẵn có nếu khớp.

- [x] **F3. Thay markup section Tổng hợp bằng bảng 6/7 cột**
  Thay block summary hiện tại (≈ dòng 729–777) bằng `<table>` 5 dòng I–V. Cột "Chiết khấu" bọc `v-if="discountMethod"` (ẩn khi null → 6 cột); colspan ô "Tổng giá trị báo giá" co theo. Dòng I/II/III/V read-only.

- [x] **F4. Row IV Chi phí vận chuyển — inputs**
  - "Thành tiền trước VAT" = `V2BaseInput` số (`shippingCost`).
  - "Chiết khấu" = input khi `discountMethod===1` (`shippingDiscount`); read-only allocated khi `===2`; cột ẩn khi null.
  - "Thuế VAT" = input group %VAT (`shippingVatPercent`, default 8) + hiện tiền VAT.
  - "Thành tiền nhập" = read-only = `shippingCost`. "Sau VAT" = `shippingAfterVat`.

- [x] **F5. Phân bổ CK tổng cộng VC vào base**
  Hàm "Phân bổ tự động" (FE, từ P7 erp-cost-catalog) phải cộng `shippingCost` vào base value để khớp BE; ghi phần VC vào `shippingDiscount`/allocated hiển thị.

- [x] **F6. Load + Save**
  fetchData: map `shipping_cost`, `shipping_vat_percent`, `shipping_discount` từ API. Payload submit: gửi 3 field này.

- [x] **F7. Validate FE inline**
  `shippingCost`/`shippingDiscount` < 0 hoặc CK VC > trước VAT → `is-invalid` + `invalid-feedback`, flag `touched` (chỉ hiện sau submit đầu). (CLAUDE.md form rule)

- [ ] **F8. Verify edit**
  Dev server compile sạch. E2E: nhập VC ở 3 chế độ CK (null/per-item/tổng), kiểm tổng khớp BE.

## Phase 3 — FE: xem + in

- [x] **F9. Print preview bảng tổng hợp**
  `QuotationPrintPreview.vue`: thay bảng totals (≈117–141) bằng bảng 6/7 cột từ `summary_breakdown` (hoặc computed đồng logic). Cột CK ẩn khi không có CK.

- [x] **F10. Màn xem `index.vue`**
  Render bảng tổng hợp 6/7 cột từ `summary_breakdown` (read-only) ở chỗ xem chi tiết.

- [ ] **F11. Verify view + print**
  Compile + E2E: mở xem + in báo giá có/không VC, có/không CK → bảng khớp màn edit.

## Phase 4 — Excel

- [x] **B11. Excel render bảng tổng hợp**
  `QuotationController::exportExcel`: truyền `summary_breakdown` qua `withSummaryData()`. `bom_list.blade.php`: thay khối tổng cũ bằng bảng 6/7 cột (ẩn cột CK khi null). (Spec 5.9)

- [ ] **B12. Verify Excel**
  `php -l` + user xuất thử 1 báo giá có VC + CK → đối chiếu bảng.

---

## Phase 5 — FE refinement row Chi phí vận chuyển (`_id/edit.vue`)

- [x] **F12. Input VC dùng `V2BaseCurrencyInput`** (format số tiền + bỏ spinner) thay `b-form-input type=number` — đồng nhất bảng chi tiết.
- [x] **F13. CK & VAT của VC: dual %↔₫ inline 2 chiều** — computed get/set: `shippingDiscountPercentModel` (base = shippingCost), `shippingVatAmountModel` (base = shippingCost − shippingCkValue). Nhập % ra tiền & ngược lại. (CK dual chỉ method=1; method=2 vẫn read-only allocated.)
- [x] **F14. CK tổng layout**: section "Chiết khấu tổng" + section "Tổng hợp" đều 100% width (flex-wrap + flex 0 0 100%).
- [x] **F15. Verify** compile + E2E nhập %/₫ qua lại + layout 100%.

- [x] **F16. Style input-group %↔₫ (addon xanh giữa) + co cột STT/Nhóm + bỏ đơn vị ₫ ở VC**

## Phase 6 — Review bảng Tổng hợp (sau feedback)

- [x] **R1. Cột "Thành tiền sau CK (trước VAT)"** (= base tính VAT), hiện khi có CK — BE `computeSummaryBreakdown` thêm `sau_ck`; edit/xem/in/excel thêm cột (v-if CK).
- [x] **R2. TSLN loại trừ chi phí vận chuyển** — margin (edit + xem) tính trên HH+DV+CP, bỏ VC cả tử/mẫu; nhãn "(không gồm VC)".
- [x] **R3. TSLN đồng nhất Create/Edit/Show, gated `canViewCostPrice`** — màn xem thêm 2 dòng TSLN dưới bảng (`breakdownMarginBefore/After`); không lên in/excel.
- [x] **R4. Giá vốn HH chỉ lấy dòng CHA** — FE edit `summaryBreakdown.hangHoa.nhap` → `lineImportTotal(p)` (BE đã đúng).
- [x] **R5. Bản in**: currencyCode dòng Tổng + dòng tỷ giá (≠VND) + giữ fallback.
- [ ] **R6. Verify**: php -l OK; chờ user E2E (cột sau-CK, TSLN excl VC nhất quán + theo quyền, in/excel).

## Phase 7 — Bugfix popup Gửi duyệt

- [x] **BF1. Popup "Gửi duyệt" làm tròn số sai so với footer**
  Triệu chứng: footer báo giá hiển thị Tổng giá nhập 7,96 USD / Tổng giá bán 11,51 USD nhưng popup gửi duyệt hiển thị 8 và 12.
  Root cause: `QuotationSubmitModal.vue::formatMoney` dùng `Math.round(n)` trước khi format → mất phần thập phân, trong khi footer `edit.vue::formatMoney` format trực tiếp giá trị gốc.
  Fix: bỏ `Math.round` trong `QuotationSubmitModal.vue` (dòng 127-130) → `new Intl.NumberFormat('vi-VN').format(n || 0)` (đồng nhất footer).

- [ ] **BF2. Verify**: compile + mở popup gửi duyệt báo giá có số lẻ (USD) → đối chiếu khớp footer.

- [x] **BF3. CK theo mặt hàng (method=1): Tổng CK footer chưa cộng CK vận chuyển**
  Triệu chứng: discountMethod===1, footer "Tổng CK" (dòng 878) + footer bảng SP (dòng 630) thiếu phần CK của Chi phí vận chuyển. Bảng Tổng hợp (`summaryBreakdown.tong.chiet_khau`) và method=2 (`totalAllocatedDiscount` cộng `shippingAllocatedDiscount`) đã đúng.
  Root cause: `totalDiscountPerItem` (edit.vue ~1394) chỉ cộng productDk + serviceDk, thiếu `shippingCkValue`.
  Fix: `return productDk + serviceDk + (Number(this.shippingCkValue) || 0)` → nhất quán method=2 + bảng Tổng hợp.

- [ ] **BF4. Verify**: method=1 có CK vận chuyển → footer Tổng CK = bảng Tổng hợp dòng V (cột Chiết khấu).

## Phase 8 — Đảo logic: VC tính vào TSLN + tổng giá trị bình thường (revert R2)

> Yêu cầu mới: Chi phí vận chuyển tính vào TSLN + tổng giá trị như Hàng hoá/Dịch vụ.
> Giá nhập VC = Thành tiền trước VAT (nếu không CK) = Thành tiền sau CK trước VAT (nếu có CK) → tức `shipping_cost − shipping_ck`. ⇒ VC đóng góp lợi nhuận tuyệt đối = 0 (giá nhập = giá bán sau CK), chỉ làm loãng % TSLN.

- [x] **G1. BE `computeSummaryBreakdown`**: `van_chuyen.nhap = shipBase − shipDisc` (thay vì 0) → `tong.nhap` tự gồm VC.
- [x] **G2. BE `calculateTotals`**: `totalImport += shipping_cost − shippingDiscount()` → margin (`_profit_margin_raw`) + cấp duyệt (`calculateLevel`) gồm VC.
- [x] **G3. FE edit `summaryBreakdown`**: `vanChuyen.nhap = shipBase − shippingCkValue`.
- [x] **G4. FE edit margin**: `marginPercent` + `marginPercentBeforeDiscount` bỏ trừ VC (dùng `tong.nhap`/`tong.truoc_vat`/`tong.sau_ck` trọn vẹn).
- [x] **G5. FE edit totals**: `totalImport` += giá nhập VC (sau CK); `totalSale` += `shippingCost`; `totalVat` += `shippingVatAmount` → footer Nhập/Bán/Sau CK/VAT/Sau VAT + bảng line-items TỔNG gồm VC, khớp BE.
- [x] **G6. FE edit hiển thị**: cell giá nhập VC (dòng IV) render `summaryBreakdown.vanChuyen.nhap` (theo quyền) thay "—"; bỏ nhãn "(không gồm VC)" ở 2 dòng TSLN.
- [x] **G7. FE view `_id/index.vue`**: cell giá nhập VC render `breakdown.van_chuyen.nhap`; `breakdownMarginBefore/After` bỏ trừ VC; bỏ nhãn "(không gồm VC)".
- [x] **G8. FE in `QuotationPrintPreview.vue`**: cell giá nhập VC render `breakdown.van_chuyen.nhap` thay "—".
- [x] **G9. Excel `bom_list.blade.php`**: dòng van_chuyen cột giá nhập render `$g['nhap']` thay "-".
- [x] **G10. Verify BE** `php -l` QuotationService + blade → No syntax errors.
- [ ] **G11. Verify E2E** (user): compile FE; báo giá có VC (3 chế độ CK) → giá nhập VC = sau CK ở edit/xem/in/excel; TSLN edit = TSLN xem = BE; cấp duyệt đổi đúng theo margin gồm VC; tổng (Sau VAT) khớp BE.

## Phase 9 — Sửa lại cấu trúc: VC chỉ vào dòng Tổng + Footer, KHÔNG vào bảng HH/DV

> User làm rõ: Phase 8 sai ở chỗ đẩy VC vào các computed của **bảng Hàng hoá/Dịch vụ phía trên**.
> Đúng: (a) bảng HH/DV phía trên thuần HH/DV; (b) VC + CK vận chuyển chỉ vào **dòng Tổng bảng Tổng hợp** + **Footer báo giá**; (c) **TSLN gồm VC** (không loại, để không bỏ sót giảm giá VC).
> Mô hình: line-based computeds = HH/DV (bảng trên). `summaryBreakdown.tong` = grand total gồm VC (Footer + dòng V + cấp duyệt + TSLN headline).

- [x] **H1. Revert pollution bảng trên**: `totalImport`/`totalSale`/`totalVat` bỏ cộng VC; `totalDiscountPerItem` bỏ `shippingCkValue` (revert BF3) → bảng line-items thuần HH/DV.
- [x] **H2. Cột CK method-2 bảng trên**: thêm `goodsAllocatedDiscount` + `goodsAutoAllocatedDiscount` (= total − phần SHIP) cho dòng TỔNG (633/634); giữ `totalAllocatedDiscount`/`totalAutoAllocatedDiscount` gồm SHIP cho logic phân bổ (allocationMatch/Đã phân bổ).
- [x] **H3. `totalDiscount` method-2** dùng `goodsAllocatedDiscount` → `totalSaleAfterDiscount` + `totalAfterVat` bảng trên thuần HH/DV.
- [x] **H4. TSLN bảng trên**: thêm `marginPercentGoods` (HH/DV = tong − vanChuyen) cho dòng TỔNG (636). Giữ `marginPercent`/`Before` GỒM VC cho Footer LN + dòng TSLN summary + cấp duyệt.
- [x] **H5. Footer báo giá** bind `summaryBreakdown.tong`: Nhập=tong.nhap, Bán=tong.truoc_vat, CK=tong.chiet_khau, Sau CK=tong.sau_ck (gồm VC).
- [x] **H6. `totalSaleVnd`** = `tong.sau_ck × rate` (gồm VC) → Footer ~VND + cấp duyệt order_value khớp BE; guard `clientLevelPreview` dùng `tong.sau_ck`.
- [x] **H7. Nhãn TSLN summary** (edit + view) bỏ "(không gồm VC)" (giờ gồm VC). Cell giá nhập VC vẫn = sau CK (G6/G7/G8/G9 giữ nguyên).
- [x] **H8. BE giữ nguyên** G1 (`van_chuyen.nhap = sau_ck`) + G2 (`totalImport += VC` → margin/calculateLevel/popup gồm VC). BE không có khái niệm "bảng HH/DV riêng" — grand total gồm VC là đúng cho popup gửi duyệt.
- [ ] **H9. Verify E2E** (user): bảng HH/DV phía trên KHÔNG đổi khi thêm VC; Footer + dòng V bảng Tổng hợp + TSLN + cấp duyệt phản ánh VC; method-1 & method-2 đều đúng; popup gửi duyệt khớp Footer.

## Phase 17 — Validate số tiền CK ≤ đơn giá bán (HH/DV/VC)

> Yêu cầu: số tiền CK (theo mặt hàng) không được lớn hơn đơn giá bán của hàng hoá / dịch vụ / chi phí vận chuyển.
> Hiện trạng: submit đã chặn (`validateDiscountPerItem` cho HH/DV; check `shippingDiscount > shippingCost` cho VC) nhưng THIẾU viền đỏ inline ở ô CK HH/DV (VC đã có inline).

- [x] **V1. Method `isItemDiscountInvalid(item)`**: method=1, `discount_amount > quoted_price` (dùng cho cả HH + DV).
- [x] **V2. Inline `is-invalid`** ô CK (% + ₫) của hàng hoá (parent) + dịch vụ, gate `discountTouched` (chỉ hiện sau submit đầu — theo CLAUDE.md form rule). VC giữ inline sẵn có.
- [x] **V3. Submit**: set `discountTouched=true`; message rõ "Số tiền CK không được lớn hơn đơn giá bán: ...".
- [ ] **V4. Verify** (user): CK theo mặt hàng, nhập CK > đơn giá bán HH/DV/VC → viền đỏ + chặn lưu + báo lỗi.

> Ghi chú: phạm vi method 1 (CK theo mặt hàng — per-unit). Method 2 (CK tổng) allocated tự phân bổ theo tỷ lệ nên không vượt; nếu cần chặn cả sửa tay allocated > thành tiền dòng thì báo thêm.

## Phase 16 — Phân hóa 2 nút phân bổ CK tổng (bỏ trùng logic)

> 2 nút "Phân bổ tự động" và "Phân bổ lại" trước đây trùng hoàn toàn (cùng gọi `handleAllocateDiscount`). Phân hóa vai trò theo trạng thái.

- [x] **A1. "Phân bổ tự động"**: `v-if="totalQuotationDiscount > 0 && totalAllocatedDiscount == 0"` (chỉ lần đầu, chưa phân bổ).
- [x] **A2. "Phân bổ lại"**: `v-if="totalQuotationDiscount > 0 && totalAllocatedDiscount > 0 && (allocationStale || !allocationMatch)"` (đã phân bổ nhưng lệch do đổi giá/đổi tổng CK). Mỗi lúc chỉ hiện tối đa 1 nút.
- [x] **A3. Cleanup**: bỏ method `handleReAllocateDiscount` (thừa); cả 2 nút gọi `handleAllocateDiscount`.
- [ ] **A4. Verify** (user): chưa phân bổ → chỉ "Phân bổ tự động"; phân bổ xong khớp → ẩn cả 2; đổi giá/tổng CK → hiện "Phân bổ lại".

## Phase 15 — CK tổng (%) tính base GỒM Chi phí vận chuyển

> Triệu chứng: nhập CK tổng theo %, giá trị tính trên "Tổng thành tiền trước VAT" nhưng base loại CPVC.
> Root cause: `qdAmountValue` (edit.vue) dùng base `this.totalSale` (HH/DV, đã loại VC ở Phase 9).
> Fix: base % = `totalSale + shippingCost` (= `summaryBreakdown.tong.truoc_vat`, gồm CPVC). 1 chỗ duy nhất — display/tổng/autoAllocation/payload đều qua `qdAmountValue`. BE không đổi (chỉ dùng `amount_value` FE gửi; allocateDiscount đã phân bổ gồm SHIP).

- [x] **D1. FE `qdAmountValue`**: base % = `totalSale + (shippingCost || 0)`.
- [ ] **D2. Verify E2E** (user): CK tổng theo % → Thành tiền CK = %×(HH+DV+CPVC); phân bổ tự động khớp; tổng sau CK đúng.

## Phase 14 — Màn /assign/product-project: thêm hàng hoá từ Báo giá tự lập đã duyệt

> Yêu cầu: ngoài hàng hoá từ BOM tổng hợp đã duyệt (`bom_list_products`), bổ sung hàng hoá từ Báo giá TỰ LẬP (type=2, không từ BOM, `bom_list_id` null) trạng thái Đã duyệt (status=4) — lấy từ `quotation_product_prices`.

- [x] **PP1. BE `ProductProjectController`**: gộp 2 nguồn qua **union khóa → phân trang → hydrate Eloquent** (vì TpModel/Brand/Origin/Unit ở DB thứ 2 → không JOIN cross-DB được).
  - `bomKeyQuery` / `quotationKeyQuery`: sub-query khóa `(source_type, row_id, sort_created)` + filter chung (`applyKeyFilters`).
  - `index`/`export`: `unionAll` → `fromSub` → orderBy `sort_created` → paginate/get → `hydrateAndTransform`.
  - `buildQuotationQuery` (Eloquent + relations `quotation.project/solution/creator.info`) + `transformQuotationItem` (cùng bộ field; "Mã BOM" = mã báo giá để truy nguồn; ERP sync = Chưa đồng bộ; id = `qtn_<id>` tránh trùng rowKey).
- [x] **PP2. Filter nhất quán 2 nguồn**: keyword/model/brand/origin/unit (cột hàng hoá), prospective_project_id (bom_lists.prospective_project_id / quotations.project_id), solution_id, created_by; erp_sync_status (BOM theo cột; báo giá tự lập coi như 0).
- [x] **PP3. Export blade**: tương thích sẵn (`$item['key'] ?? '—'`) — không sửa.
- [x] **PP4. Verify** `php -l` OK.
- [ ] **PP5. Verify E2E** (user): tạo báo giá tự lập + duyệt → hàng hoá hiện ở /assign/product-project; filter + phân trang + export đúng; hàng từ BOM không hồi quy.

## Phase 13 — Giá nhập CPVC do user tự nhập (thay vì suy ra = sau CK)

> Yêu cầu: cho user nhập "giá nhập" (giá vốn) riêng cho Chi phí vận chuyển; điều chỉnh mọi tính toán dùng giá nhập VC (TSLN, tổng giá nhập).
> Trước đây: giá nhập VC = sau CK (lợi nhuận VC = 0). Giờ: giá nhập VC độc lập → VC có thể có lãi/lỗ thật.

- [x] **I1. Migration** `2026_06_07_000001` thêm cột `shipping_import_price` decimal(18,2) default 0; backfill row cũ = `shipping_cost − shipping_discount − shipping_allocated_discount` (giữ TSLN cũ).
- [x] **I2. Entity** cast `shipping_import_price` decimal:2 (guarded=[] nên fillable sẵn).
- [x] **I3. BE compute**: `computeSummaryBreakdown` `van_chuyen.nhap = shipping_import_price`; `calculateTotals` `totalImport += shipping_import_price` (thay `shipping_cost − discount`) → TSLN + cấp duyệt dùng giá nhập user nhập.
- [x] **I4. BE persist** create (dòng 83) + update (mảng field) + **I5. Request** Store/Update rules `nullable|numeric|min:0` + **I6. Resource** trả `shipping_import_price`.
- [x] **I7. FE edit**: data `shippingImportPrice`; ô "Thành tiền nhập" dòng IV thành `V2BaseCurrencyInput` — hiện khi `canEdit` (người lập báo giá nhập/sửa, KHÔNG cần quyền Xem giá vốn); khi không edit → read-only theo `canViewCostPrice||hasUserCreatedProducts`. `summaryBreakdown.vanChuyen.nhap = shippingImportPrice`; load/reset/save payload; validate `< 0`.
- [x] **I8. View/Print/Excel**: tự cập nhật (đọc `van_chuyen.nhap` từ `summary_breakdown` BE) — không sửa.
- [x] **I9. Verify** `php -l` toàn bộ BE OK.
- [ ] **I10. Verify E2E** (user): `php artisan migrate`; nhập giá nhập VC → TSLN (edit/xem) + cấp duyệt phản ánh đúng; bảng HH/DV phía trên vẫn loại VC; in/excel hiển thị giá nhập VC = số đã nhập.

## Phase 12 — Bugfix: tạo báo giá từ tab "Hồ sơ" sai đơn vị tiền tệ

> Triệu chứng: Dự án TKT currency = USD → tab "Hồ sơ" (màn chi tiết dự án) → nút "Tạo báo giá" → báo giá ra VNĐ.
> Root cause: tab Hồ sơ gọi `createFromBom(bom_list_id)` → BE `QuotationService::createFromBom()` set `currency_id = $bomList->currency_id` (BOM default VND), KHÔNG lấy từ dự án. (FE create form từ tab "Báo giá" thì kế thừa đúng — khác entry point.)

- [x] **C1. BE `createFromBom`**: `currency_id` lấy theo **dự án** (`$project->currency_id ?: $bomList->currency_id`); tính `$exchangeRate` theo currency dự án; thêm `$bomRate` (tỷ giá BOM) để quy đổi giá đang lưu theo tiền tệ BOM.
- [x] **C2. Quy đổi giá sản phẩm tự nhập (non-ERP)**: `estimated_price = bp.estimated_price × bomRate / exchangeRate` (BOM-currency → tiền tệ báo giá). ERP vẫn quy từ VND base qua exchangeRate dự án.
- [x] **C3. Quy đổi giá dịch vụ/chi phí copy từ BOM**: `estimated_price = bsi.estimated_price × bomRate / exchangeRate`.
- [x] **C4. Verify** `php -l` OK. (FE không đổi — sau tạo điều hướng `/{id}/edit` đọc currency_id mới = USD.)
- [ ] **C5. Verify E2E** (user): dự án USD + Hồ sơ Đã duyệt → Tạo báo giá → màn edit hiển thị USD; giá ERP + tự nhập + dịch vụ đúng theo USD. Test thêm dự án VND (không hồi quy).

## Phase 11 — Toolbar báo giá gọn (không xuống 2 dòng)

- [x] **T1. edit.vue toolbar**: gap 12→8; "Chiết khấu:" → "CK:" + select 180→140 + rút gọn options ("Không CK"/"CK mặt hàng"/"CK tổng"); "Làm tròn giá" → "Làm tròn" + select 220→155 + rút gọn options ("Hàng nghìn (-3)"...); divider 24→20.
- [x] **T2. CSS compact**: `.price-toolbar` button (padding 3px 8px, font 12.5) + select/input (height 30, font 12.5) qua `::v-deep`.
- [x] **T3. VatBulkApplyToolbar.vue**: "Áp dụng VAT:" → "VAT:", input 100→70; "Áp cho tất cả" → "Tất cả" (+icon ri-checkbox-multiple-line); "Chỉ dòng VAT=0" → "VAT=0" (+icon ri-filter-line); thêm icon theo button-convention.
- [ ] **T4. Verify** (user): compile + toolbar 1 dòng ở màn rộng, text select không bị cắt.

## Phase 10 — Chuẩn hoá middleware checkPermission route duyệt báo giá

> Trace màn `/assign/quotations/pending-approval`: route BE chưa gắn `checkPermission` middleware (chỉ check ở Service). Bổ sung cho đúng convention CLAUDE.md.

- [x] **P1. Gắn middleware** (`Modules/Assign/Routes/api.php`):
  - `GET /pending-approval` → `checkPermission:Trưởng phòng duyệt giá Bom giải pháp|Ban giám đốc duyệt giá Bom giải pháp`
  - `POST /{id}/tp-approve` → `checkPermission:Trưởng phòng duyệt giá Bom giải pháp`
  - `POST /{id}/bgd-approve` → `checkPermission:Ban giám đốc duyệt giá Bom giải pháp`
  - `POST /{id}/reject` → `checkPermission:Trưởng phòng duyệt giá Bom giải pháp|Ban giám đốc duyệt giá Bom giải pháp`
  - Giữ nguyên `submit`/`self-approve` (creator-only, không có quyền tương ứng).
  - Quyền có sẵn trong seeder (id 1081/1082) — KHÔNG tạo migration. Verify: `php -l` OK, alias `checkPermission` đã đăng ký Kernel.

## Checkpoint

### Checkpoint — 2026-06-08 (Phase 8–17 CODE DONE)
Vừa hoàn thành (sau redesign tổng hợp ban đầu):
- **P7 (BF1/BF3)**: fix popup gửi duyệt làm tròn số; method=1 Tổng CK footer gồm CK vận chuyển.
- **P8–P9**: ĐẢO LOGIC VC theo ý user — VC tính vào TSLN + tổng giá trị, NHƯNG chỉ vào **dòng Tổng bảng Tổng hợp + Footer báo giá**, KHÔNG vào bảng HH/DV phía trên (tách `goods*` computed + `marginPercentGoods`; Footer + cấp duyệt bind `summaryBreakdown.tong`).
- **P10**: gắn middleware `checkPermission` route duyệt báo giá (pending-approval/tp-approve/bgd-approve/reject).
- **P11**: toolbar báo giá gọn 1 dòng (rút gọn text/select + CSS compact + VatBulkApplyToolbar).
- **P12**: fix currency tạo báo giá từ tab "Hồ sơ" (`createFromBom` lấy currency theo DỰ ÁN + quy đổi giá non-ERP/dịch vụ theo bomRate/exchangeRate).
- **P13**: giá nhập CPVC do user tự nhập (cột `shipping_import_price` + migration backfill; gate `canEdit`).
- **P14**: màn /assign/product-project gộp hàng hoá từ Báo giá tự lập đã duyệt (union khóa → hydrate Eloquent).
- **P15**: CK tổng (%) base GỒM CPVC.
- **P16**: phân hóa 2 nút phân bổ CK (tự động lần đầu / phân bổ lại khi lệch) — bỏ trùng.
- **P17**: validate inline số tiền CK ≤ đơn giá bán (HH/DV/VC).
Đang làm dở: (không)
Bước tiếp theo: ⏳ User `php artisan migrate` (cột `shipping_import_price` — migration `2026_06_07_000001`) + hard-refresh FE + E2E toàn bộ (xem mục Verify còn `[ ]` ở các Phase). Lưu ý có **2 quyết định UX chờ chốt**: (1) 2 nút phân bổ — đã chọn PA2; (2) còn lại đều theo default mình đề xuất.
Blocked:

### Checkpoint — 2026-06-05 (ALL CODE DONE — BE + FE + Excel)
Vừa hoàn thành: Toàn bộ code feature.
- BE: migration 4 cột + computeTotals/allocateDiscount cộng VC + computeSummaryBreakdown + persist/validate/Resource (summary_breakdown). `php -l` 6 file OK.
- FE edit (`_id/edit.vue`): data+computed VC, bảng Tổng hợp 6/7 cột động (HH/DV/CP/VC/Tổng), row IV inputs (trước VAT + %VAT + CK theo method), autoAllocationMap đưa VC vào base, load/save 4 field, validate inline.
- FE xem (`_id/index.vue`) + in (`QuotationPrintPreview.vue`): render bảng 6/7 cột từ `summary_breakdown` (fallback bảng cũ nếu thiếu).
- Excel (`QuotationController::exportExcel` + `bom_list.blade.php`): bảng nhóm chi phí (conditional, fallback bảng cũ — BOM export không vỡ). `php -l` OK.
Đang làm dở: (không)
Bước tiếp theo: ⏳ User: `php artisan migrate` (nếu chưa) → hard-refresh FE → E2E test (F8/F11/B12): VC ở 3 chế độ CK (null/per-item/CK tổng), kiểm bảng edit/xem/in/excel khớp + total_after_vat đúng + ẩn cột CK khi không CK.
Blocked:

### Checkpoint — 2026-06-05 (Phase 1 BE DONE)
Vừa hoàn thành: B1→B10. Migration 4 cột; cast; helper `shippingDiscount`; `computeTotals` cộng VC; `allocateDiscount` đưa VC vào base (ghi `shipping_allocated_discount`); `computeSummaryBreakdown` (4 nhóm + tổng, tách DV/CP qua `TpCost.revenue_calculation` theo `cost_id`); persist create/update + reset VC trong `clearDiscountData`; validate Store/Update; Resource trả 4 field + `summary_breakdown`. `php -l` 6 file OK.
Lưu ý: `revenue_calculation` KHÔNG ở `quotation_service_items` — tra qua `TpCost` theo `cost_id` (null/1→Dịch vụ, 0→Chi phí).
Đang làm dở: (không)
Bước tiếp theo: ⏳ User chạy `php artisan migrate` + smoke test API (tạo/sửa báo giá có VC ở 3 chế độ CK → kiểm `summary_breakdown` + total_after_vat). Sau đó sang Phase 2 FE (F1–F8).
Blocked: Chờ user migrate + xác nhận trước khi code FE.
