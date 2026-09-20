# Review package — Task 13 (API phiếu + chống trùng)

### Modules/Meeting/Services/MeetingRoomBookingService.php
```php
<?php

namespace Modules\Meeting\Services;

use Carbon\Carbon;
use Illuminate\Database\Eloquent\Collection as EloquentCollection;
use Illuminate\Database\QueryException;
use Illuminate\Http\Request;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Modules\Meeting\Entities\MeetingRoom;
use Modules\Meeting\Entities\MeetingRoomBooking;
use Modules\Timesheet\Entities\Employee;
use Modules\Timesheet\Entities\GeneralRegulation;
use Modules\Training\Services\BaseService;

/**
 * Plan quan-ly-phong-hop, Task 13 — API tạo/sửa phiếu đặt phòng + chống trùng lịch.
 * PHẦN KHÓ NHẤT của cả feature — xem task-13-brief.md mục "3 cái bẫy" trước khi sửa file này.
 *
 * ⚠️ KHÔNG sửa `Modules\Meeting\Entities\MeetingRoomBooking` /
 * `Modules\Meeting\Entities\MeetingRoomBookingParticipant` — Task 11 đang sửa song song 2 file
 * đó. Mọi thứ ở đây chỉ GỌI method/relation đã có sẵn (`overlaps()`, `statusText()`,
 * `statusColor()`, `isCanEdit()`, `isCanCancel()`, `isCanApprove()`, `isCanReject()`, `room()`,
 * `participants()`, `MeetingRoomBookingParticipant::employee()`).
 */
class MeetingRoomBookingService extends BaseService
{
    public function index(Request $request)
    {
        $query = MeetingRoomBooking::query()->select('meeting_room_bookings.*')->with(['room']);

        if ($request->filled('meeting_room_id')) {
            $query->where('meeting_room_id', $request->meeting_room_id);
        }
        if ($request->filled('company_id')) {
            $query->where('company_id', $request->company_id);
        }
        if ($request->filled('status')) {
            $query->where('status', $request->status);
        }
        if ($request->filled('booked_by')) {
            $query->where('booked_by_employee_id', $request->booked_by);
        }
        if ($request->boolean('only_mine')) {
            $query->where('booked_by_employee_id', auth()->id());
        }
        if ($request->filled('date_from')) {
            $query->where('end_at', '>=', Carbon::parse($request->date_from)->startOfDay());
        }
        if ($request->filled('date_to')) {
            $query->where('start_at', '<=', Carbon::parse($request->date_to)->endOfDay());
        }
        if ($request->filled('updated_after')) {
            $query->where('updated_at', '>', Carbon::parse($request->updated_after));
        }

        return $query->orderBy('start_at', 'desc');
    }

    /** GET chi tiết — eager load đủ để tránh N+1 (participants + phòng + người tạo/cập nhật). */
    public function loadDetail(MeetingRoomBooking $booking)
    {
        $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

        return $this->attachDisplayNames($booking);
    }

    /**
     * Task 13, Bước 3-4 — tạo phiếu. Toàn bộ luật 5.1/5.2 chạy trong 1 transaction:
     *   1. Validate cấu hình/giờ/quá khứ/quá hạn/công ty/trạng thái phòng (spec 5.1).
     *   2. Khóa (`lockForUpdate`) các phiếu Đã duyệt của phòng trong khoảng giờ liên quan rồi mới
     *      quyết định có trùng không (spec 5.2 + bẫy 1 task-13-brief) — SELECT rồi INSERT không
     *      khóa sẽ lọt cả 2 phiếu khi 2 request cách nhau vài trăm ms.
     *   3. Sinh mã trong CÙNG transaction, bắt `QueryException` mã 1062 để sinh lại tối đa 3 lần
     *      (bẫy 2 task-13-brief) — `code` đã có `unique`, khuôn `max('id')+1` kiểu cũ của dự án
     *      (`BomList::getNextCode()`) sẽ nổ 500 khi 2 request song song sinh trùng mã.
     */
    public function store(Request $request)
    {
        return DB::transaction(function () use ($request) {
            $room = MeetingRoom::findOrFail($request->meeting_room_id);
            $startAt = Carbon::parse($request->start_at);
            $endAt = Carbon::parse($request->end_at);
            $bookerCompanyId = optional(auth()->user()->info)->company_id;

            $warnings = $this->validateBookingRules($room, $startAt, $endAt, $request->attendee_count, $bookerCompanyId);

            // Bẫy 1 (task-13-brief) — khóa TRƯỚC KHI insert, không phải SELECT rời rạc.
            $this->assertNoOverlap($room->id, $startAt, $endAt);

            $status = (int) $room->require_approval === 1
                ? MeetingRoomBooking::STATUS_CHO_DUYET
                : MeetingRoomBooking::STATUS_DA_DUYET;

            $data = [
                'meeting_room_id' => $room->id,
                'title' => $request->title,
                'content' => $request->content,
                'start_at' => $startAt,
                'end_at' => $endAt,
                'status' => $status,
                'booked_by_employee_id' => auth()->id(),
                'host_employee_id' => $request->host_employee_id,
                'attendee_count' => $request->attendee_count,
                'source' => MeetingRoomBooking::SOURCE_TU_DAT,
            ];
            // company_id/department_id KHÔNG set ở đây — để hook `BaseModel::creating()` tự điền
            // theo NGƯỜI ĐANG ĐĂNG NHẬP (= người đặt), đúng spec 4.4 "company_id của người đặt".

            $booking = $this->createWithUniqueCode($data);

            $this->syncParticipants($booking, $request->input('participant_ids'));

            $booking->warnings = $warnings;

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Task 13, Bước 6 — sửa phiếu.
     * - Khóa (423) kiểm NGAY ĐẦU HÀM, trước cả validate nghiệp vụ (quy ước CLAUDE.md bản ghi khóa).
     * - Chỉ NGƯỜI ĐẶT sửa được phiếu của mình (spec 5.4) -> không phải người đặt: 403.
     * - Đổi giờ/phòng -> chạy lại toàn bộ 5.1/5.2; phòng cần duyệt thì phiếu quay về Chờ duyệt.
     */
    public function update(MeetingRoomBooking $booking, Request $request)
    {
        return DB::transaction(function () use ($booking, $request) {
            // Khóa dòng hiện tại trước khi đọc/so sánh — 1 request khác (approve/cancel) không
            // được xen vào giữa lúc ta đang kiểm tra + ghi đè.
            $booking = MeetingRoomBooking::where('id', $booking->id)->lockForUpdate()->firstOrFail();

            // "Đã tới giờ" = khóa, bất kể ai gọi — kiểm trước tiên (đúng quy ước CLAUDE.md: kiểm
            // trạng thái khóa NGAY ĐẦU HÀM, trước cả validate nghiệp vụ khác).
            if (Carbon::now()->gte(Carbon::parse($booking->start_at))) {
                throw new \Exception('Phiếu đã tới giờ bắt đầu, không thể sửa nữa', 423);
            }

            if (!in_array((int) $booking->status, [MeetingRoomBooking::STATUS_CHO_DUYET, MeetingRoomBooking::STATUS_DA_DUYET], true)) {
                throw new \Exception('Phiếu không ở trạng thái có thể sửa', 423);
            }

            if ((int) $booking->booked_by_employee_id !== (int) auth()->id()) {
                throw new \Exception('Bạn không có quyền sửa phiếu này', 403);
            }

            $room = MeetingRoom::findOrFail($request->meeting_room_id);
            $startAt = Carbon::parse($request->start_at);
            $endAt = Carbon::parse($request->end_at);
            $bookerCompanyId = optional(auth()->user()->info)->company_id;
            $attendeeCount = $request->attendee_count ?? $booking->attendee_count;

            $warnings = $this->validateBookingRules($room, $startAt, $endAt, $attendeeCount, $bookerCompanyId);

            $timeOrRoomChanged = ((int) $room->id !== (int) $booking->meeting_room_id)
                || !$startAt->eq(Carbon::parse($booking->start_at))
                || !$endAt->eq(Carbon::parse($booking->end_at));

            // Luôn loại chính phiếu đang sửa khỏi kiểm tra trùng — kể cả khi giờ/phòng không đổi,
            // chạy lại vẫn an toàn (idempotent) và rẻ hơn nhiều so với if rẽ nhánh dễ sai.
            $this->assertNoOverlap($room->id, $startAt, $endAt, $booking->id);

            $booking->meeting_room_id = $room->id;
            $booking->title = $request->title;
            $booking->content = $request->content;
            $booking->start_at = $startAt;
            $booking->end_at = $endAt;
            $booking->host_employee_id = $request->host_employee_id;
            $booking->attendee_count = $request->attendee_count;

            if ($timeOrRoomChanged) {
                $booking->status = (int) $room->require_approval === 1
                    ? MeetingRoomBooking::STATUS_CHO_DUYET
                    : MeetingRoomBooking::STATUS_DA_DUYET;
            }

            $booking->save();

            $this->syncParticipants($booking, $request->input('participant_ids'));

            $booking->warnings = $warnings;

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Spec 5.1 — toàn bộ kiểm tra tĩnh khi lưu (không tính trùng lịch, xem `assertNoOverlap`).
     * Trả về mảng cảnh báo (không chặn) — hiện tại chỉ có "vượt sức chứa" (mục 7).
     *
     * @throws ValidationException
     */
    private function validateBookingRules(MeetingRoom $room, Carbon $startAt, Carbon $endAt, $attendeeCount, $bookerCompanyId)
    {
        $warnings = [];

        // Mục 3: không đặt cho thời điểm đã qua.
        if ($startAt->lt(Carbon::now())) {
            throw ValidationException::withMessages([
                'start_at' => 'Không thể đặt phòng cho thời điểm đã qua',
            ]);
        }

        // Mục 5: phòng phải đang Hoạt động.
        if ((int) $room->status !== MeetingRoom::STATUS_ACTIVE) {
            throw ValidationException::withMessages([
                'meeting_room_id' => 'Phòng họp hiện không hoạt động',
            ]);
        }

        // Mục 6: khác công ty thì phòng phải cho phép đặt chéo công ty.
        if (!MeetingRoom::canBeBookedByCompany($room->company_id, $room->allow_cross_company, $bookerCompanyId)) {
            throw ValidationException::withMessages([
                'meeting_room_id' => 'Phòng họp này không cho phép đặt khác công ty',
            ]);
        }

        // Cấu hình theo công ty CỦA PHÒNG (phòng thuộc công ty nào thì áp giờ mở/đóng + hạn đặt
        // trước của công ty đó) — fallback hệ thống nếu công ty chưa khai ở general_regulations.
        $regulation = $room->company_id ? GeneralRegulation::where('company_id', $room->company_id)->first() : null;

        // Mục 4: không vượt quá hạn đặt trước.
        $maxAdvanceDays = (int) MeetingRoom::resolveConfig(null, optional($regulation)->meeting_room_max_advance_days, 90);
        if ($startAt->gt(Carbon::now()->addDays($maxAdvanceDays))) {
            throw ValidationException::withMessages([
                'start_at' => "Chỉ được đặt phòng trước tối đa {$maxAdvanceDays} ngày",
            ]);
        }

        // Mục 2: giờ mở/đóng cửa CHỈ áp dụng khi phiếu gọn trong 1 ngày; qua đêm thì bỏ kiểm giờ
        // mở cửa nhưng chặn quá 72 giờ (dùng diffInMinutes, KHÔNG diffInHours — diffInHours cắt
        // phần thập phân nên phiếu 72h30' có thể lọt qua nếu so bằng số giờ nguyên).
        if ($startAt->isSameDay($endAt)) {
            $openTime = $room->effectiveOpenTime(optional($regulation)->meeting_room_open_time);
            $closeTime = $room->effectiveCloseTime(optional($regulation)->meeting_room_close_time);
            $dayStr = $startAt->format('Y-m-d');
            $openAt = Carbon::parse($dayStr . ' ' . $openTime);
            $closeAt = Carbon::parse($dayStr . ' ' . $closeTime);

            if ($startAt->lt($openAt) || $endAt->gt($closeAt)) {
                throw ValidationException::withMessages([
                    'start_at' => "Khoảng giờ đặt phải nằm trong giờ mở cửa của phòng ({$openTime} - {$closeTime})",
                ]);
            }
        } else {
            if ($startAt->diffInMinutes($endAt) > 72 * 60) {
                throw ValidationException::withMessages([
                    'end_at' => 'Phiếu đặt qua đêm không được vượt quá 72 giờ',
                ]);
            }
        }

        // Mục 7: vượt sức chứa -> CẢNH BÁO, không chặn, không tự sửa số user đã nhập.
        if ($attendeeCount && $room->capacity && (int) $attendeeCount > (int) $room->capacity) {
            $warnings[] = "Số người dự kiến ({$attendeeCount}) vượt sức chứa phòng ({$room->capacity} người)";
        }

        return $warnings;
    }

    /**
     * Spec 5.2 + bẫy 1 (task-13-brief) — kiểm trùng có khóa hàng.
     * Chỉ so với phiếu ĐÃ DUYỆT (dù phòng đang tạo có cần duyệt hay không): phiếu Chờ duyệt được
     * phép trùng nhau tự do, nhưng KHÔNG ai đặt đè được lên phiếu Đã duyệt, kể cả xin duyệt.
     *
     * `lockForUpdate()` trên đúng phạm vi `(meeting_room_id, start_at, end_at)` — index bắt buộc
     * của spec 4.4 — khiến InnoDB giữ gap lock trên khoảng đang quét dù kết quả rỗng, nên request
     * thứ 2 nhắm CÙNG phòng + giờ giao nhau phải CHỜ request thứ 1 commit/rollback xong mới được
     * đọc tiếp (current read), không phải đọc snapshot cũ — đây là lý do cách này chặn được cả
     * tình huống "chưa có dòng nào để khóa" chứ không chỉ khóa dòng đã tồn tại.
     *
     * @throws ValidationException
     */
    private function assertNoOverlap($roomId, Carbon $startAt, Carbon $endAt, $excludeBookingId = null)
    {
        $query = MeetingRoomBooking::where('meeting_room_id', $roomId)
            ->where('status', MeetingRoomBooking::STATUS_DA_DUYET)
            ->where('start_at', '<', $endAt)
            ->where('end_at', '>', $startAt);

        if ($excludeBookingId) {
            $query->where('id', '!=', $excludeBookingId);
        }

        $conflict = $query->lockForUpdate()->first();

        if ($conflict) {
            throw ValidationException::withMessages([
                'start_at' => sprintf(
                    'Phòng đã có cuộc họp "%s" lúc %s - %s ngày %s',
                    $conflict->title,
                    Carbon::parse($conflict->start_at)->format('H:i'),
                    Carbon::parse($conflict->end_at)->format('H:i'),
                    Carbon::parse($conflict->start_at)->format('d/m/Y')
                ),
            ]);
        }
    }

    /**
     * Bẫy 2 (task-13-brief) — sinh mã `DPH-YYYY-NNNNN` an toàn TRONG transaction đang mở.
     * Khuôn cũ của dự án (`BomList::getNextCode()`, `max('id')+1`) sẽ 500 khi 2 request song song
     * sinh trùng mã vì `code` đã có `unique`. Ở đây bắt riêng lỗi trùng khóa (SQLSTATE 23000,
     * driver error 1062) rồi SINH LẠI — không rethrow raw QueryException ra ngoài thành 500 vô
     * nghĩa — tối đa 3 lần thử; hết lượt vẫn trùng thì mới để lỗi thật lộ ra.
     */
    private function createWithUniqueCode(array $data)
    {
        $lastException = null;

        for ($attempt = 0; $attempt < 3; $attempt++) {
            $data['code'] = $this->nextCode($attempt);

            try {
                return MeetingRoomBooking::create($data);
            } catch (QueryException $e) {
                if (!$this->isDuplicateCodeError($e)) {
                    throw $e;
                }
                $lastException = $e;
            }
        }

        throw $lastException;
    }

    private function isDuplicateCodeError(QueryException $e)
    {
        // Laravel/PDO: SQLSTATE 23000 = integrity constraint violation; driver error 1062 của
        // MySQL nằm trong message dạng "SQLSTATE[23000]: ... 1062 Duplicate entry ... 'code'".
        // errorInfo[1] (driver-specific code) là cách kiểm chính xác nhất khi PDO expose được.
        $errorInfo = $e->errorInfo ?? null;
        if (is_array($errorInfo) && isset($errorInfo[1]) && (int) $errorInfo[1] === 1062) {
            return true;
        }

        return $e->getCode() == 23000 && strpos($e->getMessage(), '1062') !== false;
    }

    private function nextCode($attemptOffset = 0)
    {
        $maxId = (int) (MeetingRoomBooking::max('id') ?? 0);

        return 'DPH-' . date('Y') . '-' . str_pad($maxId + 1 + $attemptOffset, 5, '0', STR_PAD_LEFT);
    }

    /**
     * `participant_ids === null` (key không có trong payload) -> GIỮ NGUYÊN danh sách hiện có,
     * không xóa sạch. Truyền mảng (kể cả rỗng `[]`) -> đồng bộ lại đúng mảng đó.
     */
    private function syncParticipants(MeetingRoomBooking $booking, $participantIds)
    {
        if ($participantIds === null) {
            return;
        }

        $participantIds = array_values(array_unique(array_filter((array) $participantIds)));

        $booking->participants()->delete();
        foreach ($participantIds as $employeeId) {
            $booking->participants()->create(['employee_id' => $employeeId]);
        }
    }

    /**
     * Gắn tên hiển thị cho các cột trỏ `employees.id` mà `MeetingRoomBooking` KHÔNG có relation
     * riêng (`booked_by_employee_id`, `host_employee_id`, `approved_by`, `cancelled_by`) — entity
     * đang bị khóa sửa bởi Task 11 nên KHÔNG thêm relation mới vào đó. Batch 1 query duy nhất
     * (kể cả khi gọi cho cả trang danh sách) để không N+1, gán thẳng vào từng model bằng thuộc
     * tính động (khuôn giống `used_booking_count` ở `MeetingRoomController::index()`).
     *
     * @param MeetingRoomBooking|EloquentCollection|Collection $bookings
     * @return mixed cùng kiểu truyền vào
     */
    public function attachDisplayNames($bookings)
    {
        $collection = $bookings instanceof EloquentCollection || $bookings instanceof Collection
            ? $bookings
            : collect([$bookings]);

        $employeeIds = $collection
            ->flatMap(function ($b) {
                return [$b->booked_by_employee_id, $b->host_employee_id, $b->approved_by, $b->cancelled_by];
            })
            ->filter()
            ->unique()
            ->values()
            ->all();

        $employees = empty($employeeIds)
            ? collect()
            : Employee::with('info')->whereIn('id', $employeeIds)->get()->keyBy('id');

        foreach ($collection as $booking) {
            $booking->booked_by_name = optional($employees->get($booking->booked_by_employee_id))->fullname;
            $booking->host_employee_name = $booking->host_employee_id
                ? optional($employees->get($booking->host_employee_id))->fullname
                : null;
            $booking->approved_by_name = $booking->approved_by
                ? optional($employees->get($booking->approved_by))->fullname
                : null;
            $booking->cancelled_by_name = $booking->cancelled_by
                ? optional($employees->get($booking->cancelled_by))->fullname
                : null;
        }

        return $bookings;
    }
}
```

### Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomBookingController.php
```php
<?php

namespace Modules\Meeting\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Log;
use Illuminate\Validation\ValidationException;
use Modules\Meeting\Entities\MeetingRoomBooking;
use Modules\Meeting\Http\Requests\MeetingRoomBooking\MeetingRoomBookingRequest;
use Modules\Meeting\Services\MeetingRoomBookingService;
use Modules\Meeting\Transformers\MeetingRoomBooking\DetailMeetingRoomBookingResource;
use Modules\Meeting\Transformers\MeetingRoomBooking\MeetingRoomBookingResource;

/**
 * Plan quan-ly-phong-hop, Task 13 — API tạo/sửa phiếu đặt phòng + chống trùng lịch.
 *
 * `store()` KHÔNG gắn `checkPermission` (xem `Routes/api.php`) — quyết định #8 của spec: mọi
 * nhân viên đều tự đặt phòng được, không cần quyền riêng.
 */
class MeetingRoomBookingController extends ApiController
{
    private $meetingRoomBookingService;

    public function __construct(MeetingRoomBookingService $meetingRoomBookingService)
    {
        $this->meetingRoomBookingService = $meetingRoomBookingService;
    }

    public function index(Request $request)
    {
        $query = $this->meetingRoomBookingService->index($request);
        $paginated = $query->paginate($request->per_page ?? 20)->appends($request->query());

        // Tránh N+1: gắn tên người đặt/chủ trì cho CẢ TRANG bằng 1 query (xem
        // MeetingRoomBookingService::attachDisplayNames()), không gọi lẻ từng dòng.
        $this->meetingRoomBookingService->attachDisplayNames(collect($paginated->items()));

        $result = MeetingRoomBookingResource::collection($paginated)->response()->getData();

        return $this->apiGetList($result, []);
    }

    public function show(MeetingRoomBooking $meetingRoomBooking)
    {
        $booking = $this->meetingRoomBookingService->loadDetail($meetingRoomBooking);

        return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
    }

    public function store(MeetingRoomBookingRequest $request)
    {
        try {
            $booking = $this->meetingRoomBookingService->store($request);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (ValidationException $e) {
            // Lỗi validate (trùng lịch, quá khứ, ngoài giờ mở cửa…) phải giữ nguyên để FE map
            // vào từng ô nhập — catch chung Exception bên dưới sẽ nuốt mất field lỗi.
            throw $e;
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    public function update(MeetingRoomBookingRequest $request, MeetingRoomBooking $meetingRoomBooking)
    {
        try {
            $booking = $this->meetingRoomBookingService->update($meetingRoomBooking, $request);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (ValidationException $e) {
            throw $e;
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }
}
```

### Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoomBooking;

use Modules\Training\Http\Requests\BaseRequest;

/**
 * Plan quan-ly-phong-hop, Task 13 — validate cấu trúc payload tạo/sửa phiếu đặt phòng.
 *
 * Chỉ validate PHẦN CẤU TRÚC ở đây (kiểu dữ liệu, bắt buộc, `end_at > start_at`). Toàn bộ luật
 * NGHIỆP VỤ phụ thuộc dữ liệu (giờ mở cửa phòng, quá khứ, quá hạn đặt trước, khác công ty, TRÙNG
 * LỊCH…) chạy ở `MeetingRoomBookingService` bên trong transaction có `lockForUpdate` — không làm
 * được ở tầng FormRequest vì cần đọc + khoá bản ghi khác trong cùng 1 transaction (spec 5.1/5.2).
 *
 * Dùng CHUNG cho cả tạo (POST) và sửa (PUT) — không có ô nào chỉ áp dụng cho 1 trong 2 luồng.
 */
class MeetingRoomBookingRequest extends BaseRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'meeting_room_id' => ['required', 'integer', 'exists:meeting_rooms,id'],
            'title' => ['required', 'string', 'max:255'],
            'content' => ['nullable', 'string'],
            'start_at' => ['required', 'date'],
            // `after:start_at` bao luôn kiểm "end_at > start_at" của spec 5.1 mục 1 — Laravel tự
            // trả 422 gắn field `end_at` qua BaseRequest::failedValidation() nếu vi phạm.
            'end_at' => ['required', 'date', 'after:start_at'],
            'host_employee_id' => ['nullable', 'integer'],
            // Spec 5.1 mục 7: vượt sức chứa chỉ CẢNH BÁO, không chặn -> không đặt rule so capacity
            // ở đây, việc này Service tự tính rồi trả `warnings`, KHÔNG được sửa số user đã nhập.
            'attendee_count' => ['nullable', 'integer', 'min:1'],
            'participant_ids' => ['nullable', 'array'],
            'participant_ids.*' => ['integer'],
        ];
    }

    /**
     * Get custom messages for validator errors.
     *
     * @return array
     */
    public function messages()
    {
        return [
            'meeting_room_id.required' => 'Vui lòng chọn phòng họp',
            'meeting_room_id.integer' => 'Phòng họp không hợp lệ',
            'meeting_room_id.exists' => 'Phòng họp không tồn tại',
            'title.required' => 'Vui lòng nhập tiêu đề cuộc họp',
            'title.max' => 'Tiêu đề tối đa 255 ký tự',
            'start_at.required' => 'Vui lòng chọn giờ bắt đầu',
            'start_at.date' => 'Giờ bắt đầu không hợp lệ',
            'end_at.required' => 'Vui lòng chọn giờ kết thúc',
            'end_at.date' => 'Giờ kết thúc không hợp lệ',
            'end_at.after' => 'Giờ kết thúc phải sau giờ bắt đầu',
            'host_employee_id.integer' => 'Chủ trì không hợp lệ',
            'attendee_count.integer' => 'Số người dự kiến phải là số nguyên',
            'attendee_count.min' => 'Số người dự kiến tối thiểu là 1',
            'participant_ids.array' => 'Danh sách người tham dự không hợp lệ',
            'participant_ids.*.integer' => 'Người tham dự không hợp lệ',
        ];
    }
}
```

### Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoomBooking;

use Carbon\Carbon;
use Modules\Human\Transformers\ApiResource;
use Modules\Meeting\Entities\MeetingRoomBooking;

/**
 * Plan quan-ly-phong-hop, Task 13 — 1 dòng trong màn danh sách / lưới phiếu đặt phòng.
 *
 * Quy ước payload spec 6.4 (dùng chung web + app mobile, để app không phải chép lại luật):
 * - Cờ hành động BE tính sẵn (`is_can_*`) — client CHỈ đọc, không tự suy luận lại.
 * - Thời gian trả ISO-8601 CÓ OFFSET (`+07:00`) kèm `*_text` cho người đọc.
 * - Trạng thái trả đủ `status` + `status_text` + `status_color`, client không tự map.
 *
 * List GỌN — KHÔNG nhồi participants (spec 6.4 "Payload list gọn"), chỉ Detail resource mới có.
 */
class MeetingRoomBookingResource extends ApiResource
{
    public function toArray($request): array
    {
        $isOwner = (int) $this->booked_by_employee_id === (int) auth()->id();
        $isRoomManager = optional($this->room)->manager_employee_id
            && (int) $this->room->manager_employee_id === (int) auth()->id();
        $hasApprovePermission = isCurrentEmployeeHasPermission('Duyệt phiếu đặt phòng họp');
        $canActOnApproval = $isRoomManager || $hasApprovePermission;

        return [
            'id' => $this->id,
            'code' => $this->code,
            'title' => $this->title,
            'meeting_room_id' => $this->meeting_room_id,
            'room_name' => optional($this->room)->name,
            'start_at' => self::isoDateTime($this->start_at),
            'start_at_text' => self::readableDateTime($this->start_at),
            'end_at' => self::isoDateTime($this->end_at),
            'end_at_text' => self::readableDateTime($this->end_at),
            'status' => (int) $this->status,
            'status_text' => MeetingRoomBooking::statusText($this->status),
            'status_color' => MeetingRoomBooking::statusColor($this->status),
            'booked_by_employee_id' => $this->booked_by_employee_id,
            'booked_by_name' => $this->booked_by_name,
            'host_employee_id' => $this->host_employee_id,
            'host_employee_name' => $this->host_employee_name,
            'attendee_count' => $this->attendee_count,
            'source' => (int) $this->source,
            'is_can_edit' => $this->isCanEdit() && $isOwner,
            'is_can_cancel' => $this->isCanCancel() && ($isOwner || $canActOnApproval),
            'is_can_approve' => $this->isCanApprove() && $canActOnApproval,
            'is_can_reject' => $this->isCanReject() && $canActOnApproval,
            'created_at' => self::isoDateTime($this->created_at),
        ];
    }

    public static function isoDateTime($value)
    {
        return $value ? Carbon::parse($value)->format('Y-m-d\TH:i:sP') : null;
    }

    public static function readableDateTime($value)
    {
        return $value ? Carbon::parse($value)->format('H:i d/m/Y') : null;
    }
}
```

### Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoomBooking;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;
use Modules\Meeting\Entities\MeetingRoomBooking;

/**
 * Plan quan-ly-phong-hop, Task 13 — chi tiết 1 phiếu đặt phòng (popup Xem/Sửa, và cũng dùng làm
 * response của tạo mới/cập nhật để FE có ngay cờ hành động + `warnings` mà không phải gọi lại).
 */
class DetailMeetingRoomBookingResource extends ApiResource
{
    public function toArray($request): array
    {
        $isOwner = (int) $this->booked_by_employee_id === (int) auth()->id();
        $isRoomManager = optional($this->room)->manager_employee_id
            && (int) $this->room->manager_employee_id === (int) auth()->id();
        $hasApprovePermission = isCurrentEmployeeHasPermission('Duyệt phiếu đặt phòng họp');
        $canActOnApproval = $isRoomManager || $hasApprovePermission;

        return [
            'id' => $this->id,
            'code' => $this->code,
            'title' => $this->title,
            'content' => $this->content,
            'meeting_room_id' => $this->meeting_room_id,
            'room_name' => optional($this->room)->name,
            'start_at' => MeetingRoomBookingResource::isoDateTime($this->start_at),
            'start_at_text' => MeetingRoomBookingResource::readableDateTime($this->start_at),
            'end_at' => MeetingRoomBookingResource::isoDateTime($this->end_at),
            'end_at_text' => MeetingRoomBookingResource::readableDateTime($this->end_at),
            'status' => (int) $this->status,
            'status_text' => MeetingRoomBooking::statusText($this->status),
            'status_color' => MeetingRoomBooking::statusColor($this->status),
            'booked_by_employee_id' => $this->booked_by_employee_id,
            'booked_by_name' => $this->booked_by_name,
            'host_employee_id' => $this->host_employee_id,
            'host_employee_name' => $this->host_employee_name,
            'attendee_count' => $this->attendee_count,
            'company_id' => $this->company_id,
            'department_id' => $this->department_id,
            'source' => (int) $this->source,
            'meeting_id' => $this->meeting_id,
            'approved_by' => $this->approved_by,
            'approved_by_name' => $this->approved_by_name,
            'approved_at' => MeetingRoomBookingResource::isoDateTime($this->approved_at),
            'reject_reason' => $this->reject_reason,
            'is_auto_rejected' => (bool) $this->is_auto_rejected,
            'cancelled_by' => $this->cancelled_by,
            'cancelled_by_name' => $this->cancelled_by_name,
            'cancelled_at' => MeetingRoomBookingResource::isoDateTime($this->cancelled_at),
            'cancel_reason' => $this->cancel_reason,
            'checkin_at' => MeetingRoomBookingResource::isoDateTime($this->checkin_at),
            'checkout_at' => MeetingRoomBookingResource::isoDateTime($this->checkout_at),
            'participants' => $this->whenLoaded('participants', function () {
                return $this->participants->map(function ($participant) {
                    return [
                        'employee_id' => $participant->employee_id,
                        'employee_name' => optional($participant->employee)->fullname,
                    ];
                });
            }),
            // Cảnh báo KHÔNG CHẶN (spec 5.1 mục 7, vd vượt sức chứa) — chỉ có ngay sau lần
            // tạo/sửa vừa gọi trong request này (Service gán bằng thuộc tính động), GET lại sau
            // đó không còn vì nó không phải dữ liệu lưu DB, chỉ là phản hồi tức thời của thao tác.
            'warnings' => $this->warnings ?? [],
            'created_at' => Helper::formatDateTime($this->created_at),
            'updated_at' => Helper::formatDateTime($this->updated_at),
            'created_by_name' => $this->employee_create_name,
            'updated_by_name' => $this->employee_update_name,
            'is_can_edit' => $this->isCanEdit() && $isOwner,
            'is_can_cancel' => $this->isCanCancel() && ($isOwner || $canActOnApproval),
            'is_can_approve' => $this->isCanApprove() && $canActOnApproval,
            'is_can_reject' => $this->isCanReject() && $canActOnApproval,
        ];
    }
}
```

### Modules/Meeting/Routes/api.php
```php
<?php

use Illuminate\Support\Facades\Route;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomAmenityController;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomBookingController;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomController;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Plan quan-ly-phong-hop, Task 5 — Danh mục "Tiện nghi phòng họp"
    Route::group(['prefix' => 'meeting/room-amenities'], function () {
        Route::get('/', [MeetingRoomAmenityController::class, 'index'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp');
        Route::post('/', [MeetingRoomAmenityController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        // Fix đợt review tổng, mục D: thiếu checkPermission trong khi route song sinh của phòng
        // họp (`show` bên dưới, khối "Phòng họp") đã gắn từ đầu — lệch gate giữa 2 danh mục cùng
        // khuôn thiết kế.
        Route::get('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'show'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp');
        Route::delete('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        Route::get('/{meetingRoomAmenity}/lock', [MeetingRoomAmenityController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        Route::get('/{meetingRoomAmenity}/unlock', [MeetingRoomAmenityController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    });

    // Plan quan-ly-phong-hop, Task 6 — Danh mục "Phòng họp"
    Route::group(['prefix' => 'meeting/rooms'], function () {
        // Route tĩnh (/form-options) PHẢI đặt TRƯỚC wildcard /{meetingRoom}, nếu không bị nuốt.
        // Fix vòng 2: thiếu checkPermission trong khi mọi route đọc khác của phân hệ đều đã gate.
        Route::get('/form-options', [MeetingRoomController::class, 'formOptions'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::get('/', [MeetingRoomController::class, 'index'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::post('/', [MeetingRoomController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}', [MeetingRoomController::class, 'show'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::delete('/{meetingRoom}', [MeetingRoomController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/lock', [MeetingRoomController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/unlock', [MeetingRoomController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/upcoming-bookings', [MeetingRoomController::class, 'upcomingBookings'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
    });

    // Plan quan-ly-phong-hop, Task 13 — Phiếu đặt phòng họp (tạo/sửa + chống trùng lịch).
    // `store` (POST) KHÔNG gắn checkPermission — quyết định #8: mọi nhân viên đều đặt phòng
    // được. `index`/`show` cũng chưa gắn quyền 1579 (Xem tất cả phiếu đặt phòng họp) — "luật nhìn
    // thấy phiếu" theo permission là việc của Task 14 (xem task-12 bước 4 trong plan.md).
    Route::group(['prefix' => 'meeting/room-bookings'], function () {
        Route::get('/', [MeetingRoomBookingController::class, 'index']);
        Route::post('/', [MeetingRoomBookingController::class, 'store']);
        Route::get('/{meetingRoomBooking}', [MeetingRoomBookingController::class, 'show']);
        Route::put('/{meetingRoomBooking}', [MeetingRoomBookingController::class, 'update']);
    });
});
```

### e2e/tests/meeting/meeting-room-booking.api.spec.ts
```ts
/**
 * E2E API — "Phiếu đặt phòng họp" (Task 13, plan quan-ly-phong-hop) — tạo/sửa + chống trùng lịch.
 * PHẦN KHÓ NHẤT của cả feature (task-13-brief.md).
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): API ở :8001.
 * Token admin đọc từ e2e/.auth/api-wt.json (employee id 34, company_id 1).
 * Token không quyền: e2e/.auth/user-nocost-wt.json (employee id 25, company_id 1) — dùng để test
 * "sửa phiếu không phải của mình" (403), KHÔNG liên quan quyền checkPermission (route store/update
 * không gắn checkPermission — quyết định #8: mọi nhân viên đặt phòng được).
 *
 * Máy chạy test cùng múi giờ server (Asia/Ho_Chi_Minh, xác nhận bằng `date` lúc viết spec) nên
 * dùng thẳng giờ local của Date, KHÔNG cần quy đổi UTC.
 *
 * Phủ theo ĐỊNH NGHĨA HOÀN THÀNH của task-13-brief.md:
 *   Nhóm A — validate tĩnh (spec 5.1): quá khứ, quá hạn đặt trước, ngoài giờ mở cửa (gọn 1 ngày),
 *            qua đêm >72h, phòng khoá, khác công ty (chặn/cho phép), vượt sức chứa CHỈ CẢNH BÁO.
 *   Nhóm B — chống trùng (spec 5.2): chặn khi trùng phiếu Đã duyệt (dù phòng không cần duyệt hay
 *            có phiếu Đã duyệt "cắm sẵn" trên phòng cần duyệt), cho phép nhiều phiếu Chờ duyệt
 *            trùng giờ trên phòng cần duyệt.
 *   Nhóm C — CA NGHIỆM THU: 2 request song song trùng giờ -> đúng 1 200 + 1 422, DB chỉ có 1 phiếu,
 *            không có request nào 500 (bẫy 1 + bẫy 2 task-13-brief).
 *   Nhóm D — sửa phiếu (spec 5.4): chủ sở hữu sửa được trước giờ họp, đổi giờ/phòng chạy lại toàn
 *            bộ kiểm tra + quay lại Chờ duyệt nếu phòng cần duyệt; không phải chủ -> 403; đã tới
 *            giờ họp -> 423 (không phải 422).
 *   Nhóm E — Resource: mã `DPH-YYYY-NNNNN`, cờ is_can_*, ISO-8601 có offset kèm *_text,
 *            status/status_text/status_color, participants ở detail.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import { execFileSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const ROOMS_URL = '/api/v1/meeting/rooms';
const BOOKINGS_URL = '/api/v1/meeting/room-bookings';

// runMysql()/readEnvValue() — khuôn copy nguyên văn từ meeting-room.spec.ts / room-amenity.api.spec.ts.
// Mặc định trỏ THẲNG vào worktree (nơi API :8001 đang chạy), override bằng API_REPO khi cần.
const WORKTREE_API_REPO =
  process.env.API_REPO || '/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api';

function readEnvValue(key: string): string {
  const envContent = fs.readFileSync(path.join(WORKTREE_API_REPO, '.env'), 'utf8');
  const match = envContent.match(new RegExp(`^${key}=(.*)$`, 'm'));
  return match ? match[1].trim() : '';
}

function runMysql(sql: string): string {
  const dbHost = readEnvValue('DB_HOST') || '127.0.0.1';
  const dbDatabase = readEnvValue('DB_DATABASE') || 'hrm_erp';
  const dbPassword = readEnvValue('DB_PASSWORD');
  const candidates = [
    'mysql',
    '/opt/homebrew/opt/mysql@8.0/bin/mysql',
    '/usr/local/bin/mysql',
    '/usr/local/mysql/bin/mysql',
  ];
  let lastErr: any;
  for (const bin of candidates) {
    try {
      return execFileSync(bin, ['-h', dbHost, '-uroot', dbDatabase, '-N', '-e', sql], {
        env: { ...process.env, MYSQL_PWD: dbPassword },
        encoding: 'utf8',
      });
    } catch (e: any) {
      lastErr = e;
      if (e.code !== 'ENOENT') throw e;
    }
  }
  throw lastErr;
}

function countBookingsForRoom(roomId: number): number {
  const out = runMysql(`SELECT COUNT(*) FROM meeting_room_bookings WHERE meeting_room_id=${roomId};`);
  return Number(out.trim());
}

/** `YYYY-MM-DD HH:mm:ss` giờ LOCAL (không quy đổi UTC) — Carbon::parse() ở BE hiểu thẳng chuỗi này
 *  theo timezone app (`Asia/Ho_Chi_Minh`, đã xác nhận trùng giờ máy chạy test). */
function fmt(d: Date): string {
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function addDays(base: Date, days: number): Date {
  return new Date(base.getTime() + days * 24 * 60 * 60 * 1000);
}

function addHours(base: Date, hours: number): Date {
  return new Date(base.getTime() + hours * 60 * 60 * 1000);
}

/** 09:00 ngày mai — chắc chắn trong giờ mở cửa mặc định (07:00-20:00) và chưa quá khứ. */
function tomorrow9am(): Date {
  const d = addDays(new Date(), 1);
  d.setHours(9, 0, 0, 0);
  return d;
}

const RUN_SUFFIX = Date.now();
const CODE_ROOM_NO_APPROVAL = `E2E_BK_NOAPPR_${RUN_SUFFIX}`;
const CODE_ROOM_REQUIRE_APPROVAL = `E2E_BK_APPR_${RUN_SUFFIX}`;
const CODE_ROOM_CROSS_DENIED = `E2E_BK_CROSSDENY_${RUN_SUFFIX}`;
const CODE_ROOM_CROSS_ALLOWED = `E2E_BK_CROSSOK_${RUN_SUFFIX}`;
const CODE_ROOM_INACTIVE = `E2E_BK_INACTIVE_${RUN_SUFFIX}`;
const CODE_ROOM_PARALLEL = `E2E_BK_PARALLEL_${RUN_SUFFIX}`;
const CODE_ROOM_CAPACITY = `E2E_BK_CAP_${RUN_SUFFIX}`;

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let noPermApi: APIRequestContext;
const createdRoomIds: number[] = [];
const createdBookingIds: number[] = [];

/** Dọn rác `code LIKE 'E2E_%'` còn sót từ lần chạy trước bị kill giữa chừng — phòng trước
 *  (bookings tham chiếu meeting_room_id nên phải xoá booking trước phòng), rồi mới phòng. */
async function cleanupLeftoverE2eData() {
  try {
    runMysql(`DELETE b FROM meeting_room_bookings b
      INNER JOIN meeting_rooms r ON r.id = b.meeting_room_id
      WHERE r.code LIKE 'E2E_%';`);
  } catch (e) {
    // best-effort — không chặn beforeAll nếu mysql cli không sẵn sàng, ca dọn cuối vẫn còn afterAll.
  }

  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${ROOMS_URL}?keyword=E2E_&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const leftoverIds = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith('E2E_'))
      .map((r: any) => r.id);
    if (leftoverIds.length === 0) break;
    for (const id of leftoverIds) {
      await api.delete(`${ROOMS_URL}/${id}`).catch(() => {});
    }
  }
}

test.beforeAll(async () => {
  const adminToken = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
  api = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${adminToken}` },
  });

  const nocostState = JSON.parse(fs.readFileSync(NOCOST_STATE_FILE, 'utf8'));
  const nocostToken = nocostState.origins[0].localStorage.find((i: any) => i.name === 'access_token').value;
  noPermApi = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${nocostToken}` },
  });

  await cleanupLeftoverE2eData();
});

test.afterAll(async () => {
  // Dọn dữ liệu test tạo ra — DB dùng chung với phiên khác. Xoá booking trước (FK/logic tham
  // chiếu phòng), rồi mới xoá phòng.
  for (const id of createdBookingIds) {
    try {
      runMysql(`DELETE FROM meeting_room_bookings WHERE id=${id};`);
    } catch (e) {
      // best-effort
    }
  }
  for (const id of createdRoomIds) {
    try {
      runMysql(`DELETE FROM meeting_room_bookings WHERE meeting_room_id=${id};`);
    } catch (e) {
      // best-effort
    }
    await api.delete(`${ROOMS_URL}/${id}`).catch(() => {});
  }
  await api?.dispose();
  await noPermApi?.dispose();
});

async function createRoom(data: any): Promise<number> {
  const res = await api.post(ROOMS_URL, { data });
  expect(res.status(), `tạo phòng setup phải 200: ${JSON.stringify(data)}`).toBe(200);
  const id = (await res.json()).data.id;
  createdRoomIds.push(id);
  return id;
}

// ============================= Nhóm A — validate tĩnh (spec 5.1) =============================

test('A1. tạo phiếu hợp lệ trên phòng KHÔNG cần duyệt -> Đã duyệt (2) ngay, mã DPH-YYYY-NNNNN', async () => {
  const roomId = await createRoom({
    code: CODE_ROOM_NO_APPROVAL,
    name: 'P.KhongCanDuyet',
    company_id: 1,
    require_approval: 0,
    capacity: 5,
  });

  const start = tomorrow9am();
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: roomId,
      title: `Họp A1 ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(200);
  const body = await res.json();
  createdBookingIds.push(body.data.id);

  expect(body.data.code).toMatch(/^DPH-\d{4}-\d{5}$/);
  expect(body.data.status).toBe(2);
  expect(body.data.status_text).toBe('Đã duyệt');
  expect(body.data.status_color).toBe('#2563EB');
  expect(body.data.is_can_edit).toBe(true);
  expect(body.data.is_can_cancel).toBe(true);
  // ISO-8601 CÓ OFFSET, kèm *_text cho người đọc (spec 6.4).
  expect(body.data.start_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$/);
  expect(body.data.start_at_text).toBeTruthy();
});

test('A2. không đặt cho thời điểm đã qua -> 422 field start_at', async () => {
  const start = addHours(new Date(), -2);
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: createdRoomIds[0],
      title: `Họp quá khứ ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(422);
  const body = await res.json();
  expect(body.errors).toHaveProperty('start_at');
});

test('A3. vượt quá hạn đặt trước (meeting_room_max_advance_days mặc định 90) -> 422 field start_at', async () => {
  const start = addDays(new Date(), 100);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: createdRoomIds[0],
      title: `Họp quá hạn ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(422);
  const body = await res.json();
  expect(body.errors).toHaveProperty('start_at');
});

test('A4. gọn trong 1 ngày nhưng ngoài giờ mở cửa (trước 07:00) -> 422', async () => {
  const start = addDays(new Date(), 2);
  start.setHours(5, 0, 0, 0); // 05:00 — trước giờ mở cửa mặc định 07:00
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: createdRoomIds[0],
      title: `Họp ngoài giờ ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(422);
});

test('A5. qua đêm (khác ngày) trong 72h thì BỎ kiểm giờ mở cửa -> vẫn tạo được', async () => {
  const start = addDays(new Date(), 3);
  start.setHours(22, 0, 0, 0);
  const end = addHours(start, 4); // sang ngày hôm sau 02:00 — ngoài giờ mở cửa nhưng là qua đêm nên bỏ kiểm
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: createdRoomIds[0],
      title: `Họp qua đêm hợp lệ ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(200);
  createdBookingIds.push((await res.json()).data.id);
});

test('A6. qua đêm vượt quá 72 giờ -> 422 field end_at', async () => {
  const start = addDays(new Date(), 5);
  start.setHours(8, 0, 0, 0);
  const end = addHours(start, 73);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: createdRoomIds[0],
      title: `Họp qua dài ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(422);
  const body = await res.json();
  expect(body.errors).toHaveProperty('end_at');
});

test('A7. phòng đã khoá (status=2) -> 422', async () => {
  const roomId = await createRoom({ code: CODE_ROOM_INACTIVE, name: 'P.SeBiKhoa', company_id: 1 });
  const lockRes = await api.get(`${ROOMS_URL}/${roomId}/lock`);
  expect(lockRes.status()).toBe(200);

  const start = tomorrow9am();
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: roomId,
      title: `Họp phòng khoá ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
    },
  });
  expect(res.status()).toBe(422);
});

test('A8. khác công ty mà allow_cross_company=0 -> 422; allow_cross_company=1 -> 200', async () => {
  const deniedRoomId = await createRoom({
    code: CODE_ROOM_CROSS_DENIED,
    name: 'P.KhongChoKhacCT',
    company_id: 2,
    allow_cross_company: 0,
  });
  const allowedRoomId = await createRoom({
    code: CODE_ROOM_CROSS_ALLOWED,
    name: 'P.ChoKhacCT',
    company_id: 2,
    allow_cross_company: 1,
  });

  const start = tomorrow9am();
  const end = addHours(start, 1);

  // Token admin thuộc company_id=1 (xem đầu file) -> đặt phòng company_id=2 là khác công ty.
  const denied = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: deniedRoomId, title: `Họp khác CT bị chặn ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(denied.status()).toBe(422);

  const allowed = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: allowedRoomId, title: `Họp khác CT được phép ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(allowed.status()).toBe(200);
  createdBookingIds.push((await allowed.json()).data.id);
});

test('A9. số người dự kiến > sức chứa -> CẢNH BÁO, KHÔNG chặn, KHÔNG tự sửa số đã nhập', async () => {
  const roomId = await createRoom({ code: CODE_ROOM_CAPACITY, name: 'P.SucChua5', company_id: 1, capacity: 5 });
  const start = tomorrow9am();
  const end = addHours(start, 1);
  const res = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: roomId,
      title: `Họp vượt sức chứa ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
      attendee_count: 12,
    },
  });
  expect(res.status()).toBe(200);
  const body = await res.json();
  createdBookingIds.push(body.data.id);
  expect(body.data.attendee_count).toBe(12); // giữ nguyên số user nhập, KHÔNG bị kéo về 5
  expect(Array.isArray(body.data.warnings)).toBe(true);
  expect(body.data.warnings.length).toBeGreaterThan(0);
  expect(body.data.warnings[0]).toContain('12');
});

// ========================= Nhóm B — luật chống trùng (spec 5.2) =========================

test('B1. phòng KHÔNG cần duyệt: trùng giờ với phiếu Đã duyệt -> 422 field start_at kèm tên cuộc họp giữ chỗ', async () => {
  const roomId = createdRoomIds[0]; // CODE_ROOM_NO_APPROVAL, require_approval=0
  const start = addDays(new Date(), 10);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);
  const title = `Họp giữ chỗ B1 ${RUN_SUFFIX}`;

  const first = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(first.status()).toBe(200);
  const firstBody = await first.json();
  createdBookingIds.push(firstBody.data.id);
  expect(firstBody.data.status).toBe(2); // Đã duyệt ngay vì phòng không cần duyệt

  // Trùng 1 phần giờ (09:30-10:30 giao với 09:00-10:00).
  const overlapStart = addHours(start, 0.5);
  const overlapEnd = addHours(overlapStart, 1);
  const second = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp trùng B1 ${RUN_SUFFIX}`, start_at: fmt(overlapStart), end_at: fmt(overlapEnd) },
  });
  expect(second.status()).toBe(422);
  const secondBody = await second.json();
  expect(secondBody.errors).toHaveProperty('start_at');
  expect(secondBody.errors.start_at[0]).toContain(title);

  // Chạm mép (10:00-11:00) KHÔNG tính trùng — phải tạo được (spec: chạm mép không tính trùng).
  const touchStart = end;
  const touchEnd = addHours(touchStart, 1);
  const touching = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp chạm mép B1 ${RUN_SUFFIX}`, start_at: fmt(touchStart), end_at: fmt(touchEnd) },
  });
  expect(touching.status()).toBe(200);
  createdBookingIds.push((await touching.json()).data.id);
});

test('B2. phòng CẦN duyệt: nhiều phiếu Chờ duyệt trùng giờ được phép cùng tồn tại', async () => {
  const roomId = await createRoom({
    code: CODE_ROOM_REQUIRE_APPROVAL,
    name: 'P.CanDuyet',
    company_id: 1,
    require_approval: 1,
    capacity: 5,
  });

  const start = addDays(new Date(), 11);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const [a, b] = await Promise.all([
    api.post(BOOKINGS_URL, { data: { meeting_room_id: roomId, title: `Họp chờ duyệt 1 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) } }),
    api.post(BOOKINGS_URL, { data: { meeting_room_id: roomId, title: `Họp chờ duyệt 2 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) } }),
  ]);
  expect(a.status()).toBe(200);
  expect(b.status()).toBe(200);
  const aBody = await a.json();
  const bBody = await b.json();
  createdBookingIds.push(aBody.data.id, bBody.data.id);
  expect(aBody.data.status).toBe(1); // Chờ duyệt
  expect(bBody.data.status).toBe(1);
});

test('B3. phòng CẦN duyệt nhưng ĐÃ có phiếu Đã duyệt giao giờ -> không ai đặt đè được, kể cả xin duyệt', async () => {
  const roomId = createdRoomIds.find((_id, idx) => true)!; // dùng lại room CODE_ROOM_REQUIRE_APPROVAL (B2 vừa tạo)
  // Lấy đúng room id của CODE_ROOM_REQUIRE_APPROVAL qua API cho chắc (không đoán theo mảng).
  const roomRes = await (await api.get(`${ROOMS_URL}?keyword=${CODE_ROOM_REQUIRE_APPROVAL}`)).json();
  const rows = Array.isArray(roomRes.data) ? roomRes.data : (roomRes.data?.data ?? []);
  const requireApprovalRoomId = rows.find((r: any) => r.code === CODE_ROOM_REQUIRE_APPROVAL).id;

  const start = addDays(new Date(), 12);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const pending = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: requireApprovalRoomId, title: `Họp sẽ được duyệt tay B3 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(pending.status()).toBe(200);
  const pendingId = (await pending.json()).data.id;
  createdBookingIds.push(pendingId);

  // Task 14 mới có endpoint duyệt — set thẳng DB để mô phỏng "đã được duyệt" (hành vi CHỜ DUYỆT
  // -> ĐÃ DUYỆT không phải phạm vi Task 13, chỉ cần trạng thái đúng để kiểm luật chống trùng).
  runMysql(`UPDATE meeting_room_bookings SET status=2 WHERE id=${pendingId};`);

  const overlapping = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: requireApprovalRoomId, title: `Họp xin duyệt đè B3 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(overlapping.status()).toBe(422);
});

// ========================= Nhóm C — CA NGHIỆM THU: race condition =========================

test('C1. 2 request song song trùng giờ -> đúng 1 cái 200 + 1 cái 422, DB chỉ có 1 phiếu, KHÔNG có request nào 500', async () => {
  const roomId = await createRoom({
    code: CODE_ROOM_PARALLEL,
    name: 'P.RaceCondition',
    company_id: 1,
    require_approval: 0,
  });

  const start = addDays(new Date(), 20);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);
  const payload = {
    meeting_room_id: roomId,
    title: `Họp song song ${RUN_SUFFIX}`,
    start_at: fmt(start),
    end_at: fmt(end),
  };

  const [a, b] = await Promise.all([
    api.post(BOOKINGS_URL, { data: payload }),
    api.post(BOOKINGS_URL, { data: payload }),
  ]);

  // Bẫy 2 (sinh mã trùng khi 2 request song song): KHÔNG BAO GIỜ được ra 500.
  expect(a.status(), 'request A không được 500').not.toBe(500);
  expect(b.status(), 'request B không được 500').not.toBe(500);

  const codes = [a.status(), b.status()].sort((x, y) => x - y);
  expect(codes).toEqual([200, 422]); // đúng 1 cái thắng

  const winner = a.status() === 200 ? a : b;
  const winnerBody = await winner.json();
  createdBookingIds.push(winnerBody.data.id);
  expect(winnerBody.data.code).toMatch(/^DPH-\d{4}-\d{5}$/);

  // Chứng minh bằng số liệu DB thật, không suy luận qua status code.
  expect(countBookingsForRoom(roomId)).toBe(1);
});

// ============================= Nhóm D — sửa phiếu (spec 5.4) =============================

test('D1. chủ sở hữu sửa được phiếu của mình khi chưa tới giờ (đổi giờ -> re-run trùng lịch)', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_NO_APPROVAL}_D1`, name: 'P.SuaPhieu', company_id: 1, require_approval: 0 });
  const start = addDays(new Date(), 15);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp D1 gốc ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(created.status()).toBe(200);
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);

  const newStart = addHours(start, 2);
  const newEnd = addHours(newStart, 1);
  const updated = await api.put(`${BOOKINGS_URL}/${bookingId}`, {
    data: { meeting_room_id: roomId, title: `Họp D1 đã sửa ${RUN_SUFFIX}`, start_at: fmt(newStart), end_at: fmt(newEnd) },
  });
  expect(updated.status()).toBe(200);
  const updatedBody = await updated.json();
  expect(updatedBody.data.title).toBe(`Họp D1 đã sửa ${RUN_SUFFIX}`);
  expect(updatedBody.data.start_at_text).toBeTruthy();
});

test('D2. đổi giờ/phòng của phiếu ở phòng CẦN duyệt -> phiếu quay lại Chờ duyệt', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_REQUIRE_APPROVAL}_D2`, name: 'P.SuaVeChoDuyet', company_id: 1, require_approval: 1 });
  const start = addDays(new Date(), 16);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp D2 gốc ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(created.status()).toBe(200);
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);

  // Mô phỏng đã được duyệt (Task 14 mới có endpoint approve) rồi kiểm sửa giờ có quay lại Chờ duyệt.
  runMysql(`UPDATE meeting_room_bookings SET status=2 WHERE id=${bookingId};`);

  const newStart = addHours(start, 3);
  const newEnd = addHours(newStart, 1);
  const updated = await api.put(`${BOOKINGS_URL}/${bookingId}`, {
    data: { meeting_room_id: roomId, title: `Họp D2 đổi giờ ${RUN_SUFFIX}`, start_at: fmt(newStart), end_at: fmt(newEnd) },
  });
  expect(updated.status()).toBe(200);
  const updatedBody = await updated.json();
  expect(updatedBody.data.status).toBe(1); // quay lại Chờ duyệt vì phòng cần duyệt
  expect(updatedBody.data.status_text).toBe('Chờ duyệt');
});

test('D3. sửa title-only (không đổi giờ/phòng) trên phiếu ĐÃ DUYỆT -> KHÔNG bị đẩy về Chờ duyệt', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_REQUIRE_APPROVAL}_D3`, name: 'P.SuaKhongDoiGio', company_id: 1, require_approval: 1 });
  const start = addDays(new Date(), 17);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp D3 gốc ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);
  runMysql(`UPDATE meeting_room_bookings SET status=2 WHERE id=${bookingId};`);

  const updated = await api.put(`${BOOKINGS_URL}/${bookingId}`, {
    data: { meeting_room_id: roomId, title: `Họp D3 chỉ đổi tên ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(updated.status()).toBe(200);
  const updatedBody = await updated.json();
  expect(updatedBody.data.status).toBe(2); // vẫn Đã duyệt vì giờ/phòng không đổi
});

test('D4. không phải người đặt sửa phiếu -> 403', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_NO_APPROVAL}_D4`, name: 'P.KhongPhaiChuSuaDuoc', company_id: 1 });
  const start = addDays(new Date(), 18);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp D4 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);

  const res = await noPermApi.put(`${BOOKINGS_URL}/${bookingId}`, {
    data: { meeting_room_id: roomId, title: `Họp D4 bị sửa trộm ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(res.status()).toBe(403);
});

test('D5. phiếu đã tới giờ bắt đầu -> sửa trả 423 (KHÔNG phải 422)', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_NO_APPROVAL}_D5`, name: 'P.DaToiGio', company_id: 1 });
  const start = addDays(new Date(), 19);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: { meeting_room_id: roomId, title: `Họp D5 ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);

  // "Đã tới giờ" tại THỜI ĐIỂM GỌI UPDATE — chỉnh thẳng start_at trong DB về quá khứ để tái hiện
  // xác định, không phụ thuộc timing/sleep (đúng tinh thần "lỗi phải tái hiện được trước khi sửa").
  const pastStart = addHours(new Date(), -1);
  runMysql(`UPDATE meeting_room_bookings SET start_at='${fmt(pastStart)}' WHERE id=${bookingId};`);

  const res = await api.put(`${BOOKINGS_URL}/${bookingId}`, {
    data: { meeting_room_id: roomId, title: `Họp D5 sửa muộn ${RUN_SUFFIX}`, start_at: fmt(start), end_at: fmt(end) },
  });
  expect(res.status()).toBe(423);
});

// ============================= Nhóm E — Resource + participants =============================

test('E1. detail trả kèm participants khi tạo có participant_ids', async () => {
  const roomId = await createRoom({ code: `${CODE_ROOM_NO_APPROVAL}_E1`, name: 'P.Participants', company_id: 1 });
  const start = addDays(new Date(), 21);
  start.setHours(9, 0, 0, 0);
  const end = addHours(start, 1);

  const created = await api.post(BOOKINGS_URL, {
    data: {
      meeting_room_id: roomId,
      title: `Họp E1 ${RUN_SUFFIX}`,
      start_at: fmt(start),
      end_at: fmt(end),
      participant_ids: [25],
    },
  });
  expect(created.status()).toBe(200);
  const bookingId = (await created.json()).data.id;
  createdBookingIds.push(bookingId);

  const detail = await (await api.get(`${BOOKINGS_URL}/${bookingId}`)).json();
  const participantIds = (detail.data.participants || []).map((p: any) => p.employee_id);
  expect(participantIds).toContain(25);
});
```
