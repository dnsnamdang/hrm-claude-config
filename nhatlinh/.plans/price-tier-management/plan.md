# Quản lý Bảng giá (price-tier-management) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans để thực thi task-by-task. Steps dùng checkbox (`- [ ]`).

**Goal:** Thay cơ chế cột giá cứng (`price_p3/p5/p7/p10`) bằng danh mục **Bảng giá** động (`price_tiers`: name + % + status). Hàng hoá chỉ nhập P0 (NET); BE tự tính & lưu snapshot giá các cấp (`product_unit_prices`). Có lịch sử sửa đổi bảng giá + nút tính lại hàng loạt.

**Architecture:** 3 bảng mới (`price_tiers`, `price_tier_histories`, `product_unit_prices`) + drop 4 cột khỏi `product_units`. Danh mục Bảng giá copy pattern Manufacturer (CRUD + lock/unlock, KHÔNG import/export, KHÔNG phân quyền cấp). Giá cấp = `P0 × (1 + percent/100)`, snapshot lúc lưu hàng hoá. FE: 1 menu + 1 list page + modal + modal lịch sử + nút tính lại; sửa ProductForm render cột giá động.

**Tech Stack:** Laravel 8 (PHP), Nuxt 2 (Vue 2), Bootstrap-Vue, spatie/permission, dayjs.

**Spec:** `docs/superpowers/specs/2026-06-26-price-tier-management-design.md`

## Global Constraints
- Công thức giá cấp: `price = round(price_p0 × (1 + percent/100), 2)`.
- `percent` decimal(8,2) ≥ 0; `price_*` decimal(15,2).
- Trạng thái hiển thị: BE trả `status_name` + `status_color` (trait `HasStatusBadge`), FE chỉ render `V2BaseBadge`. KHÔNG map text/màu ở FE.
- Validate: BE rethrow `ValidationException`; FE hiện lỗi inline (`is-invalid` + `invalid-feedback`, flag `touched`).
- Danh mục Bảng giá **dùng chung** (không lọc theo company/department).
- Route thao tác dữ liệu gắn `checkPermission:Quản lý danh mục bảng giá`; route xem gắn `checkPermission:Xem danh mục bảng giá`.
- Theo skill `button-convention`, `modal-popup` khi làm FE.

**Lưu ý môi trường:**
- KHÔNG có test tự động → verify bằng `php artisan migrate`, `php -l`, `tinker`, kiểm tra UI/compile.
- Repo API: `nhatlinh-api/` (chạy artisan tại đây). FE: `nhatlinh-client/`.
- **KHÔNG commit/push git.** KHÔNG đọc vendor/, node_modules/.
- **File template để copy** (đọc khi implement):
  - BE: `Modules/Category/{Entities/Manufacturer.php, Http/Controllers/Api/V1/ManufacturerController.php, Http/Requests/ManufacturerRequest.php, Services/ManufacturerService.php, Transformers/ManufacturerResource/*, Routes/api.php}`, `Entities/Concerns/HasStatusBadge.php`.
  - FE: `pages/category/manufacturers/{index.vue, AddManufacturerModal.vue}`, `components/default-menu/category.js`, store axios calls (xem 1 màn danh mục có sẵn).
  - Product (Phase 2): `Modules/Category/{Services/ProductService.php, Entities/ProductUnit.php, Transformers/ProductResource/DetailProductResource.php}`, `pages/category/products/components/ProductForm.vue`.

## File Structure
| File | Trách nhiệm |
|------|-------------|
| `Database/Migrations/2026_06_26_000001_create_price_tiers_table.php` | Bảng cấp giá |
| `Database/Migrations/2026_06_26_000002_create_price_tier_histories_table.php` | Lịch sử cấp giá |
| `Database/Migrations/2026_06_26_000003_create_product_unit_prices_table.php` | Snapshot giá cấp theo unit |
| `Database/Migrations/2026_06_26_000004_drop_price_columns_from_product_units.php` | Drop price_p3/p5/p7/p10 |
| `Entities/{PriceTier,PriceTierHistory,ProductUnitPrice}.php` | Models mới |
| `Entities/ProductUnit.php` | Sửa: bỏ field cũ + relation prices() |
| `Http/Requests/PriceTierRequest.php` | Validate |
| `Services/PriceTierService.php` | CRUD + history + recalc |
| `Services/ProductService.php` | Sửa syncProductUnits → snapshot |
| `Transformers/PriceTierResource/{PriceTierResource,DetailPriceTierResource,PriceTierHistoryResource}.php` | API output |
| `Transformers/ProductResource/DetailProductResource.php` | Sửa: tier_prices |
| `Http/Controllers/Api/V1/PriceTierController.php` | Endpoints |
| `Routes/api.php` | Routes (sửa) |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | 2 permission 1113-1114 (sửa) |
| `Database/Seeders/*` seeder 50 hàng hoá TBTH | Sửa: bỏ price_p3.. (Phase 2) |
| FE `pages/category/price-tiers/{index.vue, AddPriceTierModal.vue, PriceTierHistoryModal.vue}` | Màn bảng giá |
| FE `pages/category/products/components/ProductForm.vue` | Sửa: cột giá động |
| FE `components/default-menu/category.js` | Menu (sửa) |

---

## Phase 1: Danh mục Bảng giá

### Task 1: Migration `price_tiers` + `price_tier_histories`

**Files:**
- Create `nhatlinh-api/Modules/Category/Database/Migrations/2026_06_26_000001_create_price_tiers_table.php`
- Create `nhatlinh-api/Modules/Category/Database/Migrations/2026_06_26_000002_create_price_tier_histories_table.php`

