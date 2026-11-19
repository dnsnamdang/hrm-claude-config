# Recon: port "Báo cáo theo dõi thực hiện hợp đồng" ERP → HRM (+ nguồn `hrm_contracts`)

Ngày: 2026-11-10. Chỉ đọc, không sửa code. DB kiểm: `erp_hrm_check` (local).

Ký hiệu: `SVC` = `ERP/TanPhatDev/app/Services/Reports/MonitorContractImplementService.php`,
`RC` = `ERP/TanPhatDev/app/Http/Controllers/ReportController.php`,
`VIEW` = `ERP/TanPhatDev/resources/views/reports/monitor_contract_implement.blade.php`.

Bảng tài khoản (đã tra DB): 22 = **1311**; 181..187 = **511x** (511,5111,5112,5113,5114,5117,5118); 190 = **5211** (CK thương mại); 191 = **5212** (hàng bán trả lại); 192 = **5213** (giảm giá). `account_details.type`: 1 = Nợ, 2 = Có. Work CKHH = id 20 (CKDV không có trên DB local → `Work::getByCode()` chỉ trả CKHH).

---

## 1. Hành vi ERP

### 1.1 Route / controller / phân trang
- Route `routes/web.php:3444-3447` (prefix `reports`): page / `searchData` / `print` / `export`. **Không gate** ở page (RC:5864) — không có quyền thì vẫn vào, phạm vi rơi về "của mình".
- Quyền: `permissionScope('sale.bao_cao_theo_doi_thuc_hien_hop_dong.view')` → 4 cờ `is_all_company (≥GROUP=4) / is_company (≥3) / is_department (≥2) / is_part (≥1)` (RC:5866-5872, lặp lại ở cả 3 action còn lại).
- `searchData` (RC:5876-5911): `getData()` lấy **toàn bộ** dòng HĐ (collection phẳng, mỗi dòng = 1 HĐ gốc), `summary` = SUM toàn bộ collection (9 trường), rồi `LengthAwarePaginator(forPage(current_page, per_page))` **phân trang theo HĐ**, sau đó mới `render()` nhóm phòng → NV → HĐ trên **riêng trang đó**. Hệ quả: dòng tổng phòng/NV chỉ là tổng của các HĐ trên trang hiện tại; dòng TỔNG CỘNG là toàn bộ. FE `per_page = 30` (VIEW:290).
- Print (RC:5913-5960): đổi `date_from/date_to` từ `d/m/Y` → `Y-m-d`, cùng logic, FE gửi `per_page=999999999999999999` (VIEW:428) → 1 trang; nhúng `getTable($json)` vào `ReportTemplate::BAO_CAO_THEO_DOI_THUC_HIEN_HOP_DONG`, view `print_landscape`. Có `HEADER` công ty người đăng nhập, `TU_NGAY/DEN_NGAY`.
- Export (RC:5962-6005): như print, `getTable($json, 'export')` → `RevenueStandardServiceReportExcel` file `bao_cao_theo_doi_thuc_hien_hop_dong.xlsx`, `COLSPAN=12`, `count_data` = số dòng phòng+NV+HĐ.
- Khác biệt print vs export (`SVC:1115-1275`): print dùng `formatCurrency()`, export ghi số thô; **export để TRỐNG cột Tỉnh và Hãng ở dòng HĐ** (SVC:1196-1197), print có (SVC:1184-1185). Dòng phòng: 2 ô tỉnh/hãng trống ở cả hai; dòng NV: "N tỉnh" / "N hãng xe".
- FE (VIEW:320-333): bắt buộc `date_from` + `date_to` **trừ khi có `contract_code`**. Nhưng BE luôn `whereDate(... date_from)` → nhập chỉ mã HĐ thì gửi `"Invalid date"` (bug ERP; print/export còn nổ `Carbon::createFromFormat`).
- Link HĐ: firm → `/admin/sale/firm-contracts/{id}`, wr → `/admin/customer-care/warranty_repair_contracts/{id}/show` (VIEW:404-407).

### 1.2 Bộ lọc (`filter()` SVC:910-956, áp vào **mọi** subquery với prefix bảng HĐ của subquery đó)
| Bộ lọc | Cột |
|---|---|
| `company_id` (ô chọn chung `partials.common.company-department-filter-singer`) | `{p}.company_id =` |
| `department_id` | `{p}.department_id =` |
| `part_id` | `{p}.part_id =` |
| `employee_id` | `{p}.created_by =` (NV = **người lập HĐ**) |
| `customer_id` | `{p}.customer_id =` |
| `contract_code` | `{p}.code =` (khớp **chính xác**, không LIKE; với PLBS thì so mã PLBS, không phải mã HĐ gốc) |
| `date_from`/`date_to` | không ở filter(), dùng riêng trong từng subquery (xem từng cột) |
| `province_id[]` (multi) | sau cùng: `provinces.id IN` (tỉnh của địa điểm giao trên **báo giá**) SVC:381-383 / 901-903 |
| `vehicle_manufacts_id[]` (multi) | `vm.id IN` (hãng xe gắn với **khách hàng**) SVC:384-386 / 904-906 |

Phạm vi quyền (filter() SVC:912-935), mọi nhánh đều `OR {p}.created_by = me`:
- GROUP: không lọc.
- COMPANY: `{p}.company_id = user.info.company_id`.
- DEPARTMENT: `{p}.department_id IN employee_manage_departments(employee_id=me, company_id=user company)`.
- PART: `{p}.part_id = user.info.part_id` (bộ phận của mình, không phải bộ phận quản lý).
- Không quyền: `{p}.created_by = me`.

### 1.3 HĐ nào được lên báo cáo
**Firm (`firm_contracts`)**, SVC:36-116:
1. Tập id gốc `$firm_ids` = các HĐ có **bất kỳ** dòng `account_details` TK 1311 (`account_id=22`) có `invoiceable_date_accounting` trong kỳ (whereIn invoiceable_type bị comment SVC:47) và `firm.type NOT IN (3,6,10,7,9)`, `firm.created_at > 2023-07-01`, qua filter(). `havingRaw(income_money>0)` bị comment → kể cả phát sinh 0.
2. Dòng chi tiết: `firm.id IN ids OR firm.parent_contract_id IN ids` (kéo cả PLBS con), cùng loại trừ type & ngày.
   - Type (FirmContract.php:62-72): 1 HĐ, 2 PL bổ sung, 3 PL giảm, 4 HĐ dự án, 5 HĐDA PLBS, 6 HĐDA PLG, 7 HĐ nguyên tắc, 8 Đơn hàng nguyên tắc, 9 HĐNT PLBS, 10 ĐHNT PLG. → Lên báo cáo: **1, 2, 4, 5, 8**. HĐ nguyên tắc (7) và PLBS của nó (9) bị loại hẳn.
   - Gộp về HĐ cha: `COALESCE(firm1.id, firm.id)` với join `firm1.id = firm.parent_contract_id AND firm.type != 8` (SVC:119-121) → PLBS (2,5) gộp vào dòng HĐ cha; **ĐHNT (8) KHÔNG gộp vào HĐNT cha**, đứng thành dòng riêng (mã/ báo giá của chính ĐHNT).
   - **Không có điều kiện trạng thái** (status) nào cho HĐ gốc.
3. `GROUP BY parent_contract_id`, `ORDER BY department_id, created_by` (SVC:380).

**WR (`wr_service_contracts`)**, SVC:390-515: tương tự — id có dòng 1311 trong kỳ, `wr.type != 4` (4 = PL giảm; 1 HĐ, 2 Bảo hành, 3 PLBS đều lên), `created_at > 2023-07-01`; gộp `COALESCE(wr.parent_id, wr.id)`; không lọc status.

### 1.4 Công thức từng cột (dòng HĐ)
| Cột | Trường | Firm | WR |
|---|---|---|---|
| Hợp đồng | `contract_code` | mã HĐ cha (`COALESCE(firm1.code, firm.code)`) SVC:62 | `COALESCE(_wr.code, wr.code)` SVC:414 |
| Khách hàng | `customer_code - customer_name` | `customers` theo `firm.customer_id` (getData SVC:979) | như firm |
| Tỉnh/TP | `province_name` | `firm_quotations.delivery_place_id → delivery_places.province_id → provinces` (báo giá của HĐ cha) SVC:377-379 | `wr_service_quotations.delivery_place_id → …` SVC:897-899 |
| Hãng | `vehicle_manufacts` | **hãng xe của KHÁCH HÀNG**: `customer_has_vehicle_manufacts → vehicle_manufacts.name` (KHÔNG phải brand hàng hoá) SVC:375-376 | như firm SVC:895-896 |
| Giá trị HĐ | `total_after_vat` | `SUM_theo_cha( firm.total_after_vat − Σ PL giảm/annex (type IN 3,6,10,7,9, status=3) có parent = firm.id )` SVC:72, 289-306, 370. Không lọc kỳ. | `wr.total_after_vat − Σ PL giảm (type 4, status 3)` SVC:424, 814-829 |
| DS thực xuất – **Theo HĐ** | `revenue_contract` | Sổ cái theo `invoiceable_date_accounting` trong kỳ, contractable = HĐ: `Σ(Có−Nợ) TK 511x(181-187)+5212(191)+5213(192)` `+ Σ(Có−Nợ) TK 5211(190) với work_id ∈ {CKHH, CKDV}` (SVC:331-352). Không giới hạn invoiceable_type. | Cùng công thức nhưng **chỉ** invoiceable_type ∈ {DeclareDebtBeginning, BillAdjustDept, BillIncome, BillIncomeReport, WrAccountingService} (SVC:861) — tức KHÔNG tính doanh thu từ PXK/BorrowSell của HĐ DV. |
| DS thực xuất – **Tiêu chuẩn** | `standard_amount_export` | Theo `created_at` phiếu trong kỳ: `export(PXK type 14, status 1: Σ ped.qty × fctp.standard_price, khớp fctp theo (pe.firm_contract_id, ped.product_id))` + `borrow(borrow_sells status 1: Σ bsp.qty × fctp.standard_price qua objectable=FirmContractTabProduct)` + `sac_sub(service_accounting trong kỳ: Σ fcc.standard_price với revenue_calculation=1, khớp cost_id)` − `import(PNK type 4,9 status 1: Σ pid.qty × fctp.standard_price)` (SVC:74, 146-288) **+ chi phí dự phòng + LEAST(định mức giảm giá còn lại, 0)** (SVC:372) | `export(PXK type 17)` + `borrow` − `import(type 4,9 qua YCNH→ĐNXK detail)` + `export_work/service/extend_service` (dòng HĐ có phiếu hạch toán DV `wr_accounting_services` status 1 trong kỳ: Σ assign_qty × standard_price) SVC:426, 623-797; + dự phòng + LEAST(quota,0) SVC:892 |
| Số tiền thực thu trong kỳ | `income_money` | 1311 trong kỳ (accounting date): `Σ Có (DeclareDebtBeginning, BillAdjustDept, BillIncome, BillIncomeReport) − Σ Nợ (BillPayment, BillPaymentAuthorization)` SVC:37-56 | **chỉ** `Σ Có` 4 loại đó, KHÔNG trừ BillPayment (SVC:394) — bất đối xứng với firm |
| Tổng DSTC HĐ – **Tiêu chuẩn** | `standard_amount` | Toàn HĐ (không theo kỳ): `Σ fctp.root_quantity × standard_price` + `Σ firm_contract_costs.standard_price (revenue_calculation=1)` SVC:73,122-145,230-257 + dự phòng + LEAST(quota,0) (SVC:371) | `wr_service_contract_products (engineering_work_qty) + product_services (quantity) + items (qty) + extend_product_services (quantity)` × standard_price SVC:425,520-622 + dự phòng + LEAST(quota,0) |
| Tổng DSTC HĐ – **Thực xuất** | `standard_amount_exported` | Cùng nguồn nhưng dùng `fctp.exported_qty` và `fcc.exported=1` (cột tally lũy kế, không theo kỳ) SVC:75 | `assign_qty`/`exported_qty` SVC:427 |
| Công nợ – Phải thu | `income` | 1311 **toàn thời gian, không lọc kỳ** (SVC:310-330): `Σ Nợ (ProductExport, BorrowSell, WrAccountingService, ServiceAccounting, DeclareDebtBeginning, LiquidationRecord, BillAdjustDept) − Σ Có (ProductExport, BorrowSell, WrAccountingService, ServiceAccounting, LiquidationRecord)` | Như firm, nhưng chuỗi `'…ServiceAccountingApp\\Model\\Sale\\ServiceAccounting'` gõ dính (SVC:836) → **không trừ Có ServiceAccounting** |
| Công nợ – Đã thu | `incomed` | 1311 toàn thời gian: `Σ Có (BillIncome, BillIncomeReport, DeclareDebtBeginning, BillAdjustDept) − Σ Nợ (BillPayment, BillPaymentAuthorization)` SVC:316-317 | như firm SVC:837-838 |
| Công nợ – Còn nợ | `income_remain` | `income − incomed` (getData SVC:971) | như firm |

Phần cộng thêm vào 3 cột DSTC (SVC:77-109, 371-373; WR 429-508, 891-893):
- **Chi phí dự phòng** firm = `fsa.redundancy_cost / (fsa.before_vat_product + fsa.before_vat_repair_service) × before_vat(phần tương ứng)` (`firm_support_accounting`); WR = `wrsa.contingency_expense_percent × before_vat` (`wr_support_accounting`).
- **Định mức giảm giá còn lại** = định mức (qty × price × sale_max_percent) − giảm giá − `market_costs_percent × before_vat`; **chỉ áp HĐ tạo trước 2025-11-01**, sau ngày đó = 0; chỉ lấy phần âm (`LEAST(x,0)`).

Cấp phòng / NV (`render()` SVC:987-1106): nhóm theo `result.department_id` (phòng **của HĐ**), rồi `employee_id = created_by` (**người lập HĐ**). Dòng không có `department_id` bị **bỏ** khỏi bảng nhưng vẫn nằm trong `summary`. Mỗi cấp cộng 9 trường; đếm số tỉnh / số hãng xe khác nhau (`province_no`, `vehicle_no`). Thứ tự = thứ tự SQL (department_id, created_by), không sắp theo tên.

### 1.5 Lỗi/điểm lạ của ERP cần quyết khi port (không bê mù)
1. `GROUP BY parent_contract_id` nhưng `revenue_contract`, `income_money`, `income`, `incomed` **không SUM** (SVC:363-366, 883-886) → khi HĐ cha có PLBS, MySQL lấy giá trị của 1 dòng bất kỳ (strict=false ở cả 2 dự án nên không nổ). Các số sổ cái của PLBS (nếu ghi contractable = PLBS) có thể rơi mất.
2. Join `customer_has_vehicle_manufacts` 1-n ngay trước `SUM(...)` → KH có >1 hãng xe làm **nhân bản** total_after_vat / DSTC; DB local có **71 KH** như vậy. Cột Hãng chỉ hiện 1 hãng.
3. WR: thực thu không trừ chi; doanh thu Theo HĐ chỉ đếm 5 loại chứng từ; typo ServiceAccounting.
4. Công nợ (3 cột) là **lũy kế toàn thời gian** (không có cả mốc `date_to`), trong khi các cột khác theo kỳ.
5. Lọc chỉ mã HĐ (không ngày) bị hỏng; `contract_code` khớp chính xác.
6. Subtotal phòng/NV chỉ theo trang.

---

## 2. Tương đương cho `hrm_contracts` (morph `Modules\Assign\Entities\Contract\Contract`)

Bối cảnh mô hình HRM (`HRM/hrm-api/Modules/Assign/Entities/Contract/Contract.php`):
- Bảng `hrm_contracts` có `code, status, customer_id (bảng customers chung), quotation_id (bảng quotations HRM), company_id, department_id, part_id, created_by, total_after_vat, sign_date, effective_date, created_at`. **Không có `type`, không có `parent_contract_id`** → không có khái niệm PLBS/PL giảm/HĐ nguyên tắc/ĐHNT.
- Trạng thái (Contract.php:19-43): 3 Đang tạo, 2 Chờ TP duyệt, 14 Chờ pháp chế, 15 Chờ BGĐ, 16 Chờ KH ký, 17 KH đã ký, 6 Có hiệu lực, 19 Đang thực hiện, 18 Đóng, 20 Hết hiệu lực, 21 Gia hạn chờ duyệt, 22 Chờ quyết toán, 12 Đang QT, 11 Đã QT, 10 Đã thanh lý, 13 Không duyệt; 1/7/8/9 là mã cũ. Xuất hàng được khi 6 hoặc 19 (`EXPORTABLE_STATUSES`).
- Dòng hàng `hrm_contract_product_prices` (cha/con qua `parent_id`, `erp_product_id`, `qty_needed`, `exported_qty`, `returned_qty`, `quoted_price`, `unit_price_after_discount`, `sale_max_percent`, **`standard_price`**, `brand_id`, `net_price`, `cost_price`).
- Dịch vụ `hrm_contract_service_items` (`cost_id`, `qty`, `quoted_price`, `unit_price_after_discount`…) — **không có `standard_price`, không có `revenue_calculation`/`exported`**.
- HTHT: `firm_support_accounting` dùng chung, `contractable_type = Modules\Assign\Entities\Contract\Contract` (SupportAccounting.php:14; Contract::support_accounting morphOne :354).
- Xuất bán HĐ HRM: `product_exports.type = 21` (XUAT_BAN_HOP_DONG, hàng cha) và `20` (XUAT_SAN_XUAT_HOP_DONG, hàng con khi cha thiếu tồn), gắn qua `product_exports.emplement_contract_type/emplement_contract_id` (ProductExport.php:120-142 `scopeForHrmContract`). YCXH dòng `product_export_request_tab_products.contract_product_id → hrm_contract_product_prices.id`.
- Hạch toán xuất (ProductExportPostingService.php:60-160): loại 21/20… rơi nhánh else → `account_details.contractable_type = CONTRACTABLE_HRM_CONTRACT`, `invoiceable_type = 'App\Model\Warehouse\ProductExport'` (cùng chuỗi ERP); bút toán loại 21 có Nợ 1311/Có 5111+33311, Nợ 5211 (work_id = CKHH 20)/Có 1311, Nợ 5213/Có 1311 (:549-571) → **khớp công thức `revenue_contract` của ERP**.
- Nhập trả lại: `product_imports.emplement_contract_type/id` (type 4 thấy trên DB), hạch toán `contractable = HĐ HRM` (ProductImportAccountingService.php:446).
- Bán mượn: `borrow_sells.contractable_type = HĐ HRM`, `borrow_sell_products.objectable_type = Modules\Assign\Entities\Contract\ContractProductPrice` → BorrowSellService.php:54, 399 tăng `hrm_contract_product_prices.exported_qty`.
- Thu tiền: phiếu thu chọn được `hrm_contracts` (BillIncomeRequestService.php:447-498), hạch toán `contractable_type = detail.objectable_type` (BillIncomeAccountingService.php:145) → 1311 Có với contractable HĐ HRM. Bù trừ công nợ cũng chọn được hrm_contracts (BillAdjustDeptPickerService.php:375). `CustomerDebtAggregator::contractTables()` (:217) đã map class HRM → `hrm_contracts` (FinanceServiceProvider cố ý không map morph).
- Dịch vụ: `HrmContractServiceAccountingSource` (Modules/Finance/Services/ServiceAccounting/) cho phiếu hạch toán dịch vụ trên HĐ HRM (`service_accounting.contractable_type = HĐ HRM`).

Kiểm DB local (`erp_hrm_check`):
- `hrm_contracts`: **2 dòng** (id 13 status 1, id 15 status 6), tạo 08/2026.
- `hrm_contract_product_prices`: 8 dòng, 3 có `standard_price>0` (chỉ HĐ 15), **0 dòng `exported_qty>0`** dù HĐ 15 đã có PXH type 21 hoàn tất (PXH-34580, 3 SP) → `exported_qty` **không được cập nhật bởi luồng PXK loại 21** (chỉ bán mượn cộng).
- `hrm_contract_service_items`: 0 dòng.
- `account_details` contractable HĐ HRM: 14 dòng, toàn bộ `invoiceable_type = ProductImport` của HĐ 13 (trả lại: Có 1311 939.600, Nợ 5212 870.000). PXH-34580 chưa có bút toán (accounting_date NULL).
- `borrow_sells` contractable HĐ HRM: 0. `service_accounting` HĐ HRM: 0. `bill_income_details.objectable_type` chưa có class HRM.
- `firm_support_accounting` có 2 dòng HĐ HRM (13, 15), `market_costs_percent=0`, `redundancy_cost=0`.
→ Dữ liệu local quá mỏng để đối số; công thức phải chốt từ code, test bằng dữ liệu dựng.

### 2.1 Bảng cột ↔ nguồn HRM
| Cột | Nguồn cho `hrm_contracts` | Đánh giá |
|---|---|---|
| Tập HĐ (có 1311 trong kỳ) | `account_details` `account_id=22`, `contractable_type='Modules\\Assign\\Entities\\Contract\\Contract'`, `invoiceable_date_accounting` trong kỳ | **CÓ SẴN** |
| Lọc type / gộp cha / ĐHNT | Không có type/parent → mỗi HĐ HRM 1 dòng, không trừ phụ lục | **KHÔNG CÓ** (không cần) — nhưng cần PO xác nhận HRM chưa/không có phụ lục |
| Lọc trạng thái | ERP không lọc; HĐ HRM chưa có hiệu lực thì không có bút toán 1311 nên tự rơi | **SUY RA** — có thể thêm loại `Đang tạo/Không duyệt` cho chắc |
| Hợp đồng | `hrm_contracts.code`; link FE tới trang chi tiết HĐ HRM | **CÓ SẴN** |
| Khách hàng | `hrm_contracts.customer_id → customers` (bảng chung; còn có snapshot `customer_code/customer_name`) | **CÓ SẴN** (chọn: live `customers` như ERP hay snapshot) |
| Tỉnh/TP | `quotations` HRM **không có `delivery_place_id`** (chỉ `delivery_address` text). Lựa chọn: (a) `customers.province_id` (đã kiểm: có giá trị), (b) parse/thêm cột tỉnh giao hàng ở báo giá/HĐ, (c) để trống | **SUY RA** |
| Hãng | ERP = hãng xe của KH (`customer_has_vehicle_manufacts`) — bảng chung, dùng y được theo `customer_id`. Nếu PO hiểu "Hãng" là brand hàng thì có `hrm_contract_product_prices.brand_id` (nhiều brand/HĐ) | **CÓ SẴN** (nếu giữ nghĩa ERP); nên sửa lỗi nhân bản (GROUP_CONCAT/subquery) |
| Giá trị HĐ | `hrm_contracts.total_after_vat` (không trừ phụ lục) | **CÓ SẴN** |
| DS thực xuất – Theo HĐ | Cùng công thức sổ cái (511x+5212+5213, 5211 work CKHH/CKDV) với contractable HĐ HRM; HRM loại 21 đã ghi đúng các TK này (5211 có work_id=20) | **CÓ SẴN** (giữ biến thể firm — không giới hạn invoiceable_type) |
| DS thực xuất – Tiêu chuẩn | (1) PXK `type=21` (và có tính `20` không?), `status=1` (hoàn tất), `created_at` trong kỳ, `emplement_contract_type = HĐ HRM`: Σ `ped.qty × cpp.standard_price`. Khớp dòng: ERP khớp (HĐ, product_id) → HRM `cpp.contract_id = pe.emplement_contract_id AND cpp.erp_product_id = ped.product_id` (rủi ro trùng nếu 1 SP xuất hiện ở nhiều dòng/cha-con; đường chuẩn hơn qua `product_export_request_tab_products.contract_product_id` theo `product_export_request_id`+`product_id`). (2) Bán mượn: `borrow_sells` status 1 + `bsp.objectable_type=ContractProductPrice` → `cpp.standard_price` (**CÓ SẴN**). (3) Trả lại: `product_imports` type 4/9 status 1 `emplement_contract_*` = HĐ HRM, khớp `pid.product_id = cpp.erp_product_id` (**CÓ SẴN**, cùng rủi ro trùng). (4) Dịch vụ (`sac_sub`): HĐ HRM không có standard_price dịch vụ → 0 | **SUY RA** (hàng: chọn khoá khớp & có tính loại 20 không; dịch vụ: **KHÔNG CÓ**) |
| Số tiền thực thu trong kỳ | 1311 trong kỳ, Có (DeclareDebtBeginning, BillAdjustDept, BillIncome, BillIncomeReport) − Nợ (BillPayment, BillPaymentAuthorization), contractable HĐ HRM — phiếu thu HRM đã ghi contractable HĐ HRM | **CÓ SẴN** (theo biến thể firm) |
| Tổng DSTC – Tiêu chuẩn | `Σ cpp.qty_needed × cpp.standard_price` (dòng cha/con: standard_price của con = NULL trên mẫu → chỉ cha mang giá) + dịch vụ = 0 + dự phòng (`firm_support_accounting.redundancy_cost / (before_vat_product + before_vat_repair_service) × Σ qty × unit_price_after_discount`) ; định mức giảm giá còn lại = **0** (mọi HĐ HRM tạo sau 2025-11-01) | Hàng **CÓ SẴN**; dịch vụ **KHÔNG CÓ**; dự phòng **SUY RA** (base before_vat dùng cột nào; trên local = 0) |
| Tổng DSTC – Thực xuất | ERP dùng cột tally `exported_qty`. HRM `cpp.exported_qty` **chỉ tăng theo bán mượn**, không tăng theo PXK 21 (local: 0 dù đã xuất). Lựa chọn: (a) tính live Σ qty PXK 21 hoàn tất (toàn thời gian) − trả lại + bán mượn; (b) Σ `tab_products.qty` các YCXH chưa huỷ (như `contractRemainingByLine`, ProductExportRequestService.php:989-1043) — là "đã đề nghị" chứ không phải "đã xuất"; (c) sửa luồng xuất để cập nhật `exported_qty` | **SUY RA** |
| Công nợ – Phải thu | 1311 toàn thời gian Nợ (ProductExport, BorrowSell, ServiceAccounting, DeclareDebtBeginning, LiquidationRecord, BillAdjustDept…) − Có (ProductExport, BorrowSell, ServiceAccounting, LiquidationRecord), contractable HĐ HRM. **Lưu ý**: phiếu nhập trả lại HRM ghi Có 1311 với `invoiceable_type = ProductImport` — ERP **không đưa ProductImport vào danh sách** → hàng trả lại không giảm "Phải thu" (ERP firm cũng vậy) | **CÓ SẴN** + **SUY RA** (có thêm ProductImport không) |
| Công nợ – Đã thu | Có (BillIncome, BillIncomeReport, DeclareDebtBeginning, BillAdjustDept) − Nợ (BillPayment, BillPaymentAuthorization) | **CÓ SẴN** |
| Công nợ – Còn nợ | `income − incomed` | **CÓ SẴN** |
| Phòng / NV nhóm | `hrm_contracts.department_id` / `created_by` (+ `part_id` cho lọc) | **CÓ SẴN** |

---

## 3. HRM hiện có gì cho báo cáo này
- **Chưa có** API/route/page nào (grep `monitor`, `theo_doi_thuc_hien`, `monitor_contract` trong `hrm-api/Modules`, `hrm-api/routes`, `hrm-client/pages|components|store` → không có).
- Menu: `hrm-client/components/subsystem-menu/sale-hub.js:265` nhóm "Báo cáo → Doanh số - Doanh thu" đã có **chuỗi placeholder `'Theo dõi thực hiện hợp đồng'` chưa có link** (đổi thành `{ n: 'Theo dõi thực hiện hợp đồng', link: '/sale/…' }` như mục sales-income-summary dòng 266).
- Quyền: `hrm-api/app/Support/Permissions/Catalog/sale.php:805-821` có `sale.bao_cao_theo_doi_thuc_hien_hop_dong.view`, scopes [1,2,3,4], legacy 4 tên ERP, **`platforms => ['erp']`** → phải thêm `'hrm'` (như `accounting.bao_cao_tong_thu_nhap_tu_ban_hang.view`, accounting.php:394-402 `['erp','hrm']`) rồi chạy catalog-sync.

## 4. Mẫu port gần nhất để chép
1. **`Modules/Finance/Services/SalesIncome/*`** (`SalesIncomeReportService.php` 569 dòng, `SalesIncomeScope.php`, `SalesIncomePrintTable.php`) + `Modules/Finance/Http/Controllers/V1/SalesIncomeSummaryController.php` + route `Modules/Finance/Routes/api.php:1998-2008` (prefix `/v1/finance/sales-income-summary`: `/`, `/meta`, `/detail`, `/export`, `/export-detail`, `/print-list-data`, `/print-detail-data`; **không gate**) + client `hrm-client/pages/sale/sales-income-summary/index.vue` (+ `components/export-excel.js`, modal chi tiết). Scope: `CurrentPermission::scope(CODE)` → all/company/department/part/own; company = `auth()->user()->current_company_role` (công ty đang chọn, khác ERP `info.company_id`); department = `listManageDepartmentIds()`; part = `listManagePartIds()` + bộ phận của mình; own = NV hưởng (`ac.employee_id`). Mỗi nhánh OR "của mình".
2. Phù hợp hơn về cột "của mình" = **người lập HĐ**: `Modules/Finance/Services/CustomerDebt/CustomerDebtScope.php` (own = `contract_created_by`, áp cả dòng tổng) + `CustomerDebtAggregator::contractTables()` (đã có `hrm_contracts`), client `pages/sale/customer-debt-by-employee`. Route `Modules/Finance/Routes/api.php:1980-1985`.
→ Gợi ý: service mới `Modules/Finance/Services/MonitorContractImplement/*` với Scope bám CustomerDebtScope nhưng cột theo bảng HĐ (`{p}.company_id/department_id/part_id/created_by`), 3 nguồn union (firm / wr / hrm).

