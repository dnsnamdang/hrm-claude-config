# BOM List Phase 7 — Cập nhật theo yêu cầu khách hàng

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gộp popup thêm hàng hoá (ERP + tạo mới), thêm cấp nhóm hàng (grouping), validate BOM tổng hợp unique.

**Architecture:** Thêm 2 model mới cho second DB (TpProduct, TpProductUnit), 1 entity mới (BomListGroup), 2 migration, cập nhật BomListService + BomBuilderEditor. FE gộp PickModal + QuickCreateModal thành AddProductModal với 2 tab.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, MySQL (dual DB: hrm_tpe + erp2326)

---

## File Structure

### Backend — Tạo mới
- `Modules/Human/Entities/TpProduct.php` — Model products từ ERP (mysql2)
- `Modules/Human/Entities/TpProductUnit.php` — Model product_units từ ERP (mysql2)
- `Modules/Assign/Entities/BomListGroup.php` — Entity nhóm hàng
- `database/migrations/2026_04_08_100000_create_bom_list_groups_table.php`
- `database/migrations/2026_04_08_100001_add_erp_product_id_and_group_id_to_bom_list_products.php`

### Backend — Sửa
- `Modules/Assign/Entities/BomList.php` — Thêm relationship groups()
- `Modules/Assign/Entities/BomListProduct.php` — Thêm erp_product_id, bom_list_group_id, relationships
- `Modules/Assign/Services/BomListService.php` — Thêm syncGroups(), syncErpFields(), validateUniqueAggregate(), sửa syncProducts(), loadDetail(), store(), update()
- `Modules/Assign/Http/Controllers/Api/V1/BomListController.php` — Thêm searchErpProducts()
- `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php` — Cập nhật rules cho groups
- `Modules/Assign/Routes/api.php` — Thêm route erp-products

### Frontend — Tạo mới
- `pages/assign/bom-list/components/BomBuilderAddProductModal.vue` — Popup gộp 2 tab

### Frontend — Sửa
- `pages/assign/bom-list/components/BomBuilderEditor.vue` — Data groups mới, gọi API ERP, quản lý nhóm
- `pages/assign/bom-list/components/BomBuilderTableCard.vue` — Hiển thị row nhóm, STT I/II/III, button tạo nhóm
- `pages/assign/bom-list/components/BomBuilderSubBomModal.vue` — Filter theo solution/module, exclude nháp

### Frontend — Xoá
- `pages/assign/bom-list/components/BomBuilderPickModal.vue` — Thay bằng AddProductModal
- `pages/assign/bom-list/components/BomBuilderQuickCreateModal.vue` — Gộp vào AddProductModal

---

## Task 1: Migration + Entity — bom_list_groups

**Files:**
- Create: `database/migrations/2026_04_08_100000_create_bom_list_groups_table.php`
- Create: `Modules/Assign/Entities/BomListGroup.php`

- [ ] **Step 1: Tạo migration**

```php
<?php
// database/migrations/2026_04_08_100000_create_bom_list_groups_table.php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateBomListGroupsTable extends Migration
{
    public function up()
    {
        Schema::create('bom_list_groups', function (Blueprint $table) {
            $table->id();
            $table->integer('bom_list_id');
            $table->string('name');
            $table->integer('sort_order')->default(0);
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('bom_list_groups');
    }
}
```

- [ ] **Step 2: Tạo entity BomListGroup**

```php
<?php
// Modules/Assign/Entities/BomListGroup.php

namespace Modules\Assign\Entities;

use App\Models\BaseModel;

class BomListGroup extends BaseModel
{
    protected $table = 'bom_list_groups';

    protected $guarded = [];

    public function bomList()
    {
        return $this->belongsTo(BomList::class, 'bom_list_id');
    }

    public function products()
    {
        return $this->hasMany(BomListProduct::class, 'bom_list_group_id');
    }
}
```

- [ ] **Step 3: Chạy migration**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-api
php artisan migrate
```

Expected: Migration chạy thành công, bảng `bom_list_groups` được tạo.

---

## Task 2: Migration — thêm erp_product_id + bom_list_group_id vào bom_list_products

**Files:**
- Create: `database/migrations/2026_04_08_100001_add_erp_product_id_and_group_id_to_bom_list_products.php`

- [ ] **Step 1: Tạo migration**

```php
<?php
// database/migrations/2026_04_08_100001_add_erp_product_id_and_group_id_to_bom_list_products.php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddErpProductIdAndGroupIdToBomListProducts extends Migration
{
    public function up()
    {
        Schema::table('bom_list_products', function (Blueprint $table) {
            $table->unsignedBigInteger('erp_product_id')->nullable()->after('product_project_id');
            $table->integer('bom_list_group_id')->nullable()->after('parent_id');
        });
    }

    public function down()
    {
        Schema::table('bom_list_products', function (Blueprint $table) {
            $table->dropColumn(['erp_product_id', 'bom_list_group_id']);
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
php artisan migrate
```

Expected: 2 cột mới xuất hiện trong bảng `bom_list_products`.

---

## Task 3: Model ERP — TpProduct + TpProductUnit

**Files:**
- Create: `Modules/Human/Entities/TpProduct.php`
- Create: `Modules/Human/Entities/TpProductUnit.php`

- [ ] **Step 1: Tạo TpProduct**

```php
<?php
// Modules/Human/Entities/TpProduct.php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class TpProduct extends Model
{
    protected $table = 'products';
    protected $connection = 'mysql2';

    public function __construct(array $attributes = [])
    {
        $this->table = env('DB_DATABASE_SECOND') . '.' . $this->table;
        parent::__construct($attributes);
    }

    public function brand()
    {
        return $this->belongsTo(TpBrand::class, 'brand_id');
    }

    public function model()
    {
        return $this->belongsTo(TpModel::class, 'model_id');
    }

    public function origin()
    {
        return $this->belongsTo(TpOrigin::class, 'origin_id');
    }

    public function baseUnit()
    {
        return $this->hasOne(TpProductUnit::class, 'product_id')->where('is_base', 1);
    }
}
```

- [ ] **Step 2: Tạo TpProductUnit**

```php
<?php
// Modules/Human/Entities/TpProductUnit.php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class TpProductUnit extends Model
{
    protected $table = 'product_units';
    protected $connection = 'mysql2';

    public function __construct(array $attributes = [])
    {
        $this->table = env('DB_DATABASE_SECOND') . '.' . $this->table;
        parent::__construct($attributes);
    }

    public function unit()
    {
        return $this->belongsTo(TpUnit::class, 'unit_id');
    }

    public function product()
    {
        return $this->belongsTo(TpProduct::class, 'product_id');
    }
}
```

---

## Task 4: Cập nhật Entity — BomList + BomListProduct

**Files:**
- Modify: `Modules/Assign/Entities/BomList.php`
- Modify: `Modules/Assign/Entities/BomListProduct.php`

- [ ] **Step 1: Thêm relationship groups() vào BomList.php**

Thêm sau method `products()` (khoảng dòng 68):

```php
public function groups()
{
    return $this->hasMany(BomListGroup::class, 'bom_list_id')->orderBy('sort_order');
}
```

Thêm use statement ở đầu file:
```php
use Modules\Assign\Entities\BomListGroup;
```

- [ ] **Step 2: Thêm relationships vào BomListProduct.php**

Thêm use statement:
```php
use Modules\Human\Entities\TpProduct;
```

Thêm 2 method mới:
```php
public function erpProduct()
{
    return $this->belongsTo(TpProduct::class, 'erp_product_id');
}

public function group()
{
    return $this->belongsTo(BomListGroup::class, 'bom_list_group_id');
}
```

---

## Task 5: API endpoint — searchErpProducts

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/BomListController.php`
- Modify: `Modules/Assign/Routes/api.php`

- [ ] **Step 1: Thêm method searchErpProducts vào BomListController**

Thêm use statements:
```php
use Modules\Human\Entities\TpProduct;
```

Thêm method:
```php
public function searchErpProducts(Request $request)
{
    $query = TpProduct::with(['brand', 'model', 'origin', 'baseUnit.unit'])
        ->where('status', 1);

    if ($request->keyword) {
        $escaped = escapeLikeKeyword($request->keyword);
        $query->where(function ($q) use ($escaped) {
            $q->where('name', 'like', '%' . $escaped . '%')
              ->orWhere('code', 'like', '%' . $escaped . '%');
        });
    }

    $products = $query->orderBy('name')->limit(50)->get();

    $result = $products->map(function ($p) {
        return [
            'erp_product_id' => $p->id,
            'code' => $p->code,
            'name' => $p->name,
            'model_id' => $p->model_id,
            'model_name' => $p->model ? $p->model->name : null,
            'brand_id' => $p->brand_id,
            'brand_name' => $p->brand ? $p->brand->name : null,
            'origin_id' => $p->origin_id,
            'origin_name' => $p->origin ? $p->origin->name : null,
            'unit_id' => $p->baseUnit ? $p->baseUnit->unit_id : null,
            'unit_name' => ($p->baseUnit && $p->baseUnit->unit) ? $p->baseUnit->unit->name : null,
            'product_attributes' => $p->product_attributes,
            'source' => 'ERP',
        ];
    });

    return response()->json(['data' => $result]);
}
```

- [ ] **Step 2: Thêm method searchBomProducts vào BomListController**

```php
public function searchBomProducts(Request $request, BomList $bomList)
{
    $query = $bomList->products()
        ->with(['tpModel', 'tpBrand', 'tpOrigin', 'tpUnit'])
        ->whereNull('parent_id');

    if ($request->keyword) {
        $escaped = escapeLikeKeyword($request->keyword);
        $query->where(function ($q) use ($escaped) {
            $q->where('name', 'like', '%' . $escaped . '%')
              ->orWhere('code', 'like', '%' . $escaped . '%');
        });
    }

    $products = $query->orderBy('name')->limit(50)->get();

    $result = $products->map(function ($p) {
        return [
            'id' => $p->id,
            'code' => $p->code,
            'name' => $p->name,
            'model_id' => $p->model_id,
            'model_name' => $p->tpModel ? $p->tpModel->name : null,
            'brand_id' => $p->brand_id,
            'brand_name' => $p->tpBrand ? $p->tpBrand->name : null,
            'origin_id' => $p->origin_id,
            'origin_name' => $p->tpOrigin ? $p->tpOrigin->name : null,
            'unit_id' => $p->unit_id,
            'unit_name' => $p->tpUnit ? $p->tpUnit->name : null,
            'product_attributes' => $p->product_attributes,
            'source' => 'BOM',
        ];
    });

    return response()->json(['data' => $result]);
}
```

- [ ] **Step 3: Thêm routes**

Thêm vào group `/assign/bom-lists` trong `Routes/api.php`, **trước** route `/{bomList}`:

```php
Route::get('/erp-products', [BomListController::class, 'searchErpProducts']);
Route::get('/{bomList}/bom-products', [BomListController::class, 'searchBomProducts']);
```

---

## Task 6: Cập nhật BomListService — syncGroups + syncErpFields

**Files:**
- Modify: `Modules/Assign/Services/BomListService.php`

- [ ] **Step 1: Thêm use statements**

```php
use Modules\Assign\Entities\BomListGroup;
use Modules\Human\Entities\TpProduct;
use Modules\Human\Entities\TpProductUnit;
```

- [ ] **Step 2: Thêm method syncGroups()**

```php
private function syncGroups(BomList $bomList, array $groups = [])
{
    // Xoá groups cũ
    $bomList->groups()->delete();

    $groupMap = []; // client_group_id => db_group_id

    foreach ($groups as $index => $group) {
        $groupName = $group['name'] ?? null;
        if (!$groupName) continue;

        $dbGroup = $bomList->groups()->create([
            'name' => $groupName,
            'sort_order' => $index,
        ]);

        // Map theo index hoặc client-side id
        $clientId = $group['id'] ?? $group['client_id'] ?? $index;
        $groupMap[$clientId] = $dbGroup->id;
    }

    return $groupMap;
}
```

- [ ] **Step 3: Thêm method syncErpFields()**

```php
private function syncErpFields(BomList $bomList)
{
    $erpProducts = $bomList->products()->whereNotNull('erp_product_id')->get();

    foreach ($erpProducts as $bomProduct) {
        $erpProduct = TpProduct::with(['brand', 'model', 'origin', 'baseUnit'])
            ->find($bomProduct->erp_product_id);

        if (!$erpProduct) continue;

        $bomProduct->update([
            'name' => $erpProduct->name,
            'code' => $erpProduct->code,
            'model_id' => $erpProduct->model_id,
            'brand_id' => $erpProduct->brand_id,
            'origin_id' => $erpProduct->origin_id,
            'product_attributes' => $erpProduct->product_attributes,
            'unit_id' => $erpProduct->baseUnit ? $erpProduct->baseUnit->unit_id : $bomProduct->unit_id,
        ]);
    }
}
```

- [ ] **Step 4: Thêm method validateUniqueAggregate()**

```php
private function validateUniqueAggregate(Request $request, $excludeId = null)
{
    $type = $this->normalizeBomListType($request->input('bom_list_type'));
    if ($type !== BomList::TYPE_AGGREGATE) {
        return null; // không phải tổng hợp, skip
    }

    $query = BomList::where('bom_list_type', BomList::TYPE_AGGREGATE)
        ->where('solution_id', $request->input('solution_id'));

    if ($request->input('solution_module_id')) {
        $query->where('solution_module_id', $request->input('solution_module_id'));
    } else {
        $query->whereNull('solution_module_id');
    }

    if ($excludeId) {
        $query->where('id', '!=', $excludeId);
    }

    $existing = $query->first();
    if ($existing) {
        $moduleName = $request->input('solution_module_id') ? ' / Hạng mục' : '';
        return 'Giải pháp' . $moduleName . ' đã có BOM tổng hợp: ' . $existing->name . ' (' . $existing->code . ')';
    }

    return null;
}
```

---

## Task 7: Cập nhật BomListService — store() + update() + syncProducts() + loadDetail()

**Files:**
- Modify: `Modules/Assign/Services/BomListService.php`

- [ ] **Step 1: Cập nhật store()**

Thêm validate trước khi tạo BOM, sau dòng `$data['status'] = ...` (dòng ~120):

```php
// Validate unique BOM tổng hợp
$aggregateError = $this->validateUniqueAggregate($request);
if ($aggregateError) {
    return ['success' => false, 'message' => $aggregateError];
}
```

Thêm syncGroups sau syncSubBomRelations, thay đổi syncProducts để truyền groupMap:

```php
$bomList->fill($data);
$bomList->save();

$this->syncVersionFields($bomList);
$this->syncSubBomRelations($bomList, $request->input('sub_bom_list_ids', []));

// Sync groups trước products
$groupMap = $this->syncGroups($bomList, $request->input('bom_groups', []));
$this->syncProducts($bomList, $request->input('groups', []), $groupMap);

// Đồng bộ ERP fields
$this->syncErpFields($bomList);

return $this->loadDetail($bomList);
```

- [ ] **Step 2: Cập nhật update()**

Tương tự store(), thêm validate + syncGroups:

```php
// Validate unique BOM tổng hợp
$aggregateError = $this->validateUniqueAggregate($request, $bomList->id);
if ($aggregateError) {
    return ['success' => false, 'message' => $aggregateError];
}
```

Sau dòng `$bomList->products()->delete()`, thêm:
```php
$bomList->groups()->delete();
```

Và thay phần sync:
```php
$this->syncSubBomRelations($bomList, $request->input('sub_bom_list_ids', []));

$groupMap = $this->syncGroups($bomList, $request->input('bom_groups', []));
$this->syncProducts($bomList, $request->input('groups', []), $groupMap);

$this->syncErpFields($bomList);

return $this->loadDetail($bomList);
```

- [ ] **Step 3: Cập nhật syncProducts() — thêm groupMap + erp_product_id**

Thay thế toàn bộ method `syncProducts()`:

```php
private function syncProducts(BomList $bomList, array $groups = [], array $groupMap = [])
{
    foreach ($groups as $group) {
        $parent = $group['parent'] ?? null;
        if (!$parent || !is_array($parent)) {
            continue;
        }

        $payload = $this->mapProductPayload($parent, null);

        // Gán group_id từ groupMap
        $clientGroupId = $group['group_id'] ?? ($parent['group_id'] ?? null);
        if ($clientGroupId !== null && isset($groupMap[$clientGroupId])) {
            $payload['bom_list_group_id'] = $groupMap[$clientGroupId];
        }

        // Gán erp_product_id nếu có
        if (isset($parent['erp_product_id']) && $parent['erp_product_id']) {
            $payload['erp_product_id'] = (int) $parent['erp_product_id'];
        }

        $parentRow = $bomList->products()->create($payload);

        $children = $group['children'] ?? [];
        foreach ($children as $child) {
            if (!is_array($child)) {
                continue;
            }

            $childPayload = $this->mapProductPayload($child, $parentRow->id);

            if ($clientGroupId !== null && isset($groupMap[$clientGroupId])) {
                $childPayload['bom_list_group_id'] = $groupMap[$clientGroupId];
            }

            if (isset($child['erp_product_id']) && $child['erp_product_id']) {
                $childPayload['erp_product_id'] = (int) $child['erp_product_id'];
            }

            $bomList->products()->create($childPayload);
        }
    }
}
```

- [ ] **Step 4: Cập nhật loadDetail() — eager load groups**

```php
public function loadDetail(BomList $bomList)
{
    return $bomList->load([
        'products.tpModel',
        'products.tpBrand',
        'products.tpOrigin',
        'products.tpUnit',
        'groups',
        'childRelations',
        'employee_create.info',
    ]);
}
```

---

## Task 8: Cập nhật BomListController — handle validate response

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/BomListController.php`

- [ ] **Step 1: Cập nhật store() để handle validate error**

Trong method `store()`, sau gọi service, check response:

```php
public function store(BomListStoreRequest $request)
{
    return DB::transaction(function () use ($request) {
        $request->merge(['created_by' => auth()->user()->id]);
        $result = $this->service->store($request);

        // Handle validate error từ service
        if (is_array($result) && isset($result['success']) && $result['success'] === false) {
            return response()->json(['message' => $result['message']], 422);
        }

        return response()->json(['data' => $result, 'message' => 'Tạo BOM List thành công'], 201);
    });
}
```

- [ ] **Step 2: Tương tự cho update()**

```php
public function update(BomListStoreRequest $request, BomList $bomList)
{
    return DB::transaction(function () use ($request, $bomList) {
        $request->merge(['updated_by' => auth()->user()->id]);
        $result = $this->service->update($request, $bomList);

        if ($result === null) {
            return response()->json(['message' => 'Không thể sửa BOM List ở trạng thái này'], 403);
        }

        if (is_array($result) && isset($result['success']) && $result['success'] === false) {
            return response()->json(['message' => $result['message']], 422);
        }

        return response()->json(['data' => $result, 'message' => 'Cập nhật BOM List thành công']);
    });
}
```

---

## Task 9: Cập nhật BomListStoreRequest — thêm rules cho bom_groups

**Files:**
- Modify: `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php`

- [ ] **Step 1: Thêm rules**

```php
public function rules()
{
    $bomListId = $this->route('bomList') ? $this->route('bomList')->id : null;

    return [
        'name' => 'required|string|max:255|unique:bom_lists,name,' . $bomListId,
        'prospective_project_id' => 'required|integer',
        'solution_id' => 'required|integer',
        'solution_module_id' => 'nullable|integer',
        'customer_id' => 'required|integer',
        'note' => 'nullable|string',
        'bom_list_type' => 'required',
        'groups' => 'required|array|min:1',
        'sub_bom_list_ids' => 'nullable|array',
        'bom_groups' => 'nullable|array',
        'bom_groups.*.name' => 'required_with:bom_groups|string|max:255',
    ];
}
```

---

## Task 10: FE — BomBuilderAddProductModal.vue (Tab 1: Tìm hàng có sẵn)

**Files:**
- Create: `pages/assign/bom-list/components/BomBuilderAddProductModal.vue`

- [ ] **Step 1: Tạo component với 2 tab**

```vue
<template>
  <b-modal
    :visible="show"
    size="xl"
    title="Thêm hàng hoá"
    hide-footer
    @hide="$emit('close')"
  >
    <b-tabs v-model="activeTab" content-class="mt-3">
      <!-- Tab 1: Tìm hàng có sẵn -->
      <b-tab title="Tìm hàng hoá có sẵn">
        <div class="mb-3">
          <b-input-group>
            <b-form-input
              v-model="keyword"
              placeholder="Tìm theo mã hoặc tên hàng hoá..."
              @input="debounceSearch"
            />
          </b-input-group>
        </div>

        <div class="table-responsive" style="max-height: 400px; overflow-y: auto">
          <table class="table table-bordered table-hover table-sm mb-0">
            <thead class="thead-light">
              <tr>
                <th style="width: 40px"><b-form-checkbox v-model="selectAll" @change="toggleSelectAll" /></th>
                <th>Mã</th>
                <th>Tên hàng hoá</th>
                <th>Model</th>
                <th>Thương hiệu</th>
                <th>Xuất xứ</th>
                <th>ĐVT</th>
                <th style="width: 100px">Số lượng</th>
                <th style="width: 80px">Nguồn</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in mergedProducts" :key="item._uid" :class="{ 'table-active': item.selected }">
                <td><b-form-checkbox v-model="item.selected" /></td>
                <td>{{ item.code }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.model_name }}</td>
                <td>{{ item.brand_name }}</td>
                <td>{{ item.origin_name }}</td>
                <td>{{ item.unit_name }}</td>
                <td>
                  <b-form-input
                    v-model.number="item.qty"
                    type="number"
                    size="sm"
                    min="0"
                    :disabled="!item.selected"
                  />
                </td>
                <td>
                  <b-badge :variant="item.source === 'ERP' ? 'primary' : 'success'">
                    {{ item.source }}
                  </b-badge>
                </td>
              </tr>
              <tr v-if="mergedProducts.length === 0">
                <td colspan="9" class="text-center text-muted py-3">
                  {{ loading ? 'Đang tìm...' : 'Không tìm thấy hàng hoá' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-end mt-3">
          <b-button variant="secondary" class="mr-2" @click="$emit('close')">Đóng</b-button>
          <b-button variant="primary" :disabled="selectedCount === 0" @click="applySelection">
            Thêm {{ selectedCount }} hàng hoá
          </b-button>
        </div>
      </b-tab>

      <!-- Tab 2: Tạo mới -->
      <b-tab title="Tạo mới hàng hoá">
        <div class="row">
          <div class="col-md-6">
            <b-form-group label="Tên hàng hoá *">
              <b-form-input v-model="newProduct.name" />
            </b-form-group>
          </div>
          <div class="col-md-6">
            <b-form-group label="Mã hàng hoá">
              <b-form-input v-model="newProduct.code" placeholder="Tự sinh nếu để trống" />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Model *">
              <v-select
                v-model="newProduct.model_id"
                :options="modelOptions"
                :reduce="o => o.id"
                label="name"
                placeholder="Chọn model"
              />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Thương hiệu">
              <v-select
                v-model="newProduct.brand_id"
                :options="brandOptions"
                :reduce="o => o.id"
                label="name"
                placeholder="Chọn thương hiệu"
              />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Xuất xứ">
              <v-select
                v-model="newProduct.origin_id"
                :options="originOptions"
                :reduce="o => o.id"
                label="name"
                placeholder="Chọn xuất xứ"
              />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Đơn vị tính *">
              <v-select
                v-model="newProduct.unit_id"
                :options="unitOptions"
                :reduce="o => o.id"
                label="name"
                placeholder="Chọn ĐVT"
              />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Số lượng">
              <b-form-input v-model.number="newProduct.qty" type="number" min="0" />
            </b-form-group>
          </div>
          <div class="col-md-4">
            <b-form-group label="Đơn giá báo giá">
              <b-form-input v-model.number="newProduct.quoted_price" type="number" min="0" />
            </b-form-group>
          </div>
          <div class="col-md-12">
            <b-form-group label="Thông số kỹ thuật">
              <b-form-textarea v-model="newProduct.product_attributes" rows="2" />
            </b-form-group>
          </div>
        </div>
        <div class="d-flex justify-content-end mt-3">
          <b-button variant="secondary" class="mr-2" @click="$emit('close')">Đóng</b-button>
          <b-button variant="primary" @click="createProduct">Tạo hàng hoá</b-button>
        </div>
      </b-tab>
    </b-tabs>
  </b-modal>
</template>

<script>
let searchTimer = null

export default {
  name: 'BomBuilderAddProductModal',
  props: {
    show: { type: Boolean, default: false },
    bomListId: { type: [Number, String], default: null },
    modelOptions: { type: Array, default: () => [] },
    brandOptions: { type: Array, default: () => [] },
    originOptions: { type: Array, default: () => [] },
    unitOptions: { type: Array, default: () => [] },
    parentRowId: { type: [String, Number], default: null },
    targetGroupId: { type: [String, Number], default: null },
  },
  data() {
    return {
      activeTab: 0,
      keyword: '',
      loading: false,
      erpProducts: [],
      bomProducts: [],
      selectAll: false,
      newProduct: this.getEmptyProduct(),
    }
  },
  computed: {
    mergedProducts() {
      const erp = this.erpProducts.map((p, i) => ({
        ...p,
        _uid: 'erp_' + (p.erp_product_id || i),
        selected: p.selected || false,
        qty: p.qty || 1,
      }))
      const bom = this.bomProducts.map((p, i) => ({
        ...p,
        _uid: 'bom_' + (p.id || i),
        selected: p.selected || false,
        qty: p.qty || 1,
      }))
      return [...erp, ...bom]
    },
    selectedItems() {
      return this.mergedProducts.filter(p => p.selected)
    },
    selectedCount() {
      return this.selectedItems.length
    },
  },
  watch: {
    show(val) {
      if (val) {
        this.keyword = ''
        this.activeTab = 0
        this.newProduct = this.getEmptyProduct()
        this.searchProducts()
      }
    },
  },
  methods: {
    getEmptyProduct() {
      return {
        name: '',
        code: '',
        model_id: null,
        brand_id: null,
        origin_id: null,
        unit_id: null,
        qty: 1,
        quoted_price: 0,
        product_attributes: '',
      }
    },
    debounceSearch() {
      clearTimeout(searchTimer)
      searchTimer = setTimeout(() => this.searchProducts(), 300)
    },
    async searchProducts() {
      this.loading = true
      try {
        const params = { keyword: this.keyword }
        const [erpRes, bomRes] = await Promise.all([
          this.$axios.$get('/assign/bom-lists/erp-products', { params }),
          this.bomListId
            ? this.$axios.$get(`/assign/bom-lists/${this.bomListId}/bom-products`, { params })
            : { data: [] },
        ])
        this.erpProducts = (erpRes.data || []).map(p => ({ ...p, selected: false, qty: 1 }))
        this.bomProducts = (bomRes.data || []).map(p => ({ ...p, selected: false, qty: 1 }))
      } catch (e) {
        console.error('Search products error:', e)
      } finally {
        this.loading = false
      }
    },
    toggleSelectAll(checked) {
      this.erpProducts.forEach(p => { p.selected = checked })
      this.bomProducts.forEach(p => { p.selected = checked })
    },
    applySelection() {
      const items = this.selectedItems.map(item => ({
        erp_product_id: item.erp_product_id || null,
        code: item.code,
        name: item.name,
        model_id: item.model_id,
        model_name: item.model_name,
        brand_id: item.brand_id,
        brand_name: item.brand_name,
        origin_id: item.origin_id,
        origin_name: item.origin_name,
        unit_id: item.unit_id,
        unit_name: item.unit_name,
        product_attributes: item.product_attributes,
        qty: item.qty || 1,
        source: item.source,
      }))
      this.$emit('apply', items, this.parentRowId, this.targetGroupId)
      this.$emit('close')
    },
    createProduct() {
      const p = this.newProduct
      if (!p.name) {
        this.$bvToast.toast('Tên hàng hoá là bắt buộc', { variant: 'danger' })
        return
      }
      if (!p.unit_id) {
        this.$bvToast.toast('Đơn vị tính là bắt buộc', { variant: 'danger' })
        return
      }

      const modelOpt = this.modelOptions.find(o => o.id === p.model_id)
      const brandOpt = this.brandOptions.find(o => o.id === p.brand_id)
      const originOpt = this.originOptions.find(o => o.id === p.origin_id)
      const unitOpt = this.unitOptions.find(o => o.id === p.unit_id)

      const item = {
        erp_product_id: null,
        code: p.code || '',
        name: p.name,
        model_id: p.model_id,
        model_name: modelOpt ? modelOpt.name : '',
        brand_id: p.brand_id,
        brand_name: brandOpt ? brandOpt.name : '',
        origin_id: p.origin_id,
        origin_name: originOpt ? originOpt.name : '',
        unit_id: p.unit_id,
        unit_name: unitOpt ? unitOpt.name : '',
        product_attributes: p.product_attributes,
        qty: p.qty || 1,
        quoted_price: p.quoted_price || 0,
        source: 'NEW',
      }
      this.$emit('apply', [item], this.parentRowId, this.targetGroupId)
      this.$emit('close')
    },
  },
}
</script>
```

---

## Task 11: FE — Cập nhật BomBuilderTableCard.vue (Thêm cấp nhóm)

**Files:**
- Modify: `pages/assign/bom-list/components/BomBuilderTableCard.vue`

- [ ] **Step 1: Thêm prop bomGroups và events**

Thêm props:
```javascript
bomGroups: { type: Array, default: () => [] },
```

Thêm vào emits: `'add-group', 'edit-group', 'remove-group', 'reorder-group'`

- [ ] **Step 2: Thêm button "Tạo nhóm" ở header cột STT**

Trong header của cột STT, thêm button:
```html
<th class="sticky-col-b" :class="{ 'sticky-col-b--vo': viewOnly }">
  STT
  <b-button
    v-if="!viewOnly"
    variant="outline-primary"
    size="sm"
    class="ml-1 py-0 px-1"
    title="Tạo nhóm hàng"
    @click="$emit('add-group')"
  >
    <i class="fas fa-layer-group" />
  </b-button>
</th>
```

- [ ] **Step 3: Render row nhóm trước mỗi group products**

Trong tbody, render theo bomGroups. Mỗi group có 1 row header:

```html
<template v-for="(bomGroup, gIndex) in bomGroups">
  <!-- Group header row -->
  <tr :key="'group-' + bomGroup.id" class="bom-group-row">
    <td v-if="!viewOnly" class="sticky-col-a text-center">
      <b-button size="sm" variant="outline-danger" class="py-0 px-1" @click="$emit('remove-group', gIndex)">
        <i class="fas fa-trash" />
      </b-button>
      <b-button size="sm" variant="outline-secondary" class="py-0 px-1 ml-1" @click="$emit('edit-group', gIndex)">
        <i class="fas fa-edit" />
      </b-button>
    </td>
    <td class="sticky-col-b font-weight-bold" :class="{ 'sticky-col-b--vo': viewOnly }">
      {{ toRoman(gIndex + 1) }}
    </td>
    <td :colspan="visibleColumnCount" class="sticky-col-c font-weight-bold" :class="{ 'sticky-col-c--vo': viewOnly }">
      {{ bomGroup.name }}
    </td>
  </tr>

  <!-- Products belonging to this group -->
  <template v-for="(group, pIndex) in getGroupProducts(gIndex)">
    <!-- existing parent + children rendering, nhưng dùng pIndex cho STT -->
  </template>
</template>
```

- [ ] **Step 4: Thêm method toRoman() và getGroupProducts()**

```javascript
methods: {
  toRoman(num) {
    const roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
                   'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX']
    return roman[num] || num
  },
  getGroupProducts(groupIndex) {
    const groupId = this.bomGroups[groupIndex]?.id || this.bomGroups[groupIndex]?.client_id
    return this.groups.filter(g => g.group_id === groupId)
  },
}
```

- [ ] **Step 5: Thêm CSS cho group row**

```css
.bom-group-row {
  background-color: #e3f2fd !important;
}
.bom-group-row td {
  font-weight: bold;
  font-size: 14px;
  padding: 8px 12px;
  border-bottom: 2px solid #90caf9;
}
```

---

## Task 12: FE — Cập nhật BomBuilderEditor.vue (Data structure + logic)

**Files:**
- Modify: `pages/assign/bom-list/components/BomBuilderEditor.vue`

- [ ] **Step 1: Thêm data fields**

Trong `data()`, thêm:
```javascript
bomGroups: [],        // [{ id, client_id, name, sort_order }]
nextGroupClientId: 1, // auto-increment cho client-side ID
showAddProductModal: false,
addProductParentRowId: null,
addProductTargetGroupId: null,
```

- [ ] **Step 2: Thêm group_id vào mỗi group trong groups[]**

Khi tạo group item mới (trong applyPickSelection, saveQuickGoods, etc.), thêm `group_id`:
```javascript
// Mỗi group item trong groups[] có thêm:
{ parent: {...}, children: [...], expanded: true, group_id: targetGroupId }
```

- [ ] **Step 3: Thêm methods quản lý nhóm**

```javascript
addGroup() {
  this.$bvModal.msgBoxConfirm('Nhập tên nhóm hàng:', {
    // Hoặc dùng prompt
  })
  // Đơn giản hơn: dùng window.prompt tạm, sau refactor thành modal
  const name = window.prompt('Nhập tên nhóm hàng:')
  if (!name) return
  const clientId = 'g_' + this.nextGroupClientId++
  this.bomGroups.push({
    client_id: clientId,
    name: name,
    sort_order: this.bomGroups.length,
  })
},
editGroup(gIndex) {
  const name = window.prompt('Sửa tên nhóm:', this.bomGroups[gIndex].name)
  if (!name) return
  this.$set(this.bomGroups, gIndex, { ...this.bomGroups[gIndex], name })
},
removeGroup(gIndex) {
  const groupId = this.bomGroups[gIndex].id || this.bomGroups[gIndex].client_id
  // Xoá products thuộc group này
  this.groups = this.groups.filter(g => g.group_id !== groupId)
  this.bomGroups.splice(gIndex, 1)
  this.refreshParentTotals()
},
```

- [ ] **Step 4: Cập nhật openPickModal → openAddProductModal**

Thay thế tất cả gọi `openPickModal(parentRowId)` bằng:
```javascript
openAddProductModal(parentRowId, groupId) {
  this.addProductParentRowId = parentRowId || null
  this.addProductTargetGroupId = groupId || null
  this.showAddProductModal = true
},
```

- [ ] **Step 5: Thêm method handleAddProductApply()**

```javascript
handleAddProductApply(items, parentRowId, targetGroupId) {
  items.forEach(item => {
    const rowId = 'r_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5)
    const newRow = {
      rowId,
      sourceId: null,
      erpProductId: item.erp_product_id || null,
      code: item.code || '',
      name: item.name,
      model: item.model_name || '',
      modelId: item.model_id,
      brand: item.brand_name || '',
      brandId: item.brand_id,
      origin: item.origin_name || '',
      originId: item.origin_id,
      uom: item.unit_name || '',
      unitId: item.unit_id,
      specification: item.product_attributes || '',
      qty: item.qty || 1,
      estimatedPrice: 0,
      salePrice: item.quoted_price || 0,
      displayNo: '',
    }

    if (parentRowId) {
      // Thêm làm con
      const groupIdx = this.groups.findIndex(g => g.parent.rowId === parentRowId)
      if (groupIdx >= 0) {
        this.groups[groupIdx].children.push(newRow)
      }
    } else {
      // Thêm làm cha
      this.groups.push({
        parent: newRow,
        children: [],
        expanded: true,
        group_id: targetGroupId,
      })
    }
  })
  this.refreshParentTotals()
},
```

- [ ] **Step 6: Cập nhật recalculateDisplayNumbers() — STT reset mỗi nhóm**

```javascript
recalculateDisplayNumbers() {
  if (this.bomGroups.length > 0) {
    // Có nhóm: STT reset mỗi nhóm
    this.bomGroups.forEach(bomGroup => {
      const groupId = bomGroup.id || bomGroup.client_id
      const groupProducts = this.groups.filter(g => g.group_id === groupId)
      let parentNo = 0
      groupProducts.forEach(g => {
        parentNo++
        g.parent.displayNo = String(parentNo)
        g.children.forEach((child, cIndex) => {
          child.displayNo = parentNo + '.' + (cIndex + 1)
        })
      })
    })
  } else {
    // Không có nhóm: STT liên tục (logic cũ)
    let parentNo = 0
    this.groups.forEach(g => {
      parentNo++
      g.parent.displayNo = String(parentNo)
      g.children.forEach((child, cIndex) => {
        child.displayNo = parentNo + '.' + (cIndex + 1)
      })
    })
  }
},
```

- [ ] **Step 7: Cập nhật buildSavePayload() — thêm bom_groups + erp_product_id**

Thêm `bom_groups` vào payload:
```javascript
buildSavePayload(status) {
  const payload = {
    name: this.bomForm.name,
    prospective_project_id: this.bomForm.prospective_project_id,
    solution_id: this.bomForm.solution_id,
    solution_module_id: this.bomForm.solution_module_id || null,
    customer_id: this.bomForm.customer_id,
    note: this.bomForm.note,
    bom_list_type: this.bomForm.bom_list_type,
    status: status,
    sub_bom_list_ids: this.selectedSubBomIds,
    bom_groups: this.bomGroups.map((g, i) => ({
      id: g.id || null,
      client_id: g.client_id || null,
      name: g.name,
      sort_order: i,
    })),
    groups: this.groups.map(g => ({
      group_id: g.group_id || null,
      parent: this.mapGroupRowForSave(g.parent),
      children: g.children.map(c => this.mapGroupRowForSave(c)),
    })),
  }
  return payload
},
```

Cập nhật `mapGroupRowForSave()` — thêm erp_product_id:
```javascript
mapGroupRowForSave(row) {
  return {
    product_project_id: row.sourceId || null,
    erp_product_id: row.erpProductId || null,
    name: row.name,
    code: row.code,
    model_id: row.modelId || null,
    brand_id: row.brandId || null,
    origin_id: row.originId || null,
    unit_id: row.unitId || null,
    qty_needed: row.qty || 0,
    product_attributes: row.specification || '',
    estimated_price: row.estimatedPrice || 0,
    quoted_price: row.salePrice || 0,
  }
},
```

- [ ] **Step 8: Cập nhật loadBomDetail() — load groups từ API**

Trong method load detail, sau khi nhận response, thêm:
```javascript
// Load groups
if (data.groups && data.groups.length > 0) {
  this.bomGroups = data.groups.map(g => ({
    id: g.id,
    client_id: 'g_' + g.id,
    name: g.name,
    sort_order: g.sort_order,
  }))
  this.nextGroupClientId = data.groups.length + 1
}

// Gán group_id cho mỗi product group
// (khi map products thành groups[], set group_id = product.bom_list_group_id)
```

Trong hàm map products → groups, thêm `group_id`:
```javascript
// Khi tạo group item từ API product:
{
  parent: mapProductToRow(parentProduct),
  children: childProducts.map(c => mapProductToRow(c)),
  expanded: true,
  group_id: parentProduct.bom_list_group_id
    ? ('g_' + parentProduct.bom_list_group_id)
    : null,
}
```

---

## Task 13: FE — Cập nhật BomBuilderSubBomModal.vue (Filter)

**Files:**
- Modify: `pages/assign/bom-list/components/BomBuilderSubBomModal.vue`

- [ ] **Step 1: Cập nhật filteredSubBoms computed**

Filter thêm: exclude status nháp (status=1):

```javascript
filteredSubBoms() {
  return this.subBoms.filter(bom => {
    if (bom.bom_list_type !== 1 && bom.bom_list_type !== 'component') return false
    if (bom.status === 1) return false // Exclude nháp
    if (this.solutionId && bom.solution_id !== this.solutionId) return false
    if (this.solutionModuleId && bom.solution_module_id !== this.solutionModuleId) return false
    if (this.currentBomId && bom.id === this.currentBomId) return false
    return true
  })
}
```

Lưu ý: Cần đảm bảo props `solutionId`, `solutionModuleId`, `currentBomId` được truyền từ BomBuilderEditor.

---

## Task 14: FE — Kết nối template, xoá component cũ

**Files:**
- Modify: `pages/assign/bom-list/components/BomBuilderEditor.vue` (template)
- Delete: `pages/assign/bom-list/components/BomBuilderPickModal.vue`
- Delete: `pages/assign/bom-list/components/BomBuilderQuickCreateModal.vue`

- [ ] **Step 1: Import + register BomBuilderAddProductModal**

Trong BomBuilderEditor.vue:
```javascript
import BomBuilderAddProductModal from './BomBuilderAddProductModal.vue'

// Trong components:
components: {
  // ... existing
  BomBuilderAddProductModal,
},
```

- [ ] **Step 2: Thêm component vào template**

Thay thế BomBuilderPickModal + BomBuilderQuickCreateModal trong template bằng:
```html
<BomBuilderAddProductModal
  :show="showAddProductModal"
  :bom-list-id="bomId"
  :model-options="modelMasterOptions"
  :brand-options="brandMasterOptions"
  :origin-options="originMasterOptions"
  :unit-options="unitMasterOptions"
  :parent-row-id="addProductParentRowId"
  :target-group-id="addProductTargetGroupId"
  @close="showAddProductModal = false"
  @apply="handleAddProductApply"
/>
```

- [ ] **Step 3: Truyền events từ TableCard cho nhóm**

```html
<BomBuilderTableCard
  ...existing-props
  :bom-groups="bomGroups"
  @add-group="addGroup"
  @edit-group="editGroup"
  @remove-group="removeGroup"
  @open-pick="openAddProductModal"
  ...
/>
```

- [ ] **Step 4: Xoá import component cũ**

Xoá import BomBuilderPickModal và BomBuilderQuickCreateModal, xoá khỏi `components: {}`.

- [ ] **Step 5: Xoá file component cũ**

```bash
rm pages/assign/bom-list/components/BomBuilderPickModal.vue
rm pages/assign/bom-list/components/BomBuilderQuickCreateModal.vue
```

---

## Task 15: Test thủ công toàn bộ

- [ ] Tạo BOM mới → thêm nhóm hàng → thêm hàng từ ERP → thêm hàng tạo mới → lưu
- [ ] Mở edit BOM vừa tạo → verify groups + products load đúng
- [ ] Tạo BOM tổng hợp → verify validate unique (tạo thêm 1 BOM tổng hợp cùng giải pháp → phải lỗi)
- [ ] SubBom modal → verify chỉ hiện BOM thành phần cùng giải pháp, không hiện nháp
- [ ] Chọn hàng ERP → lưu → verify erp_product_id được lưu + fields đồng bộ
- [ ] STT nhóm hiển thị I, II, III + STT hàng reset mỗi nhóm
- [ ] Drag-drop nhóm + hàng giữa các nhóm
- [ ] Trang chi tiết (view-only) hiển thị nhóm đúng

---

## Checkpoint log

| Task | Mô tả | Status |
|------|-------|--------|
| 1 | Migration + Entity bom_list_groups | [ ] |
| 2 | Migration erp_product_id + bom_list_group_id | [ ] |
| 3 | Model TpProduct + TpProductUnit | [ ] |
| 4 | Cập nhật Entity BomList + BomListProduct | [ ] |
| 5 | API searchErpProducts + searchBomProducts | [ ] |
| 6 | Service syncGroups + syncErpFields + validateUniqueAggregate | [ ] |
| 7 | Service store/update/syncProducts/loadDetail | [ ] |
| 8 | Controller handle validate response | [ ] |
| 9 | StoreRequest thêm rules | [ ] |
| 10 | FE AddProductModal (popup gộp 2 tab) | [ ] |
| 11 | FE TableCard (row nhóm, STT I/II/III) | [ ] |
| 12 | FE Editor (data structure, logic, save) | [ ] |
| 13 | FE SubBomModal (filter) | [ ] |
| 14 | FE kết nối + xoá component cũ | [ ] |
| 15 | Test thủ công | [ ] |
