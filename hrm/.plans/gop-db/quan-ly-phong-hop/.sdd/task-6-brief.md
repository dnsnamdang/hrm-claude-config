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


## Task 6: API danh mục phòng họp

**Files:**
- Create: `Modules/Meeting/Services/MeetingRoomService.php`
- Create: `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php`
- Create: `Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php`
- Create: `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php`
- Modify: `Modules/Meeting/Routes/api.php`
- Test: `e2e/tests/meeting/meeting-room.api.spec.ts`

**Interfaces:**
- Consumes: `MeetingRoom`, `MeetingRoomAmenity` (Task 3)
- Produces:
  - `GET /api/v1/meeting/rooms` (lọc `keyword`, `company_id`, `capacity_from`, `amenity_ids[]`, `status`)
  - `GET /api/v1/meeting/rooms/form-options` → `{ amenities: [], companies: [], config: { open_time, close_time, checkin_grace_minutes } }`
  - `POST /api/v1/meeting/rooms`, `GET /{id}`, `DELETE /{id}`, `GET /{id}/lock`, `GET /{id}/unlock`
  - `GET /api/v1/meeting/rooms/{id}/upcoming-bookings` → `{ count: n, items: [...] }`

> **Ruling R1 (pre-flight):** `e2e/utils/` KHÔNG có helper `api` / `noPermApi` dùng chung — code mẫu dưới
> đây là mô tả ca kiểm, không phải code chạy nguyên văn. Mỗi spec **tự dựng `APIRequestContext`** theo khuôn
> `e2e/tests/assign/customer-demand-link.api.spec.ts` (đọc token từ `e2e/.auth/api.json`). Ca "không quyền"
> dùng tài khoản nocost có sẵn: `test.use({ storageState: '.auth/user-nocost.json' })` (sinh bởi
> `e2e/auth/login-nocost.setup.ts`). Nếu project `api-setup` đỏ trên DB gộp (bẫy đã biết: thiếu bảng
> `hrm_employees`) thì chạy spec lẻ bằng `--no-deps`.

- [ ] **Bước 1: Viết e2e API spec (đỏ trước)** — 5 ca:

```ts
test('mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho', async () => {
    await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'P.A301', company_id: 1 } });
    const dup = await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'Khác', company_id: 1 } });
    expect(dup.status()).toBe(422);

    const other = await api.post('/api/v1/meeting/rooms', { data: { code: 'A301', name: 'P.A301 CT2', company_id: 2 } });
    expect(other.status()).toBe(200);
});

test('tạo phòng là có sẵn checkin_qr_token', async () => {
    const res = await api.post('/api/v1/meeting/rooms', { data: { code: 'QR01', name: 'P.QR', company_id: 1 } });
    const id = (await res.json()).data.id;
    const detail = await (await api.get(`/api/v1/meeting/rooms/${id}`)).json();
    expect(detail.data.checkin_qr_token).toMatch(/^[0-9a-f-]{36}$/);
});

test('gắn nhiều tiện nghi rồi đọc lại đúng danh sách', async () => { /* post amenity_ids: [id1, id2] rồi GET detail */ });

test('form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty', async () => {
    const res = await (await api.get('/api/v1/meeting/rooms/form-options')).json();
    expect(res.data.config.open_time).toBeTruthy();
});

test('không quyền quản lý danh mục thì POST trả 403', async () => { /* noPermApi */ });
```

- [ ] **Bước 2: Chạy spec, xác nhận ĐỎ.**

- [ ] **Bước 3: Viết Request với unique theo công ty**

```php
'code' => [
    'required', 'string', 'max:50',
    Rule::unique('meeting_rooms', 'code')
        ->where(fn ($q) => $q->where('company_id', $this->input('company_id')))
        ->ignore($this->input('id')),
],
'name' => ['required', 'string', 'max:255'],
'company_id' => ['required', 'integer'],
'capacity' => ['nullable', 'integer', 'min:1'],
'manager_employee_id' => ['nullable', 'integer'],
'require_approval' => ['nullable', 'boolean'],
'allow_cross_company' => ['nullable', 'boolean'],
'open_time' => ['nullable', 'date_format:H:i:s'],
'close_time' => ['nullable', 'date_format:H:i:s', 'after:open_time'],
'checkin_grace_minutes' => ['nullable', 'integer', 'min:0', 'max:120'],
'amenity_ids' => ['nullable', 'array'],
'amenity_ids.*' => ['integer', 'exists:meeting_room_amenities,id'],
```

- [ ] **Bước 4: Service — `updateOrCreate` đồng bộ pivot trong transaction**

```php
return DB::transaction(function () use ($request) {
    $room = MeetingRoom::updateOrCreate(['id' => $request->input('id')], $request->only([...]));
    $room->amenities()->sync($request->input('amenity_ids', []));

    return $room->load('amenities');
});
```

- [ ] **Bước 5: Controller — `destroy` chặn xóa phòng đã có phiếu**

```php
if (!$meetingRoom->isCanDelete()) {
    return $this->responseJson(
        'Phòng họp này đã có phiếu đặt nên không xóa được. Bạn có thể Khóa phòng.',
        Response::HTTP_BAD_REQUEST
    );
}
```

- [ ] **Bước 6: Controller — `upcomingBookings` phục vụ cảnh báo trước khi Khóa**

```php
public function upcomingBookings(MeetingRoom $meetingRoom)
{
    return $this->responseJson('success', Response::HTTP_OK, [
        'count' => $meetingRoom->upcomingBookingCount(),
        'items' => [], // Phase 2 trả chi tiết khi đã có Resource của phiếu
    ]);
}
```

- [ ] **Bước 6b: Resource trả cờ hành động** — quy ước bắt buộc để app mobile không phải chép lại luật:

```php
'is_can_edit'   => $this->isCanEdit(),
'is_can_delete' => $this->isCanDelete(),
'is_can_lock'   => $this->isCanLockUpdate(),
'status_text'   => $this->status == MeetingRoom::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
```

⚠️ `isCanDelete()` truy vấn bảng phiếu → list phải `with('amenities')` và tính cờ theo lô, không gọi trong vòng lặp từng dòng (N+1).

- [ ] **Bước 7: Khai route** (đặt `/form-options` và `/getAll` TRƯỚC wildcard), gắn
`checkPermission:Quản lý danh mục phòng họp` cho POST/DELETE/lock/unlock, và
`checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp` cho `index`.

- [ ] **Bước 8: Chạy lại spec, xác nhận XANH.**

- [ ] **Bước 9: Kiểm N+1** — bật `DB::enableQueryLog()` tạm hoặc đọc Telescope: `GET /rooms?per_page=50`
phải **không** sinh 50 query cho tiện nghi (bắt buộc `with('amenities')`).

---
