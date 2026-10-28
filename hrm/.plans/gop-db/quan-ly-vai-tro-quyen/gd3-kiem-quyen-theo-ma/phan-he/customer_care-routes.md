# customer_care — đường đọc chụp mốc (GĐ3 Task 8.13)

Sinh từ `customer_care-routes.json` (máy đọc). Chụp bằng `hrm-api/tests/Support/ScopeSnapshot.php` (tokens | run | diff), ERP chạy tạm `php -S 127.0.0.1:8012` (DB rehearsal + DB_*_HRM), hrm-api 8011.

## Tài khoản (rehearsal, chỉ SELECT)

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — 31 mã customer_care có phạm vi ở mức 4, 1 ở mức 3, 35 không phạm vi, cty 1 |
| pv3 | 207 | hantt.kthn — 16 mã mức 3, 2 mức 4, cty 1 |
| pv2 | 337 | duyentt.ktcnhn — 13 mã mức 2, 2 mức 3, 6 không phạm vi, cty 1 |
| pv1 | 110 | honglv.pt — 6 mã mức 1, 9 mức 2, 2 không phạm vi, cty 1 |
| tron | 244 | nhunght.cshn (CSKH) — 5 mã mức 4, 4 mức 3, 8 mức 2, 9 không phạm vi, cty 1 |
| cty4 | 661 | hieunv.tlgd — 5 mã mức 3, 11 mức 2, 12 không phạm vi, cty 4 |
| khong_ma | 144 | huyentt.nshn — 0 mã customer_care.*, cty 1 |

Ca thiếu (chỉ PHPUnit): có mã không phạm vi (rehearsal: các dòng scope NULL của customer_care đều là mã không phạm vi), khác công ty bằng Vai trò công ty khác (c2), phạm vi 1 trên mã chỉ cho 2–4.

## Route (130 = ERP 104 + hrm-api 26) × 7 tài khoản

| id | url | tham số | mã | chuỗi phạm vi | cột lọc / cách đọc | extract |
|---|---|---|---|---|---|---|
| erp.assembly_requests.index | admin/customer-care/assembly_requests | {"type": "all"} | customer_care.phieu_yeu_cau_lap_dat_ban_giao.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.assembly_requests.searchData.all | admin/customer-care/assembly_requests/searchData | {"type": "all"} | customer_care.phieu_yeu_cau_lap_dat_ban_giao.view | có | type=all chuỗi phạm vi | datatables |
| erp.assembly_requests.show | admin/customer-care/assembly_requests/{id}/show |  | customer_care.phieu_yeu_cau_lap_dat_ban_giao.view | có | canView | detail ids=[1902, 1898, 1897, 1901, 1822, 1789] |
| erp.assembly_requests.searchData.assign_task | admin/customer-care/assembly_requests/searchData | {"type": "assign-task"} | customer_care.phieu_cho_giao_viec.view | có | type=assign-task mức 4 | datatables |
| erp.assembly_requests.searchData.wait_approve | admin/customer-care/assembly_requests/searchData | {"type": "wait-approve"} | customer_care.phieu_yeu_cau_lap_dat_ban_giao_truong_phong.approve |  | TP duyệt | datatables |
| erp.assign_other_requests.index | admin/customer-care/assign_other_requests | {"type": "all"} | customer_care.phieu_yeu_cau_giao_viec_khac.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.assign_other_requests.searchData.all | admin/customer-care/assign_other_requests/searchData | {"type": "all"} | customer_care.phieu_yeu_cau_giao_viec_khac.view | có | type=all chuỗi phạm vi | datatables |
| erp.assign_other_requests.show | admin/customer-care/assign_other_requests/{id}/show |  | customer_care.phieu_yeu_cau_giao_viec_khac.view | có | canView | detail ids=[3065, 3062, 3064, 3063, 318] |
| erp.warranty_repair_requests.index | admin/customer-care/warranty_repair_requests | {"type": "all"} | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_requests.searchData.all | admin/customer-care/warranty_repair_requests/searchData | {"type": "all"} | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | type=all chuỗi phạm vi | datatables |
| erp.warranty_repair_requests.show | admin/customer-care/warranty_repair_requests/{id}/show |  | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | canView | detail ids=[7090, 7089, 5819, 5750, 6815] |
| erp.warranty_repair_requests.searchData.waiting_handle | admin/customer-care/warranty_repair_requests/searchData | {"type": "waiting_handle"} | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm |  | xử lý | datatables |
| erp.warranty_repair_handle_requests.index | admin/customer-care/warranty_repair_handle_requests | {"type": "all"} | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_handle_requests.searchData.all | admin/customer-care/warranty_repair_handle_requests/searchData | {"type": "all"} | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | type=all chuỗi phạm vi | datatables |
| erp.warranty_repair_handle_requests.show | admin/customer-care/warranty_repair_handle_requests/{id}/show |  | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | canView | detail ids=[6624, 6623, 5413, 5373, 5312] |
| erp.warranty_repair_handle_requests.searchData.waiting_information | admin/customer-care/warranty_repair_handle_requests/searchData | {"type": "waiting_information"} | customer_care.phieu_cung_cap_thong_tin.create |  |  | datatables |
| erp.warranty_repair_information_requests.index | admin/customer-care/warranty_repair_information_requests | {"permission": "all"} | customer_care.phieu_cung_cap_thong_tin.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_information_requests.searchData.all | admin/customer-care/warranty_repair_information_requests/searchData | {"permission": "all"} | customer_care.phieu_cung_cap_thong_tin.view | có | permission=all chuỗi phạm vi | datatables |
| erp.warranty_repair_information_requests.show | admin/customer-care/warranty_repair_information_requests/{id}/show |  | customer_care.phieu_cung_cap_thong_tin.view | có | canView | detail ids=[12738, 12737, 12734, 10534, 10359] |
| erp.warranty_repair_service_quotations.index | admin/customer-care/warranty_repair_service_quotations | {"permission": "all"} | customer_care.bao_gia_dich_vu_sc_bh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_service_quotations.searchData.all | admin/customer-care/warranty_repair_service_quotations/searchData | {"permission": "all"} | customer_care.bao_gia_dich_vu_sc_bh.view | có | permission=all chuỗi phạm vi | datatables |
| erp.warranty_repair_service_quotations.show | admin/customer-care/warranty_repair_service_quotations/{id}/show |  | customer_care.bao_gia_dich_vu_sc_bh.view | có | canView | detail ids=[12740, 12732, 12729, 12739, 12721] |
| erp.warranty_repair_service_quotations.searchData.warranty | admin/customer-care/warranty_repair_service_quotations/searchData | {"permission": "index", "type": "warranty"} | customer_care.phieu_bao_hanh.create |  | Tạo phiếu bảo hành | datatables |
| erp.warranty_repair_contracts.index | admin/customer-care/warranty_repair_contracts | {"type": "all"} | customer_care.hop_dong_dich_vu_sc_bh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_contracts.searchData.all | admin/customer-care/warranty_repair_contracts/searchData | {"type": "all"} | customer_care.hop_dong_dich_vu_sc_bh.view | có | type=all chuỗi phạm vi | datatables |
| erp.warranty_repair_contracts.show | admin/customer-care/warranty_repair_contracts/{id}/show |  | customer_care.hop_dong_dich_vu_sc_bh.view | có | canView | detail ids=[8509, 8508, 8507, 8505, 8504] |
| erp.warranty_repair_contracts.searchData.assign_task | admin/customer-care/warranty_repair_contracts/searchData | {"type": "assign-task"} | customer_care.phieu_cho_giao_viec.view | có |  | datatables |
| erp.warranty_repair_contract_addition_annexs.index | admin/customer-care/warranty_repair_contract_addition_annexs | {"type": "all"} | customer_care.pl_bo_sung_hop_dong_dich_vu_sc_bh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_contract_addition_annexs.searchData.all | admin/customer-care/warranty_repair_contract_addition_annexs/searchData | {"type": "all"} | customer_care.pl_bo_sung_hop_dong_dich_vu_sc_bh.view | có | type=all chuỗi phạm vi | datatables |
| erp.warranty_repair_contract_annexs.index | admin/customer-care/warranty_repair_contract_annexs | {"type": "all"} | customer_care.pl_giam_hop_dong_dich_vu_sc_bh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.warranty_repair_contract_annexs.searchData.all | admin/customer-care/warranty_repair_contract_annexs/searchData | {"type": "all"} | customer_care.pl_giam_hop_dong_dich_vu_sc_bh.view | có | type=all chuỗi phạm vi | datatables |
| erp.warranty_repair_contract_addition_annexs.show | admin/customer-care/warranty_repair_contract_addition_annexs/{id}/show |  | customer_care.pl_bo_sung_hop_dong_dich_vu_sc_bh.view | có | canView | detail ids=[8512, 8476, 8452] |
| erp.warranty_repair_contract_annexs.show | admin/customer-care/warranty_repair_contract_annexs/{id}/show |  | customer_care.pl_giam_hop_dong_dich_vu_sc_bh.view | có | canView | detail ids=[8479, 8477, 8454, 6506, 5290] |
| erp.wr_warrantys.index | admin/customer-care/wr_warrantys | {"type": "all"} | customer_care.phieu_bao_hanh.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.wr_warrantys.searchData.all | admin/customer-care/wr_warrantys/searchData | {"type": "all"} | customer_care.phieu_bao_hanh.view | có | type=all chuỗi phạm vi | datatables |
| erp.wr_warrantys.show | admin/customer-care/wr_warrantys/{id}/show |  | customer_care.phieu_bao_hanh.view | có | canView | detail ids=[8511, 8510, 8506, 6945, 1356] |
| erp.wr_assign_tasks.index | admin/customer-care/wr_assign_tasks | {"type": "all"} | customer_care.phieu_giao_viec.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.wr_assign_tasks.searchData.all | admin/customer-care/wr_assign_tasks/searchData | {"type": "all"} | customer_care.phieu_giao_viec.view | có | type=all chuỗi phạm vi | datatables |
| erp.wr_assign_tasks.show | admin/customer-care/wr_assign_tasks/{id}/show |  | customer_care.phieu_giao_viec.view | có | canView | detail ids=[18704, 18703, 18705, 18693, 18674] |
| erp.wr_approve_results.index | admin/customer-care/wr_approve_results | {"type": "all"} | customer_care.phieu_duyet_ket_qua.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.wr_approve_results.searchData.all | admin/customer-care/wr_approve_results/searchData | {"type": "all"} | customer_care.phieu_duyet_ket_qua.view | có | type=all chuỗi phạm vi | datatables |
| erp.wr_approve_results.show | admin/customer-care/wr_assign_tasks/{id}/show |  | customer_care.phieu_duyet_ket_qua.view | có | canView (parent_id != null) | detail ids=[18691, 18690, 18683, 18682] |
| erp.wr_import_results.index | admin/customer-care/wr_import_results | {"type": "all"} | customer_care.phieu_nhap_ket_qua.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.wr_import_results.searchData.all | admin/customer-care/wr_import_results/searchData | {"type": "all"} | customer_care.phieu_nhap_ket_qua.view | có | type=all chuỗi phạm vi | datatables |
| erp.wr_import_results.show | admin/customer-care/wr_import_results/{id}/show |  | customer_care.phieu_nhap_ket_qua.view | có | canView | detail ids=[9140, 9139, 9093, 9092] |
| erp.wr_import_results.searchData.wait_approve | admin/customer-care/wr_import_results/searchData | {"type": "wait_approve_result"} | customer_care.phieu_nhap_ket_qua.approve |  |  | datatables |
| erp.handover_acceptance_records.index | admin/customer-care/handover_acceptance_records | {"type": "all"} | customer_care.bien_ban_ban_giao_nghiem_thu.view | có | cờ blade is_big_boss/is_boss/is_manager | html |
| erp.handover_acceptance_records.searchData.all | admin/customer-care/handover_acceptance_records/searchData | {"type": "all"} | customer_care.bien_ban_ban_giao_nghiem_thu.view | có | type=all chuỗi phạm vi | datatables |
| erp.handover_acceptance_records.show | admin/customer-care/handover_acceptance_records/{id}/show |  | customer_care.bien_ban_ban_giao_nghiem_thu.view | có | canView | detail ids=[8273, 8272, 8271, 8270, 8267, 8213] |
| erp.handover_acceptance_product_records.index | admin/accounting/handover_acceptance_product_records | {"type": "all"} | customer_care.bien_ban_giao_nhan.view | có | cờ blade | html |
| erp.handover_acceptance_product_records.searchData.all | admin/accounting/handover_acceptance_product_records/searchData | {"type": "all"} | customer_care.bien_ban_giao_nhan.view | có |  | datatables |
| erp.service_export_requests.index | admin/sale/service-export-requests | {"type": "all"} | customer_care.yeu_cau_lam_dich_vu.view | có | cờ blade | html |
| erp.service_export_requests.searchData.all | admin/sale/service-export-requests/searchData | {"type": "all"} | customer_care.yeu_cau_lam_dich_vu.view | có |  | datatables |
| erp.service_export_requests.searchData.forCustomerCare | admin/sale/service-export-requests/searchData | {"type": "forCustomerCare"} | customer_care.yeu_cau_lam_dich_vu.view|confirm | có | hasAny(tên min3, confirm) | datatables |
| erp.service_export_requests.show | admin/sale/service-export-requests/{id}/show |  | customer_care.yeu_cau_lam_dich_vu.view | có | canView | detail ids=[301, 300, 299, 298, 297, 296] |
| erp.service_accounting_requests.index | admin/sale/service-accounting-requests | {"type": "all"} | customer_care.yeu_cau_hach_toan_lam_dich_vu.view | có | cờ blade | html |
| erp.service_accounting_requests.searchData.all | admin/sale/service-accounting-requests/searchData | {"type": "all"} | customer_care.yeu_cau_hach_toan_lam_dich_vu.view | có |  | datatables |
| erp.service_accounting_requests.show | admin/sale/service-accounting-requests/{id}/show |  | customer_care.yeu_cau_hach_toan_lam_dich_vu.view | có | canView | detail ids=[4074, 4073, 4072, 4071, 4070, 4069] |
| erp.service_accounting.index | admin/sale/service-accounting | {"type": "all"} | customer_care.hach_toan_dich_vu.view | có | cờ blade | html |
| erp.service_accounting.searchData.all | admin/sale/service-accounting/searchData | {"type": "all"} | customer_care.hach_toan_dich_vu.view | có |  | datatables |
| erp.payment_profile.index | admin/assigns/payment_profile | {"type": "all"} | customer_care.ho_so_thanh_toan.view | có | cờ blade | html |
| erp.payment_profile.searchData.all | admin/assigns/payment_profile/searchData | {"type": "all"} | customer_care.ho_so_thanh_toan.view | có |  | datatables |
| erp.payment_profile.searchData.waiting_approver | admin/assigns/payment_profile/searchData | {"type": "waiting_approver"} | customer_care.ho_so_thanh_toan.view + approve | có |  | datatables |
| erp.monthly_commission_accounting_requests.searchData.all | admin/sale/monthly_commission_accounting_requests/searchData | {"type": "all"} | customer_care.phieu.view | có |  | datatables |
| erp.bonus_end_year_settlements.index | admin/accounting/bonus_end_year_settlements |  | customer_care.quyet_toan_nam.create |  | canCreate | html |
| erp.bonus_end_year_settlements.searchData | admin/accounting/bonus_end_year_settlements/searchData |  | customer_care.quyet_toan_nam.view | có |  | datatables |
| erp.zt_design_requirements.index | admin/sale/zt-design-requirements |  | customer_care.phieu_yeu_cau_thiet_ke_san_xuat.view | có | cờ blade | html |
| erp.zt_design_requirements.searchData | admin/sale/zt-design-requirements/searchData |  | customer_care.phieu_yeu_cau_thiet_ke_san_xuat.view | có |  | datatables |
| erp.zt_manufacture_requirements.index | admin/sale/zt-manufacture-requirements |  | customer_care.phieu_yeu_cau_thiet_ke_san_xuat.view | có | cờ blade | html |
| erp.zt_manufacture_requirements.searchData | admin/sale/zt-manufacture-requirements/searchData |  | customer_care.phieu_yeu_cau_san_xuat.view | có |  | datatables |
| erp.warranty_reports.searchData.all | admin/customer-care/warranty_reports/searchData | {"type": "all"} | customer_care.phieu.view | có | phieu >= 3 + FilterDepartmentHelper | datatables |
| erp.warranty_works.searchData.all | admin/customer-care/warranty_works/searchData | {"type": "all"} | customer_care.phieu.view | có | phieu >= 3 + FilterDepartmentHelper | datatables |
| erp.warranty_payment_requests.searchData.all | admin/customer-care/warranty_payment_requests/searchData | {"type": "all"} | customer_care.phieu.view | có | phieu >= 3 + FilterDepartmentHelper | datatables |
| erp.bill_assigns.index | admin/customer-care/bill-assigns | {"type": "all"} | customer_care.thong_bao_hoan_thien_ho_so.view |  | not_found nếu < 4 | html |
| erp.bill_assigns.searchData.all | admin/customer-care/bill-assigns/searchData | {"type": "all"} | customer_care.thong_bao_hoan_thien_ho_so.view | có |  | datatables |
| erp.customer_care_bills.index | admin/customer-care/customer-care-bills | {"type": "all"} | customer_care.thong_bao_hoan_thien_ho_so.view |  | not_found nếu < 4 | html |
| erp.customer_care_questions.index | admin/customer-care/customer-care-questions | {"type": "all"} | customer_care.thong_bao_hoan_thien_ho_so.view |  |  | html |
| erp.device_errors.index | admin/sale/device-errors | {"type": "all"} | customer_care.thong_bao_hoan_thien_ho_so.view |  |  | html |
| erp.install_requests.searchData.approve | admin/tech/install_requests/searchData | {"type": "approve"} | customer_care.lich_lap_dat.manage |  |  | datatables |
| erp.install_plans.searchData.tech | admin/tech/install_plans/searchData | {"type": "tech"} | customer_care.lich_lap_dat.manage |  |  | datatables |
| erp.install_plans.searchData.install_summary | admin/tech/install_plans/searchData | {"type": "install_summary"} | customer_care.lap_dat.manage |  |  | datatables |
| erp.install_summaries.gate | admin/tech/install_summaries |  | customer_care.lap_dat.manage |  | middleware checkPermission | html |
| erp.checksheet.gate | admin/tech/checksheet |  | customer_care.checksheet.manage |  | middleware checkPermission | html |
| erp.job_types.gate | admin/tech/job_types |  | customer_care.kieu_cong_viec.manage |  | middleware checkPermission | html |
| erp.job_norms.gate | admin/tech/job_norms |  | customer_care.dinh_muc_cong.manage |  | middleware checkPermission | html |
| erp.moving_norms.gate | admin/tech/moving_norms |  | customer_care.dinh_muc_cong.manage |  | middleware checkPermission | html |
| erp.services.create.gate | admin/sale/services/create |  | customer_care.danh_muc_goi_bao_duong.create |  | middleware checkPermission | html |
| erp.service_config_price.edit | admin/sale/service-config-price/edit |  | customer_care.gia_dich_vu.update |  | not_found | html |
| erp.report.quotationSuccessRate | admin/reports/quotationSuccessRate |  | customer_care.bao_cao_ti_le_thanh_cong_bao_gia.view | có | show_select_* | html |
| erp.report.quotationCount | admin/reports/quotationCount |  | customer_care.bao_cao_tong_hop_bao_gia.view | có | show_select_* | html |
| erp.report.quotationCountSearchData | admin/reports/quotationCountSearchData | {"from_date": "01/01/2026", "to_date": "31/10/2026"} | customer_care.bao_cao_tong_hop_bao_gia.view | có | Employee::quotationCountSearchData | auto |
| erp.report.customer_care_interval | admin/reports/customer_care_interval |  | customer_care.bao_cao_khach_hang_theo_thoi_gian_cham_soc.view | có | cờ $permissions | html |
| erp.report.customer_care_interval.searchData | admin/reports/customer_care_interval/searchData |  | customer_care.bao_cao_khach_hang_theo_thoi_gian_cham_soc.view | có | filter() | auto |
| erp.report.customer_care_interval_by_employee | admin/reports/customer_care_interval_by_employee |  | customer_care.bao_cao_khach_hang_theo_nhan_vien_kinh_doanh.view | có | cờ $permissions | html |
| erp.report.customer_care_interval_by_employee.searchData | admin/reports/customer_care_interval_by_employee/searchData |  | customer_care.bao_cao_khach_hang_theo_nhan_vien_kinh_doanh.view | có | filter() | auto |
| erp.report_product_export_request | admin/warehouse/product_export_requests/reportProductExportRequest |  | customer_care.bao_cao_danh_sach_khach_hang_can_lien_he_cham_soc.view | có | not_found nếu < 3 + cờ | html |
| erp.report_product_export_request.searchData | admin/warehouse/product_export_requests/searchDataReportProductExportRequest | {"from_date": "01/10/2026", "to_date": "31/10/2026"} | customer_care.bao_cao_danh_sach_khach_hang_can_lien_he_cham_soc.view | có | $permissions | auto |
| erp.liquidation_report | admin/warehouse/warehouse_reports/liquidationReport |  | customer_care.bao_cao_hang_thuc_day_ban.view | có | show_select_company | html |
| erp.price_asking_requests.index | admin/orders/price_asking_requests | {"type": "all"} | customer_care.phieu.view | có | @php isBigBoss + Datatable.blade | html |
| erp.price_calculates.index | admin/orders/price_calculates | {"type": "all"} | customer_care.phieu.view | có | @php isBigBoss | html |
| erp.home.topSale.0 | admin/topSale | {"type": 0} | customer_care.thong_ke_dashboard.view | có | chuỗi 4/3 | auto |
| erp.home.topSale.1 | admin/topSale | {"type": 1} | customer_care.thong_ke_dashboard.view | có | chuỗi 4/3 | auto |
| erp.home.topSale.2 | admin/topSale | {"type": 2} | customer_care.thong_ke_dashboard.view | có | chuỗi 4/3 | auto |
| erp.home.approveList | admin/approveList |  | customer_care.* (đếm việc chờ) |  | đếm việc chờ | auto |
| api.warranty_repair_requests.index.all | customer-care/warranty-repair-requests | {"type": "all", "per_page": 100, "page": 1} | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | type=all chuỗi phạm vi | auto |
| api.warranty_repair_requests.options | customer-care/warranty-repair-requests/options |  | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | scopeFlags | lists |
| api.warranty_repair_handle_requests.index.all | customer-care/warranty-repair-handle-requests | {"type": "all", "per_page": 100, "page": 1} | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | type=all chuỗi phạm vi | auto |
| api.warranty_repair_handle_requests.options | customer-care/warranty-repair-handle-requests/options |  | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | scopeFlags | lists |
| api.wr_information_requests.index.all | customer-care/wr-information-requests | {"type": "all", "per_page": 100, "page": 1} | customer_care.phieu_cung_cap_thong_tin.view | có | type=all chuỗi phạm vi | auto |
| api.wr_information_requests.options | customer-care/wr-information-requests/options |  | customer_care.phieu_cung_cap_thong_tin.view | có | scopeFlags | lists |
| api.wr_quotations.index.all | customer-care/wr-quotations | {"type": "all", "per_page": 100, "page": 1} | customer_care.bao_gia_dich_vu_sc_bh.view | có | type=all chuỗi phạm vi | auto |
| api.wr_quotations.options | customer-care/wr-quotations/options |  | customer_care.bao_gia_dich_vu_sc_bh.view | có | scopeFlags | lists |
| api.wr_warranties.index.all | customer-care/wr-warranties | {"type": "all", "per_page": 100, "page": 1} | customer_care.phieu_bao_hanh.view | có | type=all chuỗi phạm vi | auto |
| api.wr_warranties.options | customer-care/wr-warranties/options |  | customer_care.phieu_bao_hanh.view | có | scopeFlags | lists |
| api.wr_service_contracts.index.all | customer-care/wr-service-contracts | {"type": "all", "per_page": 100, "page": 1} | customer_care.hop_dong_dich_vu_sc_bh.view | có | type=all chuỗi phạm vi | auto |
| api.wr_service_contracts.options | customer-care/wr-service-contracts/options |  | customer_care.hop_dong_dich_vu_sc_bh.view | có | scopeFlags | lists |
| api.warranty_repair_requests.index.waiting | customer-care/warranty-repair-requests | {"type": "waiting_handle", "per_page": 100, "page": 1} | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm |  |  | auto |
| api.warranty_repair_handle_requests.index.waiting | customer-care/warranty-repair-handle-requests | {"type": "waiting_information", "per_page": 100, "page": 1} | customer_care.phieu_cung_cap_thong_tin.create |  |  | auto |
| api.warranty_repair_requests.show | customer-care/warranty-repair-requests/{id} |  | customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | canView | detail ids=[7090, 7089, 5819, 5750, 6815] |
| api.warranty_repair_handle_requests.show | customer-care/warranty-repair-handle-requests/{id} |  | customer_care.phieu_xu_ly_yeu_cau_di_kiem_tra_sua_chua_bao_hanh.view | có | canView | detail ids=[6624, 6623, 5413, 5373, 5312] |
| api.wr_information_requests.show | customer-care/wr-information-requests/{id} |  | customer_care.phieu_cung_cap_thong_tin.view | có | canView | detail ids=[12738, 12737, 12734, 10534, 10359] |
| api.wr_quotations.show | customer-care/wr-quotations/{id} |  | customer_care.bao_gia_dich_vu_sc_bh.view | có | canView | detail ids=[12740, 12732, 12729, 12739, 12721] |
| api.wr_warranties.show | customer-care/wr-warranties/{id} |  | customer_care.phieu_bao_hanh.view | có | canView | detail ids=[8511, 8510, 8506, 6945, 1356] |
| api.wr_service_contracts.show | customer-care/wr-service-contracts/{id} |  | customer_care.hop_dong_dich_vu_sc_bh.view | có | canView | detail ids=[8509, 8508, 8507, 8505, 8504] |
| api.levels.gate | customer-care/levels | {"per_page": 20, "page": 1} | customer_care.cap_dich_vu_bao_duong.manage|view |  | middleware | auto |
| api.costs.gate | customer-care/costs | {"per_page": 20, "page": 1} | customer_care.dich_vu_sua_chua_va_chi_phi_khac.manage|view |  | middleware | auto |
| api.note_maintenances.gate | customer-care/note-maintenances | {"per_page": 20, "page": 1} | customer_care.ghi_chu_kiem_tra_bao_duong.manage|view |  | middleware | auto |
| api.device_errors.gate | customer-care/device-errors | {"per_page": 20, "page": 1} | customer_care.danh_muc_cong_viec_loi_thiet_bi.manage |  | middleware | auto |
| api.serials.gate | customer-care/serials | {"per_page": 20, "page": 1} | customer_care.danh_muc_serial_thiet_bi_lam_dich_vu.view |  | middleware | auto |
| api.service_price_config.gate | customer-care/service-price-config | {"per_page": 20, "page": 1} | customer_care.gia_dich_vu.update (erpPermission) |  | middleware | auto |

## Không chụp HTTP (phủ bằng golden ERP `CustomerCareScopeConversionTest` / PHPUnit hrm-api `CustomerCareScopeCodesTest`)

- Partial dùng chung `partials/classes/base/Datatable.blade.php`, `DatatableSearchModal.blade.php` (cờ `this.is_big_boss = …` — ScopeSnapshot chỉ bắt `is_*: true|false`): golden render partial lấy cờ.
- `FilterDepartmentHelper::applyFilterWithCreatedBy / applyFilterWidthCreatedByOrRequested` (dùng ở ~10 model kho/đơn hàng): golden SQL.
- `Employee::dashboard_infos`, báo cáo khách hàng theo thời gian chăm sóc (controller bọc dd()): golden DB::pretend.
- `CustomerManagerService` (hrm-api, module Assign — báo giá/hợp đồng dịch vụ trong màn khách hàng): PHPUnit.
- Thông báo/người nhận (sendNotifyWith*, Employee::permission, holders): đổi tên không phạm vi → mã, cùng tập người (test tương đương tên ⇔ mã).
