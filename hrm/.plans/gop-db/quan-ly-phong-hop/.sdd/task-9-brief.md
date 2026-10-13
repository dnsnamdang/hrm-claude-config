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


> **Cơ chế gate route (đã kiểm chứng, dùng đúng thế này):**
> `middleware/checkPermission.js` là **middleware toàn cục** (khai ở `nuxt.config.js` mục
> `router.middleware`). Nó tra `route.path` trong registry menu (`components/subsystems.js` →
> `getAllMenuItems()`); nếu mục menu có `isShow` là MẢNG tên quyền mà user không khớp quyền nào →
> `redirect('/pages/extras/404')`. Vì vậy **việc đăng ký menu ở task này CHÍNH LÀ lớp chặn URL trực tiếp** —
> khai thiếu `isShow`, hoặc khai `isShow: true`, là màn mở toang cho mọi người đăng nhập.
> ⚠️ `isShow` phải là mảng tên quyền ĐÚNG TỪNG KÝ TỰ như trong DB:
> `['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp']` và
> `['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp']`.


## Task 9: Cập nhật menu phân hệ Meeting

**Files:**
- Modify: `hrm-client/components/subsystem-menu/meeting.js:24-36` (nhóm Danh mục) và `:44-52` (nhóm Quản lý phòng họp)

- [ ] **Bước 1: Thêm mục Tiện nghi vào nhóm Danh mục**

```js
{
    label: 'Tiện nghi phòng họp',
    link: '/meeting/room-amenities',
    isShow: ['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp'],
},
```

- [ ] **Bước 2: Điền link cho mục đang treo trống**

```js
{
    label: 'Quản lý phòng họp',
    icon: 'ri-door-open-line',
    isMenuCollapsed: false,
    subItems: [
        {
            label: 'Danh sách phòng họp',
            link: '/meeting/rooms',
            isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp'],
        },
        { label: 'Đăng ký phòng họp' },   // Phase 2 mới điền link
    ],
},
```

- [ ] **Bước 3: Kiểm EOL không bị phá**

```bash
cd hrm-client && git diff --numstat components/subsystem-menu/meeting.js
```
Kỳ vọng: số dòng thêm/xóa nhỏ (đúng phần vừa sửa). Cả file bị đánh dấu đổi = đã phá line ending → trả lại.

- [ ] **Bước 4: Kiểm menu render thật** — Playwright MCP mở `http://127.0.0.1:3000/meeting/dashboard`,
  đếm số mục trong nhóm *Danh mục* và *Quản lý phòng họp* bằng DOM; bấm vào *Danh sách phòng họp* phải
  điều hướng đúng `/meeting/rooms` và **render ra bảng** (vào được trang chưa chứng minh gate còn sống —
  phải đo nội dung render ra DOM).

---
