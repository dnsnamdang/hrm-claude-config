# Fix tính công thai sản ngày lễ + cắt phép

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sửa 3 bug liên quan đến nhân sự nữ nghỉ thai sản: (1) tính nhầm công hưởng lương ngày lễ/tết, (2) trừ phép oan khi công ty cài nghỉ bù/cắt phép, (3) chưa tích lũy phép hàng tháng khi cắt phép.

**Architecture:** Tất cả thay đổi nằm trong một file duy nhất — `TimesheetSummaryService.php` — hàm `calcTimesheetEmployee`. Không cần tạo file mới hay thay đổi schema. Thêm biến `$isHolidayOriginal` để lưu trạng thái ngày lễ trước khi vòng lặp attendance làm thay đổi `$isHoliday[0]`.

**Tech Stack:** PHP 7.4, Laravel 8, Eloquent ORM

---

## File thay đổi

| File | Hành động |
|------|-----------|
| `Modules/Timesheet/Services/TimesheetSummaryService.php` | Modify — 4 điểm trong hàm `calcTimesheetEmployee` |

---

### Task 1: Lưu `$isHolidayOriginal` trước vòng lặp attendance

**Vấn đề:** Tại dòng 181, khi phát hiện đơn thai sản, code đặt `$isHoliday[0] = false`. Điều này khiến mất thông tin "ngày này ban đầu có phải ngày lễ không" ở các bước sau.

**Files:**
- Modify: `Modules/Timesheet/Services/TimesheetSummaryService.php` (trước dòng 148)

- [ ] **Bước 1: Thêm `$isHolidayOriginal` trước vòng lặp attendance**

Tìm đoạn code (dòng ~145–148):
```php
          $subDay = 0;
          $nghi_co_ly_do = 0;
          $data_attendance = [];
          foreach($attendances as $attendance) {
```

Sửa thành:
```php
          $subDay = 0;
          $nghi_co_ly_do = 0;
          $data_attendance = [];
          $isHolidayOriginal = $isHoliday[0]; // lưu trước khi vòng lặp thai sản đặt lại
          foreach($attendances as $attendance) {
```

- [ ] **Bước 2: Kiểm tra thủ công**

Mở file, đảm bảo dòng `$isHolidayOriginal = $isHoliday[0];` nằm ngay trước `foreach($attendances as $attendance)` và sau `$data_attendance = [];`.

---

### Task 2: Reset công về 0 cho nhân sự thai sản ngày lễ (branch có timesheet_details)

**Vấn đề:** Sau dòng 667 (`$labour_day = $labour_day + $subDay`), nhân sự thai sản trên ngày lễ vẫn có `$labour_day > 0` do `$subDay` tích lũy từ đơn thai sản. Và `$nghi_khong_ly_do` sau đó bị tính sai.

**Files:**
- Modify: `Modules/Timesheet/Services/TimesheetSummaryService.php` (sau dòng 775)

- [ ] **Bước 1: Thêm reset sau khi tính `$nghi_khong_ly_do`**

Tìm đoạn (dòng ~773–782):
```php
          if($labour_day < $punishment_day) $punishment_day = $labour_day;
          $nghi_khong_ly_do = $workshift->labour_day - $labour_day - $nghi_co_ly_do;
          $nghi_khong_ly_do = $nghi_khong_ly_do < 0 ? 0 : $nghi_khong_ly_do;
          if ($nghi_khong_luong) {
```

Thêm block mới ngay SAU dòng `$nghi_khong_ly_do = $nghi_khong_ly_do < 0 ? 0 : $nghi_khong_ly_do;`:
```php
          if($labour_day < $punishment_day) $punishment_day = $labour_day;
          $nghi_khong_ly_do = $workshift->labour_day - $labour_day - $nghi_co_ly_do;
          $nghi_khong_ly_do = $nghi_khong_ly_do < 0 ? 0 : $nghi_khong_ly_do;
          // Thai sản + ngày lễ: không tính công hưởng lương, hiển thị 0 (TS)
          if ($nghi_thai_san > 0 && $isHolidayOriginal) {
            $labour_day = 0;
            $labour_hour = 0;
            $nghi_khong_ly_do = 0;
            $punishment_day = 0;
          }
          if ($nghi_khong_luong) {
```

- [ ] **Bước 2: Kiểm tra thủ công**

Đảm bảo block `if ($nghi_thai_san > 0 && $isHolidayOriginal)` nằm giữa `$nghi_khong_ly_do = $nghi_khong_ly_do < 0 ? 0 : $nghi_khong_ly_do;` và `if ($nghi_khong_luong) {`.

---

### Task 3: Sửa TruncatedLeave (cắt phép) cho nhân sự thai sản

**Vấn đề:** Block TruncatedLeave (dòng 784–835) áp lên tất cả nhân viên không nằm trong exception list. Nhân sự thai sản bị trừ phép oan. Nhưng họ vẫn cần được tích lũy phép hàng tháng (cộng vào `addition_leave`).

**Files:**
- Modify: `Modules/Timesheet/Services/TimesheetSummaryService.php` (dòng 787–834)

- [ ] **Bước 1: Thay thế nội dung bên trong `if(!in_array(...))`**

Tìm đoạn (dòng ~787–835):
```php
            if(!in_array($employeeInfo->id, $excepted_ids)) {

              $now = Carbon::parse($date);
              $startDayYear = $now->startOfYear()->format('Y-m-d');
              $totalLeaveDay = $this->attendanceService->getNumberOfDaysOffEmployeeByYearAndEndDate(
                $employeeInfo->id,
                $now->year,
                $date);
              $employeeAttendance = EmployeeAttendanceService::findByEmployeeidAndYearNew($employeeInfo->id,$now->year);
              $totalLeaveDay = $totalLeaveDay +$employeeAttendance->number_day_leave_outside;
              $usable_leave_days = $employeeAttendance->usable_leave_days + ($employeeAttendance->addition_leave ?? 0);
              //TODO: reset
              $truncated_day = $truncatedLeave->day;

              if($employeeInfo->vacation_start_date && $employeeInfo->vacation_start_date > $date) {
                $truncated_day = 0;
              }

              $old_truncated_day = TimesheetSummary::where('day', '>=', $startDayYear)
                                                      ->where('day', '<', $date)
                                                      ->where('employee_info_id', $employeeInfo->id)
                                                      ->where('is_truncated_day', 1)
                                                      ->sum('work_day_phep');
              if($truncated_day <= $usable_leave_days - $totalLeaveDay) {
                $employeeAttendance->truncated_day = $old_truncated_day + $truncated_day;
                $employeeAttendance->save();
                $timesheetSummary->is_truncated_day = 1;
                $labour_day = $truncated_day;
                $labour_hour = $labour_day*8;
                $nghi_phep = $labour_day;
                $nghi_khong_ly_do = 0;
                $nghi_khong_luong = $workshift->labour_day - $labour_day;
                $nghi_khac = 0;
                $nghi_che_do = 0;
              } else {
                $truncated_day = $usable_leave_days - $totalLeaveDay > 0 ? $usable_leave_days - $totalLeaveDay : 0;
                $employeeAttendance->truncated_day = $old_truncated_day + $truncated_day;
                $employeeAttendance->save();
                $timesheetSummary->is_truncated_day = 1;
                $labour_day = $truncated_day;
                $labour_hour = $labour_day*8;
                $nghi_phep = $labour_day;
                $nghi_khong_ly_do = 0;
                $nghi_khong_luong = $workshift->labour_day - $labour_day;
                $nghi_khac = 0;
                $nghi_che_do = 0;
              }
            }
```

Thay thành:
```php
            if(!in_array($employeeInfo->id, $excepted_ids)) {

              $now = Carbon::parse($date);
              $startDayYear = $now->startOfYear()->format('Y-m-d');
              $employeeAttendance = EmployeeAttendanceService::findByEmployeeidAndYearNew($employeeInfo->id, $now->year);
              $truncated_day = $truncatedLeave->day;

              if($employeeInfo->vacation_start_date && $employeeInfo->vacation_start_date > $date) {
                $truncated_day = 0;
              }

              if ($nghi_thai_san > 0) {
                // Thai sản: không trừ phép, nhưng tích lũy phép hàng tháng vào addition_leave
                if ($truncated_day > 0) {
                  $employeeAttendance->addition_leave = ($employeeAttendance->addition_leave ?? 0) + $truncated_day;
                  $employeeAttendance->save();
                }
              } else {
                $totalLeaveDay = $this->attendanceService->getNumberOfDaysOffEmployeeByYearAndEndDate(
                  $employeeInfo->id,
                  $now->year,
                  $date);
                $totalLeaveDay = $totalLeaveDay + $employeeAttendance->number_day_leave_outside;
                $usable_leave_days = $employeeAttendance->usable_leave_days + ($employeeAttendance->addition_leave ?? 0);

                $old_truncated_day = TimesheetSummary::where('day', '>=', $startDayYear)
                                                        ->where('day', '<', $date)
                                                        ->where('employee_info_id', $employeeInfo->id)
                                                        ->where('is_truncated_day', 1)
                                                        ->sum('work_day_phep');
                if($truncated_day <= $usable_leave_days - $totalLeaveDay) {
                  $employeeAttendance->truncated_day = $old_truncated_day + $truncated_day;
                  $employeeAttendance->save();
                  $timesheetSummary->is_truncated_day = 1;
                  $labour_day = $truncated_day;
                  $labour_hour = $labour_day*8;
                  $nghi_phep = $labour_day;
                  $nghi_khong_ly_do = 0;
                  $nghi_khong_luong = $workshift->labour_day - $labour_day;
                  $nghi_khac = 0;
                  $nghi_che_do = 0;
                } else {
                  $truncated_day = $usable_leave_days - $totalLeaveDay > 0 ? $usable_leave_days - $totalLeaveDay : 0;
                  $employeeAttendance->truncated_day = $old_truncated_day + $truncated_day;
                  $employeeAttendance->save();
                  $timesheetSummary->is_truncated_day = 1;
                  $labour_day = $truncated_day;
                  $labour_hour = $labour_day*8;
                  $nghi_phep = $labour_day;
                  $nghi_khong_ly_do = 0;
                  $nghi_khong_luong = $workshift->labour_day - $labour_day;
                  $nghi_khac = 0;
                  $nghi_che_do = 0;
                }
              }
            }
```

- [ ] **Bước 2: Kiểm tra thủ công**

Đảm bảo block `if ($nghi_thai_san > 0)` nằm sau khi tính `$truncated_day` và `$employeeAttendance`, và nhánh `else` chứa toàn bộ logic cũ không thay đổi.

---

### Task 4: Sửa branch không có timesheet_details + ngày lễ

**Vấn đề:** Ở branch else (nhân sự không có timesheet_detail = không chấm công), dòng 1261 vẫn gán `labour_day=1, labour_hour=8` cho ngày lễ, kể cả khi nhân sự đang nghỉ thai sản.

**Files:**
- Modify: `Modules/Timesheet/Services/TimesheetSummaryService.php` (dòng 1261–1271)

- [ ] **Bước 1: Thêm kiểm tra thai sản trước khi gán công ngày lễ**

Tìm đoạn (dòng ~1261–1271):
```php
          if($isHoliday[0]) {
            $timesheetSummary = TimesheetSummary::where('employee_info_id', $employeeInfo->id)
                                                ->where('day', $date)->first();
            if(!$timesheetSummary) {
              $timesheetSummary = new TimesheetSummary();
            }
            $timesheetSummary->employee_info_id = $employeeInfo->id;
            $timesheetSummary->labour_hour = 8;
            $timesheetSummary->labour_day = 1;
            $timesheetSummary->save();
          }
```

Thay thành:
```php
          if($isHoliday[0]) {
            $isOnMaternityleave = Attendance::whereHas('leave_type', function ($q) {
                $q->where('group_id', LeaveType::NGHI_THAI_SAN);
            })
            ->where('employee_id', $employeeInfo->id)
            ->where('attendance_status', AttendanceStatus::Approved)
            ->where('attendance_start_at', '<=', $date . ' 23:59:59')
            ->where('attendance_end_at', '>=', $date . ' 00:00:01')
            ->exists();

            if (!$isOnMaternityleave) {
              $timesheetSummary = TimesheetSummary::where('employee_info_id', $employeeInfo->id)
                                                  ->where('day', $date)->first();
              if(!$timesheetSummary) {
                $timesheetSummary = new TimesheetSummary();
              }
              $timesheetSummary->employee_info_id = $employeeInfo->id;
              $timesheetSummary->labour_hour = 8;
              $timesheetSummary->labour_day = 1;
              $timesheetSummary->save();
            }
          }
```

- [ ] **Bước 2: Kiểm tra thủ công**

Đảm bảo `Attendance` và `LeaveType` đã được import (đã có ở đầu file dòng 15 và 44). `AttendanceStatus` đã import dòng 16.

---

### Task 5: Test thủ công trên môi trường dev

Không có unit test tự động cho service này. Test thủ công theo kịch bản:

- [ ] **Kịch bản A: Thai sản + ngày lễ (có timesheet_detail)**

  1. Chọn 1 nhân viên đang có đơn nghỉ thai sản duyệt (Attendance với leave_type group_id=1).
  2. Chọn ngày trong kỳ thai sản đó mà công ty đã cài ngày lễ (Holiday).
  3. Nhân viên có timesheet_detail cho ngày đó (có ca được gán, dù không chấm công).
  4. Chạy tính công: gọi `calcTimesheetEmployee($employeeInfo, $date)` hoặc trigger qua màn hình.
  5. Kết quả mong đợi: `timesheetSummary->labour_day = 0`, `work_day_thai_san > 0`, `work_day_khong_ly_do = 0`.

- [ ] **Kịch bản B: Thai sản + ngày lễ (không có timesheet_detail)**

  1. Chọn nhân viên thai sản, ngày có Holiday, nhưng **không có ca được gán** (không có timesheet_detail).
  2. Chạy tính công.
  3. Kết quả mong đợi: không tạo TimesheetSummary mới với labour_day=1 cho ngày đó.

- [ ] **Kịch bản C: Thai sản + TruncatedLeave (cắt phép)**

  1. Chọn nhân viên thai sản, ngày có TruncatedLeave.
  2. Nhân viên không nằm trong danh sách exception.
  3. Chạy tính công.
  4. Kết quả mong đợi:
     - `timesheetSummary->work_day_phep = 0` (không trừ phép).
     - `timesheetSummary->is_truncated_day` không được set = 1.
     - `employeeAttendance->addition_leave` tăng thêm `truncatedLeave->day`.

- [ ] **Kịch bản D: Nhân viên KHÔNG thai sản + ngày lễ (regression)**

  1. Nhân viên bình thường (không có đơn thai sản), ngày lễ, có ca.
  2. Chạy tính công.
  3. Kết quả mong đợi: `labour_day = workshift->labour_day` (không đổi so với trước).

- [ ] **Kịch bản E: Nhân viên KHÔNG thai sản + TruncatedLeave (regression)**

  1. Nhân viên bình thường, ngày TruncatedLeave.
  2. Kết quả mong đợi: phép vẫn bị trừ bình thường (`work_day_phep = truncated_day`, `is_truncated_day=1`).

- [ ] **Bước cuối: Reload lại màn timesheet_details trên UI, xác nhận hiển thị đúng "0 (TS)" cho thai sản + ngày lễ.**
