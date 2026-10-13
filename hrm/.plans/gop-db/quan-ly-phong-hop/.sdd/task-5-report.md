# Task 5 — API danh mục tiện nghi phòng họp — Báo cáo

**Status: HOÀN THÀNH**

## Nơi làm việc
- BE: worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api`
  (nhánh `feat/quan-ly-phong-hop`), API chạy sẵn ở `:8001`.
- e2e: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (dùng chung).

## Quy trình TDD

### Bước 1-2: Viết spec trước, chạy xác nhận ĐỎ
File `e2e/tests/meeting/room-amenity.api.spec.ts` viết trước theo khuôn
`e2e/tests/assign/customer-demand-link.api.spec.ts`, tự dựng 2 `APIRequestContext`:
- `api`: token đọc từ `e2e/.auth/api-wt.json` (tài khoản CÓ quyền, employee_id 34).
- `noPermApi`: token đọc từ `origins[0].localStorage[0].value` của `e2e/.auth/user-nocost-wt.json`
  (employee_id 25, không có quyền).

Chạy lần đầu (trước khi có route/BE):
```
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/room-amenity.api.spec.ts --project=api --no-deps --workers=1
```
Kết quả (ĐỎ, đúng kỳ vọng — 404 vì chưa có route):
```
  ✘  1 … 1. tạo - sửa - khóa - mở khóa tiện nghi (273ms)
  -  2 … 2. trùng mã thì trả 422 kèm field code
  -  3 … 3. không quyền thì 403
  -  4 … 4. tiện nghi CHƯA gắn phòng nào thì xóa được

  Error: expect(received).toBe(expected)
  Expected: 200
  Received: 404

  1 failed
    [api] › tests/meeting/room-amenity.api.spec.ts:54:5 › 1. tạo - sửa - khóa - mở khóa tiện nghi
  3 did not run
```

### Bước 3-4: Viết BE (Service, Request, 2 Resource, Controller) + khai route

Copy khuôn từ `Modules/Assign/Services/MeetingCancelReasonService.php` /
`MeetingCancelReasonController.php` / `MeetingCancelReasonRequest.php` /
`Transformers/MeetingCancelReason/*.php`, khác đúng 3 điểm theo brief: thêm `code` (unique) +
`icon` + `sort_order`; `isCanDelete()` kiểm quan hệ `rooms()` (đã có sẵn từ Task 3); sắp xếp mặc
định `sort_order` rồi `id`.

**⚠️ 1 điểm khác khuôn gốc, chủ động thêm** — brief "Định nghĩa hoàn thành" mục 5 đòi Resource trả
thêm `is_can_lock` (khuôn `MeetingCancelReasonResource` gốc CHỈ có `is_can_edit`/`is_can_delete`,
không có `is_can_lock`) → cả 2 Resource (`MeetingRoomAmenityResource`,
`DetailMeetingRoomAmenityResource`) trả thêm `'is_can_lock' => $this->isCanLockUpdate()`. Đồng thời
`updateOrCreate()` trả về qua `DetailMeetingRoomAmenityResource` (khuôn gốc trả thẳng model qua
`response()->json($reason, 200)` lồng vào `data` — không kèm 3 cờ `is_can_*`) để FE có sẵn cờ ngay
sau khi lưu, không phải gọi lại `show`.

**Chặn N+1 (ràng buộc bổ sung từ review Task 3)**: `MeetingRoomAmenity::isCanDelete()` gọi
`rooms()->exists()` — 1 query/dòng nếu gọi trực tiếp trong Resource của danh sách.
`MeetingRoomAmenityController::index()` tính trước theo lô:
```php
$ids = collect($paginated->items())->pluck('id')->all();
MeetingRoomAmenityResource::$usedCounts = empty($ids) ? [] : DB::table('meeting_room_room_amenity')
    ->whereIn('meeting_room_amenity_id', $ids)
    ->selectRaw('meeting_room_amenity_id, COUNT(*) AS cnt')
    ->groupBy('meeting_room_amenity_id')
    ->pluck('cnt', 'meeting_room_amenity_id')
    ->all();
```
rồi `MeetingRoomAmenityResource::toArray()` đọc `self::$usedCounts[$this->id] ?? null` thay vì gọi
`isCanDelete()` từng dòng (chỉ fallback gọi `isCanDelete()` khi map không có key — an toàn cho
`show()`/response tạo-sửa vốn chỉ 1 bản ghi).

**`destroy()`** kiểm `isCanDelete()` trước khi xóa (mirror `MeetingCancelReasonController::destroy`)
— tiện nghi đang gắn phòng thì trả 400 kèm gợi ý Khóa, thay vì chặn ở khóa ngoại.

⚠️ `updateOrCreate` rethrow `ValidationException` TRƯỚC khi catch `Exception` (copy đúng
`MeetingCancelReasonController.php:60-66`). ⚠️ Route `/getAll` khai trước `/{meetingRoomAmenity}`.

### Bước 5: Chạy lại spec — XANH

```
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/room-amenity.api.spec.ts --project=api --no-deps --workers=1
```

**Dòng tổng kết (đọc đúng dòng tổng kết, không nhìn cuối log theo ruling serial):**
```
Running 4 tests using 1 worker

  ✓  1 [api] › tests/meeting/room-amenity.api.spec.ts:54:5 › 1. tạo - sửa - khóa - mở khóa tiện nghi (2.5s)
  ✓  2 [api] › tests/meeting/room-amenity.api.spec.ts:95:5 › 2. trùng mã thì trả 422 kèm field code (298ms)
  ✓  3 [api] › tests/meeting/room-amenity.api.spec.ts:103:5 › 3. không quyền thì 403 (215ms)
  ✓  4 [api] › tests/meeting/room-amenity.api.spec.ts:110:5 › 4. tiện nghi CHƯA gắn phòng nào thì xóa được (1.2s)

  4 passed (5.4s)
```

4/4 ca, đủ 4 nhóm brief yêu cầu: tạo/sửa/khóa/mở khóa · trùng mã → 422 kèm field `code` ·
không quyền → 403 · xóa khi chưa gắn phòng nào.

## Dọn dữ liệu test
`test.afterAll` trong spec tự `DELETE` mọi id đã tạo (`createdIds`). Xác nhận lại bằng tinker sau
khi chạy xong:
```
php artisan tinker --execute "echo \Modules\Meeting\Entities\MeetingRoomAmenity::where('code','like','E2E_%')->count();"
→ 0
```

## Danh sách file

| Loại | File |
|---|---|
| Create | `Modules/Meeting/Services/MeetingRoomAmenityService.php` |
| Create | `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php` |
| Create | `Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php` |
| Create | `Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php` |
| Create | `Modules/Meeting/Transformers/MeetingRoomAmenity/DetailMeetingRoomAmenityResource.php` |
| Modify | `Modules/Meeting/Routes/api.php` |
| Test | `e2e/tests/meeting/room-amenity.api.spec.ts` |

(Đường dẫn `Modules/...` ở trên đều nằm trong worktree
`/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api`.)

## Route đã khai (đúng thứ tự, `/getAll` trước wildcard)
```
GET    /api/v1/meeting/room-amenities/getAll
GET    /api/v1/meeting/room-amenities            checkPermission: Quản lý…|Xem danh mục tiện nghi phòng họp
POST   /api/v1/meeting/room-amenities             checkPermission: Quản lý danh mục tiện nghi phòng họp
GET    /api/v1/meeting/room-amenities/{id}
DELETE /api/v1/meeting/room-amenities/{id}        checkPermission: Quản lý danh mục tiện nghi phòng họp
GET    /api/v1/meeting/room-amenities/{id}/lock   checkPermission: Quản lý danh mục tiện nghi phòng họp
GET    /api/v1/meeting/room-amenities/{id}/unlock checkPermission: Quản lý danh mục tiện nghi phòng họp
```

## Định nghĩa hoàn thành — đối chiếu
1. ✅ Bằng chứng chạy ĐỎ (dán ở trên).
2. ✅ Đủ 5 file BE + route group.
3. ✅ Spec XANH, phủ đủ 4 ca (tạo/sửa/khóa/mở khóa · trùng mã → 422 field `code` · không quyền →
   403 · xóa khi chưa gắn phòng nào).
4. ✅ Đọc dòng tổng kết Playwright `4 passed (5.4s)` (không có `did not run`).
5. ✅ Resource (cả list lẫn detail) trả `is_can_edit`, `is_can_delete`, `is_can_lock`.

## Ràng buộc đã tuân thủ
- Không `git commit` / `push` / `stash` / `checkout`.
- Chỉ sửa file trong `Modules/Meeting/` (worktree BE) và `e2e/tests/meeting/`.
- Không sửa `e2e/auth/*`, `e2e/playwright.config.ts`, `.auth/api.json`, `.auth/user.json`.
- Không dispatch subagent nào khác, không tự gọi reviewer.
- PHP dùng `/opt/homebrew/opt/php@7.4/bin/php` (lint từng file BE trước khi chạy e2e).
- Không tự khởi động/tắt server nào, không `pkill`.

## Concerns
- `updateOrCreate()` trả response qua `DetailMeetingRoomAmenityResource` thay vì trả thẳng model
  như khuôn gốc `MeetingCancelReasonController` — lệch nhỏ so với "copy nguyên khuôn", nhưng là hệ
  quả bắt buộc để thỏa mãn yêu cầu cờ `is_can_lock` ở Định nghĩa hoàn thành mục 5 (khuôn gốc không
  có cờ này trên response create/update). Đã ghi rõ lý do trong code + báo cáo này để task sau
  (FE, Task 6 phòng họp tham chiếu tiện nghi) biết mà dùng đúng field.
- `destroy()` có guard chặn xóa khi đang gắn phòng (mirror hành vi của `MeetingCancelReasonController`)
  dù brief chỉ yêu cầu kiểm ca "xóa được khi CHƯA gắn phòng" — chưa có ca e2e cho nhánh "xóa bị chặn
  vì đang gắn phòng" (cần phòng họp thật, phụ thuộc Task 6 chưa làm). Đề xuất bổ sung ca này khi
  Task 6 (API phòng họp) xong, có thể gắn `meeting_room_room_amenity` thật để test.
- Permission id 1576/1577 và role Super admin (employee 34, id trong `api-wt.json`) đã được cấp sẵn
  từ Task 4 — không cần thao tác gì thêm ở task này.

---

## Fix round 1/5 — 4 finding Important từ review

### Finding 1 — Bỏ biến static `MeetingRoomAmenityResource::$usedCounts`
Đã bỏ hẳn property static. Sửa lại theo hướng không có state: `Controller::index()` sau khi
`paginate()` thì `foreach ($paginated->items() as $item) { $item->used_count = $usedCounts[$item->id] ?? 0; }`
gán thẳng vào từng model; `MeetingRoomAmenityResource::toArray()` đọc `$this->used_count` (proxy
qua `JsonResource::__get()` tới model), fallback về `isCanDelete()` khi thuộc tính chưa được set
(trường hợp Resource dùng đơn lẻ, không qua `index()`). Không còn state sống sót giữa các request.

File sửa: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php`,
`Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php`.

### Finding 2 — Ca "trùng mã → 422" assert đúng field
Xác nhận khuôn body thật của `Modules\Training\Http\Requests\BaseRequest::failedValidation()`:
```php
$json = ['code' => 422, 'errors' => $message]; // $message[field] = <msg đầu tiên của field đó>
```
(Không có file `app/Http/Requests/BaseRequest.php` ở repo này — `BaseRequest` mà
`MeetingRoomAmenityRequest` kế thừa nằm ở `Modules/Training/Http/Requests/BaseRequest.php`, đã đọc
lại nguyên văn để lấy đúng khuôn body.)

Sửa spec: parse JSON rồi assert `body.errors` có key `code` (đúng field bị lỗi), thay vì
`res.text().toContain('code')` (luôn xanh vì mọi response đều có `"code": <httpStatus>` ở top-level
— kể cả khi validate hỏng hoàn toàn hoặc lỗi rơi vào field khác).

```ts
const body = await res.json();
expect(body.errors).toHaveProperty('code');
expect(typeof body.errors.code).toBe('string');
expect(body.errors.code.length).toBeGreaterThan(0);
```

### Finding 3 — Dữ liệu test không idempotent
Sửa **cả 2** hướng đề xuất:
1. Hậu tố duy nhất theo timestamp cho mọi mã tạo trong spec: `CODE_PROJ = E2E_PROJ_${Date.now()}`,
   tương tự `CODE_X`, `CODE_DEL` — không còn literal cố định nào đụng lần chạy trước.
2. `beforeAll` gọi `cleanupLeftoverE2eData()`: liệt kê `GET ...?keyword=E2E_&per_page=100` rồi xóa
   hết bản ghi `code` bắt đầu bằng `E2E_` còn sót (trường hợp lần chạy trước bị kill giữa chừng,
   `afterAll` không kịp chạy), lặp tối đa 20 lần cho tới khi hết.

### Finding 4 — N+1 cột Người tạo/Người cập nhật
`Controller::index()` thêm `->with(['employee_create.info', 'employee_update.info'])` vào query
trước khi `paginate()`. Đúng theo ruling của người điều phối: sửa Ở MÀN MỚI
(`MeetingRoomAmenityService`/`Controller`), KHÔNG đụng `MeetingCancelReasonService` (khuôn gốc) dù
nó dính lỗi tương tự.

## Kiểm chứng lại sau fix round 1

### 1) Chạy spec 2 lần liên tiếp (chứng minh idempotent)

Lệnh (giống hệt lần trước):
```
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/room-amenity.api.spec.ts --project=api --no-deps --workers=1
```

**Lần chạy #1 — dòng tổng kết:**
```
Running 4 tests using 1 worker

  ✓  1 [api] › tests/meeting/room-amenity.api.spec.ts:92:5 › 1. tạo - sửa - khóa - mở khóa tiện nghi (2.1s)
  ✓  2 [api] › tests/meeting/room-amenity.api.spec.ts:133:5 › 2. trùng mã thì trả 422 kèm field code (259ms)
  ✓  3 [api] › tests/meeting/room-amenity.api.spec.ts:148:5 › 3. không quyền thì 403 (226ms)
  ✓  4 [api] › tests/meeting/room-amenity.api.spec.ts:155:5 › 4. tiện nghi CHƯA gắn phòng nào thì xóa được (1.2s)

  4 passed (5.0s)
```

**Lần chạy #2 — chạy NGAY SAU, không dọn tay gì thêm — dòng tổng kết:**
```
Running 4 tests using 1 worker

  ✓  1 [api] › tests/meeting/room-amenity.api.spec.ts:92:5 › 1. tạo - sửa - khóa - mở khóa tiện nghi (2.0s)
  ✓  2 [api] › tests/meeting/room-amenity.api.spec.ts:133:5 › 2. trùng mã thì trả 422 kèm field code (403ms)
  ✓  3 [api] › tests/meeting/room-amenity.api.spec.ts:148:5 › 3. không quyền thì 403 (250ms)
  ✓  4 [api] › tests/meeting/room-amenity.api.spec.ts:155:5 › 4. tiện nghi CHƯA gắn phòng nào thì xóa được (1.5s)

  4 passed (5.3s)
```
Cả 2 lần đều **4 passed**, không có ca nào "did not run" → idempotent xác nhận thật, không phải
đọc nhầm log serial.

### 2) Đếm query thật để xác nhận hết N+1

Script `nplus1_check.php` (chạy qua `artisan tinker --execute "require '...'"`): seed 6 bản ghi
`E2E_NPLUS1_*` với `created_by=updated_by=34` (khác null — bắt buộc để accessor
`employee_create_name`/`employee_update_name` THẬT SỰ bắn query khi test "trước fix", vì
`BelongsTo::getResults()` của Laravel không query nếu khóa ngoại null).

- **"Trước fix" (mô phỏng đúng cách gọi cũ — accessor + `isCanDelete()` gọi trực tiếp từng dòng,
  không `with()`, không batch `used_count`)**: **50 query** cho 6 dòng (~8 query/dòng: 2 quan hệ
  employee × 2 cấp `employee_create`→`info` + `isCanDelete()`→`rooms()->exists()`, cộng
  count+select phân trang).
- **"Sau fix" (gọi thẳng `MeetingRoomAmenityController::index()` thật)**: **9 query** cho cùng 6
  dòng — cố định, không tăng theo số dòng (1 count + 1 select phân trang + 4 truy vấn `with()`
  theo lô cho `employee_create`/`employee_update`/2 cấp `info` + 1 truy vấn `used_count` theo lô).

```
ROW_COUNT_SEEDED=6
FIXED_ROWS_RETURNED=6
UNFIXED_QUERY_COUNT=50
FIXED_QUERY_COUNT=9
```

Dữ liệu seed cho phép đo (`E2E_NPLUS1_*`) đã xóa sạch ngay trong script; xác nhận lại bằng
`MeetingRoomAmenity::where('code','like','E2E_%')->count()` → **0**.

## Định nghĩa hoàn thành fix round 1 — đối chiếu
1. ✅ Finding 1 (static property) — đã bỏ, thay bằng gán thuộc tính per-model.
2. ✅ Finding 2 (assertion rỗng nghĩa) — đã sửa, assert đúng `errors.code`.
3. ✅ Finding 3 (không idempotent) — đã sửa cả 2 hướng (hậu tố timestamp + cleanup `beforeAll`).
4. ✅ Finding 4 (N+1 employee names) — đã thêm `with()`, đo thật 50→9 query cho 6 dòng.
5. ✅ Chạy lại spec đúng lệnh cũ, đọc dòng tổng kết, 2 lần liên tiếp đều `4 passed`.
6. ✅ Chỉ đụng `Modules/Meeting/` (worktree BE) và `e2e/tests/meeting/`; không commit/push/stash.
