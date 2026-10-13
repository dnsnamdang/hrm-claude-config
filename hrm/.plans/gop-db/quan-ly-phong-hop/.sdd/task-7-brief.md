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

## Task 7: FE màn Danh mục tiện nghi `/meeting/room-amenities`

**Files:**
- Create: `hrm-client/pages/meeting/room-amenities/index.vue`
- Create: `hrm-client/pages/meeting/room-amenities/components/RoomAmenityModal.vue`

**Interfaces:**
- Consumes: API Task 5
- Produces: màn danh mục chạy được, dùng làm khuôn cho Task 8

> **Copy khuôn** từ `hrm-client/pages/assign/meeting_cancel_reason/index.vue` (bảng + bộ lọc + modal +
> khóa/mở khóa + xác nhận xóa). Gọi API bằng `this.$store.dispatch('apiGet' | 'apiPostMethod' | 'apiDelete', …)`
> đúng như file gốc (dòng 543, 648, 668, 838).

- [ ] **Bước 1: Dựng trang danh sách** — `layout: 'default-sidebar'`, cột: Mã · Tên tiện nghi · Icon ·
  Thứ tự · Trạng thái · Người cập nhật · Hành động.
  Badge trạng thái dùng `V2BaseBadge` với `variant` (`brand` = Hoạt động, `required` = Khóa) — đây là
  danh mục dùng chung 2 trạng thái cố định nên **không cần BE trả màu**.

- [ ] **Bước 2: Cờ quyền fail-closed**

```js
data() {
    return {
        canManage: false,   // KHÔNG được gán true
        canView: false,
    }
},
mounted() {
    const perms = this.$store.state.permissions || []
    this.canManage = perms.includes('Quản lý danh mục tiện nghi phòng họp')
    this.canView = this.canManage || perms.includes('Xem danh mục tiện nghi phòng họp')
}
```

- [ ] **Bước 3: Modal thêm/sửa** dựng trên `components/modal/V2BaseModal.vue`; các ô:
  `V2BaseInput` (Mã, Tên), `V2BaseSelectInModal` (Icon), `V2BaseInput` số (Thứ tự).
  Nút Xóa dùng `components/modal/base-confirm-modal.vue`, **không** tạo confirm riêng.

- [ ] **Bước 4: Tự kiểm không có HTML thô**

```bash
cd hrm-client
grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/meeting/room-amenities/ | grep -v V2Base
```
Kỳ vọng: **rỗng**.

- [ ] **Bước 5: Kiểm trên trình duyệt thật bằng Playwright MCP** — mở
`http://127.0.0.1:3000/meeting/room-amenities`, tạo 1 bản ghi, khóa, mở khóa, xóa.
Đo bằng số lấy từ DOM (số dòng bảng trước/sau khi tạo), không chỉ nhìn ảnh.

---
