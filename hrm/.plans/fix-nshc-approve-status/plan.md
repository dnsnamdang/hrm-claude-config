# Fix — NSHC duyệt đơn xin nghỉ không đổi trạng thái

## Bối cảnh
- Endpoint `POST /timesheet/.../approve` (`AttendanceController::storeApprove`) xử lý cả 2 cấp duyệt (Quản lý + NSHC).
- Đơn có `leave_type.need_nshc_approve = 1`: Quản lý duyệt → `Chờ NSHC duyệt (4)`. NSHC duyệt → phải lên `Đã duyệt (2)`.
- Bug: đoạn ép `need_nshc_approve` không loại trừ đơn đang ở `CHO_NSHC_DUYET (4)` → NSHC bấm duyệt bị set Approved(2) rồi ép ngược về 4 → trạng thái không đổi.

## Phase 1 — Fix BE
- [x] `AttendanceController::storeApprove`: chỉ ép sang `CHO_NSHC_DUYET` khi đơn CHƯA ở trạng thái `CHO_NSHC_DUYET` (tức là lần duyệt cấp 1 từ `SendApprove`). Khi đơn đã ở `CHO_NSHC_DUYET`, NSHC duyệt → giữ `Approved(2)` để recalc công chạy.

## Phase 2 — Ẩn nút "TP duyệt" thừa khi đơn đã chờ NSHC (@cuong61n, 19/11/2026)
- Hiện trạng: người NSHC mở đơn "Chờ NSHC duyệt" (màn Duyệt giấy báo vắng mặt) thấy cả "TP duyệt" lẫn "NSHC duyệt" vì BE `can_approve` cố ý trả true cho NSHC ở trạng thái 4 (dùng chung nút Duyệt ở danh sách).
- [x] 19/11/2026 FE `pages/timesheet/attendance/_id/approve.vue`: nút "TP duyệt" thêm điều kiện `attendance_status != 4`. BE không đổi (luồng duyệt vốn đúng). Chưa kiểm trên trình duyệt — chờ test.

## Verify
- [ ] NSHC duyệt đơn ở trạng thái "Chờ NSHC duyệt" → đơn chuyển "Đã duyệt", command `calc:employee_timesheet` được queue.
- [ ] Quản lý duyệt đơn `need_nshc_approve=1` ở "Gửi duyệt" → vẫn chuyển đúng "Chờ NSHC duyệt".
- [ ] Quản lý duyệt đơn `need_nshc_approve=0` → vẫn "Đã duyệt" như cũ.
