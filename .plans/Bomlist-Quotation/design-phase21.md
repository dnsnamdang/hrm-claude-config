# Phase 21: Update logic báo giá — Dịch vụ bổ sung + Cha-con + Làm tròn

> **Feature:** Bomlist-Quotation
> **Branch:** tpe-develop-assign
> **Ngày:** 2026-05-09

---

## 1. Tổng quan

6 thay đổi chính trên màn sửa/xem Báo giá:

| # | Yêu cầu | Tóm tắt |
|---|---------|---------|
| 1 | Thêm dòng dịch vụ bổ sung | Bảng riêng `quotation_service_items`, section cuối bảng |
| 2 | BOM kế thừa không sửa | Disable tên/mã/SL/ĐVT, ẩn nút xoá |
| 3 | Giá bán + VAT ở cha | Cha editable, con disable |
| 4 | VAT đồng loạt bỏ con | Skip children khi áp VAT |
| 5 | Export/Import Excel | Xuất y hệt UI, import theo logic cha-con mới |
| 6 | Làm tròn đơn giá | 3 tuỳ chọn, FE-only, persist khi Lưu |

---

## 2. Database — Migration

### 2.1 Bảng `quotation_service_items`

```php
Schema::create('quotation_service_items', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('quotation_id');
    $table->string('code', 50);           // DV-{quotation.code}-{NNN}
    $table->string('name');               // Tên dịch vụ
    $table->unsignedBigInteger('unit_id')->nullable(); // ĐVT
    $table->decimal('qty', 16, 2)->default(1);
    $table->decimal('estimated_price', 15, 2)->default(0); // Giá nhập
    $table->decimal('quoted_price', 15, 2)->default(0);    // Giá bán
    $table->decimal('vat_percent', 5, 2)->default(0);
    $table->text('note')->nullable();
    $table->integer('sort_order')->default(0);
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();

    $table->foreign('quotation_id')
          ->references('id')->on('quotations')
          ->onDelete('cascade');
    $table->index('quotation_id');
});
```

### 2.2 Mã tự sinh

Pattern: `DV-{quotation.code}-{NNN}` (3 chữ số, bắt đầu từ 001).

```php
// QuotationServiceItem::getNextCode($quotationCode)
$lastCode = self::where('code', 'like', "DV-{$quotationCode}-%")
    ->orderByRaw('CAST(SUBSTRING_INDEX(code, "-", -1) AS UNSIGNED) DESC')
    ->value('code');
$nextNum = $lastCode
    ? ((int) substr($lastCode, strrpos($lastCode, '-') + 1)) + 1
    : 1;
return sprintf("DV-%s-%03d", $quotationCode, $nextNum);
```

---

## 3. Backend

### 3.1 Entity `QuotationServiceItem`

**File:** `Modules/Assign/Entities/QuotationServiceItem.php`

```php
class QuotationServiceItem extends Model
{
    protected $fillable = [
        'quotation_id', 'code', 'name', 'unit_id', 'qty',
        'estimated_price', 'quoted_price', 'vat_percent',
        'note', 'sort_order', 'created_by', 'updated_by',
    ];

    protected $casts = [
        'qty' => 'decimal:2',
        'estimated_price' => 'decimal:2',
        'quoted_price' => 'decimal:2',
        'vat_percent' => 'decimal:2',
    ];

    protected $appends = ['import_total', 'sale_total', 'vat_amount', 'after_vat'];

    public function quotation() { return $this->belongsTo(Quotation::class); }
    public function unit() { return $this->belongsTo(\App\Models\Unit::class); }

    // Accessors
    public function getImportTotalAttribute() {
        return $this->estimated_price * $this->qty;
    }
    public function getSaleTotalAttribute() {
        return $this->quoted_price * $this->qty;
    }
    public function getVatAmountAttribute() {
        return $this->sale_total * $this->vat_percent / 100;
    }
    public function getAfterVatAttribute() {
        return $this->sale_total + $this->vat_amount;
    }

    public static function getNextCode($quotationCode) { /* xem 2.2 */ }
}
```

### 3.2 Quotation Entity — thêm relation

