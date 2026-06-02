# Plan: Danh mục Nước sản xuất (Module Category)

## Phase 1: Backend
- [x] Migration: tạo bảng `country_of_origins`
- [x] Model: `Modules/Category/Entities/CountryOfOrigin.php`
- [x] Request: `Modules/Category/Http/Requests/CountryOfOriginRequest.php`
- [x] Service: `Modules/Category/Services/CountryOfOriginService.php`
- [x] Controller: `Modules/Category/Http/Controllers/Api/V1/CountryOfOriginController.php`
- [x] Resources: `CountryOfOriginResource.php`, `DetailCountryOfOriginResource.php`
- [x] Export: `CountryOfOriginExport.php` + blade view
- [x] Routes: đăng ký trong `Modules/Category/Routes/api.php`

## Phase 2: Frontend
- [x] `pages/category/country-of-origins/index.vue`
- [x] `pages/category/country-of-origins/AddCountryOfOriginModal.vue`

## Phase 3: Permissions + Menu
- [x] Seeder: id 1089 (Quản lý), 1090 (Xem)
- [x] DB insert + gán role Super admin
- [x] Menu sidebar: `components/default-menu/category.js`
- [x] Import template: `static/Mau_import_NuocSanXuat.xlsx`

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ BE + FE + permissions
Đang làm dở: (không có)
Bước tiếp theo: Test trên trình duyệt
Blocked: (không có)
