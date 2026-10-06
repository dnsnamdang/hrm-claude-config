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

## Task 1: Tạo module `Modules/Meeting`

**Files:**
- Create: `hrm-api/Modules/Meeting/**` (sinh bằng artisan)
- Modify: `hrm-api/Modules/Meeting/Routes/api.php`

**Interfaces:**
- Consumes: —
- Produces: prefix route `/api/v1/meeting/...` nạp được; namespace `Modules\Meeting\…`

- [ ] **Bước 1: Sinh module**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan module:make Meeting
```

- [ ] **Bước 2: Dọn phần thừa**

Xóa `Modules/Meeting/Resources/assets`, `Modules/Meeting/Resources/views`, `webpack.mix.js`,
`package.json` (module này chỉ có API, không có asset FE). Giữ `Config`, `Database`, `Entities`,
`Http`, `Providers`, `Routes`, `Services`, `Transformers`, `Tests`.

- [ ] **Bước 3: Khai route prefix giống module khác**

Mở `Modules/Meeting/Routes/api.php`, thay nội dung mặc định bằng khung rỗng đúng chuẩn dự án
(xem `Modules/Assign/Routes/api.php:1-20` để copy phần `Route::group` + middleware auth):

```php
<?php

use Illuminate\Support\Facades\Route;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Danh mục tiện nghi phòng họp + danh mục phòng họp khai ở Task 5, Task 6
});
```

- [ ] **Bước 4: Kiểm module đã nạp**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan module:list | grep -i meeting
/opt/homebrew/opt/php@7.4/bin/php artisan route:list --path=meeting | head
```
Kỳ vọng: `Meeting` xuất hiện trong `module:list` (Enabled).

⚠️ Nếu `config:cache` đang trỏ production (bẫy đã biết của repo) thì chạy
`/opt/homebrew/opt/php@7.4/bin/php artisan config:clear` trước, nếu không artisan đọc nhầm DB.

- [ ] **Bước 5: Tự kiểm** — `git status` ở `hrm-api` chỉ thấy file trong `Modules/Meeting/`, không đụng file khác.

---
