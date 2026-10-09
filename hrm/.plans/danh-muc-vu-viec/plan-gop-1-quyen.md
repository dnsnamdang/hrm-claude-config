# Gộp quyền Danh mục vụ việc: 2 quyền → 1 quyền "Quản lý"

## Yêu cầu (user)
Chỉ dùng 1 quyền "Quản lý danh mục vụ việc". Bỏ "Xem danh mục vụ việc".

## Thay đổi
- [x] BE seeder `PermissionsTableSeeder.php`: xóa dòng create "Xem danh mục vụ việc" (giữ "Quản lý")
- [x] BE `Modules/Finance/Routes/api.php`: 2 route đang gate `Xem danh mục vụ việc`
      (index dòng 83, check-has-accounting dòng 87) → đổi sang `Quản lý danh mục vụ việc`
- [x] FE `components/subsystem-menu/finance.js:42`: isShow `['Quản lý danh mục vụ việc']`
- [x] FE `pages/finance/works/index.vue`: đã chỉ dùng "Quản lý" (giữ nguyên)
- [x] DB erp_hrm_check: xóa permission "Xem danh mục vụ việc"; gán "Quản lý danh mục vụ việc" vào role 18 (Super admin guard api)
- [ ] User: đăng xuất/đăng nhập lại → menu hiện
