# training — đường đọc chụp mốc (Task 8.11)

Chỉ hrm-api (ERP 0 hit, TPE_APP 0 hit). Đầu vào máy đọc: `training-routes.json`. Công cụ chụp: `scratchpad/training/snap.py` (GET thật tới 8011; ghi status, so_dong = `total` đầu tiên trong JSON hoặc độ dài mảng lớn nhất, băm id trang đầu, băm MỌI cờ bool kể cả cờ dòng `can*` theo id dòng). 42 route × 6 tài khoản = 252 ô.

## Tài khoản (rehearsal, chỉ SELECT)

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit cty1 — 58/58 mã training, mọi mã Xem phạm vi 4 |
| pv3_cty2 | 333 | cty2 — 54 mã, 18 mã Xem phạm vi 3 |
| pv2_mix | 148 | cty1 — 35 mã: 7 Xem phạm vi 2, 3 phạm vi 3, còn lại 4 |
| pv2_cty9 | 1189 | cty9 — 50 mã, 16 Xem phạm vi 2 |
| chi_phi | 207 | cty1 — chỉ training.chi_phi.manage |
| khong_ma | 337 | cty1 — 0 mã training.* |

Ca thiếu (chỉ PHPUnit): phạm vi 1 (0 người trên rehearsal), có mã không phạm vi (0 dòng scope NULL), khác công ty cùng 1 người. Bảng training_surveys / department_training_surveys / staff_training_surveys rỗng ⇒ các route khảo sát chỉ ra 0 (tín hiệu yếu, phủ bằng test). Route ghi (store/update/approve, authorize Store/UpdateTrainingSurveyRequest) không chụp — phủ bằng test.

## Route

| id | url | mã | cột lọc / cờ |
|---|---|---|---|
| teachers.index | training/teachers ?page=1&limit=100&per_page=100 | training.giang_vien.manage | cờ hasPermissionManager + dòng canEdit/canDelete; searchByFilter gate |
| examiners.index | training/examiners ?page=1&limit=100&per_page=100 | training.nguoi_cham_thi.manage | cờ hasPermissionManager + dòng canEdit/canDelete |
| examiners.summary-exam | training/examiners/summary-exam ?page=1&limit=100&per_page=100 | training.tong_hop_bai_thi.view | ExaminerService::getSummaryExam checkPermissionList 4 mức + created_by |
| training_types.index | training/training_types ?page=1&limit=100&per_page=100 | training.loai_dao_tao.manage | dòng can_edit/can_delete (resource names→codes); searchByFilter gate |
| subjects.index | training/subjects ?page=1&limit=100&per_page=100 | training.mon_hoc.manage | cờ canHasManager + dòng canEdit/canDelete |
| cost_trainings.index | training/cost_trainings ?page=1&limit=100&per_page=100 | training.chi_phi.manage | searchByFilter gate + dòng canEdit |
| course_requests.index | training/course_requests ?page=1&limit=100&per_page=100 | training.de_xuat_mo_khoa_hoc.view | checkPermissionList 4 mức + cờ is_* + isTruongPhong/isBangiamdoc/create + dòng approve |
| course_requests.waiting | training/course_requests ?page=1&limit=100&per_page=100&type=waiting | training.de_xuat_mo_khoa_hoc_*.approve | type=waiting: lọc theo quyền duyệt |
| course_requests.show.1 | training/course_requests/1 ?page=1&limit=100&per_page=100 | training.de_xuat_mo_khoa_hoc_*.approve | getDataForShow isTruongPhong/isBangiamdoc |
| training_requests.index | training/training_requests ?page=1&limit=100&per_page=100 | training.de_xuat_dao_tao.view | checkPermissionList 4 mức + cờ is_* + dòng canDepartmentHeadApprove/canManagerTrainingApprove |
| training_requests.waiting | training/training_requests ?page=1&limit=100&per_page=100&type=waiting | training.de_xuat_dao_tao_*.approve | type=waiting |
| training_requests.show.15 | training/training_requests/15 ?page=1&limit=100&per_page=100 | (tên lạ Duyệt đề xuất đào tạo) | canApprove luôn false |
| questions.index | training/questions ?page=1&limit=100&per_page=100 | training.cau_hoi.manage | cờ + dòng canEdit/canDelete + searchByFilter gate |
| questions.show.1959 | training/questions/1959 ?page=1&limit=100&per_page=100 | training.cau_hoi.manage | show gate |
| exams.index | training/exams ?page=1&limit=100&per_page=100 | training.de_thi.manage | cờ + dòng canEdit + gate |
| capability_groups.index | training/capability_groups ?page=1&limit=100&per_page=100 | training.nhom_nang_luc.manage | cờ + dòng can_edit + gate |
| capabilities.index | training/capabilities ?page=1&limit=100&per_page=100 | training.nang_luc.manage | dòng canEdit + gate |
| courses.index | training/courses ?page=1&limit=100&per_page=100 | training.khoa_hoc.view | chuỗi 4 mức CourseService::searchByFilter + cờ is_* + hasCreate + dòng can* |
| courses.waiting | training/courses ?page=1&limit=100&per_page=100&type=waiting | training.khoa_hoc_*.approve | type=waiting |
| courses.show.269 | training/courses/269 ?page=1&limit=100&per_page=100 | training.thong_tin_tat_ca_khoa_hoc.view | canViewAllInfo (cty1) |
| courses.show.256 | training/courses/256 ?page=1&limit=100&per_page=100 | training.thong_tin_tat_ca_khoa_hoc.view | canViewAllInfo (cty4) |
| courses.reportSummaryResultCourse | training/courses/reportSummaryResultCourse ?page=1&limit=100&per_page=100 | training.tong_hop_ket_qua_khoa_hoc.view | gate 403 |
| courses.training-status-by-personnel | training/courses/reports/training-status-by-personnel ?page=1&limit=100&per_page=100 | training.bao_cao_tinh_hinh_dao_tao_nhan_su.view | checkPermissionEmployeeInfo 4 mức + bản thân |
| course-registers.index | training/course-registers ?page=1&limit=100&per_page=100 | training.dang_ky_khoa_hoc.view | có approve ⇒ không lọc; không ⇒ checkPermissionList 4 mức |
| training_surveys.index | training/training_surveys ?page=1&limit=100&per_page=100 | training.phieu_khao_sat_dao_tao.view | checkPermissionList 4 mức + cờ is_* |
| tsdm.index | training/training-survey-department-manager ?page=1&limit=100&per_page=100 | training.ket_qua_khao_sat_cua_phong.view | checkPermissionList [tổng, công ty, false, false] (else id null) |
| tsd.index | training/training-survey-department ?page=1&limit=100&per_page=100 | training.phieu_khao_sat_cua_phong.create | gate getList |
| tspm.index | training/training-survey-personals-manager ?page=1&limit=100&per_page=100 | training.ket_qua_khao_sat_cua_nhan_vien.view | checkPermissionList 4 mức + cờ is_* |
| training-planning.index | training/training-planning ?page=1&limit=100&per_page=100 | training.ke_hoach_dao_tao.view | checkPermissionList 4 mức (nhánh điều kiện) |
| course-evaluation.index | training/course-evaluation ?page=1&limit=100&per_page=100 | training.yeu_cau_danh_gia_chat_luong_dao_tao.view | checkPermissionList 4 mức |
| cerm.index | training/course-evaluation-result-manager ?page=1&limit=100&per_page=100 | training.phieu_danh_gia_chat_luong_dao_tao_cua_nhan_vien.view | checkPermissionList 4 mức |
| cep.index | training/capacity-evaluate-planning ?page=1&limit=100&per_page=100 | training.ke_hoach_danh_gia.view | checkPermissionList 4 mức |
| ce.index | training/capacity-evaluate ?page=1&limit=100&per_page=100 | training.ky_thi_danh_gia_nang_luc.view | checkPermissionList [tổng, công ty, (tên lạ có dấu cách) , bộ phận, true] |
| ce.capacity-exam-summary | training/capacity-evaluate/capacity-exam-summary ?page=1&limit=100&per_page=100 | training.tong_hop_bai_thi_dgnl.view | checkPermissionList 4 mức |
| ce.get-all-select | training/capacity-evaluate/get-all-select  | training.ket_qua_danh_gia_nang_luc.view | điều kiện bản thân |
| ce.get-all-select.join | training/capacity-evaluate/get-all-select ?is_join=1 | training.tong_hop_ket_qua_danh_gia_theo_ky.view | is_join=1 |
| ce.byEvaluation.1 | training/capacity-evaluate/summaryResultExamTestByEvaluation ?evaluation_capacity_id=1 | training.tong_hop_ket_qua_danh_gia_theo_ky.view | bản thân nếu không mã |
| capacity-report.planning | training/capacity-report/planning  | training.theo_doi_thuc_hien_ke_hoach.view | CapacityReportService::checkPermission [tổng, công ty] |
| capability-frameworks.index | training/capability-frameworks ?page=1&limit=100&per_page=100 | training.khung_nang_luc.view | checkPermissionList 4 mức + cờ is_* + isChange |
| career-progressions.index | training/career-progressions ?page=1&limit=100&per_page=100 | training.bao_cao_lo_trinh_thang_tien.view | checkPermissionList [4 tên, false, true=vị trí CV] + cờ |
| career-progressions.report.68 | training/career-progressions/report ?working_position_id=68 | training.bao_cao_lo_trinh_thang_tien.view | getDetailReport checkPermissionList 4 mức |
| dashboard.getData | training/dashboard/getData  | training.*.approve | job_waiting_approve lọc isShow theo tên |