## 5. Câu hỏi cần PO chốt (xếp theo mức quan trọng)
1. **DSTC "Thực xuất" của HĐ HRM**: `hrm_contract_product_prices.exported_qty` không tăng khi PXK loại 21 hoàn tất. Tính live từ PXK 21 (− trả lại + bán mượn), hay sửa luồng xuất để ghi tally như ERP? Loại 20 (xuất SX hàng con) có tính vào DSTC không?
2. **Dịch vụ trong HĐ HRM** (`hrm_contract_service_items`) không có giá tiêu chuẩn / cờ tính doanh số → DSTC phần dịch vụ = 0 có chấp nhận không, hay cần thêm cột?
3. **Tỉnh/TP** cho HĐ HRM: báo giá HRM không có địa điểm giao dạng tỉnh → dùng tỉnh của khách hàng, hay để trống / bổ sung dữ liệu?
4. **Sửa hay giữ y lỗi ERP** khi port 2 nguồn cũ: (a) SUM không gộp sổ cái PLBS, (b) nhân bản do KH nhiều hãng xe (71 KH), (c) WR thực thu không trừ chi + typo ServiceAccounting + doanh thu WR chỉ 5 loại chứng từ, (d) subtotal phòng/NV theo trang, (e) lọc chỉ mã HĐ bị hỏng. Báo cáo HRM có buộc số khớp ERP 1:1 không?
5. **"Hãng"** giữ nghĩa ERP (hãng xe của KH) hay đổi thành thương hiệu hàng trong HĐ?
6. **Công nợ** giữ lũy kế toàn thời gian (không mốc `date_to`) như ERP, hay chặn đến `date_to`? Có trừ hàng trả lại (ProductImport Có 1311) vào "Phải thu" không?
7. HĐ HRM có lọc trạng thái (vd bỏ Đang tạo/Không duyệt/Đã thanh lý) hay chỉ dựa vào có phát sinh 1311 trong kỳ như ERP? HRM có/ sẽ có phụ lục HĐ cần trừ giá trị không?
8. Chi phí dự phòng HĐ HRM: dùng `firm_support_accounting.redundancy_cost` như firm (hiện local = 0) — đồng ý công thức firm?
9. Phạm vi công ty: theo công ty đang chọn (`current_company_role`, chuẩn HRM) hay công ty hồ sơ như ERP?
