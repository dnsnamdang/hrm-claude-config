# Check: Nhân viên nghỉ 12/10 quên làm đơn, còn phép — cách trừ phép

- Người phụ trách: @khoipv
- Bắt đầu: 02/11/2026
- Loại: Check logic (không sửa code)

## Câu hỏi

Nhân viên nghỉ ngày 12/10/2026 nhưng chưa kịp làm đơn, vẫn còn phép. Có cách nào trừ phép cho nhân viên đó không?

## Task

- [x] Trace nguồn tính "phép đã dùng"
- [x] Check các đường ghi công phép vào ngày quá khứ
- [x] Kết luận + hướng dẫn thao tác

## Kết luận

**Có cách — dùng màn "Đề nghị tra soát công admin"** (`/timesheet/admin-request-update-workings/new`), chọn lý do **"Nghỉ phép quên làm phiếu"**, nhập **Trừ số ngày phép**. Không cần duyệt. Sau đó phải **tính lại công** ngày 12/10.

### Phép đã dùng lấy từ đâu
- Phép đã dùng = tổng `timesheet_summaries.work_day_phep` (`TimesheetSummaryService::getLeaveDaysByEmployee` dòng 1142). → Muốn trừ phép thì ngày 12/10 phải có `work_day_phep > 0` sau khi tính công.
- Lúc tính công 1 ngày, `work_day_phep` lấy từ 3 nguồn (`TimesheetSummaryService` ~dòng 160–765):
  1. Đơn nghỉ phép (LT_NP) đã duyệt
  2. Tra soát công của NV đã duyệt có `number_day_leave` (dòng 753)
  3. Tra soát công admin có `number_day_leave` (dòng 758–763, ghi đè)

### Vì sao không dùng 2 cách kia
- **Đơn nghỉ phép**: tạo mới bắt buộc `application_date` và `attendance_start_at` `after_or_equal:today` (`AttendanceRequest::rules()` dòng ~88) → không tạo lùi ngày được, và đơn luôn gắn `auth()->user()` (HR không tạo hộ được).
- **NV tự tra soát** (lý do "Nghỉ phép quên làm phiếu"): bị `WorkingDateRule` chặn — tối đa `general_regulations.update_working_hour` giờ sau ca (staging đang 72h) → 12/10 đã quá hạn.

### Tra soát công admin hoạt động thế nào
- BE: `AdminRequestUpdateTimeSheetController::store` → `AdminRequestUpdateTimeSheetService::store` (dòng 127): tạo phiếu + **sinh 2 lượt chấm công giả** (bảng `timesheets`, theo `ssn` của NV) tại "Giờ tra soát từ / đến" của ngày `from_date`.
- Validate: `from_date` ≤ hôm nay; lý do "Nghỉ phép quên làm phiếu" → `number_day_leave` bắt buộc, bội 0.5; `NumberDayLeaveRule` chặn vượt số phép còn lại năm hiện tại.
- Khi tính công: 2 lượt chấm giả → `labour_day` = đủ công ca; `work_day_phep` = `number_day_leave`. Đây là đúng thiết kế (đơn phép thường cũng cộng phép vào `labour_day` qua `$subDay`, bảng công tính `cong_lam_viec = tổng công − phép`), **không bị cộng trùng**.
- **Không tự tính lại công** sau khi lưu → phải chạy `php artisan calc:employee_timesheet {employee_info_id} 2026-10-12 2026-10-12` hoặc chờ cron.

### Lưu ý khi nhập
- Giờ tra soát từ/đến phải rơi **đúng khung chấm vào / khung chấm ra của ca** NV ngày 12/10 (VD ca có khung ra 17:30–21:00 thì giờ ra 17:00 sẽ không nhận → mất 0.5 công, xem `check-cong-tra-soat-ve-som`).
- Nghỉ cả ngày → giờ phủ cả ca + Trừ phép = 1. Nghỉ nửa ngày → Trừ phép = 0.5, giờ tra soát phủ phần còn lại tương ứng.
- NV phải có `ssn` (mã chấm công) — lượt chấm giả gắn theo `ssn`.
- 1 ngày chỉ lấy **1** phiếu admin (`->first()`): nếu ngày 12/10 đã có phiếu admin khác thì xoá phiếu cũ trước.
- Bảng công tháng 10 nếu đã chốt (`timesheet_month_summaries`) → cần tổng hợp lại sau khi tính công.
