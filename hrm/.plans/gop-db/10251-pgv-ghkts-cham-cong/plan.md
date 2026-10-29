# #10251 — [App] Fix lỗi PGV, gia hạn - kết thúc sớm ở phân hệ chấm công — @cuong61n

3 ý của task (kiểm 19/10/2026):
- [x] (1) Trùng giờ PGV nhưng popup ghi "Lỗi tạo đơn xin nghỉ" — ĐÃ SỬA từ trước (TuJobs 22/04): tiêu đề "Lỗi tạo phiếu giao việc" + câu BE (đã kiểm ở #10195)
- [x] (2) Từ chối PGV, xem lại không thấy lý do — ĐÃ SỬA từ trước: danh sách + màn chi tiết đều hiện "Lý do từ chối" (test PGV-28860 "làm lại" ✓)
- [x] (3) Bộ lọc như web (sheet "Chấm công(api)"):
  - Phiếu giao việc: app đã đủ các ô của web `/timesheet/jobassignment` (Mã phiếu, Phòng ban, Trạng thái, Họ tên/Mã NV, TG bắt đầu Từ/Đến, Ngày tạo Từ/Đến) + Công ty ✓
  - Gia hạn/Kết thúc công tác: THIẾU "Người cập nhật" (web có) → thêm `SelectInput` ô Người cập nhật (danh sách `getEmployeesForFilter`, id = employees.id khớp `updated_by`; nạp khi mở bộ lọc lần đầu), đặt sau Loại phiếu như web. Bloc/API đã có sẵn updatedBy
- [x] Test simulator: Người cập nhật tìm "11010069" → "Thiều Quốc Đạt - 11010069" → `updated_by=341`, 5 phiếu = khớp API/DB ✓
