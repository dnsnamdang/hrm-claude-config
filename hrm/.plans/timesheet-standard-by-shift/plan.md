# Plan — Công định mức theo ngày phân ca (timesheet detail)

## Bối cảnh
Màn `timesheet/timesheet_details` cột "Công định mức" (`timesheet_month_summary_detail.standard`) đang tính sai cho NV chưa có phân ca trong kỳ: rơi vào fallback "số ngày − Chủ nhật" (VD Bùi Thị Hồng Ngân vào 01/06 nhưng bảng tháng 5 vẫn = 26). Yêu cầu: công định mức = số ngày ĐƯỢC PHÂN CA của chính NV trong tháng; nếu không có phân ca ngày nào → giữ cách cũ (số ngày − Chủ nhật). Chỉ áp dụng bảng tạo mới.

## Đính chính target (2026-07-06)
Màn `timesheet_details` gọi `GET timesheet/timesheet_summaries` → `TimesheetSummaryController::index` → `TimesheetSummaryService::index()` → `calcStandardWithCache()` (tính LIVE), KHÔNG đọc bảng `timesheet_month_summary_detail`. Kiểm chứng bằng API thật (Playwright fetch có token): June=26, May=26, July=25. → Fix phải nằm ở `calcStandardWithCache`, không phải CreateTimesheetSummary/MonthSummary.
Nguyên nhân 26: Ngân enter_date=01/06 (trong kỳ) → code chạy nhánh "đại diện cùng ca"; nhánh này fail trong cache → rơi fallback 30−4CN=26. Trong khi ngày phân ca THỰC của Ngân tháng 6 = 24.

## Phase 1 — BE (fix đúng chỗ)
- [x] Sửa `TimesheetSummaryService::calcStandardWithCache()`: bỏ nhánh enter/leave + "đại diện"; công định mức = số ngày phân ca của CHÍNH NV (`$shiftDetailEmployeeDates->get($id)->count()`); nếu =0 → giữ fallback weekend-basis cũ
- [x] Verify qua API thật (Playwright fetch token): Ngân June = 24 ✓ (trước 26); May = 26 (0 phân ca → fallback); July = 25. Phân bố 120 NV June: 24×117, 23×2, 7×1 — không regression
- [ ] (chờ user chốt) Có đồng bộ luồng tạo bảng tổng hợp đã lưu (CreateTimesheetSummary/standard) cho khớp không

## Ghi chú
- Lần fix trước nhắm nhầm service (CreateTimesheetSummary/MonthSummary) — đã bị revert. Header (`:358`) + Dashboard (`:299`) vẫn dùng `standard()` cũ, không đụng.

## Không làm
- Không recalc bảng đã tạo (user chốt chỉ áp dụng bảng mới)
- Không migration, không git

## Phase 2 — Redmine #11293 (2026-09-03)
Yêu cầu: NV vào/nghỉ giữa tháng, công định mức bảng CHI TIẾT phải khớp bảng TỔNG HỢP; xuất Excel bảng chi tiết thiếu tên công ty + tháng.
- [x] BE `TimesheetSummaryService::calcStandardWithCache()`: NV có enter_date/leave_date trong kỳ → gọi `AttendanceWatchRegulation::standard()` (dùng chung nguồn với bảng tổng hợp), NV trọn kỳ giữ đếm ngày phân ca từ cache
- [x] BE xoá 2 hàm chết `getNearestShiftDetailIdLocal` / `getTemplateStandardByShiftDetailLocal` (bản sao logic đại diện, thiếu lọc status/enter_date/leave_date)
- [x] BE `AttendanceWatchRegulation::standard()` (user chốt hướng B): không tìm được NV đại diện → lấy số ngày phân ca của CHÍNH NV trước, hết mới rơi fallback T7/CN. Giữ được kết quả Phase 1 (Ngân = 24, không quay lại 26) mà 2 bảng vẫn khớp
- [x] FE `components/export-excel/timesheet_details.vue`: chèn 3 dòng tiêu đề (tên công ty A1, địa chỉ A2, "Bảng công chi tiết tháng M.YYYY" A3 căn giữa); bộ lọc Công ty trống → 2 dòng đầu để trắng (user chốt). Toàn bộ merge/freeze/viền/tô T7-CN dịch theo hằng `titleRowCount`
- [x] Verify BE (local, DB hrm_prod_local): API `timesheet_summaries` khớp 100% `AttendanceWatchRegulation::standard()` ở mọi NV vào/nghỉ giữa kỳ — Nguyễn Quốc Việt (vào 22/06, phân ca 7) = 24; Ngô Xuân Thương (17/06, 11) = 24; Lưu Thế Hào (08/06, 18) = 24; Trương Tùng Dương (19/05, 10) = 23; Đinh Văn Thắng (09/04, 17) = 24
- [x] Verify không regression: Bùi Thị Hồng Ngân 6/2026 vẫn = 24 (kết quả Phase 1 giữ nguyên). Phân bố 150 NV tháng 6: 24×145, 23×2 (phân ca thật 23 ngày, trọn kỳ), 26×3 (enter_date 7-8/2026, chưa vào làm nên 0 ngày phân ca → fallback cũ, không đổi). Trước sửa có 1 NV ra 7, nay hết
- [x] Verify FE: tải Excel thật qua Playwright — R1 tên công ty, R2 địa chỉ, R3 "Bảng công chi tiết tháng 6.2026" merge A3:BM3 đậm 14 căn giữa, header dịch xuống R4-R7, freeze A8, cột CN (07/14/21/28) vẫn tô FFFFE0E0 từ dòng 8, khối tiêu đề không viền/không nền, cột A vẫn rộng 12 (không phình vì chuỗi công ty). Bỏ trống bộ lọc Công ty → R1/R2 trắng, R3 giữ nguyên

## Lưu ý Phase 2
`AttendanceWatchRegulation::standard()` là hàm dùng chung — còn `CreateTimesheetSummary:96`, `TimesheetMonthSummaryService:358,456`, `DashboadService:302` gọi. Bảng công ĐÃ CHỐT trước đây không được tính lại, nên có thể lệch với bảng tính mới ở đúng nhóm NV vào/nghỉ giữa kỳ không có đại diện.
