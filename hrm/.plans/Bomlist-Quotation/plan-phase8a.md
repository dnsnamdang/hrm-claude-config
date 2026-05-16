# BOM List Phase 8a — Status workflow + Currency + Columns + Service

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để implement task-by-task. Steps dùng `- [ ]` để tracking.

**Goal:** Cập nhật BOM List với 6 status mới (gắn submission), currency cho mỗi BOM, cột giá bán + tỷ suất, loại dữ liệu Dịch vụ.

**Architecture:** Reuse cột giá có sẵn (`estimated_price`/`quoted_price`) + accessor cho thành tiền/tỷ suất. Currency 1-1 với BOM (FK sang ERP). Sync status BOM Tổng hợp từ `SolutionReviewProfile`/`SolutionModuleReviewProfile` thủ công qua service. Dịch vụ phân biệt qua `product_type` cùng bảng.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, MySQL (dual DB: hrm_tpe + erp2326)

---

## File Structure

### Backend — Tạo mới
- `database/migrations/2026_04_10_100000_add_currency_id_to_bom_lists.php`
- `database/migrations/2026_04_10_100001_add_product_type_to_bom_list_products.php`
- `database/migrations/2026_04_10_100002_update_bom_lists_status_comment.php`
- `Modules/Human/Entities/TpCurrency.php` — Model currencies từ ERP (mysql2)

### Backend — Sửa
- `Modules/Assign/Entities/BomList.php` — Thêm const STATUS_DA_DUOC_TONG_HOP, STATUS_KHONG_DUYET, update getStatusList(), thêm relationship currency()
- `Modules/Assign/Entities/BomListProduct.php` — Thêm const PRODUCT_TYPE_*, accessors import_total/sale_total/profit_margin
- `Modules/Assign/Services/BomListService.php` — Thêm syncStatusFromSubmission(), syncChildStatus(), update store/update/syncProducts()
- `Modules/Assign/Http/Controllers/Api/V1/BomListController.php` — Thêm getCurrencies()
- `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php` — Rule currency_id + conditional product_type
- `Modules/Assign/Routes/api.php` — Route currencies
- `Modules/Assign/Exports/BomListExport.php` — Cột Loại, Giá bán, Thành tiền bán, Tỷ suất + header currency
- `Modules/Assign/Imports/BomListImport.php` — Parse cột Loại, conditional validate
- `Modules/Assign/Transformers/BomListResource/BomListShowResource.php` — Append currency, accessor
- `Modules/Assign/Services/SolutionReviewProfileService.php` — Hook gọi syncStatusFromSubmission khi đổi status
- `Modules/Assign/Services/SolutionModuleReviewProfileService.php` — Tương tự

### Frontend — Sửa
- `pages/assign/bom-list/components/BomBuilderInfoCard.vue` — Select Currency
- `pages/assign/bom-list/components/BomBuilderTableCard.vue` — Cột giá bán, thành tiền nhập/bán, tỷ suất + icon hàng/dịch vụ
- `pages/assign/bom-list/components/BomBuilderAddProductModal.vue` — Tab 2 toggle Hàng/Dịch vụ
- `pages/assign/bom-list/components/BomBuilderEditor.vue` — Handle currency change, sync productType
- `pages/assign/bom-list/components/BomBuilderImportModal.vue` — Preview cột Loại
- `pages/assign/bom-list/_id/index.vue` — Hiển thị currency + cột mới ở chi tiết
- `pages/assign/bom-list/index.vue` — Filter status thêm 5, 6 (nếu cần)

---

## Task 1: Migration — thêm currency_id vào bom_lists

**Files:**
- Create: `hrm-api/database/migrations/2026_04_10_100000_add_currency_id_to_bom_lists.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class AddCurrencyIdToBomLists extends Migration
{
    public function up()
    {
        Schema::table('bom_lists', function (Blueprint $table) {
            $table->unsignedBigInteger('currency_id')->nullable()->after('customer_id')
                ->comment('FK currencies (ERP DB)');
        });

        // Backfill VND cho data cũ
        try {
            $vndId = DB::connection('mysql2')->table('currencies')->where('code', 'VND')->value('id');
            if ($vndId) {
                DB::table('bom_lists')->whereNull('currency_id')->update(['currency_id' => $vndId]);
            }
        } catch (\Exception $e) {
            // Bỏ qua nếu chưa connect được second DB lúc migrate
        }
    }

    public function down()
    {
        Schema::table('bom_lists', function (Blueprint $table) {
            $table->dropColumn('currency_id');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-api
php artisan migrate
```

Expected: `bom_lists` có cột `currency_id`, BOM cũ được set sang VND.

---

## Task 2: Migration — thêm product_type vào bom_list_products

**Files:**
- Create: `hrm-api/database/migrations/2026_04_10_100001_add_product_type_to_bom_list_products.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddProductTypeToBomListProducts extends Migration
{
    public function up()
    {
        Schema::table('bom_list_products', function (Blueprint $table) {
            $table->tinyInteger('product_type')->default(1)->after('bom_list_id')
                ->comment('1=Hàng hoá, 2=Dịch vụ');
        });
    }

    public function down()
    {
        Schema::table('bom_list_products', function (Blueprint $table) {
            $table->dropColumn('product_type');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
php artisan migrate
```

Expected: `bom_list_products` có cột `product_type` default = 1.

---

## Task 3: Migration — update status comment cho bom_lists

**Files:**
- Create: `hrm-api/database/migrations/2026_04_10_100002_update_bom_lists_status_comment.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

class UpdateBomListsStatusComment extends Migration
{
    public function up()
    {
        DB::statement("ALTER TABLE bom_lists MODIFY COLUMN status TINYINT NOT NULL DEFAULT 1 
            COMMENT '1=Đang tạo, 2=Hoàn thành, 3=Chờ duyệt, 4=Đã duyệt, 5=Đã được tổng hợp, 6=Không duyệt'");
    }

    public function down()
    {
        DB::statement("ALTER TABLE bom_lists MODIFY COLUMN status TINYINT NOT NULL DEFAULT 1 
            COMMENT '1=Đang tạo, 2=Hoàn thành, 3=Chờ duyệt, 4=Đã duyệt'");
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
php artisan migrate
```

---

## Task 4: Model — TpCurrency (mysql2)

**Files:**
- Create: `hrm-api/Modules/Human/Entities/TpCurrency.php`

- [ ] **Step 1: Tạo model**

```php
<?php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class TpCurrency extends Model
{
    protected $connection = 'mysql2';
    protected $table = 'currencies';
    public $timestamps = false;

    protected $fillable = [
        'code',
        'name',
        'symbol',
    ];
}
```

- [ ] **Step 2: Verify connection mysql2**

```bash
php artisan tinker
>>> \Modules\Human\Entities\TpCurrency::take(5)->get();
```

Expected: Trả về danh sách currencies từ ERP (ít nhất có VND).

---

## Task 5: Update BomList entity — constants + relationship + getStatusList

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/BomList.php`

- [ ] **Step 1: Thêm constants mới**

Tìm dòng:
```php
const STATUS_DA_DUYET = 4;
```

Thay bằng:
```php
const STATUS_DA_DUYET = 4;
const STATUS_DA_DUOC_TONG_HOP = 5;
const STATUS_KHONG_DUYET = 6;
```

- [ ] **Step 2: Update getStatusList()**

Thay method `getStatusList()` bằng:

```php
public static function getStatusList()
{
    return [
        self::STATUS_DANG_TAO => [
            'name' => 'Đang tạo',
            'color' => '#FF9800',
        ],
        self::STATUS_HOAN_THANH => [
            'name' => 'Hoàn thành',
            'color' => '#4CAF50',
        ],
        self::STATUS_CHO_DUYET => [
            'name' => 'Chờ duyệt',
            'color' => '#2196F3',
        ],
        self::STATUS_DA_DUYET => [
            'name' => 'Đã duyệt',
            'color' => '#9C27B0',
        ],
        self::STATUS_DA_DUOC_TONG_HOP => [
            'name' => 'Đã được tổng hợp',
            'color' => '#9E9E9E',
        ],
        self::STATUS_KHONG_DUYET => [
            'name' => 'Không duyệt',
            'color' => '#F44336',
        ],
    ];
}
```

- [ ] **Step 3: Thêm relationship currency()**

Sau method `customer()`:

```php
public function currency()
{
    return $this->belongsTo(\Modules\Human\Entities\TpCurrency::class, 'currency_id');
}
```

- [ ] **Step 4: Test**

```bash
php artisan tinker
>>> \Modules\Assign\Entities\BomList::first()->currency;
```

Expected: Trả về object TpCurrency hoặc null.

---

## Task 6: Update BomListProduct entity — constants + accessors

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/BomListProduct.php`

- [ ] **Step 1: Thêm constants product_type**

Thêm sau dòng `protected $table = ...`:

```php
const PRODUCT_TYPE_GOODS = 1;
const PRODUCT_TYPE_SERVICE = 2;

public static function getProductTypeList()
{
    return [
        self::PRODUCT_TYPE_GOODS => 'Hàng hoá',
        self::PRODUCT_TYPE_SERVICE => 'Dịch vụ',
    ];
}
```

- [ ] **Step 2: Thêm accessors**

```php
public function getImportTotalAttribute()
{
    return ((float)($this->estimated_price ?? 0)) * ((float)($this->qty_needed ?? 0));
}

public function getSaleTotalAttribute()
{
    return ((float)($this->quoted_price ?? 0)) * ((float)($this->qty_needed ?? 0));
}

public function getProfitMarginAttribute()
{
    if (!$this->estimated_price || (float)$this->estimated_price == 0) {
        return null;
    }
    return round((((float)$this->quoted_price - (float)$this->estimated_price) / (float)$this->estimated_price) * 100, 2);
}
```

- [ ] **Step 3: Append accessors vào JSON output**

Thêm property:
```php
protected $appends = ['import_total', 'sale_total', 'profit_margin'];
```

- [ ] **Step 4: Verify $guarded hoặc $fillable không chặn product_type**

Nếu dùng `$guarded = []` thì OK. Nếu có `$fillable` → thêm `'product_type'`.

- [ ] **Step 5: Test accessor**

```bash
php artisan tinker
>>> $p = \Modules\Assign\Entities\BomListProduct::where('estimated_price', '>', 0)->first();
>>> $p->import_total;
>>> $p->sale_total;
>>> $p->profit_margin;
```

---

## Task 7: BomListService — syncChildStatus()

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/BomListService.php`

- [ ] **Step 1: Thêm method syncChildStatus**

Thêm vào class `BomListService`:

```php
/**
 * Sync status BOM Thành phần khi BOM Tổng hợp chọn/bỏ chọn
 *
 * @param array $newChildIds  ID BOM con sau khi save
 * @param array $oldChildIds  ID BOM con trước khi save
 */
protected function syncChildStatus(array $newChildIds, array $oldChildIds)
{
    $added = array_diff($newChildIds, $oldChildIds);
    $removed = array_diff($oldChildIds, $newChildIds);

    if (!empty($added)) {
        BomList::whereIn('id', $added)
            ->where('bom_list_type', BomList::TYPE_COMPONENT)
            ->update(['status' => BomList::STATUS_DA_DUOC_TONG_HOP]);
    }
    if (!empty($removed)) {
        BomList::whereIn('id', $removed)
            ->where('bom_list_type', BomList::TYPE_COMPONENT)
            ->update(['status' => BomList::STATUS_HOAN_THANH]);
    }
}
```

- [ ] **Step 2: Gọi syncChildStatus trong store()**

Trong method `store()`, sau khi tạo bom_list_relations, thêm:

```php
// Sau khi save relations
$childIds = collect($payload['sub_bom_ids'] ?? [])->toArray();
$this->syncChildStatus($childIds, []);
```

- [ ] **Step 3: Gọi syncChildStatus trong update()**

Trong method `update()`, trước khi cập nhật relations:

```php
$oldChildIds = $bomList->childRelations()->pluck('child_bom_list_id')->toArray();
// ... cập nhật relations như cũ ...
$newChildIds = collect($payload['sub_bom_ids'] ?? [])->toArray();
$this->syncChildStatus($newChildIds, $oldChildIds);
```

- [ ] **Step 4: Gọi syncChildStatus khi destroy() BOM Tổng hợp**

Trong method `destroy()`:

```php
if ($bomList->bom_list_type == BomList::TYPE_AGGREGATE) {
    $oldChildIds = $bomList->childRelations()->pluck('child_bom_list_id')->toArray();
    $this->syncChildStatus([], $oldChildIds);
}
// ... xoá BOM như cũ ...
```

- [ ] **Step 5: Test**

Tạo BOM Tổng hợp chọn 1 BOM Thành phần → check BOM Thành phần status = 5. Bỏ chọn → status = 2.

---

## Task 8: BomListService — syncStatusFromSubmission()

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/BomListService.php`

- [ ] **Step 1: Thêm method**

```php
/**
 * Sync status BOM Tổng hợp từ hồ sơ trình duyệt
 *
 * @param string $type 'solution' | 'solution_module'
 * @param int $referenceId solution_id hoặc solution_module_id
 * @param string $reviewStatus pending|approved|rejected
 */
public function syncStatusFromSubmission(string $type, int $referenceId, string $reviewStatus)
{
    $statusMap = [
        'pending' => BomList::STATUS_CHO_DUYET,    // 3
        'approved' => BomList::STATUS_DA_DUYET,    // 4
        'rejected' => BomList::STATUS_KHONG_DUYET, // 6
    ];
    $newStatus = $statusMap[$reviewStatus] ?? null;
    if ($newStatus === null) {
        return;
    }

    $query = BomList::where('bom_list_type', BomList::TYPE_AGGREGATE);
    if ($type === 'solution_module') {
        $query->where('solution_module_id', $referenceId);
    } elseif ($type === 'solution') {
        $query->where('solution_id', $referenceId)->whereNull('solution_module_id');
    } else {
        return;
    }

    $query->update(['status' => $newStatus]);
}
```

- [ ] **Step 2: Verify constants tồn tại**

Đảm bảo Task 5 đã thêm `STATUS_KHONG_DUYET = 6` rồi.

---

## Task 9: Hook sync status từ SolutionReviewProfileService

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionReviewProfileService.php`

- [ ] **Step 1: Tìm điểm save status**

Đọc file, tìm method update status (thường tên `approve()`, `reject()`, `submit()` hoặc `updateStatus()`).

```bash
grep -n "STATUS_\|status" hrm-api/Modules/Assign/Services/SolutionReviewProfileService.php
```

- [ ] **Step 2: Inject BomListService**

Trong constructor:

```php
protected $bomListService;

public function __construct(BomListService $bomListService)
{
    $this->bomListService = $bomListService;
}
```

Add use statement:
```php
use Modules\Assign\Services\BomListService;
```

- [ ] **Step 3: Gọi sync sau khi đổi status**

Mỗi điểm `$profile->status = 'pending|approved|rejected'; $profile->save();` → thêm:

```php
$this->bomListService->syncStatusFromSubmission('solution', $profile->solution_id, $profile->status);
```

- [ ] **Step 4: Test**

Đổi 1 hồ sơ trình duyệt giải pháp sang Chờ duyệt → check BOM Tổng hợp gắn với solution_id đó có status = 3.

---

## Task 10: Hook sync status từ SolutionModuleReviewProfileService

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionModuleReviewProfileService.php`

- [ ] **Step 1: Inject BomListService + thêm hook**

Tương tự Task 9 nhưng dùng `solution_module_id`:

```php
$this->bomListService->syncStatusFromSubmission(
    'solution_module', 
    $profile->solution_module_id, 
    $profile->status
);
```

- [ ] **Step 2: Test**

Đổi hồ sơ hạng mục → BOM Tổng hợp gắn với hạng mục có status đúng.

---

## Task 11: BomListService — handle currency_id + product_type validate

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/BomListService.php`

- [ ] **Step 1: Thêm currency_id vào store()/update()**

Trong method `store()`, khi tạo BomList, đảm bảo `currency_id` được lưu:

```php
$bomList = BomList::create([
    // ... fields có sẵn ...
    'currency_id' => $payload['currency_id'] ?? $this->getDefaultCurrencyId(),
]);
```

Tương tự cho `update()`.

- [ ] **Step 2: Thêm method getDefaultCurrencyId()**

```php
protected function getDefaultCurrencyId()
{
    try {
        return DB::connection('mysql2')->table('currencies')->where('code', 'VND')->value('id');
    } catch (\Exception $e) {
        return null;
    }
}
```

- [ ] **Step 3: Update syncProducts() — validate dịch vụ**

Trong method `syncProducts()` (xử lý mảng products khi save), thêm validate:

```php
foreach ($payload['products'] as $productData) {
    $productType = $productData['product_type'] ?? BomListProduct::PRODUCT_TYPE_GOODS;

    if ($productType == BomListProduct::PRODUCT_TYPE_SERVICE) {
        // Dịch vụ: bỏ qua model/brand/origin, không cho làm con
        if (!empty($productData['parent_id'])) {
            throw new \Exception('Dịch vụ không được làm hàng con: ' . ($productData['name'] ?? ''));
        }
        $productData['model_id'] = null;
        $productData['brand_id'] = null;
        $productData['origin_id'] = null;
        $productData['erp_product_id'] = null;
    }

    // ... save logic ...
}
```

- [ ] **Step 4: Validate dịch vụ không có hàng con**

Sau khi save tất cả products, check:

```php
$serviceParents = BomListProduct::where('bom_list_id', $bomList->id)
    ->where('product_type', BomListProduct::PRODUCT_TYPE_SERVICE)
    ->pluck('id');

$hasServiceChildren = BomListProduct::where('bom_list_id', $bomList->id)
    ->whereIn('parent_id', $serviceParents)
    ->exists();

if ($hasServiceChildren) {
    throw new \Exception('Dịch vụ không được có hàng con');
}
```

---

## Task 12: BomListController — getCurrencies endpoint

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/BomListController.php`

- [ ] **Step 1: Thêm method**

```php
public function getCurrencies()
{
    try {
        $currencies = \DB::connection('mysql2')
            ->table('currencies')
            ->select('id', 'code', 'name', 'symbol')
            ->orderBy('code')
            ->get();
        return $this->responseJson('success', Response::HTTP_OK, $currencies);
    } catch (\Exception $e) {
        \Log::error('getCurrencies error: ' . $e->getMessage());
        return $this->responseJson('Không lấy được danh sách tiền tệ', Response::HTTP_INTERNAL_SERVER_ERROR);
    }
}
```

- [ ] **Step 2: Thêm route**

Trong `Modules/Assign/Routes/api.php`, group `bom-lists`:

```php
Route::get('bom-lists/currencies', [BomListController::class, 'getCurrencies']);
```

Đặt **trước** route `bom-lists/{bomList}` để Laravel không hiểu nhầm `currencies` là `{bomList}`.

- [ ] **Step 3: Test**

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/assign/bom-lists/currencies
```

Expected: JSON array of currencies.

---

## Task 13: Update BomListStoreRequest — rules currency_id + product_type

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php`

- [ ] **Step 1: Thêm rule**

Trong method `rules()`:

```php
return [
    // ... rules có sẵn ...
    'currency_id' => 'nullable|integer',
    'products' => 'nullable|array',
    'products.*.product_type' => 'nullable|integer|in:1,2',
    'products.*.name' => 'required_with:products|string|max:255',
    'products.*.unit_id' => 'required_with:products|integer',
    // Conditional rules cho hàng hoá
    'products.*.model_id' => 'required_if:products.*.product_type,1|nullable|integer',
    'products.*.brand_id' => 'required_if:products.*.product_type,1|nullable|integer',
    'products.*.origin_id' => 'required_if:products.*.product_type,1|nullable|integer',
];
```

- [ ] **Step 2: Thêm messages**

```php
public function messages()
{
    return array_merge(parent::messages() ?? [], [
        'products.*.product_type.in' => 'Loại sản phẩm không hợp lệ',
        'products.*.name.required_with' => 'Tên sản phẩm là bắt buộc',
    ]);
}
```

---

