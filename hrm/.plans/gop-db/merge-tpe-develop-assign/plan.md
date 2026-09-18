# Merge `tpe-develop-assign` → `gop_db` (2026-09-14)

## Phase 1 — Kéo code + merge

### Chung
- [x] `git fetch` + `pull --ff-only` cả 2 repo (`hrm-api`, `hrm-client`), 2 nhánh
- [x] Merge `origin/tpe-develop-assign` vào `gop_db` ở 2 worktree `worktrees/gop_db-api`, `worktrees/gop_db-client`

### BE (`hrm-api` — 23 file xung đột)
- [x] Bỏ `Modules/Human/{Services/CustomerService,Http/Requests/SaveCustomerRequest}.php` (đã chuyển sang `Modules/Assign`)
- [x] Nhóm Quận/Huyện (6 file): giữ bản `gop_db`; gỡ nhóm route `/human/districts` trùng + 1 dòng `use` trùng
- [x] Giữ cả 2 bên: `Meeting`, `Quotation`, `TaskController`, `IssueService`, `MeetingController`
- [x] `ScopeService`: lấy logic #11142 của tpe, đổi `scopes` → `hrm_scopes`
- [x] `Assign/CustomerService::agentEmployees`: giữ connection DB gộp + bổ sung `leftJoin departments`
- [x] `ProspectiveProject`: dùng `resolveStatusColor` đọc `color` trong mảng, bỏ 2 mảng màu trùng, giữ `changeStatusById`
- [x] `ProspectiveProjectResource`: lấy bản tpe (`employeeInfoOf`) + `auto_close_date`/`extended_days`
- [x] `ProspectiveProjectService`: giữ eager-load của gop_db, khai lại `RESOURCE_EAGER_RELATIONS`
- [x] `AuthNewController`: `getAll(true)->load('info')->makeHidden('info')`
- [x] 2 job sync ERP: giữ bản gop_db (đã ngừng dùng sau khi gộp DB)
- [x] `e2e_provision`: logic phòng ban thật của tpe + đổi `employees` → `hrm_employees`
- [x] `php -l` sạch toàn bộ file đã sửa → commit `61a5eb676`

### FE (`hrm-client` — 22 file xung đột)
- [x] Bỏ `human-components/customer/CustomerForm.vue`, `MeetingMinutesModal.vue`
- [x] Màn Quận/Huyện: giữ bản gop_db (quyết định của user, xem design.md)
- [x] 5 file "xung đột cả file" thực chất lệch line ending → chuẩn hoá + merge 3 chiều, giữ EOL nhánh đích
- [x] `menu-sidebar.js` giữ bản gop_db; bổ sung 2 báo cáo vào `sale-hub.js` + "Lý do hủy cuộc họp"
- [x] `base-confirm-modal`: khung gop_db + ô nhập bắt buộc (`requiredInput`) của tpe
- [x] `V2BaseCompanyDepartmentFilter`: giữ 🔒 của gop_db + nhãn NV qua `employeeOptionText()`
- [x] `CustomerForm`: giữ cả khoá/mở khoá + ô Quận/Huyện cho địa chỉ nước ngoài
- [x] 2 màn form-templates: lấy bản tpe đã chuyển `V2BaseModal`
- [x] `ProspectiveProjectQuotationsTab`: lấy `FinalizeQuotationModal`
- [x] 5 màn danh sách: giữ bản gop_db; port thêm gate `can_edit`, cột+ô lọc "Loại nhiệm vụ", đổi chữ issue→Vấn đề / task→nhiệm vụ
- [x] Không còn marker conflict → commit `993cdeda5`

### Checkpoint — 2026-09-14
Vừa hoàn thành: merge xong cả 2 repo, đã commit, **chưa push**.
Bước tiếp theo: build/chạy thử `hrm-client` + smoke test 5 màn đã đụng (tasks, issues, quotations, prospective-projects, meeting) rồi mới push.
Blocked:

## Phase 2 — Kiểm thử sau merge

### Chuẩn bị môi trường
- [x] Chạy 16 migration còn thiếu của nhánh tpe trên DB `local_hrm_erp` (đều là thêm bảng/cột, chạy sạch)
- [x] Thêm 2 quyền "Quản lý/Xem danh mục lý do hủy cuộc họp" + gán role 18 (KHÔNG chạy `PermissionsTableSeeder` vì nó `delete()` sạch bảng `permissions` → mất hết gán quyền của role)
- [x] Đặt mật khẩu test `Test@12345` cho 4 tài khoản local (trừ namdangit@gmail.com)
- [x] Khởi động lại FE dev server (bản cũ treo 100% CPU, giữ cổng 3002)

### Kiểm tra tĩnh
- [x] `php -l` 238 file PHP đổi trong merge bằng **PHP 7.4** (đúng stack) → 0 lỗi
- [x] Parse 278 file `.vue`/`.js` đổi trong merge bằng vue-template-compiler + @babel/parser → phát hiện 2 lỗi, đã vá (commit `e743d75c1`)
- [x] Build Nuxt dev → 0 `ERROR in`

### Kiểm tra API (5 tài khoản khác quyền, qua server PHP 7.4 thật)
- [x] Login 5/5 OK · `user-profile` 200, 555 nhân viên, 0 bản ghi rò khối `info`
- [x] 10 endpoint × 5 tài khoản: prospective-projects, quotations, tasks, issues, meeting, districts (list + getList), scopes/getAll (+ customer_id, current_project_id), agent-employees, form-templates, customers → tất cả 200/403 đúng quyền, 0 lỗi 500
- [x] `agent-employees` trả đủ `department_code` 100/100 dòng (leftJoin bổ sung trong merge)
- [x] `resolveStatusColor`: 12 trạng thái con + 8 trạng thái cha đều ra mã màu; fallback cha→con OK; trạng thái lạ trả null
- [x] `cancel_reason_text` hiện đúng qua quan hệ eager load gộp vào `MeetingController`
- [x] `task_type_text` có dữ liệu ("Nhiệm vụ cụ thể")
- [x] Đếm query 1 trang danh sách: 25–37 query, không tăng theo số dòng → không có N+1

### Kiểm tra UI (Playwright, 5 tài khoản × 10 màn = 50 lượt)
- [x] Màn Nhiệm vụ: tiêu đề "Danh sách nhiệm vụ", cột "Loại nhiệm vụ" có dữ liệu, hết chữ "task"
- [x] Màn Vấn đề: hết chữ "issue" ở cột/tiêu đề
- [x] Popup xác nhận dùng chung: icon tròn, đỏ cho nút Xóa, nút "Xóa/Hủy" đúng
- [x] Ô nhập bắt buộc trong popup (tính năng tpe): bỏ trống → viền đỏ + "Vui lòng nhập nội dung", popup không đóng
- [x] `CustomerForm`: `showDistrict` false→true khi Quốc gia ≠ Việt Nam; vào URL `/edit` khi không đủ quyền thì tự về màn chi tiết
- [x] Màn Dự án TKT: `can_edit=false` → hành động Sửa biến mất khỏi DOM
- [x] Màn Meeting tạo mới/sửa: render đủ, có trường Mục tiêu + tải tài liệu (tính năng tpe)
- [x] Màn "Lý do hủy cuộc họp" (mục menu mới): 3 dòng, 8 cột
- [x] Còn 12 lượt gắn cờ: 5 Vue warn **pre-existing** (`errors`/`hasCustomer`/`fields` — có y hệt ở CẢ 2 nhánh trước merge) + 7 ảnh avatar 404 trên máy local. Không có lỗi nào do merge.

### Checkpoint — 2026-09-14 (sau kiểm thử)
Vừa hoàn thành: test API + UI, vá 2 lỗi cú pháp do merge, commit `e743d75c1`.
Bước tiếp theo: chờ user duyệt rồi push cả 2 repo về `origin/gop_db`.
Blocked:
