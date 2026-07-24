# Task 4 — Report: Bổ sung 9 biến HSNS cho QĐ Chấm dứt & Tạm hoãn HĐLĐ

## STATUS: DONE

## File đã sửa
1. `Modules/Decision/Http/Controllers/V1/TerminationLaborContractController.php` — 1 khối
2. `Modules/Decision/Http/Controllers/V1/SuspendLaborContractController.php` — CẢ 2 khối

## Chi tiết chèn

### Termination — 1 khối (`print()`)
- Khối `print()` bắt đầu tại dòng 162.
- `$info = $terminationLaborContract->terminationEmployeeInfo;` ĐÃ có sẵn ở dòng 181 (không gán lại).
- Chèn 9 biến MỚI TRƯỚC `fillReport(...)`.
- Tên mảng biến: `$result`. Biến info dùng: `$info` (có sẵn).

### Suspend — CẢ 2 khối
- Khối `print()` bắt đầu dòng 119. Chèn TRƯỚC `fillReport($suspendLaborContract->decision->print_template, $result)`.
- Khối `printAgreement()` bắt đầu dòng 167. Chèn TRƯỚC `fillReport($suspendLaborContract->print_template_agreement, $result)`.
- Tên mảng biến cả 2 khối: `$result`.
- Biến info: cả 2 khối gán mới `$info = $suspendLaborContract->employeeInfo;` (bảng snapshot không có các cột này, phải lấy qua quan hệ). `$info` chưa được dùng ở cả 2 khối nên dùng tên `$info` nhất quán, không ghi đè logic cũ (khối `print()` dùng `$suspendLaborContract->employeeInfo` inline cho `$trinhDoHocVan` chứ không đặt biến `$info`).

## 9 biến MỚI được thêm (không thêm lại NGAY_SINH/NOI_CU_TRU/CCCD/TRINH_DO_HOC_VAN)
GIOI_TINH, NOI_CAP_CMTND, NGAY_CAP_CMTND (fillDateVariants 'so'), DIA_CHI_THUONG_TRU, CHUYEN_NGANH, QUE_QUAN, QUOC_TICH, DIEN_THOAI, THOI_GIAN_HDLD_HIEN_TAI (fillDateVariants 'so').

## Cách lấy THOI_GIAN_HDLD_HIEN_TAI
Lấy `start_date` của HĐLĐ hiện tại qua FQN đầy đủ:
`optional(\Modules\Decision\Entities\DecisionLaborContract\DecisionLaborContract::find($xxx->labor_contract_id))->start_date`
rồi truyền vào `Helper::fillDateVariants($result, 'THOI_GIAN_HDLD_HIEN_TAI', $startHdld, 'so')`.
- Termination: `$terminationLaborContract->labor_contract_id`
- Suspend (cả 2 khối): `$suspendLaborContract->labor_contract_id`

## Verify (php -l)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/TerminationLaborContractController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/SuspendLaborContractController.php
```

## Concern
- `use Modules\Human\Helper\Helper;` đã có sẵn ở cả 2 file (Termination dòng 22, Suspend dòng 15). Không cần `use` cho DecisionLaborContract vì dùng FQN.
- Chưa xác minh runtime tên cột (`grant_location`, `grant_date`, `home_town`, `national`, `personal_telephone`, `telephone`, `gender`) trên model EmployeeInfo và quan hệ `employee_educations` — dùng đúng theo spec task. Đều null-safe nên không gây lỗi runtime kể cả khi $info null.
