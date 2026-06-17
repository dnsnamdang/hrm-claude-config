# Plan: Danh mục Loại hàng hoá (Module Category)

## Phase 1: Backend
- [x] Migration: tạo bảng `product_types`
- [x] Model: `Modules/Category/Entities/ProductType.php`
- [x] Request: `Modules/Category/Http/Requests/ProductTypeRequest.php`
- [x] Service: `Modules/Category/Services/ProductTypeService.php`
- [x] Controller: `Modules/Category/Http/Controllers/Api/V1/ProductTypeController.php`
- [x] Resources: `ProductTypeResource.php`, `DetailProductTypeResource.php`
- [x] Export: `ProductTypeExport.php` + blade view
- [x] Routes: đăng ký trong `Modules/Category/Routes/api.php`

## Phase 2: Frontend
- [x] `pages/category/product-types/index.vue`
- [x] `pages/category/product-types/AddProductTypeModal.vue`

## Phase 3: Permissions + Menu
- [x] Seeder: id 1091 (Quản lý), 1092 (Xem)
- [x] DB insert + gán role Super admin
- [x] Menu sidebar: `components/default-menu/category.js`
- [x] Import template: `static/Mau_import_LoaiHangHoa.xlsx`

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ BE + FE + permissions
Đang làm dở: (không có)
Bước tiếp theo: Test trên trình duyệt
Blocked: (không có)
