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


> **Ca BẮT BUỘC bổ sung (từ re-review Task 6) — kiểm lớp Resource của `checkin_qr_token`:**
> Lỗ bảo mật đã bịt ở 2 lớp: (1) route `GET /meeting/rooms/{id}` gắn `checkPermission`, (2) Resource chỉ trả
> `checkin_qr_token` khi có quyền `Quản lý danh mục phòng họp`. Ca e2e hiện có dùng tài khoản nocost — thiếu
> CẢ HAI quyền nên bị chặn ngay ở lớp route, **lớp (2) chưa có ca nào chạm tới**. Cần 1 ca dùng tài khoản
> **CÓ "Xem danh mục phòng họp" nhưng KHÔNG có "Quản lý danh mục phòng họp"**:
> - Cách dựng: cấp tạm quyền id **1575** (`Xem danh mục phòng họp`) cho role mà nhân viên id 25 đang có,
>   với `company_id = 1`, chạy ca kiểm, rồi **thu hồi lại đúng dòng vừa cấp** ở `afterAll`.
>   (Tra role của nhân viên 25 trong bảng **`employee_has_roles`** — KHÔNG phải `model_has_roles`.)
> - Khẳng định: gọi `GET /meeting/rooms/{id}` nhận **200** (vì đã có quyền xem) nhưng body **KHÔNG chứa**
>   `checkin_qr_token`.
> - ⚠️ DB dùng chung với phiên khác → phải thu hồi sạch, kiểm lại bằng truy vấn sau khi chạy.



> **Ca BẮT BUỘC: chứng minh gate route còn sống** (quy tắc dự án: "vào được trang ≠ gate còn sống").
> Với tài khoản THIẾU quyền (`.auth/user-nocost-wt.json`), vào thẳng `/meeting/rooms` và
> `/meeting/room-amenities` bằng URL: phải bị **redirect khỏi trang** (middleware đẩy về
> `/pages/extras/404`) — assert bằng `page.url()` VÀ assert bảng dữ liệu KHÔNG render
> (`expect(page.locator('table tbody tr')).toHaveCount(0)` hoặc tương đương). Chỉ kiểm "menu không hiện mục"
> là CHƯA đủ.


## Task 10: E2E UI + chạy lại toàn bộ bộ test của màn

**Files:**
- Create: `e2e/tests/meeting/meeting-room.spec.ts`

> **Ruling R1 (pre-flight):** `e2e/utils/` KHÔNG có helper `api` / `noPermApi` dùng chung — code mẫu dưới
> đây là mô tả ca kiểm, không phải code chạy nguyên văn. Mỗi spec **tự dựng `APIRequestContext`** theo khuôn
> `e2e/tests/assign/customer-demand-link.api.spec.ts` (đọc token từ `e2e/.auth/api.json`). Ca "không quyền"
> dùng tài khoản nocost có sẵn: `test.use({ storageState: '.auth/user-nocost.json' })` (sinh bởi
> `e2e/auth/login-nocost.setup.ts`). Nếu project `api-setup` đỏ trên DB gộp (bẫy đã biết: thiếu bảng
> `hrm_employees`) thì chạy spec lẻ bằng `--no-deps`.

- [ ] **Bước 1: Viết ca UI** — phủ: vào màn thấy bảng · tạo phòng qua modal · gắn 2 tiện nghi ·
  khóa phòng thấy cảnh báo đúng số phiếu · **tài khoản không quyền không thấy nút Thêm và vào URL trực tiếp
  không render được bảng**.

- [ ] **Bước 2: Kiểm khuôn giao diện bằng số đo, không chỉ assert dữ liệu**

> **Ruling R2 (pre-flight):** màn danh mục KHÔNG dùng `V2Footer` (component đó chỉ có ở màn chi tiết/form)
> → phép đo `.v2-footer` trong bản plan đầu sẽ trả `null` và ca test thành vô nghĩa. Thay bằng 2 phép đo có thật:

```ts
// (a) footer của V2BaseModal phải luôn nằm trong viewport kể cả khi body modal cuộn
await page.locator('.modal.show .modal-body').evaluate((el) => { el.scrollTop = el.scrollHeight; });
const footer = await page.locator('.modal.show .modal-footer').boundingBox();
const viewport = page.viewportSize()!;
expect(footer!.y + footer!.height).toBeLessThanOrEqual(viewport.height);

// (b) bảng không đẩy cả trang tràn ngang
const overflow = await page.evaluate(() => document.body.scrollWidth - document.body.clientWidth);
expect(overflow).toBeLessThanOrEqual(0);
```

- [ ] **Bước 3: Chạy cả thư mục, đọc dòng tổng kết**

```bash
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/meeting --workers=1
```
Kỳ vọng: dòng tổng kết ghi đủ số ca passed, **không có ca nào "did not run"**.

- [ ] **Bước 4: Cập nhật plan** — đánh `[x]` các task đã xong, ghi Checkpoint theo đúng format.

---
