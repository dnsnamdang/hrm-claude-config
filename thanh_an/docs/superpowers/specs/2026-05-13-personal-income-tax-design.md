# Spec — Tính Thuế TNCN trong bảng lương

**Ngày:** 2026-05-13
**Module:** Payroll (BE) + Human (FE settings)
**Owner:** @khoipv

---

## 1. Mục tiêu

Hoàn thiện logic tính Thuế Thu Nhập Cá Nhân (TNCN) trong flow tính bảng lương theo luật VN, áp dụng biểu lũy tiến 7 bậc, tự động trừ vào tổng khấu trừ để ra thực lĩnh.

**Phạm vi MVP:**
- Áp **biểu lũy tiến** cho mọi nhân viên (mặc định) HOẶC theo loại thuế khai báo trong `employee_taxs`.
- Hỗ trợ **đa-đoạn-tax-type trong cùng 1 kỳ lương** (vd: 01–10/04 chịu 10% cố định, 11–30/04 chịu lũy tiến). Thực hiện bằng cách cho phép `employee_taxs` có nhiều row theo khoảng ngày (`start_date`, `end_date`). Xem [Section 9](#9-đa-đoạn-tax-type-trong-một-kỳ-lương).
- **Đoạn lũy tiến** — base = `sumTaxableIncome($h)` (tổng các phần lương có cờ `*_tax=1`):
  - Trừ trước thuế: BHXH **(NLĐ 10.5% + NSDLĐ 21.5% = 32%)** × `insurance_salary` + Công đoàn 1% × `insurance_salary` + giảm trừ bản thân 11M (nguyên tháng) + giảm trừ NPT 4.4M × số NPT (nguyên tháng).
  - BHXH/CĐ chia tỷ lệ ngày theo `D_lt/D_total`.
- **Đoạn 10% / 20% cố định** — base = `probation_salary`:
  - Công thức: `probation_salary × D_seg / D_total × rate`.
  - KHÔNG giảm trừ.
- **Đoạn Miễn** (`tax_type=0`): thuế = 0.
- **Config global:** `tncn_tax_configs` + `insurance_configs` chỉ giữ 1 row dùng chung cho mọi company. Query bỏ filter `company_id`.
- Composition `THUE_TNCN` (feature=2 KHẤU TRỪ) tự cộng vào `total_deduction` → **không sửa công thức `thuc_linh = total_income - total_deduction - advance`**.

**⚠️ QUY ƯỚC KHÁC LUẬT (cần biết để revert nếu muốn):**

| Quy ước hiện tại | Chuẩn TT 111/2013 | Lý do chọn |
|---|---|---|
| BHXH giảm trừ = NLĐ + NSDLĐ (32%) | Chỉ NLĐ (10.5%) | Doanh nghiệp muốn giảm thuế cho NV bằng cách trừ luôn phần công ty đóng. Revert: bỏ `$employerRate` trong `calcInsuranceDeduction()`. |
| Đoạn 10% / 20% dùng `probation_salary` | 10% dùng thu nhập từ HĐ vụ việc; 20% dùng thu nhập của NV không cư trú | Codebase này dùng cả 2 loại cho case thử việc / HĐ ngắn hạn. Revert 20%: switch case trong `calc()` đổi sang `totalIncome`. |
| `tncn_tax_configs` global | Có thể khác giữa các công ty (hiếm) | Tất cả công ty trong hệ thống đều ở VN, áp cùng luật. Revert: thêm lại filter `where('company_id', ...)` trong helper + service. |

**Ngoài phạm vi:**
- Thuế cho intern/probation (đã có `tax_generals.intern_tax_type` / `probation_tax_type` riêng).
- Quyết toán thuế cuối năm.
- Thuế TNCN được hoàn / Thuế TNCN khấu trừ thêm.

---

## 2. Cấu trúc hiện tại (context đã khảo sát)

### 2.1. Composition `THUE_TNCN`

Trong `SystemSalaryCompositionSeeder.php` đã có định nghĩa nhưng bị comment:

```php
['id'=>39, 'name'=>'Thuế TNCN', 'code'=>'THUE_TNCN',
 'type'=>7 (Thuế TNCN), 'feature'=>2 (KHẤU TRỪ), 'value_type'=>2,
 'tax_deduction'=>false, 'is_show_paycheck'=>true, 'status'=>1]
```

→ Cần migration insert vào `system_salary_compositions` để các company hiện hữu có composition này.

### 2.2. Cờ thuế đã có

`employee_salary_histories` đã có các cờ boolean (mặc định false) đánh dấu khoản chịu thuế:
`p1_tax`, `p2_tax`, `p3_tax`, `seniority_tax`, `moving_expenses_tax`, `telephone_expenses_tax`, `other_allowances_tax`.

Phụ cấp động: `allowance_employee_salary_histories.is_tax` (1 = chịu thuế).

### 2.3. Cờ bảo hiểm + công đoàn

- `employee_salary_histories.has_insurance` (boolean) — có đóng BHXH không.
- `employee_salary_histories.has_union` (boolean) — có công đoàn không.
- `employee_salary_histories.insurance_salary` — lương đóng BH, đã được `EmployeeSalaryHistoryService` tính sẵn từ các phần `*_insurance = true`.

### 2.4. Tỷ lệ BHXH

Bảng `insurance_configs` lưu tỷ lệ NSDLĐ + NLĐ theo `date` hiệu lực (cấp company). Các cột NLĐ:
`worker_retire`, `worker_sick`, `worker_accident`, `worker_unemployment_insurance`, `worker_health_insurance`.

### 2.5. Phân loại thuế nhân viên

Bảng `employee_taxs` (1-1 với `employee_infos`):
- `tax_type`: 0=Miễn / 1=Lũy tiến / 2=10% / 3=20%.
- `family_allowance_type`: boolean (chưa rõ semantic, không dùng trong MVP).

### 2.6. Thân nhân

Bảng `employee_relationships`: lưu danh sách thân nhân (bố/mẹ/vợ chồng/con/anh chị em). Hiện **không** có cờ đánh dấu người phụ thuộc thuế → cần mở rộng.

### 2.7. Flow tính lương

Đi qua `Modules/Payroll/Services/SalaryService.php`, method `systemData($salary_composition_id, $employee_info_id, $salary_id)` (~dòng 1131) — đây là chỗ inject logic.

---

## 3. Schema DB

### 3.1. Bảng mới `tncn_tax_configs`

```php
Schema::create('tncn_tax_configs', function (Blueprint $table) {
    $table->id();
    $table->date('date')->comment('Ngày hiệu lực');
    $table->bigInteger('self_deduction')->default(11000000)
        ->comment('Giảm trừ bản thân (VND)');
    $table->bigInteger('dependent_deduction')->default(4400000)
        ->comment('Giảm trừ mỗi người phụ thuộc (VND)');
    $table->float('union_fee_rate')->default(1)
        ->comment('Tỷ lệ đoàn phí công đoàn NLĐ (%), mặc định 1% trên lương đóng BH');
    $table->bigInteger('company_id')->unsigned();
    $table->bigInteger('created_by')->unsigned();
    $table->bigInteger('updated_by')->unsigned()->nullable();
    $table->timestamps();
    $table->index(['company_id', 'date']);
});
```

### 3.2. Bảng mới `tncn_tax_brackets`

```php
Schema::create('tncn_tax_brackets', function (Blueprint $table) {
    $table->id();
    $table->bigInteger('tncn_tax_config_id')->unsigned()->index();
    $table->tinyInteger('level')->comment('Bậc 1-7');
    $table->bigInteger('from_amount')->comment('Từ (VND, inclusive)');
    $table->bigInteger('to_amount')->nullable()
        ->comment('Đến (VND, inclusive), null = không giới hạn');
    $table->float('rate')->comment('Thuế suất (%)');
    $table->timestamps();
});
```

**Quy ước:** brackets sort tăng theo `level`. `from_amount` của bậc N+1 = `to_amount` của bậc N + 1 (logic), tính toán dùng `from_amount` làm mốc trừ.

### 3.3. Mở rộng `employee_relationships`

```php
Schema::table('employee_relationships', function (Blueprint $table) {
    $table->boolean('is_dependent')->default(false)->after('relation')
        ->comment('Là người phụ thuộc giảm trừ thuế TNCN');
    $table->date('dependent_start_date')->nullable()->after('is_dependent')
        ->comment('Ngày bắt đầu giảm trừ');
    $table->date('dependent_end_date')->nullable()->after('dependent_start_date')
        ->comment('Ngày kết thúc giảm trừ (null = không giới hạn)');
});
```

Cập nhật `Modules/Human/Entities/EmployeeRelationship.php`: thêm `is_dependent`, `dependent_start_date`, `dependent_end_date` vào `$fillable`.

### 3.4. Migration insert composition `THUE_TNCN`

```php
// Cho từng company đang có records trong system_salary_compositions
DB::table('system_salary_compositions')->insertOrIgnore([
    'name' => 'Thuế TNCN',
    'code' => 'THUE_TNCN',
    'type' => 7,
    'feature' => 2,
    'value_type' => 2,
    'tax_deduction' => false,
    'is_show_paycheck' => true,
    'allow_to_exceed_quota' => false,
    'status' => 1,
    'description' => 'Tự động tính dựa trên biểu thuế lũy tiến từng phần và các cờ chịu thuế khai báo trong lịch sử lương nhân viên',
    'created_at' => now(), 'updated_at' => now(),
]);
```

### 3.5. Seed default cho `tncn_tax_configs`

Migration thứ 2 (chạy sau): với mỗi `company_id` có trong `companies`, insert 1 row config + 7 brackets:

| level | from_amount | to_amount | rate |
|-------|-------------|-----------|------|
| 1 | 0 | 5.000.000 | 5 |
| 2 | 5.000.000 | 10.000.000 | 10 |
| 3 | 10.000.000 | 18.000.000 | 15 |
| 4 | 18.000.000 | 32.000.000 | 20 |
| 5 | 32.000.000 | 52.000.000 | 25 |
| 6 | 52.000.000 | 80.000.000 | 30 |
| 7 | 80.000.000 | NULL | 35 |

Config: `date = '2020-07-01'`, `self_deduction = 11000000`, `dependent_deduction = 4400000`, `union_fee_rate = 1`.

---

## 4. Backend

### 4.1. Entities mới

- `Modules/Payroll/Entities/TncnTaxConfig.php` (extends BaseModel, relationship `hasMany TncnTaxBracket`).
- `Modules/Payroll/Entities/TncnTaxBracket.php` (extends BaseModel, `belongsTo TncnTaxConfig`).

### 4.2. Service + Controller + Request

Theo pattern `insurance_config` hiện có:

- `Modules/Payroll/Services/TncnTaxConfigService.php`
  - `index()` — list configs của company hiện tại + eager load brackets.
  - `save($attributes)` — upsert config + replace toàn bộ brackets trong transaction.
  - `delete($id)` — xóa cascade brackets.
- `Modules/Payroll/Http/Controllers/Api/V1/TncnTaxConfigController.php`
- `Modules/Payroll/Http/Requests/TncnTaxConfigRequest.php`
  - Validate: `date` required, `self_deduction` ≥ 0, `dependent_deduction` ≥ 0, `brackets` array có ít nhất 1 phần tử, mỗi bracket có `from_amount` ≥ 0, `rate` ∈ [0,100], `to_amount` (nếu có) > `from_amount`, không gap/overlap, bậc cuối có `to_amount = null`.

### 4.3. Routes (`Modules/Payroll/Routes/api.php`)

```php
Route::prefix('human/tncn_tax_config')->group(function () {
    Route::get('/', 'TncnTaxConfigController@index');
    Route::post('/', 'TncnTaxConfigController@store');
    Route::delete('{id}', 'TncnTaxConfigController@destroy');
});
```

### 4.4. Helper `TaxCalculator`

File: `Modules/Payroll/Helpers/TaxCalculator.php`

API:
```php
TaxCalculator::calc(
    int $employeeInfoId,
    EmployeeSalaryHistory $salaryHistory,
    int $companyId,
    string $periodDate  // YYYY-MM-DD, thường là ngày cuối kỳ lương
): int
```

**Pseudo code:** (xem Section 3 trong chat brainstorming — đã thống nhất)

Logic tóm tắt:
1. Lấy `EmployeeTax` của nhân viên. **Nếu không có row → mặc định coi tax_type = 1 (Lũy tiến).** Nếu có row và `tax_type !== 1` → return 0.
2. **Thu nhập chịu thuế** = sum các phần lương có cờ `*_tax = true` + sum phụ cấp động có `is_tax = 1`.
3. **Giảm trừ BHXH** = nếu `has_insurance` → `insurance_salary × (tỷ_lệ_NLĐ + tỷ_lệ_NSDLĐ) / 100` (lấy `insurance_configs` có `date ≤ periodDate` mới nhất, KHÔNG filter company).
   - Tỷ lệ NLĐ = `worker_retire + worker_sick + worker_accident + worker_unemployment_insurance + worker_health_insurance` (~10.5%)
   - Tỷ lệ NSDLĐ = `retire + sick + accident + unemployment_insurance + health_insurance` (~21.5%)
   - **Cộng cả 2 portion** theo quyết định nội bộ doanh nghiệp (khác TT 111 chuẩn).
4. **Giảm trừ công đoàn** = nếu `has_union` → `insurance_salary × tax_config.union_fee_rate / 100` (lấy từ config thuế hiệu lực ở bước 5).
5. **Pick config thuế** = `tncn_tax_configs` có `company_id` + `date ≤ periodDate` mới nhất. Nếu không có → return 0.
6. **Số người phụ thuộc** = count `employee_relationships` có `employee_info_id` + `is_dependent = true` + `(dependent_start_date IS NULL OR ≤ periodDate)` + `(dependent_end_date IS NULL OR ≥ periodDate)`.
7. **Thu nhập tính thuế** = thu_nhap_chiu_thue − BHXH NLĐ − công đoàn − self_deduction − (dependent_deduction × số NPT). Nếu ≤ 0 → return 0.
8. **Áp biểu lũy tiến** trên `brackets` (sort theo `level`):
   ```
   tax = 0
   for each bracket:
       if income <= bracket.from_amount: break
       upper = bracket.to_amount ?? income
       portion = min(income, upper) - bracket.from_amount
       if portion > 0: tax += portion * bracket.rate / 100
   ```
9. Trả về `(int) round(tax)`.

### 4.5. Tích hợp vào `SalaryService::systemData()`

Tại nhánh xử lý system composition, thêm case:

```php
$composition = SalaryComposition::find($salary_composition_id);
if ($composition && $composition->code === 'THUE_TNCN') {
    $salaryHistory = EmployeeSalaryHistory::where('employee_info_id', $employee_info_id)
        ->where('start_date', '<=', $periodDate)
        ->where(function ($q) use ($periodDate) {
            $q->whereNull('end_date')->orWhere('end_date', '>=', $periodDate);
        })
        ->orderByDesc('start_date')->first();
    if (!$salaryHistory) return 0;
    return TaxCalculator::calc(
        $employee_info_id, $salaryHistory, $companyId, $periodDate
    );
}
```

**Lưu ý:** Vì `TaxCalculator` tự lấy dữ liệu từ `insurance_configs` + `insurance_salary` (không đọc các row khác trong `salary_employee_data`), nên KHÔNG ràng buộc thứ tự với composition BHXH khác trong template.

---

## 5. Frontend

### 5.1. Màn `pages/human/settings/index.vue`

Thêm section mới phía dưới bảng BHXH:

**Bảng "Cấu hình thuế TNCN":**

| STT | Ngày hiệu lực | Giảm trừ bản thân | Giảm trừ mỗi NPT | Biểu thuế | Action |
|---|---|---|---|---|---|
| 1 | 07/2020 | 11.000.000 | 4.400.000 | [Xem 7 bậc] | [Sửa] [Xóa] |

- Nút `[+]` ở header → thêm row mới (date picker tháng/năm + 2 input số tiền + modal nhập brackets, pre-fill từ row gần nhất nếu có).
- Inline edit pattern giống bảng BHXH (edit / save / cancel / delete).
- Nút `[Xem 7 bậc]` mở modal hiển thị bảng brackets, có nút "Sửa" để chỉnh.

**Modal "Biểu thuế lũy tiến":**

| Bậc | Từ (VND) | Đến (VND) | Thuế suất (%) | Action |
|---|---|---|---|---|
| 1 | 0 | 5.000.000 | 5 | |
| ... | | | | |
| 7 | 80.000.000 | (Không giới hạn) | 35 | |

- Validate FE: bậc tiếp theo `from_amount` >= bậc trước `to_amount`, bậc cuối `to_amount = null`.
- Nút "Lưu tất cả" → POST cả config + brackets cùng lúc.

### 5.2. Màn nhân viên — tab "Quan hệ thân nhân"

Tìm file FE quản lý `employee_relationships` (xác định khi implement, dự kiến trong `pages/human/employees/...`). Bổ sung trong form/table:

| Họ tên | Quan hệ | Ngày sinh | **Người PT thuế** | **Từ ngày** | **Đến ngày** |
|---|---|---|---|---|---|
| Nguyễn A | Con trai | 2015-01-01 | ☑ | 2020-01-01 | (null) |

- `is_dependent` (checkbox).
- `dependent_start_date`, `dependent_end_date` (date picker, chỉ hiện khi `is_dependent = true`).
- BE Request validate: `is_dependent=true` → `dependent_start_date` required.

### 5.3. Hiển thị trên bảng lương / phiếu lương

Sau khi `THUE_TNCN` được thêm vào template lương (qua màn cấu hình salary_template), FE bảng lương + phiếu lương sẽ tự render dòng "Thuế TNCN" — **không cần code FE bảng lương riêng**.

---

## 6. Edge case & lưu ý

| # | Edge case | Hành xử |
|---|-----------|---------|
| 1 | Không tìm thấy `tncn_tax_configs` cho company tại period | Return 0 (không tính thuế, log warning). |
| 2 | `tax_type` của nhân viên ≠ 1 (Lũy tiến) cho TOÀN bộ kỳ | Áp công thức theo từng đoạn — xem [Section 9](#9-đa-đoạn-tax-type-trong-một-kỳ-lương). |
| 3 | `thu_nhap_tinh_thue ≤ 0` (sau giảm trừ) | Return 0. |
| 4 | Không có row `employee_taxs` cho nhân viên | **Mặc định coi như Lũy tiến (tax_type = 1)** — tính thuế bình thường. |
| 5 | `has_insurance = false` | Không trừ BHXH; vẫn tính thuế bình thường. |
| 6 | `has_union = false` | Không trừ công đoàn. |
| 7 | Người phụ thuộc có `dependent_end_date < periodDate` | Không đếm. |
| 8 | Sửa config thuế kỳ cũ (sau khi lương đã chốt) | Khuyến nghị: chỉ admin chỉnh, không tự tính lại lương cũ. Nếu muốn tính lại → unlock kỳ + tính lại lương thủ công. |
| 9 | Bracket rỗng (chưa nhập) | Validate ở Request, không cho lưu config. |
| 10 | Đoàn phí công đoàn không trần | Lấy tỷ lệ từ `tncn_tax_configs.union_fee_rate` (default 1%). Nếu cần trần theo lương cơ sở → ticket sau. |
| 11 | Phụ cấp động `is_tax=1` nhưng `is_show_paycheck=0` | Vẫn tính thuế (cờ thuế độc lập với cờ hiển thị). |

---

## 7. Plan thứ tự triển khai

1. **BE-DB:** 4 migration (2 bảng config + alter employee_relationships + insert composition + seed default).
2. **BE-CRUD config:** Entity + Request + Service + Controller + Routes.
3. **BE-Helper:** `TaxCalculator` + unit test (vài case: lũy tiến đủ 7 bậc, NPT = 0, NPT = 3, has_insurance=false, has_union=true, taxable=0).
4. **BE-Integration:** Inject vào `SalaryService::systemData()`, smoke test 1 kỳ lương.
5. **FE-Settings:** Section "Cấu hình thuế TNCN" + modal brackets.
6. **FE-Relationships:** 3 trường mới trong tab Quan hệ thân nhân.
7. **Test E2E:** Tạo 1 kỳ lương → verify số thuế khớp với ví dụ trong yêu cầu (6.975.000 → 447.500).

---

## 8. Câu hỏi mở (bổ sung sau khi cần)

- Thuế cho intern/probation (`tax_generals.intern_tax_type`) — flow tách riêng?
- Quyết toán thuế cuối năm (so sánh thu nhập 12 tháng so với biểu thuế năm) — feature lớn hơn, tách spec sau.
- Báo cáo thuế (Mẫu 05/KK-TNCN, 02/KK-TNCN) — tách spec sau.

---

## 9. Đa-đoạn-tax-type trong một kỳ lương

### 9.1. Bối cảnh

Nhân viên có thể đổi loại thuế giữa kỳ lương — vd: thử việc (10%) → chính thức (lũy tiến), hoặc NV nước ngoài đổi diện cư trú. Trước đây `employee_taxs` chỉ 1 row cố định → không cover được. Giải pháp: **mở rộng `employee_taxs` thành nhiều row theo khoảng ngày**, mỗi row có `tax_type` riêng, áp cho khoảng `[start_date, end_date]`.

### 9.2. Schema — alter `employee_taxs`

```php
// Migration: alter_employee_taxs_add_date_range.php
Schema::table('employee_taxs', function (Blueprint $table) {
    $table->date('start_date')->nullable()->after('tax_type')->comment('Ngày bắt đầu áp loại thuế này');
    $table->date('end_date')->nullable()->after('start_date')->comment('Ngày kết thúc (null = vô cực)');
    $table->index(['employee_info_id', 'start_date']);
});
```

- `start_date = NULL` → áp từ vô cực về trước.
- `end_date = NULL` → áp đến vô cực về sau.
- 1 NV có thể có nhiều row — **các khoảng không được overlap**, validate ở Request.
- Migration data: row cũ (nếu có) → set `start_date = NULL`, `end_date = NULL`.

### 9.3. Logic chia đoạn

```
periodStart = ngày đầu kỳ lương
periodEnd   = ngày cuối kỳ lương
D_total     = số ngày DƯƠNG LỊCH của kỳ (periodEnd - periodStart + 1)

1. Load tất cả EmployeeTax rows của NV có overlap với [periodStart, periodEnd], sort theo start_date.
2. Nếu không có row nào phủ hết kỳ → các khoảng trống mặc định tax_type=1 (Lũy tiến).
3. Cắt kỳ thành các segment_i = [seg_start_i, seg_end_i] theo từng tax_type liên tục.
4. Mỗi segment_i:
   - D_i = số ngày dương lịch trong [seg_start_i, seg_end_i]
   - income_i = thu_nhap_chiu_thue_ca_ky × D_i / D_total
   - Tính thuế segment_i theo tax_type tương ứng (xem 9.4)
5. tax_total = Σ tax_segment_i
```

**Lưu ý:**
- Dùng **ngày dương lịch** (không phải ngày công thực tế) để cắt đoạn — đơn giản, không phụ thuộc salary_calendar, khớp thực tiễn payroll VN.
- `thu_nhap_chiu_thue_ca_ky` lấy nguyên trên `EmployeeSalaryHistory` đang active tại `periodEnd` (giữ logic Cách A hiện tại). Việc chia theo ngày chỉ ảnh hưởng phân bổ thu nhập giữa các đoạn, không thay đổi tổng.

### 9.4. Công thức theo `tax_type`

| `tax_type` | Income base | Công thức cho đoạn |
|---|---|---|
| 0 (Miễn) | — | `tax_segment = 0` |
| 1 (Lũy tiến) | `sumTaxableIncome($h)` | `taxable = income_i − BHXH_i − union_i − self_deduction − dependent_deduction × NPT`<br>`tax_segment = apply_progressive(taxable)` nếu > 0, ngược lại 0 |
| 2 (10% cố định) | `probation_salary` | `tax_segment = probation_salary × D_seg / D_total × 10%` |
| 3 (20% cố định) | `probation_salary` | `tax_segment = probation_salary × D_seg / D_total × 20%` |

**Lưu ý:** Đoạn 10%/20% dùng `probation_salary` (lương thử việc) chứ KHÔNG dùng `totalIncome` chính thức. Phù hợp với case NV thử việc / HĐ ngắn hạn — nếu cần áp 20% cho NV nước ngoài không cư trú, sửa case 3 trong `TaxCalculator::calc()` đổi sang `totalIncome`.

**Quan trọng — giảm trừ bản thân + NPT theo TT 111/2013:**
- Giảm trừ áp **NGUYÊN THÁNG** vào đoạn lũy tiến đầu tiên trong kỳ (không chia theo tỷ lệ ngày).
- Nếu trong kỳ có nhiều đoạn lũy tiến không liên tục (hiếm) → cộng dồn `income_i` của tất cả đoạn lũy tiến rồi áp giảm trừ 1 lần.
- BHXH + công đoàn cũng tính 1 lần trên tổng `income_lt` (= Σ income_i của các đoạn lũy tiến), không chia theo ngày.

→ **Công thức gộp đoạn lũy tiến:**
```
income_lt = Σ income_i (i thuộc đoạn lũy tiến)
BHXH_lt   = insurance_salary × tỷ_lệ_BHXH × (D_lt / D_total)   nếu has_insurance
union_lt  = insurance_salary × union_rate × (D_lt / D_total)   nếu has_union
taxable   = income_lt − BHXH_lt − union_lt − 11tr − 4.4tr × NPT
tax_lt    = apply_progressive(max(taxable, 0))
```

Các đoạn 10% / 20% / Miễn vẫn tính độc lập theo bảng trên.

### 9.5. Cập nhật `TaxCalculator::calc(...)`

```php
TaxCalculator::calc(
    int $employeeInfoId,
    EmployeeSalaryHistory $salaryHistory,
    int $companyId,
    string $periodStart,   // YYYY-MM-DD ngày đầu kỳ
    string $periodEnd      // YYYY-MM-DD ngày cuối kỳ (cũng dùng để pick config)
): int
```

- Đổi signature: thay `$periodDate` bằng `$periodStart` + `$periodEnd`. D_total tự tính bằng số ngày dương lịch giữa 2 mốc.
- Trong `SalaryService::calcData()`: lấy `periodStart`, `periodEnd` từ salary record (`apply_date` cũ chính là `periodEnd`; `periodStart` lấy từ start_date của salary hoặc ngày 1 của tháng).

### 9.6. UI — Tab "Thuế TNCN" trên màn nhân viên

Thêm tab mới trong `pages/human/employees/[id].vue` (hoặc form NV), pattern giống `employee_salary_histories`:

| STT | Loại thuế | Từ ngày | Đến ngày | Ghi chú | Action |
|---|---|---|---|---|---|
| 1 | Lũy tiến | 2026-01-01 | (null) | Chính thức | [Sửa] [Xóa] |
| 2 | 10% | 2025-10-01 | 2025-12-31 | Thử việc | [Sửa] [Xóa] |

- Dropdown `tax_type`: Miễn / Lũy tiến / 10% / 20%.
- DatePicker `start_date`, `end_date` (nullable).
- Validate FE + BE: không overlap, `start_date ≤ end_date`.
- Không có row → mặc định Lũy tiến (giữ behavior cũ, backward compatible).

### 9.7. Use case: NV áp 1 loại thuế cố định, chưa biết ngày chuyển (open-ended)

Rất phổ biến: NV mới vào áp 10% cố định, chưa biết bao giờ lên chính thức để chuyển sang lũy tiến.

**Khi tạo NV:**

Tạo 1 row duy nhất trong `employee_taxs`:
```
tax_type    = 2 (10%)
start_date  = 2026-01-01   ← ngày bắt đầu áp
end_date    = NULL          ← vô cực, chưa biết khi nào dừng
```

Mỗi kỳ lương, `TaxCalculator` phủ row này lên `[periodStart, periodEnd]` → 1 segment duy nhất = toàn kỳ, tính `income × 10%`, không giảm trừ.

**Khi NV chuyển sang chính thức (vd: 2026-06-15):**

Thao tác trên UI tab thuế (Section 9.6):
1. Sửa row cũ → set `end_date = 2026-06-14`.
2. Thêm row mới → `tax_type=1`, `start_date=2026-06-15`, `end_date=NULL`.

Khuyến nghị UI: khi user bấm "Thêm dòng mới" và row gần nhất có `end_date=NULL`, **auto-set** `end_date = start_date_new − 1` để tránh báo lỗi overlap.

**Kỳ lương tháng giao thoa (06/2026):**

- Segment 1: `[06-01, 06-14]` — 14 ngày, tax_type=2 → `income × (14/D_total) × 10%`.
- Segment 2: `[06-15, 06-30]` — 16 ngày, tax_type=1 → gộp vào nhóm lũy tiến, hưởng FULL giảm trừ 11tr + NPT (theo Section 9.4), BHXH/CD chia tỷ lệ `16/D_total`.
- Tổng thuế kỳ này = tax_segment_1 + tax_segment_2.

**Validate Request:**

- Không cho overlap → buộc user phải close row cũ trước khi thêm row mới.
- `end_date = NULL` chỉ được phép ở row có `start_date` lớn nhất của NV (row "đang mở").

### 9.8. Edge case bổ sung

| # | Edge case | Hành xử |
|---|-----------|---------|
| 12 | Khoảng trống giữa 2 row `employee_taxs` (gap) | Đoạn gap mặc định Lũy tiến |
| 13 | Row `employee_taxs` overlap nhau | Validate Request không cho lưu |
| 14 | `start_date > periodEnd` hoặc `end_date < periodStart` | Bỏ qua row, không cắt đoạn |
| 15 | NV chuyển loại đúng ngày đầu/cuối kỳ | Đoạn 0 ngày → skip, không gây chia 0 |
| 16 | Toàn kỳ chỉ có 1 `tax_type` | Engine vẫn chạy qua flow chia đoạn — 1 segment duy nhất, kết quả khớp behavior cũ |
| 17 | `D_total = 0` (NV nghỉ cả kỳ) | Trả 0, không chia 0 |

---

## 10. Cột "Thu nhập tính thuế" (Phase 11)

**Mục tiêu:** Hiển thị thu nhập tính thuế của đoạn lũy tiến trên bảng lương như một cột thông tin.

### 10.1. Định nghĩa

```
THU_NHAP_TINH_THUE = max(0,
      thu nhập chịu thuế (prorate theo ngày đoạn lũy tiến)
    − BHXH (prorate ngày)
    − công đoàn (prorate ngày)
    − giảm trừ bản thân (nguyên tháng)
    − giảm trừ NPT (nguyên tháng) )
```

Đây CHÍNH là cơ sở (`taxable`) mà `TaxCalculator` đem áp biểu lũy tiến 7 bậc. Đoạn 10%/20% **không** đóng góp vào cột này (chúng tính thẳng trên `probation_salary`, không có khái niệm giảm trừ) → NV toàn kỳ 10%/20% thì cột = 0.

### 10.2. Kiểu composition

System composition INFO, giống nhóm Phase 8:

| Cột | Giá trị |
|---|---|
| `code` | `THU_NHAP_TINH_THUE` |
| `name` | Thu nhập tính thuế |
| `type` | 7 |
| `feature` | 3 (INFO — chỉ hiển thị, không cộng total) |
| `value_type` | 2 |
| `tax_deduction` | false |
| `is_show_paycheck` | true |
| `status` | 1 |

→ **KHÔNG** cộng vào `total_income` / `total_deduction` / `thuc_linh`. User tự kéo vào salary template khi cần.

### 10.3. Thực thi

1. **`TaxCalculator`** — refactor tách 2 private helper dùng chung cho `calc()` + `breakdown()`:
   - `aggregateSegments()`: đi qua segment → `progressiveDays`, `progressiveIncome` (prorate), `fixedTax` (10%/20%), `totalDays`.
   - `progressiveDeductions()`: trả `insurance`, `union`, `self`, `npt`, `taxable` (clamp ≥ 0).
   - `breakdown()` trả thêm key `taxable`. `calc()` giữ nguyên kết quả (chỉ tái cấu trúc nội bộ).
2. **Migration** `2026_06_18_100001_insert_thu_nhap_tinh_thue_composition.php` — insert composition (check tồn tại theo code).
3. **`SalaryService::calcData()`** — thêm code vào `$tncnCodes` + `case 'THU_NHAP_TINH_THUE': return $bd['taxable'];`.
4. **FE** — không code mới; tận dụng cơ chế hiển thị composition INFO sẵn có.

### 10.4. Smoke test (PASS)

| Case | taxable | thuế |
|---|---:|---:|
| TN chịu thuế 16tr, không BHXH/CĐ/NPT, toàn LT | 5.000.000 | 250.000 |
| TN 10tr < giảm trừ 11tr | 0 | 0 |
