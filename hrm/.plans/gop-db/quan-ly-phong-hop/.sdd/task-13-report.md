# Task 13 — Báo cáo: API tạo/sửa phiếu đặt phòng + chống trùng lịch

**Status: HOÀN THÀNH** (đã qua Fix round 2/5)

---

# Fix round 1/5 — VIỆC 1, 2, 3

## VIỆC 1 — Mutex trên dòng phòng (không chỉ dựa gap lock)

`MeetingRoomBookingService::assertNoOverlap()` nay khóa dòng phòng TRƯỚC khi kiểm trùng:

```php
// Mutex theo phòng — PHẢI đứng TRƯỚC query kiểm trùng bên dưới.
MeetingRoom::where('id', $roomId)->lockForUpdate()->first();
```

Đặt ngay đầu `assertNoOverlap()`, trước cả `SELECT ... FOR UPDATE` trên tập overlap (giữ nguyên làm
lớp thứ 2, đọc dữ liệu mới nhất sau khi mutex nhả ra). Docblock đã cập nhật giải thích rõ lý do:
gap lock chỉ đáng tin dưới `REPEATABLE-READ`; khóa 1 dòng LUÔN TỒN TẠI (phòng) thì đúng bất kể
isolation level. File: `Modules/Meeting/Services/MeetingRoomBookingService.php` (không đụng file
entity của Task 11).

## VIỆC 2 — Ca đua thật ở tầng DB (không qua HTTP)

### 2a. Ca C1 (HTTP) — đổi tên + comment cho trung thực

Đã xác nhận `php -S` (`artisan serve`) xử lý tuần tự — ca `Promise.all()` cũ đặt tên "ca nghiệm thu"
là sai. Đã sửa trong `e2e/tests/meeting/meeting-room-booking.api.spec.ts`:
- Đổi tên nhóm: `Nhóm C — 2 lần đặt trùng giờ liên tiếp` (không còn gọi "CA NGHIỆM THU: race condition").
- Test case C1 đổi tên + thêm comment nêu rõ: ca này KHÔNG loại trừ được thiếu `lockForUpdate`, chỉ
  kiểm hành vi "gửi 2 request gần nhau qua HTTP thì lần sau bị 422" — do web server tuần tự.
- Ca thật nằm ở script riêng dưới đây.

### 2b. Script PDO 2 kết nối riêng — `.sdd/task-13-race-check.php`

Không đưa vào repo code. Mô phỏng đúng 2 câu SQL của `assertNoOverlap()` bằng 2 tiến trình PHP con
(`proc_open`), mỗi tiến trình 1 kết nối PDO riêng — loại trừ hoàn toàn ảnh hưởng của `php -S` tuần
tự vì đây là 2 process hệ điều hành độc lập, không đi qua HTTP/web server.

**Bẫy khi viết script (đã tự bắt và sửa)**: bản nháp đầu tiên đặt độ trễ nhân tạo SAU khi insert
(trước commit) — kết quả là A luôn insert gần như ngay lập tức, nên B khi quét index luôn CHẠM
PHẢI một dòng đã tồn tại (dù A chưa commit) và bị chặn bởi khóa dòng thông thường của InnoDB —
đúng bất kể isolation level, KHÔNG chứng minh được gì về gap lock/gap-lock-thiếu. Phải chuyển độ
trễ ra NGAY SAU bước "kiểm tra xong, thấy trống" và TRƯỚC bước insert — đúng khe hở TOCTOU thật mà
brief mô tả ("SELECT rồi INSERT không khóa").

**3 kịch bản, chạy 3 lần (mỗi lần tạo phòng riêng, tự dọn sau khi xong):**

```
$ php task-13-race-check.php no-mutex-rc      # ĐỐI CHỨNG ÂM — bỏ mutex, ép READ COMMITTED
MySQL transaction_isolation hiện tại (session của orchestrator): REPEATABLE-READ
=== Scenario: no-mutex-rc | room_id=344 | start=2026-10-18 09:00:00 end=2026-10-18 10:00:00 ===
[A] INSERTED booking_id=84 code=RACE-A-54f9ed4a lock_wait=0.000s total=0.713s
[B] INSERTED booking_id=85 code=RACE-B-9576e36e lock_wait=0.000s total=0.726s
=== KẾT QUẢ: số phiếu trong DB cho room_id=344 = 2 ===   <-- LỌT CẢ HAI (double-booking)
=== Đã dọn sạch room_id=344 và các phiếu liên quan ===
```
Chạy lại lần 2 để chắc không phải may rủi — vẫn lọt cả hai:
```
$ php task-13-race-check.php no-mutex-rc
=== Scenario: no-mutex-rc | room_id=347 | ... ===
[A] INSERTED booking_id=88 ... lock_wait=0.000s total=0.723s
[B] INSERTED booking_id=89 ... lock_wait=0.000s total=0.710s
=== KẾT QUẢ: số phiếu trong DB cho room_id=347 = 2 ===
```

