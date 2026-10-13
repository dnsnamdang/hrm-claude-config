# Báo cáo — Phase 8 / lượt C1 (T131–T137): BE "Yêu cầu dịch vụ" trên phiếu đặt phòng

Repo `hrm-api`, nhánh `gop_db`. PHP gọi bằng `/opt/homebrew/opt/php@7.4/bin/php`. DB dùng để kiểm:
`hrm_erp` (local, đã `config:clear` trước khi chạy artisan/tinker theo đúng lưu ý môi trường).

## Trạng thái: DONE

## 0. Lệch brief — spec doc không tồn tại

Brief trỏ tới `docs/superpowers/specs/gop-db/2026-09-23-yeu-cau-dich-vu-phong-hop-design.md` mục 7
(10 luật nghiệp vụ) làm "nguồn chân lý". File này **KHÔNG tồn tại** ở bất kỳ đâu trong workspace
(`find` toàn `ERP-HRM` không ra kết quả). Đã đọc lại toàn bộ `.plans/gop-db/quan-ly-phong-hop/`
(design.md, plan.md, .sdd/) — không có bản sao khác. Xử lý: dựa hoàn toàn vào phần mô tả luật
nghiệp vụ được TRÍCH DẪN trực tiếp trong chính brief (luật 2 "chỉ nhập lúc tạo", luật 3 "đổi phòng
báo nhóm mới", luật 5 "409 kèm ai xử lý", luật 6 "đóng băng", luật 7 "quá giờ vẫn bấm được", luật 8
"phòng không người phụ trách -> 422", luật 9 "món khoá vẫn giữ ở phiếu cũ") — brief tự trích đủ chi
tiết để implement không cần đọc thêm file spec. Luật 1/4/10 không được brief trích dẫn tường minh,
suy luận hợp lý từ ngữ cảnh (luật 1: NULL khác 1 — đã làm; luật 4/10: không phát sinh case nào cần
thêm ngoài phạm vi 6 task T131-T137).

## T131 — 2 migration + entity + quan hệ

Tạo mới:
- `Database/Migrations/2026_09_23_000003_create_meeting_room_booking_services_table.php` — bảng
  `meeting_room_booking_services` đúng 8 cột brief liệt kê (`booking_id` FK cascade,
  `service_id` nullable, `service_name`, `unit`, `quantity` decimal(12,2), `note`, `sort_order`,
  timestamps), unique `(booking_id, service_id)`. **Không có `created_by`/`updated_by`** — theo
  đúng tiền lệ bảng con snapshot-theo-phiếu `meeting_room_booking_participants` (cũng không có 2
  cột này), và đúng bảng cột brief liệt kê không có chúng.
- `Database/Migrations/2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table.php` —
  4 cột `service_status`/`service_handled_by`/`service_handled_at`/`service_reject_reason` vào
  `meeting_room_bookings`, `service_status` **nullable, không default** (tự nhiên là NULL).
- `Entities/MeetingRoomBookingServiceItem.php` — đúng tên brief yêu cầu (KHÔNG đụng
  `Services/MeetingRoomBookingService.php`), `extends BaseModel`, `$table =
  'meeting_room_booking_services'`.
- `MeetingRoomBooking::serviceItems()` — `hasMany`, `orderBy('sort_order')` tường minh (đúng khuôn
  `orderBy` tường minh của `MeetingRoom::managers()`).
- `MeetingRoomBooking`: thêm 3 const `SERVICE_STATUS_*`, `serviceStatusText()`,
  `serviceStatusColor()` (khuôn y hệt `statusText()`/`statusColor()` sẵn có), thêm 4 cột mới vào
  `$fillable`.

**Migrate sạch — SỐ THẬT**:
```
$ php artisan migrate --path=Modules/Meeting/Database/Migrations
Migrated:  2026_09_23_000003_create_meeting_room_booking_services_table (90.13ms)
Migrated:  2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table (56.67ms)

$ php artisan migrate:rollback --path=Modules/Meeting/Database/Migrations --step=2
Rolled back: 2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table (59.66ms)
Rolled back: 2026_09_23_000003_create_meeting_room_booking_services_table (7.02ms)

$ php artisan migrate --path=Modules/Meeting/Database/Migrations
Migrated:  2026_09_23_000003_create_meeting_room_booking_services_table (49.87ms)
Migrated:  2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table (20.77ms)
```
Cả 2 lượt migrate + rollback + migrate lại đều sạch, không lỗi.

## T131b — SỬA LỆCH TÊN CỘT (bắt buộc, đã làm) + 1 chỗ SÓT thêm

Xác nhận đúng như brief mô tả: lượt B1 dùng cột `meeting_room_service_id` (tên tự đặt khi bảng
thật chưa tồn tại), bảng thật T131 tạo dùng `service_id` (đúng spec).

**2 chỗ đã sửa** (brief chỉ nêu 1, phát hiện thêm 1 chỗ SÓT khác cùng lỗi khi đọc code):
1. `Entities/MeetingRoomService.php::usedCount()` — đổi `where('meeting_room_service_id', ...)` →
   `where('service_id', ...)`. Đây là gate THẬT của `MeetingRoomServiceController::destroy()`
   (gọi `$meetingRoomService->usedCount()` trực tiếp).
2. **Phát hiện thêm** (KHÔNG có trong brief, cùng lỗi âm thầm): `MeetingRoomServiceController::index()`
   (dòng ~55-60) cũng dùng `meeting_room_service_id` để đếm `used_count` hàng loạt cho MÀN DANH
   SÁCH — `MeetingRoomServiceResource::toArray()` dùng số này để tính `is_can_delete` cho TỪNG
   DÒNG. Sai cột ở đây khiến `used_count` luôn = 0 trên màn danh sách → nút Xoá hiện sáng nhầm cho
   món đang được phiếu dùng (dù `destroy()` cuối cùng vẫn chặn đúng, đây vẫn là 1 lỗi hiển thị âm
   thầm khác — đã sửa cùng lúc, cùng nguyên nhân gốc).

**Ca test bắt buộc** (`test_xoa_mon_dang_duoc_phieu_dung_bi_chan`, trong file test bên dưới): tạo 1
dịch vụ tạm → tạo phiếu dùng dịch vụ đó → gọi `MeetingRoomServiceController::destroy()` → assert
HTTP **400** (đúng mã B1 đang dùng, `responseJson($message, 400)`), message chứa **"1 phiếu đặt
phòng"**, và dịch vụ **VẪN CÒN** trong DB sau khi gọi xoá. **XANH.**

## T132 — Validate (`MeetingRoomBookingRequest.php`)

- `services` → `nullable|array|max:20`, **CHỈ áp dụng khi `POST`** (tạo phiếu) — **quyết định tự
  chọn quan trọng**: brief nói "dùng CHUNG cho cả tạo và sửa" nhưng luật 2 (chỉ nhập lúc tạo) +
  luật 9 (phiếu cũ giữ món đã khoá) mâu thuẫn nhau nếu validate `services` cả ở PUT — PUT gửi kèm
  `services[]` cũ (dù Service sẽ lờ đi hoàn toàn theo T134) có thể ăn `422` OAN vì món trong đó đã
  bị khoá SAU khi phiếu tạo xong. Dùng `$this->isMethod('post')` để tách rules.
- `services.*.service_id` → `required|integer` + `Rule::exists('meeting_room_services', 'id')->where('status', MeetingRoomService::STATUS_ACTIVE)`
  (gộp "tồn tại" + "đang Hoạt động" trong 1 rule).
- `services.*.quantity` → `required|numeric|gt:0|max:999999` (cú pháp `gt:0` với giá trị literal đã
  có tiền lệ dùng ở `Modules/Finance/...` cùng Laravel 8, xác nhận hợp lệ).
- `services.*.note` → `nullable|max:255`.
- Chặn TRÙNG `service_id` trong cùng mảng — dùng `withValidator()` + `$validator->after()` để viết
  message NGHIỆP VỤ riêng ("Món dịch vụ này đã được chọn ở dòng khác..."), **KHÔNG** đi qua
  `messages()` (đúng CLAUDE.md: không viết lại message cho rule phổ biến).
- **CHỈ khai `rules()` + `withValidator()`** cho phần `services.*`, không thêm `messages()` nào
  cho `required`/`integer`/`exists`/`numeric`/`gt`/`max` (giữ nguyên các `messages()` CŨ đã có sẵn
  trong file cho `meeting_room_id`/`purpose_id`/... — đó là code cũ trước lượt này, không thuộc
  phạm vi sửa, không động vào).

## T133 — `store()` trong `MeetingRoomBookingService.php`

- Guard SỚM (trước cả `assertNoOverlap()`): phòng không có `managerIds()` mà `services` không rỗng
  → `ValidationException::withMessages(['services' => '...'])` → 422 gắn field `services`.
- `createBookingServiceItems()`: ghi từng dòng, SNAPSHOT `service_name`/`unit` đọc từ
  `MeetingRoomService` NGAY LÚC TẠO (không lưu id rồi join lúc hiển thị), `sort_order` = vị trí
  trong mảng user gửi (0,1,2...). Trả về SỐ DÒNG THẬT ĐÃ TẠO (phòng thủ race hiếm: món bị
  xoá/khoá đúng lúc giữa validate và transaction thì bỏ qua, không throw).
- `service_status`: có ≥ 1 dòng → gán `1` rồi `save()` lại; 0 dòng → không set field nào (giữ
  NULL tự nhiên, không có default ở migration).
- Bắn thông báo `notifyServiceRequested()` (nhóm "Yêu cầu dịch vụ", note "N món") NGAY SAU khi tạo
  đủ dòng, ĐỘC LẬP với thông báo Chờ duyệt/Đã duyệt đã có sẵn.

## T134 — `update()`

- **Không đọc `$request->services` ở bất kỳ đâu trong `update()`** — hàm này chưa từng đọc field
  đó trước lượt C1, và lượt này KHÔNG thêm dòng nào đọc nó → tự động thoả "gửi kèm services[] thì
  dữ liệu dịch vụ không đổi, không lỗi, lặng lẽ bỏ qua" (kết hợp với việc FormRequest cũng không
  validate `services` ở PUT, xem T132).
- Tách riêng biến `$roomChanged` (chỉ đổi PHÒNG) khỏi `$timeOrRoomChanged` (đổi giờ HOẶC phòng) —
  brief luật 3 chỉ áp dụng khi đổi PHÒNG, không phải mọi lần đổi giờ.
- `$roomChanged && $booking->service_status !== null` → `notifyServiceRequestMoved()` gửi nhóm
  "Yêu cầu dịch vụ" cho managers của phòng MỚI (dòng dịch vụ + `service_status` giữ nguyên, hàm
  chỉ gửi thông báo, không đổi dữ liệu).

## T135 — 2 endpoint xử lý

`PUT meeting/room-bookings/{id}/service-prepared`, `PUT .../service-rejected` — đặt SAU cặp
approve/reject/cancel hiện có (không cần đặt trước wildcard vì đây là route CÓ HẬU TỐ, không xung
đột thứ tự với `/{meetingRoomBooking}`). **KHÔNG gắn `checkPermission`** — gate nằm trong
`MeetingRoomBookingService::assertCanHandleServiceRequest()` (helper DÙNG CHUNG cho cả 2 hành
động, tránh chép luật ra 2 nơi lệch nhau — cùng lý do 8 hàm store/update/approve/... đã gộp
chung).

Guard ĐÚNG thứ tự brief yêu cầu:
1. `auth()->id() ∈ $booking->room->managerIds()` — sai → **403**.
2. Phiếu **không** ở trạng thái Hủy/Từ chối — sai → **423**.
3. `service_status === 1` — sai (người thứ hai bấm sau) → **409**, message ghép "ai đã xử lý lúc
   nào" qua `serviceHandledInfo()` (tra tên qua `Modules\Human\Entities\Employee` — đúng bẫy đã ghi
   sẵn trong `catalogDisplay()` của cùng file: `Modules\Timesheet\Entities\Employee::fullname`
   luôn trả `NULL`).

Thành công: `service_handled_by = auth()->id()`, `service_handled_at = now()`, `service_status = 2`
(hoặc `3` + `service_reject_reason = $reason`). **Không thêm điều kiện thời gian** (luật 7 — phiếu
đã qua giờ vẫn bấm được), khác hẳn approve/reject/cancel/update (những hàm đó khóa theo giờ vì còn
đụng LỊCH đặt phòng; xử lý dịch vụ không đụng lịch).

`MeetingRoomBookingServiceRejectRequest`: field `reason` (đúng tên brief, KHÔNG phải
`service_reject_reason`), `required|max:500`, chỉ khai `rules()`.

**Fix bắt buộc phát sinh** (không có trong brief nhưng BẮT BUỘC để 409 ra đúng mã): trong
`MeetingRoomBookingController::handleServiceException()`, mảng `$knownBusinessCodes` gốc chỉ có
`[403, 422, 423]` — THIẾU `409`. Nếu không thêm, mọi lỗi 409 hợp lệ (race condition, đúng thiết kế)
sẽ (a) bị ép `HTTP_BAD_REQUEST` (400) thay vì 409 như brief yêu cầu, VÀ (b) bị `Log::error()` làm
nhiễu log thật. Đã thêm `409` vào mảng.

## T136 — Resource phiếu

Cả `MeetingRoomBookingResource` (list) và `DetailMeetingRoomBookingResource` (detail) đều thêm:
`has_service_request` (`service_status !== null`), `service_status`, `service_status_text`,
`service_status_color` (`#D97706`/`#16A34A`/`#DC2626`), `service_handled_by_name`,
`service_handled_at`, `service_reject_reason`, `is_can_handle_service` (fail-closed: mặc định
`false`, `true` chỉ khi ĐỦ 3 điều kiện guard T135 — công thức Y HỆT giữa 2 Resource, viết lại
tường minh chứ không tái dùng vì 2 class Resource độc lập nhau, không có class cha chung để đặt
hàm helper mà không đụng phạm vi ngoài task).

`DetailMeetingRoomBookingResource` (CHỈ detail) thêm `services[]`: `service_id`, `service_name`,
`unit`, `quantity` (ép `float`), `note` — đọc qua `relationLoaded('serviceItems')` (KHÔNG
`whenLoaded()`/truy cập trực tiếp) để field này **LUÔN xuất hiện** trong response (mảng rỗng nếu
lỡ có call site nào quên eager load), tránh FE phải đoán "thiếu do quên load hay do phiếu thật
không có món".

**Eager load `serviceItems` + `room.managers`**: đã thêm `serviceItems` vào TẤT CẢ 8 vị trí
`with()`/`load()` của `MeetingRoomBookingService.php` (`index()` + 7 chỗ `load([...])` ở
`loadDetail()`, `assignMeeting()`, `store()`, `update()`, `approve()`, `reject()`, `cancel()`) —
`room.managers` đã có sẵn từ lượt A2 (fix vòng 2), không cần thêm.

**Ghi chú thiết kế quan trọng về N+1**: field `services[]` dùng `relationLoaded()` (KHÔNG lazy-load
khi thiếu) nên KHÔNG THỂ gây N+1 dù có/không eager load — đây là lựa chọn CỐ Ý an toàn hơn brief
yêu cầu tối thiểu ("cấm N+1"), không phải thiếu sót. Vẫn thêm eager load đúng theo văn bản brief để
`services[]` thực sự CÓ dữ liệu ở mọi endpoint trả `DetailMeetingRoomBookingResource`.

## T137 — Thông báo `[DPH]`

4 hàm mới trong `MeetingRoomBookingService.php`, tái dùng `buildNotificationContent()`/
`sendBookingNotification()` sẵn có — không viết cơ chế mới:

| Hàm | Khi gọi | Người nhận | Nhóm hành động |
|---|---|---|---|
| `notifyServiceRequested()` | `store()` có ≥1 món; `update()` đổi phòng (luật 3) | nhóm phụ trách (phòng mới nếu đổi phòng) | "Yêu cầu dịch vụ" |
| `notifyServiceRequestVoided()` | `reject()`, `cancel()`, auto-reject trong `approve()` — CHỈ khi `service_status === 1` | nhóm phụ trách | "Hủy yêu cầu dịch vụ" |
| `notifyServicePrepared()` | `servicePrepared()` | người đặt phiếu | "Đã chuẩn bị dịch vụ" |
| `notifyServiceRejected()` | `serviceRejected()` | người đặt phiếu | "Từ chối dịch vụ" |

**⚠️ Điểm nghi ngờ CẦN CHỐT LẠI**: 4 nhóm hành động trên (`Yêu cầu dịch vụ`, `Hủy yêu cầu dịch vụ`,
`Đã chuẩn bị dịch vụ`, `Từ chối dịch vụ`) **NẰM NGOÀI danh sách 14 giá trị đóng** của
`.claude/skills/notification-convention/SKILL.md` mục 2 ("KHÔNG tự chế nhóm hành động mới"). Đã
dùng ĐÚNG NGUYÊN VĂN brief thay vì map về nhóm gần giống, vì:
1. Brief chỉ định RÕ RÀNG 4 tên này, không để ngỏ.
2. **Tiền lệ CÓ SẴN CÙNG FILE**: `notifyCheckinReminder()`/`notifyCheckoutReminder()` (Task 68,
   đã tồn tại từ trước lượt này) dùng nhóm `Nhắc nhận phòng`/`Nhắc trả phòng` — CŨNG nằm ngoài 14
   giá trị đó, không hề bị coi là lỗi ở bất kỳ báo cáo nào trước đây.

Đã ghi rõ comment tại chỗ trong code (ngay trước 4 hàm notify mới). **Đề nghị coordinator xác nhận
lại với người giữ skill** xem có cần bổ sung chính thức 6 giá trị này (4 của lượt này + 2 của Task
68) vào danh sách 14 giá trị, hay đổi tên cho khớp danh sách — đây là quyết định về QUY ƯỚC DÙNG
CHUNG toàn hệ thống, ngoài thẩm quyền 1 lượt BE đơn lẻ.

## Cách tự kiểm — SỐ THẬT

### #2 — Test `tests/Feature/MeetingRoomBookingServiceRequestTest.php` (9 ca — 7 bắt buộc + T131b + 1 bonus)

Actor tái dùng nguyên bộ đã kiểm bằng tinker của `MeetingRoomManagersTest.php` (24/25 = 2 quản lý,
27 = người đặt, 28 = người ngoài, đều KHÔNG có sẵn quyền "Xem tất cả phiếu đặt phòng họp"/"Duyệt
phiếu đặt phòng họp" — tránh xanh giả).

```
$ vendor/bin/phpunit tests/Feature/MeetingRoomBookingServiceRequestTest.php
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

.........                                                           9 / 9 (100%)

Time: 00:03.095, Memory: 74.50 MB

OK (9 tests, 50 assertions)
```

Danh sách ca:
1. `test_tao_phieu_ba_mon_tao_dung_ba_dong_va_snapshot_dung` — 3 món → 3 dòng, `service_status=1`,
   snapshot giữ tên CŨ dù đổi tên danh mục NGAY SAU khi tạo, `sort_order` đúng thứ tự gửi lên.
2. `test_tao_phieu_khong_mon_thi_service_status_null` — 0 món → `service_status` NULL (không phải
   0/1), 0 dòng bảng con.
3. `test_update_gui_kem_services_du_lieu_dich_vu_khong_doi` — PUT gửi `services[]` khác hẳn (món
   khác, số lượng khác) → dữ liệu dịch vụ đã lưu KHÔNG đổi, không lỗi.
4. `test_nguoi_trong_nhom_phu_trach_bam_da_chuan_bi_thanh_cong` — quản lý bấm Đã chuẩn bị →
   `service_status=2`, `service_handled_by` đúng người.
5. `test_nguoi_thu_hai_bam_sau_tra_409` — quản lý B bấm SAU quản lý A → 409, message chứa "đã
   được", `service_status` giữ nguyên kết quả của A (không bị B ghi đè).
6. `test_nguoi_ngoai_nhom_bam_bi_chan_403` — người ngoài bấm Đã chuẩn bị VÀ Từ chối dịch vụ → cả 2
   đều 403, dữ liệu không đổi (ca phân quyền bắt buộc).
7. `test_phieu_da_huy_khong_xu_ly_dich_vu_duoc_va_giu_nguyen_service_status_1` — Hủy phiếu →
   `service_status` GIỮ NGUYÊN 1 (luật 6); quản lý bấm sau đó → 423, `service_status` vẫn 1.
8. `test_xoa_mon_dang_duoc_phieu_dung_bi_chan` (T131b) — xem mục T131b ở trên.
9. `test_phong_khong_nguoi_phu_trach_gui_services_bi_chan_422` (bonus, luật 8) — phòng 0 quản lý mà
   gửi `services[]` → `ValidationException` field `services`, KHÔNG tạo phiếu nào.

### #3 — `--filter MeetingRoom` toàn bộ module — TRƯỚC/SAU

Mốc TRƯỚC (brief đưa, đã xác nhận khớp lại bằng cách trừ ngược): **53 tests / 105 assertions / 5
Errors / 2 Failures**.

```
$ vendor/bin/phpunit --filter MeetingRoom
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
...
Tests: 62, Assertions: 155, Errors: 5, Failures: 2.
```

**62 = 53 + 9 (test mới), 155 = 105 + 50 (assertion mới), 5 Errors/2 Failures GIỮ NGUYÊN** — đúng
2 nhóm lỗi pre-existing đã brief xác nhận (5 lỗi `Unknown column 'code'` ở
`MeetingRoomBookingRaceTest` — cột `meeting_rooms.code` đã DROP từ Task 44; 2 fail `mode_id` ở
`MeetingRoomBookingSyncRuleTest`) — **KHÔNG đỏ thêm ca nào**.

### #4 — Đo N+1 của `index()` (T136)

Script tạm `n1_measure_c1.php`/`n1_measure_c1_small.php` (đã xoá sau khi đo) — seed 3 phòng, mỗi
phòng 2 quản lý, so sánh 2 quy mô dữ liệu:

| Quy mô | Số phiếu | Số query `index()` + Resource |
|---|---|---|
| Nhỏ | 3 phiếu (1 phiếu/phòng × 3 phòng, mỗi phiếu 2 dòng dịch vụ) | **17** |
| Lớn | 15 phiếu (5 phiếu/phòng × 3 phòng, mỗi phiếu 2 dòng dịch vụ) | **17** |

**Số query KHÔNG đổi khi số dòng tăng 5 lần (3→15 phiếu)** — xác nhận không N+1.

Ghi chú thiết kế (đã nêu ở mục T136): field `services[]` cố tình đọc bằng `relationLoaded()` thay
vì lazy-access, nên về mặt kỹ thuật KHÔNG THỂ N+1 dù có/không eager load `serviceItems` — số đo
trên xác nhận lại tổng thể `index()` (bao gồm `room.managers` đã fix từ lượt A2) vẫn ổn định sau
khi thêm các trường mới, không có N+1 nào MỚI phát sinh từ lượt C1.

### #5 — Dọn dữ liệu, baseline cuối

```
rooms=2  bookings=3  meeting_room_managers=2  meeting_room_services=5
meeting_room_booking_services=0  catalog_histories(meeting_room_services)=0
```
Đúng baseline gốc (2 phòng / 3 phiếu / 2 dòng managers / 5 dịch vụ / 0 dòng bảng con dịch vụ).

## Danh sách file tạo / sửa

**Tạo mới**
- `Modules/Meeting/Database/Migrations/2026_09_23_000003_create_meeting_room_booking_services_table.php`
- `Modules/Meeting/Database/Migrations/2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table.php`
- `Modules/Meeting/Entities/MeetingRoomBookingServiceItem.php`
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingServiceRejectRequest.php`
- `tests/Feature/MeetingRoomBookingServiceRequestTest.php`

**Sửa**
- `Modules/Meeting/Entities/MeetingRoomBooking.php` — 3 const, `serviceItems()`, `serviceStatusText()`/`serviceStatusColor()`, `$fillable`.
- `Modules/Meeting/Entities/MeetingRoomService.php` — **T131b**: `usedCount()` đổi cột.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomServiceController.php` — **T131b**: `index()` đổi cột (chỗ SÓT phát hiện thêm).
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php` — rules `services.*` (chỉ POST) + `withValidator()` chặn trùng.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php` — 2 action mới + fix `handleServiceException()` thêm mã 409.
- `Modules/Meeting/Routes/api.php` — 2 route mới.
- `Modules/Meeting/Services/MeetingRoomBookingService.php` — toàn bộ T133-T137 (store/update/reject/cancel/approve + 2 hàm mới servicePrepared/serviceRejected + helpers + 4 hàm notify + eager load).
- `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` — thêm field T136.
- `Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php` — thêm field T136 + `services[]`.

Không đụng file nào ngoài phạm vi trên (không đụng `hrm-client`, không đụng seeder/permission).

## Bàn giao cho lượt FE

### Resource — tên trường mới (cả list `MeetingRoomBookingResource` và detail `DetailMeetingRoomBookingResource`, trừ khi ghi riêng)

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `has_service_request` | bool | `true` nếu phiếu có yêu cầu dịch vụ (bất kể trạng thái) |
| `service_status` | int\|null | `1` Chờ chuẩn bị · `2` Đã chuẩn bị · `3` Từ chối · `null` không có |
| `service_status_text` | string\|null | Chữ hiển thị, BE đã dịch sẵn |
| `service_status_color` | string\|null | Mã hex, BE quyết màu — `#D97706`/`#16A34A`/`#DC2626` |
| `service_handled_by_name` | string\|null | Tên người đã bấm Đã chuẩn bị/Từ chối |
| `service_handled_at` | ISO datetime\|null | |
| `service_reject_reason` | string\|null | Chỉ có khi `service_status = 3` |
| `is_can_handle_service` | bool | fail-closed — hiện nút Đã chuẩn bị/Từ chối dịch vụ khi `true` |
| `services[]` | array | **CHỈ ở detail resource**. Mỗi phần tử: `service_id`, `service_name`, `unit`, `quantity` (float), `note` |

### Payload `services[]` khi TẠO phiếu (POST `meeting/room-bookings`)

```json
{
  "meeting_room_id": 12,
  "purpose_id": 3,
  "title": "Họp giao ban tuần",
  "start_at": "2026-10-05 09:00:00",
  "end_at": "2026-10-05 10:00:00",
  "services": [
    { "service_id": 1, "quantity": 2, "note": "Pha đặc" },
    { "service_id": 3, "quantity": 1 }
  ]
}
```
`services` optional (`nullable`), tối đa 20 dòng. **PUT sửa phiếu KHÔNG được gửi field này** (bị bỏ
qua hoàn toàn nếu gửi, không lỗi).

### 2 endpoint xử lý

```
PUT meeting/room-bookings/{id}/service-prepared      (không cần body)
PUT meeting/room-bookings/{id}/service-rejected       { "reason": "..." }   (bắt buộc, max 500)
```

### Mã lỗi từng tình huống

| Tình huống | HTTP | Field lỗi (nếu có) |
|---|---|---|
| Tạo phiếu, `services.*.service_id` không tồn tại hoặc đã bị khoá | 422 | `services.<i>.service_id` |
| Tạo phiếu, trùng `service_id` trong mảng | 422 | `services.<i>.service_id` |
| Tạo phiếu, phòng không có người phụ trách mà gửi `services[]` | 422 | `services` |
| `service-prepared`/`service-rejected`, không phải quản lý phòng | 403 | — |
| `service-prepared`/`service-rejected`, phiếu đã Hủy/Từ chối | 423 | — |
| `service-prepared`/`service-rejected`, đã có người xử lý trước (race) | 409 | — (message tự chứa "ai xử lý lúc nào") |
| `service-rejected` thiếu `reason` | 422 | `reason` |

## Điểm nghi ngờ / cần coordinator xác nhận

1. **Nhóm hành động thông báo nằm ngoài whitelist 14 giá trị của skill** — xem chi tiết mục T137.
   Đã dùng nguyên văn brief + tiền lệ có sẵn (Task 68), không tự ý đổi, nhưng đây là quyết định
   ảnh hưởng quy ước TOÀN HỆ THỐNG, không phải chỉ phạm vi lượt này.
2. Spec doc brief trỏ tới không tồn tại (mục 0) — đã tự implement dựa trên phần luật được TRÍCH DẪN
   trực tiếp trong brief, không suy diễn thêm ngoài phạm vi 7 task.
3. `handleServiceException()` phải thêm mã 409 vào whitelist "known business codes" — nếu có lượt
   sau nào khác cũng ném 409 mà controller đó dùng helper tương tự (copy-paste), cần soát lại y hệt.
