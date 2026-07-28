# Plan — Hàng hóa dự án: hàng tạm từ báo giá độc lập không render link BOM

Bug: màn Hàng hóa dự án (`/assign/product-project`) cột "Mã BOM" với hàng tạm từ báo giá độc lập hiển thị mã BG dạng LINK → click đi tới `/assign/bom-list/null` (gãy), gây hiểu nhầm "ghi nhận mã BOM list".

Chốt với user: **giữ hiển thị mã BG (truy nguồn) nhưng BỎ link BOM** khi `bom_list_id` null.

Truy vết: `bom_list_id` đã null sẵn (transformQuotationItem), không có ghi DB bom_list nào (FE-only). ERP sync không ghi bom_list.

Chốt LẠI với user (đổi ý): **Option 1 — Để trống "—" hoàn toàn** (bỏ cả mã BG khỏi cột Mã BOM).

## Phase 1 — BE + FE

### BE
- [x] `ProductProjectController::transformQuotationItem`: `bom_code => null` (thay vì `$quotation->code`); cập nhật comment

### FE
- [x] `product-project/index.vue` cell `bomCode`: chỉ render `<a @click=viewBom>` khi có `item.bom_list_id`; ngược lại render text thường → với bom_code null hiện "—" không link

## Verify
- [x] BE reflection: transformQuotationItem(qpp báo giá độc lập) → bom_code=NULL, bom_list_id=NULL (trước là BG-2026-00001)
- [x] API thật: product-projects?keyword=BZAI-DG-8S → row qtn_1 bom_code=None, bom_list_id=None
- [x] UI Playwright: cột "Mã BOM" hiện "—" không link (ảnh xác nhận); dòng BOM thật vẫn giữ link
- [x] Dữ liệu test đã revert (qpp1 erp_product_id=8310), xoá ảnh

### Checkpoint — 2026-07-09
Vừa hoàn thành: CODE DONE + VERIFIED (BE reflection + API + UI). php -l sạch.
Files: hrm-api ProductProjectController.php (bom_code=null cho dòng báo giá) + hrm-client product-project/index.vue (cell bomCode guard bom_list_id)
Đang làm dở: không
Bước tiếp theo: user verify browser với báo giá độc lập có hàng tạm đã duyệt thật
Blocked:
