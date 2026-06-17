# Nhóm hàng hoá — Đổi tên + Phân cấp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đổi tên "Loại hàng hoá" → "Nhóm hàng hoá" + thêm phân cấp cha-con (tree-table) cho module Category.

**Architecture:** Thêm `parent_id` (nullable) vào `product_types`. BE theo pattern controller/service hiện có; index hỗ trợ `tree=1` trả toàn bộ list phẳng kèm `parent_id`. FE dựng cây ở client, hiển thị thụt lề + expand/collapse qua slot của `V2BaseDataTable` (KHÔNG sửa component chung); modal thêm field "Nhóm cha".

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, spatie/laravel-permission.

**Spec:** `docs/superpowers/specs/2026-06-04-product-type-hierarchy-design.md`

**Lưu ý môi trường:**
- Dự án **không có test tự động** (PHPUnit/Jest chưa cấu hình) → mỗi task verify bằng `php artisan` / `tinker` / kiểm tra UI, theo đúng style các plan trước (product-catalog).
- Repo API: `nhatlinh-api/` (lệnh artisan chạy tại thư mục này). Repo FE: `nhatlinh-client/`.
- KHÔNG commit/push (theo CLAUDE.md).

**File Structure:**
| File | Trách nhiệm | Tạo/Sửa |
|------|-------------|---------|
| `Modules/Category/Database/Migrations/2026_06_04_000001_add_parent_id_to_product_types.php` | Thêm cột parent_id | Tạo |
| `Modules/Category/Entities/ProductType.php` | parent/children/getDescendantIds/isCanDelete | Sửa |
| `Modules/Category/Http/Requests/ProductTypeRequest.php` | Validate parent_id + chống chu trình | Sửa |
| `Modules/Category/Services/ProductTypeService.php` | Lưu parent_id, index tree=1, import parent_code, prefix NHH | Sửa |
| `Modules/Category/Transformers/ProductTypeResource/*` | Trả parent_id + parent_name | Sửa |
| `Modules/Category/Http/Controllers/Api/V1/ProductTypeController.php` | Export filename | Sửa |
| `Modules/Category/Routes/api.php` | Middleware permission đổi tên | Sửa |
| `resources/views/exports/product_types.blade.php` | Cột "Mã nhóm cha" | Sửa |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | Đổi tên 2 permission | Sửa |
| `components/default-menu/category.js` | Label menu | Sửa |
| `pages/category/product-types/index.vue` | Đổi tên label + tree-table | Sửa |
| `pages/category/product-types/AddProductTypeModal.vue` | Field Nhóm cha + prefix NHH | Sửa |
| `pages/category/product-types/treeUtils.js` | Helper dựng cây (mới) | Tạo |

---

## Phase 1: Backend — DB, Entity, Request, Service (phân cấp)

### Task 1: Migration thêm `parent_id`

**Files:**
- Create: `nhatlinh-api/Modules/Category/Database/Migrations/2026_06_04_000001_add_parent_id_to_product_types.php`

- [ ] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddParentIdToProductTypes extends Migration
{
    public function up()
    {
        Schema::table('product_types', function (Blueprint $table) {
            $table->unsignedBigInteger('parent_id')->nullable()->after('id')->index();
        });
    }

    public function down()
    {
        Schema::table('product_types', function (Blueprint $table) {
            $table->dropColumn('parent_id');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

Run (tại `nhatlinh-api/`): `php artisan migrate`
Expected: `Migrated: ..._add_parent_id_to_product_types`

- [ ] **Step 3: Verify cột tồn tại**

Run: `php artisan tinker --execute="echo Schema::hasColumn('product_types','parent_id') ? 'OK' : 'MISSING';"`
Expected: `OK`

---

### Task 2: Entity `ProductType` — quan hệ + getDescendantIds + isCanDelete

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Entities/ProductType.php`

- [ ] **Step 1: Thêm `parent_id` vào `$fillable`**

Sửa mảng `$fillable` thêm `'parent_id'`:

```php
    protected $fillable = [
        'name', 'code', 'description', 'parent_id', 'created_by', 'updated_by',
        'created_at', 'updated_at', 'company_id', 'department_id', 'part_id', 'status',
    ];
```

- [ ] **Step 2: Thêm quan hệ parent/children + helper getDescendantIds**

Thêm vào class (sau hàm `products()`):

```php
    public function parent()
    {
        return $this->belongsTo(ProductType::class, 'parent_id');
    }

    public function children()
    {
        return $this->hasMany(ProductType::class, 'parent_id');
    }

    /**
     * Trả về id toàn bộ con-cháu (đệ quy) — dùng để chống chu trình.
     */
    public function getDescendantIds(): array
    {
        $ids = [];
        foreach ($this->children as $child) {
            $ids[] = $child->id;
            $ids = array_merge($ids, $child->getDescendantIds());
        }
        return $ids;
    }
```

- [ ] **Step 3: Sửa `isCanDelete()` — cấm nếu còn sản phẩm HOẶC còn nhóm con**

Thay hàm `isCanDelete()` hiện có:

```php
    public function isCanDelete()
    {
        return $this->products()->count() === 0 && $this->children()->count() === 0;
    }
```

- [ ] **Step 4: Verify bằng tinker**

Run:
```bash
php artisan tinker --execute="\$p = Modules\Category\Entities\ProductType::first(); var_dump(method_exists(\$p,'getDescendantIds'), \$p->isCanDelete());"
```
Expected: in ra `bool(true)` cho method_exists, và `isCanDelete` trả bool không lỗi.

---

### Task 3: Request — validate `parent_id` + chống chu trình

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Http/Requests/ProductTypeRequest.php`

- [ ] **Step 1: Thêm rule `parent_id` + custom rule chống chu trình**

Thay hàm `rules()`:

```php
    public function rules()
    {
        return [
            'name' => 'required|max:255|unique:product_types,name,' . $this->id,
            'code' => [
                'required',
                'max:50',
                'regex:/^[A-Z]+\.[a-zA-Z0-9_]+$/',
                function ($attribute, $value, $fail) {
                    if (preg_match('/^[A-Z]+\.$/', $value)) {
                        $fail('Bắt buộc phải nhập');
                    }
                },
                'unique:product_types,code,' . $this->id,
            ],
            'parent_id' => [
                'nullable',
                'exists:product_types,id',
                function ($attribute, $value, $fail) {
                    if (!$value) {
                        return;
                    }
                    // Không tự làm cha chính mình
                    if ($this->id && (int) $value === (int) $this->id) {
                        $fail('Không thể chọn chính nhóm này làm nhóm cha');
                        return;
                    }
                    // Không chọn nhóm con/cháu của chính nó làm cha (chống chu trình)
                    if ($this->id) {
                        $current = \Modules\Category\Entities\ProductType::find($this->id);
                        if ($current && in_array((int) $value, $current->getDescendantIds(), true)) {
                            $fail('Không thể chọn nhóm con/cháu làm nhóm cha');
                        }
                    }
                },
            ],
        ];
    }
```

- [ ] **Step 2: Verify lỗi chu trình (manual qua API sau Phase 4)** — đánh dấu kiểm thử ở Task 12. Tạm thời verify cú pháp:

Run (tại `nhatlinh-api/`): `php -l Modules/Category/Http/Requests/ProductTypeRequest.php`
Expected: `No syntax errors detected`

---

### Task 4: Service — lưu parent_id, index tree=1, getAll kèm parent_id

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Services/ProductTypeService.php`

- [ ] **Step 1: `updateOrCreate()` lưu thêm `parent_id`**

Trong `updateOrCreate()`, ở cả nhánh update và create, thêm `'parent_id'`:

Nhánh update (`$item->update([...])`):
```php
                $item->update([
                    'code' => $normalizedCode,
                    'name' => $request->name,
                    'description' => $request->description,
                    'parent_id' => $request->parent_id ?: null,
                    'status' => $request->status,
                    'part_id' => auth()->user()->info->part_id,
                ]);
```

Nhánh create (`ProductType::create([...])`):
```php
            $item = ProductType::create([
                'name' => $request->name,
                'code' => $normalizedCode,
                'description' => $request->description,
                'parent_id' => $request->parent_id ?: null,
                'status' => $request->status,
                'part_id' => auth()->user()->info->part_id,
            ]);
```

- [ ] **Step 2: `update()` lưu thêm `parent_id`**

Trong `update(ProductTypeRequest $request, ProductType $item)`, thêm vào `$item->update([...])`:
```php
        $item->update([
            'name' => $request->name,
            'code' => strtoupper(trim($request->code)),
            'description' => $request->description,
            'parent_id' => $request->parent_id ?: null,
            'updated_by' => auth()->user()->id,
            'status' => $request->status,
        ]);
```

- [ ] **Step 3: `index()` hỗ trợ chế độ cây (`tree=1`)**

Ở cuối hàm `index()`, TRƯỚC dòng `return $query->orderBy('product_types.id', 'desc');`, thêm:

```php
        if ($request->filled('tree') && $request->tree == 1) {
            return $query->orderBy('product_types.parent_id', 'asc')
                         ->orderBy('product_types.id', 'asc');
        }
```

(Giữ nguyên dòng return mặc định bên dưới cho chế độ phẳng/phân trang.)

- [ ] **Step 4: `getAll()` trả thêm `parent_id`**

`getAll()` đang `->get()` toàn bộ cột nên đã có `parent_id`. Không cần sửa. Xác nhận bằng đọc lại hàm.

- [ ] **Step 5: Verify cú pháp**

Run: `php -l Modules/Category/Services/ProductTypeService.php`
Expected: `No syntax errors detected`

---

### Task 5: Transformer — trả `parent_id` + `parent_name`

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Transformers/ProductTypeResource/ProductTypeResource.php`
- Modify: `nhatlinh-api/Modules/Category/Transformers/ProductTypeResource/DetailProductTypeResource.php`

- [ ] **Step 1: Đọc 2 file resource để biết cấu trúc `toArray`**

Run: `sed -n '1,80p' nhatlinh-api/Modules/Category/Transformers/ProductTypeResource/ProductTypeResource.php`

- [ ] **Step 2: Thêm field vào mảng trả về của `ProductTypeResource::toArray()`**

Thêm 2 dòng (cùng cấp với `code`, `name`):
```php
            'parent_id' => $this->parent_id,
            'parent_name' => optional($this->parent)->name,
```

- [ ] **Step 3: Thêm tương tự vào `DetailProductTypeResource::toArray()`**

```php
            'parent_id' => $this->parent_id,
            'parent_name' => optional($this->parent)->name,
```

- [ ] **Step 4: Verify cú pháp**

Run:
```bash
php -l Modules/Category/Transformers/ProductTypeResource/ProductTypeResource.php
php -l Modules/Category/Transformers/ProductTypeResource/DetailProductTypeResource.php
```
Expected: `No syntax errors detected` (×2)

---

## Phase 2: Backend — Đổi tên (prefix NHH, export, permission)

### Task 6: Đổi prefix mã `LHH` → `NHH` (import)

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Services/ProductTypeService.php`

- [ ] **Step 1: Sửa regex + message trong `validateImportData()`**

Tìm đoạn:
```php
            if ($code && !preg_match('/^LHH\.[A-Za-z0-9_]+$/i', $code)) {
                $errors[] = 'Mã phải theo định dạng LHH.xxxx';
```
Thay thành:
```php
            if ($code && !preg_match('/^NHH\.[A-Za-z0-9_]+$/i', $code)) {
                $errors[] = 'Mã phải theo định dạng NHH.xxxx';
```

- [ ] **Step 2: Thêm xử lý cột "Mã nhóm cha" trong `validateImportData()`**

Sau khi validate `code/name/status`, thêm resolve parent (đặt trước dòng tạo `$rows[] = [...]`):

```php
            // Mã nhóm cha (optional)
            $parentCode = isset($item['parent_code']) ? strtoupper(trim($item['parent_code'])) : null;
            $parentId = null;
            if ($parentCode) {
                if ($parentCode === strtoupper((string) $code)) {
                    $errors[] = 'Nhóm cha không được trùng mã chính nó';
                    $isValid = false;
                } else {
                    $parent = $existingByCode->get($parentCode);
                    if (!$parent && !isset($codesInFile[$parentCode])) {
                        $errors[] = 'Mã nhóm cha không tồn tại';
                        $isValid = false;
                    } else {
                        $parentId = $parent ? $parent->id : null; // nếu cha nằm trong file, resolve khi import
                    }
                }
            }
```

Và bổ sung `'parent_code' => $parentCode` vào mảng `$rows[]`:
```php
            $rows[] = ['index' => $index, 'row' => $row, 'code' => $code, 'name' => $name, 'status' => $status, 'description' => $description, 'parent_code' => $parentCode, 'isValid' => $isValid, 'errors' => $errors];
```

- [ ] **Step 3: Xử lý `parent_code` khi tạo trong `importItems()`**

Trong vòng lặp tạo bản ghi, trước `ProductType::create([...])` thêm resolve parent theo DB (mã đã import ở vòng trước cũng có trong DB do tạo tuần tự):

```php
                $parentId = null;
                if (!empty($item['parent_code'])) {
                    $parent = ProductType::whereRaw('UPPER(code) = ?', [strtoupper(trim($item['parent_code']))])->first();
                    $parentId = $parent ? $parent->id : null;
                }
```

Và thêm `'parent_id' => $parentId` vào `ProductType::create([...])`.

- [ ] **Step 4: Verify cú pháp**

Run: `php -l Modules/Category/Services/ProductTypeService.php`
Expected: `No syntax errors detected`

---

### Task 7: Export — đổi filename + thêm cột "Mã nhóm cha"

**Files:**
- Modify: `nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/ProductTypeController.php`
- Modify: `nhatlinh-api/resources/views/exports/product_types.blade.php`

- [ ] **Step 1: Đổi filename export**

Trong `ProductTypeController::export()` đổi:
```php
                'danh_sach_loai_hang_hoa.xls'
```
thành:
```php
                'danh_sach_nhom_hang_hoa.xls'
```

- [ ] **Step 2: Đọc view export hiện tại**

Run: `cat nhatlinh-api/resources/views/exports/product_types.blade.php`

- [ ] **Step 3: Sửa header cột "loại hàng hoá" → "nhóm hàng hoá" + thêm cột "Mã nhóm cha"**

Trong file blade: đổi mọi text "loại hàng hoá" → "nhóm hàng hoá"; thêm 1 cột header `<th>Mã nhóm cha</th>` và ô dữ liệu tương ứng `<td>{{ optional($row['parent'] ?? null)['code'] ?? '' }}</td>` (điều chỉnh theo cấu trúc `$data` thực tế thấy ở Step 2 — `$data` là mảng đã transform; nếu có `parent_id` thì map sang code).

> Nếu `$data` không có sẵn mã nhóm cha, bổ sung `parent_name`/`parent_code` vào transformer (đã thêm `parent_name` ở Task 5; thêm `parent_code => optional($this->parent)->code` nếu cần cột mã).

- [ ] **Step 4: Verify cú pháp PHP của controller**

Run: `php -l Modules/Category/Http/Controllers/Api/V1/ProductTypeController.php`
Expected: `No syntax errors detected`

---

### Task 8: Permission — đổi tên 2 quyền + update DB + route middleware

**Files:**
- Modify: `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (dòng 1035-1036)
- Modify: `nhatlinh-api/Modules/Category/Routes/api.php` (block `/product-types`, dòng ~64-89)

- [ ] **Step 1: Sửa seeder (giữ nguyên id 1091, 1092)**

Đổi dòng 1035-1036 thành:
```php
        Permission::create(['id' => 1091, 'guard_name' => 'api', 'name' => 'Quản lý danh mục nhóm hàng hoá', 'display_name' => 'Quản lý danh mục nhóm hàng hoá', 'group' => 'Danh mục chung', 'type' => 8]);
        Permission::create(['id' => 1092, 'guard_name' => 'api', 'name' => 'Xem danh mục nhóm hàng hoá', 'display_name' => 'Xem danh mục nhóm hàng hoá', 'group' => 'Danh mục chung', 'type' => 8]);
```
(Comment dòng 1034 `// Danh mục loại hàng hoá` → `// Danh mục nhóm hàng hoá`)

- [ ] **Step 2: Update DB bản ghi hiện có (KHÔNG xóa-tạo lại, giữ role assignment)**

Run (tại `nhatlinh-api/`):
```bash
php artisan tinker --execute="
use App\Models\Permission;
Permission::where('id',1091)->update(['name'=>'Quản lý danh mục nhóm hàng hoá','display_name'=>'Quản lý danh mục nhóm hàng hoá']);
Permission::where('id',1092)->update(['name'=>'Xem danh mục nhóm hàng hoá','display_name'=>'Xem danh mục nhóm hàng hoá']);
app()['cache']->forget('spatie.permission.cache');
echo 'updated';
"
```
Expected: `updated`

- [ ] **Step 3: Sửa middleware trong routes**

Trong block `/product-types` của `Modules/Category/Routes/api.php`, thay toàn bộ chuỗi:
- `Quản lý danh mục loại hàng hoá` → `Quản lý danh mục nhóm hàng hoá`
- `Xem danh mục loại hàng hoá` → `Xem danh mục nhóm hàng hoá`

(7 dòng middleware: index, export, import/validate, import, post, put, show, delete, lock, unlock — đổi tất cả.)

- [ ] **Step 4: Verify**

Run: `php -l Modules/Category/Routes/api.php`
Expected: `No syntax errors detected`
Run kiểm tra DB: `php artisan tinker --execute="echo App\Models\Permission::find(1091)->name;"`
Expected: `Quản lý danh mục nhóm hàng hoá`

---

## Phase 3: Frontend — Đổi tên label + menu

### Task 9: Menu label

**Files:**
- Modify: `nhatlinh-client/components/default-menu/category.js`

- [ ] **Step 1: Đổi label**

Đổi:
```js
    {
        label: 'Loại hàng hoá',
        link: '/category/product-types',
    },
```
thành:
```js
    {
        label: 'Nhóm hàng hoá',
        link: '/category/product-types',
    },
```

- [ ] **Step 2: Verify UI** — chạy FE (`cd nhatlinh-client && npm run dev` nếu chưa chạy), mở `/category`, xác nhận menu hiển thị "Nhóm hàng hoá".

---

### Task 10: Đổi tên label trong `index.vue` + prefix import

**Files:**
- Modify: `nhatlinh-client/pages/category/product-types/index.vue`

- [ ] **Step 1: Thay toàn bộ chuỗi "loại hàng hoá" → "nhóm hàng hoá"** trong file (giữ nguyên hoa/thường):
  - Filter panel `title`, `quickSearchPlaceholder`.
  - Label filter "Mã loại hàng hoá" → "Mã nhóm hàng hoá", "Tên loại hàng hoá" → "Tên nhóm hàng hoá".
  - `V2BaseDataTable` `title="Danh sách loại hàng hoá"` → `"Danh sách nhóm hàng hoá"`, `itemLabel="loại hàng hoá"` → `"nhóm hàng hoá"`.
  - `tableColumns`: title cột `'Mã loại hàng hoá - Tên loại hàng hoá'` → `'Mã nhóm hàng hoá - Tên nhóm hàng hoá'`.
  - `deleteConfirmMessage`, `lockConfirmMessage`, title nút khoá (`'Khoá loại hàng hoá'`...).
  - `head().title`, `pageTitle()`.
  - Import modal: `title="Import Loại hàng hoá"` → `"Import Nhóm hàng hoá"`.
  - `importColumns`: label/aliases/placeholder "loại hàng hoá"→"nhóm hàng hoá", placeholder `'VD: LHH.0001'` → `'VD: NHH.0001'`.

- [ ] **Step 2: Đổi regex prefix import ở `importValidationRules()`**

Đổi:
```js
                const codePattern = /^LHH\..+$/
                if (!codePattern.test(code)) {
                    errors.push('Mã loại hàng hoá phải theo định dạng LHH.xxxx')
```
thành:
```js
                const codePattern = /^NHH\..+$/
                if (!codePattern.test(code)) {
                    errors.push('Mã nhóm hàng hoá phải theo định dạng NHH.xxxx')
```

- [ ] **Step 3: Đổi template file name (nếu giữ file mẫu cũ thì giữ; khuyến nghị đổi)**

Đổi `template-file-name="Mau_import_LoaiHangHoa.xlsx"` và `handleDownloadImportTemplate()` href/download `'/Mau_import_LoaiHangHoa.xlsx'` → `'/Mau_import_NhomHangHoa.xlsx'`. (Cần copy/đổi tên file mẫu trong `nhatlinh-client/static/` tương ứng + thêm cột "Mã nhóm cha".)

- [ ] **Step 4: Verify** — mở `/category/product-types`, xác nhận tất cả label hiển thị "nhóm hàng hoá".

---

## Phase 4: Frontend — Tree-table + field Nhóm cha

### Task 11: Helper dựng cây

**Files:**
- Create: `nhatlinh-client/pages/category/product-types/treeUtils.js`

- [ ] **Step 1: Tạo file helper**

```js
// Dựng cây từ list phẳng + làm phẳng có thứ tự (parent trước con), gắn _level/_hasChildren
export function buildOrderedTree(flatList) {
    const byId = new Map()
    flatList.forEach((n) => byId.set(n.id, { ...n, _children: [] }))
    const roots = []
    byId.forEach((node) => {
        const pid = node.parent_id
        if (pid && byId.has(pid)) {
            byId.get(pid)._children.push(node)
        } else {
            roots.push(node)
        }
    })
    const ordered = []
    const walk = (nodes, level) => {
        nodes.forEach((node) => {
            node._level = level
            node._hasChildren = node._children.length > 0
            ordered.push(node)
            walk(node._children, level + 1)
        })
    }
    walk(roots, 0)
    return ordered
}

// Lọc danh sách chọn "Nhóm cha": loại chính nó + toàn bộ con-cháu (khi sửa)
export function excludeSelfAndDescendants(flatList, selfId) {
    if (!selfId) return flatList
    const childrenOf = new Map()
    flatList.forEach((n) => {
        const pid = n.parent_id || 0
        if (!childrenOf.has(pid)) childrenOf.set(pid, [])
        childrenOf.get(pid).push(n.id)
    })
    const blocked = new Set([selfId])
    const stack = [selfId]
    while (stack.length) {
        const cur = stack.pop()
        ;(childrenOf.get(cur) || []).forEach((cid) => {
            if (!blocked.has(cid)) {
                blocked.add(cid)
                stack.push(cid)
            }
        })
    }
    return flatList.filter((n) => !blocked.has(n.id))
}
```

- [ ] **Step 2: Verify lint** — `cd nhatlinh-client && npx eslint pages/category/product-types/treeUtils.js` (nếu eslint cấu hình); nếu không, kiểm tra import không lỗi ở Task 12.

---

### Task 12: `index.vue` — chế độ cây (tải toàn bộ, indent, expand/collapse)

**Files:**
- Modify: `nhatlinh-client/pages/category/product-types/index.vue`

- [ ] **Step 1: Import helper + thêm state**

Thêm import: `import { buildOrderedTree } from './treeUtils'`
Thêm vào `data()`: `allRows: [], collapsedIds: [],` (mảng id nhóm đang thu gọn).

- [ ] **Step 2: Sửa `loadData()` sang chế độ cây**

Thay thân `loadData()` để gọi `tree=1`, không phân trang:

```js
        async loadData() {
            try {
                this.loading = true
                const apiFilters = {
                    tree: 1,
                    code: this.filters.code,
                    name: this.filters.name,
                    status: this.filters.status,
                    created_by: this.filters.created_by,
                    updated_by: this.filters.updated_by,
                    updated_from: this.filters.updated_from,
                    updated_to: this.filters.updated_to,
                }
                if (this.filters.keyword) apiFilters.keyword = this.filters.keyword

                const { data } = await this.$store.dispatch(
                    'apiGetMethod',
                    `category/product-types${buildQueryString(apiFilters)}`,
                )
                this.allRows = buildOrderedTree(data || [])
            } catch (error) {
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
                }
            } finally {
                this.loading = false
            }
        },
```

- [ ] **Step 3: Thêm computed `tableData` (lọc dòng hiển thị theo trạng thái thu gọn) + bỏ pagination**

Xoá `tableData` khỏi `data()` (đã chuyển sang `allRows`). Thêm computed:

```js
        tableData() {
            // Khi đang lọc (keyword/code/name/status) → BE đã lọc, hiển thị phẳng tất cả allRows
            const filtering =
                this.filters.keyword || this.filters.code || this.filters.name || this.filters.status
            if (filtering) return this.allRows
            // Ẩn dòng nếu có bất kỳ tổ tiên nào đang bị thu gọn
            const collapsed = new Set(this.collapsedIds)
            const byId = new Map(this.allRows.map((r) => [r.id, r]))
            return this.allRows.filter((row) => {
                let p = row.parent_id
                while (p && byId.has(p)) {
                    if (collapsed.has(p)) return false
                    p = byId.get(p).parent_id
                }
                return true
            })
        },
```

Trong template, đổi `<V2BaseDataTable :pagination="pagination" ...>` thành `<V2BaseDataTable :pagination="null" ...>` (ẩn thanh phân trang ở chế độ cây). Xoá các handler `@page-change`/`@page-size-change` không còn dùng (hoặc giữ no-op).

- [ ] **Step 4: Thêm toggle expand + sửa slot tên hiển thị thụt lề**

Thêm method:
```js
        toggleExpand(item) {
            const idx = this.collapsedIds.indexOf(item.id)
            if (idx >= 0) this.collapsedIds.splice(idx, 1)
            else this.collapsedIds.push(item.id)
        },
```

Sửa slot `#cell-itemInfo`: bọc phần `V2BaseTitleSubInfo` trong 1 `div` có `:style="{ paddingLeft: (item._level * 20) + 'px' }"` và thêm icon toggle trước tiêu đề:
```html
<template #cell-itemInfo="{ item }">
    <div class="d-flex justify-content-between align-items-start position-relative" style="padding-right: 120px">
        <div class="d-flex align-items-start" :style="{ paddingLeft: (item._level * 20) + 'px' }">
            <button
                v-if="item._hasChildren"
                type="button"
                class="tree-toggle-btn mr-1"
                @click="toggleExpand(item)"
            >
                <i :class="collapsedIds.includes(item.id) ? 'ri-arrow-right-s-line' : 'ri-arrow-down-s-line'"></i>
            </button>
            <span v-else class="tree-toggle-spacer mr-1"></span>
            <V2BaseTitleSubInfo ... (giữ nguyên nội dung cũ) ... />
        </div>
        <div class="row-actions"> ... (giữ nguyên) ... </div>
    </div>
</template>
```

Thêm style scoped:
```scss
.tree-toggle-btn { background: none; border: none; cursor: pointer; padding: 0; font-size: 16px; line-height: 1; color: #6b7280; }
.tree-toggle-spacer { display: inline-block; width: 16px; }
```

- [ ] **Step 5: Bỏ logic phân trang thừa**

Xoá/đơn giản hoá `handlePageChange`, `handlePageSizeChange`, và phần cập nhật `this.pagination` trong `loadData` (đã bỏ). Giữ `pagination` object trong data nếu còn ref khác, hoặc xoá hẳn nếu không dùng. `getNumericalOrder` ở slot `#cell-index`: thay bằng số thứ tự đơn giản `{{ index + 1 }}` (vì không còn phân trang).

- [ ] **Step 6: Verify UI**
  - Mở `/category/product-types`: danh sách hiển thị dạng cây, nhóm con thụt vào.
  - Click icon ▸/▾: thu gọn/mở nhánh.
  - Gõ tìm kiếm: hiển thị phẳng các kết quả khớp.

---

### Task 13: `AddProductTypeModal.vue` — field "Nhóm cha" + prefix NHH

**Files:**
- Modify: `nhatlinh-client/pages/category/product-types/AddProductTypeModal.vue`

- [ ] **Step 1: Đổi prefix mã + label**

Đổi `prefix="LHH."` → `prefix="NHH."`. Đổi mọi "loại hàng hoá" → "nhóm hàng hoá" (title modal, label, placeholder).

- [ ] **Step 2: Thêm field "Nhóm cha" vào template (Row mới sau Row 1)**

```html
<div class="form-row">
    <div class="col-md-12 mb-2">
        <V2BaseLabel>Nhóm cha</V2BaseLabel>
        <V2BaseSelect
            v-model="data.parent_id"
            :options="parentOptions"
            size="sm"
            :allowClear="true"
            placeholder="— Không có (nhóm gốc) —"
            :disabled="isShow"
        />
        <div v-if="formError['parent_id']" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError['parent_id'] }}
        </div>
    </div>
</div>
```

- [ ] **Step 3: Thêm state + load options nhóm cha**

Thêm import: `import { excludeSelfAndDescendants } from './treeUtils'`
Thêm vào `data()`: trong `data` object thêm `parent_id: null,`; thêm field cấp component `allTypes: [],`.
Thêm computed:
```js
    computed: {
        parentOptions() {
            const list = excludeSelfAndDescendants(this.allTypes, this.id)
            return list.map((t) => ({
                id: t.id,
                name: '— '.repeat(t._level || 0) + (t.code + ' - ' + t.name),
            }))
        },
    },
```
Thêm method tải danh sách (gọi `getAll` rồi dựng level bằng buildOrderedTree để hiển thị thụt lề):
```js
        async loadParentOptions() {
            try {
                const { data } = await this.$store.dispatch('apiGetMethod', 'category/product-types/getAll')
                const { buildOrderedTree } = require('./treeUtils')
                this.allTypes = buildOrderedTree(data || [])
            } catch (e) {
                this.allTypes = []
            }
        },
```
Gọi `loadParentOptions()` trong `mounted()` và trong `resetModal()`.

> Lưu ý: `getAll` trả list `{status: ACTIVE}` — đủ cho chọn nhóm cha. Nếu cần cả nhóm khoá làm cha thì đổi BE `getAll` bỏ filter status (hỏi trước khi đổi vì là hàm dùng chung).

- [ ] **Step 4: `loadData()` map `parent_id`**

Trong `loadData()` của modal, thêm `parent_id: data.parent_id || null,` vào object `this.data`.

- [ ] **Step 5: `resetData()` + `submitForm()` payload thêm `parent_id`**

`resetData()` thêm `parent_id: null,`.
`submitForm()` payload thêm:
```js
                    parent_id: this.data.parent_id || null,
```

- [ ] **Step 6: Verify UI**
  - Tạo mới: chọn "Nhóm cha" → lưu → danh sách hiển thị đúng cấp.
  - Sửa nhóm có con: dropdown "Nhóm cha" KHÔNG hiện chính nó + con-cháu.

---

## Phase 5: Kiểm thử tổng thể

### Task 14: Test end-to-end (manual)

- [ ] **Step 1: Tạo cây nhiều cấp**
  - Tạo nhóm gốc "Bàn ghế" (NHH.0001).
  - Tạo nhóm con "Bàn học sinh" (parent = Bàn ghế).
  - Tạo nhóm cháu "Bàn đơn" (parent = Bàn học sinh).
  - Xác nhận danh sách hiển thị 3 cấp thụt lề + expand/collapse hoạt động.

- [ ] **Step 2: Chống chu trình**
  - Sửa "Bàn ghế", thử chọn nhóm cha = "Bàn đơn" (cháu) → API trả 422, FE hiện lỗi "Không thể chọn nhóm con/cháu làm nhóm cha".
  - Thử chọn cha = chính nó → lỗi.

- [ ] **Step 3: Điều kiện xóa**
  - Xóa "Bàn ghế" (còn con) → bị chặn ("Dữ liệu đang được sử dụng").
  - Gán 1 sản phẩm vào "Bàn đơn" rồi xóa "Bàn đơn" → bị chặn.
  - Xóa nhóm lá không có sản phẩm → thành công.

- [ ] **Step 4: Import có "Mã nhóm cha"**
  - Import file: dòng 1 mã NHH.A100 (cha trống), dòng 2 mã NHH.A101 parent_code=NHH.A100 → cả 2 tạo đúng quan hệ.
  - Dòng có parent_code không tồn tại → báo lỗi dòng đó.
  - Dòng mã sai định dạng (không NHH.) → báo lỗi.

- [ ] **Step 5: Đổi tên & permission**
  - Menu hiển thị "Nhóm hàng hoá".
  - Export ra file `danh_sach_nhom_hang_hoa.xls` có cột "Mã nhóm cha".
  - Tài khoản chỉ có quyền "Xem danh mục nhóm hàng hoá" → xem được, không tạo/sửa/xóa được.

- [ ] **Step 6: Cập nhật plan + STATUS (wrap up)**
  - Đánh dấu `[x]` tất cả task xong.
  - Ghi Checkpoint vào plan.md.
  - Cập nhật STATUS.md.

---

## Checkpoint — 2026-06-04

**Trạng thái: CODE HOÀN THÀNH (chạy trực tiếp trên `main`, chưa commit theo yêu cầu).**

Đã thực thi qua subagent-driven (mỗi nhóm: implementer + spec review + code-quality review + fix):
- **Nhóm A — BE Phase 1 (Task 1-5):** ✅ migration parent_id, entity (parent/children/getDescendantIds BFS+visited, isCanDelete), Request chống chu trình, Service tree=1 + eager-load parent, transformer parent_id/parent_name/parent_code.
- **Nhóm B — BE đổi tên (Task 6-8):** ✅ prefix NHH (import regex), import cột "Mã nhóm cha", export filename + cột mã nhóm cha, permission seeder + update DB (giữ id 1091/1092) + middleware route, message text.
- **Nhóm FE (Task 9-13):** ✅ menu label, treeUtils.js, đổi tên toàn bộ index.vue + prefix NHH, tree-table (tải toàn bộ per_page=100000, indent + expand/collapse, pagination=null), modal field "Nhóm cha" (loại self+con-cháu, hiển thị nhóm cha inactive khi sửa).

**Đã verify chức năng BE thực tế (tinker):**
- getDescendantIds (A→[B,C], C→[]), isCanDelete (cha có con→false, lá→true), index tree ordering ✅
- Import nhóm cha: validate báo lỗi đúng khi cha không tồn tại, import link cha-con đúng ✅

**Quyết định review đáng chú ý:**
- getDescendantIds đổi sang BFS 1 query + visited set (chống N+1 + chống vòng lặp nếu data chu trình).
- tree=1 trả Builder → xử lý phía FE bằng `per_page=100000` (giữ shape data+meta).
- KHÔNG tạo migration cho permission (CLAUDE.md) — đã update DB dev qua tinker, production re-seed.

**Còn lại (cần user verify trên app đang chạy):**
- Test UI thủ công (Task 14 step 1-5 phần FE): tạo cây nhiều cấp, expand/collapse, chống chu trình hiển thị lỗi inline, import file Excel thật, kiểm tra phân quyền. BE đã smoke-test pass; FE chưa chạy dev server trong phiên này.
- File mẫu import `Mau_import_NhomHangHoa.xlsx` trong `nhatlinh-client/static/` (thêm cột "Mã nhóm cha") — chưa tạo file vật lý, mới đổi tên tham chiếu.

**Cập nhật sau review của user (2026-06-04):**
- Sửa bug field "Nhóm cha" lúc tạo mới hiện nhầm "(ngừng hoạt động)": do V2BaseSelect (Select2) phát giá trị string → so sánh `String()` + chỉ áp fallback khi đang sửa (`this.id`).
- **Đổi danh sách về MÔ HÌNH PHẲNG** (theo yêu cầu user): `index.vue` bỏ tree-table, quay lại bảng phân trang server như các danh mục khác. Giữ quan hệ cha-con ở DB + field "Nhóm cha" trong form + import cột "Mã nhóm cha". (Nhánh `tree=1` ở BE còn nhưng không dùng.)

**Bước tiếp theo:** user chạy `nhatlinh-client` + `nhatlinh-api`, test UI; sau đó tự commit. Feature kế tiếp trong Module 1: #2 `supplier-category` (DM-04).

---

## Self-review (đã rà)

- **Spec coverage:** Phần A (đổi tên: menu T9, label T10/T13, prefix T6/T10/T13, export T7, permission T8) ✓. Phần B (parent_id T1, entity T2, request T3, service T4, transformer T5, tree FE T11/T12, field nhóm cha T13) ✓. Edge cases (chống chu trình T3/T14, xóa T2/T14, import parent T6/T14) ✓.
- **Placeholder scan:** Mỗi step có code/command cụ thể; Task 7 Step 3 phụ thuộc cấu trúc view thực tế (đã ghi rõ đọc trước ở Step 2 + phương án bổ sung transformer).
- **Type consistency:** `buildOrderedTree`/`excludeSelfAndDescendants` dùng nhất quán giữa T11/T12/T13; field `parent_id`, `parent_name`, `_level`, `_hasChildren` đặt tên thống nhất.
