# Kho dữ liệu hàng hoá — thêm cột "Trạng thái HH công ty quản lý"

**Chốt:** 03/11/2026 · **Nhánh:** `develop` (hrm-client + hrm-api) · **Trạng thái:** DONE (FE+BE+test+Playwright), CHƯA commit

## Yêu cầu

Màn **Kho dữ liệu hàng hoá** (`/master-data/products/warehouse`) thêm 1 cột **"Trạng thái HH công ty quản lý"** — hiển thị trạng thái của hàng hoá **tại chính công ty ĐANG QUẢN LÝ (sở hữu)** nó, không phụ thuộc công ty đang đăng nhập.

> Ví dụ user: hàng A do công ty TPE quản lý, trạng thái "Ngừng kinh doanh". Khi đăng nhập công ty Vinh xem Kho dữ liệu, cột này vẫn hiện "Ngừng kinh doanh" (trạng thái của công ty quản lý).

Vị trí cột: giữa **"Hệ số giá cũ"** và **"Trạng thái"** (ảnh mockup user chỉ mũi tên vào khoảng trống đó).

## Phát hiện then chốt — KHÔNG cần query mới

`owner_status` (= `pco.status` tại công ty quản lý) **đã được `ProductService::index()` select sẵn** qua scope `->withOwnerStatus()` (dùng nội bộ cho cờ `can_take_back`). Scope leftJoin 1:1 theo UNIQUE `(product_id, company_id)` nên **không N+1, không thêm query**. Đường export cũng dùng lại `index()` qua `->toBase()` nên `$item->owner_status` có sẵn.

- `Product::scopeWithOwnerStatus()` — leftJoin `product_company_coefficients as pco` ON `pco.product_id=products.id AND pco.company_id=products.company_id`, select `pco.status AS owner_status`.
- `owner_status = null` ở đường **catalog popup** (`ProductCatalogController::popupQuery` không select cột này) → resource null-safe, trả null, vô hại.

## Thay đổi

### BE (hrm-api)
- `Modules/MasterData/Transformers/Product/ProductListResource.php`
  - Tính `$ownerStatus = $this->owner_status !== null ? (int) $this->owner_status : null;`
  - Khối `owner_company_*` thêm 3 field badge: `owner_status`, `owner_status_text` (= `ProductCompany::STATUS_TEXT[$ownerStatus]`), `owner_status_color` (= `ProductCompany::STATUS_COLOR[$ownerStatus]`). Null-safe.
- `app/ExcelExport/ExportColumnRegistry.php`
  - `products_warehouse`: thêm `'owner_status_text' => 'Trạng thái HH công ty quản lý'` ngay trước `status_text` (khớp thứ tự cột FE).
- `Modules/MasterData/Services/Product/ProductExportService.php`
  - `cell()`: thêm `case 'owner_status_text'` → `ProductCompany::STATUS_TEXT[(int)$item->owner_status]`, không dòng ⇒ `''`.
  - `WIDTHS`: thêm `'owner_status_text' => 24`.

### FE (hrm-client)
- `utils/product-list-screens.js`
  - `warehouse.columns` + `warehouse.defaultColumns`: thêm `'owner_status'` ngay trước `'company_status'`.
  - `PRODUCT_COLUMN_DEFS`: `owner_status: { title: 'Trạng thái HH công ty quản lý', width: '200px', align: 'center' }`.
  - `PRODUCT_EXPORT_FIELD_KEY_MAP`: `owner_status: 'owner_status_text'`.
- `components/product/ProductListPage.vue`
  - Thêm `<template #cell-owner_status>` → `<V2BaseBadge v-if="item.owner_status" :color="item.owner_status_color">{{ item.owner_status_text }}</V2BaseBadge>`, rỗng ⇒ `—` xám. FE KHÔNG map số→chữ, KHÔNG tự chọn màu (đúng quy ước badge).

## Test

- `Modules/MasterData/Tests/Feature/ProductTakeApiTest.php`
  - Thêm `warehouse_tra_owner_status_badge_cua_cong_ty_quan_ly()`: B (công ty 6) xem Kho dữ liệu, hàng A (công ty 1) status `STOPPED` → `owner_status=4`, `owner_status_text='Ngừng kinh doanh'`, `owner_status_color=STATUS_COLOR[STOPPED]` (#DC2626); hàng không có dòng công ty quản lý → cả 3 field null.
- **Kết quả:** ProductTakeApiTest **28/28 xanh** (gồm test mới + `owner_status_chi_tu_dong_that` cũ). ProductExportApiTest 8/9 — 1 fail `khong_co_truong_gia_nao_trong_output` là **PRE-EXISTING** (bắt key `price_coefficients_text` chứa "price"), fail y hệt khi stash hết thay đổi của task này ⇒ không liên quan.

## Playwright

`http://127.0.0.1:3000/master-data/products/warehouse`:
- Header cột **"Trạng thái HH công ty quản lý"** xuất hiện đúng vị trí (index 15, giữa "Hệ số giá cũ" và "Trạng thái").
- Badge render từ màu BE: "Đang kinh doanh" → `rgb(22,163,74)` = `#16A34A` (= `STATUS_COLOR[3]`), FE đọc đúng `owner_status_color`. ✓
- Không có console error liên quan (chỉ noise HMR reexport-not-found của Nuxt dev).
