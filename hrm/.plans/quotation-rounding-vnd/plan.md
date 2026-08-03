# Plan — Làm tròn báo giá theo tiền tệ (VNĐ khoá Số nguyên)

## Phase 1 — FE edit.vue (create + update)

- [x] **T1. Computed `isVndCurrency`** = `this.currencyCode === 'VND'`.
- [x] **T2. Init `roundingMode` theo currency** (trong `loadDetail`, thay dòng gán `roundingMode`): VNĐ → `'0'`; khác → giá trị đã lưu (`item.rounding_mode`) hoặc `null`.
- [x] **T3. Watcher `currencyCode`**: khi = 'VND' → ép `roundingMode='0'` (an toàn nếu currency resolve trễ; không clobber non-VND).
- [x] **T4. Template**: `<b-form-select v-model="roundingMode" :disabled="isVndCurrency">` + tooltip icon đổi động: VNĐ → "Đồng VNĐ mặc định làm tròn đến số nguyên"; khác → giữ text cũ.
- [x] **T5. Verify**: lint FE (không đổi công thức); `roundingPrecision` với mode '0' → precision 0 (số nguyên) áp cho formatMoney (thành tiền/thuế/tổng). Save gửi `rounding_mode=0` khi VNĐ.
- [ ] **T6. Verify E2E** (user): tạo báo giá dự án VNĐ → Làm tròn = "Số nguyên (0)" + mờ + tooltip; số tiền hiển thị số nguyên. Tạo báo giá USD → mặc định "tối đa 2 số lẻ", chọn kiểu khác được. Áp dụng cho cả báo giá độc lập lẫn từ BOM. Lưu → reload giữ đúng.

### Checkpoint — 2026-07-02
Vừa hoàn thành: T1–T5 (FE edit.vue: isVndCurrency + init theo currency + watcher + disable/tooltip). Tái dùng roundingPrecision cho tính toán. Không đụng BE/migration.
Đang làm dở: (không)
Bước tiếp theo: user build FE + E2E (T6).
Blocked:

## Phase 2 — FIX: ô NHẬP giá chưa làm tròn theo loại tiền tệ

> Sau khi select làm tròn hiển thị đúng (VNĐ=Số nguyên): các cell TỔNG/thành tiền/thuế đã làm tròn qua `formatMoney(roundingPrecision)`, NHƯNG ô NHẬP tiền (`V2BaseCurrencyInput`: giá nhập/bán, CK₫, CK phân bổ, CPVC, VAT₫) hiển thị raw 2 số lẻ → lệch với loại tiền tệ (VNĐ vẫn cho nhập thập phân).

- [x] **R1. `V2BaseCurrencyInput`** (Assign-only): thêm prop `precision` (Number|null, default null=giữ hành vi cũ). `formatCurrency` làm tròn theo precision (clamp ≥0, bỏ trailing zero như maximumFractionDigits). `onInput`: precision=0 → chặn nhập dấu "." (số nguyên).
- [x] **R2. edit.vue**: truyền `:precision="roundingPrecision"` cho các ô TIỀN (₫): estimated_price/quoted_price (parent/child/svc), discount_amount, allocated_discount_amount (parent/svc), qd.amount_value, shippingCost/shippingImportPrice/shippingDiscount/shippingAllocatedDiscount/shippingVatAmountModel. KHÔNG áp cho ô % (discount_percent, vat_percent, percent_value, shippingDiscountPercentModel, shippingVatPercent).
- [x] **R3. Verify**: VNĐ → roundingPrecision=0 → ô tiền chỉ nhập số nguyên; USD → precision 2. Ô % giữ nguyên. Tổng vẫn khớp formatMoney.
- [ ] **R4. Verify E2E** (user): báo giá VNĐ → ô giá nhập/bán/CK₫/CPVC không cho gõ thập phân, hiển thị số nguyên; USD → 2 số lẻ; VAT%/CK% vẫn nhập thập phân bình thường; tổng/thành tiền khớp.

### Checkpoint — 2026-07-02 (Phase 2)
Vừa hoàn thành: R1–R3. Prop precision cho V2BaseCurrencyInput + wire roundingPrecision vào ô tiền edit.vue.
Bước tiếp theo: user build FE + E2E (R4).
Blocked:

## Phase 3 — BUGFIX: nhận diện VNĐ sai (mã ERP là 'VNĐ' không phải 'VND')

> Root cause (đã query ERP `currencies`): tiền VNĐ có `code='VNĐ'` (ký tự đ), rate=1. Detection `currencyCode === 'VND'` → luôn false → chọn VNĐ nhưng select làm tròn không ép "Số nguyên (0)", ô nhập không integer, và dòng tỷ giá hiện nhầm cho VNĐ.

- [x] **X1. `isVndCurrency`**: chuẩn hoá mã `toUpperCase().replace(/Đ/g,'D')` rồi so `=== 'VND'` → khớp cả 'VND' lẫn 'VNĐ' (và null→fallback 'VND').
- [x] **X2. Watcher `currencyCode`**: đổi `if (code === 'VND')` → `if (this.isVndCurrency)`.
- [x] **X3. Dòng tỷ giá** (edit.vue): `v-if="currencyCode !== 'VND'"` → `v-if="!isVndCurrency"` (không hiện tỷ giá cho VNĐ).
- [x] **X4. View + Print + list** (index.vue, QuotationPrintPreview.vue): tỷ giá/điều kiện VNĐ chuẩn hoá tương tự (dùng helper isVnd chung).
- [ ] **X5. Verify E2E** (user): tạo báo giá chọn VNĐ → select làm tròn = "Số nguyên (0)" + disable; ô tiền integer; không hiện dòng tỷ giá. Chọn USD → 2 số lẻ + hiện tỷ giá.

### Checkpoint — 2026-07-02 (Phase 3)
Vừa hoàn thành: X1–X4. Fix nhận diện VNĐ ('VNĐ' code) toàn bộ edit + view + print.
Bước tiếp theo: user build FE + E2E (X5).
Blocked:

## Phase 4 — Tinh chỉnh làm tròn cho tiền tệ khác VNĐ

> 2 điểm: (1) đổi giữa 2 ngoại tệ CÓ phần lẻ (USD↔EUR) → giữ lựa chọn làm tròn; (2) tiền tệ KHÔNG phần lẻ (JPY/KRW) → mặc định "Số nguyên (0)" nhưng vẫn cho đổi.

- [x] **Y1. Data + computed**: `zeroDecimalCurrencyCodes = ['JPY','KRW','KWR']`; `isZeroDecimalCurrency` (chuẩn hoá code); `currencyDefaultRounding` = (VNĐ||không-lẻ) ? '0' : null.
- [x] **Y2. Init/reset paths** (initCreateMode, selectProject, loadDetail fallback): dùng `currencyDefaultRounding` → JPY mặc định '0'; USD null; giữ giá trị đã lưu khi Sửa.
- [x] **Y3. handleChangeCurrency**: loại không-lẻ (VNĐ/JPY/KRW) → '0'; từ không-lẻ→có-lẻ → null; **có-lẻ↔có-lẻ (USD↔EUR) → giữ nguyên** roundingMode.
- [x] **Y4. Select disabled**: giữ `:disabled="isVndCurrency"` → JPY/KRW default '0' nhưng **vẫn cho đổi** (chỉ VNĐ khoá).
- [ ] **Y5. Verify E2E** (user): USD chọn "1 số lẻ" → đổi sang EUR → vẫn "1 số lẻ"; chọn JPY → mặc định "Số nguyên (0)" (cho đổi được); JPY→USD → về "2 số lẻ"; VNĐ vẫn khoá '0'.

### Checkpoint — 2026-07-03 (Phase 4)
Vừa hoàn thành: Y1–Y4. Giữ lựa chọn khi đổi ngoại tệ có-lẻ + JPY/KRW mặc định số nguyên (editable).
Bước tiếp theo: user build FE + E2E (Y5).
Blocked:
