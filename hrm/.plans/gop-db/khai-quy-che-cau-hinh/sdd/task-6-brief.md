# Task 6 brief

## Task 6: FormRequest + Controller + Routes

**Files:**
- Create: `Modules/MasterData/Http/Requests/ScheduleRegulationVersionRequest.php`
- Create: `Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`
- Modify: `Modules/MasterData/Routes/api.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (thêm test HTTP)

**Interfaces:**
- Consumes: `RegulationConfigService` (Task 3-5).
- Produces các endpoint (prefix `/api/v1/master-data`):
  - `GET  regulation-config/congno?company_id={id}` → `RegulationConfigController@showCongno` → `responseSuccessJson('OK',200,$config)` (config từ `getCongnoConfig`).
  - `POST regulation-config/congno/versions` → `@store` → tạo version (áp-ngay nếu ngày ≤ hôm nay); trả `{version, config}`.
  - `PUT  regulation-config/congno/versions/{id}` → `@update` → sửa pending; trả `{version, config}`.
  - `DELETE regulation-config/congno/versions/{id}` → `@cancel` → huỷ pending; trả `{config}`.
- `ScheduleRegulationVersionRequest` rules: `company_id required|integer`; `effective_date required|date`; `note nullable|string|max:500`; `values` required array + 7 rule con theo bảng Global Constraints (dùng `values.limit_export_debt_employee` v.v.). `messages()` tiếng Việt ("Bắt buộc phải nhập", "Chỉ cho phép nhập số nguyên").

- [ ] **Step 1: Xác định tên quyền để gate (không đẻ quyền mới)**

Run (FE menu → route regulation-config dùng permission gì):
`cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client && grep -rn "regulation-config" --include=*.js --include=*.vue components/ layouts/ store/ middleware/ | grep -i "perm\|permission\|can\|menu"`
và tra seeder BE:
`cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && grep -rin "quy chế\|cấu hình công ty\|regulation" Modules/*/Database/Seeders/PermissionsTableSeeder.php`
Quyết định: dùng đúng tên quyền điều khiển menu/màn này. **Nếu màn chưa gắn quyền riêng**, tái dùng quyền chỉnh sửa cấu hình công ty mà `Modules/Human/.../CompanyController` đang dùng (grep `isCurrentEmployeeHasPermission` trong CompanyController). Ghi tên quyền đã chọn vào `.plans/gop-db/khai-quy-che-cau-hinh/design.md`. KHÔNG tạo quyền mới.

- [ ] **Step 2: Viết test HTTP (failing)**

```php
    /** @test */
    public function api_creates_pending_version_and_returns_config()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $user = $this->actingAsSeededUserWithPermission(); // helper: đăng nhập user có quyền (xem ghi chú)

        $payload = [
            'company_id' => $companyId,
            'effective_date' => '2099-01-01',
            'note' => 'Tăng lãi suất',
            'values' => [
                'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
                'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
                'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.6,
            ],
        ];
        $res = $this->postJson('/api/v1/master-data/regulation-config/congno/versions', $payload);
        $res->assertStatus(200);
        $res->assertJsonPath('data.config.pending.0.diff_snapshot.0.key', 'interest_rate');

        $get = $this->getJson('/api/v1/master-data/regulation-config/congno?company_id=' . $companyId);
        $get->assertStatus(200);
        $get->assertJsonCount(7, 'data.fields');
    }
```

> Ghi chú implementer: `actingAsSeededUserWithPermission()` — tạo/tìm 1 employee-user và cấp quyền đã chọn ở Step 1 (spatie `givePermissionTo`), rồi `$this->actingAs($user, 'api')` theo guard dự án. Nếu test HTTP quá phụ thuộc seeder quyền, có thể tách assertion quyền sang test riêng và test này gán quyền trực tiếp.

- [ ] **Step 3: Viết FormRequest**

```php
<?php

namespace Modules\MasterData\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ScheduleRegulationVersionRequest extends FormRequest
{
    public function authorize() { return true; } // gate ở controller bằng isCurrentEmployeeHasPermission

    public function rules()
    {
        return [
            'company_id' => 'required|integer',
            'effective_date' => 'required|date',
            'note' => 'nullable|string|max:500',
            'values' => 'required|array',
            'values.limit_export_debt_employee' => 'required|integer|min:0',
            'values.adjust_odd_balance' => 'required|integer|min:0',
            'values.overdue_date_max_customer' => 'required|integer|min:0',
            'values.overdue_date_max_agency' => 'required|integer|min:0',
            'values.overdue_date_max_service' => 'required|integer|min:0',
            'values.warning_due_date' => 'nullable|integer|min:0',
            'values.interest_rate' => 'required|numeric|min:0',
        ];
    }

