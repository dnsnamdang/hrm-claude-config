# Phiếu công tác khác — áp quy tắc "Chấm công tại địa điểm cố định"

Redmine #11223 · nhánh `tpe-develop-assign_fix` · phiếu mẫu: https://hrm.eteksofts.com/assign/assign_business/13689/show

## Yêu cầu
Phiếu công tác khác (`assign_requests.business_type = 2`) phải xử lý cờ `fixed_position` giống Phiếu giao công tác chấm công (`business_trip_assigns`):
- KHÔNG tích → địa điểm phiếu chỉ dùng cho lần chấm ĐẦU TIÊN của ngày đầu; sau đó bỏ ràng buộc vị trí (công tác di chuyển).
- CÓ tích → giữ ràng buộc vị trí suốt cả kỳ công tác.

## BE
- [x] `Modules/Timesheet/Services/TimesheetService.php` — `placeToCheckInOut()`, nhánh `new_business_trip` + `business_type != 1`: gom `businessPlaces` rồi áp quy tắc `isFirstDay` / `fixed_position` (copy khuôn từ nhánh `business_trip` cùng hàm).

## FE
- Không cần sửa: checkbox "Chấm công tại địa điểm cố định" đã có sẵn trong `components/assign-components/assign-business/AssignBusinessForm.vue:227-237` (trong template `business_type == 2`) và BE đã lưu ở `Modules/Assign/Services/AssignBusinessService.php:324,456`.

## Còn bỏ ngỏ (chưa nằm trong task)
- `allPlaceToCheckInOut()` (dùng bởi `checkTimesheet()` chạy lại cờ `accept`) hiện chưa xử lý `new_business_trip` — giữ nguyên, chưa đụng.
- Phiếu công tác kỹ thuật (`business_type = 1`) lấy địa điểm từ `assign_business_tasks.places`, không có cờ `fixed_position` — ngoài phạm vi #11223.

## Test (2026-08-25)
- [x] Test ở mức service trên DB local (`php artisan tinker`, bọc transaction + rollback), phiếu thật **PCT-13471** (business_type=2, 05→06/08/2026, địa điểm Song Khê - Bắc Giang), NV Nguyễn Văn Tế (employee_info 404, ssn 41410781, company 3, `max_distance_for_business_trip = 3000m`). Điểm xa dùng để thử: Hà Nội, cách ~50km.
- 6 kịch bản (ngày đầu chưa chấm / đã chấm / có-không tích cố định / ngày thứ 2 / lượt chấm ca hành chính) đều ra đúng kỳ vọng; chạy lại trên code cũ cho thấy trước đây **luôn chặn** ở mọi trường hợp.
- Script: `scratchpad/test_fixed_position.php` (không commit). Dữ liệu sau test kiểm tra lại: `fixed_position = 0`, 2 dòng timesheet gốc còn nguyên.

## Test E2E qua API app (2026-08-25)
- [x] Tự tạo phiếu `PCT-E2E-TEST` (business_type=2, hôm nay 08:00 → mai 17:00, địa điểm Hồ Gươm), gán `employees.id = 13` (namdangit@gmail.com — email này được controller bỏ qua kiểm tra thiết bị), đổi tạm mật khẩu để lấy JWT.
- `GET /api/v1/timekeeper/listTimesheetTypes` → phiếu hiện đúng `type = new_business_trip`, name "Phiếu công tác khác".
- `POST /api/v1/timekeeper/` — **KHÔNG tích cố định**: lượt đầu ở xa 50km → 422 "Vị trí chấm công không hợp lệ"; lượt đầu đúng điểm → 200; lượt 2 và 3 ở xa → **200** (đã mở khoá).
- **CÓ tích cố định**: lượt đầu xa → 422; lượt đầu đúng điểm → 200; lượt 2, 3 ở xa → **422** (vẫn chặn suốt kỳ).
- Đã dọn sạch: xoá phiếu + dòng `assign_request_employees` + các lượt chấm test, trả lại hash mật khẩu cũ và `login_count` cho `employees.id = 13`.
