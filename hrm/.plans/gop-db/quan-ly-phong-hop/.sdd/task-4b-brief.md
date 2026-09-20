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

## Task 4b: Dựng đường đăng nhập e2e cho worktree (thêm 17/09/2026 — Ruling R6)

**Vì sao có task này:** bộ e2e của dự án **hỏng sẵn trên DB gộp**, không phải do worktree — `api-setup`
chết vì `Table 'hrm_erp.hrm_employees' doesn't exist`, tài khoản fixture `e2e_assign@test.local` không tồn
tại trong bảng `employees`, và token trong `.auth/api.json` / `.auth/user.json` trả **401 ở cả `:8000` lẫn
`:8001`** (token chưa hết hạn nhưng đã bị vô hiệu). Không sửa `e2e/auth/api.setup.ts` và
`database/e2e_provision.php` — tài sản dùng chung, phải qua PR.

**Files:**
- Create: `.plans/gop-db/quan-ly-phong-hop/.sdd/mint-auth.php` (script chạy qua tinker, KHÔNG nằm trong repo code)
- Create: `e2e/.auth/api-wt.json`
- Overwrite: `e2e/.auth/user-wt.json`, `e2e/.auth/user-nocost-wt.json` (đang giữ token chết)
- **KHÔNG đụng**: `e2e/.auth/api.json`, `user.json`, `user-nocost.json` (của phiên khác)

**Interfaces:**
- Produces: `e2e/.auth/api-wt.json` dạng `{ "token": "<JWT>", "employee_id": <id> }`;
  `user-wt.json` / `user-nocost-wt.json` là storageState hợp lệ cho origin `http://127.0.0.1:3001`

**Thông tin đã kiểm chứng sẵn — dùng luôn, đừng khảo sát lại:**
- Guard JWT dùng model **`App\Models\TpEmployee`** (`config/auth.php:44,70`).
- Phân quyền đọc qua `Employee::roles` + `role_has_permissions.company_id = auth()->user()->current_company_role`
  (`app/Helper/PermissionHelper.php:19-34`). Bảng `model_has_roles` **không tồn tại** trên DB gộp.
- Role nhiều quyền nhất: `Super admin` (id 18, 2464 quyền), kế tiếp `Admin_TPE` (id 19, 1892 quyền).
- Nuxt chỉ cần đúng 1 khoá `access_token` trong localStorage (kiểm từ `user.json` cũ).

- [ ] **Bước 1: Chọn 2 tài khoản**

```sql
-- tài khoản CÓ quyền: phải thấy 'Quản lý danh mục phòng họp' (Task 4 đã seed + gán)
SELECT e.id, e.email, e.current_company_role FROM employees e
JOIN <bảng nối role của employee> ... WHERE p.name = 'Quản lý danh mục phòng họp' LIMIT 3;
-- tài khoản KHÔNG quyền: employee bất kỳ không nằm trong danh sách trên
```
Tự xác định tên bảng nối bằng cách đọc quan hệ `roles()` trong `Modules/Timesheet/Entities/Employee.php`
(KHÔNG đoán tên bảng — `model_has_roles` không có trên DB này).

- [ ] **Bước 2: Viết script mint token**

```php
// .sdd/mint-auth.php — chạy bằng: php artisan tinker --execute="require '<đường dẫn tuyệt đối>';"
$ids = [/* id có quyền */, /* id không quyền */];
foreach ($ids as $id) {
    $u = \App\Models\TpEmployee::find($id);
    echo 'MINT=' . json_encode(['id' => $id, 'token' => \JWTAuth::fromUser($u)]) . PHP_EOL;
}
```

- [ ] **Bước 3: Ghi 3 file auth** (`api-wt.json`, `user-wt.json`, `user-nocost-wt.json`).
  storageState đúng khuôn:

```json
{"cookies": [], "origins": [{"origin": "http://127.0.0.1:3001",
  "localStorage": [{"name": "access_token", "value": "<JWT>"}]}]}
```

- [ ] **Bước 4: Kiểm token thật sự dùng được (API)**

```bash
TOK=$(python3 -c "import json,io;print(json.load(io.open('e2e/.auth/api-wt.json'))['token'])")
curl -s -o /dev/null -w "%{http_code}
" -H "Authorization: Bearer $TOK" -H "Accept: application/json" \
  http://127.0.0.1:8001/api/v1/assign/meeting_cancel_reasons
```
Kỳ vọng: **200**. Nếu vẫn 401 → BLOCKED, báo lại ngay, đừng tự tạo tài khoản mới trong DB dùng chung.

- [ ] **Bước 5: Kiểm token dùng được ở UI** — Playwright mở `http://127.0.0.1:3001/meeting/dashboard` với
  `storageState: '.auth/user-wt.json'`, kỳ vọng **KHÔNG** bị đẩy về `/login` và có phần tử sidebar phân hệ.

- [ ] **Bước 6: Ghi lại vào báo cáo** id + email của 2 tài khoản đã chọn, để các task sau dùng đúng.

---
