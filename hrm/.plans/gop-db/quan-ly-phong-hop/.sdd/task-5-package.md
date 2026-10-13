# Review package — Task 5 (API danh mục tiện nghi)

## File BE mới

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

    /** Dropdown — chỉ tiện nghi đang Hoạt động */
    public function getAll(Request $request)
    {
        return MeetingRoomAmenity::query()
            ->select('meeting_room_amenities.*')
            ->where('status', MeetingRoomAmenity::STATUS_ACTIVE)
            ->orderBy('sort_order', 'asc')
            ->orderBy('id', 'asc')
            ->get();
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
        $query = $this->meetingRoomAmenityService->index($request);
        $paginated = $query->paginate($request->per_page ?? 10)->appends($request->query());

        // Tránh N+1: tính số phòng đang gắn theo LÔ cho cả trang, thay vì gọi
        // isCanDelete()->rooms()->exists() cho từng dòng trong Resource.
        $ids = collect($paginated->items())->pluck('id')->all();
        MeetingRoomAmenityResource::$usedCounts = empty($ids) ? [] : DB::table('meeting_room_room_amenity')
            ->whereIn('meeting_room_amenity_id', $ids)
            ->selectRaw('meeting_room_amenity_id, COUNT(*) AS cnt')
            ->groupBy('meeting_room_amenity_id')
            ->pluck('cnt', 'meeting_room_amenity_id')
            ->all();

        $result = MeetingRoomAmenityResource::collection($paginated)->response()->getData();
        MeetingRoomAmenityResource::$usedCounts = [];

        return $this->apiGetList($result, []);
    }

    /** Dropdown chọn tiện nghi cho phòng họp — chỉ tiện nghi đang Hoạt động */
    public function getAll(Request $request)
    {
        $result = $this->meetingRoomAmenityService->getAll($request);

        return $this->responseJson('success', Response::HTTP_OK, $result);
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

### Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php
```php
<?php

namespace Modules\Meeting\Http\Requests\MeetingRoomAmenity;

use Illuminate\Validation\Rule;
use Modules\Training\Http\Requests\BaseRequest;

/**
 * Plan quan-ly-phong-hop, Task 5 — validate form thêm/sửa tiện nghi phòng họp.
 * `BaseRequest::failedValidation()` đã rethrow `ValidationException` (422) nên FE map được
 * lỗi vào từng ô nhập; KHÔNG catch chung ở controller.
 */
class MeetingRoomAmenityRequest extends BaseRequest
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
            'code' => ['required', 'string', 'max:50', Rule::unique('meeting_room_amenities', 'code')->ignore($id)],
            'name' => ['required', 'string', 'max:255'],
            'icon' => ['nullable', 'string', 'max:100'],
            'sort_order' => ['nullable', 'integer', 'min:0'],
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
            'code.required' => 'Vui lòng nhập mã tiện nghi',
            'code.max' => 'Mã tiện nghi tối đa 50 ký tự',
            'code.unique' => 'Mã tiện nghi đã tồn tại trong hệ thống',
            'name.required' => 'Vui lòng nhập tên tiện nghi',
            'name.max' => 'Tên tiện nghi tối đa 255 ký tự',
            'icon.max' => 'Icon tối đa 100 ký tự',
            'sort_order.integer' => 'Thứ tự sắp xếp phải là số nguyên',
            'sort_order.min' => 'Thứ tự sắp xếp không được âm',
        ];
    }
}
```

### Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoomAmenity;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;

/**
 * Plan quan-ly-phong-hop, Task 5 — 1 dòng trong màn danh sách "Tiện nghi phòng họp".
 *
 * ⚠️ N+1 (review Task 3): `isCanDelete()` gọi `rooms()->exists()` — 1 query/dòng nếu gọi trực
 * tiếp trong vòng lặp. Controller::index() PHẢI tính trước theo lô rồi gán vào `self::$usedCounts`
 * (id => số phòng đang gắn) trước khi dựng collection; thiếu bước đó thì rơi lại về gọi
 * `isCanDelete()` từng dòng (đúng nhưng chậm — N+1).
 */
class MeetingRoomAmenityResource extends ApiResource
{
    /** @var array<int,int> id => số phòng đang gắn tiện nghi này */
    public static array $usedCounts = [];

    public function toArray($request): array
    {
        $usedCount = self::$usedCounts[$this->id] ?? null;
        $isCanDelete = $usedCount !== null ? ((int) $usedCount === 0) : $this->isCanDelete();

        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'icon' => $this->icon,
            'sort_order' => $this->sort_order,
            'status' => $this->status,
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

### Modules/Meeting/Transformers/MeetingRoomAmenity/DetailMeetingRoomAmenityResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoomAmenity;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;

/**
 * Plan quan-ly-phong-hop, Task 5 — chi tiết 1 tiện nghi phòng họp (popup Xem/Sửa, và cũng
 * dùng làm response của tạo mới / cập nhật để FE có sẵn 3 cờ is_can_* ngay sau khi lưu).
 */
class DetailMeetingRoomAmenityResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'icon' => $this->icon,
            'sort_order' => $this->sort_order,
            'status' => $this->status,
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

    // Danh mục phòng họp khai ở Task 6
});
```

### e2e/tests/meeting/room-amenity.api.spec.ts
```ts
/**
 * E2E API — Danh mục "Tiện nghi phòng họp" (Task 5, plan quan-ly-phong-hop).
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): API ở :8001.
 * Token đọc từ e2e/.auth/api-wt.json (tài khoản CÓ quyền quản lý danh mục).
 * Ca "không quyền" dùng token của e2e/.auth/user-nocost-wt.json (tài khoản id 25).
 *
 * Phủ 4 ca theo brief:
 *   1. tạo -> sửa -> khóa -> mở khóa
 *   2. trùng mã -> 422 kèm field `code`
 *   3. không quyền -> 403
 *   4. xóa: tiện nghi CHƯA gắn phòng nào thì xóa được
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const AMENITIES_URL = '/api/v1/meeting/room-amenities';

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let noPermApi: APIRequestContext;
const createdIds: number[] = [];

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
  for (const id of createdIds) {
    await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
  }
  await api?.dispose();
  await noPermApi?.dispose();
});

test('1. tạo - sửa - khóa - mở khóa tiện nghi', async () => {
  const created = await api.post(AMENITIES_URL, {
    data: { code: 'E2E_PROJ', name: 'Máy chiếu E2E', icon: 'ri-projector-line' },
  });
  expect(created.status()).toBe(200);
  const createdBody = await created.json();
  const id = createdBody.data.id;
  createdIds.push(id);
  expect(createdBody.data.code).toBe('E2E_PROJ');
  expect(createdBody.data.name).toBe('Máy chiếu E2E');
  expect(createdBody.data.status).toBe(1);
  expect(createdBody.data.is_can_edit).toBe(true);
  expect(createdBody.data.is_can_delete).toBe(true);
  expect(createdBody.data.is_can_lock).toBe(true);

  // Sửa
  const updated = await api.post(AMENITIES_URL, {
    data: { id, code: 'E2E_PROJ', name: 'Máy chiếu E2E (đã sửa)', icon: 'ri-projector-line', sort_order: 5 },
  });
  expect(updated.status()).toBe(200);
  const updatedBody = await updated.json();
  expect(updatedBody.data.name).toBe('Máy chiếu E2E (đã sửa)');
  expect(updatedBody.data.sort_order).toBe(5);

  // Khóa
  const locked = await api.get(`${AMENITIES_URL}/${id}/lock`);
  expect(locked.status()).toBe(200);

  const detailAfterLock = await (await api.get(`${AMENITIES_URL}/${id}`)).json();
  expect(detailAfterLock.data.status).toBe(2);
  expect(detailAfterLock.data.is_can_lock).toBe(false);

  // Mở khóa
  const unlocked = await api.get(`${AMENITIES_URL}/${id}/unlock`);
  expect(unlocked.status()).toBe(200);

  const detailAfterUnlock = await (await api.get(`${AMENITIES_URL}/${id}`)).json();
  expect(detailAfterUnlock.data.status).toBe(1);
  expect(detailAfterUnlock.data.is_can_lock).toBe(true);
});

test('2. trùng mã thì trả 422 kèm field code', async () => {
  const res = await api.post(AMENITIES_URL, {
    data: { code: 'E2E_PROJ', name: 'Trùng mã' },
  });
  expect(res.status()).toBe(422);
  expect(await res.text()).toContain('code');
});

test('3. không quyền thì 403', async () => {
  const res = await noPermApi.post(AMENITIES_URL, {
    data: { code: 'E2E_X', name: 'X' },
  });
  expect(res.status()).toBe(403);
});

test('4. tiện nghi CHƯA gắn phòng nào thì xóa được', async () => {
  const created = await api.post(AMENITIES_URL, {
    data: { code: 'E2E_DEL', name: 'Tiện nghi để xóa' },
  });
  expect(created.status()).toBe(200);
  const id = (await created.json()).data.id;

  const detail = await (await api.get(`${AMENITIES_URL}/${id}`)).json();
  expect(detail.data.is_can_delete).toBe(true);

  const destroyed = await api.delete(`${AMENITIES_URL}/${id}`);
  expect(destroyed.status()).toBe(200);

  const afterDelete = await api.get(`${AMENITIES_URL}/${id}`);
  expect(afterDelete.status()).toBe(404);
});
```
