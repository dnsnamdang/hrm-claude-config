# Quản lý phòng họp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development`
> (khuyến nghị) hoặc `superpowers:executing-plans` để thực thi từng task. Các bước dùng checkbox `- [ ]`.

**Goal:** Dựng phần Quản lý phòng họp trong phân hệ Meeting — khai báo phòng, đặt phòng gắn với phiếu
Meeting, màn theo dõi tình trạng phòng, check-in, báo cáo hiệu quả.

**Architecture:** Module BE mới `Modules/Meeting`; bảng `meeting_room_bookings` là **nguồn duy nhất**
giữ chỗ và kiểm tra trùng; phiếu Meeting chọn phòng thì service tự sinh/cập nhật booking. FE ở
`pages/meeting/`, một bộ API dùng chung cho web và app mobile (BE trả cờ hành động, thời gian ISO-8601).

**Tech Stack:** PHP 7.4 · Laravel 8 · nwidart/laravel-modules · spatie/laravel-permission ·
MySQL (DB gộp `hrm_erp`) · Nuxt 2.14 (Vue 2) · Bootstrap-Vue · Playwright (Node 20).

**Spec:** `docs/superpowers/specs/gop-db/2026-09-17-quan-ly-phong-hop-design.md`

## Global Constraints

- **Nhánh `gop_db`** ở cả 2 repo. KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`. Tài liệu ghi về
  `.plans/gop-db/quan-ly-phong-hop/`.
- **KHÔNG commit, KHÔNG push git** (quy tắc dự án). Mỗi task kết thúc bằng bước tự kiểm, không phải commit.
- **Line ending**: nhiều file `hrm-client` là CRLF. Sửa file nào thì giữ nguyên EOL của file đó; sau khi
  sửa bằng script phải chạy `git diff --numstat` kiểm tra, số dòng xóa bất thường = đã phá EOL.
- **Model mới BẮT BUỘC `extends App\Models\BaseModel`**, `created_by`/`updated_by` nằm trong `$fillable`.
- **Danh mục dùng cột `status`** (1 Hoạt động · 2 Khóa) theo khuôn `MeetingCancelReason`, KHÔNG dùng `is_active`.
- **FE màn mới: mọi element form dùng `V2Base*`**, cấm HTML thô. Select trong modal dùng `V2BaseSelectInModal`.
- **Cờ quyền FE khởi tạo `false`**, chỉ bật từ `$store.state.permissions`. Cấm gán literal `true`.
- **Nút không dùng được thì ẩn hẳn**, không disable — ở **cả** dòng danh sách lẫn footer màn chi tiết.
- **Số định dạng `1,234.56`** (`toLocaleString('en-US')`). Cấm `toLocaleString('vi-VN')` cho số.
- **Chữ đỏ chỉ dành cho lỗi validate**; text phụ dùng xám `#6b7280` (KHÔNG dùng `.text-muted` — class này
  trong hrm-client là màu ĐỎ).
- **Chạy lệnh**:
  - BE: `/opt/homebrew/opt/php@7.4/bin/php artisan …` (trong `hrm-api`)
  - PHPUnit: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter <TênTest>`
  - e2e: `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test <spec> --workers=1`
  - Playwright MCP luôn mở `http://127.0.0.1:3000`, KHÔNG dùng `localhost:3000`
- **Task đụng giao diện phải mở Playwright kiểm bằng SỐ ĐO LẤY TỪ DOM trước khi báo xong.**
  Bộ e2e chạy `serial`: một ca đỏ làm các ca sau in "did not run" — phải đọc dòng tổng kết.

---

# PHASE 1 — Nền tảng + danh mục

Kết quả nghiệm thu: khai báo được phòng họp và tiện nghi, khóa/mở khóa, phân quyền chạy đúng,
menu phân hệ Meeting hết mục treo trống ở nhóm Danh mục.


> **Ghi chú đối chiếu thực tế (18/09/2026)** — 4 bước dưới đây KHÔNG chạy đúng như viết trong plan, đã có
> ruling ghi ở `.sdd/progress.md`:
> - **Task 2 bước 8** (rollback kiểm `down()`): implementer bị chặn quyền → **người điều phối tự chạy**
>   (`migrate:rollback --step=8` rồi `migrate` lại), kết quả xác nhận `down()` đúng.
> - **Task 4 bước 3** (`db:seed PermissionsTableSeeder`): **KHÔNG chạy** (Ruling R7) — seeder xoá mọi quyền
>   `guard_name='api'` rồi tạo lại, mà DB đang có **472 quyền seeder không khai**. Thay bằng INSERT có chủ đích
>   5 quyền + cấp cho role Super admin. File seeder vẫn được sửa để lúc deploy chạy đúng.
> - **Task 8 bước 5b** (nút "Xem lịch phòng"): **hoãn sang Phase 3** — màn `/meeting/room-board` chưa tồn tại,
>   thêm nút bây giờ là nút chết.
> - **Task 10 ca khuôn giao diện**: code mẫu trong plan (Ruling R2) nhắm `.modal-body` — phần tử này **không
>   cuộn** (`overflow-y: hidden`), phần tử cuộn thật là `.v2-modal-body`. Đã sửa lúc thực thi, nếu không ca
>   test sẽ xanh giả.
> - Ngoài ra thêm **Task 4b** (dựng đường đăng nhập e2e cho worktree) vì hạ tầng e2e của dự án hỏng sẵn trên
>   DB gộp — xem mục Task 4b ở trên.


## File Structure (Phase 1)

**hrm-api**
```
Modules/Meeting/
├── module.json · composer.json
├── Providers/MeetingServiceProvider.php · RouteServiceProvider.php
├── Routes/api.php                                   ← toàn bộ route phân hệ
├── Database/Migrations/                             ← 6 bảng + 2 alter
├── Entities/MeetingRoomAmenity.php
├── Entities/MeetingRoom.php
├── Http/Controllers/Api/V1/MeetingRoomAmenityController.php
├── Http/Controllers/Api/V1/MeetingRoomController.php
├── Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php
├── Http/Requests/MeetingRoom/MeetingRoomRequest.php
├── Services/MeetingRoomAmenityService.php
├── Services/MeetingRoomService.php
└── Transformers/MeetingRoom{,Amenity}/…Resource.php
tests/Unit/MeetingRoomConfigTest.php                 ← unit test logic thuần
Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php   ← +5 quyền (id 1574-1578)
```

**hrm-client**
```
pages/meeting/room-amenities/index.vue
pages/meeting/room-amenities/components/RoomAmenityModal.vue
pages/meeting/rooms/index.vue
pages/meeting/rooms/components/MeetingRoomModal.vue
components/subsystem-menu/meeting.js                 ← điền link + thêm mục
```

**e2e**
```
tests/meeting/room-amenity.api.spec.ts
tests/meeting/meeting-room.api.spec.ts
tests/meeting/meeting-room.spec.ts                   ← UI
```

---

## Task 1: Tạo module `Modules/Meeting`

**Files:**
- Create: `hrm-api/Modules/Meeting/**` (sinh bằng artisan)
- Modify: `hrm-api/Modules/Meeting/Routes/api.php`

**Interfaces:**
- Consumes: —
- Produces: prefix route `/api/v1/meeting/...` nạp được; namespace `Modules\Meeting\…`

- [x] **Bước 1: Sinh module**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan module:make Meeting
```

- [x] **Bước 2: Dọn phần thừa**

Xóa `Modules/Meeting/Resources/assets`, `Modules/Meeting/Resources/views`, `webpack.mix.js`,
`package.json` (module này chỉ có API, không có asset FE). Giữ `Config`, `Database`, `Entities`,
`Http`, `Providers`, `Routes`, `Services`, `Transformers`, `Tests`.

- [x] **Bước 3: Khai route prefix giống module khác**

Mở `Modules/Meeting/Routes/api.php`, thay nội dung mặc định bằng khung rỗng đúng chuẩn dự án
(xem `Modules/Assign/Routes/api.php:1-20` để copy phần `Route::group` + middleware auth):

```php
<?php

use Illuminate\Support\Facades\Route;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Danh mục tiện nghi phòng họp + danh mục phòng họp khai ở Task 5, Task 6
});
```

- [x] **Bước 4: Kiểm module đã nạp**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan module:list | grep -i meeting
/opt/homebrew/opt/php@7.4/bin/php artisan route:list --path=meeting | head
```
Kỳ vọng: `Meeting` xuất hiện trong `module:list` (Enabled).

⚠️ Nếu `config:cache` đang trỏ production (bẫy đã biết của repo) thì chạy
`/opt/homebrew/opt/php@7.4/bin/php artisan config:clear` trước, nếu không artisan đọc nhầm DB.

- [x] **Bước 5: Tự kiểm** — `git status` ở `hrm-api` chỉ thấy file trong `Modules/Meeting/`, không đụng file khác.

---

## Task 2: Migration 6 bảng + 2 alter

**Files:**
- Create: `hrm-api/Modules/Meeting/Database/Migrations/2026_09_17_000001_create_meeting_room_amenities_table.php`
- Create: `…000002_create_meeting_rooms_table.php`
- Create: `…000003_create_meeting_room_room_amenity_table.php`
- Create: `…000004_create_meeting_room_bookings_table.php`
- Create: `…000005_create_meeting_room_booking_participants_table.php`
- Create: `…000006_create_meeting_room_booking_recurrences_table.php`
- Create: `…000007_add_meeting_room_id_to_meetings_table.php`
- Create: `…000008_add_meeting_room_config_to_general_regulations_table.php`

**Interfaces:**
- Produces: 6 bảng mới, cột `meetings.meeting_room_id`, 5 cột cấu hình trong `general_regulations`

> Tạo **cả 6 bảng ngay phase 1** (kể cả bảng booking chưa dùng tới) vì `MeetingRoom::isCanDelete()`
> ở Task 4 phải truy vấn `meeting_room_bookings`.

- [x] **Bước 1: Viết migration bảng tiện nghi**

```php
Schema::create('meeting_room_amenities', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->string('code', 50)->unique();
    $table->string('name', 255);
    $table->string('icon', 100)->nullable();
    $table->integer('sort_order')->default(0);
    $table->tinyInteger('status')->default(1)->comment('1 Hoạt động, 2 Khóa');
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();
});
```

- [x] **Bước 2: Viết migration bảng phòng họp**

```php
Schema::create('meeting_rooms', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->string('code', 50);
    $table->string('name', 255);
    $table->unsignedBigInteger('company_id');
    $table->unsignedBigInteger('department_id')->nullable();
    $table->unsignedBigInteger('part_id')->nullable();
    $table->tinyInteger('allow_cross_company')->default(0);
    $table->string('location', 255)->nullable();
    $table->integer('capacity')->nullable();
    $table->unsignedBigInteger('manager_employee_id')->nullable();
    $table->tinyInteger('require_approval')->default(0);
    $table->time('open_time')->nullable();
    $table->time('close_time')->nullable();
    $table->integer('checkin_grace_minutes')->nullable();
    $table->char('checkin_qr_token', 36)->nullable()->unique();
    $table->text('description')->nullable();
    $table->tinyInteger('status')->default(1)->comment('1 Hoạt động, 2 Khóa');
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();

    $table->unique(['company_id', 'code']);
    $table->index(['company_id', 'status']);
});
```

- [x] **Bước 3: Viết migration pivot**

```php
Schema::create('meeting_room_room_amenity', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('meeting_room_id');
    $table->unsignedBigInteger('meeting_room_amenity_id');
    $table->integer('quantity')->default(1);
    $table->string('note', 255)->nullable();
    $table->unique(['meeting_room_id', 'meeting_room_amenity_id'], 'mr_amenity_unique');
});
```

- [x] **Bước 4: Viết migration bảng phiếu đặt phòng**

Đủ cột theo spec mục 4.4 (`code`, `meeting_room_id`, `title`, `content`, `start_at`, `end_at`,
`status`, `booked_by_employee_id`, `host_employee_id`, `attendee_count`, `company_id`,
`department_id`, `meeting_id` unique nullable, `source`, `approved_by`, `approved_at`,
`reject_reason`, `is_auto_rejected`, `cancelled_by`, `cancelled_at`, `cancel_reason`,
`checkin_at`, `checkout_at`, `auto_released_at`, `checkout_reminded_at`, `recurrence_id`,
`created_by`, `updated_by`, `timestamps`) kèm index:

```php
$table->index(['meeting_room_id', 'start_at', 'end_at'], 'mrb_room_time_index');
$table->index('status');
$table->index('booked_by_employee_id');
$table->unique('meeting_id');
$table->index('recurrence_id');
```

- [x] **Bước 5: Viết 2 migration còn lại + 2 alter**

```php
// participants
Schema::create('meeting_room_booking_participants', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('meeting_room_booking_id');
    $table->unsignedBigInteger('employee_id');
    $table->timestamps();
    $table->unique(['meeting_room_booking_id', 'employee_id'], 'mrbp_unique');
});

// meetings
Schema::table('meetings', function (Blueprint $table) {
    $table->unsignedBigInteger('meeting_room_id')->nullable()->after('location');
});

// general_regulations
Schema::table('general_regulations', function (Blueprint $table) {
    $table->time('meeting_room_open_time')->nullable()->default('07:00:00');
    $table->time('meeting_room_close_time')->nullable()->default('20:00:00');
    $table->integer('meeting_room_checkin_grace_minutes')->nullable()->default(15);
    $table->integer('meeting_room_checkout_reminder_minutes')->nullable()->default(10);
    $table->integer('meeting_room_max_advance_days')->nullable()->default(90);
});
```

Bảng `meeting_room_booking_recurrences` theo spec mục 4.6.

- [x] **Bước 6: Chạy migration**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan config:clear
/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/Meeting/Database/Migrations
```
Kỳ vọng: 8 migration chạy OK, không lỗi.

- [x] **Bước 7: Kiểm bảng có thật + đúng index**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" hrm_erp -e "SHOW CREATE TABLE meeting_room_bookings\G" | grep -i "KEY"
```
Kỳ vọng: thấy `mrb_room_time_index (meeting_room_id, start_at, end_at)` và unique `meeting_id`.

- [x] **Bước 8: Kiểm rollback không hỏng**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --path=Modules/Meeting/Database/Migrations --step=8
/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/Meeting/Database/Migrations
```
Kỳ vọng: rollback sạch rồi migrate lại được (mọi `down()` phải `dropColumn`/`dropIfExists` đúng).

---

## Task 3: Entity + unit test cho logic cấu hình hiệu lực

**Files:**
- Create: `hrm-api/Modules/Meeting/Entities/MeetingRoomAmenity.php`
- Create: `hrm-api/Modules/Meeting/Entities/MeetingRoom.php`
- Test: `hrm-api/tests/Unit/MeetingRoomConfigTest.php`

**Interfaces:**
- Produces:
  - `MeetingRoom::STATUS_ACTIVE = 1`, `STATUS_INACTIVE = 2`
  - `MeetingRoom::resolveConfig(?$roomValue, $companyValue, $fallback)` — static, thuần
  - `MeetingRoom::canBeBookedByCompany(int $roomCompanyId, int $allowCrossCompany, int $bookerCompanyId): bool` — static, thuần
  - `$room->effectiveOpenTime($companyOpenTime)`, `effectiveCloseTime(...)`, `effectiveCheckinGrace(...)`
  - `$room->isCanEdit()`, `isCanLockUpdate()`, `isCanDelete()`, `upcomingBookingCount()`

> Hai method static để **test thuần không cần DB** — đúng khuôn `tests/Unit/WorkCalendarServiceOverlapTest.php`
> đang có trong repo.

- [x] **Bước 1: Viết test đỏ**

```php
<?php
namespace Tests\Unit;

use Tests\TestCase;
use Modules\Meeting\Entities\MeetingRoom;

class MeetingRoomConfigTest extends TestCase
{
    public function test_cau_hinh_phong_de_trong_thi_lay_cua_cong_ty()
    {
        // phòng khai riêng -> ưu tiên phòng
        $this->assertSame('08:00:00', MeetingRoom::resolveConfig('08:00:00', '07:00:00', '07:00:00'));
        // phòng để trống -> lấy công ty
        $this->assertSame('07:00:00', MeetingRoom::resolveConfig(null, '07:00:00', '06:00:00'));
        // công ty cũng trống -> lấy mặc định hệ thống
        $this->assertSame('06:00:00', MeetingRoom::resolveConfig(null, null, '06:00:00'));
        // số 0 là giá trị HỢP LỆ (ân hạn 0 phút = không ân hạn), không được coi là "trống"
        $this->assertSame(0, MeetingRoom::resolveConfig(0, 15, 15));
    }

    public function test_phong_khac_cong_ty_chi_dat_duoc_khi_bat_co_lien_cong_ty()
    {
        // cùng công ty -> luôn được
        $this->assertTrue(MeetingRoom::canBeBookedByCompany(1, 0, 1));
        // khác công ty, cờ tắt -> chặn
        $this->assertFalse(MeetingRoom::canBeBookedByCompany(1, 0, 2));
        // khác công ty, cờ bật -> cho
        $this->assertTrue(MeetingRoom::canBeBookedByCompany(1, 1, 2));
    }
}
```

- [x] **Bước 2: Chạy test, xác nhận ĐỎ**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomConfigTest
```
Kỳ vọng: FAIL — `Class "Modules\Meeting\Entities\MeetingRoom" not found`.

- [x] **Bước 3: Viết `MeetingRoomAmenity`**

```php
<?php

namespace Modules\Meeting\Entities;

use App\Models\BaseModel;

class MeetingRoomAmenity extends BaseModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 2;

    protected $table = 'meeting_room_amenities';

    protected $fillable = [
        'code', 'name', 'icon', 'sort_order', 'status', 'created_by', 'updated_by',
    ];

    public function rooms()
    {
        return $this->belongsToMany(
            MeetingRoom::class,
            'meeting_room_room_amenity',
            'meeting_room_amenity_id',
            'meeting_room_id'
        );
    }

    public function isCanEdit()
    {
        return $this->status == self::STATUS_ACTIVE;
    }

    public function isCanLockUpdate()
    {
        return $this->status == self::STATUS_ACTIVE;
    }

    /** Tiện nghi đang gắn cho phòng nào thì không xóa được, chỉ Khóa */
    public function isCanDelete()
    {
        return !$this->rooms()->exists();
    }
}
```

- [x] **Bước 4: Viết `MeetingRoom` (phần logic thuần trước)**

```php
<?php

namespace Modules\Meeting\Entities;

use App\Models\BaseModel;
use Illuminate\Support\Str;

class MeetingRoom extends BaseModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 2;

    protected $table = 'meeting_rooms';

    protected $fillable = [
        'code', 'name', 'company_id', 'department_id', 'part_id', 'allow_cross_company',
        'location', 'capacity', 'manager_employee_id', 'require_approval',
        'open_time', 'close_time', 'checkin_grace_minutes', 'checkin_qr_token',
        'description', 'status', 'created_by', 'updated_by',
    ];

    /**
     * Sinh sẵn token QR ngay khi tạo phòng (phase 5 dùng để check-in bằng cách quét mã dán
     * trước cửa). Sinh ở đây thay vì lúc cần: thêm sau đồng nghĩa phải in và dán lại QR ngoài đời.
     */
    protected static function booted()
    {
        static::creating(function (self $room) {
            if (empty($room->checkin_qr_token)) {
                $room->checkin_qr_token = (string) Str::uuid();
            }
        });
    }

    /**
     * Giá trị cấu hình có hiệu lực: phòng khai riêng -> công ty -> mặc định hệ thống.
     * Dùng `null` làm dấu "chưa khai" — KHÔNG dùng `empty()`, vì ân hạn 0 phút là giá trị hợp lệ.
     */
    public static function resolveConfig($roomValue, $companyValue, $fallback)
    {
        if ($roomValue !== null && $roomValue !== '') {
            return $roomValue;
        }
        if ($companyValue !== null && $companyValue !== '') {
            return $companyValue;
        }

        return $fallback;
    }

    public static function canBeBookedByCompany($roomCompanyId, $allowCrossCompany, $bookerCompanyId)
    {
        if ((int) $roomCompanyId === (int) $bookerCompanyId) {
            return true;
        }

        return (int) $allowCrossCompany === 1;
    }

    public function amenities()
    {
        return $this->belongsToMany(
            MeetingRoomAmenity::class,
            'meeting_room_room_amenity',
            'meeting_room_id',
            'meeting_room_amenity_id'
        )->withPivot(['quantity', 'note']);
    }

    public function effectiveOpenTime($companyOpenTime)
    {
        return self::resolveConfig($this->open_time, $companyOpenTime, '07:00:00');
    }

    public function effectiveCloseTime($companyCloseTime)
    {
        return self::resolveConfig($this->close_time, $companyCloseTime, '20:00:00');
    }

    public function effectiveCheckinGrace($companyGrace)
    {
        return (int) self::resolveConfig($this->checkin_grace_minutes, $companyGrace, 15);
    }

    public function isCanEdit()
    {
        return $this->status == self::STATUS_ACTIVE;
    }

    public function isCanLockUpdate()
    {
        return $this->status == self::STATUS_ACTIVE;
    }

    /** Chỉ xóa được phòng CHƯA từng có phiếu đặt — đã có lịch sử thì chỉ được Khóa */
    public function isCanDelete()
    {
        return !\DB::table('meeting_room_bookings')->where('meeting_room_id', $this->id)->exists();
    }

    /** Số phiếu sắp tới — dùng để cảnh báo trước khi Khóa phòng */
    public function upcomingBookingCount()
    {
        return \DB::table('meeting_room_bookings')
            ->where('meeting_room_id', $this->id)
            ->whereIn('status', [1, 2])
            ->where('start_at', '>=', now())
            ->count();
    }
}
```

- [x] **Bước 5: Chạy test, xác nhận XANH**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomConfigTest
```
Kỳ vọng: OK (2 tests).

- [x] **Bước 6: Tự kiểm audit** — grep xác nhận cả 2 entity đều `extends BaseModel` và có
`created_by`/`updated_by` trong `$fillable`:

```bash
grep -n "extends BaseModel\|created_by" Modules/Meeting/Entities/*.php
```

---

## Task 4: Thêm 5 quyền vào seeder

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

**Interfaces:**
- Produces: 5 quyền — `Quản lý danh mục phòng họp`, `Xem danh mục phòng họp`,
  `Quản lý danh mục tiện nghi phòng họp`, `Xem danh mục tiện nghi phòng họp`,
  `Xem báo cáo hiệu quả sử dụng phòng họp` (id 1574–1578)

> ⚠️ Seeder **truncate cả bảng** rồi tạo lại → id mới phải nối tiếp id lớn nhất hiện tại là **1573**.
> Quyền `Xem tất cả phiếu đặt phòng họp` và `Duyệt phiếu đặt phòng họp` thuộc **Phase 2**, không thêm ở đây.

- [x] **Bước 1: Thêm 5 dòng vào nhóm `Danh mục`** (đặt ngay dưới dòng id 1185 — quyền danh mục lý do hủy cuộc họp)

```php
// Quản lý phòng họp (phân hệ Meeting) — id nối tiếp 1573 là id lớn nhất đang có
Permission::create(['id' => 1574, 'guard_name' => 'api', 'name' => 'Quản lý danh mục phòng họp', 'display_name' => 'Quản lý danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1575, 'guard_name' => 'api', 'name' => 'Xem danh mục phòng họp', 'display_name' => 'Xem danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1576, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tiện nghi phòng họp', 'display_name' => 'Quản lý danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1577, 'guard_name' => 'api', 'name' => 'Xem danh mục tiện nghi phòng họp', 'display_name' => 'Xem danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
Permission::create(['id' => 1578, 'guard_name' => 'api', 'name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'display_name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'group' => 'Báo cáo phòng họp', 'type' => 4]);
```

- [x] **Bước 2: Kiểm trùng id / trùng tên TRƯỚC khi chạy seeder**

```bash
grep -oE "'id' => 15[0-9]{2}" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort | uniq -d
grep -c "Quản lý danh mục phòng họp" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: lệnh 1 không in gì (không id trùng); lệnh 2 in `1`.

- [x] **Bước 3: Chạy seeder**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```
Kỳ vọng: chạy xong không lỗi khóa trùng.

- [x] **Bước 4: Cấp quyền cho role admin để test được**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" hrm_erp -e \
"SELECT id,name FROM permissions WHERE id BETWEEN 1574 AND 1578;"
```
Rồi gán vào `role_has_permissions` với **`company_id = 1`** (thiếu cột này quyền không ăn).

---

## Task 4b: Dựng đường đăng nhập e2e cho worktree (thêm 17/09/2026 — Ruling R6)

**Vì sao có task này:** bộ e2e của dự án **hỏng sẵn trên DB gộp**, không phải do worktree — `api-setup`
chết vì `Table 'hrm_erp.hrm_employees' doesn't exist`, tài khoản fixture `e2e_assign@test.local` không tồn
tại trong bảng `employees`, và token trong `.auth/api.json` / `.auth/user.json` trả **401 ở cả `:8000` lẫn
`:8001`** (token chưa hết hạn nhưng đã bị vô hiệu). Không sửa `e2e/auth/api.setup.ts` và
`database/e2e_provision.php` — tài sản dùng chung, phải qua PR.

**Files:**
- Create: `.plans/gop-db/quan-ly-phong-hop/.sdd/mint-auth.php` (script chạy qua tinker, KHÔNG nằm trong repo code)
- Create: `e2e/.auth/api-wt.json`
- Overwrite: `e2e/.auth/user-wt.json`, `e2e/.auth/user-nocost-wt.json` (đang giữ token chết)
- **KHÔNG đụng**: `e2e/.auth/api.json`, `user.json`, `user-nocost.json` (của phiên khác)

**Interfaces:**
- Produces: `e2e/.auth/api-wt.json` dạng `{ "token": "<JWT>", "employee_id": <id> }`;
  `user-wt.json` / `user-nocost-wt.json` là storageState hợp lệ cho origin `http://127.0.0.1:3001`

**Thông tin đã kiểm chứng sẵn — dùng luôn, đừng khảo sát lại:**
- Guard JWT dùng model **`App\Models\TpEmployee`** (`config/auth.php:44,70`).
- Phân quyền đọc qua `Employee::roles` + `role_has_permissions.company_id = auth()->user()->current_company_role`
  (`app/Helper/PermissionHelper.php:19-34`). Bảng `model_has_roles` **không tồn tại** trên DB gộp.
- Role nhiều quyền nhất: `Super admin` (id 18, 2464 quyền), kế tiếp `Admin_TPE` (id 19, 1892 quyền).
- Nuxt chỉ cần đúng 1 khoá `access_token` trong localStorage (kiểm từ `user.json` cũ).

- [x] **Bước 1: Chọn 2 tài khoản**

```sql
-- tài khoản CÓ quyền: phải thấy 'Quản lý danh mục phòng họp' (Task 4 đã seed + gán)
SELECT e.id, e.email, e.current_company_role FROM employees e
JOIN <bảng nối role của employee> ... WHERE p.name = 'Quản lý danh mục phòng họp' LIMIT 3;
-- tài khoản KHÔNG quyền: employee bất kỳ không nằm trong danh sách trên
```
Tự xác định tên bảng nối bằng cách đọc quan hệ `roles()` trong `Modules/Timesheet/Entities/Employee.php`
(KHÔNG đoán tên bảng — `model_has_roles` không có trên DB này).

- [x] **Bước 2: Viết script mint token**

```php
// .sdd/mint-auth.php — chạy bằng: php artisan tinker --execute="require '<đường dẫn tuyệt đối>';"
$ids = [/* id có quyền */, /* id không quyền */];
foreach ($ids as $id) {
    $u = \App\Models\TpEmployee::find($id);
    echo 'MINT=' . json_encode(['id' => $id, 'token' => \JWTAuth::fromUser($u)]) . PHP_EOL;
}
```

- [x] **Bước 3: Ghi 3 file auth** (`api-wt.json`, `user-wt.json`, `user-nocost-wt.json`).
  storageState đúng khuôn:

```json
{"cookies": [], "origins": [{"origin": "http://127.0.0.1:3001",
  "localStorage": [{"name": "access_token", "value": "<JWT>"}]}]}
```

- [x] **Bước 4: Kiểm token thật sự dùng được (API)**

```bash
TOK=$(python3 -c "import json,io;print(json.load(io.open('e2e/.auth/api-wt.json'))['token'])")
curl -s -o /dev/null -w "%{http_code}
" -H "Authorization: Bearer $TOK" -H "Accept: application/json" \
  http://127.0.0.1:8001/api/v1/assign/meeting_cancel_reasons
```
Kỳ vọng: **200**. Nếu vẫn 401 → BLOCKED, báo lại ngay, đừng tự tạo tài khoản mới trong DB dùng chung.

- [x] **Bước 5: Kiểm token dùng được ở UI** — Playwright mở `http://127.0.0.1:3001/meeting/dashboard` với
  `storageState: '.auth/user-wt.json'`, kỳ vọng **KHÔNG** bị đẩy về `/login` và có phần tử sidebar phân hệ.

- [x] **Bước 6: Ghi lại vào báo cáo** id + email của 2 tài khoản đã chọn, để các task sau dùng đúng.

---

## Task 5: API danh mục tiện nghi phòng họp

**Files:**
- Create: `Modules/Meeting/Services/MeetingRoomAmenityService.php`
- Create: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php`
- Create: `Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php`
- Create: `Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php`
- Create: `Modules/Meeting/Transformers/MeetingRoomAmenity/DetailMeetingRoomAmenityResource.php`
- Modify: `Modules/Meeting/Routes/api.php`
- Test: `e2e/tests/meeting/room-amenity.api.spec.ts`

**Interfaces:**
- Consumes: `MeetingRoomAmenity` (Task 3)
- Produces: `GET|POST /api/v1/meeting/room-amenities`, `GET /{id}`, `DELETE /{id}`,
  `GET /{id}/lock`, `GET /{id}/unlock`, `GET /getAll`

> **Copy nguyên khuôn** từ danh mục lý do hủy cuộc họp — 5 file tương ứng:
> `Modules/Assign/Services/MeetingCancelReasonService.php`,
> `Modules/Assign/Http/Controllers/Api/V1/MeetingCancelReasonController.php`,
> `Modules/Assign/Http/Requests/MeetingCancelReason/MeetingCancelReasonRequest.php`,
> `Modules/Assign/Transformers/MeetingCancelReason/*.php`.
> Khác 3 điểm: thêm trường `code` (unique) và `icon`, `sort_order`; `isCanDelete()` kiểm quan hệ `rooms()`;
> sắp xếp mặc định theo `sort_order` rồi `id`.

> **Ruling R1 (pre-flight):** `e2e/utils/` KHÔNG có helper `api` / `noPermApi` dùng chung — code mẫu dưới
> đây là mô tả ca kiểm, không phải code chạy nguyên văn. Mỗi spec **tự dựng `APIRequestContext`** theo khuôn
> `e2e/tests/assign/customer-demand-link.api.spec.ts` (đọc token từ `e2e/.auth/api.json`). Ca "không quyền"
> dùng tài khoản nocost có sẵn: `test.use({ storageState: '.auth/user-nocost.json' })` (sinh bởi
> `e2e/auth/login-nocost.setup.ts`). Nếu project `api-setup` đỏ trên DB gộp (bẫy đã biết: thiếu bảng
> `hrm_employees`) thì chạy spec lẻ bằng `--no-deps`.

- [x] **Bước 1: Viết e2e API spec (đỏ trước)**

`e2e/tests/meeting/room-amenity.api.spec.ts` — phủ 4 ca:

```ts
test('tạo - sửa - khóa - mở khóa tiện nghi', async () => {
    const created = await api.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_PROJ', name: 'Máy chiếu E2E', icon: 'ri-projector-line' },
    });
    expect(created.status()).toBe(200);
    const id = (await created.json()).data.id;

    const locked = await api.get(`/api/v1/meeting/room-amenities/${id}/lock`);
    expect(locked.status()).toBe(200);

    const detail = await (await api.get(`/api/v1/meeting/room-amenities/${id}`)).json();
    expect(detail.data.status).toBe(2);
});

test('trùng mã thì trả 422 kèm field code', async () => {
    const res = await api.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_PROJ', name: 'Trùng mã' },
    });
    expect(res.status()).toBe(422);
    expect(await res.text()).toContain('code');
});

test('không quyền thì 403', async () => {
    // dùng context đăng nhập bằng tài khoản KHÔNG có quyền quản lý danh mục
    const res = await noPermApi.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_X', name: 'X' },
    });
    expect(res.status()).toBe(403);
});
```

- [x] **Bước 2: Chạy spec, xác nhận ĐỎ**

```bash
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/meeting/room-amenity.api.spec.ts --workers=1
```
Kỳ vọng: FAIL 404 (route chưa có).

- [x] **Bước 3: Viết Service + Request + 2 Resource + Controller** theo khuôn đã nêu ở trên.

Request:

```php
public function rules()
{
    $id = $this->input('id');

    return [
        'code' => ['required', 'string', 'max:50', Rule::unique('meeting_room_amenities', 'code')->ignore($id)],
        'name' => ['required', 'string', 'max:255'],
        'icon' => ['nullable', 'string', 'max:100'],
        'sort_order' => ['nullable', 'integer', 'min:0'],
    ];
}
```

⚠️ Controller `updateOrCreate` phải **rethrow `ValidationException`** trước khi catch `Exception`
(xem `MeetingCancelReasonController.php:60-66`), nếu không FE mất thông tin field và không hiện được lỗi inline.

- [x] **Bước 4: Khai route**

```php
Route::group(['prefix' => 'meeting/room-amenities'], function () {
    Route::get('/getAll', [MeetingRoomAmenityController::class, 'getAll']);
    Route::get('/', [MeetingRoomAmenityController::class, 'index'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp');
    Route::post('/', [MeetingRoomAmenityController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'show']);
    Route::delete('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}/lock', [MeetingRoomAmenityController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}/unlock', [MeetingRoomAmenityController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
});
```

⚠️ Route `/getAll` phải đặt **TRƯỚC** route wildcard `/{meetingRoomAmenity}`, nếu không bị nuốt.

- [x] **Bước 5: Chạy lại spec, xác nhận XANH** (đọc dòng tổng kết, không nhìn cuối log).

---

## Task 6: API danh mục phòng họp

**Files:**
- Create: `Modules/Meeting/Services/MeetingRoomService.php`
- Create: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php`
- Create: `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php`
- Modify: `Modules/Meeting/Routes/api.php`
- Test: `e2e/tests/meeting/meeting-room.api.spec.ts`

**Interfaces:**
- Consumes: `MeetingRoom`, `MeetingRoomAmenity` (Task 3)
- Produces:
  - `GET /api/v1/meeting/rooms` (lọc `keyword`, `company_id`, `capacity_from`, `amenity_ids[]`, `status`)
  - `GET /api/v1/meeting/rooms/form-options` → `{ amenities: [], companies: [], config: { open_time, close_time, checkin_grace_minutes } }`
  - `POST /api/v1/meeting/rooms`, `GET /{id}`, `DELETE /{id}`, `GET /{id}/lock`, `GET /{id}/unlock`
  - `GET /api/v1/meeting/rooms/{id}/upcoming-bookings` → `{ count: n, items: [...] }`

- [x] **Bước 1: Viết e2e API spec (đỏ trước)** — 5 ca:

```ts
test('mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho', async () => {
    await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'P.A301', company_id: 1 } });
    const dup = await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'Khác', company_id: 1 } });
    expect(dup.status()).toBe(422);

    const other = await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'P.A301 CT2', company_id: 2 } });
    expect(other.status()).toBe(200);
});

test('tạo phòng là có sẵn checkin_qr_token', async () => {
    const res = await api.post('/api/v1/meeting/rooms', { data: { code: 'QR01', name: 'P.QR', company_id: 1 } });
    const id = (await res.json()).data.id;
    const detail = await (await api.get(`/api/v1/meeting/rooms/${id}`)).json();
    expect(detail.data.checkin_qr_token).toMatch(/^[0-9a-f-]{36}$/);
});

test('gắn nhiều tiện nghi rồi đọc lại đúng danh sách', async () => { /* post amenity_ids: [id1, id2] rồi GET detail */ });

test('form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty', async () => {
    const res = await (await api.get('/api/v1/meeting/rooms/form-options')).json();
    expect(res.data.config.open_time).toBeTruthy();
});

test('không quyền quản lý danh mục thì POST trả 403', async () => { /* noPermApi */ });
```

- [x] **Bước 2: Chạy spec, xác nhận ĐỎ.**

- [x] **Bước 3: Viết Request với unique theo công ty**

```php
'code' => [
    'required', 'string', 'max:50',
    Rule::unique('meeting_rooms', 'code')
        ->where(fn ($q) => $q->where('company_id', $this->input('company_id')))
        ->ignore($this->input('id')),
],
'name' => ['required', 'string', 'max:255'],
'company_id' => ['required', 'integer'],
'capacity' => ['nullable', 'integer', 'min:1'],
'manager_employee_id' => ['nullable', 'integer'],
'require_approval' => ['nullable', 'boolean'],
'allow_cross_company' => ['nullable', 'boolean'],
'open_time' => ['nullable', 'date_format:H:i:s'],
'close_time' => ['nullable', 'date_format:H:i:s', 'after:open_time'],
'checkin_grace_minutes' => ['nullable', 'integer', 'min:0', 'max:120'],
'amenity_ids' => ['nullable', 'array'],
'amenity_ids.*' => ['integer', 'exists:meeting_room_amenities,id'],
```

- [x] **Bước 4: Service — `updateOrCreate` đồng bộ pivot trong transaction**

```php
return DB::transaction(function () use ($request) {
    $room = MeetingRoom::updateOrCreate(['id' => $request->input('id')], $request->only([...]));
    $room->amenities()->sync($request->input('amenity_ids', []));

    return $room->load('amenities');
});
```

- [x] **Bước 5: Controller — `destroy` chặn xóa phòng đã có phiếu**

```php
if (!$meetingRoom->isCanDelete()) {
    return $this->responseJson(
        'Phòng họp này đã có phiếu đặt nên không xóa được. Bạn có thể Khóa phòng.',
        Response::HTTP_BAD_REQUEST
    );
}
```

- [x] **Bước 6: Controller — `upcomingBookings` phục vụ cảnh báo trước khi Khóa**

```php
public function upcomingBookings(MeetingRoom $meetingRoom)
{
    return $this->responseJson('success', Response::HTTP_OK, [
        'count' => $meetingRoom->upcomingBookingCount(),
        'items' => [], // Phase 2 trả chi tiết khi đã có Resource của phiếu
    ]);
}
```

- [x] **Bước 6b: Resource trả cờ hành động** — quy ước bắt buộc để app mobile không phải chép lại luật:

```php
'is_can_edit'   => $this->isCanEdit(),
'is_can_delete' => $this->isCanDelete(),
'is_can_lock'   => $this->isCanLockUpdate(),
'status_text'   => $this->status == MeetingRoom::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
```

⚠️ `isCanDelete()` truy vấn bảng phiếu → list phải `with('amenities')` và tính cờ theo lô, không gọi trong vòng lặp từng dòng (N+1).

- [x] **Bước 7: Khai route** (đặt `/form-options` và `/getAll` TRƯỚC wildcard), gắn
`checkPermission:Quản lý danh mục phòng họp` cho POST/DELETE/lock/unlock, và
`checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp` cho `index`.

- [x] **Bước 8: Chạy lại spec, xác nhận XANH.**

- [x] **Bước 9: Kiểm N+1** — bật `DB::enableQueryLog()` tạm hoặc đọc Telescope: `GET /rooms?per_page=50`
phải **không** sinh 50 query cho tiện nghi (bắt buộc `with('amenities')`).

---

---

## ⚠️ Thay đổi COMPONENT DÙNG CHUNG — đã được user duyệt (17/09/2026)

**File**: `hrm-client/components/modal/V2BaseModal.vue` — thêm method `hide()` là **alias của `close()`** (4 dòng, thuần bổ sung).

**Vì sao phải sửa**: CLAUDE.md bắt (a) mọi popup mới dựng trên `V2BaseModal`, và (b) mọi form cảnh báo khi
thoát lúc chưa lưu bằng `utils/mixins/unsavedModalMixin.js`. Mixin đó gọi `this.$refs[ref].hide()`
(dòng 171), trong khi `V2BaseModal` chỉ có `show()` / `close()`. Mixin viết
`if (modal && typeof modal.hide === 'function') modal.hide()` → thiếu method thì **bấm "Thoát" xong modal
đứng im, không đóng, không lỗi nào báo ra**. Đã tái hiện bằng Playwright trước khi sửa, không phải suy đoán.

**Vì sao trước đây không ai vấp**: khuôn modal cũ dùng thẳng `<b-modal ref="modal">` nên có sẵn `.hide()` của
BootstrapVue. Màn này là **modal đầu tiên trong repo kết hợp `V2BaseModal` + `unsavedModalMixin`**, nên lỗ
hổng bây giờ mới lộ.

**Phạm vi ảnh hưởng**: thuần thêm method mới, KHÔNG đổi `show()` / `close()` → ~30 popup đang dùng
`V2BaseModal` giữ nguyên hành vi.

**Việc cần làm khi merge**: nêu rõ thay đổi này trong mô tả PR để team biết `V2BaseModal` nay dùng được với
`unsavedModalMixin`; cân nhắc bổ sung 1 dòng vào `.claude/skills/modal-popup/SKILL.md` (tài sản chung, sửa
qua PR riêng).

## Task 7: FE màn Danh mục tiện nghi `/meeting/room-amenities`

**Files:**
- Create: `hrm-client/pages/meeting/room-amenities/index.vue`
- Create: `hrm-client/pages/meeting/room-amenities/components/RoomAmenityModal.vue`

**Interfaces:**
- Consumes: API Task 5
- Produces: màn danh mục chạy được, dùng làm khuôn cho Task 8

> **Copy khuôn** từ `hrm-client/pages/assign/meeting_cancel_reason/index.vue` (bảng + bộ lọc + modal +
> khóa/mở khóa + xác nhận xóa). Gọi API bằng `this.$store.dispatch('apiGet' | 'apiPostMethod' | 'apiDelete', …)`
> đúng như file gốc (dòng 543, 648, 668, 838).

- [x] **Bước 1: Dựng trang danh sách** — `layout: 'default-sidebar'`, cột: Mã · Tên tiện nghi · Icon ·
  Thứ tự · Trạng thái · Người cập nhật · Hành động.
  Badge trạng thái dùng `V2BaseBadge` với `variant` (`brand` = Hoạt động, `required` = Khóa) — đây là
  danh mục dùng chung 2 trạng thái cố định nên **không cần BE trả màu**.

- [x] **Bước 2: Cờ quyền fail-closed**

```js
data() {
    return {
        canManage: false,   // KHÔNG được gán true
        canView: false,
    }
},
mounted() {
    const perms = this.$store.state.permissions || []
    this.canManage = perms.includes('Quản lý danh mục tiện nghi phòng họp')
    this.canView = this.canManage || perms.includes('Xem danh mục tiện nghi phòng họp')
}
```

- [x] **Bước 3: Modal thêm/sửa** dựng trên `components/modal/V2BaseModal.vue`; các ô:
  `V2BaseInput` (Mã, Tên), `V2BaseSelectInModal` (Icon), `V2BaseInput` số (Thứ tự).
  Nút Xóa dùng `components/modal/base-confirm-modal.vue`, **không** tạo confirm riêng.

- [x] **Bước 4: Tự kiểm không có HTML thô**

```bash
cd hrm-client
grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/room-amenities/ | grep -v V2Base
```
Kỳ vọng: **rỗng**.

- [x] **Bước 5: Kiểm trên trình duyệt thật bằng Playwright MCP** — mở
`http://127.0.0.1:3000/meeting/room-amenities`, tạo 1 bản ghi, khóa, mở khóa, xóa.
Đo bằng số lấy từ DOM (số dòng bảng trước/sau khi tạo), không chỉ nhìn ảnh.

---

## Task 8: FE màn Danh sách phòng họp `/meeting/rooms`

**Files:**
- Create: `hrm-client/pages/meeting/rooms/index.vue`
- Create: `hrm-client/pages/meeting/rooms/components/MeetingRoomModal.vue`

**Interfaces:**
- Consumes: API Task 6 (`/meeting/rooms`, `/form-options`, `/{id}/upcoming-bookings`)

- [x] **Bước 1: Trang danh sách** — cột: Mã · Tên phòng · Công ty · Vị trí · Sức chứa · Tiện nghi (chip) ·
  Người quản lý · Cần duyệt · Cho công ty khác đặt · Trạng thái · Hành động.
  Sức chứa hiển thị bằng `Number(x).toLocaleString('en-US')`.

- [x] **Bước 2: Bộ lọc** — Tìm nhanh placeholder `Tìm theo mã, tên phòng, vị trí`; các ô lọc còn lại
  (công ty, sức chứa tối thiểu, tiện nghi, trạng thái) theo chế độ gọn có nhãn floating → **bỏ placeholder
  trùng nhãn**.

- [x] **Bước 3: Modal thêm/sửa** — 1 request `GET /meeting/rooms/form-options` lúc mở modal
  (KHÔNG gọi ở `mounted`, KHÔNG bắn nhiều API rời rạc).
  - Tiện nghi: `V2BaseSelectInModal` chọn nhiều
  - Người quản lý: select nhân viên, nhãn theo khuôn chuẩn `utils/employeeOptionText.js`
    (`Tên nhân viên - Mã phòng - Mã nhân viên`)
  - Bố cục mỗi hàng đủ 12 cột, không để ô lẻ một dòng
  - Khối nhóm dùng `components/V2BaseFormSection.vue`

- [x] **Bước 4: Cảnh báo khi Khóa phòng còn phiếu sắp tới**

```js
async onLock(room) {
    const { data } = await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/upcoming-bookings`)
    const message = data.count > 0
        ? `Phòng còn ${Number(data.count).toLocaleString('en-US')} phiếu đặt sắp tới. Khóa phòng sẽ gửi thông báo cho người đặt để đổi phòng. Bạn chắc chắn khóa?`
        : 'Bạn chắc chắn muốn khóa phòng họp này?'
    const ok = await this.$confirm({ title: 'Khóa phòng họp', message })
    if (!ok) return
    await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/lock`)
    await this.fetchList()
}
```

- [x] **Bước 5: Ẩn nút Xóa khi phòng đã có phiếu** — đọc cờ `is_can_delete` do BE trả trong Resource,
  đặt trong `visible` của cột Hành động. **Không** dùng `interactable` + `disabledTitle`.

- [x] **Bước 5b: Nút *Xem lịch phòng* — HOÃN sang Phase 3.** Màn `/meeting/room-board` chưa tồn tại;
  thêm nút trỏ vào route chết là nút hỏng im lặng. Phase 3 bổ sung nút này vào **cả** cột Hành động
  của màn danh sách lẫn footer màn chi tiết.

- [x] **Bước 6: Tự kiểm HTML thô + cờ quyền**

```bash
grep -rn '<input \|<textarea\|<select \|<button \|<label ' pages/meeting/rooms/ | grep -v V2Base    # rỗng
grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/rooms/                                            # rỗng
```

---

## Task 9: Cập nhật menu phân hệ Meeting

**Files:**
- Modify: `hrm-client/components/subsystem-menu/meeting.js:24-36` (nhóm Danh mục) và `:44-52` (nhóm Quản lý phòng họp)

- [x] **Bước 1: Thêm mục Tiện nghi vào nhóm Danh mục**

```js
{
    label: 'Tiện nghi phòng họp',
    link: '/meeting/room-amenities',
    isShow: ['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp'],
},
```

- [x] **Bước 2: Điền link cho mục đang treo trống**

```js
{
    label: 'Quản lý phòng họp',
    icon: 'ri-door-open-line',
    isMenuCollapsed: false,
    subItems: [
        {
            label: 'Danh sách phòng họp',
            link: '/meeting/rooms',
            isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp'],
        },
        { label: 'Đăng ký phòng họp' },   // Phase 2 mới điền link
    ],
},
```

- [x] **Bước 3: Kiểm EOL không bị phá**

```bash
cd hrm-client && git diff --numstat components/subsystem-menu/meeting.js
```
Kỳ vọng: số dòng thêm/xóa nhỏ (đúng phần vừa sửa). Cả file bị đánh dấu đổi = đã phá line ending → trả lại.

- [x] **Bước 4: Kiểm menu render thật** — Playwright MCP mở `http://127.0.0.1:3000/meeting/dashboard`,
  đếm số mục trong nhóm *Danh mục* và *Quản lý phòng họp* bằng DOM; bấm vào *Danh sách phòng họp* phải
  điều hướng đúng `/meeting/rooms` và **render ra bảng** (vào được trang chưa chứng minh gate còn sống —
  phải đo nội dung render ra DOM).

---

## Task 10: E2E UI + chạy lại toàn bộ bộ test của màn

**Files:**
- Create: `e2e/tests/meeting/meeting-room.spec.ts`

- [x] **Bước 1: Viết ca UI** — phủ: vào màn thấy bảng · tạo phòng qua modal · gắn 2 tiện nghi ·
  khóa phòng thấy cảnh báo đúng số phiếu · **tài khoản không quyền không thấy nút Thêm và vào URL trực tiếp
  không render được bảng**.

- [x] **Bước 2: Kiểm khuôn giao diện bằng số đo, không chỉ assert dữ liệu**

> **Ruling R2 (pre-flight):** màn danh mục KHÔNG dùng `V2Footer` (component đó chỉ có ở màn chi tiết/form)
> → phép đo `.v2-footer` trong bản plan đầu sẽ trả `null` và ca test thành vô nghĩa. Thay bằng 2 phép đo có thật:

```ts
// (a) footer của V2BaseModal phải luôn nằm trong viewport kể cả khi body modal cuộn
await page.locator('.modal.show .modal-body').evaluate((el) => { el.scrollTop = el.scrollHeight; });
const footer = await page.locator('.modal.show .modal-footer').boundingBox();
const viewport = page.viewportSize()!;
expect(footer!.y + footer!.height).toBeLessThanOrEqual(viewport.height);

// (b) bảng không đẩy cả trang tràn ngang
const overflow = await page.evaluate(() => document.body.scrollWidth - document.body.clientWidth);
expect(overflow).toBeLessThanOrEqual(0);
```

- [x] **Bước 3: Chạy cả thư mục, đọc dòng tổng kết** — chạy 2 lần cho cả 2 project (`chromium` +
  `api`), tổng 4 lệnh, cả 4 đều "X passed", không ca nào "did not run". Chi tiết:
  `.sdd/task-10-report.md`.

- [x] **Bước 4: Cập nhật plan** — đánh `[x]` các task đã xong, ghi Checkpoint theo đúng format.

---

---

## ⚠️ LƯU Ý KHI DEPLOY PHASE 1 LÊN MÔI TRƯỜNG KHÁC

1. **Kiểm mã trùng TRƯỚC khi chạy migration `2026_09_18_000001`**. Migration này thêm `unique('code')` cho
   `meeting_room_bookings`. MySQL **không rollback được DDL**, nên nếu bảng ở môi trường đích đã có mã trùng,
   migration sẽ đứt **sau khi** đã tạo xong 2 khóa ngoại của pivot → trạng thái nửa vời. Chạy trước:
   ```sql
   SELECT code, COUNT(*) FROM meeting_room_bookings GROUP BY code HAVING COUNT(*) > 1;
   ```
   (Trên local bảng đang rỗng nên không lộ ra rủi ro này.)
2. **Migration có bước XOÁ DỮ LIỆU**: nó dọn các dòng `meeting_room_room_amenity` mồ côi trước khi thêm FK
   (trên DB local đã xoá 78 dòng). Điều kiện xoá là `LEFT JOIN ... WHERE r.id IS NULL` — chỉ dòng không còn cha.
   Ở môi trường có dữ liệu thật, nên đếm trước để biết sẽ xoá bao nhiêu.
3. **Chạy `PermissionsTableSeeder`**: 5 quyền mới (id 1574-1578) đã nằm trong seeder. Nhưng lưu ý seeder
   **xoá toàn bộ quyền `guard_name='api'` rồi tạo lại** — trên DB local có 472 quyền mà seeder không khai nên
   đã KHÔNG chạy seeder (xem Ruling R7), chỉ INSERT 5 dòng. Ở môi trường đích phải cân nhắc điều tương tự.
4. **Nêu trong mô tả PR**: `components/modal/V2BaseModal.vue` được thêm method `hide()` (alias `close()`),
   để modal mới dùng được với `unsavedModalMixin`. Thuần bổ sung, không đổi `show()`/`close()`.

---

# PHASE 2 — Đặt phòng + duyệt

Kết quả nghiệm thu: đặt được phòng (đặt lẻ, chưa nối Meeting — đó là Phase 4), chống trùng lịch thật sự
(có test 2 request song song), duyệt/từ chối/hủy đủ vòng đời, người liên quan nhận được thông báo.


> **Ghi chú đối chiếu thực tế Phase 2 (18/09/2026)** — 3 điểm KHÔNG diễn ra như plan viết:
> - **Task 12 bước 2**: vẫn KHÔNG chạy `db:seed` (Ruling R7 còn hiệu lực), chỉ INSERT 2 quyền có chủ đích.
> - **Thứ tự khóa**: plan chỉ nói "khóa phiếu"; thực tế phải chốt quy ước **Room → Booking cho TOÀN module**
>   sau khi review phát hiện `update()` và `MeetingRoomService::destroy()` khóa ngược chiều (nguy cơ deadlock thật).
> - **Phát sinh ngoài plan**: endpoint `GET /meeting/rooms/bookable` (Ruling R11) + đổi `isShow` của mục
>   "Đăng ký phòng họp" thành `true` — vì gate quyền danh mục chặn mất chính đối tượng mà quyết định #8 phục vụ.


## ⚠️ 3 cái bẫy đã đo thật trước khi lên plan — đọc kỹ, đừng lặp lại

**Bẫy 1 — Gửi thông báo nhầm người.** `EmployeeInfoService::sendToAllNotification($ids, $data)` nhận
**`employee_info_id`**, KHÔNG phải `employees.id`. Đã đo trên DB gộp: **chỉ 2/1099 nhân viên có
`id == employee_info_id`**. Bảng của phần phòng họp lưu `employee_id` (= `employees.id`), nên truyền thẳng
vào là **thông báo bay sang người khác** — không lỗi, không log, chỉ sai người nhận.
⇒ Mọi chỗ gửi thông báo phải map qua `employees.employee_info_id` trước. Viết **một** helper dùng chung,
đừng map lẻ ở từng chỗ.

**Bẫy 2 — Sinh mã phiếu kiểu cũ sẽ nổ.** Khuôn `getNextCode()` của dự án (`BomList.php:175-179`) dùng
`max('id') + 1`. Phase 1 đã thêm **`unique('code')`** cho `meeting_room_bookings`, nên 2 request song song
sinh cùng mã → 1 request chết bằng lỗi SQL thô (`Duplicate entry`), user thấy lỗi 500 vô nghĩa.
⇒ Sinh mã trong **cùng transaction** với `lockForUpdate`, hoặc bắt `QueryException` mã 1062 rồi sinh lại
(retry tối đa 3 lần). Phải có test 2 request song song chứng minh không ra 500.

**Bẫy 3 — Điều kiện tiên quyết từ review Phase 1**: `MeetingRoomController::destroy()` kiểm `isCanDelete()`
rồi mới mở transaction, **không `lockForUpdate`**. Phase 1 chưa ai ghi được vào bảng phiếu nên cửa sổ lỗi
chưa tồn tại; **mở luồng đặt phòng là nó thành thật ngay** (đặt phòng đúng lúc admin bấm Xóa → phiếu mồ côi).
⇒ Task 11 phải xử trước khi bật API tạo phiếu.

## Task 11: Entity phiếu + luật chống trùng (logic thuần, TDD) + vá điều kiện tiên quyết

**Files:**
- Create: `Modules/Meeting/Entities/MeetingRoomBooking.php`, `Entities/MeetingRoomBookingParticipant.php`
- Modify: `Modules/Meeting/Services/MeetingRoomService.php` (bẫy 3)
- Test: `tests/Unit/MeetingRoomBookingOverlapTest.php`

**Interfaces — task sau gọi đúng tên này:**
- `MeetingRoomBooking::STATUS_CHO_DUYET=1 · DA_DUYET=2 · TU_CHOI=3 · DA_HUY=4 · HOAN_THANH=5`
- `MeetingRoomBooking::SOURCE_TU_DAT=1 · SOURCE_TU_MEETING=2`
- `MeetingRoomBooking::overlaps($startA, $endA, $startB, $endB): bool` — static, thuần
- `MeetingRoomBooking::statusText($status): string`, `statusColor($status): string`
- `$booking->isCanEdit()`, `isCanCancel()`, `isCanApprove()`, `isCanReject()`

- [x] **Bước 1: Viết test đỏ cho luật giao giờ** (`tests/Unit/MeetingRoomBookingOverlapTest.php`)

```php
public function test_cham_mep_khong_tinh_la_trung()
{
    // 14:00-15:00 và 15:00-16:00 là HỢP LỆ (spec mục 5.2)
    $this->assertFalse(MeetingRoomBooking::overlaps(
        '2026-09-20 14:00:00', '2026-09-20 15:00:00',
        '2026-09-20 15:00:00', '2026-09-20 16:00:00'
    ));
    // lồng trong
    $this->assertTrue(MeetingRoomBooking::overlaps(
        '2026-09-20 14:00:00', '2026-09-20 16:00:00',
        '2026-09-20 14:30:00', '2026-09-20 15:00:00'
    ));
    // trùm qua
    $this->assertTrue(MeetingRoomBooking::overlaps(
        '2026-09-20 14:30:00', '2026-09-20 15:00:00',
        '2026-09-20 14:00:00', '2026-09-20 16:00:00'
    ));
    // qua đêm (đã chốt CHO PHÉP, xem spec edge case 3)
    $this->assertTrue(MeetingRoomBooking::overlaps(
        '2026-09-20 22:00:00', '2026-09-21 02:00:00',
        '2026-09-21 01:00:00', '2026-09-21 03:00:00'
    ));
}
```

- [x] **Bước 2: Chạy, xác nhận ĐỎ** — `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomBookingOverlapTest`
- [x] **Bước 3: Viết 2 entity** (`extends BaseModel`, `$fillable` đối chiếu `SHOW COLUMNS` thật), công thức giao giờ:
  `$startA < $endB && $endA > $startB` (chạm mép KHÔNG tính trùng).
- [x] **Bước 4: Chạy lại, XANH.**
- [x] **Bước 5: Vá bẫy 3** — `MeetingRoomService::destroy()`: đưa việc kiểm `isCanDelete()` vào TRONG
  `DB::transaction` và khóa các phiếu của phòng bằng `lockForUpdate()` trước khi quyết định cho xóa.

## Task 12: 2 quyền mới + luật nhìn thấy phiếu

**Files:** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (+2 dòng, id **1579-1580**)

- [x] **Bước 1:** thêm `Xem tất cả phiếu đặt phòng họp` (1579), `Duyệt phiếu đặt phòng họp` (1580),
  group `Quản lý phòng họp`, `type = 4`. Kiểm trùng id/tên như Task 4.
- [x] **Bước 2:** INSERT 2 quyền + cấp cho role Super admin (18) `company_id = 1` **bằng SQL có chủ đích**
  — **KHÔNG chạy `db:seed`** (Ruling R7 vẫn còn hiệu lực: seeder xoá 472 quyền DB đang có).
- [x] **Bước 3:** kiểm `SELECT COUNT(*) FROM permissions WHERE guard_name='api'` = **747** (745 + 2).
- [x] **Bước 4 — luật nhìn thấy phiếu** (áp dụng ở Task 14, ghi ở đây cho tập trung): không có quyền 1579 thì
  chỉ thấy phiếu **mình đặt**, **mình được mời** (bảng participants), **hoặc phiếu của phòng mình quản lý**
  (`meeting_rooms.manager_employee_id = <mình>`). Thiếu vế cuối là quản lý phòng không thấy phiếu cần mình duyệt.

## Task 13: API tạo / sửa phiếu + chống trùng (phần khó nhất của cả feature)

**Files:** `Services/MeetingRoomBookingService.php`, `Http/Controllers/Api/V1/MeetingRoomBookingController.php`,
`Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php`, `Transformers/MeetingRoomBooking/*`,
`Routes/api.php`; test `e2e/tests/meeting/meeting-room-booking.api.spec.ts`

**Validate khi lưu (spec 5.1):** `end_at > start_at`; nằm trong giờ mở cửa phòng **chỉ khi phiếu gọn trong 1 ngày**
(qua đêm thì bỏ kiểm này nhưng chặn `> 72 giờ`); không đặt quá khứ; không quá `meeting_room_max_advance_days`;
phòng `status = 1`; khác công ty thì phòng phải `allow_cross_company = 1`;
**số người > sức chứa → CẢNH BÁO, KHÔNG chặn, KHÔNG tự sửa số user nhập**.

**Luật trùng (spec 5.2)** — phải đúng từng vế:
- Phòng `require_approval = 0` → phiếu tạo ra là **Đã duyệt** ngay; trùng với phiếu Đã duyệt là **chặn 422**,
  lỗi trả về **gắn đúng field giờ** kèm tên cuộc họp đang giữ chỗ.
- Phòng `require_approval = 1` → phiếu **Chờ duyệt**, **cho phép nhiều phiếu chờ duyệt trùng giờ**.
- Phiếu **Đã duyệt** thì không ai đặt đè, kể cả xin duyệt.

- [x] **Bước 1: Viết spec e2e ĐỎ trước**, gồm ca **2 request song song**:

```ts
const [a, b] = await Promise.all([
    api.post('/api/v1/meeting/room-bookings', { data: payloadTrungGio }),
    api.post('/api/v1/meeting/room-bookings', { data: payloadTrungGio }),
]);
const codes = [a.status(), b.status()].sort();
expect(codes).toEqual([200, 422]);          // đúng 1 cái thắng
expect(await countBookings(roomId)).toBe(1); // KHÔNG được lọt 2 phiếu
```

- [x] **Bước 2: Chạy, xác nhận ĐỎ (404).**
- [x] **Bước 3: Service — kiểm trùng trong transaction có khóa:**

```php
return DB::transaction(function () use ($request) {
    // Khóa mọi phiếu còn hiệu lực của phòng trong khoảng ngày liên quan.
    // SELECT rồi INSERT mà không khóa: 2 request cách nhau 200ms lọt cả hai — lỗi kinh điển của bài toán đặt chỗ.
    $conflicts = MeetingRoomBooking::where('meeting_room_id', $roomId)
        ->whereIn('status', [MeetingRoomBooking::STATUS_DA_DUYET])
        ->where('start_at', '<', $endAt)
        ->where('end_at', '>', $startAt)
        ->lockForUpdate()
        ->get();
    if ($conflicts->isNotEmpty()) {
        throw ValidationException::withMessages(['start_at' => 'Phòng đã có cuộc họp "' . $conflicts->first()->title . '" lúc …']);
    }
    // sinh mã trong cùng transaction (xem bẫy 2)
    …
});
```

- [x] **Bước 4: Sinh mã `DPH-YYYY-NNNNN` an toàn** — trong cùng transaction, và bọc `QueryException` mã 1062
  để sinh lại tối đa 3 lần. Test song song ở bước 1 phải không ra 500.
- [x] **Bước 5: Resource trả đủ cờ hành động + thời gian ISO-8601** (quy ước cho app mobile, spec 6.4):
  `is_can_edit/cancel/approve/reject/checkin/checkout`, `start_at` dạng `2026-09-17T14:00:00+07:00` kèm
  `start_at_text`, `status_text`, `status_color`.
- [x] **Bước 6: Sửa phiếu** — chỉ người đặt, chỉ khi **chưa tới giờ bắt đầu**; đổi giờ/phòng thì chạy lại toàn bộ
  kiểm tra; phòng cần duyệt thì phiếu **quay về Chờ duyệt**. Phiếu đã tới giờ: BE trả **423**, không phải 422.
- [x] **Bước 7: Chạy lại spec, XANH**, đọc dòng tổng kết.

## Task 14: Duyệt / Từ chối / Hủy + tự từ chối phiếu trùng

- [x] **Bước 1: Spec e2e đỏ** cho luật quan trọng nhất: phòng cần duyệt, tạo **3 phiếu chờ duyệt trùng giờ**,
  duyệt 1 phiếu → phiếu đó **Đã duyệt**, **2 phiếu kia tự chuyển Từ chối** với `is_auto_rejected = 1` và
  `reject_reason` = "Phòng đã được duyệt cho cuộc họp khác".
- [x] **Bước 2: Cài đặt trong 1 transaction có `lockForUpdate`** (tránh 2 người duyệt 2 phiếu trùng giờ cùng lúc).
- [x] **Bước 3: Hủy** — người đặt / quản lý phòng / người có quyền 1580; **bắt buộc nhập lý do**; chỉ trước giờ
  bắt đầu (đã tới giờ thì **ẩn nút**, BE trả 423 — muốn kết thúc sớm là Check-out, Phase 5).
- [x] **Bước 4: Chốt chặn của quyết định #12** — phiếu `source = 2` (sinh từ Meeting) thì **KHÔNG AI hủy được**,
  kể cả quản lý phòng: kiểm ngay đầu hàm, trả **423** + message chỉ sang phiếu họp. Phase 2 chưa có phiếu
  `source = 2` nhưng **vẫn phải cài + có unit test**, nếu không Phase 4 bật lên là hở.
- [x] **Bước 5: Từ chối ≠ Hủy** — 2 trạng thái riêng, 2 màu riêng (`#DC2626` vs `#6B7280`).
- [x] **Bước 6: Luật nhìn thấy phiếu** theo Task 12 bước 4; có ca e2e cho tài khoản **quản lý phòng không có
  quyền 1579** vẫn thấy phiếu của phòng mình.

## Task 15: Thông báo (5 loại của Phase 2)

- [x] **Bước 1: Helper dùng chung** `buildNotificationContent($prefix, $action, $name, $note)` — tự cắt tên
  đối tượng 50 ký tự / tổng 120 ký tự, bọc `<b>` quanh tên. Prefix **`[DPH]`**.
- [x] **Bước 2: Helper map người nhận (BẪY 1)** — nhận mảng `employee_id`, trả mảng `employee_info_id`:
  `Employee::whereIn('id', $ids)->pluck('employee_info_id')->filter()->values()`. **Mọi** chỗ gửi đi qua đây.
- [x] **Bước 3: 5 loại thông báo** (spec mục 7): `Chờ duyệt` → quản lý phòng · `Đã duyệt` → người đặt +
  người dự (áp dụng **cả** khi phòng không cần duyệt, vì phiếu sinh ra đã là Đã duyệt) · `Từ chối` (kể cả tự
  động) → người đặt · `Thay đổi lịch` → người dự · `Hủy` → người đặt + người dự.
- [x] **Bước 4: Deep-link kèm ID** — `url = '/meeting/bookings?open_booking=' . $booking->id`,
  `type` theo bộ `meeting_room_booking_pending|approved|rejected|updated|cancelled`, `id = $booking->id`.
- [x] **Bước 5: Test** — tạo phiếu vào phòng cần duyệt rồi **đọc bảng thông báo** khẳng định người nhận là
  **đúng `employee_info_id` của quản lý phòng** (đây chính là ca bắt bẫy 1).

## Task 16: FE màn danh sách phiếu `/meeting/bookings`

- [x] Bộ lọc: khoảng ngày · phòng · công ty · trạng thái · người đặt · công tắc **Chỉ phiếu của tôi**
  (mặc định **bật** với người không có quyền 1579).
- [x] Cột: Mã · Tiêu đề · Phòng · Thời gian · Người đặt · Chủ trì · Số người · Nguồn · Trạng thái
  (badge dùng `status_color` BE trả).
- [x] Hành động đọc **từ cờ BE**, ẩn hẳn khi không dùng được, **đồng bộ y hệt** ở footer màn chi tiết.
- [x] Điền link menu **Đăng ký phòng họp** → `/meeting/bookings`, `isShow` = 2 quyền phòng họp
  (đây cũng là lớp chặn URL — xem ghi chú cơ chế gate ở Task 9).
- [x] 2 lệnh grep tự kiểm phải rỗng; cờ quyền qua mixin `CheckPermission`.

## Task 17: FE modal đặt phòng

- [x] Trường: Phòng · Ngày · Từ giờ – Đến giờ · Tiêu đề · Nội dung · Chủ trì · Người tham dự · Số người · Lặp lại
  (ô Lặp lại để **Phase 5**, chưa bật).
- [x] Select phòng **lọc được theo sức chứa tối thiểu và tiện nghi**.
- [x] Trong modal hiển thị **dải giờ bận của phòng trong ngày đó** (ai giữ, tới mấy giờ) — chọn giờ không phải
  thoát ra tra lịch. Lấy bằng **1 request**, không gọi trong vòng lặp.
- [x] Lỗi trùng giờ từ BE phải hiện **ngay dưới ô giờ** (inline), không phải toast.
- [x] Số người > sức chứa → cảnh báo vàng, **giữ nguyên số user nhập**.

## Task 18: Bộ e2e Phase 2 + chạy lại toàn bộ

- [x] Gom vào `e2e/tests/meeting/meeting-room-booking.spec.ts` (UI) + `.api.spec.ts` (API).
- [x] Ca bắt buộc: 2 request song song · duyệt 1 phiếu thì phiếu trùng tự từ chối · sửa phiếu đã tới giờ → 423 ·
  hủy phiếu `source=2` → 423 · người không quyền 1579 chỉ thấy phiếu của mình · quản lý phòng thấy phiếu cần duyệt ·
  thông báo tới **đúng người** (đọc DB) · lỗi trùng giờ hiện inline dưới ô giờ.
- [x] Chạy **cả thư mục** `tests/meeting` cho cả 2 project, **2 lần**, đọc dòng tổng kết; DB sạch rác sau khi chạy.

---

# PHASE 3 — Màn theo dõi tình trạng phòng

Kết quả nghiệm thu: nhìn 1 màn biết ngay phòng nào giờ nào trống; bấm ô trống đặt được luôn; xem được lịch tuần
của 1 phòng và bảng thẻ trạng thái thời gian thực.

## ⚠️ 5 cái bẫy của phase này — đọc trước khi code

1. **KHÔNG có FullCalendar resource-timeline.** Repo chỉ có `@fullcalendar` v5 bản **miễn phí**
   (core/timegrid/list/interaction). Dạng "resource × thời gian" là bản **Premium trả phí** ⇒ lưới Phòng × Giờ
   **phải tự dựng bằng CSS grid**, đừng mất thời gian tìm cách ép FullCalendar làm.
2. **Đo layout trong `watcher` + `$nextTick` ra DOM CŨ** (bẫy đã ghi của dự án): tính toạ độ/độ rộng khối phải
   kèm `requestAnimationFrame`, nếu không lệch đúng 1 nhịp mà **không báo lỗi gì**.
3. **Phiếu QUA ĐÊM** (đã chốt cho phép ở Phase 1): phải hiện ở **mọi ngày nó chạm**, cắt ở mép ngày kèm dấu
   tiếp diễn. Khung giờ lưới phải **tự nới** để ôm trọn phiếu nằm ngoài giờ mở cửa — nếu không, phòng đang bị
   giữ mà lưới trông như trống.
4. **CẤM `networkidle` trong e2e** — màn này có **tự refresh 60 giây**, chờ networkidle là hết giờ test.
   Và `setInterval` phải `clearInterval` khi rời màn, nếu không polling chạy ngầm mãi.
5. **1 request cho cả lưới.** `GET /meeting/rooms/board?date=` trả **cả phòng lẫn phiếu trong ngày**;
   TUYỆT ĐỐI không gọi mỗi phòng một request (spec 6.3, quy tắc hiệu năng của CLAUDE.md).

## Task 19: 3 endpoint BE cho màn theo dõi

**Files:** `MeetingRoomService.php` (thêm method), `MeetingRoomController.php`, `Routes/api.php`,
Transformer gọn cho lưới; test `e2e/tests/meeting/meeting-room-board.api.spec.ts`

- [ ] **Bước 1: Viết spec e2e ĐỎ trước** cho 3 endpoint.
- [ ] **Bước 2: `GET meeting/rooms/board?date=&company_id=&amenity_ids[]=&capacity_from=`** — **1 request** trả:
  `rooms[]` (id, code, name, capacity, location) + `bookings[]` trong ngày (id, code, title, room_id, start_at,
  end_at, status, status_color, booked_by_name) + `config` (`open_time`, `close_time` hiệu lực theo công ty).
  - Chỉ trả phiếu **còn hiệu lực** (Chờ duyệt + Đã duyệt + Hoàn thành), KHÔNG trả phiếu Đã hủy/Từ chối.
  - **Phiếu qua đêm**: phải trả cả phiếu bắt đầu hôm trước mà còn kéo sang ngày đang xem
    (điều kiện `start_at < ngày+1` AND `end_at > ngày`), đừng lọc bằng `whereDate(start_at)`.
  - **Cấm N+1**: 1 query phòng + 1 query phiếu, eager load, đếm theo lô.
  - Gate quyền: xem được màn theo dõi thì cần quyền **xem danh mục phòng** HOẶC là người đăng nhập bình thường?
    → theo quyết định #8, **mọi nhân viên đều xem được tình trạng phòng** (đây là màn tra cứu để đặt phòng)
    ⇒ **KHÔNG gắn `checkPermission`**, nhưng **chỉ trả phòng người đó được phép đặt** (dùng lại
    `MeetingRoom::canBeBookedByCompany()` như `/rooms/bookable`), và **KHÔNG trả `checkin_qr_token`**.
- [ ] **Bước 3: `GET meeting/rooms/{id}/week?start_date=`** — phiếu của 1 phòng trong tuần (7 ngày từ `start_date`).
- [ ] **Bước 4: `GET meeting/rooms/status-board`** — mỗi phòng kèm: phiếu **đang diễn ra** (nếu có) và phiếu
  **kế tiếp trong ngày**; trả sẵn `state` = `trong` / `dang_hop` / `sap_hop` để FE khỏi tự suy.
- [ ] **Bước 5: Chạy lại spec, XANH**, đọc dòng tổng kết.

## Task 20: Component dùng chung `RoomTimelineGrid.vue`

**Files:** `components/meeting-room/RoomTimelineGrid.vue` + `.claude/skills/room-timeline-grid/SKILL.md`

> CLAUDE.md bắt: thành phần chưa từng có trong project thì **tách component dùng chung ngay từ lần đầu** và
> **bổ sung SKILL.md**, không nhúng thẳng vào page.

- [ ] **Bước 1:** props `rooms`, `bookings`, `openTime`, `closeTime`, `stepMinutes` (mặc định 30), `date`;
  emit `slot-click` (phòng + giờ bắt đầu) và `booking-click`.
- [ ] **Bước 2:** dựng bằng **CSS grid**: mỗi dòng 1 phòng, cột theo bước 30 phút; khối phiếu định vị theo
  `grid-column` tính từ phút, **không** dùng `position:absolute` theo pixel (đổi cỡ màn hình là lệch).
- [ ] **Bước 3:** **vạch đỏ mốc "bây giờ"**, chỉ hiện khi đang xem ngày hôm nay.
- [ ] **Bước 4:** phiếu **qua đêm** cắt ở mép ngày, có dấu tiếp diễn (`←`/`→`); khung giờ **tự nới** nếu có phiếu
  nằm ngoài `open_time`-`close_time`.
- [ ] **Bước 5:** màu khối lấy `status_color` BE trả; chữ trong khối **không dùng animation dịch chuyển**
  (bẫy đã ghi: chữ nhoè/vỡ pixel), số đo tránh giá trị lẻ kiểu `10.5px`.
- [ ] **Bước 6:** viết `SKILL.md`: khi nào dùng, props, cách tính cột, 5 bẫy ở trên.

## Task 21: Màn `/meeting/room-board` — tab "Theo ngày"

- [ ] Chọn ngày (mặc định hôm nay) + lọc công ty/tiện nghi/sức chứa; **1 request** `board`.
- [ ] Bấm **ô trống** → mở `BookingFormModal` (tái dùng của Phase 2) với **phòng + ngày + giờ điền sẵn**;
  lưu xong thì **tải lại lưới**.
- [ ] Bấm **khối phiếu** → mở `BookingDetailModal` (tái dùng).
- [ ] `layout: 'default-sidebar'`; cờ quyền qua mixin `CheckPermission`, fail-closed.

## Task 22: Tab "Theo tuần (1 phòng)" + tab "Thẻ trạng thái"

- [ ] **Theo tuần**: dùng `@fullcalendar` timeGrid có sẵn (v5 bản free), chọn phòng ở đầu tab, gọi endpoint `week`.
- [ ] **Thẻ trạng thái**: mỗi phòng 1 thẻ — *Đang trống* / *Đang họp đến HH:mm* / *Sắp họp lúc HH:mm*, kèm tên
  cuộc họp + chủ trì. **Tự refresh 60 giây bằng `setInterval`, `clearInterval` ở `beforeDestroy`**.
- [ ] 3 tab giữ được lựa chọn khi chuyển qua lại (không mất ngày/phòng đang chọn).

## Task 23: Menu + trả nợ nút "Xem lịch phòng" của Phase 1

- [ ] `components/subsystem-menu/meeting.js`: thêm mục **Tình trạng phòng họp** → `/meeting/room-board`,
  `isShow: true` (mọi nhân viên xem được, cùng lý do với mục "Đăng ký phòng họp").
- [ ] Màn `/meeting/rooms`: bổ sung nút **Xem lịch phòng** (Phase 1 đã hoãn vì màn chưa tồn tại) → điều hướng
  sang `/meeting/room-board?room_id=<id>&date=<hôm nay>`, và màn board phải **lọc sẵn đúng phòng đó**.
- [ ] Giữ nguyên EOL; `git diff --numstat` phải gọn.

## Task 24: e2e màn theo dõi + chạy lại toàn bộ

- [ ] **Ca ĐO BẰNG SỐ (yêu cầu cứng của dự án, không được thay bằng ảnh chụp)**: phiếu 14:00-15:30 phải có khối
  **bắt đầu đúng mép cột 14:00** và **rộng đúng 3 ô 30 phút** — so `getBoundingClientRect()` của khối với của ô cột,
  sai 1 ô là lệch giờ mà mắt thường không thấy.
- [ ] Ca **bấm ô trống** → modal mở với phòng/giờ điền sẵn đúng.
- [ ] Ca **phiếu qua đêm** hiện ở cả 2 ngày, có dấu tiếp diễn.
- [ ] Ca **vạch "bây giờ"** chỉ hiện khi xem ngày hôm nay.
- [ ] Ca tab Thẻ trạng thái: phòng đang có phiếu diễn ra hiện đúng trạng thái *Đang họp*.
- [ ] Chạy **cả thư mục** `tests/meeting` cho **cả 2 project**, mỗi project **2 lần**, FOREGROUND, đọc dòng tổng kết;
  không `failed`/`did not run`/`flaky`. Kiểm DB sạch rác sau khi chạy.

## Phase 2-6 (chưa mở task chi tiết)

- [ ] Phase 2 — Đặt phòng + duyệt (CRUD phiếu, luật chống trùng + `lockForUpdate`, thông báo)
- [ ] Phase 3 — Màn theo dõi (`RoomTimelineGrid` + 3 tab)
- [ ] Phase 4 — Nối với Meeting (`MeetingRoomBookingSyncService`, ô chọn phòng trong form Meeting)
- [ ] Phase 5 — Check-in + QR + 3 job nền + đặt lặp định kỳ
- [ ] Phase 6 — Báo cáo hiệu quả sử dụng

> Lên task chi tiết cho từng phase khi bắt đầu phase đó, theo cùng khuôn trên.

---

### Checkpoint — 17/09/2026
Vừa hoàn thành: brainstorming, spec đầy đủ, plan chi tiết Phase 1 (10 task)
Đang làm dở: chưa thực thi task nào, chưa động vào code
Bước tiếp theo: chạy Task 1 — tạo module `Modules/Meeting`
Blocked:

### Checkpoint — 18/09/2026
Vừa hoàn thành: Task 10 (E2E UI chính thức + chạy lại toàn bộ) — HOÀN THÀNH, Phase 1 xong toàn bộ
10/10 task. `e2e/tests/meeting/meeting-room.spec.ts` (5 nhóm ca UI, phủ đủ 8 nhóm ca tối thiểu của
task-10-brief.md, gồm cả 2 khối bắt buộc: ca bảo mật `checkin_qr_token` lớp Resource và ca chứng
minh gate route còn sống). Xoá 3 spec smoke tạm (`_room-ui`, `_room-amenity-ui`, `_menu`), giữ
`_auth-smoke.spec.ts`. Thêm ca bảo mật vào `meeting-room.spec.ts` (nhóm E, không phải file .api) vì
cần cả kiểm UI (nút Tạo mới ẩn) lẫn kiểm API trong cùng cửa sổ cấp quyền tạm. Chạy `tests/meeting`
2 lần cho cả 2 project (chromium 11/11, api 11/11) — không ca nào "did not run", không flaky. DB
sạch rác `E2E%` sau khi chạy; quyền tạm (permission 1575 → role 20 → company 1) đã thu hồi và kiểm
lại bằng SELECT COUNT = 0. Chi tiết: `.sdd/task-10-report.md`.
Đang làm dở: không — Phase 1 hoàn thành, chưa mở Phase 2.
Bước tiếp theo: mở task chi tiết cho Phase 2 (Đặt phòng + duyệt) khi được yêu cầu tiếp tục.
Blocked:

### Checkpoint — 18/09/2026 (fix round 1)
Vừa hoàn thành: Task 10 fix round 1 (review Approved + 1 Important + 1 Minor). Important: bổ sung ca
`C1` vào nhóm C (`meeting-room.spec.ts`) — cảnh báo "chưa lưu" khi đóng modal Thêm tiện nghi (Ở lại
giữ dữ liệu / Thoát không tạo bản ghi) — ca này có ở spec smoke cũ `_room-amenity-ui.smoke.spec.ts`
nhưng bị bỏ sót khi port, nay đã bổ sung lại; ca cũ đổi tên thành `C2`. Minor: nhóm D (D1, D2) thêm
assert tường minh nút "Tạo mới" đếm 0. Báo cáo cập nhật mục Concerns liệt kê đầy đủ MỌI ca smoke bị
xoá không port (không chỉ riêng menu-rail như trước). Chạy lại 2 lần × 2 project: chromium 12/12,
api 11/11 (11→12 vì thêm ca C1) — không ca nào "did not run", không flaky. DB sạch rác `E2E%`, quyền
tạm đã thu hồi (SELECT COUNT = 0). Chi tiết: `.sdd/task-10-report.md`.
Đang làm dở: không — Phase 1 hoàn thành (đã qua fix round 1), chưa mở Phase 2.
Bước tiếp theo: chờ review round 2, hoặc mở task chi tiết cho Phase 2 (Đặt phòng + duyệt) nếu được yêu cầu.
Blocked:

### Checkpoint — 18/09/2026 (KẾT THÚC PHASE 1)
Vừa hoàn thành: toàn bộ 11 task Phase 1 + 1 đợt fix sau review tổng + 1 vòng fix residual.
Đang làm dở: không có.
Bước tiếp theo: user quyết cách đưa `feat/quan-ly-phong-hop` về `gop_db` (chưa commit gì, theo quy tắc dự án).
  Sau đó mở Phase 2 — điều kiện tiên quyết đã ghi: bổ sung `lockForUpdate` cho `destroy()` trước khi bật luồng đặt phòng.
Blocked: không.
Số liệu chốt: 14 ca e2e API + 14 ca e2e UI xanh (người điều phối tự chạy lại lần cuối);
  FK pivot 2/2, unique mã phiếu có, pivot mồ côi 0, rác test 0, `permissions guard=api` = 745 (không mất dữ liệu).

### Checkpoint — 18/09/2026 (KẾT THÚC PHASE 2)
Vừa hoàn thành: 8 task Phase 2 (11-18) + 1 đợt fix sau review tổng + các vòng fix theo task.
Đang làm dở: không có.
Bước tiếp theo: user quyết cách đưa `feat/quan-ly-phong-hop` về `gop_db`. Phase 3 (màn theo dõi phòng × giờ) chưa mở.
Blocked: không.
Số liệu chốt (người điều phối tự chạy lần cuối): PHPUnit **39 tests / 80 assertions**;
  e2e API **61 passed**; e2e UI **26 passed**; participants mồ côi 118 → **0** (đã thêm FK cascade);
  `permissions guard=api` = **747**.
Nợ kỹ thuật ghi lại (không chặn bàn giao): thiếu ca test riêng cho nhánh **423 "phiếu đã tới giờ"** ở
  `approve()`/`reject()` (code đúng, nhưng nếu sau này ai xoá nhầm nhánh đó thì không test nào báo đỏ);
  `syncParticipants()` xóa-tạo-lại (chốt cùng thiết kế check-in ở Phase 3);
  `nextCode()` dùng `max(id)+1` (rủi ro khi Phase 5 sinh hàng loạt phiếu định kỳ).

### Checkpoint — 18/09/2026 (DỪNG Ở PHASE 3 THEO YÊU CẦU USER)
Vừa hoàn thành: 6 task Phase 3 (19-24) + 1 vòng fix (làm tròn phút) + bù 3 ca coverage cho spec board API.
Đã commit: BE `8a22a9b01`, FE `7a1e9524d`.
Đang làm dở: không có.
Bước tiếp theo: **chờ user review và chỉ ra phần chưa đúng mong muốn** — không tự sửa đoán.
  Việc còn treo của Phase 3: review tổng; sửa TÊN ca F1 (assert đúng, tên lạc hậu).
Blocked: không.
Số liệu chốt: e2e API **77 passed**, e2e UI **42 passed**, PHPUnit **39 tests / 80 assertions**.


---

## Phase 3.5 — Sửa theo review của user (19/09/2026)

> Nguồn: 4 quyết định user chốt sau khi review màn Danh mục phòng họp / Tiện nghi.
> **Skill thắng spec về hình thức UI** — spec cũ (mục 10 phân quyền) bị thay bởi quyết định dưới đây.

**Quyết định mới (ghi đè spec):**
1. **Bộ quyền gộp còn 1: "Khai báo phòng họp"** — có quyền này thì tạo/sửa/khóa/xóa được CẢ phòng họp
   LẪN tiện nghi phòng họp, và vào được 2 màn danh mục. Bỏ 4 quyền cũ (`Quản lý danh mục phòng họp`,
   `Xem danh mục phòng họp`, `Quản lý danh mục tiện nghi phòng họp`, `Xem danh mục tiện nghi phòng họp`).
2. **Công ty nào tạo thì phòng thuộc công ty đó** — bỏ select Công ty ở form thêm/sửa; `company_id`
   do `BaseModel::creating()` tự điền theo người tạo. **Sửa/khóa/xóa chỉ được với phòng của công ty mình**
   (chặn ở BE, 403).
3. **Màn danh sách xem phòng của MỌI công ty** + có ô lọc Công ty.
4. **DB `meeting_rooms` bỏ `department_id`, `part_id`** (chỉ giữ `company_id`).
5. **Bổ sung Lịch sử cho 2 màn danh mục** theo skill `entity-history` (bảng chung `catalog_histories`,
   mục `Lịch sử` trong menu ⋮, khối Lịch sử thu gọn cuối popup Xem).
6. Popup **Xem** phòng / Xem tiện nghi phải đúng skill `modal-popup` (footer CHỈ có nút Đóng).
7. Màn tiện nghi: chữ nút `Khóa tiện nghi` / `Mở khóa tiện nghi` → **`Khóa` / `Mở khóa`**.

### Task 25 (BE): gộp bộ quyền về "Khai báo phòng họp"
- [x] Sửa `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`: id 1574 → `Khai báo phòng họp`;
      xóa 3 dòng 1575/1576/1577
- [x] Sửa `Modules/Meeting/Routes/api.php`: mọi `checkPermission` của `meeting/rooms` + `meeting/room-amenities`
      đổi sang `Khai báo phòng họp`
- [x] Sửa gate `checkin_qr_token` trong `DetailMeetingRoomResource` + mọi `isCurrentEmployeeHasPermission()` liên quan
- [x] Cập nhật DB local: rename permission 1574, xóa 1575-1577 + `role_has_permissions` trỏ tới chúng
- [x] FE: `components/subsystem-menu/meeting.js` + cờ quyền 2 màn danh mục

### Task 26 (BE): phòng họp thuộc công ty người tạo + chặn sửa chéo công ty
- [x] Migration `2026_09_19_000001_drop_org_columns_from_meeting_rooms_table.php` — drop `department_id`, `part_id`
- [x] Gỡ 2 cột khỏi `MeetingRoom::$fillable`, `MeetingRoomRequest`, `MeetingRoomResource`, `DetailMeetingRoomResource`
- [x] `updateOrCreate()` KHÔNG nhận `company_id` từ request nữa
- [x] Thêm `MeetingRoom::isManagedBy($companyId)` + chặn 403 ở `updateOrCreate` (nhánh sửa), `destroy`, `lock`, `unlock`
- [x] Resource trả `is_can_edit` / `is_can_delete` đã tính cả điều kiện cùng công ty (FE ẩn nút, không disable)
- [ ] Unit test: sửa phòng công ty khác → 403; tạo phòng không truyền company_id → gán đúng công ty người tạo

### Task 27 (BE): lịch sử danh mục cho phòng họp + tiện nghi
- [x] Khai `meeting_rooms`, `meeting_room_amenities` trong `CatalogHistoryService::TABLES` (nhãn cột tiếng Việt)
- [x] `MeetingRoomService` + `MeetingRoomAmenityService` dùng trait `LogsCatalogHistory`
      (create / update / lock / unlock / delete), `catalogDisplay()` đổi id → tên (công ty, quản lý, tiện nghi, trạng thái)
- [ ] Test: sửa 1 phòng → `catalog_histories` có đúng 1 dòng, diff đúng cột

### Task 28 (FE): màn danh sách + form phòng họp
- [x] Bỏ select Công ty khỏi `MeetingRoomModal.vue`
- [x] Thêm ô lọc Công ty vào bộ lọc màn danh sách
- [x] Menu ⋮ thêm mục `Lịch sử` (icon `ri-history-line`, không gắn quyền) + `<CatalogHistoryModal modal-id="history-meeting-room" record-prefix="Phòng họp" />`
- [x] Popup **Xem** phòng: footer chỉ nút `Đóng` (`fas fa-arrow-left`) + khối Lịch sử cuối popup (`SystemInfoSection`, thu gọn)

### Task 29 (FE): màn danh sách tiện nghi
- [x] Chữ nút `Khóa tiện nghi` / `Mở khóa tiện nghi` → `Khóa` / `Mở khóa`
- [x] Menu ⋮ thêm mục `Lịch sử` + `<CatalogHistoryModal modal-id="history-room-amenity" record-prefix="Tiện nghi" />`
- [x] Popup **Xem** tiện nghi: footer chỉ nút `Đóng` + khối Lịch sử cuối popup

### Task 30: e2e
- [x] Cập nhật `meeting-room.api.spec.ts` / `room-amenity.api.spec.ts` theo quyền mới + ca 403 sửa chéo công ty
- [x] Cập nhật `meeting-room.spec.ts`: bỏ ô Công ty ở form, cột Hành động dùng `V2BaseRowActions`, thêm ca A3b (Lịch sử)
- [x] Chạy lại TOÀN BỘ bộ test của 2 màn (nhớ `--no-deps`, `--workers=1`, và `API_BASE=:8001 BASE_URL=:3001`)

### Task 31 (phát sinh): sửa lỗi component dùng chung `V2BaseRowActions`
- [x] `window.addEventListener('scroll', closeMenu, true)` đóng menu ngay khi vừa mở (trình duyệt tự
      cuộn nút ⋮ vào tầm nhìn lúc bấm) → bỏ qua scroll trong 250ms đầu sau khi mở (`handleScroll()`)
- [x] Đo lại trên trình duyệt thật: bấm lần 1 sau khi lọc → menu mở (trước khi sửa: `menuOpen=false`
      dù `menuStyle` đã có toạ độ); cuộn thật sau 400ms vẫn đóng menu như cũ
- [x] User đã duyệt sửa component dùng chung (19/09/2026)

### Task 32 (phát sinh): ca e2e đỏ theo ĐỒNG HỒ
- [x] `meeting-room-board.api.spec.ts` F1/F2 đặt phiếu "sau đây 5 phút" trong khi giờ đóng cửa mặc
      định là 20:00 → chạy bộ test sau 19h là 422. Khai `open_time 00:00:00` / `close_time 23:59:59`
      cho 2 phòng setup của 2 ca đó

### Task 33 (phát sinh): 2 ca e2e chờ SAI MỐC / hết giờ
- [x] `meeting-room-board.spec.ts` J1: `toHaveCount(1)` ngay sau khi gõ từ khoá là **xanh giả** —
      lúc đó bảng đang có đúng 1 dòng "Đang tải dữ liệu...", chưa phải kết quả lọc. Khi DB chỉ còn
      vài phòng của chính spec thì `.first()` rơi trúng phòng khác (id giảm dần). Sửa: chờ đúng
      DÒNG của Phòng A hiện ra rồi mới khẳng định bộ lọc còn 1 dòng
- [x] J1 nâng `test.setTimeout(60000)`: ca đi qua 2 màn trên dev server đơn luồng, 30s mặc định hết
      giờ ngay ở bước đếm `.rtg-room-label`

### Checkpoint — 19/09/2026 (Phase 3.5)
Vừa hoàn thành: 4 yêu cầu review của user (gộp quyền "Khai báo phòng họp" + công ty theo người tạo +
  bỏ department_id/part_id; lịch sử cho 2 màn danh mục; chữ nút Khóa/Mở khóa; popup Xem đúng chuẩn),
  kèm 3 lỗi phát sinh tìm ra khi chạy lại test (component dùng chung `V2BaseRowActions`, cache quyền
  spatie trong e2e, 2 ca e2e chờ sai mốc / đỏ theo đồng hồ).
Đang làm dở: không.
Bước tiếp theo: chờ user review tiếp; Phase 4 (nối Meeting) chưa mở.
Blocked: không.
Số liệu chốt (chạy 1 lượt CẢ thư mục `tests/meeting`, `--workers=1 --no-deps`, `API_BASE=:8001`
  `BASE_URL=:3001`): **124 passed / 0 failed / 0 "did not run"** (11,5 phút) — trước đợt này chạy cả
  thư mục chỉ ra 44 passed + 29 "did not run". PHPUnit **39 tests / 80 assertions**.
  Rác `E2E%` trong `meeting_rooms` sau khi chạy = **0** (đã sửa `afterAll` xóa thẳng bằng SQL cho
  phòng mà API từ chối vì khác công ty — kéo về công ty 1 thì đụng unique `(company_id, code)`).

### Task 34 (phát sinh): rà popup Xem theo skill, đối chiếu màn `/assign/meeting_type`
- [x] Thiếu **dòng mô tả bản ghi** ở header (`V2BaseModal` prop `subtitle` + `subtitleLabel`,
      skill modal-popup mục 0) — popup trước đó chỉ có mỗi chữ "Xem phòng họp". Nay hiện
      `Phòng họp: <mã> - <tên>` / `Tiện nghi: <mã> - <tên>`, chỉ ở chế độ Sửa/Xem
- [x] Bổ sung assert e2e cho dòng mô tả ở CẢ 2 popup (ca A3b và C2)
- [x] **Không thêm** chip `Cập nhật / Bởi` như màn `/assign/meeting_type` (user chốt 19/09/2026):
      màn đó là popup `b-modal` khuôn CŨ (skill mục 1); khuôn `V2BaseModal` (mục 0) không có chip
      này, và thông tin ai-sửa-gì-lúc-nào đã nằm trong khối Lịch sử cuối popup, chi tiết hơn
- [x] Tự kiểm HTML thô ở 2 màn (`grep '<input |<textarea|<select |<button |<label |class="btn '`)
      → chỉ còn khớp trong comment, không có element thô

### Task 35 (phát sinh): khoảng cách ô trong form popup — `mb-3` → `mb-2`
- [x] Cả 4 popup của feature (`MeetingRoomModal`, `RoomAmenityModal`, `BookingFormModal`,
      `BookingDetailModal`) đang để `col-md-* mb-3` (và vài ô `mb-1`) trong khi **chuẩn dùng chung
      của project là `mb-2`** — đếm thực tế: 32 chỗ dùng `mb-2`, chỉ riêng feature này dùng `mb-3`
- [x] `V2BaseFormSection` đổi `class="mt-3"` → `class="mb-2"` (khuôn skill form-validate mục 1c;
      dùng `mt-3` thì `V2BaseModal` không triệt được margin của khối cuối)
- [x] Sửa 4 selector `.col-md-12.mb-3` trong `meeting-room.spec.ts` theo
- [x] Đo lại DOM: mọi ô `margin-bottom = 12px`, khối cuối `margin-bottom = 0px`
- Ghi chú: `components/modal/meeting-cancel-reason-modal.vue` (Redmine #11357, KHÔNG thuộc feature
  này) cũng còn `mb-3` — để nguyên, không sửa đại trà

### Task 36: rà màn DANH SÁCH phòng họp theo skill `list-page`
- [x] Thêm cột **STT** (`sticky`, `locked`, 60px) — trước đó không có; cột **Mã** thành `sticky` +
      `locked` + `sortable` (mục 4)
- [x] Thêm **Người tạo / Ngày tạo** (cột BẮT BUỘC, mục 6) và **Người cập nhật / Ngày cập nhật**
      (khai đủ nhưng ẩn mặc định)
- [x] **Bộ cột mặc định gọn còn 7 cột** `STT → Mã → Tên → Người tạo → Ngày tạo → Trạng thái →
      Hành động`; 7 cột nghiệp vụ chuyển `isVisible: false` (trước đây hiện cả 11 cột, mở màn là
      phải cuộn ngang)
- [x] Thêm popup **"Cấu hình cột hiển thị"** qua `columnCustomizationMixin` (`columnScreenKey:
      'meeting_rooms'`) + nút mở ở thanh hành động (mục 5)
- [x] Bật **sort** đúng 3 cột (Mã, Tên, Ngày tạo/Ngày cập nhật) + whitelist `$allowedSortFields`
      trong `MeetingRoomService::index()` — key FE và BE khớp nhau
- [x] **Người tạo chỉ hiện TÊN**, bỏ mã nhân viên (mục 6). Accessor dùng chung
      `BaseModel::getEmployeeCreateNameAttribute()` trả `mã - tên` nên Resource tự lấy
      `employee_create->info->fullname` — KHÔNG sửa accessor dùng chung
- [x] Ngày tạo / Ngày cập nhật **bỏ GIÂY**: `Helper::formatDateTime($x, 'd/m/Y H:i')`
- [x] e2e: `EXPECTED_COLUMNS` còn 7 cột; thêm helper `cellByHeader()` (tra ô theo TÊN CỘT thay cho
      `td:nth-child(N)` — chỉ số cột nay đổi theo cấu hình user) và `showColumns()`; ca A2 bật 3 cột
      qua popup rồi mới đo; beforeAll/afterAll xoá `user_column_settings` của màn
- [x] Bổ sung ca API `1c` cho sắp xếp: asc/desc đúng thứ tự + `sort_by` ngoài whitelist bị bỏ qua
- [x] Chạy migration thiếu ở DB local: `user_column_settings` (bảng lưu cấu hình cột)
- Còn nợ: **màn Tiện nghi phòng họp** cũng thiếu y hệt (STT, Người tạo/Ngày tạo, cấu hình cột,
  sort) — chưa sửa, chờ user quyết có làm luôn không

### Checkpoint — 19/09/2026 (KẾT THÚC ĐỢT REVIEW 1 / PHASE 3.5)
Vừa hoàn thành: task 25-36 — 4 quyết định user chốt (gộp quyền "Khai báo phòng họp" + công ty theo
  người tạo + bỏ `department_id`/`part_id`; lịch sử cho 2 màn danh mục; chữ nút Khoá/Mở khoá; popup
  Xem đúng chuẩn) và 3 đợt rà theo skill (popup Xem, khoảng cách `mb-2`, màn danh sách theo
  `list-page`), kèm 6 lỗi phát sinh tìm ra khi chạy lại test.
Đang làm dở: không.
Bước tiếp theo: user review tiếp; nếu OK thì (a) quyết có rà màn **Tiện nghi phòng họp** theo
  `list-page` như màn phòng họp không, (b) mở Phase 4 (nối phiếu đặt phòng với Meeting).
Blocked: không.
Số liệu chốt: e2e `tests/meeting` **124 passed / 0 failed / 0 "did not run"** (chạy cả thư mục 1 lượt);
  sau đó sửa thêm task 34-36 và chạy lại theo màn: rooms UI **15/15**, rooms API **11/11**,
  board UI **18/18**, booking UI **12/12**. PHPUnit **39 tests / 80 assertions**.
Việc cần biết khi bàn giao:
  - Code vẫn ở worktree `hrm-worktrees/phong-hop-{api,client}`, nhánh `feat/quan-ly-phong-hop`, **CHƯA commit**.
  - DB local đã chạy thêm 3 migration vốn thiếu: `catalog_histories`, `user_column_settings`,
    `2026_09_19_000001_drop_org_columns_from_meeting_rooms_table`.
  - Quyền 1575/1576/1577 đã bị XOÁ khỏi DB local + seeder; 1574 đổi tên thành "Khai báo phòng họp".
  - Lúc dọn dữ liệu test có chạy `DELETE FROM user_column_settings` KHÔNG kèm điều kiện → xoá cả 42
    dòng cấu hình cột của mọi màn/mọi user trên DB local (chỉ là tuỳ chọn hiển thị, user lưu lại là có).

### Task 37: merge về `gop_db` + xoá worktree (19/09/2026)
- [x] Merge `feat/quan-ly-phong-hop` → `gop_db` ở CẢ 2 repo (`--no-ff`): API `da27321d1`,
      Client `616df00b9`. Git không báo xung đột nào
- [x] **XUNG ĐỘT GIT KHÔNG THẤY ĐƯỢC — id quyền bị trùng**: trong lúc feature làm ở nhánh riêng,
      `gop_db` đã cấp **1574-1585** cho nhóm "Danh mục hàng hóa". Feature đang giữ 1574/1578/1579/
      1580 → sau merge, `PermissionsTableSeeder` khai 2 lần cùng id, chạy seeder là lỗi trùng khoá
      chính (git im lặng vì khác dòng trong cùng file). Đánh số lại **1586-1589**:
      `Khai báo phòng họp` 1586 · `Xem báo cáo hiệu quả sử dụng phòng họp` 1587 ·
      `Xem tất cả phiếu đặt phòng họp` 1588 · `Duyệt phiếu đặt phòng họp` 1589
- [x] Đồng bộ id mới vào DB local (`permissions` + `role_has_permissions`) và các ca e2e
- [x] Kiểm sau merge trên checkout chính: PHPUnit **39/39**, e2e API phòng họp + tiện nghi **17/17**
- [x] Dừng 2 dev server của worktree (kill đúng PID) rồi `git worktree remove` cả 2;
      thư mục `hrm-worktrees/` nay rỗng. **Giữ nguyên nhánh `feat/quan-ly-phong-hop`** ở cả 2 repo
      để còn tra lịch sử — chưa xoá nhánh, chưa push

### Checkpoint — 19/09/2026 (ĐÃ MERGE VỀ `gop_db`, XOÁ WORKTREE)
Vừa hoàn thành: merge `feat/quan-ly-phong-hop` → `gop_db` cả 2 repo (API `da27321d1`,
  Client `616df00b9`), xử lý trùng id quyền (1574/1578/1579/1580 → 1586-1589), đồng bộ DB local +
  e2e, kiểm lại trên checkout chính (PHPUnit 39/39, e2e API 17/17), dừng dev server worktree và
  `git worktree remove` cả 2.
Đang làm dở: không.
Bước tiếp theo:
  1. Restart Nuxt `:3000` (đang chạy từ trước lúc merge nên chưa biết page mới; lỗi
     "Can't resolve component" thì `rm -rf .nuxt/components` rồi chạy lại).
  2. User quyết: có rà **màn Tiện nghi phòng họp** theo skill `list-page` không (đang thiếu STT,
     Người tạo/Ngày tạo, popup Cấu hình cột, sort).
  3. Mở **Phase 4** — nối phiếu đặt phòng với Meeting.
Blocked: không.
Trạng thái nhánh: `gop_db` có đủ Phase 1-3 + đợt sửa review 1, **chưa push**. Nhánh
  `feat/quan-ly-phong-hop` vẫn giữ ở cả 2 repo (chưa xoá) để tra lịch sử.

---

### Task 38: rà màn DANH MỤC TIỆN NGHI phòng họp theo skill `list-page` (19/09/2026)
Trả nợ "Còn lại" của Task 36. **Hiện trạng đo trên DOM thật TRƯỚC khi sửa** (`/meeting/room-amenities`,
checkout chính :3000):
- Bảng 7 cột `Mã · Tên tiện nghi · Icon · Thứ tự · Trạng thái · Người cập nhật · Hành động`
  → thiếu **STT / Người tạo / Ngày tạo**, và **Trạng thái đứng sai chỗ** (skill mục 4: ngay trước Hành động)
- `button[title="Cấu hình cột hiển thị"]` đếm **0** (thiếu popup mục 5)
- **0 cột** sort được; API `?sort_by=code&sort_desc=true` trả **nguyên thứ tự cũ** `[Wifi, BH8, TV]`
  (BE bỏ qua tham số — đã đo bằng curl, 3 lượt giống hệt nhau)
- Panel vẫn có nút **"Tìm kiếm nâng cao"** dù chỉ 1 ô lọc (skill: ≤3 ô kể cả ô tìm nhanh → bày hết ra hàng ngang)
- API trả `created_at: "18/09/2026 19:11:59"` (**còn giây**) và `created_by_name: "DNS01 - DNS Admin"`
  (**còn mã nhân viên**) — 2 lỗi y hệt đã sửa ở màn phòng họp (mục 6)

**Việc đã làm**
- [x] BE `MeetingRoomAmenityService::index()` — whitelist `$allowedSortFields` (code, name, created_at,
      updated_at), giữ mặc định `sort_order asc, id asc`. `sort_order` KHÔNG cho sort (nó là khoá sắp
      mặc định). Đo lại bằng curl: asc `[BH8, TV, Wifi]` · desc `[Wifi, TV, BH8]` · `sort_by=(select 1)`
      quay về mặc định
- [x] BE 2 Resource (list + detail) — `created_by_name`/`updated_by_name` chỉ **TÊN**
      (`DNS01 - DNS Admin` → `DNS Admin`); ngày `d/m/Y H:i` (bỏ giây)
- [x] FE `columnCustomizationMixin` + `columnScreenKey: 'meeting_room_amenities'` + popup + nút
- [x] FE bộ cột 11 cột, mặc định hiện đúng **7 cột** `STT → Mã → Tên → Người tạo → Ngày tạo →
      Trạng thái → Hành động`; sort đúng 4 cột (Mã, Tên, Ngày cập nhật, Ngày tạo)
- [x] FE bỏ 2 chỗ `'—'`; ô dữ liệu dùng `field-line text-dark font-weight-normal` (mục 3b-2b)
- [x] FE `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`, bỏ prop `title`/`subtitle` riêng → panel tự
      chuyển chế độ hàng ngang, **không còn nút "Tìm kiếm nâng cao"** (2 ô ≤ 3)
- [x] e2e: +2 ca API (7 sắp xếp, 8 định dạng Người tạo/Ngày tạo) · +3 ca UI (C0 bộ cột mặc định,
      C3 popup cấu hình cột + ô Icon rỗng, C4 sắp xếp đếm request) · sửa tên ca A1 và F1

### 5 lỗi PHÁT SINH tìm ra khi đo (không nằm trong dự kiến ban đầu)
- [x] **Lần đổi bộ lọc ĐẦU TIÊN sau khi tải trang bị nuốt** — `oldFilters` khởi tạo `{}` nên deep
      watcher so `undefined` với `''` thấy khác nhau → `shouldCallApi = false`. Đo bằng
      `page.on('request')`: cú bấm sắp xếp đầu tiên phát ra **0 request**. Có ở **cả 3 màn** phòng
      họp / tiện nghi / phiếu đặt. Sửa: `created()` chốt `oldFilters` (đúng khuôn skill mục
      "Filter auto-search")
- [x] **Mỗi thao tác lọc/sắp xếp bắn 2 request giống hệt nhau** — `meta.per_page` BE trả **chuỗi**
      `"10"` còn `filters.per_page` là **số** `10`; `loadData()` gán lại → watcher chạy thêm lượt.
      Sửa `Number(meta.per_page)` ở 3 màn. Đo lại: mỗi cú bấm đúng **1** request
- [x] **Nút "Cấu hình cột hiển thị" bấm trong ~1 giây đầu không mở được gì** — popup khai
      `v-if="columnFieldsLoaded"`, nút thì hiện ngay. Tái hiện bằng e2e: `columnFieldsLoaded=false`
      + **0** phần tử `.modal` trong DOM. Sửa: nút cũng `v-if="columnFieldsLoaded"` (CLAUDE.md —
      nút không dùng được thì ẨN). Ca cũ của màn phòng họp xanh được chỉ vì nó làm việc khác trước
      đó đủ lâu
- [x] **Vòng dọn rác e2e treo `beforeAll` → cả file in "did not run"** — phòng rác còn phiếu đặt thì
      DELETE trả 400, vòng `for (i < 20)` vẫn lặp đủ 20 lượt × (1 GET + N DELETE) > 30s. Sửa 8 vòng
      trong 6 spec: đếm số bản ghi xoá được, **1 lượt không xoá nổi gì thì dừng**
- [x] **4 spec còn hard-code đường dẫn worktree đã xoá** (`hrm-worktrees/phong-hop-api`) làm
      `readEnvValue()` ném ENOENT → `runMysql()` chết → ca đỏ + các ca sau "did not run". Đổi mặc
      định về checkout chính `HRM/hrm-api`
- [x] Sửa luôn 4 ô `class="field-line"` TRẦN của màn phòng họp (nợ Task 36): chữ ra `#475569` nhạt
      hơn mọi ô khác — đo `getComputedStyle`: `rgb(71,85,105)` → `rgb(50,58,70)`, nay 2 màn khớp nhau

### Nợ ghi nhận, CHƯA làm (ngoài phạm vi task này)
- Màn **`/meeting/bookings`** (danh sách phiếu đặt phòng, Phase 2) chưa hề rà theo `list-page`:
  thiếu STT, Người tạo/Ngày tạo, popup cấu hình cột, sort; còn **5** chỗ `'—'` và **5** ô
  `field-line` trần. Chỉ mới sửa 2 lỗi chung (nuốt request + bắn 2 request) cho màn này

### Checkpoint — 19/09/2026 (Task 38 — rà màn Tiện nghi theo `list-page`)
Vừa hoàn thành: task 38 + 6 lỗi phát sinh ở trên.
Đang làm dở: không.
Bước tiếp theo: user review màn; sau đó mở **Phase 4** (nối phiếu đặt phòng với Meeting).
Blocked: không.
Số liệu chốt (chạy trên checkout chính, API `:8000` + Nuxt `:3000`):
  e2e API `tests/meeting` **81 passed** (0 failed, 0 "did not run") ·
  e2e UI `tests/meeting` **49 passed** · riêng `meeting-room.spec.ts` (2 màn danh mục) **18 passed**
  (trước task này là 15) · PHPUnit `--filter Meeting` **40 tests / 84 assertions**.
Việc cần biết khi bàn giao:
  - Code **chưa commit**, nằm ở checkout chính nhánh `gop_db` cả 2 repo.
  - `hrm-api` còn thay đổi **của session khác** (Assign / warehouse export print) — không đụng tới.
  - Đã bổ sung origin `127.0.0.1:3000` + `localhost:3000` vào `e2e/.auth/user-wt.json` và
    `user-nocost-wt.json` (trước chỉ có `:3001` của worktree cũ nên chạy e2e trên checkout chính là
    không đăng nhập được).
  - Đã xoá dữ liệu rác `E2E%` (10 phòng + 10 phiếu đặt) do các lần chạy bị ngắt để lại.
  - API dev chạy kèm `PHP_CLI_SERVER_WORKERS=4` cho đỡ nghẽn khi e2e bắn liên tục.

---

# PHASE 4 — Nối phiếu đặt phòng với Meeting (19/09/2026)

Nghiệm thu: **lên lịch họp là giữ phòng luôn**. Spec mục 5.6.

## Hiện trạng đã kiểm trước khi lên task (không đoán)
- `meetings.meeting_room_id` **đã có sẵn** trong DB (migration Phase 1) — không cần migration mới
- `Meeting` (`Modules/Assign/Entities/Meeting/Meeting.php`) `extends BaseModel`, đã có **2 hook**:
  `boot()::saving` (ghi `completed_at`) và `booted()::saving` (snapshot thị trường/khách hàng)
  → điểm gắn mới đặt trong `booted()` cho nhất quán, dùng `saved` + `deleted`
- 4 đường ghi `meetings`: `store()`, `update()`, `changeStatus()` (hủy), `destroy()`, cộng cron
  `autoCancelOverdueMeeting()` — tất cả đều gọi `save()`/`delete()` nên **model event phủ hết**
- `MeetingRoomBookingService` đã có sẵn luật trùng (`assertNoOverlap` — mutex `lockForUpdate` trên
  dòng phòng), luật 5.1 (`validateBookingRules`), sinh mã chống trùng (`createWithUniqueCode`),
  `syncParticipants` — **4 hàm này đang `private`**
- FE: ô "Hình thức" + "Địa điểm meeting" nằm ở `pages/assign/meeting/components/GeneralInfo.vue`
- Endpoint `GET meeting/rooms/bookable` (Task 17) đã trả danh sách phòng đặt được cho người đăng nhập

## Task 39 (BE): `MeetingRoomBookingSyncService` + gắn model event
- [x] 8 hàm của `MeetingRoomBookingService` đổi `private` → `public` để DÙNG LẠI nguyên văn
      (luật trùng có mutex, luật 5.1, sinh mã, 4 loại thông báo) — KHÔNG chép luật sang service mới
- [x] `syncFromMeeting()` + `deleteForMeeting()` + `refreshParticipants()`, gắn `Meeting::booted()`
      (`saved` / `deleted`)
- [x] Chặn trùng ném `ValidationException` → 422, **chỉ kiểm khi 5 trường phòng/giờ/hình thức/trạng
      thái đổi** (`ROOM_FIELDS`, so bằng `getChanges()`)

## Task 40 (BE): payload + dữ liệu cho FE
- [x] `meeting_room_id` vào `$request->only([...])` của `store()`/`update()` + `$fillable` của `Meeting`
- [x] `MeetingCreate/UpdateApiRequest`: `meeting_room_id` `nullable|exists`, và **`location` chỉ bắt
      buộc khi họp Trực tiếp mà CHƯA chọn phòng** (`Rule::requiredIf`) — có phòng rồi thì không bắt
      gõ thêm địa điểm
- [x] `MeetingTransformer` trả khối `meeting_room` (tên phòng, `is_locked`, mã + trạng thái + màu
      phiếu, lý do từ chối) cho FE vẽ badge
- [x] `MeetingHistoryService`: snapshot thêm **"Phòng họp"** — đổi phòng là đổi chỗ giữ chỗ, phải có vết

## Task 41 (FE): ô chọn phòng + badge trong form Meeting
- [x] `GeneralInfo.vue`: ô **Phòng họp** chỉ hiện khi `mode_id = 1`, options từ `meeting/rooms/bookable`,
      tự chèn lại phòng ĐANG CHỌN nếu phòng đã bị khóa (🔒 do `V2BaseSelect` tự gắn)
- [x] Badge trạng thái giữ phòng cạnh nhãn (chữ + màu do BE trả) + dòng lý do khi bị từ chối
- [x] `create.vue` / `MeetingForm.vue` khai sẵn `meeting_room_id` + `meeting_room` trong khung form
      (Vue 2 không reactive với key thêm sau)
- [x] Dấu `*` của "Địa điểm meeting" tự tắt khi đã chọn phòng

## Task 42: kiểm chứng
- [x] PHPUnit `MeetingRoomBookingSyncRuleTest` — 7 ca cho luật giữ phòng + `ROOM_FIELDS`
      (có đối chứng ÂM: `conclusion`/`note`/cờ cron KHÔNG được nằm trong danh sách kiểm trùng)
- [x] e2e API `meeting-room-sync.api.spec.ts` — **7 ca**, đi qua đúng endpoint người dùng bấm
- [x] e2e UI `meeting-room-sync.spec.ts` — **2 ca** (ẩn/hiện theo Hình thức + badge đỏ Từ chối)
- [x] Chạy lại toàn bộ: e2e API `tests/meeting` **88 passed**, e2e UI `tests/meeting` **51 passed**,
      PHPUnit **toàn bộ 173 tests / 474 assertions**

### 3 việc phát sinh khi đo (không có trong dự kiến)
- [x] **`attendee_count = 0` và 0 người tham dự ở mọi phiếu sinh từ cuộc họp** — hook `Meeting::saved`
      chạy TRƯỚC khi controller `syncCompanyMembers()` ghi bảng `meeting_employees`. Sửa bằng
      `refreshParticipants()` gọi tường minh ở CUỐI `store()`/`update()` (2 đường ghi duy nhất đổi
      được thành phần dự họp); cố tình KHÔNG hook vào `MeetingEmployee` vì sync xoá-rồi-tạo-lại sẽ
      thành N+1 lượt ghi cho một lần lưu
- [x] **500 khi đổi phòng sau khi phiếu bị từ chối** — `meeting_room_bookings.meeting_id` là
      **UNIQUE** (spec 4.4) nên KHÔNG được insert phiếu thứ hai cho cùng cuộc họp. Sửa: luôn DÙNG
      LẠI đúng dòng phiếu cũ và "hồi sinh" nó (xoá sạch `reject_reason`/`cancel_*`/`approved_*`,
      đặt lại trạng thái theo `require_approval`)
- [x] **Lỗi 422 rơi vào hư không** — tầng phiếu trả key `start_at`, form meeting không có ô nào tên
      đó nên màn hình không hiện gì. Sửa: `rethrowForMeetingForm()` gom về `meeting_room_id`

### ⚠️ KHÔNG phải lỗi Phase 4 — 4 ca `tests/assign` đỏ vì DB LOCAL THIẾU MIGRATION
`meeting-host.api/spec`, `meeting-investment-survey`, `meeting-by-market-grouping` đỏ ở bước đọc
meeting fixture #44: API trả 500 `Unknown column 'meeting_report_id' in 'field list'`.
Nguyên nhân: migration `Modules/Assign/.../2026_09_18_000001_add_meeting_link_to_tasks_table.php`
(Redmine #11456) **chưa chạy trên DB local** — `migrate:status` còn hàng chục migration "No".
Bằng chứng không liên quan Phase 4: `git diff` của `MeetingTransformer` chỉ **thêm 36 dòng** khối
phòng họp, truy vấn `tasks` gây lỗi đã có nguyên văn trong `HEAD`.
**Chưa tự chạy migration** vì DB local dùng chung với các session khác — cần user quyết.
Lệnh nếu muốn chạy riêng file đó:
`php artisan migrate --path=Modules/Assign/Database/Migrations/2026_09_18_000001_add_meeting_link_to_tasks_table.php`

### Task 43 (lỗi user báo): tạo được 2 cuộc họp TRÙNG khung giờ cùng phòng
- [x] **Tái hiện**: đặt 1 phiếu Đã duyệt giữ chỗ → tạo cuộc họp đúng khung giờ đó → **HTTP 200**,
      sinh phiếu thứ 2 đè lên (đúng dấu vết user gặp: phiếu `DPH-2026-01385` của meeting 909 đè
      `DPH-2026-00001` ở phòng 1618, ngày 19/09 08:00-12:00 vs 09:00-12:00)
- [x] **Gốc**: hook `Meeting::saved` lọc "có đổi phòng/giờ không" bằng `getChanges()`, mà Laravel
      **chỉ gọi `syncChanges()` trong `performUpdate()`** (`Model.php:1074`) — đường **INSERT không
      gọi**, nên lúc TẠO cuộc họp `getChanges()` luôn RỖNG → bỏ qua sạch `assertNoOverlap()` **và**
      `validateBookingRules()` (quá khứ, phòng khóa, khác công ty, ngoài giờ mở cửa, hạn đặt trước).
      Đường SỬA vẫn chạy đúng nên ca P4-2 cũ xanh — lỗ chỉ ở đường TẠO
- [x] **Sửa tận gốc, không phụ thuộc framework**: thêm điều kiện `aboutToHoldRoom` (chưa có phiếu,
      hoặc phiếu đang chết) → **sắp đi giữ chỗ thì BẮT BUỘC kiểm**, `getChanges()` chỉ còn dùng để
      quyết định có kiểm lại cho phiếu đang sống hay không
- [x] Ca test **P4-2b** viết TRƯỚC khi sửa (đỏ `Expected 422 / Received 200`), sau khi sửa xanh;
      ca còn assert thêm: khung giờ đó chỉ còn ĐÚNG 1 phiếu Đã duyệt và meeting bị chặn không được
      lưu nửa vời
- [x] Chạy lại: e2e API `tests/meeting` **89 passed**, e2e UI **51 passed**, PHPUnit **173/474**
- [x] **Dọn dữ liệu hỏng do lỗi sinh ra** (user chốt 19/09/2026: *"xoá phiếu cũ hơn"*):
      xoá `DPH-2026-00001` "test lần 1" (id 1384, tạo 18/09) + 1 dòng người tham dự của nó;
      giữ `DPH-2026-01385` của meeting 909. API **từ chối Hủy** ("Phiếu đã tới giờ bắt đầu… dùng
      Check-out" — phiếu 09:00-12:00 trong khi lúc dọn là 10:03) nên phải xoá thẳng dòng DB;
      đã `mysqldump` sao lưu 2 dòng ra scratchpad trước khi xoá.
      Đo lại: toàn DB còn **0 cặp** phiếu chồng giờ; lưới `/meeting/room-board` phòng B1 ngày
      19/09 chỉ còn **1 khối** "Test phòng hợp"

### Checkpoint — 19/09/2026 (KẾT THÚC PHASE 4)
Vừa hoàn thành: task 39-42 (nối phiếu đặt phòng với Meeting) + 3 lỗi phát sinh ở trên.
Đang làm dở: không.
Bước tiếp theo: user review; sau đó Phase 5 (check-in + QR + 3 job nền + đặt lặp định kỳ).
Blocked: không (4 ca `tests/assign` đỏ là do DB local thiếu migration, chờ user quyết có chạy không).
Số liệu chốt (SAU khi vá lỗi trùng giờ ở Task 43): e2e API `tests/meeting` **89 passed** ·
  e2e UI `tests/meeting` **51 passed** · riêng Phase 4: API 8/8, UI 2/2 · PHPUnit **173 tests / 474 assertions**.
Việc cần biết khi bàn giao:
  - Code **chưa commit**, cả 2 repo đứng ở `gop_db`.
  - Ô "Phòng họp" chỉ hiện khi Hình thức = **Trực tiếp**; chuyển sang Online là **nhả phòng** nhưng
    `meeting_room_id` vẫn giữ trong DB để còn dấu vết.
  - Cuộc họp **nháp cũng giữ chỗ** (theo spec 5.6 dòng 1, không kèm điều kiện trạng thái).
  - Màn DANH SÁCH meeting chưa hiện cột phòng họp (dùng `MeetingResource`, không phải
    `MeetingTransformer`) — ngoài phạm vi Phase 4, làm khi user yêu cầu.

---

### Task 44: bỏ trường MÃ ở 2 màn danh mục + thêm GHI CHÚ cho Tiện nghi (19/09/2026)

**User chốt**: (1) **xoá hẳn cột `code`** khỏi `meeting_rooms` + `meeting_room_amenities`;
(2) Ghi chú của Tiện nghi hiện ở **form + popup Xem + cột ẨN mặc định** (đúng skill list-page mục 6).

⚠️ Lệch skill `list-page` (mục 3/4: cột **Mã** là cột định danh, sticky + locked + link mở popup Xem)
→ đã confirm với user trước khi code. Hệ quả: **cột TÊN lên làm cột định danh** (sticky + locked +
sortable + là link mở popup Xem), bộ cột mặc định còn `STT → Tên → Người tạo → Ngày tạo → Trạng thái
→ Hành động`.

**Quyết định đi kèm (giữ nguyên tinh thần nghiệp vụ cũ)**: `code` đang mang ràng buộc duy nhất
(`meeting_rooms`: unique theo `(company_id, code)`; `meeting_room_amenities`: unique toàn hệ thống).
Bỏ mã mà không thay gì thì **2 phòng trùng tên trong cùng công ty** sẽ lọt — nên chuyển ràng buộc đó
sang **TÊN**: phòng unique theo `(company_id, name)`, tiện nghi unique theo `name`. Kiểm DB trước:
0 bản ghi trùng tên nên thêm index được ngay.

- [x] Migration `2026_09_19_000002_drop_code_add_note_meeting_room_catalogs` — gỡ 2 unique index cũ,
      DROP `code` ở cả 2 bảng, thêm `note` (text) cho tiện nghi, thêm unique mới
      `(company_id, name)` cho phòng và `name` cho tiện nghi. Đã chạy trên DB local, kiểm lại schema
- [x] BE: 2 entity `$fillable`; 2 FormRequest (bỏ rule mã, chuyển unique sang TÊN, thêm `note`);
      2 service (bỏ `code` khỏi tìm nhanh + whitelist sort + `catalogColumns` lịch sử; tiện nghi
      thêm `note` vào cả 2 chỗ ghi + lịch sử); `statusBoard`; **6 Resource** (list/detail/board/
      bookable của phòng + list/detail của tiện nghi)
- [x] FE: 2 màn danh sách (bỏ cột Mã, **TÊN thành cột định danh** sticky+locked+sortable+link mở
      popup Xem, placeholder tìm nhanh, nhãn popup Lịch sử), 2 modal (bỏ ô Mã → Tên chiếm trọn hàng;
      dòng mô tả bản ghi chỉ còn tên; tiện nghi thêm ô **Ghi chú** textarea), `RoomTimelineGrid`
      bỏ mã phòng ở dòng phụ. Thêm cột **Ghi chú** (ẩn mặc định) cho màn tiện nghi
- [x] e2e: chuyển toàn bộ fixture/selector của **8 spec** sang định danh bằng TÊN (dọn rác, lọc,
      sắp xếp, bộ cột kỳ vọng, ca "trùng mã" → "trùng TÊN"); mã PHIẾU `DPH-YYYY-NNNNN` giữ nguyên
- [x] Kiểm màn thật bằng Playwright MCP (đo DOM): 2 bảng còn đúng 6 cột mặc định
      `STT → Tên → Người tạo → Ngày tạo → Trạng thái → Hành động`, Tên là link mở popup Xem,
      ô tìm nhanh đổi chữ, form không còn ô Mã (`hasCodeInput = false`, hàng đầu `col-md-12`),
      Ghi chú lưu + hiện đúng ở popup Xem và ở cột khi bật, trùng tên báo lỗi ngay ô Tên,
      lưới theo dõi phòng + danh sách phiếu vẫn render đúng
- [ ] **CHƯA chạy bộ e2e** (user chốt 19/09/2026: không chạy e2e sau mỗi task, khi cần sẽ yêu cầu)

### Task 45: bổ sung Xuất Excel + Import Excel cho 2 màn danh mục (19/09/2026)

User yêu cầu sau khi tôi rà skill: `list-page` **không** bắt buộc màn danh sách phải có
Import/Xuất/In (chỉ bắt "có nút Xuất thì phải mở popup chọn trường" — mục 14b; nút In thì `print-page`
mục 0 + trần 2.000 dòng), **nhưng** 2 màn danh mục song sinh cùng phân hệ
(`/assign/meeting_type`, `/assign/meeting_cancel_reason`) đều có Import + Xuất → 2 màn phòng họp
đang lệch. Nút In: không màn danh mục nào có → không làm.

- [x] BE `ExportColumnRegistry`: thêm `meeting_rooms` (13 cột) + `meeting_room_amenities` (9 cột)
- [x] BE Resource: thêm khoá SCALAR cho file xuất — phòng `amenity_names` / `require_approval_text` /
      `allow_cross_company_text` (mảng + boolean vào ô Excel sẽ ra "Array"/"1"), tiện nghi `status_text`
- [x] BE 2 controller: `export()` (dùng `DynamicExport` + registry, KHÔNG viết class `*Export` riêng),
      `validateImport()`, `import()` (validate LẠI ở máy chủ rồi mới ghi, `DB::transaction`,
      trả 207 khi có dòng hỏng), `importTemplate()` (PhpSpreadsheet, có dropdown cho cột Có/Không +
      Trạng thái), helper dựng mẫu `buildImportTemplate()` dùng chung
- [x] BE 2 service: `validateImportData()` + `importRows()` — bắt trùng TÊN với DB **và** trùng giữa
      các dòng trong CHÍNH file; phòng: tên tiện nghi phải CÓ trong danh mục (không tự tạo), tên
      người quản lý phải khớp đúng 1 nhân viên; import cũng ghi **Lịch sử** như tạo tay
- [x] BE routes: `/export`, `/import-template`, `/import/validate`, `/import` — route TĨNH đặt
      TRƯỚC wildcard, gate `checkPermission:Khai báo phòng họp`
- [x] FE 2 màn: nút **Import Excel** (cam) + **Xuất Excel** (xanh lá) theo `button-convention` §2b,
      `ExportFieldsModal` (tick sẵn đúng cột đang hiện) + `V2BaseImportModal` 4 bước,
      `exportFieldsMixin`, map key cột bảng → key cột file (`exportFieldKeyMap`)
- [x] Sửa lỗi UX của chính file mẫu (tự phát hiện khi đo): dòng ví dụ điền "Wifi, Máy chiếu" và
      tên tiện nghi đã tồn tại → tải mẫu về Validate là **đỏ ngay 2 dòng**. Nay 2 cột phụ thuộc dữ
      liệu thật để TRỐNG, cách nhập ghi ở TIÊU ĐỀ cột ("Tiện nghi (ngăn bởi dấu phẩy)"), tên mẫu
      tiện nghi đổi sang tên chưa tồn tại
- [x] Đo trên trình duyệt: tải mẫu → upload lại chính nó → **Validate 2/2 hợp lệ** → **Import thành
      công 2 phòng họp**, bảng tự nạp lại; xuất file ra đúng cột đã tick (đọc lại file bằng
      PhpSpreadsheet: `STT | Tên tiện nghi | Ghi chú | Trạng thái`)
- [x] **User báo nút quá sát nhau** — đo DOM: khoảng cách giữa 4 nút = **0px** (`margin-right: 0px`)
      vì tôi chỉ khai `class="mb-2"`, THIẾU `mr-2` của khuôn chuẩn (47 chỗ trong repo dùng
      `mr-2 mb-2`, màn tham chiếu `meeting_cancel_reason` cũng vậy). Sửa: 3 nút đầu `mr-2 mb-2`,
      nút CUỐI giữ `mb-2` (không thừa lề phải). Đo lại: **12px đều** giữa cả 4 nút, cùng cao 32px,
      cùng một hàng
- [x] Đối chiếu nốt `button-convention`: màu (Import `secondary status="warning"` = cam
      `#B45309`/`#FCD34D`; Xuất `secondary status="success"` = xanh lá `#15803D`/`#86EFAC`) — mục 2b;
      icon `ri-upload-line` / `ri-file-excel-2-line` — mục 3; chữ "Import Excel" / "Xuất Excel" —
      mục 4; thứ tự primary → secondary — mục 5. Tất cả khớp
- [ ] **CHƯA chạy bộ e2e** (theo cách làm việc user đã chốt); cũng **chưa viết ca e2e** cho 2 chức
      năng mới này

### Task 46: rà + chuẩn hoá màn `/meeting/bookings` theo skill `list-page` (19/09/2026)

Rà ra **10 điểm lệch**, sửa hết:

| # | Lệch | Mục skill | Đã sửa |
|---|---|---|---|
| 1 | Thiếu cột STT; cột Mã chưa sticky/locked/sortable | 4 | thêm STT + Mã `sticky+locked+sortable` |
| 2 | Cột Mã là `<span>` trần, mở chi tiết bằng nút "Xem" riêng | 3a + 1 | Mã thành `v2-cell-link` mở popup, **bỏ nút Xem** |
| 3 | Cột Hành động tự dựng `<div>` + 5 icon rời | 1-2 | dùng `V2BaseRowActions` (2 nút chính + menu ⋮) |
| 4 | **Thiếu hành động "Lịch sử"** — và phiếu CHƯA hề ghi log | 1 + entity-history | trait `LogsCatalogHistory` + đăng ký bảng vào `CatalogHistoryService::TABLES`; ghi log ở **tạo / sửa / duyệt / từ chối (cả tự động) / hủy** |
| 5 | Không có popup Cấu hình cột, không cột nào sort được | 5 | `columnCustomizationMixin` (`screen_key: meeting_room_bookings`) + whitelist sort BE (code/time/created_at/updated_at) |
| 6 | Thiếu Người tạo / Ngày tạo (bắt buộc) + Người/Ngày cập nhật | 6 | thêm 4 cột + 4 khoá `*_text` ở Resource + eager load chống N+1 |
| 7 | 5 chỗ dấu `—` ở ô rỗng | 3b-3 | để TRỐNG |
| 8 | 5 ô `field-line` trần (chữ xám nhạt) | 3b-2b | `field-line text-dark font-weight-normal` |
| 9 | Bảng hiện cả 10 cột, phải cuộn ngang | 6 | mặc định 9 cột; Người đặt/Chủ trì/Số người/Nguồn ẩn |
| 10 | Chưa có Xuất Excel | 14b | popup chọn trường + `ExportColumnRegistry['meeting_room_bookings']` + `GET meeting/room-bookings/export` (dùng LẠI `index()` nên file tuân đúng luật nhìn thấy phiếu). **KHÔNG Import** — đây là chứng từ, phải đi qua luật chống trùng + duyệt |

**2 lỗi câm phát hiện thêm khi đo:**
- `Employee::fullname` (accessor) trả **NULL**, tên thật ở `employee_infos.fullname` → lịch sử ghi
  "(trống)". Lỗi này **có sẵn từ Phase 1** ở `MeetingRoomService::catalogDisplay()` (Người quản lý
  phòng) — đã sửa cả 2 nơi, và fallback về id khi không tra được tên.
- `CatalogHistoryService::TABLES` còn khai cột `code` cho 2 danh mục đã bỏ mã ở Task 44 → dọn, thêm
  `note` cho tiện nghi.

**Đo trên màn thật**: bảng còn 9 cột đúng thứ tự · Mã là link · 3 cột sort được, mỗi cú bấm **1
request** · menu ⋮ có "Lịch sử", popup hiện đúng diff (nhãn tiếng Việt, giờ `14:00 01/10/2026`,
người thực hiện) · Xuất Excel popup đủ 14 trường, tải file đúng tên.

- [ ] **CHƯA chạy bộ e2e**; ca e2e cho Lịch sử phiếu + Xuất Excel cũng chưa viết

---

## Task 47 — Giãn khoảng cách hàng bộ lọc (nhãn floating) ✅

User báo: *"khoảng cách dòng của bộ lọc quá gần nhau"*. Truy nguồn: **màn không sai** — `list-page`
SKILL.md quy định hàng lọc floating cách **18px** (không dưới 16px), nhưng chính component dùng chung
`components/V2BaseSmartFilterPanel.vue` ép cứng `margin-bottom: 0.5rem !important` (**8px**) cho mọi
`col-*` trong vùng lọc, áp cho cả 98 màn dùng panel.

**Chốt với user**: chỉ giãn cho nhánh **BẬT `floating`** (11 màn), không đụng 88 màn còn lại.

**Sửa** (`V2BaseSmartFilterPanel.vue`, +19/−1):
- Template: `.smart-advanced-filters` nhận thêm `:class="{ 'smart-advanced-filters--floating': floating }"`.
- CSS: nhánh floating → `[class*='col-'] { margin-bottom: 0 !important }` + `.form-row { row-gap: 18px }`.
  Dùng `row-gap` chứ KHÔNG tăng `margin-bottom`: margin cộng luôn một khoảng thừa **dưới hàng cuối**,
  đội sát mép đáy panel.

**Đo trên trình duyệt thật** (Playwright MCP, DOM):

| Màn | floating | Khoảng cách hàng | rowGap | margin-bottom cột |
|---|---|---|---|---|
| `/meeting/bookings` (6 ô / 2 hàng) | có | **18px** (trước: 8px) | 18px | 0px |
| `/meeting/rooms` (4 ô / 1 hàng) | có | — (1 hàng) | 18px | 0px |
| `/assign/tasks` (15 ô / 4 hàng) | KHÔNG | **8px** (không đổi) | normal | 8px |

Nhãn khi bay lên (thêm `.is-float`, đo sau 1 nhịp hiệu ứng): nhô khỏi mép trên ô **6px**, hở tới đáy
ô hàng trên **13px** (trước chỉ còn ~3px — đúng cái "dính" user thấy). Đáy hàng cuối → mép card còn
**11px** (card `padding-bottom: 10px`), không bị cụt.

- Đã ghi lại luật vào `.claude/skills/list-page/SKILL.md` (panel tự lo, page KHÔNG tự thêm `mb-*`).
- [ ] CHƯA chạy e2e.

**Bổ sung cùng ngày — chỗ nối trên cùng** (user: *"sửa luôn trên các màn Danh sách phòng họp, Danh
sách tiện nghi"*): đo lại 2 màn đó thì `/meeting/rooms` chỉ có **1 hàng** ô lọc nên `row-gap` không
với tới — chỗ chật thật là **hở giữa hàng tìm nhanh và hàng ô lọc đầu tiên: 8px**
(`.quick-search-row { margin-bottom: 8px }`). Thêm `.smart-advanced-filters--floating { padding-top: 10px }`
(8 + 10 = 18px). Đặt padding trên KHỐI LỌC chứ không nới margin hàng tìm nhanh: panel đóng thì
`v-show` cho khối lọc `display: none`, padding tự mất.

| Màn | Hở khối trên → hàng lọc đầu | Giữa các hàng lọc | Panel đóng: tới mép card |
|---|---|---|---|
| `/meeting/rooms` (4 ô / 1 hàng) | **8 → 18px** | — | **19px** (không đổi) |
| `/meeting/bookings` (6 ô / 2 hàng) | **18px** | 18px | — |
| `/meeting/room-amenities` | chế độ INLINE (1 ô lọc nằm cạnh ô tìm nhanh, khối nâng cao `display: none`) → không có gì để giãn, card vẫn cao 100px |
| `/assign/tasks` (KHÔNG floating) | **8px** (không đổi) | 8px | — |

Nhãn hàng lọc đầu khi bay lên: hở **13px** tới đáy ô tìm nhanh (trước ~2px). Ở bề ngang 760px màn
`/meeting/rooms` xuống 4 hàng, đo đủ 3 khoảng **18px**.

---

# PHASE 6 — Phiếu đăng ký phòng tách 2 hướng (19/09/2026)

User: *"Thiết kế đặt theo 2 hướng: Từ meeting → kế thừa thông tin; Đặt cho các nhu cầu khác: đào tạo,
văn nghệ, ăn uống… Hiện form đăng ký đăng kiêm luôn chức năng tạo cuộc họp là chưa đúng."*
Tham khảo `helpamis.misa.vn/amis-phong-hop` (trang chỉ có mục lục, không mô tả trường → thiết kế theo
nếp có sẵn của HRM).

## Task 48 — DB: danh mục mục đích + cột `purpose_id` ✅
- `2026_09_19_000003_create_meeting_room_purposes_table.php` (đã chạy): bảng `meeting_room_purposes`
  (name UNIQUE, icon, sort_order, note, status — **không có `code`**, theo nếp Task 44) +
  `meeting_room_bookings.purpose_id` (nullable + index).
- `MeetingRoomPurpose` entity (`isCanDelete()` = chưa phiếu nào dùng) + `MeetingRoomPurposesTableSeeder`
  (6 mục: Đào tạo · Phỏng vấn · Tiếp khách · Sự kiện - Văn nghệ · Ăn uống - Liên hoan · Khác).
  Seeder dùng `firstOrCreate`, **KHÔNG truncate** — phiếu đang trỏ `purpose_id` vào đây.

## Task 49 — Danh mục "Mục đích sử dụng phòng" (BE + FE) ✅
- BE: Service/Controller/Request/2 Resource copy nguyên khuôn danh mục Tiện nghi (lịch sử, sort
  whitelist, Import/Export Excel). Routes `meeting/room-purposes/*` gate `checkPermission:Khai báo phòng họp`,
  **trừ `/options`** (như `meeting/rooms/bookable`: mọi nhân viên đều đặt phòng nên phải đọc được mục đích).
- `ExportColumnRegistry['meeting_room_purposes']` + `CatalogHistoryService::TABLES['meeting_room_purposes']`.
- Gom `buildImportTemplate()` (trùng từng ký tự ở 2 controller) thành trait
  `Modules/Meeting/Http/Controllers/Concerns/BuildsImportTemplate.php`, 3 controller cùng dùng.
- FE: `pages/meeting/room-purposes/` (index + modal) copy từ `room-amenities`; menu Danh mục thêm mục
  "Mục đích sử dụng phòng".

## Task 50 — BE phiếu: mục đích + 2 endpoint cho hướng cuộc họp ✅
- `purpose_id` vào fillable/store/update (fallback `has()` như 3 field nullable khác), Resource
  (`purpose_id`, `purpose_name`), lọc `purpose_id` + `source`, cột lịch sử (`purpose_id` → tên),
  export (`purpose_name`, đổi nhãn `Tiêu đề`→`Nội dung sử dụng`, `Chủ trì`→`Người phụ trách`).
- `purpose_id` **bắt buộc** ở `MeetingRoomBookingRequest` — phiếu đi qua endpoint này luôn là phiếu tự đặt.
- `GET meeting/room-bookings/bookable-meetings`: cuộc họp trực tiếp, chưa có phòng, chưa kết thúc, chưa
  hủy, do MÌNH tạo hoặc MÌNH chủ trì.
- `POST meeting/room-bookings/assign-meeting`: ghi `meetings.meeting_room_id` → hook Phase 4 sinh phiếu.
  **Không insert thẳng phiếu** (2 đường ghi = 2 bộ luật phải giữ khớp mãi mãi).
- `MeetingRoomBooking::isCanEdit()` nay loại `source = 2`; `Service::update()` chặn 423.

## Task 51 — FE form đăng ký 2 hướng ✅
- `BookingFormModal.vue`: radio "Gắn với cuộc họp" / "Nhu cầu khác" (ẩn khi Sửa — phiếu từ cuộc họp
  không sửa được nên form Sửa luôn là hướng 2); khối kế thừa CHỈ ĐỌC; bỏ Tiêu đề-cuộc-họp/Chủ trì/
  Người tham dự khỏi hướng 2, thay bằng Mục đích + Nội dung sử dụng + Người phụ trách + Số người + Ghi chú.
- `BookingDetailModal.vue`: phiếu từ cuộc họp hiện link `/assign/meeting/<id>/show` (route đúng là
  `/show`, `/assign/meeting/<id>` KHÔNG tồn tại → link chết im lặng), phiếu tự đặt hiện Mục đích.
- `bookings/index.vue`: thêm cột **Mục đích** (hiện mặc định) + 2 ô lọc (Mục đích, Hướng đăng ký),
  nhãn "Từ meeting" → "Từ cuộc họp".
- `room-board/index.vue`: bấm ô trống ép `bookingMode = 'other'` (hướng 1 không có ô ngày/giờ).

## Đo trên trình duyệt thật (Playwright MCP)
| Việc | Kết quả đo |
|---|---|
| `/meeting/room-purposes` | 6 dòng seed, cột STT · Tên mục đích · Người tạo · Ngày tạo · Trạng thái · Hành động |
| Form — hướng cuộc họp | radio tick sẵn; chọn cuộc họp → khối chỉ đọc hiện Tên/Thời gian/Chủ trì/Số người/Nội dung; ô "Thời gian (theo cuộc họp)" = `09:30 25/09/2026 - 11:00 25/09/2026`; **không có** ô Ngày/Từ giờ/Mục đích |
| Lưu hướng cuộc họp | toast "Đăng ký phòng thành công", bảng thêm DPH-2026-02386, cột Mục đích TRỐNG, giờ đúng giờ họp |
| Form — nhu cầu khác | đúng 7 ô: Phòng · Ngày · Từ giờ · Đến giờ · Mục đích * · Nội dung sử dụng * · Người phụ trách · Số người · Ghi chú; **không có** Người tham dự |
| Lưu nhu cầu khác | DPH-2026-02387, cột Mục đích = "Phỏng vấn" |
| Nút hành động | phiếu `source=2` chỉ còn **Lịch sử** (không Sửa/Hủy); phiếu tự đặt của mình có Sửa/Hủy/Lịch sử |
| Popup Xem | phiếu cuộc họp: link `/assign/meeting/939/show` (mở được, không 404) + dòng nhắc sửa ở màn Cuộc họp; phiếu tự đặt: "Mục đích sử dụng: Phỏng vấn", nhãn "Người phụ trách" |
| Màn Tình trạng phòng | bấm ô trống → mode `other`, điền sẵn ngày 19/09/2026, 17:00→17:30, phòng đúng |

**API đã kiểm bằng curl**: thiếu `purpose_id` → 422 đúng ô; sửa phiếu `source=2` → 423; `assign-meeting`
trả phiếu `source=2` + `meeting_code/meeting_name`.

**Dữ liệu test đã dọn sạch** (3 cuộc họp `[TEST P6]` + 4 phiếu sinh ra).

## e2e — ĐÃ SỬA, CHƯA CHẠY
- `meeting-room-booking.spec.ts`: `EXPECTED_COLUMNS` theo bộ cột mới; thêm helper `chonHuongNhuCauKhac()`;
  B1/B2 chọn hướng + chọn Mục đích; `Tiêu đề` → `Nội dung sử dụng`.
- `meeting-room-board.spec.ts`: B1 assert radio `value="other"` được tick sẵn.
- `meeting-room-sync.api.spec.ts`: thêm **P6-1** (bookable-meetings + assign-meeting → phiếu source 2,
  gán xong biến mất khỏi danh sách) và **P6-2** (PUT phiếu source 2 → 423, dữ liệu không đổi).
- [ ] CHƯA chạy bộ nào (theo yêu cầu: chỉ chạy khi user gọi).

## Task 52 — Popup Xem phiếu dùng CHÍNH form, khuôn màn Danh mục phòng họp ✅

User: *"Popup xem chi tiết phiếu đặt phòng làm như popup xem chi tiết Phòng"* → chốt hướng **dùng lại
chính form đăng ký ở chế độ Xem** (giống `MeetingRoomModal.vue`: một popup cho Thêm/Sửa/Xem).

- **XOÁ `pages/meeting/bookings/components/BookingDetailModal.vue`** (khuôn "nhãn + dòng chữ" riêng).
  Hai popup cùng một dữ liệu mà nhìn khác hẳn nhau, thêm trường phải sửa 2 chỗ.
- `BookingFormModal.vue` nhận prop **`isShow`**: khoá toàn bộ ô nhập (`:disabled="isShow"` như popup
  phòng), tiêu đề "Xem phiếu đặt phòng", dòng mô tả bản ghi **"Mã phiếu: DPH-…"**, footer đổi sang
  **Duyệt / Từ chối / Hủy phiếu** theo cờ BE, và **khối Lịch sử `SystemInfoSection`** ở cuối — đúng
  như popup Xem phòng.
- Khối chỉ có ở chế độ Xem: **Thông tin phiếu** (Trạng thái · Người đặt · Công ty · Ngày tạo),
  **Nội dung cuộc họp** (phiếu `source = 2`: Tiêu đề/Chủ trì/Số người/Nội dung — form không có ô nào
  cho nhánh này), **Người tham dự** (chip, phiếu cũ + phiếu từ cuộc họp), **Kết quả xử lý**
  (Người duyệt / Lý do từ chối / Lý do hủy).
- Ẩn khi Xem: 2 ô lọc phụ (sức chứa, tiện nghi), dải giờ bận, cảnh báo vượt sức chứa — đều là công cụ
  lúc ĐANG chọn phòng.
- Chế độ Xem **không gọi** 3 API danh sách (tiện nghi / phòng đặt được / cuộc họp gán được): mở popup
  chỉ đọc mà bắn 4 request là thừa. Chỉ nạp danh mục mục đích để hiện đúng TÊN.
- 2 màn gọi popup đổi theo: `bookings/index.vue` (`formIsShow`) và `room-board/index.vue` (bấm khối
  phiếu = Xem, bấm ô trống = Tạo mới — cùng một instance nên phải gỡ cả `selectedDetailItem` lẫn cờ).

**3 lỗi câm bắt được khi đo (đã sửa):**
1. Ô "Thời gian (theo cuộc họp)" đọc `selectedMeeting` → ở chế độ Xem danh sách đó không nạp, phiếu đã
   đặt xong vẫn hiện câu *"Chọn cuộc họp để xem thời gian"*. Nay lấy giờ của CHÍNH phiếu.
2. Phòng hiện **🔒 Phòng B nhỏ** — nhánh fallback của `roomOptions` gắn `is_locked` cho mọi phòng ở chế
   độ Xem (vì không nạp danh sách), nhìn như phòng bị khoá.
3. `created_at_text` của `DetailMeetingRoomBookingResource` in cả **giây** (`19/09/2026 05:42:42`) —
   `Helper::formatDateTime()` mặc định `d/m/Y H:i:s`.

**Đo trên trình duyệt** (đã dọn 2 phiếu test sau khi đo):

| Luồng | Kết quả |
|---|---|
| Xem phiếu `source=2` | 5 khối, ngày tạo `19/09/2026 05:42`, thời gian `08:00 19/09/2026 - 12:00 19/09/2026`, link cuộc họp, khối Lịch sử ở cuối |
| Xem phiếu tự đặt | 4 khối, **0/7 ô mở khoá** (tất cả disabled), footer `Hủy phiếu · Đóng` |
| Bấm "Hủy phiếu" trong popup Xem | popup xác nhận → lưu xong popup TỰ ĐÓNG, dòng chuyển "Đã hủy" |
| Xem → Đóng → Tạo mới | tiêu đề "Đăng ký phòng họp", `isShow=false`, 0 ô bị khoá |
| Xem → Đóng → Sửa | tiêu đề "Sửa phiếu đặt phòng", 7 ô mở, footer `Lưu · Đóng` |
| Màn Tình trạng phòng | bấm khối phiếu → "Xem phiếu đặt phòng"; bấm ô trống → "Đăng ký phòng họp" điền sẵn giờ |
| Deep-link `?open_booking=2280` | popup Xem tự mở đúng phiếu, bảng nền vẫn 10 cột |

**e2e — đã sửa, CHƯA chạy**: A3 + F1 (`meeting-room-booking.spec.ts`) và C1 (`meeting-room-board.spec.ts`)
đổi `#modal-booking-detail` → `#modal-booking-form`; C1 kiểm thêm TIÊU ĐỀ vì nay 2 luồng (Xem / Tạo mới)
dùng chung một modal-id.

## Task 53 — Gom hướng dẫn trong popup đặt phòng vào icon ⓘ ✅

User: *"popup đặt phòng → đưa các thông tin hướng dẫn vào info icon cho gọn"*.

3 đoạn chữ hướng dẫn trong `BookingFormModal.vue` chuyển thành icon ⓘ:

| Trước (dòng chữ xám) | Sau |
|---|---|
| Dưới radio: *"Chọn cuộc họp đã tạo — tiêu đề, thời gian… / Đặt phòng cho đào tạo, phỏng vấn…"* | ⓘ cạnh **tiêu đề khối "Hướng đăng ký"** (`#title` slot), nội dung giải thích CẢ 2 hướng để đọc TRƯỚC khi chọn |
| Dưới khối tóm tắt cuộc họp: *"Thông tin trên lấy từ cuộc họp. Muốn sửa thì vào màn Cuộc họp."* | ⓘ trên nhãn **"Chọn cuộc họp"** (`V2BaseLabel :hint`) |
| Chế độ Xem: *"Đổi phòng hoặc thời gian của phiếu này ở màn Cuộc họp."* | ⓘ trên nhãn **"Cuộc họp"** |

**Giữ nguyên dạng chữ** câu báo rỗng *"Bạn chưa có cuộc họp nào cần phòng…"* — đó là trạng thái RỖNG
(giải thích vì sao select không có gì để chọn), giấu vào icon thì người dùng nhìn select trống trơn
không hiểu vì sao, đúng lỗi "hỏng im lặng".

**Dùng `V2BaseFieldHint` / `V2BaseLabel :hint`** (icon ⓘ dùng chung của FE, `ri-information-line` 14px
+ tooltip `.v2-field-hint-tooltip`), KHÔNG tự dựng icon mới. ⚠️ Lưu ý cho lần sau: skill
`info-icon-tooltip` quy định `b-popover custom-class="info-popover"` và cấm `v-b-tooltip`, nhưng
`V2BaseFieldHint` (component ⓘ cho NHÃN TRƯỜNG, dùng rộng khắp FE) lại chạy `v-b-tooltip` — hai kiểu
song song cho 2 vai trò khác nhau (nhãn trường vs tiêu đề bảng/biểu đồ), đã báo user.

**Đo trên trình duyệt**: popup Thêm mới còn **2 icon ⓘ**, không còn đoạn chữ hướng dẫn nào; hover ra
đúng nội dung, tooltip đúng class chuẩn. Chiều cao thân popup **636 → 588px (bớt 48px)** — đo bằng cách
chèn lại 2 đoạn chữ cũ rồi so. Chế độ Xem: nhãn "Cuộc họp" có ⓘ, hover ra đúng câu nhắc.

## Task 54 — Popup phiếu: trạng thái lên tiêu đề + bố cục 2 cột ✅

User: *"Trạng thái đưa lên tiêu đề popup / Thông tin đang bị kéo quá dài theo chiều dọc / mở rộng popup,
chia 2 phần: nội dung chính bên trái + panel bên phải"*.

**Sửa component dùng chung `components/modal/V2BaseModal.vue`** (user duyệt): thêm slot **`title-suffix`**
ngay trong `<h5 class="modal-title">`. Thuần bổ sung — popup không truyền slot thì render y hệt trước
(đã bỏ `text-truncate` định thêm: tiêu đề dài trước nay xuống dòng, cắt "…" là mất chữ mà không có
tooltip thay thế). 30+ popup khác dùng lại được khi cần badge/chip cạnh tiêu đề.

**Bố cục mới của `BookingFormModal.vue`** — popup `size="lg"` → **`xl`** (đo: 1140px):

| Cột TRÁI (8/12, 765px) — ô NHẬP | Cột PHẢI (4/12, 383px) — chỉ ĐỌC |
|---|---|
| Hướng đăng ký (chỉ khi Thêm mới) | Thông tin phiếu: Người đặt · Công ty · Ngày tạo *(chế độ Xem)* |
| Cuộc họp / Nội dung sử dụng | Cảnh báo vượt sức chứa |
| Phòng họp & thời gian | Cuộc họp đã chọn (tóm tắt) |
| Nội dung cuộc họp *(Xem, phiếu từ cuộc họp)* | Dải giờ bận trong ngày |
| | Người tham dự · Kết quả xử lý *(chế độ Xem)* |

Lịch sử (`SystemInfoSection`) để **ngang cả 2 cột** ở dưới — timeline có cột ngày + nội dung, nhét vào
panel 4/12 là vỡ chữ.

**Rút ngắn chiều dọc, ngoài việc chia cột:**
- **Trạng thái** rời khối "Thông tin phiếu" → badge cạnh tiêu đề popup; kèm chữ xám "Từ cuộc họp"/"Tự đặt".
- **Bỏ khối "Hướng đăng ký" ở chế độ Xem** — radio khoá cứng chỉ để đọc mà tốn nguyên một card (đo 76px);
  thông tin đó nay là chữ cạnh tiêu đề.
- Gộp **Phòng · Ngày · Từ giờ · Đến giờ** vào MỘT hàng (trước là 2 hàng); Mục đích 4/12 + Nội dung 8/12.
- Panel phải dùng dòng "nhãn : giá trị" (`.side-row`) thay vì `V2BaseLabel` + ô chỉ đọc (panel hẹp,
  nhãn-trên/giá-trị-dưới cao gấp đôi mà không thêm thông tin gì).
- Dải giờ bận xếp 2 dòng (giờ + trạng thái / người đặt) cho vừa bề ngang panel — đo `scrollWidth` = `clientWidth`, không tràn.

**Đo trên trình duyệt** (chiều cao NỘI DUNG `scrollHeight`, khung nhìn thân popup 617–680px):

| Chế độ | 2 cột | Nếu ép về 1 cột | Bớt | Còn phải cuộn? |
|---|---|---|---|---|
| Xem phiếu (từ cuộc họp) | **612px** | 887px | −275px | **Không** |
| Thêm mới — Gắn với cuộc họp | **557px** | 647px | −90px | **Không** |
| Thêm mới — Nhu cầu khác | **682px** | 784px | −102px | Không (lệch 2px) |

Trước Task 54, cả 3 chế độ đều phải cuộn dọc. Cách đo: chèn CSS ép 2 cột về `width: 100%` ngay trên
trang rồi so `scrollHeight` — cùng nội dung, chỉ khác bố cục.

**Kiểm thêm**: màn hình hẹp 900px → 2 cột tự xếp chồng, không tràn ngang. Màn Tình trạng phòng: bấm ô
trống ra "Đăng ký phòng họp" (không cuộn), bấm khối phiếu ra "Xem phiếu đặt phòng" kèm badge. Lỗi
trùng giờ / quá khứ vẫn hiện INLINE (ngay dưới hàng giờ), không phải toast. Popup Xem phòng họp (dùng
chung `V2BaseModal`) tiêu đề không bị cắt.

**e2e — đã sửa, CHƯA chạy**: ca B2 đổi chỗ neo lỗi trùng giờ (`.v2-error` nay nằm ở hàng NGAY DƯỚI hàng
giờ, vì mỗi ô giờ chỉ rộng 2/12 — nhét câu lỗi dài vào trong ô là vỡ 5-6 dòng giữa các ô nhập).

## Task 55 — Popup phiếu: bỏ chia card, xếp lại thứ tự, panel hiện thông tin phòng ✅

User: *"Không cần chia nội dung theo các card ⇒ tốn nhiều diện tích / Xếp các nội dung theo thứ tự hợp
lý / Khi chọn Phòng ⇒ hiển thị các thông tin của Phòng sang panel bên phải"*.

**1. Bỏ hẳn `V2BaseFormSection`** trong popup (còn **0** card). Mỗi card tốn ~76px chỉ cho khung +
tiêu đề. Thay bằng một dòng chữ nhỏ `.group-title` (12px, #475569, không viền, không nền) — đúng nếp
"UI phẳng/gọn" user vẫn chọn.

**2. Thứ tự cột trái theo đúng trình tự người dùng điền:**
`Hướng đăng ký` → `Việc gì` (cuộc họp / mục đích + nội dung) → `Phòng & thời gian` (2 ô lọc phụ trợ
đứng NGAY TRÊN ô Phòng vì chúng là công cụ để chọn nó) → `Ai phụ trách, mấy người` → `Ghi chú`.

**3. Panel phải — khối "Thông tin phòng" MỚI**, hiện ngay khi chọn phòng: Phòng · Vị trí · Sức chứa ·
Giờ mở cửa · Quản lý · *Duyệt phiếu* ("Phải chờ quản lý duyệt" / "Đặt xong là dùng được") · Tiện nghi
(chip). Chưa chọn thì ghi "Chọn phòng để xem thông tin phòng." Panel đầy đủ theo thứ tự:
Thông tin phòng → cảnh báo vượt sức chứa → Dải giờ bận → Cuộc họp đã chọn → (Xem) Thông tin phiếu →
Người tham dự → Kết quả xử lý.

**BE kèm theo:**
- `BookableMeetingRoomResource` (+`location`, `open_time`, `close_time`, `manager_name`, `description`)
  — trước đây cố tình cắt hết field quản trị; nay panel cần "phòng ở đâu, mở giờ nào, ai quản lý".
  ⚠️ VẪN KHÔNG trả `checkin_qr_token` (credential check-in QR) — cửa sau đó đóng vĩnh viễn.
- `DetailMeetingRoomBookingResource` thêm khối `room{...}` cùng khuôn — popup **Xem** không gọi
  `meeting/rooms/bookable` nên không có khối này thì panel trống đúng lúc người duyệt cần xem sức chứa.
- Eager load `room.amenities`, `room.manager.info`, `purpose` ở **7 chỗ** `$booking->load(...)` và
  `with(['amenities','manager.info'])` ở `bookableForCurrentEmployee()` — tránh N+1.

**Đo trên trình duyệt** (chiều cao NỘI DUNG `scrollHeight` / khung nhìn):

| Chế độ | Trước Task 55 (có card) | Sau (phẳng) | Phải cuộn? |
|---|---|---|---|
| Thêm mới — Nhu cầu khác | 682px | **459px** (khung 464) | **Không** |
| Xem phiếu tự đặt | ~612px | **409px** (khung 414) | **Không** |

Panel đổi theo phòng: chọn "Phòng B nhỏ" → *Tầng 4 · 8 người · Đặt xong là dùng được*; đổi sang
"Phòng lớn A" → *KHu A, tầng 4 · Phải chờ quản lý duyệt · 2 chip tiện nghi* (đo chip cách nhau 4px,
panel không tràn ngang). Dòng "Sức chứa" TỰ ẨN khi phòng chưa khai sức chứa, không in dòng rỗng.

**1 lỗi câm bắt được**: `.booking-chips/.booking-chip` vốn nằm trong `BookingDetailModal.vue` đã xoá ở
Task 52 → chip tiện nghi/người tham dự render dính liền thành một chuỗi chữ ("Bàn họp 8 ngườiWifi tốc
độ cao"). Đã chuyển style sang popup.

**Kiểm lại luồng**: lưu phiếu mới OK (DPH-2026-02391, đã xoá sau khi đo); màn Tình trạng phòng cả 2
luồng (ô trống → Đăng ký, khối phiếu → Xem) đều có panel thông tin phòng.

**e2e — đã sửa, CHƯA chạy**: helper `fillDatePickerInput()` bấm ra `.section-header` để đóng popup
lịch — class đó biến mất cùng card, đổi sang `.group-title`.

### Task 55b — bỏ tiêu đề "Phòng họp & thời gian" ở popup XEM (cả 2 hướng đăng ký)

User chốt 19/09/2026 (2 nhịp: trước cho hướng "gắn cuộc họp", sau bổ sung "bỏ cả ở loại đặt theo nhu
cầu khác"). Chế độ Xem không có 2 ô lọc phụ trợ nên nhánh này chỉ còn vài ô CHỈ ĐỌC — thêm một dòng
tiêu đề nữa là chữ nhiều hơn nội dung. Điều kiện cuối: `v-if="!isShow"`.

Đo lại, cột trái **0 tiêu đề nhóm** ở cả hai:

| Popup Xem | Nội dung | Khung | Cuộn? |
|---|---|---|---|
| Phiếu từ cuộc họp | 360px | 365px | Không |
| Phiếu nhu cầu khác | 387px | 392px | Không |

Form **Thêm/Sửa GIỮ NGUYÊN** 2 tiêu đề ("Hướng đăng ký", "Phòng họp & thời gian") — bên đó có 5-6 ô
nhập nên vẫn cần mốc phân nhóm, và helper e2e `fillDatePickerInput()` bấm `.group-title` để đóng popup
lịch cũng chỉ chạy ở form Thêm (đã đo lại: vẫn còn đủ).

### Task 55c — căn giữa ô lọc "Chỉ phiếu của tôi"

User: *"căn giữa dòng so với các item lọc khác (hiện đang lệch lên trên)"*.

**Tái hiện trước khi sửa** (đo DOM, hàng cuối bộ lọc `/meeting/bookings`):
tâm ô "Hướng đăng ký" = **257**, tâm công tắc "Chỉ phiếu của tôi" = **249** ⇒ lệch **8px** lên trên.
Nguyên nhân: công tắc chỉ cao **19px** trong khi ô lọc nhãn floating cao **36px**, mà cột lọc canh
theo MÉP TRÊN.

**Sửa**: bọc công tắc bằng `.booking-filter-switch` (`min-height: 36px` + `align-items: center`) —
cao đúng bằng một ô lọc rồi canh giữa. CSS đặt ở khối `<style>` của TRANG (nội dung slot biên dịch
trong phạm vi trang), **KHÔNG** đụng `V2BaseSmartFilterPanel` (98 màn dùng chung).
Nhân tiện bổ sung `@import '@/assets/scss/v2-styles.scss'` — trang này trước đây **thiếu hẳn** khối
`<style>` mà skill `list-page` bắt buộc.

**Đo lại**: 2 ô cùng hàng đều có tâm **257**, lệch **0px**, cao bằng nhau 36px. Bấm công tắc vẫn chạy
đúng: **1 request**, bảng lọc còn 1 dòng, bảng vẫn đủ 10 cột.

## Task 56 — Phiếu từ cuộc họp: thêm Loại meeting / Khách hàng / Chủ trì + popup thành phần ✅

User: *"với phiếu đặt từ meeting ⇒ hiển thị thêm: Loại Meeting, Khách hàng (nếu có), Người chủ trì,
click vào số người tham gia xem popup danh sách thành phần meeting"*.

**BE** — `DetailMeetingRoomBookingResource` thêm khối `meeting_info`: `code · name · type_name ·
customer_name · host_name · members[]`. `members` gộp **company_members + customer_members** của CUỘC
HỌP, mỗi dòng `{name, role, group}` (Nội bộ / Khách mời).
⚠️ KHÔNG dùng `participants` của phiếu: phiếu chỉ đồng bộ thành phần NỘI BỘ (dòng có `employee_id`),
trong khi `attendee_count` đếm CẢ khách mời — lấy nhầm nguồn thì bấm vào "N người" ra danh sách ngắn
hơn chính con số đó. `host_name` lấy `employee_infos.fullname` (accessor `Employee::fullname` trả NULL).
Eager load `meeting.meeting_type`, `meeting.host.info`, `meeting.company_members`,
`meeting.customer_members` ở `loadDetail()`.

**FE** — khối cuộc họp ở popup Xem nay có: Tiêu đề · **Loại meeting** · **Khách hàng** *(ẩn hẳn ô khi
meeting không có khách)* · **Người chủ trì** · **Số người tham gia** · Nội dung.
Số người là `<button class="v2-cell-link">` ("2 người" + icon 👥) mở **popup con `modal-meeting-members`**
(`V2BaseModal`, khuôn modal-lồng-modal đã có tiền lệ ở chính màn này với popup xác nhận Duyệt/Hủy).
Không có thành phần thì in số trơn, KHÔNG để nút bấm chết.

**Đo trên trình duyệt**: popup Xem phiếu `DPH-2026-01385` hiện đủ *Loại meeting: Họp với Nhà cung cấp ·
Khách hàng: DNS MEDIA TEST · Người chủ trì: E2E Assign · Số người tham gia: 2 người*; bấm vào →
popup "Thành phần cuộc họp" (phụ đề "Cuộc họp: Test phòng hợp") liệt kê **1. E2E Assign — Nội bộ**,
**2. Nguyễn Đăng NAm — GĐ — Khách mời**; số dòng khớp đúng số người. Đóng popup con bằng **Đóng** hay
**×** đều chỉ đóng nó, popup phiếu vẫn mở (đo: `.modal.show` còn đúng `modal-booking-form`).

**e2e — đã sửa, CHƯA chạy**: ca P6-1 (`meeting-room-sync.api.spec.ts`) chốt thêm khối `meeting_info`
(có `code`, `type_name`, `host_name` khác rỗng) và **`members.length` = `attendee_count`**.

## Task 57 — Rà toàn bộ nút theo skill `button-convention` ✅

Rà 4 màn đã đụng trong đợt này (`/meeting/bookings`, popup phiếu, `/meeting/room-board`,
`/meeting/room-purposes`). **Đạt sẵn**: mọi `V2BaseButton` đều có icon + `size="sm"`; toolbar đúng màu
(Tạo mới teal · Import **cam** · Xuất Excel **xanh lá**) và đúng lề `mr-2 mb-2`; thứ tự footer popup
(chính → danger → Đóng cuối); chữ đúng bảng chuẩn; mọi nút đổi trạng thái đều có popup xác nhận.

**5 điểm lệch đã sửa:**

| # | Lệch | Sửa |
|---|---|---|
| 1 | `submitSave()` của popup phiếu (POST/PUT) **không có lớp tải** (mục 6b) | thêm `$safeLoadingStart()` trước lệnh gọi + `$safeLoadingFinish()` trong `finally` |
| 2 | `approveItem/rejectItem/cancelItem` ở **cả 2 màn** (bookings + room-board) không có lớp tải, lại bọc `$confirm` **trong** `try` | tách: hỏi TRƯỚC → `try { $safeLoadingStart() … } finally { $safeLoadingFinish() }` |
| 3 | Icon "Từ chối" dùng `ri-close-line` (dấu × đóng) | đổi `ri-close-circle-line` — nút footer, `acceptIcon` popup, icon cột hành động, cả 2 màn |
| 4 | Câu hỏi xác nhận chỉ có mã phiếu, **không nêu hệ quả** (mục 6c) | *"Duyệt phiếu 'DPH-…'? Phòng X sẽ bị giữ 09:00 - 10:00."* / *"Hủy phiếu 'DPH-…'? Phòng X sẽ được nhả ra cho người khác đặt."* |
| 5 | Nút "Bỏ lọc phòng" (`/meeting/room-board`) — chữ nằm trong nhóm **KHÔNG dùng** của mục 4.2 | đổi thành **"Xem tất cả phòng"** + icon `ri-list-check-2` (đặt theo KẾT QUẢ; không dùng "Làm mới" vì nút này chỉ bỏ ghim 1 phòng, không reset cả bộ lọc) |

**Xung đột skill ↔ spec — user chốt theo SKILL (19/09/2026):** mục 5 cấm "Từ chối"/"Hủy phiếu" ở cột
hành động danh sách (2 thao tác phủ quyết cần đọc phiếu trước), trong khi brief Task 16 lại bắt "đồng
bộ y hệt footer chi tiết". → **Bỏ 2 nút khỏi cột hành động**, chỉ còn **Sửa · Duyệt · Lịch sử**; Từ
chối / Hủy phiếu làm ở footer popup Xem (đã có sẵn). 2 hàm `rejectItem()/cancelItem()` GIỮ NGUYÊN —
popup emit thẳng vào chúng.

**Đo trên trình duyệt**: cột hành động 2 dòng hiện tại chỉ còn `Lịch sử` (đúng cờ BE), không còn
`Hủy`; bấm Lưu khi thiếu dữ liệu → 422, **lớp tải đã tắt** (không kẹt), 6 lỗi inline hiện đúng, popup
vẫn mở; `$safeLoadingStart/Finish` tồn tại trên instance (không ném lỗi).

**e2e — đã sửa, CHƯA chạy** (`meeting-room-booking.spec.ts`):
- `createBooking()` nay tự gắn `purpose_id` (Phase 6 bắt buộc) — nạp 1 lần ở `beforeAll` qua
  `/meeting/room-purposes/options`. **Không có bước này thì chính `beforeAll` đỏ và cả bộ in
  "did not run"**.
- A2: bộ nút mới (Sửa · Duyệt · Lịch sử; khẳng định **không** còn Xem/Từ chối/Hủy) + kiểm cột Mục đích.
- A3: mở popup bằng link Mã (nút "Xem" đã bỏ từ Task 46).
- C1/C2: bấm Từ chối / Hủy phiếu ở **footer popup Xem**, kiểm thêm popup phiếu tự đóng sau khi lưu.
- C3: sau khi duyệt, cột hành động còn Sửa + Lịch sử.

## Task 58 — Thiết kế lại màn Tình trạng phòng họp: MOCKUP (chờ user chốt) ⏸

User: *"Tham khảo /assign/my-todo → tab Lịch làm việc để thiết kế lịch hợp lý hơn. Tạo file mockup
html trước để chốt thiết kế trước khi sửa."*

**Mockup**: `.plans/gop-db/quan-ly-phong-hop/mockup/room-board.html` (mở bằng `file://`, không cần server).

**Nguồn token** (memory "Demo HTML HRM dùng style V2 thật" — KHÔNG tự chế palette):
`CalendarHeader.vue` (view-toggle active `#2e71c3`, nav tròn 30px, nút "Hôm nay" `#0a99a7`),
`WeekGrid.vue` (lưới bo 10px, viền `#d6dde6`, header gradient `#f3fdfe→#e2f6f9` + gạch `#20d9ea`,
hôm nay `rgba(10,153,167,.05)` + số bo tròn gradient), `WorkItemCard.vue` (thẻ viền trái 3px, nền
nhạt theo màu loại, tiêu đề 12px, badge chấm trạng thái). Màu trạng thái phiếu lấy đúng BE
`MeetingRoomBooking::statusColor()`.

**3 view đề xuất** (thay 3 tab hiện tại):
1. **Ngày** — Phòng (hàng) × Giờ (cột). Cột phòng hiện thêm **sức chứa · vị trí**; phiếu là thẻ trải
   đúng số cột giờ; ô ngoài giờ mở cửa **gạch chéo, không bấm**; rê vào ô trống hiện **+** để đặt nhanh.
2. **Tuần** — 1 phòng × 7 ngày, hàng giờ — khuôn y hệt lưới Tuần của Lịch làm việc.
3. **Thẻ phòng** — mỗi phòng 1 thẻ: trạng thái (Đang họp / Sắp họp / Trống), **trống tới mấy giờ**,
   lịch kế tiếp, tiện nghi, có phải chờ duyệt không, nút *Xem lịch phòng* + *Đặt phòng*.

**Thêm so với bản hiện tại**: thanh điều khiển 1 hàng (toggle + ‹ nhãn kỳ › + Hôm nay + nút Đăng ký),
hàng **chip trạng thái kèm số đếm** (bấm để lọc) thay panel lọc chiếm chỗ, **vạch đỏ "Bây giờ"**,
chú thích màu.

**Đã đo trên trình duyệt** (mockup): thẻ 08:00-10:00 rộng 170px = **2 cột giờ** (1 cột 89px) ✓;
có vạch "Bây giờ" ✓; 3 view đổi qua lại OK (Ngày 5 thẻ · Tuần 12 hàng giờ + 4 thẻ + cột hôm nay nổi
bật · Thẻ phòng 3 thẻ đủ 3 trạng thái) ✓; **0 lỗi console**, không tràn ngang ở 1512px.

✅ **User chốt "ok" 19/09/2026** — đã dựng vào code màn thật, xem Task 59.


## Task 59 — Dựng thiết kế mới vào màn Tình trạng phòng họp ✅

Theo đúng mockup Task 58 (user chốt "ok").

**`pages/meeting/room-board/index.vue`**
- **Bỏ `b-tabs`** -> 3 nút chuyển view (`v-show` theo `activeView`: `day` | `week` | `cards`), giữ
  `role="tab"` + thêm `data-testid="rb-view-*"`. Lý do bỏ: thanh điều khiển chung phải nằm NGOÀI cả 3
  view, mà `b-tabs` thì mỗi tab là một pane riêng.
  ⚠️ Mất `lazy` của b-tabs -> **tự giữ nếp lazy-load** bằng 2 cờ `weekTabOpened` / `statusTabOpened`
  trong watcher `activeView` (không thì mở màn là gọi luôn cả 3 API).
- **Một cụm điều hướng dùng chung**: `‹ nhãn kỳ ›` + "Hôm nay" (view Ngày lùi/tiến 1 NGÀY, view Tuần
  1 TUẦN, view Thẻ không có kỳ). Trước đây mỗi tab một cụm nút riêng — 3 chỗ phải sửa khi đổi hành vi.
- **Hàng chip trạng thái kèm số đếm** (Tất cả · Đang họp · Sắp họp · Trống), bấm để lọc. Số đếm tính
  từ CHÍNH dữ liệu đang có: view Thẻ dùng `state` BE trả, view Ngày/Tuần tự suy từ phiếu trong ngày —
  không gọi thêm API. 3 ô lọc cũ (công ty · tiện nghi · sức chứa) thu về cuối hàng chip.
- **Chú thích màu** (4 trạng thái phiếu + ngoài giờ + vạch "Bây giờ").
- **Thẻ phòng** giàu hơn: meta phòng (sức chứa · vị trí), "Đang họp … đến HH:mm", Người đặt, **Kế
  tiếp**, **Duyệt phiếu** (phải chờ duyệt / đặt xong dùng luôn), + 2 nút **Xem lịch phòng** (nhảy sang
  view Tuần đúng phòng) và **Đặt phòng** (mở popup, ép hướng "Nhu cầu khác" + chọn sẵn phòng).
- Lịch tuần (FullCalendar) kéo về cùng token với lưới Tuần của Lịch làm việc bằng `::v-deep .fc-*`
  (viền `#d6dde6`, header gradient + gạch `#20d9ea`, cột hôm nay gạch chân `#0a99a7`, sự kiện viền
  trái 3px). `--fc-today-bg-color` **chỉ ăn ở ô THÂN lịch** — cột tiêu đề hôm nay phải tô tay
  (đo: nền trong suốt).
- Dọn: bỏ import `V2BaseIconButton` + 3 khối style `.rb-toolbar*` không còn markup nào dùng.

**`components/meeting-room/RoomTimelineGrid.vue`**
- Đổi sang token lịch (viền `#d6dde6`, bo 10px, header gradient + gạch `#20d9ea`, cột phòng `#fbfcfe`).
- Khối phiếu **2 dòng** khi rộng ≥ 2 ô: tiêu đề + `08:00 - 12:00` + chấm màu & tên trạng thái.
- **Ô ngoài giờ mở cửa**: gạch chéo, `cursor: not-allowed`, tooltip "Ngoài giờ mở cửa", **bấm không
  ăn** (trước đây trông y hệt ô trống, bấm vào mới bị BE chặn).
- Ô trống **hover hiện dấu `+`**.

## Đo trên trình duyệt (đều là số lấy từ DOM)

| Kiểm | Kết quả |
|---|---|
| Thanh điều khiển | 3 nút Ngày/Tuần/Thẻ phòng, nút active nền `rgb(46,113,195)` = `#2e71c3` đúng token; nhãn kỳ `19/09/2026`; có nút Đăng ký phòng |
| Chip | 4 chip `Tất cả 2 · Đang họp 0 · Sắp họp 0 · Trống 2`; 3 ô lọc gọn ở cuối hàng |
| Chú thích | đủ 6 mục |
| Lưới Ngày | 52 ô; phiếu in `Test phòng hợp \| 08:00 - 12:00 \| Đã duyệt`; viền ô `rgb(214,221,230)` = `#d6dde6`; header gradient đúng |
| Ô ngoài giờ | **tái hiện bằng cách ép giờ mở cửa 10:00** (phiếu thật 08:00-12:00 -> lưới nới ra 08:00): **8 ô** gạch chéo, `cursor: not-allowed`, tooltip "Ngoài giờ mở cửa" |
| Vạch "Bây giờ" | lúc đo là 21:30 > giờ đóng cửa 20:00 nên **đúng là không hiện** (`showNowLine=false`, đã kiểm `nowMinute=1289 > gridEnd=1200`) |
| Chip lọc | bấm "Đang họp" -> lưới còn **0 phòng**; bấm "Tất cả" -> **2 phòng** |
| View Tuần | nhãn đổi `14/09/2026 - 20/09/2026`, chọn phòng -> lịch render **2 sự kiện**, header gradient + gạch `rgb(32,217,234)` |
| View Thẻ phòng | nhãn "Tình trạng lúc này", 2 thẻ; thẻ in đủ `8 người · Tầng 4 \| Hôm nay: Không còn lịch nào \| Duyệt phiếu: Đặt xong là dùng được` + 2 nút |
| Nút trên thẻ | "Xem lịch phòng" -> sang view Tuần; "Đặt phòng" -> popup Tạo mới, hướng `other`, phòng 1618 chọn sẵn, panel hiện đúng thông tin phòng |
| Tổng thể | không tràn ngang ở 1512px; **0 lỗi build/Vue** (2 lỗi console còn lại là `menu-settings` 400 + favicon 404, có sẵn từ trước) |

**e2e — đã sửa, CHƯA chạy**: `meeting-room-board.spec.ts` thay **11 chỗ** `getByRole('tab', …)` bằng
`[data-testid="rb-view-day|week|cards"]` (tab giờ là nút chuyển view, không còn vai trò `tab` của
bootstrap-vue).

## Task 60 — Tình trạng phòng: lọc trạng thái, khung giờ theo cấu hình, lọc gọn, tên phòng nổi bật ✅

### 1. Chỉ hiện phiếu ĐÃ CHỐT
`MeetingRoomService::VALID_BOOKING_STATUSES` từ `[Chờ duyệt, Đã duyệt, Hoàn thành]` → **`[Đã duyệt,
Hoàn thành]`** (dùng chung cho `board` / `status-board` / `week`). Màn này chỉ để biết **phòng nào đã
được đăng ký**, phiếu chờ duyệt mới là đề nghị.

⚠️ **Đánh đổi phải biết**: `assertNoOverlap()` VẪN coi phiếu Chờ duyệt là đang giữ giờ → một ô nhìn
"trống" trên lưới vẫn có thể bị BE từ chối vì trùng phiếu chờ duyệt của người khác. Có chủ đích, đã ghi
ngay tại hằng số.

**Đo**: DB có 3 phiếu trong ngày (Đã duyệt + **Chờ duyệt** + **Đã hủy**) → lưới hiện **đúng 1** phiếu
Đã duyệt; `bookings` BE trả về cũng chỉ 1.

### 2. Khung giờ bám ĐÚNG cấu hình
`RoomTimelineGrid`: bỏ cơ chế **tự nới lưới** theo phiếu; `gridStart/End` nay chính là `open_time` /
`close_time` (cấu hình `general_regulations` qua `resolveBoardConfig`). Phiếu lòi ra ngoài chỉ hiện
phần nằm trong, mép có mũi tên ←/→ sẵn có. Bỏ luôn class gạch chéo "ngoài giờ" của Task 58 — nay
không còn cột nào ngoài giờ để gạch.
**Đo**: cột đầu `07:00`, cột cuối `19:30`, **26 cột** = đúng khung 07:00–20:00.

### 3. Bộ lọc gọn hơn
3 ô (Công ty · Tiện nghi · Sức chứa) thu vào **một nút "Bộ lọc"** có **badge số điều kiện đang áp**;
panel mở/đóng bên dưới hàng chip. Hàng chip nay chỉ còn 4 chip + nút.
**Đo**: panel đóng mặc định (cao 0) → bấm mở cao 80px, đủ 3 ô; nhập "Sức chứa ≥ 5" → badge hiện **1**,
lưới còn **1 phòng**. Hàng chip cao **32px**.

### 4. Tên phòng nổi bật
Cột phòng: tên **13px / 700 / `#0f172a`**, dòng phụ (sức chứa · vị trí) **11px / `#94a3b8`**
(trước đó hai dòng gần như cùng cỡ và độ đậm). Đo đúng các giá trị trên từ `getComputedStyle`.

**e2e — đã sửa, CHƯA chạy**:
- `meeting-room-board.api.spec.ts` C1: **đảo kỳ vọng** — phiếu Chờ duyệt nay **KHÔNG** được hiện trên
  board (bản cũ khẳng định phải hiện). Giữ ca lại thay vì xoá để ai sửa `VALID_BOOKING_STATUSES` là đỏ ngay.
- `meeting-room-board.spec.ts` A3: đổi từ "khung giờ tự nới" sang "khung giờ = đúng cấu hình, 26 cột,
  cột đầu 07:00 / cột cuối 19:30".

## Task 61 — Chờ duyệt vẽ mờ/gạch chéo · bỏ chú thích "Ngoài giờ" · màn Cấu hình phòng họp ✅

### 1. Phiếu Chờ duyệt quay lại lưới, vẽ MỜ + GẠCH CHÉO
`VALID_BOOKING_STATUSES` nhận lại `STATUS_CHO_DUYET` (đảo lại Task 60). Lý do quay đầu: BE
`assertNoOverlap()` VẪN coi phiếu chờ duyệt là đang giữ giờ — giấu đi thì ô nhìn "trống" mà đặt vào
lại báo trùng giờ. FE: `.rtg-booking--pending` = `repeating-linear-gradient` + viền `dashed` +
`opacity .85`, nhận diện bằng **`Number(block.status) === 1`** (KHÔNG so chuỗi `status_text` — đổi
một chữ ở BE là hỏng thầm lặng).
Nền gạch chéo phải là **`background-image`** chứ không phải `background`: `bookingStyle()` gán màu nền
inline, dùng shorthand là mất luôn màu trạng thái.

**Đo**: lưới 2 phiếu — `Test phòng hợp (Đã duyệt)` viền `solid`, opacity 1, không gạch chéo;
`KT cho duyet gach cheo (Chờ duyệt)` có class pending, **gạch chéo**, viền `dashed`, opacity **0.85**.

### 2. Bỏ "Ngoài giờ mở cửa" khỏi thanh chú thích
Task 60 đã bỏ cột ngoài giờ nên mục này thành chú thích cho thứ không còn tồn tại. Chú thích nay:
Đã duyệt · Chờ duyệt (ô mẫu **cũng gạch chéo**) · Hoàn thành · Đã hủy · Bây giờ.
🐛 **Lỗi câm bắt được**: ô mẫu Chờ duyệt ban đầu KHÔNG gạch chéo — `:style="{ background: … }"`
(shorthand) đè mất `background-image` của class. Đổi sang `backgroundColor` (đo lại: `true`).

### 3 + 4. Menu "Cấu hình" + màn cấu hình dạng hub
- `components/subsystem-menu/meeting.js`: thêm mục **CUỐI** sidebar `Cấu hình` → `/meeting/settings`,
  gate `['Khai báo phòng họp']` (khớp gate route BE).
- `pages/meeting/settings/index.vue` — **hub**: lưới thẻ (icon tròn + tên + mô tả + mũi tên), khuôn
  `.gcard` của `SubsystemHubOverview.vue` để 2 màn landing cùng họ; hiện có 1 thẻ **Giờ mở cửa phòng họp**.
- `pages/meeting/settings/room-hours.vue` — form: Công ty áp dụng · Giờ mở cửa · Giờ đóng cửa + dòng
  giải thích (khung giờ này quyết định lưới Tình trạng phòng + chặn đặt ngoài giờ; giờ riêng của phòng
  thắng). Đổi công ty thì **nạp lại giờ của công ty đó** (mỗi công ty một cấu hình) — không thì lưu đè nhầm.
- BE: `MeetingSettingController` (`GET/POST meeting/settings/room-hours`, gate `Khai báo phòng họp`),
  ghi vào `general_regulations.meeting_room_open_time/close_time` theo `company_id`, `firstOrNew`
  (công ty mới chưa có dòng). **Cố tình KHÔNG** thêm field vào
  `Timesheet\...\GeneralRegulationController::update()` — danh sách trắng của module khác.

**Đo end-to-end**: `/meeting/settings` hiện 1 thẻ; bấm vào ra form điền sẵn `07:00`/`20:00` + đúng công
ty; sửa giờ mở thành **09:00** → toast "Lưu cấu hình thành công" → lưới Tình trạng phòng **bắt đầu từ
09:00, còn 22 cột** (trước là 07:00 / 26 cột). Trả lại 07:00–20:00 sau khi đo.
Validate: gửi `open 10:00 / close 09:00` → **422** `Giờ đóng cửa phải sau giờ mở cửa`, trả theo field.
Mục "Cấu hình" xuất hiện đúng 1 lần ở sidebar, trỏ `/meeting/settings`.

**e2e — đã sửa, CHƯA chạy**: `meeting-room-board.api.spec.ts` C1 **trả lại** kỳ vọng "phiếu Chờ duyệt
PHẢI thấy trên board" (Task 60 từng đảo ngược), kèm ghi chú vì sao quay đầu.

## Task 62 — Lịch Tuần bám cấu hình · chip + chú thích cùng hàng · fix lỗi UI ✅

### 1. "Các lịch chỉ lấy khung giờ theo cấu hình"
Task 60 mới sửa lưới **Ngày**; lịch **Tuần** (FullCalendar) vẫn vẽ trọn **00:00–24:00** → 2 view của
cùng một màn hiện 2 khung giờ khác nhau, phải cuộn qua mấy tiếng trống mới thấy lịch.
- Thêm `slotMinTime`/`slotMaxTime` + hàm `applyConfigToWeekCalendar()` gọi sau mỗi lần `board` trả
  `config` (giờ mở cửa đổi theo CÔNG TY đang lọc, không phải hằng số).
- Phải gọi **`api.setOption()`** trên instance đang sống: đổi giá trị trong object `weekCalendarOptions`
  KHÔNG tự đẩy xuống FullCalendar v5 (nó chỉ đọc lúc mount).
**Đo**: cấu hình công ty của tài khoản test là **08:30–17:30** → lưới Ngày `08:30 → 17:00` (**18 cột**),
lịch Tuần slot `08:30 → 17:00`. Hai view khớp nhau.

### 2. Chip lọc + chú thích màu CÙNG MỘT HÀNG
Gộp `.rb-legend` vào `.rb-chip-row`, ngăn cách bằng một vạch dọc mảnh.
**Đo**: tâm chip và tâm cụm chú thích **lệch 0px**; hàng cao **32px** (trước là 2 dòng riêng), không tràn ngang.

### 3. Lỗi UI đã fix
| 🐛 Lỗi | Đo trước khi sửa | Sau khi sửa |
|---|---|---|
| **Khối phiếu đè lên cột tên phòng**: từ Task 60 lưới không nới nữa, phiếu bắt đầu TRƯỚC giờ mở cửa cho `grid-column` ≤ 0 nên khối bị đẩy ra ngoài lưới | khối ở `x=246` trong khi ô giờ đầu ở `x=426` | kẹp `colStart0 = max(0, …)`, `colEnd0 = min(totalCols, …)`; phiếu nằm TRỌN ngoài khung thì không vẽ. Khối giờ bắt đầu đúng `x=426`, có mũi tên `←` báo còn kéo dài ra ngoài |
| **Lịch Tuần cao 928px** (`height: 'auto'`) — phải cuộn cả trang mới thấy hết tuần | 928px | `height: 620` + `expandRows: true` → **620px**, hàng giờ tự chia đều |
| Mũi tên ←/→ trước chỉ mang nghĩa "phiếu qua đêm" | — | nay mang thêm nghĩa "kéo dài ra ngoài KHUNG GIỜ đang xem" |

**Rà thêm, không thấy lỗi**: không tràn ngang ở 1512px lẫn 900px (lưới tự cuộn ngang, cột phòng
`sticky`); chữ trong khối phiếu không tràn; thẻ phòng 2 thẻ cao đều 184px, 2 nút cùng hàng, chữ không
tràn; chú thích tự ẩn ở view Thẻ phòng; nút ‹ › + "Hôm nay" đổi đúng tuần (14/09→07/09→về tuần hiện tại).

**e2e — đã sửa, CHƯA chạy**: ca A3 **bỏ hard-code 07:00-20:00**, đọc `config` từ chính API `board` rồi
so với DOM — giờ mở cửa là cấu hình THEO CÔNG TY, DB mỗi máy một khác (đã dính thật: công ty của tài
khoản e2e trên máy dev là 08:30-17:30).

## Task 63 — View Tuần: gộp ô chọn phòng vào bộ lọc (cascade, bắt buộc) + header lịch gọn ✅

### 1. Lỗi ô chọn phòng — tái hiện trước khi sửa
Đo DOM lúc bấm ô "Phòng" ở view Tuần: **2 select2 ở trạng thái `--open` cùng lúc** (1 nhìn thấy + 1
container mồ côi cao 0px), do ô phòng nằm LẺ trong thân view trong khi select2 công ty/tiện nghi nằm ở
panel lọc — 3 view dùng `v-show` nên select2 của view ẩn vẫn sống trong DOM. Dời ô phòng vào panel lọc
làm nó dựng lại ở đúng một chỗ → chỉ còn **1 dropdown nhìn thấy** khi mở.

### 2. Gộp vào bộ lọc, sau Công ty, cascade, bắt buộc
- Ô **Phòng** nay nằm trong `.rb-filter-panel`, thứ tự đo thật: **Công ty → Phòng * → Tiện nghi →
  Sức chứa tối thiểu**.
- **Cascade**: `weekRoomOptions` lọc `rooms` theo `filters.company_id` (BE đã lọc khi có `company_id`,
  nhưng lúc không lọc thì trả phòng mọi công ty → lọc lại ở FE cho khớp ô Công ty ngay cạnh).
- **Bắt buộc**: `allowClear=false` + `syncWeekRoom()` — vào view Tuần mà chưa chọn thì lấy phòng đầu;
  phòng đang chọn không còn hợp lệ (đổi công ty) thì chọn lại phòng đầu, KHÔNG gọi API `week` của
  phòng thuộc công ty khác. Vào view Tuần cũng **tự mở panel lọc** (trường bắt buộc không được giấu
  sau một cú bấm). Công ty không có phòng nào → hiện dòng "Công ty đang chọn chưa có phòng nào đặt được".
- **Đo cascade**: đổi công ty → CN Hải Phòng: giữ "Phòng B nhỏ" (vẫn hợp lệ); đổi → Tân Phát: **tự
  nhảy sang "Phòng lớn A"**; bỏ lọc công ty: danh sách trở lại **2 phòng**, giữ nguyên phòng đang chọn.
  Lịch luôn hiện, không còn màn trống "Chọn phòng để xem lịch tuần".

### 3. Header lịch tuần gọn hơn
Tự dựng bằng `dayHeaderContent` (trả `domNodes`, không nối chuỗi HTML): dòng trên **thứ** (T2…CN) nhỏ
màu `#0a7c88`, dòng dưới **số ngày** đậm; hôm nay số **bo tròn 22px gradient, chữ trắng** — khuôn
`WeekGrid.vue` của màn Lịch làm việc. Mặc định FullCalendar in "T2 14/09" một dòng dài, 7 cột nhìn rối.
**Đo**: header `T2 14 · T3 15 · … · CN 20`, ô hôm nay `width 22px`, `border-radius 50%`, chữ trắng;
header cao 69px; lịch vẫn 620px, 2 sự kiện; nút "Tuần trước/Tuần sau" vẫn đổi đúng kỳ (→ 07/09–13/09).

**e2e — đã sửa, CHƯA chạy**: E1 + G1 bỏ chờ `rb-week-empty` (view Tuần nay TỰ chọn phòng nên màn trống
đó gần như không còn xuất hiện), chuyển sang chờ `.rb-week-room-field`. Các mốc khác giữ nguyên
(`button[title="Tuần trước|Tuần sau"]` vẫn đúng vì nút điều hướng chung đổi `title` theo view).

## Task 64 — Bộ lọc 1 hàng 4 ô · tiện nghi chọn bằng ô tích · view Tuần bỏ "Hôm nay" ✅

1. **4 ô lọc trên ĐÚNG một hàng**: mỗi ô `col-md-3` (trước là 4+4+5+3 = **16 cột** nên ô Sức chứa rơi
   xuống dòng 2 ngay khi view Tuần bật ô Phòng).
   **Đo**: view Ngày 3 ô / **1 hàng**; view Tuần 4 ô (Công ty · Phòng * · Tiện nghi · Sức chứa) / **1 hàng**.

2. **Lọc tiện nghi dùng `CheckboxMultiSelect`** (component dùng chung) thay select2 multiple: danh sách
   có **ô tích**, ô tìm trong danh sách, "Chọn tất cả / Xóa tất cả", giá trị đã chọn hiện thành chip.
   **Đo**: tích "Bàn họp 8 người" → chip hiện, badge bộ lọc = **1**, lưới còn **1 phòng**; bỏ tích →
   về **2 phòng**, badge biến mất.

3. **View Tuần bỏ nút "Hôm nay"** (`v-if="activeView !== 'week'"`) — điều hướng tuần đã có ‹ ›, nhãn kỳ
   luôn nói rõ đang xem tuần nào.
   **Đo**: view Ngày còn nút, view Tuần **không còn**.

**e2e**: không ca nào bám nút "Hôm nay" hay ô lọc tiện nghi của màn này → **không phải sửa spec**.

## Task 65 — Thanh tiêu đề Lịch tuần: thứ và ngày chung 1 dòng ✅

`.rb-fc-dayhead` đổi `flex-direction: column` → `row` (gap 5px, căn giữa), vòng tròn "hôm nay" thu từ
22px → 20px, `.fc-col-header-cell-cushion` padding `8px` → `5px`.

**Đo trước**: `nameTop 363` / `numTop 377` (2 dòng), ô tiêu đề cao **69px**.
**Đo sau**: cả 7 ô `sameRow = true` (tâm 2 span lệch < 2px, vd "T2 14" name x=375 / num x=393),
ô tiêu đề cao **47px** — dôi 22px cho phần lưới giờ. Hôm nay (T7 19) vẫn giữ vòng tròn gradient.

**e2e**: không spec nào bám `.rb-fc-dayhead` / `.fc-col-header` → không phải sửa spec.

## Task 66 — Màn Cấu hình dựng theo khuôn panel "Phê duyệt" của phân hệ Công việc ✅

Bỏ lưới thẻ `.ms-card` (Task 61), dựng lại `pages/meeting/settings/index.vue` theo đúng nhánh
**nav-mode** của `components/sale/SaleHubSidebar.vue` — panel mà menu **Phê duyệt** (phân hệ Công
việc) đang dùng: `.dtop` (tên + "N nhóm · M mục") › `.navwrap` = cột nhóm `.subcats/.scat` bên trái
+ `.subdetail` bên phải (`.sdh` + danh sách `.rows/.row` có icon, mô tả, mũi tên).

**KHÔNG import component gốc**: nó là flyout gắn sidebar (`position: fixed`, tự đọc cây menu phân
hệ, kèm tìm kiếm/yêu thích/gần đây). Ở đây là một TRANG với danh sách cấu hình tự khai → chỉ mượn
khuôn + **đúng bộ số đo đo được từ panel thật**.

**Đối chiếu số đo (panel "Phê duyệt" → màn Cấu hình)** — trùng khít:

| | Panel gốc | Màn Cấu hình |
| --- | --- | --- |
| `.dtop` padding | 18px 26px 14px | 18px 26px 14px |
| `.dhead` | 17px / 800 | 17px / 800 |
| `.dsub` | 12.5px · `#7a8699` | 12.5px · `#7a8699` |
| `.subcats` | rộng 224px · nền `#faf9fd` · padding 10px 8px | y hệt |
| `.scat.on` | cao 36px · radius 9px · nền `rgb(46,113,195)` · 700 | y hệt |
| `.sdh` | 15px / 800 | 15px / 800 |
| `.row` | 13px `#37414f` · radius 9px | 13px `#37414f` · radius 9px |

`--acc` dùng `#2e71c3` = đúng màu chip đang chọn của panel gốc, cũng là màu nút view đang bật của
màn Tình trạng phòng họp. Dữ liệu chuyển thành **nhóm → mục** (hiện 1 nhóm "Phòng họp" / 1 mục
"Giờ mở cửa phòng họp") để thêm cấu hình sau chỉ việc khai thêm nhóm.

**Kiểm bằng trình duyệt**: bấm dòng "Giờ mở cửa phòng họp" → sang `/meeting/settings/room-hours`,
tiêu đề "Giờ mở cửa phòng họp", form nạp đúng công ty đang chọn.
**e2e**: không spec nào bám `.ms-card` / `/meeting/settings` → không phải sửa spec.

## Task 67 — Cấu hình là màn CHUNG của phân hệ · hub hiện thẳng ô nhập · mỗi hub có nút Lịch sử ✅

**FE**
- `/meeting/settings` nay là **cấu hình chung của phân hệ Meeting** (tiêu đề "Cấu hình", dòng phụ
  "N nhóm cấu hình · phân hệ Meeting"); "Cấu hình phòng họp" chỉ là **1 hub** trong cột trái.
- Bấm hub → panel phải hiện **thẳng các trường cần cấu hình**, KHÔNG thêm một cấp trang nữa:
  trang `pages/meeting/settings/room-hours.vue` (Task 61) **đã xoá**, ruột chuyển thành component
  `components/meeting-room/RoomHoursSettingPanel.vue`. Hub mới sau này = thêm 1 component cùng khuôn.
- Mỗi hub có nút **Lịch sử** (`secondary`, `ri-history-line`) nằm cùng hàng với tiêu đề hub, mở
  `CatalogHistoryModal` dùng chung. Nút **ẩn hẳn** khi chưa biết phạm vi (chưa chọn công ty) —
  hiện xám rồi mở popup rỗng thì user tưởng mất lịch sử. Panel con báo phạm vi lên bằng
  `scope-change` ⇒ lịch sử luôn đúng công ty đang xem; đổi hub thì xoá phạm vi cũ.

**BE**
- `CatalogHistoryService::TABLES` thêm khoá **`meeting_room_settings`** (`Giờ mở cửa`/`Giờ đóng cửa`).
  Khoá đặt theo **HUB**, không theo tên bảng: giá trị nằm ở `general_regulations` — bảng dùng chung
  nhiều màn và đã có lịch sử riêng (`general_regulation_history`); lấy tên bảng làm khoá thì nút
  Lịch sử của hub này sẽ hiện lẫn thay đổi của màn khác. `table_id` = `company_id`.
- `MeetingSettingController::updateRoomHours()` chụp giá trị trước khi ghi rồi
  `logUpdate(...)`. Ảnh chụp đi qua `MeetingRoom::resolveConfig()` như lúc đọc: công ty chưa khai gì
  thì giá trị đang có hiệu lực là **giờ mặc định**, ghi log `null → 08:30` là sai sự thật.
  Không đổi gì → `logUpdate()` tự bỏ qua, không sinh log rác.

**Kiểm bằng trình duyệt (công ty Tân Phát)**
- Panel hiện thẳng 3 ô: Áp dụng cho công ty · Giờ mở cửa `08:30` · Giờ đóng cửa `17:30` + nút Lưu.
- Đổi giờ đóng cửa `17:30 → 18:00`, Lưu → DB `general_regulations.meeting_room_close_time = 18:00:00`
  và **đúng 1 dòng** `catalog_histories`: `{"Giờ đóng cửa":"17:30"} → {"Giờ đóng cửa":"18:00"}`
  (chỉ trường ĐỔI, không kèm giờ mở cửa).
- Popup Lịch sử: `20/09/2026 08:47 · Thay đổi thông tin · Người thực hiện: E2E Assign — PHÒNG THIẾT
  BỊ Ô TÔ 2 · Giờ đóng cửa: 17:30 → 18:00`, có đủ bộ lọc 3 nhóm hành động + danh sách người thực hiện.
- Lần Lưu mà **không đổi gì** (ca đầu, gõ hụt vào datepicker) → API 200 nhưng **không sinh log** — đúng.
- Đã trả cấu hình về `17:30` và **xoá 2 dòng lịch sử kiểm thử** (`catalog_histories` còn 0 dòng khoá này).

**e2e**: không spec nào bám `/meeting/settings` hay trang `room-hours` → không phải sửa spec.

## Task 68 — Bỏ chọn công ty · 3 cấu hình mới (nhắc nhận/trả phòng, cho đặt ngoài giờ) ✅

### 1. Bỏ ô "Áp dụng cho công ty"
Cấu hình luôn thuộc **công ty của người đang đăng nhập** (`current_company_role`, rơi về
`info->company_id`). BE **BỎ QUA hẳn `company_id` trong payload/query** — không chỉ ẩn ô ở FE: giữ
lại thì ai cũng sửa được cấu hình công ty khác bằng cách đổi query string. FE hiện dòng
"Áp dụng cho: <tên công ty>" để người dùng biết mình đang khai cho ai.

### 2. Ba cấu hình mới
| Trường | DB (`general_regulations`) | Ý nghĩa |
| --- | --- | --- |
| Nhắc nhận phòng trước (phút) | `meeting_room_checkin_reminder_minutes` (MỚI, default 15) | thông báo web/app trước giờ bắt đầu |
| Nhắc trả phòng trước (phút) | `meeting_room_checkout_reminder_minutes` (đã có từ 2026_09_17_000008) | nhắc trước giờ kết thúc, chỉ phiếu **chưa trả phòng** |
| Cho đặt ngoài khung giờ hoạt động | `meeting_room_allow_outside_hours` (MỚI, default 0) | gate luật giờ mở/đóng cửa khi lưu phiếu |

`0 phút` = **tắt nhắc** (không phải "thiếu dữ liệu") → validate `min:0`, trần 1440.
Thêm `meeting_room_bookings.checkin_reminded_at` (cặp với `checkout_reminded_at` có sẵn) để command
chạy mỗi phút không bắn trùng.

### 3. Command nhắc lịch — `meeting:send-booking-reminders`
`app/Console/Commands/SendMeetingRoomBookingReminders.php`, lịch **everyMinute + withoutOverlapping**
(mốc nhắc của mỗi phiếu rơi vào phút khác nhau). Quét theo cửa sổ = số phút LỚN NHẤT đang khai rồi
lọc lại theo cấu hình của công ty **CỦA PHÒNG** (giống mọi luật khác của phiếu). Dùng lại
`sendBookingNotification()` (prefix `[DPH]`, map `employees.id → employee_info_id`).
- Nhắc nhận phòng → người đặt + người tham dự; điều kiện `status = Đã duyệt`, `checkin_at` rỗng.
- Nhắc trả phòng → người đặt + người phụ trách (KHÔNG bắn cả phòng 20 người); điều kiện
  `checkout_at` rỗng = **chưa trả phòng sớm**.

⚠️ **BẪY đã dính và đã xử lý**: `EmployeeInfoService::sendNotification()` gọi
`auth()->user()->employee_info_id` khi không truyền tham số người gửi → chạy trong CLI là ném lỗi,
bị `try/catch` của `sendBookingNotification()` **nuốt mất**: command in "thành công" mà không thông
báo nào tới nơi. Nay `sendBookingNotification()` nhận thêm `$sender`, command truyền bản ghi
`employees` của người đặt phiếu.

### 4. Validate phiếu đặt phòng
`MeetingRoomBookingService::validateBusinessRules()` chỉ kiểm giờ mở/đóng cửa khi
`allow_outside_hours = 0`. Nhánh `else` cũ đổi thành `elseif (!isSameDay)` — để `else` thì bật cấu
hình sẽ vô hiệu hoá luôn **trần 72 giờ** của phiếu qua đêm (phiếu trong ngày rơi vào `else`).

### 5. Đo thật (công ty Tân Phát)
- Form: không còn select công ty, dòng "Áp dụng cho: CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT",
  4 ô + radio Có/Không (mặc định **Không**).
- Lưu `20 / 5 / Có` → DB `ci=20, co=5, allow=1`; lịch sử ghi đúng nhãn tiếng Việt:
  `{"Nhắc lịch nhận phòng trước (phút)":"15"...,"Cho đặt ngoài khung giờ hoạt động":"Không"}` →
  `{"...":"20", "...":"5", "...":"Có"}`.
- Phiếu **06:00–06:30** (ngoài 08:30–17:30): cấu hình **Có** → `200` tạo được; cấu hình **Không** →
  `422 "Khoảng giờ đặt phải nằm trong giờ mở cửa của phòng (08:30:00 - 17:30:00)"`; phiếu 09:00
  trong giờ vẫn `200`.
- Command: phiếu bắt đầu sau 10' (cấu hình 20') → **"Nhắc nhận phòng ... Còn 20 phút"**; phiếu kết
  thúc sau 3' (cấu hình 5') → **"Nhắc trả phòng ... Còn 5 phút"**; `notifications` 242 → 245.
  Chạy lại lần 2 → **0 phiếu** (không nhắc trùng). Đặt nhắc nhận phòng = **0** → không nhắc.
  Phiếu đã có `checkout_at` → **không** nhắc trả phòng.
- Đã trả lại nguyên trạng: xoá 2 phiếu + 3 thông báo kiểm thử, phiếu có sẵn #2390 về giá trị cũ,
  cấu hình về `08:30 / 17:30 / 15 / 10 / Không`, xoá log lịch sử kiểm thử.

### 6. e2e
Thêm ca **A4b** vào `meeting-room-booking.api.spec.ts`: bật cấu hình → phiếu 05:00 `200`, tắt →
`422`, và **trả lại cấu hình cũ trong `finally`** (ca này ghi vào cấu hình chung của công ty).
Kiểm ca đã nhận diện bằng `--list`; **chưa chạy** bộ test (theo chỉ đạo chỉ chạy khi được yêu cầu).

## Task 69 — Thẻ phòng: màu theo trạng thái + thanh live · Select phòng có dòng phụ công ty ✅

### 1. Thẻ phòng — màu theo TRẠNG THÁI PHÒNG
- Badge đổi từ `status_color` của PHIẾU sang màu **trạng thái phòng** (`stateColor()` đọc thẳng
  `stateChips`): phiếu Đã duyệt luôn xanh dương nên trước đây thẻ "Đang họp" và "Sắp họp" ra **cùng
  một màu**, nhìn thẻ không phân biệt được. Nay đỏ `#DC2626` / cam `#D97706` / xanh `#16A34A`, khớp
  đúng dải chip lọc phía trên. Trạng thái duyệt của phiếu KHÔNG mất — vẫn ở dòng "Đang họp"/"Kế tiếp".
- Thêm **viền trái 4px** + nền tiêu đề nhạt cùng tông, và icon trong badge
  (`ri-broadcast-line` / `ri-time-line` / `ri-checkbox-circle-line`).

### 2. Phòng đang họp — khối "live"
Chấm nhấp nháy + chữ **ĐANG DIỄN RA** + "còn 2h39" + thanh tiến độ buổi họp (`liveProgress()`:
% đã trôi, kẹp trong [0,100], cắt giờ bằng substring — KHÔNG `new Date(iso)`, bẫy múi giờ của dự án).
Animation đặt **chỉ trên chấm và thanh** (khối rỗng), KHÔNG lên khối chứa chữ — bẫy "chữ nhoè vì
animation trên khối chứa chữ". Có `@media (prefers-reduced-motion: reduce)` tắt animation.

### 3. Select phòng họp — dòng phụ là TÊN CÔNG TY
- Component dùng chung mới `components/SubtextSelect.vue` (khuôn `DescriptionInfoSelect.vue`:
  `templateResult` + `escapeMarkup`, tự escape text, **tự gắn 🔒** cho option khoá +
  `lockedMarkerHandled: true` — helper `select2LockedOption` nhường quyền cho wrapper tự khai template).
  Danh sách chọn: 2 dòng; **ô đã chọn: 1 dòng** (nhồi 2 dòng vào ô là vỡ chiều cao lưới form).
- BE: `BookableMeetingRoomResource` trả thêm `company_name`, `bookableForCurrentEmployee()` eager
  load `company` (chống N+1).

### 4. Đo thật trên trình duyệt
- Thẻ "Phòng B nhỏ" (đang họp 09:00–12:00): `data-state=dang_hop`, viền trái `rgb(220,38,38) 4px`,
  badge nền đỏ + icon, live "ĐANG DIỄN RA · còn 2h39", thanh **12%** (09:21 ⇒ 21/180 phút ✓).
- Thẻ "Phòng lớn A" (trống): viền trái `rgb(22,163,74)`, badge xanh, **không** có khối live.
- Select phòng: option 1 = "Phòng B nhỏ" + dòng phụ "CN HẢI PHÒNG - CÔNG TY CP…", 11px `#94a3b8`,
  `nameTop 450` vs `subTop 470` (đúng 2 dòng). Chọn xong ô hiện 1 dòng cao **30px**, không có dòng
  phụ; panel phải đổi đúng phòng ⇒ `v-model` qua wrapper vẫn chạy.
- Sửa thêm: dòng phụ trên hàng đang rê chuột (nền xanh `rgb(88,151,251)`, chữ trắng) bị chìm →
  đổi sang `rgba(255,255,255,.82)`; đo lại: hàng highlight `rgba(255,255,255,0.82)`, hàng thường
  `rgb(148,163,184)`.

### 5. e2e (đã sửa spec, CHƯA chạy)
- `meeting-room-board.spec.ts` F1: thêm đo viền trái đỏ 4px + khối live + **% thanh tiến độ trong
  khoảng 5–60%** (phiếu setup đã trôi ~17%); F2: viền xanh + **không** có khối live.
- `meeting-room-booking.spec.ts`: mở dropdown phòng, đo `.sts-option__name` = tên phòng,
  `.sts-option__sub` khác rỗng, 11px `#94a3b8`, nằm DƯỚI tên; chọn xong ô **không** có dòng phụ.
- Ca cũ dùng `hasText` (khớp chuỗi con) nên option 2 dòng không làm đỏ ca nào.

## Task 70 — Form đặt phòng: dải bận/rảnh có màu · chặn ngày giờ quá khứ · khối lọc phòng rõ nghĩa ✅

### 1. Panel phải — liệt kê CẢ dải bận lẫn dải rảnh, tô màu
- Computed `daySlots` xen kẽ khoảng **bận** (phiếu đang giữ giờ) và khoảng **rảnh** (phần còn lại
  của giờ hoạt động). BẬN đỏ `#DC2626`, RẢNH xanh `#16A34A` (viền trái + nền nhạt), kèm **chú thích
  màu** ngay trên danh sách. Trạng thái duyệt của phiếu vẫn giữ màu BE trả (`status_color`) ở chip.
- 3 quy tắc đã xử lý: khoảng bận **chồng nhau** (phiếu chờ duyệt được phép trùng) gộp bằng
  `Math.max` để không sinh dải rảnh ảo; ngày là **hôm nay** thì cắt bỏ phần đã trôi qua; **không rõ
  giờ hoạt động** thì chỉ liệt kê dải bận (thà thiếu còn hơn bịa khung 07:00–20:00 rồi mời đặt vào
  giờ bị chặn).
- **BE**: `MeetingRoomService::attachEffectiveHours()` gắn `effective_open_time/close_time`
  (phòng > công ty > mặc định) cho `GET meeting/rooms/bookable`, gom cấu hình theo công ty bằng 1
  query `whereIn` (không N+1). Tiện thể **sửa một lỗ cũ**: phòng không khai giờ riêng thì dòng
  "Giờ mở cửa" ở panel trước đây **biến mất**, nay hiện đúng giờ theo công ty.

### 2. Không cho chọn ngày/giờ quá khứ
`:disabled-date` (so theo NGÀY, không so mốc hiện tại — nếu không hôm nay bị khoá từ 00:01) và
`:disabled-time` cho cả 2 ô giờ, **chỉ áp khi ngày đang chọn là hôm nay** (ngày mai trở đi khoá theo
giờ hiện tại sẽ chặn nhầm cả buổi sáng).

### 3. Khối lọc phòng — nhìn ra là BỘ LỌC
2 ô "Sức chứa tối thiểu" + "Tiện nghi" trước đây nằm trần giữa các ô bắt buộc nên user tưởng là
trường phải điền. Nay bọc trong khối: nền xám + **viền đứt**, icon phễu, tiêu đề "LỌC NHANH DANH
SÁCH PHÒNG", ghi chú *(không lưu vào phiếu)*, nút **Xóa lọc** (chỉ hiện khi đang lọc), placeholder
đổi thành "Tất cả sức chứa"/"Tất cả tiện nghi", và **đếm số phòng khớp** — cái đếm mới là tín hiệu
rõ nhất rằng 2 ô này chỉ lọc danh sách.

### 4. Đo thật (Phòng B nhỏ, hôm nay 20/09, phiếu 09:00–12:00)
- Panel: `Bận` đỏ `09:00 → 12:00 · Đã duyệt · DNS Admin` (viền `rgb(220,38,38)`, nền `#fef2f2`) và
  `Rảnh` xanh `12:00 → 20:00 · Còn trống` (viền `rgb(22,163,74)`, nền `#f0fdf4`); dải rảnh trước
  09:00 **bị cắt đúng** vì lúc đo là 09:33. Dòng "Giờ mở cửa 07:00 - 20:00" nay hiện (phòng thuộc
  CN Hải Phòng, không khai giờ riêng).
- Lịch: ngày 1/2/19 **disabled**, hôm nay 20 chọn được, 21 chọn được.
- Ô giờ (lúc 09:36): giờ 07, 08 **disabled**, 09+ mở; chọn giờ 09 → phút 00–35 disabled, 40 mở
  (`wrongCount = 0` khi đối chiếu toàn bộ 60 ô phút); chọn 09 + 45 → ô nhận `09:45`.
- Khối lọc: `2 / 2 phòng` → nhập sức chứa 6 → `1 / 2 phòng khớp bộ lọc` + hiện "Xóa lọc" → bấm Xóa
  lọc → về `2 / 2 phòng`, ô sức chứa rỗng, nút biến mất.

### 5. e2e (đã sửa spec, CHƯA chạy)
- **Sửa ca cũ**: 2 chỗ đếm `.busy-slot-item` nay lọc `[data-slot-type="busy"]` — panel có thêm dải
  rảnh nên đếm chung sẽ ra số khác mà tưởng lỗi dữ liệu.
- **Thêm đo**: màu viền dải bận/rảnh, có ít nhất 1 dải rảnh kèm chữ "Còn trống", chú thích Bận/Rảnh;
  khối lọc (tiêu đề, "không lưu vào phiếu", đếm phòng đổi theo lọc, Xóa lọc trả về trạng thái đầu);
  ô Ngày khoá ngày hôm qua. Đóng lịch bằng bấm `.group-title`, **không dùng Escape** (Escape đóng cả
  popup + bật hộp thoại "Thông tin chưa lưu").

## Task 71 — Panel giờ bận/rảnh: khoảng ĐANG DIỄN RA gọi đúng là "Đang họp" ✅

Trước đây khoảng giờ đang diễn ra vẫn in trạng thái phiếu ("Đã duyệt", xanh dương) — người xem
không biết phòng **đang có người trong đó** hay chỉ mới được duyệt lịch. Nay khoảng bao trùm thời
điểm hiện tại hiện **"Đang họp"** đỏ `#DC2626` + icon `ri-broadcast-line` + nền đậm hơn, đúng cách
tab **Thẻ phòng** đang thể hiện.

Điều kiện gắn nhãn (`slot.live`): ngày đang xem là **hôm nay** · phiếu **Đã duyệt** · `start ≤ now < end`.
Phiếu **Chờ duyệt** dù trùng giờ vẫn giữ nhãn "Chờ duyệt" — chưa ai cho dùng phòng thì gọi là
"Đang họp" là nói sai trạng thái.

**Đo thật (Phòng B nhỏ)**
- Hôm nay lúc 09:40, phiếu 09:00–12:00 (Đã duyệt): `data-live="1"`, chữ **"Đang họp"** màu
  `rgb(220,38,38)`, icon `ri-broadcast-line`, nền `#fee2e2`.
- Ngày mai, phiếu 14:00–15:00: `data-live` rỗng, vẫn **"Đã duyệt"** màu `rgb(37,99,235)` (màu BE
  trả), icon ổ khoá. Phiếu kiểm thử đã xoá sau khi đo.

**e2e**: thêm ca **B3** — chèn phiếu bao trùm "bây giờ" bằng SQL (API chặn `start_at` quá khứ nên
không tạo được qua API), mở form với ngày hôm nay → đúng 1 dải `data-live="1"`, có chữ "Đang họp",
**không** có chữ "Đã duyệt", màu `rgb(220,38,38)`; đổi sang ngày mai → dải bận quay lại "Đã duyệt"
và không còn dải nào `data-live`. Rác dọn theo `afterAll` sẵn có (xoá booking theo `createdRoomIds`).

## Task 72 — Ô chọn giờ ở form đặt phòng bám theo cấu hình giờ mở cửa ✅

Task 70 mới chặn giờ QUÁ KHỨ; mốc ngoài khung giờ hoạt động vẫn chọn được rồi mới ăn 422 từ BE.
Nay `disabled-time` khoá thêm mốc **ngoài giờ mở cửa CÓ HIỆU LỰC của phòng đang chọn**
(giờ riêng của phòng → cấu hình công ty ở `/meeting/settings` → mặc định hệ thống).

**2 trường hợp CỐ Ý không khoá** (nếu không là chặn oan / làm chết cấu hình):
- Chưa chọn phòng hoặc không rõ giờ → không biết khoá theo mốc nào.
- Công ty bật **"Cho đặt phòng ngoài khung giờ hoạt động"** (Task 68) → BE cho lưu thì FE không
  được chặn. BE bổ sung `allow_outside_hours` cho từng phòng ở `GET meeting/rooms/bookable`
  (lấy từ cấu hình công ty CỦA PHÒNG, cùng chỗ với `effective_open_time/close_time`).

Thêm **tooltip ⓘ** trên nhãn "Từ giờ"/"Đến giờ" nói rõ vì sao nhiều mốc bị mờ: *"Chỉ chọn trong giờ
mở cửa của phòng: 08:30 - 17:30."* / *"Công ty cho phép đặt ngoài khung giờ hoạt động nên mọi mốc
giờ đều chọn được."* / *"Chọn phòng trước…"*.

**Đo thật (Phòng lớn A — công ty khai 08:30–17:30, ngày mai)**
- Cấu hình **Không** cho đặt ngoài giờ: cột giờ khoá `00–07` và `18–23`, mở `08–17`;
  giờ **08** khoá đúng 30 phút đầu (mở từ 08:30), giờ **17** mở tới 17:30 rồi khoá từ 17:31,
  giờ 12 không khoá phút nào. Tooltip: "Chỉ chọn trong giờ mở cửa của phòng: 08:30 - 17:30."
- Bật cấu hình **Có**: **không giờ nào bị khoá**, tooltip đổi sang câu "Công ty cho phép đặt ngoài
  khung giờ hoạt động…". Đã trả cấu hình về **Không** sau khi đo.

**e2e**: thêm phép đo trong ca B1 — đọc khung giờ từ dòng "Giờ mở cửa" trên panel (KHÔNG hard-code
08:30–17:30 vì đây là cấu hình theo công ty, mỗi máy/CI một khác) rồi kiểm: giờ mở cửa chọn được,
giờ ngay trước giờ mở cửa và ngay sau giờ đóng cửa bị khoá. Đóng bảng chọn giờ bằng bấm
`.group-title`, không dùng Escape.

## Task 73 — Chữ nút Lưu đổi theo việc phòng có cần duyệt hay không ✅

| Phòng | Nút | Icon | Hỏi xác nhận |
| --- | --- | --- | --- |
| `require_approval = 1` | **Lưu và gửi duyệt** | `ri-send-plane-line` | ✅ |
| `require_approval = 0` | **Lưu đăng ký** | `ri-save-3-line` | ❌ (lưu thẳng) |

**Chữ**: dùng **"Lưu và gửi duyệt"** — đúng bộ chữ của `components/V2Footer.vue`
(nút `save_and_submit_approve`) và đúng quy tắc skill `button-convention` (viết **"và"**, không viết
"&"). User viết "Lưu & gửi duyệt"; đây là khác biệt DUY NHẤT so với yêu cầu, thuộc diện
"skill thắng spec khi về hình thức UI".

**Popup xác nhận** (skill `button-convention` mục 6c — nhóm "Gửi đi để duyệt" BẮT BUỘC hỏi): hỏi
TRƯỚC khi bật lớp tải, nêu tên phòng + hệ quả + tên người duyệt, `textAccept` đúng chữ trên nút gốc:
*Gửi duyệt phiếu đặt phòng "Phòng lớn A"? Phiếu ở trạng thái Chờ duyệt cho tới khi DNS Admin duyệt.*

**Đo thật**
- Chưa chọn phòng → "Lưu đăng ký"; chọn **Phòng lớn A** (panel: "Phải chờ quản lý duyệt") → nút đổi
  thành **"Lưu và gửi duyệt"** + icon máy bay; chọn **Phòng B nhỏ** ("Đặt xong là dùng được") → về
  **"Lưu đăng ký"** + icon đĩa mềm.
- Bấm "Lưu và gửi duyệt" → **hiện popup** đúng nội dung trên → xác nhận → phiếu `DPH-2026-02391`
  trạng thái **Chờ duyệt**.
- Bấm "Lưu đăng ký" (Phòng B nhỏ) → **KHÔNG popup** (đếm `.modal.show[id^=app-confirm]` = 0) →
  phiếu `DPH-2026-02399` trạng thái **Đã duyệt**.
- Đã xoá 2 phiếu + thông báo sinh kèm.

**e2e**
- 2 chỗ bấm `getByRole('button', { name: 'Lưu' })` đổi sang `[data-testid="booking-save-button"]`
  (chữ trên nút nay động, bám chữ là ca gãy khi nhánh khác được chọn).
- Thêm ca **B4**: đo chữ nút theo 2 loại phòng (describe B tạo thêm 1 phòng `require_approval = 1`),
  bấm Lưu ở phòng cần duyệt → có popup, đúng tên phòng + chữ "Chờ duyệt" + nút "Lưu và gửi duyệt";
  bấm Hủy → không gọi API, popup đăng ký vẫn mở. Ca chỉ ĐO, không tạo phiếu.

## Task 74 — Popup Duyệt / Từ chối / Hủy / Gửi duyệt: thông tin có FORMAT ✅

Trước đây nhồi hết vào MỘT CÂU: *"Duyệt phiếu 'DPH-2026-02391'? Phòng Phòng lớn A sẽ bị giữ 14:00
22/09/2026 - 15:00 22/09/2026."* — duyệt liên tiếp nhiều phiếu thì phải đọc hết câu mới nhặt ra
được mã phiếu / phòng / giờ. Nay tách 3 phần: **câu hỏi 1 dòng** → **bảng thông tin** (nhãn xám bên
trái, giá trị đậm bên phải, khối nền `#f8fafc` viền trái xanh) → **dòng hệ quả** (xám).

**Helper dùng chung** `utils/confirmInfoHtml.js`:
- `confirmInfoHtml({ intro, rows, note })` — dựng HTML cho `message` của `$confirm()`
  (`base-confirm-modal` render bằng `v-html`). Dòng có giá trị rỗng **tự bị bỏ**, không để lại nhãn trống.
- `bookingConfirmRows(item)` — bộ dòng CHUẨN của phiếu đặt phòng (Mã phiếu · Nội dung · Phòng họp ·
  Thời gian · Người đặt) để 3 popup không mỗi cái hiện một bộ trường khác nhau.
- Style để **inline trong chuỗi**, KHÔNG thêm class + CSS vào `components/modal/base-confirm-modal.vue`
  (popup dùng chung của 70+ màn — sửa phải hỏi trước theo CLAUDE.md).
- Mọi giá trị đi qua `escapeHtml()`: nội dung phiếu là chữ NGƯỜI DÙNG nhập, chèn thẳng vào `v-html`
  là mở cửa cho HTML lạ.

**Áp cho 4 popup**: Duyệt · Từ chối · Hủy (màn danh sách) và Lưu và gửi duyệt (form) — cùng khuôn nên
4 popup của cùng một phiếu nhìn như một bộ. Dòng hệ quả riêng từng popup: duyệt → "phiếu khác trùng
giờ sẽ tự động bị từ chối"; từ chối → "người đặt nhận thông báo kèm lý do"; hủy → "phòng được nhả ra".

**Đo thật (phiếu Chờ duyệt `DPH-2026-02391`)**
- Popup **Duyệt**: tiêu đề "Duyệt phiếu đặt phòng", câu hỏi "Duyệt phiếu đặt phòng này?", bảng đúng
  5 dòng `Mã phiếu · Nội dung · Phòng họp · Thời gian (09:00 23/09/2026 → 10:00 23/09/2026) · Người đặt`,
  dòng hệ quả xám, nút `Duyệt` / `Hủy`.
- Popup **Từ chối** (mở từ footer popup Xem): cùng khuôn, **vẫn còn ô nhập lý do** (`textarea` = 1).
- Phiếu kiểm thử đã xoá (kèm log + thông báo), không duyệt/từ chối thật.

**e2e**: ca **C3** thêm đo cấu trúc popup duyệt — có câu hỏi, đủ 5 nhãn, nêu đúng tên phiếu, có dòng
hệ quả, và bảng ≥ 5 khối dòng (không phải một câu chạy dài). Ca B4 (Task 73) vẫn xanh vì popup mới
vẫn chứa tên phòng + chữ "Chờ duyệt". Ca C1/C2 không bám câu chữ nên không ảnh hưởng.

## Task 75 — Họp Online cũng chọn được phòng · có phòng thì ẩn ô Địa điểm ✅

### 1. Bỏ điều kiện "chỉ họp Trực tiếp mới có phòng"
Lý do nghiệp vụ (user chốt 20/09/2026): họp Online vẫn cần phòng — cả nhóm ngồi chung một phòng để
kết nối với đối tác. `mode_id` bị gỡ khỏi **4 chỗ**:

| Chỗ | Trước | Sau |
| --- | --- | --- |
| `MeetingRoomBookingService::bookableMeetings()` | `where('mode_id', MODE_TRUC_TIEP)` | bỏ — cuộc họp Online nay hiện trong ô "Cuộc họp" của form đăng ký |
| `…::assignMeeting()` | chặn 423 "Cuộc họp Online không cần phòng họp" | bỏ guard |
| `MeetingRoomBookingSyncService::meetingHoldsRoom()` | có phòng **+ mode = 1** + chưa hủy | có phòng + chưa hủy |
| `…::ROOM_FIELDS` | có `mode_id` | bỏ (đổi hình thức không cần kiểm trùng lại) |

Kéo theo: `releaseReason()` bỏ nhánh "Cuộc họp chuyển sang hình thức Online".
**Hệ quả quan trọng**: trước đây chuyển Trực tiếp → Online là phiếu **tự hủy im lặng**, phòng trống
ra trong khi người ta vẫn ngồi họp ở đó. Nay phiếu giữ nguyên.

### 2. FE màn Cuộc họp (`pages/assign/meeting/components/GeneralInfo.vue`)
- Ô **Phòng họp**: bỏ `v-if="form.mode_id == 1"` → hiện ở cả 2 hình thức.
- Khối **Địa điểm meeting**: thêm `v-if="!form.meeting_room_id"` → **ẩn hẳn khi đã chọn phòng**
  (phòng họp chính là địa điểm; để cả 2 ô là mời khai 2 nơi cho cùng một cuộc họp rồi lệch nhau).
  Giá trị `location` đã nhập **không bị xóa** (không tự sửa dữ liệu người dùng) — bỏ chọn phòng là ô
  hiện lại nguyên nội dung cũ. Dấu `*` nay chỉ còn phụ thuộc hình thức Trực tiếp.
- Sửa 2 chỗ chữ/ghi chú đã lỗi thời trong `BookingFormModal.vue` ("họp trực tiếp, chưa chọn phòng…").
- Validate BE không phải đổi: `location` vẫn `requiredIf(mode == 1 && không có phòng)` — đúng luật mới.

### 3. Đo thật
- Màn Tạo meeting, hình thức **Trực tuyến (Online)**: ô **Phòng họp hiện** (trước đây mất), ô Link họp hiện.
- Chọn phòng → **ô Địa điểm biến mất**; bỏ chọn phòng → **hiện lại**.
- `GET meeting/room-bookings/bookable-meetings` trả cuộc họp **Online** (trước bị lọc mất).
- `POST assign-meeting` cho cuộc họp Online → **200**, sinh phiếu `Từ cuộc họp`, trạng thái Đã duyệt.
- Đổi hình thức Online → Trực tiếp → Online (qua Eloquent để chạy hook): phiếu **giữ nguyên
  `status = 2`**, `cancel_reason` rỗng — trước đây bước này hủy phiếu.
- Dữ liệu kiểm thử (1 meeting + 1 phiếu + thông báo) đã xoá sạch.

### 4. e2e — ĐẢO 2 ca cũ (hành vi đổi, không phải test hỏng)
- `meeting-room-sync.api.spec.ts` **P4-3**: "chuyển Online → nhả phòng (phiếu Đã hủy)" →
  **"VẪN GIỮ phòng"**: phiếu còn `status = 2`, và cuộc họp khác đặt trùng giờ bị chặn **422**
  (bằng chứng phòng vẫn bị giữ — thay cho phép đo cũ "đặt lại được ngay").
- `meeting-room-sync.spec.ts` **P4UI-1**: đổi tên ca; đo ô Phòng họp hiện **ngay** không chờ chọn
  hình thức, chọn phòng → nhãn Địa điểm **rỗng** (ẩn hẳn), đổi sang Online → ô Phòng **vẫn còn** và
  giữ đúng phòng đã chọn, bỏ chọn phòng → Địa điểm hiện lại kèm dấu `*`.

## Task 76 — Chọn phòng KHÔNG còn mù: biết trống/bận theo đúng khung giờ ✅

**Vấn đề** (user nêu 20/09/2026): cả màn Cuộc họp lẫn form đăng ký đều đổ **toàn bộ phòng đang hoạt
động**, không xét giờ. Người dùng chọn trong trạng thái mù, bấm Lưu mới ăn lỗi
`Phòng đã có cuộc họp "X" lúc 09:00 - 10:00 ngày 21/09`, rồi phải tự mò từng phòng khác.
Chốt làm **A + B + C**; phiếu Chờ duyệt = **vàng, vẫn cho chọn + cảnh báo**.

### BE — `GET meeting/rooms/availability?start_at=&end_at=[&exclude_booking_id=]`
`MeetingRoomService::availabilityForSlot()`: lấy đúng danh sách phòng của `bookable` rồi gắn
- `availability`: `free` · `pending` (chỉ phiếu Chờ duyệt chạm — luật hiện tại KHÔNG chặn) ·
  `busy` (có phiếu Đã duyệt chạm),
- `conflict`: phiếu đang chiếm (tên, giờ, ngày, trạng thái, người đặt),
- `outside_hours`: khung giờ nằm ngoài giờ mở cửa (KHÔNG gộp vào `busy` — phòng vẫn trống, chỉ là
  luật giờ chặn).

Chi tiết đáng nhớ: **1 query** cho mọi phòng (`whereIn` + điều kiện giao `start < end && end > start`,
chạm mép không tính); **chỉ đọc, không `lockForUpdate`** — chốt chặn thật vẫn là `assertNoOverlap()`
có khóa lúc ghi; `exclude_booking_id` để phiếu đang sửa không tự coi mình là kẻ chiếm chỗ của mình.

### FE
- `SubtextSelect` thêm `statusText` + `tone` → mỗi option có **chấm màu + chữ trạng thái** trước dòng
  phụ: `● Đã bị giữ 14:00–15:00 · CN HẢI PHÒNG…`. Phòng **trống xếp lên đầu**, bận xuống cuối.
- **Form đăng ký** (`BookingFormModal`): nạp availability theo `slotRange` (meeting → giờ cuộc họp;
  nhu cầu khác → ngày + 2 ô giờ), debounce 350ms + chống race bằng `availabilityRequestId`.
  Thêm: cảnh báo đỏ/vàng ngay dưới ô phòng, khối **"Phòng còn trống (n)"** ở panel phải (bấm 1 phát
  đổi phòng), và **chặn Lưu ngay ở FE** khi phòng `busy` (khỏi gọi API để ăn 422). Đổi phòng thì xoá
  lỗi cũ của ô (lỗi của phòng trước treo trên phòng mới là báo sai).
- **Màn Cuộc họp** (`GeneralInfo.vue`): select phòng đổi sang `SubtextSelect` + cùng bộ trạng thái
  theo `start_date/end_date`, cảnh báo đỏ/vàng, và hàng **chip "Phòng còn trống"** (chỉ hiện khi
  phòng đang chọn không dùng được hoặc chưa chọn phòng).

### Đo thật
- API: khung trống → cả 2 phòng `free`; khung 09:30–10:30 hôm nay → `Phòng B nhỏ = busy` kèm
  `Phỏng vấn ứng viên 09:00–12:00 · Đã duyệt · DNS Admin`; tạo phiếu **Chờ duyệt** → `pending`;
  thêm `exclude_booking_id` → trở lại `free`.
- Form đăng ký (ngày mai 14:30–15:30, đã chiếm Phòng B nhỏ 14:00–15:00): dropdown hiện
  `Phòng lớn A ● Còn trống` (xếp trước) và `Phòng B nhỏ ● Đã bị giữ 14:00–15:00` (đỏ `rgb(220,38,38)`);
  chọn phòng bận → cảnh báo đỏ nền `#fef2f2` + khối "Phòng còn trống" 1 phòng; bấm **Lưu** → lỗi
  inline, **popup không đóng**, không gọi API; bấm gợi ý → đổi sang Phòng lớn A, cảnh báo biến mất.
- Màn Cuộc họp (cùng khung giờ): dropdown y hệt; chọn phòng bận → cảnh báo
  *"Phòng đã bị giữ 14:00–15:00 cho "KT chiem cho". Lưu sẽ bị chặn…"* + chip `Phòng lớn A`; bấm chip
  → đổi phòng, cảnh báo mất.
- Toàn bộ phiếu/thông báo kiểm thử đã xoá.

### e2e (đã sửa spec, CHƯA chạy)
- `meeting-room-booking.api.spec.ts` **A4c**: availability trả `free` → `busy` (kèm `conflict.status = 2`,
  `start_at = 09:00`) → `free` khi `exclude_booking_id`.
- `meeting-room-booking.spec.ts` **B5**: dropdown có nhãn "Đã bị giữ" màu đỏ, chọn phòng bận → cảnh
  báo + gợi ý phòng trống, bấm Lưu → **đếm request POST = 0** và popup vẫn mở, bấm gợi ý → đổi phòng
  và cảnh báo biến mất.

## Task 77 (mục D của tư vấn) — Hết phòng thì mách KHE TRỐNG GẦN NHẤT ✅

Task 76 giải quyết "phòng nào trống"; còn ca **mọi phòng đều bận** thì người dùng vẫn bế tắc. Nay
form mách khe trống gần nhất trong ngày và cho **đổi giờ bằng 1 nút**.

**BE** — `availabilityForSlot()` trả thêm `next_free_slot` (`{start, end}` dạng `HH:mm`) cho phòng
`busy`:
- Khe phải **dài đúng bằng thời lượng đang định đặt**, quét từ giờ người dùng muốn (hoặc giờ mở cửa,
  cái nào muộn hơn) tới giờ đóng cửa; công ty cho đặt ngoài giờ thì quét cả ngày.
- Chỉ né phiếu **ĐÃ DUYỆT**: phiếu Chờ duyệt không chặn ai (luật hiện tại) nên né nó là mách sai,
  làm người dùng tưởng phòng kín hơn thực tế.
- Hết chỗ trong ngày → `null` (FE nói thẳng thay vì mách một khung giờ sai). Phiếu qua đêm → không
  tính (không có khái niệm "khe trong ngày").
- Dữ liệu cả ngày lấy bằng **1 query** cho mọi phòng, chỉ chạy khi phiếu gọn trong 1 ngày.

**FE**
- **Form đăng ký**: khi `freeRoomSuggestions` rỗng → khối vàng *"Hết phòng trong khung giờ này —
  khe trống gần nhất trong ngày"*, mỗi dòng `Phòng X · 10:00 → 11:00` + nút **Đổi giờ** (đặt luôn
  từ giờ/đến giờ + chọn phòng). Hướng **gắn cuộc họp** chỉ hiện thông tin, KHÔNG có nút — giờ lấy
  theo cuộc họp, sửa ở đây là phiếu lệch cuộc họp rồi hook ghi đè lại.
- **Màn Cuộc họp**: hàng chip `Phòng B nhỏ 10:00–11:00`; bấm → dời **giờ** cuộc họp sang khe đó
  (giữ nguyên NGÀY) + chọn phòng.

**Đo thật** (chiếm cả 2 phòng 09:00–10:00, muốn đặt 09:30–10:30):
- API: cả 2 phòng `busy`, `next_free_slot = 10:00–11:00`.
- Form đăng ký: khối "Phòng còn trống" **0 dòng**, khối khe thay thế **2 dòng**
  `Phòng B nhỏ 10:00 → 11:00 [Đổi giờ]`, `Phòng lớn A 10:00 → 11:00 [Đổi giờ]`; bấm Đổi giờ →
  ô giờ thành **10:00 / 11:00**, phòng = Phòng B nhỏ, cảnh báo đỏ và khối gợi ý biến mất, khối
  "Phòng còn trống" hiện lại 1 phòng (khung giờ mới đã trống).
- Màn Cuộc họp: label *"Hết phòng trong khung giờ này — khe gần nhất:"* + 2 chip; bấm chip →
  giờ họp thành `22/09/2026 10:00 → 11:00`, phòng = Phòng B nhỏ.
- Phiếu kiểm thử + thông báo đã xoá.

**e2e**: **A4c** kiểm thêm `next_free_slot = 10:00–11:00` khi bận và **null** khi trống;
**B6** (mới) chiếm nốt phòng còn lại → khối "Phòng còn trống" rỗng, khối khe thay thế có dòng
`10:00`, bấm "Đổi giờ" → ô giờ 10:00/11:00, phòng được chọn, cảnh báo + gợi ý biến mất.

## Task 78 — Vá lỗ hổng "chọn phòng xong, nhập tiếp, lưu thì phòng đã bị chiếm" ✅ (phần rẻ)

Task 76/77 mới trả lời "lúc CHỌN phòng nào trống". Người dùng chọn phòng xong còn ngồi nhập nội
dung/người tham dự vài phút — trong khoảng đó người khác kịp đặt mất phòng, bấm Lưu là ăn 422.

**1. Kiểm lại NGAY TRƯỚC KHI GỬI** (`BookingFormModal.submitSave`): chờ đúng 1 request
`availability` rồi mới quyết định. Bị chiếm → chặn tại form, **không gửi request nào**, giữ nguyên
mọi dữ liệu đang nhập, hiện cảnh báo nêu tên phiếu + người chiếm và khối "Phòng còn trống" đã cập nhật.

**2. Theo dõi SỐNG khi form đang mở** (45 giây/lần, cả form đăng ký lẫn màn Cuộc họp): phòng bị
chiếm mất trong lúc đang nhập thì cảnh báo hiện ngay, không đợi tới lúc bấm Lưu. Nhịp 45s là đủ —
mục tiêu là "phát hiện trong lúc còn đang nhập", không phải đồng bộ tức thời. Timer dọn ở
`beforeDestroy` (để sót là rời màn rồi vẫn bắn request nền).

**3. Màn Cuộc họp**: thêm watcher `formError.meeting_room_id` — BE vừa từ chối vì phòng bị chiếm thì
nạp lại tình trạng NGAY, hàng "Phòng còn trống"/"khe gần nhất" hiện đúng thực tế mới; người dùng đổi
phòng rồi bấm Lưu lại, KHÔNG mất dữ liệu đang nhập.

**Đo thật (đúng kịch bản user nêu)**
- Điền đủ form, chọn Phòng B nhỏ lúc **còn trống** (không cảnh báo) → gọi API cho "người khác" chiếm
  đúng khung giờ → bấm **Lưu**: **0 request POST**, popup còn nguyên, ô Nội dung vẫn là
  `KT race chiem phong`, lỗi + cảnh báo ghi rõ *"Phòng đã bị giữ 09:00–10:00 cho "KT nguoi khac chiem
  truoc" (E2E Assign)"*, khối "Phòng còn trống" cập nhật còn **Phòng lớn A**.
- Bấm gợi ý → đổi sang Phòng lớn A (hết cảnh báo) → chiếm nốt phòng đó bằng API, **không thao tác gì
  trên màn** → cảnh báo **tự hiện** (nhịp 45s) kèm khe thay thế `10:00 → 11:00`.
- Phiếu + thông báo kiểm thử đã xoá.

**e2e**: thêm ca **B7** — chọn phòng lúc còn trống, tạo phiếu chiếm chỗ bằng API, bấm Lưu → cảnh báo
hiện, lỗi inline dưới ô phòng, **đếm POST = 0**, popup vẫn mở, ô Nội dung giữ nguyên giá trị.

**2 quyết định user chốt 20/09/2026** (đã ghi vào `design.md` mục "Quyết định đã chốt"):
- **KHÔNG làm giữ chỗ tạm** — dừng ở mức kiểm lại trước khi lưu + theo dõi sống. Tránh thêm
  cột/bảng + lệnh dọn, và tránh cảnh "phòng bị giữ ảo" khi người dùng bỏ form giữa chừng.
- **Lưu cuộc họp mà phòng bị chiếm thì CHẶN CẢ cuộc họp** (giữ nguyên hành vi hiện tại), không lưu
  meeting rồi âm thầm bỏ phòng. Bù bằng: nạp lại tình trạng + gợi ý phòng/khe để đổi 1 bấm, dữ liệu
  đang nhập không mất.

⇒ Task 78 **khép lại, không còn việc tồn**.

## Task 79 — Lưu meeting báo "Có lỗi xảy ra": lỗi 422 bị NUỐT ✅

**Triệu chứng (user báo)**: lưu cuộc họp hiện toast chung *"Có lỗi xảy ra"*, mở Network mới thấy
`422 {"message":"The given data was invalid.","errors":{"meeting_room_id":["Khoảng giờ đặt phải nằm
trong giờ mở cửa của phòng (08:30:00 - 17:30:00)"]}}`.

**Nguyên nhân**: `pages/assign/meeting/create.vue` và `pages/assign/meeting/_id/edit.vue` chỉ bắt
**400 / 403 / 423**. Laravel `ValidationException` trả **422** với khuôn `{ message, errors }` —
KHÁC khuôn 400 của dự án (`data.data`) — nên rơi xuống nhánh `else` ⇒ toast chung, câu lỗi thật
biến mất. Luật phòng họp (giờ mở cửa, trùng lịch) do hook đồng bộ Phase 4 ném ra đúng bằng
`ValidationException`, nên MỌI lỗi phòng họp khi lưu meeting đều bị nuốt.

**Sửa**: thêm nhánh `422` ở cả 2 file — đổ `data.errors` (fallback `data.data`) vào
`paymentProfile/setFormError` để lỗi hiện **inline dưới đúng ô** (`MeetingForm` tự nhảy sang tab
chứa lỗi), toast lấy **câu lỗi đầu tiên** thay vì câu chung.

**Đo thật**
- *Tái hiện*: gọi thẳng `POST assign/meeting/944` với giờ 18:00–19:00 (ngoài khung 08:30–17:30) →
  đúng payload 422 user dán. Trên màn Sửa (code cũ): toast "Có lỗi xảy ra", **không** có lỗi inline.
- *Sau khi sửa*: chặn đúng lệnh lưu trả 422 y như BE → lỗi đỏ hiện **ngay dưới ô "Phòng họp"**:
  *"Khoảng giờ đặt phải nằm trong giờ mở cửa của phòng (08:30:00 - 17:30:00)"*, tab "Thông tin" có
  chấm đỏ báo tab chứa lỗi, màn **ở lại** `/assign/meeting/944/edit` (dữ liệu đang nhập còn nguyên).
- Cuộc họp + phiếu + thành viên kiểm thử đã xoá.

**e2e**: thêm ca **P4UI-3** trong `meeting-room-sync.spec.ts` — chặn lệnh lưu trả 422 (không phụ
thuộc cấu hình giờ mở cửa của máy chạy test), đo lỗi hiện inline dưới ô "Phòng họp" và URL vẫn ở
màn Sửa.

⚠️ **Đáng rà tiếp**: khuôn `catch` này (chỉ bắt 400/403/423) được copy ở nhiều màn khác trong repo —
màn nào gọi API có `ValidationException` cũng sẽ nuốt lỗi y hệt. Chưa rà đại trà trong task này.

## Task 80 — Quy hết việc đặt phòng về form "Đăng ký phòng họp" ✅

**Chốt với user 20/09/2026**: (1) form Meeting KHÔNG còn chọn phòng trực tiếp, chỉ có nút mở popup
đăng ký; (2) chỉ đăng ký được **từ trạng thái "Lên lịch" (status 1) trở đi** — nháp thì giờ còn nhảy,
giữ phòng theo giờ nháp là chiếm chỗ ảo của người khác; (3) meeting đã có phòng mà **đổi giờ thì phiếu
tự đổi theo** (giữ nguyên hành vi).

### FE — form Meeting (`GeneralInfo.vue`) nhẹ hẳn
GỠ toàn bộ: select phòng, `roomOptions` + tình trạng trống/bận, cảnh báo đỏ/vàng, chip "Phòng còn
trống", chip "khe giờ gần nhất", nhịp theo dõi 45s, watcher `formError.meeting_room_id`, các timer.
THAY bằng 1 khối gọn: `Phòng họp: <tên> [badge trạng thái phiếu]` + nút **Đăng ký phòng / Đổi phòng /
Hủy đăng ký**. Nút ẩn khi chưa đủ điều kiện và **nói rõ lý do bằng chữ** ("Lên lịch xong mới đăng ký
phòng được (bản nháp còn đổi giờ)." / "Lưu cuộc họp trước…" / "Cuộc họp đã hủy.").

⚠️ Bẫy đã dính: màn Sửa KHÔNG đổ `id` vào `form` (id nằm ở route) → chỉ đọc `form.id` là màn Sửa
luôn tưởng "cuộc họp chưa lưu" và nút không bao giờ hiện. Nay có computed `meetingId` đọc cả
`$route.params.id`.

### FE — popup dùng chung nhận "cuộc họp đặt sẵn"
`BookingFormModal` thêm prop **`presetMeeting`**: ẩn radio "Hướng đăng ký" (không cho chuyển sang
Nhu cầu khác), ô "Cuộc họp" thành dòng chữ chỉ đọc, `data.meeting_id` điền sẵn.
`selectedMeeting` ưu tiên `presetMeeting` — cuộc họp ĐÃ CÓ PHÒNG không nằm trong `bookable-meetings`
(BE lọc `whereNull meeting_room_id`), tra trong danh sách đó sẽ ra null và popup mất sạch giờ/tên.

### BE — `POST meeting/room-bookings/unassign-meeting`
Gỡ phòng khỏi cuộc họp: chỉ `meetings.meeting_room_id = null` + `save()`, hook tự hủy phiếu
(`releaseReason()` ghi "Cuộc họp đã bỏ chọn phòng"). KHÔNG dùng nút "Hủy phiếu" sẵn có: hủy phiếu mà
cuộc họp vẫn trỏ phòng thì lần lưu sau hook thấy "đang giữ phòng mà chưa có phiếu" nên **sinh lại
phiếu mới** — phòng bị giữ lại âm thầm. Quyền kiểm theo vai trò trong cuộc họp (người tạo / chủ trì).

### Đo thật (cuộc họp `KT.DANGKY.PHONG`)
- Nháp (status 0): khối hiện *"Chưa đăng ký phòng — Lên lịch xong mới đăng ký phòng được (bản nháp
  còn đổi giờ)"*, **không có** nút nào.
- Lên lịch (status 1): nút **"Đăng ký phòng"** → popup mở với dòng `KT.DANGKY.PHONG - KT dang ky
  phong tu meeting` (chỉ đọc), **không còn** radio "Nhu cầu khác", thời gian kế thừa
  `2026-09-21 09:00:00 - 10:00:00`; select phòng vẫn đủ tình trạng trống/bận (Task 76).
- Chọn "Phòng B nhỏ" → **Lưu đăng ký** → popup đóng, khối trên form Meeting đổi thành
  **"Phòng B nhỏ"** + badge **"Đã duyệt"** + 2 nút "Đổi phòng"/"Hủy đăng ký".
- **Hủy đăng ký** → popup xác nhận có format (Cuộc họp · Phòng họp · Thời gian + dòng hệ quả) →
  xác nhận → DB: `meetings.meeting_room_id = NULL`, phiếu `status = 4` lý do *"Cuộc họp đã bỏ chọn
  phòng"*; khối quay lại "Chưa đăng ký phòng".
- Dữ liệu kiểm thử đã xoá sạch.

### e2e
**Viết lại P4UI-1** (ca cũ đo select phòng — không còn đúng màn hình): nháp → không có nút + có dòng
lý do; lên lịch → nút hiện, popup có cuộc họp đặt sẵn và không cho đổi hướng; chọn phòng + lưu →
khối hiện tên phòng, badge "Chờ duyệt", ô "Địa điểm meeting" **ẩn hẳn**; hủy đăng ký → quay lại
"Chưa đăng ký phòng", ô Địa điểm hiện lại, DB phiếu `status = 4`.

## Task 81 — 4 chỉnh sau khi quy về form Đăng ký phòng ✅

### 1. Tiêu đề khối lọc trong popup đăng ký
"LỌC NHANH DANH SÁCH PHÒNG" in hoa + giãn chữ nhìn **nặng hơn cả tiêu đề cấp trên** ("Phòng họp &
thời gian"), trong khi nó chỉ là công cụ phụ trợ. Bỏ `text-transform: uppercase` + `letter-spacing`,
hạ về xám `#64748b`.
**Đo**: `.room-filter__title` = `none · 11.5px · 600`, nhỏ hơn `.group-title` (`12px · 600`).

### 2. Định dạng ngày giờ trong popup
Thêm `dateTimeText()` chuẩn hoá MỌI chuỗi ngày giờ về **`dd/mm/yyyy HH:mm`**, xử lý 2 khuôn:
chuỗi DB thô `2026-09-21 09:00:00` (cuộc họp truyền từ form Meeting) và chuỗi BE trả **giờ trước
ngày** `21:00 20/09/2026`. Áp cho ô "Thời gian (theo cuộc họp)", panel "Cuộc họp đã chọn" và **nhãn
option** của select cuộc họp. Không sửa BE (chuỗi đó nhiều màn khác đang đọc).
**Đo**: `20/09/2026 21:00 - 20/09/2026 23:26` ở cả ô lẫn panel; option
`TPE.MET.KH.26.0818 - … (20/09/2026 21:00)`.

### 3. "Lưu và Lên lịch" không còn bắt buộc Địa điểm
BE (`MeetingCreateApiRequest` + `MeetingUpdateApiRequest`): `location` chỉ `requiredIf` khi
**`status >= CHOT_LICH (2)`** + họp Trực tiếp + chưa có phòng. FE: dấu `*` cũng chỉ hiện từ Chốt lịch.
Lý do: phòng chỉ đăng ký được sau khi cuộc họp đã "Lên lịch" (Task 80) — bắt gõ địa điểm ở bước lên
lịch là ép khai chỗ tạm rồi lát nữa phải xoá.

### 4. Màn danh sách meeting
- Nút **"Đăng ký phòng họp"** (secondary, `ri-door-open-line`) mở đúng popup dùng chung, hướng mặc
  định "Gắn với cuộc họp" — người dùng chọn cuộc họp ngay trong popup, không phải mở từng cuộc họp.
  Đăng ký xong tự `loadData()` để cột Phòng họp cập nhật.
- Cột **"Phòng họp"** (200px, sau "Địa điểm", có trong cấu hình cột + danh sách xuất Excel). BE:
  `MeetingResource` trả `meeting_room_id` + `meeting_room_name`, thêm quan hệ `Meeting::meeting_room()`
  và **eager load** ở danh sách (không N+1 mỗi dòng một truy vấn).
**Đo**: header có "Phòng họp" đúng vị trí thứ 11; dòng `TPE.MET.KH.26.0817` hiện `Phòng B nhỏ`, dòng
chưa đăng ký hiện `-`; bấm nút → popup mở, có ô "Cuộc họp *" chọn được (không phải chế độ preset).

**e2e**: thêm **P4-7** (API) — `location` rỗng + `status = 1` lưu được (200); `status = 2` mà không
phòng lẫn địa điểm thì bị chặn (400).

## Task 82 — Action "Đăng ký phòng họp" theo TỪNG DÒNG ở danh sách meeting ✅

User báo "chưa thấy action". Đo lại: nút toolbar VẪN hiện (x=1168, y=195) — cái thiếu là **hành động
theo dòng**. Bổ sung vào cột Hành động: `Đăng ký phòng họp` (dòng chưa có phòng) / `Đổi phòng họp`
(dòng đã có), mở popup với **cuộc họp của đúng dòng đó** đặt sẵn. Điều kiện hiện: từ "Lên lịch"
(status ≥ 1), chưa Hoàn thành/Hủy, có quyền quản lý — cùng mốc với nút trên form Meeting (Task 80).

⚠️ **Bẫy bố cục đã dính**: `V2BaseRowActions` lấy **2 phần tử ĐẦU** của mảng làm nút icon ngoài
bảng, phần còn lại mới vào menu "⋮". Đặt hành động mới ở GIỮA mảng thì ở những dòng KHÔNG có nút Xóa
(đa số) nó bị đẩy lên thành **icon không chữ** — nhìn không ra, đúng như user phản ánh. Nay đặt
**CUỐI mảng** để luôn rơi vào menu ⋮ có chữ; nút icon ngoài bảng trở lại đúng bộ cũ (Sửa · In biên bản).

⚠️ **Bẫy dữ liệu đã dính**: `MeetingResource` tách NGÀY và GIỜ thành 2 field (`start_date` =
"20/09/2026", `start_time` = "21:00"). Lần đầu chỉ lấy `start_date` → popup hiện
*"20/09/2026 - 20/09/2026"*, **mất sạch giờ**. Nay ghép `date + time` trước khi truyền sang popup.

**Đo thật**: menu ⋮ của dòng chưa có phòng = `Tạo phiếu công tác khác · Lịch sử · Đăng ký phòng họp`;
dòng đã có phòng = `… · Đổi phòng họp`. Bấm → popup mở, ô Cuộc họp chỉ đọc
`TPE.MET.KH.26.0818 - Test meeing + dky phòng họp`, **không** có radio hướng, thời gian kế thừa
`20/09/2026 21:00 - 20/09/2026 23:26`.

**e2e**: thêm **P4UI-4** — cột "Phòng họp" của dòng hiện đúng phòng; hành động nằm TRONG menu ⋮
(không phải icon trần); bấm → popup có cuộc họp đặt sẵn và thời gian đủ `dd/mm/yyyy HH:mm` hai đầu.

## Task 83 — Chỉ người TẠO hoặc người CHỦ TRÌ mới đăng ký phòng cho cuộc họp ✅

BE vốn đã chặn ở service (`assignMeeting` / `unassignMeeting` ném 403), nhưng FE vẫn hiện nút cho
mọi người → bấm xong mới ăn lỗi. Nay đưa điều kiện ra thành **cờ** để ẩn nút từ đầu.

- **Entity** `Meeting::canBookRoom()` = `canEdit()` (người tạo **hoặc** người chủ trì) + mốc trạng
  thái của Task 80 (từ "Lên lịch", chưa Hoàn thành/Hủy). Một nguồn sự thật, không chép điều kiện.
- **Resource**: `can_book_room` có ở CẢ danh sách (`MeetingResource`) lẫn chi tiết (`MeetingTransformer`).
- **FE**: form Meeting và menu ⋮ ở danh sách đều đọc thẳng cờ, **fail-closed** (`=== true`, thiếu cờ
  là ẩn) — không tự suy quyền từ `created_by` ở FE (CLAUDE.md). Khi bị ẩn vì quyền, khối phòng nói rõ
  *"Chỉ người tạo cuộc họp hoặc người chủ trì mới đăng ký được phòng."*

**Đo thật** (tài khoản E2E Assign = employee 1180)
| Ca | can_manage | can_edit | **can_book_room** |
| --- | --- | --- | --- |
| Mình tạo (0818, status 1) | true | — | **true** |
| Người khác tạo + người khác chủ trì (837) | false | false | **false** |
| Người khác tạo, **mình chủ trì** (837) | false | true | **true** |
| Người khác tạo, status 2 (0816) | false | — | **false** |

Giao diện: dòng 0818 → menu ⋮ có "Đăng ký phòng họp"; dòng 0816 → **không còn nút ⋮** (hành động bị
ẩn). Form: meeting của mình → nút hiện; meeting người khác → bị đá sang `/show`, không có nút; set
mình làm chủ trì 837 → vào `/edit` và nút **hiện**. Đã trả `host_employee_id` của 837 về nguyên trạng.

**e2e**: thêm **P4-8** (API) — đo `can_book_room` qua 4 ca: người tạo · người khác hẳn · mình chủ trì
· bản nháp.

## Task 84 — Lỗi ẩn 422 khi MỞ popup đăng ký phòng ✅

**Triệu chứng (user báo)**: mở popup đăng ký phòng → Network có
`422 {"errors":{"start_at":["Không hợp lệ"],"end_at":["Không hợp lệ","Giờ kết thúc phải sau giờ bắt đầu"]}}`,
giao diện không báo gì.

**Tái hiện**: `GET /meeting/rooms/availability?start_at=20/09/2026 21:00&end_at=20/09/2026 23:26` → 422.

**Nguyên nhân (do chính Task 81/82 gây ra)**: khi thêm phần format hiển thị, `presetMeeting.start_at`
/`end_at` bị gán **chuỗi HIỂN THỊ** `dd/mm/yyyy HH:mm`. Nhưng 2 field đó là chuỗi **máy đọc** mà
popup đem đi gọi API xét phòng trống → BE validate `date` trượt. Lỗi rơi vào `catch` của
`loadRoomAvailability()` (chỉ `console.error`) nên **màn hình im lặng**, chỉ khác là mọi phòng mất
nhãn trống/bận.

**Sửa 3 lớp**
1. `GeneralInfo.presetMeetingForBooking`: `start_at`/`end_at` giữ **chuỗi thô** `form.start_date`
   (chuỗi hiển thị nằm ở `start_at_text`).
2. `index.vue.openRoomBookingForMeeting`: danh sách tách `start_date` (`20/09/2026`) + `start_time`
   (`21:00`) → dựng lại `YYYY-MM-DD HH:mm:00` trước khi truyền.
3. `BookingFormModal`: thêm `toApiDateTime()` nhận cả 3 khuôn (`…T…+07:00`, `YYYY-MM-DD HH:mm:ss`,
   `dd/mm/yyyy HH:mm`) và **`slotRange` trả null khi không parse được** → KHÔNG bắn request rác nữa.

**Đo lại**: request đi với `start_at=2026-09-20 21:00:00&end_at=2026-09-20 23:26:00` → **200**;
select phòng có nhãn trạng thái (`Phòng B nhỏ` → "Trống (ngoài giờ mở cửa)", `Phòng lớn A` →
"Còn trống" — đúng theo cấu hình giờ của công ty mỗi phòng tại thời điểm đo).

**e2e**: ca **P4UI-4** nay bắt mọi lượt gọi `rooms/availability` trong ca: **không lượt nào khác 200**
và query phải là `start_at=YYYY-MM-DD…` (chặn đúng lỗi này tái diễn).

## Task 85 — "Danh sách phòng họp" chuyển về menu Danh mục ✅

`components/subsystem-menu/meeting.js`: mục **Danh sách phòng họp** (`/meeting/rooms`) rời nhóm
"Quản lý phòng họp" → vào nhóm **Danh mục**, đứng trước "Tiện nghi phòng họp" (cùng họ danh mục khai
báo: phòng · tiện nghi · mục đích sử dụng). Nhóm "Quản lý phòng họp" giữ đúng phần vận hành: Đăng ký
phòng họp · Tình trạng phòng họp. **Quyền gate giữ nguyên** `['Khai báo phòng họp']` — registry này
CHÍNH LÀ lớp chặn URL, đổi quyền ở đây là mở/khoá màn ngoài ý muốn.

**Đo thật**: panel **Danh mục** = `Loại meeting · Danh sách phòng họp · Tiện nghi phòng họp · Mục đích
sử dụng phòng` (4 chức năng); panel **Quản lý phòng họp** = `Đăng ký phòng họp · Tình trạng phòng họp`
(2 chức năng); vào thẳng `/meeting/rooms` vẫn mở được (tiêu đề "Danh mục phòng họp") ⇒ gate còn sống.

**e2e — sửa 2 ca cũ bám vị trí menu** (đổi bố cục làm sai giả định của ca cũ):
- `meeting-room-board.spec.ts`: nhóm "Quản lý phòng họp" nay **2 mục** (trước 3) + assert "Danh sách
  phòng họp" KHÔNG còn ở nhóm này.
- `meeting-room.spec.ts` F1: đo "Danh sách phòng họp" ở **nhóm Danh mục** (href `/meeting/rooms`) và
  khẳng định nó không còn ở nhóm cũ.

## Task 86 — Thêm nhanh tiện nghi ngay trong form phòng họp ✅

**Yêu cầu**: "Form tạo phòng họp thêm popup cho phép thêm nhanh tiện nghi".

**Cách làm — dùng lại NGUYÊN form của màn danh mục, không dựng form thứ hai**:
- `pages/meeting/room-amenities/components/RoomAmenityModal.vue`:
  - thêm prop **`modalId`** (mặc định `modal-room-amenity`) — bootstrap-vue định danh modal bằng id,
    2 chỗ dùng trùng id thì `$bvModal.show/hide` bắn vào cả hai;
  - `submitSave()` nay **emit kèm bản ghi vừa lưu**: `this.$emit('event', body.data)` — màn danh mục
    bỏ qua tham số này nên không ảnh hưởng chỗ dùng cũ.
- `pages/meeting/rooms/components/MeetingRoomModal.vue`:
  - nút **"Thêm tiện nghi"** (`secondary size="sm"`, `ri-add-line`, `data-testid="room-quick-add-amenity"`)
    nằm CÙNG HÀNG với nhãn "Tiện nghi", dạt phải;
  - `<RoomAmenityModal modal-id="modal-room-amenity-quick">` lồng trong popup phòng (tiền lệ popup
    lồng: `#modal-meeting-members` trong `BookingFormModal.vue`);
  - `onQuickAmenitySaved(amenity)` → `loadFormOptions()` nạp lại danh mục rồi **tự tích id vừa tạo**
    vào `data.amenity_ids` (gán MẢNG MỚI, `push` tại chỗ là select2 không vẽ lại chip);
  - `canQuickAddAmenity = !isShow && hasAPermission('Khai báo phòng họp')` — BE gate
    `POST meeting/room-amenities` bằng đúng quyền này, fail-closed như CLAUDE.md.

**Đo thật trên trình duyệt (Playwright MCP)**:
- nhãn "Tiện nghi" tâm y `468.8` — nút tâm y `468.8` ⇒ cùng hàng;
- bấm nút: 2 modal cùng mở (`#modal-meeting-room` + `#modal-room-amenity-quick`, cùng z-index 1050,
  popup con đứng SAU trong DOM nên nằm trên), `elementFromPoint` giữa ô nhập tên trả về **chính ô đó**
  ⇒ bấm được, không bị backdrop cha che;
- lưu tiện nghi "ZZZ Test T86" → toast "Thêm mới thành công", popup con đóng, **popup cha còn nguyên**,
  select tiện nghi: `optCount 3 → 4` và `selectedOptions = [{v:1116, t:'ZZZ Test T86'}]` ⇒ tự tích đúng;
- bấm "Đóng" và bấm **Escape** trong popup con: chỉ popup con đóng, popup cha còn mở, chip vẫn giữ,
  còn đúng 1 backdrop, `body.modal-open` còn nguyên;
- mở popup **Xem phòng họp**: nút `data-testid="room-quick-add-amenity"` đếm **0** và popup con không
  mount (ẩn hẳn, không phải disable).
- **Dọn dữ liệu**: đã xoá `meeting_room_amenities#1116` + dòng `catalog_histories` `create` của nó.

**e2e** (`tests/meeting/meeting-room.spec.ts`, nhóm A — chưa chạy, theo quy ước chỉ chạy khi được yêu cầu):
- **A2b**: đo cùng hàng nhãn/nút · popup con chồng lên và bấm được (`elementFromPoint`) · lưu xong
  `selectedOptions` chứa tiện nghi mới (đo v-model, không chỉ nhìn chip) · popup cha còn mở;
- **A2c**: chế độ Xem — nút đếm 0, popup con không mount.

---

### Checkpoint — 20/09/2026 (KẾT THÚC ĐỢT TASK 65-86)

Vừa hoàn thành: Task 65-86 — 22 task liên tiếp theo yêu cầu user trong 1 phiên:
- **Cấu hình phân hệ** (65-68): thanh Lịch tuần 1 dòng · màn `/meeting/settings` dựng lại theo khuôn
  hub "Phê duyệt" của phân hệ Assign (rail hub + panel cấu hình inline + nút Lịch sử theo từng hub) ·
  bỏ chọn công ty · 2 mốc nhắc nhận/trả phòng + cờ "cho đặt ngoài giờ" + lệnh nền
  `meeting:send-booking-reminders` chạy mỗi phút.
- **Trình bày** (69-74, 81): màu trạng thái thẻ phòng + thanh live · `SubtextSelect` (tên phòng +
  công ty dạng dòng phụ) · dải giờ bận/rảnh có màu · chặn ngày giờ quá khứ · khối lọc phòng nhìn ra
  là bộ lọc · nhãn "Đang họp" · picker bám giờ mở cửa · nút "Lưu và gửi duyệt" / "Lưu đăng ký" theo
  cờ cần duyệt · popup duyệt có bảng thông tin (`utils/confirmInfoHtml.js`).
- **Đặt phòng từ meeting** (75-84): trực tiếp lẫn online đều chọn được phòng · API
  `GET meeting/rooms/availability` (trống / chờ duyệt / bận + gợi ý khung giờ trống gần nhất) ·
  chống tranh phòng (kiểm lại trước khi lưu + theo dõi 45s) · **quy hết về form Đặt phòng** (nút
  "Đăng ký phòng" trên form meeting + nút/cột ở màn danh sách meeting) · cờ `can_book_room`
  (chỉ người tạo hoặc chủ trì) · vá 3 lỗi ẩn nuốt 422.
- **Danh mục** (85-86): "Danh sách phòng họp" về nhóm Danh mục · **thêm nhanh tiện nghi ngay trong
  form phòng họp** (popup lồng, lưu xong tự tích).

Đang làm dở: không.

Bước tiếp theo: user review đợt này. Phase 5 (check-in QR + job nền + đặt lặp định kỳ) và Phase 6
(báo cáo) vẫn chưa mở.

Blocked: không.

Việc cần biết khi bàn giao:
- **Code ĐÃ COMMIT + PUSH** (user tự làm, 20/09/2026 tối): cả 2 repo ở `gop_db`, working tree sạch,
  ngang `origin/gop_db`.
  - `hrm-api`: `296aeab93` "Booking gd1" (20:15) + `0833f1a41` "fix" (21:18)
  - `hrm-client`: `1791c98ac` "Booking gd1" (20:15) + `bee1c02d3` ".." (21:18)
  - Toàn bộ Task 65-86 nằm trong 2 commit **20:15** (đã kiểm: `data-testid="room-quick-add-amenity"`
    và prop `modalId` của Task 86 đều có trong `HEAD`). Hai commit 21:18 gộp thêm việc của phiên khác
    (`master-data/product-*`, `CatalogHistoryService`) — không thuộc feature này.
- ⚠️ **Thư mục `e2e/` KHÔNG nằm trong repo git nào** (`HRM/e2e` không có `.git`) → spec của đợt này
  chỉ tồn tại trên máy, không đi theo commit. Cần đưa lên chung thì phải bàn chỗ chứa trước.
- **Bộ e2e của đợt này CHƯA CHẠY** (user chốt: chỉ chạy khi được yêu cầu). Đã sửa/bổ sung spec
  (nằm ngoài git, xem gạch đầu dòng trên):
  `meeting-room-booking.spec.ts`, `meeting-room-booking.api.spec.ts`, `meeting-room-sync.spec.ts`,
  `meeting-room-sync.api.spec.ts`, `meeting-room-board.spec.ts`, `meeting-room.spec.ts` (thêm A2b, A2c).
  Chạy: `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" API_BASE=http://127.0.0.1:8000 \
  BASE_URL=http://127.0.0.1:3000 npx playwright test tests/meeting --no-deps --workers=1`.
- Mọi thay đổi đều đã đo trên trình duyệt thật bằng Playwright MCP; dữ liệu test sinh ra trong lúc
  kiểm đã xoá hết (phiếu đặt, meeting, thông báo, `catalog_histories`, tiện nghi `ZZZ Test T86`).
- **2 bản ghi của USER giữ nguyên, không đụng**: meeting `TPE.MET.KH.26.0818` và giờ mở cửa công ty 1
  đang là `00:30-23:59` (do user tự đổi).
- Migration đã chạy trên DB local: `2026_09_20_000001_*`, `2026_09_20_000002_*` (2 cột mốc nhắc +
  các cột cấu hình mới trong `general_regulations`).

---

## Phase 7 — Fix lỗi 403 luồng quản lý phòng họp (21/09/2026)

Báo lỗi từ VPS: (1) vào màn "Tình trạng phòng họp" hiện toast 403 "Bạn không có quyền thực hiện
chức năng này"; (2) menu Danh mục không có "Danh sách phòng họp".

**Nguyên nhân gốc (đã tái hiện bằng Playwright MCP, không đoán):**

- Cả 2 triệu chứng cùng quy về quyền `Khai báo phòng họp` — tài khoản trên VPS KHÔNG có quyền này.
- (1) là lỗi CODE: `pages/meeting/room-board/index.vue::loadAmenityOptions()` gọi
  `meeting/rooms/form-options` — route gate `checkPermission:Khai báo phòng họp`
  (`Modules/Meeting/Routes/api.php:77`) — trong khi màn cố ý mở cho MỌI nhân viên
  (`isShow: true`, `/board` + `/status-board` không gate). Page có `try/catch` im lặng nhưng
  interceptor chung `plugins/axios.js:32` đã bắn toast TRƯỚC khi page bắt được.
  Lỗi y hệt ở `pages/meeting/bookings/components/BookingFormModal.vue::loadFormOptions()`.
- (2) là lỗi DỮ LIỆU/DEPLOY, không phải code: registry gate `isShow: ['Khai báo phòng họp']`
  (`components/subsystem-menu/meeting.js:43`) chạy đúng thiết kế. Quyền chỉ nằm trong
  `PermissionsTableSeeder` (seeder `delete()` toàn bộ permissions guard `api`) và id vừa bị đánh
  số lại **1574 → 1586** ngày 19/09; id 1574 nay là "Xem danh mục tính chất hàng hóa".

**Quyết định đã chốt (user, 21/09/2026):**

- (1) MỞ endpoint tiện nghi thay vì tắt toast — đúng tiền lệ `rooms/bookable`,
  `rooms/availability`, `room-purposes/options` của chính module (comment ở các route đó đã ghi:
  gate danh mục cho màn dùng chung là "select trống trơn, không lỗi, không giải thích — hỏng im lặng").
- (2) Gate menu GIỮ NGUYÊN (khai báo phòng là việc của người quản trị) → cấp quyền trên VPS, không sửa code.

### Task

- [x] T87 — BE: thêm `GET meeting/room-amenities/options` KHÔNG gắn `checkPermission`, trả tiện nghi
      đang hoạt động (route TĨNH đặt TRƯỚC wildcard `/{meetingRoomAmenity}`)
- [x] T88 — FE: `room-board/index.vue::loadAmenityOptions()` đổi sang endpoint mới
- [x] T89 — FE: `BookingFormModal.vue::loadFormOptions()` đổi sang endpoint mới
- [x] T90 — Kiểm bằng Playwright MCP: nhân viên KHÔNG có quyền `Khai báo phòng họp` → 0 toast 403,
      ô lọc Tiện nghi CÓ option (đo bằng số lấy từ DOM, cả 2 màn)
- [x] T91 — Cập nhật ca e2e `meeting-room-board.spec.ts` cho hành vi mới
- [x] T92 — Soạn SQL kiểm tra + cấp quyền `Khai báo phòng họp` cho VPS (user tự chạy)

### Checkpoint — 21/09/2026

Vừa hoàn thành: T87-T92 — fix 403 luồng quản lý phòng họp.

**Code đã sửa (CHƯA commit, theo quy tắc project):**
- `hrm-api/Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php` — thêm `options()`
- `hrm-api/Modules/Meeting/Routes/api.php` — `GET meeting/room-amenities/options`, KHÔNG gắn checkPermission
- `hrm-client/pages/meeting/room-board/index.vue` — `loadAmenityOptions()` đổi endpoint
- `hrm-client/pages/meeting/bookings/components/BookingFormModal.vue` — `loadFormOptions()` đổi endpoint
- `e2e/tests/meeting/meeting-room-board.api.spec.ts` — thêm ca A4 (khoá cả 2 chiều gate)

**Số đo thật (Playwright MCP, trình duyệt thật) — mô phỏng tài khoản không có quyền:**

| Phép đo | Trước fix | Sau fix |
|---|---|---|
| Toast trên `/meeting/room-board` | 1 — "Bạn không có quyền thực hiện chức năng này" | 0 |
| Request 403 khi mở màn | 1 (`meeting/rooms/form-options`) | 0 |
| Option ô lọc "Tiện nghi" (room-board) | 0 | 3 |
| Option ô lọc "Tiện nghi" (modal Đăng ký) | 0 | 3 (+ 6 mục đích, 2 phòng) |

**Đo bằng curl với token nhân viên KHÔNG có quyền (employee 1184):**
- `meeting/room-amenities/options` -> 200 (mới, cố ý mở)
- `meeting/rooms/form-options` -> 403 (gate GIỮ NGUYÊN)
- `meeting/room-amenities` (danh mục) -> 403 (gate GIỮ NGUYÊN — chỉ mở đúng `/options`)
- `meeting/rooms/board` -> 200

Luồng bình thường (super admin) đo lại sau fix: 3 tiện nghi, 2 phòng, 0 toast.

Đang làm dở: không.

Bước tiếp theo: user chạy `vps-cap-quyen-phong-hop.sql` trên VPS để xử lý phần menu
(thiếu quyền `Khai báo phòng họp` — không sửa được bằng code).

Blocked: không.

⚠️ Bộ e2e CHƯA CHẠY (chỉ chạy khi user yêu cầu). Ca A4 mới đã kiểm parse bằng
`npx playwright test --list` (17 ca trong file, A4 đăng ký đúng).

---

## Phase 7b — Thêm nhanh tiện nghi lưu chậm (21/09/2026)

**Đo thật (Playwright MCP, từ lúc bấm Lưu tới lúc chip tiện nghi hiện ra):**

| Mốc | Thời gian |
|---|---|
| `POST meeting/room-amenities` | 716 ms |
| `GET meeting/rooms/form-options` (nạp lại sau lưu) | 1122 ms |
| Popup con đóng | 794 ms |
| **Chip tiện nghi hiện ra** | **2014 ms** |

**Nguyên nhân:** `onQuickAmenitySaved()` gọi `await loadFormOptions()` — nạp LẠI toàn bộ
`form-options` chỉ để biết 1 tiện nghi vừa tạo, trong khi response của chính lệnh POST đã trả
đủ bản ghi (`id`/`name`/`status`). 2 request chạy NỐI TIẾP nên user chờ cộng dồn.

**Đo trong PHP để chắc chắn không phải BE chậm:**
- `MeetingRoomAmenityService::updateOrCreate()` = 16-47 ms, 10 query (chỉ 2 query THẬT:
  insert tiện nghi + insert `catalog_histories`; 8 query còn lại là `information_schema.columns`
  do `BaseModel` gọi `Schema::hasColumn()` ở hook creating/saving)
- `MeetingRoomService::formOptions()` = 1.4-27 ms, 3 query, payload bé (13 tiện nghi, 5 công ty)
- Middleware `CheckPermission` = ~135 ms/request (`Employee::find` 45ms + `getAllPermissions()`
  90ms, 618 quyền, 4 query) — KHÔNG rẻ đi ở lần gọi sau

=> Việc thật chỉ vài chục ms; phần lớn thời gian là CHI PHÍ DỰNG REQUEST. Bỏ được 1 request là
bỏ được ~1.1s.

### Task

- [x] T93 — FE: `onQuickAmenitySaved()` gộp thẳng bản ghi POST trả về vào `amenityOptions`,
      KHÔNG gọi lại `loadFormOptions()`; giữ nạp lại làm đường lui khi payload thiếu id/name
- [x] T94 — Đo lại bằng Playwright MCP, so trước/sau trên cùng phép đo
- [x] T95 — Dọn dữ liệu test sinh ra trong lúc đo

### Ghi nhận để user quyết (CHƯA làm — đụng hàm dùng chung, theo CLAUDE.md phải hỏi trước)

- `app/Models/BaseModel.php` gọi `Schema::hasColumn()` **8 lần mỗi lần lưu** (hook creating +
  saving), mỗi lần là 1 query `information_schema.columns`. Local: 1.861 bảng / 29.497 cột,
  ~3.4ms/lượt => ~27ms. Trên DB production lớn hơn, `information_schema` thường đắt hơn nhiều.
  Ảnh hưởng MỌI model `extends BaseModel`, không riêng phòng họp.
- Middleware `CheckPermission` nạp lại toàn bộ 618 quyền mỗi request, không cache theo request.

### Checkpoint — 21/09/2026 (Phase 7b)

Vừa hoàn thành: T93-T95.

**Code đã sửa (CHƯA commit):**
- `hrm-client/pages/meeting/rooms/components/MeetingRoomModal.vue`
  - `onQuickAmenitySaved()` gộp thẳng bản ghi POST trả về vào `amenityOptions` (chèn đúng thứ tự
    `sort_order` -> `id`), KHÔNG gọi lại `loadFormOptions()`; thiếu `id`/`name` mới nạp lại
  - `loadFormOptions()` map thêm `sort_order` để có mốc chèn
- `e2e/tests/meeting/meeting-room.spec.ts` — ca A2b assert thêm: sau khi bấm Lưu chỉ ĐÚNG 1 request,
  0 request `form-options`

**Số đo trước/sau (Playwright MCP, cùng phép đo: từ lúc bấm Lưu tới lúc chip tiện nghi hiện ra):**

| | Trước | Sau |
|---|---|---|
| Số request sau khi bấm Lưu | 2 (POST + form-options) | **1** (chỉ POST) |
| Thời gian tới lúc chip hiện | 2014 ms | **928 / 1368 ms** (2 lượt đo) |

Luồng Sửa đo lại sau fix: modal mở đúng, `form-options?room_id=2810`, 15 option đủ
`is_locked` + `sort_order`, 2 tiện nghi tích sẵn — không hồi quy.

Dữ liệu test đã dọn: 10 tiện nghi `ZZZ Perf%` (id 1119-1128) + dòng `catalog_histories` tương ứng;
pivot `meeting_room_room_amenity` = 0 nên không đụng phòng nào. Còn lại 5 tiện nghi, trong đó
1117/1118 KHÔNG phải của tôi (có sẵn từ trước) nên giữ nguyên.

Đang làm dở: không.

Bước tiếp theo: user quyết 2 việc ở mục "Ghi nhận để user quyết" (BaseModel `Schema::hasColumn`,
cache quyền trong `CheckPermission`) — cả hai đều là HÀM DÙNG CHUNG, chưa đụng.

Blocked: không.

---

## Phase 7c — Chuyển quyền Meeting về đúng phân hệ (21/09/2026)

Cột `permissions.type` = PHÂN HỆ ở màn Phân quyền. Phân hệ Meeting đã khai `permissionType: 26`
trong `components/subsystems.js` nhưng DB chưa có quyền nào type=26 → khối "Phân hệ meeting"
rỗng, còn 20 quyền meeting nằm nhờ ở type 4 (Phân hệ giao việc).

**Đã rà: `type` CHỈ để gom nhóm hiển thị** — không có `where('type')` nào trên `permissions` ở BE
(`AuthNewController` chỉ `select('permissions.*')`), `role_has_permissions` khoá theo
`permission_id`. Nên đổi type KHÔNG làm ai mất quyền.

**User chốt 21/09/2026:** 12 quyền -> type 26 (Meeting); 8 quyền báo cáo meeting -> type 29
(CSKH trước bán, theo đúng nơi menu đã dời 3 báo cáo này từ 16/09).

| Đích | Id |
|---|---|
| 26 — Meeting | 989, 1004, 1184, 1185, 1586 (Danh mục) · 1095-1098 (Quản lý meeting) · 1588, 1589 (Quản lý phòng họp) · 1587 (Báo cáo phòng họp) |
| 29 — CSKH trước bán | 1057-1061 (meeting theo nhân viên/dự án) · 1174-1176 (kết quả theo thị trường) |

### Task

- [x] T96 — Chụp mốc đối chứng: số dòng `role_has_permissions` + permission_ids của vài role
- [x] T97 — Seeder `PermissionsTableSeeder.php`: đổi `type` 4 -> 26/29 cho 20 quyền
- [x] T98 — Migration cộng dồn `UPDATE ... WHERE id IN (...)`, có `down()` trả về 4
- [x] T99 — Chạy migration + kiểm DB (12 type=26, 8 type=29, 0 quyền meeting còn ở type 4)
- [x] T100 — Kiểm KHÔNG ai mất quyền: `role_has_permissions` trước/sau phải bằng nhau tuyệt đối
- [x] T101 — Kiểm màn Phân quyền bằng Playwright MCP, đo số quyền từng khối trên DOM

- [x] T102 — Sửa lỗi gom nhóm ở `components/setting/Permission.vue` (phát sinh trong lúc kiểm)

### Checkpoint — 21/09/2026 (Phase 7c)

Vừa hoàn thành: T96-T102.

**Code đã sửa (CHƯA commit):**
- `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — 20 dòng đổi `type`
  (diff đúng 20 thêm / 20 xoá, không nhiễu EOL)
- `hrm-api/database/migrations/2026_09_21_000001_move_meeting_permissions_to_meeting_subsystem.php` — MỚI
- `hrm-client/components/setting/Permission.vue` — gom nhóm theo CẶP (`type`, `group`)

**⚠️ Lỗi phát sinh khi kiểm — đáng nhớ:** `Permission.vue::initListPermissions()` gom nhóm CHỈ theo
tên `group`, bỏ qua `type`. Lỗi nằm im nhiều tháng vì trước đây không tên nhóm nào dùng ở 2 phân hệ.
Vừa chuyển quyền Meeting sang type 26 mà giữ tên nhóm "Danh mục" (type 4 cũng có nhóm này) là 5 quyền
danh mục meeting hiện nhầm trong khối "Phân hệ giao việc" — KHÔNG lỗi, KHÔNG báo gì. User chốt sửa
tận gốc (21/09/2026) sau khi đo phạm vi ảnh hưởng.

**Số đo (Playwright MCP, đo từ DOM + state component):**

| Khối | Trước đợt | Sau BE (FE chưa sửa) | Sau cả 2 |
|---|---|---|---|
| Phân hệ meeting | không có khối | 7 | **12** |
| Phân hệ giao việc | 192 | 177 | **172** |
| Phân hệ CSKH trước bán | 0 | 8 | **8** |

- Khối Meeting gồm 4 nhóm: Danh mục 5 · Quản lý meeting 4 · Quản lý phòng họp 2 · Báo cáo phòng họp 1;
  12 id đúng danh sách đã chốt.
- 25 khối phân hệ còn lại giữ nguyên số tuyệt đối (đã liệt kê so từng dòng).
- Tổng nhóm 159 -> 160, sinh ĐÚNG 1 nhóm mới `{Danh mục, type 26, 5 quyền}` — khớp con số mô phỏng
  trước khi sửa.
- `group_id_` (id DOM accordion) không trùng sau khi tách nhóm; tích/bỏ tích quyền vẫn chạy.

**KHÔNG AI MẤT QUYỀN** (chốt chặn quan trọng nhất):
- `role_has_permissions`: 16.691 dòng trước -> 16.691 dòng sau
- Số quyền của từng role trong 20 quyền đổi đợt này khớp TỪNG DÒNG với mốc trước migration
  (27 role, so khớp chuỗi nguyên văn)
- Seeder vs DB: 762 quyền khai trong seeder, 0 id trùng thật, 0 dòng lệch `type`

Đang làm dở: không.

Bước tiếp theo: user review. Trên VPS cần chạy migration này cùng đợt deploy.

Blocked: không.

**Ghi chú e2e:** nhánh `gop_db` KHÔNG có màn ma trận phân quyền (`pages/admin/roles/` không tồn tại,
không có markup `pm-srow`) — spec `e2e/tests/admin/permission-matrix-screens.spec.ts` là của nhánh
khác, sẽ đỏ trên nhánh này dù có hay không thay đổi của đợt này. Màn phân quyền duy nhất trên `gop_db`
là `/human/roles/add/_id`, hiện CHƯA có spec nào; chưa tạo spec mới cho nó (chờ user quyết).

---

## Phase 7d — Tên phòng bị cắt hụt ở cột nhãn lưới (22/09/2026)

Báo lỗi: "/meeting/room-board — khi có nhiều phòng, tên phòng bị ẩn 1 phần phía trên".

**Đo thật (Playwright MCP, chặn API trả 15 phòng tên dài/ngắn khác nhau — KHÔNG đụng dữ liệu):**

| Ô | Số dòng tên | Cao nội dung | Cao ô | Tràn lên trên |
|---|---|---|---|---|
| "Phòng họp Hội đồng quản trị tầng 12 toà nhà Tân Phát" | 3 | 83px | 64px | **10px** |
| "Phòng đào tạo nội bộ khu vực miền Bắc" | 2 | 65px | 64px | 1px |
| "Phòng hội thảo lớn tầng trệt" | 2 | 65px | 64px | 1px |
| "Phòng tiếp khách VIP tầng 5" | 2 | 65px | 64px | 1px |
| "Phòng A" (và 10 ô tên ngắn) | 1 | 47px | 64px | 0 (dư 8px) |

4/15 ô lỗi, và cả 4 đều là tên phải xuống dòng.

**Nguyên nhân:** hàng lưới cao CỐ ĐỊNH 64px (`gridTemplateRows: 36px repeat(n, 64px)`), ô nhãn
`padding: 8px 12px` nên vùng chứa chỉ còn **48px** — trong khi nội dung 1 dòng tên đã chiếm 47px
(tiêu đề line-height 18.2px + dòng phụ 14.3px + khoảng cách). Tên xuống 2 dòng là 65px, 3 dòng 83px.
`.rtg-room-label` có `align-items: center` + `.rtg-cell { overflow: hidden }` nên phần thừa bị cắt
ĐỀU cả trên lẫn dưới — mắt bắt rõ nhất là chữ hụt phía trên.

⚠️ **SỐ LƯỢNG PHÒNG KHÔNG PHẢI NGUYÊN NHÂN** — thủ phạm là tên dài trên cột nhãn rộng 180px.
Nhiều phòng chỉ làm dễ gặp tên dài hơn.

**User chốt 22/09/2026:** tên kẹp 1 dòng + đuôi `…`, hover xem đủ; GIỮ cột nhãn 180px và hàng 64px
(lưới đều, không dài thêm, không đụng vị trí khối phiếu).

### Task

- [x] T103 — `.rtg-room-label`: ép tên 1 dòng + ellipsis; `title` trên ô để hover xem tên đủ
- [x] T104 — Đo lại bằng Playwright MCP với đúng 15 phòng đó: 0 ô tràn
- [x] T105 — Bổ sung ca e2e cho khuôn mới

### Checkpoint — 22/09/2026 (Phase 7d)

Vừa hoàn thành: T103-T105.

**Code đã sửa (CHƯA commit):**
- `hrm-client/components/meeting-room/RoomTimelineGrid.vue`
  - template: thêm `:title="room.name"` trên ô nhãn (hover đọc trọn tên)
  - SCSS: `.rtg-room-label > * { min-width: 0; width: 100% }` +
    `.field-line`/`.project-sub` kẹp 1 dòng `white-space: nowrap !important` + ellipsis
  - ⚠️ `!important` BẮT BUỘC: `V2BaseTitleSubInfo` đặt `white-space: normal` bằng INLINE style.
    `min-width: 0` cũng bắt buộc, thiếu nó con của flex không co lại nên ellipsis không bao giờ hiện.
- `e2e/tests/meeting/meeting-room-board.spec.ts` — thêm ca A5 (chặn API bơm tên dài, đo 4 điều:
  hàng vẫn 64px · 0 tràn trên/dưới · tên đúng 1 dòng · có `…` + `title` đầy đủ)

**Số đo trước/sau (15 phòng dựng bằng chặn API, KHÔNG đụng dữ liệu):**

| | Trước | Sau |
|---|---|---|
| Ô nhãn bị tràn/cắt chữ | **4/15** (tệ nhất tràn 10px) | **0/15** |
| Số dòng tên tối đa | 3 | 1 |
| Chiều cao hàng | 64px | 64px (không đổi) |
| Tên dài có `…` + title đầy đủ | không | 4/4 ô |

**Hồi quy đã kiểm với dữ liệu thật (2 phòng, ngày 20/09 có 2 phiếu):**
- Nhãn: 0 ô tràn, `title` đúng tên
- Khối phiếu: mỗi khối nằm GỌN trong đúng 1 hàng phòng, lề trên/dưới đều 6px, cao 52px trong hàng 64px
- 94 ô trống render bình thường

Đang làm dở: không.

Bước tiếp theo: user review.

Blocked: không.

---

## Phase 7e — Nút ở thẻ trạng thái phòng bị vỡ chữ 2 dòng (22/09/2026)

Ảnh user chụp production (`hrm-crm.eteksofts.com/meeting/room-board`, tab "Thẻ phòng"): nhãn 2 nút
"Xem lịch phòng" / "Đặt phòng" xuống 2 dòng ("Xem lịch / phòng"). Không riêng thẻ user khoanh —
TẤT CẢ thẻ đều bị.

**Đo thật (chặn `status-board` bơm 5 phòng như ảnh, viewport 1900px):** 10/10 nút `soDong = 2`,
`white-space: normal`.

| Số đo | Giá trị |
|---|---|
| Thẻ rộng | 261px (padding 28) -> vùng chứa **233px** |
| 2 nút cần khi không xuống dòng | 127 + 99 + gap 8 = **234px** |
| **Thiếu** | **1px** |

**Nguyên nhân:** `.rb-status-card__foot .v2-btn { flex: 1 1 auto }` cho nút CO nhỏ hơn bề rộng chữ,
mà `V2BaseButton` không khoá `white-space` -> chữ tự xuống dòng. Lưới thẻ
`minmax(260px, 1fr)` cấp vùng chứa 233px, thiếu đúng 1px so với nhu cầu 234px.

**Không đổi chữ nút:** `button-convention` không có chữ chuẩn cho hành động này; "Xem lịch phòng"
đúng công thức `<động từ> + <đối tượng>` nên giữ nguyên, chỉ nới chỗ.

### Task

- [x] T106 — `.rb-status-card__foot .v2-btn`: `white-space: nowrap`; foot thêm `flex-wrap: wrap`
      (lưới an toàn cho màn rất hẹp). **User chốt giữa chừng: bỏ chữ "phòng" khỏi nhãn nút**
      -> "Xem lịch" / "Đặt"; nhờ vậy `minmax` GIỮ NGUYÊN 260px (không phải nới 280px)
- [x] T107 — Đo lại: 0/10 nút xuống dòng, thẻ vẫn đủ rộng, số cột hợp lý
- [x] T108 — Bổ sung ca e2e

### Checkpoint — 22/09/2026 (Phase 7e)

Vừa hoàn thành: T106-T108.

**Code đã sửa (CHƯA commit):** `hrm-client/pages/meeting/room-board/index.vue`
- Nhãn 2 nút trên thẻ: "Xem lịch phòng" -> **"Xem lịch"**, "Đặt phòng" -> **"Đặt"** (user chốt)
- `.rb-status-card__foot .v2-btn { white-space: nowrap }` + foot `flex-wrap: wrap` (lưới an toàn)
- `.rb-status-grid` GIỮ `minmax(260px, 1fr)` — nhãn ngắn rồi nên không cần nới

`e2e/tests/meeting/meeting-room-board.spec.ts` — thêm ca F3 (đo 4 bề rộng màn).

**Số đo trước/sau (chặn `status-board` bơm 5 phòng như ảnh production):**

| | Trước | Sau |
|---|---|---|
| Nút vỡ chữ 2 dòng | **10/10** | **0/10** |
| Nút tràn khỏi thẻ | 0 | 0 |
| 2 nút cần / vùng chứa có | 234px / 233px (thiếu 1px) | 161px / 233px |
| Số cột ở màn 1900px | 6 | 6 (không đổi) |

Kiểm ở 4 bề rộng 1900 / 1440 / 1280 / 1024 — đều 0 nút vỡ chữ, 0 nút tràn.

⚠️ **Bẫy phép đo (đã dính rồi sửa):** đếm số dòng chữ trong nút bằng `chiều cao nút / line-height`
là SAI — nút cao 32px, line-height 14px nên nút 1 dòng cũng ra "2 dòng". Phải đếm bằng
`Range.getClientRects().length` trên chính text node. Ca e2e F3 ghi rõ bẫy này.

**Chưa đụng (chờ user quyết):** vẫn còn một nút "Xem lịch phòng" khác ở cột Hành động màn
`/meeting/rooms` (`pages/meeting/rooms/index.vue:683`). Ở đó chữ "phòng" KHÔNG thừa (đang trong
danh sách phòng, không phải thẻ mang tên phòng), và ca e2e J1 + meeting-room.spec bám đúng chữ đó
-> để nguyên.

Đang làm dở: không.

Bước tiếp theo: user review.

Blocked: không.

---

## Phase 8 — Yêu cầu dịch vụ trên phiếu đặt phòng (23/09/2026)

**Mục tiêu.** Người đặt phòng nhờ người phụ trách chuẩn bị trà / nước / hoa quả… ngay trên phiếu DPH;
người phụ trách nhận thông báo, chuẩn bị xong thì xác nhận lại cho người đặt biết.

**Spec:** `docs/superpowers/specs/gop-db/2026-09-23-yeu-cau-dich-vu-phong-hop-design.md`
(11 quyết định user chốt 23/09/2026 — đọc mục 3 trước khi code).

**Ràng buộc chung (áp cho MỌI task dưới đây):**

- Nhánh `gop_db` ở cả 2 repo. Không `git stash` (nhiều session chạy song song).
- **Không thêm quyền mới** — danh mục dùng `checkPermission:Khai báo phòng họp`.
- Model mới `extends BaseModel`; `created_by`/`updated_by` phải có trong `$fillable`.
- FE: mọi element form là `V2Base*`, select trong modal là `V2BaseSelectInModal`; nút trong cụm
  `class="mr-2 mb-2"`, nút cuối `mb-2`; badge dùng `V2BaseBadge` với **màu do BE trả**.
- Số: `1,234.5` (chuẩn quốc tế) — FE `toLocaleString('en-US')`, BE `number_format()` mặc định.
- Cờ quyền FE khởi tạo `false` (fail-closed), không bao giờ gán literal `true`.
- Nút không dùng được thì **ẩn hẳn**, không disable; ẩn/hiện phải **khớp giữa danh sách và chi tiết**.
- Mỗi task đụng UI: **đo bằng số lấy từ DOM qua Playwright MCP** (`http://127.0.0.1:3000`), không
  nhìn ảnh rồi kết luận. E2E **chỉ chạy khi user yêu cầu**, nhưng spec vẫn phải viết/cập nhật.

### A. Nhiều người phụ trách phòng (nền tảng — làm TRƯỚC)

> Yêu cầu dịch vụ bắn cho "nhóm phụ trách", nên phải có nhóm trước. Đây là phần rủi ro nhất của
> Phase 8 vì đụng luồng duyệt phiếu đang chạy.

- [x] T109 — Migration `2026_09_23_000001_create_meeting_room_managers_table.php`: bảng nối
      (`meeting_room_id` FK cascade, `employee_id` index, unique cặp) + **backfill** từ
      `meeting_rooms.manager_employee_id` + **drop cột cũ**. `down()` dựng lại cột và đổ ngược
      người đầu tiên của mỗi phòng. Chạy `migrate` rồi đếm: số dòng bảng nối = số phòng có
      `manager_employee_id` khác NULL trước khi chạy (chụp số trước — local hiện 2 phòng, đều có PT).
- [x] T110 — `Entities/MeetingRoom.php`: bỏ `manager()` + `manager_employee_id` khỏi `$fillable`;
      thêm `managers()` (`belongsToMany` Employee qua `meeting_room_managers`) và
      `managerIds(): array` (cache trong thuộc tính để không query lại nhiều lần trong 1 request).
- [x] T111 — `Services/MeetingRoomService.php`: lưu nhóm phụ trách bằng `sync()` trong transaction
      (store + update); sort cột "Người quản lý" đổi sang sub-query theo tên người ĐẦU TIÊN, giữ
      whitelist cột sort; eager load `managers` ở mọi chỗ trả danh sách (**cấm N+1**).
- [x] T112 — `Http/Requests/MeetingRoom/MeetingRoomRequest.php`: `manager_employee_ids` =
      `required|array|min:1`, từng phần tử `integer|exists`. **Chỉ khai `rules()`, KHÔNG khai
      `messages()`** (câu chuẩn đã có ở lang file).
- [x] T113 — 2 Resource phòng (`MeetingRoomResource`, `DetailMeetingRoomResource`): trả
      `manager_employee_ids[]`, `manager_names[]`, `manager_name_text` (ghép `", "`).
      `BookableMeetingRoomResource` **vẫn không trả id thô** (giữ nguyên chủ ý cũ).
- [x] T114 — `Services/MeetingRoomBookingService.php` — sửa 4 chỗ so 1 id thành so theo nhóm:
      `applyVisibilityScope()` (≈dòng 179) dùng `whereHas('managers')`; gate duyệt (≈200, ≈777);
      danh sách người nhận thông báo (≈1193-1198) bắn **toàn bộ** `managerIds()`, rỗng thì không gửi.
- [x] T115 — 2 Resource phiếu (`MeetingRoomBookingResource`, `DetailMeetingRoomBookingResource`):
      `$isRoomManager` tính theo `managerIds()`.
- [x] T116 — Import/Export phòng họp (`MeetingRoomService` ≈1054 + `BuildsImportTemplate`): cột
      `ManagerName` nhận **nhiều tên ngăn bằng `;`**; tên không khớp nhân viên nào → báo lỗi ĐÚNG
      DÒNG (không bỏ qua im lặng). Export ghép ngược lại bằng `"; "`.
- [x] T117 — `app/Services/CatalogHistoryService.php` (≈441-450): ghi lịch sử theo danh sách tên,
      nhãn giữ "Người quản lý phòng"; kiểm 1 lần sửa thật để chắc lịch sử không in ra id trần.
- [x] T118 — FE `pages/meeting/rooms/components/MeetingRoomModal.vue`: select **nhiều người**,
      `required`; giữ nguyên cách vá option cho người đã nghỉ việc (nay là vá theo mảng
      `manager_names` API trả về, thiếu thì lưu lại là **mất người** — bẫy cũ đã dính 1 lần).
- [x] T119 — FE `pages/meeting/rooms/index.vue`: cột "Người quản lý" hiện **2 tên đầu + "+N"**,
      `title` đủ danh sách; cập nhật map import (`row.ManagerName`).
- [x] T120 — FE `pages/meeting/bookings/components/BookingFormModal.vue` panel phải: dòng
      "Người phụ trách" ghép nhiều tên (≈dòng 464) và câu gợi ý gửi duyệt (≈1925) đổi theo.
- [x] T121 — PHPUnit `MeetingRoomManagersTest`: backfill giữ đúng số lượng · phòng 2 phụ trách thì
      **cả 2** duyệt được phiếu · người ngoài nhóm gọi `approve` → 403 · `applyVisibilityScope`
      trả phiếu của phòng mình phụ trách.
- [x] T122 — Đo bằng Playwright MCP: form phòng lưu 2 phụ trách → danh sách hiện "A, B" (đọc
      `textContent` thật, không chỉ nhìn ảnh); bỏ trống ô phụ trách → chặn, hiện lỗi dưới ô.

### B. Danh mục Dịch vụ phòng họp

- [x] T123 — Migration `..._000002_create_meeting_room_services_table.php` (name unique · unit ·
      icon · sort_order · note · status · created_by/updated_by · timestamps) + Seeder
      `MeetingRoomServicesTableSeeder` 5 món mẫu (Trà · Nước suối · Hoa quả · Khăn lạnh · Bánh ngọt),
      idempotent theo `name` (`firstOrCreate`).
- [x] T124 — BE: `Entities/MeetingRoomService.php` (extends BaseModel) ·
      **`Services/MeetingRoomServiceCatalogService.php`** (KHÔNG đặt `MeetingRoomServiceService` —
      vừa khó đọc vừa dễ nhầm với `Services/MeetingRoomBookingService.php` đang có) ·
      `MeetingRoomServiceController` · `MeetingRoomServiceRequest` · 2 Resource — copy nguyên khuôn
      `MeetingRoomPurpose*`, đổi tên đầy đủ (kể cả **entity-type của `catalog_histories`** và bảng
      trong rule `unique` — 2 chỗ hay sót khi copy màn danh mục).
- [x] T125 — Routes `meeting/room-services` đủ 10 route theo đúng thứ tự route TĨNH trước wildcard;
      tất cả gắn `checkPermission:Khai báo phòng họp`, **trừ `/options`**.
- [x] T126 — `/options` nhận `include_ids` → `where('status',1)->orWhereIn('id',$includeIds)`, trả kèm
      `is_locked` để `V2BaseSelect` tự gắn 🔒 (KHÔNG nối chữ vào `name`).
- [x] T127 — Chặn xoá món đang có phiếu dùng: `destroy()` đếm `meeting_room_booking_services` trước,
      >0 thì trả lỗi nêu số phiếu + gợi ý dùng Khoá.
- [ ] T128 — FE màn `pages/meeting/room-services/index.vue` + `components/RoomServiceModal.vue` —
      copy `room-purposes`, soát đủ **4 chỗ sót im lặng**: entity-type lịch sử · thẻ kebab component ·
      rule unique · key lưu cấu hình cột.
- [ ] T129 — Đăng ký menu `components/subsystem-menu/meeting.js` nhóm **Danh mục**, nhãn "Dịch vụ
      phòng họp"; **đếm số link trên hub bằng DOM** sau khi thêm (khai sai key là cả nhóm biến mất
      im lặng).
- [ ] T130 — Đo bằng Playwright MCP: thêm/sửa/khoá/mở khoá 1 món, cột Người cập nhật **ra tên**
      (cách duy nhất phát hiện thiếu audit), mục Lịch sử ghi đúng.

### C. Yêu cầu dịch vụ trên phiếu

- [x] T131 — Migration `..._000003_create_meeting_room_booking_services_table.php` (booking_id FK
      cascade · service_id · service_name/unit snapshot · quantity decimal(12,2) · note · sort_order ·
      unique `(booking_id, service_id)`) + `..._000004_add_service_columns_to_meeting_room_bookings`
      (4 cột `service_*`, `service_status` **nullable**). Entity **`MeetingRoomBookingServiceItem`**
      (tên tránh đụng `Services/MeetingRoomBookingService.php`) + quan hệ
      `MeetingRoomBooking::serviceItems()` (`hasMany`, order theo `sort_order`).
- [x] T132 — `MeetingRoomBookingRequest`: `services` `nullable|array|max:20`; `services.*.service_id`
      bắt buộc + `exists` + đang Hoạt động; `services.*.quantity` `numeric|gt:0|max:999999`;
      `services.*.note` `nullable|max:255`; **chặn trùng `service_id`** trong mảng. Không khai
      `messages()` cho rule phổ biến.
- [x] T133 — `MeetingRoomBookingService::store()`: trong transaction ghi các dòng (snapshot
      `service_name`/`unit` lấy từ danh mục tại thời điểm tạo), set `service_status = 1` khi có dòng,
      **NULL** khi không. Phòng không có người phụ trách mà gửi `services[]` → **422**.
- [x] T134 — `update()`: **bỏ hoàn toàn** khoá `services` khỏi payload đọc vào (chặn ở BE). Đổi phòng
      thì giữ nguyên dòng dịch vụ và bắn thông báo cho nhóm phụ trách phòng MỚI.
- [x] T135 — 2 endpoint `PUT meeting/room-bookings/{id}/service-prepared` · `/service-rejected`
      (+ `MeetingRoomBookingServiceRejectRequest`: `reason` bắt buộc ≤ 500). Guard: chỉ người trong
      `managerIds()`, chỉ khi `service_status = 1`, phiếu không Hủy/Từ chối → ngược lại **409** kèm
      câu nêu ai đã xử lý lúc nào. Ghi `service_handled_by/at`.
- [x] T136 — Resource phiếu trả thêm: `has_service_request` · `service_status` · `service_status_text`
      · `service_status_color` (`#D97706`/`#16A34A`/`#DC2626`) · `service_handled_by_name` ·
      `service_handled_at` · `service_reject_reason` · `services[]` (detail, từ `serviceItems`) ·
      **`is_can_handle_service` fail-closed**. Eager load `serviceItems` + `room.managers` ở cả
      `index()` lẫn `show()` (cấm N+1).
- [x] T137 — Thông báo `[DPH]` 5 mốc qua `sendBookingNotification()` — nhóm hành động:
      `Yêu cầu dịch vụ` (tạo mới + đổi phòng) · `Hủy yêu cầu dịch vụ` (phiếu Hủy/Từ chối khi đang
      Chờ chuẩn bị) · `Đã chuẩn bị dịch vụ` · `Từ chối dịch vụ`. Tên phiếu ≤ 50 ký tự, tổng ≤ 120,
      deep-link kèm ID.
- [x] T138 — FE khối "Yêu cầu dịch vụ" trong `BookingFormModal.vue`: **tiêu đề nhóm phẳng** (KHÔNG
      card), chỉ hiện khi đã chọn phòng **và** phòng có ≥ 1 phụ trách (không thì hiện dòng xám
      `#6b7280` giải thích — **không dùng `.text-muted`**, class đó bị ép đỏ). Mỗi dòng:
      `V2BaseSelectInModal` (món đã chọn biến khỏi dropdown dòng khác) + số lượng + ghi chú + nút xoá;
      dưới cùng nút "Thêm dòng". Lỗi validate hiện **đồng thời mọi dòng**, không tự sửa số user gõ.
- [x] T139 — FE chế độ **chỉ đọc**: màn Sửa phiếu và popup Xem render khối dạng đọc + `V2BaseBadge`
      trạng thái (màu BE trả).
- [x] T140 — FE 2 nút ở footer popup Xem: "Đã chuẩn bị" (primary) · "Từ chối" (nhóm nguy hiểm →
      `base-confirm-modal` nhập lý do), **`v-if="item.is_can_handle_service"`**, không disable.
- [x] T141 — FE `pages/meeting/bookings/index.vue`: cột "Dịch vụ" (badge) trong bộ cột cấu hình được +
      ô lọc "Trạng thái dịch vụ" (Chờ chuẩn bị / Đã chuẩn bị / Từ chối / Không có yêu cầu); BE lọc
      tương ứng (`whereNull` cho "Không có yêu cầu").

### D. Kiểm chứng & tài liệu

- [x] T142 — PHPUnit `MeetingRoomBookingServiceRequestTest`: `update()` gửi kèm `services[]` →
      dữ liệu **không đổi** · người thứ hai bấm → 409 · phiếu Hủy → không xác nhận được ·
      phòng không có phụ trách → 422 · người ngoài nhóm → 403.
- [ ] T143 — E2E `e2e/tests/meeting/meeting-room-service.api.spec.ts` + `.spec.ts` — 8 ca ở mục 10
      của spec, **có ca không quyền cả 2 chiều**. Nhớ `--workers=1`, `--no-deps`,
      `API_BASE=http://127.0.0.1:8001 BASE_URL=http://127.0.0.1:3001` nếu chạy ở checkout phụ.
- [x] T144 — Đo bằng Playwright MCP trước khi báo xong: khoảng cách 2 nút liền nhau **= 12px** ·
      khối dịch vụ **không tràn ngang** ở 1900/1440/1280/1024 · badge đúng mã màu (đọc
      `getComputedStyle`) · nút "Đã chuẩn bị" **không tồn tại trong DOM** với người ngoài nhóm.
- [x] T145 — Dọn dữ liệu test sinh ra trong lúc đo (kiểm `E2E%` / `DPH-` rác = 0).
- [ ] T146 — Cập nhật `design.md` (nếu phát sinh quyết định mới) + `STATUS.md` + mục
      "LƯU Ý KHI DEPLOY" của plan này (migration 3 bước, seeder danh mục, KHÔNG chạy
      `PermissionsTableSeeder`).

### Task phát sinh trong lúc thực thi Phase 8 (T147–T152)

- [x] T147 — (C3) `assignMeeting()` nhận `services[]` + FE mở khối dịch vụ cho **cả 2 hướng** đăng ký
      (hụt so với quyết định #9 của user, phát hiện lúc làm FE)
- [x] T148 — (C3) BE `index()` lọc theo `service_status` (FE đã gửi tham số nhưng BE chưa có nhánh `where`)
- [x] T149 — (C4) Gom 2 nút dịch vụ liền nhau ở footer popup + bỏ `mr-2` → khoảng cách **8px** đúng
      khuôn 73 file còn lại (trước 16px do cộng dồn với spacing sẵn có của `.modal-footer`)
- [x] T150 — (D0) Vá `V2BaseModal` thiếu computed `subtitleFullText` → khôi phục tooltip dòng mô tả
      cho ~20 popup dùng khuôn này
- [x] T151 — (D1/D2) Chuẩn hoá message validate toàn luồng phòng họp: xoá 46 câu tự chế, thêm 5 key
      cho trường mới của Phase 8, dùng `attributes()` thay vì viết lại cả câu
- [x] T152 — (D3) **Bổ sung 53 mục tiếng Việt vào lang file dùng chung** `vi/validation.php` (0 mục
      còn tiếng Anh) + FE `locales/vi.json` 5 → 31 key; dọn ngược 18 key thừa ở module Meeting

### Checkpoint — 23/09/2026 (Phase 8)

**Vừa hoàn thành:** T109–T127, T131–T142, T144, T145, T147–T152. (**T128–T130 CHƯA làm** —
xem mục 0 của Bước tiếp theo.) Khối A (nhiều người phụ trách phòng), khối B
(danh mục Dịch vụ phòng họp), khối C (yêu cầu dịch vụ trên phiếu) **code done + đã review + đã đo
trên trình duyệt thật**. Nhóm D: đã làm D0/D1/D2/D3.

**Đang làm dở:** không.

**Bước tiếp theo:**
0. ⚠️ **T128–T130 — MÀN FE DANH MỤC DỊCH VỤ CHƯA LÀM** (`pages/meeting/room-services/` chưa tồn tại,
   menu chưa khai). BE đã xong đủ (bảng + 10 route + `/options`), FE mới chỉ dùng `/options` trong
   popup đặt phòng — tức **chưa có chỗ nào thêm/sửa/khoá món dịch vụ trên giao diện**, phải seed hoặc
   sửa thẳng DB. Đây là việc phải làm trước khi bàn giao.
1. **T143 — viết bộ e2e** `e2e/tests/meeting/meeting-room-service.{api.spec,spec}.ts` (8 ca ở mục 10
   của spec, có ca phân quyền 2 chiều). User đã chốt **chạy sau**, nhưng spec thì vẫn phải viết.
2. Rà lại spec e2e sẵn có của màn `meeting/bookings` cho khớp bố cục nút mới (T149).
3. User commit khi ưng — **toàn bộ Phase 8 đang nằm ở working tree, CHƯA commit** (đúng quy ước
   CLAUDE.md: không commit khi chưa có yêu cầu).

**Blocked:** không. 3 việc chờ user quyết (không chặn code): câu lỗi có kèm tên trường hay không ·
sửa `plugins/vee-validate.js` để 4 rule FE hiện được con số · dọn message thừa ở 188 FormRequest khác.

**Số đo chốt lại:**
- PHPUnit toàn bộ suite: **231 tests / 681 assertions**, 5 Errors + 2 Failures = **đúng mức đỏ CÓ SẴN
  từ trước Phase 8** (2 nhóm test cũ của Meeting), không đỏ mới ở bất kỳ module nào.
- `--filter MeetingRoom`: **65 tests / 179 assertions**.
- N+1: `index()` 3 phiếu và 15 phiếu đều **17 query**; sau khi vá `room.managers`, cấu hình 15 phòng
  × 15 phiếu giảm **43 → 11 query** (board 36 → 8).
- DB local đã trả về **baseline 2 phòng / 3 phiếu / 0 dòng dịch vụ / 2 dòng người phụ trách**.

---

### Checkpoint — 30/09/2026 (báo giá + sửa marker xung đột đã lỡ push)

**1. File báo giá** `quan-ly-phong-hop/bao-gia-quan-ly-phong-hop.xlsx` (user yêu cầu 26–28/09):
cây 3 cấp (nhóm chức năng → chức năng → xử lý/logic), 11 nhóm / 121 dòng cấp 3, công chỉ nhập ở
cấp 3, cấp 1–2 tự cộng, đơn giá ô F3 (CHƯA điền), tổng **89.75 công** (Đã xong 45 · Đã xong chưa
commit 6 · Chưa làm 19.75 · Bổ sung mới 19). Số công do Claude ước lượng — chưa được user duyệt.
Kèm 3 chức năng **user mới yêu cầu, CHƯA brainstorm/spec**: (7) Dọn phòng họp — người dọn trên phòng
+ cấu hình thông báo app sau check-out + xác nhận đã dọn; (8) Đánh giá phòng — sao + ghi chú;
(9) Đổi phòng — sang phòng trống, hoặc hoán đổi với user khác. Sheet "Giả định & cần chốt" có 7 câu
phải hỏi khách trước khi làm (ảnh hưởng công). Nhóm 7, 8 phụ thuộc Check-in/Check-out (Phase 5).
Máy không có LibreOffice → công thức chưa recalc, user mở Excel lưu 1 lần.

**2. Marker xung đột lọt vào merge commit đã push** — `8ad4b904d` (merge `03183c203` của khoipv vào
`gop_db`) commit nguyên `<<<<<<<`/`>>>>>>>` trong `pages/meeting/rooms/components/MeetingRoomModal.vue`.
Sửa: giữ `managerLockedOptions` (HEAD, nhiều người phụ trách) + `originalStatus` (khoipv, cảnh báo
Hoạt động → Khoá), BỎ `managerNameNotInStore` (fix kiểu 1 quản lý, đã bị thay). User commit + push
ở `976e1eb32`. Đã kiểm: 0 marker toàn repo client + api, template/script parse được, dev server nạp
component OK. ⚠️ CHƯA mở popup thật: role Super admin (18) trên DB local không có quyền 1586 → màn
`/meeting/rooms` đá 404; cấp tạm quyền bị chặn.

**Bước tiếp theo:** vẫn như checkpoint 23/09 (T128–T130 màn FE Dịch vụ, T143 e2e) + khi khách chốt
báo giá thì brainstorm 3 chức năng mới (trả lời 7 câu ở sheet 2 trước).
