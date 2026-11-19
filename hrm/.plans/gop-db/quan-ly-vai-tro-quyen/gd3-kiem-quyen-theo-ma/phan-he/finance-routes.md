# finance — đường đọc chụp mốc (GĐ3 Task 8.14)

Sinh từ `finance-routes.json` (máy đọc). Chụp bằng `hrm-api/tests/Support/ScopeSnapshot.php` (tokens | run | diff), chạy 3 tiến trình song song theo nhóm tài khoản (ghép `ket_qua`). ERP chạy tạm `php -S 127.0.0.1:8012` (DB rehearsal + DB_*_HRM), hrm-api 8011.
Tham số loại danh sách: dò từng model ERP — `_type` nếu model so `$request->_type == "<loại>"`, ngược lại `type`.

## Tài khoản (rehearsal, chỉ SELECT)

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — finance: 39 dòng mức 4, 1 mức 3, cty 1 |
| pv3 | 207 | hantt.kthn — 21 mức 3, 1 mức 4, cty 1 |
| pv2 | 604 | minhnt.ptkd — 19 mức 2, 2 mức 3, cty 1 |
| pv1 | 110 | honglv.pt — 10 mức 1, 2 mức 2, 1 mức 3, cty 1 |
| tron | 196 | hantn.kthn (kế toán) — 34 mức 4, 23 mức 3, 7 mức 2, cty 1 |
| cty4 | 661 | hieunv.tlgd — chỉ 4 mã finance không phạm vi, cty 4 |
| khong_ma | 145 | nguyetdtm.nshn — 0 mã finance.*, cty 1 |

Ca thiếu (chỉ PHPUnit golden): có mã không phạm vi (null), mã ở công ty khác qua Vai trò (c2), từng mã riêng lẻ ở từng mức.

## Route (270 = ERP 187 + hrm-api 83) × 7 tài khoản = 1890 ô

| id | url | tham số | mã | cột lọc / cách đọc | extract |
|---|---|---|---|---|---|
| erp.declare_debt_supplier_beginning.index | admin/accounting/declare-debt-supplier-beginning | {"type": "all"} | finance.cong_no_dau_ky.view | cờ blade is_* | html |
| erp.declare_debt_supplier_beginning.searchData.none | admin/accounting/declare-debt-supplier-beginning/searchData |  | finance.cong_no_dau_ky.view | searchByFilter type=None | datatables |
| erp.declare_debt_supplier_beginning.show | admin/accounting/declare-debt-supplier-beginning/{id}/show |  | finance.cong_no_dau_ky.view | canView | detail ids=[1561, 1560, 1559, 1558, 1557, 1556] |
| erp.declare_debt_beginning.index | admin/accounting/declare-debt-beginning | {"type": "all"} | finance.cong_no_dau_ky.view | cờ blade is_* | html |
| erp.declare_debt_beginning.searchData.none | admin/accounting/declare-debt-beginning/searchData |  | finance.cong_no_dau_ky.view | searchByFilter type=None | datatables |
| erp.warranty_payment.index | admin/customer-care/warranty_payments | {"type": "all"} | finance.phieu_chi.view | cờ blade is_* | html |
| erp.warranty_payment.searchData.all | admin/customer-care/warranty_payments/searchData | {"_type": "all"} | finance.phieu_chi.view | searchByFilter type=all | datatables |
| erp.warranty_payment.searchData.for-approved | admin/customer-care/warranty_payments/searchData | {"_type": "for-approved"} | finance.phieu_chi.view | searchByFilter type=for-approved | datatables |
| erp.warranty_payment.searchData.approved | admin/customer-care/warranty_payments/searchData | {"_type": "approved"} | finance.phieu_chi.view | searchByFilter type=approved | datatables |
| erp.warranty_payment.searchData.index | admin/customer-care/warranty_payments/searchData | {"_type": "index"} | finance.phieu_chi.view | searchByFilter type=index | datatables |
| erp.addition_accounting_request.index | admin/income-expenditure/addition_accounting_requests | {"type": "all"} | finance.phieu_yeu_cau_hach_toan_bo_sung.view | cờ blade is_* | html |
| erp.addition_accounting_request.searchData.all | admin/income-expenditure/addition_accounting_requests/searchData | {"type": "all"} | finance.phieu_yeu_cau_hach_toan_bo_sung.view | searchByFilter type=all | datatables |
| erp.addition_accounting_request.searchData.for-approved | admin/income-expenditure/addition_accounting_requests/searchData | {"type": "for-approved"} | finance.phieu_yeu_cau_hach_toan_bo_sung.view | searchByFilter type=for-approved | datatables |
| erp.addition_accounting_request.searchData.index | admin/income-expenditure/addition_accounting_requests/searchData | {"type": "index"} | finance.phieu_yeu_cau_hach_toan_bo_sung.view | searchByFilter type=index | datatables |
| erp.addition_accounting_request.show | admin/income-expenditure/addition_accounting_requests/{id}/show |  | finance.phieu_yeu_cau_hach_toan_bo_sung.view | canView | detail ids=[2292, 2291, 2290, 2289, 2288, 2287] |
| erp.bill_adjust_dept.index | admin/income-expenditure/bill_adjust_dept | {"type": "all"} | finance.phieu_ke_toan.view | cờ blade is_* | html |
| erp.bill_adjust_dept.searchData.all | admin/income-expenditure/bill_adjust_dept/searchData | {"_type": "all"} | finance.phieu_ke_toan.view | searchByFilter type=all | datatables |
| erp.bill_adjust_dept.searchData.index | admin/income-expenditure/bill_adjust_dept/searchData | {"_type": "index"} | finance.phieu_ke_toan.view | searchByFilter type=index | datatables |
| erp.bill_adjust_dept.show | admin/income-expenditure/bill_adjust_dept/{id}/show |  | finance.phieu_ke_toan.view | canView | detail ids=[15681, 15680, 15679, 15678, 15677, 15676] |
| erp.bill_adjust_dept_request.index | admin/income-expenditure/bill_adjust_dept_requests | {"type": "all"} | finance.phieu_yeu_cau_dieu_chinh.view | cờ blade is_* | html |
| erp.bill_adjust_dept_request.page.for-accounting | admin/income-expenditure/bill_adjust_dept_requests/for-accounting |  | finance.phieu_yeu_cau_dieu_chinh.view | cờ blade is_* | html |
| erp.bill_adjust_dept_request.searchData.all | admin/income-expenditure/bill_adjust_dept_requests/searchData | {"_type": "all"} | finance.phieu_yeu_cau_dieu_chinh.view | searchByFilter type=all | datatables |
| erp.bill_adjust_dept_request.searchData.for-accounting | admin/income-expenditure/bill_adjust_dept_requests/searchData | {"_type": "for-accounting"} | finance.phieu_yeu_cau_dieu_chinh.view | searchByFilter type=for-accounting | datatables |
| erp.bill_adjust_dept_request.searchData.index | admin/income-expenditure/bill_adjust_dept_requests/searchData | {"_type": "index"} | finance.phieu_yeu_cau_dieu_chinh.view | searchByFilter type=index | datatables |
| erp.bill_adjust_dept_request.show | admin/income-expenditure/bill_adjust_dept_requests/{id}/show |  | finance.phieu_yeu_cau_dieu_chinh.view | canView | detail ids=[12658, 12657, 12656, 12655, 12654, 12653] |
| erp.bill_income.index | admin/income-expenditure/bill_incomes | {"type": "all"} | finance.phieu_thu.view | cờ blade is_* | html |
| erp.bill_income.searchData.all | admin/income-expenditure/bill_incomes/searchData | {"_type": "all"} | finance.phieu_thu.view | searchByFilter type=all | datatables |
| erp.bill_income.searchData.for-approved | admin/income-expenditure/bill_incomes/searchData | {"type": "for-approved"} | finance.phieu_thu.view | searchByFilter type=for-approved | datatables |
| erp.bill_income.searchData.approved | admin/income-expenditure/bill_incomes/searchData | {"type": "approved"} | finance.phieu_thu.view | searchByFilter type=approved | datatables |
| erp.bill_income.searchData.index | admin/income-expenditure/bill_incomes/searchData | {"_type": "index"} | finance.phieu_thu.view | searchByFilter type=index | datatables |
| erp.bill_income.show | admin/income-expenditure/bill_incomes/{id}/show |  | finance.phieu_thu.view | canView | detail ids=[2839, 2838, 2837, 2836, 2835, 2834] |
| erp.bill_income_report.index | admin/income-expenditure/bill_income_report | {"type": "all"} | finance.phieu_bao_co.view | cờ blade is_* | html |
| erp.bill_income_report.page.for-accounting | admin/income-expenditure/bill_income_report/for-accounting |  | finance.phieu_bao_co.view | cờ blade is_* | html |
| erp.bill_income_report.searchData.all | admin/income-expenditure/bill_income_report/searchData | {"_type": "all"} | finance.phieu_bao_co.view | searchByFilter type=all | datatables |
| erp.bill_income_report.searchData.approved | admin/income-expenditure/bill_income_report/searchData | {"_type": "approved"} | finance.phieu_bao_co.view | searchByFilter type=approved | datatables |
| erp.bill_income_report.searchData.index | admin/income-expenditure/bill_income_report/searchData | {"_type": "index"} | finance.phieu_bao_co.view | searchByFilter type=index | datatables |
| erp.bill_income_report.show | admin/income-expenditure/bill_income_report/{id}/show |  | finance.phieu_bao_co.view | canView | detail ids=[4805, 4804, 4803, 4802, 4801, 4800] |
| erp.bill_income_request.index | admin/income-expenditure/bill_income_requests | {"type": "all"} | finance.phieu_de_nghi_thu.view | cờ blade is_* | html |
| erp.bill_income_request.page.for-accounting | admin/income-expenditure/bill_income_requests/for-accounting |  | finance.phieu_de_nghi_thu.view | cờ blade is_* | html |
| erp.bill_income_request.searchData.all | admin/income-expenditure/bill_income_requests/searchData | {"_type": "all"} | finance.phieu_de_nghi_thu.view | searchByFilter type=all | datatables |
| erp.bill_income_request.searchData.for-accounting | admin/income-expenditure/bill_income_requests/searchData | {"_type": "for-accounting"} | finance.phieu_de_nghi_thu.view | searchByFilter type=for-accounting | datatables |
| erp.bill_income_request.searchData.approved | admin/income-expenditure/bill_income_requests/searchData | {"_type": "approved"} | finance.phieu_de_nghi_thu.view | searchByFilter type=approved | datatables |
| erp.bill_income_request.searchData.index | admin/income-expenditure/bill_income_requests/searchData | {"_type": "index"} | finance.phieu_de_nghi_thu.view | searchByFilter type=index | datatables |
| erp.bill_income_request.show | admin/income-expenditure/bill_income_requests/{id}/show |  | finance.phieu_de_nghi_thu.view | canView | detail ids=[2939, 2938, 2937, 2936, 2935, 2934] |
| erp.bill_payment.index | admin/income-expenditure/bill_payments | {"type": "all"} | finance.phieu_chi.view | cờ blade is_* | html |
| erp.bill_payment.searchData.all | admin/income-expenditure/bill_payments/searchData | {"_type": "all"} | finance.phieu_chi.view | searchByFilter type=all | datatables |
| erp.bill_payment.searchData.for-approved | admin/income-expenditure/bill_payments/searchData | {"_type": "for-approved"} | finance.phieu_chi.view | searchByFilter type=for-approved | datatables |
| erp.bill_payment.searchData.approved | admin/income-expenditure/bill_payments/searchData | {"_type": "approved"} | finance.phieu_chi.view | searchByFilter type=approved | datatables |
| erp.bill_payment.searchData.index | admin/income-expenditure/bill_payments/searchData | {"_type": "index"} | finance.phieu_chi.view | searchByFilter type=index | datatables |
| erp.bill_payment.show | admin/income-expenditure/bill_payments/{id}/show |  | finance.phieu_chi.view | canView | detail ids=[1633, 1632, 1631, 1630, 1629, 1628] |
| erp.bill_payment_authorization.index | admin/income-expenditure/bill_payment_authorizations | {"type": "all"} | finance.phieu_uy_nhiem_chi.view | cờ blade is_* | html |
| erp.bill_payment_authorization.searchData.all | admin/income-expenditure/bill_payment_authorizations/searchData | {"_type": "all"} | finance.phieu_uy_nhiem_chi.view | searchByFilter type=all | datatables |
| erp.bill_payment_authorization.searchData.approved | admin/income-expenditure/bill_payment_authorizations/searchData | {"_type": "approved"} | finance.phieu_uy_nhiem_chi.view | searchByFilter type=approved | datatables |
| erp.bill_payment_authorization.searchData.index | admin/income-expenditure/bill_payment_authorizations/searchData | {"_type": "index"} | finance.phieu_uy_nhiem_chi.view | searchByFilter type=index | datatables |
| erp.bill_payment_authorization.show | admin/income-expenditure/bill_payment_authorizations/{id}/show |  | finance.phieu_uy_nhiem_chi.view | canView | detail ids=[3279, 3278, 3277, 3276, 3275, 3274] |
| erp.bill_payment_request.index | admin/income-expenditure/bill_payment_requests | {"type": "all"} | finance.phieu_de_nghi_thanh_toan.view | cờ blade is_* | html |
| erp.bill_payment_request.searchData.all | admin/income-expenditure/bill_payment_requests/searchData | {"_type": "all"} | finance.phieu_de_nghi_thanh_toan.view | searchByFilter type=all | datatables |
| erp.bill_payment_request.searchData.for-approved | admin/income-expenditure/bill_payment_requests/searchData | {"_type": "for-approved"} | finance.phieu_de_nghi_thanh_toan.view | searchByFilter type=for-approved | datatables |
| erp.bill_payment_request.searchData.approved | admin/income-expenditure/bill_payment_requests/searchData | {"_type": "approved"} | finance.phieu_de_nghi_thanh_toan.view | searchByFilter type=approved | datatables |
| erp.bill_payment_request.searchData.index | admin/income-expenditure/bill_payment_requests/searchData | {"_type": "index"} | finance.phieu_de_nghi_thanh_toan.view | searchByFilter type=index | datatables |
| erp.bill_payment_request.show | admin/income-expenditure/bill_payment_requests/{id}/show |  | finance.phieu_de_nghi_thanh_toan.view | canView | detail ids=[5267, 5266, 5265, 5264, 5263, 5262] |
| erp.price_asking_request.index | admin/orders/price_asking_requests | {"type": "all"} | finance.yeu_cau_hoi_gia.approve | cờ blade is_* | html |
| erp.price_asking_request.searchData.approve | admin/orders/price_asking_requests/searchData | {"type": "approve"} | finance.yeu_cau_hoi_gia.approve | searchByFilter type=approve | datatables |
| erp.price_asking_request.searchData.none | admin/orders/price_asking_requests/searchData |  | finance.yeu_cau_hoi_gia.approve | searchByFilter type=None | datatables |
| erp.price_asking_request.show | admin/orders/price_asking_requests/{id}/show |  | finance.yeu_cau_hoi_gia.approve | canView | detail ids=[4698, 4697, 4696, 4695, 4694, 4693] |
| erp.borrow_export_request.index | admin/warehouse/borrow_export_requests | {"type": "all"} | finance.phieu_hang_muon.view | cờ blade is_* | html |
| erp.borrow_export_request.page.forAccounting | admin/warehouse/borrow_export_requests/forAccounting |  | finance.phieu_hang_muon.view | cờ blade is_* | html |
| erp.borrow_export_request.searchData.all | admin/warehouse/borrow_export_requests/searchData | {"type": "all"} | finance.phieu_hang_muon.view | searchByFilter type=all | datatables |
| erp.borrow_export_request.searchData.for-approve | admin/warehouse/borrow_export_requests/searchData | {"type": "for-approve"} | finance.phieu_hang_muon.view | searchByFilter type=for-approve | datatables |
| erp.borrow_export_request.searchData.accounting | admin/warehouse/borrow_export_requests/searchData | {"type": "accounting"} | finance.phieu_hang_muon.view | searchByFilter type=accounting | datatables |
| erp.borrow_export_request.show | admin/warehouse/borrow_export_requests/{id}/show |  | finance.phieu_hang_muon.view | canView | detail ids=[367, 366, 365, 364, 363, 362] |
| erp.borrow_extend_request.index | admin/warehouse/borrow_extend_requests | {"type": "all"} | finance.phieu_hang_muon.view | cờ blade is_* | html |
| erp.borrow_extend_request.page.forAccounting | admin/warehouse/borrow_extend_requests/forAccounting |  | finance.phieu_hang_muon.view | cờ blade is_* | html |
| erp.borrow_extend_request.searchData.all | admin/warehouse/borrow_extend_requests/searchData | {"type": "all"} | finance.phieu_hang_muon.view | searchByFilter type=all | datatables |
| erp.borrow_extend_request.searchData.for-approve | admin/warehouse/borrow_extend_requests/searchData | {"type": "for-approve"} | finance.phieu_hang_muon.view | searchByFilter type=for-approve | datatables |
| erp.borrow_extend_request.searchData.accounting | admin/warehouse/borrow_extend_requests/searchData | {"type": "accounting"} | finance.phieu_hang_muon.view | searchByFilter type=accounting | datatables |
| erp.borrow_extend_request.show | admin/warehouse/borrow_extend_requests/{id}/show |  | finance.phieu_hang_muon.view | canView | detail ids=[3239, 3238, 3237, 3236, 3235, 3234] |
| erp.borrow_sell_request.index | admin/warehouse/borrow_sell_requests | {"type": "all"} | finance.xuat_hang_vuot_han_muc_cong_no_* | cờ blade is_* | html |
| erp.borrow_sell_request.page.forAccounting | admin/warehouse/borrow_sell_requests/forAccounting |  | finance.xuat_hang_vuot_han_muc_cong_no_* | cờ blade is_* | html |
| erp.borrow_sell_request.searchData.all | admin/warehouse/borrow_sell_requests/searchData | {"type": "all"} | finance.xuat_hang_vuot_han_muc_cong_no_* | searchByFilter type=all | datatables |
| erp.borrow_sell_request.searchData.waiting_approve | admin/warehouse/borrow_sell_requests/searchData | {"type": "waiting_approve"} | finance.xuat_hang_vuot_han_muc_cong_no_* | searchByFilter type=waiting_approve | datatables |
| erp.borrow_sell_request.searchData.accounting | admin/warehouse/borrow_sell_requests/searchData | {"type": "accounting"} | finance.xuat_hang_vuot_han_muc_cong_no_* | searchByFilter type=accounting | datatables |
| erp.borrow_sell_request.show | admin/warehouse/borrow_sell_requests/{id}/show |  | finance.xuat_hang_vuot_han_muc_cong_no_* | canView | detail ids=[5270, 5269, 5268, 5267, 5266, 5265] |
| erp.self_inventory_request.index | admin/warehouse/self_inventory_requests | {"type": "all"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | cờ blade is_* | html |
| erp.self_inventory_request.page.all | admin/warehouse/self_inventory_requests/all |  | finance.tong_kiem_ke_kho_theo_hang_hoa.view | cờ blade is_* | html |
| erp.self_inventory_request.searchData.all | admin/warehouse/self_inventory_requests/searchData | {"type": "all"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | searchByFilter type=all | datatables |
| erp.self_inventory_request.searchData.index | admin/warehouse/self_inventory_requests/searchData | {"type": "index"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | searchByFilter type=index | datatables |
| erp.self_inventory_request.show | admin/warehouse/self_inventory_requests/{id}/show |  | finance.tong_kiem_ke_kho_theo_hang_hoa.view | canView | detail ids=[3, 2, 1] |
| erp.self_inventory_request_all.index | admin/warehouse/self_inventory_request_alls | {"type": "all"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | cờ blade is_* | html |
| erp.self_inventory_request_all.searchData.all | admin/warehouse/self_inventory_request_alls/searchData | {"type": "all"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | searchByFilter type=all | datatables |
| erp.self_inventory_request_all.searchData.index | admin/warehouse/self_inventory_request_alls/searchData | {"type": "index"} | finance.tong_kiem_ke_kho_theo_hang_hoa.view | searchByFilter type=index | datatables |
| erp.prepick_cancel_request.index | admin/warehouse/prepick_cancel_requests | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_cancel_request.page.forAccounting | admin/warehouse/prepick_cancel_requests/forAccounting |  | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_cancel_request.searchData.all | admin/warehouse/prepick_cancel_requests/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.prepick_cancel_request.searchData.accounting | admin/warehouse/prepick_cancel_requests/searchData | {"type": "accounting"} | finance.phieu_hang_giu.view | searchByFilter type=accounting | datatables |
| erp.prepick_cancel_request.show | admin/warehouse/prepick_cancel_requests/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[4630, 4629, 4628, 4627, 4626, 4625] |
| erp.prepick_cancel.index | admin/warehouse/prepick_cancels | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_cancel.searchData.none | admin/warehouse/prepick_cancels/searchData |  | finance.phieu_hang_giu.view | searchByFilter type=None | datatables |
| erp.prepick_cancel.searchData.all | admin/warehouse/prepick_cancels/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.prepick_cancel.show | admin/warehouse/prepick_cancels/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[4563, 4562, 4561, 4560, 4559, 4558] |
| erp.prepick_extend_request.index | admin/warehouse/prepick_extend_requests | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_extend_request.page.forAccounting | admin/warehouse/prepick_extend_requests/forAccounting |  | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_extend_request.searchData.all | admin/warehouse/prepick_extend_requests/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.prepick_extend_request.searchData.waiting_approve | admin/warehouse/prepick_extend_requests/searchData | {"type": "waiting_approve"} | finance.phieu_hang_giu.view | searchByFilter type=waiting_approve | datatables |
| erp.prepick_extend_request.searchData.accounting | admin/warehouse/prepick_extend_requests/searchData | {"type": "accounting"} | finance.phieu_hang_giu.view | searchByFilter type=accounting | datatables |
| erp.prepick_extend_request.show | admin/warehouse/prepick_extend_requests/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[1988, 1987, 1986, 1985, 1984, 1983] |
| erp.prepick_transfer2.index | admin/warehouse/prepick_transfer2 | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.prepick_transfer2.searchData.all | admin/warehouse/prepick_transfer2/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.prepick_transfer2.searchData.approve | admin/warehouse/prepick_transfer2/searchData | {"type": "approve"} | finance.phieu_hang_giu.view | searchByFilter type=approve | datatables |
| erp.prepick_transfer2.show | admin/warehouse/prepick_transfer2/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[1751, 1750, 1749, 1748, 1747, 1746] |
| erp.product_export.index | admin/warehouse/product_exports | {"type": "all"} | finance.phieu_xuat_hang.view | cờ blade is_* | html |
| erp.product_export.page.all | admin/warehouse/product_exports/all |  | finance.phieu_xuat_hang.view | cờ blade is_* | html |
| erp.product_export.page.forAccounting | admin/warehouse/product_exports/forAccounting |  | finance.phieu_xuat_hang.view | cờ blade is_* | html |
| erp.product_export.searchData.all | admin/warehouse/product_exports/searchData | {"type": "all"} | finance.phieu_xuat_hang.view | searchByFilter type=all | datatables |
| erp.product_export.searchData.forAccounting | admin/warehouse/product_exports/searchData | {"type": "forAccounting"} | finance.phieu_xuat_hang.view | searchByFilter type=forAccounting | datatables |
| erp.product_export.show | admin/warehouse/product_exports/{id}/show |  | finance.phieu_xuat_hang.view | canView | detail ids=[43283, 43282, 43281, 43280, 43279, 43278] |
| erp.product_export_request.index | admin/warehouse/product_export_requests | {"type": "all"} | finance.yeu_cau_xuat_hang.view | cờ blade is_* | html |
| erp.product_export_request.page.all | admin/warehouse/product_export_requests/all |  | finance.yeu_cau_xuat_hang.view | cờ blade is_* | html |
| erp.product_export_request.page.forAccounting | admin/warehouse/product_export_requests/forAccounting |  | finance.yeu_cau_xuat_hang.view | cờ blade is_* | html |
| erp.product_export_request.searchData.all | admin/warehouse/product_export_requests/searchData | {"type": "all"} | finance.yeu_cau_xuat_hang.view | searchByFilter type=all | datatables |
| erp.product_export_request.searchData.for_approve | admin/warehouse/product_export_requests/searchData | {"type": "for_approve"} | finance.yeu_cau_xuat_hang.view | searchByFilter type=for_approve | datatables |
| erp.product_export_request.searchData.for-manager | admin/warehouse/product_export_requests/searchData | {"type": "for-manager"} | finance.yeu_cau_xuat_hang.view | searchByFilter type=for-manager | datatables |
| erp.product_export_request.searchData.accounting | admin/warehouse/product_export_requests/searchData | {"type": "accounting"} | finance.yeu_cau_xuat_hang.view | searchByFilter type=accounting | datatables |
| erp.product_export_request.show | admin/warehouse/product_export_requests/{id}/show |  | finance.yeu_cau_xuat_hang.view | canView | detail ids=[44441, 44440, 44439, 44438, 44437, 44436] |
| erp.product_import.index | admin/warehouse/product_imports | {"type": "all"} | finance.phieu_nhap_hang.view | cờ blade is_* | html |
| erp.product_import.page.all | admin/warehouse/product_imports/all |  | finance.phieu_nhap_hang.view | cờ blade is_* | html |
| erp.product_import.page.forAccounting | admin/warehouse/product_imports/forAccounting |  | finance.phieu_nhap_hang.view | cờ blade is_* | html |
| erp.product_import.searchData.all | admin/warehouse/product_imports/searchData | {"type": "all"} | finance.phieu_nhap_hang.view | searchByFilter type=all | datatables |
| erp.product_import.searchData.forAccounting | admin/warehouse/product_imports/searchData | {"type": "forAccounting"} | finance.phieu_nhap_hang.view | searchByFilter type=forAccounting | datatables |
| erp.product_import.show | admin/warehouse/product_imports/{id}/show |  | finance.phieu_nhap_hang.view | canView | detail ids=[15814, 15813, 15812, 15811, 15810, 15809] |
| erp.product_import_direct_transfer.index | admin/warehouse/product_import_direct_transfer_requests | {"type": "all"} | finance.phieu_chuyen_hang_nhap_thang.view | cờ blade is_* | html |
| erp.product_import_direct_transfer.searchData.all | admin/warehouse/product_import_direct_transfer_requests/searchData | {"type": "all"} | finance.phieu_chuyen_hang_nhap_thang.view | searchByFilter type=all | datatables |
| erp.product_import_direct_transfer.searchData.waiting_approve | admin/warehouse/product_import_direct_transfer_requests/searchData | {"type": "waiting_approve"} | finance.phieu_chuyen_hang_nhap_thang.view | searchByFilter type=waiting_approve | datatables |
| erp.product_import_direct_transfer.show | admin/warehouse/product_import_direct_transfer_requests/{id}/show |  | finance.phieu_chuyen_hang_nhap_thang.view | canView | detail ids=[1025, 1024, 1023, 1022, 1021, 1020] |
| erp.product_import_request.index | admin/warehouse/product_import_requests | {"type": "all"} | finance.yeu_cau_nhap_hang.view | cờ blade is_* | html |
| erp.product_import_request.page.all | admin/warehouse/product_import_requests/all |  | finance.yeu_cau_nhap_hang.view | cờ blade is_* | html |
| erp.product_import_request.page.forAccounting | admin/warehouse/product_import_requests/forAccounting |  | finance.yeu_cau_nhap_hang.view | cờ blade is_* | html |
| erp.product_import_request.searchData.all | admin/warehouse/product_import_requests/searchData | {"type": "all"} | finance.yeu_cau_nhap_hang.view | searchByFilter type=all | datatables |
| erp.product_import_request.searchData.for_approve | admin/warehouse/product_import_requests/searchData | {"type": "for_approve"} | finance.yeu_cau_nhap_hang.view | searchByFilter type=for_approve | datatables |
| erp.product_import_request.searchData.managerApprove | admin/warehouse/product_import_requests/searchData | {"type": "managerApprove"} | finance.yeu_cau_nhap_hang.view | searchByFilter type=managerApprove | datatables |
| erp.product_import_request.searchData.departmentManagerApprove | admin/warehouse/product_import_requests/searchData | {"type": "departmentManagerApprove"} | finance.yeu_cau_nhap_hang.view | searchByFilter type=departmentManagerApprove | datatables |
| erp.product_import_request.searchData.accounting | admin/warehouse/product_import_requests/searchData | {"type": "accounting"} | finance.yeu_cau_nhap_hang.view | searchByFilter type=accounting | datatables |
| erp.product_import_request.show | admin/warehouse/product_import_requests/{id}/show |  | finance.yeu_cau_nhap_hang.view | canView | detail ids=[15588, 15587, 15586, 15585, 15584, 15583] |
| erp.product_prepick_request.index | admin/warehouse/product_prepick_requests | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.product_prepick_request.page.all | admin/warehouse/product_prepick_requests/all |  | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.product_prepick_request.page.forAccounting | admin/warehouse/product_prepick_requests/forAccounting |  | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.product_prepick_request.searchData.all | admin/warehouse/product_prepick_requests/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.product_prepick_request.searchData.accounting | admin/warehouse/product_prepick_requests/searchData | {"type": "accounting"} | finance.phieu_hang_giu.view | searchByFilter type=accounting | datatables |
| erp.product_prepick_request.show | admin/warehouse/product_prepick_requests/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[2742, 2741, 2740, 2739, 2738, 2737] |
| erp.product_transfer.index | admin/warehouse/product_transfers | {"type": "all"} | finance.phieu_dieu_chuyen_hang.view | cờ blade is_* | html |
| erp.product_transfer.searchData.all | admin/warehouse/product_transfers/searchData | {"type": "all"} | finance.phieu_dieu_chuyen_hang.view | searchByFilter type=all | datatables |
| erp.product_transfer.show | admin/warehouse/product_transfers/{id}/show |  | finance.phieu_dieu_chuyen_hang.view | canView | detail ids=[1117, 1116, 1115, 1114, 1113, 1112] |
| erp.product_transfer_request.index | admin/warehouse/product_transfer_requests | {"type": "all"} | finance.yeu_cau_chuyen_hang.view | cờ blade is_* | html |
| erp.product_transfer_request.page.all | admin/warehouse/product_transfer_requests/all |  | finance.yeu_cau_chuyen_hang.view | cờ blade is_* | html |
| erp.product_transfer_request.page.forAccounting | admin/warehouse/product_transfer_requests/forAccounting |  | finance.yeu_cau_chuyen_hang.view | cờ blade is_* | html |
| erp.product_transfer_request.searchData.all | admin/warehouse/product_transfer_requests/searchData | {"type": "all"} | finance.yeu_cau_chuyen_hang.view | searchByFilter type=all | datatables |
| erp.product_transfer_request.searchData.approve | admin/warehouse/product_transfer_requests/searchData | {"type": "approve"} | finance.yeu_cau_chuyen_hang.view | searchByFilter type=approve | datatables |
| erp.product_transfer_request.show | admin/warehouse/product_transfer_requests/{id}/show |  | finance.yeu_cau_chuyen_hang.view | canView | detail ids=[8230, 8229, 8228, 8227, 8226, 8225] |
| erp.warehouse_export_request.index | admin/warehouse/warehouse_export_requests | {"type": "all"} | finance.de_nghi_xuat_kho.view | cờ blade is_* | html |
| erp.warehouse_export_request.page.forWarehouse | admin/warehouse/warehouse_export_requests/forWarehouse |  | finance.de_nghi_xuat_kho.view | cờ blade is_* | html |
| erp.warehouse_export_request.searchData.all | admin/warehouse/warehouse_export_requests/searchData | {"type": "all"} | finance.de_nghi_xuat_kho.view | searchByFilter type=all | datatables |
| erp.warehouse_export_request.searchData.for-approve | admin/warehouse/warehouse_export_requests/searchData | {"type": "for-approve"} | finance.de_nghi_xuat_kho.view | searchByFilter type=for-approve | datatables |
| erp.warehouse_export_request.searchData.warehouse | admin/warehouse/warehouse_export_requests/searchData | {"type": "warehouse"} | finance.de_nghi_xuat_kho.view | searchByFilter type=warehouse | datatables |
| erp.warehouse_export_request.show | admin/warehouse/warehouse_export_requests/{id}/show |  | finance.de_nghi_xuat_kho.view | canView | detail ids=[39058, 39057, 39056, 39055, 39054, 39053] |
| erp.warehouse_import.index | admin/warehouse/warehouse_imports | {"type": "all"} | finance.phieu_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import.page.all | admin/warehouse/warehouse_imports/all |  | finance.phieu_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import.page.forAccounting | admin/warehouse/warehouse_imports/forAccounting |  | finance.phieu_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import.searchData.all | admin/warehouse/warehouse_imports/searchData | {"type": "all"} | finance.phieu_nhap_kho.view | searchByFilter type=all | datatables |
| erp.warehouse_import.searchData.for_approve | admin/warehouse/warehouse_imports/searchData | {"type": "for_approve"} | finance.phieu_nhap_kho.view | searchByFilter type=for_approve | datatables |
| erp.warehouse_import.searchData.approve | admin/warehouse/warehouse_imports/searchData | {"type": "approve"} | finance.phieu_nhap_kho.view | searchByFilter type=approve | datatables |
| erp.warehouse_import.show | admin/warehouse/warehouse_imports/{id}/show |  | finance.phieu_nhap_kho.view | canView | detail ids=[11594, 11593, 11592, 11591, 11590, 11589] |
| erp.warehouse_import_request.index | admin/warehouse/warehouse_import_requests | {"type": "all"} | finance.de_nghi_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import_request.page.all | admin/warehouse/warehouse_import_requests/all |  | finance.de_nghi_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import_request.page.forWarehouse | admin/warehouse/warehouse_import_requests/forWarehouse |  | finance.de_nghi_nhap_kho.view | cờ blade is_* | html |
| erp.warehouse_import_request.searchData.all | admin/warehouse/warehouse_import_requests/searchData | {"type": "all"} | finance.de_nghi_nhap_kho.view | searchByFilter type=all | datatables |
| erp.warehouse_import_request.searchData.for-approve | admin/warehouse/warehouse_import_requests/searchData | {"type": "for-approve"} | finance.de_nghi_nhap_kho.view | searchByFilter type=for-approve | datatables |
| erp.warehouse_import_request.searchData.warehouse | admin/warehouse/warehouse_import_requests/searchData | {"type": "warehouse"} | finance.de_nghi_nhap_kho.view | searchByFilter type=warehouse | datatables |
| erp.warehouse_import_request.show | admin/warehouse/warehouse_import_requests/{id}/show |  | finance.de_nghi_nhap_kho.view | canView | detail ids=[11044, 11043, 11042, 11041, 11040, 11039] |
| erp.warehouse_prepick_request.index | admin/warehouse/warehouse_prepick_requests | {"type": "all"} | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.warehouse_prepick_request.page.all | admin/warehouse/warehouse_prepick_requests/all |  | finance.phieu_hang_giu.view | cờ blade is_* | html |
| erp.warehouse_prepick_request.searchData.all | admin/warehouse/warehouse_prepick_requests/searchData | {"type": "all"} | finance.phieu_hang_giu.view | searchByFilter type=all | datatables |
| erp.warehouse_prepick_request.searchData.for-approve | admin/warehouse/warehouse_prepick_requests/searchData | {"type": "for-approve"} | finance.phieu_hang_giu.view | searchByFilter type=for-approve | datatables |
| erp.warehouse_prepick_request.show | admin/warehouse/warehouse_prepick_requests/{id}/show |  | finance.phieu_hang_giu.view | canView | detail ids=[2744, 2743, 2742, 2741, 2740, 2739] |
| erp.home.approveList | admin/approveList |  | finance.*.approve (đếm việc chờ) | đếm việc chờ | lists |
| erp.account_banks.index | admin/accounting/account-banks |  | finance.danh_muc_tai_khoan_ngan_hang.manage | chặn trang | html |
| erp.declare_limit_debt.index | admin/accounting/declare-limit-debt |  | finance.khai_bao_han_muc_cong_no_khach_hang.* | cờ | html |
| erp.declare_limit_debt.searchData | admin/accounting/declare-limit-debt/searchData |  | finance.khai_bao_han_muc_cong_no_khach_hang.* | getDeclareLimitDebt | auto |
| api.accounts.index | finance/accounts | {"per_page": 50} | finance.* | danh sách | auto |
| api.accounts.index.all | finance/accounts | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.type-accounts.index | finance/type-accounts | {"per_page": 50} | finance.* | danh sách | auto |
| api.type-accounts.index.all | finance/type-accounts | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.currencies.index | finance/currencies | {"per_page": 50} | finance.* | danh sách | auto |
| api.currencies.index.all | finance/currencies | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.works.index | finance/works | {"per_page": 50} | finance.* | danh sách | auto |
| api.works.index.all | finance/works | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.cost-debts.index | finance/cost-debts | {"per_page": 50} | finance.* | danh sách | auto |
| api.cost-debts.index.all | finance/cost-debts | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.source-capitals.index | finance/source-capitals | {"per_page": 50} | finance.* | danh sách | auto |
| api.source-capitals.index.all | finance/source-capitals | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.account-banks.index | finance/account-banks | {"per_page": 50} | finance.* | danh sách | auto |
| api.account-banks.index.all | finance/account-banks | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-transfer-requests.index | finance/product-transfer-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-transfer-requests.index.all | finance/product-transfer-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-transfers.index | finance/product-transfers | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-transfers.index.all | finance/product-transfers | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-income-requests.index | finance/bill-income-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-income-requests.index.all | finance/bill-income-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-income-requests/pending.index | finance/bill-income-requests/pending | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-income-requests/pending.index.all | finance/bill-income-requests/pending | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-incomes.index | finance/bill-incomes | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-incomes.index.all | finance/bill-incomes | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-income-reports.index | finance/bill-income-reports | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-income-reports.index.all | finance/bill-income-reports | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-payments.index | finance/bill-payments | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-payments.index.all | finance/bill-payments | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-payment-authorizations.index | finance/bill-payment-authorizations | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-payment-authorizations.index.all | finance/bill-payment-authorizations | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-payment-requests.index | finance/bill-payment-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-payment-requests.index.all | finance/bill-payment-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-adjust-dept-requests.index | finance/bill-adjust-dept-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-adjust-dept-requests.index.all | finance/bill-adjust-dept-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.bill-adjust-depts.index | finance/bill-adjust-depts | {"per_page": 50} | finance.* | danh sách | auto |
| api.bill-adjust-depts.index.all | finance/bill-adjust-depts | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.addition-accounting-requests.index | finance/addition-accounting-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.addition-accounting-requests.index.all | finance/addition-accounting-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-imports.index | finance/product-imports | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-imports.index.all | finance/product-imports | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-import-requests.index | finance/product-import-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-import-requests.index.all | finance/product-import-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-import-direct-transfers.index | finance/product-import-direct-transfers | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-import-direct-transfers.index.all | finance/product-import-direct-transfers | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.warehouse-imports.index | finance/warehouse-imports | {"per_page": 50} | finance.* | danh sách | auto |
| api.warehouse-imports.index.all | finance/warehouse-imports | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.warehouse-import-requests.index | finance/warehouse-import-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.warehouse-import-requests.index.all | finance/warehouse-import-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.borrow-export-requests.index | finance/borrow-export-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.borrow-export-requests.index.all | finance/borrow-export-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.borrow-extend-requests.index | finance/borrow-extend-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.borrow-extend-requests.index.all | finance/borrow-extend-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.borrow-sell-requests.index | finance/borrow-sell-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.borrow-sell-requests.index.all | finance/borrow-sell-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.borrow-stocks.index | finance/borrow-stocks | {"per_page": 50} | finance.* | danh sách | auto |
| api.borrow-stocks.index.all | finance/borrow-stocks | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.prepick-cancel-requests.index | finance/prepick-cancel-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.prepick-cancel-requests.index.all | finance/prepick-cancel-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.prepick-extend-requests.index | finance/prepick-extend-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.prepick-extend-requests.index.all | finance/prepick-extend-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.prepick-transfer-requests.index | finance/prepick-transfer-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.prepick-transfer-requests.index.all | finance/prepick-transfer-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.product-prepick-requests.index | finance/product-prepick-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.product-prepick-requests.index.all | finance/product-prepick-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.warehouse-prepick-requests.index | finance/warehouse-prepick-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.warehouse-prepick-requests.index.all | finance/warehouse-prepick-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.prepick-stocks.index | finance/prepick-stocks | {"per_page": 50} | finance.* | danh sách | auto |
| api.prepick-stocks.index.all | finance/prepick-stocks | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.accounting-prepick-cancels.index | finance/accounting-prepick-cancels | {"per_page": 50} | finance.* | danh sách | auto |
| api.accounting-prepick-cancels.index.all | finance/accounting-prepick-cancels | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.self-inventory-requests.index | finance/self-inventory-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.self-inventory-requests.index.all | finance/self-inventory-requests | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.position-inventories.index | finance/position-inventories | {"per_page": 50} | finance.* | danh sách | auto |
| api.position-inventories.index.all | finance/position-inventories | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.declare-limit-debts.index | finance/declare-limit-debts | {"per_page": 50} | finance.* | danh sách | auto |
| api.declare-limit-debts.index.all | finance/declare-limit-debts | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.declare-debt-beginnings.index | finance/declare-debt-beginnings | {"per_page": 50} | finance.* | danh sách | auto |
| api.declare-debt-beginnings.index.all | finance/declare-debt-beginnings | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.declare-debt-supplier-beginnings.index | finance/declare-debt-supplier-beginnings | {"per_page": 50} | finance.* | danh sách | auto |
| api.declare-debt-supplier-beginnings.index.all | finance/declare-debt-supplier-beginnings | {"per_page": 50, "type": "all"} | finance.* | danh sách | auto |
| api.assign/product-export-requests.index | assign/product-export-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.assign/warehouse-export-requests.index | assign/warehouse-export-requests | {"per_page": 50} | finance.* | danh sách | auto |
| api.assign/product-exports.index | assign/product-exports | {"per_page": 50} | finance.* | danh sách | auto |
