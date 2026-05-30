# Danh sách phụ lục chờ duyệt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo màn danh sách phụ lục chờ duyệt gộp tất cả 6 loại phụ lục, gồm 1 API mới ở BE + 1 trang FE.

**Architecture:** Tạo ContractAnnexService query trực tiếp bảng `contract_annexes` với join contracts/customers. Tạo ContractAnnexController expose endpoint GET. FE tạo trang approve.vue theo pattern của `contract/contract/approve.vue`.

**Tech Stack:** Laravel 8, PHP 7.4, Nuxt 2, Vue 2, Bootstrap-Vue, Select2, vue2-datepicker

**Spec:** `docs/superpowers/specs/2026-05-21-contract-annex-approve-list-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|---------------|
| **Tạo mới** | `hrm-thanhan-api/Modules/Category/Services/ContractAnnexService.php` | Query gộp tất cả phụ lục với filter + phân trang |
| **Tạo mới** | `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexApproveResource.php` | Format response (thêm annex_type_label, can_approve, can_edit, can_delete) |
| **Tạo mới** | `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexController.php` | Endpoint GET list-approve |
| **Sửa** | `hrm-thanhan-api/Modules/Category/Routes/api.php` | Thêm route group `/contract_annex` |
| **Tạo mới** | `hrm-thanhan-client/pages/contract/contract_annex/approve.vue` | Trang FE danh sách phụ lục chờ duyệt |

---

### Task 1: Tạo ContractAnnexService

**Files:**
- Create: `hrm-thanhan-api/Modules/Category/Services/ContractAnnexService.php`

- [ ] **Step 1: Tạo file ContractAnnexService.php**

```php
<?php

namespace Modules\Category\Services;

use Modules\Training\Services\BaseService;
use Illuminate\Http\Request;
use Modules\Category\Entities\Contract\ContractAnnex;

class ContractAnnexService extends BaseService
{
    public function getListApprove(Request $request)
    {
        $result = ContractAnnex::query()
            ->when($request->status, function ($query) use ($request) {
                return $query->where('status', $request->status);
            }, function ($query) {
                return $query->where('status', ContractAnnex::CHO_DUYET);
            })
            ->when($request->annex_type, function ($query) use ($request) {
                return $query->where('annex_type', $request->annex_type);
            })
            ->when($request->customer_id, function ($query) use ($request) {
                return $query->whereHas('contract', function ($q) use ($request) {
                    $q->where('customer_id', $request->customer_id);
                });
            })
            ->when($request->main_company_id, function ($query) use ($request) {
                return $query->whereHas('contract', function ($q) use ($request) {
                    $q->where('main_company_id', $request->main_company_id);
                });
            })
            ->when($request->created_by, function ($query) use ($request) {
                return $query->where('created_by', $request->created_by);
            })
            ->when($request->from_time, function ($query) use ($request) {
                return $query->whereDate('created_at', '>=', $request->from_time);
            })
            ->when($request->to_time, function ($query) use ($request) {
                return $query->whereDate('created_at', '<=', $request->to_time);
            });

        return $result->orderBy('id', 'desc');
    }
}
```

- [ ] **Step 2: Verify file syntax**

Run: `cd D:\laragon\www\dns\hrm-thanhan-api && php -l Modules/Category/Services/ContractAnnexService.php`
Expected: `No syntax errors detected`

---

### Task 2: Tạo ContractAnnexApproveResource

**Files:**
- Create: `hrm-thanhan-api/Modules/Category/Transformers/ContractAnnexResource/ContractAnnexApproveResource.php`

- [ ] **Step 1: Tạo file Resource**

```php
<?php

namespace Modules\Category\Transformers\ContractAnnexResource;

use Carbon\Carbon;
use Modules\Human\Transformers\ApiResource;
use Modules\Category\Entities\Customer\CategoryCustomer;

class ContractAnnexApproveResource extends ApiResource
{
    const ANNEX_TYPE_LABELS = [
        'reduce_price' => 'Giảm giá',
        'reduce_quantity' => 'Giảm khối lượng',
        'reduce_vat' => 'Thay đổi VAT',
        'extend_time' => 'Gia hạn thời gian',
        'change_information' => 'Thay đổi thông tin',
        'change_product_name' => 'Đổi tên sản phẩm',
    ];

    public function toArray($request): array
    {
        $contract = $this->contract;
        $customer = $contract ? CategoryCustomer::find($contract->customer_id) : null;

        return [
            'id' => $this->id,
            'code' => $this->code,
            'annex_no' => $this->annex_no,
            'annex_type' => $this->annex_type,
            'annex_type_label' => self::ANNEX_TYPE_LABELS[$this->annex_type] ?? $this->annex_type,
            'contract_code' => $contract->code ?? '',
            'number_contract' => $contract->number ?? '',
            'customer_code' => $customer->code ?? '',
            'customer_name' => $customer->name ?? '',
            'created_at' => $this->created_at ? Carbon::parse($this->created_at)->format('d/m/Y') : null,
            'creator' => $this->employee_create->info->fullname ?? '',
            'created_by' => $this->created_by,
            'approver' => $this->approver->info->fullname ?? '',
            'approved_time' => $this->approved_time ? Carbon::parse($this->approved_time)->format('d/m/Y') : null,
            'reason_deny' => $this->reason_deny,
            'status' => $this->status,
            'can_approve' => $this->canApprove(),
            'can_edit' => $this->canEdit(),
            'can_delete' => $this->canDelete(),
        ];
    }
}
```

- [ ] **Step 2: Verify file syntax**

Run: `cd D:\laragon\www\dns\hrm-thanhan-api && php -l Modules/Category/Transformers/ContractAnnexResource/ContractAnnexApproveResource.php`
Expected: `No syntax errors detected`

---

### Task 3: Tạo ContractAnnexController + Route

**Files:**
- Create: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ContractAnnexController.php`
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php`

- [ ] **Step 1: Tạo file ContractAnnexController.php**

```php
<?php

namespace Modules\Category\Http\Controllers\Api\V1;

use Illuminate\Http\Request;
use Modules\Category\Services\ContractAnnexService;
use Modules\Category\Transformers\ContractAnnexResource\ContractAnnexApproveResource;

class ContractAnnexController extends ApiController
{
    private $contractAnnexService;

    public function __construct(ContractAnnexService $contractAnnexService)
    {
        $this->contractAnnexService = $contractAnnexService;
    }

    public function listApprove(Request $request)
    {
        $result = $this->contractAnnexService->getListApprove($request);
        return $this->apiGetList(ContractAnnexApproveResource::apiPaginate($result, $request));
    }
}
```

- [ ] **Step 2: Thêm route vào api.php**

Trong file `hrm-thanhan-api/Modules/Category/Routes/api.php`, thêm ngay **trước** block `Route::group(['prefix' => '/contract_annex_price']` (trước dòng 353):

```php
    Route::group(['prefix' => '/contract_annex'], function () {
        Route::get('/list-approve', [ContractAnnexController::class, 'listApprove']);
    });
```

Và thêm use statement ở đầu file (cùng khu vực các use khác):

```php
use Modules\Category\Http\Controllers\Api\V1\ContractAnnexController;
```

- [ ] **Step 3: Verify syntax cả 2 file**

Run: `cd D:\laragon\www\dns\hrm-thanhan-api && php -l Modules/Category/Http/Controllers/Api/V1/ContractAnnexController.php && php -l Modules/Category/Routes/api.php`
Expected: `No syntax errors detected` cho cả 2

- [ ] **Step 4: Test API bằng artisan route:list**

Run: `cd D:\laragon\www\dns\hrm-thanhan-api && php artisan route:list --path=contract_annex/list`
Expected: Thấy route `GET api/v1/category/contract_annex/list-approve`

---

### Task 4: Tạo trang FE approve.vue

**Files:**
- Create: `hrm-thanhan-client/pages/contract/contract_annex/approve.vue`

- [ ] **Step 1: Tạo file approve.vue**

```vue
<template>
    <div>
        <PageHeader :title="title" :items="items" />

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <div class="row mb-md-2">
                            <div class="col-sm-12 col-md-12">
                                <div id="tickets-table_filter" class="dataTables_filter text-md-right">
                                    <b-button v-b-toggle.collapse-1 variant="light">
                                        <img src="@/assets/images/file-icons/filter.svg" /> <span>Bộ lọc</span>
                                    </b-button>
                                </div>
                            </div>
                            <div class="col-sm-12 col-md-12">
                                <b-collapse id="collapse-1">
                                    <div class="search-wrap">
                                        <form @submit.prevent="getData(1)">
                                            <div class="row">
                                                <div class="col-md-3 search-filter">
                                                    <Select2
                                                        v-select2-focus
                                                        :settings="{ allowClear: true }"
                                                        v-model="formFilter.customer_id"
                                                        :options="customers"
                                                        placeholder="Khách hàng"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <Select2
                                                        v-select2-focus
                                                        :settings="{ allowClear: true }"
                                                        v-model="formFilter.main_company_id"
                                                        :options="companies"
                                                        placeholder="Công ty"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <Select2
                                                        v-select2-focus
                                                        :settings="{ allowClear: true }"
                                                        v-model="formFilter.annex_type"
                                                        :options="annexTypes"
                                                        placeholder="Loại phụ lục"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <Select2
                                                        v-select2-focus
                                                        :settings="{ allowClear: true }"
                                                        v-model="formFilter.created_by"
                                                        :options="employees"
                                                        placeholder="Người lập"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <date-picker
                                                        v-model="formFilter.from_time"
                                                        type="date"
                                                        format="DD/MM/YYYY"
                                                        value-type="YYYY-MM-DD"
                                                        placeholder="Ngày lập từ"
                                                        v-on:keyup.enter="searchAndSave"
                                                    ></date-picker>
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <date-picker
                                                        v-model="formFilter.to_time"
                                                        type="date"
                                                        format="DD/MM/YYYY"
                                                        value-type="YYYY-MM-DD"
                                                        placeholder="Ngày lập đến"
                                                        v-on:keyup.enter="searchAndSave"
                                                    ></date-picker>
                                                </div>
                                                <div class="col-md-3 search-filter">
                                                    <Select2
                                                        v-select2-focus
                                                        :settings="{ allowClear: true }"
                                                        v-model="formFilter.status"
                                                        :options="statuses"
                                                        placeholder="Trạng thái"
                                                        v-on:keyup.enter="searchAndSave"
                                                    />
                                                </div>
                                                <div class="col-md-3">
                                                    <button @click="reset()" type="button" class="btn btn-reset mr-1">
                                                        Đặt lại
                                                    </button>
                                                    <button
                                                        type="submit"
                                                        class="btn btn-primary mr-1"
                                                        @click="searchAndSave"
                                                    >
                                                        Áp dụng
                                                    </button>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </b-collapse>
                            </div>
                        </div>
                        <!-- Table -->
                        <div class="table-responsive mb-0">
                            <b-table-simple :sticky-header="true" :tbody-tr-class="'tr-hover'" bordered>
                                <b-thead>
                                    <b-tr>
                                        <b-th>STT</b-th>
                                        <b-th>Mã phụ lục</b-th>
                                        <b-th>Số phụ lục</b-th>
                                        <b-th>Mã hợp đồng</b-th>
                                        <b-th>Số hợp đồng</b-th>
                                        <b-th>Mã khách hàng</b-th>
                                        <b-th>Khách hàng</b-th>
                                        <b-th>Loại phụ lục</b-th>
                                        <b-th>Ngày lập</b-th>
                                        <b-th>Người lập</b-th>
                                        <b-th>Người duyệt</b-th>
                                        <b-th>Trạng thái</b-th>
                                        <b-th>Hành động</b-th>
                                    </b-tr>
                                </b-thead>
                                <b-tbody>
                                    <b-tr v-for="(item, index) in tableData" :key="index">
                                        <b-td class="text-center">{{
                                            getNumericalOrder(formFilter.page, formFilter.per_page, index)
                                        }}</b-td>
                                        <b-td>
                                            <nuxt-link :to="getDetailLink(item)">{{ item.code }}</nuxt-link>
                                        </b-td>
                                        <b-td>{{ item.annex_no }}</b-td>
                                        <b-td>{{ item.contract_code }}</b-td>
                                        <b-td>{{ item.number_contract }}</b-td>
                                        <b-td>{{ item.customer_code }}</b-td>
                                        <b-td class="min-w-200">{{ item.customer_name }}</b-td>
                                        <b-td>{{ item.annex_type_label }}</b-td>
                                        <b-td>{{ item.created_at }}</b-td>
                                        <b-td>{{ item.creator }}</b-td>
                                        <b-td>{{ item.approver }}</b-td>
                                        <b-td>
                                            <BaseStatusColor :status="item.status" :colorMap="statusColorMap" style="font-size: 13px;">{{
                                                getStatusText(item)
                                            }}</BaseStatusColor>
                                        </b-td>
                                        <b-td>
                                            <div class="text-center text-nowrap">
                                                <b-button
                                                    :to="getDetailLink(item)"
                                                    class="btn-small"
                                                    v-b-tooltip.hover.top="'Xem'"
                                                >
                                                    <img src="@/assets/images/file-icons/eyes.svg" />
                                                </b-button>
                                                <b-button
                                                    v-if="item.can_edit"
                                                    :to="getEditLink(item)"
                                                    variant="secondary"
                                                    class="btn-small"
                                                    v-b-tooltip.hover.top="'Sửa'"
                                                >
                                                    <img src="@/assets/images/file-icons/pen.svg" />
                                                </b-button>
                                                <b-button
                                                    v-if="item.can_approve"
                                                    :to="getDetailLink(item)"
                                                    variant="secondary"
                                                    class="btn-small"
                                                    v-b-tooltip.hover.top="'Duyệt'"
                                                >
                                                    <img src="@/assets/images/file-icons/approve.svg" />
                                                </b-button>
                                                <b-button
                                                    v-if="item.can_delete"
                                                    v-b-modal.modal-delete-selected
                                                    @click="setDeleteItem(item)"
                                                    variant="secondary"
                                                    class="btn-small"
                                                    v-b-tooltip.hover.top="'Xóa'"
                                                >
                                                    <img src="@/assets/images/file-icons/trash.svg" />
                                                </b-button>
                                            </div>
                                        </b-td>
                                    </b-tr>
                                    <b-tr v-if="tableData.length == 0">
                                        <b-td colspan="13">Không có dữ liệu</b-td>
                                    </b-tr>
                                </b-tbody>
                            </b-table-simple>
                        </div>
                        <div class="row paging" v-if="!isLoading">
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
                                            v-model="formFilter.page"
                                            :total-rows="totalRows"
                                            :per-page="formFilter.per_page"
                                        ></b-pagination>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <confirm-delete-selected @event="deleteItem"></confirm-delete-selected>
    </div>
</template>
<script>
import ConfirmDeleteSelected from '@/components/modal/confirm-delete-selected'
import PageHeader from '@/components/Page-header'
import BaseStatusColor from '@/components/BaseStatusColor.vue'
import { buildQuery } from '@/utils/url-action'
import { getNumericalOrder } from '@/utils/common.js'
import DatePicker from 'vue2-datepicker'
import searchMixin from '@/utils/mixins/searchMixinPlugin.js'

const ANNEX_TYPE_ROUTE_MAP = {
    'reduce_price': 'contract_annex_price',
    'reduce_quantity': 'contract_annex_quantity',
    'reduce_vat': 'contract_annex_vat',
    'extend_time': 'contract_annex_time',
    'change_information': 'contract_annex_information',
    'change_product_name': 'contract_annex_product_name',
}

const ANNEX_TYPE_API_MAP = {
    'reduce_price': 'category/contract_annex_price',
    'reduce_quantity': 'category/contract_annex_quantity',
    'reduce_vat': 'category/contract_annex_vat',
    'extend_time': 'category/contract_annex_time',
    'change_information': 'category/contract_annex_information',
    'change_product_name': 'category/contract_annex_product_name',
}

const initialStateForm = {
    page: 1,
    per_page: 10,
    customer_id: undefined,
    main_company_id: undefined,
    annex_type: undefined,
    created_by: undefined,
    from_time: undefined,
    to_time: undefined,
    status: undefined,
}

export default {
    head() {
        return {
            title: `${this.title}`,
        }
    },
    components: {
        ConfirmDeleteSelected,
        PageHeader,
        BaseStatusColor,
        DatePicker,
    },
    mixins: [searchMixin],
    data() {
        return {
            title: 'Danh sách phụ lục chờ duyệt',
            items: [
                {
                    text: 'Quản lý hợp đồng',
                },
                {
                    text: 'Danh sách phụ lục chờ duyệt',
                },
            ],
            tableData: [],
            totalRows: 0,
            pageOptions: [10, 25, 50, 100],
            formFilter: { ...initialStateForm },
            isLoading: false,
            oldFormFilter: { ...initialStateForm },
            deleteItemData: null,
            customers: [],
            statuses: [
                { id: 2, text: 'Chờ duyệt' },
                { id: 3, text: 'Đã duyệt' },
                { id: 4, text: 'Không duyệt' },
            ],
            annexTypes: [
                { id: 'reduce_price', text: 'Giảm giá' },
                { id: 'reduce_quantity', text: 'Giảm khối lượng' },
                { id: 'reduce_vat', text: 'Thay đổi VAT' },
                { id: 'extend_time', text: 'Gia hạn thời gian' },
                { id: 'change_information', text: 'Thay đổi thông tin' },
                { id: 'change_product_name', text: 'Đổi tên sản phẩm' },
            ],
            debounceTimer: null,
            debounceDelay: 100,
            localStorageKey: 'contract-annex-approve',
            pathsToKeep: ['/contract/contract_annex'],
            statusColorMap: {
                1: 'status-pill pj-status-blue',
                2: 'status-pill pj-status-yellow',
                3: 'status-pill pj-status-green',
                4: 'status-pill pj-status-red',
            },
        }
    },
    mounted() {
        this.getCustomers()
        const savedState = this.loadFilterState()
        this.formFilter = savedState.filter

        if (!this.formFilter.page || this.formFilter.page < 1) {
            this.formFilter.page = 1
        }
        if (!this.formFilter.per_page || this.formFilter.per_page < 1) {
            this.formFilter.per_page = 10
        }
        this.getData()
    },
    computed: {
        companies() {
            return this.$store.state.companies.map((val) => ({ ...val, text: val.code }))
        },
        employees() {
            return this.$store.state.employees.map((val) => ({ ...val, text: val.name }))
        },
    },
    watch: {
        'formFilter.page': {
            handler() {
                this.savePaginationState()
                this.getData()
            },
        },
        'formFilter.per_page': {
            handler() {
                this.savePaginationState()
                this.getData()
            },
        },
        formFilter: {
            handler(newVal) {
                this.saveFilterState()
                this.debounceGetData()
                this.oldFormFilter = JSON.parse(JSON.stringify(this.formFilter))
            },
            deep: true,
        },
    },
    beforeDestroy() {
        if (this.debounceTimer) clearTimeout(this.debounceTimer)
    },
    methods: {
        getNumericalOrder,

        async getData($event = null) {
            this.isLoading = true
            this.formFilter.page = $event || this.formFilter.page
            const { data, meta } = await this.$store.dispatch(
                'apiGetMethod',
                `category/contract_annex/list-approve${buildQuery(this.formFilter)}`
            )

            this.tableData = data
            this.totalRows = meta.total
            this.isLoading = false
            this.saveFilterState()
        },

        async getCustomers() {
            const { data } = await this.$store.dispatch('apiGetMethod', `category/customers?per_page=2000`)
            this.customers = data.map((val) => ({ ...val, text: val.code + ' - ' + val.name }))
        },

        reset() {
            Object.assign(this.formFilter, initialStateForm)
            this.clearFilterState()
            this.getData()
        },

        async searchAndSave() {
            this.formFilter.page = 1
            this.saveFilterState()
            this.getData()
        },

        debounceGetData() {
            if (this.debounceTimer) clearTimeout(this.debounceTimer)
            this.debounceTimer = setTimeout(() => {
                this.getData()
            }, this.debounceDelay)
        },

        getDetailLink(item) {
            const route = ANNEX_TYPE_ROUTE_MAP[item.annex_type]
            return `/contract/${route}/${item.id}`
        },

        getEditLink(item) {
            const route = ANNEX_TYPE_ROUTE_MAP[item.annex_type]
            return `/contract/${route}/${item.id}/edit`
        },

        setDeleteItem(item) {
            this.deleteItemData = item
        },

        async deleteItem() {
            if (!this.deleteItemData) return
            const apiPath = ANNEX_TYPE_API_MAP[this.deleteItemData.annex_type]
            this.$bvModal.hide('modal-delete-selected')
            await this.$store.dispatch('apiDelete', `${apiPath}/${this.deleteItemData.id}`)
            this.getData()

            this.$toasted.global.success({
                message: 'Xóa thành công',
            })
            this.deleteItemData = null
        },

        getStatusText(item) {
            if (item.status == 1) return 'Đang tạo'
            if (item.status == 2) return 'Chờ duyệt'
            if (item.status == 3) return 'Đã duyệt'
            if (item.status == 4) return 'Không duyệt'
        },
    },
}
</script>
<style lang="scss" scoped>
/deep/ .table-b-table-default {
    white-space: nowrap;
}

/deep/ .min-w-200 {
    min-width: 200px;
}
</style>
```

- [ ] **Step 2: Verify trang load được**

Mở trình duyệt, navigate tới `/contract/contract_annex/approve`.
Expected: Trang hiển thị với tiêu đề "Danh sách phụ lục chờ duyệt", bảng dữ liệu, bộ lọc hoạt động.

---

### Task 5: Test end-to-end

- [ ] **Step 1: Test API trực tiếp**

Gọi API qua browser hoặc Postman:
```
GET /api/v1/category/contract_annex/list-approve?status=2&per_page=10
```
Expected: Response JSON có `data` array và `meta` object với phân trang.

- [ ] **Step 2: Test filter trên FE**

1. Mở trang `/contract/contract_annex/approve`
2. Bấm "Bộ lọc" → chọn Loại phụ lục = "Giảm giá" → bấm "Áp dụng"
3. Expected: Chỉ hiển thị phụ lục loại giảm giá
4. Đổi Trạng thái = "Đã duyệt"
5. Expected: Hiển thị phụ lục đã duyệt

- [ ] **Step 3: Test navigate đến trang detail**

1. Bấm icon "Xem" (mắt) trên 1 phụ lục
2. Expected: Navigate tới trang detail tương ứng (vd: `/contract/contract_annex_price/5`)
3. Bấm icon "Sửa" (nếu có)
4. Expected: Navigate tới `/contract/contract_annex_price/5/edit`

- [ ] **Step 4: Test xóa**

1. Bấm icon "Xóa" trên 1 phụ lục có trạng thái Đang tạo / Không duyệt
2. Expected: Modal xác nhận hiện lên
3. Bấm xác nhận
4. Expected: Phụ lục bị xóa, danh sách reload

- [ ] **Step 5: Test phân trang**

1. Đổi per_page = 25
2. Expected: Hiển thị tối đa 25 item
3. Navigate sang trang 2
4. Expected: Dữ liệu đúng trang