    public function messages()
    {
        return [
            'required' => 'Bắt buộc phải nhập',
            'integer' => 'Chỉ cho phép nhập số nguyên',
            'numeric' => 'Chỉ cho phép nhập số',
            'min' => 'Giá trị không được nhỏ hơn :min',
            'date' => 'Ngày không hợp lệ',
        ];
    }
}
```

- [ ] **Step 4: Viết Controller**

```php
<?php

namespace Modules\MasterData\Http\Controllers\V1;

use App\Http\Controllers\Api\Traits\ResponseTrait;
use Illuminate\Routing\Controller;
use Illuminate\Http\Request;
use Modules\MasterData\Http\Requests\ScheduleRegulationVersionRequest;
use Modules\MasterData\Services\RegulationConfigService;

class RegulationConfigController extends Controller
{
    use ResponseTrait;

    // Quyền đã xác định ở Task 6 Step 1 — thay bằng tên quyền thực tế:
    const PERM_EDIT = '__REPLACE_WITH_PERMISSION_FROM_STEP_1__';

    private $service;

    public function __construct(RegulationConfigService $service)
    {
        $this->service = $service;
    }

    private function guard()
    {
        if (!$this->isCurrentEmployeeHasPermission(self::PERM_EDIT)) {
            abort(403, 'Bạn không có quyền thao tác cấu hình quy chế');
        }
    }

    public function showCongno(Request $request)
    {
        $this->guard();
        $companyId = (int) $request->query('company_id');
        $config = $this->service->getCongnoConfig($companyId);
        return $this->responseSuccessJson('OK', 200, $config);
    }

    public function store(ScheduleRegulationVersionRequest $request)
    {
        $this->guard();
        $data = $request->validated();
        $version = $this->service->createCongnoVersion(
            (int) $data['company_id'], $data['effective_date'], $data['values'],
            $data['note'] ?? null, auth()->id()
        );
        return $this->responseSuccessJson('Đã lưu phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig((int) $data['company_id']),
        ]);
    }

    public function update(ScheduleRegulationVersionRequest $request, $id)
    {
        $this->guard();
        $data = $request->validated();
        $version = $this->service->updateCongnoVersion(
            (int) $id, $data['effective_date'], $data['values'], $data['note'] ?? null
        );
        return $this->responseSuccessJson('Đã cập nhật phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig((int) $version->scope_id),
        ]);
    }

    public function cancel($id)
    {
        $this->guard();
        $version = \Modules\MasterData\Entities\RegulationScheduledVersion::findOrFail($id);
        $companyId = (int) $version->scope_id;
        $this->service->cancelCongnoVersion((int) $id);
        return $this->responseSuccessJson('Đã huỷ phiên bản', 200, [
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }
}
```

> `abort(422)` từ service (`abort_unless`) và `abort(403)` sẽ được exception handler dự án chuyển thành JSON. Nếu handler chưa chuẩn hoá 422 → wrap `updateCongnoVersion`/`cancelCongnoVersion` trong try/catch `HttpException` và trả `responseValidationErrorJson`/`responseJson`. Implementer kiểm `app/Exceptions/Handler.php` trước.

- [ ] **Step 5: Đăng ký routes**

Sửa `Modules/MasterData/Routes/api.php` — thêm trong group `/v1/master-data`:

```php
Route::group(['prefix' => '/v1/master-data'], function () {
    Route::get('regulation-config/congno', 'V1\RegulationConfigController@showCongno');
    Route::post('regulation-config/congno/versions', 'V1\RegulationConfigController@store');
    Route::put('regulation-config/congno/versions/{id}', 'V1\RegulationConfigController@update');
    Route::delete('regulation-config/congno/versions/{id}', 'V1\RegulationConfigController@cancel');
});
```

> Kiểm namespace controller mà route module dùng: grep `RouteServiceProvider` của MasterData (`$moduleNamespace`). Nếu không auto-namespace, dùng FQCN đầy đủ `Modules\MasterData\Http\Controllers\V1\RegulationConfigController@...`.

- [ ] **Step 6: Chạy test → pass**

Run: `php artisan route:list --path=master-data` (xác nhận 4 route) rồi `php artisan test --filter=RegulationCongnoVersioningTest`
Expected: route hiện đủ; test HTTP PASS.

- [ ] **Step 7: Commit**

```bash
git add Modules/MasterData/Http Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): congno regulation-config API (show/store/update/cancel)"
```

---

