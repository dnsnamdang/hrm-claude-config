# Task 22 — Tab "Theo tuần (1 phòng)" + Tab "Thẻ trạng thái" — Báo cáo

**Status: HOÀN THÀNH — đã qua Fix round 1 (xem mục cuối file).** 2 tab mới chạy được trong CÙNG page
`room-board/index.vue` (bootstrap-vue `<b-tabs lazy>`). Sau fix round 1: **18/18 ca Playwright
XANH** (6 ca cũ Task 21 + 1 ca A4 mới của round 1 + 7 ca Task 22 + 4 ca I/J/K của Task 23 chạy chung
file), 2 lệnh grep tự kiểm đều RỖNG. Dữ liệu test đã dọn sạch, phòng thật `B1` (id 1618) còn nguyên.

## File sửa

- `pages/meeting/room-board/index.vue` (worktree `phong-hop-client`, nhánh `feat/quan-ly-phong-hop`)
  — thêm `<b-tabs v-model="activeTabIndex" lazy>` bọc 3 tab: "Theo ngày" (giữ nguyên Task 21),
  "Theo tuần (1 phòng)" (FullCalendar timeGrid v5 free, chọn phòng bằng `V2BaseSelect` tái dùng
  `rooms` đã tải cho tab Ngày — không gọi API riêng cho danh sách phòng), "Thẻ trạng thái" (grid thẻ
  đọc `state`/`current_booking`/`next_booking` từ `GET meeting/rooms/status-board`, `setInterval`
  60s trong `startStatusPolling()`, `clearInterval` ở `beforeDestroy()` page-level).
- `e2e/tests/meeting/_room-board-ui.smoke.spec.ts` — thêm helper `pickSelect2Option()` (copy từ
  `meeting-room-booking.spec.ts`) + 4 nhóm ca mới E/F/G/H (7 test), cộng thêm setup room/booking
  riêng cho tab trạng thái trong `describe F`'s `beforeAll`.

## Quyết định kỹ thuật đáng chú ý

1. **Lazy load đúng nghĩa**: `<b-tabs lazy>` khiến b-tab-pane CHƯA bấm tới không render (API của
   tab đó không bị gọi). Tab 0 "Theo ngày" vẫn active ngay từ đầu nên hành vi Task 21 không đổi.
   Cờ `weekTabOpened`/`statusTabOpened` (watcher `activeTabIndex`) đảm bảo API tab Tuần/Trạng thái
   CHỈ gọi lần đầu user bấm mở, không gọi lại mỗi lần quay lại tab (trừ khi phòng/tuần đổi).
2. **Giữ lựa chọn khi chuyển tab**: mọi state (`date`, `weekRoomId`, `weekStartDate`, dữ liệu đã
   tải) nằm ở `data()` của CHÍNH page — `<b-tabs lazy>` chỉ huỷ/dựng lại DOM của tab-pane, không huỷ
   state (page component không bị destroy). Đo được ở ca G1/G2.
3. **FullCalendar tuần**: `firstDay: 1` + `weekStartDate` luôn chốt về Thứ 2 (`mondayOf()`) để 7
   ngày BE trả (`start_date` → `+7 ngày`) khớp CHÍNH XÁC 7 cột Thứ 2→Chủ nhật FullCalendar vẽ. Bấm
   Tuần trước/sau khi calendar ĐANG mount phải gọi thẳng `calendarApi.gotoDate()` — đổi
   `options.initialDate` không tự điều hướng lại (giới hạn đã biết của `@fullcalendar/vue` v5, xem
   comment tại `loadWeek()`).
4. **403 `week()` xử lý tử tế**: `weekForbidden` hiện thông báo thay vì màn trắng (task-19-report.md
   mục Concerns #2). Ca E2 test bằng phòng thật `B1` (id 1618) — đo được cả 2 nhánh (403 hoặc load
   được), không giả định cứng công ty của tài khoản test.
5. **Màu badge KHÔNG tự chế**: "Đang họp đến.."/"Sắp họp lúc.." dùng `V2BaseBadge :color="...status_color"`
   của CHÍNH phiếu (BE trả), không tự map màu theo `state`. "Đang trống" dùng `variant="muted"` có
   sẵn của component (không có phiếu nào để lấy màu BE) — ghi rõ lý do trong code comment.
6. **Refresh chéo tab**: Duyệt/Từ chối/Hủy/Lưu phiếu giờ gọi `refreshLoadedViews()` — tải lại
   "Theo ngày" LUÔN + "Theo tuần"/"Thẻ trạng thái" NẾU đã từng mở, tránh 3 tab lệch dữ liệu nhau sau
   khi đổi trạng thái phiếu.

## 2 lệnh grep tự kiểm

```
$ grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/room-board/ | grep -v V2Base
(rỗng)

$ grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/room-board/
(rỗng)
```

## Playwright — dòng tổng kết (FOREGROUND, không đẩy nền)

Lệnh chạy:
```
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/_room-board-ui.smoke.spec.ts --project=chromium --no-deps --workers=1
```

Kết quả cuối (sau 2 vòng sửa lỗi do chính spec viết sai, KHÔNG phải lỗi code màn — xem mục "Vấn đề
gặp phải khi viết test" bên dưới):

```
Running 13 tests using 1 worker
...
  13 passed (2.6m)
```

Không có dòng "did not run" nào — cả 6 ca cũ (A1-A3, B1, C1, D1) lẫn 7 ca mới (E1, E2, F1, F2, G1,
G2, H1) đều xanh trong CÙNG 1 lần chạy.

## Số đo DOM thật (log console của Playwright)

- **E1** (chọn Phòng A, tuần chứa `TEST_DATE`): `1 sự kiện, mã DPH-2026-01385` đúng `booking1Code`;
  bấm "Tuần trước" → `0 sự kiện`; bấm "Tuần sau" quay lại → lại `1 sự kiện`.
- **E2** (phòng thật B1 id 1618, tab Theo tuần): `forbidden=false calendarShown=true` (tài khoản
  test cùng công ty B1 nên load được — nhánh 403 không rơi vào lần chạy này, nhưng code xử lý cả 2
  nhánh, không phụ thuộc giả định).
- **F1** (phòng có phiếu đang diễn ra): `state=dang_hop`, badge `"Đang họp đến 17:04"` (đúng
  `end_at` của phiếu setup), mã phiếu `E2EOFF_BOARD_STATUS_BK_...` — đúng tên cuộc họp + người đặt.
- **G1** (chuyển 3 tab qua lại): ô ngày ở tab "Theo ngày" vẫn `= 23/09/2026` (TEST_DATE) sau khi đi
  qua Theo tuần + Thẻ trạng thái rồi quay lại.
- **G2** (chọn Phòng A ở tab Theo tuần rồi chuyển đi/về): select2 vẫn hiện "Phòng A", vẫn `1 sự
  kiện` — không mất lựa chọn, không gọi lại API (dữ liệu đã có sẵn).
- **H1** (bẫy #4, dùng `page.clock` tua ảo thay vì chờ thật 60s): mở tab Thẻ trạng thái + tua 65s ảo
  → `2 request status-board` (1 lúc mở + 1 lúc interval bắn — CHỨNG MINH polling THẬT SỰ chạy, không
  chỉ gọi 1 lần lúc mount). Rời màn (`goto /meeting/bookings`) + tua thêm 65s ảo → **vẫn `2` — không
  tăng** → `clearInterval()` hoạt động đúng.

## Dữ liệu test — dọn sạch, không đụng dữ liệu thật

Xác nhận sau khi chạy xong: `meeting_rooms`/`meeting_room_bookings` LIKE `'E2EOFF_%'` = **0 dòng**;
phòng thật `B1` (id 1618) vẫn `code = 'B1'`. Toàn bộ phòng/phiếu của Task 22 dùng prefix
`E2EOFF_BOARD_*`, dọn ở `afterAll` chung của file (chạy cả khi có ca fail — mode `serial`).

## Vấn đề gặp phải khi viết test (đã tự phát hiện + sửa, không phải lỗi code màn)

1. **E1 lần đầu fail vì hiểu sai UX của "Tuần này"**: test bấm "Tuần này" mong quay lại đúng tuần
   đang xem trước đó, nhưng nút đó (đúng thiết kế) nhảy về tuần HIỆN TẠI THẬT ngoài đời — khác tuần
   chứa `TEST_DATE` (cố tình cách "hôm nay" 5 ngày để né dữ liệu thật). Sửa test dùng "Tuần sau" để
   quay lại đúng tuần đã xem — không phải sửa code màn.
2. **Chọn phòng qua select2 bằng click thẳng vào `<li>` không gõ lọc trước** bị timeout ngẫu nhiên
   khi danh sách phòng dài (nhiều phòng thật + phòng do spec khác tạo). Đã thay bằng
   `pickSelect2Option()` — copy khuôn ĐÃ KIỂM CHỨNG từ `meeting-room-booking.spec.ts` (gõ vào
   `.select2-search__field` lọc trước rồi mới click).
3. **Tạo phiếu "đang diễn ra" cho ca F1 KHÔNG dùng được API `POST room-bookings`** vì service chặn
   cứng "Không thể đặt phòng cho thời điểm đã qua" (`start_at < now()`, spec 5.1 mục 3) — start_at
   10' trước "bây giờ" luôn bị 422. Đây là dữ liệu SETUP để test đọc `status-board` (không test luồng
   tạo phiếu), nên chuyển sang chèn thẳng bằng SQL (`status=2` Đã duyệt), dùng `booked_by_employee_id`
   lấy từ phiếu `booking1` (tạo qua API ở `beforeAll` chung) để `booked_by_name` join đúng tên thật.

## Concerns / lưu ý cho task sau

1. **Refresh chéo tab (`refreshLoadedViews()`) chỉ chạy khi Duyệt/Từ chối/Hủy/Lưu từ modal của
   CHÍNH page này** — nếu Task 23/24 mở `BookingDetailModal` từ nơi khác rồi thao tác, tab Tuần/
   Trạng thái của màn `room-board` (nếu đang mở ở tab khác của trình duyệt) sẽ KHÔNG tự cập nhật
   tức thời (chỉ tự làm mới sau tối đa 60s nhờ polling của tab Trạng thái; tab Tuần thì đợi user đổi
   phòng/tuần hoặc F5). Chấp nhận được cho phạm vi task này.
2. **`weekRoomOptions` dùng lại `rooms` đã lọc theo `filters` của tab "Theo ngày"** (company_id/
   amenity_ids/capacity_from) — nếu user đang lọc hẹp ở tab Ngày rồi sang tab Tuần, danh sách phòng
   để chọn cũng bị lọc theo đúng bộ lọc đó (không phải toàn bộ phòng hệ thống). Đây là lựa chọn có
   chủ đích để tránh gọi thêm API riêng (đúng tinh thần "1 màn = càng ít API càng tốt"), nhưng nêu ra
   để Task 23/24 biết nếu cần "chọn phòng không giới hạn bởi bộ lọc tab Ngày" thì phải đổi nguồn data.
3. **CSS FullCalendar import trực tiếp trong `<script>`** (`import '@fullcalendar/common/main.css'`
   v.v., KHÔNG import trong `<style scoped>` vì vue-loader sẽ gắn scope đè lên selector của thư viện)
   — repo hiện không import CSS này ở đâu khác (kể cả màn timesheet cũ dùng FullCalendar cũng không
   thấy import), nên đây là lần đầu style FullCalendar thực sự được nạp đúng cách trong hrm-client.
   Playwright đã xác nhận layout render đúng (đo được toạ độ/kích thước sự kiện qua `eventDidMount`),
   nhưng nếu 1 màn FullCalendar khác sau này KHÔNG import CSS tương tự thì sẽ vỡ layout.

---

## Fix round 1 (review Task 20-22) — bẫy `Math.round()` làm ô ĐANG BỊ GIỮ hiển thị TRỐNG

**Status: ĐÃ SỬA + đo được bằng ca test mới, 18/18 ca Playwright XANH (không phải 13 — có thêm A4
của round này + nhóm I/J/K của Task 23 chạy song song trên CÙNG file spec, không xung đột).**

### Bug gốc

`components/meeting-room/RoomTimelineGrid.vue:275-276` (`bookingsForRoom()`) tính cột bắt đầu/kết
thúc của khối phiếu bằng `Math.round()`. Với `stepMinutes=30`, phiếu bắt đầu **14:15** bị làm tròn
**LÊN** 14:30 → nửa ô 14:00-14:30 đang bị giữ **hiển thị TRỐNG** — nguy hiểm vì màn này chỉ để biết
phòng nào giờ nào còn trống, sai hướng "trống hơn" khiến user đặt đè vào ô đã có người. Nguồn dữ
liệu lệch phút có thật: `BookingFormModal.vue` dùng ô giờ `type="time"` không ép bước 30'.

### Sửa

- **`components/meeting-room/RoomTimelineGrid.vue`** — `colStart0` đổi `Math.round()` →
  `Math.floor()`, `colEnd0` đổi `Math.round()` → `Math.ceil()`. Nguyên tắc: sai số CHỈ được phép làm
  ô trông **bận hơn** thực tế (an toàn), không bao giờ **trống hơn** (nguy hiểm).
- **`.claude/skills/room-timeline-grid/SKILL.md`** — thêm mục **5.6 "Làm tròn phút lệch bước — LUÔN
  theo hướng BẬN HƠN, không bao giờ theo hướng TRỐNG HƠN"**, ghi rõ lý do + tránh người sau dùng lại
  component đổi ngược về `Math.round()`.
- **`e2e/tests/meeting/_room-board-ui.smoke.spec.ts`** — thêm ca **A4** trong nhóm A (phòng + phiếu
  RIÊNG, không đụng Phòng A/B của các nhóm ca khác): phiếu **14:15-15:45** (step 30') phải hiện
  ĐÚNG 4 ô (14:00, 14:30, 15:00, 15:30) — đo `getBoundingClientRect()` của khối so với **cột thật**
  `[data-col-time="14:00"]` (mép trái) và `[data-col-time="15:30"]` (mép phải), cùng cách đo với A1.

### Số đo thật (log Playwright)

```
[đo thật] Phiếu 14:15-15:45: khối x=3038.56 width=373.94 (kỳ vọng x=3038.56, width=373.94 = 4 ô 14:00->16:00)
✓ A4. Phiếu lệch phút 14:15-15:45 (step 30) hiện ĐỦ 4 ô 14:00->16:00, KHÔNG làm tròn vào trong (22.9s)
```

Mép trái khối khớp tuyệt đối mép trái cột 14:00 (không lệch sang 14:30), mép phải khối khớp mép
phải cột 15:30 (= mép trái cột 16:00) — đúng 4 ô, không phải 3 ô như `Math.round()` sẽ tính nhầm.

### `task-21-report.md` (MINOR — file báo cáo Task 21 bị thiếu)

Đã viết bù `/.sdd/task-21-report.md` (agent Task 21 bị dừng trước khi kịp ghi): tóm tắt màn "Theo
ngày" đã làm gì, 6 ca e2e gốc (A1-A3, B1, C1, D1), 3 phép đo port từ `_gridpreview.vue`/
`_grid-preview.smoke.spec.ts` (Task 20) sang màn thật, xác nhận 2 file tạm đó đã bị xoá khỏi
worktree.

### Chạy lại TOÀN BỘ file spec (FOREGROUND, đọc dòng tổng kết)

Lệnh giống hệt lần trước, chạy lại sau khi sửa xong:

```
Running 18 tests using 1 worker
...
  18 passed (3.3m)
```

Không có dòng "did not run" nào. 18 ca gồm: A1-A4 (4, có thêm A4 mới), B1, C1, D1 (Task 21 cũ),
E1-E2, F1-F2, G1-G2, H1 (Task 22, 7 ca), và I1, J1, K1-K2 (4 ca — do agent Task 23 thêm vào CÙNG file
spec dùng chung trong lúc tôi đang sửa round này; chạy chung không xung đột, không đụng file nào
của Task 23 theo đúng yêu cầu điều phối).

### Dọn dữ liệu test

Chạy `_room-board-ui.smoke.spec.ts` nhiều lần trong lúc debug (fix round trước + round này) để lại
**1 phòng mồ côi** `E2EOFF_BOARD_B_1789723503625` (không có phiếu nào tham chiếu, không có tiến
trình Playwright nào còn chạy) — có thể do một lần chạy trước đó bị dừng/trùng giờ với tiến trình
khác trên cùng DB dev khiến bước `afterAll` xoá phòng qua API bị bỏ sót. Đã xoá thủ công bằng SQL
sau khi xác nhận an toàn (0 phiếu tham chiếu, không tiến trình nào đang chạy). Xác nhận lại cuối
cùng: `meeting_rooms`/`meeting_room_bookings` LIKE `'E2EOFF_%'` = **0 dòng** cả hai; phòng thật `B1`
(id 1618) vẫn `code = 'B1'`.

### Phạm vi đụng file ngoài `pages/meeting/room-board/` (đã xin phép qua chỉ đạo fix round)

Round này BẮT BUỘC sửa `components/meeting-room/RoomTimelineGrid.vue` (dùng chung, nằm ngoài phạm
vi gốc "chỉ đụng `pages/meeting/room-board/`") và `.claude/skills/room-timeline-grid/SKILL.md` —
theo đúng chỉ đạo trực tiếp của coordinator cho fix round 1, không tự ý mở rộng phạm vi. KHÔNG đụng
`components/subsystem-menu/meeting.js` hay `pages/meeting/rooms/index.vue` (đang do agent Task 23
sửa song song).