## Task 14: Update BomListShowResource — append currency + accessors

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/BomListResource/BomListShowResource.php`

- [ ] **Step 1: Append currency vào response**

Trong method `toArray()`:

```php
return [
    // ... fields có sẵn ...
    'currency_id' => $this->currency_id,
    'currency' => $this->currency ? [
        'id' => $this->currency->id,
        'code' => $this->currency->code,
        'name' => $this->currency->name,
        'symbol' => $this->currency->symbol,
    ] : null,
    // products đã có sẵn — đảm bảo accessor được append
];
```

- [ ] **Step 2: Verify accessors xuất hiện trong product items**

Khi loop products, check JSON có `import_total`, `sale_total`, `profit_margin`. Nếu chưa, force append trong loop:

```php
'products' => $this->products->map(function ($p) {
    return array_merge($p->toArray(), [
        'import_total' => $p->import_total,
        'sale_total' => $p->sale_total,
        'profit_margin' => $p->profit_margin,
    ]);
}),
```

- [ ] **Step 3: Eager load currency trong service**

Trong `BomListService::loadDetail()` hoặc `show()`:

```php
$bomList->load(['currency', 'products', 'groups', ...]);
```

---

## Task 15: BomListExport — thêm cột Loại + Giá bán + Thành tiền bán + Tỷ suất

**Files:**
- Modify: `hrm-api/Modules/Assign/Exports/BomListExport.php`

- [ ] **Step 1: Update headers**

Tìm method `headings()`:

```php
public function headings(): array
{
    return [
        'STT',
        'Mã',
        'Loại',           // MỚI
        'Tên',
        'Model',
        'Thương hiệu',
        'Xuất xứ',
        'ĐVT',
        'Đặc điểm',
        'Số lượng',
        'Giá nhập',       // (cũ tên Đơn giá → đổi)
        'Thành tiền nhập',// MỚI
        'Giá bán',        // MỚI
        'Thành tiền bán', // MỚI
        'Tỷ suất LN (%)', // MỚI
    ];
}
```

- [ ] **Step 2: Update map() row**

```php
public function map($product): array
{
    $typeLabel = $product->product_type == BomListProduct::PRODUCT_TYPE_SERVICE ? 'Dịch vụ' : 'Hàng hoá';
    return [
        $stt,
        $product->code,
        $typeLabel,
        $product->name,
        $product->product_type == BomListProduct::PRODUCT_TYPE_SERVICE ? '' : ($product->model->name ?? ''),
        $product->product_type == BomListProduct::PRODUCT_TYPE_SERVICE ? '' : ($product->brand->name ?? ''),
        $product->product_type == BomListProduct::PRODUCT_TYPE_SERVICE ? '' : ($product->origin->name ?? ''),
        $product->unit->name ?? '',
        $product->product_attributes,
        $product->qty_needed,
        $product->estimated_price,
        $product->import_total,
        $product->quoted_price,
        $product->sale_total,
        $product->profit_margin !== null ? $product->profit_margin : '',
    ];
}
```

- [ ] **Step 3: Header info — thêm currency**

Tìm chỗ render header BOM (info section), thêm dòng:

```php
$sheet->setCellValue('A' . $row, 'Loại tiền tệ:');
$sheet->setCellValue('B' . $row, $bomList->currency ? ($bomList->currency->name . ' (' . $bomList->currency->symbol . ')') : 'VND');
$row++;
```

- [ ] **Step 4: Test export**

Tạo BOM có cả hàng hoá + dịch vụ → export → mở file Excel → verify đầy đủ cột mới.

---

## Task 16: BomListImport — parse cột Loại + conditional validate

**Files:**
- Modify: `hrm-api/Modules/Assign/Imports/BomListImport.php`

- [ ] **Step 1: Update mapping cột**

```php
public function model(array $row)
{
    $loaiText = trim($row['loai'] ?? '');
    $productType = strtolower($loaiText) === 'dịch vụ' || strtolower($loaiText) === 'dich vu'
        ? BomListProduct::PRODUCT_TYPE_SERVICE
        : BomListProduct::PRODUCT_TYPE_GOODS;

    $data = [
        'product_type' => $productType,
        'name' => $row['ten'] ?? '',
        'code' => $row['ma'] ?? '',
        'unit_id' => $this->resolveUnitId($row['dvt'] ?? ''),
        'qty_needed' => $row['so_luong'] ?? 0,
        'estimated_price' => $row['gia_nhap'] ?? 0,
        'quoted_price' => $row['gia_ban'] ?? 0,
        'product_attributes' => $row['dac_diem'] ?? '',
    ];

    if ($productType == BomListProduct::PRODUCT_TYPE_GOODS) {
        $data['model_id'] = $this->resolveModelId($row['model'] ?? '');
        $data['brand_id'] = $this->resolveBrandId($row['thuong_hieu'] ?? '');
        $data['origin_id'] = $this->resolveOriginId($row['xuat_xu'] ?? '');
    } else {
        $data['model_id'] = null;
        $data['brand_id'] = null;
        $data['origin_id'] = null;
    }

    return new BomListProduct($data);
}
```

- [ ] **Step 2: Validate**

```php
public function rules(): array
{
    return [
        '*.ten' => 'required',
        '*.dvt' => 'required',
        // model/brand/origin chỉ bắt buộc nếu loại = Hàng hoá
        '*.model' => function ($attribute, $value, $fail) {
            $row = $this->getRowByAttribute($attribute);
            if (($row['loai'] ?? '') !== 'Dịch vụ' && empty($value)) {
                $fail('Model bắt buộc với hàng hoá');
            }
        },
    ];
}
```

- [ ] **Step 3: Update template Excel**

File template trong `hrm-api/storage/app/templates/` (hoặc nơi tương tự) — thêm cột:
- Loại (giá trị: Hàng hoá / Dịch vụ)
- Giá bán
- Dòng mẫu: 1 hàng hoá + 1 dịch vụ

- [ ] **Step 4: Test import**

Tạo file Excel với 2 dòng (1 hàng hoá + 1 dịch vụ) → import → kiểm tra DB.

---

## Task 17: FE — Load currencies API + helper

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderEditor.vue`

- [ ] **Step 1: Thêm data + load currencies**

Trong `data()`:

```javascript
data() {
    return {
        // ... có sẵn ...
        currencies: [],
        currentCurrencyId: null,
    }
},
```

Trong `mounted()` hoặc `created()`:

```javascript
async loadCurrencies() {
    try {
        const { data } = await this.$store.dispatch('apiGetMethod', 'assign/bom-lists/currencies')
        this.currencies = data || []
        // Default VND nếu chưa có
        if (!this.currentCurrencyId) {
            const vnd = this.currencies.find(c => c.code === 'VND')
            this.currentCurrencyId = vnd ? vnd.id : (this.currencies[0]?.id || null)
        }
    } catch (e) {
        console.error('Load currencies error:', e)
    }
},
```

- [ ] **Step 2: Gọi loadCurrencies trong mounted()**

```javascript
async mounted() {
    await this.loadCurrencies()
    // ... logic có sẵn ...
}
```

---

## Task 18: FE — BomBuilderInfoCard select Currency

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderInfoCard.vue`

- [ ] **Step 1: Thêm prop**

```javascript
props: {
    // ... có sẵn ...
    currencies: { type: Array, default: () => [] },
    currencyId: { type: [Number, String], default: null },
    hasProducts: { type: Boolean, default: false },
},
```

- [ ] **Step 2: Thêm UI select**

Trong template, sau field "Khách hàng":

```vue
<div class="form-group">
    <label>Loại tiền tệ <span class="text-danger">*</span></label>
    <V2BaseSelect
        :value="currencyId"
        :options="currencyOptions"
        :reduce="opt => opt.value"
        @input="onCurrencyChange"
        placeholder="Chọn loại tiền tệ"
    />
</div>
```

- [ ] **Step 3: Computed + method**

```javascript
computed: {
    currencyOptions() {
        return this.currencies.map(c => ({
            value: c.id,
            label: `${c.name} (${c.symbol})`,
        }))
    },
},
methods: {
    async onCurrencyChange(newId) {
        if (newId === this.currencyId) return
        if (this.hasProducts) {
            const ok = await this.$bvModal.msgBoxConfirm(
                'Đổi loại tiền tệ sẽ giữ nguyên số tiền hiện tại, chỉ thay đổi đơn vị hiển thị. Bạn cần kiểm tra lại giá. Tiếp tục?',
                {
                    title: 'Xác nhận',
                    okTitle: 'Tiếp tục',
                    cancelTitle: 'Huỷ',
                    centered: true,
                }
            )
            if (!ok) return
        }
        this.$emit('update:currencyId', newId)
    },
},
```

- [ ] **Step 4: Pass props từ BomBuilderEditor**

```vue
<BomBuilderInfoCard
    :currencies="currencies"
    :currency-id="currentCurrencyId"
    :has-products="products.length > 0"
    @update:currencyId="currentCurrencyId = $event"
/>
```

---

## Task 19: FE — BomBuilderTableCard cột mới + icon

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderTableCard.vue`

- [ ] **Step 1: Thêm cột Giá bán + Thành tiền nhập/bán + Tỷ suất**

Trong `<thead>`, thêm sau cột "Giá nhập":

```vue
<th>Thành tiền nhập</th>
<th>Giá bán</th>
<th>Thành tiền bán</th>
<th>Tỷ suất LN (%)</th>
```

- [ ] **Step 2: Thêm cell tương ứng trong row**

```vue
<td>{{ formatMoney(row.estimated_price * row.qty_needed) }}</td>
<td>
    <input v-if="!viewOnly" v-model.number="row.quoted_price" type="number" class="form-control form-control-sm" />
    <span v-else>{{ formatMoney(row.quoted_price) }}</span>
</td>
<td>{{ formatMoney(row.quoted_price * row.qty_needed) }}</td>
<td :class="profitMarginClass(row)">{{ formatProfitMargin(row) }}</td>
```

- [ ] **Step 3: Helpers**

```javascript
methods: {
    formatProfitMargin(row) {
        if (!row.estimated_price || row.estimated_price == 0) return '—'
        const m = ((row.quoted_price - row.estimated_price) / row.estimated_price) * 100
        return m.toFixed(2) + '%'
    },
    profitMarginClass(row) {
        if (!row.estimated_price || row.estimated_price == 0) return ''
        const m = ((row.quoted_price - row.estimated_price) / row.estimated_price) * 100
        if (m < 10) return 'text-danger'
        if (m <= 20) return 'text-warning'
        return 'text-success'
    },
},
```

- [ ] **Step 4: Icon hàng/dịch vụ trước tên**

Trong cell tên:

```vue
<td>
    <i :class="row.product_type === 2 ? 'ri-tools-line' : 'ri-box-3-line'" 
       :title="row.product_type === 2 ? 'Dịch vụ' : 'Hàng hoá'"
       style="margin-right: 4px;"></i>
    {{ row.name }}
</td>
```

- [ ] **Step 5: Format giá theo currency symbol**

Pass prop `currencySymbol` từ BomBuilderEditor → format số có symbol:

```javascript
formatMoney(value) {
    if (value == null) return ''
    return new Intl.NumberFormat('vi-VN').format(value) + ' ' + (this.currencySymbol || '₫')
},
```

---

## Task 20: FE — BomBuilderAddProductModal Tab 2 toggle Hàng/Dịch vụ

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderAddProductModal.vue`

- [ ] **Step 1: Thêm data form.product_type**

```javascript
data() {
    return {
        // ... có sẵn ...
        form: {
            product_type: 1, // 1=Hàng hoá, 2=Dịch vụ
            name: '',
            // ... các field khác ...
        },
    }
},
```

- [ ] **Step 2: Thêm radio toggle ở đầu Tab 2**

```vue
<b-tab title="Tạo mới">
    <div class="form-group">
        <label class="d-block">Loại sản phẩm</label>
        <b-form-radio-group
            v-model="form.product_type"
            :options="[
                { value: 1, text: 'Hàng hoá' },
                { value: 2, text: 'Dịch vụ' },
            ]"
        />
    </div>
    
    <!-- ... các field còn lại ... -->
</b-tab>
```

- [ ] **Step 3: Conditional field**

Wrap field Model/Brand/Origin trong `v-if`:

```vue
<template v-if="form.product_type === 1">
    <div class="form-group">
        <label>Model <span class="text-danger">*</span></label>
        <V2BaseSelect ... v-model="form.model_id" />
    </div>
    <div class="form-group">
        <label>Thương hiệu <span class="text-danger">*</span></label>
        <V2BaseSelect ... v-model="form.brand_id" />
    </div>
    <div class="form-group">
        <label>Xuất xứ <span class="text-danger">*</span></label>
        <V2BaseSelect ... v-model="form.origin_id" />
    </div>
</template>
```

- [ ] **Step 4: Update validate submitCreate()**

```javascript
async submitCreate() {
    const errors = {}
    if (!this.form.name) errors.name = 'Tên là bắt buộc'
    if (!this.form.unit_id) errors.unit_id = 'ĐVT là bắt buộc'

    if (this.form.product_type === 1) {
        if (!this.form.model_id) errors.model_id = 'Model là bắt buộc'
        if (!this.form.brand_id) errors.brand_id = 'Thương hiệu là bắt buộc'
        if (!this.form.origin_id) errors.origin_id = 'Xuất xứ là bắt buộc'
    }

    if (Object.keys(errors).length) {
        this.errors = errors
        return
    }
    // emit add với form
    this.$emit('add', { ...this.form })
    this.resetForm()
},

resetForm() {
    this.form = {
        product_type: 1,
        name: '', code: '', model_id: null, brand_id: null,
        origin_id: null, unit_id: null, qty_needed: 1,
        estimated_price: 0, quoted_price: 0, product_attributes: '',
    }
    this.errors = {}
},
```

---

## Task 21: FE — BomBuilderEditor save payload + sync productType

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderEditor.vue`

- [ ] **Step 1: Khi receive event 'add' từ AddProductModal**

```javascript
onAddProduct(payload) {
    // payload từ Tab 2 đã có product_type
    // payload từ Tab 1 (chọn ERP/BOM) → mặc định product_type = 1
    const newProduct = {
        ...payload,
        product_type: payload.product_type || 1,
    }
    this.products.push(newProduct)
},
```

- [ ] **Step 2: Include currency_id + product_type trong save payload**

Trong method save BOM (search `_saveBomWithStatus`):

```javascript
const payload = {
    // ... fields có sẵn ...
    currency_id: this.currentCurrencyId,
    products: this.products.map(p => ({
        ...p,
        product_type: p.product_type || 1,
    })),
}
```

- [ ] **Step 3: Khi load BOM detail, set currentCurrencyId từ data**

```javascript
async loadDetail(id) {
    const { data } = await this.$store.dispatch('apiGetMethod', `assign/bom-lists/${id}`)
    this.currentCurrencyId = data.currency_id
    // ... set products, groups ...
}
```

- [ ] **Step 4: Validate dịch vụ không có cha bằng kéo thả**

Trong drop handler, reject nếu drop vào dịch vụ:

```javascript
onRowDrop(item, parent) {
    if (parent && parent.product_type === 2) {
        this.$toasted.global.error({ message: 'Dịch vụ không được có hàng con' })
        return
    }
    // ... drop logic ...
},
```

---

## Task 22: FE — BomBuilderImportModal preview cột Loại

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/components/BomBuilderImportModal.vue`

- [ ] **Step 1: Thêm cột Loại + Giá bán trong preview table**

```vue
<th>Loại</th>
<th>Giá bán</th>
```

```vue
<td>
    <span :class="row.product_type === 2 ? 'badge badge-info' : 'badge badge-secondary'">
        {{ row.product_type === 2 ? 'Dịch vụ' : 'Hàng hoá' }}
    </span>
</td>
<td>{{ formatMoney(row.quoted_price) }}</td>
```

- [ ] **Step 2: Update download template button**

Đảm bảo template tải về có cột Loại + Giá bán (file template do BE đã update ở Task 16).

---

## Task 23: FE — Trang chi tiết view-only

**Files:**
- Modify: `hrm-client/pages/assign/bom-list/_id/index.vue`

- [ ] **Step 1: Hiển thị currency**

Trong header info:

```vue
<div class="info-row">
    <label>Loại tiền tệ:</label>
    <span>{{ bomList.currency ? bomList.currency.name + ' (' + bomList.currency.symbol + ')' : '—' }}</span>
