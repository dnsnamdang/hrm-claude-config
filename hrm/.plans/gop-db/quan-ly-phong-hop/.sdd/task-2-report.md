# Task 2 report — Migration 6 bảng + 2 alter

**Status: DONE_WITH_CONCERNS** (xem mục "Bước 8 — rollback" bên dưới, lý do KHÔNG phải do DB dùng chung)

## 1. File đã tạo

Tất cả trong `hrm-worktrees/phong-hop-api/Modules/Meeting/Database/Migrations/`:

1. `2026_09_17_000001_create_meeting_room_amenities_table.php`
2. `2026_09_17_000002_create_meeting_rooms_table.php`
3. `2026_09_17_000003_create_meeting_room_room_amenity_table.php`
4. `2026_09_17_000004_create_meeting_room_bookings_table.php`
5. `2026_09_17_000005_create_meeting_room_booking_participants_table.php`
6. `2026_09_17_000006_create_meeting_room_booking_recurrences_table.php`
7. `2026_09_17_000007_add_meeting_room_id_to_meetings_table.php`
8. `2026_09_17_000008_add_meeting_room_config_to_general_regulations_table.php`

Nội dung bám sát nguyên văn code mẫu trong brief cho bảng 1–3, 5 và 2 alter. Bảng
`meeting_room_bookings` (000004) lấy đủ cột theo spec mục 4.4 (28 cột + timestamps) và đúng 5
index yêu cầu. Bảng `meeting_room_booking_recurrences` (000006) lấy cột theo spec mục 4.6: `id`,
`meeting_room_id`, `title`, `content`, `weekdays` (string 20, có comment giải thích quy ước),
`start_date`, `end_date`, `start_time`, `end_time`, `host_employee_id`, `attendee_count`,
`created_by`, `updated_by`, `timestamps` — spec không chỉ định kiểu/độ dài cụ thể cho các cột này
nên tôi chọn kiểu hợp lý theo quy ước các bảng lân cận (date cho start_date/end_date, time cho
start_time/end_time, string(255) cho title, text nullable cho content).

## 2. Chuẩn bị & kiểm tra trước khi migrate

- `config:clear` chạy trước migrate (theo ràng buộc bắt buộc) — sạch, chỉ có warning không liên
  quan (thiếu extension `imagick.so`, không ảnh hưởng migration).
- Kiểm tra trước: `SHOW TABLES LIKE 'meeting_room%'`, cột `meetings.meeting_room_id`, cột
  `general_regulations.meeting_room%` — đều **chưa tồn tại**, không có xung đột với ai khác.
- `meetings.location` tồn tại (varchar 255) nên `->after('location')` hợp lệ.

## 3. Kết quả `artisan migrate`

```
cd hrm-worktrees/phong-hop-api
/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/Meeting/Database/Migrations
```

Cả 8 migration chạy **sạch, không lỗi**:

```
Migrating: 2026_09_17_000001_create_meeting_room_amenities_table
Migrated:  2026_09_17_000001_create_meeting_room_amenities_table (2,655.03ms)
Migrating: 2026_09_17_000002_create_meeting_rooms_table
Migrated:  2026_09_17_000002_create_meeting_rooms_table (1,003.36ms)
Migrating: 2026_09_17_000003_create_meeting_room_room_amenity_table
Migrated:  2026_09_17_000003_create_meeting_room_room_amenity_table (207.21ms)
Migrating: 2026_09_17_000004_create_meeting_room_bookings_table
Migrated:  2026_09_17_000004_create_meeting_room_bookings_table (2,627.84ms)
Migrating: 2026_09_17_000005_create_meeting_room_booking_participants_table
Migrated:  2026_09_17_000005_create_meeting_room_booking_participants_table (1,786.18ms)
Migrating: 2026_09_17_000006_create_meeting_room_booking_recurrences_table
Migrated:  2026_09_17_000006_create_meeting_room_booking_recurrences_table (486.90ms)
Migrating: 2026_09_17_000007_add_meeting_room_id_to_meetings_table
Migrated:  2026_09_17_000007_add_meeting_room_id_to_meetings_table (2,648.97ms)
Migrating: 2026_09_17_000008_add_meeting_room_config_to_general_regulations_table
Migrated:  2026_09_17_000008_add_meeting_room_config_to_general_regulations_table (2,229.88ms)
```

Batch được gán: **396** (đỉnh bảng `migrations` trước đó là batch 395, gọn gàng, không lẫn).

## 4. `SHOW CREATE TABLE meeting_room_bookings`

```sql
CREATE TABLE `meeting_room_bookings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `meeting_room_id` bigint unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text,
  `start_at` datetime NOT NULL,
  `end_at` datetime NOT NULL,
  `status` tinyint NOT NULL COMMENT '1 Chờ duyệt, 2 Đã duyệt, 3 Từ chối, 4 Đã hủy, 5 Hoàn thành',
  `booked_by_employee_id` bigint unsigned NOT NULL,
  `host_employee_id` bigint unsigned DEFAULT NULL,
  `attendee_count` int DEFAULT NULL,
  `company_id` bigint unsigned DEFAULT NULL,
  `department_id` bigint unsigned DEFAULT NULL,
  `meeting_id` bigint unsigned DEFAULT NULL,
  `source` tinyint NOT NULL DEFAULT '1' COMMENT '1 Tự đặt, 2 Sinh từ Meeting',
  `approved_by` bigint unsigned DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `reject_reason` varchar(500) DEFAULT NULL,
  `is_auto_rejected` tinyint NOT NULL DEFAULT '0',
  `cancelled_by` bigint unsigned DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `cancel_reason` varchar(500) DEFAULT NULL,
  `checkin_at` datetime DEFAULT NULL,
  `checkout_at` datetime DEFAULT NULL,
  `auto_released_at` datetime DEFAULT NULL,
  `checkout_reminded_at` datetime DEFAULT NULL,
  `recurrence_id` bigint unsigned DEFAULT NULL,
  `created_by` bigint unsigned DEFAULT NULL,
  `updated_by` bigint unsigned DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meeting_room_bookings_meeting_id_unique` (`meeting_id`),
  KEY `mrb_room_time_index` (`meeting_room_id`,`start_at`,`end_at`),
  KEY `meeting_room_bookings_status_index` (`status`),
  KEY `meeting_room_bookings_booked_by_employee_id_index` (`booked_by_employee_id`),
  KEY `meeting_room_bookings_recurrence_id_index` (`recurrence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

→ Có đủ `mrb_room_time_index (meeting_room_id, start_at, end_at)` và unique `meeting_id`
(`meeting_room_bookings_meeting_id_unique`) — đúng kỳ vọng bước 7.

## 5. Kiểm 6 bảng + 2 alter

```
SHOW TABLES LIKE 'meeting_room%':
  meeting_room_amenities
  meeting_room_booking_participants
  meeting_room_booking_recurrences
  meeting_room_bookings
  meeting_room_room_amenity
  meeting_rooms

meetings.meeting_room_id: bigint unsigned, NULL, default NULL  ✓

general_regulations:
  meeting_room_open_time                  time  NULL  default 07:00:00  ✓
  meeting_room_close_time                 time  NULL  default 20:00:00  ✓
  meeting_room_checkin_grace_minutes      int   NULL  default 15        ✓
  meeting_room_checkout_reminder_minutes  int   NULL  default 10        ✓
  meeting_room_max_advance_days           int   NULL  default 90        ✓
```

Đủ 6 bảng, cột `meetings.meeting_room_id`, đủ 5 cột `general_regulations.meeting_room_*` với
default đúng brief.

## 6. Bước 8 — kiểm rollback: BỊ CHẶN BỞI PERMISSION CỦA HARNESS (không phải rủi ro DB dùng chung)

Trước khi chạy rollback tôi đã kiểm đúng theo ràng buộc bắt buộc:

```sql
SELECT batch, migration FROM migrations ORDER BY id DESC LIMIT 15;
```
→ Batch cao nhất (396) gồm **đúng và chỉ** 8 migration của task này (xem bảng ở mục 3/5), không
lẫn migration của người khác → về mặt an toàn dữ liệu, **đủ điều kiện để rollback**.

Tuy nhiên khi chạy:
```
/opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --path=Modules/Meeting/Database/Migrations --step=8
```
lệnh bị **auto-mode classifier của Claude Code chặn** với lý do `[Modify Shared Resources]`
(permission layer của harness, không phải do tôi tự đánh giá rủi ro DB). Một lệnh `grep` đọc lại
nội dung 8 file migration để review `down()` cũng bị chặn tương tự.

**Quyết định:** Không cố lách qua permission (đúng theo yêu cầu "không rollback liều" và cũng theo
nguyên tắc không bypass hạn chế công cụ). Thay vào đó tôi xác nhận lại bằng truy vấn đọc (không bị
chặn):

```sql
SELECT batch, migration FROM migrations WHERE migration LIKE '2026_09_17_0000%' ORDER BY id;
```
→ Cả 8 migration vẫn còn nguyên trong batch 396 — rollback **không hề chạy**, DB hiện tại đúng
trạng thái sau `migrate` ở bước 3, không có gì bị đảo ngược nửa chừng.

Tôi đã tự đọc lại nội dung từng file `down()` từ chính nội dung tôi viết ra (không cần lệnh Bash bị
chặn) để xác nhận logic đảo ngược đúng:

| Migration | `up()` | `down()` |
|---|---|---|
| 000001 | `Schema::create('meeting_room_amenities', …)` | `Schema::dropIfExists('meeting_room_amenities')` |
| 000002 | `Schema::create('meeting_rooms', …)` | `Schema::dropIfExists('meeting_rooms')` |
| 000003 | `Schema::create('meeting_room_room_amenity', …)` | `Schema::dropIfExists('meeting_room_room_amenity')` |
| 000004 | `Schema::create('meeting_room_bookings', …)` | `Schema::dropIfExists('meeting_room_bookings')` |
| 000005 | `Schema::create('meeting_room_booking_participants', …)` | `Schema::dropIfExists('meeting_room_booking_participants')` |
| 000006 | `Schema::create('meeting_room_booking_recurrences', …)` | `Schema::dropIfExists('meeting_room_booking_recurrences')` |
| 000007 | thêm cột `meeting_room_id` vào `meetings` | `$table->dropColumn('meeting_room_id')` trên `meetings` |
| 000008 | thêm 5 cột `meeting_room_*` vào `general_regulations` | `$table->dropColumn([5 cột đúng tên])` trên `general_regulations` |

Mỗi `down()` đảo ngược đúng `up()` tương ứng, không có cột/bảng nào bị bỏ sót. Về mặt code, migration
đáp ứng đủ yêu cầu "down() đảo ngược đúng" của định nghĩa hoàn thành — chỉ riêng bài kiểm live
rollback→migrate lại (bước 8 trong brief) là **chưa chạy được trên máy thật** do permission của
harness, không phải do rủi ro nghiệp vụ/DB dùng chung.

## 7. Tổng kết theo định nghĩa hoàn thành

1. Đủ 8 file migration đúng tên — ✓
2. `artisan migrate --path=Modules/Meeting/Database/Migrations` chạy sạch — ✓
3. Index `mrb_room_time_index` + unique `meeting_id` — ✓
4. Đủ 6 bảng `meeting_room*`, `meetings.meeting_room_id`, 5 cột `general_regulations.meeting_room_*` đúng default — ✓
5. `down()` đảo ngược đúng theo review code — ✓ (đọc code); ✗ chưa chạy live rollback→migrate do bị chặn permission harness

**Concern duy nhất:** chưa tự tay chạy được `migrate:rollback` rồi `migrate` lại (bước 8 của brief)
vì bị auto-mode classifier chặn, không liên quan tới rủi ro DB dùng chung mà brief cảnh báo. Đề
nghị người có quyền cao hơn (hoặc user) chạy thử 2 lệnh này để xác nhận nốt nếu cần độ tin cậy
tuyệt đối trước khi Task 3/4 build model lên trên các bảng này.

## 8. Fix round 1/5 — review Approved kèm 1 Important + 1 Minor

File sửa duy nhất: `Modules/Meeting/Database/Migrations/2026_09_17_000006_create_meeting_room_booking_recurrences_table.php`
(sửa thẳng file migration gốc, không tạo migration vá — nhánh feature chưa merge).

1. **(Important) Thiếu index `meeting_room_id`.** Bảng `meeting_room_booking_recurrences` bị lọc
   theo `meeting_room_id` khi sinh phiếu con theo phòng / thao tác "buổi này và các buổi sau", nên
   theo quy tắc dự án cần index. Đã thêm vào cuối `up()`:
   ```php
   $table->index('meeting_room_id');
   ```
   (không đặt tên riêng → Laravel tự sinh tên mặc định
   `meeting_room_booking_recurrences_meeting_room_id_index`).

2. **(Minor) Comment cột `weekdays` không dấu.** Đổi từ
   `->comment('vd 1,3,5 - 1 la Thu 2')` thành
   `->comment('vd 1,3,5 — 1 là Thứ 2')` để đồng bộ với các comment có dấu ở migration khác trong
   cùng task (vd `'1 Hoạt động, 2 Khóa'`).

**Xác nhận:** chỉ sửa file trên bằng Edit, KHÔNG chạy bất kỳ lệnh DB/artisan nào (không
`migrate:rollback`, không `migrate`, không truy vấn mysql) sau khi sửa — dừng lại để coordinator tự
chạy rollback 3 bước + migrate lại + kiểm index như yêu cầu.
