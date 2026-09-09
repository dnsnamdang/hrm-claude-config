# Fix: TONG_VDM_QUY_DOI lệch 0.01 so với bảng công (nhánh tpe) — @namdangit

- [x] BE: `Modules/Payroll/Jobs/CreateEmployeePayroll.php` case `TONG_VDM_QUY_DOI` đọc thẳng `vdm_total` thay vì `round(total_overtime_minutes_after / 8, 2)` (2026-09-08)
  - Lý do: bảng công làm tròn từng nhóm hệ số rồi cộng; bảng lương cộng rồi chia 8 và cột `total_overtime_minutes_after` chỉ lưu 1 số thập phân → lệch 3.65 vs 3.66
- [ ] Chạy lại bảng lương 709 để kiểm tra khớp 3.66
