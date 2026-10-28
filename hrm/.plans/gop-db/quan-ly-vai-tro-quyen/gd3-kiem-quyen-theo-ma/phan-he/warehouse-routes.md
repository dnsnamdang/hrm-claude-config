# Phân hệ warehouse — đường ĐỌC chụp mốc (Task 7a, GĐ3)

Nguồn: `scan-wh-0.json` (55 hit scope_chain ERP + 1 client) truy ngược tới route bằng `route:list` ERP / route dump hrm-api; cộng các màn hrm-api lọc phạm vi qua hằng `PERMISSION_VIEW_*` trong Entity (scanner KHÔNG bắt — xem mục "Scanner sót"). File máy đọc: `warehouse-routes.json` (đầu vào `hrm-api/tests/Support/ScopeSnapshot.php`).

Base: ERP `http://127.0.0.1:8012` (DB rehearsal), hrm-api `http://127.0.0.1:8011/api/v1`. Cột "Lấy so_dong" = kiểu trích xuất (xem đầu ScopeSnapshot.php).

| # | app | method | url | mã quyền | chuỗi phạm vi? | cột lọc đang dùng | tham số | lấy so_dong |
|---|---|---|---|---|---|---|---|---|
| 1 | erp | GET | `admin/warehouse/warehouse_exports` | `warehouse.phieu_xuat_kho.view` | có | cờ is_big_boss/is_boss/is_manager (blade) | — | html |
| 2 | erp | GET | `admin/warehouse/warehouse_exports/searchData` | `warehouse.phieu_xuat_kho.view` | có | type=all: 4 ⇒ status≠3 ∪ created_by=tôi; 3 ⇒ company_id ∪ tôi; 2 ⇒ created_by ∈ department_members | length=100 type=all | datatables |
| 3 | erp | GET | `admin/warehouse/warehouse_exports/{id}/show` | `warehouse.phieu_xuat_kho.view` | có | canView: có 1 trong 4 tên Xem (không xét công ty) hoặc Kế toán kho cùng company_id hoặc created_by=tôi | — | detail (12 id) |
| 4 | erp | GET | `admin/warehouse/delivery_trips/searchData` | `warehouse.chuyen_xe.view` | có | route checkPermission:Thủ kho; type=all: 4/3 company_id/2 department_members (created_by) | length=100 type=all | datatables |
| 5 | erp | GET | `admin/warehouse/delivery_trips/{id}/show` | `warehouse.chuyen_xe.view` | có | route Thủ kho + canView (chuỗi Xem chuyến xe) | — | detail (11 id) |
| 6 | erp | GET | `admin/other_delivery_trips/searchData` | `warehouse.chuyen_xe.view` | có | route Thủ kho; type=all: chuỗi Xem chuyến xe | length=100 type=all | datatables |
| 7 | erp | GET | `admin/warehouse/delivery_trip_accounting` | `warehouse.phieu_hach_toan_van_chuyen.view` | có | cờ blade | — | html |
| 8 | erp | GET | `admin/warehouse/delivery_trip_accounting/searchData` | `warehouse.phieu_hach_toan_van_chuyen.view` | có | type=all: 4 tất cả / 3 company_id / còn lại created_by=tôi | length=100 type=all | datatables |
| 9 | erp | GET | `admin/warehouse/other_delivery_trip_accounting` | `warehouse.phieu_hach_toan_van_chuyen.view` | có | cờ blade | — | html |
| 10 | erp | GET | `admin/warehouse/other_delivery_trip_accounting/searchData` | `warehouse.phieu_hach_toan_van_chuyen.view` | có | type=all: như trên | length=100 type=all | datatables |
| 11 | erp | GET | `admin/warehouse/delivery_payment_requests/searchData` | `warehouse.de_nghi_thanh_toan_van_chuyen.view` | có | gọi DeliveryTrip/DeliveryTripAccounting::searchByFilter (type theo request) | length=100 | datatables |
| 12 | erp | GET | `admin/delivery_cost_summaries` | `warehouse.tong_hop_gia_van_chuyen_de_xuat.view` | có | route checkPermission:Quản lý chi phí vận chuyển; cờ blade | type=all | html |
| 13 | erp | GET | `admin/delivery_cost_summaries/searchData` | `warehouse.tong_hop_gia_van_chuyen_de_xuat.view` | có | type=all: 4 tất cả / 3 công ty người lập / 2 phòng ban (created_by) | length=100 type=all | datatables |
| 14 | erp | GET | `admin/delivery_cost_summaries/{id}/show` | `warehouse.tong_hop_gia_van_chuyen_de_xuat.view` | có | canView chuỗi Xem tổng hợp giá VC | — | detail (8 id) |
| 15 | erp | GET | `admin/warehouse/beginning_stocks/searchData` | `warehouse.khai_bao_ton_kho_vat_ly.view` | có | route Thủ kho; 4 tất cả / 3 company_id | length=100 | datatables |
| 16 | erp | GET | `admin/warehouse/warehouse_imports/excShortage/searchData` | `warehouse.xu_ly_thua_thieu_nhap_kho.view` | có | type=employee: 4 tất cả / 3 company_id / còn lại created_by | length=100 type=employee | datatables |
| 17 | erp | GET | `admin/warehouse/warehouse_imports/searchDataDiscrepancy` | `warehouse.xu_ly_thua_thieu_nhap_kho.view` | có | searchByDiscrepancyFilter: 4 tất cả / 3 company_id | length=100 | datatables |
| 18 | erp | GET | `admin/inventory/discrepancy/searchData` | `warehouse.xu_ly_thua_thieu_nhap_kho.view` | có | type=employee: 4/3 company_id/created_by | length=100 type=employee | datatables |
| 19 | erp | GET | `admin/warehouse/inventory_exports` | `warehouse.phieu_xuat_hang_dieu_chinh_kiem_ke.view` | có | cờ blade | — | html |
| 20 | erp | GET | `admin/warehouse/inventory_exports/searchData` | `warehouse.phieu_xuat_hang_dieu_chinh_kiem_ke.view` | không | (searchByFilter không chuỗi phạm vi — lọc theo cờ FE) | length=100 type=all | datatables |
| 21 | erp | GET | `admin/warehouse/inventory_exports/{id}/show` | `warehouse.phieu_xuat_hang_dieu_chinh_kiem_ke.view` | có | canView chuỗi | — | detail (7 id) |
| 22 | erp | GET | `admin/warehouse/inventory_imports` | `warehouse.phieu_nhap_kho_dieu_chinh_kiem_ke.view` | có | cờ blade | — | html |
| 23 | erp | GET | `admin/warehouse/inventory_imports/searchData` | `warehouse.phieu_nhap_hang_dieu_chinh_kiem_ke.view` | không | (xem ghi chú) | length=100 type=all | datatables |
| 24 | erp | GET | `admin/warehouse/inventory_imports/{id}/show` | `warehouse.phieu_nhap_hang_dieu_chinh_kiem_ke.view` | có | canView chuỗi | — | detail (7 id) |
| 25 | erp | GET | `admin/warehouse/warehouse_inventory_imports` | `warehouse.phieu_nhap_kho_dieu_chinh_kiem_ke.view` | có | cờ blade | — | html |
| 26 | erp | GET | `admin/warehouse/warehouse_inventory_imports/searchData` | `warehouse.phieu_nhap_kho_dieu_chinh_kiem_ke.view` | không |  | length=100 type=all | datatables |
| 27 | erp | GET | `admin/warehouse/position_inventories` | `warehouse.tong_kiem_ke_kho_theo_vi_tri.view` | có | cờ blade | — | html |
| 28 | erp | GET | `admin/warehouse/position_inventories/searchData` | `warehouse.tong_kiem_ke_kho_theo_vi_tri.view` | không |  | length=100 type=all | datatables |
| 29 | erp | GET | `admin/warehouse/position_inventory_results` | `warehouse.phieu_kiem_ke_vi_tri.view` | có | cờ blade | — | html |
| 30 | erp | GET | `admin/warehouse/position_inventory_results/searchData` | `warehouse.phieu_kiem_ke_vi_tri.view` | không |  | length=100 type=all | datatables |
| 31 | erp | GET | `admin/warehouse/self_inventories` | `warehouse.phieu_kiem_ke_hang_hoa.view` | có | cờ blade | — | html |
| 32 | erp | GET | `admin/warehouse/self_inventories/searchData` | `warehouse.phieu_kiem_ke_hang_hoa.view` | không |  | length=100 type=all | datatables |
| 33 | erp | GET | `admin/warehouse/position_transfers/searchData` | `warehouse.dieu_chuyen_vi_tri.view` | không |  | length=100 type=all | datatables |
| 34 | erp | GET | `admin/warehouse/warehouse_reports/holdDetail` | `warehouse.bao_cao_hang_gui.view` | có | cờ is_all_company/is_company/is_department | — | html |
| 35 | erp | GET | `admin/warehouse/warehouse_reports/holdDetailSearchData` | `warehouse.bao_cao_hang_gui.view` | có | 4 tất cả / 3 company_id / 2 department (employee_id ∈ phòng) | per_page=100 date_from=2026-01-01 date_to=2026-10-31 | auto |
| 36 | erp | GET | `admin/warehouse/warehouse_reports/holdDetailLogSearchData` | `warehouse.bao_cao_hang_gui.view` | có | như trên (drill-down 1 KH×NV×hàng: 5509×184×11169) | per_page=100 date_from=2020-01-01 date_to=2026-10-31 customer_id=5509 employee_id=184 product_id=11169 | auto |
| 37 | erp | GET | `admin/warehouse/warehouse_reports/changeSummaryReport` | `warehouse.bao_cao_ton_kho.view` | có | trang: chặn nếu không Xem báo cáo tồn kho; danh sách công ty (4 tất cả / còn lại công ty mình) + kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies,acc_warehouses,acc_com_warehouses |
| 38 | erp | GET | `admin/warehouse/warehouse_reports/stockCardDetail` | `warehouse.bao_cao_ton_kho.view` | có | trang: chặn nếu không Xem báo cáo tồn kho; danh sách công ty (4 tất cả / còn lại công ty mình) + kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies,acc_warehouses,acc_com_warehouses |
| 39 | erp | GET | `admin/warehouse/warehouse_reports/stockGeneralProduct` | `warehouse.bao_cao_ton_kho.view` | có | trang: chặn nếu không Xem báo cáo tồn kho; danh sách công ty (4 tất cả / còn lại công ty mình) + kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies,acc_warehouses,acc_com_warehouses |
| 40 | erp | GET | `admin/warehouse/warehouse_reports/stockWareshouseProduct` | `warehouse.bao_cao_ton_kho.view` | có | trang: chặn nếu không Xem báo cáo tồn kho; danh sách công ty (4 tất cả / còn lại công ty mình) + kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies,acc_warehouses,acc_com_warehouses |
| 41 | erp | GET | `admin/warehouse/warehouse_reports/stockLocationProduct` | `warehouse.bao_cao_ton_kho.view` | có | trang: chặn nếu không Xem báo cáo tồn kho; danh sách công ty (4 tất cả / còn lại công ty mình) + kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies,acc_warehouses,acc_com_warehouses |
| 42 | erp | GET | `admin/warehouse/warehouse_reports/stockCard` | `warehouse.bao_cao_ton_kho.view` | có | route Thủ kho; kho getForSelectCompanies | — | html vars=all_warehouses,$scope.companies |
| 43 | erp | GET | `admin/arrange_deliveries/reportArrangeGoodBySupplierSearchData` | `warehouse.bao_cao_boc_xep.view` | có | 4 tất cả / 3 p_ep/p_ip.company_id / còn lại created_by | per_page=100 startDate=2026-09-01 endDate=2026-10-31 | auto |
| 44 | erp | GET | `admin/arrange_deliveries/reportArrangeGoodByEmployeeSearchData` | `warehouse.bao_cao_boc_xep.view` | có | 4/3 company_id | per_page=100 startDate=2026-09-01 endDate=2026-10-31 | auto |
| 45 | erp | GET | `admin/arrange_deliveries/reportArrangeGoodByEmployeeDetailSearchData` | `warehouse.bao_cao_boc_xep.view` | có | 4/3 company_id | per_page=100 startDate=2026-09-01 endDate=2026-10-31 | auto |
| 46 | erp | GET | `admin/reports/detailTripReport` | `warehouse.bao_cao_van_chuyen.view` | có | cờ permissions is_all_company/is_company/is_department | — | html |
| 47 | erp | GET | `admin/reports/detailTripReportSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | 4 tất cả / 3 company_id | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 48 | erp | GET | `admin/reports/transportByStaff` | `warehouse.bao_cao_van_chuyen.view` | có | cờ permissions | — | html |
| 49 | erp | GET | `admin/reports/transportByStaffSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | 4/3 company_id (phòng/nhân viên) | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 50 | erp | GET | `admin/reports/transportByDriverSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | getAccountDetail: 4/3 company_id | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 51 | erp | GET | `admin/reports/detailTransportByDriverSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | getAccountDetail | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 52 | erp | GET | `admin/reports/detailEffectiveByDriverSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | 4/3 company_id | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 53 | erp | GET | `admin/reports/detailEffectiveTransportByDriverSearchData` | `warehouse.bao_cao_van_chuyen.view` | có | 4/3 company_id | per_page=100 from_date=01/01/2026 to_date=31/10/2026 | auto |
| 54 | erp | GET | `admin/warehouse/warehouses/searchData` | `warehouse.kho.manage` | không | route checkPermission:Quản lý kho | length=100 | datatables |
| 55 | api | GET | `finance/position-transfers` | `warehouse.dieu_chuyen_vi_tri.view` | có | scopedQuery: 4 tất cả / 3 company_id ∪ created_by / theo kho warehouse_id ∪ created_by / còn lại created_by | per_page=100 | auto |
| 56 | api | GET | `finance/position-transfers/{id}` | `warehouse.dieu_chuyen_vi_tri.view` | có | canView | — | detail (10 id) |
| 57 | api | GET | `finance/position-inventory-results` | `warehouse.phieu_kiem_ke_vi_tri.view` | có | scopedQuery: 4 / 3 company_id ∪ created_by / created_by; status≠DANG_TAO ∪ tôi | per_page=100 | auto |
| 58 | api | GET | `finance/position-inventories` | `warehouse.tong_kiem_ke_kho_theo_vi_tri.view` | có | scopedQuery (Xem kế hoạch kiểm kê theo vị trí …) | per_page=100 | auto |
| 59 | api | GET | `finance/position-inventories/{id}` | `warehouse.tong_kiem_ke_kho_theo_vi_tri.view` | có | canView | — | detail (13 id) |
| 60 | api | GET | `finance/self-inventories` | `warehouse.phieu_kiem_ke_hang_hoa.view` | có | scopedQuery type=all: 4 / 3 company_id ∪ created_by / created_by | per_page=100 type=all | auto |
| 61 | api | GET | `finance/self-inventories/{id}` | `warehouse.phieu_kiem_ke_hang_hoa.view` | có | canView | — | detail (7 id) |
| 62 | api | GET | `finance/warehouse-inventory-imports` | `warehouse.phieu_nhap_kho_dieu_chinh_kiem_ke.view` | có | scopedQuery: 4 / 3 company_id / Kế toán kho / created_by | per_page=100 | auto |
| 63 | api | GET | `finance/warehouse-inventory-imports/{id}` | `warehouse.phieu_nhap_kho_dieu_chinh_kiem_ke.view` | có | canView | — | detail (7 id) |
| 64 | api | GET | `finance/exc-shortage-imports` | `warehouse.xu_ly_thua_thieu_nhap_kho.view` | có | scopedQuery: 4 / 3 company_id / created_by | per_page=100 | auto |
| 65 | api | GET | `finance/exc-shortage-imports/{id}` | `warehouse.xu_ly_thua_thieu_nhap_kho.view` | có | canView | — | detail (8 id) |
| 66 | api | GET | `finance/inventory-audit-reports` | `warehouse.bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.view` | có | scopedQuery 4/3 (bảng rỗng trên rehearsal) | per_page=100 | auto |
| 67 | api | GET | `finance/stock-card/options` | `warehouse.bao_cao_ton_kho.view` | có | kho/công ty cho dropdown: 4 tất cả / Thủ kho kho mình | — | lists |
| 68 | api | GET | `finance/stock-general-product/options` | `warehouse.bao_cao_ton_kho.view` | có | WarehouseStockReportService: 4 / 3 company / theo kho | — | lists |
| 69 | api | GET | `finance/stock-detail-by-product/options` | `warehouse.bao_cao_ton_kho.view` | có | như trên | — | lists |
| 70 | api | GET | `finance/transport-cost-by-staff/meta` | `warehouse.bao_cao_van_chuyen.view` | có | cờ + danh sách công ty/phòng theo phạm vi | — | lists |
| 71 | api | GET | `finance/transport-cost-by-staff` | `warehouse.bao_cao_van_chuyen.view` | có | 4/3/2 theo tên (chi phí VC theo NVKD + báo cáo VC) | date_from=2026-01-01 date_to=2026-10-31 per_page=100 | auto |
| 72 | api | GET | `finance/beginning-stocks` | `warehouse.ton_kho_dau_ky.manage` | không | route checkPermission:Khai báo tồn kho đầu kỳ | per_page=100 | auto |

## Tài khoản (rehearsal, công ty 1, employee_infos.company_role NULL/=1 ⇒ ERP và HRM cùng công ty)

- `pv4` = employee 13 — namdangit — cả 20 mã kho có phạm vi ở mức 4 (Tổng công ty), công ty 1
- `pv3` = employee 207 — hantt.kthn — 11 mã kho có phạm vi ở mức 3 (Công ty), không mức 4, công ty 1
- `pv2` = employee 337 — duyentt.ktcnhn — bao_cao_hang_gui.view mức 2 (Phòng ban); các mã khác mức 3, công ty 1
- `pv2b` = employee 311 — thombt.khohn — chuyen_xe.view mức 2; hang_gui/phieu_xuat_kho mức 3, công ty 1 (bổ sung)
- `khong_ma` = employee 144 — huyentt.nshn — không có mã warehouse.* nào (vẫn có 401 quyền khác), công ty 1

Phạm vi từng tài khoản trên 20 mã kho có phạm vi (công ty 1; trống = không có mã):

| mã (warehouse.*.view) | pv4 (13) | pv3 (207) | pv2 (337) | pv2b (311) | khong_ma (144) |
|---|---|---|---|---|---|
| bao_cao_boc_xep | 4 | 3 | 3 | 3 | |
| bao_cao_hang_gui | 4 | 3 | **2** | 3 | |
| bao_cao_ton_kho | 4 | 3 | 3 | | |
| bao_cao_van_chuyen | 4 | 3 | 3 | 3 | |
| bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke | 4 | | | | |
| chuyen_xe | 4 | 3 | | **2** | |
| de_nghi_thanh_toan_van_chuyen | 4 | | | 3 | |
| dieu_chuyen_vi_tri | 4 | 3 | | | |
| khai_bao_ton_kho_vat_ly | 4 | | | 3 | |
| phieu_hach_toan_van_chuyen | 4 | 3 | | 3 | |
| phieu_kiem_ke_hang_hoa | 4 | 3 | 3 | 3 | |
| phieu_kiem_ke_vi_tri | 4 | | 3 | 3 | |
| phieu_nhap_hang_dieu_chinh_kiem_ke | 4 | 3 | | 3 | |
| phieu_nhap_kho_dieu_chinh_kiem_ke | 4 | | | 3 | |
| phieu_xuat_hang_dieu_chinh_kiem_ke | 4 | 3 | | 3 | |
| phieu_xuat_kho_dieu_chinh_kiem_ke | 4 | | | 3 | |
| phieu_xuat_kho | 4 | 3 | 3 | 3 | |
| tong_hop_gia_van_chuyen_de_xuat | 4 | | | | |
| tong_kiem_ke_kho_theo_vi_tri | 4 | | | 3 | |
| xu_ly_thua_thieu_nhap_kho | 4 | | | | |

Ca thiếu:
- **Phạm vi 1 (Bộ phận)**: Catalog warehouse không có mã nào cho phép scope 1 (`scopes` tối đa [2,3,4]) ⇒ không tồn tại.
- **Có mã nhưng phạm vi NULL**: rehearsal có 0 dòng `role_has_permissions.scope IS NULL` cho mã có phạm vi (toàn hệ thống, không riêng kho) ⇒ không có người thật. Ca U8 "có mã không phạm vi chỉ thấy phiếu mình" chỉ kiểm được bằng test BE (7b).
- Phạm vi 2 chỉ có ở 2 mã: `bao_cao_hang_gui` (12 người, chọn 337) và `chuyen_xe` (4 người, chọn 311). `phieu_xuat_kho`, `tong_hop_gia_van_chuyen_de_xuat`, `de_nghi_thanh_toan_van_chuyen` cho phép 2 nhưng không ai đang giữ mức 2.
- Khác công ty: cả 5 tài khoản ở công ty 1; không đổi công ty đang làm việc trên DB.

## Không chụp (ghi rõ lý do)

- Bản **xuất Excel / in danh sách** (`exportList`, `printList`, `*Export`, `*Print`, `export-rows`, `print-list-data`) — dùng lại đúng query của searchData/index đã chụp; trả xlsx/HTML in.
- ERP các nơi gọi `WarehouseExport::searchByFilter` / `DeliveryTrip::searchByFilter` với `type` khác `all` (không vào nhánh phạm vi): `product_exports`, `product_imports`, `warehouse_reimports`, `borrow_sells`, `employee_delivery_payments`, `warehouse_imports/searchData`, `modal_data/searchWarehouseExportAndImport`, `other_delivery_payment_requests/searchData`.
- ERP báo cáo kho chỉ gác `checkPermission:Thủ kho|Kế toán kho` (không chuỗi phạm vi): `multiWarehouseReport*`, `stockCardSearchData`, `accounting*`, `saleReport*`, `orderImportReport*`, `inventoryByLocationReport*`, `stockOfProductReport*`, `warehouseReport*` … (giữ 1 mẫu `warehouses/searchData`).
- ERP `*SearchData` dữ liệu của các báo cáo tồn kho (stockGeneralProduct…): phạm vi chỉ quyết định danh sách công ty/kho ở trang (đã chụp qua biến JS trang), searchData lọc theo kho người dùng chọn.
- hrm-api: `filter-options`, `form-options`, `histories`, `print-data`, `self-inventory-requests(-alls)`, `stock-card` / `stock-general-product` / `stock-detail-by-product` index (cần chọn kho + ngày; phạm vi nằm ở `/options` đã chụp).
- hrm-client `pages/finance/warehouse-exports` gọi `GET assign/warehouse-exports` — **route này không tồn tại trên hrm-api nhánh rbac** (chỉ có `assign/warehouse-exports/{id}/product-export-data`) ⇒ không chụp được; hit scope_chain duy nhất của client nằm ở màn này.

## Scanner sót (báo cho 7b)

hrm-api lọc phạm vi kho qua **hằng** trong Entity/Service, `permission:scan` chỉ bắt chuỗi trong lời gọi kiểm ⇒ scan-wh-0 ghi api scope_chain = 0 nhưng thực tế có: `PositionTransfer`, `PositionInventoryResult`, `PositionInventory`, `SelfInventory`, `WarehouseInventoryImport`, `ExcShortageWarehouseImport`, `InventoryAuditReport` (`PERMISSION_VIEW_ALL_COMPANY/COMPANY/WAREHOUSE` + `scopedQuery()/canView()`), `WarehouseStockReportService`, `StockCardReportService`, `TransportCostByStaffReportService` (mảng tên). ERP `InventoryExport/InventoryImport…::searchByFilter` dùng `$permissions['is_all_company']` (tên lấy từ mảng) — cũng ngoài tầm scanner.

