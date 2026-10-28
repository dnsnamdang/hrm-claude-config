# Mốc phân hệ human — đường đọc (Task 8.6)

Chụp bằng tests/Support/ScopeSnapshot.php (hrm-api :8011, DB hrm_erp_rbac_rehearsal). ERP: chỉ 1 chỗ (Employee::canOpenHrmAccountScreen → mục menu tài khoản HRM) — đo tay bằng curl đếm link `/admin/accounts` trên trang ERP (xem human-so-sanh.md).

## Tài khoản

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — mọi mã human.* Xem = 4, đủ mã manage/configure (tai_khoan.manage, cau_hinh.configure) |
| pv4_thieu | 145 | Xem = 4, ho_so_tu_khai.view = 3, KHÔNG tai_khoan.manage, KHÔNG cau_hinh.configure, không bao_cao... |
| pv2 | 148 | Xem = 2 (nhiem_vu, phan_cong, ho_so, nghi_viec, tu_khai, than_nhan, dinh_bien, quy_luong, bao_hiem, tai_khoan); không dinh_bien_theo_quy_mo / bao_cao phong ban / manage |
| pv2_b | 110 | như 148, phòng/bộ phận khác |
| khong_ma | 207 | 0 mã human.* |

Ca thiếu: phạm vi 1 (0 người giữ mã human.* ở mức 1), phạm vi 3 chỉ có ở ho_so_tu_khai.view (145), có mã không phạm vi (0 người), khác công ty ⇒ chỉ PHPUnit (HumanScopeCodesTest).

## Route

| id | method · url | mã | chuỗi phạm vi? | cột lọc / cách lấy |
|---|---|---|---|---|
| missions.index | GET human/missions | human.nhiem_vu.view | có | MissionService::index (override local) 4 tất cả · 3 missions.company_id · 2 departments ∈ phòng quản lý · else created_by (auto) |
| dm.index | GET human/department-manpowers | human.dinh_bien_theo_quy_mo.view | có | DepartmentManpowerService::index (override local) 4/3 company_id/2 department_id/else created_by; kết quả gom theo phòng (mảng) (auto) |
| dm.report | GET human/department-manpowers/report | human.bang_nhan_su_theo_dinh_bien.view + human.bang_nhan_su_va_quy_luong.view | có | DepartmentManpowerService::report: chuỗi 4/3/2/1 định biên + chuỗi 4/3/2 quỹ lương (employee_infos) + cờ permissions 4 khoá (auto) |
| dm.report.co | GET human/department-manpowers/report | human.bang_nhan_su_theo_dinh_bien.view | không | cờ is_* bảng nhân sự theo định biên (lists) |
| dm.assign | GET human/department-manpowers/assignment_missions | human.phan_cong_nhiem_vu.view | có | assignment_missions: chuỗi 4/3/2/1 employee_infos (override local) + cờ 4 khoá (auto) |
| dm.assign.co | GET human/department-manpowers/assignment_missions | human.phan_cong_nhiem_vu.view | không | cờ is_* (lists) |
| ei.index | GET human/employee-infos | human.ho_so_nhan_su.view | có | EmployeeInfoService::getEmployeeInfos → checkPermissionList 4 tên ho_so + true, bảng employee_infos (auto) |
| ei.index.co | GET human/employee-infos | human.ho_so_nhan_su.view + nhan_vien_nghi_viec.view | không | cờ permissions + permission_resigned (is_*) (lists) |
| ei.resigned | GET human/employee-infos | human.nhan_vien_nghi_viec.view | có | resigned=1 → checkPermissionList 4 tên nghỉ việc + true (auto) |
| euq.index | GET human/employee-update-requests | human.ho_so_tu_khai.view | có | EmployeeInfoUpdateRequestService: chuỗi 4/3/2/1 + else employee_info_id (auto) |
| euq.index.co | GET human/employee-update-requests | human.ho_so_tu_khai.view | không | cờ is_* (lists) |
| employee.index | GET human/employee | human.tai_khoan_nhan_vien.view | có | EmployeeService::getEmployees → applyAccountViewScope (checkPermissionList 4 tên + true, employee_infos) (auto) |
| employee.index.co | GET human/employee | human.tai_khoan_nhan_vien.view | không | cờ is_* (lists) |
| employee.personnel | GET human/employee/getPersonnel | human.than_nhan.view | có | EmployeeService::getPersonnel: cờ 4/3/2/1 đọc 1 lần, lọc phòng/bộ phận (auto) |
| employee.personnel.co | GET human/employee/getPersonnel | human.than_nhan.view | không | cờ is_* (lists) |
| company.report | GET human/companies/getDataForReport | human.bao_cao_danh_sach_phong_ban.view | có | CompanyService::getDataReport: 4 tất cả · 3 companies.id · else phòng của tôi (2 chỗ) (auto) |
| company.report.co | GET human/companies/getDataForReport | human.bao_cao_danh_sach_phong_ban.view | không | cờ is_all_company/is_company (lists) |
| ins.month | GET payroll/salary/insurance_report_month | human.bao_hiem_theo_thang.view | có | SalaryService::insurance_report_month chuỗi 4/3/2/1 employee_infos (auto) |
| ins.month.co | GET payroll/salary/insurance_report_month | human.bao_hiem_theo_thang.view | không | cờ is_* (lists) |
| ins.year | GET payroll/salary/insurance_report_year | human.bao_hiem_theo_nam.view | có | SalaryService::insurance_report_year chuỗi 4/3/2/1 (lists: data.departments + cờ) (lists) |
| salary.report | GET payroll/salary/report | human.bang_nhan_su_va_quy_luong.view | có | SalaryService::report chuỗi 4/3/2/1 employee_infos (auto) |
| accounts.index | GET admin/accounts | human.tai_khoan_nhan_vien.view|manage | có | middleware 5 tên + AccountService (applyAccountViewScope) + can_manage (auto) |
| accounts.index.co | GET admin/accounts | human.tai_khoan_nhan_vien.manage | không | cờ can_manage (lists) |
| accounts.show | GET admin/accounts/{id} | human.tai_khoan_nhan_vien.view | có | show ngoài phạm vi ⇒ 404 (detail) |
| selfnotif.index | GET human/self-notifications | human.thong_bao_noi_bo.manage | không | danh sách thông báo nội bộ, cờ canCreate từng dòng (hash content) (auto) |
| regcfg.departments | GET master-data/regulation-config-departments | human.cau_hinh.configure | không | middleware checkPermission:Cài đặt cấu hình (status 200/403) (auto) |
| regcfg.show | GET master-data/regulation-config/congno | human.cau_hinh.configure | không | middleware + guard() controller (auto) |