```php
// Quotation.php
public function serviceItems()
{
    return $this->hasMany(QuotationServiceItem::class)
                ->orderBy('sort_order');
}
```

### 3.3 QuotationController — CRUD dịch vụ bổ sung

**Thêm 3 method:**

```php
// POST /assign/quotations/{id}/service-items
public function storeServiceItem(Request $request, $id)
{
    $quotation = Quotation::findOrFail($id);
    // Validate status = DANG_TAO
    // Validate: name required, qty > 0, prices >= 0, vat 0-100
    // Auto-gen code
    // Create QuotationServiceItem
    // recomputeTotals
    // Return item
}

// PUT /assign/quotations/{id}/service-items/{itemId}
public function updateServiceItem(Request $request, $id, $itemId)
{
    // Validate status = DANG_TAO
    // Validate same rules
    // Update item
    // recomputeTotals
    // Return item
}

// DELETE /assign/quotations/{id}/service-items/{itemId}
public function deleteServiceItem($id, $itemId)
{
    // Validate status = DANG_TAO
    // Delete item
    // recomputeTotals
    // Return success
}
```

**Routes** (`Modules/Assign/Routes/api.php`):
```php
// Trong group quotations
Route::post('/{id}/service-items', [QuotationController::class, 'storeServiceItem']);
Route::put('/{id}/service-items/{itemId}', [QuotationController::class, 'updateServiceItem']);
Route::delete('/{id}/service-items/{itemId}', [QuotationController::class, 'deleteServiceItem']);
```

### 3.4 QuotationController::show — eager load service items

```php
// Thêm 'serviceItems.unit' vào with() khi load quotation
$quotation->load('serviceItems.unit');
```

### 3.5 QuotationService::computeTotals — cập nhật logic

**Thay đổi 1: Giá bán cha dùng trực tiếp (không roll-up từ con)**

```php
// CŨ (lines 250-260):
if ($hasChildren) {
    $lineSale = SUM(child.quoted_price × child.qty);
} else {
    $lineSale = product.quoted_price × product.qty;
}

// MỚI:
// Luôn dùng trực tiếp quoted_price × qty cho mọi parent/orphan
$lineSale = $product->quoted_price * $product->qty_needed;
```

**Thay đổi 2: Cộng thêm dịch vụ bổ sung vào tổng**

```php
// Sau loop products, thêm:
foreach ($quotation->serviceItems as $item) {
    $totalSale += $item->sale_total;
    $totalVat += $item->vat_amount;
}
$totalAfterVat = $totalSale + $totalVat;
```

### 3.6 QuotationController::exportExcel — cập nhật

**Thay đổi:**
- Không còn roll-up quoted_price cha từ con (dùng trực tiếp)
- Hàng hoá con: `quoted_price` và `vat_percent` để null (xuất ô trống)
- Truyền thêm `$serviceItems` vào BomListExport
- BomListExport truyền xuống blade

### 3.7 BomListExport — thêm support service items

```php
// Thêm property
protected $serviceItems = [];

public function withServiceItems($items) {
    $this->serviceItems = $items;
    return $this;
}

// view() truyền thêm serviceItems vào blade
```

### 3.8 bom_list.blade.php — thêm section dịch vụ bổ sung

```blade
{{-- Sau tất cả group/ungrouped, trước footer --}}
@if(count($serviceItems ?? []) > 0)
<tr class="group-row">
    <td colspan="{{ count($columns) }}" style="font-weight:bold; background:#f0f0f0;">
        Dịch vụ bổ sung
    </td>
</tr>
@foreach($serviceItems as $si => $item)
<tr>
    <td>{{ $si + 1 }}</td>
    <td>{{ $item->code }}</td>
    <td>{{ $item->name }}</td>
    {{-- Render đầy đủ: SL, ĐVT, Giá nhập, Thành tiền nhập, Giá bán, Thành tiền bán, ... --}}
</tr>
@endforeach
@endif
```

### 3.9 Import prices — cập nhật logic

**Thay đổi validate (Pass 1):**
- Dòng có mã `DV-*` → validate trong `quotation_service_items` thay vì BOM
- Hàng hoá cha: validate giá bán + VAT% (editable)
- Hàng hoá con: chỉ validate giá nhập (skip giá bán + VAT)

**Thay đổi validate (Pass 2):**
- Bỏ validate parent-child consistency cho quoted_price + vat_percent
- Giữ validate giá nhập cha = SUM con (nếu cần, hoặc bỏ luôn vì cha giá nhập roll-up)

**Thay đổi import:**
- Cha: update `quoted_price` + `vat_percent` vào `quotation_product_prices`
- Con: update `estimated_price` vào `quotation_product_prices` (bỏ quoted_price + vat_percent)
- Dòng `DV-*`: update vào `quotation_service_items`

**Bảng tổng hợp import:**

| Loại dòng | Giá nhập | Giá bán | VAT% |
|-----------|----------|---------|------|
| Cha (có con) | Skip (roll-up) | Import ✓ | Import ✓ |
| Con | Import ✓ | Skip | Skip |
| Orphan | Import ✓ | Import ✓ | Import ✓ |
| Dịch vụ bổ sung (DV-*) | Import ✓ | Import ✓ | Import ✓ |
| Nhóm (La Mã) | Skip | Skip | Skip |

### 3.10 File mẫu import — cập nhật

- Thêm dòng dịch vụ bổ sung vào cuối
- Hàng hoá con: lock cột Giá bán + VAT%
- Hàng hoá cha: unlock Giá bán + VAT% (đảo ngược so với hiện tại)

---

## 4. Frontend

### 4.1 Dòng dịch vụ bổ sung — Section cuối bảng

**File:** `hrm-client/pages/assign/quotations/_id/edit.vue`

**Template:** Sau tất cả grouped rows, thêm:
```html
<!-- Section dịch vụ bổ sung -->
<tr class="group-row">
    <td :colspan="totalColumns" class="font-weight-bold bg-light">
        Dịch vụ bổ sung
        <V2BaseButton v-if="canEdit" light size="sm" class="ml-2"
            @click="showAddServiceModal = true">
            <template #prefix><i class="ri-add-line"></i></template>
            Thêm dịch vụ
        </V2BaseButton>
    </td>
</tr>
<tr v-for="(svc, si) in serviceItems" :key="'svc-' + svc.id">
    <td>{{ si + 1 }}</td>
    <td>{{ svc.code }}</td>
    <td>
        <input v-if="canEdit" v-model="svc.name" class="form-control form-control-sm" />
        <span v-else>{{ svc.name }}</span>
    </td>
    <!-- SL, ĐVT, Giá nhập, Giá bán, VAT% — tất cả editable khi canEdit -->
    <!-- Nút xoá: chỉ hiện khi canEdit -->
</tr>
```

**Popup thêm dịch vụ:** Modal đơn giản với fields: Tên, SL, ĐVT, Giá nhập, Giá bán, VAT%, Ghi chú. Gọi API `POST /service-items`. Mã tự sinh từ BE.

**API calls:**
```javascript
// store
async addServiceItem(payload) {
    await this.$store.dispatch('apiPostMethod', {
        url: `assign/quotations/${this.quotationId}/service-items`,
        payload,
    })
    await this.fetchData()
}
// delete
async deleteServiceItem(itemId) {
    // Confirm trước
    await this.$store.dispatch('apiDeleteMethod', {
        url: `assign/quotations/${this.quotationId}/service-items/${itemId}`,
    })
    await this.fetchData()
}
```

### 4.2 BOM kế thừa — Disable thông tin

- Dòng BOM (cả cha/con/orphan): disable input tên, mã, SL, ĐVT
- Ẩn nút xoá cho dòng BOM
- Chỉ cho sửa giá theo logic cha-con mới (xem 4.3)

**Cách phân biệt:** Dòng BOM có `bom_list_product_id`, dòng dịch vụ bổ sung có `id` từ `quotation_service_items` và mã bắt đầu `DV-`.

### 4.3 Logic giá cha-con — Đảo ngược

**Sửa `refreshParentRollups()` (line ~690):**
```javascript
refreshParentRollups() {
    this.products.forEach(p => {
        if (p.parent_id) return  // skip children
        const children = this.products.filter(c => Number(c.parent_id) === Number(p.bom_list_product_id))
        if (!children.length) return  // skip orphans

        // Giá nhập vẫn roll-up từ con (GIỮ NGUYÊN)
        const totalImport = children.reduce((sum, c) => sum + (parseFloat(c.estimated_price) || 0) * (parseFloat(c.qty) || 0), 0)
        const parentQty = parseFloat(p.qty) || 1
        p.estimated_price = totalImport / parentQty

        // BỎ roll-up quoted_price + vat_percent — cha nhập tay
        // (xoá các dòng set p.quoted_price = ... và p.vat_percent = MAX(...))
    })
}
```

**Template — hàng hoá cha (có con):**
- `estimated_price`: disabled (auto roll-up)
- `quoted_price`: **editable** (nhập tay)
- `vat_percent`: **editable** (nhập tay)

**Template — hàng hoá con:**
- `estimated_price`: editable (giữ nguyên)
- `quoted_price`: **disabled** (ẩn input hoặc hiện text "—")
- `vat_percent`: **disabled** (ẩn input hoặc hiện text "—")

**Template — orphan (không cha không con):**
- Tất cả editable (giữ nguyên)

**Tính thành tiền cha:**
```javascript
// CŨ: lineSaleTotal roll-up từ con
// MỚI: dùng trực tiếp
lineSaleTotal(product) {
    return (parseFloat(product.quoted_price) || 0) * (parseFloat(product.qty) || 0)
}
```

### 4.4 VAT đồng loạt — Bỏ con

**Sửa `applyVatToProducts()`:**
```javascript
applyVatToProducts(vatPercent, mode) {
    const eligible = this.products.filter(p => {
        // BỎ hàng hoá con
        if (p.parent_id) return false
        if (mode === 'zero_only') return parseFloat(p.vat_percent) === 0
        return true
    })
    eligible.forEach(p => { p.vat_percent = vatPercent })

    // Áp cho cả dịch vụ bổ sung
    const svcEligible = this.serviceItems.filter(s => {
        if (mode === 'zero_only') return parseFloat(s.vat_percent) === 0
        return true
    })
    svcEligible.forEach(s => { s.vat_percent = vatPercent })

    this.vatBulkKey++
}
```

### 4.5 Làm tròn đơn giá

**UI:** Dropdown + nút "Làm tròn" trên toolbar (cạnh VAT đồng loạt).

```html
<div class="d-flex align-items-center ml-3" v-if="canEdit">
    <b-form-select v-model="roundingMode" size="sm" style="width:180px">
        <option :value="null" disabled>Chọn kiểu làm tròn</option>
        <option value="-1">Làm tròn hàng chục</option>
        <option value="0">Làm tròn số nguyên</option>
        <option value="1">Làm tròn 1 số thập phân</option>
    </b-form-select>
    <V2BaseButton light size="sm" class="ml-1" @click="confirmRounding"
        :disabled="roundingMode === null">
        <template #prefix><i class="ri-calculator-line mr-1"></i></template>
        Làm tròn
    </V2BaseButton>
</div>
```

**Data:**
```javascript
roundingMode: null, // -1 | 0 | 1
```

**Methods:**
```javascript
confirmRounding() {
    const labels = { '-1': 'hàng chục', '0': 'số nguyên', '1': '1 số thập phân' }
    // Dùng BaseConfirmModal hoặc confirm()
    // Message: "Bạn có chắc muốn làm tròn đến [label] cho toàn bộ đơn giá? Thao tác này không thể hoàn tác."
    // OK → applyRounding()
},

applyRounding() {
    const precision = parseInt(this.roundingMode)
    const round = (val, p) => {
        const factor = Math.pow(10, p)
        return Math.round(val * factor) / factor
    }

    // Áp cho dòng BOM
    this.products.forEach(p => {
        const isChild = !!p.parent_id
        const hasChildren = this.products.some(c => Number(c.parent_id) === Number(p.bom_list_product_id))

        // Giá nhập: round cho con + orphan (cha roll-up nên không round trực tiếp)
        if (!hasChildren) {
            p.estimated_price = round(parseFloat(p.estimated_price) || 0, precision)
        }

        // Giá bán: round cho cha + orphan (con không có giá bán)
        if (!isChild) {
            p.quoted_price = round(parseFloat(p.quoted_price) || 0, precision)
        }
    })

    // Roll-up lại giá nhập cha sau khi round con
    this.refreshParentRollups()

    // Áp cho dịch vụ bổ sung
    this.serviceItems.forEach(s => {
        s.estimated_price = round(parseFloat(s.estimated_price) || 0, precision)
        s.quoted_price = round(parseFloat(s.quoted_price) || 0, precision)
    })

    // Thành tiền sau VAT: tính lại tự động (computed) nên không cần round riêng
    // Nhưng nếu muốn round thành tiền sau VAT hiển thị:
    // → round lineAfterVat khi render (hoặc lưu precision vào data để computed dùng)

    this.vatBulkKey++ // force re-render
}
```

**Lưu ý thành tiền sau VAT:**
- Thành tiền sau VAT = (giá bán × SL) + VAT tiền → là computed value
- Sau khi round giá bán, thành tiền tự tính lại
- Nếu cần round thêm thành tiền sau VAT: lưu `roundingPrecision` vào data, khi render `lineAfterVat` thì dùng `round(value, precision)`

### 4.6 Trang xem chi tiết (show)

**File:** `hrm-client/pages/assign/quotations/_id/index.vue`

- Load thêm `serviceItems` từ API
- Hiển thị section "Dịch vụ bổ sung" cuối bảng (readonly)
- Hàng hoá con: Giá bán + VAT% hiện "—"
- Logic tính tổng giống edit

### 4.7 Save — Persist dịch vụ + giá đã làm tròn

**Sửa `save()` method:**
```javascript
async save(silent = false, { strict = false } = {}) {
    // ... validation hiện tại ...

    // Build payload products (giữ nguyên)
    // Thêm serviceItems vào payload
    const payload = {
        ...this.formData,
        products: this.buildProductsPayload(),
        service_items: this.serviceItems.map(s => ({
            id: s.id || null,
            name: s.name,
            unit_id: s.unit_id,
            qty: s.qty,
            estimated_price: s.estimated_price,
            quoted_price: s.quoted_price,
            vat_percent: s.vat_percent,
            note: s.note,
            sort_order: s.sort_order,
        })),
    }

    // Gọi PUT API
}
```

**BE update method:** Nhận `service_items` array → sync (upsert existing, create new, delete removed).

---

## 5. Tác động downstream

### 5.1 Lịch sử BOM (BomListLog)
- Thêm action mới cho dịch vụ bổ sung: `add_service`, `update_service`, `delete_service`
- Hoặc log chung vào quotation history (đơn giản hơn)

### 5.2 Duyệt giá
- `computeTotals()` đã gộp dịch vụ bổ sung → tổng giá trị dùng để xác định cấp duyệt đã chính xác
- Popup gửi duyệt hiện tổng → đã đúng

### 5.3 Version báo giá (snapshot)
- Snapshot cần bao gồm cả dịch vụ bổ sung
- Khi xem version cũ phải hiển thị đúng dịch vụ tại thời điểm duyệt

### 5.4 Điều chỉnh giá
- Khi tạo báo giá điều chỉnh (version mới), dịch vụ bổ sung kế thừa sang version mới

---

## 6. Edge cases

1. **Báo giá không có BOM products (chỉ dịch vụ):** Cho phép — tổng chỉ từ dịch vụ bổ sung
2. **Import file có mã DV-* không tồn tại:** Trả lỗi unmatched, skip dòng đó
3. **Làm tròn giá = 0:** Giữ nguyên 0, không lỗi
4. **Làm tròn nhiều lần:** Cho phép, mỗi lần round trên giá trị hiện tại (có thể thay đổi thêm)
5. **Xoá dịch vụ bổ sung khi đang sửa (chưa lưu):** FE xoá khỏi array, khi Lưu thì BE sync (dịch vụ bị xoá sẽ bị delete)
6. **Cha không có con (orphan):** Logic giữ nguyên — editable tất cả
7. **Cha có con nhưng tất cả con bị ẩn (filter):** Vẫn dùng logic cha-con, không thay đổi
