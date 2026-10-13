# Re-review package — đợt fix sau review tổng (A→H)

## Migration mới
### phong-hop-api/Modules/Meeting/Database/Migrations/2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table.php
```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

/**
 * Fix đợt review tổng Phase 1 "Quản lý phòng họp" — mục A + H.
 *
 * A.3: pivot `meeting_room_room_amenity` không có FK -> `MeetingRoomService::destroy()` xóa
 * phòng mà không `detach()` tiện nghi để lại dòng mồ côi vĩnh viễn (đã đo: 78 dòng trước khi
 * sửa). Dòng mồ côi làm `MeetingRoomAmenityController::index()` đếm nhầm (JOIN thô theo
 * `meeting_room_amenity_id`) khiến tiện nghi từng gắn phòng đã xóa bị khóa nút Xóa vĩnh viễn dù
 * `isCanDelete()` (join `meeting_rooms`) nói ngược lại.
 *
 * PHẢI dọn sạch dòng mồ côi TRƯỚC khi thêm FK, nếu không migration lỗi ngay khi tạo constraint.
 *
 * H: `meeting_room_bookings.code` chưa có ràng buộc unique. Bảng đang 0 dòng (Phase 2 chưa sinh
 * phiếu) nên thêm unique bây giờ là miễn phí — để dành sau, 2 request song song sinh trùng mã
 * `DPH-YYYY-NNNNN` sẽ không có gì cản.
 */
class AddForeignKeysToMeetingRoomRoomAmenityTable extends Migration
{
    public function up()
    {
        // Dọn dòng mồ côi 2 chiều TRƯỚC khi thêm FK (câu lệnh giống hệt câu đã dùng để đo trước/sau
        // trong báo cáo đợt fix — chỉ xóa đúng dòng mồ côi, không đụng dòng còn hợp lệ).
        DB::statement(
            'DELETE p FROM meeting_room_room_amenity p '
            . 'LEFT JOIN meeting_rooms r ON r.id = p.meeting_room_id '
            . 'WHERE r.id IS NULL'
        );
        DB::statement(
            'DELETE p FROM meeting_room_room_amenity p '
            . 'LEFT JOIN meeting_room_amenities a ON a.id = p.meeting_room_amenity_id '
            . 'WHERE a.id IS NULL'
        );

        Schema::table('meeting_room_room_amenity', function (Blueprint $table) {
            $table->foreign('meeting_room_id', 'mr_room_amenity_room_fk')
                ->references('id')->on('meeting_rooms')->onDelete('cascade');
            $table->foreign('meeting_room_amenity_id', 'mr_room_amenity_amenity_fk')
                ->references('id')->on('meeting_room_amenities')->onDelete('cascade');
        });

        Schema::table('meeting_room_bookings', function (Blueprint $table) {
            $table->unique('code', 'mrb_code_unique');
        });
    }

    public function down()
    {
        Schema::table('meeting_room_room_amenity', function (Blueprint $table) {
            $table->dropForeign('mr_room_amenity_room_fk');
            $table->dropForeign('mr_room_amenity_amenity_fk');
        });

        Schema::table('meeting_room_bookings', function (Blueprint $table) {
            $table->dropUnique('mrb_code_unique');
        });
    }
}
```

## BE đã sửa
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
     *
     * Fix đợt review tổng, mục B.1: nhận thêm `room_id` (tùy chọn, chỉ dùng khi mở form ở chế độ
     * Sửa). Có `room_id` -> trả KÈM tiện nghi đã khóa mà phòng đó đang dùng (không chỉ tiện nghi
     * ACTIVE như trước) để không mất giá trị đang chọn khi mở lại form — quy tắc
     * `utils/select2LockedOption.js` (CLAUDE.md "Danh mục bị khóa vẫn phải hiện ở bản ghi đang
     * dùng nó"). Mỗi option kèm cờ `is_locked` để FE đánh dấu 🔒 tự động, KHÔNG cần tự viết
     * `templateResult`.
     */
    public function formOptions(Request $request)
    {
        $roomId = $request->room_id;

        // Tiện nghi ĐÃ KHÓA mà phòng này đang dùng — chỉ tra khi có room_id, tránh query thừa
        // cho form Thêm mới (không có room_id).
        $lockedAmenityIds = [];
        if ($roomId) {
            $lockedAmenityIds = DB::table('meeting_room_room_amenity')
                ->join(
                    'meeting_room_amenities',
                    'meeting_room_amenities.id',
                    '=',
                    'meeting_room_room_amenity.meeting_room_amenity_id'
                )
                ->where('meeting_room_room_amenity.meeting_room_id', $roomId)
                ->where('meeting_room_amenities.status', MeetingRoomAmenity::STATUS_INACTIVE)
                ->pluck('meeting_room_amenities.id')
                ->all();
        }

        $amenities = MeetingRoomAmenity::query()
            ->where(function ($q) use ($lockedAmenityIds) {
                $q->where('status', MeetingRoomAmenity::STATUS_ACTIVE);
                if (!empty($lockedAmenityIds)) {
                    $q->orWhereIn('id', $lockedAmenityIds);
                }
            })
            ->orderBy('sort_order', 'asc')
            ->orderBy('id', 'asc')
            ->get();

        $amenities->each(function ($amenity) use ($lockedAmenityIds) {
            // Dynamic attribute — Eloquent gộp thẳng vào $attributes nên serialize JSON bình
            // thường, khuôn giống `used_count` ở `MeetingRoomAmenityController::index()`.
            $amenity->is_locked = in_array($amenity->id, $lockedAmenityIds, true);
        });

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

            // Fix đợt review tổng, mục F: form KHÔNG có ô nhập department_id/part_id — đưa 2 cột
            // này vào $data khi trống thì `BaseModel::boot()` (creating/saving hook) tự điền
            // phòng ban/bộ phận CỦA NGƯỜI ĐANG TẠO, gán nhầm đơn vị cho phòng họp một cách âm
            // thầm (Phase 2 lọc theo department_id/part_id sẽ sai theo). Bỏ hẳn 2 cột khỏi
            // payload — cột trong DB vẫn giữ nguyên, chỉ không có UI/luồng nào ghi vào nó nữa.
            $data = $request->only([
                'code', 'name', 'company_id', 'allow_cross_company',
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

    /**
     * Fix đợt review tổng, mục A.1: `delete()` trần để lại pivot mồ côi vĩnh viễn ở
     * `meeting_room_room_amenity` (không có FK ON DELETE CASCADE trước fix mục A.3) — 78 dòng đã
     * đo được trong DB trước khi sửa. `detach()` TRƯỚC khi xóa phòng, cùng 1 transaction với
     * lệnh xóa (controller đã bọc `DB::transaction` quanh lời gọi hàm này).
     */
    public function destroy(MeetingRoom $meetingRoom)
    {
        $meetingRoom->amenities()->detach();
        $meetingRoom->delete();
    }
}
```

### Modules/Meeting/Services/MeetingRoomAmenityService.php
```php
<?php

namespace Modules\Meeting\Services;

use Illuminate\Http\Request;
use Modules\Meeting\Entities\MeetingRoomAmenity;
use Modules\Training\Services\BaseService;

/**
 * Plan quan-ly-phong-hop, Task 5 — danh mục "Tiện nghi phòng họp".
 * Khuôn copy từ `MeetingCancelReasonService`. Khác: thêm `code` (unique) + `icon` + `sort_order`,
 * sắp xếp mặc định theo `sort_order` rồi `id`.
 */
class MeetingRoomAmenityService extends BaseService
{
    public function index(Request $request)
    {
        $query = MeetingRoomAmenity::query()->select('meeting_room_amenities.*');

        if (isset($request->keyword)) {
            $escapedKeyword = escapeLikeKeyword($request->keyword);
            if ($escapedKeyword !== '') {
                $query->where(function ($q) use ($escapedKeyword) {
                    $q->where('name', 'like', '%' . $escapedKeyword . '%')
                        ->orWhere('code', 'like', '%' . $escapedKeyword . '%');
                });
            }
        }

        if (isset($request->status)) {
            $query->where('status', $request->status);
        }

        return $query->orderBy('sort_order', 'asc')->orderBy('id', 'asc');
    }

    /**
     * @return MeetingRoomAmenity|array
     */
    public function updateOrCreate(Request $request)
    {
        if (isset($request->id)) {
            $amenity = MeetingRoomAmenity::find($request->id);

            if ($amenity && $amenity->status == MeetingRoomAmenity::STATUS_ACTIVE) {
                $amenity->update([
                    'code' => $request->code,
                    'name' => $request->name,
                    'icon' => $request->icon,
                    'sort_order' => $request->sort_order ?? $amenity->sort_order,
                ]);
            } else {
                return ['status' => '404', 'message' => 'Dữ liệu đã thay đổi, vui lòng tải lại'];
            }
        } else {
            $amenity = MeetingRoomAmenity::create([
                'code' => $request->code,
                'name' => $request->name,
                'icon' => $request->icon,
                'sort_order' => $request->sort_order ?? 0,
                'status' => MeetingRoomAmenity::STATUS_ACTIVE,
            ]);
        }

        return $amenity;
    }

    public function destroy(MeetingRoomAmenity $meetingRoomAmenity)
    {
        $meetingRoomAmenity->delete();
    }
}
```

### Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php
```php
<?php

namespace Modules\Meeting\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Meeting\Entities\MeetingRoomAmenity;
use Modules\Meeting\Http\Requests\MeetingRoomAmenity\MeetingRoomAmenityRequest;
use Modules\Meeting\Services\MeetingRoomAmenityService;
use Modules\Meeting\Transformers\MeetingRoomAmenity\DetailMeetingRoomAmenityResource;
use Modules\Meeting\Transformers\MeetingRoomAmenity\MeetingRoomAmenityResource;

/**
 * Plan quan-ly-phong-hop, Task 5 — danh mục "Tiện nghi phòng họp".
 * Khuôn copy từ `MeetingCancelReasonController`, khác: thêm `code` (unique) + `icon` + `sort_order`,
 * `destroy()` chặn khi tiện nghi đang gắn phòng (kiểm `isCanDelete()` — quan hệ `rooms()`).
 */
class MeetingRoomAmenityController extends ApiController
{
    private $meetingRoomAmenityService;

    public function __construct(MeetingRoomAmenityService $meetingRoomAmenityService)
    {
        $this->meetingRoomAmenityService = $meetingRoomAmenityService;
    }

    public function index(Request $request)
    {
        // Tránh N+1 cột Người tạo/Người cập nhật: employee_create_name/employee_update_name
        // (accessor trong BaseModel) load quan hệ employee_create/employee_update + ->info
        // riêng cho TỪNG dòng nếu không eager-load trước.
        $query = $this->meetingRoomAmenityService->index($request)
            ->with(['employee_create.info', 'employee_update.info']);
        $paginated = $query->paginate($request->per_page ?? 10)->appends($request->query());

        // Tránh N+1 cột is_can_delete: tính số phòng đang gắn theo LÔ cho cả trang, thay vì gọi
        // isCanDelete()->rooms()->exists() cho từng dòng trong Resource. Gán THẲNG vào từng model
        // (không dùng static property trên Resource — tránh rò state sang request khác nếu build
        // response ném exception giữa chừng).
        //
        // Fix đợt review tổng, mục A.2: PHẢI join `meeting_rooms` — đếm pivot thô trước đây
        // (không join) tính luôn cả dòng mồ côi trỏ tới phòng đã xóa, khiến tiện nghi từng gắn
        // phòng đã xóa mãi mãi `is_can_delete = false` dù `isCanDelete()` (dùng `rooms()->exists()`,
        // có join `meeting_rooms`) nói ngược lại. Cùng 1 luật đếm với `isCanDelete()`.
        $ids = collect($paginated->items())->pluck('id')->all();
        $usedCounts = empty($ids) ? [] : DB::table('meeting_room_room_amenity')
            ->join('meeting_rooms', 'meeting_rooms.id', '=', 'meeting_room_room_amenity.meeting_room_id')
            ->whereIn('meeting_room_room_amenity.meeting_room_amenity_id', $ids)
            ->selectRaw('meeting_room_room_amenity.meeting_room_amenity_id AS meeting_room_amenity_id, COUNT(*) AS cnt')
            ->groupBy('meeting_room_room_amenity.meeting_room_amenity_id')
            ->pluck('cnt', 'meeting_room_amenity_id')
            ->all();

        foreach ($paginated->items() as $item) {
            $item->used_count = $usedCounts[$item->id] ?? 0;
        }

        $result = MeetingRoomAmenityResource::collection($paginated)->response()->getData();

        return $this->apiGetList($result, []);
    }

    public function updateOrCreate(MeetingRoomAmenityRequest $request)
    {
        try {
            return DB::transaction(function () use ($request) {
                $result = $this->meetingRoomAmenityService->updateOrCreate($request);
                if (is_array($result) && isset($result['status']) && $result['status'] === '404') {
                    return $this->responseNotFound($result['message']);
                }

                return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomAmenityResource($result));
            });
        } catch (\Illuminate\Validation\ValidationException $e) {
            // Lỗi validate phải giữ nguyên để FE map vào từng ô nhập — catch chung bên dưới
            // sẽ biến nó thành 400 mất thông tin field.
            throw $e;
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show(MeetingRoomAmenity $meetingRoomAmenity)
    {
        return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomAmenityResource($meetingRoomAmenity));
    }

    /**
     * Xóa 1 tiện nghi. Kiểm lại ở BE dù FE đã làm mờ nút: tiện nghi đang gắn cho phòng nào
     * đó mà xóa đi thì phòng đó mất tiện nghi ngoài ý muốn.
     */
    public function destroy(MeetingRoomAmenity $meetingRoomAmenity)
    {
        if (!$meetingRoomAmenity->isCanDelete()) {
            return $this->responseJson(
                'Tiện nghi này đang được gắn cho phòng họp nên không xóa được. Bạn có thể Khóa tiện nghi này.',
                Response::HTTP_BAD_REQUEST
            );
        }

        try {
            return DB::transaction(function () use ($meetingRoomAmenity) {
                $this->meetingRoomAmenityService->destroy($meetingRoomAmenity);

                return $this->responseJson('success', Response::HTTP_OK);
            });
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function lock(MeetingRoomAmenity $meetingRoomAmenity)
    {
        if (!$meetingRoomAmenity->isCanLockUpdate()) {
            return $this->responseBadRequest('Dữ liệu đã thay đổi, vui lòng tải lại');
        }

        $meetingRoomAmenity->status = MeetingRoomAmenity::STATUS_INACTIVE;
        $meetingRoomAmenity->save();

        return $this->responseJson('Khóa thành công', Response::HTTP_OK);
    }

    public function unlock(MeetingRoomAmenity $meetingRoomAmenity)
    {
        $meetingRoomAmenity->status = MeetingRoomAmenity::STATUS_ACTIVE;
        $meetingRoomAmenity->save();

        return $this->responseJson('Mở khóa thành công', Response::HTTP_OK);
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

### Modules/Meeting/Routes/api.php
```php
<?php

use Illuminate\Support\Facades\Route;
use Modules\Meeting\Http\Controllers\Api\V1\MeetingRoomAmenityController;
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
        Route::get('/form-options', [MeetingRoomController::class, 'formOptions']);
        Route::get('/', [MeetingRoomController::class, 'index'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::post('/', [MeetingRoomController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}', [MeetingRoomController::class, 'show'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
        Route::delete('/{meetingRoom}', [MeetingRoomController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/lock', [MeetingRoomController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/unlock', [MeetingRoomController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục phòng họp');
        Route::get('/{meetingRoom}/upcoming-bookings', [MeetingRoomController::class, 'upcomingBookings'])->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp');
    });
});
```

## FE đã sửa
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
            // Fix đợt review tổng, mục B.2: tên người quản lý khi id đó KHÔNG có trong
            // $store.state.employees (đã nghỉ việc) — API `GET rooms/{id}` trả sẵn `manager_name`,
            // lưu lại đây để computed `employeeOptions` chèn option giữ giá trị đang chọn.
            managerNameNotInStore: '',
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
        //
        // Fix đợt review tổng, mục B.2: `$store.state.employees` chỉ chứa nhân viên ĐANG làm việc
        // (Employee::getAll(true)) — phòng có quản lý đã nghỉ việc thì id đó KHÔNG có trong danh
        // sách, select sẽ hiện trống dù `data.manager_employee_id` vẫn còn giá trị, lưu lại là mất
        // dữ liệu (CLAUDE.md "danh mục đã khóa vẫn phải hiện ở bản ghi đang dùng nó"). Chèn thêm
        // 1 option dùng `manager_name` mà API `GET rooms/{id}` đã trả sẵn (`loadData()`), đánh dấu
        // `is_locked: true` để `select2LockedOption.js` (đã gọi sẵn trong V2BaseSelectInModal) tự
        // gắn 🔒 — KHÔNG tự viết templateResult, KHÔNG nối chữ "(đã khóa)" vào tên.
        employeeOptions() {
            const options = (this.$store.state.employees || []).map((employee) => ({
                id: employee.id,
                name: employeeOptionText(employee),
            }))

            const managerId = this.data.manager_employee_id
            if (managerId && !options.some((opt) => opt.id === managerId)) {
                options.push({
                    id: managerId,
                    name: this.managerNameNotInStore || `Nhân viên #${managerId}`,
                    is_locked: true,
                })
            }

            return options
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
                // Fix đợt review tổng, mục B.1: truyền `room_id` khi đang Sửa/Xem (this.id đã có
                // giá trị TRƯỚC khi modal mở — xem index.vue editItem()/viewItem() gán
                // selectedItem rồi mới $bvModal.show) để BE trả kèm tiện nghi đã khóa mà phòng
                // này đang dùng, tránh mất lựa chọn cũ khi mở form Sửa.
                const url = this.id
                    ? `meeting/rooms/form-options?room_id=${this.id}`
                    : 'meeting/rooms/form-options'
                const body = await this.$store.dispatch('apiGetMethod', url)
                const options = body.data || {}
                this.amenityOptions = (options.amenities || []).map((amenity) => ({
                    id: amenity.id,
                    name: amenity.name,
                    is_locked: !!amenity.is_locked,
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
            this.managerNameNotInStore = ''
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
                // Mục B.2: giữ tên quản lý đã nghỉ việc để employeeOptions chèn lại option đó.
                this.managerNameNotInStore = detail.manager_name || ''
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
