# Lịch sử chỉnh sửa tab Chung (Quy định chung) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Người phụ trách:** @khoipv
**Goal:** Ghi lịch sử chỉnh sửa 14 trường tab "Chung" màn Quy định chung và hiển thị qua modal timeline giống EmployeeHistoryModal.

**Architecture:** Bảng log mới `general_regulation_history` (old/new = JSON chỉ gồm trường thay đổi, diff ở BE trong `GeneralRegulationService::save()`); endpoint `GET general-regulations/histories` scope theo công ty; FE thêm nút mở modal timeline mới `GeneralHistoryModal.vue` copy pattern `EmployeeHistoryModal.vue`, bộ lọc client-side.

**Tech Stack:** PHP 7.4 / Laravel 8 (Modules/Timesheet), MySQL; Nuxt 2 / Vue 2 + Bootstrap-Vue, V2Base components.

**Spec:** `docs/superpowers/specs/2026-07-10-general-regulations-history-design.md`

## Global Constraints

- PHP 7.4: KHÔNG dùng `?->`, named arguments, match.
- KHÔNG commit/push git ở bất kỳ bước nào.
- KHÔNG thêm permission mới, KHÔNG sửa PermissionsTableSeeder (route chỉ `auth:api`).
- KHÔNG log `profit_margin_threshold` hay bất kỳ cột nào ngoài 14 TRACKED_FIELDS.
- Migration PHẢI có PHPDoc trên `up()`/`down()` theo mẫu project (xem `2026_06_01_000001_create_employee_history_table.php`).
- FE: trước khi code Task 4-5 phải đọc `.claude/skills/modal-popup/SKILL.md` và `.claude/skills/button-convention/SKILL.md`, nếu convention khác code mẫu trong plan thì ưu tiên skill.
- KHÔNG tự chạy `php artisan migrate` trên DB user nếu user chưa đồng ý — hỏi trước khi migrate (Task 1 Step 3).

---

## Phase 1 — Backend

### Task 1: Migration + Entity `GeneralRegulationHistory`

**Files:**
- Create: `hrm-api/Modules/Timesheet/Database/Migrations/2026_07_10_000001_create_general_regulation_history_table.php`
- Create: `hrm-api/Modules/Timesheet/Entities/GeneralRegulationHistory.php`

**Interfaces:**
- Produces: model `Modules\Timesheet\Entities\GeneralRegulationHistory` (fillable: general_regulation_id, company_id, action, old_value, new_value, changed_by, changed_at; relation `user()` → `Modules\Human\Entities\Employee`) — Task 2 dùng.

- [x] **Step 1: Viết migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateGeneralRegulationHistoryTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('general_regulation_history', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('general_regulation_id')->index()->comment('ID bản ghi quy định chung');
            $table->unsignedBigInteger('company_id')->nullable()->index()->comment('Công ty của bản ghi quy định chung');
            $table->string('action')->comment('Loại thao tác: update');
            $table->text('old_value')->nullable()->comment('Giá trị cũ — JSON chỉ gồm các trường thay đổi');
            $table->text('new_value')->nullable()->comment('Giá trị mới — JSON chỉ gồm các trường thay đổi');
            $table->unsignedBigInteger('changed_by')->nullable()->comment('Người thực hiện thay đổi');
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
        Schema::dropIfExists('general_regulation_history');
    }
}
```

- [x] **Step 2: Viết entity**

```php
<?php

namespace Modules\Timesheet\Entities;

use App\Models\BaseModel;
use Modules\Human\Entities\Employee;

class GeneralRegulationHistory extends BaseModel
{
    protected $table = 'general_regulation_history';

    protected $fillable = [
        'general_regulation_id',
        'company_id',
        'action',
        'old_value',
        'new_value',
        'changed_by',
        'changed_at',
    ];

    public function user()
    {
        return $this->belongsTo(Employee::class, 'changed_by');
    }
}
```

> Trước khi viết: mở `hrm-api/Modules/Human/Entities/EmployeeHistory.php` xác nhận base class `App\Models\BaseModel` tồn tại đúng namespace; nếu Employee model trong project là class khác thì dùng đúng class mà `EmployeeHistory::user()` đang dùng.

- [x] **Step 3: php -l 2 file + HỎI USER rồi mới migrate** — user đồng ý 2026-07-10, migrated OK

Run: `php -l <từng file>` → Expected: `No syntax errors detected`.
Hỏi user cho phép chạy `php artisan migrate` (chỉ tạo bảng mới, không đụng bảng cũ). Sau khi user đồng ý:
Run (trong `hrm-api/`): `php artisan migrate`
Expected: `Migrated: 2026_07_10_000001_create_general_regulation_history_table`.

- [x] **Step 4: Verify tinker tạo/xoá bản ghi** — PASS (created id=1, relation Employee, cleaned)

Tạo file scratchpad `verify_task1.php`:
```php
<?php
$h = \Modules\Timesheet\Entities\GeneralRegulationHistory::create([
    'general_regulation_id' => 1, 'company_id' => 1, 'action' => 'update',
    'old_value' => json_encode(['max_distance' => 100]),
    'new_value' => json_encode(['max_distance' => 200]),
    'changed_by' => 1,
]);
echo 'created id=' . $h->id . PHP_EOL;
echo 'user relation ok: ' . get_class($h->user()->getRelated()) . PHP_EOL;
\Modules\Timesheet\Entities\GeneralRegulationHistory::where('id', $h->id)->delete();
echo 'cleaned' . PHP_EOL;
```
Run: `php artisan tinker <path>/verify_task1.php`
Expected: in `created id=N`, class Employee, `cleaned`.

### Task 2: Ghi log trong `GeneralRegulationService::save()` + method `histories()`

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Services/GeneralRegulationService.php`

**Interfaces:**
- Consumes: `GeneralRegulationHistory` (Task 1).
- Produces: `GeneralRegulationService::histories(): array` — mảng item `{id, action, old_value, new_value, changed_by, changed_by_name, changed_at (d/m/Y H:i:s), changed_at_raw (Y-m-d)}` — Task 3 dùng. `save()` giữ nguyên signature/return.

- [x] **Step 1: Thêm import + constants + sửa `save()` + thêm private helpers + `histories()`**

Import thêm đầu file: `use Modules\Timesheet\Entities\GeneralRegulationHistory;`

Thêm constants trong class:
```php
    /** 14 trường tab "Chung" được ghi lịch sử chỉnh sửa (spec 2026-07-10-general-regulations-history) */
    const TRACKED_FIELDS = [
        'basis_for_calculating_weekend',
        'update_working_in_month',
        'update_working_time',
        'update_working_in_hour',
        'update_working_hour',
        'update_late_in_out_hour',
        'not_goong_working_shift',
        'timekeeping_max_distance',
        'max_distance',
        'max_distance_for_business_trip',
        'max_distance_for_over_time',
        'min_days_for_insurance',
        'map_provider_type',
        'note_email',
    ];

    /** Các trường bật/tắt — FE gửi true/false, DB lưu 0/1 → cần chuẩn hoá trước khi so sánh */
    const BOOLEAN_TRACKED_FIELDS = [
        'update_working_in_month',
        'update_working_in_hour',
        'not_goong_working_shift',
        'timekeeping_max_distance',
    ];
```

