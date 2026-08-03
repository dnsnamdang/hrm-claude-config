# Plan — Tìm kiếm hàng hoá ERP theo Model (Redmine #10863)

@manhcuong · 2026-07-30

## Bối cảnh
Issue #10863 ở trạng thái **Phản hồi**: QA báo "model có kí tự đặc biệt đang k search được".

Tái hiện trên dev (`assign/quotations/erp-product-search`, hàng `BT3D-144511445000114402014400:01`):
`1445` → 5 kq · `1445/1` → 5 kq · `'1445/1` → 4 kq · `1440/2` → 5 kq · `(14450001)` → 4 kq ·
**`&#039;1445/1` → 0 kq**.

⇒ Search KHÔNG hỏng. Hỏng ở **hiển thị**: ERP lưu chuỗi đã HTML-escape (`&#039;` = `'`),
HRM in thẳng ra popup nên QA copy đúng chuỗi đang thấy → ERP escape thêm lần nữa → không khớp.

## Task
- [x] Helper chung `erpText()` trong `app/Helper/FormatHelper.php`: `html_entity_decode(ENT_QUOTES|ENT_HTML5)` rồi `ltrim("'")` (gộp luôn hành vi stripLeadingQuote cũ); non-string trả nguyên
- [x] `ErpProductSearchService::stripLeadingQuote()` → gọi `erpText()` (popup Thêm hàng hoá: name/code/model/brand/origin/unit/cate/manufacture)
- [x] `BomListController`: 2 closure `$stripLeadingQuote` → `erpText()`; thêm `erpText()` cho block map ở ~dòng 557 (code/name/model/brand/origin)
- [x] `BomListService::stripLeadingQuote()` → `erpText()` (chuẩn hoá lúc GHI tên/mã ERP vào bom_list_products)
- [x] `QuotationImportService::stripLeadingQuote()` → `erpText()`
- [x] `DetailQuotationResource`: `erpText()` cho code/name + model/brand/origin/unit của cả nhánh qpp và blp (chi tiết báo giá + bản in + preview)
- [x] `DetailBomListResource`: `erpText()` cho name/code + 4 tên danh mục (chi tiết BOM)
- [x] `ProductProjectController`: `erpText()` ở 3 block map (hàng hoá dự án + picker "Dùng lại hàng tạm dự án")
- [x] `QuotationExcelExport::catalog()`: map `erpText()` cho model/brand/origin/unit → file Excel xuất ra sạch

## Verify
- [x] `php -l` sạch 7 file
- [x] Unit helper: `&#039;1445/1 (14450001) 1440/2 (014400020)` → `1445/1 (14450001) 1440/2 (014400020)`; `'ABC-123` → `ABC-123`; `&amp;M&#039;s` → `&M's`; null/int giữ nguyên
- [x] Không regression: `GET /assign/quotations/116` local vẫn 200, 8 hàng, 0 chuỗi escaped
- [ ] Cần verify trên dev sau khi deploy: popup Thêm hàng hoá hiện `1445/1 (14450001)…`, copy chuỗi đó search ra kết quả

## Checkpoint — 2026-07-30
Vừa hoàn thành: fix toàn bộ điểm hiển thị/ghi chuỗi ERP trong module Assign.
Bước tiếp theo: deploy dev → QA test lại #10863 → chuyển trạng thái issue.
Blocked: không. Chưa commit (theo quy tắc).
