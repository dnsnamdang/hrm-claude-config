# GĐ3 — Các vấn đề tồn chờ user xem (ghi 30/10/2026)

Trạng thái nhánh `rbac` (3 repo `wt-rbac/*`):
- 8.1 → 8.17 đã push lên `origin/rbac` (hrm-api `91eabc900`, ERP `83f96d0c69`, client `1fedbf942`).
- **Commit local CHƯA push**: 8.18 (ERP `a51bdd3def`, client `68c18bbbc`); màn Vai trò (hrm-api `d9359428f`, client `449cbd4ec`).
- Chưa merge `gop_db`.

---

## A. Cần user quyết

### A1. 169 chỗ kiểm theo Vai trò nghiệp vụ chưa có mã (8.18)

File: `has-role-chua-co-ma.csv` (cùng thư mục, cột `xu_ly = chua_co_ma`). Mỗi dòng có mã ứng viên và số người bị ảnh hưởng trên rehearsal.

Đổi sang mã sẽ đổi người được phép trên dữ liệu thật, nên chưa đổi.

| Nhóm | Số chỗ | Ghi chú |
|---|---|---|
| TGĐ ⇒ xem mọi công ty | 49 | |
| isBigBoss (GĐ ‖ Ban GĐ) | 53 | |
| GĐ riêng | 18 | Gồm hrm-api `ContractService.php:1139` (duyệt HĐ dự án TKT vượt hạn mức). Chưa có mã cấp BGĐ ở HRM. Mã ứng viên `sale.hop_dong_ban_giam_doc.approve` chỉ khai cho ERP; 53 cặp NV×công ty giữ mã, so với 25 cặp giữ Vai trò GĐ ⇒ dùng mã này là mở rộng quyền |
| Trưởng phòng | 22 | Rehearsal 0 người có Vai trò tên đúng "Trưởng phòng" ⇒ các nhánh này hiện **luôn false** |
| CSKH | 6 | |
| Kế toán | 3 | |

Cách quyết: theo từng nhóm, hoặc để gộp vào Task 12.

### A2. Duyệt báo giá dự án (ERP `ProjectQuotation.php:1965-1967`)

Hiện cho qua nếu có mã HOẶC có Vai trò TGĐ/GĐ. Bỏ vế Vai trò ⇒ 17 cặp NV×công ty mất quyền duyệt. Phải cấp mã cho họ trước khi bỏ.

### A3. Ràng buộc "GĐ/TP được xoá liên hệ khách hàng"

- Vị trí: hrm-api `CustomerService.php:2504-2512`, ERP `Customer.php:509-511`.
- Mã KH không có phạm vi (đã chốt ở Step 4), nên không biểu diễn được 3 tầng.
- Đây là ràng buộc ghi, ngoài phạm vi GĐ3. Hai chỗ phải đổi cùng lúc.

### A4. Tên quyền lạ đang bị ép `false` (8.14 → 8.17)

Không ai qua được các chỗ này. User nói sẽ xem và quyết theo từng mã. Danh sách:
- WarrantyPayment "Xem tất cả phiếu chi của phòng ban/bộ phận" ×4.
- 31 tên ở purchase.
- 6 chỗ `can('Tên' && …)` ở purchase, vốn luôn false từ trước.
- Sale:
  - cờ DS tiêu chuẩn theo NV;
  - BH-SC-BD theo công ty;
  - 2 mục menu duyệt kế hoạch phòng ban;
  - "YC vận chuyển" ×10 (chỉ có alias api).
- 'Quản lý danh mục đính kèm' (ERP `routes/web.php:828`).
- Danh sách cũ hơn: checkpoint `plan.md` và `task-8.14..8.17-report.md` (sdd).

### A5. Push 8.18

ERP 1 commit + client 1 commit lên `origin/rbac` — chờ user cho phép.

---

## B. Lỗi có sẵn (không do GĐ3 gây ra) — nên sửa trước khi lên prod

