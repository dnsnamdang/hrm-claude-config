# Plan — Đơn xin nghỉ: chặn trùng thời gian + msg lỗi rõ nghĩa

Nhánh: `tpe` (cả 2 repo). Xem `design.md` cùng thư mục.

## Phase 1 — BE chặn trùng đúng mọi trạng thái còn hiệu lực

- [x] Xác định nguyên nhân: `$absence_status` trong `AttendanceRequest::withValidator()` thiếu `CHO_NSHC_DUYET`
- [x] Loại trừ giả thuyết "gửi qua app": chỉ có 1 route `POST /timesheet/attendance` dùng chung
- [x] Thêm `AttendanceStatus::CHO_NSHC_DUYET` vào `$absence_status` + comment giải thích
- [x] Đổi `message_mobile` thành `"Đã có đơn xin nghỉ trùng thời gian (mã đơn: ...). Vui lòng chọn lại thời gian hoặc huỷ đơn cũ."`
- [x] `php -l` pass
- [x] Verify thực tế: tạo đơn A → duyệt cấp 1 (đơn sang "Chờ NSHC duyệt") → tạo đơn B trùng thời gian, khác loại nghỉ → phải bị chặn

## Phase 2 — FE hiện đúng lý do

- [x] `add.vue`: đặt `<ConfirmAttendance @event="handleEvent" :message="duplicate_attendance_code" />` vào template (trước đó chỉ import + register nên popup không tồn tại trong DOM)
- [x] `add.vue`: `callbackError(error)` lấy `error?.response?.data?.message_mobile`, fallback `"Tạo đơn xin nghỉ thất bại"`
- [x] `_id/index.vue`: truyền `error` vào `callbackError`, toast lấy `message_mobile`, fallback `"Sửa đơn xin nghỉ thất bại"`
- [x] Verify UI: toast báo đúng lý do + popup "Cảnh báo: các đơn xin nghỉ sau đây trùng thời gian" liệt kê mã đơn, bấm dòng mở được đơn trùng

## Phase 3 — Bàn giao

- [x] Kiểm line ending không bị phá (`git diff --stat` chỉ vài dòng)
- [x] Commit 2 repo trên nhánh `tpe` — `hrm-api` b6c25c730, `hrm-client` 21a7b95d4 (CHƯA push)

### Checkpoint — 2026-09-11
Vừa hoàn thành: XONG CẢ 2 MỤC, ĐÃ VERIFY THẬT, ĐÃ COMMIT (`hrm-api` b6c25c730, `hrm-client` 21a7b95d4 trên nhánh `tpe`, CHƯA push).
Cách verify (API :8002 / FE :3005 / DB `hrm_prod_30_3_26`, tài khoản DNS Admin):
1. Tạo đơn A 05/10/2026 08:00→06/10/2026 17:00, loại "Nghỉ kết hôn" → duyệt cấp 1 → đơn sang trạng thái 4 (Chờ NSHC duyệt).
2. Tạo đơn B 05/10 09:00→06/10 12:00, loại "Nghỉ phép" (khác loại, trùng thời gian) → **HTTP 422**, đơn B KHÔNG được tạo, `message_mobile` = "Đã có đơn xin nghỉ trùng thời gian (mã đơn: ...)". Trước khi sửa thì lọt.
3. Trên UI màn Tạo mới: hiện popup "Cảnh báo: các đơn xin nghỉ sau đây trùng thời gian" (bảng STT / Mã đơn / Thời gian) + toast đỏ đúng lý do.
4. Đối chứng ở tầng service: `getListAttendance` với danh sách trạng thái cũ trả rỗng, với danh sách mới trả đúng đơn đang "Chờ NSHC duyệt".
Đã xoá đơn test khỏi DB local sau khi verify.
Đang làm dở: không.
Bước tiếp theo: push nhánh `tpe` + báo QA test lại trên dev; dữ liệu đã lỡ trùng trên prod (13413 / 13426) NSHC tự xử lý.
Blocked:
