# Phân hệ assign — đường đọc chụp mốc (Task 8.12)

Công cụ: `scratchpad/assign/snap.py` (bản training: băm id + mọi cờ bool). Token: `ScopeSnapshot.php tokens` (`scratchpad/assign-tokens.json`). API 8011, DB `hrm_erp_rbac_rehearsal`. ERP: 0 hit assign ⇒ không chụp.

## Tài khoản

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit cty1 — 60/60 mã assign, 20 mã Xem phạm vi 4 + kế hoạch&KQ phạm vi 3 |
| pv3_cty2 | 333 | cty2 — 24 mã, 8 mã Xem phạm vi 3 |
| pv3_cty4 | 522 | cty4 — 9 mã Xem phạm vi 3 (giao công tác/giao việc/đề xuất CT/gia hạn/HSTT/bc thực hiện CV…) |
| pv3_cty9 | 1190 | cty9 — 7 mã Xem phạm vi 3 (giải pháp/BOM/bàn giao/hiệu suất/phân bổ/version) |
| pv2 | 148 | cty1 — 42 mã, 16 Xem phạm vi 2, quyết toán 3 |
| pv1_mix | 110 | cty1 — 40 mã: 6 Xem phạm vi 1 (task/issue/BOM/GP/hiệu suất GP/phân bổ NL), 9 phạm vi 2, quyết toán 3 |
| pv2_cty9 | 1189 | cty9 — 30 mã, 9 Xem phạm vi 2, bc thực hiện CV 3 |
| khong_ma | 337 | cty1 — 0 mã assign.* |

## Route (48) — ô `status/so_dong` ở mốc trước

