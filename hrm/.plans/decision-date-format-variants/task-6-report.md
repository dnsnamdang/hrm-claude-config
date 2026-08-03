# Task 6 — Report

## STATUS: DONE

## File đã sửa
- `Modules/Decision/Http/Controllers/V1/EmployeeDisciplineController.php`
- `Modules/Decision/Http/Controllers/V1/DecisionRegulationSalaryController.php`

## 1) EmployeeDisciplineController.php — method `print()`

### (a) THOI_GIAN_KY_LUAT (composite khoảng) — biểu thức GỐC thực tế
Biến nguồn: `$employeeDiscipline->from_date` / `$employeeDiscipline->to_date` (KHÔNG phải `$from`/`$to`).

Biểu thức gốc (dòng ~156, nằm trong `if ($employeeDiscipline->from_date && $employeeDiscipline->to_date)`):
```php
$result['THOI_GIAN_KY_LUAT'] = 'Kể từ ngày ' . Helper::formatDate($employeeDiscipline->from_date) . ' đến ngày ' . Helper::formatDate($employeeDiscipline->to_date);
```
Nhánh else gốc: `$result['THOI_GIAN_KY_LUAT'] = '';`

Sau khi sửa:
```php
if ($employeeDiscipline->from_date && $employeeDiscipline->to_date) {
    $result['THOI_GIAN_KY_LUAT'] = 'Kể từ ngày ' . Helper::formatDate($employeeDiscipline->from_date) . ' đến ngày ' . Helper::formatDate($employeeDiscipline->to_date); // GIỮ NGUYÊN
    $result['THOI_GIAN_KY_LUAT_SO'] = 'Kể từ ngày ' . Helper::formatDate($employeeDiscipline->from_date) . ' đến ngày ' . Helper::formatDate($employeeDiscipline->to_date);
    $result['THOI_GIAN_KY_LUAT_CHU'] = 'Kể từ ' . Helper::formatDateVICapitalInline($employeeDiscipline->from_date) . ' đến ' . Helper::formatDateVICapitalInline($employeeDiscipline->to_date);
} else {
    $result['THOI_GIAN_KY_LUAT'] = '';
    $result['THOI_GIAN_KY_LUAT_SO'] = '';
    $result['THOI_GIAN_KY_LUAT_CHU'] = '';
}
```
- Dòng gốc giữ y nguyên; _SO copy y hệt biểu thức gốc; _CHU dùng `formatDateVICapitalInline` với chữ "ngày" thường trong câu ("Kể từ ... đến ...").
- Bổ sung set `_SO`/`_CHU` = `''` trong nhánh else để đồng bộ khi thiếu ngày.

### (b) NGAY_SA_THAI (ngày đơn)
- Biến nguồn: `$employeeDiscipline->dismissal_date`
- Dòng trước: kết thúc block THOI_GIAN_KY_LUAT
- Gốc: `$result['NGAY_SA_THAI'] = $employeeDiscipline->dismissal_date ? Helper::formatDate($employeeDiscipline->dismissal_date) : '';`
- Sau:
```php
if ($employeeDiscipline->dismissal_date) {
    Helper::fillDateVariants($result, 'NGAY_SA_THAI', $employeeDiscipline->dismissal_date, 'so');
} else {
    $result['NGAY_SA_THAI'] = '';
}
```
- Dòng sau: `$result['SO_THANG_CHAM_TANG_LUONG'] = ...`
- Lưu ý: giữ null-guard gốc (dismissal_date có thể null). Khi có ngày dùng fillDateVariants 'so' → set NGAY_SA_THAI + NGAY_SA_THAI_SO + NGAY_SA_THAI_CHU.

### (c) NGAY_XAY_RA (ngày đơn)
- Biến nguồn: `$report->incident_date` (trong block `if ($employeeDiscipline->trouble_shooting_report_id)`)
- Dòng trước: `$result['LOAI_SU_CO'] = ...;`
- Gốc: `$result['NGAY_XAY_RA'] = Helper::formatDate($report->incident_date);`
- Sau: `Helper::fillDateVariants($result, 'NGAY_XAY_RA', $report->incident_date, 'so');`
- Dòng sau: `$result['NOI_XAY_RA'] = $report->incident_address;`

## 2) DecisionRegulationSalaryController.php — method `print()`

### NGAY_QUYET_DINH (ngày đơn)
- Biến nguồn: `$decisionRegulationSalaryAll->decision->effective_date`
- Dòng trước: `$result['SO_QUYET_DINH'] = $decisionRegulationSalaryAll->decision->code;`
- Gốc (dòng ~129): `$result['NGAY_QUYET_DINH'] = date('d/m/Y', strtotime($decisionRegulationSalaryAll->decision->effective_date));`
- Sau: `Helper::fillDateVariants($result, 'NGAY_QUYET_DINH', $decisionRegulationSalaryAll->decision->effective_date, 'so');`
- Dòng sau: `$result['TEN_CONG_TY'] = $decisionRegulationSalaryAll->decision->company->name;`
- Đã THÊM `use Modules\Human\Helper\Helper;` (file trước đó chưa import). EmployeeDisciplineController đã có sẵn import (dòng 24).

## VERIFY (php -l)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/EmployeeDisciplineController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/DecisionRegulationSalaryController.php
```

## Concern
- NGAY_SA_THAI: task chỉ yêu cầu gọi thẳng fillDateVariants, nhưng gốc có null-guard (dismissal_date nullable). Đã giữ guard bằng if/else để tránh fillDateVariants xử lý null (giữ nguyên hành vi cũ khi thiếu ngày → chuỗi rỗng). Nếu reviewer muốn gọi thẳng không guard thì cần xác nhận hành vi fillDateVariants với input null.
