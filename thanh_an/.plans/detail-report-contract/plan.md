# Báo cáo chi tiết hợp đồng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo màn báo cáo chi tiết hợp đồng hiển thị danh sách sản phẩm từ nhiều hợp đồng, hỗ trợ lọc, phân trang, phân quyền 3 cấp và export Excel client-side.

**Architecture:** Clone pattern từ báo cáo chi tiết thầu (BidPackageController::detailReport + pages/bid_package/detail-report). BE thêm method `detailReport` vào ContractController, query `contract_products` JOIN `contracts`. FE tạo page mới tại `pages/contract/detail-report/index.vue`.

**Tech Stack:** Laravel 8, PHP 7.4, Nuxt 2 (Vue 2), Bootstrap-Vue, ExcelJS, file-saver

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `Modules/Category/Http/Controllers/Api/V1/ContractController.php` | Thêm `detailReport()`, `applyContractDetailReportPermissions()`, `applyContractDetailReportFilters()` |
| Modify | `Modules/Category/Routes/api.php` | Thêm route `GET /contracts/detail-report` |
| Create | `pages/contract/detail-report/index.vue` | Trang FE báo cáo chi tiết hợp đồng |

---

### Task 1: Backend — Thêm route detail-report cho contracts

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:308-331`

- [ ] **Step 1: Thêm route detail-report**

Mở file `Modules/Category/Routes/api.php`, trong group `contracts` (dòng 308), thêm route mới **trước** route `/{contract}` (dòng 315) để tránh bị catch bởi route parameter:

```php
Route::get('/detail-report', [ContractController::class, 'detailReport']);
```

Thêm sau dòng `Route::get('/by-customer', ...)` (dòng 314), trước `Route::get('/{contract}', ...)` (dòng 315).

Kết quả:
```php
Route::group(['prefix' => '/contracts'], function () {
    Route::post('/', [ContractController::class, 'store']);
    Route::get('/', [ContractController::class, 'index']);
    Route::get('/getContractsByField', [ContractController::class, 'getContractsByField']);
    Route::post('/delivery-address', [ContractController::class, 'addDeliveryAddress']);
    Route::get('/assign-employee-search-data', [ContractController::class, 'assignEmployeeSearchData']);
    Route::get('/by-customer', [ContractController::class, 'getByCustomer']);
    Route::get('/detail-report', [ContractController::class, 'detailReport']);
    Route::get('/{contract}', [ContractController::class, 'show']);
    // ... rest unchanged
});
```

---

### Task 2: Backend — Thêm method detailReport vào ContractController

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractController.php`

- [ ] **Step 1: Thêm import Carbon**

Kiểm tra đầu file đã có `use Carbon\Carbon;` chưa. Nếu chưa, thêm:
```php
use Carbon\Carbon;
```

- [ ] **Step 2: Thêm method detailReport**

Thêm method `detailReport` vào cuối class ContractController (trước dấu `}` đóng class):

```php
public function detailReport(Request $request)
{
    $perPage = $request->get('per_page', 20);

    $query = ContractProduct::query()
        ->join('contracts', 'contracts.id', '=', 'contract_products.contract_id')
        ->leftJoin('units', 'units.id', '=', 'contract_products.unit_id')
        ->leftJoin('employees', 'employees.id', '=', 'contracts.created_by')
        ->leftJoin('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
        ->leftJoin('companies', 'companies.id', '=', 'contracts.main_company_id')
        ->where('contracts.record_type', Contract::HOP_DONG)
        ->select([
            'contracts.id as contract_id',
            'contracts.code as contract_code',
            'contract_products.array_product_name',
            'contracts.type',
            'companies.code as main_company_name',
            'contracts.contract_sign_time',
            'contracts.contract_end_time',
            'contracts.number as contract_number',
            'contracts.name as contract_name',
            'contracts.customer_area_name',
            'contracts.customer_province_name',
            'contracts.status',
            'contracts.customer_code',
            'contracts.customer_name',
            'contracts.customer_address',
            'contract_products.internal_code',
            'contract_products.import_type_id',
            'contract_products.product_code',
            'contract_products.product_name',
            'contract_products.specification',
            'units.name as unit_name',
            'contract_products.qty',
            'contract_products.price',
            'contract_products.price_before_vat',
            'contract_products.vat_percent',
            'contract_products.amount',
            'employee_infos.code as employee_code',
            'employee_infos.fullname as employee_name',
        ])
        ->orderBy('contracts.contract_sign_time', 'desc')
        ->orderBy('contracts.id', 'desc')
        ->orderBy('contract_products.id', 'asc');

    $this->applyContractDetailReportPermissions($query);
    $this->applyContractDetailReportFilters($query, $request);

    $results = $query->paginate($perPage);

    $statusMap = [
        1 => 'Đang tạo',
        2 => 'Chờ duyệt',
        3 => 'Đã duyệt',
        4 => 'Không duyệt',
    ];

    $data = $results->getCollection()->map(function ($item) use ($statusMap) {
        return [
            'contract_id' => $item->contract_id,
            'contract_code' => $item->contract_code ?: '-',
            'array_product_name' => $item->array_product_name ?: '-',
            'type_name' => Contract::TYPE_NAME[$item->type] ?? '-',
            'main_company_name' => $item->main_company_name ?: '-',
            'contract_sign_time' => $item->contract_sign_time ? Carbon::parse($item->contract_sign_time)->format('d/m/Y') : '-',
            'contract_end_time' => $item->contract_end_time ? Carbon::parse($item->contract_end_time)->format('d/m/Y') : '-',
            'contract_number' => $item->contract_number ?: '-',
            'contract_name' => $item->contract_name ?: '-',
            'customer_area_name' => $item->customer_area_name ?: '-',
            'customer_province_name' => $item->customer_province_name ?: '-',
            'status_name' => $statusMap[$item->status] ?? '-',
            'customer_code' => $item->customer_code ?: '-',
            'customer_name' => $item->customer_name ?: '-',
            'customer_address' => $item->customer_address ?: '-',
            'internal_code' => $item->internal_code ?: '-',
            'import_type_name' => $item->import_type_id == 1 ? 'Nhập khẩu' : ($item->import_type_id == 2 ? 'Phân phối lại' : '-'),
            'product_code' => $item->product_code ?: '-',
            'product_name' => $item->product_name ?: '-',
            'specification' => $item->specification ?: '-',
            'unit_name' => $item->unit_name ?: '-',
            'qty' => $item->qty,
            'price' => $item->price,
            'total_before_vat' => round(($item->price_before_vat ?? 0) * ($item->qty ?? 0)),
            'vat_percent' => $item->vat_percent,
            'amount' => $item->amount,
            'employee_code' => $item->employee_code ?: '-',
            'employee_name' => $item->employee_name ?: '-',
        ];
    });

    return response()->json([
        'data' => $data,
        'meta' => [
            'total' => $results->total(),
            'per_page' => $results->perPage(),
            'current_page' => $results->currentPage(),
            'last_page' => $results->lastPage(),
        ],
    ]);
}
```

- [ ] **Step 3: Thêm method applyContractDetailReportPermissions**

Thêm ngay sau method `detailReport`:

```php
private function applyContractDetailReportPermissions($query)
{
    if (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết hợp đồng theo tổng công ty")) {
    } elseif (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết hợp đồng theo công ty")) {
        $query->where('contracts.company_id', auth()->user()->info->company_id);
    } elseif (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết hợp đồng theo nhóm nghiệp vụ")) {
        $query->where(function ($q) {
            $q->whereIn('contracts.created_by', listManageEmployeeIdsByGroup())
                ->orWhere('contracts.created_by', auth()->user()->id);
        });
    } else {
        $query->where('contracts.created_by', auth()->user()->id);
    }
}
```

- [ ] **Step 4: Thêm method applyContractDetailReportFilters**

Thêm ngay sau method `applyContractDetailReportPermissions`:

```php
private function applyContractDetailReportFilters($query, Request $request)
{
    if ($request->contract_code) {
        $query->where('contracts.code', 'like', '%' . $request->contract_code . '%');
    }
    if ($request->type) {
        $query->where('contracts.type', $request->type);
    }
    if ($request->company_id) {
        $query->where('contracts.main_company_id', $request->company_id);
    }
    if ($request->customer_code) {
        $query->where('contracts.customer_code', 'like', '%' . $request->customer_code . '%');
    }
    if ($request->customer_id) {
        $query->where('contracts.customer_id', $request->customer_id);
    }
    if ($request->province_id) {
        $province = \Modules\Category\Entities\CustomerProvince::find($request->province_id);
        if ($province) {
            $query->where('contracts.customer_province_name', 'like', '%' . $province->name . '%');
        }
    }
    if ($request->employee_id) {
        $query->where('contracts.created_by', $request->employee_id);
    }
    if ($request->status) {
        $query->where('contracts.status', $request->status);
    }
}
```

- [ ] **Step 5: Test API**

Chạy thử API bằng trình duyệt hoặc Postman:
```
GET /api/v1/category/contracts/detail-report?per_page=5
```

Expected: JSON response với `data` array chứa các object có 27 fields + `contract_id`, và `meta` object có `total`, `per_page`, `current_page`, `last_page`.

---

### Task 3: Frontend — Tạo trang báo cáo chi tiết hợp đồng

**Files:**
- Create: `hrm-thanhan-client/pages/contract/detail-report/index.vue`

- [ ] **Step 1: Tạo file index.vue**

Tạo file `pages/contract/detail-report/index.vue` với nội dung sau (clone từ bid_package/detail-report, đã thay đổi cho hợp đồng):

```vue
<template>
    <div>
        <PageHeader :title="title" :items="items" />

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <div class="row mb-2">
                            <div class="col-12">
                                <div class="d-flex flex-wrap justify-content-end gap-2 header-action-row">
                                    <b-button
                                        variant="secondary"
                                        :disabled="isExporting"
                                        class="btn-export"
                                        @click="exportExcel"
                                    >
                                        <b-spinner small type="grow" class="mr-2" v-if="isExporting" />
                                        <i class="fas fa-file-excel mr-1"></i>
                                        Xuất excel
                                    </b-button>

                                    <b-button v-b-toggle.filters variant="light" class="btn-filter">
                                        <img src="@/assets/images/file-icons/filter.svg" /> <span>Bộ lọc</span>
                                    </b-button>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12">
                                <b-collapse id="filters">
                                    <div class="search-wrap">
                                        <div class="row gx-3 gy-3">
                                            <div class="col-md-3 search-filter">
                                                <b-form-input
                                                    v-model="formFilter.contract_code"
                                                    placeholder="Mã hợp đồng"
                                                    type="text"
                                                    v-on:keyup.enter="searchAndSave"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.type"
                                                    :options="typeOptions"
                                                    placeholder="Loại hợp đồng"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.company_id"
                                                    :options="companies"
                                                    placeholder="Công ty thực hiện"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <b-form-input
                                                    v-model="formFilter.customer_code"
                                                    placeholder="Mã khách hàng"
                                                    type="text"
                                                    v-on:keyup.enter="searchAndSave"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.customer_id"
                                                    :options="customers"
                                                    placeholder="Khách hàng"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.province_id"
                                                    :options="provinces"
                                                    placeholder="Tỉnh thành"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.employee_id"
                                                    :options="employees"
                                                    placeholder="Nhân viên thực hiện"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <Select2
                                                    v-select2-focus
                                                    :settings="{ allowClear: true }"
                                                    v-model="formFilter.status"
                                                    :options="statusOptions"
                                                    placeholder="Trạng thái"
                                                />
                                            </div>
                                            <div class="col-md-3 search-filter">
                                                <button @click="reset()" class="btn btn-reset mr-1">Đặt lại</button>
                                                <button @click="searchAndSave" class="btn btn-primary">Áp dụng</button>
                                            </div>
                                        </div>
                                    </div>
                                </b-collapse>
                            </div>
                        </div>

                        <div class="table-wrapper">
                            <div v-if="isBusy" class="text-center text-muted py-3">
                                <b-spinner small></b-spinner> Đang tải dữ liệu...
                            </div>

                            <div v-else class="table-responsive mb-0 basic-table basic-table-border">
                                <b-table-simple bordered :tbody-tr-class="'tr-hover'" :no-local-sorting="true">
                                    <b-thead class="report-header">
                                        <b-tr>
                                            <b-th class="space-normal align-middle head-col-1">STT</b-th>
                                            <b-th class="space-normal align-middle td-width-120 head-col-2">Mã hợp đồng</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Mảng hàng hóa</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Loại hợp đồng</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Công ty thực hiện</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Ngày ký</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Ngày kết thúc</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Số hợp đồng bán</b-th>
                                            <b-th class="space-normal align-middle td-width-200">Tên hợp đồng</b-th>
                                            <b-th class="space-normal align-middle td-width-100">Địa bàn</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Tỉnh thành</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Trạng thái</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Mã khách hàng</b-th>
                                            <b-th class="space-normal align-middle td-width-200">Tên khách hàng</b-th>
                                            <b-th class="space-normal align-middle td-width-200">Địa chỉ</b-th>
                                            <b-th class="space-normal align-middle td-width-100">Mã nội bộ</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Hàng hóa</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Mã hàng</b-th>
                                            <b-th class="space-normal align-middle td-width-200">Tên hàng</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Quy cách</b-th>
                                            <b-th class="space-normal align-middle td-width-75">ĐVT</b-th>
                                            <b-th class="space-normal align-middle td-width-100">Số lượng</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Đơn giá</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Doanh số trước thuế</b-th>
                                            <b-th class="space-normal align-middle td-width-100">Thuế GTGT</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Doanh số sau thuế</b-th>
                                            <b-th class="space-normal align-middle td-width-120">Mã nhân viên</b-th>
                                            <b-th class="space-normal align-middle td-width-150">Tên nhân viên</b-th>
                                        </b-tr>
                                    </b-thead>
                                    <b-tbody>
                                        <template v-if="tableData.length">
                                            <b-tr
                                                v-for="(row, index) in tableData"
                                                :key="index"
                                                :class="index % 2 === 0 ? 'even-customer-row' : 'odd-customer-row'"
                                            >
                                                <b-td class="space-normal align-middle head-col-1">
                                                    {{ getNumericalOrder(formFilter.page, formFilter.per_page, index) }}
                                                </b-td>
                                                <b-td class="space-normal align-middle td-width-120 head-col-2">
                                                    <b-link :to="`/contract/contract/${row.contract_id}`">
                                                        {{ row.contract_code }}
                                                    </b-link>
                                                </b-td>
                                                <b-td class="space-normal align-middle td-width-150">{{ row.array_product_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.type_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-150">{{ row.main_company_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.contract_sign_time }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.contract_end_time }}</b-td>
                                                <b-td class="space-normal align-middle td-width-150">{{ row.contract_number }}</b-td>
                                                <b-td class="space-normal align-middle td-width-200">{{ row.contract_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-100">{{ row.customer_area_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.customer_province_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.status_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.customer_code }}</b-td>
                                                <b-td class="space-normal align-middle td-width-200">{{ row.customer_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-200">{{ row.customer_address }}</b-td>
                                                <b-td class="space-normal align-middle td-width-100">{{ row.internal_code }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.import_type_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.product_code }}</b-td>
                                                <b-td class="space-normal align-middle td-width-200">{{ row.product_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.specification }}</b-td>
                                                <b-td class="space-normal align-middle td-width-75">{{ row.unit_name }}</b-td>
                                                <b-td class="space-normal align-middle td-width-100 text-right">{{ row.qty | formatNumber }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120 text-right">{{ row.price | formatNumber }}</b-td>
                                                <b-td class="space-normal align-middle td-width-150 text-right">{{ row.total_before_vat | formatNumber }}</b-td>
                                                <b-td class="space-normal align-middle td-width-100 text-right">{{ row.vat_percent }}</b-td>
                                                <b-td class="space-normal align-middle td-width-150 text-right">{{ row.amount | formatNumber }}</b-td>
                                                <b-td class="space-normal align-middle td-width-120">{{ row.employee_code }}</b-td>
                                                <b-td class="space-normal align-middle td-width-150">{{ row.employee_name }}</b-td>
                                            </b-tr>
                                        </template>
                                        <b-tr v-else>
                                            <b-td colspan="28" class="text-center text-muted">Chưa có dữ liệu</b-td>
                                        </b-tr>
                                    </b-tbody>
                                </b-table-simple>
                            </div>
                        </div>

                        <div class="row paging" v-if="!isBusy">
                            <div class="page-total col-md-6">Tổng số bản ghi: {{ totalRows }}</div>
                            <div class="col">
                                <div class="dataTables_paginate paging_simple_numbers float-right">
                                    <ul class="pagination pagination-rounded mb-0">
                                        <b-form-select
                                            v-model="formFilter.per_page"
                                            size="sm"
                                            :options="pageOptions"
                                        ></b-form-select>
                                        <b-pagination
                                            v-model="currentPage"
                                            :total-rows="totalRows"
                                            :per-page="formFilter.per_page"
                                            @input="onPageChange"
                                        ></b-pagination>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PageHeader from '@/components/Page-header'
import Select2 from 'v-select2-component'
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'
import moment from 'moment'
import { buildQuery } from '@/utils/url-action'
import { getNumericalOrder } from '@/utils/common.js'

export default {
    head() {
        return { title: this.title }
    },
    components: { PageHeader, Select2 },
    data() {
        return {
            title: 'Báo cáo chi tiết hợp đồng',
            items: [{ text: 'Hợp đồng' }, { text: 'Báo cáo chi tiết hợp đồng' }],
            typeOptions: [
                { id: 1, text: 'Trong thầu' },
                { id: 2, text: 'Ngoài thầu' },
                { id: 3, text: 'Cho/Tặng' },
                { id: 4, text: 'Đặt/Mượn' },
                { id: 5, text: 'Nguyên tắc' },
            ],
            statusOptions: [
                { id: 1, text: 'Đang tạo' },
                { id: 2, text: 'Chờ duyệt' },
                { id: 3, text: 'Đã duyệt' },
                { id: 4, text: 'Không duyệt' },
            ],
            customers: [],
            provinces: [],
            tableData: [],
            totalRows: 0,
            isBusy: false,
            isExporting: false,
            pageOptions: [10, 25, 50, 100],
            formFilter: {
                page: 1,
                per_page: 20,
                contract_code: null,
                type: null,
                company_id: null,
                customer_code: null,
                customer_id: null,
                province_id: null,
                employee_id: null,
                status: null,
            },
        }
    },
    computed: {
        currentPage: {
            get() {
                return this.formFilter.page
            },
            set(value) {
                this.formFilter.page = value
            },
        },
        companies() {
            return this.$store.state.companies.map((val) => ({ ...val, text: val.name }))
        },
        employees() {
            return this.$store.state.employees.map((val) => ({ ...val, text: val.name }))
        },
    },
    mounted() {
        this.getData()
        this.getCustomers()
        this.getProvinces()
    },
    watch: {
        'formFilter.per_page': {
            handler() {
                this.formFilter.page = 1
                this.getData()
            },
        },
    },
    methods: {
        getNumericalOrder,

        onPageChange(page) {
            this.formFilter.page = page
            this.getData()
        },

        searchAndSave() {
            this.formFilter.page = 1
            this.getData()
        },

        reset() {
            Object.assign(this.formFilter, {
                page: 1,
                per_page: this.formFilter.per_page,
                contract_code: null,
                type: null,
                company_id: null,
                customer_code: null,
                customer_id: null,
                province_id: null,
                employee_id: null,
                status: null,
            })
            this.getData()
        },

        async getCustomers() {
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', 'category/customers?per_page=2000')
                this.customers = data.map((val) => ({ ...val, text: val.code + ' - ' + val.name }))
            } catch (e) {
                console.log(e)
            }
        },

        async getProvinces() {
            try {
                const response = await this.$store.dispatch('apiGet', 'category/customer_provinces?per_page=200')
                this.provinces = response.data.data.map((val) => ({ ...val, text: val.code + ' - ' + val.name }))
            } catch (e) {
                console.log(e)
            }
        },

        async getData() {
            this.isBusy = true
            try {
                const { data, meta } = await this.$store.dispatch(
                    'apiGetMethod',
                    `category/contracts/detail-report${buildQuery(this.formFilter)}`,
                )
                this.tableData = data
                this.totalRows = meta.total
            } catch (error) {
                console.log(error)
                this.$toasted.global.error({ message: 'Tải dữ liệu thất bại' })
            } finally {
                this.isBusy = false
            }
        },

        async exportExcel() {
            if (this.isExporting) return
            this.isExporting = true
            this.$nuxt.$loading.start()
            try {
                const rows = await this.fetchAllPages()
                await this.generateWorkbook(rows)
            } catch (error) {
                console.log(error)
                this.$toasted.global.error({ message: 'Xuất excel thất bại' })
            } finally {
                this.$nuxt.$loading.finish()
                this.isExporting = false
            }
        },

        async fetchAllPages() {
            const params = { ...this.formFilter, page: 1, per_page: 500 }
            const first = await this.$store.dispatch(
                'apiGetMethod',
                `category/contracts/detail-report${buildQuery(params)}`,
            )
            const total = first.meta?.total || 0
            const totalPages = Math.max(1, Math.ceil(total / 500))
            const allRows = [...(first.data || [])]

            for (let page = 2; page <= totalPages; page++) {
                const res = await this.$store.dispatch(
                    'apiGetMethod',
                    `category/contracts/detail-report${buildQuery({ ...params, page })}`,
                )
                allRows.push(...(res.data || []))
            }
            return allRows
        },

        async generateWorkbook(rows) {
            const workbook = new ExcelJS.Workbook()
            const sheet = workbook.addWorksheet('Báo cáo chi tiết hợp đồng')

            const columns = [
                { header: 'Mã hợp đồng', key: 'contract_code', width: 16 },
                { header: 'Mảng hàng hóa', key: 'array_product_name', width: 25 },
                { header: 'Loại hợp đồng', key: 'type_name', width: 18 },
                { header: 'Công ty thực hiện', key: 'main_company_name', width: 20 },
                { header: 'Ngày ký', key: 'contract_sign_time', width: 14 },
                { header: 'Ngày kết thúc', key: 'contract_end_time', width: 14 },
                { header: 'Số hợp đồng bán', key: 'contract_number', width: 20 },
                { header: 'Tên hợp đồng', key: 'contract_name', width: 30 },
                { header: 'Địa bàn', key: 'customer_area_name', width: 14 },
                { header: 'Tỉnh thành', key: 'customer_province_name', width: 16 },
                { header: 'Trạng thái', key: 'status_name', width: 18 },
                { header: 'Mã khách hàng', key: 'customer_code', width: 16 },
                { header: 'Tên khách hàng', key: 'customer_name', width: 30 },
                { header: 'Địa chỉ', key: 'customer_address', width: 35 },
                { header: 'Mã nội bộ', key: 'internal_code', width: 14 },
                { header: 'Hàng hóa', key: 'import_type_name', width: 16 },
                { header: 'Mã hàng', key: 'product_code', width: 16 },
                { header: 'Tên hàng', key: 'product_name', width: 30 },
                { header: 'Quy cách', key: 'specification', width: 16 },
                { header: 'ĐVT', key: 'unit_name', width: 10 },
                { header: 'Số lượng', key: 'qty', width: 12 },
                { header: 'Đơn giá', key: 'price', width: 16 },
                { header: 'Doanh số trước thuế', key: 'total_before_vat', width: 20 },
                { header: 'Thuế GTGT', key: 'vat_percent', width: 12 },
                { header: 'Doanh số sau thuế', key: 'amount', width: 20 },
                { header: 'Mã nhân viên', key: 'employee_code', width: 14 },
                { header: 'Tên nhân viên', key: 'employee_name', width: 22 },
            ]
            sheet.columns = columns

            sheet.insertRow(1, ['BÁO CÁO CHI TIẾT HỢP ĐỒNG'])
            sheet.mergeCells(1, 1, 1, columns.length)
            const titleCell = sheet.getCell('A1')
            titleCell.style = {
                font: { bold: true, size: 16, color: { argb: 'FF1C1C1C' } },
                fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF2CC' } },
                alignment: { horizontal: 'center', vertical: 'middle' },
            }
            sheet.getRow(1).height = 40

            const headerRow = sheet.getRow(2)
            headerRow.eachCell((cell) => {
                cell.style = {
                    font: { bold: true, color: { argb: 'FF1C1C1C' } },
                    fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF2CC' } },
                    alignment: { horizontal: 'center', vertical: 'middle', wrapText: true },
                    border: {
                        top: { style: 'thin' },
                        left: { style: 'thin' },
                        bottom: { style: 'thin' },
                        right: { style: 'thin' },
                    },
                }
            })
            headerRow.height = 30

            const numCols = new Set([21, 22, 23, 24, 25])
            rows.forEach((row) => {
                const excelRow = sheet.addRow({
                    contract_code: row.contract_code,
                    array_product_name: row.array_product_name,
                    type_name: row.type_name,
                    main_company_name: row.main_company_name,
                    contract_sign_time: row.contract_sign_time,
                    contract_end_time: row.contract_end_time,
                    contract_number: row.contract_number,
                    contract_name: row.contract_name,
                    customer_area_name: row.customer_area_name,
                    customer_province_name: row.customer_province_name,
                    status_name: row.status_name,
                    customer_code: row.customer_code,
                    customer_name: row.customer_name,
                    customer_address: row.customer_address,
                    internal_code: row.internal_code,
                    import_type_name: row.import_type_name,
                    product_code: row.product_code,
                    product_name: row.product_name,
                    specification: row.specification,
                    unit_name: row.unit_name,
                    qty: Number(row.qty) || 0,
                    price: Number(row.price) || 0,
                    total_before_vat: Number(row.total_before_vat) || 0,
                    vat_percent: row.vat_percent,
                    amount: Number(row.amount) || 0,
                    employee_code: row.employee_code,
                    employee_name: row.employee_name,
                })
                excelRow.eachCell((cell, colIndex) => {
                    cell.border = {
                        top: { style: 'thin', color: { argb: 'FFBFC7D5' } },
                        left: { style: 'thin', color: { argb: 'FFBFC7D5' } },
                        bottom: { style: 'thin', color: { argb: 'FFBFC7D5' } },
                        right: { style: 'thin', color: { argb: 'FFBFC7D5' } },
                    }
                    cell.alignment = { vertical: 'middle', wrapText: true }
                    if (numCols.has(colIndex) && typeof cell.value === 'number') {
                        cell.alignment = { horizontal: 'right', vertical: 'middle' }
                        cell.numFmt = '#,##0'
                    }
                })
            })

            const timestamp = moment().format('YYYY-MM-DD_HH-mm-ss')
            const buffer = await workbook.xlsx.writeBuffer()
            saveAs(
                new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }),
                `bao_cao_chi_tiet_hop_dong_${timestamp}.xlsx`,
            )
        },
    },
}
</script>

<style lang="scss" scoped>
@import '@/assets/scss/custom-table.scss';

.basic-table-border {
    border: 2px solid #a0a0c0;
    border-radius: 0.4rem;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(12, 30, 66, 0.08);
}

.basic-table-border .table {
    border-collapse: separate;
    border-spacing: 0;
}

.basic-table-border th,
.basic-table-border td {
    border: 1px solid rgba(95, 107, 146, 0.55);
    padding: 0.35rem 0.45rem;
}

.basic-table-border .head-col-1,
.basic-table-border .head-col-2 {
    background-color: #f5f5f5;
    border-right: 1px solid rgba(108, 119, 150, 0.45);
}

.basic-table-border .head-col-1 {
    border-left: 1px solid rgba(108, 119, 150, 0.45);
}

.header-action-row {
    justify-content: flex-end;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.header-action-row .btn-filter {
    min-width: 140px;
    border-color: rgba(59, 130, 246, 0.35);
}

.header-action-row .btn-filter img {
    width: 18px;
}

.search-wrap {
    padding: 20px;
    background: #f3f6ff;
    border: 1px solid #dbe5ff;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

.search-filter {
    padding-bottom: 10px;
}

.table-wrapper {
    min-height: 420px;
}

.table-wrapper .table-responsive {
    min-height: 360px;
    max-height: 72vh;
    overflow: auto;
}

.paging {
    margin-bottom: 16px;
    padding: 10px 0 !important;
    background: #f5f5f5;
    font-size: 14px;
    margin: 0;

    .page-total {
        flex: 1;
        line-height: 34px;
    }

    .custom-select {
        margin: 2px 30px;
        padding: 0 8px 0 12px !important;
        width: 70px;
    }
}

.page-total {
    line-height: 34px;
}

.btn-export {
    min-width: 140px;
}

.text-right {
    text-align: right !important;
}

.text-center {
    text-align: center;
}
</style>
```

- [ ] **Step 2: Test trang FE**

Mở trình duyệt, truy cập: `http://localhost:3000/contract/detail-report`

Kiểm tra:
1. Trang hiển thị đúng tiêu đề "Báo cáo chi tiết hợp đồng"
2. Breadcrumb: Hợp đồng > Báo cáo chi tiết hợp đồng
3. Bảng hiển thị dữ liệu với 27 cột + STT
4. Bộ lọc hoạt động (mở/đóng, nhập liệu, áp dụng, đặt lại)
5. Phân trang hoạt động
6. Link "Mã hợp đồng" dẫn đến trang chi tiết hợp đồng
7. Các cột số hiển thị đúng format (có dấu phẩy ngăn cách nghìn)

- [ ] **Step 3: Test export Excel**

1. Click nút "Xuất excel"
2. File tải về có tên `bao_cao_chi_tiet_hop_dong_YYYY-MM-DD_HH-mm-ss.xlsx`
3. Mở file kiểm tra: title vàng, header vàng, data có border, cột số align phải
