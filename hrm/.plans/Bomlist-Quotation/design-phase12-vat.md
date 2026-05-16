# Design Phase 12 — Quản lý VAT cho Báo giá

**Ngày brainstorm:** 2026-04-19
**Người phụ trách:** @dnsnamdang
**Branch:** `tpe-develop-assign` (cả API + Client)

---

## 1. Scope & Nguyên tắc

### 1.1 Mục tiêu

Bổ sung quản lý thuế VAT cho từng dòng sản phẩm trong báo giá (module Assign / BomList-Quotation). Hỗ trợ:

- Nhập VAT(%) tự do cho từng sản phẩm có giá bán.
- Chỉ áp VAT ở dòng sản phẩm CHA (với cấu trúc 2 cấp CHA → CON).
- 2 cơ chế áp VAT đồng loạt nhanh: soft-prompt lần đầu + toolbar thủ công.
- Hiển thị Tiền VAT + Thành tiền sau VAT ở mọi màn view/export.

### 1.2 Quyết định đã chốt qua brainstorming

| # | Điểm | Quyết định |
|---|---|---|
| 1 | VAT input | **Nhập số tự do** — cột `vat_percent` decimal(5,2) trên `quotation_product_prices`. Không dùng master table `tax_rates`. |
| 2 | Giá CHA khi có CON | **Roll-up:** CHA có CON → input `quoted_price` CHA bị disable, Thành tiền CHA = tổng Thành tiền CON. VAT áp trên Thành tiền CHA roll-up. TỔNG báo giá = sum CHA (roll-up). |
| 3 | Default VAT% | **0%** + soft-prompt khi nhập ≠ 0 lần đầu trong session (hỏi áp cho các dòng còn 0%). |
| 4 | Tính trước/sau VAT | **Trước VAT** — Tỷ suất LN + V (giá trị đơn hàng) + Cấp duyệt đều tính từ `totalSale` trước VAT. Tổng VAT + Tổng sau VAT chỉ là thông tin tham khảo, không ảnh hưởng cấp duyệt. |
| 5 | UX bulk apply thủ công | Toolbar gọn trên bảng: `[VAT đồng loạt: [__%]  [Áp cho tất cả]  [Chỉ dòng VAT=0]]`. 2 button riêng cho 2 scenario phổ biến. |
| 6 | Phạm vi | **Full coverage** — edit + show báo giá + list báo giá + tab "Báo giá" ở dự án tiền khả thi + export Excel + history log. |

### 1.3 Breaking change

- Schema: thêm 1 cột `quotation_product_prices.vat_percent` + 2 cột `quotations.total_vat_amount` + `total_after_vat`.
- Logic giá CHA-có-CON đổi: giá CHA không lưu riêng nữa (BE force = 0), Thành tiền CHA = sum CON. Báo giá nháp cũ (status 1/2/3) giữ giá CHA trong DB nhưng không dùng — khi mở lại edit + save, BE clear về 0.
- Báo giá đã duyệt (status=4) giữ nguyên 100%, `total_vat_amount = 0`, `total_after_vat = total_sale` (không sửa lại lịch sử).

### 1.4 Không làm

- Không dùng master table `tax_rates` (DB2 `mysql2`) — nhập tự do.
- Không gate VAT theo `can_view_import_price` — VAT là info công khai cho khách.
- Không log mỗi lần user nhập VAT vào 1 dòng — chỉ log bulk apply + save_draft (meta bao gồm `total_vat_amount`).
- Không thêm permission mới.

---

## 2. Data model

### 2.1 Migration 1 — `2026_04_19_100001_add_vat_to_quotation_product_prices.php`

```php
public function up() {
    Schema::table('quotation_product_prices', function (Blueprint $t) {
        $t->decimal('vat_percent', 5, 2)->default(0)->after('quoted_price')
          ->comment('VAT % — chỉ có giá trị ở dòng CHA hoặc dòng độc lập; CON luôn = 0');
    });
}

public function down() {
    Schema::table('quotation_product_prices', function (Blueprint $t) {
        $t->dropColumn('vat_percent');
    });
}
```

### 2.2 Migration 2 — `2026_04_19_100002_add_vat_totals_to_quotations.php`

```php
public function up() {
    Schema::table('quotations', function (Blueprint $t) {
        $t->decimal('total_vat_amount', 18, 2)->default(0)->after('sales_note')
          ->comment('Tổng tiền VAT (currency gốc của quotation, không quy VND)');
        $t->decimal('total_after_vat', 18, 2)->default(0)->after('total_vat_amount')
          ->comment('Tổng bán sau VAT = totalSale + total_vat_amount');
    });
}
```

Lý do cache 2 field trên `quotations`: list báo giá + tab "Báo giá" ở dự án cần sort/filter nhanh theo Tổng sau VAT, không tính lại từ productPrices mỗi request.

### 2.3 Công thức (canonical — cả BE và FE tham chiếu mục này)

**Định danh row:**
- `isParentWithChildren(row)`: `row.parent_id = null` AND tồn tại record khác cùng quotation có `parent_id = row.id`.
- `isOrphan(row)`: `row.parent_id = null` AND không có children.
- `isChild(row)`: `row.parent_id ≠ null`.

**Per row:**
```
lineImportTotal(row) = row.estimated_price × row.qty_needed         // giữ nguyên logic cũ

lineSaleTotal(row):
  if isParentWithChildren(row):
      return Σ lineSaleTotal(child) for child in row.children       // NEW — roll-up
  else:
      return row.quoted_price × row.qty_needed

lineVatAmount(row):
  if isChild(row):
      return null                                                    // hiển thị "—"
  return lineSaleTotal(row) × (row.vat_percent / 100)

lineAfterVat(row):
  if isChild(row):
      return null
  return lineSaleTotal(row) + lineVatAmount(row)
```

**Tổng:**
```
totalImport = Σ lineImportTotal(row) for row in {orphans ∪ children}
totalSale   = Σ lineSaleTotal(row)   for row in {orphans ∪ parentsWithChildren}
totalVat    = Σ lineVatAmount(row)   for row in {orphans ∪ parentsWithChildren}
totalAfterVat = totalSale + totalVat
```

**Margin + Cấp duyệt (trước VAT):**
```
margin = (totalSale − totalImport) / totalSale × 100
V = totalSale × currency.exchange_rate                              // quy VND
levelV = lookup(configs.order_value, V)
levelM = lookup(configs.profit_margin, margin)
price_approval_level = max(levelV, levelM)
```

Lưu ý: `totalVat` và `totalAfterVat` KHÔNG tham gia tính margin hay cấp duyệt.

---

## 3. Workflow

Workflow BG (1 → 2/3 → 4, Từ chối → 1) không đổi. Chỉ bổ sung:

- Khi save nháp → `recomputeTotals` → persist `total_vat_amount + total_after_vat`.
- Bulk apply VAT → `quotation_histories.action = update_vat_bulk`.

---

## 4. Backend refactor

### 4.1 Entity updates (2 file)

- `QuotationProductPrice.php`: thêm `'vat_percent'` vào `$fillable`, cast `decimal:2`.
- `Quotation.php`: thêm `'total_vat_amount', 'total_after_vat'` vào `$fillable`, cast `decimal:2`.

### 4.2 `QuotationService.php` — 4 method đổi + 2 method mới

**`upsertPrices(Quotation $q, array $products)` (gọi từ `update`):**
- Với mỗi row:
  - **CHA-có-CON:** force `quoted_price = 0`, giữ `vat_percent` user nhập.
  - **CON:** force `vat_percent = 0`, giữ `quoted_price`.
  - **Orphan:** giữ nguyên cả 2.
- Sau upsert, gọi `recomputeTotals($q)`.

**`calculateLevel(Quotation $q)`:**
- Dùng công thức mục 2.3. Trả response bao gồm `total_import, total_sale, total_vat, total_after_vat, margin, level`.

**`recomputeTotals(Quotation $q)` — helper private NEW:**
- Load products + prices, tính `totalSale, totalVat, totalAfterVat`.
- Update `quotations.total_vat_amount`, `total_after_vat` (persist cache).

**`applyBulkVat(Quotation $q, float $vatPercent, string $mode)` — NEW:**
- Validate:
  - `$q->status == 1` — status ≠ 1 → 422 "Báo giá đã gửi, không thể sửa VAT".
  - `$q->created_by == auth()->id()` → 403 nếu không.
  - `$vatPercent ∈ [0, 100]` (form request đã validate, vẫn check defensive).
  - `$mode ∈ ['all', 'zero_only']`.
- Query eligible rows: `bom_list_products` có `parent_id = NULL` thuộc BOM của quotation (tức là CHA-có-CON hoặc orphan). Skip CON.
- Với mỗi eligible row:
  - Mode `all`: update/insert `quotation_product_prices.vat_percent = $vatPercent`.
  - Mode `zero_only`: chỉ update nếu record hiện tại (hoặc chưa tồn tại → coi = 0) có `vat_percent = 0`.
- Đếm `affected_count`.
- Gọi `recomputeTotals($q)`.
- Log `quotation_histories`: `action = update_vat_bulk`, meta:
  ```json
  {
      "vat_percent": 10,
      "mode": "zero_only",
      "affected_count": 7,
      "total_vat_before": 2500000,
      "total_vat_after": 4200000
  }
  ```
- Return `['affected_count' => N, 'products' => updatedList, 'totals' => [...]]`.

**`submit/selfApprove/tpApprove/bgdApprove`:** thêm 1 dòng `$this->recomputeTotals($q)` trước khi save status mới để cache luôn đúng.

### 4.3 Controller + Route + Form Request

**`QuotationController`:** thêm action:
```php
public function applyVatBulk(QuotationApplyVatBulkRequest $req, $id) {
    $q = Quotation::findOrFail($id);
    $result = $this->service->applyBulkVat($q, $req->vat_percent, $req->mode);
    return response()->json(['data' => $result]);
}
```

**Route (`Modules/Assign/Routes/api.php`):**
```php
Route::post('quotations/{id}/apply-vat-bulk', [QuotationController::class, 'applyVatBulk']);
```

**`QuotationApplyVatBulkRequest`:**
```php
public function rules() {
    return [
        'vat_percent' => 'required|numeric|min:0|max:100',
        'mode' => 'required|in:all,zero_only',
    ];
}
```

### 4.4 Transformers — 2 file cập nhật

**`DetailQuotationResource`:**
- Root: thêm `total_vat_amount`, `total_after_vat`.
- Mỗi product: thêm `vat_percent` (từ `quotation_product_prices`), `is_parent_with_children` (bool — BE compute, FE dùng để disable input).
- KHÔNG trả `line_vat_amount`, `line_after_vat` — FE tự compute để tránh sync bug.

**`QuotationResource` (list):**
- Thêm `total_after_vat` để cột list báo giá dùng.

### 4.5 History — constant mới

Thêm vào `QuotationHistory`:
```php
const ACTION_UPDATE_VAT_BULK = 'update_vat_bulk';
```

Không log từng lần user nhập VAT vào 1 dòng. `save_draft` action cũ mở rộng meta: `{..., total_vat_amount: N}`.

### 4.6 Excel Export — `QuotationController::exportExcel`

Sửa template blade tại chỗ: `resources/views/exports/bom_list.blade.php` (quotation hiện đang reuse template này qua `BomListExport` class — giữ reuse để maintain 1 template, không fork):
- Header: thêm 3 cột sau "Thành tiền bán" — VAT(%), Tiền VAT, Thành tiền sau VAT. Các cột này chỉ render khi dữ liệu truyền vào có trường VAT (template dùng `@if(isset($item->vat_percent))` để backward-compat cho export BOM thuần tuý nếu có).
- Body: CON hiển thị blank 3 ô (không "—" để kế toán xử lý số dễ).
- Footer: sau dòng "TỔNG" thêm 2 dòng: "Tổng VAT", "Tổng sau VAT".

---

## 5. Frontend refactor

### 5.1 Màn edit làm giá — `pages/assign/quotations/_id/edit.vue`

**Cột table** (thêm 3 cột cuối, sau "Tỷ suất LN"):
```
STT | Mã | Tên | SL | ĐVT | Giá nhập | Thành tiền nhập | Giá bán | Thành tiền bán | Tỷ suất LN | VAT(%) | Tiền VAT | Thành tiền sau VAT
```

**Row behavior:**
- **CHA-có-CON:** ô `quoted_price` `:disabled="true"` + tooltip "Tự động tính từ SP con". Ô `vat_percent` editable. Thành tiền bán + Tiền VAT + Thành tiền sau VAT computed từ roll-up.
- **CON:** 3 cột VAT(%), Tiền VAT, Thành tiền sau VAT render `"—"` (text-muted), không input.
- **Orphan:** tất cả editable như bình thường.

**Tooltip ℹ️ cạnh header `VAT(%)`:** "VAT chỉ áp dụng trên dòng sản phẩm cha hoặc sản phẩm độc lập. Sản phẩm con được cộng gộp vào cha."

**Toolbar "Áp VAT đồng loạt"** (section riêng nằm giữa info-card và table, component `VatBulkApplyToolbar.vue`):
```
Áp VAT đồng loạt:  [____] %   [Áp cho tất cả]   [Chỉ dòng VAT=0]
```
- Props: `:disabled`, `:quotation-id`.
- Events: emit `applied` sau khi call API thành công, payload `{ products, totals }` → parent update state.
- Button disabled khi `!canEdit` (status ≠ 1 hoặc không phải creator).
- Validate: input rỗng/âm/>100 → button disabled. Click OK → call `store.dispatch('quotation/applyVatBulk', ...)` → toast success → emit `applied`.

**Soft-prompt modal** (`VatFirstEntryPromptModal.vue`):
- Trigger: trong `@input` của VAT% input, kiểm tra:
  - `oldValue === 0 && newValue > 0`
  - `!this.vatPromptShownThisSession` (data flag)
  - `countZeroRows > 1` (trong quotation còn ≥ 2 row eligible có vat=0)
- Body: `Áp dụng [X]% VAT cho [N] sản phẩm còn đang để 0%?`
- 2 button:
  - `[Áp dụng tất cả dòng còn 0%]` → call bulk apply mode=`zero_only` với `X` vừa nhập → set flag.
  - `[Chỉ dòng này]` → close modal → set flag (không call API).
- Flag `vatPromptShownThisSession` = data-level trong edit.vue, reset khi component unmount/route change.

**Row TỔNG ở cuối bảng** (update):
```
| STT...Giá nhập (colspan=6) | Thành tiền nhập | Giá bán | Thành tiền bán | Tỷ suất LN | VAT(%) | Tiền VAT | Thành tiền sau VAT |
| TỔNG                       | totalImport     | —       | totalSale      | margin%    | —      | totalVat | totalAfterVat      |
```
Cell `Giá bán` + `VAT(%)` ở row TỔNG để trống. `totalVat` + `totalAfterVat` in đậm.

**Footer (bên ngoài bảng)** — GIỮ NGUYÊN, không thêm dòng VAT:
```
Tổng nhập:          xxx USD
Tổng bán:           xxx USD (xxx VND)
Tỷ suất LN:         x.xx%                   ← trước VAT
────────────────────────────────────────
Cấp duyệt dự kiến:  C2 — TP                 ← tính theo V trước VAT
```

**Computed mới:**
```js
isParentWithChildren(row)   // đã có, giữ nguyên
lineSaleTotal(row)          // đổi: if isParentWithChildren → sum(children.lineSaleTotal)
lineVatAmount(row)          // NEW: null nếu isChild; lineSaleTotal × vat_percent/100
lineAfterVat(row)           // NEW: null nếu isChild; lineSaleTotal + lineVatAmount
totalVat                    // NEW: Σ lineVatAmount qua {orphans ∪ parentsWithChildren}
totalAfterVat               // NEW: totalSale + totalVat
```

**Validate submit:**
- Giữ logic hiện có (check giá bán > 0 trên orphan + CON; skip CHA-có-CON).
- Không validate VAT bắt buộc — VAT = 0 hợp lệ.

### 5.2 Màn show báo giá — `pages/assign/quotations/_id/index.vue`

- Thêm 3 cột readonly vào bảng (CON render "—").
- Row TỔNG cuối bảng: thêm cell `totalVat` + `totalAfterVat`.
- Footer ngoài bảng: giữ nguyên, không thêm gì.

### 5.3 Màn list báo giá — `pages/assign/quotations/index.vue`

- Thêm cột **"Tổng sau VAT"** sau cột "Tổng giá trị" hiện có.
- Format: `{{ formatMoney(row.total_after_vat) }} {{ row.currency_code }}`.
- Thêm vào `availableColumns` cho ColumnCustomizationModal (default visible).

### 5.4 Tab "Báo giá" ở dự án tiền khả thi — `pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

- Thêm cột **"Tổng sau VAT"** sau cột "Tổng bán" hiện có.

### 5.5 Store — `store/quotation.js`

Thêm 1 action:
```js
async applyVatBulk({ dispatch }, { id, vat_percent, mode }) {
    return dispatch('apiPostMethod', {
        url: `assign/quotations/${id}/apply-vat-bulk`,
        payload: { vat_percent, mode },
    })
}
```

### 5.6 Component mới (2 file)

| File | Mục đích |
|---|---|
| `components/assign/quotation/VatBulkApplyToolbar.vue` | Toolbar mini: input + 2 button. Emit `applied` với payload response. |
| `components/assign/quotation/VatFirstEntryPromptModal.vue` | Modal soft-prompt lần đầu nhập VAT ≠ 0 |

### 5.7 Files impact tổng

| File | Change |
|---|---|
| `pages/assign/quotations/_id/edit.vue` | +3 cột, disable parent input, toolbar, soft-prompt, row TỔNG mở rộng, 4 computed mới |
| `pages/assign/quotations/_id/index.vue` | +3 cột readonly, row TỔNG mở rộng |
| `pages/assign/quotations/index.vue` | +1 cột, columnCustomization |
| `components/assign/.../ProspectiveProjectQuotationsTab.vue` | +1 cột |
| `store/quotation.js` | +1 action |
| `components/assign/quotation/VatBulkApplyToolbar.vue` | NEW |
| `components/assign/quotation/VatFirstEntryPromptModal.vue` | NEW |

---

## 6. Testing outline

### 6.1 Migration + schema
- [ ] `php artisan migrate` OK 2 migration mới.
- [ ] `DESCRIBE quotation_product_prices` có `vat_percent DECIMAL(5,2) DEFAULT 0`.
- [ ] `DESCRIBE quotations` có `total_vat_amount`, `total_after_vat`.
- [ ] Báo giá cũ load OK, tất cả `vat_percent = 0`.

### 6.2 BE — roll-up + VAT logic
- [ ] Orphan: giá 100, qty 2, VAT 10% → lineSale 200, lineVat 20, lineAfter 220.
- [ ] CHA-CON, CHA user nhập giá riêng = 500: save → DB `CHA.quoted_price = 0`. Reload edit → Thành tiền CHA = sum CON.
- [ ] CHA-CON, VAT = 10% CHA, 15% CON: save → DB `CON.vat_percent = 0`. Reload → CON VAT = 0.
- [ ] 2 orphan + 1 group CHA-3-CON: totalSale = orphan1 + orphan2 + sum(3 CON). Không double.
- [ ] `calculateLevel` trả 6 field `total_import, total_sale, total_vat, total_after_vat, margin, level`. Margin dùng `total_sale`.

