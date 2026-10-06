# Fix #11525 — Nghỉ phép buổi sáng, chấm chiều bị tính KLD (ca không bắt buộc chấm ra) — @namdangit

Code sửa ở `develop` rồi chuyển sang `gop_db` theo yêu cầu user (develop không giữ thay đổi). File: `hrm-api/Modules/Timesheet/Services/TimesheetSummaryService.php`

- [x] Ca có chấm vào + KHÔNG bắt buộc chấm ra + có nghỉ giữa ca: không có chấm vào buổi sáng mà có chấm từ giờ bắt đầu nghỉ giữa ca → là chấm vào buổi chiều, tính nửa ca (labour/2); mốc đi muộn = "Nghỉ đến" (đơn nghỉ kéo qua thì lấy giờ hết đơn) + "Cho phép đi muộn"; áp phạt đi muộn theo ca như thường
- [x] Test 15 kịch bản trên DB local (NV 1597, ca 6, 04/08/2026) + hồi quy 297 cặp NV/ngày cũ vs mới: 296 giống hệt, 1 đổi đúng chủ đích (chấm chiều không đơn nghỉ: 0 công → 0.5 công + đi muộn)
- [x] Commit `a011d29aa` + push `gop_db` (30/09/2026)
- [ ] Deploy PROD (git pull gop_db) trước 21:00 để cron calc:many_timesheet tính lại tháng 9
