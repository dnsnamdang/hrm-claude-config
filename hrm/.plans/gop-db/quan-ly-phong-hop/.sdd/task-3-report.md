# Task 3 — Báo cáo: Entity + unit test cho logic cấu hình hiệu lực

## Files đã tạo (đúng scope cho phép)
- `hrm-api/Modules/Meeting/Entities/MeetingRoomAmenity.php` (worktree: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api/Modules/Meeting/Entities/MeetingRoomAmenity.php`)
- `hrm-api/Modules/Meeting/Entities/MeetingRoom.php` (worktree: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api/Modules/Meeting/Entities/MeetingRoom.php`)
- `hrm-api/tests/Unit/MeetingRoomConfigTest.php` (worktree: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api/tests/Unit/MeetingRoomConfigTest.php`)

Không đụng file nào khác (git status trong worktree chỉ thấy `modules_statuses.json` đã M sẵn từ trước,
không phải do task này sửa).

## TDD — bằng chứng lần chạy ĐỎ (trước khi có entity)

Lệnh chạy: `cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomConfigTest`

```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

EE                                                                  2 / 2 (100%)

Time: 00:00.598, Memory: 48.50 MB

There were 2 errors:

1) Tests\Unit\MeetingRoomConfigTest::test_cau_hinh_phong_de_trong_thi_lay_cua_cong_ty
Error: Class 'Modules\Meeting\Entities\MeetingRoom' not found

/Users/dnsnamdang/.../hrm-worktrees/phong-hop-api/tests/Unit/MeetingRoomConfigTest.php:12

2) Tests\Unit\MeetingRoomConfigTest::test_phong_khac_cong_ty_chi_dat_duoc_khi_bat_co_lien_cong_ty
Error: Class 'Modules\Meeting\Entities\MeetingRoom' not found

/Users/dnsnamdang/.../hrm-worktrees/phong-hop-api/tests/Unit/MeetingRoomConfigTest.php:24

ERRORS!
Tests: 2, Assertions: 0, Errors: 2.
```

Đúng như kỳ vọng của brief: fail vì `MeetingRoom` chưa tồn tại.

## Sau khi viết 2 entity — bằng chứng lần chạy XANH

```
PHPUnit 9.6.34 by Sebastian Bergmann and contributors.

..                                                                  2 / 2 (100%)

Time: 00:01.081, Memory: 46.50 MB

OK (2 tests, 7 assertions)
```

2/2 test pass, 7 assertion — khớp brief.

## Đối chiếu cột $fillable với schema thật (SHOW COLUMNS trên DB `hrm_erp`)

### `meeting_room_amenities`
```
id, code, name, icon, sort_order, status, created_by, updated_by, created_at, updated_at
```
`$fillable` khai: `code, name, icon, sort_order, status, created_by, updated_by` — đủ toàn bộ cột
non-timestamp/non-PK, khớp brief.

### `meeting_rooms`
```
id, code, name, company_id, department_id, part_id, allow_cross_company, location, capacity,
manager_employee_id, require_approval, open_time, close_time, checkin_grace_minutes,
checkin_qr_token, description, status, created_by, updated_by, created_at, updated_at
```
`$fillable` khai đủ: `code, name, company_id, department_id, part_id, allow_cross_company, location,
capacity, manager_employee_id, require_approval, open_time, close_time, checkin_grace_minutes,
checkin_qr_token, description, status, created_by, updated_by` — khớp 1-1 với cột thật (trừ id/timestamps
tự quản lý).

## Audit grep (bước 6 của brief)

```
$ grep -n "extends BaseModel\|created_by" Modules/Meeting/Entities/*.php
Modules/Meeting/Entities/MeetingRoomAmenity.php:7:class MeetingRoomAmenity extends BaseModel
Modules/Meeting/Entities/MeetingRoomAmenity.php:15:        'code', 'name', 'icon', 'sort_order', 'status', 'created_by', 'updated_by',
Modules/Meeting/Entities/MeetingRoom.php:8:class MeetingRoom extends BaseModel
Modules/Meeting/Entities/MeetingRoom.php:19:        'description', 'status', 'created_by', 'updated_by',
```

Cả 2 entity đều `extends BaseModel`, cả 2 đều có `created_by`/`updated_by` trong `$fillable`.

## Ghi chú tuân thủ

- Không `git commit`/`push`/`stash`/`checkout`.
- Không chạy migrate/seed/rollback.
- Hook sinh `checkin_qr_token` đặt ở `protected static function booted()` (không override `boot()`),
  đúng ghi chú của người điều phối về `BaseModel::boot()` đã tự gán `created_by`/`updated_by`.
- `company_id` không được set cứng trong entity Task 3 — để `BaseModel` tự điền từ
  `auth()->user()->info->company_id` khi trống, đúng hành vi đã ghi trong ghi chú điều phối; Task 6 sẽ
  đặt `company_id` là `required` ở Request khi người dùng chọn công ty thủ công.

## Kết quả

STATUS: DONE — 2/2 test pass (7 assertions), cả 2 entity đúng interface brief yêu cầu, không có
concern nào phát sinh.