- [x] **Step 1:** Tạo migration `price_tiers`:
```php
<?php
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreatePriceTiersTable extends Migration
{
    public function up()
    {
        Schema::create('price_tiers', function (Blueprint $table) {
            $table->id();
            $table->string('code', 50)->unique();
            $table->string('name', 255);
            $table->decimal('percent', 8, 2)->default(0);
            $table->integer('status')->default(1);
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->timestamps();
        });
    }
    public function down() { Schema::dropIfExists('price_tiers'); }
}
```
- [x] **Step 2:** Tạo migration `price_tier_histories`:
```php
<?php
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreatePriceTierHistoriesTable extends Migration
{
    public function up()
    {
        Schema::create('price_tier_histories', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('price_tier_id');
            $table->string('action', 20)->default('update'); // create|update|delete
            $table->string('old_name')->nullable();
            $table->string('new_name')->nullable();
            $table->decimal('old_percent', 8, 2)->nullable();
            $table->decimal('new_percent', 8, 2)->nullable();
            $table->unsignedBigInteger('changed_by')->nullable();
            $table->timestamps();
            $table->foreign('price_tier_id')->references('id')->on('price_tiers')->onDelete('cascade');
        });
    }
    public function down() { Schema::dropIfExists('price_tier_histories'); }
}
```
- [x] **Step 3:** Run `php artisan migrate`. Expected: 2 migrations Migrated.
- [x] **Step 4:** Verify `php artisan tinker --execute="echo Schema::hasTable('price_tiers')&&Schema::hasTable('price_tier_histories')?'OK':'NO';"` → OK.

### Task 2: Entity `PriceTier` + `PriceTierHistory`

**Files:**
- Create `Modules/Category/Entities/PriceTier.php`
- Create `Modules/Category/Entities/PriceTierHistory.php`

**Interfaces:**
- Produces: `PriceTier::STATUS_ACTIVE=1`, `STATUS_INACTIVE=2`; `PriceTier::getNextCode(): string`; `PriceTier::isCanEdit()`, `isCanDelete()`; relations `histories()`, `productUnitPrices()`.

- [x] **Step 1:** Đọc `Modules/Category/Entities/Manufacturer.php` làm mẫu (BaseModel, HasStatusBadge, created/updated employee accessors, isCanEdit/Lock/Unlock). Tạo `PriceTier`:
```php
<?php

namespace Modules\Category\Entities;

use App\Models\BaseModel;
use Modules\Human\Entities\Employee;

class PriceTier extends BaseModel
{
    use \Modules\Category\Entities\Concerns\HasStatusBadge;

    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 2;

    protected $fillable = [
        'code', 'name', 'percent', 'status',
        'created_by', 'updated_by', 'company_id', 'department_id', 'part_id',
        'created_at', 'updated_at',
    ];

    public function updatedByEmployee() { return $this->belongsTo(Employee::class, 'updated_by'); }
    public function createdByEmployee() { return $this->belongsTo(Employee::class, 'created_by'); }

    public function getEmployeeUpdateNameAttribute()
    {
        return $this->updatedByEmployee && $this->updatedByEmployee->info
            ? $this->updatedByEmployee->info->code . ' - ' . $this->updatedByEmployee->info->fullname : null;
    }
    public function getEmployeeCreateNameAttribute()
    {
        return $this->createdByEmployee && $this->createdByEmployee->info
            ? $this->createdByEmployee->info->code . ' - ' . $this->createdByEmployee->info->fullname : null;
    }

    public function histories()
    {
        return $this->hasMany(PriceTierHistory::class, 'price_tier_id')->orderByDesc('id');
    }

    public function productUnitPrices()
    {
        return $this->hasMany(ProductUnitPrice::class, 'price_tier_id');
    }

    public function isCanEdit() { return $this->status == self::STATUS_ACTIVE; }
    public function isCodeEditable() { return false; } // mã tự sinh
    public function isCanLockUpdate() { return true; }
    public function isCanUnlockUpdate() { return true; }

    // Chỉ xoá khi chưa áp vào hàng hoá nào (chưa có snapshot)
    public function isCanDelete() { return $this->productUnitPrices()->count() === 0; }

    // Mã tự sinh BG.0001, BG.0002...
    public static function getNextCode(): string
    {
        $last = static::where('code', 'like', 'BG.%')->orderByRaw('CAST(SUBSTRING(code, 4) AS UNSIGNED) DESC')->first();
        $next = $last ? ((int) substr($last->code, 3)) + 1 : 1;
        return 'BG.' . str_pad($next, 4, '0', STR_PAD_LEFT);
    }
}
```
- [x] **Step 2:** Tạo `PriceTierHistory`:
```php
<?php

namespace Modules\Category\Entities;

use App\Models\BaseModel;
use Modules\Human\Entities\Employee;

class PriceTierHistory extends BaseModel
{
    protected $fillable = [
        'price_tier_id', 'action', 'old_name', 'new_name',
        'old_percent', 'new_percent', 'changed_by',
    ];

    public function changedByEmployee() { return $this->belongsTo(Employee::class, 'changed_by'); }

    public function getChangedByNameAttribute()
    {
        return $this->changedByEmployee && $this->changedByEmployee->info
            ? $this->changedByEmployee->info->code . ' - ' . $this->changedByEmployee->info->fullname : null;
    }
}
```
- [x] **Step 3:** Verify `php -l` 2 file → No syntax errors. (Nếu `BaseModel` không có ở namespace đó → kiểm tra `use App\Models\BaseModel;` giống Manufacturer.)

### Task 3: Request `PriceTierRequest`

**Files:** Create `Modules/Category/Http/Requests/PriceTierRequest.php`

- [x] **Step 1:** Đọc `ManufacturerRequest.php` làm mẫu. **Extend `BaseRequest`** (`Modules\Training\Http\Requests\BaseRequest`) — class này có `failedValidation` custom trả `{code, errors}` 422 mà FE dựa vào để hiện lỗi inline; KHÔNG dùng `FormRequest` thẳng (sẽ trả sai format). Tạo:
```php
<?php

namespace Modules\Category\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;

class PriceTierRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'percent' => 'required|numeric|min:0',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => 'Vui lòng nhập tên bảng giá',
            'percent.required' => 'Vui lòng nhập phần trăm',
            'percent.numeric' => 'Phần trăm phải là số',
            'percent.min' => 'Phần trăm không được âm',
        ];
    }
}
```
- [x] **Step 2:** `php -l` → OK.

### Task 4: Service `PriceTierService` (CRUD + history)

**Files:** Create `Modules/Category/Services/PriceTierService.php`

**Interfaces:**
- Produces: `index(Request)`, `getAll(Request)`, `updateOrCreate(PriceTierRequest)`, `show(PriceTier)`, `destroy(PriceTier)`, `lock(PriceTier)`, `unlock(PriceTier)`, `histories(PriceTier)`, `recalcAllProducts(): int` (Task 11).

- [x] **Step 1:** Đọc `ManufacturerService.php` làm mẫu cho index/getAll/lock/unlock/destroy. Tạo `PriceTierService` với:
  - `index`: filter `code` (like), `keyword` (like name/code), `status`; orderByDesc id; paginate. KHÔNG lọc company/department.
  - `getAll`: trả các cấp `status = ACTIVE` (dùng cho ProductForm).
  - `updateOrCreate`: nếu không có id → create (code = `PriceTier::getNextCode()`, status=ACTIVE, created_by=auth) + ghi history action `create`. Nếu có id → cập nhật, nếu `name` hoặc `percent` đổi → ghi history action `update` (old/new). Code KHÔNG đổi.
  - `destroy`: nếu `!isCanDelete()` → throw ValidationException("Bảng giá đã áp vào hàng hoá, không thể xoá"). Ngược lại ghi history `delete` rồi xoá.
  - `lock`/`unlock`: set status INACTIVE/ACTIVE.
  - `histories`: trả `$priceTier->histories`.
```php
<?php

namespace Modules\Category\Services;

use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Modules\Category\Entities\PriceTier;
use Modules\Category\Entities\PriceTierHistory;
use Modules\Category\Http\Requests\PriceTierRequest;

class PriceTierService
{
    public function index(Request $request)
    {
        $query = PriceTier::query();
        if (isset($request->code)) {
            $query->where('code', 'like', '%' . $request->code . '%');
        }
        if (isset($request->keyword)) {
            $kw = $request->keyword;
            $query->where(function ($q) use ($kw) {
                $q->where('name', 'like', '%' . $kw . '%')->orWhere('code', 'like', '%' . $kw . '%');
            });
        }
        if (isset($request->status) && $request->status !== '') {
            $query->where('status', $request->status);
        }
        return $query->orderByDesc('id')->paginate($request->per_page ?? 20);
    }

    public function getAll(Request $request)
    {
        return PriceTier::where('status', PriceTier::STATUS_ACTIVE)->orderBy('id')->get();
    }

    public function updateOrCreate(PriceTierRequest $request)
    {
        $userId = auth()->id();
        $data = [
            'name' => trim($request->name),
            'percent' => $request->percent,
        ];

        if ($request->id) {
            $tier = PriceTier::findOrFail($request->id);
            $nameChanged = $tier->name !== $data['name'];
            $percentChanged = (float) $tier->percent !== (float) $data['percent'];
            if ($nameChanged || $percentChanged) {
                PriceTierHistory::create([
                    'price_tier_id' => $tier->id,
                    'action' => 'update',
                    'old_name' => $tier->name,
                    'new_name' => $data['name'],
                    'old_percent' => $tier->percent,
                    'new_percent' => $data['percent'],
                    'changed_by' => $userId,
                ]);
            }
            $tier->update(array_merge($data, ['updated_by' => $userId]));
            return $tier;
        }

        $tier = PriceTier::create(array_merge($data, [
            'code' => PriceTier::getNextCode(),
            'status' => PriceTier::STATUS_ACTIVE,
            'created_by' => $userId,
            'updated_by' => $userId,
        ]));
        PriceTierHistory::create([
            'price_tier_id' => $tier->id,
            'action' => 'create',
            'new_name' => $tier->name,
            'new_percent' => $tier->percent,
            'changed_by' => $userId,
        ]);
        return $tier;
    }

    public function show(PriceTier $priceTier) { return $priceTier; }

    public function destroy(PriceTier $priceTier)
    {
        if (!$priceTier->isCanDelete()) {
            throw ValidationException::withMessages([
                'id' => 'Bảng giá đã áp vào hàng hoá, không thể xoá. Hãy khoá thay vì xoá.',
            ]);
        }
        PriceTierHistory::create([
            'price_tier_id' => $priceTier->id,
            'action' => 'delete',
            'old_name' => $priceTier->name,
            'old_percent' => $priceTier->percent,
            'changed_by' => auth()->id(),
        ]);
        $priceTier->delete();
    }

    public function lock(PriceTier $priceTier)
    {
        $priceTier->update(['status' => PriceTier::STATUS_INACTIVE, 'updated_by' => auth()->id()]);
        return $priceTier;
    }

    public function unlock(PriceTier $priceTier)
    {
        $priceTier->update(['status' => PriceTier::STATUS_ACTIVE, 'updated_by' => auth()->id()]);
        return $priceTier;
    }

    public function histories(PriceTier $priceTier) { return $priceTier->histories; }
}
```
- [x] **Step 2:** `php -l` → OK. (Phương thức `recalcAllProducts()` thêm ở Task 11.)

### Task 5: Resources `PriceTier`

**Files:**
- Create `Modules/Category/Transformers/PriceTierResource/PriceTierResource.php`
- Create `Modules/Category/Transformers/PriceTierResource/DetailPriceTierResource.php`
- Create `Modules/Category/Transformers/PriceTierResource/PriceTierHistoryResource.php`

- [x] **Step 1:** Đọc `Transformers/ManufacturerResource/*` làm mẫu. `PriceTierResource` (list):
```php
<?php

namespace Modules\Category\Transformers\PriceTierResource;

use Illuminate\Http\Resources\Json\JsonResource;

class PriceTierResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'percent' => $this->percent,
            'status' => $this->status,
            'status_name' => $this->status_name,
            'status_color' => $this->status_color,
            'employee_create_name' => $this->employee_create_name,
            'employee_update_name' => $this->employee_update_name,
            'is_can_edit' => $this->isCanEdit(),
            'is_can_delete' => $this->isCanDelete(),
            'created_at' => optional($this->created_at)->format('d/m/Y H:i'),
            'updated_at' => optional($this->updated_at)->format('d/m/Y H:i'),
        ];
    }
}
```
- [x] **Step 2:** `DetailPriceTierResource` = giống list (đủ field cho form sửa). `PriceTierHistoryResource`:
```php
<?php

namespace Modules\Category\Transformers\PriceTierResource;

use Illuminate\Http\Resources\Json\JsonResource;

class PriceTierHistoryResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'action' => $this->action,
            'old_name' => $this->old_name,
            'new_name' => $this->new_name,
            'old_percent' => $this->old_percent,
            'new_percent' => $this->new_percent,
            'changed_by_name' => $this->changed_by_name,
            'created_at' => optional($this->created_at)->format('d/m/Y H:i'),
        ];
    }
}
```
- [x] **Step 3:** `php -l` 3 file → OK.

### Task 6: Controller `PriceTierController`

**Files:** Create `Modules/Category/Http/Controllers/Api/V1/PriceTierController.php`

- [x] **Step 1:** Đọc `ManufacturerController.php` làm mẫu (cách trả response, dùng Resource, bắt route-model-binding). Tạo controller với actions: `index, getAll, updateOrCreate, show, update, delete, lock, unlock, histories`. `update` có thể dùng chung `updateOrCreate` (gán id từ route) hoặc gọi service. Wrap trả về `PriceTierResource`/`DetailPriceTierResource`/`PriceTierHistoryResource::collection`. KHÔNG catch chung Exception (để ValidationException bubble).
- [x] **Step 2:** `php -l` → OK.

### Task 7: Routes + Permission

**Files:**
- Modify `Modules/Category/Routes/api.php`
- Modify `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [x] **Step 1:** Thêm 2 permission vào seeder (sau id 1112), group "Danh mục chung", type 8:
```php
Permission::create(['id' => 1113, 'guard_name' => 'api', 'name' => 'Quản lý danh mục bảng giá', 'display_name' => 'Quản lý danh mục bảng giá', 'group' => 'Danh mục chung', 'type' => 8]);
Permission::create(['id' => 1114, 'guard_name' => 'api', 'name' => 'Xem danh mục bảng giá', 'display_name' => 'Xem danh mục bảng giá', 'group' => 'Danh mục chung', 'type' => 8]);
```
- [x] **Step 2:** Thêm group route `price-tiers` trong `Routes/api.php` (theo mẫu `manufacturers`, KHÔNG có import/export):
```php
Route::group(['prefix' => '/price-tiers'], function () {
    Route::get('/', [PriceTierController::class, 'index'])->middleware('checkPermission:Xem danh mục bảng giá');
    Route::get('/getAll', [PriceTierController::class, 'getAll']);
    Route::post('/recalc-products', [PriceTierController::class, 'recalcProducts'])->middleware('checkPermission:Quản lý danh mục bảng giá'); // Phase 3
    Route::post('/', [PriceTierController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục bảng giá');
    Route::put('/{priceTier}', [PriceTierController::class, 'update'])->middleware('checkPermission:Quản lý danh mục bảng giá');
    Route::get('/{priceTier}', [PriceTierController::class, 'show'])->middleware('checkPermission:Xem danh mục bảng giá');
    Route::get('/{priceTier}/histories', [PriceTierController::class, 'histories'])->middleware('checkPermission:Xem danh mục bảng giá');
    Route::delete('/{priceTier}', [PriceTierController::class, 'delete'])->middleware('checkPermission:Quản lý danh mục bảng giá');
    Route::get('/{priceTier}/lock', [PriceTierController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục bảng giá');
    Route::get('/{priceTier}/unlock', [PriceTierController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục bảng giá');
});
```
> Lưu ý: route `recalc-products` đặt TRƯỚC `/{priceTier}` để không bị nuốt bởi route-model-binding. Action `recalcProducts` của controller thêm ở Phase 3 (Task 11) — Step này khai báo route trước, nếu chạy thử Phase 1 thì comment dòng đó lại.
- [x] **Step 3:** Đảm bảo `use Modules\Category\Http\Controllers\Api\V1\PriceTierController;` ở đầu `Routes/api.php`.
- [x] **Step 4:** Verify: php -l 2 file → No syntax errors. Route:list bị lỗi pre-existing (DecisionController namespace sai ở module Decision, không liên quan Task 7). Xác nhận 9 route price-tiers có mặt trong api.php qua grep (index, getAll, updateOrCreate, update, show, histories, lock, unlock, delete); recalc-products đã comment Phase 3.

### Task 8: FE — Menu + List page Bảng giá

**Files:**
- Modify `nhatlinh-client/components/default-menu/category.js`
- Create `nhatlinh-client/pages/category/price-tiers/index.vue`
- Create `nhatlinh-client/pages/category/price-tiers/AddPriceTierModal.vue`
- Create `nhatlinh-client/pages/category/price-tiers/PriceTierHistoryModal.vue`

- [x] **Step 1:** Thêm menu item "Bảng giá" vào `category.js` (đọc cách đăng ký menu manufacturers, kèm `permission`/`isShow` theo quyền "Xem danh mục bảng giá" — theo pattern route-guard đã làm ở quotation).
- [x] **Step 2:** Đọc `pages/category/manufacturers/index.vue` làm mẫu. Tạo `index.vue`: list table (cột Mã, Tên, %, Trạng thái = `V2BaseBadge :color="item.status_color"`, Người tạo/sửa, Thao tác), filter keyword + status, nút Thêm/Sửa/Khoá/Mở khoá/Xoá + nút **Lịch sử** mỗi dòng + nút **"Tính lại giá hàng hoá"** trên toolbar (Phase 3 sẽ nối action). Theo skill `button-convention`.
- [x] **Step 3:** Tạo `AddPriceTierModal.vue` (đọc `AddManufacturerModal.vue` mẫu): input `name`, `percent` (number/percent), validate inline (`is-invalid` + `invalid-feedback`, flag `touched`). Mã hiển thị read-only (server sinh, khi thêm mới có thể ẩn). Theo skill `modal-popup`.
- [x] **Step 4:** Tạo `PriceTierHistoryModal.vue`: bảng lịch sử (Hành động, Tên cũ→mới, % cũ→mới, Người sửa, Thời gian) load từ `GET price-tiers/{id}/histories`.
- [x] **Step 5:** Thêm store/axios calls cho price-tiers (index/getAll/store/update/delete/lock/unlock/histories). Verify FE compile sạch (`npm run dev` hoặc build), test UI: CRUD + khoá + lịch sử.

---

## Phase 2: Đổi cấu trúc giá hàng hoá

### Task 9: Migration product price + Entity ProductUnitPrice + sửa ProductUnit

**Files:**
- Create `Database/Migrations/2026_06_26_000003_create_product_unit_prices_table.php`
- Create `Database/Migrations/2026_06_26_000004_drop_price_columns_from_product_units.php`
- Create `Modules/Category/Entities/ProductUnitPrice.php`
- Modify `Modules/Category/Entities/ProductUnit.php`

**Interfaces:**
- Produces: `ProductUnitPrice` fillable `product_unit_id, price_tier_id, percent, price`; relation `ProductUnit::prices()`.

- [x] **Step 1:** Migration `product_unit_prices`:
```php
<?php
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateProductUnitPricesTable extends Migration
{
    public function up()
    {
        Schema::create('product_unit_prices', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('product_unit_id');
            $table->unsignedBigInteger('price_tier_id');
            $table->decimal('percent', 8, 2)->default(0);
            $table->decimal('price', 15, 2)->default(0);
            $table->timestamps();
            $table->foreign('product_unit_id')->references('id')->on('product_units')->onDelete('cascade');
            $table->foreign('price_tier_id')->references('id')->on('price_tiers')->onDelete('cascade');
            $table->unique(['product_unit_id', 'price_tier_id']);
        });
    }
    public function down() { Schema::dropIfExists('product_unit_prices'); }
}
```
- [x] **Step 2:** Migration drop cột:
```php
<?php
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class DropPriceColumnsFromProductUnits extends Migration
{
    public function up()
    {
        Schema::table('product_units', function (Blueprint $table) {
            $table->dropColumn(['price_p3', 'price_p5', 'price_p7', 'price_p10']);
        });
    }
    public function down()
    {
        Schema::table('product_units', function (Blueprint $table) {
            $table->decimal('price_p3', 15, 2)->default(0);
            $table->decimal('price_p5', 15, 2)->default(0);
            $table->decimal('price_p7', 15, 2)->default(0);
            $table->decimal('price_p10', 15, 2)->default(0);
        });
    }
}
```
- [x] **Step 3:** Tạo `ProductUnitPrice`:
```php
<?php

namespace Modules\Category\Entities;

use Illuminate\Database\Eloquent\Model;

class ProductUnitPrice extends Model
{
    protected $table = 'product_unit_prices';
    protected $fillable = ['product_unit_id', 'price_tier_id', 'percent', 'price'];

    public function productUnit() { return $this->belongsTo(ProductUnit::class, 'product_unit_id'); }
    public function priceTier() { return $this->belongsTo(PriceTier::class, 'price_tier_id'); }
}
```
- [x] **Step 4:** Sửa `ProductUnit.php`: bỏ `price_p3/p5/p7/p10` khỏi `$fillable`; thêm relation:
```php
public function prices()
{
    return $this->hasMany(ProductUnitPrice::class, 'product_unit_id');
}
```
- [x] **Step 5:** `php artisan migrate` → 2 migrations OK. `php -l` các entity → OK. Verify cột đã drop: `php artisan tinker --execute="echo Schema::hasColumn('product_units','price_p3')?'STILL':'DROPPED';"` → DROPPED.

### Task 10: Sửa ProductService.syncProductUnits → snapshot + Resource

**Files:**
- Modify `Modules/Category/Services/ProductService.php`
- Modify `Modules/Category/Transformers/ProductResource/DetailProductResource.php`
- Modify seeder 50 hàng hoá TBTH (tìm file seeder set `price_p3..`)

**Interfaces:**
- Consumes: `PriceTier::where('status', ACTIVE)`, `ProductUnitPrice`, `ProductUnit::prices()`.

- [x] **Step 1:** Sửa `syncProductUnits()`: bỏ `price_p3/p5/p7/p10`; sau khi tạo mỗi `ProductUnit`, tính snapshot từ các tier ACTIVE. Thêm helper `syncUnitPrices(ProductUnit $pu)`:
```php
private function syncProductUnits(Product $product, array $units)
{
    $product->productUnits()->delete(); // cascade xoá product_unit_prices

    $tiers = \Modules\Category\Entities\PriceTier::where('status', \Modules\Category\Entities\PriceTier::STATUS_ACTIVE)->get();

    foreach ($units as $unitData) {
        $isBase = ($unitData['is_base_unit'] ?? 0) == 1;
        $pu = ProductUnit::create([
            'product_id' => $product->id,
            'unit_id' => $unitData['unit_id'],
            'is_base_unit' => $isBase ? 1 : 0,
            'conversion_rate' => $isBase ? 1 : ($unitData['conversion_rate'] ?? 1),
            'price_p0' => $unitData['price_p0'] ?? 0,
        ]);
        $this->syncUnitPrices($pu, $tiers);
    }
}

private function syncUnitPrices(ProductUnit $pu, $tiers)
{
    $p0 = (float) $pu->price_p0;
    foreach ($tiers as $tier) {
        \Modules\Category\Entities\ProductUnitPrice::updateOrCreate(
            ['product_unit_id' => $pu->id, 'price_tier_id' => $tier->id],
            ['percent' => $tier->percent, 'price' => round($p0 * (1 + $tier->percent / 100), 2)]
        );
    }
}
```
> `$product->productUnits()->delete()` xoá unit cũ → cascade xoá snapshot (FK onDelete cascade). Mỗi lần lưu tính lại toàn bộ theo tier ACTIVE hiện tại → đồng thời dọn tier đã khoá.
- [x] **Step 2:** Sửa `DetailProductResource.php` (và list resource nếu trả product_units): bỏ `price_p3/p5/p7/p10`, thêm `tier_prices`:
```php
'product_units' => $this->productUnits->map(function ($pu) {
    return [
        'id' => $pu->id,
        'unit_id' => $pu->unit_id,
        'is_base_unit' => $pu->is_base_unit,
        'conversion_rate' => $pu->conversion_rate,
        'price_p0' => $pu->price_p0,
        'tier_prices' => $pu->prices->map(function ($pp) {
            return [
                'price_tier_id' => $pp->price_tier_id,
                'tier_name' => optional($pp->priceTier)->name,
                'percent' => $pp->percent,
                'price' => $pp->price,
            ];
        }),
    ];
}),
```
> Eager load tránh N+1: trong ProductService load `productUnits.prices.priceTier` khi show.
- [x] **Step 3:** Sửa seeder 50 hàng hoá TBTH: bỏ các key `price_p3/p5/p7/p10`, chỉ giữ `price_p0`. (Tìm bằng `grep -rn "price_p3" nhatlinh-api/Modules/Category/Database/Seeders/`.) → Seeder `SchoolEquipmentSeeder.php` không có price_p3..p10 nên không cần sửa.
- [x] **Step 4:** Rà soát toàn bộ reference cũ: `grep -rn "price_p3\|price_p5\|price_p7\|price_p10" nhatlinh-api/Modules/ nhatlinh-client/` → sửa/bỏ mọi nơi còn dùng (Resource khác, Export, FE). Ghi log nếu có nơi ngoài dự kiến. → BE: sửa ProductService (service), DetailProductResource (resource), ProductRequest (validation), ProductController (eager-load). FE: ProductForm.vue còn reference → xử lý toàn bộ trong Task 11 (full dynamic implementation).
- [x] **Step 5:** `php -l` ProductService + Resource → OK. Smoke-test tinker: tạo 2 tier ACTIVE (5%, 10%), dùng ProductUnit thực id=1 price_p0=1000 → product_unit_prices: 2 dòng, giá 1050.00 và 1100.00. Đã dọn sạch data test.

### Task 11: FE ProductForm — cột giá động

**Files:** Modify `nhatlinh-client/pages/category/products/components/ProductForm.vue`

- [x] **Step 1:** Load danh sách tier ACTIVE khi mở form: gọi `GET price-tiers/getAll` → lưu `this.priceTiers = [{id, name, percent}]`.
- [x] **Step 2:** Thay header bảng units: giữ cột "Giá P0 (Net)" editable; thay 4 cột cứng P3/P5/P7/P10 bằng `v-for` theo `priceTiers`:
```html
<th v-for="t in priceTiers" :key="t.id">{{ t.name }} ({{ t.percent }}%)</th>
```
- [x] **Step 3:** Thay 4 cell cứng bằng cell động (read-only, tính tại FE để preview):
```html
<td v-for="t in priceTiers" :key="t.id">
    <V2BaseCurrencyInput :value="tierPrice(unit, t)" size="sm" placeholder="0" disabled />
</td>
```
Thêm method:
```js
tierPrice(unit, tier) {
    const p0 = Number(unit.price_p0) || 0
    return Math.round(p0 * (1 + Number(tier.percent) / 100) * 100) / 100
}
```
- [x] **Step 4:** Bỏ logic cũ liên quan `onPriceP0Change` set `price_p3..` (nếu có) — giờ giá cấp tính trực tiếp qua `tierPrice()`, không lưu vào unit. Khi submit chỉ gửi `price_p0` mỗi unit (BE tự snapshot). Nếu init unit có `price_p3..` thì xoá khỏi default unit object.
- [x] **Step 5:** Khi sửa product: form nhận `tier_prices` từ BE — không bắt buộc dùng (preview tính từ P0 hiện tại + tier hiện tại là đủ). Verify FE compile + UI: mở form, gõ P0 → các cột cấp tự cập nhật; lưu → reload thấy giá đúng.

---

## Phase 3: Nút tính lại hàng loạt

### Task 12: BE — recalcAllProducts + endpoint

**Files:**
- Modify `Modules/Category/Services/PriceTierService.php`
- Modify `Modules/Category/Http/Controllers/Api/V1/PriceTierController.php`
- (Route đã khai ở Task 7 — bỏ comment nếu đã comment)

- [x] **Step 1:** Thêm `recalcAllProducts()` vào `PriceTierService`:
```php
public function recalcAllProducts(): int
{
    $tiers = PriceTier::where('status', PriceTier::STATUS_ACTIVE)->get();
    $count = 0;
    \Modules\Category\Entities\ProductUnit::chunkById(200, function ($units) use ($tiers, &$count) {
        foreach ($units as $pu) {
            $p0 = (float) $pu->price_p0;
            // dọn snapshot của tier không còn active
            \Modules\Category\Entities\ProductUnitPrice::where('product_unit_id', $pu->id)
                ->whereNotIn('price_tier_id', $tiers->pluck('id'))->delete();
            foreach ($tiers as $tier) {
                \Modules\Category\Entities\ProductUnitPrice::updateOrCreate(
                    ['product_unit_id' => $pu->id, 'price_tier_id' => $tier->id],
                    ['percent' => $tier->percent, 'price' => round($p0 * (1 + $tier->percent / 100), 2)]
                );
            }
            $count++;
        }
    });
    return $count;
}
```
- [x] **Step 2:** Thêm action `recalcProducts()` vào controller: gọi service, trả `{ message, count }`. Bọc trong DB::transaction nếu muốn an toàn.
- [x] **Step 3:** Đảm bảo route `POST price-tiers/recalc-products` (Task 7) đã bật. Verify: `php artisan route:list --path=price-tiers`.
- [x] **Step 4:** Smoke-test tinker: đổi percent 1 tier, gọi `app(PriceTierService::class)->recalcAllProducts()` → kiểm tra `product_unit_prices.price` cập nhật theo percent mới.

### Task 13: FE — nút "Tính lại giá hàng hoá"

**Files:** Modify `nhatlinh-client/pages/category/price-tiers/index.vue`

- [x] **Step 1:** Nối action nút "Tính lại giá hàng hoá" — ĐÃ làm sẵn ở Task 8: confirm modal `confirm-recalc-price-tier` → `POST category/price-tiers/recalc-products` → toast count. Route BE bật ở Task 12. Khớp response `{message, count}`.
- [x] **Step 2:** Verify UI: user test (FE chưa build do node v12). Logic đã xác nhận khớp endpoint.

### Checkpoint — 2026-06-26 (code 13 task)
Vừa hoàn thành: Task 12 — BE recalcAllProducts() + endpoint POST price-tiers/recalc-products + bật route
Đang làm dở: —
Bước tiếp theo: Task 13 — FE nút "Tính lại giá hàng hoá" trong index.vue (confirm modal → POST recalc-products → toast count)
Blocked: —

### Checkpoint — 2026-06-26 (final review + user test fixes)
Vừa hoàn thành: **TOÀN BỘ 13 TASK + final review opus + sửa lỗi phát sinh khi user test**.
- Final review: 0 Critical. Fix 1 Important (modal map lỗi 422 `beErrors.name[0]`→bỏ `[0]`).
- Tối ưu N+1 (theo yêu cầu user): `index()` dùng `withCount('productUnitPrices')`, `isCanDelete()` đọc `product_unit_prices_count` (fallback query).
- Setup dev: tạo permission 1113/1114 + gán role 18 (Super admin) qua insert pivot trực tiếp + reset cache spatie (KHÔNG chạy seeder vì seeder TRUNCATE bảng permissions — sẽ phá phân quyền). Verify hasPermissionTo YES.
- **Bug user test 1** — menu không hiện: do quyền nạp lúc login (phiên cũ chưa có 1113/1114) → user re-login. Menu code đã đúng.
- **Bug user test 2** — `[Vue warn] computed "errors" already defined in data`: dự án đăng ký vee-validate toàn cục (inject computed `errors` ErrorBag). Đổi `errors`→`formErrors` trong `AddPriceTierModal.vue` (data + template + script). FIXED.
- **Bug user test 3** — load trang 500 (2 toast "Lỗi máy chủ"+"Lỗi khi tải dữ liệu"): `PriceTierService::index()` tự `->paginate()` trong khi controller `apiPaginate()` cũng gọi `->paginate()` → paginate 2 lần → `Collection::paginate does not exist`. Sửa: index() trả query builder (bỏ `->paginate()`), giống Manufacturer. Verify tinker `apiPaginate OK`. FIXED.
Đang làm dở: —
Bước tiếp theo: User test lại UI đầy đủ (re-login để thấy menu) → commit 2 repo.
Blocked: —

---

## Phase 4: Auto-fill giá vào Báo giá bán

**Quyết định:** dropdown "Cấp giá" đầu phiếu (P0 + các cấp ACTIVE, mặc định P0) → đơn giá MỌI dòng tự điền theo cấp + đơn vị tính từng dòng. Đơn giá **khoá (read-only)**. **Lưu `price_tier_id` vào phiếu** (null = P0). Khi sửa phiếu: khôi phục selector + GIỮ đơn giá đã lưu (chỉ tính lại khi user đổi cấp / đổi ĐVT / chọn hàng mới). Nguồn giá: `tier_prices` snapshot, thiếu thì `P0×(1+%/100)`.

### Task 14: BE — lưu price_tier_id + trả tier prices trong getAll

**Files:**
- Create `nhatlinh-api/Modules/Sale/Database/Migrations/2026_06_26_000005_add_price_tier_id_to_sale_quotations.php`
- Modify `Modules/Sale/Entities/SaleQuotation.php` (fillable)
- Modify `Modules/Sale/Services/SaleQuotationService.php` (updateOrCreate payload)
- Modify `Modules/Sale/Http/Requests/SaleQuotationRequest.php` (rule)
- Modify `Modules/Sale/Transformers/SaleQuotationResource/DetailSaleQuotationResource.php` (trả về)
- Modify `Modules/Category/Services/ProductService.php` (getAll load prices)

- [x] **Step 1:** Migration add cột:
```php
Schema::table('sale_quotations', function (Blueprint $table) {
    $table->unsignedBigInteger('price_tier_id')->nullable()->after('customer_contact_id');
});
```
down(): `dropColumn('price_tier_id')`. Run `php artisan migrate`.
- [x] **Step 2:** `SaleQuotation` fillable: thêm `'price_tier_id'`.
- [x] **Step 3:** `SaleQuotationService::updateOrCreate` payload: thêm `'price_tier_id' => $request->price_tier_id,`.
- [x] **Step 4:** `SaleQuotationRequest` rules: thêm `'price_tier_id' => 'nullable|exists:price_tiers,id',`.
- [x] **Step 5:** `DetailSaleQuotationResource`: thêm `'price_tier_id' => $this->price_tier_id,`.
- [x] **Step 6:** `ProductService::getAll`: đổi `.with(['productUnits.unit'])` → `.with(['productUnits.unit', 'productUnits.prices'])` để FE có `product_units[].prices [{price_tier_id, percent, price}]`.
- [x] **Step 7:** `php -l` + smoke-test tinker: Schema::hasColumn → TRUE; relation_loaded=YES (prices_count=0 — DB chưa có snapshot, expected); tất cả 6 file No syntax errors.

### Task 15: FE — selector cấp giá + auto-fill + khoá đơn giá

**Files:** Modify `nhatlinh-client/components/sale/quotation/QuotationForm.vue`

- [x] **Step 1:** `data`: thêm `priceTierId: null`, `priceTiers: []`. Load `category/price-tiers/getAll` (chỉ ACTIVE) trong created/fetch → `this.priceTiers`.
- [x] **Step 2:** Thêm select **"Cấp giá"** đầu phiếu (cạnh KH/ngày). Options: `[{value: null, text: 'Giá gốc (P0)'}, ...priceTiers.map(t => ({value: t.id, text: t.name + ' (' + t.percent + '%)'}))]`. v-model `priceTierId`.
- [x] **Step 3:** Method `priceForUnit(productUnit, tierId)`:
```js
priceForUnit(pu, tierId) {
    if (!pu) return 0
    const p0 = Number(pu.price_p0) || 0
    if (!tierId) return p0
    const snap = (pu.prices || []).find(p => p.price_tier_id === tierId)
    if (snap) return Number(snap.price) || 0
    const tier = this.priceTiers.find(t => t.id === tierId)
    return tier ? Math.round(p0 * (1 + Number(tier.percent) / 100) * 100) / 100 : p0
}
```
Helper lấy productUnit theo it.product_id + it.unit_id từ `productRaw`.
- [x] **Step 4:** Khi chọn hàng (`onPickProducts`) + đổi ĐVT (`onProductChange`/đổi unit_id): set `it.unit_price = this.priceForUnit(<productUnit theo unit_id>, this.priceTierId)` thay cho `= 0`.
- [x] **Step 5:** Watch `priceTierId`: khi đổi → tính lại `unit_price` cho TẤT CẢ dòng theo cấp mới (theo unit_id từng dòng). Tính lại line_amount.
- [x] **Step 6:** Ô **Đơn giá** (input line ~188-195): thành **read-only/disabled** (bỏ cho nhập tay). Vẫn hiển thị currency-format.
- [x] **Step 7:** Submit payload: thêm `price_tier_id: this.priceTierId`.
- [x] **Step 8:** Khi sửa phiếu (load detail): set `this.priceTierId = detail.price_tier_id ?? null`; **GIỮ** unit_price đã lưu mỗi dòng (KHÔNG auto tính lại khi load). Chỉ tính lại khi user đổi selector/ĐVT/chọn hàng mới.
- [x] **Step 9:** Verify: chọn cấp giá → đơn giá tự điền & khoá; đổi cấp → mọi dòng đổi; lưu → đọc lại đúng price_tier_id + giá. (FE chưa build do node v12 → user test.)

### Checkpoint — 2026-06-26 (Task 15 done)
Vừa hoàn thành: Task 15 — FE QuotationForm.vue: selector Cấp giá + auto-fill đơn giá + khoá ô + watch + load detail giữ giá cũ + payload price_tier_id
Đang làm dở: —
Bước tiếp theo: User test UI (FE chưa build do Node v12) — xác nhận selector hiển thị, đơn giá auto-fill khi chọn cấp, lưu phiếu có price_tier_id, đọc lại phiếu cũ hiển thị đúng cấp giá
Blocked: —

---

## Self-Review checklist (đã verify)
- [x] Không còn reference `price_p3/p5/p7/p10` ở BE & FE (trừ migration gốc + down()).
- [x] Permission 1113-1114 đã tạo + gán role 18 Super admin (DB dev).
- [x] Route thao tác đều có `checkPermission`; route xem có quyền xem.
- [x] FE chỉ render trạng thái qua `V2BaseBadge` (không hardcode màu/text).
- [x] Validate inline đủ ở modal Bảng giá (đã đổi `errors`→`formErrors` tránh vee-validate).
- [x] index() trả query builder (apiPaginate pattern) — FIXED lỗi 500.
- [x] Báo giá: QuotationForm.vue đã implement đầy đủ Phase 4 (Task 15) — user xác nhận khi test UI.
