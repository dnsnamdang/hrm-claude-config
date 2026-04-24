# Plan Phase 16 — UI polish quotation + remote search BOM

> **Ngày bắt đầu:** 2026-04-23
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign`

**Goal:** Gom các điều chỉnh UI nhỏ phát sinh khi test Phase 14-15: hiển thị VAT trên dòng con, thêm Sửa/Xoá YCBG trong tab Hồ sơ, chuyển select Model/Brand/Xuất xứ sang remote search.

## Scope
- Dòng con trong Báo giá (edit + show): vẫn **hiển thị** Tiền VAT + Thành tiền sau VAT tính theo VAT% riêng của con. Tổng vẫn **không** cộng con (roll-up qua cha).
- Tab "Hồ sơ" (`/assign/prospective-projects/:id/manager`): sub-table YCBG thêm nút **Sửa** + **Xoá** khi `status === 1 && created_by === currentUser`.
- Popup "Thêm hàng hoá" (BOM): Model/Brand/Xuất xứ load 200 item mặc định, gõ thì gọi API remote search. Thêm nút **Làm mới** reset filter.

## BE
- [x] 1. `ProductProjectController::getModel|getBrands|getOrigins` — `orderBy('name')->limit(200)` giữ hỗ trợ `keyword`.
- [x] 2. `ProspectiveProjectService::listReviewProfiles` — expose `created_by` trong payload `pricing_requests[]`.

## FE
- [x] 3. `quotations/_id/edit.vue` + `quotations/_id/index.vue`:
  - `lineVatAmount(p)` / `lineAfterVat(p)`: bỏ early-return `null` cho con → compute theo VAT% con.
  - Template dòng con: thay "—" bằng `formatMoney(lineVatAmount(child))` / `formatMoney(lineAfterVat(child))`.
  - `totalVat` vẫn filter `!p.parent_id` — không đổi logic tổng.
- [x] 4. `ProspectiveProjectReviewProfilesTab.vue`: sub-table action cell thêm nút Sửa (→ `/assign/pricing-requests/:id/edit`) + Xoá (confirm + `apiDelete`). Method `canEditPricingRequest(pr)` + `handleDeletePricingRequest(pr)`.
- [x] 5. `components/V2BaseSelectRemote.vue` (mới): bọc jQuery Select2 trực tiếp với chế độ `ajax.transport` gọi `fetchFn(keyword)`. Emit `select` với `{id, text}`. Hỗ trợ `initialOption` cho value có sẵn.
- [x] 6. `BomBuilderAddProductModal.vue`:
  - Import `V2BaseSelectRemote` + đăng ký component.
  - Tab 1 filter (Model/Brand/Xuất xứ) + Tab 2 form (3 field tương ứng): `V2BaseSelect` → `V2BaseSelectRemote` với `fetchFn` tương ứng.
  - `fetchModels/fetchBrands/fetchOrigins` gọi `assign/product-projects/get-model|brand|origin?keyword=...`.
  - `selectedModel/selectedBrand/selectedOrigin` cache tên đã chọn qua `@select` → dùng khi set `*_name` trong `createProduct`.
  - Reset cache ở `watch show`, `resetNewProduct`, `onProductTypeChange(2)`.
- [x] 7. `BomBuilderAddProductModal.vue`: thêm nút **Làm mới** (`ri-refresh-line`) cùng hàng với filter (layout 3+2+2+2+3). Method `resetFilters()` clear keyword + 3 filter + gọi `searchProducts()`.

## Test thủ công
- [ ] 8. Báo giá có parent-children: dòng con hiện đúng Tiền VAT + Sau VAT theo VAT% riêng, tổng báo giá KHÔNG đổi (chỉ cộng qua cha).
- [ ] 9. Tab Hồ sơ → expand YCBG "Đang tạo" của chính mình → thấy 3 nút (Xem / Sửa / Xoá). YCBG status ≠ 1 hoặc không phải creator → chỉ thấy Xem.
- [ ] 10. Xoá YCBG từ tab Hồ sơ → confirm → biến mất khỏi list + toast success.
- [ ] 11. Popup thêm hàng hoá (Tab 1): click select Model → hiện 200 item → gõ search → gọi API remote → ra kết quả match.
- [ ] 12. Tab 2 "Thêm mới": chọn Model/Brand/Xuất xứ → submit → sản phẩm mới có đủ `model_name/brand_name/origin_name`.
- [ ] 13. Click **Làm mới** → 4 filter clear → reload danh sách hàng hoá có sẵn.

## Checkpoint — 2026-04-23 (Phase 16 code DONE)
Vừa hoàn thành:
- BE: limit 200 + orderBy name cho 3 endpoint Model/Brand/Origin; expose `created_by` trong YCBG payload của review-profiles.
- FE: hiển thị VAT per row cho dòng con (edit + show); thêm Sửa/Xoá YCBG trong tab Hồ sơ; tạo mới `V2BaseSelectRemote` dùng jQuery Select2 ajax; migrate 6 V2BaseSelect trong AddProductModal sang remote; thêm nút Làm mới + layout 3+2+2+2+3.
Bước tiếp theo: User test task 8-13.
Blocked: Không.
