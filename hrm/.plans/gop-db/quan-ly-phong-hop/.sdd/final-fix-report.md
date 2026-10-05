# Báo cáo đợt fix sau review tổng — Phase 1 "Quản lý phòng họp"

Ngày: 2026-09-18
BE: `hrm-worktrees/phong-hop-api` (nhánh `feat/quan-ly-phong-hop`)
FE: `hrm-worktrees/phong-hop-client`

## Status: HOÀN THÀNH toàn bộ A–H (1 mục phụ trong G.3 không dựng được data sạch — ghi rõ lý do bên dưới)

## Danh sách A–H

- **A. Xóa phòng để lại rác pivot** — XONG
  - A.1: `MeetingRoomService::destroy()` gọi `$meetingRoom->amenities()->detach()` trước `delete()`, cùng transaction (controller đã bọc sẵn).
  - A.2: `MeetingRoomAmenityController::index()` — câu đếm `used_count` đổi sang JOIN `meeting_rooms`, cùng luật với `MeetingRoomAmenity::isCanDelete()`.
  - A.3: Migration mới `2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table.php` — dọn pivot mồ côi 2 chiều rồi thêm FK CASCADE cho `meeting_room_room_amenity` (cả 2 cột). Đã chạy sạch, xác nhận bằng `SHOW CREATE TABLE`.
  - A.4: Ca e2e API `room-amenity.api.spec.ts` test 6 — tạo phòng gắn tiện nghi → xóa phòng → tiện nghi đó `is_can_delete = true` và `DELETE` trả 200. PASS.

- **B. Sửa phòng làm mất im lặng tiện nghi khóa / quản lý đã nghỉ việc** — XONG
  - B.1: `MeetingRoomService::formOptions()` nhận `room_id` (optional) — trả kèm tiện nghi đã khóa mà phòng đó đang dùng, cờ `is_locked`.
  - B.2: `MeetingRoomModal.vue` — `employeeOptions()` chèn option quản lý không có trong `$store.state.employees` (đã nghỉ việc), dùng `manager_name` từ API detail, `is_locked: true`. FE gọi `form-options?room_id=<id>` khi `this.id` có giá trị.
  - B.3: KHÔNG viết `templateResult` riêng — dựa hoàn toàn vào `utils/select2LockedOption.js` đã gọi sẵn trong `V2BaseSelectInModal`.
  - B.4: Ca e2e API mới (`meeting-room.api.spec.ts` test 8) — tạo tiện nghi, gắn phòng, khóa tiện nghi, gọi `form-options?room_id=` → tiện nghi khóa vẫn có mặt + `is_locked=true`; đồng thời kiểm không rò sang phòng khác. PASS.
  - **Kiểm bằng Playwright MCP thật (bắt buộc theo CLAUDE.md vì đây là thay đổi UI)**: tạo phòng thật qua API, gắn 1 tiện nghi rồi khóa tiện nghi đó, gán `manager_employee_id=26` (nhân viên `status=0`, đã nghỉ). Mở modal Sửa trên trình duyệt thật (port 3001) — đo DOM `.select2-selection__rendered` / `.select2-selection__choice`:
    - Chip quản lý: `"×🔒 Bùi Văn Long"` — value giữ nguyên, có dấu khóa.
    - Chip tiện nghi: `"×🔒 Tiện nghi verify khóa"` — value giữ nguyên, có dấu khóa.
    - Bấm Lưu → `GET rooms/183` sau lưu vẫn còn `manager_employee_id: 26` và tiện nghi id 299 (so `updated_at` đã đổi, chứng minh có ghi đè thật, không phải cache cũ) — **không mất dữ liệu khi lưu lại**, đúng như brief cảnh báo.
    - Đã dọn dữ liệu test thủ công này (mở khóa, xóa phòng, xóa tiện nghi) ngay sau khi đo xong.

- **C. e2e hard-code đường dẫn worktree** — XONG
  - `meeting-room.spec.ts` Nhóm E: `WORKTREE_API_REPO` đổi thành `process.env.API_REPO || path.join(__dirname, '..', '..', '..', 'hrm-api')` — mặc định trỏ checkout chính `HRM/hrm-api`, đã xác nhận thư mục + `.env` tồn tại.
  - Thêm khối comment đầu file liệt kê `BASE_URL`, `API_BASE`, `API_REPO` (mặc định + cách override) và 3 file `.auth/*-wt.json` cần có trước khi chạy.

- **D. Route xem chi tiết tiện nghi thiếu gate** — XONG
  - `Modules/Meeting/Routes/api.php` — route `GET /{meetingRoomAmenity}` (show) gắn `checkPermission:Quản lý danh mục tiện nghi phòng họp|Xem danh mục tiện nghi phòng họp`, khớp route song sinh `show` của phòng họp.

- **E. Xóa code chết `getAll`** — XONG
  - Xóa route `GET /getAll`, `MeetingRoomAmenityController::getAll()`, `MeetingRoomAmenityService::getAll()`. Grep FE xác nhận không nơi nào gọi (`grep -rn "room-amenities.*getAll"` rỗng).

- **F. Không gửi `department_id`/`part_id` khi lưu phòng** — XONG (kèm lưu ý quan trọng, xem mục Concerns)
  - `MeetingRoomService::updateOrCreate()` bỏ 2 cột khỏi `$request->only([...])`. Cột DB giữ nguyên.

- **G. 2 ca test xanh giả + coverage thiếu** — XONG
  - G.1: `meeting-room.api.spec.ts` ca 6 — thay `expect(text).not.toContain('checkin_qr_token')` (chạy trên body 403 `{message,code}`, luôn xanh) bằng assert đúng khuôn body lỗi của middleware `checkPermission` (`toHaveProperty('message')`, `not.toHaveProperty('data')`).
  - G.2: ca 4 — thêm setup tạo 1 tiện nghi ACTIVE riêng cho ca này + `expect(res.data.amenities.length).toBeGreaterThan(0)` trước vòng lặp.
  - G.3: thêm 2 ca CHẶN XÓA:
    - Tiện nghi đang gắn phòng → `DELETE` trả 400, `is_can_delete=false` (`room-amenity.api.spec.ts` test 5). PASS.
    - **Phòng đã có phiếu đặt → CHƯA TEST ĐƯỢC.** Lý do: `meeting_room_bookings` chưa có BE endpoint tạo phiếu (Phase 2 chưa triển khai — `upcomingBookings()` hiện trả `items: []` cố định, không có service/model insert). Cách duy nhất tạo dữ liệu "sạch" là chèn thẳng SQL vào bảng nghiệp vụ phức tạp (nhiều cột NOT NULL: `status`, `booked_by_employee_id`, khuôn `code` sinh tự động DPH-YYYY-NNNNN chưa có logic) mà không có bất kỳ code path nào trong hệ thống xác nhận là đúng — làm vậy là bịa dữ liệu giả cho ca test giả, không phải test thật. Đã KHÔNG thêm ca này, đúng theo hướng dẫn của brief ("đừng bịa ca giả"). `MeetingRoom::isCanDelete()` (đọc thẳng `meeting_room_bookings`) và route `destroy` chặn `is_can_delete=false` → 400 đã có sẵn logic, chỉ thiếu ca test tới khi Phase 2 có endpoint tạo phiếu thật.
  - G.4: Port lại ca menu — thêm Nhóm F (`F1`, `F2`) vào `meeting-room.spec.ts`: "Danh sách phòng họp" + "Tiện nghi phòng họp" có `href` đúng, "Đăng ký phòng họp" không có `href`. PASS cả 3 lần chạy.

- **H. `unique('code')` cho `meeting_room_bookings`** — XONG
  - Gộp vào cùng migration `2026_09_18_000001_...` (đúng gợi ý "gộp chung file migration ở mục A.3 cũng được"). Xác nhận `SHOW CREATE TABLE meeting_room_bookings` có `UNIQUE KEY mrb_code_unique (code)`.

## Số dòng pivot mồ côi trước/sau

- Trước khi sửa (đo bằng đúng câu `DELETE ... LEFT JOIN ... WHERE ... IS NULL` dạng SELECT COUNT): **78 dòng** mồ côi cả 2 chiều (`meeting_room_id` lẫn `meeting_room_amenity_id`, do 2 bảng cha `meeting_rooms`/`meeting_room_amenities` tại thời điểm đo đều đang 0 dòng — pivot 100% trỏ tới bản ghi đã bị xóa từ trước).
- Sau khi chạy migration: **0 dòng** mồ côi (xác nhận lại lần nữa sau khi chạy trọn bộ e2e 2 lần mỗi bộ + kiểm tra thủ công bằng Playwright — vẫn 0).

## Kết quả migration

```
php artisan migrate --path=Modules/Meeting/Database/Migrations --force
Migrating: 2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table
Migrated:  2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table (836.13ms)
```

