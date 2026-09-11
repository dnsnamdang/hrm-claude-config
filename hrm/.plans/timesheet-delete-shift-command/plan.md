# Plan — Command xoá ca `timesheet:delete-shift`

## BE
- [x] Tạo `worktrees/tpe-api/app/Console/Commands/Timesheet/DeleteShift.php` (nhánh **tpe**) — signature `timesheet:delete-shift {--company=} {--employee=} {--date=} {--from=} {--to=} {--force}`; mặc định dry-run, xoá theo đúng logic `ShiftDetailEmployeeDateController::destroy()` (shift_detail_employee_dates + timesheet_summaries + timesheet_details)
- [x] Chạy xử lý CN Vinh (company_id = 3) ngày 31/08 trên DB local `hrm_prod_6_6`: xoá 16 ca / 15 bảng công tổng hợp / 15 chi tiết
- [ ] Chạy lệnh tương tự trên server production (chưa làm — cần user thực hiện)

### Checkpoint — 2026-09-04
Vừa hoàn thành: command + xử lý CN Vinh 31/08 trên DB local.
Đang làm dở: không.
Bước tiếp theo: chạy `php artisan timesheet:delete-shift --company=3 --date=2026-08-31 --force` trên server thật.
Blocked: không có quyền truy cập server production từ session này.

## Phase 2 — dọn cả khi ca đã bị xoá trước đó
- [x] Quét `timesheet_summaries`/`timesheet_details` độc lập với `shift_detail_employee_dates` (ca đã xoá mà bảng công còn sót vẫn dọn được)
- [x] Cảnh báo `overtime_details` mồ côi + tuỳ chọn `--with-overtime`
- [x] Test local 2 kịch bản: còn đủ ca (16 ca/15 bảng công) và chỉ còn bảng công (0 ca/15 bảng công)
- [x] Push nhánh `tpe`: 1967ea349 (bản đầu) → 6e1bb11f9 (bản quét đủ bảng)
