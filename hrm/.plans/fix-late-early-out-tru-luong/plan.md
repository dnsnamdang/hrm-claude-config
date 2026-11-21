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

## Phase 2 — Về sớm có đơn duyệt không hiện (20/11/2026) — @cuong61n
- [x] 20/11/2026 Điều tra: NV có đơn đi muộn/về sớm "có trừ lương" duyệt (vd emp 23, đơn id 242, ngày 18/11/2026, chấm ra 15:53 < 17:30) → bảng công không hiện "(VS)", `minutes_early=0`, đủ công. Nguyên nhân: khối "tha hoàn toàn" của Phase 1 (`TimesheetSummaryService` ~dòng 770-784) xoá `minutes_early`. Kiểm bằng DB prod (chỉ đọc) + đọc code; chưa sửa.
- [x] 21/11/2026 Sửa theo tin nhắn Huyền (worktrees/gop_db-api, nhánh gop_db, CHƯA commit): (1) gỡ khối "tha hoàn toàn" của Phase 1 → có đơn vẫn hiện (M)/(VS) + phút; (2) `$allLateEarlyOuts` bỏ lọc `has_salary_deduction=1`, thêm lọc đã duyệt → mọi đơn duyệt miễn đếm số lần, không đơn thì đếm lần + phút. `php -l` OK; chưa chạy tính lại (local không có dữ liệu NV này).
- [ ] Chạy `calc:employee_timesheet` tháng 11/2026 cho NV có đơn + kiểm màn timesheet_details (emp 23 ngày 18/11 phải ra (VS) ~96 phút, số lần không tăng).
- [ ] Còn lệch chỗ khác: `TimesheetMonthSummaryService` đếm lần mọi ngày, `CreateTimesheetSummary` chỉ miễn đơn trừ lương — chờ user chốt có đồng bộ không.
- [x] 21/11/2026 Báo cáo tổng hợp chấm công (`ReportService::timekeeper_report`, màn timekeeper_report) có SQL đếm lần RIÊNG: sửa cho khớp bảng công chi tiết — mọi đơn ĐÃ DUYỆT (bất kỳ lý do) miễn đếm lần, chỉ còn phút; sửa lỗi lệch thứ (DAYOFWEEK MySQL 1=CN nhưng code ánh xạ 1=monday → 18/11 thứ Tư bị tra cột thursday). Kiểm: tinker chạy được 45 dòng không lỗi SQL; chưa đối chiếu số liệu NV có đơn (local không có). Chưa commit.
- [x] 21/11/2026 Đã đẩy `gop_db` (commit 5388c418e, chỉ 2 file ReportService + TimesheetSummaryService) và kéo lên PROD hrm-tpe (`git pull --ff-only` ở /var/www/tpe/hrm-api, không chạy build_tpe.sh vì chỉ BE, không migrate). Tính lại Đào Thị Thúy (id 23, mã 11710160, HN_QTTT) 01–20/11: ngày 18/11 trước `minutes_early=0, is_early=0` → sau `minutes_early=96, is_early=1`, labour_day vẫn 1.00, punishment_day 0 (prod chưa ca nào bật phạt). Chưa nhìn màn hình prod.
- [ ] Còn: TimesheetMonthSummaryService + CreateTimesheetSummary chưa đồng bộ luật đếm lần; đơn không trừ lương vẫn dời mốc; chưa tính lại cho NV khác có đơn.
- [x] 21/11/2026 Lỗi thật sau lần deploy đầu: Thúy vẫn `so_lan_ve_som=1` dù có đơn duyệt. Nguyên nhân: `late_early_outs.start_at` là chuỗi `'Y-m-d 00:00:00'`, so `<= day ('Y-m-d')` luôn sai ở ngày đầu đơn → đơn 1 ngày không bao giờ khớp (lỗi có từ trước, cả bản cũ). Sửa so 10 ký tự đầu ở 2 chỗ `TimesheetSummaryService` (commit ae89ee644, đã pull lên prod). Kiểm bằng gọi `getDataTimesheet` trên prod: Thúy 01–20/11 → `so_lan_ve_som=0, ve_som=96, ô 18/11="1(VS)"`.
- [ ] Cùng lỗi so chuỗi còn ở `Modules/Agent/Support/ChamCongTongHop.php:109` (công cụ AI chat) — chưa sửa, chờ user.
- [x] 21/11/2026 Tính lại PROD cho mọi NV có đơn đi muộn/về sớm ĐÃ DUYỆT giao 06/06→21/11: 28 đơn / 20 NV, 28 lệnh `calc:employee_timesheet` đều "Cập nhật thành công". So trước/sau (220 dòng công): 14 ngày đổi (đều do đơn có trừ lương: phút đi muộn/về sớm hiện lại, vd NV 1258 ngày 15/09 = 75', 27/10 = 93'), labour_day vẫn 1.00, punishment_day vẫn 0. Chưa tính lại bảng tổng hợp THÁNG (timesheet_month_summaries). Số liệu trước lưu ở scratchpad before.tsv (phiên này).
