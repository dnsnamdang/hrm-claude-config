# Yêu cầu điều chỉnh giải pháp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép KD tạo phiếu yêu cầu điều chỉnh giải pháp gửi TP/PM xử lý, hiển thị trong tab con "YCĐC GP" tại màn chi tiết Dự án TKT.

**Architecture:** Entity mới `solution_adjustment_requests` với 3 status (Đã gửi / Tiếp nhận / Từ chối). API nested dưới `/prospective-projects/{id}/solution-adjustment-requests`. FE: tab "Giải pháp" tách 2 tab con, tab mới chứa danh sách + popup tạo/xem.

**Tech Stack:** Laravel 8 (BE), Nuxt 2 / Vue 2 (FE), MySQL, Bootstrap-Vue

**Spec chi tiết:** `docs/superpowers/specs/2026-05-06-request-solution-adjustment-design.md`

---

## Phase 1: Backend — Migration + Entity

### Task 1: Migration

**Files:**
- Create: `hrm-api/Modules/Assign/Database/migrations/2026_05_06_000001_create_solution_adjustment_requests_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateSolutionAdjustmentRequestsTable extends Migration
{
    public function up()
    {
        Schema::create('solution_adjustment_requests', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('code')->unique();
            $table->unsignedBigInteger('prospective_project_id');
            $table->unsignedBigInteger('solution_id');
            $table->unsignedBigInteger('solution_version_id');
            $table->text('content');
            $table->tinyInteger('status')->default(1);
            $table->text('reject_reason')->nullable();
            $table->unsignedBigInteger('processed_by')->nullable();
            $table->timestamp('processed_at')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('solution_adjustment_requests');
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-api && php artisan migrate
```

Expected: Migration chạy thành công, bảng `solution_adjustment_requests` được tạo.

---

### Task 2: Entity Model

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/SolutionAdjustmentRequest.php`

- [ ] **Step 1: Tạo Model**

```php
<?php

namespace Modules\Assign\Entities;

use App\Models\BaseModel;
use App\Models\File;
use Modules\Timesheet\Entities\Employee;

class SolutionAdjustmentRequest extends BaseModel
{
    protected $table = 'solution_adjustment_requests';

    protected $fillable = [
        'code',
        'prospective_project_id',
        'solution_id',
        'solution_version_id',
        'content',
        'status',
        'reject_reason',
        'processed_by',
        'processed_at',
        'company_id',
        'department_id',
        'part_id',
        'created_by',
        'updated_by',
    ];

    const STATUS_DA_GUI = 1;
    const STATUS_TIEP_NHAN = 2;
    const STATUS_TU_CHOI = 3;

    const STATUSES = [
        ['id' => self::STATUS_DA_GUI, 'name' => 'Đã gửi', 'color' => 'primary'],
        ['id' => self::STATUS_TIEP_NHAN, 'name' => 'Tiếp nhận', 'color' => 'success'],
        ['id' => self::STATUS_TU_CHOI, 'name' => 'Từ chối', 'color' => 'danger'],
    ];

    public function prospectiveProject()
    {
        return $this->belongsTo(ProspectiveProject::class, 'prospective_project_id');
    }

    public function solution()
    {
        return $this->belongsTo(Solution::class, 'solution_id');
    }

    public function processedByEmployee()
    {
        return $this->belongsTo(Employee::class, 'processed_by');
    }

    public function files()
    {
        return $this->hasMany(File::class, 'table_id', 'id')
            ->where('table', 'solution_adjustment_requests');
    }

    public function getNextCode()
    {
        $maxId = static::max('id') ?? 0;
        return 'YCDCGP.' . str_pad($maxId + 1, 5, '0', STR_PAD_LEFT);
    }

    public function getStatusNameAttribute()
    {
        $status = collect(self::STATUSES)->firstWhere('id', $this->status);
        return $status ? $status['name'] : '';
    }

    public function getStatusColorAttribute()
    {
        $status = collect(self::STATUSES)->firstWhere('id', $this->status);
        return $status ? $status['color'] : '';
    }

    public function getIsCanAcceptAttribute()
    {
        if ($this->status != self::STATUS_DA_GUI) return false;
        return $this->isCurrentUserTPOrPM();
    }

    public function getIsCanRejectAttribute()
    {
        if ($this->status != self::STATUS_DA_GUI) return false;
        return $this->isCurrentUserTPOrPM();
    }

    private function isCurrentUserTPOrPM()
    {
        $userId = auth()->user()->id ?? null;
        if (!$userId) return false;

        // PM phụ trách GP
        if ($this->solution && $this->solution->pm_id == $userId) {
            return true;
        }

        // TP phòng nhận GP (dùng pattern departmentsManager từ Solution)
        if ($this->solution && $this->solution->requestSolution) {
            $manageDepartmentIds = Solution::departmentsManager();
            if (in_array($this->solution->requestSolution->receive_dept, $manageDepartmentIds)) {
                return true;
            }
        }

        return false;
    }
}
```

---

## Phase 2: Backend — Request Validation

### Task 3: Store Request

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Requests/StoreSolutionAdjustmentRequestRequest.php`

- [ ] **Step 1: Tạo FormRequest**

```php
<?php

namespace Modules\Assign\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;
use Modules\Assign\Entities\Solution;

class StoreSolutionAdjustmentRequestRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'solution_id' => 'required|exists:solutions,id',
            'content' => 'required|string',
        ];
    }

    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            $prospectiveProject = $this->route('prospectiveProject');
            $solution = Solution::find($this->solution_id);

            if (!$solution || $solution->prospective_project_id != $prospectiveProject->id) {
                $validator->errors()->add('solution_id', 'Giải pháp không thuộc dự án này.');
                return;
            }

            $allowedStatuses = [
                Solution::STATUS_DA_DUYET_GIAI_PHAP,
                Solution::STATUS_DA_DUYET_GIA,
                Solution::STATUS_CHO_LAM_GIA,
                Solution::STATUS_CHOT_GIAI_PHAP,
            ];
            if (!in_array($solution->status, $allowedStatuses)) {
                $validator->errors()->add('solution_id', 'Giải pháp chưa được duyệt, không thể tạo yêu cầu điều chỉnh.');
            }

            if ($prospectiveProject->created_by != auth()->user()->id) {
                $validator->errors()->add('solution_id', 'Chỉ người tạo dự án mới được tạo yêu cầu điều chỉnh.');
            }
        });
    }
}
```

---

### Task 4: Reject Request

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Requests/RejectSolutionAdjustmentRequestRequest.php`

- [ ] **Step 1: Tạo FormRequest**

```php
<?php

namespace Modules\Assign\Http\Requests;

use Modules\Training\Http\Requests\BaseRequest;

class RejectSolutionAdjustmentRequestRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'reject_reason' => 'required|string',
        ];
    }
}
```

---

## Phase 3: Backend — Service + Resource

### Task 5: Service

**Files:**
- Create: `hrm-api/Modules/Assign/Services/SolutionAdjustmentRequestService.php`

- [ ] **Step 1: Tạo Service**

```php
<?php

namespace Modules\Assign\Services;

use Modules\Training\Services\BaseService;
use Modules\Assign\Entities\SolutionAdjustmentRequest;
use Modules\Assign\Entities\Solution;
use Modules\Timesheet\Entities\Employee;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\EmployeeManageDepartment;
use Modules\Timesheet\Services\EmployeeInfoService;
use App\Helper\TableFileHelper;
use Illuminate\Support\Facades\Log;

class SolutionAdjustmentRequestService extends BaseService
{
    public function index($request, $prospectiveProject)
    {
        return SolutionAdjustmentRequest::query()
            ->where('prospective_project_id', $prospectiveProject->id)
            ->when($request->keyword, function ($query) use ($request) {
                $query->where('code', 'LIKE', '%' . $request->keyword . '%');
            })
            ->when($request->status, function ($query) use ($request) {
                $query->where('status', $request->status);
            })
            ->orderBy($request->sort_by ?? 'id', toBoolean($request->sort_desc) ? 'desc' : 'asc');
    }

    public function store($request, $prospectiveProject)
    {
        $solution = Solution::findOrFail($request->solution_id);

        $model = new SolutionAdjustmentRequest();
        $result = SolutionAdjustmentRequest::create([
            'code' => $model->getNextCode(),
            'prospective_project_id' => $prospectiveProject->id,
            'solution_id' => $solution->id,
            'solution_version_id' => $solution->current_version_id,
            'content' => $request->content,
            'status' => SolutionAdjustmentRequest::STATUS_DA_GUI,
        ]);

        if ($request->has('files')) {
            $files = $request->input('files', []);
            TableFileHelper::createForTable('solution_adjustment_requests', (int) $result->id, $files, auth()->id());
        }

        $this->sendNotification($result, $solution);

        return $result;
    }

    public function accept($solutionAdjustmentRequest)
    {
        $solutionAdjustmentRequest->update([
            'status' => SolutionAdjustmentRequest::STATUS_TIEP_NHAN,
            'processed_by' => auth()->user()->id,
            'processed_at' => now(),
        ]);

        return $solutionAdjustmentRequest;
    }

    public function reject($request, $solutionAdjustmentRequest)
    {
        $solutionAdjustmentRequest->update([
            'status' => SolutionAdjustmentRequest::STATUS_TU_CHOI,
            'reject_reason' => $request->reject_reason,
            'processed_by' => auth()->user()->id,
            'processed_at' => now(),
        ]);

        return $solutionAdjustmentRequest;
    }

    private function sendNotification($solutionAdjustmentRequest, $solution)
    {
        try {
            $employeeInfoIds = [];

            // PM phụ trách GP
            if ($solution->pm_id) {
                $pmEmployee = Employee::find($solution->pm_id);
                if ($pmEmployee && $pmEmployee->employee_info_id) {
                    $employeeInfoIds[] = $pmEmployee->employee_info_id;
                }
            }

            // TP phòng nhận GP
            if ($solution->requestSolution && $solution->requestSolution->receive_dept) {
                $deptId = $solution->requestSolution->receive_dept;
                $managerIds = EmployeeManageDepartment::where('department_id', $deptId)
                    ->pluck('employee_id')
                    ->toArray();

                foreach ($managerIds as $managerId) {
                    $manager = Employee::find($managerId);
                    if ($manager && $manager->employee_info_id) {
                        $employeeInfoIds[] = $manager->employee_info_id;
                    }
                }
            }

            $employeeInfoIds = array_values(array_unique($employeeInfoIds));
            if (empty($employeeInfoIds)) return;

            $data = [
                'url' => '/assign/prospective-projects/' . $solutionAdjustmentRequest->prospective_project_id,
                'title' => 'Yêu cầu điều chỉnh giải pháp mới',
                'content' => "Có yêu cầu điều chỉnh giải pháp: {$solutionAdjustmentRequest->code} - GP: {$solution->code} - {$solution->name}",
                'type' => 'solution_adjustment_request',
                'id' => $solutionAdjustmentRequest->id,
                'employeeInfo' => auth()->user()->employeeInfo ?? null,
            ];

            EmployeeInfoService::sendToAllNotification($employeeInfoIds, $data);
        } catch (\Exception $e) {
            Log::error("Lỗi gửi thông báo YCĐC GP: " . $e->getMessage());
        }
    }
}
```

---

### Task 6: Resource (List + Detail)

**Files:**
- Create: `hrm-api/Modules/Assign/Transformers/SolutionAdjustmentRequestResource.php`
- Create: `hrm-api/Modules/Assign/Transformers/DetailSolutionAdjustmentRequestResource.php`

- [ ] **Step 1: Tạo List Resource**

```php
<?php

namespace Modules\Assign\Transformers;

use Modules\Human\Transformers\ApiResource;

class SolutionAdjustmentRequestResource extends ApiResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'employee_create_name' => $this->employee_create_name,
            'created_at' => $this->created_at ? $this->created_at->format('d/m/Y') : '',
            'status' => $this->status,
            'status_name' => $this->status_name,
            'status_color' => $this->status_color,
            'is_can_accept' => $this->is_can_accept,
            'is_can_reject' => $this->is_can_reject,
        ];
    }
}
```

- [ ] **Step 2: Tạo Detail Resource**

```php
<?php

namespace Modules\Assign\Transformers;

use Modules\Human\Transformers\ApiResource;

class DetailSolutionAdjustmentRequestResource extends ApiResource
{
    public function toArray($request)
    {
        $solution = $this->solution;
        $solutionVersionText = $solution ? $solution->getVersionText() : '';

        return [
            'id' => $this->id,
            'code' => $this->code,
            'solution_id' => $this->solution_id,
            'solution_code' => $solution ? $solution->code : '',
            'solution_name' => $solution ? $solution->name : '',
            'solution_version' => $solutionVersionText,
            'content' => $this->content,
            'employee_create_name' => $this->employee_create_name,
            'created_at' => $this->created_at ? $this->created_at->format('d/m/Y') : '',
            'status' => $this->status,
            'status_name' => $this->status_name,
            'status_color' => $this->status_color,
            'reject_reason' => $this->reject_reason,
            'processed_by_name' => $this->processedByEmployee ? $this->processedByEmployee->name : '',
            'processed_at' => $this->processed_at ? date('d/m/Y', strtotime($this->processed_at)) : '',
            'files' => $this->files,
            'is_can_accept' => $this->is_can_accept,
            'is_can_reject' => $this->is_can_reject,
        ];
    }
}
```

---

## Phase 4: Backend — Controller + Routes

### Task 7: Controller

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/SolutionAdjustmentRequestController.php`

- [ ] **Step 1: Tạo Controller**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Response;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Exception;
use Modules\Assign\Entities\ProspectiveProject;
use Modules\Assign\Entities\SolutionAdjustmentRequest;
use Modules\Assign\Services\SolutionAdjustmentRequestService;
use Modules\Assign\Transformers\SolutionAdjustmentRequestResource;
use Modules\Assign\Transformers\DetailSolutionAdjustmentRequestResource;
use Modules\Assign\Http\Requests\StoreSolutionAdjustmentRequestRequest;
use Modules\Assign\Http\Requests\RejectSolutionAdjustmentRequestRequest;

class SolutionAdjustmentRequestController extends ApiController
{
    protected $service;

    public function __construct(SolutionAdjustmentRequestService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request, ProspectiveProject $prospectiveProject)
    {
        try {
            $result = $this->service->index($request, $prospectiveProject);
            return $this->apiGetList(SolutionAdjustmentRequestResource::apiPaginate($result, $request));
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function store(StoreSolutionAdjustmentRequestRequest $request, ProspectiveProject $prospectiveProject)
    {
        try {
            return DB::transaction(function () use ($request, $prospectiveProject) {
                $result = $this->service->store($request, $prospectiveProject);
                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show(ProspectiveProject $prospectiveProject, SolutionAdjustmentRequest $solutionAdjustmentRequest)
    {
        try {
            return $this->responseJson('success', Response::HTTP_OK, new DetailSolutionAdjustmentRequestResource($solutionAdjustmentRequest));
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function accept(ProspectiveProject $prospectiveProject, SolutionAdjustmentRequest $solutionAdjustmentRequest)
    {
        try {
            return DB::transaction(function () use ($solutionAdjustmentRequest) {
                $result = $this->service->accept($solutionAdjustmentRequest);
                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function reject(RejectSolutionAdjustmentRequestRequest $request, ProspectiveProject $prospectiveProject, SolutionAdjustmentRequest $solutionAdjustmentRequest)
    {
        try {
            return DB::transaction(function () use ($request, $solutionAdjustmentRequest) {
                $result = $this->service->reject($request, $solutionAdjustmentRequest);
                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
}
```

---

### Task 8: Routes

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php`

- [ ] **Step 1: Thêm route group**

Thêm block sau vào file `api.php`, đặt sau group `/assign/prospective-projects` hiện có (khoảng sau dòng 234):

```php
// Yêu cầu điều chỉnh giải pháp
Route::group(['prefix' => '/assign/prospective-projects/{prospectiveProject}/solution-adjustment-requests'], function () {
    Route::get('/', [SolutionAdjustmentRequestController::class, 'index']);
    Route::post('/', [SolutionAdjustmentRequestController::class, 'store']);
    Route::get('/{solutionAdjustmentRequest}', [SolutionAdjustmentRequestController::class, 'show']);
    Route::put('/{solutionAdjustmentRequest}/accept', [SolutionAdjustmentRequestController::class, 'accept']);
    Route::put('/{solutionAdjustmentRequest}/reject', [SolutionAdjustmentRequestController::class, 'reject']);
});
```

- [ ] **Step 2: Thêm import Controller**

Thêm vào đầu file `api.php`:

```php
use Modules\Assign\Http\Controllers\Api\V1\SolutionAdjustmentRequestController;
```

- [ ] **Step 3: Test API bằng Postman/curl**

```bash
# Test index (thay {projectId} bằng ID thực)
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/v1/assign/prospective-projects/{projectId}/solution-adjustment-requests
```

Expected: Response `{ code: 200, data: [], ... }` (danh sách rỗng).

---

## Phase 5: Frontend — Tab con + Danh sách

### Task 9: Tách tab "Giải pháp" thành 2 tab con

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/_id/manager.vue`

- [ ] **Step 1: Thêm import component mới**

Thêm vào phần import (sau dòng `import SolutionInfoTab ...`):

```javascript
import SolutionAdjustmentTab from '../../prospective-projects/components/SolutionAdjustmentTab.vue'
```

- [ ] **Step 2: Đăng ký component**

Thêm `SolutionAdjustmentTab` vào object `components: { ... }`.

- [ ] **Step 3: Thêm data cho sub-tab**

Thêm vào `data()`:

```javascript
solutionSubTab: 'info', // 'info' | 'adjustment'
```

- [ ] **Step 4: Sửa template tab "Giải pháp"**

Thay thế block `<div v-show="activeTab === 'solution-info'">` (dòng 69-72) bằng:

```html
<!-- TAB: GIẢI PHÁP (2 tab con) -->
<div v-show="activeTab === 'solution-info'">
    <b-tabs v-model="solutionSubTabIndex" content-class="mt-3" nav-class="mb-0">
        <b-tab title="Thông tin giải pháp" active>
            <SolutionInfoTab :solution-data="solutionData" />
        </b-tab>
        <b-tab title="Yêu cầu điều chỉnh GP">
            <SolutionAdjustmentTab
                v-if="solutionData.id"
                :project-id="$route.params.id"
                :solution-data="solutionData"
                :is-project-creator="isProjectCreator"
            />
            <div v-else class="empty-state-box">
                <i class="ri-lightbulb-line empty-state-icon"></i>
                <p class="empty-state-text">Dự án chưa có giải pháp tương ứng</p>
            </div>
        </b-tab>
    </b-tabs>
</div>
```

- [ ] **Step 5: Thêm computed `isProjectCreator`**

Thêm vào `computed`:

```javascript
isProjectCreator() {
    if (!this.project) return false
    const meId = this.$store.state.current_employee?.id
    if (!meId) return false
    return Number(this.project.created_by) === Number(meId)
},
```

- [ ] **Step 6: Thêm data `solutionSubTabIndex`**

Thêm vào `data()`:

```javascript
solutionSubTabIndex: 0,
```

---

### Task 10: Component danh sách YCĐC

**Files:**
- Create: `hrm-client/pages/assign/prospective-projects/components/SolutionAdjustmentTab.vue`

- [ ] **Step 1: Tạo component**

```vue
<template>
    <div class="v2-styles solution-adjustment-tab">
        <!-- Nút tạo -->
        <div class="d-flex justify-content-end mb-3" v-if="canCreate">
            <V2BaseButton variant="primary" size="sm" @click="openCreateModal">
                <i class="ri-add-line mr-1"></i> Tạo yêu cầu
            </V2BaseButton>
        </div>

        <!-- Danh sách -->
        <V2BaseDataTable
            :data="tableData"
            :columns="tableColumns"
            :pagination="pagination"
            :loading="loading"
            title="Yêu cầu điều chỉnh giải pháp"
            rowKey="id"
            itemLabel="yêu cầu"
            emptyText="Chưa có yêu cầu điều chỉnh giải pháp nào."
            @page-change="handlePageChange"
            @page-size-change="handlePageSizeChange"
        >
            <template #cell-index="{ index }">
                {{ getNumericalOrder(pagination.currentPage, pagination.pageSize, index) }}
            </template>

            <template #cell-code="{ item }">
                <span class="text-primary cursor-pointer" @click="openDetailModal(item)">
                    {{ item.code }}
                </span>
            </template>

            <template #cell-status="{ item }">
                <V2BaseBadge :color="item.status_color" :text="item.status_name" />
            </template>

            <template #cell-actions="{ item }">
                <div class="row-actions">
                    <button
                        class="btn btn-light border btn-sm mr-1"
                        v-b-tooltip.hover.top="'Xem chi tiết'"
                        @click="openDetailModal(item)"
                    >
                        <i class="ri-eye-line"></i>
                    </button>
                    <button
                        v-if="item.is_can_accept"
                        class="btn btn-success border btn-sm mr-1"
                        v-b-tooltip.hover.top="'Tiếp nhận'"
                        @click="confirmAccept(item)"
                    >
                        <i class="ri-check-line"></i>
                    </button>
                    <button
                        v-if="item.is_can_reject"
                        class="btn btn-danger border btn-sm"
                        v-b-tooltip.hover.top="'Từ chối'"
                        @click="openRejectModal(item)"
                    >
                        <i class="ri-close-line"></i>
                    </button>
                </div>
            </template>
        </V2BaseDataTable>

        <!-- Modal tạo yêu cầu -->
        <b-modal
            v-model="showCreateModal"
            title="Tạo yêu cầu điều chỉnh giải pháp"
            size="lg"
            no-close-on-backdrop
            @hidden="resetCreateForm"
        >
            <div class="form-group">
                <V2BaseLabel text="Giải pháp" />
                <V2BaseInput
                    :value="solutionDisplay"
                    disabled
                />
            </div>
            <div class="form-group">
                <V2BaseLabel text="Nội dung điều chỉnh" required />
                <textarea
                    v-model="createForm.content"
                    class="form-control"
                    rows="5"
                    placeholder="Nhập nội dung cần điều chỉnh..."
                ></textarea>
                <V2BaseError :error="formErrors.content" />
            </div>
            <div class="form-group">
                <V2BaseLabel text="File đính kèm" />
                <FileAttachmentTable
                    v-model="createForm.files"
                    :editable="true"
                />
            </div>
            <template #modal-footer>
                <V2BaseButton variant="secondary" @click="showCreateModal = false">Hủy</V2BaseButton>
                <V2BaseButton variant="primary" :isShowLoading="submitting" @click="submitCreate">
                    Gửi yêu cầu
                </V2BaseButton>
            </template>
        </b-modal>

        <!-- Modal xem chi tiết -->
        <b-modal
            v-model="showDetailModal"
            title="Chi tiết yêu cầu điều chỉnh giải pháp"
            size="lg"
            ok-only
            ok-title="Đóng"
        >
            <div class="form-group">
                <V2BaseLabel text="Mã yêu cầu" />
                <V2BaseInput :value="detailData.code" disabled />
            </div>
            <div class="form-group">
                <V2BaseLabel text="Giải pháp" />
                <V2BaseInput
                    :value="`${detailData.solution_code} - ${detailData.solution_name} (${detailData.solution_version})`"
                    disabled
                />
            </div>
            <div class="form-group">
                <V2BaseLabel text="Người yêu cầu" />
                <V2BaseInput :value="detailData.employee_create_name" disabled />
            </div>
            <div class="form-group">
                <V2BaseLabel text="Ngày gửi" />
                <V2BaseInput :value="detailData.created_at" disabled />
            </div>
            <div class="form-group">
                <V2BaseLabel text="Trạng thái" />
                <div>
                    <V2BaseBadge :color="detailData.status_color" :text="detailData.status_name" />
                </div>
            </div>
            <div class="form-group">
                <V2BaseLabel text="Nội dung điều chỉnh" />
                <textarea
                    :value="detailData.content"
                    class="form-control"
                    rows="5"
                    disabled
                ></textarea>
            </div>
            <div v-if="detailData.status === 3" class="form-group">
                <V2BaseLabel text="Lý do từ chối" />
                <textarea
                    :value="detailData.reject_reason"
                    class="form-control"
                    rows="3"
                    disabled
                ></textarea>
            </div>
            <div v-if="detailData.processed_by_name" class="form-group">
                <V2BaseLabel text="Người xử lý" />
                <V2BaseInput :value="`${detailData.processed_by_name} — ${detailData.processed_at}`" disabled />
            </div>
            <div v-if="detailData.files && detailData.files.length" class="form-group">
                <V2BaseLabel text="File đính kèm" />
                <FileAttachmentTable
                    :value="detailData.files"
                    :editable="false"
                />
            </div>
        </b-modal>

        <!-- Modal từ chối -->
        <b-modal
            v-model="showRejectModal"
            title="Từ chối yêu cầu điều chỉnh"
            size="md"
            no-close-on-backdrop
            @hidden="resetRejectForm"
        >
            <div class="form-group">
                <V2BaseLabel text="Lý do từ chối" required />
                <textarea
                    v-model="rejectForm.reject_reason"
                    class="form-control"
                    rows="4"
                    placeholder="Nhập lý do từ chối..."
                ></textarea>
                <V2BaseError :error="rejectErrors.reject_reason" />
            </div>
            <template #modal-footer>
                <V2BaseButton variant="secondary" @click="showRejectModal = false">Hủy</V2BaseButton>
                <V2BaseButton variant="danger" :isShowLoading="submitting" @click="submitReject">
                    Từ chối
                </V2BaseButton>
            </template>
        </b-modal>

        <!-- Confirm tiếp nhận -->
        <BaseConfirmModal
            :id="'confirm-accept-adjustment'"
            :message="'Bạn có chắc muốn tiếp nhận yêu cầu điều chỉnh này?'"
            @confirm="submitAccept"
        />
    </div>
</template>

<script>
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseError from '@/components/V2BaseError.vue'
import FileAttachmentTable from '@/components/FileAttachmentTable.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import { getNumericalOrder } from '@/utils/common.js'
import { buildQuery } from '@/utils/url-action'

export default {
    name: 'SolutionAdjustmentTab',
    components: {
        V2BaseDataTable,
        V2BaseButton,
        V2BaseBadge,
        V2BaseLabel,
        V2BaseInput,
        V2BaseError,
        FileAttachmentTable,
        BaseConfirmModal,
    },
    props: {
        projectId: { type: [String, Number], required: true },
        solutionData: { type: Object, default: () => ({}) },
        isProjectCreator: { type: Boolean, default: false },
    },
    data() {
        return {
            loading: false,
            submitting: false,
            tableData: [],
            pagination: {
                currentPage: 1,
                pageSize: 20,
                total: 0,
            },

            // Create
            showCreateModal: false,
            createForm: { content: '', files: [] },
            formErrors: {},

            // Detail
            showDetailModal: false,
            detailData: {},

            // Reject
            showRejectModal: false,
            rejectForm: { reject_reason: '' },
            rejectErrors: {},
            selectedItem: null,
        }
    },
    computed: {
        canCreate() {
            if (!this.isProjectCreator) return false
            if (!this.solutionData || !this.solutionData.id) return false
            const allowedStatuses = [11, 13, 15, 17]
            return allowedStatuses.includes(Number(this.solutionData.status))
        },
        solutionDisplay() {
            if (!this.solutionData) return ''
            const version = this.solutionData.current_version_code
                ? ` (V${this.solutionData.current_version_code})`
                : ''
            return `${this.solutionData.code || ''} - ${this.solutionData.name || ''}${version}`
        },
        tableColumns() {
            return [
                { key: 'index', label: 'STT', width: '60px' },
                { key: 'code', label: 'Mã yêu cầu' },
                { key: 'employee_create_name', label: 'Người yêu cầu' },
                { key: 'created_at', label: 'Ngày gửi', width: '120px' },
                { key: 'status', label: 'Trạng thái', width: '120px' },
                { key: 'actions', label: 'Hành động', width: '140px' },
            ]
        },
        baseUrl() {
            return `assign/prospective-projects/${this.projectId}/solution-adjustment-requests`
        },
    },
    mounted() {
        this.loadData()
    },
    methods: {
        getNumericalOrder,

        async loadData() {
            this.loading = true
            try {
                const params = buildQuery({
                    page: this.pagination.currentPage,
                    per_page: this.pagination.pageSize,
                })
                const res = await this.$store.dispatch('apiGetMethod', `${this.baseUrl}?${params}`)
                this.tableData = res.data || []
                if (res.meta) {
                    this.pagination.total = res.meta.total || 0
                    this.pagination.currentPage = res.meta.current_page || 1
                }
            } catch (error) {
                this.$toasted?.global?.error?.({ message: 'Không thể tải danh sách yêu cầu điều chỉnh' })
            } finally {
                this.loading = false
            }
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

        // === Tạo ===
        openCreateModal() {
            this.createForm = { content: '', files: [] }
            this.formErrors = {}
            this.showCreateModal = true
        },
        resetCreateForm() {
            this.createForm = { content: '', files: [] }
            this.formErrors = {}
        },
        async submitCreate() {
            this.formErrors = {}
            if (!this.createForm.content || !this.createForm.content.trim()) {
                this.formErrors.content = 'Nội dung điều chỉnh không được để trống'
                return
            }

            this.submitting = true
            try {
                const payload = {
                    solution_id: this.solutionData.id,
                    content: this.createForm.content,
                    files: this.createForm.files || [],
                }
                await this.$store.dispatch('apiPostMethod', {
                    url: this.baseUrl,
                    payload,
                })
                this.$toasted?.global?.success?.({ message: 'Gửi yêu cầu điều chỉnh thành công' })
                this.showCreateModal = false
                this.loadData()
            } catch (error) {
                if (error?.response?.data?.errors) {
                    this.formErrors = error.response.data.errors
                } else {
                    this.$toasted?.global?.error?.({ message: 'Có lỗi xảy ra, vui lòng thử lại' })
                }
            } finally {
                this.submitting = false
            }
        },

        // === Chi tiết ===
        async openDetailModal(item) {
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', `${this.baseUrl}/${item.id}`)
                this.detailData = data || {}
                this.showDetailModal = true
            } catch (error) {
                this.$toasted?.global?.error?.({ message: 'Không thể tải chi tiết yêu cầu' })
            }
        },

        // === Tiếp nhận ===
        confirmAccept(item) {
            this.selectedItem = item
            this.$bvModal.show('confirm-accept-adjustment')
        },
        async submitAccept() {
            if (!this.selectedItem) return
            this.submitting = true
            try {
                await this.$store.dispatch('apiPutMethod', {
                    url: `${this.baseUrl}/${this.selectedItem.id}/accept`,
                })
                this.$toasted?.global?.success?.({ message: 'Đã tiếp nhận yêu cầu điều chỉnh' })
                this.loadData()
            } catch (error) {
                this.$toasted?.global?.error?.({ message: 'Có lỗi xảy ra, vui lòng thử lại' })
            } finally {
                this.submitting = false
            }
        },

        // === Từ chối ===
        openRejectModal(item) {
            this.selectedItem = item
            this.rejectForm = { reject_reason: '' }
            this.rejectErrors = {}
            this.showRejectModal = true
        },
        resetRejectForm() {
            this.rejectForm = { reject_reason: '' }
            this.rejectErrors = {}
            this.selectedItem = null
        },
        async submitReject() {
            this.rejectErrors = {}
            if (!this.rejectForm.reject_reason || !this.rejectForm.reject_reason.trim()) {
                this.rejectErrors.reject_reason = 'Lý do từ chối không được để trống'
                return
            }

            this.submitting = true
            try {
                await this.$store.dispatch('apiPutMethod', {
                    url: `${this.baseUrl}/${this.selectedItem.id}/reject`,
                    payload: { reject_reason: this.rejectForm.reject_reason },
                })
                this.$toasted?.global?.success?.({ message: 'Đã từ chối yêu cầu điều chỉnh' })
                this.showRejectModal = false
                this.loadData()
            } catch (error) {
                if (error?.response?.data?.errors) {
                    this.rejectErrors = error.response.data.errors
                } else {
                    this.$toasted?.global?.error?.({ message: 'Có lỗi xảy ra, vui lòng thử lại' })
                }
            } finally {
                this.submitting = false
            }
        },
    },
}
</script>
```

---

## Phase 5B: FE — Tab YCĐC trên màn Solution manager (TP/PM)

### Task 10B: Thêm tab YC Điều chỉnh vào /assign/solutions/:id

**Files:**
- Modify: `hrm-client/pages/assign/solutions/_id/manager.vue`
- Modify: `hrm-api/Modules/Assign/Services/SolutionAdjustmentRequestService.php` (notification URL)

- [x] **Step 1: Import SolutionAdjustmentTab**
- [x] **Step 2: Thêm tab `{ key: 'adjustment-requests', label: 'YC Điều chỉnh', icon: 'ri-edit-2-line' }`**
- [x] **Step 3: Thêm template với `is-project-creator="false"` (TP/PM không tạo yêu cầu)**
- [x] **Step 4: Sửa notification URL → `/assign/solutions/{solutionId}?active_tab=adjustment-requests`**

---

## Phase 5C: Fix UI theo feedback

### Task 10C: Các fix đã áp dụng

- [x] V2BaseDataTable: đổi `label` → `title` cho column headers
- [x] V2BaseBadge: đổi `:text` → slot content, STATUSES dùng hex color
- [x] V2BaseButton: đổi `variant` → boolean props (`primary`/`light`), thêm `status="danger"` cho Từ chối
- [x] Bỏ bộ lọc (V2BaseFilterPanel) — màn này ít dữ liệu
- [x] Bỏ cột Hành động — click mã yêu cầu mở popup chi tiết, Tiếp nhận/Từ chối trong popup
- [x] Button pattern theo FinalizeSolutionModal: primary action + #prefix icon trước, light "Đóng" sau
- [x] `isProjectCreator` dùng `main_sale_employee_id` thay vì `created_by`
- [x] BE validation cũng dùng `main_sale_employee_id`

---

## Phase 6: Test thủ công

### Task 11: Test toàn bộ flow

- [ ] **Step 1: Đăng nhập bằng tài khoản KD (người tạo dự án)**
- [ ] **Step 2: Vào Dự án TKT có GP đã duyệt → Tab "Giải pháp"**

Expected: Hiện 2 tab con "Thông tin giải pháp" và "Yêu cầu điều chỉnh GP".

- [ ] **Step 3: Bấm tab "Yêu cầu điều chỉnh GP"**

Expected: Danh sách rỗng, hiện nút "Tạo yêu cầu".

- [ ] **Step 4: Bấm "Tạo yêu cầu" → điền nội dung → "Gửi yêu cầu"**

Expected: Toast "Gửi yêu cầu điều chỉnh thành công", danh sách hiện 1 dòng với mã YCDCGP.00001, status "Đã gửi".

- [ ] **Step 5: Bấm mã yêu cầu → xem chi tiết**

Expected: Popup hiện đầy đủ thông tin: mã, GP, người yêu cầu, ngày gửi, nội dung, trạng thái.

- [ ] **Step 6: Đăng nhập bằng tài khoản TP/PM → vào cùng dự án → tab YCĐC**

Expected: Danh sách hiện phiếu vừa tạo, có nút Tiếp nhận + Từ chối.

- [ ] **Step 7: Bấm "Tiếp nhận"**

Expected: Confirm → toast thành công, status chuyển "Tiếp nhận" (badge xanh).

- [ ] **Step 8: Tạo phiếu mới → bấm "Từ chối" → nhập lý do**

Expected: Toast thành công, status "Từ chối" (badge đỏ). Xem chi tiết hiện lý do từ chối + người xử lý.

- [ ] **Step 9: Kiểm tra notification**

Expected: TP/PM nhận được notification khi KD tạo phiếu mới.

- [ ] **Step 10: Đăng nhập user khác (không phải KD tạo dự án)**

Expected: Tab YCĐC hiện danh sách nhưng KHÔNG hiện nút "Tạo yêu cầu".

---

## Checkpoint

### Checkpoint — 2026-05-06 (2)
Vừa hoàn thành: Phase 1-5 + 5B + 5C code DONE. BE: 8 files mới + sửa api.php + fix notification URL. FE: 1 file mới (SolutionAdjustmentTab.vue) + sửa 2 file (prospective-projects manager.vue + solutions manager.vue). Nhiều vòng fix UI theo feedback.
Đang làm dở: Chưa test
Bước tiếp theo: Chạy migration (`php artisan migrate`) + test thủ công theo Phase 6
Blocked:
