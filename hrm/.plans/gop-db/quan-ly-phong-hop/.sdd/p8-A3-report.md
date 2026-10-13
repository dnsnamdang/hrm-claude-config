# Báo cáo — Phase 8 / lượt A3 (T118–T120): FE `hrm-client` theo kịp "nhiều người phụ trách phòng"

Nhánh: `gop_db`. Chỉ sửa `hrm-client`. KHÔNG đụng `hrm-api` (chỉ đọc để đối chiếu hợp đồng API).
KHÔNG chạy Playwright/mở trình duyệt — theo đúng ràng buộc của brief, mọi phép đo trên trình
duyệt thật để người điều phối làm sau (xem mục cuối).

## Đối chiếu hợp đồng API (đọc hrm-api, không sửa)

Đã đọc và xác nhận khớp với bảng hợp đồng trong brief:

- `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php` (dùng cho `GET meeting/rooms`
  — màn danh sách): trả `manager_employee_ids` (mảng id), `manager_names` (mảng tên, **cùng thứ tự**
  với `manager_employee_ids`), `manager_name` (chuỗi ghép `"; "`, không bao giờ `null`).
- `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php` (dùng cho
  `GET meeting/rooms/{id}` — modal Sửa/Xem): trả đúng 3 khoá y hệt.
- `Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php` (dùng cho
  `GET meeting/rooms/bookable` — modal Đặt phòng): CHỈ trả `manager_name` (chuỗi ghép `"; "`),
  KHÔNG trả `manager_employee_ids`/`manager_names` (cố ý, để không lộ id thô người phụ trách cho
  endpoint không gate quyền — đọc comment trong file, hợp lý).
- `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`: `manager_employee_ids` =
  `['required', 'array', 'min:1']`, `manager_employee_ids.*` = `['integer', 'exists:employees,id']`.
  Không còn rule nào cho `manager_employee_id` số ít.
- `Modules/Meeting/Entities/MeetingRoom.php` — `managerIds()` và `managerNames()` cùng dựng từ một
  `loadedManagers()` (load 1 lần, `orderBy('meeting_room_managers.id')` tường minh) nên 2 mảng
  **chắc chắn cùng thứ tự** — khớp giả định "vá theo cùng chỉ số" của brief.

Không có chỗ nào brief lệch code thật.

## T118 — `pages/meeting/rooms/components/MeetingRoomModal.vue`

File: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client/pages/meeting/rooms/components/MeetingRoomModal.vue`

1. **Ô "Người quản lý" → chọn nhiều, bắt buộc** (dòng ~74-95): `V2BaseLabel required`, đổi
   `v-model="data.manager_employee_id"` → `v-model="data.manager_employee_ids"`, thêm
   `:extraSettings="{ multiple: true }"` (đúng cách khai của ô "Tiện nghi" cùng file, dòng ~118 —
   copy nguyên khuôn, không tự chế). Lỗi hiện qua `V2BaseError` dựa vào `error.manager_employee_ids`
   — **giống hệt cách các ô khác của form này đang làm** (BE trả 422 vào `error`, FE chỉ hiển thị,
   KHÔNG tự chặn submit ở FE — cùng cách "Tên phòng" đang làm, không thêm cơ chế mới).
2. `emptyData()`: `manager_employee_id: null` → `manager_employee_ids: []`.
3. `loadData()`: đọc `detail.manager_employee_ids` (map `Number()`) + `detail.manager_names`, dựng
   `managerLockedOptions` (xem mục 5).
4. `submitSave()`: payload `manager_employee_ids: this.data.manager_employee_ids || []` (mảng), bỏ
   khoá số ít cũ.
5. `computed.employeeOptions` không còn đọc `this.data.manager_employee_ids` trực tiếp mà ghép từ
   `data.managerLockedOptions` (xem mục 5).
6. Component: giữ `V2BaseSelectInModal` (đúng vì trong modal). Nhãn nhân viên vẫn dùng
   `employeeOptionText()` (`utils/employeeOptionText.js`) — không đổi, đã đúng khuôn từ trước.

### Mục 5 — cơ chế vá option người đã nghỉ việc (điểm phải tự quyết)

Brief yêu cầu giữ cơ chế vá nhưng mở rộng cho TỪNG người. Bản thân việc mở rộng này **dẫm đúng vào
bẫy đã tài liệu hoá ở `select-and-input-state/SKILL.md` mục 2b**: nếu option vá được tính lại mỗi
khi `data.manager_employee_ids` đổi (tức là mỗi lần user tick thêm 1 người), `employeeOptions` sinh
ra mảng MỚI mỗi lượt tick → `V2BaseSelectInModal` (multiple) thấy prop `options` đổi tham chiếu →
select2 dựng lại → **mất sạch các lựa chọn đã tick trước đó khi tích người thứ 2 trở đi**. Skill nói
rõ trường hợp này (giữ giá trị khoá cũ ở màn Sửa) **không được dùng cờ `keep-locked-options`**, phải
"tìm cách khác".

Cách tôi chọn — tách phần vá ra khỏi vòng phản ứng theo lựa chọn đang tick:

- Thêm `data.managerLockedOptions: []` — mảng "vá" tính **MỘT LẦN** trong `loadData()` (lúc mở modal
  Sửa/Xem, dựa vào `detail.manager_employee_ids` + `detail.manager_names` của response, KHÔNG dựa
  vào state đang chọn hiện tại), lọc bỏ id nào đã có sẵn trong `$store.state.employees`.
- `employeeOptions` computed chỉ phụ thuộc `$store.state.employees` + `data.managerLockedOptions` —
  hai nguồn này **không đổi khi user tick/bỏ tick** trong lúc đang sửa, nên tham chiếu mảng ổn định
  suốt phiên sửa, select2 không bị dựng lại giữa chừng.
- `resetLocalData()` reset `managerLockedOptions = []` cùng lúc với `emptyData()`.

**Giải thích luồng theo đúng mục 3 của "cách tự kiểm" trong brief** — phòng có 2 người quản lý, 1
người đã nghỉ việc:

1. Mở Sửa: `GET meeting/rooms/{id}` trả `manager_employee_ids: [10, 99]`,
   `manager_names: ["Nguyễn Văn A", "Trần Thị B (đã nghỉ)"]`. Giả sử id `10` còn trong
   `$store.state.employees`, id `99` thì không.
2. `loadData()` gán `data.manager_employee_ids = [10, 99]`, và dựng
   `managerLockedOptions = [{ id: 99, name: "Trần Thị B (đã nghỉ)", is_locked: true }]` (chỉ id
   không có trong store).
3. `employeeOptions` = toàn bộ nhân viên đang làm việc (có id `10`) + option vá (id `99`,
   `is_locked: true`). Select hiện ĐỦ 2 chip: "Nguyễn Văn A" (bình thường) và
   "🔒 Trần Thị B (đã nghỉ)" (được `select2LockedOption.js` tự gắn 🔒, không cần khai gì thêm).
4. User không đụng gì tới ô này (hoặc tick thêm người thứ 3, thứ 4) — `managerLockedOptions` không
   đổi trong suốt phiên sửa nên option vá cho id `99` **không biến mất** giữa chừng (đây chính là
   bẫy mục 2b nếu làm sai).
5. Bấm Lưu: `data.manager_employee_ids` vẫn là `[10, 99, ...]` (thêm id mới nếu có) →
   payload gửi đúng `manager_employee_ids: [10, 99, ...]`. Người đã nghỉ việc (`99`) **không bị mất**
   khỏi phòng khi lưu lại.
6. Nếu user chủ động BỎ tick "🔒 Trần Thị B (đã nghỉ)" thì `data.manager_employee_ids` chỉ còn
   `[10]`, lưu lại thì id `99` bị gỡ khỏi phòng — đúng ý muốn của user (chủ động xoá người quản lý
   đã nghỉ việc), không phải bug.

## T119 — `pages/meeting/rooms/index.vue`

File: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client/pages/meeting/rooms/index.vue`

1. `#cell-manager_name` (dòng ~150-162): đổi nguồn từ `item.manager_name` (chuỗi) sang
   `item.manager_names` (mảng). Hiện tối đa 2 tên đầu, thêm ` +N` khi > 2 (method mới
   `managerNamesSummary()`), thuộc tính `title` chứa **đủ** danh sách ngăn bằng `, `. Mảng rỗng →
   `v-if` false → ô để trống hẳn, KHÔNG in "Chưa có" (đúng list-page SKILL mục 3b-3).
2. Chữ vẫn dùng `field-line text-dark font-weight-normal` (đã đúng sẵn từ trước, không đổi) —
   `font-weight: 400`.
