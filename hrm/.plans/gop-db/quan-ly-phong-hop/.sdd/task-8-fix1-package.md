# Re-review package — Task 8 fix round 1

## BE (worktree phong-hop-api)
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

    /**
     * Fix round 1 (review) — Resource cần `company_name` hiển thị ở màn danh sách/chi tiết.
     * Cùng nguồn `Modules\Human\Entities\Company` đang dùng ở `MeetingRoomService::formOptions()`.
     */
    public function company()
    {
        return $this->belongsTo(\Modules\Human\Entities\Company::class, 'company_id', 'id');
    }

    /**
     * Fix round 1 (review) — Resource cần `manager_name`. `manager_employee_id` trỏ tới
     * `employees.id` (khớp cách FE chọn nhân viên qua `$store.state.employees`, nạp từ
     * `Employee::getAll()`), KHÔNG phải `employee_infos.id`.
     *
     * ⚠️ Cố tình KHÔNG dùng `Employee::getAll(true)` (chỉ lấy nhân viên ĐANG làm việc) ở đây —
     * đây là quan hệ Eloquent đọc trực tiếp bằng khoá ngoại, phải trả đúng người quản lý đã lưu dù
     * người đó đã nghỉ việc, nếu không `manager_name` cho phòng có quản lý đã nghỉ sẽ lại rỗng y
     * hệt lỗi mà lần sửa này đang vá (FE trước đây tra theo state.employees, vốn lọc
     * `onlyActive = true`, nên bỏ sót đúng trường hợp này).
     */
    public function manager()
    {
        return $this->belongsTo(\Modules\Timesheet\Entities\Employee::class, 'manager_employee_id', 'id');
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
            // Fix round 1 (review) — FE trước đây tự tra tên công ty/người quản lý từ
            // $store.state.employees (chỉ chứa nhân viên ĐANG làm việc) nên phòng có quản lý đã
            // nghỉ việc hiện "—" dù dữ liệu còn nguyên. BE trả sẵn tên, tránh sai dữ liệu âm thầm.
            'company_name' => optional($this->company)->name,
            'department_id' => $this->department_id,
            'part_id' => $this->part_id,
            'allow_cross_company' => (bool) $this->allow_cross_company,
            'location' => $this->location,
            'capacity' => $this->capacity,
            'manager_employee_id' => $this->manager_employee_id,
            'manager_name' => optional($this->manager)->fullname,
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
 *
 * ⚠️ Fix round 1 (review, CRITICAL 1): `checkin_qr_token` là credential check-in bằng QR
 * (Phase 5) — vai trò chỉ có quyền "Xem danh mục phòng họp" (route `show` cho cả 2 quyền)
 * KHÔNG được thấy token, chỉ "Quản lý danh mục phòng họp" mới thấy. Defense-in-depth: BE tự
 * gate ở Resource, không dựa vào FE ẩn field.
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
            // Fix round 1 (review, đồng bộ với MeetingRoomResource) — tránh FE tự tra tên qua
            // $store.state.employees (chỉ có nhân viên đang làm việc, bỏ sót quản lý đã nghỉ).
            'company_name' => optional($this->company)->name,
            'department_id' => $this->department_id,
            'part_id' => $this->part_id,
            'allow_cross_company' => (bool) $this->allow_cross_company,
            'location' => $this->location,
            'capacity' => $this->capacity,
            'manager_employee_id' => $this->manager_employee_id,
            'manager_name' => optional($this->manager)->fullname,
            'require_approval' => (bool) $this->require_approval,
            'open_time' => $this->open_time,
            'close_time' => $this->close_time,
            'checkin_grace_minutes' => $this->checkin_grace_minutes,
            'checkin_qr_token' => $this->when(
                isCurrentEmployeeHasPermission('Quản lý danh mục phòng họp'),
                $this->checkin_qr_token
            ),
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
        // ⚠️ N+1 (review Task 3 + fix round 1 IMPORTANT 3 + fix round 1 mục "việc BE"):
        // `amenities` tránh N+1 khi Resource đọc quan hệ tiện nghi; `employee_create.info` /
        // `employee_update.info` tránh N+1 khi Resource đọc `employee_create_name` /
        // `employee_update_name`; `company` / `manager.info` tránh N+1 khi Resource đọc
        // `company_name` / `manager_name` (mới thêm — trước đây FE tự tra tên từ
        // $store.state.employees, bỏ sót quản lý đã nghỉ việc).
        $query = MeetingRoom::query()->select('meeting_rooms.*')
            ->with(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'manager.info']);

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

            // `company` / `manager.info` để DetailMeetingRoomResource đọc `company_name` /
            // `manager_name` ngay sau khi lưu mà không phải lazy-load (fix round 1, đồng bộ
            // với eager load trong index()).
            return $room->load(['amenities', 'company', 'manager.info']);
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
        // Fix round 1 IMPORTANT 3 + fix round 1 mục "việc BE": kèm employee_create/employee_update.info
        // tránh N+1 khi Resource đọc employee_create_name/employee_update_name; company/manager.info
        // tránh N+1 khi Resource đọc company_name/manager_name (xem MeetingRoomService::index()).
        $meetingRoom->load(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'manager.info']);

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

