# Command xoá dữ liệu chấm công theo nhân sự + ngày

**Người phụ trách:** @namdangit

## Mục tiêu

Command artisan xoá dữ liệu chấm công (`timesheet_summaries` + `timesheet_details`) của 1 nhân sự trong 1 khoảng ngày — dùng khi cần xoá để chạy lại tính công.

## Quyết định chính

- **Signature:** `php artisan delete:employee_timesheet {employee_info_id} {from_date} {to_date?} {--force}`
  - `to_date` bỏ trống = xoá đúng 1 ngày (`from_date`)
  - Ngày format `Y-m-d`, khớp cột `timesheet_summaries.day`
- **CHỈ xoá 2 bảng** `timesheet_details` + `timesheet_summaries` (user chốt lại 2026-07-02, ban đầu định xoá kèm 3 bảng con `timesheet_detail_assigns`/`timesheet_detail_job_assignments`/`overtime_details` — đã bỏ)
- **An toàn:** in số bản ghi từng bảng + `$this->confirm()` trước khi xoá; `--force` bỏ qua xác nhận. Xoá trong `DB::transaction`.
- **Vị trí file:** `hrm-api/app/Console/Commands/DeleteEmployeeTimesheet.php` (cùng chỗ các command timesheet khác như `CalcEmployeeTimesheet.php`; `Modules/Timesheet/Console/` trống, không dùng)

## Luồng xử lý

1. Validate: employee tồn tại (`EmployeeInfo`), ngày đúng format, `from_date <= to_date`
2. Lấy `summary_ids` từ `TimesheetSummary` (employee + whereBetween day) → `detail_ids` từ `TimesheetDetail`
3. Đếm + hiện bảng số lượng → confirm (trừ khi `--force`)
4. Xoá theo thứ tự: details → summaries
5. In số bản ghi đã xoá mỗi bảng
