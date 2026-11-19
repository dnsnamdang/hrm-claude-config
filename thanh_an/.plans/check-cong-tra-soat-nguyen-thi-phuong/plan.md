# Check: Đã tra soát công mà vẫn 0.5 công (Nguyễn Thị Phương 22/10) — @khoipv

Màn: `timesheet/timesheet_details` — demothanhan.dnsmedia.vn
NV: Nguyễn Thị Phương — NV.00032 (employee_info_id 32, ssn 32) — ngày 22/10/2026
(Có 2 NV trùng tên; NV.00172 ngày 22/10 = 1(MKP), không liên quan)

## Task
- [x] Tìm employee_info_id của NV trên demo → 32
- [x] Gọi API `timesheet_summaries/detail` ngày 2026-10-22 → xem ca, giờ chấm, tra soát, labour_day
- [x] Lấy dữ liệu chấm thô (`/timekeeper`) + phiếu tra soát (`/timesheet/request-update-working`)
- [x] Đối chiếu code `TimesheetSummaryService::calcTimesheetEmployee()` → kết luận

## Dữ liệu demo
- Ca #56 "Ca Hành chính (Đội Cấn)_NEW" 08:00–17:30, khung vào 07:00–10:15, khung ra 15:30–20:00, quên chấm vào/ra trừ 0.5.
- Có phiếu giao việc #2636 (Abbott) → `checkout_accept` = 11:00.
- Chấm thô 22/10: 08:00 (Tra soát, id 440680) · 10:31:31 (máy) · 17:30 (Tra soát, id 440681) · 17:32:55 (máy).
- Phiếu tra soát **ĐNTSC-3294**: 08:00–17:30, tạo 23/10, **duyệt 30/10/2026 09:59** (Trần Hồng Vân).
- Bảng công 22/10 (summary 78779): `updated_at` = 28/10 22:28 (giờ VN) → checkin NULL, checkout 17:32:55 → trừ quên chấm vào 0.5 → **0.5 KLD/2**.

## Kết luận (KHÔNG phải bug logic tính công)
- Công 22/10 được tính lần cuối 28/10, **trước khi** phiếu tra soát được duyệt (30/10). Bản ghi tra soát 08:00 sinh ra lúc duyệt (id nằm trong dải id ngày 30/10) nên chưa được tính.
- Duyệt tra soát KHÔNG tự tính lại công: `RequestUpdateTimeSheetController::storeApprove()` dòng 187-190 đang comment `calcTimesheetEmployee`. Công chỉ cập nhật khi cron server chạy `calc:*` (không khai báo trong `app/Console/Kernel.php` → crontab ngoài).
- Mô phỏng tính lại: checkin 08:00 (trong khung 07:00–10:15) + checkout 17:32:55 → đủ **1 công**, không muộn/sớm.

## Hướng xử lý (chờ user)
- Chạy tay trên server demo: `php artisan calc:employee_timesheet 32 2026-10-22 2026-10-22`, hoặc chờ cron tính công lần tới.
- (Tuỳ chọn, cần user duyệt) Bật lại tính công ngay khi duyệt tra soát (bỏ comment dòng 187-190) — cần hỏi lý do trước đây comment.
