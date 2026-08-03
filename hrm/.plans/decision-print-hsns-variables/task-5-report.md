# Task 5 — Biến THOI_GIAN_HDLD_HIEN_TAI

## STATUS: DONE

## File sửa
- `Modules/Decision/Http/Controllers/V1/DecisionLaborContractController.php`
  - Khối `print()` — mảng `$result`, sau dòng NGAY_HIEU_LUC (dòng ~163):
    `Helper::fillDateVariants($result, 'THOI_GIAN_HDLD_HIEN_TAI', $decisionLaborContract->start_date, 'so');`
  - Khối `prepareContractData()` — mảng `$data`, sau dòng NGAY_HIEU_LUC (dòng ~333):
    `Helper::fillDateVariants($data, 'THOI_GIAN_HDLD_HIEN_TAI', $decisionLaborContract->start_date, 'so');`
  - Đã sửa CẢ 2 khối (print=$result, prepareContractData=$data), nguồn `start_date`.
- `Modules/Decision/Http/Controllers/V1/AppendixLaborContractController.php`
  - Khối `print()` — mảng `$result`, sau dòng NGAY_HOP_DONG (dòng ~153).
  - Biến nguồn: `$decisionContract` (= DecisionLaborContract::find(decision_labor_contract_id)), bọc `optional()`:
    `Helper::fillDateVariants($result, 'THOI_GIAN_HDLD_HIEN_TAI', optional($decisionContract)->start_date, 'so');`

`use Modules\Human\Helper\Helper;` đã có sẵn ở cả 2 file.

## Verify
`php -l` cả 2 file → "No syntax errors detected" (2/2 pass).

## Concern
Không. Chỉ thêm biến mới, không đụng logic khác. Không commit git.
