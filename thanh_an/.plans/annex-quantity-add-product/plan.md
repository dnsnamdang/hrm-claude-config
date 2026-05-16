# Thêm hàng hóa mới vào phụ lục thay đổi số lượng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép thêm sản phẩm mới từ danh mục hệ thống vào phụ lục thay đổi số lượng — tạo nhóm mới/chọn nhóm cũ, nhân bản, và tạo contract_products mới khi duyệt.

**Architecture:** Tái sử dụng modal `ProductModalWithDuplicate` đã có sẵn (đang bị comment). FE đánh dấu sản phẩm mới bằng `contract_product_id = null` + `product_id`. BE xử lý riêng sản phẩm mới khi store/update/approve — tạo `contract_products` mới khi duyệt.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue

**Spec:** `docs/superpowers/specs/2026-05-08-annex-quantity-add-product-design.md`

---

## File Map

| File | Hành động | Trách nhiệm |
|------|-----------|-------------|
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/components/ProductComponent.vue` | Modify | Bỏ comment nút thêm nhóm/hàng hóa, thêm nút "+" vào header nhóm, sửa `addProduct` thêm default fields |
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/add.vue` | Modify | Sửa logic submit — phân biệt sản phẩm cũ/mới |
| `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/edit.vue` | Modify | Sửa logic submit — phân biệt sản phẩm cũ/mới |
| `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php` | Modify | Sửa validation + logic store/update/approve cho sản phẩm mới |
| `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexQuantityDetailResource.php` | Modify | Xử lý sản phẩm mới khi trả detail (edit/view) |

---

### Task 1: FE — Bỏ comment nút thêm nhóm + thêm hàng hóa trong ProductComponent.vue

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/components/ProductComponent.vue:5-9`

- [x] **Step 1: Bỏ comment nút "Thêm nhóm" và nút header**

Tại dòng 5-9, thay khối comment bằng nút hoạt động:

```html
<h4 class="m-0">Danh sách hàng hóa</h4>
<div class="d-flex align-items-center">
    <base-add-button v-if="!isShow" @click="addGroupProduct" class="mr-1" title="Thêm nhóm" />
    <b-button v-b-toggle.filter-product variant="light" class="btn-icon ml-1">
        <img src="@/assets/images/file-icons/filter.svg" alt="Filter" class="icon-style" />
    </b-button>
</div>
```

- [x] **Step 2: Thêm nút "Thêm hàng hóa" vào header mỗi nhóm**

Tại dòng ~135-137 (trong template group header), sửa `<b-td>` chứa `group.group_name`:

```html
<b-td class="space-normal align-middle head-col-2a">
    <b>{{ group.group_name }}</b>
    <b-button v-if="!isShow" variant="link" size="sm" class="ml-1 p-0" @click="showPopupProduct(gIndex)">
        <i class="fas fa-plus text-primary"></i>
    </b-button>
</b-td>
```

- [x] **Step 3: Kiểm tra UI**

Mở trình duyệt → vào trang thêm phụ lục thay đổi số lượng → chọn hợp đồng.
- Xác nhận hiển thị nút "Thêm nhóm" ở trên header
- Xác nhận hiển thị nút "+" bên cạnh tên mỗi nhóm
- Click nút "+" → modal danh sách hàng hóa mở ra
- Click "Thêm nhóm" → nhóm mới được tạo với tên mặc định "Nhóm N"

---

### Task 2: FE — Sửa hàm addProduct thêm default fields cho sản phẩm mới

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/components/ProductComponent.vue:945-1047`

- [x] **Step 1: Sửa hàm addProduct — thêm fields mặc định**

Trong hàm `addProduct`, tại cả 2 nhánh (duplicate và normal), thêm các field vào object `item`:

Nhánh **duplicate** (dòng ~955), thêm vào object `item`:
```js
let item = {
    ...data,
    product_id: data.id,
    contract_product_id: null,
    contract_qty: 0,
    is_new: true,
    technical_specification: data.content_no_html,
    product_trade_name: data.trade_name,
    // ... giữ nguyên các field còn lại
}
```

Nhánh **normal** (dòng ~1000), thêm vào object `item`:
```js
let item = {
    ...data,
    product_id: data.id,
    contract_product_id: null,
    contract_qty: 0,
    is_new: true,
    technical_specification: data.content_no_html,
    product_trade_name: data.trade_name,
    // ... giữ nguyên các field còn lại
}
```

- [x] **Step 2: Kiểm tra UI**

Mở trình duyệt → trang thêm phụ lục → chọn hợp đồng → click "+" ở nhóm → chọn sản phẩm mới → thêm.
- Xác nhận sản phẩm hiển thị trong bảng
- Cột "Số lượng trên HD" hiển thị 0
- Cột "Số lượng sau đ/c" cho phép nhập
- Xác nhận nhân bản hoạt động

---

### Task 3: FE — Sửa logic submit trong add.vue

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/add.vue:62-70`

- [x] **Step 1: Sửa hàm submitForm**

Thay thế đoạn build `products` (dòng 63-70):

```js
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => item.qty > 0)
    .map((item) => {
        if (item.contract_product_id) {
            return {
                contract_product_id: item.contract_product_id,
                qty: item.qty,
                contract_qty: item.contract_qty,
            }
        } else {
            return {
                contract_product_id: null,
                product_id: item.product_id,
                qty: item.qty,
                contract_qty: 0,
                group_name: item.group_name,
                unit_id: item.unit_id,
                price: item.price || 0,
            }
        }
    })
```

- [x] **Step 2: Kiểm tra**

Tạo phụ lục mới → thêm sản phẩm cũ (điều chỉnh qty) + sản phẩm mới → bấm Lưu.
- Kiểm tra payload trong DevTools Network tab
- Sản phẩm cũ có `contract_product_id`, sản phẩm mới có `product_id` và `contract_product_id: null`

---

### Task 4: FE — Sửa logic submit trong edit.vue

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/edit.vue:92-99`

- [x] **Step 1: Sửa hàm submitForm**

Thay thế đoạn build `products` (dòng 92-99):

```js
const products = this.formSubmit.groups
    .flatMap((group) => group.products.map((item) => ({ ...item, group_name: group.group_name })))
    .filter((item) => item.qty > 0)
    .map((item) => {
        if (item.contract_product_id) {
            return {
                contract_product_id: item.contract_product_id,
                qty: item.qty,
                contract_qty: item.contract_qty,
            }
        } else {
            return {
                contract_product_id: null,
                product_id: item.product_id,
                qty: item.qty,
                contract_qty: 0,
                group_name: item.group_name,
                unit_id: item.unit_id,
                price: item.price || 0,
            }
        }
    })
```

- [x] **Step 2: Kiểm tra**

Mở phụ lục đã lưu có sản phẩm mới → sửa → bấm Lưu.
- Xác nhận sản phẩm mới vẫn hiển thị đúng sau khi load lại
- Xác nhận payload gửi đi đúng format

---

### Task 5: BE — Sửa validation và logic store()

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php:49-104`

- [x] **Step 1: Sửa validation trong store()**

Thay đổi validation rules (dòng 51-60):

```php
$request->validate([
    'contract_id' => 'required',
    'status' => 'required',
    'products'     => 'required|array|min:1',
    'products.*.contract_product_id'      => 'nullable|numeric',
    'products.*.product_id'               => 'required_without:products.*.contract_product_id|numeric',
    'products.*.qty' => 'required|numeric|min:0.01',
    'products.*.group_name'               => 'required_without:products.*.contract_product_id|string',
    'products.*.unit_id'                  => 'nullable|numeric',
    'products.*.price'                    => 'nullable|numeric',
    'print_template' => 'required',
    'print_template_type_id' => 'required',
    'print_template_id' => 'required',
]);
```

- [x] **Step 2: Sửa logic kiểm tra sản phẩm trong store()**

Sửa vòng lặp kiểm tra sản phẩm (dòng 75-87) — bỏ qua kiểm tra snapshot cho sản phẩm mới:

```php
foreach ($newItems as $contractProductId => $new) {
    // Sản phẩm mới — bỏ qua kiểm tra snapshot
    if (empty($new['contract_product_id'])) {
        continue;
    }

    $contractProduct = ContractProduct::query()->find($contractProductId);
    if (!isset($snapshotItems[$contractProductId])) {
        return $this->responseJson("Sản phẩm {$contractProduct->product_code} không tồn tại trong hợp đồng.", Response::HTTP_BAD_REQUEST);
    }

    $item = $snapshotItems[$contractProductId];
    $newQty = $new['qty'];
    if ($newQty < 0) {
        return $this->responseJson("Số lượng điều chỉnh không hợp lệ (SP {$contractProduct->product_code}).", Response::HTTP_BAD_REQUEST);
    }
}
```

Lưu ý: vì `$newItems` dùng `keyBy('contract_product_id')` mà sản phẩm mới có `contract_product_id = null`, nên cần đổi sang dùng index thường:

```php
$newItems = collect($request->products);

foreach ($newItems as $new) {
    // Sản phẩm mới — bỏ qua kiểm tra snapshot
    if (empty($new['contract_product_id'])) {
        continue;
    }

    $contractProductId = $new['contract_product_id'];
    $contractProduct = ContractProduct::query()->find($contractProductId);
    if (!isset($snapshotItems[$contractProductId])) {
        return $this->responseJson("Sản phẩm {$contractProduct->product_code} không tồn tại trong hợp đồng.", Response::HTTP_BAD_REQUEST);
    }

    $item = $snapshotItems[$contractProductId];
    $newQty = $new['qty'];
    if ($newQty < 0) {
        return $this->responseJson("Số lượng điều chỉnh không hợp lệ (SP {$contractProduct->product_code}).", Response::HTTP_BAD_REQUEST);
    }
}
```

- [x] **Step 3: Kiểm tra**

Dùng Postman hoặc FE gửi request tạo phụ lục với sản phẩm mới → xác nhận lưu thành công, `annex.data` chứa đúng dữ liệu.

---

### Task 6: BE — Sửa validation và logic update()

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php:106-158`

- [x] **Step 1: Sửa validation trong update()**

Thay đổi validation rules (dòng 108-116) — giống store():

```php
$request->validate([
    'status' => 'required',
    'products'     => 'required|array|min:1',
    'products.*.contract_product_id'      => 'nullable|numeric',
    'products.*.product_id'               => 'required_without:products.*.contract_product_id|numeric',
    'products.*.qty' => 'required|numeric|min:0.01',
    'products.*.group_name'               => 'required_without:products.*.contract_product_id|string',
    'products.*.unit_id'                  => 'nullable|numeric',
    'products.*.price'                    => 'nullable|numeric',
    'print_template' => 'required',
    'print_template_type_id' => 'required',
    'print_template_id' => 'required',
]);
```

- [x] **Step 2: Sửa logic kiểm tra sản phẩm trong update()**

Sửa vòng lặp kiểm tra (dòng 128-141) — giống store():

```php
$newItems = collect($request->products);

foreach ($newItems as $new) {
    if (empty($new['contract_product_id'])) {
        continue;
    }

    $contractProductId = $new['contract_product_id'];
    $contractProduct = ContractProduct::query()->find($contractProductId);
    if (!isset($snapshotItems[$contractProductId])) {
        return $this->responseJson("Sản phẩm {$contractProduct->product_code} không tồn tại trong hợp đồng.", Response::HTTP_BAD_REQUEST);
    }

    $item = $snapshotItems[$contractProductId];
    $newQty = $new['qty'];
    if ($newQty < 0) {
        return $this->responseJson("Số lượng thay đổi không hợp lệ (SP {$contractProduct->product_code}).", Response::HTTP_BAD_REQUEST);
    }
}
```

- [x] **Step 3: Kiểm tra**

Sửa phụ lục có sản phẩm mới → lưu → xác nhận cập nhật thành công.

---

### Task 7: BE — Sửa logic approve() để xử lý sản phẩm mới

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexQuantityController.php:161-243`

Đây là task quan trọng nhất. Hàm `approve()` cần xử lý 2 loại sản phẩm.

- [x] **Step 1: Sửa toàn bộ hàm approve()**

Thay thế logic trong `DB::transaction` (dòng 164-237):

```php
public function approve(Request $request, ContractAnnex $annex)
{
    try {
        DB::transaction(function () use ($request, $annex) {
            $oldVersion = $annex->version;
            $newVersion = $oldVersion + 1;

            $snapshot = ContractVersion::getSnapshot($annex->contract_id, $oldVersion);
            $snapshotItems = collect();
            foreach ($snapshot['groups'] as $group) {
                foreach ($group['products'] as $item) {
                    $snapshotItems->put($item['id'], $item);
                }
            }

            $annexData = collect($annex->data);

            // --- Xử lý sản phẩm CŨ (có contract_product_id) ---
            $oldProducts = $annexData->filter(fn($item) => !empty($item['contract_product_id']));
            foreach ($oldProducts as $new) {
                $contractProductId = $new['contract_product_id'];
                $contractProduct = ContractProduct::query()->find($contractProductId);
                if (!isset($snapshotItems[$contractProductId])) {
                    return $this->responseJson("Sản phẩm {$contractProduct->product_code} không tồn tại trong hợp đồng.", Response::HTTP_BAD_REQUEST);
                }

                $item = $snapshotItems[$contractProductId];
                $oldQty = $item['qty'];
                $newQty = $new['qty'];
                if ($newQty < 0) {
                    return $this->responseJson("Số lượng thay đổi không hợp lệ (SP {$contractProduct->product_code}).", Response::HTTP_BAD_REQUEST);
                }

                // Update snapshot
                $item['qty'] = $newQty;
                $snapshotItems->put($contractProductId, $item);

                // Ghi change
                ContractChange::create([
                    'contract_id' => $annex->contract_id,
                    'annex_id' => $annex->id,
                    'version'     => $newVersion,
                    'entity_type' => 'contractProduct',
                    'entity_key'  => (string)$contractProductId,
                    'field_name'  => 'qty',
                    'old_value'   => $oldQty,
                    'new_value'   => $newQty,
                ]);
            }

            // --- Xử lý sản phẩm MỚI (có product_id, không có contract_product_id) ---
            $newProducts = $annexData->filter(fn($item) => empty($item['contract_product_id']));
            foreach ($newProducts as $new) {
                $product = \Modules\Category\Entities\Product::find($new['product_id']);
                if (!$product) {
                    return $this->responseJson("Sản phẩm không tồn tại trong danh mục.", Response::HTTP_BAD_REQUEST);
                }

                $groupName = $new['group_name'] ?? 'Nhóm mới';

                // Tìm hoặc tạo ContractGroup
                $contractGroup = \Modules\Category\Entities\Contract\ContractGroup::firstOrCreate(
                    ['contract_id' => $annex->contract_id, 'group_name' => $groupName],
                );

                // Tạo ContractProduct mới
                $contractProduct = ContractProduct::create([
                    'contract_id'      => $annex->contract_id,
                    'contract_group_id' => $contractGroup->id,
                    'product_id'       => $product->id,
                    'product_name'     => $product->name,
                    'product_code'     => $product->product_code,
                    'internal_code'    => $product->internal_code,
                    'qty'              => $new['qty'],
                    'contract_qty'     => $new['qty'],
                    'price'            => $new['price'] ?? 0,
                    'amount'           => ($new['price'] ?? 0) * $new['qty'],
                    'unit_id'          => $new['unit_id'] ?? null,
                    'exported_qty'     => 0,
                    'specification'    => $product->specification ?? '',
                    'product_trade_name' => $product->trade_name ?? '',
                    'owner_country'    => $product->owner_country ?? '',
                    'producer_country' => $product->producer_country ?? '',
                    'vat_percent'      => $product->tax ?? 0,
                ]);

                // Thêm vào snapshot — tìm group theo group_name
                $groupFound = false;
                foreach ($snapshot['groups'] as &$snGroup) {
                    if ($snGroup['group_name'] === $groupName) {
                        $snGroup['products'][] = [
                            'id' => $contractProduct->id,
                            'product_id' => $product->id,
                            'product_name' => $product->name,
                            'product_code' => $product->product_code,
                            'internal_code' => $product->internal_code,
                            'product_trade_name' => $product->trade_name ?? '',
                            'specification' => $product->specification ?? '',
                            'owner_country' => $product->owner_country ?? '',
                            'producer_country' => $product->producer_country ?? '',
                            'unit_id' => $new['unit_id'] ?? null,
                            'qty' => $new['qty'],
                            'price' => $new['price'] ?? 0,
                            'amount' => ($new['price'] ?? 0) * $new['qty'],
                            'exported_qty' => 0,
                            'vat_percent' => $product->tax ?? 0,
                        ];
                        $groupFound = true;
                        break;
                    }
                }
                unset($snGroup);

                // Nếu group chưa có trong snapshot → tạo mới
                if (!$groupFound) {
                    $snapshot['groups'][] = [
                        'group_name' => $groupName,
                        'group_id' => $contractGroup->id,
                        'products' => [
                            [
                                'id' => $contractProduct->id,
                                'product_id' => $product->id,
                                'product_name' => $product->name,
                                'product_code' => $product->product_code,
                                'internal_code' => $product->internal_code,
                                'product_trade_name' => $product->trade_name ?? '',
                                'specification' => $product->specification ?? '',
                                'owner_country' => $product->owner_country ?? '',
                                'producer_country' => $product->producer_country ?? '',
                                'unit_id' => $new['unit_id'] ?? null,
                                'qty' => $new['qty'],
                                'price' => $new['price'] ?? 0,
                                'amount' => ($new['price'] ?? 0) * $new['qty'],
                                'exported_qty' => 0,
                                'vat_percent' => $product->tax ?? 0,
                            ],
                        ],
                    ];
                }

                // Ghi change
                ContractChange::create([
                    'contract_id' => $annex->contract_id,
                    'annex_id' => $annex->id,
                    'version'     => $newVersion,
                    'entity_type' => 'contractProduct',
                    'entity_key'  => (string)$contractProduct->id,
                    'field_name'  => 'qty',
                    'old_value'   => 0,
                    'new_value'   => $new['qty'],
                ]);
            }

            // --- Cập nhật trạng thái phụ lục ---
            $annex->approver_id = auth()->user()->id;
            $annex->approved_time = Carbon::now();
            $annex->status = ContractAnnex::DA_DUYET;
            $annex->save();

            // --- Cập nhật snapshot cho sản phẩm cũ ---
            foreach ($snapshot['groups'] as &$group) {
                foreach ($group['products'] as &$item) {
                    $cpid = $item['id'];
                    if ($snapshotItems->has($cpid)) {
                        $item['qty'] = $snapshotItems[$cpid]['qty'];
                    }
                }
            }
            unset($group, $item);

            // --- Lưu phiên bản mới ---
            ContractVersion::create([
                'contract_id' => $annex->contract_id,
                'version'     => $newVersion,
                'data'        => $snapshot,
            ]);

            // --- Cập nhật contract_products cho sản phẩm cũ ---
            foreach ($oldProducts as $new) {
                $contract_product = ContractProduct::where('id', $new['contract_product_id'])->first();
                $contract_product->qty -= $new['qty'] ?? 0;
                $contract_product->save();
            }

            // --- Cập nhật current_version ---
            $contract = $annex->contract;
            $contract->update([
                'current_version' => $newVersion,
            ]);

            return $this->responseJson('success', Response::HTTP_OK);
        });
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

- [x] **Step 2: Kiểm tra**

Tạo phụ lục có cả sản phẩm cũ và mới → gửi duyệt → duyệt.
- Kiểm tra `contract_products` có bản ghi mới
- Kiểm tra `contract_versions` có snapshot mới chứa sản phẩm mới
- Kiểm tra `contract_changes` ghi nhận thay đổi cho cả 2 loại sản phẩm
- Kiểm tra `contract.current_version` đã tăng

---

### Task 8: BE — Sửa ContractAnnexQuantityDetailResource xử lý sản phẩm mới

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexQuantityDetailResource.php:26-73`

- [x] **Step 1: Sửa hàm toArray()**

Sản phẩm mới lưu trong `annex.data` có `product_id` thay vì `contract_product_id`. Khi load detail (edit/view), cần lấy thông tin từ master `products` table.

Thay thế nội dung hàm `toArray()`:

```php
public function toArray($request): array
{
    $annexData = collect($this->data);
    $reduceItems  = $annexData->filter(fn($item) => !empty($item['contract_product_id']))
                              ->keyBy('contract_product_id');

    $data = ContractVersion::getSnapshot($this->contract_id, $this->version);

    foreach ($data['groups'] as $gKey => $group) {
        $filteredProducts = [];
        foreach ($group['products'] as $pKey => $product) {
            $item = $reduceItems[$product['id']] ?? null;
            if ($item) {
                $product['contract_qty'] = $item['contract_qty'] ?? 0;
                $product['qty'] = $item['qty'] ?? 0;
                $product['adjusted_qty'] = ($product['contract_qty'] ?? 0) - ($item['qty'] ?? 0);
                $product['amount'] = ($item['qty'] ?? 0) * ($product['price'] ?? 0);
                $filteredProducts[] = $product;
            }
        }
        $data['groups'][$gKey]['products'] = $filteredProducts;
    }

    // Loại bỏ các groups không còn products nào
    $data['groups'] = array_values(array_filter($data['groups'], function ($group) {
        return !empty($group['products']);
    }));

    // --- Xử lý sản phẩm MỚI (có product_id, không có contract_product_id) ---
    $newProducts = $annexData->filter(fn($item) => empty($item['contract_product_id']));
    foreach ($newProducts as $newItem) {
        $product = \Modules\Category\Entities\Product::find($newItem['product_id']);
        if (!$product) continue;

        $groupName = $newItem['group_name'] ?? 'Nhóm mới';
        $packageInfos = $product->packageInformations ?? collect();
        $usuallyUnit = $packageInfos->first(fn($p) => $p->is_usually);

        $productData = [
            'id' => null,
            'contract_product_id' => null,
            'product_id' => $product->id,
            'product_name' => $product->name,
            'product_code' => $product->product_code,
            'internal_code' => $product->internal_code,
            'product_trade_name' => $product->trade_name ?? '',
            'specification' => $product->specification ?? '',
            'owner_country' => $product->owner_country ?? '',
            'producer_country' => $product->producer_country ?? '',
            'unit_id' => $usuallyUnit ? $usuallyUnit->unit_id : ($newItem['unit_id'] ?? null),
            'unit_name' => $usuallyUnit ? $usuallyUnit->unit_name : '',
            'units' => $packageInfos->map(fn($p) => [
                'id' => $p->unit_id,
                'text' => $p->unit_name,
            ])->values()->toArray(),
            'contract_qty' => 0,
            'qty' => $newItem['qty'] ?? 0,
            'price' => $newItem['price'] ?? 0,
            'amount' => ($newItem['qty'] ?? 0) * ($newItem['price'] ?? 0),
            'is_new' => true,
            'vat_percent' => $product->tax ?? 0,
            'prices' => [],
        ];

        // Tìm group theo group_name hoặc tạo mới
        $groupFound = false;
        foreach ($data['groups'] as &$group) {
            if ($group['group_name'] === $groupName) {
                $group['products'][] = $productData;
                $groupFound = true;
                break;
            }
        }
        unset($group);

        if (!$groupFound) {
            $data['groups'][] = [
                'group_name' => $groupName,
                'products' => [$productData],
            ];
        }
    }

    return [
        'id' => $this->id,
        'code' => $this->code,
        'annex_no' => $this->annex_no,
        'contract_id' => $this->contract_id,
        'contract' => $data,
        'created_by' => $this->created_by,
        'updated_by' => $this->updated_by,
        'approver_id' => $this->approver_id,
        'approved_time' => $this->approved_time,
        'status' => $this->status,
        'version' => $this->version,
        'reason_deny' => $this->reason_deny,
        'canEdit' => $this->canEdit(),
        'canDelete' => $this->canDelete(),
        'canApprove' => $this->canApprove(),
        'print_template' => $this->print_template,
        'print_template_type_id' => $this->print_template_type_id,
        'print_template_id' => $this->print_template_id,
    ];
}
```

- [x] **Step 2: Kiểm tra**

Lưu phụ lục có sản phẩm mới → mở lại trang edit → xác nhận:
- Sản phẩm mới hiển thị đúng tên, mã, đơn vị
- `contract_qty = 0`
- `qty` hiển thị đúng giá trị đã lưu
- Sản phẩm nằm đúng nhóm

---

### Task 9: FE — Sửa edit.vue xử lý sản phẩm mới khi load detail

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract_annex_quantity/_id/edit.vue:146-159`

- [x] **Step 1: Sửa hàm getDetail()**

Khi load detail, sản phẩm mới từ BE trả về có `contract_product_id = null` và `is_new = true`. Cần đảm bảo FE map đúng field `contract_product_id` (hiện tại map `item.id` cho `contract_product_id` khi submit — sản phẩm mới có `id = null`).

Hàm `getDetail` hiện tại gán `this.formSubmit.groups = data.contract.groups` — điều này đã đúng vì BE trả sản phẩm mới kèm `contract_product_id: null` và `product_id`.

Không cần sửa `getDetail`. Nhưng cần kiểm tra trong `submitForm` (đã sửa ở Task 4): khi sản phẩm cũ từ snapshot có field `id` (là `contract_product_id`), cần map đúng:

```js
if (item.contract_product_id) {
    return {
        contract_product_id: item.contract_product_id,
        qty: item.qty,
        contract_qty: item.contract_qty,
    }
} else if (item.id && !item.is_new) {
    // Sản phẩm cũ từ snapshot — id chính là contract_product_id
    return {
        contract_product_id: item.id,
        qty: item.qty,
        contract_qty: item.contract_qty,
    }
} else {
    // Sản phẩm mới
    return {
        contract_product_id: null,
        product_id: item.product_id,
        qty: item.qty,
        contract_qty: 0,
        group_name: item.group_name,
        unit_id: item.unit_id,
        price: item.price || 0,
    }
}
```

Cập nhật tương tự trong `add.vue` (Task 3).

- [x] **Step 2: Kiểm tra end-to-end**

1. Tạo phụ lục mới → thêm sản phẩm cũ + mới → Lưu
2. Mở lại edit → xác nhận hiển thị đúng → sửa qty → Lưu lại
3. Gửi duyệt → Duyệt
4. Kiểm tra DB: `contract_products`, `contract_versions`, `contract_changes`
5. Mở trang view phụ lục → xác nhận hiển thị đúng

---

### Task 10: Kiểm tra tổng thể

- [x] **Step 1: Test tạo phụ lục chỉ có sản phẩm mới**

Tạo phụ lục → chỉ thêm sản phẩm mới (không điều chỉnh sản phẩm cũ) → Lưu → Gửi duyệt → Duyệt → Xác nhận OK.

- [x] **Step 2: Test tạo phụ lục hỗn hợp (cũ + mới)**

Tạo phụ lục → điều chỉnh qty sản phẩm cũ + thêm sản phẩm mới → Lưu → Gửi duyệt → Duyệt → Xác nhận cả 2 loại đều xử lý đúng.

- [x] **Step 3: Test nhân bản sản phẩm**

Thêm sản phẩm mới → nhân bản sản phẩm đó → xác nhận có 2 dòng trong bảng → Lưu → kiểm tra data đúng.

- [x] **Step 4: Test thêm nhóm mới**

Click "Thêm nhóm" → nhập tên nhóm → thêm sản phẩm vào nhóm mới → Lưu → Load lại edit → xác nhận nhóm mới hiển thị đúng.

- [x] **Step 5: Test phụ lục bị từ chối → edit lại**

Tạo phụ lục có sản phẩm mới → gửi duyệt → từ chối → mở edit → xác nhận sản phẩm mới vẫn hiển thị → sửa lại → gửi duyệt lại.

---

### Checkpoint — 2026-05-08

**Tất cả 10 task đã hoàn thành.**

Bugs đã fix sau implementation:
1. **UI không giống HĐ gốc** — Sửa lại nút thêm nhóm (bỏ title), group name editable, thêm link "Thêm hàng hóa" cuối mỗi nhóm
2. **Vue 2 reactivity** — Thêm `qty: 0`, `amount: 0` vào addProduct để Vue 2 track được
3. **Tên hàng hóa không hiện sau lưu** — Sửa `$product->name` → `$product->product_name`, relationship `packageInformations` → `ProductPackageInformation::where(...)`, owner/producer country lookup từ ID
4. **Đơn vị tính không hiện** — FE dùng `item.units` (mảng select2 options) nhưng snapshot thiếu field `units`. Sửa `getDataForAnnex` luôn load `units` từ `product_package_informations`, sửa approve snapshot thêm `units`

**Files đã thay đổi:**
- FE: `ProductComponent.vue`, `add.vue`, `edit.vue`
- BE: `ContractAnnexQuantityController.php`, `ContractAnnexQuantityDetailResource.php`, `ContractController.php` (getDataForAnnex)
