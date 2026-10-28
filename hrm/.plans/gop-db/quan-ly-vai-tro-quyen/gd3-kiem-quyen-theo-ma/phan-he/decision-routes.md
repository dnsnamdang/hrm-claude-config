# decision — đường đọc + mã (Task 8.7)

Mốc: 68 route × 6 tài khoản = 408 ô (hrm-api 8011 + ERP 8012, DB hrm_erp_rbac_rehearsal). Chụp bằng tests/Support/ScopeSnapshot.php.

## Tài khoản

- `pv4` · 13 — namdangit C1 — mọi mã decision.* Xem = 4, đủ manage/confirm/approve/import/mau_in
- `pv4_thieu` · 145 — C1 Xem = 4, KHÔNG quyet_dinh.approve / bien_ban.approve / phieu_bh.approve / quyet_dinh.import
- `pv3` · 522 — C4 mọi mã Xem = 3, đủ manage/confirm/approve
- `pv3_b` · 1190 — C9 Xem = 3 (thiếu dashboard, bao_cao_*, ho_tro_chi_phi, phieu_dang_ky_bh)
- `pv2` · 1189 — C9 Xem = 2 (danh mục khen thưởng = 3), confirm + manage, KHÔNG approve, KHÔNG mau_in
- `khong_ma` · 207 — 0 mã decision.*

Ca thiếu trên rehearsal: phạm vi 1 (0 người), có mã không phạm vi (0 người), khác công ty ⇒ PHPUnit (DecisionScopeCodesTest).

## Route

| app | url | mã | chuỗi phạm vi | cột lọc |
|---|---|---|---|---|
| api | decision/department-establishment | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/department-change | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/department-dissolution | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/decision-reward | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/decision-salary-bonus | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/manpower-planning | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/regulation-salary | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/accept-personnel | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/employee-discipline | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/appoint-personnel | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/transfer-personnel | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/renew-labor-contract | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/salary-change | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/assign-training | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/termination-labor-contract | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/retirement | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/suspend-labor-contract | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/increase-seniority | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | regulations/general | decision.quyet_dinh.view | có | DecisionService::filterDecision → checkPermissionList [4 tên,true] (4 · 3 company_id · 2 dept∪part∪created_by · 1 part∪created_by · else created_by; có customBuilder ⇒ đối tượng bị tác động) + status≠Đang tạo ∪ created_by |
| api | decision/department-dissolution/waiting-approve | decision.quyet_dinh.confirm|approve | không | type=waiting-approve: status theo Xem xét / Duyệt quyết định |
| api | decision/decision-reward/waiting-approve | decision.quyet_dinh.confirm|approve | không | type=waiting-approve: status theo Xem xét / Duyệt quyết định |
| api | decision/decision-salary-bonus/waiting-approve | decision.quyet_dinh.confirm|approve | không | type=waiting-approve: status theo Xem xét / Duyệt quyết định |
| api | decision/waiting-approve | decision.quyet_dinh.confirm|approve | không | WaitingApproveService: status theo Xem xét (Đã tạo) / Duyệt (Đã xem xét) |
| api | decision/labor-contract | decision.hop_dong_lao_dong.view | có | checkPermissionList [4 tên,false,false,true] ⇒ else labor_contract_employee_info_id = mình |
| api | decision/training-contract | decision.hop_dong_dao_tao.view | có | checkPermissionList [4 tên,true] |
| api | decision/appendix-labor-contract | decision.phu_luc_hop_dong_lao_dong.view | có | checkPermissionList [4 tên,true] |
| api | decision/insurance-out-company | decision.dang_ky_tham_gia_bao_hiem_ngoai_cong_ty.view | có | checkPermissionList [4 tên,true] |
| api | decision/insurance | decision.phieu_dang_ky_bao_hiem.view | có | checkPermissionList [4 tên,true] |
| api | decision/trouble-shooting-report | decision.bien_ban_xu_ly_su_co.view | có | checkPermissionList [4 tên,true] |
| api | decision/insurance-type | decision.danh_muc_loai_bao_hiem.view | có | checkPermissionList [4 tên,true] |
| api | decision/insurance-type | decision.danh_muc_loai_bao_hiem.view | không | cờ permissions.is_all_company/is_company |
| api | decision/operating-support | decision.ho_tro_chi_phi.view | có | checkPermissionList [2 tên,false,false,true] |
| api | decision/operating-support | decision.ho_tro_chi_phi.view | không | cờ permissions.is_all_company/is_company |
| api | decision/reward-type | decision.danh_muc_loai_khen_thuong.view | có | checkPermissionList cờ is_all_company/is_company (RewardTypeService tự lọc theo cờ) |
| api | decision/reward-type | decision.danh_muc_loai_khen_thuong.view | không | cờ permissions.is_all_company/is_company |
| api | decision/reward-mode | decision.danh_muc_hinh_thuc_khen_thuong.view | có | checkPermissionList [2 tên + 2 tên unknown,true] |
| api | decision/reward-mode | decision.danh_muc_hinh_thuc_khen_thuong.view | không | cờ permissions.is_all_company/is_company |
| api | decision/reward-title | decision.danh_muc_danh_hieu_khen_thuong.view | có | checkPermissionList [2 tên + 2 tên unknown,true] |
| api | decision/reward-title | decision.danh_muc_danh_hieu_khen_thuong.view | không | cờ permissions.is_all_company/is_company |
| api | decision/insurance-packages | decision.danh_muc_goi_bao_hiem.view | có | checkPermissionList [2 tên,false,false,true] |
| api | decision/incident-type | decision.danh_muc_loai_su_co.view | có | checkPermissionList [2 tên,false,false,true] |
| api | decision/incident-type | decision.danh_muc_loai_su_co.view | không | cờ permissions.is_all_company/is_company |
| api | decision/report/insurance-register | decision.bao_cao_dang_ky_bao_hiem.view | có | checkPermissionList [4 tên,true] bảng insurance_registers |
| api | decision/report/regulation-salary | decision.bao_cao_thang_bang_luong.view | có | checkPermissionList [2 tên,false,false,false] ⇒ else whereNull |
| api | decision/report/out-company-single-employee-insurance | decision.bao_cao_dang_ky_bao_hiem.view | có | checkPermissionList [4 tên,true] |
| api | decision/report/out-company-group-employee-insurance | decision.bao_cao_dang_ky_bao_hiem.view | có | checkPermissionList [4 tên,true] |
| api | decision/dashboard/issued | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/labor-contract-effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/training-contract-effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/waiting-approve | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/not-approve | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/unfinished | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/expired-soon | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/organizational-structure | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/personnel | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/administration | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/ratio-decisions | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/list-labor-contract-effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/list-training-contract-effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/all-decisions-by-time | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/detail-issued | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| api | decision/dashboard/detail-effective | decision.dashboard_quyet_dinh.view | có | checkPermissionListWithCompanyFilter [4,3,2 dashboard] (4 = công ty quản lý được; 3 company; 2 dept∪part∪created_by); không quyền ⇒ viewerScope; waiting-approve thêm Quản lý/Duyệt/Xem xét |
| erp | admin/report_templates | decision.mau_in.manage | không | middleware checkPermission (status; trang không quyền = -1) |
| erp | admin/report_templates/searchData | decision.mau_in.manage | không | middleware checkPermission (status; trang không quyền = -1) |
| erp | admin/print-templates | decision.mau_in.manage | không | middleware checkPermission (status; trang không quyền = -1) |
| erp | admin/print-templates/searchData | decision.mau_in.manage | không | middleware checkPermission (status; trang không quyền = -1) |
| erp | admin/print-template-variables/get-variables | decision.mau_in.manage | không | middleware checkPermission (status; trang không quyền = -1) |
