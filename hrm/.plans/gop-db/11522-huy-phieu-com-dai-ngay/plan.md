# #11522 — [App quản lý cơm] Không huỷ được phiếu ĐK suất ăn dài ngày / cơm khách dài ngày — @cuong61n

Nguyên nhân (tái hiện trên simulator 19/10/2026):
- Khách dài ngày (type 3): `LTTicket.cancelTicketRequest` chỉ đọc `fromDate`/`guestRegisterRiceTime`, không đọc `guestLongStartDate` → thoát `return false` im lặng, không gọi API ("bấm huỷ không báo gì")
- Suất ăn dài ngày (type 1): app gửi `from_date` = ngày BẮT ĐẦU phiếu; phiếu đang chạy thì BE (`after_or_equal:today`) trả 422 "Không hợp lệ" → app hiện "Có lỗi xảy ra! Vui lòng thử lại sau."

## Phase 1 — App
- [x] `from_date` tính như web (`AddRegisterRiceComponent::showConfirmCancelRegisterRice`): type 2 = giờ ăn khách; type 1/3 = phiếu đã bắt đầu + quá giờ chốt hôm nay → ngày mai, còn lại max(ngày bắt đầu, hôm nay). Giờ chốt: `regular_time_register_employee` (type 1) / `regular_time_register_customer` (type 3, thêm API `getLimitTimeToRegisterCustomer`)
- [x] Báo lỗi đúng câu BE (lỗi theo trường lấy câu đầu); huỷ xong báo "Đã huỷ phiếu từ ngày dd/mm/yyyy"
- [x] Test simulator (local, đã quá giờ chốt): PDKSA dài ngày 01/10–30/11 → huỷ từ 20/10 ✓; khách dài ngày 01/10–30/11 → huỷ từ 20/10 ✓; phiếu bắt đầu 25/10 → huỷ từ 25/10 ✓. Chưa test được case trước giờ chốt (huỷ từ hôm nay) vì test sau 10:20
- Dữ liệu test local: rice_sheet_registrations 2195, 2196, 2197 (TEST11522-*) — đã huỷ
