# Nhà cung cấp (Supplier) + Nhóm NCC — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để thực thi task-by-task. Steps dùng checkbox (`- [ ]`).

**Goal:** Tạo 2 danh mục mới trong module Category — Nhóm nhà cung cấp (`supplier_groups`) và Nhà cung cấp (`suppliers` + bảng con `supplier_contacts`) — theo pattern Manufacturer.

**Architecture:** 3 bảng mới. Nhóm NCC copy 1:1 pattern Manufacturer. NCC giống Manufacturer nhưng nhiều trường (MST, nhóm, địa chỉ Tỉnh/Phường, liên hệ nhiều) + cấm xóa (chỉ khóa). FE: 2 menu, 2 list page, modal NCC có địa chỉ cascading + bảng liên hệ động.

**Tech Stack:** Laravel 8 (PHP 8.1), Nuxt 2 (Vue 2), Bootstrap-Vue, spatie/permission, maatwebsite/excel.

**Spec:** `docs/superpowers/specs/2026-06-05-supplier-category-design.md`

**Lưu ý môi trường:**
- KHÔNG có test tự động → verify bằng `php artisan migrate`, `php -l`, `tinker`, kiểm tra UI.
- Repo API: `nhatlinh-api/` (chạy artisan tại đây). FE: `nhatlinh-client/`.
- **KHÔNG commit/push git.** KHÔNG đọc vendor/, node_modules/.
- **File template để copy** (đọc khi implement): Manufacturer ở `Modules/Category/{Entities/Manufacturer.php, Http/Controllers/Api/V1/ManufacturerController.php, Http/Requests/ManufacturerRequest.php, Services/ManufacturerService.php, Transformers/ManufacturerResource/*, Routes/api.php}`, `app/ExcelExport/ManufacturerExport.php`, `resources/views/exports/manufacturers.blade.php`, FE `pages/category/manufacturers/{index.vue, AddManufacturerModal.vue}`.

**File Structure:**
| File | Trách nhiệm |
|------|-------------|
| `Database/Migrations/2026_06_05_000001_create_supplier_groups_table.php` | Bảng nhóm NCC |
| `Database/Migrations/2026_06_05_000002_create_suppliers_table.php` | Bảng NCC |
| `Database/Migrations/2026_06_05_000003_create_supplier_contacts_table.php` | Bảng liên hệ NCC |
| `Entities/{SupplierGroup,Supplier,SupplierContact}.php` | Models |
| `Http/Requests/{SupplierGroupRequest,SupplierRequest}.php` | Validate |
| `Services/{SupplierGroupService,SupplierService}.php` | Business logic |
| `Transformers/SupplierGroupResource/*`, `Transformers/SupplierResource/*` | API output |
| `Http/Controllers/Api/V1/{SupplierGroupController,SupplierController}.php` | Endpoints |
| `app/ExcelExport/{SupplierGroupExport,SupplierExport}.php` + views | Export |
| `Routes/api.php` | Routes (sửa) |
| `PermissionsTableSeeder.php` | 4 permission (sửa) |
| FE `pages/category/supplier-groups/{index,AddSupplierGroupModal}.vue` | Màn nhóm NCC |
| FE `pages/category/suppliers/{index,AddSupplierModal}.vue` | Màn NCC |
| FE `components/default-menu/category.js` | Menu (sửa) |

---

## Phase 1: Backend — Nhóm nhà cung cấp (supplier_groups)

### Task 1: Migration `supplier_groups`

**Files:** Create `nhatlinh-api/Modules/Category/Database/Migrations/2026_06_05_000001_create_supplier_groups_table.php`

- [ ] **Step 1:** Tạo migration:
```php
<?php
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateSupplierGroupsTable extends Migration
{
    public function up()
    {
        Schema::create('supplier_groups', function (Blueprint $table) {
            $table->id();
            $table->string('code', 50)->unique();
            $table->string('name', 255);
            $table->text('description')->nullable();
            $table->integer('status')->default(1);
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->timestamps();
        });
    }
    public function down() { Schema::dropIfExists('supplier_groups'); }
}
```
- [ ] **Step 2:** Run `php artisan migrate`. Expected: Migrated.
- [ ] **Step 3:** Verify `php artisan tinker --execute="echo Schema::hasTable('supplier_groups')?'OK':'NO';"` → OK.

### Task 2: Entity `SupplierGroup`

**Files:** Create `Modules/Category/Entities/SupplierGroup.php`

- [ ] **Step 1:** Đọc `Modules/Category/Entities/Manufacturer.php` làm mẫu. Tạo `SupplierGroup` giống hệt, đổi: `$table = 'supplier_groups'`; quan hệ `products()` → `suppliers()`:
```php
    public function suppliers()
    {
        return $this->hasMany(Supplier::class, 'supplier_group_id');
    }
    public function isCanDelete()
    {
        return $this->suppliers()->count() === 0;
    }
```
Giữ nguyên constants, `$fillable` (code, name, description, created_by, updated_by, created_at, updated_at, company_id, department_id, part_id, status), accessor tên người tạo/cập nhật, isCanEdit/isCodeEditable/isCanLockUpdate/isCanUnlockUpdate.
- [ ] **Step 2:** Verify `php -l Modules/Category/Entities/SupplierGroup.php`.

### Task 3: Request `SupplierGroupRequest`

**Files:** Create `Modules/Category/Http/Requests/SupplierGroupRequest.php`

- [ ] **Step 1:** Copy `ManufacturerRequest.php`, đổi class name → `SupplierGroupRequest`, đổi bảng unique `manufacturers` → `supplier_groups` ở cả `name` và `code`. Giữ regex + prepareForValidation + messages.
- [ ] **Step 2:** Verify `php -l`.

### Task 4: Service `SupplierGroupService`

**Files:** Create `Modules/Category/Services/SupplierGroupService.php`

- [ ] **Step 1:** Copy `ManufacturerService.php`. Thay:
  - `use Modules\Category\Entities\Manufacturer;` → `use Modules\Category\Entities\SupplierGroup;`
  - Mọi `Manufacturer::` → `SupplierGroup::`, mọi `manufacturers.` (cột bảng trong query) → `supplier_groups.`
  - Regex import `^HSX\.` → `^NNCC\.`, message "HSX.xxxx" → "NNCC.xxxx".
  - Tên method import (nếu là `importManufacturers`) → `importItems` (hoặc giữ tên, miễn controller gọi đúng).
- [ ] **Step 2:** Verify `php -l`.

### Task 5: Transformers SupplierGroup

**Files:** Create `Modules/Category/Transformers/SupplierGroupResource/SupplierGroupResource.php` + `DetailSupplierGroupResource.php`

- [ ] **Step 1:** Copy 2 file từ `ManufacturerResource/`, đổi namespace `SupplierGroupResource`, class name tương ứng. Giữ nguyên các field trả về (id, name, code, status, description, created_at, updated_by_name, created_by_name, updated_at, is_can_edit, is_can_lock_update, is_can_unlock_update).
- [ ] **Step 2:** Verify `php -l` cả 2.

### Task 6: Controller + Routes SupplierGroup

**Files:** Create `Modules/Category/Http/Controllers/Api/V1/SupplierGroupController.php`; Modify `Modules/Category/Routes/api.php`

- [ ] **Step 1:** Copy `ManufacturerController.php`, đổi:
  - class → `SupplierGroupController`; `use` Service/Resource/Request/Entity sang Supplier-group tương ứng; biến `$manufacturerService` → `$supplierGroupService`.
  - Route-model-binding param `Manufacturer $manufacturer` → `SupplierGroup $supplierGroup`.
  - Export filename `'danh_sach_hang_san_xuat.xls'` → `'danh_sach_nhom_nha_cung_cap.xls'` (xem Task 7).
  - Các message "hãng sản xuất" → "nhóm nhà cung cấp".
- [ ] **Step 2:** Trong `Routes/api.php`, thêm `use Modules\Category\Http\Controllers\Api\V1\SupplierGroupController;` (đầu file) và thêm group `/supplier-groups` (copy block `/manufacturers`, đổi controller + param + permission strings sang "...nhóm nhà cung cấp"). Xem spec mục 4.7.
- [ ] **Step 3:** Verify `php -l` controller + routes.

### Task 7: Export SupplierGroup

**Files:** Create `app/ExcelExport/SupplierGroupExport.php`; Create `resources/views/exports/supplier_groups.blade.php`

- [ ] **Step 1:** Copy `ManufacturerExport.php` → `SupplierGroupExport`, đổi view name → `exports.supplier_groups`.
- [ ] **Step 2:** Copy `manufacturers.blade.php` → `supplier_groups.blade.php`, đổi tiêu đề/header "hãng sản xuất" → "nhóm nhà cung cấp".
- [ ] **Step 3:** Verify `php -l SupplierGroupExport.php`.

---

## Phase 2: Backend — Nhà cung cấp (suppliers + supplier_contacts)

### Task 8: Migrations suppliers + supplier_contacts

**Files:** Create `2026_06_05_000002_create_suppliers_table.php`, `2026_06_05_000003_create_supplier_contacts_table.php`

- [ ] **Step 1:** suppliers (xem spec 3.2 — đầy đủ cột: code unique, name, tax_code, supplier_group_id index, province_id, ward_id, address(500), phone(30), email(100), note text, status, audit, tổ chức).
- [ ] **Step 2:** supplier_contacts (xem spec 3.3 — supplier_id index, fullname, role, phone, email, timestamps).
- [ ] **Step 3:** Run `php artisan migrate`. Verify cả 2 bảng tồn tại qua tinker `Schema::hasTable`.

### Task 9: Entities Supplier + SupplierContact

**Files:** Create `Modules/Category/Entities/Supplier.php`, `SupplierContact.php`

- [ ] **Step 1:** `Supplier.php` (theo Manufacturer + spec 4.1):
  - `$table='suppliers'`, `$fillable` đầy đủ (code, name, tax_code, supplier_group_id, province_id, ward_id, address, phone, email, note, status, created_by, updated_by, company_id, department_id, part_id).
  - Constants STATUS_ACTIVE=1, STATUS_INACTIVE=2.
  - `group()` belongsTo(SupplierGroup, 'supplier_group_id'); `contacts()` hasMany(SupplierContact, 'supplier_id').
  - accessor tên người tạo/cập nhật (copy Manufacturer).
  - `isCanEdit()` = status==ACTIVE; `isCanLockUpdate()`/`isCanUnlockUpdate()` = true; `isCodeEditable()` = true.
  - `isCanDelete()`: `return false;`
- [ ] **Step 2:** `SupplierContact.php`: `$table='supplier_contacts'`, `$fillable=['supplier_id','fullname','role','phone','email']`, `supplier()` belongsTo(Supplier).
- [ ] **Step 3:** Verify `php -l` cả 2.

### Task 10: Request `SupplierRequest`

**Files:** Create `Modules/Category/Http/Requests/SupplierRequest.php`

- [ ] **Step 1:** Tạo theo spec 4.2:
```php
<?php
namespace Modules\Category\Http\Requests;
use Modules\Training\Http\Requests\BaseRequest;

class SupplierRequest extends BaseRequest
{
    protected function prepareForValidation()
    {
        if ($this->has('code') && !empty($this->code)) {
            $this->merge(['code' => formatCodeTrimAfterDot($this->code)]);
        }
    }
    public function rules()
    {
        return [
            'name' => 'required|max:255|unique:suppliers,name,' . $this->id,
            'code' => [
                'required', 'max:50', 'regex:/^[A-Z]+\.[a-zA-Z0-9_]+$/',
                function ($attribute, $value, $fail) {
                    if (preg_match('/^[A-Z]+\.$/', $value)) { $fail('Bắt buộc phải nhập'); }
                },
                'unique:suppliers,code,' . $this->id,
            ],
            'tax_code' => 'nullable|max:50',
            'supplier_group_id' => 'nullable|exists:supplier_groups,id',
            'province_id' => 'nullable|integer',
            'ward_id' => 'nullable|integer',
            'address' => 'nullable|max:500',
            'phone' => 'nullable|max:30',
            'email' => 'nullable|email|max:100',
            'note' => 'nullable',
            'contacts' => 'nullable|array',
            'contacts.*.fullname' => 'required_with:contacts|max:255',
            'contacts.*.role' => 'nullable|max:100',
            'contacts.*.phone' => 'nullable|max:30',
            'contacts.*.email' => 'nullable|email|max:100',
        ];
    }
    public function messages()
    {
        return [
            'code.regex' => 'Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu gạch dưới (_).',
            'email.email' => 'Email không đúng định dạng',
            'contacts.*.fullname.required_with' => 'Tên người liên hệ là bắt buộc',
            'contacts.*.email.email' => 'Email liên hệ không đúng định dạng',
        ];
    }
}
```
- [ ] **Step 2:** Verify `php -l`.

### Task 11: Service `SupplierService` (sync contacts + import)

**Files:** Create `Modules/Category/Services/SupplierService.php`

- [ ] **Step 1:** Copy `ManufacturerService.php` làm khung, đổi model `Supplier`, bảng `suppliers`. Thêm `use Modules\Category\Entities\SupplierContact;`.
- [ ] **Step 2:** `index()`: thêm eager-load `->with('group')`; thêm filter:
```php
        if (isset($request->supplier_group_id)) $query->where('suppliers.supplier_group_id', $request->supplier_group_id);
```
keyword search mở rộng: name|code|tax_code|phone.
- [ ] **Step 3:** `updateOrCreate()` và `update()`: sau khi lưu supplier, gọi `$this->syncContacts($supplier, $request->contacts ?? []);`. Thêm method:
```php
    public function syncContacts(Supplier $supplier, array $contacts): void
    {
        $keepIds = collect($contacts)->pluck('id')->filter()->all();
        $supplier->contacts()->whereNotIn('id', $keepIds ?: [0])->delete();
        foreach ($contacts as $c) {
            if (empty($c['fullname'])) continue;
            $payload = [
                'fullname' => $c['fullname'],
                'role' => $c['role'] ?? null,
                'phone' => $c['phone'] ?? null,
                'email' => $c['email'] ?? null,
            ];
            if (!empty($c['id'])) {
                SupplierContact::where('id', $c['id'])->where('supplier_id', $supplier->id)->update($payload);
            } else {
                $supplier->contacts()->create($payload);
            }
        }
    }
```
- [ ] **Step 4:** Bỏ `destroy()` (supplier cấm xóa) hoặc giữ nhưng không dùng. KHÔNG có route delete.
- [ ] **Step 5:** `validateImportData()`/`importItems()`: regex `^NCC\.`; resolve `supplier_group_id` từ cột `group_code` (tra `SupplierGroup` theo code, optional); KHÔNG xử lý contacts; địa chỉ vào cột `address`. Các cột import: code, name, tax_code, group_code, address, phone, email, status.
- [ ] **Step 6:** Verify `php -l`.

### Task 12: Transformers Supplier

**Files:** Create `Modules/Category/Transformers/SupplierResource/SupplierResource.php` + `DetailSupplierResource.php`

- [ ] **Step 1:** `SupplierResource` (list) trả: id, code, name, tax_code, supplier_group_id, group_name (`optional($this->group)->name`), phone, email, address, province_id, ward_id, status, created_by_name, updated_by_name, created_at, updated_at, is_can_edit, is_can_lock_update, is_can_unlock_update, is_can_delete (`$this->isCanDelete()`).
- [ ] **Step 2:** `DetailSupplierResource` (show): tất cả trường trên + `note` + `contacts` (`$this->contacts->map(fn($c)=>['id'=>$c->id,'fullname'=>$c->fullname,'role'=>$c->role,'phone'=>$c->phone,'email'=>$c->email])`).
- [ ] **Step 3:** Verify `php -l` cả 2.

### Task 13: Controller + Routes Supplier (không delete)

**Files:** Create `Modules/Category/Http/Controllers/Api/V1/SupplierController.php`; Modify `Routes/api.php`

- [ ] **Step 1:** Copy `ManufacturerController`, đổi sang Supplier. Khác biệt:
  - **Bỏ hẳn action `delete`** (supplier cấm xóa).
  - `show()`: `$supplier->load('group','contacts');` trước khi trả `DetailSupplierResource`.
  - `updateOrCreate()`/`update()`: giữ wrap `DB::transaction`. KHÔNG catch chung `Exception` quanh validation — để `SupplierRequest` tự ném `ValidationException` (FormRequest tự trả 422). Nếu copy code có try/catch Exception, đảm bảo không nuốt ValidationException (FormRequest validate chạy trước khi vào controller nên an toàn).
- [ ] **Step 2:** `Routes/api.php`: thêm `use ...SupplierController;` + group `/suppliers` (xem spec 4.7) — **KHÔNG có route delete**.
- [ ] **Step 3:** Verify `php -l` controller + routes.

### Task 14: Export Supplier

**Files:** Create `app/ExcelExport/SupplierExport.php`; Create `resources/views/exports/suppliers.blade.php`

- [ ] **Step 1:** `SupplierExport` copy pattern, view `exports.suppliers`.
- [ ] **Step 2:** `suppliers.blade.php`: cột STT, Mã, Tên, MST, Nhóm NCC (`$item['group_name'] ?? ''`), Địa chỉ (`$item['address'] ?? ''`), SĐT, Email, Trạng thái, Người tạo, Người cập nhật.
- [ ] **Step 3:** Controller export filename `'danh_sach_nha_cung_cap.xls'`.
- [ ] **Step 4:** Verify `php -l`.

---

## Phase 3: Backend — Permissions

### Task 15: 4 permission mới

**Files:** Modify `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [ ] **Step 1:** Tìm id permission lớn nhất hiện có trong seeder (grep `'id' =>` các dòng Permission::create gần khối "Danh mục chung"). Chọn 4 id trống kế tiếp (vd nếu max là 1095 thì dùng 1096-1099).
- [ ] **Step 2:** Thêm khối (đặt cạnh các permission "Danh mục chung", thay `<idN>` bằng id trống thực tế):
```php
        // Danh mục nhà cung cấp
        Permission::create(['id' => <id1>, 'guard_name' => 'api', 'name' => 'Quản lý danh mục nhà cung cấp', 'display_name' => 'Quản lý danh mục nhà cung cấp', 'group' => 'Danh mục chung', 'type' => 8]);
        Permission::create(['id' => <id2>, 'guard_name' => 'api', 'name' => 'Xem danh mục nhà cung cấp', 'display_name' => 'Xem danh mục nhà cung cấp', 'group' => 'Danh mục chung', 'type' => 8]);
        // Danh mục nhóm nhà cung cấp
        Permission::create(['id' => <id3>, 'guard_name' => 'api', 'name' => 'Quản lý danh mục nhóm nhà cung cấp', 'display_name' => 'Quản lý danh mục nhóm nhà cung cấp', 'group' => 'Danh mục chung', 'type' => 8]);
        Permission::create(['id' => <id4>, 'guard_name' => 'api', 'name' => 'Xem danh mục nhóm nhà cung cấp', 'display_name' => 'Xem danh mục nhóm nhà cung cấp', 'group' => 'Danh mục chung', 'type' => 8]);
