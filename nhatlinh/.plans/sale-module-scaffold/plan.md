# Plan — Khung phân hệ Kinh doanh (Sale Module Scaffold)

**Goal:** Scaffold khung module `Sale` (BE + FE), dashboard trống vào được qua switcher. Chưa entity/permission/nghiệp vụ.
**Spec:** `docs/superpowers/specs/2026-06-25-sale-module-scaffold-design.md`
**Plan chi tiết:** `docs/superpowers/plans/2026-06-25-sale-module-scaffold.md`
**Phụ trách:** @manhcuong

---

## Phase 1 — Backend (`nhatlinh-api/Modules/Sale`) — ✅ REVIEW PASS
- [x] `module.json` (name=Sale, alias=sale, provider SaleServiceProvider)
- [x] `composer.json` (namespace `Modules\Sale\`)
- [x] `Config/config.php` → `['name' => 'Sale']`
- [x] `Providers/RouteServiceProvider.php` (copy Rice, Route::prefix('api'))
- [x] `Providers/SaleServiceProvider.php` (copy Rice/Category)
- [x] `Routes/api.php` (group `/v1/sale` auth:api → GET /dashboard)
- [x] `Routes/web.php` (rỗng)
- [x] `Http/Controllers/Api/V1/DashboardController.php` (trả `{module:'sale'}`)
- [x] Đăng ký `"Sale": true` vào `modules_statuses.json`
- [x] Verify `php artisan module:list` → Sale **Enabled** (route:list lỗi pre-existing ở module Decision, không liên quan; route Sale xác minh qua đọc file)
- [ ] Manual test user: `GET /api/v1/sale/dashboard` + JWT → `{code:200,data:{module:'sale'}}`
- Minor (final review): `use ...Eloquent\Factory;` thừa trong `SaleServiceProvider` (copy từ Rice gốc)

## Phase 2 — Frontend (`nhatlinh-client`) — ✅ REVIEW PASS (5/5, 0 thừa)
- [x] Copy `icon_giao_hang.svg` → `icon_sale.svg`
- [x] `pages/sale/dashboard/index.vue` (placeholder, layout default, title "Kinh doanh")
- [x] `components/default-menu/sale.js` (`saleItems` — mục "Tổng quan")
- [x] Wire `layouts/default.vue` (import saleItems dòng 10 + nhánh `firstUri==='sale'` dòng 92-94)
- [x] Thêm tile "Kinh doanh" vào `components/BasicSubsystem.vue` (dòng 83-88, icon_sale.svg, không gate)
- [x] **(BỔ SUNG sau review)** Thêm tile "Kinh doanh" vào lưới trang chủ `pages/index.vue` (layout `system`) — đây mới là "phân hệ" user thấy ở localhost root. Plan ban đầu sót nơi này.
- [ ] Verify `yarn dev` build sạch (user — Node14 npx eslint không chạy được trong subagent)
- [ ] Manual test user: tile hiện → click → /sale/dashboard + sidebar "Tổng quan"

## Phase 3 — Wrap up
- [x] Cập nhật checkpoint + STATUS.md

---

### Checkpoint — 2026-06-25 (CODE HOÀN THÀNH)
Vừa hoàn thành: **Toàn bộ khung phân hệ Kinh doanh (module `Sale`)** — subagent-driven, chạy main chưa commit.
 - BE: `Modules/Sale` (module.json, composer.json, Config, 2 Providers, Routes api/web, DashboardController) + `"Sale": true` trong modules_statuses.json. Module **Enabled**. Endpoint `GET api/v1/sale/dashboard` → `{code:200,data:{module:'sale'}}`. Task review PASS.
 - FE: `pages/sale/dashboard/index.vue` (placeholder) + `default-menu/sale.js` + wire `layouts/default.vue` (dòng 10, 92-94) + tile "Kinh doanh" trong `BasicSubsystem.vue` (dòng 83-88) + `icon_sale.svg`. Task review PASS 5/5, 0 thừa.
 - Integration check: định danh `sale` nhất quán BE↔FE.
Đang làm dở: (không).
Bước tiếp theo: **User test thủ công** — (1) `GET /api/v1/sale/dashboard` + JWT; (2) `yarn dev` FE → switcher hiện tile "Kinh doanh" → click vào /sale/dashboard render placeholder + sidebar "Tổng quan". Sau đó user tự commit. Đợt sau: bổ sung nghiệp vụ Kinh doanh (mỗi feature 1 spec/plan).
Minor (chưa fix, để nhất quán pattern Rice): `use ...Eloquent\Factory;` thừa trong `SaleServiceProvider` — `RiceServiceProvider` gốc cũng có import này.
Blocked: (không)
