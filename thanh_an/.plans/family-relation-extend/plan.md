# Mở rộng mối quan hệ gia đình — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm 3 loại mối quan hệ mới (Ông, Bà, Khác) vào phần Thông tin gia đình, với ô text tự do khi chọn "Khác".

**Architecture:** Thêm cột `relation_other_text` vào 2 bảng DB. Cập nhật constant + fillable + service BE. Thêm 3 entry vào dropdown FE + conditional text input theo pattern "Nguồn tiếp nhận".

**Tech Stack:** Laravel 8, PHP 7.4, MySQL, Nuxt 2 (Vue 2), Bootstrap-Vue

**Spec:** `docs/superpowers/specs/2026-05-21-family-relation-extend-design.md`

---

### Task 1: Migration — Thêm cột `relation_other_text`

**Files:**
- Create: `hrm-thanhan-api/Modules/Human/Database/Migrations/2026_05_21_000001_add_relation_other_text_to_employee_relationships_table.php`

- [x] **Step 1: Tạo migration file**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddRelationOtherTextToEmployeeRelationshipsTable extends Migration
{
    public function up()
    {
        Schema::table('employee_relationships', function (Blueprint $table) {
            $table->string('relation_other_text', 255)->nullable()->after('relation');
        });

        Schema::table('employee_relationship_tmps', function (Blueprint $table) {
            $table->string('relation_other_text', 255)->nullable()->after('relation');
        });
    }

    public function down()
    {
        Schema::table('employee_relationships', function (Blueprint $table) {
            $table->dropColumn('relation_other_text');
        });

        Schema::table('employee_relationship_tmps', function (Blueprint $table) {
            $table->dropColumn('relation_other_text');
        });
    }
}
```

- [x] **Step 2: Chạy migration**

Run: `php artisan migrate`

Expected: Migration chạy thành công, 2 bảng đều có cột `relation_other_text` mới.

---

### Task 2: Model — Cập nhật constant + fillable

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationship.php:12-42`
- Modify: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipTmp.php:13-27`

- [x] **Step 1: Cập nhật EmployeeRelationship model**

Trong `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationship.php`:

Thêm `'relation_other_text'` vào `$fillable` (sau `'relation'`, dòng 16):

```php
protected $fillable = [
    'employee_info_id',
    'name',
    'birthday',
    'relation',
    'relation_other_text',
    'job',
    'phone_number',
    'address',
    'is_dependent',
    'dependent_start_date',
    'dependent_end_date',
];
```

Thêm 3 entry vào `RELATIONSHIP_TYPE` constant (dòng 32-42):

```php
public const RELATIONSHIP_TYPE = [
    0 => 'Bố',
    1 => 'Mẹ',
    2 => 'Anh trai',
    3 => 'Chị gái',
    4 => 'Vợ/chồng',
    5 => 'Em trai',
    6 => 'Em gái',
    7 => 'Con trai',
    8 => 'Con gái',
    9 => 'Ông',
    10 => 'Bà',
    11 => 'Khác',
];
```

- [x] **Step 2: Cập nhật EmployeeRelationshipTmp model**

Trong `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipTmp.php`:

Thêm `'relation_other_text'` vào `$fillable` (sau `'relation'`, dòng 19):

```php
protected $fillable = [
    'employee_relationship_id',
    'employee_update_request_id',
    'employee_info_id',
    'name',
    'birthday',
    'relation',
    'relation_other_text',
    'job',
    'phone_number',
    'address',
    'is_dependent',
    'dependent_start_date',
    'dependent_end_date',
];
```

---

### Task 3: Service — Lưu `relation_other_text` khi sync

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoService.php:536-542`
- Modify: `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoUpdateRequestService.php:789-795,818-824`

- [x] **Step 1: Cập nhật EmployeeInfoService.syncEmployeeRelationships()**

Trong `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoService.php`, sau dòng 536 (`$employeeRelationship->relation = ...`), thêm:

```php
$employeeRelationship->relation = $relationship['relation'];
$employeeRelationship->relation_other_text = ($relationship['relation'] == 11)
    ? ($relationship['relation_other_text'] ?? null)
    : null;
```

(Thay thế dòng 536 gốc bằng 3 dòng trên — dòng `relation` giữ nguyên, thêm 2 dòng `relation_other_text` ngay sau.)

- [x] **Step 2: Cập nhật EmployeeInfoUpdateRequestService.syncEmployeeRelationships()**

Trong `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoUpdateRequestService.php`, sau dòng 789 (`$employeeRelationship->relation = ...`), thêm:

```php
$employeeRelationship->relation = $relationship['relation'];
$employeeRelationship->relation_other_text = ($relationship['relation'] == 11)
    ? ($relationship['relation_other_text'] ?? null)
    : null;
```

- [x] **Step 3: Cập nhật EmployeeInfoUpdateRequestService.addEmployeeRelationships()**

Trong cùng file, sau dòng 818 (`$employeeRelationship->relation = ...`), thêm tương tự:

```php
$employeeRelationship->relation = $relationship['relation'];
$employeeRelationship->relation_other_text = ($relationship['relation'] == 11)
    ? ($relationship['relation_other_text'] ?? null)
    : null;
```

---

### Task 4: Validation — Thêm rule cho `relation_other_text`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Http/Requests/CreateEmployeeInfoRequest.php:64,218`

- [x] **Step 1: Thêm validation rule**

Trong `CreateEmployeeInfoRequest.php`, sau dòng 64 (`'relationships.*.relation' => 'required'`), thêm:

```php
'relationships.*.relation' => 'required',
'relationships.*.relation_other_text' => 'required_if:relationships.*.relation,11|max:255',
```

- [x] **Step 2: Thêm error message**

Sau dòng 218 (`'relationships.*.relation.required' => 'Bắt buộc phải nhập'`), thêm:

```php
'relationships.*.relation.required' => 'Bắt buộc phải nhập',
'relationships.*.relation_other_text.required_if' => 'Bắt buộc phải nhập khi chọn Khác',
'relationships.*.relation_other_text.max' => 'Không được vượt quá 255 ký tự',
```

**Lưu ý:** `SaveEmployeeInfoUpdateRequest.php` hiện đã comment out các rule `relationships.*` (dòng 76-79), nên KHÔNG cần thêm rule ở đây. Error messages đã có sẵn ở dòng 281-285 — chỉ cần thêm message cho `relation_other_text` nếu sau này uncomment rules.

---

### Task 5: Frontend — EmployeeInfoForm.vue (main — edit)

**Files:**
- Modify: `hrm-thanhan-client/components/human-components/employee_info/EmployeeInfoForm.vue:1131-1145,2279-2289`

- [x] **Step 1: Thêm 3 entry vào listRelations**

Tại dòng 2289 (sau `{ value: 8, text: 'Con gái' }`), thêm:

```javascript
listRelations: [
    { value: 0, text: 'Bố' },
    { value: 1, text: 'Mẹ' },
    { value: 2, text: 'Anh trai' },
    { value: 3, text: 'Chị gái' },
    { value: 4, text: 'Vợ/chồng' },
    { value: 5, text: 'Em trai' },
    { value: 6, text: 'Em gái' },
    { value: 7, text: 'Con trai' },
    { value: 8, text: 'Con gái' },
    { value: 9, text: 'Ông' },
    { value: 10, text: 'Bà' },
    { value: 11, text: 'Khác' },
],
```

- [x] **Step 2: Thêm ô text input sau dropdown mối quan hệ**

Tại dòng 1145 (sau `</td>` đóng của cột Mối quan hệ), thay thế toàn bộ `<td>` chứa dropdown bằng:

```html
<td>
    <b-form-select
        :options="listRelations"
        class="form-control"
        v-model="relationships[index].relation"
    />

    <b-form-input
        v-if="relationships[index].relation === 11"
        v-model="relationships[index].relation_other_text"
        placeholder="Nhập mối quan hệ"
        class="form-control mt-1"
    />

    <span
        v-if="!relationships[index].relation && relationships[index].relation !== 0"
        class="field-required"
        >{{
            formError['relationships.' + index + '.relation']
        }}</span
    >
</td>
```

**Lưu ý quan trọng:** Condition check `!relationships[index].relation` sẽ bị `true` khi value = 0 (Bố). Cần sửa thành `relationships[index].relation === null || relationships[index].relation === ''` hoặc thêm `&& relationships[index].relation !== 0`. Kiểm tra logic hiện tại — nếu đang hoạt động tốt thì giữ nguyên.

---

### Task 6: Frontend — EmployeeInfoForm.vue (my-info-request)

**Files:**
- Modify: `hrm-thanhan-client/components/human-components/employee_info/my-info-request/EmployeeInfoForm.vue:1661-1674,2700-2710`

- [x] **Step 1: Thêm 3 entry vào listRelations**

Tại dòng 2710 (sau `{ value: 8, text: 'Con gái' }`), thêm 3 entry giống Task 5 Step 1:

```javascript
{ value: 9, text: 'Ông' },
{ value: 10, text: 'Bà' },
{ value: 11, text: 'Khác' },
```

- [x] **Step 2: Thêm ô text input sau dropdown mối quan hệ**

Tại dòng 1674 (sau `</td>` đóng của cột Mối quan hệ). Thêm `b-form-input` ngay sau `b-form-select` và trước `<span>` error, bên trong cùng `<td>`:

```html
<b-form-select
    :options="listRelations"
    class="form-control"
    v-model="relationships[index].relation"
/>

<b-form-input
    v-if="relationships[index].relation === 11"
    v-model="relationships[index].relation_other_text"
    placeholder="Nhập mối quan hệ"
    class="form-control mt-1"
/>

<span
    v-if="!relationships[index].relation"
    class="field-required"
    >{{
        formError['relationships.' + index + '.relation']
    }}</span
>
```

---

### Task 7: Frontend — EmployeeInfoForm.vue (request-update)

**Files:**
- Modify: `hrm-thanhan-client/components/human-components/employee_info/request-update/EmployeeInfoForm.vue:1695-1708,2761-2771`

- [x] **Step 1: Thêm 3 entry vào listRelations**

Tại dòng 2771 (sau `{ value: 8, text: 'Con gái' }`), thêm 3 entry:

```javascript
{ value: 9, text: 'Ông' },
{ value: 10, text: 'Bà' },
{ value: 11, text: 'Khác' },
```

- [x] **Step 2: Thêm ô text input sau dropdown mối quan hệ**

Tại dòng 1708 (sau `</td>` đóng của cột Mối quan hệ). Thêm `b-form-input` ngay sau `b-form-select` và trước `<span>` error, bên trong cùng `<td>`:

```html
<b-form-select
    :options="listRelations"
    class="form-control"
    v-model="relationships[index].relation"
/>

<b-form-input
    v-if="relationships[index].relation === 11"
    v-model="relationships[index].relation_other_text"
    placeholder="Nhập mối quan hệ"
    class="form-control mt-1"
/>

<span
    v-if="!relationships[index].relation"
    class="field-required"
    >{{
        formError['relationships.' + index + '.relation']
    }}</span
>
```

---

### Task 8: Verify — Kiểm tra end-to-end

- [ ] **Step 1: Test màn edit employee** (`human/employee_info/:id/edit`)
  - Mở form edit → kéo xuống Thông tin gia đình
  - Dropdown mối quan hệ phải hiện thêm: Ông, Bà, Khác
  - Chọn "Ông" → save → load lại → dropdown vẫn hiện "Ông"
  - Chọn "Bà" → save → load lại → dropdown vẫn hiện "Bà"

- [ ] **Step 2: Test "Khác" + text tự do**
  - Chọn "Khác" → ô text input hiện ra
  - Nhập "Cậu ruột" → save → load lại → dropdown = "Khác", ô text = "Cậu ruột"
  - Chọn "Khác" nhưng KHÔNG nhập text → save → BE validation chặn

- [ ] **Step 3: Test chuyển đổi giá trị**
  - Chọn "Khác" + nhập "Cậu ruột" → save
  - Edit lại → đổi sang "Bố" → save → load lại → dropdown = "Bố", `relation_other_text` = null trong DB

- [ ] **Step 4: Test flow update request** (`human/employee_info/:id/update_request`)
  - Tạo yêu cầu cập nhật với quan hệ "Khác" + text
  - Verify dữ liệu lưu vào bảng `employee_relationship_tmps`

- [ ] **Step 5: Test flow my-info-request** (`human/employee_info/my-info-request/:id`)
  - NV tự cập nhật với quan hệ "Ông" hoặc "Khác"
  - Verify hiển thị đúng

- [ ] **Step 6: Test backward compatibility**
  - Mở NV có dữ liệu gia đình cũ (relation = 0-8) → hiển thị bình thường, không lỗi
