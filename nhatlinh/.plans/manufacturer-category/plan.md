# Plan: Danh mục Hãng sản xuất (Module Category)

## Phase 1: Backend

### BE Tasks
- [x] Migration: tạo bảng `manufacturers`
- [x] Model: `Modules/Category/Entities/Manufacturer.php`
- [x] Request: `Modules/Category/Http/Requests/ManufacturerRequest.php`
- [x] Service: `Modules/Category/Services/ManufacturerService.php`
- [x] Controller: `Modules/Category/Http/Controllers/Api/V1/ManufacturerController.php`
- [x] Resources: `ManufacturerResource.php`, `DetailManufacturerResource.php`
- [x] Export: `ManufacturerExport.php` + blade view `exports/manufacturers.blade.php`
- [x] Routes: đăng ký routes trong `Modules/Category/Routes/api.php`

## Phase 2: Frontend

### FE Tasks
- [x] `pages/category/manufacturers/index.vue` — trang danh sách
- [x] `pages/category/manufacturers/AddManufacturerModal.vue` — modal tạo/sửa/xem

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ BE + FE cho danh mục Hãng sản xuất
Đang làm dở: (không có)
Bước tiếp theo: Test trên trình duyệt tại http://127.0.0.1:3000/category/manufacturers
Blocked: (không có)
