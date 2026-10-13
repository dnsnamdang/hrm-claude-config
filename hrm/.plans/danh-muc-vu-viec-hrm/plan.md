# Danh mục Vụ việc (HRM) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port danh mục "Vụ việc" (bảng `works`) từ ERP sang HRM dưới dạng CRUD trong `Modules/Finance`, menu ở phân hệ Tài chính, FE V2Base.

**Architecture:** BE Laravel module `Modules/Finance` (Entity `Work` trên connection mặc định đọc bảng `works` trong DB gộp; Service + Controller + Request + Resource + routes `/v1/finance/works`). FE Nuxt2 V2Base: menu phân hệ Tài chính + trang list (`V2BaseFilterPanel` + `V2BaseDataTable`) + modal thêm/sửa; gọi API qua action generic `apiGetMethod/apiPostMethod/apiPutMethod/apiDeleteMethod`. Không tạo bảng/migration mới, không đụng code ERP.

**Tech Stack:** PHP 7.4 / Laravel 8 (nwidart modules) / MySQL (DB gộp) / spatie-permission; Nuxt 2 (Vue 2) + Bootstrap-Vue + V2Base components.

**Spec:** `docs/superpowers/specs/2026-07-31-danh-muc-vu-viec-hrm-design.md`

## Global Constraints

- Nhánh `gop_db` cho CẢ `hrm-api` và `hrm-client`. (Hiện cả 2 repo đang ở `gop_db`.)
- **DB verify:** mọi kiểm thử BE phải chạy trên **DB đã gộp** (có sẵn bảng `works`, `account_details`, `employees`/`employee_infos`). `.env` hrm-api mặc định trỏ `hrm_pro` (PROD, KHÔNG có bảng `works`) → phải trỏ tạm DB gộp (vd `erp_hrm_check` local hoặc DB gộp trên server) trước khi test. Không có test harness tự động cho module → verify bằng `php artisan route:list` / tinker / curl / browser.
- Bảng `works` dùng chung với hạch toán ERP → **KHÔNG** thêm cột, **KHÔNG** migration, **KHÔNG** SoftDeletes. Xóa cứng, luôn qua `canDelete()`.
- Danh mục **toàn cục** — không `company_id`, không phân cấp.
- **2 quyền:** `Xem danh mục vụ việc`, `Quản lý danh mục vụ việc`. Route thao tác (store/update/destroy) gắn `->middleware('checkPermission:Quản lý danh mục vụ việc')`.
- **Rule xóa/khóa y hệt ERP:** đã có `account_details.work_id` trỏ tới → không xóa, không chuyển status=2.
- Validate: BE để `FormRequest` tự **rethrow ValidationException** (KHÔNG catch chung `Exception`) → 422 `{message, errors}`. FE hiện lỗi inline từng field (viền đỏ `is-invalid` + text), dùng cờ `touched` (chỉ hiện sau submit đầu).
- Toàn bộ text tiếng Việt.
- **KHÔNG commit/push** khi user chưa yêu cầu (quy tắc dự án). Mỗi task kết thúc bằng verify, không auto-commit.
- URL API cuối cùng: `/api/v1/finance/works` (FE gọi path `finance/works`).

---

### Task 1: BE — Entity `Work` + `WorkService` (tầng dữ liệu)

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/Work.php`
- Create: `hrm-api/Modules/Finance/Services/WorkService.php`

**Interfaces:**
- Produces:
  - `Work` (Eloquent, `$table='works'`, connection mặc định) với `canDelete(): bool`.
  - `WorkService::getWorks(Request $request): LengthAwarePaginator` (mỗi item có `created_by_name`).
  - `WorkService::createWork(array $attrs): Work`
  - `WorkService::updateWork(int $id, array $attrs): Work|null`
  - `WorkService::deleteWork(int $id): bool` (chỉ xóa khi `canDelete()`, ngược lại `false`)
  - `WorkService::hasAccounting(int $id): bool`

- [ ] **Step 1: Tạo Entity `Work`**

`hrm-api/Modules/Finance/Entities/Work.php`:
```php
<?php

namespace Modules\Finance\Entities;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;

class Work extends Model
{
    protected $table = 'works';

    protected $fillable = [
        'code', 'name', 'note', 'status', 'created_by', 'updated_by',
    ];

    /**
     * Không xóa/khóa được nếu vụ việc đã phát sinh hạch toán (account_details.work_id).
     */
    public function canDelete(): bool
    {
        return !DB::table('account_details')->where('work_id', $this->id)->exists();
    }
}
```

- [ ] **Step 2: Tạo `WorkService`**

`hrm-api/Modules/Finance/Services/WorkService.php`:
```php
<?php

namespace Modules\Finance\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\Work;

class WorkService
{
    public function getWorks(Request $request)
    {
        $limit = (int) $request->get('per_page', 10);

        $query = Work::query()
            ->leftJoin('employees', 'employees.id', '=', 'works.created_by')
            ->leftJoin('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
            ->select('works.*', 'employee_infos.fullname as created_by_name');

        if ($request->filled('code')) {
            $query->where('works.code', 'like', '%' . $request->get('code') . '%');
        }
        if ($request->filled('name')) {
            $query->where('works.name', 'like', '%' . $request->get('name') . '%');
        }
        if ($request->filled('keyword')) {
            $kw = $request->get('keyword');
            $query->where(function ($q) use ($kw) {
                $q->where('works.code', 'like', "%$kw%")
                  ->orWhere('works.name', 'like', "%$kw%");
            });
        }
        if ($request->filled('status')) {
            $query->where('works.status', $request->get('status'));
        }

        return $query->orderBy('works.created_at', 'desc')->paginate($limit);
    }

    public function createWork(array $attrs): Work
    {
        return Work::create([
            'code' => $attrs['code'],
            'name' => $attrs['name'],
            'note' => $attrs['note'] ?? null,
            'status' => $attrs['status'] ?? '1',
            'created_by' => auth()->id(),
        ]);
    }

    public function updateWork(int $id, array $attrs)
    {
        $work = Work::find($id);
        if (!$work) {
            return null;
        }
        $work->code = $attrs['code'];
        $work->name = $attrs['name'];
        $work->note = $attrs['note'] ?? null;
        // Y hệt ERP: chỉ cho khóa (status=2) khi CHƯA phát sinh hạch toán.
        if (($attrs['status'] ?? null) == 2 && $work->canDelete()) {
            $work->status = 2;
        } elseif (($attrs['status'] ?? null) == 1) {
            $work->status = 1;
        }
        $work->updated_by = auth()->id();
        $work->save();

        return $work;
    }

    public function deleteWork(int $id): bool
    {
        $work = Work::find($id);
        if (!$work || !$work->canDelete()) {
            return false;
        }
        return (bool) $work->delete();
    }

    public function hasAccounting(int $id): bool
    {
        return DB::table('account_details')->where('work_id', $id)->exists();
    }
}
```

- [ ] **Step 3: Verify bằng tinker (trên DB gộp)**

Chạy trong `hrm-api/` (sau khi trỏ `.env` DB sang schema gộp):
```bash
php artisan tinker --execute='
echo "works count = ".\Modules\Finance\Entities\Work::count()."\n";
$w = \Modules\Finance\Entities\Work::first();
echo "first work: id={$w->id} code={$w->code} canDelete=".($w->canDelete()?"1":"0")."\n";
'
```
Expected: in ra số dòng `works` (≈21) và 1 vụ việc mẫu + cờ canDelete. Không lỗi class/bảng.

---

### Task 2: BE — API layer (Controller + Request + Resource + Routes)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/ApiController.php` (base nhỏ, `responseJson`)
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/WorkController.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/WorkRequest.php`
- Create: `hrm-api/Modules/Finance/Transformers/WorkResource/WorkListResource.php`
- Create: `hrm-api/Modules/Finance/Transformers/WorkResource/WorkDetailResource.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm route vào group `/v1/finance` sẵn có)

**Interfaces:**
- Consumes: `WorkService` (Task 1).
- Produces: endpoints
  - `GET /api/v1/finance/works` → `{ code, message, data:[...], total, lastPage, currentPage, perPage }`
  - `POST /api/v1/finance/works`
  - `PUT /api/v1/finance/works/{id}`
  - `DELETE /api/v1/finance/works/{id}`
  - `GET /api/v1/finance/works/{id}/check-has-accounting` → `{ data: { has_accounting: bool } }`

- [ ] **Step 1: Base controller `ApiController`**

`hrm-api/Modules/Finance/Http/Controllers/V1/ApiController.php`:
```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Routing\Controller as BaseController;

class ApiController extends BaseController
{
    protected function responseJson($message, $code = 200, $data = null)
    {
        return response()->json([
            'code' => $code,
            'message' => $message,
            'data' => $data,
        ], $code);
    }
}
```

- [ ] **Step 2: Request `WorkRequest` (dùng chung create/update, unique-ignore theo route id)**

`hrm-api/Modules/Finance/Http/Requests/WorkRequest.php`:
```php
<?php

namespace Modules\Finance\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class WorkRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $id = $this->route('id'); // null khi tạo mới, id khi cập nhật
        return [
            'code' => 'required|unique:works,code,' . $id,
            'name' => 'required',
        ];
    }

    public function messages(): array
    {
        return [
            'code.required' => 'Bắt buộc phải nhập',
            'code.unique' => 'Mã vụ việc đã tồn tại',
            'name.required' => 'Bắt buộc phải nhập',
        ];
    }
}
```
> `FormRequest` mặc định ném `ValidationException` khi fail → HTTP 422 `{message, errors:{field:[...]}}`. KHÔNG bọc try/catch.

- [ ] **Step 3: Resources**

`hrm-api/Modules/Finance/Transformers/WorkResource/WorkListResource.php`:
```php
<?php

namespace Modules\Finance\Transformers\WorkResource;

use Illuminate\Http\Resources\Json\ResourceCollection;

class WorkListResource extends ResourceCollection
{
    public function toArray($request): array
    {
        $page = (int) $request->get('page', 1);
        $limit = (int) $request->get('per_page', 10);

        $result = [];
        foreach ($this->collection as $index => $w) {
            $result[] = [
                'stt' => ($page - 1) * $limit + 1 + $index,
                'id' => $w->id,
                'code' => $w->code,
                'name' => $w->name,
                'note' => $w->note,
                'status' => (string) $w->status,
                'status_text' => (string) $w->status === '1' ? 'Hoạt động' : 'Khóa',
                'created_by_name' => $w->created_by_name ?? null,
                'created_at' => $w->created_at ? $w->created_at->format('d/m/Y') : null,
                'is_can_delete' => $w->canDelete(),
            ];
        }
        return $result;
    }
}
```

`hrm-api/Modules/Finance/Transformers/WorkResource/WorkDetailResource.php`:
```php
<?php

namespace Modules\Finance\Transformers\WorkResource;

use Illuminate\Http\Resources\Json\JsonResource;

class WorkDetailResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'note' => $this->note,
            'status' => (string) $this->status,
            'is_can_delete' => $this->canDelete(),
        ];
    }
}
```

- [ ] **Step 4: `WorkController`**

`hrm-api/Modules/Finance/Http/Controllers/V1/WorkController.php`:
```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Modules\Finance\Http\Requests\WorkRequest;
use Modules\Finance\Services\WorkService;
use Modules\Finance\Transformers\WorkResource\WorkDetailResource;
use Modules\Finance\Transformers\WorkResource\WorkListResource;

class WorkController extends ApiController
{
    private $workService;

    public function __construct(WorkService $workService)
    {
        $this->workService = $workService;
    }

    public function index(Request $request)
    {
        $works = $this->workService->getWorks($request);

        return (new WorkListResource($works))->additional([
            'total' => $works->total(),
            'lastPage' => $works->lastPage(),
            'currentPage' => $works->currentPage(),
            'perPage' => (int) $works->perPage(),
        ]);
    }

    public function store(WorkRequest $request)
    {
        $work = $this->workService->createWork($request->all());
        return new WorkDetailResource($work);
    }

    public function update(WorkRequest $request, $id)
    {
        $work = $this->workService->updateWork((int) $id, $request->all());
        if (!$work) {
            return $this->responseJson('Không tìm thấy vụ việc', 404);
        }
        return new WorkDetailResource($work);
    }

    public function destroy($id)
    {
        $ok = $this->workService->deleteWork((int) $id);
        if (!$ok) {
            return $this->responseJson('Vụ việc đã phát sinh hạch toán, không thể xóa', Response::HTTP_BAD_REQUEST);
        }
        return $this->responseJson('Xóa vụ việc thành công', 200);
    }

    public function checkHasAccounting($id)
    {
        return $this->responseJson('success', 200, [
            'has_accounting' => $this->workService->hasAccounting((int) $id),
        ]);
    }
}
```

- [ ] **Step 5: Routes**

Sửa `hrm-api/Modules/Finance/Routes/api.php` — thay group rỗng bằng:
```php
<?php

use Illuminate\Support\Facades\Route;
use Modules\Finance\Http\Controllers\V1\WorkController;

Route::group(['prefix' => '/v1/finance', 'middleware' => 'auth:api'], function () {
    Route::group(['prefix' => 'works'], function () {
        Route::get('/', [WorkController::class, 'index'])->middleware('checkPermission:Xem danh mục vụ việc');
        Route::post('/', [WorkController::class, 'store'])->middleware('checkPermission:Quản lý danh mục vụ việc');
        Route::put('/{id}', [WorkController::class, 'update'])->middleware('checkPermission:Quản lý danh mục vụ việc');
        Route::delete('/{id}', [WorkController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục vụ việc');
        Route::get('/{id}/check-has-accounting', [WorkController::class, 'checkHasAccounting'])->middleware('checkPermission:Xem danh mục vụ việc');
    });
});
```

- [ ] **Step 6: Verify route + lint**

```bash
cd hrm-api
php -l Modules/Finance/Entities/Work.php
php -l Modules/Finance/Services/WorkService.php
php -l Modules/Finance/Http/Controllers/V1/ApiController.php
php -l Modules/Finance/Http/Controllers/V1/WorkController.php
php -l Modules/Finance/Http/Requests/WorkRequest.php
php artisan route:list --path=finance/works
```
Expected: `php -l` tất cả "No syntax errors"; `route:list` liệt kê đủ 5 route `api/v1/finance/works...` kèm middleware `checkPermission`.

- [ ] **Step 7: Verify hành vi qua tinker (không cần HTTP/token)**

```bash
php artisan tinker --execute='
$req = new \Illuminate\Http\Request();
$s = new \Modules\Finance\Services\WorkService();
$p = $s->getWorks($req);
echo "total=".$p->total().", first created_by_name=".optional($p->first())->created_by_name."\n";
'
```
Expected: total ≈ 21, có `created_by_name` (hoặc null nếu created_by rỗng). Không lỗi cột ambiguous.

---

### Task 3: BE — Permission (seeder + áp non-destructive)

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

**Interfaces:**
- Produces 2 permission `name`: `Xem danh mục vụ việc`, `Quản lý danh mục vụ việc` (guard `api`), group `Danh mục vụ việc`, `type` = phân hệ Tài chính.

- [ ] **Step 1: Xác định `type` của phân hệ Tài chính đang dùng**

Các phân hệ Tài chính đã build trước (Sổ NKC, Bảng kê mã phí) có thể đã dùng 1 `type`. Tìm:
```bash
cd hrm-api
grep -nE "nhật ký chung|mã phí|Tài chính|finance" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
grep -oE "'type' => [0-9]+" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort -u
```
Quy tắc: nếu đã có permission Tài chính với `type = N` → **dùng lại N**. Nếu chưa có type nào cho Tài chính → dùng số type kế tiếp chưa dùng (max hiện có + 1) và ghi vào checkpoint để FE map tab phân quyền. (Ghi rõ số type đã chọn vào checkpoint.)

- [ ] **Step 2: Thêm 2 permission vào seeder**

Thêm 2 dòng vào cụm khai báo (chọn `id` chưa dùng — kiểm bằng `grep "'id' =>" ... | sort -t'>' -k2 -n | tail`), với `<TYPE>` từ Step 1:
```php
Permission::create(['id' => <ID1>, 'guard_name' => 'api', 'name' => 'Xem danh mục vụ việc', 'display_name' => 'Xem', 'group' => 'Danh mục vụ việc', 'type' => <TYPE>]);
Permission::create(['id' => <ID2>, 'guard_name' => 'api', 'name' => 'Quản lý danh mục vụ việc', 'display_name' => 'Quản lý', 'group' => 'Danh mục vụ việc', 'type' => <TYPE>]);
```

- [ ] **Step 3: Áp permission lên DB gộp KHÔNG destructive (KHÔNG chạy full seeder — nó `truncate hrm_permissions`)**

```bash
php artisan tinker --execute='
use App\Models\Permission;
Permission::firstOrCreate(["name" => "Xem danh mục vụ việc", "guard_name" => "api"], ["display_name" => "Xem", "group" => "Danh mục vụ việc", "type" => <TYPE>]);
Permission::firstOrCreate(["name" => "Quản lý danh mục vụ việc", "guard_name" => "api"], ["display_name" => "Quản lý", "group" => "Danh mục vụ việc", "type" => <TYPE>]);
echo Permission::whereIn("name", ["Xem danh mục vụ việc","Quản lý danh mục vụ việc"])->count()." permissions\n";
'
```
Expected: `2 permissions`. Sau đó gán 2 quyền cho role admin/test user (qua màn Phân quyền hoặc tinker `->givePermissionTo`).

- [ ] **Step 4: Verify chặn quyền**

Gọi `GET /api/v1/finance/works` bằng user KHÔNG có quyền → 403; user CÓ quyền `Xem danh mục vụ việc` → 200. (Test kỹ ở Task 5 khi có FE, hoặc curl với JWT.)

---

### Task 4: FE — Menu phân hệ Tài chính

**Files:**
- Create: `hrm-client/components/subsystem-menu/finance.js`
- Modify: `hrm-client/components/subsystems.js` (import + đổi `menu`)

**Interfaces:**
- Consumes: quyền `Xem danh mục vụ việc` (gate `isShow`).
- Produces: item menu link `/finance/works` dưới phân hệ Tài chính.

- [ ] **Step 1: Tạo file menu**

`hrm-client/components/subsystem-menu/finance.js`:
```js
export const financeItems = [
    {
        label: 'Tổng quan',
        icon: 'ri-dashboard-line',
        link: '/finance/dashboard',
        isShow: true,
    },
    {
        label: 'Danh mục - kế toán',
        icon: 'ri-list-check-2',
        isMenuCollapsed: false,
        subItems: [
            {
                label: 'Danh mục vụ việc',
                link: '/finance/works',
                isShow: ['Xem danh mục vụ việc', 'Quản lý danh mục vụ việc'],
            },
        ],
    },
]
```

- [ ] **Step 2: Wire vào `subsystems.js`**

Thêm import (cạnh các import subsystem-menu, ~dòng 20):
```js
import { financeItems } from '@/components/subsystem-menu/finance'
```
Trong block `key: 'finance'` (~dòng 327) đổi:
```js
        menu: dashboardOnlyMenu('finance'),
```
thành:
```js
        menu: financeItems,
```

- [ ] **Step 3: Verify**

`cd hrm-client && npm run dev` (hoặc build hiện có), đăng nhập user có quyền → vào phân hệ **Tài chính** → thấy nhóm "Danh mục - kế toán" › "Danh mục vụ việc". User không có quyền → item ẩn.
Expected: menu hiện đúng theo quyền, link tới `/finance/works`.

---

### Task 5: FE — Trang danh sách `pages/finance/works/index.vue`

**Files:**
- Create: `hrm-client/pages/finance/works/index.vue`

**Interfaces:**
- Consumes: API `GET finance/works` (Task 2), quyền `Quản lý danh mục vụ việc`, component `WorkModal` (Task 6).
- Produces: trang list có filter (keyword + status), bảng, phân trang; nút "Thêm" + "Sửa"/"Xóa" mở/gọi modal.

> **QUAN TRỌNG:** trước khi viết, ĐỌC file mẫu chuẩn `hrm-client/pages/assign/attachment-type/index.vue` để lấy đúng tên prop/slot của `V2BaseFilterPanel`/`V2BaseDataTable` phiên bản hiện hành. Nếu prop/slot khác code dưới đây (viết theo mẫu attachment-type), bám theo file mẫu.

- [ ] **Step 1: Tạo trang list**

`hrm-client/pages/finance/works/index.vue`:
```vue
<template>
  <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
    <div class="container-fluid">
      <V2BaseFilterPanel
        title="Bộ lọc danh mục vụ việc"
        :collapsed="filterCollapsed"
        :quickSearchValue="filters.keyword"
        quickSearchPlaceholder="Tìm theo mã, tên vụ việc"
        :filters="filters"
        @toggle-panel="filterCollapsed = !filterCollapsed"
        @quick-search-change="(v) => (filters.keyword = v)"
        @search="handleSearch"
        @reset="handleReset"
      >
        <template #advanced-filters="{ collapsed }">
          <div v-show="!collapsed" class="row">
            <div class="col-md-3">
              <V2BaseLabel>Trạng thái</V2BaseLabel>
              <V2BaseSelect v-model="filters.status" :options="statusFilterOptions" size="sm" />
            </div>
          </div>
        </template>
      </V2BaseFilterPanel>

      <V2BaseDataTable
        :data="tableData"
        :columns="tableColumns"
        :pagination="pagination"
        :loading="loading"
        title="Danh sách vụ việc"
        rowKey="id"
        itemLabel="vụ việc"
        emptyText="Không có dữ liệu phù hợp bộ lọc."
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #actions-bottom>
          <V2BaseButton v-if="canManage" primary size="sm" @click="openCreate">Thêm vụ việc</V2BaseButton>
        </template>
        <template #cell-index="{ index }">
          {{ (pagination.currentPage - 1) * pagination.pageSize + index + 1 }}
        </template>
        <template #cell-status="{ row }">
          <V2BaseBadge :variant="row.status === '1' ? 'success' : 'danger'">
            {{ row.status_text }}
          </V2BaseBadge>
        </template>
        <template #cell-actions="{ row }">
          <V2BaseIconButton icon="ri-pencil-line" title="Sửa" @click="openEdit(row)" />
          <V2BaseIconButton
            v-if="canManage && row.is_can_delete"
            icon="ri-delete-bin-line"
            title="Xóa"
            @click="openDelete(row)"
          />
        </template>
      </V2BaseDataTable>

      <WorkModal ref="workModal" @saved="loadData" />

      <BaseConfirmModal
        ref="confirmDelete"
        title="Xóa vụ việc"
        :message="`Bạn có chắc muốn xóa vụ việc &quot;${(itemToDelete || {}).name || ''}&quot;?`"
        @confirm="handleConfirmDelete"
      />
    </div>
  </div>
</template>

<script>
import V2BaseFilterPanel from '@/components/V2BaseFilterPanel.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import CheckPermission from '@/utils/mixins/CheckPermission'
import filterStateMixin from '@/utils/mixins/filterStateMixin.js'
import { buildQueryString } from '@/utils/url-action'
import WorkModal from './WorkModal.vue'

const initialStateForm = { keyword: undefined, status: undefined }

export default {
  layout: 'default-sidebar',
  mixins: [PageTitleMixin, CheckPermission, filterStateMixin],
  components: {
    V2BaseFilterPanel, V2BaseDataTable, V2BaseSelect, V2BaseLabel,
    V2BaseButton, V2BaseBadge, V2BaseIconButton, BaseConfirmModal, WorkModal,
  },
  data() {
    return {
      loading: false,
      tableData: [],
      pagination: { currentPage: 1, pageSize: 10, total: 0, totalPages: 1, from: 0, to: 0 },
      filterCollapsed: true,
      filters: { ...initialStateForm },
      ignoredFields: ['keyword'],
      oldFilters: {},
      itemToDelete: null,
      statusFilterOptions: [
        { id: undefined, name: 'Tất cả' },
        { id: '1', name: 'Hoạt động' },
        { id: '2', name: 'Khóa' },
      ],
      // filterStateMixin
      filterFieldName: 'filters',
      localStorageKey: 'finance_works',
      pathsToKeep: ['/finance/works'],
      expirationTime: 10 * 60 * 1000,
    }
  },
  computed: {
    canManage() {
      return this.hasAPermission('Quản lý danh mục vụ việc')
    },
    tableColumns() {
      return [
        { key: 'index', title: 'STT', sticky: true, align: 'left' },
        { key: 'code', title: 'Mã vụ việc', sticky: true, align: 'left' },
        { key: 'name', title: 'Tên vụ việc', align: 'left', cellClass: 'text-wrap' },
        { key: 'note', title: 'Ghi chú', align: 'left', cellClass: 'text-wrap' },
        { key: 'status', title: 'Trạng thái', align: 'left' },
        { key: 'created_by_name', title: 'Người tạo', align: 'left' },
        { key: 'created_at', title: 'Ngày tạo', align: 'left' },
        { key: 'actions', title: 'Thao tác', align: 'center' },
      ]
    },
  },
  created() {
    this.oldFilters = JSON.parse(JSON.stringify(this.filters))
  },
  watch: {
    filters: {
      handler(newVal) {
        const shouldCallApi = !this.ignoredFields.some((f) => newVal[f] !== this.oldFilters[f])
        if (shouldCallApi) {
          this.pagination.currentPage = 1
          this.loadData()
        }
        this.oldFilters = JSON.parse(JSON.stringify(this.filters))
      },
      deep: true,
    },
  },
  mounted() {
    const savedState = this.loadFilterState()
    if (savedState) {
      this.filters = { ...initialStateForm, ...savedState.filter }
      if (savedState.filterCollapsed !== undefined) this.filterCollapsed = savedState.filterCollapsed
    }
    this.oldFilters = JSON.parse(JSON.stringify(this.filters))
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const apiFilters = {
          page: this.pagination.currentPage,
          per_page: this.pagination.pageSize,
          status: this.filters.status,
        }
        if (this.filters.keyword) apiFilters.keyword = this.filters.keyword

        const res = await this.$store.dispatch('apiGetMethod', `finance/works${buildQueryString(apiFilters)}`)
        this.tableData = res.data || []
        Object.assign(this.pagination, {
          currentPage: res.currentPage || 1,
          pageSize: res.perPage || 10,
          total: res.total || 0,
          totalPages: res.lastPage || 1,
        })
      } catch (error) {
        if (error?.response?.status !== 403) {
          this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
        }
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.filters = { ...initialStateForm }
    },
    handlePageChange(page) {
      this.pagination.currentPage = page
      this.loadData()
    },
    handlePageSizeChange(size) {
      this.pagination.pageSize = size
      this.pagination.currentPage = 1
      this.loadData()
    },
    openCreate() {
      this.$refs.workModal.open(null)
    },
    openEdit(row) {
      this.$refs.workModal.open(row.id)
    },
    openDelete(row) {
      this.itemToDelete = row
      this.$refs.confirmDelete.show()
    },
    async handleConfirmDelete() {
      try {
        await this.$store.dispatch('apiDeleteMethod', `finance/works/${this.itemToDelete.id}`)
        this.$toasted?.global?.success?.({ message: 'Đã xóa thành công' })
        this.loadData()
      } catch (error) {
        if (error?.response?.status !== 403) {
          this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Xóa thất bại' })
        }
      }
    },
  },
}
</script>

<style lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

- [ ] **Step 2: Verify browser**

Vào `/finance/works`: bảng load danh sách vụ việc; gõ keyword → tự search; đổi trạng thái → tự lọc; phân trang chạy; nút "Thêm vụ việc" chỉ hiện khi có quyền Quản lý; nút Xóa chỉ hiện khi `is_can_delete`.

---

### Task 6: FE — Modal thêm/sửa `pages/finance/works/WorkModal.vue`

**Files:**
- Create: `hrm-client/pages/finance/works/WorkModal.vue`

**Interfaces:**
- Consumes: API `POST/PUT finance/works`, `GET finance/works/{id}/check-has-accounting` (Task 2).
- Produces: `open(id)` (id=null → tạo mới; id → sửa); emit `saved` khi lưu thành công.

> Tham chiếu mẫu modal chuẩn: `hrm-client/pages/assign/attachment-type/AddAttachmentTypeModal.vue` (bắt 422 → `formError`). Code dưới bổ sung cờ `touched` client-side theo CLAUDE.md.

- [ ] **Step 1: Tạo modal**

`hrm-client/pages/finance/works/WorkModal.vue`:
```vue
<template>
  <b-modal id="finance-work-modal" ref="modal" hide-footer size="lg" @hide="reset">
    <template #modal-header>
      <h5 class="modal-title mb-0">{{ id ? 'Sửa vụ việc' : 'Thêm vụ việc' }}</h5>
    </template>

    <div class="modal-body">
      <div class="mb-2">
        <V2BaseLabel>Mã vụ việc <span class="text-danger">*</span></V2BaseLabel>
        <V2BaseInput v-model="form.code" size="sm" placeholder="VD: VV001" :class="{ 'is-invalid': touched && formError.code }" />
        <div v-if="touched && formError.code" class="text-small-error mt-1">
          <i class="ri-error-warning-line mr-1"></i>{{ formError.code }}
        </div>
      </div>

      <div class="mb-2">
        <V2BaseLabel>Tên vụ việc <span class="text-danger">*</span></V2BaseLabel>
        <V2BaseInput v-model="form.name" size="sm" :class="{ 'is-invalid': touched && formError.name }" />
        <div v-if="touched && formError.name" class="text-small-error mt-1">
          <i class="ri-error-warning-line mr-1"></i>{{ formError.name }}
        </div>
      </div>

      <div class="mb-2">
        <V2BaseLabel>Trạng thái</V2BaseLabel>
        <V2BaseSelectInModal v-model="form.status" :options="statusOptions" :allowClear="false" size="sm" :disabled="lockDisabled" />
        <div v-if="lockDisabled" class="text-small-hint mt-1">Vụ việc đã phát sinh hạch toán, không thể khóa.</div>
      </div>

      <div class="mb-2">
        <V2BaseLabel>Ghi chú</V2BaseLabel>
        <V2BaseTextarea v-model="form.note" rows="3" size="sm" />
      </div>
    </div>

    <div class="modal-footer">
      <V2BaseButton primary :disabled="submitting" @click="submit">Lưu</V2BaseButton>
      <V2BaseButton light @click="$refs.modal.hide()">Đóng</V2BaseButton>
    </div>
  </b-modal>
</template>

<script>
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseTextarea from '@/components/V2BaseTextarea.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'

export default {
  components: { V2BaseLabel, V2BaseInput, V2BaseTextarea, V2BaseSelectInModal, V2BaseButton },
  data() {
    return {
      id: null,
      form: { code: '', name: '', note: '', status: '1' },
      formError: {},
      touched: false,
      submitting: false,
      hasAccounting: false,
      statusOptions: [
        { id: '1', name: 'Hoạt động' },
        { id: '2', name: 'Khóa' },
      ],
    }
  },
  computed: {
    // Đã dùng hạch toán → không cho khóa (khớp rule BE updateWork)
    lockDisabled() {
      return !!this.id && this.hasAccounting
    },
  },
  methods: {
    async open(id) {
      this.reset()
      this.id = id
      if (id) await this.loadDetail(id)
      this.$refs.modal.show()
    },
    reset() {
      this.id = null
      this.form = { code: '', name: '', note: '', status: '1' }
      this.formError = {}
      this.touched = false
      this.hasAccounting = false
    },
    async loadDetail(id) {
      const res = await this.$store.dispatch('apiGetMethod', `finance/works/${id}`)
      const d = res.data || res
      this.form = { code: d.code || '', name: d.name || '', note: d.note || '', status: String(d.status || '1') }
      const acc = await this.$store.dispatch('apiGetMethod', `finance/works/${id}/check-has-accounting`)
      this.hasAccounting = !!(acc.data && acc.data.has_accounting)
    },
    validateLocal() {
      const e = {}
      if (!this.form.code || !this.form.code.trim()) e.code = 'Bắt buộc phải nhập'
      if (!this.form.name || !this.form.name.trim()) e.name = 'Bắt buộc phải nhập'
      this.formError = e
      return Object.keys(e).length === 0
    },
    async submit() {
      this.touched = true
      if (!this.validateLocal()) return
      this.submitting = true
      try {
        const payload = {
          code: this.form.code.trim(),
          name: this.form.name.trim(),
          note: (this.form.note || '').trim(),
          status: this.form.status,
        }
        if (this.id) {
          await this.$store.dispatch('apiPutMethod', { url: `finance/works/${this.id}`, payload })
        } else {
          await this.$store.dispatch('apiPostMethod', { url: 'finance/works', payload })
        }
        this.$toasted?.global?.success?.({ message: this.id ? 'Cập nhật thành công' : 'Thêm mới thành công' })
        this.$emit('saved')
        this.$refs.modal.hide()
      } catch (error) {
        const code = Number(error?.response?.status)
        if (code === 422) {
          const errs = error.response.data.errors || {}
          // Laravel 422: errors.field = [msg] → lấy msg đầu
          this.formError = Object.keys(errs).reduce((a, k) => {
            a[k] = Array.isArray(errs[k]) ? errs[k][0] : errs[k]
            return a
          }, {})
        } else if (code !== 403) {
          this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Thao tác thất bại' })
        }
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>

<style scoped>
.text-small-error { color: #dc3545; font-size: 12px; }
.text-small-hint { color: #6c757d; font-size: 12px; }
</style>
```

- [ ] **Step 2: Verify browser (end-to-end)**

- Thêm mới: bỏ trống Mã/Tên rồi Lưu → hiện lỗi inline đỏ (touched). Nhập đủ → lưu, list refresh.
- Mã trùng → BE 422 → lỗi inline "Mã vụ việc đã tồn tại".
- Sửa 1 vụ việc **chưa** dùng hạch toán: đổi trạng thái sang Khóa được.
- Sửa 1 vụ việc **đã** dùng hạch toán (`check-has-accounting=true`): option Khóa disabled + hint; nút Xóa ẩn ở list.
- Xóa vụ việc chưa dùng: confirm → xóa thành công.

---

### Task 7: FE — Thêm tab phân hệ "Tài chính" (type 8) vào màn Phân quyền

**Files:**
- Modify: `hrm-client/components/setting/Permission.vue`

**Bối cảnh:** màn Phân quyền render mỗi phân hệ là 1 accordion hard-code `accordion-1..7` gọi `filterPermission(N)` (N = `type`). Quyền type 8 (vụ việc) hiện không có tab → không gán được qua UI. Cần thêm accordion thứ 8 "Tài chính".

- [ ] **Step 1:** Đọc block accordion-7 (khoảng dòng 396→ hết block, trước khi mở block kế/đóng container) làm mẫu. Xác nhận `filterPermission(N)` lọc theo `permission.type == N`.
- [ ] **Step 2:** Copy nguyên block accordion-7 thành block mới đặt NGAY SAU block 7: đổi `accordion-7`→`accordion-8` (mọi chỗ: `v-b-toggle.accordion-8`, `id="accordion-8"`), đổi `filterPermission(7)`→`filterPermission(8)`, đổi nhãn header phân hệ thành **"Tài chính"**. Giữ nguyên cấu trúc/class còn lại.
- [ ] **Step 3:** Verify đọc lại: có đúng 1 block `accordion-8` + `filterPermission(8)` + nhãn "Tài chính"; không phá block 1-7. (Không lint được do eslint version mismatch — verify bằng đọc + browser sau.)

## Verify tổng thể (sau tất cả task)

- `php artisan route:list --path=finance` đủ 5 route + middleware.
- Đăng nhập user có quyền → menu Tài chính › Danh mục - kế toán › Danh mục vụ việc → CRUD đầy đủ.
- User thiếu quyền `Quản lý...` → không thấy nút Thêm/Sửa/Xóa và API store/update/destroy trả 403.
- Không thay đổi cấu trúc bảng `works`; ERP (nếu chạy trên cùng DB gộp) vẫn đọc bình thường.

## Checkpoint — 2026-07-31 (CODE DONE, no-commit)
Vừa hoàn thành: cả 6 task qua subagent-driven (mỗi task implementer + reviewer), no-commit.
- Task 1: Work.php + WorkService.php (php -l sạch)
- Task 2: ApiController/WorkController/WorkRequest/WorkListResource/WorkDetailResource + Routes/api.php — FIX Critical: thêm `'middleware'=>'auth:api'` group /v1/finance
- Task 3: 2 permission (id 1107/1108, type=8) vào PermissionsTableSeeder (CHƯA áp DB)
- Task 4: components/subsystem-menu/finance.js + subsystems.js (menu: financeItems)
- Task 5: pages/finance/works/index.vue (chỉnh 5 điểm khớp V2Base thật)
- Task 6: pages/finance/works/WorkModal.vue (chỉnh 4 điểm khớp component thật)
- Task 7: Permission.vue — thêm accordion "Tài chính" (type 8) → quyền vụ việc gán được qua UI Phân quyền
Nhất quán chuỗi quyền + path /api/v1/finance/works: đã verify.
Đang làm dở: (không) — CHƯA commit, CHƯA verify runtime.
Bước tiếp theo (user, trên môi trường DB gộp): (1) áp 2 permission qua tinker firstOrCreate; (2) gán quyền cho role qua UI Phân quyền tab "Tài chính" (hoặc tinker givePermissionTo); (3) verify BE `php artisan route:list --path=finance/works`; (4) `yarn dev` verify FE end-to-end; (5) commit khi OK.
Quyết định đã chốt: phân hệ Tài chính = type 8 MỚI (không có type Tài chính sẵn) → đã thêm tab type 8 vào Permission.vue.
Blocked:

---

## Bugfix — 405 khi bấm Sửa (finance/works/{id})

**Triệu chứng:** bấm Sửa → `GET /api/v1/finance/works/28` trả **405 Method Not Allowed**.
**Root cause:** WorkModal.vue (loadDetail) gọi `GET finance/works/{id}` nhưng route group `works` chỉ có index/store/`PUT {id}`/`DELETE {id}`/check-has-accounting — **thiếu `GET /{id}` (show)** → URI tồn tại cho PUT/DELETE nhưng không có GET → 405.
**Fix (BE-only):**
- [x] `WorkService::getWork(int $id)` = `Work::find($id)`.
- [x] `WorkController::show($id)` trả `WorkDetailResource` (404 nếu không thấy).
- [x] Route `GET works/{id}` → show, middleware `checkPermission:Quản lý danh mục vụ việc` (đặt sau `/{id}/check-has-accounting`, khác segment nên không xung đột).
- [x] Verified: route đăng ký, show(28) trả {id,code,name,note,status,is_can_delete}. FE không đổi.

## Bổ sung — filter Người lập/Người cập nhật + cột Người/Ngày cập nhật (finance/works)
**BE (WorkService::getWorks):** join thêm `employees as u_emp`/`employee_infos as u_info` cho updated_by → select `u_info.fullname as updated_by_name`; thêm filter `created_by`, `updated_by` (where works.created_by/updated_by = id). **WorkListResource:** thêm `updated_by_name`, `updated_at` (d/m/Y).
**FE (finance/works/index.vue):** initialStateForm thêm created_by/updated_by; 2 filter V2BaseSelect "Người lập"/"Người cập nhật" dùng `$store.state.employeeOptions` (id=employees.id, khớp works.created_by/updated_by) + allowClear; apiFilters gửi created_by/updated_by; tableColumns thêm cột "Người cập nhật" (updated_by_name) + "Ngày cập nhật" (updated_at).
**Verified:** tinker list trả field mới, filter created_by/updated_by giảm số dòng; lint BE + compile FE OK.
