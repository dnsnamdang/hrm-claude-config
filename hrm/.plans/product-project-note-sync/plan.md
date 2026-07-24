# Plan — Fix cột Ghi chú Hàng hóa dự án

## Phase 1 — Database
- [x] Migration thêm `note` TEXT nullable vào `quotation_product_prices`
- [x] Migration thêm `note` TEXT nullable vào `bom_list_products`
- [x] Chạy migrate + verify cột tồn tại (1 file gộp 2 bảng)

## Phase 2 — Backend
- [x] `QuotationProductPrice`: `$guarded=[]` sẵn → note ghi được (không cần sửa)
- [x] `QuotationService::saveDirectProduct`: map `note` (create + update cùng `$data`)
- [x] `BomListService::mapProductPayload`: map `note` từ `$row`
- [x] `ProductProjectController::transformQuotationItem`: `note => $item->note`
- [x] `php -l` các file sửa (sạch)

## Phase 3 — Frontend Báo giá
- [x] `QuotationProductSearchModal.vue`: `note` vào `createProduct` + `applySelection`
- [x] `quotations/_id/edit.vue`: apply handler set `note` (dòng chính + con recipe) + payload lưu gửi `note` + load đọc `p.note`
- [x] `DetailQuotationResource.php`: trả `note` cho product (round-trip edit)

## Phase 4 — Frontend BOM
- [x] `BomBuilderAddProductModal.vue`: `note` vào `createProduct` + `applySelection`
- [x] `BomBuilderEditModal.vue`: input `editForm.note` sẵn; editForm build đọc row.note; save (`updatedRow`) đã có note
- [x] `BomBuilderEditor.vue`: `mapGroupRowForSave` payload +note; `handleAddProductApply` newRow +note; recipe child +note; `cloneSubBomGroup` (gộp sub-BOM) cha/con +note; popup-select builders (4 chỗ) +note

## Phase 5 — Data test + Verify
- [x] Chèn 3 hàng tạm (2 có note, 1 không) vào BG-2026-00001 + duyệt (status=4) project 8
- [x] Verify BE transform trả note đúng (tinker: HH-90001/90002 có note, HH-90003 null)
- [x] Verify UI `/assign/product-project?prospective_project_id=8` — cột Ghi chú hiển thị đúng (Playwright, ảnh product-project-note-fixed.png)
- [x] Verify trang sửa báo giá vẫn render (19 dòng, no error overlay); không compile error FE
- [ ] (User) test thực tế tạo/sửa hàng tạm mới ở form báo giá + BOM builder lưu note round-trip

## Phase 6 — Fix cột "Người tạo" trống (hàng từ báo giá đã duyệt)
- [x] Root cause: `transformQuotationItem` đọc `$creator->fullname` thẳng trên Employee (Modules\Human\Entities\Employee KHÔNG có accessor fullname) → luôn null. Nhánh BOM `transformItem` đọc đúng qua `employee_create->info->fullname`.
- [x] Fix: đổi `$creator = optional(optional($quotation)->creator)` → `optional(optional(optional($quotation)->creator)->info)` (đọc qua ->info). Eager load `quotation.creator.info` đã có sẵn, không cần sửa query.
- [x] `php -l` sạch + tinker verify: OLD=NULL, NEW='DNS Admin' (quotation_id=1, created_by=13)

---
### Checkpoint — 2026-07-06 (Phase 6)
Vừa hoàn thành: Fix cột "Người tạo" trống ở màn Hàng hóa dự án cho hàng đồng bộ từ báo giá đã duyệt. Sửa `ProductProjectController::transformQuotationItem` đọc `creator->info->fullname` thay vì `creator->fullname`.
Đang làm dở: (không)
Bước tiếp theo: User hard-refresh màn `/assign/product-project` xác nhận cột "Người tạo" hiển thị tên NV khởi tạo.
Blocked:
