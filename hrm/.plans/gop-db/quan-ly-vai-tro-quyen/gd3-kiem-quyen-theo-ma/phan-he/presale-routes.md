# presale — đường ĐỌC chụp mốc (Task 8.8)

Chỉ hrm-api (ERP 0 hit). API http://127.0.0.1:8011/api/v1, DB hrm_erp_rbac_rehearsal. Tài khoản:

- `pv4` = 13 — C1 mọi mã presale Xem = 4, đủ confirm/approve/create
- `pv4_thieu` = 145 — C1 Xem = 4 (không danh_sach_bao_gia), confirm, KHÔNG duyệt giá Bom
- `pv3` = 1190 — C9 Xem = 3, đủ confirm/approve TP+BGĐ
- `pv2` = 148 — C1 Xem = 2 (meeting NV = 3), confirm, TP duyệt giá
- `pv1` = 110 — C1 báo giá/YC GP/dự án/GP = 1, meeting NV = 3, không confirm/duyệt
- `khong_ma` = 207 — 0 mã presale.*

Ca thiếu: phạm vi 1 chỉ có ở 4 mã danh sách (110); có mã không phạm vi cho mã Xem phạm vi (0 người); khác công ty ⇒ PHPUnit.

| id | url | mã | chuỗi phạm vi? | cột lọc / ghi chú | extract |
|---|---|---|---|---|---|
| bao-gia.index | GET assign/quotations | presale.danh_sach_bao_gia.view | có | QuotationService::list → checkPermissionListWithColumn [4 tên,true] cột created_by | auto |
| bao-gia.pending | GET assign/quotations/pending-approval | presale.gia_bom_giai_phap_truong_phong.approve|ban_giam_doc.approve | không | applyPendingApprovalScope hasTp/hasBgd | auto |
| yc-gp.index | GET assign/request-solutions | presale.danh_sach_yeu_cau_lam_giai_phap.view | có | RequestSolutionService → checkPermissionListWithColumn [4 tên,true] cột receive_id | auto |
| yc-gp.pending | GET assign/request-solutions/pending | presale.yeu_cau_lam_giai_phap.confirm | không | pending: không quyền tiếp nhận ⇒ 1=0 | auto |
| du-an.index | GET assign/prospective-projects | presale.danh_sach_du_an_tien_kha_thi.view | có | ProspectiveProjectService::index → VIEW_PERMISSIONS[0] / scopeByViewPermission ∪ KD hỗ trợ | auto |
| du-an.index-tree | GET assign/prospective-projects | presale.danh_sach_du_an_tien_kha_thi.view | có | như trên, chế độ cây mặc định | auto |
| pricing.index | GET assign/pricing-requests | presale.gia_ban_theo_*.create | không | PricingRequestController::index cờ xây dựng giá | auto |
| gia-han.pending | GET assign/prospective-project-extensions/pending-approval | presale.gia_han_du_an_tkt_*.approve | không | middleware TP|BGĐ + lọc cấp | auto |
| solutions.index | GET assign/solutions | — | không | không gác quyền presale trực tiếp — đối chứng | auto |
| dm.danh_muc_nhom_nganh | GET assign/scopes | presale.danh_muc_nhom_nganh.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_ung_dung | GET assign/applications | presale.danh_muc_ung_dung.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_vai_tro_du_an | GET assign/project_roles | presale.danh_muc_vai_tro_du_an.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_hang_muc_du_an | GET assign/project_items | presale.danh_muc_hang_muc_du_an.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_giai_doan_du_an | GET assign/project_phases | presale.danh_muc_giai_doan_du_an.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_nhom_giai_phap | GET assign/industries | presale.danh_muc_nhom_giai_phap.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_nguyen_nhan_that_bai_du_an | GET assign/reason_project_failures | presale.danh_muc_nguyen_nhan_that_bai_du_an.manage|view | không | middleware manage|view | auto |
| dm.danh_muc_mau_phieu_thu_thap_thong_tin | GET assign/form-templates | presale.danh_muc_mau_phieu_thu_thap_thong_tin.manage|view | không | middleware manage|view | auto |
| bc.solution-requests-by-department | GET assign/report/solution-requests-by-department | presale.bao_cao_theo_doi_giai_phap_theo_phong_kd.view | có | applyPermissionFilter 4 · 3 c.id∪rs.created_by · 2 d.id∪part∪created_by · else e.id=tôi | auto |
| bc.customer-development | GET assign/report/customer-development | presale.bao_cao_phat_trien_khach_hang.view | có | applyPermissionScopeToEmployees / applyPermissionFilter | auto |
| bc.customer-development.filter | GET assign/report/customer-development/filter-options | presale.bao_cao_phat_trien_khach_hang.view | có | applyPermissionFilter | lists |
| bc.prospective-projects | GET assign/report/prospective-projects | presale.bao_cao_tong_hop_du_an_tkt.view | có | applyPermissionFilter 4/3/2 | auto |
| bc.prospective-projects.filter | GET assign/report/prospective-projects/filter-options | presale.bao_cao_tong_hop_du_an_tkt.view | có | applyPermissionFilter | lists |
| bc.solutions-work-summary | GET assign/report/solutions-work-summary-by-department | presale.bao_cao_tong_hop_gp.view | có | checkPermissionList [4 tên,true] solutions | auto |
| bc.division-market | GET assign/report/division-market | presale.bao_cao_phan_chia_thi_truong.view | không | middleware | auto |
| bc.meeting-by-employees | GET assign/report/meeting-by-employees | presale.bao_cao_meeting_theo_nhan_vien.view | có | applyEmployeeScope 4/3/2 | auto |
| bc.meeting-by-employees.filter | GET assign/report/meeting-by-employees/filter-options | presale.bao_cao_meeting_theo_nhan_vien.view | có | filterOptions canAll | lists |
| bc.potential-customer-care | GET assign/report/potential-customer-care | presale.bao_cao_ket_qua_cham_soc_khach_hang_tiem_nang.view | có | applyPermissionFilter 4/3/2 meetings | auto |
| bc.potential-customer-care.filter | GET assign/report/potential-customer-care/filter-options | presale.bao_cao_ket_qua_cham_soc_khach_hang_tiem_nang.view | có |  | lists |
| bc.service-demand | GET assign/report/service-demand | presale.bao_cao_tong_hop_nhu_cau_lam_dich_vu.view | có | 4/3 | auto |
| bc.service-demand.filter | GET assign/report/service-demand/filter-options | presale.bao_cao_tong_hop_nhu_cau_lam_dich_vu.view | có | canAll | lists |
| bc.potential-customer-tracking | GET assign/report/potential-customer-tracking | presale.bao_cao_tong_hop_cskh_tiem_nang.view | có | 4/3/2 | auto |
| bc.potential-customer-tracking.filter | GET assign/report/potential-customer-tracking/filter-options | presale.bao_cao_tong_hop_cskh_tiem_nang.view | có |  | lists |
| bc.meeting-by-projects | GET assign/report/meeting-by-projects | presale.bao_cao_meeting_theo_du_an.view | có | applyProjectScope 4/3 | auto |
| bc.meeting-by-projects.filter | GET assign/report/meeting-by-projects/filter-options | presale.bao_cao_meeting_theo_du_an.view | có | canAll | lists |
| bc.prospective-project-results | GET assign/report/prospective-project-results | presale.bao_cao_ket_qua_du_an_tkt.view | có | 4/3/2 | auto |
| bc.prospective-project-results.filter | GET assign/report/prospective-project-results/filter-options | presale.bao_cao_ket_qua_du_an_tkt.view | có |  | lists |
| bc.meeting-by-market | GET assign/report/meeting-by-market | presale.bao_cao_ket_qua_meeting_theo_thi_truong.view | có | applyPermissionFilter 4/3/2 | auto |
| bc.customer-market-development | GET assign/report/customer-market-development | presale.bao_cao_phat_trien_thi_truong_khach_hang.view | có | permissionLevel all/company/department/self | auto |
