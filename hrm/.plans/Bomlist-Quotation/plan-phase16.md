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

---

## Phase 17 — Cascade status Dự án TKT + Giải pháp

> **Ngày bắt đầu:** 2026-05-05
> **Goal:** Khi gửi YCBG → đổi status Dự án TKT + Giải pháp sang "Chờ xây dựng giá". Khi báo giá duyệt cuối → đổi Dự án TKT sang "Thương thảo giá" + Giải pháp sang "Đã duyệt giá".

| Trigger | Dự án TKT | Giải pháp |
|---------|-----------|-----------|
| Gửi YCBG | → `STATUS_DU_TOAN` (6) | → `STATUS_CHO_LAM_GIA` (15) |
| Báo giá duyệt cuối | → `STATUS_THUONG_THAO_GIA` (7) | → `STATUS_DA_DUYET_GIA` (mới = 13) |

### BE
- [x] 25. `Solution.php`: thêm constant `STATUS_DA_DUYET_GIA = 13` + entry trong `STATUSES` array (`'Đã duyệt giá'`, color `success`)
- [x] 26. `PricingRequestService::send()`: cascade update `project.status = 6` + `solution.status = 15`
- [x] 27. `QuotationService`: tạo `cascadeApprovedStatus()` → update `project.status = 7` + `solution.status = 13`. Gọi tại 3 điểm duyệt cuối: `selfApprove()`, `tpApprove()` (Level 2), `bgdApprove()`

### Test thủ công
- [ ] 28. Gửi YCBG → Dự án TKT status = "Dự toán", Giải pháp status = "Chờ làm giá"
- [ ] 29. Duyệt báo giá (test cả 3 level) → Dự án TKT = "Thương thảo giá", Giải pháp = "Đã duyệt giá"
- [ ] 30. Gửi YCBG nhiều lần → status vẫn đúng (idempotent)

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

## Checkpoint — 2026-05-05 (Phase 17 code DONE)
Vừa hoàn thành: Cascade status Dự án TKT + Giải pháp — 3 task BE (25-27). Solution thêm STATUS_DA_DUYET_GIA=13. PricingRequestService::send() cascade project→Dự toán + solution→Chờ làm giá. QuotationService thêm cascadeApprovedStatus() gọi tại 3 nhánh duyệt cuối (selfApprove/tpApprove L2/bgdApprove) → project→Thương thảo giá + solution→Đã duyệt giá.
Bước tiếp theo: User test task 28-30 (gửi YCBG check status, duyệt báo giá check status, gửi nhiều lần check idempotent).
Blocked: Không.

---

## Phase 18 — Chốt giải pháp

> **Ngày bắt đầu:** 2026-05-06
> **Goal:** Sale click "Chốt giải pháp" trên chi tiết Dự án TKT → popup chọn 1 hồ sơ (Đã duyệt/Hết hiệu lực) + ghi chú → cascade status YCGP/GP/hồ sơ + thông báo PM & người tạo GP.

### Luồng xử lý

```
Sale click "Chốt giải pháp" (button trên manager.vue)
  └→ Popup hiện danh sách hồ sơ (status: approved / expired)
     └→ Sale chọn 1 hồ sơ + nhập ghi chú
        └→ Click "Lưu & thông báo"
           ├→ 1. Thông báo: PM giải pháp (solution.pm_id) + Người tạo GP (solution.created_by)
           ├→ 2. RequestSolution.status → STATUS_DA_CHOT_GP (mới)
           ├→ 3. Solution.status → STATUS_CHOT_GIAI_PHAP (17)
           ├→ 4. SolutionReviewProfile (được chọn).status → 'finalized'
           └→ 5. ProspectiveProject.status → STATUS_THUONG_THAO_DU_AN_HOP_DONG (8)
```

### Điều kiện hiển thị button
- User là `main_sale_employee_id` của dự án
- Có ít nhất 1 hồ sơ giải pháp ở status `approved` hoặc `expired`

### BE

#### Migration
- [x] 31. Migration `add_finalized_fields_to_solution_review_profiles`:
  - `finalized_at` datetime nullable
  - `finalized_note` text nullable

#### Entity constants
- [x] 32. `SolutionReviewProfile.php`: thêm `STATUS_FINALIZED = 'finalized'` + entry STATUSES array ('Đã chốt', color phù hợp)
- [x] 33. `RequestSolution.php`: thêm `STATUS_DA_CHOT_GP = 11` + entry STATUSES array ('Đã chốt giải pháp')

#### Service + Controller + Route
- [x] 34. `ProspectiveProjectService::finalizeSolution($project, $reviewProfileId, $note)`:
  - Validate: user là `main_sale_employee_id`
  - Validate: profile thuộc solution của project + status in (approved, expired)
  - DB::transaction:
    a. Update profile: status='finalized', finalized_at=now(), finalized_note=$note
    b. Update RequestSolution: status=STATUS_DA_CHOT_GP
    c. Update Solution: status=STATUS_CHOT_GIAI_PHAP (17)
    d. Update ProspectiveProject: status=STATUS_THUONG_THAO_DU_AN_HOP_DONG (8)
  - Notify: PM (solution.pm_id) + Creator (solution.created_by) — pattern `EmployeeInfoService::sendToAllNotification`
- [x] 35. `ProspectiveProjectController::finalizeSolution()` — gọi service, return response
- [x] 36. Request validation: `review_profile_id` required|exists, `note` nullable|string|max:1000
- [x] 37. Route: `POST /api/v1/assign/prospective-projects/{id}/finalize-solution`

#### API trả danh sách hồ sơ cho popup
- [x] 38. `ProspectiveProjectService::getFinalizableProfiles($project)`:
  - Query SolutionReviewProfile where solution_id + status in (approved, expired)
  - Return: id, code, solution_version_code, status, status_name, approved_at

### FE

- [x] 39. `FinalizeSolutionModal.vue` (component mới, theo pattern `CloseProjectModal.vue`):
  - Load danh sách hồ sơ từ API
  - Bảng: Mã hồ sơ, Version GP, Trạng thái, Ngày duyệt + radio chọn 1
  - Textarea: ghi chú chốt GP
  - Button: "Lưu & thông báo" (disabled khi chưa chọn hồ sơ)
- [x] 40. `manager.vue`: thêm button "Chốt giải pháp" + import modal + logic hiển thị (kiểm tra có hồ sơ approved/expired)
- [x] 41. Sau khi chốt thành công: reload data, toast success

### Test thủ công
- [ ] 42. Button chỉ hiện khi user là NV KD + có ít nhất 1 hồ sơ Đã duyệt/Hết hiệu lực
- [ ] 43. Popup hiện đúng danh sách hồ sơ, chọn 1 + nhập ghi chú → click Lưu
- [ ] 44. Sau chốt: YCGP = "Đã chốt GP", GP = "Chốt giải pháp", Hồ sơ = "Đã chốt", Dự án = "Thương thảo HĐ"
- [ ] 45. PM + người tạo GP nhận thông báo
- [ ] 46. User không phải NV KD → không thấy button
