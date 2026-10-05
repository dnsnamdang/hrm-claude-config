# Task 17 — FE modal đặt phòng — Báo cáo

**Status: HOÀN THÀNH.** Modal Tạo mới/Sửa hoạt động, 2/2 ca smoke xanh (dòng tổng kết thật, không
suy diễn), 2 lệnh grep bắt buộc đều RỖNG.

## File tạo / sửa (chỉ trong `pages/meeting/bookings/`, worktree `phong-hop-client`)

- **Tạo mới**: `pages/meeting/bookings/components/BookingFormModal.vue` — modal form Thêm/Sửa
  phiếu đặt phòng, dựng trên `V2BaseModal` + `unsavedModalMixin` (khuôn `MeetingRoomModal.vue`).
- **Sửa**: `pages/meeting/bookings/index.vue` — thêm nút "Tạo mới" (slot `#actions` của
  `V2BaseDataTable`, KHÔNG gate quyền vì `store()` không gắn `checkPermission` — mọi nhân viên đặt
  phòng được), nối nút "Sửa" sang `BookingFormModal` (trước đó tạm mở modal Xem), thêm
  `selectedFormItem` + `createItem()/handleFormEvent()/handleFormCloseModal()`.
- **Sửa (chỉ comment)**: `pages/meeting/bookings/components/BookingDetailModal.vue` — cập nhật lại
  2 đoạn comment đầu file/prop `isShow` cho khớp thực tế (nút Sửa nay mở `BookingFormModal`, không
  còn "sẽ thay thân modal ở Task 17" nữa). Không đổi hành vi/markup.
- **Tạo mới** (bộ e2e dùng chung): `e2e/tests/meeting/_booking-form-ui.smoke.spec.ts`.

## Đáp ứng yêu cầu brief

1. Trường: Phòng · Ngày · Từ giờ – Đến giờ · Tiêu đề · Nội dung · Chủ trì · Người tham dự · Số
   người dự kiến. KHÔNG có ô "Lặp lại định kỳ" (Phase 5).
2. Select "Phòng họp" lọc qua 2 ô UI-only (Sức chứa tối thiểu, Lọc theo tiện nghi) gọi lại
   `GET meeting/rooms?status=1&capacity_from=&amenity_ids[]=` mỗi khi đổi filter.
3. Dải giờ bận: `GET meeting/room-bookings?meeting_room_id=&date_from=&date_to=` — **1 request**,
   watcher trên `data.meeting_room_id`/`data.date`, có guard chống race (tăng dần
   `busySlotsRequestId`, bỏ response cũ). Chỉ tính status Chờ duyệt/Đã duyệt là "bận" (khớp
   `assertNoOverlap()` BE — Đã duyệt mới thật sự chặn giờ).
4. Lỗi trùng giờ (`errors.start_at` từ response 422) render bằng `V2BaseError` NGAY DƯỚI ô "Từ
   giờ", KHÔNG toast (đã kiểm `.toasted.error` = 0 trong test B).
5. Cảnh báo vượt sức chứa: tính CLIENT-SIDE (so `attendee_count` với capacity của phòng đang chọn
   trong `roomOptions`) — hiện banner vàng `.capacity-warning` NGAY khi gõ, không chờ lưu; không
   chặn Lưu; không sửa số user đã nhập (đã đo `toHaveValue('10')` giữ nguyên sau khi cảnh báo hiện).
6. Lưu thành công: `markFormSaved()` → `$emit('event')` (index.vue gọi `loadData()`) →
   `closeModal()`.

## 2 lệnh grep bắt buộc — cả 2 RỖNG

```
$ grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/bookings/ | grep -v V2Base
(rỗng)
$ grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/bookings/
(rỗng)
```

## Playwright — dòng tổng kết thật

Spec `_booking-form-ui.smoke.spec.ts` (2 ca, `mode: 'serial'`):

```
Running 2 tests using 1 worker

  ✓  1 [chromium] › ... A. Tạo mới không trùng giờ -> dải giờ bận đúng 1 khoảng, cảnh báo vượt sức chứa, bảng tăng đúng 1 dòng (20.1s)
  ✓  2 [chromium] › ... B. Đặt trùng giờ phiếu đã duyệt -> lỗi hiện INLINE đúng dưới ô "Từ giờ", KHÔNG phải toast (21.2s)

  2 passed (44.1s)
```

Chạy lại thêm bộ smoke Task 16 (`_bookings-ui.smoke.spec.ts`) để chắc không phá màn danh sách —
**5 passed (48.5s)**, không "did not run" nào.

## Số đo DOM thật (trích từ test đã chạy xanh, không suy diễn)

- **Test A** (bảng tăng đúng 1 dòng): trước khi mở modal Tạo mới, `table.data-table tbody tr` lọc
  theo phòng test = **1** dòng (phiếu setup qua API). Sau khi Lưu thành công (giờ 11:00–12:00,
  không trùng) → cùng locator = **2** dòng, có đúng 1 dòng chứa tiêu đề vừa tạo.
- **Dải giờ bận** (`c` trong đề bài): mở modal, chọn đúng phòng + ngày mai → `.busy-slot-item`
  đếm được **đúng 1** phần tử (khớp 1 phiếu Đã duyệt 09:00–10:00 có sẵn), nội dung chứa "09:00",
  "10:00", "Đã duyệt". Ở test B (sau khi Test A đã tạo thêm 1 phiếu Đã duyệt 11:00–12:00), cùng
  locator đếm được **đúng 2** phần tử — chứng minh watcher gọi lại đúng khi dữ liệu đổi.
- **Cảnh báo vượt sức chứa**: phòng test `capacity=5`, nhập "Số người dự kiến" = 10 →
  `.capacity-warning` chuyển visible NGAY (không cần lưu), chứa cả "10" và "5"; ô nhập vẫn giữ
  nguyên giá trị `"10"` (`toHaveValue('10')`) — không bị code tự sửa/kéo về max. Giảm về 3 (≤
  capacity) → `.capacity-warning` biến mất (`toBeHidden`).
- **Lỗi trùng giờ hiện đúng dưới ô "Từ giờ"** (`b` trong đề bài): đặt phiếu mới 09:30–10:30 (chồng
  lấn phiếu setup 09:00–10:00 "Đã duyệt") → bấm Lưu:
  - `fieldBlock(modal, 'Từ giờ').locator('.v2-error')` **visible**, nội dung chứa tên phiếu đang
    chiếm giờ (message BE: `Phòng đã có cuộc họp "<title>" lúc HH:mm - HH:mm ngày dd/mm/yyyy`).
  - `fieldBlock(modal, 'Đến giờ').locator('.v2-error')` **count = 0** (lỗi không lem sang field
    khác).
  - `page.locator('.toasted.error')` **count = 0** — xác nhận KHÔNG phải toast.
  - Modal vẫn mở sau Lưu thất bại; bảng vẫn giữ nguyên 2 dòng (không tăng).

## Dữ liệu test — dọn sạch

Mã theo hậu tố `Date.now()` (`E2E_BKFORM_<ts>`), dọn ở `afterAll` (best-effort, chạy cả khi ca
fail): xoá mọi `meeting_room_bookings` thuộc phòng test qua SQL trực tiếp (không có API xoá
booking, chỉ Duyệt/Từ chối/Hủy), rồi xoá phòng qua `DELETE /meeting/rooms/{id}`. Đã xác minh sau
khi chạy xong: `GET meeting/rooms` không còn phòng nào tên chứa "E2E"/"Debug" — sạch. (Có 2 phòng
debug thủ công `1368/1369/1370` phát sinh trong lúc tôi tự debug bằng Playwright MCP để tìm bug
kiểu dữ liệu bên dưới — đã xoá thủ công ngay sau đó, xác minh lại bằng API cũng KHÔNG còn.)

## Bug thật đã bắt + sửa TRƯỚC khi báo xong (đúng yêu cầu "tái hiện lỗi trước khi sửa")

1. **`V2BaseSelectInModal` trả `meeting_room_id` dạng CHUỖI** (`"1369"`) dù `id` gốc trong
   `roomOptions` là số (`1369`) — so `===` trực tiếp luôn `false`. Hậu quả kép: (a) `roomOptions`
   tưởng phòng vừa chọn KHÔNG có trong list nên tự chèn thêm 1 option "khoá" trùng tên
   (`Phòng #1369`, `capacity: 0`) đè lên chính lựa chọn vừa chọn; (b) `selectedRoomCapacity` khớp
   nhầm vào option giả đó → luôn ra `0` → cảnh báo vượt sức chứa KHÔNG BAO GIỜ hiện. Tái hiện bằng
   cách soi trực tiếp state Vue (`vm.data`/`vm.roomOptions`) qua Playwright, thấy rõ 2 option cùng
   id khác kiểu. Sửa bằng so sánh `String(opt.id) === String(selectedId)` (đúng khuôn
   `utils/select2LockedOption.js` đã dùng cho đúng tình huống này).
2. **`Escape` trong ô giờ/ngày đóng LUÔN CẢ MODAL** — field nằm trong `<b-modal>`
   (`V2BaseModal` không tắt `no-close-on-esc`), nhấn Escape để đóng popup vue2-datepicker bị
   bootstrap-vue bắt và đóng cả modal cha, khiến bước "Lưu" sau đó không tìm thấy nút (modal đã
   biến mất). Đây là gotcha đã có trong memory dự án ("Modal + mốc chờ e2e hrm-client"). Sửa ở
   SPEC (không phải component): thay `Escape` bằng click ra khối `.section-header` trung lập trong
   modal để đóng popup mà không đụng phím tắt của modal.

## Concerns / ghi chú cho reviewer

- `meeting/rooms/form-options` và `meeting/rooms` (dùng để nạp tiện nghi + danh sách phòng trong
  modal) đều gắn `checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp` ở BE — nhân
  viên KHÔNG có quyền đó (dù `store()` phiếu đặt phòng không yêu cầu quyền gì) sẽ nhận 403 khi mở
  modal, và ô "Phòng họp" sẽ KHÔNG có option nào để chọn (bắt lỗi im lặng, giống hệt
  `loadRoomOptions()` đã có sẵn ở `index.vue` từ Task 16). Đây là gap kế thừa từ thiết kế phân
  quyền Task 6, không thuộc phạm vi sửa của Task 17 (chỉ đụng `pages/meeting/bookings/`) — nêu ra
  để phase sau cân nhắc có nên nới quyền đọc danh mục phòng cho mọi nhân viên hay không.
- Khi phòng đang chọn (lúc Sửa) không khớp bộ lọc sức chứa/tiện nghi hiện tại, tôi chèn thêm 1
  option "khoá" (🔒) để KHÔNG mất lựa chọn — nhưng `capacity` của option chèn thêm này mặc định
  `0` vì `DetailMeetingRoomBookingResource` không trả `capacity` của phòng. Hệ quả: nếu đang Sửa 1
  phiếu mà phòng bị lọc khỏi danh sách, cảnh báo vượt sức chứa sẽ tạm không tính đúng cho tới khi
  user đổi bộ lọc để phòng đó xuất hiện lại bình thường (capacity thật). Edge case hiếm, chưa viết
  ca test riêng.
- Ca smoke bắt buộc theo brief chỉ có (a)/(b)/(c); tôi gộp phần đo cảnh báo vượt sức chứa (yêu cầu
  #5) vào chung Test A để tận dụng cùng 1 phiên mở modal — không tách thành ca riêng.
