# Design: sumDate tính theo ca làm việc thay vì weekend

## Bối cảnh

`sumDate()` trong `AttendanceTrait` hiện tính ngày công nghỉ dựa vào weekend/holiday. Yêu cầu: tính dựa trên NV có ca làm việc hay không (query `shift_detail_employee_dates`). Ngày không có ca = 0 công.

## Thay đổi

### AttendanceTrait.php — `sumDate()`
- Bỏ logic `isWeekend`, `congWeekend`. Bỏ param `$has_working_shift`
- Batch query `ShiftDetailEmployeeDate` 1 lần cho khoảng ngày
- Loop: ngày không có ca → skip (+0). Ngày có ca → check holiday → check giờ (≤6h = 0.5, >6h = 1)
- `$employee_info` nếu null → fallback `auth()->user()->info`

### TimesheetSummaryService.php (caller #2)
- Bỏ param `!!$workshift` khi gọi `sumDate`

### AttendanceController.php (caller #3)
- Truyền thêm employee_info từ request hoặc auth user

## Không thay đổi
- `getNumberOfDaysOffByList` (caller #1) — giữ nguyên
- Bảng `shift_detail_employee_dates`, model, logic phân ca
