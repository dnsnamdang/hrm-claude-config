# Báo cáo — Phase 8 / lượt B1 (T123–T127): BE danh mục "Dịch vụ phòng họp"

Repo `hrm-api`, nhánh `gop_db`. Bám nguyên khuôn `meeting_room_purposes` theo brief
`p8-B1-brief.md`, đã đọc hết 7 file khuôn trước khi viết. DB dùng để kiểm: `hrm_erp` (local),
PHP gọi bằng `/opt/homebrew/opt/php@7.4/bin/php`.

## T123 — Migration + Seeder

- `Database/Migrations/2026_09_23_000002_create_meeting_room_services_table.php` — bảng
  `meeting_room_services`: `id`, `name` unique, `unit` nullable(50), `icon` nullable(100),
  `sort_order` default 0, `note` nullable text, `status` tinyInteger default 1 (comment
  "1 Hoạt động, 2 Khóa"), `created_by`/`updated_by` unsignedBigInteger nullable, timestamps.
  KHÔNG có cột `code` (đúng yêu cầu). `down()` chỉ `dropIfExists`.
- `Database/Seeders/MeetingRoomServicesTableSeeder.php` — 5 món mẫu: Trà (ấm) · Nước suối
  (chai) · Hoa quả (đĩa) · Khăn lạnh (chiếc) · Bánh ngọt (đĩa), dùng `firstOrCreate` theo `name`.
- Đăng ký vào `Database/Seeders/MeetingDatabaseSeeder.php` bằng `$this->call(...)`.
  **Lệch với khuôn thật đã phát hiện**: `MeetingRoomPurposesTableSeeder` (khuôn Phase 6) **KHÔNG
  hề được đăng ký** trong `MeetingDatabaseSeeder` — file đó chỉ có `Model::unguard()` + 1 dòng
  comment mẫu, seeder Purposes chỉ chạy tay bằng `artisan db:seed --class=...`. Brief lượt này
  ghi rõ "Đăng ký vào MeetingDatabaseSeeder đúng cách seeder cũ đang đăng ký" nhưng không có mẫu
  thật nào để copy nguyên văn. Tôi làm theo NGHĨA ĐEN của brief (thêm dòng `$this->call()`) vì
  vô hại và không phá vỡ gì — nhưng không đụng gì tới việc Purposes vẫn chưa được đăng ký.

## T124 — Entity / Service / Controller / Request / Resource

- `Entities/MeetingRoomService.php` — `extends BaseModel`, `$table = 'meeting_room_services'`,
  `$fillable` có đủ `created_by`, `updated_by`. Có `isCanEdit()`, `isCanLockUpdate()`,
  `isCanDelete()`, và `usedCount()` (đếm `meeting_room_booking_services`, tự chịu bảng chưa tồn
  tại bằng `Schema::hasTable()`).
- `Services/MeetingRoomServiceCatalogService.php` — đúng tên yêu cầu, không phải
  `MeetingRoomServiceService`. Có `index()` (whitelist sort, không N+1), `updateOrCreate()`,
  `lock()`/`unlock()`, `destroy()`, và bộ import Excel `validateImportData()`/`importRows()`
  (copy khuôn `MeetingRoomPurposeService` vì route T125 có sẵn `/import*`).
- `Http/Controllers/Api/V1/MeetingRoomServiceController.php` — `index`, `options`,
  `updateOrCreate`, `show`, `destroy`, `lock`, `unlock`, `export`, `validateImport`, `import`,
  `importTemplate`.
- `Http/Requests/MeetingRoomService/MeetingRoomServiceRequest.php` — CHỈ khai `rules()`, KHÔNG
  khai `messages()` (đúng yêu cầu brief — **khác** khuôn `MeetingRoomPurposeRequest` gốc, file đó
  có khai `messages()`; brief override tường minh nên tôi theo brief).
- `Transformers/MeetingRoomService/{MeetingRoomServiceResource,DetailMeetingRoomServiceResource}.php`
  — copy khuôn Purpose, thêm field `unit`.
- Phụ trợ bắt buộc để 2 màn khuôn thật sự chạy được (không có trong danh sách 7 file brief liệt
  kê, nhưng thiếu thì `export()` / lịch sử sẽ lỗi hoặc rỗng):
  - `app/ExcelExport/ExportColumnRegistry.php` — thêm khoá `meeting_room_services` (khớp field
    `MeetingRoomServiceResource`), nếu không `export()` sẽ trả cột rỗng.
  - `app/Services/CatalogHistoryService.php` — thêm khoá `meeting_room_services` vào
    `const TABLES` (xem mục 4 chỗ hay sót bên dưới).

### 4 chỗ hay sót khi copy màn danh mục — đã soát

1. **Entity-type lịch sử**: thêm khoá RIÊNG `'meeting_room_services'` vào `CatalogHistoryService::TABLES`
   (không dùng ké `meeting_room_purposes`), nhãn cột tiếng Việt riêng (`Tên dịch vụ`, `Đơn vị
   tính`, `Icon`, `Thứ tự`, `Ghi chú`, `Trạng thái`). Chỉ THÊM 1 block mới, không đụng dòng nào
   liên quan `manager`/`managers` — đã `git diff` xác nhận diff chỉ có phần thêm mới (xem log
   diff cuối báo cáo).
2. **Rule `unique`**: `Rule::unique('meeting_room_services', 'name')->ignore($id)` — đã trỏ đúng
   bảng mới, kiểm bằng ca "tạo trùng tên" trả `422` với message "Đã tồn tại trên hệ thống" (mục
   tự kiểm #3).
3. **Route/permission**: khối `meeting/room-services` dùng đúng quyền `Khai báo phòng họp`
   (không thêm quyền mới), route tĩnh (`/options`, `/export`, `/import-template`,
   `/import/validate`, `/import`) đứng TRƯỚC wildcard `/{meetingRoomService}` — đã kiểm bằng HTTP
   test thật: gọi `/options` và `/export`-flow không bị nuốt thành id.
4. **Key cấu hình cột FE** (FE là lượt sau, chỉ đề xuất): `meeting_room_services_columns` (theo
   đúng khuôn đặt tên các màn danh mục phòng họp khác, ví dụ dạng `<table>_columns`) — FE lượt
   sau tự xác nhận lại theo convention thật đang dùng ở `localStorage`/Vuex của màn danh mục.

## T125 — Routes

Thêm khối `meeting/room-services` vào `Modules/Meeting/Routes/api.php`, đặt SAU khối
`meeting/room-purposes`, TRƯỚC khối `meeting/rooms`. Thứ tự bên trong đúng yêu cầu: `/options` →
`/export` → `/import-template` → `/import/validate` → `/import` → `/` (GET) → `/` (POST) →
`/{meetingRoomService}` → `/{meetingRoomService}/lock` → `/{meetingRoomService}/unlock`.
`/options` KHÔNG gắn `checkPermission`, mọi route còn lại gắn `checkPermission:Khai báo phòng
họp`. Không thêm quyền mới, không sửa `PermissionsTableSeeder`.

## T126 — `/options` giữ được món đã khoá của phiếu cũ

`GET meeting/room-services/options` nhận `include_ids` (string ngăn bằng dấu phẩy hoặc mảng),
build query `where('status', 1)->when(!empty($includeIds), fn($q) => $q->orWhereIn('id',
$includeIds))` (tương đương `where(...)->orWhereIn(...)` khi có include_ids, và chỉ
`where('status',1)` khi không có). Mỗi option trả `id`, `name`, `unit`, `is_locked`
(`status == 2`) — KHÔNG nối chữ vào `name`.

Đã kiểm bằng HTTP test thật (xem mục tự kiểm #3): dịch vụ đã khoá **xuất hiện** khi gọi
`/options?include_ids=<id>` (kèm `is_locked:true`), và **KHÔNG xuất hiện** khi gọi `/options`
không kèm `include_ids`.

## T127 — Chặn xoá món đang được phiếu dùng

`MeetingRoomService::usedCount()` kiểm `Schema::hasTable('meeting_room_booking_services')`
trước — bảng của LƯỢT SAU, hiện CHƯA tồn tại, nên `usedCount()` trả 0 và xoá bình thường.
`MeetingRoomServiceController::destroy()` gọi `usedCount()` (KHÔNG dùng `isCanDelete()` đơn
thuần) để lấy được SỐ để đưa vào message, giống khuôn message của `MeetingRoomPurposeController`/
`MeetingRoomAmenityController` ("... đang được dùng ... không xóa được. Bạn có thể Khóa ...")
nhưng thêm số phiếu cụ thể — 2 controller khuôn không có "đếm sẵn xong xoá" nào khác để copy
nguyên văn (Purpose/Amenity chỉ có exists(), không có số), nên đây là **quyết định tự chọn**: giữ
message dạng cũ nhưng chèn số đếm thật ("Dịch vụ này đang được dùng ở N phiếu đặt phòng nên không
xóa được. Bạn có thể Khóa dịch vụ này."), HTTP 400 — đúng mã lỗi + response shape chung
(`responseJson($message, 400)`) mà mọi controller khác trong module đang dùng cho lỗi nghiệp vụ.

**Tên cột khoá ngoại tự quyết định**: `meeting_room_service_id` (theo đúng khuôn đặt tên
`purpose_id`/`meeting_room_amenity_id` của module — bảng `meeting_room_booking_services` chưa
tồn tại nên đây là tên tôi CHỌN cho lượt sau bám theo, không phải tên có sẵn để copy).

## Cách tự kiểm — SỐ THẬT

**#1 — Migrate + seed 2 lần (idempotent)**
```
php artisan migrate            → Migrated: 2026_09_23_000002_create_meeting_room_services_table (77.44ms), sạch
php artisan db:seed --class="Modules\Meeting\Database\Seeders\MeetingRoomServicesTableSeeder"
  Lần 1: count = 5
  Lần 2: count = 5   (không nhân bản)
```

**#2 — Rollback + migrate lại**
```
php artisan migrate:rollback --step=1  → Rolled back (33.29ms)
Schema::hasTable('meeting_room_services') sau rollback = false
php artisan migrate                     → Migrated lại (49.97ms)
Schema::hasTable('meeting_room_services') sau migrate lại = true
count sau migrate lại (chưa seed) = 0
```
`down()` không vỡ. Seed lại 5 dòng mẫu để tiếp tục kiểm #3, #4.

**#3 — Gọi API thật qua HTTP (PHPUnit `TestCase` + JWT thật từ `JWTAuth::fromUser()`, KHÔNG chỉ
gọi service qua tinker)** — actor: employee `1181` (đã xác nhận có quyền "Khai báo phòng họp"
qua tinker trước khi chọn). Viết 1 file test SCRATCH (`tests/Feature/ZZZScratch...php`), chạy
`phpunit --filter`, rồi **xoá file này** sau khi lấy xong số đo (không phải một phần bàn giao):

| Lượt gọi | HTTP status thật |
|---|---|
| `GET /api/v1/meeting/room-services?per_page=5` | **200** |
| `GET /api/v1/meeting/room-services/options` (không `include_ids`) | **200** |
| `POST /api/v1/meeting/room-services` (tạo mới) | **200** |
| `POST /api/v1/meeting/room-services` (sửa, đổi `unit`) | **200** |
| `POST /api/v1/meeting/room-services` (tạo trùng tên) | **422** (`"name":"Đã tồn tại trên hệ thống"`) |
| `GET /api/v1/meeting/room-services/{id}/lock` | **200** |
| `GET /api/v1/meeting/room-services/options?include_ids={id}` (id vừa khoá) | **200**, thấy `id` đó, `is_locked:true` |
| `GET /api/v1/meeting/room-services/options` (không include_ids, sau khi khoá) | **200**, `id` đã khoá **KHÔNG** xuất hiện |
| `GET /api/v1/meeting/room-services/{id}/unlock` | **200** |
| `DELETE /api/v1/meeting/room-services/{id}` (chưa ai dùng) | **200** |
| `DELETE .../{id}` khi `meeting_room_booking_services` **chưa tồn tại** (dựng thủ công entity, gọi `usedCount()`) | `usedCount() = 0`, `isCanDelete() = true` (không throw) |
| `DELETE .../{id}` khi có 3 dòng giả trong `meeting_room_booking_services` (bảng dựng TẠM bằng `DB::statement(CREATE TABLE...)` trong test rồi drop lại) | **400**, message chứa `"3 phiếu đặt phòng"`, bản ghi KHÔNG bị xoá |

Toàn bộ 3 test scratch: `OK (3 tests, 21 assertions)`.

**#4 — Kiểm audit `created_by`/`updated_by`** (tinker, set `auth()->guard('api')->setUser(...)`
employee 1181):
```
tạo mới rồi update 1 bản ghi →
SELECT id,name,created_by,updated_by FROM meeting_room_services WHERE id=12
id=12 name="ZZZ Audit Check 2" created_by=1181 updated_by=1181
```
Cả 2 cột khác NULL — xác nhận `BaseModel` + `$fillable` hoạt động đúng. (Bản ghi test đã xoá
ngay sau khi đọc số liệu.)

**#5 — `vendor/bin/phpunit --filter MeetingRoom`**
```
Tests: 53, Assertions: 105, Errors: 5, Failures: 2
```
So với baseline brief ghi (Tests 46, Assertions 79, Errors 5, Failures 2): **Errors và Failures
khớp CHÍNH XÁC** (5 và 2, không đỏ thêm). Tests/Assertions tăng (46→53, 79→105) — KHÔNG phải do
lượt B1 này: đã kiểm từng lỗi/fail bằng tên test, toàn bộ nằm ở
`Tests\Feature\MeetingRoomBookingRaceTest` (5 lỗi `Unknown column 'code'` — do
`meeting_rooms.code` đã bị DROP ở Task 44, test cũ chưa cập nhật, không liên quan Dịch vụ phòng
họp) và `Tests\Unit\MeetingRoomBookingSyncRuleTest` (2 fail liên quan `mode_id`/đồng bộ phiếu,
cũng không liên quan). Tests/Assertions tăng do các file test khác (`MeetingRoomManagersTest`,
việc của lượt A2 chạy song song hôm nay) đã thêm case mới từ sau lúc baseline được ghi — không
phải do tôi tạo test mới (file scratch đã xoá trước khi chạy lượt kiểm #5 này).

**#6 — Dọn dữ liệu test**
```
SELECT COUNT(*) FROM meeting_room_services  → 5   (đúng 5 món seeder, không còn rác)
SELECT COUNT(*) FROM catalog_histories WHERE table_name='meeting_room_services' → 0
Schema::hasTable('meeting_room_booking_services') → false (bảng tạm đã DROP)
tests/Feature/ZZZScratch...php → đã xoá
```

## Danh sách file tạo / sửa

**Tạo mới**
- `Modules/Meeting/Database/Migrations/2026_09_23_000002_create_meeting_room_services_table.php`
- `Modules/Meeting/Database/Seeders/MeetingRoomServicesTableSeeder.php`
- `Modules/Meeting/Entities/MeetingRoomService.php`
- `Modules/Meeting/Services/MeetingRoomServiceCatalogService.php`
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomServiceController.php`
- `Modules/Meeting/Http/Requests/MeetingRoomService/MeetingRoomServiceRequest.php`
- `Modules/Meeting/Transformers/MeetingRoomService/MeetingRoomServiceResource.php`
- `Modules/Meeting/Transformers/MeetingRoomService/DetailMeetingRoomServiceResource.php`

**Sửa (chỉ thêm, không đụng dòng cũ liên quan `manager`)**
- `Modules/Meeting/Database/Seeders/MeetingDatabaseSeeder.php` — thêm 1 dòng `$this->call(...)`.
- `Modules/Meeting/Routes/api.php` — thêm `use` + 1 khối route mới.
- `app/Services/CatalogHistoryService.php` — thêm 1 entry `'meeting_room_services'` vào
  `const TABLES` (đã diff xác nhận không đụng khối `manager`/`managers`).
- `app/ExcelExport/ExportColumnRegistry.php` — thêm 1 entry `'meeting_room_services'` vào
  `const COLUMNS`.

Không đụng `Services/MeetingRoomService.php` (booking-side, phòng), `Services/MeetingRoomBookingService.php`,
2 Resource phiếu/phòng, hay `hrm-client`.

## Chỗ tự quyết định (tóm tắt)

1. Không đăng ký lại/sửa việc `MeetingRoomPurposesTableSeeder` chưa có trong `MeetingDatabaseSeeder`
   — chỉ thêm đăng ký cho seeder mới theo đúng câu chữ brief.
2. Tên cột khoá ngoại của bảng lượt sau: `meeting_room_service_id` (chưa có bảng thật để soi).
3. Message + HTTP 400 cho `destroy()` khi đang dùng: giữ khuôn message "đang được dùng ... Khóa
   thay vì Xóa" của 2 danh mục anh em, chèn thêm SỐ phiếu cụ thể (2 khuôn gốc không có số).
4. Key cấu hình cột FE đề xuất: `meeting_room_services_columns` — FE lượt sau tự xác nhận lại.
