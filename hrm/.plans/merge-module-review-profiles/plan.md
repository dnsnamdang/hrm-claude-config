# Gộp hồ sơ trình duyệt hạng mục vào tab Hồ sơ giải pháp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gộp hồ sơ trình duyệt hạng mục vào bảng chung trên tab Hồ sơ của trang quản lý giải pháp, để PM duyệt tất cả tại một nơi.

**Architecture:** Mở rộng API `getSolutionReviewProfiles` để query thêm `solution_module_review_profiles` qua các `solution_modules` thuộc giải pháp, merge 2 collection → sort → paginate thủ công. Frontend thêm 3 filter + 2 cột vào bảng hiện tại, tạo `ModuleApprovalViewModal` mới cho xem + duyệt hồ sơ hạng mục.

**Tech Stack:** PHP 7.4 / Laravel 8 (BE), Nuxt 2 / Vue 2 (FE)

**Spec:** `docs/superpowers/specs/2026-04-25-merge-module-review-profiles-design.md`

---

## Phase 1: Backend — Mở rộng API review-profiles

### Task 1: Mở rộng `getSolutionReviewProfiles()` — thêm query hồ sơ hạng mục

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionService.php:1715-1832`

- [ ] **Step 1: Tách logic transform hồ sơ giải pháp thành private method**

Tách block map ở dòng 1769-1818 thành method riêng để tái sử dụng pattern transform. Thêm method mới:

```php
/**
 * Transform 1 SolutionReviewProfile thành array response.
 */
private function transformSolutionReviewProfile(SolutionReviewProfile $profile): array
{
    return [
        'id' => $profile->id,
        'type' => 'solution',
        'solution_id' => $profile->solution_id,
        'module_id' => null,
        'module_name' => null,
        'solution_version_id' => $profile->solution_version_id,
        'solution_version_code' => \Modules\Assign\Entities\Solution::formatVersionCode($profile->solution_version_code),
        'module_version_code' => null,
        'version_display' => \Modules\Assign\Entities\Solution::formatVersionCode($profile->solution_version_code),
        'profile_code' => $profile->code,
        'status' => $profile->status,
        'status_name' => SolutionReviewProfile::getStatusName($profile->status),
        'status_color' => SolutionReviewProfile::getStatusColor($profile->status),
        'start_date' => optional($profile->start_date)->format('d/m/Y'),
        'start_date_raw' => optional($profile->start_date)->format('Y-m-d'),
        'sent_date' => optional($profile->sent_date)->format('d/m/Y'),
        'sent_date_raw' => optional($profile->sent_date)->format('Y-m-d'),
        'review_deadline' => optional($profile->review_deadline)->format('d/m/Y'),
        'review_deadline_raw' => optional($profile->review_deadline)->format('Y-m-d'),
        'dept_head_id' => $profile->dept_head_id,
        'content' => $profile->content,
        'reason_deny' => $profile->reason_deny,
        'created_at' => $profile->created_at,
        'updated_at' => $profile->updated_at,
        'created_by' => $profile->created_by,
        'updated_by' => $profile->updated_by,
        'files' => $profile->files->map(function ($file) {
            return [
                'id' => $file->id,
                'name' => $file->name,
                'attachment_type_id' => $file->attachment_type_id,
                'employee_id' => $file->employee_id,
                'file_name' => $file->file_name,
                'file_path' => $file->file_path,
                'file_size' => $file->file_size,
                'file_type' => $file->file_type,
            ];
        })->values(),
        'bom_lists' => $profile->bomLists->map(function ($bom) {
            $employee = $bom->createdByEmployee;
            return [
                'id' => $bom->id,
                'code' => $bom->code,
                'name' => $bom->name,
                'created_by_code' => optional($employee)->code ?? '',
                'created_by_name' => $employee && $employee->info ? $employee->info->fullname : '',
                'created_at' => $bom->created_at ? $bom->created_at->format('d/m/Y') : null,
            ];
        })->values(),
    ];
}
```

- [ ] **Step 2: Thêm private method transform hồ sơ hạng m��c**

```php
/**
 * Transform 1 SolutionModuleReviewProfile thành array response.
 */
private function transformModuleReviewProfile(SolutionModuleReviewProfile $profile, Solution $solution): array
{
    $module = $profile->solutionModule;
    $moduleVersionCode = $profile->module_version_code ?? null;

    return [
        'id' => $profile->id,
        'type' => 'module',
        'solution_id' => $solution->id,
        'module_id' => $profile->solution_module_id,
        'module_name' => $module ? $module->name : null,
        'solution_version_id' => null,
        'solution_version_code' => null,
        'module_version_id' => $profile->module_version_id ?? null,
        'module_version_code' => $moduleVersionCode,
        'version_display' => $moduleVersionCode,
        'profile_code' => $profile->code,
        'status' => $profile->status,
        'status_name' => SolutionModuleReviewProfile::getStatusName($profile->status),
        'status_color' => SolutionModuleReviewProfile::getStatusColor($profile->status),
        'start_date' => optional($profile->start_date)->format('d/m/Y'),
        'start_date_raw' => optional($profile->start_date)->format('Y-m-d'),
        'sent_date' => optional($profile->sent_date)->format('d/m/Y'),
        'sent_date_raw' => optional($profile->sent_date)->format('Y-m-d'),
        'review_deadline' => optional($profile->review_deadline)->format('d/m/Y'),
        'review_deadline_raw' => optional($profile->review_deadline)->format('Y-m-d'),
        'dept_head_id' => $profile->dept_head_id ?? null,
        'pm_id' => $profile->pm_id ?? null,
        'content' => $profile->content,
        'reason_deny' => $profile->reason_deny ?? null,
        'created_at' => $profile->created_at,
        'updated_at' => $profile->updated_at,
        'created_by' => $profile->created_by,
        'updated_by' => $profile->updated_by,
        'files' => $profile->files->map(function ($file) {
            return [
                'id' => $file->id,
                'name' => $file->name,
                'attachment_type_id' => $file->attachment_type_id,
                'employee_id' => $file->employee_id,
                'file_name' => $file->file_name,
                'file_path' => $file->file_path,
                'file_size' => $file->file_size,
                'file_type' => $file->file_type,
            ];
        })->values(),
        'bom_lists' => $profile->bomLists->map(function ($bom) {
            $employee = $bom->createdByEmployee;
            return [
                'id' => $bom->id,
                'code' => $bom->code,
                'name' => $bom->name,
                'created_by_code' => optional($employee)->code ?? '',
                'created_by_name' => $employee && $employee->info ? $employee->info->fullname : '',
                'created_at' => $bom->created_at ? $bom->created_at->format('d/m/Y') : null,
            ];
        })->values(),
    ];
}
```

- [ ] **Step 3: Viết lại `getSolutionReviewProfiles()` — gộp 2 nguồn dữ liệu**

Viết lại method chính. Giữ nguyên signature, thêm xử lý params `type`, `solution_module_id`, `module_version_id`:

```php
public function getSolutionReviewProfiles(Request $request, Solution $solution): array
{
    $type = $request->input('type', 'all');
    $perPage = max((int) $request->input('per_page', 10), 1);
    $page = max((int) $request->input('page', 1), 1);
    $sortField = $request->input('sort_field', 'created_at');
    $sortDir = strtolower($request->input('sort_dir', 'desc')) === 'asc' ? 'asc' : 'desc';
    $allowedSortFields = ['id', 'code', 'status', 'sent_date', 'review_deadline', 'created_at', 'updated_at'];
    $sortColumn = in_array($sortField, $allowedSortFields, true) ? $sortField : 'created_at';

    $merged = collect();

    // 1. Query hồ sơ giải pháp
    if ($type === 'all' || $type === 'solution') {
        $solutionQuery = $solution->reviewProfiles()->with(['files', 'bomLists.createdByEmployee.info']);
        $this->applyCommonReviewProfileFilters($solutionQuery, $request);

        if ($request->filled('solution_version_id')) {
            $solutionQuery->where('solution_version_id', $request->solution_version_id);
        }

        $solutionProfiles = $solutionQuery->get()->map(function ($profile) {
            return $this->transformSolutionReviewProfile($profile);
        });

        $merged = $merged->concat($solutionProfiles);
    }

    // 2. Query hồ sơ hạng mục
    if ($type === 'all' || $type === 'module') {
        $moduleIds = SolutionModule::where('solution_id', $solution->id)->pluck('id');

        if ($moduleIds->isNotEmpty()) {
            $moduleQuery = SolutionModuleReviewProfile::whereIn('solution_module_id', $moduleIds)
                ->with(['files', 'bomLists.createdByEmployee.info', 'solutionModule']);

            $this->applyCommonReviewProfileFilters($moduleQuery, $request);

            if ($request->filled('solution_module_id')) {
                $moduleQuery->where('solution_module_id', $request->solution_module_id);
            }
            if ($request->filled('module_version_id')) {
                $moduleQuery->where('module_version_id', $request->module_version_id);
            }

            $moduleProfiles = $moduleQuery->get()->map(function ($profile) use ($solution) {
                return $this->transformModuleReviewProfile($profile, $solution);
            });

            $merged = $merged->concat($moduleProfiles);
        }
    }

    // 3. Sort
    $merged = $merged->sortBy($sortColumn, SORT_REGULAR, $sortDir === 'desc')->values();

    // 4. Paginate thủ công
    $total = $merged->count();
    $lastPage = max((int) ceil($total / $perPage), 1);
    $page = min($page, $lastPage);
    $items = $merged->forPage($page, $perPage)->values()->toArray();
    $from = $total > 0 ? (($page - 1) * $perPage) + 1 : 0;
    $to = $total > 0 ? min($page * $perPage, $total) : 0;

    return [
        'review_profiles' => $items,
        'review_profile_statuses' => array_values(SolutionReviewProfile::STATUSES),
        'meta' => [
            'current_page' => $page,
            'per_page' => $perPage,
            'total' => $total,
            'last_page' => $lastPage,
            'from' => $from,
            'to' => $to,
        ],
    ];
}
```

- [ ] **Step 4: Thêm private method `applyCommonReviewProfileFilters`**

```php
private function applyCommonReviewProfileFilters($query, Request $request): void
{
    if ($request->filled('keyword')) {
        $escaped = escapeLikeKeyword($request->keyword);
        $query->where(function ($q) use ($escaped) {
            $q->where('code', 'like', '%' . $escaped . '%')
                ->orWhere('content', 'like', '%' . $escaped . '%');
        });
    }

    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    if ($request->filled('sent_date_from')) {
        $query->whereDate('sent_date', '>=', $request->sent_date_from);
    }
    if ($request->filled('sent_date_to')) {
        $query->whereDate('sent_date', '<=', $request->sent_date_to);
    }
    if ($request->filled('review_deadline_from')) {
        $query->whereDate('review_deadline', '>=', $request->review_deadline_from);
    }
    if ($request->filled('review_deadline_to')) {
        $query->whereDate('review_deadline', '<=', $request->review_deadline_to);
    }
}
```

- [ ] **Step 5: Thêm use statement cho `SolutionModuleReviewProfile` và `SolutionModule`**

Ở đầu file `SolutionService.php`, thêm nếu chưa có:

```php
use Modules\Assign\Entities\SolutionModuleReviewProfile;
use Modules\Assign\Entities\SolutionModule;
```

- [ ] **Step 6: Kiểm tra API hoạt động**

Gọi thử trên trình duyệt hoặc Postman:

```
GET /api/v1/assign/solutions/15/manager/review-profiles?type=all
```

Kỳ vọng: response trả về cả hồ sơ giải pháp lẫn hồ sơ hạng mục, mỗi record có field `type`.

```
GET /api/v1/assign/solutions/15/manager/review-profiles?type=module
```

Kỳ vọng: chỉ trả hồ sơ hạng mục.

```
GET /api/v1/assign/solutions/15/manager/review-profiles?type=solution
```

Kỳ vọng: chỉ trả hồ sơ giải pháp (giống response cũ + thêm field `type`).

---

## Phase 2: Frontend — Mở rộng bảng và filter

### Task 2: Thêm filter Loại, Hạng mục, Version HM vào ReviewProfilesTab

**Files:**
- Modify: `hrm-client/pages/assign/solutions/components/manager/ReviewProfilesTab.vue`

- [ ] **Step 1: Thêm 3 filter fields vào `initialStateForm` và `data()`**

Trong `initialStateForm` (dòng 148-158), thêm 3 fields:

```js
const initialStateForm = {
    keyword: undefined,
    status: undefined,
    type: 'all',                    // MỚI
    solution_module_id: undefined,  // MỚI
    module_version_id: undefined,   // MỚI
    solution_version_id: undefined,
    sent_date_from: undefined,
    sent_date_to: undefined,
    review_deadline_from: undefined,
    review_deadline_to: undefined,
    sort_field: 'created_at',
    sort_dir: 'desc',
}
```

Trong `data()`, thêm 2 option arrays:

```js
data() {
    return {
        // ... giữ nguyên các field hiện có ...
        moduleOptions: [],          // MỚI
        moduleVersionOptions: [],   // MỚI
        typeOptions: [              // MỚI
            { id: 'all', name: 'Tất cả' },
            { id: 'solution', name: 'Giải pháp' },
            { id: 'module', name: 'Hạng mục' },
        ],
    }
},
```

- [ ] **Step 2: Thêm 3 ô filter vào template `#advanced-filters`**

Sau ô filter "Version GP" (dòng 27-35), thêm 3 ô filter mới. Toàn bộ block `<div class="form-row filter-grid">` thay bằng:

```html
<div class="form-row filter-grid">
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Trạng thái</V2BaseLabel>
        <V2BaseSelect
            v-model="filters.status"
            :options="statusOptions"
            :allowClear="true"
            placeholder="Chọn trạng thái"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Loại</V2BaseLabel>
        <V2BaseSelect
            v-model="filters.type"
            :options="typeOptions"
            :allowClear="false"
        />
    </div>
    <div v-if="filters.type !== 'solution'" class="col-md-3 mb-2">
        <V2BaseLabel>Hạng mục</V2BaseLabel>
        <V2BaseSelect
            v-model="filters.solution_module_id"
            :options="moduleOptions"
            :allowClear="true"
            placeholder="Chọn hạng mục"
        />
    </div>
    <div v-if="filters.type !== 'solution' && filters.solution_module_id" class="col-md-3 mb-2">
        <V2BaseLabel>Version HM</V2BaseLabel>
        <V2BaseSelect
            v-model="filters.module_version_id"
            :options="moduleVersionOptions"
            :allowClear="true"
            placeholder="Chọn version"
        />
    </div>
    <div v-if="filters.type !== 'module'" class="col-md-3 mb-2">
        <V2BaseLabel>Version GP</V2BaseLabel>
        <V2BaseSelect
            v-model="filters.solution_version_id"
            :options="solutionVersionOptions"
            :allowClear="true"
            placeholder="Chọn version"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Ngày gửi từ</V2BaseLabel>
        <V2BaseDatePicker
            v-model="filters.sent_date_from"
            :allowClear="true"
            placeholder="Từ ngày"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Ngày gửi đến</V2BaseLabel>
        <V2BaseDatePicker
            v-model="filters.sent_date_to"
            :allowClear="true"
            placeholder="Đến ngày"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Hạn duyệt từ</V2BaseLabel>
        <V2BaseDatePicker
            v-model="filters.review_deadline_from"
            :allowClear="true"
            placeholder="Từ ngày"
        />
    </div>
    <div class="col-md-3 mb-2">
        <V2BaseLabel>Hạn duyệt đến</V2BaseLabel>
        <V2BaseDatePicker
            v-model="filters.review_deadline_to"
            :allowClear="true"
            placeholder="Đến ngày"
        />
    </div>
</div>
```

- [ ] **Step 3: Thêm watcher cho filter type và solution_module_id**

Thêm 2 watcher trong block `watch`:

```js
'filters.type'(newType) {
    if (newType === 'solution') {
        this.filters.solution_module_id = undefined
        this.filters.module_version_id = undefined
    }
    this.pagination.currentPage = 1
    this.loadData()
},
'filters.solution_module_id'(newId) {
    this.filters.module_version_id = undefined
    this.moduleVersionOptions = []
    if (newId) {
        this.loadModuleVersionOptions(newId)
    }
},
```

- [ ] **Step 4: Thêm method load danh sách hạng mục và version hạng mục**

Thêm 2 methods mới trong `methods`:

```js
async loadModuleOptions() {
    if (!this.solution?.id) return
    try {
        const response = await this.$store.dispatch(
            'apiGetMethod',
            `assign/solutions/${this.solution.id}/manager/modules`,
        )
        const modules = response?.data || []
        this.moduleOptions = Array.isArray(modules)
            ? modules.map((m) => ({ id: m.id, name: m.name || m.code }))
            : []
    } catch (error) {
        this.moduleOptions = []
    }
},
async loadModuleVersionOptions(moduleId) {
    if (!moduleId) return
    try {
        const response = await this.$store.dispatch(
            'apiGetMethod',
            `assign/solution-modules/${moduleId}/versions`,
        )
        const versions = response?.data?.versions || response?.data || []
        this.moduleVersionOptions = Array.isArray(versions)
            ? versions.map((v) => ({ id: v.id, name: 'V' + (v.code || v.name) }))
            : []
    } catch (error) {
        this.moduleVersionOptions = []
    }
},
```

- [ ] **Step 5: Gọi `loadModuleOptions` khi khởi tạo**

Trong `created()` (dòng 259-262), thêm:

```js
async created() {
    await this.loadData()
    this.loadSolutionVersionOptions()
    this.loadModuleOptions()
},
```

Và trong watcher `solution.id` (dòng 264-269):

```js
'solution.id'(newId) {
    if (!newId) return
    this.pagination.currentPage = 1
    this.loadData()
    this.loadSolutionVersionOptions()
    this.loadModuleOptions()
},
```

### Task 3: Thêm 2 cột mới (Loại, Hạng mục) vào bảng

**Files:**
- Modify: `hrm-client/pages/assign/solutions/components/manager/ReviewProfilesTab.vue`

- [ ] **Step 1: Cập nhật computed `tableColumns`**

Thay toàn bộ `tableColumns` computed:

```js
tableColumns() {
    return [
        {
            key: 'index',
            label: 'STT',
            title: 'STT',
            width: '60px',
            minWidth: '60px',
            sticky: true,
            align: 'left',
        },
        {
            key: 'profileInfo',
            label: 'Mã / Nội dung hồ sơ',
            title: 'Mã / Nội dung hồ sơ',
            width: '350px',
            minWidth: '350px',
            sticky: true,
            align: 'left',
        },
        {
            key: 'profileType',
            label: 'Loại',
            title: 'Loại',
            width: '120px',
            minWidth: '120px',
            align: 'left',
        },
        {
            key: 'moduleName',
            label: 'Hạng mục',
            title: 'Hạng mục',
            width: '180px',
            minWidth: '180px',
            align: 'left',
        },
        {
            key: 'versionDisplay',
            label: 'Version',
            title: 'Version',
            width: '140px',
            minWidth: '140px',
            align: 'left',
        },
        {
            key: 'status',
            label: 'Trạng thái',
            title: 'Trạng thái',
            width: '160px',
            minWidth: '160px',
            align: 'left',
        },
        {
            key: 'sentDate',
            label: 'Ngày gửi',
            title: 'Ngày gửi',
            width: '120px',
            minWidth: '120px',
            align: 'left',
        },
        {
            key: 'deadline',
            label: 'Hạn duyệt',
            title: 'Hạn duyệt',
            width: '120px',
            minWidth: '120px',
            align: 'left',
        },
    ]
},
```

- [ ] **Step 2: Thêm template slot cho 3 cột mới, cập nhật cột version**

Trong template, sau slot `#cell-profileInfo`, thêm:

```html
<template #cell-profileType="{ item }">
    <V2BaseBadge
        :color="item.type === 'solution' ? '#2563EB' : '#7C3AED'"
        :title="item.type === 'solution' ? 'Giải pháp' : 'Hạng mục'"
    >
        {{ item.type === 'solution' ? 'Giải pháp' : 'Hạng mục' }}
    </V2BaseBadge>
</template>

<template #cell-moduleName="{ item }">
    {{ item.module_name || '—' }}
</template>

<template #cell-versionDisplay="{ item }">
    <V2BaseBadge v-if="item.version_display" size="xs">
        {{ item.version_display }}
    </V2BaseBadge>
    <span v-else>—</span>
</template>
```

Xoá slot `#cell-solutionVersion` cũ (dòng 117-122) vì đã thay bằng `#cell-versionDisplay`.

### Task 4: Cập nhật logic row actions cho hồ sơ hạng mục

**Files:**
- Modify: `hrm-client/pages/assign/solutions/components/manager/ReviewProfilesTab.vue`

- [ ] **Step 1: Cập nhật `getRowActions` để xử lý cả 2 loại**

```js
getRowActions(profile) {
    const actions = [
        {
            key: 'view',
            title: 'Xem',
            icon: 'ri-eye-line',
            class: 'btn btn-light border btn-sm mr-1',
            interactable: true,
        },
    ]

    let editable = false
    if (profile.type === 'module') {
        editable = this.canDecideModuleProfile(profile)
    } else {
        editable = this.canEditByCreator(profile) || this.canEditByDeptHead(profile)
    }

    if (editable) {
        const isPending = String(profile.status || '') === 'pending'
        actions.push({
            key: 'edit',
            title: isPending ? 'Duyệt' : 'Sửa',
            icon: 'ri-edit-line',
            class: 'btn btn-light border btn-sm',
            interactable: true,
        })
    }

    return actions
},
```

- [ ] **Step 2: Thêm method `canDecideModuleProfile`**

```js
canDecideModuleProfile(profile) {
    if (String(profile.status || '') !== 'pending') return false
    const pmId = this.solution?.pm_id
    return !!pmId && !!this.currentEmployeeId && String(pmId) === String(this.currentEmployeeId)
},
```

- [ ] **Step 3: Cập nhật `handleRowAction` để phân loại event**

```js
handleRowAction(payload) {
    const { action, item } = payload
    if (item.type === 'module') {
        if (action === 'view') {
            this.$emit('view-module-profile', item)
        } else if (action === 'edit') {
            this.$emit('edit-module-profile', item)
        }
        return
    }
    if (action === 'view') {
        this.$emit('view-profile', item)
        return
    }
    if (action === 'edit') {
        this.$emit('edit-profile', item)
    }
},
```

---

## Phase 3: Frontend — Tạo ModuleApprovalViewModal

### Task 5: Tạo component `ModuleApprovalViewModal.vue`

**Files:**
- Create: `hrm-client/pages/assign/solutions/components/manager/ModuleApprovalViewModal.vue`

- [ ] **Step 1: Tạo file component**

Tạo file mới `ModuleApprovalViewModal.vue` với cấu trúc tham chiếu từ `SolutionApprovalModal.vue` nhưng đơn giản hơn (readonly + duyệt):

```vue
<template>
    <div>
        <b-modal
            id="module-review-profile-modal"
            size="xl"
            scrollable
            no-close-on-backdrop
            content-class="shadow modal-xxl"
            @hidden="handleModalHidden"
        >
            <template #modal-header>
                <div class="d-flex align-items-center w-100">
                    <div class="review-modal-header-icon mr-2">
                        <i class="ri-file-paper-2-line" style="font-size: 16px"></i>
                    </div>
                    <div>
                        <h5 class="modal-title m-0">Hồ sơ trình duyệt hạng mục {{ profileData.profile_code }}</h5>
                    </div>
                </div>
                <button type="button" class="close" @click="closeModal">
                    <span aria-hidden="true">&times;</span>
                </button>
            </template>

            <div class="popup-layout">
                <div class="left-col">
                    <div class="section-card">
                        <div class="section-hd">
                            <div class="icon-chip-sm"><i class="ri-file-list-3-line"></i></div>
                            <h5 class="m-0">Hồ sơ và tài liệu đính kèm</h5>
                        </div>
                        <div class="section-bd">
                            <div v-if="isRejected && profileData.reason_deny" class="mb-3">
                                <div class="reject-reason-box">
                                    <div class="reject-reason-header">
                                        <i class="ri-close-circle-line"></i>
                                        Lý do từ chối
                                    </div>
                                    <div class="reject-reason-content">{{ profileData.reason_deny }}</div>
                                </div>
                            </div>

                            <div class="mb-3">
                                <label class="font-weight-bold">Nội dung trình duyệt</label>
                                <div class="review-content-readonly border rounded p-3" v-html="profileData.content || '—'"></div>
                            </div>

                            <div class="mb-3">
                                <FileAttachmentTable
                                    :files="profileData.files || []"
                                    :readonly="true"
                                />
                            </div>

                            <div v-if="profileData.bom_lists && profileData.bom_lists.length" class="mb-3">
                                <label class="font-weight-bold">BOM tổng hợp</label>
                                <BomListTable :bomLists="profileData.bom_lists" :readonly="true" />
                            </div>

                            <div v-if="profileData.id" class="mb-3">
                                <comment-thread type="solution_module_review_profile" :model-id="profileData.id" />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="sticky-info-col">
                    <div class="section-card">
                        <div class="section-hd">
                            <h5 class="mb-0 d-flex align-items-center" style="gap: 8px">
                                <i class="ri-information-line info-title-icon"></i>
                                Thông tin tham chiếu
                            </h5>
                        </div>
                        <div class="section-bd">
                            <div class="info-group">
                                <div class="info-group-title">
                                    <i class="ri-file-list-3-line"></i>
                                    Thông tin hạng mục
                                </div>
                                <div class="kv-list">
                                    <div class="kv-item">
                                        <div class="kv-label">Dự án</div>
                                        <div class="kv-value">{{ solution.project_code || '—' }} - {{ solution.project_name || '—' }}</div>
                                    </div>
                                    <div class="kv-item">
                                        <div class="kv-label">Giải pháp</div>
                                        <div class="kv-value">{{ solution.code || '—' }} - {{ solution.name || '—' }}</div>
                                    </div>
                                    <div class="kv-item">
                                        <div class="kv-label">Hạng mục</div>
                                        <div class="kv-value">{{ profileData.module_name || '—' }}</div>
                                    </div>
                                </div>
                            </div>

                            <div class="info-group">
                                <div class="info-group-title">
                                    <i class="ri-time-line"></i>
                                    Thời gian
                                </div>
                                <div class="kv-list">
                                    <div class="kv-item" v-if="profileData.sent_date">
                                        <div class="kv-label">Ngày gửi</div>
                                        <div class="kv-value">{{ profileData.sent_date }}</div>
                                    </div>
                                    <div class="kv-item">
                                        <div class="kv-label">Thời gian thực hiện</div>
                                        <div class="kv-value">{{ profileData.start_date || '—' }}</div>
                                    </div>
                                    <div class="kv-item">
                                        <div class="kv-label">Hạn duyệt</div>
                                        <div class="kv-value">{{ profileData.review_deadline || '—' }}</div>
                                    </div>
                                </div>
                            </div>

                            <div class="info-group">
                                <div class="info-group-title">
                                    <i class="ri-user-settings-line"></i>
                                    Trạng thái
                                </div>
                                <div class="kv-list">
                                    <div class="kv-item">
                                        <div class="kv-label">Trạng thái</div>
                                        <div class="kv-value">
                                            <V2BaseBadge :color="profileData.status_color">
                                                {{ profileData.status_name || '—' }}
                                            </V2BaseBadge>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <template #modal-footer>
                <template v-if="canDecide">
                    <V2BaseButton status="danger" size="sm" :disabled="isSaving" @click="showRejectModal">
                        <template #prefix><i class="ri-close-circle-line" style="font-size: 15px"></i></template>
                        Từ chối
                    </V2BaseButton>
                    <V2BaseButton primary size="sm" :disabled="isSaving" @click="handleApprove">
                        <template #prefix><i class="ri-check-double-line" style="font-size: 15px"></i></template>
                        Duyệt
                    </V2BaseButton>
                </template>
                <V2BaseButton tertiary size="sm" @click="closeModal">
                    <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                    Đóng
                </V2BaseButton>
            </template>
        </b-modal>

        <V2BaseRejectApproveModal
            id="modal-reject-module-review-profile"
            title="Từ chối hồ sơ trình duyệt hạng mục"
            reasonLabel="Lý do từ chối"
            reasonPlaceholder="Nhập lý do từ chối"
            @confirm="handleReject"
        />
    </div>
</template>

<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import FileAttachmentTable from '@/components/FileAttachmentTable.vue'
import CommentThread from '@/components/comments/CommentThread.vue'
import V2BaseRejectApproveModal from '@/components/modal/V2BaseRejectApproveModal.vue'
import BomListTable from '@/components/BomListTable.vue'

export default {
    name: 'ModuleApprovalViewModal',
    components: {
        V2BaseButton,
        V2BaseBadge,
        FileAttachmentTable,
        CommentThread,
        V2BaseRejectApproveModal,
        BomListTable,
    },
    props: {
        solution: {
            type: Object,
            default: () => ({}),
        },
        currentEmployeeId: {
            type: [Number, String, null],
            default: null,
        },
    },
    data() {
        return {
            profileData: {},
            isSaving: false,
        }
    },
    computed: {
        isPM() {
            const pmId = this.solution?.pm_id
            return !!pmId && !!this.currentEmployeeId && String(pmId) === String(this.currentEmployeeId)
        },
        canDecide() {
            return this.isPM && String(this.profileData.status || '') === 'pending'
        },
        isRejected() {
            return String(this.profileData.status || '') === 'rejected'
        },
    },
    methods: {
        open(profile) {
            this.profileData = { ...profile }
            this.$bvModal.show('module-review-profile-modal')
        },
        closeModal() {
            this.$bvModal.hide('module-review-profile-modal')
        },
        handleModalHidden() {
            this.profileData = {}
            this.isSaving = false
        },
        showRejectModal() {
            this.$bvModal.show('modal-reject-module-review-profile')
        },
        async handleApprove() {
            if (this.isSaving) return
            this.isSaving = true
            try {
                await this.$store.dispatch('apiPostMethod', {
                    url: `assign/solution-modules/${this.profileData.module_id}/manager/review-profiles/${this.profileData.id}/decision`,
                    payload: { action: 'approve' },
                })
                this.$toasted?.global?.success?.({ message: 'Đã duyệt hồ sơ trình duyệt hạng mục' })
                this.$emit('decided')
                this.closeModal()
            } catch (error) {
                const msg = error?.response?.data?.message || 'Có lỗi xảy ra'
                this.$toasted?.global?.error?.({ message: msg })
            } finally {
                this.isSaving = false
            }
        },
        async handleReject(reason) {
            if (this.isSaving) return
            this.isSaving = true
            try {
                await this.$store.dispatch('apiPostMethod', {
                    url: `assign/solution-modules/${this.profileData.module_id}/manager/review-profiles/${this.profileData.id}/decision`,
                    payload: { action: 'reject', reason_deny: reason },
                })
                this.$toasted?.global?.success?.({ message: 'Đã từ chối hồ sơ trình duyệt hạng mục' })
                this.$emit('decided')
                this.closeModal()
            } catch (error) {
                const msg = error?.response?.data?.message || 'Có lỗi xảy ra'
                this.$toasted?.global?.error?.({ message: msg })
            } finally {
                this.isSaving = false
            }
        },
    },
}
</script>
```

Style có thể tái sử dụng từ `SolutionApprovalModal.vue` — copy các CSS class `.popup-layout`, `.left-col`, `.sticky-info-col`, `.section-card`, `.section-hd`, `.section-bd`, `.info-group`, `.kv-list`, `.kv-item`, `.kv-label`, `.kv-value`, `.reject-reason-box`, `.reject-reason-header`, `.reject-reason-content` vào `<style scoped>` của file này.

---

## Phase 4: Frontend — Tích hợp modal vào trang manager

### Task 6: Đăng ký ModuleApprovalViewModal trong manager.vue

**Files:**
- Modify: `hrm-client/pages/assign/solutions/_id/manager.vue`

- [ ] **Step 1: Import component**

Sau dòng `import SolutionApprovalModal` (dòng 173):

```js
import ModuleApprovalViewModal from '../components/manager/ModuleApprovalViewModal.vue'
```

- [ ] **Step 2: Đăng ký trong components**

Thêm `ModuleApprovalViewModal` vào object `components` (sau `SolutionApprovalModal`).

- [ ] **Step 3: Thêm component vào template**

Sau tag `<SolutionApprovalModal ... />` (dòng 139-145), thêm:

```html
<ModuleApprovalViewModal
    ref="moduleApprovalViewModal"
    :solution="solutionData"
    :current-employee-id="currentEmployeeId"
    @decided="handleModuleReviewProfileDecided"
/>
```

- [ ] **Step 4: Thêm event listeners trên ReviewProfilesTab**

Cập nhật `<ReviewProfilesTab>` (dòng 97-105), thêm 2 event listener mới:

```html
<ReviewProfilesTab
    v-else-if="activeTab === 'review-profiles'"
    ref="reviewProfilesTab"
    :solution="solutionData"
    :can-decide="canDecideSolutionReviewProfile"
    :current-employee-id="currentEmployeeId"
    @view-profile="handleViewReviewProfile"
    @edit-profile="handleEditReviewProfile"
    @view-module-profile="handleViewModuleReviewProfile"
    @edit-module-profile="handleEditModuleReviewProfile"
/>
```

- [ ] **Step 5: Thêm handler methods**

Trong `methods`, thêm:

```js
handleViewModuleReviewProfile(profile) {
    if (!profile) return
    this.$refs.moduleApprovalViewModal?.open(profile)
},
handleEditModuleReviewProfile(profile) {
    if (!profile) return
    this.$refs.moduleApprovalViewModal?.open(profile)
},
async handleModuleReviewProfileDecided() {
    if (this.$refs.reviewProfilesTab && typeof this.$refs.reviewProfilesTab.loadData === 'function') {
        await this.$refs.reviewProfilesTab.loadData()
    }
    await this.loadSolutionDetail()
},
```

---

## Phase 5: Kiểm tra thủ công

### Task 7: Test thủ công trên trình duyệt

- [ ] **Step 1: Mở trang giải pháp, tab Hồ sơ**

Truy cập `http://127.0.0.1:3000/assign/solutions/15/manager`, chuyển sang tab "Hồ sơ".

Kỳ vọng:
- Bảng hiện cả hồ sơ giải pháp (badge "Giải pháp" xanh) và hồ sơ hạng mục (badge "Hạng mục" tím)
- Cột "Hạng mục" hiện tên hạng mục cho loại module, trống cho loại solution
- Cột "Version" hiện version GP hoặc HM tuỳ loại

- [ ] **Step 2: Test filter Loại**

- Chọn "Giải pháp" → chỉ hiện hồ sơ giải pháp, ẩn filter Hạng mục + Version HM
- Chọn "Hạng mục" → chỉ hiện hồ sơ hạng mục, hiện filter Hạng mục, ẩn filter Version GP
- Chọn "Tất cả" → hiện cả 2 loại

- [ ] **Step 3: Test filter Hạng mục + Version HM**

- Chọn hạng mục cụ thể → chỉ hiện hồ sơ của hạng mục đó
- Chọn version HM → lọc thêm theo version
- Đổi hạng mục → Version HM reset

- [ ] **Step 4: Test xem + duyệt hồ sơ hạng mục**

- Click icon xem hồ sơ hạng mục → modal mở, hiện đầy đủ nội dung, file, BOM, bình luận
- Nếu đăng nhập là PM + hồ sơ pending → hiện nút Duyệt + Từ chối
- Click Duyệt → toast thành công, modal đóng, bảng reload, status cập nhật
- Test Từ chối → nhập lý do → toast thành công

- [ ] **Step 5: Test quyền trưởng phòng**

Đăng nhập bằng tài khoản trưởng phòng:
- Mở modal hồ sơ hạng mục → chỉ có nút "Đóng", không có nút Duyệt/Từ chối

- [ ] **Step 6: Test edge case**

- Giải pháp không có hạng mục → bảng chỉ hiện hồ sơ giải pháp, dropdown Hạng mục rỗng
- Sort theo ngày gửi → sort đúng xuyên cả 2 loại
- Pagination hoạt động đúng khi tổng > 10 bản ghi
