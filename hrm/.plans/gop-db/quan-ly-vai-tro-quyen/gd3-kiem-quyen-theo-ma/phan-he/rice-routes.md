# rice — đường đọc (mốc GĐ3 Task 8.4)

Chỉ hrm-api (ERP 0 hit). Bảng rice_* ở kết nối `mysql_tpe`. File máy đọc: `rice-routes.json` (10 route × 5 tài khoản).

| app · method · url | mã | chuỗi phạm vi | lọc đang dùng |
|---|---|---|---|
| api GET rice/sheet-registration | rice.phieu_dang_ky_suat_an.view | có (4/3/2) | checkRicePermissionList: 4 toàn bộ / 3 rice_company_id = công ty cơm ∪ rice_created_by = tôi / 2 rice_department_id ∈ phòng cơm mình quản lý ∪ tôi / còn lại tôi; dòng có is_can_cancel (suat_an_khach*.create, bao_com.manage) |
| api GET rice/sheet-registration/get-guest | — | không | không lọc quyền (đối chứng) |
| api GET rice/report/rice-detail | rice.bao_cao_com_chi_tiet.view | có | checkRicePermissionList trên rice_employee_infos (cột mình = id) + rice_registration_rice_supports |
| api GET rice/report/rice-detail-guest | rice.bao_cao_com_chi_tiet.view | có | rice_companies qua rice_employee_infos + phiếu khách/khách dài ngày |
| api GET rice/report/rice-general (department_and_employee) | rice.bao_cao_com_tong_hop.view | có | như chi tiết, type general |
| api GET rice/report/rice-general (department) | rice.bao_cao_com_tong_hop.view | có | getPaginatedDepartment |
| api GET rice/report/rice-general-guest | tong_hop (+ chi_tiet ở phần khách dài ngày, giữ như cũ) | có | |
| api GET rice/report/rice-general/print | tong_hop | có | generalReport + generalReportGuest |
| api GET rice/menu-board | rice.bao_com.manage | không | middleware |
| api GET rice/menu-board/get-by-date | rice.bao_com.manage | không | middleware |

Tài khoản (công ty 1): 13 (3 mã Xem = 4 + đủ mã thao tác), 337 (Xem = 4, không bao_com.manage), 311 và 148 (2 mã báo cáo = 2, không mã phiếu), 207 (không mã rice). Catalog không có phạm vi 3 nào trên rehearsal (0 người) và không có người "có mã không phạm vi" ⇒ 2 ca này chỉ PHPUnit.
