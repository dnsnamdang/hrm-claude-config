# Task 9 (bullet 1) report - e2e specs GĐ2b (chưa chạy)

Status: DONE_WITH_CONCERNS (chỉ viết + biên dịch; KHÔNG chạy test, không commit)

## Files (HRM/e2e/tests/admin/)
- admin-accounts.spec.ts (9 ca, serial): list = API total + 10 cột + filter; tìm nhanh; thêm (Lưu trống 4 lỗi/422, chọn hồ sơ tự điền email, lưu); sửa (unsaved guard, đổi email); khoá/mở khoá/lịch sử; API 422/404; redirect /human/employee (+:id, /add); ca "chỉ xem" (skip nếu thiếu ACCOUNTS_VIEWONLY_TOKEN); không quyền (API 403, 3 trang -> /pages/extras/404, menu không link).
- admin-employee-roles.spec.ts (12 ca, serial): list + cột + tiêu đề công ty; lọc (main+concurrent=total) + tìm nhanh; chip + bấm chip; chip "+n" (skip nếu không có NV >3 vai trò); popup Quyền đang được cấp (tab, "trùng", đỏ rgb(220, 38, 38), không đỏ ở dòng thường, table-wrapper max-height none, tab phòng ban); chi tiết 2:1 + footer không đè + checkbox theo API; tick vai trò thử + Lưu + PUT có company_ids + khôi phục; lịch sử; kiêm nhiệm: PUT không có khóa company_ids (route.fulfill, không ghi DB; skip nếu không có NV kiêm nhiệm); bulk popup chỉ danh mục công ty C (so bulk/options + SQL company_id/status, không bấm Áp dụng); redirect /timesheet/setting/employees (+:id); API 404/422; không quyền (API 403 x4, trang -> 404, DB không đổi).
- gd2b-fixture.ts (helper mới, không phải spec): sql/esc, insertProfile (INSERT employee_infos mã E2EZZ…), createAccountViaApi, workingCompany (từ bulk/options), cleanupAccounts, cleanupRoles. Không sửa file nào ngoài tests/admin/.

## Kiểm biên dịch
`npx playwright test tests/admin/admin-accounts.spec.ts tests/admin/admin-employee-roles.spec.ts --list` => 21 ca của 2 spec (+3 setup) liệt kê, "Total: 25 tests in 5 files", không lỗi.
`npx tsc --noEmit -p .` KHÔNG chạy được: e2e/ không cài typescript (npx in banner "not the tsc command"). Playwright --list đã transpile cả 2 spec + fixture bằng babel (không kiểm kiểu).

## Giả định về fixture/tài khoản
- TEST_EMAIL/TEST_PASSWORD có cả "Quản lý tài khoản nhân viên" và "Quản lý phân quyền" ở công ty đang làm (namdangit id 13).
- Ca không quyền: ACCOUNTS_NOPERM_TOKEN / EMPLOYEE_ROLES_NOPERM_TOKEN / ROLES_NOPERM_TOKEN (JWT) hoặc đăng nhập NO_1652_EMAIL (không có trên rehearsal -> phải truyền token, như admin-roles.spec).
- Chạy cho worktree: BASE_URL=http://127.0.0.1:3011 API_BASE=http://127.0.0.1:8011 API_REPO=<wt-rbac>/hrm-api; --workers=1.
- INSERT employee_infos dùng cột code, fullname, email, company_id, department_id, ssn, status, created_at, updated_at (theo Task 5); nếu DB có cột NOT NULL khác thì beforeAll lỗi.
- Tạo tài khoản qua API tự sinh company_employees ở công ty chính (đúng như Task 5) -> NV thử xuất hiện ở Màn 2.
- Tên vai trò thử `E2E Zz Vai trò NV …`, hồ sơ `E2EZZ…`, email `e2e-zz-…@test.local`; afterAll dọn (employees + bảng con, employee_infos, roles + role_has_permissions + history).

## Concerns
1. Selector chưa chạy thật, dựa trên đọc code client: span[title=...] của V2BaseRowActions, `.er-role-check label`, `.gp-dup-bar`, `.gp-table .table-wrapper`, `#admin-employee-granted-permissions`, `#bulk-permission-modal`, pickSelect2 theo placeholder; có thể cần chỉnh khi chạy lần đầu.
2. Cấu hình cột lưu theo user (columnCustomization) có thể làm ca "10 cột mặc định" lệch nếu tài khoản test đã tuỳ chỉnh.
3. Spec Màn 2 phụ thuộc có sẵn >=1 vai trò hoạt động có quyền ở công ty C để sao chép (tạo quyền trùng).
4. Ca "chỉ xem" và "+n"/"kiêm nhiệm" tự skip khi thiếu token/dữ liệu.
5. Đã đối chiếu: redirect /timesheet/setting/employees(/ :id) có trong hrm-client wt-rbac (Task 6).
