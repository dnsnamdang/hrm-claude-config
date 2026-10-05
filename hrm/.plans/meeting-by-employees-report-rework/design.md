# Design — Báo cáo meeting nhân viên theo thời gian (Redmine #11145)

> Feature: `meeting-by-employees-report-rework` · Phụ trách: @junfoke · Nhánh `task_11145` (tách từ `tpe`, cả 2 repo)

## Mục tiêu

Sửa báo cáo có sẵn `Báo cáo thời gian meeting theo nhân viên` để đo đúng **khối lượng công việc
thực tế** của phòng ban / nhân viên: đổi tên, lọc trạng thái theo mốc thời gian, thêm 2 cột nội
dung, và cho chọn cột khi in.

## Scope

| Có làm | Không làm |
| --- | --- |
| Đổi **chữ hiển thị** ở 5 chỗ | KHÔNG đổi tên 4 quyền (id 1057-1060) và KHÔNG đổi URL route |
| Lọc trạng thái theo mốc thời gian **của từng meeting** | Không đụng các báo cáo meeting khác |
| Thêm ô lọc Phòng ban / Bộ phận trên FE (BE đã hỗ trợ sẵn) | Không sửa quyền, không migration |
| 2 cột `Nội dung meeting` + `Kết luận cuộc họp` | |
| Chọn ẩn/hiện cột khi **In** | Không áp cho Xuất Excel, không áp cho bảng trên màn |

## Quyết định (user chốt 12/09/2026)

1. **Mốc thời gian xét THEO TỪNG MEETING, không theo cả khoảng lọc.**
   Meeting đã qua giờ bắt đầu → chỉ lấy `Hoàn thành` / `Hủy`; meeting chưa tới → chỉ lấy `Chốt lịch`.
   Lý do: khoảng lọc hay vắt qua hôm nay (lọc cả tháng, lọc tuần) — xét theo cả khoảng thì luôn
   mất một nửa dữ liệu.

2. **Meeting `Hủy`: đếm số lượng, KHÔNG cộng thời lượng.**
   Cuộc họp không diễn ra thì không tốn thời gian của nhân viên — cộng vào là thổi phồng số giờ
   làm việc, đúng thứ báo cáo này sinh ra để tránh. Có chip `Hủy` riêng để nhìn ra ngay.
   ⚠️ Đây là **thay đổi số liệu**: trước nay báo cáo lọc cứng `REPORT_STATUSES = [Chốt lịch, Hoàn thành]`,
   `Hủy` chưa từng xuất hiện. Mọi KPI / biểu đồ / popup drill-down sẽ khác con số hôm nay.

3. **Chọn cột chỉ áp cho màn In**, dùng lại `components/modal/column-customization-modal.vue`.

4. **Đổi tên chỉ ở chữ hiển thị.** Giữ nguyên tên 4 quyền trong seeder và URL
   `/assign/report/meeting-by-employees` — đổi tên quyền là mất sạch gán quyền cho role
   (đúng lỗi đã làm vỡ build `tpe-develop-assign` tuần trước); đổi URL làm chết link đã lưu.

## Hiện trạng code

- BE [`MeetingByEmployeesService::getFilteredQuery()`](../../hrm-api/Modules/Assign/Services/Report/MeetingByEmployeesService.php) lọc cứng 1 dòng `whereIn('meetings.status', Meeting::REPORT_STATUSES)`
- BE đã hỗ trợ sẵn `department_id` / `part_id` / `employee_id`; FE mới chỉ có ô Nhân viên
- `content` + `conclusion` là **cột thật** trên bảng `meetings`, chỉ chưa được `formatMeetingData()` trả ra
- Bảng lồng 4 cấp Công ty → Phòng ban → Nhân viên → **Meeting**; 2 cột mới nằm ở dòng meeting

## Việc phát hiện thêm, ngoài phạm vi

`pages/assign/report/meeting-by-employees/index.vue:508` — `is_department: this.hasAPermission(...) || true`.
`|| true` làm câu kiểm quyền thành vô nghĩa (fail-open, CLAUDE.md cấm). Chưa sửa trong task này,
chờ user quyết.