```
- [ ] **Step 3:** Insert vào DB dev (KHÔNG re-seed toàn bộ) + gán cho role Admin. Chạy tinker (thay id + tên role admin thực tế — kiểm tra bảng roles trước):
```bash
php artisan tinker --execute="
use App\Models\Permission; use App\Models\Role;
\$names=['Quản lý danh mục nhà cung cấp','Xem danh mục nhà cung cấp','Quản lý danh mục nhóm nhà cung cấp','Xem danh mục nhóm nhà cung cấp'];
\$ids=[<id1>,<id2>,<id3>,<id4>];
foreach(\$names as \$i=>\$n){ Permission::firstOrCreate(['name'=>\$n,'guard_name'=>'api'],['id'=>\$ids[\$i],'display_name'=>\$n,'group'=>'Danh mục chung','type'=>8]); }
\$admin=Role::where('name','Super Admin')->orWhere('name','Admin')->first();
if(\$admin){ \$admin->givePermissionTo(\$names); }
app()->make(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions();
echo 'perm done; admin='.(\$admin?\$admin->name:'NONE');
"
```
- [ ] **Step 4:** Verify `php artisan tinker --execute="echo App\Models\Permission::whereIn('name',['Quản lý danh mục nhà cung cấp'])->count();"` → 1.

---

## Phase 4: Frontend — Nhóm NCC + Menu

### Task 16: Menu + màn Nhóm NCC

**Files:** Modify `components/default-menu/category.js`; Create `pages/category/supplier-groups/index.vue` + `AddSupplierGroupModal.vue`

- [ ] **Step 1:** `category.js`: thêm 2 item:
```js
    { label: 'Nhà cung cấp', link: '/category/suppliers' },
    { label: 'Nhóm nhà cung cấp', link: '/category/supplier-groups' },
```
- [ ] **Step 2:** Copy `pages/category/manufacturers/index.vue` → `pages/category/supplier-groups/index.vue`. Thay: mọi "hãng sản xuất" → "nhóm nhà cung cấp", endpoint `category/manufacturers` → `category/supplier-groups`, import modal component → `AddSupplierGroupModal`, `localStorageKey`/`pathsToKeep` → supplier-groups, prefix import `HSX`→`NNCC`, template-file-name tương ứng.
- [ ] **Step 3:** Copy `AddManufacturerModal.vue` → `AddSupplierGroupModal.vue`. Thay tên/label "hãng sản xuất" → "nhóm nhà cung cấp", prefix `HSX.` → `NNCC.`, endpoint `category/supplier-groups`.
- [ ] **Step 4:** Verify: mở `/category/supplier-groups`, CRUD thử 1 nhóm.

---

## Phase 5: Frontend — Nhà cung cấp

### Task 17: `pages/category/suppliers/index.vue`

**Files:** Create `pages/category/suppliers/index.vue`

- [ ] **Step 1:** Copy `manufacturers/index.vue`. Thay endpoint → `category/suppliers`, label → "nhà cung cấp", localStorageKey/pathsToKeep → suppliers, modal → `AddSupplierModal`, prefix import `HSX`→`NCC`.
- [ ] **Step 2:** Thêm filter "Nhóm NCC" trong advanced-filters (V2BaseSelect, options từ `supplierGroupOptions`). Thêm vào `data()`/`mounted()`:
```js
        // data
        supplierGroupOptions: [],
        // mounted: tải nhóm NCC cho filter
        this.loadSupplierGroups()
        // methods
        async loadSupplierGroups() {
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', 'category/supplier-groups/getAll')
                this.supplierGroupOptions = (data || []).map((g) => ({ id: g.id, name: g.code + ' - ' + g.name }))
            } catch (e) { this.supplierGroupOptions = [] }
        },
```
Thêm `supplier_group_id` vào `initialStateForm` + `apiFilters` trong loadData.
- [ ] **Step 3:** Cột bảng: hiển thị mã+tên (itemInfo), MST, Nhóm NCC (`item.group_name`), SĐT/email, trạng thái. **Row actions: chỉ Xem + Sửa + Khóa/Mở khóa — BỎ nút Xóa** (xóa block `confirmDeleteItem`/icon delete và modal confirm-delete). Bỏ `deleteConfirmMessage`/`itemToDelete`/`handleConfirmDelete` nếu không dùng.
- [ ] **Step 4:** Verify: mở `/category/suppliers`, danh sách hiển thị, không có nút Xóa.

### Task 18: `pages/category/suppliers/AddSupplierModal.vue` (địa chỉ cascading + liên hệ động)

**Files:** Create `pages/category/suppliers/AddSupplierModal.vue`

- [ ] **Step 1:** Copy `AddManufacturerModal.vue` làm khung (`size="xl"`). Cấu trúc `data.data`:
```js
            data: {
                code: '', name: '', tax_code: '', supplier_group_id: null,
                province_id: null, ward_id: null, address: '',
                phone: '', email: '', note: '', status: 1,
                contacts: [],
            },
            provinceOptions: [], wardOptions: [], supplierGroupOptions: [],
```
- [ ] **Step 2:** Template các hàng (theo spec 5.3): Hàng 1 Mã(prefix `NCC.`)/Tên/Trạng thái; Hàng 2 MST/Nhóm NCC(V2BaseSelect supplierGroupOptions)/SĐT/Email; Hàng 3 địa chỉ: Tỉnh(V2BaseSelect provinceOptions @change=onProvinceChange)/Phường-Xã(V2BaseSelect wardOptions)/ô text Số nhà-đường (`address`); Hàng 4 Ghi chú(textarea). Validate inline cho Mã/Tên.
- [ ] **Step 3:** Bảng liên hệ động — thêm dưới Ghi chú:
```html
<div class="form-row"><div class="col-12">
  <div class="d-flex justify-content-between align-items-center mb-2">
    <V2BaseLabel>Người liên hệ</V2BaseLabel>
    <V2BaseButton v-if="!isShow" size="sm" secondary @click="addContact">
      <template #prefix><i class="ri-add-line"></i></template> Thêm liên hệ
    </V2BaseButton>
  </div>
  <table class="table table-sm">
    <thead><tr><th>Tên<span class="text-danger">*</span></th><th>Chức vụ</th><th>SĐT</th><th>Email</th><th></th></tr></thead>
    <tbody>
      <tr v-for="(c, i) in data.contacts" :key="i">
        <td><V2BaseInput v-model="c.fullname" size="sm" :disabled="isShow" :class="{ 'is-invalid': touched && !c.fullname }" /></td>
        <td><V2BaseInput v-model="c.role" size="sm" :disabled="isShow" /></td>
        <td><V2BaseInput v-model="c.phone" size="sm" :disabled="isShow" /></td>
        <td><V2BaseInput v-model="c.email" size="sm" :disabled="isShow" /></td>
        <td><V2BaseIconButton v-if="!isShow" danger @click="removeContact(i)"><i class="ri-delete-bin-6-line"></i></V2BaseIconButton></td>
      </tr>
      <tr v-if="!data.contacts.length"><td colspan="5" class="text-center text-muted">Chưa có liên hệ</td></tr>
    </tbody>
  </table>
</div></div>
```
- [ ] **Step 4:** Methods:
```js
        addContact() { this.data.contacts.push({ fullname: '', role: '', phone: '', email: '' }) },
        removeContact(i) { this.data.contacts.splice(i, 1) },
        async loadProvinces() {
            const res = await this.$store.dispatch('apiGet', 'addresses?level=1')
            if (res.data && res.data.code == 200) this.provinceOptions = res.data.data.map((p) => ({ id: p.id, name: p.name }))
        },
        async loadWards(provinceId) {
            this.wardOptions = []
            if (!provinceId) return
            const res = await this.$store.dispatch('apiGet', `addresses?level=3&parent_id=${provinceId}`)
            if (res.data && res.data.code == 200) this.wardOptions = res.data.data.map((w) => ({ id: w.id, name: w.name }))
        },
        onProvinceChange(val) { this.data.province_id = val; this.data.ward_id = null; this.loadWards(val) },
        async loadSupplierGroups() {
            const { data } = await this.$store.dispatch('apiGetMethod', 'category/supplier-groups/getAll')
            this.supplierGroupOptions = (data || []).map((g) => ({ id: g.id, name: g.code + ' - ' + g.name }))
        },
```
Gọi `loadProvinces()` + `loadSupplierGroups()` trong `mounted()`.
- [ ] **Step 5:** `loadData()` (edit): fill data + `this.data.contacts = data.contacts || []`; nếu có `province_id` → `await this.loadWards(data.province_id)` để có label Phường/Xã.
- [ ] **Step 6:** `submitForm()` payload: gửi toàn bộ field + `contacts: this.data.contacts`. Endpoint `category/suppliers`. Validate inline: set `touched=true` khi submit; chặn nếu thiếu Mã/Tên hoặc dòng liên hệ thiếu tên.
- [ ] **Step 7:** Verify UI: tạo NCC có 2 liên hệ + chọn Tỉnh→Phường → lưu → mở lại thấy đủ; đổi Tỉnh reset Phường.

---

## Phase 6: Kiểm thử

### Task 19: Test end-to-end (manual)

- [ ] **Step 1:** Nhóm NCC: tạo "NNCC.0001 - NVL", sửa, khóa/mở khóa, export, import file mẫu.
- [ ] **Step 2:** NCC: tạo "NCC.0001" gắn nhóm NVL + 2 liên hệ + địa chỉ Tỉnh/Phường → lưu → mở lại đủ dữ liệu. Sửa: xóa 1 liên hệ + thêm 1 liên hệ → lưu → đúng (sync). Đổi Tỉnh → Phường reset.
- [ ] **Step 3:** Cấm xóa: nhóm NCC còn NCC → xóa bị chặn. NCC không có nút Xóa, chỉ Khóa.
- [ ] **Step 4:** Import NCC: file có group_code hợp lệ + 1 dòng group_code sai → dòng sai báo lỗi.
- [ ] **Step 5:** Phân quyền: tài khoản chỉ "Xem danh mục nhà cung cấp" → xem được, không tạo/sửa.
- [ ] **Step 6 (wrap up):** đánh dấu [x], ghi Checkpoint plan.md, cập nhật STATUS.md.

---

## Checkpoint — 2026-06-05

**Trạng thái: CODE HOÀN THÀNH (chạy trên `main`, chưa commit).**

Thực thi qua subagent-driven (mỗi nhóm: implementer + spec review + code-quality review + fix):
- **Nhóm A — BE Nhóm NCC (Task 1-7):** ✅ supplier_groups (migration, entity, request, service, transformer, controller, routes, export) — copy pattern Manufacturer. Fix: thêm updated_by.
- **Nhóm B — BE NCC (Task 8-14):** ✅ suppliers + supplier_contacts (migrations, entities, request có contacts, service + syncContacts, transformer kèm contacts, controller KHÔNG delete, routes, export). Fix: try/catch+Log controller, eager-load update(), gộp query import.
- **Nhóm C — Permissions (Task 15):** ✅ 4 quyền (id 1097-1100) + seeder + DB + gán role Super admin (id 18). Tên quyền khớp tuyệt đối route↔seeder↔DB.
- **Nhóm D — FE Menu + Nhóm NCC (Task 16):** ✅ menu 2 item, supplier-groups list+modal (copy manufacturers). Review sạch.
- **Nhóm E — FE NCC (Task 17-18):** ✅ suppliers list (lọc nhóm NCC, KHÔNG nút xóa) + modal xl (địa chỉ Tỉnh→Phường cascading + bảng liên hệ động). Fix: formError={}, ward_id set sau loadWards.

**Đã verify chức năng BE thực tế (tinker):**
- syncContacts upsert/delete đúng (thêm 2 → giữ 1 + thêm 1 → đúng 2 tên).
- isCanDelete: nhóm NCC còn NCC → false, hết NCC → true; supplier → false (cấm xóa).
- group relation, cleanup ✅.

**Còn lại (user verify trên app đang chạy — Task 19):**
- Test UI: tạo nhóm NCC; tạo NCC gắn nhóm + 2 liên hệ + địa chỉ Tỉnh/Phường → lưu → mở lại đủ; sửa (xóa/thêm liên hệ → sync); đổi Tỉnh reset Phường; NCC không có nút Xóa; import; phân quyền.
- File mẫu import `Mau_import_NhaCungCap.xlsx` + `Mau_import_NhomNhaCungCap.xlsx` trong `nhatlinh-client/static/` — mới đổi tên tham chiếu, chưa tạo file vật lý.

**Bước tiếp theo:** user test UI + tự commit. Feature kế tiếp Module 1: #3 `unit-conversion` (DM-08) hoặc #4 `customer-category` (DM-05).

---

## Self-review (đã rà)

- **Spec coverage:** supplier_groups (T1-7) ✓; suppliers+contacts (T8-14) ✓; permission (T15) ✓; FE menu+nhóm (T16) ✓; FE NCC list không-xóa (T17) ✓; modal địa chỉ cascading + liên hệ động (T18) ✓; test (T19) ✓. Cấm xóa NCC (T9 isCanDelete=false + T13 bỏ route + T17 bỏ nút) ✓. Sync contacts (T11) ✓. Import resolve group (T11) ✓.
- **Placeholder scan:** id permission để `<idN>` — CỐ Ý (phải tra id trống thực tế ở T15 step 1, có hướng dẫn). Các phần copy chỉ rõ file mẫu + token thay thế.
- **Type consistency:** field `supplier_group_id`, `contacts[]` (fullname/role/phone/email), `group_name`, `province_id`/`ward_id`/`address` nhất quán giữa migration/entity/request/service/transformer/FE.
