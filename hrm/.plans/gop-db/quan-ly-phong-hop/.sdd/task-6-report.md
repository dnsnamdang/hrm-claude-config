# Task 6 report — API danh mục phòng họp

## Status: HOÀN THÀNH

## File đã tạo/sửa

BE (worktree `hrm-worktrees/phong-hop-api`):
- Create: `Modules/Meeting/Services/MeetingRoomService.php`
- Create: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php`
- Create: `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php`
- Modify: `Modules/Meeting/Routes/api.php` (thêm group `meeting/rooms`, `/form-options` khai trước wildcard `/{meetingRoom}`, `/upcoming-bookings` sau wildcard 1-segment nhưng không đụng nó vì khác số segment)

E2E:
- Create: `e2e/tests/meeting/meeting-room.api.spec.ts` (5 ca ban đầu; sau fix round 1 thêm ca 6 → 6 ca, xem mục "Fix round 1" cuối file)

## Dòng tổng kết Playwright

**ĐỎ (trước khi viết BE, chỉ route chưa tồn tại → 404):**
```
1 failed
  [api] › tests/meeting/meeting-room.api.spec.ts:60:5 › 1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho
4 did not run
```

**XANH (sau khi viết BE, chạy 2 lần liên tiếp để xác nhận idempotent):**
```
Running 5 tests using 1 worker
  ✓ 1..5
5 passed (8.5s)
```
```
Running 5 tests using 1 worker
  ✓ 1..5
5 passed (11.5s)
```

**Chạy chung với Task 5 (`room-amenity.api.spec.ts`) để kiểm không phá vỡ nhau:**
```
Running 9 tests using 1 worker
  ✓ 1..9
9 passed (12.7s)
```
(Không có nhánh serial nào báo "did not run".)

Đã kiểm DB sau mỗi lần chạy: không còn dòng `code LIKE 'E2E_%'` trong `meeting_rooms` /
`meeting_room_amenities` — afterAll dọn sạch, chạy lại lần 2 vẫn xanh.

## Kiểm N+1 (bước 9 của brief)

Dựng script gọi thẳng `MeetingRoomService::index()` + luồng batch trong Controller (không
qua HTTP) với `DB::enableQueryLog()`, tạo 5 phòng rồi lọc theo keyword, `per_page=50`:
- Query cho `meeting_rooms` (count + select): 2
- Query cho `amenities` (`with('amenities')`, batch qua `whereIn('meeting_room_id', ids)`): **1 query duy nhất** cho cả 5 dòng — không phải 5.
- Query cho `used_booking_count` (`whereIn(...)->groupBy(...)`): **1 query duy nhất** — không gọi `isCanDelete()` trong vòng lặp.

→ Đúng yêu cầu bắt buộc: `with('amenities')` + tính cờ theo lô bằng cách gán
`$room->used_booking_count` vào từng model (KHÔNG dùng biến static trên Resource như Task 5).

Đã dọn 5 phòng test `N1Q_*` tạo ra trong lúc đo N+1.

## Concerns

- Vẫn còn N+1 riêng cho `employee_update_name` / `employee_create_name` (accessor trong
  `App\Models\BaseModel` gọi quan hệ `employee_create`/`employee_update` không eager-load) —
  với 5 dòng phát sinh thêm ~35 query phụ (qua `Employee::info`, `EmployeeInfo`, company...).
  Đây là **pattern có sẵn trong toàn bộ codebase**, Task 5 (`MeetingRoomAmenityResource`) cũng
  bị y hệt (không `with('employeeCreate', 'employeeUpdate')`), và brief/ràng buộc N+1 của Task 6
  chỉ nêu đích danh `amenities` + `isCanDelete()`/`upcomingBookingCount()`. Không tự ý mở rộng
  scope sang sửa `BaseModel` hay đổi accessor dùng chung — nêu ở đây để người review cân nhắc
  có cần 1 task riêng dọn N+1 tên người tạo/sửa cho toàn hệ thống hay không.
- `formOptions()` lấy `company_id` ưu tiên từ `$request->company_id`, fallback
  `auth()->user()->info->company_id`; nếu công ty đó chưa có dòng trong `general_regulations`
  thì rơi về hằng số mặc định hệ thống (`07:00:00`/`20:00:00`/15 phút) qua
  `MeetingRoom::resolveConfig()` — đúng thứ tự phòng → công ty → mặc định hệ thống theo thiết kế entity, dù ở đây không có giá trị "phòng" (form-options dùng cho tạo mới, chưa có phòng).
- Chưa viết `getAll` (dropdown) riêng cho `meeting/rooms` — brief Task 6 không liệt kê
  endpoint này trong "Produces" (khác Task 5 có `/getAll`); nếu FE cần dropdown chọn phòng thì
  cần task/bổ sung riêng.

---

## Fix round 1/5 (review trả 2 Critical + 2 Important)

### CRITICAL 1 — Lộ `checkin_qr_token` cho mọi nhân viên đăng nhập

- `Modules/Meeting/Routes/api.php`: route `GET /{meetingRoom}` (show) trước đây chỉ có
  `auth:api` ở group cha, không có `checkPermission`. Đã gắn
  `->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp')`.
- `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php`: bọc
  `checkin_qr_token` bằng `$this->when(isCurrentEmployeeHasPermission('Quản lý danh mục phòng họp'), $this->checkin_qr_token)`
  (helper toàn cục trong `app/Helper/PermissionHelper.php`) — defense-in-depth, vai trò chỉ có
  quyền "Xem danh mục phòng họp" (vẫn qua được route) sẽ KHÔNG thấy field này trong response.
- Thêm ca e2e mới **6. không quyền thì GET chi tiết phòng cũng trả 403, không lộ checkin_qr_token**
  — token nocost không có cả 2 quyền phòng họp nên nhận 403 ở tầng route (chưa tới Resource);
  đã assert thêm `expect(text).not.toContain('checkin_qr_token')` để chặn cả 2 lớp.

### CRITICAL 2 — Assertion rỗng nghĩa trong spec

- Ca 1 (`meeting-room.api.spec.ts`) trước đây `expect(await dup.text()).toContain('code')`
  luôn pass vì mọi response đều có key top-level `"code": <httpStatus>`. Đã sửa: parse JSON,
  assert đúng khuôn `BaseRequest::failedValidation()` — `body.errors.code` tồn tại, là string
  không rỗng (giống cách Task 5 vừa sửa trong `room-amenity.api.spec.ts`).

### IMPORTANT 3 — N+1 `employee_create_name` / `employee_update_name`

- `MeetingRoomService::index()`: đổi `->with('amenities')` thành
  `->with(['amenities', 'employee_create.info', 'employee_update.info'])` (tên quan hệ đúng
  là **snake_case** `employee_create`/`employee_update`, report round trước ghi nhầm camelCase).
- `MeetingRoomController::show()`: đổi `$meetingRoom->load('amenities')` thành
  `$meetingRoom->load(['amenities', 'employee_create.info', 'employee_update.info'])`.
- Đo lại bằng script gọi thẳng `MeetingRoom::query()` (không qua HTTP) với
  `DB::enableQueryLog()`, 5 phòng test, `per_page=20`:

  | | TRƯỚC fix (chỉ `with('amenities')`) | SAU fix (`with(['amenities','employee_create.info','employee_update.info'])`) |
  |---|---|---|
  | Query count (5 dòng) | **40** | **10** |

  40 → 10: giảm đúng phần N+1 do `employee_create_name`/`employee_update_name` (mỗi dòng trước
  đây tốn ~6 query qua `employee_create`→`info`→company check, `employee_update` tương tự khi
  có; các dòng test chỉ có `created_by` nên chỉ tốn 1 nhánh/dòng — 40 vẫn còn cao vì
  `getEmployeeCreateNameAttribute()`/`getEmployeeUpdateNameAttribute()` không chỉ load quan hệ
  mà còn kích hoạt thêm `master_settings` lookup lồng trong `Company` model boot). Không còn
  N+1 theo nghĩa "1 query/dòng cho quan hệ nhân sự" — phần query còn lại (10 cho 5 dòng) là
  chi phí cố định của `amenities` (1) + `used_booking_count` (1) + các lookup phụ dùng chung
  cho toàn bộ trang (không tăng tuyến tính theo số dòng nữa).

### IMPORTANT 4 — Mã dữ liệu test cố định

- Mọi mã test (`E2E_A301`, `E2E_QR01`, `E2E_RM_AM1`, `E2E_RM_AM2`, `E2E_AM_ROOM`, `E2E_NOPERM`,
  thêm `E2E_NOPGET` cho ca 6 mới) gắn hậu tố `Date.now()` — không còn literal cố định.
- Thêm `cleanupLeftoverE2eData()` chạy trong `beforeAll`: quét `GET /meeting/rooms?keyword=E2E_`
  và `GET /meeting/room-amenities?keyword=E2E_`, xóa hết bản ghi còn sót (phòng trước, tiện
  nghi sau — đúng thứ tự FK) trước khi test chạy — cùng khuôn Task 5 vừa áp dụng.

### Chạy lại sau khi sửa

**Lần 1 (`meeting-room.api.spec.ts`, `--project=api --no-deps --workers=1`):**
```
Running 6 tests using 1 worker
  ✓ 1..6
6 passed (12.1s)
```

**Lần 2 (chạy lại xác nhận idempotent):**
```
Running 6 tests using 1 worker
  ✓ 1..6
6 passed (11.7s)
```

**Chạy chung cả thư mục `tests/meeting` (Task 6 + Task 5):**
```
Running 10 tests using 1 worker
  ✓ 1..10
10 passed (11.9s)
```
(Không có nhánh serial nào báo "did not run".)

Đã kiểm DB sau khi chạy: `SELECT COUNT(*) FROM meeting_rooms WHERE code LIKE 'E2E_%'` = 0,
`SELECT COUNT(*) FROM meeting_room_amenities WHERE code LIKE 'E2E_%'` = 0; dữ liệu tạo ra khi
đo N+1 (`N1Q2_*`) cũng đã xóa thủ công qua API sau khi đo xong.

### Không sửa (đã ghi nhận, để lại theo yêu cầu coordinator)

- `destroy()` không `lockForUpdate`.
- `unlock()` không kiểm điều kiện đối xứng với `lock()`.
