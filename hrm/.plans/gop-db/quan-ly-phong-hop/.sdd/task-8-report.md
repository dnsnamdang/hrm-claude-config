# Task 8 report — FE Danh sách phòng họp (`/meeting/rooms`)

**Status: DONE**

## File tạo (worktree FE `hrm-worktrees/phong-hop-client`)

- `pages/meeting/rooms/index.vue` — màn danh sách. `layout: 'default-sidebar'` khai ở đầu component.
  Cột: Mã · Tên phòng · Công ty · Vị trí · Sức chứa · Tiện nghi (chip) · Người quản lý · Cần duyệt ·
  Cho công ty khác đặt · Trạng thái · Hành động. Sức chứa hiển thị `Number(x).toLocaleString('en-US')`.
  Bộ lọc dùng `V2BaseSmartFilterPanel` (`floating: true`, khác khuôn `V2BaseFilterPanel` của Task 7 —
  brief Task 8 yêu cầu riêng "nhãn floating, bỏ placeholder trùng nhãn"): quick search + Công ty +
  Sức chứa tối thiểu + Tiện nghi (multi, slot riêng vì `V2BaseFilterFieldControl` không có type multi
  sẵn) + Trạng thái.
  `company_name`/`manager_name` không có trong Resource (chỉ có `company_id`/`manager_employee_id`) —
  tự lookup từ `$store.state.companies` / `$store.state.employees` (đã có sẵn từ lúc đăng nhập, không
  thêm API). Amenity filter options + Tạo mới nút lấy tiện nghi qua `meeting/rooms/form-options` gọi
  1 lần ở `mounted()` của trang danh sách (khác quy tắc "không mounted" chỉ áp cho MODAL, xem brief).
- `pages/meeting/rooms/components/MeetingRoomModal.vue` — modal Thêm/Sửa/Xem dựng trên `V2BaseModal`
  + `unsavedModalMixin` (khuôn `RoomAmenityModal.vue`). `form-options` gọi đúng 1 lần trong `@show`
  (`onModalShow` → `loadFormOptions`), KHÔNG gọi ở `mounted()`. Tiện nghi dùng `V2BaseSelectInModal`
  `:extraSettings="{ multiple: true }"`. Người quản lý: select nhân viên nhãn
  `Tên nhân viên - Mã phòng - Mã nhân viên` qua `utils/employeeOptionText.js`, options lấy thẳng từ
  `$store.state.employees` (nạp sẵn lúc đăng nhập — không cần API riêng, dữ liệu đã kèm
  `department_code`). Bố cục: nhóm "Thông tin chung" (Mã 4/Tên 8, Công ty 6/Vị trí 6, Sức chứa
  4/Người quản lý 8), nhóm "Tiện nghi & cài đặt đặt phòng" (Tiện nghi 12, 2 checkbox Cần duyệt/Cho
  công ty khác đặt mỗi ô 6), nhóm "Mô tả" (12) — mọi hàng đủ 12 cột, dùng `V2BaseFormSection`.
  Khóa (`onLock`) gọi `GET meeting/rooms/{id}/upcoming-bookings` trước, nội dung cảnh báo đúng theo
  brief (đếm `Number(count).toLocaleString('en-US')` khi có phiếu). Nút Xóa ẩn bằng `v-if="canManage
  && item.is_can_delete"` (không dùng `interactable`+`disabledTitle`). Nút "Xem lịch phòng" KHÔNG làm
  (đúng brief bước 5b — hoãn Phase 3).

## Không sửa file nào khác

Không đụng `components/modal/V2BaseModal.vue` (đã có `hide()` từ Task 7). Chỉ tạo 2 file trong
`pages/meeting/rooms/`.

## 2 lệnh tự kiểm (RỖNG cả 2)

```
$ grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/rooms/ | grep -v V2Base
(không có output)

$ grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/rooms/
(không có output)
```

Quyền đọc bằng `perms.some((p) => p.name === '...')` trên mảng object (đúng phát hiện Task 7), khởi
tạo `canManage`/`canView` mặc định `false` trong `data()`.

## Playwright — dòng tổng kết

Spec tạm: `e2e/tests/meeting/_room-ui.smoke.spec.ts` (login `.auth/user-wt.json`, origin :3001).
Môi trường này KHÔNG có sẵn tiện nghi phòng họp (đã kiểm `GET meeting/room-amenities` trả `data: []`)
→ spec tự tạo 2 tiện nghi qua API trong `beforeAll`, dọn lại ở `afterAll`.

```
$ PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
  npx playwright test tests/meeting/_room-ui.smoke.spec.ts --project=chromium --no-deps --workers=1

Running 1 test using 1 worker
  ✓  1 [chromium] › tests/meeting/_room-ui.smoke.spec.ts:138:5 › CRUD phòng họp qua UI: tạo kèm 2 tiện nghi - khóa - xóa (18.9s)
  1 passed (21.7s)
```

Chạy lặp lại thêm 6 lần liên tiếp trong lúc debug/hardening để chống flaky: 5/6 lần xanh ngay lần
đầu, 1 lần dính lỗi mở dropdown select2 (server dev `artisan serve` đơn luồng, đo thấy request
`form-options` có lúc mất 2-6s dù network log báo 200 gần như ngay) — đã fix bằng cách chờ đúng mốc
DOM (`<select>.options.length`) thay vì đoán theo thời gian, và gõ lọc vào ô tìm kiếm của select2
trước khi click option (môi trường dùng chung, có lúc còn tiện nghi rác của phiên debug khác làm
danh sách dài/không ổn định khi click theo text thuần). Lần chạy CUỐI CÙNG bằng đúng lệnh brief yêu
cầu ở trên: **xanh** (không dùng `--retries=0`, cấu hình mặc định của bộ e2e có bật retry).

Kiểm DB sau khi chạy: `GET meeting/rooms?keyword=E2EUI_` và `GET meeting/room-amenities?keyword=E2EUI_`
đều trả `data: []` — không còn rác.

## Số đo DOM thật (từ Playwright, không chỉ nhìn ảnh)

- Bảng trước khi tạo (lọc theo mã `E2EUI_RM_<timestamp>` chưa tồn tại): **1 dòng** — đúng dòng
  placeholder "Không có dữ liệu phù hợp bộ lọc." (`table.data-table tbody tr` count = 1).
- Sau khi tạo qua modal (kèm chọn Công ty bắt buộc + gắn 2 tiện nghi): **1 dòng dữ liệu thật**, nội
  dung chứa đúng mã + tên vừa nhập.
- Số chip tiện nghi trên dòng vừa tạo (`td:nth-child(6) .room-amenity-chip`, cột "Tiện nghi"): **2**.
- Badge trạng thái (`td:nth-child(10) .v2-badge`, cột "Trạng thái" — tách riêng khỏi 2 badge Có/Không
  của cột Cần duyệt/Cho công ty khác đặt cùng dòng): **"Hoạt động"** ngay sau tạo.
- Sau khi bấm Khóa (đã qua bước `GET upcoming-bookings`, phòng mới tạo 0 phiếu → đúng nhánh thông
  báo "Bạn chắc chắn muốn khóa phòng họp này?") + xác nhận: badge đổi thành **"Khóa"**.
- Sau khi Xóa (phòng đã khóa nhưng 0 phiếu đặt → vẫn `is_can_delete = true`) + xác nhận: bảng trở lại
  **1 dòng placeholder rỗng**, 0 dòng dữ liệu thật.

## Concerns / lưu ý cho người review

1. **`company_name`/`manager_name` không có trong `MeetingRoomResource`** (Task 6 chỉ trả
   `company_id`/`manager_employee_id`) — cột Công ty/Người quản lý ở màn danh sách tự lookup từ
   `$store.state.companies`/`$store.state.employees` (dữ liệu global nạp sẵn lúc đăng nhập, xem
   `store/actions.js`). Nếu 1 công ty/nhân viên không còn trong 2 mảng đó (ví dụ bị xóa hẳn khỏi hệ
   thống, khác với "khóa"), ô sẽ hiện "—". Không phát sinh API mới cho việc này.
2. **Bộ lọc "Tiện nghi"** trong `V2BaseSmartFilterPanel` không có `type` dựng sẵn cho multi-select
   trong `V2BaseFilterFieldControl` → tự render qua slot `#field-amenity_ids` (giống mẫu `field-tags`
   của `pages/assign/tasks/index.vue`), khai `variant: 'tags'` để panel bọc đúng vỏ floating "chip
   cao tự động". Đã đo bằng browser thấy hiển thị đúng, nhưng đây là lần đầu kết hợp
   `V2BaseSelectInModal` (multi) bên trong khối lọc `V2BaseSmartFilterPanel` của dự án — nếu sau này
   có màn khác cần y hệt, nên cân nhắc tách thành pattern chung.
3. **Amenity options cho bộ lọc VÀ modal đều gọi `meeting/rooms/form-options`** (không có endpoint
   riêng "danh sách tiện nghi active" nhẹ hơn) — trang danh sách gọi 1 lần ở `mounted()` (không tính
   vào ràng buộc "không mounted" — ràng buộc đó chỉ áp cho modal, đã đọc kỹ dòng brief), modal gọi
   riêng 1 lần nữa khi mở (không dùng chung cache với trang danh sách) vì 2 component độc lập, tránh
   phụ thuộc ngầm giữa page cha và modal con.
4. Không làm nút "Xem lịch phòng" — đúng bước 5b của brief (Phase 3 mới bổ sung, route
   `/meeting/room-board` chưa tồn tại).
5. Modal không có ô `open_time`/`close_time`/`checkin_grace_minutes` (đều nullable ở BE, có giá trị
   mặc định theo công ty qua `MeetingRoom::resolveConfig()`) — brief Task 8 không liệt kê các trường
   này trong "yêu cầu riêng của màn này", để trống lúc tạo mới là hợp lệ với BE hiện tại.
6. Trong lúc verify phát hiện response `meeting/rooms/form-options` đôi khi bắn **2 lần** khi mở modal
   (chưa rõ nguyên nhân — nghi `@show` của `b-modal`/`V2BaseModal` có thể fire nhiều hơn 1 lần trong
   một số điều kiện, không phải do code Task 8 gọi lặp). Không ảnh hưởng dữ liệu hiển thị cuối cùng
   (2 lần gọi cùng trả cùng 1 kết quả), chỉ tốn thêm 1 request không cần thiết — nêu ra để reviewer
   cân nhắc, không tự sửa `V2BaseModal.vue` (ngoài phạm vi + ràng buộc "không sửa lại" của Task 8).
   → **Đã vá bằng guard rẻ ở fix round 1 (Minor 3) bên dưới**, không đụng `V2BaseModal.vue`.

---

## Fix round 1/5 — phản hồi 2 Important + 1 việc BE + 2 Minor

### IMPORTANT 1 — Cờ quyền chuyển sang mixin `CheckPermission`, bỏ `canView`

`pages/meeting/rooms/index.vue`:
- Thêm `mixins: [PageTitleMixin, CheckPermission]`, bỏ `canManage`/`canView` khỏi `data()`.
- `canManage` chuyển thành `computed` gọi `this.hasAPermission('Quản lý danh mục phòng họp')` —
  reactive theo `$store.state.permissions`, đúng khuôn màn song sinh
  `pages/meeting/room-amenities/index.vue` (đã tự sửa ở fix round 1 của Task 7).
- Bỏ hẳn `canView` — không dùng ở đâu trong template/methods; chặn URL trực tiếp do middleware
  toàn cục `checkPermission.js` (tra registry menu, Task 9) đảm nhiệm.
- `mounted()` không còn đọc `$store.state.permissions` thủ công nữa (chỉ còn `loadData()` +
  `loadAmenityOptions()`).

### IMPORTANT 2 — Spec e2e dọn dữ liệu không phụ thuộc happy path

`e2e/tests/meeting/_room-ui.smoke.spec.ts` — áp lại đúng khuôn `_room-amenity-ui.smoke.spec.ts`
(fix round 1 của Task 7):
- Thêm hàm `deleteByCodePrefix(resourceUrl, prefix)` (khuôn copy `deleteByCodePrefix` /
  `cleanupLeftoverE2eData`), dùng chung cho cả 2 tài nguyên (`meeting/rooms`,
  `meeting/room-amenities`).
- `beforeAll`: quét xóa rác `E2EUI_` (rooms trước, amenities sau — đúng thứ tự tránh vướng FK qua
  pivot) còn sót từ lần chạy trước bị kill giữa chừng, TRƯỚC KHI tạo 2 tiện nghi setup của lần
  chạy này.
- `afterEach` (MỚI — trước đây chỉ dọn ở bước cuối của happy path): xóa phòng theo mã `CODE` của
  chính lần chạy này, rồi xóa 2 tiện nghi setup theo `amenityIds` đã lưu — chạy dù ca pass hay
  fail.
- Bước 3 "Xóa qua UI" ở cuối test **giữ nguyên** (vẫn cần verify hành vi Xóa thật qua UI);
  `afterEach` chỉ là lưới an toàn khi ca fail TRƯỚC bước đó.

**Chứng minh cleanup chạy cả khi FAIL**: chèn tạm dòng
`expect('remove-me-after-cleanup-check').toBe('TEMP_FORCE_FAIL')` ngay sau bước Lưu (trước khi đo
số chip/badge), chạy lại:

```
✘ 1 [chromium] › ... tạo kèm 2 tiện nghi - khóa - xóa (10.4s)
  Error: expect(received).toBe(expected)
  Expected: "TEMP_FORCE_FAIL"
  Received: "remove-me-after-cleanup-check"
  1 failed
```

Kiểm DB ngay sau ca fail này (phòng + 2 tiện nghi đã tạo xong trước điểm ép fail):

```
GET meeting/rooms?keyword=E2EUI_       -> 0 rows
GET meeting/room-amenities?keyword=E2EUI_ -> 0 rows
```

Cả phòng lẫn 2 tiện nghi đều đã bị `afterEach` dọn sạch dù test fail giữa chừng. Đã **gỡ dòng
assertion tạm**, verify lại `grep -n "TEMP_FORCE_FAIL" e2e/tests/meeting/_room-ui.smoke.spec.ts`
ra rỗng, và chạy lại xác nhận xanh (xem dòng tổng kết ở mục cuối).

### Việc BE — `company_name`/`manager_name` (reviewer quyết làm luôn)

Worktree BE `hrm-worktrees/phong-hop-api`:

1. **`Modules/Meeting/Entities/MeetingRoom.php`** — thêm 2 quan hệ:
   - `company()`: `belongsTo(Modules\Human\Entities\Company::class, 'company_id', 'id')` — cùng
     nguồn `Company` đang dùng ở `MeetingRoomService::formOptions()`.
   - `manager()`: `belongsTo(Modules\Timesheet\Entities\Employee::class, 'manager_employee_id',
     'id')` — **cố tình KHÔNG lọc theo trạng thái đang làm việc** (đây là quan hệ Eloquent đọc
     thẳng theo khoá ngoại đã lưu), khác hẳn `Employee::getAll(true)` mà FE dùng cho
     `$store.state.employees` — đúng là điểm khác biệt vá lỗi.
2. **`MeetingRoomResource`** (list) và **`DetailMeetingRoomResource`** (chi tiết/response
   tạo-sửa) — cả 2 đều thêm `company_name` = `optional($this->company)->name` và `manager_name` =
   `optional($this->manager)->fullname`. Brief chỉ nêu `MeetingRoomResource`; tôi chủ động thêm
   luôn vào `DetailMeetingRoomResource` để nhất quán 2 Resource của cùng 1 entity (tránh trường hợp
   modal Xem/Sửa thiếu trường mà danh sách lại có) — nêu rõ đây là mở rộng phạm vi nhỏ, có lý do,
   không phải làm lố.
3. **Eager load** — thêm `'company', 'manager.info'` vào:
   - `MeetingRoomService::index()` (đã có sẵn `with([...])`).
   - `MeetingRoomController::show()` (đã có sẵn `load([...])`).
   - `MeetingRoomService::updateOrCreate()` (đã có sẵn `$room->load('amenities')` — thêm 2 quan hệ
     mới để response POST/PUT có tên ngay, không lazy-load).
4. **FE** (`pages/meeting/rooms/index.vue`): bỏ hẳn 2 method `companyName(item)`/`managerName(item)`
   tự tra `$store.state.companies`/`$store.state.employees`, bỏ import `employeeFullName` (không
   còn dùng). 2 cột đọc thẳng `item.company_name` / `item.manager_name || '—'`.
5. **E2E API** — thêm ca 7 vào `tests/meeting/meeting-room.api.spec.ts`: tạo phòng có
   `company_id` + `manager_employee_id`, khẳng định `company_name`/`manager_name` đúng ở **CẢ 3**
   nguồn đọc (response POST, GET chi tiết, GET danh sách) — không chỉ riêng response tạo mới.

**Bằng chứng đã fix đúng bug** (không phải sửa lý thuyết): tìm 1 nhân viên đã nghỉ việc thật trong
DB (`employee_infos.status != 1`, id=26 "Bùi Văn Long"), tạo phòng với
`manager_employee_id: 26` qua API:

```json
{"manager_employee_id": 26, "manager_name": "Bùi Văn Long", ...}
```

`manager_name` trả đúng dù nhân viên này chắc chắn KHÔNG có trong `$store.state.employees`
(`Employee::getAll(true)` chỉ lấy `employee_infos.status = 1`) — xác nhận bug đã được vá, không
còn phụ thuộc trạng thái làm việc của người quản lý.

**Đo số query trước/sau (chống N+1)** — dùng `DB::enableQueryLog()` qua `tinker`, 2 phòng khác
công ty + khác người quản lý (`company_id` 1 và 2, `manager_employee_id` 34 và 25):

| Kịch bản | Tổng query | Query đụng `companies` | Query đụng `employees` |
|---|---|---|---|
| **CÓ** eager load `company`, `manager.info` (code hiện tại) | 17 | 1 (`WHERE id IN (1,2)`) | 1 (`WHERE id IN (25,34)`) + 1 `employee_infos IN (...)` |
| **KHÔNG** eager load (mô phỏng quên thêm `with()`) | 20 | 6 | 4 |

Không eager-load thì mỗi phòng tự lazy-load `company`/`manager` RIÊNG (không gộp được thành 1
query `WHERE IN`) → 6 query đụng `companies` + 4 query đụng `employees` cho chỉ 2 dòng, so với 1 +
1 khi có eager load. Có eager load, `company`/`manager.info` luôn gộp thành đúng 1 query mỗi bảng
bất kể số dòng trả về (tuyến tính O(1) thay vì O(n)) — chênh lệch càng lớn khi danh sách càng dài.

⚠️ Ghi chú ngoài phạm vi: cả 2 kịch bản đo được đều có thêm ~10 query "nhiễu" (`master_settings`,
`employee_infos`, `companies` lặp) không liên quan tới thay đổi lần này — xác nhận đây là chi phí
CÓ SẴN của accessor `employee_create_name`/`employee_update_name` (từ Task 6/`BaseModel`), tồn tại
CẢ TRƯỚC VÀ SAU khi tôi sửa. Không thuộc phạm vi Task 8, không tự ý sửa; nêu ra để BE cân nhắc ở
lần tối ưu khác.

Dữ liệu test tạo tay để đo query (id 61, 62, phòng quản lý nghỉ việc id 63) đã xóa qua API ngay
sau khi đo xong.

### MINOR 3 — Guard chống gọi trùng `loadFormOptions()`

`pages/meeting/rooms/components/MeetingRoomModal.vue`: thêm `loadingFormOptions: false` ở
`data()`, `if (this.loadingFormOptions) return` ở đầu `loadFormOptions()`, set `true`/`false` bọc
quanh khối `try/finally`. Không đụng `V2BaseModal.vue`.

### MINOR 4 — Đổi `V2BaseSelectInModal` → `V2BaseSelect` cho ô lọc "Tiện nghi"

`pages/meeting/rooms/index.vue`: ô lọc "Tiện nghi" (nằm NGOÀI modal, trong
`V2BaseSmartFilterPanel`) đổi từ `V2BaseSelectInModal` sang `V2BaseSelect` (đã hỗ trợ sẵn
`extraSettings.multiple`) — đúng quy ước "select trong modal/popup mới dùng `V2BaseSelectInModal`,
ngoài modal dùng `V2BaseSelect`". Đổi cả import + khai báo component. `MeetingRoomModal.vue` (2 ô
Tiện nghi + Công ty NẰM TRONG modal) giữ nguyên `V2BaseSelectInModal` — đúng quy ước, không đổi.

### Kiểm lại 2 lệnh tự kiểm (RỖNG cả 2)

```
$ grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/rooms/ | grep -v V2Base
(không có output)

$ grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/rooms/
(không có output)
```

### Playwright — dòng tổng kết sau fix

**UI smoke** (chromium, đúng lệnh brief đưa, không `--retries=0` — cấu hình mặc định có bật
retry):

```
$ PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
  npx playwright test tests/meeting/_room-ui.smoke.spec.ts --project=chromium --no-deps --workers=1

Running 1 test using 1 worker
  ✓  1 [chromium] › tests/meeting/_room-ui.smoke.spec.ts:179:5 › CRUD phòng họp qua UI: tạo kèm 2 tiện nghi - khóa - xóa (21.5s)
  1 passed (23.8s)
```

Chạy thêm 2 lần liên tiếp với `--retries=0` (loại bỏ hoàn toàn khả năng "xanh nhờ retry") ngay
trước lần trên: cả 2 lần đều `1 passed` (18.7s và 14.3s).

**API — cả thư mục `tests/meeting --project=api`** (không chỉ riêng spec vừa sửa, để chắc không phá
spec BE của Task 5/6):

```
$ PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" API_BASE=http://127.0.0.1:8001 \
  npx playwright test tests/meeting --project=api --no-deps --workers=1

Running 11 tests using 1 worker
  ✓   1 [api] › tests/meeting/meeting-room.api.spec.ts:124:5 › 1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho (1.2s)
  ✓   2 [api] › tests/meeting/meeting-room.api.spec.ts:153:5 › 2. tạo phòng là có sẵn checkin_qr_token (622ms)
  ✓   3 [api] › tests/meeting/meeting-room.api.spec.ts:169:5 › 3. gắn nhiều tiện nghi rồi đọc lại đúng danh sách (1.9s)
  ✓   4 [api] › tests/meeting/meeting-room.api.spec.ts:199:5 › 4. form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty (494ms)
  ✓   5 [api] › tests/meeting/meeting-room.api.spec.ts:212:5 › 5. không quyền quản lý danh mục thì POST trả 403 (280ms)
  ✓   6 [api] › tests/meeting/meeting-room.api.spec.ts:219:5 › 6. không quyền thì GET chi tiết phòng cũng trả 403, không lộ checkin_qr_token (581ms)
  ✓   7 [api] › tests/meeting/meeting-room.api.spec.ts:233:5 › 7. tạo phòng có company_id + manager_employee_id -> company_name/manager_name đúng ở cả 3 nguồn đọc (917ms)
  ✓   8 [api] › tests/meeting/room-amenity.api.spec.ts:92:5 › 1. tạo - sửa - khóa - mở khóa tiện nghi (2.1s)
  ✓   9 [api] › tests/meeting/room-amenity.api.spec.ts:133:5 › 2. trùng mã thì trả 422 kèm field code (398ms)
  ✓  10 [api] › tests/meeting/room-amenity.api.spec.ts:148:5 › 3. không quyền thì 403 (439ms)
  ✓  11 [api] › tests/meeting/room-amenity.api.spec.ts:155:5 › 4. tiện nghi CHƯA gắn phòng nào thì xóa được (1.3s)

  11 passed (14.8s)
```

Ca 1-6 (Task 6, có sẵn từ trước) và 4 ca của `room-amenity.api.spec.ts` (Task 5) đều xanh —
xác nhận thay đổi Entity/Resource/Service của Task 8 fix round 1 không phá spec BE cũ. Ca 7 (mới)
cũng xanh.

### Kiểm DB sạch rác `E2EUI_%` / `E2E_%` sau khi chạy hết mọi lệnh trên

```
GET meeting/rooms?keyword=E2E             -> 0 dòng có code bắt đầu E2E
GET meeting/room-amenities?keyword=E2E    -> 0 dòng có code bắt đầu E2E
```

### File đụng tới trong fix round 1

**FE** (`hrm-worktrees/phong-hop-client`):
- `pages/meeting/rooms/index.vue` — mixin `CheckPermission`, bỏ `canView`, `canManage` thành
  computed; bỏ `companyName()`/`managerName()`, đọc thẳng `item.company_name`/`item.manager_name`;
  đổi `V2BaseSelectInModal` → `V2BaseSelect` cho ô lọc Tiện nghi.
- `pages/meeting/rooms/components/MeetingRoomModal.vue` — thêm guard `loadingFormOptions`.

**BE** (`hrm-worktrees/phong-hop-api`):
- `Modules/Meeting/Entities/MeetingRoom.php` — thêm quan hệ `company()`, `manager()`.
- `Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php` — thêm `company_name`,
  `manager_name`.
- `Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php` — thêm `company_name`,
  `manager_name` (mở rộng nhỏ ngoài yêu cầu gốc, có lý do — xem mục "Việc BE" ở trên).
- `Modules/Meeting/Services/MeetingRoomService.php` — eager load `company`, `manager.info` trong
  `index()` và `updateOrCreate()`.
- `Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php` — eager load `company`,
  `manager.info` trong `show()`.

**E2E** (`e2e/`):
- `tests/meeting/_room-ui.smoke.spec.ts` — thêm `deleteByCodePrefix()`, `beforeAll` dọn rác cũ,
  `afterEach` dọn dữ liệu của lần chạy này (không phụ thuộc happy path).
- `tests/meeting/meeting-room.api.spec.ts` — thêm ca 7 (company_name/manager_name).

Không đụng `components/modal/V2BaseModal.vue` (giữ nguyên `hide()` alias từ Task 7).
