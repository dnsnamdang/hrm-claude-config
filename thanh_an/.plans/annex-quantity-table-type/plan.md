# Phụ lục thay đổi số lượng — 2 kiểu bảng Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép mỗi phụ lục thay đổi số lượng chọn Kiểu A (SL sau đ/c) hoặc Kiểu B (SL điều chỉnh), áp dụng cho form nhập liệu và bản in.

**Architecture:** Lưu `table_type` trong cột `data` JSON của `contract_annexes` (không cần migration). FE dùng radio toggle trên ProductComponent để chuyển đổi giữa 2 bộ cột. BE print template dùng `@if` để render bảng tương ứng.

**Tech Stack:** Laravel 8, Vue 2, Bootstrap-Vue, Blade template

**Status:** Hoàn thành

### Checkpoint — 2026-05-09
Vừa hoàn thành: Task 8 — test E2E + fix bug phát sinh
Đã fix trong session này:
- BE validation: `qty` required → conditional theo `table_type` (store + update)
- BE store/update: `$new['qty']` → dùng `adjust_qty` khi Kiểu B
- BE approve: toàn bộ logic xử lý `$new['qty']` → hỗ trợ Kiểu B (`adjust_qty`)
- BE DetailResource: trả thêm `adjust_qty`, `adjust_amount` cho mỗi product
- BE print: tính `adjustedQty = contractQty + adjust_qty` cho Kiểu B
- FE ProductComponent: thay `confirm()` bằng `b-modal` Bootstrap-Vue
- FE GeneralComponent: fix lỗi CKEditor init — bọc `$nextTick` + guard `$refs.editor`
Bước tiếp theo: Không còn
Blocked: (không)

---

## File Map

| File | Vai trò | Thay đổi |
|------|---------|----------|
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/components/ProductComponent.vue` | Bảng hàng hóa chính | Thêm toggle, 2 cột mới, logic ẩn/hiện, changeProduct, tổng nhóm, confirm khi chuyển kiểu |
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/add.vue` | Tạo mới phụ lục | Set `table_type = 2` mặc định, gửi `table_type` lên API |
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/edit.vue` | Sửa phụ lục | Load `table_type` từ API, gửi `table_type` khi save |
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/index.vue` | Chi tiết phụ lục | Load `table_type` từ API |
| `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexQuantityDetailResource.php` | API response chi tiết | Trả `table_type` |
| `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php` | Controller store/update/print | Lưu `table_type`, truyền vào print view |
| `hrm-thanhan-api/resources/views/prints/contract-annex-qty-print.blade.php` | Template in phụ lục | Thêm @if cho Kiểu B |

---

### Task 1: BE — DetailResource trả `table_type`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexQuantityDetailResource.php:24-123`

- [ ] **Step 1: Thêm `table_type` vào response**

Trong method `toArray`, sau dòng `$annexData = collect($this->data);` (line 24), thêm logic lấy `table_type`. Rồi thêm vào mảng return.

Tìm đoạn:
```php
$annexData = collect($this->data);
```

Thay bằng:
```php
$rawData = is_string($this->data) ? json_decode($this->data, true) : (is_array($this->data) ? $this->data : []);
$tableType = $rawData['table_type'] ?? 1;
$annexData = collect($this->data);
```

Rồi trong mảng return (line 104-123), thêm `table_type`:
```php
return [
    'id' => $this->id,
    'code' => $this->code,
    'annex_no' => $this->annex_no,
    'contract_id' => $this->contract_id,
    'contract' => $data,
    'table_type' => $tableType,
    // ... giữ nguyên các field khác
];
```

- [ ] **Step 2: Verify**

Kiểm tra API bằng cách gọi `GET /api/v1/category/contract_annex_quantity/{id}` — response phải có field `table_type` (mặc định = 1 cho phụ lục cũ).

---

### Task 2: BE — Controller lưu `table_type` trong store/update

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php:49-175`

- [ ] **Step 1: Sửa method `store` — lưu `table_type` vào data JSON**

Hiện tại `$annex->data = $request->products;` (line 104) chỉ lưu mảng products. Cần thay đổi để lưu cả `table_type`.

Tìm đoạn trong store (line 104):
```php
$annex->data = $request->products;
```

Thay bằng:
```php
$annex->data = [
    'table_type' => $request->input('table_type', 2),
    'products' => $request->products,
];
```

- [ ] **Step 2: Sửa method `update` — lưu `table_type` vào data JSON**

Tìm đoạn trong update (line 161):
```php
$annex->data = $request->products;
```

Thay bằng:
```php
$annex->data = [
    'table_type' => $request->input('table_type', 2),
    'products' => $request->products,
];
```

- [ ] **Step 3: Cập nhật DetailResource để đọc đúng cấu trúc data mới**

Vì data giờ là `{ table_type: X, products: [...] }` thay vì `[...]`, cần sửa DetailResource.

Trong `ContractAnnexQuantityDetailResource.php`, tìm:
```php
$rawData = is_string($this->data) ? json_decode($this->data, true) : (is_array($this->data) ? $this->data : []);
$tableType = $rawData['table_type'] ?? 1;
$annexData = collect($this->data);
```

Thay bằng:
```php
$rawData = is_string($this->data) ? json_decode($this->data, true) : (is_array($this->data) ? $this->data : []);
$tableType = $rawData['table_type'] ?? 1;
// Backward compatible: phụ lục cũ data là array products, phụ lục mới data là { table_type, products }
$productsArray = isset($rawData['products']) ? $rawData['products'] : $rawData;
$annexData = collect($productsArray);
```

- [ ] **Step 4: Cập nhật Controller approve/print để đọc đúng cấu trúc data mới**

Trong method `approve` (line 193):
```php
$annexData = collect($annex->data);
```

Thay bằng:
```php
$rawAnnexData = is_array($annex->data) ? $annex->data : (is_string($annex->data) ? json_decode($annex->data, true) : []);
$annexProducts = isset($rawAnnexData['products']) ? $rawAnnexData['products'] : $rawAnnexData;
$annexData = collect($annexProducts);
```

Trong method `print` (line 411):
```php
$annexQtyMap = collect($annex->data)->keyBy('contract_product_id');
```

Thay bằng:
```php
$rawAnnexData = is_array($annex->data) ? $annex->data : (is_string($annex->data) ? json_decode($annex->data, true) : []);
$tableType = $rawAnnexData['table_type'] ?? 1;
$annexProducts = isset($rawAnnexData['products']) ? $rawAnnexData['products'] : $rawAnnexData;
$annexQtyMap = collect($annexProducts)->keyBy('contract_product_id');
```

- [ ] **Step 5: Verify**

Test tạo phụ lục mới → kiểm tra `data` trong DB phải có dạng `{"table_type": 2, "products": [...]}`. Kiểm tra xem phụ lục cũ (data dạng mảng) vẫn hiển thị bình thường.

---

### Task 3: BE — Print template hỗ trợ Kiểu B

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php:399-464` (method print)
- Modify: `hrm-thanhan-api/resources/views/prints/contract-annex-qty-print.blade.php`

- [ ] **Step 1: Controller print — truyền `tableType` và xử lý data Kiểu B**

Sau khi đã có `$tableType` từ Task 2 Step 4, cần truyền vào view và tính toán cho Kiểu B.

Tìm đoạn build products array trong print (khoảng line 430-441):
```php
$products[] = [
    'product_name' => $product['product_name'],
    'product_trade_name' => $product['product_trade_name'] ?? '',
    'producer_country' => $product['producer_country'] ?? '',
    'specification' => $product['specification'] ?? '',
    'unit_name' => isset($product['unit_id']) ? (Unit::find($product['unit_id'])->name ?? '') : '',
    'contract_qty' => $contractQty,
    'adjusted_qty' => $adjustedQty,
    'price' => $price,
    'amount_before' => $amountBefore,
    'amount_after' => $amountAfter,
];
```

Thêm field `adjust_qty` và `adjust_amount` cho Kiểu B:
```php
$adjustQty = 0;
$adjustAmount = 0;
if ($tableType == 2 && $annexQtyMap->has($contractProductId)) {
    $adjustQty = $annexQtyMap[$contractProductId]['adjust_qty'] ?? 0;
    $adjustAmount = $price * $adjustQty;
}

$products[] = [
    'product_name' => $product['product_name'],
    'product_trade_name' => $product['product_trade_name'] ?? '',
    'producer_country' => $product['producer_country'] ?? '',
    'specification' => $product['specification'] ?? '',
    'unit_name' => isset($product['unit_id']) ? (Unit::find($product['unit_id'])->name ?? '') : '',
    'contract_qty' => $contractQty,
    'adjusted_qty' => $adjustedQty,
    'price' => $price,
    'amount_before' => $amountBefore,
    'amount_after' => $amountAfter,
    'adjust_qty' => $adjustQty,
    'adjust_amount' => $adjustAmount,
];
```

Truyền `$tableType` vào view:
Tìm:
```php
$result['CHI_TIET_HANG_HOA'] = view('prints.contract-annex-qty-print', compact('products'))->render();
```

Thay bằng:
```php
$result['CHI_TIET_HANG_HOA'] = view('prints.contract-annex-qty-print', compact('products', 'tableType'))->render();
```

Đồng thời, với Kiểu B, `GIA_TRI_HOP_DONG_SAU_DIEU_CHINH` cần tính khác:
```php
if ($tableType == 2) {
    $tongThanhTienDieuChinh = array_sum(array_column($products, 'adjust_amount'));
    $result['GIA_TRI_HOP_DONG_SAU_DIEU_CHINH'] = number_format($tongThanhTienDieuChinh);
}
```

- [ ] **Step 2: Blade template — thêm Kiểu B**

Thay toàn bộ file `contract-annex-qty-print.blade.php` thành:

```blade
<div class="body">
    <div class="row">
        <table class="main-table" style="width: 100%; table-layout: fixed; font-size: 14px; border-collapse: collapse;">
            <thead>
                <tr>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 3%; padding: 2px;">STT</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 12%; padding: 2px;">Tên hàng hóa</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 10%; padding: 2px;">Tên thương mại</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 12%; padding: 2px;">Hãng, nước sản xuất</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 5%; padding: 2px;">Quy cách</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 4%; padding: 2px;">Đơn vị tính</td>
                    <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 5%; padding: 2px;">SL trên HD</td>
                    @if(($tableType ?? 1) == 2)
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 5%; padding: 2px;">SL điều chỉnh</td>
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 8%; padding: 2px;">Đơn giá bán (Gồm VAT)</td>
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 10%; padding: 2px;">Thành tiền</td>
                    @else
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 5%; padding: 2px;">SL sau đ/c</td>
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 8%; padding: 2px;">Đơn giá bán (Gồm VAT)</td>
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 10%; padding: 2px;">Thành tiền trên hđ</td>
                        <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 10%; padding: 2px;">Thành tiền sau đ/c</td>
                    @endif
                </tr>
            </thead>
            <tbody>
                @php
                $total_amount_before = 0;
                $total_amount_after = 0;
                $total_adjust_amount = 0;
                @endphp

                @foreach ($products as $k => $item)
                @php
                $total_amount_before += $item['amount_before'];
                $total_amount_after += $item['amount_after'];
                $total_adjust_amount += $item['adjust_amount'] ?? 0;
                @endphp
                <tr>
                    <td style="border: 1px solid black; text-align: center; padding: 2px; font-size: 13px;">{{ $k + 1 }}</td>
                    <td style="border: 1px solid black; padding: 2px; font-size: 13px; word-wrap: break-word;">{{ $item['product_name'] }}</td>
                    <td style="border: 1px solid black; padding: 2px; font-size: 13px; word-wrap: break-word;">{{ $item['product_trade_name'] }}</td>
                    <td style="border: 1px solid black; padding: 2px; font-size: 12px; word-wrap: break-word;">{{ $item['producer_country'] }}</td>
                    <td style="border: 1px solid black; padding: 2px; font-size: 13px;">{{ $item['specification'] }}</td>
                    <td style="border: 1px solid black; padding: 2px; font-size: 13px; text-align: center;">{{ $item['unit_name'] }}</td>
                    <td style="border: 1px solid black; text-align: center; padding: 2px; font-size: 13px;">{{ $item['contract_qty'] }}</td>
                    @if(($tableType ?? 1) == 2)
                        <td style="border: 1px solid black; text-align: center; padding: 2px; font-size: 13px;">{{ $item['adjust_qty'] }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-size: 12px;">{{ number_format($item['price']) }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-size: 12px;">{{ number_format($item['adjust_amount']) }}</td>
                    @else
                        <td style="border: 1px solid black; text-align: center; padding: 2px; font-size: 13px;">{{ $item['adjusted_qty'] }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-size: 12px;">{{ number_format($item['price']) }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-size: 12px;">{{ number_format($item['amount_before']) }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-size: 12px;">{{ number_format($item['amount_after']) }}</td>
                    @endif
                </tr>
                @endforeach

                <tr>
                    @if(($tableType ?? 1) == 2)
                        <td colspan="9" style="border: 1px solid black; text-align: center; padding: 2px; font-weight: bold; font-size: 13px;">Tổng cộng</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-weight: bold; font-size: 12px;">{{ number_format($total_adjust_amount) }}</td>
                    @else
                        <td colspan="9" style="border: 1px solid black; text-align: center; padding: 2px; font-weight: bold; font-size: 13px;">Tổng cộng</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-weight: bold; font-size: 12px;">{{ number_format($total_amount_before) }}</td>
                        <td style="border: 1px solid black; text-align: right; padding: 2px; font-weight: bold; font-size: 12px;">{{ number_format($total_amount_after) }}</td>
                    @endif
                </tr>
            </tbody>
        </table>
    </div>
</div>
```

- [ ] **Step 3: Verify**

Test in phụ lục cũ (không có `table_type`) → phải render Kiểu A giống như hiện tại. Test phụ lục mới (table_type=2) → phải render Kiểu B.

---

### Task 4: FE — ProductComponent thêm toggle và cột mới

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/components/ProductComponent.vue`

- [ ] **Step 1: Thêm 2 cột mới vào mảng `columns` trong `data()`**

Tìm cột cuối cùng trong mảng `columns` (line 446-451):
```javascript
{
    label: 'Thành tiền sau đ/c',
    key: 'amount',
    isVisible: true,
    isRequired: false,
},
```

Thêm ngay sau đó:
```javascript
{
    label: 'Số lượng điều chỉnh',
    key: 'adjust_qty',
    isVisible: false,
    isRequired: false,
},
{
    label: 'Thành tiền',
    key: 'adjust_amount',
    isVisible: false,
    isRequired: false,
},
```

- [ ] **Step 2: Thêm radio toggle trên bảng hàng hóa**

Tìm đoạn header bảng (line 5-12):
```html
<div class="col-md-12 mb-2 d-flex justify-content-between align-items-center">
    <h4 class="m-0">Danh sách hàng hóa</h4>
    <div class="d-flex align-items-center">
        <base-add-button @click="addGroupProduct" class="mr-1" v-if="!isShow" />
        <b-button v-b-toggle.filter-product variant="light" class="btn-icon ml-1">
            <img src="@/assets/images/file-icons/filter.svg" alt="Filter" class="icon-style" />
        </b-button>
    </div>
</div>
```

Thay bằng:
```html
<div class="col-md-12 mb-2 d-flex justify-content-between align-items-center">
    <h4 class="m-0">Danh sách hàng hóa</h4>
    <div class="d-flex align-items-center">
        <b-form-radio-group
            v-model="formSubmit.table_type"
            :options="tableTypeOptions"
            button-variant="outline-primary"
            size="sm"
            buttons
            class="mr-2"
            :disabled="isShow"
            @change="onTableTypeChange"
        ></b-form-radio-group>
        <base-add-button @click="addGroupProduct" class="mr-1" v-if="!isShow" />
        <b-button v-b-toggle.filter-product variant="light" class="btn-icon ml-1">
            <img src="@/assets/images/file-icons/filter.svg" alt="Filter" class="icon-style" />
        </b-button>
    </div>
