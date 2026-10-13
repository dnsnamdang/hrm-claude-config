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

## Task 16: FE màn danh sách phiếu `/meeting/bookings`

- [ ] Bộ lọc: khoảng ngày · phòng · công ty · trạng thái · người đặt · công tắc **Chỉ phiếu của tôi**
  (mặc định **bật** với người không có quyền 1579).
- [ ] Cột: Mã · Tiêu đề · Phòng · Thời gian · Người đặt · Chủ trì · Số người · Nguồn · Trạng thái
  (badge dùng `status_color` BE trả).
- [ ] Hành động đọc **từ cờ BE**, ẩn hẳn khi không dùng được, **đồng bộ y hệt** ở footer màn chi tiết.
- [ ] Điền link menu **Đăng ký phòng họp** → `/meeting/bookings`, `isShow` = 2 quyền phòng họp
  (đây cũng là lớp chặn URL — xem ghi chú cơ chế gate ở Task 9).
- [ ] 2 lệnh grep tự kiểm phải rỗng; cờ quyền qua mixin `CheckPermission`.
