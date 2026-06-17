# Đồng bộ Phòng ban/Chức vụ kiêm nhiệm từ Quyết định bổ nhiệm sang Hồ sơ nhân sự

> Người phụ trách: @khoipv
> Loại: Feature nhỏ (1 phase) — sửa luồng sync quyết định bổ nhiệm → EmployeeInfo
> Ngày tạo: 2026-06-11

## 1. Mục tiêu

Khi duyệt một **quyết định bổ nhiệm** có tick **Kiêm nhiệm** (`decision_appoint_personnels.is_concurrently = 1`),
hệ thống phải **thêm 1 dòng** vào "Phòng ban/Chức vụ kiêm nhiệm" của hồ sơ nhân sự
(bảng `employee_concurrently_department_has_positions`), đồng thời **giữ nguyên** vị trí chính của nhân viên.

## 2. Hiện trạng (vấn đề)

- `is_concurrently` chỉ tồn tại ở bảng `decision_appoint_personnels`.
- `AppendixLaborContractService::autogenousAppendixLaborContract()` (dòng 739-902) **không** copy `is_concurrently`
  sang phụ lục `appendix_labor_contracts`.
- `AppendixLaborContractService::updateEmployeeInfo()` (dòng 567-613) **luôn ghi đè** `department_id`, `part_id`,
  `employee_work_position_id`, `employee_role_id`, `direct_manager_*` của `EmployeeInfo` bằng các giá trị `new_*`
  — **không phân biệt** bổ nhiệm thường hay kiêm nhiệm, và **chưa bao giờ** ghi vào bảng kiêm nhiệm.

→ Bổ nhiệm kiêm nhiệm hiện đang bị xử lý sai: ghi đè vị trí chính thay vì thêm dòng kiêm nhiệm.

## 3. Quyết định thiết kế (đã chốt với user)

| # | Nội dung | Quyết định |
|---|----------|-----------|
| 1 | Khi kiêm nhiệm, có ghi đè phòng ban/bộ phận chính không? | **KHÔNG.** Giữ nguyên vị trí chính, chỉ THÊM dòng kiêm nhiệm. |
| 2 | Cách `updateEmployeeInfo` biết được "kiêm nhiệm"? | **Phương án A** — thêm cột `is_concurrently` vào `appendix_labor_contracts`. |
| 3 | Bộ phận (part) kiêm nhiệm — bảng kiêm nhiệm thiếu cột `part_id` | **Bỏ.** Không lưu part kiêm nhiệm; không thêm cột. |
| 4 | Duyệt lại / sync nhiều lần | **Chống trùng** theo `(employee_info_id, department_id, working_position_id)`. |

## 4. Phạm vi thay đổi (Backend — Modules/Decision)

### 4.1. Migration
- Thêm cột `is_concurrently` (boolean, default `0`) vào bảng `appendix_labor_contracts`.
- PHPDoc trên `up()` / `down()` theo file mẫu project.

### 4.2. `autogenousAppendixLaborContract()` (AppendixLaborContractService.php)
- Trong mảng `updateOrCreate(...)`, thêm:
  ```php
  'is_concurrently' => $relationDecision->is_concurrently ?? 0,
  ```
  (Với quyết định điều chuyển / điều chỉnh lương — `$relationDecision` không có field này → `?? 0`.)
- Đảm bảo `is_concurrently` nằm trong `$fillable` của entity `AppendixLaborContract`.

### 4.3. `updateEmployeeInfo($appendixLaborContract, $employeeInfo)` (AppendixLaborContractService.php:567)
Rẽ nhánh theo `$appendixLaborContract->is_concurrently`:

- **Kiêm nhiệm (`= 1`)** → KHÔNG ghi đè các field chính. Thay vào:
  - `firstOrCreate` 1 dòng `EmployeeConcurrentlyDepartmentPosition` theo khóa chống trùng
    `['employee_info_id' => ..., 'department_id' => new_department_id, 'working_position_id' => new_working_position_id]`,
    set thêm `title_id = new_title_id`, `title = Title::find(new_title_id)?->name`.
  - Nếu là dòng **mới tạo** (chưa tồn tại) → ghi lịch sử section `"Phòng ban/ Chức vụ kiêm nhiệm"`
    qua `saveEmployeeChangeHistory($oldData=[], $newData, $employeeInfoId, 'Thông tin nhân sự', 'Phòng ban/ Chức vụ kiêm nhiệm', true, ['title_id', 'position_order_index'])`
    — đúng pattern hàm `EmployeeInfoService::syncEmployeeConcurrentlyDepartmentHasPosition()`.
  - Nếu đã tồn tại → bỏ qua (không ghi history trùng).

- **Không kiêm nhiệm (`= 0` / null)** → giữ nguyên logic hiện tại (ghi đè vị trí chính + history "Thông tin cơ bản").

## 5. Mapping dữ liệu (kiêm nhiệm)

| Cột bảng kiêm nhiệm | Nguồn từ phụ lục / quyết định |
|---------------------|-------------------------------|
| `employee_info_id`  | `EmployeeInfo` của nhân viên được bổ nhiệm |
| `department_id`     | `new_department_id` |
| `working_position_id` | `new_working_position_id` |
| `title_id`          | `new_title_id` |
| `title`             | `Title::find(new_title_id)?->name` |
| ~~part_id~~         | **bỏ** (bảng không có cột) |

## 6. Ngoài phạm vi (giữ nguyên hành vi hiện tại)

- **Lương & "Phụ cấp kiêm nhiệm" (PC_KN):** `storeEmployeeSalaryHistory()` vẫn chạy như cũ. Không đụng.
- **Hủy duyệt quyết định kiêm nhiệm:** Hiện không revert vị trí chính → cũng **không** tự động xóa dòng kiêm nhiệm
  (giữ nhất quán hành vi cũ).
- **Bộ phận (part) kiêm nhiệm:** không lưu (xem QĐ #3).
- **Quyết định bổ nhiệm hiệu lực tương lai:** sync chỉ chạy khi `effective_date <= hôm nay` (logic sẵn có,
  dòng 897). Không mở rộng cron trong feature này.

## 7. File dự kiến chạm

- `hrm-api/database/migrations/xxxx_add_is_concurrently_to_appendix_labor_contracts_table.php` (mới)
- `hrm-api/Modules/Decision/Entities/.../AppendixLaborContract.php` (thêm fillable)
- `hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php` (2 hàm)

→ Không chạm Frontend. Không chạm permission/seeder.
