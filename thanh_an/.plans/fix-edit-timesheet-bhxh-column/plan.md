# Fix: Sửa bảng công crash — sai tên cột BHXH (@khoipv)

## Bối cảnh
- Lỗi: `SQLSTATE[42S22] Unknown column 'work_day_huong_bhxh' in 'field list'` khi Sửa bảng công (timesheet_month_summaries).
- Root cause: commit `5e402cd` "Fix excel bảng công" (05/05/2026) thêm 2 dòng vào `TimesheetMonthSummaryService::update()` ghi cột `work_day_huong_bhxh` / `work_day_huong_bhxh_tv` — KHÔNG tồn tại trên bảng `timesheet_month_summary_detail` (cột thật: `nghi_huong_bhxh` / `nghi_huong_bhxh_tv`, theo migration v2 + Job CreateTimesheetSummary).
- Phần đọc list (396/427) cũng sai tên cột → từ trước tới nay trả null/0 (bug ngầm, không crash).

## Phương án (đã chốt với user)
Chỉ sửa cho hết crash + hiển thị đúng; KHÔNG đụng công thức `total_khong_luong` (giữ nguyên hành vi số liệu).
Giữ nguyên tên field API `work_day_huong_bhxh` mà FE đang dùng, chỉ map đúng cột DB bên trong.

## Tasks
- [x] BE — `update()` 764-765: ghi `nghi_huong_bhxh` / `nghi_huong_bhxh_tv`
- [x] BE — list 396/427: đọc `nghi_huong_bhxh` / `nghi_huong_bhxh_tv`
- [x] `php -l` pass
- [ ] User test qua UI: Sửa 1 dòng bảng công → lưu thành công, cột BHXH hiển thị đúng

## Không làm (tách yêu cầu riêng nếu cần)
- Cộng BHXH vào `total_khong_luong` (dòng 350/353) — sẽ làm số liệu thay đổi, cần kiểm thử lương riêng.

### Checkpoint — 2026-06-02
Vừa hoàn thành: Sửa 4 vị trí trong TimesheetMonthSummaryService.php, lint pass.
Đang làm dở: (không)
Bước tiếp theo: User test Sửa bảng công trên UI.
Blocked:
