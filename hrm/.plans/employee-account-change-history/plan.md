# Lịch sử thay đổi tài khoản nhân viên (human/employee) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bổ sung tính năng "Lịch sử thay đổi" cho màn quản lý tài khoản nhân viên (`human/employee`), mirror pattern lịch sử của `assign/tasks`.

**Architecture:** Bảng `employee_history` độc lập (giống `task_history`). Ghi log đặt trong `EmployeeService` (bao phủ cả luồng tạo thủ công lẫn auto-tạo tài khoản từ màn hồ sơ) + trong `EmployeeController::updateStatus`. Một endpoint riêng `GET /human/employee/{id}/histories` trả về lịch sử đã resolve ID→tên. Frontend thêm modal timeline + nút trên mỗi dòng danh sách.

**Tech Stack:** Laravel (nwidart/laravel-modules) + MySQL ở `hrm-api`; Nuxt 2 / Vue 2 + BootstrapVue ở `hrm-client`.

**Spec:** `docs/superpowers/specs/2026-06-01-employee-account-change-history-design.md`

**Lưu ý về test:** Feature tham chiếu (`task_history`) trong codebase này **không có** test tự động, và module không có harness test cho loại feature này. Theo nguyên tắc "follow established patterns in existing codebases", plan dùng **bước xác minh thủ công** (artisan migrate + tinker + thao tác UI) thay cho TDD failing-test-first. Mỗi task vẫn có bước verify rõ ràng với output mong đợi.

**Lưu ý git:** Thư mục gốc `D:\laragon\www\hrm` **không** phải git repo; `hrm-api` và `hrm-client` là 2 repo riêng. Commit dùng `git -C <đường-dẫn-repo>`. Tác giả commit: @khoipv.

---

## File Structure

**hrm-api (repo: `D:/laragon/www/hrm/hrm-api`):**
- Create: `Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php` — schema bảng lịch sử
- Create: `Modules/Human/Entities/EmployeeHistory.php` — entity + quan hệ `employee()`, `user()`
- Modify: `Modules/Human/Entities/Employee.php` — thêm quan hệ `history()`
- Modify: `Modules/Human/Services/EmployeeService.php` — `logHistory()`, `buildHistorySnapshot()`, ghi log trong `createEmployee()`/`updateEmployee()`
- Modify: `Modules/Human/Http/Controllers/Api/V1/EmployeeController.php` — `histories()`, `formatHistories()`, ghi log trong `updateStatus()`
- Modify: `Modules/Human/Routes/api.php` — route `/{id}/histories`

**hrm-client (repo: `D:/laragon/www/hrm/hrm-client`):**
- Create: `pages/human/employee/components/EmployeeHistoryModal.vue` — modal timeline
- Modify: `pages/human/employee/index.vue` — nút "Lịch sử" + đăng ký modal

---

## Task 1: Bảng `employee_history` + Entity + quan hệ

**Files:**
- Create: `hrm-api/Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php`
- Create: `hrm-api/Modules/Human/Entities/EmployeeHistory.php`
- Modify: `hrm-api/Modules/Human/Entities/Employee.php` (thêm method `history()`)

- [ ] **Step 1: Tạo migration**

Tạo `hrm-api/Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php`:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateEmployeeHistoryTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('employee_history', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('employee_id')->comment('ID tài khoản nhân viên');
            $table->string('action')->comment('Loại thao tác: create, update, change_status');
            $table->text('old_value')->nullable()->comment('Giá trị cũ (JSON)');
            $table->text('new_value')->nullable()->comment('Giá trị mới (JSON)');
            $table->unsignedBigInteger('changed_by')->comment('Người thực hiện thay đổi');
            $table->timestamp('changed_at')->useCurrent()->comment('Thời điểm thay đổi');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('employee_history');
    }
}
```

- [ ] **Step 2: Tạo entity `EmployeeHistory`**

Tạo `hrm-api/Modules/Human/Entities/EmployeeHistory.php`:

```php
<?php

namespace Modules\Human\Entities;

use App\Models\BaseModel;

class EmployeeHistory extends BaseModel
{
    protected $table = 'employee_history';

    protected $fillable = [
        'employee_id',
        'action',
        'old_value',
        'new_value',
        'changed_by',
        'changed_at',
    ];

    public function employee()
    {
        return $this->belongsTo(Employee::class, 'employee_id');
    }

    public function user()
    {
        return $this->belongsTo(Employee::class, 'changed_by');
    }
}
```

- [ ] **Step 3: Thêm quan hệ `history()` vào `Employee`**

Trong `hrm-api/Modules/Human/Entities/Employee.php`, thêm ngay sau method `companies()` (khoảng dòng 322):

```php
    public function history()
    {
        return $this->hasMany(EmployeeHistory::class, 'employee_id')->orderBy('changed_at', 'asc');
    }
```

(Class `EmployeeHistory` cùng namespace `Modules\Human\Entities` nên không cần thêm `use`.)

- [ ] **Step 4: Chạy migration**

Run: `php artisan module:migrate Human`
Expected: in ra dòng `Migrated: ... create_employee_history_table` (không lỗi).

- [ ] **Step 5: Xác minh bảng tồn tại**

Run: `php artisan tinker --execute="echo Schema::hasTable('employee_history') ? 'OK' : 'MISSING';"`
Expected: in ra `OK`.

- [ ] **Step 6: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-api add Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php Modules/Human/Entities/EmployeeHistory.php Modules/Human/Entities/Employee.php
git -C D:/laragon/www/hrm/hrm-api commit -m "feat(human): them bang employee_history va entity EmployeeHistory"
```

---

## Task 2: Helper ghi log + snapshot, ghi `create` trong `EmployeeService`

**Files:**
- Modify: `hrm-api/Modules/Human/Services/EmployeeService.php`

- [ ] **Step 1: Thêm `use` cho EmployeeHistory**

Ở đầu file `EmployeeService.php`, trong khối `use`, thêm:

```php
use Modules\Human\Entities\EmployeeHistory;
```

(Kiểm tra `EmployeeInfo` đã được import; nếu chưa, các class trong service thường dùng FQN — giữ nguyên style hiện có.)

- [ ] **Step 2: Thêm 2 helper private vào cuối class `EmployeeService`**

Thêm (trước dấu `}` đóng class):

```php
    /**
     * Ghi một dòng lịch sử thay đổi tài khoản nhân viên.
     */
    private function logHistory($employeeId, $action, $oldValue, $newValue)
    {
        EmployeeHistory::create([
            'employee_id' => $employeeId,
            'action'      => $action,
            'old_value'   => $oldValue,
            'new_value'   => $newValue,
            'changed_by'  => auth()->id(),
            'changed_at'  => now(),
        ]);
    }

    /**
     * Tạo snapshot các trường được theo dõi của tài khoản nhân viên.
     * Mật khẩu KHÔNG bao giờ lưu giá trị — chỉ cờ password_changed.
     */
    private function buildHistorySnapshot(Employee $employee, bool $passwordChanged = false)
    {
        return [
            'email'                    => $employee->email,
            'status'                   => $employee->status,
            'employee_info_id'         => $employee->employee_info_id,
            'rice_setting_location_id' => $employee->rice_setting_location_id,
            'company_ids'              => $employee->companies()->pluck('companies.id')->toArray(),
            'password_changed'         => $passwordChanged,
        ];
    }
```

(`Employee` đã được dùng trong service — xác nhận có `use Modules\Human\Entities\Employee;` ở đầu file; nếu service tham chiếu qua `$this->_model` và FQN, thêm `use Modules\Human\Entities\Employee;` để type-hint hoạt động.)

- [ ] **Step 3: Ghi log `create` trong nhánh tạo mới của `createEmployee()`**

Trong `createEmployee()`, ở **nhánh `else`** (tạo mới `Employee`), sau dòng `$employee->save();` cuối cùng của nhánh (sau `$employee->companies()->sync(...)` và `$employee->save();`, khoảng dòng 191), thêm:

```php
            $this->logHistory(
                $employee->id,
                'create',
                null,
                json_encode($this->buildHistorySnapshot($employee), JSON_UNESCAPED_UNICODE)
            );
```

(KHÔNG ghi log ở nhánh `if (!empty($dataEmployee['id']))` — đó là edge-case fill bản ghi cũ, không phải tạo mới.)

- [ ] **Step 4: Xác minh ghi `create` qua thao tác thực tế**

Mở UI `human/employee/add` (hoặc tạo hồ sơ mới ở `human/employee_info/add` để kích hoạt auto-tạo tài khoản), tạo một tài khoản. Sau đó:

Run: `php artisan tinker --execute="$h = Modules\Human\Entities\EmployeeHistory::latest('id')->first(); echo $h ? ($h->action.' | emp='.$h->employee_id.' | '.$h->new_value) : 'NONE';"`
Expected: in ra dòng bắt đầu bằng `create | emp=<id> | {"email":...,"status":...,"company_ids":[...],"password_changed":false}`.

- [ ] **Step 5: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-api add Modules/Human/Services/EmployeeService.php
git -C D:/laragon/www/hrm/hrm-api commit -m "feat(human): ghi lich su create tai khoan nhan vien"
```

---

## Task 3: Ghi `update` / `change_status` trong `EmployeeService::updateEmployee()`

**Files:**
- Modify: `hrm-api/Modules/Human/Services/EmployeeService.php`

- [ ] **Step 1: Chụp snapshot cũ ở đầu `updateEmployee()`**

Trong `updateEmployee(array $dataEmployee, $employeeId)`, ngay sau `$employee = $this->_model->find($employeeId);` (dòng ~208), thêm:

```php
        $oldSnapshot = $this->buildHistorySnapshot($employee);
        $oldStatus = $employee->status;
        $passwordChanged = !empty($dataEmployee['password']) && !empty($dataEmployee['change_pass']);
```

- [ ] **Step 2: Ghi log ở cuối `updateEmployee()`**

Ngay **trước** `return $employee;` (cuối hàm, sau `$employee->companies()->sync(...)` + `$employee->save();`, khoảng dòng 239), thêm:

```php
        $newSnapshot = $this->buildHistorySnapshot($employee, $passwordChanged);

        $oldCompanies = $oldSnapshot['company_ids'];
        $newCompanies = $newSnapshot['company_ids'];
        sort($oldCompanies);
        sort($newCompanies);

        $nonStatusChanged = $passwordChanged
            || $oldSnapshot['email'] !== $newSnapshot['email']
            || $oldSnapshot['employee_info_id'] !== $newSnapshot['employee_info_id']
            || $oldSnapshot['rice_setting_location_id'] !== $newSnapshot['rice_setting_location_id']
            || $oldCompanies !== $newCompanies;

        $statusChanged = $oldStatus != $employee->status;

        if ($statusChanged && !$nonStatusChanged) {
            $this->logHistory($employee->id, 'change_status', (string) $oldStatus, (string) $employee->status);
        } elseif ($statusChanged || $nonStatusChanged) {
            $this->logHistory(
                $employee->id,
                'update',
                json_encode($oldSnapshot, JSON_UNESCAPED_UNICODE),
                json_encode($newSnapshot, JSON_UNESCAPED_UNICODE)
            );
        }
        // Nếu không có thay đổi nào: không ghi log (tránh nhiễu).
```

- [ ] **Step 3: Xác minh `update` (đổi nhiều trường)**

Trên UI `human/employee/{id}`, đổi công ty (hoặc địa điểm cơm) rồi Lưu. Sau đó:

Run: `php artisan tinker --execute="$h = Modules\Human\Entities\EmployeeHistory::latest('id')->first(); echo $h->action.' | old='.$h->old_value.' | new='.$h->new_value;"`
Expected: `update | old={...} | new={...}` với `company_ids` (hoặc `rice_setting_location_id`) khác nhau giữa old và new.

- [ ] **Step 4: Xác minh `change_status` (chỉ đổi trạng thái)**

Trên cùng tài khoản, chỉ đổi Trạng thái (Hoạt động ↔ Khóa), không đổi gì khác, rồi Lưu. Sau đó:

Run: `php artisan tinker --execute="$h = Modules\Human\Entities\EmployeeHistory::latest('id')->first(); echo $h->action.' | old='.$h->old_value.' | new='.$h->new_value;"`
Expected: `change_status | old=1 | new=0` (hoặc `0`→`1`).

- [ ] **Step 5: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-api add Modules/Human/Services/EmployeeService.php
git -C D:/laragon/www/hrm/hrm-api commit -m "feat(human): ghi lich su update va change_status tai khoan nhan vien"
```

---

## Task 4: Ghi `change_status` trong `EmployeeController::updateStatus()`

**Files:**
- Modify: `hrm-api/Modules/Human/Http/Controllers/Api/V1/EmployeeController.php`

- [ ] **Step 1: Thêm `use` cho EmployeeHistory**

Ở đầu `EmployeeController.php`, trong khối `use`, thêm:

```php
use Modules\Human\Entities\EmployeeHistory;
```

- [ ] **Step 2: Ghi log trong `updateStatus()`**

Trong `updateStatus(Request $request, $employeeId)`, sửa khối để chụp trạng thái cũ và ghi log. Thay đoạn hiện tại:

```php
            $employee = Employee::query()->find($employeeId);

            $employee->status = $request->status;
            $employee->save();
```

bằng:

```php
            $employee = Employee::query()->find($employeeId);

            $oldStatus = $employee->status;
            $employee->status = $request->status;
            $employee->save();

            if ($oldStatus != $request->status) {
                EmployeeHistory::create([
                    'employee_id' => $employee->id,
                    'action'      => 'change_status',
                    'old_value'   => (string) $oldStatus,
                    'new_value'   => (string) $request->status,
                    'changed_by'  => auth()->id(),
                    'changed_at'  => now(),
                ]);
            }
```

(Giữ nguyên phần cập nhật `EmployeeInfo` phía dưới.)

- [ ] **Step 3: Xác minh**

Gọi endpoint đổi trạng thái nhanh (nếu UI có chỗ gọi `updateStatus`) hoặc dùng tinker mô phỏng. Kiểm tra:

Run: `php artisan tinker --execute="$h = Modules\Human\Entities\EmployeeHistory::where('action','change_status')->latest('id')->first(); echo $h->old_value.'->'.$h->new_value;"`
Expected: in ra dạng `1->0` hoặc `0->1`.

- [ ] **Step 4: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-api add Modules/Human/Http/Controllers/Api/V1/EmployeeController.php
git -C D:/laragon/www/hrm/hrm-api commit -m "feat(human): ghi lich su change_status qua updateStatus"
```

---

## Task 5: Endpoint `/histories` + format resolve ID→tên + route

**Files:**
- Modify: `hrm-api/Modules/Human/Http/Controllers/Api/V1/EmployeeController.php`
- Modify: `hrm-api/Modules/Human/Routes/api.php`

- [ ] **Step 1: Thêm `use` cho các model resolve**

Ở đầu `EmployeeController.php`, thêm vào khối `use`:

```php
use Modules\Human\Entities\Company;
use Modules\Rice\Entities\Setting\RiceSettingLocation;
use Carbon\Carbon;
```

(`EmployeeInfo` và `EmployeeHistory` đã import từ các task trước. Kiểm tra `Company` đã tồn tại ở `Modules\Human\Entities\Company`.)

- [ ] **Step 2: Thêm method `histories()` + `formatHistories()` vào `EmployeeController`**

Thêm 2 method (đặt sau `show()`):

```php
    /**
     * API lấy lịch sử thay đổi của một tài khoản nhân viên.
     */
    public function histories($id)
    {
        $histories = EmployeeHistory::with('user.info')
            ->where('employee_id', $id)
            ->orderBy('changed_at', 'asc')
            ->get();

        return $this->responseJson('success', Response::HTTP_OK, $this->formatHistories($histories));
    }

    /**
     * Resolve ID→tên trong snapshot JSON (batch để tránh N+1), format ngày & người thực hiện.
     */
    private function formatHistories($histories)
    {
        $employeeInfoIds = collect();
        $companyIds = collect();
        $riceLocationIds = collect();

        foreach ($histories as $item) {
            foreach (['old_value', 'new_value'] as $field) {
                $json = is_string($item->$field) ? json_decode($item->$field, true) : null;
                if (!is_array($json)) {
                    continue;
                }
                if (!empty($json['employee_info_id'])) {
                    $employeeInfoIds->push($json['employee_info_id']);
                }
                if (!empty($json['rice_setting_location_id'])) {
                    $riceLocationIds->push($json['rice_setting_location_id']);
                }
                if (!empty($json['company_ids']) && is_array($json['company_ids'])) {
                    foreach ($json['company_ids'] as $cid) {
                        $companyIds->push($cid);
                    }
                }
            }
        }

        $employeeInfoMap = $employeeInfoIds->unique()->isNotEmpty()
            ? EmployeeInfo::whereIn('id', $employeeInfoIds->unique())->pluck('fullname', 'id')
            : collect();

        $companyMap = $companyIds->unique()->isNotEmpty()
            ? Company::whereIn('id', $companyIds->unique())->pluck('name', 'id')
            : collect();

        $riceLocationMap = $riceLocationIds->unique()->isNotEmpty()
            ? RiceSettingLocation::whereIn('id', $riceLocationIds->unique())->pluck('name', 'id')
            : collect();

        return $histories->map(function ($item) use ($employeeInfoMap, $companyMap, $riceLocationMap) {
            return [
                'id'              => $item->id,
                'action'          => $item->action,
                'old_value'       => $this->resolveSnapshot($item->old_value, $employeeInfoMap, $companyMap, $riceLocationMap),
                'new_value'       => $this->resolveSnapshot($item->new_value, $employeeInfoMap, $companyMap, $riceLocationMap),
                'changed_by_name' => optional(optional($item->user)->info)->fullname
                    ?? optional($item->user)->email
                    ?? null,
                'changed_at'      => $item->changed_at
                    ? Carbon::parse($item->changed_at)->format('d/m/Y H:i:s')
                    : ($item->created_at ? Carbon::parse($item->created_at)->format('d/m/Y H:i:s') : null),
            ];
        })->values();
    }

    /**
     * Với snapshot JSON (action create/update): resolve company_ids→tên, rice location→tên,
     * employee_info_id→tên; giữ nguyên status (số) & password_changed cho frontend map.
     * Với change_status: giá trị là chuỗi status thô → trả nguyên.
     */
    private function resolveSnapshot($value, $employeeInfoMap, $companyMap, $riceLocationMap)
    {
        if (!$value) {
            return null;
        }

        $data = is_string($value) ? json_decode($value, true) : null;
        if (!is_array($data)) {
            return $value; // change_status: "1"/"0"
        }

        if (!empty($data['company_ids']) && is_array($data['company_ids'])) {
            $data['company_ids'] = array_values(array_map(
                fn($cid) => $companyMap[$cid] ?? $cid,
                $data['company_ids']
            ));
        }
        if (!empty($data['rice_setting_location_id'])) {
            $data['rice_setting_location_id'] = $riceLocationMap[$data['rice_setting_location_id']]
                ?? $data['rice_setting_location_id'];
        }
        if (!empty($data['employee_info_id'])) {
            $data['employee_info_id'] = $employeeInfoMap[$data['employee_info_id']]
                ?? $data['employee_info_id'];
        }

        return json_encode($data, JSON_UNESCAPED_UNICODE);
    }
