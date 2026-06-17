# Plan — Fix lỗi "Illegal operator and value combination" khi tạo phiếu tra soát công

API: `POST /timesheet/request-update-working` → `RequestUpdateTimeSheetController@store` → `CreateUpdateTimeSheetRequest`

Nguyên nhân: closure `$validator->after()` chạy query check trùng lịch với `where('request_start_at', '<=', null)` khi field bị null → Laravel ném `InvalidArgumentException`.

## Phase 1 — Fix
- [x] BE: Trong `CreateUpdateTimeSheetRequest::withValidator()`, guard early-return query check trùng khi thiếu `employee_id` / `working_date` / `request_start_at` / `request_end_at`; tách logic gom lỗi thành `collectErrorMessages()` để cả 2 nhánh đều trả lỗi validate đúng

### Checkpoint — 2026-05-29
Vừa hoàn thành: fix lỗi Illegal operator and value combination ở CreateUpdateTimeSheetRequest.php
Đang làm dở: không
Bước tiếp theo: user test lại API POST /timesheet/request-update-working với payload thiếu request_start_at/request_end_at → phải trả lỗi validate "Bắt buộc nhập" thay vì 500
Blocked:

## Phase 2 — Fix app không báo trùng (422) do định dạng giờ ISO

Nguyên nhân: cột `request_start_at`/`request_end_at` kiểu `TIME`. App gửi ISO datetime (`2026-05-30T08:30:00.000`), MySQL không ép được sang TIME → query check trùng trả 0 dòng → bỏ qua lỗi trùng. Web gửi `H:i` thì parse được nên báo 422 đúng.

- [x] BE: Thêm `prepareForValidation()` ở `CreateUpdateTimeSheetRequest` chuẩn hoá `request_start_at`/`request_end_at` về `H:i:s` bằng `Carbon::parse()` (xử lý cả ISO datetime lẫn `H:i`) → query check trùng + `formatTime` ở store nhận đúng định dạng

### Checkpoint — 2026-05-30
Vừa hoàn thành: thêm prepareForValidation chuẩn hoá giờ về H:i:s
Đang làm dở: không
Bước tiếp theo: user test lại trên APP với payload trùng giờ phiếu đã có → phải trả 422 "Đã có phiếu tra soát công trong khoảng thời gian này"
Blocked:
