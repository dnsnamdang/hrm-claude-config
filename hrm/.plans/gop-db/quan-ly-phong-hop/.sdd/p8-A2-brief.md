# Brief — Phase 8 / lượt A2 (task T114–T117): nối phần còn lại của BE sang "nhiều người phụ trách"

Đây là yêu cầu của bạn. Dùng **đúng** tên hàm / tên trường viết trong file này.

## Bối cảnh

Repo `hrm-api` (Laravel 8, PHP 7.4), nhánh `gop_db`, module `Modules/Meeting`.
Lượt trước (A1) đã đổi `meeting_rooms.manager_employee_id` (1 người) thành bảng nối
`meeting_room_managers` (nhiều người): cột cũ **đã bị drop**, entity `MeetingRoom` nay có
`managers()`, `managerIds(): array`, `managerNames(): array`.
**Đọc `.sdd/p8-A1-report.md` mục "Bàn giao" trước khi code** để dùng đúng chữ ký thật.

Lượt này sửa 4 chỗ còn lại vẫn đang đọc cột đã drop. Đây là phần **rủi ro nhất** của cả Phase 8:
sai là phiếu đặt phòng biến mất khỏi màn của người quản lý, hoặc người không phụ trách lại duyệt
được phiếu — cả hai đều **không có lỗi nào báo ra**.

## Việc phải làm

### T114 — `Modules/Meeting/Services/MeetingRoomBookingService.php` (4 chỗ)

Tìm bằng `grep -n "manager_employee_id" Modules/Meeting/Services/MeetingRoomBookingService.php`.

1. **`applyVisibilityScope()`** (~dòng 179): `$r->where('manager_employee_id', $employeeId)` →
   `$r->whereHas('managers', function ($q) use ($employeeId) { $q->where('employee_id', $employeeId); })`.
   Giữ nguyên toàn bộ các vế `orWhere` khác của phạm vi — **đừng gộp/đơn giản hoá** chúng: đây là
   luật "phiếu của mình HOẶC phiếu của phòng mình quản lý", bỏ sót vế nào là mất phiếu im lặng.
2. **Gate ~dòng 200**: `if ($room && $room->manager_employee_id && (int) $room->manager_employee_id === $employeeId)`
   → kiểm `in_array($employeeId, $room->managerIds(), true)`.
3. **Gate duyệt ~dòng 777** (`$isRoomManager`): đổi tương tự, dùng `(int) auth()->id()`.
4. **Người nhận thông báo ~dòng 1193-1198**: hiện `if (!$room->manager_employee_id) return;` rồi gửi
   cho mảng `[$room->manager_employee_id]` → gửi cho **toàn bộ** `$room->managerIds()`; mảng rỗng thì
   return sớm (không gửi). Giữ nguyên tham số người gửi (`$sender`) đang truyền — có một cái bẫy đã
   ghi trong comment ngay trên đó, đọc trước khi sửa.

### T115 — 2 Resource phiếu

`Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php` (~dòng 24) và
`DetailMeetingRoomBookingResource.php` (~dòng 18): biến `$isRoomManager` tính bằng
`in_array((int) auth()->id(), optional($this->room)->managerIds() ?: [], true)`.
Phòng chưa load thì phải ra `false`, **không được** ra `true`. Mọi cờ `is_can_*` ở 2 file này giữ
nguyên ý nghĩa cũ, chỉ đổi cách xác định "tôi có phải người quản lý phòng không".

### T116 — Import / Export phòng họp

- `Services/MeetingRoomService.php` ~dòng 1054 (chỗ map `ManagerName` → `manager_employee_id`):
  nhận **nhiều tên ngăn bằng dấu `;`**, trim từng tên, bỏ phần tử rỗng.
- Tên không khớp nhân viên nào → **báo lỗi đúng dòng đó** theo đúng cơ chế báo lỗi import hiện có của
  file này (đọc cách các cột khác đang báo lỗi rồi làm theo, đừng tự chế kiểu mới).
- **Dòng import không có tên phụ trách nào → cũng là lỗi dòng** (phòng bắt buộc có ≥ 1 người phụ
  trách, đã chốt ở lượt A1).
- Export: ghép ngược danh sách tên bằng `"; "`.
- `Http/Controllers/Concerns/BuildsImportTemplate.php` + file mẫu import: cập nhật mô tả cột
  `ManagerName` cho biết được phép nhiều tên ngăn bằng `;`.

### T117 — `app/Services/CatalogHistoryService.php` (~dòng 441-450)

Chỗ này đang đổi giá trị thô sang chữ để ghi lịch sử danh mục, có nhắc
`manager_employee_id` => 'Người quản lý phòng'. Đổi sang khoá mới (`manager_employee_ids` hoặc tên
trường thực tế mà `MeetingRoomService::catalogDisplay()` đưa sang — **đọc hàm đó trước**), hiển thị
**danh sách TÊN** ngăn bằng `, `. Nhãn giữ nguyên "Người quản lý phòng".
Lịch sử **không được** in ra id trần.

## Ràng buộc bắt buộc

- **Không `git commit` / `push` / `stash`.** Không đụng `hrm-client`.
- Không sửa file ngoài 4 nhóm trên. Không tạo subagent. Không tự gọi reviewer.
- Cấm N+1: chỗ nào lặp qua nhiều phiếu/phòng thì eager load `room.managers`.
- Không tự viết lại message validate cho rule phổ biến.

## Cách tự kiểm (bắt buộc, ghi SỐ THẬT vào báo cáo)

1. `grep -rn "manager_employee_id" Modules app` — chỉ còn được phép xuất hiện trong **migration**
   (file tạo bảng cũ + file `2026_09_23_000001_*`). Bất kỳ chỗ nào khác là còn sót.
2. PHPUnit: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingRoom` — chạy
   TRƯỚC khi sửa để lấy mốc, chạy lại SAU khi sửa; báo cáo cả 2 con số. Không được để đỏ thêm ca nào.
3. Viết **test mới** `Modules/Meeting/Tests/Feature/MeetingRoomManagersTest.php` (hoặc thư mục test
   thật của module — kiểm cấu trúc hiện có trước) chứng minh 4 điều, mỗi điều 1 ca:
   - phòng có 2 người phụ trách → **cả 2** đều duyệt được phiếu;
   - người **ngoài** nhóm gọi duyệt → bị chặn (403 hoặc exception đúng như luồng hiện tại);
   - `applyVisibilityScope()` trả phiếu của phòng mình phụ trách cho **cả 2** người;
   - thông báo khi tạo phiếu bắn cho **đủ 2** người (assert số người nhận, không assert nội dung).
   Chạy và dán kết quả thật vào báo cáo. Ca nào chưa đỏ được trước khi sửa thì nói rõ vì sao.
4. Kiểm tay 1 lượt trên DB local (2 phòng, 3 phiếu): thêm người phụ trách thứ 2 cho 1 phòng bằng SQL,
   xác nhận `applyVisibilityScope` trả đúng phiếu cho người đó (chạy qua tinker cũng được), rồi **xoá
   dữ liệu test đã thêm**.

## Báo cáo

Ghi đầy đủ vào `.plans/gop-db/quan-ly-phong-hop/.sdd/p8-A2-report.md`: từng task đã làm, số đo thật
của 4 mục tự kiểm, danh sách file sửa, chỗ nào bạn thấy luật cũ mơ hồ và bạn đã chọn hiểu thế nào.
Trả về chat ngắn gọn: trạng thái, file đã sửa, 1 dòng kết quả test, điểm nghi ngờ.

---

## BỔ SUNG SAU KHI LƯỢT A1 XONG (đọc kỹ — 3 việc phát sinh, đều BẮT BUỘC làm trong lượt này)

A1 đã drop cột `manager_employee_id` và xoá quan hệ `manager()`. Hệ quả: **một số chỗ đang gãy thật**,
không chỉ là "cần đổi cho đẹp".

### BS-1 — 7 chỗ eager load `room.manager.info` trong `MeetingRoomBookingService.php`

`grep -n "room.manager" Modules/Meeting/Services/MeetingRoomBookingService.php` — mỗi chỗ
`->with('room.manager.info')` nay ném `RelationNotFoundException` (lỗi **500**). Đổi hết sang
`->with('room.managers.info')` (kèm `info` để không N+1 khi lấy tên). Sửa **đủ cả 7**, thiếu 1 chỗ là
một endpoint chết mà các endpoint khác vẫn chạy — rất dễ tưởng đã xong.

### BS-2 — `BookableMeetingRoomResource.php`: `manager_name` đang ra `null`

Resource này (dùng cho danh sách phòng chọn được ở popup đặt phòng) vẫn dựng `manager_name` từ quan
hệ cũ nên nay luôn `null` → panel phải của popup đặt phòng mất dòng "Người phụ trách".
Đổi sang lấy từ `managers` và trả **`manager_name_text`** (chuỗi ghép `", "`, rỗng thì `''`) —
**đúng tên trường mà 2 Resource phòng ở lượt A1 đã trả**, để FE chỉ phải học một tên.
Giữ nguyên chủ ý của file: **không trả id thô** của người phụ trách.
Ghi vào báo cáo: FE `BookingFormModal.vue` còn đọc `selectedRoomInfo.manager_name` (2 chỗ, ~dòng 464
và ~1925) — **đó là việc của lượt FE sau**, bạn chỉ ghi lại, không sửa `hrm-client`.

### BS-3 — Import phòng họp đang ÂM THẦM bỏ qua người phụ trách

Ở `MeetingRoomService` (~dòng 1066) mảng tạo phòng vẫn gán `manager_employee_id` — cột không còn tồn
tại nên Laravel **bỏ qua không báo lỗi**, kết quả là import xong phòng không có ai phụ trách.
Sửa theo T116, và **thêm 1 ca test import** chứng minh: file 1 dòng có 2 tên ngăn bằng `;` → tạo ra
đúng 2 dòng `meeting_room_managers`.

### Thứ tự ưu tiên nếu bạn phải cắt bớt việc

BS-1 → T114 → T115 → BS-2 → BS-3/T116 → T117. Không được dừng giữa chừng ở trạng thái còn chỗ nào
đọc quan hệ `manager()` cũ.

### Ghi chú sửa lỗi mô tả trong brief gốc

Mục T111 của lượt A1 nói "sort cột người quản lý ở dòng 716" — **sai**: đoạn đó là
`catalogDisplay()` phục vụ ghi lịch sử, không phải sort. Whitelist sort chưa từng có cột người quản
lý và FE cũng chưa khai `sortable` cho cột đó. **Đừng tự thêm tính năng sort mới** trong lượt này;
T117 bên dưới chính là phần `catalogDisplay()` đó.
