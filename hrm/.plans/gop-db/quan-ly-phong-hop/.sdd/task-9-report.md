# Task 9 — Cập nhật menu phân hệ Meeting — Báo cáo

**Status: HOÀN THÀNH**

## File sửa

`hrm-client/components/subsystem-menu/meeting.js` (worktree `phong-hop-client`) — đúng 2 chỗ:

1. Nhóm `Danh mục`: thêm mục `Tiện nghi phòng họp` (`link: '/meeting/room-amenities'`, `isShow: ['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp']`).
2. Nhóm `Quản lý phòng họp`: điền link cho `Danh sách phòng họp` (`link: '/meeting/rooms'`, `isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp']`). `Đăng ký phòng họp` giữ nguyên không link (Phase 2).

### `git diff --numstat`

```
11      2       components/subsystem-menu/meeting.js
```

Diff gọn, đúng 2 vùng sửa, không đánh dấu đổi cả file (kiểm `file` + `grep -c $'\r'` xác nhận file gốc là LF/UTF-8, không lẫn CRLF — không có gì bị phá).

## Phát hiện quan trọng trước khi viết e2e

Phân hệ `meeting` nằm trong `HUB_SUBSYSTEMS` (`components/subsystem-menu/hub.js`) → sidebar dùng kiểu
HUB/MISA (`components/sale/SaleHubSidebar.vue`, class `.sale-cats` / `.misa-detail`), **không phải**
cây UBold `#side-menu` cũ mà brief mô tả ban đầu. Đã dò DOM thật bằng 1 script Playwright tạm (đã xoá)
trước khi viết spec chính thức, thay vì đoán selector theo brief.

Panel nhóm mở ra render `.misa-detail .rows .row[data-k]`; mỗi `.row` có `href` nếu màn đã có `link`,
không có `href` nếu màn chưa xây dựng (bấm chỉ nổi toast "Tính năng đang phát triển").

⚠️ Đo thật: panel "Danh mục" với tài khoản admin worktree (`.auth/user-wt.json`) chỉ hiện **2 dòng**
(Loại meeting, Tiện nghi phòng họp) chứ không phải 3 — mục "Lý do hủy cuộc họp" (đã có từ trước, Task 9
không đụng tới) bị `isScreenVisible()` lọc mất vì tài khoản admin worktree không có quyền "Quản lý/Xem
danh mục lý do hủy cuộc họp". Đây là gap quyền có sẵn từ trước, không liên quan thay đổi của Task 9 —
assertion bám đúng số đo thật (2), có ghi chú trong spec.

## Kiểm chứng Playwright (spec `e2e/tests/meeting/_menu.smoke.spec.ts`)

Lệnh chạy:
```
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
npx playwright test tests/meeting/_menu.smoke.spec.ts --project=chromium --no-deps --workers=1
```

**Dòng tổng kết:**
```
Running 4 tests using 1 worker
  ✓ 1 [chromium] › Meeting — sidebar hub, admin (đủ quyền) › Nhóm Quản lý phòng họp: 2 mục, Danh sách phòng họp có link và render bảng thật (7.4s)
  ✓ 2 [chromium] › Meeting — sidebar hub, admin (đủ quyền) › Nhóm Danh mục: Tiện nghi phòng họp có link và render bảng thật (7.5s)
  ✓ 3 [chromium] › Meeting — vào thẳng URL, tài khoản THIẾU quyền › /meeting/rooms bị đẩy khỏi trang, bảng KHÔNG render (6.7s)
  ✓ 4 [chromium] › Meeting — vào thẳng URL, tài khoản THIẾU quyền › /meeting/room-amenities bị đẩy khỏi trang, bảng KHÔNG render (3.8s)
  4 passed (26.9s)
```
Không có "did not run"; đọc đúng dòng tổng kết theo yêu cầu (bộ chạy `serial`).

### Đo DOM từng bước (tài khoản admin)

- Nhóm "Quản lý phòng họp": `panel.locator('.rows .row')` → `toHaveCount(2)`. Row "Danh sách phòng họp"
  có `href="/meeting/rooms"`; row "Đăng ký phòng họp" tồn tại (count 1) nhưng `getAttribute('href') === null`
  — xác nhận Phase 2 vẫn treo trống đúng ý.
- Bấm "Danh sách phòng họp" → `page.waitForURL('**/meeting/rooms')` → ô tìm `Tìm theo mã, tên phòng, vị trí`
  visible → `table.data-table tbody tr` có ≥1 dòng render thật ra DOM (không chỉ URL đổi).
- Nhóm "Danh mục": `panel.locator('.rows .row')` → `toHaveCount(2)` (giải thích gap quyền ở trên). Row
  "Tiện nghi phòng họp" có `href="/meeting/room-amenities"`.
- Bấm "Tiện nghi phòng họp" → URL `/meeting/room-amenities` → ô tìm `Tìm theo mã, tên tiện nghi` visible →
  bảng có ≥1 dòng trong DOM.

### Ca tài khoản THIẾU quyền (`.auth/user-nocost-wt.json`)

- Vào thẳng `/meeting/rooms` bằng URL → bị `checkPermission.js` redirect, `page.url()` chứa
  `/pages/extras/404`; đo DOM: ô tìm `Tìm theo mã, tên phòng, vị trí` → `toHaveCount(0)`,
  `table.data-table` → `toHaveCount(0)` (bảng KHÔNG render, không chỉ dựa vào URL).
- Vào thẳng `/meeting/room-amenities` bằng URL → cùng kết quả: redirect `/pages/extras/404`, ô tìm
  `Tìm theo mã, tên tiện nghi` và `table.data-table` đều `toHaveCount(0)`.

→ Lớp chặn URL trực tiếp (`middleware/checkPermission.js` tra `isShow` vừa khai) **còn sống** cho cả 2
màn mới đăng ký menu.

## Concerns

1. `git status` trong worktree còn cho thấy `components/modal/V2BaseModal.vue` bị sửa — **không phải do
   task này**, có khả năng là do task khác đang chạy song song trong cùng worktree. Không đụng tới file
   đó, chỉ ghi nhận lại để tránh hiểu nhầm khi review diff tổng.
2. Tài khoản admin worktree thiếu quyền "Quản lý/Xem danh mục lý do hủy cuộc họp" (mục cũ, không phải
   Task 9 tạo ra) — không chặn task này nhưng nên báo lại nếu có ai cần audit quyền của tài khoản test.
3. Spec `_menu.smoke.spec.ts` là spec tạm (tiền tố `_`) đúng theo khuôn 2 spec UI trước đó của plan
   (`_room-ui.smoke.spec.ts`, `_room-amenity-ui.smoke.spec.ts`) — Task 10 sẽ viết bộ e2e chính thức.
