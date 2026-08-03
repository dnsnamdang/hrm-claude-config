# Design (tóm tắt) — Khung phân hệ Kinh doanh

**Spec đầy đủ:** `docs/superpowers/specs/2026-06-25-sale-module-scaffold-design.md`
**Phụ trách:** @manhcuong · **Ngày:** 2026-06-25

## Mục tiêu
Tạo phân hệ mới **"Kinh doanh"** (module `Sale`) — khung trống vào được qua switcher, render dashboard placeholder. Chưa nghiệp vụ, chưa permission.

## Quyết định lớn
- BE `Modules/Sale` (alias `sale`), FE `pages/sale`, URL `/sale`, label **Kinh doanh**.
- Trang đích `/sale/dashboard` (placeholder), dùng **layout chung `default.vue`** (PA A).
- Endpoint `GET api/v1/sale/dashboard` → `{ data: { module: 'sale' } }` (auth:api).
- Icon switcher: copy `icon_giao_hang.svg` → `icon_sale.svg`.
- **KHÔNG** entity/migration/permission/business logic.

## Scope đợt này
Scaffold BE (6 file + đăng ký modules_statuses) + FE 5 bước (dashboard, menu sale.js, wire default.vue, tile BasicSubsystem, copy icon).
