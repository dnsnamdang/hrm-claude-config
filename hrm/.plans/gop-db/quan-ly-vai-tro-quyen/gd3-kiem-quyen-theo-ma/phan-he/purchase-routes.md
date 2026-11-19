# purchase — đường đọc chụp mốc (GĐ3 Task 8.15)

Sinh từ `purchase-routes.json` (máy đọc). Chụp bằng `hrm-api/tests/Support/ScopeSnapshot.php` (tokens | run | diff), 3 tiến trình song song theo nhóm tài khoản (ghép `ket_qua`). ERP chạy tạm `php -S 127.0.0.1:8012` (DB rehearsal + DB_DATABASE_HRM rehearsal). purchase chỉ có ở ERP (catalog 88 mã, mọi mã `platforms [erp]`, mọi alias guard web; hrm-api/hrm-client 0 chỗ kiểm tên purchase) ⇒ không route hrm-api.
Tham số loại danh sách: dò từng model — `_type` nếu model so `$request->_type == "<loại>"`, ngược lại `type`. Báo cáo: `current_page=1&per_page=50&page=1`, không lọc ngày.

## Tài khoản (rehearsal, chỉ SELECT)

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — purchase: 46 mã mức 4, 1 mức 2, cty 1 |
| pv3 | 207 | hantt.kthn — 29 mức 3, 3 mức 4, 1 mức 2, cty 1 |
| pv2 | 24 | tuannd.kd1 — 17 mức 2, 1 mức 3, cty 1 |
| pv1 | 110 | honglv.pt — 9 mức 1, 4 mức 2, cty 1 |
| tron | 157 | huongttt.kddau — 14 mức 4, 6 mức 3, 14 mức 2, cty 1 |
| cty4 | 901 | sonll.tpsg — 31 mức 3, 2 mức 4, cty 4 |
| khong_ma | 145 | nguyetdtm.nshn — 0 mã purchase.*, cty 1 |

Ca thiếu (chỉ PHPUnit golden `PurchaseScopeConversionTest`): có mã không phạm vi (null), mã ở công ty khác qua Vai trò (c2), từng mã riêng lẻ ở từng mức, mức bộ phận (1) cho mã có 4 mức (110 chỉ có ở 9 mã).

## Route (242, toàn ERP) × 7 tài khoản = 1694 ô

| id | url | tham số | mã | cột lọc / cách đọc | extract |
|---|---|---|---|---|---|
| erp.assign_employee.index | admin/assign/employee |  | purchase.phieu_phan_cong_nhan_vien_phu_trach.view | cờ blade is_* | html |
| erp.assign_employee.searchData.all | admin/assign/employee/searchData | {"type": "all"} | purchase.phieu_phan_cong_nhan_vien_phu_trach.view | searchByFilter type=all | datatables |
| erp.assign_employee.searchData.none | admin/assign/employee/searchData |  | purchase.phieu_phan_cong_nhan_vien_phu_trach.view | searchByFilter type=None | datatables |
| erp.assign_employee.show | admin/assign/employee/{id}/show |  | purchase.phieu_phan_cong_nhan_vien_phu_trach.view | canView | detail ids=[1170, 1169, 1168, 1167, 1166, 1165] |
| erp.buy_debt_contract_beginning.index | admin/accounting/buy-debt-contract-beginning |  | purchase.hop_dong_mua_dau_ky.view | cờ blade is_* | html |
| erp.buy_debt_contract_beginning.searchData.all | admin/accounting/buy-debt-contract-beginning/searchData | {"type": "all"} | purchase.hop_dong_mua_dau_ky.view | searchByFilter type=all | datatables |
| erp.buy_debt_contract_beginning.searchData.none | admin/accounting/buy-debt-contract-beginning/searchData |  | purchase.hop_dong_mua_dau_ky.view | searchByFilter type=None | datatables |
| erp.buy_debt_contract_beginning.show | admin/accounting/buy-debt-contract-beginning/{id}/show |  | purchase.hop_dong_mua_dau_ky.view | canView | detail ids=[1978, 1977, 1976, 1975, 1974, 1973] |
| erp.insurance_additional.index | admin/insurance/additional-insurance |  | purchase.bao_hiem.view | cờ blade is_* | html |
| erp.insurance_additional.searchData.all | admin/insurance/additional-insurance/searchData | {"type": "all"} | purchase.bao_hiem.view | searchByFilter type=all | datatables |
| erp.insurance_additional.searchData.index | admin/insurance/additional-insurance/searchData | {"type": "index"} | purchase.bao_hiem.view | searchByFilter type=index | datatables |
| erp.insurance_additional.searchData.list | admin/insurance/additional-insurance/searchData | {"type": "list"} | purchase.bao_hiem.view | searchByFilter type=list | datatables |
| erp.insurance_contract.index | admin/insurance/principle-contracts |  | purchase.bao_hiem.view | cờ blade is_* | html |
| erp.insurance_contract.searchData.all | admin/insurance/principle-contracts/searchData | {"type": "all"} | purchase.bao_hiem.view | searchByFilter type=all | datatables |
| erp.insurance_contract.searchData.none | admin/insurance/principle-contracts/searchData |  | purchase.bao_hiem.view | searchByFilter type=None | datatables |
| erp.insurance_form.index | admin/insurance/form-insurance |  | purchase.bao_hiem.view | cờ blade is_* | html |
| erp.insurance_form.searchData.all | admin/insurance/form-insurance/searchData | {"type": "all"} | purchase.bao_hiem.view | searchByFilter type=all | datatables |
| erp.insurance_form.searchData.index | admin/insurance/form-insurance/searchData | {"type": "index"} | purchase.bao_hiem.view | searchByFilter type=index | datatables |
| erp.insurance_form.searchData.list | admin/insurance/form-insurance/searchData | {"type": "list"} | purchase.bao_hiem.view | searchByFilter type=list | datatables |
| erp.insurance_form_after.index | admin/insurance/form-after-insurance |  | purchase.bao_hiem.view | cờ blade is_* | html |
| erp.insurance_form_after.searchData.all | admin/insurance/form-after-insurance/searchData | {"type": "all"} | purchase.bao_hiem.view | searchByFilter type=all | datatables |
| erp.insurance_form_after.searchData.index | admin/insurance/form-after-insurance/searchData | {"type": "index"} | purchase.bao_hiem.view | searchByFilter type=index | datatables |
| erp.insurance_form_after.searchData.list | admin/insurance/form-after-insurance/searchData | {"type": "list"} | purchase.bao_hiem.view | searchByFilter type=list | datatables |
| erp.insurance_form_after.searchData.accept | admin/insurance/form-after-insurance/searchData | {"type": "accept"} | purchase.bao_hiem.view | searchByFilter type=accept | datatables |
| erp.insurance_request.index | admin/insurance/principle-request |  | purchase.bao_hiem.view | cờ blade is_* | html |
| erp.insurance_request.searchData.all | admin/insurance/principle-request/searchData | {"type": "all"} | purchase.bao_hiem.view | searchByFilter type=all | datatables |
| erp.insurance_request.searchData.index | admin/insurance/principle-request/searchData | {"type": "index"} | purchase.bao_hiem.view | searchByFilter type=index | datatables |
| erp.insurance_request.searchData.list | admin/insurance/principle-request/searchData | {"type": "list"} | purchase.bao_hiem.view | searchByFilter type=list | datatables |
| erp.insurance_request.searchData.accept | admin/insurance/principle-request/searchData | {"type": "accept"} | purchase.bao_hiem.view | searchByFilter type=accept | datatables |
| erp.assign_department_brand.index | admin/assign_department_brands |  | purchase.phieu_phan_cong_phong_phu_trach.view | cờ blade is_* | html |
| erp.assign_department_brand.searchData.waiting_approve | admin/assign_department_brands/searchData | {"type": "waiting_approve"} | purchase.phieu_phan_cong_phong_phu_trach.view | searchByFilter type=waiting_approve | datatables |
| erp.assign_department_brand.searchData.waiting_assign_employee | admin/assign_department_brands/searchData | {"type": "waiting_assign_employee"} | purchase.phieu_phan_cong_phong_phu_trach.view | searchByFilter type=waiting_assign_employee | datatables |
| erp.assign_department_brand.searchData.none | admin/assign_department_brands/searchData |  | purchase.phieu_phan_cong_phong_phu_trach.view | searchByFilter type=None | datatables |
| erp.assign_department_brand.show | admin/assign_department_brands/{id}/show |  | purchase.phieu_phan_cong_phong_phu_trach.view | canView | detail ids=[575, 574, 573, 572, 571, 570] |
| erp.buy_contract2.index | admin/orders/buy_contract2 |  | purchase.hop_dong_mua_hang_nhap_khau.view | cờ blade is_* | html |
| erp.buy_contract2.searchData.all | admin/orders/buy_contract2/searchData | {"type": "all"} | purchase.hop_dong_mua_hang_nhap_khau.view | searchByFilter type=all | datatables |
| erp.buy_contract2.searchData.approve | admin/orders/buy_contract2/searchData | {"type": "approve"} | purchase.hop_dong_mua_hang_nhap_khau.view | searchByFilter type=approve | datatables |
| erp.buy_contract2.searchData.index | admin/orders/buy_contract2/searchData | {"type": "index"} | purchase.hop_dong_mua_hang_nhap_khau.view | searchByFilter type=index | datatables |
| erp.buy_contract2.show | admin/orders/buy_contract2/{id}/show |  | purchase.hop_dong_mua_hang_nhap_khau.view | canView | detail ids=[1031, 1030, 1029, 1028, 1027, 1026] |
| erp.firm_warranty_confirm.index | admin/orders/firm_warranty_confirms |  | purchase.phieu_xac_nhan_bao_hanh.view | cờ blade is_* | html |
| erp.firm_warranty_confirm.searchData.all | admin/orders/firm_warranty_confirms/searchData | {"type": "all"} | purchase.phieu_xac_nhan_bao_hanh.view | searchByFilter type=all | datatables |
| erp.firm_warranty_confirm.searchData.for-approved | admin/orders/firm_warranty_confirms/searchData | {"type": "for-approved"} | purchase.phieu_xac_nhan_bao_hanh.view | searchByFilter type=for-approved | datatables |
| erp.firm_warranty_confirm.searchData.none | admin/orders/firm_warranty_confirms/searchData |  | purchase.phieu_xac_nhan_bao_hanh.view | searchByFilter type=None | datatables |
| erp.firm_warranty_confirm.show | admin/orders/firm_warranty_confirms/{id}/show |  | purchase.phieu_xac_nhan_bao_hanh.view | canView | detail ids=[71, 70, 69, 68, 67, 66] |
| erp.firm_warranty_request.index | admin/orders/firm_warranty_requests |  | purchase.phieu_yeu_cau_hang_bao_hanh.view | cờ blade is_* | html |
| erp.firm_warranty_request.searchData.all | admin/orders/firm_warranty_requests/searchData | {"type": "all"} | purchase.phieu_yeu_cau_hang_bao_hanh.view | searchByFilter type=all | datatables |
| erp.firm_warranty_request.searchData.for-approved | admin/orders/firm_warranty_requests/searchData | {"type": "for-approved"} | purchase.phieu_yeu_cau_hang_bao_hanh.view | searchByFilter type=for-approved | datatables |
| erp.firm_warranty_request.searchData.none | admin/orders/firm_warranty_requests/searchData |  | purchase.phieu_yeu_cau_hang_bao_hanh.view | searchByFilter type=None | datatables |
| erp.firm_warranty_request.show | admin/orders/firm_warranty_requests/{id}/show |  | purchase.phieu_yeu_cau_hang_bao_hanh.view | canView | detail ids=[132, 131, 130, 129, 128, 127] |
| erp.firm_warranty.index | admin/orders/firm_warrantys |  | purchase.thu_yeu_cau_hang_bao_hanh.view | cờ blade is_* | html |
| erp.firm_warranty.searchData.all | admin/orders/firm_warrantys/searchData | {"type": "all"} | purchase.thu_yeu_cau_hang_bao_hanh.view | searchByFilter type=all | datatables |
| erp.firm_warranty.searchData.for-approved | admin/orders/firm_warrantys/searchData | {"type": "for-approved"} | purchase.thu_yeu_cau_hang_bao_hanh.view | searchByFilter type=for-approved | datatables |
| erp.firm_warranty.searchData.none | admin/orders/firm_warrantys/searchData |  | purchase.thu_yeu_cau_hang_bao_hanh.view | searchByFilter type=None | datatables |
| erp.firm_warranty.show | admin/orders/firm_warrantys/{id}/show |  | purchase.thu_yeu_cau_hang_bao_hanh.view | canView | detail ids=[79, 78, 77, 76, 75, 73] |
| erp.import_record.index | admin/orders/import-records |  | purchase.hop_dong_mua_hang_nhap_khau.view | cờ blade is_* | html |
| erp.import_record.searchData.all | admin/orders/import-records/searchData | {"type": "all"} | purchase.hop_dong_mua_hang_nhap_khau.view | searchByFilter type=all | datatables |
| erp.import_record.searchData.none | admin/orders/import-records/searchData |  | purchase.hop_dong_mua_hang_nhap_khau.view | searchByFilter type=None | datatables |
| erp.inland_buy_contract.index | admin/orders/inland_buy_contracts |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* | html |
| erp.inland_buy_contract.page.forApprover | admin/orders/inland_buy_contracts/forApprover |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* / middleware | html |
| erp.inland_buy_contract.searchData.approve | admin/orders/inland_buy_contracts/searchData | {"type": "approve"} | purchase.hop_dong_mua_ngoai.view | searchByFilter type=approve | datatables |
| erp.inland_buy_contract.searchData.annexes | admin/orders/inland_buy_contracts/searchData | {"type": "annexes"} | purchase.hop_dong_mua_ngoai.view | searchByFilter type=annexes | datatables |
| erp.inland_buy_contract.searchData.none | admin/orders/inland_buy_contracts/searchData |  | purchase.hop_dong_mua_ngoai.view | searchByFilter type=None | datatables |
| erp.inland_buy_contract.show | admin/orders/inland_buy_contracts/{id}/show |  | purchase.hop_dong_mua_ngoai.view | canView | detail ids=[896, 895, 894, 893, 892, 891] |
| erp.inland_buy_contract_annex.index | admin/orders/inland_buy_contract_annexs |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* | html |
| erp.inland_buy_contract_annex.page.forApprover | admin/orders/inland_buy_contract_annexs/forApprover |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* / middleware | html |
| erp.inland_buy_contract_annex.searchData.approve | admin/orders/inland_buy_contract_annexs/searchData | {"type": "approve"} | purchase.hop_dong_mua_ngoai.view | searchByFilter type=approve | datatables |
| erp.inland_buy_contract_annex.searchData.none | admin/orders/inland_buy_contract_annexs/searchData |  | purchase.hop_dong_mua_ngoai.view | searchByFilter type=None | datatables |
| erp.inland_buy_contract_annex.show | admin/orders/inland_buy_contract_annexs/{id}/show |  | purchase.hop_dong_mua_ngoai.view | canView | detail ids=[36, 35, 34, 33, 32, 31] |
| erp.inland_buy_contract_annex2.index | admin/orders/inland_buy_contract_annex2 |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* | html |
| erp.inland_buy_contract_annex2.page.forApprover | admin/orders/inland_buy_contract_annex2/forApprover |  | purchase.hop_dong_mua_ngoai.view | cờ blade is_* / middleware | html |
| erp.inland_buy_contract_annex2.searchData.approve | admin/orders/inland_buy_contract_annex2/searchData | {"type": "approve"} | purchase.hop_dong_mua_ngoai.view | searchByFilter type=approve | datatables |
| erp.inland_buy_contract_annex2.searchData.none | admin/orders/inland_buy_contract_annex2/searchData |  | purchase.hop_dong_mua_ngoai.view | searchByFilter type=None | datatables |
| erp.inland_buy_contract_annex2.show | admin/orders/inland_buy_contract_annex2/{id}/show |  | purchase.hop_dong_mua_ngoai.view | canView | detail ids=[2, 1] |
| erp.inland_buy_contract_new.index | admin/orders/inland_buy_contract_new |  | purchase.hop_dong_mua_hang_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_buy_contract_new.searchData.all | admin/orders/inland_buy_contract_new/searchData | {"_type": "all"} | purchase.hop_dong_mua_hang_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_buy_contract_new.searchData.for-approved | admin/orders/inland_buy_contract_new/searchData | {"_type": "for-approved"} | purchase.hop_dong_mua_hang_trong_nuoc.view | searchByFilter type=for-approved | datatables |
| erp.inland_buy_contract_new.searchData.none | admin/orders/inland_buy_contract_new/searchData |  | purchase.hop_dong_mua_hang_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_buy_contract_new.show | admin/orders/inland_buy_contract_new/{id}/show |  | purchase.hop_dong_mua_hang_trong_nuoc.view | canView | detail ids=[2400, 2399, 2398, 2397, 2396, 2395] |
| erp.inland_order_notification_new.index | admin/orders/inland_order_notification_new |  | purchase.luong_mua_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_order_notification_new.searchData.all | admin/orders/inland_order_notification_new/searchData | {"_type": "all"} | purchase.luong_mua_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_order_notification_new.searchData.none | admin/orders/inland_order_notification_new/searchData |  | purchase.luong_mua_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_order_notification_new.show | admin/orders/inland_order_notification_new/{id}/show |  | purchase.luong_mua_trong_nuoc.view | canView | detail ids=[5838, 5837, 5836, 5835, 5834, 5833] |
| erp.inland_order_request.index | admin/orders/inland_order_requests |  | purchase.yeu_cau_dat_hang_ngoai.view | cờ blade is_* | html |
| erp.inland_order_request.searchData.all | admin/orders/inland_order_requests/searchData | {"type": "all"} | purchase.yeu_cau_dat_hang_ngoai.view | searchByFilter type=all | datatables |
| erp.inland_order_request.searchData.approve | admin/orders/inland_order_requests/searchData | {"type": "approve"} | purchase.yeu_cau_dat_hang_ngoai.view | searchByFilter type=approve | datatables |
| erp.inland_order_request.searchData.department_approve | admin/orders/inland_order_requests/searchData | {"type": "department_approve"} | purchase.yeu_cau_dat_hang_ngoai.view | searchByFilter type=department_approve | datatables |
| erp.inland_order_request.searchData.none | admin/orders/inland_order_requests/searchData |  | purchase.yeu_cau_dat_hang_ngoai.view | searchByFilter type=None | datatables |
| erp.inland_order_request.show | admin/orders/inland_order_requests/{id}/show |  | purchase.yeu_cau_dat_hang_ngoai.view | canView | detail ids=[986, 985, 984, 983, 982, 981] |
| erp.inland_order_request_new.index | admin/orders/inland_order_request_new |  | purchase.phieu_yeu_cau_dat_hang_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_order_request_new.page.forDepartmentApprover | admin/orders/inland_order_request_new/forDepartmentApprover |  | purchase.phieu_yeu_cau_dat_hang_trong_nuoc.view | cờ blade is_* / middleware | html |
| erp.inland_order_request_new.searchData.all | admin/orders/inland_order_request_new/searchData | {"type": "all"} | purchase.phieu_yeu_cau_dat_hang_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_order_request_new.searchData.none | admin/orders/inland_order_request_new/searchData |  | purchase.phieu_yeu_cau_dat_hang_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_order_request_new.show | admin/orders/inland_order_request_new/{id}/show |  | purchase.phieu_yeu_cau_dat_hang_trong_nuoc.view | canView | detail ids=[5823, 5822, 5821, 5820, 5819, 5818] |
| erp.inland_order_summary_new.index | admin/orders/inland_order_summary_new |  | purchase.don_hoi_hang_po_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_order_summary_new.searchData.all | admin/orders/inland_order_summary_new/searchData | {"_type": "all"} | purchase.don_hoi_hang_po_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_order_summary_new.searchData.for-approve | admin/orders/inland_order_summary_new/searchData | {"_type": "for-approve"} | purchase.don_hoi_hang_po_trong_nuoc.view | searchByFilter type=for-approve | datatables |
| erp.inland_order_summary_new.searchData.none | admin/orders/inland_order_summary_new/searchData |  | purchase.don_hoi_hang_po_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_order_summary_new.show | admin/orders/inland_order_summary_new/{id}/show |  | purchase.don_hoi_hang_po_trong_nuoc.view | canView | detail ids=[4327, 4326, 4325, 4324, 4323, 4322] |
| erp.inland_purchase_invoice.index | admin/orders/inland_purchase_invoice |  | purchase.pi_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_purchase_invoice.page.forApprove | admin/orders/inland_purchase_invoice/forApprove |  | purchase.pi_trong_nuoc.view | cờ blade is_* / middleware | html |
| erp.inland_purchase_invoice.searchData.all | admin/orders/inland_purchase_invoice/searchData | {"_type": "all"} | purchase.pi_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_purchase_invoice.searchData.for-approve | admin/orders/inland_purchase_invoice/searchData | {"_type": "for-approve"} | purchase.pi_trong_nuoc.view | searchByFilter type=for-approve | datatables |
| erp.inland_purchase_invoice.searchData.xnk | admin/orders/inland_purchase_invoice/searchData | {"_type": "xnk"} | purchase.pi_trong_nuoc.view | searchByFilter type=xnk | datatables |
| erp.inland_purchase_invoice.searchData.none | admin/orders/inland_purchase_invoice/searchData |  | purchase.pi_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_purchase_invoice.show | admin/orders/inland_purchase_invoice/{id}/show |  | purchase.pi_trong_nuoc.view | canView | detail ids=[4101, 4100, 4099, 4098, 4097, 4096] |
| erp.order_notification2.index | admin/orders/order_notification2 |  | purchase.luong_mua_nhap_khau.view | cờ blade is_* | html |
| erp.order_notification2.searchData.all | admin/orders/order_notification2/searchData | {"type": "all"} | purchase.luong_mua_nhap_khau.view | searchByFilter type=all | datatables |
| erp.order_notification2.searchData.none | admin/orders/order_notification2/searchData |  | purchase.luong_mua_nhap_khau.view | searchByFilter type=None | datatables |
| erp.order_notification2.show | admin/orders/order_notification2/{id}/show |  | purchase.luong_mua_nhap_khau.view | canView | detail ids=[1711, 1710, 1709, 1708, 1707, 1706] |
| erp.order_request2.index | admin/orders/order_request2 |  | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | cờ blade is_* | html |
| erp.order_request2.page.all | admin/orders/order_request2/all |  | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | cờ blade is_* / middleware | html |
| erp.order_request2.page.forDepartmentApprover | admin/orders/order_request2/forDepartmentApprover |  | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | cờ blade is_* / middleware | html |
| erp.order_request2.searchData.all | admin/orders/order_request2/searchData | {"type": "all"} | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | searchByFilter type=all | datatables |
| erp.order_request2.searchData.none | admin/orders/order_request2/searchData |  | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | searchByFilter type=None | datatables |
| erp.order_request2.show | admin/orders/order_request2/{id}/show |  | purchase.phieu_yeu_cau_dat_hang_nhap_khau.view | canView | detail ids=[4071, 4070, 4069, 4068, 4067, 4066] |
| erp.order_summary2.index | admin/orders/order_summary2 |  | purchase.don_hoi_hang_po_nhap_khau.view | cờ blade is_* | html |
| erp.order_summary2.searchData.all | admin/orders/order_summary2/searchData | {"type": "all"} | purchase.don_hoi_hang_po_nhap_khau.view | searchByFilter type=all | datatables |
| erp.order_summary2.searchData.for-approve | admin/orders/order_summary2/searchData | {"type": "for-approve"} | purchase.don_hoi_hang_po_nhap_khau.view | searchByFilter type=for-approve | datatables |
| erp.order_summary2.searchData.none | admin/orders/order_summary2/searchData |  | purchase.don_hoi_hang_po_nhap_khau.view | searchByFilter type=None | datatables |
| erp.order_summary2.show | admin/orders/order_summary2/{id}/show |  | purchase.don_hoi_hang_po_nhap_khau.view | canView | detail ids=[1470, 1469, 1467, 1466, 1465, 1464] |
| erp.purchase_invoice.index | admin/orders/purchase_invoice |  | purchase.pi_nhap_khau.view | cờ blade is_* | html |
| erp.purchase_invoice.page.forApprove | admin/orders/purchase_invoice/forApprove |  | purchase.pi_nhap_khau.view | cờ blade is_* / middleware | html |
| erp.purchase_invoice.searchData.all | admin/orders/purchase_invoice/searchData | {"_type": "all"} | purchase.pi_nhap_khau.view | searchByFilter type=all | datatables |
| erp.purchase_invoice.searchData.for-approve | admin/orders/purchase_invoice/searchData | {"_type": "for-approve"} | purchase.pi_nhap_khau.view | searchByFilter type=for-approve | datatables |
| erp.purchase_invoice.searchData.xnk | admin/orders/purchase_invoice/searchData | {"_type": "xnk"} | purchase.pi_nhap_khau.view | searchByFilter type=xnk | datatables |
| erp.purchase_invoice.searchData.none | admin/orders/purchase_invoice/searchData |  | purchase.pi_nhap_khau.view | searchByFilter type=None | datatables |
| erp.purchase_invoice.show | admin/orders/purchase_invoice/{id}/show |  | purchase.pi_nhap_khau.view | canView | detail ids=[1349, 1348, 1347, 1346, 1345, 1344] |
| erp.root_order_request.index | admin/orders/root_order_request |  | purchase.phieu_yeu_cau_dat_hang.view | cờ blade is_* | html |
| erp.root_order_request.page.forApprover | admin/orders/root_order_request/forApprover |  | purchase.phieu_yeu_cau_dat_hang.view | cờ blade is_* / middleware | html |
| erp.root_order_request.searchData.all | admin/orders/root_order_request/searchData | {"_type": "all"} | purchase.phieu_yeu_cau_dat_hang.view | searchByFilter type=all | datatables |
| erp.root_order_request.searchData.for-approved | admin/orders/root_order_request/searchData | {"_type": "for-approved"} | purchase.phieu_yeu_cau_dat_hang.view | searchByFilter type=for-approved | datatables |
| erp.root_order_request.searchData.none | admin/orders/root_order_request/searchData |  | purchase.phieu_yeu_cau_dat_hang.view | searchByFilter type=None | datatables |
| erp.root_order_request.show | admin/orders/root_order_request/{id}/show |  | purchase.phieu_yeu_cau_dat_hang.view | canView | detail ids=[8595, 8594, 8593, 8592, 8591, 8590] |
| erp.buy_service_contract.index | admin/orders/buy-service-contract |  | purchase.hop_dong_mua_dich_vu.view | cờ blade is_* | html |
| erp.buy_service_contract.searchData.all | admin/orders/buy-service-contract/searchData | {"type": "all"} | purchase.hop_dong_mua_dich_vu.view | searchByFilter type=all | datatables |
| erp.buy_service_contract.searchData.for-approve | admin/orders/buy-service-contract/searchData | {"type": "for-approve"} | purchase.hop_dong_mua_dich_vu.view | searchByFilter type=for-approve | datatables |
| erp.buy_service_contract.searchData.index | admin/orders/buy-service-contract/searchData | {"type": "index"} | purchase.hop_dong_mua_dich_vu.view | searchByFilter type=index | datatables |
| erp.buy_service_contract.show | admin/orders/buy-service-contract/{id}/show |  | purchase.hop_dong_mua_dich_vu.view | canView | detail ids=[90, 89, 88, 87, 86, 85] |
| erp.shipping_quote.index | admin/delivery_international_requests |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* | html |
| erp.shipping_quote.searchData.none | admin/delivery_international_requests/searchData |  | purchase.van_chuyen_quoc_te.view | searchByFilter type=None | datatables |
| erp.shipping_quote.show | admin/delivery_international_requests/{id}/show |  | purchase.van_chuyen_quoc_te.view | canView | detail ids=[431, 430, 429, 428, 427, 426] |
| erp.summary_order_shipping_price.index | admin/delivery_international_order |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* | html |
| erp.summary_order_shipping_price.page.forApprove | admin/delivery_international_order/forApprove |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* / middleware | html |
| erp.summary_order_shipping_price.searchData.approve | admin/delivery_international_order/searchData | {"type": "approve"} | purchase.van_chuyen_quoc_te.view | searchByFilter type=approve | datatables |
| erp.summary_order_shipping_price.searchData.none | admin/delivery_international_order/searchData |  | purchase.van_chuyen_quoc_te.view | searchByFilter type=None | datatables |
| erp.summary_shipping_price.index | admin/delivery_international_general |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* | html |
| erp.summary_shipping_price.page.forApprove | admin/delivery_international_general/forApprove |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* / middleware | html |
| erp.summary_shipping_price.page.forDepartmentApprove | admin/delivery_international_general/forDepartmentApprove |  | purchase.van_chuyen_quoc_te.view | cờ blade is_* / middleware | html |
| erp.summary_shipping_price.searchData.approve | admin/delivery_international_general/searchData | {"type": "approve"} | purchase.van_chuyen_quoc_te.view | searchByFilter type=approve | datatables |
| erp.summary_shipping_price.searchData.department_approve | admin/delivery_international_general/searchData | {"type": "department_approve"} | purchase.van_chuyen_quoc_te.view | searchByFilter type=department_approve | datatables |
| erp.summary_shipping_price.searchData.employee | admin/delivery_international_general/searchData | {"type": "employee"} | purchase.van_chuyen_quoc_te.view | searchByFilter type=employee | datatables |
| erp.summary_shipping_price.searchData.none | admin/delivery_international_general/searchData |  | purchase.van_chuyen_quoc_te.view | searchByFilter type=None | datatables |
| erp.summary_shipping_price.show | admin/delivery_international_general/{id}/show |  | purchase.van_chuyen_quoc_te.view | canView | detail ids=[427, 426, 425, 424, 423, 422] |
| erp.custom_declaration.index | admin/orders/custom_declarations |  | purchase.to_khai_hai_quan.view | cờ blade is_* | html |
| erp.custom_declaration.searchData.all | admin/orders/custom_declarations/searchData | {"type": "all"} | purchase.to_khai_hai_quan.view | searchByFilter type=all | datatables |
| erp.custom_declaration.searchData.approve | admin/orders/custom_declarations/searchData | {"type": "approve"} | purchase.to_khai_hai_quan.view | searchByFilter type=approve | datatables |
| erp.custom_declaration.searchData.none | admin/orders/custom_declarations/searchData |  | purchase.to_khai_hai_quan.view | searchByFilter type=None | datatables |
| erp.custom_declaration.show | admin/orders/custom_declarations/{id}/show |  | purchase.to_khai_hai_quan.view | canView | detail ids=[840, 839, 838, 837, 836, 835] |
| erp.order_import_request.index | admin/orders/order_import_requests |  | purchase.tong_hop_chi_phi_nhap_khau.view | cờ blade is_* | html |
| erp.order_import_request.searchData.all | admin/orders/order_import_requests/searchData | {"type": "all"} | purchase.tong_hop_chi_phi_nhap_khau.view | searchByFilter type=all | datatables |
| erp.order_import_request.searchData.none | admin/orders/order_import_requests/searchData |  | purchase.tong_hop_chi_phi_nhap_khau.view | searchByFilter type=None | datatables |
| erp.order_import_request.show | admin/orders/order_import_requests/{id}/show |  | purchase.tong_hop_chi_phi_nhap_khau.view | canView | detail ids=[775, 774, 773, 772, 771, 770] |
| erp.inland_product_arrived_new.index | admin/orders/inland_product_arrived_news |  | purchase.phieu_bao_hang_ve_mua_trong_nuoc.view | cờ blade is_* | html |
| erp.inland_product_arrived_new.searchData.all | admin/orders/inland_product_arrived_news/searchData | {"_type": "all"} | purchase.phieu_bao_hang_ve_mua_trong_nuoc.view | searchByFilter type=all | datatables |
| erp.inland_product_arrived_new.searchData.none | admin/orders/inland_product_arrived_news/searchData |  | purchase.phieu_bao_hang_ve_mua_trong_nuoc.view | searchByFilter type=None | datatables |
| erp.inland_product_arrived_new.show | admin/orders/inland_product_arrived_news/{id}/show |  | purchase.phieu_bao_hang_ve_mua_trong_nuoc.view | canView | detail ids=[2938, 2937, 2936, 2935, 2934, 2933] |
| erp.rule_inland_buy_contract.index | admin/orders/rule_inland_buy_contracts |  | purchase.hop_dong_nguyen_tac_mua_hang.view | cờ blade is_* | html |
| erp.rule_inland_buy_contract.page.forApprover | admin/orders/rule_inland_buy_contracts/forApprover |  | purchase.hop_dong_nguyen_tac_mua_hang.view | cờ blade is_* / middleware | html |
| erp.rule_inland_buy_contract.searchData.all | admin/orders/rule_inland_buy_contracts/searchData | {"type": "all"} | purchase.hop_dong_nguyen_tac_mua_hang.view | searchByFilter type=all | datatables |
| erp.rule_inland_buy_contract.searchData.approve | admin/orders/rule_inland_buy_contracts/searchData | {"type": "approve"} | purchase.hop_dong_nguyen_tac_mua_hang.view | searchByFilter type=approve | datatables |
| erp.rule_inland_buy_contract.searchData.use | admin/orders/rule_inland_buy_contracts/searchData | {"type": "use"} | purchase.hop_dong_nguyen_tac_mua_hang.view | searchByFilter type=use | datatables |
| erp.rule_inland_buy_contract.searchData.none | admin/orders/rule_inland_buy_contracts/searchData |  | purchase.hop_dong_nguyen_tac_mua_hang.view | searchByFilter type=None | datatables |
| erp.rule_inland_buy_contract.show | admin/orders/rule_inland_buy_contracts/{id}/show |  | purchase.hop_dong_nguyen_tac_mua_hang.view | canView | detail ids=[50, 49, 48, 47, 46, 45] |
| erp.report.assign_employee_brands.page | admin/assign/report/assign_employee_brands |  | purchase.bao_cao_thuong_hieu_hang_san_xuat_theo_nhan_vien_phong_ban_phu_trach.view | cờ trang báo cáo | html |
| erp.report.assign_employee_brands.search | admin/assign/report/assign_employee_brands_search_data | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_thuong_hieu_hang_san_xuat_theo_nhan_vien_phong_ban_phu_trach.view | dữ liệu báo cáo | auto |
| erp.report.assign_department_brands.page | admin/assign/report/assign_department_brands |  | purchase.bao_cao_danh_sach_thuong_hieu_hang_san_xuat.view | cờ trang báo cáo | html |
| erp.report.assign_department_brands.search | admin/assign/report/assign_department_brands_search_data | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_danh_sach_thuong_hieu_hang_san_xuat.view | dữ liệu báo cáo | auto |
| erp.report.summary_return_warranty.page | admin/orders/firm_warranty_confirms/summaryReturnWarranty |  | purchase.tinh_trang_tra_hang_bao_hanh.view | cờ trang báo cáo | html |
| erp.report.summary_return_warranty.search | admin/orders/firm_warranty_confirms/summaryReturnWarrantySearchData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.tinh_trang_tra_hang_bao_hanh.view | dữ liệu báo cáo | auto |
| erp.report.report_for_buyer.page | admin/orders/inland_order_requests/reportForBuyer |  | purchase.bao_cao_duyet_gia_hang_mua_ngoai.view | cờ trang báo cáo | html |
| erp.report.report_for_buyer.search | admin/orders/inland_order_requests/reportForBuyerSearchData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_duyet_gia_hang_mua_ngoai.view | dữ liệu báo cáo | auto |
| erp.report.report_for_buyer_request.page | admin/orders/inland_order_requests/reportForBuyerRequest |  | purchase.bao_cao_duyet_gia_hang_mua_ngoai.view | cờ trang báo cáo | html |
| erp.report.report_for_buyer_request.search | admin/orders/inland_order_requests/reportForBuyerRequestSearchData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_duyet_gia_hang_mua_ngoai.view | dữ liệu báo cáo | auto |
| erp.report.warning_product_delivery.page | admin/orders/reports/warning_product_delivery |  | purchase.canh_bao_hang_can_giao.view | cờ trang báo cáo | html |
| erp.report.warning_product_delivery.search | admin/orders/reports/warningProductDeliverySearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.canh_bao_hang_can_giao.view | dữ liệu báo cáo | auto |
| erp.report.import_product_sale.page | admin/orders/reports/importProductSale |  | purchase.bao_cao_doanh_so_nhap_mua_hang.view | cờ trang báo cáo | html |
| erp.report.import_product_sale.search | admin/orders/reports/importProductSaleSearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_doanh_so_nhap_mua_hang.view | dữ liệu báo cáo | auto |
| erp.report.order_product_sale.page | admin/orders/reports/orderProductSale |  | purchase.bao_cao_doanh_so_dat_hang_nha_cung_cap.view | cờ trang báo cáo | html |
| erp.report.order_product_sale.search | admin/orders/reports/orderProductSaleSearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_doanh_so_dat_hang_nha_cung_cap.view | dữ liệu báo cáo | auto |
| erp.report.change_import_price.page | admin/orders/reports/changeImportPrice |  | purchase.bao_cao_bien_dong_gia_nhap_mua.view | cờ trang báo cáo | html |
| erp.report.change_import_price.search | admin/orders/reports/changeImportPriceSearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_bien_dong_gia_nhap_mua.view | dữ liệu báo cáo | auto |
| erp.report.cost_import.page | admin/orders/reports/costImport |  | purchase.bao_cao_chi_phi_nhap_hang_theo_hop_dong.view | cờ trang báo cáo | html |
| erp.report.cost_import.search | admin/orders/reports/costImportSearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_chi_phi_nhap_hang_theo_hop_dong.view | dữ liệu báo cáo | auto |
| erp.report.product_confirm_warranty.page | admin/orders/reports/productConfirmWarranty |  | purchase.bao_cao_hang_hoa_da_xac_nhan_bao_hanh.view | cờ trang báo cáo | html |
| erp.report.product_confirm_warranty.search | admin/orders/reports/productConfirmWarrantySearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_hang_hoa_da_xac_nhan_bao_hanh.view | dữ liệu báo cáo | auto |
| erp.report.fast_delivery.page | admin/orders/reports/fastDelivery |  | purchase.chi_phi_van_chuyen_nhanh.view | cờ trang báo cáo | html |
| erp.report.fast_delivery.search | admin/orders/reports/fastDeliverySearch | {"current_page": 1, "per_page": 50, "page": 1} | purchase.chi_phi_van_chuyen_nhanh.view | dữ liệu báo cáo | auto |
| erp.report.product_by_manufacture.page | admin/orders/reports/productByManufacture |  | purchase.bao_cao_danh_sach_hang_hoa_theo_hang_san_xuat.view | cờ trang báo cáo | html |
| erp.report.product_by_manufacture.search | admin/orders/reports/productByManufactureSearchData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_danh_sach_hang_hoa_theo_hang_san_xuat.view | dữ liệu báo cáo | auto |
| erp.report.order_report_process.page | admin/orders/reports/orderReportProcess |  | purchase.bao_cao_qua_trinh_dat_hang_theo_nhan_vien.view | cờ trang báo cáo | html |
| erp.report.stock_transfer.page | admin/stock-transfer/report |  | purchase.bao_cao_luan_chuyen_hang_hoa.view | cờ trang báo cáo | html |
| erp.report.stock_transfer.search | admin/stock-transfer/report/searchData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_luan_chuyen_hang_hoa.view | dữ liệu báo cáo | auto |
| erp.report.warehouse_warning.page | admin/warehouse-warning/report |  | purchase.canh_bao_dat_hang_ton_kho.view | cờ trang báo cáo | html |
| erp.report.supplier_debt.page | admin/sale/reports/supplier-debt-details |  | purchase.bao_cao_chi_tiet_cong_no_nha_cung_cap_trong_nuoc.view | cờ trang báo cáo | html |
| erp.report.supplier_debt.search | admin/sale/reports/supplier-debt-detailsData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_chi_tiet_cong_no_nha_cung_cap_trong_nuoc.view | dữ liệu báo cáo | auto |
| erp.report.supplier_debt_nation.page | admin/sale/reports/supplier-debt-nation-details |  | purchase.bao_cao_chi_tiet_cong_no_nha_cung_cap_nuoc_ngoai.view | cờ trang báo cáo | html |
| erp.report.supplier_debt_nation.search | admin/sale/reports/supplier-debt-nation-detailsData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bao_cao_chi_tiet_cong_no_nha_cung_cap_nuoc_ngoai.view | dữ liệu báo cáo | auto |
| erp.report.compare_supplier_debt.page | admin/sale/reports/compare-supplier-debt-details |  | purchase.bang_doi_chieu_cong_no_1_nha_cung_cap_trong_nuoc.view | cờ trang báo cáo | html |
| erp.report.compare_supplier_debt.search | admin/sale/reports/compare-supplier-debt-detailsData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bang_doi_chieu_cong_no_1_nha_cung_cap_trong_nuoc.view | dữ liệu báo cáo | auto |
| erp.report.compare_supplier_debt_nation.page | admin/sale/reports/compare-supplier-debt-nation-details |  | purchase.bang_doi_chieu_cong_no_1_nha_cung_cap_nuoc_ngoai.view | cờ trang báo cáo | html |
| erp.report.compare_supplier_debt_nation.search | admin/sale/reports/compare-supplier-debt-nation-detailsData | {"current_page": 1, "per_page": 50, "page": 1} | purchase.bang_doi_chieu_cong_no_1_nha_cung_cap_nuoc_ngoai.view | dữ liệu báo cáo | auto |
| erp.mw.orders/buy_contract_annexs | admin/orders/buy_contract_annexs |  | Mua hàng | middleware | html |
| erp.mw.orders/buy_contract_annexs/forApprover | admin/orders/buy_contract_annexs/forApprover |  | Duyệt hợp đồng đặt hàng | middleware | html |
| erp.mw.orders/buy_contracts | admin/orders/buy_contracts |  | Mua hàng | middleware | html |
| erp.mw.orders/buy_contracts/forApprover | admin/orders/buy_contracts/forApprover |  | Duyệt hợp đồng đặt hàng | middleware | html |
| erp.mw.orders/buy_requests | admin/orders/buy_requests |  | Mua hàng | middleware | html |
| erp.mw.orders/buy_requests/forApprover | admin/orders/buy_requests/forApprover |  | Duyệt đề xuất đặt hàng | middleware | html |
| erp.mw.orders/inland_buy_contract2 | admin/orders/inland_buy_contract2 |  | Mua hàng | middleware | html |
| erp.mw.orders/inland_buy_contract2/forApprover | admin/orders/inland_buy_contract2/forApprover |  | Duyệt hợp đồng đặt hàng | middleware | html |
| erp.mw.orders/inland_order_notification2/forCreator | admin/orders/inland_order_notification2/forCreator |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/inland_order_notification_new/forCreator | admin/orders/inland_order_notification_new/forCreator |  | Tổng hợp đặt hàng trong nước | middleware | html |
| erp.mw.orders/inland_order_request2/forApprover | admin/orders/inland_order_request2/forApprover |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/inland_order_request2/forDepartmentApprover | admin/orders/inland_order_request2/forDepartmentApprover |  | Duyệt yêu cầu đặt hàng | middleware | html |
| erp.mw.orders/inland_order_request_new/forApprover | admin/orders/inland_order_request_new/forApprover |  | Tổng hợp đặt hàng trong nước | middleware | html |
| erp.mw.orders/inland_order_summary2 | admin/orders/inland_order_summary2 |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/inland_order_summary2/forApprover | admin/orders/inland_order_summary2/forApprover |  | Mua hàng | middleware | html |
| erp.mw.orders/inland_order_summary2/forFirstApprover | admin/orders/inland_order_summary2/forFirstApprover |  | Duyệt đơn hàng theo hãng | middleware | html |
| erp.mw.orders/order_notification2/forCreator | admin/orders/order_notification2/forCreator |  | Tổng hợp đặt hàng nhập khẩu | middleware | html |
| erp.mw.orders/order_notifications/forCreator | admin/orders/order_notifications/forCreator |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/order_request2/forApprover | admin/orders/order_request2/forApprover |  | Tổng hợp đặt hàng nhập khẩu | middleware | html |
| erp.mw.orders/order_requests/forApprover | admin/orders/order_requests/forApprover |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/order_requests/forDepartmentApprover | admin/orders/order_requests/forDepartmentApprover |  | Duyệt yêu cầu đặt hàng | middleware | html |
| erp.mw.orders/order_summaries | admin/orders/order_summaries |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/order_summaries/forApprover | admin/orders/order_summaries/forApprover |  | Mua hàng | middleware | html |
| erp.mw.orders/order_summaries/forFirstApprover | admin/orders/order_summaries/forFirstApprover |  | Duyệt đơn hàng theo hãng | middleware | html |
| erp.mw.orders/summary_annexs | admin/orders/summary_annexs |  | Tổng hợp đặt hàng | middleware | html |
| erp.mw.orders/summary_annexs/forApprover | admin/orders/summary_annexs/forApprover |  | Mua hàng | middleware | html |
| erp.home.approveList | admin/approveList |  | purchase.*.approve (đếm việc chờ) | đếm việc chờ | lists |
| erp.report.order_product.page | admin/orders/reports/order_product |  | tên lạ (không alias) ⇒ false | cờ trang báo cáo | html |
| erp.report.order_product.search | admin/orders/reports/orderProductSearch | {"current_page": 1, "per_page": 50, "page": 1} | tên lạ (không alias) ⇒ false | dữ liệu báo cáo | auto |
| erp.report.order_supplier.page | admin/orders/reports/order_supplier |  | tên lạ (không alias) ⇒ false | cờ trang báo cáo | html |
| erp.report.order_supplier.search | admin/orders/reports/orderSupplierSearch | {"current_page": 1, "per_page": 50, "page": 1} | tên lạ (không alias) ⇒ false | dữ liệu báo cáo | auto |