`SHOW CREATE TABLE meeting_room_room_amenity` xác nhận:
```
CONSTRAINT `mr_room_amenity_amenity_fk` FOREIGN KEY (`meeting_room_amenity_id`) REFERENCES `meeting_room_amenities` (`id`) ON DELETE CASCADE,
CONSTRAINT `mr_room_amenity_room_fk` FOREIGN KEY (`meeting_room_id`) REFERENCES `meeting_rooms` (`id`) ON DELETE CASCADE
```
`SHOW CREATE TABLE meeting_room_bookings` xác nhận: `UNIQUE KEY mrb_code_unique (code)`.

## Dòng tổng kết từng lần chạy test (đọc đúng dòng cuối, không suy diễn từ "không thấy failed")

**project=api** (tests/meeting, `--no-deps --workers=1`):
- Lần 1 (trước khi thêm ca B.4): `13 passed (22.0s)`
- Lần 2 (trước khi thêm ca B.4): `13 passed (20.6s)`
- Lần 3 (sau khi thêm ca B.4, test 8): `14 passed (27.2s)`
- Lần 4 (lặp lại chống flaky): `14 passed (21.3s)`
- Lần 5 (final, sau khi dọn dữ liệu verify tay): `14 passed (21.2s)`

**project=chromium** (tests/meeting, `--no-deps --workers=1`):
- Lần 1: `14 passed (1.9m)`
- Lần 2 (lặp lại chống flaky): `14 passed (2.0m)`
- Lần 3 (final, sau khi thêm ca B.4 ở BE): `14 passed (2.1m)`

Không có ca nào in "did not run" ở bất kỳ lần chạy nào (bộ chạy `serial`, đã đọc kỹ dòng tổng kết mỗi lần theo đúng cảnh báo trong CLAUDE.md).

## Kiểm chứng cuối (mục KIỂM CHỨNG BẮT BUỘC)

1. Migration chạy sạch — xem trên.
2. Pivot mồ côi = 0 — xác nhận lại lần cuối cùng.
3. Cả 2 project chạy 2 lần, đọc dòng tổng kết — xem trên (thực tế chạy > 2 lần vì có thêm ca B.4 giữa chừng, lần nào cũng full pass).
4. Sau khi chạy: `SELECT COUNT(*) FROM meeting_rooms WHERE code LIKE 'E2E%'` = 0, tương tự `meeting_room_amenities` = 0; pivot mồ côi = 0; `SELECT COUNT(*) FROM permissions WHERE guard_name='api'` = **745** (không đổi).
5. 2 lệnh grep tự kiểm FE (`pages/meeting/rooms/`, `pages/meeting/room-amenities/` với `<input |<textarea|<select |<button |<label |class="btn |class="form-control` trừ `V2Base`) — cả 2 RỖNG.

## Concerns

1. **Mục F chỉ chặn được đường "client tự gửi `department_id`/`part_id`"**, KHÔNG chặn được auto-fill của `App\Models\BaseModel::boot()` (hook `creating`/`saving` dùng chung toàn hệ thống) — hook này tự điền `department_id`/`part_id` từ `employee_info` của NGƯỜI ĐANG TẠO bất cứ khi nào cột đó trống lúc `create()`, bất kể `$data` có key đó hay không. Đã đo thật: tạo phòng test qua API (không gửi `department_id`/`part_id`) vẫn ra `department_id: 36, part_id: 20` (đơn vị của tài khoản admin token đang dùng). Đây là hành vi CÓ SẴN của `BaseModel`, dùng chung cho toàn bộ project — theo CLAUDE.md ("sửa hàm dùng chung → hỏi ý kiến trước khi làm") KHÔNG tự sửa. Task chỉ yêu cầu "bỏ 2 cột khỏi payload lưu" (đã làm đúng nghĩa đen), nhưng nếu Phase 2 thực sự cần `department_id`/`part_id` của phòng KHÔNG bị lệch theo người tạo, cần bàn thêm hướng xử lý riêng (ví dụ: sau khi `create()` xong thì set lại `null` tường minh, hoặc thêm ô chọn ở form).
2. **G.3 phần "phòng đã có phiếu đặt"** chưa có ca test — lý do đã nêu ở mục G phía trên (chưa có BE endpoint tạo booking ở Phase 1/Phase 2 chưa triển khai). Logic chặn xóa (`MeetingRoom::isCanDelete()`) đã tồn tại sẵn và đúng dạng với logic tiện nghi (đã test được), chỉ thiếu data thật để phủ bằng e2e.
3. Dữ liệu dùng để kiểm B bằng Playwright MCP (room `MANUALVERIFY_RM_...`, amenity `MANUALVERIFY_AM_...`, employee id 26 mượn tạm làm quản lý) đã được dọn sạch (mở khóa tiện nghi → xóa phòng → xóa tiện nghi) ngay sau khi đo xong, xác nhận lại bằng query — 0 dòng còn sót.
4. Phiên Playwright MCP dùng `localStorage.setItem('access_token', ...)` (token từ `.auth/user-wt.json`) để đăng nhập vào `127.0.0.1:3001` — theo đúng cơ chế mà cả bộ e2e `storageState` đang dùng, không phải hình thức đăng nhập lạ.

## File đã sửa

**BE** (`hrm-worktrees/phong-hop-api`):
- `Modules/Meeting/Services/MeetingRoomService.php`
- `Modules/Meeting/Services/MeetingRoomAmenityService.php`
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php`
- `Modules/Meeting/Routes/api.php`
- `Modules/Meeting/Database/Migrations/2026_09_18_000001_add_foreign_keys_to_meeting_room_room_amenity_table.php` (mới)

**FE** (`hrm-worktrees/phong-hop-client`):
- `pages/meeting/rooms/components/MeetingRoomModal.vue`

**e2e** (`ERP-HRM/HRM/e2e/tests/meeting/`):
- `meeting-room.api.spec.ts` (sửa ca 6, ca 4; thêm ca 8)
- `room-amenity.api.spec.ts` (thêm ca 5, ca 6)
- `meeting-room.spec.ts` (sửa `WORKTREE_API_REPO` → `API_REPO` env; thêm header doc; thêm Nhóm F)

## Fix vòng 2

### Việc 1 — ca 6 (`room-amenity.api.spec.ts`) xanh giả, thêm assert thẳng bảng pivot

- **Vấn đề**: ca 6 chỉ assert `is_can_delete === true` và `DELETE → 200`, cả hai đường đều đi qua
  `MeetingRoomAmenity::isCanDelete()` = `rooms()->exists()` (đã `JOIN meeting_rooms`) — dòng pivot
  mồ côi (phòng đã xóa nhưng chưa `detach()`) vô hình với nó, nên ca này không bảo vệ được gì cho
  phần fix quan trọng nhất (mục A.3/A.4 vòng 1).
- **Sửa**: copy nguyên khuôn `runMysql()`/`readEnvValue()` từ `meeting-room.spec.ts` (đọc credential
  qua `process.env.API_REPO`, mặc định checkout chính, không hard-code mật khẩu/đường dẫn tuyệt đối)
  sang `room-amenity.api.spec.ts`. Thêm hàm `countPivotRowsForRoom(roomId)` chạy
  `SELECT COUNT(*) FROM meeting_room_room_amenity WHERE meeting_room_id=<id>` và thêm 1 dòng assert
  `toBe(0)` ngay sau khi `DELETE /meeting/rooms/{roomId}` trả 200, **giữ nguyên** 2 assert cũ
  (`is_can_delete`, `DELETE 200`).

**Đối chứng âm** — tạm gỡ đúng cơ chế đang test:
1. `MeetingRoomService::destroy()`: comment dòng `$meetingRoom->amenities()->detach();`.
2. DB: `ALTER TABLE meeting_room_room_amenity DROP FOREIGN KEY mr_room_amenity_amenity_fk, DROP FOREIGN KEY mr_room_amenity_room_fk;`
3. Chạy riêng ca 6 (`-g "6\. xóa phòng"`, project `api`) → **ĐỎ đúng chỗ**, đúng dòng assert mới thêm:
   ```
   Error: pivot của phòng vừa xoá phải sạch, không còn dòng mồ côi
   Expected: 0
   Received: 1
   ```
   (in cả ở lần chạy đầu và lần retry #1 — 2/2 đỏ đúng chỗ, không flake).
4. Dọn 2 dòng pivot mồ côi phát sinh trong lúc đối chứng (test bị fail nên không tới được bước
   xóa tiện nghi; `afterAll` vẫn xóa amenity qua `createdIds`, để lại pivot mồ côi cả 2 chiều) —
   xác nhận lại `orphan pivot rows = 0` trước khi thêm lại FK (bắt buộc, nếu không `ALTER TABLE
   ... ADD CONSTRAINT` sẽ báo lỗi vì dữ liệu hiện có vi phạm khóa ngoại).
5. Thêm lại đúng 2 FK cũ (cùng tên constraint, cùng cột, cùng `ON DELETE CASCADE`):
   ```sql
   ALTER TABLE meeting_room_room_amenity
     ADD CONSTRAINT mr_room_amenity_room_fk FOREIGN KEY (meeting_room_id) REFERENCES meeting_rooms (id) ON DELETE CASCADE,
     ADD CONSTRAINT mr_room_amenity_amenity_fk FOREIGN KEY (meeting_room_amenity_id) REFERENCES meeting_room_amenities (id) ON DELETE CASCADE;
   ```
6. Bỏ comment lại `detach()` — `git diff Modules/Meeting/Services/MeetingRoomService.php` (so với
   bản gốc trong git index của worktree) **rỗng**, xác nhận hoàn nguyên đúng nguyên văn.
7. Chạy lại riêng ca 6 → **XANH**:
   ```
   ✓  1 [api] › tests/meeting/room-amenity.api.spec.ts:272:5 › 6. xóa phòng thì tiện nghi từng gắn phòng đó phải xóa được (pivot đã được detach) (2.3s)
   1 passed (4.5s)
   ```

`SHOW CREATE TABLE meeting_room_room_amenity` sau khi hoàn nguyên — đủ 2 FK CASCADE, đúng tên,
đúng cột như trước khi đối chứng:
```
CONSTRAINT `mr_room_amenity_amenity_fk` FOREIGN KEY (`meeting_room_amenity_id`) REFERENCES `meeting_room_amenities` (`id`) ON DELETE CASCADE,
CONSTRAINT `mr_room_amenity_room_fk` FOREIGN KEY (`meeting_room_id`) REFERENCES `meeting_rooms` (`id`) ON DELETE CASCADE
```

### Việc 2 — gate route `GET /meeting/rooms/form-options`

- `Modules/Meeting/Routes/api.php`: thêm
  `->middleware('checkPermission:Quản lý danh mục phòng họp|Xem danh mục phòng họp')` cho route
  `form-options`, khớp gate của route `index` song sinh.
- **Kiểm không làm chết form** (Playwright MCP thật, port 3001, token `.auth/user-wt.json` — tài
  khoản admin có quyền, bơm vào `localStorage.access_token` rồi navigate — đúng cơ chế đăng nhập
  bộ e2e đang dùng):
  - Mở `/meeting/rooms`, bấm "Tạo mới" → modal "Thêm phòng họp" mở, network log ghi 2 lần
    `GET .../meeting/rooms/form-options => [200] OK`.
  - Mở combobox "Chọn công ty" → 5 option công ty hiện đủ (load thật từ `form-options`, không rỗng).
  - Không submit gì, đóng tab, không tạo bản ghi nào.
  - Đối chứng phía không quyền: `curl` bằng token `.auth/user-nocost-wt.json` gọi thẳng
    `GET /meeting/rooms/form-options` → **403** (gate thật sự chặn, không phải mở hờ).

## Kết quả 2 bộ test — Fix vòng 2 (đọc dòng tổng kết, serial)

**project=api** (`tests/meeting`, `--no-deps --workers=1`): `14 passed (24.3s)`

**project=chromium** (`tests/meeting`, `--no-deps --workers=1`): `14 passed (2.0m)`

Không có ca nào in "did not run".

## Kiểm chứng DB cuối — Fix vòng 2

```
meeting_rooms E2E leftover          = 0
meeting_room_amenities E2E leftover = 0
orphan pivot rows                   = 0
permissions guard=api                = 745
```

`SHOW CREATE TABLE meeting_room_room_amenity` — đủ 2 FK CASCADE như trên.

## File đã sửa — Fix vòng 2

- `HRM/e2e/tests/meeting/room-amenity.api.spec.ts` (thêm `runMysql`/`readEnvValue`/
  `countPivotRowsForRoom`, thêm 1 assert vào ca 6)
- `hrm-worktrees/phong-hop-api/Modules/Meeting/Routes/api.php` (gate route `form-options`)
- `hrm-worktrees/phong-hop-api/Modules/Meeting/Services/MeetingRoomService.php` — **KHÔNG có thay
  đổi net** (dùng tạm để đối chứng âm rồi hoàn nguyên đúng nguyên văn, đã xác nhận qua diff rỗng)