</div>
```

- [ ] **Step 3: Thêm data và methods cho toggle**

Trong `data()`, thêm:
```javascript
tableTypeOptions: [
    { text: 'SL sau điều chỉnh', value: 1 },
    { text: 'SL điều chỉnh', value: 2 },
],
previousTableType: null,
```

Trong `methods`, thêm:
```javascript
onTableTypeChange(newValue) {
    const hasData = this.formSubmit.groups.some(g =>
        g.products.some(p => (Number(p.qty) || 0) > 0 || (Number(p.adjust_qty) || 0) > 0)
    )
    if (!hasData) {
        this.previousTableType = newValue
        this.applyTableTypeColumns()
        return
    }
    if (confirm('Chuyển kiểu bảng sẽ reset số lượng đã nhập về 0. Bạn có chắc?')) {
        this.formSubmit.groups.forEach(group => {
            group.products.forEach(product => {
                product.qty = 0
                product.adjust_qty = 0
                product.amount = 0
                product.adjust_amount = 0
            })
        })
        this.previousTableType = newValue
        this.applyTableTypeColumns()
    } else {
        this.$nextTick(() => {
            this.formSubmit.table_type = this.previousTableType
        })
    }
},
applyTableTypeColumns() {
    const isTypeB = this.formSubmit.table_type === 2
    this.fields = this.fields.map(f => {
        if (['qty', 'contract_amount', 'amount'].includes(f.key)) {
            return { ...f, isVisible: !isTypeB }
        }
        if (['adjust_qty', 'adjust_amount'].includes(f.key)) {
            return { ...f, isVisible: isTypeB }
        }
        return f
    })
},
```

- [ ] **Step 4: Gọi `applyTableTypeColumns` khi mount + watch**

Trong `mounted()`, thêm sau `await this.getFields()`:
```javascript
this.previousTableType = this.formSubmit.table_type || 1
this.applyTableTypeColumns()
```

Thêm watcher cho `formSubmit.table_type`:
```javascript
watch: {
    'formSubmit.table_type': {
        handler(newVal) {
            if (newVal) {
                this.applyTableTypeColumns()
            }
        },
        immediate: true,
    },
    // giữ nguyên watcher formSubmit hiện tại
}
```

- [ ] **Step 5: Thêm template render cho 2 cột mới**

Trong template loop `v-for="f in visibleFieldsExceptName"` (line 180-252), tìm đoạn sau `template v-else-if="f.key === 'amount'"` (line 234-236):
```html
<template v-else-if="f.key === 'amount'">
    {{ item.amount | formatNumber }}
</template>
```

Thêm ngay sau:
```html
<template v-else-if="f.key === 'adjust_qty'">
    <currency-input
        :item="item.adjust_qty"
        @update:item="
            (val) => {
                item.adjust_qty = val
                changeProduct(gIndex, pIndex, item)
            }
        "
        :disabled="isShow"
    />
    <base-helper-error
        :error="
            formError[
                'groups.' + gIndex + '.products.' + pIndex + '.adjust_qty'
            ]
        "
    />
</template>
<template v-else-if="f.key === 'adjust_amount'">
    {{ item.adjust_amount | formatNumber }}
</template>
```

- [ ] **Step 6: Sửa method `changeProduct` hỗ trợ Kiểu B**

Tìm method `changeProduct` (line 1064-1077):
```javascript
changeProduct(gIndex, index, product) {
    const qty = Number(product.qty) || 0
    const price = Number(product.price) || 0
    const price_discounted = Number(product.price_discounted) || 0

    // Tính amount
    this.formSubmit.groups[gIndex].products[index].amount = qty * price

    // Tính annex_price và amount_discounted
    const annex_price = price - price_discounted
    this.formSubmit.groups[gIndex].products[index].annex_price = annex_price
    this.formSubmit.groups[gIndex].products[index].amount_discounted = annex_price * qty
},
```

Thay bằng:
```javascript
changeProduct(gIndex, index, product) {
    const price = Number(product.price) || 0

    if (this.formSubmit.table_type === 2) {
        const adjustQty = Number(product.adjust_qty) || 0
        this.formSubmit.groups[gIndex].products[index].adjust_amount = price * adjustQty
    } else {
        const qty = Number(product.qty) || 0
        const price_discounted = Number(product.price_discounted) || 0
        this.formSubmit.groups[gIndex].products[index].amount = qty * price
        const annex_price = price - price_discounted
        this.formSubmit.groups[gIndex].products[index].annex_price = annex_price
        this.formSubmit.groups[gIndex].products[index].amount_discounted = annex_price * qty
    }
},
```

- [ ] **Step 7: Thêm method `getGroupTotalAdjustAmount` và cập nhật template tổng nhóm**

Trong methods, thêm:
```javascript
getGroupTotalAdjustAmount(group) {
    if (!group) return 0
    return (group.products || []).reduce((sum, product) => {
        const adjustAmount = Number(product.adjust_amount) || 0
        return sum + adjustAmount
    }, 0)
},
```

Tìm đoạn hiển thị tổng nhóm cho `amount` (line 268-269):
```html
<tbody
    v-if="visibleFieldsExceptName.some((f) => f.key === 'amount')"
    :key="`group-total-${gIndex}`"
>
```

Thay điều kiện v-if:
```html
<tbody
    v-if="visibleFieldsExceptName.some((f) => f.key === 'amount' || f.key === 'adjust_amount')"
    :key="`group-total-${gIndex}`"
>
```

Trong dòng tổng (line 286-308), tìm đoạn hiển thị amount:
```html
<span v-if="f.key === 'amount'" class="font-weight-bold text-primary">
    {{ getGroupTotalAmount(group) | formatNumber }}
</span>
```

Thêm ngay sau:
```html
<span v-if="f.key === 'adjust_amount'" class="font-weight-bold text-primary">
    {{ getGroupTotalAdjustAmount(group) | formatNumber }}
</span>
```

- [ ] **Step 8: Thêm class cho cột mới vào `getHeadClass`**

Tìm đoạn map trong `getHeadClass` (line 866-913), thêm:
```javascript
adjust_qty: 'td-width-100',
adjust_amount: 'td-width-150',
```

- [ ] **Step 9: Thêm `adjust_qty: 0, adjust_amount: 0` vào addProduct**

Tìm trong method `addProduct` (line 951), đoạn tạo item cho sản phẩm duplicate (line 960-992) và sản phẩm thường (line 1010-1042), thêm 2 field vào cả 2 object:

Sau `amount: 0,` thêm:
```javascript
adjust_qty: 0,
adjust_amount: 0,
```

Tương tự cho `handleImportSuccess` — tìm các chỗ tạo item object, thêm:
```javascript
adjust_qty: 0,
adjust_amount: 0,
```

- [ ] **Step 10: Verify**

Chạy dev server FE. Mở trang tạo phụ lục mới → thấy radio toggle. Click chuyển kiểu → cột thay đổi. Nhập SL điều chỉnh → thành tiền tính đúng.

---

### Task 5: FE — add.vue set `table_type = 2` mặc định và gửi lên API

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/add.vue:44-49`

- [ ] **Step 1: Set `table_type = 2` trong `formSubmit`**

Tìm formSubmit trong data() (line 44-49):
```javascript
formSubmit: {
    contract_id: null,
    annex_no: '',
    groups: [],
    contract: {},
},
```

Thay bằng:
```javascript
formSubmit: {
    contract_id: null,
    annex_no: '',
    groups: [],
    contract: {},
    table_type: 2,
},
```

- [ ] **Step 2: Gửi `table_type` lên API khi submit**

Tìm payload trong submitForm (line 94-108):
```javascript
await this.$store.dispatch('apiPostMethod', {
    url: `category/contract_annex_quantity`,
    payload: {
        contract_id: this.formSubmit.contract_id,
        products,
        annex_no: this.formSubmit.annex_no,
        print_template: this.formSubmit.print_template,
        print_template_id: this.formSubmit.print_template_id,
        print_template_type_id: this.formSubmit.print_template_type_id,
        status: status,
        total: this.$refs.general.$refs.product.$refs.total
            ? this.$refs.general.$refs.product.$refs.total.total
            : '',
    },
})
```

Thêm `table_type` vào payload:
```javascript
await this.$store.dispatch('apiPostMethod', {
    url: `category/contract_annex_quantity`,
    payload: {
        contract_id: this.formSubmit.contract_id,
        products,
        annex_no: this.formSubmit.annex_no,
        print_template: this.formSubmit.print_template,
        print_template_id: this.formSubmit.print_template_id,
        print_template_type_id: this.formSubmit.print_template_type_id,
        status: status,
        table_type: this.formSubmit.table_type,
        total: this.$refs.general.$refs.product.$refs.total
            ? this.$refs.general.$refs.product.$refs.total.total
            : '',
    },
})
```

Cũng cần sửa logic filter products: khi Kiểu B, cần filter theo `adjust_qty` thay vì `qty`. Tìm (line 63-65):
```javascript
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => item.qty > 0)
```

Thay bằng:
```javascript
const isTypeB = this.formSubmit.table_type === 2
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => isTypeB ? (item.adjust_qty > 0) : (item.qty > 0))
```

Và trong `.map()` bên dưới, khi Kiểu B cần gửi `adjust_qty` thay vì `qty`:
```javascript
.map((item) => {
    if (item.contract_product_id) {
        const result = {
            contract_product_id: item.contract_product_id,
            contract_qty: item.contract_qty,
        }
        if (isTypeB) {
            result.adjust_qty = item.adjust_qty
        } else {
            result.qty = item.qty
        }
        return result
    } else if (item.id && !item.is_new) {
        const result = {
            contract_product_id: item.id,
            contract_qty: item.contract_qty,
        }
        if (isTypeB) {
            result.adjust_qty = item.adjust_qty
        } else {
            result.qty = item.qty
        }
        return result
    } else {
        const result = {
            contract_product_id: null,
            product_id: item.product_id,
            contract_qty: 0,
            group_name: item.group_name,
            unit_id: item.unit_id,
            price: item.price || 0,
        }
        if (isTypeB) {
            result.adjust_qty = item.adjust_qty
        } else {
            result.qty = item.qty
        }
        return result
    }
})
```

---

### Task 6: FE — edit.vue load `table_type` và gửi lên API

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/edit.vue:55-181`

- [ ] **Step 1: Load `table_type` từ API response**

Tìm method getDetail (line 166-179):
```javascript
async getDetail() {
    this.isLoading = true
    const { data } = await this.$store.dispatch(
        'apiGetMethod',
        `category/contract_annex_quantity/${this.$route.params.id}`,
    )
    this.formSubmit = data
    this.formSubmit.groups = data.contract.groups
    this.isLoading = false
```

Thêm sau `this.formSubmit.groups = data.contract.groups`:
```javascript
this.formSubmit.table_type = data.table_type || 1
```

- [ ] **Step 2: Gửi `table_type` lên API khi save**

Tương tự add.vue. Tìm đoạn filter products (line 92-95):
```javascript
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => item.qty > 0)
```

Thay bằng:
```javascript
const isTypeB = this.formSubmit.table_type === 2
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => isTypeB ? (item.adjust_qty > 0) : (item.qty > 0))
```

Và `.map()` tương tự Task 5 Step 2.

Thêm `table_type` vào payload gửi API (line 120-133):
```javascript
payload: {
    products,
    annex_no: this.formSubmit.annex_no,
    print_template: this.formSubmit.print_template,
    print_template_id: this.formSubmit.print_template_id,
    print_template_type_id: this.formSubmit.print_template_type_id,
    status: status,
    table_type: this.formSubmit.table_type,
    total: ...
},
```

---

### Task 7: FE — index.vue (chi tiết) load `table_type`

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/index.vue:163-173`

- [ ] **Step 1: Load `table_type` từ API response**

Tìm method getDetail (line 163-173):
```javascript
async getDetail() {
    this.isLoading = true
    const { data } = await this.$store.dispatch(
        'apiGetMethod',
        `category/contract_annex_quantity/${this.$route.params.id}`,
    )

    this.formSubmit = data
    this.formSubmit.groups = data.contract.groups
    this.isLoading = false
},
```

Thêm sau `this.formSubmit.groups = data.contract.groups`:
```javascript
this.formSubmit.table_type = data.table_type || 1
```

- [ ] **Step 2: Verify**

Mở chi tiết phụ lục cũ → Kiểu A, radio disabled. Mở phụ lục mới Kiểu B → đúng cột Kiểu B.

---

### Task 8: Test end-to-end

- [ ] **Step 1: Test tạo phụ lục mới (Kiểu B mặc định)**

1. Mở trang tạo mới phụ lục thay đổi số lượng
2. Chọn hợp đồng → thấy radio "SL điều chỉnh" đang được chọn
3. Thêm hàng hóa → nhập SL điều chỉnh = 5 → Thành tiền = đơn giá × 5
4. Lưu → mở lại edit → vẫn đúng Kiểu B

- [ ] **Step 2: Test chuyển kiểu A → B trên form**

1. Tạo phụ lục mới, chuyển sang Kiểu A
2. Nhập SL sau đ/c = 80 → thấy Thành tiền trên hđ và Thành tiền sau đ/c
3. Chuyển sang Kiểu B → confirm → số lượng reset về 0
4. Nhập SL điều chỉnh = 5 → chỉ thấy Thành tiền

- [ ] **Step 3: Test in phụ lục Kiểu A và Kiểu B**

1. Tạo và duyệt 1 phụ lục Kiểu A → vào print → bảng 11 cột (STT + 10)
2. Tạo và duyệt 1 phụ lục Kiểu B → vào print → bảng 10 cột (STT + 9, không có "Thành tiền trên hđ")

- [ ] **Step 4: Test backward compatibility phụ lục cũ**

1. Mở chi tiết phụ lục cũ (tạo trước khi có feature này)
2. Phải hiển thị đúng Kiểu A
3. In phụ lục cũ → bảng đúng Kiểu A
