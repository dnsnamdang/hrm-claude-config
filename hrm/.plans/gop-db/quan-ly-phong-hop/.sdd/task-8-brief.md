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


> **2 phát hiện từ Task 7 — BẮT BUỘC áp dụng, đừng lặp lại lỗi:**
>
> 1. **`$store.state.permissions` là mảng OBJECT `{id, name, ...}`, KHÔNG phải mảng chuỗi.**
>    Viết `perms.includes('Quản lý danh mục phòng họp')` là **luôn false** → cờ quyền fail-closed vĩnh viễn,
>    nút biến mất với cả người có quyền, mà console không báo gì. Dùng đúng khuôn có sẵn:
>    `perms.some(p => p.name === 'Quản lý danh mục phòng họp')`, hoặc dùng mixin
>    `utils/mixins/CheckPermission.js` (`hasAPermission()`).
> 2. **`components/modal/V2BaseModal.vue` nay đã có method `hide()`** (alias của `close()`, Task 7 bổ sung)
>    để dùng được `unsavedModalMixin` — mixin gọi `this.$refs[ref].hide()`. Cứ dùng bình thường,
>    KHÔNG sửa lại component dùng chung đó lần nữa.
>
> **Ràng buộc giữ nguyên**: modal dựng trên `V2BaseModal`, select trong modal dùng `V2BaseSelectInModal`,
> xác nhận dùng `$confirm`/`base-confirm-modal`, badge dùng `V2BaseBadge`, số dùng `toLocaleString('en-US')`,
> cấm `.text-muted`, nút không dùng được thì ẩn hẳn.


## Task 8: FE màn Danh sách phòng họp `/meeting/rooms`

**Files:**
- Create: `hrm-client/pages/meeting/rooms/index.vue`
- Create: `hrm-client/pages/meeting/rooms/components/MeetingRoomModal.vue`

**Interfaces:**
- Consumes: API Task 6 (`/meeting/rooms`, `/form-options`, `/{id}/upcoming-bookings`)

- [ ] **Bước 1: Trang danh sách** — cột: Mã · Tên phòng · Công ty · Vị trí · Sức chứa · Tiện nghi (chip) ·
  Người quản lý · Cần duyệt · Cho công ty khác đặt · Trạng thái · Hành động.
  Sức chứa hiển thị bằng `Number(x).toLocaleString('en-US')`.

- [ ] **Bước 2: Bộ lọc** — Tìm nhanh placeholder `Tìm theo mã, tên phòng, vị trí`; các ô lọc còn lại
  (công ty, sức chứa tối thiểu, tiện nghi, trạng thái) theo chế độ gọn có nhãn floating → **bỏ placeholder
  trùng nhãn**.

- [ ] **Bước 3: Modal thêm/sửa** — 1 request `GET /meeting/rooms/form-options` lúc mở modal
  (KHÔNG gọi ở `mounted`, KHÔNG bắn nhiều API rời rạc).
  - Tiện nghi: `V2BaseSelectInModal` chọn nhiều
  - Người quản lý: select nhân viên, nhãn theo khuôn chuẩn `utils/employeeOptionText.js`
    (`Tên nhân viên - Mã phòng - Mã nhân viên`)
  - Bố cục mỗi hàng đủ 12 cột, không để ô lẻ một dòng
  - Khối nhóm dùng `components/V2BaseFormSection.vue`

- [ ] **Bước 4: Cảnh báo khi Khóa phòng còn phiếu sắp tới**

```js
async onLock(room) {
    const { data } = await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/upcoming-bookings`)
    const message = data.count > 0
        ? `Phòng còn ${Number(data.count).toLocaleString('en-US')} phiếu đặt sắp tới. Khóa phòng sẽ gửi thông báo cho người đặt để đổi phòng. Bạn chắc chắn khóa?`
        : 'Bạn chắc chắn muốn khóa phòng họp này?'
    const ok = await this.$confirm({ title: 'Khóa phòng họp', message })
    if (!ok) return
    await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/lock`)
    await this.fetchList()
}
```

- [ ] **Bước 5: Ẩn nút Xóa khi phòng đã có phiếu** — đọc cờ `is_can_delete` do BE trả trong Resource,
  đặt trong `visible` của cột Hành động. **Không** dùng `interactable` + `disabledTitle`.

- [ ] **Bước 5b: Nút *Xem lịch phòng* — HOÃN sang Phase 3.** Màn `/meeting/room-board` chưa tồn tại;
  thêm nút trỏ vào route chết là nút hỏng im lặng. Phase 3 bổ sung nút này vào **cả** cột Hành động
  của màn danh sách lẫn footer màn chi tiết.

- [ ] **Bước 6: Tự kiểm HTML thô + cờ quyền**

```bash
grep -rn '<input \|<textarea\|<select \|<button \|<label ' pages/meeting/rooms/ | grep -v V2Base    # rỗng
grep -rnE 'can[A-Za-z]*\s*=\s*true' pages/meeting/rooms/                                            # rỗng
```

---
