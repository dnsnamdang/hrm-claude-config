# Mẫu in riêng cho hợp đồng lao động — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mỗi hợp đồng lao động lưu bản mẫu in HTML riêng, không còn phụ thuộc vào bảng `print_templates` dùng chung.

**Architecture:** Thêm cột `print_template` (longText) vào bảng `employment_contracts`. Migration backfill data cũ bằng cách copy nội dung từ `print_templates`. FE chuyển sang layout 2 tab với CKEditor cho phép chỉnh sửa mẫu in. BE ưu tiên bản riêng khi in, fallback về FK cũ.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), CKEditor (qua `$loadCKEditor`), Bootstrap-Vue (`b-tabs`, `b-tab`)

---

## Phase 1: Backend

### Task 1: Migration — thêm cột + backfill data cũ

**Files:**
- Create: `hrm-thanhan-api/database/migrations/2026_05_22_160000_add_print_template_column_to_employment_contracts.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class AddPrintTemplateColumnToEmploymentContracts extends Migration
{
    public function up()
    {
        Schema::table('employment_contracts', function (Blueprint $table) {
            $table->longText('print_template')->nullable()->after('print_template_id');
        });

        DB::table('employment_contracts')
            ->whereNotNull('print_template_id')
            ->whereNull('print_template')
            ->orderBy('id')
            ->chunk(100, function ($contracts) {
                foreach ($contracts as $contract) {
                    $template = DB::table('print_templates')
                        ->where('id', $contract->print_template_id)
                        ->value('template');

                    if ($template) {
                        DB::table('employment_contracts')
                            ->where('id', $contract->id)
                            ->update(['print_template' => $template]);
                    }
                }
            });
    }

    public function down()
    {
        Schema::table('employment_contracts', function (Blueprint $table) {
            $table->dropColumn('print_template');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd /hrm-thanhan-api && php artisan migrate
```

Expected: Migration chạy thành công, cột `print_template` được thêm, data cũ được backfill.

- [ ] **Step 3: Verify bằng SQL**

```sql
SELECT id, print_template_id, LEFT(print_template, 100) as preview
FROM employment_contracts
WHERE print_template_id IS NOT NULL
LIMIT 5;
```

Expected: Các record có `print_template_id` giờ cũng có `print_template` chứa nội dung HTML.

---

### Task 2: Sửa validation — cho phép gửi print_template

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Http/Requests/StoreEmployeeContractRequest.php:20-30`

- [ ] **Step 1: Thêm rule print_template**

Trong hàm `rules()`, thêm dòng sau vào mảng return (sau `'print_template_id'`):

```php
'print_template' => 'nullable|string',
```

File sau khi sửa, mảng return đầy đủ:

```php
return [
    'employee_id' => 'required',
    'contracting_unit_id' => 'required|numeric',
    'contract_number' => 'required|unique:employment_contracts,contract_number,' . $id,
    'effective_date' => 'required|date',
    'sign_day' => 'required|date',
    'contract_type' => 'required|numeric',
    'expiration_date' => 'required|date',
    'print_type' => 'required|numeric',
    'print_template_id' => 'required|numeric',
    'print_template' => 'nullable|string',
];
```

---

### Task 3: Sửa logic in — ưu tiên bản riêng

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Http/Controllers/Api/V1/EmploymentContractController.php:239-241`

- [ ] **Step 1: Sửa đoạn lấy template trong hàm `print()`**

Tìm đoạn code (line 239-241):

```php
$template = PrintTemplate::query()->findOrFail($employmentContract->print_template_id);
$template = fillReport($template->template, $result);
$template = clearNull($template);
```

Thay bằng:

```php
if (!empty($employmentContract->print_template)) {
    $templateContent = $employmentContract->print_template;
} else {
    $templateContent = PrintTemplate::query()
        ->findOrFail($employmentContract->print_template_id)
        ->template;
}
$template = fillReport($templateContent, $result);
$template = clearNull($template);
```

- [ ] **Step 2: Verify — test in hợp đồng cũ**

Mở trình duyệt, vào chi tiết một hợp đồng cũ → bấm In → kiểm tra mẫu in hiển thị đúng nội dung.

---

## Phase 2: Frontend

### Task 4: Thêm field `print_template` vào form data

**Files:**
- Modify: `hrm-thanhan-client/pages/human/employment-contract/components/EmploymentContract.vue:318-321`

- [ ] **Step 1: Sửa props default**

Tìm đoạn (line 318-323):

```js
formProps: {
    type: Object,
    default: () => ({
        attached_files: [],
    }),
},
```

Thay bằng:

```js
formProps: {
    type: Object,
    default: () => ({
        attached_files: [],
        print_template: null,
    }),
},
```

---

### Task 5: Chuyển layout sang 2 tab

**Files:**
- Modify: `hrm-thanhan-client/pages/human/employment-contract/components/EmploymentContract.vue:1-304`

- [ ] **Step 1: Bọc nội dung form hiện tại trong b-tabs**

Thay toàn bộ phần `<template>` (line 1-304) bằng:

```vue
<template>
    <div class="card-body">
        <b-tabs content-class="mt-3">
            <b-tab title="Thông tin hợp đồng" active>
                <div class="row">
                    <div class="col-md-12">
                        <h4>Thông tin hợp đồng</h4>
                    </div>
                    <div class="col-md-12">
                        <div v-if="form.reason_deny && form.status == 4">
                            <label style="color: #df4b4b; font-size: 14px">Lý do không ký:</label>
                            <textarea class="form-control" disabled>{{ form.reason_deny }}</textarea>
                        </div>
                    </div>

                    <div class="col-md-12 mt-4">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Họ và tên NLĐ <Required /> </label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            name="name"
                                            v-validate="'required'"
                                            :options="employeesOptions"
                                            v-model="form.employee_id"
                                        ></base-select2>
                                        <span class="text-danger" v-if="errors.first('name')">{{ errors.first('name') }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Đơn vị ký hợp đồng <Required /> </label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            v-validate="'required'"
                                            name="contracting_unit_id"
                                            v-model="form.contracting_unit_id"
                                            :options="companyOptions"
                                        ></base-select2>
                                        <span class="text-danger" v-if="errors.first('contracting_unit_id')">{{
                                            errors.first('contracting_unit_id')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Số hợp đồng <Required /> </label>
                                    <div class="col-sm-8">
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="form.contract_number"
                                            v-validate="'required'"
                                            autocomplete="off"
                                            name="contract_number"
                                        />
                                        <span
                                            class="text-danger"
                                            v-if="errors.first('contract_number') || errorsMsg['contract_number']"
                                            >{{ errors.first('contract_number') || errorsMsg.contract_number[0] }}</span
                                        >
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Tên hợp đồng </label>
                                    <div class="col-sm-8">
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="form.contract_name"
                                            autocomplete="off"
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Thời hạn hợp đồng</label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            name="contract_term"
                                            v-model="form.contract_term"
                                            :settings="{ allowClear: true }"
                                            :options="contractTermOptions"
                                        ></base-select2>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Ngày có hiệu lực <Required /></label>
                                    <div class="col-sm-8">
                                        <base-date-picker
                                            name="effective_date"
                                            v-validate="'required'"
                                            v-model="form.effective_date"
                                        ></base-date-picker>
                                        <span class="text-danger" v-if="errors.first('effective_date')">{{
                                            errors.first('effective_date')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Lương cơ bản</label>
                                    <div class="col-sm-8">
                                        <currency-input
                                            v-model="form.basic_salary"
                                            name="basic_salary"
                                            autocomplete="off"
                                            v-validate="'money_format'"
                                        />
                                        <span class="text-danger" v-if="errors.first('basic_salary')">{{
                                            errors.first('basic_salary')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Tỷ lệ hưởng lương (%)</label>
                                    <div class="col-sm-8">
                                        <input
                                            class="form-control"
                                            type="text"
                                            name="salary_rate"
                                            v-model="form.salary_rate"
                                            autocomplete="off"
                                            v-validate="'decimal|max_value:100'"
                                        />
                                        <span class="text-danger" v-if="errors.first('salary_rate')">{{
                                            errors.first('salary_rate')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Vị trí công việc</label>
                                    <div class="col-sm-8">
                                        <input class="form-control" type="text" v-model="form.position" />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Bộ phận công tác</label>
                                    <div class="col-sm-8">
                                        <input class="form-control" type="text" v-model="form.part" />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Ngày ký <Required /></label>
                                    <div class="col-sm-8">
                                        <base-date-picker
                                            name="sign_day"
                                            v-validate="'required'"
                                            v-model="form.sign_day"
                                        ></base-date-picker>
                                        <span class="text-danger" v-if="errors.first('sign_day')">{{
                                            errors.first('sign_day')
                                        }}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Mã nhân viên <Required /></label>
                                    <div class="col-sm-8">
                                        <input
                                            class="form-control"
                                            type="text"
                                            v-model="form.employee_code"
                                            autocomplete="off"
                                        />
                                    </div>
                                </div>

                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Loại hợp đồng <Required /></label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            v-validate="'required'"
                                            :options="contractTypeOptions"
                                            name="contract_type"
                                            v-model="form.contract_type"
                                        ></base-select2>
                                        <span class="text-danger" v-if="errors.first('contract_type')">{{
                                            errors.first('contract_type')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Hình thức làm việc</label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            :options="workTypeOptions"
                                            name="work_type"
                                            v-model="form.work_type"
                                        ></base-select2>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Ngày hết hạn <Required /></label>
                                    <div class="col-sm-8">
                                        <base-date-picker
                                            name="expiration_date"
                                            v-validate="'required'"
                                            v-model="form.expiration_date"
                                        ></base-date-picker>
                                        <span class="text-danger" v-if="errors.first('expiration_date')">{{
                                            errors.first('expiration_date')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Lương đóng bảo hiểm</label>
                                    <div class="col-sm-8">
                                        <currency-input
                                            v-model="form.social_insurance_salary"
                                            v-validate="'money_format'"
                                            name="social_insurance_salary"
                                            autocomplete="off"
                                        />
                                        <span class="text-danger" v-if="errors.first('social_insurance_salary')">{{
                                            errors.first('social_insurance_salary')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Người đại diện công ty ký</label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            :options="employeesOptions"
                                            name="signer"
                                            v-model="form.signer"
                                            :settings="{ allowClear: true }"
                                        ></base-select2>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Ghi chú</label>
                                    <div class="col-sm-8">
                                        <b-form-textarea
                                            rows="4"
                                            wrap="soft"
                                            class="form-control"
                                            v-model="form.note"
                                        ></b-form-textarea>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Loại mẫu in</label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            v-validate="'required'"
                                            name="print_type"
                                            :options="printTypeOptions"
                                            v-model="form.print_type"
                                        ></base-select2>
                                        <span class="text-danger" v-if="errors.first('print_type')">{{
                                            errors.first('print_type')
                                        }}</span>
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label class="col-sm-4 col-form-label">Mẫu in</label>
                                    <div class="col-sm-8">
                                        <base-select2
                                            name="print_template_id"
                                            :options="printTemplateOptions"
                                            v-model="form.print_template_id"
                                            @input="onChangeTemplate"
                                        ></base-select2>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </b-tab>

            <b-tab title="Mẫu in">
                <div class="row">
                    <div class="col-lg-8">
                        <textarea
                            ref="printEditor"
                            v-model="form.print_template"
                            cols="30"
                            rows="10"
                            data-height="600"
                            name="print_template"
                        ></textarea>
                    </div>
                    <div class="col-lg-4">
                        <div class="table-responsive" style="max-height: 650px; overflow-y: auto">
                            <table class="table table-bordered table-hover">
                                <thead>
                                    <tr>
                                        <th class="text-center">Tên biến</th>
                                        <th class="text-center">Mô tả</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-for="(v, index) in variables">
                                        <tr :key="'group-' + index">
                                            <td colspan="2" class="font-weight-bold">
                                                {{ v.stt }}. {{ v.group }}
                                            </td>
                                        </tr>
                                        <template v-for="(obj, oIndex) in v.objects">
                                            <template v-for="(item, iIndex) in obj.items">
                                                <tr :key="'var-' + index + '-' + oIndex + '-' + iIndex">
                                                    <td>{{ item.name }}</td>
                                                    <td>{{ item.description }}</td>
                                                </tr>
                                            </template>
                                        </template>
                                    </template>
                                    <tr v-if="!variables.length">
                                        <td colspan="2" class="text-center">Chưa có dữ liệu</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </b-tab>
        </b-tabs>
    </div>
</template>
```

---

### Task 6: Thêm logic CKEditor + methods + watchers

**Files:**
- Modify: `hrm-thanhan-client/pages/human/employment-contract/components/EmploymentContract.vue` (script section)

- [ ] **Step 1: Thêm data variables**

Trong `data()`, thêm 2 field mới vào object return (sau `workTypeOptions`):

```js
printEditor: null,
variables: [],
```

- [ ] **Step 2: Sửa watcher `form.print_type` và thêm watcher mới**

Tìm đoạn watch (line 359-372):

```js
watch: {
    'form.employee_id': function (newVal) {
        this.form.employee_code = this.employeesOptions.find((employee) => employee.id == newVal)?.code
    },
    'form.print_type': function (newVal) {
        this.onChangePrintType()
    },
    form: {
        deep: true,
        handler() {
            this.$emit('update:errorsMsg', [])
        },
    },
},
```

Thay bằng:

```js
watch: {
    'form.employee_id': function (newVal) {
        this.form.employee_code = this.employeesOptions.find((employee) => employee.id == newVal)?.code
    },
    'form.print_type': function (newVal) {
        this.onChangePrintTypeAndGetVariables(newVal)
    },
    'form.print_template': function (newVal) {
        if (this.printEditor && newVal !== this.printEditor.getData()) {
            this.printEditor.setData(newVal || '')
        }
    },
    form: {
        deep: true,
        handler() {
            this.$emit('update:errorsMsg', [])
        },
    },
},
```

- [ ] **Step 3: Thêm init CKEditor trong mounted**

Tìm đoạn `mounted()` (line 404-408):

```js
mounted() {
    if (this.form.print_type) {
        this.onChangePrintType()
    }
},
```

Thay bằng:

```js
mounted() {
    if (this.form.print_type) {
        this.onChangePrintTypeAndGetVariables(this.form.print_type, { resetTemplate: false })
    }
    this.$nextTick(() => {
        if (this.$refs.printEditor) {
            this.$loadCKEditor(this.$refs.printEditor).then((editor) => {
                this.printEditor = editor

                this.printEditor.on('change', () => {
                    this.form.print_template = this.printEditor.getData()
                })

                this.printEditor.on('instanceReady', () => {
                    this.printEditor.setData(this.form.print_template || '')
                })
            })
        }
    })
},
```

- [ ] **Step 4: Thay method `onChangePrintType` và thêm methods mới**

Tìm method `onChangePrintType` (line 464-476):

```js
async onChangePrintType() {
    console.log(this.form.print_type, 123)
    const api_url = 'human/print-templates'
    this.isBusy = true
    const params = {
        type: this.form.print_type,
    }

    const response = await this.$store.dispatch('apiGet', `${api_url}${buildQueryString(params)}`)
    this.printTemplateOptions = response.data.data.map(function (item, index) {
        return { id: item.id, text: item.name }
    })
},
```

Thay bằng 3 methods:

```js
async onChangePrintTypeAndGetVariables(newVal, options = { resetTemplate: true }) {
    if (typeof newVal !== 'undefined') this.form.print_type = newVal

    this.variables = []
    this.printTemplateOptions = []

    if (options && options.resetTemplate) {
        this.form.print_template_id = null
        this.form.print_template = ''
        if (this.printEditor) this.printEditor.setData('')
    }

    await this.$nextTick()
    await Promise.all([this.onChangePrintType(), this.getVariables()])
},

async onChangePrintType() {
    const api_url = 'human/print-templates'
    const params = {
        type: this.form.print_type,
    }
    const response = await this.$store.dispatch('apiGet', `${api_url}${buildQueryString(params)}`)
    this.printTemplateOptions = response.data.data.map(function (item) {
        return { id: item.id, text: item.name }
    })
},

async onChangeTemplate() {
    if (!this.form.print_template_id) {
        this.form.print_template = ''
        if (this.printEditor) this.printEditor.setData('')
        return
    }
    const response = await this.$store.dispatch('apiGet', `human/print-templates/${this.form.print_template_id}`)
    this.form.print_template = response.data.data.template
    if (this.printEditor) this.printEditor.setData(this.form.print_template)
},

async getVariables() {
    if (!this.form.print_type) return
    const params = { template_type_id: this.form.print_type }
    const response = await this.$store.dispatch(
        'apiGetMethod',
        `human/print-template-variables/get-variables${buildQueryString(params)}`
    )
    this.variables = response.data
},
```

---

## Phase 3: Verify

### Task 7: Test end-to-end

- [ ] **Step 1: Test tạo mới hợp đồng**

1. Mở `/human/employment-contract/add`
2. Điền thông tin Tab 1 → chọn Loại mẫu in → chọn Mẫu in
3. Chuyển Tab 2 → kiểm tra CKEditor hiển thị nội dung template + bảng biến bên phải
4. Tùy chỉnh nội dung trong CKEditor
5. Submit → kiểm tra lưu thành công

- [ ] **Step 2: Test edit hợp đồng vừa tạo**

1. Mở hợp đồng vừa tạo → Edit
2. Tab 2 → kiểm tra CKEditor hiển thị nội dung đã tùy chỉnh
3. Sửa thêm → Submit → kiểm tra cập nhật đúng

- [ ] **Step 3: Test in hợp đồng**

1. Mở chi tiết hợp đồng vừa tạo → bấm In
2. Kiểm tra mẫu in hiển thị đúng nội dung đã tùy chỉnh (không phải mẫu gốc)
3. Kiểm tra các biến (SO_HOP_DONG, TEN_NHAN_SU, ...) được thay thế đúng

- [ ] **Step 4: Test hợp đồng cũ không bị ảnh hưởng**

1. Mở một hợp đồng cũ (tạo trước migration) → bấm In
2. Kiểm tra mẫu in hiển thị đúng nội dung (đã được backfill từ migration)
3. Edit hợp đồng cũ → Tab 2 hiển thị nội dung trong CKEditor

- [ ] **Step 5: Test đổi mẫu gốc không ảnh hưởng hợp đồng đã lưu**

1. Vào quản lý mẫu in → sửa nội dung một mẫu gốc
2. Mở hợp đồng đã dùng mẫu đó → In → nội dung vẫn là bản cũ (không bị thay đổi theo)
