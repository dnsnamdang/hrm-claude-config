# Plan — Tính Thuế TNCN trong bảng lương

> **Spec:** `docs/superpowers/specs/2026-05-13-personal-income-tax-design.md`
> **Owner:** @khoipv
> **Tạo:** 2026-05-13

---

## Phase 1 — BE: Database

### Task 1.1 — Migration tạo bảng `tncn_tax_configs` ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_05_14_100001_create_tncn_tax_configs_table.php`

- [x] Tạo schema theo Section 3.1 của spec (id, date, self_deduction, dependent_deduction, union_fee_rate, company_id, created_by, updated_by, timestamps, index [company_id, date])
- [x] `comment()` đầy đủ trên các cột
- [x] KHÔNG khai foreign key constraint (theo convention)
- [x] Chạy `php artisan migrate` → verify bảng tạo OK

### Task 1.2 — Migration tạo bảng `tncn_tax_brackets` ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_05_14_100002_create_tncn_tax_brackets_table.php`

- [x] Tạo schema theo Section 3.2: id, tncn_tax_config_id (index), level (tinyInteger), from_amount, to_amount (nullable), rate (float), timestamps
- [x] `comment()` đầy đủ
- [x] Migrate → verify

### Task 1.3 — Migration alter `employee_relationships` ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_05_14_100003_add_dependent_columns_to_employee_relationships_table.php`

- [x] Thêm 3 cột theo Section 3.3: `is_dependent` (boolean default false), `dependent_start_date` (date nullable), `dependent_end_date` (date nullable)
- [x] Migrate → verify
- [x] Down migration drop 3 cột

### Task 1.4 — Migration insert composition `THUE_TNCN` ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_05_14_100004_insert_thue_tncn_system_salary_composition.php`

- [x] Theo Section 3.4 — insert vào `system_salary_compositions` (check tồn tại theo code = 'THUE_TNCN' trước khi insert)
- [x] `type=7, feature=2, value_type=2, tax_deduction=false, is_show_paycheck=true, status=1`
- [x] Down: delete where code='THUE_TNCN'
- [x] Migrate → verify row có trong DB

### Task 1.5 — Migration seed default `tncn_tax_configs` cho mỗi company ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_05_14_100005_seed_default_tncn_tax_configs.php`

- [x] Loop qua mọi company trong bảng `companies`
- [x] Insert 1 row config: `date='2020-07-01'`, `self_deduction=11000000`, `dependent_deduction=4400000`, `union_fee_rate=1`
- [x] Insert 7 brackets theo bảng Section 3.5
- [x] Down: chỉ xóa configs/brackets do migration tạo (date='2020-07-01')
- [x] Migrate → 9 company, 9 config, 63 brackets ✅

---

## Phase 2 — BE: Entities + CRUD config

### Task 2.1 — Entity `TncnTaxConfig`

**File tạo:**
- `hrm-thanhan-api/Modules/Payroll/Entities/TncnTaxConfig.php`

- [x] Extends `BaseModel`, `$table = 'tncn_tax_configs'`, `$guarded = []`
- [x] Relationship `brackets() : hasMany(TncnTaxBracket::class, 'tncn_tax_config_id')`
- [x] Cast `date` → date

### Task 2.2 — Entity `TncnTaxBracket` ✅

**File tạo:**
- `Modules/Payroll/Entities/TncnTaxBracket.php`

- [x] Extends `BaseModel`, `$table = 'tncn_tax_brackets'`
- [x] Relationship `config() : belongsTo(TncnTaxConfig::class, 'tncn_tax_config_id')`

### Task 2.3 — Update Entity `EmployeeRelationship` ✅

**File sửa:**
- `Modules/Human/Entities/EmployeeRelationship.php`

- [x] Thêm `is_dependent`, `dependent_start_date`, `dependent_end_date` vào `$fillable`
- [x] Cast 2 cột date → date, is_dependent → boolean

### Task 2.4 — `TncnTaxConfigRequest` ✅

**File tạo:**
- `Modules/Payroll/Http/Requests/TncnTaxConfigRequest.php`

- [x] Extends `FormRequest` (theo pattern InsuranceConfig)
- [x] Validate rules đầy đủ cho config + brackets
- [x] Custom `withValidator`: check gap/overlap, bậc cuối to_amount=null, từng bậc tiếp theo bắt đầu = bậc trước to_amount

### Task 2.5 — `TncnTaxConfigService` ✅

**File tạo:**
- `Modules/Payroll/Services/TncnTaxConfigService.php`

- [x] `index($request)` — list config theo company hiện tại, eager load brackets, order date desc
- [x] `store($attributes)` — DB::transaction: insert config + brackets
- [x] `update($id, $attributes)` — DB::transaction: update config, delete brackets cũ, insert mới
- [x] `delete($id)` — DB::transaction: delete brackets → delete config

### Task 2.6 — Transformer (List) ✅

**File tạo:**
- `Modules/Payroll/Transformers/TncnTaxConfigResource/TncnTaxConfigListResource.php`

- [x] Map config + brackets về JSON gọn (id, date, deductions, union_fee_rate, brackets)
- [x] Không cần Detail riêng vì list đã trả đủ thông tin (config đơn giản)

### Task 2.7 — Controller ✅

**File tạo:**
- `Modules/Payroll/Http/Controllers/Api/V1/TncnTaxConfigController.php`

- [x] Extends `ApiController` (Payroll)
- [x] `index` trả Resource
- [x] `store(TncnTaxConfigRequest)` + `update($id, TncnTaxConfigRequest)` + `delete($id)`

### Task 2.8 — Routes ✅

**File sửa:**
- `Modules/Payroll/Routes/api.php`

- [x] Thêm group `prefix('human/tncn_tax_config')` với 4 routes
- [x] `php artisan route:list` xác nhận 4 endpoint hoạt động

---

## Phase 3 — BE: Helper TaxCalculator + Integration

### Task 3.1 — Helper `TaxCalculator` ✅

**File tạo:**
- `Modules/Payroll/Helpers/TaxCalculator.php`

- [x] Method static `calc($employeeInfoId, $salaryHistory, $companyId, $periodDate): int`
- [x] Bước 1: check EmployeeTax — không có row → mặc định Lũy tiến, tax_type ≠ 1 → 0
- [x] **Bước 2 (CÁCH A):** sum 7 field tĩnh trên `employee_salary_histories` theo cờ `*_tax`
- [x] Bước 3: Giảm trừ BHXH NLĐ (5 cột worker_*) từ `insurance_configs` mới nhất ≤ periodDate
- [x] Bước 4: pick `tncn_tax_configs` theo company + date
- [x] Bước 5: giảm trừ công đoàn (insurance_salary × union_fee_rate / 100)
- [x] Bước 6: count `employee_relationships` is_dependent + ngày
- [x] Bước 7: thu nhập tính thuế, ≤ 0 → 0
- [x] Bước 8: áp lũy tiến 7 bậc
- [x] Smoke test 4 case: 2.150.000 / 1.927.500 / 1.267.500 / 0 — đều khớp tay

### Task 3.2 — Inject vào `SalaryService::calcData()` ✅

**File sửa:**
- `Modules/Payroll/Services/SalaryService.php` — thêm case 'THUE_TNCN' ở đầu method `calcData()` (~dòng 1413)
- Import `Modules\Payroll\Helpers\TaxCalculator`

- [x] Trong `calcData`, thêm nhánh `if ($salary_composition_code == 'THUE_TNCN')` chạy đầu tiên
- [x] Lấy `EmployeeSalaryHistory` mới nhất theo `start_date` ≤ apply_date
- [ ] Gọi `TaxCalculator::calc(...)` → return int
- [ ] Đảm bảo logic không ảnh hưởng các composition khác

### Task 3.3 — Smoke test TaxCalculator ✅

- [x] Test 1 — TN=30tr, 0 BHXH/CD, 0 NPT → 2.150.000 ✅
- [x] Test 2 — TN=30tr, BHXH 10.5%, CĐ 1%, 0 NPT → 1.927.500 ✅
- [x] Test 3 — TN=30tr, BHXH 10.5%, CĐ 1%, 1 NPT → 1.267.500 ✅
- [x] Test 4 — TN=10tr (sau giảm trừ âm) → 0 ✅
- [ ] E2E qua bảng lương thật — anh test khi UI sẵn sàng (Phase 6)

---

## Phase 4 — FE: Settings Cấu hình thuế

### Task 4.1 — Constants + DEFAULT brackets ✅

- [x] Embed DEFAULT_BRACKETS trong component `TncnTaxConfigSection.vue` (7 bậc luật)
- [x] Const URL `human/tncn_tax_config`

### Task 4.2 — Section "Cấu hình thuế TNCN" ✅

**File tạo:**
- `pages/human/settings/components/TncnTaxConfigSection.vue`

**File sửa:**
- `pages/human/settings/index.vue` — import + mount component sau bảng BHXH

- [x] Bảng inline edit pattern giống BHXH: STT | Ngày HL | GT bản thân | GT NPT | CĐ % | Biểu thuế (nút mở modal) | Action
- [x] DatePicker month picker (YYYY-MM)
- [x] Nút `[+]` thêm row mới — pre-fill từ row gần nhất hoặc DEFAULT
- [x] Gọi `apiGet` (list), `apiPostMethod`/`apiPutMethod` (save), `apiDelete` (xóa)
- [x] Confirm dialog trước khi xóa

### Task 4.3 — Modal "Biểu thuế lũy tiến" ✅

**File tạo:**
- `pages/human/settings/components/TncnBracketsModal.vue`

- [x] Bảng N bậc: Bậc | Từ | Đến | Thuế suất | Action
- [x] Nút thêm/xóa bậc, tự sync `from_amount` bậc tiếp theo
- [x] Bậc cuối auto `to_amount = null` ("Không giới hạn")
- [x] Validate FE: rate 0-100, "Đến" > "Từ", relink khi thay đổi

### Task 4.4 — Test FE

- [ ] Anh test trên UI thật (Phase 6)

---

## Phase 5 — FE: Thân nhân — đánh dấu người phụ thuộc

### Task 5.1 — Bổ sung 3 trường vào form thân nhân ✅

**File sửa (FE):**
- `components/human-components/employee_info/EmployeeInfoForm.vue` — thêm 3 cột vào bảng "Thông tin gia đình"
  - `is_dependent` (b-form-checkbox)
  - `dependent_start_date` (date-picker, chỉ show khi is_dependent=true)
  - `dependent_end_date` (date-picker, chỉ show khi is_dependent=true)
- [x] Cập nhật `addRelationship()` + state init để có 3 field

**File sửa (BE):**
- `Modules/Human/Services/EmployeeInfoService.php`
  - [x] `select(...)` thêm 3 cột để FE đọc khi edit NV cũ
  - [x] `syncEmployeeRelationships()` lưu 3 trường mới

**Lưu ý:**
- Chưa cập nhật 2 file biến thể: `my-info-request/EmployeeInfoForm.vue` và `request-update/EmployeeInfoForm.vue` (khác scope — màn yêu cầu cập nhật thông tin)
- Validation BE cho `is_dependent=true` → `dependent_start_date` required → để ticket sau khi anh xác nhận flow

### Task 5.2 — Test FE

- [ ] Anh test trên UI thật (Phase 6)

---

## Phase 6 — Test E2E

### Task 6.1 — Tạo template lương có composition THUE_TNCN

- [ ] Vào màn cấu hình salary template → thêm composition `THUE_TNCN` vào nhóm Khấu trừ
- [ ] Verify hiện đúng trong template

### Task 6.2 — Tính 1 kỳ lương đầy đủ

- [ ] Setup: 1 NV có lương, đóng BHXH, có 1 người phụ thuộc đã đánh dấu
- [ ] Tạo bảng lương → verify dòng "Thuế TNCN" có số tiền đúng theo công thức
- [ ] Verify `total_deduction` đã cộng thuế
- [ ] Verify `thuc_linh` = total_income − total_deduction − advance đúng
- [ ] Export phiếu lương → verify hiển thị dòng thuế

### Task 6.3 — Test edge case

- [ ] NV không có người phụ thuộc → thuế khớp công thức không trừ NPT
- [ ] NV `has_insurance = false` → không trừ BHXH
- [ ] NV `has_union = false` → không trừ công đoàn
- [ ] NV thu nhập thấp (sau giảm trừ ≤ 0) → thuế = 0
- [ ] NV có row `employee_taxs` với `tax_type=0` (Miễn) → thuế = 0
- [ ] Company chưa config thuế → thuế = 0 (không lỗi)

---

## Checkpoint

_(cập nhật khi wrap up)_

### Checkpoint — 2026-05-13 (khởi tạo)
Vừa hoàn thành: Brainstorming + spec đầy đủ + plan
Đang làm dở: Chưa bắt đầu code
Bước tiếp theo: Task 1.1 — Migration `tncn_tax_configs`
Blocked: Không

### Checkpoint — 2026-05-14 (cuối phiên — E2E verify trên bảng lương 108)
Vừa hoàn thành:
- Verify integration end-to-end trên bảng lương 108, NV 42 (Nguyễn Thị Hải)
- Khẳng định: composition `THUE_TNCN` tự cộng vào `total_deduction`, `thuc_linh` tự cập nhật — engine có sẵn lo phần này, KHÔNG sửa công thức nào
- Phát hiện bug **dữ liệu** (không phải code): user nhập `self_deduction = 1.000.000` thay vì 11.000.000 → thuế tính ra 740.641 (cao bất thường). Hướng dẫn sửa qua UI Settings
- Bổ sung ví dụ minh họa đầy đủ vào `design.md` (8 bước tính cho Nguyễn Thị Hải + tác động xuống thuc_linh + 3 bài học khi test)
- FE đã được user/linter chỉnh: dùng `BaseDatePicker`, `BaseCurrencyInput` thay date-picker + input number

Đang làm dở: Không

Bước tiếp theo: Anh test trên các kỳ lương khác + các case khác (NV có nhiều phần lương chịu thuế, NPT theo nhiều khoảng thời gian) để xác nhận trước khi đóng feature

Blocked: Không

### Checkpoint — 2026-05-14
Vừa hoàn thành:
- **Phase 1 (DB):** 5 migration đã chạy migrate trên local — 9 company × 9 config × 63 brackets, composition THUE_TNCN đã insert, 3 cột mới trên employee_relationships
- **Phase 2 (CRUD config):** Entity + Service + Request (với withValidator check gap/overlap) + Resource + Controller + 4 routes (GET/POST/PUT/DELETE `/api/v1/human/tncn_tax_config`)
- **Phase 3 (TaxCalculator):** Helper `Modules/Payroll/Helpers/TaxCalculator.php` (Cách A — 7 cờ tĩnh), inject vào `SalaryService::calcData()` với case 'THUE_TNCN'. 4/4 smoke test pass (tinker)
- **Phase 4 (FE Settings):** `TncnTaxConfigSection.vue` + `TncnBracketsModal.vue` + mount vào `pages/human/settings/index.vue`
- **Phase 5 (FE Thân nhân):** Bổ sung 3 cột vào `components/human-components/employee_info/EmployeeInfoForm.vue` + sync trong `EmployeeInfoService.php` (select + syncEmployeeRelationships)

Đang làm dở: Chưa làm Phase 6 (E2E qua UI thật — anh chạy server FE để test)

Bước tiếp theo: Anh review code rồi test E2E theo Task 6.1-6.3:
1. Vào màn Cấu hình HCNS → verify section TNCN load 7 bậc default, sửa/xóa OK
2. Vào màn NV → tab Thông tin gia đình → tick "Người PT thuế" → lưu → reload verify
3. Cấu hình salary template thêm composition `THUE_TNCN` → tạo bảng lương → verify số thuế

Blocked: Không
Lưu ý:
- Đã chọn **Cách A** (7 cờ tĩnh trên `employee_salary_histories`) — không cover phụ cấp động
- Chưa update 2 file biến thể của EmployeeInfoForm (my-info-request, request-update)
- Validation BE "is_dependent=true → start_date required" chưa thêm — chờ anh xác nhận
