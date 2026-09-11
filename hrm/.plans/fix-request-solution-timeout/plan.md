# Fix POST /assign/request-solutions timeout 30s

## BE
- [x] `RequestSolutionService::calculateNeedReceiveDate()` — vòng lặp đếm ngày làm việc treo vô hạn khi trưởng phòng tiếp nhận không có (hoặc thiếu) ngày phân ca trong cửa sổ quét; guard cũ `$workingDaysCount > 365` không bao giờ chạm vì biến đếm không tăng. Đổi sang chặn theo số ngày đã quét (`$maxScanDays = $startDate->diffInDays($endDate)`), quét hết cửa sổ mà chưa đủ ngày làm việc thì fallback cộng lịch thường. Áp cho cả 2 nhánh (có/không có trưởng phòng).

### Checkpoint — 2026-08-26
Vừa hoàn thành: sửa 2 vòng lặp trong `Modules/Assign/Services/RequestSolutionService.php` (nhánh `tpe`), `php -l` pass.
Đang làm dở: chưa test thực tế trên dev.
Bước tiếp theo: gọi lại POST /api/v1/assign/request-solutions với payload cũ, kiểm tra `need_receive_date` trả về.
Blocked:
