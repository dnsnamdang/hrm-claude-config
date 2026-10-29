# #11323 — [App Chấm công] Đơn xin nghỉ: loại nghỉ mặc định là "Nghỉ kết hôn" — @cuong61n

Nguyên nhân: `GiayBaoVangMatBloc._onInitLoad` (tạo mới) chọn sẵn `leaveTypes.elementAtOrNull(2)` = phần tử thứ 3 của danh sách = Nghỉ kết hôn.
- [x] Bỏ chọn sẵn: loại nghỉ / tỷ lệ hưởng lương để trống, `leaveTypeId` giữ mặc định -1 (19/10/2026)
- [x] Bắt buộc chọn: BE `AttendanceRequest` đã trả "Bắt buộc chọn" vào `leave_type_id` khi không có loại nghỉ, app đã map lỗi vào ô Loại nghỉ → không phải sửa BE
- [x] Chọn loại nghỉ thì xoá luôn lỗi "Bắt buộc chọn" của lần gửi trước (`_onLoaiNghiSelected`)
- [x] Test simulator (flavor tpeLocal, 19/10/2026): mở Xin nghỉ → Loại nghỉ trống "Chọn loại nghỉ" ✓; gửi khi chưa chọn → "Bắt buộc chọn" dưới ô ✓; chọn Nghỉ phép → lỗi biến mất ✓; gửi khi thiếu ngày/lý do → lỗi ở các ô đó, Loại nghỉ không lỗi ✓. Màn sửa đơn cũ không đổi (lấy loại nghỉ từ đơn)
