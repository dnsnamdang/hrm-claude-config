# Design Phase 23: Đổi nguồn dữ liệu Danh sách hàng hoá dự án

## Mục tiêu

Chuyển trang "Danh sách hàng hoá dự án" (`/assign/product-project`) từ bảng `product_projects` sang `bom_list_products`. Bỏ bảng `product_projects`. Thêm trạng thái đồng bộ ERP (chờ làm tính năng sau).

## Quyết định

- Nguồn dữ liệu mới: `bom_list_products` JOIN `bom_lists` (lấy dự án, giải pháp)
- Bỏ hẳn bảng `product_projects` + `product_project_attachments`
- Trang danh sách chuyển sang **read-only** (bỏ CRUD, import) — tạo/sửa/xoá hàng hoá qua màn BOM
- 1 hàng hoá chỉ nằm trong 1 BOM (không trùng lặp)

## 1. Database

### Migration mới

```php
// 1. Thêm cột erp_sync_status vào bom_list_products
Schema::table('bom_list_products', function (Blueprint $table) {
    $table->tinyInteger('erp_sync_status')->default(0)->after('sort_order');
    // 0 = Chưa đồng bộ, 1 = Đã đồng bộ
});

// 2. Drop bảng product_project_attachments (FK trước)
Schema::dropIfExists('product_project_attachments');

// 3. Drop bảng product_projects
Schema::dropIfExists('product_projects');
```

## 2. Backend — Bỏ

| File | Hành động |
|------|-----------|
| `Entities/ProductProject.php` | Xoá |
| `Entities/ProductProjectAttachment.php` | Xoá |
| `Services/ProductProjectService.php` | Xoá |
| `Http/Controllers/Api/V1/ProductProjectController.php` | Giữ lại các method helper (get-model, get-brand, get-origin, get-unit, create-*), xoá CRUD |
| `Http/Resources/ProductProjectListResource.php` | Xoá |
| `ExcelExport/ProductProjectExport.php` (nếu có) | Xoá hoặc thay thế |
| Routes `api.php` | Xoá routes CRUD, giữ routes helper + đổi index |

## 3. Backend — Sửa/Tạo mới

### Controller: sửa `ProductProjectController`

**Method `index()`** — query mới:
```php
BomListProduct::query()
    ->join('bom_lists', 'bom_list_products.bom_list_id', '=', 'bom_lists.id')
    ->where('bom_lists.bom_list_type', BomList::TYPE_AGGREGATE)   // Chỉ BOM Tổng hợp
    ->where('bom_lists.status', BomList::STATUS_DA_DUYET)          // Chỉ Đã duyệt
    ->leftJoin('tp_models', 'bom_list_products.model_id', '=', 'tp_models.id')
    ->leftJoin('tp_brands', 'bom_list_products.brand_id', '=', 'tp_brands.id')
    ->leftJoin('tp_origins', 'bom_list_products.origin_id', '=', 'tp_origins.id')
    ->leftJoin('tp_units', 'bom_list_products.unit_id', '=', 'tp_units.id')
    ->select('bom_list_products.*', 'bom_lists.code as bom_code', 'bom_lists.name as bom_name',
             'bom_lists.prospective_project_id', 'bom_lists.solution_id',
             'tp_models.name as model_name', 'tp_brands.name as brand_name',
             'tp_origins.name as origin_name', 'tp_units.name as unit_name')
    ->with(['bomList.project', 'bomList.solution', 'creator.info'])
```

**Filters:**
- `keyword` — search code, name
- `model_id`, `brand_id`, `origin_id`, `unit_id`
- `prospective_project_id` (qua bom_lists)
- `solution_id` (qua bom_lists)
- `created_by`
- `erp_sync_status` (0/1)

**Response fields:**
- code, name, model_name, brand_name, origin_name, unit_name
- qty_needed, estimated_price, quoted_price, product_attributes
- bom_code, bom_name (từ bom_lists)
- project_name, solution_name (qua relation)
- erp_sync_status, created_by_name, created_at

**Method `export()`** — xuất Excel từ query tương tự

**Bỏ methods:** store, update, destroy, importValidate, importProducts, show, getAll

**Giữ methods:** getModel, getBrands, getOrigins, getUnits, getManufacturers, getTaxRates, getGroupProduct, createModel, createBrand, createOrigin, createUnit

### Routes cập nhật

```php
// Giữ
Route::get('/product-projects', [ProductProjectController::class, 'index']);
Route::get('/product-projects/export', [ProductProjectController::class, 'export']);
Route::get('/product-projects/get-model', ...);
Route::get('/product-projects/get-brand', ...);
Route::get('/product-projects/get-origin', ...);
Route::get('/product-projects/get-unit', ...);
Route::get('/product-projects/get-manufacturer', ...);
Route::get('/product-projects/get-group-product', ...);
Route::get('/product-projects/get-tax-rates', ...);
Route::get('/product-projects/get-suppliers', ...);
Route::post('/product-projects/create-model', ...);
Route::post('/product-projects/create-brand', ...);
Route::post('/product-projects/create-origin', ...);
Route::post('/product-projects/create-unit', ...);

// Bỏ
// POST   /product-projects (store)
// GET    /product-projects/getAll
// GET    /product-projects/{id} (show)
// PUT    /product-projects/{id} (update)
// DELETE /product-projects/{id} (destroy)
// POST   /product-projects/import/validate
// POST   /product-projects/import
```

## 4. Frontend — Sửa `product-project/index.vue`

### Bỏ
- Button "Thêm mới", Import
- Row actions: Sửa, Xoá
- Component `CreateProductProjectModal`
- Các data/method liên quan CRUD

### Giữ
- Danh sách read-only
- Column customization
- Export Excel
- Quick search
- Sorting, pagination

### Thêm cột mới
- **Mã BOM** — `bom_code` (link sang BOM chi tiết)
- **Trạng thái ĐB** — `erp_sync_status` (pill: "Chưa đồng bộ" xám, "Đã đồng bộ" xanh)

### Bỏ cột
- Nhà cung cấp, Nhóm hàng, Hãng SX, VAT, Loại hàng hoá

### Filter cập nhật
- Giữ: keyword, Model, Thương hiệu, Xuất xứ, ĐVT, Dự án, Giải pháp, Người tạo
- Thêm: Trạng thái đồng bộ ERP (select: Tất cả / Chưa đồng bộ / Đã đồng bộ)
- Bỏ: Nhà cung cấp, Nhóm hàng, Hãng SX, VAT, Loại hàng hoá

### Row action
- Chỉ còn: Xem chi tiết BOM (navigate `/assign/bom-list/{bom_list_id}`)

## 5. Bỏ file

### Backend
- `Modules/Assign/Entities/ProductProject.php`
- `Modules/Assign/Entities/ProductProjectAttachment.php`
- `Modules/Assign/Services/ProductProjectService.php`
- `Modules/Assign/Http/Resources/ProductProjectListResource.php`

### Frontend
- `pages/assign/product-project/components/CreateProductProjectModal.vue`

## 6. Ảnh hưởng downstream

- BOM add product modal — **không ảnh hưởng** (đã dùng `erp-products` + `bom-products`, không dùng `product_projects`)
- Routes helper (get-model, create-brand...) — **giữ nguyên endpoint**, chỉ bỏ dependency vào ProductProject entity
- Entity `BomListProduct` — thêm accessor `erp_sync_status_name`, thêm vào `$appends` nếu cần
