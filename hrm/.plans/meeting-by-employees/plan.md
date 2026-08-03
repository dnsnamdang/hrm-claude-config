# Plan — Báo cáo meeting theo nhân viên

## Phase 1 — Fix biểu đồ Top phòng ban sai số liệu

### BE
- [x] `getChartData()` — đếm distinct meeting cho mỗi phòng ban (trước đây cộng theo từng lượt tham gia nên số meeting/phút bị nhân lên theo số nhân viên)
- [x] `getChartData()` — áp bộ lọc `part_id` (Bộ phận) vào metric bằng `employeeMatchesScopeFilters()`, thêm `part_id` vào select `info`

### Checkpoint — 2026-07-27
Vừa hoàn thành: fix `Modules/Assign/Services/Report/MeetingByEmployeesService.php::getChartData()`; verify local qua tinker — chart khớp bảng chi tiết (dept 124: 4/553, dept 58: 3/395; lọc bộ phận: 3/433).
Đang làm dở: không có.
Bước tiếp theo: deploy dev, kiểm tra lại màn `/assign/report/meeting-by-employees`.
Blocked:
