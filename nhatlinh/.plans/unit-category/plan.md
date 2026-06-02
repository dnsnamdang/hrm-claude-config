# Plan: Danh mục Đơn vị tính (Module Category)

## Phase 1: Backend
- [x] Migration: tạo bảng `units`
- [x] Model: `Modules/Category/Entities/Unit.php`
- [x] Request: `Modules/Category/Http/Requests/UnitRequest.php`
- [x] Service: `Modules/Category/Services/UnitService.php`
- [x] Controller: `Modules/Category/Http/Controllers/Api/V1/UnitController.php`
- [x] Resources: `UnitResource.php`, `DetailUnitResource.php`
- [x] Export: `UnitExport.php` + blade view
- [x] Routes: đăng ký trong `Modules/Category/Routes/api.php`

## Phase 2: Frontend
- [x] `pages/category/units/index.vue`
- [x] `pages/category/units/AddUnitModal.vue`

## Phase 3: Permissions + Menu
- [x] Seeder: id 1093 (Quản lý), 1094 (Xem)
- [x] DB insert + gán role Super admin
- [x] Menu sidebar: `components/default-menu/category.js`
- [x] Import template: `static/Mau_import_DonViTinh.xlsx`

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ BE + FE + permissions
Đang làm dở: (không có)
Bước tiếp theo: Test trên trình duyệt
Blocked: (không có)
