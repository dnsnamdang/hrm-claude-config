# Danh mục hàng hoá — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng CRUD danh mục hàng hoá với nhiều ĐVT/giá và upload ảnh cho module Category.

**Architecture:** 2 bảng mới (products, product_units) + bảng files chung cho ảnh. BE theo pattern ManufacturerController. FE list page giống manufacturers, form tạo/sửa là router riêng (không popup).

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap 4, Bootstrap-Vue

---

## Phase 1: Backend — Database & Entity

### Task 1: Migration `products`

**Files:**
- Create: `Modules/Category/Database/Migrations/2026_06_03_000001_create_products_table.php`

- [x] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateProductsTable extends Migration
{
    public function up()
    {
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('code', 50)->unique();
            $table->string('name', 255);
            $table->unsignedBigInteger('manufacturer_id')->nullable();
            $table->unsignedBigInteger('country_of_origin_id')->nullable();
            $table->unsignedBigInteger('product_type_id')->nullable();
            $table->text('specifications')->nullable();
            $table->decimal('vat', 5, 2)->default(0);
            $table->text('description')->nullable();
            $table->integer('status')->default(1);
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('products');
    }
}
```

- [x] **Step 2: Chạy migration**

Run: `cd /hrm-api && php artisan migrate`

---

### Task 2: Migration `product_units`

**Files:**
- Create: `Modules/Category/Database/Migrations/2026_06_03_000002_create_product_units_table.php`

- [x] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateProductUnitsTable extends Migration
{
    public function up()
    {
        Schema::create('product_units', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('product_id');
            $table->unsignedBigInteger('unit_id');
            $table->tinyInteger('is_base_unit')->default(0);
            $table->decimal('price_p0', 15, 2)->default(0);
            $table->decimal('price_p3', 15, 2)->default(0);
            $table->decimal('price_p5', 15, 2)->default(0);
            $table->decimal('price_p7', 15, 2)->default(0);
            $table->decimal('price_p10', 15, 2)->default(0);
            $table->timestamps();

            $table->foreign('product_id')->references('id')->on('products')->onDelete('cascade');
            $table->unique(['product_id', 'unit_id']);
        });
    }

    public function down()
    {
        Schema::dropIfExists('product_units');
    }
}
```

- [x] **Step 2: Chạy migration**

Run: `cd /hrm-api && php artisan migrate`

---

### Task 3: Entity Product

**Files:**
- Create: `Modules/Category/Entities/Product.php`

- [x] **Step 1: Tạo entity**

```php
<?php

namespace Modules\Category\Entities;

use App\Models\BaseModel;
use App\Models\File;
use Modules\Human\Entities\Employee;

class Product extends BaseModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 2;

    protected $table = 'products';

    protected $fillable = [
        'code', 'name', 'manufacturer_id', 'country_of_origin_id', 'product_type_id',
        'specifications', 'vat', 'description', 'status',
        'created_by', 'updated_by', 'company_id', 'department_id', 'part_id',
        'created_at', 'updated_at',
    ];

    public function manufacturer()
    {
        return $this->belongsTo(Manufacturer::class, 'manufacturer_id');
    }

    public function countryOfOrigin()
    {
        return $this->belongsTo(CountryOfOrigin::class, 'country_of_origin_id');
    }

    public function productType()
    {
        return $this->belongsTo(ProductType::class, 'product_type_id');
    }

    public function productUnits()
    {
        return $this->hasMany(ProductUnit::class, 'product_id');
    }

    public function files()
    {
        return $this->hasMany(File::class, 'table_id', 'id')
            ->where('table', 'products');
    }

    public function updatedByEmployee()
    {
        return $this->belongsTo(Employee::class, 'updated_by');
    }

    public function createdByEmployee()
    {
        return $this->belongsTo(Employee::class, 'created_by');
    }

    public function getEmployeeUpdateNameAttribute()
    {
        return $this->updatedByEmployee && $this->updatedByEmployee->info
            ? $this->updatedByEmployee->info->code . ' - ' . $this->updatedByEmployee->info->fullname
            : null;
    }

    public function getEmployeeCreateNameAttribute()
    {
        return $this->createdByEmployee && $this->createdByEmployee->info
            ? $this->createdByEmployee->info->code . ' - ' . $this->createdByEmployee->info->fullname
            : null;
    }

    public function getBaseUnitNameAttribute()
    {
        $baseUnit = $this->productUnits->firstWhere('is_base_unit', 1);
        return $baseUnit && $baseUnit->unit ? $baseUnit->unit->name : null;
    }

    public function isCanEdit()
    {
        return $this->status == self::STATUS_ACTIVE;
    }

    public function isCanLockUpdate()
    {
        return true;
    }

    public function isCanUnlockUpdate()
    {
        return true;
    }

    public function isCanDelete()
    {
        return true;
    }
}
```

---

### Task 4: Entity ProductUnit

**Files:**
- Create: `Modules/Category/Entities/ProductUnit.php`

- [x] **Step 1: Tạo entity**

```php
<?php

namespace Modules\Category\Entities;

use Illuminate\Database\Eloquent\Model;

class ProductUnit extends Model
{
    protected $table = 'product_units';

    protected $fillable = [
        'product_id', 'unit_id', 'is_base_unit',
        'price_p0', 'price_p3', 'price_p5', 'price_p7', 'price_p10',
    ];

    public function product()
    {
        return $this->belongsTo(Product::class, 'product_id');
    }

    public function unit()
    {
        return $this->belongsTo(Unit::class, 'unit_id');
    }
}
```

---

## Phase 2: Backend — Request, Service, Transformer, Controller, Routes

### Task 5: ProductRequest

**Files:**
- Create: `Modules/Category/Http/Requests/ProductRequest.php`

- [x] **Step 1: Tạo request**

```php
<?php

namespace Modules\Category\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;

class ProductRequest extends BaseRequest
{
    public function rules()
    {
        $rules = [
            'code' => 'required|max:50|unique:products,code,' . $this->id,
            'name' => 'required|max:255',
            'manufacturer_id' => 'nullable|exists:manufacturers,id',
            'country_of_origin_id' => 'nullable|exists:country_of_origins,id',
            'product_type_id' => 'nullable|exists:product_types,id',
            'vat' => 'nullable|numeric|min:0|max:100',
            'specifications' => 'nullable|string',
            'description' => 'nullable|string|max:5000',
            'units' => 'required|array|min:1',
            'units.*.unit_id' => 'required|exists:units,id',
            'units.*.is_base_unit' => 'required|in:0,1',
            'units.*.price_p0' => 'nullable|numeric|min:0',
            'units.*.price_p3' => 'nullable|numeric|min:0',
            'units.*.price_p5' => 'nullable|numeric|min:0',
            'units.*.price_p7' => 'nullable|numeric|min:0',
            'units.*.price_p10' => 'nullable|numeric|min:0',
            'images' => 'nullable|array',
            'images.*.file_path' => 'required_with:images|string',
        ];

        return $rules;
    }

    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            $units = $this->input('units', []);

            if (!empty($units)) {
                $baseCount = collect($units)->where('is_base_unit', 1)->count();
                if ($baseCount !== 1) {
                    $validator->errors()->add('units', 'Phải có đúng 1 đơn vị tính cơ bản');
                }

                $unitIds = collect($units)->pluck('unit_id')->filter();
                if ($unitIds->count() !== $unitIds->unique()->count()) {
                    $validator->errors()->add('units', 'Không được chọn trùng đơn vị tính');
                }
            }
        });
    }

    public function messages()
    {
        return [
            'code.required' => 'Mã hàng hoá không được để trống',
            'code.max' => 'Mã hàng hoá tối đa 50 ký tự',
            'code.unique' => 'Mã hàng hoá đã tồn tại',
            'name.required' => 'Tên hàng hoá không được để trống',
            'name.max' => 'Tên hàng hoá tối đa 255 ký tự',
            'units.required' => 'Phải có ít nhất 1 đơn vị tính',
            'units.min' => 'Phải có ít nhất 1 đơn vị tính',
            'vat.min' => 'VAT không được nhỏ hơn 0',
            'vat.max' => 'VAT không được lớn hơn 100',
        ];
    }
}
```

---

### Task 6: ProductService

**Files:**
- Create: `Modules/Category/Services/ProductService.php`

- [x] **Step 1: Tạo service**

```php
<?php

namespace Modules\Category\Services;

use Illuminate\Http\Request;
use Modules\Training\Services\BaseService;
use Modules\Category\Entities\Product;
use Modules\Category\Entities\ProductUnit;
use Modules\Category\Http\Requests\ProductRequest;
use App\Models\File;

class ProductService extends BaseService
{
    public function index(Request $request)
    {
        $query = Product::query()
            ->select('products.*')
            ->with(['manufacturer', 'productType', 'productUnits.unit']);

        if (isset($request->company_id)) {
            $query->where('products.company_id', $request->company_id);
        }

        if (isset($request->department_id)) {
            $query->where('products.department_id', $request->department_id);
        }

        if (isset($request->name)) {
            $query->where('products.name', 'like', '%' . $request->name . '%');
        }

        if (isset($request->code)) {
            $query->where('products.code', 'like', '%' . $request->code . '%');
        }

        if (isset($request->status)) {
            $query->where('products.status', $request->status);
        }

        if (isset($request->manufacturer_id)) {
            $query->where('products.manufacturer_id', $request->manufacturer_id);
        }

        if (isset($request->country_of_origin_id)) {
            $query->where('products.country_of_origin_id', $request->country_of_origin_id);
        }

        if (isset($request->product_type_id)) {
            $query->where('products.product_type_id', $request->product_type_id);
        }

        if (isset($request->keyword)) {
            $escapedKeyword = escapeLikeKeyword($request->keyword);
            if ($escapedKeyword !== '') {
                $query->where(function ($q) use ($escapedKeyword) {
                    $q->where('products.name', 'like', '%' . $escapedKeyword . '%')
                        ->orWhere('products.code', 'like', '%' . $escapedKeyword . '%');
                });
            }
        }

        if (isset($request->created_by)) {
            $query->where('products.created_by', $request->created_by);
        }

        if (isset($request->updated_by)) {
            $query->where('products.updated_by', $request->updated_by);
        }

        if ($request->filled('updated_from')) {
            $query->whereDate('products.updated_at', '>=', $request->updated_from);
        }

        if ($request->filled('updated_to')) {
            $query->whereDate('products.updated_at', '<=', $request->updated_to);
        }

        if (isset($request->sort_by) && isset($request->sort_desc)) {
            $sortField = $request->sort_by;
            $sortDir = strtolower($request->sort_desc) == 'true' ? 'desc' : 'asc';
            if (!in_array($sortDir, ['asc', 'desc'])) {
                $sortDir = 'desc';
            }
            $allowedSortFields = [
                'updated_at' => 'products.updated_at',
            ];
            if (array_key_exists($sortField, $allowedSortFields)) {
                return $query->orderBy($allowedSortFields[$sortField], $sortDir);
            }
        }

        return $query->orderBy('products.id', 'desc');
    }

    public function getAll(Request $request)
    {
        return Product::query()
            ->select('products.*')
            ->with(['productUnits.unit'])
            ->where('products.status', Product::STATUS_ACTIVE)
            ->orderBy('products.id', 'asc')
            ->get();
    }

    public function updateOrCreate(ProductRequest $request)
    {
        $productData = [
            'code' => trim($request->code),
            'name' => $request->name,
            'manufacturer_id' => $request->manufacturer_id,
            'country_of_origin_id' => $request->country_of_origin_id,
            'product_type_id' => $request->product_type_id,
            'specifications' => $request->specifications,
            'vat' => $request->vat ?? 0,
            'description' => $request->description,
            'status' => $request->status ?? 1,
            'part_id' => auth()->user()->info->part_id,
        ];

        if (isset($request->id)) {
            $product = Product::find($request->id);

            if ($product && $product->status == Product::STATUS_ACTIVE) {
                $product->update(array_merge($productData, [
                    'updated_by' => auth()->user()->info->id,
                ]));
            } else {
                return [
                    'status' => '404',
                    'message' => 'Dữ liệu đã thay đổi, vui lòng tải lại',
                ];
            }
        } else {
            $product = Product::create(array_merge($productData, [
                'created_by' => auth()->user()->info->id,
            ]));
        }

        $this->syncProductUnits($product, $request->units);
        $this->syncImages($product, $request->images ?? []);

        return response()->json($product->load(['productUnits.unit', 'files']), 200);
    }

    public function update(ProductRequest $request, Product $product)
    {
        if ($product->status != Product::STATUS_ACTIVE) {
            return [
                'status' => '404',
                'message' => 'Dữ liệu đã thay đổi, vui lòng tải lại',
            ];
        }

        $product->update([
            'code' => trim($request->code),
            'name' => $request->name,
            'manufacturer_id' => $request->manufacturer_id,
            'country_of_origin_id' => $request->country_of_origin_id,
            'product_type_id' => $request->product_type_id,
            'specifications' => $request->specifications,
            'vat' => $request->vat ?? 0,
            'description' => $request->description,
            'status' => $request->status ?? 1,
            'updated_by' => auth()->user()->info->id,
        ]);

        $this->syncProductUnits($product, $request->units);
        $this->syncImages($product, $request->images ?? []);

        return $product->load(['productUnits.unit', 'files']);
    }

    public function destroy(Product $product)
    {
        File::where('table', 'products')->where('table_id', $product->id)->delete();
        $product->delete();
    }

    private function syncProductUnits(Product $product, array $units)
    {
        $product->productUnits()->delete();

        foreach ($units as $unitData) {
            ProductUnit::create([
                'product_id' => $product->id,
                'unit_id' => $unitData['unit_id'],
                'is_base_unit' => $unitData['is_base_unit'] ?? 0,
                'price_p0' => $unitData['price_p0'] ?? 0,
                'price_p3' => $unitData['price_p3'] ?? 0,
                'price_p5' => $unitData['price_p5'] ?? 0,
                'price_p7' => $unitData['price_p7'] ?? 0,
                'price_p10' => $unitData['price_p10'] ?? 0,
            ]);
        }
    }

    private function syncImages(Product $product, array $images)
    {
        $newPaths = collect($images)->pluck('file_path')->filter()->toArray();

        File::where('table', 'products')
            ->where('table_id', $product->id)
            ->whereNotIn('file_path', $newPaths)
            ->delete();

        $existingPaths = File::where('table', 'products')
            ->where('table_id', $product->id)
            ->pluck('file_path')
            ->toArray();

        foreach ($images as $image) {
            if (!empty($image['file_path']) && !in_array($image['file_path'], $existingPaths)) {
                File::create([
                    'table' => 'products',
                    'table_id' => $product->id,
                    'file_path' => $image['file_path'],
                    'file_name' => $image['file_name'] ?? null,
                    'file_size' => $image['file_size'] ?? null,
                    'file_type' => $image['file_type'] ?? null,
                    'created_by' => auth()->user()->info->id ?? null,
                ]);
            }
        }
    }
}
```

---

### Task 7: Transformers

**Files:**
- Create: `Modules/Category/Transformers/ProductResource/ProductResource.php`
- Create: `Modules/Category/Transformers/ProductResource/DetailProductResource.php`

- [x] **Step 1: Tạo ProductResource (list)**

```php
<?php

namespace Modules\Category\Transformers\ProductResource;

use Modules\Human\Transformers\ApiResource;
use Modules\Human\Helper\Helper;

class ProductResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'manufacturer_name' => $this->manufacturer ? $this->manufacturer->name : null,
            'country_of_origin_name' => $this->countryOfOrigin ? $this->countryOfOrigin->name : null,
            'product_type_name' => $this->productType ? $this->productType->name : null,
            'base_unit_name' => $this->base_unit_name,
            'vat' => $this->vat,
            'status' => $this->status,
            'description' => $this->description,
            'created_at' => Helper::formatDateTime($this->created_at),
            'updated_at' => Helper::formatDateTime($this->updated_at),
            'created_by_name' => $this->employee_create_name,
            'updated_by_name' => $this->employee_update_name,
            'is_can_edit' => $this->isCanEdit(),
            'is_can_lock_update' => $this->isCanLockUpdate(),
            'is_can_unlock_update' => $this->isCanUnlockUpdate(),
        ];
    }
}
```

- [x] **Step 2: Tạo DetailProductResource (detail)**

```php
<?php

namespace Modules\Category\Transformers\ProductResource;

use Modules\Human\Transformers\ApiResource;
use Modules\Human\Helper\Helper;

class DetailProductResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'manufacturer_id' => $this->manufacturer_id,
            'manufacturer_name' => $this->manufacturer ? $this->manufacturer->name : null,
            'country_of_origin_id' => $this->country_of_origin_id,
            'country_of_origin_name' => $this->countryOfOrigin ? $this->countryOfOrigin->name : null,
            'product_type_id' => $this->product_type_id,
            'product_type_name' => $this->productType ? $this->productType->name : null,
            'specifications' => $this->specifications,
            'vat' => $this->vat,
            'description' => $this->description,
            'status' => $this->status,
            'created_at' => Helper::formatDateTime($this->created_at),
            'updated_at' => Helper::formatDateTime($this->updated_at),
            'created_by_name' => $this->employee_create_name,
            'updated_by_name' => $this->employee_update_name,
            'is_can_lock_update' => $this->isCanLockUpdate(),
            'is_can_unlock_update' => $this->isCanUnlockUpdate(),
            'product_units' => $this->productUnits->map(function ($pu) {
                return [
                    'id' => $pu->id,
                    'unit_id' => $pu->unit_id,
                    'unit_name' => $pu->unit ? $pu->unit->name : null,
                    'is_base_unit' => $pu->is_base_unit,
                    'price_p0' => $pu->price_p0,
                    'price_p3' => $pu->price_p3,
                    'price_p5' => $pu->price_p5,
                    'price_p7' => $pu->price_p7,
                    'price_p10' => $pu->price_p10,
                ];
            }),
            'images' => $this->files->map(function ($file) {
                return [
                    'id' => $file->id,
                    'file_path' => $file->file_path,
                    'file_name' => $file->file_name,
                    'file_size' => $file->file_size,
                ];
            }),
        ];
    }
}
```

---

### Task 8: ProductController

**Files:**
- Create: `Modules/Category/Http/Controllers/Api/V1/ProductController.php`

- [x] **Step 1: Tạo controller**

```php
<?php

namespace Modules\Category\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use Modules\Category\Services\ProductService;
use Modules\Category\Transformers\ProductResource\ProductResource;
use Modules\Category\Transformers\ProductResource\DetailProductResource;
use Modules\Category\Http\Requests\ProductRequest;
use Modules\Category\Entities\Product;
use App\ExcelExport\ProductExport;
use Excel;

class ProductController extends ApiController
{
    private $productService;

    public function __construct(ProductService $productService)
    {
        $this->productService = $productService;
    }

    public function index(Request $request)
    {
        $result = $this->productService->index($request);
        return $this->apiGetList(ProductResource::apiPaginate($result, $request));
    }

    public function getAll(Request $request)
    {
        $result = $this->productService->getAll($request);
        return $this->responseJson('success', Response::HTTP_OK, $result);
    }

    public function updateOrCreate(ProductRequest $request)
    {
        try {
            return DB::transaction(function () use ($request) {
                $result = $this->productService->updateOrCreate($request);

                if (is_array($result) && isset($result['status']) && $result['status'] === '404') {
                    return $this->responseNotFound($result['message']);
                }

                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (\Illuminate\Validation\ValidationException $e) {
            throw $e;
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function update(ProductRequest $request, Product $product)
    {
        try {
            return DB::transaction(function () use ($request, $product) {
                $result = $this->productService->update($request, $product);

                if (is_array($result) && isset($result['status']) && $result['status'] === '404') {
                    return $this->responseNotFound($result['message']);
                }

                return $this->responseJson(
                    'success',
                    Response::HTTP_OK,
                    new DetailProductResource($result)
                );
            });
        } catch (\Illuminate\Validation\ValidationException $e) {
            throw $e;
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show(Product $product)
    {
        $product->load(['manufacturer', 'countryOfOrigin', 'productType', 'productUnits.unit', 'files']);
        return $this->responseJson('success', Response::HTTP_OK, new DetailProductResource($product));
    }

    public function delete(Product $product)
    {
        try {
            return DB::transaction(function () use ($product) {
                if (!$product->isCanDelete()) {
                    return $this->responseBadRequest('Dữ liệu đang được sử dụng, vui lòng tải lại');
                }
                $this->productService->destroy($product);

                return $this->responseJson('success', Response::HTTP_OK);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function lock(Product $product)
    {
        if (!$product->isCanLockUpdate()) {
            return $this->responseBadRequest('Dữ liệu đã thay đổi, vui lòng tải lại');
        }
        $product->status = Product::STATUS_INACTIVE;
        $product->save();
        return $this->responseJson('lock item success', Response::HTTP_OK);
    }

    public function unlock(Product $product)
    {
        $product->status = Product::STATUS_ACTIVE;
        $product->save();
        return $this->responseJson('unlock item success', Response::HTTP_OK);
    }

    public function export(Request $request)
    {
        try {
            $response = $this->index($request);
            $data = $response->getData(true)['data'];

            return Excel::download(
                (new ProductExport())->forData($data),
                'danh_sach_hang_hoa.xls'
            );
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
}
```

---

### Task 9: Routes

**Files:**
- Modify: `Modules/Category/Routes/api.php`

- [x] **Step 1: Thêm routes cho products**

Thêm vào cuối file, trước dấu `});` đóng group chính:

```php
    // Hàng hoá
    Route::group(['prefix' => '/products'], function () {
        Route::get('/', [ProductController::class, 'index'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá|Xem danh mục hàng hoá');
        Route::get('/getAll', [ProductController::class, 'getAll']);
        Route::get('/export', [ProductController::class, 'export'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
        Route::post('/', [ProductController::class, 'updateOrCreate'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
        Route::put('/{product}', [ProductController::class, 'update'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
        Route::get('/{product}', [ProductController::class, 'show'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá|Xem danh mục hàng hoá');
        Route::delete('/{product}', [ProductController::class, 'delete'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
        Route::get('/{product}/lock', [ProductController::class, 'lock'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
        Route::get('/{product}/unlock', [ProductController::class, 'unlock'])
            ->middleware('checkPermission:Quản lý danh mục hàng hoá');
    });
```

- [x] **Step 2: Thêm use statement**

Thêm ở đầu file:

```php
use Modules\Category\Http\Controllers\Api\V1\ProductController;
```

---

### Task 10: ExcelExport

**Files:**
- Create: `app/ExcelExport/ProductExport.php`
- Create: `resources/views/exports/products.blade.php`

- [x] **Step 1: Tạo ProductExport**

```php
<?php

namespace App\ExcelExport;

use Maatwebsite\Excel\Concerns\FromView;
use Maatwebsite\Excel\Concerns\Exportable;
use Illuminate\Contracts\View\View;

class ProductExport implements FromView
{
    use Exportable;

    private $data;

    public function forData($data)
    {
        $this->data = $data;
        return $this;
    }

    public function view(): View
    {
        $data = $this->data;
        return view('exports.products', compact('data'));
    }
}
```

- [x] **Step 2: Tạo Blade view**

```blade
<table>
    <thead>
        <tr>
            <th>STT</th>
            <th>Mã hàng</th>
            <th>Tên hàng hoá</th>
            <th>Hãng sản xuất</th>
            <th>Loại hàng hoá</th>
            <th>ĐVT cơ bản</th>
            <th>VAT (%)</th>
            <th>Trạng thái</th>
            <th>Ngày cập nhật</th>
            <th>Người cập nhật</th>
        </tr>
    </thead>
    <tbody>
        @foreach($data as $index => $item)
        <tr>
            <td>{{ $index + 1 }}</td>
            <td>{{ $item['code'] ?? '' }}</td>
            <td>{{ $item['name'] ?? '' }}</td>
            <td>{{ $item['manufacturer_name'] ?? '' }}</td>
            <td>{{ $item['product_type_name'] ?? '' }}</td>
            <td>{{ $item['base_unit_name'] ?? '' }}</td>
            <td>{{ $item['vat'] ?? 0 }}</td>
            <td>{{ ($item['status'] ?? 1) == 1 ? 'Hoạt động' : 'Khoá' }}</td>
            <td>{{ $item['updated_at'] ?? '' }}</td>
            <td>{{ $item['updated_by_name'] ?? '' }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

---

## Phase 3: Frontend — Danh sách hàng hoá

### Task 11: List page `products/index.vue`

**Files:**
- Create: `pages/category/products/index.vue`

- [x] **Step 1: Tạo file index.vue**

Pattern giống `pages/category/manufacturers/index.vue` nhưng:
- Nút "Tạo mới" → `$router.push('/category/products/create')` (không mở modal)
- Không có Import Excel
- Filter thêm: manufacturer_id (select), country_of_origin_id (select), product_type_id (select)
- Columns: STT, itemInfo (code+name), manufacturer, productType, baseUnit, updatedAt, status
- Row actions: Xem → `$router.push('/category/products/' + item.id)`, Sửa → `$router.push('/category/products/' + item.id + '/edit')`, Xoá → confirm modal
- `created()`: load thêm manufacturers, countryOfOrigins, productTypes options bằng getAll

```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <V2BaseFilterPanel
                title="Bộ lọc danh sách hàng hoá"
                subtitle="Bạn có thể chọn tìm kiếm nâng cao để lọc nhiều thông tin hơn"
                :collapsed="filterCollapsed"
                :quickSearchValue="filters.keyword"
                quickSearchPlaceholder="Tìm theo mã hàng, tên hàng hoá..."
                :filters="filters"
                @toggle-panel="toggleFilterPanel"
                @quick-search-change="handleKeywordChange"
                @filter-change="handleFilterChange"
                @search="handleSearch"
                @reset="handleReset"
            >
                <template #advanced-filters="{ collapsed: slotCollapsed }">
                    <div v-show="!slotCollapsed" class="advanced-filters">
                        <div class="form-row">
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Mã hàng</V2BaseLabel>
                                <V2BaseInput v-model="filters.code" placeholder="Nhập mã hàng" size="sm" />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Tên hàng hoá</V2BaseLabel>
                                <V2BaseInput v-model="filters.name" placeholder="Nhập tên hàng hoá" size="sm" />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Hãng sản xuất</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.manufacturer_id"
                                    :options="manufacturerOptions"
                                    :allowClear="true"
                                    placeholder="Chọn hãng sản xuất"
                                />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Nước sản xuất</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.country_of_origin_id"
                                    :options="countryOfOriginOptions"
                                    :allowClear="true"
                                    placeholder="Chọn nước sản xuất"
                                />
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Loại hàng hoá</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.product_type_id"
                                    :options="productTypeOptions"
                                    :allowClear="true"
                                    placeholder="Chọn loại hàng hoá"
                                />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Trạng thái</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.status"
                                    :options="statusOptions"
                                    :allowClear="true"
                                    placeholder="Chọn trạng thái"
                                />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Người tạo</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.created_by"
                                    :options="employeeOptions"
                                    :allowClear="true"
                                    placeholder="Chọn người tạo"
                                />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Người cập nhật</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.updated_by"
                                    :options="employeeOptions"
                                    :allowClear="true"
                                    placeholder="Chọn người cập nhật"
                                />
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Cập nhật từ</V2BaseLabel>
                                <V2BaseDatePicker
                                    v-model="filters.updated_from"
                                    type="date"
                                    value-type="YYYY-MM-DD"
                                    format="DD/MM/YYYY"
                                    size="sm"
                                />
                            </div>
                            <div class="col-md-3 mb-3">
                                <V2BaseLabel>Cập nhật đến</V2BaseLabel>
                                <V2BaseDatePicker
                                    v-model="filters.updated_to"
                                    type="date"
                                    value-type="YYYY-MM-DD"
                                    format="DD/MM/YYYY"
                                    size="sm"
                                />
                            </div>
                        </div>
                    </div>
                </template>
            </V2BaseFilterPanel>

            <V2BaseDataTable
                :data="tableData"
                :columns="tableColumns"
                :pagination="pagination"
                :loading="loading"
                title="Danh sách hàng hoá"
                :sortBy="filters.sort_by === 'updated_at' ? 'updatedAt' : filters.sort_by"
                :sortDirection="filters.sort_desc ? 'desc' : 'asc'"
                rowKey="id"
                itemLabel="hàng hoá"
                emptyText="Không có dữ liệu phù hợp bộ lọc."
                @sort="handleSort"
                @page-change="handlePageChange"
                @page-size-change="handlePageSizeChange"
            >
                <template #actions>
                    <V2BaseButton primary size="sm" class="mr-2 mb-2" @click="createItem">
                        <template #prefix>
                            <i class="ri-add-line" style="font-size: 13px"></i>
                        </template>
                        Tạo mới
                    </V2BaseButton>
                    <V2BaseButton secondary size="sm" class="mb-2" @click="exportExcel">
                        <template #prefix>
                            <i class="ri-file-excel-2-line" style="font-size: 13px"></i>
                        </template>
                        Xuất Excel
                    </V2BaseButton>
                </template>

                <template #cell-index="{ index }">
                    {{ getNumericalOrder(pagination.currentPage, pagination.pageSize, index) }}
                </template>

                <template #cell-itemInfo="{ item }">
                    <div class="d-flex justify-content-between align-items-start position-relative" style="padding-right: 120px">
                        <V2BaseTitleSubInfo
                            :title="[
                                { text: item.code, isLightColor: true },
                                { text: item.name, isLightColor: false },
                            ]"
                            :separatorTitle="'-'"
                            titleClass="field-line font-weight-bold text-dark"
                            :subs="[
                                [
                                    [
                                        { text: 'Người tạo:', isBold: false },
                                        { text: item.created_by_name || '—', isBold: true },
                                    ],
                                    [
                                        { text: 'Ngày tạo:', isBold: false },
                                        { text: item.created_at, isBold: true },
                                    ],
                                ],
                            ]"
                            separator=""
                        ></V2BaseTitleSubInfo>

                        <div class="row-actions">
                            <button type="button" class="action-icon-btn" title="Xem" @click="viewItem(item)">
                                <i class="ri-eye-line"></i>
                            </button>
                            <button type="button" class="action-icon-btn" title="Sửa" :disabled="item.status === 2" @click="editItem(item)">
                                <i class="ri-edit-line"></i>
                            </button>
                            <button type="button" class="action-icon-btn action-icon-danger" title="Xoá" @click="confirmDeleteItem(item)">
                                <i class="ri-delete-bin-6-line"></i>
                            </button>
                        </div>
                    </div>
                </template>

                <template #cell-manufacturer="{ item }">
                    <div class="field-line text-dark">{{ item.manufacturer_name || '—' }}</div>
                </template>

                <template #cell-productType="{ item }">
                    <div class="field-line text-dark">{{ item.product_type_name || '—' }}</div>
                </template>

                <template #cell-baseUnit="{ item }">
                    <div class="field-line text-dark">{{ item.base_unit_name || '—' }}</div>
                </template>

                <template #cell-updatedAt="{ item }">
                    <V2BaseTitleSubInfo
                        :title="item.updated_at"
                        titleClass="field-line text-dark"
                        :titleBold="false"
                        :subs="[
                            [
                                [
                                    { text: 'bởi', isBold: false },
                                    { text: item.updated_by_name, isBold: true },
                                ],
                            ],
                        ]"
                        :separator="''"
                    ></V2BaseTitleSubInfo>
                </template>

                <template #cell-status="{ item }">
                    <div class="status-wrap">
                        <span v-html="renderStatus(item.status)"></span>
                        <button
                            class="toggle-status-btn"
                            :title="item.status === 2 ? 'Mở khoá hàng hoá' : 'Khoá hàng hoá'"
                            @click="confirmToggleLock(item)"
                        >
                            <i :class="item.status === 2 ? 'ri-lock-unlock-line' : 'ri-lock-line'"></i>
                        </button>
                    </div>
                </template>
            </V2BaseDataTable>
        </div>

        <BaseConfirmModal
            id="confirm-delete-product"
            title="Xác nhận xóa"
            :message="deleteConfirmMessage"
            text-close="Hủy"
            text-accept="Xóa"
            @event="handleConfirmDelete"
        />

        <BaseConfirmModal
            id="confirm-toggle-lock-product"
            :title="lockConfirmTitle"
            :message="lockConfirmMessage"
            text-close="Hủy"
            :text-accept="lockConfirmAction"
            @event="toggleLock"
        />
    </div>
</template>

<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseFilterPanel from '@/components/V2BaseFilterPanel.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseDatePicker from '@/components/V2BaseDatePicker.vue'
import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import { buildQueryString, buildQuery } from '@/utils/url-action'
import { getNumericalOrder } from '@/utils/common.js'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

const initialStateForm = {
    keyword: undefined,
    code: undefined,
    name: undefined,
    manufacturer_id: undefined,
    country_of_origin_id: undefined,
    product_type_id: undefined,
    status: undefined,
    created_by: undefined,
    updated_by: undefined,
    updated_from: undefined,
    updated_to: undefined,
    sort_by: 'id',
    sort_desc: true,
}

export default {
    mixins: [PageTitleMixin],
    head() {
        return { title: 'Danh sách hàng hoá' }
    },
    components: {
        V2BaseButton, V2BaseFilterPanel, V2BaseDataTable, V2BaseLabel,
        V2BaseSelect, V2BaseInput, V2BaseDatePicker, V2BaseTitleSubInfo,
        BaseConfirmModal,
    },
    data() {
        return {
            loading: false,
            tableData: [],
            pagination: { currentPage: 1, pageSize: 10, total: 0, totalPages: 1, from: 0, to: 0 },
            filterCollapsed: true,
            filters: { ...initialStateForm },
            itemToDelete: null,
            itemToToggle: null,
            statusOptions: [{ id: 1, name: 'Hoạt động' }, { id: 2, name: 'Khóa' }],
            manufacturerOptions: [],
            countryOfOriginOptions: [],
            productTypeOptions: [],
            ignoredFields: ['keyword'],
            oldFilters: {},
        }
    },
    computed: {
        pageTitle() { return 'Danh sách hàng hoá' },
        employeeOptions() { return this.$store.state.allEmployeesOptions || [] },
        tableColumns() {
            return [
                { key: 'index', title: 'STT', width: '60px', minWidth: '60px', align: 'left' },
                { key: 'itemInfo', title: 'Mã hàng - Tên hàng hoá', width: '400px', cellClass: 'text-wrap', minWidth: '250px', align: 'left' },
                { key: 'manufacturer', title: 'Hãng sản xuất', width: '180px', minWidth: '120px', align: 'left' },
                { key: 'productType', title: 'Loại hàng hoá', width: '160px', minWidth: '120px', align: 'left' },
                { key: 'baseUnit', title: 'ĐVT cơ bản', width: '120px', minWidth: '100px', align: 'left' },
                { key: 'updatedAt', title: 'Cập nhật', width: '160px', minWidth: '160px', align: 'left', sortable: true },
                { key: 'status', title: 'Trạng thái', width: '140px', minWidth: '140px', align: 'left' },
            ]
        },
        deleteConfirmMessage() {
            return this.itemToDelete ? `Bạn có chắc muốn xóa hàng hoá '${this.itemToDelete.name}'?` : ''
        },
        lockConfirmTitle() {
            return this.itemToToggle ? (this.itemToToggle.status === 2 ? 'Xác nhận mở khoá' : 'Xác nhận khoá') : ''
        },
        lockConfirmMessage() {
            if (!this.itemToToggle) return ''
            const action = this.itemToToggle.status === 2 ? 'mở khoá' : 'khoá'
            return `Bạn có chắc muốn ${action} hàng hoá '${this.itemToToggle.name}'?`
        },
        lockConfirmAction() {
            return this.itemToToggle ? (this.itemToToggle.status === 2 ? 'Mở khoá' : 'Khoá') : ''
        },
    },
    async created() {
        await Promise.all([
            this.loadData(),
            this.loadFilterOptions(),
        ])
    },
    watch: {
        filters: {
            handler(newVal) {
                const shouldCallApi = !this.ignoredFields.some((field) => newVal[field] !== this.oldFilters[field])
                if (shouldCallApi) this.loadData()
                this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            },
            deep: true,
        },
    },
    methods: {
        getNumericalOrder,

        async loadFilterOptions() {
            try {
                const [mfRes, coRes, ptRes] = await Promise.all([
                    this.$store.dispatch('apiGetMethod', 'category/manufacturers/getAll'),
                    this.$store.dispatch('apiGetMethod', 'category/country-of-origins/getAll'),
                    this.$store.dispatch('apiGetMethod', 'category/product-types/getAll'),
                ])
                this.manufacturerOptions = (mfRes.data || []).map(i => ({ id: i.id, name: i.name }))
                this.countryOfOriginOptions = (coRes.data || []).map(i => ({ id: i.id, name: i.name }))
                this.productTypeOptions = (ptRes.data || []).map(i => ({ id: i.id, name: i.name }))
            } catch (e) {
                console.error('Error loading filter options:', e)
            }
        },

        async loadData() {
            this.loading = true
            try {
                const query = buildQuery(this.filters, this.pagination)
                const { data, meta } = await this.$store.dispatch('apiGetMethod', `category/products?${query}`)
                this.tableData = data || []
                if (meta) {
                    this.pagination = {
                        currentPage: meta.current_page,
                        pageSize: meta.per_page,
                        total: meta.total,
                        totalPages: meta.last_page,
                        from: meta.from || 0,
                        to: meta.to || 0,
                    }
                }
            } catch (e) {
                console.error(e)
            } finally {
                this.loading = false
            }
        },

        toggleFilterPanel() { this.filterCollapsed = !this.filterCollapsed },

        handleKeywordChange(val) { this.filters.keyword = val },

        handleFilterChange(newFilters) { this.filters = { ...this.filters, ...newFilters } },

        handleSearch() { this.pagination.currentPage = 1; this.loadData() },

        handleReset() {
            this.filters = { ...initialStateForm }
            this.pagination.currentPage = 1
            this.loadData()
        },

        handleSort({ key, direction }) {
            const sortMap = { updatedAt: 'updated_at' }
            this.filters.sort_by = sortMap[key] || key
            this.filters.sort_desc = direction === 'desc'
        },

        handlePageChange(page) { this.pagination.currentPage = page; this.loadData() },

        handlePageSizeChange(size) {
            this.pagination.pageSize = size
            this.pagination.currentPage = 1
            this.loadData()
        },

        createItem() { this.$router.push('/category/products/create') },

        viewItem(item) { this.$router.push(`/category/products/${item.id}`) },

        editItem(item) {
            if (item.status === 2) return
            this.$router.push(`/category/products/${item.id}/edit`)
        },

        confirmDeleteItem(item) {
            this.itemToDelete = item
            this.$bvModal.show('confirm-delete-product')
        },

        async handleConfirmDelete() {
            if (!this.itemToDelete) return
            try {
                this.$nuxt.$loading.start()
                await this.$store.dispatch('apiDeleteMethod', `category/products/${this.itemToDelete.id}`)
                this.$nuxt.$loading.finish()
                this.$toasted.global.success({ message: 'Xóa thành công' })
                this.loadData()
            } catch (e) {
                this.$nuxt.$loading.finish()
                this.$toasted.global.error({ message: e?.response?.data?.message || 'Xóa thất bại' })
            } finally {
                this.itemToDelete = null
            }
        },

        confirmToggleLock(item) {
            this.itemToToggle = item
            this.$bvModal.show('confirm-toggle-lock-product')
        },

        async toggleLock() {
            if (!this.itemToToggle) return
            try {
                this.$nuxt.$loading.start()
                const action = this.itemToToggle.status === 2 ? 'unlock' : 'lock'
                await this.$store.dispatch('apiGetMethod', `category/products/${this.itemToToggle.id}/${action}`)
                this.$nuxt.$loading.finish()
                this.$toasted.global.success({ message: action === 'lock' ? 'Khoá thành công' : 'Mở khoá thành công' })
                this.loadData()
            } catch (e) {
                this.$nuxt.$loading.finish()
                this.$toasted.global.error({ message: e?.response?.data?.message || 'Thao tác thất bại' })
            } finally {
                this.itemToToggle = null
            }
        },

        async exportExcel() {
            try {
                this.$nuxt.$loading.start()
                const query = buildQueryString(this.filters)
                const response = await this.$store.dispatch('apiDownloadFile', `category/products/export?${query}`)
                const url = window.URL.createObjectURL(new Blob([response]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'danh_sach_hang_hoa.xls')
                document.body.appendChild(link)
                link.click()
                link.remove()
                this.$nuxt.$loading.finish()
            } catch (e) {
                this.$nuxt.$loading.finish()
                this.$toasted.global.error({ message: 'Xuất Excel thất bại' })
            }
        },

        renderStatus(status) {
            if (status === 1) return '<span class="badge badge-pill badge-success">Hoạt động</span>'
            return '<span class="badge badge-pill badge-secondary">Khoá</span>'
        },
    },
}
</script>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

---

## Phase 4: Frontend — Form tạo/sửa/xem

### Task 12: ProductForm component (dùng chung cho create/edit/view)

**Files:**
- Create: `pages/category/products/components/ProductForm.vue`

- [x] **Step 1: Tạo ProductForm.vue**

Component dùng chung cho 3 trang create/edit/view. Nhận props `mode` ('create'|'edit'|'view') và `productId`.

```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <div class="card shadow-sm">
                <div class="card-header bg-white d-flex align-items-center justify-content-between py-3">
                    <div class="d-flex align-items-center">
                        <div
                            class="d-flex align-items-center justify-content-center mr-2"
                            style="width: 28px; height: 28px; border-radius: 999px; background: rgba(22, 163, 74, 0.1); color: #16a34a;"
                        >
                            <i class="ri-shopping-bag-line" style="font-size: 16px"></i>
                        </div>
                        <div>
                            <h5 class="mb-0" style="font-size: 14px; font-weight: 800">
                                {{ mode === 'view' ? 'Xem chi tiết hàng hoá' : mode === 'edit' ? 'Sửa hàng hoá' : 'Tạo mới hàng hoá' }}
                            </h5>
                            <V2BaseMetaInfo
                                v-if="productId && (form.updated_at || form.updated_by_name)"
                                variant="chip"
                                :updated-at="form.updated_at"
                                :updated-by="form.updated_by_name"
                            />
                        </div>
                    </div>
                </div>

                <div class="card-body">
                    <!-- Section 1: Thông tin cơ bản -->
                    <h6 class="font-weight-bold mb-3">Thông tin cơ bản</h6>

                    <div class="form-row">
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>Mã hàng <Required v-if="!isView" /></V2BaseLabel>
                            <V2BaseInput
                                v-model.trim="form.code"
                                placeholder="VD: NL-BTTH01"
                                size="sm"
                                :disabled="isView"
                            />
                            <div v-if="formError['code']" class="text-small-error mt-1">
                                <i class="ri-error-warning-line mr-1"></i>{{ formError['code'] }}
                            </div>
                        </div>
                        <div class="col-md-6 mb-2">
                            <V2BaseLabel>Tên hàng hoá <Required v-if="!isView" /></V2BaseLabel>
                            <V2BaseInput
                                v-model="form.name"
                                placeholder="Nhập tên hàng hoá"
                                size="sm"
                                :disabled="isView"
                            />
                            <div v-if="formError['name']" class="text-small-error mt-1">
                                <i class="ri-error-warning-line mr-1"></i>{{ formError['name'] }}
                            </div>
                        </div>
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>Trạng thái</V2BaseLabel>
                            <V2BaseSelect
                                v-model="form.status"
                                :options="statusOptions"
                                size="sm"
                                :allowClear="false"
                                :disabled="isView"
                            />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>Hãng sản xuất</V2BaseLabel>
                            <V2BaseSelect
                                v-model="form.manufacturer_id"
                                :options="manufacturerOptions"
                                :allowClear="true"
                                placeholder="Chọn hãng sản xuất"
                                :disabled="isView"
                            />
                        </div>
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>Nước sản xuất</V2BaseLabel>
                            <V2BaseSelect
                                v-model="form.country_of_origin_id"
                                :options="countryOfOriginOptions"
                                :allowClear="true"
                                placeholder="Chọn nước sản xuất"
                                :disabled="isView"
                            />
                        </div>
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>Loại hàng hoá</V2BaseLabel>
                            <V2BaseSelect
                                v-model="form.product_type_id"
                                :options="productTypeOptions"
                                :allowClear="true"
                                placeholder="Chọn loại hàng hoá"
                                :disabled="isView"
                            />
                        </div>
                        <div class="col-md-3 mb-2">
                            <V2BaseLabel>VAT (%)</V2BaseLabel>
                            <V2BaseInput
                                v-model="form.vat"
                                type="number"
                                placeholder="VD: 8, 10"
                                size="sm"
                                :disabled="isView"
                            />
                            <div v-if="formError['vat']" class="text-small-error mt-1">
                                <i class="ri-error-warning-line mr-1"></i>{{ formError['vat'] }}
                            </div>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="col-md-12 mb-2">
                            <V2BaseLabel>Thông số kỹ thuật</V2BaseLabel>
                            <V2BaseTextarea
                                v-model="form.specifications"
                                rows="5"
                                placeholder="Nhập thông số kỹ thuật..."
                                size="sm"
                                :disabled="isView"
                            ></V2BaseTextarea>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="col-md-12 mb-2">
                            <V2BaseLabel>Mô tả</V2BaseLabel>
                            <V2BaseTextarea
                                v-model="form.description"
                                rows="3"
                                placeholder="Nhập mô tả..."
                                size="sm"
                                :disabled="isView"
                            ></V2BaseTextarea>
                        </div>
                    </div>

                    <!-- Section 2: Đơn vị tính & Bảng giá -->
                    <hr />
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="font-weight-bold mb-0">Đơn vị tính &amp; Bảng giá</h6>
                        <V2BaseButton v-if="!isView" secondary size="sm" @click="addUnit">
                            <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
                            Thêm đơn vị tính
                        </V2BaseButton>
                    </div>

                    <div v-if="formError['units']" class="text-small-error mb-2">
                        <i class="ri-error-warning-line mr-1"></i>{{ formError['units'] }}
                    </div>

                    <div class="table-responsive" v-if="form.units.length > 0">
                        <table class="table table-bordered table-sm mb-0">
                            <thead class="thead-light">
                                <tr>
                                    <th style="width: 80px" class="text-center">Cơ bản</th>
                                    <th style="width: 200px">Đơn vị tính</th>
                                    <th>Giá P0 (Net)</th>
                                    <th>Giá P3</th>
                                    <th>Giá P5</th>
                                    <th>Giá P7</th>
                                    <th>Giá P10</th>
                                    <th v-if="!isView" style="width: 50px"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(unit, index) in form.units" :key="index">
                                    <td class="text-center align-middle">
                                        <input
                                            type="radio"
                                            :checked="unit.is_base_unit == 1"
                                            :disabled="isView"
                                            @change="setBaseUnit(index)"
                                        />
                                    </td>
                                    <td>
                                        <V2BaseSelect
                                            v-model="unit.unit_id"
                                            :options="unitOptions"
                                            :allowClear="true"
                                            placeholder="Chọn ĐVT"
                                            size="sm"
                                            :disabled="isView"
                                        />
                                        <div v-if="unitErrors[index]" class="text-small-error mt-1">
                                            <i class="ri-error-warning-line mr-1"></i>{{ unitErrors[index] }}
                                        </div>
                                    </td>
                                    <td><V2BaseInput v-model="unit.price_p0" type="number" size="sm" placeholder="0" :disabled="isView" /></td>
                                    <td><V2BaseInput v-model="unit.price_p3" type="number" size="sm" placeholder="0" :disabled="isView" /></td>
                                    <td><V2BaseInput v-model="unit.price_p5" type="number" size="sm" placeholder="0" :disabled="isView" /></td>
                                    <td><V2BaseInput v-model="unit.price_p7" type="number" size="sm" placeholder="0" :disabled="isView" /></td>
                                    <td><V2BaseInput v-model="unit.price_p10" type="number" size="sm" placeholder="0" :disabled="isView" /></td>
                                    <td v-if="!isView" class="text-center align-middle">
                                        <button type="button" class="btn btn-sm btn-link text-danger p-0" @click="removeUnit(index)">
                                            <i class="ri-delete-bin-6-line"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-else class="text-muted small">Chưa có đơn vị tính nào.</div>

                    <!-- Section 3: Hình ảnh -->
                    <hr />
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="font-weight-bold mb-0">Hình ảnh sản phẩm</h6>
                        <V2BaseButton v-if="!isView" secondary size="sm" @click="triggerImageUpload">
                            <template #prefix><i class="ri-image-add-line" style="font-size: 13px"></i></template>
                            Thêm hình ảnh
                        </V2BaseButton>
                        <input
                            ref="imageInput"
                            type="file"
                            accept=".jpg,.jpeg,.png"
                            multiple
                            style="display: none"
                            @change="onImagesSelected"
                        />
                    </div>

                    <div class="d-flex flex-wrap" style="gap: 12px" v-if="form.images.length > 0">
                        <div
                            v-for="(img, index) in form.images"
                            :key="index"
                            class="position-relative border rounded"
                            style="width: 150px; height: 150px; overflow: hidden"
                        >
                            <div v-if="uploadingIndexes.includes(index)" class="d-flex align-items-center justify-content-center w-100 h-100">
                                <b-spinner small variant="primary"></b-spinner>
                            </div>
                            <img
                                v-else-if="img.file_path"
                                :src="img.file_path"
                                class="w-100 h-100"
                                style="object-fit: cover; cursor: pointer"
                                @click="previewImage(img.file_path)"
                            />
                            <button
                                v-if="!isView && !uploadingIndexes.includes(index)"
                                type="button"
                                class="btn btn-sm btn-danger position-absolute"
                                style="top: 4px; right: 4px; padding: 2px 6px; font-size: 11px"
                                @click="removeImage(index)"
                            >
                                <i class="ri-close-line"></i>
                            </button>
                            <div class="text-truncate small text-center px-1" style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(255,255,255,0.8)">
                                {{ img.file_name || '' }}
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-muted small">Chưa có hình ảnh nào.</div>

                    <!-- Meta info -->
                    <V2BaseMetaInfo
                        v-if="productId"
                        variant="block"
                        :created-by="form.created_by_name"
                        :created-at="form.created_at"
                        class="mt-3"
                    />
                </div>

                <!-- Footer -->
                <div class="card-footer bg-white d-flex align-items-center" style="gap: 8px">
                    <V2BaseButton v-if="!isView" primary @click="submitForm(1)" :disabled="isSubmitting">
                        <template #prefix><i class="ri-save-3-line mr-1"></i></template>
                        Lưu
                    </V2BaseButton>

                    <V2BaseButton v-if="mode === 'create'" secondary @click="submitForm(2)" :disabled="isSubmitting">
                        <template #prefix><i class="ri-save-3-line mr-1"></i></template>
                        Lưu &amp; Tiếp tục
                    </V2BaseButton>

                    <V2BaseButton v-if="isView && form.status === 1" secondary @click="goEdit">
                        <template #prefix><i class="ri-edit-line mr-1"></i></template>
                        Sửa
                    </V2BaseButton>

                    <V2BaseButton light @click="goBack" :disabled="isSubmitting">
                        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                        Quay lại
                    </V2BaseButton>
                </div>
            </div>
        </div>

        <!-- Image Preview Modal -->
        <b-modal id="preview-image-modal" hide-footer size="lg" centered>
            <template #modal-header="{ close }">
                <h5 class="modal-title">Xem ảnh</h5>
                <button type="button" class="close" @click="close()"><span>&times;</span></button>
            </template>
            <div class="text-center">
                <img :src="previewImageUrl" class="img-fluid" />
            </div>
        </b-modal>
    </div>
</template>

<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseTextarea from '@/components/V2BaseTextarea.vue'
import V2BaseMetaInfo from '@/components/V2BaseMetaInfo.vue'
import Required from '@/components/common/Required'

export default {
    components: {
        V2BaseButton, V2BaseLabel, V2BaseInput, V2BaseSelect,
        V2BaseTextarea, V2BaseMetaInfo, Required,
    },
    props: {
        mode: { type: String, default: 'create' },
        productId: { type: [Number, String], default: null },
    },
    data() {
        return {
            form: {
                code: '', name: '', status: 1,
                manufacturer_id: null, country_of_origin_id: null, product_type_id: null,
                vat: 0, specifications: '', description: '',
                units: [], images: [],
                created_by_name: '', created_at: '', updated_by_name: '', updated_at: '',
            },
            formError: {},
            unitErrors: {},
            isSubmitting: false,
            uploadingIndexes: [],
            previewImageUrl: '',
            statusOptions: [{ id: 1, name: 'Hoạt động' }, { id: 2, name: 'Khóa' }],
            manufacturerOptions: [],
            countryOfOriginOptions: [],
            productTypeOptions: [],
            unitOptions: [],
        }
    },
    computed: {
        isView() { return this.mode === 'view' },
    },
    async created() {
        await this.loadSelectOptions()
        if (this.productId) {
            await this.loadData()
        }
    },
    methods: {
        async loadSelectOptions() {
            try {
                const [mfRes, coRes, ptRes, uRes] = await Promise.all([
                    this.$store.dispatch('apiGetMethod', 'category/manufacturers/getAll'),
                    this.$store.dispatch('apiGetMethod', 'category/country-of-origins/getAll'),
                    this.$store.dispatch('apiGetMethod', 'category/product-types/getAll'),
                    this.$store.dispatch('apiGetMethod', 'category/units/getAll'),
                ])
                this.manufacturerOptions = (mfRes.data || []).map(i => ({ id: i.id, name: i.name }))
                this.countryOfOriginOptions = (coRes.data || []).map(i => ({ id: i.id, name: i.name }))
                this.productTypeOptions = (ptRes.data || []).map(i => ({ id: i.id, name: i.name }))
                this.unitOptions = (uRes.data || []).map(i => ({ id: i.id, name: i.name }))
            } catch (e) {
                console.error('Error loading options:', e)
            }
        },

        async loadData() {
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', `category/products/${this.productId}`)
                this.form = {
                    code: data.code || '',
                    name: data.name || '',
                    status: data.status || 1,
                    manufacturer_id: data.manufacturer_id || null,
                    country_of_origin_id: data.country_of_origin_id || null,
                    product_type_id: data.product_type_id || null,
                    vat: data.vat || 0,
                    specifications: data.specifications || '',
                    description: data.description || '',
                    units: (data.product_units || []).map(pu => ({
                        unit_id: pu.unit_id,
                        is_base_unit: pu.is_base_unit,
                        price_p0: pu.price_p0 || 0,
                        price_p3: pu.price_p3 || 0,
                        price_p5: pu.price_p5 || 0,
                        price_p7: pu.price_p7 || 0,
                        price_p10: pu.price_p10 || 0,
                    })),
                    images: (data.images || []).map(img => ({
                        file_path: img.file_path,
                        file_name: img.file_name,
                        file_size: img.file_size,
                    })),
                    created_by_name: data.created_by_name || '',
                    created_at: data.created_at || '',
                    updated_by_name: data.updated_by_name || '',
                    updated_at: data.updated_at || '',
                }
            } catch (e) {
                console.error('Error loading product:', e)
                const status = Number(e?.response?.status)
                if (status === 404) {
                    this.$toasted?.global?.error?.({ message: 'Dữ liệu đã thay đổi, vui lòng tải lại' })
                }
                this.$router.push('/category/products')
            }
        },

        addUnit() {
            this.form.units.push({
                unit_id: null, is_base_unit: this.form.units.length === 0 ? 1 : 0,
                price_p0: 0, price_p3: 0, price_p5: 0, price_p7: 0, price_p10: 0,
            })
        },

        removeUnit(index) {
            const wasBase = this.form.units[index].is_base_unit == 1
            this.form.units.splice(index, 1)
            if (wasBase && this.form.units.length > 0) {
                this.form.units[0].is_base_unit = 1
            }
        },

        setBaseUnit(index) {
            this.form.units.forEach((u, i) => { u.is_base_unit = i === index ? 1 : 0 })
        },

        validateUnits() {
            this.unitErrors = {}
            let valid = true
            const seen = new Set()
            this.form.units.forEach((u, i) => {
                if (!u.unit_id) {
                    this.unitErrors[i] = 'Vui lòng chọn đơn vị tính'
                    valid = false
                } else if (seen.has(u.unit_id)) {
                    this.unitErrors[i] = 'Đơn vị tính đã được chọn'
                    valid = false
                }
                if (u.unit_id) seen.add(u.unit_id)
            })
            return valid
        },

        triggerImageUpload() {
            this.$refs.imageInput.value = ''
            this.$refs.imageInput.click()
        },

        async onImagesSelected(e) {
            const files = Array.from(e.target.files || [])
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
            const maxSize = 20 * 1024 * 1024

            for (const file of files) {
                if (!allowedTypes.includes(file.type)) {
                    this.$toasted.global.error({ message: `${file.name}: Chỉ chấp nhận file .jpg, .jpeg, .png` })
                    continue
                }
                if (file.size > maxSize) {
                    this.$toasted.global.error({ message: `${file.name}: Kích thước tối đa 20MB` })
                    continue
                }

                const index = this.form.images.length
                this.form.images.push({ file_path: null, file_name: file.name, file_size: file.size })
                this.uploadingIndexes.push(index)

                try {
                    const formData = new FormData()
                    formData.append('attachments[]', file)
                    const response = await this.$store.dispatch('uploadImage', formData)
                    this.form.images[index].file_path = response.data.data[0]
                } catch (err) {
                    this.$toasted.global.error({ message: `Upload ${file.name} thất bại` })
                    this.form.images.splice(index, 1)
                } finally {
                    this.uploadingIndexes = this.uploadingIndexes.filter(i => i !== index)
                }
            }
        },

        removeImage(index) {
            this.form.images.splice(index, 1)
        },

        previewImage(url) {
            this.previewImageUrl = url
            this.$bvModal.show('preview-image-modal')
        },

        goEdit() {
            this.$router.push(`/category/products/${this.productId}/edit`)
        },

        goBack() {
            this.$router.push('/category/products')
        },

        resetForm() {
            this.form = {
                code: '', name: '', status: 1,
                manufacturer_id: null, country_of_origin_id: null, product_type_id: null,
                vat: 0, specifications: '', description: '',
                units: [], images: [],
                created_by_name: '', created_at: '', updated_by_name: '', updated_at: '',
            }
            this.formError = {}
            this.unitErrors = {}
        },

        async submitForm(action = 1) {
            this.isSubmitting = true
            this.formError = {}

            if (!this.validateUnits()) {
                this.isSubmitting = false
                return
            }

            try {
                this.$nuxt.$loading.start()

                const payload = {
                    code: (this.form.code || '').trim(),
                    name: (this.form.name || '').trim(),
                    status: this.form.status || 1,
                    manufacturer_id: this.form.manufacturer_id || null,
                    country_of_origin_id: this.form.country_of_origin_id || null,
                    product_type_id: this.form.product_type_id || null,
                    vat: this.form.vat || 0,
                    specifications: (this.form.specifications || '').trim(),
                    description: (this.form.description || '').trim(),
                    units: this.form.units.map(u => ({
                        unit_id: u.unit_id,
                        is_base_unit: u.is_base_unit,
                        price_p0: u.price_p0 || 0,
                        price_p3: u.price_p3 || 0,
                        price_p5: u.price_p5 || 0,
                        price_p7: u.price_p7 || 0,
                        price_p10: u.price_p10 || 0,
                    })),
                    images: this.form.images
                        .filter(img => img.file_path)
                        .map(img => ({
                            file_path: img.file_path,
                            file_name: img.file_name || null,
                            file_size: img.file_size || null,
                        })),
                }

                if (this.productId) {
                    payload.id = this.productId
                    await this.$store.dispatch('apiPutMethod', {
                        url: `category/products/${this.productId}`,
                        payload,
                    })
                } else {
                    await this.$store.dispatch('apiPostMethod', {
                        url: 'category/products',
                        payload,
                    })
                }

                this.$nuxt.$loading.finish()
                this.$toasted.global.success({
                    message: this.productId ? 'Cập nhật thành công' : 'Thêm mới thành công',
                })

                if (action === 1) {
                    this.$router.push('/category/products')
                } else if (action === 2) {
                    this.resetForm()
                }
            } catch (error) {
                this.$nuxt.$loading.finish()

                if (error.response && error.response.status === 422) {
                    this.formError = error.response.data.errors || {}
                }

                let errorMessage = this.productId ? 'Cập nhật thất bại' : 'Thêm mới thất bại'
                if (error?.response?.status === 404) {
                    errorMessage = 'Dữ liệu đã thay đổi, vui lòng tải lại'
                } else if (error?.response?.status === 422) {
                    errorMessage = 'Bạn chưa nhập đầy đủ thông tin'
                } else {
                    errorMessage = error?.response?.data?.message || errorMessage
                }
                this.$toasted.global.error({ message: errorMessage })
            } finally {
                this.isSubmitting = false
            }
        },
    },
}
</script>

<style lang="scss" scoped>
.text-small-error {
    font-size: 12px;
    color: #dc3545;
    display: flex;
    align-items: center;
}
</style>
```

---

### Task 13: Create page

**Files:**
- Create: `pages/category/products/create.vue`

- [x] **Step 1: Tạo create.vue**

```vue
<script>
import ProductForm from './components/ProductForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    mixins: [PageTitleMixin],
    head() { return { title: 'Tạo mới hàng hoá' } },
    components: { ProductForm },
    computed: { pageTitle() { return 'Tạo mới hàng hoá' } },
}
</script>

<template>
    <ProductForm mode="create" />
</template>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

---

### Task 14: Edit page

**Files:**
- Create: `pages/category/products/_id/edit.vue`

- [x] **Step 1: Tạo edit.vue**

```vue
<script>
import ProductForm from '../components/ProductForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    mixins: [PageTitleMixin],
    head() { return { title: 'Sửa hàng hoá' } },
    components: { ProductForm },
    computed: { pageTitle() { return 'Sửa hàng hoá' } },
}
</script>

<template>
    <ProductForm mode="edit" :productId="Number($route.params.id)" />
</template>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

---

### Task 15: View page

**Files:**
- Create: `pages/category/products/_id/index.vue`

- [x] **Step 1: Tạo view page**

```vue
<script>
import ProductForm from '../components/ProductForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    mixins: [PageTitleMixin],
    head() { return { title: 'Chi tiết hàng hoá' } },
    components: { ProductForm },
    computed: { pageTitle() { return 'Chi tiết hàng hoá' } },
}
</script>

<template>
    <ProductForm mode="view" :productId="Number($route.params.id)" />
</template>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

---

## Phase 5: Cập nhật isCanDelete các entity liên quan

### Task 16: Cập nhật isCanDelete cho Manufacturer, CountryOfOrigin, ProductType, Unit

**Files:**
- Modify: `Modules/Category/Entities/Manufacturer.php`
- Modify: `Modules/Category/Entities/CountryOfOrigin.php`
- Modify: `Modules/Category/Entities/ProductType.php`
- Modify: `Modules/Category/Entities/Unit.php`

- [x] **Step 1: Manufacturer — thêm relation + sửa isCanDelete**

Thêm vào `Manufacturer.php`:

```php
public function products()
{
    return $this->hasMany(Product::class, 'manufacturer_id');
}

// Sửa isCanDelete:
public function isCanDelete()
{
    return $this->products()->count() === 0;
}
```

- [x] **Step 2: CountryOfOrigin — thêm relation + sửa isCanDelete**

Thêm vào `CountryOfOrigin.php`:

```php
public function products()
{
    return $this->hasMany(Product::class, 'country_of_origin_id');
}

public function isCanDelete()
{
    return $this->products()->count() === 0;
}
```

- [x] **Step 3: ProductType — thêm relation + sửa isCanDelete**

Thêm vào `ProductType.php`:

```php
public function products()
{
    return $this->hasMany(Product::class, 'product_type_id');
}

public function isCanDelete()
{
    return $this->products()->count() === 0;
}
```

- [x] **Step 4: Unit — thêm relation + sửa isCanDelete**

Thêm vào `Unit.php`:

```php
use Modules\Category\Entities\ProductUnit;

public function productUnits()
{
    return $this->hasMany(ProductUnit::class, 'unit_id');
}

public function isCanDelete()
{
    return $this->productUnits()->count() === 0;
}
```

---

## Tổng kết file structure

### Backend (tạo mới):
```
Modules/Category/
├── Database/Migrations/
│   ├── 2026_06_03_000001_create_products_table.php
│   └── 2026_06_03_000002_create_product_units_table.php
├── Entities/
│   ├── Product.php
│   └── ProductUnit.php
├── Http/
│   ├── Controllers/Api/V1/ProductController.php
│   └── Requests/ProductRequest.php
├── Services/ProductService.php
└── Transformers/ProductResource/
    ├── ProductResource.php
    └── DetailProductResource.php

app/ExcelExport/ProductExport.php
resources/views/exports/products.blade.php
```

### Backend (sửa):
```
Modules/Category/Routes/api.php (thêm routes)
Modules/Category/Entities/Manufacturer.php (isCanDelete)
Modules/Category/Entities/CountryOfOrigin.php (isCanDelete)
Modules/Category/Entities/ProductType.php (isCanDelete)
Modules/Category/Entities/Unit.php (isCanDelete)
```

### Frontend (tạo mới):
```
pages/category/products/
├── index.vue
├── create.vue
├── components/
│   └── ProductForm.vue
└── _id/
    ├── index.vue
    └── edit.vue
```

### Checkpoint — Plan hoàn thành
- 16 tasks, 4 phases
- BE: 2 migration + 2 entity + 1 request + 1 service + 2 transformer + 1 controller + routes + export
- FE: 1 list page + 1 form component + 3 route pages (create/edit/view)
- Cập nhật isCanDelete cho 4 entity liên quan
