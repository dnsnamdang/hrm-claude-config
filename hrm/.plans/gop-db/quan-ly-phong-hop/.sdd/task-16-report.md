# Task 16 report — FE màn danh sách phiếu đặt phòng `/meeting/bookings`

**Status: DONE (đã fix round 1)**

## Fix round 1/5 — ca F1 cũ bị sai giả định sau khi điền link menu

**Nguyên nhân:** ca `F1` (`tests/meeting/meeting-room.spec.ts`, viết ở Task 10/Phase 1) khẳng định
"Đăng ký phòng họp KHÔNG có href" — đúng lúc đó vì Phase 2 chưa làm. Task 16 điền
`link: '/meeting/bookings'` cho đúng mục đó (theo yêu cầu brief) nên giả định cũ hết hiệu lực.
Vì bộ test `meeting-room.spec.ts` chạy `serial`, ca F1 đỏ kéo theo ca F2 in "did not run".

**Đã sửa:** `e2e/tests/meeting/meeting-room.spec.ts`, ca `F1`:
- Đổi tên ca cho khớp assert mới: *"cả 2 mục đều có href, bấm 'Đăng ký phòng họp' điều hướng đúng +
  render bảng phiếu thật"*.
- `Danh sách phòng họp` vẫn assert `href="/meeting/rooms"` (không đổi).
- `Đăng ký phòng họp` nay assert **CÓ** `href="/meeting/bookings"` (trước đây assert `null`).
- Thêm bước bấm vào dòng, `waitForURL('**/meeting/bookings')`, rồi **đo DOM thật**: bảng
  `table.data-table` render đủ 10 cột đúng thứ tự (không chỉ đo URL — đúng tinh thần "vào được
  trang không chứng minh gate còn sống").

**Đã rà toàn bộ `tests/meeting/`** tìm giả định "Đăng ký phòng họp chưa có link" hoặc số mục
menu cũ khác: `grep -rn "Đăng ký phòng họp" tests/meeting/*.ts` chỉ còn đúng 1 chỗ (ca F1 vừa sửa);
không còn assertion nào khác đếm số dòng `.rows .row` trong nhóm "Quản lý phòng họp" hay giả định
liên quan. File mới `_booking-form-ui.smoke.spec.ts` (Task 17 thêm trong lúc tôi đang chạy) tự
tạo/dọn dữ liệu riêng, không đụng tới phần menu này.

**Chạy lại `tests/meeting --project=chromium --no-deps --workers=1` (đúng phạm vi coordinator yêu
cầu — project `chromium` của repo này CHỦ ĐỊNH bỏ qua `*.api.spec.ts`, xem `testIgnore` trong
`playwright.config.ts`; các spec `.api.spec.ts` (meeting-room-booking, meeting-room, room-amenity)
chạy ở project `api` riêng, ngoài phạm vi lệnh coordinator chỉ định), chạy FOREGROUND, dòng tổng
kết:**
```
21 passed (3.6m)
```
Không `failed`, không `did not run`, không `flaky`. Gồm cả 2 smoke spec của tôi (Task 16, 5 ca) +
smoke spec Task 17 (2 ca) + `_auth-smoke` (1 ca) + `meeting-room.spec.ts` (13 ca, có F1 vừa sửa).

DB sau khi chạy: `meeting_rooms=0`, `meeting_room_bookings=0`, `meeting_room_amenities=0`, không còn
dòng cấp quyền tạm `role_has_permissions (1575, role 20)` — sạch rác.

File đụng tới ở fix round này: **chỉ** `e2e/tests/meeting/meeting-room.spec.ts` (ca F1). Không sửa
gì thêm ở `pages/meeting/bookings/` (không cần thiết cho fix này).

---

## File tạo/sửa (trong worktree FE `hrm-worktrees/phong-hop-client`)

- Tạo `pages/meeting/bookings/index.vue` — màn danh sách (bộ lọc + bảng + hành động).
- Tạo `pages/meeting/bookings/components/BookingDetailModal.vue` — popup Xem chi tiết (chỉ đọc),
  dùng chung cho nút Xem/Sửa, footer có Duyệt/Từ chối/Hủy đọc theo cờ BE. *Form Sửa đầy đủ trường
  (chọn phòng theo sức chứa/tiện nghi, dải giờ bận...) là phạm vi Task 17 "FE modal đặt phòng",
  CHƯA xây ở Task này — đã ghi rõ trong comment đầu file.*
- Sửa `components/subsystem-menu/meeting.js` — điền `link: '/meeting/bookings'` cho mục "Đăng ký
  phòng họp", `isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp']`.
- Tạo `e2e/tests/meeting/_bookings-ui.smoke.spec.ts` (thư mục e2e dùng chung, không thuộc worktree).

## 2 lệnh grep tự kiểm (cả 2 RỖNG)

```
grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/bookings/ | grep -v V2Base
# (rỗng)

grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/bookings/
# (rỗng)
```

## git diff --numstat của file menu

```
8       2       components/subsystem-menu/meeting.js
```
Chỉ thêm/sửa đúng khối "Đăng ký phòng họp" (điền link + isShow), không đụng dòng nào khác.

## Dòng tổng kết Playwright (chạy 2 lần, cả 2 XANH)

Lệnh chạy:
```
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/_bookings-ui.smoke.spec.ts --project=chromium --no-deps --workers=1
```
Lần 1 (bắt lỗi thật — không phải giả): `A2` fail vì kỳ vọng cột Số người = `'0'`, thực tế API trả
`attendee_count = null` khi tạo phiếu không gửi field này → FE hiện đúng `'—'` (không phải bug FE,
sửa lại kỳ vọng trong spec). 4 ca sau in "did not run" (đúng cảnh báo mode `serial`), **không phải
"passed"** — đã đọc đúng dòng tổng kết, không tưởng nhầm.

Lần 2 (sau khi sửa spec) — dòng tổng kết:
```
5 passed (1.0m)
```
Kiểm DB sạch rác sau cả 2 lần chạy (kể cả lần fail): `meeting_rooms=0`, `meeting_room_bookings=0`,
`role_has_permissions` không còn dòng cấp quyền tạm (1575/role 20).

## Số đo DOM thật (từ ca A2/A3/B1/C1)

- Header bảng: đúng 10 cột, đúng thứ tự
  `['Mã','Tiêu đề','Phòng','Thời gian','Người đặt','Chủ trì','Số người','Nguồn','Trạng thái','Hành động']`.
- Lọc theo phòng vừa tạo (mã `E2E_BKUI_<suffix>`, `require_approval=1`) → bảng còn đúng **2 dòng**.
- Phiếu A (giữ "Chờ duyệt", status=1): badge `.v2-badge` text = **"Chờ duyệt"**; số nút hành động
  `.v2-icon-btn` trong dòng = **5** (Xem, Sửa, Duyệt, Từ chối, Hủy — đủ 5 title tương ứng).
- Phiếu B (gọi API `/approve` → status=2): badge text = **"Đã duyệt"**; số nút hành động = **3**
  (Xem, Sửa, Hủy) — nút Duyệt/Từ chối **đếm = 0** (chứng minh cờ BE `is_can_approve`/`is_can_reject`
  được tôn trọng, không hiện cứng).
- Cột Số người ô Phiếu A = `'—'` (attendee_count null), cột Nguồn = `'Tự đặt'`.
- Modal Xem chi tiết (`#modal-booking-detail`): hiện đúng tiêu đề phiếu + badge "Chờ duyệt"; footer
  có đủ 3 nút Duyệt/Từ chối/Hủy phiếu (đếm bằng `getByRole('button', {name})` = 1 mỗi nút).
- Công tắc "Chỉ phiếu của tôi" (`getByRole('checkbox', {name:'Chỉ phiếu của tôi'})`):
  - Admin `user-wt` (employee 34, có quyền 1579 qua role 18) → **KHÔNG check** (mặc định TẮT).
  - `user-nocost-wt` (employee 25, role 20, cấp TẠM quyền 1575 qua DB để qua gate, vẫn KHÔNG có
    1579) → **CÓ check** (mặc định BẬT).

## Quyết định kỹ thuật đáng chú ý (đọc code thật, không đoán theo brief)

1. **Field `room` không tồn tại** trong `MeetingRoomBookingResource`/`DetailMeetingRoomBookingResource`
   — tên phòng nằm ở field **`room_name`**. Đã dùng đúng `room_name` (brief ghi "room" là rút gọn).
2. **Field chủ trì** là `host_employee_name` (không phải `host_name` như brief tóm tắt).
3. Endpoint sửa phiếu là **`PUT meeting/room-bookings/{id}`** (không phải POST như brief tóm tắt);
   không dùng tới trong Task này vì chưa có form sửa thật.
4. `meeting/rooms` (nguồn cho ô lọc "Phòng họp") yêu cầu quyền danh mục phòng riêng (khác quyền
   xem phiếu) — bọc try/catch im lặng như `loadAmenityOptions()` của `rooms/index.vue`: người
   không có quyền đó vẫn dùng được màn bình thường, chỉ là ô lọc theo phòng không có option.
5. Trạng thái/Nguồn: **status_text/status_color đọc thẳng từ BE** (không map ở FE); riêng **Nguồn**
   (`source` 1/2 → "Tự đặt"/"Từ meeting") là FE tự map vì BE không trả field `source_text` — đây
   KHÔNG phải trường trạng thái nên không vi phạm quy tắc "BE trả thì không tự map".

## Concerns cho coordinator

1. **Gate route dùng quyền phòng, không dùng quyền phiếu** — đúng theo yêu cầu brief
   (`isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp']`), nhưng đã tự kiểm bằng SQL
   trên DB dev: **2 role duy nhất có quyền phòng họp (18, 100125) đều ĐÃ có sẵn quyền 1579/1580**,
   không có role nào tách riêng "có quyền phòng nhưng thiếu quyền xem phiếu". Nghĩa là với cấu hình
   quyền hiện tại, một nhân viên bình thường (không có quyền danh mục phòng) sẽ bị chặn hẳn khỏi
   `/meeting/bookings` — kể cả khi họ chỉ cần xem/hủy phiếu CỦA CHÍNH MÌNH (BE `store`/`cancel` cố
   tình KHÔNG gắn quyền theo quyết định #8 "mọi nhân viên đặt phòng được"). Đã làm đúng lời dặn của
   brief, nhưng đây có thể là gap sản phẩm cần plan xác nhận lại (có nên tách 1 quyền
   "Xem/đặt phòng họp" phổ biến hơn cho `isShow` không, để khớp quyết định #8).
2. **Nút "Sửa" hiện chỉ mở modal Xem chi tiết (chỉ đọc)** — Task 17 ("FE modal đặt phòng") mới xây
   form sửa thật (chọn phòng theo sức chứa/tiện nghi, dải giờ bận...). Đã ghi chú rõ trong code
   (`BookingDetailModal.vue` đầu file) để Task 17 biết thay thân modal, giữ nguyên props/API gọi ra
   (`viewItem`/`editItem` ở `index.vue` đã trỏ đúng chỗ, không cần sửa lại chữ ký khi Task 17 vào).
3. Chưa test hành động Từ chối/Hủy (nhập lý do bắt buộc rồi gọi API) bằng Playwright thật trong Task
   này — đã đọc code `base-confirm-modal`/`$confirm` xác nhận `requiredInput` chặn đóng popup khi
   rỗng, nhưng theo đúng tinh thần "test xanh/đọc code không tính là đã kiểm", nên khuyến nghị Task
   18 (bộ e2e Phase 2 chính thức) bổ sung ca bấm nút Từ chối/Hủy thật trên trình duyệt.
