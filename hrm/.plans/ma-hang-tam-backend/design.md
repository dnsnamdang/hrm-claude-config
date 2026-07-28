# ma-hang-tam-backend — Tóm tắt

**@manhcuong · 2026-07-22**

## Mục tiêu
Bỏ trường "Mã" khi tạo hàng tạm (Báo giá + BOM). Mã do **Backend tự sinh khi lưu**, theo `id` dòng để không trùng. Sinh 1 lần, giữ cố định.

## Quyết định
- Prefix tách nguồn: Báo giá tự xây = `HHBG`+id (bảng `quotation_product_prices`), BOM = `HHB`+id (bảng `bom_list_products`). Pad 6 số → `HHBG000012`.
- Chỉ sinh cho hàng tạm (`erp_product_id` NULL) & khi `code` rỗng. Dòng cũ FE gửi lại code → BE giữ nguyên.
- Không trùng: prefix tách 2 bảng + `id` không tái dùng.
- Hướng "nhẹ" — **sinh 1 lần giữ cố định**, KHÔNG refactor delete-recreate BOM, KHÔNG sửa FE gửi id.
- Giữ nguyên mã cũ, không backfill.

## Điểm chạm
- **BE:** `QuotationService::saveDirectProduct` (insert→update HHBG+id, bỏ block HH-NNNNN cũ); `BomListService::syncProducts` (cha+con insert→update HHB+id); `BomListService::validateProductCodes` (nới, bỏ bắt buộc code hàng tạm).
- **FE:** `QuotationProductSearchModal.vue` (bỏ trường Mã — dùng chung Báo giá+BOM); `quotations/_id/edit.vue` (code rỗng + xoá `nextGoodsCode()`); `BomBuilderEditor.vue` (code rỗng + xoá `getNextGoodsCode()` + nới validate + sửa `dedupeTempGoodsCodes` clear code khi trùng).

## Không làm
delete-recreate BOM · FE gửi id · backfill · unique DB · migration/permission.

Spec chi tiết: `docs/superpowers/specs/2026-07-22-ma-hang-tam-backend-design.md`
