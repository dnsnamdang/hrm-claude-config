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
