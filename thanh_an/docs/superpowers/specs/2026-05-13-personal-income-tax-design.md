# Spec — Tính Thuế TNCN trong bảng lương

**Ngày:** 2026-05-13
**Module:** Payroll (BE) + Human (FE settings)
**Owner:** @khoipv

---

## 1. Mục tiêu

Hoàn thiện logic tính Thuế Thu Nhập Cá Nhân (TNCN) trong flow tính bảng lương theo luật VN, áp dụng biểu lũy tiến 7 bậc, tự động trừ vào tổng khấu trừ để ra thực lĩnh.

**Phạm vi MVP:**
- Áp **biểu lũy tiến** cho mọi nhân viên (mặc định). Nếu nhân viên đã có row `employee_taxs` và `tax_type ≠ 1` (Miễn / 10% / 20%) → trả 0 (các case này bổ sung sau khi có UI khai báo).
- Bảng `employee_taxs` hiện đang rỗng → mọi nhân viên rơi vào nhánh mặc định = Lũy tiến.
- UI khai báo `employee_taxs` (dropdown chọn loại thuế từng NV) → **tách ticket sau**.
- Trừ trước thuế: BHXH/BHYT/BHTN NLĐ đóng (từ `insurance_configs`) + Đoàn phí công đoàn (từ `tncn_tax_configs.union_fee_rate`, default 1%) + giảm trừ bản thân + giảm trừ người phụ thuộc.
- Composition `THUE_TNCN` (feature=2 KHẤU TRỪ) được tự động cộng vào `total_deduction` → **không sửa công thức `thuc_linh = total_income - total_deduction - advance`**.

**Ngoài phạm vi:**
- Thuế cho intern/probation (đã có `tax_generals.intern_tax_type` / `probation_tax_type` riêng).
- Thuế suất 10% / 20% cố định.
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
3. **Giảm trừ BHXH NLĐ** = nếu `has_insurance` → `insurance_salary × (worker_retire + worker_sick + worker_accident + worker_unemployment_insurance + worker_health_insurance) / 100` (lấy `insurance_configs` có `date ≤ periodDate` mới nhất).
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
| 2 | `tax_type` của nhân viên ≠ 1 (Lũy tiến) — chỉ áp khi có row `employee_taxs` | Return 0 (MVP). |
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

- UI khai báo `employee_taxs` (dropdown Miễn / Lũy tiến / 10% / 20%) trên màn nhân viên — ticket riêng.
- Thuế cho `tax_type = 2` (10% cố định) và `tax_type = 3` (20% cố định) — áp trên gross hay trên taxable income?
- Thuế cho intern/probation (`tax_generals.intern_tax_type`) — flow tách riêng?
- Quyết toán thuế cuối năm (so sánh thu nhập 12 tháng so với biểu thuế năm) — feature lớn hơn, tách spec sau.
- Báo cáo thuế (Mẫu 05/KK-TNCN, 02/KK-TNCN) — tách spec sau.
