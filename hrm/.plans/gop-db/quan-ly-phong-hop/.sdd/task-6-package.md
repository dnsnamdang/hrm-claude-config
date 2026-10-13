# Review package — Task 6 (API danh mục phòng họp)

### Modules/Meeting/Services/MeetingRoomService.php
```php
<?php

namespace Modules\Meeting\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Human\Entities\Company;
use Modules\Meeting\Entities\MeetingRoom;
use Modules\Meeting\Entities\MeetingRoomAmenity;
use Modules\Timesheet\Entities\GeneralRegulation;
use Modules\Training\Services\BaseService;

/**
 * Plan quan-ly-phong-hop, Task 6 — danh mục "Phòng họp".
 * Khuôn copy từ `MeetingRoomAmenityService` (Task 5), thêm lọc theo công ty/sức chứa/tiện
 * nghi và đồng bộ pivot tiện nghi trong `updateOrCreate`.
 */
class MeetingRoomService extends BaseService
{
    public function index(Request $request)
    {
        // ⚠️ N+1 (review Task 3): luôn kèm sẵn `amenities` ở đây, Controller không được tự
        // load lại trong vòng lặp Resource.
        $query = MeetingRoom::query()->select('meeting_rooms.*')->with('amenities');

        if (isset($request->keyword)) {
            $escapedKeyword = escapeLikeKeyword($request->keyword);
            if ($escapedKeyword !== '') {
                $query->where(function ($q) use ($escapedKeyword) {
                    $q->where('name', 'like', '%' . $escapedKeyword . '%')
                        ->orWhere('code', 'like', '%' . $escapedKeyword . '%');
                });
            }
        }

        if (isset($request->company_id) && $request->company_id !== '') {
            $query->where('company_id', $request->company_id);
        }

        if (isset($request->capacity_from) && $request->capacity_from !== '') {
            $query->where('capacity', '>=', $request->capacity_from);
        }

        if ($request->filled('amenity_ids')) {
            $amenityIds = (array) $request->amenity_ids;
            $query->whereHas('amenities', function ($q) use ($amenityIds) {
                $q->whereIn('meeting_room_amenities.id', $amenityIds);
            });
        }

        if (isset($request->status) && $request->status !== '') {
            $query->where('status', $request->status);
        }

        return $query->orderBy('id', 'desc');
    }

    /**
     * Dữ liệu phục vụ form thêm/sửa phòng họp trong 1 request: tiện nghi đang hoạt động,
     * danh sách công ty, và cấu hình giờ mặc định của công ty đang đăng nhập (fallback hệ
     * thống nếu công ty chưa khai ở `general_regulations`).
     */
    public function formOptions(Request $request)
    {
        $amenities = MeetingRoomAmenity::query()
            ->where('status', MeetingRoomAmenity::STATUS_ACTIVE)
            ->orderBy('sort_order', 'asc')
            ->orderBy('id', 'asc')
            ->get();

        $companies = Company::query()
            ->where('status', 1)
            ->orderBy('name', 'asc')
            ->get(['id', 'name', 'code']);

        $companyId = $request->company_id ?? (auth()->user()->info->company_id ?? null);
        $regulation = $companyId ? GeneralRegulation::where('company_id', $companyId)->first() : null;

        $config = [
            'open_time' => MeetingRoom::resolveConfig(null, $regulation->meeting_room_open_time ?? null, '07:00:00'),
            'close_time' => MeetingRoom::resolveConfig(null, $regulation->meeting_room_close_time ?? null, '20:00:00'),
            'checkin_grace_minutes' => (int) MeetingRoom::resolveConfig(null, $regulation->meeting_room_checkin_grace_minutes ?? null, 15),
        ];

        return [
            'amenities' => $amenities,
            'companies' => $companies,
            'config' => $config,
        ];
    }

    /**
     * @return MeetingRoom|array
     */
    public function updateOrCreate(Request $request)
    {
        return DB::transaction(function () use ($request) {
            $id = $request->input('id');

            if ($id) {
                $room = MeetingRoom::find($id);
                if (!$room || $room->status != MeetingRoom::STATUS_ACTIVE) {
                    return ['status' => '404', 'message' => 'Dữ liệu đã thay đổi, vui lòng tải lại'];
                }
            }

            $data = $request->only([
                'code', 'name', 'company_id', 'department_id', 'part_id', 'allow_cross_company',
                'location', 'capacity', 'manager_employee_id', 'require_approval',
                'open_time', 'close_time', 'checkin_grace_minutes', 'description',
            ]);

            if ($id) {
                $room->update($data);
            } else {
                $data['status'] = MeetingRoom::STATUS_ACTIVE;
                $room = MeetingRoom::create($data);
            }

            $room->amenities()->sync($request->input('amenity_ids', []));

            return $room->load('amenities');
        });
    }

    public function destroy(MeetingRoom $meetingRoom)
    {
        $meetingRoom->delete();
    }
}
```

### Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
```php
<?php

namespace Modules\Meeting\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Validation\ValidationException;
use Modules\Meeting\Entities\MeetingRoom;
use Modules\Meeting\Http\Requests\MeetingRoom\MeetingRoomRequest;
use Modules\Meeting\Services\MeetingRoomService;
use Modules\Meeting\Transformers\MeetingRoom\DetailMeetingRoomResource;
use Modules\Meeting\Transformers\MeetingRoom\MeetingRoomResource;

/**
 * Plan quan-ly-phong-hop, Task 6 — danh mục "Phòng họp".
 * Khuôn copy từ `MeetingRoomAmenityController` (Task 5), thêm `form-options` (dữ liệu dựng
 * form trong 1 request) và `upcomingBookings` (cảnh báo trước khi Khóa phòng).
 */
class MeetingRoomController extends ApiController
{
    private $meetingRoomService;

    public function __construct(MeetingRoomService $meetingRoomService)
    {
        $this->meetingRoomService = $meetingRoomService;
    }

    public function index(Request $request)
    {
        $query = $this->meetingRoomService->index($request);
        $paginated = $query->paginate($request->per_page ?? 10)->appends($request->query());

        // Tránh N+1 (review Task 3): tính số phiếu đã đặt theo LÔ cho cả trang, gán thẳng
        // vào từng model trước khi map Resource — KHÔNG gọi $room->isCanDelete() từng dòng.
        $ids = collect($paginated->items())->pluck('id')->all();
        $usedCounts = empty($ids) ? collect() : DB::table('meeting_room_bookings')
            ->whereIn('meeting_room_id', $ids)
            ->selectRaw('meeting_room_id, COUNT(*) AS cnt')
            ->groupBy('meeting_room_id')
            ->pluck('cnt', 'meeting_room_id');

        foreach ($paginated->items() as $room) {
            $room->used_booking_count = (int) ($usedCounts[$room->id] ?? 0);
        }

        $result = MeetingRoomResource::collection($paginated)->response()->getData();

        return $this->apiGetList($result, []);
    }

    /** Dữ liệu dựng form thêm/sửa phòng họp trong 1 request: tiện nghi + công ty + cấu hình giờ */
    public function formOptions(Request $request)
    {
        $result = $this->meetingRoomService->formOptions($request);

        return $this->responseJson('success', Response::HTTP_OK, $result);
    }

    public function updateOrCreate(MeetingRoomRequest $request)
    {
        try {
            $result = $this->meetingRoomService->updateOrCreate($request);
            if (is_array($result) && isset($result['status']) && $result['status'] === '404') {
                return $this->responseNotFound($result['message']);
            }

            return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomResource($result));
        } catch (ValidationException $e) {
            // Lỗi validate phải giữ nguyên để FE map vào từng ô nhập — catch chung bên dưới
            // sẽ biến nó thành 400 mất thông tin field.
            throw $e;
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show(MeetingRoom $meetingRoom)
    {
        $meetingRoom->load('amenities');

        return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomResource($meetingRoom));
    }

    /**
     * Xóa 1 phòng họp. Chặn khi phòng đã có phiếu đặt (dù mới/đã hủy) — xóa mất phòng thì
     * lịch sử phiếu mồ côi `meeting_room_id`; trường hợp này chỉ được Khóa.
     */
    public function destroy(MeetingRoom $meetingRoom)
    {
        if (!$meetingRoom->isCanDelete()) {
            return $this->responseJson(
                'Phòng họp này đã có phiếu đặt nên không xóa được. Bạn có thể Khóa phòng.',
                Response::HTTP_BAD_REQUEST
            );
        }

        try {
            return DB::transaction(function () use ($meetingRoom) {
                $this->meetingRoomService->destroy($meetingRoom);

                return $this->responseJson('success', Response::HTTP_OK);
            });
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function lock(MeetingRoom $meetingRoom)
    {
        if (!$meetingRoom->isCanLockUpdate()) {
            return $this->responseBadRequest('Dữ liệu đã thay đổi, vui lòng tải lại');
        }

        $meetingRoom->status = MeetingRoom::STATUS_INACTIVE;
        $meetingRoom->save();

        return $this->responseJson('Khóa thành công', Response::HTTP_OK);
    }

    public function unlock(MeetingRoom $meetingRoom)
    {
        $meetingRoom->status = MeetingRoom::STATUS_ACTIVE;
        $meetingRoom->save();

        return $this->responseJson('Mở khóa thành công', Response::HTTP_OK);
    }

    /** Số phiếu sắp tới + danh sách — dùng để cảnh báo trước khi Khóa phòng */
    public function upcomingBookings(MeetingRoom $meetingRoom)
    {
        return $this->responseJson('success', Response::HTTP_OK, [
            'count' => $meetingRoom->upcomingBookingCount(),
            'items' => [], // Phase 2 trả chi tiết khi đã có Resource của phiếu
        ]);
    }
}
```

### Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoom;

use Illuminate\Validation\Rule;
use Modules\Training\Http\Requests\BaseRequest;

/**
 * Plan quan-ly-phong-hop, Task 6 — validate form thêm/sửa danh mục "Phòng họp".
 *
 * ⚠️ `company_id` khai `required`: `BaseModel::boot()` tự điền `company_id` từ
 * `auth()->user()->info->company_id` khi cột trống lúc tạo, nhưng ở đây người dùng phải
 * chọn tường minh công ty sở hữu phòng (dùng để tính unique `code` theo công ty và quyết
 * định `allow_cross_company`) — không được dựa vào auto-fill.
 *
 * `code` chỉ unique TRONG CÙNG công ty: khác công ty được trùng mã (VD 2 chi nhánh cùng có
 * phòng "A301"). `ignore($id)` để sửa phòng không tự đụng chính nó.
 */
class MeetingRoomRequest extends BaseRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        $id = $this->input('id');

        return [
            'code' => [
                'required', 'string', 'max:50',
                Rule::unique('meeting_rooms', 'code')
                    ->where(fn ($q) => $q->where('company_id', $this->input('company_id')))
                    ->ignore($id),
            ],
            'name' => ['required', 'string', 'max:255'],
            'company_id' => ['required', 'integer'],
            'department_id' => ['nullable', 'integer'],
            'part_id' => ['nullable', 'integer'],
            'allow_cross_company' => ['nullable', 'boolean'],
            'location' => ['nullable', 'string', 'max:255'],
            'capacity' => ['nullable', 'integer', 'min:1'],
            'manager_employee_id' => ['nullable', 'integer'],
            'require_approval' => ['nullable', 'boolean'],
            'open_time' => ['nullable', 'date_format:H:i:s'],
            'close_time' => ['nullable', 'date_format:H:i:s', 'after:open_time'],
            'checkin_grace_minutes' => ['nullable', 'integer', 'min:0', 'max:120'],
            'description' => ['nullable', 'string'],
            'amenity_ids' => ['nullable', 'array'],
            'amenity_ids.*' => ['integer', 'exists:meeting_room_amenities,id'],
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
            'code.required' => 'Vui lòng nhập mã phòng họp',
            'code.max' => 'Mã phòng họp tối đa 50 ký tự',
            'code.unique' => 'Mã phòng họp đã tồn tại trong công ty này',
            'name.required' => 'Vui lòng nhập tên phòng họp',
            'name.max' => 'Tên phòng họp tối đa 255 ký tự',
            'company_id.required' => 'Vui lòng chọn công ty',
            'company_id.integer' => 'Công ty không hợp lệ',
            'capacity.integer' => 'Sức chứa phải là số nguyên',
            'capacity.min' => 'Sức chứa tối thiểu là 1',
            'open_time.date_format' => 'Giờ mở cửa không hợp lệ (HH:mm:ss)',
            'close_time.date_format' => 'Giờ đóng cửa không hợp lệ (HH:mm:ss)',
            'close_time.after' => 'Giờ đóng cửa phải sau giờ mở cửa',
            'checkin_grace_minutes.integer' => 'Ân hạn check-in phải là số nguyên',
            'checkin_grace_minutes.min' => 'Ân hạn check-in không được âm',
            'checkin_grace_minutes.max' => 'Ân hạn check-in tối đa 120 phút',
            'amenity_ids.array' => 'Danh sách tiện nghi không hợp lệ',
            'amenity_ids.*.exists' => 'Tiện nghi không tồn tại trong hệ thống',
        ];
    }
}
```

### Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoom;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;
use Modules\Meeting\Entities\MeetingRoom;

/**
 * Plan quan-ly-phong-hop, Task 6 — 1 dòng trong màn danh sách "Phòng họp".
 *
 * ⚠️ N+1 (review Task 3): `isCanDelete()` truy vấn bảng `meeting_room_bookings` — 1 query/dòng
 * nếu gọi trực tiếp trong vòng lặp. `MeetingRoomController::index()` PHẢI tính trước theo lô
 * rồi gán `used_booking_count` thẳng vào TỪNG MODEL (không dùng biến static trên Resource như
 * Task 5) trước khi dựng collection.
 */
class MeetingRoomResource extends ApiResource
{
    public function toArray($request): array
    {
        $usedCount = $this->used_booking_count ?? null;
        $isCanDelete = $usedCount !== null ? ((int) $usedCount === 0) : $this->isCanDelete();

        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'company_id' => $this->company_id,
            'department_id' => $this->department_id,
            'part_id' => $this->part_id,
            'allow_cross_company' => (bool) $this->allow_cross_company,
            'location' => $this->location,
            'capacity' => $this->capacity,
            'manager_employee_id' => $this->manager_employee_id,
            'require_approval' => (bool) $this->require_approval,
            'open_time' => $this->open_time,
            'close_time' => $this->close_time,
            'checkin_grace_minutes' => $this->checkin_grace_minutes,
            'status' => $this->status,
            'status_text' => $this->status == MeetingRoom::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
            'amenities' => $this->whenLoaded('amenities', function () {
                return $this->amenities->map(function ($amenity) {
                    return [
                        'id' => $amenity->id,
                        'code' => $amenity->code,
                        'name' => $amenity->name,
                        'icon' => $amenity->icon,
                        'quantity' => $amenity->pivot->quantity ?? null,
                        'note' => $amenity->pivot->note ?? null,
                    ];
                });
            }),
            'created_at' => Helper::formatDateTime($this->created_at),
            'updated_at' => Helper::formatDateTime($this->updated_at),
            'updated_by_name' => $this->employee_update_name,
            'created_by_name' => $this->employee_create_name,
            'is_can_edit' => $this->isCanEdit(),
            'is_can_delete' => $isCanDelete,
            'is_can_lock' => $this->isCanLockUpdate(),
        ];
    }
}
```

### Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoom;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;
use Modules\Meeting\Entities\MeetingRoom;

/**
 * Plan quan-ly-phong-hop, Task 6 — chi tiết 1 phòng họp (popup Xem/Sửa, và cũng dùng làm
 * response của tạo mới / cập nhật để FE có sẵn `checkin_qr_token` + 3 cờ is_can_* ngay sau
 * khi lưu).
 */
class DetailMeetingRoomResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'company_id' => $this->company_id,
            'department_id' => $this->department_id,
            'part_id' => $this->part_id,
            'allow_cross_company' => (bool) $this->allow_cross_company,
            'location' => $this->location,
            'capacity' => $this->capacity,
            'manager_employee_id' => $this->manager_employee_id,
            'require_approval' => (bool) $this->require_approval,
            'open_time' => $this->open_time,
            'close_time' => $this->close_time,
            'checkin_grace_minutes' => $this->checkin_grace_minutes,
            'checkin_qr_token' => $this->checkin_qr_token,
            'description' => $this->description,
            'status' => $this->status,
            'status_text' => $this->status == MeetingRoom::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
            'amenities' => $this->whenLoaded('amenities', function () {
                return $this->amenities->map(function ($amenity) {
                    return [
                        'id' => $amenity->id,
                        'code' => $amenity->code,
                        'name' => $amenity->name,
                        'icon' => $amenity->icon,
                        'quantity' => $amenity->pivot->quantity ?? null,
                        'note' => $amenity->pivot->note ?? null,
                    ];
                });
            }),
            'created_at' => Helper::formatDateTime($this->created_at),
            'updated_at' => Helper::formatDateTime($this->updated_at),
            'updated_by_name' => $this->employee_update_name,
            'created_by_name' => $this->employee_create_name,
            'is_can_edit' => $this->isCanEdit(),
            'is_can_delete' => $this->isCanDelete(),
            'is_can_lock' => $this->isCanLockUpdate(),
        ];
    }
}
```

### Modules/Meeting/Routes/api.php
```php
<?php

use Illuminate\Support\Facades\Route;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomAmenityController;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomController;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Plan quan-ly-phong-hop, Task 5 — Danh mục "Tiện nghi phòng họp"
    Route::group(['prefix' => 'meeting/room-amenities'], function () {
        // /getAll đặt TRƯỚC route wildcard /{meetingRoomAmenity}, nếu không bị nuốt.
        Route::get('/getAll', [MeetingRoomAmenityController::class, 'getAll']);
        Route::get('/', [MeetingRoomAmenityController::class, 'index'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp');
        Route::post('/', [MeetingRoomAmenityController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        Route::get('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'show']);
        Route::delete('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        Route::get('/{meetingRoomAmenity}/lock', [MeetingRoomAmenityController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
        Route::get('/{meetingRoomAmenity}/unlock', [MeetingRoomAmenityController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    });

    // Plan quan-ly-phong-hop, Task 6 — Danh mục "Phòng họp"
    Route::group(['prefix' => 'meeting/rooms'], function () {
        // Route tĩnh (/form-options) PHẢI đặt TRƯỚC wildcard /{meetingRoom}, nếu không bị nuốt.
        Route::get('/form-options', [MeetingRoomController::class, 'formOptions']);
        Route::get('/', [MeetingRoomController::class, 'index'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::post('/', [MeetingRoomController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}', [MeetingRoomController::class, 'show']);
        Route::delete('/{meetingRoom}', [MeetingRoomController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/lock', [MeetingRoomController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/unlock', [MeetingRoomController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/upcoming-bookings', [MeetingRoomController::class, 'upcomingBookings'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
    });
});
```

### e2e/tests/meeting/meeting-room.api.spec.ts
```ts
/**
 * E2E API — Danh mục "Phòng họp" (Task 6, plan quan-ly-phong-hop).
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): API ở :8001.
 * Token đọc từ e2e/.auth/api-wt.json (tài khoản CÓ quyền quản lý danh mục, employee id 34).
 * Ca "không quyền" dùng token của e2e/.auth/user-nocost-wt.json (tài khoản id 25).
 *
 * Phủ 5 ca theo brief:
 *   1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho
 *   2. tạo phòng là có sẵn checkin_qr_token
 *   3. gắn nhiều tiện nghi rồi đọc lại đúng danh sách
 *   4. form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty
 *   5. không quyền quản lý danh mục thì POST trả 403
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const ROOMS_URL = '/api/v1/meeting/rooms';
const AMENITIES_URL = '/api/v1/meeting/room-amenities';

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let noPermApi: APIRequestContext;
const createdRoomIds: number[] = [];
const createdAmenityIds: number[] = [];

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
});

test.afterAll(async () => {
  // Dọn dữ liệu test tạo ra — DB dùng chung với phiên khác.
  for (const id of createdRoomIds) {
    await api.delete(`${ROOMS_URL}/${id}`).catch(() => {});
  }
  for (const id of createdAmenityIds) {
    await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
  }
  await api?.dispose();
  await noPermApi?.dispose();
});

test('1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho', async () => {
  const created = await api.post(ROOMS_URL, {
    data: { code: 'E2E_A301', name: 'P.A301', company_id: 1 },
  });
  expect(created.status()).toBe(200);
  const createdBody = await created.json();
  createdRoomIds.push(createdBody.data.id);

  const dup = await api.post(ROOMS_URL, {
    data: { code: 'E2E_A301', name: 'Khác', company_id: 1 },
  });
  expect(dup.status()).toBe(422);
  expect(await dup.text()).toContain('code');

  const other = await api.post(ROOMS_URL, {
    data: { code: 'E2E_A301', name: 'P.A301 CT2', company_id: 2 },
  });
  expect(other.status()).toBe(200);
  const otherBody = await other.json();
  createdRoomIds.push(otherBody.data.id);
});

test('2. tạo phòng là có sẵn checkin_qr_token', async () => {
  const res = await api.post(ROOMS_URL, {
    data: { code: 'E2E_QR01', name: 'P.QR', company_id: 1 },
  });
  expect(res.status()).toBe(200);
  const id = (await res.json()).data.id;
  createdRoomIds.push(id);

  const detail = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  expect(detail.data.checkin_qr_token).toMatch(/^[0-9a-f-]{36}$/);
  expect(detail.data.is_can_edit).toBe(true);
  expect(detail.data.is_can_delete).toBe(true);
  expect(detail.data.is_can_lock).toBe(true);
  expect(detail.data.status_text).toBe('Hoạt động');
});

test('3. gắn nhiều tiện nghi rồi đọc lại đúng danh sách', async () => {
  const amenity1 = await api.post(AMENITIES_URL, { data: { code: 'E2E_RM_AM1', name: 'Máy chiếu E2E rooms' } });
  const amenity2 = await api.post(AMENITIES_URL, { data: { code: 'E2E_RM_AM2', name: 'Bảng trắng E2E rooms' } });
  expect(amenity1.status()).toBe(200);
  expect(amenity2.status()).toBe(200);
  const amenityId1 = (await amenity1.json()).data.id;
  const amenityId2 = (await amenity2.json()).data.id;
  createdAmenityIds.push(amenityId1, amenityId2);

  const created = await api.post(ROOMS_URL, {
    data: { code: 'E2E_AM_ROOM', name: 'P.Tiện nghi', company_id: 1, amenity_ids: [amenityId1, amenityId2] },
  });
  expect(created.status()).toBe(200);
  const id = (await created.json()).data.id;
  createdRoomIds.push(id);

  const detail = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  const returnedAmenityIds = (detail.data.amenities || []).map((a: any) => a.id).sort();
  expect(returnedAmenityIds).toEqual([amenityId1, amenityId2].sort());

  // Sửa lại chỉ còn 1 tiện nghi -> sync phải bỏ tiện nghi còn lại
  const updated = await api.post(ROOMS_URL, {
    data: { id, code: 'E2E_AM_ROOM', name: 'P.Tiện nghi', company_id: 1, amenity_ids: [amenityId1] },
  });
  expect(updated.status()).toBe(200);
  const detailAfterUpdate = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  const returnedAmenityIdsAfterUpdate = (detailAfterUpdate.data.amenities || []).map((a: any) => a.id);
  expect(returnedAmenityIdsAfterUpdate).toEqual([amenityId1]);
});

test('4. form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty', async () => {
  const res = await (await api.get(`${ROOMS_URL}/form-options`)).json();
  expect(res.data.config.open_time).toBeTruthy();
  expect(res.data.config.close_time).toBeTruthy();
  expect(typeof res.data.config.checkin_grace_minutes).toBe('number');
  expect(Array.isArray(res.data.amenities)).toBe(true);
  expect(Array.isArray(res.data.companies)).toBe(true);
  // Tiện nghi trả về đều đang hoạt động (status = 1)
  for (const amenity of res.data.amenities) {
    expect(amenity.status).toBe(1);
  }
});

test('5. không quyền quản lý danh mục thì POST trả 403', async () => {
  const res = await noPermApi.post(ROOMS_URL, {
    data: { code: 'E2E_NOPERM', name: 'X', company_id: 1 },
  });
  expect(res.status()).toBe(403);
});
```
