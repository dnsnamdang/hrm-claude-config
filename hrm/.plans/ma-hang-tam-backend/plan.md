# ma-hang-tam-backend — Plan

**@manhcuong · 2026-07-22**

## Phase 1 — Backend sinh mã

### BE
- [x] `QuotationService::saveDirectProduct`: xoá block sinh `HH-NNNNN` cũ; sau `create()` nếu hàng tạm & code rỗng → update `HHBG`+pad(id,6); nhánh update giữ code cũ
- [x] `BomListService::syncProducts`: sau create cha & con, nếu hàng tạm & code rỗng → update `HHB`+pad(id,6)
- [x] `BomListService::validateProductCodes`: nới bỏ bắt buộc code với hàng tạm (chỉ kiểm ERP)

## Phase 2 — Frontend bỏ trường Mã + bỏ sinh mã FE

### FE
- [x] `QuotationProductSearchModal.vue`: bỏ trường "Mã" (Tên hàng hoá full-width); createProduct phát `code: ''`
- [x] `quotations/_id/edit.vue`: `onAddProductApply` code rỗng; xoá `nextGoodsCode()`
- [x] `BomBuilderEditor.vue`: `handleAddProductApply` (2564) + `resetQuickGoodsForm` (2674) → code rỗng; xoá `getNextGoodsCode()`; nới `validateProductCodes` FE (chỉ kiểm ERP); `dedupeTempGoodsCodes` clear code khi trùng. (Dòng 1477 `popupGoods` = master product_projects deprecated, KHÔNG đụng — ngoài luồng hàng tạm)

## Verify (khi user yêu cầu)
- [ ] Báo giá tự xây + hàng tạm → HHBG+id, reload giữ mã
- [ ] BOM cha+con hàng tạm → HHB+id
- [ ] Sửa + thêm mới → dòng cũ giữ mã, dòng mới id mới
- [ ] Gộp sub-BOM không trùng mã
- [ ] Hàng ERP giữ mã ERP
