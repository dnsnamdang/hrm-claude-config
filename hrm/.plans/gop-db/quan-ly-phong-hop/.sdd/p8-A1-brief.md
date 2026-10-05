# Brief — Phase 8 / lượt A1 (task T109–T113): 1 phòng họp có NHIỀU người phụ trách

Đây là yêu cầu của bạn. Dùng **đúng** các tên cột / tên hàm / tên trường viết trong file này.

## Bối cảnh 5 dòng

Repo `hrm-api` (Laravel 8, PHP 7.4), nhánh `gop_db`, module `Modules/Meeting`.
Hiện `meeting_rooms.manager_employee_id` là **1 người** phụ trách phòng, và người đó cũng chính là
người duyệt phiếu đặt phòng. Phase 8 sắp thêm tính năng "yêu cầu dịch vụ" (nhờ chuẩn bị trà, nước,
hoa quả) gửi cho **nhóm** phụ trách phòng, nên trước hết phải đổi 1 người → nhiều người.
Lượt này CHỈ làm phần bảng + entity + service/request/resource **của màn phòng họp**.
Phần phiếu đặt phòng (`MeetingRoomBookingService`, 2 Resource phiếu, import/export, lịch sử) là lượt
sau — **đừng đụng vào**, nhưng đọc mục "Bàn giao cho lượt sau" ở cuối để đặt tên cho khớp.

## Việc phải làm

### T109 — Migration bảng nối + backfill + drop cột cũ

Tạo `Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php`:

- Bảng `meeting_room_managers`: `id` bigIncrements · `meeting_room_id` unsignedBigInteger, FK →
  `meeting_rooms.id` **cascade on delete** · `employee_id` unsignedBigInteger, index · `timestamps()`
  · unique `(meeting_room_id, employee_id)`.
- Backfill **trong cùng migration**, sau khi tạo bảng: mỗi dòng `meeting_rooms` có
  `manager_employee_id` khác NULL → 1 dòng trong bảng nối (`created_at`/`updated_at` = `now()`).
- Sau khi backfill xong mới **drop cột `manager_employee_id`** khỏi `meeting_rooms`.
- `down()`: thêm lại cột `manager_employee_id` (unsignedBigInteger nullable, đặt sau `capacity`),
  đổ ngược người phụ trách **có id nhỏ nhất** của mỗi phòng, rồi drop bảng nối.
- Trước khi chạy migration, **đếm và ghi lại** `SELECT COUNT(*) FROM meeting_rooms WHERE
  manager_employee_id IS NOT NULL`. Sau khi chạy, `SELECT COUNT(*) FROM meeting_room_managers` phải
  bằng đúng số đó. Ghi cả 2 số vào báo cáo.

Chạy: `/opt/homebrew/opt/php@7.4/bin/php artisan migrate` (php KHÔNG có trong PATH, phải gọi đường
dẫn tuyệt đối này).

### T110 — Entity `Modules/Meeting/Entities/MeetingRoom.php`

- Bỏ `manager_employee_id` khỏi `$fillable`; **xoá** quan hệ `manager()` (dòng ~90).
- Thêm `managers()`: `belongsToMany(\Modules\Timesheet\Entities\Employee::class,
  'meeting_room_managers', 'meeting_room_id', 'employee_id')->withTimestamps()`.
- Thêm `managerIds(): array` — trả mảng `employee_id`, **cache vào thuộc tính protected** để gọi
  nhiều lần trong 1 request không query lại. Nếu quan hệ `managers` đã được eager load thì đọc từ
  quan hệ, không query thêm.
- Thêm `managerNames(): array` — mảng tên nhân viên theo đúng thứ tự `managers`.

Tên nhân viên lấy đúng cách mà quan hệ `manager()` cũ đang lấy (đọc code cũ trước khi xoá, ở
`MeetingRoomResource` có sẵn cách dựng `manager_name` — giữ nguyên nguồn đó).

### T111 — `Modules/Meeting/Services/MeetingRoomService.php`

- Lưu nhóm phụ trách bằng `$room->managers()->sync($ids)` **bên trong transaction đang có** của cả
  `store` lẫn `update` (đọc code hiện tại, đừng tạo transaction thứ hai lồng nhau).
- Sort cột người quản lý (hiện ở ~dòng 716, `if ($column === 'manager_employee_id')`): đổi sang
  `manager_name`, order bằng **sub-query lấy tên người phụ trách có `meeting_room_managers.id` nhỏ
  nhất**. Giữ whitelist cột sort (không cho order theo cột tuỳ ý).
- Mọi chỗ trả danh sách/chi tiết phòng: `->with('managers')` (cấm N+1).
- KHÔNG đụng phần import ở ~dòng 1054 (lượt sau làm).

### T112 — `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`

- Thay rule `manager_employee_id` bằng:
  `'manager_employee_ids' => ['required', 'array', 'min:1']` và
  `'manager_employee_ids.*' => ['integer', 'exists:employees,id']`
  (kiểm tên bảng nhân viên thật trong repo trước khi viết `exists`, đừng đoán).
- **CHỈ khai `rules()`, TUYỆT ĐỐI không khai `messages()`** — câu lỗi tiếng Việt đã có sẵn ở
  `hrm-api/resources/lang/vi/validation.php`. Được phép khai `attributes()` nếu cần tên trường.

### T113 — 2 Resource phòng

`Transformers/MeetingRoom/MeetingRoomResource.php` và `DetailMeetingRoomResource.php`: bỏ
`manager_employee_id`, trả thay bằng:

- `manager_employee_ids` — mảng id
- `manager_names` — mảng tên
- `manager_name_text` — chuỗi ghép bằng `", "` (rỗng thì trả `''`, KHÔNG trả `null`)

`Transformers/MeetingRoom/BookableMeetingRoomResource.php` **giữ nguyên** — nó cố tình không trả id
người phụ trách, đọc comment đầu file trước khi định sửa.

## Ràng buộc bắt buộc

- Model mới/đang sửa: giữ `extends BaseModel`; `created_by`/`updated_by` phải nằm trong `$fillable`.
- **Không `git commit`, không `git push`, không `git stash`** — CLAUDE.md của project cấm; cứ để thay
  đổi ở working tree.
- Không sửa file ngoài danh sách trên. Không đụng `hrm-client` ở lượt này.
- Không tự viết lại message validate cho rule phổ biến.
- Không tạo subagent.

## Cách tự kiểm (bắt buộc làm, ghi số thật vào báo cáo)

1. `artisan migrate` chạy sạch; 2 con số đếm ở T109 bằng nhau.
2. `artisan migrate:rollback --step=1` rồi `migrate` lại — chứng minh `down()` không vỡ. Sau khi
   rollback, `meeting_rooms.manager_employee_id` phải có lại dữ liệu; kiểm bằng 1 câu SELECT rồi
   migrate lên lại. (DB local hiện có 2 phòng, 3 phiếu — số nhỏ, kiểm tay được.)
3. Chạy PHPUnit hiện có của module để chắc không làm đỏ cái đang xanh:
   `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoom` — ghi lại số
   tests/assertions và **so với lúc chưa sửa** (chạy trước khi sửa để có mốc).
4. `grep -rn "manager_employee_id" Modules/Meeting app` — trong phạm vi 5 task này phải không còn chỗ
   nào đọc cột đã drop, TRỪ: `Services/MeetingRoomBookingService.php`, 2 Resource phiếu
   (`MeetingRoomBookingResource`, `DetailMeetingRoomBookingResource`), phần import ~dòng 1054 và
   `app/Services/CatalogHistoryService.php` — **4 chỗ đó là việc của lượt sau, để nguyên**, nhưng
   phải liệt kê ra trong báo cáo đúng số dòng.

## Bàn giao cho lượt sau (ghi rõ trong báo cáo)

- Chữ ký `managerIds()` / `managerNames()` bạn đã viết.
- Tên bảng + tên cột khoá ngoại thực tế.
- Cách bạn lấy tên nhân viên (để 2 Resource phiếu và import dùng đúng nguồn đó).

## Báo cáo

Ghi báo cáo đầy đủ vào `.plans/gop-db/quan-ly-phong-hop/.sdd/p8-A1-report.md`, gồm: việc đã làm theo
từng task, số đo thật của 4 mục tự kiểm, danh sách file đã sửa, 4 chỗ còn `manager_employee_id` để
lại cho lượt sau, mục Bàn giao, và mọi chỗ bạn thấy nghi ngờ.
Trả về chat **ngắn gọn**: trạng thái (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), danh sách
file đã sửa, 1 dòng kết quả test, và các điểm nghi ngờ.
