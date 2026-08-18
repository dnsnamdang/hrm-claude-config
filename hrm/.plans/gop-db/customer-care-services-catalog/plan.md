# Plan — Danh mục gói bảo dưỡng (ERP → HRM, phân hệ CSKH)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị)
> hoặc superpowers:executing-plans để thực thi từng task. Đánh `[x]` khi xong từng step.

Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Spec: `docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md`

**Goal:** Port màn ERP "Quản lý gói bảo dưỡng" (`admin/sale/services`) sang HRM `/customer-care/services` — đầy đủ CRUD + Sao chép + In + Export + Đính kèm S3, không đổi schema, 2 cổng chạy song song.

**Architecture:** BE `Modules/CustomerCare` theo khuôn CostController/CostService/CostResource có sẵn; FE theo khuôn `pages/finance/accounts/` (index + add + \_id/edit + print + components/FormComponent) vì cùng dạng form trang riêng, list theo khuôn `pages/customer-care/costs/index.vue`.

**Tech stack:** Laravel 8 (PHP 7.4) · Nuxt 2 / Vue 2 / Bootstrap-Vue · maatwebsite/excel · CmcS3Helper (S3) · fillReport + bảng `report_templates` chung.

## Global constraints (áp cho MỌI task)

- Nhánh `gop_db` cả 2 repo — KHÔNG migration, KHÔNG sửa schema, KHÔNG dùng `mysql2`/`DB_DATABASE_SECOND`.
- KHÔNG commit git ở bất kỳ step nào (chỉ commit khi user yêu cầu).
- KHÔNG sửa `PermissionsTableSeeder` — quyền dùng lại 3 bản ghi ERP 101023/101024/101025 theo TÊN.
- `auth()->user()->id` = id nhân viên duy nhất (employees đã gộp — mục 0b `.plans/gop-db/design.md`).
- BE rethrow `ValidationException` (không catch chung); messages tiếng Việt như ERP.
- FE: đọc `.claude/skills/button-convention/SKILL.md` + `.claude/skills/modal-popup/SKILL.md` trước khi code; task in đọc thêm `.claude/skills/print-page/SKILL.md`. Validate inline `is-invalid` + `invalid-feedback` + flag `touched`.
- Verify FE bằng `vue-template-compiler` + babel parse (KHÔNG dùng eslint — project không có config).
- Migration/quyền: chỉ update tay DB local bằng SQL (ghi trong task), không seeder.

---

## Phase 1 — BE `Modules/CustomerCare` (hrm-api)

### Task 1.1 — Entities

**Files (tạo mới):**
- `Modules/CustomerCare/Entities/Service/Service.php`
- `Modules/CustomerCare/Entities/Service/ServiceMaintain.php`
- `Modules/CustomerCare/Entities/Service/ServiceMaintainLevel.php`
- `Modules/CustomerCare/Entities/Service/ServiceLevel.php`

**Interfaces (task sau dùng):** `Service::maintains()`, `serviceLevels()`, `companies()` (pivot `coefficient`), `products()` (pivot `group_id`), `company()`, `employeeCreate()`, `employeeUpdate()`, `serviceQuotationItems()` (query builder — không cần model riêng), `isCanDelete(): bool`, `Service::STATUS_ACTIVE = 1`, `STATUS_LOCK = 0`.

- [ ] **Step 1: Viết 4 entity.** Mẫu code (PHPDoc theo convention file mẫu project):

```php
<?php

namespace Modules\CustomerCare\Entities\Service;

use App\Models\BaseModel;
use Illuminate\Support\Facades\DB;
use Modules\CustomerCare\Entities\Level\Level;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Entities\Company;

/**
 * Gói bảo dưỡng — bảng ERP `services` trên DB gộp.
 * 2 cổng ERP/HRM chạy song song trên cùng bảng — KHÔNG đổi schema/hành vi ghi.
 */
class Service extends BaseModel
{
    protected $table = 'services';

    const STATUS_ACTIVE = 1;
    const STATUS_LOCK = 0;

    const STATUSES = [
        self::STATUS_ACTIVE => 'Hoạt động',
        self::STATUS_LOCK => 'Khóa',
    ];

    protected $fillable = [
        'name', 'code', 'status', 'note', 'sale_max_percent', 'attachments',
        'company_id', 'coefficient_cost_price_service', 'vat_percent',
        'created_by', 'updated_by',
    ];

    /** ERP luôn lưu mã in hoa. */
    public function setCodeAttribute($value)
    {
        $this->attributes['code'] = mb_strtoupper(trim((string) $value), 'UTF-8');
    }

    public function maintains()
    {
        return $this->hasMany(ServiceMaintain::class, 'service_id');
    }

    public function serviceLevels()
    {
        return $this->hasMany(ServiceLevel::class, 'service_id')->orderBy('order');
    }

    public function companies()
    {
        return $this->belongsToMany(Company::class, 'company_service_coefficients')
            ->withPivot('coefficient');
    }

    public function products()
    {
        // Bảng `products` của ERP trên DB gộp — không có model HRM, join bảng trực tiếp.
        return $this->belongsToMany(\Modules\CustomerCare\Entities\Service\ErpProduct::class,
            'service_has_products', 'service_id', 'product_id')->withPivot('group_id');
    }

    public function company()
    {
        return $this->belongsTo(Company::class, 'company_id');
    }

    public function employeeCreate()
    {
        return $this->belongsTo(Employee::class, 'created_by');
    }

    public function employeeUpdate()
    {
        return $this->belongsTo(Employee::class, 'updated_by');
    }

    /**
     * Điều kiện xóa GIỮ NGUYÊN ERP (user chốt 2026-08-04): chưa gắn hàng hoá và chưa có
     * `service_quotation_items`. ⚠️ 6 bảng `wr_*` đang dùng service_id KHÔNG kiểm — rủi ro
     * đã báo, user quyết giữ nguyên (spec mục 3.4).
     */
    public function isCanDelete(): bool
    {
        return !DB::table('service_has_products')->where('service_id', $this->id)->exists()
            && !DB::table('service_quotation_items')->where('service_id', $this->id)->exists();
    }
}
```

  - `ErpProduct`: model tối giản `protected $table = 'products'` (đặt cùng thư mục, PHPDoc ghi rõ là bảng ERP dùng chung) — chỉ để belongsToMany hoạt động.
  - `ServiceMaintain`: `$table = 'service_maintains'`, fillable `service_id, name, unit_id, quantity`, `maintainLevels()` hasMany `ServiceMaintainLevel` (`service_maintain_id`). Kế thừa `Model` thuần (bảng KHÔNG có created_by/updated_by — chỉ timestamps).
  - `ServiceMaintainLevel`: `$table = 'service_maintain_levels'`, fillable `service_maintain_id, level_id, note_maintenance_id, order`, `Model` thuần.
  - `ServiceLevel`: `$table = 'service_levels'`, fillable `service_id, level_id, quota_work, benefit_coefficient, base_price, key_word, order`, `level()` belongsTo `Modules\CustomerCare\Entities\Level\Level`, `Model` thuần.
  - ⚠️ Kiểm tra `Modules\Timesheet\Entities\Company` có accessor gì lạ không trước khi dùng; cần cột `work_price`, `header`, `name` (bảng `companies` dùng chung — đã xác nhận trong spec).

- [ ] **Step 2: Verify:** `php -l` từng file sạch; `php artisan tinker --execute="echo Modules\CustomerCare\Entities\Service\Service::query()->count();"` ra 207.

### Task 1.2 — ServiceRequest (validation)

**Files (tạo mới):** `Modules/CustomerCare/Http/Requests/Service/ServiceRequest.php`

**Interfaces:** dùng cho cả store + update (phân biệt qua `$this->route('service')`); Task 1.5 controller type-hint class này.

- [ ] **Step 1: Viết request** — mẫu theo `Http/Requests/Cost/CostRequest.php` (extends `Modules\Training\Http\Requests\BaseRequest`):

```php
protected function prepareForValidation()
{
    $data = [];
    if ($this->has('name')) {
        $data['name'] = trim((string) $this->name);
    }
    if ($this->has('code')) {
        $data['code'] = mb_strtoupper(trim((string) $this->code), 'UTF-8');
    }
    // Các trường phần trăm/hệ số: dấu phẩy là dấu THẬP PHÂN (bài học màn costs — không strip).
    foreach (['vat_percent', 'sale_max_percent', 'coefficient_cost_price_service'] as $field) {
        if ($this->has($field)) {
            $data[$field] = str_replace(',', '.', (string) $this->get($field));
        }
    }
    if (!empty($data)) {
        $this->merge($data);
    }
}

public function rules()
{
    $service = $this->route('service');
    $ignoreId = is_object($service) ? $service->id : $service;
    $isUpdate = (bool) $ignoreId;

    return [
        'name' => ['required', 'max:255', Rule::unique('services', 'name')->ignore($ignoreId)],
        'code' => ['required', 'max:255', Rule::unique('services', 'code')->ignore($ignoreId)],
        // Sửa lỗi ERP: rule cũ `max:100` thiếu numeric nên chạy theo độ dài chuỗi (spec mục 6.1).
        'vat_percent' => ['required', 'numeric', 'min:0', 'max:100'],
        'sale_max_percent' => ['nullable', 'numeric', 'min:0', 'max:99'],
        'company_id' => ['required', 'exists:companies,id'],
        // Sửa lỗi ERP: validate cả khi store (spec mục 6.4).
        'coefficient_cost_price_service' => ['nullable', 'numeric', 'min:1', 'max:100'],
        'status' => $isUpdate ? ['required', 'in:0,1'] : ['nullable'],
        'note' => ['nullable', 'max:255'],
        'attachments' => ['nullable', 'array'],
        'attachments.*' => ['file', 'mimes:pdf'],
        'product_groups' => ['nullable', 'array'],
        'product_groups.*.product_id' => ['required', 'exists:products,id'],
        'product_groups.*.group_id' => ['required', 'exists:groups,id'],
        'maintains' => ['nullable', 'array'],
        'maintains.*.name' => ['required', 'max:255'],
        'maintains.*.unit_id' => ['required', 'numeric', 'exists:units,id'],
        'maintains.*.quantity' => ['required', 'numeric'],
        'maintains.*.levels' => ['required', 'array'],
        'maintains.*.levels.*.level_id' => ['required', 'exists:levels,id'],
        'maintains.*.levels.*.note_maintenance_ids' => ['required', 'array'],
        'maintains.*.levels.*.note_maintenance_ids.*' => ['numeric', 'exists:note_maintenances,id'],
        'maintains.0.levels.*.quota_work' => ['required', 'numeric'],
        'maintains.0.levels.*.benefit_coefficient' => ['nullable', 'numeric'],
        'maintains.0.levels.*.base_price' => ['nullable', 'numeric'],
        'maintains.0.levels.*.key_word' => ['nullable'],
    ];
}
```

  - `messages()`: port đủ messages ERP (`'Bắt buộc phải nhập'`, `'Đã tồn tại'`, `'Phải là số'`, `'Không tồn tại'`…) cho từng rule như `ServiceStoreRequest`/`ServiceUpdateRequest` ERP + messages cho rule mới thêm (`vat_percent.max` → `'Tối đa 100'`, `attachments.*.mimes` → `'Chỉ nhận file PDF'`).
  - `attributes()`: tên trường tiếng Việt (Tên gói bảo dưỡng, Mã gói bảo dưỡng, VAT, Định mức đàm phán giá, Công ty quản lý, Hệ số giá bán, Nội dung kiểm tra, ĐVT, SL, Định mức công…).
  - ⚠️ FE gửi multipart (có file) nên `maintains`/`product_groups`/`companies` gửi dạng JSON string → trong `prepareForValidation` thêm decode:

```php
foreach (['maintains', 'product_groups', 'companies'] as $field) {
    if ($this->has($field) && is_string($this->get($field))) {
        $data[$field] = json_decode($this->get($field), true) ?: [];
    }
}
```

- [ ] **Step 2: Verify:** `php -l` sạch.

### Task 1.3 — ServiceService (business logic)

**Files (tạo mới):** `Modules/CustomerCare/Services/ServiceService.php`

**Interfaces (controller Task 1.5 gọi):**
- `index(Request): Builder` — with đủ quan hệ, lọc name/code/status/created_by, sort whitelist, default `created_at desc`
- `optionsData(): array` — `['units' => …, 'levels' => …, 'note_maintenances' => …, 'companies' => …]`
- `dataForEdit(Service): array` — object + maintains (gộp levels) + groups + companies + company_work_price
- `store(Request): Service` / `update(Request, Service): Service` — throw `ValidationException` khi vướng cấp đã dùng
- `destroy(Service): string` — `'deleted'|'locked'`
- `searchProducts(Request): Collection` / `searchGroups(Request): Collection`
- `priceByLevel(Service): array` — cho tooltip + export

- [ ] **Step 1: Viết service.** Khung + các đoạn cốt lõi:

```php
public function index(Request $request)
{
    $query = Service::query()->with([
        'employeeCreate.info', 'employeeUpdate.info', 'company',
        'serviceLevels.level',
    ]);

    foreach (['name', 'code'] as $field) {
        if ($request->filled($field)) {
            $value = escapeLikeKeyword($request->get($field));
            if ($value !== '') {
                $query->where($field, 'like', '%' . $value . '%');
            }
        }
    }
    // status nhận cả '0' — kiểm has() như CostService.
    if ($request->has('status') && $request->get('status') !== '' && $request->get('status') !== null) {
        $query->where('status', (int) $request->get('status'));
    }
    if ($request->filled('created_by')) {
        $query->where('created_by', $request->get('created_by'));
    }

    $allowedSortFields = ['name', 'code', 'status', 'created_at', 'updated_at'];
    if ($request->filled('sort_by') && in_array($request->sort_by, $allowedSortFields, true)) {
        return $query->orderBy($request->sort_by,
            strtolower($request->get('sort_desc')) === 'true' ? 'desc' : 'asc');
    }

    return $query->orderBy('created_at', 'desc');
}

/** Giá hiển thị tooltip/export: floor(đơn giá công cty quản lý × định mức × hệ số giá bán gói). */
public function priceByLevel(Service $service): array
{
    $workPrice = $service->company->work_price ?? 0;
    $coefficient = $service->coefficient_cost_price_service ?? 1;

    return $service->serviceLevels->map(function ($sl) use ($workPrice, $coefficient) {
        return [
            'level_name' => $sl->level->name ?? ('Cấp ' . $sl->order),
            'price' => floor($workPrice * $sl->quota_work * $coefficient),
        ];
    })->all();
}
```

  - `optionsData()`: units (`DB::table('units')->select('id','name')->orderBy('name')` — bảng ERP chung), levels (`Level::query()->select('id','name')->orderBy('name')`), note_maintenances (`NoteMaintenance::query()->select('id','name','key_name')`), companies (`Company::query()->select('id','name','work_price','header')`).
  - `store(Request)` (controller bọc transaction):

```php
public function store(Request $request): Service
{
    $employeeId = auth()->user()->id;

    $service = Service::create([
        'name' => $request->name,
        'code' => $request->code,
        'sale_max_percent' => $request->sale_max_percent,
        'note' => $request->note,
        'company_id' => $request->company_id,
        'coefficient_cost_price_service' => $request->coefficient_cost_price_service ?? 1,
        'status' => Service::STATUS_ACTIVE,
        'vat_percent' => $request->vat_percent,
        'attachments' => $this->uploadAttachments($request, null),
        'created_by' => $employeeId,
        'updated_by' => $employeeId,
    ]);

    $this->saveServiceMaintain($service, $request->get('maintains') ?: []);
    $this->syncCompanies($service, $request->get('companies') ?: []);
    $this->syncProducts($service, $request->get('product_groups') ?: []);

    return $service;
}
```

  - `update()`: như store nhưng `fill` + cho `status`; `attachments` = `uploadAttachments($request, $service->attachments)` (NỐI chuỗi cũ — sửa lỗi ERP nối kiểu phần tử, spec 6.3).
  - `uploadAttachments(Request $request, ?string $existing): ?string` — dùng `App\Helper\CmcS3Helper::putFiles($request->file('attachments'), 'services')` (mẫu `Modules/Assign/Services/CustomerService.php:917`); ghép `implode(', ', $urls)`, có `$existing` thì `$existing . ', ' . $new`. Không file mới → trả `$existing` nguyên vẹn.
  - `saveServiceMaintain(Service $service, array $maintains): void` — port NGUYÊN logic ERP `Service::saveServiceMaintain()` (delete-all-recreate `service_maintains` + `service_maintain_levels`; sync `service_levels` theo `maintains[0]['levels']` bằng firstOrNew `service_id`+`level_id`, set `quota_work/benefit_coefficient/base_price/key_word(json_encode)/order`). Điểm khác duy nhất: chỗ ERP `return false` khi cấp bị loại còn `service_quotation_items.service_level_id` → **throw ValidationException**:

```php
if (ServiceQuotationItemQuery/* DB::table('service_quotation_items') */
        ->whereIn('service_level_id', $serviceLevelsQuery->pluck('id'))->exists()) {
    throw \Illuminate\Validation\ValidationException::withMessages([
        'maintains' => ['Không thể xóa cấp dịch vụ đã được sử dụng!'],
    ]);
}
```

    (`$maintains` rỗng → return sớm, không đụng dữ liệu cũ — như ERP `if ($request->maintains)`.)
  - `syncCompanies`: `[$id => ['coefficient' => $c]]`, dòng `company_id` quản lý ép coefficient 1; mảng rỗng → không sync (như ERP `if ($request->companies)`).
  - `syncProducts`: `products()->sync([product_id => ['group_id' => g]])` — LUÔN sync kể cả rỗng (ERP sync `[]` để xóa hết — giữ nguyên).
  - `destroy(Service): string` — port `delete()` + `deleteDB()` ERP:

```php
public function destroy(Service $service): string
{
    if (!$service->isCanDelete()) {
        $service->status = Service::STATUS_LOCK;
        $service->updated_by = auth()->user()->id;
        $service->save();
        return 'locked';
    }

    foreach ($service->maintains as $maintain) {
        $maintain->maintainLevels()->delete();
    }
    $service->maintains()->delete();
    $service->serviceLevels()->delete();
    // ERP không dọn pivot companies khi xóa — GIỮ NGUYÊN (spec 4.3); products rỗng sẵn (điều kiện isCanDelete).
    $service->delete();
    return 'deleted';
}
```

  - `dataForEdit(Service): array` — port `Service::getDataForEdit()` ERP: load `products` (kèm pivot group_id + tên nhóm từ bảng `groups`), `maintains.maintainLevels`, `serviceLevels`, `companies`; gộp maintainLevels theo `order` thành `levels[] = ['level_id', 'note_maintenance_ids' => [...], 'quota_work', 'benefit_coefficient', 'key_word' => json_decode, 'base_price']` (join `serviceLevels` keyBy `order`); `groups` gom products theo group; companies không pivot → toàn bộ companies coefficient=1; kèm `company_work_price`.
  - `searchProducts(Request)`: `DB::table('products')->where('status', 1)` + lọc `keyword` (name/code like) hoặc `group_id`, select `id, name, code, group_id` + join `groups` lấy `group_name`, limit 50.
  - `searchGroups(Request)`: `DB::table('groups')->where('status', 1)` + lọc name like, select `id, name`, limit 50.
  - ⚠️ Kiểm tra thực tế cột `status` của `products`/`groups` trên DB gộp trước khi code (ERP lọc `status=1` ở `groups.searchData` — xác nhận lại bằng `SHOW COLUMNS`).

- [ ] **Step 2: Verify:** `php -l` sạch.

### Task 1.4 — Transformers + Export Excel

**Files (tạo mới):**
- `Modules/CustomerCare/Transformers/ServiceResource/ServiceListResource.php`
- `Modules/CustomerCare/Transformers/ServiceResource/ServiceDetailResource.php`
- `hrm-api/app/ExcelExport/ServiceExport.php`
- `hrm-api/resources/views/exports/services.blade.php`

**Interfaces:** ListResource cho index/export; DetailResource cho show (edit + copy).

- [ ] **Step 1: `ServiceListResource`** (extends `Modules\Human\Transformers\ApiResource`, mẫu `CostResource`):

```php
return [
    'id' => $this->id,
    'name' => $this->name,
    'code' => $this->code,
    'company_name' => $this->company->name ?? '',
    'status' => $this->status,
    'status_name' => Service::STATUSES[$this->status] ?? null,
    'price_by_level' => $this->price_by_level,   // service gán trước khi resolve (mảng level_name/price)
    'created_by_name' => $this->created_by_name,
    'updated_by_name' => $this->updated_by_name,
    'created_at' => Helper::formatDateTime($this->created_at, 'd/m/Y'),
    'updated_at' => Helper::formatDateTime($this->updated_at, 'd/m/Y'),
    'is_can_delete' => true,   // nút Xóa LUÔN hiện như ERP; BE tự quyết xóa/khóa (spec 3.4)
];
```

  (`price_by_level`: controller/service map `$item->price_by_level = $this->priceByLevel($item)` sau khi paginate — tránh N+1 vì đã eager load.)
- [ ] **Step 2: `ServiceDetailResource`** — trả nguyên cấu trúc `dataForEdit`: các cột `services` + `maintains[]` (name, unit_id, quantity, levels[] như Interfaces Task 1.3) + `groups[]` (id, name, products[] {id, name, code}) + `companies[]` (id, name, work_price, coefficient) + `company_work_price` + `attachments` (tách chuỗi thành mảng URL cho FE render icon file).
- [ ] **Step 3: `ServiceExport`** — copy y nguyên khuôn `app/ExcelExport/CostExport.php` (FromView + Exportable), view `exports.services`. View 6 cột như bản ERP `sale/services/export/list.blade.php`: STT · Tên dịch vụ · Mã dịch vụ · Giá dịch vụ (implode `', '` từ `price_by_level`: `"{level_name}: {number_format(price)}"`) · Công ty quản lý dịch vụ · Trạng thái. Tiêu đề "Danh sách dịch vụ".
- [ ] **Step 4: Verify:** `php -l` 3 file PHP sạch; view blade render thử qua tinker với 1 mảng giả.

### Task 1.5 — Controller + Routes + print-data

**Files:**
- Tạo: `Modules/CustomerCare/Http/Controllers/V1/ServiceController.php`
- Sửa: `Modules/CustomerCare/Routes/api.php` (thêm group `/services` cuối file, trong group `/v1/customer-care` sẵn có)

**Interfaces (FE Phase 2-4 gọi):**

| Method | URI | Response |
|---|---|---|
| GET | `/v1/customer-care/services` | paginate ServiceListResource |
| GET | `/v1/customer-care/services/options-data` | `{units, levels, note_maintenances, companies}` |
| GET | `/v1/customer-care/services/export` | file xlsx `Danh_sach_dich_vu.xlsx` |
| GET | `/v1/customer-care/services/search-products?keyword=&group_id=` | `[{id,name,code,group_id,group_name}]` |
| GET | `/v1/customer-care/services/search-groups?keyword=` | `[{id,name}]` |
| GET | `/v1/customer-care/services/{service}` | ServiceDetailResource |
| GET | `/v1/customer-care/services/{service}/print-data` | `{template: html}` |
| POST | `/v1/customer-care/services` | created |
| POST | `/v1/customer-care/services/{service}` | updated (multipart nên dùng POST, không PUT) |
| DELETE | `/v1/customer-care/services/{service}` | `{message}` — báo rõ 'đã khóa' hay 'đã xóa' |

- [ ] **Step 1: Routes** — theo khuôn group `/costs` trong `Routes/api.php:42-60`. Route tĩnh (`options-data`, `export`, `search-products`, `search-groups`) đặt TRƯỚC `/{service}`. Middleware:
  - store: `->middleware('checkPermission:Thêm danh mục gói bảo dưỡng')`
  - update: `->middleware('checkPermission:Sửa danh mục gói bảo dưỡng')`
  - delete: `->middleware('checkPermission:Xóa danh mục gói bảo dưỡng')`
  - index/show/print-data/export/options/search: KHÔNG gate (như ERP — user chốt).
- [ ] **Step 2: Controller** — khuôn `CostController`: constructor inject `ServiceService`; `index` → `apiGetList(ServiceListResource::apiPaginate(...))` (gán `price_by_level` cho từng item trước); `show` → load `dataForEdit`; `store/update` bọc `DB::transaction`, catch `\Exception` nhưng **rethrow `ValidationException`** trước khi catch chung:

```php
} catch (\Illuminate\Validation\ValidationException $e) {
    throw $e;
} catch (Exception $e) {
    Log::error($e);
    return $this->responseBadRequest($e->getMessage());
}
```

  `delete` → message theo kết quả `'locked'|'deleted'` (khuôn CostController::delete). `export` → `Excel::download((new ServiceExport())->forData($data), 'Danh_sach_dich_vu.xlsx')` — **KHÔNG áp filter** (ERP export toàn bộ, spec 4.3): dùng `Service::query()->with(...)->get()` chứ không `index($request)`.
- [ ] **Step 3: `printData(Service $service)`** — port `Service::getPrintDataAttribute()` + `getNote()` ERP (nguồn: `D:\laragon\www\erp\app\Model\Sale\Service.php:286-402`) thành method `buildPrintData(Service): string` trong `ServiceService` — copy nguyên HTML string ERP (bảng thead 2 hàng: STT/Nội dung/SL + colspan Cấp bảo dưỡng theo levels + 2 cột Kiểm tra Có/Không + Ghi chú; mỗi maintain 1 hàng, ô cấp = implode `key_name` của note_maintenances theo level; chú giải toàn bộ note_maintenances; khối Nội dung đề xuất; bảng ký KTV/KHÁCH HÀNG). Controller theo khuôn `Modules/Finance/.../AccountController.php:237-253`:

```php
const DANH_MUC_KIEM_TRA_BAO_DUONG = 191;   // đặt trong ErpReportTemplate hoặc Service entity

$template = \Modules\Finance\Entities\ErpReportTemplate::query()->find(191);
$html = fillReport($template->template, [
    'HEADER' => $this->serviceService->companyHeader(),   // copy AccountService::companyHeader()
    'NOI_DUNG_BAO_DUONG' => $this->serviceService->buildPrintData($service),
    'TEN_DICH_VU' => mb_strtoupper($service->name, 'UTF-8'),
]);
$html = clearNull($html);
return $this->responseJson('success', Response::HTTP_OK, ['template' => $html]);
```

  - Thêm const `DANH_MUC_KIEM_TRA_BAO_DUONG = 191` vào `ErpReportTemplate` (sửa file `Modules/Finance/Entities/ErpReportTemplate.php` — chỉ THÊM const, hỏi lại nếu thấy conflict) hoặc để const trong `Service` entity nếu không muốn đụng module Finance → **chọn để trong `Service` entity**, không sửa file module khác.
  - ⚠️ Kiểm `fillReport()` + `clearNull()` có trong `app/Helper/FormatHelper.php` hrm-api (đã xác nhận `fillReport` có; `clearNull` chưa — nếu thiếu thì port hàm từ ERP helpers vào FormatHelper, hàm chỉ regex bỏ placeholder `{...}` còn sót).
- [x] ~~**Step 4: Update quyền (data, chạy tay local):** `UPDATE permissions SET type = 24
  WHERE id IN (101023, 101024, 101025);`~~ — ĐÃ LÀM rồi ĐỔI HƯỚNG (Task 5.8, 2026-08-06):
  type đã revert về NULL, quyền giờ là 3 bản ghi HRM mới 1126-1128 trong seeder.
  KHÔNG chạy SQL này khi deploy — dùng bộ SQL ở Task 5.8.
- [ ] **Step 5: Verify BE tổng thể:**
  - `php -l` toàn bộ file mới/sửa.
  - `php artisan route:list | grep customer-care/services` đủ 10 route.
  - Smoke test bằng token user thật (curl): index trả 207 bản ghi phân trang; show 1 gói có maintains/groups/companies đúng cấu trúc; store gói mới tối giản (không maintains) → xóa được (deleted); store + maintains 2 cấp → sửa bỏ 1 cấp chưa dùng OK; user KHÔNG quyền gọi store → 403; export tải được file; print-data trả HTML chứa tên gói uppercase.
  - So sánh chéo: mở màn ERP `admin/sale/services` cùng gói vừa tạo từ HRM — hiển thị/sửa bình thường (2 cổng song song OK).

---

## Phase 2 — FE màn danh sách (hrm-client)

### Task 2.1 — `pages/customer-care/services/index.vue` + menu

**Files:**
- Tạo: `hrm-client/pages/customer-care/services/index.vue`
- Sửa: `hrm-client/components/subsystem-menu/customer-care.js:27` — mục "Danh mục gói bảo dưỡng" thêm `link: '/customer-care/services'`, `isShow: true` (màn không gate quyền xem, như ERP)

**Interfaces:** dùng API index/export/delete Task 1.5. Đọc skill `button-convention` + `modal-popup` trước khi code.

- [ ] **Step 1: Dựng list** — khuôn `pages/customer-care/costs/index.vue` (575 dòng, cùng phân hệ):
  - Cột: STT · Tên gói bảo dưỡng (kèm tooltip/popover hover hiện các dòng `price_by_level`: "Cấp X: 1.234.000") · Mã · Công ty quản lý gói bảo dưỡng · Trạng thái (badge xanh Hoạt động / đỏ Khóa) · Người tạo · Ngày tạo · Người sửa · Ngày sửa · Hành động.
  - Filter: Tên, Mã, Trạng thái (select 2 giá trị), Người tạo (select nhân viên — nguồn theo cách costs/index.vue lấy dropdown nhân viên) — server-side qua query params `name/code/status/created_by`.
  - Sort server-side các cột name/code/status/created_at/updated_at (khớp whitelist BE).
  - Phân trang chuẩn V2 (áp 4 bài học phân trang Phase 8 finance-account-catalog — xem costs/index.vue đã áp sẵn).
- [ ] **Step 2: Hành động + quyền** — `$can('Thêm danh mục gói bảo dưỡng')` v.v.:
  - Đầu trang: **Thêm mới** (quyền Thêm) → `/customer-care/services/create`; **Xuất excel** (không gate) → gọi `/services/export` responseType blob, tải `Danh_sach_dich_vu.xlsx`.
  - Từng dòng: **Sao chép** (quyền Thêm) → `/customer-care/services/create?copy_from={id}` · **Sửa** (quyền Sửa) → `/customer-care/services/{id}/edit` · **In** (không gate) → `/customer-care/services/{id}/print` (mở tab mới) · **Xóa** (quyền Xóa) → modal confirm theo skill modal-popup, message giải thích "gói đang dùng sẽ chuyển sang Khóa thay vì xóa"; sau khi gọi DELETE hiện message BE trả về (đã khóa / đã xóa) rồi reload list.
- [ ] **Step 3: Verify:** build FE (`npm run dev` sẵn chạy — hard refresh); parse check bằng vue-template-compiler; browser: mở màn với user có/không quyền — nút ẩn đúng; lọc từng field + lọc `status=0`; phân trang; export tải file mở được; xóa gói đang dùng → badge chuyển Khóa; menu CSKH sáng mục "Danh mục gói bảo dưỡng".

---

## Phase 3 — FE form tạo/sửa/sao chép

### Task 3.1 — Form component + trang create/edit

**Files:**
- Tạo: `hrm-client/pages/customer-care/services/components/ServiceFormComponent.vue` (form dùng chung)
- Tạo: `hrm-client/pages/customer-care/services/create.vue`
- Tạo: `hrm-client/pages/customer-care/services/_id/edit.vue`
- Tạo: `hrm-client/pages/customer-care/services/components/ProductSearchModal.vue` + `GroupSearchModal.vue`

**Interfaces:** cấu trúc thư mục + cách create/edit bọc form chung: theo `pages/finance/accounts/` (`add.vue`, `_id/edit.vue`, `components/AccountFormComponent.vue`). Data submit multipart: các field scalar + `attachments[]` file + `maintains`/`companies`/`product_groups` JSON string (khớp decode Task 1.2).

- [ ] **Step 1: Khối 1 — Thông tin chung** (2 hàng × 4 cột): Tên\*, Mã\* (uppercase khi nhập), Định mức đàm phán giá (%), VAT (%)\*, Công ty quản lý\* (select từ options-data, mặc định = công ty user login lấy từ store; đổi → gọi `recalcPrices()`), Trạng thái (chỉ edit, select Hoạt động/Khóa), Ghi chú, Hệ số giá bán gói bảo dưỡng (mặc định 1, đổi → `recalcPrices()`). Validate inline `is-invalid`/`invalid-feedback` + `touched`.
- [ ] **Step 2: Khối 2 — Ma trận bảo dưỡng.** State:

```js
form: {
  maintains: [ { name: '', unit_id: null, quantity: null } ],   // hàng
  levels: [ { level_id: null, quota_work: null, benefit_coefficient: null,
              base_price: null, key_word: [] } ],                // cột (dùng chung mọi hàng)
  cells: {}  // cells[`${rowIdx}_${colIdx}`] = [note_maintenance_id, ...]
}
```

  - Header cột: select cấp (options levels) + nút ✕ xóa cột; nút + thêm cột. Hàng: nút thêm/xóa hàng nội dung (Tên*, ĐVT* select units, SL* số nguyên).
  - Ô ma trận: multi-select ghi chú (options note_maintenances, hiển thị `key_name`).
  - Hàng chân bảng theo cột: Định mức công* (input) · Hệ số công nghệ (input) · Giá vốn (readonly) · Giá công thức (readonly) · Giá bán cơ sở (input) · Gợi ý hàng hoá (tags — dùng `b-form-tags` Bootstrap-Vue) · Giá bán theo công ty (readonly mỗi công ty 1 hàng, công ty quản lý in đậm ×1).
  - Công thức (port nguyên ERP — `ServiceMaintainLevel.blade.php`):

```js
primeCost(level)  = companyWorkPrice * level.quota_work * (level.benefit_coefficient || 1)
recipeCost(level) = primeCost(level) * form.coefficient_cost_price_service
// đổi quota_work HOẶC benefit_coefficient -> base_price tự set = recipeCost
// giá bán theo công ty = base_price * (company.id == form.company_id ? 1 : company.coefficient)
```

  - Submit build `maintains` payload đúng cấu trúc BE (mỗi maintain: name/unit_id/quantity + `levels[]` = cột: level_id, note_maintenance_ids (từ cells), quota_work/benefit_coefficient/base_price/key_word — chỉ maintain đầu cần đủ thông số, các maintain sau copy level_id + note_ids như ERP submit_data).
- [ ] **Step 3: Khối 3 — Giá vốn theo công ty**: bảng companies từ options-data — STT · Công ty · Đơn giá công (`work_price`) · Giá vốn từng cấp (= quota_work × work_price) · Hệ số giá bán (input; dòng công ty quản lý disabled giá trị 1, đổi công ty quản lý → dòng mới disabled, dòng cũ mở lại).
- [ ] **Step 4: Khối 4 — Áp dụng cho hàng hóa**: 2 nút mở `ProductSearchModal` (search keyword → bảng kết quả id/mã/tên/nhóm, chọn từng dòng) và `GroupSearchModal` (search tên nhóm → chọn nhóm → gọi search-products?group_id → add toàn bộ). Modal theo skill modal-popup. Bảng kết quả gom theo nhóm (khuôn ERP form.blade khối 4): header nhóm + nút xóa nhóm (confirm "xóa nhóm sẽ xóa toàn bộ hàng"), từng hàng có nút xóa. Chống trùng: hàng đã có → toast warning "Hàng hóa đã được chọn".
- [ ] **Step 5: Khối 5 — Đính kèm PDF**: input file multiple accept=".pdf"; danh sách file mới thêm/xóa trước khi lưu; file cũ (edit) render icon + link mở tab mới, KHÔNG có nút xóa (nguyên trạng ERP).
- [ ] **Step 6: create.vue / edit.vue / copy**:
  - `create.vue`: bọc form, submit POST `/services`. Nếu có `?copy_from={id}` → gọi show, prefill toàn bộ (kể cả tên/mã — user tự sửa vì unique; đính kèm KHÔNG prefill), toast nhắc "Đang sao chép từ gói {name} — hãy đổi tên/mã trước khi lưu".
  - `edit.vue`: gọi show → prefill (maintains → dựng lại levels/cells theo `order`; groups; companies; attachments cũ); submit POST `/services/{id}`.
  - Lỗi validate BE dạng `maintains.0.levels.2.quota_work` → map về đúng ô/cột trên ma trận; lỗi khác hiện inline theo field; lỗi `maintains` (cấp đã dùng) hiện toast + giữ nguyên form.
- [ ] **Step 7: Verify:** parse check các file .vue; browser đủ kịch bản: tạo gói mới đủ 5 khối → so số liệu giá từng cấp với màn ERP cùng input; sửa gói thật (chọn gói CHƯA dùng ở báo giá) đổi định mức → giá tự tính lại; copy gói 207 dòng có sẵn → đổi tên/mã lưu OK; xóa cột cấp đã dùng ở `service_quotation_items` → BE chặn + toast đúng message; validate: bỏ trống Tên/Mã/VAT/ĐVT/SL/Định mức công → lỗi inline đúng ô; upload 2 PDF lưu rồi mở lại thấy link S3.

---

## Phase 4 — In phiếu

### Task 4.1 — `_id/print.vue`

**Files:**
- Tạo: `hrm-client/pages/customer-care/services/_id/print.vue`

**Interfaces:** GET `/services/{id}/print-data` → `{template: html}`. Đọc skill `print-page` TRƯỚC khi code (chống mất viền/tràn cột/không tự bật hộp thoại in).

- [ ] **Step 1:** Khuôn `pages/finance/accounts/print.vue` (cùng cơ chế template HTML từ `report_templates` ERP): fetch print-data, render `v-html` trong layout in, tự bật `window.print()` theo skill.
- [ ] **Step 2: Verify:** in thử 1 gói có ≥2 cấp + ≥5 nội dung — đối chiếu bản in ERP cùng gói (cột cấp, tick ghi chú, chú giải, khối ký); kiểm gói có ghi chú (`note`) hiện dòng "Ghi chú: …"; kiểm sang trang không mất viền theo checklist skill print-page.

---

## Verify tổng thể (sau 4 phase)

- [ ] Chạy lại đủ smoke BE (Task 1.5 Step 5) sau khi FE hoàn thiện.
- [ ] Regression 4 màn CSKH cũ (levels / note-maintenances / costs) vẫn hoạt động — cùng module, routes chung file.
- [ ] Tạo 1 gói từ HRM → mở ERP sửa → mở lại HRM thấy thay đổi (song song 2 chiều).
- [ ] Xóa gói test đã tạo (dọn data).
- [ ] Cập nhật STATUS.md + checkpoint; nhắc bộ SQL quyền cho môi trường deploy — ~~update `type=24`~~
      ĐÃ ĐỔI theo Task 5.8: INSERT 3 quyền 1126-1128 + copy grant + revert type NULL.

### Checkpoint — 2026-08-04
Vừa hoàn thành: plan chi tiết 4 phase / 8 task (sau khi spec được user duyệt)
Đang làm dở: (không)
Bước tiếp theo: user chọn cách thực thi (subagent-driven / inline) → code Task 1.1
Blocked: (không)

---

## Phase 5 — Chỉnh sửa theo yêu cầu user (sau khi code 4 phase xong)

### Task 5.1 — Bỏ cột "Hành động", chuyển nút vào cột "Tên gói bảo dưỡng" (2026-08-05)

**File sửa:** `hrm-client/pages/customer-care/services/index.vue`

- [x] Bỏ cột `actions` khỏi `tableColumns` + xóa template `#cell-actions`
- [x] Trong `#cell-name`: giữ tên (kèm tooltip giá theo cấp) + thêm `div.row-actions` bên dưới chứa 4 nút V2BaseIconButton (Sao chép · Sửa · In · Xóa) — dùng class `.row-actions` có sẵn trong `v2-styles.scss`, quyền gate giữ nguyên
- [x] Verify: parse template bằng vue-template-compiler

### Task 5.2 — Form tạo mới: hệ số giá bán + cột Giá vốn (2026-08-05)

**File sửa:** `hrm-client/pages/customer-care/services/components/ServiceFormComponent.vue`

- [x] "Hệ số giá bán gói bảo dưỡng" tạo mới để TRỐNG như ERP (`new Service({})` không prefill),
      bỏ mặc định `1` trong `emptyForm()` — công thức `recipeCost()` vẫn coi trống = 1, placeholder
      "Mặc định 1" giữ nguyên; edit/copy vẫn load giá trị từ DB (`?? 1`)
- [x] Bảng "Giá vốn theo công ty": LUÔN hiện cột "Giá vốn" như ERP (ERP render `colspan=0` kể cả
      khi chưa có cấp) — chưa có cột cấp thì hiện 1 cột "Giá vốn" rowspan 2, ô body "—"; có cấp thì
      colspan theo số cấp như cũ; ẩn hàng header phụ khi rỗng
- [x] Verify: parse template + script bằng vue-template-compiler

### Task 5.3 — Hệ số giá bán: placeholder + bỏ mặc định 1 ở bảng công ty (2026-08-05)

**File sửa:** `hrm-client/pages/customer-care/services/components/ServiceFormComponent.vue`

- [x] Placeholder "Hệ số giá bán gói bảo dưỡng": "Mặc định 1" → "Nhập hệ số"
- [x] Bảng "Giá vốn theo công ty", cột Hệ số giá bán: ~~tạo mới để TRỐNG~~ → **user chốt LẠI
      (2026-08-05, muộn hơn): mặc định 1 như ERP** (`ServiceController::create()` gán coefficient=1).
      Đã khôi phục init `coefficient: 1`; dòng công ty quản lý disabled hiển thị theo giá trị.
      Riêng ô "Hệ số giá bán gói bảo dưỡng" khối 1 VẪN để trống (chốt cũ giữ nguyên)
- [x] Ô trống quy về 1 khi TÍNH giá bán theo công ty + khi SUBMIT (pivot
      `company_service_coefficients.coefficient` NOT NULL DEFAULT 1.00 — gửi `num('')=0` sẽ làm giá ×0,
      null sẽ lỗi SQL; cùng pattern benefit_coefficient)
- [x] Verify: parse template + script bằng vue-template-compiler

### Task 5.4 — Popup chọn hàng hóa theo UX popup báo giá (2026-08-05)

User yêu cầu "dùng popup chọn hàng hóa như màn assign/quotations/create". KHÔNG tái dùng nguyên
`QuotationProductSearchModal` vì: (1) nó search qua `ErpApiService` → HTTP sang ERP CŨ (cấm trên
nhánh gop_db cho tính năng mới); (2) payload apply không có `group_id` mà form gói bảo dưỡng bắt
buộc. → Dựng lại `ProductSearchModal` của services THEO ĐÚNG UX popup báo giá (filter panel + tick
chọn nhiều + chọn cả trang + phân trang server-side + "Thêm N hàng hoá" không đóng popup), search
trên DB gộp qua API CSKH.

**Files:**
- `hrm-api/Modules/CustomerCare/Services/ServiceService.php` — mở rộng `searchProducts` (join
  brands/product_models, filter brand/manufacture/origin/group, keyword match cả model; CÓ `page`
  → paginate `{total, products}`, KHÔNG có → giữ limit 50 cho GroupSearchModal) + `productCatalogs()`
- `hrm-api/Modules/CustomerCare/Http/Controllers/V1/ServiceController.php` + `Routes/api.php` —
  action + route GET `services/product-catalogs`
- `hrm-client/pages/customer-care/services/components/ProductSearchModal.vue` — viết lại theo
  skill modal-popup mục 4 (8 điểm bắt buộc) + table-popup-layout.md
- `hrm-client/pages/customer-care/services/components/ServiceFormComponent.vue` — `@select` đơn lẻ
  → `@apply` mảng, toast tổng hợp thêm/trùng

- [x] BE: mở rộng searchProducts + productCatalogs + route
- [x] FE: viết lại ProductSearchModal (filter panel, multi-select, phân trang, footer Thêm N)
- [x] FE: ServiceFormComponent nhận apply mảng
- [x] Verify: php -l + route:list + parse 2 file Vue
- [x] **Bộ cột giống tab Hàng hoá popup báo giá** (user yêu cầu 2026-08-05): ☑ · Ảnh · Loại hàng hóa ·
      Tên hàng hoá · Model · Mã hàng · Giá niêm yết (/ĐVT cơ bản) · Bảo hành · VAT(%) · Định mức đàm
      phán giá (%) · Ghi chú · Tính chất hàng hóa. BỎ 3 cột SL tồn/KM/LR (tồn kho realtime chỉ tính
      được bên ERP, không có trên DB gộp) + cột Nguồn (services luôn là hàng ERP thật).
      BE enrich nhánh phân trang theo đúng công thức ERP `SearchController:394-412`: giá lẻ đơn vị
      cơ bản (`product_unit_prices` price_type 1) × `product_company_coefficients` theo công ty user
      (làm tròn nghìn); `sale_max_percent` từ `product_unit_prices`; map PRODUCT_TYPES/PRODUCT_CATES
      port từ `App\BaseProduct` ERP; bảo hành "X tháng/ngày/năm" như DetailQuotationResource;
      `avatar_url` tuyệt đối theo ERP_URL. Smoke tinker: dòng mẫu đủ field, legacy branch giữ 7 key.
- [x] **Cột "Hình ảnh" ở bảng "Áp dụng cho hàng hóa" ngoài form** (user yêu cầu 2026-08-05):
      thumbnail 26px + placeholder icon, group-head colspan 3→4, empty colspan 4→5.
      `avatar_url` phủ đủ 3 luồng: popup tick chọn (emit kèm) · chọn cả nhóm (nhánh legacy
      search-products giờ cũng map avatar_url) · load edit/copy (`dataForEdit` thêm field, show
      endpoint trả thẳng dataForEdit không qua resource). Helper chung `productAvatarUrl()`.
      Smoke tinker 3 luồng đều ra URL S3.
- [x] **Popup chọn nhóm hàng hóa cùng phong cách** (user yêu cầu 2026-08-05): viết lại
      GroupSearchModal — tick chọn NHIỀU nhóm + chọn cả trang + giữ lựa chọn qua trang, phân trang
      server-side 20/50/100, cột "Số hàng hóa" (selectSub cùng điều kiện lọc products), debounce
      400ms, footer "Thêm N nhóm hàng" không tự đóng, backdrop không đóng. BE `searchGroups` thêm
      chế độ `page` → `{total, groups}` (không page giữ limit 50). Form: `onSelectGroup` (1 nhóm,
      tự đóng) → `onApplyGroups` (mảng, Promise.all nạp hàng từng nhóm, toast tổng hợp
      thêm/trùng/nhóm rỗng).
      🐛 **Sửa kèm bug thật**: luồng "chọn cả nhóm" trước bị `limit 50` cắt hàng — nhóm lớn nhất
      2.288 hàng chỉ nạp 50 (ERP addProductGroup nạp đủ). Giờ `search-products?group_id=` không
      limit (chỉ limit 50 khi search tự do không page). Smoke: nhóm 2301 trả đủ 2.288.
      **Chỉnh theo user (cùng ngày)**: popup BÉ như modal ERP chooseProductGroup (680px × 84vh,
      không full màn), cột giống ERP: STT + Tên nhóm (bỏ cột Số hàng hóa; BE vẫn trả
      products_count, FE không hiển thị). Giữ tick nhiều + phân trang + footer Thêm N.
      Ẩn nhãn "Số dòng/trang:" của V2BasePagination bằng CSS scoped ở CẢ 2 popup (không sửa
      component gốc); bỏ label "Tên nhóm" ở hàng tìm kiếm popup nhóm.

### Task 5.5 — VAT không bắt buộc (2026-08-05)

User chốt VAT không bắt buộc (form ERP không đánh dấu required-label, dù rule BE ERP là
`required|max:100` — HRM theo UI/user, không theo rule ERP).

- [x] `ServiceRequest`: `vat_percent` required → nullable (giữ numeric/min/max — vẫn là fix lỗi
      thiếu numeric của ERP); bỏ message required; `prepareForValidation` bỏ qua null/'' cho 3
      trường số (ép `(string) null` = '' sẽ làm `nullable` mất tác dụng, '' vẫn chạy numeric)
- [x] `ServiceService` store/update: `vat_percent ?? 0` — cột `services.vat_percent` NOT NULL
      DEFAULT 0, gửi null sẽ lỗi SQL
- [x] FE: bỏ `<Required />` ở label VAT (%) + bỏ check bắt buộc trong `validate()`
- [x] Verify: php -l 2 file + parse ServiceFormComponent

### Task 5.6 — Sao chép mang theo file đính kèm (2026-08-05)

User báo ERP copy vẫn lấy file đính kèm. Thực tế ERP chỉ HIỂN THỊ file gói nguồn ở màn copy
(form.documents), khi lưu thì RƠI MẤT (submit_data không gửi kèm — thiếu sót ERP). HRM làm trọn:
hiển thị VÀ lưu hẳn vào gói mới (dùng chung URL S3 — an toàn vì không có luồng xóa file S3).

- [x] FE `loadService`: bỏ `isCopy ? [] :` — copy giữ `attachmentsList`; `buildFormData` (create)
      gửi `existing_attachments` = join(', ')
- [x] BE: rule `existing_attachments nullable|string`; `store()` truyền vào `uploadAttachments`
      làm chuỗi nền, file mới upload nối sau
- [x] Verify: php -l + parse Vue
- [x] Hệ số giá bán bảng công ty hiện "1.00" khi edit → ép `(float)` ở `dataForEdit` + `Number()`
      ở FE loadService (cột decimal(4,2) trả chuỗi). Smoke gói 228: trả 1
- [x] Căn phải ô nhập hệ số: rule `.v2-input__wrapper.text-right .v2-input` trong `.service-form`
      (class trên V2BaseInput rơi vào wrapper, input không kế thừa text-align) + thêm text-right
      cho ô hệ số khối 1
- [x] Toast validate theo chuẩn base dự án (khuôn `shift-detail/add.vue`): fail client-side lẫn
      BE 422 đều toast lỗi "Vui lòng kiểm tra lại dữ liệu nhập" + `scrollToInputError()`
      (`@/utils/helpers`, bắt cả `.v2-error`) cuộn tới ô lỗi đầu tiên; bỏ toast warning
      "Bạn chưa nhập đầy đủ thông tin". Lỗi nghiệp vụ `maintains` (cấp đã dùng) vẫn toast message
      riêng của BE
- [x] Nút "Sao chép" ở màn SỬA như ERP (edit.blade.php): secondary + ri-file-copy-line, đứng
      giữa Lưu và Hủy (thứ tự skill button-convention), cả header + cuối trang; chỉ hiện khi
      `isEdit && canCreate` (quyền Thêm — cùng gate với nút ở màn danh sách; hasAPermission là
      mixin GLOBAL plugins/global-mixins.js, không cần import); mở TAB MỚI
      `/create?copy_from={id}` như ERP target=_blank
- [x] Màn PREVIEW in `/services/{id}/print`: nền trắng (khuôn insurance-packages — layout mặc
      định nền xám) + viền bảng cho preview bằng scoped CSS `::v-deep` (nội dung v-html; bộ style
      trong `options.styles` CHỈ sang cửa sổ in nên preview trước đó không có viền). Trừ bảng
      `.no-border` (khối ký) như bản in
- [x] Font/style màn in khớp ERP `public/css/pdf.css` (áp CẢ preview lẫn options.styles):
      Times New Roman 16px · viền ô `1px solid black` padding 5px 8px · th giữa/đậm/middle ·
      `td > p` bỏ margin · `.block` page-break-inside avoid · lề in đổi 12mm 10mm →
      **15mm 10mm 15mm 20mm** khớp cửa sổ in ERP (print.blade.php)
### Task 5.7 — Popup chọn hàng hóa: đủ bộ lọc như popup báo giá (2026-08-05)

User yêu cầu bộ lọc "đầy đủ... giống bên báo giá". Popup báo giá có 18 trường; làm 17 (BỎ "Tồn kho"
— cần subquery stock realtime của ERP, không tái tạo trên DB gộp). Toàn bộ query trên DB gộp,
port semantics từ ERP `SearchController::searchProductStockBuyerApi:1263-1567`.

- [x] BE `searchProducts` thêm filter: product_types/product_cates (multi; cates =
      orWhereJsonContains) · brand_ids/manufacture_ids (multi) · model (model_id) ·
      scope/chapter/job_group/job_cluster (qua `product_group_classifies` → group_ids) ·
      group_id_use/product_id_use/vehicle_manufact/brand/model/life (qua `productables`
      polymorphic — type strings 'App\Model\Product\Group', 'App\Product',
      'App\Model\Common\Vehicle*')
- [x] BE `productCatalogs` mở rộng: product_types/product_cates (từ const) + scopes, chapters
      (kèm scope_id), job_groups (kèm chapter_id), job_clusters (group_id → job_group_id),
      group_classifies (1.018 dòng cho cascade FE), vehicle_manufacts/brands/models (kèm khoá cha),
      vehicle_lifes (bảng `vehicle_life` số ít, KHÔNG có status)
- [x] BE endpoint mới `GET /services/search-models?keyword=` (product_models 38.280 dòng → remote)
- [x] FE ProductSearchModal: 17 ô lọc + cascade client-side y khuôn popup báo giá (Lĩnh vực→Chương→
      Nhóm CV→Cụm CV→Nhóm hàng; Hãng xe→Loại xe→Model xe; watcher reset cấp dưới + availableGroups
      gỡ giá trị không còn hợp lệ); Model + "Dùng cho máy" dùng V2BaseSelectRemote
- [x] Verify: php -l + smoke tinker từng nhóm filter + parse Vue
- [x] Bỏ nhóm nút Lưu/Sao chép/Hủy ở HEADER form (user chốt 2026-08-05) — nút hành động chỉ đặt
      cuối trang như ERP; header giữ tiêu đề + icon

- [x] 🐛 In dính chữ "In" + khoảng trống trên header + tràn 2 tờ: do TỰ BẬT in khi tải xong —
      window.open không có user gesture bị chặn popup → plugin fallback `window.print()` in
      nguyên trang preview (kèm layout). Fix: BỎ auto-print, chờ user bấm nút In như mọi màn
      print.vue khác (printPackage gọi ĐỒNG BỘ trong click handler — không await trước
      window.open); bỏ waitImagesLoaded (ảnh đã cache từ preview). Kèm lưới an toàn `@media print`
      trên preview: ẩn .no-print + bỏ padding container nếu user tự Ctrl+P

### Task 5.8 — Chuyển 3 quyền sang seeder theo pattern màn TK ngân hàng (2026-08-06)

User chốt ĐỔI hướng quyền: thay vì dùng lại 3 quyền ERP 101023–101025 (design cũ QĐ số 2),
làm như màn `bank-account-catalog` — tạo quyền HRM MỚI guard `api` trong seeder, quyền ERP cũ
giữ nguyên `type = NULL` (ẩn khỏi màn Phân quyền HRM; role ERP cũ vẫn dùng được vì
`CheckPermission` so theo TÊN). Routes + FE check theo tên → KHÔNG sửa code.

- [x] Seeder `PermissionsTableSeeder.php`: thêm 3 quyền id 1126/1127/1128 —
      `Thêm/Sửa/Xóa danh mục gói bảo dưỡng`, guard `api`, group `Danh mục dịch vụ bảo dưỡng`, type 24
- [x] DB local `gop_db` (KHÔNG chạy seeder — `run()` truncate): INSERT tay 3 bản ghi
      + copy grant role từ quyền ERP cùng tên (101023→{18,100062,100097}, 101024→{18,100062,100097},
      101025→{18,100062}) vào `role_has_permissions`
- [x] Revert `UPDATE permissions SET type = NULL WHERE id IN (101023,101024,101025)`
      (gỡ hack type=24 cũ — tránh hiện trùng tên trong tab CSKH)
- [x] Reset cache spatie (`permission:cache-reset` báo "Unable to flush" dù driver file —
      dùng `php artisan cache:forget spatie.permission.cache` thay thế, verify key đã mất)
- [x] Verify: `php -l` seeder sạch; query DB 3 quyền mới đủ grants (1126/1127→{18,100062,100097},
      1128→{18,100062}); smoke tinker employee 461 (role 100062) `getAllPermissions()` chứa đủ
      3 tên quyền → middleware sẽ PASS; design.md QĐ số 2 đã cập nhật
- [x] Nhắc deploy (thay SQL `type=24` cũ ở "Verify tổng thể"): môi trường khác chạy tay bộ SQL —
      INSERT 3 quyền 1126-1128 + copy grant từ 101023-25 + revert type NULL (xem lệnh ở trên)

⚠️ Phát hiện kèm (2026-08-06, NGOÀI scope task này): 6 quyền CSKH seeder 1119–1124
(`Quản lý/Xem cấp dịch vụ bảo dưỡng`, `ghi chú kiểm tra`, `dịch vụ sửa chữa và chi phí khác`)
KHÔNG tồn tại trong DB local `gop_db` (query theo tên = 0 dòng) → 3 màn levels /
note-maintenances / costs đang 403 toàn bộ route có gate trên local. Chờ user xác nhận
hướng xử lý (insert tay 6 quyền + gán role tương tự?).

---

## Phase 5 — Tài liệu test case (yêu cầu user 2026-08-07)

- [x] Rà lại BE: `ServiceController`, `ServiceService` (index/optionsData/dataForEdit/store/update/destroy/priceByLevel/saveServiceMaintain/syncCompanies/syncProducts/searchProducts/searchGroups/buildPrintData), `Service` entity, `ServiceRequest`, `ServiceListResource`, `Routes/api.php`
- [x] Rà lại FE: `pages/customer-care/services/index.vue`, `create.vue`, `_id/edit.vue`, `_id/print.vue`, `components/ServiceFormComponent.vue`, `ProductSearchModal.vue`, `GroupSearchModal.vue`
- [x] Xác định phân quyền: 3 quyền `Thêm/Sửa/Xóa danh mục gói bảo dưỡng` chỉ gate 3 route ghi; xem/in/export/options KHÔNG gate; menu không gate → sinh section TC-ROLE 7 TC
- [x] Viết `generate-testcase.py` theo skill `testcase-documenter`
- [x] Sinh `testcase.xlsx` — 137 TC (7 TC-ROLE + 8 section La mã), P0 = 87 (64%)

### Checkpoint — 2026-08-07 (Phase 5)
Vừa hoàn thành: `testcase.xlsx` (137 TC) + `generate-testcase.py` cho màn Danh mục gói bảo dưỡng.
Đang làm dở: không.
Bước tiếp theo: QA review file; cần chỉnh thì sửa `generate-testcase.py` rồi chạy lại (`python .plans/gop-db/customer-care-services-catalog/generate-testcase.py`).
Blocked: không.

### Điểm cần nghiệp vụ xác nhận (ghi nhận khi viết test case, chưa sửa code)
- **Tooltip giá ở danh sách lệch với form**: `ServiceService::priceByLevel()` = floor(work_price × quota_work × coefficient_cost_price_service) — KHÔNG nhân `benefit_coefficient`, trong khi `primeCost()` ở form CÓ nhân. Gói có Hệ số công nghệ ≠ 1 sẽ thấy 2 con số khác nhau (TC_04.006, TC_08.002).
- **Bất đối xứng khi lưu**: xóa hết hàng ma trận rồi lưu thì dữ liệu cũ KHÔNG bị xóa (`saveServiceMaintain` return khi mảng rỗng), nhưng xóa hết hàng hóa rồi lưu thì pivot BỊ xóa sạch (`syncProducts` luôn sync). Hai hành vi ngược nhau, đều là nguyên trạng ERP (TC_06.017 vs TC_06.018).
- **Export Excel không áp bộ lọc** — xuất toàn bộ danh mục (TC_05.053), giữ nguyên theo ERP.
- **`isCanDelete()` không kiểm 6 bảng `wr_*`** đang dùng `service_id` — rủi ro đã báo và user chốt giữ nguyên (ghi lại để QA không coi là bug mới).
- **FE không chặn URL form theo quyền**: user thiếu quyền vẫn mở được `/create` và `/{id}/edit`, chỉ bị chặn khi Lưu (403) — TC-ROLE-07.

---

## Phase 6 — Fix bug: hệ số giá bán theo công ty bị cắt về 99.99 (2026-08-07)

**Triệu chứng:** màn `customer-care/services/{id}/edit`, nhập "Hệ số giá bán" (khối 3 — Giá vốn
theo công ty) ≥ 100 → lưu thành công nhưng mở lại thấy 99.99.

**Nguyên nhân:** `company_service_coefficients.coefficient` là `decimal(4,2)` (trần 99.99);
MySQL chạy non-strict (`config/database.php` `'strict' => false`) nên clamp âm thầm, không báo
lỗi. `ServiceRequest` cũng không có rule `max` cho `companies.*.coefficient`.

- [x] BE: migration `2026_08_07_000001_alter_coefficient_precision_company_service_coefficients.php`
      ALTER `company_service_coefficients.coefficient` `decimal(4,2)` → `decimal(10,2)`
      (giữ NOT NULL DEFAULT 1.00) — bảng dùng chung ERP, user chốt đổi schema 2026-08-07. Đã chạy local (3.3s)
- [x] BE: `ServiceRequest` thêm `max:99999999.99` cho `companies.*.coefficient` + message "Tối đa 99.999.999,99"
- [x] FE: `ServiceFormComponent.vue` thêm `companyKey(i, field)` + viền đỏ `is-invalid` và `V2BaseError`
      cho ô hệ số từng công ty (key lỗi `companies.{index}.coefficient` — payload build đúng thứ tự `companyRows`)
- [x] ~~Data-fix: 4 dòng bị cắt của gói 232 reset về 1.00~~ — **ĐÃ REVERT** (user chốt 2026-08-07:
      không sửa dữ liệu đã lưu). id 1461-1464 trả lại 99.99 đúng nguyên trạng; user tự nhập lại trên UI nếu muốn
- [x] Verify: `SHOW COLUMNS` → `decimal(10,2)`; smoke SQL ghi 150.50 đọc lại đúng 150.50 (đã revert);
      `php -l` 2 file BE sạch; SFC parse sạch (vue-template-compiler + babel)
- [ ] Chờ user test tay trên UI: nhập hệ số 100 / 150.5 → lưu → mở lại màn sửa phải đúng giá trị
- [ ] Nhắc deploy: môi trường khác phải chạy migration này (hoặc SQL
      `ALTER TABLE company_service_coefficients MODIFY coefficient DECIMAL(10,2) NOT NULL DEFAULT 1.00;`)

### Checkpoint — 2026-08-07 (Phase 6)
Vừa hoàn thành: fix bug hệ số giá bán theo công ty bị clamp về 99.99 (migration + validate BE + lỗi inline FE + data-fix).
Đang làm dở: không.
Bước tiếp theo: user test tay trên `customer-care/services/{id}/edit`.
Lưu ý: KHÔNG tự động sửa dữ liệu nghiệp vụ đã lưu — chỉ sửa schema/code, data để user tự nhập lại.
Blocked: không.

---

## Phase 7 — Ô "Hệ số giá bán" bảng Giá vốn theo công ty dùng base định dạng số (2026-08-10)

**File sửa:** `hrm-client/pages/customer-care/services/components/ServiceFormComponent.vue`

- [x] FE: đổi `V2BaseInput` + `@input.native="sanitizeNumberEvent($event, 2)"` → `V2BaseCurrencyInput`
      (`v-model="company.coefficient"`, `:precision="2"`, placeholder `1`) — cùng khuôn ô "Giá bán cơ sở"
      đã dùng ở khối 2. Có phân tách hàng nghìn khi nhập/hiển thị, tự chặn ký tự lạ + tối đa 2 số lẻ
- [x] Giữ nguyên `:disabled="isManagingCompany(company)"`, `class="text-right"` và `is-invalid`
      (style `.is-invalid .v2-currency-input` đã có sẵn ở cuối file)
- [x] Ô trống: base emit `null` — `companyPrice()` và payload submit đã xử lý `null → 1`, không cần sửa
- [x] Verify: SFC parse sạch (vue-template-compiler + babel)
- [ ] Chờ user test tay: nhập `1500.5` → hiện `1,500.5`; xoá trống → lưu vẫn về 1; dòng công ty quản lý vẫn khoá

### Checkpoint — 2026-08-10 (Phase 7)
Vừa hoàn thành: ô "Hệ số giá bán" (khối 3 — Giá vốn theo công ty) chuyển sang `V2BaseCurrencyInput` precision 2.
Đang làm dở: không.
Bước tiếp theo: user test tay trên `customer-care/services/create` và `/{id}/edit`.
Blocked: không.

---

## Phase 8 — Khóa nút Xóa cho gói đã được sử dụng (2026-08-10)

**Triệu chứng user báo:** gói vừa tạo, chưa dùng ở đâu, bấm Xóa vẫn hiện cảnh báo
"Gói đang được sử dụng sẽ chuyển sang trạng thái Khóa thay vì xóa…".

**Nguyên nhân:** `ServiceListResource` hardcode `is_can_delete => true` (Task 1.4 — chủ ý copy ERP:
nút Xóa luôn hiện, BE tự quyết xóa hay khóa) nên FE không biết gói nào dùng được; câu cảnh báo trong
`deleteConfirmMessage()` là text TĨNH, hiện cho MỌI dòng. Kiểm DB: gói 231 "Gói bảo dưỡng 0708"
có `service_has_products` = 0 và `service_quotation_items` = 0 → thực tế xóa được, cảnh báo sai.

**Quyết định (user 2026-08-10):** KHÁC ERP có chủ đích — ERP luôn cho bấm Xóa rồi âm thầm chuyển
Khóa (`Sale\ServiceController::delete()`); HRM khóa hẳn nút Xóa với gói đã dùng. Điều kiện "đã dùng"
GIỮ NGUYÊN `Service::isCanDelete()` đã chốt 2026-08-04 (đã gắn hàng hoá HOẶC đã dùng ở báo giá).

- [x] BE: `ServiceService::markCanDelete($services)` — tính cờ cho cả trang bằng 2 query gộp
      (`whereIn` trên `service_has_products` + `service_quotation_items`), tránh 2 query × N dòng
- [x] BE: `ServiceController::index()` gọi `markCanDelete()` sau vòng gán `price_by_level`
- [x] BE: `ServiceListResource` trả `is_can_delete` thật (`?? true` cho luồng export — export không dùng cờ này)
- [x] FE: `index.vue` nút Xóa `:interactable="!!item.is_can_delete"`, bọc `<span :title>` vì
      V2BaseIconButton disabled có `pointer-events: none` nên title trên nút không hiện
- [x] FE: `deleteConfirmMessage()` bỏ câu "sẽ chuyển sang trạng thái Khóa" →
      "Bạn có chắc chắn muốn xóa gói bảo dưỡng 'X'? Hành động này không thể hoàn tác."
- [x] FE: `confirmDeleteItem()` chặn sớm nếu `!is_can_delete` (phòng gọi nhầm)
- [x] BE `destroy()` GIỮ NGUYÊN nhánh chuyển Khóa — chốt chặn cuối nếu dữ liệu đổi giữa lúc load list và lúc bấm Xóa
- [x] Verify: `php -l` 3 file; smoke tinker `markCanDelete()` khớp 100% `isCanDelete()` từng dòng
      (id 1/2/3 = false, 231 = true); resource resolve ra `is_can_delete` đúng; SFC parse sạch
- [ ] Chờ user test tay: gói 231 xóa được (không còn cảnh báo sai); gói đã gắn hàng hoá/báo giá → nút Xóa mờ + tooltip

**Lưu ý nghiệp vụ:** trước đây bấm Xóa ở gói đang dùng = cách khóa nhanh gói đó. Giờ nút đã khóa,
muốn chuyển gói sang trạng thái Khóa phải vào màn Sửa → trường Trạng thái.

### Task 8.1 — Chốt lại điều kiện `is_can_delete` + wording tooltip (2026-08-10)

User hỏi vì sao gói 227 "Gói bảo dưỡng test" (K-HA) không xóa được. Tra DB: gói này **chưa phát
sinh nghiệp vụ ở đâu** — `service_quotation_items` = 0, cả 6 bảng `wr_*` = 0, hợp đồng/phụ lục/
xuất kho/hạch toán DV = 0. Chỉ vướng `service_has_products` = 2 dòng (2 hàng hoá tick ở khối 4
"Áp dụng cho hàng hóa" của chính gói đó: `CH-PRO-8125`, `AVC-CAUTRUC1TON`).

Đã đưa 3 phương án (chặn theo nghiệp vụ thật + quét đủ bảng wr_* / chỉ bỏ vế hàng hoá / giữ nguyên ERP).
→ **User chốt: GIỮ NGUYÊN như ERP** (`!products()->exists() && !serviceQuotationItems()->exists()`).
Muốn xóa gói đã gắn hàng hoá thì vào màn Sửa bỏ hết hàng hoá → Lưu → Xóa.

- [x] KHÔNG đổi `Service::isCanDelete()` / `ServiceService::destroy()` — giữ nguyên điều kiện ERP
- [x] FE: sửa wording tooltip nút Xóa bị khóa cho đúng CẢ HAI vế + chỉ luôn cách xử lý:
      "Không thể xóa: gói đã gắn hàng hoá hoặc đã được dùng ở báo giá. Vào Sửa bỏ hết hàng hoá nếu
      muốn xóa gói." (câu cũ "đã được sử dụng" gây hiểu nhầm đúng như tình huống gói 227)
- [x] Verify: SFC parse sạch

**Rủi ro vẫn còn (đã báo, user giữ nguyên):** 6 bảng `wr_*` dùng `service_id` KHÔNG nằm trong điều
kiện xóa — số dòng thực tế trên DB gộp: `wr_service_quotation_extend_product_services` 15.233 ·
`wr_import_result_services` 3.511 · `wr_assign_task_extend_product_services` 2.769 ·
`wr_service_contract_extend_product_services` 1.811 · `wr_accounting_service_items` 1.562 ·
`wr_import_result_extend_product_services` 1.348. Gói chưa gắn hàng hoá + chưa có báo giá nhưng đã
phát sinh ở các bảng này VẪN xóa được → để lại dữ liệu mồ côi.

### Checkpoint — 2026-08-10 (Phase 8)
Vừa hoàn thành: BE trả `is_can_delete` thật + FE khóa nút Xóa cho gói đã được sử dụng.
Đang làm dở: không.
Bước tiếp theo: user test tay trên `customer-care/services`.
Blocked: không.

---

## Phase 9 — File .pdf giả lọt bước chọn, lưu mới báo 422 (2026-08-10)

**Triệu chứng user báo:** chọn được file `DT_DN_0356560090-…_BBNT.pdf` ở khối "File đính kèm (PDF)"
nhưng bấm Lưu thì 422 `{"attachments.0": "Chỉ nhận file PDF"}`.

**Nguyên nhân:** file KHÔNG phải PDF — 128 byte, nội dung là JSON lỗi của cổng phát hành BBNT:
`{"type":"ERROR","code":null,"message":"system_error","errors":["Illegal base64 character 2d"]}`,
`file` nhận diện "JSON text data". Trình duyệt vẫn lưu tên `.pdf` nên:
- FE `onFilesPicked()` chỉ kiểm ĐUÔI TÊN (`/\.pdf$/i`) → lọt
- `<input accept=".pdf">` cũng chỉ lọc theo đuôi → hộp chọn file vẫn cho tick
- BE `ServiceRequest` `mimes:pdf` đọc NỘI DUNG THẬT (finfo) → chặn đúng lúc Lưu

Phụ: lỗi BE trả theo key `attachments.0` nhưng FE chỉ đọc `fieldError('attachments')` → không có
lỗi inline nào hiện, user chỉ thấy JSON 422 thô. BE hoàn toàn đúng, sửa 2 điểm ở FE.

- [x] FE `onFilesPicked()`: thêm kiểm chữ ký `%PDF-` (5 byte đầu, `FileReader.readAsArrayBuffer`
      trên `file.slice(0, 5)`) — chuyển sang `async/for…of` vì đọc file là bất đồng bộ.
      File hỏng bị chặn ngay lúc chọn
- [x] FE: computed `attachmentsErrors` gộp lỗi chọn file phía FE (`attachmentsLocalErrors`) + lỗi BE
      theo key `attachments` LẪN `attachments.{i}` → hiện inline dưới khối đính kèm thay vì im lặng
- [x] FE (user yêu cầu 2026-08-10): bỏ toast cho lỗi chọn file — tên file dài, toast trôi nhanh khó
      đọc. Cả 2 lỗi (sai đuôi / không phải PDF thật) hiện INLINE bằng `V2BaseError :messages`
      (component tự join nhiều dòng). Lỗi FE hiện ngay khi chọn; lỗi BE vẫn chờ `touched`;
      `removeNewFile()` xoá cảnh báo cũ
- [x] KHÔNG đụng BE — `mimes:pdf` đang chặn đúng
- [x] Verify: SFC parse sạch (vue-template-compiler + babel)
- [ ] Chờ user test tay: chọn lại đúng file lỗi → bị chặn ngay kèm toast; chọn PDF thật → thêm + lưu bình thường

### Checkpoint — 2026-08-10 (Phase 9)
Vừa hoàn thành: chặn file .pdf giả ngay lúc chọn + hiện lỗi `attachments.{i}` inline.
Đang làm dở: không.
Bước tiếp theo: user test tay khối File đính kèm ở màn tạo/sửa gói bảo dưỡng.
Blocked: không.

---

## Phase 10 — Cho gỡ file đính kèm đã lưu ở màn Sửa (2026-08-10)

**User hỏi:** `customer-care/services/235/edit` sao không xóa được file đã thêm lúc tạo.

**Hiện trạng (không phải bug):** port đúng ERP — `sale/services/form.blade.php:419-423` render
`form.documents` (file đã lưu) chỉ có 2 thẻ `<a>` để xem, KHÔNG có nút xóa; chỉ
`addition_attachments` (file mới chọn) mới có `removeFile()`. BE `services.attachments` là chuỗi URL
nối nhau, `uploadAttachments()` chỉ append.

**User chốt 2026-08-10:** thêm nút gỡ, **chỉ gỡ khỏi gói — KHÔNG xóa object trên S3** (gói tạo bằng
Sao chép dùng CHUNG URL với gói nguồn, xóa thật sẽ làm hỏng file của gói kia).

- [x] BE `ServiceService::keptAttachments($request, $service)` — danh sách file giữ lại khi update:
      không gửi `existing_attachments` (cổng ERP/client cũ) → giữ nguyên; gửi rỗng → gỡ hết;
      `array_intersect` với chuỗi hiện có của CHÍNH gói đó → chặn client nhét URL lạ vào cột
- [x] BE `update()` dùng `uploadAttachments($request, $this->keptAttachments(...))` thay cho
      `$service->attachments`; tách helper `splitAttachments()` dùng chung với `dataForEdit()`
- [x] BE KHÔNG gọi S3 delete — cố ý (xem lý do trên)
- [x] FE: file đã lưu có nút ✕ `removeSavedFile(index)`, title "Gỡ file khỏi gói (bấm Lưu mới có
      hiệu lực)"; không confirm — cùng kiểu `removeProduct()`, chưa Lưu thì chưa mất gì
- [x] FE `buildFormData()`: màn Sửa LUÔN gửi `existing_attachments` (kể cả chuỗi rỗng = gỡ hết);
      màn Tạo vẫn chỉ gửi khi sao chép từ gói khác
- [x] Verify: `php -l` sạch; smoke reflection `keptAttachments()` 5 ca (không gửi key → giữ nguyên ·
      giữ 1 · giữ 2 · rỗng → NULL · URL lạ → NULL) đều đúng; SFC parse sạch
- [ ] Chờ user test tay trên gói 235: gỡ file → Lưu → mở lại không còn file; gỡ hết → cột
      `attachments` = NULL; link S3 cũ vẫn mở được (không xóa object)

### Checkpoint — 2026-08-10 (Phase 10)
Vừa hoàn thành: màn Sửa gỡ được file đính kèm đã lưu (chỉ gỡ khỏi gói, giữ file trên S3).
Đang làm dở: không.
Bước tiếp theo: user test tay trên `customer-care/services/235/edit`.
Blocked: không.

---

## Phase 11 — Màn Sao chép thiếu trường Trạng thái (2026-08-11)

**User báo:** `customer-care/services/create?copy_from=235` không có trường Trạng thái.

**Nguyên nhân (lỗi port):** FE gate `v-if="isEdit"` → màn sao chép (mode `create`) bị ẩn. ERP gốc
`sale/services/form.blade.php:84` gate bằng `ng-if="form.id"`, mà luồng copy của ERP gán
`$scope.form = new Service(response.data.service)` (có `id`) → ERP CÓ hiện Trạng thái ở màn sao chép,
prefill theo gói nguồn.

**User chốt 2026-08-11:** chỉ sửa FE cho giống ERP — BE giữ nguyên `store()` luôn lưu
`STATUS_ACTIVE` (ERP `ServiceController@store:134` cũng hardcode `status = 1`). Màn Thêm mới
(không có `?copy_from`) vẫn ẩn Trạng thái như ERP.

- [x] FE: thêm computed `isCopy` (mode create + có `copyFromId`)
- [x] FE: trường Trạng thái đổi gate `v-if="isEdit"` → `v-if="isEdit || isCopy"`
- [x] FE `loadService()`: bỏ ép `status: isCopy ? 1`, prefill theo trạng thái gói nguồn như ERP
- [x] FE `buildFormData()`: giữ nguyên chỉ gửi `status` khi Sửa (BE bỏ qua khi tạo)
- [x] Verify: SFC parse sạch (vue-template-compiler + babel)
- [ ] Chờ user test tay: mở `create?copy_from=235` -> có Trạng thái đúng trạng thái gói 235; màn Thêm mới thuần vẫn không có; Lưu bản sao -> gói mới ở Hoạt động

## Phase 11b — Căn phải các ô nhập số ở form gói bảo dưỡng (2026-08-11)

**User yêu cầu:** các ô nhập số căn phải hết cho dễ đọc.

Dùng lại pattern có sẵn: `class="text-right"` trên `V2BaseInput` (class rơi vào `.v2-input__wrapper`,
scss `.service-form .v2-input__wrapper.text-right .v2-input` đã có sẵn ở cuối file trỏ xuống input con).
`V2BaseCurrencyInput` (Giá bán cơ sở, Hệ số giá bán) vốn đã căn phải sẵn qua class `--currency`.

- [x] Định mức đàm phán giá (%) — `form.sale_max_percent`
- [x] VAT (%) — `form.vat_percent`
- [x] SL (bảng ma trận) — `maintain.quantity`
- [x] Định mức công — `col.quota_work`
- [x] Hệ số công nghệ — `col.benefit_coefficient`
- [x] Hệ số giá bán gói bảo dưỡng — đã có sẵn từ trước
- [x] Verify: SFC parse sạch. KHÔNG chạy prettier trên file này — bản prettier cài qua npx format
      lệch với style hiện có (đụng 82 dòng không liên quan), đã revert.
- [ ] Chờ user xem lại giao diện form tạo/sửa

### Checkpoint — 2026-08-11 (Phase 11)
Vừa hoàn thành: màn Sao chép hiện lại trường Trạng thái (prefill theo gói nguồn, đúng ERP) + căn phải toàn bộ ô nhập số ở form.
Đang làm dở: không.
Bước tiếp theo: user test tay `customer-care/services/create?copy_from=235`.
Blocked: không.

## Phase 11c — Bảng rỗng ở form chiếm nửa màn hình (2026-08-11)

**User yêu cầu:** ở `customer-care/services/create`, bảng "Danh mục kiểm tra bảo dưỡng định kỳ" và
"Áp dụng cho hàng hóa" khi chưa có dữ liệu vẫn cao chình ình → thừa khoảng trống theo CHIỀU CAO.
Muốn bảng cao đúng bằng nội dung, có data tới đâu nở tới đó.

**Nguyên nhân:** `assets/scss/default.scss:85` — style chung `.table-responsive { min-height: 50vh }`
(hợp lý cho màn danh sách). Form này có 3 bảng bọc trong `.table-responsive` nên mỗi bảng dù rỗng
vẫn chiếm tối thiểu nửa viewport.

- [x] `ServiceFormComponent.vue`: override cục bộ `.service-form .table-responsive { min-height: 0 }`
      (specificity 0,2,0 > 0,1,0 của rule chung; style block không scoped nhưng bọc trong `.service-form`)
- [x] KHÔNG sửa `assets/scss/default.scss` — file dùng chung toàn hệ thống, đụng vào là ảnh hưởng mọi màn danh sách
- [x] Verify: template + script parse sạch (vue-template-compiler + @babel/parser), SCSS compile sạch (node-sass)
- [ ] Chờ user xem lại giao diện form tạo mới

**Ghi chú lần đầu làm sai:** hiểu nhầm thành thu hẹp chiều NGANG (thêm class `matrix-table--fit`,
`width: auto`) — đã revert sạch, không còn dấu vết trong code.

## Phase 11d — File đính kèm thành trường bắt buộc (2026-08-11)

**User yêu cầu:** khối "File đính kèm (PDF)" ở form gói bảo dưỡng phải bắt buộc.

**Quy tắc chốt:** sau khi lưu, gói phải còn ít nhất 1 file — tính CẢ file mới upload (`attachments`)
lẫn file đã lưu được giữ lại / mang sang khi sao chép (`existing_attachments`).

BE (`ServiceRequest.php`):
- [x] `attachments` => `required_without:existing_attachments|array|min:1` (bỏ `nullable`)
- [x] Message `attachments.required_without` + `attachments.min` = "Bắt buộc phải đính kèm ít nhất 1 file PDF"
- [x] Verify semantics bằng `artisan tinker`: existing rỗng/không gửi -> chặn; existing có URL -> cho qua
      (Laravel coi `existing_attachments = ''` là failing-required nên vẫn bắt upload — đúng ca "gỡ hết file")

FE (`ServiceFormComponent.vue`):
- [x] Tiêu đề khối thêm `<Required />`
- [x] `validate()`: thiếu file -> `errors.attachments`, hiện inline qua computed `attachmentsErrors` sẵn có
- [x] Viền đỏ đặt trên ô "Thêm file" (`document-item--invalid`) vì khối này không có `<input>` hiển thị
- [x] `syncAttachmentError()` gọi ở `onFilesPicked` / `removeNewFile` / `removeSavedFile` — sau lần submit đầu,
      thêm file là lỗi tắt ngay, gỡ hết file là lỗi bật lại (không phải bấm Lưu mới biết)
- [x] Verify: template + script + scss sạch; PHP `php -l` sạch

**Lưu ý downstream:** gói CŨ chưa có file đính kèm sẽ không lưu được ở màn Sửa cho tới khi bổ sung file.

## Phase 11e — Ô "Chọn ghi chú" (multi-select) thiếu icon dropdown (2026-08-11)

**Nguyên nhân:** Select2 chỉ render `.select2-selection__arrow` cho chế độ chọn 1; bản `--multiple`
không có phần tử đó. `V2BaseSelect.vue` cũng chỉ style mũi tên dưới `.select2-selection--single`
(dòng ~300) nên mọi multi-select đều không có icon — ô ghi chú trong ma trận trông như ô text.

- [x] Vẽ lại mũi tên bằng `::after` trên `.select2-selection--multiple` (tam giác 5px 4px 0 4px, #888 —
      khớp mặc định select2), lật lên khi `.select2-container--open`
- [x] `padding-right: 20px !important` cho `.select2-selection__rendered` để tag/ô search không đè icon
      (specificity 4 class > `.v2-select--sm ...` 3 class nên thắng `padding: 4px 8px !important`)
- [x] Để CỤC BỘ trong `.service-form`, KHÔNG sửa `V2BaseSelect.vue` (component dùng chung — cần user duyệt)
- [x] Verify: SFC sạch, selector sinh ra đúng `.service-form .select2-selection--multiple::after`
- [ ] Hỏi user: có muốn chuyển fix này vào `V2BaseSelect` để mọi multi-select toàn hệ thống có icon không

## Phase 11f — "Gợi ý hàng hoá" nhập lúc tạo mới nhưng mở màn Sửa lại rỗng (2026-08-11)

**Trace (không đoán):**
- `service_levels.key_word` của gói mới (234/235/236) = `'[]'` — tức FE ĐÃ gửi mảng rỗng, không phải BE làm mất
- Gói cũ 220 = `[{"text":"Lọc trần"},...]`; chạy `dataForEdit(220)` trả đúng mảng object -> đường ĐỌC (BE + `normalizeKeyWord`) không lỗi
- => lỗi ở khâu NHẬP: `b-form-tags` mặc định chỉ chốt chữ đang gõ thành tag khi bấm Enter hoặc gõ dấu
  phân cách `,`. Gõ xong bấm thẳng nút Lưu -> chữ vẫn nằm trong ô nhập, `v-model` vẫn `[]` -> lưu rỗng

- [x] Thêm prop `add-on-change` cho `b-form-tags` (bootstrap-vue 2.21.2 có prop này) — blur/change cũng chốt tag,
      nên bấm Lưu ngay sau khi gõ vẫn ăn (blur chạy trước click)
- [x] Verify: DB + `dataForEdit` đã kiểm bằng tinker; SFC parse sạch
- [ ] Chờ user test: tạo mới -> gõ gợi ý -> bấm Lưu luôn (KHÔNG Enter) -> mở Sửa phải thấy tag
- [ ] Dữ liệu đã lưu rỗng trước đó (gói 234/235/236...) phải nhập lại thủ công — không tự sửa data nghiệp vụ

**Chưa đụng:** `components/modal/other-allowance-modal.vue`, `other-deduction-modal.vue`,
`other-income-modal.vue` cũng dùng `b-form-tags` không có `add-on-change` -> dính cùng bẫy (ngoài scope, cần user duyệt).

## Phase 11g — Lọc nhanh theo TÊN + MÃ ở màn danh sách (2026-08-11)

**User yêu cầu:** ô tìm kiếm nhanh ở `customer-care/services` lọc được cả tên lẫn mã
(trước đó ô này bind thẳng `filters.name` nên chỉ ra tên).

BE (`ServiceService::index()`):
- [x] Thêm nhánh `keyword`: `where(fn => name LIKE % OR code LIKE %)` bọc closure để `orWhere` không
      phá các điều kiện status/created_by; dùng `escapeLikeKeyword()` như `searchProducts`
- [x] Verify tinker: SQL ra `where (name like ? or code like ?) and status = ?`; tìm theo mã / theo tên đều trúng

FE (`pages/customer-care/services/index.vue`):
- [x] `initialStateForm` thêm `keyword`; panel bind `:quickSearchValue="filters.keyword"`,
      placeholder "Tìm theo tên hoặc mã gói bảo dưỡng..."
- [x] `handleQuickSearchChange` ghi vào `filters.keyword`; xóa trắng ô (nút ×) -> tự `handleSearch()`
      để bỏ lọc ngay, không bắt bấm thêm nút Tìm kiếm
- [x] `ignoredFields` = `['keyword', 'name', 'code']` — các ô GÕ TAY chờ Enter/nút Tìm kiếm.
      (Trước đây `code` không nằm trong danh sách -> gõ mã ở bộ lọc nâng cao bắn 1 request mỗi ký tự)
- [x] Ô "Tên gói bảo dưỡng" / "Mã" ở bộ lọc nâng cao GIỮ NGUYÊN (lọc chính xác từng trường)
- [x] Verify: SFC parse sạch, `php -l` sạch
- [ ] Chờ user test: gõ mã vào ô tìm nhanh -> Enter -> ra đúng gói

### Bổ sung — auto-search cho ô gõ tay (user hỏi 2026-08-11)

User phản hồi: ô "Tên gói bảo dưỡng"/"Mã" phải tự search như filter Trạng thái. Đổi từ "chờ Enter"
sang auto-search có debounce 400ms (khuôn `ProductSearchModal.vue` cùng feature, timer module scope).

- [x] `ignoredFields` -> `debouncedFields = ['keyword','name','code']`; watcher: ô gõ tay chờ 400ms,
      filter dropdown gọi API ngay như cũ
- [x] `handleSearch` (Enter / nút Tìm kiếm) `clearTimeout` -> tìm ngay, không chờ debounce
- [x] `handleReset` + `beforeDestroy` cũng `clearTimeout` (tránh request cũ bắn sau khi reset/rời màn)
- [x] `handleQuickSearchChange` bỏ nhánh gọi `handleSearch()` khi xóa trắng — watcher lo hết, tránh 2 request
- [x] Verify: SFC parse sạch, không còn tham chiếu `ignoredFields`

## Phase 11h — Nút In ở màn print không hiện icon (2026-08-11)

**Nguyên nhân:** `_id/print.vue` dùng `<i class="fa fa-print">` — cú pháp Font Awesome **4**.
Project nhúng Font Awesome **5** (`assets/fonts/fa-solid-900.*`), FA5 yêu cầu class họ `fas`/`far`/`fab`;
class `fa` trơ không set `font-family` nên glyph không render (nút chỉ còn chữ "In").

- [x] Thay `<button class="btn btn-primary">` thô bằng `V2BaseButton primary size="sm"` + icon
      `ri-printer-line` qua slot `#prefix` (skill button-convention: In = primary + ri-printer-line)
- [x] `:disabled` -> `:interactable="!loading && !!template"` (prop của V2BaseButton)
- [x] Import + đăng ký `V2BaseButton`; giữ class `no-print`
- [x] Verify: SFC parse sạch

**Ghi nhận (ngoài scope):** còn nhiều màn khác dùng cú pháp FA4 `class="fa fa-*"` (assign_business,
assign_approve_result...) — cùng lỗi tiềm ẩn, chưa đụng.

## Phase 11i — Multi-select không có icon dropdown (2026-08-11)

**User báo:** popup "Chọn hàng hóa áp dụng" ở `customer-care/services/create` — 4 ô lọc đầu
(Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất) không có mũi tên dropdown,
các ô còn lại có.

**Nguyên nhân:** 4 ô đó là select2 **multiple**. select2 chỉ render thẻ
`<span class="select2-selection__arrow">` ở chế độ **single**; multiple không có thẻ nào để style
→ rule mũi tên `V2BaseSelect.vue:300` (`.select2-selection--single .select2-selection__arrow`)
không bám vào đâu. Không phải lỗi riêng màn này — mọi multi-select toàn project đều thiếu.

**User chốt 2026-08-11:** sửa cả `V2BaseSelect` + `V2BaseSelectInModal` (component dùng chung)
để đồng bộ toàn project, không vá riêng popup.

- [x] `V2BaseSelect.vue`: `.select2-selection--multiple` thêm `position: relative` + `::after` vẽ
      tam giác bằng border (đúng thông số theme default: `border-width: 5px 4px 0`, màu `#888`,
      `right: 12px` để trùng vị trí mũi tên của single), `pointer-events: none` để click xuyên qua
- [x] `V2BaseSelect.vue`: `.select2-container--open` lật mũi tên lên (khớp hành vi single)
- [x] `V2BaseSelect.vue`: chừa `padding-right` cho `.select2-selection__rendered` ở multiple —
      sửa cả rule base (26px) lẫn 4 rule size xs(24) / sm(26) / md(26) / lg(28) vì chúng dùng
      shorthand `padding` đè lên rule base
- [x] `V2BaseSelectInModal.vue`: nút xóa tất cả (×) đang ghim `right: 6px` sẽ đè mũi tên →
      đẩy sang `right: 26px`, `padding-right` của rendered tăng 28px → 44px
- [x] Verify: SFC parse sạch (vue-template-compiler) + 3 khối style compile sạch (node-sass)
- [x] Rà `.none-select-arrow` (rule ẩn mũi tên ở `custom-theme.scss`): chỉ 1 nơi dùng và đã comment,
      lại là Select2 single thuần — không xung đột
- [ ] Chờ user test: popup chọn hàng hóa + các màn khác có multi-select (trong và ngoài modal)

## Phase 11j — Xuất Excel: cảnh báo "Number stored as text" ở cột Mã dịch vụ (2026-08-13)

**User báo:** mở file `Danh_sach_dich_vu.xlsx`, ô mã `01` (C7) hiện tam giác xanh
*"The number in this cell is formatted as text or preceded by an apostrophe"*.

**Nguyên nhân:** `ServiceExport` dùng `FromView` → Maatwebsite dựng file bằng **Html Reader** của
PhpSpreadsheet, mỗi ô đi qua `DefaultValueBinder`:
- `125` → nhìn như số → ghi thành **number** (căn phải)
- `01` → có số 0 đứng đầu → binder giữ **text** → Excel gắn cờ *number stored as text*
→ Không mất dữ liệu, nhưng cột Mã **không đồng nhất kiểu** và Excel cảnh báo.

**Ràng buộc:** `phpoffice/phpspreadsheet` **1.25.2** — API chính thức `getIgnoredErrors()` chỉ có từ
**1.26**; Html Reader 1.25 cũng chưa hỗ trợ `data-type` trên `<td>` → không ép kiểu trong blade được.

**User chốt (2026-08-13):** ép text + tắt tam giác, **chỉ sửa BE của màn này** (không nâng vendor);
phạm vi **cả vùng dữ liệu** (Tên · Mã · Giá · Công ty · Trạng thái), cột STT giữ number.

- [x] `ServiceExport` implements `WithEvents` — `AfterSheet`: ép B4:F{last} thành `TYPE_STRING`
      + number format `@`; cột A (STT) giữ number. Vùng đã ép lưu ở `textRange()` để controller vá tiếp
- [x] File mới `app/ExcelExport/IgnoredErrorsPatcher.php` — vá `<ignoredErrors sqref=... numberStoredAsText="1"/>`
      vào `xl/worksheets/sheet1.xml`, chèn **trước `<drawing>`** (đúng thứ tự schema OOXML, sai chỗ Excel báo hỏng file);
      có guard chống vá 2 lần + fallback chèn trước `</worksheet>` nếu file không có ảnh
- [x] `ServiceController::export()` — `Excel::raw()` → ghi file tạm → patch → `response()->download()->deleteFileAfterSend(true)`
      (KHÔNG dùng `Excel::store()`: nó ghi qua disk Laravel nên đường dẫn temp tuyệt đối bị ghép vào gốc disk)
- [x] Verify trên dữ liệu thật (215 gói): **1.071/1.071 ô vùng B..F đều là text** (0 ô sai kiểu),
      mã toàn số `222` giữ nguyên dạng text · STT vẫn là number · `<ignoredErrors sqref="B4:F222">` có mặt và
      **đứng trước `<drawing>`** · XML parse lại sạch · logo letterhead còn (1 drawing) · 3 dòng chữ ký còn nguyên
- [x] Verify end-to-end qua chính `ServiceController::export()`: HTTP 200, `Content-Disposition` +
      `Content-Type` xlsx đúng, file 90.732 bytes đã được vá
- [ ] Chờ user test: mở bằng Excel thật, hết tam giác xanh

**Ghi nhận (không sửa):** dòng chữ ký cuối (Ngày…/Người lập/(Ký, họ tên)) cũng nằm trong vùng ép text
và vùng `ignoredErrors` — vô hại, vì vốn đã là chữ.

**Nợ kỹ thuật:** khi dự án nâng `phpoffice/phpspreadsheet` lên >= 1.26 thì bỏ `IgnoredErrorsPatcher`
và dùng API chính thức `Cell::getIgnoredErrors()->setNumberStoredAsText(true)`.

## Phase 11k — Xuất Excel: đổi "dịch vụ" → "gói bảo dưỡng", nới cột, giá xuống dòng (2026-08-13)

**User yêu cầu:** file Excel còn dùng chữ "dịch vụ" (di sản copy từ ERP) trong khi màn danh sách đã
đổi hết sang "gói bảo dưỡng"; các cột hẹp; cột Giá gộp nhiều cấp trên 1 dòng dài.

**Chốt:** đổi tên file + tiêu đề + 4 header cột; nới rộng toàn bộ cột; mỗi mức giá theo cấp dịch vụ
xuống 1 dòng riêng trong ô. Giữ nguyên tên danh mục **"cấp dịch vụ"** (là danh mục riêng, không đổi).

- [x] `hrm-client/pages/customer-care/services/index.vue` — tên file tải về `Danh_sach_dich_vu.xlsx`
      → `Danh_sach_goi_bao_duong.xlsx` (tên thật khi lưu do FE quyết định)
- [x] `ServiceController::export()` — đổi tên file ở `response()->download()` cho khớp FE
- [x] `resources/views/exports/services.blade.php` — tiêu đề "Danh sách gói bảo dưỡng"; header
      Tên / Mã / Giá / Công ty quản lý **gói bảo dưỡng**; mỗi cấp giá 1 dòng (`<br>`)
- [x] `ServiceExport` — khai độ rộng cột (nguồn duy nhất, bỏ `width` trong blade) + wrap text
      + chiều cao dòng tự động cho vùng dữ liệu
- [x] Verify: sinh file thật qua chính luồng export, đọc lại bằng PhpSpreadsheet đối chiếu
      header / độ rộng / ô Giá có ký tự xuống dòng / wrapText / vùng ép text còn nguyên
- [ ] Chờ user test: mở bằng Excel thật

### Checkpoint — 2026-08-13
Vừa hoàn thành: Phase 11k — file xuất Excel đổi hết "dịch vụ" → "gói bảo dưỡng" (tên file + tiêu đề
+ 4 header cột), nới rộng 6 cột, cột Giá tách mỗi cấp dịch vụ 1 dòng.
Đang làm dở: không có — code xong, đã verify bằng file sinh thật.
Bước tiếp theo: user mở file bằng Excel thật để xác nhận (rộng cột vừa mắt, giá xuống dòng đúng ý).
Blocked:

## Phase 11l — Form gói bảo dưỡng dùng V2Footer chuẩn (2026-08-13)

**User yêu cầu:** màn (form Thêm/Sửa) chưa dùng `V2Footer` — đang tự dựng hàng nút cuối trang.

**Chốt:** dùng chuẩn `V2Footer` cố định đáy; nút Lưu lấy từ `menu.submit_form`
(**chấp nhận mất icon spinner**, chống bấm 2 lần vẫn còn ở đầu `save()` + loading bar toàn cục);
nút Sao chép đi qua slot `custom-actions`; nút "Hủy" đổi thành "Quay lại" của footer.

- [x] `ServiceFormComponent.vue` — thay khối `d-flex justify-content-end` bằng `<V2Footer>`
      (`:menu="footerMenu"` = `{ submit_form: true }`, `url-back="/customer-care/services"`,
      `@submitForm="save"`, slot `custom-actions` chứa nút Sao chép)
- [x] import + đăng ký component `V2Footer`, thêm computed `footerMenu`
- [x] `.service-form { padding-bottom: 90px }` — footer `position: fixed` cao 50px sẽ che khối cuối
- [x] Giữ nguyên `goBack()` (luồng sau khi lưu) và popup "Thông tin chưa lưu" ở trang vỏ
      (`unsavedChildFormMixin.beforeRouteLeave` — không phụ thuộc nút bấm)
- [x] Verify: SFC parse + template compile sạch (vue-template-compiler), script parse sạch (babel),
      8 check template + 5 check script + style; `V2Footer` có thật slot `custom-actions` và
      `menu.submit_form`; không đụng id modal (`confirm-service-form` vs `confirm` của footer)
- [ ] Chờ user test trình duyệt: 2 màn `create` + `edit`

**Ghi nhận:** cả 2 trang `create.vue` / `_id/edit.vue` dùng chung `ServiceFormComponent` nên chỉ sửa 1 file.

### Checkpoint — 2026-08-13
Vừa hoàn thành: Phase 11l — form Thêm/Sửa gói bảo dưỡng chuyển sang footer chuẩn `V2Footer`.
Đang làm dở: không có.
Bước tiếp theo: user mở `/customer-care/services/create` và màn sửa để xác nhận footer + nút Sao chép.
Blocked:

## Phase 12 — Bộ tài liệu bàn giao: Testcase + HDSD + SRS (2026-08-17)

**User yêu cầu:** xuất bộ 3 tài liệu cho màn Danh mục gói bảo dưỡng theo skill mới nhất, bố cục
bám bộ mẫu đã chốt của team (`.plans/gop-db/customer-docs/`).

### Chuẩn bị
- [x] Đọc lại toàn bộ code nguồn trên nhánh `gop_db` để tài liệu bám code thật:
      BE `ServiceController` / `ServiceService` / `ServiceRequest` / `ServiceListResource` /
      entity `Service` + `Routes/api.php` (3 quyền Thêm / Sửa / Xóa; list-detail-print-export
      KHÔNG gate; `serviceNotLocked` gắn ở route sửa + xóa);
      FE `pages/customer-care/services/*` + `components/ServiceFormComponent.vue`
- [x] Chụp 14 ảnh thật trên cổng dev `hrm-crm.eteksofts.com` (1440×900) → `gbd_shots/`
      (chỉ để local, `.gitignore` đã chặn `**/.plans/**/*_shots/`)

### Testcase
- [x] `gen_testcase.py` — dùng engine chung `tc_engine.py` (form 17 cột, 2 khối summary DNS/TP),
      thay hẳn `generate-testcase.py` cũ (form 15 cột) → đã xoá file cũ
- [x] `testcase.xlsx` — **171 TC**, P0 108 (63%), 11 TC-ROLE + 10 mục La Mã
- [x] Bộ kiểm tra thuật ngữ kỹ thuật: sạch (đổi ví dụ giá 8.400.000 → 5.600.000 để không đụng
      luật chặn mã lỗi 400/403/404/422)

### SRS
- [x] `gen_srs.py` — form MỚI 4 chương (Giới thiệu / Phân quyền / Đặc tả chi tiết / Quy tắc
      nghiệp vụ), bám bản mẫu `SRS - Danh mục khách hàng.docx`: giữ dòng "Menu:" trong Layout,
      nhãn mục con `2.x.y` và tiêu đề BR in đậm, tiêu đề trang đầu 24pt không in đậm
- [x] `SRS - Danh mục gói bảo dưỡng.docx` — FR-01…FR-11, 38 bảng, 23 ảnh (14 ảnh thật +
      1 sơ đồ tổng quan + 8 biểu đồ use case), **37 trang**, mục lục đã được Word cập nhật thật
- [x] Tự kiểm: không còn mục nào của form cũ (Tổng quan / Mini-Spec / Tiêu chí nghiệm thu /
      Ngoài phạm vi / Chức năng liên quan / Route (FE) / Phân hệ:)

### HDSD
- [x] `gen_hdsd.py` — bám bố cục `HDSD_Danh muc khach hang.docx`: TỔNG QUAN (thuật ngữ, cập nhật
      tài liệu, giới thiệu, quyền + phạm vi dữ liệu) → 9 PHẦN chức năng → PHẦN 10 hướng dẫn theo
      từng quyền + 9 câu hỏi thường gặp
- [x] `HDSD_Danh muc goi bao duong.docx` — **31 trang**, 13 Heading 1, 9 bảng, 15 ảnh

### Ghi nhận nghiệp vụ cần user chốt
- [ ] Xuất Excel + In phiếu + Xem danh sách/chi tiết hiện KHÔNG gắn quyền — tài liệu đã ghi rõ là
      hiện trạng giữ nguyên theo phần mềm cũ. Nếu nghiệp vụ muốn siết thì phải bổ sung quyền mới.
- [ ] Xuất Excel không áp bộ lọc màn hình (luôn ra đủ toàn bộ danh mục) — giữ nguyên như ERP.

### Checkpoint — 2026-08-17
Vừa hoàn thành: Phase 12 — đủ bộ 3 tài liệu (testcase.xlsx 171 TC, SRS 37 trang, HDSD 31 trang)
cho màn Danh mục gói bảo dưỡng, sinh bằng 3 script `gen_*.py` chạy lại được.
Đang làm dở: không có.
Bước tiếp theo: user đọc lại 3 file và chốt 2 câu hỏi nghiệp vụ ở mục "Ghi nhận nghiệp vụ cần user chốt".
Blocked:
