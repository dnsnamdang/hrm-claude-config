# Task 24 — Báo cáo: gom bộ e2e chính thức Phase 3 + rà ca lạc hậu

## Status
ĐANG CHỜ kết quả chạy verify (2 lệnh bắt buộc) — cập nhật ngay khi có.

## Việc đã làm

### 1. Gom bộ UI chính thức cho Phase 3
- Tạo mới: `e2e/tests/meeting/meeting-room-board.spec.ts` — copy nguyên văn nội dung của
  `_room-board-ui.smoke.spec.ts`, chỉ sửa phần comment đầu file (mô tả lại là bộ chính thức Phase 3,
  liệt kê đủ 11 nhóm A-K, sửa lệnh chạy mẫu trỏ sang tên file mới). KHÔNG sửa bất kỳ logic test nào.
- Xoá: `e2e/tests/meeting/_room-board-ui.smoke.spec.ts`.
- Giữ nguyên: `e2e/tests/meeting/_auth-smoke.spec.ts` (theo yêu cầu brief).

**Ca PORT sang (toàn bộ 18/18 ca của smoke file — KHÔNG bỏ ca nào):**

| Nhóm | Ca | Nội dung |
|---|---|---|
| A (Task 21 + fix Task 22) | A1 | Khối 14:00-15:30 đúng mép cột + đúng 3 ô rộng |
| | A2 | Phiếu qua đêm có dấu tiếp diễn, bắt đầu mép trái lưới |
| | A3 | Khung giờ tự nới khi có phiếu ngoài 07:00-20:00 |
| | A4 | Phiếu lệch phút 14:15-15:45 hiện đủ 4 ô, không bị `Math.round()` làm tròn vào trong (fix round 1) |
| B | B1 | Bấm ô trống -> modal đặt phòng điền sẵn đúng phòng/ngày/giờ |
| C | C1 | Bấm khối phiếu -> modal chi tiết đúng mã |
| D | D1 | `?room_id=&date=` lọc đúng 1 dòng phòng, đúng ngày |
| E (Task 22) | E1 | Tab Theo tuần: chọn phòng -> đúng 1 sự kiện; Tuần trước/Tuần sau đúng số |
| | E2 | Tab Theo tuần với phòng khác công ty -> 403 tử tế hoặc load được, không trắng màn |
| F (Task 22) | F1 | Thẻ trạng thái: phòng đang có phiếu Đã duyệt -> "Đang họp đến HH:mm" |
| | F2 | Thẻ trạng thái: phòng không có phiếu -> "Đang trống" |
| G (Task 22) | G1 | Chuyển 3 tab qua lại -> Theo ngày vẫn giữ TEST_DATE |
| | G2 | Chuyển tab -> Theo tuần vẫn giữ Phòng đã chọn + dữ liệu đúng |
| H (Task 22) | H1 | `clock.install()` tua 65s ảo: polling status-board còn chạy khi ở màn, dừng hẳn sau khi rời màn (clearInterval) |
| I (Task 23) | I1 | Menu hub "Quản lý phòng họp" có đúng 3 mục, "Tình trạng phòng họp" href đúng + bấm vào lưới render thật |
| J (Task 23) | J1 | Nút "Xem lịch phòng" ở `/meeting/rooms` -> URL đúng room_id+date hôm nay, board lọc sẵn đúng phòng |
| K (Task 23) | K1 | Tài khoản thiếu quyền vào thẳng `/meeting/room-board` -> vào được, lưới render |
| | K2 | Tài khoản thiếu quyền vào `/meeting/rooms` -> vẫn bị chặn (gate danh mục không bị nới lỏng) |

**Ca cố ý bỏ: KHÔNG có.** Toàn bộ 18 ca của smoke file đều đáng giữ (không có ca trùng lặp, không có
ca chỉ để thăm dò tạm) — khác với gotcha đã xảy ra ở Phase 2 (gom mất ca "cảnh báo chưa lưu"), lần
này đối chiếu từng ca 1-1 giữa file cũ và file mới trước khi xoá smoke.

### 2. Rà ca lạc hậu do Task 23 (thêm mục menu thứ 3)
- **F1 của `meeting-room.spec.ts` (Phase 1, dòng 714-754)**: đã kiểm — case này KHÔNG đếm tổng số
  mục trong nhóm "Quản lý phòng họp" (không có `rows.toHaveCount(N)` cho cả nhóm), chỉ assert từng
  dòng cụ thể bằng `.filter({hasText: ...}).toHaveCount(1)` cho "Danh sách phòng họp" và "Đăng ký
  phòng họp". Việc Task 23 thêm mục thứ 3 ("Tình trạng phòng họp") KHÔNG làm ca này đỏ — comment
  trong file (dòng 727-730) cũng đã ghi nhận bài học "đổi hành vi thường làm sai giả định của ca cũ"
  từ lần Task 16 điền link "Đăng ký phòng họp". **Kết luận: F1 không lạc hậu, không cần sửa.**
  (Xác nhận thêm bằng cách chạy thật ở bước verify bên dưới.)
- Rà thêm toàn thư mục `tests/meeting/`: không còn spec nào giả định "màn room-board chưa tồn tại"
  hay "nút Xem lịch phòng chưa có" — 2 giả định cũ này chỉ từng nằm ở nhóm I/J/K của
  `_room-board-ui.smoke.spec.ts` (đã ghi "Task 23 — ... (trả nợ nút Phase 1)"), nay đã port nguyên
  vào bộ chính thức. `meeting-room-booking.spec.ts` và các file `*.api.spec.ts` không đụng tới menu
  sidebar / nút "Xem lịch phòng" nên không có gì lạc hậu.

### 3. Không sửa code sản phẩm
Không đụng `pages/**`, `components/**`, `Modules/**` — chỉ thao tác trong `e2e/tests/meeting/`.

## Kết quả chạy verify (FOREGROUND, từng file)

(điền sau khi có kết quả)

## Concerns
(điền sau khi có kết quả)
