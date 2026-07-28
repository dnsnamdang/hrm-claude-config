# Task 7 — Report

## STATUS: DONE

## File sửa
- `Modules/Decision/Http/Controllers/V1/DecisionLaborContractController.php`
- `Modules/Decision/Http/Controllers/V1/AppendixLaborContractController.php`

## Import Helper
- File 1 (`DecisionLaborContractController`): THÊM `use Modules\Human\Helper\Helper;` (trước đó chưa có).
- File 2 (`AppendixLaborContractController`): đã có sẵn (dòng 26), không đụng.

## Xác nhận tên mảng
- File 1 Khối 1 = method `print()` → dùng `$result`. ✔
- File 1 Khối 2 = method `prepareContractData()` → dùng `$data`. ✔
- File 2 method `print()` → dùng `$result`. ✔

---

## FILE 1 — KHỐI 1 (`print`, `$result`)

### (a) NGAY_HOP_DONG (composite giữ nguyên + thêm SO/CHU)
TRƯỚC:
```php
$result['NGAY_HOP_DONG'] = 'ngày ' . date('d', strtotime($decisionLaborContract->created_at)) . ' tháng ' . date('m', strtotime($decisionLaborContract->created_at)) . ' năm ' . date('Y', strtotime($decisionLaborContract->created_at));
```
SAU:
```php
$result['NGAY_HOP_DONG'] = 'ngày ' . date('d', strtotime($decisionLaborContract->created_at)) . ' tháng ' . date('m', strtotime($decisionLaborContract->created_at)) . ' năm ' . date('Y', strtotime($decisionLaborContract->created_at));
$result['NGAY_HOP_DONG_SO'] = Helper::formatDate($decisionLaborContract->created_at);
$result['NGAY_HOP_DONG_CHU'] = Helper::formatDateVICapital($decisionLaborContract->created_at);
```

### (b) NGAY_SINH (giữ nguyên + fillDateVariants keep)
TRƯỚC:
```php
$result['NGAY_SINH'] = Carbon::parse($decisionLaborContract->employeeInfo->birthday)->format('d-m-Y');
```
SAU:
```php
$result['NGAY_SINH'] = Carbon::parse($decisionLaborContract->employeeInfo->birthday)->format('d-m-Y');
Helper::fillDateVariants($result, 'NGAY_SINH', $decisionLaborContract->employeeInfo->birthday, 'keep');
```

### (c) NGAY_CAP_CMTND (giữ nguyên + fillDateVariants keep)
TRƯỚC:
```php
$result['NGAY_CAP_CMTND'] = Carbon::parse($decisionLaborContract->employeeInfo->grant_date)->format('d-m-Y');
```
SAU:
```php
$result['NGAY_CAP_CMTND'] = Carbon::parse($decisionLaborContract->employeeInfo->grant_date)->format('d-m-Y');
Helper::fillDateVariants($result, 'NGAY_CAP_CMTND', $decisionLaborContract->employeeInfo->grant_date, 'keep');
```

### (d) NGAY_HIEU_LUC (THAY dòng gốc)
TRƯỚC:
```php
$result['NGAY_HIEU_LUC'] = Carbon::parse($decisionLaborContract->start_date)->format('d/m/Y');
```
SAU:
```php
Helper::fillDateVariants($result, 'NGAY_HIEU_LUC', $decisionLaborContract->start_date, 'so');
```

### (e) THOI_HAN_HOP_DONG (composite giữ nguyên + thêm SO/CHU)
TRƯỚC:
```php
$result['THOI_HAN_HOP_DONG'] = 'Từ ngày ' . Carbon::parse($decisionLaborContract->start_date)->format('d') . ' tháng ' . Carbon::parse($decisionLaborContract->start_date)->format('m') . ' năm ' . Carbon::parse($decisionLaborContract->start_date)->format('Y') .
    ' đến ngày ' . Carbon::parse($decisionLaborContract->end_date)->format('d') . ' tháng ' . Carbon::parse($decisionLaborContract->end_date)->format('m') . ' năm ' . Carbon::parse($decisionLaborContract->end_date)->format('Y');
```
SAU (thêm ngay dưới):
```php
$result['THOI_HAN_HOP_DONG_SO'] = 'Từ ngày ' . Helper::formatDate($decisionLaborContract->start_date) . ' đến ngày ' . Helper::formatDate($decisionLaborContract->end_date);
$result['THOI_HAN_HOP_DONG_CHU'] = 'Từ ' . Helper::formatDateVICapitalInline($decisionLaborContract->start_date) . ' đến ' . Helper::formatDateVICapitalInline($decisionLaborContract->end_date);
```
(THOI_HAN — diffInMonths — KHÔNG đụng.)

---

## FILE 1 — KHỐI 2 (`prepareContractData`, `$data`)

### (a) NGAY_HOP_DONG
TRƯỚC:
```php
$data['NGAY_HOP_DONG'] = 'ngày ' . date('d', strtotime($decisionLaborContract->created_at)) . ' tháng ' . date('m', strtotime($decisionLaborContract->created_at)) . ' năm ' . date('Y', strtotime($decisionLaborContract->created_at));
```
SAU:
```php
$data['NGAY_HOP_DONG'] = 'ngày ' . date('d', strtotime($decisionLaborContract->created_at)) . ' tháng ' . date('m', strtotime($decisionLaborContract->created_at)) . ' năm ' . date('Y', strtotime($decisionLaborContract->created_at));
$data['NGAY_HOP_DONG_SO'] = Helper::formatDate($decisionLaborContract->created_at);
$data['NGAY_HOP_DONG_CHU'] = Helper::formatDateVICapital($decisionLaborContract->created_at);
```

### (b) NGAY_SINH
TRƯỚC:
```php
$data['NGAY_SINH'] = Carbon::parse($decisionLaborContract->employeeInfo->birthday)->format('d-m-Y');
```
SAU:
```php
$data['NGAY_SINH'] = Carbon::parse($decisionLaborContract->employeeInfo->birthday)->format('d-m-Y');
Helper::fillDateVariants($data, 'NGAY_SINH', $decisionLaborContract->employeeInfo->birthday, 'keep');
```

### (c) NGAY_CAP_CMTND
TRƯỚC:
```php
$data['NGAY_CAP_CMTND'] = Carbon::parse($decisionLaborContract->employeeInfo->grant_date)->format('d-m-Y');
```
SAU:
```php
$data['NGAY_CAP_CMTND'] = Carbon::parse($decisionLaborContract->employeeInfo->grant_date)->format('d-m-Y');
Helper::fillDateVariants($data, 'NGAY_CAP_CMTND', $decisionLaborContract->employeeInfo->grant_date, 'keep');
```

### (d) NGAY_HIEU_LUC (THAY)
TRƯỚC:
```php
$data['NGAY_HIEU_LUC'] = Carbon::parse($decisionLaborContract->start_date)->format('d/m/Y');
```
SAU:
```php
Helper::fillDateVariants($data, 'NGAY_HIEU_LUC', $decisionLaborContract->start_date, 'so');
```

### (e) THOI_HAN_HOP_DONG (composite giữ nguyên + thêm SO/CHU)
SAU (thêm ngay dưới dòng gốc):
```php
$data['THOI_HAN_HOP_DONG_SO'] = 'Từ ngày ' . Helper::formatDate($decisionLaborContract->start_date) . ' đến ngày ' . Helper::formatDate($decisionLaborContract->end_date);
$data['THOI_HAN_HOP_DONG_CHU'] = 'Từ ' . Helper::formatDateVICapitalInline($decisionLaborContract->start_date) . ' đến ' . Helper::formatDateVICapitalInline($decisionLaborContract->end_date);
```

---

## FILE 2 — Appendix (`print`, mảng `$result`)

Tên biến nguồn:
- NGAY_HOP_DONG ← `$decisionContract->created_at` (`$decisionContract = DecisionLaborContract::find(...)`, có thể null)
- NGAY_SINH ← `$appendixLaborContract->birthday`
- NGAY_CAP_CMTND ← `$appendixLaborContract->grant_date`

### NGAY_HOP_DONG
TRƯỚC:
```php
$result['NGAY_HOP_DONG'] = $decisionContract ? Helper::formatDate($decisionContract->created_at) : '';
```
SAU (giữ null-guard cho `$decisionContract`):
```php
Helper::fillDateVariants($result, 'NGAY_HOP_DONG', $decisionContract ? $decisionContract->created_at : null, 'so');
```

### NGAY_SINH
TRƯỚC:
```php
$result['NGAY_SINH'] = Helper::formatDate($appendixLaborContract->birthday);
```
SAU:
```php
Helper::fillDateVariants($result, 'NGAY_SINH', $appendixLaborContract->birthday, 'so');
```

### NGAY_CAP_CMTND
TRƯỚC:
```php
$result['NGAY_CAP_CMTND'] = $appendixLaborContract->grant_date ? Helper::formatDate($appendixLaborContract->grant_date) : '';
```
SAU:
```php
Helper::fillDateVariants($result, 'NGAY_CAP_CMTND', $appendixLaborContract->grant_date, 'so');
```

---

## VERIFY (php -l)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/DecisionLaborContractController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/AppendixLaborContractController.php
```

## Concern
- File 2 NGAY_HOP_DONG: `$decisionContract` có thể null (find). Đã giữ null-guard bằng cách truyền `$decisionContract ? $decisionContract->created_at : null` để fillDateVariants (null-safe) không lỗi. Khi null, base `NGAY_HOP_DONG` = '' như logic cũ ('so' set base = formatDate(null) → '').