```

- [ ] **Step 3: Thêm route**

Trong `hrm-api/Modules/Human/Routes/api.php`, group `/human/employee` (dòng ~167), thêm route `/histories` **ngay trước** `Route::get('/{id}', ...)`:

```php
        Route::get('/{id}/histories', [EmployeeController::class, 'histories']);
        Route::get('/{id}', [EmployeeController::class, 'show']);
```

(Đặt trước `/{id}` để Laravel khớp đúng; thực tế segment `/histories` khác nên không bị nuốt, nhưng đặt trước cho chắc.)

- [ ] **Step 4: Xác minh endpoint**

Run: `php artisan route:list --path=human/employee | grep histories`
Expected: in ra dòng `GET|HEAD  api/.../human/employee/{id}/histories ... EmployeeController@histories`.

Sau đó gọi thực tế (qua trình duyệt/Postman đã đăng nhập) `GET /api/v1/human/employee/{id}/histories` với một id đã có lịch sử.
Expected: JSON `{ code: 200, message: "success", data: [ { id, action, old_value, new_value, changed_by_name, changed_at } ... ] }`, trong đó `company_ids` trong `new_value` là mảng **tên công ty** (không phải số).

- [ ] **Step 5: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-api add Modules/Human/Http/Controllers/Api/V1/EmployeeController.php Modules/Human/Routes/api.php
git -C D:/laragon/www/hrm/hrm-api commit -m "feat(human): endpoint lich su tai khoan nhan vien voi resolve ID->ten"
```

---

## Task 6: Frontend — `EmployeeHistoryModal.vue`

**Files:**
- Create: `hrm-client/pages/human/employee/components/EmployeeHistoryModal.vue`

- [ ] **Step 1: Tạo component modal**

Tạo `hrm-client/pages/human/employee/components/EmployeeHistoryModal.vue`:

```vue
<template>
    <b-modal id="employee-history-modal" title="Lịch sử thay đổi tài khoản" scrollable size="lg" body-class="p-0">
        <template #modal-header="{ close }">
            <div class="d-flex align-items-center justify-content-between w-100">
                <h5 class="mb-0 d-flex align-items-baseline" style="gap: 8px">
                    <i class="ri-history-line text-primary"></i>
                    <span>Lịch sử thay đổi tài khoản</span>
                    <small v-if="subtitle" class="text-muted font-weight-normal">{{ subtitle }}</small>
                </h5>
                <b-button size="sm" variant="light" class="border-0" @click="close" title="Đóng">
                    <i class="ri-close-line"></i>
                </b-button>
            </div>
        </template>

        <div class="p-3">
            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div>
            </div>

            <div v-else-if="!historyItems.length" class="text-center py-5" style="color: #9ca3af; font-style: italic">
                <i class="ri-history-line" style="font-size: 40px"></i>
                <p class="mt-2 mb-0">Chưa có lịch sử thao tác nào.</p>
            </div>

            <ul v-else class="ho-timeline">
                <li v-for="(log, i) in historyItems" :key="'hl-' + i" class="ho-timeline-item">
                    <div class="ho-timeline-dot" :class="getActionColor(log.action)"></div>
                    <div class="ho-timeline-content">
                        <div class="ho-timeline-time">{{ log.changed_at }}</div>
                        <div class="ho-timeline-text font-weight-bold">{{ getActionLabel(log.action) }}</div>
                        <div class="ho-timeline-actor" v-if="log.changed_by_name">— {{ log.changed_by_name }}</div>

                        <div v-if="log.action === 'update' && log.changes && log.changes.length" class="mt-2">
                            <template v-for="(change, ci) in log.changes">
                                <div v-if="change.type === 'list'" :key="ci" class="change-item change-item--list">
                                    <div class="change-field mb-1">{{ change.field }}:</div>
                                    <div v-if="change.removed.length" class="change-list-group">
                                        <div v-for="(r, ri) in change.removed" :key="'r' + ri" class="change-list-row removed">
                                            <i class="ri-subtract-line"></i> {{ r }}
                                        </div>
                                    </div>
                                    <div v-if="change.added.length" class="change-list-group">
                                        <div v-for="(a, ai) in change.added" :key="'a' + ai" class="change-list-row added">
                                            <i class="ri-add-line"></i> {{ a }}
                                        </div>
                                    </div>
                                </div>
                                <div v-else :key="ci" class="change-item">
                                    <span class="change-field">{{ change.field }}:</span>
                                    <span class="change-old" v-if="change.old">{{ change.old }}</span>
                                    <i class="ri-arrow-right-line mx-1 text-muted" v-if="change.old"></i>
                                    <span class="change-new">{{ change.new }}</span>
                                </div>
                            </template>
                        </div>

                        <div v-if="log.action === 'change_status'" class="mt-2">
                            <div class="change-item">
                                <span class="change-field">Trạng thái:</span>
                                <span class="change-old">{{ getStatusLabel(log.old_value) }}</span>
                                <i class="ri-arrow-right-line mx-1 text-muted"></i>
                                <span class="change-new">{{ getStatusLabel(log.new_value) }}</span>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>

        <template #modal-footer>
            <b-button variant="light" @click="$bvModal.hide('employee-history-modal')">
                <i class="ri-close-circle-line mr-1"></i>Đóng
            </b-button>
        </template>
    </b-modal>
</template>

<script>
const ACTION_LABELS = {
    create: 'Tạo mới tài khoản',
    update: 'Cập nhật thông tin',
    change_status: 'Thay đổi trạng thái',
}

const ACTION_COLORS = {
    create: 'green',
    update: 'amber',
    change_status: 'blue',
}

const STATUS_LABELS = {
    1: 'Hoạt động',
    0: 'Khóa',
}

const FIELD_LABELS = {
    email: 'Email',
    status: 'Trạng thái',
    company_ids: 'Công ty',
    rice_setting_location_id: 'Địa điểm nhận suất ăn',
    employee_info_id: 'Hồ sơ liên kết',
    password_changed: 'Mật khẩu',
}

const LIST_FIELDS = ['company_ids']

const IGNORED_FIELDS = ['employee_info_id']

export default {
    name: 'EmployeeHistoryModal',
    data() {
        return {
            loading: false,
            subtitle: '',
            historyItems: [],
        }
    },
    methods: {
        async open(item) {
            this.subtitle = item.email || ''
            this.historyItems = []
            this.$bvModal.show('employee-history-modal')
            await this.fetchHistory(item.id)
        },
        async fetchHistory(id) {
            this.loading = true
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', `human/employee/${id}/histories`)
                const raw = data || []
                this.historyItems = raw.map((h) => this.parseHistoryItem(h))
            } catch (error) {
                console.error(error)
                this.$toasted?.global?.error?.({ message: 'Lỗi khi tải lịch sử' })
            } finally {
                this.loading = false
            }
        },
        parseHistoryItem(item) {
            const result = { ...item, changes: [] }
            if (item.action === 'update') {
                result.changes = this.diffJson(item.old_value, item.new_value)
            }
            return result
        },
        diffJson(oldStr, newStr) {
            try {
                const oldObj = typeof oldStr === 'string' ? JSON.parse(oldStr) : oldStr
                const newObj = typeof newStr === 'string' ? JSON.parse(newStr) : newStr
                if (!oldObj || !newObj) return []

                const changes = []

                // Mật khẩu: chỉ hiển thị khi đổi (false -> true)
                if (!oldObj.password_changed && newObj.password_changed) {
                    changes.push({ type: 'text', field: FIELD_LABELS.password_changed, old: '', new: 'Đã thay đổi' })
                }

                for (const key of Object.keys(newObj)) {
                    if (key === 'password_changed') continue
                    if (IGNORED_FIELDS.includes(key)) continue

                    if (LIST_FIELDS.includes(key)) {
                        const oldArr = Array.isArray(oldObj[key]) ? oldObj[key] : []
                        const newArr = Array.isArray(newObj[key]) ? newObj[key] : []
                        const oldSet = oldArr.map(String)
                        const newSet = newArr.map(String)
                        const removed = oldSet.filter((x) => !newSet.includes(x))
                        const added = newSet.filter((x) => !oldSet.includes(x))
                        if (removed.length || added.length) {
                            changes.push({ type: 'list', field: FIELD_LABELS[key] || key, removed, added })
                        }
                        continue
                    }

                    const oldVal = this.formatValue(key, oldObj[key])
                    const newVal = this.formatValue(key, newObj[key])
                    if (oldVal !== newVal) {
                        changes.push({
                            type: 'text',
                            field: FIELD_LABELS[key] || key,
                            old: oldVal || '(trống)',
                            new: newVal || '(trống)',
                        })
                    }
                }
                return changes
            } catch {
                return []
            }
        },
        formatValue(key, val) {
            if (val === null || val === undefined) return ''
            if (key === 'status') return STATUS_LABELS[val] || val
            if (Array.isArray(val)) return val.join(', ')
            if (typeof val === 'object') return JSON.stringify(val)
            return String(val)
        },
        getActionLabel(action) {
            return ACTION_LABELS[action] || action
        },
        getActionColor(action) {
            return ACTION_COLORS[action] || 'gray'
        },
        getStatusLabel(status) {
            const key = typeof status === 'string' ? parseInt(status) : status
            return STATUS_LABELS[key] !== undefined ? STATUS_LABELS[key] : status
        },
    },
}
</script>

<style scoped>
.ho-timeline {
    padding: 0;
    list-style: none;
    margin: 0;
}
.ho-timeline-item {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    position: relative;
}
.ho-timeline-item:not(:last-child)::before {
    content: '';
    position: absolute;
    left: 7px;
    top: 28px;
    bottom: 0;
    width: 2px;
    background: #e5e7eb;
}
.ho-timeline-dot {
    width: 16px;
    height: 16px;
    border-radius: 999px;
    flex: 0 0 auto;
    margin-top: 2px;
}
.ho-timeline-dot.green {
    background: #dcfce7;
    border: 2px solid #16a34a;
}
.ho-timeline-dot.amber {
    background: #fef3c7;
    border: 2px solid #d97706;
}
.ho-timeline-dot.blue {
    background: #dbeafe;
    border: 2px solid #2563eb;
}
.ho-timeline-dot.gray {
    background: #f3f4f6;
    border: 2px solid #9ca3af;
}
.ho-timeline-time {
    font-size: 11px;
    color: #9ca3af;
    font-family: monospace;
}
.ho-timeline-text {
    font-size: 13px;
    color: #374151;
    margin-top: 2px;
}
.ho-timeline-actor {
    font-size: 11px;
    color: #6b7280;
    margin-top: 2px;
}
.change-item {
    font-size: 12px;
    padding: 3px 8px;
    background: #f8fafc;
    border-radius: 4px;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px;
}
.change-field {
    font-weight: 600;
    color: #475569;
    margin-right: 4px;
}
.change-old {
    color: #dc2626;
    word-break: break-word;
}
.change-new {
    color: #16a34a;
    font-weight: 500;
    word-break: break-word;
}
.change-item--list {
    flex-direction: column;
    align-items: flex-start;
}
.change-list-group {
    width: 100%;
}
.change-list-row {
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 3px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.change-list-row.removed {
    color: #dc2626;
    background: #fef2f2;
}
.change-list-row.added {
    color: #16a34a;
    background: #f0fdf4;
}
.change-list-row i {
    font-size: 14px;
    flex-shrink: 0;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-client add pages/human/employee/components/EmployeeHistoryModal.vue
git -C D:/laragon/www/hrm/hrm-client commit -m "feat(human): them EmployeeHistoryModal cho lich su tai khoan"
```

---

## Task 7: Frontend — nút "Lịch sử" + đăng ký modal trong `index.vue`

**Files:**
- Modify: `hrm-client/pages/human/employee/index.vue`

- [ ] **Step 1: Thêm nút "Lịch sử" vào cell Actions**

Trong `pages/human/employee/index.vue`, trong `<template v-slot:cell(Actions)="{ item }">` (dòng ~151), thêm nút **trước** nút xóa (sau nút sửa, dòng ~160):

```html
                                        <b-button
                                            variant="info"
                                            class="btn-mini"
                                            @click="$refs.employeeHistoryModal.open(item)"
                                            v-if="hasPermissionEmployeeAccount"
                                            title="Lịch sử thay đổi"
                                        >
                                            <i class="ri-history-line"></i>
                                        </b-button>
```

- [ ] **Step 2: Đặt component modal trong template**

Ngay trước thẻ đóng `</div>` ngoài cùng của template (hoặc cạnh modal xóa hiện có), thêm:

```html
        <EmployeeHistoryModal ref="employeeHistoryModal" />
```

- [ ] **Step 3: Import + đăng ký component**

Trong khối `<script>` của `index.vue`, thêm import (cùng chỗ các import khác) và đăng ký vào `components`:

```js
import EmployeeHistoryModal from './components/EmployeeHistoryModal.vue'
```

Và trong object `components: { ... }` thêm:

```js
        EmployeeHistoryModal,
```

(Nếu `index.vue` chưa có khối `components`, thêm `components: { EmployeeHistoryModal },` vào trong `export default {`.)

- [ ] **Step 4: Xác minh trên UI**

Chạy client (`yarn dev` / `npm run dev` ở `hrm-client` nếu chưa chạy), mở màn `human/employee`. Với mỗi dòng có nút lịch sử (icon đồng hồ). Bấm vào một tài khoản đã có thay đổi.
Expected:
- Modal "Lịch sử thay đổi tài khoản" mở ra.
- Hiển thị timeline: dòng "Tạo mới tài khoản", các dòng "Cập nhật thông tin" với diff (vd Công ty thêm/bớt, Địa điểm nhận suất ăn cũ→mới, "Mật khẩu: Đã thay đổi"), và "Thay đổi trạng thái" Hoạt động→Khóa.
- Tên công ty/địa điểm hiển thị bằng chữ (không phải số ID).

- [ ] **Step 5: Commit**

```bash
git -C D:/laragon/www/hrm/hrm-client add pages/human/employee/index.vue
git -C D:/laragon/www/hrm/hrm-client commit -m "feat(human): them nut Lich su tren danh sach tai khoan nhan vien"
```

---

## Self-Review checklist (đã rà)

- **Spec coverage:** Migration+entity (Task 1) ✓; ghi create bao phủ cả luồng auto-tạo từ hồ sơ (Task 2, vì cùng đi qua `createEmployee`) ✓; update/change_status (Task 3) ✓; updateStatus (Task 4) ✓; endpoint + resolve ID→tên (Task 5) ✓; modal + nút danh sách (Task 6–7) ✓; mật khẩu chỉ cờ, không lưu giá trị (Task 2 snapshot + Task 6 hiển thị) ✓.
- **Deviation có chủ đích so với spec:** spec nêu `EmployeeHistoryResource`; plan format trong controller (`formatHistories()`) để bám pattern `getLogs` sẵn có & tránh N+1. Đã ghi rõ.
- **Type consistency:** `buildHistorySnapshot()` trả keys `email/status/employee_info_id/rice_setting_location_id/company_ids/password_changed` — khớp với `resolveSnapshot()` (Task 5) và `FIELD_LABELS`/`LIST_FIELDS`/`diffJson` ở frontend (Task 6). `logHistory()` signature `($employeeId,$action,$oldValue,$newValue)` nhất quán giữa Task 2 và 3. Action strings `create/update/change_status` nhất quán BE↔FE.
- **Placeholder scan:** không còn TBD/TODO; mọi step code có nội dung cụ thể.
