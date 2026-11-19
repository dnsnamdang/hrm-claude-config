# Check: Tra soát công 08:00–17:00 chỉ được 0.5 công (KLD/2) — @khoipv

Màn: `timesheet` Bảng công chi tiết trong tháng — demothanhan.dnsmedia.vn
NV: Lê Đức Bình (employee_info_id 70, mã CC 70) — ngày 16/10/2026

## Task
- [x] Trace luồng tra soát công → `RequestUpdateTimeSheetService::storeApprove()` (dòng 334-359) tạo 2 bản ghi `timesheets` 08:00 và 17:00 (accept=1, place "Tra soát công")
- [x] Trace tính công `TimesheetSummaryService::calcTimesheetEmployee()`
- [x] Gọi API demo `GET /api/v1/timesheet/timesheet_summaries/detail?employee_info_id=70&day=2026-10-16`

## Kết luận (KHÔNG phải bug code — do cấu hình ca)
- Ca thực tế của NV ngày 16/10: **#53 "Ca Kỹ thuật Hà Nội (NEW)"** 09:30–17:30, khung chấm vào 07:00–10:00, **khung chấm ra 17:30–21:00**, phạt quên chấm vào/ra = 0.5 công.
- 17:00 nằm ngoài khung chấm ra (< 17:30) → không được nhận là giờ ra (`second_actual` dòng 377-384 lọc `>= attendance_end_at_from`; nhánh tra soát dòng 460-467 cũng chỉ nhận checkout trong khung) → 17:00 bị đẩy vào `checkin_out_center` (giữa ca).
- Kết quả DB: checkin 08:00, **checkout NULL**, checkin_out_center 17:00 → nhánh "chỉ có checkin" (dòng 478-485) trừ `penalty_notime_checkout_day` 0.5 → labour_day 0.5, `work_day_khong_ly_do` 0.5 → hiển thị "0.5 KLD/2".
- Nếu 17:00 được nhận là giờ ra thì chỉ tính về sớm 30 phút (phạt theo punishment rule ca 53: 1–30' trừ 0.5h), vẫn đủ 1 công.
- Lưu ý: đơn xin về sớm (LateEarlyOut) chỉ dời `checkout_accept` (dòng 361-364), KHÔNG mở rộng khung chấm ra → về 17:00 có đơn xin về sớm vẫn bị coi là không chấm ra (chưa test thực tế).

## Hướng xử lý (chờ user chọn)
- Tra soát lại giờ ra ≥ 17:30 (nếu thực tế ở lại đến 17:30), hoặc
- HCNS sửa ca #53: lùi "Chấm ra từ" sớm hơn (vd 15:30/16:00 như các ca khác) → 17:00 nhận là giờ ra, tính về sớm 30', đủ công. Sau đó chạy lại tính công ngày 16/10.
