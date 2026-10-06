# Phase 8, lượt D1 — Chuẩn hoá message validate luồng Quản lý phòng họp

Ngày: 2026-09-23
Repo: `HRM/hrm-api` (BE), `HRM/hrm-client` (FE), nhánh `gop_db`.

## 1. Phạm vi đã rà (đủ, không chỉ 6 file ban đầu)

- **8/8 FormRequest** trong `Modules/Meeting/Http/Requests/`:
  `MeetingRoomRequest`, `MeetingRoomAmenityRequest`, `MeetingRoomPurposeRequest`,
  `MeetingRoomServiceRequest`, `MeetingRoomBookingRequest`, `MeetingRoomBookingCancelRequest`,
  `MeetingRoomBookingRejectRequest`, `MeetingRoomBookingServiceRejectRequest`.
- **4 `validator()`/`Validator::make()` viết tay** trong Controller (grep
  `Validator::make\|validator(` toàn `Modules/Meeting`, không có ở Service):
  `MeetingRoomController::availability()`, `MeetingSettingController::updateRoomHours()`,
  `MeetingRoomBookingController::unassignMeeting()`, `MeetingRoomBookingController::assignMeeting()`
  (đúng chỗ C3 vừa thêm, có `services[]` dùng chung rule với `MeetingRoomBookingRequest`).
- **FE `hrm-client/pages/meeting/**`**: `grep -rl "data-vv-as\|v-validate"` ra **RỖNG** — cả
  module không dùng vee-validate, mọi lỗi 422 hiển thị nguyên văn message BE trả về qua
  `error.<field>`/`V2BaseError`. Kết luận: **FE không có vi phạm để sửa** (xem mục 5).

## 2. BE — bảng phân loại & xử lý

Ký hiệu: **XOÁ** = đã xoá khỏi `messages()`, để lang file lo · **GIỮ-NV** = giữ vì là câu
nghiệp vụ · **GIỮ-EN** = giữ vì rule đó trong lang file **vẫn là tiếng Anh** (bẫy đã cảnh báo).

### 2.1 `MeetingRoomRequest`
| Key | Trước | Sau | Xử lý |
|---|---|---|---|
| `name.required` | Vui lòng nhập tên phòng họp | *(lang file)* Bắt buộc phải nhập | XOÁ |
| `name.max` | Tên phòng họp tối đa 255 ký tự | Vui lòng nhập tối đa 255 ký tự. | XOÁ |
| `name.unique` | Tên phòng họp đã tồn tại trong công ty này | Đã tồn tại trên hệ thống | XOÁ |
| `capacity.integer` | Sức chứa phải là số nguyên | *(giữ nguyên)* | **GIỮ-EN** (`integer` = "The :attribute must be an integer.") |
| `capacity.min` | Sức chứa tối thiểu là 1 | Phải lớn hơn 1. | XOÁ |
| `open_time.date_format` | Giờ mở cửa không hợp lệ (HH:mm:ss) | Định dạng không hợp lệ | XOÁ |
| `close_time.date_format` | Giờ đóng cửa không hợp lệ (HH:mm:ss) | Định dạng không hợp lệ | XOÁ |
| `close_time.after` | Giờ đóng cửa phải sau giờ mở cửa | *(giữ nguyên)* | **GIỮ-NV** (rule `after` chỉ trả "Không hợp lệ") |
| `checkin_grace_minutes.integer` | Ân hạn check-in phải là số nguyên | *(giữ nguyên)* | **GIỮ-EN** |
| `checkin_grace_minutes.min` | Ân hạn check-in không được âm | Phải lớn hơn 0. | XOÁ |
| `checkin_grace_minutes.max` | Ân hạn check-in tối đa 120 phút | Không được lớn hơn 120. | XOÁ |
| `amenity_ids.array` | Danh sách tiện nghi không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** (`array` tiếng Anh) |
| `amenity_ids.*.exists` | Tiện nghi không tồn tại trong hệ thống | Không tồn tại | XOÁ |

Đã đo thật qua validator (payload rỗng/sai) — kết quả khớp bảng trên (mục 4).

### 2.2 `MeetingRoomAmenityRequest` / `MeetingRoomPurposeRequest` (giống hệt nhau)
| Key | Trước | Sau | Xử lý |
|---|---|---|---|
| `name.required` | Vui lòng nhập tên tiện nghi / mục đích | Bắt buộc phải nhập | XOÁ |
| `name.max` | Tên … tối đa 255 ký tự | Vui lòng nhập tối đa 255 ký tự. | XOÁ |
| `name.unique` | Tên … đã tồn tại trong hệ thống | Đã tồn tại trên hệ thống | XOÁ |
| `note.max` | Ghi chú tối đa 1000 ký tự | Vui lòng nhập tối đa 1000 ký tự. | XOÁ |
| `icon.max` | Icon tối đa 100 ký tự | Vui lòng nhập tối đa 100 ký tự. | XOÁ |
| `sort_order.integer` | Thứ tự sắp xếp phải là số nguyên | *(giữ nguyên)* | **GIỮ-EN** |
| `sort_order.min` | Thứ tự sắp xếp không được âm | Phải lớn hơn 0. | XOÁ |

