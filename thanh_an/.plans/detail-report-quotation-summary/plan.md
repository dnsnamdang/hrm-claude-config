# Sửa báo cáo chi tiết báo giá — Mỗi báo giá 1 dòng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sửa báo cáo `plan/detail-report` từ mỗi hàng hóa 1 dòng sang mỗi báo giá 1 dòng, bấm vào hiện popup chi tiết sản phẩm.

**Architecture:** BE tạo API mới `summaryReport` query trực tiếp bảng `quotations` + subquery tính aggregate từ `quotation_tab_products`. FE sửa bảng 19 cột, thêm popup gọi API `quotations/{id}` có sẵn.

**Tech Stack:** PHP 7.4, Laravel 8, Nuxt 2, Bootstrap-Vue, ExcelJS

---

## Phase 1: Chuẩn bị

### Task 1: Backup file cũ

**Files:**
- Copy: `hrm-thanhan-client/pages/plan/detail-report/index.vue` → `hrm-thanhan-client/pages/plan/detail-report/index.backup.vue`

- [ ] **Step 1: Copy file backup**

```powershell
Copy-Item "D:\laragon\www\dns\hrm-thanhan-client\pages\plan\detail-report\index.vue" "D:\laragon\www\dns\hrm-thanhan-client\pages\plan\detail-report\index.backup.vue"
```

---

## Phase 2: Backend

### Task 2: Thêm route `summary-report`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:260`

- [ ] **Step 1: Thêm route mới**

Thêm dòng sau **trước** route `/{quotation}` (dòng 262) và **sau** dòng `detail-report/export` (dòng 261):

```php
Route::get('/summary-report', [QuotationController::class, 'summaryReport']);
```

File sau khi sửa (dòng 260-263):

```php
Route::get('/detail-report', [QuotationController::class, 'detailReport']);
Route::get('/detail-report/export', [QuotationController::class, 'exportDetailReport']);
Route::get('/summary-report', [QuotationController::class, 'summaryReport']);
Route::get('/{quotation}', [QuotationController::class, 'show']);
```

---

### Task 3: Thêm method `summaryReport` trong QuotationController

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/QuotationController.php`

- [ ] **Step 1: Thêm method `summaryReport`**

Thêm method mới sau method `detailReport` (sau dòng 653):

```php
public function summaryReport(Request $request)
{
    $perPage = $request->get('per_page', 20);

    $query = \Modules\Category\Entities\Quotation\Quotation::query()
        ->leftJoin('employees', 'employees.id', '=', 'quotations.created_by')
        ->leftJoin('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
        ->leftJoin('companies', 'companies.id', '=', 'quotations.main_company_contractor')
        ->select([
            'quotations.id',
            'quotations.code as quotation_code',
            \DB::raw('(SELECT GROUP_CONCAT(qapi.array_product_name SEPARATOR ", ") FROM quotation_array_product_ids qapi WHERE qapi.quotation_id = quotations.id) as array_product_name'),
            'quotations.project_type',
            'companies.code as main_company_name',
            'quotations.created_at as quotation_created_at',
            'quotations.receiver_time',
            'quotations.process_time',
            'quotations.customer_area_name',
            'quotations.customer_province_name',
            'quotations.status as quotation_status',
            'quotations.customer_code',
            'quotations.customer_name',
            'quotations.customer_address',
            'quotations.customer_last_used_name',
            \DB::raw('(SELECT COUNT(*) FROM quotation_tab_products qtp WHERE qtp.quotation_id = quotations.id) as product_count'),
            \DB::raw('(SELECT COALESCE(SUM(ROUND(qtp.price_before_vat * qtp.qty)), 0) FROM quotation_tab_products qtp WHERE qtp.quotation_id = quotations.id) as total_before_vat'),
            \DB::raw('(SELECT COALESCE(SUM(qtp.amount), 0) FROM quotation_tab_products qtp WHERE qtp.quotation_id = quotations.id) as total_after_vat'),
            'employee_infos.code as employee_code',
            'employee_infos.fullname as employee_name',
        ])
        ->orderBy('quotations.created_at', 'desc')
        ->orderBy('quotations.id', 'desc');

    $this->applyDetailReportPermissions($query);
    $this->applySummaryReportFilters($query, $request);

    $results = $query->paginate($perPage);

    $statusMap = [
        1 => 'Đang tạo', 2 => 'Chờ duyệt', 3 => 'Đã duyệt',
        4 => 'Đã lập hợp đồng', 5 => 'Bị từ chối', 6 => 'Không duyệt',
        7 => 'Đã gửi thầu', 8 => 'Đã lập gói thầu', 9 => 'Chuyển hợp đồng',
        10 => 'Đang lập hợp đồng', 11 => 'Đang lập gói thầu', 12 => 'Hủy báo giá',
        13 => 'Chờ BGĐ duyệt', 15 => 'TP dừng dự toán', 16 => 'BGĐ dừng dự toán',
    ];

    $projectTypeMap = [
        1 => 'Trong thầu', 2 => 'Ngoài thầu',
        4 => 'Hợp đồng Cho/Tặng', 5 => 'Hợp đồng Đặt/Mượn', 6 => 'Hợp đồng Nguyên tắc',
    ];

    $data = $results->getCollection()->map(function ($item) use ($statusMap, $projectTypeMap) {
        return [
            'quotation_id' => $item->id,
            'quotation_code' => $item->quotation_code ?: '-',
            'array_product_name' => $item->array_product_name ?: '-',
            'project_type_name' => $projectTypeMap[$item->project_type] ?? '-',
            'main_company_name' => $item->main_company_name ?: '-',
            'created_at' => $item->quotation_created_at ? \Carbon\Carbon::parse($item->quotation_created_at)->format('d/m/Y') : '-',
            'receiver_time' => $item->receiver_time ? \Carbon\Carbon::parse($item->receiver_time)->format('d/m/Y') : '-',
            'process_time' => $item->process_time ? \Carbon\Carbon::parse($item->process_time)->format('d/m/Y') : '-',
            'customer_area_name' => $item->customer_area_name ?: '-',
            'customer_province_name' => $item->customer_province_name ?: '-',
            'status_name' => $statusMap[$item->quotation_status] ?? '-',
            'customer_code' => $item->customer_code ?: '-',
            'customer_name' => $item->customer_name ?: '-',
            'customer_address' => $item->customer_address ?: '-',
            'customer_last_used_name' => $item->customer_last_used_name ?: '-',
            'product_count' => (int) $item->product_count,
            'total_before_vat' => (int) $item->total_before_vat,
            'total_after_vat' => (int) $item->total_after_vat,
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

- [ ] **Step 2: Thêm method `applySummaryReportFilters`**

Thêm sau method `applyDetailReportFilters` (sau dòng 801):

```php
private function applySummaryReportFilters($query, Request $request)
{
    if ($request->quotation_code) {
        $query->where('quotations.code', 'like', '%' . $request->quotation_code . '%');
    }
    if ($request->project_type) {
        $query->where('quotations.project_type', $request->project_type);
    }
    if ($request->company_id) {
        $query->where('quotations.main_company_contractor', $request->company_id);
    }
    if ($request->customer_code) {
        $query->where('quotations.customer_code', 'like', '%' . $request->customer_code . '%');
    }
    if ($request->customer_id) {
        $query->where('quotations.customer_id', $request->customer_id);
    }
    if ($request->province_id) {
        $province = \Modules\Category\Entities\CustomerProvince::find($request->province_id);
        if ($province) {
            $query->where('quotations.customer_province_name', $province->name);
        }
    }
    if ($request->employee_id) {
        $query->where('quotations.created_by', $request->employee_id);
    }
    if ($request->internal_code) {
        $query->whereExists(function ($sub) use ($request) {
            $sub->select(\DB::raw(1))
                ->from('quotation_tab_products')
                ->whereColumn('quotation_tab_products.quotation_id', 'quotations.id')
                ->where('quotation_tab_products.internal_code', 'like', '%' . $request->internal_code . '%');
        });
    }
    if ($request->product_code) {
        $query->whereExists(function ($sub) use ($request) {
            $sub->select(\DB::raw(1))
                ->from('quotation_tab_products')
                ->whereColumn('quotation_tab_products.quotation_id', 'quotations.id')
                ->where('quotation_tab_products.product_code', 'like', '%' . $request->product_code . '%');
        });
    }
}
```

- [ ] **Step 3: Kiểm tra API**

Mở trình duyệt hoặc Postman, gọi:
```
GET /api/v1/category/quotations/summary-report?per_page=5
```
Expected: trả về JSON `{ data: [...], meta: { total: ... } }` với mỗi item là 1 báo giá có `product_count`, `total_before_vat`, `total_after_vat`.

---

## Phase 3: Frontend

### Task 4: Sửa template — bảng 19 cột + popup

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/detail-report/index.vue`

- [ ] **Step 1: Thay toàn bộ phần `<b-thead>` + `<b-tbody>`**

Thay block `<b-thead>` (dòng 129-167) bằng:

```html
<b-thead class="report-header">
    <b-tr>
        <b-th class="space-normal align-middle head-col-1">STT</b-th>
        <b-th class="space-normal align-middle td-width-120 head-col-2">Mã báo giá</b-th>
        <b-th class="space-normal align-middle td-width-150">Mảng hàng hóa</b-th>
        <b-th class="space-normal align-middle td-width-120">Loại báo giá</b-th>
        <b-th class="space-normal align-middle td-width-150">Công ty thực hiện</b-th>
        <b-th class="space-normal align-middle td-width-120">Ngày tiếp nhận</b-th>
        <b-th class="space-normal align-middle td-width-120">Ngày kết chuyển</b-th>
        <b-th class="space-normal align-middle td-width-100">Địa bàn</b-th>
        <b-th class="space-normal align-middle td-width-120">Tỉnh thành</b-th>
        <b-th class="space-normal align-middle td-width-120">Trạng thái</b-th>
        <b-th class="space-normal align-middle td-width-120">Mã khách hàng</b-th>
        <b-th class="space-normal align-middle td-width-200">Tên khách hàng</b-th>
        <b-th class="space-normal align-middle td-width-200">Địa chỉ</b-th>
        <b-th class="space-normal align-middle td-width-200">KH sử dụng cuối cùng</b-th>
        <b-th class="space-normal align-middle td-width-100">Số mặt hàng</b-th>
        <b-th class="space-normal align-middle td-width-150">Tổng trước thuế</b-th>
        <b-th class="space-normal align-middle td-width-150">Tổng sau thuế</b-th>
        <b-th class="space-normal align-middle td-width-120">Mã nhân viên</b-th>
        <b-th class="space-normal align-middle td-width-150">Tên nhân viên</b-th>
    </b-tr>
</b-thead>
```

Thay block `<b-tbody>` (dòng 168-263) bằng:

```html
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
                <b-link :to="`/plan/quotation/${row.quotation_id}`">
                    {{ row.quotation_code }}
                </b-link>
            </b-td>
            <b-td class="space-normal align-middle td-width-150">{{ row.array_product_name }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.project_type_name }}</b-td>
            <b-td class="space-normal align-middle td-width-150">{{ row.main_company_name }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.created_at }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.process_time }}</b-td>
            <b-td class="space-normal align-middle td-width-100">{{ row.customer_area_name }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.customer_province_name }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.status_name }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.customer_code }}</b-td>
            <b-td class="space-normal align-middle td-width-200">{{ row.customer_name }}</b-td>
            <b-td class="space-normal align-middle td-width-200">{{ row.customer_address }}</b-td>
            <b-td class="space-normal align-middle td-width-200">{{ row.customer_last_used_name }}</b-td>
            <b-td
                class="space-normal align-middle td-width-100 text-center"
                :class="row.product_count > 0 ? 'clickable-cell' : 'clickable-cell zero'"
                @click="row.product_count > 0 && openProductModal(row)"
            >{{ row.product_count || '0' }}</b-td>
            <b-td class="space-normal align-middle td-width-150 text-right">{{ row.total_before_vat | formatNumber }}</b-td>
            <b-td class="space-normal align-middle td-width-150 text-right">{{ row.total_after_vat | formatNumber }}</b-td>
            <b-td class="space-normal align-middle td-width-120">{{ row.employee_code }}</b-td>
            <b-td class="space-normal align-middle td-width-150">{{ row.employee_name }}</b-td>
        </b-tr>
    </template>
    <b-tr v-else>
        <b-td colspan="19" class="text-center text-muted">Chưa có dữ liệu</b-td>
    </b-tr>
</b-tbody>
```

- [ ] **Step 2: Thêm popup modal sau thẻ đóng `</div>` cuối cùng của card (trước `</div></template>`)**

Thêm ngay trước `</div></template>` cuối file (trước dòng 293):

```html
<!-- Product Detail Modal -->
<b-modal
    ref="productModal"
    :title="productModalTitle"
    size="xl"
    hide-footer
    scrollable
    modal-class="report-drill-modal"
    @hidden="closeProductModal"
>
    <div v-if="modalLoading" class="text-center py-4"><b-spinner></b-spinner> Đang tải...</div>
    <div v-else>
        <div class="row mb-3 popup-meta">
            <div class="col-md-6">
                <table class="table table-sm table-borderless mb-0">
                    <tr>
                        <td class="text-muted" style="width: 140px">Mã báo giá</td>
                        <td class="font-weight-bold">{{ selectedQuotation.quotation_code }}</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Loại báo giá</td>
                        <td>{{ selectedQuotation.project_type_name }}</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Ngày tiếp nhận</td>
                        <td>{{ selectedQuotation.created_at }}</td>
                    </tr>
                </table>
            </div>
            <div class="col-md-6">
                <table class="table table-sm table-borderless mb-0">
                    <tr>
                        <td class="text-muted" style="width: 140px">Trạng thái</td>
                        <td>{{ selectedQuotation.status_name }}</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Khách hàng</td>
                        <td>{{ selectedQuotation.customer_name }}</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Nhân viên</td>
                        <td>{{ selectedQuotation.employee_name }}</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Tổng giá trị</td>
                        <td class="font-weight-bold">{{ selectedQuotation.total_after_vat | formatNumber }} đ</td>
                    </tr>
                </table>
            </div>
        </div>
        <h6 class="mb-2">Danh sách hàng hóa</h6>
        <div class="modal-table-scroll">
            <b-table-simple bordered small class="modal-sticky-table">
                <b-thead>
                    <b-tr>
                        <b-th class="text-center" style="width: 50px">STT</b-th>
                        <b-th>Mã hàng</b-th>
                        <b-th>Tên hàng</b-th>
                        <b-th>Quy cách</b-th>
                        <b-th class="text-center">ĐVT</b-th>
                        <b-th class="text-right">SL</b-th>
                        <b-th class="text-right">Đơn giá</b-th>
                        <b-th class="text-right">DS trước thuế</b-th>
                        <b-th class="text-center">Thuế GTGT</b-th>
                        <b-th class="text-right">DS sau thuế</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="(item, i) in modalItems" :key="i">
                        <b-td class="text-center">{{ i + 1 }}</b-td>
                        <b-td>{{ item.product_code || item.code }}</b-td>
                        <b-td>{{ item.product_name || item.name }}</b-td>
                        <b-td>{{ item.specification }}</b-td>
                        <b-td class="text-center">{{ item.unit_name }}</b-td>
                        <b-td class="text-right">{{ item.qty | formatNumber }}</b-td>
                        <b-td class="text-right">{{ item.price | formatNumber }}</b-td>
                        <b-td class="text-right">{{ computeBeforeVat(item) | formatNumber }}</b-td>
                        <b-td class="text-center">{{ item.vat_percent }}%</b-td>
                        <b-td class="text-right">{{ item.amount | formatNumber }}</b-td>
                    </b-tr>
                    <b-tr v-if="!modalItems.length">
                        <b-td colspan="10" class="text-center text-muted">Không có hàng hóa</b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
        </div>
        <div class="modal-table-footer" v-if="modalItems.length">
            Tổng: <b>{{ modalItems.length }}</b> sản phẩm
        </div>
    </div>
</b-modal>
```

---

### Task 5: Sửa script — data, methods, filters

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/detail-report/index.vue` (phần `<script>`)

- [ ] **Step 1: Thêm data mới cho popup**

Trong `data()`, thêm 3 property mới sau `isExporting: false`:

```javascript
modalLoading: false,
selectedQuotation: {},
modalItems: [],
```

- [ ] **Step 2: Đổi API trong method `getData`**

Sửa method `getData()` — đổi URL từ `category/quotations/detail-report` sang `category/quotations/summary-report`:

```javascript
async getData() {
    this.isBusy = true
    try {
        const { data, meta } = await this.$store.dispatch(
            'apiGetMethod',
            `category/quotations/summary-report${buildQuery(this.formFilter)}`,
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
```

- [ ] **Step 3: Đổi API trong method `fetchAllPages`**

Sửa method `fetchAllPages()` — đổi URL tương tự:

```javascript
async fetchAllPages() {
    const params = { ...this.formFilter, page: 1, per_page: 500 }
    const first = await this.$store.dispatch(
        'apiGetMethod',
        `category/quotations/summary-report${buildQuery(params)}`,
    )
    const total = first.meta?.total || 0
    const totalPages = Math.max(1, Math.ceil(total / 500))
    const allRows = [...(first.data || [])]

    for (let page = 2; page <= totalPages; page++) {
        const res = await this.$store.dispatch(
            'apiGetMethod',
            `category/quotations/summary-report${buildQuery({ ...params, page })}`,
        )
        allRows.push(...(res.data || []))
    }
    return allRows
},
```

