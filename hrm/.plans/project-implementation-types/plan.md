# Phase A — KD tự triển khai + Permission xem giá vốn + Lock giá bán ERP

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép KD tự tạo báo giá từ BOM (type 1), thêm permission xem giá vốn, lock giá bán hàng ERP = giá niêm yết.

**Architecture:** 3 block: (1) API mới `create-from-bom` + FE button, (2) Permission "Xem giá vốn hàng hoá" ẩn data từ API+FE, (3) Lock quoted_price hàng ERP theo giá Bán lẻ từ `product_unit_prices` ERP DB.

**Tech Stack:** Laravel 8, Nuxt 2 (Vue 2), MySQL cross-DB (mysql2 connection), Spatie Permission

**Branch:** tpe-develop-assign  
**Spec:** docs/superpowers/specs/2026-05-24-project-implementation-types-design.md

---

## Task 1: Tạo Model TpProductUnitPrice (đọc giá niêm yết từ ERP DB)

**Files:**
- Create: `hrm-api/Modules/Human/Entities/TpProductUnitPrice.php`

- [ ] **Step 1: Tạo Model**

```php
<?php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class TpProductUnitPrice extends Model
{
    protected $table = 'product_unit_prices';
    protected $connection = 'mysql2';

    public function __construct(array $attributes = [])
    {
        $this->table = env('DB_DATABASE_SECOND') . '.' . $this->table;
        parent::__construct($attributes);
    }

    public function productUnit()
    {
        return $this->belongsTo(TpProductUnit::class, 'product_unit_id');
    }
}
```

- [ ] **Step 2: Thêm helper static lấy giá Bán lẻ theo product_id**

Thêm vào cuối class:

```php
/**
 * Lấy giá Bán lẻ (price_type_id=1) cho 1 hoặc nhiều erp_product_id.
 * Return: [erp_product_id => price]
 */
public static function getRetailPrices(array $erpProductIds): array
{
    if (empty($erpProductIds)) return [];

    $dbSecond = env('DB_DATABASE_SECOND');

    return \Illuminate\Support\Facades\DB::connection('mysql2')
        ->table("{$dbSecond}.product_unit_prices as pup")
        ->join("{$dbSecond}.product_units as pu", 'pu.id', '=', 'pup.product_unit_id')
        ->where('pu.is_base', 1)
        ->where('pup.price_type_id', 1)
        ->whereIn('pu.product_id', $erpProductIds)
        ->pluck('pup.price', 'pu.product_id')
        ->mapWithKeys(fn($price, $productId) => [(int) $productId => (float) $price])
        ->toArray();
}

/**
 * Lấy giá vốn (cost_price) cho 1 hoặc nhiều erp_product_id.
 * Return: [erp_product_id => cost_price]
 */
public static function getCostPrices(array $erpProductIds): array
{
    if (empty($erpProductIds)) return [];

    $dbSecond = env('DB_DATABASE_SECOND');

    return \Illuminate\Support\Facades\DB::connection('mysql2')
        ->table("{$dbSecond}.product_units as pu")
        ->where('pu.is_base', 1)
        ->whereIn('pu.product_id', $erpProductIds)
        ->pluck('pu.cost_price', 'pu.product_id')
        ->mapWithKeys(fn($price, $productId) => [(int) $productId => (float) $price])
        ->toArray();
}
```

- [ ] **Step 3: Verify**

```bash
cd hrm-api && php artisan tinker --execute="
use Modules\Human\Entities\TpProductUnitPrice;
\$prices = TpProductUnitPrice::getRetailPrices([3895, 3896]);
var_dump(\$prices);
"
```

Expected: array có 2 keys với giá Bán lẻ tương ứng.

---

## Task 2: Migration — Permission "Xem giá vốn hàng hoá"

**Files:**
- Create: `hrm-api/database/migrations/2026_05_24_000001_add_permission_xem_gia_von_hang_hoa.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

class AddPermissionXemGiaVonHangHoa extends Migration
{
    public function up()
    {
        $exists = DB::table('permissions')
            ->where('name', 'Xem giá vốn hàng hoá')
            ->exists();

        if (!$exists) {
            DB::table('permissions')->insert([
                'name' => 'Xem giá vốn hàng hoá',
                'guard_name' => 'web',
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }

    public function down()
    {
        DB::table('permissions')
            ->where('name', 'Xem giá vốn hàng hoá')
            ->delete();
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-api && php artisan migrate
```

---

## Task 3: BE — QuotationService::createFromBom()

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Thêm method `createFromBom`**

Thêm sau method `createFromRequest()` (sau dòng 122):

```php
/**
 * Phase A — KD tự triển khai: tạo báo giá trực tiếp từ BOM (bỏ PricingRequest).
 * Điều kiện: BOM phải AGGREGATE + Đã duyệt, dự án phải implementation_type=1.
 */
public function createFromBom(BomList $bomList): Quotation
{
    return DB::transaction(function () use ($bomList) {
        if ((int) $bomList->bom_list_type !== BomList::TYPE_AGGREGATE) {
            throw new \Exception('Chỉ tạo báo giá từ BOM tổng hợp.');
        }
        if ((int) $bomList->status !== BomList::STATUS_DA_DUYET) {
            throw new \Exception('BOM phải ở trạng thái Đã duyệt.');
        }

        $project = ProspectiveProject::findOrFail($bomList->prospective_project_id);
        if ((int) $project->implementation_type !== ProspectiveProject::IMPLEMENTATION_TYPE_SELF) {
            throw new \Exception('Chỉ dự án Tự triển khai mới được tạo báo giá trực tiếp.');
        }

        $customer = $project->customer_id ? Customer::find($project->customer_id) : null;

        $solutionVersionCode = null;
        if ($bomList->solution_version_id) {
            $sv = SolutionVersion::find($bomList->solution_version_id);
            $solutionVersionCode = $sv->code ?? null;
        }
        $moduleVersionCode = null;
        if ($bomList->solution_module_version_id) {
            $smv = SolutionModuleVersion::find($bomList->solution_module_version_id);
            $moduleVersionCode = $smv->code ?? null;
        }

        $quotation = new Quotation();
        $quotation->fill([
            'pricing_request_id' => null,
            'bom_list_id' => $bomList->id,
            'project_id' => $project->id,
            'solution_id' => $bomList->solution_id,
            'solution_version_id' => $bomList->solution_version_id,
            'solution_version_code' => $solutionVersionCode,
            'solution_module_id' => $bomList->solution_module_id,
            'solution_module_version_id' => $bomList->solution_module_version_id,
            'module_version_code' => $moduleVersionCode,
            'currency_id' => $bomList->currency_id,
            'description' => null,
            'deadline' => null,
            'delivery_time' => null,
            'warranty_time' => null,
            'payment_terms' => null,
            'validity_days' => null,
            'customer_id' => $project->customer_id,
            'customer_code' => $project->customer_code ?? ($customer->code ?? null),
            'customer_name' => $project->customer_name ?: ($customer->name ?? ''),
            'customer_tax_code' => $project->customer_tax_code ?? null,
            'customer_address' => $project->customer_address ?? null,
            'customer_email' => $project->customer_email ?? null,
            'customer_contact_name' => $project->customer_contact_name ?? null,
            'customer_contact_phone' => $project->customer_contact_phone ?? null,
            'status' => Quotation::STATUS_DANG_TAO,
        ]);
        $quotation->code = $quotation->getNextCode();
        $quotation->save();

        // Snapshot giá: hàng ERP lấy giá vốn + giá niêm yết, hàng tạm lấy từ BOM
        $bomProducts = BomListProduct::where('bom_list_id', $bomList->id)->get();
        $erpIds = $bomProducts->pluck('erp_product_id')->filter()->unique()->values()->toArray();
        $retailPrices = TpProductUnitPrice::getRetailPrices($erpIds);
        $costPrices = TpProductUnitPrice::getCostPrices($erpIds);

        $rows = [];
        $now = now();
        foreach ($bomProducts as $bp) {
            $erpId = $bp->erp_product_id ? (int) $bp->erp_product_id : null;
            if ($erpId) {
                $estimatedPrice = $costPrices[$erpId] ?? 0;
                $quotedPrice = $retailPrices[$erpId] ?? 0;
            } else {
                $estimatedPrice = (float) ($bp->estimated_price ?? 0);
                $quotedPrice = 0;
            }
            $rows[] = [
                'quotation_id' => $quotation->id,
                'bom_list_product_id' => $bp->id,
                'estimated_price' => $estimatedPrice,
                'quoted_price' => $quotedPrice,
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

        // Chuyển status dự án + solution (tương đương gửi YCXD giá)
        $project->update(['status' => ProspectiveProject::STATUS_DU_TOAN]);
        $solution = Solution::find($bomList->solution_id);
        if ($solution) {
            $solution->update(['status' => Solution::STATUS_CHO_LAM_GIA]);
        }

        $this->logHistory($quotation->id, QuotationHistory::ACTION_CREATE, null, Quotation::STATUS_DANG_TAO);

        return $quotation->fresh();
    });
}
```

- [ ] **Step 2: Thêm import ở đầu file (nếu chưa có)**

Kiểm tra đầu file đã có các import sau chưa, thêm nếu thiếu:

```php
use Modules\Human\Entities\TpProductUnitPrice;
use Modules\Assign\Entities\Customer;
use Modules\Assign\Entities\SolutionVersion;
use Modules\Assign\Entities\SolutionModuleVersion;
```

---

## Task 4: BE — Route + Controller cho createFromBom

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (dòng 367, trong group quotations)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`

- [ ] **Step 1: Thêm route**

Trong `api.php`, thêm vào group `/assign/quotations` (trước dòng `Route::get('/{id}'...`):

```php
Route::post('/create-from-bom', [QuotationController::class, 'createFromBom']);
```

Phải đặt TRƯỚC route `/{id}` để tránh conflict.

- [ ] **Step 2: Thêm method trong Controller**

Thêm vào `QuotationController.php`:

```php
public function createFromBom(Request $request)
{
    try {
        $request->validate(['bom_list_id' => 'required|integer']);
        $bomList = \Modules\Assign\Entities\BomList::findOrFail($request->bom_list_id);
        $quotation = $this->service->createFromBom($bomList);
        return $this->responseJson('Đã tạo báo giá', Response::HTTP_OK, [
            'id' => $quotation->id,
            'code' => $quotation->code,
        ]);
    } catch (\Illuminate\Validation\ValidationException $e) {
        throw $e;
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_UNPROCESSABLE_ENTITY);
    }
}
```

---

## Task 5: BE — Đổi logic `resolveCanViewImportPrice` sang permission

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php` (dòng 168-199)

- [ ] **Step 1: Đổi method `resolveCanViewImportPrice()`**

Thay thế toàn bộ method (dòng 168-199):

```php
private function resolveCanViewImportPrice(): bool
{
    return isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá');
}
```

- [ ] **Step 2: Ẩn estimated_price + profit data khi không có quyền**

Trong method `toArray()`, sau dòng `$canView = $this->resolveCanViewImportPrice()` — sửa phần map products (dòng 32-61).

Tìm block:
```php
$products = $prices->map(function ($qpp) use ($parentIdsWithChildren) {
```

Đổi thành:
```php
$canViewCostPrice = $this->resolveCanViewImportPrice();
$products = $prices->map(function ($qpp) use ($parentIdsWithChildren, $canViewCostPrice) {
```

Trong return array của closure, đổi dòng `estimated_price`:
```php
'estimated_price' => $canViewCostPrice ? $qpp->estimated_price : null,
```

- [ ] **Step 3: Ẩn estimated_price trong service_items**

Trong method `resolveServiceItems()` (dòng 201), thêm check permission:

Tìm:
```php
private function resolveServiceItems()
{
    $serviceItems = $this->serviceItems;
    if ($serviceItems->isEmpty()) return [];
```

Thêm sau `if ($serviceItems->isEmpty()) return [];`:
```php
$canViewCostPrice = isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá');
```

Trong return map, đổi dòng `estimated_price`:
```php
'estimated_price' => $canViewCostPrice ? (float) ($si->estimated_price ?? 0) : null,
```

---

## Task 6: BE — Lock giá bán hàng ERP trong upsertPrices

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` (method `upsertPrices`, dòng 361)

- [ ] **Step 1: Sửa upsertPrices — bỏ qua quoted_price hàng ERP**

Thêm logic kiểm tra `erp_product_id` trước khi update `quoted_price`. Sửa method `upsertPrices`:

Tìm (dòng 361-403):
```php
private function upsertPrices(Quotation $quotation, array $products): void
{
    // Load toàn bộ products của BOM để biết quan hệ parent/child
    $productMap = $quotation->bomList->products()->get()->keyBy('id');

    foreach ($products as $p) {
        $productId = $p['bom_list_product_id'] ?? null;
        if (!$productId) continue;

        $product = $productMap->get($productId);
        if (!$product) continue;

        $updateData = [
            'estimated_price' => $p['estimated_price'] ?? 0,
            'quoted_price' => $p['quoted_price'] ?? 0,
            'vat_percent' => $p['vat_percent'] ?? 0,
        ];
```

Thay thành:
```php
private function upsertPrices(Quotation $quotation, array $products): void
{
    $productMap = $quotation->bomList->products()->get()->keyBy('id');

    // Lấy giá niêm yết hàng ERP để enforce lock
    $erpIds = $productMap->pluck('erp_product_id')->filter()->unique()->values()->toArray();
    $retailPrices = TpProductUnitPrice::getRetailPrices($erpIds);

    foreach ($products as $p) {
        $productId = $p['bom_list_product_id'] ?? null;
        if (!$productId) continue;

        $product = $productMap->get($productId);
        if (!$product) continue;

        $isErp = !empty($product->erp_product_id);

        $updateData = [
            'vat_percent' => $p['vat_percent'] ?? 0,
        ];

        if ($isErp) {
            // Hàng ERP: lock quoted_price = giá niêm yết, giữ estimated_price snapshot
            $updateData['quoted_price'] = $retailPrices[(int) $product->erp_product_id] ?? ($p['quoted_price'] ?? 0);
        } else {
            // Hàng tạm: user toàn quyền
            $updateData['estimated_price'] = $p['estimated_price'] ?? 0;
            $updateData['quoted_price'] = $p['quoted_price'] ?? 0;
        }
```

Phần còn lại (discount fields + updateOrCreate + recomputeTotals) giữ nguyên.

- [ ] **Step 2: Thêm import TpProductUnitPrice nếu chưa có**

Đầu file `QuotationService.php`:
```php
use Modules\Human\Entities\TpProductUnitPrice;
```

---

## Task 7: BE — Ẩn profit margin trong calculateTotals khi không có quyền

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` (method `calculateTotals`, dòng 572)

- [ ] **Step 1: Thêm flag `can_view_cost_price` vào response**

Tìm return array cuối method `calculateTotals()` (dòng 629-641):

```php
return [
    'total_import' => $totalImport,
    ...
    'profit_margin_percent' => $margin,
    ...
];
```

Đổi thành:
```php
$canViewCostPrice = isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá');

return [
    'total_import' => $canViewCostPrice ? $totalImport : null,
    'total_sale' => $totalSale,
    'total_discount' => $totalDiscount,
    'total_sale_after_discount' => $totalSaleAfterDiscount,
    'total_vat' => $totalVat,
    'total_after_vat' => $totalAfterVat,
    'profit_margin_percent' => $canViewCostPrice ? $margin : null,
    'exchange_rate' => $exchangeRate,
    'currency_code' => $currencyCode,
    'total_sale_vnd' => $totalSaleAfterDiscount * $exchangeRate,
    'total_import_vnd' => $canViewCostPrice ? $totalImport * $exchangeRate : null,
    'can_view_cost_price' => $canViewCostPrice,
];
```

---

## Task 8: BE — searchErpProducts trả thêm list_price

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/BomListController.php` (method `searchErpProducts`, dòng 270)

- [ ] **Step 1: Bổ sung giá niêm yết vào response**

Tìm đoạn return map (dòng 289-305):

```php
$result = $products->map(function ($p) use ($stripLeadingQuote) {
    return [
        'erp_product_id' => $p->id,
        ...
        'source' => 'ERP',
    ];
});
```

Thêm trước đoạn map:
```php
$erpIds = $products->pluck('id')->toArray();
$retailPrices = \Modules\Human\Entities\TpProductUnitPrice::getRetailPrices($erpIds);
```

Đổi closure:
```php
$result = $products->map(function ($p) use ($stripLeadingQuote, $retailPrices) {
    return [
        'erp_product_id' => $p->id,
        'code' => $stripLeadingQuote($p->code),
        'name' => $stripLeadingQuote($p->name),
        'model_id' => $p->model_id,
        'model_name' => $stripLeadingQuote($p->tpModel ? $p->tpModel->name : null),
        'brand_id' => $p->brand_id,
        'brand_name' => $stripLeadingQuote($p->brand ? $p->brand->name : null),
        'origin_id' => $p->origin_id,
        'origin_name' => $stripLeadingQuote($p->origin ? $p->origin->name : null),
        'unit_id' => $p->baseUnit ? $p->baseUnit->unit_id : null,
        'unit_name' => $stripLeadingQuote(($p->baseUnit && $p->baseUnit->unit) ? $p->baseUnit->unit->name : null),
        'product_attributes' => $p->product_attributes,
        'list_price' => $retailPrices[(int) $p->id] ?? null,
        'source' => 'ERP',
    ];
});
```

---

## Task 9: BE — Import Excel giá: skip giá bán hàng ERP

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` (method `importPrices` — nếu có)

- [ ] **Step 1: Tìm method importPrices trong QuotationController**

File `QuotationController.php` dòng 379-380 có route `import-prices/validate` + `import-prices`.

- [ ] **Step 2: Sửa logic import — lock quoted_price hàng ERP**

Logic tương tự Task 6: khi import, nếu product có `erp_product_id` → bỏ qua giá bán từ Excel, giữ giá niêm yết.

Tìm đoạn xử lý import prices trong controller (method `importPrices`), thêm check:

```php
// Trong vòng lặp xử lý từng dòng import:
$bomProduct = $productMap->get($bomListProductId);
$isErp = $bomProduct && !empty($bomProduct->erp_product_id);

if ($isErp) {
    // Skip quoted_price từ Excel, giữ giá niêm yết
    unset($row['quoted_price']);
}
```

Cần đọc code thực tế của method `importPrices` để xác định vị trí chính xác.

---

## Task 10: BE — Export Excel báo giá: ẩn cột giá nhập + tỷ suất LN

**Files:**
- Modify: Export file báo giá (BomListExport hoặc blade template)

- [ ] **Step 1: Xác định file export**

Đã biết: `BomListExport.php` + blade `bom_list.blade.php` chứa các cột:
- "Đơn giá nhập" (estimated_price)
- "Tỷ suất LN (%)" (profit_margin)

- [ ] **Step 2: Truyền flag `can_view_cost_price` vào export**

Trong controller export, thêm:
```php
$canViewCostPrice = isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá');
```

Truyền vào export class / blade view.

- [ ] **Step 3: Trong blade, ẩn cột khi không có quyền**

```blade
@if($canViewCostPrice)
    <th>Đơn giá nhập</th>
@endif
...
@if($canViewCostPrice)
    <th>Tỷ suất LN (%)</th>
@endif
```

Tương tự cho các dòng data.

---

## Task 11: FE — Nút "Tạo báo giá" trên trang chi tiết Dự án TKT (tab Hồ sơ)

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectReviewProfilesTab.vue`

- [ ] **Step 1: Thêm nút "Tạo báo giá" bên cạnh nút YCXD giá**

Tìm (dòng 91-98):
```html
<button
    v-if="canRequestPricing(item)"
    class="btn btn-light border btn-sm"
    v-b-tooltip.hover.top="'Yêu cầu xây dựng giá'"
    @click="openPricingRequestModal(item)"
>
    <i class="ri-price-tag-3-line text-primary"></i>
</button>
```

Thêm ngay sau (trước `</span>`):
```html
<button
    v-if="canCreateQuotationDirect(item)"
    class="btn btn-light border btn-sm"
    :disabled="creatingQuotation"
    v-b-tooltip.hover.top="'Tạo báo giá'"
    @click="handleCreateQuotationFromBom(item)"
>
    <i class="ri-file-list-3-line text-success"></i>
</button>
```

- [ ] **Step 2: Thêm data + methods**

Trong `data()`:
```js
creatingQuotation: false,
```

Trong `methods`:
```js
canCreateQuotationDirect(item) {
    // Type 1 (Tự triển khai) + hồ sơ Đã duyệt + là KD phụ trách + có BOM
    return this.isSelfImplementation && this.isSaleOfProject
        && (item.status === 'approved' || item.status_name === 'Đã duyệt')
        && item.bom_list && item.bom_list.id
},
async handleCreateQuotationFromBom(item) {
    if (this.creatingQuotation) return
    if (!item.bom_list || !item.bom_list.id) {
        this.$toasted?.global?.error?.({ message: 'Hồ sơ chưa có BOM' })
        return
    }
    this.creatingQuotation = true
    try {
        const res = await this.$store.dispatch('call_api', {
            url: '/api/v1/assign/quotations/create-from-bom',
            method: 'POST',
            payload: { bom_list_id: item.bom_list.id },
        })
        if (res?.data?.id) {
            this.$toasted?.global?.success?.({ message: 'Đã tạo báo giá' })
            this.$router.push(`/assign/quotations/${res.data.id}/edit`)
        }
    } catch (e) {
        const msg = e?.response?.data?.message || 'Không thể tạo báo giá'
        this.$toasted?.global?.error?.({ message: msg })
    } finally {
        this.creatingQuotation = false
    }
},
```

- [ ] **Step 3: Thêm computed `isSelfImplementation`**

Trong `computed` (hoặc props — tuỳ cách component nhận project data):
```js
isSelfImplementation() {
    return Number(this.project?.implementation_type) === 1
},
```

Kiểm tra xem component đã nhận prop `project` hay chưa — nếu chưa thì cần truyền từ parent.

- [ ] **Step 4: Ẩn nút YCXD giá khi type=1**

Sửa `canRequestPricing`:
```js
canRequestPricing(item) {
    if (this.isSelfImplementation) return false
    const statusApproved = item.status === 'approved' || item.status_name === 'Đã duyệt'
    return this.isSaleOfProject && statusApproved
},
```

---

## Task 12: FE — Ẩn cột giá nhập + tỷ suất LN trên form sửa báo giá

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

- [ ] **Step 1: Dùng flag `can_view_cost_price` từ API**

API `calculateTotals` đã trả `can_view_cost_price` (Task 7). Cũng dùng `can_view_import_price` từ show quotation.

Trong `data()` hoặc khi load quotation:
```js
canViewCostPrice: false,
```

Khi nhận response show quotation:
```js
this.canViewCostPrice = res.data?.can_view_import_price || false
```

- [ ] **Step 2: Ẩn cột "Giá nhập" trong bảng sản phẩm**

Tìm header "Giá nhập" (dòng ~210) và các input estimated_price (dòng ~256):

Thêm `v-if="canViewCostPrice"` vào `<th>` và `<td>` tương ứng.

- [ ] **Step 3: Ẩn cột "Tỷ suất LN"**

Tìm header "Tỷ suất LN" (dòng ~224):

Thêm `v-if="canViewCostPrice"`.

- [ ] **Step 4: Ẩn dòng tỷ suất trong bảng tổng hợp giá trị**

Tìm dòng hiển thị "Tỷ suất lợi nhuận" trong summary table:

Thêm `v-if="canViewCostPrice"`.

- [ ] **Step 5: Ẩn trong service items section**

Cột "Giá nhập" của dịch vụ bổ sung (dòng ~368):

Thêm `v-if="canViewCostPrice"`.

---

## Task 13: FE — Lock giá bán hàng ERP trên form sửa báo giá

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

- [ ] **Step 1: Xác định hàng ERP vs hàng tạm**

API show quotation đã trả `erp_product_id` trong mỗi product (DetailQuotationResource dòng 59).

Tạo helper method:
```js
isErpProduct(product) {
    return product.erp_product_id != null
},
```

- [ ] **Step 2: Lock input giá bán cho hàng ERP**

Tìm input `quoted_price` cho parent product (dòng ~260-267). Thêm `:disabled`:

```html
<V2BaseCurrencyInput
    v-model="product.quoted_price"
    :disabled="isErpProduct(product)"
    ...
/>
```

- [ ] **Step 3: Lock input giá nhập cho hàng ERP (nếu hiển thị)**

```html
<V2BaseCurrencyInput
    v-if="canViewCostPrice"
    v-model="product.estimated_price"
    :disabled="isErpProduct(product)"
    ...
/>
```

- [ ] **Step 4: Hiển thị badge "ERP" hoặc "Tạm" cho từng sản phẩm (optional)**

Bên cạnh tên sản phẩm, thêm badge nhỏ để user biết:
```html
<span v-if="isErpProduct(product)" class="badge badge-info badge-sm ml-1">ERP</span>
<span v-else class="badge badge-warning badge-sm ml-1">Tạm</span>
```

---

## Task 14: FE — Ẩn cột trên trang xem báo giá (view)

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/index.vue`

- [ ] **Step 1: Tương tự Task 12 — ẩn cột giá nhập + tỷ suất LN**

Dùng `can_view_import_price` từ API response.

Thêm `v-if="canViewCostPrice"` cho:
- Cột "Giá nhập" (th + td)
- Cột "Tỷ suất LN" (th + td)
- Dòng tỷ suất trong bảng tổng hợp

---

## Task 15: FE — Ẩn cột trong popup gửi duyệt

**Files:**
- Modify: File popup gửi duyệt báo giá (trong `edit.vue` hoặc component riêng)

- [ ] **Step 1: Tìm popup gửi duyệt**

Grep "gửi duyệt" hoặc "submit" trong quotation edit/components.

- [ ] **Step 2: Ẩn tổng giá nhập + tỷ suất LN**

Thêm `v-if="canViewCostPrice"` cho các dòng hiển thị tổng giá nhập và tỷ suất LN trong popup.

---

## Task 16: FE — Ẩn cột trong in báo giá (print preview)

**Files:**
- Modify: Print preview component/modal của báo giá

- [ ] **Step 1: Tìm print preview**

Grep "print" hoặc "in báo giá" trong quotation pages.

- [ ] **Step 2: Ẩn cột giá nhập + tỷ suất LN khi không có quyền**

Tương tự Task 12.

---

### Checkpoint — 2026-05-24
Vừa hoàn thành: Tất cả 16 tasks Phase A
Đang làm dở: Không
Bước tiếp theo: Test thủ công, sau đó chuyển sang Phase B

**Verify checklist:**
- [x] KD type 1 có thể tạo báo giá trực tiếp từ BOM (không qua YCXD giá)
- [x] User không có permission "Xem giá vốn hàng hoá" → không thấy giá nhập + tỷ suất LN (cả API + FE)
- [x] Giá bán hàng ERP bị lock = giá Bán lẻ trên tất cả báo giá (type 1/2/3)
- [x] Hàng tạm vẫn sửa giá nhập + giá bán bình thường
- [x] Export Excel ẩn cột đúng theo permission
- [x] Import Excel skip giá bán hàng ERP
- [ ] Báo giá cũ (trước deploy) vẫn hoạt động bình thường (cần test thủ công)

### Checkpoint — 2026-05-24 (Session 2: Bug fix + Brainstorm Phase B)
Vừa hoàn thành:
- Fix pivot table `review_profile_bom_lists` collision (thêm `profile_type` column + migration)
- Fix BOM type filter cho type=1 (component thay vì aggregate)
- Fix `pricing_request_id` + commercial fields nullable (2 migration)
- Lock giá ERP tại thời điểm tạo BG (bỏ syncErpPrices)
- Permission-aware validate giá nhập (ERP+no quyền → bỏ validate, user-created → giữ, dịch vụ → luôn validate)
- Cột "Giá nhập" luôn hiện: ERP+có quyền=readonly, ERP+không quyền="—", user-created=editable, dịch vụ=editable
- Fix permission "Xem giá vốn hàng hoá": guard_name web→api, group→Báo giá, type→4
- Footer: LN + Cấp duyệt chỉ hiện khi có quyền xem giá vốn
Đang làm dở: Brainstorm Phase B — đã hỏi 4 câu, chốt được 3 quyết định
Bước tiếp theo: Tiếp tục brainstorm Phase B (câu hỏi tiếp: phạm vi lọc theo phòng)
Blocked: Không

**Phase B — Quyết định đã chốt:**
1. Type 2: chỉ NLG cùng phòng KD mới thấy và tạo báo giá từ YCXD giá
2. `department_id` trên PricingRequest lấy từ phòng KD (auto BaseModel), Quotation lấy từ phòng NLG (auto BaseModel)
3. DS YCXD giá: "theo phòng" = Type 2 cùng dept, "theo công ty" = Type 3
4. DS Báo giá: giữ nguyên logic hiện tại
5. Chờ TP duyệt: quotation.department_id IN employee_manage_departments của TP
6. Chờ BGĐ duyệt: quotation.company_id = user.info.company_id
7. Notification YCXD giá: tách theo Type (Type 2 cùng phòng, Type 3 theo công ty)

---

## Phase B — Phân quyền XD giá theo phòng/công ty + Lọc duyệt BG

**Goal:** Tách quyền XD giá theo Type triển khai, lọc duyệt BG theo phòng quản lý (TP) và công ty (BGĐ).

**Spec:** .plans/project-implementation-types/design-phaseB.md

---

### Task 17: Migration — Đổi tên + tạo permission mới

**Files:**
- Create: `hrm-api/database/migrations/2026_05_25_100000_rename_and_add_pricing_permissions.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Spatie\Permission\Models\Permission;

class RenameAndAddPricingPermissions extends Migration
{
    public function up()
    {
        // 1. Đổi tên permission cũ
        Permission::where('name', 'Xây dựng giá Bom giải pháp')
            ->update([
                'name' => 'Xây dựng giá bán theo công ty',
                'display_name' => 'Xây dựng giá bán theo công ty',
            ]);

        // 2. Tạo permission mới
        Permission::updateOrCreate(
            ['name' => 'Xây dựng giá bán theo phòng'],
            [
                'guard_name' => 'api',
                'display_name' => 'Xây dựng giá bán theo phòng',
                'group' => 'Báo giá',
                'type' => 4,
            ]
        );
    }

    public function down()
    {
        Permission::where('name', 'Xây dựng giá bán theo công ty')
            ->update([
                'name' => 'Xây dựng giá Bom giải pháp',
                'display_name' => 'Xây dựng giá Bom giải pháp',
            ]);

        Permission::where('name', 'Xây dựng giá bán theo phòng')->delete();
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
php artisan migrate
```

---

### Task 18: BE — PricingRequestController::index tách logic theo 2 quyền

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/PricingRequestController.php` (line 59-73)

- [ ] **Step 1: Sửa logic phân quyền trong index()**

Thay đoạn check `hasBuildPrice` hiện tại bằng:

```php
$hasBuildByDept = (new \App\CommonServices\PermissionService())
    ->isCurrentEmployeeHasPermission('Xây dựng giá bán theo phòng');
$hasBuildByCompany = (new \App\CommonServices\PermissionService())
    ->isCurrentEmployeeHasPermission('Xây dựng giá bán theo công ty');

$buildStatuses = [
    PricingRequest::STATUS_CHO_XD_GIA,
    PricingRequest::STATUS_DANG_XD_GIA,
    PricingRequest::STATUS_DA_CO_BAO_GIA,
    PricingRequest::STATUS_DONG,
    PricingRequest::STATUS_DUNG,
];

if ($hasBuildByDept || $hasBuildByCompany) {
    $currentDeptId = optional(optional(auth()->user())->info)->department_id;

    $query->where(function ($q) use ($hasBuildByDept, $hasBuildByCompany, $buildStatuses, $currentDeptId) {
        $q->whereIn('status', $buildStatuses);

        $q->where(function ($inner) use ($hasBuildByDept, $hasBuildByCompany, $currentDeptId) {
            if ($hasBuildByDept && $currentDeptId) {
                // Type 2: YCXD giá cùng phòng
                $inner->orWhere(function ($sub) use ($currentDeptId) {
                    $sub->where('department_id', $currentDeptId)
                        ->whereHas('project', function ($pq) {
                            $pq->where('implementation_type', \Modules\Assign\Entities\ProspectiveProject::IMPLEMENTATION_TYPE_BY_DEPT);
                        });
                });
            }
            if ($hasBuildByCompany) {
                // Type 3 (hoặc NULL — legacy)
                $inner->orWhereHas('project', function ($pq) {
                    $pq->where(function ($t) {
                        $t->where('implementation_type', \Modules\Assign\Entities\ProspectiveProject::IMPLEMENTATION_TYPE_CROSS_DEPT)
                          ->orWhereNull('implementation_type');
                    });
                });
            }
        });
    });
} else {
    // NV KD: chỉ thấy YCXD giá mình tạo
    $query->where('created_by', auth()->id());
}
```

- [ ] **Step 2: Verify**

Kiểm tra PricingRequest model có relation `project()` — nếu chưa có thì thêm.

---

### Task 19: BE — PricingRequestService notification tách theo Type

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/PricingRequestService.php` (line 262-283)

- [ ] **Step 1: Sửa notifyPricingBuildersNewRequest()**

```php
private function notifyPricingBuildersNewRequest(PricingRequest $request): void
{
    try {
        $project = $request->project;
        $implementationType = (int) ($project->implementation_type ?? ProspectiveProject::IMPLEMENTATION_TYPE_CROSS_DEPT);

        if ($implementationType === ProspectiveProject::IMPLEMENTATION_TYPE_BY_DEPT) {
            // Type 2: gửi cho NLG cùng phòng có quyền "theo phòng"
            $recipientIds = \Modules\Timesheet\Services\EmployeeInfoService::listEmployeeInfoByPermission('Xây dựng giá bán theo phòng');
            if ($recipientIds->isNotEmpty()) {
                $deptId = $request->department_id;
                $recipientIds = $recipientIds->filter(function ($infoId) use ($deptId) {
                    $info = \Modules\Human\Entities\EmployeeInfo::find($infoId);
                    return $info && (int) $info->department_id === (int) $deptId;
                });
            }
        } else {
            // Type 3: gửi cho NLG có quyền "theo công ty"
            $recipientIds = \Modules\Timesheet\Services\EmployeeInfoService::listEmployeeInfoByPermission('Xây dựng giá bán theo công ty');
        }

        if ($recipientIds->isEmpty()) return;

        $senderName = $this->getCurrentEmployeeName();
        $projectName = $project->name ?? '';

        \Modules\Timesheet\Services\EmployeeInfoService::sendToAllNotification($recipientIds->toArray(), [
            'url' => '/assign/pricing-requests/' . $request->id,
            'title' => '<b>' . $senderName . '</b> gửi yêu cầu xây dựng giá <b>' . $request->code . '</b>'
                . ($projectName ? ' cho dự án ' . $projectName : ''),
            'type' => 'pricing_request_sent',
            'id' => $request->id,
        ]);
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('PricingRequest notification error: ' . $e->getMessage());
    }
}
```

---

### Task 20: BE — QuotationService::getPendingApproval lọc theo dept/company

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` (line 1074-1104)

- [ ] **Step 1: Sửa getPendingApproval()**

```php
public function getPendingApproval(array $filters): \Illuminate\Database\Eloquent\Builder
{
    $hasTp = $this->hasPermission('Trưởng phòng duyệt giá Bom giải pháp');
    $hasBgd = $this->hasPermission('Ban giám đốc duyệt giá Bom giải pháp');

    $query = Quotation::with([
        'pricingRequest:id,code',
        'bomList:id,code,name',
        'project:id,code,name,customer_name',
        'solution:id,name',
        'solutionVersion:id,code',
        'currency:id,code',
        'creator.info',
        'approver.info',
        'productPrices.bomListProduct:id,qty_needed',
    ]);

    if ($hasTp && $hasBgd) {
        $managedDeptIds = $this->getManagedDepartmentIds();
        $companyId = optional(optional(auth()->user())->info)->company_id;

        $query->where(function ($q) use ($managedDeptIds, $companyId) {
            if ($managedDeptIds->isNotEmpty()) {
                $q->orWhere(function ($sub) use ($managedDeptIds) {
                    $sub->where('status', Quotation::STATUS_CHO_TP_DUYET)
                        ->whereIn('department_id', $managedDeptIds);
                });
            }
            if ($companyId) {
                $q->orWhere(function ($sub) use ($companyId) {
                    $sub->where('status', Quotation::STATUS_CHO_BGD_DUYET)
                        ->where('company_id', $companyId);
                });
            }
        });
    } elseif ($hasTp) {
        $managedDeptIds = $this->getManagedDepartmentIds();
        $query->where('status', Quotation::STATUS_CHO_TP_DUYET);
        if ($managedDeptIds->isNotEmpty()) {
            $query->whereIn('department_id', $managedDeptIds);
        } else {
            $query->whereRaw('1 = 0');
        }
    } elseif ($hasBgd) {
        $companyId = optional(optional(auth()->user())->info)->company_id;
        $query->where('status', Quotation::STATUS_CHO_BGD_DUYET);
        if ($companyId) {
            $query->where('company_id', $companyId);
        } else {
            $query->whereRaw('1 = 0');
        }
    } else {
        $query->whereRaw('1 = 0');
    }

    $this->applyListFilters($query, $filters);

    return $query;
}
```

- [ ] **Step 2: Thêm helper getManagedDepartmentIds()**

```php
private function getManagedDepartmentIds(): \Illuminate\Support\Collection
{
    $employeeInfoId = auth()->user()->employee_info_id ?? null;
    if (!$employeeInfoId) return collect();

    $employee = \Modules\Human\Entities\Employee::where('employee_info_id', $employeeInfoId)->first();
    if (!$employee) return collect();

    return \DB::table('employee_manage_departments')
        ->where('employee_id', $employee->id)
        ->pluck('department_id');
}
```

---

### Task 21: BE — Validate quyền duyệt/từ chối theo dept/company

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Thêm helper ensureTpCanApprove() và ensureBgdCanApprove()**

```php
private function ensureTpCanApprove(Quotation $quotation): void
{
    $managedDeptIds = $this->getManagedDepartmentIds();
    if (!$managedDeptIds->contains((int) $quotation->department_id)) {
        throw new \Exception('Bạn không quản lý phòng ban của báo giá này.');
    }
}

private function ensureBgdCanApprove(Quotation $quotation): void
{
    $companyId = optional(optional(auth()->user())->info)->company_id;
    if ((int) $quotation->company_id !== (int) $companyId) {
        throw new \Exception('Bạn không thuộc công ty của báo giá này.');
    }
}
```

- [ ] **Step 2: Gọi trong tpApprove(), bgdApprove(), reject()**

Trong `tpApprove()`:
```php
$this->ensurePermission('Trưởng phòng duyệt giá Bom giải pháp');
$this->ensureTpCanApprove($quotation); // THÊM
```

Trong `bgdApprove()`:
```php
$this->ensurePermission('Ban giám đốc duyệt giá Bom giải pháp');
$this->ensureBgdCanApprove($quotation); // THÊM
```

Trong `reject()`:
```php
// Sau ensurePermission, thêm:
if ($quotation->status === Quotation::STATUS_CHO_TP_DUYET) {
    $this->ensureTpCanApprove($quotation);
} elseif ($quotation->status === Quotation::STATUS_CHO_BGD_DUYET) {
    $this->ensureBgdCanApprove($quotation);
}
```

---

## Phase C — Báo giá trực tiếp (không GP, không BOM)

> Spec: `.plans/project-implementation-types/design-phaseC.md`
> Scope: Type 1 (tự triển khai) — KD tạo báo giá trực tiếp từ Dự án TKT, không qua Giải pháp/BOM.

### Task 22: Migration — DB changes cho báo giá trực tiếp

**Files:**
- Create: `hrm-api/database/migrations/2026_05_27_100000_add_direct_quotation_support.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddDirectQuotationSupport extends Migration
{
    public function up()
    {
        // 1. quotations.bom_list_id nullable
        Schema::table('quotations', function (Blueprint $table) {
            $table->unsignedBigInteger('bom_list_id')->nullable()->change();
        });

        // 2. quotation_product_prices: bom_list_product_id nullable + thêm product fields
        Schema::table('quotation_product_prices', function (Blueprint $table) {
            $table->unsignedBigInteger('bom_list_product_id')->nullable()->change();
        });

        // Drop unique constraint cũ (vì bom_list_product_id nullable)
        Schema::table('quotation_product_prices', function (Blueprint $table) {
            $table->dropUnique('uq_quotation_product');
        });

        Schema::table('quotation_product_prices', function (Blueprint $table) {
            $table->unsignedInteger('quotation_group_id')->nullable()->after('bom_list_product_id');
            $table->unsignedBigInteger('parent_id')->nullable()->after('quotation_group_id');
            $table->tinyInteger('product_type')->default(1)->after('parent_id');
            $table->unsignedBigInteger('erp_product_id')->nullable()->after('product_type');
            $table->string('code')->nullable()->after('erp_product_id');
            $table->string('name')->nullable()->after('code');
            $table->unsignedBigInteger('model_id')->nullable()->after('name');
            $table->unsignedBigInteger('brand_id')->nullable()->after('model_id');
            $table->unsignedBigInteger('origin_id')->nullable()->after('brand_id');
            $table->unsignedBigInteger('unit_id')->nullable()->after('origin_id');
            $table->double('qty_needed')->default(0)->after('unit_id');
            $table->text('product_attributes')->nullable()->after('qty_needed');
            $table->integer('sort_order')->default(0)->after('product_attributes');

            $table->index(['quotation_id', 'bom_list_product_id'], 'idx_quotation_bom_product');
        });

        // 3. Tạo bảng quotation_groups
        Schema::create('quotation_groups', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('quotation_id');
            $table->string('name');
            $table->integer('sort_order')->default(0);
            $table->timestamps();

            $table->index('quotation_id', 'idx_quotation_groups_quotation');
        });
    }

    public function down()
    {
        Schema::dropIfExists('quotation_groups');

        Schema::table('quotation_product_prices', function (Blueprint $table) {
            $table->dropIndex('idx_quotation_bom_product');
            $table->dropColumn([
                'quotation_group_id', 'parent_id', 'product_type', 'erp_product_id',
                'code', 'name', 'model_id', 'brand_id', 'origin_id', 'unit_id',
                'qty_needed', 'product_attributes', 'sort_order',
            ]);
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-api && php artisan migrate
```

---

### Task 23: BE — Model QuotationGroup + QuotationProductPrice relations

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/QuotationGroup.php`
- Modify: `hrm-api/Modules/Assign/Entities/QuotationProductPrice.php`
- Modify: `hrm-api/Modules/Assign/Entities/Quotation.php`

- [ ] **Step 1: Tạo Model QuotationGroup**

```php
<?php

namespace Modules\Assign\Entities;

use Modules\Human\Entities\BaseModel;

class QuotationGroup extends BaseModel
{
    protected $table = 'quotation_groups';
    protected $guarded = [];
}
```

- [ ] **Step 2: Thêm relations mới vào QuotationProductPrice**

```php
// Thêm vào QuotationProductPrice.php
public function quotationGroup()
{
    return $this->belongsTo(QuotationGroup::class, 'quotation_group_id');
}

public function parent()
{
    return $this->belongsTo(self::class, 'parent_id');
}

public function children()
{
    return $this->hasMany(self::class, 'parent_id');
}

// Relations ERP (chỉ dùng khi bom_list_product_id IS NULL)
public function tpModel()
{
    return $this->belongsTo(\Modules\Human\Entities\TpModel::class, 'model_id');
}

public function tpBrand()
{
    return $this->belongsTo(\Modules\Human\Entities\TpBrand::class, 'brand_id');
}

public function tpOrigin()
{
    return $this->belongsTo(\Modules\Human\Entities\TpOrigin::class, 'origin_id');
}

public function tpUnit()
{
    return $this->belongsTo(\Modules\Human\Entities\TpUnit::class, 'unit_id');
}
```

- [ ] **Step 3: Thêm relation `quotationGroups` vào Quotation model**

```php
// Thêm vào Quotation.php
public function quotationGroups()
{
    return $this->hasMany(QuotationGroup::class)->orderBy('sort_order');
}
```

- [ ] **Step 4: Thêm helper `isDirectQuotation()` vào Quotation model**

```php
public function isDirectQuotation(): bool
{
    return empty($this->bom_list_id);
}
```

---

### Task 24: BE — QuotationService::createDirect()

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Thêm method createDirect()**

```php
public function createDirect(ProspectiveProject $project): Quotation
{
    return DB::transaction(function () use ($project) {
        if ((int) $project->implementation_type !== ProspectiveProject::IMPLEMENTATION_TYPE_SELF) {
            throw new \Exception('Chỉ dự án Tự triển khai mới được tạo báo giá trực tiếp.');
        }

        $customer = $project->customer_id ? Customer::find($project->customer_id) : null;

        $quotation = new Quotation();
        $quotation->fill([
            'pricing_request_id' => null,
            'bom_list_id' => null,
            'project_id' => $project->id,
            'solution_id' => null,
            'solution_version_id' => null,
            'solution_version_code' => null,
            'solution_module_id' => null,
            'solution_module_version_id' => null,
            'module_version_code' => null,
            'currency_id' => null,
            'customer_id' => $project->customer_id,
            'customer_code' => $project->customer_code ?? ($customer ? $customer->code : null),
            'customer_name' => $project->customer_name ?: ($customer ? $customer->name : ''),
            'customer_tax_code' => $project->customer_tax_code ?? null,
            'customer_address' => $project->customer_address ?? null,
            'customer_email' => $project->customer_email ?? null,
            'customer_contact_name' => $project->customer_contact_name ?? null,
            'customer_contact_phone' => $project->customer_contact_phone ?? null,
            'status' => Quotation::STATUS_DANG_TAO,
        ]);
        $quotation->code = $quotation->getNextCode();
        $quotation->save();

        if ($project->status < ProspectiveProject::STATUS_DU_TOAN) {
            $project->update(['status' => ProspectiveProject::STATUS_DU_TOAN]);
        }

        $this->logHistory($quotation->id, QuotationHistory::ACTION_CREATE, null, Quotation::STATUS_DANG_TAO);

        return $quotation->fresh();
    });
}
```

- [ ] **Step 2: Thêm route + controller method**

Route (`Routes/api.php`):
```php
Route::post('/create-direct', [QuotationController::class, 'createDirect']);
```

Controller:
```php
public function createDirect(Request $request)
{
    try {
        $projectId = $request->input('project_id');
        $project = ProspectiveProject::findOrFail($projectId);
        $quotation = $this->quotationService->createDirect($project);
        return $this->responseJson(new DetailQuotationResource($quotation));
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

---

### Task 25: BE — Sửa upsertPrices() hỗ trợ báo giá trực tiếp

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Sửa upsertPrices — xử lý 2 case**

Logic mới:
```php
private function upsertPrices(Quotation $quotation, array $products): void
{
    if ($quotation->isDirectQuotation()) {
        $this->upsertDirectProducts($quotation, $products);
    } else {
        $this->upsertBomProducts($quotation, $products);
    }
    $this->recomputeTotals($quotation);
}
```

- [ ] **Step 2: Extract logic cũ vào upsertBomProducts()**

Move toàn bộ logic hiện tại của `upsertPrices` vào method mới `upsertBomProducts()`. Giữ nguyên logic, chỉ đổi tên.

- [ ] **Step 3: Viết upsertDirectProducts()**

```php
private function upsertDirectProducts(Quotation $quotation, array $products): void
{
    $sentIds = collect($products)->pluck('price_id')->filter()->toArray();

    // Xóa products không còn trong danh sách FE gửi
    QuotationProductPrice::where('quotation_id', $quotation->id)
        ->when(!empty($sentIds), fn($q) => $q->whereNotIn('id', $sentIds))
        ->when(empty($sentIds), fn($q) => $q)
        ->delete();

    // Sync groups
    $groupData = collect($products)
        ->pluck('quotation_group_id', 'group_name')
        ->filter(fn($v, $k) => $k)
        ->unique();
    // Groups sẽ được sync riêng qua syncDirectGroups()

    foreach ($products as $p) {
        $isErp = !empty($p['erp_product_id']);

        $data = [
            'quotation_id' => $quotation->id,
            'bom_list_product_id' => null,
            'quotation_group_id' => $p['quotation_group_id'] ?? null,
            'parent_id' => $p['parent_id'] ?? null,
            'product_type' => $p['product_type'] ?? 1,
            'erp_product_id' => $p['erp_product_id'] ?? null,
            'code' => $p['code'] ?? null,
            'name' => $p['name'] ?? null,
            'model_id' => $p['model_id'] ?? null,
            'brand_id' => $p['brand_id'] ?? null,
            'origin_id' => $p['origin_id'] ?? null,
            'unit_id' => $p['unit_id'] ?? null,
            'qty_needed' => $p['qty_needed'] ?? 0,
            'product_attributes' => $p['product_attributes'] ?? null,
            'sort_order' => $p['sort_order'] ?? 0,
            'vat_percent' => $p['vat_percent'] ?? 0,
        ];

        if (!$isErp) {
            $data['estimated_price'] = $p['estimated_price'] ?? 0;
            $data['quoted_price'] = $p['quoted_price'] ?? 0;
        }

        // Discount fields
        foreach (['discount_input_mode', 'discount_percent', 'discount_amount', 'allocated_discount_amount'] as $field) {
            if (array_key_exists($field, $p)) {
                $data[$field] = $p[$field] ?? 0;
            }
        }

        if (!empty($p['price_id'])) {
            QuotationProductPrice::where('id', $p['price_id'])
                ->where('quotation_id', $quotation->id)
                ->update($data);
        } else {
            $data['created_by'] = auth()->id();
            $data['updated_by'] = auth()->id();
            QuotationProductPrice::create($data);
        }
    }
}
```

---

### Task 26: BE — Sửa recomputeTotals() hỗ trợ báo giá trực tiếp

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Step 1: Đọc code recomputeTotals() hiện tại**

Xác định chỗ nào đọc từ `bomList->products` và cần fallback.

- [ ] **Step 2: Sửa recomputeTotals()**

Khi `isDirectQuotation()`:
- Thay `$bomList->products` bằng `$quotation->productPrices` 
- Dùng `$qpp->qty_needed` thay vì `$blp->qty_needed`
- Dùng `$qpp->parent_id` thay vì `$blp->parent_id`
- Dùng `$qpp->erp_product_id` thay vì `$blp->erp_product_id`
- Logic tính toán (VAT, discount, totals) giữ nguyên

---

### Task 27: BE — Sửa DetailQuotationResource hỗ trợ 2 nguồn data

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php`

- [ ] **Step 1: Sửa phần load products**

Khi `isDirectQuotation()`:
- Load products trực tiếp từ `quotation_product_prices` (với relations tpModel/tpBrand/tpOrigin/tpUnit trên QPP)
- Map fields: dùng `$qpp->name`, `$qpp->code`, `$qpp->qty_needed`... thay vì `$qpp->bomListProduct->name`

Khi có BOM:
- Giữ nguyên logic hiện tại

- [ ] **Step 2: Sửa phần load groups**

```php
if ($this->isDirectQuotation()) {
    $groups = QuotationGroup::where('quotation_id', $this->id)
        ->orderBy('sort_order')
        ->get(['id', 'name', 'sort_order']);
} else {
    $groups = DB::table('bom_list_groups')
        ->where('bom_list_id', $this->bom_list_id)
        ->orderBy('sort_order')
        ->get(['id', 'name', 'sort_order']);
}
```

- [ ] **Step 3: Thêm flag `is_direct_quotation` vào response**

```php
'is_direct_quotation' => $this->isDirectQuotation(),
```

---

### Task 28: BE — Sync groups cho báo giá trực tiếp

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php`
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`

- [ ] **Step 1: Thêm method syncDirectGroups()**

```php
private function syncDirectGroups(Quotation $quotation, array $groups): void
{
    $sentIds = collect($groups)->pluck('id')->filter()->toArray();

    // Xóa groups không còn
    QuotationGroup::where('quotation_id', $quotation->id)
        ->when(!empty($sentIds), fn($q) => $q->whereNotIn('id', $sentIds))
        ->delete();

    foreach ($groups as $idx => $g) {
        if (!empty($g['id'])) {
            QuotationGroup::where('id', $g['id'])
                ->where('quotation_id', $quotation->id)
                ->update([
                    'name' => $g['name'],
                    'sort_order' => $g['sort_order'] ?? $idx,
                ]);
        } else {
            QuotationGroup::create([
                'quotation_id' => $quotation->id,
                'name' => $g['name'],
                'sort_order' => $g['sort_order'] ?? $idx,
            ]);
        }
    }
}
```

- [ ] **Step 2: Gọi syncDirectGroups trong save()**

Trong controller `save()`: nếu `isDirectQuotation()` và request có `groups` → gọi `syncDirectGroups()` trước `upsertPrices()`.

---

### Task 29: BE — Export Excel hỗ trợ báo giá trực tiếp

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`

- [ ] **Step 1: Sửa exportExcel() — build virtual BOM khi không có BOM**

Khi `$quotation->isDirectQuotation()`:
- Thay vì load `$quotation->bomList->products`, build collection products từ `quotation_product_prices` với structure giống BomListProduct (name, code, qty_needed, erp_product_id, parent_id, tpModel, tpBrand, tpOrigin, tpUnit...)
- Build virtual groups từ `quotation_groups`
- Gán vào object để blade template render được (cùng property names)

---

### Task 30: FE — Ẩn tab GP + BOM trên Dự án TKT Type 1

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/_id/manager.vue`

- [ ] **Step 1: Sửa computed tabs()**

Ẩn tab `solution-info` và các tab phụ thuộc solution (tasks, issues, files, review-profiles) khi `tktForm.implementation_type === 1`:

```js
// Trong computed tabs()
const isSelf = this.tktForm && Number(this.tktForm.implementation_type) === 1

// Filter tabs:
// - solution-info: ẩn khi isSelf
// - tasks, issues, files, review-profiles: ẩn khi isSelf (vì không có solution)
// - req: ẩn khi isSelf (không có YC làm GP)
```

---

### Task 31: FE — Tab Báo giá thêm nút "Tạo báo giá" cho Type 1

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

- [ ] **Step 1: Nhận thêm prop**

```js
props: {
    projectId: { type: [Number, String], required: true },
    mainSaleEmployeeId: { type: [Number, String, null], default: null },
    implementationType: { type: [Number, null], default: null },
},
```

- [ ] **Step 2: Thêm nút "Tạo báo giá"**

Trong template, trước V2BaseDataTable:
```html
<div v-if="canCreateDirect" class="mb-3">
    <button class="btn btn-primary btn-sm" :disabled="creating" @click="handleCreateDirect">
        <i class="ri-add-line mr-1"></i>
        {{ creating ? 'Đang tạo...' : 'Tạo báo giá' }}
    </button>
</div>
```

- [ ] **Step 3: Thêm computed + method**

```js
computed: {
    canCreateDirect() {
        return Number(this.implementationType) === 1 && this.isSaleOfProject
    },
},
methods: {
    async handleCreateDirect() {
        this.creating = true
        try {
            const res = await this.$store.dispatch('apiPostMethod', {
                url: 'assign/quotations/create-direct',
                payload: { project_id: this.projectId },
            })
            const id = res?.data?.id
            if (id) {
                this.$router.push(`/assign/quotations/${id}/edit`)
            }
        } catch (e) {
            this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi tạo báo giá' })
        } finally {
            this.creating = false
        }
    },
}
```

- [ ] **Step 4: Truyền prop từ manager.vue**

```html
<ProspectiveProjectQuotationsTab
    :project-id="$route.params.id"
    :main-sale-employee-id="tktForm && tktForm.main_sale_employee_id"
    :implementation-type="tktForm && tktForm.implementation_type"
/>
```

---

### Task 32: FE — Form edit báo giá: chế độ quản lý sản phẩm trực tiếp

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

- [ ] **Step 1: Detect chế độ direct quotation**

```js
computed: {
    isDirectQuotation() {
        return this.item && this.item.is_direct_quotation === true
    },
}
```

- [ ] **Step 2: Thêm UI quản lý nhóm (quotation_groups)**

Khi `isDirectQuotation`:
- Hiện nút "Thêm nhóm" → thêm row group mới vào `this.groups`
- Mỗi group header có: input tên nhóm (editable), nút xóa nhóm, nút "Thêm hàng hoá"
- Drag-drop sắp xếp nhóm (optional — có thể dùng sort_order + nút lên/xuống)

- [ ] **Step 3: Thêm UI thêm/xóa sản phẩm**

Khi `isDirectQuotation`:
- Mỗi nhóm có nút "Thêm hàng hoá" → mở modal search ERP + thêm hàng tự tạo (reuse `BomBuilderAddProductModal` hoặc tạo tương tự)
- Mỗi product row có nút xóa (icon trash)
- Hàng cha có nút "Thêm hàng con"
- Fields sản phẩm editable: name, code, qty_needed (cho hàng tự tạo), unit
- Fields giá editable: estimated_price, quoted_price, vat_percent, discount (giống hiện tại)

- [ ] **Step 4: Sửa save() — gửi full data cho báo giá trực tiếp**

Khi `isDirectQuotation`:
```js
const payload = {
    // ... commercial fields (description, deadline, ...)
    groups: this.groups.map((g, i) => ({
        id: g.id || null,
        name: g.name,
        sort_order: i,
    })),
    products: this.products.map((p, i) => ({
        price_id: p.price_id || null,
        quotation_group_id: p.quotation_group_id || null,
        parent_id: p.parent_id || null,
        product_type: p.product_type || 1,
        erp_product_id: p.erp_product_id || null,
        code: p.code,
        name: p.name,
        model_id: p.model_id || null,
        brand_id: p.brand_id || null,
        origin_id: p.origin_id || null,
        unit_id: p.unit_id || null,
        qty_needed: p.qty_needed,
        product_attributes: p.product_attributes || null,
        sort_order: i,
        estimated_price: p.estimated_price,
        quoted_price: p.quoted_price,
        vat_percent: p.vat_percent,
        discount_input_mode: p.discount_input_mode,
        discount_percent: p.discount_percent,
        discount_amount: p.discount_amount,
        allocated_discount_amount: p.allocated_discount_amount,
    })),
    // ... service_items, discount data
}
```

---

### Task 33: FE — Trang xem báo giá + in + gửi duyệt: hỗ trợ báo giá trực tiếp

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/index.vue`

- [ ] **Step 1: Sửa trang xem — ẩn cột BOM khi direct**

Khi `is_direct_quotation`:
- Ẩn link BOM trong header info
- Products đã có đầy đủ data từ API (Task 27) nên render giống cũ

- [ ] **Step 2: Kiểm tra popup gửi duyệt + in báo giá**

Confirm các component này đọc data từ quotation response (không truy cập BOM trực tiếp). Nếu có chỗ nào reference `bom_list` → xử lý null case.

---

### Checkpoint Phase C — 2026-05-27

**Verify checklist:**
- [ ] Migration chạy thành công
- [ ] Dự án Type 1: ẩn tab GP + BOM
- [ ] Tab Báo giá: nút "Tạo báo giá" chỉ hiện cho Type 1 + KD phụ trách
- [ ] Tạo báo giá trực tiếp → quotation trống, redirect edit
- [ ] Form edit: thêm/xóa nhóm, thêm/xóa sản phẩm (ERP + tự tạo), parent-child
- [ ] Form edit: nhập giá + VAT + chiết khấu hoạt động bình thường
- [ ] Lưu → sync groups + products đúng
- [ ] Xem chi tiết báo giá trực tiếp hiển thị đúng
- [ ] Export Excel báo giá trực tiếp hoạt động
- [ ] Gửi duyệt → duyệt → hoạt động bình thường
- [ ] Báo giá cũ (có BOM) vẫn hoạt động không ảnh hưởng

---

### Checkpoint Phase B — 2026-05-25
Vừa hoàn thành: Tất cả 5 tasks Phase B (T17-T21)
Đang làm dở: Không
Bước tiếp theo: Test thủ công Phase B, sau đó Phase C
Blocked: Không

**Verify checklist:**
- [x] Permission "Xây dựng giá Bom giải pháp" đổi tên thành "Xây dựng giá bán theo công ty"
- [x] Permission mới "Xây dựng giá bán theo phòng" đã tạo (group=Báo giá)
- [x] DS YCXD giá: quyền "theo phòng" chỉ thấy Type 2 cùng dept, quyền "theo công ty" chỉ thấy Type 3
- [x] Notification YCXD giá: Type 2 gửi NLG cùng phòng, Type 3 gửi NLG có quyền công ty
- [x] Chờ TP duyệt: lọc theo employee_manage_departments
- [x] Chờ BGĐ duyệt: lọc theo company_id
- [x] tpApprove/bgdApprove/reject: validate dept/company trước khi cho duyệt
- [ ] Test: NLG có quyền "theo phòng" thấy đúng YCXD giá Type 2 cùng phòng
- [ ] Test: NLG có quyền "theo công ty" thấy đúng YCXD giá Type 3
- [ ] Test: TP chỉ thấy BG chờ duyệt của phòng mình quản lý
- [ ] Test: BGĐ chỉ thấy BG chờ duyệt của công ty mình

### Checkpoint — 2026-05-25 (Session 3: Bug fix + Menu + Phân quyền)
Vừa hoàn thành:
- [x] Menu "Quản lý báo giá": bỏ isShow, luôn hiện
- [x] Menu "Yêu cầu báo giá": cập nhật tên quyền cũ → mới (theo công ty + theo phòng)
- [x] FE pricing-requests/index.vue + _id/index.vue: đổi tên quyền cũ "Xây dựng giá Bom giải pháp" → check cả 2 quyền mới
- [x] FE quotations/index.vue: nút Sửa thêm check creator_id (chỉ người tạo mới thấy)
- [x] FE quotations/_id/edit.vue: canEdit thêm check creator_id (người khác vào = readonly)
- [x] BE DetailQuotationResource: hàng user tự tạo (non-ERP) luôn trả estimated_price, không phụ thuộc quyền Xem giá vốn
Đang làm dở: Điều tra bug import BOM — service item mất nhóm (đã xác định nguyên nhân: cột Nhóm hàng chỉ ghi ở dòng đầu, chưa carry-forward)
Bước tiếp theo: Xác nhận hướng sửa bug import BOM với user, sau đó Phase C
Blocked: Chờ user xác nhận convention file Excel (nhóm hàng ghi 1 lần hay mỗi dòng)

# Plan — Phương án triển khai dự án

**Spec:** `docs/superpowers/specs/2026-05-23-project-implementation-types-design.md`
**Design:** `design.md`

---

## Phase 1 — DB & Model ✅ DONE 2026-05-23

### BE
- [x] Migration: thêm `prospective_projects.implementation_type` (tinyint NOT NULL default 3) — `2026_05_23_000001_add_implementation_type_to_prospective_projects_table.php`
- [x] Migration: đổi `solutions.request_solution_id` sang nullable — `2026_05_23_000002_make_request_solution_id_nullable_on_solutions.php`
- [x] Cập nhật `ProspectiveProject` entity: const `IMPLEMENTATION_TYPE_SELF=1, BY_DEPT=2, CROSS_DEPT=3` + mảng `IMPLEMENTATION_TYPES` + thêm vào `$fillable`.
- [x] Helper `ProspectiveProject::isLockedImplementationType()` + accessor `is_locked_implementation_type`.
- [x] Transformer: `DetailProspectiveProjectResource` + `ProspectiveProjectResource` trả về `implementation_type` (+ `is_locked_implementation_type` cho detail).
- [x] `ProspectiveProjectRequest`: thêm rule `implementation_type|nullable|integer|in:1,2,3`.
- [x] `ProspectiveProjectService::update()`: throw `ValidationException` khi đổi type lúc đã locked.

### FE
- [x] `pages/assign/prospective-projects/constants.js` — export `IMPL_TYPE_*`, `IMPLEMENTATION_TYPES`, các `STATUS_*`.
- [x] `ProjectInfoSection.vue`: thêm V2BaseSelect "Cách triển khai dự án" (default=3), disable khi locked + helper text.
- [x] `add.vue` + `_id/edit.vue`: thêm `implementation_type: 3` + `is_locked_implementation_type: false` vào `formSubmit`.

### Checkpoint — 2026-05-23
Vừa hoàn thành: Phase 1 (Migration + Entity + FormRequest + Service guard + Transformer + FE form). Chưa chạy migration + chưa test browser.
Đang làm dở: không
Bước tiếp theo: User chạy 2 migrations + smoke test màn `/assign/prospective-projects/add` (xem dropdown hiện đủ 3 option, default=3) + edit dự án cũ (dropdown vẫn = 3, không lock). Sau đó tiếp Phase 2.
Blocked: không

## Phase 2 — Type=1 luồng tạo Solution không qua RequestSolution ✅ DONE 2026-05-23

### BE
- [x] `SolutionService::normalizePayload()` — branch type=1 (ép has_modules=false, pm_id=auth, request_solution_id=null, status=DANG_TRIEN_KHAI)
- [x] `SolutionService::create()` — end_date ưu tiên payload `internal_need_gp_date`
- [x] `SolutionService::updateRequestSolution()` — null-guard đầu hàm
- [x] `SolutionRequest` — `request_solution_id` nullable khi type=1
- [x] Null-safe `Solution::isCanManage()` (line 158)
- [x] `ProspectiveProjectService::syncStatusBySolution()` — branch type=1 (chỉ 2 trạng thái DANG_TRIEN_KHAI/DA_DUYET_GIAI_PHAP)

### FE
- [x] `index.vue` — action icon "Tạo giải pháp" cho type=1 + status=THU_THAP_TT (đã làm task #6)
- [x] `SolutionForm.vue` — nhận query `prospective_project_id`, capture `implementation_type` từ project, preset has_modules=false, pm_id=auth khi type=1
- [x] `InfoTab.vue` — ẩn checkbox has_modules, hiện helper text "KD trực tiếp làm GP" cho type=1
- [x] `manager.vue` — không cần sửa (nút PM/Leader duyệt đã gate bằng status, không xuất hiện khi type=1)

## Phase 3 — Type=1 Hồ sơ trình duyệt auto-approve ✅ DONE 2026-05-23

### BE
- [x] `SolutionService::storeSolutionReviewProfile()` — branch $isSelf: status='approved' ngay, approved_at, Solution=DA_DUYET_GIAI_PHAP, SolutionVersion approved_at, BOM 'approved', skip notification
- [x] `SolutionService::reviewSolutionProfileDecision()` — throw 422 khi type=1
- [x] `DetailSolutionResource` — trả về `implementation_type`

### FE
- [x] `SolutionApprovalModal.vue` — ẩn block "Người phê duyệt", ẩn footer dept_head action, đổi text "Lưu & Trình duyệt" → "Lưu & Duyệt" khi isSelfImplementation
- [x] Cột "Trạng thái duyệt" — type=1 hiển thị "approved" tự nhiên (BE trả về status đúng)

## Phase 4 — Type=2 (Triển khai theo Phòng) ✅ DONE 2026-05-23

### BE
- [x] `RequestSolutionService::store()` — type=2 lock `receive_dept = project.main_sale_department_id`, throw 422 nếu type=1 cố tạo YC
- [x] `RequestSolutionService::update()` — type=2 lock receive_dept tương tự
- [x] `RequestSolutionService::pending()` — filter mở rộng: type=3 (departmentsManager + backward compat null), type=2 (receive_dept = phòng user hiện tại)
- [x] `Solution::isCanManage()` — branch type=2 (check `receive_dept == auth.dept_id` thay vì departmentsManager)

### FE
- [x] `RequestTab.vue` — computed `isByDept` + watcher autoReceiveDept, auto-set + disable select + helper text cho type=2

## Phase 5 — QA (CHỜ USER TEST)

- [ ] Chạy 2 migrations: `php artisan migrate`
- [ ] Test type=1 end-to-end: tạo dự án (chọn Tự triển khai) → submit để chuyển status=2 → bấm icon "Tạo giải pháp" trên list → form Solution preset đúng (ẩn YC làm GP, KD=PM, không hạng mục) → lưu → kiểm tra Solution=`7 Đang triển khai`, Project=`4 Đang làm GP` → vào manager → tạo BOM tổng hợp Hoàn thành cho version → tạo Hồ sơ trình duyệt → bấm "Lưu & Duyệt" → kiểm tra Solution=`11 Đã duyệt GP`, Project=`5 Đã duyệt GP`, profile=`approved`
- [ ] Test type=2 end-to-end: tạo dự án (chọn Theo Phòng) → tạo YC làm GP → kiểm tra receive_dept auto-lock = phòng KD → submit YC → user có permission ở phòng KD đó vào `/assign/request-solution/pending` thấy YC → tiếp nhận → flow giống type=3
- [ ] Test type=3: tạo dự án mặc định Liên phòng ban → toàn bộ luồng cũ vẫn hoạt động (không regression)
- [ ] Edge: dự án đã có Solution → đổi implementation_type → bị chặn 422
- [ ] Edge: dự án type=1 → cố gọi API tạo RequestSolution → bị chặn 422
- [ ] Edge: dự án cũ default type=3 sau migration → list/edit không vỡ

### Checkpoint — 2026-05-23
Vừa hoàn thành: Phase 1+2+3+4 — toàn bộ BE + FE cho type=1 (Tự triển khai) + type=2 (Theo phòng) + bảo toàn type=3.
Đang làm dở: không
Bước tiếp theo: User chạy migration + test theo checklist Phase 5.
Blocked: không

### Checkpoint — 2026-05-24 (HOÀN THÀNH)
User test xong type=1 và type=2 → OK. Các fix bổ sung trong quá trình test:
- Null-safe `DetailSolutionResource::project_internal_need_gp_date` + `request_solution_status` cho type=1
- Sửa `normalizePayload` để Lưu nháp giữ TAO_NHAP, chỉ Lưu & gửi mới nhảy DANG_TRIEN_KHAI (type=1)
- Chặn tạo Solution thứ 2 cho dự án đã có Solution (BE + FE ẩn icon "Tạo giải pháp")
- Ẩn nút "Lưu và duyệt hạng mục" trong edit.vue khi type=1
- Ẩn block "Yêu cầu làm GP" trong InfoTab + ProjectInfoTab + list solutions cho type=1
- Disable PM select + helper "KD là PM" cho type=1
- Ẩn field "Hạn duyệt" trong modal review profile cho type=1
- Bỏ filter `bom_list_type=TYPE_AGGREGATE` ban đầu rồi revert lại (vẫn yêu cầu BOM tổng hợp)
- `handleReviewProfileSaved` redirect sang manager page sau Lưu & Duyệt type=1 (tránh toast can_edit=false)
- Thêm `implementation_type: 3` vào tktForm init để Vue 2 reactive khi populate từ project
- Filter BE: loại dự án type=1 ra khỏi dropdown chọn dự án trong form tạo YC làm GP

Trạng thái: ✅ Hoàn thành, đã chuyển sang "Hoàn thành" trong STATUS.md.