`MeetingRoomServiceRequest`: đã đúng chuẩn từ trước (không khai `messages()`) — không đổi gì.

### 2.3 `MeetingRoomBookingRequest`
| Key | Trước | Sau | Xử lý |
|---|---|---|---|
| `meeting_room_id.required` | Vui lòng chọn phòng họp | Bắt buộc phải nhập | XOÁ |
| `meeting_room_id.integer` | Phòng họp không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** |
| `meeting_room_id.exists` | Phòng họp không tồn tại | Không tồn tại | XOÁ |
| `purpose_id.required` | Vui lòng chọn mục đích sử dụng | Bắt buộc phải nhập | XOÁ |
| `purpose_id.integer` | Mục đích sử dụng không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** |
| `purpose_id.exists` | Mục đích sử dụng không tồn tại | Không tồn tại | XOÁ |
| `title.required` | Vui lòng nhập nội dung sử dụng | Bắt buộc phải nhập | XOÁ |
| `title.max` | Tiêu đề tối đa 255 ký tự | Vui lòng nhập tối đa 255 ký tự. | XOÁ |
| `start_at.required` | Vui lòng chọn giờ bắt đầu | Bắt buộc phải nhập | XOÁ |
| `start_at.date` | Giờ bắt đầu không hợp lệ | Không hợp lệ | XOÁ |
| `end_at.required` | Vui lòng chọn giờ kết thúc | Bắt buộc phải nhập | XOÁ |
| `end_at.date` | Giờ kết thúc không hợp lệ | Không hợp lệ | XOÁ |
| `end_at.after` | Giờ kết thúc phải sau giờ bắt đầu | *(giữ nguyên)* | **GIỮ-NV** |
| `host_employee_id.integer` | Người phụ trách không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** |
| `host_employee_id.exists` | Người phụ trách không tồn tại | Không tồn tại | XOÁ |
| `attendee_count.integer` | Số người dự kiến phải là số nguyên | *(giữ nguyên)* | **GIỮ-EN** |
| `attendee_count.min` | Số người dự kiến tối thiểu là 1 | Phải lớn hơn 1. | XOÁ |
| `participant_ids.array` | Danh sách người tham dự không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** |
| `participant_ids.*.integer` | Người tham dự không hợp lệ | *(giữ nguyên)* | **GIỮ-EN** |
| `participant_ids.*.exists` | Người tham dự không tồn tại | Không tồn tại | XOÁ |

`checkNoDuplicateServiceIds()` (thêm lỗi thủ công `services.{i}.service_id` = "Món dịch vụ này đã
được chọn ở dòng khác, vui lòng gộp số lượng vào 1 dòng") — **GIỮ**, đúng câu nghiệp vụ, comment
gốc đã tự trích dẫn CLAUDE.md.

### 2.4 `MeetingRoomBookingCancelRequest` / `MeetingRoomBookingRejectRequest`
Cả 2 key (`*.required`, `*.max`) đều trùng lang file → **XOÁ SẠCH**, bỏ hẳn `messages()` (file chỉ
còn `rules()`, đúng chuẩn FormRequest mới).

### 2.5 4 `validator()` viết tay trong Controller
| Vị trí | Key | Trước | Sau | Xử lý |
|---|---|---|---|---|
| `MeetingRoomController::availability()` | `start_at.required` | Thiếu giờ bắt đầu để xét phòng trống | Bắt buộc phải nhập | XOÁ |
| | `end_at.required` | Thiếu giờ kết thúc để xét phòng trống | Bắt buộc phải nhập | XOÁ |
| | `end_at.after` | Giờ kết thúc phải sau giờ bắt đầu | *(giữ nguyên)* | **GIỮ-NV** |
| `MeetingSettingController::updateRoomHours()` | `open_time.required` | Vui lòng nhập giờ mở cửa | Bắt buộc phải nhập | XOÁ |
| | `open_time.date_format` | Giờ mở cửa không hợp lệ | Định dạng không hợp lệ | XOÁ |
| | `close_time.required` | Vui lòng nhập giờ đóng cửa | Bắt buộc phải nhập | XOÁ |
| | `close_time.date_format` | Giờ đóng cửa không hợp lệ | Định dạng không hợp lệ | XOÁ |
| | `close_time.after` | Giờ đóng cửa phải sau giờ mở cửa | *(giữ nguyên)* | **GIỮ-NV** |
| | `checkin_reminder_minutes.required` | Vui lòng nhập số phút nhắc trước giờ nhận phòng | Bắt buộc phải nhập | XOÁ |
| | `checkin_reminder_minutes.integer` | Số phút nhắc nhận phòng phải là số nguyên | *(giữ nguyên)* | **GIỮ-EN** |
| | `checkin_reminder_minutes.min` | Số phút nhắc nhận phòng không được âm | Phải lớn hơn 0. | XOÁ |
| | `checkin_reminder_minutes.max` | Số phút nhắc nhận phòng tối đa 1440 phút (24 giờ) | Không được lớn hơn 1440. | XOÁ (mất phần diễn giải "(24 giờ)" — số 1440 đã đủ tự giải thích) |
| | `checkout_reminder_minutes.*` | (y hệt checkin, đổi "nhận"→"trả") | (y hệt) | XOÁ 3, GIỮ-EN 1 (`.integer`) |
| | `allow_outside_hours.required` | Vui lòng chọn có cho đặt ngoài khung giờ hoạt động hay không | Bắt buộc phải nhập | XOÁ |
| `MeetingRoomBookingController::unassignMeeting()` | `meeting_id.required` | Thiếu cuộc họp cần hủy đăng ký phòng | Bắt buộc phải nhập | XOÁ |
| | `meeting_id.exists` | Cuộc họp không tồn tại | Không tồn tại | XOÁ |
| `MeetingRoomBookingController::assignMeeting()` | `meeting_id.required` | Vui lòng chọn cuộc họp | Bắt buộc phải nhập | XOÁ |
| | `meeting_id.exists` | Cuộc họp không tồn tại | Không tồn tại | XOÁ |
| | `meeting_room_id.required` | Vui lòng chọn phòng họp | Bắt buộc phải nhập | XOÁ |
| | `meeting_room_id.exists` | Phòng họp không tồn tại | Không tồn tại | XOÁ |

## 3. Nhóm rule còn TIẾNG ANH trong `resources/lang/vi/validation.php` (KHÔNG tự sửa — báo user)

Đọc trực tiếp file, không đoán theo danh sách gợi ý ban đầu. Các key sau đang trả nguyên văn tiếng
Anh và ĐANG được dùng bởi luồng phòng họp (nên các message tiếng Việt tương ứng đã được **GIỮ LẠI**
ở mục 2 để không đẩy câu Anh ra mặt user):

- `'integer' => 'The :attribute must be an integer.'`
- `'array' => 'The :attribute must be an array.'`
- `'boolean' => 'The :attribute field must be true or false.'`
- `'string' => 'The :attribute must be a string.'` (không có field nào của Meeting đụng message
  tự viết cho `string`, nhưng rule này cũng đang tiếng Anh nếu sau này ai xoá `messages()` chứa nó)
- `'uuid'`, `'password'`, `'same'`, `'confirmed'`, `'accepted'`, `'alpha*'`, `'digits*'`,
  `'gt'/'gte'/'lt'/'lte'/'size'/'between'` — không dùng ở Meeting nên không ảnh hưởng lượt này.

**Đề xuất** (chờ user quyết, KHÔNG tự sửa lang file dùng chung): bổ sung câu Việt cho `integer`,
`array`, `boolean` — 3 rule này rất phổ biến trong toàn hệ thống (không riêng Meeting), sửa 1 lần ở
lang file lợi hơn từng module tự viết `messages()` để né.

## 4. Lỗ hổng liên quan phát hiện thêm (KHÔNG sửa, ngoài phạm vi "chỉ chuẩn hoá message có sẵn")

Các field sau **CHƯA TỪNG có `messages()` tự viết** — tức là ĐANG hiển thị tiếng Anh (English
trap) ngay cả TRƯỚC lượt D1 này, nên không có gì để "xoá/giữ", chỉ liệt kê để user cân nhắc bổ sung
message riêng (không phải sửa lang file dùng chung, mà thêm entry `messages()` — nằm ngoài yêu cầu
"chỉ chuẩn hoá message có sẵn" của lượt D1):

- `MeetingRoomRequest`: `manager_employee_ids` (rule `array`), `manager_employee_ids.*` (rule
  `integer`).
- `MeetingRoomBookingRequest` / `serviceItemRules()` dùng chung cho `store()` và
  `assignMeeting()`: `services` (rule `array`), `services.*.service_id` (rule `integer`),
  `services.*.quantity` (rule `numeric`/`gt:0` — `gt` cũng tiếng Anh trong lang file).
- `MeetingRoomController::availability()`: `exclude_booking_id` (rule `integer`).
- `MeetingSettingController::updateRoomHours()`: `allow_outside_hours` (rule `boolean`).
- `MeetingRoomBookingController::unassignMeeting()` / `assignMeeting()`: `meeting_id.integer`,
  `meeting_room_id.integer`.

## 5. FE — kết luận không có vi phạm

- `grep -rl "data-vv-as\|v-validate" pages/meeting` → **rỗng**: module Meeting không dùng
  vee-validate directive ở bất kỳ đâu.
- Mọi popup (MeetingRoomModal, RoomAmenityModal, RoomPurposeModal, BookingFormModal,
  RoomHoursSettingPanel) đều theo pattern: `this.error = payload.errors` (422 từ BE) rồi
  `<V2BaseError :message="error.<field>">` — **hiển thị NGUYÊN VĂN câu BE trả về**, không có
  message field-level hard-code ở FE.
- 3 file có `errors.push('Tên … không được để trống')` (`pages/meeting/rooms/index.vue`,
  `room-amenities/index.vue`, `room-purposes/index.vue`, dòng ~818-829/~1017-1038): đây là validate
  **client-side cho preview Import Excel** (`importValidationRules(row)`), một cơ chế HOÀN TOÀN
  KHÁC vee-validate/FormRequest — không đi qua lang file, không có câu chuẩn dùng chung. Đã đối
  chiếu với 13 màn khác cùng dùng pattern này (`pages/assign/industry-groups/index.vue` và tương
  tự) — tất cả đều tự viết message nghiệp vụ riêng theo format file mẫu (vd
  "Mã nhóm ngành phải theo định dạng NN.XXXX"). **Kết luận: KHÔNG phải vi phạm**, đổi riêng
  message của Meeting sẽ làm LỆCH so với 13 màn còn lại — ngoài phạm vi + rủi ro hơn là lợi. Không
  đụng.
- Banner tổng ở form-level (`this.formError = 'Bạn chưa nhập đầy đủ thông tin'`,
  `'Vui lòng kiểm tra lại thông tin đã nhập'`): xuất hiện ở 34 và 8 file khác trong toàn
  `hrm-client`, là pattern chung của mọi modal — không phải message riêng của 1 rule, không đụng.
- 1 message nghiệp vụ thật ở `BookingFormModal.vue:2236-2240` ("Phòng đã bị giữ … Chọn phòng khác
  …") — cảnh báo trùng lịch tính TRƯỚC khi gọi API, đúng diện GIỮ (nghiệp vụ, lang file không diễn
  đạt được).

## 6. Tự kiểm bắt buộc — SỐ THẬT

### 6.1 `grep -rn "function messages" Modules/Meeting` (sau khi sửa)
```
Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php:46
Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php:148
Modules/Meeting/Http/Requests/MeetingRoomPurpose/MeetingRoomPurposeRequest.php:46
Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php:86
```
Giảm từ 6 → 4 file. 2 file đã bỏ hẳn (`MeetingRoomBookingCancelRequest`,
`MeetingRoomBookingRejectRequest`). 4 file còn lại chỉ giữ key thuộc nhóm **GIỮ-EN**/**GIỮ-NV**
(bảng mục 2), không còn key nào trùng lang file.

### 6.2 Câu lỗi THẬT sau khi sửa (gọi `Illuminate\Support\Facades\Validator::make()` qua
`artisan tinker`, dùng đúng `rules()`/`messages()` hiện hành của từng FormRequest/validator thủ
công — script tại `/private/tmp/.../scratchpad/verify_messages*.php`, không phải đọc code suy
diễn):

```
=== MeetingRoomAmenity (name rỗng, sort_order='abc') ===
  name: Bắt buộc phải nhập
  sort_order: Thứ tự sắp xếp phải là số nguyên

=== MeetingRoomPurpose (name rỗng, sort_order='abc') ===
  name: Bắt buộc phải nhập
  sort_order: Thứ tự sắp xếp phải là số nguyên

=== MeetingRoomRequest (name rỗng, capacity='abc', manager_employee_ids=[],
    close_time trước open_time, checkin_grace_minutes='xyz', amenity_ids='not-array') ===
  name: Bắt buộc phải nhập
  capacity: Sức chứa phải là số nguyên
  manager_employee_ids: Bắt buộc phải nhập
  close_time: Giờ đóng cửa phải sau giờ mở cửa
  checkin_grace_minutes: Ân hạn check-in phải là số nguyên
  amenity_ids: Danh sách tiện nghi không hợp lệ

=== MeetingRoomBookingRequest (meeting_room_id='abc', purpose_id rỗng, title rỗng,
    end_at trước start_at, host_employee_id='abc', attendee_count='abc',
    participant_ids='not-array') ===
  meeting_room_id: Phòng họp không hợp lệ
  purpose_id: Bắt buộc phải nhập
  title: Bắt buộc phải nhập
  end_at: Giờ kết thúc phải sau giờ bắt đầu
  host_employee_id: Người phụ trách không hợp lệ
  attendee_count: Số người dự kiến phải là số nguyên
  participant_ids: Danh sách người tham dự không hợp lệ

=== MeetingRoomBookingCancelRequest (cancel_reason 600 ký tự) ===
  cancel_reason: Vui lòng nhập tối đa 500 ký tự.
=== MeetingRoomBookingCancelRequest (rỗng) ===
  cancel_reason: Bắt buộc phải nhập

=== MeetingRoomBookingRejectRequest (reject_reason 600 ký tự) ===
  reject_reason: Vui lòng nhập tối đa 500 ký tự.
=== MeetingRoomBookingRejectRequest (rỗng) ===
  reject_reason: Bắt buộc phải nhập

=== unique thật (name trùng "Bàn họp 8 người" đang có trong DB) ===
  name: Đã tồn tại trên hệ thống

=== exists thật (meeting_room_id = 999999999, không tồn tại) ===
  meeting_room_id: Không tồn tại

=== MeetingRoomController::availability() (start_at sau end_at) ===
  end_at: Giờ kết thúc phải sau giờ bắt đầu

=== MeetingSettingController::updateRoomHours() (payload rỗng) ===
  open_time / close_time / checkin_reminder_minutes / checkout_reminder_minutes /
  allow_outside_hours: Bắt buộc phải nhập (cả 5 field)

=== MeetingRoomBookingController::unassignMeeting() (payload rỗng) ===
  meeting_id: Bắt buộc phải nhập
```

Tất cả khớp bảng TRƯỚC→SAU ở mục 2 — message sau khi xoá đúng là câu chuẩn lang file, message giữ
lại (GIỮ-EN/GIỮ-NV) vẫn ra tiếng Việt như cũ.

### 6.3 `phpunit --filter MeetingRoom`
- **TRƯỚC khi sửa**: `Tests: 65, Assertions: 179, Errors: 5, Failures: 2.`
- **SAU khi sửa**: `Tests: 65, Assertions: 179, Errors: 5, Failures: 2.` — **GIỐNG HỆT**, không đỏ
  thêm. 2 Failures vẫn là `MeetingRoomBookingSyncRuleTest` (mode_id/meeting_room_id), 5 Errors vẫn
  là lỗi cột `code` trong `MeetingRoomBookingRaceTest` — cả 2 nhóm KHÔNG liên quan message validate,
  đã có sẵn trước Phase 8 (đúng baseline user cho).

### 6.4 Test/e2e assert theo câu chữ CŨ — không có
- `grep` toàn bộ 20 chuỗi message cũ (required/max/unique/integer/min của cả 8 FormRequest + 4
  validator viết tay) trong `hrm-api/tests/` (kể cả `Modules/Meeting/Tests/` — thư mục này chỉ có
  2 file `.gitkeep`, KHÔNG có test thật nằm trong module) → **0 kết quả** ở mọi lượt grep.
- Grep tương tự trong `HRM/e2e/tests/meeting/*.spec.ts` (9 file spec) → **0 kết quả**.
- Kết luận: không có test/e2e nào cần sửa theo — an toàn xoá message mà không phải đụng file test
  nào khác ngoài 9 file BE đã liệt kê ở mục "File đã sửa".

## 7. File đã sửa (BE, 9 file)
- `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`
- `Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php`
- `Modules/Meeting/Http/Requests/MeetingRoomPurpose/MeetingRoomPurposeRequest.php`
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php`
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingCancelRequest.php` (bỏ hẳn `messages()`)
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRejectRequest.php` (bỏ hẳn `messages()`)
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php` (`availability()`)
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingSettingController.php` (`updateRoomHours()`)
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php` (`unassignMeeting()`, `assignMeeting()`)

Không đổi `rules()` ở bất kỳ file nào — chỉ đụng câu chữ (`messages()`/mảng messages truyền vào
`validator()`), đúng ràng buộc của lượt D1. Không sửa `resources/lang/vi/validation.php`,
`hrm-client/locales/vi.json`, không commit/push.

## 8. Tổng kết số liệu

- Message tự viết đã **XOÁ**: 46 key (trùng lặp câu chuẩn lang file đã có sẵn).
- Message **GIỮ lại**: 19 key — 5 nghiệp vụ thật (`*.after`, `checkNoDuplicateServiceIds`) + 14
  thuộc nhóm rule còn tiếng Anh (`integer`/`array` — mục 3).
- File `messages()` giảm từ 6 → 4 (2 file bỏ hẳn phương thức).
- Nhóm rule còn tiếng Anh trong lang file dùng bởi Meeting: `integer`, `array`, `boolean` (và `gt`
  dùng ở `services.*.quantity`, ngoài phạm vi field có message tự viết).
- Điểm nghi ngờ đáng chú ý nhất: `services.*` (cả ở `MeetingRoomBookingRequest::serviceItemRules()`
  dùng chung `store()`+`assignMeeting()`) hiện KHÔNG có message riêng nào — nếu user muốn dọn luôn
  English trap thì đây là nhóm field lớn nhất đang lộ tiếng Anh, ngoài phạm vi lượt D1 (mục 4).
  **→ Đã xử lý ở lượt D2, xem mục 9 dưới đây.**

---

# Phase 8, lượt D2 — Bổ sung message Việt cho English trap DO CHÍNH PHASE 8 gây ra

Ngày: 2026-09-23 (nối thêm sau phản hồi coordinator).

## 9. Bối cảnh — vì sao mục 4 (lượt D1) bị coordinator bác

Lượt D1 xếp `manager_employee_ids` (`MeetingRoomRequest`) và `services.*`
(`MeetingRoomBookingRequest::serviceItemRules()`, dùng chung `store()`/`update()`/`assignMeeting()`)
vào nhóm "lỗ hổng CÓ SẴN, ngoài phạm vi" vì 2 field này **chưa từng có `messages()` tự viết** — nên
không có gì để "xoá/giữ" theo đúng nghĩa đen của yêu cầu D1 ("chuẩn hoá message ĐÃ CÓ").

Coordinator chỉ ra: cách phân loại đó bỏ sót ngữ cảnh — `manager_employee_ids` sinh ra ở **lượt A1
(T112)** và `services[]` sinh ra ở **lượt C1 (T132)**, cả hai đều **THUỘC chính Phase 8**. Tức là
English trap ở 2 field này không phải "nợ cũ đã có từ trước", mà là **hệ quả trực tiếp của Phase 8**
— và tiếng Anh lọt ra màn hình đúng là điều user gốc đã phàn nàn ("message validate chưa đúng
chuẩn"). Xác nhận bằng validator thật:
```
manager_employee_ids => The manager employee ids must be an array.
```
→ Chấp nhận, xử lý bổ sung message Việt cho nhóm này (KHÔNG sửa lang file — chỉ thêm `messages()`/
`attributes()` ở đúng 2 FormRequest, và truyền tay cho validator thủ công của `assignMeeting()`).

## 10. Rà lại TỪNG rule của 2 nhóm field — không suy đoán, gọi validator thật để biết rule nào
đã Việt sẵn (lang file) và rule nào còn Anh

| Field | Rule | Câu hiện tại (đo qua validator) | Cần message riêng? |
|---|---|---|---|
| `manager_employee_ids` | `required` | Bắt buộc phải nhập | Không (đã Việt) |
| `manager_employee_ids` | `array` | The manager employee ids must be an array. | **CÓ** |
| `manager_employee_ids` | `min:1` | (không tách được khỏi `required` khi mảng rỗng — `required` chặn trước; lang `min.array` = "Phải có ít nhất :min phần tử." đã Việt) | Không |
| `manager_employee_ids.*` | `integer` | The manager_employee_ids.1 must be an integer. | **CÓ** |
| `manager_employee_ids.*` | `exists:employees,id` | Không tồn tại | Không (đã Việt) |
| `services` | `array` | The services must be an array. | **CÓ** |
| `services` | `max:20` | Không được có nhiều hơn 20 phần tử. (type `array` vì có rule `array` đứng cùng) | Không (đã Việt) |
| `services.*.service_id` | `required` | Bắt buộc phải nhập | Không |
| `services.*.service_id` | `integer` | The services.0.service_id must be an integer. | **CÓ** |
| `services.*.service_id` | `exists (Rule::exists ... where status)` | Không tồn tại | Không (đã Việt) |
| `services.*.quantity` | `required` | Bắt buộc phải nhập | Không |
| `services.*.quantity` | `numeric` | Không hợp lệ (type `numeric` — rule `numeric` bản thân ĐÃ Việt trong lang file) | Không |
| `services.*.quantity` | `gt:0` | The services.0.quantity must be greater than 0. | **CÓ** |
| `services.*.quantity` | `max:999999` | Không được lớn hơn 999999. (type `numeric` vì có rule `numeric`) | Không (đã Việt) |
| `services.*.note` | `max:255` | Vui lòng nhập tối đa 255 ký tự. (type `string`, không có rule numeric/array đứng cùng) | Không (đã Việt) |

**Kết luận: chỉ 5 rule thật sự cần message riêng** — `manager_employee_ids.array`,
`manager_employee_ids.*.integer`, `services.array`, `services.*.service_id.integer`,
`services.*.quantity.gt`. Đúng như coordinator liệt kê, TRỪ `manager_employee_ids` (`min`) và
`services` (`max`) — 2 rule này ĐÃ có câu Việt chuẩn (`min.array`/`max.array`), nên **không khai**
(đúng nguyên tắc "rule nào lang file đã có câu Việt thì không khai lại").

## 11. Cách làm — `attributes()` thay vì viết lại cả câu

Theo đúng đề nghị của coordinator, ưu tiên `attributes()` (mẫu đã có sẵn trong codebase, vd
`Modules/Finance/Http/Requests/ProductTransfer/ProductTransferFormRequest.php`) để câu lỗi có tên
trường tiếng Việt, thay vì viết hẳn câu dài kiểu cũ:

**`MeetingRoomRequest`** — thêm `attributes()` + 2 key vào `messages()`:
```php
public function attributes()
{
    return [
        'manager_employee_ids' => 'Người quản lý',
        'manager_employee_ids.*' => 'Người quản lý',
    ];
}
// trong messages():
'manager_employee_ids.array' => ':attribute không hợp lệ',
'manager_employee_ids.*.integer' => ':attribute không hợp lệ',
```

**`MeetingRoomBookingRequest`** — `services[]` được dùng ở CẢ `store()`/`update()` (qua FormRequest)
LẪN `MeetingRoomBookingController::assignMeeting()` (validator thủ công, không đi qua FormRequest
nên không tự nhận `messages()`/`attributes()` của class). Để không chép câu chữ ra 2 nơi rồi lệch
nhau dần (đúng tinh thần `serviceItemRules()` đã tách sẵn từ lượt C3), thêm 2 static method mới:
```php
public static function serviceItemMessages(): array
{
    return [
        'services.array' => ':attribute không hợp lệ',
        'services.*.service_id.integer' => ':attribute không hợp lệ',
        'services.*.quantity.gt' => 'Phải lớn hơn 0',
    ];
}

public static function serviceItemAttributes(): array
{
    return [
        'services' => 'Danh sách dịch vụ',
        'services.*.service_id' => 'Dịch vụ',
    ];
}
```
`messages()`/`attributes()` của chính `MeetingRoomBookingRequest` giờ `array_merge()` 2 hàm tĩnh này
vào (cho `store()`/`update()`), và `MeetingRoomBookingController::assignMeeting()` truyền thẳng 2
hàm tĩnh này làm tham số 3-4 của `validator()`:
```php
$validator = validator(
    $request->all(),
    $rules,
    MeetingRoomBookingRequest::serviceItemMessages(),
    MeetingRoomBookingRequest::serviceItemAttributes()
);
```

⚠️ Viết HOA `'Người quản lý'`/`'Dịch vụ'` (không phải chữ thường) — vì message dùng `:attribute` làm
**CẢ CÂU đứng riêng** (`":attribute không hợp lệ"` → `"Người quản lý không hợp lệ"`), không phải
chèn giữa câu như kiểu dùng `:attribute` gốc của Laravel (`"The :attribute field is required."`).
Đã tự bắt lỗi này ở vòng đo đầu (ra `"người quản lý không hợp lệ"` chữ thường đầu câu) và sửa lại
trước khi chốt.

`meeting_id.integer`/`meeting_room_id.integer` trong `assignMeeting()` **KHÔNG đụng** — 2 field này
có từ Phase 6 (Task 50), TRƯỚC Phase 8, nên English trap của chúng đúng là nợ cũ, giữ nguyên phân
loại "ngoài phạm vi" của lượt D1.

## 12. Câu lỗi THẬT sau khi bổ sung (gọi validator qua `artisan tinker`, dùng đúng FormRequest thật
— `new MeetingRoomRequest()`/`new MeetingRoomBookingRequest()` rồi gọi `->messages()`/`->attributes()`,
và với `assignMeeting()` thì gọi đúng 2 static method mới y hệt code controller)

```
=== MeetingRoomRequest — manager_employee_ids = 'not-array' ===
  manager_employee_ids: Người quản lý không hợp lệ

=== MeetingRoomRequest — manager_employee_ids = [999999999, 'abc'] ===
  manager_employee_ids.0: Không tồn tại          (id không tồn tại — exists, đã Việt sẵn)
  manager_employee_ids.1: Người quản lý không hợp lệ   (phần tử không phải số — integer, MỚI)

=== MeetingRoomBookingRequest (store) — services = 'not-array' ===
  services: Danh sách dịch vụ không hợp lệ

=== MeetingRoomBookingRequest (store) — services.0 = {service_id:'abc', quantity:0} ===
  services.0.service_id: Dịch vụ không hợp lệ     (không phải số nguyên — integer, MỚI)
  services.0.quantity: Phải lớn hơn 0             (gt:0, MỚI)

=== MeetingRoomBookingRequest (store) — services.0 = {service_id:999999999, quantity:5000000} ===
  services.0.service_id: Không tồn tại            (exists, đã Việt sẵn)
  services.0.quantity: Không được lớn hơn 999999. (max:999999, đã Việt sẵn — type numeric)

=== MeetingRoomBookingRequest (store) — 21 dòng services ===
  services: Không được có nhiều hơn 20 phần tử.   (max:20 trên mảng, đã Việt sẵn — type array)

=== MeetingRoomBookingController::assignMeeting() — services = 'not-array' (dùng static helpers) ===
  meeting_id: Bắt buộc phải nhập
  meeting_room_id: Bắt buộc phải nhập
  services: Danh sách dịch vụ không hợp lệ

=== checkNoDuplicateServiceIds() — 2 dòng cùng service_id=5 (không đổi, vẫn đúng như trước) ===
  services.1.service_id: Món dịch vụ này đã được chọn ở dòng khác, vui lòng gộp số lượng vào 1 dòng
```

**Không còn chữ tiếng Anh nào** trong mọi kịch bản đã kiểm (mảng sai kiểu, phần tử không phải số, id
không tồn tại, số lượng ≤ 0, số lượng vượt trần, quá 20 dòng, trùng món) — đúng yêu cầu coordinator.

## 13. `phpunit --filter MeetingRoom` sau lượt D2

```
Tests: 65, Assertions: 179, Errors: 5, Failures: 2.
```
**Giống hệt** mốc TRƯỚC lượt D1 và SAU lượt D1 — không đỏ thêm. 5 Errors + 2 Failures vẫn đúng 2
nhóm cũ (cột `code` thiếu ở `MeetingRoomBookingRaceTest`, `mode_id`/`meeting_room_id` ở
`MeetingRoomBookingSyncRuleTest`), không liên quan message validate.

## 14. Test/e2e assert theo câu chữ cũ của 2 field này — không có

`grep -rn "manager_employee_ids\|must be an array\|must be an integer" tests/` (hrm-api) và grep
tương tự trong `HRM/e2e/tests/meeting/*.spec.ts` cho các chuỗi liên quan (`manager_employee_ids`,
"Người quản lý không hợp lệ", "Dịch vụ không hợp lệ", "Danh sách dịch vụ không hợp lệ") → **0 kết
quả cả 2 nơi**. Không có gì phải sửa theo.

## 15. File đã sửa thêm ở lượt D2 (nối vào mục 7 — File đã sửa)

- `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php` — thêm `attributes()`, thêm 2
  key vào `messages()`.
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php` — thêm
  `serviceItemMessages()`/`serviceItemAttributes()` (static), thêm `attributes()`, `messages()` nay
  `array_merge()` với `serviceItemMessages()`.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php` — `assignMeeting()`
  truyền thêm tham số 3-4 (`messages`, `attributes`) cho `validator()`, lấy từ 2 static method mới.

Không đổi `rules()` ở file nào (đúng ràng buộc D1 vẫn giữ nguyên cho D2). Không sửa lang file, không
commit/push/stash.

## 16. Tổng kết số liệu (gộp cả D1 + D2)

- Message tự viết đã XOÁ (D1): 46 key.
- Message GIỮ lại từ D1: 19 key.
- Message MỚI THÊM ở D2 (English trap do chính Phase 8 gây ra): **5 key** —
  `manager_employee_ids.array`, `manager_employee_ids.*.integer`, `services.array`,
  `services.*.service_id.integer`, `services.*.quantity.gt` — cộng 2 `attributes()` mới (
  `MeetingRoomRequest`, `MeetingRoomBookingRequest`) và 2 static helper dùng chung với
  `assignMeeting()`.
- Nhóm rule còn tiếng Anh trong lang file mà Meeting đang dùng KHÔNG CÒN field nào của riêng Phase 8
  bị bỏ sót — chỉ còn nợ cũ thật sự (Phase 6 trở về trước): `meeting_id.integer`/
  `meeting_room_id.integer` ở `assignMeeting()`/`unassignMeeting()`, `exclude_booking_id.integer` ở
  `availability()`, `allow_outside_hours.boolean` ở `updateRoomHours()`.
