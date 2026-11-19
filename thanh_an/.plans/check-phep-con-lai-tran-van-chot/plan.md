# Check: NV Trần Văn Chót làm đơn nghỉ phép 21/11 bị báo "Ngày nghỉ không được lớn hơn số ngày nghỉ còn lại" — @khoipv

Màn: `https://demothanhan.dnsmedia.vn/timesheet/report/attendance_report` — NV.00046 Trần Văn Chót (employee_info_id 46, Phòng Kho HCM 2, company_id 4)
Bắt đầu: 17/11/2026

## Task
- [x] Tìm nơi sinh lỗi: `LeaveDayNPRule` (BE) ← `AttendanceRequest::withValidator()` dòng 201–226
- [x] So công thức "còn lại" của báo cáo (`ReportService::attendance_report` dòng 778–812) với công thức validate
- [x] Lấy số liệu trên demo: báo cáo phép, danh sách đơn Nghỉ phép đã duyệt, bảng công 10/10 + 07/11
- [x] Soát các NV khác có cùng tình trạng (công ty 4)
- [x] Chờ user chốt hướng xử lý → 17/11 chọn **hướng 1 (sửa code tính công)**, cách: thêm tham số tùy chọn vào `sumDate()`

## Phase 2 — Sửa code tính công (17/11/2026)
Quy tắc: ngày đã chốt là ngày thường (`timesheet_summaries.type_day = 1`, chỉ cập nhật đúng ngày chạy) → đơn nghỉ trong ngày đó tính như ngày thường, bỏ qua quy định cuối tuần hiện tại.
### BE
- [x] `AttendanceTrait::sumDate()` thêm tham số tùy chọn `$workingDates = []` — ngày nằm trong danh sách thì bỏ qua check cuối tuần (mặc định rỗng → các chỗ gọi khác không đổi)
- [x] `TimesheetSummaryService::calcTimesheetEmployee()` truyền `[$date]` khi `type_day == 1`
- [x] Test local (transaction + rollback, quy định sau rollback vẫn = 5): giả lập quy định 4
  - `sumDate` 14/03 08:00–17:30: không truyền → **0**, truyền `['2026-03-14']` → **1**
  - Tính lại 5 NV/ngày T7 chẵn type_day 1 có đơn (11, 28, 135 ngày 14/03; 29 ngày 28/03; 74 ngày 11/04): phép / không lương / labour_day / data_attendance **giữ nguyên** như trước khi đổi quy định
- [x] Soát demo: 106 lượt đơn đã duyệt rơi vào T7 chẵn 09/03–02/11/2026 → **32 đơn / 31 NV-ngày** bị bảng công về 0 (toàn bộ 10/10 và 24/10, cập nhật 06/11 ~22:1x–22:3x VN). Các dòng "lệch" còn lại là đơn nhiều ngày (bảng công 1/ngày) → đúng.
- [x] Commit `60931eac` đã push `origin/master` (17/11/2026, theo yêu cầu user)
- [ ] Deploy BE lên demo, chạy lại công 10/10 + 24/10 (lệnh bên dưới)
- [ ] Kiểm lại báo cáo phép: NV.00046 còn **0** (app chặn đơn 21/11 là đúng)

### Lệnh tính lại sau khi deploy
**Cách nhanh (khuyên dùng) — 2 lệnh, tính lại cả ngày cho mọi NV đang làm:**
```
php artisan calc:timesheet 2026-10-10
php artisan calc:timesheet 2026-10-24
```
An toàn vì cả 2 ngày đã được tính lại toàn bộ hôm 06/11 bằng đúng code này (chỉ khác lỗi cuối tuần); ngày đã qua không bị đổi `type_day`. NV không có đơn nghỉ 2 ngày đó sẽ ra như cũ (trừ khi có tra soát/điều chỉnh mới sau 06/11 — khi đó số mới là đúng).

**Cách chỉ tính 31 NV-ngày bị lỗi:**
```
php artisan calc:employee_timesheet 6 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 13 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 17 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 19 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 24 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 26 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 28 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 29 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 31 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 34 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 46 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 54 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 89 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 122 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 128 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 135 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 144 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 174 2026-10-10 2026-10-10
php artisan calc:employee_timesheet 6 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 17 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 24 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 27 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 41 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 48 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 59 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 67 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 73 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 111 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 139 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 164 2026-10-24 2026-10-24
php artisan calc:employee_timesheet 169 2026-10-24 2026-10-24
```

