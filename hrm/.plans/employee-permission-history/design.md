# employee-permission-history — Tóm tắt

## Mục tiêu
Bổ sung "Lịch sử thay đổi" cho màn **Phân quyền người dùng** (`/timesheet/setting/employees` + màn Sửa `/employees/{id}`) — audit ai đổi quyền của user nào, cũ → mới, lúc nào.

## Bối cảnh kỹ thuật
- Màn lưu qua `POST timesheet/employees` → `EmployeeController::store` → `EmployeeService::storeRole()` (endpoint **chỉ màn này** dùng, có `auth:api`).
- `storeRole` ghi 3 nhóm cho 1 nhân viên: **roles** (xóa hết `employee_has_roles` rồi insert lại), **all_department** (cờ trên `company_employees`), **manager_departments** (bảng `employee_manage_departments`: company/department/part_ids).
- Không có action create/delete user ở đây (user đến từ đồng bộ) → chỉ action `update`.

## Quyết định (đã chốt với user)
1. Track **cả 3 nhóm** (roles + all_department + manager_departments).
2. Nút "Lịch sử thay đổi" ở **CẢ HAI**: màn Sửa (cạnh Lưu/Quay lại) + dropdown thao tác từng dòng danh sách.
3. **KHÔNG** permission riêng.
4. Biến thể **full-snapshot** (lưu snapshot đầy đủ 2 phía, FE tự diff added/removed) — vì roles + manager_departments là list.

## Thiết kế
- **DB**: bảng `employee_permission_history` (module Timesheet): `employee_id` (index), `action`, `old_value`/`new_value` (JSON `{all_department, roles:[tên], manager_departments:[{company, department, parts:[tên]}]}`), `changed_by`, `changed_at`, timestamps. KHÔNG company_id (scope theo employee_id).
- **BE**: `EmployeeService`:
  - `buildPermissionSnapshot($employeeId)` — đọc roles/all_department/manager_departments, resolve **TÊN** (company/department/part), sort ổn định để so sánh.
  - `storeRole()` chụp snapshot TRƯỚC mutation → sau mutation gọi `logPermissionHistory()` (so sánh JSON, khác mới ghi 1 dòng full-snapshot). `changed_by = auth()->id()` (route có auth:api).
  - `permissionHistories($employeeId)` sort cũ→mới, trả `changed_by_name` + giờ.
  - Controller `histories(Request)` đọc `employee_id`; route `GET timesheet/employees/histories` đặt **TRƯỚC** `/{id}`.
- **FE**: `components/setting/employee-permission/EmployeePermissionHistoryModal.vue` — `open(employeeId, name)`, tự diff: Quyền chip **+ xanh / − đỏ**, Quản lý tất cả phòng ban cũ→mới (Có/Không), Phân công phòng ban thêm(xanh)/bỏ(đỏ) "Công ty › Phòng ban — Bộ phận". Bộ lọc Người/ngày. Gắn vào cả 2 màn.

## Auth note
Auth model = `App\Models\TpEmployee`, id khớp Employee id → `user.info->fullname` (xem [[master-settings-notes]]).
