# Design: Command check:employee-status-diff

## Mục tiêu

Tạo Artisan command kiểm tra sự khác biệt trường `status` giữa 2 cặp bảng HRM ↔ ERP:

1. `employee_infos` (HRM) ↔ `employee_infos` trên mysql2 (ERP)
2. `employees` (HRM) ↔ `employees` trên mysql2 (ERP)

Command chỉ **đọc và báo cáo**, không thay đổi dữ liệu. Lấy HRM làm chuẩn.

## Command signature

```
php artisan check:employee-status-diff
```

Không có argument hay option.

## Logic xử lý

### Cặp 1: EmployeeInfo ↔ TpEmployeeInfo

- Query join `employee_infos` (default connection) với `employee_infos` (mysql2) theo `id`
- Điều kiện: `employee_infos.status != tp_employee_infos.status`
- Select: `id`, `code`, `fullname`, `status` từ cả 2 bảng

### Cặp 2: Employee ↔ TpEmployee

- Query join `employees` (default connection) với `employees` (mysql2) theo `id`
- Điều kiện: `employees.status != tp_employees.status`
- Select: `id`, `status` từ cả 2 bảng + lấy `code`, `fullname` từ `employee_infos` qua `employee_info_id`

## Output format

### Bảng 1: EmployeeInfo

```
=== So sánh EmployeeInfo ↔ TpEmployeeInfo ===
+----+--------+----------------+-------------+----------------+
| ID | Mã NV  | Họ tên         | Status HRM  | Status Tp      |
+----+--------+----------------+-------------+----------------+
| 5  | NV-001 | Nguyễn Văn A   | Đang làm(1) | Nghỉ việc(0)   |
| 12 | NV-008 | Trần Thị B     | Tạm nghỉ(3) | Đang làm(1)    |
+----+--------+----------------+-------------+----------------+
Tổng: 2 nhân sự khác status
```

### Bảng 2: Employee

```
=== So sánh Employee ↔ TpEmployee ===
+----+--------+----------------+-------------+----------------+
| ID | Mã NV  | Họ tên         | Status HRM  | Status Tp      |
+----+--------+----------------+-------------+----------------+
| 3  | NV-001 | Nguyễn Văn A   | Active(1)   | Inactive(0)    |
+----+--------+----------------+-------------+----------------+
Tổng: 1 nhân sự khác status
```

### Summary

```
=== Tổng kết ===
EmployeeInfo khác status: 2
Employee khác status: 1
```

Nếu không có khác biệt, in: `Không có nhân sự nào khác status.`

## Status mapping

**EmployeeInfo:**

| Giá trị | Tên        |
|---------|------------|
| 0       | Nghỉ việc  |
| 1       | Đang làm   |
| 2       | Ứng viên   |
| 3       | Tạm nghỉ   |

**Employee:**

| Giá trị | Tên      |
|---------|----------|
| 0       | Inactive |
| 1       | Active   |

## Vị trí file

- `app/Console/Commands/CheckEmployeeStatusDiff.php`

## Model & Connection

- `EmployeeInfo` → default connection, bảng `employee_infos`
- `TpEmployeeInfo` → mysql2 connection, bảng `employee_infos`
- `Employee` → default connection, bảng `employees`
- `TpEmployee` → mysql2 connection, bảng `employees`

Dùng model từ `Modules\Human\Entities\` cho cả 4.