3. Map import (dòng ~1032, nay ~1058 sau khi thêm comment):
   `manager_name: String(row.ManagerName || '').trim()` — **giữ nguyên, không cần sửa code** (đã
   đúng theo brief). Chỉ bổ sung dòng mô tả cột import: đổi `label` của cột `ManagerName` (dòng
   ~470-482) thành `'Người quản lý (nhiều người ngăn bởi dấu ";")'` + thêm alias tương ứng, và nới
   `width` từ `200px` → `260px` cho vừa nhãn dài hơn.
4. `exportFields` (`{ id: 'manager_name', name: 'Người quản lý' }`, dòng ~427/436) và khai cột bảng
   `{ key: 'manager_name', title: 'Người quản lý', minWidth, ... }` (dòng ~565/581) **vẫn khớp**:
   cả 2 chỗ đều dùng khoá `manager_name` — export dùng đúng khoá BE `MeetingRoomResource` trả
   (chuỗi ghép `"; "`, hợp lý cho file Excel/1 dòng text), còn cột bảng tôi CỐ Ý **giữ nguyên key**
   `manager_name` (không đổi sang `manager_names`) để không phá cấu hình cột đã lưu của user
   (`column_customizations`, xem list-page SKILL mục 4 — đổi key coi là cột MỚI, không cần ở đây vì
   ý nghĩa cột không đổi, chỉ đổi NGUỒN dữ liệu hiển thị bên trong slot). Nới `minWidth` từ `160px`
   lên `200px` để 2 tên + "+N" không bị bóp quá chật.

Không có ô lọc nào tham chiếu `manager_employee_id` (đã grep, rỗng) nên không phải sửa filter.

## T120 — `pages/meeting/bookings/components/BookingFormModal.vue`

**Kết luận: KHÔNG PHẢI SỬA CODE.** Đã đọc kỹ cả 2 chỗ BE và FE:

- Panel phải (dòng ~464-467): `v-if="selectedRoomInfo.manager_name"` + hiện
  `{{ selectedRoomInfo.manager_name }}`, nhãn `"Quản lý"`.
- Câu gợi ý gửi duyệt (dòng ~1924-1938): `receiver = room.manager_name || 'quản lý phòng'`, dùng
  trong `Người duyệt: {{ receiver }}` và câu `Phiếu ở trạng thái Chờ duyệt cho tới khi ${receiver}
  duyệt.`.
- `selectedRoomInfo` (computed, dòng ~961-970) lấy từ `allBookableRoomsRaw` (`GET
  meeting/rooms/bookable`) khi Thêm/Sửa, hoặc `viewDetail.room` khi Xem.
- Đọc `BookableMeetingRoomResource.php`: field `'manager_name' => implode('; ', $this->managerNames())`
  — đúng khoá `manager_name` mà FE đang đọc, giá trị đã là chuỗi ghép nhiều tên bằng `"; "`. Comment
  trong file BE còn ghi rõ: *"tình cờ khớp lại đúng khoá FE `BookingFormModal.vue` đang đọc — sửa
  xong không cần đợi lượt FE nữa"*.

Nhãn: brief chỉ yêu cầu sửa nếu đang ghi SỐ ÍT kiểu "Người phụ trách". Nhãn hiện tại là **"Quản lý"**
(panel) và **"Người duyệt"** (popup xác nhận) — cả hai đều trung tính về số nhiều/số ít trong tiếng
Việt (không giống "Người phụ trách" hàm ý 1 người), nên **không sửa nhãn**.

⚠️ Điểm ghi nhận (không thuộc phạm vi T120, không sửa): khi phòng có ≥ 2 người quản lý, câu
`Phiếu ở trạng thái Chờ duyệt cho tới khi Nguyễn Văn A; Trần Thị B duyệt.` đọc hơi gượng (dấu `;`
giữa câu văn) — đây là hệ quả trực tiếp của thiết kế `manager_name` (chuỗi ghép `"; "` dùng cho "chỗ
chỉ cần 1 dòng text") mà brief đã xác nhận đúng hợp đồng, không phải lỗi FE. Nêu ra để người điều
phối cân nhắc có cần tách câu văn khác (vd liệt kê bằng dấu phẩy khi hiện trong câu) ở lượt sau hay
không — KHÔNG tự quyết định sửa vì đây là quyết định về hành văn nghiệp vụ, ngoài phạm vi brief.

## Kết quả 4 mục tự kiểm (brief mục "Cách tự kiểm")

1. `grep -rn "manager_employee_id\b" pages components | grep -v manager_employee_ids` → **RỖNG**
   (đã chạy, không còn chỗ nào dùng khoá số ít cũ).
2. `grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/meeting/rooms | grep -v V2Base`
   → ra 2 dòng, cả hai đều **có sẵn từ trước** (không phải do tôi thêm):
   `index.vue:107` (comment) và `index.vue:110`
   (`<button type="button" class="v2-cell-link field-line text-wrap" @click="viewItem(item)">`).
   Đây là mẫu `<button class="v2-cell-link">` cho cột định danh mở modal Xem — đúng ngoại lệ đã
   liệt kê ở `list-page/SKILL.md` mục 3a ("Màn DANH MỤC dùng modal ... Cột định danh là
   `<button class="v2-cell-link field-line">`"), không phải HTML thô cần dọn.
3. Giải thích luồng vá option người nghỉ việc — xem mục T118 phần "Mục 5" ở trên (6 bước, kèm lý do
   kỹ thuật vì sao tách `managerLockedOptions` ra khỏi computed phụ thuộc giá trị đang chọn).
4. Lint: **dự án KHÔNG có script `lint`** (`package.json` chỉ có `dev`/`build`/`build:fresh`/
   `start`/`generate`) và **không có binary `eslint`** trong `node_modules/.bin` → không chạy được,
   không có kết quả để dán. Có `.prettierrc` (`semi: false`, `singleQuote: true`, `tabWidth: 4`,
   `printWidth: 120`) — code mới viết tuân theo (đã đối chiếu style file hiện có, kể cả cách dùng
   `;(...)` đầu dòng khi statement bắt đầu bằng `(` — đúng convention đã thấy lặp lại ở nhiều file
   khác trong repo, vd `pages/assign/meeting/components/MeetingForm.vue:561`).

## File đã sửa

- `HRM/hrm-client/pages/meeting/rooms/components/MeetingRoomModal.vue`
- `HRM/hrm-client/pages/meeting/rooms/index.vue`
- `HRM/hrm-client/pages/meeting/bookings/components/BookingFormModal.vue` — **KHÔNG sửa**, chỉ đọc
  và xác nhận đã đúng (ghi rõ ở đây theo yêu cầu brief).

## Những điểm tôi phải tự quyết (không hỏi lại vì đủ căn cứ trong brief/skill)

1. Cách vá option cho nhiều người (tách khỏi computed phụ thuộc giá trị đang chọn) — theo đúng
   hướng dẫn "tìm cách khác" của skill mục 2b, đã giải trình ở trên.
2. Không đổi `key` cột `manager_name` ở `index.vue` (giữ nguyên để không phá cấu hình cột đã lưu
   của user) — hợp lý vì Ý NGHĨA cột không đổi (vẫn là "Người quản lý"), chỉ đổi cách tính hiển thị
   bên trong slot.
3. Không đổi gì ở `BookingFormModal.vue` — đã đọc BE Resource xác nhận khớp.
4. Không viết logic chặn submit ở FE cho "bắt buộc ≥ 1 người quản lý" — theo đúng pattern hiện có
   của form này (mọi validate khác đều dựa vào lỗi 422 từ BE, không có kiểm tra local trước submit).

## Người điều phối cần đo lại gì trên trình duyệt

### A. `MeetingRoomModal.vue` — modal Thêm/Sửa/Xem phòng họp (`/meeting/rooms`)

1. **Thêm phòng mới, không chọn Người quản lý, bấm Lưu** → phải thấy lỗi đỏ inline ngay dưới ô
   "Người quản lý" (không phải toast), nhãn có dấu `*` đỏ. Đo bằng DOM:
   `document.querySelector('.v2-input-error')` (hoặc class `V2BaseError` thật sự render ra) có nội
   dung, và ô select có class `is-invalid` / viền đỏ.
2. **Thêm phòng mới, chọn 2 người quản lý, Lưu** → mở lại (Sửa) phải thấy đúng 2 chip, đúng thứ tự
   đã chọn hoặc theo thứ tự BE trả (`managerIds()`/`managerNames()` theo `meeting_room_managers.id`
   tăng dần) — không thiếu, không lặp.
3. **Kịch bản trọng tâm — người đã nghỉ việc** (cần chuẩn bị dữ liệu: 1 phòng có ≥ 2 quản lý, sau đó
   cho 1 người nghỉ việc/xoá khỏi employees đang hoạt động, hoặc tìm phòng đã có sẵn dữ liệu tương
   tự trong DB thật):
   - Mở Sửa → phải thấy ĐỦ chip của người đã nghỉ việc, có tiền tố `🔒 ` ở TRƯỚC tên (cả ở
     dropdown lẫn ở chip đang hiển thị — đo bằng `getComputedStyle`/`textContent` của
     `.select2-selection__choice`).
   - **Tick thêm 1 người quản lý thứ 3** (người đang làm việc) — chip của người đã nghỉ việc
     (🔒) và chip vừa chọn trước đó KHÔNG được biến mất. Đây là phép đo trực tiếp bẫy mục 2b đã nêu
     trong báo cáo — đếm số `.select2-selection__choice` trước và sau khi tick, phải tăng đúng 1,
     không giảm về 0.
   - Lưu lại → mở lại lần nữa, người đã nghỉ việc vẫn còn trong `manager_employee_ids` (kiểm qua
     Network tab response của `GET meeting/rooms/{id}` sau khi lưu).
4. **Popup lồng "Thêm nhanh tiện nghi"** (nút "Thêm tiện nghi") — không liên quan trực tiếp task
   này nhưng nằm cùng modal, kiểm nhanh không bị vỡ do đổi cấu trúc `data`.
5. Đo `.select2-selection__choice` cho ô "Người quản lý" đúng khuôn chip chung (nền `#eff6ff`, viền
   `#bfdbfe`, chữ `#1e40af`, bo góc `5px`) — component dùng chung nên khả năng cao đã đúng, đo 1
   lần cho chắc.

### B. `index.vue` — màn danh sách (`/meeting/rooms`)

1. Bật cột "Người quản lý" trong "Cấu hình cột hiển thị" (mặc định `isVisible: false`).
2. Phòng có 1 người quản lý → ô hiện đúng 1 tên, không có "+N", `title` = tên đó.
3. Phòng có > 2 người quản lý → ô hiện `"Tên A, Tên B +N"`, hover vào ô (đo `title` attribute qua
   DOM, không cần thật sự hover) phải thấy ĐỦ danh sách ngăn `, `.
4. Phòng KHÔNG có người quản lý nào (nếu tồn tại dữ liệu như vậy, hoặc test bằng phòng mới) → ô để
   TRẮNG HẲN, không có chữ "Chưa có" hay dấu gạch ngang.
5. Chữ trong ô: đo `getComputedStyle(el).fontWeight` phải là `"400"`, không phải `"700"`/`"bold"`.
6. **Import Excel**: mở modal Import, kiểm cột "Người quản lý" có hiện nhãn mới
   `'Người quản lý (nhiều người ngăn bởi dấu ";")'`. Thử import 1 dòng có ô `ManagerName` =
   `"Nguyễn Văn A; Trần Thị B"` → validate xong, kiểm phòng tạo ra có đủ 2 người quản lý (không thể
   kiểm bằng code tĩnh, cần chạy thật qua BE `resolveManagerIds()`).
7. **Xuất Excel**: xuất 1 phòng có nhiều quản lý → cột "Người quản lý" trong file ra đúng chuỗi
   `"A; B"` (không phải mảng/JSON thô).
8. Đối chiếu điểm 3g của skill list-page (không thuộc phạm vi sửa lần này nhưng nên tiện thể kiểm):
   cột "Người quản lý" hiện KHÔNG có `sortable` (kiểm bảng `tableColumns` không có `sortable: true`
   cho key này) — vì nội dung là mảng rút gọn, sort theo chuỗi ghép sẽ không khớp cái nhìn thấy;
   xác nhận đúng là KHÔNG bật sort (đã kiểm tĩnh: cột không khai `sortable`, chỉ cần xác nhận trên
   UI không có mũi tên sort ở tiêu đề cột này).

### C. `BookingFormModal.vue` — modal Đặt phòng (`/meeting/bookings`)

1. Mở form Thêm phiếu đặt phòng, chọn 1 phòng có ≥ 2 người quản lý → panel phải "Thông tin phòng"
   dòng "Quản lý" phải hiện ĐỦ các tên, ngăn bằng `"; "` (đo `textContent` của `.side-row__value`
   tương ứng).
2. Với phòng đó, bật `require_approval` (hoặc chọn sẵn phòng cần duyệt) rồi bấm "Lưu và gửi duyệt"
   → popup xác nhận phải hiện dòng "Người duyệt" với ĐỦ các tên (không chỉ 1 tên), và câu ghi chú
   dưới cùng cũng lặp lại đủ tên đó.
3. Mở phiếu đã tạo ở chế độ Xem (`isShow`) — kiểm `viewDetail.room.manager_name` cũng ra đúng chuỗi
   ghép nhiều tên (không rớt về `null`/rỗng) khi BE trả kèm trong response chi tiết phiếu.
