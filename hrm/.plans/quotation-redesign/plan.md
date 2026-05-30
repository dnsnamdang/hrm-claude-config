# Quotation Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Biến báo giá thành đối tượng độc lập — hỗ trợ tạo trực tiếp (không qua YCXD giá), 2 type (từ BOM / tự nhập), DB sạch cho thống kê.

**Architecture:** Migration thêm cột `type` + chuyển nullable các FK. Refactor `QuotationService.create()` chung cho cả 2 luồng. FE tách `QuotationForm.vue` (2800 dòng edit.vue) thành component riêng, thêm `create.vue` wrapper.

**Tech Stack:** PHP 7.4, Laravel 8, MySQL, Nuxt 2 (Vue 2), Bootstrap-Vue

---

## File Structure

### Backend (hrm-api)

| File | Action | Responsibility |
|---|---|---|
| `database/migrations/2026_05_28_100000_add_quotation_type_and_nullable_columns.php` | Create | Migration: thêm `type`, chuyển nullable |
| `Modules/Assign/Entities/Quotation.php` | Modify | Thêm TYPE_* constants + `getTypeList()` |
| `Modules/Assign/Http/Requests/Quotation/QuotationStoreRequest.php` | Modify | Đổi rules: `project_id` required thay vì `pricing_request_id` |
| `Modules/Assign/Services/QuotationService.php` | Modify | Refactor: `create()` chung + `createFromPricingRequest()` delegate |
| `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` | Modify | Đổi `store()` dùng service mới |
| `Modules/Assign/Transformers/QuotationResource.php` | Modify | Thêm `type`, `type_name` |
| `Modules/Assign/Transformers/DetailQuotationResource.php` | Modify | Thêm `type`, `type_name` |

### Frontend (hrm-client)

| File | Action | Responsibility |
|---|---|---|
| `pages/assign/quotations/create.vue` | Create | Wrapper tạo mới: chọn dự án → load BOM → render QuotationForm |
| `pages/assign/quotations/components/QuotationForm.vue` | Create | Form chung tách từ edit.vue |
| `pages/assign/quotations/_id/edit.vue` | Modify | Refactor: tách form ra, giữ wrapper load data |
| `pages/assign/quotations/index.vue` | Modify | Thêm button "Tạo báo giá" + cột type |
| `pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue` | Modify | Sửa navigate URL |

---

## Phase 1: Backend — DB + Model + Request

### Task 1: Migration — thêm type + chuyển nullable

**Files:**
- Create: `hrm-api/database/migrations/2026_05_28_100000_add_quotation_type_and_nullable_columns.php`

- [ ] **Step 1: Tạo migration file**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddQuotationTypeAndNullableColumns extends Migration
{
    public function up()
    {
        Schema::table('quotations', function (Blueprint $table) {
            $table->tinyInteger('type')->default(1)->after('code')
                  ->comment('1=Từ BOM, 2=Tự nhập');

            $table->unsignedBigInteger('pricing_request_id')->nullable()->change();
            $table->unsignedBigInteger('bom_list_id')->nullable()->change();
            $table->unsignedBigInteger('solution_id')->nullable()->change();
            $table->unsignedBigInteger('solution_version_id')->nullable()->change();
            $table->unsignedBigInteger('currency_id')->nullable()->change();

            $table->text('description')->nullable()->change();
            $table->string('delivery_time')->nullable()->change();
            $table->string('warranty_time')->nullable()->change();
            $table->text('payment_terms')->nullable()->change();
        });

        // Drop unique riêng vì pricing_request_id giờ nullable + không còn 1-1
        Schema::table('quotations', function (Blueprint $table) {
            // Tên index: quotations_pricing_request_id_unique
            $table->dropUnique(['pricing_request_id']);
            $table->index('type');
        });
    }

    public function down()
    {
        Schema::table('quotations', function (Blueprint $table) {
            $table->dropIndex(['type']);
            $table->dropColumn('type');
            $table->unsignedBigInteger('pricing_request_id')->unique()->change();
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

Run: `cd hrm-api && php artisan migrate`
Expected: Migration chạy OK, bảng `quotations` có cột `type`, các FK nullable.

- [ ] **Step 3: Verify schema**

Run: `cd hrm-api && php artisan tinker --execute="echo \Illuminate\Support\Facades\Schema::hasColumn('quotations', 'type') ? 'OK' : 'FAIL';"`
Expected: `OK`

---

### Task 2: Model Quotation — thêm TYPE constants

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/Quotation.php:10-50`

- [ ] **Step 1: Thêm constants sau STATUS_DUNG (dòng ~18)**

Thêm sau `const STATUS_DUNG = 6;`:

```php
const TYPE_FROM_BOM = 1;
const TYPE_SELF_BUILT = 2;
```

- [ ] **Step 2: Thêm method getTypeList() sau getStatusList()**

Thêm sau closing `}` của `getStatusList()` (sau dòng ~51):

```php
public static function getTypeList()
{
    return [
        self::TYPE_FROM_BOM => ['name' => 'Từ BOM', 'color' => '#2196F3'],
        self::TYPE_SELF_BUILT => ['name' => 'Tự nhập', 'color' => '#FF9800'],
    ];
}
```

- [ ] **Step 3: Verify**

Run: `cd hrm-api && php artisan tinker --execute="echo \Modules\Assign\Entities\Quotation::TYPE_FROM_BOM . ' ' . \Modules\Assign\Entities\Quotation::TYPE_SELF_BUILT;"`
Expected: `1 2`

---

### Task 3: QuotationStoreRequest — đổi rules cho tạo trực tiếp

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/Quotation/QuotationStoreRequest.php`

- [ ] **Step 1: Đổi nội dung rules()**

Thay toàn bộ nội dung file thành:

```php
<?php

namespace Modules\Assign\Http\Requests\Quotation;

use Illuminate\Foundation\Http\FormRequest;

class QuotationStoreRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'project_id'   => 'required|integer|exists:prospective_projects,id',
            'bom_list_id'  => 'nullable|integer',
            'currency_id'  => 'nullable|integer',
            'description'  => 'nullable|string',
            'deadline'     => 'nullable|date',
            'delivery_time'  => 'nullable',
            'warranty_time'  => 'nullable',
            'payment_terms'  => 'nullable|string',
            'validity_days'  => 'nullable|integer|min:0',
            'note'           => 'nullable|string',

            'products'                          => 'sometimes|array',
            'products.*.quotation_group_id'     => 'nullable',
            'products.*.parent_id'              => 'nullable|integer',
            'products.*.product_type'           => 'nullable|integer|in:1,2',
            'products.*.erp_product_id'         => 'nullable|integer',
            'products.*.code'                   => 'nullable|string|max:255',
            'products.*.name'                   => 'nullable|string|max:255',
            'products.*.model_id'               => 'nullable|integer',
            'products.*.brand_id'               => 'nullable|integer',
            'products.*.origin_id'              => 'nullable|integer',
            'products.*.unit_id'                => 'nullable|integer',
            'products.*.qty_needed'             => 'nullable|numeric|min:0',
            'products.*.product_attributes'     => 'nullable|string',
            'products.*.sort_order'             => 'nullable|integer|min:0',
            'products.*.estimated_price'        => 'nullable|numeric|min:0',
            'products.*.quoted_price'           => 'nullable|numeric|min:0',
            'products.*.vat_percent'            => 'nullable|numeric|min:0|max:100',
            'products.*.discount_input_mode'    => 'nullable|in:percent,amount',
            'products.*.discount_percent'       => 'nullable|numeric|min:0|max:100',
            'products.*.discount_amount'        => 'nullable|numeric|min:0',
            'products.*.allocated_discount_amount' => 'nullable|numeric|min:0',

            'groups'              => 'sometimes|array',
            'groups.*.temp_id'    => 'nullable|string',
            'groups.*.name'       => 'required|string|max:255',
            'groups.*.sort_order' => 'nullable|integer|min:0',

            'discount_method'                        => 'nullable|integer|in:1,2',
            'quotation_discounts'                    => 'sometimes|array',
            'quotation_discounts.*.discount_type_id' => 'required_with:quotation_discounts.*|integer',
            'quotation_discounts.*.input_mode'       => 'required_with:quotation_discounts.*|in:percent,amount',
            'quotation_discounts.*.percent_value'    => 'nullable|numeric|min:0|max:100',
            'quotation_discounts.*.amount_value'     => 'nullable|numeric|min:0',

            'service_items'                        => 'sometimes|array',
            'service_items.*.name'                 => 'required|string|max:255',
            'service_items.*.specification'        => 'nullable|string|max:500',
            'service_items.*.unit_id'              => 'required|integer',
            'service_items.*.qty'                  => 'required|numeric|min:0',
            'service_items.*.estimated_price'      => 'nullable|numeric|min:0',
            'service_items.*.quoted_price'         => 'nullable|numeric|min:0',
            'service_items.*.vat_percent'          => 'nullable|numeric|min:0|max:100',
            'service_items.*.discount_input_mode'  => 'nullable|in:percent,amount',
            'service_items.*.discount_percent'     => 'nullable|numeric|min:0|max:100',
            'service_items.*.discount_amount'      => 'nullable|numeric|min:0',
            'service_items.*.allocated_discount_amount' => 'nullable|numeric|min:0',
            'service_items.*.sort_order'           => 'nullable|integer|min:0',
        ];
    }
}
```

---

## Phase 2: Backend — Service Refactor + Controller

### Task 4: QuotationService — tạo method create() chung

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Thêm method `create()` — đặt trước `createFromRequest()`**

Thêm trước `public function createFromRequest(PricingRequest $request): Quotation` (dòng ~32):

```php
/**
 * Tạo báo giá chung — dùng cho cả tạo trực tiếp và delegate từ YCXD giá.
 *
 * @param array $data Validated data từ QuotationStoreRequest
 *   - project_id (required)
 *   - bom_list_id (nullable)
 *   - pricing_request_id (nullable, set bởi createFromPricingRequest)
 *   - currency_id (nullable, default VNĐ)
 *   - products, groups, service_items, quotation_discounts (optional arrays)
 */
public function create(array $data): Quotation
{
    return DB::transaction(function () use ($data) {
        $project = ProspectiveProject::findOrFail($data['project_id']);
        $customer = $project->customer_id ? Customer::find($project->customer_id) : null;
        $defaultCurrency = TpCurrency::where('code', 'VNĐ')->value('id') ?? 1;

        $bomList = null;
        $solutionVersionCode = null;
        $moduleVersionCode = null;
        $type = Quotation::TYPE_SELF_BUILT;

        if (!empty($data['bom_list_id'])) {
            $bomList = BomList::find($data['bom_list_id']);
            if ($bomList) {
                $type = Quotation::TYPE_FROM_BOM;
                if ($bomList->solution_version_id) {
                    $sv = SolutionVersion::find($bomList->solution_version_id);
                    $solutionVersionCode = $sv ? $sv->code : null;
                }
                if ($bomList->solution_module_version_id) {
                    $smv = SolutionModuleVersion::find($bomList->solution_module_version_id);
                    $moduleVersionCode = $smv ? $smv->code : null;
                }
            }
        }

        $quotation = new Quotation();
        $quotation->fill([
            'type' => $type,
            'pricing_request_id' => $data['pricing_request_id'] ?? null,
            'bom_list_id' => $bomList ? $bomList->id : null,
            'project_id' => $project->id,
            'solution_id' => $bomList ? $bomList->solution_id : null,
            'solution_version_id' => $bomList ? $bomList->solution_version_id : null,
            'solution_version_code' => $solutionVersionCode,
            'solution_module_id' => $bomList ? $bomList->solution_module_id : null,
            'solution_module_version_id' => $bomList ? $bomList->solution_module_version_id : null,
            'module_version_code' => $moduleVersionCode,
            'currency_id' => $data['currency_id'] ?? ($bomList ? $bomList->currency_id : $defaultCurrency),
            'description' => $data['description'] ?? null,
            'deadline' => $data['deadline'] ?? null,
            'delivery_time' => $data['delivery_time'] ?? null,
            'warranty_time' => $data['warranty_time'] ?? null,
            'payment_terms' => $data['payment_terms'] ?? null,
            'validity_days' => $data['validity_days'] ?? null,
            'note' => $data['note'] ?? null,
            'discount_method' => $data['discount_method'] ?? null,
            'customer_id' => $project->customer_id,
            'customer_code' => $project->customer_code ?? ($customer ? $customer->code : null),
            'customer_name' => $project->customer_name ?: ($customer ? $customer->name : ''),
            'customer_tax_code' => $project->customer_tax_code ?? null,
            'customer_address' => $project->customer_address ?? null,
            'customer_email' => $project->customer_email ?? null,
            'customer_contact_name' => $project->customer_contact_name ?? null,
            'customer_contact_phone' => $project->customer_contact_phone ?? null,
            'status' => Quotation::STATUS_DANG_TAO,
            'created_by' => auth()->id(),
            'updated_by' => auth()->id(),
        ]);
        $quotation->code = $quotation->getNextCode();
        $quotation->save();

        // Copy sản phẩm từ BOM
        if ($bomList) {
            $bomProducts = BomListProduct::where('bom_list_id', $bomList->id)->get();
            $erpIds = $bomProducts->pluck('erp_product_id')->filter()->unique()->values()->toArray();
            $retailPrices = TpProductUnitPrice::getRetailPrices($erpIds);
            $costPrices = TpProductUnitPrice::getCostPrices($erpIds);
            $rows = [];
            $now = now();
            foreach ($bomProducts as $bp) {
                $erpId = $bp->erp_product_id ? (int) $bp->erp_product_id : null;
                $rows[] = [
                    'quotation_id' => $quotation->id,
                    'bom_list_product_id' => $bp->id,
                    'estimated_price' => $erpId ? ($costPrices[$erpId] ?? 0) : (float) ($bp->estimated_price ?? 0),
                    'quoted_price' => $erpId ? ($retailPrices[$erpId] ?? 0) : 0,
                    'created_by' => auth()->id(),
                    'updated_by' => auth()->id(),
                    'created_at' => $now,
                    'updated_at' => $now,
                ];
            }
            if (!empty($rows)) {
                foreach (array_chunk($rows, 500) as $chunk) {
                    QuotationProductPrice::insert($chunk);
                }
            }
        }

        // Groups cho báo giá tự nhập
        $groupIdMap = [];
        if (!$bomList && !empty($data['groups']) && is_array($data['groups'])) {
            $groupIdMap = $this->syncDirectGroups($quotation, $data['groups']);
        }

        // Products cho báo giá tự nhập
        if (!$bomList && !empty($data['products']) && is_array($data['products'])) {
            if (!empty($groupIdMap)) {
                foreach ($data['products'] as &$p) {
                    $gid = $p['quotation_group_id'] ?? null;
                    if ($gid && isset($groupIdMap[$gid])) {
                        $p['quotation_group_id'] = $groupIdMap[$gid];
                    }
                }
                unset($p);
            }
            $this->upsertDirectProducts($quotation, $data['products']);
        }

        // Service items
        if (!empty($data['service_items']) && is_array($data['service_items'])) {
            foreach ($data['service_items'] as $si) {
                $quotation->serviceItems()->create([
                    'name' => $si['name'] ?? '',
                    'specification' => $si['specification'] ?? null,
                    'unit_id' => $si['unit_id'] ?? null,
                    'qty' => $si['qty'] ?? 0,
                    'estimated_price' => $si['estimated_price'] ?? 0,
                    'quoted_price' => $si['quoted_price'] ?? 0,
                    'vat_percent' => $si['vat_percent'] ?? 0,
                    'discount_input_mode' => $si['discount_input_mode'] ?? null,
                    'discount_percent' => $si['discount_percent'] ?? 0,
                    'discount_amount' => $si['discount_amount'] ?? 0,
                    'allocated_discount_amount' => $si['allocated_discount_amount'] ?? 0,
                    'sort_order' => $si['sort_order'] ?? 0,
                ]);
            }
        }

        // Quotation discounts
        if (!empty($data['quotation_discounts']) && is_array($data['quotation_discounts'])) {
            foreach ($data['quotation_discounts'] as $qd) {
                QuotationDiscount::create([
                    'quotation_id' => $quotation->id,
                    'discount_type_id' => $qd['discount_type_id'],
                    'input_mode' => $qd['input_mode'] ?? 'percent',
                    'percent_value' => $qd['percent_value'] ?? 0,
                    'amount_value' => $qd['amount_value'] ?? 0,
                ]);
            }
        }

        $this->recomputeTotals($quotation);

        if ($project->status < ProspectiveProject::STATUS_DU_TOAN) {
            $project->update(['status' => ProspectiveProject::STATUS_DU_TOAN]);
        }

        $this->logHistory($quotation->id, QuotationHistory::ACTION_CREATE, null, Quotation::STATUS_DANG_TAO);

        return $quotation->fresh();
    });
}
```

- [ ] **Step 2: Xóa method `createDirect()` (dòng ~237-379)**

Xóa toàn bộ method `createDirect()` vì logic đã gộp vào `create()`.

- [ ] **Step 3: Verify — tinker test create()**

Run: `cd hrm-api && php artisan tinker --execute="echo 'QuotationService methods: ' . implode(', ', get_class_methods(\Modules\Assign\Services\QuotationService::class));"`
Expected: Có `create`, có `createFromRequest`, có `createFromBom`, KHÔNG có `createDirect`.

---

### Task 5: QuotationController — đổi store() dùng create() chung

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php:88-103`

- [ ] **Step 1: Thay method store()**

Thay toàn bộ method `store()` (dòng ~88-103) thành:

```php
public function store(QuotationStoreRequest $request)
{
    try {
        $project = \Modules\Assign\Entities\ProspectiveProject::findOrFail($request->project_id);

        $employeeId = auth()->user()->employee_id ?? null;
        if (!$employeeId || (int) $project->main_sale_employee_id !== (int) $employeeId) {
            abort(403, 'Bạn không phải Sale phụ trách dự án này');
        }

        $quotation = $this->service->create($request->validated());

        return $this->responseJson('Đã tạo báo giá', Response::HTTP_OK, new DetailQuotationResource($quotation));
    } catch (ValidationException $e) {
        throw $e;
    } catch (Exception $e) {
        Log::error($e);
        $code = $e->getCode() === 403 ? Response::HTTP_FORBIDDEN : Response::HTTP_UNPROCESSABLE_ENTITY;
        return $this->responseJson($e->getMessage(), $code);
    }
}
```

- [ ] **Step 2: Xóa method createDirect() (dòng ~123-136)**

Xóa toàn bộ method `createDirect()` vì `store()` đã thay thế.

- [ ] **Step 3: Cập nhật routes — xóa route create-direct**

File: `hrm-api/Modules/Assign/Routes/api.php` dòng ~367

Xóa dòng:
```php
Route::post('/create-direct', [QuotationController::class, 'createDirect']);
```

Route `POST /` (dòng ~369) đã tồn tại và sẽ gọi `store()` mới.

---

### Task 6: Resources — thêm type + type_name

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/QuotationResource.php:32-74`
- Modify: `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php`

- [ ] **Step 1: QuotationResource — thêm type sau code**

Trong method `toArray()`, thêm sau `'code' => $this->code,` (dòng ~34):

```php
'type' => (int) $this->type,
'type_name' => Quotation::getTypeList()[(int) $this->type]['name'] ?? '',
```

- [ ] **Step 2: DetailQuotationResource — thêm type**

Tìm `return [` trong `toArray()` (dòng ~124), thêm sau `'code' =>`:

```php
'type' => (int) $this->type,
'type_name' => Quotation::getTypeList()[(int) $this->type]['name'] ?? '',
```

- [ ] **Step 3: Verify API response**

Run: `cd hrm-api && php artisan tinker --execute="
\$q = \Modules\Assign\Entities\Quotation::first();
echo json_encode(['type' => \$q->type, 'type_name' => \Modules\Assign\Entities\Quotation::getTypeList()[\$q->type]['name'] ?? '']);
"`
Expected: `{"type":1,"type_name":"Từ BOM"}`

---

## Phase 3: Frontend — QuotationForm tách từ edit.vue

### Task 7: Tạo QuotationForm.vue — copy template + script từ edit.vue

**Files:**
- Create: `hrm-client/pages/assign/quotations/components/QuotationForm.vue`
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

Đây là task lớn nhất — tách ~2500 dòng form logic ra khỏi edit.vue.

**Chiến lược:**
1. Copy toàn bộ `edit.vue` thành `QuotationForm.vue`
2. Sửa QuotationForm: thêm props (`mode`, `initialData`, `quotationType`), emit thay vì gọi API trực tiếp
3. Sửa edit.vue: xóa form logic, import QuotationForm, truyền data + handle events

- [ ] **Step 1: Copy edit.vue thành QuotationForm.vue**

```bash
cp hrm-client/pages/assign/quotations/_id/edit.vue \
   hrm-client/pages/assign/quotations/components/QuotationForm.vue
```

- [ ] **Step 2: Sửa QuotationForm.vue — đổi component name + thêm props**

Trong `<script>`, đổi:
```js
export default {
    name: 'QuotationForm',
    // Bỏ layout: 'default-sidebar' (layout thuộc page, không thuộc component)
    // Bỏ mixins: [PageTitleMixin] (page title thuộc wrapper)
    props: {
        mode: { type: String, default: 'edit', validator: v => ['create', 'edit'].includes(v) },
        initialData: { type: Object, default: null },
        quotationType: { type: Number, default: 1 },
    },
```

- [ ] **Step 3: QuotationForm.vue — thay data loading bằng props**

Trong `data()`, xóa `loading: false`, `item: null`. Thêm:
```js
data() {
    return {
        item: this.initialData ? JSON.parse(JSON.stringify(this.initialData)) : null,
        // ... giữ nguyên phần còn lại
    }
},
```

Thay `mounted()`:
```js
async mounted() {
    if (this.initialData) {
        this.item = JSON.parse(JSON.stringify(this.initialData))
        this.initFormFromItem()
    }
    await this.loadConfigs()
    await this.loadCurrencyOptions()
    await this.loadDiscountTypes()
    await this.loadUnitOptions()
},
```

Thêm `watch` cho `initialData`:
```js
watch: {
    initialData: {
        deep: true,
        handler(val) {
            if (val) {
                this.item = JSON.parse(JSON.stringify(val))
                this.initFormFromItem()
            }
        }
    }
},
```

- [ ] **Step 4: QuotationForm.vue — computed sử dụng props**

Thay `isCreateMode`:
```js
isCreateMode() {
    return this.mode === 'create'
},
```

Bỏ `pageTitle` computed (thuộc wrapper).

Thay `isDirectQuotation`:
```js
isDirectQuotation() {
    if (this.mode === 'create') return this.quotationType === 2
    return !!this.item?.is_direct_quotation
},
```

- [ ] **Step 5: QuotationForm.vue — emit thay vì gọi API**

Thay method `save()`:
```js
async save() {
    const data = this.buildSavePayload()
    this.$emit('save', data)
},
```

Thêm method `buildSavePayload()` — extract logic build payload từ save() cũ:
```js
buildSavePayload() {
    const data = {
        description: this.form.description || null,
        delivery_time: this.form.delivery_time,
        warranty_time: this.form.warranty_time,
        payment_terms: this.form.payment_terms,
        validity_days: this.form.validity_days,
        note: this.form.note,
        currency_id: this.form.currency_id,
        discount_method: this.discountMethod,
    }
    // Products
    if (this.isDirectQuotation) {
        data.groups = this.directGroups.map(g => ({
            id: g.id || undefined,
            temp_id: g.temp_id || undefined,
            name: g.name,
            sort_order: g.sort_order,
        }))
    }
    data.products = this.products.map(p => ({ ...p }))
    // Service items
    data.service_items = this.serviceItems.map(si => ({ ...si }))
    // Discounts
    if (this.discountMethod === 2) {
        data.quotation_discounts = this.quotationDiscounts.map(qd => ({ ...qd }))
    }
    return data
},
```

Thay `handleSaveDraft()` — emit 'save':
```js
async handleSaveDraft() {
    this.saving = true
    try {
        const data = this.buildSavePayload()
        this.$emit('save', data)
    } finally {
        this.saving = false
    }
},
```

Thay `submitForApproval()` — emit 'submit-approval':
```js
submitForApproval() {
    this.$emit('submit-approval')
},
```

- [ ] **Step 6: QuotationForm.vue — xóa route-related code**

Xóa:
- `watch: { '$route.params.id' }` (thuộc wrapper)
- `initCreateMode()` method (thuộc create.vue wrapper)
- `showProjectPickerModal` + project picker modal template + methods (thuộc create.vue)
- `loadMyProjects`, `searchProjects`, `selectProject` methods (thuộc create.vue)

- [ ] **Step 7: QuotationForm.vue — method initFormFromItem()**

Extract logic khởi tạo form từ item (hiện nằm rải rác trong `mounted` và `loadDetail`):

```js
initFormFromItem() {
    if (!this.item) return
    this.form = {
        description: this.item.description || '',
        validity_days: this.item.validity_days,
        delivery_time: this.item.delivery_time,
        warranty_time: this.item.warranty_time,
        payment_terms: this.item.payment_terms || '',
        note: this.item.note || '',
        currency_id: this.item.currency?.id || this.item.currency_id || null,
    }
    this.products = this.item.products || []
    this.serviceItems = this.item.service_items || []
    this.discountMethod = this.item.discount_method || null
    this.quotationDiscounts = this.item.quotation_discounts || []
    this.directGroups = this.item.groups || []
    this.canViewCostPrice = this.item.can_view_cost_price || false
},
```

---

### Task 8: Refactor edit.vue — dùng QuotationForm component

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

- [ ] **Step 1: Cắt gọn edit.vue — chỉ giữ wrapper logic**

Thay toàn bộ edit.vue thành wrapper ~150 dòng:

```vue
<template>
    <div class="v2-styles min-vh-100 pt-1 pb-5 quotation-edit">
        <div class="container-fluid">
            <div v-if="loading" class="text-center py-4">Đang tải...</div>
            <div v-else-if="!item" class="text-center py-4 text-muted">Không tìm thấy báo giá.</div>
            <QuotationForm
                v-else
                mode="edit"
                :initialData="item"
                :quotationType="item.type || 1"
                @save="handleSave"
                @submit-approval="handleSubmitApproval"
            />
        </div>
    </div>
</template>

<script>
import QuotationForm from '../components/QuotationForm.vue'
import PageTitleMixin from '@/mixins/PageTitleMixin'

export default {
    name: 'QuotationEdit',
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    components: { QuotationForm },
    data() {
        return {
            loading: false,
            item: null,
        }
    },
    computed: {
        pageTitle() {
            if (!this.item) return 'Làm giá'
            const statusColor = this.item.status_color || '#9E9E9E'
            const statusName = this.item.status_name || ''
            const statusTxt = statusName
                ? `<span class="topbar-status-inline" style="color:${statusColor}">(${statusName})</span>`
                : ''
            return `Làm giá: <strong>${this.item.code || ''}</strong> ${statusTxt}`
        },
    },
    async mounted() {
        await this.loadDetail()
    },
    methods: {
        async loadDetail() {
            this.loading = true
            try {
                const id = this.$route.params.id
                const res = await this.$store.dispatch('apiGetMethod', `assign/quotations/${id}`)
                this.item = res?.data || null
            } catch (e) {
                this.item = null
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi tải báo giá' })
            } finally {
                this.loading = false
            }
        },
        async handleSave(data) {
            try {
                const id = this.$route.params.id
                await this.$store.dispatch('apiPutMethod', {
                    url: `assign/quotations/${id}`,
                    payload: data,
                })
                this.$toasted?.global?.success?.({ message: 'Đã lưu báo giá' })
                await this.loadDetail()
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi lưu' })
            }
        },
        async handleSubmitApproval() {
            try {
                const id = this.$route.params.id
                await this.$store.dispatch('apiPostMethod', {
                    url: `assign/quotations/${id}/submit`,
                    payload: {},
                })
                this.$toasted?.global?.success?.({ message: 'Đã gửi duyệt' })
                await this.loadDetail()
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi gửi duyệt' })
            }
        },
    },
}
</script>
```

**Lưu ý quan trọng:** Task 7 và Task 8 phải làm cùng nhau. QuotationForm.vue được tách từ edit.vue — cả hai file phải hoạt động đồng bộ. Test luồng edit sau khi tách để đảm bảo regression-free.

- [ ] **Step 2: Test regression — edit báo giá hiện có**

Mở browser: `http://localhost:3000/assign/quotations/{id_có_sẵn}/edit`
Kiểm tra:
- Form hiển thị đúng dữ liệu
- Sửa giá bán → lưu → reload → giá mới được lưu
- Tab dịch vụ hoạt động
- Tab chiết khấu hoạt động

---

## Phase 4: Frontend — create.vue + entry points

### Task 9: Tạo create.vue — wrapper tạo mới

**Files:**
- Create: `hrm-client/pages/assign/quotations/create.vue`

- [ ] **Step 1: Tạo file create.vue**

```vue
<template>
    <div class="v2-styles min-vh-100 pt-1 pb-5 quotation-create">
        <div class="container-fluid">
            <!-- Chọn dự án -->
            <div v-if="!selectedProject" class="card p-4">
                <h5 class="mb-3">Tạo báo giá mới</h5>
                <div class="form-group">
                    <V2BaseLabel>Dự án <span class="text-danger">*</span></V2BaseLabel>
                    <div class="input-group cursor-pointer" @click="showProjectModal = true">
                        <input
                            type="text"
                            class="form-control"
                            placeholder="Chọn dự án..."
                            :value="selectedProject ? selectedProject.name : ''"
                            readonly
                        />
                        <div class="input-group-append">
                            <span class="input-group-text"><i class="ri-search-line"></i></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chọn BOM (nếu có nhiều) -->
            <div v-else-if="bomOptions.length > 1 && !selectedBom" class="card p-4">
                <h5 class="mb-3">Chọn BOM tổng hợp</h5>
                <p class="text-muted mb-3">Dự án <strong>{{ selectedProject.name }}</strong> có {{ bomOptions.length }} BOM tổng hợp đã duyệt.</p>
                <div class="form-group">
                    <V2BaseLabel>BOM tổng hợp <span class="text-danger">*</span></V2BaseLabel>
                    <V2BaseSelect
                        :options="bomSelectOptions"
                        placeholder="Chọn BOM..."
                        @input="onBomSelect"
                    />
                </div>
            </div>

            <!-- Loading khi đang tải BOM products -->
            <div v-else-if="loadingBomProducts" class="text-center py-4">Đang tải sản phẩm từ BOM...</div>

            <!-- Form báo giá -->
            <QuotationForm
                v-else-if="formReady"
                mode="create"
                :initialData="initialFormData"
                :quotationType="quotationType"
                @save="handleCreate"
            />

            <!-- Modal chọn dự án -->
            <b-modal
                :visible="showProjectModal"
                title="Chọn dự án"
                size="lg"
                centered
                :hide-footer="true"
                @hidden="showProjectModal = false"
            >
                <div class="mb-3">
                    <input
                        type="text"
                        class="form-control"
                        placeholder="Tìm theo tên hoặc mã dự án..."
                        v-model="projectSearch"
                        @input="debouncedSearchProjects"
                    />
                </div>
                <div v-if="projectSearching" class="text-center py-3">Đang tìm...</div>
                <div v-else-if="projectResults.length === 0" class="text-center py-3 text-muted">Không tìm thấy dự án nào.</div>
                <div v-else class="list-group">
                    <a
                        v-for="p in projectResults"
                        :key="p.id"
                        href="#"
                        class="list-group-item list-group-item-action"
                        @click.prevent="selectProject(p)"
                    >
                        <div class="font-weight-bold">{{ p.code }} — {{ p.name }}</div>
                        <small class="text-muted">KH: {{ p.customer_name || '—' }}</small>
                    </a>
                </div>
            </b-modal>
        </div>
    </div>
</template>

<script>
import QuotationForm from './components/QuotationForm.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import PageTitleMixin from '@/mixins/PageTitleMixin'

let searchTimer = null

export default {
    name: 'QuotationCreate',
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    components: { QuotationForm, V2BaseLabel, V2BaseSelect },
    data() {
        return {
            selectedProject: null,
            bomOptions: [],
            selectedBom: null,
            quotationType: 2,
            loadingBomProducts: false,
            formReady: false,
            initialFormData: null,
            creating: false,
            // Project picker
            showProjectModal: false,
            projectSearch: '',
            projectResults: [],
            projectSearching: false,
        }
    },
    computed: {
        pageTitle() { return 'Tạo báo giá mới' },
        currentEmployeeId() { return this.$store.state.current_employee?.id || null },
        bomSelectOptions() {
            return this.bomOptions.map(b => ({
                value: b.id,
                label: `${b.code} — ${b.name}`,
            }))
        },
    },
    async mounted() {
        const projectId = this.$route.query.project_id
        if (projectId) {
            await this.loadProjectById(projectId)
        }
    },
    methods: {
        async loadProjectById(id) {
            try {
                const res = await this.$store.dispatch('apiGetMethod', `assign/prospective-projects/${id}`)
                const project = res?.data || null
                if (!project) {
                    this.$toasted?.global?.error?.({ message: 'Không tìm thấy dự án' })
                    return
                }
                if (Number(project.main_sale_employee_id) !== Number(this.currentEmployeeId)) {
                    this.$toasted?.global?.error?.({ message: 'Bạn không phải Sale phụ trách dự án này' })
                    return
                }
                await this.onProjectSelected(project)
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi tải dự án' })
            }
        },
        debouncedSearchProjects() {
            clearTimeout(searchTimer)
            searchTimer = setTimeout(() => this.searchProjects(), 300)
        },
        async searchProjects() {
            if (!this.projectSearch.trim()) {
                this.projectResults = []
                return
            }
            this.projectSearching = true
            try {
                const res = await this.$store.dispatch('apiGetMethod',
                    `assign/prospective-projects?search=${encodeURIComponent(this.projectSearch)}&sale_employee_id=${this.currentEmployeeId}&per_page=20`
                )
                this.projectResults = res?.data || []
            } catch (e) {
                this.projectResults = []
            } finally {
                this.projectSearching = false
            }
        },
        async selectProject(project) {
            this.showProjectModal = false
            this.projectSearch = ''
            this.projectResults = []
            await this.onProjectSelected(project)
        },
        async onProjectSelected(project) {
            this.selectedProject = project
            this.selectedBom = null
            this.formReady = false

            // Load BOM tổng hợp đã duyệt
            try {
                const res = await this.$store.dispatch('apiGetMethod',
                    `assign/bom-lists?prospective_project_id=${project.id}&bom_list_type=2&status=4`
                )
                this.bomOptions = res?.data || []
            } catch (e) {
                this.bomOptions = []
            }

            if (this.bomOptions.length === 1) {
                await this.onBomSelected(this.bomOptions[0])
            } else if (this.bomOptions.length === 0) {
                this.quotationType = 2
                this.buildInitialFormData(null)
            }
            // Nếu > 1 BOM → hiện dropdown (template handles it)
        },
        async onBomSelect(bomId) {
            const bom = this.bomOptions.find(b => b.id === Number(bomId))
            if (bom) await this.onBomSelected(bom)
        },
        async onBomSelected(bom) {
            this.selectedBom = bom
            this.quotationType = 1
            this.buildInitialFormData(bom)
        },
        buildInitialFormData(bom) {
            const p = this.selectedProject
            this.initialFormData = {
                code: '(tự sinh)',
                project_id: p.id,
                project: { id: p.id, code: p.code, name: p.name },
                bom_list_id: bom ? bom.id : null,
                bom_list: bom ? { id: bom.id, code: bom.code, name: bom.name } : null,
                solution_version_code: bom ? bom.solution_version_code : null,
                customer_id: p.customer_id,
                customer_name: p.customer_name,
                customer_code: p.customer_code,
                customer_tax_code: p.customer_tax_code,
                customer_address: p.customer_address,
                customer_email: p.customer_email,
                customer_contact_name: p.customer_contact_name,
                customer_contact_phone: p.customer_contact_phone,
                currency_id: null,
                currency: null,
                description: '',
                delivery_time: null,
                warranty_time: null,
                payment_terms: '',
                validity_days: null,
                note: '',
                status: 1,
                status_name: 'Đang tạo',
                status_color: '#9E9E9E',
                type: this.quotationType,
                products: [],
                service_items: [],
                groups: [],
                discount_method: null,
                quotation_discounts: [],
                can_view_cost_price: true,
                is_direct_quotation: this.quotationType === 2,
            }
            this.formReady = true
        },
        async handleCreate(data) {
            if (this.creating) return
            this.creating = true
            try {
                const payload = {
                    ...data,
                    project_id: this.selectedProject.id,
                    bom_list_id: this.selectedBom ? this.selectedBom.id : null,
                }
                const res = await this.$store.dispatch('apiPostMethod', {
                    url: 'assign/quotations',
                    payload,
                })
                const newId = res?.data?.id
                this.$toasted?.global?.success?.({ message: 'Đã tạo báo giá' })
                if (newId) {
                    this.$router.push(`/assign/quotations/${newId}/edit`)
                }
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi tạo báo giá' })
            } finally {
                this.creating = false
            }
        },
    },
}
</script>
```

- [ ] **Step 2: Test tạo báo giá trực tiếp**

Mở: `http://localhost:3000/assign/quotations/create`
Kiểm tra:
- Hiện modal chọn dự án
- Chọn dự án → hệ thống kiểm tra BOM
- Click "Tạo báo giá" → tạo record → redirect edit

---

### Task 10: index.vue — thêm button "Tạo báo giá" + cột type

**Files:**
- Modify: `hrm-client/pages/assign/quotations/index.vue`

- [ ] **Step 1: Thêm button "Tạo báo giá"**

Tìm vị trí header hoặc toolbar trong template, thêm:

```html
<button class="btn btn-primary btn-sm" @click="$router.push('/assign/quotations/create')">
    <i class="ri-add-line mr-1"></i>
    Tạo báo giá
</button>
```

- [ ] **Step 2: Thêm cột "Loại" vào bảng**

Trong `tableColumns` computed hoặc data, thêm cột:

```js
{ key: 'type_name', label: 'Loại', title: 'Loại', align: 'center', width: '100px' },
```

- [ ] **Step 3: Test**

Mở: `http://localhost:3000/assign/quotations`
Kiểm tra: button "Tạo báo giá" hiện, cột "Loại" hiện giá trị "Từ BOM" cho báo giá cũ.

---

### Task 11: ProspectiveProjectQuotationsTab.vue — sửa navigate URL

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue:231-233`

- [ ] **Step 1: Sửa handleCreateDirect()**

Thay:
```js
handleCreateDirect() {
    this.$router.push(`/assign/quotations/new/edit?project_id=${this.projectId}`)
},
```

Thành:
```js
handleCreateDirect() {
    this.$router.push(`/assign/quotations/create?project_id=${this.projectId}`)
},
```

- [ ] **Step 2: Test**

Mở chi tiết dự án TKT → tab Báo giá → click "Tạo báo giá" → phải chuyển sang `/assign/quotations/create?project_id=168`.

---

## Phase 5: Cleanup + Test E2E

### Task 12: Dọn code cũ — xóa createFromBom nếu không dùng

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php`

- [ ] **Step 1: Kiểm tra xem createFromBom có được FE gọi không**

```bash
grep -rn 'create-from-bom' hrm-client/ --include="*.vue" --include="*.js"
```

Nếu **có kết quả**: giữ nguyên, KHÔNG xóa.
Nếu **không có kết quả**: xóa route `create-from-bom` và method `createFromBom()` trong controller.

- [ ] **Step 2: Kiểm tra xem createDirect route cũ đã bị xóa chưa**

```bash
grep -n 'create-direct' hrm-api/Modules/Assign/Routes/api.php
```

Expected: Không có kết quả (đã xóa ở Task 5).

---

### Task 13: Test E2E — regression luồng YCXD giá

- [ ] **Step 1: Test tạo báo giá từ YCXD giá**

Luồng: YCXD giá → nhấn tạo báo giá → kiểm tra báo giá được tạo với `type = 1`, `pricing_request_id != null`.

- [ ] **Step 2: Test edit báo giá từ YCXD giá**

Mở edit báo giá cũ (có pricing_request_id) → sửa giá → lưu → reload → giá mới.

- [ ] **Step 3: Test tạo báo giá trực tiếp — dự án có BOM**

Luồng: `/assign/quotations/create` → chọn dự án có BOM → hệ thống set type=1 → form hiện sản phẩm từ BOM → lưu.

- [ ] **Step 4: Test tạo báo giá trực tiếp — dự án không có BOM**

Luồng: `/assign/quotations/create` → chọn dự án không có BOM → type=2 → form trống → tự nhập sản phẩm → lưu.

- [ ] **Step 5: Test tạo từ tab dự án TKT**

Luồng: chi tiết dự án → tab Báo giá → "Tạo báo giá" → chuyển sang create.vue với project_id tự fill.

- [ ] **Step 6: Test quyền — user không phải Sale phụ trách**

Truy cập `/assign/quotations/create?project_id=X` với user không phải Sale → BE trả 403.

---

## Phase 6: Bugfix — Thêm hàng con cho báo giá tự nhập

### Task 14: Thêm nút "Thêm con" ở dòng hàng cha khi báo giá tự nhập

- [x] **Step 1: Thêm nút "Thêm con" vào cột tên hàng (dòng cha) — giống BomBuilderTableCard.vue**
- [x] **Step 2: Thêm method `openAddChildProduct(parent)` — set parentRowId rồi mở modal**
- [x] **Step 3: Thêm CSS `inline-actions-under` (hover show) + reset parentRowId trong `openAddProduct()`**
- [ ] **Step 4: Test — thêm hàng cha → hover hiện nút "Thêm con" → click → modal → chọn SP → SP con gắn vào cha**

---

## Checkpoint

### Checkpoint — 2026-05-27
Vừa hoàn thành: Tất cả 13 tasks (Task 1-13) — BE + FE hoàn chỉnh
Đang làm dở: Không
Bước tiếp theo: Test trên browser — chạy migration, test flow tạo báo giá trực tiếp + từ BOM
Blocked: Không

**Thay đổi so với plan gốc:**
- Task 7-8: Không tách QuotationForm.vue (rủi ro cao với 2800 dòng). Thay vào đó refactor edit.vue tại chỗ: đổi `is_direct_quotation` → `type`, thêm BOM detection trong `selectProject()`, thêm BOM picker modal.
- Task 9: `create.vue` chỉ là redirect page → `/assign/quotations/new/edit` (tận dụng create mode có sẵn trong edit.vue)
