# Brief — Phase 8 / lượt B1 (task T123–T127): BE danh mục "Dịch vụ phòng họp"

Đây là yêu cầu của bạn. Dùng **đúng** tên bảng / tên class / tên route viết trong file này.

## Bối cảnh

Repo `hrm-api` (Laravel 8, PHP 7.4), nhánh `gop_db`, module `Modules/Meeting`.
Phase 8 làm tính năng: người đặt phòng nhờ người phụ trách chuẩn bị **trà, nước, hoa quả…** cho cuộc
họp. Lượt này chỉ làm **danh mục** các món đó (BE). Phần gắn vào phiếu đặt phòng là lượt sau.

**Khuôn mẫu bắt buộc bám theo: danh mục "Mục đích sử dụng phòng"** — `meeting_room_purposes`.
Đọc hết bộ file của nó trước khi viết dòng nào:

- `Modules/Meeting/Database/Migrations/2026_09_19_000003_create_meeting_room_purposes_table.php`
- `Modules/Meeting/Entities/MeetingRoomPurpose.php`
- `Modules/Meeting/Services/MeetingRoomPurposeService.php`
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomPurposeController.php`
- `Modules/Meeting/Http/Requests/MeetingRoomPurpose/MeetingRoomPurposeRequest.php`
- `Modules/Meeting/Transformers/MeetingRoomPurpose/{MeetingRoomPurposeResource,DetailMeetingRoomPurposeResource}.php`
- `Modules/Meeting/Routes/api.php` (khối `meeting/room-purposes`, ~dòng 44-59)

Làm **giống hệt** khuôn đó, chỉ khác phần ghi dưới đây. Đừng phát minh kiểu mới.

## Việc phải làm

### T123 — Migration + Seeder

`Database/Migrations/2026_09_23_000002_create_meeting_room_services_table.php`, bảng
`meeting_room_services`:

| Cột | Kiểu |
|---|---|
| `id` | bigIncrements |
| `name` | string(255), **unique** |
| `unit` | string(50) nullable — đơn vị tính: ly · chai · đĩa · phần |
| `icon` | string(100) nullable |
| `sort_order` | integer default 0 |
| `note` | text nullable |
| `status` | tinyInteger default 1, comment `1 Hoạt động, 2 Khóa` |
| `created_by`, `updated_by` | unsignedBigInteger nullable |
| timestamps | |

**KHÔNG có cột `code`** — 2 danh mục phòng họp còn lại đã bỏ mã (migration
`2026_09_19_000002_drop_code_add_note_meeting_room_catalogs.php`), danh mục sinh sau không đi ngược.

`Database/Seeders/MeetingRoomServicesTableSeeder.php`: 5 món mẫu — Trà (ấm) · Nước suối (chai) ·
Hoa quả (đĩa) · Khăn lạnh (chiếc) · Bánh ngọt (đĩa). Dùng `firstOrCreate` theo `name` để chạy lại
nhiều lần không nhân bản. Đăng ký vào `MeetingDatabaseSeeder` đúng cách seeder cũ đang đăng ký.

### T124 — Entity / Service / Controller / Request / Resource

- `Entities/MeetingRoomService.php` — **`extends BaseModel`** (`use App\Models\BaseModel;`),
  `$table = 'meeting_room_services'`, `$fillable` có đủ **`created_by`, `updated_by`**.
- `Services/MeetingRoomServiceCatalogService.php` — **đặt đúng tên này**. KHÔNG đặt
  `MeetingRoomServiceService` (khó đọc, và dễ nhầm với `Services/MeetingRoomBookingService.php`
  đang tồn tại).
- `Http/Controllers/Api/V1/MeetingRoomServiceController.php`
- `Http/Requests/MeetingRoomService/MeetingRoomServiceRequest.php` — rule: `name` bắt buộc, `max:255`,
  **`unique` trên bảng `meeting_room_services`** (nhớ bỏ qua chính bản ghi khi sửa — copy đúng cách
  `MeetingRoomPurposeRequest` đang làm); `unit` nullable max 50; `icon` nullable max 100; `sort_order`
  nullable integer; `note` nullable. **CHỈ khai `rules()`, KHÔNG khai `messages()`.**
- `Transformers/MeetingRoomService/{MeetingRoomServiceResource,DetailMeetingRoomServiceResource}.php`

⚠️ **4 chỗ hay sót khi copy màn danh mục — soát đủ, ghi vào báo cáo từng chỗ:**
1. **entity-type của lịch sử** trong `app/Services/CatalogHistoryService.php` (danh mục mới phải có
   khoá riêng + nhãn cột tiếng Việt riêng, không dùng ké khoá của `meeting_room_purposes`);
2. rule `unique` trỏ **đúng bảng mới** (copy nhầm là chặn trùng theo bảng cũ, không ai phát hiện);
3. tên route/permission trong `Routes/api.php`;
4. key lưu cấu hình cột ở FE (**FE là lượt sau**, bạn chỉ ghi lại key nên dùng).

### T125 — Routes

Thêm khối `meeting/room-services` vào `Routes/api.php`, đúng thứ tự **route TĨNH trước wildcard**
(`/options`, `/export`, `/import-template`, `/import/validate`, `/import` phải đứng trước
`/{meetingRoomService}`, nếu không "export" bị nuốt thành id):

```
GET    /options            KHÔNG checkPermission
GET    /export             checkPermission:Khai báo phòng họp
GET    /import-template    checkPermission:Khai báo phòng họp
POST   /import/validate    checkPermission:Khai báo phòng họp
POST   /import             checkPermission:Khai báo phòng họp
GET    /                   checkPermission:Khai báo phòng họp
POST   /                   checkPermission:Khai báo phòng họp   (updateOrCreate)
GET    /{meetingRoomService}          checkPermission:Khai báo phòng họp
DELETE /{meetingRoomService}          checkPermission:Khai báo phòng họp
GET    /{meetingRoomService}/lock     checkPermission:Khai báo phòng họp
GET    /{meetingRoomService}/unlock   checkPermission:Khai báo phòng họp
```

**KHÔNG thêm quyền mới** — dùng lại đúng quyền `Khai báo phòng họp` đang có.
`/options` không gắn quyền vì form đặt phòng của **mọi nhân viên** phải đọc được (giống
`meeting/room-purposes/options` và `meeting/rooms/bookable` — đọc comment ở đó).

### T126 — `/options` phải giữ được món đã khoá của phiếu cũ

`GET meeting/room-services/options` nhận tham số `include_ids` (mảng hoặc chuỗi id ngăn bằng `,`):

```php
->where('status', 1)->orWhereIn('id', $includeIds)
```

Mỗi option trả `id`, `name`, `unit`, và **`is_locked`** (`status == 2`).
KHÔNG nối chữ "(đã khoá)" vào `name` — FE có helper tự gắn 🔒 dựa vào cờ `is_locked`.

### T127 — Chặn xoá món đang được phiếu dùng

`destroy()`: trước khi xoá, đếm số dòng trong bảng `meeting_room_booking_services`
(**bảng này lượt sau mới tạo** — viết code chịu được việc bảng chưa tồn tại: kiểm
`Schema::hasTable()` trước, chưa có thì coi như đếm = 0). Nếu > 0 → trả lỗi nêu **số phiếu đang dùng**
và gợi ý dùng **Khoá** thay cho Xoá. Dùng đúng mã lỗi + cách trả lỗi mà các danh mục khác trong
module đang dùng cho tình huống tương tự (đọc `MeetingRoomAmenityService`/`MeetingRoomService` xem
có sẵn khuôn "đang được dùng, không xoá được" chưa; có thì copy, không có thì ghi rõ bạn tự chọn gì).

## Ràng buộc bắt buộc

- **Không `git commit` / `push` / `stash`.** Không đụng `hrm-client`. Không tạo subagent, không tự
  gọi reviewer.
- Không thêm quyền mới, không sửa `PermissionsTableSeeder` (seeder đó truncate cả bảng).
- Luôn phân trang danh sách; cấm N+1; chỉ select cột cần.
- Không tự viết lại message cho rule validate phổ biến.
- **Một agent khác có thể đang sửa** `Services/MeetingRoomBookingService.php`, 2 Resource phiếu,
  `MeetingRoomService.php` (phần import) và `app/Services/CatalogHistoryService.php`. Nếu bạn cần sửa
  `CatalogHistoryService.php` (mục T124.1) thì **chỉ thêm khoá mới của danh mục dịch vụ**, tuyệt đối
  không đụng các dòng liên quan `manager` — và nếu thấy file đang khác lúc bạn đọc, đọc lại rồi sửa
  chèn, đừng ghi đè cả file.

## Cách tự kiểm (bắt buộc, ghi SỐ THẬT vào báo cáo)

1. `artisan migrate` sạch; `artisan db:seed --class="Modules\Meeting\Database\Seeders\MeetingRoomServicesTableSeeder"`
   chạy **2 lần** → vẫn đúng 5 bản ghi (chứng minh idempotent). Gọi PHP bằng
   `/opt/homebrew/opt/php@7.4/bin/php`.
2. `artisan migrate:rollback --step=1` rồi `migrate` lại — `down()` không vỡ.
3. Gọi thử API bằng tinker hoặc curl với token hợp lệ (nếu dựng được): tạo · sửa · khoá · mở khoá ·
   `/options` có và không có `include_ids` · xoá. Ghi lại HTTP status thật của từng lượt.
   Không dựng được token thì gọi thẳng service qua tinker và nói rõ đã kiểm ở mức nào.
4. **Kiểm audit**: tạo 1 bản ghi rồi sửa nó, `SELECT id,name,created_by,updated_by FROM
   meeting_room_services` phải có **cả 2 cột khác NULL**. Đây là cách duy nhất phát hiện thiếu
   `BaseModel`/`$fillable` — không có exception nào báo.
5. `vendor/bin/phpunit --filter MeetingRoom` — so với baseline: Tests 46, Assertions 79, Errors 5,
   Failures 2 (mức đỏ CÓ SẴN từ trước). Không được đỏ thêm.
6. Dọn sạch dữ liệu test tự tạo (trừ 5 món của seeder).

## Báo cáo

Ghi đầy đủ vào `.plans/gop-db/quan-ly-phong-hop/.sdd/p8-B1-report.md`: từng task, số đo thật 6 mục
tự kiểm, danh sách file tạo/sửa, **4 chỗ hay sót đã soát thế nào**, key cấu hình cột đề xuất cho FE,
và chỗ nào bạn phải tự quyết.
Trả về chat ngắn gọn: trạng thái, file đã sửa, 1 dòng kết quả test, điểm nghi ngờ.
