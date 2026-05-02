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

## Bug fix (Phase 16 test)
- [x] 14. Fix `applyBulkVat` chỉ áp VAT cho parent (`whereNull('parent_id')`) → sửa áp cho tất cả cấp (cha + con + orphan).
- [x] 15. Fix tab Hồ sơ: lấy thêm hồ sơ `status=expired` + thêm cột Trạng thái (V2BaseBadge).
- [x] 16. Bỏ log history `update_vat_bulk` khỏi `applyBulkVat` (không ghi lịch sử phê duyệt).
- [x] 17. Thêm validate `vat_percent: nullable|numeric|min:0|max:100` vào `QuotationUpdateRequest` + FE validate VAT < 0 (toast "Giá trị VAT không hợp lệ" + border đỏ).
- [x] 18. Fix `PricingRequestService::ensureDraftAndOwner` strict comparison `!==` → `(int)` cast (status string "1" !== int 1 → luôn block sửa).
- [x] 19. `PricingRequestFormModal` hỗ trợ edit mode (prop `requestId`): load data GET show → fill form → PUT update. Tab Hồ sơ nút Sửa mở modal thay vì navigate sang link.
- [x] 20. Fix toast trùng khi sửa YCBG (bỏ toast parent `onPricingRequestSaved`, giữ toast modal).
- [x] 21. Fix emit `saved` dùng `created` undefined trong edit mode → dùng `{ id: savedId }`.
- [x] 22. Tab Báo giá trong manager: thêm cột "Loại tiền tệ", đổi "Tổng bán" → "Tổng giá trị báo giá" dùng `total_after_vat`, fix "Ngày duyệt" invalid Date (hiển thị string đã format từ API).
- [x] 23. Thêm option "Đóng" (value:5) vào filter trạng thái `/assign/quotations`.
- [x] 24. Fix `CompactReviewEditor` textarea gốc bị hiện double với CKEditor → ẩn khi `isEditorReady`.

## Checkpoint — 2026-04-23 (Phase 16 code DONE)
Vừa hoàn thành:
- BE: limit 200 + orderBy name cho 3 endpoint Model/Brand/Origin; expose `created_by` trong YCBG payload của review-profiles.
- FE: hiển thị VAT per row cho dòng con (edit + show); thêm Sửa/Xoá YCBG trong tab Hồ sơ; tạo mới `V2BaseSelectRemote` dùng jQuery Select2 ajax; migrate 6 V2BaseSelect trong AddProductModal sang remote; thêm nút Làm mới + layout 3+2+2+2+3.
Bước tiếp theo: User test task 8-13.
Blocked: Không.

## Checkpoint — 2026-04-29 (Bug fix batch)
Vừa hoàn thành: 11 bug fix (task 14-24) từ user test — VAT bulk apply tất cả cấp, validate VAT≥0, fix strict comparison block sửa YCBG, modal edit YCBG thay navigate, fix double textarea CKEditor, cột tiền tệ + tổng giá trị + ngày duyệt tab Báo giá, filter Đóng cho quotations.
Bước tiếp theo: User test lại toàn bộ task 8-13 + các bug fix mới.
Blocked: Không.
