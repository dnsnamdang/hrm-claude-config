# Phụ cấp kiêm nhiệm ở tab Thông tin thu nhập — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development để triển khai từng task. Steps dùng checkbox (`- [ ]`).
> **Lưu ý project:** KHÔNG commit/push git. BE verify bằng `php -l`; FE verify bằng browser (Node 14 + Laragon). Không migration.

**Goal:** Khi nhân viên có ≥1 dòng phòng ban kiêm nhiệm, cho nhập tay Phụ cấp kiêm nhiệm (PC_KN) trong popup Thông tin thu nhập của hồ sơ nhân sự, lưu thật vào `employee_salary_history_allowances`, và hiện cột PC_KN trên bảng.

**Architecture:** BE Payroll: store đọc mảng `employee_salary_history_allowances` riêng (vì `$request->only` whitelist bỏ nó) → service `syncAllowances` xóa cũ + tạo lại, resolve allowance theo `allowance_id` hoặc `allowance_code='PC_KN'`. List đã trả allowances sẵn (eager-load). FE: modal nhận `concurrentPositions`, đảm bảo có entry PC_KN editable, gửi kèm khi submit.

**Tech Stack:** PHP 7.4 / Laravel 8 (Payroll module); Nuxt 2 / Vue 2 / Bootstrap-Vue (hrm-client).

**Spec:** `.plans/employee-info-concurrent-allowance/design.md`

---

## File Structure

**BE (`hrm-api`):**
- `Modules/Payroll/Http/Requests/EmployeeSalaryHistoryRequest.php` — validate mảng allowances.
- `Modules/Payroll/Services/EmployeeSalaryHistoryService.php` — thêm method `syncAllowances()` + import.
- `Modules/Payroll/Http/Controllers/Api/V1/EmployeeSalaryHistoryController.php` — store gọi `syncAllowances()` trong transaction.

**FE (`hrm-client`):**
- `components/modal/add-salary-history-modal.vue` — prop + computed + method + template PC_KN.
- `components/human-components/employee_info/EmployeeInfoForm.vue` — truyền prop + gọi prepareConcurrentAllowance.

---

> **Tiến độ:** Task 1-5 CODE DONE (2026-06-11), qua spec + code-quality review (BE: đổi `forceDelete`; FE: clone form trong `init`, key v-for ổn định). Task 6 chờ user verify browser.

## Task 1: BE — Request validate mảng allowances — ✅ DONE

**Files:**
- Modify: `hrm-api/Modules/Payroll/Http/Requests/EmployeeSalaryHistoryRequest.php`

- [ ] **Step 1: Thêm rule vào `rules()`**

Trong mảng `$rules` (sau dòng `'rank_id' => 'required',`, trước `];`), thêm:
```php
            'employee_salary_history_allowances' => 'nullable|array',
            'employee_salary_history_allowances.*.actual_amount' => 'nullable|numeric|min:0',
```

- [ ] **Step 2: Lint**

Run: `php -l hrm-api/Modules/Payroll/Http/Requests/EmployeeSalaryHistoryRequest.php`
Expected: `No syntax errors detected`

---

## Task 2: BE — Service `syncAllowances()`

**Files:**
- Modify: `hrm-api/Modules/Payroll/Services/EmployeeSalaryHistoryService.php`

- [ ] **Step 1: Thêm import (đầu file, cạnh các `use` khác)**

```php
use Modules\Human\Entities\Allowance;
use Modules\Payroll\Entities\EmployeeSalaryHistoryAllowance;
```
> Nếu file đã có sẵn 1 trong 2 import này thì bỏ qua dòng trùng.

- [ ] **Step 2: Thêm method `syncAllowances()` (đặt ngay sau method `save()`)**

```php
    public function syncAllowances($entity, array $allowances)
    {
        // Xóa phụ cấp cũ rồi tạo lại từ payload (FE gửi nguyên mảng)
        $entity->employeeSalaryHistoryAllowances()->delete();

        foreach ($allowances as $item) {
            $allowance = null;
            if (!empty($item['allowance_id'])) {
                $allowance = Allowance::find($item['allowance_id']);
            } elseif (!empty($item['allowance_code'])) {
                $allowance = Allowance::where('code', $item['allowance_code'])->first();
            }

            if (!$allowance) {
                continue;
            }

            EmployeeSalaryHistoryAllowance::create([
                'employee_salary_history_id' => $entity->id,
                'allowance_id' => $allowance->id,
                'allowance_name' => $allowance->name,
                'actual_amount' => $item['actual_amount'] ?? 0,
                'is_insurance' => $item['is_insurance'] ?? 0,
                'is_tax' => $item['is_tax'] ?? 0,
                'according_salary_ratio' => $item['according_salary_ratio'] ?? 0,
                'note' => $item['note'] ?? null,
            ]);
        }
    }
```

- [ ] **Step 3: Lint**

Run: `php -l hrm-api/Modules/Payroll/Services/EmployeeSalaryHistoryService.php`
Expected: `No syntax errors detected`

---

## Task 3: BE — Controller store gọi `syncAllowances()`

**Files:**
- Modify: `hrm-api/Modules/Payroll/Http/Controllers/Api/V1/EmployeeSalaryHistoryController.php`

- [ ] **Step 1: Gọi syncAllowances trong transaction của `store()`**

Trong `store()`, tìm:
```php
            $entity = $this->employeeSalaryHistoryService->save($employeeSalaryHistory);

            // Lưu lịch sử hồ sơ nhân sự sau khi lưu thành công
```
và chèn giữa 2 dòng đó (ngay sau dòng `$entity = ...save(...)`):
```php

            $this->employeeSalaryHistoryService->syncAllowances(
                $entity,
                $request->input('employee_salary_history_allowances', [])
            );
```
> `$request` ở đây là `app(EmployeeSalaryHistoryRequest::class)` (đã gán đầu hàm) → đọc được mảng allowances mà `$request->only([...])` đã bỏ.

- [ ] **Step 2: Lint**

Run: `php -l hrm-api/Modules/Payroll/Http/Controllers/Api/V1/EmployeeSalaryHistoryController.php`
Expected: `No syntax errors detected`

---

## Task 4: FE — Modal nhận props + logic PC_KN

**Files:**
- Modify: `hrm-client/components/modal/add-salary-history-modal.vue`

- [ ] **Step 1: Thêm prop `concurrentPositions`**

Trong khối `props: { ... }`, thêm:
```javascript
        concurrentPositions: {
            type: Array,
            default: () => [],
        },
```

- [ ] **Step 2: Thêm computed**

Trong `computed: { ... }` (cạnh `isUseDecision`), thêm:
```javascript
        hasConcurrent() {
            return (this.concurrentPositions || []).some((p) => p && p.department_id)
        },
        nonConcurrentAllowances() {
            return (this.form.employee_salary_history_allowances || []).filter(
                (a) => a.allowance_name !== 'Phụ cấp kiêm nhiệm' && a.allowance_code !== 'PC_KN'
            )
        },
        pcknEntry() {
            return (
                (this.form.employee_salary_history_allowances || []).find(
                    (a) => a.allowance_name === 'Phụ cấp kiêm nhiệm' || a.allowance_code === 'PC_KN'
                ) || null
            )
        },
```

- [ ] **Step 3: Thêm method `prepareConcurrentAllowance()`**

Trong `methods: { ... }` (ví dụ sau `init()`), thêm:
```javascript
        prepareConcurrentAllowance() {
            if (!Array.isArray(this.form.employee_salary_history_allowances)) {
                this.$set(this.form, 'employee_salary_history_allowances', [])
            }
            if (!this.hasConcurrent) return
            const exists = this.form.employee_salary_history_allowances.find(
                (a) => a.allowance_name === 'Phụ cấp kiêm nhiệm' || a.allowance_code === 'PC_KN'
            )
            if (!exists) {
                this.form.employee_salary_history_allowances.push({
                    allowance_code: 'PC_KN',
                    allowance_name: 'Phụ cấp kiêm nhiệm',
                    actual_amount: 0,
                    is_insurance: 0,
                    is_tax: 0,
                    according_salary_ratio: 0,
                })
            }
        },
```

- [ ] **Step 4: Template — đổi v-for readonly sang `nonConcurrentAllowances` + thêm dòng PC_KN editable**

Tìm dòng:
```html
                            <b-tr
                                v-for="(salaryAllowance, index) in form.employee_salary_history_allowances"
                                :key="index"
                            >
```
Đổi `in form.employee_salary_history_allowances` → `in nonConcurrentAllowances`.

Sau `</b-tr>` đóng vòng v-for đó (ngay trước `<b-tbody> </b-tbody>`), thêm dòng PC_KN:
```html
                            <b-tr v-if="hasConcurrent && pcknEntry">
                                <b-td>Phụ cấp kiêm nhiệm</b-td>
                                <b-td class="text-center align-middle">
                                    <currency-input
                                        v-model="pcknEntry.actual_amount"
                                        :disabled="isUseDecision"
                                    />
                                </b-td>
                                <b-td></b-td>
                                <b-td></b-td>
                                <b-td></b-td>
                            </b-tr>
```
> `currency-input` là component đã dùng sẵn trong file này (xem các dòng `actual_amount` khác). Nếu tên khác (vd `<Currency>`), dùng đúng tên đang có trong template.

- [ ] **Step 5: Verify build/lint FE (nếu có script lint)**

Run: `cd hrm-client; npx eslint components/modal/add-salary-history-modal.vue` (nếu dự án dùng eslint). Nếu không có, bỏ qua — verify ở Task 6 (browser).

---

## Task 5: FE — EmployeeInfoForm truyền prop + gọi prepare

**Files:**
- Modify: `hrm-client/components/human-components/employee_info/EmployeeInfoForm.vue`

- [ ] **Step 1: Truyền prop `concurrent-positions` xuống modal**

Tìm khối nhúng (~dòng 2356):
```html
        <AddSalaryHistoryModal
            @event="getListEmployeeSalary"
            :employee_info_id="id"
            :employee-salary-history="employeeSalaryHistory"
            :departments="departments"
            :workingPositions="listWorkingPositions"
            ref="salaryHistory"
        />
```
Thêm 1 dòng prop trước `ref="salaryHistory"`:
```html
            :concurrent-positions="employee_concurrently_department_has_positions"
```

- [ ] **Step 2: Gọi `prepareConcurrentAllowance()` trong `openSalaryHistory()`**

Tìm method (~dòng 2999):
```javascript
        openSalaryHistory(employeeSalaryHistory = null) {
            this.$bvModal.show('add-salary-history')

            if (employeeSalaryHistory) {
                this.$refs.salaryHistory.init(employeeSalaryHistory)
                this.$refs.salaryHistory.setDepartment(employeeSalaryHistory.department_id)
                if (employeeSalaryHistory.working_position) {
                    this.$refs.salaryHistory.setWorkingPosition(employeeSalaryHistory.working_position.id)
                }
            } else {
                this.employeeSalaryHistory = null
                this.$refs.salaryHistory.setDepartment(this.form.department_id)
                this.$refs.salaryHistory.setWorkingPosition(this.form.employee_work_position_id)
            }
        },
```
Thêm `this.$refs.salaryHistory.prepareConcurrentAllowance()` ở CUỐI cả 2 nhánh (cuối khối `if` và cuối khối `else`), ví dụ sau dòng setWorkingPosition trong `if` và sau setWorkingPosition trong `else`.

> Dùng `this.$nextTick(() => this.$refs.salaryHistory.prepareConcurrentAllowance())` nếu gọi ngay sau `init()` mà chưa thấy entry (đảm bảo form đã gán xong).

---

## Task 5b: FE — Dòng PC_KN cho tick BHXH/Thuế/Theo tỉ lệ — ✅ DONE (2026-06-11)
Theo yêu cầu bổ sung: thay 3 ô `<b-td></b-td>` trống của dòng PC_KN bằng 3 `b-form-checkbox` `:value="1" :unchecked-value="0" :disabled="isUseDecision"` v-model vào `pcknEntry.is_insurance / is_tax / according_salary_ratio` (mirror các dòng phụ cấp khác). Không sửa BE (syncAllowances đã map sẵn 3 trường). File: `add-salary-history-modal.vue`.

## Task 7: BUG — Báo cáo lương gắn PC kiêm nhiệm nhầm phòng — ✅ CODE DONE (2026-06-11)
> Verify SQL: emp17 (PC_KN 200k, phòng kiêm nhiệm cd_id=551) → dòng kiêm nhiệm nhận salary_concurrently=200000, mainQuery=0. `php -l` sạch. Chờ user verify browser trên môi trường có data (Lê Văn Hồng).


**Triệu chứng:** Màn `human/report/employee_salary_report` hiển thị PC kiêm nhiệm ở dòng PHÒNG CHÍNH thay vì dòng PHÒNG KIÊM NHIỆM.
**Root cause:** `Modules/Payroll/Services/SalaryService.php::report()` — `$mainQuery.salary_concurrently = COALESCE(pckn.actual_amount,0)` (gắn vào phòng chính); `$concurrentQuery.salary_concurrently = 0`.
**Quyết định user:** Chuyển PC_KN sang dòng phòng kiêm nhiệm; nếu NV có nhiều phòng kiêm nhiệm → chỉ gắn vào dòng đầu tiên (`cd.id = MIN(id)`).
**Fix (BE only, 1 file):**
- mainQuery: bỏ join `pckn`; `salary_concurrently = 0`; bỏ `+ COALESCE(pckn.actual_amount,0)` khỏi `total`.
- concurrentQuery: thêm join `pckn` (on `esh.id`, `AND deleted_at IS NULL`); `salary_concurrently` và `total` = `CASE WHEN cd.id = (SELECT MIN(c2.id) ... WHERE c2.employee_info_id = employee_infos.id) THEN COALESCE(pckn.actual_amount,0) ELSE 0 END`.
- Phần tổng hợp (group/sum theo dòng) không đổi → tổng phòng Kiểm soát +PC_KN, phòng chính −PC_KN tự động.
**Verify:** local Lê Văn Hồng không có data; cần user verify trên môi trường có data (PC_KN hiện ở dòng "(kiêm nhiệm)" phòng kiêm nhiệm, phòng chính = 0).

## Task 6: Verify thủ công end-to-end (browser) — ⏳ CHỜ USER

### Checkpoint — 2026-06-11
Vừa hoàn thành: Task 1-5 code (BE 3 file: Request + Service syncAllowances(forceDelete) + Controller store; FE 2 file: modal prop/computed/method/template + EmployeeInfoForm truyền prop + gọi prepare). Qua spec review ✅ + code-quality review ✅ (đã vá: BE forceDelete tránh rác soft-delete; FE clone form trong init tránh mutate object parent, key v-for ổn định). `php -l` BE sạch.
Đang làm dở: không có.
Bước tiếp theo: User verify browser theo Task 6.
Blocked: (không)


- [ ] **Step 1: Có kiêm nhiệm → nhập & lưu PC_KN**
1. Mở `human/employee_info/{id}` của NV; tab "Phòng ban/Chức vụ kiêm nhiệm" thêm ≥1 dòng (chọn phòng ban + chức vụ).
2. Sang tab "Thông tin thu nhập" → "Thêm" (hoặc sửa 1 dòng) → popup hiện ô **"Phụ cấp kiêm nhiệm"** editable → nhập số tiền → Lưu.
Expected: lưu thành công; bảng thu nhập hiện **cột "Phụ cấp kiêm nhiệm"** với đúng số tiền.

- [ ] **Step 2: Sửa lại đúng giá trị (prefill)**
Bấm sửa lại bản ghi vừa lưu → popup prefill đúng số tiền PC_KN → đổi số khác → Lưu → cột cập nhật.

- [ ] **Step 3: Không kiêm nhiệm → không hiện ô**
NV không có dòng phòng ban kiêm nhiệm → popup thu nhập KHÔNG hiện ô PC_KN; lưu lương bình thường không tạo phụ cấp rác.

- [ ] **Step 4: Lỗi (nếu có)** → xem `hrm-api/storage/logs/laravel-2026-06-11.log`.

---

## Self-Review

- **Spec coverage:** 4.2 store đọc allowances → Task 3; syncAllowances resolve code → Task 2; 4.3 validate → Task 1; 5.1 truyền prop + prepare → Task 5; 5.2 modal prop/computed/method/template → Task 4; cột/list đã có sẵn (không task). ✓
- **Placeholder scan:** không TBD; mọi step có code/lệnh cụ thể. ✓
- **Type consistency:** `concurrentPositions` prop ↔ `:concurrent-positions`; entry PC_KN dùng `allowance_code='PC_KN'` nhất quán FE (push/computed) ↔ BE resolve theo `allowance_code`; `pcknEntry`/`hasConcurrent`/`nonConcurrentAllowances`/`prepareConcurrentAllowance` đặt tên nhất quán FE; `syncAllowances($entity, array)` chữ ký khớp lời gọi controller. ✓
