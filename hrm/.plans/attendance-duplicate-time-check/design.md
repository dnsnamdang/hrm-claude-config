# Đơn xin nghỉ — chặn trùng thời gian + thông báo lỗi rõ nghĩa

**Người phụ trách:** @junfoke
**Nhánh:** `tpe` (cả `hrm-api` và `hrm-client`) — user chốt làm thẳng trên `tpe`
**Ngày:** 2026-09-11

## Hiện tượng QA báo

1. Có nhân viên nộp được **2 đơn xin nghỉ cùng khoảng thời gian, khác loại nghỉ**
   (đơn 13413 "Nghỉ ốm hưởng BHXH" 10/09 07:40→14/09 18:59 và đơn 13426 "Nghỉ phép"
   11/09 07:49→14/09 19:59, cả hai đang "Chờ NSHC duyệt").
2. Tạo 2 phiếu trùng thời gian trên web thì bị chặn, nhưng chỉ hiện toast
   **"Tạo đơn xin nghỉ thất bại"**, không nói lý do là trùng thời gian.

## Nguyên nhân

### (1) Bỏ sót trạng thái "Chờ NSHC duyệt" khi dò trùng

`AttendanceRequest::withValidator()` dò đơn trùng qua `getListAttendance(...)` với danh sách
trạng thái `[Approved(2), SendApprove(1), Creating(0)]` — **thiếu `CHO_NSHC_DUYET(4)`**.

Vòng duyệt NSHC được thêm sau (commit `3b58903b4`, 29/05/2024) mà không cập nhật danh sách này.
Hệ quả: đơn đã qua duyệt cấp 1, đang chờ NSHC duyệt thì **vô hình** với bộ dò trùng → nộp được
đơn thứ 2 trùng thời gian. Khớp đúng ảnh QA (cả 2 đơn đều ở trạng thái "Chờ NSHC duyệt").

**Giả thuyết "gửi đơn qua app" là SAI**: app và web dùng chung đúng 1 endpoint
`POST /timesheet/attendance` (`Modules/Timesheet/Routes/api.php`), không có API riêng cho mobile,
nên cùng chạy qua `AttendanceRequest`.

Lưu ý thêm: bộ dò trùng truyền `$absence_type = null` nên **không phân biệt loại nghỉ** — lỗi này
làm lọt cả trường hợp trùng cùng loại nghỉ, không riêng khác loại.

### (2) Popup cảnh báo trùng không bao giờ hiện ở màn Tạo mới

BE đã trả đủ dữ liệu (`errors.duplicate_attendance_code` = danh sách đơn trùng, HTTP 422) và
`pages/timesheet/attendance/add.vue` cũng gọi `this.$bvModal.show('modal-warning')`.
Nhưng component `ConfirmAttendance` (chứa `b-modal id="modal-warning"`) **chỉ được import và
đăng ký, không hề đặt trong template** của `add.vue` — trong khi `_id/index.vue` và
`_id/approve.vue` đều có thẻ này. Modal không tồn tại trong DOM → lệnh `show` im lặng không làm gì
→ user chỉ còn thấy toast chung chung của `callbackError`.

Thêm nữa, `callbackError` khai báo không nhận tham số nên dù BE trả `message_mobile`
("Đã bị trùng thời gian xin nghỉ trước đó") thì toast vẫn cứng câu "Tạo đơn xin nghỉ thất bại".

## Cách sửa

| Nơi | Sửa gì |
| --- | --- |
| `hrm-api` · `Modules/Timesheet/Http/Requests/AttendanceRequest.php` | Thêm `AttendanceStatus::CHO_NSHC_DUYET` vào `$absence_status` của bộ dò trùng. Đổi `message_mobile` thành câu có mã đơn trùng. |
| `hrm-client` · `pages/timesheet/attendance/add.vue` | Đặt `<ConfirmAttendance />` vào template; `callbackError(error)` lấy `message_mobile` làm nội dung toast. |
| `hrm-client` · `pages/timesheet/attendance/_id/index.vue` | Cùng cách xử lý toast cho màn Sửa (truyền `error` vào `callbackError`). |

**Giữ nguyên `Rejected(3)`** ngoài danh sách — đơn đã bị từ chối không chiếm chỗ.

**Không đổi contract API**: `message` vẫn là `"fails"`, chỉ làm giàu `message_mobile` (trường vốn
đã dành cho việc hiển thị lý do). App mobile hưởng lợi luôn mà không cần sửa.

## Ngoài phạm vi (ghi lại để theo dõi)

- `getNumberOfDaysOff*` chỉ đếm đơn `Approved` → số ngày nghỉ đã dùng **chưa tính** đơn đang
  "Chờ NSHC duyệt"/"Gửi duyệt". Là vấn đề riêng về quota, không thuộc issue này.
- Dữ liệu đã lỡ trùng trên production (vd 13413 / 13426) cần NSHC tự xử lý — bản vá chỉ chặn từ
  nay, không đụng dữ liệu cũ.
