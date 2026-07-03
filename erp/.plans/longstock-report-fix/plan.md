# Fix lỗi 500 Báo cáo hàng tồn lâu (longStockReport)

## Bối cảnh
- URL: `/admin/warehouse/warehouse_reports/longStockReport` — vừa vào đã báo "Đã có lỗi xảy ra".
- Trang load xong tự gọi AJAX `longStockReportSearchData` → endpoint trả 500.

## Nguyên nhân gốc
- `Product::longStockReportSearchData()` / `longStockReportSummary()` build SQL có:
  `CASE WHEN wil.type = 1 THEN pid.import_price ELSE bs.import_price END`
  với join `beginning_stocks as bs`.
- Cột `beginning_stocks.import_price` đã bị **DROP** bởi migration
  `2023_04_04_135705_update_qty_stock.php` (drop `total_price`, `import_price`).
- MySQL parse cột không tồn tại → `SQLSTATE[42S22] Unknown column 'bs.import_price'` → 500.
- Thực tế lô tồn đầu kỳ (type=2) bị loại khỏi report do `DATEDIFF(NOW(), wi.received_time) > long_stock_days`
  (lô đầu kỳ không có `warehouse_imports` cha → `received_time` NULL → loại). Nhánh `ELSE` không bao giờ dùng.

## Tasks
- [x] Tái hiện lỗi qua tinker (login giả employee, chạy searchData/summary) → xác nhận lỗi cột `bs.import_price`
- [x] Truy migration làm mất cột → `2023_04_04_135705_update_qty_stock.php`
- [x] Xác minh type=2 bị filter loại, `pid.import_price` cho kết quả total_value không đổi (14,747,818,045.2250)
- [x] Sửa `app/Product.php::longStockReportSearchData` — bỏ CASE/join chết, dùng `pid.import_price`
- [x] Sửa `app/Product.php::longStockReportSummary` — tương tự
- [x] Verify lại bằng tinker: searchData paginate + summary chạy OK, số liệu khớp
- [ ] (Tùy chọn) Dọn bản trùng chết ở `app/ProductTemplate.php`, `app/ProductInfo.php` (không route nào gọi)

## Lưu ý
- Chỉ `Product.php` được `WarehouseReportsController` dùng. ProductTemplate/ProductInfo có copy y hệt nhưng không được gọi.

### Checkpoint — 2026-06-18
Vừa hoàn thành: Sửa `app/Product.php` (longStockReportSearchData + longStockReportSummary), bỏ join `beginning_stocks as bs` + dùng `pid.import_price`. Verify tinker: searchData=1407 dòng, summary total_value=14,747,818,045.2250 (không đổi).
Đang làm dở: không
Bước tiếp theo: User reload trang xác nhận hết lỗi. Tùy chọn dọn bản trùng ở ProductTemplate.php/ProductInfo.php.
Blocked:
