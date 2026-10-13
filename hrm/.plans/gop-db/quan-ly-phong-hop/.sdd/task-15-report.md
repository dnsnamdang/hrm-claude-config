# Task 15 report — 5 loại thông báo nghiệp vụ (phòng họp)

**Status: DONE** — TDD đỏ → xanh đầy đủ. Chạy lại **2 lần liên tiếp** cả thư mục `tests/meeting
--project=api --no-deps --workers=1` ở **foreground**: cả 2 lần **59 passed, không có dòng
`flaky`/`failed`/`did not run`**. DB sạch rác sau khi chạy (kiểm bằng SQL, xem cuối file).

## File sửa / tạo (chỉ trong `Modules/Meeting/` + `e2e/tests/meeting/`)

Sửa:
- `Modules/Meeting/Services/MeetingRoomBookingService.php`
  - Thêm `use Illuminate\Support\Facades\Log;` + `use Modules\Timesheet\Services\EmployeeInfoService;`.
  - Gọi thông báo tại đúng 5 điểm nghiệp vụ: `store()` (Chờ duyệt HOẶC Đã duyệt ngay nếu phòng
    không cần duyệt), `update()` (Thay đổi lịch khi đổi giờ/phòng), `approve()` (Đã duyệt cho
    phiếu thắng + Từ chối cho từng phiếu tự động thua cuộc), `reject()` (Từ chối thủ công),
    `cancel()` (Hủy).
  - Thêm 1 khối helper dùng chung ở cuối class (Task 15):
    - `mapEmployeeIdsToEmployeeInfoIds(array $employeeIds)` — **helper BẪY 1 duy nhất**, map
      `employees.id` → `employees.employee_info_id` bằng
      `Employee::whereIn('id', $ids)->pluck('employee_info_id')->filter()->values()->all()`.
      **Mọi** đường gửi thông báo đều đi qua `sendBookingNotification()` → hàm này.
    - `buildNotificationContent($prefix, $action, $name, $note = '')` — khuôn
      `[{PREFIX}] {Nhóm hành động}: <b>{Tên đối tượng ≤50 ký tự}</b>. {Ghi chú}`, tổng ≤ 120 ký tự
      (cắt ghi chú trước, giữ tên).
    - `roomTimeNote()`, `participantEmployeeIds()` — tiện ích dựng ghi chú/danh sách người dự.
    - `sendBookingNotification()` — bọc `try/catch (\Throwable)` + `Log::error()`, map người nhận
      qua helper bẫy 1, gọi `EmployeeInfoService::sendToAllNotification()`. Lỗi gửi KHÔNG làm hỏng
      transaction nghiệp vụ (không rethrow).
    - `notifyPendingApproval()` / `notifyApproved()` / `notifyRejected()` / `notifyScheduleChanged()`
      / `notifyCancelled()` — đúng 5 loại theo bảng spec mục 7, `type` theo bộ
      `meeting_room_booking_pending|approved|rejected|updated|cancelled`, `url` luôn
      `/meeting/bookings?open_booking=<id>`.
