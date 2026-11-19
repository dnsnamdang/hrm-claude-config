# sale — đường đọc chụp mốc (GĐ3 Task 8.16)

Sinh bằng `scratchpad/sale/gen_routes_sale.py` từ route:list ERP + funcmap tên sale theo hàm. 7 tài khoản: pv4=13 (namdangit — sale: 46 mã mức 4, 2 mức 2, cty 1), pv3=207 (hantt.kthn — 31 mức 3, 5 mức 4, cty 1), pv2=24 (tuannd.kd1 — 32 mức 2, 2 mức 4, cty 1), pv1=110 (honglv.pt — 27 mức 1, 4 mức 2, 1 mức 4, cty 1), tron=145 (nguyetdtm.nshn — 8 mức 4, 4 mức 3, cty 1), cty4=901 (sonll.tpsg — 33 mức 3, 2 mức 4, cty 4), khong_ma=336 (honglt.khohn — 0 mã sale.*, cty 1).

Ngày báo cáo ERP: thăm dò d/m/Y và Y-m-d bằng TK pv4, giữ bản trả 200 (ghi ở cột ghi chú).

Bỏ khỏi mốc HTTP (> 45–60 s, php -S trả 500 ở 60 s) — phủ bằng golden `SaleScopeConversionTest` theo từng mã:
- `erp.report.marketPlanAreaMonthSearchData` — > 45–60 s (php -S trả 500 ở 60 s) — phủ bằng golden theo từng mã
- `erp.report.marketPlanDepartmentByCustomerSearchData` — > 45–60 s (php -S trả 500 ở 60 s) — phủ bằng golden theo từng mã
- `erp.report.salePlanAreaByTimeSearchData` — > 45–60 s (php -S trả 500 ở 60 s) — phủ bằng golden theo từng mã
- `erp.report.planDepartmentByGroupCustomerSearchData` — > 45–60 s (php -S trả 500 ở 60 s) — phủ bằng golden theo từng mã
- `erp.report.salesDepartmentGroupCustomerSearchData` — > 45–60 s (php -S trả 500 ở 60 s) — phủ bằng golden theo từng mã

