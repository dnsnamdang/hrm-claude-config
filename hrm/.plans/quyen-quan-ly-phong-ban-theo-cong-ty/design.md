# Quyền quản lý phòng ban theo từng công ty — Redmine #10761

**Người phụ trách:** @cuong61n
**Nhánh:** `tpe-develop-assign` (cả `hrm-api` + `hrm-client`)
**Màn:** `/timesheet/setting/employees/[id]` — Phân quyền người dùng

## Vấn đề

Checkbox "Quản lý tất cả phòng ban" khi tích sẽ ẩn toàn bộ bảng phân Công ty / Phòng ban / Bộ phận.
PM hiểu cờ này là "quản lý tất cả phòng ban trong công ty của chính nhân viên đó", nên khi tích thì
không còn cách nào phân nhanh quyền cho **các công ty khác**.

## Quyết định

1. Đổi text checkbox tổng → **"Quản lý tất cả phòng ban trong công ty của tôi"**, và siết ngữ nghĩa:
   cờ chỉ có tác dụng trong công ty của chính nhân viên (`employee_infos.company_id`), không lan sang
   công ty đang chọn (`current_company_role`).
2. Thêm **checkbox "Quản lý tất cả phòng ban" theo từng dòng công ty** trong bảng phân công. Tích →
   dòng đó ăn toàn bộ phòng ban **và toàn bộ bộ phận** của công ty đó, ẩn 2 cột Phòng ban / Bộ phận.
3. Lưu trữ: thêm cột `all_department` (boolean, default 0) vào bảng `employee_manage_departments`.
   Dòng "tất cả" = 1 bản ghi `company_id = X, department_id = NULL, part_ids = NULL, all_department = 1`.
4. Rà soát toàn bộ điểm đọc quyền theo phòng ban/bộ phận để hợp nhất 2 nguồn (cờ tổng + cờ theo dòng).

## Phạm vi ảnh hưởng (BE)

Các hàm trùng lặp cùng logic nằm rải rác, đều phải hiểu cờ mới:

- `app/Helper/PermissionHelper.php` — `listManageDepartmentIds`, `listManagePartIds` (helper gốc)
- `app/CommonServices/PermissionService.php`, `app/Models/TpEmployee.php`
- `Modules/Timesheet/Services/TimesheetService.php` — `listManageEmployeeInfoIds`, `listManageDepartmentIds`, `listManageDepartments`
- `Modules/Human/Services/` — CustomerService, MissionService, DepartmentManpowerService
- `Modules/Assign/Services/` — AssignJobService, JobRequestService, AssignBusinessService, QuotationService
- `Modules/Training/` — SubjectController, TrainingRequestController
- Chiều ngược (tìm người quản lý 1 phòng ban để gửi thông báo/duyệt):
  `EmployeeInfoService::listEmployeeInfoHasPermission`, `listEmployeeInfoByPermissionAndDepartment`,
  `HandoverService::sendNotificationToApprovers`, `RequestSolutionController`,
  `NotifyRequestSolutionDeadlineCommand`

Cách làm: viết helper dùng chung trong `PermissionHelper.php`, các bản sao gọi lại helper thay vì
tự query — giữ nguyên hành vi cũ, chỉ cộng thêm nguồn dữ liệu mới.

## Rủi ro

- Người đang tích cờ tổng và dựa vào nó để xem dữ liệu **công ty khác** sẽ mất quyền sau khi deploy →
  phải phân lại bằng bảng (tích "tất cả phòng ban" ở dòng công ty tương ứng). Đây là siết quyền có chủ đích.
- Dòng `department_id = NULL` phải được loại khỏi mọi chỗ `pluck('department_id')` cũ để không sinh
  `whereIn([null])`.
