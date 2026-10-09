# Fix: Báo cáo hàng có thể bán theo công ty — ẩn nhầm cột kho

## Bug
Tổng "đang xuất hàng bán" (6) ≠ cột kho hiển thị (LN=5). Kho SG (đang-xuất=1) không hiện cột → lệch.

## Root cause (copy-paste)
`WarehouseReportCompaniesProductSummary::getTotalSumStock` (điều kiện ẩn/hiện cột) — 3 biến gán nhầm:
dòng 70/74/78 gọi `getSumStockKmQty` thay vì `getSumStockHoldQty`/`getSumStockSaleQty`/`getSumStockWerKmQty`.
→ chỉ tính tồn+KM tồn, bỏ qua hàng gửi + đang xuất → kho tồn=0 nhưng có đang-xuất (SG, liên kho cross-company) bị ẩn cột. Tổng server-side vẫn đúng nên tồn tại lâu không ai thấy.

## Fix
Sửa 3 lời gọi đúng tên hàm. Cột kho hiện khi có bất kỳ tồn/KM/gửi/đang-xuất.

## Tasks
- [x] Fix 3 dòng getTotalSumStock (blade compile OK)
- [x] Commit + push master

## ĐÍNH CHÍNH (2026-07-15) — bug thật là PREPICK, không phải ẩn cột SG
Chẩn đoán "ẩn cột SG" ban đầu SAI (breakdown quên lọc company → quy nhầm cho SG; thực ra SG thuộc cty 4, cty 1=0).
**Bug thật:** "Tổng đang xuất Hàng bán" = wer_total − wer_km_total, KHÔNG trừ prepick/hold; còn per-warehouse (wer_{acc}) đã trừ → lệch đúng số prepick (LN prepick=1 → Tổng 6 vs LN 5).
**Fix (commit bfb0e6f06a):** trừ prepick+hold ở 4 chỗ tính Tổng:
- FE getter `WarehouseReportCompaniesProduct.wer_sale_total`
- Controller `stockCompaniesSearchData` footer (dòng ~427)
- Controller `stockCompaniesExport` footer
- Export blade per-product (stock_companies_product_report dòng ~122, trước đó còn blank vì DB không có alias wer_sale_total)
User xác nhận: "Đang xuất Hàng bán" KHÔNG tính prepick.

## Ghi chú: fix getTotalSumStock (commit 2e04989b2c) là bug KHÁC (copy-paste ẩn cột kho tồn=0 có hàng gửi/đang-xuất) — vẫn hợp lệ, GIỮ lại, không liên quan vụ prepick.
