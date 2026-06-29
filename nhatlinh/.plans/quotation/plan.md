# Báo giá bán (Sale / Quotation) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans để thực thi task-by-task. Steps dùng checkbox (`- [ ]`).

**Goal:** Xây Báo giá BÁN độc lập, customer-centric trong phân hệ Kinh doanh (`Modules/Sale` + `pages/sale`): CRUD master-detail + workflow duyệt 1 cấp + xuất PDF, phân quyền theo cấp tổ chức.

**Architecture:** 2 bảng mới `sale_quotations` (header) + `sale_quotation_items` (dòng hàng). Service tính tiền BE (subtotal → CK tổng → phân bổ VAT → total) + đồng bộ items + chuyển trạng thái. Controller resource + submit/approve/reject/exportPdf. FE: list page (V2BaseFilterPanel + phân quyền cấp + filterStateMixin), form master-detail, modal duyệt/từ chối, tải PDF blob. KHÔNG đụng bản Báo giá hiện có trong `Modules/Assign`.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, spatie/permission, barryvdh/laravel-dompdf (cài mới).

**Spec:** `docs/superpowers/specs/2026-06-25-quotation-design.md`

## Global Constraints

- Repo API: `nhatlinh-api/` (chạy artisan tại đây). FE: `nhatlinh-client/`. **KHÔNG commit/push git. KHÔNG đọc vendor/, node_modules/.**
- KHÔNG có test tự động → verify bằng `php artisan migrate`, `php -l`, `tinker`, kiểm tra UI.
- Trạng thái: BE trả `status_name` + `status_color`, FE chỉ render `<V2BaseBadge :color>`. KHÔNG hardcode tên/màu ở FE.
- DB: `company_id/department_id/part_id` (unsignedBigInteger nullable), `created_by/updated_by` thủ công, `timestamps()`, KHÔNG SoftDeletes, KHÔNG `branch_id`. **KHÔNG `solution_version_id`** (ngoại lệ có chủ đích: báo giá bán độc lập, không gắn giải pháp).
- Form validate: BE rethrow `ValidationException` (không catch chung Exception); FE hiện lỗi inline (`is-invalid` + `invalid-feedback`) dùng flag `touched`.
- Permission: sửa trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, KHÔNG tạo migration permission. Route thao tác gắn `checkPermission`.
- Container trang dùng `V2Footer` → `padding-bottom: 60px`.
- Tiền tính ở BE; FE chỉ hiển thị realtime.
- Mã `BG-YYYY-NNNNN` sinh theo `max(id)` bảng `sale_quotations` (độc lập bảng `quotations` của Assign).

**File mẫu để copy (đọc khi implement):**
| Mục đích | File mẫu |
|---|---|
| Trait status badge | `Modules/Category/Entities/Concerns/HasStatusBadge.php` |
| Master-detail entity + sync items | `Modules/Category/Entities/{Bom,BomItem}.php`, `Modules/Category/Services/BomService.php:64-179` |
| getNextCode() | `Modules/Assign/Entities/Quotation.php:118-122` |
| BaseRequest | `Modules/Training/Http/Requests/BaseRequest.php` |
| Controller resource | `Modules/Category/Http/Controllers/Api/V1/ProductController.php` |
| Resource list/detail | `Modules/Category/Transformers/ProductResource/{ProductResource,DetailProductResource}.php` (extends `Modules\Human\Transformers\ApiResource`) |
| Routes + checkPermission | `Modules/Category/Routes/api.php` |
| **Phân quyền theo cấp (index)** | `Modules/Assign/Services/AssignRequestService.php:31-102` + helper `app/Helper/PermissionHelper.php` (`isCurrentEmployeeHasPermission`, `listManageDepartmentIds`, `listManagePartIds`) |
| FE list page (filter panel + phân quyền cấp + mixin) | `pages/assign/bom-list/index.vue`, filter cascading `components/.../V2BaseCompanyDepartmentFilter` |
| FE master-detail form | `pages/assign/quotations/_id/edit.vue` (tham khảo bảng dòng động + tính tổng) |
| FE export blob | `pages/assign/bom-list/index.vue` (handleExportList) |
| Store API | `store/actions.js` (`apiGetMethod`, `apiPostMethod`), `store/quotation.js` |
| Menu Sale | `components/default-menu/sale.js` |

**File Structure (sẽ tạo/sửa):**
| File | Trách nhiệm |
|---|---|
| `Modules/Sale/Database/Migrations/2026_06_25_000001_create_sale_quotations_table.php` | Bảng header |
| `Modules/Sale/Database/Migrations/2026_06_25_000002_create_sale_quotation_items_table.php` | Bảng dòng |
| `Modules/Sale/Entities/{SaleQuotation,SaleQuotationItem}.php` | Models |
| `Modules/Sale/Entities/Concerns/HasStatusBadge.php` | Trait (copy từ Category) |
| `Modules/Sale/Http/Requests/SaleQuotationRequest.php` | Validate store/update |
| `Modules/Sale/Http/Requests/SaleQuotationRejectRequest.php` | Validate từ chối |
| `Modules/Sale/Services/SaleQuotationService.php` | Tính tiền + sync items + workflow |
| `Modules/Sale/Transformers/SaleQuotationResource/{SaleQuotationResource,DetailSaleQuotationResource}.php` | API output |
| `Modules/Sale/Http/Controllers/Api/V1/QuotationController.php` | Endpoints |
| `Modules/Sale/Resources/views/pdf/quotation.blade.php` | Template PDF |
| `Modules/Sale/Routes/api.php` | Routes (sửa) |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | 8 permission (sửa) |
| FE `store/sale-quotation.js` | Store actions |
| FE `pages/sale/quotation/index.vue` | Danh sách |
| FE `pages/sale/quotation/_id/index.vue` | Xem chi tiết |
| FE `pages/sale/quotation/_id/edit.vue`, `pages/sale/quotation/create.vue` | Form thêm/sửa |
| FE `components/sale/quotation/{RejectModal,SubmitModal}.vue` | Modal workflow |
| FE `components/default-menu/sale.js` | Menu (sửa) |

---

## Phase 1: Backend — Database + Entities

### Task 1: Migration `sale_quotations`

**Files:** Create `nhatlinh-api/Modules/Sale/Database/Migrations/2026_06_25_000001_create_sale_quotations_table.php`

**Interfaces:** Produces bảng `sale_quotations` với các cột dưới (Service/Resource dựa vào).

- [ ] **Step 1:** Tạo migration:
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSaleQuotationsTable extends Migration
{
    public function up()
    {
        Schema::create('sale_quotations', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('code', 30)->unique()->comment('BG-YYYY-NNNNN');
            $table->unsignedBigInteger('customer_id');
            $table->unsignedBigInteger('customer_contact_id')->nullable();
            $table->date('quotation_date');
            $table->date('valid_until')->nullable();
            $table->decimal('subtotal', 18, 2)->default(0);
            $table->tinyInteger('discount_type')->nullable()->comment('1=%, 2=tiền');
            $table->decimal('discount_value', 18, 2)->default(0);
            $table->decimal('discount_amount', 18, 2)->default(0);
            $table->decimal('vat_amount', 18, 2)->default(0);
            $table->decimal('total_amount', 18, 2)->default(0);
            $table->tinyInteger('status')->default(1)->comment('1=Nháp,2=Chờ duyệt,3=Đã duyệt,4=Từ chối');
            $table->text('rejected_reason')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
            $table->index(['customer_id', 'status']);
            $table->index(['created_by', 'status']);
        });
    }
    public function down() { Schema::dropIfExists('sale_quotations'); }
}
```
> Ghi chú: KHÔNG có `solution_version_id` — báo giá bán hoàn toàn độc lập, không gắn Giải pháp/Dự án/BOM (lệch convention có chủ đích).
- [ ] **Step 2:** Run `cd nhatlinh-api && php artisan migrate`. Expected: `Migrated: ..._create_sale_quotations_table`.
- [ ] **Step 3:** Verify `php artisan tinker --execute="echo Schema::hasTable('sale_quotations')?'OK':'NO';"` → OK.

### Task 2: Migration `sale_quotation_items`

**Files:** Create `Modules/Sale/Database/Migrations/2026_06_25_000002_create_sale_quotation_items_table.php`

**Interfaces:** Produces bảng `sale_quotation_items` (cascade theo `quotation_id`).

- [ ] **Step 1:** Tạo migration:
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSaleQuotationItemsTable extends Migration
{
    public function up()
    {
        Schema::create('sale_quotation_items', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('quotation_id');
            $table->unsignedBigInteger('product_id');
            $table->unsignedBigInteger('unit_id')->nullable();
            $table->decimal('quantity', 18, 2)->default(0);
            $table->decimal('unit_price', 18, 2)->default(0);
            $table->decimal('vat_rate', 5, 2)->default(0);
            $table->decimal('line_amount', 18, 2)->default(0);
            $table->integer('sort_order')->default(0);
            $table->timestamps();
            $table->foreign('quotation_id')->references('id')->on('sale_quotations')->onDelete('cascade');
            $table->index('quotation_id');
        });
    }
    public function down() { Schema::dropIfExists('sale_quotation_items'); }
}
```
- [ ] **Step 2:** Run `php artisan migrate`. Expected: Migrated.
- [ ] **Step 3:** Verify tinker `Schema::hasTable('sale_quotation_items')` → OK.

### Task 3: Trait `HasStatusBadge` cho module Sale

**Files:** Create `Modules/Sale/Entities/Concerns/HasStatusBadge.php`

- [ ] **Step 1:** Copy nguyên file `Modules/Category/Entities/Concerns/HasStatusBadge.php`, đổi namespace dòng đầu thành `namespace Modules\Sale\Entities\Concerns;`. Giữ nguyên 3 method `statusDefinitions()`, `getStatusNameAttribute()`, `getStatusColorAttribute()`.
- [ ] **Step 2:** Verify `php -l Modules/Sale/Entities/Concerns/HasStatusBadge.php`.

### Task 4: Entity `SaleQuotation`

**Files:** Create `Modules/Sale/Entities/SaleQuotation.php`

**Interfaces:** Produces:
- consts `STATUS_DRAFT=1, STATUS_PENDING=2, STATUS_APPROVED=3, STATUS_REJECTED=4`
- `getNextCode(): string`, accessor `status_name/status_color/customer_name/employee_create_name/employee_update_name`
- relations `items()`, `customer()`, `contact()`
- `isCanEdit()`, `isCanDelete()`, `isCanSubmit()`, `isCanApprove()`

- [ ] **Step 1:** Tạo entity:
```php
<?php
namespace Modules\Sale\Entities;

use App\Models\BaseModel;
use Modules\Sale\Entities\Concerns\HasStatusBadge;
use Modules\Category\Entities\CustomerCategory;
use Modules\Category\Entities\CustomerCategoryContact;
use Modules\Human\Entities\Employee;

class SaleQuotation extends BaseModel
{
    use HasStatusBadge;

    const STATUS_DRAFT = 1;
    const STATUS_PENDING = 2;
    const STATUS_APPROVED = 3;
    const STATUS_REJECTED = 4;

    const STATUSES = [
        ['id' => 1, 'name' => 'Nháp', 'color' => '#6B7280'],
        ['id' => 2, 'name' => 'Chờ duyệt', 'color' => '#D97706'],
        ['id' => 3, 'name' => 'Đã duyệt', 'color' => '#059669'],
        ['id' => 4, 'name' => 'Từ chối', 'color' => '#DC2626'],
    ];

    protected $table = 'sale_quotations';

    protected $fillable = [
        'code', 'customer_id', 'customer_contact_id', 'quotation_date', 'valid_until',
        'subtotal', 'discount_type', 'discount_value', 'discount_amount', 'vat_amount', 'total_amount',
        'status', 'rejected_reason',
        'company_id', 'department_id', 'part_id', 'created_by', 'updated_by',
    ];

    protected $casts = [
        'quotation_date' => 'date:Y-m-d',
        'valid_until' => 'date:Y-m-d',
    ];

    public function getNextCode()
    {
        $maxId = static::max('id') ?? 0;
        return 'BG-' . date('Y') . '-' . str_pad($maxId + 1, 5, '0', STR_PAD_LEFT);
    }

    public function items()
    {
        return $this->hasMany(SaleQuotationItem::class, 'quotation_id')->orderBy('sort_order');
    }

    public function customer()
    {
        return $this->belongsTo(CustomerCategory::class, 'customer_id');
    }

    public function contact()
    {
        return $this->belongsTo(CustomerCategoryContact::class, 'customer_contact_id');
    }

    public function createdByEmployee()
    {
        return $this->belongsTo(Employee::class, 'created_by');
    }

    public function updatedByEmployee()
    {
        return $this->belongsTo(Employee::class, 'updated_by');
    }

    public function getCustomerNameAttribute()
    {
        return $this->customer ? $this->customer->code . ' - ' . $this->customer->name : null;
    }

    public function getEmployeeCreateNameAttribute()
    {
        return $this->createdByEmployee && $this->createdByEmployee->info
            ? $this->createdByEmployee->info->code . ' - ' . $this->createdByEmployee->info->fullname : null;
    }

    public function getEmployeeUpdateNameAttribute()
    {
        return $this->updatedByEmployee && $this->updatedByEmployee->info
            ? $this->updatedByEmployee->info->code . ' - ' . $this->updatedByEmployee->info->fullname : null;
    }

    public function isCanEdit()
    {
        return in_array((int) $this->status, [self::STATUS_DRAFT, self::STATUS_REJECTED]);
    }

    public function isCanDelete()
    {
        return (int) $this->status === self::STATUS_DRAFT;
    }

    public function isCanSubmit()
    {
        return in_array((int) $this->status, [self::STATUS_DRAFT, self::STATUS_REJECTED]);
    }

    public function isCanApprove()
    {
        return (int) $this->status === self::STATUS_PENDING;
    }
}
```
- [ ] **Step 2:** Verify `php -l Modules/Sale/Entities/SaleQuotation.php`.
- [ ] **Step 3:** Verify `php artisan tinker --execute="echo (new Modules\Sale\Entities\SaleQuotation)->getNextCode();"` → in ra `BG-2026-00001`.

### Task 5: Entity `SaleQuotationItem`

**Files:** Create `Modules/Sale/Entities/SaleQuotationItem.php`

**Interfaces:** Produces relations `quotation()`, `product()`, `unit()`.

- [ ] **Step 1:** Tạo entity:
```php
<?php
namespace Modules\Sale\Entities;

use App\Models\BaseModel;
use Modules\Category\Entities\Product;
use Modules\Category\Entities\Unit;

class SaleQuotationItem extends BaseModel
{
    protected $table = 'sale_quotation_items';

    protected $fillable = [
        'quotation_id', 'product_id', 'unit_id', 'quantity', 'unit_price',
        'vat_rate', 'line_amount', 'sort_order',
    ];

    public function quotation()
    {
        return $this->belongsTo(SaleQuotation::class, 'quotation_id');
    }

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
- [ ] **Step 2:** Verify `php -l Modules/Sale/Entities/SaleQuotationItem.php`. Xác nhận class `Modules\Category\Entities\Unit` tồn tại (đã thấy trong Category/Entities); nếu tên khác thì sửa import cho khớp.

---

## Phase 2: Backend — Request + Service

### Task 6: Request `SaleQuotationRequest` + `SaleQuotationRejectRequest`

**Files:** Create `Modules/Sale/Http/Requests/SaleQuotationRequest.php`, `Modules/Sale/Http/Requests/SaleQuotationRejectRequest.php`

**Interfaces:** Produces validate cho store/update + reject (`reason` required).

- [ ] **Step 1:** Tạo `SaleQuotationRequest` (extends BaseRequest của Training để có `failedValidation` ném ValidationException):
```php
<?php
namespace Modules\Sale\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;

class SaleQuotationRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'customer_id' => 'required|exists:category_customers,id',
            'customer_contact_id' => 'nullable|exists:customer_category_contacts,id',
            'quotation_date' => 'required|date',
            'valid_until' => 'nullable|date|after_or_equal:quotation_date',
            'discount_type' => 'nullable|in:1,2',
            'discount_value' => 'nullable|numeric|min:0',
            'items' => 'required|array|min:1',
            'items.*.product_id' => 'required|exists:products,id',
            'items.*.unit_id' => 'nullable|integer',
            'items.*.quantity' => 'required|numeric|gt:0',
            'items.*.unit_price' => 'required|numeric|min:0',
            'items.*.vat_rate' => 'nullable|numeric|min:0',
        ];
    }

    public function messages()
    {
        return [
            'customer_id.required' => 'Vui lòng chọn khách hàng',
            'quotation_date.required' => 'Vui lòng chọn ngày báo giá',
            'valid_until.after_or_equal' => 'Hiệu lực đến phải sau hoặc bằng ngày báo giá',
            'items.required' => 'Báo giá phải có ít nhất 1 dòng hàng',
            'items.min' => 'Báo giá phải có ít nhất 1 dòng hàng',
            'items.*.product_id.required' => 'Vui lòng chọn hàng hoá',
            'items.*.quantity.gt' => 'Số lượng phải lớn hơn 0',
            'items.*.unit_price.required' => 'Vui lòng nhập đơn giá',
        ];
    }
}
```
- [ ] **Step 2:** Tạo `SaleQuotationRejectRequest`:
```php
<?php
namespace Modules\Sale\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;

class SaleQuotationRejectRequest extends BaseRequest
{
    public function rules()
    {
        return ['reason' => 'required|string|max:1000'];
    }
    public function messages()
    {
        return ['reason.required' => 'Vui lòng nhập lý do từ chối'];
    }
}
```
- [ ] **Step 3:** Verify `php -l` cả 2 file. Xác nhận bảng contact tên `customer_category_contacts` (đã thấy migration `2026_06_05_000005_create_customer_category_contacts_table.php`).

### Task 7: Service `SaleQuotationService` — tính tiền + sync items + CRUD

**Files:** Create `Modules/Sale/Services/SaleQuotationService.php`

**Interfaces:**
- Consumes: `SaleQuotation`, `SaleQuotationItem`, helper `isCurrentEmployeeHasPermission`, `listManageDepartmentIds`, `listManagePartIds`, `auth()->user()`.
- Produces:
  - `getListForUser($request): Builder` — query đã lọc theo quyền cấp + filter.
  - `updateOrCreate(Request $request): SaleQuotation`
  - `destroy(SaleQuotation $q): void`
  - `recomputeTotals(SaleQuotation $q): void` — tính subtotal/discount/vat/total từ items đã lưu.
  - `submit/approve/reject($q[, $reason]): SaleQuotation`

- [ ] **Step 1:** Tạo khung service + import:
```php
<?php
namespace Modules\Sale\Services;

use Illuminate\Http\Request;
use Illuminate\Database\Eloquent\Builder;
use Modules\Sale\Entities\SaleQuotation;
use Modules\Sale\Entities\SaleQuotationItem;

