> ## ⚠️ NƠI LÀM VIỆC — WORKTREE (chốt 17/09/2026, user yêu cầu)
>
> Nhánh `gop_db` đang được một phiên làm việc khác dùng → mọi thay đổi code của plan này làm trong
> **worktree riêng**, nhánh `feat/quan-ly-phong-hop`:
>
> | Thứ | Đường dẫn |
> |---|---|
> | Repo BE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` |
> | Repo FE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client` |
> | Bộ e2e | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (DÙNG CHUNG, không có worktree) |
> | Tài liệu (plan, ledger) | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/` |
>
> - API của worktree chạy ở **`http://127.0.0.1:8001`**, Nuxt của worktree ở **`http://127.0.0.1:3001`**.
>   Cổng 8000/3000 là server của phiên khác — **KHÔNG đụng, KHÔNG tắt, KHÔNG `pkill`**.
> - Chạy e2e phải truyền cả 2 biến: `BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`.
> - Phiên đăng nhập của Playwright gắn theo ORIGIN. `.auth/user.json` chỉ dùng được cho `:3000` → đã tạo sẵn
>   **`.auth/user-wt.json`** (admin) và **`.auth/user-nocost-wt.json`** (tài khoản thiếu quyền) với origin
>   đổi sang `:3001`. Spec UI phải khai `test.use({ storageState: '.auth/user-wt.json' })`, KHÔNG dùng
>   `user.json` (dùng nhầm là bị đẩy về `/login`, rất dễ tưởng lỗi đăng nhập).
> - TUYỆT ĐỐI KHÔNG `git commit` / `push` / `stash` / `checkout` file.
> - Worktree KHÔNG có `.plans`, `.claude`, `docs`, `CLAUDE.md` (là symlink ngoài repo) — tài liệu ghi về
>   đường dẫn tài liệu ở bảng trên.
> - Đường dẫn trong phần dưới ghi `hrm-api/...` hay `hrm-client/...` thì hiểu là **thư mục tương ứng trong
>   worktree**, không phải checkout gốc.


> **Ràng buộc bổ sung từ review Task 3 (bắt buộc áp dụng ở task này):**
> `MeetingRoom::isCanDelete()`, `upcomingBookingCount()` và `MeetingRoomAmenity::isCanDelete()` là
> **instance method, mỗi lần gọi bắn 1 query**. Gọi chúng trong vòng lặp danh sách là N+1 kinh điển
> (50 dòng = 50 query). Ở màn danh sách phải **tính theo lô 1 lần** rồi tra map, ví dụ:
>
> ```php
> $usedCounts = \DB::table('meeting_room_bookings')
>     ->whereIn('meeting_room_id', $roomIds)
>     ->selectRaw('meeting_room_id, COUNT(*) AS cnt')
>     ->groupBy('meeting_room_id')
>     ->pluck('cnt', 'meeting_room_id');
> ```
>
> rồi Resource đọc `$usedCounts[$room->id] ?? 0` thay vì gọi `$room->isCanDelete()` từng dòng.
> Luôn kèm `with('amenities')` cho danh sách phòng.


## Task 5: API danh mục tiện nghi phòng họp

**Files:**
- Create: `Modules/Meeting/Services/MeetingRoomAmenityService.php`
- Create: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php`
- Create: `Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php`
- Create: `Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php`
- Create: `Modules/Meeting/Transformers/MeetingRoomAmenity/DetailMeetingRoomAmenityResource.php`
- Modify: `Modules/Meeting/Routes/api.php`
- Test: `e2e/tests/meeting/room-amenity.api.spec.ts`

**Interfaces:**
- Consumes: `MeetingRoomAmenity` (Task 3)
- Produces: `GET|POST /api/v1/meeting/room-amenities`, `GET /{id}`, `DELETE /{id}`,
  `GET /{id}/lock`, `GET /{id}/unlock`, `GET /getAll`

> **Copy nguyên khuôn** từ danh mục lý do hủy cuộc họp — 5 file tương ứng:
> `Modules/Assign/Services/MeetingCancelReasonService.php`,
> `Modules/Assign/Http/Controllers/Api/V1/MeetingCancelReasonController.php`,
> `Modules/Assign/Http/Requests/MeetingCancelReason/MeetingCancelReasonRequest.php`,
> `Modules/Assign/Transformers/MeetingCancelReason/*.php`.
> Khác 3 điểm: thêm trường `code` (unique) và `icon`, `sort_order`; `isCanDelete()` kiểm quan hệ `rooms()`;
> sắp xếp mặc định theo `sort_order` rồi `id`.

> **Ruling R1 (pre-flight):** `e2e/utils/` KHÔNG có helper `api` / `noPermApi` dùng chung — code mẫu dưới
> đây là mô tả ca kiểm, không phải code chạy nguyên văn. Mỗi spec **tự dựng `APIRequestContext`** theo khuôn
> `e2e/tests/assign/customer-demand-link.api.spec.ts` (đọc token từ `e2e/.auth/api.json`). Ca "không quyền"
> dùng tài khoản nocost có sẵn: `test.use({ storageState: '.auth/user-nocost.json' })` (sinh bởi
> `e2e/auth/login-nocost.setup.ts`). Nếu project `api-setup` đỏ trên DB gộp (bẫy đã biết: thiếu bảng
> `hrm_employees`) thì chạy spec lẻ bằng `--no-deps`.

- [ ] **Bước 1: Viết e2e API spec (đỏ trước)**

`e2e/tests/meeting/room-amenity.api.spec.ts` — phủ 4 ca:

```ts
test('tạo - sửa - khóa - mở khóa tiện nghi', async () => {
    const created = await api.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_PROJ', name: 'Máy chiếu E2E', icon: 'ri-projector-line' },
    });
    expect(created.status()).toBe(200);
    const id = (await created.json()).data.id;

    const locked = await api.get(`/api/v1/meeting/room-amenities/${id}/lock`);
    expect(locked.status()).toBe(200);

    const detail = await (await api.get(`/api/v1/meeting/room-amenities/${id}`)).json();
    expect(detail.data.status).toBe(2);
});

test('trùng mã thì trả 422 kèm field code', async () => {
    const res = await api.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_PROJ', name: 'Trùng mã' },
    });
    expect(res.status()).toBe(422);
    expect(await res.text()).toContain('code');
});

test('không quyền thì 403', async () => {
    // dùng context đăng nhập bằng tài khoản KHÔNG có quyền quản lý danh mục
    const res = await noPermApi.post('/api/v1/meeting/room-amenities', {
        data: { code: 'E2E_X', name: 'X' },
    });
    expect(res.status()).toBe(403);
});
```

- [ ] **Bước 2: Chạy spec, xác nhận ĐỎ**

```bash
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/meeting/room-amenity.api.spec.ts --workers=1
```
Kỳ vọng: FAIL 404 (route chưa có).

- [ ] **Bước 3: Viết Service + Request + 2 Resource + Controller** theo khuôn đã nêu ở trên.

Request:

```php
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
```

⚠️ Controller `updateOrCreate` phải **rethrow `ValidationException`** trước khi catch `Exception`
(xem `MeetingCancelReasonController.php:60-66`), nếu không FE mất thông tin field và không hiện được lỗi inline.

- [ ] **Bước 4: Khai route**

```php
Route::group(['prefix' => 'meeting/room-amenities'], function () {
    Route::get('/getAll', [MeetingRoomAmenityController::class, 'getAll']);
    Route::get('/', [MeetingRoomAmenityController::class, 'index'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp');
    Route::post('/', [MeetingRoomAmenityController::class, 'updateOrCreate'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'show']);
    Route::delete('/{meetingRoomAmenity}', [MeetingRoomAmenityController::class, 'destroy'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}/lock', [MeetingRoomAmenityController::class, 'lock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
    Route::get('/{meetingRoomAmenity}/unlock', [MeetingRoomAmenityController::class, 'unlock'])->middleware('checkPermission:Quản lý danh mục tiện nghi phòng họp');
});
```

⚠️ Route `/getAll` phải đặt **TRƯỚC** route wildcard `/{meetingRoomAmenity}`, nếu không bị nuốt.

- [ ] **Bước 5: Chạy lại spec, xác nhận XANH** (đọc dòng tổng kết, không nhìn cuối log).

---
