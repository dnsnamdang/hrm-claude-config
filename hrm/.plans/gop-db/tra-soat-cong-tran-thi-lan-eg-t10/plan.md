# Tra soát công T10/2026 — Trần Thị Lan (EG_KD2, 92411109) — @cuong61n

Nguồn: tin nhắn hỗ trợ 05/11/2026 10:53 — "2 ngày 19/10 và 24/10 đều chấm 17h hơn, 1 ngày ra 0, 1 ngày ra 0.5 (KLD), không có đơn nghỉ / đề nghị tra soát công".

## Phase 1 — Điều tra (chỉ đọc PROD, không sửa dữ liệu)

- [x] Tra dữ liệu chấm công PROD (DB `hrm_erp_gop`, `timesheets` theo ssn 92411109) — 05/11/2026
  - 19/10 (T2, ca 61 "Ca Kinh doanh" 08:00–17:00): chỉ có 1 lượt quẹt máy lúc **17:54** (máy conn 36), không có lượt buổi sáng.
  - 24/10 (T7, ca 65 "Ca Kinh doanh_HN_Thứ 7" 08:00–11:30): chỉ có 1 lượt lúc **17:02**, không có lượt buổi sáng.
  - Máy conn 36 sáng 2 ngày đó vẫn chạy bình thường (19/10: 25 lượt quẹt buổi sáng, 24/10: 4 lượt) → không phải lỗi máy/lỗi hút dữ liệu.
  - Không có đơn tra soát công cho 19/10, 24/10 (chỉ có 03/10, 26/10 đã duyệt và 03/11 đang chờ), không có đơn nghỉ.
- [x] Đối chiếu cấu hình ca + code tính công (`TimesheetSummaryService` ~dòng 640–700, bản đang chạy PROD `bde416d7b`) — 05/11/2026
  - Cả 2 ca: **chỉ bắt buộc chấm VÀO** (has_time_check_out = 0), khung nhận chấm vào ca 61: 05:30–14:00, ca 65: 05:30–10:00. Lượt 17h hơn nằm ngoài khung chấm vào → coi là chỉ có chấm ra, **không chấm vào**.
  - Phạt "không chấm vào": ca 61 trừ 1 công → 19/10 còn **0** (KLD); ca 65 trừ 0,5 công → 24/10 còn **0,5**. Hai số khác nhau là do mức phạt cấu hình khác nhau ở 2 ca, không phải do lệch dữ liệu.
  - Kết luận: hệ thống tính **đúng theo cấu hình**, không có lỗi code. Muốn được công thì NV làm **đề nghị tra soát công** 2 ngày đó (bổ sung giờ vào), duyệt xong hệ thống tự tính lại.
- [x] Trả lời người hỏi — 05/11/2026 (đã soạn nội dung trả lời)

- [x] Chỉ ra nơi cấu hình mức trừ công — 05/11/2026: Danh mục ca làm việc → sửa ca → ô tích "Nếu không có giờ vào thì bị trừ công" + Giờ công / Ngày công (`working_shifts.penalty_notime_checkin_hour/_day`, form `pages/timesheet/timeworking/add-working-shift/_id/index.vue` ~dòng 760–816). Ca 61: 8 giờ / 1 công (sửa lần cuối 23/05/2025); ca 65: 3,5 giờ / 0,5 công (sửa lần cuối 28/04/2025) — cả 2 do Đỗ Thị Tố Uyên (92311091) cập nhật.

Trạng thái: xong, không đổi code / dữ liệu.