- **Dashboard Đào tạo** (`hrm-client/pages/training/dashboard/index.vue:636-655`): ẩn khối quản lý với MỌI người, vì so `roles[].name` với tên gốc trong khi tên Vai trò đã có tiền tố công ty. Lỗi có từ GĐ1.
- **Golden ERP trôi DB**: test MasterData hrm-api ghi `companies#1.updated_at/updated_by` không trong transaction.
  - 8.17 đã né bằng `GoldenRows::stripVolatile`; gốc chưa sửa.
  - Chạy suite ERP và hrm-api song song trên cùng DB test ⇒ nhiều ca E. Phải chạy tuần tự.

---

## C. Dọn ở Task 11/12 (đã biết, chưa làm)

- Scanner bỏ sót `isRole(` (~190 chỗ ERP) ⇒ thêm vào `CallSiteScanner::ROLE_RE`.
- Comment "Super admin luôn xem giá vốn" ×5 ở BE hrm-api còn sai (code đã bỏ đặc quyền).
- File chết `topmenubar_old.blade.php`; middleware `checkRole` không route nào dùng ⇒ gỡ.
- Nhánh `elseif` cùng một mã (vô nghĩa) ở ERP:
  - `Customer.php:1339/1432/1524`;
  - `CustomerService.php:783-789`;
  - `ErpPermissionHelper.php:143-146`.
- `sale/tmp_product_requests/index.blade.php:59-61` gọi `permissionScope` 3 lần cho cùng mã.
- `routes/web.php` ERP đổi cả route đã comment (vô hại, chỉ làm diff nhiễu).
- Popup chọn người duyệt còn kiểm theo tên (~140 chỗ).
- Socket `server_node/server.js` vẫn đọc claim `permissions` theo tên cũ trong JWT ⇒ đổi sang mã khi bỏ claim cũ.

---

## D. Màn Phân quyền vai trò dựng lại theo mockup (29/10)

- File (đã commit 30/10, xem dưới): hrm-client `pages/admin/roles/{_id/permissions.vue, index.vue, components/PermissionTree.vue, PermissionSummaryList.vue, RolePermissionsViewModal.vue, RoleHoldersModal.vue}` + `utils/permissionTree.js` (thêm `summarizeGrants`); hrm-api `app/Services/Admin/RoleManagementService.php` + `tests/Feature/Rbac/AdminRoleApiTest.php` — nằm trong working tree `wt-rbac`.
- Đã kiểm bằng Playwright: tài khoản 13 (Super admin role 18) và tài khoản 24 (không quyền).
- Spec `HRM/e2e/tests/admin/admin-roles.spec.ts` đã cập nhật, CHƯA chạy.
- 30/10 sửa treo trình duyệt (đo bằng Playwright, cùng kịch bản trước/sau):
  - Ô tìm debounce 300ms: gõ `ca_lam_viec` rồi Backspace nhanh ⇒ ô trống sau 0,1s (trước 4,4s), không còn long task.
  - Tự mở thẻ chỉ khi kết quả nằm trong ≤ 3 phân hệ; bỏ lọc thì trả lại trạng thái mở trước đó. Gõ 1 ký tự giữ 1 thẻ mở (trước: mở cả 18).
  - Ô cấp chỉ dựng select2 khi bấm (ô nhẹ giống hệt, đo khớp kích thước/màu). "Mở tất cả" còn 0,97s (trước 2s); tick 1 ô lúc mở hết còn 0,17s (trước 1,9s).
- 30/10 bấm chip ở bảng "Quyền đã phân" ⇒ lọc danh sách bên dưới theo phân hệ (bấm lại = bỏ lọc).
- 30/10 danh sách vai trò:
  - Popup "Quyền đang có" làm lại theo mockup: lọc Phân hệ / Chức năng / Loại + ô tìm, chip đếm, thẻ phân hệ, nhãn loại + nhãn cấp. Dùng chung component `PermissionSummaryList.vue` với màn Phân quyền.
  - Bấm "Số người giữ" mở popup mới `RoleHoldersModal.vue` (API có sẵn `admin/employee-roles?role_ids[]=`).
- 30/10 BE hrm-api `RoleManagementService` (CHƯA commit):
  - `holders_count` chỉ đếm nhân viên còn tồn tại + thuộc công ty, khớp popup. Trước đây đếm cả 12 dòng gán mồ côi ⇒ 7/101 vai trò lệch, vd Super Admin 10 → 7.
  - Xoá vai trò: chặn nếu còn nhân viên tồn tại giữ (kể cả người ngoài công ty); chỉ còn dòng mồ côi thì cho xoá và dọn luôn các dòng đó.
  - +3 test; Rbac hrm-api 389 OK.
  - 12 dòng gán mồ côi ở các vai trò KHÔNG bị xoá thì vẫn nằm trong DB `employee_has_roles` (employee_id 1, 7, 11, 15, 16, 17, 19×2, 20, 21, 23, 654 trên rehearsal) — chờ user quyết có dọn hay không.
- 30/10 mã quyền mặc định ẩn ở màn Phân quyền và popup Quyền đang có; tick "Hiện mã quyền" để xem. Lựa chọn nhớ theo trình duyệt (localStorage `admin.roles.showPermissionCode`), dùng chung 2 nơi.
- 30/10 popup Người giữ đổi sang bảng dùng chung `V2BaseDataTable` (style MISA).
- 30/10 chạy e2e `admin-roles` trên 3011/8011 (DB rehearsal, API_REPO tạm trỏ SQL dọn về rehearsal): **13 passed**. Lúc chạy bắt thêm 3 lỗi, đã sửa:
  - "Chỉ hiện quyền đã chọn" không tự mở thẻ chứa quyền đã chọn.
  - Mở ô cấp qua ô nhẹ để focus rơi về body ⇒ Esc / phím mũi tên không ăn.
  - Tiêu đề thẻ "Cây quyền" bẻ dòng ở khổ 1280.
  - Bài học spec: `row.locator('a, b')` có dấu phẩy trần bị tách thành selector toàn trang — dùng `:is(a, b)`.
- **Đã commit local (chưa push)**: hrm-api `d9359428f`, hrm-client `449cbd4ec`.
- 30/10 (CHƯA commit):
  - Màn danh sách vai trò thêm 3 bộ lọc (chọn nhiều): Người sửa gần nhất (`updated_by[]`), Quyền (`permission_codes[]`), Người đang giữ (`holder_ids[]`). Danh mục lấy từ API mới `GET admin/roles/filter-options` (người sửa / 892 quyền / người đang giữ, 0,27s). +5 test BE; Rbac hrm-api 394 OK.
  - Màn Vai trò nhân viên (chi tiết): thẻ vai trò mặc định chỉ hiện vai trò đang cấp. Nút "Cấp thêm vai trò" ⇄ "Chỉ hiện vai trò đang cấp"; gõ tìm thì tìm trên toàn bộ; vai trò đã tick/bỏ tick giữ dòng tới khi lưu.
  - Lịch sử đổi tên vai trò: đã có sẵn (BE ghi + popup hiện, e2e "sửa tên; lịch sử ghi đủ" xanh) — không sửa code.
  - E2E: admin-roles 14/14, admin-employee-roles 16/16 (đã sửa spec theo hành vi mới).

---

## E. Checklist deploy (khi lên prod)

- Đồng bộ Catalog trước: `finance.*` / `purchase.*` / `sale.*` / `master_data.*` (kèm các phân hệ GĐ3 trước).
- `php artisan queue:restart`.
- Socket còn phụ thuộc claim tên quyền cũ trong JWT — không bỏ claim `permissions` trước khi đổi socket.
- Phát hành TPE_APP cùng đợt (Task 9).