- `e2e/tests/meeting/meeting-room-booking.api.spec.ts`
  - Thêm helper `employeeInfoIdOf()`, `queryNotifications()` (đọc thẳng bảng `notifications`).
  - **Fix quan trọng trong chính helper test** (không phải code nghiệp vụ): thêm tham số `raw` cho
    `runMysql()`, dùng `mysql --raw` khi đọc cột `data` (JSON). mysql CLI ở chế độ batch (stdout
    không phải tty) tự ý escape thêm 1 lớp `\` → `\\`, biến `ờ` (do PHP `json_encode()` sinh
    ra) thành `\\u1edd`, `JSON.parse()` phía Node đọc ra chữ rác thay vì tiếng Việt thật. Bắt được
    lỗi này chính từ ca K1 khi so `title` chứa `[DPH] Chờ duyệt:` — RED thật, không phải false
    positive.
  - Thêm cleanup `notifications` (lọc `type LIKE 'meeting_room_booking_%'`) vào `afterAll` TRƯỚC
    khi xoá booking.
  - Thêm nhóm **K** (7 ca): K1 (bẫy 1, đọc DB), K2 (Đã duyệt thủ công), K2b (Đã duyệt ngay lúc tạo
    ở phòng không cần duyệt — nhánh riêng của spec), K3 (Từ chối thủ công), K4 (Từ chối tự động,
    2 phiếu thua cuộc), K5 (Hủy), K6 (Thay đổi lịch).

## Bảng tên bảng thông báo + cách map (đúng thứ đề bài yêu cầu báo cáo)

- **Tên bảng**: `notifications` (Laravel database notifications chuẩn, migration
  `Modules/Timesheet/Database/Migrations/2022_01_10_080757_create_notifications_table.php`) — cột
  `notifiable_type` + `notifiable_id` (morph, `notifiable_id` = `employee_infos.id`), cột `data`
  (JSON text: `url`, `title`, `type`, `id`).
- **Cách map đã dùng (bẫy 1)**: `Modules\Timesheet\Entities\Employee` (class đã dùng sẵn trong
  `MeetingRoomBookingService`/`MeetingService::notifyMeetingEmployees()`) —
  `Employee::whereIn('id', $employeeIds)->pluck('employee_info_id')->filter()->values()->all()`.
  Đo thật trên DB worktree: employee 34 (admin) ↔ `employee_info_id` **23**; employee 25 (nocost)
  ↔ `employee_info_id` **13** — cả 2 đều KHÁC `employees.id`, khớp mô tả "chỉ 2/1099 nhân viên có
  `id == employee_info_id`". Ca **K1** đọc thẳng bảng `notifications`, khẳng định
  `notifiable_id = 13` (employee_info_id của quản lý phòng nocost), KHÔNG phải `25`.

## Quyết định phạm vi (khác chữ nghĩa literal chỗ nào, và vì sao)

- Task 15 chỉ yêu cầu đúng **5 loại** thông báo (không đụng "Sắp đến hạn"/"Cập nhật khoá phòng" —
  2 dòng còn lại trong bảng spec mục 7 vốn thuộc job nền mục 8, ngoài phạm vi task này).
- `update()` chỉ bắn **"Thay đổi lịch"** khi `timeOrRoomChanged`, **không** bắn thêm "Chờ duyệt"
  dù đôi khi phiếu quay lại trạng thái Chờ duyệt (D2 test cũ) — vì "Chờ duyệt" trong định nghĩa
  hoàn thành chỉ gắn với sự kiện **Tạo phiếu**, không phải mọi lần phiếu chuyển VỀ Chờ duyệt. Ghi
  rõ lý do bằng comment tại đúng chỗ gọi trong `update()`.
- `notifyPendingApproval()` bỏ qua êm (không gửi cho ai) nếu phòng chưa gán `manager_employee_id`
  — không có người nhận hợp lệ thì không có gì để map/gửi, không log lỗi (không phải sự cố).

## Bằng chứng ĐỎ → XANH

**RED (trước khi cài BE)** — chạy cả file `meeting-room-booking.api.spec.ts`:
```
✘ K1 — 0/1 thông báo Chờ duyệt (Expected: 1, Received: 0)
6 did not run  (K2..K6 phía sau K1 trong serial mode)
37 passed
```
(Toàn bộ ca A-J cũ vẫn xanh nguyên — xác nhận baseline chưa bị đụng trước khi sửa BE.)

**Vòng RED thứ 2 (sau khi cài BE, TRƯỚC khi phát hiện lỗi helper test)** — K1 vẫn đỏ, nhưng vì lý
do KHÁC: `notis[0].data.title` chứa `[DPH] Ch\\u1edd duy\\u1ec7t: ...` thay vì tiếng Việt thật —
lỗi ở `runMysql()` (mysql CLI batch mode escape kép `\`), không phải lỗi BE. Sửa `runMysql(sql,
raw=true)` bằng cờ `--raw` cho đúng 1 chỗ gọi (`queryNotifications`) — không đổi hành vi của mọi
ca khác đang dùng `runMysql()` mặc định.

**GREEN (sau khi sửa cả BE lẫn helper test)** — chạy 2 lần liên tiếp, foreground:

Lần 1 (chỉ file booking, 45 ca):
```
Running 45 tests using 1 worker
...
45 passed (1.2m)
```

Lần 2 (cả thư mục `tests/meeting`, 59 ca):
```
Running 59 tests using 1 worker
...
59 passed (1.6m)
```

Lần 3 (lặp lại lần 2 để chắc không flaky):
```
Running 59 tests using 1 worker
...
59 passed (1.6m)
```

Không có `flaky`, không có `failed`, không có `did not run` ở 2 lần chạy cuối cùng (cả thư mục).

## Ghi chú về nhiễu môi trường trong lúc làm (không phải lỗi logic Task 15)

Lần chạy RED đầu tiên (baseline) ghi nhận 1 ca `flaky` ở **H2** (từ chối) — do TÔI vô tình sửa
`store()`/`update()`/`approve()` (thêm lời gọi tới các hàm `notify*` CHƯA ĐƯỢC ĐỊNH NGHĨA) trong
lúc `php artisan serve` đang phục vụ request của chính lần chạy RED đó (vừa launch test nền, vừa
Edit file cùng lúc) — gây Fatal Error thoáng qua cho 1-2 request. Đã tự nhận ra và từ vòng chạy thứ
2 trở đi KHÔNG sửa file trong lúc test đang chạy. Lần chạy sau đó còn ghi nhận 1 flaky khác ở **F2**
(test cũ Task 13, không liên quan gì tới thông báo) — khớp đúng mô tả nhiễu môi trường đã có trong
`task-14-report.md` (nhiều phiên Playwright/PHP dev server chạy song song, xác nhận có tiến trình
Chrome profile `playwright_chromiumdev_profile-*` của phiên khác đang chạy tại thời điểm đó qua
`ps aux`). 2 lần chạy CUỐI CÙNG (sau khi hết nhiễu, không sửa file trong lúc chạy) đều sạch 100%.

## Kiểm DB sạch rác (sau khi chạy xong)

```sql
rooms_leftover              0
bookings_leftover_no_room   0
notifications_leftover      0   -- lọc type LIKE 'meeting_room_booking_%'
```

## Concerns / lưu ý cho người review

1. **Không sửa `Modules\Meeting\Entities\MeetingRoomBooking` /
   `MeetingRoomBookingParticipant`** — đúng ràng buộc của brief (2 file đó do Task 11 khoá).
2. Đã đọc lại `MeetingRoomBookingService.php` ngay trước mỗi lần sửa để phát hiện thay đổi từ
   agent khác (brief cảnh báo có agent song song fix Task 14 round — thứ tự khoá/gom catch). Tại
   thời điểm tôi đọc, nội dung liên quan (`store`/`update`/`approve`/`reject`/`cancel`) khớp đúng
   với lần đọc đầu tiên — không phát hiện thay đổi cần merge tay. Nên kiểm tra lại 1 lượt trước khi
   merge nhánh, phòng trường hợp agent kia commit thêm sau khi tôi đọc lần cuối.
3. `sendBookingNotification()` gọi `EmployeeInfoService::sendToAllNotification()` KHÔNG có
   fallback cho ngữ cảnh không `auth()` (khác với `MeetingService::notifyMeetingEmployees()`) —
   vì mọi route store/update/approve/reject/cancel của module này đều nằm sau middleware
   `auth:api` (xem `Routes/api.php`), nên `auth()->user()` luôn có giá trị khi các hàm `notify*`
   được gọi. Nếu sau này có job nền (CLI) tự động approve/cancel thì phải bổ sung fallback giống
   `MeetingService`.
4. Chưa làm 2 dòng còn lại của bảng spec mục 7 ("Sắp đến hạn", "Cập nhật khoá phòng ngừng sử
   dụng") — cố ý, vì thuộc job nền (mục 8), ngoài phạm vi Task 15.

---

# Fix round 1 — 2 Important + 1 Minor (từ review)

**Status: DONE.** 2 Important đã sửa + có test tự động (1 unit mới, 1 feature mới bắt SQL thật).
Minor (bổ sung mục "Fix round 2" vào `task-14-report.md`) đã làm — xem file đó.

## IMPORTANT 1 — `buildNotificationContent()` xoá sạch ghi chú thay vì cắt ngắn

**Lỗi**: khi tổng nội dung vượt 120 ký tự, code cũ (`if (...<= 120) { $content .= ' ' . $note; }`)
BỎ HẲN ghi chú nếu không đủ chỗ, thay vì cắt ngắn theo đúng skill `notification-convention` mục 1 +
4 ("dài hơn thì cắt", "cắt Ghi chú TRƯỚC"). Với loại **Từ chối**, ghi chú CHÍNH LÀ lý do
(`reject_reason` cho phép tới 500 ký tự) — tiêu đề dài một chút là lý do biến mất hoàn toàn, người
nhận chỉ thấy "bị từ chối" mà không biết vì sao.

**Sửa** (`Modules/Meeting/Services/MeetingRoomBookingService.php`, hàm `buildNotificationContent()`):
tính `$budget = 120 - mb_strlen($plainHead) - 1` (ngân sách còn lại cho ghi chú sau khi trừ phần đầu
cố định — đo trên bản KHÔNG bọc `<b>`, đúng số ký tự người dùng nhìn thấy). Ghi chú vượt ngân sách
thì cắt còn `$budget - 3` ký tự + `...` (nếu `$budget > 3`), hoặc cắt trần không thêm `...` nếu ngân
sách quá nhỏ (≤ 3 ký tự). Tên đối tượng (đã cắt tối đa 50 ký tự ở bước trước) chỉ "mất chỗ cho ghi
chú" khi `$budget <= 0` — đúng thứ tự skill quy định (cắt Ghi chú trước, không đụng lại Tên).

**Ghi chú kỹ thuật** (theo yêu cầu review): đã ghi rõ trong docblock — 120 ký tự đo trên bản KHÔNG
có thẻ `<b>` (biến `$plainHead`), vì đây là số ký tự thực sự NGƯỜI DÙNG NHÌN THẤY trên màn khoá/push
(thẻ chỉ là markup hiển thị đậm cho FE `v-html`, không phải ký tự hiển thị) — chuỗi trả về CÓ bọc
`<b>` dài hơn 7 ký tự markup vẫn đúng tinh thần "≤ 120 ký tự nhìn thấy". Chọn đo trên bản plain thay
vì bản có tag, ghi lại quyết định này để không ai hiểu nhầm là quên trừ độ dài thẻ.

**Test mới** (`tests/Unit/MeetingRoomBookingNotificationContentTest.php`, PHPUnit thuần — hàm không
đụng DB): 9 ca (test_tong_do_dai... có 5 data set) —
- (a) `test_ten_doi_tuong_qua_50_ky_tu_thi_bi_cat_con_47_ky_tu_them_ba_cham` — tên 60 ký tự bị cắt
  đúng còn 47 + `...` (50 ký tự).
- (b) `test_tu_choi_tieu_de_dai_va_ly_do_dai_thi_ly_do_van_con_bi_cat_ngan_khong_bi_xoa` — CA BẮT
  LỖI THẬT: tiêu đề > 50 ký tự + `reject_reason` dài (~180 ký tự) → nội dung VẪN còn nhãn "Lý do:"
  + một phần thật của lý do gốc (so khớp 10 ký tự đầu của lý do gốc phải xuất hiện đúng ở đầu phần
  còn lại — chứng minh cắt từ CUỐI, không phải cắt ngẫu nhiên/xoá sạch).
- (c) `test_tong_do_dai_luon_toi_da_120_ky_tu_o_moi_to_hop_dai_ngan` (5 tổ hợp tên/ghi chú dài-ngắn,
  gồm tổ hợp xấu nhất tên 80 ký tự + ghi chú lặp ~900 ký tự) — luôn ≤ 120 ký tự đo trên bản KHÔNG
  thẻ `<b>`.
- 2 ca phụ trợ: ghi chú ngắn giữ nguyên (không tự thêm `...` khi không cần), không có ghi chú thì
  không thừa khoảng trắng cuối câu.

Chạy riêng: `vendor/bin/phpunit --filter MeetingRoomBookingNotificationContent` → **9/9 PASS**
(gộp trong lần chạy `--filter "MeetingRoom"` tổng, xem dòng tổng kết cuối file).

## IMPORTANT 2 — `MeetingRoomService::destroy()` chưa có test chứng minh thứ tự khóa

Đây là **việc nối tiếp của Task 14** (agent phụ trách bị dừng giữa chừng) — bẫy 3 của
`task-13-brief.md`/`task-14-brief.md`/`task-15-brief.md`. Bản vá (khóa `meeting_rooms` TRƯỚC
`meeting_room_bookings` trong `destroy()`) **đã có sẵn trong code** khi tôi nhận việc — tôi chỉ bổ
sung bằng chứng test tự động + tài liệu, KHÔNG viết lại logic nghiệp vụ. Toàn bộ chi tiết (bản vá,
lý do, test mới, đối chứng âm ĐỎ→XANH) đã ghi đầy đủ vào
**`.sdd/task-14-report.md` mục "Fix round 2"** (đúng chỗ của nó — đây là việc thuộc Task 14, không
phải Task 15) theo đúng yêu cầu MINOR của review. Tóm tắt nhanh:

- Test mới: `test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking()` trong
  `tests/Feature/MeetingRoomBookingRaceTest.php` — gọi trực tiếp `MeetingRoomService::destroy()`
  thật, bắt SQL bằng `DB::listen()`, khẳng định chỉ số mảng của câu `FOR UPDATE` trên
  `meeting_rooms` NHỎ HƠN chỉ số câu `FOR UPDATE` trên `meeting_room_bookings` (kiểm THỨ TỰ, không
  chỉ sự tồn tại).
- Đối chứng âm: đảo tạm 2 lệnh khóa trong `destroy()` → **ĐỎ** (`Failed asserting that 1 is less
  than 0`, SQL log cho thấy `meeting_room_bookings` chạy TRƯỚC `meeting_rooms`) → hoàn nguyên →
  **XANH** (39/39). Output đầy đủ nằm trong `task-14-report.md`.

## MINOR — bổ sung mục "Fix round 2" vào `task-14-report.md`

Đã làm — xem file đó, mục cuối cùng.

## File sửa/tạo thêm ở fix round 1 (Task 15)

- Sửa `Modules/Meeting/Services/MeetingRoomBookingService.php` — viết lại `buildNotificationContent()`
  (IMPORTANT 1).
- Tạo `tests/Unit/MeetingRoomBookingNotificationContentTest.php` (IMPORTANT 1).
- Sửa `tests/Feature/MeetingRoomBookingRaceTest.php` — thêm
  `test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking()` + import
  `Modules\Meeting\Services\MeetingRoomService` (IMPORTANT 2).
- Sửa `.plans/gop-db/quan-ly-phong-hop/.sdd/task-14-report.md` — thêm mục "Fix round 2" (MINOR).
- KHÔNG đụng `reject()`/`cancel()` (lỗi `manager_employee_id` không khóa) — coordinator đã ghi
  nhận, chủ động để lại.

## Kết quả chạy (foreground, đọc dòng tổng kết) — sau khi sửa cả 2 Important

**`vendor/bin/phpunit --filter "MeetingRoom"`** — chạy 2 lần liên tiếp:

Lần 1:
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
.......................................                           39 / 39 (100%)
OK (39 tests, 80 assertions)
```

Lần 2 (lặp lại để chắc không flaky):
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
.......................................                           39 / 39 (100%)
OK (39 tests, 80 assertions)
```

(39 test = 9 ca mới `MeetingRoomBookingNotificationContentTest` + 5 ca cũ `MeetingRoomBookingRaceTest`
gồm 1 ca mới `test_destroy_...` + các ca `MeetingRoomBookingOverlapTest`/`MeetingRoomBookingStateTest`/
`MeetingRoomConfigTest` không đổi.)

**`tests/meeting --project=api --no-deps --workers=1`** (Playwright, foreground) — chạy 2 lần liên
tiếp, xác nhận `buildNotificationContent()` không làm hỏng 45 ca booking cũ (kể cả K3/K4 đọc nội
dung "Lý do:"):

Lần 1:
```
Running 59 tests using 1 worker
...
59 passed (1.9m)
```

Lần 2:
```
Running 59 tests using 1 worker
...
59 passed (1.7m)
```

Không có `flaky`/`failed`/`did not run` ở bất kỳ lần chạy nào (cả PHPUnit lẫn Playwright).

## Kiểm DB sạch rác sau fix round 1

```sql
rooms_leftover_e2e          0   -- meeting_rooms code LIKE 'E2E_%'
rooms_leftover_phpunit      0   -- meeting_rooms code LIKE 'PHPUNIT_%'
bookings_leftover_no_room   0   -- meeting_room_bookings mồ côi (không còn phòng)
notifications_leftover      0   -- notifications type LIKE 'meeting_room_booking_%'
```

## Concerns còn lại sau fix round 1

- `reject()`/`cancel()` đọc `manager_employee_id` không khóa phòng trước — theo chỉ đạo coordinator,
  KHÔNG sửa, để lại làm việc của vòng khác.
- IMPORTANT 2 chỉ chứng minh THỨ TỰ khóa đúng trong 1 lần gọi đơn lẻ, chưa có đối chứng 2-tiến-trình
  song song thật cho cặp `destroy()` + `store()`/`update()` (đã ghi rõ trong `task-14-report.md`
  mục "Concerns mới sau fix round 2").
