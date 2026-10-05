# Task 11 — Báo cáo: Entity phiếu + luật chống trùng (TDD) + vá bẫy 3

**Status: DONE**

## File tạo / sửa (trong worktree `hrm-worktrees/phong-hop-api`)

- Create: `Modules/Meeting/Entities/MeetingRoomBooking.php`
- Create: `Modules/Meeting/Entities/MeetingRoomBookingParticipant.php`
- Create: `tests/Unit/MeetingRoomBookingOverlapTest.php`
- Modify: `Modules/Meeting/Services/MeetingRoomService.php` (bẫy 3 — `destroy()`)

Không đụng file nào khác; không `git commit/push/stash/checkout`.

## Bảng đối chiếu `$fillable` vs `SHOW COLUMNS` thật (DB `hrm_erp`)

**`meeting_room_bookings`** — mọi cột trừ `id`/`timestamps` đều đưa vào `$fillable`, khớp 1-1 với
`SHOW COLUMNS` đo trực tiếp trên DB:
`code, meeting_room_id, title, content, start_at, end_at, status, booked_by_employee_id,
host_employee_id, attendee_count, company_id, department_id, meeting_id, source, approved_by,
approved_at, reject_reason, is_auto_rejected, cancelled_by, cancelled_at, cancel_reason,
checkin_at, checkout_at, auto_released_at, checkout_reminded_at, recurrence_id, created_by, updated_by`

**`meeting_room_booking_participants`** — `SHOW COLUMNS` thật chỉ có
`id, meeting_room_booking_id, employee_id, created_at, updated_at` — **KHÔNG có** `created_by`/
`updated_by` (khác với `meeting_room_bookings`). Do đó `$fillable` của
`MeetingRoomBookingParticipant` chỉ gồm `meeting_room_booking_id, employee_id` — **lệch khỏi yêu cầu
chung "created_by/updated_by trong $fillable"** vì 2 cột đó không tồn tại trên bảng này (đã ghi rõ lý
do bằng comment trong file). `BaseModel::boot()` tự bỏ qua field không tồn tại nhờ bọc
`Schema::hasColumn`, nên không có rủi ro runtime — chỉ là entity này không có gì để mass-assign
thêm ngoài 2 cột trên.

## TDD — bằng chứng ĐỎ trước, XANH sau

**ĐỎ** (trước khi tạo entity, class `MeetingRoomBooking` chưa tồn tại):
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
E                                                                   1 / 1 (100%)
There was 1 error:
1) Tests\Unit\MeetingRoomBookingOverlapTest::test_cham_mep_khong_tinh_la_trung
Error: Class 'Modules\Meeting\Entities\MeetingRoomBooking' not found
ERRORS!
Tests: 1, Assertions: 0, Errors: 1.
```

**XANH** (sau khi viết 2 entity):
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
.                                                                   1 / 1 (100%)
Time: 00:00.760, Memory: 40.50 MB
OK (1 test, 4 assertions)
```
Chạy kèm `MeetingRoomConfigTest.php` (khuôn có sẵn) để chắc không phá gì: `OK (2 tests, 7 assertions)`.

## Interfaces đã có đủ (đúng tên cho Task sau gọi)

- `STATUS_CHO_DUYET=1 · DA_DUYET=2 · TU_CHOI=3 · DA_HUY=4 · HOAN_THANH=5`
- `SOURCE_TU_DAT=1 · SOURCE_TU_MEETING=2`
- `MeetingRoomBooking::overlaps($startA, $endA, $startB, $endB): bool` — dùng `Carbon::lt/gt`,
  công thức `startA < endB && endA > startB` (chạm mép KHÔNG trùng), test phủ đủ 4 ca gồm qua đêm.
- `statusText($status)`, `statusColor($status)` — dùng đúng 5 cặp chữ/màu từ spec 4.8
  (Chờ duyệt `#D97706` · Đã duyệt `#2563EB` · Từ chối `#DC2626` · Đã hủy `#6B7280` · Hoàn thành `#16A34A`).
- `$booking->isCanEdit()` / `isCanCancel()` / `isCanApprove()` / `isCanReject()`:
  - `isCanEdit()`: status ∈ {Chờ duyệt, Đã duyệt} và `now() < start_at` (spec 5.4).
  - `isCanCancel()`: status ∈ {Chờ duyệt, Đã duyệt}, `source != SOURCE_TU_MEETING` (quyết định #12),
    và `now() < start_at` (spec 5.5). Đây chỉ là phần dữ liệu thuần của bản ghi — quyền "ai được bấm"
    (người đặt/quản lý phòng/quyền 1580) cần actor đăng nhập nên để Task 13/14 kiểm ở Service.
  - `isCanApprove()` / `isCanReject()`: status == Chờ duyệt (spec 5.3).
  - Các method này KHÔNG có test bắt buộc theo brief (chỉ `overlaps()` có ca test chỉ định); logic
    bám sát design.md mục 5.3-5.5, không đụng DB.

## Vá bẫy 3 — `MeetingRoomService::destroy()`

Trước đây service `destroy()` chỉ `detach()` + `delete()` trần, kiểm `isCanDelete()` nằm ở
`MeetingRoomController::destroy()` **trước khi** mở `DB::transaction` — đọc không khóa, để hở cửa sổ
giữa lúc kiểm và lúc xóa thật cho 1 request tạo phiếu chen vào.

Đã sửa: đưa việc kiểm (giờ dùng thẳng bảng `meeting_room_bookings` qua entity `MeetingRoomBooking`)
vào **bên trong** `destroy()` — hàm này chạy trong `DB::transaction` mà controller đã mở sẵn quanh lời
gọi `$this->meetingRoomService->destroy($meetingRoom)` — và khóa bằng `->lockForUpdate()` trước khi
quyết định cho xóa:

```php
public function destroy(MeetingRoom $meetingRoom)
{
    $hasBooking = MeetingRoomBooking::where('meeting_room_id', $meetingRoom->id)
        ->lockForUpdate()
        ->exists();

    if ($hasBooking) {
        throw new \Exception('Phòng họp này đã có phiếu đặt nên không xóa được. Bạn có thể Khóa phòng.');
    }

    $meetingRoom->amenities()->detach();
    $meetingRoom->delete();
}
```

Controller vẫn giữ nguyên early-check `isCanDelete()` trước transaction (chỉ là UX fail-fast, không
authoritative) và `catch (Exception $e)` sẵn có sẽ bắt exception mới ném ra, trả 400 với đúng message —
không đổi hành vi HTTP quan sát được từ ngoài.

## Bộ e2e API (`tests/meeting`) sau khi vá — dòng tổng kết

```
Running 14 tests using 1 worker
  ✓ 1..14 (tất cả đều ✓, không có "did not run")
14 passed (40.1s)
```
Lệnh đã chạy đúng như yêu cầu (`BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`,
`--project=api --no-deps --workers=1`). Ca số 14 (xóa phòng → tiện nghi từng gắn phải xóa được) vẫn
xanh, xác nhận luồng xóa phòng hiện có không bị phá bởi `lockForUpdate` mới thêm.

## Concerns

1. `MeetingRoomBookingParticipant` không có `created_by`/`updated_by` trong `$fillable` vì cột không
   tồn tại trên bảng — nêu ở trên để Task sau không thắc mắc tại sao entity này khác khuôn.
2. `isCanEdit()`/`isCanCancel()` dùng `Carbon::now()` (phụ thuộc thời điểm chạy) — chưa có unit test
   riêng (brief chỉ bắt buộc test cho `overlaps()`); Task 13/14 khi viết e2e nên tự thêm ca kiểm cho 2
   method này nếu cần, đặc biệt biên "đã tới giờ bắt đầu" (423 LOCKED, spec 5.4/5.5).
3. Chưa đụng Service/Controller/Request/Resource/route cho `MeetingRoomBooking` — đúng phạm vi Task 11,
   để Task 13 làm.

---

## Fix round 1/5 (review) — 2 Important đã xử

**Files sửa/thêm thêm (vẫn chỉ trong `Modules/Meeting/Entities/` và `tests/Unit/`):**
- Modify: `Modules/Meeting/Entities/MeetingRoomBooking.php` (guard `overlaps()`)
- Modify: `tests/Unit/MeetingRoomBookingOverlapTest.php` (thêm ca test rỗng/null)
- Create: `tests/Unit/MeetingRoomBookingStateTest.php` (test 4 method isCan* với `Carbon::setTestNow()`)

Không đụng `Modules/Meeting/Services/MeetingRoomService.php` hay bất kỳ file Service/Controller/
Request/Resource nào của Task 13 đang chạy song song.

### IMPORTANT 1 — `overlaps()` nuốt input rỗng/null thành "bây giờ"

Đã xác nhận đúng như reviewer đo: `Carbon::parse(null)` và `Carbon::parse('')` không ném lỗi, âm thầm
trả về `now()`. Đã thêm guard đầu hàm `overlaps()`: 4 tham số `startA/endA/startB/endB`, hễ giá trị nào
`=== null || === ''` thì ném `InvalidArgumentException` kèm tên tham số cụ thể trong message (không
đoán "bây giờ" nữa).

Test mới trong `MeetingRoomBookingOverlapTest`: `test_moc_gio_rong_hoac_null_thi_nem_loi_khong_duoc_doan_la_bay_gio`,
dùng `@dataProvider` phủ đủ 8 tổ hợp (4 vị trí tham số × `null`/`''`), mỗi ca gọi
`$this->expectException(InvalidArgumentException::class)` + `expectExceptionMessageMatches()` kiểm
message có nêu đúng tên tham số rỗng.

### IMPORTANT 2 — 4 method isCan* chưa có test

Thêm file mới `tests/Unit/MeetingRoomBookingStateTest.php`, dùng `Carbon::setTestNow()` để bơm thời
gian giả và `tearDown()` gọi `Carbon::setTestNow()` (không tham số) để không rò sang test khác. Phủ:

- `isCanEdit()` / `isCanCancel()`: 1 giây **trước** `start_at` → true; **đúng mốc** `start_at` → false;
  1 giây **sau** → false (kiểm cả 2 biên, đúng chỗ hay lệch 1 nhịp). Thêm ca `isCanEdit()` luôn false
  với status Đã hủy/Từ chối/Hoàn thành dù chưa tới giờ; ca `isCanCancel()` luôn false khi
  `source = SOURCE_TU_MEETING` dù chưa tới giờ (quyết định #12).
- `isCanApprove()` / `isCanReject()`: dùng `@dataProvider` phủ cả 5 trạng thái — chỉ `true` khi
  **Chờ duyệt**, 4 trạng thái còn lại đều `false`.

### Kết quả chạy sau khi sửa

```
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter "MeetingRoomBooking|MeetingRoomConfig"

PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
.........................                                         25 / 25 (100%)
Time: 00:10.995, Memory: 108.50 MB
OK (25 tests, 47 assertions)
```

Breakdown: `MeetingRoomBookingOverlapTest` 1 (luật giao giờ, 4 ca) + 8 (dataProvider rỗng/null) = 9 test;
`MeetingRoomBookingStateTest` 2 (isCanEdit) + 2 (isCanCancel) + 5 (isCanApprove dataProvider) +
5 (isCanReject dataProvider) = 14 test; `MeetingRoomConfigTest` (khuôn có sẵn, không đụng) = 2 test.
9 + 14 + 2 = 25, tất cả xanh — không có test cũ nào bị vỡ bởi guard mới.

### Ghi chú khác

- Nghi vấn `unique('code')` reviewer đã tự xác minh (migration `2026_09_18_000001`) — không đụng, đúng
  chỉ đạo.
- `git status --short` trong worktree lúc này còn thấy
  `M Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — **không phải do task này sửa**
  (không nằm trong scope `Modules/Meeting/Entities/` + `tests/Unit/`), khả năng là Task 12 đang chạy
  song song trong cùng worktree. Không đụng vào, chỉ ghi nhận để tránh hiểu nhầm khi review diff.
