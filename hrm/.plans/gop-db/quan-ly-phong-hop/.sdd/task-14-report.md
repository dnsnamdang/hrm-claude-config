# Task 14 report — Duyệt / Từ chối / Hủy phiếu + luật nhìn thấy phiếu

**Status: DONE** — 3 endpoint mới (approve/reject/cancel) + luật nhìn thấy phiếu áp vào
`index()`/`show()`. TDD đỏ→xanh đầy đủ. Chạy lại 2 lần liên tiếp cả thư mục `tests/meeting
--project=api` ở **foreground**: cả 2 lần **52 passed, không có dòng `flaky`/`failed`/`did not run`**.

## File sửa / tạo (chỉ trong `Modules/Meeting/` + `e2e/tests/meeting/`)

Tạo mới:
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRejectRequest.php` — validate
  `reject_reason` bắt buộc.
- `Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingCancelRequest.php` — validate
  `cancel_reason` bắt buộc.

Sửa:
- `Modules/Meeting/Services/MeetingRoomBookingService.php`
  - Thêm `approve()`, `reject()`, `cancel()`, `canActOnApprovalByRoom()`.
  - Thêm `applyVisibilityScope()` (dùng trong `index()`) và `canView()` (dùng trong `loadDetail()`)
    — luật nhìn thấy phiếu (Task 12 bước 4): không có quyền *Xem tất cả phiếu đặt phòng họp* thì
    chỉ thấy phiếu mình đặt / được mời (participants) / phòng mình quản lý.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php`
  - Thêm action `approve()`, `reject()`, `cancel()`.
  - Bọc `show()` bằng try/catch để trả đúng mã lỗi khi `loadDetail()` ném 403 (không đủ điều kiện
    nhìn thấy phiếu).
