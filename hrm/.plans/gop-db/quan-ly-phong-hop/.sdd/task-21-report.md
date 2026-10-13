# Task 21 — Màn `/meeting/room-board` tab "Theo ngày" — Báo cáo (viết bù)

> File này bị thiếu vì agent thực hiện Task 21 bị dừng trước khi kịp ghi báo cáo. Nội dung dưới đây
> viết bù lại từ code + e2e đã có trong worktree tại thời điểm bắt đầu Task 22 (agent Task 22 đọc
> lại `pages/meeting/room-board/index.vue`, `components/meeting-room/RoomTimelineGrid.vue` và
> `e2e/tests/meeting/_room-board-ui.smoke.spec.ts` bản gốc 6 ca trước khi thêm tab mới).

**Status: HOÀN THÀNH** (xác nhận lại — 6 ca e2e gốc của Task 21 vẫn XANH khi Task 22 chạy lại toàn
bộ file, không "did not run").

## Màn đã làm gì

`pages/meeting/room-board/index.vue` — tab "Theo ngày" của màn "Tình trạng phòng họp":

- Thanh điều hướng ngày (Ngày trước/Hôm nay/Ngày sau + `V2BaseDatePicker`) + bộ lọc Công ty/Tiện
  nghi/Sức chứa tối thiểu, đọc sẵn query `?date=&room_id=` lúc `data()` khởi tạo (né bắn thêm 1
  request thừa ở `mounted()`).
- **1 request DUY NHẤT** `GET meeting/rooms/board?date=&company_id=&amenity_ids=&capacity_from=`
  trả cả `rooms[]` + `bookings[]` + `config` (giờ mở/đóng cửa) — dựng lưới Phòng × Giờ bằng
  `components/meeting-room/RoomTimelineGrid.vue` (component CSS-grid tự dựng, không dùng
  FullCalendar resource-timeline vì repo chỉ có bản miễn phí).
- Bấm **ô trống** → mở `BookingFormModal` (tái dùng Phase 2) với phòng/ngày/giờ điền sẵn qua
  `$refs` + `markFormPristine()` (modal không có prop nhận giá trị điền sẵn).
- Bấm **khối phiếu** → mở `BookingDetailModal` (tái dùng Phase 2), nối đủ 3 handler
  Duyệt/Từ chối/Hủy ở footer (modal tự ẩn/hiện nút theo cờ BE `is_can_*`).
- `?room_id=` lọc sẵn 1 phòng cụ thể (dùng cho nút "Xem lịch phòng" của Task 23), lọc CLIENT-SIDE
  trên `rooms` đã tải — không gọi lại API. Có nút "Bỏ lọc phòng".
- `layout: 'default-sidebar'`, mixin `CheckPermission` (endpoint `board` không gắn
  `checkPermission` ở BE — mọi nhân viên tra được tình trạng phòng, theo quyết định #8 của plan).

## 3 phép đo đã PORT từ `pages/meeting/_gridpreview.vue` (Task 20) sang màn thật

Task 20 dựng `RoomTimelineGrid.vue` trên 1 page tạm (`_gridpreview.vue`) kèm bộ e2e tạm
(`_grid-preview.smoke.spec.ts`) để kiểm layout độc lập trước khi có API thật. Task 21 port 3 phép
đo đó sang `_room-board-ui.smoke.spec.ts` nhóm **A** (chạy trên dữ liệu THẬT qua API `board`):

1. **A1** — khối phiếu 14:00-15:30 bắt đầu ĐÚNG mép trái cột giờ 14:00 (`boundingBox().x` sai số
   ≤1px) và rộng ĐÚNG 3 ô 30' (`boundingBox().width` khớp `colWidth × 3`).
2. **A2** — phiếu qua đêm (22:00 hôm trước → 02:00 hôm chạy) có dấu tiếp diễn `←` ở đầu (không có
   `→` vì không cắt tiếp sang ngày sau nữa trong phạm vi lưới), và bắt đầu đúng mép trái lưới (ô
   đầu tiên của phòng, không lùi theo giờ 22:00 thật).
3. **A3** — khung giờ lưới TỰ NỚI ra ngoài mặc định 07:00-20:00 (26 cột) khi có phiếu qua đêm chạm
   ngoài khung giờ đó — đo được > 26 cột thay vì cố định.

## 6 ca e2e gốc (trước khi Task 22 thêm nhóm E/F/G/H)

Bộ `_room-board-ui.smoke.spec.ts`, 4 nhóm:

- **A. Lưới hiển thị đúng** — A1, A2, A3 (3 phép đo ở trên).
- **B. Bấm ô trống → modal điền sẵn đúng** — B1: bấm ô 10:00 Phòng A → `BookingFormModal` mở, đo
  giá trị 4 ô Phòng họp/Ngày/Từ giờ/Đến giờ đều khớp đúng phòng + ngày + khung giờ vừa bấm.
- **C. Bấm khối phiếu → modal chi tiết đúng mã** — C1: bấm khối 14:00-15:30 → `BookingDetailModal`
  mở đúng, subtitle chứa đúng mã phiếu.
- **D. Query `?room_id=&date=` → lọc sẵn đúng phòng, đúng ngày** — D1: mở URL với `room_id` Phòng A
  → lưới chỉ còn 1 dòng Phòng A, thấy phiếu Phòng A, KHÔNG thấy phiếu Phòng B (dữ liệu phòng khác
  không lẫn vào), nút "Bỏ lọc phòng" hiện đúng lúc đang lọc.

Dữ liệu test: 2 phòng tạm (`E2EOFF_BOARD_A_*`/`E2EOFF_BOARD_B_*`), 2 phiếu tạm (1 phiếu trong ngày,
1 phiếu qua đêm), `TEST_DATE` lùi +5 ngày kể từ hôm chạy để né cả "hôm nay" (vạch bây giờ) lẫn ngày
có dữ liệu thật (phòng B1 19/09). Dọn ở `afterAll`, không đụng dữ liệu thật.

## 2 file tạm đã xoá (theo task-21-brief.md mục 7, đã xác nhận KHÔNG còn trong worktree)

- `pages/meeting/_gridpreview.vue`
- `e2e/tests/meeting/_grid-preview.smoke.spec.ts`

## Lưu ý

Report này viết bù sau khi Task 22 đã bắt đầu sửa cùng file `_room-board-ui.smoke.spec.ts` (thêm
nhóm E/F/G/H) và cùng component `RoomTimelineGrid.vue` (fix round 1: `Math.round()` → `floor`/
`ceil` cho mép phiếu lệch phút — xem `task-22-report.md`). Không có thay đổi nào khác về mặt hành
vi của tab "Theo ngày" so với lúc Task 21 bàn giao, ngoài đúng 1 fix đó.
