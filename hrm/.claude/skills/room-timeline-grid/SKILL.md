---
name: room-timeline-grid
description: "Use when hiển thị lưới \"Phòng × Giờ\" (mỗi dòng 1 phòng họp, cột chia theo mốc giờ, khối phiếu đặt nằm ngang) — màn Sơ đồ đặt phòng / Theo dõi tình trạng phòng / bất kỳ màn nào cần xem nhiều phòng cùng lúc theo dòng thời gian. Dùng component `components/meeting-room/RoomTimelineGrid.vue`, KHÔNG tự dựng lưới mới."
---

# Skill: RoomTimelineGrid — lưới Phòng × Giờ dùng chung

Plan quan-ly-phong-hop, Task 20. Trước task này, dạng "resource × thời gian" **chưa từng có**
trong hrm-client → đã tách thành component dùng chung `components/meeting-room/RoomTimelineGrid.vue`
ngay từ lần đầu (CLAUDE.md mục "BẮT BUỘC rà project trước khi làm bất kỳ UI/logic nào").

Task 21 (màn "Sơ đồ đặt phòng") dùng lại component này; Phase 5-6 (dashboard/báo cáo phòng họp)
có thể dùng tiếp — **đừng nhân bản, hãy tái sử dụng**.

---

## 1. Khi nào dùng

- Cần vẽ 1 lưới **nhiều phòng (dòng) × mốc giờ (cột)**, mỗi phòng có thể có 0..n phiếu đặt nằm
  ngang trên dòng của nó (giống Google Calendar "resource view", hoặc FullCalendar
  resource-timeline).
- **KHÔNG** dùng khi chỉ cần lịch dạng tháng/tuần/ngày thông thường (dùng FullCalendar v5 sẵn có,
  bản miễn phí của repo đủ cho case đó — xem mục 5.1 bẫy #1).

## 2. Props / Emit

| Prop | Kiểu | Mặc định | Ghi chú |
|---|---|---|---|
| `rooms` | `Array<{id, code, name, capacity, location}>` | `[]` | mỗi phần tử = 1 dòng |
| `bookings` | `Array<{id, code, title, meeting_room_id, start_at, end_at, status, status_color, booked_by_name}>` | `[]` | `start_at`/`end_at` chấp nhận ISO-8601 có offset (`2026-09-18T08:00:00+07:00`, khuôn BE trả — xem `MeetingRoomBookingResource::isoDateTime()`) hoặc `YYYY-MM-DD HH:mm:ss` |
| `openTime` | `String 'HH:mm:ss'` | `'07:00:00'` | mép trái mặc định của lưới |
| `closeTime` | `String 'HH:mm:ss'` | `'20:00:00'` | mép phải mặc định của lưới |
| `stepMinutes` | `Number` | `30` | độ rộng 1 cột, tính bằng phút |
| `date` | `String 'YYYY-MM-DD'` | bắt buộc | ngày đang xem — quyết định phiếu nào hiện, vạch "bây giờ" có hiện không |

Emit:
- `slot-click` → payload `{ room, startAt, endAt }` (giờ bắt đầu/kết thúc của Ô TRỐNG vừa bấm,
  chuỗi `'YYYY-MM-DD HH:mm:ss'`) — dùng để mở form đặt phòng nạp sẵn phòng + giờ.
- `booking-click` → payload là NGUYÊN object booking vừa bấm — dùng để mở popup chi tiết phiếu.

## 3. Cách tính cột từ phút (đọc trước khi sửa component)

Toàn bộ bảng (góc + header giờ + nhãn phòng + ô trống + khối phiếu + vạch "bây giờ") là con của
**ĐÚNG MỘT** `display:grid` (`.rtg-grid` trong component) — không lồng grid con theo từng dòng.
Lý do: 2 grid riêng biệt có thể bo tròn track-size khác nhau vài phần trăm pixel dù cùng
`grid-template-columns`, làm khối phiếu lệch mép cột 1px mà mắt thường không thấy nhưng
`getBoundingClientRect()` của e2e bắt được ngay.

Quy trình tính (xem `computed` của `RoomTimelineGrid.vue`):

1. Đổi mọi mốc giờ về **"phút tuyệt đối tính từ 00:00 của `date`"** — gọi là `absMin`. Phiếu bắt
   đầu/kết thúc khác ngày `date` thì `absMin` âm (trước `date`) hoặc > 1440 (sau `date`).
   ```js
   absMin = (epochDay(bookingDateStr) - epochDay(refDateStr)) * 1440 + hh * 60 + mm
   ```
   `epochDay()` dùng `Date.UTC(y, m-1, d) / 86400000` — **KHÔNG** dùng `new Date('YYYY-MM-DD')`
   hay so lệch bằng local Date, để hiệu ngày không phụ thuộc timezone máy chạy test (bẫy đã ghi ở
   `BookingFormModal.vue`, xem `.plans/gop-db/quan-ly-phong-hop/`).
2. Cắt (`clip`) `absMin` về khoảng `[0, 1440]` để có mốc HIỂN THỊ trong ngày `date`:
   `displayStart = max(startAbsMin, 0)`, `displayEnd = min(endAbsMin, 1440)`.
3. Khung lưới (`gridStartMinutes`/`gridEndMinutes`) = mở rộng `openMinutes`/`closeMinutes` cho vừa
   `displayStart`/`displayEnd` của MỌI phiếu chạm ngày đó, rồi làm tròn về bội số `stepMinutes`
   (`floor` cho đầu, `ceil` cho cuối) — đây chính là bước "tự nới khung giờ" (mục 5.3).
4. Cột 0-index của 1 mốc phút: `colIndex = (min - gridStartMinutes) / stepMinutes`.
5. Khối phiếu: `style="grid-column: {colIndex(displayStart) + 2} / span {colIndex(displayEnd) - colIndex(displayStart)}"`
   (`+2` vì cột 1 là cột nhãn phòng, cột phút bắt đầu từ cột 2). **Tuyệt đối không** đổi sang
   `position: absolute` + tính `left/width` bằng px — đổi cỡ màn hình/zoom trình duyệt sẽ làm khối
   lệch khỏi cột (grid tự co giãn theo `1fr`, pixel thì không).
6. Vạch "bây giờ" là **ngoại lệ hợp lý duy nhất**: dùng 1 overlay `grid-column: 2 / -1` (chiếm
   đúng vùng cột giờ, cùng 1 grid nên khớp tuyệt đối với các cột), bên trong đặt
   `left: calc(<phần trăm> * 100%)` — dùng **phần trăm**, không phải pixel cố định, nên vẫn co
   giãn đúng khi resize/zoom. Không áp kỹ thuật này cho khối phiếu vì phần trăm không cho ra số
   cột nguyên (rất khó match chính xác 1 cột như khối phiếu cần).

## 4. Ví dụ tối thiểu

```vue
<RoomTimelineGrid
    :rooms="rooms"
    :bookings="bookings"
    :date="selectedDate"
    open-time="07:00:00"
    close-time="20:00:00"
    :step-minutes="30"
    @slot-click="onSlotClick"
    @booking-click="onBookingClick"
/>
```

`onSlotClick({ room, startAt, endAt })` → mở `BookingFormModal` với `room_id` + giờ nạp sẵn.
`onBookingClick(booking)` → mở `BookingDetailModal` với `booking.id`.

## 5. 5 cái bẫy (đọc trước khi sửa hoặc nhân bản component)

### 5.1 Không có FullCalendar resource-timeline
Repo chỉ có `@fullcalendar` v5 **bản miễn phí** (core/timegrid/list/interaction). Dạng
"resource × thời gian" là tính năng **Premium trả phí** → đừng mất thời gian tìm cách ép
FullCalendar render kiểu này, phải tự dựng bằng CSS grid như component này.

### 5.2 Đo layout trong `watcher`/`$nextTick` ra DOM CŨ
Bẫy đã ghi chung của dự án (`vue2-nexttick-trong-watcher-do-dom-cu`): nếu về sau cần ĐO layout
bằng JS (ví dụ cuộn tới đúng cột "bây giờ" khi mount) thì phải đo trong
`requestAnimationFrame(() => { ... })` sau `$nextTick`, không đo ngay trong watcher — nếu không,
kết quả đo lệch đúng 1 nhịp render mà **không báo lỗi gì**. `RoomTimelineGrid.vue` hiện tại
**không cần đo DOM bằng JS** (mọi định vị là khai báo qua CSS grid), tránh được bẫy này hoàn
toàn — giữ nguyên cách tiếp cận đó khi mở rộng, đừng thêm code đo pixel nếu không thật sự cần.

### 5.3 Phiếu QUA ĐÊM + tự nới khung giờ
Phiếu bắt đầu hôm trước hoặc kết thúc hôm sau vẫn phải hiện ở MỌI ngày nó chạm, cắt đúng mép ngày
(00:00/24:00) và có dấu tiếp diễn (`←` nếu bắt đầu trước ngày đang xem, `→` nếu kết thúc sau ngày
đang xem). Khung giờ lưới (`gridStartMinutes`/`gridEndMinutes`) phải **tự nới** để ôm trọn phần
hiển thị của phiếu đó dù nó nằm ngoài `openTime`-`closeTime` mặc định — không nới thì phòng đang
bị giữ mà lưới trông như trống (dữ liệu đúng, UI nói dối).

### 5.4 Cấm animation dịch chuyển trên khối chứa chữ
Bẫy chung của dự án (`chu-nhoe-vi-animation-tren-khoi-chua-chu`): animate `transform`/`left`/
`width`/`grid-column` của 1 khối có chữ bên trong làm chữ **nhoè/vỡ pixel** khi trình duyệt tween
qua các giá trị không phải số nguyên. `.rtg-booking` chỉ có `transition: filter` (đổi độ sáng nền
lúc hover) — **không** thêm `transition`/`animation` trên `grid-column`, `left`, `width`,
`transform` của khối phiếu hay của `.rtg-now-line`.

### 5.5 Số đo tránh giá trị lẻ
Mọi padding/margin/border-radius/font-size trong component đều dùng số nguyên px (`6px`, `8px`,
`64px`…), không dùng `10.5px` kiểu vậy — giá trị lẻ dễ vỡ khi trình duyệt làm tròn subpixel khác
nhau giữa các phần tử tưởng như phải bằng nhau.

### 5.6 Làm tròn phút lệch bước — LUÔN theo hướng BẬN HƠN, không bao giờ theo hướng TRỐNG HƠN
`bookingsForRoom()` quy đổi phút của phiếu ra số cột lưới (`stepMinutes`, mặc định 30'). Phiếu
thật KHÔNG phải lúc nào cũng bắt đầu/kết thúc đúng mốc chia hết cho `stepMinutes` (vd 14:15-15:45
khi step=30) — form đặt phòng (`BookingFormModal.vue`, ô giờ `type="time"`) không ép giờ theo bước
30'. Mép bắt đầu PHẢI `Math.floor()`, mép kết thúc PHẢI `Math.ceil()` — TUYỆT ĐỐI không
`Math.round()` cho 1 trong 2 mép:
- `Math.round()` có thể làm tròn **vào trong** (14:15 → cột 14:30), khiến nửa ô 14:00-14:30 **đang
  bị giữ hiển thị TRỐNG**. Màn này CHỈ để biết phòng nào giờ nào còn trống — sai lệch hướng "trống
  hơn" khiến user đặt đè vào đúng khoảng đã có người (bug thật, phát hiện ở review Fix round 1 của
  Task 22, sửa tại `bookingsForRoom()`).
- `floor`/`ceil` chỉ có thể làm ô trông **bận hơn thực tế** một chút (an toàn) — không bao giờ theo
  hướng ngược lại. Test case phủ: phiếu 14:15-15:45 (step 30') phải hiện đúng span 4 ô
  (14:00-14:30-15:00-15:30), KHÔNG phải 3 ô.

## 6. Việc KHÔNG phải làm lại

- Màu khối phiếu đọc thẳng `status_color` BE trả (`MeetingRoomBooking::statusColor()`) — component
  tự pha `rgba(..., 0.16)` làm nền + `rgba(..., 0.5)` làm viền, KHÔNG tự map trạng thái → màu ở FE
  (quy tắc chung CLAUDE.md mục Badge trạng thái).
- Nhãn phòng dùng lại `V2BaseTitleSubInfo` (title = tên phòng, subs = mã/sức chứa/vị trí) —
  không tự viết markup tiêu đề + phụ đề mới.
- Số sức chứa hiển thị bằng `toLocaleString('en-US')` (chuẩn định dạng số toàn hệ thống).
