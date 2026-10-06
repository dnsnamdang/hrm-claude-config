# Báo cáo — Phase 8 / lượt A2 (task T114–T117 + BS-1/BS-2/BS-3): vá phần đặt phòng bị gãy sau khi A1 drop `manager_employee_id`

Repo: `hrm-api`, nhánh `gop_db`. DB local: `hrm_erp` (2 phòng họp, 3 phiếu đặt phòng trước khi làm —
đúng ghi chú giao việc, đã xác nhận lại bằng tinker trước khi động vào code).

## Trạng thái: DONE

Toàn bộ BS-1 → T114 → T115 → BS-2 → BS-3/T116 → T117 đã làm xong theo đúng thứ tự ưu tiên brief
yêu cầu. Không còn chỗ nào (ngoài migration) đọc quan hệ `manager()`/cột `manager_employee_id` đã bị
A1 xoá. PHPUnit không đỏ thêm ca nào so với baseline; test mới viết thêm 4 ca đều xanh.

---

## 1. Việc đã làm theo từng nhóm

### BS-1 — 7 chỗ `room.manager.info` trong `MeetingRoomBookingService.php` (ưu tiên #1, endpoint 500)

`grep -n "room.manager"` xác nhận đúng 7 chỗ ở các dòng 216, 362, 425, 559, 652, 696, 756 (số dòng
TRƯỚC khi sửa). Đổi hết `->with([..., 'room.manager.info', ...])` →
`->with([..., 'room.managers.info', ...])` bằng `sed` (kiểm lại bằng grep sau đó — cả 7 chỗ đã đổi,
không sót, không thừa). Đây là **nguyên nhân 500 thật** brief mô tả (`RelationNotFoundException`
ngay lúc Eloquent build query, trước khi vào logic nghiệp vụ) — ảnh hưởng `loadDetail()`,
`assignMeeting()`, `store()`, `update()`, `approve()`, `reject()`, `cancel()`.

### T114 — 4 chỗ đọc `manager_employee_id` trong `MeetingRoomBookingService.php`

1. `applyVisibilityScope()` (dòng 179 cũ): đổi `$r->where('manager_employee_id', $employeeId)` →
   `$r->whereHas('managers', function ($q) use ($employeeId) { $q->where('employee_id', $employeeId); })`.
   Giữ nguyên 2 vế `orWhere` khác (booked_by, participants) — không gộp/đơn giản hoá, đã tự kiểm lại
   bằng cách đọc lại đúng khối `$query->where(function ($q) ...)` sau khi sửa.
2. Gate `canView()` (dòng 200 cũ): `$room->manager_employee_id && (int) $room->manager_employee_id === $employeeId`
   → `in_array($employeeId, $room->managerIds(), true)`.
3. Gate duyệt `canActOnApprovalByRoom()` (dòng 777 cũ): tương tự, dùng `(int) auth()->id()`.
4. Người nhận thông báo `notifyPendingApproval()` (dòng 1193-1198 cũ): `if (!$room->manager_employee_id) return;`
   rồi gửi `[$room->manager_employee_id]` → đổi thành `$managerIds = $room->managerIds(); if (empty($managerIds)) return;`
   rồi gửi `$managerIds` (toàn bộ). Tham số người gửi (`$sender`, mặc định null trong lời gọi này)
   **giữ nguyên**, không đổi — đúng yêu cầu brief.

Cũng cập nhật 3 dòng COMMENT còn nhắc `manager_employee_id` (dòng 161, 765, 1059 cũ) cho khớp code
thật, để `grep` audit ở mục 3 không còn thấy chỗ nào (kể cả comment) ngoài migration.

### T115 — 2 Resource phiếu

`MeetingRoomBookingResource.php` và `DetailMeetingRoomBookingResource.php`: thay biến `$isRoomManager`
bằng **đúng chữ ký** brief cho:
```php
$isRoomManager = in_array((int) auth()->id(), optional($this->room)->managerIds() ?: [], true);
```
Phòng chưa load → `optional($this->room)->managerIds()` ra `null` → `?: []` chốt mảng rỗng →
`in_array` trên mảng rỗng → `false` (đúng yêu cầu "phòng chưa load thì phải ra false"). Mọi cờ
`is_can_*` giữ nguyên công thức cũ (`isCanEdit() && $isOwner`, `isCanCancel() && (...)` …), chỉ đổi
cách tính `$isRoomManager`.

**Phát sinh thêm (ngoài yêu cầu chữ ký `$isRoomManager`, nhưng cùng file T115 đang sửa)**:
`DetailMeetingRoomBookingResource.php` dòng 46 (nested `'room' => [...]`) còn
`'manager_name' => optional(optional($this->room->manager)->info)->fullname` — đọc quan hệ `manager()`
đã xoá, luôn ra `null` (Eloquent không throw khi đọc property/quan hệ không tồn tại qua magic
`__get`, chỉ trả `null` — đã xác nhận qua đọc code `Model::getRelationValue()`). Đổi sang
`implode(', ', $this->room->managerNames())`. Đã `grep` `hrm-client/pages/meeting` — KHÔNG có chỗ
nào đang đọc khoá `room.manager_name` của endpoint chi tiết phiếu này, nên sửa không ảnh hưởng FE
hiện tại, chỉ tránh để hồi quy im lặng tồn tại vĩnh viễn.

### BS-2 — `BookableMeetingRoomResource.php`: `manager_name` luôn `null`

Đổi field `manager_name` (đọc qua quan hệ `manager()` đã xoá, luôn `null`) → **`manager_name_text`**
(đúng tên trường `MeetingRoomResource`/`DetailMeetingRoomResource` ở lượt A1 đã dùng), giá trị
`implode(', ', $this->managerNames())`. Không trả id thô. Nguồn `managers` đã được eager load sẵn ở
`MeetingRoomService::bookableForCurrentEmployee()` (dòng 133: `->with(['amenities', 'managers', 'company'])`
— A1 đã làm, không cần sửa thêm) nên không phát sinh N+1.

**Ghi lại cho lượt FE sau** (brief yêu cầu, KHÔNG sửa `hrm-client`): `BookingFormModal.vue` còn đọc
`selectedRoomInfo.manager_name` ở 2 chỗ (~dòng 464, ~1925) — field cũ, sẽ ra `undefined` cho tới khi
FE đổi sang `manager_name_text`.

### BS-3 / T116 — Import/Export phòng họp (`MeetingRoomService.php`)

- Thêm hàm mới `resolveManagerIds(string $rawNames, ?string &$error): ?array` — tách theo `;`, trim
  từng phần tử, bỏ phần tử rỗng; rỗng sau khi lọc → lỗi "Phòng phải có ít nhất 1 người phụ trách";
  từng tên gọi lại `resolveManagerId()` (hàm cũ, GIỮ NGUYÊN không sửa) — dừng ở tên ĐẦU TIÊN không
  khớp/trùng nhiều người (tái dùng nguyên câu lỗi cũ, không tự chế kiểu báo lỗi mới).
- `validateRoomRow()`: đổi từ "chỉ validate khi có nhập" (`$managerName !== '' && ...`) sang LUÔN
  validate qua `resolveManagerIds()` (rỗng cũng lỗi).
- `importRows()`: gọi `resolveManagerIds()`, nếu `null` thì `throw` đúng cơ chế lỗi-theo-dòng hiện
  có của file (bắt bởi `catch (\Exception $e)` trong vòng lặp, gán vào `errors[] = ['row' => ..., 'message' => ...]`).
- **BS-3 (lỗi âm thầm thật)**: bỏ `'manager_employee_id' => $managerId` khỏi mảng `MeetingRoom::create([...])`
  (cột đã drop, không còn trong `$fillable`, Eloquent bỏ qua không báo) → thay bằng
  `$room->managers()->sync($managerIds)` NGAY SAU `create()`, đúng khuôn `amenities()->sync()` ngay
  dưới.
- **Export** (`ExportColumnRegistry.php` mapping `'manager_name' => 'Người quản lý'` cho bảng
  `meeting_rooms`, dùng cho nút Xuất Excel danh sách phòng): đây là 1 lỗi CÙNG HỌ với BS-2 mà brief
  không liệt tên file nhưng nằm đúng trong đề bài "Export: ghép ngược danh sách tên bằng `"; "`" —
  A1 đã XOÁ khoá `manager_name` khỏi `MeetingRoomResource` (đổi thành `manager_name_text`, ghép
  bằng `", "`), khiến cột "Người quản lý" của file Excel LUÔN RỖNG (đúng cảnh báo có sẵn ngay trong
  comment của `ExportColumnRegistry.php`: "Khoá PHẢI khớp Resource, lệch là cột ra rỗng mà không có
  lỗi nào báo" — đang xảy ra thật). Đồng thời phát hiện FE `pages/meeting/rooms/index.vue` (cột bảng
  `#cell-manager_name` dòng 151 + payload import dòng 1032) **cũng** đọc đúng khoá `manager_name` này
  — nghĩa là cột "Người quản lý" ở MÀN DANH SÁCH PHÒNG cũng đang rỗng từ sau lượt A1, không chỉ file
  xuất Excel. Xử lý: thêm LẠI khoá `manager_name` vào `MeetingRoomResource.php` (giữ nguyên
  `manager_name_text` cho chỗ khác đang cần), giá trị `implode('; ', $this->managerNames())` — dùng
  `"; "` đúng yêu cầu brief (khác `manager_name_text` dùng `", "`) để 1 file Excel xuất ra RE-IMPORT
  lại được thẳng (khớp dấu `;` mà `resolveManagerIds()` tách). Việc này tình cờ SỬA LUÔN cả 2 chỗ
  (Excel xuất + cột bảng FE), dù chỉ sửa 1 khoá dữ liệu ở BE — không đụng file `hrm-client` nào.
- `BuildsImportTemplate.php` (trait dựng file mẫu): đọc code thật — file này là trait THUẦN, không
  có nội dung riêng cho từng danh mục (chữ tiêu đề cột nằm ở `MeetingRoomController::importTemplate()`,
  không phải trait). Đây là **chỗ lệch giữa brief và code thật** (brief ghi "sửa
  `BuildsImportTemplate.php` + file mẫu import" — không tồn tại nội dung ManagerName trong file đó):
  đã cập nhật đúng chỗ thật — tiêu đề cột E ở `MeetingRoomController::importTemplate()`:
  `'Người quản lý (tên nhân viên)'` → `'Người quản lý (tên nhân viên, bắt buộc >= 1, nhiều người ngăn bởi dấu ;) *'`.
  Không sửa `BuildsImportTemplate.php`.
- **Test mới cho BS-3** (nằm trong `tests/Feature/MeetingRoomManagersTest.php` — xem mục 3, brief
  yêu cầu 4 ca cho T114-T117 KHÔNG có ca riêng cho import; ca import round-trip qua
  `resolveManagerIds()`/`sync()` đã được kiểm TAY qua tinker thay vì viết thêm ca PHPUnit riêng, vì
  4 ca bắt buộc theo brief đã chiếm đủ "Cách tự kiểm #3" — xem mục "Điểm nghi ngờ" bên dưới về việc
  này).

### T117 — `app/Services/CatalogHistoryService.php` + `MeetingRoomService.php` (roomSnapshot)

Đọc `MeetingRoomService::catalogDisplay()` trước theo đúng chỉ dẫn brief: xác nhận khoá
`manager_employee_id` không còn được `catalogColumns()`/`catalogDisplay()` xử lý (A1 đã bỏ ở T111),
và A1 đã để lại bàn giao rõ ràng trong docblock: nhóm phụ trách (nhiều người) CHƯA vào lịch sử, cần
khoá ảo kiểu `amenities` ở `roomSnapshot()` + đăng ký nhãn ở `CatalogHistoryService::TABLES`.

- `CatalogHistoryService.php`: đổi khoá `'manager_employee_id' => 'Người quản lý phòng'` →
  `'managers' => 'Người quản lý phòng'` trong `TABLES['meeting_rooms']['columns']`. Nhãn giữ nguyên
  đúng yêu cầu.
- `MeetingRoomService::roomSnapshot()`: thêm khoá ảo `managers`, **KHÔNG dùng**
  `$room->managerNames()` (đệm cache + dựa vào `relationLoaded('managers')` của model — gọi lần 2
  SAU KHI `sync()` đã đổi pivot vẫn trả kết quả CŨ, vì quan hệ coi như "đã nạp" từ lần snapshot
  TRƯỚC). Đây là bẫy tôi tự phát hiện khi đọc kỹ cách `managerNames()`/`loadedManagers()` hoạt động
  (A1 bàn giao) — nếu dùng sai sẽ khiến BEFORE/AFTER snapshot LUÔN giống nhau, lịch sử không bao giờ
  ghi nhận đổi nhóm phụ trách dù dữ liệu đã đổi thật. Sửa bằng cách gọi THẲNG
  `$room->managers()->orderBy('employees.id')->get()->pluck('fullname')->implode(', ')` (query MỚI
  mỗi lần gọi, không qua cache nào) — đúng khuôn `amenities` đang làm ngay phía trên (order theo id
  của bảng LIÊN QUAN để 2 lần chụp cùng dữ liệu luôn ra cùng chuỗi, không lệch do thứ tự `sync()`).
  Hiển thị **danh sách TÊN** ngăn `, `, KHÔNG in ra id trần — đúng yêu cầu brief.
- Cập nhật 2 docblock liên quan (`catalogColumns()`, `catalogDisplay()`) từ "CHƯA làm, bàn giao lượt
  sau" sang "đã làm, xem `roomSnapshot()`".

---

## 2. Số đo thật của 4 mục tự kiểm (mục "Cách tự kiểm" của brief)

### 2.1. `grep -rn "manager_employee_id" Modules app`

Chạy SAU khi sửa xong toàn bộ:
```
grep -rn "manager_employee_id\b" Modules app | grep -v "Database/Migrations" | grep -vE "^\s*//|^\s*\*|manager_employee_ids"
```
Kết quả: **8 dòng**, TẤT CẢ đều là comment giải thích lịch sử (đã đọc thủ công từng dòng để xác
nhận, không phải code thật đọc cột):
- `MeetingRoomService.php` dòng 687, 689, 728, 1087 — comment giải thích T111/BS-3.
- `DetailMeetingRoomBookingResource.php` dòng 33 — comment mô tả field cũ trước khi đổi.
- `MeetingRoomResource.php` dòng 35 — comment mô tả field cũ (của A1, giữ nguyên).
- `MeetingRoom.php` dòng 85 — comment mô tả quan hệ CŨ đã xoá (của A1).
- `Routes/api.php` dòng 113 — comment mô tả spec (của A1, không đổi vì không phải phạm vi).
- `CatalogHistoryService.php` dòng 448 — comment giải thích T117.

Ngoài migration + comment: **KHÔNG còn chỗ nào đọc cột đã drop**. `manager_employee_ids` (số nhiều,
field Request/khoá ảo hợp lệ của T112/A1, KHÔNG phải cột đã drop) xuất hiện ở
`MeetingRoomRequest.php`, `MeetingRoomResource.php`, `DetailMeetingRoomResource.php`,
`MeetingRoomService.php` — đúng như thiết kế, không phải sót.

Đã kiểm thêm (ngoài yêu cầu grep của brief) bằng regex rộng hơn cho cả `->manager` (không hậu tố
`_id`/`s`) trên toàn `Modules`/`app` — chỉ còn 2 dòng ở `app/Transformers/Fractal/CustomScope.php`
(`$this->manager->getSerializer()`), không liên quan Meeting, là API của thư viện Fractal.

### 2.2. PHPUnit `--filter MeetingRoom` — mốc TRƯỚC và SAU

**Trước khi sửa (chạy lại đúng baseline, xác nhận khớp số brief đưa)**:
```
Tests: 46, Assertions: 79, Errors: 5, Failures: 2.
```
5 Errors: `MeetingRoomBookingRaceTest` — `SQLSTATE[42S22]: Column not found: 1054 Unknown column
'code' in 'field list'` khi insert `meeting_rooms`. **Đã xác minh gốc rễ**: cột `code` của
`meeting_rooms` bị DROP THẬT ở migration `2026_09_19_000002_drop_code_add_note_meeting_room_catalogs.php`
(Task 44, có trước cả Phase 8) — test đó tự chèn `code` là code test CŨ chưa cập nhật theo schema
mới, không liên quan gì tới việc DROP `manager_employee_id` của A1/A2. 2 Failures:
`MeetingRoomBookingSyncRuleTest` — thiếu `mode_id` trong `ROOM_FIELDS`, cũng không liên quan.

**Sau khi sửa xong T114-T117 + BS-1/2/3 (chưa tính test mới)**:
```
Tests: 46, Assertions: 79, Errors: 5, Failures: 2.
```
Giống hệt baseline — không có ca nào đang xanh bị đỏ.

**Sau khi thêm `tests/Feature/MeetingRoomManagersTest.php` (4 ca mới), chạy lại `--filter MeetingRoom`
toàn bộ**:
```
Tests: 50, Assertions: 92, Errors: 5, Failures: 2.
```
Đúng bằng baseline + 4 test mới (46+4=50 tests, 79+13=92 assertions), 5 Errors/2 Failures GIỮ
NGUYÊN — không làm đỏ thêm ca nào.

### 2.3. Test mới `tests/Feature/MeetingRoomManagersTest.php`

Đặt ở `tests/Feature/` (KHÔNG phải `Modules/Meeting/Tests/Feature/`) — đã kiểm cấu trúc trước khi
viết: `Modules/Meeting/Tests/{Unit,Feature}/` chỉ có 2 file `.gitkeep`, KHÔNG được khai trong
`phpunit.xml` (`<testsuite>` chỉ scan `./tests/Unit` và `./tests/Feature`), nên đặt test ở đó sẽ
KHÔNG BAO GIỜ được `phpunit` chạy — toàn bộ 5 file test `MeetingRoom*` hiện có của module đều nằm ở
`tests/Unit`/`tests/Feature` gốc repo, đây mới là "thư mục test thật" theo đúng chỉ dẫn brief.

4 ca (mỗi ca đúng 1 điều bắt buộc), chạy riêng:
```
$ vendor/bin/phpunit tests/Feature/MeetingRoomManagersTest.php
OK (4 tests, 13 assertions)
```

- `test_ca_hai_nguoi_phu_trach_deu_duyet_duoc_phieu` — phòng test có 2 quản lý (employee 24, 25),
  2 phiếu RIÊNG (giờ khác nhau, không đè lịch), mỗi người `approve()` 1 phiếu, assert cả 2 phiếu ra
  `STATUS_DA_DUYET`.
- `test_nguoi_ngoai_nhom_phu_trach_bi_chan_khi_duyet` — employee 28 (không phải quản lý, không có
  quyền "Duyệt phiếu đặt phòng họp") gọi `approve()` → assert bắt được `Exception` mã `403`, và
  phiếu VẪN "Chờ duyệt" (không lọt duyệt).
- `test_apply_visibility_scope_tra_phieu_cho_ca_hai_nguoi_phu_trach` — phiếu đặt bởi employee 27
  (KHÔNG phải quản lý, để phép đo chỉ phản ánh đúng vế "phòng mình quản lý"), gọi
  `MeetingRoomBookingService::index()` (nơi `applyVisibilityScope()` được áp) với `actingAs` lần
  lượt 24 → 25 → 28: 2 người quản lý đều thấy phiếu trong kết quả, người ngoài (28) KHÔNG thấy.
- `test_thong_bao_cho_duyet_ban_cho_du_hai_nguoi_phu_trach` — `Notification::fake()` +
  `notifyPendingApproval()`, assert `Notification::assertSentTimes(BaseNotification::class, 2)` +
  `assertSentTo([$recipientA, $recipientB], ...)` — chỉ đếm SỐ người nhận + ĐÚNG người, không assert
  nội dung, đúng yêu cầu brief.

**Actor dùng trong test — đã kiểm bằng tinker TRƯỚC khi viết** (tránh bẫy chọn nhầm nhân viên có sẵn
quyền che lấp lỗi): employee 13 và 34 (2 mã hay dùng nhất trong bộ test cũ của module) đều CÓ SẴN cả
2 quyền "Xem tất cả phiếu đặt phòng họp" và "Duyệt phiếu đặt phòng họp" theo role hiện tại của DB
local — dùng làm "người ngoài nhóm" sẽ xanh giả (đi qua nhánh quyền thay vì nhánh đang kiểm). Đã dò
thủ công (không qua `auth()`/guard, join thẳng `role_has_permissions` theo đúng logic
`isCurrentEmployeeHasPermission()`) và chọn ra 24, 25 (không quyền, dùng làm 2 quản lý), 27 (không
quyền, không quản lý, dùng làm người đặt), 28 (không quyền, không quản lý, không đặt, dùng làm
"người ngoài") — toàn bộ cùng `company_id = 1`, cùng trạng thái `active`.

**Ca nào chưa "đỏ được" trước khi sửa**: không áp dụng theo nghĩa TDD cổ điển (brief không yêu cầu
viết trước rồi thấy đỏ) — nhưng đã tự kiểm bằng cách tạm inline lại code CŨ (đọc
`$room->manager_employee_id`, giờ cột không còn tồn tại) để xác nhận nếu A2 chưa sửa thì 3/4 ca đầu
sẽ ném `Illuminate\Database\QueryException` (cột không tồn tại — vì `MeetingRoom` entity vẫn có thể
bị truy vấn cột lạ nếu ai đó thêm lại field vào `$fillable`)/hoặc `managerIds()` không tồn tại lúc
A1 chưa chạy — không thực hiện đối chứng âm đầy đủ (revert code thật) vì rủi ro làm vỡ trạng thái
đang sửa dở của nhánh chung; tự tin vào tính đúng đắn qua việc code MỚI gọi đúng
`managerIds()`/`whereHas('managers', ...)` đã được A1 lập tài liệu chữ ký rõ ràng và đã tự kiểm tay
ở mục 2.4 dưới trên DATA THẬT.

### 2.4. Kiểm tay trên DB local (2 phòng, 3 phiếu) — qua tinker

- Trước: `meeting_room_managers` cho phòng thật `id=1618` chỉ có 1 dòng (`employee_id=13`), phòng có
  2 phiếu (`id=2280`, `id=2390`, cùng đã "Đã duyệt").
- Thêm SQL trực tiếp: `employee_id=24` làm quản lý THỨ HAI của phòng `1618`.
- `actingAs` employee 24 (qua `Auth::guard('api')->onceUsingId(24)`), gọi
  `MeetingRoomBookingService::index()` lọc `meeting_room_id=1618` → kết quả trả **đúng cả 2** phiếu
  `[2390, 2280]` — xác nhận `applyVisibilityScope()` hoạt động đúng trên DATA THẬT, không chỉ trên
  dữ liệu test tự dựng.
- Xoá dòng vừa thêm (`DELETE ... WHERE meeting_room_id=1618 AND employee_id=24`). Xác nhận lại:
  `meeting_room_managers` về đúng **2 dòng** (baseline gốc), phòng `1618` chỉ còn quản lý `employee_id=13`.
- DB local sau khi dọn: **2 phòng, 3 phiếu, 2 dòng `meeting_room_managers`** — đúng baseline ban đầu.

---

## 3. Danh sách file đã sửa/tạo

**Sửa** (theo đúng 4 nhóm + phần mở rộng nội-nhóm đã giải trình ở mục 1):
1. `Modules/Meeting/Services/MeetingRoomBookingService.php` — BS-1 (7 chỗ eager load) + T114 (4 chỗ
   logic) + 3 comment.
2. `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` — T115.
3. `Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php` — T115 +
   sửa thêm `room.manager_name` (dòng 46 cũ) cùng lý do BS-2.
4. `Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php` — BS-2.
5. `Modules/Meeting/Services/MeetingRoomService.php` — BS-3/T116 (`resolveManagerIds()` mới,
   `validateRoomRow()`, `importRows()`) + T117 (`roomSnapshot()`, 2 docblock).
6. `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php` — deviation phát sinh từ
   T116 "Export": khôi phục khoá `manager_name` (ghép `; `) để không rỗng ở file Excel xuất + cột
   bảng FE `pages/meeting/rooms/index.vue` (xem mục 1, BS-3/T116).
7. `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php` — 1 dòng tiêu đề cột
   `ManagerName` của `importTemplate()` (chỗ lệch brief vs code thật, xem mục 1 T116).
8. `app/Services/CatalogHistoryService.php` — T117.

**Tạo mới**:
9. `tests/Feature/MeetingRoomManagersTest.php` — 4 ca theo mục "Cách tự kiểm" #3.

Không đụng file nào ngoài danh sách trên. Không đụng `hrm-client`. Không `git commit`/`push`/`stash`.

---

## 4. Chỗ brief mơ hồ / lệch code thật — đã tự chọn hiểu thế nào

1. **T117 chỉ nêu `CatalogHistoryService.php` nhưng việc thật cần sửa CẢ `MeetingRoomService.php`
   (`roomSnapshot()`)** — brief viết "Chỗ này đang đổi giá trị thô sang chữ... Đổi sang khoá mới...".
   Đọc code thật: `catalogDisplay()` (nơi đổi giá trị thô sang chữ) không map khoá `managers` được
   (nó là quan hệ, không phải cột — giống hệt lý do `amenities` cũng không đi qua hàm này). Nhóm phụ
   trách phải vào lịch sử qua khoá ẢO ở `roomSnapshot()`, đúng như chính A1 đã bàn giao rõ trong
   docblock. Tôi sửa cả 2 file (`CatalogHistoryService.php` cho nhãn hiển thị + `MeetingRoomService.php`
   cho giá trị/khoá ảo) vì thiếu 1 trong 2 thì tính năng không hoạt động — nhãn không khớp giá trị.

2. **T116 "Export: ghép ngược... bằng `; `" không nêu tên file, nhưng việc thật nằm ở
   `MeetingRoomResource.php` (đã sửa ở A1) + gián tiếp `app/ExcelExport/ExportColumnRegistry.php`
   (KHÔNG sửa file này, chỉ khôi phục khoá cho khớp)** — xem giải trình đầy đủ ở mục 1. Quyết định:
   phục hồi khoá `manager_name` ở `MeetingRoomResource.php` (thay vì sửa `ExportColumnRegistry.php`
   đổi khoá tra cứu) để tận dụng đúng cơ chế sẵn có (`DynamicExport` đọc theo khoá của Resource) và
   không phải đụng thêm 1 file ngoài phạm vi Meeting.

3. **T116 "`BuildsImportTemplate.php` + file mẫu import"** — code thật: `BuildsImportTemplate.php`
   là trait DÙNG CHUNG, không có nội dung `ManagerName`. Nội dung tiêu đề cột nằm ở
   `MeetingRoomController::importTemplate()`. Đã sửa đúng chỗ thật, không đụng trait.

4. **Brief đưa ví dụ `manager_employee_ids hoặc tên trường thực tế` cho khoá lịch sử (T117)** — chọn
   `managers` (không phải `manager_employee_ids`, vốn là tên field REQUEST của form Sửa phòng, khác
   ngữ cảnh) để nhất quán với khuôn khoá ảo `amenities` đã có sẵn trong `roomSnapshot()`.

---

## 5. Điểm nghi ngờ khác / bàn giao

- **Import tạo phòng (`importRows()`) ghi lịch sử "Tạo mới" qua `logCatalogCreate($room)` (hàm của
  trait, dùng `catalogSnapshot()` — KHÔNG dùng `roomSnapshot()`)** → log "Tạo mới" của phòng import
  từ Excel sẽ THIẾU cả `amenities` LẪN `managers` trong snapshot đầy đủ. Đây là hành vi **CÓ SẴN TỪ
  TRƯỚC** (không phải do tôi/A1 gây ra — `amenities` cũng đã thiếu kiểu này trước Phase 8), không
  thuộc phạm vi T116/T117 của lượt này (T116 chỉ yêu cầu sửa parsing + tạo phòng, T117 chỉ yêu cầu
  đổi khoá lịch sử của luồng `updateOrCreate()` màn nhập tay) — nêu ra để lượt sau cân nhắc đổi
  `importRows()` sang gọi `app(CatalogHistoryService::class)->log(..., $this->roomSnapshot($room))`
  thay `logCatalogCreate()` nếu muốn lịch sử phòng import đầy đủ như tạo tay.
- **Không viết thêm 1 ca PHPUnit riêng cho BS-3 (import 2 tên → 2 dòng `meeting_room_managers`)** —
  đã đọc kỹ logic `resolveManagerIds()`/`importRows()` mới viết và tự tin đúng theo cùng pattern đã
  test qua `managers()->sync()` ở 4 ca chính; đã kiểm bằng `php -l` (cú pháp sạch) + đọc lại toàn bộ
  đường đi. Đây là thiếu sót SO VỚI brief BS-3 (yêu cầu rõ "thêm 1 ca test import chứng minh: file 1
  dòng có 2 tên ngăn bằng `;` → tạo ra đúng 2 dòng `meeting_room_managers`") — TỰ NHẬN đây là việc
  CHƯA làm đủ, không phải quên mà là đánh đổi thời gian cho 4 ca bắt buộc của mục "Cách tự kiểm" #3.
  Nếu reviewer yêu cầu, việc bổ sung khá nhỏ: gọi `MeetingRoomService::importRows([[...['manager_name' => 'Tên A; Tên B']...]])`
  trực tiếp (không qua HTTP) rồi assert `DB::table('meeting_room_managers')->where('meeting_room_id', $newRoomId)->count() === 2`.
- **`Employee::exists` rule ở `MeetingRoomRequest.php` (T112, việc của A1) dùng bảng `employees`** —
  đã xác nhận lại `resolveManagerId()`/`resolveManagerIds()` (T116, việc của tôi) CŨNG dùng
  `\Modules\Human\Entities\Employee` (khác namespace với `\Modules\Timesheet\Entities\Employee` mà
  `MeetingRoom::managers()` quan hệ tới) nhưng CÙNG trỏ bảng `employees` — đã kiểm bằng
  `Schema::hasColumn`/đọc `$table` property, không có xung đột id vì cùng 1 bảng vật lý, 2 class chỉ
  khác accessor `fullname` (đã ghi trong báo cáo A1 mục 5.3) — `resolveManagerId()` chỉ dùng
  `->pluck('id')`, không đụng accessor `fullname`, nên không bị ảnh hưởng bởi khác biệt đó.
- **Cấm N+1**: đã rà lại toàn bộ chỗ sửa — `roomSnapshot()` gọi `$room->managers()->get()` 2 lần cho
  1 phòng (BEFORE/AFTER, cố ý KHÔNG cache vì lý do đã giải trình ở mục 1/T117), nhưng đây là 2 query
  nhỏ cho ĐÚNG 1 bản ghi phòng trong 1 lần lưu, không lặp qua danh sách nhiều phòng/phiếu → không
  phải N+1 theo nghĩa "N tăng theo số dòng danh sách". `resolveManagerIds()` gọi `resolveManagerId()`
  (1 query/tên) trong vòng lặp theo SỐ NGƯỜI PHỤ TRÁCH của 1 dòng Excel (thường 1-3 người), không
  lặp theo số DÒNG import — chấp nhận được, cùng bậc chi phí với `resolveAmenityIds()` đã có sẵn từ
  trước theo đúng pattern của file.

---

**Kết luận**: DONE. Không còn chỗ nào đọc quan hệ `manager()`/cột `manager_employee_id` đã drop
ngoài migration + comment lịch sử. PHPUnit `--filter MeetingRoom`: 46→50 test (thêm 4, tất cả xanh),
79→92 assertion, 5 Error/2 Failure GIỮ NGUYÊN (pre-existing, không liên quan Phase 8). Kiểm tay trên
DB thật (2 phòng, 3 phiếu) xác nhận đúng, đã dọn sạch dữ liệu test.

---

## Fix vòng 1 (coordinator yêu cầu — 4 việc nhỏ)

Trạng thái: **DONE**. Cả 4 việc đã làm, không đụng file ngoài phạm vi, không đụng `hrm-client`,
không commit/push/stash.

### 1. Chuẩn hoá khoá tên người phụ trách — theo đúng quyết định đã chốt

- **`Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php`**: bỏ `manager_name_text`,
  giữ `manager_employee_ids` + `manager_names` + `manager_name` (ghép `"; "`).
- **`Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php`**: y hệt trên (trước đó
  file này CHỈ có `manager_name_text`, chưa từng có `manager_name` — đã thêm mới đúng công thức
  `implode('; ', $this->managerNames())`).
- **`Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php`**: đổi khoá
  `manager_name_text` → `manager_name` (giữ nguyên `"; "`, giữ nguyên chủ ý cũ "không trả id thô").
  **Lợi ích phụ phát sinh**: FE `BookingFormModal.vue` (~dòng 464, ~1925) đang đọc đúng
  `selectedRoomInfo.manager_name` — đổi tên khoá này khớp LẠI với field FE đang đọc, nên điểm nghi
  ngờ "FE đọc field cũ" đã ghi ở báo cáo gốc (mục BS-2) **coi như đã tự hết** cho đúng đường
  `BookableMeetingRoomResource`, không cần đợi lượt FE nữa (2 chỗ dùng `manager_name` cho form/panel
  chọn phòng của popup đặt phòng). Vẫn CHƯA đụng file `hrm-client` nào — chỉ là hệ quả tự nhiên của
  việc BE trả đúng khoá cũ trở lại.

Tự kiểm bắt buộc:
```
$ grep -rn "manager_name_text" Modules app
(rỗng — 2 dòng comment còn sót có nhắc chữ này ban đầu đã được viết lại để không còn chứa chuỗi đó,
xác nhận lại bằng đúng lệnh trên, exit code 1 = không khớp dòng nào)
```

### 2. Ca test import còn thiếu (BS-3) — đã viết đủ 2 ca

Thêm vào `tests/Feature/MeetingRoomManagersTest.php`:

- `test_import_phong_hop_hai_ten_ngan_boi_cham_phay_tao_dung_hai_dong_quan_ly()` — gọi thẳng
  `MeetingRoomService::importRows()` (không qua HTTP) với 1 dòng `manager_name` =
  `"Nguyễn Đức Tuân; Nguyễn Thị Cần"` (tên THẬT của employee 24/25, khớp cách `resolveManagerId()`
  tra theo `fullname`) → assert `result['success'] === 1`, rồi assert
  `meeting_room_managers` của phòng vừa tạo có ĐÚNG 2 dòng, đúng 2 id `[24, 25]`.
- `test_import_phong_hop_thieu_nguoi_phu_trach_bao_loi_dong_khong_tao_phong()` — 1 dòng
  `manager_name` rỗng → assert `result['failed'] === 1`, đúng `row = 2`, message chứa "người phụ
  trách", VÀ **assert không có phòng nào được tạo ra** (`MeetingRoom::where('name', ...)->first()`
  phải `null`) — đây chính là bẫy Eloquent từng ÂM THẦM BỎ QUA `manager_employee_id` lạ mà KHÔNG tạo
  phòng-không-ai-quản-lý nữa, chốt bằng test thay vì chỉ đọc code.

Cả 2 ca gọi `actingAs(employee 27)` trước khi `importRows()` (cần `auth()` để `BaseModel::creating()`
tự điền `company_id` + để hàm dedupe theo tên phòng trong công ty hoạt động đúng). Dọn dẹp: thêm
`catalog_histories` (bảng `table_name='meeting_rooms'`) vào `tearDown()` vì `importRows()` gọi
`logCatalogCreate()` thật, ghi 1 dòng lịch sử cho phòng vừa tạo — nếu không dọn sẽ để rác vĩnh viễn.

### 3. Bẫy cache ở `MeetingRoom.php` — đã vá bằng hàm `syncManagers()`

Không sửa `managerIds()`/`managerNames()` để tự "đoán" khi nào cache hết hạn (Eloquent không có hook
để 2 hàm này tự biết pivot vừa bị `sync()` ở nơi khác) — thay vào đó **thêm 1 hàm mới**
`MeetingRoom::syncManagers(array $employeeIds): array` là ĐƯỜNG DUY NHẤT được phép gọi để đồng bộ
người phụ trách:
```php
public function syncManagers(array $employeeIds): array
{
    $result = $this->managers()->sync($employeeIds);
    $this->unsetRelation('managers');   // xoá quan hệ đã nạp trên chính model
    $this->managerIdsCache = null;      // xoá cache riêng của managerIds()
    $this->managerNamesCache = null;    // xoá cache riêng của managerNames()
    return $result;
}
```
Đổi cả 2 chỗ đang gọi thẳng `$room->managers()->sync($ids)` (2 chỗ DUY NHẤT trong toàn repo, đã
`grep` xác nhận trước khi sửa) sang gọi `$room->syncManagers($ids)`:
`MeetingRoomService::updateOrCreate()` (dòng ~839 cũ) và `MeetingRoomService::importRows()` (dòng
~1092 cũ). Đã ghi rõ trong docblock của `syncManagers()`: bất kỳ chỗ nào TỰ VIẾT LẠI
`$room->managers()->sync(...)` ở service khác trong tương lai sẽ KHÔNG được vá — quy ước là bắt buộc
đi qua hàm này.

**Ca test chứng minh** (`test_managerIds_khong_con_stale_cache_sau_khi_syncManagers()`): tạo phòng 2
người phụ trách (24, 25) → đọc `managerIds()` (mồi cache) + `managerNames()` (mồi luôn quan hệ đã
nạp) → gọi `syncManagers([30])` → đọc lại `managerIds()` TRÊN CÙNG OBJECT → assert ra đúng `[30]`
(không phải `[24, 25]` cũ).

**Đối chứng âm đã tự làm** (bắt buộc theo tinh thần dự án — "lỗi phải tái hiện được trước khi sửa"):
tạm xoá 3 dòng xoá cache trong `syncManagers()`, chạy riêng ca test trên:
```
$ vendor/bin/phpunit --filter test_managerIds_khong_con_stale_cache_sau_khi_syncManagers tests/Feature/MeetingRoomManagersTest.php
FAILURES!
Tests: 1, Assertions: 2, Failures: 1.
--- Expected
+++ Actual
@@ @@
 Array &0 (
-    0 => 30
+    0 => 24
+    1 => 25
 )
```
Đúng bẫy mô tả — cache stale ra `[24, 25]` cũ thay vì `[30]` mới. Khôi phục lại 3 dòng xoá cache,
chạy lại: **xanh**.

### 4. `managers()` thêm `orderBy` tường minh

`Modules/Meeting/Entities/MeetingRoom.php::managers()`: thêm `->orderBy('meeting_room_managers.id')`
ngay trong định nghĩa quan hệ (áp dụng cho MỌI nơi gọi `$room->managers()`, không chỉ 2 hàm
`managerIds()`/`managerNames()`). Cập nhật lại docblock của `managerNames()` (trước đây khẳng định
"đi theo thứ tự khoá pivot" như một mặc định của MySQL — SAI, MySQL không đảm bảo thứ tự khi thiếu
`ORDER BY`) để không còn dựa vào "may rủi".

Ảnh hưởng phụ (không phải lỗi, ghi lại để minh bạch): `MeetingRoomService::roomSnapshot()` tự thêm
`->orderBy('employees.id')` NGAY TRÊN query `$room->managers()` cho khoá ảo lịch sử — nay query đó
có 2 `ORDER BY` (pivot id trước, employees.id sau), pivot id thắng vì đứng trước. Không sửa gì thêm
ở `roomSnapshot()` vì kết quả vẫn ĐÚNG YÊU CẦU (tất định, cùng dữ liệu ra cùng chuỗi mọi lần gọi) —
chỉ đổi tiêu chí sắp xếp từ "theo id nhân viên" sang "theo thứ tự pivot", không ảnh hưởng tính đúng
đắn của diff BEFORE/AFTER.

### Kết quả test sau fix vòng 1

Lệnh đã chạy:
```
$ vendor/bin/phpunit tests/Feature/MeetingRoomManagersTest.php
OK (7 tests, 26 assertions)

$ vendor/bin/phpunit --filter MeetingRoom
Tests: 53, Assertions: 105, Errors: 5, Failures: 2.
```
So với mốc trước fix vòng 1 (50 test / 92 assertion / 5 Error / 2 Failure): **+3 test, +13
assertion, Error/Failure GIỮ NGUYÊN** (vẫn đúng 5 Error/2 Failure pre-existing đã giải trình ở báo
cáo gốc, không liên quan Phase 8) — **không đỏ thêm ca nào**.

Kiểm DB sau khi chạy toàn bộ:
```
rooms=2 bookings=3 managers=2 catalog_hist_leftover=0
```
Đúng baseline gốc (2 phòng, 3 phiếu, 2 dòng `meeting_room_managers`), không còn rác `catalog_histories`
của các ca import mới.

### File sửa thêm ở fix vòng 1 (ngoài danh sách gốc)

- `Modules/Meeting/Entities/MeetingRoom.php` — thêm `syncManagers()`, thêm `orderBy` ở `managers()`,
  cập nhật 2 docblock.
- `Modules/Meeting/Services/MeetingRoomService.php` — đổi 2 chỗ gọi `sync()` sang `syncManagers()`.
- `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php`,
  `DetailMeetingRoomResource.php`, `BookableMeetingRoomResource.php` — chuẩn hoá khoá (mục 1).
- `tests/Feature/MeetingRoomManagersTest.php` — thêm 3 ca test (2 ca import + 1 ca cache), thêm dọn
  `catalog_histories` vào `tearDown()`.

Không phát sinh file mới ngoài các file đã liệt kê ở báo cáo gốc.

---

## Fix vòng 2 (coordinator yêu cầu — vá 1 lỗi N+1 thật do Phase 8 gây ra)

Trạng thái: **DONE**. Đúng theo yêu cầu phối hợp, **chỉ sửa 2 file**:
`Modules/Meeting/Services/MeetingRoomBookingService.php` và
`Modules/Meeting/Services/MeetingRoomService.php`. Trước khi sửa đã `git status` để xác nhận có agent
khác đang chạy song song (tạo danh mục "Dịch vụ phòng họp" + sửa `Routes/api.php` +
`CatalogHistoryService.php` + `MeetingDatabaseSeeder.php`) — không đụng tới bất kỳ file nào của họ,
và đọc lại đúng nội dung hiện tại của 2 file mục tiêu trước khi chèn (không có xung đột dòng, 2 vị
trí sửa của tôi không giao với vùng agent kia đang động vào).

### Vấn đề (xác nhận đúng như coordinator mô tả)

BS-1 (fix vòng trước) chỉ sửa 7 chỗ `->load([...])` của luồng **1 phiếu đơn** (detail/store/update/
approve/reject/cancel/assignMeeting). 4 luồng trả **DANH SÁCH phiếu** vẫn chỉ `->with('room')`,
thiếu `room.managers`, trong khi `MeetingRoomBookingResource`/`DetailMeetingRoomBookingResource`
tính `$isRoomManager` bằng `optional($this->room)->managerIds()` cho TỪNG DÒNG khi resolve Resource.

### 4 chỗ đã sửa

1. `MeetingRoomBookingService::index()` (dòng 97 cũ) — nuôi màn danh sách phiếu + export.
2. `MeetingRoomService::board()` (dòng 542 cũ) — lưới Phòng × Giờ.
3. `MeetingRoomService::week()` (dòng 576 cũ) — lịch tuần 1 phòng.
4. `MeetingRoomService::statusBoard()` (dòng 622 cũ) — `current_booking`/`next_booking` mỗi phòng.

Cả 4 chỗ đổi `->with('room')` (hoặc `['room', ...]`) → `->with('room.managers')` (hoặc
`['room.managers', ...]`). Không thêm `.info`: `MeetingRoom::managers()` đã tự `->with('info')` ngay
trong định nghĩa quan hệ (từ lượt A1). Đã `grep` lại sau khi sửa — không còn chỗ nào trong 2 file này
gọi `with('room')`/`with(['room', ...])` trần (thiếu `.managers`).

### Đo bằng số — TRƯỚC và SAU khi sửa

**Cách đo**: tạm revert 4 chỗ trên về `with('room')` (bản TRƯỚC fix), chạy script đo, khôi phục lại
bản ĐÚNG (bản SAU fix), chạy lại script đo — cùng 1 kịch bản seed/dọn, chỉ khác code đang chạy. Script
tự seed dữ liệu, đo bằng `DB::enableQueryLog()`, rồi XOÁ SẠCH ngay sau mỗi cấu hình (kể cả khi lỗi
giữa chừng, bọc `try/finally`) — không để lại rác.

**Phát hiện quan trọng trước khi chốt số liệu** (đã tự kiểm bằng tinker riêng): 2 lỗi ban đầu trong
cách đo, đã sửa trước khi lấy số cuối:
1. **Đo lần đầu gọi thẳng Service, KHÔNG bọc `MeetingRoomBookingResource::collection(...)->resolve()`**
   — N+1 nằm TRONG `toArray()` của Resource, gọi thẳng Service (trả về Eloquent Collection/Builder,
   không transform) thì N+1 KHÔNG BAO GIỜ kích hoạt dù có/không sửa. Sửa: đo qua đúng combo Service +
   Resource, giống hệt Controller thật đang làm.
2. **Eloquent `BelongsTo::match()` dùng dictionary theo khoá ngoại** — nhiều phiếu CÙNG 1 phòng dùng
   CHUNG 1 PHP OBJECT `room` (đã xác nhận bằng `spl_object_id()`: 2 phiếu cùng `meeting_room_id` trả
   về CÙNG object). Nghĩa là chi phí N+1 tỉ lệ với **SỐ PHÒNG KHÁC NHAU** xuất hiện trong trang, KHÔNG
   PHẢI tổng số dòng phiếu nếu nhiều phiếu dùng lại cùng phòng (dòng sau dùng lại cache đã "mồi" trên
   object phòng dùng chung). Vì vậy đo theo **2 cấu hình** để thấy đủ cả 2 khía cạnh:
   - **Cấu hình A**: 3 phòng × 5 phiếu/phòng = 15 phiếu, **3 phòng khác nhau** (đúng gợi ý "2-3
     phòng" của coordinator).
   - **Cấu hình B**: 15 phòng × 1 phiếu/phòng = 15 phiếu, **15 phòng khác nhau** (mô phỏng trang
     danh sách thật liệt kê phiếu của nhiều phòng khác nhau — kịch bản N+1 THẬT SỰ tăng theo số dòng).

Mỗi phòng test đều có **2 người phụ trách** (đúng yêu cầu "mỗi phòng ≥ 2 người phụ trách"), actor đo
= employee 13 (đã có quyền "Xem tất cả phiếu đặt phòng họp" nên `applyVisibilityScope()` không thêm
điều kiện lọc, cô lập đúng biến đang đo).

**Số liệu thật** (lệnh: `php n1_measure.php`, script viết riêng cho lần đo này, đã xoá sau khi dùng
xong — không còn trong repo):

| Cấu hình | Luồng | TRƯỚC fix | SAU fix | Chênh lệch |
|---|---|---|---|---|
| A (3 phòng, 15 phiếu) | `index()` | 25 query | 17 query | **-8** |
| A (3 phòng, 15 phiếu) | `board()` | 13 query | 9 query | **-4** |
| B (15 phòng, 15 phiếu) | `index()` | 43 query | 11 query | **-32** |
| B (15 phòng, 15 phiếu) | `board()` | 36 query | 8 query | **-28** |

**Đọc số liệu**: TRƯỚC khi sửa, chênh lệch giữa cấu hình A và B (tăng từ 3 lên 15 phòng khác nhau,
gấp 5 lần) khiến số query TRƯỚC-fix tăng vọt (`index()`: 25→43, `board()`: 13→36) — đúng như mô tả
"tăng theo số dòng" KHI mỗi dòng là 1 phòng mới (kịch bản thực tế của 1 trang danh sách phiếu trải
trên nhiều phòng khác nhau). SAU khi sửa, số query ở cả 2 cấu hình đều THẤP và ỔN ĐỊNH quanh mức
8-17 — không còn phụ thuộc số phòng khác nhau trong trang (thậm chí cấu hình B ít hơn A đôi chút do
các yếu tố khác không liên quan `managers`, không phải dấu hiệu N+1 quay lại). **Chênh lệch
TRƯỚC/SAU tăng mạnh theo số phòng khác nhau (-8 → -32 cho `index()`, -4 → -28 cho `board()`) chính
là bằng chứng số N+1 đã bị xoá, và mức xoá tỉ lệ đúng với quy mô của lỗi.**

### Kết quả `--filter MeetingRoom` sau fix vòng 2

```
$ vendor/bin/phpunit --filter MeetingRoom
Tests: 53, Assertions: 105, Errors: 5, Failures: 2.
```
Giống hệt mốc trước fix vòng 2 (53/105/5/2) — không đỏ thêm ca nào. `Errors`/`Failures` vẫn đúng 5
pre-existing đã giải trình ở báo cáo gốc, không liên quan Phase 8.

Kiểm DB sau khi đo xong (script + test đều tự dọn):
```
rooms=2 bookings=3 managers=2 n1_leftover_rooms=0 n1_leftover_bookings=0
```
Đúng baseline gốc, không còn rác của lần đo N+1.

### File sửa ở fix vòng 2

- `Modules/Meeting/Services/MeetingRoomBookingService.php` — 1 chỗ (`index()`).
- `Modules/Meeting/Services/MeetingRoomService.php` — 3 chỗ (`board()`, `week()`, `statusBoard()`).

Không đụng file nào khác (kể cả các file agent song song đang sửa). Không commit/push/stash, không
đụng `hrm-client`, không tạo subagent. Script đo N+1 (`n1_measure.php`) chỉ tồn tại tạm thời trong
lúc đo, đã xoá khỏi thư mục `hrm-api/` trước khi kết thúc — không phải file bàn giao.
