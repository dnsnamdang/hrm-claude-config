## Phạm vi review: lượt C1 (T131–T137 + T131b)

## diff --stat (file C1 đã sửa)

## diff -U10

## FILE MỚI: Modules/Meeting/Database/Migrations/2026_09_23_000003_create_meeting_room_booking_services_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

/**
 * Phase 8, lượt C1 (T131) — 1 dòng "món dịch vụ" (trà, nước, hoa quả...) được người đặt phòng yêu
 * cầu trên MỘT phiếu đặt phòng cụ thể. `service_name`/`unit` là SNAPSHOT tại thời điểm tạo, KHÔNG
 * join lại danh mục `meeting_room_services` lúc hiển thị (danh mục đổi tên sau đó không được làm
 * sai lệch phiếu cũ).
 *
 * `service_id` NULLABLE (khác `booking_id`): phòng thủ cho trường hợp món trong danh mục bị mất đi
 * (dù luồng Xoá của danh mục — `MeetingRoomService::usedCount()`, T131b — đã chặn xoá món đang
 * được phiếu dùng), dòng lịch sử dịch vụ của phiếu cũ vẫn đọc được `service_name` snapshot dù
 * `service_id` không còn trỏ tới đâu.
 */
class CreateMeetingRoomBookingServicesTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_booking_services', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('booking_id')->index();
            $table->unsignedBigInteger('service_id')->nullable()->index();
            $table->string('service_name', 255);
            $table->string('unit', 50)->nullable();
            $table->decimal('quantity', 12, 2);
            $table->string('note', 255)->nullable();
            $table->integer('sort_order')->default(0);
            $table->timestamps();

            $table->foreign('booking_id', 'mrbs_booking_fk')
                ->references('id')->on('meeting_room_bookings')->onDelete('cascade');
            $table->unique(['booking_id', 'service_id'], 'mrbs_booking_service_unique');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_booking_services');
    }
}
```

## FILE MỚI: Modules/Meeting/Database/Migrations/2026_09_23_000004_add_service_columns_to_meeting_room_bookings_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

/**
 * Phase 8, lượt C1 (T131) — 4 cột theo dõi trạng thái "yêu cầu dịch vụ" ngay trên phiếu đặt phòng.
 *
 * `service_status` NULLABLE là điểm mấu chốt: `NULL` = phiếu KHÔNG kèm yêu cầu dịch vụ nào, khác
 * hẳn `1` = "đã yêu cầu, chưa ai chuẩn bị". Gộp chung 2 nghĩa này (vd mặc định về 0/1) làm bộ lọc
 * và badge màn danh sách sai cho MỌI phiếu — xem thêm design mục 7 (10 luật nghiệp vụ), luật 1.
 */
class AddServiceColumnsToMeetingRoomBookingsTable extends Migration
{
    public function up()
    {
        Schema::table('meeting_room_bookings', function (Blueprint $table) {
            $table->tinyInteger('service_status')
                ->nullable()
                ->comment('NULL không yêu cầu dịch vụ, 1 Chờ chuẩn bị, 2 Đã chuẩn bị, 3 Từ chối')
                ->after('recurrence_id');
            $table->unsignedBigInteger('service_handled_by')->nullable()->after('service_status');
            $table->dateTime('service_handled_at')->nullable()->after('service_handled_by');
            $table->string('service_reject_reason', 500)->nullable()->after('service_handled_at');
        });
    }

    public function down()
    {
        Schema::table('meeting_room_bookings', function (Blueprint $table) {
            $table->dropColumn(['service_status', 'service_handled_by', 'service_handled_at', 'service_reject_reason']);
        });
    }
}
```

## FILE MỚI: Modules/Meeting/Entities/MeetingRoomBookingServiceItem.php
```php
<?php

namespace Modules\Meeting\Entities;

use App\Models\BaseModel;

/**
 * Phase 8, lượt C1 (T131) — 1 dòng "món dịch vụ" được yêu cầu trên MỘT phiếu đặt phòng.
 *
 * Đặt tên `MeetingRoomBookingServiceItem` — KHÔNG đặt `MeetingRoomBookingService` vì đụng
 * `Services/MeetingRoomBookingService.php` (service tầng nghiệp vụ của phiếu) đang tồn tại.
 *
 * `service_name`/`unit` là SNAPSHOT lúc tạo (đọc từ danh mục `meeting_room_services` tại thời
 * điểm `MeetingRoomBookingService::store()` chạy) — KHÔNG join lại danh mục lúc hiển thị, danh
 * mục đổi tên sau đó không được làm sai lệch phiếu cũ (brief T133).
 *
 * Cùng khuôn bảng con snapshot-theo-phiếu `meeting_room_booking_participants`: KHÔNG có
 * `created_by`/`updated_by` (bảng không có 2 cột này — `BaseModel::boot()` tự bỏ qua nhờ
 * `Schema::hasColumn()`, không lỗi gì khi thiếu).
 */
class MeetingRoomBookingServiceItem extends BaseModel
{
    protected $table = 'meeting_room_booking_services';

    protected $fillable = [
        'booking_id', 'service_id', 'service_name', 'unit', 'quantity', 'note', 'sort_order',
    ];

    public function booking()
    {
        return $this->belongsTo(MeetingRoomBooking::class, 'booking_id', 'id');
    }

    /** Danh mục gốc — có thể `null` nếu món đã mất đi (xem docblock migration, phòng thủ). */
    public function service()
    {
        return $this->belongsTo(MeetingRoomService::class, 'service_id', 'id');
    }
}
```

## FILE MỚI: Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingServiceRejectRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoomBooking;

use Modules\Training\Http\Requests\BaseRequest;

/**
 * Phase 8, lượt C1 (T135) — validate body của PUT
 * `/meeting/room-bookings/{id}/service-rejected`. Field tên `reason` (KHÔNG phải
 * `service_reject_reason`/`reject_reason`) — đúng nguyên văn brief T135.
 *
 * CHỈ khai `rules()`, KHÔNG khai `messages()` — câu chuẩn cho `required`/`max` đã có sẵn ở lang
 * file (CLAUDE.md).
 */
class MeetingRoomBookingServiceRejectRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'reason' => ['required', 'string', 'max:500'],
        ];
    }
}
```

## FILE MỚI: tests/Feature/MeetingRoomBookingServiceRequestTest.php
```php
<?php

namespace Tests\Feature;

use App\Models\TpEmployee;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Meeting\Entities\MeetingRoom;
use Modules\Meeting\Entities\MeetingRoomBooking;
use Modules\Meeting\Entities\MeetingRoomService;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomServiceController;
use Modules\Meeting\Services\MeetingRoomBookingService;
use Tests\TestCase;

/**
 * Phase 8, lượt C1 (T131-T137) — "Yêu cầu dịch vụ" trên phiếu đặt phòng. Bằng chứng cho mục
 * "Cách tự kiểm" #2 của brief `.sdd/p8-C1-brief.md` (7 ca tối thiểu) + T131b (1 ca chặn xoá món
 * đang được phiếu dùng, đúng cột `service_id`).
 *
 * Actor TÁI DÙNG nguyên bộ 4 người của `MeetingRoomManagersTest.php` (đã kiểm bằng tinker trước
 * khi chọn, KHÔNG có sẵn quyền "Xem tất cả phiếu đặt phòng họp"/"Duyệt phiếu đặt phòng họp" — dùng
 * làm actor "ngoài nhóm" mà có sẵn quyền là xanh giả):
 *   - employee 24, 25 = 2 người phụ trách phòng test (company_id=1).
 *   - employee 27 = người đặt phiếu.
 *   - employee 28 = người NGOÀI nhóm (không quản lý, không đặt, không có 2 quyền trên).
 *
 * Không dùng RefreshDatabase (khớp `MeetingRoomBookingRaceTest`/`MeetingRoomManagersTest` — TestCase
 * gốc không tự rollback) — tự dọn dữ liệu ở tearDown(). `meeting_room_booking_services` xoá THEO
 * TAY (không chỉ dựa FK cascade) để chắc chắn sạch kể cả khi 1 ca fail giữa chừng.
 */
class MeetingRoomBookingServiceRequestTest extends TestCase
{
    private const MANAGER_A_ID = 24;
    private const MANAGER_B_ID = 25;
    private const BOOKER_ID = 27;
    private const OUTSIDER_ID = 28;

    /** @var int[] */
    private $roomIdsToCleanup = [];

    /** @var int[] */
    private $bookingIdsToCleanup = [];

    /** @var int[] danh mục dịch vụ tạo TẠM cho ca T131b, xoá lại ở tearDown() */
    private $catalogServiceIdsToCleanup = [];

    protected function tearDown(): void
    {
        foreach ($this->bookingIdsToCleanup as $bookingId) {
            // FK `mrbs_booking_fk` (ON DELETE CASCADE) đã tự xoá dòng `meeting_room_booking_services`
            // liên quan, nhưng vẫn xoá TƯỜNG MINH thêm 1 lần để test không phụ thuộc HOÀN TOÀN vào
            // cascade (đúng tinh thần "tự dọn", phòng khi 1 ca fail giữa chừng trước khi FK kịp chạy).
            DB::table('meeting_room_booking_services')->where('booking_id', $bookingId)->delete();
            DB::table('catalog_histories')->where('table_name', 'meeting_room_bookings')->where('table_id', $bookingId)->delete();
            DB::table('meeting_room_bookings')->where('id', $bookingId)->delete();
        }
        foreach ($this->roomIdsToCleanup as $roomId) {
            DB::table('meeting_room_managers')->where('meeting_room_id', $roomId)->delete();
            DB::table('meeting_rooms')->where('id', $roomId)->delete();
        }
        foreach ($this->catalogServiceIdsToCleanup as $serviceId) {
            DB::table('catalog_histories')->where('table_name', 'meeting_room_services')->where('table_id', $serviceId)->delete();
            DB::table('meeting_room_services')->where('id', $serviceId)->delete();
        }
        $this->bookingIdsToCleanup = [];
        $this->roomIdsToCleanup = [];
        $this->catalogServiceIdsToCleanup = [];

        parent::tearDown();
    }

    /** @param int[] $managerIds */
    private function createTestRoom(string $suffix, array $managerIds, bool $requireApproval = false): int
    {
        // Cùng bẫy đã ghi ở `MeetingRoomManagersTest` — `meeting_rooms` KHÔNG còn cột `code`.
        $roomId = DB::table('meeting_rooms')->insertGetId([
            'name' => 'PHPUnit Service Room ' . $suffix . '_' . time() . '_' . mt_rand(1000, 9999),
            'company_id' => 1,
            'status' => MeetingRoom::STATUS_ACTIVE,
            'require_approval' => $requireApproval ? 1 : 0,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        $this->roomIdsToCleanup[] = $roomId;

        foreach ($managerIds as $employeeId) {
            DB::table('meeting_room_managers')->insert([
                'meeting_room_id' => $roomId,
                'employee_id' => $employeeId,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }

        return $roomId;
    }

    /**
     * @param  array<int, array{service_id:int, quantity:float, note?:string}> $services
     */
    private function buildStoreRequest(int $roomId, array $services, \DateTimeInterface $startAt, \DateTimeInterface $endAt): Request
    {
        return Request::create('/', 'POST', [
            'meeting_room_id' => $roomId,
            // Bypass FormRequest (gọi thẳng Service, cùng khuôn `MeetingRoomManagersTest`) nên
            // `purpose_id` không cần tồn tại thật — `store()` không tự validate FK này, chỉ
            // FormRequest (đã bị bỏ qua ở test này) mới `exists:meeting_room_purposes,id`.
            'purpose_id' => null,
            'title' => 'PHPUnit Service Booking_' . time() . '_' . mt_rand(1000, 9999),
            'start_at' => $startAt->format('Y-m-d H:i:s'),
            'end_at' => $endAt->format('Y-m-d H:i:s'),
            'services' => $services,
        ]);
    }

    /** 3 dịch vụ Hoạt động ĐẦU TIÊN của danh mục thật (baseline local: 5 món, seed sẵn). */
    private function firstActiveServices(int $limit = 3)
    {
        return MeetingRoomService::where('status', MeetingRoomService::STATUS_ACTIVE)
            ->orderBy('id')
            ->limit($limit)
            ->get();
    }

    /**
     * Ca 1/7 — tạo phiếu 3 món -> 3 dòng bảng con, `service_status = 1`, SNAPSHOT tên/đơn vị tính
     * đúng NGAY TẠI THỜI ĐIỂM TẠO (T133) — đổi tên danh mục SAU khi tạo không được ảnh hưởng dòng
     * đã lưu, kiểm bằng cách đổi tên danh mục NGAY SAU KHI TẠO rồi so sánh snapshot vẫn giữ tên CŨ.
     */
    public function test_tao_phieu_ba_mon_tao_dung_ba_dong_va_snapshot_dung()
    {
        $roomId = $this->createTestRoom('3MON', [self::MANAGER_A_ID]);
        $catalog = $this->firstActiveServices(3);
        $this->assertCount(3, $catalog, 'Cần >= 3 dịch vụ Hoạt động trong danh mục local để chạy ca này');

        $originalNames = $catalog->pluck('name', 'id')->all();

        $services = $catalog->values()->map(function ($item, $index) {
            return ['service_id' => $item->id, 'quantity' => $index + 1, 'note' => 'Ghi chú dòng ' . $index];
        })->all();

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $request = $this->buildStoreRequest(
            $roomId,
            $services,
            now()->addDays(30)->setTime(9, 0),
            now()->addDays(30)->setTime(10, 0)
        );

        $service = app(MeetingRoomBookingService::class);
        $booking = $service->store($request);
        $this->bookingIdsToCleanup[] = $booking->id;

        $this->assertSame(
            MeetingRoomBooking::SERVICE_STATUS_CHO_CHUAN_BI,
            (int) MeetingRoomBooking::find($booking->id)->service_status,
            'Phiếu có dịch vụ phải ra service_status = 1 (Chờ chuẩn bị)'
        );

        $rows = DB::table('meeting_room_booking_services')->where('booking_id', $booking->id)->orderBy('sort_order')->get();
        $this->assertCount(3, $rows, 'Phải tạo đúng 3 dòng bảng con');

        // Đổi tên danh mục NGAY SAU KHI TẠO — snapshot đã lưu không được đổi theo.
        foreach ($catalog as $item) {
            MeetingRoomService::where('id', $item->id)->update(['name' => 'ĐÃ ĐỔI TÊN ' . $item->id]);
        }

        $rowsAfterRename = DB::table('meeting_room_booking_services')->where('booking_id', $booking->id)->orderBy('sort_order')->get();
        foreach ($rowsAfterRename as $index => $row) {
            $originalService = $catalog->values()[$index];
            $this->assertSame(
                $originalNames[$originalService->id],
                $row->service_name,
                'Snapshot service_name PHẢI giữ nguyên tên LÚC TẠO, không đổi theo danh mục sau này'
            );
            $this->assertSame($originalService->unit, $row->unit, 'Snapshot unit phải khớp danh mục lúc tạo');
            $this->assertSame((float) ($index + 1), (float) $row->quantity, 'Số lượng phải đúng thứ tự user gửi lên');
            $this->assertSame($index, (int) $row->sort_order, 'sort_order phải ĐÚNG thứ tự user gửi lên (0,1,2)');
        }

        // Khôi phục tên danh mục để không ảnh hưởng ca test khác chạy sau trong cùng tiến trình.
        foreach ($catalog as $item) {
            MeetingRoomService::where('id', $item->id)->update(['name' => $originalNames[$item->id]]);
        }
    }

    /** Ca 2/7 — tạo phiếu KHÔNG món nào -> `service_status` phải là NULL (khác 0/1). */
    public function test_tao_phieu_khong_mon_thi_service_status_null()
    {
        $roomId = $this->createTestRoom('NOMON', [self::MANAGER_A_ID]);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $request = $this->buildStoreRequest($roomId, [], now()->addDays(31)->setTime(9, 0), now()->addDays(31)->setTime(10, 0));

        $booking = app(MeetingRoomBookingService::class)->store($request);
        $this->bookingIdsToCleanup[] = $booking->id;

        $fresh = MeetingRoomBooking::find($booking->id);
        $this->assertNull($fresh->service_status, 'Phiếu không kèm dịch vụ PHẢI ra service_status = NULL, không phải 0/1');
        $this->assertSame(0, DB::table('meeting_room_booking_services')->where('booking_id', $booking->id)->count());
    }

    /**
     * Ca 3/7 — `update()` gửi kèm `services[]` mới -> dữ liệu dịch vụ ĐÃ LƯU không đổi (luật 2:
     * dịch vụ chỉ nhập lúc TẠO). Không lỗi, chỉ lặng lẽ bỏ qua field này.
     */
    public function test_update_gui_kem_services_du_lieu_dich_vu_khong_doi()
    {
        $roomId = $this->createTestRoom('UPD', [self::MANAGER_A_ID]);
        $catalog = $this->firstActiveServices(2);
        $this->assertGreaterThanOrEqual(2, $catalog->count());

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 1, 'note' => null]],
            now()->addDays(32)->setTime(9, 0),
            now()->addDays(32)->setTime(10, 0)
        );
        $booking = app(MeetingRoomBookingService::class)->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        $rowsBefore = DB::table('meeting_room_booking_services')->where('booking_id', $booking->id)->get();
        $this->assertCount(1, $rowsBefore);
        $statusBefore = MeetingRoomBooking::find($booking->id)->service_status;

        // PUT gửi kèm services[] KHÁC HẲN (2 món khác, số lượng khác) — phải bị Service lờ đi.
        $updateRequest = Request::create('/', 'PUT', [
            'meeting_room_id' => $roomId,
            'title' => 'PHPUnit Service Booking Updated_' . time(),
            'start_at' => now()->addDays(32)->setTime(9, 0)->format('Y-m-d H:i:s'),
            'end_at' => now()->addDays(32)->setTime(10, 30)->format('Y-m-d H:i:s'),
            'services' => [
                ['service_id' => $catalog[1]->id, 'quantity' => 99, 'note' => 'Không được ghi vào DB'],
            ],
        ]);

        app(MeetingRoomBookingService::class)->update(MeetingRoomBooking::findOrFail($booking->id), $updateRequest);

        $rowsAfter = DB::table('meeting_room_booking_services')->where('booking_id', $booking->id)->orderBy('id')->get();
        $this->assertCount(1, $rowsAfter, 'Số dòng dịch vụ KHÔNG được đổi sau update()');
        $this->assertSame($rowsBefore[0]->service_id, $rowsAfter[0]->service_id, 'service_id của dòng dịch vụ KHÔNG được đổi');
        $this->assertSame((float) $rowsBefore[0]->quantity, (float) $rowsAfter[0]->quantity, 'quantity KHÔNG được đổi (99 của payload PUT phải bị bỏ qua)');
        $this->assertSame(
            (string) $statusBefore,
            (string) MeetingRoomBooking::find($booking->id)->service_status,
            'service_status KHÔNG được đổi sau update()'
        );
    }

    /** Ca 4/7 — người TRONG nhóm phụ trách bấm "Đã chuẩn bị" -> service_status = 2 + ghi service_handled_by. */
    public function test_nguoi_trong_nhom_phu_trach_bam_da_chuan_bi_thanh_cong()
    {
        $roomId = $this->createTestRoom('PREP', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        $catalog = $this->firstActiveServices(1);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 2, 'note' => null]],
            now()->addDays(33)->setTime(9, 0),
            now()->addDays(33)->setTime(10, 0)
        );
        $booking = app(MeetingRoomBookingService::class)->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        $this->actingAs(TpEmployee::find(self::MANAGER_A_ID), 'api');
        $result = app(MeetingRoomBookingService::class)->servicePrepared(MeetingRoomBooking::findOrFail($booking->id));

        $this->assertSame(MeetingRoomBooking::SERVICE_STATUS_DA_CHUAN_BI, (int) $result->service_status);
        $this->assertSame(self::MANAGER_A_ID, (int) $result->service_handled_by, 'Phải ghi ĐÚNG người vừa bấm vào service_handled_by');
        $this->assertNotNull($result->service_handled_at);
    }

    /** Ca 5/7 — NGƯỜI THỨ HAI bấm SAU (dù cùng là quản lý phòng) -> 409, kèm câu nêu ai đã xử lý. */
    public function test_nguoi_thu_hai_bam_sau_tra_409()
    {
        $roomId = $this->createTestRoom('RACE', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        $catalog = $this->firstActiveServices(1);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 1, 'note' => null]],
            now()->addDays(34)->setTime(9, 0),
            now()->addDays(34)->setTime(10, 0)
        );
        $booking = app(MeetingRoomBookingService::class)->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        $service = app(MeetingRoomBookingService::class);

        $this->actingAs(TpEmployee::find(self::MANAGER_A_ID), 'api');
        $service->servicePrepared(MeetingRoomBooking::findOrFail($booking->id));

        $this->actingAs(TpEmployee::find(self::MANAGER_B_ID), 'api');
        $caught = null;
        try {
            $service->servicePrepared(MeetingRoomBooking::findOrFail($booking->id));
        } catch (\Exception $e) {
            $caught = $e;
        }

        $this->assertNotNull($caught, 'Người thứ hai bấm SAU PHẢI bị chặn bằng exception');
        $this->assertSame(409, $caught->getCode(), 'Đúng mã lỗi 409 (race condition), không phải mã khác. Message: ' . $caught->getMessage());
        $this->assertStringContainsString(
            'đã được',
            mb_strtolower($caught->getMessage()),
            'Message 409 phải nêu rõ AI đã xử lý (luật 5). Message thật: ' . $caught->getMessage()
        );

        $this->assertSame(
            MeetingRoomBooking::SERVICE_STATUS_DA_CHUAN_BI,
            (int) MeetingRoomBooking::find($booking->id)->service_status,
            'service_status phải giữ nguyên kết quả của người BẤM TRƯỚC (A), không bị người B ghi đè'
        );
        $this->assertSame(self::MANAGER_A_ID, (int) MeetingRoomBooking::find($booking->id)->service_handled_by);
    }

    /** Ca 6/7 (phân quyền, bắt buộc) — người NGOÀI nhóm phụ trách bấm -> 403, dữ liệu không đổi. */
    public function test_nguoi_ngoai_nhom_bam_bi_chan_403()
    {
        $roomId = $this->createTestRoom('OUT', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        $catalog = $this->firstActiveServices(1);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 1, 'note' => null]],
            now()->addDays(35)->setTime(9, 0),
            now()->addDays(35)->setTime(10, 0)
        );
        $booking = app(MeetingRoomBookingService::class)->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        $this->actingAs(TpEmployee::find(self::OUTSIDER_ID), 'api');
        $service = app(MeetingRoomBookingService::class);

        $caught = null;
        try {
            $service->servicePrepared(MeetingRoomBooking::findOrFail($booking->id));
        } catch (\Exception $e) {
            $caught = $e;
        }

        $this->assertNotNull($caught, 'Người NGOÀI nhóm phụ trách PHẢI bị chặn bằng exception');
        $this->assertSame(403, $caught->getCode(), 'Đúng mã lỗi 403 (permission). Message: ' . $caught->getMessage());
        $this->assertSame(
            MeetingRoomBooking::SERVICE_STATUS_CHO_CHUAN_BI,
            (int) MeetingRoomBooking::find($booking->id)->service_status,
            'service_status PHẢI giữ nguyên "Chờ chuẩn bị" — không được xử lý lọt'
        );
        $this->assertNull(MeetingRoomBooking::find($booking->id)->service_handled_by);

        // Cùng guard, cùng actor — Từ chối dịch vụ cũng phải bị chặn giống hệt (điều kiện 1 dùng
        // chung `assertCanHandleServiceRequest()` cho cả 2 hành động).
        $caughtReject = null;
        try {
            $service->serviceRejected(MeetingRoomBooking::findOrFail($booking->id), 'Không đủ nguyên liệu');
        } catch (\Exception $e) {
            $caughtReject = $e;
        }
        $this->assertNotNull($caughtReject);
        $this->assertSame(403, $caughtReject->getCode());
    }

    /**
     * Ca 7/7 — phiếu đã Hủy thì KHÔNG xử lý dịch vụ được nữa (423), và `service_status` GIỮ
     * NGUYÊN = 1 (luật 6 đóng băng — lịch sử phải đọc được "đã yêu cầu mà chưa ai xử lý").
     */
    public function test_phieu_da_huy_khong_xu_ly_dich_vu_duoc_va_giu_nguyen_service_status_1()
    {
        $roomId = $this->createTestRoom('CANCEL', [self::MANAGER_A_ID]);
        $catalog = $this->firstActiveServices(1);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 1, 'note' => null]],
            now()->addDays(36)->setTime(9, 0),
            now()->addDays(36)->setTime(10, 0)
        );
        $bookingService = app(MeetingRoomBookingService::class);
        $booking = $bookingService->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        // Người đặt tự hủy phiếu của mình (spec 5.5) — vẫn actingAs BOOKER.
        $bookingService->cancel(MeetingRoomBooking::findOrFail($booking->id), 'Đổi kế hoạch, không họp nữa');

        $cancelled = MeetingRoomBooking::find($booking->id);
        $this->assertSame(MeetingRoomBooking::STATUS_DA_HUY, (int) $cancelled->status);
        $this->assertSame(
            MeetingRoomBooking::SERVICE_STATUS_CHO_CHUAN_BI,
            (int) $cancelled->service_status,
            'Luật 6 (đóng băng): Hủy phiếu KHÔNG được tự đổi service_status — phải giữ nguyên 1'
        );

        // Quản lý phòng bấm "Đã chuẩn bị" trên phiếu đã Hủy -> phải bị chặn (423), KHÔNG lọt qua.
        $this->actingAs(TpEmployee::find(self::MANAGER_A_ID), 'api');
        $caught = null;
        try {
            $bookingService->servicePrepared(MeetingRoomBooking::findOrFail($booking->id));
        } catch (\Exception $e) {
            $caught = $e;
        }

        $this->assertNotNull($caught, 'Phiếu đã Hủy PHẢI chặn xử lý dịch vụ');
        $this->assertSame(423, $caught->getCode(), 'Đúng mã lỗi 423 (sai trạng thái phiếu). Message: ' . $caught->getMessage());
        $this->assertSame(
            MeetingRoomBooking::SERVICE_STATUS_CHO_CHUAN_BI,
            (int) MeetingRoomBooking::find($booking->id)->service_status,
            'service_status vẫn PHẢI giữ nguyên 1 sau lần bấm bị chặn'
        );
    }

    /**
     * T131b — bằng chứng BẮT BUỘC theo brief: tạo phiếu dùng món X -> gọi xoá món X -> bị chặn
     * (đúng mã lỗi/response shape B1 đang dùng: `responseJson($message, 400)`), và món VẪN CÒN
     * trong DB. Trước khi sửa `MeetingRoomService::usedCount()` (cột `meeting_room_service_id` sai
     * tên), ca này sẽ FAIL vì `usedCount()` ném lỗi SQL "Unknown column" (cột đó không tồn tại
     * trong bảng thật) — đã tự đối chứng bằng cách đọc lại git diff trước khi sửa, không revert
     * code để chạy lại vì rủi ro ảnh hưởng dữ liệu đang dùng chung.
     */
    public function test_xoa_mon_dang_duoc_phieu_dung_bi_chan()
    {
        $catalogServiceId = DB::table('meeting_room_services')->insertGetId([
            'name' => 'PHPUnit Xoa Mon Dang Dung_' . time() . '_' . mt_rand(1000, 9999),
            'unit' => 'ly',
            'sort_order' => 999,
            'status' => MeetingRoomService::STATUS_ACTIVE,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        $this->catalogServiceIdsToCleanup[] = $catalogServiceId;

        $roomId = $this->createTestRoom('DELMON', [self::MANAGER_A_ID]);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $storeRequest = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalogServiceId, 'quantity' => 1, 'note' => null]],
            now()->addDays(37)->setTime(9, 0),
            now()->addDays(37)->setTime(10, 0)
        );
        $booking = app(MeetingRoomBookingService::class)->store($storeRequest);
        $this->bookingIdsToCleanup[] = $booking->id;

        $this->assertSame(
            1,
            DB::table('meeting_room_booking_services')->where('service_id', $catalogServiceId)->count(),
            'Setup: phải có đúng 1 phiếu đang dùng món này trước khi thử xoá'
        );

        $controller = app(MeetingRoomServiceController::class);
        $response = $controller->destroy(MeetingRoomService::findOrFail($catalogServiceId));

        $this->assertSame(400, $response->getStatusCode(), 'Xoá món đang được phiếu dùng PHẢI trả 400 (đúng mã B1 đang dùng)');
        $body = json_decode($response->getContent(), true);
        $this->assertStringContainsString(
            '1 phiếu đặt phòng',
            $body['message'] ?? '',
            'Message phải nêu rõ SỐ phiếu đang dùng. Message thật: ' . json_encode($body, JSON_UNESCAPED_UNICODE)
        );

        $this->assertNotNull(
            MeetingRoomService::find($catalogServiceId),
            'Món dịch vụ đang có phiếu dùng TUYỆT ĐỐI KHÔNG được xoá — đây chính là lỗi im lặng T131b cảnh báo'
        );
    }

    /** Bổ sung (T133, luật 8) — phòng KHÔNG có người phụ trách nào mà gửi services[] -> 422, không tạo phiếu. */
    public function test_phong_khong_nguoi_phu_trach_gui_services_bi_chan_422()
    {
        $roomId = $this->createTestRoom('NOMGR', []);
        $catalog = $this->firstActiveServices(1);

        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');
        $request = $this->buildStoreRequest(
            $roomId,
            [['service_id' => $catalog[0]->id, 'quantity' => 1, 'note' => null]],
            now()->addDays(38)->setTime(9, 0),
            now()->addDays(38)->setTime(10, 0)
        );

        $caught = null;
        try {
            $booking = app(MeetingRoomBookingService::class)->store($request);
            if ($booking) {
                $this->bookingIdsToCleanup[] = $booking->id;
            }
        } catch (\Illuminate\Validation\ValidationException $e) {
            $caught = $e;
        }

        $this->assertNotNull($caught, 'Phòng không có người phụ trách mà gửi services[] PHẢI bị chặn bằng ValidationException (422)');
        $this->assertArrayHasKey('services', $caught->errors(), 'Lỗi phải gắn vào field services để FE hiển thị đúng ô');

        $this->assertSame(
            0,
            DB::table('meeting_room_bookings')->where('meeting_room_id', $roomId)->count(),
            'KHÔNG được tạo phiếu nào khi bị chặn ở bước validate sớm'
        );
    }
}
```