- `Modules/Meeting/Routes/api.php` — thêm 3 route `PUT .../approve`, `.../reject`, `.../cancel`.
- `e2e/tests/meeting/meeting-room-booking.api.spec.ts`
  - Thêm nhóm **G** (duyệt + tự động từ chối trùng), **H** (từ chối), **I** (hủy + quyết định #12),
    **J** (luật nhìn thấy phiếu) — 16 ca mới (38 ca tổng, từ 22 ca gốc Task 13... thực tế 22 vì F1/F2
    đã có; xem chi tiết bên dưới).
  - Sửa ca **F2** (Task 13): thêm `participant_ids: [25]` khi tạo `bookingAtOutsiderRoom` — luật
    nhìn thấy phiếu mới (Task 14) áp vào `show()` sẽ chặn 403 nếu không cập nhật, vì actor `nocost`
    trong ca này vốn không liên quan gì tới phòng đó (đúng tinh thần CLAUDE.md: đổi hành vi phải cập
    nhật ca cũ, không phải bỏ qua).
  - Sửa `afterAll` — gộp N câu `DELETE ... WHERE id=X` (mỗi câu tự spawn 1 tiến trình `mysql` CLI)
    thành 2 câu `DELETE ... WHERE id IN (...)` + `test.setTimeout(120000)`. Đây là fix **hiệu năng
    dọn dẹp**, không liên quan tới luật nghiệp vụ — cần thiết vì Task 14 gần gấp đôi số phòng/phiếu
    file này tạo ra, vượt ngân sách mặc định 30s của hook `afterAll`.

## Quyết định kỹ thuật khác với chữ nghĩa literal của RÀNG BUỘC

Đề bài viết: *"Route duyệt/từ chối gắn checkPermission phù hợp"*. Tôi **cố tình KHÔNG** gắn
`checkPermission:Duyệt phiếu đặt phòng họp` (quyền 1580) làm middleware route cho `approve`/`reject`,
vì **spec 5.3 (nguồn chân lý)** ghi rõ: *"Người duyệt = người quản lý phòng (`manager_employee_id`)
HOẶC người có quyền Duyệt phiếu đặt phòng họp"*. Quyền 1580 là quyền TĨNH theo role; "có phải quản lý
CỦA ĐÚNG PHÒNG này" là dữ liệu của TỪNG BẢN GHI — middleware route không kiểm được. Gắn cứng
middleware đó sẽ **chặn luôn** quản lý phòng hợp lệ không có quyền 1580 (chính là ca G4/I3 trong định
nghĩa hoàn thành, và ca F1/F2 đã có sẵn từ Task 13). Gate thật nằm trong
`MeetingRoomBookingService::canActOnApprovalByRoom()`, chạy TRONG transaction có khóa — đúng tinh
thần "Gate ở BE trước" của spec 5.3. Đã ghi rõ lý do bằng comment tại `Routes/api.php` và tại chính
hàm đó.

## Bằng chứng ĐỎ → XANH

**RED (trước khi cài BE)** — chạy `meeting-room-booking.api.spec.ts` một mình:
```
✘ G1. ... — kiểm bằng DB thật   (404 — route chưa tồn tại)
15 did not run
22 passed (2.1m)
```
(22 ca A-F của Task 13 vẫn xanh nguyên — xác nhận baseline chưa bị đụng trước khi sửa BE.)

**GREEN (sau khi cài BE, trước khi phát hiện flake)** — chạy riêng file, 38 ca: 37 passed + 1 failed
(J3) do `afterAll` hook vượt 30s (lỗi dọn dẹp, không phải lỗi logic) → đã sửa bằng batch SQL nói trên.

## Điều tra ca flaky (theo yêu cầu coordinator) — KẾT LUẬN: môi trường, không phải lỗi logic

**Dữ kiện coordinator đưa**: chạy `tests/meeting --project=api --no-deps --workers=1` ra
`1 flaky` tại **G1** (đỏ lần 1, xanh khi Playwright tự retry), `51 passed`.

**Không truy được trace gốc của đúng lần chạy đó** — `test-results/`/`playwright-report/` bị một
phiên Playwright KHÁC (đang chạy `potential-customer-care.spec.ts`, xác nhận bằng `ps aux` thấy
tiến trình Chrome/node của phiên đó tại đúng thời điểm) ghi đè trước khi tôi kịp đọc. Vì vậy kết luận
dưới đây dựa trên (a) review lại code đường đi của `approve()`, và (b) đối chiếu thời lượng chạy +
tương quan tải hệ thống qua nhiều lần chạy — không phải đọc trực tiếp stack trace của đúng lần fail
đó. Nếu ca này tái phát khi chạy ĐƠN ĐỘC (không phiên nào khác chạy song song) thì cần điều tra lại
bằng trace thật, kết luận dưới đây KHÔNG coi là đóng hồ sơ vĩnh viễn.

**1) Review code — G1 KHÔNG có actor đồng thời nào để xảy ra race thật:**
G1 chạy hoàn toàn TUẦN TỰ, 1 client: tạo 3 phiếu (await từng cái một) → gọi `PUT .../approve` 1 lần
→ đọc lại bằng `mysql` CLI (kết nối MỚI, riêng biệt). Khác với ca C1 (Task 13) vốn cố tình bắn
`Promise.all()` 2 request cùng lúc để kiểm race thật, G1 không có 2 actor nào tranh chấp cùng 1 dòng.
`DB::transaction()` của Laravel COMMIT xong TRƯỚC KHI controller trả response HTTP (không có job
hàng đợi/commit bất đồng bộ) — nên khi `await api.put(...)` ở test resolve, transaction đã commit;
1 kết nối `mysql` MỚI mở sau đó luôn thấy dữ liệu đã commit (không có vấn đề visibility xuyên kết
nối kiểu snapshot cũ, vì snapshot của kết nối mới chỉ mở SAU thời điểm commit).
Thứ tự khóa trong `approve()` (Room → Booking đích → các Booking Chờ duyệt xung đột) khớp đúng thứ
tự đã dùng ở `assertNoOverlap()`/`store()`/`update()` (đã kiểm chứng ở Task 13) — không có lock-order
mới bị đảo ngược để gây deadlock/race.

