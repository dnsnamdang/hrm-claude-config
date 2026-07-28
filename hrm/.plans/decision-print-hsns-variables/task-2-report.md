# Task 2 Report — Bổ sung 13 biến HSNS + 2 biến CAP_BAC vào 3 controller print()

## STATUS: DONE

## Files sửa
- `Modules/Decision/Http/Controllers/V1/AppointPersonnelController.php`
- `Modules/Decision/Http/Controllers/V1/TransferPersonnelController.php`
- `Modules/Decision/Http/Controllers/V1/SalaryChangeController.php`

## Chi tiết từng file

### AppointPersonnelController::print()
- Biến EmployeeInfo dùng: `$appoint_employee_info`
- Cách nạp: đã có sẵn dòng `$appoint_employee_info = EmployeeInfo::where('id', $decisionAppointPersonnel->appoint_employee->employee_info_id)->first();` (dòng 202) → trả về instance EmployeeInfo đầy đủ accessor/relation. Gán lại `$info = $appoint_employee_info;`. KHÔNG cần `EmployeeInfo::find` mới.
- Model cho CAP_BAC: `$decisionAppointPersonnel` (old_rank_name / new_rank_name)
- Vị trí chèn: sau `LUONG_P3` (dòng ~241 cũ), trước `fillReport(...)`.

### TransferPersonnelController::print()
- Biến EmployeeInfo dùng: `$transfer_employee_info`
- Cách nạp: đã có sẵn `$transfer_employee_info = EmployeeInfo::where('id', $decisionTransferPersonnel->transfer_employee->employee_info_id)->first();` (dòng 222) → instance EmployeeInfo. Gán `$info = $transfer_employee_info;`. KHÔNG cần find mới.
- Model cho CAP_BAC: `$decisionTransferPersonnel`
- Vị trí chèn: sau `LUONG_P3` trong method `print()`, trước `fillReport(...)`.
- Lưu ý: file còn method riêng `exportWord()` + `prepareContractData()` cũng build biến in nhưng Task 2 chỉ yêu cầu sửa `print()` — KHÔNG đụng vào các method đó (xem concern).

### SalaryChangeController::print()
- Biến EmployeeInfo dùng: `$transfer_employee`
- Cách nạp: đã có sẵn `$transfer_employee = EmployeeInfo::where('id', $salaryChange->salary_change_employee->employee_info_id)->first();` (dòng 180) → instance EmployeeInfo. Gán `$info = $transfer_employee;`. KHÔNG cần find mới.
- Model cho CAP_BAC: `$salaryChange`
- Vị trí chèn: sau `LUONG_P3`, trước `fillReport(...)`.

## Kiểm tra biến trùng
Đã audit toàn bộ 3 method `print()`: KHÔNG có biến nào trong 13+2 biến mới (NGAY_SINH, NGAY_CAP_CMTND, GIOI_TINH, CMTND, NOI_CAP_CMTND, DIA_CHI_THUONG_TRU, NOI_CU_TRU, QUE_QUAN, QUOC_TICH, CHUYEN_NGANH, TRINH_DO_HOC_VAN, DIEN_THOAI, MAIL, CAP_BAC_TRUOC_TD, CAP_BAC_SAU_TD) đã tồn tại trước đó. Không có dòng cũ nào bị bỏ.

## use Helper
Cả 3 file đã có sẵn `use Modules\Human\Helper\Helper;` — không cần thêm.

## Verify (php -l)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/AppointPersonnelController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/TransferPersonnelController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/SalaryChangeController.php
```

## Concern
- TransferPersonnelController có method `exportWord()` gọi `prepareContractData()` (build biến in cho xuất Word) — method này CHƯA có 13+2 biến HSNS mới. Task 2 chỉ yêu cầu sửa `print()`, nên `prepareContractData()` chưa được đụng đến. Nếu bản xuất Word cần cùng bộ biến, cần task bổ sung. (Ngoài ra `prepareContractData()` hiện có bug sẵn có: build vào `$result[...]` nhưng return `$data` — không thuộc phạm vi Task 2.)
- `$info` là instance EmployeeInfo đầy đủ (đã dùng chính biến `first()` sẵn có), nên accessor `full_address`/`full_address_residence` + relation `employee_educations` hoạt động bình thường.
