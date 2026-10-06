# Review package — Task 11 (entity phiếu + luật giao giờ + vá lockForUpdate)

## git status
 M Modules/Meeting/Services/MeetingRoomService.php
?? Modules/Meeting/Entities/MeetingRoomBooking.php
?? Modules/Meeting/Entities/MeetingRoomBookingParticipant.php
?? tests/Unit/MeetingRoomBookingOverlapTest.php

### Modules/Meeting/Entities/MeetingRoomBooking.php
```php
<?php

namespace Modules\Meeting\Entities;

use App\Models\BaseModel;
use Carbon\Carbon;

class MeetingRoomBooking extends BaseModel
{
    const STATUS_CHO_DUYET = 1;
    const STATUS_DA_DUYET = 2;
    const STATUS_TU_CHOI = 3;
    const STATUS_DA_HUY = 4;
    const STATUS_HOAN_THANH = 5;

    const SOURCE_TU_DAT = 1;
    const SOURCE_TU_MEETING = 2;

    protected $table = 'meeting_room_bookings';

    protected $fillable = [
        'code', 'meeting_room_id', 'title', 'content', 'start_at', 'end_at', 'status',
        'booked_by_employee_id', 'host_employee_id', 'attendee_count', 'company_id',
        'department_id', 'meeting_id', 'source', 'approved_by', 'approved_at',
        'reject_reason', 'is_auto_rejected', 'cancelled_by', 'cancelled_at', 'cancel_reason',
        'checkin_at', 'checkout_at', 'auto_released_at', 'checkout_reminded_at',
        'recurrence_id', 'created_by', 'updated_by',
    ];

    public function participants()
    {
        return $this->hasMany(MeetingRoomBookingParticipant::class, 'meeting_room_booking_id');
    }

    public function room()
    {
        return $this->belongsTo(MeetingRoom::class, 'meeting_room_id', 'id');
    }

    /**
     * Luật "giao giờ" (spec 5.2): `startA < endB AND endA > startB`. Chạm mép KHÔNG tính trùng
     * (14:00-15:00 và 15:00-16:00 là hợp lệ) — dùng đúng công thức nửa mở, không phải
     * "<=/>=" như thói quen hay viết nhầm.
     *
     * Thuần, static, không đụng DB — tầng gọi (Task 13) chịu trách nhiệm nạp đúng 2 mốc để so.
     */
    public static function overlaps($startA, $endA, $startB, $endB)
    {
        $startA = Carbon::parse($startA);
        $endA = Carbon::parse($endA);
        $startB = Carbon::parse($startB);
        $endB = Carbon::parse($endB);

        return $startA->lt($endB) && $endA->gt($startB);
    }

    public static function statusText($status)
    {
        $map = [
            self::STATUS_CHO_DUYET => 'Chờ duyệt',
            self::STATUS_DA_DUYET => 'Đã duyệt',
            self::STATUS_TU_CHOI => 'Từ chối',
            self::STATUS_DA_HUY => 'Đã hủy',
            self::STATUS_HOAN_THANH => 'Hoàn thành',
        ];

        return $map[$status] ?? '';
    }

    /** 9 mã màu chuẩn của hệ thống (design.md mục 4.8) — BE trả màu, FE/app chỉ hiển thị. */
    public static function statusColor($status)
    {
        $map = [
            self::STATUS_CHO_DUYET => '#D97706',
            self::STATUS_DA_DUYET => '#2563EB',
            self::STATUS_TU_CHOI => '#DC2626',
            self::STATUS_DA_HUY => '#6B7280',
            self::STATUS_HOAN_THANH => '#16A34A',
        ];

        return $map[$status] ?? '';
    }

    /** Người đặt sửa được phiếu của mình khi còn hiệu lực và chưa tới giờ bắt đầu (spec 5.4). */
    public function isCanEdit()
    {
        return in_array((int) $this->status, [self::STATUS_CHO_DUYET, self::STATUS_DA_DUYET], true)
            && Carbon::now()->lt(Carbon::parse($this->start_at));
    }

    /**
     * Spec 5.5: hủy được từ lúc tạo tới trước giờ bắt đầu, TRỪ phiếu sinh từ Meeting
     * (quyết định #12 — `source = 2` không ai hủy được ở màn phòng họp).
     * Chỉ kiểm phần dữ liệu thuần của bản ghi; quyền "ai được bấm" (người đặt/quản lý
     * phòng/quyền 1580) do tầng Service kiểm riêng vì cần actor đăng nhập.
     */
    public function isCanCancel()
    {
        return in_array((int) $this->status, [self::STATUS_CHO_DUYET, self::STATUS_DA_DUYET], true)
            && (int) $this->source !== self::SOURCE_TU_MEETING
            && Carbon::now()->lt(Carbon::parse($this->start_at));
    }

    /** Spec 5.3: chỉ phiếu Chờ duyệt mới duyệt được. */
    public function isCanApprove()
    {
        return (int) $this->status === self::STATUS_CHO_DUYET;
    }

    /** Spec 5.3: chỉ phiếu Chờ duyệt mới từ chối được. */
    public function isCanReject()
    {
        return (int) $this->status === self::STATUS_CHO_DUYET;
    }
}
```

### Modules/Meeting/Entities/MeetingRoomBookingParticipant.php
```php
<?php

namespace Modules\Meeting\Entities;

use App\Models\BaseModel;

class MeetingRoomBookingParticipant extends BaseModel
{
    protected $table = 'meeting_room_booking_participants';

    /**
     * `SHOW COLUMNS meeting_room_booking_participants` thật (worktree, DB hrm_erp): chỉ có
     * id / meeting_room_booking_id / employee_id / created_at / updated_at — KHÔNG có
     * created_by / updated_by (khác `meeting_room_bookings`). `BaseModel::boot()` tự bỏ qua
     * 2 cột này vì đã bọc `Schema::hasColumn`, nên không đưa vào $fillable ở đây.
     */
    protected $fillable = [
        'meeting_room_booking_id', 'employee_id',
    ];

    public function booking()
    {
        return $this->belongsTo(MeetingRoomBooking::class, 'meeting_room_booking_id', 'id');
    }

    public function employee()
    {
        return $this->belongsTo(\Modules\Timesheet\Entities\Employee::class, 'employee_id', 'id');
    }
}
```

### tests/Unit/MeetingRoomBookingOverlapTest.php
```php
<?php
namespace Tests\Unit;

use Tests\TestCase;
use Modules\Meeting\Entities\MeetingRoomBooking;

class MeetingRoomBookingOverlapTest extends TestCase
{
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
}
```

### diff MeetingRoomService.php (vá bẫy 3)
```diff
diff --git a/Modules/Meeting/Services/MeetingRoomService.php b/Modules/Meeting/Services/MeetingRoomService.php
index e101f0ef4..2a63801a4 100644
--- a/Modules/Meeting/Services/MeetingRoomService.php
+++ b/Modules/Meeting/Services/MeetingRoomService.php
@@ -7,6 +7,7 @@ use Illuminate\Support\Facades\DB;
 use Modules\Human\Entities\Company;
 use Modules\Meeting\Entities\MeetingRoom;
 use Modules\Meeting\Entities\MeetingRoomAmenity;
+use Modules\Meeting\Entities\MeetingRoomBooking;
 use Modules\Timesheet\Entities\GeneralRegulation;
 use Modules\Training\Services\BaseService;
 
@@ -178,9 +179,24 @@ class MeetingRoomService extends BaseService
      * `meeting_room_room_amenity` (không có FK ON DELETE CASCADE trước fix mục A.3) — 78 dòng đã
      * đo được trong DB trước khi sửa. `detach()` TRƯỚC khi xóa phòng, cùng 1 transaction với
      * lệnh xóa (controller đã bọc `DB::transaction` quanh lời gọi hàm này).
+     *
+     * Bẫy 3 (review Phase 1, task-11-brief): `MeetingRoomController::destroy()` kiểm
+     * `isCanDelete()` (đọc KHÔNG khóa) rồi mới mở transaction — giữa 2 bước đó, một request
+     * khác có thể vừa tạo phiếu đặt phòng xen vào, tạo ra phiếu mồ côi khi phòng bị xóa. Kiểm
+     * lại lần nữa Ở ĐÂY, bên TRONG transaction mà controller đã mở, và khóa (`lockForUpdate`)
+     * mọi phiếu của phòng trước khi quyết định cho xóa: request tạo phiếu song song phải đợi
+     * transaction này commit/rollback xong, không còn cửa sổ hở giữa kiểm tra và xóa.
      */
     public function destroy(MeetingRoom $meetingRoom)
     {
+        $hasBooking = MeetingRoomBooking::where('meeting_room_id', $meetingRoom->id)
+            ->lockForUpdate()
+            ->exists();
+
+        if ($hasBooking) {
+            throw new \Exception('Phòng họp này đã có phiếu đặt nên không xóa được. Bạn có thể Khóa phòng.');
+        }
+
         $meetingRoom->amenities()->detach();
         $meetingRoom->delete();
     }
```

## Cột thật của 2 bảng
```
Field	Type	Null	Key	Default	Extra
id	bigint unsigned	NO	PRI	NULL	auto_increment
code	varchar(50)	NO	UNI	NULL	
meeting_room_id	bigint unsigned	NO	MUL	NULL	
title	varchar(255)	NO		NULL	
content	text	YES		NULL	
start_at	datetime	NO		NULL	
end_at	datetime	NO		NULL	
status	tinyint	NO	MUL	NULL	
booked_by_employee_id	bigint unsigned	NO	MUL	NULL	
host_employee_id	bigint unsigned	YES		NULL	
attendee_count	int	YES		NULL	
company_id	bigint unsigned	YES		NULL	
department_id	bigint unsigned	YES		NULL	
meeting_id	bigint unsigned	YES	UNI	NULL	
source	tinyint	NO		1	
approved_by	bigint unsigned	YES		NULL	
approved_at	datetime	YES		NULL	
reject_reason	varchar(500)	YES		NULL	
is_auto_rejected	tinyint	NO		0	
cancelled_by	bigint unsigned	YES		NULL	
cancelled_at	datetime	YES		NULL	
cancel_reason	varchar(500)	YES		NULL	
checkin_at	datetime	YES		NULL	
checkout_at	datetime	YES		NULL	
auto_released_at	datetime	YES		NULL	
checkout_reminded_at	datetime	YES		NULL	
recurrence_id	bigint unsigned	YES	MUL	NULL	
created_by	bigint unsigned	YES		NULL	
updated_by	bigint unsigned	YES		NULL	
created_at	timestamp	YES		NULL	
updated_at	timestamp	YES		NULL	
Field	Type	Null	Key	Default	Extra
id	bigint unsigned	NO	PRI	NULL	auto_increment
meeting_room_booking_id	bigint unsigned	NO	MUL	NULL	
employee_id	bigint unsigned	NO		NULL	
created_at	timestamp	YES		NULL	
updated_at	timestamp	YES		NULL	
```