- [ ] **Step 4: Thêm methods cho popup**

Thêm 3 methods mới trong `methods`:

```javascript
computeBeforeVat(item) {
    return Math.round((item.price_before_vat || 0) * (item.qty || 0))
},

async openProductModal(row) {
    this.modalLoading = true
    this.selectedQuotation = row
    this.$refs.productModal.show()
    try {
        const res = await this.$store.dispatch('apiGetMethod', `category/quotations/${row.quotation_id}`)
        const detail = res.data || res
        let items = []
        if (detail.groups && detail.groups.length) {
            detail.groups.forEach((g) => {
                if (g.products && g.products.length) {
                    g.products.forEach((p) => {
                        if (!p.unit_name && p.units && p.units.length) {
                            const found = p.units.find((u) => u.id === p.unit_id || u.unit_id === p.unit_id)
                            p.unit_name = found
                                ? found.unit_name || found.text
                                : p.units[0].unit_name || p.units[0].text || ''
                        }
                        items.push(p)
                    })
                }
            })
        }
        this.modalItems = items
    } catch (e) {
        console.log(e)
        this.$toasted.global.error({ message: 'Tải chi tiết báo giá thất bại' })
        this.$refs.productModal.hide()
    } finally {
        this.modalLoading = false
    }
},

closeProductModal() {
    this.modalItems = []
    this.selectedQuotation = {}
},
```

- [ ] **Step 5: Thêm computed `productModalTitle`**

Thêm trong `computed`:

```javascript
productModalTitle() {
    return this.selectedQuotation.quotation_code
        ? `Chi tiết báo giá — ${this.selectedQuotation.quotation_code}`
        : 'Chi tiết báo giá'
},
```

---

### Task 6: Sửa export Excel

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/detail-report/index.vue` (method `generateWorkbook`)

- [ ] **Step 1: Thay toàn bộ method `generateWorkbook`**

```javascript
async generateWorkbook(rows) {
    const workbook = new ExcelJS.Workbook()
    const sheet = workbook.addWorksheet('Báo cáo chi tiết báo giá')

    const columns = [
        { header: 'Mã báo giá', key: 'quotation_code', width: 16 },
        { header: 'Mảng hàng hóa', key: 'array_product_name', width: 25 },
        { header: 'Loại báo giá', key: 'project_type_name', width: 18 },
        { header: 'Công ty thực hiện', key: 'main_company_name', width: 20 },
        { header: 'Ngày tiếp nhận', key: 'created_at', width: 14 },
        { header: 'Ngày kết chuyển', key: 'process_time', width: 14 },
        { header: 'Địa bàn', key: 'customer_area_name', width: 14 },
        { header: 'Tỉnh thành', key: 'customer_province_name', width: 16 },
        { header: 'Trạng thái', key: 'status_name', width: 18 },
        { header: 'Mã khách hàng', key: 'customer_code', width: 16 },
        { header: 'Tên khách hàng', key: 'customer_name', width: 30 },
        { header: 'Địa chỉ', key: 'customer_address', width: 35 },
        { header: 'KH sử dụng cuối cùng', key: 'customer_last_used_name', width: 25 },
        { header: 'Số mặt hàng', key: 'product_count', width: 14 },
        { header: 'Tổng trước thuế', key: 'total_before_vat', width: 20 },
        { header: 'Tổng sau thuế', key: 'total_after_vat', width: 20 },
        { header: 'Mã nhân viên', key: 'employee_code', width: 14 },
        { header: 'Tên nhân viên', key: 'employee_name', width: 22 },
    ]
    sheet.columns = columns

    sheet.insertRow(1, ['BÁO CÁO CHI TIẾT BÁO GIÁ'])
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

    const numCols = new Set([14, 15, 16])
    rows.forEach((row) => {
        const excelRow = sheet.addRow({
            quotation_code: row.quotation_code,
            array_product_name: row.array_product_name,
            project_type_name: row.project_type_name,
            main_company_name: row.main_company_name,
            created_at: row.created_at,
            process_time: row.process_time,
            customer_area_name: row.customer_area_name,
            customer_province_name: row.customer_province_name,
            status_name: row.status_name,
            customer_code: row.customer_code,
            customer_name: row.customer_name,
            customer_address: row.customer_address,
            customer_last_used_name: row.customer_last_used_name,
            product_count: Number(row.product_count) || 0,
            total_before_vat: Number(row.total_before_vat) || 0,
            total_after_vat: Number(row.total_after_vat) || 0,
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
        `bao_cao_chi_tiet_bao_gia_${timestamp}.xlsx`,
    )
},
```

---

### Task 7: Thêm styles cho popup và clickable-cell

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/detail-report/index.vue` (phần `<style>`)

- [ ] **Step 1: Thêm styles mới vào cuối block `<style lang="scss" scoped>`**

Thêm trước thẻ đóng `</style>` (trước dòng 693):

```scss
.clickable-cell {
    cursor: pointer;
    color: #7030a0;
    font-weight: 600;
    user-select: none;

    &:hover {
        background: rgba(#7030a0, 0.06);
    }

    &::after {
        content: '↗';
        margin-left: 4px;
        opacity: 0.4;
        font-size: 11px;
    }

    &:hover::after {
        opacity: 1;
    }

    &.zero {
        color: #ada496;
        cursor: default;
        font-weight: 400;

        &::after {
            content: '–';
            opacity: 0.5;
        }

        &:hover {
            background: transparent;
            color: #ada496;
        }
    }
}

.popup-meta {
    margin-top: 0;
    ::v-deep table td {
        font-size: 13px;
        padding: 2px 6px;
        color: #1a1815;
        font-weight: 500;
        vertical-align: middle;
    }
    ::v-deep table td.text-muted {
        font-size: 13px;
        font-weight: 400;
        color: #82796a !important;
        white-space: nowrap;
        padding-right: 4px;
        &::after {
            content: ':';
        }
    }
}

.modal-table-scroll {
    max-height: 400px;
    overflow: auto;
    border: 1px solid #e5e2da;
    border-radius: 4px;
}

::v-deep .modal-sticky-table {
    border-collapse: separate;
    border-spacing: 0;

    thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #fafaf7;
        border-bottom: 1px solid #c9c5ba;
    }
}

.modal-table-footer {
    padding: 8px 12px;
    font-size: 13px;
    color: #4a453c;
    border-top: 1px solid #e5e2da;
    background: #fafaf7;
    border-radius: 0 0 4px 4px;
}
```

- [ ] **Step 2: Thêm style không scoped cho modal**

Thêm block style mới sau `</style>` cuối cùng:

```html
<style lang="scss">
.report-drill-modal .modal-body {
    padding-top: 16px;
}
</style>
```

---

## Phase 4: Kiểm tra

### Task 8: Kiểm tra trên trình duyệt

- [ ] **Step 1: Kiểm tra bảng chính**

Mở `/plan/detail-report`. Xác nhận:
- Mỗi dòng = 1 báo giá (không lặp báo giá)
- 19 cột hiển thị đúng
- Cột "Số mặt hàng" có số, clickable khi > 0
- Cột "Tổng trước thuế" / "Tổng sau thuế" format number đúng
- Phân trang hoạt động

- [ ] **Step 2: Kiểm tra popup**

Bấm vào số mặt hàng của 1 báo giá:
- Popup mở với thông tin tổng quan phía trên
- Bảng sản phẩm hiển thị đúng (mã hàng, tên, quy cách, ĐVT, SL, đơn giá, DS trước thuế, thuế, DS sau thuế)
- Footer hiển thị tổng số sản phẩm

- [ ] **Step 3: Kiểm tra filter**

Thử filter theo mã báo giá, loại, công ty, khách hàng → bảng lọc đúng.

- [ ] **Step 4: Kiểm tra export Excel**

Bấm "Xuất Excel" → file tải về có 18 cột (không có cột sản phẩm chi tiết), có cột Số mặt hàng / Tổng trước thuế / Tổng sau thuế.

- [ ] **Step 5: Kiểm tra backup**

Xác nhận file `index.backup.vue` tồn tại và nội dung giống bản cũ.
