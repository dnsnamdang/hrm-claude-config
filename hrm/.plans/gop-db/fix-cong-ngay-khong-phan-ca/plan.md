# Fix: Bảng công chi tiết hiện ngày không có phân ca — @manhcuong

Sửa/xoá phân ca chỉ gỡ `shift_detail_employee_dates`, dòng công tạo sẵn (`timesheet_summaries` + `timesheet_details`) vẫn nằm lại → cron tính theo ca cũ (VD Etek 17/10/2026: nghỉ không lý do).

## Phase 1
### BE
- [x] `ShiftDetailEmployeeDateService::pruneTimesheetsWithoutShift()` + gọi ở sửa bảng phân ca (từ ngày mai), xoá bảng phân ca, phân ca theo ngày, cron `create:timesheet_detail` — nhánh `fix/orphan-timesheet-summary` (từ gop_db)
- [x] Dọn prod `hrm_erp_gop`: xoá 399 dòng công cty 8 (17/10 + Thứ 7 chẵn tới 31/07/2027), backup `HRM/tools/backup_orphan_ts_20261019/`
- [x] Siết: cron chỉ gỡ ngày tương lai, chia lô xoá 1000 id
- [x] Test tích hợp 49 case qua route thật (3 loại tài khoản) + cron toàn bộ NV — 49/49 PASS, không có log lỗi
- [x] Commit + push lên `gop_db`, deploy prod (8b6147bfe, 19/10/2026)

## Phase 2 — Chặn tạo sẵn dòng công ngày tương lai
Nguyên nhân: 26/08/2026 chạy `create:many_timesheet_detail_by_employee --company_id=8 2026-08-22 2026-08-22` → tham số lệch vị trí, to_date = "-1" → Carbon năm 1969 → tạo công Etek tới 07/2027.
### BE (nhánh `fix/no-future-timesheet` từ gop_db)
- [x] Trait `Timesheet/ResolvesTimesheetDateRange`: thiếu to_date = from_date, sai định dạng / from > to / quá ngày mai → báo lỗi
- [x] `create:many_timesheet_detail_by_employee`: ngày rơi vào ô employee_info_id thì dời lại; id không phải số → lỗi
- [x] `create:many_timesheet_detail` dùng chung trait
- [x] `WorkShiftDetailService::createTimesheetDetail` (hàm dùng chung, user đồng ý): ngày > ngày mai → bỏ qua
- [x] Test rollback 19/19 PASS (test_future_ts.php)
- [x] Dọn prod: xoá 3.857 dòng công cty 8 day >= 21/10/2026, backup `HRM/tools/backup_future_ts_20261019/`
- [x] Commit + push gop_db (ecd3888e8, 19/10/2026) — chưa deploy prod

### Checkpoint — 2026-10-19
Vừa hoàn thành: code + test rollback trên local, dọn dữ liệu prod nhóm A+B
Đang làm dở: chưa commit (worktree `HRM/worktrees/orphan-ts-api`)
Bước tiếp theo: commit → push gop_db → deploy
Blocked: nhóm C (cty 1 ngày 28/09, cty 9 ngày 12/10 + 16/10 — có công nhưng mất ca) chờ HR quyết
