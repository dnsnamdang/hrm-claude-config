# timesheet — đường đọc chụp mốc (Task 8.5)

API hrm-api 8011, DB hrm_erp_rbac_rehearsal. ERP: 0 hit timesheet ⇒ không chụp.

## Tài khoản

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — mã Xem timesheet = 4 (bảng tổng hợp/tháng/phân ca = 3) + mọi mã duyệt/thiết lập |
| pv4_khong_duyet | 145 | mã Xem = 4 như 13, KHÔNG mã duyệt/xác nhận nào, không thong_so.configure |
| pv2 | 148 | mã Xem = 2 (phan_cong/phieu_yeu_cau = 3), duyệt cấp phòng; quản lý phòng 55 |
| pv2_b | 110 | mã Xem = 2 như 148 (phan_cong/phieu_yeu_cau = 3); quản lý phòng 47, thuộc bộ phận 26. (578 — người duy nhất có phạm vi 3 cho don_xin_nghi/du_lieu — bị vô hiệu hoá ⇒ không có ca pv3) |
| khong_ma | 207 | 0 mã timesheet.* |

Ca thiếu: phạm vi 3 cho mã Xem đơn/dữ liệu (người duy nhất 578 bị vô hiệu hoá), phạm vi 1 (0 người), có mã không phạm vi, khác công ty ⇒ chỉ PHPUnit (TimesheetScopeCodesTest).

## Route

| id | url | tham số | mã | chuỗi? | cột lọc / ghi chú |
|---|---|---|---|---|---|
| attendance.index | timesheet/attendance |  | timesheet.don_xin_nghi.view | có | AttendanceService::index → checkPermissionList 4/3/2/1 bảng attendances (+ cờ is_* ở controller); dòng có can_approve/can_reject (PD/NSHC) |
| attendance.approve | timesheet/attendance/approve |  | timesheet.don_xin_nghi.approve |  | AttendanceService::approve — PD-Đơn xin nghỉ / NSHC duyệt |
| attendance.static | timesheet/attendance/static-data |  |  |  | staticData (cờ permissions nếu có) |
| leo.index | timesheet/late-in-early-out |  | timesheet.dang_ky_di_muon_ve_som.view | có | LateEarlyOutService::index → checkPermissionList late_early_outs |
| leo.approve | timesheet/late-in-early-out/approve |  | timesheet.dang_ky_di_muon_ve_som.approve |  | approve — PD-Đăng ký đi muộn về sớm |
| leo.static | timesheet/late-in-early-out/static-data |  |  |  | staticData |
| ota.index1 | timesheet/overtime-assignment | {"assignment_type": 1} | timesheet.phan_cong_lam_them.view | có | OvertimeAssignmentService::index type1 → checkPermissionList phân công (băm id: dòng có recess_*/approved_at = now() khi null) |
| ota.index2 | timesheet/overtime-assignment | {"assignment_type": 2} | timesheet.dang_ky_lam_them.view | có | OvertimeAssignmentService::index type≠1 → checkPermissionList đăng ký (băm id: dòng có recess_*/approved_at = now() khi null) |
| ota.static1 | timesheet/overtime-assignment/static-data | {"assignment_type": 1} | timesheet.phan_cong_lam_them.view | có | staticData cờ type 1 |
| ota.static2 | timesheet/overtime-assignment/static-data | {"assignment_type": 2} | timesheet.dang_ky_lam_them.view | có | staticData cờ type 2 |
| ota.approve | timesheet/overtime-assignment/approve |  | timesheet.dang_ky_lam_them.approve |  | approve — PD-Đăng ký làm thêm (băm id: dòng có recess_*/approved_at = now() khi null) |
| otr.index | timesheet/overtime-requirement |  | timesheet.phieu_yeu_cau_lam_them.view | có | OvertimeRequirementService::index → checkPermissionList |
| otr.approve | timesheet/overtime-requirement/approve |  | timesheet.phieu_yeu_cau_lam_them.approve |  | approve — PD-Phiếu yêu cầu làm thêm |
| otr.static | timesheet/overtime-requirement/static-data |  | timesheet.phieu_yeu_cau_lam_them.view | có | staticData cờ |
| rut.index | timesheet/request-update-working |  | timesheet.de_nghi_tra_soat_cong.view | có | RequestUpdateTimeSheetService::index → checkPermissionList |
| rut.approve | timesheet/request-update-working/approve |  | timesheet.de_nghi_tra_soat_cong.approve |  | approve — PD/XN-Đề nghị tra soát công |
| rut.static | timesheet/request-update-working/static-data |  | timesheet.de_nghi_tra_soat_cong.view | có | staticData cờ |
| timekeeper.index | timekeeper | {"time_gteq": "2026-10-15 00:00:00", "time_lteq": "2026-10-21 23:59:59"} | timesheet.du_lieu_cham_cong.view | có | TimekeeperService::index chuỗi 4/3/2/1 + cờ |
| timekeeper.flags | timekeeper | {"time_gteq": "2026-10-15 00:00:00", "time_lteq": "2026-10-21 23:59:59"} | timesheet.du_lieu_cham_cong.view | có | cờ permissions |
| ts_summary.index | timesheet/timesheet_summaries | {"daterange": "2026-09-01,2026-09-30"} | timesheet.bang_cham_cong_chi_tiet.view | có | TimesheetSummaryController::index chuỗi 4/3/2/1 + cờ |
| month_summary.show | timesheet/timesheet_month_summaries/show | {"id": 342} | timesheet.bang_cham_cong_tong_hop_trong_thang.view | có | TimesheetMonthSummaryService::show chuỗi 3/2/1 + cờ (bảng 342 công ty 1) |
| timeworking.index | timesheet/timeworking |  | timesheet.ca_lam_viec.view | có | WorkShiftService::index 4/3 + cờ is_all_company |
| timeworking.histories | timesheet/timeworking/histories |  | timesheet.ca_lam_viec.manage|view |  | middleware Quản lý ca làm việc/Xem danh mục ca … tổng công ty/công ty |
| shift_details.index | timesheet/shift_details |  | timesheet.phan_ca.manage | có | WorkShiftDetailService::index → checkPermissionListNotAllCompany 3/2/1 |
| shift_details.general | timesheet/shift_details/general | {"day": ["2026-10-01", "2026-10-31"]} | timesheet.phan_ca.manage | có | general → checkPermissionShiftByDate |
| sdeds.by_date | timesheet/shift-detail-employee-dates/get-employee-by-date | {"date": "2026-10-15"} | timesheet.phan_ca.manage | có | checkPermissionShiftByDate |
| sah.index | timesheet/shift-assignment-histories |  | timesheet.phan_ca.manage | có | middleware Phân ca 3/2/1 + applyPermissionScope |
| rep.timekeeper | timesheet/reports/timekeeper_report | {"from": "2026-09-01", "to": "2026-09-30"} | timesheet.bao_cao_tong_hop_cham_cong.view | có | ReportService::timekeeper_report chuỗi + cờ |
| rep.bta | timesheet/reports/business_trip_assign_report | {"from": "2026-09-01", "to": "2026-09-30"} | timesheet.bao_cao_tong_hop_di_giao_viec_cong_tac.view | có | business_trip_assign_report chuỗi 4/3/2 |
| rep.bta_job | timesheet/reports/business_trip_assign_report | {"from": "2026-09-01", "to": "2026-09-30", "type": "job_assign"} | timesheet.bao_cao_tong_hop_di_giao_viec_cong_tac.view | có | business_trip_assign_report type job_assign |
| rep.bta_business | timesheet/reports/business_trip_assign_report_ | {"from": "2026-09-01", "to": "2026-09-30", "type": "business"} | timesheet.bao_cao_tong_hop_di_giao_viec_cong_tac.view | có | BusinessTripAssign::searchByFilter chuỗi 4/3/2/1 |
| rep.bta_jobnote | timesheet/reports/business_trip_assign_report_ | {"from": "2026-09-01", "to": "2026-09-30", "type": "job_assign"} | timesheet.bao_cao_tong_hop_di_giao_viec_cong_tac.view | có | JobAssignmentNote::searchByFilter chuỗi 4/3/2/1 |
| rep.bta_all | timesheet/reports/business_trip_assign_report_ | {"from": "2026-09-01", "to": "2026-09-30"} | timesheet.bao_cao_tong_hop_di_giao_viec_cong_tac.view | có | combined |
| rep.overtime | timesheet/reports/overtime_report | {"from": "2026-09-01", "to": "2026-09-30"} | timesheet.bao_cao_lam_them_gio.view | có | overtime_report chuỗi + cờ |
| rep.overtime_detail | timesheet/reports/overtime_report_detail | {"from": "2026-09-01", "to": "2026-09-30"} | timesheet.bao_cao_lam_them_gio_chi_tiet.view | có | overtime_report_detail chuỗi + cờ |
| rep.attendance | timesheet/reports/attendance_report | {"year": 2026} | timesheet.bao_cao_phep.view | có | attendance_report chuỗi + cờ |
| aer.index | timesheet/attendances-extend-requests |  | timesheet.don_xin_nghi.approve |  | AttendancesExtendRequestService::index PD/NSHC |
| leave_type.histories | timesheet/leave-type/histories |  | timesheet.thong_so.configure |  | middleware Thiết lập thông số |
| master_settings.histories | master-settings/histories |  | timesheet.thong_so.configure |  | routes/api.php middleware Thiết lập thông số |
| sh.working_shift_59 | setting-histories/working_shift/59 |  | timesheet.ca_lam_viec.manage|view |  | WorkingShiftAdapter permissions + authorize 4/3 (ca công ty 1) |
| sh.working_shift_62 | setting-histories/working_shift/62 |  | timesheet.ca_lam_viec.manage|view |  | WorkingShiftAdapter authorize (ca công ty 9) |
| sh.master_setting | setting-histories/master_setting/1 |  | timesheet.thong_so.configure |  | MasterSettingAdapter permissions Thiết lập thông số |
