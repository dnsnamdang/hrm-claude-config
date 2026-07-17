# Plan — assign-settings-history (Lịch sử thay đổi tab Thông tin chung, /assign/settings)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Đánh `[x]` khi xong.

Người phụ trách: @khoipv
Spec đầy đủ: `docs/superpowers/specs/2026-07-16-assign-settings-history-design.md` (ĐỌC TRƯỚC KHI CODE — chứa quyết định đã chốt, whitelist, edge case)

**Goal:** Nút "Lịch sử thay đổi" + modal timeline trên tab Thông tin chung màn Cấu hình phân hệ Giao việc, ghi log subset-diff (scalar + 3 danh sách) vào bảng `assign_config_history`.

**Architecture:** Log ghi trong `AssignConfigService::create()` bằng diff trạng thái DB trước/sau (mẫu `GeneralRegulationService::logHistoryIfChanged`), 3 danh sách coi như 3 "trường" (mảng chuẩn hoá + sort, tên chức vụ denormalize). Endpoint đọc `GET assign/configs/histories?company_id=`. FE copy mẫu `HumanSettingHistoryModal.vue`.

## Global Constraints

- PHP 7.4 — KHÔNG dùng `?->`. JSON luôn `JSON_UNESCAPED_UNICODE`.
- KHÔNG commit/push git. Migration CHỜ user đồng ý mới chạy (targeted `--path`).
- Khối log bọc `try/catch (\Throwable $e) { Log::error($e); }` — đang trong `DB::transaction` của controller, không bao giờ fail luồng lưu.
- KHÔNG đổi hành vi lưu hiện có của `create()` (kể cả bug `technical_room_double` — chỉ báo, không sửa).
- KHÔNG track: `km_support_stay_cost`, `km_support_regulation_cost`, `places_origin` (tab 2).
- Không permission riêng; route trong group `auth:api` sẵn có.

---

## Phase 1 — BE

### T1. Migration bảng `assign_config_history`

- [x] File mới `hrm-api/Modules/Assign/Database/Migrations/2026_07_16_000001_create_assign_config_history_table.php` — PHPDoc trên `up()`/`down()` theo mẫu `2026_07_14_000013_create_working_shift_history_table.php`:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateAssignConfigHistoryTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('assign_config_history', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('assign_config_id')->index()->comment('Cấu hình phân hệ giao việc');
            $table->unsignedBigInteger('company_id')->nullable()->index()->comment('Công ty (scope khi liệt kê)');
            $table->string('action')->comment('Loại thao tác: update');
            $table->text('old_value')->nullable()->comment('JSON chỉ gồm trường thay đổi — giá trị cũ');
            $table->text('new_value')->nullable()->comment('JSON chỉ gồm trường thay đổi — giá trị mới');
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
        Schema::dropIfExists('assign_config_history');
    }
}
```

- [x] `php -l` file. CHƯA migrate (chờ user đồng ý ở T10).

### T2. Entity `AssignConfigHistory`

- [x] File mới `hrm-api/Modules/Assign/Entities/AssignConfigHistory.php`:

```php
<?php

namespace Modules\Assign\Entities;

use App\Models\BaseModel;
use Modules\Human\Entities\Employee;

class AssignConfigHistory extends BaseModel
{
    protected $table = 'assign_config_history';

    protected $fillable = [
        'assign_config_id',
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

### T3. Service — hằng + normalize + snapshot

**Files:** Modify `hrm-api/Modules/Assign/Services/AssignConfigService.php`
**Interfaces (Produces):** `buildTrackedSnapshot(?AssignConfig $config): array` — mảng 26 key (23 scalar + `time_slots` + `working_positions_overtime_support` + `working_positions_always_full_time`); `normalizeTrackedValue($field, $value)`.

- [x] Thêm `use Modules\Assign\Entities\AssignConfigHistory;` + hằng (sau `protected $_model;`):

```php
    /** 23 trường scalar tab "Thông tin chung" được track lịch sử (KHÔNG gồm km_support_*, places_origin — tab 2) */
    const TRACKED_FIELDS = [
        'work_warranty', 'work_repair', 'work_installation', 'work_other',
        'cost_business_trip_support', 'cost_stay_support', 'unit_price_work',
        'cost_overtime_support', 'cost_stay_overtime_support',
        'cost_regulation_support', 'cost_regulation_other_support',
        'assignment_extend_time', 'assignment_extend_days',
        'technical_overseas_fee', 'technical_room_single', 'technical_room_double', 'technical_room_triple',
        'other_overseas_fee', 'other_room_single', 'other_room_double', 'other_room_triple',
        'is_all_working_positions_overtime_support', 'is_all_working_positions_always_full_time',
    ];

    const BOOLEAN_TRACKED_FIELDS = [
        'is_all_working_positions_overtime_support',
        'is_all_working_positions_always_full_time',
    ];

    /** 3 danh sách track như "trường": so sánh bằng json_encode mảng đã chuẩn hoá + sort */
    const LIST_TRACKED_KEYS = [
        'time_slots',
        'working_positions_overtime_support',
        'working_positions_always_full_time',
    ];
```

- [x] Method `normalizeTrackedValue` (copy `GeneralRegulationService::normalizeTrackedValue` + special-case time):

```php
    /**
     * Chuẩn hoá giá trị để so sánh/lưu log: rỗng → null, boolean → 0/1,
     * assignment_extend_time → 'H:i', numeric → số (int nếu tròn), còn lại → string.
     * Tránh log rác kiểu "5" → 5 hay "08:00" → "08:00:00".
     */
    private function normalizeTrackedValue($field, $value)
    {
        if ($value === null || $value === '') {
            return null;
        }
        if (in_array($field, self::BOOLEAN_TRACKED_FIELDS, true)) {
            return filter_var($value, FILTER_VALIDATE_BOOLEAN) ? 1 : 0;
        }
        if ($field === 'assignment_extend_time') {
            return substr(trim((string) $value), 0, 5);
        }
        if (is_numeric($value)) {
            $number = (float) $value;
            return $number == (int) $number ? (int) $number : $number;
        }
        return (string) $value;
    }
```

- [x] Method `buildTrackedSnapshot` — đọc từ DB, `$config` null (công ty chưa có record) → scalar null + list rỗng. Time slot convert timezone Y HỆT `index()` (`Carbon::parse(...)->tz(config('app.timezone'))->format('H:i')`). Tên chức vụ join `working_positions` tại thời điểm log, chức vụ đã mất → `'#'.working_position_id`:

```php
    /**
     * Chụp snapshot 23 trường scalar + 3 danh sách (khung giờ, 2 DS chức vụ) từ DB.
     * Dùng để diff trước/sau khi lưu — $config null nghĩa là công ty chưa có cấu hình.
     */
    private function buildTrackedSnapshot($config)
    {
        $snapshot = [];
        foreach (self::TRACKED_FIELDS as $field) {
            $snapshot[$field] = $config ? $this->normalizeTrackedValue($field, $config->getAttribute($field)) : null;
        }
        $snapshot['time_slots'] = [];
        $snapshot['working_positions_overtime_support'] = [];
        $snapshot['working_positions_always_full_time'] = [];
        if (!$config) {
            return $snapshot;
        }

        $slots = [];
        $rows = DB::table('assign_config_time_slots')
            ->where('assign_config_id', $config->id)
            ->select('time_slot', 'work')
            ->get();
        foreach ($rows as $row) {
            $work = $row->work;
            if (is_numeric($work)) {
                $number = (float) $work;
                $work = $number == (int) $number ? (int) $number : $number;
            }
            $slots[] = [
                'time_slot' => $row->time_slot ? Carbon::parse($row->time_slot)->tz(config('app.timezone'))->format('H:i') : null,
                'work' => $work,
            ];
        }
        usort($slots, function ($a, $b) {
            return [$a['time_slot'], $a['work']] <=> [$b['time_slot'], $b['work']];
        });
        $snapshot['time_slots'] = $slots;

        $positions = DB::table('assign_config_working_positions')
            ->leftJoin('working_positions', 'working_positions.id', '=', 'assign_config_working_positions.working_position_id')
            ->where('assign_config_working_positions.assign_config_id', $config->id)
            ->orderBy('assign_config_working_positions.working_position_id')
            ->select('assign_config_working_positions.type', 'assign_config_working_positions.working_position_id', 'working_positions.name')
            ->get();
        foreach ($positions as $position) {
            $item = [
                'id' => (int) $position->working_position_id,
                'name' => $position->name !== null ? $position->name : '#' . $position->working_position_id,
            ];
            if ((int) $position->type === AssignConfig::TYPE_WORKING_POSITIONS_OVERTIME_SUPPORT) {
                $snapshot['working_positions_overtime_support'][] = $item;
            } elseif ((int) $position->type === AssignConfig::TYPE_WORKING_POSITIONS_ALWAYS_FULL_TIME) {
                $snapshot['working_positions_always_full_time'][] = $item;
            }
        }

        return $snapshot;
    }
```

- [x] `php -l`.

### T4. Service — diff + ghi log, hook vào `create()`

**Interfaces (Produces):** `logHistoryIfChanged(AssignConfig $config, array $oldSnapshot, array $newSnapshot): void`.

- [x] Method diff + insert (1 dòng log N key, key order theo thứ tự whitelist):

```php
    /**
     * So sánh snapshot trước/sau khi lưu, có trường thay đổi thì ghi 1 dòng lịch sử
     * (old/new = JSON chỉ gồm các trường đổi; danh sách lưu cả mảng cũ + mới).
     * Không đổi gì → không ghi.
     */
    private function logHistoryIfChanged($config, array $oldSnapshot, array $newSnapshot)
    {
        $oldChanged = [];
        $newChanged = [];
        foreach (self::TRACKED_FIELDS as $field) {
            if ($oldSnapshot[$field] !== $newSnapshot[$field]) {
                $oldChanged[$field] = $oldSnapshot[$field];
                $newChanged[$field] = $newSnapshot[$field];
            }
        }
        foreach (self::LIST_TRACKED_KEYS as $key) {
            if (json_encode($oldSnapshot[$key]) !== json_encode($newSnapshot[$key])) {
                $oldChanged[$key] = $oldSnapshot[$key];
                $newChanged[$key] = $newSnapshot[$key];
            }
        }
        if (empty($newChanged)) {
            return;
        }
        AssignConfigHistory::create([
            'assign_config_id' => $config->id,
            'company_id' => $config->company_id,
            'action' => 'update',
            'old_value' => json_encode($oldChanged, JSON_UNESCAPED_UNICODE),
            'new_value' => json_encode($newChanged, JSON_UNESCAPED_UNICODE),
            'changed_by' => Auth::id(),
            'changed_at' => Carbon::now(),
        ]);
    }
```

- [x] Hook vào `create()` — CHỈ thêm 2 khối, không đụng logic giữa:
  - Đầu hàm (trước `if (AssignConfig::query()->...exists())`):

```php
        // Lịch sử thay đổi: chụp snapshot TRƯỚC mọi mutation (null-safe, không bao giờ fail luồng lưu)
        $oldSnapshot = null;
        try {
            $oldConfigForHistory = AssignConfig::query()->where('company_id', $attributes['company_id'])->first();
            $oldSnapshot = $this->buildTrackedSnapshot($oldConfigForHistory);
        } catch (\Throwable $e) {
            Log::error($e);
        }
```

  - Cuối hàm, SAU `$this->refreshAssignRequestsExtendConfig($assignConfig);` và TRƯỚC `return $assignConfig;`:

```php
        try {
            if ($oldSnapshot !== null) {
                $newSnapshot = $this->buildTrackedSnapshot(AssignConfig::query()->find($assignConfig->id));
                $this->logHistoryIfChanged($assignConfig, $oldSnapshot, $newSnapshot);
            }
        } catch (\Throwable $e) {
            Log::error($e);
        }
```

- [x] `php -l`.

### T5. Service — `histories()` (mẫu `HumanSettingHistoryService::histories`)

**Interfaces (Produces):** mảng `[{id, action, old_value, new_value, changed_by, changed_by_name, changed_at 'd/m/Y H:i:s', changed_at_raw 'Y-m-d'}]` sort cũ→mới.

- [x] Thêm method public:

```php
    /**
     * Lịch sử thay đổi tab Thông tin chung màn Cấu hình phân hệ giao việc,
     * scope theo company_id truyền lên (FE gửi current_company), sắp xếp cũ nhất trước.
     */
    public function histories($companyId)
    {
        $logs = AssignConfigHistory::with('user.info')
            ->where('company_id', $companyId)
            ->orderBy('changed_at', 'asc')
            ->orderBy('id', 'asc')
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

### T6. Controller + route

- [x] `AssignConfigController` thêm method (try/catch + `responseJson` như `store()`):

```php
    /**
     * API lịch sử thay đổi tab Thông tin chung
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function histories(Request $request)
    {
        try {
            $data = $this->assignConfigService->histories($request->company_id);

            return $this->responseJson('success', Response::HTTP_OK, $data);
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
```

- [x] `Modules/Assign/Routes/api.php` group `'/assign/configs'` (dòng ~732) — thêm `GET /histories` **TRƯỚC** `GET /{companyId}` (không thì bị nuốt):

```php
    Route::group(['prefix' => '/assign/configs'], function () {
        Route::get('/histories', [AssignConfigController::class, 'histories']);
        Route::get('/{companyId}', [AssignConfigController::class, 'index']);
        Route::post('/', [AssignConfigController::class, 'store']);
    });
```

- [x] `php -l` cả 2 file. Verify route không bị nuốt: gọi `GET /v1/assign/configs/histories?company_id=1` (kèm token) → JSON `{message:'success', data:[...]}`, KHÔNG phải AssignConfigDetailResource.

## Phase 2 — FE

### T7. Modal `AssignConfigHistoryModal.vue`

- [x] File mới `hrm-client/pages/assign/settings/components/AssignConfigHistoryModal.vue` — **copy mẫu `hrm-client/pages/human/settings/components/HumanSettingHistoryModal.vue`** (đọc file mẫu TRƯỚC khi viết; tuân skill `modal-popup`: hide-footer, header icon tròn `ri-history-line` + nút X, footer chỉ nút Đóng tertiary; bộ lọc + timeline giữ nguyên cấu trúc). Khác biệt so với mẫu:
  - Modal id `assign-config-history-modal`, title "Lịch sử thay đổi — Cấu hình phân hệ giao việc".
  - `open()` → fetch `apiGetMethod` URL `` `assign/configs/histories?company_id=${this.$store.state.current_company}` `` (response `responseJson` → `data.data`).
  - Chỉ 1 action `update` → BỎ nhánh insurance/rowLabel của mẫu; mỗi log = 1 khối timeline, dot 1 màu amber.
  - Const nhãn (khớp 100% key BE — 23 scalar + 3 list):

```js
const FIELD_LABELS = {
    work_warranty: 'Hệ số công HC tối đa — Bảo hành',
    work_repair: 'Hệ số công HC tối đa — Sửa chữa - bảo dưỡng',
    work_installation: 'Hệ số công HC tối đa — Lắp đặt',
    work_other: 'Hệ số công HC tối đa — Khác',
    cost_business_trip_support: 'Hỗ trợ công tác phí - kỹ thuật',
    cost_stay_support: 'Hỗ trợ lưu trú - kỹ thuật',
    unit_price_work: 'Đơn giá công khoán',
    cost_overtime_support: 'Hỗ trợ công tác phí (vượt công định mức)',
    cost_stay_overtime_support: 'Hỗ trợ lưu trú (vượt công định mức)',
    cost_regulation_support: 'Hỗ trợ công tác phí - PTC khác (Xe công ty)',
    cost_regulation_other_support: 'Hỗ trợ công tác phí - PCT khác (Xe ngoài)',
    assignment_extend_time: 'Gia hạn phiếu giao công tác — Số giờ',
    assignment_extend_days: 'Gia hạn phiếu giao công tác — Số ngày',
    technical_overseas_fee: 'Phiếu CT kỹ thuật — Công tác phí nước ngoài',
    technical_room_single: 'Phiếu CT kỹ thuật — Phòng tiêu chuẩn',
    technical_room_double: 'Phiếu CT kỹ thuật — Phòng tại khu du lịch',
    technical_room_triple: 'Phiếu CT kỹ thuật — Phòng ba',
    other_overseas_fee: 'Phiếu CT khác — Công tác phí nước ngoài',
    other_room_single: 'Phiếu CT khác — Phòng tiêu chuẩn',
    other_room_double: 'Phiếu CT khác — Phòng tại khu du lịch',
    other_room_triple: 'Phiếu CT khác — Phòng ba',
    is_all_working_positions_overtime_support: 'Tất cả chức vụ được tính PCT kỹ thuật',
    is_all_working_positions_always_full_time: 'Tất cả chức vụ luôn đủ công hành chính',
    time_slots: 'Khung giờ tính ngày xuất phát',
    working_positions_overtime_support: 'Chức vụ được tính PCT kỹ thuật',
    working_positions_always_full_time: 'Chức vụ luôn được tính đủ công hành chính',
}
const MONEY_FIELDS = [
    'cost_business_trip_support', 'cost_stay_support', 'unit_price_work',
    'cost_overtime_support', 'cost_stay_overtime_support',
    'cost_regulation_support', 'cost_regulation_other_support',
    'technical_overseas_fee', 'technical_room_single', 'technical_room_double', 'technical_room_triple',
    'other_overseas_fee', 'other_room_single', 'other_room_double', 'other_room_triple',
]
const BOOLEAN_FIELDS = ['is_all_working_positions_overtime_support', 'is_all_working_positions_always_full_time']
const LIST_FIELDS = ['time_slots', 'working_positions_overtime_support', 'working_positions_always_full_time']
```

  - `parseHistoryItem(item)`: JSON.parse old/new; mỗi key trong new_value:
    - key scalar → `{type: 'diff', field: FIELD_LABELS[key], old: formatValue(key, oldObj[key]), new: formatValue(key, newObj[key])}` — render **cũ ĐỎ `.change-old` #dc2626 → mới XANH `.change-new` #16a34a**.
    - key thuộc `LIST_FIELDS` → diff FE thành chip:

```js
listItemKey(field, item) {
    return field === 'time_slots' ? `${item.time_slot}|${item.work}` : String(item.id)
},
listItemLabel(field, item) {
    return field === 'time_slots' ? `Trước ${item.time_slot}h — ${item.work} công` : item.name
},
buildListChange(field, oldArr, newArr) {
    const oldList = oldArr || []
    const newList = newArr || []
    const oldKeys = oldList.map((i) => this.listItemKey(field, i))
    const newKeys = newList.map((i) => this.listItemKey(field, i))
    return {
        type: 'list',
        field: FIELD_LABELS[field],
        added: newList.filter((i) => !oldKeys.includes(this.listItemKey(field, i))).map((i) => this.listItemLabel(field, i)),
        removed: oldList.filter((i) => !newKeys.includes(this.listItemKey(field, i))).map((i) => this.listItemLabel(field, i)),
    }
},
```

    Template render `type === 'list'`: chip **thêm = XANH** (badge nền #dcfce7 chữ #16a34a, prefix `+`), **bớt = ĐỎ** (nền #fee2e2 chữ #dc2626, prefix `−`); phần tử giữ nguyên không hiển thị.
  - `formatValue(key, val)`: null/rỗng → `(trống)`; BOOLEAN_FIELDS → `Có`/`Không` (giá trị 1/0); MONEY_FIELDS → phân tách nghìn `Number(val).toLocaleString('vi-VN')`; còn lại String.
  - Bộ lọc client-side giữ nguyên mẫu: Trường (options từ FIELD_LABELS — với dòng có nhiều key thì match nếu CHỨA key) / Người thực hiện (gom distinct từ data, value = `changed_by`) / Từ ngày / Đến ngày (so `changed_at_raw`); nút Tìm kiếm primary + Làm mới tertiary theo skill `button-convention`. Empty state khi 0 log.
  - Modal tự chứa state, KHÔNG thêm Vuex action, KHÔNG đụng `form` của page.

### T8. Nút mở modal trên tab Thông tin chung

- [x] `hrm-client/pages/assign/settings/index.vue` — ĐỌC skill `button-convention` trước. Sửa khối nút cuối tab Thông tin chung (dòng ~586-592, khối `dataTables_filter text-md-right`): thêm nút lịch sử BÊN TRÁI nút Lưu (giữ nguyên `b-button` Lưu cũ):

```html
<div id="tickets-table_filter" class="dataTables_filter text-md-right mt-2">
    <V2BaseButton light size="sm" class="mr-2" @click="$refs.assignConfigHistoryModal.open()">
        <template #prefix><i class="ri-history-line"></i></template>
        Lịch sử thay đổi
    </V2BaseButton>
    <b-button @click="submitSave()" variant="success">
        <i class="fas fa-save"></i> Lưu
    </b-button>
</div>
```

- [x] Cuối template tab (cạnh `<add-time-slot-modal>`): `<assign-config-history-modal ref="assignConfigHistoryModal"></assign-config-history-modal>`; import + đăng ký component `AssignConfigHistoryModal from './components/AssignConfigHistoryModal.vue'` (`V2BaseButton` đã import sẵn).
- [x] Compile check: `npx vue-template-compiler` hoặc chờ dev server — không lỗi template.

## Phase 3 — Verify (spec mục 7)

### T9. php -l + migrate

- [ ] `php -l` toàn bộ file BE sửa/mới (migration, entity, service, controller, routes).
- [x] **HỎI user đồng ý** (ĐÃ migrate 2026-07-16, 565ms) → `php artisan migrate --path=Modules/Assign/Database/Migrations/2026_07_16_000001_create_assign_config_history_table.php` (targeted — không đụng migration pending khác). Verify bảng tồn tại.

### T10. Tinker round-trip THẬT

Ghi `$maxId = AssignConfigHistory::max('id') ?? 0` TRƯỚC test; chụp config gốc của công ty test để khôi phục; dọn bằng `where('id','>',$maxId)->delete()`. KHÔNG đụng `EmployeeInfo::save()`. Gọi qua `app(AssignConfigService::class)->create([...])` với `Auth::setUser` user thật:

- [x] (a) Đổi 1 scalar (`work_warranty`) → 1 log, old/new đúng subset 1 key.
- [x] (b) Lưu lại y nguyên (no-op) → 0 log mới.
- [x] (c) Đổi CHỈ `km_support_stay_cost` + `places_origin` → 0 log (ngoài whitelist).
- [x] (d) Boolean: gửi `is_all_... = true` khi DB đang `1` → 0 log; `assignment_extend_time` gửi `'08:00'` khi DB `'08:00:00'` → 0 log (không log rác).
- [x] (e) Đổi `time_slots` (thêm 1 + bớt 1) → 1 log, old/new = mảng `[{time_slot 'H:i', work}]` đúng; request KHÔNG có key `time_slots` → không diff key đó.
- [x] (f) Đổi DS chức vụ → old/new = `[{id, name}]` tên đúng từ `working_positions`; tick "Tất cả" (is_all=1 + ids=[]) → log 2 key (is_all + list bớt).
- [x] (g) Công ty CHƯA có record (chọn company test chưa cấu hình) → first save → 1 log old toàn null/[]; XÓA record + time_slots/positions con của company test sau đó.
- [x] (h) Đổi 2 scalar 1 lần lưu → 1 dòng 2 key, key order theo whitelist.
- [x] (i) `histories($companyId)` → đúng format, sort cũ→mới, `changed_by_name` đúng.
- [x] Dọn: log test = 0 dòng mới, config công ty test khôi phục nguyên trạng (so sánh lại snapshot).

### T11. Route + regression an toàn

- [x] HTTP thật (token user thật): `GET /v1/assign/configs/histories?company_id=<id>` → 200 JSON data mảng; `GET /v1/assign/configs/<companyId>` vẫn trả resource config bình thường (route không bị nuốt/nuốt nhầm).
- [x] Regression try/catch: tinker `Schema::rename('assign_config_history', 'assign_config_history_bak')` → gọi `create()` lưu config → vẫn thành công + `laravel.log` có dòng error → rename lại. (Log BE ở `hrm-api/storage/logs/laravel.log` — LOG_CHANNEL=single.)

### T12. Playwright E2E

Lưu ý [[playwright-phantom-writes]]: chỉ thao tác đúng màn `/assign/settings`, sau test check log lạ + khôi phục giá trị.

- [x] Login → `/assign/settings` tab Thông tin chung → thấy nút "Lịch sử thay đổi" bên trái nút Lưu.
- [x] Mở modal → network CHỈ GET histories (không POST) → empty state hoặc list log.
- [x] Đổi 1 trường (vd `work_warranty` 1.5→2) + bấm Lưu → mở modal → dòng mới: nhãn "Hệ số công HC tối đa — Bảo hành", cũ đỏ 1.5 → mới xanh 2, đúng người + giờ.
- [x] Đổi khung giờ / chức vụ → modal render chip thêm xanh/bớt đỏ.
- [x] Bộ lọc 4 loại (Trường/Người/Từ/Đến) hoạt động; nút Làm mới reset.
- [x] Khôi phục giá trị như trước test (qua UI hoặc tinker query builder) + dọn log test bằng tinker (`where('id','>',$maxId)->delete()`) → bảng history về đúng trạng thái trước test.

### Checkpoint — 2026-07-16 (subagent-driven, Fable 5)
Vừa hoàn thành: TOÀN BỘ T1-T12 — CODE DONE + MIGRATED + VERIFIED. 4 nhóm code (A: migration+entity / B: service+controller+route / C: modal FE / D: nút) mỗi nhóm review riêng đều PASS; tinker round-trip 11/11 PASS (data khôi phục nguyên trạng, log test = 0); Playwright UI 7/7 PASS (network sạch, không phantom write); final whole-branch review verdict READY (0 finding bắt buộc, các Minor đều accepted — chi tiết trong final review: company_id query param = accepted risk nhất quán endpoint index có sẵn).
Đang làm dở: (không)
Bước tiếp theo: user verify browser bằng mắt → quyết định commit (2 repo đang uncommitted trên branch feature-10455, chưa git theo quy tắc).
Blocked: (không)

---

## Phase 4 — Mở rộng tab "Giới hạn khoảng cách tính công tác phí" (2026-07-16, user duyệt — spec mục 9)

Không migration mới. Nút riêng từng tab, modal scope theo tab.

### T13. BE — track thêm 2 km + places_origin

- [x] `AssignConfigService.php`: `TRACKED_FIELDS` thêm 2 key CUỐI mảng: `'km_support_stay_cost', 'km_support_regulation_cost'`. `LIST_TRACKED_KEYS` thêm `'places_origin'`. Sửa comment const TRACKED_FIELDS (bỏ ghi chú "KHÔNG gồm km_support_*, places_origin").
- [x] `buildTrackedSnapshot()`: khởi tạo `$snapshot['places_origin'] = [];` cùng chỗ 3 list cũ; sau khối positions thêm:

```php
        $placeItems = [];
        $places = DB::table('assign_config_place_origins')
            ->where('assign_config_id', $config->id)
            ->select('name', 'place_lat', 'place_lng')
            ->get();
        foreach ($places as $place) {
            $placeItems[] = [
                'name' => ($place->name !== null && $place->name !== '') ? (string) $place->name : null,
                'lat' => $this->normalizeTrackedValue('place_lat', $place->place_lat),
                'lng' => $this->normalizeTrackedValue('place_lng', $place->place_lng),
            ];
        }
        usort($placeItems, function ($a, $b) {
            return [$a['name'], $a['lat'], $a['lng']] <=> [$b['name'], $b['lat'], $b['lng']];
        });
        $snapshot['places_origin'] = $placeItems;
```

  (Cột `place` địa chỉ text KHÔNG track. `place_lat`/`place_lng` không thuộc BOOLEAN/extend_time → normalize numeric sẵn có.) `php -l`.

### T14. FE — modal scope + nhãn mới

- [x] `AssignConfigHistoryModal.vue`:
  - `FIELD_LABELS` thêm: `km_support_stay_cost: 'Số Km hỗ trợ lưu trú'`, `km_support_regulation_cost: 'Số Km hỗ trợ công tác phí'`, `places_origin: 'Danh sách địa điểm gốc'`. `LIST_FIELDS` thêm `'places_origin'`.
  - `SCOPE_FIELDS = { common: [<26 key Phase 1>], places: ['km_support_stay_cost', 'km_support_regulation_cost', 'places_origin'] }`.
  - `open(scope)` (mặc định `'common'`) lưu `this.scope`; `parseHistoryItem` CHỈ xét key thuộc `SCOPE_FIELDS[this.scope]`; log sau lọc 0 key → loại khỏi `historyItems` (filter). Bộ lọc "Trường" options theo scope. Title modal + phụ đề tab: common → `— Thông tin chung`, places → `— Giới hạn khoảng cách tính công tác phí`.
  - `listItemKey` places_origin: `` `${item.name}|${item.lat}|${item.lng}` ``; `listItemLabel`: `` `${item.name || '(trống)'} (${item.lat}, ${item.lng})` ``.
  - Compile template + node --check script.

### T15. FE — nút tab 2 + scope nút tab 1

- [x] `pages/assign/settings/index.vue`: nút tab 1 hiện tại đổi `@click` thành `$refs.assignConfigHistoryModal.open('common')`. Thêm nút giống hệt (light + ri-history-line + sm, label "Lịch sử thay đổi") BÊN TRÁI nút Lưu ở khối `dataTables_filter` THỨ HAI (tab Giới hạn khoảng cách, dòng ~760) → `open('places')`. Compile check.

### T16. Verify tinker Phase 2

- [x] (maxId trước test, dọn `where('id','>',$maxId)`, snapshot + khôi phục config nguyên trạng): (a) đổi `km_support_stay_cost` → 1 log 1 key; (b) đổi tên 1 địa điểm → 1 log `places_origin` old/new mảng {name,lat,lng} đúng; (c) đổi tọa độ → log; (d) no-op → 0 log; (e) đổi 1 trường tab 1 + 1 trường tab 2 cùng 1 lần lưu → 1 dòng chứa key cả 2 tab; (f) request thiếu key `places_origin` → không diff key đó; `histories()` format OK.

### T17. Playwright Phase 2

- [x] Tab 2 có nút lịch sử; mở → chỉ GET; seed log hỗn hợp 2 tab (qua UI đổi cả 2 tab rồi Lưu 1 lần) → modal tab 1 CHỈ hiện phần tab 1, modal tab 2 CHỈ hiện phần tab 2 (cùng 1 dòng log DB); chip địa điểm `Tên (lat, lng)` thêm xanh/bớt đỏ; đổi km → diff đỏ/xanh; khôi phục UI + dọn log tinker; check phantom-write.


### Checkpoint — 2026-07-16 (Phase 2, subagent-driven Fable 5)
Vừa hoàn thành: Phase 4 (T13-T17) — track thêm tab "Giới hạn khoảng cách tính công tác phí" (2 km + places_origin {name,lat,lng}, không migration mới) + modal scope theo tab (nút riêng tab 2, open('common'/'places'), log hỗn hợp 2 tab = 1 dòng DB hiển thị tách). Review code PASS (3 minor: 2 comment đã sửa, 1 lý thuyết chấp nhận); verify tinker 7/7 + Playwright 8/8 PASS; place_origins khôi phục GIỮ ID CŨ (không phá tham chiếu assign_requests); log test dọn sạch.
Đang làm dở: (không)
Bước tiếp theo: user verify browser 2 tab → quyết định commit. LƯU Ý: bảng history còn 10 dòng THẬT (id 10-19, user id 13 tự test browser ~10:24-10:28 sáng nay) — không phải rác của phiên verify, chờ user quyết giữ/xóa.
Blocked: (không)

---

## Phase 5 — Lịch sử tab Quản lý dự án → Cấu hình mức độ ưu tiên (2026-07-16, user duyệt — spec mục 10)

User chốt: kéo thả STT = 1 dòng log `reorder`; 1 nút chung tab. Bảng mới `priority_level_history` (GLOBAL, không company_id). Full-snapshot per-row, KHÔNG track sort_order trong create/update/delete.

### T18. Migration + Entity + helper log

- [x] Migration `2026_07_16_000002_create_priority_level_history_table.php` (Modules/Assign, PHPDoc up/down theo mẫu `2026_07_16_000001`): `id`, `priority_level_id` unsignedBigInteger NULLABLE index comment 'Mức độ ưu tiên (NULL với log reorder)', `action` string comment 'create | update | delete | reorder', `old_value`/`new_value` text nullable, `changed_by` unsignedBigInteger nullable, `changed_at` timestamp useCurrent, timestamps. CHƯA migrate (chờ user duyệt).
- [x] Entity `Modules/Assign/Entities/PriorityLevelHistory.php`: `$table='priority_level_history'`, fillable [priority_level_id, action, old_value, new_value, changed_by, changed_at], `user()` belongsTo `Modules\Human\Entities\Employee` theo changed_by, static `log(array $data)` bọc try/catch \Throwable + `Log::error('PriorityLevelHistory::log failed: ' . $e->getMessage())` (mẫu `Modules/Human/Entities/HumanSettingHistory.php`).
- [x] `php -l` cả 2 file.

### T19. Service — snapshot + hook create/update + logDeleted/logReorderIfChanged + histories

- [x] `Modules/Assign/Services/PriorityLevelService.php` thêm use (Carbon, PriorityLevelHistory) + code:

```php
    const SNAPSHOT_FIELDS = ['name', 'response_days', 'response_hours', 'color'];

    /** Chụp snapshot 4 trường nghiệp vụ (KHÔNG sort_order — FE luôn gửi lại theo vị trí, gây nhiễu log) */
    private function buildSnapshot(PriorityLevel $priorityLevel)
    {
        $snapshot = [];
        foreach (self::SNAPSHOT_FIELDS as $field) {
            $value = $priorityLevel->getAttribute($field);
            if ($value === null || $value === '') {
                $snapshot[$field] = null;
            } elseif (is_numeric($value)) {
                $number = (float) $value;
                $snapshot[$field] = $number == (int) $number ? (int) $number : $number;
            } else {
                $snapshot[$field] = (string) $value;
            }
        }
        return $snapshot;
    }
```

- [x] `create()`: sau `PriorityLevel::create(...)` trước return → `PriorityLevelHistory::log(['priority_level_id' => $priorityLevel->id, 'action' => 'create', 'old_value' => null, 'new_value' => json_encode($this->buildSnapshot($priorityLevel), JSON_UNESCAPED_UNICODE), 'changed_by' => auth()->id(), 'changed_at' => Carbon::now()]);`
- [x] `update()`: `$oldSnapshot = $this->buildSnapshot($priorityLevel);` TRƯỚC `$priorityLevel->update(...)`; sau update `$newSnapshot = $this->buildSnapshot($priorityLevel);` → `if ($oldSnapshot !== $newSnapshot)` → log action 'update' với old/new = json_encode 2 snapshot đầy đủ.
- [x] Method mới `logDeleted(PriorityLevel $priorityLevel)`: log action 'delete', old_value = json_encode snapshot, new_value = null.
- [x] Method mới `logReorderIfChanged(array $oldOrder)`: `$newOrder = PriorityLevel::query()->orderBy('sort_order', 'asc')->orderBy('created_at', 'desc')->pluck('name')->all();` → `if ($oldOrder !== $newOrder)` → log ['priority_level_id' => null, 'action' => 'reorder', 'old_value' => json_encode(['order' => $oldOrder], JSON_UNESCAPED_UNICODE), 'new_value' => json_encode(['order' => $newOrder], JSON_UNESCAPED_UNICODE), 'changed_by' => auth()->id(), 'changed_at' => Carbon::now()].
- [x] Method mới `histories()`: mẫu `AssignConfigService::histories` (with user.info, sort changed_at ASC + id ASC, changed_by_name fallback fullname/email/—, changed_at d/m/Y H:i:s + changed_at_raw Y-m-d) + thêm `row_label`: action khác 'reorder' → name lấy từ json_decode(new_value)['name'] ?? json_decode(old_value)['name'] ?? null; reorder → null. Trả thêm `priority_level_id`. `php -l`.

### T20. Controller + route

- [x] `PriorityLevelController::destroy`: sau `$priorityLevel->delete();` thêm `$this->priorityLevelService->logDeleted($priorityLevel);` (helper log đã try/catch — không fail transaction).
- [x] `bulkUpdateSortOrder`: trong transaction, TRƯỚC foreach → `$oldOrder = PriorityLevel::query()->orderBy('sort_order', 'asc')->orderBy('created_at', 'desc')->pluck('name')->all();`; SAU foreach → `$this->priorityLevelService->logReorderIfChanged($oldOrder);`
- [x] Method `histories(Request $request)` mẫu `AssignConfigController::histories` (try/catch + responseJson 3-arg gọi `$this->priorityLevelService->histories()`).
- [x] Route group `/assign/priority-levels` (api.php ~738): thêm `Route::get('/histories', [PriorityLevelController::class, 'histories']);` NGAY SAU dòng `/getAll` (trước mọi route có tham số). `php -l` cả 2 file.

### T21. FE — modal PriorityLevelHistoryModal.vue

- [x] File mới `pages/assign/settings/components/PriorityLevelHistoryModal.vue` — chrome modal (b-modal hide-footer, header icon tròn ri-history-line + X, footer Đóng tertiary, bộ lọc collapse, timeline, CSS) theo `AssignConfigHistoryModal.vue` CÙNG THƯ MỤC. Khác biệt:
  - Modal id `priority-level-history-modal`, title "Lịch sử thay đổi — Cấu hình mức độ ưu tiên".
  - `open()` không tham số, fetch `apiGetMethod 'assign/priority-levels/histories'`.
  - `FIELD_LABELS = { name: 'Tên mức độ ưu tiên', response_days: 'Số ngày phản hồi', response_hours: 'Số giờ phản hồi', color: 'Mã màu' }`.
  - `ACTION_META = { create: {title: 'Thêm mức độ ưu tiên', dot #16a34a}, update: {title: 'Cập nhật mức độ ưu tiên', dot #f59e0b}, delete: {title: 'Xóa mức độ ưu tiên', dot #dc2626}, reorder: {title: 'Đổi thứ tự ưu tiên', dot #f59e0b} }`; badge `row_label` cạnh title khi có.
  - Render theo action: create → liệt kê 4 trường giá trị XANH (#16a34a); delete → liệt kê ĐỎ (#dc2626); update → CHỈ trường old !== new: `Nhãn: cũ (đỏ) → mới (xanh)`; reorder → so 2 mảng order theo vị trí: chỉ hiện vị trí khác nhau dạng `STT i+1: tên cũ (đỏ) → tên mới (xanh)` (nếu 2 mảng lệch độ dài thì hiện đủ phần dư).
  - Giá trị `color` render swatch: span inline-block 12×12px border-radius 3px border nhạt `:style="{background: value}"` + text mã màu — áp cả create/update/delete.
  - Bộ lọc client-side: Thao tác (4 option theo ACTION_META) / Người thực hiện / Từ ngày / Đến ngày (changed_at_raw); nút Tìm kiếm + Làm mới; empty state.
  - Compile template + node --check script.

### T22. FE — nút mở modal

- [x] `pages/assign/settings/index.vue`: header khối priority (div `ml-auto` chứa nút "Thêm dòng" `addPriorityRow()`) → thêm TRƯỚC nút Thêm dòng: V2BaseButton light size sm class mr-2 + prefix ri-history-line + "Lịch sử thay đổi" → `@click="$refs.priorityLevelHistoryModal.open()"`. Thêm tag `<priority-level-history-modal ref="priorityLevelHistoryModal"></priority-level-history-modal>` cạnh BaseConfirmModal cuối template + import/đăng ký component. Compile check.

### T23. Verify tinker Phase 3

- [x] (maxId trước test; dòng priority test TỰ TẠO TỰ XÓA — KHÔNG đụng dòng thật vì có thể đang được projectPhases dùng; dọn log where id > maxId): create qua service → 1 log create snapshot 4 trường; update đổi 1 trường → 1 log update old/new; update no-op → 0 log; delete dòng test + logDeleted → 1 log delete; reorder qua flow bulkUpdateSortOrder với 2 dòng test → 1 dòng reorder old/new order đúng; reorder no-op → 0 log; `histories()` format + row_label đúng (reorder → null). KHÔNG đổi sort_order dòng thật; log test cuối = 0.

### T24. Playwright Phase 3

- [x] Tab Quản lý dự án → Cấu hình mức độ ưu tiên: nút lịch sử trái nút Thêm dòng; mở modal → CHỈ GET histories; thêm dòng test qua UI → log create; sửa dòng test → log update diff; kéo thả STT → log reorder; xóa dòng test → log delete; swatch màu render đúng; bộ lọc Thao tác; dọn log tinker → 0; check phantom write (POST/PUT/DELETE chỉ vào priority-levels), sort_order dòng thật nguyên trạng.


### Checkpoint — 2026-07-16 (Phase 3, subagent-driven Fable 5)
Vừa hoàn thành: Phase 5 (T18-T24) — lịch sử CRUD + kéo thả tab Cấu hình mức độ ưu tiên. Bảng priority_level_history ĐÃ migrate (2026_07_16_000002). Review PASS (1 minor color-normalize đã fix inline: chỉ response_days/hours qua nhánh numeric); verify tinker 7/7 + Playwright 7/7 PASS (kéo thả thật qua drag handle; reorder no-op không log được kiểm chứng cả trên UI); log=0, dòng thật nguyên trạng.
Đang làm dở: (không)
Bước tiếp theo: user verify browser tab Quản lý dự án → quyết định commit (cùng 10 log thật id 10-19 chờ quyết giữ/xóa).
Blocked: (không)

---

## Phase 6 — Lịch sử sub-tab Cấu hình hạn (2026-07-16, user duyệt — spec mục 11)

6 trường hạn nằm trên entity `GeneralRegulation` (bảng general_regulations, theo công ty) nhưng lưu qua endpoint riêng `POST assign/my-job/deadline-config` (`MyJobService::saveDeadlineConfig` — KHÔNG qua GeneralRegulationService). Bảng MỚI `assign_deadline_config_history` (tách riêng theo tiền lệ human-settings-history). Subset-diff, chỉ action `update`.

### T25. Migration + Entity

- [x] Migration `2026_07_16_000003_create_assign_deadline_config_history_table.php` (Modules/Assign, PHPDoc up/down theo mẫu 2026_07_16_000002): `id`, `general_regulation_id` unsignedBigInteger index comment 'Quy định chung (nơi lưu 6 trường cấu hình hạn)', `company_id` unsignedBigInteger nullable index, `action` string comment 'Loại thao tác: update', `old_value`/`new_value` text nullable comment JSON subset, `changed_by` unsignedBigInteger nullable, `changed_at` timestamp useCurrent, timestamps. CHƯA migrate.
- [x] Entity `Modules/Assign/Entities/AssignDeadlineConfigHistory.php`: `$table='assign_deadline_config_history'`, fillable [general_regulation_id, company_id, action, old_value, new_value, changed_by, changed_at], `user()` belongsTo `Modules\Human\Entities\Employee`, static `log(array $data)` try/catch \Throwable + Log::error (mẫu `PriorityLevelHistory`).
- [x] `php -l` cả 2 file.

### T26. Service — MyJobService

- [x] `Modules/Assign/Services/MyJobService.php` — kiểm tra + thêm use còn thiếu (Carbon, AssignDeadlineConfigHistory; GeneralRegulation đã có). Thêm:

```php
    /** 6 trường cấu hình hạn (sub-tab Cấu hình hạn màn /assign/settings) được track lịch sử */
    const DEADLINE_TRACKED_FIELDS = [
        'task_due_days',
        'issue_due_days',
        'meeting_due_days',
        'solution_due_days',
        'category_late_task_threshold',
        'people_late_task_threshold',
    ];

    /** Chụp snapshot 6 trường hạn đã chuẩn hoá — $generalRegulation null (công ty chưa có record) → toàn null */
    private function buildDeadlineSnapshot($generalRegulation)
    {
        $snapshot = [];
        foreach (self::DEADLINE_TRACKED_FIELDS as $field) {
            $value = $generalRegulation ? $generalRegulation->getAttribute($field) : null;
            if ($value === null || $value === '') {
                $snapshot[$field] = null;
            } elseif (is_numeric($value)) {
                $number = (float) $value;
                $snapshot[$field] = $number == (int) $number ? (int) $number : $number;
            } else {
                $snapshot[$field] = (string) $value;
            }
        }
        return $snapshot;
    }

    /** So snapshot trước/sau, có trường đổi thì ghi 1 dòng lịch sử (old/new = JSON chỉ gồm trường đổi) */
    private function logDeadlineHistoryIfChanged($generalRegulation, array $oldSnapshot)
    {
        $newSnapshot = $this->buildDeadlineSnapshot($generalRegulation);
        $oldChanged = [];
        $newChanged = [];
        foreach (self::DEADLINE_TRACKED_FIELDS as $field) {
            if ($oldSnapshot[$field] !== $newSnapshot[$field]) {
                $oldChanged[$field] = $oldSnapshot[$field];
                $newChanged[$field] = $newSnapshot[$field];
            }
        }
        if (empty($newChanged)) {
            return;
        }
        AssignDeadlineConfigHistory::log([
            'general_regulation_id' => $generalRegulation->id,
            'company_id' => $generalRegulation->company_id,
            'action' => 'update',
            'old_value' => json_encode($oldChanged, JSON_UNESCAPED_UNICODE),
            'new_value' => json_encode($newChanged, JSON_UNESCAPED_UNICODE),
            'changed_by' => auth()->id(),
            'changed_at' => Carbon::now(),
        ]);
    }
```

- [x] Hook `saveDeadlineConfig()` (dòng ~1024): sau dòng fetch `$generalRegulation = GeneralRegulation::where(...)->first();` → thêm `$oldSnapshot = $this->buildDeadlineSnapshot($generalRegulation);`. Trước `return [...]` cuối hàm → thêm `$this->logDeadlineHistoryIfChanged($generalRegulation, $oldSnapshot);`. KHÔNG đổi gì khác trong hàm.
- [x] Method `deadlineHistories()`: mẫu histories chuẩn — `AssignDeadlineConfigHistory::with('user.info')->where('company_id', auth()->user()->current_company_role)->orderBy('changed_at','asc')->orderBy('id','asc')->get()` → map trả id/action/old_value/new_value/changed_by/changed_by_name (fullname ?: email ?: '—' qua optional(), KHÔNG ?->)/changed_at d/m/Y H:i:s/changed_at_raw Y-m-d. `php -l`.

### T27. Controller + route

- [x] `MyJobController` thêm method `getDeadlineConfigHistories()`: try/catch + `responseJson('success', Response::HTTP_OK, $this->myJobService->deadlineHistories())` (theo pattern các method cùng controller).
- [x] Route group my-job (api.php ~903): thêm `Route::get('/deadline-config/histories', [MyJobController::class, 'getDeadlineConfigHistories']);` NGAY TRÊN dòng `GET '/deadline-config'`. `php -l` cả 2 file.

### T28. FE — modal DeadlineConfigHistoryModal.vue

- [x] File mới `pages/assign/settings/components/DeadlineConfigHistoryModal.vue` — chrome theo `AssignConfigHistoryModal.vue` cùng thư mục nhưng ĐƠN GIẢN HƠN: không scope, không danh sách, chỉ diff scalar. Modal id `deadline-config-history-modal`, title "Lịch sử thay đổi — Cấu hình hạn". `open()` fetch `apiGetMethod 'assign/my-job/deadline-config/histories'` (KHÔNG query param). FIELD_LABELS 6: task_due_days 'Cảnh báo sớm task trước (ngày)' / issue_due_days 'Cảnh báo sớm Issue trước (ngày)' / meeting_due_days 'Meeting sắp tới lịch trước (ngày)' / solution_due_days 'Giải pháp sắp tới hạn trước (ngày)' / category_late_task_threshold 'Hạng mục nhiều task trễ khi có từ (task trễ)' / people_late_task_threshold 'Nhân sự nhiều task trễ khi có từ (task trễ)'. Giá trị số thường (String), null/rỗng → '(trống)', cũ đỏ #dc2626 → mới xanh #16a34a. Bộ lọc client-side Trường/Người/Từ–Đến ngày + Tìm kiếm/Làm mới + empty state. JSON.parse an toàn. Compile + node --check.

### T29. FE — nút mở modal

- [x] `pages/assign/settings/index.vue`: khối Actions sub-tab Cấu hình hạn (`d-flex justify-content-end mt-4` chứa nút "Lưu cấu hình" `saveDeadlineConfig`) → thêm TRƯỚC nút Lưu cấu hình: V2BaseButton light size sm + prefix ri-history-line + "Lịch sử thay đổi" → `@click="$refs.deadlineConfigHistoryModal.open()"`. Tag `<deadline-config-history-modal ref="deadlineConfigHistoryModal"></deadline-config-history-modal>` cạnh 2 modal history đã có + import/đăng ký. Compile check.

### T30. Verify tinker Phase 4

- [x] (maxId trước test; chụp 6 trường deadline của general_regulations công ty test + khôi phục que query builder — entity dùng chung NHIỀU màn, TUYỆT ĐỐI chỉ đụng 6 trường này): đổi 1 trường qua `saveDeadlineConfig` flow thật (Auth user 13) → 1 log subset 1 key; no-op → 0; 2 trường → 1 dòng 2 key; xác nhận 0 dòng mới ở `general_regulation_history` + `human_setting_history` (2 bảng log khác của entity); company chưa có record (nếu có company test an toàn) → create + log old=null → XÓA record vừa tạo bằng query builder; `deadlineHistories()` format + scope company. Dọn log = 0, giá trị khôi phục.

### T31. Playwright Phase 4

- [x] Tab Quản lý dự án → sub-tab Cấu hình hạn: nút lịch sử trái nút "Lưu cấu hình"; mở modal → CHỈ GET histories; đổi "Cảnh báo sớm task trước" → Lưu → modal dòng mới diff cũ đỏ → mới xanh + người + giờ; bộ lọc; khôi phục giá trị qua UI; dọn log tinker → 0; phantom check (POST chỉ vào my-job/deadline-config).


### Checkpoint — 2026-07-16 (Phase 4, subagent-driven Fable 5)
Vừa hoàn thành: Phase 6 (T25-T31) — lịch sử sub-tab Cấu hình hạn. 6 trường deadline nằm trên GeneralRegulation (entity dùng chung) nhưng lưu qua endpoint riêng my-job/deadline-config → bảng RIÊNG assign_deadline_config_history (ĐÃ migrate 2026_07_16_000003) theo tiền lệ human-settings-history. Review PASS (3 minor cosmetic chấp nhận); verify tinker 6/6 (kể cả first-save company 6 + cách ly 2 bảng log cũ của entity + scope company) + Playwright 4/4 PASS; log=0, general_regulations khôi phục từng trường khớp snapshot (query builder, không Eloquent save).
Đang làm dở: (không)
Bước tiếp theo: user verify browser CẢ 4 phase → quyết định commit. TOÀN BỘ màn /assign/settings đã có lịch sử: tab Thông tin chung + tab Giới hạn khoảng cách (assign_config_history) / tab Cấu hình mức độ ưu tiên (priority_level_history) / tab Cấu hình hạn (assign_deadline_config_history).
Blocked: (không)
