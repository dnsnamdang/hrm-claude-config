# Công định mức riêng từng nhân viên

## Mục tiêu

Thay đổi công định mức từ 1 giá trị chung cho toàn bảng chấm công tổng hợp thành giá trị riêng cho từng nhân viên, dựa vào phân ca chi tiết của từng người.

## Scope

- Module: Timesheet
- Màn ảnh hưởng: Chi tiết bảng chấm công tổng hợp (`timesheet_summaries/_id`)
- API: `timesheet_month_summaries/show`

## Quyết định thiết kế

| Quyết định | Lựa chọn |
|---|---|
| Hiển thị | Cột "Công ĐM" mỗi dòng NV có giá trị riêng |
| Lưu trữ | Lưu vào DB khi tạo/tổng hợp bảng |
| Logic tính | Giữ nguyên `AttendanceWatchRegulation::standard()` |
| Cột cũ `timesheet_month_summaries.standard` | Giữ nguyên, không hiển thị |

## Database

### Migration: thêm cột vào `timesheet_month_summary_details`

```sql
ALTER TABLE timesheet_month_summary_details
ADD COLUMN standard DECIMAL(8,2) NULL COMMENT 'Công định mức riêng từng NV, tính theo phân ca chi tiết';
```

## Backend

### Tính toán khi tổng hợp

File: `Modules/Timesheet/Services/TimesheetMonthSummaryService.php`

Trong flow tạo/tổng hợp bảng chấm công, khi loop từng NV để tạo record `timesheet_month_summary_details`:

```php
$standard = AttendanceWatchRegulation::standard($start_date, $end_date, $company, $employeeInfo);
```

Lưu `$standard` vào field `standard` của record detail.

### API show

Response hiện tại đã trả toàn bộ fields từ `timesheet_month_summary_details`. Field `standard` mới sẽ tự động có trong response mà không cần sửa thêm query/resource.

## Frontend

### Màn chi tiết bảng chấm công tổng hợp

File: `pages/timesheet/timesheet_summaries/_id/index.vue`

Thay đổi dòng hiển thị công định mức:
- Trước: `formatNumber(summary.standard)` — giá trị chung
- Sau: `formatNumber(employee.standard)` — giá trị riêng từng NV

## Không thay đổi

- Hàm `AttendanceWatchRegulation::standard()` — giữ nguyên toàn bộ logic
- Cột `timesheet_month_summaries.standard` — giữ trong DB, không xoá
- Các màn khác sử dụng `standard` chung (dashboard, export...) — không ảnh hưởng

## Edge cases

- NV không có phân ca (`shift_detail_employee_dates` trống): hàm `standard()` fallback về tính theo cấu hình cuối tuần chung → vẫn trả ra giá trị hợp lệ
- NV vào/nghỉ giữa kỳ: hàm `standard()` đã xử lý case này (dòng 56-76)
- Bảng chấm công đã tạo trước khi deploy: cột `standard` sẽ NULL → frontend cần fallback về `summary.standard` nếu `employee.standard` là null
