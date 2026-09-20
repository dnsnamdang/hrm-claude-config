# Review package — Task 14 (duyệt/từ chối/hủy + luật nhìn thấy phiếu)

## Service (chỉ các method của Task 14)
```php

            $booking->save();

            $this->syncParticipants($booking, $request->input('participant_ids'));

            $booking->warnings = $warnings;

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Task 14, Bước 1-2 — Duyệt (spec 5.3) + tự động Từ chối mọi phiếu Chờ duyệt CÙNG PHÒNG giao
     * giờ (spec 5.2 vế "duyệt phiếu nào phiếu đó thắng"). TOÀN BỘ trong 1 transaction có khóa —
     * 2 người duyệt 2 phiếu trùng giờ cùng lúc mà không khóa là duyệt lọt cả hai.
     *
     * Thứ tự khóa PHẢI giống `assertNoOverlap()` (Room trước, Booking sau) — nếu đảo ngược
     * (khóa Booking trước rồi mới khóa Room) sẽ tạo lock order khác với `store()`/`update()`,
     * nguy cơ deadlock khi 2 transaction khóa chéo nhau theo 2 thứ tự khác nhau.
     */
    public function approve(MeetingRoomBooking $booking)
    {
        return DB::transaction(function () use ($booking) {
            // Mutex theo phòng — PHẢI khóa TRƯỚC (đúng thứ tự với assertNoOverlap()/store()/update()).
            $room = MeetingRoom::where('id', $booking->meeting_room_id)->lockForUpdate()->firstOrFail();

            $booking = MeetingRoomBooking::where('id', $booking->id)->lockForUpdate()->firstOrFail();

            if (!$this->canActOnApprovalByRoom($room)) {
                throw new \Exception('Bạn không có quyền duyệt phiếu này', 403);
            }

            if (!$booking->isCanApprove()) {
                throw new \Exception('Phiếu không ở trạng thái Chờ duyệt', 423);
            }

            $booking->status = MeetingRoomBooking::STATUS_DA_DUYET;
            $booking->approved_by = auth()->id();
            $booking->approved_at = Carbon::now();
            $booking->save();

            // Mọi phiếu CHỜ DUYỆT khác cùng phòng giao giờ với phiếu vừa duyệt -> tự Từ chối.
            // Khóa (`lockForUpdate`) TRƯỚC khi cập nhật — cùng phạm vi index bắt buộc spec 4.4.
            $conflicts = MeetingRoomBooking::where('meeting_room_id', $booking->meeting_room_id)
                ->where('id', '!=', $booking->id)
                ->where('status', MeetingRoomBooking::STATUS_CHO_DUYET)
                ->where('start_at', '<', $booking->end_at)
                ->where('end_at', '>', $booking->start_at)
                ->lockForUpdate()
                ->get();

            foreach ($conflicts as $conflict) {
                $conflict->status = MeetingRoomBooking::STATUS_TU_CHOI;
                $conflict->is_auto_rejected = 1;
                $conflict->reject_reason = 'Phòng đã được duyệt cho cuộc họp khác';
                $conflict->save();
            }

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Task 14, Bước 5 — Từ chối (spec 5.3). Từ chối ≠ Hủy (spec 5.5): trạng thái + màu riêng,
     * `is_auto_rejected` LUÔN = 0 ở đây (chỉ auto-reject của `approve()` mới set = 1).
     * `reject_reason` bắt buộc đã được `MeetingRoomBookingRejectRequest` validate ở tầng Request.
     */
    public function reject(MeetingRoomBooking $booking, $reason)
    {
        return DB::transaction(function () use ($booking, $reason) {
            $room = MeetingRoom::findOrFail($booking->meeting_room_id);
            $booking = MeetingRoomBooking::where('id', $booking->id)->lockForUpdate()->firstOrFail();

            if (!$this->canActOnApprovalByRoom($room)) {
                throw new \Exception('Bạn không có quyền từ chối phiếu này', 403);
            }

            if (!$booking->isCanReject()) {
                throw new \Exception('Phiếu không ở trạng thái Chờ duyệt', 423);
            }

            $booking->status = MeetingRoomBooking::STATUS_TU_CHOI;
            $booking->is_auto_rejected = 0;
            $booking->reject_reason = $reason;
            $booking->save();

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Task 14, Bước 3-4 — Hủy (spec 5.5).
     *
     * QUYẾT ĐỊNH #12 (spec 5.5 + plan) kiểm NGAY ĐẦU HÀM, TRƯỚC transaction/lock: phiếu
     * `source = SOURCE_TU_MEETING` thì KHÔNG AI hủy được, kể cả quản lý phòng — Phase 2 chưa có
     * đường sinh phiếu `source = 2` (Phase 4 mới đồng bộ Meeting -> booking) nhưng chốt chặn phải
     * cài NGAY, nếu không Phase 4 bật lên là hở toang.
     */
    public function cancel(MeetingRoomBooking $booking, $reason)
    {
        if ((int) $booking->source === MeetingRoomBooking::SOURCE_TU_MEETING) {
            throw new \Exception(
                'Phiếu này sinh từ cuộc họp (Meeting), vui lòng thay đổi lịch/phòng ở chính phiếu họp đó.',
                423
            );
        }

        return DB::transaction(function () use ($booking, $reason) {
            $booking = MeetingRoomBooking::where('id', $booking->id)->lockForUpdate()->firstOrFail();

            // "Đã tới giờ" = khóa, bất kể ai gọi — kiểm trước tiên (đúng quy ước CLAUDE.md).
            if (Carbon::now()->gte(Carbon::parse($booking->start_at))) {
                throw new \Exception('Phiếu đã tới giờ bắt đầu, không thể hủy nữa. Muốn kết thúc sớm, dùng Check-out.', 423);
            }

            if (!in_array((int) $booking->status, [MeetingRoomBooking::STATUS_CHO_DUYET, MeetingRoomBooking::STATUS_DA_DUYET], true)) {
                throw new \Exception('Phiếu không ở trạng thái có thể hủy', 423);
            }

            // Ai được hủy (spec 5.5): người đặt · quản lý phòng · người có quyền 1580.
            $isOwner = (int) $booking->booked_by_employee_id === (int) auth()->id();
            if (!$isOwner) {
                $room = MeetingRoom::findOrFail($booking->meeting_room_id);
                if (!$this->canActOnApprovalByRoom($room)) {
                    throw new \Exception('Bạn không có quyền hủy phiếu này', 403);
                }
            }

            $booking->status = MeetingRoomBooking::STATUS_DA_HUY;
            $booking->cancelled_by = auth()->id();
            $booking->cancelled_at = Carbon::now();
            $booking->cancel_reason = $reason;
            $booking->save();

            $booking->load(['room', 'participants.employee.info', 'employee_create.info', 'employee_update.info']);

            return $this->attachDisplayNames($booking);
        });
    }

    /**
     * Spec 5.3: "Người duyệt = quản lý phòng (`manager_employee_id`) HOẶC người có quyền
     * *Duyệt phiếu đặt phòng họp*". Dùng chung cho approve/reject/cancel (spec 5.5 cũng liệt
     * đúng 2 vế này + người đặt).
     *
     * ⚠️ CỐ TÌNH KHÔNG gắn `checkPermission:Duyệt phiếu đặt phòng họp` ở tầng route cho
     * approve/reject (xem `Routes/api.php`): route middleware chỉ kiểm ĐƯỢC quyền tĩnh của
     * role, không kiểm được "có phải quản lý CỦA ĐÚNG PHÒNG này không" — 1 phòng cụ thể. Gắn
     * cứng middleware đó sẽ CHẶN LUÔN quản lý phòng không có quyền 1580 (trường hợp bình thường,
     * xem F1/F2 của task-13-report + G4/I3 của task-14), trái spec 5.3. Gate thật nằm ở ĐÂY.
     */
    private function canActOnApprovalByRoom(MeetingRoom $room)
    {
        $isRoomManager = $room->manager_employee_id && (int) $room->manager_employee_id === (int) auth()->id();

        return $isRoomManager || isCurrentEmployeeHasPermission('Duyệt phiếu đặt phòng họp');
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
```

## Controller
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
use Modules\Meeting\Http\Requests\MeetingRoomBooking\MeetingRoomBookingCancelRequest;
use Modules\Meeting\Http\Requests\MeetingRoomBooking\MeetingRoomBookingRejectRequest;
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
        try {
            // Task 14, Bước 6 — luật nhìn thấy phiếu (loadDetail() ném 403 nếu không đủ điều
            // kiện: không có quyền 1579 và không phải người đặt/được mời/quản lý phòng).
            $booking = $this->meetingRoomBookingService->loadDetail($meetingRoomBooking);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (Exception $e) {
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    public function store(MeetingRoomBookingRequest $request)
    {
        try {
            $booking = $this->meetingRoomBookingService->store($request);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (ValidationException $e) {
            // Lỗi validate (trùng lịch, quá khứ, ngoài giờ mở cửa…) phải giữ nguyên field lỗi để
            // FE map vào từng ô nhập — catch chung Exception bên dưới sẽ nuốt mất field lỗi.
            // Bắt Ở ĐÂY (trước catch Exception) rồi TỰ DỰNG response theo ĐÚNG khuôn
            // `BaseRequest::failedValidation()` (fix round 1, VIỆC 3) — nếu rethrow thẳng,
            // handler mặc định của Laravel trả `{message, errors}` khác khuôn `{code, errors}`
            // mà toàn bộ phần còn lại của app dùng, khiến FE phải đoán 2 khuôn lỗi 422 khác nhau.
            return $this->responseValidationError($e);
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
            return $this->responseValidationError($e);
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    /**
     * Task 14, Bước 1-2 — Duyệt phiếu (spec 5.3) + tự động Từ chối phiếu Chờ duyệt trùng giờ
     * cùng phòng (spec 5.2). KHÔNG gắn `checkPermission` ở route (xem `Routes/api.php` +
     * `MeetingRoomBookingService::canActOnApprovalByRoom()`).
     */
    public function approve(MeetingRoomBooking $meetingRoomBooking)
    {
        try {
            $booking = $this->meetingRoomBookingService->approve($meetingRoomBooking);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    /** Task 14, Bước 5 — Từ chối phiếu (spec 5.3), Từ chối ≠ Hủy (spec 5.5). */
    public function reject(MeetingRoomBookingRejectRequest $request, MeetingRoomBooking $meetingRoomBooking)
    {
        try {
            $booking = $this->meetingRoomBookingService->reject($meetingRoomBooking, $request->reject_reason);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    /**
     * Task 14, Bước 3-4 — Hủy phiếu (spec 5.5) + chốt chặn quyết định #12
     * (`source = SOURCE_TU_MEETING` thì KHÔNG AI hủy được, kể cả quản lý phòng).
     */
    public function cancel(MeetingRoomBookingCancelRequest $request, MeetingRoomBooking $meetingRoomBooking)
    {
        try {
            $booking = $this->meetingRoomBookingService->cancel($meetingRoomBooking, $request->cancel_reason);

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomBookingResource($booking));
        } catch (Exception $e) {
            Log::error($e);
            $code = in_array($e->getCode(), [403, 422, 423]) ? $e->getCode() : Response::HTTP_BAD_REQUEST;

            return $this->responseJson($e->getMessage(), $code);
        }
    }

    /**
     * Fix round 1 (review), VIỆC 3 — chuẩn hoá `ValidationException` ném từ Service (trùng lịch,
     * quá khứ, ngoài giờ mở cửa…) về ĐÚNG khuôn `{code, errors}` của
     * `Modules\Training\Http\Requests\BaseRequest::failedValidation()` — khuôn lỗi 422 DUY NHẤT
     * mà FE (Task 17) cần nhận diện để hiện lỗi inline dưới đúng ô, không phải đoán giữa khuôn này
     * và khuôn mặc định `{message, errors}` của Laravel. `errors.<field>` là 1 CHUỖI (lấy message
     * đầu tiên), không phải mảng — khớp cách `BaseRequest` đang làm.
     */
    private function responseValidationError(ValidationException $e)
    {
        $message = [];
        foreach ($e->errors() as $field => $items) {
            $message[$field] = $items[0];
        }

        return response()->json([
            'code' => Response::HTTP_UNPROCESSABLE_ENTITY,
            'errors' => $message,
        ], Response::HTTP_UNPROCESSABLE_ENTITY);
    }
}
```

## Routes
```php

    // Plan quan-ly-phong-hop, Task 13 — Phiếu đặt phòng họp (tạo/sửa + chống trùng lịch).
    // `store` (POST) KHÔNG gắn checkPermission — quyết định #8: mọi nhân viên đều đặt phòng
    // được. `index`/`show` áp "luật nhìn thấy phiếu" (Task 14, quyền 1579 "Xem tất cả phiếu đặt
    // phòng họp") NGAY BÊN TRONG Service (`applyVisibilityScope()`/`canView()`) — không gắn
    // `checkPermission` cứng ở route vì người KHÔNG có quyền 1579 vẫn phải xem được phiếu của
    // CHÍNH MÌNH/được mời/phòng mình quản lý, chỉ bị lọc bớt phần "của người khác".
    //
    // Plan quan-ly-phong-hop, Task 14 — Duyệt/Từ chối/Hủy phiếu.
    // `approve`/`reject` CỐ TÌNH KHÔNG gắn `checkPermission:Duyệt phiếu đặt phòng họp` — spec 5.3:
    // "người duyệt = quản lý phòng (manager_employee_id) HOẶC người có quyền 1580". Quyền 1580 là
    // quyền TĨNH theo role, không biết "quản lý CỦA ĐÚNG PHÒNG nào" — 1 phòng cụ thể là dữ liệu
    // của TỪNG BẢN GHI, middleware route không kiểm được. Gắn cứng middleware ở đây sẽ CHẶN LUÔN
    // quản lý phòng không có quyền 1580 (trường hợp bình thường, xem F1/F2 task-13 + G4/I3
    // task-14) — trái spec. Gate thật nằm trong
    // `MeetingRoomBookingService::canActOnApprovalByRoom()`, chạy TRONG transaction có khóa.
    // `cancel` cũng KHÔNG gắn — người đặt phải hủy được phiếu của mình (không có quyền riêng nào
    // cho việc đó) — kiểm quyền bên trong Service theo đúng luật spec 5.5 (người đặt / quản lý
    // phòng / quyền 1580).
    Route::group(['prefix' => 'meeting/room-bookings'], function () {
        Route::get('/', [MeetingRoomBookingController::class, 'index']);
        Route::post('/', [MeetingRoomBookingController::class, 'store']);
        Route::get('/{meetingRoomBooking}', [MeetingRoomBookingController::class, 'show']);
        Route::put('/{meetingRoomBooking}', [MeetingRoomBookingController::class, 'update']);
        Route::put('/{meetingRoomBooking}/approve', [MeetingRoomBookingController::class, 'approve']);
        Route::put('/{meetingRoomBooking}/reject', [MeetingRoomBookingController::class, 'reject']);
        Route::put('/{meetingRoomBooking}/cancel', [MeetingRoomBookingController::class, 'cancel']);
    });
});
```

## 2 Request mới
### Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingRejectRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoomBooking;

use Modules\Training\Http\Requests\BaseRequest;

/**
 * Plan quan-ly-phong-hop, Task 14 — validate body của PUT `/meeting/room-bookings/{id}/reject`.
 *
 * Spec 5.3: "Từ chối bắt buộc nhập lý do". Chỉ validate CẤU TRÚC ở đây (bắt buộc + độ dài) —
 * luật NGHIỆP VỤ (chỉ phiếu Chờ duyệt mới từ chối được, ai được từ chối) nằm ở
 * `MeetingRoomBookingService::reject()` vì cần đọc + khoá bản ghi.
 */
class MeetingRoomBookingRejectRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'reject_reason' => ['required', 'string', 'max:500'],
        ];
    }

    public function messages()
    {
        return [
            'reject_reason.required' => 'Vui lòng nhập lý do từ chối',
            'reject_reason.max' => 'Lý do từ chối tối đa 500 ký tự',
        ];
    }
}
```
### Modules/Meeting/Http/Requests/MeetingRoomBooking/MeetingRoomBookingCancelRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoomBooking;

use Modules\Training\Http\Requests\BaseRequest;

/**
 * Plan quan-ly-phong-hop, Task 14 — validate body của PUT `/meeting/room-bookings/{id}/cancel`.
 *
 * Spec 5.5: "Bắt buộc nhập lý do". Chỉ validate CẤU TRÚC ở đây — luật NGHIỆP VỤ (ai được hủy,
 * chỉ trước giờ bắt đầu, quyết định #12 chặn `source = 2`) nằm ở
 * `MeetingRoomBookingService::cancel()` vì cần đọc + khoá bản ghi.
 */
class MeetingRoomBookingCancelRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'cancel_reason' => ['required', 'string', 'max:500'],
        ];
    }

    public function messages()
    {
        return [
            'cancel_reason.required' => 'Vui lòng nhập lý do hủy',
            'cancel_reason.max' => 'Lý do hủy tối đa 500 ký tự',
        ];
    }
}
```