| app | method | url | tham số | mã quyền | chuỗi phạm vi? | cột lọc / cách lấy |
|---|---|---|---|---|---|---|
| erp | GET | `admin/contracts` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/contracts/listContractEligibleMonthlyAccounting` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/contracts/listContractWaitingSettlement` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/contracts/install` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/contracts/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/contracts/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/contracts/searchData` | type=approved | sale.hop_dong.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/contracts/searchData` | type=department | sale.hop_dong.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/contracts/searchData` | type=waiting | sale.hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/contracts/{id}/show` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/quotations` |  | sale.bao_gia.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/quotations/all` |  | sale.bao_gia.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/quotations/searchData` |  | sale.bao_gia.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/quotations/searchData` | type=all | sale.bao_gia.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/quotations/searchData` | type=approved | sale.bao_gia.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/quotations/searchData` | type=department | sale.bao_gia.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/quotations/{id}/show` |  | sale.bao_gia.view | có | canView (detail)  |
| erp | GET | `admin/accounting/opening-contracts` |  | sale.hop_dong_ban_dau_ky.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/accounting/opening-contracts/searchData` |  | sale.hop_dong_ban_dau_ky.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/accounting/opening-contracts/searchData` | type=all | sale.hop_dong_ban_dau_ky.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/accounting/opening-contracts/searchData` | type=create_bill | sale.hop_dong_ban_dau_ky.view | có | searchByFilter type=create_bill (datatables)  |
| erp | GET | `admin/accounting/opening-contracts/{id}/show` |  | sale.hop_dong_ban_dau_ky.view | có | canView (detail)  |
| erp | GET | `admin/division_market/department` |  | sale.phan_chia_thi_truong_phong_ban.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/division_market/department/forApprover` |  | sale.phan_chia_thi_truong_phong_ban.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/division_market/department/searchData` |  | sale.phan_chia_thi_truong_phong_ban.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/division_market/department/{id}/show` |  | sale.phan_chia_thi_truong_phong_ban.view | có | canView (detail)  |
| erp | GET | `admin/division_market/employee` |  | sale.phan_chia_thi_truong_nhan_vien.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/division_market/employee/forApprover` |  | sale.phan_chia_thi_truong_nhan_vien.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/division_market/employee/searchData` |  | sale.phan_chia_thi_truong_nhan_vien.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/division_market/employee/searchData` | type=for-approved | sale.phan_chia_thi_truong_nhan_vien.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/division_market/employee/{id}/show` |  | sale.phan_chia_thi_truong_nhan_vien.view | có | canView (detail)  |
| erp | GET | `admin/insurance/accounting-insurance` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/insurance/accounting-insurance/searchData` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/insurance/accounting-insurance/searchData` | type=all | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/insurance/accounting-insurance/searchData` | type=wait_approve | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=wait_approve (datatables)  |
| erp | GET | `admin/insurance/accounting-requests-insurance` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/insurance/accounting-requests-insurance/searchData` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/insurance/accounting-requests-insurance/searchData` | type=all | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/insurance/accounting-requests-insurance/searchData` | type=wait_approve | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=wait_approve (datatables)  |
| erp | GET | `admin/orders/price_asking_requests` |  | sale.yeu_cau_hoi_gia.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/price_asking_requests/searchData` |  | sale.yeu_cau_hoi_gia.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/orders/price_asking_requests/searchData` | type=approve | sale.yeu_cau_hoi_gia.view | có | searchByFilter type=approve (datatables)  |
| erp | GET | `admin/orders/price_asking_requests/searchData` | type=calculate | sale.yeu_cau_hoi_gia.view | có | searchByFilter type=calculate (datatables)  |
| erp | GET | `admin/orders/price_asking_requests/searchData` | type=xnk_approve | sale.yeu_cau_hoi_gia.view | có | searchByFilter type=xnk_approve (datatables)  |
| erp | GET | `admin/orders/price_asking_requests/{id}/show` |  | sale.yeu_cau_hoi_gia.view | có | canView (detail)  |
| erp | GET | `admin/orders/price_calculates` |  | sale.tinh_gia_ban.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/price_calculates/searchData` |  | sale.tinh_gia_ban.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/orders/price_calculates/searchData` | type=all | sale.tinh_gia_ban.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/orders/price_calculates/{id}/show` |  | sale.tinh_gia_ban.view | có | canView (detail)  |
| erp | GET | `admin/orders/price_calculate_requests` |  | sale.yeu_cau_tinh_gia_ban.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/price_calculate_requests/searchData` |  | sale.yeu_cau_tinh_gia_ban.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/orders/price_calculate_requests/searchData` | type=approve | sale.yeu_cau_tinh_gia_ban.view | có | searchByFilter type=approve (datatables)  |
| erp | GET | `admin/orders/price_calculate_requests/searchData` | type=calculate | sale.yeu_cau_tinh_gia_ban.view | có | searchByFilter type=calculate (datatables)  |
| erp | GET | `admin/orders/price_calculate_requests/{id}/show` |  | sale.yeu_cau_tinh_gia_ban.view | có | canView (detail)  |
| erp | GET | `admin/plan/market/company` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/market/company/forApprover` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/market/company/searchData` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/market/company/searchData` | type=for-approved | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/market/company/{id}/show` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | canView (detail)  |
| erp | GET | `admin/plan/market/department` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/market/department/forApprover` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/market/department/searchData` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/market/department/searchData` | type=for-approved | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/market/department/{id}/show` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | canView (detail)  |
| erp | GET | `admin/plan/market/employee` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/market/employee/forApprover` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/market/employee/searchData` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/market/employee/searchData` | type=for-approved | sale.ke_hoach_phat_trien_thi_truong.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/market/employee/{id}/show` |  | sale.ke_hoach_phat_trien_thi_truong.view | có | canView (detail)  |
| erp | GET | `admin/plan/sale/company` |  | sale.ke_hoach_ban_hang.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/sale/company/forApprover` |  | sale.ke_hoach_ban_hang.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/sale/company/searchData` |  | sale.ke_hoach_ban_hang.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/sale/company/searchData` | type=for-approved | sale.ke_hoach_ban_hang.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/sale/company/{id}/show` |  | sale.ke_hoach_ban_hang.view | có | canView (detail)  |
| erp | GET | `admin/plan/sale/department` |  | sale.ke_hoach_ban_hang.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/sale/department/forApprover` |  | sale.ke_hoach_ban_hang.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/sale/department/searchData` |  | sale.ke_hoach_ban_hang.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/sale/department/searchData` | type=for-approved | sale.ke_hoach_ban_hang.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/sale/department/{id}/show` |  | sale.ke_hoach_ban_hang.view | có | canView (detail)  |
| erp | GET | `admin/plan/sale/employee` |  | sale.ke_hoach_ban_hang.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/plan/sale/employee/forApprover` |  | sale.ke_hoach_ban_hang.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/plan/sale/employee/searchData` |  | sale.ke_hoach_ban_hang.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/plan/sale/employee/searchData` | type=for-approved | sale.ke_hoach_ban_hang.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/plan/sale/employee/{id}/show` |  | sale.ke_hoach_ban_hang.view | có | canView (detail)  |
| erp | GET | `admin/orders/buy-service-accounting` |  | sale.hach_toan_mua_dich_vu.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/buy-service-accounting/searchData` | type=all | sale.hach_toan_mua_dich_vu.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/orders/buy-service-accounting/searchData` | type=index | sale.hach_toan_mua_dich_vu.view | có | searchByFilter type=index (datatables)  |
| erp | GET | `admin/orders/buy-service-accounting/{id}/show` |  | sale.hach_toan_mua_dich_vu.view | có | canView (detail)  |
| erp | GET | `admin/orders/buy-service-accounting-request` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/buy-service-accounting-request/searchData` | type=all | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/orders/buy-service-accounting-request/searchData` | type=for-approve | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=for-approve (datatables)  |
| erp | GET | `admin/orders/buy-service-accounting-request/searchData` | type=index | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | searchByFilter type=index (datatables)  |
| erp | GET | `admin/orders/buy-service-accounting-request/{id}/show` |  | sale.yeu_cau_hach_toan_dich_vu_can_mua.view | có | canView (detail)  |
| erp | GET | `admin/orders/buy-service-request` |  | sale.yeu_cau_mua_dich_vu.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/buy-service-request/searchData` | type=all | sale.yeu_cau_mua_dich_vu.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/orders/buy-service-request/searchData` | type=can_create_contract | sale.yeu_cau_mua_dich_vu.view | có | searchByFilter type=can_create_contract (datatables)  |
| erp | GET | `admin/orders/buy-service-request/searchData` | type=for-approve | sale.yeu_cau_mua_dich_vu.view | có | searchByFilter type=for-approve (datatables)  |
| erp | GET | `admin/orders/buy-service-request/searchData` | type=index | sale.yeu_cau_mua_dich_vu.view | có | searchByFilter type=index (datatables)  |
| erp | GET | `admin/orders/buy-service-request/{id}/show` |  | sale.yeu_cau_mua_dich_vu.view | có | canView (detail)  |
| erp | GET | `admin/sale/contract_annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/contract_annexes/all` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/sale/contract_annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/contract_annexes/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/contract_annexes/searchData` | type=approve | sale.hop_dong.view | có | searchByFilter type=approve (datatables)  |
| erp | GET | `admin/sale/contract_annexes/searchData` | type=approved | sale.hop_dong.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/sale/contract_annexes/searchData` | type=department | sale.hop_dong.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/sale/contract_annexes/searchData` | type=waiting | sale.hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` | type=approve | sale.hop_dong.view | có | searchByFilter type=approve (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` | type=approved | sale.hop_dong.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` | type=department | sale.hop_dong.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/sale/contract_term_annexes/searchData` | type=waiting | sale.hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/liquidation_records` |  | sale.bien_ban_thanh_ly_hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/liquidation_records/searchData` |  | sale.bien_ban_thanh_ly_hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/liquidation_records/searchData` | type=all | sale.bien_ban_thanh_ly_hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/liquidation_records/searchData` | type=waiting | sale.bien_ban_thanh_ly_hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/liquidation_records/{id}/show` |  | sale.bien_ban_thanh_ly_hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/project_contracts` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/project_contracts/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/project_quotations` |  | sale.bao_gia.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/project_quotations/searchData` |  | sale.bao_gia.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/project_quotations/{id}/show` |  | sale.bao_gia.view | có | canView (detail)  |
| erp | GET | `admin/sale/service_contracts` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/service_contracts/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=approved | sale.hop_dong.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=department | sale.hop_dong.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=waiting | sale.hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=valid_waiting | sale.hop_dong.view | có | searchByFilter type=valid_waiting (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=create_bill | sale.hop_dong.view | có | searchByFilter type=create_bill (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=liquidation_record | sale.hop_dong.view | có | searchByFilter type=liquidation_record (datatables)  |
| erp | GET | `admin/sale/service_contracts/searchData` | type=can_export | sale.hop_dong.view | có | searchByFilter type=can_export (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/service_contract_annexes/all` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` | type=approve | sale.hop_dong.view | có | searchByFilter type=approve (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` | type=approved | sale.hop_dong.view | có | searchByFilter type=approved (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` | type=department | sale.hop_dong.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/sale/service_contract_annexes/searchData` | type=waiting | sale.hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/service_contract_addition_annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/service_contract_addition_annexes/all` |  | sale.hop_dong.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/sale/service_contract_addition_annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/service_contract_addition_annexes/searchData` | type=all | sale.hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/service_quotations` |  | sale.bao_gia.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/service_quotations/ofDepartment` |  | sale.bao_gia.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/sale/service_quotations/searchData` |  | sale.bao_gia.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/service_quotations/searchData` | type=all | sale.bao_gia.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/service_quotations/searchData` | type=contract | sale.bao_gia.view | có | searchByFilter type=contract (datatables)  |
| erp | GET | `admin/sale/service_quotations/searchData` | type=department | sale.bao_gia.view | có | searchByFilter type=department (datatables)  |
| erp | GET | `admin/sale/settlement_contracts` |  | sale.quyet_toan_hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/settlement_contracts/searchData` |  | sale.quyet_toan_hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/settlement_contracts/searchData` | type=accounting | sale.quyet_toan_hop_dong.view | có | searchByFilter type=accounting (datatables)  |
| erp | GET | `admin/sale/settlement_contracts/searchData` | type=all | sale.quyet_toan_hop_dong.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/sale/settlement_contracts/searchData` | type=waiting | sale.quyet_toan_hop_dong.view | có | searchByFilter type=waiting (datatables)  |
| erp | GET | `admin/sale/settlement_contracts/{id}/show` |  | sale.quyet_toan_hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/target/company` |  | sale.chi_tieu_kinh_doanh.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/target/company/forApprover` |  | sale.chi_tieu_kinh_doanh.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/target/company/searchData` |  | sale.chi_tieu_kinh_doanh.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/target/company/searchData` | type=for-approved | sale.chi_tieu_kinh_doanh.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/target/company/{id}/show` |  | sale.chi_tieu_kinh_doanh.view | có | canView (detail)  |
| erp | GET | `admin/target/department` |  | sale.chi_tieu_kinh_doanh.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/target/department/forApprover` |  | sale.chi_tieu_kinh_doanh.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/target/department/searchData` |  | sale.chi_tieu_kinh_doanh.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/target/department/searchData` | type=for-approved | sale.chi_tieu_kinh_doanh.view | có | searchByFilter type=for-approved (datatables)  |
| erp | GET | `admin/target/department/{id}/show` |  | sale.chi_tieu_kinh_doanh.view | có | canView (detail)  |
| erp | GET | `admin/target/product` |  | sale.chi_tieu_phat_trien_san_pham.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/target/product/searchData` |  | sale.chi_tieu_phat_trien_san_pham.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/delivery_requests` |  | sale.phieu_yeu_cau_van_chuyen.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/delivery_requests/for-approve` |  | sale.phieu_yeu_cau_van_chuyen.view | có | cờ blade / middleware (html)  |
| erp | GET | `admin/delivery_requests/searchData` | type=all | sale.phieu_yeu_cau_van_chuyen.view | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/delivery_requests/searchData` | type=for-approve | sale.phieu_yeu_cau_van_chuyen.view | có | searchByFilter type=for-approve (datatables)  |
| erp | GET | `admin/delivery_requests/searchData` | type=index | sale.phieu_yeu_cau_van_chuyen.view | có | searchByFilter type=index (datatables)  |
| erp | GET | `admin/sale/firm-contracts` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/firm-contracts/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/firm-contracts/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/firm-contracts-annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/firm-contracts-annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/firm-contracts-annexes/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/firm-contracts-addition-annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/firm-contracts-addition-annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/firm-contracts-addition-annexes/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/zt-firm-contracts` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/zt-firm-contracts/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/zt-firm-contracts/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/zt-firm-contracts-annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/zt-firm-contracts-annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/zt-firm-contracts-annexes/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/zt-firm-contracts-addition-annexes` |  | sale.hop_dong.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/zt-firm-contracts-addition-annexes/searchData` |  | sale.hop_dong.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/zt-firm-contracts-addition-annexes/{id}` |  | sale.hop_dong.view | có | canView (detail)  |
| erp | GET | `admin/sale/firm-quotations` |  | sale.bao_gia.view | có | cờ blade is_* (html)  |
| erp | GET | `admin/sale/firm-quotations/searchData` |  | sale.bao_gia.view | có | searchByFilter type=None (datatables)  |
| erp | GET | `admin/sale/firm-quotations/{id}/show` |  | sale.bao_gia.view | có | canView (detail)  |
| erp | GET | `admin/orders/buy-service-contract` |  | (sale.* popup) | có | cờ blade is_* (html)  |
| erp | GET | `admin/orders/buy-service-contract/searchData` | type=all | (sale.* popup) | có | searchByFilter type=all (datatables)  |
| erp | GET | `admin/orders/buy-service-contract/{id}/show` |  | (sale.* popup) | có | canView (detail)  |
| erp | GET | `admin/contracts/listContractEligibleMonthlyAccountingData` |  | sale.hop_dong_cho_quyet_toan.view | có | searchByFilter (auto)  |
| erp | GET | `admin/contracts/listContractWaitingSettlementData` |  | sale.hop_dong_cho_quyet_toan.view | có | searchByFilter (auto)  |
| erp | GET | `admin/modal_data/searchContract` |  | sale.hop_dong.view (popup HĐ) | có | searchByFilter (auto)  |
| erp | GET | `admin/reports/detailTripReport` |  | sale.bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/transportByStaff` |  | sale.bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/revenue-contract` |  | sale.bao_cao_theo_doi_chi_tieu_kd_theo_thoi_gian.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/revenue-contract/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_theo_doi_chi_tieu_kd_theo_thoi_gian.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/bonus-business-contract` |  | sale.bao_cao_chi_phi_ban_hang_theo_hop_dong.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/bonus-business-contract/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_chi_phi_ban_hang_theo_hop_dong.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/bonus-business-employee` |  | sale.bao_cao_thuong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/sale-product` |  | sale.bao_cao_ban_hang_theo_hang_hoa.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/sale-product/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_ban_hang_theo_hang_hoa.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/market-commodity` |  | sale.bao_cao_thi_truong_theo_hang_hoa.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-commodity/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thi_truong_theo_hang_hoa.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/market-plan-department` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-department/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/market-area-department` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-area-department/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/market-area-month` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-group-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-group-customer/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/market-plan-department-group-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-department-group-customer/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/market-plan-detail-department-group-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-detail-department-group-customer/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/market-plan-province-time` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-province-time/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/handle-debt-bad` |  | sale.bao_cao_xu_ly_no_xau.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/handle-debt-bad/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_xu_ly_no_xau.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/handle-debt-overdue` |  | sale.bao_cao_xu_ly_no_qua_han.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/handle-debt-overdue/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_xu_ly_no_qua_han.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/warning-debt_due_date` |  | sale.canh_bao_thu_no_den_han.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/warning-debt_due_date/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.canh_bao_thu_no_den_han.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/monitor_contract_implement` |  | sale.bao_cao_theo_doi_thuc_hien_hop_dong.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/monitor_contract_implement/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_theo_doi_thuc_hien_hop_dong.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/revenue_standard_employee` |  | sale.bao_cao_doanh_so_tieu_chuan_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/revenue_standard_employee/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_doanh_so_tieu_chuan_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/revenue_standard_contract` |  | sale.bao_cao_chi_tiet_doanh_so_tieu_chuan_theo_1_hop_dong.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/revenue_standard_contract/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_chi_tiet_doanh_so_tieu_chuan_theo_1_hop_dong.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/by_sales_staff` |  | sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/by_sales_staff/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/market-plan-department-by-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-compare-by-province` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/market-plan-compare-by-province-searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/warranty_repair_service` |  | sale.bao_cao_lam_dich_vu_bao_hanh_sua_chua_bao_duong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/warranty_repair_service/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_lam_dich_vu_bao_hanh_sua_chua_bao_duong.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/warranty_repair_service_by_customer` |  | sale.bao_cao_so_luot_sua_chua_bao_duong_cho_1_khach_hang.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/warranty_repair_service_by_customer/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_so_luot_sua_chua_bao_duong_cho_1_khach_hang.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/compare-contract-by-time` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/compare-contract-by-time/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/plan-area-by-time` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/compare-contract-by-province` |  | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/compare-contract-by-province/searchData` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_phat_trien_thi_truong_theo_nhan_vien.view | có | báo cáo (auto) ngày ymd |
| erp | GET | `admin/reports/plan-department-by-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_cua_phong_ban_theo_khach_hang.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-department-by-customer-searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_cua_phong_ban_theo_khach_hang.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/plan-department-by-group-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhom_khach_hang_chi_tiet.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-department-by-employee` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-department-by-employee-searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/plan-department-by-province` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-department-by-province-searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/sales-department-by-group-customer` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-sales-customer-group` |  | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/plan-sales-customer-group-searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_thuc_hien_ke_hoach_ban_hang_theo_nhan_vien.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/target-bussines-employee` |  | sale.bao_cao_giao_chi_tieu_kinh_doanh_theo_phong_ban.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/target-bussines-employee/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_giao_chi_tieu_kinh_doanh_theo_phong_ban.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/reports/target-bussines-department` |  | sale.bao_cao_giao_chi_tieu_kinh_doanh_theo_phong_ban.view | có | báo cáo (html)  |
| erp | GET | `admin/reports/target-bussines-department/searchData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_giao_chi_tieu_kinh_doanh_theo_phong_ban.view | có | báo cáo (auto) ngày dmy |
| erp | GET | `admin/sale/reports/customer-debt-detailsData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (auto) ngày dmy |
| erp | GET | `admin/sale/reports/compare-customer-debts-data` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (auto) ngày dmy |
| erp | GET | `admin/sale/reports/customer-debt-detail-by-employeeData` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (auto) ngày dmy |
| erp | GET | `admin/sale/reports/customer-debt-details` |  | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (html)  |
| erp | GET | `admin/sale/reports/compare-customer-debts` |  | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (html)  |
| erp | GET | `admin/sale/reports/customer-debt-detail-by-employee` |  | sale.bao_cao_*cong_no_khach_hang* | có | báo cáo công nợ KH (getSelectionCanShow) (html)  |
| erp | GET | `admin/customer-care/reports/customercare/contracts` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.hop_dong.view|sale.bao_gia.view | có | CustomerCareReportService (auto) ngày ymd |
| erp | GET | `admin/customer-care/reports/customercare/quotations` | year=2026, from_month=1, to_month=10, date_from=2026-01-01, date_to=2026-10-31, from_date=2026-01-01, to_date=2026-10-31, startDate=2026-01-01, endDate=2026-10-31, year_c=2025, year_p=2025 | sale.hop_dong.view|sale.bao_gia.view | có | CustomerCareReportService (auto) ngày ymd |
| erp | GET | `admin/reports/quotation_count/print` | year=2026, from_month=1, to_month=10, date_from=01/01/2026, date_to=31/10/2026, from_date=01/01/2026, to_date=31/10/2026, startDate=01/01/2026, endDate=31/10/2026, year_c=2025, year_p=2025 | sale.bao_gia.view | có | Employee::quotationCount* (html)  |
| erp | GET | `admin/sale/project_analysis` |  | Tạo phân tích dự án | không | middleware (html)  |
| erp | GET | `admin/sale/project_analysis/searchData` |  | Tạo phân tích dự án | không | middleware (html)  |
| erp | GET | `admin/support-accounting` |  | Xem danh danh sách hỗ trợ hạch toán | không | middleware (html)  |
| erp | GET | `admin/support-accounting/searchData` |  | Xem danh danh sách hỗ trợ hạch toán | không | middleware (html)  |
| erp | GET | `admin/approveList` |  | sale.*.approve (đếm việc chờ) | có | đếm việc chờ (lists)  |
| erp | GET | `admin/quotations` | menu=1 | topmenubar | không | html (html) trang + menu (băm nội dung) |
| api | GET | `assign/contracts` | limit=100 | sale.hop_dong_du_an_tkt.view | có |  (auto)  |
| api | GET | `finance/delivery-requests` | type=all | sale.phieu_yeu_cau_van_chuyen.view | có |  (auto)  |
| api | GET | `finance/delivery-requests` |  | sale.phieu_yeu_cau_van_chuyen.view | có |  (auto)  |
| api | GET | `finance/buy-service-requests` | type=all | sale.yeu_cau_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-requests` |  | sale.yeu_cau_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-requests` | type=for-approve | sale.yeu_cau_mua_dich_vu_*.approve | có |  (auto)  |
| api | GET | `finance/buy-service-accounting-requests` | type=all | sale.yeu_cau_hach_toan_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-accounting-requests` |  | sale.yeu_cau_hach_toan_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-accountings` | type=all | sale.hach_toan_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-accountings` |  | sale.hach_toan_mua_dich_vu.view | có |  (auto)  |
| api | GET | `finance/buy-service-accountings/catalogs` |  | sale.hach_toan_mua_dich_vu.create (mw) | có |  (auto)  |
| api | GET | `finance/due-configs` |  | sale.cau_hinh_chan_luong_hang_qua_han.configure (mw) | có |  (auto)  |
| api | GET | `finance/customer-debt-details` | date_from=2026-01-01, date_to=2026-10-31, start_date=2026-01-01, end_date=2026-10-31 | sale.bao_cao_chi_tiet_cong_no_khach_hang.view | có |  (auto)  |
| api | GET | `finance/customer-debt-details/meta` |  | sale.bao_cao_chi_tiet_cong_no_khach_hang.view | có |  (auto)  |
| api | GET | `finance/customer-debt-by-employee` | date_from=2026-01-01, date_to=2026-10-31, start_date=2026-01-01, end_date=2026-10-31 | sale.bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.view | có |  (auto)  |
| api | GET | `finance/customer-debt-by-employee/meta` |  | sale.bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.view | có |  (auto)  |
| api | GET | `finance/customer-debt-compare` | date_from=2026-01-01, date_to=2026-10-31, start_date=2026-01-01, end_date=2026-10-31 | sale.bao_cao_doi_soat_cong_no_khach_hang.view | có |  (auto)  |
| api | GET | `finance/customer-debt-compare/meta` |  | sale.bao_cao_doi_soat_cong_no_khach_hang.view | có |  (auto)  |
| api | GET | `finance/transport-cost-by-staff` | date_from=2026-01-01, date_to=2026-10-31 | sale.bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.view | có |  (auto)  |
| api | GET | `finance/transport-cost-by-staff/meta` |  | sale.bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.view | có |  (auto)  |
| api | GET | `finance/prepick-tracking` |  | sale.bao_cao_giu_hang.view | có |  (auto)  |
| api | GET | `finance/prepick-tracking/meta` |  | sale.bao_cao_giu_hang.view | có |  (auto)  |
