# Tab "Dữ liệu liên quan" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hiển thị chứng từ nghiệp vụ liên quan (Kế hoạch, Thầu, Hợp đồng) trên tab "Dữ liệu liên quan" trong màn chi tiết dự toán.

**Architecture:** Thêm 1 endpoint BE `GET /v1/category/projects/{project}/related-data` query Quotation, BidPackage, Contract theo `project_id`, trả về mảng phẳng. FE `RelationDataComponent` gọi API lúc mounted, render bảng với mã chứng từ là `nuxt-link`.

**Tech Stack:** PHP 7.4 / Laravel 8, Nuxt 2 / Vue 2 / Bootstrap-Vue

---

## Task 1: Thêm relation `creator()` vào Quotation và Contract model

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Entities/Quotation/Quotation.php`
- Modify: `hrm-thanhan-api/Modules/Category/Entities/Contract/Contract.php`

Hai model này có field `created_by` nhưng chưa có relation `creator()`. BidPackage đã có pattern tương tự tại dòng 122-125.

- [x] **Step 1: Thêm relation `creator()` vào Quotation model**

Mở file `hrm-thanhan-api/Modules/Category/Entities/Quotation/Quotation.php`, thêm method sau bên cạnh relation `approver()` (sau dòng 114):

```php
public function creator()
{
    return $this->belongsTo(Employee::class, 'created_by', 'id');
}
```

Model đã import `App\Models\Employee` ở dòng 7, không cần thêm use.

- [x] **Step 2: Thêm relation `creator()` vào Contract model**

Mở file `hrm-thanhan-api/Modules/Category/Entities/Contract/Contract.php`, thêm method sau bên cạnh relation `approver()` (sau dòng 147):

```php
public function creator()
{
    return $this->belongsTo(Employee::class, 'created_by', 'id');
}
```

Model đã import `App\Models\Employee` ở dòng 7, không cần thêm use.

---

## Task 2: Thêm endpoint `relatedData` vào ProjectController

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php`

- [x] **Step 1: Thêm import BidPackage**

Thêm use statement ở đầu file (đã có import Quotation dòng 22, Contract dòng 28):

```php
use Modules\Category\Entities\BidPackage\BidPackage;
```

- [x] **Step 2: Thêm method `relatedData`**

Thêm method sau vào cuối class `ProjectController` (trước dấu `}` cuối file, sau method `applyProjectDetailReportFilters`):

```php
public function relatedData(Project $project)
{
    $data = collect();

    $quotation = Quotation::where('project_id', $project->id)
        ->with('creator.info')
        ->first();

    if ($quotation) {
        $data->push([
            'type' => 'quotation',
            'label' => 'Kế hoạch',
            'id' => $quotation->id,
            'code' => $quotation->code,
            'executor_name' => $quotation->creator->info->fullname ?? null,
        ]);
    }

    $bidPackages = BidPackage::where('project_id', $project->id)
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

    $contracts = Contract::where('project_id', $project->id)
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

Lưu ý: `Contract::HOP_DONG` để chỉ lấy hợp đồng chính, không lấy phụ lục.

---

## Task 3: Thêm route mới

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php`

- [x] **Step 1: Thêm route vào group projects**

Mở file `hrm-thanhan-api/Modules/Category/Routes/api.php`, trong group `prefix => '/projects'` (dòng 233-249), thêm route mới trước route `/{project}` (dòng 239) để tránh conflict:

```php
Route::get('/{project}/related-data', [ProjectController::class, 'relatedData']);
```

Thêm sau dòng 241 (`/{project}/getProductForQuotation`), trước dòng 242 (`/{project}` PUT):

```php
Route::get('/{project}/related-data', [ProjectController::class, 'relatedData']);
```

---

## Task 4: Kiểm tra API bằng trình duyệt hoặc tool

- [ ] **Step 1: Test API** _(thủ công — user tự test)_

Truy cập API qua browser hoặc Postman:

```
GET /api/v1/category/projects/{project_id}/related-data
```

Với `project_id` là ID của một dự toán đã có báo giá/gói thầu/hợp đồng.

Expected response:
```json
{
  "message": "success",
  "status": 200,
  "data": [
    {
      "type": "quotation",
      "label": "Kế hoạch",
      "id": 45,
      "code": "BG-001/2025",
      "executor_name": "Nguyễn Văn A"
    }
  ]
}
```

Kiểm tra các case:
- Dự toán không có chứng từ → `data: []`
- Dự toán có đầy đủ cả 3 loại → 3+ items
- Dự toán chỉ có báo giá → 1 item "Kế hoạch"

---

## Task 5: Implement RelationDataComponent.vue

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/project/components/RelationDataComponent.vue`

- [x] **Step 1: Viết lại RelationDataComponent.vue**

Thay toàn bộ nội dung file `RelationDataComponent.vue`:

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
        projectId: {
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
                    `category/projects/${this.projectId}/related-data`
                )
                this.items = data
            } catch (e) {
                this.items = []
            }
        },
        getDetailRoute(item) {
            const routeMap = {
                quotation: `/plan/quotation/${item.id}`,
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

## Task 6: Bỏ comment out và truyền prop ở trang chi tiết

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/project/_id/index.vue`

- [x] **Step 1: Bỏ comment out RelationDataComponent**

Mở file `hrm-thanhan-client/pages/sale/project/_id/index.vue`, tại dòng 15, thay:

```html
<!-- <RelationDataComponent :formSubmit="formSubmit" :formError="formError" :isShow="true" /> -->
```

thành:

```html
<RelationDataComponent :projectId="$route.params.id" />
```

---

## Task 7: Test FE trên trình duyệt

- [ ] **Step 1: Kiểm tra tab hiển thị đúng** _(thủ công — user tự test)_

Mở trình duyệt, truy cập trang chi tiết dự toán: `/sale/project/{id}`

Kiểm tra:
1. Tab "Dữ liệu liên quan" hiển thị trong `GeneralComponent`
2. Bảng hiển thị đúng 3 cột header
3. Dữ liệu hiện theo đúng phân hệ (Kế hoạch / Thầu / Hợp đồng)
4. Mã chứng từ là link click được
5. Click vào mã → chuyển đến trang chi tiết tương ứng
6. Người thực hiện hiển thị đúng tên
7. Dự toán không có chứng từ → bảng rỗng (chỉ header)
8. Dự toán có nhiều gói thầu/hợp đồng → hiện nhiều dòng
