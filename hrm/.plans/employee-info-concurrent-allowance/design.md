# Nhập & lưu Phụ cấp kiêm nhiệm (PC_KN) ở tab Thông tin thu nhập — Hồ sơ nhân sự

> Người phụ trách: @khoipv
> Loại: Feature vừa (1 phase, BE + FE)
> Ngày tạo: 2026-06-11

## 1. Mục tiêu

Trên màn sửa hồ sơ nhân sự (`human/employee_info/{id}`), khi nhân viên có ≥1 dòng **"Phòng ban/Chức vụ kiêm nhiệm"** (thêm tay, không qua quyết định):
- Popup **"Thông tin thu nhập"** hiện 1 ô nhập **Phụ cấp kiêm nhiệm (PC_KN)** — nhập tay số tiền.
- Lưu thật vào lịch sử lương (bảng `employee_salary_history_allowances`).
- Bảng "Thông tin thu nhập" hiện **cột "Phụ cấp kiêm nhiệm"** với giá trị đã lưu.

## 2. Hiện trạng (nguyên nhân)

1. **Cột không hiện vì CHƯA CÓ DỮ LIỆU PC_KN:** `service::list()` đã eager-load `employeeSalaryHistoryAllowances` (dòng 32) và model `EmployeeSalaryHistory` không có `$hidden/$visible/$appends` → quan hệ **đã tự serialize** thành `employee_salary_history_allowances` trong response list. Cột `showConcurrentAllowanceColumn`/`getConcurrentAllowance` ẩn chỉ vì nhân viên **chưa có** bản ghi phụ cấp tên `'Phụ cấp kiêm nhiệm'` (chưa có đường nhập tay). → **Không cần sửa ListResource.**
2. **Popup không cho nhập:** `add-salary-history-modal.vue` chỉ render `form.employee_salary_history_allowances` ở chế độ Sửa (lấy từ object list), `actual_amount` để `disabled`; khi Thêm mới mảng không được khởi tạo; không có dòng PC_KN; modal không biết NV có kiêm nhiệm hay không.
3. **BE không lưu phụ cấp:** `store()` dùng `$request->only([...])` whitelist cố định (không có allowances); `EmployeeSalaryHistoryService::save()` chỉ fill cột cơ bản; Request không validate allowances. Chỉ Decision module mới ghi vào bảng phụ cấp. → **Đây là gap chính cần vá.**

Bảng `employee_salary_history_allowances` đã có sẵn (cột: `employee_salary_history_id, allowance_id, allowance_name, according_salary_ratio, actual_amount, note, is_insurance, is_tax`, có `softDeletes`). PC_KN nhận diện qua `Allowance` `code='PC_KN'`, name `'Phụ cấp kiêm nhiệm'`. **Không cần migration.**

## 3. Quyết định thiết kế (đã chốt với user)

| # | Nội dung | Quyết định |
|---|----------|-----------|
| 1 | Khi nào hiện ô PC_KN | Khi NV có ≥1 dòng phòng ban kiêm nhiệm (`department_id` khác null). |
| 2 | Giá trị PC_KN | Nhập tay số tiền. |
| 3 | Phạm vi | Lưu thật (FE + BE). |
| 4 | Khóa ô khi dùng quyết định | Ô PC_KN `disabled` theo `isUseDecision` (nhất quán popup). |
| 5 | Tick BHXH/Thuế/Theo tỉ lệ cho PC_KN | CÓ (cập nhật 2026-06-11) — dòng PC_KN cho tick `is_insurance / is_tax / according_salary_ratio` như các phụ cấp khác (mặc định 0). BE đã lưu sẵn 3 trường, chỉ sửa FE template. |
| 6 | Mô hình hóa PC_KN | Là 1 entry trong `employee_salary_history_allowances` (không tạo field scalar riêng). |

## 4. Phạm vi Backend (`hrm-api` — Modules/Payroll)

### 4.1. List trả phụ cấp — ĐÃ CÓ SẴN (chỉ verify)
- `service::list()` đã `->with('employeeSalaryHistoryAllowances')`; model không ẩn quan hệ → response list đã có `employee_salary_history_allowances`. **Không sửa.** Chỉ verify lại bằng API/tinker sau khi có dữ liệu PC_KN.

### 4.2. Lưu phụ cấp khi store/update
- `EmployeeSalaryHistoryController::store()`: sau khi `$entity = ...->save(...)` và TRONG cùng transaction, gọi:
  ```php
  $this->employeeSalaryHistoryService->syncAllowances(
      $entity,
      request()->input('employee_salary_history_allowances', [])
  );
  ```
  (Đọc allowances **riêng** vì `$request->only([...])` không lấy mảng này.)
- `EmployeeSalaryHistoryService::syncAllowances($entity, array $allowances)` (method mới):
  - Xóa phụ cấp cũ của bản ghi (`$entity->employeeSalaryHistoryAllowances()->delete()` — soft delete) rồi tạo lại từ payload. FE gửi **nguyên mảng** nên không mất phụ cấp khác.
  - **Resolve allowance theo `allowance_id` HOẶC `allowance_code`** (FE entry PC_KN gửi `allowance_code='PC_KN'`, không gửi id): nếu có `allowance_id` → `Allowance::find(id)`; elif `allowance_code` → `Allowance::where('code', code)->first()`. Bỏ qua item không resolve được allowance.
  - `allowance_name` lấy từ allowance resolve được; map `actual_amount` (mặc định 0), `is_insurance`/`is_tax`/`according_salary_ratio` (mặc định 0).
  - KHÔNG bỏ item amount=0 (lưu cả 0 để cột vẫn hiện — `getConcurrentAllowance` trả 0 ≠ null).

> Resolve theo `code` giúp FE không cần biết `allowance_id` của PC_KN → bỏ phụ thuộc `allowanceOptions` ở FE.

### 4.3. Request validation
- `EmployeeSalaryHistoryRequest::rules()`: thêm (nới lỏng vì id do BE resolve):
  ```php
  'employee_salary_history_allowances' => 'nullable|array',
  'employee_salary_history_allowances.*.actual_amount' => 'nullable|numeric|min:0',
  ```

> Không migration. Không đụng logic tính lương payroll (CreateEmployeePayroll đã đọc PC_KN từ bảng này — sẽ tự nhận giá trị mới).

## 5. Phạm vi Frontend (`hrm-client`)

### 5.1. `components/human-components/employee_info/EmployeeInfoForm.vue`
- Truyền xuống `<AddSalaryHistoryModal>` (dòng ~2356): `:concurrent-positions="employee_concurrently_department_has_positions"` (mảng kiêm nhiệm live).
- Trong `openSalaryHistory()` (cả 2 nhánh Thêm/Sửa): sau `init()`/`setDepartment()` gọi `this.$refs.salaryHistory.prepareConcurrentAllowance()` (vì nhánh Thêm mới KHÔNG gọi `init()`).
- KHÔNG cần `allowanceOptions`/`pcknAllowance` (BE resolve theo code).

### 5.2. `components/modal/add-salary-history-modal.vue`
- **Prop mới:** `concurrentPositions: { type: Array, default: () => [] }`.
- **Computed `hasConcurrent`:** `(this.concurrentPositions || []).some(p => p && p.department_id)`.
- **Computed `nonConcurrentAllowances`:** `(this.form.employee_salary_history_allowances || []).filter(a => a.allowance_name !== 'Phụ cấp kiêm nhiệm' && a.allowance_code !== 'PC_KN')` — dùng cho v-for readonly (loại PC_KN ra).
- **Computed `pcknEntry`:** tìm entry PC_KN (`allowance_name === 'Phụ cấp kiêm nhiệm'` hoặc `allowance_code === 'PC_KN'`) trong `form.employee_salary_history_allowances`, hoặc null.
- **Method `prepareConcurrentAllowance()`:**
  - Nếu `form.employee_salary_history_allowances` chưa là mảng → `this.$set(this.form, 'employee_salary_history_allowances', [])`.
  - Nếu `hasConcurrent` và chưa có `pcknEntry` → push `{ allowance_code: 'PC_KN', allowance_name: 'Phụ cấp kiêm nhiệm', actual_amount: 0, is_insurance: 0, is_tax: 0, according_salary_ratio: 0 }`.
- **Template (bảng phụ cấp trong popup):**
  - Đổi v-for readonly từ `form.employee_salary_history_allowances` → `nonConcurrentAllowances`.
  - Thêm 1 dòng PC_KN editable `v-if="hasConcurrent && pcknEntry"`: cột tên "Phụ cấp kiêm nhiệm" + `currency-input` editable `:disabled="isUseDecision"` `v-model="pcknEntry.actual_amount"` + 3 ô trống (BHXH/Thuế/Theo tỉ lệ — bỏ trống, không tick).
- **Submit:** `sendSubmitForm()` đã gửi nguyên `this.form` (gồm `employee_salary_history_allowances`) → không đổi.

> Lưu ý: `init()` thay `this.form = employeeSalaryHistory` (object từ list) — ở chế độ Sửa, list đã trả `employee_salary_history_allowances` (mục 4.1) nên `pcknEntry` prefill đúng.

### 5.3. Bảng "Thông tin thu nhập" (EmployeeInfoForm)
- Không đổi: `showConcurrentAllowanceColumn` + `getConcurrentAllowance` đã đọc theo tên `'Phụ cấp kiêm nhiệm'`; sẽ tự hiện sau khi list trả allowances + có dữ liệu lưu.

## 6. Luồng dữ liệu

```
Thêm dòng PB kiêm nhiệm (form) → mở popup Thu nhập → hiện ô PC_KN (editable)
   → nhập số tiền → Lưu → POST payload kèm employee_salary_history_allowances[PC_KN]
   → BE store(): save history + syncAllowances() ghi bảng employee_salary_history_allowances
   → reload list (getListEmployeeSalary) → ListResource trả allowances
   → cột "Phụ cấp kiêm nhiệm" hiện giá trị; popup Sửa prefill đúng.
```

## 7. Ngoài phạm vi
- Không tự tính PC_KN theo công thức (nhập tay).
- Không tick BHXH/Thuế cho PC_KN.
- Không migration; không đụng job tính lương (chỉ đọc lại giá trị mới).
- Không xử lý đồng bộ ngược từ quyết định (đã có feature `appoint-concurrent-sync-employee` riêng cho bảng phòng ban kiêm nhiệm; phần lương PC_KN qua quyết định vẫn theo luồng Decision cũ).

## 8. File dự kiến chạm
**BE:**
- `Modules/Payroll/Services/EmployeeSalaryHistoryService.php` (thêm method `syncAllowances`)
- `Modules/Payroll/Http/Controllers/Api/V1/EmployeeSalaryHistoryController.php` (store gọi syncAllowances trong transaction)
- `Modules/Payroll/Http/Requests/EmployeeSalaryHistoryRequest.php` (validate mảng allowances)
- *(ListResource KHÔNG sửa — list đã trả allowances sẵn)*

**FE:**
- `components/human-components/employee_info/EmployeeInfoForm.vue`
- `components/modal/add-salary-history-modal.vue`