| id | url | mã | cột lọc / cờ | pv4 | pv3_cty2 | pv3_cty4 | pv3_cty9 | pv2 | pv1_mix | pv2_cty9 | khong_ma |
|---|---|---|---|---|---|---|---|---|---|---|---|
| job_requests.index | `assign/job_requests` | `assign.danh_sach_phieu_de_xuat_cong_viec_can_lam.view` | JobRequestService chuỗi 4 mức + cờ permissions + canApproveJobRequest | 200/488 | 200/0 | 200/1 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| job_requests.waiting | `assign/job_requests` | `assign.phieu_de_xuat_cong_viec.approve` | type=waiting: duyệt TP | 200/2 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| assign_jobs.index | `assign/assign_jobs` | `assign.danh_sach_phieu_giao_viec.view` | AssignJobService chuỗi 4 mức + cờ + canApprove/Import | 200/353 | 200/0 | 200/36 | 200/0 | 200/11 | 200/24 | 200/0 | 200/0 |
| assign_jobs.waiting | `assign/assign_jobs` | `assign.phieu_giao_cong_viec.approve` | type=waiting | 200/7 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| assign_requests.index | `assign/assign_requests` | `assign.danh_sach_phieu_de_xuat_di_cong_tac.view` | AssignRequestService chuỗi 4 mức + cờ + canCreateAssignBusiness | 200/159 | 200/0 | 200/8 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| assign_requests.waiting | `assign/assign_requests` | `assign.phieu_de_xuat_di_cong_tac.manage` | type=waiting | 200/33 | 200/0 | 200/3 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| assign_business.all | `assign/assign_business` | `assign.danh_sach_phieu_giao_cong_tac.view` | AssignBusinessService::searchByFilter type=all chuỗi 4 mức + cờ + dòng canEdit/Approve (Resource $permissions) | 200/7491 | 200/0 | 200/495 | 200/0 | 200/0 | 200/2 | 200/0 | 200/0 |
| assign_business.waiting | `assign/assign_business` | `assign.phieu_giao_cong_tac.approve` | type=waiting | 200/85 | 200/85 | 200/85 | 200/0 | 200/85 | 200/85 | 200/85 | 200/0 |
| assign_business.waiting_pbr | `assign/assign_business` | `assign.de_nghi_thanh_toan_phieu_cong_tac.create` | type=waiting-payment-business | 200/4592 | 200/0 | 200/226 | 200/0 | 200/0 | 200/0 | 200/0 | 200/1043 |
| dashboard.assign_business | `assign/dashboard/assign-business` | `assign.danh_sach_phieu_giao_cong_tac.view` | getAssignBusiness chuỗi 4 mức | 500/48 | 500/48 | 500/48 | 500/48 | 500/48 | 500/48 | 500/48 | 500/48 |
| dashboard.index | `assign/dashboard` | `assign.*.approve` | DashboardService isShow + WaitingApproveService chuỗi ĐNTT | 200/1484 | 200/325 | 200/340 | 200/33 | 200/325 | 200/326 | 200/325 | 200/0 |
| payment_business_request.index | `assign/payment-business-request` | `assign.danh_sach_de_nghi_thanh_toan.view` | Criteria chuỗi 4 mức + cờ controller | 200/1134 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| payment_profile.index | `assign/payment-profile` | `assign.danh_sach_ho_so_thanh_toan.view` | Criteria chuỗi 4 mức + cờ Transformer | 200/3429 | 200/0 | 200/596 | 200/0 | 200/0 | 200/1 | 200/0 | 200/0 |
| settlement_contract.index | `assign/settlement-contract` | `assign.danh_sach_quyet_toan_hop_dong.view` | Criteria chuỗi 4 mức + cờ controller | 200/4 | 200/0 | 200/4 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| extend_end_soon.index | `assign/extend-end-soon-request` | `assign.danh_sach_gia_han_ket_thuc_som.view` | Criteria chuỗi 4 mức + cờ Transformer | 200/1850 | 200/0 | 200/623 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| rp.by_customer | `assign/reports/assign_task_department_by_customer` | `assign.bao_cao_thuc_hien_cong_viec_cho_phong_ban_khach_hang.view` | ReportController cờ + 2 chuỗi 4 mức | 200/22 | 200/0 | 200/3 | 200/0 | 200/0 | 200/1 | 200/0 | 200/0 |
| rp.work_and_performance | `assign/reports/work-and-performance` | `assign.bao_cao_cong_duoc_huong_theo_phieu_cong_tac.view` | cờ 3 khoá → WorkAndPerformanceService | 200/4921 | 200/0 | 200/791 | 200/0 | 200/0 | 200/2 | 200/0 | 200/0 |
| rp.performance_by_employee | `assign/reports/performance-by-employee` | `assign.bao_cao_hieu_suat_nv.view` | applyPermissionFilter 3 mức | 200/8 | 200/0 | 200/0 | 200/0 | 200/2 | 200/0 | 200/0 | 200/0 |
| rp.employee_work_performance | `assign/report/employee-work-performance` | `assign.bao_cao_ke_hoach_ket_qua_lam_viec.view` | permissionLevel 3 mức | 200/5977 | 403/49 | 403/49 | 403/49 | 403/49 | 403/49 | 403/49 | 403/49 |
| rp.employee_work_performance.filter | `assign/report/employee-work-performance/filter-options` | `assign.bao_cao_ke_hoach_ket_qua_lam_viec.view` | permissionLevel | 200/1 | 403/47 | 403/47 | 403/47 | 403/47 | 403/47 | 403/47 | 403/47 |
| rp.solution_versions | `assign/report/solution-versions` | `assign.bao_cao_version_giai_phap.view` | applyPermissionFilter 3 mức | 200/37 | 200/0 | 200/0 | 200/0 | 200/2 | 200/0 | 200/0 | 200/0 |
| rp.performance_by_solutions | `assign/report/performance-by-solutions` | `assign.bao_cao_hieu_suat_gp.view` | checkPermissionList 4 tên + true | 200/7 | 200/0 | 200/0 | 200/0 | 200/1 | 200/0 | 200/0 | 200/0 |
| rp.task_manager_by_employees | `assign/report/task-manager-by-employees` | `assign.bao_cao_phan_bo_nguon_luc.view` | applyPermissionFilter 4 mức | 200/77 | 200/1 | 200/1 | 200/13 | 200/1 | 200/1 | 200/1 | 200/1 |
| customer_demands.index | `assign/customer-demands` | `assign.danh_sach_nhu_cau_khach_hang.view` | applyPermissionFilter 4 mức + canHandoverAll | 200/501 | 200/0 | 200/0 | 200/0 | 200/5 | 200/0 | 200/0 | 200/0 |
| tasks.index | `assign/tasks` | `assign.danh_sach_task.view` | applyPermissionScope + tier3 + Duyệt triển khai task | 200/19 | 200/0 | 200/0 | 200/0 | 200/3 | 200/0 | 200/0 | 200/0 |
| issues.index | `assign/issues` | `assign.danh_sach_issue.view` | applyPermissionScope + tier3 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| bom_lists.index | `assign/bom-lists` | `assign.danh_sach_bom_list.view` | checkPermissionListWithColumn 4 tên + true | 200/16 | 200/0 | 200/0 | 200/0 | 200/1 | 200/0 | 200/0 | 200/0 |
| handovers.index | `assign/handovers` | `assign.danh_sach_ban_giao_cong_viec.view` | checkPermissionListWithColumn 3 tên + null + true | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| handovers.pending | `assign/handovers/pending` | `assign.ban_giao_cong_viec.approve` | gate Duyệt bàn giao | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 | 200/0 |
| solutions.index | `assign/solutions` | `assign.danh_sach_lam_giai_phap.view` | checkPermissionList 4 tên + true (ids) | 200/38 | 200/0 | 200/0 | 200/0 | 200/2 | 200/0 | 200/0 | 200/0 |
| ts.job_assignment | `timesheet/job-assignment` | `assign.phieu_giao_viec.manage` | JobAssignmentNoteController index gate + Entity can* | 200/9274 | 200/28 | 200/21669 | 200/0 | 200/273 | 200/356 | 200/0 | 200/47 |
| ts.business_trip_assigns | `timesheet/business_trip_assigns` | `assign.phieu_di_cong_tac.manage` | BusinessTripAssignController index gate + Entity can* | 200/11643 | 200/0 | 200/1327 | 200/0 | 200/252 | 200/650 | 200/0 | 200/14 |
| ts.business_trip_assigns.finish_extend | `timesheet/business_trip_assigns/listFinishExtend` | `assign.gia_han_ket_thuc_som.create` | gate Gia hạn | 200/435 | 200/0 | 200/10 | 200/1 | 200/435 | 200/435 | 200/1 | 200/435 |
| cat.internal_business_scopes | `assign/internal-business-scopes` | `assign.danh_muc_linh_vuc_cong_ty_kinh_doanh.manage|view` | middleware | 200/8 | 403/0 | 403/0 | 403/0 | 403/0 | 200/8 | 403/0 | 403/0 |
| cat.customer_scopes | `assign/customer-scopes` | `assign.danh_muc_linh_vuc_khach_hang.manage|view` | middleware | 200/206 | 403/0 | 403/0 | 200/206 | 200/206 | 200/206 | 403/0 | 403/0 |
| cat.customer_scope_groups | `assign/customer-scope-groups` | `assign.danh_muc_nhom_linh_vuc_khach_hang.manage|view` | middleware | 200/23 | 403/0 | 403/0 | 403/0 | 200/23 | 200/23 | 403/0 | 403/0 |
| cat.attachment_types | `assign/attachment-types` | `assign.danh_muc_loai_tai_lieu.manage|view` | middleware | 200/16 | 403/0 | 403/0 | 200/16 | 200/16 | 200/16 | 403/0 | 403/0 |
| cat.questions | `assign/questions` | `assign.danh_muc_cau_hoi_khao_sat.manage|view` | middleware | 200/0 | 403/0 | 403/0 | 200/0 | 200/0 | 200/0 | 403/0 | 403/0 |
| cat.discount_types | `assign/discount_types` | `assign.danh_muc_loai_giam_gia.manage` | middleware | 200/1 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |
| cfg.configs_histories | `assign/configs/histories` | `assign.phan_he_giao_viec_cong_tac.configure` | middleware | 200/0 | 200/0 | 200/1 | 200/0 | 403/0 | 403/0 | 200/0 | 403/0 |
| cfg.priority_histories | `assign/priority-levels/histories` | `assign.phan_he_giao_viec_cong_tac.configure` | middleware | 200/12 | 200/0 | 200/0 | 200/0 | 403/0 | 403/0 | 200/0 | 403/0 |
| cfg.project_close_logs | `assign/project-close-configs/logs` | `assign.phan_he_giao_viec_cong_tac.configure` | middleware | 200/0 | 200/0 | 200/0 | 200/0 | 403/0 | 403/0 | 200/0 | 403/0 |
| cfg.deadline_histories | `assign/my-job/deadline-config/histories` | `assign.phan_he_giao_viec_cong_tac.configure` | middleware | 200/0 | 200/0 | 200/0 | 200/0 | 403/0 | 403/0 | 200/0 | 403/0 |
| sh.assign_config | `setting-histories/assign_config/1` | `assign.phan_he_giao_viec_cong_tac.configure` | SettingHistory adapter permissions() | 200/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |
| sh.priority_level | `setting-histories/priority_level/1` | `assign.phan_he_giao_viec_cong_tac.configure` | SettingHistory adapter permissions() | 200/12 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |
| sh.deadline_config | `setting-histories/deadline_config/1` | `assign.phan_he_giao_viec_cong_tac.configure` | SettingHistory adapter permissions() | 200/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |
| sh.project_close_config | `setting-histories/project_close_config/1` | `assign.phan_he_giao_viec_cong_tac.configure` | SettingHistory adapter permissions() | 200/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |
| sh.bom_price_approval_config | `setting-histories/bom_price_approval_config/1` | `assign.phan_he_giao_viec_cong_tac.configure` | SettingHistory adapter permissions() | 200/5 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 | 403/0 |

## Bỏ khỏi mốc HTTP

- `assign/my-job/assign-business-list` (MyJobAssignBusinessResource): 55–59 s/ô, sát ngưỡng 60 s làm sập `php -S` (bài học 8.9) ⇒ phủ bằng PHPUnit `AssignScopeCodesTest::test_entity_can_nhan_danh_sach_ma_va_dashboard` (cùng các hàm `AssignRequest::can*($permissions)` nhận danh sách mã).
- `dashboard.assign_business` 500 ở mọi tài khoản cả trước/sau (lỗi sẵn `$date` khi 1 ngày) — vẫn giữ trong mốc nhưng tín hiệu yếu.
- Route ghi (store/update/approve…) chỉ đổi chuỗi middleware tên → mã (min_scope null) — không chụp.

## Ca thiếu (chỉ PHPUnit)

- Có mã không phạm vi (rehearsal 0 dòng scope NULL cho mã có phạm vi), khác công ty, phạm vi 1 trên mã bàn giao (allowed 2–4).
- Nhiều ô phạm vi 2/1 ra 0 dòng (người không quản lý phòng có phiếu) — tín hiệu yếu, phủ bằng test SQL từng mức.