class SaleQuotationService
{
    // ... các method bên dưới
}
```
- [ ] **Step 2:** `getListForUser` — phân quyền theo cấp (copy pattern `AssignRequestService::searchByFilter`, đổi tên quyền + cột):
```php
    public function getListForUser($request): Builder
    {
        $query = SaleQuotation::query()->with(['customer', 'createdByEmployee.info']);

        if (isCurrentEmployeeHasPermission('Xem tất cả báo giá bán')) {
            $query->where('status', '!=', SaleQuotation::STATUS_DRAFT);
        } elseif (isCurrentEmployeeHasPermission('Xem báo giá bán theo công ty')) {
            $query->where('company_id', auth()->user()->current_company_role);
        } elseif (isCurrentEmployeeHasPermission('Xem báo giá bán theo phòng ban')) {
            $deps = listManageDepartmentIds(); $parts = listManagePartIds();
            $query->where(function ($q) use ($deps, $parts) {
                $q->whereIn('department_id', $deps ?: [0])
                  ->orWhereIn('part_id', $parts ?: [0])
                  ->orWhere('created_by', auth()->user()->id);
            });
        } elseif (isCurrentEmployeeHasPermission('Xem báo giá bán theo bộ phận')) {
            $parts = listManagePartIds();
            $query->where(function ($q) use ($parts) {
                $q->whereIn('part_id', $parts ?: [0])
                  ->orWhere('created_by', auth()->user()->id);
            });
        } else {
            $query->where('created_by', auth()->user()->id);
        }

        if (!empty($request['keyword'])) {
            $query->where('code', 'like', '%' . $request['keyword'] . '%');
        }
        if (!empty($request['customer_id'])) $query->where('customer_id', $request['customer_id']);
        if (!empty($request['status'])) $query->where('status', $request['status']);
        if (!empty($request['company_id'])) $query->where('company_id', $request['company_id']);
        if (!empty($request['department_id'])) $query->where('department_id', $request['department_id']);
        if (!empty($request['part_id'])) $query->where('part_id', $request['part_id']);
        if (!empty($request['from_date'])) $query->whereDate('quotation_date', '>=', $request['from_date']);
        if (!empty($request['to_date'])) $query->whereDate('quotation_date', '<=', $request['to_date']);

        return $query->orderByDesc('id');
    }
```
- [ ] **Step 3:** `updateOrCreate` — tạo/sửa header + sync items + tính tiền, trong transaction (controller đã bọc DB::transaction, ở đây không bọc lại):
```php
    public function updateOrCreate(Request $request): SaleQuotation
    {
        $payload = [
            'customer_id' => $request->customer_id,
            'customer_contact_id' => $request->customer_contact_id,
            'quotation_date' => $request->quotation_date,
            'valid_until' => $request->valid_until,
            'discount_type' => $request->discount_type,
            'discount_value' => $request->discount_value ?? 0,
            'company_id' => auth()->user()->info->company_id ?? null,
            'department_id' => auth()->user()->info->department_id ?? null,
            'part_id' => auth()->user()->info->part_id ?? null,
            'updated_by' => auth()->user()->id,
        ];

        if ($request->id) {
            $quotation = SaleQuotation::findOrFail($request->id);
            $quotation->update($payload);
        } else {
            $quotation = new SaleQuotation();
            $quotation->fill($payload);
            $quotation->status = SaleQuotation::STATUS_DRAFT;
            $quotation->created_by = auth()->user()->id;
            $quotation->code = $quotation->getNextCode();
            $quotation->save();
        }

        $this->syncItems($quotation, $request->items ?? []);
        $this->recomputeTotals($quotation);
        return $quotation->fresh('items');
    }

    protected function syncItems(SaleQuotation $quotation, array $items): void
    {
        $quotation->items()->delete();
        foreach (array_values($items) as $i => $it) {
            if (empty($it['product_id'])) continue;
            $qty = (float) ($it['quantity'] ?? 0);
            $price = (float) ($it['unit_price'] ?? 0);
            $quotation->items()->create([
                'product_id' => $it['product_id'],
                'unit_id' => $it['unit_id'] ?? null,
                'quantity' => $qty,
                'unit_price' => $price,
                'vat_rate' => $it['vat_rate'] ?? 0,
                'line_amount' => round($qty * $price, 2),
                'sort_order' => $i,
            ]);
        }
    }
```
- [ ] **Step 4:** `recomputeTotals` — công thức spec mục 4 (subtotal → CK → phân bổ VAT → total):
```php
    public function recomputeTotals(SaleQuotation $quotation): void
    {
        $items = $quotation->items()->get();
        $subtotal = round($items->sum('line_amount'), 2);

        $discountAmount = 0;
        if ((int) $quotation->discount_type === 1) {
            $discountAmount = round($subtotal * ((float) $quotation->discount_value) / 100, 2);
        } elseif ((int) $quotation->discount_type === 2) {
            $discountAmount = min((float) $quotation->discount_value, $subtotal);
        }

        $vatAmount = 0;
        foreach ($items as $it) {
            $alloc = $subtotal > 0 ? $discountAmount * ((float) $it->line_amount / $subtotal) : 0;
            $vatAmount += round(((float) $it->line_amount - $alloc) * ((float) $it->vat_rate) / 100, 2);
        }
        $vatAmount = round($vatAmount, 2);

        $quotation->update([
            'subtotal' => $subtotal,
            'discount_amount' => $discountAmount,
            'vat_amount' => $vatAmount,
            'total_amount' => round(($subtotal - $discountAmount) + $vatAmount, 2),
        ]);
    }
```
- [ ] **Step 5:** workflow + destroy:
```php
    public function submit(SaleQuotation $quotation): SaleQuotation
    {
        $quotation->update([
            'status' => SaleQuotation::STATUS_PENDING,
            'rejected_reason' => null,
            'updated_by' => auth()->user()->id,
        ]);
        return $quotation;
    }

    public function approve(SaleQuotation $quotation): SaleQuotation
    {
        $quotation->update(['status' => SaleQuotation::STATUS_APPROVED, 'updated_by' => auth()->user()->id]);
        return $quotation;
    }

    public function reject(SaleQuotation $quotation, string $reason): SaleQuotation
    {
        $quotation->update([
            'status' => SaleQuotation::STATUS_REJECTED,
            'rejected_reason' => $reason,
            'updated_by' => auth()->user()->id,
        ]);
        return $quotation;
    }

    public function destroy(SaleQuotation $quotation): void
    {
        $quotation->items()->delete();
        $quotation->delete();
    }
```
- [ ] **Step 6:** Verify `php -l Modules/Sale/Services/SaleQuotationService.php`.

---

## Phase 3: Backend — Resources + Controller + Routes

### Task 8: Resources list + detail

**Files:** Create `Modules/Sale/Transformers/SaleQuotationResource/SaleQuotationResource.php`, `Modules/Sale/Transformers/SaleQuotationResource/DetailSaleQuotationResource.php`

**Interfaces:** Produces JSON list + detail (kèm `status_name/status_color`, các flag is_can_*).

- [ ] **Step 1:** List resource:
```php
<?php
namespace Modules\Sale\Transformers\SaleQuotationResource;

use Modules\Human\Transformers\ApiResource;

class SaleQuotationResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'customer_id' => $this->customer_id,
            'customer_name' => $this->customer_name,
            'quotation_date' => optional($this->quotation_date)->format('Y-m-d'),
            'valid_until' => optional($this->valid_until)->format('Y-m-d'),
            'total_amount' => $this->total_amount,
            'status' => $this->status,
            'status_name' => $this->status_name,
            'status_color' => $this->status_color,
            'employee_create_name' => $this->employee_create_name,
            'created_at' => optional($this->created_at)->format('Y-m-d H:i'),
            'is_can_edit' => $this->isCanEdit(),
            'is_can_delete' => $this->isCanDelete(),
            'is_can_submit' => $this->isCanSubmit(),
            'is_can_approve' => $this->isCanApprove(),
        ];
    }
}
```
- [ ] **Step 2:** Detail resource (thêm items + dữ liệu tính tiền + contact):
```php
<?php
namespace Modules\Sale\Transformers\SaleQuotationResource;

use Modules\Human\Transformers\ApiResource;

class DetailSaleQuotationResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'customer_id' => $this->customer_id,
            'customer_name' => $this->customer_name,
            'customer_contact_id' => $this->customer_contact_id,
            'quotation_date' => optional($this->quotation_date)->format('Y-m-d'),
            'valid_until' => optional($this->valid_until)->format('Y-m-d'),
            'subtotal' => $this->subtotal,
            'discount_type' => $this->discount_type,
            'discount_value' => $this->discount_value,
            'discount_amount' => $this->discount_amount,
            'vat_amount' => $this->vat_amount,
            'total_amount' => $this->total_amount,
            'status' => $this->status,
            'status_name' => $this->status_name,
            'status_color' => $this->status_color,
            'rejected_reason' => $this->rejected_reason,
            'is_can_edit' => $this->isCanEdit(),
            'is_can_delete' => $this->isCanDelete(),
            'is_can_submit' => $this->isCanSubmit(),
            'is_can_approve' => $this->isCanApprove(),
            'items' => $this->items->map(function ($it) {
                return [
                    'id' => $it->id,
                    'product_id' => $it->product_id,
                    'product_name' => optional($it->product)->name,
                    'product_code' => optional($it->product)->code,
                    'unit_id' => $it->unit_id,
                    'unit_name' => optional($it->unit)->name,
                    'quantity' => $it->quantity,
                    'unit_price' => $it->unit_price,
                    'vat_rate' => $it->vat_rate,
                    'line_amount' => $it->line_amount,
                ];
            }),
        ];
    }
}
```
- [ ] **Step 3:** Verify `php -l` cả 2.

### Task 9: Controller `QuotationController`

**Files:** Create `Modules/Sale/Http/Controllers/Api/V1/QuotationController.php`

**Interfaces:** Consumes `SaleQuotationService`, `SaleQuotationRequest`, `SaleQuotationRejectRequest`, Resources. Produces endpoints index/show/store(updateOrCreate)/update/destroy/submit/approve/reject/exportPdf.

- [ ] **Step 1:** Tạo controller (theo pattern ProductController + index như Assign QuotationController):
```php
<?php
namespace Modules\Sale\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;
use Modules\Sale\Entities\SaleQuotation;
use Modules\Sale\Services\SaleQuotationService;
use Modules\Sale\Http\Requests\SaleQuotationRequest;
use Modules\Sale\Http\Requests\SaleQuotationRejectRequest;
use Modules\Sale\Transformers\SaleQuotationResource\SaleQuotationResource;
use Modules\Sale\Transformers\SaleQuotationResource\DetailSaleQuotationResource;

class QuotationController extends ApiController
{
    protected $service;

    public function __construct(SaleQuotationService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        try {
            $query = $this->service->getListForUser($request->all());
            return $this->apiGetList(SaleQuotationResource::apiPaginate($query, $request));
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show($id)
    {
        $quotation = SaleQuotation::with(['items.product', 'items.unit', 'customer', 'contact'])->findOrFail($id);
        return $this->responseJson('success', Response::HTTP_OK, new DetailSaleQuotationResource($quotation));
    }

    public function updateOrCreate(SaleQuotationRequest $request)
    {
        try {
            return DB::transaction(function () use ($request) {
                if ($request->id) {
                    $existing = SaleQuotation::find($request->id);
                    if ($existing && !$existing->isCanEdit()) {
                        return $this->responseBadRequest('Báo giá ở trạng thái này không thể sửa');
                    }
                }
                $quotation = $this->service->updateOrCreate($request);
                return $this->responseJson('success', Response::HTTP_OK, new DetailSaleQuotationResource(
                    $quotation->load(['items.product', 'items.unit', 'customer', 'contact'])
                ));
            });
        } catch (\Illuminate\Validation\ValidationException $e) {
            throw $e;
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function destroy($id)
    {
        try {
            return DB::transaction(function () use ($id) {
                $quotation = SaleQuotation::findOrFail($id);
                if (!$quotation->isCanDelete()) {
                    return $this->responseBadRequest('Chỉ được xóa báo giá ở trạng thái Nháp');
                }
                $this->service->destroy($quotation);
                return $this->responseJson('success', Response::HTTP_OK);
            });
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function submit($id)
    {
        try {
            $quotation = SaleQuotation::findOrFail($id);
            if (!$quotation->isCanSubmit()) {
                return $this->responseBadRequest('Báo giá không ở trạng thái gửi duyệt được');
            }
            if ((int) $quotation->created_by !== (int) auth()->user()->id) {
                return $this->responseBadRequest('Chỉ người tạo được gửi duyệt');
            }
            return $this->responseJson('success', Response::HTTP_OK, $this->service->submit($quotation));
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function approve($id)
    {
        try {
            $quotation = SaleQuotation::findOrFail($id);
            if (!$quotation->isCanApprove()) {
                return $this->responseBadRequest('Báo giá không ở trạng thái chờ duyệt');
            }
            return $this->responseJson('success', Response::HTTP_OK, $this->service->approve($quotation));
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function reject(SaleQuotationRejectRequest $request, $id)
    {
        try {
            $quotation = SaleQuotation::findOrFail($id);
            if (!$quotation->isCanApprove()) {
                return $this->responseBadRequest('Báo giá không ở trạng thái chờ duyệt');
            }
            return $this->responseJson('success', Response::HTTP_OK, $this->service->reject($quotation, $request->reason));
        } catch (\Illuminate\Validation\ValidationException $e) {
            throw $e;
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function exportPdf($id)
    {
        try {
            $quotation = SaleQuotation::with(['items.product', 'items.unit', 'customer', 'contact'])->findOrFail($id);
            $pdf = \PDF::loadView('sale::pdf.quotation', ['q' => $quotation]);
            return $pdf->stream($quotation->code . '.pdf');
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
}
```
- [ ] **Step 2:** Verify `php -l Modules/Sale/Http/Controllers/Api/V1/QuotationController.php`.

### Task 10: Routes

**Files:** Modify `Modules/Sale/Routes/api.php`

- [ ] **Step 1:** Thêm `use` + group `/quotations` vào trong group `/v1/sale` hiện có (giữ dòng dashboard). Nội dung:
```php
use Modules\Sale\Http\Controllers\Api\V1\QuotationController;

// ... bên trong Route::group(['prefix' => '/v1/sale', 'middleware' => 'auth:api'], function () {
    Route::group(['prefix' => '/quotations'], function () {
        Route::get('/', [QuotationController::class, 'index'])
            ->middleware('checkPermission:Xem tất cả báo giá bán|Xem báo giá bán theo công ty|Xem báo giá bán theo phòng ban|Xem báo giá bán theo bộ phận');
        Route::get('/{id}', [QuotationController::class, 'show']);
        Route::post('/', [QuotationController::class, 'updateOrCreate'])
            ->middleware('checkPermission:Thêm báo giá bán|Sửa báo giá bán');
        Route::delete('/{id}', [QuotationController::class, 'destroy'])
            ->middleware('checkPermission:Xóa báo giá bán');
        Route::post('/{id}/submit', [QuotationController::class, 'submit']);
        Route::post('/{id}/approve', [QuotationController::class, 'approve'])
            ->middleware('checkPermission:Duyệt báo giá bán');
        Route::post('/{id}/reject', [QuotationController::class, 'reject'])
            ->middleware('checkPermission:Duyệt báo giá bán');
        Route::get('/{id}/pdf', [QuotationController::class, 'exportPdf']);
    });
```
> `updateOrCreate` gộp thêm/sửa → gắn cả 2 quyền `Thêm|Sửa`. (Phân biệt sâu hơn để Service/Controller kiểm tra `isCanEdit` như đã có.)
- [ ] **Step 2:** Verify `php -l Modules/Sale/Routes/api.php`.
- [ ] **Step 3:** Verify route nạp được: `php artisan route:list --path=sale/quotations` → liệt kê đủ route.

---

## Phase 4: Backend — Permissions + PDF

### Task 11: 8 permission mới

**Files:** Modify `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [ ] **Step 1:** Tìm id permission lớn nhất hiện dùng: `grep -oE "'id' => [0-9]+" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort -t'>' -k2 -n | tail -3`. Chọn 8 id trống kế tiếp (gọi `<id1>..<id8>`).
- [ ] **Step 2:** Thêm khối (group `Báo giá bán`, đặt cạnh nhóm permission danh mục/kinh doanh; thay `<idN>` bằng id thực tế; `type` lấy theo giá trị các permission cùng khu vực — tham khảo dòng lân cận, mặc định `4`):
```php
        // Báo giá bán (Sale)
        Permission::create(['id' => <id1>, 'guard_name' => 'api', 'name' => 'Xem tất cả báo giá bán', 'display_name' => 'Xem tất cả báo giá bán', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id2>, 'guard_name' => 'api', 'name' => 'Xem báo giá bán theo công ty', 'display_name' => 'Xem báo giá bán theo công ty', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id3>, 'guard_name' => 'api', 'name' => 'Xem báo giá bán theo phòng ban', 'display_name' => 'Xem báo giá bán theo phòng ban', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id4>, 'guard_name' => 'api', 'name' => 'Xem báo giá bán theo bộ phận', 'display_name' => 'Xem báo giá bán theo bộ phận', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id5>, 'guard_name' => 'api', 'name' => 'Thêm báo giá bán', 'display_name' => 'Thêm báo giá bán', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id6>, 'guard_name' => 'api', 'name' => 'Sửa báo giá bán', 'display_name' => 'Sửa báo giá bán', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id7>, 'guard_name' => 'api', 'name' => 'Xóa báo giá bán', 'display_name' => 'Xóa báo giá bán', 'group' => 'Báo giá bán', 'type' => 4]);
        Permission::create(['id' => <id8>, 'guard_name' => 'api', 'name' => 'Duyệt báo giá bán', 'display_name' => 'Duyệt báo giá bán', 'group' => 'Báo giá bán', 'type' => 4]);
```
- [ ] **Step 3:** Insert vào DB dev + gán Super admin (KHÔNG re-seed toàn bộ). Chạy tinker (kiểm tra tên role admin thực tế trước):
```bash
php artisan tinker --execute="
use App\Models\Permission; use App\Models\Role;
\$names=['Xem tất cả báo giá bán','Xem báo giá bán theo công ty','Xem báo giá bán theo phòng ban','Xem báo giá bán theo bộ phận','Thêm báo giá bán','Sửa báo giá bán','Xóa báo giá bán','Duyệt báo giá bán'];
foreach(\$names as \$n){ Permission::firstOrCreate(['name'=>\$n,'guard_name'=>'api'],['display_name'=>\$n,'group'=>'Báo giá bán','type'=>4]); }
\$admin=Role::where('name','Super Admin')->orWhere('name','Super admin')->orWhere('name','Admin')->first();
if(\$admin){ \$admin->givePermissionTo(\$names); }
app()->make(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions();
echo 'perm done; admin='.(\$admin?\$admin->name:'NONE');
"
```
- [ ] **Step 4:** Verify `php artisan tinker --execute="echo App\Models\Permission::where('name','Duyệt báo giá bán')->count();"` → 1.

### Task 12: Cài dompdf + template PDF

**Files:** Create `Modules/Sale/Resources/views/pdf/quotation.blade.php`; Modify `nhatlinh-api/composer.json` (qua composer require)

- [ ] **Step 1:** Cài package (PHP 7.4 → dùng `^1.0`): `cd nhatlinh-api && composer require barryvdh/laravel-dompdf:^1.0`. Expected: cài xong, auto-discovery đăng ký facade `Barryvdh\DomPDF\Facade\Pdf` alias `PDF`.
- [ ] **Step 2:** Xác nhận view namespace `sale::` hoạt động (module nwidart tự đăng ký `Resources/views`). Kiểm tra `Modules/Sale/Providers/SaleServiceProvider.php` có `loadViewsFrom(..., 'sale')` — nếu chưa, view path mặc định module là `sale::`. Verify bằng Task 12 step 4.
- [ ] **Step 3:** Tạo `Modules/Sale/Resources/views/pdf/quotation.blade.php`:
```blade
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <style>
        * { font-family: DejaVu Sans, sans-serif; font-size: 12px; }
        h2 { text-align: center; margin: 0 0 4px; }
        table { width: 100%; border-collapse: collapse; margin-top: 8px; }
        th, td { border: 1px solid #333; padding: 4px 6px; }
        th { background: #f0f0f0; }
        .text-right { text-align: right; }
        .text-center { text-align: center; }
        .no-border td { border: none; padding: 2px 0; }
    </style>
</head>
<body>
    <h2>BÁO GIÁ</h2>
    <div class="text-center">Số: {{ $q->code }}</div>
    <table class="no-border" style="margin-top:10px;">
        <tr><td style="width:50%">Khách hàng: {{ optional($q->customer)->name }}</td>
            <td>Ngày báo giá: {{ optional($q->quotation_date)->format('d/m/Y') }}</td></tr>
        <tr><td>Người liên hệ: {{ optional($q->contact)->fullname }}</td>
            <td>Hiệu lực đến: {{ optional($q->valid_until)->format('d/m/Y') }}</td></tr>
    </table>
    <table>
        <thead>
            <tr>
                <th class="text-center">STT</th><th>Hàng hoá</th><th class="text-center">ĐVT</th>
                <th class="text-right">SL</th><th class="text-right">Đơn giá</th>
                <th class="text-right">VAT %</th><th class="text-right">Thành tiền</th>
            </tr>
        </thead>
        <tbody>
            @foreach($q->items as $i => $it)
            <tr>
                <td class="text-center">{{ $i + 1 }}</td>
                <td>{{ optional($it->product)->name }}</td>
                <td class="text-center">{{ optional($it->unit)->name }}</td>
                <td class="text-right">{{ number_format($it->quantity, 0, ',', '.') }}</td>
                <td class="text-right">{{ number_format($it->unit_price, 0, ',', '.') }}</td>
                <td class="text-right">{{ $it->vat_rate }}</td>
                <td class="text-right">{{ number_format($it->line_amount, 0, ',', '.') }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
    <table class="no-border" style="margin-top:8px; width:40%; float:right;">
        <tr><td>Tạm tính:</td><td class="text-right">{{ number_format($q->subtotal, 0, ',', '.') }}</td></tr>
        <tr><td>Chiết khấu:</td><td class="text-right">{{ number_format($q->discount_amount, 0, ',', '.') }}</td></tr>
        <tr><td>VAT:</td><td class="text-right">{{ number_format($q->vat_amount, 0, ',', '.') }}</td></tr>
        <tr><td><strong>Tổng cộng:</strong></td><td class="text-right"><strong>{{ number_format($q->total_amount, 0, ',', '.') }}</strong></td></tr>
    </table>
</body>
</html>
```
- [ ] **Step 4:** Verify: tạo 1 báo giá test qua tinker (hoặc dùng sau khi có FE), gọi `GET /api/v1/sale/quotations/{id}/pdf` → tải về file PDF mở được. Tạm thời verify render view: `php artisan tinker --execute="echo view('sale::pdf.quotation', ['q' => Modules\Sale\Entities\SaleQuotation::with('items.product','items.unit','customer','contact')->first()])->render() ? 'VIEW_OK' : 'NO';"` (sau khi đã có ít nhất 1 bản ghi; nếu chưa có bản ghi, bỏ qua tới Phase 7).

---

## Phase 5: Frontend — Store + Menu + Danh sách

### Task 13: Store `sale-quotation.js`

**Files:** Create `nhatlinh-client/store/sale-quotation.js`

**Interfaces:** Produces actions dùng `apiGetMethod`/`apiPostMethod` (root). Tham khảo `store/quotation.js`.

- [ ] **Step 1:** Tạo store:
```javascript
export const actions = {
    async list({ dispatch }, query) {
        return await dispatch('apiGetMethod', `sale/quotations${query || ''}`, { root: true })
    },
    async detail({ dispatch }, id) {
        return await dispatch('apiGetMethod', `sale/quotations/${id}`, { root: true })
    },
    async save({ dispatch }, payload) {
        return await dispatch('apiPostMethod', { url: 'sale/quotations', payload }, { root: true })
    },
    async remove({ dispatch }, id) {
        return await dispatch('apiDeleteMethod', { url: `sale/quotations/${id}` }, { root: true })
    },
    async submit({ dispatch }, id) {
        return await dispatch('apiPostMethod', { url: `sale/quotations/${id}/submit`, payload: {} }, { root: true })
    },
    async approve({ dispatch }, id) {
        return await dispatch('apiPostMethod', { url: `sale/quotations/${id}/approve`, payload: {} }, { root: true })
    },
    async reject({ dispatch }, { id, reason }) {
        return await dispatch('apiPostMethod', { url: `sale/quotations/${id}/reject`, payload: { reason } }, { root: true })
    },
}
```
- [ ] **Step 2:** Xác nhận tên action xóa thực tế trong `store/actions.js` (`apiDeleteMethod` hay tên khác — grep). Nếu khác, sửa cho khớp. (Nếu chỉ có `apiGetMethod`/`apiPostMethod`, dùng axios trực tiếp như các trang khác.)

### Task 14: Menu Sale — thêm mục Báo giá

**Files:** Modify `nhatlinh-client/components/default-menu/sale.js`

- [ ] **Step 1:** Thêm item vào `saleItems`:
```javascript
export const saleItems = [
    {
        label: 'Tổng quan',
        link: '/sale/dashboard',
    },
    {
        label: 'Báo giá',
        link: '/sale/quotation',
    },
]
```
- [ ] **Step 2:** Verify: chạy FE, menu phân hệ Kinh doanh hiện mục "Báo giá".

### Task 15: Danh sách `pages/sale/quotation/index.vue`

**Files:** Create `nhatlinh-client/pages/sale/quotation/index.vue`

**Interfaces:** Consumes store `sale-quotation/list`, `sale-quotation/remove`, `sale-quotation/submit/approve/reject`. Dùng `V2BaseFilterPanel`, `V2BaseCompanyDepartmentFilter`, `filterStateMixin`, `V2BaseBadge`, `V2BaseButton`.

- [ ] **Step 1:** Copy khung từ `pages/assign/bom-list/index.vue` (đã có V2BaseFilterPanel + phân quyền cấp + filterStateMixin + auto-search). Đổi:
  - Endpoint `assign/bom-lists` → `sale/quotations` (dùng store action `sale-quotation/list`).
  - `localStorageKey: 'sale_quotation'`, `pathsToKeep: ['/sale/quotation']`.
  - Tiêu đề panel "Bộ lọc Báo giá".
- [ ] **Step 2:** `initialStateForm` + `filters` gồm: `keyword, customer_id, status, company_id, department_id, part_id, from_date, to_date`. `ignoredFields: ['keyword']`. Cài deep watcher auto-search + `oldFilters` theo list-page skill.
- [ ] **Step 3:** Cột bảng: STT, Mã (`code`), Khách hàng (`customer_name`), Ngày BG (`quotation_date`), Hiệu lực (`valid_until`), Tổng tiền (`total_amount`, format số), Trạng thái:
```html
<V2BaseBadge :color="row.status_color" size="sm">{{ row.status_name }}</V2BaseBadge>
```
- [ ] **Step 4:** Cột thao tác (theo flag từ BE):
  - Xem → `/sale/quotation/{id}` (luôn có)
  - Sửa (`row.is_can_edit`) → `/sale/quotation/{id}/edit`
  - Gửi duyệt (`row.is_can_submit`) → gọi `sale-quotation/submit` qua SubmitModal
  - Duyệt / Từ chối (`row.is_can_approve`) → approve / mở RejectModal
  - Xuất PDF → `handleExportPdf(row)` (Task 18 cơ chế blob)
  - Xóa (`row.is_can_delete`) → confirm → `sale-quotation/remove`
- [ ] **Step 5:** Filter panel: dùng `V2BaseCompanyDepartmentFilter :form="filters" :permissions="permissions"` (cascading Công ty→Phòng ban→Bộ phận) + dropdown KH (load `category/customers`) + dropdown trạng thái (options `[{id:1,name:'Nháp'},{id:2,name:'Chờ duyệt'},{id:3,name:'Đã duyệt'},{id:4,name:'Từ chối'}]`) + 2 datepicker from/to. Nút "Tạo mới" → `/sale/quotation/create` (ẩn nếu không có quyền Thêm).
- [ ] **Step 6:** `<style lang="scss">` thêm `@import '@/assets/scss/v2-styles.scss';`. Container `padding-bottom: 60px`.
- [ ] **Step 7:** Verify: mở `/sale/quotation`, danh sách load, filter auto-search hoạt động, badge trạng thái đúng màu.

---

## Phase 6: Frontend — Form master-detail + Workflow + PDF

### Task 16: Form thêm/sửa `create.vue` + `_id/edit.vue`

**Files:** Create `nhatlinh-client/pages/sale/quotation/create.vue`, `nhatlinh-client/pages/sale/quotation/_id/edit.vue`

**Interfaces:** Consumes store `sale-quotation/save`, `sale-quotation/detail`. Dùng V2BaseSelect, V2BaseInput, V2BaseDatePicker, V2BaseButton.

- [ ] **Step 1:** Tạo 1 component dùng chung `components/sale/quotation/QuotationForm.vue` để cả create/edit dùng (giảm trùng lặp). Props: `quotationId` (null = tạo mới). State `form`:
```javascript
data() {
  return {
    form: {
      id: null, customer_id: null, customer_contact_id: null,
      quotation_date: null, valid_until: null,
      discount_type: 1, discount_value: 0,
      items: [],
    },
    customerOptions: [], contactOptions: [], productOptions: [],
    touched: false, saving: false,
  }
}
```
- [ ] **Step 2:** Header template: V2BaseSelect KH (`customerOptions`, @change → `loadContacts(customer_id)` + reset contact), V2BaseSelect người liên hệ (`contactOptions`), V2BaseDatePicker ngày báo giá (required, `valueType="YYYY-MM-DD"`), V2BaseDatePicker hiệu lực đến. Validate inline Mã KH/Ngày BG bằng `:class="{ 'is-invalid': touched && !form.customer_id }"` + `<div class="invalid-feedback">`.
- [ ] **Step 3:** Bảng dòng hàng động:
```html
<table class="table table-sm">
  <thead><tr>
    <th>Hàng hoá<span class="text-danger">*</span></th><th>ĐVT</th>
    <th>SL<span class="text-danger">*</span></th><th>Đơn giá<span class="text-danger">*</span></th>
    <th>VAT %</th><th class="text-right">Thành tiền</th><th></th>
  </tr></thead>
  <tbody>
    <tr v-for="(it, i) in form.items" :key="i">
      <td><V2BaseSelect v-model="it.product_id" :options="productOptions" size="sm"
            @change="onProductChange(it)" :class="{ 'is-invalid': touched && !it.product_id }" /></td>
      <td><V2BaseSelect v-model="it.unit_id" :options="it.unitOptions || []" size="sm" /></td>
      <td><V2BaseInput v-model.number="it.quantity" type="number" size="sm" /></td>
      <td><V2BaseInput v-model.number="it.unit_price" type="number" size="sm" /></td>
      <td><V2BaseInput v-model.number="it.vat_rate" type="number" size="sm" /></td>
      <td class="text-right">{{ formatMoney(lineAmount(it)) }}</td>
      <td><a href="#" @click.prevent="removeItem(i)"><i class="ri-delete-bin-6-line text-danger"></i></a></td>
    </tr>
    <tr v-if="!form.items.length"><td colspan="7" class="text-center text-muted">Chưa có dòng hàng</td></tr>
  </tbody>
</table>
<V2BaseButton secondary size="sm" @click="addItem"><template #prefix><i class="ri-add-line"></i></template> Thêm dòng</V2BaseButton>
```
- [ ] **Step 4:** Footer CK + tổng (tính realtime FE, BE vẫn tính lại khi lưu):
```html
<div class="d-flex justify-content-end">
  <table class="table-sm" style="width:320px">
    <tr><td>Tạm tính</td><td class="text-right">{{ formatMoney(subtotal) }}</td></tr>
    <tr><td>Chiết khấu
      <V2BaseSelect v-model="form.discount_type" :options="[{id:1,name:'%'},{id:2,name:'Tiền'}]" size="sm" style="width:90px;display:inline-block" />
      <V2BaseInput v-model.number="form.discount_value" type="number" size="sm" style="width:120px;display:inline-block" />
    </td><td class="text-right">{{ formatMoney(discountAmount) }}</td></tr>
    <tr><td>VAT</td><td class="text-right">{{ formatMoney(vatAmount) }}</td></tr>
    <tr><td><strong>Tổng cộng</strong></td><td class="text-right"><strong>{{ formatMoney(totalAmount) }}</strong></td></tr>
  </table>
</div>
```
- [ ] **Step 5:** Computed tính tiền (mirror công thức BE — phân bổ CK theo tỉ lệ):
```javascript
computed: {
  subtotal() { return this.form.items.reduce((s, it) => s + (Number(it.quantity)||0) * (Number(it.unit_price)||0), 0) },
  discountAmount() {
    if (Number(this.form.discount_type) === 1) return Math.round(this.subtotal * (Number(this.form.discount_value)||0) / 100)
    if (Number(this.form.discount_type) === 2) return Math.min(Number(this.form.discount_value)||0, this.subtotal)
    return 0
  },
  vatAmount() {
    const sub = this.subtotal, disc = this.discountAmount
    return this.form.items.reduce((s, it) => {
      const la = (Number(it.quantity)||0) * (Number(it.unit_price)||0)
      const alloc = sub > 0 ? disc * (la / sub) : 0
      return s + (la - alloc) * (Number(it.vat_rate)||0) / 100
    }, 0)
  },
  totalAmount() { return (this.subtotal - this.discountAmount) + this.vatAmount },
}
```
- [ ] **Step 6:** Methods:
```javascript
methods: {
  lineAmount(it) { return (Number(it.quantity)||0) * (Number(it.unit_price)||0) },
  formatMoney(v) { return new Intl.NumberFormat('vi-VN').format(Math.round(v||0)) },
  addItem() { this.form.items.push({ product_id: null, unit_id: null, quantity: 1, unit_price: 0, vat_rate: 0, unitOptions: [] }) },
  removeItem(i) { this.form.items.splice(i, 1) },
  onProductChange(it) {
    const p = this.productRaw.find((x) => x.id === it.product_id)
    if (p) {
      it.vat_rate = p.vat || 0
      it.unitOptions = (p.product_units || []).map((u) => ({ id: u.unit_id, name: u.unit_name }))
      const base = (p.product_units || []).find((u) => u.is_base_unit)
      it.unit_id = base ? base.unit_id : (it.unitOptions[0] && it.unitOptions[0].id) || null
    }
  },
  async loadCustomers() { /* dispatch category/customers, map {id, name: code+' - '+name} */ },
  async loadContacts(customerId) { /* load contact theo KH → contactOptions */ },
  async loadProducts() { /* load products (kèm vat + product_units) → productOptions + productRaw */ },
  async submitForm() {
    this.touched = true
    if (!this.form.customer_id || !this.form.quotation_date || !this.form.items.length) return
    if (this.form.items.some((it) => !it.product_id || !(Number(it.quantity) > 0) || it.unit_price === '' || it.unit_price == null)) return
    this.saving = true
    try {
      const payload = { ...this.form, items: this.form.items.map((it) => ({
        product_id: it.product_id, unit_id: it.unit_id, quantity: it.quantity, unit_price: it.unit_price, vat_rate: it.vat_rate,
      })) }
      await this.$store.dispatch('sale-quotation/save', payload)
      this.$router.push('/sale/quotation')
    } finally { this.saving = false }
  },
}
```
- [ ] **Step 7:** `create.vue` render `<QuotationForm />`; `_id/edit.vue` render `<QuotationForm :quotation-id="$route.params.id" />`. Trong form, `mounted()` nếu có `quotationId` → gọi `sale-quotation/detail` fill `form` (map items, gọi loadContacts + set unitOptions từng dòng). Nếu BE trả `is_can_edit=false` → chuyển hướng về danh sách kèm cảnh báo.
- [ ] **Step 8:** Verify: tạo mới 1 báo giá 2 dòng + CK → lưu → quay lại danh sách thấy bản ghi; mở Sửa → đúng dữ liệu; tổng tiền FE khớp BE.

### Task 17: Modal Gửi duyệt + Từ chối

**Files:** Create `nhatlinh-client/components/sale/quotation/SubmitModal.vue`, `nhatlinh-client/components/sale/quotation/RejectModal.vue`

- [ ] **Step 1:** `SubmitModal.vue`: theo modal-popup skill, confirm "Gửi báo giá {{code}} đi duyệt?", emit `@confirmed` → cha gọi `sale-quotation/submit`.
- [ ] **Step 2:** `RejectModal.vue`: textarea lý do (required, validate inline `touched`), emit `@confirmed(reason)` → cha gọi `sale-quotation/reject`.
- [ ] **Step 3:** Nhúng 2 modal vào `index.vue` (và `_id/index.vue`). Sau mỗi action → reload danh sách / detail + toast.
- [ ] **Step 4:** Verify: phiếu Nháp → Gửi duyệt → trạng thái Chờ duyệt; tài khoản có quyền Duyệt → Duyệt (Đã duyệt) hoặc Từ chối (nhập lý do → Từ chối, hiện rejected_reason).

### Task 18: Xem chi tiết `_id/index.vue` + Xuất PDF

**Files:** Create `nhatlinh-client/pages/sale/quotation/_id/index.vue`

- [ ] **Step 1:** Trang xem: gọi `sale-quotation/detail`, hiển thị header + bảng dòng (read-only) + tổng tiền + badge trạng thái + (nếu Từ chối) lý do. Nút theo flag: Sửa (is_can_edit), Gửi duyệt (is_can_submit), Duyệt/Từ chối (is_can_approve), Xuất PDF.
- [ ] **Step 2:** `handleExportPdf(id)` — tải blob (pattern `handleExportList`):
```javascript
async handleExportPdf(id, code) {
  const token = localStorage.getItem('access_token')
  const res = await this.$axios.get(`/api/v1/sale/quotations/${id}/pdf`, {
    responseType: 'arraybuffer',
    headers: { Authorization: `Bearer ${token}` },
  })
  const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
  const a = document.createElement('a')
  a.href = url; a.setAttribute('download', `${code || 'bao-gia'}.pdf`)
  document.body.appendChild(a); a.click(); a.parentNode.removeChild(a)
}
```
(Xác nhận key token trong localStorage trùng với các trang export khác — grep `access_token` / `localStorage.getItem` trong trang assign export; dùng đúng key.)
- [ ] **Step 3:** Verify: mở chi tiết 1 báo giá → bấm Xuất PDF → tải file PDF hiển thị đúng KH, dòng hàng, tổng tiền.

---

## Phase 7: Kiểm thử end-to-end (manual)

### Task 19: Test E2E

- [ ] **Step 1:** Tạo báo giá: chọn KH → contact đổ đúng; thêm 2 dòng hàng (chọn SP → VAT + ĐVT tự đổ); nhập SL/đơn giá; CK tổng 10% → tổng tiền FE khớp; Lưu (Nháp). Mở lại Sửa → đủ dữ liệu.
- [ ] **Step 2:** So khớp tiền BE: `php artisan tinker` đọc bản ghi vừa tạo → `subtotal/discount_amount/vat_amount/total_amount` đúng công thức (test 1 dòng VAT 8%, 1 dòng VAT 10%, CK 10% → kiểm tra phân bổ).
- [ ] **Step 3:** Workflow: Gửi duyệt → Chờ duyệt; tài khoản quyền Duyệt → Từ chối (lý do) → Từ chối; sửa lại → Gửi duyệt → Duyệt → Đã duyệt. Phiếu Đã duyệt: không có nút Sửa/Xóa.
- [ ] **Step 4:** Xóa: chỉ phiếu Nháp xóa được; phiếu Chờ duyệt/Đã duyệt/Từ chối không có nút Xóa (hoặc bị chặn 400).
- [ ] **Step 5:** Phân quyền cấp: tài khoản chỉ "Xem báo giá bán theo bộ phận" → chỉ thấy phiếu thuộc bộ phận mình + phiếu mình tạo. Tài khoản "Xem tất cả" → thấy mọi phiếu trừ Nháp của người khác.
- [ ] **Step 6:** Xuất PDF: tải PDF, kiểm tra hiển thị tiếng Việt đúng (DejaVu Sans), số tiền, tổng.
- [ ] **Step 7 (wrap up):** đánh `[x]` task xong, ghi Checkpoint vào plan.md, cập nhật STATUS.md.

---

## Checkpoint — 2026-06-25

**Trạng thái: CODE HOÀN THÀNH (BE+FE, subagent-driven, chạy trên branch `quotation` chưa commit).**

Thực thi subagent-driven (mỗi phase: implementer + review spec/chất lượng + fix):
- **Phase 1 (T1-5):** ✅ DB `sale_quotations` + `sale_quotation_items` (KHÔNG solution_version_id), trait HasStatusBadge, entity SaleQuotation/Item. Migrate OK, getNextCode → `BG-2026-00001`.
- **Phase 2 (T6-7):** ✅ Request + Service (tính tiền phân bổ CK, sync items, phân quyền cấp, workflow). Fix: "Xem tất cả" ẩn Nháp người khác; org fields chỉ set khi tạo (không ghi đè khi update).
- **Phase 3 (T8-10):** ✅ Resource list/detail + Controller (index/show/updateOrCreate/destroy/submit/approve/reject/exportPdf) + Routes + checkPermission. Fix: destroy rethrow ValidationException; detail thêm employee_create_name/created_at.
- **Phase 4 (T11-12):** ✅ 8 permission (id **1105-1112**, group "Báo giá bán", gán Super admin) + cài `barryvdh/laravel-dompdf:1.0.2` + Blade PDF. Fix: id permission tránh trùng (ban đầu nhầm 1047-1054).
- **Phase 5 (T13-15):** ✅ store/sale-quotation.js + menu + danh sách (V2BaseFilterPanel + V2BaseCompanyDepartmentFilter + filterStateMixin + auto-search + badge). Fix: bỏ double API call ở sort/reset, watcher reset trang 1, clearFilterState.
- **Phase 6 (T16-18):** ✅ QuotationForm (master-detail, tính tiền realtime, validate inline) + create/edit + SubmitModal/RejectModal + trang chi tiết + xuất PDF blob. Fix: tuân thủ modal-popup + button-convention, bỏ double toast, payload map tường minh.

**Review tổng thể (opus):** SẴN SÀNG — BE↔FE field khớp, tên quyền khớp tuyệt đối, công thức tiền nhất quán, workflow 3 lớp đồng nhất, PDF đầy đủ. 0 Critical/Important liên phase.

**Endpoint FE dùng:** KH `category/customers/getAll`; contact `category/customers/{id}` (mảng contacts); SP `category/products/getAll` (vat + product_units, ĐVT ở `pu.unit.name`); lưu `sale-quotation/save`; xóa dispatch `apiDelete`.

**Minor để sau merge:** submit/approve/reject không transaction (1 update đơn); show findOrFail (ApiController handle 404); listManagePartIds trả string array (helper chung); menu không gate quyền; getNextCode theo max(id) (spec đã chấp nhận).

**Còn lại (user — Task 19):** test UI trên trình duyệt (tạo/sửa/workflow/xóa/phân quyền cấp/PDF), so khớp tiền BE bằng tinker, rồi tự commit cả 2 repo.

**Bước tiếp theo:** user test trình duyệt + commit.

---

## Self-review (đã rà)

- **Spec coverage:** DB header+items (T1-2,4-5) ✓; trait badge (T3) ✓; mã BG (T4) ✓; validate + rethrow (T6) ✓; tính tiền + phân bổ VAT + sync items + workflow + phân quyền cấp (T7) ✓; resource status_name/color + flags (T8) ✓; controller resource + submit/approve/reject + exportPdf (T9) ✓; routes + checkPermission (T10) ✓; 8 permission Timesheet seeder (T11) ✓; dompdf + Blade PDF (T12) ✓; store (T13) ✓; menu (T14) ✓; list page filter panel + phân quyền + mixin + badge (T15) ✓; form master-detail + tính tiền realtime + validate inline (T16) ✓; modal gửi duyệt/từ chối (T17) ✓; xem chi tiết + PDF blob (T18) ✓; E2E (T19) ✓.
- **Placeholder scan:** `<idN>` permission CỐ Ý (tra id trống thực tế ở T11 step 1). Các method FE `loadCustomers/loadContacts/loadProducts` mô tả rõ nguồn API; endpoint `category/customers` + `products` cần xác nhận tên thực tế khi implement (grep store/route Category). Tên action xóa store (`apiDeleteMethod`) cần xác nhận (T13 step 2).
- **Type consistency:** field `customer_id/customer_contact_id/quotation_date/valid_until/discount_type/discount_value/items[]{product_id,unit_id,quantity,unit_price,vat_rate,line_amount}` nhất quán migration ↔ entity ↔ request ↔ service ↔ resource ↔ FE. Flag `is_can_edit/is_can_delete/is_can_submit/is_can_approve` khớp entity ↔ resource ↔ FE. Trạng thái 1..4 khớp const ↔ STATUSES ↔ FE dropdown.
- **Sai lệch convention có chủ đích:** KHÔNG có `solution_version_id` (T1) — báo giá bán độc lập, không gắn Giải pháp/Dự án/BOM.

---

## Phase 8: UX/UI revamp + bổ sung chức năng (2026-06-25)

### Task 20: Restyle form + chi tiết theo style Assign
- [x] QuotationForm.vue + _id/index.vue: info-table header, bảng quotation-edit-table sticky-head, totals-card. Bỏ Dự án/Giải pháp/BOM/YCBG/tiền tệ/giá nhập/tỷ suất/Model-Thương hiệu-Xuất xứ/nhóm. Giữ 100% script.
- [x] Đổi list filter KH `category/customers?per_page=10000` → `category/customers/getAll` (hết 403).

### Task 21: 8 chức năng bổ sung (theo báo giá Assign)
- [x] BE: migration thêm `warranty_time` (int) + `terms` (text) vào sale_quotations; Entity/Request/Service/DetailResource cập nhật; rule `items.*.product_id` thêm `distinct`; Detail resource trả thêm customer_address/email/contact_name/contact_phone/warranty_time/terms.
- [x] FE QuotationForm: (1) hiện Địa chỉ+Email KH, (2) SĐT người liên hệ, (3) Bảo hành (tháng), (4) editor Điều khoản báo giá (CompactReviewEditor/CKEditor) cuối form, (5) kéo-thả dòng (vuedraggable), (6) validate trùng mã hàng (inline+toast), (7) Đơn giá dùng V2BaseCurrencyInput, (8) chiết khấu % ⇄ tiền hai chiều.
- [x] FE _id/index.vue: hiển thị thêm địa chỉ/email/SĐT/bảo hành + render terms (v-html).

### Task 22: E2E test (Playwright global, Node 20)
- [x] e2e/quotation.e2e.js + run.sh + README — luồng login→tạo→tính tiền→Nháp→Gửi duyệt→Chờ duyệt. Chạy **6/6 PASS**; BE verify giá 100.000 → tổng 550.000.

## Checkpoint — 2026-06-25 (lần 2)

Vừa hoàn thành: UX revamp (Task 20) + 8 chức năng bổ sung (Task 21) + E2E test (Task 22). Tất cả verify bằng Playwright 6/6 PASS + kiểm dữ liệu BE.
Setup DB dev (đã được user duyệt): cấp 8 quyền báo giá bán cho role 3/18/21 company 1; seed dữ liệu mẫu mã `*.E2E` (1 đơn vị/nhóm hàng/hàng hoá/khách hàng); migration warranty_time+terms đã chạy.
Đang làm dở: (không)
Bước tiếp theo: user test trình duyệt đầy đủ (kéo-thả, chiết khấu 2 chiều, trùng mã, editor) + tự commit 2 repo. Tuỳ chọn: đưa Bảo hành/Điều khoản/địa chỉ KH vào file PDF (hiện PDF chưa có).
Blocked: (không)

---

## Phase 9: Modal chọn hàng hoá + cột + lọc (2026-06-25/26)

### Task 23: Modal "Chọn hàng hoá" (popup + lọc + chọn hàng loạt)
- [x] `components/sale/quotation/ProductPickerModal.vue`: lọc keyword + nhóm hàng + **hãng SX + nước SX + phân loại**; checkbox + chọn tất cả; hàng đã có → disable + badge "Đã thêm" + toast. QuotationForm: nút "Thêm hàng hoá" mở modal, cột Hàng hoá read-only, `onPickProducts` dựng dòng (bỏ Select2 per-row).

### Task 24: Cột Thông số KT + ẩn/hiện cột + tổng hợp chi phí + filter
- [x] Cột "Thông số kỹ thuật" (text rút gọn + tooltip, stripHtml) — BE DetailResource map thêm `specifications` (từ product, không đổi DB).
- [x] Nút ẩn/hiện cột (dropdown: Thông số KT / ĐVT / VAT).
- [x] Tổng hợp chi phí 5 dòng: Tổng thành tiền → Chiết khấu → Tổng thành tiền sau CK (chỉ khi có CK) → VAT → Tổng thành tiền sau VAT.

### Task 25: Tinh chỉnh UI
- [x] totals-card rộng 460px + header "TỔNG HỢP CHI PHÍ" + dòng tổng cuối nền xanh.
- [x] Modal: header icon X; 5 bộ lọc xếp đều chiều rộng; footer "Đóng + icon".

## Phase 10: In + fix phân quyền (2026-06-26)

### Task 26: Thay "Xuất PDF" → "In" (xem trước + print)
- [x] `components/sale/quotation/QuotationPrintPreview.vue` (modal xem trước + window.print A4 dọc, tham khảo Assign). Thay nút ở `_id/index.vue` + row action `index.vue` (handlePrint fetch detail). BE pdf endpoint giữ nguyên (không dùng).

### Task 27: Fix toast 403 khi vào sửa (loadContacts)
- [x] Nguyên nhân: form gọi `category/customers/{id}` (gated quyền danh mục KH) → 403. Thêm endpoint Sale `GET /v1/sale/customer-contacts/{customerId}` (chỉ auth) + `QuotationController@customerContacts`; FE loadContacts đổi sang endpoint này.

### Task 28: Fix FE route guard (vào màn dù thiếu quyền)
- [x] Nguyên nhân: `middleware/checkPermission.js` chỉ guard route có trong `allMenuItems` + có `isShow`; menu `category`/`sale` chưa đăng ký + chưa có `isShow`.
- [x] Thêm `isShow` cho `sale.js` (Báo giá → 4 quyền) + `category.js` (9 màn → quyền Quản lý/Xem); đăng ký `categoryItems`+`saleItems` vào middleware. Verify: có quyền → vào OK; thiếu quyền → redirect /pages/extras/404.

### Task 29: Seeder 50 hàng hoá thiết bị trường học
- [x] `Modules/Category/Database/Seeders/SchoolEquipmentSeeder.php` (idempotent): 50 SP (mã TBTH.xxxx) + ĐVT/nhóm/hãng SX/nước SX. Đã chạy.

### Setup dev DB (đã thực hiện, user duyệt)
- Sync + gán role 3/18/21 (company 1) các quyền "Danh mục chung" (18 quyền: hàng hoá/nhóm hàng hoá/ĐVT/hãng SX/nước SX/KH/NCC/nhóm NCC/kho) — vì DB dev chưa seed các quyền MODULE-1 dù seeder đã có. Báo giá bán: quyền 1105-1112.

## Checkpoint — 2026-06-26

Vừa hoàn thành: modal chọn hàng hoá (lọc + chọn hàng loạt), cột Thông số KT + ẩn/hiện cột, tổng hợp chi phí 5 dòng, tinh chỉnh UI, tính năng In (print preview), fix toast 403 loadContacts, **fix FE route guard** (chặn truy cập màn khi thiếu quyền), seeder 50 hàng hoá.
Tất cả verify bằng Playwright E2E 6/6 PASS + diag trực quan; route guard kiểm chứng 2 chiều (có quyền vào OK / thiếu quyền redirect 404).
Bước tiếp theo: user test trình duyệt toàn bộ + tự commit 2 repo. Tuỳ chọn: đưa bảo hành/điều khoản/địa chỉ vào file PDF (nếu vẫn cần endpoint pdf), rà các phân hệ khác có cùng lỗ hổng route-guard.
Blocked: (không)

**Lưu ý team:** quyền nhóm "Danh mục chung" + "Báo giá bán" có trong PermissionsTableSeeder nhưng CHƯA seed vào DB dev hiện tại — khi deploy phải seed + gán role qua màn phân quyền.

## Checkpoint — 2026-06-27 (bổ sung báo giá + setup DB chuẩn)

Vừa hoàn thành (đợt cải tiến báo giá, BE+FE, chưa commit):
- **Auto-fill giá** (Phase 4 của price-tier): selector "Cấp giá" đầu phiếu, đơn giá tự điền theo cấp+ĐVT, **đơn giá khoá read-only**, lưu `price_tier_id` vào phiếu.
- **Banner công ty trong bản In** (tham khảo Assign): `QuotationPrintPreview.vue` thêm `<img :src="companyHeader">` (nguồn `store.employee_company.header`) + CSS preview & print.
- **Footer màn người duyệt**: hiển thị Tổng giá Net / Tổng giá bán / Chiết khấu / Tổng sau CK; **cảnh báo khi Tổng sau CK < Tổng giá Net** (badge đỏ + confirm trước khi Duyệt). BE: `DetailSaleQuotationResource` thêm `net_price`/`net_amount`/`total_net` (eager-load `items.product.productUnits`).
- **Nút "Lưu & Gửi duyệt"** ở form tạo/sửa (`submitForm(true)` → save → submit → về detail).
- **Menu Kinh doanh xuống sidebar**: `sale.js` (thêm icon, `isShow:true` luôn hiện) + `Sidebar.vue` nạp `saleItems` khi firstUri='sale' + `default-sidebar.vue` title "KINH DOANH" + dashboard page thêm layout.
- **Danh sách báo giá**: fix tiêu đề cột (`label`→`title`); thêm 4 cột **Ngày tạo / Người tạo / Ngày duyệt / Người duyệt** (migration `approved_at`+`approved_by`; `approve()` set; entity relation+accessor; list resource + eager-load); **format datetime `d/m/Y H:i:s`**, ngày báo giá/hiệu lực `d/m/Y`.
- **Validate ngày hiệu lực phải SAU ngày báo giá** (BE rule `after:quotation_date` + FE inline `validUntilInvalid` + chặn submit).
- **SaleDemoSeeder** (`Modules/Sale/Database/Seeders`): seed KH + 2 cấp giá + recalc + 3 phiếu demo (đa trạng thái, created_by, approved_at). Idempotent.

Setup DB chuẩn `nhatlinh` (đã chạy): migrate toàn bộ feature; seed permission (597, gán hết cho role **Admin id 1**); seed 50 hàng hoá; SaleDemoSeeder.
Bug đã fix khi user test: (1) menu ẩn do `role_has_permissions.company_id=0` trong khi user-profile lọc `company_id=1` → sửa company_id=1 (user nhận đủ quyền); (2) list báo giá 500 do `PriceTierService::index` paginate 2 lần → trả query builder; (3) Vue warn `errors` trùng vee-validate → đổi `errors`→`formErrors` trong AddPriceTierModal; (4) phiếu seed không hiện do Nháp+created_by null → set created_by + đa trạng thái.

Bước tiếp theo: user reload FE test toàn bộ (Node v12 chưa build) + commit 2 repo.
Blocked: (không)

### Checkpoint — 2026-06-28 (UI danh sách)
Vừa hoàn thành: màn danh sách báo giá — **mã BG là link** (nuxt-link → `/sale/quotation/:id` xem chi tiết, hover underline). Nút **In đã có sẵn** ở cột thao tác (handlePrint → QuotationPrintPreview). Không đổi logic khác.
Bước tiếp theo: user reload test click mã + In.

### Checkpoint — 2026-06-28 (Xuất Excel danh sách)
Vừa hoàn thành: nút **Xuất Excel** màn danh sách báo giá (slot #actions, V2BaseButton secondary + ri-download-line). BE: `Modules/Sale/Exports/SaleQuotationExport.php` (FromCollection+WithHeadings+WithMapping+ShouldAutoSize, 10 cột STT/Mã/KH/Ngày BG/Tổng tiền/Trạng thái/Ngày tạo/Người tạo/Ngày duyệt/Người duyệt, tổng tiền (float)); `QuotationController::export()` dùng `getListForUser($filters)->get()` → `SaleQuotationResource::collection()->resolve()` → `Excel::download(...,'bao_gia_ban.xlsx')`; route `GET /quotations/export` ĐẶT TRƯỚC `/{id}` + checkPermission giống index. FE exportExcel(): token + buildQueryString(filters) (không page/per_page) + axios arraybuffer + blob download (revoke URL). Review opus: Spec ✅ + Quality Approved (đã fix 3 minor: float/revoke/MIME). Không N+1 (service eager-load customer + createdBy/approvedBy.info).
Bước tiếp: user test xuất theo filter.
