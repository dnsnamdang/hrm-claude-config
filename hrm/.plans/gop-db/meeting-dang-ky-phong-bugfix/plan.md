# Sửa popup "Đăng ký phòng họp" — danh sách phòng trống + lỗi "thời điểm đã qua" — @cuong61n

Nhánh `gop_db` (worktree gop_db-client). Khách (chị Nguyễn Lệ) báo 13/11/2026.

- [x] 13/11 Danh sách "Phòng còn trống" chỉ hiện 5 phòng dù còn nhiều hơn → bỏ `.slice(0,5)` ở `BookingFormModal.vue` (`freeRoomSuggestions`), danh sách cuộn `max-height: 320px`. Chờ test.
- [x] 13/11 Sửa giờ cuộc họp (chưa lưu) rồi bấm Đăng ký phòng → lưu báo "Không thể đặt phòng cho thời điểm đã qua": popup hiện giờ trên form nhưng BE `assign-meeting` kiểm theo giờ đã lưu trong DB (giờ cũ, đã qua). Fix: `GeneralInfo.openRoomBookingModal` chặn + toast "Thời gian cuộc họp đã thay đổi nhưng chưa lưu. Vui lòng lưu cuộc họp trước khi đăng ký phòng." khi form lệch `savedSchedule`. Chờ test.
- [ ] (gợi ý, chưa làm) API `meeting/rooms/availability` mất ~2,1s với 14 phòng — nên đo query BE để rút ngắn.

- [x] 13/11 Đã thử thêm thanh tải nuxt khi nạp phòng trống nhưng user yêu cầu bỏ → đã gỡ, không còn thay đổi ở phần loading.
