# Check: Đơn xin nghỉ 1779 — Số ngày nghỉ dự kiến = 0 — @khoipv

Màn: `https://demothanhan.dnsmedia.vn/timesheet/attendance/1779`

## Task
- [x] Lấy dữ liệu đơn 1779 trên demo (`GET /api/v1/timesheet/attendance/1779`)
- [x] Gọi lại `calculate-intend-day` trên demo với cùng khoảng thời gian
- [x] Xem quy định chung (`GET /api/v1/general-regulations`) + ngày lễ + loại nghỉ
- [x] Đối chiếu các đơn nghỉ thứ 7 khác (300 đơn gần nhất) trước / sau ngày đổi quy định
- [ ] Chờ user: có sửa `total_days` đơn 1779 → 1 không (sửa tay DB, đơn đã duyệt nên UI không sửa được)

## Dữ liệu đơn 1779
- Phạm Văn Tấn (employee_id 106, Kỹ thuật HCM, company_id 4) — Nghỉ không lương (leave_type 5, `is_calc_holiday = 0`)
- Tạo **02/11/2026 10:23** — nghỉ **07/11/2026 08:00 → 17:30** (thứ 7 **đầu tiên** của tháng → thứ 7 lẻ)
- `total_days = 0`, trạng thái Đã duyệt

## Kết luận — KHÔNG phải bug code, do đổi quy định cuối tuần sau khi tạo đơn
- Quy định chung (id 1) `updated_at = 03/11/2026 08:31` (giờ VN), `updated_by = 179`, hiện `basis_for_calculating_weekend = 4` (nghỉ CN + **thứ 7 chẵn**).
- Trước đó là `5` (nghỉ CN + **thứ 7 lẻ**) — đã ghi nhận ở `.plans/fix-so-ngay-nghi-du-kien-0` (28/08).
- Lúc tạo đơn (02/11), 07/11 là thứ 7 lẻ → ngày nghỉ cuối tuần → `congWeekend` = 0 → `total_days = 0` là **đúng theo quy định lúc đó**. Nghỉ không lương là loại duy nhất cho lưu 0 ngày nên không bị chặn.
- Hiện tại gọi lại API trên demo: 07/11 → **1**, 14/11 (thứ 7 chẵn) → **0** ⇒ đúng quy định mới.
- `total_days` lưu cứng lúc tạo đơn, đổi quy định không tính lại đơn cũ (có chủ đích, xem fix 1619).

## Đối chứng
| Nhóm đơn | Kết quả |
|---|---|
| Đơn tạo trước 03/11 (09–10/2026) | chỉ có đơn nghỉ thứ 7 **chẵn** (12/09, 26/09, 10/10, 24/10) ra 0.5/1 — thứ 7 lẻ là ngày nghỉ, không ai làm đơn |
| Đơn tạo sau 03/11 cho 07/11 (1787, 1789, 1791, 1793, 1795–1801) | đều 0.5 / 1 |
| Đơn tạo sau 03/11 cho 21/11 (1788, 1802, 1804) | 2 / 1 / 1.5 |
| **1779** — duy nhất tạo trước 03/11 cho 07/11 | **0** |

Không có đơn nào khác tạo trước 03/11 cho thứ 7 sau 03/11 trong 300 đơn gần nhất.

## Ảnh hưởng tới tính công (hỏi thêm 09/11) — KHÔNG ảnh hưởng
- [x] `TimesheetSummaryService::calcTimesheetEmployee()` (dòng 109–175) KHÔNG đọc `attendances.total_days`, mà gọi lại `sumDate()` theo quy định **tại thời điểm tính công**.
- [x] Kiểm chứng demo `timesheet_summaries/detail?employee_info_id=106&day=2026-11-07` (summary 80334, tính lần cuối 08/11 22:08 VN):
      `type_day = 1` (ngày thường), `work_day_khong_luong = 1.0`, `data_attendance = [{"id":1779,"total_day":1}]`, ca #89 "Ca linh hoạt_T7 HCM" 08:00–17:30 → **công đã tính đúng 1 ngày nghỉ không lương**.
- [x] Payroll không đọc `attendances.total_days` (lương lấy từ bảng công).
- Chỗ còn dùng `total_days` đã lưu (chỉ ảnh hưởng hiển thị):
  - `get-total-leave-day` (ô "Số ngày đã nghỉ" trên form đơn): NV 106 loại Nghỉ không lương năm 2026 = **2.5** (đúng ra 3.5)
  - `DashboadService.php:224` — dashboard ngày 07/11 hiện "Nghỉ không lương 0"
  - `ReportService.php:203` — danh sách đơn trong báo cáo
- Hạn mức: Nghỉ không lương (`LT_NKL`) không bị kiểm `LeaveDayRule` → thiếu 1 ngày không làm sai việc chặn đơn.

## Hỏi thêm 09/11: Bảng phân ca tổng hợp ngày 14/11 (thứ 7 chẵn) vẫn hiện ca
- [x] Header đỏ: chỉ là CSS `.saturday/.sunday` (`timeworking/index.vue:320`), tô mọi T7/CN, không xét quy định chung.
- [x] Ô ca — `TimeWorkingService::getListEmployee()` (dòng 149–184):
  - Ngày `<= hôm nay` → lấy ca thực tế đã sinh (`shift_detail_dates` theo ngày) → đúng.
  - Ngày **tương lai** → lọc theo cờ thứ trong tuần của phân ca (`shift_details.saturday = 1`), **KHÔNG gọi `isWeekend()`** → mọi thứ 7 đều hiện ca.
- [x] Ca thực tế khi tới ngày — `TimesheetService::getWorkshift()` dòng 682–683: `isWeekend()` = true → **return null, không tạo ca** (dùng cho chấm công, tạo bảng công, tra soát, OT…).
- [x] Kiểm chứng demo (NV.00042, 00055, 00025):
  | Ngày | Bảng phân ca | Bảng công |
  |---|---|---|
  | 17/10, 31/10 (T7 lẻ, quy định cũ = nghỉ) | trống | không có bản ghi |
  | 24/10 (T7 chẵn, quy định cũ = làm) | có ca | 1 công |
  | 07/11 (T7 lẻ, quy định mới = làm) | có ca | 1 công |
  | 14/11, 28/11 (T7 chẵn, quy định mới = nghỉ) | **hiện ca (dự báo sai)** | — (chưa tới) |
- ⇒ 14/11 tới ngày sẽ KHÔNG có ca / không tính công; cột 14/11 sẽ thành trống. Bảng phân ca chỉ hiển thị sai ở phần ngày tương lai.
- [ ] Chờ user: có sửa nhánh ngày tương lai của `TimeWorkingService::getListEmployee()` thêm check `isWeekend()` cho khớp `getWorkshift()` không.

## Ghi chú
- Vẫn còn tồn tại vấn đề đã biết: `AttendanceWatchRegulation::isWeekend()/congWeekend()` dùng `GeneralRegulation::first()` (công ty id 1) cho mọi công ty — NV company 4 cũng theo quy định công ty 1. Task riêng, chưa làm.

### Checkpoint — 09/11/2026
Vừa hoàn thành: chốt nguyên nhân đơn 1779 = 0 (đổi quy định cuối tuần 5 → 4 ngày 03/11, sau khi tạo đơn)
Đang làm dở: (không)
Bước tiếp theo: chờ user quyết có sửa `total_days` đơn 1779 → 1 không
Blocked:
