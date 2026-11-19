# #10155 — [App Chấm công] Phiếu giao việc + phiếu đi CT: lỗi bộ lọc — @cuong61n

- [x] (1) PGV không lọc được người được giao việc — ĐÃ CHẠY: ô "Họ tên / Mã nhân viên" gửi `employee` (LIKE mã/tên); test app "12510967" → phiếu của Nguyễn Đình Vũ ✓
- [x] (2) Phiếu đi CT lọc theo nhân viên đi CT — app có ô "Người đi công tác" nhưng KHÔNG có tác dụng (19/10/2026):
  - BE `BusinessTripAssignService::index` chỉ đọc `employee` (chữ), bỏ qua `employee_id` app gửi → thêm lọc `employee_id` = business_trip_employees.employee_id (employee_infos.id) bằng whereExists
  - App bản Tân Phát lấy danh sách từ getEmployeesForFilter (id = employees.id) → thêm `employee_info_id` vào `ListEmployeeInfo` (mặc định 0), bloc gửi employeeInfoId nếu có, không có thì id (Thành An: list_employee_infos đã là employee_infos.id)
  - Test: API employee_id=6 → 6 phiếu khớp DB; app chọn DNS Admin → employee_id=6 → PCT10395, PCT10029, PCT4514… ✓
- [x] Sửa kèm lỗi của chính mình ở #10195: hàm `_canDuyetPhieuCongTac` chèn giữa `@RoutePage()` và class TongQuanChamCongPage → build_runner bỏ mất TongQuanChamCongRoute. Đã chuyển hàm lên trên annotation, sinh lại code, app_router.gr.dart không đổi so với git ✓
