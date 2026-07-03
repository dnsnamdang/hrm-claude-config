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

## Phase 7 — Đa-đoạn tax_type trong 1 kỳ lương

> **Spec:** Section 9 trong `docs/superpowers/specs/2026-05-13-personal-income-tax-design.md`
> **Mục tiêu:** Hỗ trợ NV đổi loại thuế giữa kỳ (vd: 01–10/04 chịu 10%, 11–30/04 chịu lũy tiến).

### Task 7.1 — Migration alter `employee_taxs` ✅

**File tạo:**
- `Modules/Payroll/Database/Migrations/2026_05_26_100001_add_date_range_to_employee_taxs_table.php`

- [x] Thêm 2 cột: `start_date` (date nullable), `end_date` (date nullable)
- [x] Thêm index `[employee_info_id, start_date]`
- [x] Down: drop 2 cột + index
- [x] Migrate → verify

### Task 7.2 — Update Entity + Request `EmployeeTax` ✅

- [x] `EmployeeTax`: thêm `start_date`, `end_date` vào `$fillable` + cast date
- [x] Request validate: `start_date ≤ end_date`, không overlap, chỉ row mới nhất được end_date=NULL

### Task 7.3 — `EmployeeTaxService` CRUD nhiều row/NV ✅

- [x] Thêm `listByEmployee`, `storeRow`, `updateRow` (giữ `delete` cũ)
- [x] Tạo `EmployeeTaxController` (4 endpoints) + 4 routes `human/employee_tax`
- [x] `php artisan route:list` xác nhận hoạt động

### Task 7.4 — Refactor `TaxCalculator::calc(...)` hỗ trợ đa đoạn ✅

**File sửa:**
- `Modules/Payroll/Helpers/TaxCalculator.php`

- [x] Đổi signature: `($empId, $h, $companyId, $periodStart, $periodEnd)` — D_total tự tính từ ngày dương lịch
- [x] `buildSegments()` load EmployeeTax rows overlap kỳ, cắt thành segments, gap → mặc định Lũy tiến
- [x] `calcProgressivePortion()` gộp các đoạn lũy tiến, BHXH/CD chia tỷ lệ ngày, giảm trừ NGUYÊN THÁNG
- [x] Đoạn 10%/20%: `income_i × rate`, không giảm trừ
- [x] Đoạn Miễn: 0

### Task 7.5 — Update `SalaryService::calcData()` truyền params mới ✅

**File sửa:**
- `Modules/Payroll/Services/SalaryService.php` (case 'THUE_TNCN')

- [x] Derive `periodStart` = đầu tháng, `periodEnd` = cuối tháng từ `apply_date`
- [x] Truyền vào `TaxCalculator::calc(...)`

### Task 7.6 — Smoke test TaxCalculator đa đoạn ✅ (qua tinker, 6/6 PASS)

- [x] Test 1 — No row, full LT, 0 NPT → 1.395.961 (khớp tay với self=1M)
- [x] Test 2 — Toàn kỳ 10% → 1.600.000 (16M × 10%)
- [x] Test 3 — Toàn kỳ 20% → 3.200.000
- [x] Test 4 — Toàn kỳ Miễn → 0
- [x] Test 5 — 10% (10d) + LT (20d) → 1.203.760 (533K + 670K)
- [x] Test 6 — 10% (5d) + gap LT (14d) + 20% (11d) → 1.804.299 (267K + 1.173K + 364K)
- [ ] PHPUnit test thật — để sau (smoke đủ cover logic)

### Task 7.7 — FE: Tab "Thuế TNCN" trên màn nhân viên ✅

**File tạo:**
- `components/human-components/employee_info/EmployeeTaxTab.vue`

**File sửa:**
- `components/human-components/employee_info/EmployeeInfoForm.vue` — import + mount tab mới sau tab "Thông tin thu nhập và bảo hiểm" (chỉ hiện khi `id` đã tồn tại)

- [x] Bảng inline edit: STT | Loại thuế | Từ ngày | Đến ngày | Action
- [x] Dropdown 4 loại: Miễn / Lũy tiến / 10% / 20%
- [x] DatePicker `start_date`, `end_date` (nullable, hiển thị "Vô cực" nếu trống)
- [x] Auto-set end_date của row đang mở khi thêm row mới (tránh overlap)
- [x] Gọi `apiGet`/`apiPostMethod`/`apiPutMethod`/`apiDelete`

### Task 7.8 — Test E2E đa đoạn

- [ ] Tạo NV có 2 row tax: 01–10/04 = 10%, 11–30/04 = Lũy tiến
- [ ] Chạy bảng lương tháng 04 → verify số thuế = tax_10 + tax_lt
- [ ] Verify đoạn 10% không trừ giảm trừ
- [ ] Verify đoạn lũy tiến hưởng full 11tr + NPT
- [ ] Test backward compat: NV không có row nào → kết quả khớp behavior cũ

---

## Phase 11 — Cột "Thu nhập tính thuế" (composition INFO)

> **Mục tiêu:** Thêm cột hiển thị thu nhập tính thuế của đoạn lũy tiến (= thu nhập chịu thuế prorate − BHXH − công đoàn − giảm trừ bản thân − NPT, clamp ≥ 0). Kiểu INFO feature=3 giống Phase 8, đoạn 10%/20% → 0.

### Task 11.1 — BE: Mở rộng `TaxCalculator::breakdown()` trả `taxable` ✅

**File sửa:**
- `Modules/Payroll/Helpers/TaxCalculator.php`

- [x] Refactor: tách `aggregateSegments()` (đi segment → progressiveDays/Income + fixedTax) và `progressiveDeductions()` (insurance/union/self/npt/taxable) dùng chung cho `calc()` + `breakdown()` — bỏ trùng lặp với `calcProgressivePortion()` cũ
- [x] `breakdown()` trả thêm key `taxable` (đã clamp ≥ 0)
- [x] `calc()` dùng helper mới, giữ nguyên kết quả (verify smoke test)

### Task 11.2 — BE: Migration insert composition `THU_NHAP_TINH_THUE` ✅

**File tạo:**
- `Modules/Payroll/Database/migrations/2026_06_18_100001_insert_thu_nhap_tinh_thue_composition.php`

- [x] `type=7, feature=3 (INFO), value_type=2, tax_deduction=false, is_show_paycheck=true, status=1` (check tồn tại theo code)
- [x] Down: delete theo code
- [x] Migrate → verify row OK

### Task 11.3 — BE: `SalaryService::calcData()` thêm case ✅

**File sửa:**
- `Modules/Payroll/Services/SalaryService.php`

- [x] Thêm `'THU_NHAP_TINH_THUE'` vào `$tncnCodes`
- [x] `case 'THU_NHAP_TINH_THUE': return $bd['taxable'];`

### Task 11.4 — Smoke test ✅

- [x] TN chịu thuế 16tr, không BHXH/CĐ/NPT → taxable=5.000.000, thuế=250.000 (5tr×5%)
- [x] TN 10tr < giảm trừ 11tr → taxable=0 (clamp)
- [x] Verify `calc()` không đổi kết quả sau refactor

### Task 11.5 — Test E2E (chờ user)

- [ ] Thêm composition `THU_NHAP_TINH_THUE` vào salary template (FE đã có sẵn cơ chế hiển thị composition INFO — không cần code FE mới)
- [ ] Tạo bảng lương → verify cột "Thu nhập tính thuế" hiển thị đúng
- [ ] Verify cột KHÔNG cộng vào total_income/total_deduction/thuc_linh

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

### Checkpoint — 2026-05-27 (Phase 8/9/10 + tinh chỉnh)
Vừa hoàn thành:
- **Phase 8 (4 cột giảm trừ):** Tạo 3 system composition `GIAM_TRU_BAN_THAN`, `GIAM_TRU_NPT`, `GIAM_TRU_BHXH_TNCN` (feature=3 INFO). `TaxCalculator::breakdown()` trả `[self, npt, bhxh]`. Tổng giảm trừ KHÔNG còn system — user tự tạo custom với formula `GIAM_TRU_BAN_THAN + GIAM_TRU_NPT + GIAM_TRU_BHXH_TNCN`.
- **Phase 9 (Config global):** Consolidate `tncn_tax_configs` còn 1 row chuẩn (self=11M). Bỏ filter `company_id` trong TaxCalculator + InsuranceConfig query + TncnTaxConfigService. Tham số `$companyId` trong helper giờ là legacy.
- **Phase 10 (Quy ước nghiệp vụ — KHÁC TT 111):**
  - Đoạn 10% và 20% cố định: base income = `probation_salary × D_seg/D_total × rate` (KHÔNG dùng total income chính thức)
  - BHXH cho mục đích TNCN = NLĐ (10.5%) + NSDLĐ (21.5%) = **32%** × `insurance_salary` — quyết định nội bộ doanh nghiệp để giảm thuế cho NV (chuẩn luật chỉ trừ phần NLĐ)
  - 6 test case PASS sau khi sửa
- **Tài liệu:** Cập nhật `design.md` + spec — ghi rõ 3 quy ước khác chuẩn + cách revert nếu muốn

Đang làm dở: Không

Bước tiếp theo:
- Anh test trên FE: tab Thuế TNCN của NV + 4 cột mới trên bảng lương
- E2E qua bảng lương thật (Task 7.8 + 8.5)
- Nếu công ty muốn đổi quy ước (BHXH chỉ NLĐ / 10%/20% không dùng probation / config theo company) → đọc design.md mục "Các quyết định lớn" để biết cách sửa

Blocked: Không

---

### Checkpoint — 2026-05-26 (Phase 7 — Đa đoạn tax_type)
Vừa hoàn thành:
- **Task 7.1 (DB):** Migration alter `employee_taxs` thêm `start_date`, `end_date` (nullable) + index `[employee_info_id, start_date]` — migrated OK
- **Task 7.2 (Entity + Request):** Cast date, validate non-overlap + chỉ row mới nhất được `end_date=NULL`
- **Task 7.3 (Service + Controller + Routes):** `EmployeeTaxService` thêm `listByEmployee/storeRow/updateRow`, tạo `EmployeeTaxController` + 4 routes `human/employee_tax/{GET,POST,PUT,DELETE}`
- **Task 7.4 (TaxCalculator):** Refactor signature `($empId, $h, $companyId, $periodStart, $periodEnd)`, dùng ngày dương lịch (D_total = ngày trong kỳ), `buildSegments()` cắt kỳ theo tax_type, gap → mặc định Lũy tiến, đoạn LT gộp lại để áp giảm trừ NGUYÊN THÁNG + BHXH/CD theo tỷ lệ ngày, đoạn 10%/20% áp gross
- **Task 7.5 (SalaryService):** Derive `periodStart/periodEnd` từ `apply_date` (đầu→cuối tháng), truyền vào TaxCalculator
- **Task 7.6 (Smoke test):** 6/6 case PASS qua tinker (full LT/10%/20%/Miễn/half-half/gap)
- **Task 7.7 (FE):** Tạo `EmployeeTaxTab.vue` (component riêng, gọi API trực tiếp), mount vào `EmployeeInfoForm.vue` thành tab mới "Thuế TNCN" sau tab thu nhập

Đang làm dở: Task 7.8 (E2E qua bảng lương thật) — chờ user chạy server FE để test

Bước tiếp theo:
1. Anh chạy FE → vào màn nhân viên → tab "Thuế TNCN" → thêm row tax_type=2 từ 01-10/04, row tax_type=1 từ 11/04 vô cực
2. Tạo bảng lương tháng 04 → verify số thuế hiển thị
3. Test edge: NV không có row → kết quả khớp behavior cũ

Blocked: Không
Lưu ý:
- Spec đã update: dùng **ngày dương lịch** (calendar days) thay vì working days — đơn giản, không phụ thuộc salary_calendar
- Backward compat: NV không có row `employee_taxs` → mặc định toàn kỳ Lũy tiến (giữ behavior trước Phase 7)
- Spell-check tiếng Việt báo nhiều warning trong TaxCalculator.php — bỏ qua

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
