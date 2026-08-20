# Design (tóm tắt) — cut-erp-sync

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-19-cut-erp-sync-design.md`
Feature tiền đề: `.plans/gop-db/employee-create-bank-null/` (bug lộ ra vấn đề này)

## Mục tiêu

Sau khi gộp DB, các khối "đồng bộ sang ERP" trong module Nhân sự đang **đọc/ghi chính bảng mà chúng
vừa ghi**, qua một connection thừa (`mysql2`). Vô nghĩa, tốn query, và có nguy cơ ghi đè nhầm.
Feature này cắt các khối đó.

## Hiện trạng đã kiểm chứng (không suy đoán)

| Kiểm tra | Kết quả |
| --- | --- |
| `master_settings.use_erp` | `1` (use_crm = 0, use_rice = 1) |
| `.env` `DB_DATABASE_SECOND` | `gop_db` — **cùng database** với `DB_DATABASE` |
| Model còn `setConnection('mysql2')` | **chỉ 2 file**: `Modules/Human/Entities/TpEmployeeInfo`, `app/Models/TpEmployeeInfo` (≈100 model `Tp*` khác đã dùng connection mặc định từ các đợt trước) |
| Cặp model cùng bảng | `Company`↔`TpCompany` (`companies`) · `Department`↔`TpDepartment` (`departments`) · `Part`↔`TpPart` (`parts`) · `Employee`↔`TpEmployee` (`employees`) · `EmployeeInfo`↔`TpEmployeeInfo` (`employee_infos`) |
| Cặp **khác** bảng | `Group` (`hrm_groups`) ↔ `TpGroup` (`department_groups`) → **đồng bộ thật, giữ nguyên** |
| `TpModuleMapping` (`module_mappings`) | không có nơi nào trong code **đọc** để tra cứu, chỉ ghi |

## Quyết định

**Gỡ** (đồng bộ ghi trùng chính bảng của mình):
- Khối `if ($useErp)` trong `boot()` của `Company`, `Department`, `Part`, `Employee`, `EmployeeInfo`
- Khối đồng bộ password/status sang `TpEmployee` trong `EmployeeService::updateEmployee`
- `setConnection('mysql2')` + constructor query `master_settings` của 2 model `TpEmployeeInfo`
- 4 lệnh `\Config::set("database.default", "mysql2")` trong `AuthController` (+ 2 lệnh khôi phục)
- `SyncEmployeeInfoToErpJob` / `SyncEmployeeToErpJob` → chuyển thành **no-op** (giữ class để job còn
  tồn trong hàng đợi không nổ; xoá hẳn ở bước sau)

**Giữ nguyên có chủ đích:**
- `Group` → `TpGroup`: khác bảng, là đồng bộ thật
- Nhánh `use_crm` (đang tắt) và các nhánh `use_erp` chỉ **đọc** dữ liệu ERP:
  `DailyJobService`, `CheckDueConfigsManager`, `CreateEmployeePayroll`, `MasterSettingService`

**Cứu được khi gỡ:** hook `EmployeeInfo::updated` đồng bộ `status`/`email` sang bảng `employees` +
ghi `EmployeeHistory` vốn bị đặt **nhầm** bên trong nhánh `use_erp` — đã tách ra ngoài, nay chạy
độc lập với cờ ERP.

## Bug tiềm ẩn phát hiện thêm (chưa sửa — chờ ý kiến)

- `Group::boot()`: `TpGroup::find($model->code)` tra theo **khoá chính** nhưng truyền vào **`code`**
  → gần như luôn không tìm thấy, mỗi lần lưu nhóm lại INSERT thêm 1 dòng `department_groups`.
- `EmployeeInfo` nhánh `use_rice`: `findRiceCompany()` trả null khi hồ sơ chưa có `company_id`
  → notice `Trying to get property 'id' of non-object` (dòng 143/158/161). Code có sẵn, không thuộc scope.
