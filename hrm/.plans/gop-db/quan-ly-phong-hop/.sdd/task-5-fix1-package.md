# Re-review package — Task 5 fix round 1 (4 finding)

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
        $ids = collect($paginated->items())->pluck('id')->all();
        $usedCounts = empty($ids) ? [] : DB::table('meeting_room_room_amenity')
            ->whereIn('meeting_room_amenity_id', $ids)
            ->selectRaw('meeting_room_amenity_id, COUNT(*) AS cnt')
            ->groupBy('meeting_room_amenity_id')
            ->pluck('cnt', 'meeting_room_amenity_id')
            ->all();

        foreach ($paginated->items() as $item) {
            $item->used_count = $usedCounts[$item->id] ?? 0;
        }

        $result = MeetingRoomAmenityResource::collection($paginated)->response()->getData();

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

### Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php
```php
<?php

namespace Modules\Meeting\Transformers\MeetingRoomAmenity;

use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;

/**
 * Plan quan-ly-phong-hop, Task 5 — 1 dòng trong màn danh sách "Tiện nghi phòng họp".
 *
 * ⚠️ N+1 (review Task 3, fix round 1): `isCanDelete()` gọi `rooms()->exists()` — 1 query/dòng nếu
 * gọi trực tiếp trong vòng lặp. Controller::index() PHẢI tính trước theo lô rồi gán thẳng thuộc
 * tính `used_count` vào TỪNG model (`$item->used_count = ...`) trước khi dựng collection — KHÔNG
 * dùng static property trên class Resource (rủi ro rò state sang request khác trong cùng tiến
 * trình long-running/queue nếu build response ném exception giữa chừng mà static chưa kịp reset).
 * Thiếu bước gán thì rơi lại về gọi `isCanDelete()` từng dòng (đúng nhưng chậm — N+1) — vẫn giữ
 * làm fallback an toàn cho các nơi gọi Resource với 1 bản ghi đơn lẻ (không set `used_count`).
 */
class MeetingRoomAmenityResource extends ApiResource
{
    public function toArray($request): array
    {
        $usedCount = $this->used_count;
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
 *
 * Fix round 1 (review):
 *   - Mã tiện nghi gắn hậu tố duy nhất theo timestamp (KHÔNG dùng literal cố định) — chạy lại
 *     nhiều lần / bị kill giữa chừng không còn đụng mã cũ còn sót.
 *   - beforeAll chủ động dọn mọi bản ghi `code LIKE 'E2E_%'` còn sót từ lần chạy trước bị kill
 *     (afterAll không kịp chạy) — kết hợp với hậu tố timestamp để bộ test THẬT SỰ idempotent.
 *   - Ca "trùng mã" parse JSON và assert lỗi gắn đúng field `errors.code`, không chỉ
 *     `res.text().toContain('code')` (chuỗi đó luôn có mặt vì response nào cũng có
 *     `"code": <httpStatus>` ở top-level).
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const AMENITIES_URL = '/api/v1/meeting/room-amenities';

// Hậu tố duy nhất cho mỗi lần chạy — tránh đụng mã còn sót của lần chạy trước.
const RUN_SUFFIX = Date.now();
const CODE_PROJ = `E2E_PROJ_${RUN_SUFFIX}`;
const CODE_X = `E2E_X_${RUN_SUFFIX}`;
const CODE_DEL = `E2E_DEL_${RUN_SUFFIX}`;

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let noPermApi: APIRequestContext;
const createdIds: number[] = [];

/** Xóa mọi bản ghi `code LIKE 'E2E_%'` còn sót (lần chạy trước bị kill giữa chừng, afterAll
 *  không kịp dọn). Dùng `keyword` của index() (lọc theo name/code) + xóa từng trang cho tới hết. */
async function cleanupLeftoverE2eData() {
  // eslint-disable-next-line no-constant-condition
  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${AMENITIES_URL}?keyword=E2E_&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    // apiGetList() trả `data` là mảng item trực tiếp (paginate resource ->response()->getData()
    // được prepend thêm code/message ở cấp ngoài, KHÔNG lồng thêm 1 lớp `data` nữa).
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const leftoverIds = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith('E2E_'))
      .map((r: any) => r.id);
    if (leftoverIds.length === 0) break;
    for (const id of leftoverIds) {
      await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
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
  // Dọn dữ liệu test tạo ra — DB dùng chung với phiên khác.
  for (const id of createdIds) {
    await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
  }
  await api?.dispose();
  await noPermApi?.dispose();
});

test('1. tạo - sửa - khóa - mở khóa tiện nghi', async () => {
  const created = await api.post(AMENITIES_URL, {
    data: { code: CODE_PROJ, name: 'Máy chiếu E2E', icon: 'ri-projector-line' },
  });
  expect(created.status()).toBe(200);
  const createdBody = await created.json();
  const id = createdBody.data.id;
  createdIds.push(id);
  expect(createdBody.data.code).toBe(CODE_PROJ);
  expect(createdBody.data.name).toBe('Máy chiếu E2E');
  expect(createdBody.data.status).toBe(1);
  expect(createdBody.data.is_can_edit).toBe(true);
  expect(createdBody.data.is_can_delete).toBe(true);
  expect(createdBody.data.is_can_lock).toBe(true);

  // Sửa
  const updated = await api.post(AMENITIES_URL, {
    data: { id, code: CODE_PROJ, name: 'Máy chiếu E2E (đã sửa)', icon: 'ri-projector-line', sort_order: 5 },
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
    data: { code: CODE_PROJ, name: 'Trùng mã' },
  });
  expect(res.status()).toBe(422);

  // Khuôn body thật của BaseRequest::failedValidation(): { code: 422, errors: { <field>: <msg> } }.
  // res.text().toContain('code') luôn xanh (mọi response đều có key top-level "code": <httpStatus>)
  // nên PHẢI parse JSON rồi assert đúng field lỗi nằm trong `errors`.
  const body = await res.json();
  expect(body.errors).toHaveProperty('code');
  expect(typeof body.errors.code).toBe('string');
  expect(body.errors.code.length).toBeGreaterThan(0);
});

test('3. không quyền thì 403', async () => {
  const res = await noPermApi.post(AMENITIES_URL, {
    data: { code: CODE_X, name: 'X' },
  });
  expect(res.status()).toBe(403);
});

test('4. tiện nghi CHƯA gắn phòng nào thì xóa được', async () => {
  const created = await api.post(AMENITIES_URL, {
    data: { code: CODE_DEL, name: 'Tiện nghi để xóa' },
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