Sửa `save()` (giữ nguyên phần còn lại):
```php
    public function save(array $attributes)
    {
        $company_id = auth()->user()->current_company_role;
        $entity = $this->model->where('company_id', '=', $company_id)->first();
        if ($entity) {
            $oldSnapshot = $this->buildTrackedSnapshot($entity);
            $entity->fill($attributes)->save();
            $this->logHistoryIfChanged($entity, $oldSnapshot);
            return $entity;
        } else {
            return null;
        }
    }
```

Thêm các method mới cuối class:
```php
    /**
     * Chụp giá trị đã chuẩn hoá của 14 trường tab Chung.
     */
    private function buildTrackedSnapshot(GeneralRegulation $entity)
    {
        $snapshot = [];
        foreach (self::TRACKED_FIELDS as $field) {
            $snapshot[$field] = $this->normalizeTrackedValue($field, $entity->getAttribute($field));
        }
        return $snapshot;
    }

    /**
     * Chuẩn hoá giá trị để so sánh/lưu log: rỗng → null, boolean → 0/1,
     * numeric → số (int nếu tròn), còn lại → string. Tránh log rác kiểu "5" → 5.
     */
    private function normalizeTrackedValue($field, $value)
    {
        if ($value === null || $value === '') {
            return null;
        }
        if (in_array($field, self::BOOLEAN_TRACKED_FIELDS, true)) {
            return filter_var($value, FILTER_VALIDATE_BOOLEAN) ? 1 : 0;
        }
        if (is_numeric($value)) {
            $number = (float) $value;
            return $number == (int) $number ? (int) $number : $number;
        }
        return (string) $value;
    }

    /**
     * So sánh snapshot trước/sau khi lưu, có trường thay đổi thì ghi 1 dòng lịch sử
     * (old/new = JSON chỉ gồm các trường đổi). Không đổi gì → không ghi.
     */
    private function logHistoryIfChanged(GeneralRegulation $entity, array $oldSnapshot)
    {
        $oldChanged = [];
        $newChanged = [];
        foreach (self::TRACKED_FIELDS as $field) {
            $newValue = $this->normalizeTrackedValue($field, $entity->getAttribute($field));
            if ($oldSnapshot[$field] !== $newValue) {
                $oldChanged[$field] = $oldSnapshot[$field];
                $newChanged[$field] = $newValue;
            }
        }
        if (empty($newChanged)) {
            return;
        }
        GeneralRegulationHistory::create([
            'general_regulation_id' => $entity->id,
            'company_id' => $entity->company_id,
            'action' => 'update',
            'old_value' => json_encode($oldChanged, JSON_UNESCAPED_UNICODE),
            'new_value' => json_encode($newChanged, JSON_UNESCAPED_UNICODE),
            'changed_by' => auth()->id(),
            'changed_at' => Carbon::now(),
        ]);
    }

    /**
     * Lịch sử chỉnh sửa quy định chung của công ty hiện tại (mới nhất trước).
     */
    public function histories()
    {
        $companyId = auth()->user()->current_company_role;
        $logs = GeneralRegulationHistory::with('user.info')
            ->where('company_id', $companyId)
            ->orderBy('changed_at', 'desc')
            ->orderBy('id', 'desc')
            ->get();

        return $logs->map(function ($log) {
            $changedByName = null;
            if ($log->user) {
                $changedByName = optional($log->user->info)->fullname ?: $log->user->email;
            }
            $changedAt = $log->changed_at ? Carbon::parse($log->changed_at) : null;

            return [
                'id' => $log->id,
                'action' => $log->action,
                'old_value' => $log->old_value,
                'new_value' => $log->new_value,
                'changed_by' => $log->changed_by,
                'changed_by_name' => $changedByName ?: '—',
                'changed_at' => $changedAt ? $changedAt->format('d/m/Y H:i:s') : '',
                'changed_at_raw' => $changedAt ? $changedAt->format('Y-m-d') : '',
            ];
        })->values()->all();
    }
```

> Trước khi code: xác nhận relation `info()` tồn tại trên model Employee (xem `EmployeeController::formatHistories` của Human đang dùng `user.info`). Nếu tên khác thì dùng đúng tên đó.

- [x] **Step 2: php -l** — sạch

Run: `php -l hrm-api/Modules/Timesheet/Services/GeneralRegulationService.php`
Expected: `No syntax errors detected`.

- [x] **Step 3: Verify tinker diff logic** — 6/6 case PASS, đã khôi phục giá trị + dọn log test (count về 0)

Tạo scratchpad `verify_task2.php` (dùng company có sẵn record general_regulations; Auth::setUser 1 user thật của company đó):
```php
<?php
use Modules\Timesheet\Entities\GeneralRegulation;
use Modules\Timesheet\Entities\GeneralRegulationHistory;
use Illuminate\Support\Facades\Auth;

$user = \Modules\Human\Entities\Employee::find(13); // user DNS Admin — chỉnh id nếu cần
Auth::setUser($user);
$service = app(\Modules\Timesheet\Services\GeneralRegulationService::class);
$entity = GeneralRegulation::where('company_id', $user->current_company_role)->first();
$origMax = $entity->max_distance;
$countBefore = GeneralRegulationHistory::count();

// Case 1: đổi 1 trường → +1 log, subset đúng 1 key
$service->save(['max_distance' => ($origMax ?: 0) + 111]);
$log = GeneralRegulationHistory::orderBy('id', 'desc')->first();
echo 'case1 +log: ' . (GeneralRegulationHistory::count() - $countBefore) . PHP_EOL; // 1
echo 'case1 new_value: ' . $log->new_value . PHP_EOL; // {"max_distance":<orig+111>}

// Case 2: lưu lại đúng giá trị đó (không đổi) → không thêm log
$service->save(['max_distance' => ($origMax ?: 0) + 111]);
echo 'case2 +log: ' . (GeneralRegulationHistory::count() - $countBefore) . PHP_EOL; // vẫn 1

// Case 3: chỉ profit_margin_threshold → không log
$service->save(['profit_margin_threshold' => 33]);
echo 'case3 +log: ' . (GeneralRegulationHistory::count() - $countBefore) . PHP_EOL; // vẫn 1

// Case 4: boolean true/false vs 0/1 — gửi lại đúng giá trị hiện tại dạng boolean → không log
$service->save(['not_goong_working_shift' => (bool) $entity->fresh()->not_goong_working_shift]);
echo 'case4 +log: ' . (GeneralRegulationHistory::count() - $countBefore) . PHP_EOL; // vẫn 1

// Case 5: đổi 2 trường 1 lần → 1 dòng log 2 key
$service->save(['max_distance' => ($origMax ?: 0) + 222, 'update_late_in_out_hour' => 99]);
$log5 = GeneralRegulationHistory::orderBy('id', 'desc')->first();
echo 'case5 keys: ' . implode(',', array_keys(json_decode($log5->new_value, true))) . PHP_EOL;

// Case 6: histories() format
$rows = $service->histories();
echo 'histories first: ' . json_encode($rows[0], JSON_UNESCAPED_UNICODE) . PHP_EOL;

// Khôi phục + dọn log test
$service->save(['max_distance' => $origMax, 'update_late_in_out_hour' => $entity->update_late_in_out_hour]);
GeneralRegulationHistory::where('id', '>', $log && $countBefore >= 0 ? 0 : 0)->where('created_at', '>=', now()->subMinutes(10))->delete();
echo 'cleaned, count=' . GeneralRegulationHistory::count() . PHP_EOL;
```
Run: `php artisan tinker <path>/verify_task2.php`
Expected: case1=1, case2=1, case3=1, case4=1, case5 keys=`max_distance,update_late_in_out_hour`, histories first có đủ 8 key + changed_by_name ≠ rỗng, cuối cùng count về như ban đầu.
> LƯU Ý: khôi phục `profit_margin_threshold` về giá trị cũ nếu case 3 làm đổi (đọc giá trị trước khi chạy). Dọn SẠCH log test trước khi kết thúc task.

### Task 3: Controller `histories()` + route

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Http/Controllers/Api/V1/GeneralRegulationController.php`
- Modify: `hrm-api/Modules/Timesheet/Routes/api.php` (group `general-regulations`, dòng 286-290)

**Interfaces:**
- Consumes: `GeneralRegulationService::histories()` (Task 2).
- Produces: `GET /api/v1/general-regulations/histories` → `{message: 'success', data: [...]}` — FE Task 4 gọi qua `apiGetMethod('general-regulations/histories')`.

- [x] **Step 1: Thêm method vào controller** (sau `getColumn`, dùng đúng style try/catch của `getColumn`)

```php
    public function histories()
    {
        try {
            $result = $this->generalRegulationService->histories();

            return $this->responseJson('success', Response::HTTP_OK, $result);
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
```

- [x] **Step 2: Thêm route** trong group hiện có (`Modules/Timesheet/Routes/api.php:286-290`):

```php
    Route::group(array('prefix' => '/general-regulations', 'middleware' => 'auth:api'), function () {
        Route::get('/', [GeneralRegulationController::class, 'index']);
        Route::post('/', [GeneralRegulationController::class, 'update']);
        Route::get('/get-column', [GeneralRegulationController::class, 'getColumn']);
        Route::get('/histories', [GeneralRegulationController::class, 'histories']);
    });
```

- [x] **Step 3: Verify**

Run: `php -l` 2 file → No syntax errors. ĐÃ PASS.
`php artisan route:list` crash do lỗi CÓ SẴN module Decision (web.php:17 trỏ DecisionController thiếu namespace V1 — không liên quan feature này, cần báo user); route đã verify bằng script bootstrap router thật: `GET|HEAD api/v1/general-regulations/histories → GeneralRegulationController@histories [api,auth:api]`.

## Phase 2 — Frontend

### Task 4: Component `GeneralHistoryModal.vue`

**Files:**
- Create: `hrm-client/components/setting/general/GeneralHistoryModal.vue`

**Interfaces:**
- Produces: component `GeneralHistoryModal` expose method `open()` (không tham số) — Task 5 gọi `$refs.generalHistoryModal.open()`.
- Consumes: API `GET general-regulations/histories` (Task 3) qua `this.$store.dispatch('apiGetMethod', 'general-regulations/histories')`.

- [x] **Step 0: Đọc `.claude/skills/modal-popup/SKILL.md`** — đã áp dụng: hide-footer + footer tự viết (V2BaseButton tertiary "Đóng" + fa-arrow-left), header icon tròn + nút X `class="close"`, content-class="shadow", closeModal() — thay cho footer/header mẫu trong brief.

- [x] **Step 1: Viết component** — copy khung `pages/human/employee/components/EmployeeHistoryModal.vue` với các thay đổi: id modal `general-history-modal`, title "Lịch sử thay đổi quy định chung", KHÔNG cần diffJson (BE diff sẵn), KHÔNG có action create/change_status/password. Code đầy đủ:

```vue
<template>
    <b-modal id="general-history-modal" title="Lịch sử thay đổi quy định chung" scrollable size="lg" body-class="p-0">
        <template #modal-header="{ close }">
            <div class="d-flex align-items-center justify-content-between w-100">
                <h5 class="mb-0 d-flex align-items-baseline" style="gap: 8px">
                    <i class="ri-history-line text-primary"></i>
                    <span>Lịch sử thay đổi quy định chung</span>
                </h5>
                <b-button size="sm" variant="light" class="border-0" @click="close" title="Đóng">
                    <i class="ri-close-line"></i>
                </b-button>
            </div>
        </template>

        <div class="px-3 pb-3 pt-2">
            <div v-if="!loading && historyItems.length" class="d-flex justify-content-end">
                <V2BaseButton secondary size="sm" @click="showFilter = !showFilter">
                    <template #prefix><i class="ri-filter-3-line" style="font-size: 15px"></i></template>
                    Bộ lọc
                </V2BaseButton>
            </div>

            <b-collapse v-model="showFilter" class="mt-1">
                <div v-if="!loading && historyItems.length" class="gh-filter-bar form-row">
                    <div class="col-md-3 mb-2">
                        <V2BaseLabel>Trường chỉnh sửa</V2BaseLabel>
                        <V2BaseSelectInModal
                            v-model="filters.field"
                            :options="fieldOptions"
                            :allowClear="true"
                            placeholder="Tất cả trường"
                        />
                    </div>
                    <div class="col-md-3 mb-2">
                        <V2BaseLabel>Người thực hiện</V2BaseLabel>
                        <V2BaseSelectInModal
                            v-model="filters.performer"
                            :options="performerOptions"
                            :allowClear="true"
                            placeholder="Tất cả người thực hiện"
                        />
                    </div>
                    <div class="col-md-3 mb-2">
                        <V2BaseLabel>Từ ngày</V2BaseLabel>
                        <V2BaseDatePicker
                            v-model="filters.dateFrom"
                            type="date"
                            value-type="YYYY-MM-DD"
                            format="DD/MM/YYYY"
                            size="sm"
                            placeholder="Từ ngày"
                        />
                    </div>
                    <div class="col-md-3 mb-2">
                        <V2BaseLabel>Đến ngày</V2BaseLabel>
                        <V2BaseDatePicker
                            v-model="filters.dateTo"
                            type="date"
                            value-type="YYYY-MM-DD"
                            format="DD/MM/YYYY"
                            size="sm"
                            placeholder="Đến ngày"
                        />
                    </div>
                    <div class="col-12 text-right mt-1">
                        <V2BaseButton primary size="sm" class="mr-2" @click="applyFilter">
                            <template #prefix><i class="ri-search-line" style="font-size: 15px"></i></template>
                            Tìm kiếm
                        </V2BaseButton>
                        <V2BaseButton tertiary size="sm" @click="resetFilters">
                            <template #prefix><i class="ri-refresh-line" style="font-size: 15px"></i></template>
                            Làm mới
                        </V2BaseButton>
                    </div>
                </div>
            </b-collapse>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div>
            </div>

            <div v-else-if="!historyItems.length" class="text-center py-5" style="color: #9ca3af; font-style: italic">
                <i class="ri-history-line" style="font-size: 40px"></i>
                <p class="mt-2 mb-0">Chưa có lịch sử thay đổi.</p>
            </div>

            <div
                v-else-if="!filteredHistory.length"
                class="text-center py-4"
                style="color: #9ca3af; font-style: italic"
            >
                <i class="ri-filter-off-line" style="font-size: 32px"></i>
                <p class="mt-2 mb-0">Không có lịch sử phù hợp bộ lọc.</p>
            </div>

            <ul v-else class="ho-timeline">
                <li v-for="(log, i) in filteredHistory" :key="'gh-' + i" class="ho-timeline-item">
                    <div class="ho-timeline-dot amber"></div>
                    <div class="ho-timeline-content">
                        <div class="ho-timeline-time">{{ log.changed_at }}</div>
                        <div class="ho-timeline-text font-weight-bold">Cập nhật quy định chung</div>
                        <div class="ho-timeline-actor" v-if="log.changed_by_name">— {{ log.changed_by_name }}</div>
                        <div v-if="log.changes && log.changes.length" class="mt-2">
                            <div v-for="(change, ci) in log.changes" :key="ci" class="change-item">
                                <span class="change-field">{{ change.field }}:</span>
                                <span class="change-old" :title="change.oldTitle">{{ change.old }}</span>
                                <i class="ri-arrow-right-line mx-1 text-muted"></i>
                                <span class="change-new" :title="change.newTitle">{{ change.new }}</span>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>

        <template #modal-footer>
            <b-button variant="light" @click="$bvModal.hide('general-history-modal')">
                <i class="ri-close-circle-line mr-1"></i>Đóng
            </b-button>
        </template>
    </b-modal>
</template>

<script>
// Nhãn 14 trường tab Chung được track (khớp TRACKED_FIELDS BE + nhãn UI General.vue)
const FIELD_LABELS = {
    basis_for_calculating_weekend: 'Nghỉ tuần',
    update_working_in_month: 'Bật/tắt số lần tra soát công tối đa trong tháng',
    update_working_time: 'Số lần tra soát công tối đa trong tháng',
    update_working_in_hour: 'Bật/tắt tra soát công trong vòng X giờ',
    update_working_hour: 'Số giờ được tra soát công',
    update_late_in_out_hour: 'Lập đơn đi muộn/về sớm trước (giờ)',
    not_goong_working_shift: 'Không sử dụng google map với ca làm việc',
    timekeeping_max_distance: 'Bật/tắt khoảng cách chấm công tối đa',
    max_distance: 'Khoảng cách chấm công tối đa (m)',
    max_distance_for_business_trip: 'Khoảng cách chấm công tối đa cho phiếu giao việc công tác (m)',
    max_distance_for_over_time: 'Khoảng cách chấm công tối đa cho làm thêm giờ (m)',
    min_days_for_insurance: 'Số ngày công tối thiểu tính BHXH',
    map_provider_type: 'Bản đồ',
    note_email: 'Nội dung đính kèm email',
}

const BOOLEAN_FIELDS = [
    'update_working_in_month',
    'update_working_in_hour',
    'not_goong_working_shift',
    'timekeeping_max_distance',
]

// Khớp weekend_options trong General.vue
const WEEKEND_LABELS = {
    0: 'Thứ 7',
    1: 'Chủ Nhật',
    2: 'Thứ 7 và CN',
    3: 'Chiều T7 và CN',
    4: 'Thứ 7 tuần chẵn và CN',
    5: 'Thứ 7 tuần lẻ và CN',
}

const MAP_PROVIDER_LABELS = {
    1: 'Sử dụng bản đồ mất phí',
    2: 'Sử dụng bản đồ miễn phí',
}

const NOTE_EMAIL_MAX_LENGTH = 100

export default {
    name: 'GeneralHistoryModal',
    data() {
        return {
            loading: false,
            historyItems: [],
            showFilter: false,
            filters: { field: null, performer: null, dateFrom: null, dateTo: null },
            appliedFilters: { field: null, performer: null, dateFrom: null, dateTo: null },
        }
    },
    computed: {
        fieldOptions() {
            return Object.keys(FIELD_LABELS).map((key) => ({ value: key, text: FIELD_LABELS[key] }))
        },
        performerOptions() {
            const map = new Map()
            this.historyItems.forEach((h) => {
                if (h.changed_by != null && !map.has(h.changed_by)) {
                    map.set(h.changed_by, h.changed_by_name || '#' + h.changed_by)
                }
            })
            return Array.from(map, ([value, text]) => ({ value, text }))
        },
        filteredHistory() {
            const f = this.appliedFilters
            return this.historyItems.filter((h) => {
                if (f.performer && String(h.changed_by) !== String(f.performer)) return false
                if (f.field && !(h.changes || []).some((c) => c.key === f.field)) return false
                if (f.dateFrom && (!h.changed_at_raw || h.changed_at_raw < f.dateFrom)) return false
                if (f.dateTo && (!h.changed_at_raw || h.changed_at_raw > f.dateTo)) return false
                return true
            })
        },
    },
    methods: {
        async open() {
            this.historyItems = []
            this.showFilter = false
            this.resetFilters()
            this.$bvModal.show('general-history-modal')
            await this.fetchHistory()
        },
        applyFilter() {
            this.appliedFilters = { ...this.filters }
        },
        resetFilters() {
            this.filters = { field: null, performer: null, dateFrom: null, dateTo: null }
            this.appliedFilters = { field: null, performer: null, dateFrom: null, dateTo: null }
        },
        async fetchHistory() {
            this.loading = true
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', 'general-regulations/histories')
                this.historyItems = (data || []).map((h) => this.parseHistoryItem(h))
            } catch (error) {
                console.error(error)
                this.$toasted.global.error({ message: 'Lỗi khi tải lịch sử' })
            } finally {
                this.loading = false
            }
        },
        // BE đã diff sẵn: old_value/new_value là JSON chỉ gồm các trường thay đổi
        parseHistoryItem(item) {
            const changes = []
            try {
                const oldObj = JSON.parse(item.old_value || '{}') || {}
                const newObj = JSON.parse(item.new_value || '{}') || {}
                Object.keys(newObj).forEach((key) => {
                    changes.push({
                        key,
                        field: FIELD_LABELS[key] || key,
                        old: this.formatValue(key, oldObj[key]),
                        new: this.formatValue(key, newObj[key]),
                        oldTitle: key === 'note_email' ? this.stripHtml(oldObj[key]) : '',
                        newTitle: key === 'note_email' ? this.stripHtml(newObj[key]) : '',
                    })
                })
            } catch (e) {
                console.error(e)
            }
            return { ...item, changes }
        },
        formatValue(key, val) {
            if (val === null || val === undefined || val === '') return '(trống)'
            if (BOOLEAN_FIELDS.includes(key)) return Number(val) ? 'Bật' : 'Tắt'
            if (key === 'basis_for_calculating_weekend') return WEEKEND_LABELS[val] || String(val)
            if (key === 'map_provider_type') return MAP_PROVIDER_LABELS[val] || String(val)
            if (key === 'note_email') {
                const text = this.stripHtml(val)
                if (!text) return '(trống)'
                return text.length > NOTE_EMAIL_MAX_LENGTH ? text.slice(0, NOTE_EMAIL_MAX_LENGTH) + '…' : text
            }
            return String(val)
        },
        stripHtml(html) {
            if (!html) return ''
            const div = document.createElement('div')
            div.innerHTML = String(html)
            return (div.textContent || div.innerText || '').trim()
        },
    },
}
</script>

<style scoped>
.gh-filter-bar {
    padding: 12px 10px;
    margin: 0 0 16px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
}
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
.ho-timeline-dot.amber {
    background: #fef3c7;
    border: 2px solid #d97706;
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
</style>
```

- [x] **Step 2: Verify compile** — project không có eslint; verify bằng vue-template-compiler (0 lỗi) + `node --check` script. Verify runtime dồn về Task 6.

### Task 5: Nút "Lịch sử thay đổi" trên tab Chung (`General.vue`)

**Files:**
- Modify: `hrm-client/components/setting/general/General.vue`

**Interfaces:**
- Consumes: `GeneralHistoryModal.open()` (Task 4).

- [x] **Step 0: Đọc `.claude/skills/button-convention/SKILL.md`** — skill thắng brief: nút "Xem log/Lịch sử" cấp page thuộc nhóm `light` (không phải secondary) → dùng V2BaseButton light + ri-history-line + size sm.

- [x] **Step 1: Thêm nút + render modal.** Trong template, ngay sau `<div class="general-st-1">` mở đầu (trước `<p class="heading">Nghỉ tuần</p>`), thêm:

```html
            <div class="d-flex justify-content-end">
                <V2BaseButton secondary size="sm" @click="$refs.generalHistoryModal.open()">
                    <template #prefix><i class="ri-history-line" style="font-size: 15px"></i></template>
                    Lịch sử thay đổi
                </V2BaseButton>
            </div>
```

Cuối template (trước `</div>` đóng `.general`), thêm:
```html
        <GeneralHistoryModal ref="generalHistoryModal" />
```

Trong `<script>`, thêm import + khai báo components (component hiện chưa có block `components`):
```js
import GeneralHistoryModal from './GeneralHistoryModal.vue'

export default {
    components: { GeneralHistoryModal },
    props: { ... }, // giữ nguyên
```

> LƯU Ý: KHÔNG đụng vào `model`/`blur`/watcher — modal chỉ đọc, không mutate model (tránh trigger watcher auto-save).

- [x] **Step 2: Verify compile + smoke** — PASS trong Task 6: nút hiện đúng, modal mở, mở/đóng modal chỉ bắn GET /histories, KHÔNG có POST tự bắn.

## Phase 3 — Verify E2E + Wrap up

### Task 6: E2E Playwright + dọn dữ liệu test

- [x] **Step 1: E2E flow chính** (login localhost:3000, JWT mint từ TpEmployee id 13 — namdangit/DNS Admin): PASS — đổi 1→2 → toast + POST 200 → modal hiện "Lập đơn đi muộn/về sớm trước (giờ): 1 (đỏ) → 2 (xanh)" + giờ + người; đổi lại → dòng đảo ngược 2→1.
  1. Mở `/timesheet/setting/general` tab Chung.
  2. Đổi "Lập đơn đăng ký trước" X giờ → blur → toast "Cập nhật thành công".
  3. Mở modal "Lịch sử thay đổi" → thấy dòng mới nhất: thời gian hôm nay, người = namdangit, nội dung `Lập đơn đi muộn/về sớm trước (giờ): <cũ> → <mới>` (cũ đỏ, mới xanh).
  4. Đổi lại giá trị cũ → mở lại modal → có thêm dòng đảo ngược.
- [x] **Step 2: Test bộ lọc**: PASS — trường khớp hiện đủ, "Nghỉ tuần" → empty-state lọc, lọc người OK, Từ ngày=mai & Đến ngày=hôm qua đều rỗng; dropdown đủ 14 trường.
- [x] **Step 3: Case không log**: PASS — 2 lần lưu mức sàn ở price-approval (POST 200 ×2) → lịch sử tab Chung không thêm dòng nào (DB + UI).
- [x] **Step 4: Dọn** — PASS: xoá 2 log test (id 5,6), count về 0 như trước test; khôi phục update_late_in_out_hour=1, profit_margin_threshold=0.00.

### Task 6b (bổ sung theo user 2026-07-10): thời gian xếp cũ → mới

- [x] Đổi `histories()` orderBy changed_at/id `desc` → `asc` (GeneralRegulationService.php) + sửa PHPDoc "(cũ nhất trước)". php -l sạch. Tinker verify: 2 dòng test 08/07 + 09/07 trả về trước các dòng 10/07 — đúng asc; đã dọn 2 dòng test, GIỮ 6 dòng log thật user tạo lúc ~11:00 10/07. FE hiển thị theo thứ tự nhận → cũ trên, mới dưới.

### Task 7: Wrap up

- [x] Đánh `[x]` các task xong trong plan này + ghi checkpoint.
- [x] Cập nhật `.plans/STATUS.md` (entry general-regulations-history → trạng thái mới).
- [x] `design.md` + spec đối chiếu với implement: khớp; 2 deviation có chủ đích do skill FE thắng brief (footer/header modal theo modal-popup, nút light theo button-convention) — không cần sửa spec (spec đã ghi "khi implement đọc skill").

---

## Phase 2 — Lịch sử 2 tab Miễn chấm công (user duyệt 2026-07-10, làm CẢ 2 tab + cho phép chèn log vào 2 hàm dùng chung Human)

Spec chi tiết: mục "Phase 2" trong docs/superpowers/specs/2026-07-10-general-regulations-history-design.md. Theo skill `.claude/skills/entity-history/SKILL.md` — biến thể ACTION log (add/remove + snapshot NV), không phải diff trường.

### Task 8: Migration + Entity `TimekeepingExemptionHistory` (kèm helper log tĩnh)

**Files:**
- Create: `hrm-api/Modules/Timesheet/Database/Migrations/2026_07_10_000002_create_timekeeping_exemption_history_table.php` (cột theo spec Phase 2; PHPDoc up/down)
- Create: `hrm-api/Modules/Timesheet/Entities/TimekeepingExemptionHistory.php` — fillable đủ cột; relation `user()` → `Modules\Human\Entities\Employee` (changed_by); static helper:

```php
    /**
     * Ghi 1 dòng lịch sử thêm/xoá NV miễn chấm công. Nuốt lỗi (try/catch)
     * để KHÔNG làm fail luồng chính (save/delete/sync phòng ban).
     *
     * @param string   $action       add|remove
     * @param int      $employeeId   employee_infos.id
     * @param int|null $typeEmployee 2=CTV, khác/null=thường
     * @param string   $source       manual|department_sync|employee_sync
     */
    public static function log($action, $employeeId, $typeEmployee, $source)
    {
        try {
            $info = \Modules\Timesheet\Entities\EmployeeInfo::find($employeeId);
            $snapshot = json_encode([
                'employee_id' => $employeeId,
                'code' => $info ? $info->code : null,
                'fullname' => $info ? $info->fullname : null,
            ], JSON_UNESCAPED_UNICODE);
            self::create([
                'employee_id' => $employeeId,
                'type_employee' => $typeEmployee,
                'action' => $action,
                'old_value' => $action === 'remove' ? $snapshot : null,
                'new_value' => $action === 'add' ? $snapshot : null,
                'source' => $source,
                'changed_by' => auth()->id(),
                'changed_at' => \Carbon\Carbon::now(),
            ]);
        } catch (\Exception $e) {
            \Illuminate\Support\Facades\Log::error($e);
        }
    }
```
(company_id để BaseModel::creating tự điền; xác nhận EmployeeInfo entity Timesheet có cột code/fullname — nếu tên khác thì chỉnh.)

- [x] Viết 2 file + php -l + migrate (bảng mới — user đã đồng ý migrate đợt này) + tinker verify log('add',...) tạo dòng đúng snapshot rồi xoá.

### Task 9: Log points Timesheet + endpoint histories

**Files:** Modify `TimekeepingExemptionService.php`, `TimekeepingExemptionController.php`, `Routes/api.php` (group timekeeping-exemptions).

- [x] `save()`: chỉ log khi thực sự `create` (nhánh `empty($entity)`) → `TimekeepingExemptionHistory::log('add', $attributes['id'], null, 'manual')` SAU khi create thành công.
- [x] `delete($id)`: `$rows = $this->model->where('employee_id', $id)->get();` trước khi delete; nếu delete trả > 0 → log `remove` cho TỪNG row với `type_employee` của row đó, source manual.
- [x] Service `histories($request)`: query `TimekeepingExemptionHistory::with('user.info')`; `$request->type === 'cooperation'` → `where('type_employee', 2)` ngược lại `where(fn: type_employee != 2 or null)`; **KHÔNG lọc company**; sort `changed_at` ASC + `id` ASC; map trả `{id, action, source, old_value, new_value, changed_by, changed_by_name (fullname ?? email ?? '—'), changed_at d/m/Y H:i:s, changed_at_raw Y-m-d}`.
- [x] Controller `histories(Request $request)` try/catch style getColumn → responseJson('success', 200, $result). Route `GET /histories` trong group (đặt trước `DELETE /{id}` cho gọn — không xung đột vì khác method).
- [x] php -l + tinker: add mới → 1 dòng add; add trùng → không log; delete → remove đúng type; histories lọc type đúng + thứ tự ASC. Dọn log test.

### Task 10: Log points module Human (2 hàm DÙNG CHUNG — CHỈ chèn log, không đổi logic)

**Files:** Modify `hrm-api/Modules/Human/Services/DepartmentService.php` (~dòng 100-122), `hrm-api/Modules/Human/Services/EmployeeInfoService.php` (~dòng 1211-1224).

- [x] DepartmentService::createDepartment nhánh cooperation_type OPERATIONS:
  - Row tồn tại + `type_employee` cũ != 2 → sau khi save: log `remove` (typeEmployee cũ, source department_sync) + log `add` (2, department_sync). Nếu đã =2 sẵn → KHÔNG log.
  - Nhánh create mới type 2 → log `add` (2, department_sync).
  - Nhánh else (bulk delete type 2): get danh sách employee_id TRƯỚC khi delete → log `remove` (2, department_sync) từng NV.
- [x] EmployeeInfoService::createTimekeepingExemption: sau create → log `add` (2, employee_sync).
- [x] php -l 2 file; diff soát kỹ KHÔNG đổi dòng logic nào ngoài chèn log; tinker verify 1 nhánh (createTimekeepingExemption với department vận hành giả lập) rồi dọn.

### Task 11: FE — modal dùng chung + nút 2 tab

**Files:**
- Create: `hrm-client/components/setting/general/TimekeepingExemptionHistoryModal.vue` — theo GeneralHistoryModal.vue + skill entity-history/modal-popup; prop `type` ('normal'|'cooperation'); id modal `timekeeping-exemption-history-modal-{type}`; fetch `apiGetMethod('timekeeping-exemptions/histories?type=' + this.type)`; render mỗi dòng: chấm xanh + `Thêm nhân viên: <code> - <fullname>` (action add, class change-new) / chấm đỏ + `Xóa nhân viên: ...` (remove, change-old) + badge nguồn (manual→"Thủ công", department_sync→"Tự động theo phòng ban NV", employee_sync→"Tự động theo hồ sơ NV"); bộ lọc: Thao tác (Thêm/Xóa) + Người thực hiện + Từ/Đến ngày.
- Modify: `hrm-client/pages/timesheet/setting/general/index.vue` — tab 2: nút "Lịch sử thay đổi" (V2BaseButton light + ri-history-line size sm) cạnh nút Thêm mới + render modal type normal.
- Modify: `hrm-client/pages/timesheet/setting/general/components/CooperationOperation.vue` — nút tương tự + modal type cooperation (đọc file trước để đặt đúng vị trí header).
- [x] Verify compile (vue-template-compiler + node --check).

### Task 12: E2E Playwright Phase 2 + dọn

- [x] Tab 2: thêm 1 NV → modal lịch sử tab 2 hiện "Thêm nhân viên..." xanh + Thủ công; xoá NV đó → dòng "Xóa nhân viên..." đỏ; add NV đã tồn tại → không thêm dòng.
- [x] Tab CTV: mở modal type cooperation → chỉ thấy log type 2 (nếu chưa có data sync thì tạo qua tinker EmployeeInfoService::createTimekeepingExemption với phòng ban vận hành, hoặc chấp nhận empty state + verify lọc type bằng tinker).
- [x] Bộ lọc thao tác/người/ngày; mở/đóng modal không bắn POST.
- [x] Dọn: xoá log test + bản ghi exemption test bằng tinker.

### Task 12b (bổ sung theo user 2026-07-10): bỏ badge nguồn + thêm mã phòng ban

- [x] BE `TimekeepingExemptionHistory::log()`: snapshot thêm `department_code` (EmployeeInfo with('department') → department.code). Cột `source` DB vẫn ghi bình thường (chỉ bỏ hiển thị). Tinker verify: new_value có `"department_code":"HN_KD2"`, đã dọn dòng test (2 log thật của user giữ nguyên).
- [x] FE modal: bỏ span badge nguồn + SOURCE_LABELS + CSS .source-badge; `formatEmployee` → "Mã NV - Tên - Mã phòng ban" (bỏ qua phần thiếu — log cũ không có department_code vẫn hiện bình thường). Compile TEMPLATE OK + SCRIPT OK, 0 reference badge còn lại.
- [x] FIX phát sinh (user báo log xoá không hiện mã phòng): API server là `php -S 127.0.0.1:8000 server.php` giữ opcache code CŨ của entity → 2 log user tạo lúc 11:55/11:57 không có department_code dù NV có phòng ban (HN_NSHC). Đã restart server (PID mới) + verify xuyên web server: POST add + DELETE NV 24 → cả 2 log đều có `"department_code":"HN_KD2"`; đã dọn 2 log test, NV 24 ra khỏi danh sách. LƯU Ý: 2 dòng log cũ (id 9, 10 — Nguyễn Chí Lợi/Kim Thị Nguyên) ghi bằng code cũ nên vĩnh viễn không có mã phòng ban trừ khi backfill.

### Task 13: Wrap up Phase 2 (plan checkpoint + STATUS.md + đối chiếu spec) — DONE 2026-07-10

---

## Phase 3 — Lịch sử tab "Chung" màn Quy định làm thêm (/timesheet/setting/overtime) (user 2026-07-10)

Mirror Phase 1 (biến thể subset-diff) sang màn overtime. Endpoint `overtime_regulations/update` chỉ dùng riêng màn này (Vuex `saveOvertimeConfig`) → không rủi ro trường lạ. Track 9 trường tab Chung = đúng danh sách `$request->only` trong `OvertimeRegulationController::update`. KHÔNG permission riêng (giống Phase 1). Màn auto-save (watcher deep model) → nút+modal không đụng model. Theo skill `.claude/skills/entity-history/SKILL.md`.

9 TRACKED_FIELDS: basis_for_calculating_overtime, minimum, minimum_time, maximum, maximum_time, have_continuous_time, continuous_time_max, continuous_time_relax, time_from. BOOLEAN: minimum, maximum, have_continuous_time.

### Task 14: Migration + Entity `OvertimeRegulationHistory`

**Files:**
- Create: `hrm-api/Modules/Timesheet/Database/Migrations/2026_07_10_000003_create_overtime_regulation_history_table.php` (bảng `overtime_regulation_history`, cột như general_regulation_history nhưng cột id entity = `overtime_regulation_id`; PHPDoc up/down).
- Create: `hrm-api/Modules/Timesheet/Entities/OvertimeRegulationHistory.php` (fillable: overtime_regulation_id, company_id, action, old_value, new_value, changed_by, changed_at; relation `user()` → Employee).

- [x] php -l + migrate (bảng `overtime_regulation_history` ĐÃ chạy 2026-07-10) + tinker verify tạo/xoá.

### Task 15: Ghi log trong `OvertimeRegulationService::save()` + `histories()`

**Files:** Modify `hrm-api/Modules/Timesheet/Services/OvertimeRegulationService.php`.

- [x] Import `OvertimeRegulationHistory`; const TRACKED_FIELDS(9)+BOOLEAN_TRACKED_FIELDS(3); save() snapshot trước/sau + logHistoryIfChanged; helper buildTrackedSnapshot/normalizeTrackedValue/logHistoryIfChanged; histories() với `with('user.info')`, scope company, sort ASC, trả changed_by_name + changed_at + changed_at_raw. php -l sạch. Tinker 6 case PASS (đổi 1 trường→1 log subset; lưu lại/boolean tương đương→không log; 2 trường→1 dòng 2 key; boolean 1→0 không rác; histories ASC + changed_by_name="DNS Admin"; dọn count=0).

### Task 16: Controller `histories()` + route

**Files:** Modify `OvertimeRegulationController.php` (thêm `use Exception; use Log;` + method histories try/catch), `Routes/api.php` group overtime_regulations (thêm `GET /histories`).

- [x] php -l sạch. Verify qua web server thật: `GET /api/v1/overtime_regulations/histories` → HTTP 200 `{code,message:success,data:[]}`.

### Task 17: FE modal `OvertimeHistoryModal.vue` + nút trên `components/setting/overtime/General.vue`

**Files:**
- Create: `hrm-client/components/setting/overtime/OvertimeHistoryModal.vue` (copy GeneralHistoryModal.vue: id `overtime-history-modal`, title "Lịch sử thay đổi quy định làm thêm", FIELD_LABELS 9 trường, BASIS_LABELS 3 phương án, BOOLEAN_FIELDS 3; fetch `overtime_regulations/histories`; bỏ note_email/HTML — overtime không có trường HTML).
- Modify: `hrm-client/components/setting/overtime/General.vue` (nút V2BaseButton light + ri-history-line ngay sau `<div class="general-st-1">`; import + register + render modal; KHÔNG đụng model/watcher).

- [x] Verify compile: vue-template-compiler template OK + node --check script OK cả 2 file.

### Task 18: E2E write-path qua web server + dọn + wrap up

- [x] E2E qua web server thật (restart `php -S` để nạp code mới; JWT TpEmployee 13): show → POST update (đổi maximum/maximum_time/time_from) → HTTP 200 → GET histories trả 1 log `{maximum:0,maximum_time:100,time_from:30}` → `{maximum:1,maximum_time:123,time_from:9}` (đúng subset 3 trường đổi, boolean 0/1, changed_by_name + giờ). Khôi phục giá trị gốc + dọn sạch bảng (histories về `data:[]`).
- [ ] (User) verify bằng mắt trên browser: `/timesheet/setting/overtime` tab Chung → nút "Lịch sử thay đổi" → đổi 1 trường → modal hiện dòng đỏ→xanh + bộ lọc. FE đã compile OK, modal mirror byte-level Phase 1 (đã Playwright-verified) chỉ khác nhãn/9 trường.

---

## Phase 4 — Lịch sử 3 mục danh sách tab Chung màn Quy định làm thêm (user 2026-07-10)

User báo 2 mục "chức vụ không được làm thêm" (chọn công ty + chức vụ theo công ty) chưa được ghi log. User chốt: track CẢ mục P3 kỹ thuật (3 mục), GỘP CHUNG vào modal "Lịch sử thay đổi" hiện có. Biến thể ACTION-LOG thêm/bớt (không diff trường). 3 endpoint store() dạng full-replace danh sách:
- `overtime_companies` (OvertimeCompanyService::store) — global, thay toàn bộ list công ty.
- `overtime_position_restrictions` (OvertimePositionRestrictionService::store) — per công ty (overtime_company_id = company_id do FE gửi thẳng), thay toàn bộ chức vụ 1 công ty.
- `p3_technical_based_on_working_position_company` (P3TechnicalBasedOnWorkingPositionService::store) — per công ty.

Ghi chung bảng `overtime_regulation_history` với action mới: `company_restriction_update` / `position_restriction_update` / `p3_position_update`; new_value = JSON `{context, added:[tên], removed:[tên]}`, old_value=null, overtime_regulation_id=0 (không gắn 1 bản ghi cụ thể). company_id do BaseModel tự điền (bỏ qua khi query list-action). histories() scope: `(action='update' AND company_id=current) OR action!='update'` (field-diff theo công ty, list-action global).

### Task 19: BE — helper log + 3 điểm store + histories()

**Files:** Modify `OvertimeRegulationHistory.php` (static `logListChange`), `OvertimeRegulationService.php` (histories partition), `OvertimeCompanyService.php`, `OvertimePositionRestrictionService.php`, `P3TechnicalBasedOnWorkingPositionService.php` (diff old/new trong store + resolve tên Company/WorkingPosition + log).

- [x] php -l 5 file sạch. Tinker verify PASS: OC no-op→0 log; thêm/bớt công ty→company_restriction_update (context null, added/removed tên công ty); thêm/bớt chức vụ→position_restriction_update (context=tên công ty, added/removed tên CV); P3→p3_position_update tương tự; histories() partition trả cả field 'update' (theo công ty) + 3 loại list-action (global) đúng ASC. Config khôi phục nguyên vẹn, đã dọn 6 log test (giữ log field thật).

### Task 20: FE — modal render list-action

**Files:** Modify `hrm-client/components/setting/overtime/OvertimeHistoryModal.vue` (parseHistoryItem branch theo action: 'update'→field diff cũ; list-action→title + context + added xanh "Thêm"/removed đỏ "Bỏ"). Thêm nhãn LIST_TITLES.

- [x] parseHistoryItem branch kind field/list; template render 2 dạng (field: cũ→mới; list: Thêm xanh/Bỏ đỏ + context tên công ty). Verify compile: vue-template-compiler + node --check OK. (Web server đã restart nạp code Phase 4 cho browser.)
- [x] REDESIGN hiển thị (user 2026-07-10 báo output cũ khó hiểu — thực chất browser chạy JS cũ trước Task 20): gộp mỗi loại 1 dòng "Thêm N chức vụ: A, B" (xanh) / "Bỏ N chức vụ: C, D" (đỏ) với icon; tiêu đề rõ (LIST_META title+unit); chip công ty (ri-building-2-line) thay cho "— tên"; chấm màu theo thao tác (chỉ thêm→xanh/chỉ bỏ→đỏ/cả hai→amber); "Người thực hiện: …". Compile lại OK. USER CẦN HARD-REFRESH để nạp JS mới.

## Phase 5 — Lịch sử tab "Khung giờ làm thêm" (CRUD overtime_hours) (user 2026-07-10)

Entity `overtime_hours` (6 trường: type 1/2/3, start_at, end_at, weekday_ratio, dayoff_ratio, holiday_ratio), CRUD create/update/delete per công ty → biến thể FULL-SNAPSHOT (create/update/delete như employee_history). Bảng riêng `overtime_hour_history`, nút + modal RIÊNG trên tab "Khung giờ làm thêm" (không gộp modal tab Chung). KHÔNG permission riêng.

### Task 21: BE — migration + entity + log CRUD + histories + route
**Files:** Create migration `2026_07_10_000004_create_overtime_hour_history_table.php` + entity `OvertimeHourHistory.php` (static `log()` try/catch — QUAN TRỌNG: store() nằm trong DB::transaction, log lỗi không được rollback save thật). Modify `OvertimeHourService.php` (buildSnapshot + log create/update/delete + histories ASC), `OvertimeHourController.php` (+histories), `Routes/api.php` (GET /timesheet/overtime-hour/histories ĐẶT TRƯỚC /{id} tránh nuốt route).
- [x] php -l 4 file sạch. Migration `2026_07_10_000004_create_overtime_hour_history_table` ĐÃ CHẠY. Route GET histories đặt trước /{id}. Tinker verify PASS: create→snapshot đầy đủ; update→old+new (no-op không log); delete→old+new NULL; histories count=3 ASC đúng format. Dọn sạch (row test đã xóa qua delete).

### Task 22: FE — modal + nút trên tab Khung giờ
**Files:** Create `hrm-client/components/setting/overtime/OvertimeHourHistoryModal.vue` (create=xanh liệt kê snapshot; update=amber diff cũ→mới; delete=đỏ liệt kê snapshot; TYPE_LABELS + nhãn 6 trường; bộ lọc Thao tác/Người/ngày). Modify `pages/timesheet/setting/overtime/index.vue` (nút light+ri-history-line cạnh "Thêm mới" tab 2 + render modal).
- [x] Verify compile (vue-template-compiler + node --check 2 file OK). Route + histories qua web server 200. Web server đã restart nạp code Phase 5.

### Checkpoint Phase 5 — 2026-07-10
Vừa hoàn thành: Task 21→22 (inline Opus). Lịch sử CRUD tab "Khung giờ làm thêm" (entity overtime_hours) — biến thể full-snapshot create/update/delete. Bảng riêng `overtime_hour_history` (migrated), helper static `OvertimeHourHistory::log()` try/catch (an toàn trong DB::transaction của store). Service log 3 action + histories() ASC theo công ty. Nút+modal RIÊNG trên tab Khung giờ (OvertimeHourHistoryModal: Thêm xanh liệt kê / Sửa amber diff / Xóa đỏ liệt kê). Verify tinker CRUD PASS + route web 200 + FE compile sạch; dọn sạch data test. Web server restart.
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh browser → tab Khung giờ làm thêm → thêm/sửa/xóa 1 khung giờ → nút "Lịch sử thay đổi".
Blocked: (không)

---

### Checkpoint Phase 4 — 2026-07-10
Vừa hoàn thành: Task 19→20 (inline Opus). Log 3 danh sách (công ty áp dụng / chức vụ cấm làm thêm / P3 kỹ thuật) dạng action-log thêm/bớt, gộp chung modal + endpoint `overtime_regulations/histories`. Helper `OvertimeRegulationHistory::logListChange` (try/catch \Throwable, overtime_regulation_id=0, action mới). 3 service store() thêm diff old/new + resolve tên Company/WorkingPosition. histories() partition field-diff(theo công ty) + list-action(global). FE modal render 2 dạng. Verify tinker 3 danh sách + partition PASS; config khôi phục nguyên; FE compile sạch; dọn log test (giữ 2 log field thật user tạo lúc test browser). Web server đã restart.
Đang làm dở: (không)
Bước tiếp theo: user verify browser — đổi công ty/chức vụ/P3 ở tab Chung màn overtime → nút "Lịch sử thay đổi" thấy dòng Thêm/Bỏ.
Blocked: (không)

---

### Checkpoint Phase 3 — 2026-07-10
Vừa hoàn thành: Task 14→18 (inline, model Opus 4.8 theo user đổi). Mirror Phase 1 subset-diff sang màn Quy định làm thêm. Migration `2026_07_10_000003_create_overtime_regulation_history_table` ĐÃ CHẠY. BE verify tinker 6 case PASS + E2E write-path qua web server thật PASS (POST update→GET histories đúng diff 3 trường + boolean 0/1 + người + giờ). FE compile sạch (template + script). Đã dọn sạch data test (bảng history rỗng, entity khôi phục giá trị gốc). Đã restart API server `php -S` nạp code mới (route/controller/service overtime histories đã hoạt động qua web).
Đang làm dở: (không)
Bước tiếp theo: user verify bằng mắt trên browser tab Chung màn overtime.
Blocked: (không)

---

### Checkpoint Phase 2 — 2026-07-10
Vừa hoàn thành: Task 8→13 (subagent-driven Fable). Migration 2026_07_10_000002 ĐÃ CHẠY. E2E Playwright 7/7 PASS (add/remove log đúng màu + badge nguồn, add trùng không log, partition CTV/thường đúng, bộ lọc, không POST tự phát, dọn sạch). Final review READY; đã áp fix-now: `catch (\Throwable)` trong TimekeepingExemptionHistory::log (thay \Exception).
Đang làm dở: (không)
Bước tiếp theo: user verify bằng mắt 2 tab + QUYẾT ĐỊNH phát sinh bên dưới.
Blocked: (không)

**Phát sinh chờ user quyết (final review Phase 2):**
1. ⚠️ Điểm mutation thứ 5 CHƯA log: hook `EmployeeInfo::updated` (Modules/Human/Entities/EmployeeInfo.php:161-176) tự XOÁ toàn bộ timekeeping_exemptions khi NV chuyển khỏi phòng ban vận hành → lịch sử có thể có "Thêm" không có "Xóa" tương ứng. Muốn log đủ phải chèn vào model hook của EmployeeInfo (entity nhạy cảm — save() đồng bộ ERP) → CHỜ user đồng ý mới làm.
2. (chấp nhận ship) helper log() bỏ tham số companyId → cột company_id bảng history luôn NULL (endpoint cố ý không lọc company nên không ảnh hưởng); log add ghi type_employee=NULL còn remove ghi 0 (cùng partition normal, hiển thị đúng).

---

### Checkpoint — 2026-07-10 (2)
Vừa hoàn thành: Task 1→7 (subagent-driven, mỗi task 1 implementer + 1 reviewer, final whole-feature review READY). Migration ĐÃ CHẠY (user đồng ý). E2E Playwright PASS toàn bộ (flow chính, bộ lọc, case không log từ price-approval, dọn data + khôi phục giá trị).
Đang làm dở: (không)
Bước tiếp theo: user verify bằng mắt trên browser (`localhost:3000/timesheet/setting/general` tab Chung → nút "Lịch sử thay đổi").
Blocked: (không)

**Ghi chú tồn đọng (ship-as-is, đã triage ở final review):**
- History insert trong save() không bọc try/catch — giống pattern EmployeeService gốc; nếu muốn hardening thì sửa cả 2 nơi sau.
- BaseModel (spatie LogsActivity) ghi kèm activity_log cho mỗi dòng history — hành vi có sẵn toàn project.
- ⚠️ LỖI CÓ SẴN không thuộc feature: `php artisan route:list` crash do `Modules/Decision/Routes/web.php:17` trỏ `DecisionController` thiếu namespace `V1` — cần báo team Decision.
