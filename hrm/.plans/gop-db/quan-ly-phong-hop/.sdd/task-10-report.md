# Task 10 — E2E UI chính thức + chạy lại toàn bộ — Báo cáo

**Status: HOÀN THÀNH** (đã qua Fix round 1)

## Fix round 1 (review Approved kèm 1 Important + 1 Minor)

- **IMPORTANT — mất coverage "cảnh báo chưa lưu"**: bổ sung ca `C1` mới vào nhóm C
  (`meeting-room.spec.ts`) — mở modal Thêm tiện nghi, gõ dở tên (form dirty), bấm nút đóng modal →
  assert popup "Thông tin chưa lưu" hiện đúng text (`Bạn có thông tin chưa lưu. Có chắc chắn muốn
  thoát?`) → chọn **"Ở lại"** → modal vẫn mở, ô tên giữ nguyên giá trị (`toHaveValue`) → đóng lại,
  chọn **"Thoát"** → modal đóng, bảng KHÔNG tăng dòng. Ca cũ (tạo/khóa/mở khóa/xóa) đổi tên thành `C2`.
  Copy nguyên văn logic đã kiểm chứng chạy ổn của `_room-amenity-ui.smoke.spec.ts` (bản đã xoá).
- **MINOR — bám sát câu chữ brief ở ca quyền**: nhóm D (D1, D2) — thêm 1 dòng assert tường minh
  `expect(page.getByRole('button', { name: 'Tạo mới' })).toHaveCount(0)` bên cạnh 2 assertion đã có
  (URL bị đá + bảng không render).
- **Cập nhật mục Concerns** (xem bên dưới) — liệt kê đầy đủ MỌI ca của 3 spec smoke đã xoá mà KHÔNG
  được port sang bộ chính thức, không chỉ riêng ca menu-rail như báo cáo lần trước.
- Chạy lại cả thư mục `tests/meeting`, 2 lần × 2 project (chromium/api) — xem mục "Dòng tổng kết" đã
  cập nhật bên dưới (số ca chromium tăng từ 11 → 12 do thêm ca C1).

## File

- Sửa: `e2e/tests/meeting/meeting-room.spec.ts` (5 nhóm `test.describe`, **12 ca UI** — tăng 1 ca so
  với bản trước fix round 1)
- Xoá (đã phủ bởi bộ chính thức, trừ phần nêu ở Concerns): `_room-ui.smoke.spec.ts`,
  `_room-amenity-ui.smoke.spec.ts`, `_menu.smoke.spec.ts`
- Giữ lại: `_auth-smoke.spec.ts` (hạ tầng đăng nhập worktree, không liên quan UI màn này)
- Không sửa: `meeting-room.api.spec.ts`, `room-amenity.api.spec.ts` (giữ nguyên 7 + 4 ca đã có)

## Spec giữ / xoá

| File | Trạng thái |
|---|---|
| `meeting-room.spec.ts` | **UI chính thức** — 12 ca (5 nhóm A-E) |
| `meeting-room.api.spec.ts` | giữ nguyên (7 ca, Task 6+8) |
| `room-amenity.api.spec.ts` | giữ nguyên (4 ca, Task 5) |
| `_auth-smoke.spec.ts` | giữ (hạ tầng đăng nhập) |
| `_room-ui.smoke.spec.ts` | **XOÁ** — phủ bởi nhóm A (không thiếu ca nào, xem Concerns #2) |
| `_room-amenity-ui.smoke.spec.ts` | **XOÁ** — phủ bởi nhóm C (đủ cả ca "chưa lưu" sau fix round 1) |
| `_menu.smoke.spec.ts` | **XOÁ** — phần nocost-gate thay bởi nhóm D; phần menu-rail **KHÔNG** port (xem Concerns #2) |

## Cấu trúc `meeting-room.spec.ts` (5 nhóm, đúng 8 nhóm ca tối thiểu của brief)

- **A. Admin — Danh mục phòng họp** (serial, 4 ca): A1 11 cột đúng thứ tự · A2 tạo qua modal + 2 tiện
  nghi, đo cột Công ty/Người quản lý ra TÊN thật (không rỗng, không `—`, không id số) · A3 khóa/mở
  khóa đổi badge · A4 xóa khi chưa có phiếu đặt, bảng giảm đúng 1 dòng
- **B. Khuôn giao diện** (Ruling R2, 1 ca): modal footer nằm trong viewport khi cuộn `.v2-modal-body`
  (đã đo DOM thật bằng Playwright MCP trước khi viết — phần tử scroll thật là `.v2-modal-body`, không
  phải `.modal-body` như code mẫu gốc trong brief, vì CSS đã tắt cuộn của `.modal-body`) + trang không
  tràn ngang
- **C. Danh mục tiện nghi phòng họp** (2 ca, **mới thêm C1 ở fix round 1**): C1 cảnh báo "chưa lưu"
  khi đóng modal (Ở lại giữ dữ liệu / Thoát không tạo bản ghi) · C2 tạo → khóa → mở khóa → xóa, đo
  DOM từng bước
- **D. Gate route trực tiếp** (ca bắt buộc #2 đầu brief, 2 ca): nocost vào thẳng URL `/meeting/rooms`
  và `/meeting/room-amenities` → bị đẩy `/pages/extras/404` VÀ bảng không render VÀ nút "Tạo mới"
  đếm 0 (**3 assertion sau fix round 1**, không chỉ URL)
- **E. Bảo mật `checkin_qr_token`** (ca bắt buộc #1 đầu brief, 2 ca): cấp tạm permission id 1575
  (`Xem danh mục phòng họp`) vào `role_has_permissions` cho **role_id=20** (`company_id=1`) của nhân
  viên 25, qua `mysql` CLI (đọc credential từ `.env` worktree tại runtime, không hardcode mật khẩu) →
  E1 kiểm UI (vào được trang, bảng render, nút "Tạo mới" ẨN vì chỉ có quyền Xem không có quyền Quản
  lý) → E2 kiểm API (`GET /meeting/rooms/{id}` trả 200 nhưng body KHÔNG chứa `checkin_qr_token`) →
  `afterAll` thu hồi đúng dòng vừa cấp + `SELECT COUNT(*)` xác nhận lại = 0.

Đặt ca bảo mật trong file UI (không phải `.api.spec.ts`) vì cần cả phép đo UI (ẩn nút "Tạo mới") lẫn
phép đo API trong cùng 1 cửa sổ cấp quyền tạm — gọn hơn tách 2 nơi.

### Cách xác định đúng role để cấp quyền (không đoán)
`employee_has_roles` của nhân viên 25 có 2 dòng: `role_id=100003` (`model_type=App\Employee`) và
`role_id=20` (`model_type=Modules\Timesheet\Entities\Employee`). Chỉ dòng thứ 2 khớp model auth thật
mà middleware `CheckPermission` dùng (`$employee->getAllPermissions()`, xem `task-4b-report.md` mục 1)
— xác nhận bằng thực nghiệm curl trực tiếp trước khi đưa vào spec: cấp permission 1575 cho
`role_id=20/company_id=1` → GET chi tiết trả 200 không có `checkin_qr_token`; xoá dòng đó → trả lại 403.

## Dòng tổng kết từng lần chạy (SAU fix round 1)

**Lần 1 — chromium (12 ca):**
```
Running 12 tests using 1 worker
  ✓ 1 _auth-smoke.spec.ts › token admin ... (5.9s)
  ✓ 2 meeting-room.spec.ts › A1 ... (4.5s)
  ✓ 3 meeting-room.spec.ts › A2 ... (9.9s)
  ✓ 4 meeting-room.spec.ts › A3 ... (14.3s)
  ✓ 5 meeting-room.spec.ts › A4 ... (9.7s)
  ✓ 6 meeting-room.spec.ts › B1 ... (4.2s)
  ✓ 7 meeting-room.spec.ts › C1 (mới) ... (8.6s)
  ✓ 8 meeting-room.spec.ts › C2 ... (19.5s)
  ✓ 9 meeting-room.spec.ts › D1 ... (3.8s)
  ✓ 10 meeting-room.spec.ts › D2 ... (4.6s)
  ✓ 11 meeting-room.spec.ts › E1 ... (5.7s)
  ✓ 12 meeting-room.spec.ts › E2 ... (1.2s)
  12 passed (1.9m)
```

**Lần 1 — api (11 ca, không đổi):**
```
Running 11 tests using 1 worker
  ✓ 1-7 meeting-room.api.spec.ts (ca 1-7)
  ✓ 8-11 room-amenity.api.spec.ts (ca 1-4)
  11 passed (13.5s)
```

**Lần 2 — chromium (kiểm ổn định):**
```
Running 12 tests using 1 worker
  ... toàn bộ 12 ca ✓ ...
  12 passed (1.7m)
```

**Lần 2 — api (kiểm ổn định):**
```
Running 11 tests using 1 worker
  ... toàn bộ 11 ca ✓ ...
  11 passed (14.0s)
```

→ Cả 4 lệnh đều đọc đúng dòng tổng kết "N passed", **không có ca nào "did not run"**, không flaky qua
2 lần chạy (kể cả ca `C1` mới thêm).

Lệnh dùng (đúng theo brief, `--no-deps` vì `api-setup` hỏng sẵn trên DB gộp):
```bash
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting --project=chromium --no-deps --workers=1
npx playwright test tests/meeting --project=api --no-deps --workers=1
```

## Kiểm DB sạch rác + thu hồi quyền (sau lần chạy cuối)

```sql
SELECT id,code,name FROM meeting_rooms WHERE code LIKE 'E2E%';          -- rỗng
SELECT id,code,name FROM meeting_room_amenities WHERE code LIKE 'E2E%'; -- rỗng
SELECT * FROM role_has_permissions WHERE permission_id=1575 AND role_id=20 AND company_id=1; -- rỗng
SELECT COUNT(*) FROM permissions WHERE guard_name='api';                -- 745 (không đổi so với baseline Task 4)
```
Cả 3 truy vấn đầu đều rỗng; tổng số quyền `guard_name='api'` vẫn 745 — không có dữ liệu rác, không có
quyền tạm còn sót.

## Concerns

1. Code mẫu `(a)` trong Ruling R2 của brief dùng `.modal.show .modal-body`.scrollTop — đã đo DOM thật
   (Playwright MCP) và xác nhận phần tử đó KHÔNG scroll (CSS `V2BaseModal.vue` đã tắt cuộn của
   `.modal-body`, chỉ `.v2-modal-body` mới thật sự cuộn). Spec đã sửa selector cuộn thành
   `.modal.show .v2-modal-body` để phép đo có ý nghĩa thật (nếu giữ nguyên như brief, `el.scrollTop`
   sẽ là no-op và ca test luôn xanh giả). Footer selector `.modal.show .modal-footer` giữ nguyên vì
   khớp DOM thật.

2. **Danh sách đầy đủ mọi ca của 3 spec smoke đã xoá KHÔNG được port sang bộ chính thức** (yêu cầu bổ
   sung của fix round 1 — trước đây chỉ nêu riêng ca menu-rail):
   - `_room-ui.smoke.spec.ts` → **không mất ca nào**. Toàn bộ luồng (baseline rỗng → tạo qua modal
     gắn 2 tiện nghi → đo chip/badge → khóa (có kiểm message) → xóa) đã port đủ vào nhóm A (A1-A4).
   - `_room-amenity-ui.smoke.spec.ts` → **trước fix round 1 thiếu 1 ca** (cảnh báo "chưa lưu" khi đóng
     modal dở dang) — **đã bổ sung ở fix round 1 thành ca `C1`**. Phần còn lại (tạo/khóa/mở khóa/xóa)
     đã port đủ vào `C2`.
   - `_menu.smoke.spec.ts` → có 3 ca gốc: (a) admin bấm nhóm rail "Quản lý phòng họp" → kiểm
     `.rows .row` đếm đúng 2, `href` của "Danh sách phòng họp" đúng, "Đăng ký phòng họp" CHƯA có
     `href` (Phase 2), rồi click qua kiểm bảng render; (b) tương tự cho nhóm "Danh mục" +
     "Tiện nghi phòng họp"; (c) nocost vào thẳng URL bị đẩy 404 + bảng không render. Chỉ ca (c) được
     port (nhóm D, nay có thêm assert nút "Tạo mới"). **Ca (a) và (b) — phép đo sidebar HUB (bấm mở
     nhóm rail, đếm số dòng trong panel, kiểm thuộc tính `href` của từng mục menu) — KHÔNG được port**,
     vì 8 nhóm ca tối thiểu của `task-10-brief.md` không yêu cầu lại phần này (thuộc phạm vi Task 9,
     đã có báo cáo riêng `task-9-report.md` với dòng tổng kết 4/4 passed tại thời điểm đóng task đó).
     Nếu coordinator muốn giữ phép đo menu-rail này trong bộ hồi quy dài hạn (chống hỏng menu sau này
     khi ai đó sửa `components/subsystem-menu/meeting.js` hoặc sidebar hub dùng chung), cần 1 task bổ
     sung riêng — chưa có ca nào chặn hồi quy cho phần đó ở bộ hiện tại.

3. Ca bảo mật (nhóm E) phụ thuộc `mysql` CLI có sẵn trên máy chạy test (đã thử nhiều đường dẫn binary
   phổ biến, không có thì lỗi rõ ràng thay vì âm thầm bỏ qua) và đọc `.env` của worktree API tại
   runtime — nếu sau này việc merge worktree về nhánh chính đổi đường dẫn `.env`, cần cập nhật hằng
   `WORKTREE_API_REPO` trong spec.

4. Không phát hiện lỗi sản phẩm mới nào trong quá trình viết/fix Task 10 (không sửa `pages/meeting/*`
   hay BE).
