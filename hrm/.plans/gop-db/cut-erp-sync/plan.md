# Plan — cut-erp-sync

Người phụ trách: @khoipv · Nhánh: `gop_db` · Spec: `docs/superpowers/specs/gop-db/2026-08-19-cut-erp-sync-design.md`

## Phase 1 — Khảo sát (không đoán, kiểm chứng bằng DB + grep)

- [x] Đếm model còn `setConnection('mysql2')` → chỉ 2 file `TpEmployeeInfo`
- [x] Đối chiếu `$table` từng cặp `X` ↔ `TpX` + `SHOW TABLES LIKE 'hrm_%'` → xác định cặp cùng bảng / khác bảng
- [x] Đọc `master_settings`: `use_erp=1`, `use_crm=0`, `use_rice=1`
- [x] Grep `TpModuleMapping::` → không nơi nào đọc để tra cứu, chỉ ghi

## Phase 2 — Gỡ đồng bộ ghi trùng bảng

- [x] `Company.php`: gỡ khối `if ($useErp)` trong `boot()` (hook created/updated ghi `TpCompany` + `TpModuleMapping`)
- [x] `Department.php`: gỡ khối tương ứng
- [x] `Part.php`: gỡ khối tương ứng
- [x] `Employee.php`: gỡ khối tương ứng (dispatch `SyncEmployeeToErpJob` + `TpModuleMapping`)
- [x] `EmployeeInfo.php`: gỡ khối tương ứng **nhưng giữ lại** hook `updated` đồng bộ `status`/`email`
      sang bảng `employees` + ghi `EmployeeHistory` (nghiệp vụ HRM bị đặt nhầm trong nhánh `use_erp`)
- [x] `EmployeeService.php`: gỡ khối đồng bộ password/status sang `TpEmployee` + khối `if ($useErp)` rỗng
- [x] Gỡ 9 import không còn dùng ở 6 file trên

## Phase 3 — Cắt connection `mysql2` và các job chết

- [x] `Modules/Human/Entities/TpEmployeeInfo.php` + `app/Models/TpEmployeeInfo.php`: bỏ constructor
      `setConnection('mysql2')` (kèm query `master_settings` mỗi lần khởi tạo model)
- [x] `SyncEmployeeInfoToErpJob` + `SyncEmployeeToErpJob`: `handle()` thành no-op có log, giữ class
      cho job còn tồn trong hàng đợi
- [x] `AuthController`: gỡ 6 lệnh `\Config::set("database.default", ...)` (4 sang `mysql2`, 2 khôi phục)

## Phase 4 — Verify

- [x] `php -l` sạch trên toàn bộ 13 file sửa (gồm cả 3 file của feature `employee-create-bank-null`)
- [x] Smoke test 1 (tinker, transaction + rollback): `TpEmployeeInfo` connection = mặc định ·
      `TpEmployeeInfo::find()` đọc được bản ghi chưa commit · tạo `Company`/`Department`/`Part`/
      `Employee`/`EmployeeInfo` không lỗi · hook đồng bộ `status` sang `employees` vẫn chạy ·
      `auth()->attempt()` trả token sau khi bỏ `Config::set` → **PASS toàn bộ**
- [x] Smoke test 2 (tinker, gọi thẳng `syncEmployeeBankAccounts` qua Reflection): ghi đúng 5 cột
      `account_number/account_name/bank_name/bank_branch/bank_province` + tạo 1 dòng
      `employee_bank_accounts` → **PASS**
- [x] Kiểm tra DB sau test: 0 dòng rác ở `employee_infos`, `employees`, `companies`, `departments`,
      `parts`, `employee_bank_accounts`
- [x] **User test trình duyệt** — đây là phần rủi ro nhất, cần người thật:
      1. **Đăng nhập / đăng xuất / đổi mật khẩu** (đã gỡ `Config::set` trong `AuthController`)
      2. Tạo mới + sửa **nhân viên** (có tài khoản ngân hàng)
      3. Tạo mới + sửa **công ty**, **phòng ban**, **bộ phận**
      4. Đổi trạng thái hồ sơ nhân sự → kiểm tra tài khoản đăng nhập bị khoá theo + có dòng lịch sử
      5. Đổi mật khẩu nhân viên từ màn quản trị

### Checkpoint — 2026-08-19
Vừa hoàn thành: Phase 1-4 (trừ mục user test). Gỡ toàn bộ đồng bộ ERP ghi trùng bảng trong module
Nhân sự, cắt connection `mysql2` khỏi 2 model `TpEmployeeInfo`, vô hiệu 2 job sync, gỡ `Config::set`
khỏi `AuthController`. Diff: 13 file, -557/+105 dòng.
Đang làm dở: không.
Bước tiếp theo: user test 5 luồng ở Phase 4 trên trình duyệt.
Blocked: không.

## Còn nợ / cần user quyết

- [ ] Xoá hẳn 2 job `SyncEmployeeInfoToErpJob`, `SyncEmployeeToErpJob` sau khi hàng đợi sạch
- [ ] Nhánh `use_crm` (đang tắt) vẫn ghi `TpModuleMapping` ở 10 chỗ — dọn khi bật/bỏ hẳn CRM
- [ ] Bug `Group::boot()` — `TpGroup::find($model->code)` tra khoá chính bằng `code` → mỗi lần lưu
      nhóm có thể INSERT thêm dòng thừa vào `department_groups`. **Chưa sửa, chờ user xác nhận**
- [ ] Cân nhắc tắt hẳn cờ `use_erp` và gỡ nốt ~100 model `Tp*` còn lại (chúng chỉ là model trỏ bảng
      ERP, không còn dùng connection riêng nên **không** gây bug loại này)
