# Fix: Serial dư vượt số lượng thiết bị — chặn lại ở luồng Duyệt kết quả

**Owner:** @junfoke
**Ngày:** 2026-08-24
**Module:** CustomerCare — Duyệt kết quả giao việc (WrApproveResults) / Serial

## Bối cảnh / Triệu chứng
Màn **Yêu cầu SC-BH** (Warranty Repair Request) khi chọn thiết bị (vd máy kiểm tra phanh SL-580,
product_id 8739) báo **"Thêm số lượng cho thiết bị"** và không cho chọn.

Nguyên nhân: FE chặn khi `qty < serials.length` (đúng logic). Thiết bị có **qty = 1 nhưng 2–3 serial
đang sử dụng** → dữ liệu serial bị dư. Lỗi diện rộng (nhiều KH, riêng product 8739 có hàng chục KH bị,
1 KH tới 3 serial).

## Điều tra nguồn serial dư (bằng chứng query trên prod)
- KHÔNG từ phiếu xuất, KHÔNG từ BBGN (0/27 khớp bảng `handover_acceptance_product_record_serials`).
- 27 serial dư là `tp`, `invoiceable=NULL`, `parent_id=NULL`, do 5 nhân viên tạo tay.
- Phân loại: **17 nhập tay màn "Danh mục serial thiết bị"** (`SerialController::addSerial`) +
  **10 từ nhập kết quả PGV** (`WrAssignTask::syncProduct` nhánh không có `serial_id`).

## Nguyên nhân gốc
Chốt kiểm "serial ≤ số lượng thiết bị" ở luồng **Duyệt kết quả** (`checkValidateSerial`) **đã bị
comment tắt dần qua 3 đợt**:
- 2024-07-01 (f0d2e63 — nguyentienvu4897): tắt nhánh cảnh báo TH1 (`count_serial_is_null == 0`).
- 2025-07-28 (86e23ba — dnsnamdang): tắt nốt nhánh TH2 → hàm luôn `return [true]`.
- 2026-01-26 (5afac62 — nguyentrancu97, "fix"): comment 3 nơi gọi (`store`/`update`/`approve`) + dọn xác.

Suy luận vì sao tắt (message commit không ghi): chốt cũ so sánh dùng `count_serial_is_null` không clamp,
khi thiết bị đã dư serial sẵn dễ chặn nhầm phiếu hợp lệ → dev tắt cho qua thay vì sửa → data càng dư.

## Giải pháp (đã làm)
Bật lại `checkValidateSerial` + viết lại phần thân cho chuẩn TH1/TH2 và **không chặn nhầm**:
- Chỉ đếm serial **thêm mới thật sự** (khác rỗng, không trùng, chưa nằm trong serial đang dùng của
  thiết bị). Dòng có `serial_id` (ĐỔI serial) đã bị `$arr` loại sẵn → không tính.
- `free_slots = qty - số serial đang dùng`, **clamp về 0** nếu âm (data dư sẵn) → không sai điều kiện.
- **TH1** (`free_slots == 0` mà vẫn thêm mới): chặn, báo "…đã đủ, vào Danh mục serial ngừng bớt 1 serial cũ…".
- **TH2** (`countThêmMới > free_slots`): chặn, báo "…số serial nhập thêm vượt số chỗ còn lại…".
- Bật lại 2 nơi gọi `store` + `update`.

## Đặc điểm quan trọng (an toàn khi bật lại)
Chốt **chỉ chặn khi user thực sự nhập serial MỚI** lên thiết bị đã đủ. Nếu phiếu không thêm serial mới
(chọn serial có sẵn / không đụng serial) thì `countThêmMới = 0` → KHÔNG chặn, kể cả thiết bị đang dư
serial. Nhờ vậy bật lại không làm kẹt các phiếu hợp lệ như bản cũ.

## Việc còn lại (chưa làm — cần team quyết)
1. **Dọn data prod**: rà mọi (product+customer) có `serial active > exported_qty`, tắt bớt serial dư về
   `status=2` (ưu tiên giữ serial gắn phiếu xuất). Chỉ soạn query + script, KHÔNG tự chạy.
2. **Vá nguồn còn lại**: 2 luồng nhập tay (`SerialController::addSerial`) và `WrAssignTask::syncProduct`
   nhánh no-serial_id cũng nên đối chiếu tổng serial active trên DB (gom 1 helper chung), để bịt tận gốc.

## File thay đổi
- `app/Http/Controllers/Customercare/WrApproveResultsController.php`
  - `checkValidateSerial()` — bật lại + viết chuẩn TH1/TH2.
  - `store()`, `update()` — bật lại lời gọi `checkValidateSerial`.
