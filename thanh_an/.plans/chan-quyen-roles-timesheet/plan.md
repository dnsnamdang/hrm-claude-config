# Chặn truy cập màn Phân quyền (roles) khi không có quyền — @khoipv

## Bối cảnh
- Menu "Thiết lập" (chứa mục Phân quyền) ẩn/hiện theo quyền `'Thiết lập thông số'` (`utils/menu.js:236`).
- Sidebar `SettingSlidebar.vue` không tự check quyền; backend `timesheet/roles` chỉ có `auth:api`.
- Bug: tài khoản không có quyền vẫn vào được `/timesheet/setting/roles/add/3` qua URL trực tiếp.
- Yêu cầu: không có quyền `'Thiết lập thông số'` → trả về 404.

## Task
- [x] (bỏ) ~~Middleware check-setting.js~~ → đổi sang pattern chuẩn dự án cho đồng nhất
- [x] `roles/index.vue` — `mounted()`: `hasAPermission('Thiết lập thông số')`, không có → `$router.push({ path: 'pages/extras/404' })`
- [x] `roles/add/_id.vue` — `mounted()`: check tương tự

## Ghi chú
- Theo đúng pattern đang dùng ở `pages/category/customer/_id/edit.vue` (mixin global `CheckPermission.hasAPermission` + push sang `pages/extras/404`).
- `hasAPermission` là global mixin (`plugins/global-mixins.js`), dùng được mọi component.
- Quyền gate: `'Thiết lập thông số'` — chính là quyền hiện menu "Thiết lập" (`utils/menu.js:236`).
- Hạn chế của pattern (giống các màn khác): check ở `mounted()` client-side; `asyncData` trong _id.vue vẫn gọi API `timesheet/permissions` 1 lần trước khi redirect. Chấp nhận để đồng nhất codebase.
