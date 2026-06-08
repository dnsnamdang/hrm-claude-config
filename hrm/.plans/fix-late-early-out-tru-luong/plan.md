# Plan — Fix đăng ký đi muộn/về sớm "có trừ lương" vẫn bị tính đi muộn

## Bối cảnh
- NV Nguyễn Thị Thu Huyền (mã 12410481, employee_info_id=1258) đăng ký đi muộn/về sớm ngày 4/6/2026 (bản ghi `late_early_outs` id=186) nhưng bảng công chi tiết tháng vẫn tính đi muộn 35'.
- Nguyên nhân: bản ghi có `has_salary_deduction=1` ("có trừ lương"). Nhánh này trong `TimesheetSummaryService::calcTimesheetEmployee` KHÔNG dời `checkin_accept` → `minutes_late` vẫn đầy đủ.
- Bảng công chi tiết tháng (`TimesheetMonthSummaryService`) hiển thị Lần/Phút/Công đi muộn đều từ `minutes_late` (không dùng `is_late`); cột Công (trừ lương) = `minutes_late/(8*60)` → "đi muộn" và "trừ lương" là cùng 1 con số, không tách được.
- Quyết định nghiệp vụ (user chốt): **Tha hoàn toàn** — khi có đăng ký "có trừ lương" được duyệt áp dụng cho ngày đó thì `minutes_late=0` (không đi muộn, không trừ lương), kể cả phần vượt cửa sổ đăng ký.

## Phạm vi
- Chỉ đụng nhánh "có trừ lương" (`$late_early_out_tru_luong`). Nhánh "không trừ lương" (`$late_early_out`) giữ nguyên.

## BE
- [x] `TimesheetSummaryService::calcTimesheetEmployee`: thêm block tha hoàn toàn cho `$late_early_out_tru_luong` (sau dòng 730, trước khối phạt) — tha đi muộn nếu `late_coming_shift_start>0`, tha về sớm nếu `early_leaving_shift_end>0`.
- [x] Tính lại công chị Huyền tháng 6/2026: `php artisan calc:employee_timesheet 1258 2026-06-01 2026-06-30` → OK.

## Verify
- [x] DB `timesheet_summaries` ngày 2026-06-04 (emp 1258): `is_late=0`, `minutes_late=0`, `punishment_day=0`. ✓
- [x] Regression: 2026-06-05 (không đăng ký) vẫn `is_late=1, minutes_late=1`. ✓
- [ ] Reload màn bảng công chi tiết tháng trên FE để xác nhận cụm Đi muộn ngày 4/6 = 0 (user kiểm tra).

## Lưu ý
- Sau thay đổi, "có trừ lương" trở nên khoan dung hơn "không trừ lương" (loại sau chỉ tha trong cửa sổ, phần vượt vẫn tính). Đã báo user.
