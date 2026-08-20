# Plan — employee-create-bank-null

Người phụ trách: @khoipv · Nhánh: `gop_db` · Spec: `docs/superpowers/specs/gop-db/2026-08-19-employee-create-bank-null-design.md`

## Phase 1 — BE: fix lỗi 500 khi tạo nhân viên có tài khoản ngân hàng

- [x] Xác định nguyên nhân gốc: `TpEmployeeInfo` dùng connection `mysql2` (PDO riêng) → nằm ngoài
      transaction của `EmployeeInfoController::store()` → không đọc được dòng `employee_infos` chưa commit
- [x] Kiểm chứng bằng tinker (beginTransaction → insert → find qua 2 connection → rollback)
- [x] `EmployeeInfoService.php` `syncEmployeeBankAccounts()`: thay khối `TpEmployeeInfo::find()->save()`
      bằng `DB::table('employee_infos')->where('id', ...)->update([...])` trên connection mặc định
      (kèm comment giải thích lý do không dùng lại Eloquent/`mysql2`)
- [x] `EmployeeInfoService.php`: gỡ import `TpEmployeeInfo` (không còn dùng trong file)

## Phase 2 — BE: guard null các chỗ `TpEmployeeInfo::find()` còn lại

- [x] Rà 5 chỗ gọi `TpEmployeeInfo::find()` ngoài chỗ nổ:
      `SalaryService.php:2287` và `CreateEmployeePayroll.php:864` — **đã có guard sẵn**, không sửa
- [x] `AuthController.php` `createNewToken()`: guard `if ($tp_employee_info)`, đổi
      `EmployeeInfo::where('id', $tp_employee_info->id)` → `$employee_info_id` (trước đây null là lỗi ngay
      bước đăng nhập); gộp 2 nhánh if/else trùng lặp thành 1
- [x] `WrContractWaitSettlementResource.php`: guard `TpEmployee`/`TpEmployeeInfo`/`TpCustomer` null
      (`optional()` cho `creator`, `approver`, `customer_code`)
- [x] Xác nhận luồng tạo/sửa nhân viên không còn chỗ nào khác đọc model `Tp*` bên trong transaction
      (grep `Tp[A-Z]*::` trong `EmployeeInfoService`, `EmployeeService`, `EmployeeInfoController`)

## Phase 3 — Verify

- [x] `php -l` 3 file sửa — sạch
- [x] Tinker probe: chứng minh root cause + fix hoạt động, rollback sạch (0 dòng test sót trong DB)
- [x] **User test trình duyệt**: tạo mới nhân viên có nhập tài khoản ngân hàng → lưu thành công,
      kiểm tra `employee_infos.account_number / bank_name / bank_branch / bank_province / account_name`
      đã điền đúng theo tài khoản đầu tiên
- [x] User test regression: sửa nhân viên (đổi tài khoản ngân hàng), đăng nhập lại, màn
      "Hợp đồng chờ quyết toán" (Assign)

### Checkpoint — 2026-08-19
Vừa hoàn thành: Phase 1 + 2 + phần verify tự động của Phase 3 (fix lỗi tạo nhân viên + guard null 2 chỗ khác).
Đang làm dở: không.
Bước tiếp theo: user test trình duyệt theo 2 mục chưa tick ở Phase 3.
Blocked: không.

## Còn nợ → đã xử lý ở feature `cut-erp-sync` (2026-08-19)

- Sau khi gộp DB, `SyncEmployeeInfoToErpJob` đang đọc/ghi **chính bảng nó vừa ghi** qua connection thừa
  (`mysql2` trỏ cùng database) → vô nghĩa và có nguy cơ ghi đè. Cần quyết định tắt `use_erp` / gỡ dần các
  model `Tp*`. Ảnh hưởng rộng: `Company`, `Department`, `Employee`, `Part`, `Group`, `EmployeeInfo`,
  `EmployeeService`, `DailyJobService` đều có nhánh `use_erp`.
