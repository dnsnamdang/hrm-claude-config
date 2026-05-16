# Quotation Flow cho loại Cho/Tặng, Đặt/Mượn, Nguyên tắc — Implementation Plan

> **Trạng thái: ĐÃ TEST XONG — CHỜ COMMIT**

### Checkpoint — 2026-04-25 (2)
Vừa hoàn thành: Test xong toàn bộ flow + fix bug + thêm tính năng hợp đồng liên quan
Đang làm dở: Không
Bước tiếp theo: Commit code
Blocked: Không

**Bugfix + feature session 2026-04-25:**
- [x] BE: Bỏ validate bắt buộc `qty` cho báo giá loại Nguyên tắc (type 6) trong StoreQuotationRequest
- [x] BE: Default `qty`, `amount`, `price_before_vat` về 0 khi null trong QuotationService.syncGroups()
- [x] BE: Thêm cột `related_contract_id` vào bảng contracts (migration + fillable)
- [x] BE: Thêm API `GET /contracts/by-customer` lọc HĐ theo customer_id, loại trừ chính nó
- [x] BE: Thêm `related_contract_id` vào ContractDetailResource
- [x] FE: Thêm data `relatedContracts`, method `getRelatedContracts()` trong Contract GeneralComponent
- [x] FE: Gọi `getRelatedContracts()` sau addNegotiation, onQuotationChange, addCustomer, và mounted (edit/show)
- [x] FE: Bỏ Required cho trường hợp đồng liên quan
- [x] FE: Set `project_id` và `quotation_code` trong `onQuotationChange` để hiển thị mã dự toán
- [x] DB: Fix data cũ — cập nhật project_id cho hợp đồng ID 23-25

**Bugfix session 2026-04-24:**
- [x] FE: Bổ sung loại dự toán 4/5/6 vào dropdown `projectTypes` ở Quotation GeneralComponent + index
- [x] FE: Fix `$refs.total` undefined khi TotalComponent bị ẩn (add.vue + edit.vue)
- [x] FE: Fix prop `formSubmit` default trong ModalProductModal (factory function)
- [x] FE: Fix `meta?.total` optional chaining trong ModalProductModal
- [x] BE: Bổ sung type 4/5/6 vào `$typeNames` trong QuotationResource (danh sách báo giá)
- [x] BE: Bỏ validate `request_complete_time` + `complete_time` cho type 4/5/6 trong RenderQuotationRequest
- [x] FE: Hiện cột giá bán cho loại Cho/Tặng (type 4 báo giá, type 3 hợp đồng)
- [x] FE: Fix `onQuotationChange` mapping sai field (units thay vì packageInformations, product_trade_name)
- [x] FE: Gọi `updatePrice()` sau khi set groups từ báo giá để tính giá min/max
- [x] FE: Giữ giá vốn từ báo giá, không bị `updatePrice()` ghi đè

### Checkpoint — 2026-04-24
Vừa hoàn thành: Tất cả 10 task (BE + FE)
Đang làm dở: Không
Bước tiếp theo: Test thủ công trên trình duyệt toàn bộ flow mới
Blocked: Không

**Goal:** Sửa flow dự toán loại 4/5/6 để đi qua bước phân công báo giá + báo giá trước khi sang hợp đồng, thay vì gửi thẳng.

**Architecture:** Tái sử dụng flow type 1/2 cho type 4/5/6 ở cả BE và FE. BE sửa 3 service (Project, Quotation, Contract) + thêm 1 API endpoint mới. FE sửa 3 component (Quotation GeneralComponent, Quotation ProductComponent, Contract GeneralComponent).

**Tech Stack:** PHP 7.4, Laravel 8, Nuxt 2 (Vue 2), Bootstrap-Vue

**Người phụ trách:** @khoipv

---

### Task 1: BE — ProjectService — Gộp type 4/5/6 vào flow phân công báo giá

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/ProjectService.php:211-257` (method `store`)
- Modify: `hrm-thanhan-api/Modules/Category/Services/ProjectService.php:274-320` (method `update`)

- [x] **Step 1: Sửa method `store()` — gộp type 4/5/6 vào nhánh type 1/2**

Tại line 212, thay:
```php
if ($project->project_type == 1 || $project->project_type == 2) {
```
Thành:
```php
if (in_array($project->project_type, [1, 2, 4, 5, 6])) {
```

Xóa toàn bộ nhánh `else if ($project->isChoTangOrDatMuon())` (line 242-257):
```php
// XÓA ĐOẠN NÀY (line 242-257):
} else if ($project->isChoTangOrDatMuon()) {
    $project->group_process = 'Hợp đồng';
    $project->approver_id = auth()->user()->id;
    $project->approved_time = Carbon::now();
    $project->status = Project::CHO_BGD_DUYET_CHUYEN_HD;
    $project->save();

    $employee_infos = listEmployeeInfoHasPermission('BGĐ duyệt dự toán chuyển hợp đồng');
    $data = [
        'url' => '/sale/project/waiting-approve-transfer/' . $project->id,
        'title' => 'Dự toán <b>' . $project->code . '</b> cần BGĐ duyệt chuyển hợp đồng',
        'type' => 'project',
        'id' => $project->id,
    ];
    EmployeeInfoService::sendToAllNotification($employee_infos, $data);
}
```

- [x] **Step 2: Sửa method `update()` — tương tự như store()**

Tại line 275, thay:
```php
if ($project->project_type == 1 || $project->project_type == 2) {
```
Thành:
```php
if (in_array($project->project_type, [1, 2, 4, 5, 6])) {
```

Xóa toàn bộ nhánh `else if ($project->isChoTangOrDatMuon())` (line 305-320):
```php
// XÓA ĐOẠN NÀY (line 305-320):
} else if ($project->isChoTangOrDatMuon()) {
    $project->group_process = 'Hợp đồng';
    $project->approver_id = auth()->user()->id;
    $project->approved_time = Carbon::now();
    $project->status = Project::CHO_BGD_DUYET_CHUYEN_HD;
    $project->save();

    $employee_infos = listEmployeeInfoHasPermission('BGĐ duyệt dự toán chuyển hợp đồng');
    $data = [
        'url' => '/sale/project/waiting-approve-transfer/' . $project->id,
        'title' => 'Dự toán <b>' . $project->code . '</b> cần BGĐ duyệt chuyển hợp đồng',
        'type' => 'project',
        'id' => $project->id,
    ];
    EmployeeInfoService::sendToAllNotification($employee_infos, $data);
}
```

---

### Task 2: BE — Xóa logic BGĐ duyệt chuyển HĐ trên dự toán

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/ProjectService.php:411-484` (xóa method `approveTransferContract`)
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php:230-241` (xóa method `approveTransferContract`)
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:233-234` (xóa route)

- [x] **Step 1: Xóa method `approveTransferContract()` trong ProjectService**

Xóa toàn bộ method tại line 411-484:
```php
// XÓA method approveTransferContract() (line 411-484)
```

- [x] **Step 2: Xóa method `approveTransferContract()` trong ProjectController**

Xóa toàn bộ method tại line 230-241:
```php
// XÓA (line 230-241):
public function approveTransferContract(Request $request, Project $project)
{
    try {
        return DB::transaction(function () use ($request, $project) {
            $this->projectService->approveTransferContract($request, $project);
            return $this->responseJson('success', Response::HTTP_OK);
        });
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

- [x] **Step 3: Xóa route `approve-transfer-contract`**

Xóa line 233-234 trong `Routes/api.php`:
```php
// XÓA:
Route::put('/{project}/approve-transfer-contract', [ProjectController::class, 'approveTransferContract'])
    ->middleware('checkPermission:BGĐ duyệt dự toán chuyển hợp đồng');
```

---

### Task 3: BE — QuotationService — Type 4/5/6 luôn qua BGĐ duyệt

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/QuotationService.php:437-464` (method `approve`)

- [x] **Step 1: Sửa method `approve()` — type 4/5/6 luôn set CHO_BGĐ_DUYET**

Tại line 437-464, thay toàn bộ đoạn:
```php
if ($request->status == Quotation::DA_DUYET) {
    $switch = false;

    foreach ($request->groups as $group) {
        foreach ($group['products'] as $product) {
            if ($product['import_type_id'] == 1) {
                if ($product['price'] < $product['price_min'] || $product['price'] > $product['price_max']) {
                    $switch = true;
                }
            } else if ($product['import_type_id'] == 2) {
                $min = $product['price_min'] ?? null;
                $max = $product['price_max'] ?? null;
                $price = $product['price'];

                if (
                    ($min && !$max && $price < $min) ||
                    (!$min && $max && $price > $max) ||
                    ($min && $max && ($price < $min || $price > $max))
                ) {
                    $switch = true;
                }
            }
        }
    }
    if ($switch) {
        $quotation->status = Quotation::CHO_BGĐ_DUYET;
        $quotation->save();
    }
```

Thành:
```php
if ($request->status == Quotation::DA_DUYET) {
    if (in_array($quotation->project_type, [4, 5, 6])) {
        $quotation->status = Quotation::CHO_BGĐ_DUYET;
        $quotation->save();
    } else {
        $switch = false;

        foreach ($request->groups as $group) {
            foreach ($group['products'] as $product) {
                if ($product['import_type_id'] == 1) {
                    if ($product['price'] < $product['price_min'] || $product['price'] > $product['price_max']) {
                        $switch = true;
                    }
                } else if ($product['import_type_id'] == 2) {
                    $min = $product['price_min'] ?? null;
                    $max = $product['price_max'] ?? null;
                    $price = $product['price'];

                    if (
                        ($min && !$max && $price < $min) ||
                        (!$min && $max && $price > $max) ||
                        ($min && $max && ($price < $min || $price > $max))
                    ) {
                        $switch = true;
                    }
                }
            }
        }
        if ($switch) {
            $quotation->status = Quotation::CHO_BGĐ_DUYET;
            $quotation->save();
        }
    }
```

---

### Task 4: BE — QuotationService — Render type 4/5/6 chuyển thẳng hợp đồng

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/QuotationService.php:696-731` (method `render`)

- [x] **Step 1: Thêm nhánh type 4/5/6 trong method `render()`**

Sau đoạn `} else if ($quotation->project_type == 2) { ... }` (line 730), thêm:
```php
} else if (in_array($quotation->project_type, [4, 5, 6])) {
    $quotation->update([
        'status' => Quotation::CHUYEN_HOP_DONG,
        'group_process' => 'Hợp đồng',
        'process_time' => Carbon::now()
    ]);

    if ($quotation->contract_manager_id) {
        $employee = Employee::find($quotation->contract_manager_id);
        $data = [
            'url' => '/plan/quotation/' . $quotation->id,
            'title' => 'Báo giá <b>' . $quotation->code . '</b> đã được phân công cho bạn lập hợp đồng',
            'type' => 'quotation',
            'id' => $quotation->id
        ];
        EmployeeInfoService::sendNotification($employee->employee_info_id, $data);
    } else {
        $employee_infos = listEmployeeInfoHasPermission('Phân công hợp đồng');
        $data = [
            'url' => '/plan/quotation/' . $quotation->id,
            'title' => 'Báo giá <b>' . $quotation->code . '</b> cần phân công nhân viên lập hợp đồng',
            'type' => 'quotation',
            'id' => $quotation->id
        ];
        EmployeeInfoService::sendToAllNotification($employee_infos, $data);
    }

    if ($project) {
        $project->update([
            'group_process' => 'Hợp đồng',
            'status' => Project::DA_CHUYEN_HOP_DONG,
            'process_time' => Carbon::now()
        ]);
    }
}
```

---

### Task 5: BE — ContractService — Validate quotation thay vì project

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/ContractService.php:159-165` (method `store`)

- [x] **Step 1: Sửa validation trong method `store()`**

Thay đoạn (line 159-165):
```php
// Nếu là HĐ Cho/Tặng hoặc Đặt/Mượn → validate dự toán
if (in_array($contract->type, [Contract::CHO_TANG, Contract::DAT_MUON, Contract::NGUYEN_TAC])) {
    $project = Project::find($request->project_id);
    if (!$project || $project->status != Project::DA_CHUYEN_HOP_DONG || !in_array($project->project_type, [4, 5, 6])) {
        throw new \Exception('Dự toán không hợp lệ hoặc chưa được BGĐ duyệt');
    }
}
```

Thành:
```php
if (in_array($contract->type, [Contract::CHO_TANG, Contract::DAT_MUON, Contract::NGUYEN_TAC])) {
    $quotation = Quotation::find($request->quotation_id);
    if (!$quotation || $quotation->status != Quotation::CHUYEN_HOP_DONG || !in_array($quotation->project_type, [4, 5, 6])) {
        throw new \Exception('Báo giá không hợp lệ hoặc chưa được duyệt');
    }
}
```

> Lưu ý: Cần thêm `use Modules\Category\Entities\Quotation\Quotation;` ở đầu file nếu chưa có.

---

### Task 6: BE — Thêm API endpoint lấy báo giá cho hợp đồng

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/QuotationService.php` (thêm method)
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/QuotationController.php` (thêm method)
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:240-260` (thêm route)

- [x] **Step 1: Thêm method `approvedForContract()` trong QuotationService**

Thêm method mới vào `QuotationService.php`:
```php
public function approvedForContract(Request $request)
{
    return Quotation::where('status', Quotation::CHUYEN_HOP_DONG)
        ->when($request->project_type, function ($query) use ($request) {
            return $query->where('project_type', $request->project_type);
        })
        ->whereIn('project_type', [4, 5, 6])
        ->orderBy('id', 'desc')
        ->get();
}
```

- [x] **Step 2: Thêm method `approvedForContract()` trong QuotationController**

Thêm method mới vào `QuotationController.php`:
```php
public function approvedForContract(Request $request)
{
    try {
        $result = $this->quotationService->approvedForContract($request);
        return $this->responseJson('success', Response::HTTP_OK, QuotationResource::collection($result));
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

> Lưu ý: Kiểm tra `QuotationResource` đã có sẵn chưa, dùng resource tương ứng. Nếu không có thì dùng `$result` trực tiếp.

- [x] **Step 3: Thêm route trong `api.php`**

Thêm trước route `/{quotation}` (line 245) để tránh conflict:
```php
Route::get('/approved-for-contract', [QuotationController::class, 'approvedForContract']);
```

---

### Task 7: FE — Báo giá — Ẩn tab và TotalComponent khi project_type = 4/5/6

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/quotation/components/GeneralComponent.vue:460` (TotalComponent)
- Modify: `hrm-thanhan-client/pages/plan/quotation/components/GeneralComponent.vue:667` (tab Thư mời)
- Modify: `hrm-thanhan-client/pages/plan/quotation/components/GeneralComponent.vue:852` (tab Ủy quyền)

- [x] **Step 1: Ẩn TotalComponent khi project_type = 4/5/6**

Tại line 460, thay:
```vue
<TotalComponent :formSubmit="formSubmit" :formError="formError" ref="total" />
```
Thành:
```vue
<TotalComponent v-if="![4,5,6].includes(formSubmit.project_type)" :formSubmit="formSubmit" :formError="formError" ref="total" />
```

- [x] **Step 2: Ẩn tab "Thư mời báo giá" khi project_type = 4/5/6**

Tại line 667, thay:
```vue
<b-tab>
    <template #title>
        <span :class="{ 'text-danger': hasErrorInInvitationTab }"> Thư mời báo giá</span>
```
Thành:
```vue
<b-tab v-if="![4,5,6].includes(formSubmit.project_type)">
    <template #title>
        <span :class="{ 'text-danger': hasErrorInInvitationTab }"> Thư mời báo giá</span>
```

- [x] **Step 3: Ẩn tab "Ủy quyền" khi project_type = 4/5/6**

Tại line 852, thay:
```vue
<b-tab>
    <template #title>
        <span :class="{ 'text-danger': hasErrorInAuthTab }">Ủy quyền</span>
```
Thành:
```vue
<b-tab v-if="![4,5,6].includes(formSubmit.project_type)">
    <template #title>
        <span :class="{ 'text-danger': hasErrorInAuthTab }">Ủy quyền</span>
```

---

### Task 8: FE — Báo giá — Ẩn cột bảng hàng hóa theo loại dự toán

**Files:**
- Modify: `hrm-thanhan-client/pages/plan/quotation/components/ProductComponent.vue:924-928` (computed `visibleFieldsExceptName`)

- [x] **Step 1: Thêm logic ẩn cột theo project_type trong computed `visibleFieldsExceptName`**

Tại line 924-928, thay:
```js
visibleFieldsExceptName() {
    return this.visibleFields.filter(
        (f) => f.key !== 'product_name' && f.key !== 'product_trade_name' && f.key !== 'product_code',
    )
},
```
Thành:
```js
visibleFieldsExceptName() {
    let fields = this.visibleFields.filter(
        (f) => f.key !== 'product_name' && f.key !== 'product_trade_name' && f.key !== 'product_code',
    )
    if (this.formSubmit.project_type == 4 || this.formSubmit.project_type == 5) {
        const hiddenKeys = ['price_pre_contract', 'price', 'price_before_vat', 'amount', 'price_difference_coefficient']
        fields = fields.filter((f) => !hiddenKeys.includes(f.key))
    }
    if (this.formSubmit.project_type == 6) {
        const hiddenKeys = ['qty', 'amount', 'price_difference_coefficient']
        fields = fields.filter((f) => !hiddenKeys.includes(f.key))
    }
    return fields
},
```

---

### Task 9: FE — Hợp đồng — Chọn báo giá thay vì dự toán cho type 3/4/5

**Files:**
- Modify: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue:33-43` (dropdown template)
- Modify: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue:1226-1228` (mounted)
- Modify: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue:1895-1955` (methods)
- Modify: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue:1297-1300` (watcher)

- [x] **Step 1: Sửa template — đổi label và v-model từ dự toán sang báo giá**

Tại line 33-43, thay:
```vue
<div class="col-md-4" v-if="formSubmit.type == 3 || formSubmit.type == 4 || formSubmit.type == 5">
    <label>Dự toán <Required /></label>
    <base-select2
        v-model="formSubmit.project_id"
        :options="projectOptions"
        :disabled="isShow || isEdit"
        placeholder="Chọn dự toán"
        @input="onProjectChange"
    />
    <base-helper-error :error="formError['project_id']" />
</div>
```
Thành:
```vue
<div class="col-md-4" v-if="formSubmit.type == 3 || formSubmit.type == 4 || formSubmit.type == 5">
    <label>Báo giá <Required /></label>
    <base-select2
        v-model="formSubmit.quotation_id"
        :options="quotationOptions"
        :disabled="isShow || isEdit"
        placeholder="Chọn báo giá"
        @input="onQuotationChange"
    />
    <base-helper-error :error="formError['quotation_id']" />
</div>
```

- [x] **Step 2: Thêm data `quotationOptions` và sửa method**

Trong `data()`, thêm:
```js
quotationOptions: [],
```

- [x] **Step 3: Sửa method `changeType()` — gọi `getQuotationsForContract` thay vì `getProjectsForContract`**

Tại line 1901-1903, thay:
```js
if (this.formSubmit.type == 3 || this.formSubmit.type == 4 || this.formSubmit.type == 5) {
    this.getProjectsForContract()
}
```
Thành:
```js
if (this.formSubmit.type == 3 || this.formSubmit.type == 4 || this.formSubmit.type == 5) {
    this.getQuotationsForContract()
}
```

- [x] **Step 4: Sửa mounted — gọi `getQuotationsForContract` thay vì `getProjectsForContract`**

Tại line 1226-1228, thay:
```js
if (this.formSubmit.type == 3 || this.formSubmit.type == 4 || this.formSubmit.type == 5) {
    this.getProjectsForContract()
}
```
Thành:
```js
if (this.formSubmit.type == 3 || this.formSubmit.type == 4 || this.formSubmit.type == 5) {
    this.getQuotationsForContract()
}
```

- [x] **Step 5: Thêm method `getQuotationsForContract()`**

Thay method `getProjectsForContract()` (line 1906-1930) thành:
```js
async getQuotationsForContract() {
    const projectTypeMap = { 3: 4, 4: 5, 5: 6 }
    const projectType = projectTypeMap[this.formSubmit.type] || 5
    try {
        const res = await this.$store.dispatch(
            'apiGetMethod',
            `category/quotations/approved-for-contract?project_type=${projectType}`
        )
        this.quotationOptions = (res.data || []).map((q) => ({
            id: q.id,
            text: `${q.code} - ${q.customer_name}`,
        }))
        if (this.formSubmit.quotation_id && !this.quotationOptions.find((q) => q.id == this.formSubmit.quotation_id)) {
            const quotationCode = this.formSubmit.objectable_code || ''
            const customerName = this.formSubmit.customer_name || ''
            this.quotationOptions.unshift({
                id: this.formSubmit.quotation_id,
                text: `${quotationCode} - ${customerName}`.replace(/ - $/, ''),
            })
        }
    } catch (e) {
        console.error(e)
    }
},
```

- [x] **Step 6: Thêm method `onQuotationChange()`**

Thay method `onProjectChange()` (line 1932-2001) thành:
```js
async onQuotationChange(quotationId) {
    if (!quotationId) return
    try {
        const { data } = await this.$store.dispatch(
            'apiGetMethod',
            `category/quotations/${quotationId}`
        )
        this.formSubmit.quotation_id = data.id
        this.formSubmit.objectable_id = data.id
        this.formSubmit.objectable_code = data.code
        this.formSubmit.objectable_type = 'App\\Modules\\Category\\Entities\\Quotation\\Quotation'

        // Thông tin khách hàng
        this.formSubmit.customer_id = data.customer_id
        this.formSubmit.customer_code = data.customer_code
        this.formSubmit.customer_name = data.customer_name
        this.formSubmit.customer_phone = data.customer_phone
        this.formSubmit.customer_address = data.customer_address
        this.formSubmit.customer_area_id = data.customer_area_id
        this.formSubmit.customer_area_name = data.customer_area_name
        this.formSubmit.customer_province_id = data.customer_province_id
        this.formSubmit.customer_province_name = data.customer_province_name
        this.formSubmit.customer_group_name = data.customer_group_name
        this.formSubmit.receiving_source = data.receiving_source

        // Giá bán min, max
        this.formSubmit.price_type_min_id = data.price_type_min_id || null
        this.formSubmit.price_type_max_id = data.price_type_max_id || null

        // Mảng hàng hóa
        this.formSubmit.array_product_id = data.array_product_id || null
        this.formSubmit.product_group_id = data.product_group_id || null

        // Ghi chú
        this.formSubmit.note = data.note

        // Hàng hóa (groups + products)
        this.formSubmit.groups = (data.groups || []).map((group) => ({
            ...group,
            products: (group.products || []).map((product) => {
                const pkgInfos = product.packageInformations || []
                const usuallyUnit = pkgInfos.find((u) => u.is_usually) || pkgInfos[0]
                return {
                    ...product,
                    product_trade_name: product.trade_name,
                    owner_country: product.origin_name,
                    units: pkgInfos.map((u) => ({ id: u.unit_id, text: u.unit_name })),
                    unit_id: usuallyUnit ? usuallyUnit.unit_id : '',
                    unit_name: usuallyUnit ? usuallyUnit.unit_name : (product.unit_name || ''),
                    edit_product_name: false,
                    edit_trade_name: false,
                    edit_owner_country: false,
                    edit_producer_country: false,
                    edit_technical_specification: false,
                    price_difference_coefficient: 0,
                    edit_code: false,
                    prices: product.prices || [],
                    price_min: '',
                    price_max: '',
                    price_cost: '',
                }
            }),
        }))

        this.getReceiveAddresses()
        this.$forceUpdate()
    } catch (e) {
        console.error(e)
    }
},
```

- [x] **Step 7: Sửa watcher `formSubmit.project_id`**

Tại line 1297-1300, tìm watcher cho `formSubmit.project_id` liên quan đến type 3/4/5 và sửa thành watch `formSubmit.quotation_id`:
```js
'formSubmit.quotation_id': {
    handler(newVal) {
        if (newVal && (this.formSubmit.type == 3 || this.formSubmit.type == 4 || this.formSubmit.type == 5) && this.quotationOptions.length === 0) {
            this.getQuotationsForContract()
        }
    },
},
```

---

### Task 10: Kiểm tra và dọn dẹp

**Files:**
- Review: Tất cả file đã sửa

- [x] **Step 1: Kiểm tra import Quotation trong ContractService**

Mở `hrm-thanhan-api/Modules/Category/Services/ContractService.php`, kiểm tra đầu file có `use` Quotation model chưa:
```php
use Modules\Category\Entities\Quotation\Quotation;
```
Nếu chưa có, thêm vào.

- [x] **Step 2: Kiểm tra QuotationResource có field cần thiết**

Mở QuotationResource (nếu có), kiểm tra response có trả về `code`, `customer_name`, `project_type` để FE dùng cho dropdown.

- [x] **Step 3: Test thủ công flow mới**

Test theo thứ tự:
1. Tạo dự toán loại Cho/Tặng → Duyệt → Kiểm tra nhận notification phân công báo giá
2. Phân công nhân viên làm báo giá
3. Lập báo giá → Kiểm tra ẩn tab "Thư mời", "Ủy quyền", TotalComponent
4. Kiểm tra bảng hàng hóa ẩn đúng cột
5. Gửi duyệt → TP duyệt → Kiểm tra luôn chuyển CHO_BGĐ_DUYET
6. BGĐ duyệt → Render → Kiểm tra chuyển thẳng hợp đồng
7. Tạo hợp đồng loại Cho/Tặng → Kiểm tra dropdown chọn báo giá
8. Lặp lại test cho loại Đặt/Mượn và Nguyên tắc
9. Test flow cũ (loại Trong thầu, Ngoài thầu) vẫn hoạt động bình thường
