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

## ⚠️ 3 cái bẫy đã đo thật trước khi lên plan — đọc kỹ, đừng lặp lại

**Bẫy 1 — Gửi thông báo nhầm người.** `EmployeeInfoService::sendToAllNotification($ids, $data)` nhận
**`employee_info_id`**, KHÔNG phải `employees.id`. Đã đo trên DB gộp: **chỉ 2/1099 nhân viên có
`id == employee_info_id`**. Bảng của phần phòng họp lưu `employee_id` (= `employees.id`), nên truyền thẳng
vào là **thông báo bay sang người khác** — không lỗi, không log, chỉ sai người nhận.
⇒ Mọi chỗ gửi thông báo phải map qua `employees.employee_info_id` trước. Viết **một** helper dùng chung,
đừng map lẻ ở từng chỗ.

**Bẫy 2 — Sinh mã phiếu kiểu cũ sẽ nổ.** Khuôn `getNextCode()` của dự án (`BomList.php:175-179`) dùng
`max('id') + 1`. Phase 1 đã thêm **`unique('code')`** cho `meeting_room_bookings`, nên 2 request song song
sinh cùng mã → 1 request chết bằng lỗi SQL thô (`Duplicate entry`), user thấy lỗi 500 vô nghĩa.
⇒ Sinh mã trong **cùng transaction** với `lockForUpdate`, hoặc bắt `QueryException` mã 1062 rồi sinh lại
(retry tối đa 3 lần). Phải có test 2 request song song chứng minh không ra 500.

**Bẫy 3 — Điều kiện tiên quyết từ review Phase 1**: `MeetingRoomController::destroy()` kiểm `isCanDelete()`
rồi mới mở transaction, **không `lockForUpdate`**. Phase 1 chưa ai ghi được vào bảng phiếu nên cửa sổ lỗi
chưa tồn tại; **mở luồng đặt phòng là nó thành thật ngay** (đặt phòng đúng lúc admin bấm Xóa → phiếu mồ côi).
⇒ Task 11 phải xử trước khi bật API tạo phiếu.

## Task 13: API tạo / sửa phiếu + chống trùng (phần khó nhất của cả feature)

**Files:** `Services/MeetingRoomBookingService.php`, `Http/Controllers/Api/V1/MeetingRoomBookingController.php`,
`Http/Requests/MeetingRoomBooking/MeetingRoomBookingRequest.php`, `Transformers/MeetingRoomBooking/*`,
`Routes/api.php`; test `e2e/tests/meeting/meeting-room-booking.api.spec.ts`

**Validate khi lưu (spec 5.1):** `end_at > start_at`; nằm trong giờ mở cửa phòng **chỉ khi phiếu gọn trong 1 ngày**
(qua đêm thì bỏ kiểm này nhưng chặn `> 72 giờ`); không đặt quá khứ; không quá `meeting_room_max_advance_days`;
phòng `status = 1`; khác công ty thì phòng phải `allow_cross_company = 1`;
**số người > sức chứa → CẢNH BÁO, KHÔNG chặn, KHÔNG tự sửa số user nhập**.

**Luật trùng (spec 5.2)** — phải đúng từng vế:
- Phòng `require_approval = 0` → phiếu tạo ra là **Đã duyệt** ngay; trùng với phiếu Đã duyệt là **chặn 422**,
  lỗi trả về **gắn đúng field giờ** kèm tên cuộc họp đang giữ chỗ.
- Phòng `require_approval = 1` → phiếu **Chờ duyệt**, **cho phép nhiều phiếu chờ duyệt trùng giờ**.
- Phiếu **Đã duyệt** thì không ai đặt đè, kể cả xin duyệt.

- [ ] **Bước 1: Viết spec e2e ĐỎ trước**, gồm ca **2 request song song**:

```ts
const [a, b] = await Promise.all([
    api.post('/api/v1/meeting/room-bookings', { data: payloadTrungGio }),
    api.post('/api/v1/meeting/room-bookings', { data: payloadTrungGio }),
]);
const codes = [a.status(), b.status()].sort();
expect(codes).toEqual([200, 422]);          // đúng 1 cái thắng
expect(await countBookings(roomId)).toBe(1); // KHÔNG được lọt 2 phiếu
```

- [ ] **Bước 2: Chạy, xác nhận ĐỎ (404).**
- [ ] **Bước 3: Service — kiểm trùng trong transaction có khóa:**

```php
return DB::transaction(function () use ($request) {
    // Khóa mọi phiếu còn hiệu lực của phòng trong khoảng ngày liên quan.
    // SELECT rồi INSERT mà không khóa: 2 request cách nhau 200ms lọt cả hai — lỗi kinh điển của bài toán đặt chỗ.
    $conflicts = MeetingRoomBooking::where('meeting_room_id', $roomId)
        ->whereIn('status', [MeetingRoomBooking::STATUS_DA_DUYET])
        ->where('start_at', '<', $endAt)
        ->where('end_at', '>', $startAt)
        ->lockForUpdate()
        ->get();
    if ($conflicts->isNotEmpty()) {
        throw ValidationException::withMessages(['start_at' => 'Phòng đã có cuộc họp "' . $conflicts->first()->title . '" lúc …']);
    }
    // sinh mã trong cùng transaction (xem bẫy 2)
    …
});
```

- [ ] **Bước 4: Sinh mã `DPH-YYYY-NNNNN` an toàn** — trong cùng transaction, và bọc `QueryException` mã 1062
  để sinh lại tối đa 3 lần. Test song song ở bước 1 phải không ra 500.
- [ ] **Bước 5: Resource trả đủ cờ hành động + thời gian ISO-8601** (quy ước cho app mobile, spec 6.4):
  `is_can_edit/cancel/approve/reject/checkin/checkout`, `start_at` dạng `2026-09-17T14:00:00+07:00` kèm
  `start_at_text`, `status_text`, `status_color`.
- [ ] **Bước 6: Sửa phiếu** — chỉ người đặt, chỉ khi **chưa tới giờ bắt đầu**; đổi giờ/phòng thì chạy lại toàn bộ
  kiểm tra; phòng cần duyệt thì phiếu **quay về Chờ duyệt**. Phiếu đã tới giờ: BE trả **423**, không phải 422.
- [ ] **Bước 7: Chạy lại spec, XANH**, đọc dòng tổng kết.
