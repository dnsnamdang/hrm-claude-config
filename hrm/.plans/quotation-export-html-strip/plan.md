# Xuất Excel báo giá — cột "Thông số kỹ thuật" hiện thẻ HTML

- [x] Thêm helper chung `htmlToText()` (`app/Helper/FormatHelper.php`) — HTML rich-text → text thuần giữ ngắt dòng
- [x] `QuotationExcelExport::normalize()` hạ HTML của `attributes` + `note` về text thuần
- [x] Blade `exports/assign/quotation_excel.blade.php` dùng `nl2br(e(...))` để Excel xuống dòng trong ô
- [x] Cột "Thông số kỹ thuật": tắt autosize, width 45 + wrap text, canh trên
- [x] Blade BOM `bom_list_import_format.blade.php` dùng lại helper chung (bỏ closure trùng logic)
- [x] Verify: xuất thật báo giá 289, đọc lại file — text thuần, đúng dòng, công thức các cột khác không đổi

## Rà toàn luồng (đợt 2)

- [x] `exports/bom_list.blade.php` (Excel BÁO GIÁ gửi khách + BOM): đang in HTML thô, `</div>` không xuống dòng → các dòng dính liền. Sửa sang `nl2br(e(htmlToText(...)))`, bỏ closure trùng logic
- [x] `exports/product_projects.blade.php` (Hàng hoá dự án): `strip_tags` trơ nuốt hết ngắt dòng → sửa sang helper chung
- [x] `htmlToText()`: bỏ qua chuỗi không có thẻ HTML (giữ nguyên "< 16Mpa", "a > b", "&") — cùng quy tắc với FE `utils/specHtml.js`
- [x] `QuotationImportService::assertMatchesBom()`: hạ HTML CẢ 2 PHÍA cho cột TSKT — nếu không, round-trip export→import báo "không khớp với BOM gốc" và chặn cả file
- [x] Màn IN (FE `QuotationPrintPreview`, `SummaryQuotationForm`) dùng `$specHtml` → đã đúng, không sửa
- [x] Verify: xuất thật 2 file của báo giá 289 (`export-quotation-data` + `export-excel` gửi khách) đọc lại bằng PhpSpreadsheet; test `assertMatchesBom` 3 case (file bản mới / file bản cũ còn HTML / user sửa tay)
- [x] Note quy tắc vào `.claude/skills/export-excel/SKILL.md` mục 1b + bảng lỗi + checklist + file tham chiếu; `.claude/skills/print-page/SKILL.md` mục 2 (bản in giữ HTML)
