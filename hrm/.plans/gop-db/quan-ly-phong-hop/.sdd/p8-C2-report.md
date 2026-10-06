# Báo cáo — Phase 8 / lượt C2 (T138–T141): FE "Yêu cầu dịch vụ" trên phiếu đặt phòng

Repo `hrm-client`, nhánh `gop_db`. **Chỉ sửa `hrm-client`** — không đụng `hrm-api`.

## Trạng thái: DONE_WITH_CONCERNS

Code đã viết đủ 4 task (T138–T141), tự kiểm tĩnh (compile template + parse script) sạch, nhưng
**chưa được kiểm chứng trên trình duyệt thật** (đúng chỉ đạo — brief cấm tự mở Playwright/trình
duyệt ở lượt này). "CONCERNS" vì có 2 điểm lệch giữa brief/spec và **CODE THẬT** phải xin coordinator
xác nhận trước khi merge (mục "Điểm nghi ngờ" bên dưới) — đã tự quyết theo hướng an toàn nhất
(không mất dữ liệu, không nút chết) và ghi rõ lý do tại chỗ trong code.

## File đã sửa (chỉ 2 file, đúng phạm vi)

- `pages/meeting/bookings/components/BookingFormModal.vue` (+381/-1 dòng)
- `pages/meeting/bookings/index.vue` (+152 dòng)

## T138 — Khối nhập "Yêu cầu dịch vụ" (chỉ TẠO MỚI)

- Vị trí: cột trái (`col-lg-8`) của `BookingFormModal.vue`, ngay sau khối "Ai phụ trách / Ghi chú",
  bên trong `<template v-if="!isMeetingMode">` hiện có — **tiêu đề nhóm phẳng** `.group-title` y hệt
  các khối khác của modal (KHÔNG `V2BaseFormSection`, đúng comment ~dòng 2393 cũ / user chốt
  19/09/2026).
- **Điều kiện hiện** (computed `showServiceEditableBlock`): `!id && !isShow && !isMeetingMode &&
  data.meeting_room_id && roomHasManagers`. `roomHasManagers` đọc `selectedRoomInfo.manager_name`
  (chuỗi ghép `"; "` do `BookableMeetingRoomResource` trả — Resource này CHỦ Ý không trả id thô của
  người phụ trách, nên "có người phụ trách hay không" chỉ suy được qua chuỗi này khác rỗng).
- **Phòng không có người phụ trách** (computed `showServiceNoManagerNote`): hiện dòng
  `.service-empty-note` màu `#6b7280` — "Phòng này chưa khai người phụ trách nên chưa nhận yêu cầu
  dịch vụ." — **KHÔNG dùng `.text-muted`** (grep xác nhận, xem mục Tự kiểm).
- Mỗi dòng là 1 `<tr>` trong bảng (`V2BaseTableScroll` bọc `<table class="... v2-form-table">`, đúng
  khuôn "bảng trong form" của `WrMerchandiseTable.vue` — form-validate skill mục 3b-1): `món`
  (`V2BaseSelectInModal`, nguồn `GET meeting/room-services/options`, KHÔNG `include_ids` vì form tạo
  mới không có dòng cũ nào cần giữ) · `số lượng` (`V2BaseInput type="text"`, theo đúng nếp cột "SL"
  của `WrMerchandiseTable.vue` — không dùng `V2BaseCurrencyInput`) · `ghi chú` · nút xoá dòng
  (`V2BaseIconButton`). Cuối bảng: nút "Thêm dòng" (`secondary`, icon `ri-add-line`).
- **Món đã chọn ở dòng khác biến khỏi dropdown dòng còn lại**: `serviceOptionsForRow(idx)` lọc theo
  `service_id` của các dòng KHÁC (không lọc theo chính dòng đang render).
- **Số lượng để trống, không tự điền theo `attendee_count`** — khởi tạo `''`, `addServiceRow()` push
  `{ service_id: null, quantity: '', note: '' }`.
- **Không tự sửa giá trị user nhập**: không có `Math.min/max`, không format lại khi gõ, không tự xoá
  dòng trống — submit gửi NGUYÊN VẸN mọi dòng (kể cả dòng thiếu `service_id`/`quantity`) để BE 422
  đúng field, KHÔNG filter rồi "âm thầm bỏ dòng lỗi" (đã grep `= max`, `Math.min(`, `Math.max(` trong
  vùng service — rỗng).
- **Hiện hết lỗi mọi dòng cùng lúc**: file này KHÔNG dùng `vee-validate` ở bất kỳ đâu (đã grep
  `v-validate`/`$validator` — rỗng, kể cả trước khi tôi sửa) — toàn bộ validate của form dựa vào BE
  422 map phẳng vào `this.error`. Tôi giữ đúng nếp đó cho khối dịch vụ: lỗi Laravel dạng
  `services.<i>.<field>` đọc trực tiếp qua `serviceRowError(idx, field)`, hiện đồng thời ở MỌI dòng
  ngay khi `this.error = payload.errors` (submitSave() đã làm sẵn, không cần code thêm).
- **Xoá dòng dọn đúng lỗi theo CHỈ SỐ**: `removeServiceRow()` gọi `removeRowErrors(this.error,
  'services', idx)` (`utils/rowFieldErrors.js` có sẵn, đúng skill form-validate mục 3b) — xoá dòng
  giữa thì lỗi các dòng SAU tự kéo lên đúng vị trí, không ăn oan.
- **Payload**: `services: [{ service_id, quantity: Number|null, note: string|null }]`, CHỈ gửi khi
  `!this.id` (tạo mới) và `data.services.length > 0` — 0 dòng thì KHÔNG gửi khoá `services` (đúng
  brief). PUT sửa phiếu không gửi field này (khớp C1: BE `update()` không đọc field đó nữa).

### ⚠️ Tự quyết — khối chỉ hiện ở hướng "Nhu cầu khác", KHÔNG hiện ở "Gắn với cuộc họp"

Spec mục 3 quyết định #9 ghi: *"Phiếu sinh từ cuộc họp (source = 2) cũng yêu cầu dịch vụ được — dùng
chung form."* Nhưng đọc **CODE THẬT** của lượt C1
(`MeetingRoomBookingService::assignMeeting()`, hàm BE gọi khi hướng "Gắn với cuộc họp" bấm Lưu) xác
nhận hàm này **KHÔNG đọc field `request->services` ở bất kỳ đâu** — chỉ `store()` (hướng "Nhu cầu
khác") mới đọc. Nếu hiện khối nhập ở cả 2 hướng, user nhập dịch vụ ở hướng "Gắn với cuộc họp" rồi bấm
Lưu sẽ bị **ÂM THẦM MẤT DỮ LIỆU** (đúng loại lỗi CLAUDE.md cấm tuyệt đối: "không tự sửa/xoá giá trị
user nhập"). Đã tự quyết theo CODE THẬT (đúng chỉ đạo brief "brief lệch code thật thì theo code
thật"): khối chỉ `v-if` trong `<template v-if="!isMeetingMode">` sẵn có, hướng "Gắn với cuộc họp"
không thấy khối này. Ghi comment tại chỗ trong code (computed `showServiceEditableBlock`).

**Coordinator cần xác nhận**: có mở 1 BE task riêng để `assignMeeting()` cũng đọc/ghi `services[]`
không, hay chốt chính thức "yêu cầu dịch vụ chỉ áp dụng hướng Nhu cầu khác" (khác văn bản spec hiện
tại) rồi update lại spec.

## T139 — Chế độ CHỈ ĐỌC (Sửa phiếu + popup Xem)

- Computed `serviceViewRows` = `viewDetail.services || []`, dùng CHUNG cho cả 2 chế độ.
- **Sửa phiếu** (`id && !isShow`): hiện khối chỉ khi `serviceViewRows.length > 0` (phiếu không có
  dịch vụ thì không có gì để "khoá hẳn" hiện ra) — bảng CHỈ ĐỌC, không nút thêm/xoá, không ô nhập
  (đúng luật 5b "khoá hẳn kể cả khi phiếu còn Chờ duyệt" — không có nhánh nào theo trạng thái phiếu).
- **Popup Xem** (`isShow`): cùng bảng + thêm `V2BaseBadge` cạnh tiêu đề nhóm, `:color`/text đọc
  THẲNG `viewDetail.service_status_color`/`service_status_text` do BE trả — **không map số → chữ,
  không tự chọn màu** (grep xác nhận không có `service_status === 1 ? ... :`-kiểu map nào).
- **Trạng thái Từ chối** (`Number(viewDetail.service_status) === 3`): thêm dòng "Lý do từ chối". Luôn
  hiện (không điều kiện theo status) 2 dòng "Người xử lý"/"Thời gian xử lý" khi có
  `service_handled_by_name`/`service_handled_at`. Class riêng `.service-info-row__label` (`#6b7280`)
  / `.service-info-row__value` (`#374151`) — đúng mã màu brief chốt, KHÔNG in đậm, KHÔNG tô đỏ.
- Số lượng ở khối CHỈ ĐỌC hiển thị qua `formatQuantity()` = `Number(value).toLocaleString('en-US')`
  — CẤM `'vi-VN'` (grep `toLocaleString('vi-VN')` trong `pages/meeting/bookings` ra rỗng).

## T140 — 2 nút xử lý ở popup Xem

- 2 nút mới trong `<template #footer>`, `v-if="viewDetail && viewDetail.is_can_handle_service"` (fail
  ẨN HẲN, không disable — đúng cờ fail-closed BE trả).
- `BookingFormModal.vue` chỉ **emit** `service-prepared`/`service-rejected` (kèm `viewDetail`), đúng
  nếp `approve`/`reject`/`cancel` sẵn có (component con emit, `index.vue` xử lý API + confirm).
- `index.vue`: `servicePreparedItem()` gọi `$confirm()` rồi `PUT
  meeting/room-bookings/{id}/service-prepared`; `serviceRejectedItem()` mở `$confirm()` với
  `showInput + requiredInput` (lý do bắt buộc, KHÔNG tự dựng popup riêng, KHÔNG
  `$bvModal.msgBoxConfirm()`) rồi `PUT .../service-rejected` payload `{ reason }` (đúng tên field C1
  bàn giao, KHÔNG phải `service_reject_reason`).
- Thành công → toast + đóng popup (`$bvModal.hide('modal-booking-form')`) + `loadData()` (nạp lại
  danh sách) — đúng nếp approve/reject/cancel.
- **409** (người khác vừa xử lý): `handleServiceActionError()` — hiện ĐÚNG `error.response.data.message`
  của BE (không câu chung chung), rồi nạp lại **CẢ danh sách LẪN chính popup đang mở**
  (`this.$refs.bookingFormModal.loadData(item.id)`) để 2 nút biến mất NGAY tại chỗ, không bắt user tự
  đóng/mở lại mới thấy trạng thái mới (khắt khe hơn 1 chút so với brief — brief chỉ nói "nạp lại",
  không rõ nạp popup hay chỉ danh sách; chọn nạp cả 2 vì rẻ và đúng tinh thần UX của luật 5).

### ⚠️ Tự quyết — đổi chữ nút từ "Đã chuẩn bị"/"Từ chối" (brief) sang "Đã chuẩn bị dịch vụ"/"Từ chối
dịch vụ"

Brief T140 ghi nguyên văn `"Đã chuẩn bị" (primary) và "Từ chối" (nhóm nguy hiểm)`. Nhưng đúng cụm
footer này ĐÃ CÓ sẵn 1 nút "Từ chối" khác (Từ chối **PHIẾU** — is_can_reject, do quản lý/người duyệt
bấm khi phiếu Chờ duyệt). Người trong nhóm phụ trách phòng **thường CŨNG là người duyệt phiếu** (spec
mục 3c: không phân vai giữa duyệt phiếu và xử lý dịch vụ), nên rất dễ gặp cảnh 1 người thấy ĐỒNG THỜI
2 nút "Từ chối" — không phân biệt được, và `data-testid` theo TEXT cũng vỡ. Đã đổi theo CLAUDE.md mục
4.1 "Nêu rõ đối tượng khi chữ trần gây mơ hồ" → **"Đã chuẩn bị dịch vụ"** / **"Từ chối dịch vụ"** —
khớp đúng tên 2 nhóm hành động thông báo C1 đã dùng (`notifyServicePrepared`/`notifyServiceRejected`,
T137: "Đã chuẩn bị dịch vụ"/"Từ chối dịch vụ"), nên nút và thông báo chuông gọi cùng một tên. Ghi rõ
comment tại chỗ trong code.

**Coordinator cần xác nhận**: đồng ý đổi chữ nút này, hay giữ nguyên "Đã chuẩn bị"/"Từ chối" theo văn
bản brief (chấp nhận rủi ro 2 nút "Từ chối" đứng cạnh nhau)?

## T141 — Màn danh sách `pages/meeting/bookings/index.vue`

- **Cột "Dịch vụ"**: thêm vào `allColumns()` với `isVisible: false` (đúng brief "không đổi bộ cột mặc
  định hiện tại" — cùng nếp 4 cột nghiệp vụ khác đã `isVisible: false`). Cell template
  `#cell-service` render `V2BaseBadge` đọc `item.service_status_text`/`service_status_color`, phiếu
  không có dịch vụ → `v-if` false → để TRỐNG, không in "Không có" (đã kiểm không có string "Không có"
  literal nào trong template mới).
- **Ô lọc "Trạng thái dịch vụ"**: thêm vào `filterFields()` dạng `type: 'select'`, options
  `serviceStatusOptions` = Chờ chuẩn bị (1) · Đã chuẩn bị (2) · Từ chối (3) · Không có yêu cầu
  (sentinel `'none'`, vì cột `service_status` chỉ có NULL/1/2/3 — không dùng số 0). Màn này ĐÃ bật
  `:floating="true"` trên `V2BaseSmartFilterPanel` → theo đúng skill list-page: KHÔNG đặt
  `placeholder` (nhãn floating tự nói tên trường), khai y hệt cấu trúc field `status`/`source` sẵn có
  cùng file (copy đúng pattern, không tự chế kiểu mới).

### ⚠️ LỆCH CODE THẬT nghiêm trọng — BE `index()` CHƯA lọc theo `service_status`

Đã đọc toàn bộ `MeetingRoomBookingService::index()` (hrm-api, KHÔNG sửa, chỉ đọc để đối chiếu theo
đúng brief "được phép ĐỌC hrm-api"). Hàm này liệt kê đầy đủ các `if ($request->filled(...))` cho
`meeting_room_id`/`company_id`/`status`/`purpose_id`/`source`/`booked_by`/`only_mine`/`date_from`/
`date_to`/`updated_after` — **HOÀN TOÀN KHÔNG có nhánh nào đọc `service_status`**. Lượt C1 (T131–T137)
không đụng tới hàm `index()` này (chỉ thêm `with(['serviceItems'])` để tránh N+1 cho field mới của
Resource, không thêm filter).

Hệ quả: ô lọc "Trạng thái dịch vụ" tôi vừa thêm ở FE **hiện tại không lọc được gì** — chọn giá trị,
gửi `?service_status=1` lên, BE lặng lẽ bỏ qua tham số lạ (Laravel không lỗi khi thừa query param
không đọc tới), danh sách trả về y hệt như không lọc. Đây KHÔNG phải lỗi ẩn (UI phản hồi rõ: bảng
không đổi khi đổi bộ lọc — QA/coordinator sẽ thấy ngay khi test), nhưng vẫn là **bug chức năng thật**
nếu merge nguyên trạng.

Đã cân nhắc 2 hướng và chọn hướng A:
- **(A) — đã làm**: vẫn implement đủ UI theo đúng brief T141 (cột + ô lọc), gửi tham số
  `service_status` (giá trị `1`/`2`/`3`/`'none'`) lên BE đúng convention hiện có, ghi rõ TRONG CODE
  (comment tại computed `serviceStatusOptions`) + báo cáo này rằng BE cần 1 task riêng thêm nhánh
  `where` tương ứng trong `index()`. Lý do chọn: brief giao đủ 4 task T138-T141 cho lượt FE, không
  giao BE; dừng lại không làm UI thì T141 coi như bỏ dở, mà việc thêm 1 dòng `where` ở BE lại NGOÀI
  quyền hạn "KHÔNG đụng hrm-api" của chính lượt này.
- (B) — không chọn: bỏ hẳn ô lọc, chỉ làm cột. Bị loại vì brief T141 yêu cầu RÕ cả 2, và cột không có
  ô lọc đi kèm cũng là làm nửa vời.

**Coordinator cần xác nhận / hành động**: mở 1 BE task nhỏ thêm
`if ($request->filled('service_status')) { ... }` vào `MeetingRoomBookingService::index()` — gợi ý
map: `1`/`2`/`3` → `where('service_status', $value)`, `'none'` →
`whereNull('service_status')`. Chưa có BE task này thì **ô lọc hiện diện nhưng không hoạt động** —
nếu coordinator muốn ẩn tạm ô lọc cho tới khi BE xong, có thể tự xoá đoạn field `service_status` khỏi
`filterFields()` (đã cô lập gọn trong 1 khối, dễ bật/tắt).

## Ràng buộc bắt buộc — đã kiểm

- Mọi element form dùng `V2Base*` — không `<input>`/`<select>`/`<button>` thô, không
  `class="form-control"`/`class="btn "` mới (xem mục Tự kiểm #1).
- Badge dùng `V2BaseBadge`, màu lấy từ BE (`service_status_color`) — không tự chọn màu.
- Không hard-code cờ quyền `= true` — `is_can_handle_service` đọc thẳng từ BE, không có logic FE tự
  suy luận quyền.
- Không `git commit`/`push`/`stash`. Không đụng `hrm-api` (chỉ ĐỌC để đối chiếu, không `Edit`/`Write`
  file nào bên đó — có thể verify: `git status` phía `hrm-api` sạch, không file nào đổi).
- Không dùng Playwright/mở trình duyệt.

## Cách tự kiểm — SỐ THẬT

### #1 — Grep HTML thô (brief mục "Cách tự kiểm")

```
$ grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/meeting/bookings | grep -v V2Base
pages/meeting/bookings/index.vue:92:  <button type="button" class="v2-cell-link field-line" @click="viewItem(item)">
```
**1 dòng, ĐÃ CÓ TỪ TRƯỚC** (cột Mã mở popup Xem — khuôn danh mục dùng modal, skill list-page mục 3a,
không phải code của lượt này). Phần tôi thêm: **0 dòng vi phạm**.

### #2 — `toLocaleString('vi-VN')`

```
$ grep -rn "toLocaleString('vi-VN')" pages/meeting/bookings
(rỗng)
```

### #3 — `.text-muted`

```
$ grep -rn "text-muted" pages/meeting/bookings
BookingFormModal.vue:535: <!-- ⚠️ `.text-muted` bị SCSS toàn cục ép ĐỎ (CLAUDE.md) — dùng #6b7280. -->
BookingFormModal.vue:2787: `.text-muted`: SCSS toàn cục ép nó thành đỏ (CLAUDE.md), user tưởng...
```
Cả 2 dòng là COMMENT cảnh báo không dùng, không phải usage thật. **0 dòng dùng class `.text-muted`.**

### #4 — Nút mới: `mr-2 mb-2` + `v-if` (không `disabled`)

Đã rà toàn bộ nút mới (footer popup: Duyệt/Đã chuẩn bị dịch vụ/Từ chối/Hủy phiếu/Từ chối dịch vụ/Lưu
đều `mr-2 mb-2`, Đóng cuối cụm chỉ `mb-2`; nút "Thêm dòng" đứng riêng lẻ không cần `mr-2`; nút xoá
dòng `V2BaseIconButton` trong ô bảng không thuộc cụm toolbar/footer nên không áp quy tắc này). Mọi
nút điều kiện hiện đều qua `v-if`, KHÔNG có `:disabled`/`interactable=false` nào dùng để ẨN nút (chỉ
`:interactable="!isSubmitSave"` trên nút Lưu — đó là khoá double-submit, không phải gate quyền).

### #5 — Static check thay Playwright (không mở trình duyệt)

`vue-template-compiler` compile cả 2 `<template>` — **0 lỗi**. `@babel/parser` parse cả 2 `<script>`
(sourceType module) — **0 lỗi cú pháp**. `git diff` chỉ đúng 2 file trong phạm vi, EOL thuần LF (`grep
-c $'\r'` = 0 cả 2 file).

## Chỗ tự quyết khác (nhỏ, không cần xác nhận riêng)

- **Không dùng `V2BaseCurrencyInput` cho ô số lượng** dù brief/spec nhắc "hiển thị 1,234.5 chuẩn quốc
  tế": rà project (`grep -rln "V2BaseCurrencyInput"` rồi đối chiếu `WrMerchandiseTable.vue`) thấy
  convention SẴN CÓ cho cặp "số lượng/đơn giá" là `V2BaseInput` (số lượng) + `V2BaseCurrencyInput`
  (tiền) — không có tiền lệ dùng currency-format cho ô số lượng thuần. Áp dụng: ô NHẬP dùng
  `V2BaseInput` trần (đúng nếp), còn yêu cầu "1,234.5 chuẩn quốc tế" áp cho khối CHỈ ĐỌC (Sửa/Xem) qua
  `formatQuantity()`.
- **Bỏ `:allowClear="false"` khỏi select "Món"**: brief/spec không nói rõ, nhưng skill
  select-and-input-state mục 1b cấm tắt nút xoá nhanh cho trường nghiệp vụ bình thường kể cả bắt
  buộc — giữ mặc định `true` (component đã tự bật sẵn).
- **Toàn bộ khối dịch vụ KHÔNG dùng `vee-validate`** — khớp đúng file GỐC (đã grep xác nhận file này
  chưa từng dùng `v-validate`/`$validator` ở bất kỳ đâu, kể cả trước khi tôi sửa): mọi validate hiện
  có của `BookingFormModal.vue` đều đi qua BE 422 → `this.error`. Bám theo nếp CHÍNH FILE ĐANG SỬA
  (ưu tiên hơn skill form-validate chung, vì đây không phải "màn hoàn toàn mới" mà là mở rộng 1 form
  đã có sẵn convention riêng).

## Người điều phối cần đo gì trên trình duyệt

### A. Popup Tạo mới — khối nhập dịch vụ (T138)

1. Mở `/meeting/bookings`, bấm "Tạo mới" → chọn hướng **"Nhu cầu khác"** → chọn 1 **phòng có người
   phụ trách** (vd phòng đã gán quản lý ở `/meeting/rooms`). Đo: khối "Yêu cầu dịch vụ" xuất hiện
   ngay dưới "Ghi chú", có bảng 3 cột (Món/Số lượng/Ghi chú) + nút "Thêm dòng".
2. Chọn **phòng KHÔNG có người phụ trách** (nếu có dữ liệu; hoặc tạo tạm 1 phòng test không gán
   quản lý). Đo: khối nhập biến mất, thay bằng 1 dòng chữ. `getComputedStyle(dòng đó).color` phải ra
   `rgb(107, 114, 128)` (= `#6b7280`), KHÔNG phải `rgb(220, 53, 69)` (đỏ của `.text-muted`).
3. Bấm "Thêm dòng" 2 lần → chọn CÙNG 1 món ở dòng 1 → mở dropdown dòng 2: đếm số option, đối chiếu
   với dropdown dòng 1 lúc chưa chọn gì — dòng 2 phải THIẾU đúng 1 option (món đã chọn ở dòng 1).
4. Bấm "Thêm dòng" 1 dòng, ĐỂ TRỐNG cả 3 ô, bấm Lưu (chặn `waitForResponse` hoặc `route.abort` cho
   `meeting/room-bookings` nếu muốn tái hiện lỗi có kiểm soát, hoặc cứ để gọi thật). Đo: dưới ô "Món"
   của dòng đó phải hiện `.v2-error` màu đỏ (không phải toast chung chung), chữ trong ô "Món" GIỮ
   NGUYÊN (không bị BE hay FE tự điền/xoá).
5. Đổi "Hướng đăng ký" sang **"Gắn với cuộc họp"**: đo khối "Yêu cầu dịch vụ" KHÔNG xuất hiện (đúng
   quyết định tự chốt — xin xác nhận riêng ở mục "Tự quyết" trên trước, nếu coordinator muốn hiện cả
   2 hướng thì đây là điểm cần sửa lại sau khi có BE task tương ứng).
6. Đo khoảng cách 2 nút "Xóa dòng" và nút liền kề nếu có nhiều dòng (không bắt buộc theo brief nhưng
   nên đo cho chắc — brief chỉ yêu cầu đo cụm nút FOOTER, xem mục D).

### B. Màn Sửa phiếu — khối chỉ đọc (T139)

7. Tạo 1 phiếu có ≥1 dịch vụ (bước A), Lưu xong → bấm "Sửa" phiếu đó. Đo: khối "Yêu cầu dịch vụ"
   hiện đúng số dòng đã tạo, KHÔNG có nút thêm/xoá dòng nào (đếm `V2BaseIconButton`/`button` trong
   khối này phải = 0), KHÔNG ô nào bấm sửa được (thử click vào ô "Món" — không mở dropdown).
8. Sửa phiếu KHÔNG có dịch vụ nào → đo khối "Yêu cầu dịch vụ" KHÔNG xuất hiện ở màn Sửa (không phải
   dòng trống).

### C. Popup Xem — badge + xử lý (T139/T140)

9. Mở popup Xem phiếu có dịch vụ (trạng thái "Chờ chuẩn bị"). Đo: badge cạnh tiêu đề "Yêu cầu dịch
   vụ" có `background-color`/`color` khớp `service_status_color` BE trả (F12 → Network xem response
   `GET meeting/room-bookings/{id}`, so với `getComputedStyle(badge).backgroundColor`/`.color`).
10. **Đăng nhập bằng tài khoản LÀ người phụ trách phòng đó** (hoặc 1 trong nhóm phụ trách), mở lại
    popup Xem phiếu "Chờ chuẩn bị": đo 2 nút "Đã chuẩn bị dịch vụ" (xanh teal `#1abc9c`) và "Từ chối
    dịch vụ" (đỏ) CÓ trong DOM, đứng cạnh Duyệt/Từ chối(phiếu)/Hủy phiếu (tuỳ cờ). Đo khoảng cách
    `getBoundingClientRect()` giữa 2 nút LIỀN KỀ bất kỳ trong cụm — phải đúng **12px** cả 6 cặp nút.
11. **Đăng nhập bằng tài khoản NGOÀI nhóm phụ trách** (không phải quản lý phòng), mở cùng phiếu: đo
    `document.querySelector('[data-testid="booking-service-prepared-button"]')` phải `=== null` (ẨN
    HẲN khỏi DOM, không phải `display:none`/disabled).
12. Bấm "Đã chuẩn bị dịch vụ" (tài khoản có quyền) → xác nhận popup `$confirm` hiện đúng tên phiếu +
    thời gian → bấm Xác nhận → đo: popup Xem đóng, toast thành công, danh sách nạp lại, badge ở dòng
    đó đổi màu/chữ đúng "Đã chuẩn bị" (`#16A34A`).
13. **Tái hiện 409**: mở phiếu "Chờ chuẩn bị" ở 2 tab (2 tài khoản khác nhau CÙNG trong nhóm phụ
    trách) → tab 1 bấm "Đã chuẩn bị dịch vụ" trước → tab 2 bấm SAU (không reload). Đo: tab 2 hiện
    toast lỗi ĐÚNG câu BE trả (chứa tên người đã xử lý + thời gian, KHÔNG phải "Có lỗi xảy ra"), sau
    đó nút "Đã chuẩn bị dịch vụ"/"Từ chối dịch vụ" ở tab 2 BIẾN MẤT khỏi DOM ngay (không cần F5).
14. Bấm "Từ chối dịch vụ" → không nhập lý do, bấm nút xác nhận trong popup: đo popup KHÔNG đóng (lý
    do bắt buộc). Nhập lý do rồi xác nhận → đo: thành công, mở lại popup Xem phiếu đó thấy dòng "Lý
    do từ chối" + "Người xử lý" + "Thời gian xử lý", màu chữ nhãn = `rgb(107, 114, 128)` (#6b7280),
    giá trị = `rgb(55, 65, 81)` (#374151), `font-weight` KHÔNG phải `bold`/`700`.

### D. Màn danh sách (T141)

15. Mở `/meeting/bookings`, bấm nút "Cấu hình cột hiển thị" → tick "Dịch vụ" → đo cột mới xuất hiện,
    ô của phiếu có dịch vụ hiện badge đúng màu BE trả, ô của phiếu KHÔNG có dịch vụ HOÀN TOÀN TRỐNG
    (không có text "Không có" hay `-`).
16. Mở khối "Tìm kiếm nâng cao" (hoặc bộ lọc gọn nếu ≤3 ô), đo có ô "Trạng thái dịch vụ" với 4 lựa
    chọn (Chờ chuẩn bị/Đã chuẩn bị/Từ chối/Không có yêu cầu), nhãn floating hoạt động đúng (nhãn nằm
    giữa ô khi rỗng, bay lên khi chọn giá trị — vì màn này đã bật `floating`).
    ⚠️ **ĐO XONG SẼ THẤY BỘ LỌC KHÔNG LỌC ĐƯỢC GÌ** — đây là hệ quả CHỦ Ý đã ghi rõ ở mục "LỆCH CODE
    THẬT" trên: BE `index()` chưa đọc tham số `service_status`. KHÔNG phải bug FE, ĐỪNG báo lại như
    một bug mới — cần quyết định có mở BE task hay tạm ẩn ô lọc.
17. Kiểm Network tab khi đổi ô lọc "Trạng thái dịch vụ": xác nhận request gửi đúng
    `service_status=1`/`2`/`3`/`none` tuỳ lựa chọn (đúng convention để BE cắm thêm sau).

## Danh sách file sửa (đầy đủ)

- `pages/meeting/bookings/components/BookingFormModal.vue`
- `pages/meeting/bookings/index.vue`

Không sửa file nào khác, không đụng `hrm-api`.
