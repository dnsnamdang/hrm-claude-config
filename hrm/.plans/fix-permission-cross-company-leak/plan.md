# Fix: Lộ hồ sơ chéo công ty do `orWhere created_by` trong helper phân quyền

Người phụ trách: @khoipv

## Bối cảnh

Màn `human/employee_info`, đứng ở công ty ETEK tập đoàn (id 8) với quyền "Xem hồ sơ nhân sự theo công ty" nhưng vẫn thấy nhân sự của Tân Phát (id 1).

**Nguyên nhân gốc:** các helper trong `hrm-api/app/Helper/PermissionHelper.php`, ở nhánh quyền cấp **công ty**, có vế `->orWhere($table.'.created_by', auth()->user()->id)` — mọi bản ghi do user đang đăng nhập tạo đều hiện ra bất kể công ty. Tài khoản DNS Admin (id 13) là người tạo 243 hồ sơ active của Tân Phát → lộ sang khi xem ở ETEK.

**Hướng fix (đã duyệt — cách 1):** sửa trực tiếp helper chung — bỏ vế `orWhere created_by` ở nhánh quyền cấp công ty (tương đương "created_by kèm điều kiện cùng công ty"). KHÔNG sửa nhánh phòng ban/bộ phận vì nhiều bảng dùng helper không có cột `company_id` (contracts, tasks, suppliers...) — thêm tham chiếu `company_id` sẽ vỡ SQL màn khác.

## Tasks

- [x] Sửa `checkPermissionList` — nhánh quyền công ty (permissions[1]): bỏ `orWhere created_by`
- [x] Sửa `checkPermissionListWithCompanyFilter` — nhánh quyền công ty (permissions[1]): bỏ `orWhere created_by`
- [x] Sửa `checkPermissionListNotAllCompany` — nhánh quyền công ty (permissions[0]): bỏ `orWhere created_by`
- [x] Sửa `checkPermissionListWithColumn` — nhánh quyền công ty (permissions[1]): bỏ `orWhere created_by`, GIỮ `orWhere $column` (quyền xem bản ghi gắn với chính mình)
- [x] `php -l` kiểm tra syntax — pass
- [x] Verify bằng script bootstrap Laravel: user 1060 (chỉ role 26 "theo công ty") tại công ty 8 → chỉ thấy 23 hồ sơ company_id=8, không còn công ty khác

## Phát hiện thêm trong lúc verify (nguyên nhân thứ 2 của triệu chứng)

Tài khoản DNS Admin (employee 13) mang role **Super admin (18)** — tại công ty 8, role 18 và Admin_TPE (19) có sẵn cả 4 quyền gồm "Xem hồ sơ nhân sự theo **tổng công ty**" → nhánh không lọc, thấy hết mọi công ty. Đây là **dữ liệu phân quyền**, không phải code. Muốn tài khoản admin không thấy hết tại ETEK thì gỡ quyền "theo tổng công ty" của role 18/19 tại company 8 trên màn phân quyền.

Lưu ý kiến trúc: `isCurrentEmployeeHasPermission` lấy role theo `employee_has_roles` KHÔNG lọc theo cột `company_id` của pivot (role gán ở công ty 1 vẫn có hiệu lực khi đứng ở công ty 8, miễn role đó có dòng `role_has_permissions` tại công ty 8). Chưa sửa — cần quyết định của team.

Bug có sẵn (chưa sửa): `checkPermissionListWithCompanyFilter` nhánh bộ phận dùng nhầm `$query` thay vì `$q` trong closure (`PermissionHelper.php:~281`) → fatal "Undefined variable $query" nếu nhánh này chạy.

### Checkpoint — 2026-08-06
Vừa hoàn thành: fix `orWhere created_by` nhánh quyền công ty ở 4 helper + verify bằng script với user 1060.
Đang làm dở: không.
Bước tiếp theo: user quyết định có gỡ quyền "theo tổng công ty" của role 18/19 tại company 8 không; cân nhắc fix bug `$query`/`$q` và việc lọc role theo company pivot.
Blocked: (trống)

## Cập nhật lần 2 — gỡ quyền tổng công ty tại company 8 (đã làm, theo yêu cầu user)

User vẫn thấy nhân sự công ty khác vì test bằng tài khoản 787 (Trịnh Thị Lợi — Admin_TPE) / 1103 (Lê Thị Vân Anh — Super admin): 2 role này tại company 8 có quyền "theo tổng công ty".

- [x] DELETE 4 dòng `role_has_permissions` tại `company_id = 8`: role 18, 19 × permission 872 ("Xem hồ sơ nhân sự theo tổng công ty"), 883 ("Xem danh sách nhân viên nghỉ việc theo tổng công ty"). Khôi phục: tick lại trên màn phân quyền (hoặc INSERT lại 4 dòng trên).
- [x] Verify: user 787 và 1103 tại company 8 → chỉ còn 23 hồ sơ company 8, Nguyệt/Chiến không còn xuất hiện.

## Cập nhật lần 3 — công ty 4 (Tân Phát Sài Gòn) + phát hiện lý do UI lưu không ăn

User báo đã bỏ tick "tổng công ty" trên UI phân quyền (`timesheet/setting/roles/add/18`, tab Sài Gòn) nhưng DB vẫn còn → điều tra:

- Role 18 chưa từng có lần lưu thành công nào gần đây (`roles.updated_at` = 22/06, `role_permission_history` không có dòng nào của role 18) → thao tác lưu trên UI chưa bao giờ persist.
- Phát hiện **972 dòng mồ côi** trong `role_has_permissions` (permission_id không còn trong bảng `permissions`; riêng role 18: 324 dòng). Payload chứa id mồ côi sẽ làm `syncPermissionsByCompany` crash duplicate PK (đã tái hiện). FE bình thường không gửi id mồ côi (Resource join với permissions), nhưng đây là mìn tiềm ẩn — nên dọn.
- [x] Gỡ 872/883 khỏi role 18 @ công ty 4 bằng chính `RoleService::save()` với payload chuẩn như FE (có ghi `role_permission_history` id=2, changed_by=13).
- [x] Verify: DNS Admin đứng ở công ty 4 → 'tổng công ty' false, danh sách chỉ còn 215 hồ sơ company 4, Nguyệt biến mất.

Tồn đọng mới:
- Role 18 vẫn còn "tổng công ty" (872/883) tại công ty 1 (HQ), 2 (CN Hải Phòng), 3 (CN Vinh) → đứng ở các công ty đó admin vẫn thấy toàn tập đoàn. Chờ user quyết có gỡ tiếp không.
- Dọn 972 dòng mồ côi `role_has_permissions` (orphan permission_id).
- Điều tra vì sao thao tác lưu trên UI của user không persist (khả năng: request lỗi thầm lặng — controller catch Exception trả 500 nhưng FE không có .catch → không toast, không log).

### Checkpoint — 2026-08-06 (lần 2)
Vừa hoàn thành: gỡ quyền tổng công ty (hồ sơ + nghỉ việc) của role 18/19 tại company 8, verify sạch bằng cả 2 tài khoản user test.
Đang làm dở: không.
Bước tiếp theo: (tồn đọng) bug `$query`/`$q` dòng ~281 PermissionHelper; cân nhắc lọc role theo `employee_has_roles.company_id`; nhánh phòng ban/bộ phận vẫn còn `orWhere created_by`.
Blocked: (trống)

## Ghi chú tồn đọng (chưa fix trong đợt này)

- Nhánh quyền **phòng ban/bộ phận** (permissions[2]/[3]) vẫn còn `orWhere created_by` không giới hạn công ty → cùng loại leak nếu user có quyền cấp phòng ban. Chưa sửa được an toàn vì không phải bảng nào cũng có `company_id`.
- Nhánh fallback cá nhân (`created_by = user`, permissions[4]) cũng hiện bản ghi chéo công ty do mình tạo — hành vi "cá nhân" chủ đích, giữ nguyên.
