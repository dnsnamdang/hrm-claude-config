# Sửa base "Tổng TNS lũy tiến" (quyết toán thưởng NS quý)

## Yêu cầu (user chốt)
Ở **dòng nhân viên**, cột **"Tổng TNS lũy tiến"** (base để tính lũy tiến → phân chia thưởng thêm) phải **cộng thêm** phần TNS tháng + quý mà HĐ của NV đóng góp cho **TBP + TP** (`commission_month/quarter_part_lead` + `..._dept_lead`). → base lớn hơn → thưởng thêm + phân chia lớn hơn.

Phương án **A**: KHÔNG đụng "Tổng thu nhập" NV. Thu nhập NV = **Thưởng TH HĐ (commission_cost) + TNS tháng NV + TNS quý NV + Phân chia thưởng thêm NV** — chỉ phần own.

## Thiết kế
- Tách rõ: `sum_commission_employee` = **own** (tháng+quý NV) — giữ nguyên, dùng cho thu nhập & downstream. `sum_tns_luy_tien` = own + đóng góp TBP/TP (chỉ role='employee') — dùng làm base lũy tiến + hiển thị cột "Tổng TNS lũy tiến".
- Chỉ áp cho `role='employee'`; TP/TBP giữ nguyên.

## Tasks
- [ ] FE class `BillProductivitySettlementQuarterEmployee.blade.php`: getter `sum_tns_luy_tien` = sum_commission_employee + (nếu employee) đóng góp part_lead+dept_lead (tháng+quý). Getter income giữ dùng `sum_commission_employee`.
- [ ] Cột "Tổng TNS lũy tiến" đổi `sum_commission_employee` → `sum_tns_luy_tien`: `form.blade.php` (225, 281) + `show.blade.php` (nếu có).
- [ ] BE `BillProductivitySettlementQuarter::syncEmployees()`: `$sum_own` (own) + `$sum_luy_tien` (own + đóng góp TBP/TP từ contracts, chỉ employee). tier dùng `$sum_luy_tien`; `sum_commission_employee` lưu `$sum_own`; `sum_income_quarter` dùng `$sum_own`.
- [ ] `php -l` + user test số liệu.

## File
- `resources/views/partials/classes/accounting/BillProductivitySettlementQuarterEmployee.blade.php`
- `resources/views/accounting/bill_productivity_settlement_quarters/form.blade.php` (+ show.blade.php)
- `app/Model/Accounting/BillProductivitySettlementQuarter.php`