### 6.3 BE — applyVatBulk
- [ ] `vat=10, mode=all`, 2 orphan + 1 CHA-2-CON → 3 row có vat=10 (2 orphan + 1 CHA), 2 CON vẫn vat=0.
- [ ] `mode=zero_only`, 1 orphan có vat=5 → giữ 5, các row khác update.
- [ ] `vat=-5` hoặc `vat=150` → 422.
- [ ] `mode` invalid → 422.
- [ ] Status=2 → 422 "không thể sửa VAT".
- [ ] User khác creator → 403.
- [ ] `quotation_histories` có record `action=update_vat_bulk` với đủ 5 meta key.

### 6.4 BE — recomputeTotals cache
- [ ] Save nháp → `total_vat_amount + total_after_vat` update đúng.
- [ ] Submit → approve → totals persist ở status=4.
- [ ] Reject về 1, user clear VAT → save → totals recompute = 0.

### 6.5 FE edit — core
- [ ] Mở edit: cột VAT hiển thị 0, Tiền VAT = 0, Thành tiền sau VAT = Thành tiền bán.
- [ ] CHA-có-CON: ô giá bán disabled, tooltip hover OK. VAT input editable.
- [ ] CON: 3 cell VAT hiện "—".
- [ ] Nhập VAT=10 ở orphan → Tiền VAT + Thành tiền sau VAT row update realtime. Row TỔNG update.

### 6.6 FE — soft-prompt
- [ ] Báo giá mới, nhập VAT=10 dòng 1 → **modal xuất hiện**.
- [ ] Click "Áp dụng tất cả dòng còn 0%" → tất cả eligible = 10.
- [ ] Nhập VAT=5 dòng khác sau đó → **KHÔNG prompt lần 2**.
- [ ] Click "Chỉ dòng này" → chỉ row đó = 10, flag set.
- [ ] Báo giá chỉ 1 row → nhập VAT → **không prompt** (countZeroRows ≤ 1).
- [ ] Reload → nhập VAT lần đầu → prompt lại (session-scoped).

### 6.7 FE — toolbar
- [ ] Nhập 15 + "Áp cho tất cả" → call mode=all → toast "Đã áp 15% cho N dòng".
- [ ] Nhập 8 + "Chỉ dòng VAT=0" → giữ dòng 15%, dòng 0 → 8.
- [ ] Nhập -5 → button disabled.
- [ ] Nhập 150 → button disabled.
- [ ] Input rỗng → button disabled.
- [ ] Status=2 → toolbar disabled.

### 6.8 FE — row TỔNG + footer
- [ ] Row TỔNG ở cuối bảng có 2 cell mới: Tiền VAT + Thành tiền sau VAT update realtime khi đổi VAT.
- [ ] Footer ngoài bảng giữ 4 mục (Tổng nhập, Tổng bán, Tỷ suất LN, Cấp duyệt) — KHÔNG thêm dòng VAT.
- [ ] Đổi `quoted_price` → Tỷ suất LN + Cấp duyệt update.
- [ ] Đổi `vat_percent` → Tỷ suất LN + Cấp duyệt **KHÔNG đổi** (tính trước VAT). Chỉ row TỔNG Tiền VAT + Thành tiền sau VAT update.
- [ ] Scenario totalSale=100M, margin=30% → Cấp duyệt = C2. Đổi VAT=10% → vẫn C2.

### 6.9 Show + list + tab dự án
- [ ] Show báo giá: 3 cột readonly đủ data, CON "—", row TỔNG đủ 2 cell mới.
- [ ] List báo giá: cột "Tổng sau VAT" = `total_sale + total_vat`.
- [ ] Column customization: toggle ẩn cột → state persist.
- [ ] Tab "Báo giá" dự án: cột "Tổng sau VAT" đúng.

### 6.10 Export Excel
- [ ] File mở được.
- [ ] 3 cột mới (VAT%, Tiền VAT, Thành tiền sau VAT).
- [ ] CON blank 3 ô.
- [ ] Footer 2 dòng mới: "Tổng VAT", "Tổng sau VAT".
- [ ] Format số + currency symbol đúng.

### 6.11 History
- [ ] Bulk apply → history có entry `action=update_vat_bulk`.
- [ ] Mở `QuotationHistoryModal` → thấy entry mới.
- [ ] Meta đủ: `vat_percent, mode, affected_count, total_vat_before, total_vat_after`.

### 6.12 Permission + edge cases
- [ ] User quyền "Xây dựng giá" không phải creator → edit readonly (input + toolbar disabled).
- [ ] User NV KD (`can_view_import_price=false`) mở show báo giá → thấy VAT(%), Tiền VAT, Thành tiền sau VAT (KHÔNG gate).
- [ ] Báo giá rỗng không có dòng → footer hiển thị 0 không crash.
- [ ] Báo giá toàn CHA-có-CON (không orphan): totalSale từ CHA roll-up, VAT áp CHA đúng.
- [ ] Báo giá 1 orphan VAT=0: totalVat=0, totalAfterVat=totalSale.

---

## 7. Thứ tự triển khai đề xuất (sẽ cụ thể hoá trong `plan-phase12.md`)

1. **BE migration + entity + service** (nhóm 12.1) — migration + model + `recomputeTotals` + `upsertPrices` + `calculateLevel` + `applyBulkVat` + smoke test `php artisan migrate` + tinker test service methods.
2. **BE controller + route + form request + transformer + history** (nhóm 12.2) — endpoint ready, Postman test.
3. **BE export Excel** (nhóm 12.3) — template blade update + smoke test xuất file.
4. **FE store + components mới** (nhóm 12.4) — action `applyVatBulk` + `VatBulkApplyToolbar.vue` + `VatFirstEntryPromptModal.vue`.
5. **FE edit.vue** (nhóm 12.5) — 3 cột, disable parent, toolbar integrate, soft-prompt integrate, row TỔNG, 4 computed.
6. **FE show + list + tab dự án** (nhóm 12.6) — 3 cột readonly / 1 cột list / 1 cột tab.
7. **Test thủ công end-to-end** (nhóm 12.7) — 12 module ở section 6.

---

## 8. Risks

1. **Báo giá nháp cũ (status 1-3) có `CHA.quoted_price` != 0 → user mở lại thấy Thành tiền CHA roll-up khác số user từng nhập.**  
   → Mitigation: khi load edit, hiển thị banner info nếu phát hiện `CHA.quoted_price > 0` (before save): "Giá CHA cũ bị thay thế bởi tổng SP con. Lưu để áp dụng."
2. **Soft-prompt không mở đúng lúc (trigger quá sớm/muộn).**  
   → Mitigation: test case 6.6 covers most scenarios. Session flag dùng data-level (không localStorage) để mỗi lần mở lại edit sẽ hỏi đầu phiên đúng 1 lần.
3. **Race condition applyBulkVat + user nhập VAT cùng lúc.**  
   → Mitigation: BE update atomic trong transaction, FE reload products từ response sau bulk apply (overwrite state local).
4. **Excel export format tiền VAT với 0% trông dư thừa.**  
   → Mitigation: nếu toàn báo giá VAT=0, vẫn in 3 cột nhưng giá trị = 0 (không ẩn dynamic — giữ template fixed dễ maintain).
5. **Cấp duyệt không đổi khi thay VAT gây khó hiểu cho user nếu spec công ty là theo sau VAT.**  
   → Mitigation: decision đã chốt trước VAT (chuẩn kế toán VN). Nếu sau này spec đổi, chỉ cần sửa 1 chỗ công thức margin + V trong `calculateLevel` + FE computed.
