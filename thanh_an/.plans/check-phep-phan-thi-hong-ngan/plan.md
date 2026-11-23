# Check: NV Phan Thị Hồng Ngạn (NV.00150) có Ngày bắt đầu tính phép 23/11 nhưng hôm nay (23/11) chưa dùng được phép — @khoipv

Màn: `https://demothanhan.dnsmedia.vn/human/employee_info/150/edit` — employee_info_id 150, company_id 4, Phòng Tổng hợp - HCNS HN
Bắt đầu: 23/11/2026 · Loại: Check logic (không sửa code)

## Task
- [x] Lấy dữ liệu NV trên demo: vào cty 23/03/2026, chính thức 23/05/2026, **bắt đầu tính phép 23/11/2026**
- [x] Lấy báo cáo phép 2026 trên demo: được dùng **0**, đã nghỉ 0, còn 0
- [x] Trace nguồn "được dùng": validate `LeaveDayNPRule` (qua `AttendanceRequest::withValidator`) đọc `employee_attendances.usable_leave_days`, do `EmployeeAttendanceService::updateDataAll()` tính (lệnh `php artisan update:attendance` / nút "Cập nhật dữ liệu" `/timesheet/setting/holiday` → `GET timesheet/employee-attendance/update-data`). Không tính lại theo thời gian thực.
- [x] Mô phỏng công thức với quy định chấm công (bản ghi duy nhất id 1, `show()` bỏ qua company_id)
- [x] Kiểm Carbon `createFromFormat('Y-m-d')` lấy giờ hiện tại (test PHP local)
- [x] Chờ user chốt → 23/11 chọn **sửa code so theo ngày** để dùng được ngay trong ngày bắt đầu

## Phase 2 — Sửa code (23/11/2026)
### BE
- [x] `EmployeeAttendanceService::getUsableLeaveDays()`: mốc ngày bắt đầu tính phép lấy `startOfDay()` trước khi so `lte($now)` (điều kiện ứng phép)
- [x] Test local (reflection, `$now` lùi 2 giây giả lập vòng lặp, quy định local giống demo: ứng type 2, max 6): `enter_date` hôm nay → **1**, ngày mai → 0, hôm qua → 1
- [x] Commit `5e9d171b` trên `thanhan-dev` (chưa push), cherry-pick lên `master` = `d7346d7a`, đã push `origin/master` (23/11/2026, theo yêu cầu user)
- [ ] Deploy API lên demo (không migration)

## Phase 3 — User bấm "Cập nhật dữ liệu" nhưng báo cáo vẫn 0 (23/11/2026)
- [x] Demo: NV 150 vẫn `usable_leave_days = 0`; không NV nào đổi số so với sáng → lần cập nhật chưa ghi số mới
- [x] Báo cáo (`ReportService::attendance_report`) đọc thẳng `employee_attendances` → không phải lỗi báo cáo
- [x] Local: chạy `updateDataAll()` bản đã sửa (transaction + rollback) → NV 150 **usable = 1**, chạy mất **~102 s** ⇒ code đúng
- [x] Nút "Cập nhật dữ liệu" chỉ `dispatch` job `UpdateEmployeeAttendance` (ShouldQueue, `QUEUE_CONNECTION=database`) → chạy nền qua `queue:work`. Nghi: (1) demo chưa deploy `d7346d7a`; (2) worker không chạy / chưa `queue:restart` nên còn chạy code cũ; (3) job ~100 s vượt `--timeout` mặc định 60 s của worker → bị kill, NV id lớn (150) chưa tới lượt
- [x] User chạy lại → báo cáo phép demo NV 150: **Tổng phép được dùng = 1**, còn lại 1 (ảnh 23/11 09:45)
- [x] Giải thích cách tính cho user: 1 ngày = **ứng** T11 + T12 (mỗi tháng 0.5), không phải phép đã tích; T11 không bao giờ đủ 10 công → sang T12 được dùng còn 0.5

### Checkpoint — 23/11/2026 (Phase 3)
Vừa hoàn thành: xác nhận code đúng ở local (NV 150 = 1); khoanh nguyên nhân ở phía server demo (deploy / queue)
Đang làm dở: —
Bước tiếp theo: user chạy `git log -1` + `php artisan update:attendance` trên server demo
Blocked: không có quyền vào server demo
- [ ] Sau deploy: chạy `php artisan update:attendance` (hoặc bấm "Cập nhật dữ liệu" ở `/timesheet/setting/holiday`) → NV 150 được dùng 1

### Checkpoint — 23/11/2026 (Phase 2)
Vừa hoàn thành: sửa `getUsableLeaveDays()` so theo ngày + test local đạt
Đang làm dở: —
Bước tiếp theo: user commit/deploy API → chạy `php artisan update:attendance` trên demo → kiểm báo cáo phép NV.00150 = 1
Blocked:

## Công thức áp cho NV 150 (quy định hiện tại)
- Tháng 1–10: trước tháng bắt đầu tính phép → 0.
- Tháng 11: công 23/11 → hôm nay < 10 (`additional_for_unpaid_leave_greater = 10`) → 0. Cả tháng 11 chỉ còn ~6 ngày làm → **tháng 11 không bao giờ đủ 10 công**.
- Thâm niên: tính phép từ T11 (>6) → mốc 01/01/2027 → 0. Phép năm trước: 0.
- Ứng phép (`allow_to_advance_leave = true`, type 2 – tối đa 6): chỉ cộng khi `vacation_start_date <= $now` → tháng 11 ứng (12 − 10)/2 = **1 ngày**.

## Nguyên nhân hôm nay chưa dùng được
1. `usable_leave_days` chỉ cập nhật khi chạy `update:attendance`; lần chạy trước 23/11 thì ngày bắt đầu tính phép còn ở tương lai → không ứng → 0.
2. Kể cả chạy lại **trong ngày 23/11** vẫn ra 0: `getUsableLeaveDays()` so `Carbon::createFromFormat('Y-m-d', '2026-11-23')` (mang **giờ hiện tại** lúc tạo) với `$now` tạo ở đầu vòng lặp → mốc ngày bắt đầu luôn trễ hơn `$now` vài giây → `lte` = false → không ứng. (Test local: `lte=false`.) ⇒ đúng ngày bắt đầu tính phép không bao giờ được ứng.
3. Từ **24/11**, chạy lại cập nhật → được dùng = **1** (ứng), NV làm đơn tối đa 1 ngày.

## Lưu ý thêm (báo user)
- Sang tháng 12: tháng 11 không đủ công nên không được 0.5; ứng còn (12 − 11)/2 = 0.5 → được dùng tụt về **0.5** (+0.5 khi tháng 12 đủ 10 công). Nếu NV đã nghỉ 1 ngày trong tháng 11 thì đầu tháng 12 sẽ âm 0.5 → app báo "Ngày đã nghỉ không được lớn hơn số ngày được sử dụng" cho tới khi tháng 12 đủ công.

## Hướng xử lý (chờ user)
- Không sửa code: từ 24/11 chạy `php artisan update:attendance` hoặc bấm "Cập nhật dữ liệu" (Cài đặt ngày nghỉ) → NV có 1 ngày.
- Nếu muốn dùng được ngay trong ngày bắt đầu: sửa `getUsableLeaveDays()` so theo ngày (`startOfDay()` / `lte($now->endOfDay())`) — hàm dùng chung tính phép mọi NV, cần user xác nhận.

### Checkpoint — 23/11/2026
Vừa hoàn thành: ra nguyên nhân (được dùng = 0 do chưa tính lại + bẫy giờ trong `getUsableLeaveDays` đúng ngày bắt đầu)
Đang làm dở: —
Bước tiếp theo: user chốt chờ 24/11 cập nhật dữ liệu hay sửa code so theo ngày
Blocked:
