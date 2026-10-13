# Fix: công đi đường lấy từ ĐỀ NGHỊ THANH TOÁN (payment_business_requests)

**Nhánh:** tpe. Ngày: 2026-08-01.

## Bối cảnh
Bảng chấm công chi tiết hiển thị `cong_di_duong` = `timesheet_summaries.work_day_timekeeper_to_go`, ghi bởi job `CreateTimesheetSummary`. Nguồn CŨ: `PaymentProfileEmployee.road_travel_allowance_approve` (hồ sơ thanh toán). User muốn lấy từ **đề nghị thanh toán** `payment_business_requests` (đã duyệt), bỏ hồ sơ thanh toán.

## Cấu trúc payment_business
`PaymentBusinessRequest (status, approved_time)` → `PaymentBusinessRequestEmployee (payment_business_request_id, employee_id)` → `PaymentBusinessRequestEmployeeDetail (road_travel_allowance_approve)`.

## Tasks
- [x] `CreateTimesheetSummary.php`: đổi nguồn `road_travel_allowance_approve` (dòng 118, dùng cho lương) + `cong_di_duong` (dòng 131, hiển thị) từ PaymentProfile → PaymentBusinessRequest (đã duyệt approved_time trong kỳ, sum EmployeeDetail.road_travel_allowance_approve). GIỮ `work_arrears` (dòng 128) từ hồ sơ thanh toán.
- [x] Thêm import PaymentBusinessRequest + PaymentBusinessRequestEmployeeDetail. php -l sạch.
- [ ] User: TÍNH LẠI bảng công tháng liên quan để áp (bảng chi tiết đọc số đã tính sẵn, không realtime).

## Lưu ý
Job build sẵn (không realtime) → phải regenerate timesheet month summary mới thấy số mới.

## Task 2 (2026-08-01) — Fix TẦNG HIỂN THỊ getDataTimesheet (live)
- [x] `TimesheetSummaryService::getDataTimesheet` (phục vụ FE bảng chi tiết qua index): tính `cong_di_duong` LIVE từ payment_business_requests đã duyệt trong kỳ (không đọc work_day_timekeeper_to_go nữa) → hiện ngay không cần tính lại.
- [x] Giữ CreateTimesheetSummary (lương) như đã chốt (a).
