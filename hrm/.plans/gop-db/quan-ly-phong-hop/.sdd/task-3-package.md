# Review package — Task 3 (2 Entity + unit test)

## File thuộc task này

### Modules/Meeting/Entities/MeetingRoomAmenity.php
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

### Modules/Meeting/Entities/MeetingRoom.php
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

### tests/Unit/MeetingRoomConfigTest.php
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

## Cột thật trong DB để đối chiếu $fillable
```
Field	Type	Null	Key	Default	Extra
id	bigint unsigned	NO	PRI	NULL	auto_increment
code	varchar(50)	NO		NULL	
name	varchar(255)	NO		NULL	
company_id	bigint unsigned	NO	MUL	NULL	
department_id	bigint unsigned	YES		NULL	
part_id	bigint unsigned	YES		NULL	
allow_cross_company	tinyint	NO		0	
location	varchar(255)	YES		NULL	
capacity	int	YES		NULL	
manager_employee_id	bigint unsigned	YES		NULL	
require_approval	tinyint	NO		0	
open_time	time	YES		NULL	
close_time	time	YES		NULL	
checkin_grace_minutes	int	YES		NULL	
checkin_qr_token	char(36)	YES	UNI	NULL	
description	text	YES		NULL	
status	tinyint	NO		1	
created_by	bigint unsigned	YES		NULL	
updated_by	bigint unsigned	YES		NULL	
created_at	timestamp	YES		NULL	
updated_at	timestamp	YES		NULL	
Field	Type	Null	Key	Default	Extra
id	bigint unsigned	NO	PRI	NULL	auto_increment
code	varchar(50)	NO	UNI	NULL	
name	varchar(255)	NO		NULL	
icon	varchar(100)	YES		NULL	
sort_order	int	NO		0	
status	tinyint	NO		1	
created_by	bigint unsigned	YES		NULL	
updated_by	bigint unsigned	YES		NULL	
created_at	timestamp	YES		NULL	
updated_at	timestamp	YES		NULL	
```
