# Fix: chặn "Từ ngày" > "Đến ngày" — báo cáo Công nợ chi tiết KH

## URL / Bối cảnh
- `admin/sale/reports/customer-debt-details` (SaleReportsController@customerDebtDetailsData + exportCustomerDebtDetails).
- Bug: nhập Từ ngày > Đến ngày (vd 20/07 → 13/07) vẫn ra kết quả, không chặn.
- Param: `startDate`/`endDate` (directive date-form lưu model Y-m-d → so sánh chuỗi hợp lệ).

## Fix
- [x] BE: helper `validateReportDateRange()` throw ValidationException (errors.endDate) khi endDate < startDate; gọi ở customerDebtDetailsData + exportCustomerDebtDetails.
- [x] FE: chặn inline trong getCustomerDebtDetailsData — set $scope.errors.endDate + toastr, return (span `<% errors.endDate %>` đã có sẵn).
- [x] php -l sạch, blade compile OK.
- [ ] User reload test: nhập ngược ngày → báo lỗi "Đến ngày phải lớn hơn hoặc bằng Từ ngày", không query.

## Không làm: không đụng logic query/getReportData.
