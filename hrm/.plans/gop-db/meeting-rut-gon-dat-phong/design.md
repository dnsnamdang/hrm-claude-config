# Rút gọn đường đặt phòng khi tạo meeting (app + web)

Người phụ trách: @namdangit · Mở 01/11/2026 · Nguồn: đánh giá phân hệ Meeting mobile (mục 1 "đặt phòng phải đi đường vòng").

## Vấn đề
Luật hiện tại (giữ nguyên): cuộc họp phải **Lên lịch** mới đặt được phòng (`can_book_room`, bản nháp còn đổi giờ).
Đường đi thực tế:
- App: Tạo meeting → Hub → Lên lịch → xác nhận → Thông tin chung → Sửa → mở mục Thời gian, địa điểm → Đăng ký phòng → Chọn phòng → Gửi (~8–10 bấm). Lúc điền form không biết giờ đó còn phòng.
- Web: Lưu và Lên lịch → về danh sách → mở lại cuộc họp → Sửa → Đăng ký phòng → popup.

## Đã chốt với user (01/11/2026)
- Làm cả 3 phần A + B + C, **cả app lẫn web**.
- **A — Hỏi đặt phòng ngay sau Lên lịch**: Lên lịch thành công + chưa có phòng + `can_book_room` → hộp
  "Đặt phòng cho cuộc họp này?" [Đặt phòng] [Để sau] → mở thẳng form/popup đặt phòng (cuộc họp điền sẵn).
  Web: sau khi đặt xong / bấm Để sau mới về danh sách như cũ (ngoại lệ "thao tác chưa kết thúc luồng").
- **B — Nút Đăng ký phòng ở màn xem**: chưa có phòng + được đặt → hiện ngay ở Hub (app) / màn Xem (web),
  không bắt vào Sửa.
- **C — Xem phòng trống + chọn phòng DỰ KIẾN ngay trên form tạo**: ô Phòng họp hiện "Còn N phòng trống khung giờ
  này" (API `v1/meeting/rooms/availability`, tự cập nhật khi đổi giờ), bấm mở danh sách để chọn phòng dự kiến.
  Phòng dự kiến **chưa giữ chỗ**, không lưu BE — chỉ nhớ trong lượt thao tác đó; tới bước A form đặt phòng
  mở với phòng đó chọn sẵn. Thoát ra là mất.

## Không làm
- Không đổi luật "Lên lịch mới giữ phòng", không đổi BE, không migration.
- Không đổi luồng của màn "Đăng ký phòng họp" độc lập.

## Phạm vi code (dự kiến)
- TPE_APP `develop`: `meeting_hub_page.dart` (A, B), `meeting_rooms/meeting_room_box.dart` (C hiển thị + nút B),
  `meeting_general_page.dart` (truyền phòng dự kiến), `meeting_create.dart` (giữ phòng dự kiến trong lượt tạo),
  `meeting_room_booking_form_page.dart` đã có `roomId` → dùng lại.
- hrm-client `gop_db`: `pages/assign/meeting/components/GeneralInfo.vue` (C, B ở chế độ xem),
  `pages/assign/meeting/create.vue` + `_id/edit.vue` (A sau Lưu và Lên lịch),
  `pages/meeting/bookings/components/BookingFormModal.vue` (thêm prop tuỳ chọn `presetRoomId` — component
  dùng chung với màn Đăng ký phòng họp, không truyền thì như cũ).

## Kiểm
- App: bấm thử simulator tpeDev (A/B/C, phòng tự duyệt + phòng cần duyệt, họp Online).
- Web: Playwright đo DOM (hộp hỏi, nút ở màn xem, số phòng trống đổi theo giờ, popup chọn sẵn phòng); cập nhật spec e2e meeting (không tự chạy cả bộ — chỉ khi user yêu cầu).
