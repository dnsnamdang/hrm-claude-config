# Plan — Kế toán Module Scaffold

**Goal:** Scaffold khung module `Accounting` (BE + FE v2) nhất quán với module hiện có, chưa có entity nghiệp vụ.

**Spec:** `docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`

---

## Phase 1 — Backend scaffold

### BE
- [x] Tạo thư mục `hrm-api/Modules/Accounting/` copy structure từ `Modules/Decision/` (Config, Console, Database/{Migrations,Seeders,factories}, Entities, Enums, Export, Http/{Controllers/Api/V1,Requests,Middleware}, Jobs, Mail, Providers, Repositories, Resources/{views,lang,assets}, Routes, Rules, Services, Transformers)
- [x] Tạo `module.json` (name=Accounting, alias=accounting, provider AccountingServiceProvider)
- [x] Tạo `composer.json` (namespace `Modules\\Accounting\\`)
- [x] Tạo `Providers/AccountingServiceProvider.php`
- [x] Tạo `Providers/RouteServiceProvider.php` (prefix `api/v1/accounting`)
- [x] Tạo `Config/config.php` trả `['name' => 'Accounting']`
- [x] Tạo `Routes/api.php` với route `GET /dashboard` → `DashboardController@index` (middleware `auth:api`)
- [x] Tạo `Routes/web.php` (shell rỗng)
- [x] Tạo `Http/Controllers/Api/V1/DashboardController.php` (trả `{ module: 'accounting' }` + try/catch + Log::error)
- [x] Đăng ký `"Accounting": true` vào `hrm-api/modules_statuses.json`
- [x] Chạy `composer dump-autoload` + `php artisan module:list` — Accounting Enabled
- [x] Verify route `GET api/v1/accounting/dashboard` đã đăng ký (qua tinker)
- [ ] **Manual test (user thực hiện):** gọi `GET /api/v1/accounting/dashboard` với JWT → kỳ vọng `{ code: 200, data: { module: 'accounting' } }`

## Phase 2 — Frontend scaffold

### FE
- [x] Copy `assets/images/icon_quyet_dinh.svg` → `icon_ke_toan.svg` (placeholder)
- [x] Thêm commit `is_use_accounting` trong `store/actions.js` từ master-setting `use_accounting`
- [x] Thêm tile Kế toán + computed `isUseAccounting` trong `components/BasicSubsystem.vue`
- [x] Thêm tile Kế toán + computed tương tự trong `pages/index.vue`
- [x] Tạo layout riêng `layouts/accounting.vue` (style giống Assign: sidebar + topbar trên cùng)
- [x] Tạo `components/accounting-components/accounting-slidebar.vue` (sidebar có logo + 1 mục "Tổng quan")
- [x] Tạo `components/accounting-components/AccountingMenu.vue` (topbar với grid phân hệ + avatar/logout)
- [x] Tạo `assets/scss/custom-accounting.scss` (re-import custom-assign.scss)
- [x] Set `layout: 'accounting'` trong `pages/accounting/index.vue` + `dashboard.vue`
- [x] Gỡ wiring cũ trong `layouts/default.vue` (không dùng nữa vì có layout riêng)
- [x] Tạo `pages/accounting/index.vue` placeholder (V2BaseTitleSubInfo + v2-styles.scss)
- [x] Tạo `pages/accounting/dashboard.vue` placeholder
- [x] Thêm checkbox "Sử dụng kế toán" vào `pages/timesheet/setting/setting-master/index.vue` (state `useAccounting` + payload `use_accounting` + đọc ngược từ API category `use_accounting`)
- [ ] **Manual test (user thực hiện):** `yarn dev` build không lỗi
- [ ] **Manual test (user thực hiện):** insert master-setting `use_accounting=1` → tile "Kế toán" hiện ở grid + home → click vào `/accounting/dashboard` render placeholder

## Phase 3 — Wrap up

- [x] Cập nhật checkpoint + STATUS.md

---

### Checkpoint — 2026-04-21
Vừa hoàn thành: Phase 1 BE (11/11 task code) + Phase 2 FE (7/7 task code). Module `Accounting` Enabled trong `php artisan module:list`, route `GET api/v1/accounting/dashboard` đã đăng ký, tile FE đã wiring theo flag `is_use_accounting`.
Đang làm dở: Không có.
Bước tiếp theo: User manual test — (1) gọi endpoint với JWT, (2) `yarn dev` FE build + insert master-setting `use_accounting=1` để thấy tile. Sau khi test xong chuyển scaffold sang "Hoàn thành" trong STATUS.md.
Blocked: Không.
