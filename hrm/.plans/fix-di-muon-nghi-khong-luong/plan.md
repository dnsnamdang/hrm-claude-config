# Fix: chấm công tính "đi muộn" oan khi có đơn nghỉ KHÔNG LƯƠNG

## Vấn đề
NV Nguyễn Hồng Hải (id 195, mã 11610145) ngày 22/7/2026:
- Có đơn NGHỈ KHÔNG LƯƠNG buổi sáng 08:30–12:00 (đã duyệt, leave_type 5, salary_ratio=0).
- Chấm công vào 10:00 → hệ thống báo "M" (đi muộn), minutes_late=90, is_late=1, hiển thị "0.5(M) KL/2".

## Nguyên nhân
`TimesheetSummaryService::calcTimesheetEmployee`, dòng 688 (đi muộn) + 699 (về sớm):
`if(... && $subDay == 0)` — `$subDay` CHỈ đếm nghỉ CÓ LƯƠNG (salary_ratio>0, dòng 177). Nghỉ không lương rơi vào `$nghi_co_ly_do` (dòng 180), không được xét → vẫn tính muộn.
→ Nghỉ có lương nửa buổi thì miễn muộn, nghỉ KHÔNG lương nửa buổi thì VẪN bị muộn (bất nhất). Cả hai đều có đơn duyệt phủ đầu ca.

## Quyết định nghiệp vụ (user chốt 2026-07-27)
KHÔNG tính đi muộn khi có đơn nghỉ không lương.

## Fix
Thêm `&& $nghi_co_ly_do == 0` vào điều kiện dòng 688 (đi muộn) và 699 (về sớm) → có bất kỳ đơn nghỉ nào (có/không lương) phủ ca thì không phạt muộn/sớm.

## Tasks
- [x] Sửa dòng 688 + 699 (thêm `&& $nghi_co_ly_do == 0`)
- [x] Verify logic: NV 195 ngày 22/7 → is_late=0 (không chạy recalc prod; user tự recalc test)
- [x] Đánh giá edge case (nghỉ chiều + muộn sáng — nhất quán hành vi cũ)

### Checkpoint — 2026-07-27
Vừa hoàn thành: sửa 688+699 thêm `&& $nghi_co_ly_do == 0`; php -l sạch; xác nhận đơn NV195/22-7 là "Nghỉ không lương" salary_ratio=0 → sau fix không tính muộn.
Chưa làm: user RECALC công NV195 ngày 22 để áp dụng (chưa chạy recalc vì .env trỏ hrm_pro PROD, chỉ đọc). CHƯA commit.
Blocked: —
