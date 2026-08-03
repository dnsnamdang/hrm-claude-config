# Loại hình tổ chức & Lĩnh vực khách hàng (HRM) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Quy ước HRM (CLAUDE.md):** KHÔNG commit/đẩy git. Verify bằng `php -l`, `php artisan tinker`, `npm run lint`, `npm run build`, và browser. Mọi form validate: BE rethrow `ValidationException`, FE hiện lỗi inline (`field-required`/`is-invalid`). Làm việc tiếng Việt.

**Goal:** Bổ sung trường "Loại hình tổ chức" (5 loại) + 2 trường bắt buộc "Nhóm lĩnh vực khách hàng" và "Lĩnh vực khách hàng" (đồng bộ 2 chiều) trên form/khoá tìm kiếm khách hàng HRM, tái dùng catalog có sẵn ở `Modules/Assign`.

**Architecture:** Bảng `customers` thêm 2 cột nullable (`customer_scope_group_id`, `customer_scope_id`); `required` chỉ ở tầng validate. FE nạp danh mục qua 2 endpoint `getAll` có sẵn (không cần đổi BE catalog) và xử lý lọc/đồng bộ 2 chiều hoàn toàn client-side trong component dùng chung `CustomerScopeSelect.vue`. `customer_type` giữ kiểu int, value `2` ('Tổ chức') đổi nhãn thành 'Doanh nghiệp tư nhân', thêm `3,4,5` dùng chung layout tổ chức.

**Tech Stack:** Laravel 8 (Modules/Human, Modules/Assign), Nuxt 2 / Vue 2, vue-multiselect, Bootstrap-Vue.

**Spec:** `.plans/customer-org-type-and-scope/design.md`

---

## File Structure

**Backend (Modules/Human):**

- Create: `hrm-api/Modules/Human/Database/Migrations/2026_06_09_000001_add_customer_scope_fields_to_customers_table.php` — 2 cột mới.
- Modify: `hrm-api/Modules/Human/Entities/Customer.php` — `CUSTOMER_TYPES`, `$fillable`, quan hệ `scopeGroup`/`scope`.
- Modify: `hrm-api/Modules/Human/Http/Requests/SaveCustomerRequest.php` — rule + nhánh org.
- Modify: `hrm-api/Modules/Human/Http/Requests/UpdateCustomerRequest.php` — rule + nhánh org.
- Modify: `hrm-api/Modules/Human/Services/CustomerService.php` — `createCustomer`/`updateCustomer`.

**Frontend (hrm-client):**

- Create: `hrm-client/components/human-components/customer/CustomerScopeSelect.vue` — 2 dropdown + đồng bộ 2 chiều.
- Modify: `hrm-client/components/human-components/customer/CustomerForm.vue` — nhãn, options, `isOrganization`, nhúng component.
- Modify: `hrm-client/pages/human/customers/index.vue` — nhãn filter + cột + options.

**Không đụng:** catalog CRUD ở `Modules/Assign` (đã có); endpoint `getAll` đã đủ dùng.

---

## PHASE 1 — BACKEND (Modules/Human)

### Task 1: Migration thêm 2 cột vào `customers`

**Files:**

- Create: `hrm-api/Modules/Human/Database/Migrations/2026_06_09_000001_add_customer_scope_fields_to_customers_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddCustomerScopeFieldsToCustomersTable extends Migration
{
    public function up()
    {
        Schema::table('customers', function (Blueprint $table) {
            $table->unsignedBigInteger('customer_scope_group_id')->nullable()->after('customer_type')
                ->comment('Nhóm lĩnh vực khách hàng');
            $table->unsignedBigInteger('customer_scope_id')->nullable()->after('customer_scope_group_id')
                ->comment('Lĩnh vực khách hàng');
        });
    }

    public function down()
    {
        Schema::table('customers', function (Blueprint $table) {
            $table->dropColumn(['customer_scope_group_id', 'customer_scope_id']);
        });
    }
}
```

> Ghi chú: KHÔNG thêm `foreign()` cứng — catalog nằm cùng DB nhưng để nullable + không ràng buộc FK cứng (tránh chặn xoá danh mục; nhất quán với cách `prospective_projects` chỉ thêm `customer_scope_id` không FK). Ràng buộc hợp lệ kiểm ở tầng validate.

- [ ] **Step 2: Chạy migration**

Run: `cd hrm-api && php artisan migrate --path=Modules/Human/Database/Migrations/2026_06_09_000001_add_customer_scope_fields_to_customers_table.php`
Expected: `Migrated: ...add_customer_scope_fields_to_customers_table`

- [ ] **Step 3: Verify cột tồn tại**

Run: `cd hrm-api && php artisan tinker --execute="echo implode(',', \Illuminate\Support\Facades\Schema::getColumnListing('customers'));"`
Expected: chuỗi cột có chứa `customer_scope_group_id` và `customer_scope_id`.

---

### Task 2: Customer entity — CUSTOMER_TYPES, fillable, quan hệ

**Files:**

- Modify: `hrm-api/Modules/Human/Entities/Customer.php`

- [ ] **Step 1: Cập nhật hằng `CUSTOMER_TYPES`** (đang ở dòng ~22)

Thay khối:

```php
    public const CUSTOMER_TYPES = [
        [
            'id' => 1,
            'name' => 'Cá nhân'
        ],
        [
            'id' => 2,
            'name' => 'Tổ chức'
        ]
    ];
```

bằng:

```php
    public const CUSTOMER_TYPES = [
        ['id' => 1, 'name' => 'Cá nhân'],
        ['id' => 2, 'name' => 'Doanh nghiệp tư nhân'],
        ['id' => 3, 'name' => 'Doanh nghiệp nước ngoài'],
        ['id' => 4, 'name' => 'Tổ chức phi chính phủ'],
        ['id' => 5, 'name' => 'Cơ quan nhà nước'],
    ];
```

- [ ] **Step 2: Thêm 2 cột vào `$fillable`**

Trong mảng `$fillable` (sau `'customer_type',`) thêm:

```php
        'customer_scope_group_id',
        'customer_scope_id',
```

- [ ] **Step 3: Thêm 2 quan hệ** (đặt cạnh các quan hệ `belongsTo` khác, vd sau `ward()`)

```php
    public function scopeGroup()
    {
        return $this->belongsTo(\Modules\Assign\Entities\CustomerScopeGroup\CustomerScopeGroup::class, 'customer_scope_group_id');
    }

    public function scope()
    {
        return $this->belongsTo(\Modules\Assign\Entities\CustomerScope\CustomerScope::class, 'customer_scope_id');
    }
```

- [ ] **Step 4: Verify cú pháp**

Run: `cd hrm-api && php -l Modules/Human/Entities/Customer.php`
Expected: `No syntax errors detected`

- [ ] **Step 5: Verify text loại hình mới**

Run: `cd hrm-api && php artisan tinker --execute="\$c = new \Modules\Human\Entities\Customer(); \$c->customer_type = 4; echo \$c->customer_type_text;"`
Expected: `Tổ chức phi chính phủ`

---

### Task 3: Validation — SaveCustomerRequest & UpdateCustomerRequest

**Files:**

- Modify: `hrm-api/Modules/Human/Http/Requests/SaveCustomerRequest.php`
- Modify: `hrm-api/Modules/Human/Http/Requests/UpdateCustomerRequest.php`

- [ ] **Step 1: SaveCustomerRequest — mở rộng `customer_type` + thêm rule scope**

Trong `rules()`, đổi dòng:

```php
            'customer_type' => 'required|in:1,2',
```

thành:

```php
            'customer_type' => 'required|in:1,2,3,4,5',
            'customer_scope_group_id' => 'required|exists:customer_scope_groups,id',
            'customer_scope_id' => ['required', 'exists:customer_scopes,id',
                function ($attribute, $value, $fail) {
                    $belongs = DB::table('customer_scope_group_members')
                        ->where('customer_scope_id', $value)
                        ->where('customer_scope_group_id', $this->customer_scope_group_id)
                        ->exists();
                    if (!$belongs) {
                        $fail('Lĩnh vực không thuộc nhóm lĩnh vực đã chọn');
                    }
                }],
```

> `DB` đã `use Illuminate\Support\Facades\DB;` sẵn trong file — không cần thêm import.

- [ ] **Step 2: SaveCustomerRequest — áp rule tổ chức cho mọi loại ≠ Cá nhân**

Đổi nhánh:

```php
        } else if ($this->customer_type == 2) {
```

thành:

```php
        } else {
```

(Cá nhân là `== 1` ở nhánh `if` phía trên; mọi loại còn lại 2–5 dùng chung rule tổ chức.)

- [ ] **Step 3: SaveCustomerRequest — thêm message lỗi**

Trong `messages()`, thêm:

```php
            'customer_scope_group_id.required' => 'Bắt buộc nhập',
            'customer_scope_group_id.exists' => 'Không tồn tại',
            'customer_scope_id.required' => 'Bắt buộc nhập',
            'customer_scope_id.exists' => 'Không tồn tại',
```

- [ ] **Step 4: UpdateCustomerRequest — lặp lại Step 1–3 y hệt** trong `hrm-api/Modules/Human/Http/Requests/UpdateCustomerRequest.php`

Đổi `'customer_type' => 'required|in:1,2',` → `'required|in:1,2,3,4,5',` + thêm 2 rule scope (giống Step 1).
Đổi `} else if ($this->customer_type == 2) {` → `} else {`.
Thêm 4 dòng message (giống Step 3).

- [ ] **Step 5: Verify cú pháp cả 2 file**

Run: `cd hrm-api && php -l Modules/Human/Http/Requests/SaveCustomerRequest.php && php -l Modules/Human/Http/Requests/UpdateCustomerRequest.php`
Expected: `No syntax errors detected` (cả 2)

---

### Task 4: CustomerService — lưu scope + mở rộng nhánh tổ chức

**Files:**

- Modify: `hrm-api/Modules/Human/Services/CustomerService.php` (`createCustomer` ~407, `updateCustomer` ~483)

- [ ] **Step 1: `createCustomer` — đổi nhánh tổ chức `== 2` → `else`**

Đổi (dòng ~423):

```php
        } else if ($request->customer_type == 2) {
            if ($request->parent_id) {
                $parent = Customer::where('id', $request->parent_id)
                    ->where('customer_type', 2)
```

thành:

```php
        } else {
            if ($request->parent_id) {
                $parent = Customer::where('id', $request->parent_id)
                    ->where('customer_type', '!=', 1)
```

- [ ] **Step 2: `createCustomer` — gán scope trước `$customer->save();`**

Ngay trước dòng `$customer->save();` (dòng ~472, sau `$customer->code = $request->code;`) thêm:

```php
        $customer->customer_scope_group_id = $request->customer_scope_group_id;
        $customer->customer_scope_id = $request->customer_scope_id;
```

- [ ] **Step 3: `createCustomer` — đồng bộ contacts/deputies cho mọi loại tổ chức**

Đổi (dòng ~474):

```php
        if ($request->customer_type == 2) {
            $customer->syncContacts($request->contacts);

            $customer->syncDeputies($request->deputies);
        }
```

thành:

```php
        if ($request->customer_type != 1) {
            $customer->syncContacts($request->contacts);

            $customer->syncDeputies($request->deputies);
        }
```

- [ ] **Step 4: `updateCustomer` — lặp lại Step 1–3 cho hàm `updateCustomer`**

Đổi `} else if ($request->customer_type == 2) {` → `} else {` và `->where('customer_type', 2)` → `->where('customer_type', '!=', 1)` (dòng ~498–501).
Thêm 2 dòng gán scope trước `$customer->save();` (dòng ~547).
Đổi `if ($request->customer_type == 2) {` (dòng ~549) → `if ($request->customer_type != 1) {`.

- [ ] **Step 5: Verify cú pháp**

Run: `cd hrm-api && php -l Modules/Human/Services/CustomerService.php`
Expected: `No syntax errors detected`

- [ ] **Step 6: Verify show() trả về scope ids cho prefill**

`show()` trả entity gốc nên 2 cột tự có trong response. Xác nhận:
Run: `cd hrm-api && php artisan tinker --execute="echo json_encode(array_keys((new \Modules\Human\Services\CustomerService())->_model->first()->toArray() ?? []));"`
Expected: danh sách key có `customer_scope_group_id`, `customer_scope_id` (nếu có ít nhất 1 customer). Nếu lỗi khởi tạo service, bỏ qua — đã xác nhận là cột bảng ở Task 1.

---

## PHASE 2 — FRONTEND (hrm-client)

### Task 5: Component dùng chung `CustomerScopeSelect.vue`

**Files:**

- Create: `hrm-client/components/human-components/customer/CustomerScopeSelect.vue`

Component nhận `group-id`/`scope-id` (sync), `errors`, `is-show`; tự nạp danh mục qua `getAll`; xử lý đồng bộ 2 chiều client-side.

- [ ] **Step 1: Tạo file component**

```vue
<template>
  <div class="row">
    <div class="col-xl-6">
      <div class="form-group">
        <label class="form-label"
          >Nhóm lĩnh vực khách hàng<span class="field-required"
            >(*)</span
          ></label
        >
        <multiselect
          track-by="id"
          label="name"
          placeholder="Chọn nhóm lĩnh vực"
          :value="selectedGroup"
          :options="groupOptions"
          :disabled="isShow"
          @select="onSelectGroup($event)"
        >
          <template slot="singleLabel" slot-scope="{ option }">{{
            option.name
          }}</template>
          <template slot="noResult">Không tìm thấy</template>
        </multiselect>
        <span v-if="errors['customer_scope_group_id']" class="field-required">{{
          errors["customer_scope_group_id"][0]
        }}</span>
      </div>
    </div>
    <div class="col-xl-6">
      <div class="form-group">
        <label class="form-label"
          >Lĩnh vực khách hàng<span class="field-required">(*)</span></label
        >
        <multiselect
          track-by="id"
          label="name"
          placeholder="Chọn lĩnh vực"
          :value="selectedScope"
          :options="scopeOptions"
          :disabled="isShow"
          @select="onSelectScope($event)"
        >
          <template slot="singleLabel" slot-scope="{ option }">{{
            option.name
          }}</template>
          <template slot="noResult">Không tìm thấy</template>
        </multiselect>
        <span v-if="errors['customer_scope_id']" class="field-required">{{
          errors["customer_scope_id"][0]
        }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  components: { Multiselect },
  props: {
    groupId: { type: [Number, String], default: null },
    scopeId: { type: [Number, String], default: null },
    errors: { type: [Object, Array], default: () => ({}) },
    isShow: { type: Boolean, default: false },
  },
  data() {
    return {
      groups: [], // [{id, name}]
      scopes: [], // [{id, name, groups: [{id}]}]
    };
  },
  computed: {
    selectedGroup() {
      return this.groups.find((g) => g.id == this.groupId) || null;
    },
    selectedScope() {
      return this.scopes.find((s) => s.id == this.scopeId) || null;
    },
    // Lĩnh vực hiển thị: lọc theo nhóm đang chọn (Top-Down). Chưa chọn nhóm → hiện tất cả.
    scopeOptions() {
      if (!this.groupId) return this.scopes;
      return this.scopes.filter((s) =>
        (s.groups || []).some((g) => g.id == this.groupId),
      );
    },
    // Nhóm hiển thị: nếu đã chọn lĩnh vực → chỉ các nhóm hợp lệ của lĩnh vực đó.
    groupOptions() {
      if (!this.scopeId) return this.groups;
      const scope = this.scopes.find((s) => s.id == this.scopeId);
      if (!scope) return this.groups;
      const ids = (scope.groups || []).map((g) => g.id);
      return this.groups.filter((g) => ids.includes(g.id));
    },
  },
  mounted() {
    this.loadGroups();
    this.loadScopes();
  },
  methods: {
    async loadGroups() {
      const res = await this.$store.dispatch(
        "apiGet",
        "assign/customer-scope-groups/getAll",
      );
      if (res.data && res.data.code == 200) {
        this.groups = (res.data.data || []).map((g) => ({
          id: g.id,
          name: g.name,
        }));
      }
    },
    async loadScopes() {
      const res = await this.$store.dispatch(
        "apiGet",
        "assign/customer-scopes/getAll",
      );
      if (res.data && res.data.code == 200) {
        this.scopes = (res.data.data || []).map((s) => ({
          id: s.id,
          name: s.name,
          groups: (s.groups || []).map((g) => ({ id: g.id })),
        }));
      }
    },
    onSelectGroup(group) {
      this.$emit("update:groupId", group.id);
      // Top-Down: nếu lĩnh vực đang chọn không thuộc nhóm mới → reset lĩnh vực
      const scope = this.scopes.find((s) => s.id == this.scopeId);
      if (scope && !(scope.groups || []).some((g) => g.id == group.id)) {
        this.$emit("update:scopeId", null);
      }
    },
    onSelectScope(scope) {
      this.$emit("update:scopeId", scope.id);
      // Bottom-Up: 1 nhóm → auto-fill; nhiều nhóm → để người dùng chọn
      const groupIds = (scope.groups || []).map((g) => g.id);
      if (groupIds.length === 1) {
        this.$emit("update:groupId", groupIds[0]);
      } else if (
        !groupIds.includes(Number(this.groupId)) &&
        !groupIds.includes(this.groupId)
      ) {
        // nhóm hiện tại không hợp lệ với lĩnh vực mới → xoá để buộc chọn lại
        this.$emit("update:groupId", null);
      }
    },
  },
};
</script>
```

> Endpoint `getAll` không gắn `checkPermission` nên mọi user tạo/sửa KH đều gọi được. `customer-scopes/getAll` trả mỗi scope kèm `groups: [{id}]` (đã eager-load `with('groups:id')`).

- [ ] **Step 2: Verify build component không lỗi parse**

Run: `cd hrm-client && npx eslint components/human-components/customer/CustomerScopeSelect.vue`
Expected: không có error (warning về style cho phép).

---

### Task 6: CustomerForm.vue — nhãn, options, isOrganization, nhúng component

**Files:**

- Modify: `hrm-client/components/human-components/customer/CustomerForm.vue`

- [ ] **Step 1: Đổi nhãn "Đối tượng" → "Loại hình tổ chức"** (dòng ~36)

Đổi:

```html
                                                >Đối tượng<span class="field-required">(*)</span></label
```

thành:

```html
                                                >Loại hình tổ chức<span class="field-required">(*)</span></label
```

- [ ] **Step 2: Cập nhật `listCustomerType` (data, dòng ~1080)**

Đổi:

```js
            listCustomerType: [
                { value: 1, text: 'Cá nhân' },
                { value: 2, text: 'Tổ chức' },
            ],
```

thành:

```js
            listCustomerType: [
                { value: 1, text: 'Cá nhân' },
                { value: 2, text: 'Doanh nghiệp tư nhân' },
                { value: 3, text: 'Doanh nghiệp nước ngoài' },
                { value: 4, text: 'Tổ chức phi chính phủ' },
                { value: 5, text: 'Cơ quan nhà nước' },
            ],
```

- [ ] **Step 3: Thêm 2 trường scope vào `form` (data, trong object `form`)**

Sau `customer_type: null,` thêm:

```js
                customer_scope_group_id: null,
                customer_scope_id: null,
```

- [ ] **Step 4: Thêm computed `isOrganization`** (trong `computed: {}`)

```js
        isOrganization() {
            return [2, 3, 4, 5].includes(Number(this.form.customer_type))
        },
```

- [ ] **Step 5: Thay điều kiện template `form.customer_type == 2` → `isOrganization`**

Dùng Edit `replace_all` đổi mọi `v-if="form.customer_type == 2"` thành `v-if="isOrganization"` trong file (các dòng ~296, 394, 683, 746). Giữ nguyên `v-if="form.customer_type == 1"` (Cá nhân).

> Verify sau khi đổi: `grep -c "form.customer_type == 2" CustomerForm.vue` phải = 0; `grep -c "isOrganization" CustomerForm.vue` ≥ 5 (1 computed + ≥4 template).

- [ ] **Step 6: Import + đăng ký component `CustomerScopeSelect`**

Trong block `import` (đầu `<script>`), thêm:

```js
import CustomerScopeSelect from "@/components/human-components/customer/CustomerScopeSelect";
```

Trong `components: {}` thêm `CustomerScopeSelect,`.

- [ ] **Step 7: Nhúng component vào form**

Ngay sau khối `col-xl-4` chứa select "Loại hình tổ chức" (sau thẻ đóng `</div>` của col đó, dòng ~50), thêm:

```html
<div class="col-xl-12">
  <CustomerScopeSelect
    :group-id="form.customer_scope_group_id"
    :scope-id="form.customer_scope_id"
    :errors="errors"
    :is-show="isShow"
    @update:groupId="form.customer_scope_group_id = $event"
    @update:scopeId="form.customer_scope_id = $event"
  />
</div>
```

> Hai trường này áp dụng cho MỌI loại hình (cả Cá nhân và tổ chức) nên đặt ngoài các khối điều kiện `customer_type`.

- [ ] **Step 8: Verify lint**

Run: `cd hrm-client && npx eslint components/human-components/customer/CustomerForm.vue`
Expected: không có error.

---

### Task 7: customers/index.vue — filter + cột + options

**Files:**

- Modify: `hrm-client/pages/human/customers/index.vue`

- [ ] **Step 1: Đổi nhãn cột (dòng ~287)**

Đổi:

```js
                    key: 'customer_type_text',
                    label: 'Đối tượng',
```

thành:

```js
                    key: 'customer_type_text',
                    label: 'Loại hình tổ chức',
```

- [ ] **Step 2: Cập nhật `listCustomerType` (dòng ~328)**

Đổi:

```js
            listCustomerType: [
                { id: 1, value: 1, text: 'Cá nhân' },
                { id: 2, value: 2, text: 'Tổ chức' },
            ],
```

thành:

```js
            listCustomerType: [
                { id: 1, value: 1, text: 'Cá nhân' },
                { id: 2, value: 2, text: 'Doanh nghiệp tư nhân' },
                { id: 3, value: 3, text: 'Doanh nghiệp nước ngoài' },
                { id: 4, value: 4, text: 'Tổ chức phi chính phủ' },
                { id: 5, value: 5, text: 'Cơ quan nhà nước' },
            ],
```

- [ ] **Step 3: (Kiểm tra) nhãn filter "Đối tượng"** trên template (gần `v-model="formFilter.customer_type"`, dòng ~62). Nếu có text/label "Đối tượng" cạnh filter → đổi thành "Loại hình tổ chức".

- [ ] **Step 4: Xác nhận không còn "Nhóm khách hàng"**

Run: `cd hrm-client && grep -ni "Nhóm khách hàng\|customer_group" pages/human/customers/index.vue components/human-components/customer/CustomerForm.vue`
Expected: không có kết quả (HRM vốn không có field này — chỉ xác nhận).

- [ ] **Step 5: Verify lint**

Run: `cd hrm-client && npx eslint pages/human/customers/index.vue`
Expected: không có error.

---

## PHASE 3 — VERIFY TỔNG THỂ

### Task 8: Kiểm thử end-to-end

- [ ] **Step 1: Build FE**

Run: `cd hrm-client && npm run build`
Expected: build PASS, không lỗi compile.

- [ ] **Step 2: Verify BE validate qua tinker (thiếu scope → 422)**

Run:

```bash
cd hrm-api && php artisan tinker --execute="
\$r = new \Modules\Human\Http\Requests\SaveCustomerRequest();
\$rules = \$r->merge(['customer_type' => 2])->rules();
echo array_key_exists('customer_scope_group_id', \$rules) && array_key_exists('customer_scope_id', \$rules) ? 'OK rules' : 'MISSING';
"
```

Expected: `OK rules`

- [ ] **Step 3: Browser — Tạo khách hàng (Cá nhân)**
  - Mở `/human/customers/add`, chọn Loại hình tổ chức = "Cá nhân".
  - Bỏ trống Nhóm/Lĩnh vực → bấm Lưu → thấy lỗi inline đỏ "Bắt buộc nhập" tại cả 2 ô.
  - Chọn Nhóm → ô Lĩnh vực chỉ hiện lĩnh vực thuộc nhóm (Top-Down). Lưu thành công.

- [ ] **Step 4: Browser — Đồng bộ 2 chiều (Bottom-Up)**
  - Tạo mới, KHÔNG chọn nhóm, gõ tìm 1 lĩnh vực **chỉ thuộc 1 nhóm** (vd "Chung cư") → Nhóm tự điền.
  - Chọn lĩnh vực **thuộc nhiều nhóm** (vd "Bệnh viện") → Nhóm KHÔNG tự điền, danh sách Nhóm chỉ còn các nhóm hợp lệ; buộc chọn 1 mới lưu được.

- [ ] **Step 5: Browser — Loại hình tổ chức (2–5)**
  - Lần lượt chọn "Doanh nghiệp tư nhân", "Doanh nghiệp nước ngoài", "Tổ chức phi chính phủ", "Cơ quan nhà nước" → đều hiện form tổ chức (deputies/contacts/tax_code) giống nhau. Lưu thành công với scope hợp lệ.

- [ ] **Step 6: Browser — Sửa khách hàng (prefill)**
  - Mở `/human/customers/:id/edit` của KH vừa tạo → Nhóm + Lĩnh vực hiển thị đúng giá trị đã lưu; danh sách Lĩnh vực đã lọc theo nhóm. Đổi nhóm → lĩnh vực reset nếu không hợp lệ. Lưu thành công.
  - Mở 1 KH CŨ (chưa có scope) → form bắt chọn Nhóm/Lĩnh vực trước khi lưu (không backfill tự động).

- [ ] **Step 7: Browser — Danh sách + tìm kiếm**
  - `/human/customers`: cột "Loại hình tổ chức" hiển thị đúng 5 nhãn; filter "Loại hình tổ chức" có 5 lựa chọn, lọc đúng.

- [ ] **Step 8: Cập nhật STATUS.md** → chuyển `customer-org-type-and-scope` sang trạng thái phù hợp (CODE DONE / chờ user verify), KHÔNG commit git.

---

## Self-Review (đã rà với spec)

- **Loại hình tổ chức (5 loại, rename value 2):** Task 2 (const), Task 6 Step 2 (FE form), Task 7 Step 2 (list). ✅
- **2 trường scope bắt buộc + searchable:** Task 1 (DB), Task 3 (validate required), Task 5 (component searchable). ✅
- **Đồng bộ 2 chiều (Top-Down/Bottom-Up đa nhóm):** Task 5 Step 1 (`scopeOptions`/`groupOptions`/`onSelectGroup`/`onSelectScope`). ✅
- **Required chỉ khi tạo/sửa, không backfill:** cột nullable (Task 1), required ở Request (Task 3), không có seeder backfill. ✅
- **Ẩn "Nhóm khách hàng":** Task 7 Step 4 xác nhận HRM không có (no-op an toàn). ✅
- **Tái dùng catalog Assign, không sửa BE catalog:** dùng `getAll` sẵn có (Task 5). ✅
- **Org types 2–5 dùng chung layout + rule + sync deputies/contacts:** Task 3 Step 2/4 (`else`), Task 4 (service `!= 1`), Task 6 Step 4–5 (`isOrganization`). ✅
- **Hiện lỗi inline:** dùng `errors['field']` + `field-required` (Task 3 messages, Task 5/6 template). ✅
