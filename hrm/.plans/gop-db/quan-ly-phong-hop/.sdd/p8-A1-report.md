# Báo cáo — Phase 8 / lượt A1 (task T109–T113): 1 phòng họp có NHIỀU người phụ trách

Repo: `hrm-api`, nhánh `gop_db`. DB local: `hrm_erp` (2 phòng họp, 3 phiếu đặt phòng trước khi làm —
đúng như ghi chú giao việc).

## Trạng thái: DONE_WITH_CONCERNS

Cả 5 task (T109–T113) đã làm xong và tự kiểm bằng số đo thật (mục dưới). "DONE_WITH_CONCERNS" vì:
(1) phải sửa thêm 1 file ngoài danh sách 5 file được giao (`MeetingRoomController.php`) để tránh vỡ
ngay endpoint `show`/`export` của chính màn phòng họp — xem mục "Deviation"; (2) `MeetingRoomBookingService.php`
+ 2 Resource phiếu đặt (đúng 3/4 chỗ brief bảo "để nguyên cho lượt sau") **sẽ crash 500 ngay khi có
request thật** vì quan hệ `manager()` đã bị xoá — đây là hệ quả bắt buộc của T110, brief đã lường
trước và giao việc đó cho lượt sau, nhưng cần lượt sau chạy **NGAY**, không được trì hoãn, nếu không
toàn bộ tính năng đặt phòng (không chỉ màn phòng họp) sẽ hỏng trên môi trường đang chạy chung code.

---

## 1. Việc đã làm theo từng task

### T109 — Migration bảng nối + backfill + drop cột cũ

File mới: `Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php`

- Bảng `meeting_room_managers`: `id` bigIncrements, `meeting_room_id` unsignedBigInteger (FK ->
  `meeting_rooms.id` `onDelete('cascade')`, tên constraint `mr_managers_room_fk`), `employee_id`
  unsignedBigInteger có index, `timestamps()`, unique `(meeting_room_id, employee_id)` (tên
  `mr_managers_room_employee_unique`).
- Backfill NGAY TRONG migration (sau `Schema::create`, trước `dropColumn`): lấy toàn bộ
  `meeting_rooms` có `manager_employee_id IS NOT NULL`, insert theo lô 1 câu `insert()`,
  `created_at`/`updated_at` = `now()` dùng chung cho cả lô.
- `down()`: thêm lại `manager_employee_id` (`unsignedBigInteger nullable`, `after('capacity')` —
  đúng vị trí cũ), đổ ngược bằng `MIN(meeting_room_managers.id)` theo từng `meeting_room_id`, rồi
  `dropIfExists('meeting_room_managers')`.
- Không khai `messages()` (đây là migration, không áp dụng); không đụng file nào khác.

### T110 — Entity `Modules/Meeting/Entities/MeetingRoom.php`

- Bỏ `manager_employee_id` khỏi `$fillable`.
- Xoá quan hệ `manager()` (`belongsTo`).
- Thêm `managers()`: `belongsToMany(Employee::class, 'meeting_room_managers', 'meeting_room_id',
  'employee_id')->withTimestamps()->with('info')`.
  - **`->with('info')` không có trong yêu cầu gốc của brief nhưng BẮT BUỘC phải thêm** — xem mục
    "Tự kiểm #Hiệu năng" bên dưới, nếu không mỗi lần đọc `managerNames()` của 1 phòng N người phụ
    trách sẽ ra N query `employee_infos` (N+1 âm thầm, brief không nhắc tới điểm này).
- Thêm `managerIds(): array` và `managerNames(): array` — cả 2 dùng chung 1 hàm private
  `loadedManagers()`: nếu `managers` đã eager load thì đọc thẳng, chưa có thì gọi `$this->load('managers')`
  (KHÔNG gọi `$this->managers()->get()` — cách đó lấy Collection mới mỗi lần, không đánh dấu quan
  hệ đã nạp trên model, nên gọi cả `managerIds()` lẫn `managerNames()` liền nhau mà chưa eager load
  sẽ ra 2 query pivot thay vì 1 — đã đo và sửa, xem mục tự kiểm).
  - `managerIds()` đệm vào `protected $managerIdsCache`, `managerNames()` đệm vào
    `protected $managerNamesCache`.
- Nguồn tên nhân viên: **giữ nguyên `Employee::fullname`** (accessor có sẵn trên
  `Modules\Timesheet\Entities\Employee`, đọc qua `$this->info->fullname`, trả `"UNKNOWN"` nếu nhân
  viên chưa gắn `employee_infos`) — đúng nguồn mà `MeetingRoomResource`/`DetailMeetingRoomResource`
  cũ đang dùng qua quan hệ `manager()`.

### T111 — `Modules/Meeting/Services/MeetingRoomService.php`

- `updateOrCreate()`: thêm `$room->managers()->sync($request->input('manager_employee_ids', []));`
  ngay sau `$room->amenities()->sync(...)`, **trong CÙNG `DB::transaction()`** đang bọc cả nhánh tạo
  mới lẫn sửa (hàm này gộp chung `store`/`update` thành 1 method `updateOrCreate()`, không phải 2
  method riêng như câu chữ brief mô tả — xem mục "Chỗ lệch giữa brief và code thật" #2).
- 3 chỗ `->with([...])` đổi `'manager.info'` (hoặc `'manager'`) -> `'managers'`: `index()` (dòng
  ~51), `bookableForCurrentEmployee()` (dòng ~134), và `->load([...])` cuối `updateOrCreate()`
  (dòng ~838).
- `catalogColumns()`: bỏ `'manager_employee_id'` khỏi mảng cột theo dõi lịch sử — cột đã bị drop,
  để lại sẽ đọc ra `null` (không lỗi) khiến lịch sử âm thầm ghi "Người quản lý phòng: ... -> (trống)"
  ở MỌI lần sửa.
- `catalogDisplay()`: xoá case `if ($column === 'manager_employee_id')` (dead code sau khi bỏ khỏi
  `catalogColumns()`).
- KHÔNG đụng phần import ở ~dòng 1054 (nay dịch xuống dòng 1066 sau các sửa phía trên — số dòng
  thật tại thời điểm bàn giao, xem mục 4 "chỗ còn `manager_employee_id`").
- **Không tìm thấy sort-theo-người-quản-lý nào trong code thật** để đổi sang `manager_name` — xem
  mục "Chỗ lệch giữa brief và code thật" #1, KHÔNG tự thêm tính năng sort mới.

### T112 — `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`

- Thay rule `'manager_employee_id' => ['nullable', 'integer']` bằng:
  ```php
  'manager_employee_ids' => ['required', 'array', 'min:1'],
  'manager_employee_ids.*' => ['integer', 'exists:employees,id'],
  ```
- Đã kiểm tên bảng nhân viên thật trước khi viết `exists`: `Modules\Timesheet\Entities\Employee::$table
  = 'employees'` (không phải `employee_infos`) — khớp brief.
- KHÔNG thêm gì vào `messages()` cho rule mới (đã kiểm bằng `Validator::make()` trực tiếp — lỗi ra
  đúng câu có sẵn trong lang file: "Bắt buộc phải nhập" / "Không tồn tại", xem mục tự kiểm).
  `messages()` cũ của file (cho `name`/`capacity`/`open_time`/...) giữ nguyên, không thuộc phạm vi
  T112 nên không dọn.

### T113 — 2 Resource phòng

`MeetingRoomResource.php` và `DetailMeetingRoomResource.php`: bỏ khoá `manager_employee_id` +
`manager_name`, thay bằng:
```php
'manager_employee_ids' => $this->managerIds(),
'manager_names' => $this->managerNames(),
'manager_name_text' => implode(', ', $this->managerNames()),
```
`implode(', ', [])` trả `''` (không `null`) khi phòng chưa có người phụ trách — khớp yêu cầu.

`BookableMeetingRoomResource.php`: **giữ nguyên hoàn toàn, không sửa 1 dòng nào**, đúng chỉ dẫn của
brief. Hệ quả: field `manager_name` của Resource này (dòng 53:
`optional(optional($this->manager)->info)->fullname`) sẽ LUÔN ra `null` sau lượt này, vì quan hệ
`manager()` đã bị xoá (Eloquent không báo lỗi khi đọc property không tồn tại, chỉ trả `null` im
lặng — đã xác nhận bằng tinker). Đây LÀ MỘT REGRESSION THẬT (modal đặt phòng sẽ mất tên người quản
lý), nhưng nằm ngoài quyền quyết định của lượt này vì brief nói rõ "giữ nguyên". Ghi lại để reviewer
quyết định hướng xử lý.

---

## 2. Deviation — sửa thêm 1 file ngoài danh sách 5 file được giao

`Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php` — 2 dòng:
- `show()` (dòng ~200): `->load([..., 'manager.info'])` -> `->load([..., 'managers'])`
- `export()` (dòng ~326): `->with([..., 'manager.info'])` -> `->with([..., 'managers'])`

**Lý do bắt buộc phải sửa**: quan hệ `manager()` đã bị xoá ở T110 (đúng yêu cầu). 2 dòng trên trong
Controller gọi `->load('manager.info')` / `->with('manager.info')` — đây là request tới 1 quan hệ
KHÔNG CÒN TỒN TẠI. Đã tái hiện lỗi TRƯỚC khi sửa bằng tinker:

```
>>> \Modules\Meeting\Entities\MeetingRoom::with('manager.info')->first();
Illuminate\Database\Eloquent\RelationNotFoundException: Call to undefined relationship [manager]
on model [Modules\Meeting\Entities\MeetingRoom].
```

Đây là exception KHÔNG BẮT ĐƯỢC bằng try/catch nghiệp vụ thường (nó ném ra ngay lúc Eloquent build
query, trước khi vào logic của Controller) — nghĩa là API `GET meeting/rooms/{id}` (show) và
`GET meeting/rooms/export` (xuất Excel) sẽ trả lỗi 500 ngay lập tức với MỌI request, không phải lỗi
nghiệp vụ. Đây chính là 2 endpoint CỦA MÀN PHÒNG HỌP (không phải domain phiếu đặt phòng), nên tôi
quyết định sửa kèm thay vì để vỡ chức năng chính của lượt này. Đã kiểm lại: cả `index()` (dòng 44,
gọi `MeetingRoomService::index()` — đã sửa ở T111) và `bookable()` (gọi
`bookableForCurrentEmployee()` — đã sửa ở T111) không còn tham chiếu nào tới `manager.info`/`manager`
trong Controller ngoài 2 chỗ trên.

---

## 3. Số đo thật của 4 mục tự kiểm

### 3.1. `artisan migrate` chạy sạch; 2 con số đếm ở T109 bằng nhau

```
$ php artisan migrate
Migrating: 2026_09_23_000001_create_meeting_room_managers_table
Migrated:  2026_09_23_000001_create_meeting_room_managers_table (344.26ms)
```

- Trước khi chạy: `SELECT COUNT(*) FROM meeting_rooms WHERE manager_employee_id IS NOT NULL` = **2**
- Sau khi chạy: `SELECT COUNT(*) FROM meeting_room_managers` = **2**
- 2 phòng backfill đúng: `meeting_room_id=1618, employee_id=13` và `meeting_room_id=2810, employee_id=13`
- `Schema::hasColumn('meeting_rooms', 'manager_employee_id')` sau migrate = **false** (đã drop)

### 3.2. `migrate:rollback --step=1` rồi `migrate` lại

```
$ php artisan migrate:rollback --step=1
Rolling back: 2026_09_23_000001_create_meeting_room_managers_table
Rolled back:  2026_09_23_000001_create_meeting_room_managers_table (232.72ms)
```

- Sau rollback: `Schema::hasColumn('meeting_rooms', 'manager_employee_id')` = **true**;
  `SELECT id, name, manager_employee_id FROM meeting_rooms` trả cả 2 phòng đều có
  `manager_employee_id = 13` (đúng — cả 2 phòng chỉ có 1 người phụ trách nên "id nhỏ nhất" = người
  duy nhất); bảng `meeting_room_managers` không còn tồn tại (`Schema::hasTable` = **false**).
- `php artisan migrate` lại: chạy sạch lần 2, `meeting_room_managers` count = **2** (khớp lại số ban
  đầu), `manager_employee_id` bị drop lại.

### 3.3. PHPUnit `--filter MeetingRoom` — mốc TRƯỚC và SAU khi sửa

**Trước khi sửa (mốc)**:
```
...................................F.F...EEEEE                    46 / 46 (100%)
Tests: 46, Assertions: 79, Errors: 5, Failures: 2.
```
- 5 Errors đều ở `Tests\Feature\MeetingRoomBookingRaceTest` — pre-existing, KHÔNG liên quan việc
  đang làm: `SQLSTATE[42S22]: Column not found: 1054 Unknown column 'code' in 'field list'` khi
  insert `meeting_rooms` (bảng `meeting_rooms` không có cột `code`, lỗi migration/DB local khác,
  đã có từ trước khi tôi chạm vào file nào).
- 2 Failures đều ở `Tests\Unit\MeetingRoomBookingSyncRuleTest` — pre-existing, về việc thiếu
  `mode_id` trong `ROOM_FIELDS`, không liên quan `manager_employee_id`.

**Sau khi sửa xong (T109–T113 + deviation Controller)**:
```
Tests: 46, Assertions: 79, Errors: 5, Failures: 2.
```
**GIỐNG HỆT baseline** — đã `diff` 2 file output, chỉ khác timestamp/số ngẫu nhiên sinh trong tên
phòng test, nội dung lỗi và số lượng y hệt. Không có test nào ĐANG XANH bị làm ĐỎ.

Ghi chú thêm (không phải regression do tôi gây ra, nhưng liên quan): 1 trong 5 lỗi baseline
(`test_approve_that_su_dung_lockForUpdate_tren_dong_phong`) có câu insert RAW chứa cả `code` LẪN
`manager_employee_id`:
```
insert into meeting_rooms (..., manager_employee_id) values (..., 34, ...)
```
Test này ĐÃ lỗi từ trước (ở cột `code`) nên chưa bao giờ chạy tới đoạn `manager_employee_id`. Nếu ai
đó sửa xong lỗi `code` trước khi lượt sau kịp sửa `MeetingRoomBookingRaceTest.php`, test này sẽ lỗi
tiếp vì cột `manager_employee_id` giờ không còn tồn tại — nêu ra để lượt sau biết, không phải việc
của lượt này (file test thuộc domain booking).

### 3.4. `grep -rn "manager_employee_id" Modules/Meeting app`

Tổng hợp các chỗ CÒN đọc/ghi cột đã drop (loại bỏ dòng migration lịch sử và comment thuần tuý —
2 loại đó không phải "đọc cột" theo nghĩa runtime):

| File | Dòng | Loại | Thuộc lượt nào |
|---|---|---|---|
| `Modules/Meeting/Services/MeetingRoomBookingService.php` | 179, 200, 777, 1193, 1198 | code thật | **Lượt sau** (brief exclude) |
| `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` | 24, 25 | code thật | **Lượt sau** (brief exclude — 1 trong 2 "Resource phiếu") |
| `Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php` | 18, 19 | code thật | **Lượt sau** (brief exclude — Resource phiếu còn lại) |
| `Modules/Meeting/Services/MeetingRoomService.php` | 1066 (`'manager_employee_id' => $managerId` trong import) | code thật | **Lượt sau** (brief exclude — "phần import ~dòng 1054", số dòng THẬT tại thời điểm bàn giao là 1066 vì các sửa T111 phía trên đẩy dòng xuống) |
| `app/Services/CatalogHistoryService.php` | 450 (label `'manager_employee_id' => 'Người quản lý phòng'`), 441 (comment) | code thật + comment | **Lượt sau** (brief exclude) |
| `Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php` | 11 | **chỉ comment** | Không phải lượt sau, không phải lượt này — brief bảo "giữ nguyên", comment giải thích lý do không trả trường này. Đây là **ngoại lệ thứ 5 không có trong danh sách 4 chỗ brief liệt kê**, xin lưu ý khi review. |
| `Modules/Meeting/Database/Migrations/2026_09_17_000002_create_meeting_rooms_table.php` | 21 | migration lịch sử (định nghĩa cột gốc) | Không đụng — migration cũ giữ nguyên đúng lịch sử schema |
| `Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php` | nhiều dòng | migration MỚI của chính task này (backfill/drop/down) | Việc của lượt này, không phải "còn sót" |
| `Modules/Meeting/Database/Migrations/2026_09_18_000002_...php`, `Modules/Meeting/Routes/api.php:113` | 1 mỗi file | comment thuần | Vô hại |

**Kết luận mục 4**: ngoài 4 chỗ brief liệt kê + 1 ngoại lệ comment ở `BookableMeetingRoomResource.php`
(brief tự yêu cầu giữ nguyên file này), **KHÔNG còn chỗ nào trong phạm vi 5 task đọc cột đã drop**.

---

## 4. Danh sách file đã sửa/tạo

**Trong phạm vi 5 task được giao:**
1. `Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php` (mới — T109)
2. `Modules/Meeting/Entities/MeetingRoom.php` (T110)
3. `Modules/Meeting/Services/MeetingRoomService.php` (T111)
4. `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php` (T112)
5. `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php` (T113)
6. `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php` (T113)

**Ngoài phạm vi (deviation, có lý do + tái hiện lỗi kèm theo ở mục 2):**
7. `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php` (2 dòng eager-load, tránh
   500 ngay lập tức ở `show()`/`export()`)

Không commit, không push, không stash — toàn bộ thay đổi còn ở working tree.

---

## 5. Chỗ lệch giữa brief và code thật

1. **Sort cột người quản lý không tồn tại.** Brief T111 viết: "Sort cột người quản lý (hiện ở
   ~dòng 716, `if ($column === 'manager_employee_id')`): đổi sang `manager_name`, order bằng
   sub-query...". Đọc code thật: dòng ~716 (trước khi tôi sửa) là trong `catalogDisplay()` — hàm
   phục vụ HIỂN THỊ GIÁ TRỊ TRONG LỊCH SỬ THAY ĐỔI (`CatalogHistoryService`), KHÔNG PHẢI sort của
   danh sách. Whitelist sort thật (`$allowedSortFields`, dòng ~92-96 của `index()`) chỉ có
   `name`/`created_at`/`updated_at` — chưa từng có `manager_employee_id` hay `manager_name`. Kiểm
   thêm ở FE (`hrm-client/pages/meeting/rooms/index.vue`, chỉ đọc, không sửa): cột `manager_name`
   khai ở đó (dòng ~565) KHÔNG có `sortable: true`. Kết luận: tính năng "sort theo người quản lý"
   chưa từng tồn tại ở cả BE lẫn FE — brief mô tả nhầm 1 đoạn code khác (`catalogDisplay`) thành
   sort. Tôi **không tự thêm tính năng sort mới** (ngoài phạm vi T111, và thêm nửa vời ở BE mà FE
   chưa có cột `sortable` thì vô dụng). Nếu lượt sau/PM thực sự muốn sort theo người quản lý, cần
   brief riêng (đụng cả BE lẫn FE, FE lại ngoài phạm vi mọi lượt của phase này theo chỉ dẫn task).

2. **`store` và `update` là 1 method, không phải 2.** Brief nói "trong transaction đang có của cả
   `store` lẫn `update`" — code thật gộp chung thành 1 method `updateOrCreate(Request $request)`
   với 1 `DB::transaction()` bọc cả nhánh tạo mới (`!$id`) và sửa (`$id`). Tôi đặt `managers()->sync()`
   đúng bên trong transaction đó, dùng chung cho cả 2 nhánh — tinh thần yêu cầu vẫn đúng
   (không mở transaction thứ 2 lồng nhau), chỉ tên hàm khác brief mô tả.

3. **`Employee::fullname` KHÔNG trả `NULL` như 1 comment cũ trong `MeetingRoomService::catalogDisplay()`
   nói.** Comment cũ (dòng 717-719, đã xoá cùng block) viết "`Employee::fullname` (accessor trên
   Employee) trả NULL — tên thật nằm ở `employee_infos.fullname`". Đọc code thật của accessor
   (`Modules/Timesheet/Entities/Employee.php` dòng 37-41):
   ```php
   public function getFullnameAttribute($value)
   {
       if ($this->info) return $this->info->fullname;
       return "UNKNOWN";
   }
   ```
   Accessor này ĐỌC qua `info` và tự trả kết quả đúng (hoặc `"UNKNOWN"` nếu thiếu `info`), KHÔNG
   trả `null`. Comment cũ đó là của 1 code path KHÁC (`catalogDisplay` dùng
   `Modules\Human\Entities\Employee` — model khác hẳn `Modules\Timesheet\Entities\Employee`, 2 class
   trùng tên ngắn `Employee` nhưng khác namespace/khác cách định nghĩa `fullname`). Đã xác nhận
   bằng tinker (mục tự kiểm): `Employee::pluck('fullname')` của
   `Modules\Timesheet\Entities\Employee` trả đúng tên thật, không có dòng nào ra `"UNKNOWN"` với 2
   nhân viên đang có manager. Không ảnh hưởng brief (brief bảo dùng đúng nguồn `manager()` cũ đang
   dùng — `Modules\Timesheet\Entities\Employee::fullname` — tôi đã làm đúng), chỉ ghi lại để tránh
   nhầm lẫn 2 class `Employee` khác nhau trong module `Human` và `Timesheet` ở các lượt sau.

---

## 6. Bàn giao cho lượt sau

### 6.1. Chữ ký `managerIds()` / `managerNames()`

```php
// Modules/Meeting/Entities/MeetingRoom.php
public function managers(): BelongsToMany   // belongsToMany(Employee::class, 'meeting_room_managers', 'meeting_room_id', 'employee_id')->withTimestamps()->with('info')
public function managerIds(): array         // mảng employees.id, đệm ở $managerIdsCache
public function managerNames(): array       // mảng fullname CÙNG THỨ TỰ managerIds(), đệm ở $managerNamesCache
```
Cả 2 dùng chung `private function loadedManagers()` — gọi hàm này thay vì tự viết
`$room->managers()->get()` nếu cần thêm hàm tương tự (vd `managerCodes()`), để không phá cơ chế
share-1-query.

### 6.2. Tên bảng + tên cột khoá ngoại thực tế

- Bảng nối: `meeting_room_managers` (`id`, `meeting_room_id`, `employee_id`, `created_at`, `updated_at`)
- FK: `meeting_room_id` -> `meeting_rooms.id`, constraint name `mr_managers_room_fk`, `onDelete('cascade')`
- Unique: `(meeting_room_id, employee_id)`, constraint name `mr_managers_room_employee_unique`
- `employee_id` trỏ `employees.id` (bảng `employees`, model `Modules\Timesheet\Entities\Employee`)
  — **KHÔNG** phải `employee_infos.id`.
- KHÔNG có FK ràng buộc `employee_id` -> `employees.id` (giống style `manager_employee_id` cũ —
  không có FK, chỉ index). Nêu ra để lượt sau biết nếu cần thêm.

### 6.3. Cách lấy tên nhân viên (để 2 Resource phiếu và import dùng đúng nguồn)

Dùng `Employee::fullname` (accessor có sẵn trên `Modules\Timesheet\Entities\Employee`, đọc qua
`$employee->info->fullname`, KHÔNG phải `Modules\Human\Entities\Employee` — xem mục 5.3 ở trên, 2
class dễ nhầm). Cách gọn nhất cho lượt sau: `$room->managerNames()` (mảng) hoặc
`implode(', ', $room->managerNames())` (chuỗi) — đã có sẵn trên Entity, không cần viết lại logic
join `employee_infos`.

### 6.4. Việc CHƯA làm, cần lượt sau xử lý (theo mức độ khẩn cấp)

**KHẨN CẤP — có thể gây lỗi 500 ngay khi có traffic thật:**
- `Modules/Meeting/Services/MeetingRoomBookingService.php`: 7 chỗ `->with(['room.amenities',
  'room.manager.info', 'purpose', ...])` (dòng 216, 362, 425, 559, 652, 696, 756) — quan hệ
  `manager` trên `MeetingRoom` không còn tồn tại, MỌI lần đọc phiếu đặt phòng (list/detail/tạo/sửa)
  sẽ ném `RelationNotFoundException` ngay tại câu `->with(...)`, trước cả khi vào logic nghiệp vụ.
  Cũng còn 5 chỗ đọc `$room->manager_employee_id` trực tiếp (dòng 179, 200, 777, 1193, 1198) — cột
  không còn nên các điều kiện này sẽ luôn `null`/`false` một cách IM LẶNG (không throw, khác với
  lỗi `.with()` ở trên) — ảnh hưởng logic "ai được duyệt phiếu = quản lý phòng" (dòng 777, 1193,
  1198) sẽ luôn coi KHÔNG AI là quản lý phòng nữa.
- `Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` (dòng 24-25) và
  `DetailMeetingRoomBookingResource.php` (dòng 18-19, 46): cùng vấn đề — đọc
  `$this->room->manager_employee_id` / `optional($this->room->manager)->info` trên quan hệ đã xoá.

**Nên làm, không khẩn cấp bằng:**
- `Modules/Meeting/Services/MeetingRoomService.php` dòng 1066 (import Excel phòng họp): đang
  `MeetingRoom::create(['manager_employee_id' => $managerId, ...])`. Vì `manager_employee_id`
  không còn trong `$fillable` (đã bỏ ở T110), Laravel Eloquent `create()` sẽ ÂM THẦM BỎ QUA key này
  (KHÔNG throw MassAssignmentException ở Laravel 8 mặc định) — nghĩa là **import Excel phòng họp
  từ giờ tạo phòng KHÔNG CÓ người phụ trách nào**, dù cột `manager_name` trong file Excel có giá
  trị. Cần đổi sang `$room->managers()->sync([$managerId])` sau khi `create()`, giống cách
  `amenities` đang làm ở ngay dưới (dòng 1072-1074 hiện tại).
- `app/Services/CatalogHistoryService.php` dòng 450: nhãn `'manager_employee_id' => 'Người quản lý
  phòng'` không còn khớp cột nào (đã bỏ khỏi `catalogColumns()` ở T111) — vô hại (chỉ là 1 entry
  thừa trong mảng nhãn), nhưng **lịch sử thay đổi phòng họp hiện KHÔNG ghi nhận thay đổi nhóm phụ
  trách** (không phải lỗi mới — trước đây ghi 1 người, giờ không ghi ai). Muốn khôi phục cần: (a)
  thêm khoá ảo `managers` vào `MeetingRoomService::roomSnapshot()` (khuôn y hệt cách `amenities`
  đang làm ở đó — nối tên bằng `, `), và (b) đăng ký nhãn hiển thị cho khoá `managers` trong
  `CatalogHistoryService::TABLES`. Tôi CỐ TÌNH không tự làm việc này vì nó đụng vào file
  `CatalogHistoryService.php` — file brief nói rõ dành cho lượt sau, và làm nửa vời (chỉ sửa 1 bên)
  sẽ khó theo dõi hơn để nguyên.
- `Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php` dòng 53: `manager_name`
  sẽ luôn ra `null` (xem mục T113 ở trên) — modal đặt phòng (`BookingFormModal.vue`) sẽ mất tên
  người quản lý hiển thị trong panel "Thông tin phòng". Brief bảo giữ nguyên file này ở lượt A1 nên
  tôi không sửa, nhưng đây là hồi quy thật cần quyết định: đổi field này sang dùng
  `$this->managerNames()` (hoặc trả thêm `manager_names` mảng, tuỳ FE cần gì) ở lượt kế tiếp có
  đụng tới file này.

---

## 7. Điểm nghi ngờ khác (không nằm trong mục nào ở trên)

- Migration mới KHÔNG thêm FK ràng buộc `employee_id -> employees.id` (chỉ index thường), theo
  đúng style cột `manager_employee_id` cũ (cũng không có FK). Nếu policy chung của dự án đang
  chuyển sang luôn thêm FK cho khoá ngoại mới (thấy có ở
  `2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table.php`), có thể cân nhắc
  thêm FK cho bảng `employee_id` này ở 1 migration riêng — tôi không tự quyết vì brief không yêu
  cầu và thêm FK cho cột trỏ tới bảng `employees` (~rất lớn, bảng lõi hệ thống) nên hỏi trước khi
  làm.
- `managers()->sync()` trong `updateOrCreate()` không kiểm tra "trùng công ty" — 1 employee từ công
  ty khác vẫn add được làm quản lý phòng (giống hành vi cũ của `manager_employee_id`, không giới
  hạn theo công ty). Giữ nguyên hành vi cũ, không tự thêm ràng buộc mới ngoài yêu cầu.
- Đã tạo 1 phòng test qua tinker để tự kiểm N+1/queries (`Tinker Test Room A1 ...`, id tạm 2811) và
  đã XOÁ SẠCH (phòng + pivot + `catalog_histories` liên quan) trước khi kết thúc — DB local đã về
  đúng baseline: 2 phòng, 3 phiếu, 2 dòng `meeting_room_managers`.