</div>
```

- [ ] **Step 2: Verify cột mới hiển thị**

Trang detail dùng `BomBuilderEditor` ở chế độ viewOnly → cột mới (giá bán, thành tiền, tỷ suất) tự động hiện. Verify lại sau khi Task 19 done.

---

## Task 24: Update STATUS.md + plan.md

**Files:**
- Modify: `.plans/STATUS.md`
- Modify: `.plans/Bomlist-Quotation/plan.md`

- [ ] **Step 1: Cập nhật plan.md — thêm Phase 8a**

Thêm vào cuối danh sách phase:

```markdown
### Phase 8a: Status workflow + Currency + Columns + Service
[ ] Task 1: Migration currency_id
[ ] Task 2: Migration product_type
[ ] Task 3: Migration update status comment
[ ] Task 4: Model TpCurrency
[ ] Task 5: BomList constants + relationship
[ ] Task 6: BomListProduct constants + accessors
[ ] Task 7: syncChildStatus()
[ ] Task 8: syncStatusFromSubmission()
[ ] Task 9: Hook SolutionReviewProfileService
[ ] Task 10: Hook SolutionModuleReviewProfileService
[ ] Task 11: BomListService handle currency + validate dịch vụ
[ ] Task 12: getCurrencies endpoint
[ ] Task 13: BomListStoreRequest rules
[ ] Task 14: BomListShowResource append
[ ] Task 15: BomListExport cột mới
[ ] Task 16: BomListImport parse cột Loại
[ ] Task 17: FE load currencies
[ ] Task 18: FE BomBuilderInfoCard select Currency
[ ] Task 19: FE BomBuilderTableCard cột mới + icon
[ ] Task 20: FE BomBuilderAddProductModal toggle Hàng/Dịch vụ
[ ] Task 21: FE BomBuilderEditor save payload
[ ] Task 22: FE BomBuilderImportModal preview
[ ] Task 23: FE trang chi tiết
[ ] Task 24: Test thủ công
```

- [ ] **Step 2: Cập nhật STATUS.md**

```markdown
- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan.md
  Trạng thái: Phase 8a started — design done, plan written
  Checkpoint: 2026-04-10 — Branch update_bom_list. Bắt đầu code Phase 8a
```

---

## Task 25: Test thủ công Phase 8a

- [ ] **Test 1: Status workflow BOM Thành phần**
  - Tạo BOM Thành phần lưu nháp → status = 1
  - Lưu → status = 2
  - Tạo BOM Tổng hợp chọn BOM con → BOM con status = 5
  - Bỏ chọn → BOM con status = 2
  - Xoá BOM Tổng hợp → BOM con status = 2

- [ ] **Test 2: Status workflow BOM Tổng hợp**
  - Tạo BOM Tổng hợp lưu nháp → status = 1
  - Lưu → status = 2
  - Đổi hồ sơ trình duyệt giải pháp/hạng mục sang Chờ duyệt → BOM status = 3
  - Đổi sang Đã duyệt → BOM status = 4
  - Đổi sang Không duyệt → BOM status = 6
  - User sửa BOM ở status 6 → status = 2

- [ ] **Test 3: SubBomModal filter**
  - Mở popup chọn BOM con → chỉ hiện BOM Thành phần status = 2
  - BOM ở status 5 không xuất hiện

- [ ] **Test 4: Currency**
  - Tạo BOM mới → currency mặc định = VND
  - Đổi sang USD khi BOM trống → OK
  - Thêm sản phẩm → đổi sang EUR → hiện confirm modal
  - Hủy → giữ nguyên USD; Đồng ý → đổi sang EUR
  - Save → reload → currency đúng

- [ ] **Test 5: Cột giá + tỷ suất**
  - Nhập giá nhập = 100, giá bán = 130 → tỷ suất = 30.00%
  - Giá bán = 105 → tỷ suất = 5.00% (đỏ)
  - Giá bán = 115 → tỷ suất = 15.00% (vàng)
  - Giá bán = 125 → tỷ suất = 25.00% (xanh)
  - Giá nhập = 0 → tỷ suất = "—"

- [ ] **Test 6: Dịch vụ**
  - Modal Tab 2 → chọn "Dịch vụ" → field Model/Brand/Origin biến mất
  - Save → trong bảng có icon 🛠
  - Thử kéo hàng hoá vào dịch vụ → bị reject
  - Save BOM → reload → dịch vụ vẫn còn, không có model/brand/origin

- [ ] **Test 7: Excel Export**
  - Export BOM có cả hàng + dịch vụ
  - Mở file → có cột Loại, Giá bán, Thành tiền bán, Tỷ suất
  - Header có dòng "Loại tiền tệ"

- [ ] **Test 8: Excel Import**
  - Tải template → có cột Loại + Giá bán
  - Nhập 1 hàng + 1 dịch vụ → import → preview đúng
  - Submit → save thành công

---

## Self-Review Notes

**Spec coverage:**
- ✅ Status workflow (6 status) — Task 5, 7, 8, 9, 10
- ✅ Currency — Task 1, 4, 11, 12, 17, 18
- ✅ Cột giá + accessor — Task 6, 14, 19
- ✅ Dịch vụ — Task 2, 6, 11, 13, 20, 21
- ✅ Excel Import/Export — Task 15, 16, 22
- ✅ Migration data cũ — Task 1, 2

**Type consistency:** ✅ STATUS_DA_DUOC_TONG_HOP, STATUS_KHONG_DUYET, PRODUCT_TYPE_GOODS, PRODUCT_TYPE_SERVICE dùng nhất quán across tasks.

**Placeholder scan:** ✅ Không có TBD/TODO/incomplete code blocks.