## FE (worktree phong-hop-client)
### pages/meeting/rooms/index.vue
```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <!-- Plan quan-ly-phong-hop, Task 8 — bộ lọc dùng V2BaseSmartFilterPanel (khác Task 7 dùng
                 V2BaseFilterPanel) vì màn này có 4 trường lọc nâng cao, cần nhãn floating gọn cho
                 chế độ "Tìm kiếm nâng cao" (brief yêu cầu riêng, không phải khuôn chung của phân hệ). -->
            <V2BaseSmartFilterPanel
                table="meeting_rooms"
                :filter-fields="filterFields"
                :filters="filters"
                :collapsed="filterCollapsed"
                :quickSearchValue="filters.keyword"
                quickSearchPlaceholder="Tìm theo mã, tên phòng, vị trí"
                :floating="true"
                @toggle-panel="toggleFilterPanel"
                @quick-search-change="handleQuickSearchChange"
                @filter-change="handleFilterChange"
                @search="handleSearch"
                @reset="handleReset"
            >
                <!-- Tiện nghi: chọn nhiều, không có type dựng sẵn trong V2BaseFilterFieldControl nên
                     tự render qua slot (giống mẫu `field-tags` của pages/assign/tasks/index.vue) -->
                <template #field-amenity_ids>
                    <V2BaseSelect
                        v-model="filters.amenity_ids"
                        :options="amenityOptions"
                        :extraSettings="{ multiple: true }"
                        placeholder="Chọn tiện nghi"
                        size="sm"
                        :allowClear="true"
                    />
                </template>
            </V2BaseSmartFilterPanel>

            <!-- DATA TABLE -->
            <V2BaseDataTable
                :data="tableData"
                :columns="tableColumns"
                :pagination="pagination"
                :loading="loading"
                :title="title"
                rowKey="id"
                itemLabel="phòng họp"
                emptyText="Không có dữ liệu phù hợp bộ lọc."
                @page-change="handlePageChange"
                @page-size-change="handlePageSizeChange"
            >
                <template #actions>
                    <V2BaseButton v-if="canManage" primary size="sm" class="mb-2" @click="createItem">
                        <template #prefix>
                            <i class="ri-add-line" style="font-size: 13px"></i>
                        </template>
                        Tạo mới
                    </V2BaseButton>
                </template>

                <!-- Custom code column -->
                <template #cell-code="{ item }">
                    <span class="field-line">{{ item.code }}</span>
                </template>

                <!-- Custom name column -->
                <template #cell-name="{ item }">
                    <V2BaseTitleSubInfo :title="item.name" titleClass="field-line" :titleBold="false">
                    </V2BaseTitleSubInfo>
                </template>

                <!-- Custom company column -->
                <template #cell-company_name="{ item }">
                    <span class="field-line">{{ item.company_name || '—' }}</span>
                </template>

                <!-- Custom location column -->
                <template #cell-location="{ item }">
                    <span class="field-line">{{ item.location || '—' }}</span>
                </template>

                <!-- Custom capacity column -->
                <template #cell-capacity="{ item }">
                    {{ item.capacity != null && item.capacity !== '' ? Number(item.capacity).toLocaleString('en-US') : '—' }}
                </template>

                <!-- Custom amenities column (chip) -->
                <template #cell-amenities="{ item }">
                    <div v-if="item.amenities && item.amenities.length" class="room-amenity-chips">
                        <span v-for="amenity in item.amenities" :key="amenity.id" class="room-amenity-chip">
                            <i v-if="amenity.icon" :class="amenity.icon"></i>
                            {{ amenity.name }}
                        </span>
                    </div>
                    <span v-else style="color: #6b7280">—</span>
                </template>

                <!-- Custom manager column -->
                <template #cell-manager_name="{ item }">
                    <span class="field-line">{{ item.manager_name || '—' }}</span>
                </template>

                <!-- Custom require_approval column -->
                <template #cell-require_approval="{ item }">
                    <V2BaseBadge :variant="item.require_approval ? 'brand' : 'muted'">
                        {{ item.require_approval ? 'Có' : 'Không' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom allow_cross_company column -->
                <template #cell-allow_cross_company="{ item }">
                    <V2BaseBadge :variant="item.allow_cross_company ? 'brand' : 'muted'">
                        {{ item.allow_cross_company ? 'Có' : 'Không' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom status column -->
                <template #cell-status="{ item }">
                    <V2BaseBadge :variant="item.status == 2 ? 'required' : 'brand'">
                        {{ item.status == 2 ? 'Khóa' : 'Hoạt động' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom actions column -->
                <template #cell-actions="{ item }">
                    <div class="d-flex align-items-center justify-content-center" style="gap: 8px">
                        <V2BaseIconButton size="sm" title="Xem" @click="() => viewItem(item)">
                            <i class="ri-eye-line"></i>
                        </V2BaseIconButton>
                        <V2BaseIconButton
                            v-if="canManage && item.is_can_edit"
                            size="sm"
                            title="Sửa"
                            @click="() => editItem(item)"
                        >
                            <i class="ri-edit-line"></i>
                        </V2BaseIconButton>
                        <!-- Khóa: có kiểm bookings sắp tới trước khi hỏi xác nhận (onLock) — Mở khóa
                             không cần kiểm, hỏi thẳng. -->
                        <V2BaseIconButton
                            v-if="canManage && (item.status == 2 || item.is_can_lock)"
                            size="sm"
                            :title="item.status == 2 ? 'Mở khóa phòng họp' : 'Khóa phòng họp'"
                            @click="() => onToggleLock(item)"
                        >
                            <i :class="item.status == 2 ? 'ri-lock-unlock-line' : 'ri-lock-line'"></i>
                        </V2BaseIconButton>
                        <!-- Ẩn hẳn (không dùng interactable+disabledTitle) khi phòng đã có phiếu đặt -->
                        <V2BaseIconButton
                            v-if="canManage && item.is_can_delete"
                            size="sm"
                            danger
                            title="Xóa"
                            @click="() => confirmDeleteItem(item)"
                        >
                            <i class="ri-delete-bin-6-line"></i>
                        </V2BaseIconButton>
                    </div>
                </template>
            </V2BaseDataTable>
        </div>

        <!-- Xác nhận xóa — thao tác phá huỷ dữ liệu nên bật `danger` (nút đỏ + icon cảnh báo) -->
        <BaseConfirmModal
            id="confirm-delete-meeting-room"
            title="Xác nhận xóa"
            :message="deleteConfirmMessage"
            text-close="Hủy"
            text-accept="Xóa"
            danger
            accept-icon="ri-delete-bin-line"
            @event="handleConfirmDeleteItem"
        />

        <!-- Meeting Room Modal -->
        <MeetingRoomModal
            ref="meetingRoomModal"
            :id="selectedItem ? selectedItem.id : null"
            :isShow="isShow"
            @event="eventHandler"
            @closeModal="handleCloseModal"
        />
    </div>
</template>
<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import V2BaseSmartFilterPanel from '@/components/V2BaseSmartFilterPanel.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import MeetingRoomModal from '@/pages/meeting/rooms/components/MeetingRoomModal.vue'
import { buildQuery } from '@/utils/url-action'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import CheckPermission from '@/utils/mixins/CheckPermission'

const initialStateForm = {
    page: 1,
    per_page: 10,
    keyword: '',
    company_id: '',
    capacity_from: '',
    amenity_ids: [],
    status: '',
}

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin, CheckPermission],
    head() {
        return {
            title: `${this.title}`,
        }
    },
    components: {
        V2BaseButton,
        V2BaseIconButton,
        V2BaseSmartFilterPanel,
        V2BaseSelect,
        V2BaseDataTable,
        V2BaseTitleSubInfo,
        V2BaseBadge,
        BaseConfirmModal,
        MeetingRoomModal,
    },
    data() {
        return {
            loading: false,
            title: 'Danh mục phòng họp',
            tableData: [],
            pagination: {
                currentPage: 1,
                pageSize: 10,
                total: 0,
                totalPages: 1,
                from: 0,
                to: 0,
            },

            filterCollapsed: true,
            filters: { ...initialStateForm },

            // Tuỳ chọn bộ lọc — tiện nghi lấy qua form-options (không có API riêng danh sách tiện
            // nghi active, dùng chung endpoint dựng form). Công ty đọc thẳng $store.state.companies
            // (đã có sẵn từ user-profile lúc đăng nhập), không cần gọi thêm API.
            amenityOptions: [],

            // Items for actions
            itemToDelete: null,
            selectedItem: null,
            isShow: false,

            // Filter watching
            ignoredFields: ['keyword'],
            oldFilters: {},

            // Status options
            statusOptions: [
                { id: 1, name: 'Hoạt động' },
                { id: 2, name: 'Khóa' },
            ],
        }
    },
    computed: {
        // Cờ quyền fail-closed: dùng helper có sẵn `hasAPermission()` (mixin CheckPermission,
        // reactive theo $store.state.permissions) thay vì tự gán 1 lần ở mounted() — đúng khuôn
        // màn song sinh `pages/meeting/room-amenities/index.vue` (fix round 1). Chỉ gate hiện/ẩn
        // nút (Tạo mới/Sửa/Xóa/Khóa); chặn vào URL trực tiếp do middleware toàn cục
        // `checkPermission.js` (tra registry menu, Task 9) lo, KHÔNG phải việc của page nên không
        // cần `canView` ở đây (đã bỏ, dead code — không dùng ở đâu trong template).
        canManage() {
            return this.hasAPermission('Quản lý danh mục phòng họp')
        },
        pageTitle() {
            return 'Danh mục phòng họp'
        },
        companyOptions() {
            return (this.$store.state.companies || []).map((c) => ({ id: c.id, name: c.name }))
        },
        filterFields() {
            return [
                {
                    key: 'company_id',
                    label: 'Công ty',
                    type: 'select',
                    options: this.companyOptions,
                    col: 3,
                    resetKeys: ['company_id'],
                },
                {
                    key: 'capacity_from',
                    label: 'Sức chứa tối thiểu',
                    type: 'number',
                    col: 3,
                    resetKeys: ['capacity_from'],
                },
                {
                    key: 'amenity_ids',
                    label: 'Tiện nghi',
                    variant: 'tags',
                    col: 3,
                    resetKeys: ['amenity_ids'],
                    inputCount: 1,
                },
                {
                    key: 'status',
                    label: 'Trạng thái',
                    type: 'select',
                    options: this.statusOptions,
                    col: 3,
                    resetKeys: ['status'],
                },
            ]
        },
        tableColumns() {
            return [
                {
                    key: 'code',
                    title: 'Mã',
                    width: '110px',
                    minWidth: '100px',
                    align: 'left',
                },
                {
                    key: 'name',
                    title: 'Tên phòng',
                    minWidth: '160px',
                    cellClass: 'text-wrap',
                    align: 'left',
                },
                {
                    key: 'company_name',
                    title: 'Công ty',
                    minWidth: '140px',
                    align: 'left',
                },
                {
                    key: 'location',
                    title: 'Vị trí',
                    minWidth: '120px',
                    align: 'left',
                },
                {
                    key: 'capacity',
                    title: 'Sức chứa',
                    width: '90px',
                    align: 'center',
                },
                {
                    key: 'amenities',
                    title: 'Tiện nghi',
                    minWidth: '200px',
                    align: 'left',
                },
                {
                    key: 'manager_name',
                    title: 'Người quản lý',
                    minWidth: '160px',
                    align: 'left',
                },
                {
                    key: 'require_approval',
                    title: 'Cần duyệt',
                    width: '90px',
                    align: 'center',
                },
                {
                    key: 'allow_cross_company',
                    title: 'Cho công ty khác đặt',
                    width: '130px',
                    align: 'center',
                },
                {
                    key: 'status',
                    title: 'Trạng thái',
                    width: '100px',
                    align: 'left',
                },
                {
                    key: 'actions',
                    title: 'Hành động',
                    width: '150px',
                    align: 'center',
                },
            ]
        },

        deleteConfirmMessage() {
            if (!this.itemToDelete) return ''
            return `Bạn có chắc muốn xóa phòng họp '${this.itemToDelete.name}'?`
        },
    },
    async mounted() {
        await Promise.all([this.loadData(), this.loadAmenityOptions()])

        if (this.$route.query.message) {
            this.$toasted.global.success({
                message: this.$route.query.message,
            })
        }
    },
    watch: {
        filters: {
            handler(newVal) {
                const shouldCallApi = !this.ignoredFields.some((field) => newVal[field] !== this.oldFilters[field])

                if (shouldCallApi) {
                    this.loadData()
                }

                this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            },
            deep: true,
        },
    },
    methods: {
        async loadAmenityOptions() {
            try {
                const body = await this.$store.dispatch('apiGetMethod', 'meeting/rooms/form-options')
                const options = body.data || {}
                this.amenityOptions = (options.amenities || []).map((a) => ({ id: a.id, name: a.name }))
            } catch (error) {
                console.error('Error loading amenity options:', error)
            }
        },

        // Data loading
        async loadData() {
            try {
                this.loading = true

                this.filters.page = this.pagination.currentPage
                this.filters.per_page = this.pagination.pageSize

                const { data, meta } = await this.$store.dispatch(
                    'apiGetMethod',
                    `meeting/rooms${buildQuery(this.filters)}`
                )

                this.tableData = data
                this.pagination.currentPage = meta.current_page
                this.pagination.pageSize = meta.per_page
                this.pagination.total = meta.total
                this.pagination.totalPages = meta.last_page
                this.pagination.from = meta.from
                this.pagination.to = meta.to
            } catch (error) {
                console.error('Error loading data:', error)
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
                }
            } finally {
                this.loading = false
            }
        },

        // Filter handlers
        toggleFilterPanel() {
            this.filterCollapsed = !this.filterCollapsed
        },

        handleQuickSearchChange(value) {
            this.filters.keyword = value
        },

        handleFilterChange({ key, value }) {
            this.filters[key] = value
        },

        async handleSearch() {
            this.pagination.currentPage = 1
            this.filters.page = 1
            this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            await this.loadData()
        },

        async handleReset() {
            this.filters = { ...initialStateForm }
            this.pagination.currentPage = 1
            this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            await this.loadData()
        },

        async handlePageChange(page) {
            this.pagination.currentPage = page
            this.filters.page = page
            await this.loadData()
        },

        async handlePageSizeChange(pageSize) {
            this.pagination.pageSize = pageSize
            this.filters.per_page = pageSize
            this.pagination.currentPage = 1
            this.filters.page = 1
            await this.loadData()
        },

        // CRUD operations
        createItem() {
            this.selectedItem = null
            this.isShow = false
            this.$refs.meetingRoomModal?.resetModal()
            this.$bvModal.show('modal-meeting-room')
        },

        async viewItem(item) {
            this.selectedItem = item
            this.isShow = true
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.meetingRoomModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-meeting-room')
            }
        },

        async editItem(item) {
            this.selectedItem = item
            this.isShow = false
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.meetingRoomModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-meeting-room')
            }
        },

        // Khóa phòng: kiểm phiếu sắp tới trước, nội dung cảnh báo ghi rõ số phiếu (yêu cầu riêng
        // của Task 8, brief bước 4).
        async onLock(room) {
            try {
                const { data } = await this.$store.dispatch(
                    'apiGetMethod',
                    `meeting/rooms/${room.id}/upcoming-bookings`
                )
                const message =
                    data.count > 0
                        ? `Phòng còn ${Number(data.count).toLocaleString(
                              'en-US'
                          )} phiếu đặt sắp tới. Khóa phòng sẽ gửi thông báo cho người đặt để đổi phòng. Bạn chắc chắn khóa?`
                        : 'Bạn chắc chắn muốn khóa phòng họp này?'

                const ok = await this.$confirm({
                    title: 'Khóa phòng họp',
                    message,
                    textAccept: 'Khóa',
                    danger: true,
                    acceptIcon: 'ri-lock-line',
                })
                if (!ok) return

                await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/lock`)
                this.$toasted?.global?.success?.({ message: 'Khóa phòng họp thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error locking room:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage =
                    status === 404
                        ? 'Dữ liệu đã thay đổi, vui lòng tải lại'
                        : error?.response?.data?.message || 'Khóa phòng họp thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        async onUnlock(room) {
            try {
                const ok = await this.$confirm({
                    title: 'Mở khóa phòng họp',
                    message: 'Bạn có chắc muốn mở khóa phòng họp này?',
                    textAccept: 'Mở khóa',
                    acceptIcon: 'ri-lock-unlock-line',
                })
                if (!ok) return

                await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/unlock`)
                this.$toasted?.global?.success?.({ message: 'Mở khóa phòng họp thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error unlocking room:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage = error?.response?.data?.message || 'Mở khóa phòng họp thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        async onToggleLock(room) {
            if (room.status == 2) {
                await this.onUnlock(room)
            } else {
                await this.onLock(room)
            }
        },

        async deleteItem(item) {
            try {
                await this.$store.dispatch('apiDelete', `meeting/rooms/${item.id}`)
                this.$toasted?.global?.success?.({ message: 'Xóa thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error deleting item:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage =
                    status === 404
                        ? 'Dữ liệu đã thay đổi, vui lòng tải lại'
                        : error?.response?.data?.message || 'Xóa thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        // Confirm modals
        confirmDeleteItem(item) {
            this.itemToDelete = item
            this.$bvModal.show('confirm-delete-meeting-room')
        },

        async handleConfirmDeleteItem() {
            if (!this.itemToDelete) return

            await this.deleteItem(this.itemToDelete)
            this.itemToDelete = null
        },

        // Event handler for modal
        async eventHandler() {
            this.selectedItem = null
            this.isShow = false
            await this.loadData()
        },

        handleCloseModal() {
            this.selectedItem = null
            this.isShow = false
            this.$bvModal.hide('modal-meeting-room')
        },
    },
}
</script>
<style lang="scss">
@import '@/assets/scss/v2-styles.scss';

.room-amenity-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.room-amenity-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 999px;
    background: #f0fdfa;
    border: 1px solid #ccfbf1;
    color: #0f766e;
    font-size: 11px;
    white-space: nowrap;
}
</style>
```

### pages/meeting/rooms/components/MeetingRoomModal.vue
```vue
<template>
    <!--
        Plan quan-ly-phong-hop, Task 8 — popup Thêm / Sửa / Xem phòng họp.
        Khuôn copy từ `pages/meeting/room-amenities/components/RoomAmenityModal.vue` (Task 7),
        thêm nhóm Công ty/Vị trí/Sức chứa/Người quản lý + Tiện nghi (chọn nhiều) + 2 cờ cài đặt.
        `form-options` chỉ gọi 1 lần MỖI LẦN MỞ modal (hook @show = onModalShow), KHÔNG gọi ở
        mounted() — brief Task 8 bước 3.
    -->
    <V2BaseModal
        ref="modal"
        modal-id="modal-meeting-room"
        :title="modalTitle"
        icon="ri-door-open-line"
        size="lg"
        @show="onModalShow"
        @shown="onUnsavedModalShown"
        @hide="onUnsavedModalHide"
        @hidden="onHidden"
    >
        <V2BaseFormSection title="Thông tin chung">
            <div class="form-row">
                <div class="col-md-4 mb-3">
                    <V2BaseLabel required>Mã phòng</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.code"
                        placeholder="VD: A301"
                        size="sm"
                        maxlength="50"
                        :disabled="isShow"
                        :invalid="!!error.code"
                    />
                    <V2BaseError v-if="error.code" :message="error.code" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-8 mb-3">
                    <V2BaseLabel required>Tên phòng</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.name"
                        placeholder="VD: Phòng họp tầng 3"
                        size="sm"
                        maxlength="255"
                        :disabled="isShow"
                        :invalid="!!error.name"
                    />
                    <V2BaseError v-if="error.name" :message="error.name" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-6 mb-3">
                    <V2BaseLabel required>Công ty</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.company_id"
                        :options="companyOptions"
                        placeholder="Chọn công ty"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="false"
                        :invalid="!!error.company_id"
                    />
                    <V2BaseError v-if="error.company_id" :message="error.company_id" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-6 mb-3">
                    <V2BaseLabel>Vị trí</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.location"
                        placeholder="VD: Tầng 3, tòa nhà A"
                        size="sm"
                        maxlength="255"
                        :disabled="isShow"
                        :invalid="!!error.location"
                    />
                    <V2BaseError v-if="error.location" :message="error.location" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-4 mb-3">
                    <V2BaseLabel>Sức chứa</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.capacity"
                        type="number"
                        min="0"
                        placeholder="VD: 10"
                        size="sm"
                        :disabled="isShow"
                        :invalid="!!error.capacity"
                    />
                    <V2BaseError v-if="error.capacity" :message="error.capacity" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-8 mb-3">
                    <V2BaseLabel>Người quản lý</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.manager_employee_id"
                        :options="employeeOptions"
                        placeholder="Chọn người quản lý"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="true"
                        :invalid="!!error.manager_employee_id"
                    />
                    <V2BaseError
                        v-if="error.manager_employee_id"
                        :message="error.manager_employee_id"
                        size="sm"
                        class="mb-0 mt-1"
                    />
                </div>
            </div>
        </V2BaseFormSection>

        <V2BaseFormSection title="Tiện nghi & cài đặt đặt phòng" class="mt-3">
            <div class="form-row">
                <div class="col-md-12 mb-3">
                    <V2BaseLabel>Tiện nghi</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.amenity_ids"
                        :options="amenityOptions"
                        :extraSettings="{ multiple: true }"
                        placeholder="Chọn tiện nghi phòng họp"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="true"
                    />
                    <V2BaseError v-if="error.amenity_ids" :message="error.amenity_ids" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-6 mb-1">
                    <div class="d-flex align-items-center" style="gap: 8px">
                        <V2BaseCheckbox v-model="data.require_approval" :disabled="isShow" />
                        <span class="mb-0" style="cursor: pointer" @click="toggleRequireApproval">
                            Cần duyệt trước khi đặt
                        </span>
                    </div>
                </div>

                <div class="col-md-6 mb-1">
                    <div class="d-flex align-items-center" style="gap: 8px">
                        <V2BaseCheckbox v-model="data.allow_cross_company" :disabled="isShow" />
                        <span class="mb-0" style="cursor: pointer" @click="toggleAllowCrossCompany">
                            Cho công ty khác đặt
                        </span>
                    </div>
                </div>
            </div>
        </V2BaseFormSection>

        <V2BaseFormSection title="Mô tả" class="mt-3">
            <div class="form-row">
                <div class="col-md-12 mb-1">
                    <V2BaseTextarea
                        v-model="data.description"
                        placeholder="Ghi chú thêm về phòng họp"
                        size="sm"
                        :disabled="isShow"
                        style="min-height: 72px; resize: vertical"
                    />
                    <V2BaseError v-if="error.description" :message="error.description" size="sm" class="mb-0 mt-1" />
                </div>
            </div>
        </V2BaseFormSection>

        <V2BaseError v-if="formError" :message="formError" size="sm" class="mb-0 mt-2" />

        <template #footer>
            <V2BaseButton v-if="!isShow" primary size="sm" :interactable="!isSubmitSave" @click="submitSave(false)">
                <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
                Lưu
            </V2BaseButton>
            <V2BaseButton
                v-if="!id && !isShow"
                secondary
                size="sm"
                :interactable="!isSubmitSave"
                @click="submitSave(true)"
            >
                <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
                Lưu và tiếp tục
            </V2BaseButton>
            <V2BaseButton tertiary size="sm" @click="closeModal">
                <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                Đóng
            </V2BaseButton>
        </template>
    </V2BaseModal>
</template>

<script>
import V2BaseModal from '@/components/modal/V2BaseModal.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseCheckbox from '@/components/V2BaseCheckbox.vue'
import V2BaseTextarea from '@/components/V2BaseTextarea.vue'
import V2BaseError from '@/components/V2BaseError.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseFormSection from '@/components/V2BaseFormSection.vue'
import unsavedModalMixin from '@/utils/mixins/unsavedModalMixin'
import { employeeOptionText } from '@/utils/employeeOptionText'

const emptyData = () => ({
    code: '',
    name: '',
    company_id: null,
    location: '',
    capacity: '',
    manager_employee_id: null,
    amenity_ids: [],
    require_approval: false,
    allow_cross_company: false,
    description: '',
})

export default {
    components: {
        V2BaseModal,
        V2BaseInput,
        V2BaseLabel,
        V2BaseSelectInModal,
        V2BaseCheckbox,
        V2BaseTextarea,
        V2BaseError,
        V2BaseButton,
        V2BaseFormSection,
    },
    mixins: [unsavedModalMixin],
    props: {
        id: { type: Number, default: null },
        isShow: { type: Boolean, default: false },
    },
    data() {
        return {
            data: emptyData(),
            error: {},
            formError: '',
            isSubmitSave: false,
            // form-options: tiện nghi + công ty — nạp 1 lần MỖI LẦN modal mở (xem onModalShow).
            amenityOptions: [],
            companyOptions: [],
            // Fix round 1 (Minor 3) — guard chống gọi trùng: đã đo thấy `@show` của
            // b-modal/V2BaseModal thỉnh thoảng bắn form-options 2 lần khi mở modal (nguyên nhân
            // gốc chưa tái hiện được, không phải do code màn này gây ra). Guard rẻ, tự vệ —
            // KHÔNG đụng V2BaseModal.vue.
            loadingFormOptions: false,
        }
    },
    computed: {
        modalTitle() {
            if (this.isShow) return 'Xem phòng họp'
            return this.id ? 'Sửa phòng họp' : 'Thêm phòng họp'
        },
        // Nhân viên đã có sẵn trong $store.state.employees (nạp lúc đăng nhập, xem
        // store/actions.js) — không cần gọi thêm API riêng cho ô "Người quản lý".
        // Nhãn theo khuôn chuẩn `utils/employeeOptionText.js`.
        employeeOptions() {
            return (this.$store.state.employees || []).map((employee) => ({
                id: employee.id,
                name: employeeOptionText(employee),
            }))
        },
    },
    watch: {
        id: {
            handler(newId) {
                if (!newId) {
                    this.data = emptyData()
                    this.error = {}
                    this.formError = ''
                }
            },
            immediate: false,
        },
    },
    methods: {
        // Cảnh báo "chưa lưu" (utils/mixins/unsavedModalMixin.js) theo dõi this.data,
        // modal ref="modal" khớp mặc định unsavedModalRef() nhưng vẫn khai rõ cho dễ đọc.
        unsavedSnapshotSource() {
            return this.data
        },
        unsavedModalRef() {
            return 'modal'
        },

        async onModalShow() {
            if (!this.id) {
                this.resetLocalData()
            }
            // 1 request duy nhất, gọi ở đây (lúc modal MỞ), KHÔNG gọi ở mounted() — brief Task 8
            // bước 3: tránh gọi lại API mỗi lần component modal được dựng lên nhưng chưa mở.
            await this.loadFormOptions()
        },

        async loadFormOptions() {
            if (this.loadingFormOptions) return
            this.loadingFormOptions = true
            try {
                const body = await this.$store.dispatch('apiGetMethod', 'meeting/rooms/form-options')
                const options = body.data || {}
                this.amenityOptions = (options.amenities || []).map((amenity) => ({
                    id: amenity.id,
                    name: amenity.name,
                }))
                this.companyOptions = (options.companies || []).map((company) => ({
                    id: company.id,
                    name: company.name,
                }))
            } catch (error) {
                console.error('Error loading form options:', error)
                this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu dựng form' })
            } finally {
                this.loadingFormOptions = false
            }
        },

        resetLocalData() {
            this.data = emptyData()
            this.error = {}
            this.formError = ''
        },

        resetModal() {
            this.error = {}
            this.formError = ''
            if (!this.id) {
                this.resetLocalData()
            }
        },

        toggleRequireApproval() {
            if (this.isShow) return
            this.data.require_approval = !this.data.require_approval
        },

        toggleAllowCrossCompany() {
            if (this.isShow) return
            this.data.allow_cross_company = !this.data.allow_cross_company
        },

        async loadData(id) {
            try {
                const response = await this.$store.dispatch('apiGet', `meeting/rooms/${id}`)
                const detail = response.data.data
                this.data = {
                    code: detail.code || '',
                    name: detail.name || '',
                    company_id: detail.company_id ?? null,
                    location: detail.location || '',
                    capacity: detail.capacity ?? '',
                    manager_employee_id: detail.manager_employee_id ?? null,
                    amenity_ids: (detail.amenities || []).map((amenity) => amenity.id),
                    require_approval: !!detail.require_approval,
                    allow_cross_company: !!detail.allow_cross_company,
                    description: detail.description || '',
                }
                // Modal show() gọi TRƯỚC khi load xong -> @shown đã chốt mốc trên form rỗng.
                // Chốt lại ở đây để dữ liệu detail vừa nạp không bị tính nhầm là user vừa sửa.
                this.$nextTick(() => this.markFormPristine())
                return true
            } catch (error) {
                console.error('Error loading data:', error)
                const status = Number(error?.response?.status)
                let errorMessage = 'Lỗi khi tải dữ liệu'

                if (status === 403) return false
                if (status === 404) errorMessage = 'Dữ liệu đã thay đổi, vui lòng tải lại'
                else if (error?.response?.data?.message) errorMessage = error.response.data.message

                this.$toasted?.global?.error?.({ message: errorMessage })
                return false
            }
        },

        closeModal() {
            this.$refs.modal?.close()
        },

        /** V2BaseModal phát `hidden` sau khi popup đóng hẳn — dọn state ở đây, không cần setTimeout */
        onHidden() {
            this.resetLocalData()
            this.$emit('closeModal')
        },

        async submitSave(continueAfterSave = false) {
            if (this.isSubmitSave) return
            this.isSubmitSave = true
            this.error = {}
            this.formError = ''

            try {
                const payload = {
                    code: (this.data.code || '').trim(),
                    name: (this.data.name || '').trim(),
                    company_id: this.data.company_id,
                    location: (this.data.location || '').trim(),
                    capacity: this.data.capacity === '' || this.data.capacity === null ? null : Number(this.data.capacity),
                    manager_employee_id: this.data.manager_employee_id || null,
                    amenity_ids: this.data.amenity_ids || [],
                    require_approval: !!this.data.require_approval,
                    allow_cross_company: !!this.data.allow_cross_company,
                    description: (this.data.description || '').trim(),
                }
                if (this.id) payload.id = this.id

                await this.$store.dispatch('apiPostMethod', { url: 'meeting/rooms', payload })

                const message = this.id ? 'Cập nhật thành công' : 'Thêm mới thành công'
                this.$toasted?.global?.success?.({ message })
                this.markFormSaved()
                this.$emit('event')

                if (continueAfterSave) {
                    this.resetModal()
                    this.$nextTick(() => this.markFormPristine())
                } else {
                    this.closeModal()
                }
            } catch (error) {
                console.error('Error saving meeting room:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const payload = error?.response?.data
                if (status === 422 && payload?.errors) {
                    this.error = payload.errors
                    this.formError = 'Bạn chưa nhập đầy đủ thông tin'
                } else if (status === 404) {
                    this.formError = 'Dữ liệu đã thay đổi, vui lòng tải lại'
                    this.$toasted?.global?.error?.({ message: this.formError })
                } else {
                    this.formError = payload?.message || (this.id ? 'Cập nhật thất bại' : 'Thêm mới thất bại')
                    this.$toasted?.global?.error?.({ message: this.formError })
                }
            } finally {
                this.isSubmitSave = false
            }
        },
    },
}
</script>
```

### e2e/tests/meeting/_room-ui.smoke.spec.ts
```ts
/**
 * SMOKE UI — Danh mục "Phòng họp" (Task 8, plan quan-ly-phong-hop).
 * Tạm thời (Task 10 sẽ viết bộ e2e chính thức) — chỉ verify khuôn UI chạy được thật trên browser:
 * mở màn -> tạo 1 phòng gắn 2 tiện nghi qua modal -> khóa -> xóa, đo bằng số/text lấy từ DOM.
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): Nuxt ở :3001, API ở :8001.
 * Chạy: PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 \
 *   API_BASE=http://127.0.0.1:8001 npx playwright test _room-ui.smoke --project=chromium --no-deps --workers=1
 *
 * Môi trường này KHÔNG có sẵn tiện nghi phòng họp nào (đã kiểm: GET meeting/room-amenities trả
 * data rỗng) -> phải tự tạo 2 tiện nghi qua API trong beforeAll rồi mới gắn được vào form.
 *
 * CẤM chờ `networkidle` (app polling nền) — chờ mốc DOM cụ thể.
 *
 * Fix round 1 (review) — IMPORTANT 2: phòng test trước đây chỉ được xóa ở BƯỚC CUỐI của test (happy
 * path) — fail ở bước Khóa hoặc bước đo badge thì bản ghi `E2EUI_RM_<ts>` nằm lại vĩnh viễn trong DB
 * dùng chung. Áp lại đúng khuôn `_room-amenity-ui.smoke.spec.ts` (fix round 1 của Task 7):
 *   - `beforeAll` quét xóa rác `E2EUI_` (cả rooms lẫn amenities) còn sót từ lần chạy trước bị kill
 *     giữa chừng, TRƯỚC KHI tạo dữ liệu setup của lần chạy này.
 *   - `afterEach` xóa phòng + 2 tiện nghi của CHÍNH lần chạy này (theo mã `CODE`/`AM1_CODE`/
 *     `AM2_CODE`) — chạy dù ca pass hay fail, không phụ thuộc happy path.
 *   - Bước 3 (Xóa qua UI) ở cuối test GIỮ NGUYÊN — đó là việc test hành vi UI thật; `afterEach` chỉ
 *     là lưới an toàn khi ca fail trước khi tới được bước đó.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.use({ storageState: '.auth/user-wt.json' });

test.describe.configure({ mode: 'serial' });

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const ROOMS_URL = '/api/v1/meeting/rooms';
const AMENITIES_URL = '/api/v1/meeting/room-amenities';

const RUN_SUFFIX = Date.now();
const CODE = `E2EUI_RM_${RUN_SUFFIX}`;
const NAME = `Phòng họp E2E UI ${RUN_SUFFIX}`;
const AM1_CODE = `E2EUI_AM1_${RUN_SUFFIX}`;
const AM1_NAME = `Tiện nghi E2E UI 1 ${RUN_SUFFIX}`;
const AM2_CODE = `E2EUI_AM2_${RUN_SUFFIX}`;
const AM2_NAME = `Tiện nghi E2E UI 2 ${RUN_SUFFIX}`;

const ROOMS_LIST_GET_RE = /\/api\/v1\/meeting\/rooms(\?|$)/;

let api: APIRequestContext;
const amenityIds: number[] = [];

/** Xóa mọi bản ghi `code` bắt đầu bằng `prefix` trong `resourceUrl`, lặp theo trang cho tới khi hết
 *  (khuôn copy từ `_room-amenity-ui.smoke.spec.ts::deleteByCodePrefix` / `room-amenity.api.spec.ts`).
 *  Dùng cho CẢ dọn rác lần chạy trước (beforeAll, prefix rộng `E2EUI_`) LẪN dọn bản ghi của chính
 *  lần chạy này (afterEach, prefix hẹp = mã chính xác). */
async function deleteByCodePrefix(resourceUrl: string, prefix: string) {
  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${resourceUrl}?keyword=${encodeURIComponent(prefix)}&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const ids = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith(prefix))
      .map((r: any) => r.id);
    if (ids.length === 0) break;
    for (const id of ids) {
      await api.delete(`${resourceUrl}/${id}`).catch(() => {});
    }
  }
}

test.beforeAll(async () => {
  const token = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
  api = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${token}` },
  });

  // Dọn rác của LẦN CHẠY TRƯỚC bị kill giữa chừng — phòng trước (FK tới tiện nghi qua pivot),
  // tiện nghi sau.
  await deleteByCodePrefix(ROOMS_URL, 'E2EUI_');
  await deleteByCodePrefix(AMENITIES_URL, 'E2EUI_');

  // Setup dữ liệu: tạo 2 tiện nghi active để có option gắn vào phòng trong modal.
  for (const [code, name] of [
    [AM1_CODE, AM1_NAME],
    [AM2_CODE, AM2_NAME],
  ]) {
    const res = await api.post(AMENITIES_URL, { data: { code, name } });
    expect(res.status(), `tạo tiện nghi setup ${code}`).toBe(200);
    const body = await res.json();
    amenityIds.push(body.data.id);
  }
});

test.afterEach(async () => {
  // Chạy dù ca pass hay fail — phòng + tiện nghi của LẦN CHẠY NÀY không được để lại DB dùng chung.
  // Xóa phòng TRƯỚC tiện nghi (FK qua bảng pivot amenities).
  await deleteByCodePrefix(ROOMS_URL, CODE);
  for (const id of amenityIds) {
    await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
  }
});

test.afterAll(async () => {
  await api?.dispose();
});

/**
 * Chờ ô select (bọc trong 1 element chứa `wrapperText`) có ĐỦ option nạp xong.
 *
 * KHÔNG đủ nếu chỉ chờ response GET `form-options`: server dev (`artisan serve`, đơn luồng) xử lý
 * chậm khi có nhiều request xếp hàng — đã đo thực tế response về sau 2-6s dù network log báo 200
 * gần như ngay. Đợi thẳng DOM (`<select>.options.length`) mới là mốc đúng, không đoán thời gian.
 */
async function waitForSelectOptions(page: import('@playwright/test').Page, wrapperClass: string, wrapperText: string, minOptions = 1) {
  await page.waitForFunction(
    ({ wrapperClass, wrapperText, minOptions }) => {
      const wraps = [...document.querySelectorAll(`#modal-meeting-room ${wrapperClass}`)];
      const wrap = wraps.find((el) => (el.textContent || '').includes(wrapperText));
      const select = wrap ? wrap.querySelector('select') : null;
      return !!select && select.options.length >= minOptions;
    },
    { wrapperClass, wrapperText, minOptions },
    { timeout: 20000 },
  );
}

/**
 * Bấm mở dropdown select2, có RETRY — đã đo thấy đôi lúc 1 cú click không làm dropdown mở (server
 * dev đơn luồng làm event loop / render bận), khiến bước chọn option sau đó timeout. Thử lại vài
 * lần thay vì tăng timeout suông cho 1 click.
 */
async function openSelect2(page: import('@playwright/test').Page, fieldLocator: import('@playwright/test').Locator) {
  for (let attempt = 0; attempt < 5; attempt++) {
    await fieldLocator.locator('.select2-selection').click();
    try {
      await page.locator('.select2-container--open').first().waitFor({ state: 'visible', timeout: 3000 });
      return;
    } catch (e) {
      // thử lại
    }
  }
  throw new Error('select2 dropdown không mở được sau 5 lần thử');
}

/**
 * Mở dropdown rồi chọn 1 option theo text hiển thị, có RETRY toàn bộ thao tác mở+chọn.
 *
 * Gõ vào ô tìm kiếm của dropdown để LỌC danh sách còn đúng 1-2 dòng trước khi click — môi trường
 * này có dữ liệu tiện nghi cũ (đợt debug trước) lẫn trong danh mục, danh sách dài/phải cuộn làm
 * click theo text không ổn định. Gõ lọc tránh hẳn việc phải cuộn hay đoán vị trí.
 */
async function pickSelect2Option(
  page: import('@playwright/test').Page,
  fieldLocator: import('@playwright/test').Locator,
  optionText: string | null,
) {
  for (let attempt = 0; attempt < 3; attempt++) {
    await openSelect2(page, fieldLocator);
    if (optionText) {
      const searchField = page.locator('.select2-container--open .select2-search__field').first();
      await searchField.fill(optionText);
    }
    const option = optionText
      ? page.locator('.select2-container--open li.select2-results__option', { hasText: optionText }).first()
      : page.locator('.select2-container--open li.select2-results__option:not(.select2-results__message)').first();
    try {
      await option.click({ timeout: 5000 });
      return;
    } catch (e) {
      // Thử lại bằng cách mở lại dropdown ở vòng sau — TUYỆT ĐỐI không nhấn Escape ở đây: modal
      // dùng unsavedModalMixin bắt phím Escape để hỏi "Thông tin chưa lưu", popup đó che kín màn
      // hình và làm mọi click sau đứng hình (đã đo trúng lỗi này).
    }
  }
  throw new Error(`Không chọn được option "${optionText}" sau 3 lần thử`);
}

test('CRUD phòng họp qua UI: tạo kèm 2 tiện nghi - khóa - xóa', async ({ page }) => {
  test.setTimeout(90000); // server dev đơn luồng, form-options có lúc mất vài giây mới về

  await page.goto('/meeting/rooms');

  const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
  // Server dev đơn luồng — lần vào màn đầu tiên có lúc chậm hơn 5s mặc định.
  await expect(searchBox).toBeVisible({ timeout: 20000 });

  const rows = page.locator('table.data-table tbody tr');

  // 0. Lọc theo mã duy nhất của lần chạy này -> baseline PHẢI là 0 dòng dữ liệu thật.
  await searchBox.fill(CODE);
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    searchBox.press('Enter'),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  await expect(rows).toHaveCount(1); // 1 dòng placeholder "Không có dữ liệu..."

  // 1. Tạo mới qua modal — @show gọi form-options (công ty + tiện nghi) 1 lần.
  await page.getByRole('button', { name: 'Tạo mới' }).click();
  const modal = page.locator('#modal-meeting-room');
  await expect(modal).toBeVisible();

  await modal.getByPlaceholder('VD: A301').fill(CODE);
  await modal.getByPlaceholder('VD: Phòng họp tầng 3').fill(NAME);

  // Công ty (bắt buộc) — chọn option đầu tiên, không lệ thuộc công ty cụ thể nào. Chờ options nạp
  // xong TRÊN DOM (không đoán theo thời gian network) rồi mới click.
  const companyField = modal.locator('.col-md-6.mb-3').filter({ hasText: 'Công ty' });
  await waitForSelectOptions(page, '.col-md-6.mb-3', 'Công ty', 1);
  await pickSelect2Option(page, companyField, null);

  await modal.getByPlaceholder('VD: Tầng 3, tòa nhà A').fill('Tầng 5, tòa nhà E2E');
  await modal.getByPlaceholder('VD: 10').fill('12');

  // Tiện nghi — chọn nhiều, chọn đúng 2 tiện nghi vừa setup ở beforeAll (khớp theo TÊN, không lệ
  // thuộc dữ liệu có sẵn trong môi trường). ⚠️ Đã đo: dropdown TỰ ĐÓNG sau mỗi lần chọn (khác hành
  // vi mặc định select2 multi) -> phải mở lại dropdown trước khi chọn tiện nghi thứ 2.
  const amenityField = modal.locator('.col-md-12.mb-3').filter({ hasText: 'Tiện nghi' }).first();
  await waitForSelectOptions(page, '.col-md-12.mb-3', 'Tiện nghi', 2);
  await pickSelect2Option(page, amenityField, AM1_NAME);
  await pickSelect2Option(page, amenityField, AM2_NAME);
  // Đóng dropdown — bấm ra vùng trống trong thân modal.
  await modal.locator('.v2-modal-body').click({ position: { x: 5, y: 5 } });

  // Lưu — nút đầu tiên trong footer luôn là "Lưu" (khuôn footer: Lưu / Lưu và tiếp tục / Đóng).
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    modal.locator('.v2-modal-footer button').first().click(),
  ]);
  await expect(modal).toBeHidden();

  // Đo bằng DOM: bảng phải tăng đúng 1 dòng so với baseline (0 -> 1 bản ghi thật)
  await expect(rows).toHaveCount(1);
  const row = rows.first();
  await expect(row).toContainText(CODE);
  await expect(row).toContainText(NAME);

  // Đo số chip tiện nghi trên dòng vừa tạo — cột "Tiện nghi" là cột thứ 6 (Mã, Tên phòng, Công ty,
  // Vị trí, Sức chứa, Tiện nghi, ...).
  const chips = row.locator('td:nth-child(6) .room-amenity-chip');
  await expect(chips).toHaveCount(2);

  // Badge trạng thái là cột thứ 10 (... Cần duyệt, Cho công ty khác đặt, Trạng thái, Hành động) —
  // dòng còn có 2 badge Có/Không khác nên KHÔNG dùng `.v2-badge` chung chung.
  const statusBadge = row.locator('td:nth-child(10) .v2-badge');
  await expect(statusBadge).toHaveText('Hoạt động');

  // 2. Khóa — popup xác nhận render bằng plugin $confirm() (base-confirm-modal.vue, id ngẫu nhiên
  // sinh lúc runtime) -> lọc theo tiêu đề thay vì id cố định.
  await row.getByTitle('Khóa phòng họp').click();
  const lockConfirm = page.locator('.modal-content').filter({ hasText: 'Khóa phòng họp' });
  await expect(lockConfirm).toBeVisible();
  // Phòng vừa tạo chưa có phiếu đặt nào -> đúng nhánh "không có phiếu" của onLock().
  await expect(lockConfirm).toContainText('Bạn chắc chắn muốn khóa phòng họp này?');
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    lockConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(statusBadge).toHaveText('Khóa');

  // 3. Xóa — dọn sạch dữ liệu test qua UI (happy path). `afterEach` ở trên là lưới an toàn nếu ca
  // fail trước bước này (phòng đã khóa nhưng chưa từng có phiếu đặt -> vẫn is_can_delete).
  await row.getByTitle('Xóa').click();
  const deleteConfirm = page.locator('#confirm-delete-meeting-room');
  await expect(deleteConfirm).toBeVisible();
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    deleteConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  await expect(rows).toHaveCount(1); // trở lại 1 dòng placeholder rỗng — đã dọn sạch
});
```
