# Plan — Tối ưu API user-profile

## Phase 1 — Cắt payload tại nguồn (không đổi hợp đồng FE)

### BE — `app/Http/Controllers/Api/AuthNewController.php::userProfile()`
- [x] Grep `TPE_APP` + `TanPhatDev` + `elearning` xem client nào đọc `employee.permissions`
- [x] Bỏ `$mergedAttributes['permissions']` (trùng với `permissions` top-level) — giảm **202.131 B**
- [x] `departments`: đổi sang `parentDepartment:id,name` + `departmentLead:id,code,fullname`, bỏ quan hệ lồng `.employee` — giảm **266.133 B**
- [x] `departments`: đối chiếu 67 dòng, 0 lệch ở `parent_department.{id,name}` và `department_lead.{id,code,fullname}`
- [x] `employees`: **KHÔNG lọc cột** — rà 43 file thấy FE đang dùng `department_name`, `part_name`, `email`, `personal_telephone`, `working_position_name`; chỉ đổi `load('info')` → `load('info:id,fullname,code,department_id')` (JSON không đổi 1 byte, 59 ms → 40 ms)
- [x] `companies` / `groups`: giữ nguyên — đã nhỏ (23,8 KB / 2,9 KB), không đáng đổi
- [x] `permissions`: `select('permissions.id','permissions.name')` thay `permissions.*` — bỏ 8 cột không client nào đọc (`guard_name`, `created_at`, `updated_at`, `display_name`, `group`, `group_category`, `type`, `sort_order`), giảm **159.349 B**
- [x] `departments`: `makeHidden()` 22 cột cấu hình lương thưởng/hiển thị — đã quét toàn bộ hrm-client + TPE_APP, 0 nơi đọc; giảm thêm **74 KB** (68 → 46 cột)
- [x] Đo lại: **1.336.257 → 867.993 B (−35%)**, 353 → 305 ms, 38 → 34 query; 14/16 khối giống hệt từng byte

### FE — `hrm-client`
- [x] Rà mọi nơi đọc 2 quan hệ: chỉ 1 file (`pages/decision/department-change/components/FormComponent.vue:469-483`), dùng đúng `parent_department.{id,name}` + `department_lead.{fullname,code}` → còn đủ
- [x] Xác nhận FE **không** đọc `res.data.employee` (khối vừa thu gọn) — `store/actions.js` chỉ commit `employee_data` / `employee_info`
- [x] App TPE_APP (đối chiếu từng JsonKey với response thật, xem design.md): `departments` đọc qua `ApiValueData` (id/name/code) nên không chạm 2 quan hệ; `permissions` đọc từ top-level (`user_api_service_profile_ext.dart:12`); domain `EmployeeInfo.permissions` có `@Default([])` nên null cũng an toàn
- [x] Thử trên trình duyệt LOCAL (client :3002 → API :8003, nhánh gop_db): đăng nhập OK, 0 lỗi console
- [x] Store đủ dữ liệu: permissions 698, departments 68, employees 555, list_employee_infos 555, và toàn bộ options dẫn xuất (employeeOptions, activeCompanyEmployeeOptions, allEmployeesData…)
- [x] Màn Quyết định điều chuyển phòng ban: 45/68 phòng có `parent_department`, 48/68 có `department_lead`; nhãn ra đúng `Nguyễn Đức Long - HN_KD2 - NV.00035`; các cột form dùng (`objective`, `task`, `telephone`, `title_id`, `position`, `department_assistants`, `department_lead_id`) còn đủ
- [x] `CreateTaskModal.peopleOptions`: 555/555 có name, code, dept, email; 533 có phone (22 người vốn không có SĐT)
- [x] `SalesTeamSection`: 555 có dept/email, 533 phone, 168 part (đúng số người thuộc bộ phận)
- [x] **So menu bản gốc vs bản mới trên cùng máy: 40 = 40 mục, 698 = 698 quyền** → phân quyền không đổi
- [x] Màn /assign/tasks và /assign/prospective-projects render bình thường (10 dòng dữ liệu, 0 lỗi)

### Checkpoint Phase 1 — 22/09/2026
Vừa hoàn thành: 3 thay đổi BE, đã đối chiếu output cũ/mới trên dữ liệu thật (script `/tmp/verify2.php`
trên server, dựng cả 2 phiên bản hàm từ chính source rồi so từng khoá).
Kết quả cuối: **1.336.257 → 633.250 B (−53%)** trên server, **1.579.984 → 748.196 B (−53%)** trên
local; 34 query (−4); 13/16 khối giống hệt từng byte, 3 khối đổi đúng thiết kế
(`employee` −202.131 B, `departments` −341.527 B, `permissions` −159.349 B).
Đối chiếu nội dung: departments 67 dòng **0 giá trị lệch**, permissions **628 quyền, tập id giống
hệt, 0 tên lệch**. Kèm theo: gỡ được việc lộ 121 cột hồ sơ cá nhân (số CCCD của 47 trưởng phòng, mã số thuế,
ngày sinh) cho mọi user đăng nhập.
Đã test xong trên LOCAL (client :3002 + API :8003) — xem phần FE ở trên.
Đang làm dở: chưa commit, chưa deploy lên `/var/www/hrm_crm`.
Bước tiếp theo: chờ user duyệt để commit + deploy dev CRM.
Blocked: không

## Phase 2 — Cache phía server

### BE
- [ ] Tách khối danh mục dùng chung (`departments`, `parts`, `companies`, `groups`, `employees`, `list_employee_infos`) ra `CommonCatalogService`
- [ ] Cache theo khoá `catalog:{company_id}:{version}`, TTL 1 giờ (`CACHE_DRIVER=file` sẵn có, không cần Redis)
- [ ] Bump version khi sửa phòng ban / bộ phận / nhân sự / công ty / nhóm — gắn vào `saved`/`deleted` của các Model tương ứng
- [ ] Giữ phần theo người dùng (`employee`, `permissions`, `notifications`) **không cache**

### Checkpoint Phase 2
- [ ] Đích: thời gian < 0,25 s khi cache nóng; kiểm dữ liệu mới hiện ngay sau khi sửa danh mục

## Phase 3 — ETag / 304 + cache trình duyệt

### BE
- [ ] Sinh `ETag` từ version cache + id người dùng; trả `304 Not Modified` khi `If-None-Match` khớp

### FE — `store/actions.js`
- [ ] Lưu payload vào `localStorage` kèm ETag; gửi `If-None-Match`, gặp 304 thì dựng store từ bản lưu
- [ ] Xoá bản lưu khi đăng xuất và khi đổi công ty (`current_company`)

### Checkpoint Phase 3
- [ ] Đích: F5 lần 2 trở đi gần như không tốn CPU server (304, vài KB)

## Phase 4 — Nghiệm thu
- [ ] Đo lại 1 / 3 / 10 request đồng thời, so với baseline 22/09/2026 (2,4 s cho 10 request)
- [ ] Kiểm `us%` khi tải — mục tiêu không còn chạm 90%
- [ ] Port sang nhánh `tpe-develop-assign` nếu kết quả đạt