### Còn hở (chưa xử lý, đã báo user)
- Ngày đã chốt **cuối tuần** (`type_day = 2`) vẫn tính theo quy định hiện tại. Ví dụ T7 tháng 1–2/2026 (thời "nghỉ chiều T7", T7 tính 0.5): nếu tính lại bây giờ (quy định 4) sẽ ra 0 (T7 chẵn) hoặc 1 (T7 lẻ). Muốn đúng tuyệt đối cần lưu lịch sử quy định cuối tuần.
- Bảng công có vẻ được tính lại tháng trước vào tối mùng 6 hằng tháng (`updated_at` 06/04, 06/07, 06/08, 06/09, 06/11 ~22h VN) — không thấy trong `Kernel.php`, có thể là crontab server. Cần deploy trước 06/12 để tháng 11 không bị lỗi tương tự (T7 chẵn tháng 11 là ngày nghỉ theo quy định mới nên không ảnh hưởng, nhưng các lần đổi quy định sau này thì có).

### Checkpoint — 17/11/2026
Vừa hoàn thành: sửa `sumDate()` + `calcTimesheetEmployee()`, test local OK, lập danh sách 31 NV-ngày cần tính lại
Đang làm dở: —
Bước tiếp theo: user deploy BE lên demo → chạy 31 lệnh → kiểm lại báo cáo phép
Blocked: 

## 2 công thức "phép còn lại" đang lệch nhau
| Chỗ | Đã nghỉ lấy từ đâu |
|---|---|
| Báo cáo phép (`ReportService::attendance_report`) + ô "còn lại" trên form (`get-total-leave-day`) | Σ `timesheet_summaries.work_day_phep` trong năm + nghỉ ngoài hệ thống |
| Validate khi tạo đơn (`AttendanceRequest` → `LeaveDayNPRule`) | Σ `attendances.total_days` các đơn Nghỉ phép **đã duyệt** trong năm + nghỉ ngoài + ngày cắt phép |

## Số liệu demo NV 46
- Được dùng: 6 (`usable_leave_days` 6, cộng thêm 0)
- Đơn Nghỉ phép đã duyệt 2026: 14/04, 19/06, 05/08, 16/09, **10/10 (#1725, T7 thứ 2 trong tháng)**, 07/11 → mỗi đơn 1 ngày = **6**
- Bảng công: T4 1, T6 1, T8 1, T9 1, **T10 0**, T11 1 = **5** → báo cáo còn 1
- Validate: 6 − 6 = 0 < 1 (đơn 21/11) → chặn

## Nguyên nhân
- Bảng công 10/10 (summary 77754) bị tính lại lúc **06/11/2026 22:12** (VN), sau khi quy định chung đổi ngày 03/11 sang "nghỉ CN + thứ 7 chẵn" (xem `.plans/check-don-nghi-1779-so-ngay-0`).
- `calcTimesheetEmployee()` gọi lại `sumDate()` theo quy định **hiện tại** → 10/10 (thứ 7 chẵn) thành ngày nghỉ cuối tuần → `congWeekend` = 0 → `data_attendance = [{"id":1725,"total_day":0}]`, `work_day_phep = 0`, trong khi vẫn ghi `labour_day = 1.0`.
- Lúc làm đơn (10/10) quy định còn là "nghỉ thứ 7 lẻ" → 10/10 là ngày làm → trừ 1 phép là đúng.
- ⇒ App chặn là **đúng** theo đơn đã duyệt (đã dùng đủ 6/6). Báo cáo hiện "còn 1" là **sai** do bảng công tháng 10 bị tính lại theo quy định mới.

## Ảnh hưởng NV khác (công ty 4) — lệch "đơn đã duyệt" vs "bảng công"
Có đơn phép T7 chẵn tháng 10 (10/10, 24/10) bị về 0 trong bảng công: NV.00046, 00089, 00139, 00067, 00073, 00122, 00006, 00034, 00024, 00026, 00028, 00029, 00031, 00111, 00013, 00017, 00128, 00144, 00054 (một số NV còn lệch vì lý do khác, chưa soát).

## Hướng xử lý (chờ user chốt)
1. Sửa code tính công: ngày đã qua dùng quy định cuối tuần tại thời điểm đó / hoặc dùng `total_days` đã lưu của đơn đã duyệt → tính lại T10 cho các NV trên.
2. Chỉ sửa dữ liệu: cập nhật `work_day_phep` các ngày 10/10, 24/10 cho các đơn bị về 0 (không chặn được tái diễn khi tính lại công).
3. Nếu công ty coi 10/10 không trừ phép → phải sửa `total_days` đơn #1725 (và các đơn tương tự) về 0 để validate khớp.
