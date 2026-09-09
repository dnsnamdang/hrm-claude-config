# Fix: tạo hồ sơ nhân sự báo "chưa có Mã check in cơm" (nhánh tpe, @namdangit)

Nguyên nhân: `EmployeeInfoController::store` chỉ mở transaction trên `mysql`, dòng `rice_employee_infos` (`mysql_tpe`) commit ngay → lần tạo hỏng để lại dòng mồ côi giữ `rice_ssn`; lần tạo lại trùng unique `rice_ssn`, lỗi bị nuốt trong try/catch tạo tài khoản → báo sai nguyên nhân. Server ETEK có 45 dòng mồ côi (id 1973 giữ 12609078 + 24 lần thử lại 07–08/09/2026).

## BE (worktrees/tpe-api)
- [x] `store()`: transaction trên cả `mysql` + `mysql_tpe` (helper begin/commit/rollBack), rollback cả khi validate fail
- [x] `store()`: bỏ try/catch nuốt lỗi tạo tài khoản; trùng `rice_employee_infos_rice_ssn_unique` → 422 "Mã check in cơm X đã tồn tại trên phân hệ Cơm…", lỗi khác ném ra ngoài
- [x] Tái hiện local (etek_prod_local + hrm_prod_local, parent 4) gọi thẳng controller: có mồ côi → 422 đúng message, không phát sinh dòng mới; không mồ côi → 200, rice_ssn = ssn
- [ ] Server: xoá dòng mồ côi `rice_company_id=4` có `employee_info_id` không tồn tại trong `hrm_etek.employee_infos` (SQL đã gửi), rồi tạo lại hồ sơ
- [ ] (Chưa làm, user chưa chốt) `syncFaceToRiceDevices`: bỏ qua máy cơm khi nhân sự không thuộc phân hệ Cơm
