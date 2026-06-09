# Plan — delete-timesheet-command

**Người phụ trách:** @namdangit

## Phase 1: Command xoá timesheet

### BE

- [x] Tạo `app/Console/Commands/DeleteEmployeeTimesheet.php` — signature `delete:employee_timesheet {employee_info_id} {from_date} {to_date?} {--force}`
- [x] Validate employee + ngày, đếm bản ghi 5 bảng, confirm, xoá trong transaction theo thứ tự con → cha
- [x] Verify: php -l + chạy thử với employee/ngày không có dữ liệu + có dữ liệu (abort ở confirm)
- [x] Verify xoá thật: tạo data giả (summary+detail+detail_assign ngày 2020-05-05, NV 1590) → `--force` xoá sạch 3 bảng, 46 summary ngày khác của NV còn nguyên
- [x] (Yêu cầu bổ sung) Thu hẹp: CHỈ xoá 2 bảng timesheet_details + timesheet_summaries, bỏ 3 bảng con — verify lại xoá thật với --force

### Checkpoint — 2026-07-02
Vừa hoàn thành: Command delete:employee_timesheet — code + verify đầy đủ; đã thu hẹp về chỉ 2 bảng theo yêu cầu user
Đang làm dở: (không)
Bước tiếp theo: (không — feature xong)
Blocked: (không)
