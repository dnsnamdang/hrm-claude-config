# payroll — đường đọc chụp mốc (Task 8.10, 28/10/2026)

Chỉ hrm-api (ERP 0 hit, TPE_APP 0 hit). Đầu vào máy đọc: `payroll-routes.json`. 11 route × 5 tài khoản = 55 ô.

| id | method · url | mã | chuỗi phạm vi? | lọc / cờ | cách lấy |
|---|---|---|---|---|---|
| salary.index | GET payroll/salary?limit=100 | payroll.bang_luong.view | có (4/3/else) | 4 toàn bộ · 3 `company_id` · else `company_id` + (status disabled ∪ created_by) | auto, băm id |
| salary.index.flags | GET payroll/salary?limit=1 | payroll.bang_luong.view | — | cờ `is_all_company` | lists |
| salary.employee.{730,728,740} | GET payroll/salary/{id}/employee | payroll.bang_luong.view | có (4/3/else) | 4 toàn bộ · 3 `employee_infos.company_id` · else bản thân; bảng lương cty 1/3/4 | auto, băm id |
| reports.payroll_info.{2026,2025} | GET timesheet/reports/payroll_info?from= | payroll.bao_cao_bang_chi_tra.view | có (4/3/2/1/else) | company / phòng∪bộ phận quản lý / bộ phận / bản thân + 4 cờ is_* | lists, băm nội dung (tổng tiền 12 tháng) |
| employee_infos.flags | GET employee_infos?limit=5 | payroll.bang_luong.manage | — | cờ `permissions.is_company` | lists |
| salary_compositions.index | GET payroll/salary-compositions | payroll.thanh_phan_luong.manage | — | middleware (cờ hasManageSalaryComposition luôn true khi qua) | auto |
| setting_histories.salary | GET setting-histories/human_setting_salary/1 | timesheet.thong_so.configure \| payroll.thong_so_luong.configure | — | HumanSettingSalaryAdapter::permissions + công ty | auto (status) |
| human_settings.histories.salary | GET human/settings/histories?scope=salary | như trên | — | HumanSettingHistoryController | auto (status) |

## Tài khoản (rehearsal, chỉ SELECT)
| key | NV | ghi chú |
|---|---|---|
| pv4 | 13 | bang_luong.view 4, bao_cao_bang_chi_tra.view 4, mọi mã không phạm vi |
| pv3 | 145 | bang_luong.view 3, bao_cao 3, bang_luong.manage; không approve/thanh_phan/thong_so_luong |
| pv3_cty3 | 408 | công ty 3: bang_luong.view 3, manage, thanh_phan, thong_so_luong (+ timesheet.thong_so); không bao_cao |
| pv2 | 148 | bao_cao_bang_chi_tra.view 2; không bang_luong.* |
| khong_ma | 207 | 0 mã payroll có hit |

## Ca thiếu / không chụp
- Phạm vi 1 (bao_cao_bang_chi_tra): rehearsal 0 người ⇒ chỉ PHPUnit.
- Có mã không phạm vi / khác công ty: chỉ PHPUnit.
- `bonus_distributions` rỗng ⇒ can_approve / approve / reject chỉ PHPUnit (approve/reject là ghi).
- POST general-regulations (ghi) ⇒ chỉ PHPUnit.
