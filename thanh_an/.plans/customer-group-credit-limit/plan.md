# Hạn mức công nợ theo từng KH — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển hạn mức công nợ từ `customer_groups` xuống `category_customers`, dọn dẹp code nhóm KH, thêm UI hạn mức vào form + list khách hàng.

**Architecture:** 2 migration tách riêng (thêm trước, xóa sau). BE thêm validation/filter/resource cho customer, xóa tương ứng ở customer group. FE thêm toggle+input vào GeneralComponent, thêm 2 cột+filter vào list KH, dọn modal+list nhóm KH.

**Tech Stack:** PHP 7.4, Laravel 8, MySQL, Nuxt 2 (Vue 2), Bootstrap-Vue

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`

---

## File Structure

| Action | File |
|--------|------|
| Create | `hrm-thanhan-api/database/migrations/2026_05_19_100000_add_debt_limit_to_category_customers_table.php` |
| Create | `hrm-thanhan-api/database/migrations/2026_05_19_100001_remove_debt_limit_from_customer_groups_table.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Http/Requests/StoreCategoryCustomerRequest.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Services/CustomerService.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/CategoryCustomerResource.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/DetailCategoryCustomerResource.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Http/Requests/CustomerGroup/CustomerGroupRequest.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Services/CustomerGroupService.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/CustomerGroupResource.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/DetailCustomerGroupResource.php` |
| Modify | `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/CustomerGroupController.php` |
| Modify | `hrm-thanhan-client/pages/category/customer/components/GeneralComponent.vue` |
| Modify | `hrm-thanhan-client/pages/category/customer/index.vue` |
| Modify | `hrm-thanhan-client/components/modal/CustomerGroupModal.vue` |
| Modify | `hrm-thanhan-client/pages/category/customer_groups/index.vue` |

---

## Phase 1 — BE: Migration + Validation (Task 1-3)

### Task 1: Migration thêm 2 cột vào `category_customers`

**Files:**
- Create: `hrm-thanhan-api/database/migrations/2026_05_19_100000_add_debt_limit_to_category_customers_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddDebtLimitToCategoryCustomersTable extends Migration
{
    public function up()
    {
        Schema::table('category_customers', function (Blueprint $table) {
            $table->decimal('max_debt_limit', 18, 2)->nullable()->after('additional_info')
                ->comment('Hạn mức công nợ tối đa (VNĐ)');
            $table->tinyInteger('is_debt_limit_active')->default(0)->after('max_debt_limit')
                ->comment('1 = đang áp dụng hạn mức, 0 = không áp dụng');
        });
    }

    public function down()
    {
        Schema::table('category_customers', function (Blueprint $table) {
            $table->dropColumn(['max_debt_limit', 'is_debt_limit_active']);
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-thanhan-api && php artisan migrate
```

Expected: `Migrating: 2026_05_19_100000_add_debt_limit_to_category_customers_table` → `Migrated`

---

### Task 2: Migration xóa 2 cột khỏi `customer_groups`

**Files:**
- Create: `hrm-thanhan-api/database/migrations/2026_05_19_100001_remove_debt_limit_from_customer_groups_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class RemoveDebtLimitFromCustomerGroupsTable extends Migration
{
    public function up()
    {
        Schema::table('customer_groups', function (Blueprint $table) {
            $table->dropColumn(['max_debt_limit', 'is_debt_limit_active']);
        });
    }

    public function down()
    {
        Schema::table('customer_groups', function (Blueprint $table) {
            $table->decimal('max_debt_limit', 18, 2)->nullable()->after('status')
                ->comment('Hạn mức công nợ tối đa (VNĐ)');
            $table->tinyInteger('is_debt_limit_active')->default(0)->after('max_debt_limit')
                ->comment('1 = đang áp dụng hạn mức, 0 = không áp dụng');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-thanhan-api && php artisan migrate
```

Expected: `Migrating: 2026_05_19_100001_remove_debt_limit_from_customer_groups_table` → `Migrated`

---

### Task 3: Validation — thêm rules cho customer, xóa rules cho customer group

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Requests/StoreCategoryCustomerRequest.php:79` (trước `];` cuối rules)
- Modify: `hrm-thanhan-api/Modules/Category/Http/Requests/StoreCategoryCustomerRequest.php:100` (trước `];` cuối messages)
- Modify: `hrm-thanhan-api/Modules/Category/Http/Requests/CustomerGroup/CustomerGroupRequest.php`

- [ ] **Step 1: Thêm validation rules vào `StoreCategoryCustomerRequest`**

Trong method `rules()`, thêm SAU dòng `'person_charge_business.*.group_permission_id' => 'required',` (line 77):

```php
            'is_debt_limit_active' => 'nullable|in:0,1',
            'max_debt_limit' => [
                'nullable',
                'numeric',
                'min:1',
                function ($attribute, $value, $fail) {
                    if ((int) $this->is_debt_limit_active === 1 && ($value === null || $value === '')) {
                        $fail('Vui lòng nhập hạn mức công nợ tối đa khi đang áp dụng hạn mức');
                    }
                },
            ],
```

- [ ] **Step 2: Thêm messages tiếng Việt**

Trong method `messages()`, thêm SAU dòng cuối cùng hiện có (line 97, trước `];`):

```php
            'max_debt_limit.numeric' => 'Hạn mức công nợ phải là số',
            'max_debt_limit.min' => 'Hạn mức công nợ phải lớn hơn 0',
```

- [ ] **Step 3: Xóa validation rules khỏi `CustomerGroupRequest`**

Sửa `CustomerGroupRequest.php` — xóa rules `is_debt_limit_active` + `max_debt_limit`, chỉ giữ lại `name`, `code`, `status`:

```php
    public function rules()
    {
        return [
            'name' => 'required|unique:customer_groups,name,' . $this->id,
            'code' => 'required|unique:customer_groups,code,' . $this->id,
            'status' => 'required',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => 'Bắt buộc phải nhập',
            'name.unique' => 'Tên này đã tồn tại',
            'code.required' => 'Bắt buộc phải nhập',
            'code.unique' => 'Mã này đã tồn tại',
            'status.required' => 'Bắt buộc phải nhập',
        ];
    }
```

---

## Phase 2 — BE: Service + Resource + Controller (Task 4-6)

### Task 4: CustomerService — thêm filter + 2 field vào store/update

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerService.php:84` (sau filter keyword, trước permission check)
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerService.php:199-229` (store — thêm 2 field vào create array)
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerService.php:254-282` (update — thêm 2 field vào update array)

- [ ] **Step 1: Thêm filter `is_debt_limit_active` vào `index()`**

Sau block filter `keyword` (line 84, trước `if (isCurrentEmployeeHasPermission...)`), thêm:

```php
            ->when(isset($request->is_debt_limit_active) && in_array((int) $request->is_debt_limit_active, [0, 1]), function ($query) use ($request) {
                return $query->where('is_debt_limit_active', (int) $request->is_debt_limit_active);
            });
```

Lưu ý: filter này dùng `when(condition, callback)` nên nối tiếp vào chain hiện có. Kết thúc bằng `;` thay vì `;` ở line 84 cũ.

- [ ] **Step 2: Thêm 2 field vào `store()` — block `CategoryCustomer::create()`**

Trong method `store()`, thêm 2 field vào cuối array `create()` (sau `'customer_province_name'`, line 228):

```php
                'is_debt_limit_active' => (int) ($request->is_debt_limit_active ?? 0),
                'max_debt_limit' => $request->max_debt_limit !== null && $request->max_debt_limit !== ''
                    ? $request->max_debt_limit
                    : null,
```

- [ ] **Step 3: Thêm 2 field vào `update()` — block `$customer->update()`**

Trong method `update()`, thêm 2 field vào cuối array `update()` (sau `'customer_province_name'`, line 281):

```php
                'is_debt_limit_active' => (int) ($request->is_debt_limit_active ?? 0),
                'max_debt_limit' => $request->max_debt_limit !== null && $request->max_debt_limit !== ''
                    ? $request->max_debt_limit
                    : null,
```

---

### Task 5: Resource — thêm 2 field cho customer, xóa 2 field cho customer group

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/CategoryCustomerResource.php:47`
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/DetailCategoryCustomerResource.php:56`
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/CustomerGroupResource.php:25-26`
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/DetailCustomerGroupResource.php:25-26`

- [ ] **Step 1: Thêm 2 field vào `CategoryCustomerResource`**

Sau `'created_by_name'` (line 47), thêm:

```php
            'max_debt_limit' => $this->max_debt_limit !== null ? (float) $this->max_debt_limit : null,
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
```

- [ ] **Step 2: Thêm 2 field vào `DetailCategoryCustomerResource`**

Sau `'full_address'` (line 56), thêm:

```php
            'max_debt_limit' => $this->max_debt_limit !== null ? (float) $this->max_debt_limit : null,
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
```

- [ ] **Step 3: Xóa 2 field khỏi `CustomerGroupResource`**

Xóa 2 dòng (line 25-26):
```php
            'max_debt_limit' => $this->max_debt_limit !== null ? (float) $this->max_debt_limit : null,
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
```

- [ ] **Step 4: Xóa 2 field khỏi `DetailCustomerGroupResource`**

Xóa 2 dòng (line 25-26):
```php
            'max_debt_limit' => $this->max_debt_limit !== null ? (float) $this->max_debt_limit : null,
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
```

---

### Task 6: CustomerGroupService + CustomerGroupController — dọn dẹp

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerGroupService.php:29-31` (xóa filter)
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerGroupService.php:48-56,62-70` (xóa 2 field trong update + create)
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/CustomerGroupController.php:66-77` (xóa log mapping)

- [ ] **Step 1: Xóa filter `is_debt_limit_active` khỏi `CustomerGroupService::index()`**

Xóa block (line 29-31):
```php
        if (isset($request->is_debt_limit_active) && in_array((int) $request->is_debt_limit_active, [0, 1])) {
            $query->where('is_debt_limit_active', (int) $request->is_debt_limit_active);
        }
```

- [ ] **Step 2: Xóa 2 field khỏi update trong `updateOrCreate()`**

Trong block `$customerGroup->update([...])` (line 48-56), xóa:
```php
                    'is_debt_limit_active' => (int) $request->is_debt_limit_active,
                    'max_debt_limit' => $request->max_debt_limit !== null && $request->max_debt_limit !== ''
                        ? $request->max_debt_limit
                        : null,
```

Chỉ giữ lại `name`, `code`, `status`.

- [ ] **Step 3: Xóa 2 field khỏi create trong `updateOrCreate()`**

Trong block `CustomerGroup::create([...])` (line 62-70), xóa:
```php
                'is_debt_limit_active' => (int) $request->is_debt_limit_active,
                'max_debt_limit' => $request->max_debt_limit !== null && $request->max_debt_limit !== ''
                    ? $request->max_debt_limit
                    : null,
```

Chỉ giữ lại `name`, `code`, `status`.

- [ ] **Step 4: Xóa log mapping khỏi `CustomerGroupController::getLogs()`**

Xóa 2 block if (line 66-77):
```php
                if ($key === 'is_debt_limit_active') {
                    $item['value_before'] = $item['value_before'] == 1 ? 'Đang áp dụng' : 'Không áp dụng';
                    $item['value_after'] = $item['value_after'] == 1 ? 'Đang áp dụng' : 'Không áp dụng';
                }
                if ($key === 'max_debt_limit') {
                    $item['value_before'] = $item['value_before'] !== null && $item['value_before'] !== ''
                        ? number_format((float) $item['value_before'], 0, ',', '.') . ' VNĐ'
                        : '(trống)';
                    $item['value_after'] = $item['value_after'] !== null && $item['value_after'] !== ''
                        ? number_format((float) $item['value_after'], 0, ',', '.') . ' VNĐ'
                        : '(trống)';
                }
```

---

## Phase 3 — FE: Form KH (Task 7)

### Task 7: GeneralComponent.vue — thêm toggle + input hạn mức

**Files:**
- Modify: `hrm-thanhan-client/pages/category/customer/components/GeneralComponent.vue`

- [ ] **Step 1: Thêm template HTML — toggle + input hạn mức**

Sau block "Địa chỉ" (line 188-189, trước `</div>` đóng của `col-xl-12 row mt-2` ở line 190), thêm:

```html
            <div class="col-md-6 row mt-3">
                <div class="col-md-3">
                    <label>Áp dụng hạn mức</label>
                </div>
                <div class="col-md-9">
                    <div class="toggle-row">
                        <label class="toggle">
                            <input type="checkbox" v-model="isDebtLimitActiveBool" :disabled="isShow" />
                            <div class="toggle-track"><div class="toggle-thumb"></div></div>
                        </label>
                        <span class="toggle-label">
                            {{ isDebtLimitActiveBool ? 'Đang áp dụng' : 'Không áp dụng' }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-md-6 row mt-3">
                <div class="col-md-3">
                    <label>
                        Hạn mức công nợ tối đa (VNĐ)
                        <Required v-if="isDebtLimitActiveBool" />
                    </label>
                </div>
                <div class="col-md-9">
                    <input
                        v-model="maxDebtLimitFormatted"
                        class="form-control"
                        placeholder="0"
                        type="text"
                        inputmode="numeric"
                        :disabled="isShow || !isDebtLimitActiveBool"
                    />
                    <span v-if="formError['max_debt_limit']" class="text-muted">
                        {{ formError['max_debt_limit'][0] || formError['max_debt_limit'] }}
                    </span>
                </div>
            </div>
```

- [ ] **Step 2: Thêm computed properties**

Trong block `computed` của component (tìm section `computed:`), thêm:

```javascript
        isDebtLimitActiveBool: {
            get() {
                return Number(this.formSubmit.is_debt_limit_active) === 1
            },
            set(val) {
                this.$set(this.formSubmit, 'is_debt_limit_active', val ? 1 : 0)
            },
        },
        maxDebtLimitFormatted: {
            get() {
                const v = this.formSubmit.max_debt_limit
                if (v === null || v === undefined || v === '') return ''
                return Number(v).toLocaleString('vi-VN')
            },
            set(val) {
                const digits = String(val).replace(/[^\d]/g, '')
                this.$set(this.formSubmit, 'max_debt_limit', digits === '' ? null : Number(digits))
            },
        },
```

- [ ] **Step 3: Thêm CSS scoped**

Trong block `<style lang="scss" scoped>` (hoặc tạo mới nếu chưa có), thêm:

```scss
.toggle-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-top: 4px;
}
.toggle {
    display: inline-block;
    cursor: pointer;
    user-select: none;
    margin: 0;
}
.toggle input {
    display: none;
}
.toggle-track {
    width: 34px;
    height: 20px;
    background: #e5e5ea;
    border-radius: 999px;
    position: relative;
    transition: background 0.25s ease;
}
.toggle-thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 16px;
    height: 16px;
    background: #fff;
    border-radius: 50%;
    transition: transform 0.25s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}
.toggle input:checked + .toggle-track {
    background: #34c759;
}
.toggle input:checked + .toggle-track .toggle-thumb {
    transform: translateX(14px);
}
.toggle input:disabled + .toggle-track {
    opacity: 0.5;
    cursor: not-allowed;
}
.toggle-label {
    font-size: 13px;
    color: #495057;
}
```

- [ ] **Step 4: Đảm bảo default data khi tạo mới**

Kiểm tra parent component (trang add KH) — khi tạo mới, `formSubmit` phải chứa:
```javascript
is_debt_limit_active: 0,
max_debt_limit: null,
```

Tìm file parent (`pages/category/customer/add.vue` hoặc tương đương) và thêm 2 field này vào `formSubmit` default nếu chưa có.

---

## Phase 4 — FE: List KH (Task 8)

### Task 8: customer/index.vue — thêm 2 cột, filter, template cell

**Files:**
- Modify: `hrm-thanhan-client/pages/category/customer/index.vue`

- [ ] **Step 1: Thêm `is_debt_limit_active` vào `initialStateForm`**

Tại `initialStateForm` (line 269-282), thêm SAU `customer_area_id: undefined,`:

```javascript
    is_debt_limit_active: undefined,
```

- [ ] **Step 2: Thêm 2 field vào array `fields`**

Trong array `fields` (line 318-424), thêm SAU block `status` (line 414-418) và TRƯỚC block `actions` (line 419-423):

```javascript
                {
                    key: 'max_debt_limit',
                    label: 'Hạn mức công nợ (VNĐ)',
                    sortable: true,
                    tdClass: 'text-right',
                    isVisible: true,
                },
                {
                    key: 'is_debt_limit_active',
                    label: 'Áp dụng hạn mức',
                    sortable: true,
                    tdClass: 'text-center',
                    isVisible: true,
                },
```

- [ ] **Step 3: Thêm `listDebtLimitStatus` vào `data()`**

Trong `data()` return, thêm (ví dụ sau `customerAreas: []` ở line 466):

```javascript
            listDebtLimitStatus: [
                { id: 1, text: 'Đang áp dụng' },
                { id: 0, text: 'Không áp dụng' },
            ],
```

- [ ] **Step 4: Thêm filter Select2 vào template**

Trong template, tìm block filter collapse (line 34-137). Thêm SAU filter "Người tạo" (line 119-120) và TRƯỚC div chứa nút Đặt lại/Áp dụng (line 121):

```html
                                                <div class="col-md-3">
                                                    <base-select2
                                                        v-model="formFilter.is_debt_limit_active"
                                                        :options="listDebtLimitStatus"
                                                        placeholder="Áp dụng hạn mức"
                                                        :settings="{ allowClear: true }"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
```

- [ ] **Step 5: Thêm template cell cho 2 cột mới**

Trong `<b-table>`, sau template `cell(status)` (line 158-160) và trước template `cell(actions)` (line 161), thêm:

```html
                                <template v-slot:cell(max_debt_limit)="{ item }">
                                    <span v-if="item.is_debt_limit_active == 1 && item.max_debt_limit !== null">
                                        {{ formatMoney(item.max_debt_limit) }}
                                    </span>
                                    <span v-else class="text-muted">—</span>
                                </template>
                                <template v-slot:cell(is_debt_limit_active)="{ item }">
                                    <span :style="getDebtLimitBadge(item.is_debt_limit_active)" class="badge">
                                        {{ item.is_debt_limit_active == 1 ? 'Đang áp dụng' : 'Không áp dụng' }}
                                    </span>
                                </template>
```

- [ ] **Step 6: Thêm methods `formatMoney` + `getDebtLimitBadge`**

Trong `methods`, thêm (ví dụ sau `getNumericalOrder` ở line 551):

```javascript
        formatMoney(v) {
            if (v === null || v === undefined || v === '') return ''
            return Number(v).toLocaleString('vi-VN')
        },
        getDebtLimitBadge(active) {
            if (Number(active) === 1) {
                return 'background-color: #E5F8EC; color: #00B63E;'
            }
            return 'background-color: #F2F2F5; color: #6E6E73;'
        },
```

---

## Phase 5 — FE: Dọn dẹp nhóm KH (Task 9-10)

### Task 9: CustomerGroupModal.vue — xóa toggle + input hạn mức

**Files:**
- Modify: `hrm-thanhan-client/components/modal/CustomerGroupModal.vue`

- [ ] **Step 1: Xóa 2 form-group trong template**

Xóa line 40-68 (từ `<div class="form-group col-md-6">` chứa toggle đến `</div>` đóng của form-group input hạn mức):

```html
                <div class="form-group col-md-6">
                    <label>Trạng thái áp dụng hạn mức</label>
                    ...
                </div>
                <div class="form-group col-md-6">
                    <label>
                        Hạn mức công nợ tối đa (VNĐ)
                        ...
                    </label>
                    ...
                </div>
```

- [ ] **Step 2: Xóa 2 computed properties**

Xóa `isDebtLimitActiveBool` và `maxDebtLimitFormatted` (line 126-145):

```javascript
    computed: {
        isDebtLimitActiveBool: { ... },
        maxDebtLimitFormatted: { ... },
    },
```

Xóa luôn block `computed` nếu không còn property nào khác.

- [ ] **Step 3: Xóa default data trong `resetModal`**

Trong `resetModal()` (line 156-167), sửa block else để chỉ còn `this.data = {}`:

```javascript
            } else {
                this.data = {}
            }
```

- [ ] **Step 4: Xóa toàn bộ CSS scoped toggle**

Xóa toàn bộ block `<style lang="scss" scoped>` (line 209-258) chứa `.toggle-row`, `.toggle`, `.toggle-track`, `.toggle-thumb`, `.toggle-label`.

---

### Task 10: customer_groups/index.vue — xóa 2 cột, filter, methods

**Files:**
- Modify: `hrm-thanhan-client/pages/category/customer_groups/index.vue`

- [ ] **Step 1: Xóa filter Select2 "Áp dụng hạn mức" trong template**

Xóa block (line 54-63):
```html
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.is_debt_limit_active"
                                                    :options="listDebtLimitStatus"
                                                    placeholder="Áp dụng hạn mức"
                                                    v-on:keyup.enter="getData"
                                                />
                                            </div>
```

- [ ] **Step 2: Xóa 2 template cell**

Xóa template `cell(max_debt_limit)` (line 110-115) và `cell(is_debt_limit_active)` (line 116-119):

```html
                                <template v-slot:cell(max_debt_limit)="{ item }">
                                    ...
                                </template>
                                <template v-slot:cell(is_debt_limit_active)="{ item }">
                                    ...
                                </template>
```

- [ ] **Step 3: Xóa `is_debt_limit_active` khỏi `initialStateForm`**

Xóa dòng `is_debt_limit_active: undefined,` (line 270) trong `initialStateForm`.

- [ ] **Step 4: Xóa 2 field khỏi array `fields`**

Xóa 2 block trong `fields` (line 327-338):
```javascript
                {
                    key: 'max_debt_limit',
                    label: 'Hạn mức công nợ (VNĐ)',
                    sortable: true,
                    tdClass: 'text-right',
                },
                {
                    key: 'is_debt_limit_active',
                    label: 'Áp dụng hạn mức',
                    sortable: true,
                    tdClass: 'text-center',
                },
```

- [ ] **Step 5: Xóa `listDebtLimitStatus` khỏi data**

Xóa block (line 377-386):
```javascript
            listDebtLimitStatus: [
                {
                    id: 1,
                    text: 'Đang áp dụng',
                },
                {
                    id: 0,
                    text: 'Không áp dụng',
                },
            ],
```

- [ ] **Step 6: Xóa 2 entry log columns**

Xóa 2 dòng trong `columns` (line 394-395):
```javascript
                { column: 'max_debt_limit', name: 'Hạn mức công nợ tối đa' },
                { column: 'is_debt_limit_active', name: 'Trạng thái áp dụng hạn mức' },
```

- [ ] **Step 7: Xóa methods `formatMoney` + `getDebtLimitBadge`**

Xóa 2 methods (line 441-450):
```javascript
        formatMoney(v) { ... },
        getDebtLimitBadge(active) { ... },
```

---

## Phase 6 — Test (Task 11)

### Task 11: User test end-to-end

- [ ] **Test 1: Form KH — tạo mới**
  - Mở form tạo KH mới → toggle OFF, input rỗng → lưu OK
  - Bật toggle, để trống hạn mức → toast lỗi "Vui lòng nhập hạn mức công nợ tối đa khi đang áp dụng hạn mức"
  - Bật toggle, nhập 500.000.000 → lưu OK

- [ ] **Test 2: Form KH — sửa**
  - Mở lại KH vừa tạo → toggle ON, giá trị 500.000.000
  - Tắt toggle → input disable nhưng giữ 500.000.000 → lưu OK
  - Bật lại toggle → giá trị vẫn còn

- [ ] **Test 3: Form KH — edit KH cũ**
  - Mở KH cũ (chưa có data 2 cột mới) → toggle OFF, input rỗng, lưu OK

- [ ] **Test 4: List KH**
  - 2 cột mới hiển thị: hạn mức format VND, badge "Đang áp dụng" / "Không áp dụng"
  - KH toggle OFF → cột hạn mức hiện `—`

- [ ] **Test 5: Filter list KH**
  - Chọn "Đang áp dụng" → lọc đúng
  - Chọn "Không áp dụng" → lọc đúng
  - Đặt lại → full list

- [ ] **Test 6: Nhóm KH**
  - Modal tạo/sửa nhóm KH → không còn toggle + input hạn mức
  - List nhóm KH → không còn 2 cột + filter hạn mức
  - Lịch sử thay đổi nhóm KH → vẫn hoạt động bình thường
