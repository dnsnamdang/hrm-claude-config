# Ca ghi nhận lịch sử chấm công — Tóm tắt

> **Spec đầy đủ**: `docs/superpowers/specs/2026-08-29-ca-ghi-nhan-cham-cong-design.md`
> **Plan**: `.plans/ca-ghi-nhan-cham-cong/plan.md` · **Nhánh**: `tpe` (api + client) · **@cuong61n**

## Mục tiêu

Một loại ca làm việc **chỉ để ghi nhận lịch sử chấm công**, phân vào ngày lễ / Chủ nhật:
nhân sự **vẫn chấm công được** trên app và máy chấm công, nhưng **không ảnh hưởng bất kỳ
phép tính nào** (công định mức, lương, đơn phép, tiền cơm, tăng ca) — *"hiểu nó như chưa
từng được phân ca vậy"*. Có ký hiệu **`CC`** trên `/timesheet/timesheet_details` để biết
người đó có chấm công. Logic chấm công giữ nguyên (vẫn phải đứng gần địa điểm hợp lệ).

## Cách làm

Cờ **`working_shifts.is_attendance_only`**. Phân ca vẫn ghi vào `shift_detail_employee_dates`
như mọi ca khác ⇒ **dùng nguyên 2 màn `/shift-detail/general` và `/shift-detail/add`, không
tạo màn mới, không thêm quyền, không thêm menu**. Đổi lại phải chèn điều kiện loại trừ tại
**18 điểm**, gói trong **một scope + một helper duy nhất**.

## 3 phát hiện định hình thiết kế

1. **Luồng chấm công không đọc bảng phân ca.** `getWorkshift()` (`TimesheetService:763`) với
   ngày ≤ hôm nay đọc `timesheet_summaries → timesheet_details`. Mà `timesheet_details` lại là
   đầu vào của toàn bộ phép tính công ⇒ ca này **không được sinh** `timesheet_detail`, và luồng
   chấm công phải có đường tra ca **riêng** (`getAttendanceOnlyShift()`, gọi bổ sung ở 4 điểm).
2. **Có 3 đường sinh `timesheet_details`, chỉ 1 đường đi qua `getWorkshift()`.** Hai đường kia
   (`InsertEmployeeByDateWorkingShift:37` và `ShiftDetailEmployeeDateController:91`) tạo thẳng
   — vá `getWorkshift` là **chưa đủ**.
3. **`timesheets.employee_info_id` chứa `ssn`, không phải id** (`TimekeeperService:193`,
   `FetchAttendanceCommand:207`). Query "có chấm công không" phải join qua `employee_infos.ssn`,
   join thẳng `id` sẽ khớp nhầm người **mà không báo lỗi**.

## Rủi ro đã chấp nhận

**Fail-open** — sót 1 trong 18 điểm là sai số công **âm thầm, không có exception**. Kiểm soát:
(a) một `ShiftDetailEmployeeDate::scopeExcludeAttendanceOnly()` + một `WorkShift::attendanceOnlyIds()`,
không rải điều kiện; (b) **nghiệm thu bằng số**: công định mức + tổng công lương + số suất cơm +
`COUNT(timesheet_details)` của 1 phòng ban 1 tháng phải **y hệt** trước/sau khi phân ca thử;
(c) BE reset mọi hệ số tính công của ca về 0 làm lớp phòng vệ thứ hai.

ⓘ **Bẫy NULL nêu ở bản spec đầu là báo động giả** (kiểm 2026-08-29): `working_shift_id` khai
NOT NULL, 0/428.354 dòng thật là NULL. Cột nullable là `shift_detail_id`, đã nhầm hai cột.
Scope vẫn bọc `whereNull()->orWhereNotIn()` làm phòng vệ nếu schema đổi về sau.

## Quyết định đã chốt

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Bản chất ca | Chỉ mở cổng chấm công — form ẩn khối "Tính công" + "Cài đặt" |
| 2 | Ký hiệu | Ký hiệu chữ **`CC`**, cùng bộ M / VS / P / KLĐ / GV / CT (dùng chung cho màn hình + Excel + bản in) |
| 3 | Bấm vào ô | Vẫn mở popup xem giờ chấm / ảnh / ghi chú; phần công trống |
| 4 | Trùng ca | Chặn — dùng cơ chế **424 "Cảnh báo trùng ca"** sẵn có, miễn phí cả 2 chiều |
| 5 | Điều kiện hiện `CC` | Chỉ khi **có chấm công thật** (phân ca + có bản ghi `timesheets` ngày đó) |
| 6 | Phân quyền | Dùng chung 3 quyền phân ca sẵn có (412/413/414), **không thêm quyền** |
| 7 | Màn phân ca | Dùng nguyên `/shift-detail/general` và `/shift-detail/add`, **không tạo màn mới** |
| 8 | Hướng kiến trúc | Cờ + loại trừ 18 điểm — **hệ quả bắt buộc của #7** (bảng riêng thì phải union 2 bảng ở mọi đường đọc/ghi của 2 màn đó, nhiều việc và rủi ro hơn) |

## Không sửa

Màn phân ca (general / add / edit / modal / lịch sử) · popup chi tiết chấm công · luồng máy
chấm công (Hikvision, ZKTeco vốn không đọc phân ca) · màn `timesheet_details` FE · `WorkShiftService::index()`.
