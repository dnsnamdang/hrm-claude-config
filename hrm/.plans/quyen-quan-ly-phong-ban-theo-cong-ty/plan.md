# Plan — Quyền quản lý phòng ban theo từng công ty (#10761)

## Phase 1 — Lưu trữ & phân quyền theo dòng công ty

### BE

- [x] Migration thêm cột `all_department` (boolean, default 0) vào `employee_manage_departments`
- [x] `EmployeeManageDepartment`: thêm `all_department` vào `$fillable`
- [x] `PermissionHelper`: thêm helper dùng chung `employeeManagesAllDepartmentsIn`, `manageDepartmentIdsOf`, `managePartIdsOf`, `employeeIdsManagingDepartment`
- [x] `PermissionHelper::listManageDepartmentIds` / `listManagePartIds` gọi helper mới (cờ tổng chỉ áp dụng cho công ty của NV)
- [x] `EmployeeService::storeRole`: lưu dòng "tất cả phòng ban" theo công ty (department_id NULL)
- [x] `DetailResource`: trả `all_department` theo từng dòng công ty; lọc dòng NULL khỏi danh sách phòng ban
- [x] `buildPermissionSnapshot`: ghi lịch sử thay đổi cho cờ theo dòng
- [x] Đồng bộ các bản sao `listManageDepartmentIds`: PermissionService, TpEmployee, TimesheetService, CustomerService, MissionService, DepartmentManpowerService, AssignJobService, JobRequestService, AssignBusinessService, QuotationService, SubjectController, TrainingRequestController
- [x] Đồng bộ `TimesheetService::listManageEmployeeInfoIds`, `listManageDepartments`, `AssignBusinessService::listManageEmployeeInfoIds`
- [x] Đồng bộ chiều ngược (tìm người quản lý phòng ban): EmployeeInfoService x2, HandoverService, RequestSolutionController, NotifyRequestSolutionDeadlineCommand

### FE

- [x] Đổi text checkbox tổng thành "Quản lý tất cả phòng ban trong công ty của tôi"
- [x] Thêm checkbox "Quản lý tất cả phòng ban" trong ô Công ty của từng dòng bảng phân công
- [x] Tích → ẩn cột Phòng ban / Bộ phận của dòng đó, ẩn nút "Thêm phòng ban"
- [x] `submitSave`: gửi `all_department` theo từng dòng, bỏ qua departments khi tích
- [x] `EmployeePermissionHistoryModal`: hiển thị cờ theo dòng trong lịch sử thay đổi

### Phase 2 — Chạy & kiểm thử

- [x] Chạy migration trên `hrm_prod_local` (cột `all_department` đã có)
- [x] Bộ test BE 42 assert (helper, storeRole, DetailResource, lịch sử, 6 service khác) — 42 PASS / 0 FAIL
- [x] Test API end-to-end: POST lưu cờ theo dòng → DB đúng → GET detail trả đúng
- [x] Test UI Playwright: đổi text cờ tổng, tích/bỏ tích theo dòng, lưu, reload, lịch sử thay đổi
- [x] Smoke test 13 endpoint dùng helper phân quyền — không có 500
- [x] Sửa chữ hướng dẫn dòng "tất cả" từ `text-muted` (bị theme render màu đỏ) sang xám nghiêng
- [x] Thêm chặn lưu khi dòng phân công chưa chọn công ty (trước đây BE bỏ qua âm thầm)
- [x] Audit 22 tài khoản đang bật cờ tổng: 100% có `company_role` trùng công ty của NV → không ai mất quyền
- [x] Dọn sạch dữ liệu test (NV 1892/1893 về nguyên trạng)

### Checkpoint — 2026-08-05
Vừa hoàn thành: Phase 1 + Phase 2 (code, migration, test BE/API/UI đầy đủ)
Đang làm dở: (không)
Bước tiếp theo: chạy migration trên môi trường TPE/prod rồi báo QC test lại
Blocked:
