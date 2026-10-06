# Brief — Phase 8 / lượt C1 (task T131–T137): BE "Yêu cầu dịch vụ" trên phiếu đặt phòng

Repo `hrm-api`, nhánh `gop_db`, module `Modules/Meeting`. Dùng **đúng** tên bảng/cột/class/route dưới đây.

## Bối cảnh

Người đặt phòng nhờ người phụ trách phòng chuẩn bị trà / nước / hoa quả… cho cuộc họp.
Lượt B1 đã dựng **danh mục** `meeting_room_services` (tên · đơn vị tính · icon · khoá/mở khoá) và
endpoint `GET meeting/room-services/options`. Lượt A1/A2 đã đổi phòng họp sang **nhiều người phụ
trách** (`MeetingRoom::managerIds()`, `managers()`, `syncManagers()`).
Lượt này: gắn yêu cầu dịch vụ vào **phiếu đặt phòng** (`meeting_room_bookings`, mã `DPH-YYYY-NNNNN`).

Đọc trước khi code: `.sdd/p8-B1-report.md` (tên class/khoá danh mục thật) và
`docs/superpowers/specs/gop-db/2026-09-23-yeu-cau-dich-vu-phong-hop-design.md` **mục 7 (10 luật
nghiệp vụ)** — mục đó là nguồn chân lý, brief này chỉ diễn giải lại.

## Việc phải làm

### T131 — 2 migration + entity + quan hệ

`Database/Migrations/2026_09_23_000003_create_meeting_room_booking_services_table.php` —
bảng `meeting_room_booking_services`:

| Cột | Kiểu |
|---|---|
| `id` | bigIncrements |
| `booking_id` | unsignedBigInteger, index, FK → `meeting_room_bookings.id` **cascade on delete** |
| `service_id` | unsignedBigInteger **nullable**, index |
| `service_name` | string(255) — **snapshot** tên món lúc yêu cầu |
| `unit` | string(50) nullable — **snapshot** đơn vị tính |
| `quantity` | decimal(12,2) |
| `note` | string(255) nullable |
| `sort_order` | integer default 0 |
| timestamps | |

unique `(booking_id, service_id)`.

`Database/Migrations/2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table.php` —
thêm vào `meeting_room_bookings`:

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `service_status` | tinyInteger **nullable** | **NULL = phiếu KHÔNG kèm dịch vụ** · 1 Chờ chuẩn bị · 2 Đã chuẩn bị · 3 Từ chối |
| `service_handled_by` | unsignedBigInteger nullable | `employees.id` người bấm |
| `service_handled_at` | dateTime nullable | |
| `service_reject_reason` | string(500) nullable | |

> `NULL` khác `1` là điểm mấu chốt: "không yêu cầu gì" và "đã yêu cầu, chưa ai chuẩn bị" phải phân
> biệt được, nếu không bộ lọc và badge sai cho MỌI phiếu.

Entity **`Entities/MeetingRoomBookingServiceItem.php`** — đặt đúng tên này, KHÔNG đặt
`MeetingRoomBookingService` (đụng `Services/MeetingRoomBookingService.php` đang có). `extends
BaseModel`, `$table = 'meeting_room_booking_services'`.
Quan hệ `MeetingRoomBooking::serviceItems()` — `hasMany`, `orderBy('sort_order')` **tường minh**.

### T131b — SỬA LỆCH TÊN CỘT DO LƯỢT B1 ĐỂ LẠI (bắt buộc, làm cùng T131)

Lượt B1 viết guard "chặn xoá món đang có phiếu dùng" trong
`Services/MeetingRoomServiceCatalogService.php::destroy()` khi bảng `meeting_room_booking_services`
**chưa tồn tại**, nên đã tự đặt tên cột khoá ngoại là **`meeting_room_service_id`**.
Bảng thật bạn tạo ở T131 dùng tên **`service_id`** (theo spec).

→ Sửa `destroy()` của B1 cho trỏ đúng cột **`service_id`**.

⚠️ Đây là lỗi **im lặng** nếu bỏ qua: câu đếm trỏ sai cột sẽ ném lỗi SQL, hoặc tệ hơn là đếm ra 0 và
**cho xoá món đang được phiếu dùng** — không ai phát hiện cho tới khi mở phiếu cũ thấy mất tên món.
Bắt buộc có **1 ca test** chứng minh: tạo phiếu dùng món X → gọi xoá món X → bị chặn (đúng mã lỗi
B1 đang dùng), và món vẫn còn trong DB.

### T132 — Validate (`Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php`)

- `services` → `nullable|array|max:20`
- `services.*.service_id` → bắt buộc, `integer`, `exists` trên `meeting_room_services`, và **phải
  đang Hoạt động** (`status = 1`) — món đã khoá thì không cho chọn MỚI (phiếu cũ vẫn giữ, xem luật 9).
- `services.*.quantity` → bắt buộc, `numeric`, `> 0`, `<= 999999`
- `services.*.note` → `nullable|max:255`
- **Chặn trùng `service_id`** trong cùng mảng (unique theo cặp `(booking_id, service_id)` ở DB chỉ là
  lưới an toàn cuối, phải báo lỗi tử tế trước đó).
- **CHỈ khai `rules()`, KHÔNG khai `messages()`** cho rule phổ biến. Chỉ được viết câu riêng cho luật
  nghiệp vụ mà lang file không diễn đạt được (vd câu báo trùng món).

### T133 — `store()` trong `Services/MeetingRoomBookingService.php`

Trong **transaction đang có**:
- Ghi từng dòng vào `meeting_room_booking_services`, **snapshot `service_name` + `unit`** đọc từ danh
  mục tại thời điểm tạo (KHÔNG chỉ lưu `service_id` rồi join lúc hiển thị — danh mục đổi tên là phiếu
  cũ sai).
- `sort_order` theo đúng thứ tự user gửi lên.
- Có ≥ 1 dòng → `service_status = 1`; không dòng nào → để **NULL**.
- **Phòng không có người phụ trách nào mà gửi `services[]` → trả 422** kèm câu nêu rõ lý do (luật 8).
  Chặn ở BE, không dựa FE ẩn.

### T134 — `update()`

- **Bỏ hoàn toàn** khoá `services` khỏi payload đọc vào: phiếu chỉ nhập dịch vụ lúc TẠO (luật 2).
  Gửi kèm `services[]` thì dữ liệu dịch vụ **không đổi** — không lỗi, chỉ lặng lẽ bỏ qua.
- **Đổi phòng lúc sửa phiếu**: dòng dịch vụ giữ nguyên, `service_status` giữ nguyên, và **bắn thông
  báo cho nhóm phụ trách phòng MỚI** (luật 3) — nếu không, đồ nằm ở phòng không ai biết.

### T135 — 2 endpoint xử lý

```
PUT meeting/room-bookings/{meetingRoomBooking}/service-prepared
PUT meeting/room-bookings/{meetingRoomBooking}/service-rejected
```

Đặt **trước** wildcard nếu cần, cạnh cặp `approve`/`reject` sẵn có; **KHÔNG gắn `checkPermission`** —
gate theo vai trò ngay trong service (giống `approve`/`reject`).
`MeetingRoomBookingServiceRejectRequest`: `reason` bắt buộc, `max:500`.

Guard (đủ 3 điều kiện, thiếu 1 là hỏng luật):
1. người đăng nhập ∈ `$booking->room->managerIds()`;
2. `service_status === 1`;
3. phiếu **không** ở trạng thái Hủy / Từ chối.

Sai điều kiện 2 (người thứ hai bấm sau) → **409** kèm câu nêu **ai đã xử lý lúc nào** (luật 5).
Sai điều kiện 1 → **403**. Thành công → ghi `service_handled_by = auth()->id()`, `service_handled_at`,
`service_status = 2` (hoặc 3 + `service_reject_reason`).
**Phiếu đã qua giờ vẫn bấm được** (luật 7) — đừng thêm điều kiện thời gian.

### T136 — Resource phiếu

`MeetingRoomBookingResource` (list) và `DetailMeetingRoomBookingResource` (detail) trả thêm:

| Trường | Ghi chú |
|---|---|
| `has_service_request` | `service_status !== null` |
| `service_status` | 1/2/3 hoặc null |
| `service_status_text` | "Chờ chuẩn bị" · "Đã chuẩn bị" · "Từ chối" (null → `null`) |
| `service_status_color` | `#D97706` · `#16A34A` · `#DC2626` — **BE quyết màu**, FE chỉ hiển thị |
| `service_handled_by_name`, `service_handled_at`, `service_reject_reason` | |
| `services[]` (chỉ detail) | `service_id`, `service_name`, `unit`, `quantity`, `note` |
| `is_can_handle_service` | **fail-closed**: mặc định `false`, chỉ `true` khi đủ 3 điều kiện guard ở T135 |

Eager load `serviceItems` **và** `room.managers` ở cả `index()` lẫn chỗ lấy chi tiết — **cấm N+1**.
(Lượt trước vừa dính đúng lỗi này: `$isRoomManager` tính theo từng dòng làm mỗi dòng bắn 1 query.)

### T137 — Thông báo `[DPH]`

Dùng lại `sendBookingNotification()` sẵn có. 4 mốc (nhóm hành động → người nhận):

| Khi nào | Nhóm hành động | Người nhận |
|---|---|---|
| Tạo phiếu có ≥ 1 dòng dịch vụ | `Yêu cầu dịch vụ` | toàn bộ nhóm phụ trách phòng |
| Sửa phiếu đổi sang phòng khác (phiếu có dịch vụ) | `Yêu cầu dịch vụ` | nhóm phụ trách phòng MỚI |
| Phiếu Hủy / Từ chối trong khi `service_status = 1` | `Hủy yêu cầu dịch vụ` | nhóm phụ trách |
| Bấm Đã chuẩn bị / Từ chối dịch vụ | `Đã chuẩn bị dịch vụ` / `Từ chối dịch vụ` | **người đặt phiếu** |

Khuôn nội dung: `[DPH] {Nhóm hành động}: {Tên phiếu}. {Ghi chú}` — tên ≤ 50 ký tự, tổng ≤ 120 ký tự,
deep-link kèm ID. Đọc `.claude/skills/notification-convention/SKILL.md` trước khi viết câu.
Ghi chú gợi ý: tạo mới → "N món"; từ chối → lý do.

## Ràng buộc bắt buộc

- **Luật 6 (đóng băng)**: phiếu Hủy/Từ chối thì `service_status` **GIỮ NGUYÊN giá trị đang có**
  (không tự đổi sang trạng thái khác) — lịch sử phải đọc được là "đã yêu cầu mà chưa ai xử lý".
- Không thêm quyền mới. Không sửa `PermissionsTableSeeder`.
- `extends BaseModel`, `$fillable` có `created_by`/`updated_by`.
- Luôn `auth()->id()`; cấm `auth()->user()->info->id`.
- **Không `git commit`/`push`/`stash`**, không đụng `hrm-client`, không tạo subagent, không tự gọi
  reviewer.

## Cách tự kiểm (bắt buộc, SỐ THẬT vào báo cáo)

1. `artisan migrate` sạch, `migrate:rollback --step=2` rồi `migrate` lại cũng sạch.
   PHP gọi bằng `/opt/homebrew/opt/php@7.4/bin/php`.
2. **Viết test** `tests/Feature/MeetingRoomBookingServiceRequestTest.php`, tối thiểu 7 ca:
   - tạo phiếu 3 món → 3 dòng bảng con, `service_status = 1`, snapshot tên đúng;
   - tạo phiếu không món → `service_status` **NULL**;
   - `update()` gửi kèm `services[]` → dữ liệu dịch vụ **không đổi**;
   - người trong nhóm phụ trách bấm Đã chuẩn bị → 2 + ghi `service_handled_by`;
   - **người thứ hai** bấm sau → **409**;
   - người **ngoài** nhóm bấm → **403** (ca phân quyền, bắt buộc phải có);
   - phiếu đã Hủy → không xử lý được; và `service_status` **giữ nguyên 1**.
   Chạy thật, dán output.
3. `--filter MeetingRoom` — mốc hiện tại 53 tests / 105 assertions / 5 Errors / 2 Failures (mức đỏ
   CÓ SẴN từ trước, không liên quan Phase 8). Không được đỏ thêm.
4. **Đo N+1**: seed tạm ~15 phiếu có dịch vụ trên 2-3 phòng, bật `DB::enableQueryLog()`, gọi
   `index()` → số query **không được tăng theo số dòng**. Dán số thật. Xoá sạch dữ liệu seed sau khi đo.
5. Dọn dữ liệu test; cuối cùng `SELECT COUNT(*)` 3 bảng (`meeting_rooms`, `meeting_room_bookings`,
   `meeting_room_booking_services`) phải về đúng baseline (2 / 3 / 0).

## Báo cáo

`.sdd/p8-C1-report.md`: từng task, output test thật, số query đo được, file tạo/sửa, chỗ tự quyết,
và **bàn giao cho lượt FE**: tên trường Resource, mã lỗi từng tình huống, payload `services[]` mẫu.
Trả về chat ngắn gọn: trạng thái, file, 1 dòng kết quả test, điểm nghi ngờ.
