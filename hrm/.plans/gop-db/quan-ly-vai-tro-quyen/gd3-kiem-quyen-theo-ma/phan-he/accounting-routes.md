# accounting — đường đọc chụp mốc (GĐ3 Task 8.9)

Tài khoản (rehearsal, công ty 1 — ERP kiểm quyền theo công ty trong hồ sơ):

- `pv4` NV 13 — namdangit — 27 mã accounting có phạm vi ở mức 4 + 17 mã không phạm vi, công ty 1
- `pv3` NV 207 — hantt.kthn — 23 mã ở mức 3, 1 mã mức 4, 14 mã không phạm vi, công ty 1
- `pv2` NV 24 — tuannd.kd1 — 13 mã ở mức 2, 1 mã mức 3, không mã không phạm vi, công ty 1
- `pv1` NV 110 — honglv.pt — 11 mã ở mức 1 (Bộ phận), công ty 1
- `tron` NV 148 — hieudd.da — 4 mã mức 2, 1 mức 3, 1 mã không phạm vi, công ty 1
- `khong_ma` NV 311 — thombt.khohn — không có mã accounting.* nào, công ty 1

Ca thiếu: **có mã Xem không phạm vi** (rehearsal 0 người có mã accounting có phạm vi mà scope NULL) và **khác công ty** ⇒ phủ bằng PHPUnit (`AccountingScopeConversionTest` mức null / c2).

Bỏ khỏi mốc HTTP (chạy > 60 s trên rehearsal, làm sập php -S): erp.account_details.searchData, erp.account_details.searchDataDebtCustomer, erp.account_details.searchDataBalance, erp.account_details.searchDataDebtEmployee, erp.account_details.searchDataBalanceEmployee, erp.account_details.searchDataAccountDetailBook, erp.account_details.searchData.supplier, erp.report.analysis_profit_contract.searchData — phủ bằng AccountingScopeConversionTest (DB::pretend).

| # | app | method | url | mã | chuỗi phạm vi? | cột lọc / ghi chú | params | extract |
|---|---|---|---|---|---|---|---|---|
| 1 | erp | GET | `admin/accounting/bill_bonus_business` | `accounting.phieu_tinh_thuong_kinh_doanh.view` | có | cờ blade |  | html |
| 2 | erp | GET | `admin/accounting/bill_bonus_business/searchData` | `accounting.phieu_tinh_thuong_kinh_doanh.view` | có | -=all chuỗi phạm vi |  | datatables |
| 3 | erp | GET | `admin/accounting/bill_commission_settlement_months` | `accounting.quyet_toan_hoa_hong_thang.view` | có | cờ blade |  | html |
| 4 | erp | GET | `admin/accounting/bill_commission_settlement_months/searchData` | `accounting.quyet_toan_hoa_hong_thang.view` | có | _type=all chuỗi phạm vi | _type=all | datatables |
| 5 | erp | GET | `admin/accounting/bill_commission_settlement_quarters` | `accounting.quyet_toan_hoa_hong_quy.view` | có | cờ blade |  | html |
| 6 | erp | GET | `admin/accounting/bill_commission_settlement_quarters/searchData` | `accounting.quyet_toan_hoa_hong_quy.view` | có | _type=all chuỗi phạm vi | _type=all | datatables |
| 7 | erp | GET | `admin/accounting/bill_productivity_settlement_quarters` | `accounting.quyet_toan_hoa_hong_quy.view` | có | cờ blade |  | html |
| 8 | erp | GET | `admin/accounting/bill_productivity_settlement_quarters/searchData` | `accounting.quyet_toan_hoa_hong_quy.view` | có | _type=all chuỗi phạm vi | _type=all | datatables |
| 9 | erp | GET | `admin/accounting/closing_entries` | `accounting.ket_chuyen_chi_phi_phai_tra.view` | có | cờ blade |  | html |
| 10 | erp | GET | `admin/accounting/closing_entries/searchData` | `accounting.ket_chuyen_chi_phi_phai_tra.view` | có | -=all chuỗi phạm vi |  | datatables |
| 11 | erp | GET | `admin/customer-care/wr_accounting_service_requests` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | cờ blade |  | html |
| 12 | erp | GET | `admin/customer-care/wr_accounting_service_requests/searchData` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | type=all chuỗi phạm vi | type=all | datatables |
| 13 | erp | GET | `admin/customer-care/wr_accounting_services` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | cờ blade |  | html |
| 14 | erp | GET | `admin/customer-care/wr_accounting_services/searchData` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | type=all chuỗi phạm vi | type=all | datatables |
| 15 | erp | GET | `admin/income-expenditure/bill_profits` | `accounting.phieu_tinh_lai.view` | có | cờ blade |  | html |
| 16 | erp | GET | `admin/income-expenditure/bill_profits/searchData` | `accounting.phieu_tinh_lai.view` | có | _type=all chuỗi phạm vi | _type=all | datatables |
| 17 | erp | GET | `admin/warehouse/beginning_accounting_stocks` | `accounting.khai_bao_ton_kho_ke_toan.view` | có | cờ blade |  | html |
| 18 | erp | GET | `admin/warehouse/beginning_accounting_stocks/searchData` | `accounting.khai_bao_ton_kho_ke_toan.view` | có | -=all chuỗi phạm vi |  | datatables |
| 19 | erp | GET | `admin/warehouse/borrow_sells` | `accounting.phieu_xuat_ban_hang_muon.view` | có | cờ blade |  | html |
| 20 | erp | GET | `admin/warehouse/borrow_sells/searchData` | `accounting.phieu_xuat_ban_hang_muon.view` | có | _type=all chuỗi phạm vi | _type=all | datatables |
| 21 | erp | GET | `admin/warehouse/borrow_sell_requests` | `accounting.phieu_yeu_cau_xuat_ban_hang_muon.view` | có | cờ blade |  | html |
| 22 | erp | GET | `admin/warehouse/borrow_sell_requests/searchData` | `accounting.phieu_yeu_cau_xuat_ban_hang_muon.view` | có | type=all chuỗi phạm vi | type=all | datatables |
| 23 | erp | GET | `admin/warehouse/join_export_requests` | `accounting.yeu_cau_xuat_ghep.view` | có | cờ blade |  | html |
| 24 | erp | GET | `admin/warehouse/join_export_requests/searchData` | `accounting.yeu_cau_xuat_ghep.view` | có | type=all chuỗi phạm vi | type=all | datatables |
| 25 | erp | GET | `admin/warehouse/split_export_requests` | `accounting.yeu_cau_xuat_tach.view` | có | cờ blade |  | html |
| 26 | erp | GET | `admin/warehouse/split_export_requests/searchData` | `accounting.yeu_cau_xuat_tach.view` | có | type=all chuỗi phạm vi | type=all | datatables |
| 27 | erp | GET | `admin/warehouse/join_export_requests/all` | `accounting.yeu_cau_xuat_ghep.view` | có | trang tất cả: cờ + bộ lọc kho |  | html |
| 28 | erp | GET | `admin/warehouse/split_export_requests/all` | `accounting.yeu_cau_xuat_tach.view` | có | trang tất cả: cờ + bộ lọc kho |  | html |
| 29 | erp | GET | `admin/customer-care/wr_accounting_service_requests/all` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | trang tất cả: cờ + bộ lọc kho |  | html |
| 30 | erp | GET | `admin/customer-care/wr_accounting_services/all` | `accounting.phieu_hach_toan_dich_vu_hddv.view` | có | trang tất cả: cờ + bộ lọc kho |  | html |
| 31 | erp | GET | `admin/accounting/bill_commission_settlement_quarters/searchData` | `accounting.quyet_toan_hoa_hong_quy.approve` | không | _type=approved: có quyền duyệt ⇒ phiếu chờ duyệt, không ⇒ của mình | _type=approved | datatables |
| 32 | erp | GET | `admin/accounting/bill_productivity_settlement_quarters/searchData` | `accounting.quyet_toan_hoa_hong_quy.approve` | không | _type=approved: có quyền duyệt ⇒ phiếu chờ duyệt, không ⇒ của mình | _type=approved | datatables |
| 33 | erp | GET | `admin/income-expenditure/bill_profits/searchData` | `accounting.quyet_toan_hoa_hong_quy.approve` | không | _type=approved: có quyền duyệt ⇒ phiếu chờ duyệt, không ⇒ của mình | _type=approved | datatables |
| 34 | erp | GET | `admin/customer-care/wr_accounting_service_requests/searchData` | `accounting.ke_toan_kho.manage` | không | type=wait_approve: Kế toán kho | type=wait_approve | datatables |
| 35 | erp | GET | `admin/warehouse/borrow_sell_requests/forAccounting` | `accounting.ke_toan_kho.manage` | không | route checkPermission Kế toán kho |  | html |
| 36 | erp | GET | `admin/warehouse/join_export_requests/forAccounting` | `accounting.ke_toan_kho.manage` | không | route checkPermission Kế toán kho |  | html |
| 37 | erp | GET | `admin/warehouse/split_export_requests/forAccounting` | `accounting.ke_toan_kho.manage` | không | route checkPermission Kế toán kho |  | html |
| 38 | erp | GET | `admin/accounting/account_details` | `accounting.so_chi_tiet_cong_no_phai_thu_khach_hang.view` | có | phạm vi 4/3 + company |  | html |
| 39 | erp | GET | `admin/accounting/account_details/balance-debt` | `accounting.bang_can_doi_phat_sinh_cong_no_khach_hang.view` | có | phạm vi 4/3 + company |  | html |
| 40 | erp | GET | `admin/accounting/account_details/list-detail-debt-employee` | `accounting.so_chi_tiet_cong_no_nhan_vien.view` | có | phạm vi 4/3 + company |  | html |
| 41 | erp | GET | `admin/accounting/account_details/balance-debt-employee` | `accounting.bang_can_doi_phat_sinh_cong_no_nhan_vien.view` | có | phạm vi 4/3 + company |  | html |
| 42 | erp | GET | `admin/accounting/account_details/account-detail-book` | `accounting.so_chi_tiet_tai_khoan.view` | có | phạm vi 4/3 + company |  | html |
| 43 | erp | GET | `admin/reports/summary_sale` | `accounting.bao_cao_tong_hop_ban_hang.view` | có | cờ is_* / chuỗi phạm vi | type=all | html |
| 44 | erp | GET | `admin/reports/summary_sale` | `accounting.bao_cao_ban_hang_theo_mat_hang.view` | có | cờ is_* / chuỗi phạm vi | type=item | html |
| 45 | erp | GET | `admin/reports/summary_sale/searchData` | `accounting.bao_cao_tong_hop_ban_hang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3, type=all | auto |
| 46 | erp | GET | `admin/reports/summary_sale/searchData` | `accounting.bao_cao_ban_hang_theo_mat_hang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3, type=item | auto |
| 47 | erp | GET | `admin/reports/summary_sale/getReportSaleDetail` | `accounting.bao_cao_ban_hang_theo_mat_hang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3, type=item | auto |
| 48 | erp | GET | `admin/reports/revenue-contract-valid` | `accounting.bao_cao_doanh_thu_hop_dong_hieu_luc.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 49 | erp | GET | `admin/reports/revenue-contract-valid/searchData` | `accounting.bao_cao_doanh_thu_hop_dong_hieu_luc.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 50 | erp | GET | `admin/reports/bonus-contract-report` | `accounting.bao_cao_thuong_theo_hop_dong.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 51 | erp | GET | `admin/reports/bonus-contract-report/searchData` | `accounting.bao_cao_thuong_theo_hop_dong.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 52 | erp | GET | `admin/reports/commission-month` | `accounting.bao_cao_thuong_nang_suat_thang.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 53 | erp | GET | `admin/reports/commission-month/searchData` | `accounting.bao_cao_thuong_nang_suat_thang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 54 | erp | GET | `admin/reports/commission-quarter` | `accounting.bao_cao_thuong_nang_suat_thang.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 55 | erp | GET | `admin/reports/commission-quarter/searchData` | `accounting.bao_cao_thuong_nang_suat_thang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 56 | erp | GET | `admin/reports/commission-settlement-quarter` | `accounting.bao_cao_tong_thu_nhap_tu_ban_hang.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 57 | erp | GET | `admin/reports/commission-settlement-quarter/searchData` | `accounting.bao_cao_tong_thu_nhap_tu_ban_hang.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 58 | erp | GET | `admin/reports/commission-month-employee` | `accounting.bao_cao_hoa_hong_thang_theo_nhan_vien.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 59 | erp | GET | `admin/reports/commission-month-employee/searchData` | `accounting.bao_cao_hoa_hong_thang_theo_nhan_vien.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 60 | erp | GET | `admin/reports/revenue-commission` | `accounting.bao_cao_doanh_thu_tinh_hoa_hong.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 61 | erp | GET | `admin/reports/revenue-commission/searchData` | `accounting.bao_cao_doanh_thu_tinh_hoa_hong.view` | có | cờ is_* / chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 62 | erp | GET | `admin/reports/analysis-profit-contract` | `accounting.bao_cao_phan_tich_lai_lo_theo_htht_hop_dong.view` | có | cờ is_* / chuỗi phạm vi |  | html |
| 63 | erp | GET | `admin/warehouse/warehouse_infos/product_import_direct_details` | `accounting.bao_cao_ton_hang_nhap_xuat_thang_theo_nhan_vien.view` | có | cờ |  | html |
| 64 | erp | GET | `admin/warehouse/warehouse_infos/product_import_direct_details/searchData` | `accounting.bao_cao_ton_hang_nhap_xuat_thang_theo_nhan_vien.view` | có | chuỗi phạm vi | from_date=01/10/2026, to_date=31/10/2026, start_date=2026-10-01, end_date=2026-10-31, month=10/2026, year=2026, quarter=3 | auto |
| 65 | erp | GET | `admin/warehouse/warehouse_reports/accountingWarehouseProductReport` | `accounting.bao_cao_ton_kho_ke_toan.view` | có | cổng xem / cờ / bộ lọc kho |  | html |
| 66 | erp | GET | `admin/warehouse/warehouse_reports/accountingMultiWarehouseReport` | `accounting.bao_cao_ton_kho_ke_toan.view` | có | cổng xem / cờ / bộ lọc kho |  | html |
| 67 | erp | GET | `admin/warehouse/warehouse_reports/accountingChangeSummaryReport` | `accounting.bao_cao_ton_kho_ke_toan.view` | có | cổng xem / cờ / bộ lọc kho |  | html |
| 68 | erp | GET | `admin/warehouse/warehouse_reports/accountingWarehouseReport` | `accounting.bao_cao_ton_kho_ke_toan.view` | có | cổng xem / cờ / bộ lọc kho |  | html |
| 69 | erp | GET | `admin/warehouse/warehouse_reports/accountingStockCard` | `accounting.bao_cao_ton_kho_ke_toan.view` | có | cổng xem / cờ / bộ lọc kho |  | html |
| 70 | erp | GET | `admin/warehouse/warehouse_reports/accountingWarehouseProductReportSearchData` | `accounting.bao_cao_ton_kho_ke_toan.view` | có |  | from_date=01/01/2026, to_date=31/10/2026, start_date=2026-01-01, end_date=2026-10-31, month=09/2026, year=2026, quarter=3 | auto |
| 71 | erp | GET | `admin/warehouse/warehouse_reports/accountingMultiWarehouseReportSearchData` | `accounting.bao_cao_ton_kho_ke_toan.view` | có |  | from_date=01/01/2026, to_date=31/10/2026, start_date=2026-01-01, end_date=2026-10-31, month=09/2026, year=2026, quarter=3 | auto |
| 72 | erp | GET | `admin/warehouse/warehouse_reports/accountingChangeSummaryReportSearchData` | `accounting.bao_cao_ton_kho_ke_toan.view` | có |  | from_date=01/01/2026, to_date=31/10/2026, start_date=2026-01-01, end_date=2026-10-31, month=09/2026, year=2026, quarter=3 | auto |
| 73 | api | GET | `finance/borrow-sell-requests` | `accounting.ke_toan_kho.manage` | không | type=accounting: Kế toán kho ⇒ phiếu công ty ≠ đang tạo | type=accounting | auto |
| 74 | api | GET | `finance/borrow-sells` | `accounting.ke_toan_kho.manage` | không | meta is_ke_toan_kho |  | auto |
| 75 | api | GET | `finance/product-imports/warehouse-import-sources` | `accounting.ke_toan_kho.manage` | không | Kế toán kho ⇒ phiếu nhập kho chờ duyệt cùng công ty, không ⇒ rỗng |  | auto |
| 76 | api | GET | `finance/product-imports/product-import-request-sources` | `accounting.ke_toan_kho.manage` | không | như trên (YCNH) |  | auto |
| 77 | api | GET | `assign/warehouse-export-requests` | `accounting.ke_toan_kho.manage` | không | cờ can_manage từng dòng (Kế toán kho) |  | {'type': 'auto', 'hash': 'content'} |
