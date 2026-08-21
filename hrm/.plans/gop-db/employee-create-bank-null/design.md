# Design (tóm tắt) — employee-create-bank-null

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-19-employee-create-bank-null-design.md`

## Bug

Tạo mới nhân viên có nhập **Tài khoản ngân hàng** → API `POST /employee-infos` trả 500, transaction rollback,
nhân viên không được tạo.

```
ErrorException: Creating default object from empty value
  Modules/Human/Services/EmployeeInfoService.php:1317
  ← syncEmployeeBankAccounts()  (dòng 760, createEmployeeInfo)
  ← EmployeeInfoController::store() dòng 187
```

## Nguyên nhân gốc

`TpEmployeeInfo` (constructor `setConnection('mysql2')` khi `master_settings.use_erp = 1`) là **PDO connection
riêng**, dù sau khi gộp DB thì `DB_DATABASE_SECOND` đã trỏ **cùng database** với `mysql`.

`EmployeeInfoController::store()` mở `DB::beginTransaction()` trên connection `mysql`. Ở luồng **tạo mới**,
dòng `employee_infos` vừa INSERT **chưa COMMIT** → connection `mysql2` (isolation REPEATABLE READ) **không đọc
được** → `TpEmployeeInfo::find($id)` trả `null` → gán property lên `null` → warning PHP 7.4 → `ErrorException`.

Khớp triệu chứng: **ca sửa không lỗi** (bản ghi đã commit từ trước), **ca tạo mới luôn lỗi**.

Đã kiểm chứng bằng tinker (transaction + rollback): insert `employee_infos` → `TpEmployeeInfo::find()` = NULL,
`DB::table('employee_infos')->find()` = FOUND.

## Quyết định

- Ghi thông tin ngân hàng chính bằng **query builder trên connection mặc định** thay cho `TpEmployeeInfo`:
  nằm trong transaction, và **không** trigger lại hook `saved`/`updated` của `EmployeeInfo`
  (hook này dispatch `SyncEmployeeInfoToErpJob` → dễ lặp vòng).
- Sau khi gộp DB, `TpEmployeeInfo` và `EmployeeInfo` là **cùng bảng `employee_infos`** (không tồn tại
  `hrm_employee_infos`) nên đổi connection **không đổi dữ liệu đích**.
- Quét thêm các chỗ `TpEmployeeInfo::find()` không guard null → guard tối thiểu.
- **KHÔNG** đụng tới `use_erp` / gỡ các model `Tp*` / `SyncEmployeeInfoToErpJob` trong feature này
  (user chốt: chỉ làm hạng mục 1). Đây là nợ kỹ thuật còn để lại — xem mục "Còn nợ" ở plan.md.