**2) Tương quan thời lượng chạy — dấu hiệu tranh chấp tài nguyên hệ thống, không phải bug cố định
ở 1 điểm:**

| Lần chạy | Tải hệ thống lúc chạy | Kết quả | Thời lượng |
|---|---|---|---|
| Run 1 (ngay sau khi cài BE) | Phiên khác đang chạy `potential-customer-care.spec.ts` (Chrome + `artisan serve:8000`) — xác nhận bằng `ps aux` | 37 passed, 1 failed ở **J3** (do `afterAll` timeout — đã sửa) | 4.1 phút |
| Run 2 (sau khi sửa `afterAll`) | Cùng phiên khác vẫn chạy | 37 passed + **1 flaky ở A1** (GET đơn giản trong `beforeAll`, không đụng gì tới `approve()`) | 4.6 phút |
| Coordinator's run | (không rõ, nhưng cùng khung giờ) | 51 passed + **1 flaky ở G1** | 7.4 phút |
| Run 3 (phiên khác đã tắt — xác nhận `ps aux` không còn) | Sạch | **38 passed, 0 flaky** | 2.2 phút |
| Run 4 — cả thư mục, foreground | Sạch | **52 passed, 0 flaky** | 1.8 phút |
| Run 5 — cả thư mục, foreground, lặp lại | Sạch | **52 passed, 0 flaky** | 1.5 phút |

Điểm mấu chốt: **3 lần flaky khác nhau rơi vào 3 test KHÁC NHAU** (A1 đọc danh sách phòng, G1 duyệt
phiếu, J3 vốn không tự fail mà do hook dọn dẹp) — không lặp lại ở cùng 1 dòng code. Đây là chữ ký của
tranh chấp tài nguyên dùng chung (CPU/MySQL connections trên cùng máy, khi có ít nhất 2 phiên Claude
chạy Playwright + PHP dev server + MySQL cùng lúc — đúng cảnh báo đã ghi trong memory "Chạy e2e phải
--workers=1 ... cũng đừng chạy khi có agent khác đang thao tác dữ liệu"), không phải lỗi xác định ở
logic `approve()`/tự-động-từ-chối. Một race THẬT trong code (thiếu khóa) sẽ tái hiện ổn định tại
CHÍNH ca đó khi có đủ điều kiện kích hoạt, không nhảy lung tung sang các ca không liên quan.

**Kết luận**: flaky của G1 (và A1 trước đó) là **do môi trường** (nhiều phiên Playwright + PHP dev
server + MySQL chạy đồng thời trên cùng máy), **không phải lỗi logic** trong `approve()`. Không sửa
gì ở logic nghiệp vụ để "vá" ca này — chỉ sửa đúng 1 vấn đề hiệu năng thật đã tìm thấy độc lập
(`afterAll` batch SQL, nêu trên). Sau khi xác nhận không còn phiên nào khác chạy song song, chạy lại
**2 lần liên tiếp ở foreground cả thư mục `tests/meeting`** đều **52 passed, không dòng `flaky`**.

## Dòng tổng kết 2 lần chạy cuối (foreground, sau khi hết tranh chấp tài nguyên)

Lần 1:
```
Running 52 tests using 1 worker
...
52 passed (1.8m)
```

Lần 2 (chạy lại ngay sau):
```
Running 52 tests using 1 worker
...
52 passed (1.5m)
```

Không có `flaky`, không có `failed`, không có `did not run` ở cả 2 lần.

## Kết quả 3 ca trọng tâm (đã xanh ở cả 2 lần chạy cuối)

1. **G1** — tạo 3 phiếu Chờ duyệt trùng giờ cùng phòng, duyệt 1 phiếu → phiếu đó `status=2`
   (Đã duyệt), 2 phiếu còn lại **tự động** `status=3` (Từ chối) với `is_auto_rejected=1` và
   `reject_reason='Phòng đã được duyệt cho cuộc họp khác'` — kiểm bằng **truy vấn SQL trực tiếp**,
   không chỉ tin response JSON. PASS.
2. **I6** — phiếu `source=2` (dựng bằng `UPDATE ... SET source=2` trực tiếp, dọn sạch ở `afterAll`):
   cả **chính chủ (admin)** lẫn **quản lý phòng (nocost)** gọi `PUT .../cancel` đều nhận **423**.
   PASS.
3. **J1** — quản lý phòng (`nocost`, KHÔNG có quyền 1579) vẫn thấy phiếu **của người khác đặt**
   trong phòng mình quản lý qua cả `GET index()` (có mặt trong danh sách) lẫn `GET show()`
   (200, không bị 403). PASS. Đối chứng **J2** (người ngoài hoàn toàn) bị lọc khỏi `index()` và
   `show()` trả 403 — xác nhận luật không bị fail-open.

## Kiểm DB sạch rác

```sql
SELECT COUNT(*) FROM meeting_rooms WHERE code LIKE 'E2E%';                                  -- 0
SELECT COUNT(*) FROM meeting_room_amenities WHERE code LIKE 'E2E%';                          -- 0
SELECT COUNT(*) FROM meeting_room_bookings b
  JOIN meeting_rooms r ON r.id=b.meeting_room_id WHERE r.code LIKE 'E2E%';                   -- 0
```

## Concerns

1. **Deviation đã ghi ở trên** (không gắn `checkPermission` middleware cứng cho approve/reject) —
   nếu đội thấy cần "gắn checkPermission" theo đúng nghĩa route middleware, sẽ phải chấp nhận đánh
   đổi: quản lý phòng không có quyền 1580 sẽ KHÔNG duyệt được nữa, trái spec 5.3 và phá vỡ ca G4/I3.
2. **Thông báo (Task 15)** — cố tình KHÔNG implement gửi thông báo cho duyệt/từ chối/hủy trong Task
   này; theo `plan.md` đây là phạm vi riêng của Task 15 (`buildNotificationContent`, map
   `employee_info_id` qua Bẫy 1). Không phải thiếu sót của Task 14.
3. **Kết luận flaky dựa trên review code + tương quan thời lượng**, KHÔNG dựa trên trace/stack của
   đúng lần fail (đã bị phiên khác ghi đè trước khi đọc được) — nếu G1 flaky tái phát khi chạy đơn
   độc (chắc chắn không phiên nào khác đụng máy), cần điều tra lại bằng trace thật trước khi coi đây
   là kết luận cuối cùng.
4. Route model binding trong `approve()` đọc `$booking->meeting_room_id` để khóa Room TRƯỚC KHI khóa
   chính dòng Booking đó — về lý thuyết có 1 cửa sổ cực hẹp nếu đúng lúc đó có `update()` khác đổi
   `meeting_room_id` của CÙNG booking đang chờ duyệt (đổi phòng phiếu Chờ duyệt). Không có test cho
   trường hợp này (ngoài phạm vi brief), độ phức tạp/rủi ro thấp vì đổi phòng 1 phiếu đang Chờ duyệt
   trong lúc nó vừa được duyệt là kịch bản hiếm, nhưng nêu ra để đội biết nếu cần khóa chặt hơn sau
   này.

---

# Fix round 1 — Important (thứ tự khóa ngược giữa `update()` và `approve()`) + Minor (log nhiễu)

**Status: DONE.** Reviewer xác nhận kết luận flaky ở lần trước đã khép lại (không cần điều tra
thêm). Phần dưới đây xử lý đúng 2 phát hiện mới: 1 Important (nguy cơ deadlock thật), 1 Minor
(log nhiễu).

## 1. IMPORTANT — thứ tự khóa `update()` ngược với `approve()`/`store()`

**Xác nhận đúng như review chỉ ra**: `update()` (viết ở Task 13) khóa **Booking trước**
(`MeetingRoomBooking::where('id',...)->lockForUpdate()->firstOrFail()` ở đầu hàm) rồi mới gọi
`assertNoOverlap()` — hàm này khóa **Room** ở bên trong. Trong khi đó `approve()` (Task 14) khóa
**Room trước, Booking sau**. Hai chiều ngược nhau → 1 `PUT .../update` và 1 `PUT .../approve` chạm
cùng phiếu/phòng cùng lúc là deadlock kinh điển (MySQL tự giết 1 giao dịch, lỗi SQL thô lọt ra
ngoài thành 500 vì Controller `catch (Exception $e)` chung).

**Sửa**: `Modules/Meeting/Services/MeetingRoomBookingService.php`
- `update()` giờ khóa **Room TRƯỚC** (`MeetingRoom::where('id', $request->meeting_room_id)
  ->lockForUpdate()->firstOrFail()`), dùng lại biến `$room` đó cho toàn bộ phần còn lại của hàm
  (bỏ luôn lệnh `MeetingRoom::findOrFail()` thứ 2 trùng lặp trước đây), rồi mới khóa dòng Booking.
- Ghi rõ **QUY ƯỚC KHÓA DUY NHẤT của cả module** (Room trước, Booking sau) ngay trong docblock của
  `update()` — nơi dễ thấy nhất vì đây là hàm từng vi phạm quy ước.
- Sửa lại docblock của `approve()` — bản trước khẳng định sai "đã giữ đúng thứ tự khóa với
  store()/update()"; giờ ghi đúng: khớp `store()`/`assertNoOverlap()` từ Task 13, và `update()` MỚI
  ĐƯỢC SỬA ở fix round này để khớp theo, không phải đã khớp sẵn từ đầu.
- `assertNoOverlap()` vẫn tự khóa lại Room bên trong (dùng chung cho cả `store()` lẫn `update()`) —
  với `update()` giờ đây là khóa LẶP LẠI trên CÙNG 1 dòng đã khóa (vô hại, MySQL cho phép 1
  transaction tự khóa lại dòng nó đang giữ, không phải khóa mới/khóa chéo).

## 2. Ca test chứng minh `approve()` lấy mutex phòng (bằng thực nghiệm, không chỉ đọc code)

Thêm `test_approve_that_su_dung_lockForUpdate_tren_dong_phong()` vào
`tests/Feature/MeetingRoomBookingRaceTest.php` — dùng ĐÚNG kỹ thuật của
`test_assertNoOverlap_that_su_dung_lockForUpdate_tren_dong_phong()` (Task 13): gọi trực tiếp
`approve()` (public, không cần Reflection), bắt toàn bộ SQL bằng `DB::listen()`, khẳng định có câu
`SELECT ... meeting_rooms ... FOR UPDATE`. Actor đăng nhập = chính `manager_employee_id` của phòng
test (qua `actingAs($manager, 'api')`) để `canActOnApprovalByRoom()` trả `true` qua nhánh
`isRoomManager`, không cần dựng thêm role/permission — cô lập đúng biến đang kiểm (có khóa hay
không), không lẫn logic phân quyền.

**Đối chứng ÂM (thủ công, bắt buộc theo yêu cầu review) — 2 output dán nguyên văn:**

Bước 1 — gỡ tạm dòng khóa (`MeetingRoom::where('id', $booking->meeting_room_id)->lockForUpdate()->firstOrFail();`
→ bỏ `->lockForUpdate()`), chạy lại đúng ca test:

```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

F                                                                   1 / 1 (100%)

Time: 00:00.716, Memory: 44.50 MB

There was 1 failure:

1) Tests\Feature\MeetingRoomBookingRaceTest::test_approve_that_su_dung_lockForUpdate_tren_dong_phong
approve() PHẢI chạy 1 câu SELECT...FOR UPDATE khoá dòng `meeting_rooms` (mutex, fix round 1 Task 14
IMPORTANT) TRƯỚC KHI tự-động-từ-chối phiếu trùng — không thấy câu nào trong SQL log: [...danh sách
SQL thật sự chạy, không có câu nào chứa "meeting_rooms" + "for update"...]
Failed asserting that an array is not empty.

FAILURES!
Tests: 1, Assertions: 2, Failures: 1.
```

Bước 2 — hoàn nguyên dòng `->lockForUpdate()`, chạy lại:

```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

.                                                                   1 / 1 (100%)

Time: 00:00.570, Memory: 44.50 MB

OK (1 test, 3 assertions)
```

Đỏ → xanh đúng như yêu cầu, không phụ thuộc timing (đọc lại SQL log của 1 lần gọi, không đua thật).

## 3. MINOR — log nhiễu (`Log::error()` cho cả lỗi nghiệp vụ hợp lệ)

`MeetingRoomBookingController` trước đây gọi `Log::error($e)` vô điều kiện ở CẢ 6 action
(show/store/update/approve/reject/cancel), kể cả khi exception chỉ là 403 (không đủ quyền)/422
(validate)/423 (khóa/sai trạng thái) — những phản hồi ĐÚNG THIẾT KẾ cho request sai, không phải sự
cố hệ thống.

**Sửa**: gộp cả 6 catch-block trùng lặp thành 1 helper `private function handleServiceException()`
— chỉ `Log::error($e)` khi mã lỗi KHÔNG nằm trong 3 mã nghiệp vụ đã biết (403/422/423); các action
giờ chỉ còn `return $this->handleServiceException($e);`. Vừa hết log nhiễu, vừa giảm lặp code ở 6
nơi giống hệt nhau (tiện thể dọn `show()` — trước đó có catch nhưng KHÔNG hề gọi `Log::error()`,
giờ đồng nhất qua cùng 1 helper).

## 4. Kết quả chạy sau khi sửa (foreground, đọc dòng tổng kết)

**`vendor/bin/phpunit --filter "MeetingRoom"`:**
```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

.............................                                     29 / 29 (100%)

Time: 00:11.045, Memory: 124.50 MB

OK (29 tests, 57 assertions)
```

**`tests/meeting --project=api --no-deps --workers=1`, chạy 2 lần liên tiếp ở foreground:**

Lần 1:
```
...
  52 passed (1.3m)
```

Lần 2 (chạy lại ngay sau):
```
...
  52 passed (1.6m)
```

Không có dòng `flaky`, `failed`, hay `did not run` ở cả 2 lần.

## 5. Kiểm DB sạch rác sau khi chạy

```sql
SELECT COUNT(*) FROM meeting_rooms WHERE code LIKE 'E2E%';                                    -- 0
SELECT COUNT(*) FROM meeting_room_amenities WHERE code LIKE 'E2E%';                            -- 0
SELECT COUNT(*) FROM meeting_room_bookings b JOIN meeting_rooms r
  ON r.id=b.meeting_room_id WHERE r.code LIKE 'E2E%';                                          -- 0
SELECT COUNT(*) FROM meeting_rooms WHERE code LIKE 'PHPUNIT_RACE%' OR code LIKE 'PHPUNIT_APPROVE%'; -- 0
SELECT COUNT(*) FROM meeting_room_bookings WHERE code LIKE 'PHPUNIT_RACE%'
  OR code LIKE 'PHPUNIT_APPROVE%' OR code LIKE 'RACE-PHPUNIT%';                                -- 0
```

## File sửa thêm ở fix round 1

- `Modules/Meeting/Services/MeetingRoomBookingService.php` — đổi thứ tự khóa `update()`, sửa lại
  docblock `approve()`.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php` — gộp `Log::error()`
  có điều kiện vào `handleServiceException()`.
- `tests/Feature/MeetingRoomBookingRaceTest.php` — thêm
  `test_approve_that_su_dung_lockForUpdate_tren_dong_phong()`.

(File này nằm ngoài `Modules/Meeting/` + `e2e/tests/meeting/` nhưng đã là nơi Task 13 đặt sẵn toàn
bộ bộ test khóa DB tự động của module — tiếp tục đặt ca mới vào đây để dùng chung hạ tầng
`createTestRoom()`/`tearDown()` sẵn có, không tạo file rời rạc mới.)

## Concerns mới sau fix round 1

- Chưa có ca kiểm tra CHÉO thật giữa `update()` và `approve()` (bắn đồng thời 1 `update()` + 1
  `approve()` lên CÙNG phiếu để chứng minh KHÔNG còn deadlock) — ca test mới chỉ chứng minh
  `approve()` CÓ lấy mutex, chưa dựng lại kịch bản deadlock 2-chiều bằng 2 tiến trình song song như
  `test_co_mutex_thi_hai_ket_noi_song_song_chi_tao_duoc_1_phieu()` đã làm cho `store()`. Vì cả 2
  hàm giờ cùng khóa Room trước, về lý thuyết đồ thị chờ không còn chu trình (không đối xứng ngược
  chiều nữa), nhưng chưa có bằng chứng thực nghiệm 2-tiến-trình riêng cho ĐÚNG cặp `update()` +
  `approve()` như đã làm cho `store()` + `store()`.

# Fix round 2 — IMPORTANT bẫy 3 (`MeetingRoomController::destroy()` không `lockForUpdate`)

> Agent phụ trách vòng vá này bị kẹt giữa chừng rồi bị dừng — mục này được bổ sung lại (nối tiếp)
> bởi agent làm Task 15 (xem `.sdd/task-15-report.md` mục "Fix round 1" IMPORTANT 2), dựa trên
> đúng nội dung code đã có sẵn trong `MeetingRoomService::destroy()` tại thời điểm nhận việc.

## 1. Bẫy 3 (task-15-brief.md, kế thừa nguyên văn từ task-13-brief.md/task-14-brief.md)

`MeetingRoomController::destroy()` (qua `MeetingRoomService::destroy()`) trước đây kiểm
`isCanDelete()` (đọc thô `meeting_room_bookings`, KHÔNG khóa) RỒI MỚI mở transaction — Phase 1 chưa
ai ghi được vào bảng phiếu nên cửa sổ lỗi chưa từng tồn tại thật; Phase 2 (Task 13) mở luồng đặt
phòng là nó thành thật ngay: 1 request đặt phòng đúng lúc admin bấm Xóa → phiếu mồ côi
(`meeting_room_id` trỏ tới phòng đã bị xóa).

## 2. Bản vá đã có sẵn trong code (xác nhận lại, KHÔNG phải agent này viết mới)

`Modules/Meeting/Services/MeetingRoomService::destroy()` tại thời điểm nhận việc ĐÃ đổi sang:

```php
public function destroy(MeetingRoom $meetingRoom)
{
    // Room TRƯỚC (đúng quy ước khóa của module) — khóa lại chính dòng đang xử lý để chắc
    // không đọc phải bản đã bị đổi bởi giao dịch khác đang chờ, rồi mới khóa Booking.
    $meetingRoom = MeetingRoom::where('id', $meetingRoom->id)->lockForUpdate()->firstOrFail();

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

Đúng QUY ƯỚC KHÓA DUY NHẤT của cả module (Room trước, Booking sau — cùng chiều với
`store()`/`update()`/`approve()`/`assertNoOverlap()`): 1 request `destroy()` và 1 request
`update()`/`approve()` chạm cùng phòng cùng lúc sẽ KHÔNG deadlock (không còn đồ thị chờ vòng —
`update()`/`approve()` cũng luôn khóa Room trước Booking, cùng chiều). `MeetingRoomController::destroy()`
đã bọc lời gọi này trong `DB::transaction()` (không đổi ở vòng vá này).

## 3. Trước vòng vá này: CHỈ xác minh BẰNG MẮT, chưa có test tự động

Khác với `approve()`/`assertNoOverlap()` (đã có `test_approve_that_su_dung_lockForUpdate_tren_dong_phong()`
/ `test_assertNoOverlap_that_su_dung_lockForUpdate_tren_dong_phong()` bắt SQL thật bằng
`DB::listen()`), `destroy()` chưa có ca nào — nếu ai vô tình đảo lại thứ tự 2 câu khóa (hoặc xóa hẳn
1 trong 2), không ca test nào phát hiện được.

## 4. Test mới — `test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking()`

Thêm vào `tests/Feature/MeetingRoomBookingRaceTest.php`, dùng ĐÚNG kỹ thuật của
`test_approve_that_su_dung_lockForUpdate_tren_dong_phong()` (gọi trực tiếp method thật, bắt SQL bằng
`DB::listen()`), nhưng khác biệt quan trọng: bắt buộc kiểm CẢ THỨ TỰ 2 câu `FOR UPDATE` (chỉ số
mảng của câu khóa `meeting_rooms` phải nhỏ hơn chỉ số câu khóa `meeting_room_bookings`), không chỉ
kiểm sự TỒN TẠI — vì cái đang được vá chính là THỨ TỰ khóa; khóa đảo ngược vẫn "có" đủ cả 2 câu
`FOR UPDATE`, chỉ riêng đối chứng tồn tại sẽ không bắt được lỗi deadlock đúng kiểu.

## 5. Đối chứng ÂM (bắt buộc theo yêu cầu review) — ĐỎ → hoàn nguyên → XANH

Đảo tạm 2 lệnh khóa trong `destroy()` (Booking trước, Room sau):

```
1) Tests\Feature\MeetingRoomBookingRaceTest::test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking
destroy() PHẢI khoá `meeting_rooms` TRƯỚC `meeting_room_bookings` (...). SQL log:
["select exists(select * from `meeting_room_bookings` where `meeting_room_id` = ? for update) as `exists`",
 "select * from `meeting_rooms` where `id` = ? limit 1 for update",
 "delete from `meeting_room_room_amenity` where `meeting_room_room_amenity`.`meeting_room_id` = ?",
 "delete from `meeting_rooms` where `id` = ?"]
Failed asserting that 1 is less than 0.

FAILURES!
Tests: 1, Assertions: 3, Failures: 1.
```

Hoàn nguyên đúng thứ tự gốc (Room trước, Booking sau) — chạy lại cả bộ:

```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.
.......................................                           39 / 39 (100%)
OK (39 tests, 80 assertions)
```

## 6. File sửa thêm ở fix round 2

- `tests/Feature/MeetingRoomBookingRaceTest.php` — thêm
  `test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking()` + import
  `Modules\Meeting\Services\MeetingRoomService`.
- `Modules/Meeting/Services/MeetingRoomService.php` — KHÔNG đổi nội dung nghiệp vụ (đã đúng sẵn từ
  trước khi agent này nhận việc); chỉ tạm sửa rồi hoàn nguyên đúng bản gốc để làm đối chứng âm ở
  mục 5 (đã diff lại xác nhận khớp 100% bản trước khi sửa).

## Concerns mới sau fix round 2

- Vẫn CHƯA có bằng chứng thực nghiệm 2-tiến-trình song song thật (kiểu
  `test_co_mutex_thi_hai_ket_noi_song_song_chi_tao_duoc_1_phieu()`) cho ĐÚNG cặp `destroy()` +
  `store()`/`update()` — ca mới chỉ chứng minh THỨ TỰ khóa đúng trong 1 lần gọi đơn lẻ (đủ để bắt
  lỗi "ai đó đảo/xóa dòng khóa", nhưng chưa mô phỏng deadlock 2 tiến trình thật như đã làm cho
  `store()` ở Task 13).
- `reject()`/`cancel()` đọc `manager_employee_id` của phòng qua `canActOnApprovalByRoom()` mà
  KHÔNG `lockForUpdate` phòng trước — coordinator đã ghi nhận là lỗi có sẵn từ trước, CHỦ ĐỘNG để
  lại, không sửa trong vòng này.
