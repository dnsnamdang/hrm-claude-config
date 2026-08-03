# Fix: Báo cáo luân chuyển hàng hóa — tồn kho bán được = 0 khi không chọn công ty

## Bug
Cột 'SL tồn kho bán được' không hiện khi KHÔNG chọn công ty (chọn công ty thì hiện). Mã test: JONN-AG010002SP (id 5047).

## Root cause (xác nhận bằng tinker, prod erp_new)
Nhánh không-chọn-công-ty dùng các method build*SubQuery, gộp tồn theo từng công ty bằng `->union()` (DISTINCT) rồi outer SUM.
Khi >=2 công ty có cùng giá trị (vd cty1=31, cty4=25+6=31 TRÙNG), `UNION` distinct gộp 2 dòng giống nhau thành 1 → SUM ra 31 thay vì 62.
Stock bị thiếu một nửa → trừ hold/prepick/xuất của CẢ 2 công ty → âm → CASE WHEN <0 THEN 0 (stock_can_sale) → hiển thị 0/trống.
Tinker: union=31, unionAll=62.

## Fix
Đổi `->union(` thành `->unionAll(` tại 4 method build*SubQuery (stock, KM, hold, export request) trong StockTransferReportService.php — vì đều SUM partial theo công ty.

## Tasks
- [x] Root cause: union vs unionAll (tinker prod, mã 5047)
- [x] Sửa 4 chỗ ->union( -> ->unionAll(
- [x] php -l
- [ ] User test: báo cáo luân chuyển, KHÔNG chọn công ty, mã JONN-AG010002SP -> cột SL tồn kho bán được hiện đúng (tổng 2 công ty)

### Checkpoint — 2026-06-30
Vừa hoàn thành: `StockTransferReportService.php` — đổi `->union(` → `->unionAll(` ở 4 method build*SubQuery (6265/6301/6337/6381). Root cause: UNION distinct gộp 2 cty cùng tồn (31=31) → SUM thiếu nửa → stock_can_sale âm → clamp 0. Verify tinker: union=31, unionAll=62. php -l sạch.
Đang làm dở: không.
Bước tiếp theo: USER test báo cáo luân chuyển (không chọn cty, mã JONN-AG010002SP → cột SL tồn kho bán được hiện đúng) → rồi commit.
Blocked:
