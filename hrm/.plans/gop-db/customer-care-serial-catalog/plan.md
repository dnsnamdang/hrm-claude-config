# Plan — Danh mục serial thiết bị làm dịch vụ (CSKH)

**Người phụ trách:** @junfoke — 2026-08-06
**Nhánh:** `gop_db` (cả `hrm-api` và `hrm-client`)
**Design:** `.plans/gop-db/customer-care-serial-catalog/design.md`
**Spec:** `docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md`

**Mục tiêu:** màn danh sách read-only `/customer-care/serials` + Xuất Excel, 7 cột, 6 bộ lọc,
1 quyền mới id 1126, 3 route `/v1/customer-care/serials*`.

## Ràng buộc chung (áp cho mọi task)

- **Không commit / không push git** (rule dự án).
- Không dùng connection `mysql2` / `DB_CONNECTION_SECOND`.
- Bảng quyền SỐNG là `permissions`, KHÔNG phải `hrm_permissions`.
- Không sửa `App\Models\TpSerial`, `CustomerManagerService`, hay bảng `serials`.
- Cờ quyền FE khởi tạo `false`, chỉ set từ `$store.state.permissions` (fail-closed).
- `status`: 1 = Đang sử dụng, 2 = Ngưng sử dụng.
- FE dùng V2Base, bám sát `pages/customer-care/note-maintenances/index.vue`.

---

## Phase 0 — Chuẩn bị & xác minh dữ liệu

- [x] **0.1 Đọc 2 skill FE trước khi viết code màn danh sách**

`hrm-claude-config/hrm/.claude/skills/list-page/SKILL.md` và
`hrm-claude-config/hrm/.claude/skills/button-convention/SKILL.md`.

- [x] **0.2 Xác minh schema thật của `serials` trên DB gộp**

```sql
SHOW COLUMNS FROM serials;
SELECT COUNT(*) AS total,
       SUM(status = 1) AS dang_su_dung,
       SUM(status = 2) AS ngung_su_dung,
       SUM(created_by IS NULL OR created_by = 0) AS thieu_nguoi_tao,
       SUM(updated_by IS NULL OR updated_by = 0) AS thieu_nguoi_cap_nhat
FROM serials;
```

Ghi lại `total` — dùng đối chiếu ở Phase 4. Nếu `product_type`/`created_by` khác spec (spec ghi
`created_by` là `int`), cập nhật spec trước khi code.

- [x] **0.3 Xác minh khóa nối bảng nhân viên**

```sql
SELECT s.id, s.created_by, ei.fullname
FROM serials s
LEFT JOIN employees e ON e.id = s.created_by
LEFT JOIN employee_infos ei ON ei.id = e.employee_info_id
LIMIT 5;
```

Phải ra tên người thật (ít nhất vài dòng). Nếu `fullname` rỗng toàn bộ → dừng, báo lại: giả định
`serials.created_by = employees.id` sai, cần đổi cách nối trước khi làm tiếp.

---

## Phase 1 — Backend

- [x] **1.1 Tạo `SerialService`**

Create: `hrm-api/Modules/CustomerCare/Services/SerialService.php`

```php
<?php

namespace Modules\CustomerCare\Services;

use App\Models\TpSerial;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

/**
 * Danh mục serial thiết bị làm dịch vụ (bảng ERP `serials` trên DB gộp).
 * Màn CHỈ ĐỌC — mọi thao tác ghi serial nằm ở màn Quản lý khách hàng (Modules/MasterData).
 */
class SerialService
{
    /**
     * Cột được phép sort. `key` cột trên FE phải trùng đúng các key ở đây.
     */
    private const SORT_FIELDS = [
        'serial' => 'serials.serial',
        'product_name' => 'serials.product_name',
        'customer_name' => 'serials.customer_name',
        'status' => 'serials.status',
        'created_by_name' => 'eic.fullname',
        'updated_by_name' => 'eiu.fullname',
        'updated_at' => 'serials.updated_at',
    ];

    /**
     * @param  Request $request
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function index(Request $request)
    {
        $query = TpSerial::query()
            ->leftJoin('employees as ec', 'ec.id', '=', 'serials.created_by')
            ->leftJoin('employee_infos as eic', 'eic.id', '=', 'ec.employee_info_id')
            ->leftJoin('employees as eu', 'eu.id', '=', 'serials.updated_by')
            ->leftJoin('employee_infos as eiu', 'eiu.id', '=', 'eu.employee_info_id')
            ->select([
                'serials.id',
                'serials.serial',
                'serials.product_name',
                'serials.customer_code',
                'serials.customer_name',
                'serials.status',
                'serials.updated_at',
                DB::raw('eic.fullname as created_by_name'),
                DB::raw('eiu.fullname as updated_by_name'),
            ]);

        if ($request->filled('keyword')) {
            $keyword = escapeLikeKeyword($request->get('keyword'));
            if ($keyword !== '') {
                $query->where(function ($q) use ($keyword) {
                    $q->where('serials.serial', 'like', '%' . $keyword . '%')
                        ->orWhere('serials.product_name', 'like', '%' . $keyword . '%')
                        ->orWhere('serials.customer_name', 'like', '%' . $keyword . '%');
                });
            }
        }

        foreach (['serial' => 'serials.serial', 'product_name' => 'serials.product_name'] as $param => $column) {
            if ($request->filled($param)) {
                $value = escapeLikeKeyword($request->get($param));
                if ($value !== '') {
                    $query->where($column, 'like', '%' . $value . '%');
                }
            }
        }

        if ($request->filled('customer_id')) {
            $query->where('serials.customer_id', $request->get('customer_id'));
        }
        if ($request->filled('status')) {
            $query->where('serials.status', (int) $request->get('status'));
        }
        if ($request->filled('created_by')) {
            $query->where('serials.created_by', (int) $request->get('created_by'));
        }
        if ($request->filled('updated_by')) {
            $query->where('serials.updated_by', (int) $request->get('updated_by'));
        }

        if ($request->filled('sort_by') && array_key_exists($request->get('sort_by'), self::SORT_FIELDS)) {
            $direction = strtolower($request->get('sort_desc')) === 'true' ? 'desc' : 'asc';

            return $query->orderBy(self::SORT_FIELDS[$request->get('sort_by')], $direction);
        }

        return $query->orderBy('serials.created_at', 'desc');
    }

    /**
     * Danh sách người tạo / người cập nhật cho dropdown bộ lọc.
     * Lấy DISTINCT từ chính bảng `serials` — KHÔNG dùng human/employee-infos/list-for-select
     * vì endpoint đó trả id của `employee_infos`, lệch hệ id với `serials.created_by`
     * (= `employees.id`) nên lọc sẽ ra 0 dòng.
     *
     * @return array{created_by: array, updated_by: array}
     */
    public function filterOptions(): array
    {
        return [
            'created_by' => $this->employeeOptions('created_by'),
            'updated_by' => $this->employeeOptions('updated_by'),
        ];
    }

    /**
     * @param  string $column `created_by` hoặc `updated_by`
     * @return array
     */
    private function employeeOptions(string $column): array
    {
        return DB::table('serials')
            ->join('employees', 'employees.id', '=', 'serials.' . $column)
            ->join('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
            ->whereNotNull('employee_infos.fullname')
            ->distinct()
            ->orderBy('employee_infos.fullname')
            ->pluck('employee_infos.fullname', 'employees.id')
            ->map(function ($name, $id) {
                return ['id' => (int) $id, 'name' => $name];
            })
            ->values()
            ->toArray();
    }
}
```

- [x] **1.2 Tạo `SerialListResource`**

Create: `hrm-api/Modules/CustomerCare/Transformers/SerialResource/SerialListResource.php`

```php
<?php

namespace Modules\CustomerCare\Transformers\SerialResource;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;

class SerialListResource extends ApiResource
{
    /**
     * @param  \Illuminate\Http\Request $request
     * @return array
     */
    public function toArray($request): array
    {
        $customer = trim(implode(' - ', array_filter([
            $this->customer_code,
            $this->customer_name,
        ])));

        return [
            'id' => $this->id,
            'serial' => $this->serial,
            'product_name' => $this->product_name,
            'customer' => $customer !== '' ? $customer : null,
            'status' => (int) $this->status,
            'status_text' => (int) $this->status === 1 ? 'Đang sử dụng' : 'Ngưng sử dụng',
            // ERP gọi thẳng `employee_update->info->fullname` nên bản ghi thiếu người cập nhật
            // làm 500 — ở đây để trống.
            'created_by_name' => $this->created_by_name,
            'updated_by_name' => $this->updated_by_name,
            'updated_at' => Helper::formatDateTime($this->updated_at, 'd/m/Y'),
        ];
    }
}
```

- [x] **1.3 Tạo view xuất Excel**

Create: `hrm-api/resources/views/exports/serials.blade.php`

```blade
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="{{ public_path('css/pdf.css') }}" rel="stylesheet" type="text/css" />
</head>

<body>
    <table style="width:100%">
        <tr>
            <td colspan="7" style="width: 100%;">
                <img src="{{ public_path('images/info-tpe.jpg') }}">
            </td>
        </tr>
        <tr class="no-border">
            <td colspan="7" style="text-align: center; font-weight: bold; font-size: 25px">
                Danh mục serial thiết bị làm dịch vụ
            </td>
        </tr>

        <thead>
            <tr>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 60px">STT</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 200px">Serial thiết bị làm dịch vụ</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 300px">Tên hàng</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 300px">Khách hàng</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 130px">Trạng thái</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 180px">Người tạo</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 180px">Người cập nhật</td>
                <td style="text-align: center; font-weight: bold; border: 1px solid black; width: 130px">Ngày cập nhật</td>
            </tr>
        </thead>

        <tbody>
            @foreach($data as $k => $item)
            <tr>
                <td style="text-align: center; border: 1px solid black;">{{ $k + 1 }}</td>
                <td style="border: 1px solid black;">{{ $item['serial'] }}</td>
                <td style="border: 1px solid black;">{{ $item['product_name'] }}</td>
                <td style="border: 1px solid black;">{{ $item['customer'] }}</td>
                <td style="border: 1px solid black;">{{ $item['status_text'] }}</td>
                <td style="border: 1px solid black;">{{ $item['created_by_name'] }}</td>
                <td style="border: 1px solid black;">{{ $item['updated_by_name'] }}</td>
                <td style="border: 1px solid black;">{{ $item['updated_at'] }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
</body>

</html>
```

⚠️ Header có **8 ô** (STT + 7 cột dữ liệu) nhưng `colspan` ở 2 dòng đầu là 7 → sửa `colspan="8"`
cho 2 dòng tiêu đề khi viết file, để cột không bị lệch.

- [x] **1.4 Tạo class Export**

Create: `hrm-api/app/ExcelExport/SerialExport.php`

```php
<?php

namespace App\ExcelExport;

use Illuminate\Contracts\View\View;
use Maatwebsite\Excel\Concerns\Exportable;
use Maatwebsite\Excel\Concerns\FromView;

/**
 * Xuất Excel Danh mục serial thiết bị làm dịch vụ (phân hệ CSKH).
 */
class SerialExport implements FromView
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

        return view('exports.serials', compact('data'));
    }
}
```

- [x] **1.5 Tạo `SerialController`**

Create: `hrm-api/Modules/CustomerCare/Http/Controllers/V1/SerialController.php`

```php
<?php

namespace Modules\CustomerCare\Http\Controllers\V1;

use App\ExcelExport\SerialExport;
use App\Http\Controllers\ApiController;
use Exception;
use Excel;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Log;
use Modules\CustomerCare\Services\SerialService;
use Modules\CustomerCare\Transformers\SerialResource\SerialListResource;

/**
 * Danh mục serial thiết bị làm dịch vụ — chuyển từ ERP (admin/serials) sang CSKH.
 * CHỈ ĐỌC: thêm/sửa/đổi/xóa serial nằm ở màn Quản lý khách hàng (tab Trang thiết bị).
 */
class SerialController extends ApiController
{
    private $serialService;

    public function __construct(SerialService $serialService)
    {
        $this->serialService = $serialService;
        parent::__construct();
    }

    public function index(Request $request)
    {
        $query = $this->serialService->index($request);

        return $this->apiGetList(SerialListResource::apiPaginate($query, $request));
    }

    public function filterOptions()
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->serialService->filterOptions());
    }

    public function export(Request $request)
    {
        try {
            $collection = $this->serialService->index($request)->get();
            $data = SerialListResource::collection($collection)->resolve();

            return Excel::download(
                (new SerialExport())->forData($data),
                'danh_muc_serial_thiet_bi_lam_dich_vu.xlsx'
            );
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseBadRequest($e->getMessage());
        }
    }
}
```

- [x] **1.6 Khai route**

Modify: `hrm-api/Modules/CustomerCare/Routes/api.php`

Thêm `use Modules\CustomerCare\Http\Controllers\V1\SerialController;` ở đầu file, và thêm group
sau group `/services` (trước dấu đóng của group `/v1/customer-care`):

```php
    // Danh muc serial thiet bi lam dich vu (bang ERP `serials` tren DB gop) — CHI DOC
    Route::group(['prefix' => '/serials'], function () {
        Route::get('/', [SerialController::class, 'index'])
            ->middleware('checkPermission:Xem danh mục serial thiết bị làm dịch vụ');
        Route::get('/filter-options', [SerialController::class, 'filterOptions'])
            ->middleware('checkPermission:Xem danh mục serial thiết bị làm dịch vụ');
        Route::get('/export', [SerialController::class, 'export'])
            ->middleware('checkPermission:Xem danh mục serial thiết bị làm dịch vụ');
    });
```

- [x] **1.7 Kiểm cú pháp + route đăng ký được**

```bash
cd hrm-api
php -l Modules/CustomerCare/Services/SerialService.php
php -l Modules/CustomerCare/Http/Controllers/V1/SerialController.php
php -l Modules/CustomerCare/Transformers/SerialResource/SerialListResource.php
php -l app/ExcelExport/SerialExport.php
php artisan route:list --path=customer-care/serials
```

Kỳ vọng: 4 file `No syntax errors`; `route:list` in ra đúng **3 route**.
Nếu `route:list` báo lỗi 500 không liên quan (`PermissionHelper` gọi `employee_info_id`) — lỗi có
sẵn, dùng `php artisan route:list | findstr serials` để xác nhận thay thế.

---

## Phase 2 — Quyền & menu

- [x] **2.1 Thêm quyền vào seeder**

Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

Thêm ngay sau dòng `id => 1125`:

```php
        Permission::create(['id' => 1126, 'guard_name' => 'api', 'name' => 'Xem danh mục serial thiết bị làm dịch vụ', 'display_name' => 'Xem danh mục serial thiết bị làm dịch vụ', 'group' => 'Danh mục dịch vụ bảo dưỡng', 'type' => 24]);
```

⚠️ Kiểm lại id 1126 chưa bị ai dùng (nhánh khác có thể đã lấy):

```bash
grep -n "'id' => 1126" hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```

Nếu đã có → lấy id trống kế tiếp và cập nhật cả spec + design.

- [x] **2.2 Bơm quyền vào DB đang chạy**

Seeder không tự chạy lại trên DB đã seed → chèn tay:

```sql
INSERT INTO permissions (id, guard_name, name, display_name, `group`, type, created_at, updated_at)
VALUES (1126, 'api', 'Xem danh mục serial thiết bị làm dịch vụ',
        'Xem danh mục serial thiết bị làm dịch vụ', 'Danh mục dịch vụ bảo dưỡng', 24, NOW(), NOW());
```

Kiểm cột thật của bảng `permissions` trước khi chạy (`SHOW COLUMNS FROM permissions`) — nếu có
cột NOT NULL khác thì bổ sung. Sau đó gán quyền cho chức vụ đang test để verify được.

- [x] **2.3 Điền link vào menu CSKH**

Modify: `hrm-client/components/subsystem-menu/customer-care.js:54`

```js
            {
                label: 'Danh mục serial thiết bị làm dịch vụ',
                link: '/customer-care/serials',
                isShow: ['Xem danh mục serial thiết bị làm dịch vụ'],
            },
```

Đồng thời cập nhật đoạn chú thích đầu file (dòng 7-9) — thêm `serials` vào danh sách "Đã chuyển
sang HRM".

- [x] **2.4 Kiểm bất biến "mỗi link chỉ thuộc 1 phân hệ"**

```bash
grep -rn "customer-care/serials" hrm-client/components/subsystem-menu/
```

Kỳ vọng: đúng **1** kết quả (file `customer-care.js`).

---

## Phase 3 — Frontend

- [x] **3.1 Tạo màn danh sách**

Create: `hrm-client/pages/customer-care/serials/index.vue`

Bám nguyên khung `pages/customer-care/note-maintenances/index.vue` (mixin, watcher, phân trang,
dedupe), khác ở các điểm dưới. Phần script:

```js
const initialStateForm = {
    keyword: '',
    serial: '',
    product_name: '',
    customer_id: '',
    status: '',
    created_by: '',
    updated_by: '',
    sort_by: '',
    sort_desc: 'false',
}

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin, filterStateMixin, DedupeLoadMixin],
    head() {
        return { title: `${this.title}` }
    },
    components: {
        V2BaseButton,
        V2BaseFilterPanel,
        V2BaseDataTable,
        V2BaseLabel,
        V2BaseInput,
        V2BaseSelect,
        V2BaseSelectRemote,
    },
    data() {
        return {
            loading: false,
            title: 'Danh mục serial thiết bị làm dịch vụ',
            tableData: [],
            pagination: { currentPage: 1, pageSize: 10, total: 0, totalPages: 1, from: 0, to: 0 },
            filterCollapsed: true,
            filters: { ...initialStateForm },
            statusOptions: [
                { id: 1, name: 'Đang sử dụng' },
                { id: 2, name: 'Ngưng sử dụng' },
            ],
            creatorOptions: [],
            updaterOptions: [],
            ignoredFields: ['keyword'],
            oldFilters: {},
            filterFieldName: 'filters',
            localStorageKey: 'customer_care_serials',
            pathsToKeep: ['/customer-care/serials'],
            expirationTime: 10 * 60 * 1000,
        }
    },
    computed: {
        // Fail-closed: KHÔNG bao giờ gán literal true.
        canView() {
            return this.hasAPermission('Xem danh mục serial thiết bị làm dịch vụ')
        },
        pageTitle() {
            return this.title
        },
        /**
         * ⚠️ `key` cột sortable PHẢI trùng key trong `SerialService::SORT_FIELDS`,
         * lệch thì sort im lặng không chạy (mũi tên vẫn đổi).
         */
        tableColumns() {
            return [
                { key: 'index', title: 'STT', width: '60px', minWidth: '60px', sticky: true, align: 'left' },
                { key: 'serial', title: 'Serial thiết bị làm dịch vụ', sticky: true, align: 'left', sortable: true },
                { key: 'product_name', title: 'Tên hàng', align: 'left', cellClass: 'text-wrap', sortable: true },
                { key: 'customer_name', title: 'Khách hàng', align: 'left', cellClass: 'text-wrap', sortable: true },
                { key: 'status', title: 'Trạng thái', align: 'left', width: '150px', sortable: true },
                { key: 'created_by_name', title: 'Người tạo', align: 'left', width: '180px', sortable: true },
                { key: 'updated_by_name', title: 'Người cập nhật', align: 'left', width: '180px', sortable: true },
                { key: 'updated_at', title: 'Ngày cập nhật', align: 'left', width: '140px', sortable: true },
            ]
        },
    },
    async mounted() {
        const savedState = this.loadFilterState()
        if (savedState) {
            this.filters = { ...initialStateForm, ...savedState.filter }
            if (savedState.filterCollapsed !== undefined) {
                this.filterCollapsed = savedState.filterCollapsed
            }
        }
        const sortableKeys = this.tableColumns.filter((c) => c.sortable).map((c) => c.key)
        if (this.filters.sort_by && !sortableKeys.includes(this.filters.sort_by)) {
            this.filters.sort_by = ''
            this.filters.sort_desc = 'false'
        }
        this.oldFilters = JSON.parse(JSON.stringify(this.filters))
        await Promise.all([this.loadFilterOptions(), this.loadData()])
    },
    methods: {
        getNumericalOrder,

        buildParams(overrides = {}) {
            return {
                ...this.filters,
                page: this.pagination.currentPage,
                per_page: this.pagination.pageSize,
                ...overrides,
            }
        },

        async loadData() {
            const params = this.buildParams()
            if (this.isDuplicateLoad(params)) return

            try {
                this.loading = true
                const { data, meta } = await this.$store.dispatch(
                    'apiGetMethod',
                    `customer-care/serials${buildQueryString(params)}`
                )
                this.tableData = data
                // API trả per_page dạng CHUỖI -> phải ép Number, nếu không V2BaseDataTable gọi lại API.
                this.pagination.currentPage = Number(meta.current_page)
                this.pagination.pageSize = Number(meta.per_page)
                this.pagination.total = Number(meta.total)
                this.pagination.totalPages = Number(meta.last_page)
                this.pagination.from = Number(meta.from) || 0
                this.pagination.to = Number(meta.to) || 0
            } catch (error) {
                console.error('Error loading data:', error)
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
                }
            } finally {
                this.loading = false
            }
        },

        /** Dropdown Người tạo / Người cập nhật lấy từ chính bảng serials (đúng hệ id employees). */
        async loadFilterOptions() {
            try {
                const res = await this.$store.dispatch('apiGetMethod', 'customer-care/serials/filter-options')
                const payload = res?.data || res || {}
                this.creatorOptions = payload.created_by || []
                this.updaterOptions = payload.updated_by || []
            } catch (error) {
                console.error('Error loading filter options:', error)
            }
        },

        async fetchCustomers(keyword) {
            try {
                const kw = encodeURIComponent(keyword || '')
                const res = await this.$store.dispatch('apiGetMethod', `master-data/customers/search?q=${kw}`)
                const list = Array.isArray(res) ? res : res?.data || []
                return list.map((c) => ({
                    id: c.id,
                    text: c.text || (c.code ? `${c.code} - ${c.fullname}` : c.fullname),
                }))
            } catch (e) {
                return []
            }
        },

        async exportExcel() {
            try {
                this.$nuxt.$loading.start()
                await downloadExcel(
                    this.$axios,
                    `customer-care/serials/export${buildQueryString(
                        this.buildParams({ page: 1, per_page: 100000 })
                    )}`,
                    'danh_muc_serial_thiet_bi_lam_dich_vu.xlsx'
                )
                this.$toasted?.global?.success?.({ message: 'Xuất Excel thành công' })
            } catch (error) {
                console.error('Error exporting:', error)
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi xuất Excel' })
                }
            } finally {
                this.$nuxt.$loading.finish()
            }
        },
    },
}
```

Copy nguyên các method `toggleFilterPanel` / `handleQuickSearchChange` / `handleSearch` /
`handleReset` / `handleSort` / `handlePageChange` / `handlePageSizeChange` và deep watcher
`filters` từ `note-maintenances/index.vue` (không đổi gì).

Import bổ sung so với màn mẫu:

```js
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseSelectRemote from '@/components/V2BaseSelectRemote.vue'
```

Bỏ các import không dùng: `BaseConfirmModal`, `NoteMaintenanceModal`.

- [x] **3.2 Template màn danh sách**

6 bộ lọc trong `#advanced-filters`:

```html
<div class="form-row">
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Số serial</V2BaseLabel>
        <V2BaseInput v-model="filters.serial" placeholder="Nhập số serial" size="sm" />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Khách hàng</V2BaseLabel>
        <V2BaseSelectRemote
            v-model="filters.customer_id"
            :fetchFn="fetchCustomers"
            placeholder="Tất cả"
            size="sm"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Tên hàng</V2BaseLabel>
        <V2BaseInput v-model="filters.product_name" placeholder="Nhập tên hàng" size="sm" />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Trạng thái</V2BaseLabel>
        <V2BaseSelect v-model="filters.status" :options="statusOptions" placeholder="Tất cả" size="sm" />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Người tạo</V2BaseLabel>
        <V2BaseSelect v-model="filters.created_by" :options="creatorOptions" placeholder="Tất cả" size="sm" />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Người cập nhật</V2BaseLabel>
        <V2BaseSelect v-model="filters.updated_by" :options="updaterOptions" placeholder="Tất cả" size="sm" />
    </div>
</div>
```

⚠️ Mở `components/V2BaseSelect.vue` xác nhận tên prop danh sách (`options` / `items`) và cặp
`value-field`/`text-field` trước khi viết — dùng sai prop thì dropdown rỗng im lặng.

Bảng: `title="Danh mục serial thiết bị làm dịch vụ"`, `itemLabel="serial"`, **không có** cột
`actions`, `#actions-bottom` chỉ chứa 1 nút:

```html
<template #actions-bottom>
    <V2BaseButton secondary size="sm" class="btn-compact" @click="exportExcel">
        <template #prefix>
            <i class="ri-file-excel-2-line" style="font-size: 13px"></i>
        </template>
        Xuất Excel
    </V2BaseButton>
</template>
```

Slot cột:

```html
<template #cell-index="{ index }">
    {{ getNumericalOrder(pagination.currentPage, pagination.pageSize, index) }}
</template>
<template #cell-serial="{ item }">
    <div class="field-line font-weight-bold text-dark">{{ item.serial || '—' }}</div>
</template>
<template #cell-product_name="{ item }">
    <span class="field-line">{{ item.product_name || '—' }}</span>
</template>
<template #cell-customer_name="{ item }">
    <span class="field-line">{{ item.customer || '—' }}</span>
</template>
<template #cell-status="{ item }">
    <span :class="['status-pill', item.status === 1 ? 'tpl-status-active' : 'tpl-status-inactive']">
        {{ item.status_text }}
    </span>
</template>
<template #cell-created_by_name="{ item }">
    <span class="field-line">{{ item.created_by_name || '—' }}</span>
</template>
<template #cell-updated_by_name="{ item }">
    <span class="field-line">{{ item.updated_by_name || '—' }}</span>
</template>
<template #cell-updated_at="{ item }">
    <span class="field-line">{{ item.updated_at || '—' }}</span>
</template>
```

⚠️ Cột Khách hàng có `key = 'customer_name'` (để sort đúng cột DB) nhưng dữ liệu hiển thị nằm ở
field `customer` của resource — đúng như slot trên.

⚠️ Kiểm class `tpl-status-inactive` có tồn tại trong `assets/scss/v2-styles.scss` không; nếu
không, dùng class trạng thái ngưng đang dùng ở màn `costs`.

- [x] **3.3 Build FE không lỗi**

```bash
cd hrm-client
npx eslint pages/customer-care/serials/index.vue
```

Kỳ vọng: 0 error. Nếu dev server đang chạy, xác nhận `.nuxt/router.js` có mtime mới sau khi thêm
page (page mới không nhận là do Nuxt chưa rebuild → restart `npm run dev`).

---

## Phase 4 — Verify Backend (HTTP thật)

Lấy token bằng tài khoản có quyền 1126 vừa gán. Với mỗi case ghi lại kết quả vào bảng dưới.

- [x] **4.1 Danh sách + tổng số khớp DB**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "$API/api/v1/customer-care/serials?page=1&per_page=10"
```

Kỳ vọng: 200, `meta.total` = `SELECT COUNT(*) FROM serials` (đã ghi ở bước 0.2).

- [x] **4.2 Sáu bộ lọc, mỗi cái 1 case**

`serial=` (một serial có thật, cắt 3 ký tự) · `product_name=` · `customer_id=` · `status=1` ·
`status=2` · `created_by=` · `updated_by=`.
Mỗi case đối chiếu `meta.total` với `SELECT COUNT(*) FROM serials WHERE <điều kiện tương ứng>`.

- [x] **4.3 Sort đủ 7 cột**

Với mỗi `sort_by` ∈ {serial, product_name, customer_name, status, created_by_name,
updated_by_name, updated_at} × `sort_desc` ∈ {true, false} → 200 và thứ tự đổi đúng chiều.
Thử thêm 1 giá trị rác `sort_by=xxx` → phải rơi về mặc định `created_at desc`, không 500.

- [x] **4.4 `filter-options`**

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$API/api/v1/customer-care/serials/filter-options"
```

Kỳ vọng: 2 mảng `created_by` / `updated_by`, mỗi phần tử `{id, name}`; lấy 1 `id` bất kỳ dùng cho
case lọc ở 4.2 và phải ra > 0 dòng (nếu ra 0 → đang lệch hệ id, xem lại `employeeOptions`).

- [x] **4.5 Export**

```bash
curl -s -o serials.xlsx -w "%{http_code}" -H "Authorization: Bearer $TOKEN" \
  "$API/api/v1/customer-care/serials/export?status=1&page=1&per_page=100000"
```

Kỳ vọng: 200, file mở được. Đọc lại bằng PhpSpreadsheet: đủ **8 cột**, số dòng = `meta.total` của
cùng bộ lọc.

- [x] **4.6 Chặn quyền**

Không token → 401. Token của user **không** có quyền 1126 → 403 cho cả 3 route.

- [x] **4.7 Dữ liệu nguyên trạng**

```sql
SELECT COUNT(*), MAX(updated_at) FROM serials;
```

Phải **y hệt** kết quả ở bước 0.2 (màn read-only, không được ghi gì).

---

## Phase 5 — Verify Frontend

- [x] **5.1 Màn danh sách chạy**

Playwright: mở `/customer-care/serials`. Chờ hết "Đang tải dữ liệu" (dev server đơn luồng, màn
nặng ~15s). Kiểm:

- `window.$nuxt.$route.matched.length === 1`
- 0 request ≥ 400 trong network log
- Bảng render đủ 8 cột theo đúng thứ tự

Đọc state qua `window.$nuxt` thay vì `querySelector`.

- [x] **5.2 Bộ lọc + phân trang + sort trên UI**

Lần lượt: gõ serial → bấm Tìm kiếm; chọn 1 KH ở dropdown; chọn Trạng thái; chọn Người tạo;
đổi trang 2; đổi số dòng 25; bấm sort 2 cột.
Mỗi thao tác: đúng **1** request (không lặp), số dòng đổi đúng, không nhảy về trang 1 khi phân trang.

- [x] **5.3 Xuất Excel trên UI**

Bấm Xuất Excel sau khi đã lọc → file tải về, mở ra khớp bộ lọc đang áp dụng.

- [x] **5.4 Menu**

Sidebar CSKH hiện mục "Danh mục serial thiết bị làm dịch vụ" (không xám mờ), bấm vào ra đúng màn.
Với user không có quyền 1126 → mục biến mất và vào thẳng URL thì màn báo lỗi quyền, không trắng trang.

- [ ] **5.5 Đối chiếu ERP — CHƯA LÀM ĐƯỢC**

ERP local không chạy (cổng 8080 chỉ có trang mặc định Laragon, `/admin/serials` → 404).
Đã đối chiếu thay thế bằng **SQL trực tiếp trên cùng bảng `serials`** (nguồn duy nhất của cả 2 hệ)
— xem Phase 4, 9/9 case khớp. Cần user bật ERP local nếu muốn so bằng mắt 2 màn.

---

## Kết quả thực thi — 2026-08-06

### Số liệu dữ liệu (DB `gop_db` local)

`serials`: **21.632 dòng**. `status`: 1 → 21.427 · 2 → 192 · **3 → 12** · **0 → 1**.
`created_by`/`updated_by`: 0 dòng thiếu, 22 người tạo / 22 người cập nhật riêng biệt,
join `employees` → `employee_infos` khớp 100% (0 dòng không ra tên).

### Verify BE — 9/9 bộ lọc khớp SQL

| Case | API `meta.total` | SQL | Khớp |
| --- | --- | --- | --- |
| không lọc | 21632 | 21632 | ✅ |
| `status=1` | 21427 | 21427 | ✅ |
| `status=2` | 192 | 192 | ✅ |
| `serial=CPEO` | 7 | 7 | ✅ |
| `product_name=Cầu nâng` | 2244 | 2244 | ✅ |
| `created_by=242` | 23 | 23 | ✅ |
| `updated_by=242` | 21 | 21 | ✅ |
| `keyword=THACO` | 85 | 85 | ✅ |
| `customer_id=33601` | 1372 | 1372 | ✅ |

Sort: 7 cột × 2 chiều = 14 case đều đổi đúng thứ tự (kể cả 2 cột join `created_by_name`,
`updated_by_name`). `sort_by` giá trị rác → rơi về mặc định `created_at desc`, không 500.
`filter-options` → 22 + 22 mục dạng `{id, name}`.
Quyền: không token → 401; gỡ quyền 1126 khỏi role → **403** cả 3 route; gán lại → 200.
Export `status=2` → 200, 195 dòng (3 header + 192), 8 cột đúng thứ tự.
Dữ liệu nguyên trạng sau toàn bộ test: `COUNT=21632`, `MAX(updated_at)=2026-07-28 08:58:23`.

### Verify FE (Playwright)

`matched = 1`, 0 console error, **đúng 1 request/thao tác** (không lặp).
Đã chạy thật: lọc serial (7) · lọc trạng thái (192) · lọc người tạo + trạng thái (61, khớp SQL) ·
lọc khách hàng qua select2 remote (9, khớp SQL) · phân trang sang trang 2 (giữ nguyên bộ lọc,
`from/to` = 11/20) · sort cột Serial và cột Người tạo · nút Làm mới xóa sạch cả 4 select2 ·
Xuất Excel tải về đúng 12 dòng (3 header + 9) theo bộ lọc đang áp dụng ·
menu CSKH hiện link `/customer-care/serials`.

### Ghi nhận

- ⚠️ **`status` có 13 bản ghi ngoài 1/2** (12 dòng `status=3`, 1 dòng `status=0`). Đang giữ đúng
  hành vi ERP: hiển thị "Ngưng sử dụng", nhưng **bộ lọc "Ngưng sử dụng" gửi `status=2` nên không
  bắt được 13 dòng này** → tổng 2 lựa chọn lọc (21427 + 192) nhỏ hơn tổng bảng (21632).
  Cần user quyết có đổi thành `status != 1` không.
- ⏱ Xuất Excel **toàn bộ 21.632 dòng mất ~25 giây** (1 MB). Lọc trước rồi xuất thì nhanh
  (192 dòng ~4,5 giây). Chưa tối ưu vì ERP còn không có chức năng này.
- 📌 **4 danh mục CSKH port trước** (`levels`, `note-maintenances`, `costs`, `services`) **vẫn xuất
  Excel ở BE** — dữ liệu ít (29 / 11 / 524 dòng) nên chưa lộ, nhưng nên rà lại nếu bảng phình to.
  Không đụng trong feature này.
- 🔎 Dropdown Khách hàng dùng endpoint dùng chung `master-data/customers/search`, **tìm theo cụm
  nguyên chuỗi** (gõ "GREEN AUTO NAM" ra 0 dù có KH "…GREEN AUTO NAM ĐỊNH" trong snapshot serial).
  Hành vi có sẵn của endpoint, không thuộc màn này. Ngoài ra DB local thiếu một số KH mà bảng
  `serials` có snapshot tên → chọn KH đó sẽ ra 0 dòng, đúng dữ liệu local.
- Id quyền trong `PermissionsTableSeeder` và trong DB local **lệch nhau** với cụm CSKH cũ
  (seeder 1119-1124 vs DB 1115-1120) — lệch có sẵn từ các nhánh trước. Quyền mới **1126 trống ở
  cả hai** nên dùng được.
- `php artisan route:list` vẫn 500 do lỗi có sẵn `PermissionHelper:22` — kiểm route bằng
  `Route::getRoutes()` trong tinker.

---

## Phase 6 — Chuyển Xuất Excel từ BE sang FE (2026-08-06, user yêu cầu)

Lý do: bảng 21.632 dòng, BE dựng file mất ~25 giây trên máy local → **timeout khi lên server**.
Convention dự án cho màn nhiều dữ liệu là xuất ở FE bằng **ExcelJS + fetch theo lô**
(mẫu `components/export-excel/timesheet_details.vue`), xem [[feedback_fe_excel_export_convention]].

- [x] **6.1 FE tự dựng .xlsx**

Modify: `hrm-client/pages/customer-care/serials/index.vue`

- Thêm `import ExcelJS from 'exceljs'` + `import { saveAs } from 'file-saver'`, bỏ `downloadExcel`.
- `fetchAllPagesForExport()` gọi chính route `index` theo lô `EXPORT_CHUNK_SIZE = 5000`,
  lấy `meta.last_page` ở lô đầu để biết số vòng. **Không** gọi 1 phát `per_page = total`.
- `generateWorkbook(rows)` dựng 1 sheet: dòng tiêu đề gộp 8 cột + hàng header tô nền + 8 cột dữ
  liệu + viền + freeze 2 dòng đầu.
- Nút hiện tiến độ `Đang xuất... N%` và `:disabled="isExporting"` để chặn bấm trùng.

- [x] **6.2 Gỡ đường xuất ở BE (không để 2 đường song song)**

- Xóa `Route::get('/export', ...)` trong `Modules/CustomerCare/Routes/api.php`
- Xóa method `export()` + 4 `use` thừa (`SerialExport`, `Excel`, `Exception`, `Log`) trong
  `SerialController`
- Xóa hẳn `app/ExcelExport/SerialExport.php` và `resources/views/exports/serials.blade.php`
- `php artisan view:clear` (view đã compile còn trong `storage/framework/views`)

- [x] **6.3 Verify**

`php -l` 2 file sạch · `Route::getRoutes()` còn đúng 2 route · `GET .../serials/export` → **404** ·
không còn tham chiếu `SerialExport` / `exports.serials` trong code.
Playwright: bấm Xuất Excel với **toàn bộ 21.632 dòng** → nút chạy `Đang xuất... %`, xong sau
**14 giây**, file 21.634 dòng (2 header + 21.632), 8 cột, dòng cuối khớp DB.
(Lô 2000 mất 53 giây khi dev server đang HMR rebuild → chốt lô **5000**, ~2 giây/lô.)

---

## Checkpoint — 2026-08-06

Vừa hoàn thành: toàn bộ Phase 0-6 trừ 5.5. BE 5 file mới + 1 route group; FE 1 page + menu;
quyền 1126 (seeder + DB local + gán role 18). Verify BE 9/9 bộ lọc + 14 case sort + gate quyền;
verify FE bằng Playwright đủ lọc/phân trang/sort/export/menu.
Đang làm dở: không.
Xuất Excel đã chuyển hẳn sang FE (Phase 6), BE không còn route export.
Bước tiếp theo: user rà bằng mắt `/customer-care/serials`; chốt cách lọc cho 13 bản ghi
`status` 0/3; bật ERP local nếu muốn đối chiếu 2 màn (mục 5.5).
Blocked: không.
