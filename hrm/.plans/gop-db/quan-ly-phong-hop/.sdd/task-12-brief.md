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

## Task 12: 2 quyền mới + luật nhìn thấy phiếu

**Files:** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (+2 dòng, id **1579-1580**)

- [ ] **Bước 1:** thêm `Xem tất cả phiếu đặt phòng họp` (1579), `Duyệt phiếu đặt phòng họp` (1580),
  group `Quản lý phòng họp`, `type = 4`. Kiểm trùng id/tên như Task 4.
- [ ] **Bước 2:** INSERT 2 quyền + cấp cho role Super admin (18) `company_id = 1` **bằng SQL có chủ đích**
  — **KHÔNG chạy `db:seed`** (Ruling R7 vẫn còn hiệu lực: seeder xoá 472 quyền DB đang có).
- [ ] **Bước 3:** kiểm `SELECT COUNT(*) FROM permissions WHERE guard_name='api'` = **747** (745 + 2).
- [ ] **Bước 4 — luật nhìn thấy phiếu** (áp dụng ở Task 14, ghi ở đây cho tập trung): không có quyền 1579 thì
  chỉ thấy phiếu **mình đặt**, **mình được mời** (bảng participants), **hoặc phiếu của phòng mình quản lý**
  (`meeting_rooms.manager_employee_id = <mình>`). Thiếu vế cuối là quản lý phòng không thấy phiếu cần mình duyệt.
