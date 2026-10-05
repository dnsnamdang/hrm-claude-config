> ## ⚠️ NƠI LÀM VIỆC — WORKTREE (chốt 17/09/2026, user yêu cầu)
>
> Nhánh `gop_db` đang được một phiên làm việc khác dùng → mọi thay đổi code của plan này làm trong
> **worktree riêng**, nhánh `feat/quan-ly-phong-hop`:
>
> | Thứ | Đường dẫn |
> |---|---|
> | Repo BE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` |
> | Repo FE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client` |
> | Bộ e2e | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (DÙNG CHUNG, không có worktree) |
> | Tài liệu (plan, ledger) | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/` |
>
> - API của worktree chạy ở **`http://127.0.0.1:8001`**, Nuxt của worktree ở **`http://127.0.0.1:3001`**.
>   Cổng 8000/3000 là server của phiên khác — **KHÔNG đụng, KHÔNG tắt, KHÔNG `pkill`**.
> - Chạy e2e phải truyền cả 2 biến: `BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`.
> - Phiên đăng nhập của Playwright gắn theo ORIGIN. `.auth/user.json` chỉ dùng được cho `:3000` → đã tạo sẵn
>   **`.auth/user-wt.json`** (admin) và **`.auth/user-nocost-wt.json`** (tài khoản thiếu quyền) với origin
>   đổi sang `:3001`. Spec UI phải khai `test.use({ storageState: '.auth/user-wt.json' })`, KHÔNG dùng
>   `user.json` (dùng nhầm là bị đẩy về `/login`, rất dễ tưởng lỗi đăng nhập).
> - TUYỆT ĐỐI KHÔNG `git commit` / `push` / `stash` / `checkout` file.
> - Worktree KHÔNG có `.plans`, `.claude`, `docs`, `CLAUDE.md` (là symlink ngoài repo) — tài liệu ghi về
>   đường dẫn tài liệu ở bảng trên.
> - Đường dẫn trong phần dưới ghi `hrm-api/...` hay `hrm-client/...` thì hiểu là **thư mục tương ứng trong
>   worktree**, không phải checkout gốc.


> **Ghi chú từ người điều phối (đã đọc `app/Models/BaseModel.php` trước, dùng luôn — đừng khảo sát lại):**
> - `BaseModel::boot()` là `public static function boot()` có gọi `parent::boot()`, và tự gán `created_by`
>   / `updated_by` = `Auth::user()->id` khi bảng có cột đó. Vì vậy hook UUID của `MeetingRoom` phải đặt ở
>   **`protected static function booted()`** (như code trong brief) — KHÔNG override `boot()`, ghi đè là mất
>   audit mà không có lỗi nào báo ra.
> - ⚠️ `BaseModel` còn tự điền **`company_id`** từ `auth()->user()->info->company_id` khi model có cột
>   `company_id` và giá trị đang trống. Với `meeting_rooms` thì `company_id` do người dùng chọn nên Request
>   phải để `required` (Task 6 lo); ở Task 3 chỉ cần biết để không ngạc nhiên khi test thấy cột tự có giá trị.
> - `BaseModel` dùng trait `LogsActivity` — tạo/sửa bản ghi sẽ ghi activity log, đó là hành vi đúng của dự án.


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

- [ ] **Bước 1: Viết test đỏ**

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

- [ ] **Bước 2: Chạy test, xác nhận ĐỎ**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomConfigTest
```
Kỳ vọng: FAIL — `Class "Modules\Meeting\Entities\MeetingRoom" not found`.

- [ ] **Bước 3: Viết `MeetingRoomAmenity`**

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

- [ ] **Bước 4: Viết `MeetingRoom` (phần logic thuần trước)**

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

- [ ] **Bước 5: Chạy test, xác nhận XANH**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoomConfigTest
```
Kỳ vọng: OK (2 tests).

- [ ] **Bước 6: Tự kiểm audit** — grep xác nhận cả 2 entity đều `extends BaseModel` và có
`created_by`/`updated_by` trong `$fillable`:

```bash
grep -n "extends BaseModel\|created_by" Modules/Meeting/Entities/*.php
```

---
