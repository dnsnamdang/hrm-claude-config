# Tab "Dữ liệu liên quan" trên Báo giá — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay tab input thủ công "Dữ liệu liên quan" trên báo giá bằng tab read-only tự động lấy chứng từ liên quan (Dự toán/Thầu/Hợp đồng).

**Architecture:** Tạo endpoint BE mới `GET /quotations/{quotation}/related-data` query 3 loại entity liên quan. FE tạo component mới gọi API và render read-only table giống `RelationDataComponent` bên dự toán. Thầu/Hợp đồng liên kết trực tiếp qua `quotation_id`, Dự toán qua `project_id`.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue

---

### Task 1: Thêm relationship `creator()` vào Project model

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Entities/Project/Project.php:98` (sau method `approver()`)

- [x] **Step 1: Thêm relationship `creator()`**

Mở file `hrm-thanhan-api/Modules/Category/Entities/Project/Project.php`, thêm method sau method `approver()` (line 101):

```php
public function creator()
{
    return $this->belongsTo(Employee::class, 'created_by', 'id');
}
```

Thêm sau dòng 101 (sau closing `}` của `approver()`), trước method `groups()`.

- [x] **Step 2: Verify**

Kiểm tra file đã lưu đúng. Model `Project` đã import `App\Models\Employee` ở line 6.

---

### Task 2: Thêm endpoint `relatedData` vào QuotationController

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/QuotationController.php`
  - Thêm 2 import (sau line 13)
  - Thêm method cuối file (trước line 800)
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:274` (thêm route)

- [x] **Step 1: Thêm import models**

Mở `QuotationController.php`, thêm 2 dòng use sau line 13 (`use ...ContractAssignEmployee`):

```php
use Modules\Category\Entities\BidPackage\BidPackage;
use Modules\Category\Entities\Contract\Contract;
```

- [x] **Step 2: Thêm method `relatedData`**

Thêm method sau method `applyDetailReportFilters()` (trước closing `}` của class ở line 800):

```php
public function relatedData(Quotation $quotation)
{
    $data = collect();

    if ($quotation->project_id) {
        $project = Project::with('creator.info')->find($quotation->project_id);
        if ($project) {
            $data->push([
                'type' => 'project',
                'label' => 'Dự toán',
                'id' => $project->id,
                'code' => $project->code,
                'executor_name' => $project->creator->info->fullname ?? null,
            ]);
        }
    }

    $bidPackages = BidPackage::where('quotation_id', $quotation->id)
        ->with('implement_employee.info')
        ->get();

    foreach ($bidPackages as $bp) {
        $data->push([
            'type' => 'bid_package',
            'label' => 'Thầu',
            'id' => $bp->id,
            'code' => $bp->code,
            'executor_name' => $bp->implement_employee->info->fullname ?? null,
        ]);
    }

    $contracts = Contract::where('quotation_id', $quotation->id)
        ->where('record_type', Contract::HOP_DONG)
        ->with('creator.info')
        ->get();

    foreach ($contracts as $contract) {
        $data->push([
            'type' => 'contract',
            'label' => 'Hợp đồng',
            'id' => $contract->id,
            'code' => $contract->code,
            'executor_name' => $contract->creator->info->fullname ?? null,
        ]);
    }

    return $this->responseJson('success', Response::HTTP_OK, $data);
}
```

- [x] **Step 3: Thêm route**

Mở `hrm-thanhan-api/Modules/Category/Routes/api.php`, thêm route trước dòng `});` đóng group quotations (line 275):

```php
Route::get('/{quotation}/related-data', [QuotationController::class, 'relatedData']);
```

Thêm sau line 274 (sau route `history-approve`).

- [x] **Step 4: Verify API**

Chạy test bằng browser hoặc Postman:
- `GET /api/v1/category/quotations/{id}/related-data`
- Expected: trả JSON với `data` là mảng chứa các dòng Dự toán/Thầu/Hợp đồng

---

### Task 3: Tạo component `QuotationRelatedDataComponent.vue`

**Files:**
- Create: `hrm-thanhan-client/pages/plan/quotation/components/QuotationRelatedDataComponent.vue`

- [x] **Step 1: Tạo component**

Tạo file `hrm-thanhan-client/pages/plan/quotation/components/QuotationRelatedDataComponent.vue`:

```vue
<template>
    <div class="row g-2 category-card">
        <div class="col-md-12">
            <div class="table-responsive mb-0 mt-2">
                <b-table-simple bordered small caption-top style="min-height: 100px">
                    <b-thead class="thead-sticky">
                        <b-tr>
                            <b-th>Phân hệ nghiệp vụ</b-th>
                            <b-th>Chứng từ nghiệp vụ</b-th>
                            <b-th>Người thực hiện</b-th>
                        </b-tr>
                    </b-thead>
                    <b-tbody>
                        <b-tr v-for="(item, index) in items" :key="index">
                            <b-td>{{ item.label }}</b-td>
                            <b-td>
                                <nuxt-link :to="getDetailRoute(item)">
                                    {{ item.code }}
                                </nuxt-link>
                            </b-td>
                            <b-td>{{ item.executor_name || '' }}</b-td>
                        </b-tr>
                    </b-tbody>
                </b-table-simple>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        quotationId: {
            type: [Number, String],
            required: true,
        },
    },
    data() {
        return {
            items: [],
        }
    },
    mounted() {
        this.fetchRelatedData()
    },
    methods: {
        async fetchRelatedData() {
            try {
                const { data } = await this.$store.dispatch(
                    'apiGetMethod',
                    `category/quotations/${this.quotationId}/related-data`
                )
                this.items = data
            } catch (e) {
                this.items = []
            }
        },
        getDetailRoute(item) {
            const routeMap = {
                project: `/sale/project/${item.id}`,
                bid_package: `/bid_package/bid_package/${item.id}`,
                contract: `/contract/contract/${item.id}`,
            }
            return routeMap[item.type] || '#'
        },
    },
}
</script>

<style lang="scss"></style>
```

---

### Task 4: Sửa GeneralComponent.vue — thay tab input bằng component mới

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/quotation/components/GeneralComponent.vue`
  - Template: lines 1004–1067 (tab "Dữ liệu liên quan")
  - Script/components: line 1234 (thêm import)
  - Script/data: line 1202 (xóa `relatedDataList`)
  - Script/computed: lines 1459–1461 (xóa `hasErrorInRelatedDataTab`)

- [x] **Step 1: Thay template tab**

Thay toàn bộ block tab "Dữ liệu liên quan" (lines 1004–1067). Tìm:

```html
<b-tab>
    <template #title>
        <span :class="{ 'text-danger': hasErrorInRelatedDataTab }"> Dữ liệu liên quan</span>
    </template>
    <div class="col-md-12 mt-3">
        ...toàn bộ inline table...
    </div>
</b-tab>
```

Thay bằng:

```html
<b-tab title="Dữ liệu liên quan">
    <QuotationRelatedDataComponent :quotationId="formSubmit.id" />
</b-tab>
```

- [x] **Step 2: Thêm import component**

Trong phần `components` (line 1234, sau `TotalComponent`), thêm:

```javascript
QuotationRelatedDataComponent: () => import('./QuotationRelatedDataComponent.vue'),
```

- [x] **Step 3: Xóa `relatedDataList` trong data()**

Xóa dòng 1202:

```javascript
relatedDataList: [],
```

- [x] **Step 4: Xóa computed `hasErrorInRelatedDataTab`**

Xóa lines 1459–1461:

```javascript
hasErrorInRelatedDataTab() {
    return Object.keys(this.formError).some((key) => key.startsWith('relatedDataList.'))
},
```

- [x] **Step 5: Verify trên browser**

Mở trang chi tiết báo giá (`/plan/quotation/{id}`):
1. Tab "Dữ liệu liên quan" hiện bảng read-only với dữ liệu tự động
2. Nếu báo giá có dự toán → hiện dòng "Dự toán" với mã + link
3. Nếu báo giá có gói thầu → hiện dòng "Thầu"
4. Nếu báo giá có hợp đồng → hiện dòng "Hợp đồng"
5. Click link chứng từ → chuyển đúng trang chi tiết
6. Báo giá không có dữ liệu liên quan → bảng trống, chỉ có header

---

### Checkpoint — 2026-05-25 (hoàn tất)
Vừa hoàn thành: Toàn bộ feature — Task 1 (relationship `creator()` trên Project), Task 2 (endpoint `relatedData` + route), Task 3 (component `QuotationRelatedDataComponent.vue`), Task 4 (sửa `GeneralComponent.vue` thay tab input bằng component read-only). Đã verify trên browser
Đang làm dở: không
Bước tiếp theo: Chuyển STATUS.md sang mục Hoàn thành, merge code
Blocked: không
