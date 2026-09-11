# Plan — Bộ lọc Công ty/Phòng ban/Bộ phận/Nhân viên: tuỳ chọn hiện mục đã khoá

Người phụ trách: @namdangit · Nhánh: **`gop_db`** (worktrees/gop_db-api + gop_db-client)

> Lần đầu code nhầm trên nhánh `tpe`, đã port sang `gop_db` và **hoàn nguyên sạch `tpe`** (2026-08-24).

## Phase 1 — Công tắc 🔒 theo từng ô

### BE
- [x] `Employee::getAll($onlyActive = false)` — thêm tham số, mặc định giữ nguyên hành vi cũ
- [x] `AuthNewController::userProfile()` gọi `getAll(true)` → store.employees chỉ còn nhân sự đang làm
- [x] `OrgOptionController@index` — `GET /api/v1/org-options?type=company|department|part|employee`, trả cả bản ghi khoá kèm cờ `is_locked`
- [x] Đăng ký route trong `routes/api.php` (middleware `auth:api`)

### FE
- [x] `V2BaseSelect` + `V2BaseSelectInModal`: thêm prop `keepLockedOptions` (default false) để bỏ qua `filterUnusedLockedOptions`
- [x] `V2BaseCompanyDepartmentFilter`: nút icon 🔒/🔓 cạnh nhãn từng ô + popover mô tả
- [x] Lazy load danh sách đầy đủ khi bật công tắc, cache trong component (KHÔNG đẩy vào Vuex)
- [x] Giữ nguyên logic phân quyền + cascade cha-con cho cả danh sách đã khoá
- [x] Tắt công tắc: quay về danh sách hoạt động, giữ lại option đang được chọn
- [x] Prop `showLockedToggle` (default true) để màn nào cần thì tắt

### Checkpoint — 2026-08-24
Vừa hoàn thành: toàn bộ Phase 1 (BE + FE)
Đã test trên UI thật (Playwright, http://127.0.0.1:3000/assign/customers, tài khoản DNS Admin):
- Vào màn: chưa gọi API nào, 3 công tắc đều tắt; store còn 556 nhân viên (đã bỏ 530 người nghỉ)
- Bật Công ty: 5 → 8 (3 mục 🔒); chọn công ty khoá → ô hiện 🔒, phòng ban 63 → 5, nhân viên 556 → 9
- Tắt Công ty: về 5 + giữ đúng công ty khoá đang chọn (có 🔒); bỏ chọn → option khoá biến mất ngay
- Bật Phòng ban: 63 → 82 (19 🔒); chọn 🔒 Kho hàng → lọc chạy `department_id=101` HTTP 200; tắt công tắc vẫn giữ giá trị (82 → 64)
- Bật Nhân viên: 556 → 1087 (531 🔒); chọn 🔒 HN_KDTM - Bùi Văn Long → lọc chạy `employee_id=26` HTTP 200
- Console: 0 lỗi. Thời gian API: company 93ms/947B · department 74ms/9,6KB · part 61ms/2,6KB · employee 83ms/160KB
- Guard endpoint: type sai → 422, không token → 401
Bước tiếp theo: bàn giao / merge
Blocked:

### Checkpoint — 2026-08-24 (canh icon)
Vừa hoàn thành: sửa icon 🔒 bị lệch so với nhãn.
Nguyên nhân: bọc nhãn + icon trong `<div class="odf-label-row">` flex — `<label>` mang sẵn
`margin-bottom: 8px` của bootstrap nên chữ bị đẩy lên 4px so với icon; bọc thêm div còn ăn mất
3px line-box khiến ô có công tắc lệch lên so với ô thường (top 181.4 vs 184.4).
Cách sửa: bỏ wrapper, đặt `<span class="odf-lock-toggle">` NGAY TRONG `<V2BaseLabel>`
(component này đã là `inline-flex` + `align-items: center` + `gap: 4px`).
Đo lại: icon lệch 0px, cả 4 ô select cùng top = 184.4. Công tắc vẫn chạy (5 → 8 công ty).
Bước tiếp theo: bàn giao / merge
Blocked:

### Checkpoint — 2026-08-24 (port sang gop_db)
Vừa hoàn thành: chuyển toàn bộ thay đổi sang worktree `gop_db`, hoàn nguyên nhánh `tpe`.
- 5/6 file ở gop_db giống hệt bản tpe → copy thẳng; riêng `routes/api.php` lệch 16 dòng nên chèn tay.
- DB gộp `local_hrm_erp`: model `Company`/`Department`/`Part` không khai `$table` nhưng KHÔNG dính bẫy
  `hrm_*` — đọc đúng `companies`/`departments`/`parts` (chỉ có `hrm_employees` tồn tại, và
  `Employee` khai sẵn `$table = 'employees'`). Endpoint dùng ĐÚNG model mà `userProfile()` dùng.
- Số liệu gop_db: công ty 5/3 · phòng ban 68/19 · bộ phận 15/10 · nhân sự 555/544 (hoạt động/khoá).
- Verify Playwright trên :3002 (`/assign/customers`, màn này có đủ 4 ô): vào màn chưa gọi API, công tắc
  đều tắt, store còn 552 nhân viên; bật Công ty 5 → 8 (3 🔒), bật Bộ phận 15 → 25 (10 🔒), 2 ô còn lại
  không bị lây; icon 🔒 lệch 0px, 4 ô select cùng một đường; 0 lỗi console.
Bước tiếp theo: commit lên `gop_db`
Blocked:
