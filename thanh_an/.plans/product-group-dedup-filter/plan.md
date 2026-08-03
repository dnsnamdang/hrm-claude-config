# Plan — Gộp nhóm hàng hóa trùng tên ở bộ lọc (@namdangit)

Feature: `product-group-dedup-filter` · Màn `category/product` · 2026-07-27

## Phase 1 — Backend
- [x] BE1: `ProductService::index` (`:61-67`) — cho `product_group_id` nhận cả mảng (whereIn) lẫn đơn, giống pattern `array_product_id` (`:53-59`)
- [x] BE2: `php -l ProductService.php` sạch

## Phase 2 — Frontend
- [x] FE1: Computed `listProductGroupFilter` (`index.vue:823-838`) — thêm nhánh chưa chọn mảng → gộp `listProductGroup` theo `text`, mỗi tên 1 option (giữ id đầu tiên)
- [x] FE2: `getData()` — thêm method `buildProductQuery(overrides)` (`index.vue:850-868`): chưa chọn mảng + có `product_group_id` → gom tất cả id cùng `text`; nối tay `product_group_id[]=<id>`. Dùng chung cho cả `fetchAllProductsForExport` (export nhất quán)
- [x] FE3: Đã kiểm tra tĩnh cấu trúc (braces cân bằng, không sót biến cũ). Nuxt compile đầy đủ chờ dev server

## Phase 2b — Rà soát & vá các màn lọc nhóm khác (audit toàn client)
- [x] AUD: phân loại 32 file có `product_group` → (A) lọc cần vá / (B) nhập liệu giữ nguyên / (C) không liên quan
- [x] A2: `pages/category/product_templates/index.vue` — computed `listProductGroupFilter` (gộp) + đổi binding `:options` + `getProductGroup` giữ `array_product_id` + `buildProductQuery` (`product_group_id[]=`). Endpoint dùng chung `ProductService::index` (đã fix BE)
- [x] A3: `components/modal/ProductModal.vue` — computed gộp + helper `resolveProductGroupIds()` áp cả nhánh client (`includes`) và server (`buildQuery` mảng)
- [x] A4: `components/modal/ProductModalWithDuplicate.vue` — như A3
- [x] A5: `components/modal/ProductModalAdditionalInfo.vue` — computed gộp + `resolveProductGroupIds()` (chỉ nhánh server)
- [x] A6: `pages/contract/reports/sale-product/index.vue` — KHÔNG cần sửa (đã lọc theo tên gom-duy-nhất, không trùng)
- [x] A7: Xác nhận nhóm (B) form nhập liệu KHÔNG bị đụng (dùng `formSubmit.array_product_id`, không phải `formFilter`)

## Phase 3 — Verify
- [ ] V1: Chưa chọn mảng → dropdown nhóm chỉ 1 "nước tiểu"; chọn → sản phẩm ra cả 2 mảng
- [ ] V2: Chọn mảng → dropdown nhóm chỉ nhóm của mảng đó, lọc đúng như cũ
- [ ] V3: Backward — `product_group_id=A` (đơn) vẫn đúng
- [ ] V4: User verify UI E2E

## Checkpoint

### Checkpoint — 2026-07-27
Vừa hoàn thành: BE1-BE2 (ProductService whereIn); FE1-FE3 (product/index); Phase 2b — vá thêm 3 màn lọc (product_templates/index + 3 modal ProductModal*), audit toàn client xác nhận nhóm B/C không đụng. Backend chỉ 1 fix ProductService::index phủ hết.
Đang làm dở: không có — code xong toàn bộ 5 màn filter (A).
Bước tiếp theo: user verify UI E2E (V1-V4) trên 2 màn danh sách + 3 modal chọn hàng.
Blocked: cần Nuxt dev server để verify runtime.