```
$ php task-13-race-check.php with-mutex-rc    # ĐỐI CHỨNG DƯƠNG — có mutex, vẫn READ COMMITTED
MySQL transaction_isolation hiện tại (session của orchestrator): REPEATABLE-READ
=== Scenario: with-mutex-rc | room_id=345 | ... ===
[A] INSERTED booking_id=86 code=RACE-A-12201aa3 lock_wait=0.002s total=0.715s
[B] BLOCKED_BY_OVERLAP conflict_booking_id=86 lock_wait=0.508s total=0.517s
=== KẾT QUẢ: số phiếu trong DB cho room_id=345 = 1 ===   <-- CHỈ 1 PHIẾU
```
`lock_wait=0.508s` của B chứng minh B THẬT SỰ bị chặn ở mutex (đợi gần đúng 0.7s TOCTOU delay của
A) chứ không phải trùng hợp — đây chính xác là kịch bản coordinator lo ngại ("nếu production chạy
READ-COMMITTED"), và mutex fix nó đúng.

```
$ php task-13-race-check.php with-mutex-rr    # đối chứng dưới ĐÚNG isolation THẬT của môi trường
MySQL transaction_isolation hiện tại (session của orchestrator): REPEATABLE-READ
=== Scenario: with-mutex-rr | room_id=346 | ... ===
[A] INSERTED booking_id=87 code=RACE-A-583bf602 lock_wait=0.005s total=0.821s
[B] BLOCKED_BY_OVERLAP conflict_booking_id=87 lock_wait=0.672s total=0.680s
=== KẾT QUẢ: số phiếu trong DB cho room_id=346 = 1 ===
```

**Kết luận**: có mutex → đúng bất kể isolation level (đo cả `READ COMMITTED` lẫn `REPEATABLE-READ`
thật của môi trường); không có mutex + `READ COMMITTED` → lọt double-booking, tái hiện được 2/2
lần chạy. Dữ liệu script tạo ra đã dọn sạch (`DELETE` cuối mỗi lần chạy) — xác nhận lại bằng
`SELECT COUNT(*)` sau khi chạy cả 3 kịch bản: `meeting_room_bookings` = 0 dòng `RACE-%`,
`meeting_rooms` = 0 dòng `RACECHK_%`.

## VIỆC 3 — Thống nhất khuôn lỗi 422

Controller `MeetingRoomBookingController::store()/update()` không còn `throw $e;` cho
`ValidationException` — thêm private helper `responseValidationError()` tự dựng response ĐÚNG
khuôn `{code, errors}` của `BaseRequest::failedValidation()` (`errors.<field>` là 1 CHUỖI, lấy
message đầu tiên — không phải mảng như khuôn mặc định của Laravel):

```php
private function responseValidationError(ValidationException $e)
{
    $message = [];
    foreach ($e->errors() as $field => $items) {
        $message[$field] = $items[0];
    }
    return response()->json(['code' => 422, 'errors' => $message], 422);
}
```

Đã cập nhật ca B1 trong spec để assert đúng khuôn mới: `secondBody.code === 422`,
`typeof secondBody.errors.start_at === 'string'` (không phải mảng), và message chứa tên cuộc họp
giữ chỗ. Các ca A2/A3/A6 khác vẫn dùng `toHaveProperty` nên không cần sửa (không phụ thuộc hình
dạng chuỗi/mảng).

## Kết quả chạy lại sau fix round 1

```
Running 33 tests using 1 worker
✓ 1..33 (tất cả PASS)
33 passed (1.0m)
```
(19 ca `meeting-room-booking.api.spec.ts` + 8 ca `meeting-room.api.spec.ts` + 6 ca
`room-amenity.api.spec.ts` — không ca nào "did not run".)

DB sạch sau khi chạy: `SELECT COUNT(*) FROM meeting_room_bookings` = 0, không còn phòng
`E2E_%`/`RACECHK_%` nào sót lại.

## Concern mới phát sinh sau fix round 1

- Script `.sdd/task-13-race-check.php` chỉ chạy TAY để lấy bằng chứng, không phải một phần của bộ
  test tự động — nếu môi trường DB/schema đổi (vd thêm cột NOT NULL mới vào
  `meeting_room_bookings`), câu `INSERT` cứng trong script có thể lỗi và cần cập nhật lại thủ công.
  Không ảnh hưởng gì tới code thật (`Modules/Meeting/...`), chỉ là công cụ chẩn đoán.
- Khuôn lỗi `{code, errors}` giờ áp dụng nhất quán cho MỌI lỗi 422 của module phiếu đặt phòng
  (cả lỗi cấu trúc từ `MeetingRoomBookingRequest` lẫn lỗi nghiệp vụ từ Service) — nhưng
  `MeetingRoomController` (danh mục Phòng họp, Task 6) VẪN rethrow thẳng `ValidationException` như
  cũ (khuôn `{message, errors}` mặc định của Laravel). Đây là 2 khuôn khác nhau tồn tại song song
  giữa 2 controller trong CÙNG module — nếu Task 17 (FE) muốn 1 helper dùng chung cho toàn bộ
  phân hệ Meeting, cần thêm 1 fix round riêng cho `MeetingRoomController`/`MeetingRoomAmenityController`
  (ngoài phạm vi Task 13, chưa tự ý sửa).

## File tạo mới

- `Modules/Meeting/Services/MeetingRoomBookingService.php` — toàn bộ logic nghiệp vụ (validate 5.1,
  chống trùng có khóa 5.2, sinh mã an toàn, sửa phiếu 5.4).
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php` — `index/show/store/update`.
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php` — validate cấu trúc.
- `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` — list, gọn.
- `Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php` — chi tiết
  (participants, warnings, người duyệt/hủy...).
- `e2e/tests/meeting/meeting-room-booking.api.spec.ts` — 19 ca e2e (Nhóm A-E).

## File sửa

- `Modules/Meeting/Routes/api.php` — thêm route group `meeting/room-bookings` (index/store/show/update).
  `store` KHÔNG gắn `checkPermission` (quyết định #8).

**KHÔNG đụng** `Modules/Meeting/Entities/MeetingRoomBooking.php` /
`MeetingRoomBookingParticipant.php` — chỉ gọi method/relation có sẵn (`overlaps`, `statusText`,
`statusColor`, `isCanEdit/Cancel/Approve/Reject`, `room()`, `participants()`, `employee()`).
`git status` xác nhận 2 file đó vẫn `??` (untracked, do Task 11 tạo) — tôi không sửa gì trong đó.

## TDD — bằng chứng ĐỎ trước, XANH sau

**Cách lấy RED thật** (không phải suy diễn): comment tạm route group Task 13 trong
`Routes/api.php`, chạy spec, xác nhận 404, rồi bật lại route và chạy XANH.

### Lần 1 — ĐỎ (route bị comment)
```
1) [api] › meeting-room-booking.api.spec.ts:194:5 › A1. tạo phiếu hợp lệ trên phòng KHÔNG cần duyệt...
   Expected: 200
   Received: 404
1 failed
18 did not run
```
(mode `serial` — 1 ca fail làm 18 ca sau in "did not run", đúng cảnh báo CLAUDE.md.)

### Lần 2 — XANH (route bật lại, đã cài đủ BE)
```
Running 19 tests using 1 worker
✓ 1..19 (tất cả PASS)
19 passed (36.3s)
```

### Lần 3 — chạy lại CẢ THƯ MỤC `tests/meeting --project=api` (không phá Phase 1)
```
Running 33 tests using 1 worker
✓ 1..33 (tất cả PASS)
33 passed (1.2m)
```
33 = 19 ca mới (Task 13) + 14 ca cũ (8 `meeting-room.api.spec.ts` + 6 `room-amenity.api.spec.ts`,
đúng "hiện 14 ca" ghi trong brief). Không có ca nào "did not run".

## Ca nghiệm thu — 2 request song song (Nhóm C, ca C1)

```ts
const [a, b] = await Promise.all([api.post(BOOKINGS_URL, {data: payload}), api.post(BOOKINGS_URL, {data: payload})]);
```
Kết quả thật đo được: `[a.status(), b.status()].sort() === [200, 422]`, không request nào 500,
và `SELECT COUNT(*) FROM meeting_room_bookings WHERE meeting_room_id=<id>` (query SQL trực tiếp,
không suy luận qua status code) = **1**. Cơ chế: `assertNoOverlap()` chạy `lockForUpdate()` trên
đúng phạm vi `(meeting_room_id, start_at, end_at)` — index bắt buộc của spec 4.4 — nên InnoDB giữ
gap lock trên khoảng đang quét dù kết quả rỗng; request thứ 2 phải CHỜ request thứ 1
commit/rollback rồi mới đọc lại (current read, không phải snapshot cũ) và thấy phiếu vừa được
duyệt để tự chặn.

## Bẫy 2 — sinh mã an toàn

`createWithUniqueCode()` sinh mã trong CÙNG transaction, bắt `QueryException` (kiểm `errorInfo[1]
== 1062` hoặc message chứa `1062` khi driver không expose `errorInfo`), retry tối đa 3 lần
(`maxId + 1 + $attempt` để chắc chắn khác mã ở mỗi lần thử). Ca C1 xác nhận không request nào ra
500. Với payload trùng giờ như C1, do bị chặn sớm bởi `assertNoOverlap()` (khóa hàng), request
thua không bao giờ chạm tới bước sinh mã — cơ chế retry-1062 là lớp phòng thủ bổ sung cho các race
khác (2 phòng khác nhau/giờ không giao nhau cùng sinh mã lúc gần nhau), không được ca C1 exercise
trực tiếp; đã note rõ trong docblock của Service.

## Khóa bản ghi khi đã tới giờ — 423

`update()` kiểm ngay đầu hàm (trong transaction có `lockForUpdate` trên chính dòng đang sửa):
`Carbon::now()->gte(start_at)` → `throw new Exception(..., 423)`; controller map qua
`in_array($e->getCode(), [403,422,423])`. Ca D5 tái hiện bằng cách chỉnh thẳng `start_at` trong DB
về quá khứ (không phụ thuộc `sleep`/timing) rồi gọi update → đo được **423** (không phải 422).

## Quyết định thiết kế (không có trong brief, tự quyết định hợp lý — ghi lại để review)

1. **Company áp dụng cấu hình giờ/hạn đặt trước**: dùng công ty CỦA PHÒNG (`room->company_id`),
   không phải công ty người đặt — nhất quán với cách `MeetingRoomService::formOptions()` đã làm.
2. **Cờ `is_can_approve/is_can_reject/is_can_cancel`**: KHÔNG chỉ gọi `isCanApprove()`/`isCanReject()`
   thô (chỉ dựa trạng thái) — có kèm kiểm actor (`room->manager_employee_id == auth()->id()` HOẶC
   quyền `Duyệt phiếu đặt phòng họp`) để cờ fail-closed đúng tinh thần CLAUDE.md, dù Task 14 mới
   cài đặt CHÍNH endpoint approve/reject. Nếu Task 14 có luật actor khác (vd cho phép thêm vai trò),
   cần rà lại 2 Resource này.
3. **`is_can_checkin`/`is_can_checkout`**: KHÔNG thêm field này — check-in là Phase 5, chưa có cấu
   hình/entity method nào để tính đúng; thêm placeholder `false` dễ gây hiểu lầm là đã cài.
4. **`warnings`** (cảnh báo vượt sức chứa): trả trong response của CHÍNH request tạo/sửa (thuộc
   tính động, không lưu DB) — GET lại sau đó không còn field này, đúng bản chất "cảnh báo tức thời
   của thao tác vừa làm", không phải trạng thái thường trực của bản ghi.
5. **Participant sync**: có nhận `participant_ids` (mảng, optional) ở cả store/update — dùng lại
   `participants()`/`employee()` relation có sẵn của entity, không đụng file entity. Đây là suy luận
   hợp lý từ spec 6.4 nhưng KHÔNG có trong scope liệt kê tường minh của task-13-brief — nếu Task 15
   (thông báo) hoặc FE có yêu cầu khác về format, cần khớp lại.

## Concerns / việc cần theo dõi

- Route `index`/`show` hiện CHƯA gắn quyền 1579 (Xem tất cả phiếu đặt phòng họp) — theo đúng phạm
  vi brief ("Task 14 mới lo duyệt + luật nhìn thấy"), nhưng nghĩa là MỌI nhân viên đăng nhập hiện
  thấy được TOÀN BỘ phiếu qua `GET /meeting/room-bookings`. Task 14 bước 6 (plan.md) phải lọc lại
  theo luật nhìn thấy trước khi FE (Task 16) dùng endpoint này thật.
- Format lỗi 422 từ Service (`ValidationException::withMessages()`, rethrow ở Controller) đi qua
  handler MẶC ĐỊNH của Laravel: `{"message": "...", "errors": {"field": ["msg"]}}` — KHÁC format
  `{"code":422,"errors":{"field":"msg"}}` của `BaseRequest::failedValidation()` (dùng cho lỗi cấu
  trúc payload). Đây là hành vi ĐÃ CÓ SẴN trong `MeetingRoomController::updateOrCreate()` (cùng
  khuôn catch-rethrow), không phải tôi tự chế — nhưng FE cần biết để map đúng 2 hình dạng lỗi 422
  khác nhau tùy nguồn.
- 2 file entity (`MeetingRoomBooking.php`, `MeetingRoomBookingParticipant.php`) do Task 11 sửa song
  song — chưa merge/commit ở thời điểm tôi chạy test (thấy trong `git status` là untracked). Bộ
  test Task 13 đã chạy PASS trên đúng bản các file đó đang có trong worktree tại thời điểm này; nếu
  Task 11 đổi tiếp method signature, cần chạy lại `tests/meeting` để chắc.

---

# Fix round 2/5 — VIỆC 1, 2, 3, 4, 5

## VIỆC 1 (ưu tiên cao nhất) — Bug mất dữ liệu khi sửa phiếu

Xác nhận đúng như review chỉ ra: `update()` tính `$attendeeCount = $request->attendee_count ??
$booking->attendee_count;` để VALIDATE, nhưng dòng lưu thật lại đọc thẳng
`$request->attendee_count` (bỏ qua fallback) — PUT không kèm `attendee_count`/`host_employee_id`
(2 field `nullable`) làm giá trị đang có bị ghi đè thành `null` ÂM THẦM.

**Sửa** trong `MeetingRoomBookingService::update()`:
```php
// Dùng $request->has() (KHÔNG phải filled()) — key có mặt dù giá trị null vẫn tính là "có gửi",
// vì đây là 2 field NULLABLE hợp lệ (user có quyền xoá giá trị đã chọn).
$attendeeCount = $request->has('attendee_count') ? $request->attendee_count : $booking->attendee_count;
$hostEmployeeId = $request->has('host_employee_id') ? $request->host_employee_id : $booking->host_employee_id;

$warnings = $this->validateBookingRules($room, $startAt, $endAt, $attendeeCount, $bookerCompanyId);
...
$booking->host_employee_id = $hostEmployeeId;   // KHÔNG còn đọc thẳng $request->host_employee_id
$booking->attendee_count = $attendeeCount;      // KHÔNG còn đọc thẳng $request->attendee_count
```
Dùng ĐÚNG 2 biến này cho CẢ validate lẫn lưu — không tính lại ở chỗ khác.

**Ca e2e mới `D6`** (`e2e/tests/meeting/meeting-room-booking.api.spec.ts`): tạo phiếu
`attendee_count=10, host_employee_id=25` → PUT chỉ đổi `title` (payload KHÔNG có 2 key này) → GET
lại xác nhận cả 2 giá trị vẫn nguyên `10`/`25`.

**Đã tự kiểm ca này THẬT SỰ bắt được bug** — revert tạm dòng lưu về đọc thẳng
`$request->attendee_count`/`$request->host_employee_id`, chạy lại D6:
```
1) D6. PUT không kèm attendee_count/host_employee_id -> KHÔNG bị ghi đè thành null (fix round 2, VIỆC 1)
   Error: attendee_count không được mất khi PUT không gửi field này
   Expected: 10
   Received: null
1 failed
```
Hoàn nguyên fix → D6 xanh lại. Đúng tinh thần TDD: test đỏ trước khi có fix, xanh sau.

## VIỆC 2 — N+1 thật ở `index()` (số query đo được: 89 → 9)

`MeetingRoomBookingResource::toArray()`/`DetailMeetingRoomBookingResource::toArray()` trước đây tự
gọi `isCurrentEmployeeHasPermission('Duyệt phiếu đặt phòng họp')` — helper này (`app/Helper/
PermissionHelper.php`) KHÔNG cache, chạy lại `Employee::firstOrNew()->roles` + 1 query join
`role_has_permissions` MỖI LẦN gọi. Gọi trong `toArray()` của Resource = N+1 thật theo số dòng.

**Sửa**: `MeetingRoomBookingService::attachDisplayNames()` tính `$hasApprovePermission =
isCurrentEmployeeHasPermission(...)` **1 LẦN** cho cả lô, gán vào TỪNG MODEL bằng thuộc tính động
`$booking->has_approve_permission` (khuôn giống `booked_by_name`/`host_employee_name` đã làm sẵn
trong cùng hàm) — **KHÔNG** dùng biến `static` trên Resource (đúng như review nhắc, Task 5 đã bị
bắt lỗi kiểu này: biến static rò giá trị cache sang request/user khác vì Resource là class dùng lại
giữa các request trong cùng process). 2 Resource đọc lại `(bool) ($this->has_approve_permission ??
false)` — fallback `false` (fail-closed) nếu lỡ có call site mới quên gọi `attachDisplayNames()`.

**Đo bằng `DB::enableQueryLog()`**, script tinker tạo 1 phòng + 20 phiếu, giả lập
`Controller::index()` với `Auth::guard('api')->setUser(App\Models\TpEmployee::find(34))`:

```
=== SỐ QUERY (bản TRƯỚC FIX, gọi isCurrentEmployeeHasPermission mỗi dòng) cho 20 dòng: 89 ===
=== SỐ QUERY (bản ĐÃ FIX, đọc cờ đã tính sẵn) cho 20 dòng: 9 ===
```
(Đo "trước" bằng cách revert tạm dòng đọc cờ trong `MeetingRoomBookingResource` về gọi thẳng hàm,
chạy lại script, rồi hoàn nguyên — xác nhận lại lần nữa ra đúng 9.) Giảm từ 89 xuống 9 cho 20 dòng —
đúng như review ước lượng ("~40-60 query lặp"), thực đo còn cao hơn ước lượng (80 query thừa).

## VIỆC 3 — Ca test actor cho `is_can_approve/reject/cancel`

Thêm 2 ca `F1`/`F2` trong `meeting-room-booking.api.spec.ts`. Điểm mấu chốt phải xử lý: **token
admin (employee 34, role Super admin) ĐÃ SẴN quyền 1580** "Duyệt phiếu đặt phòng họp" qua
`role_has_permissions` (role_id=18) — xác nhận bằng DB — nên KHÔNG dùng được làm actor "người
ngoài" (mọi phiếu admin đọc đều thấy `is_can_approve=true` dù không phải quản lý phòng). Dùng ĐÚNG
1 token nocost (employee 25, role "Quản lý báo cơm", KHÔNG có quyền 1580) cho cả 2 vế đối lập bằng
cách đổi DỮ LIỆU PHÒNG (không đổi token):

- **F1**: phòng gán `manager_employee_id=25`, phiếu do admin đặt → đọc bằng token nocost:
  `is_can_cancel=true` (actor=quản lý phòng), `is_can_edit=false` (không phải chủ phiếu).
- **F2**: 2 phòng CẦN duyệt — 1 phòng gán `manager_employee_id=25`, 1 phòng KHÔNG gán. Cùng 1 token
  nocost đọc 2 phiếu Chờ duyệt (1 phiếu/phòng): `is_can_approve/reject=true` ở phòng mình quản lý,
  `=false` ở phòng người ngoài. Có thêm 1 assert qua GET **danh sách** (`index`) để chắc cờ actor
  cũng đúng ở list, không chỉ detail (đúng chỗ VIỆC 2 vừa sửa N+1).

Cả 2 ca đã chạy PASS (xem dòng tổng kết cuối file).

## VIỆC 4 — Bằng chứng khóa DB trong bộ test tự động

Tạo `tests/Feature/MeetingRoomBookingRaceTest.php` — **3 test method**, không phụ thuộc file ngoài
repo (`.sdd/task-13-race-check.php` giữ nguyên bên ngoài làm công cụ chẩn đoán ban đầu, không xoá).

1. `test_co_mutex_thi_hai_ket_noi_song_song_chi_tao_duoc_1_phieu` — ĐỐI CHỨNG DƯƠNG: connection A
   (PDO raw ngay trong tiến trình PHPUnit) + connection B (1 tiến trình `php -r` riêng, `proc_open`)
   cùng chạy mô phỏng đúng 2 câu SQL của `assertNoOverlap()` (mutex + overlap check), ép cả 2 dùng
   `READ COMMITTED` (kịch bản coordinator lo ngại nhất). Kết quả: đúng 1 `INSERTED`, 1 `BLOCKED`,
   DB chỉ có 1 phiếu.
2. `test_khong_co_mutex_thi_lot_2_phieu_doi_chung_am` — ĐỐI CHỨNG ÂM NGAY TRONG TEST NÀY (không
   phải file tách rời có thể bị xoá/quên chạy): bỏ mutex, vẫn `READ COMMITTED` → CẢ HAI cùng
   `INSERTED` → DB có 2 phiếu (double-booking) → chứng minh cơ chế đo được lỗi.
3. `test_assertNoOverlap_that_su_dung_lockForUpdate_tren_dong_phong` — **bịt lỗ hổng tự nhận của 2
   ca trên**: 2 ca đầu mô phỏng SQL BẰNG TAY (đúng như coordinator gợi ý "gọi SQL trần mô phỏng"
   cho ca đối chứng âm), nghĩa là chúng KHÔNG gọi trực tiếp `assertNoOverlap()` thật — nếu ai xoá
   dòng mutex trong method thật mà quên đồng bộ bản mô phỏng, 2 ca đó sẽ KHÔNG bắt được. Ca thứ 3
   gọi TRỰC TIẾP method thật qua `ReflectionMethod` (không cần đua/timing), bắt SQL bằng
   `DB::listen()`, khẳng định có đúng 1 câu `SELECT ... meeting_rooms ... FOR UPDATE`.

**Chạy `vendor/bin/phpunit --filter MeetingRoomBookingRace`:**
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
...                                                                 3 / 3 (100%)
OK (3 tests, 7 assertions)
```
Chạy lặp lại 3 lần liên tiếp — không flaky (`OK` cả 3 lần).

**Đối chứng âm THẬT trên chính bộ PHPUnit** (không phải suy luận) — xóa tạm dòng mutex trong
`MeetingRoomBookingService::assertNoOverlap()`, chạy lại:
```
..F                                                                 3 / 3 (100%)
1) Tests\Feature\MeetingRoomBookingRaceTest::test_assertNoOverlap_that_su_dung_lockForUpdate_tren_dong_phong
assertNoOverlap() PHẢI chạy 1 câu SELECT...FOR UPDATE khoá dòng `meeting_rooms` (mutex, fix round 1
VIỆC 1) — không thấy câu nào trong SQL log: ["select * from `meeting_room_bookings` where
`meeting_room_id` = ? and `status` = ? and `start_at` < ? and `end_at` > ? limit 1 for update"]
Tests: 3, Assertions: 6, Failures: 1.
```
2 ca đầu (mô phỏng SQL riêng) vẫn xanh như đã tự nhận trong giới hạn của chúng; ca thứ 3 đỏ ngay lập
tức — đúng như thiết kế: **ai xóa dòng mutex thật thì test đỏ, không phụ thuộc timing/concurrency**.
Hoàn nguyên dòng mutex → cả 3 xanh lại.

**Lý do KHÔNG dùng 2 connection Laravel "thật" (`artisan tinker` con) cho ca 1/2**: đã đo
`artisan tinker --execute="echo 'ok';"` mất **~1.15s** chỉ để boot framework — đủ lớn để lệch hẳn
cửa sổ đua thủ công 0.7s giữa 2 "connection", khiến ca âm/dương có thể sai kết quả tùy tải máy
(flaky) thay vì phản ánh đúng cơ chế khóa. Raw PDO (`php -r`, không boot Laravel) khởi động gần như
tức thời nên giữ được đúng cửa sổ TOCTOU dự kiến — đây là lý do dùng 2 kỹ thuật khác nhau cho 2 mục
tiêu khác nhau (ca 1/2 kiểm CƠ CHẾ khóa dưới điều kiện đua thật; ca 3 kiểm CODE THẬT có gọi cơ chế
đó hay không).

## VIỆC 5 — Thời gian ISO-8601 nhất quán

`DetailMeetingRoomBookingResource` trước đây trả `created_at`/`updated_at` bằng
`Helper::formatDateTime()` (`d/m/Y H:i:s`), khác `MeetingRoomBookingResource` (ISO-8601 có offset).
Đã sửa: cả 2 field đổi sang `MeetingRoomBookingResource::isoDateTime()`, giữ thêm
`created_at_text`/`updated_at_text` (vẫn dùng `Helper::formatDateTime()`) cho người đọc — không
field nào bị xoá, chỉ đổi Ý NGHĨA của `created_at`/`updated_at` sang máy-đọc-được và thêm field mới
cho người-đọc-được. `approved_at`/`cancelled_at`/`checkin_at`/`checkout_at` đã ISO-8601 sẵn từ đầu,
không cần sửa.

## Kết quả chạy lại sau fix round 2

**e2e `tests/meeting --project=api --no-deps --workers=1`:**
```
Running 36 tests using 1 worker
✓ 1..36 (tất cả PASS)
36 passed (1.6m)
```
(22 ca `meeting-room-booking.api.spec.ts` — thêm D6, F1, F2 so với round 1 — + 8 ca
`meeting-room.api.spec.ts` + 6 ca `room-amenity.api.spec.ts`.)

**`vendor/bin/phpunit --filter "MeetingRoom"`:**
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
............................                                      28 / 28 (100%)
OK (28 tests, 54 assertions)
```
(Gồm `MeetingRoomBookingOverlapTest`, `MeetingRoomBookingStateTest`, `MeetingRoomConfigTest` của
Task 11 + 3 ca `MeetingRoomBookingRaceTest` mới.)

**DB sạch sau khi chạy cả 2 bộ**: `meeting_room_bookings` = 0 dòng, không còn phòng
`E2E_%`/`PHPUNIT_RACE%` nào sót lại. `git status` xác nhận 2 file entity Task 11 vẫn `??`
(untracked, không bị tôi sửa).

## File thay đổi trong fix round 2

- `Modules/Meeting/Services/MeetingRoomBookingService.php` — VIỆC 1 (fallback đúng biến), VIỆC 2
  (`has_approve_permission` tính 1 lần trong `attachDisplayNames()`).
- `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` — VIỆC 2 (đọc
  cờ đã tính sẵn, không tự gọi `isCurrentEmployeeHasPermission()`).
- `Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php` — VIỆC 2
  (đồng bộ cách đọc cờ) + VIỆC 5 (ISO-8601 cho `created_at`/`updated_at` + thêm `*_text`).
- `e2e/tests/meeting/meeting-room-booking.api.spec.ts` — thêm ca `D6` (VIỆC 1), `F1`/`F2` (VIỆC 3).
- `tests/Feature/MeetingRoomBookingRaceTest.php` — **file mới** (VIỆC 4).

## Concern mới phát sinh sau fix round 2

- `attachDisplayNames()` giờ gánh thêm trách nhiệm tính quyền — tên hàm không còn mô tả đúng 100%
  việc nó làm (không chỉ "gắn tên hiển thị" nữa). Chưa đổi tên vì đây là hàm `public` đã được gọi ở
  nhiều nơi (`index/show/store/update`); đổi tên nằm ngoài phạm vi fix round này, nêu ra để Task 14
  cân nhắc nếu thêm trách nhiệm tương tự (nên tách thành `attachComputedFlags()` riêng lúc đó).
- `MeetingRoomBookingRaceTest` ca 1/2 tạo tiến trình con thật (`proc_open`) — máy CI/production nào
  chặn `proc_open`/`exec` (một số cấu hình PHP tắt hàm này vì lý do bảo mật) sẽ làm 2 ca này lỗi
  ngay ở bước spawn (`$this->fail('Không spawn được tiến trình con...')`), KHÔNG phải false-negative
  về mutex — cần kiểm `disable_functions` trong `php.ini` của môi trường CI trước khi đưa vào pipeline
  bắt buộc pass.
