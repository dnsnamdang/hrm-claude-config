# Báo cáo theo dõi thực hiện hợp đồng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn `/sale/monitor-contract-implement` trên HRM: báo cáo theo dõi thực hiện HĐ như ERP `reports/monitor_contract_implement`, gộp 3 nguồn HĐ hãng / HĐ dịch vụ / HĐ HRM vào 1 bảng, có In + Xuất Excel.

**Architecture:** Module `Finance`, thư mục `Services/MonitorContractImplement/`. Mỗi nguồn HĐ là 1 class trả `Query\Builder` cho ra **1 dòng / HĐ gốc** với cùng bộ cột (`RowShape`). Service union 3 nguồn, nối Tỉnh/Hãng, lọc, tính tổng + cây phòng → NV → HĐ trên toàn bộ dữ liệu, rồi cắt trang. Controller + route không gate, phạm vi qua `MonitorContractScope` (bám `SalesIncomeScope`, cột "của mình" = người lập HĐ). FE 1 trang Nuxt bám `pages/sale/sales-income-summary`.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), MySQL `erp_hrm_check`, PHPUnit, Playwright.

**Spec:** `HRM/.plans/bao-cao-theo-doi-thuc-hien-hop-dong/design.md` (duyệt 10/11/2026). Công thức ERP từng cột kèm số dòng: `recon.md` cùng thư mục — executor PHẢI đọc cả hai. Nguồn ERP: `ERP/TanPhatDev/app/Services/Reports/MonitorContractImplementService.php` (gọi tắt **SVC**).

## Global Constraints

- Nhánh `develop` ở cả `hrm-api` và `hrm-client`. KHÔNG push (chỉ commit local; push khi user cho). Commit kết thúc `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- KHÔNG sửa ERP, KHÔNG sửa luồng xuất kho HRM, KHÔNG sửa code dùng chung (`SalesIncome*`, `CustomerDebt*`, helper) — cần sửa thì dừng hỏi.
- Test chạy trên DB gộp thật `erp_hrm_check` bằng `DatabaseTransactions`, KHÔNG `RefreshDatabase`. Lệnh: `cd HRM/hrm-api && vendor/bin/phpunit <file>`.
- Mã quyền: `sale.bao_cao_theo_doi_thuc_hien_hop_dong.view`, scopes `[1, 2, 3, 4]`, Catalog `app/Support/Permissions/Catalog/sale.php` → `'platforms' => ['erp', 'hrm']`. KHÔNG seeder, KHÔNG migration quyền.
- Morph class: firm `App\Model\Sale\Firm\Contract\FirmContract`, wr `App\Model\Customers\WrServiceContract`, HRM `Modules\Assign\Entities\Contract\Contract`.
- TK: 22 = 1311; 181–187 = 511x; 190 = 5211; 191 = 5212; 192 = 5213. `account_details.type` 1 = Nợ, 2 = Có. Work CKHH id 20 (lấy qua code như ERP, không cứng id).
- Lọc kỳ HĐ: chỉ HĐ `created_at > '2023-07-01'` cho firm/wr (như ERP); HĐ HRM không lọc ngày tạo.
- Mẫu in: `report_templates.id = 359` (biến `HEADER`, `TU_NGAY`, `DEN_NGAY`, `CHI_TIET`), khổ ngang. `HEADER` lấy theo khuôn `SalesIncomeSummaryController::dateVariables()`.
- Phân trang 30 HĐ/trang. Số hiển thị chuẩn quốc tế (`toLocaleString('en-US')`, `number_format($x)`); Excel ô số là số thật `#,##0`.
- FE màn mới: chỉ `V2Base*`, select nhân viên khuôn `employeeOptionText`, không `.text-muted`, nút trong cụm `mr-2 mb-2`. Kiểm FE bằng Playwright tại `http://127.0.0.1:3000`.
- Tài liệu chỉ ghi vào `HRM/.plans/bao-cao-theo-doi-thuc-hien-hop-dong/`.

## Review Focus

1. **HĐ cha có PLBS ghi sổ cái riêng** — `revenue_contract/income_money/income/incomed` phải là tổng cha + PLBS (ERP lấy 1 dòng). Test ở Task 3.
2. **Khách có ≥ 2 hãng xe** — `total_after_vat` và DSTC không nhân bản; cột Hãng = các tên nối `, `; lọc Hãng khớp bất kỳ hãng nào của KH. Test ở Task 3 (firm) và Task 5 (lọc).
3. **1 SP ở 2 dòng HĐ HRM** (cùng `erp_product_id`, khác `standard_price`) — DSTC xuất phải khớp theo `contract_product_id`, không cộng chéo. Test ở Task 2.
4. **Trang 2 trở đi** — dòng tổng phòng/NV vẫn là tổng của cả phòng/NV trên toàn bộ dữ liệu lọc, không đổi theo trang; HĐ thiếu `department_id` không hiện nhưng có trong TỔNG CỘNG. Test ở Task 5.
5. **Lọc chỉ Mã HĐ, bỏ trống ngày** — không 422, không nổ; trả HĐ đó với các cột "trong kỳ" tính toàn thời gian. Test ở Task 5 (API) và Task 6 (in/xuất).

---

## Cấu trúc file

**hrm-api** (`Modules/Finance/`):
- `Services/MonitorContractImplement/MonitorContractScope.php` — phạm vi 4 cấp, cột theo alias bảng HĐ.
- `Services/MonitorContractImplement/RowShape.php` — hằng danh sách cột chung + `AMOUNT_FIELDS`.
- `Services/MonitorContractImplement/Sources/FirmContractSource.php` — port `getFirmData` (SVC:36-388) + sửa lỗi.
- `Services/MonitorContractImplement/Sources/WrContractSource.php` — port `getWrData` (SVC:390-908) + sửa lỗi.
- `Services/MonitorContractImplement/Sources/HrmContractSource.php` — nguồn mới `hrm_contracts`.
- `Services/MonitorContractImplement/Sources/ContractSourceFilters.php` — trait: `filter()` (SVC:910-956) + khoảng ngày dùng chung 3 nguồn.
- `Services/MonitorContractImplement/MonitorContractReportService.php` — union, Tỉnh/Hãng, lọc, `rows/totals/tree/search/exportRows`.
- `Services/MonitorContractImplement/MonitorContractPrintTable.php` — HTML bảng in (port `getTable` SVC:1115-1275 nhánh print).
- `Http/Controllers/V1/MonitorContractImplementController.php` — `index`, `meta`, `exportRows`, `printListData`.
- `Routes/api.php` — nhóm `/monitor-contract-implement` ngay sau nhóm `/sales-income-summary` (~L2008).
- `Tests/Feature/Concerns/GrantsMonitorContractScope.php`, `Tests/Feature/Concerns/BuildsMonitorContractFixtures.php`.
- `Tests/Feature/MonitorContract{Scope,HrmSource,FirmSource,WrSource,ReportService,Api}Test.php`.
- `app/Support/Permissions/Catalog/sale.php:813` — thêm `'hrm'`.

**hrm-client:**
- `pages/sale/monitor-contract-implement/index.vue`, `pages/sale/monitor-contract-implement/components/export-excel.js`.
- `components/subsystem-menu/sale-hub.js:265` — gắn link.
- `../e2e/tests/monitor-contract-implement.spec.ts` (bám spec e2e của sales-income-summary nếu có, không thì spec list chuẩn trong `e2e/`).

---

### Task 1: Phạm vi quyền + Catalog

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/MonitorContractScope.php`
- Create: `Modules/Finance/Tests/Feature/Concerns/GrantsMonitorContractScope.php`
- Modify: `app/Support/Permissions/Catalog/sale.php:813`
- Test: `Modules/Finance/Tests/Feature/MonitorContractScopeTest.php`

**Interfaces:**
- Produces: `MonitorContractScope::CODE = 'sale.bao_cao_theo_doi_thuc_hien_hop_dong.view'`; hằng `ALL/COMPANY/DEPARTMENT/PART/OWN` (cùng giá trị chuỗi như `SalesIncomeScope`); `level(): string`; `apply($query, string $alias): void` — lọc `{alias}.company_id|department_id|part_id`, mọi cấp OR `{alias}.created_by = auth()->id()`, OWN chỉ `{alias}.created_by`.
- Produces (test): trait `GrantsMonitorContractScope` với `ensureMonitorContractCode(): int`, `grantMonitorContractScope(int $employeeId, int $scope, ?int $companyId = null): void` — chép `GrantsSalesIncomeScope`, đổi mã.

- [x] **Step 1: Viết test** — chép cấu trúc `SalesIncomeScopeTest`, query gốc `DB::table('hrm_contracts as c')`, `apply($q, 'c')`:
  - `test_khong_quyen_chi_hd_minh_lap`: level `own`; SQL chứa `` `c`.`created_by` = ? ``, bindings `[$emp->id]`.
  - `test_quyen_cong_ty_loc_cong_ty_dang_chon_hoac_minh_lap`: scope 3 → SQL chứa `` `c`.`company_id` in (?) ``, bindings chứa `current_company_role` và `$emp->id`.
  - `test_quyen_phong_ban`: scope 2 → `` `c`.`department_id` in ``, bindings `array_merge(listManageDepartmentIds() ?: [0], [$emp->id])`.
  - `test_quyen_bo_phan_gom_bo_phan_minh`: scope 1 → `` `c`.`part_id` in ``, bindings = bộ phận quản lý ∪ `info->part_id` (unique, `?: [0]`) + `$emp->id`.
  - `test_tong_cong_ty_khong_loc`: scope 4 → SQL không có `where`.
  - `test_catalog_mo_hrm`: Catalog `sale.php` mục `CODE` có `scopes === [1,2,3,4]` và `platforms` chứa `'hrm'`.
- [x] **Step 2:** `vendor/bin/phpunit Modules/Finance/Tests/Feature/MonitorContractScopeTest.php` → FAIL (class không tồn tại).
- [x] **Step 3:** Viết `MonitorContractScope` (khối `level()` y `SalesIncomeScope`; `apply` nhận alias thay prefix + ownColumn). Thêm `'hrm'` vào `platforms` của mã ở `sale.php`.
- [x] **Step 4:** Chạy lại → 6 PASS.
- [x] **Step 5:** Commit `feat(finance): pham vi bao cao theo doi thuc hien HD + mo ma quyen cho hrm`.

---

### Task 2: Nguồn HĐ HRM

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/RowShape.php`
- Create: `Modules/Finance/Services/MonitorContractImplement/Sources/ContractSourceFilters.php`
- Create: `Modules/Finance/Services/MonitorContractImplement/Sources/HrmContractSource.php`
- Create: `Modules/Finance/Tests/Feature/Concerns/BuildsMonitorContractFixtures.php`
- Test: `Modules/Finance/Tests/Feature/MonitorContractHrmSourceTest.php`

**Interfaces:**
- Consumes: `MonitorContractScope::apply($query, $alias)`.
- Produces: `RowShape::AMOUNT_FIELDS = ['total_after_vat','revenue_contract','standard_amount_export','income_money','standard_amount','standard_amount_exported','income','incomed']` (`income_remain` tính sau = `income − incomed`). Mỗi nguồn `select` đúng các cột: `source` (`'firm'|'wr'|'hrm'`), `contract_id`, `contract_code`, `customer_id`, `company_id`, `department_id`, `part_id`, `created_by`, `province_id` (firm/wr: tỉnh địa điểm giao của báo giá HĐ gốc; hrm: `customers.province_id`), + 8 `AMOUNT_FIELDS`.
- Produces: interface ngầm cho 3 nguồn: `public function query(Request $request, MonitorContractScope $scope): \Illuminate\Database\Query\Builder` — 1 dòng / HĐ gốc. Request dùng khoá `company_id, department_id, part_id, employee_id, customer_id, contract_code, start_date, end_date` (`Y-m-d`; cả hai trống = không giới hạn kỳ).
- Produces: trait `ContractSourceFilters` với `applyFilters(Builder $q, Request $r, MonitorContractScope $scope, string $alias): void` (company/department/part/created_by=employee_id/customer_id/code chính xác + scope) và `applyPeriod(Builder $q, Request $r, string $column): void` (`whereDate >= start`, `<= end`, bỏ qua vế trống).
- Produces (test): trait `BuildsMonitorContractFixtures` — `makeHrmContract(array $attrs = []): int`, `addHrmLine(int $contractId, array $attrs): int`, `addLedger(string $contractableType, int $contractId, int $accountId, int $type, float $amount, string $invoiceableType, string $date, ?int $workId = null): void`, `addHrmExport(int $contractId, array $lineQtys /* [lineId => qty] */, int $type, int $status, string $createdAt): int`, `addHrmImportReturn(...)`, `addHrmBorrowSell(...)` cùng kiểu. Executor tự tra cột NOT NULL của từng bảng trên `erp_hrm_check`.

Công thức (design §4, recon §2.1). Khớp dòng HĐ cho PXK qua `product_export_request_tab_products.contract_product_id` (từ phiếu → YCXH → dòng tab cùng `product_id`), chỉ PXK `type = 21`, hoàn tất (`status` theo hằng hoàn tất của `ProductExport`, bám ERP `status = 1`); bán mượn qua `borrow_sell_products.objectable_type = 'Modules\Assign\Entities\Contract\ContractProductPrice'`; nhập trả lại `product_imports` type 4/9 hoàn tất `emplement_contract_*` = HĐ HRM, khớp dòng qua đường tham chiếu dòng của phiếu nếu có, chỉ khi không có mới khớp `erp_product_id` + `contract_id` (ghi rõ trong code đường đã chọn). Dự phòng: công thức firm SVC:77-109 với `firm_support_accounting` `contractable_type` HĐ HRM, base `qty × unit_price_after_discount` của phần tương ứng. Định mức giảm giá = 0. Dịch vụ = 0.

- [x] **Step 1: Viết test** — fixture chung (setUp): HĐ HRM C (`total_after_vat` 110,000,000), dòng L1 `qty_needed` 10, `standard_price` 9,000,000, `unit_price_after_discount` 10,000,000; kỳ 01/10/2026–31/10/2026. Sổ cái (contractable HĐ HRM, TK/loại như sau): 15/10 Có 181 30,000,000 (ProductExport); 15/10 Nợ 190 3,000,000 work CKHH; 15/10 Nợ 22 33,000,000 ProductExport; 20/10 Có 22 20,000,000 BillIncome; 21/10 Nợ 22 2,000,000 BillPayment; 10/09 Có 22 5,000,000 BillIncome. Chứng từ: PXK 21 hoàn tất 15/10 L1 qty 3; PXK 21 hoàn tất 10/09 L1 qty 2; bán mượn hoàn tất 16/10 L1 qty 1; nhập trả lại hoàn tất 17/10 L1 qty 1.
  - `test_hd_hrm_du_cot`: dòng `source='hrm'`, `contract_code` = mã C, `total_after_vat` 110,000,000; `revenue_contract` 27,000,000; `income_money` 18,000,000; `standard_amount_export` 27,000,000; `standard_amount` 90,000,000; `standard_amount_exported` 45,000,000; `income` 33,000,000; `incomed` 23,000,000.
  - `test_hd_khong_co_1311_trong_ky_khong_len`: kỳ 01/11–30/11 → không có dòng C.
  - `test_khong_ngay_tinh_toan_thoi_gian`: `start_date/end_date` trống + `contract_code` = mã C → `income_money` 23,000,000, `standard_amount_export` 45,000,000.
  - `test_cung_sp_hai_dong_khong_cong_cheo`: thêm L2 cùng `erp_product_id` với L1, `standard_price` 1,000,000, `qty_needed` 5; PXK 15/10 xuất L2 qty 4 → `standard_amount_export` tăng đúng 4,000,000 (= 31,000,000), `standard_amount` 95,000,000.
  - `test_pxk_loai_20_va_chua_hoan_tat_khong_tinh`: PXK type 20 hoàn tất + PXK 21 chưa hoàn tất trong kỳ → `standard_amount_export` vẫn 27,000,000.
  - `test_du_phong`: `firm_support_accounting` của C `redundancy_cost` 1,000,000, `before_vat_product` 100,000,000, `before_vat_repair_service` 0 → `standard_amount` = 90,000,000 + giá trị theo công thức SVC:77-109 (ghi phép tính trong comment test).
  - `test_pham_vi_khong_quyen_chi_hd_minh_lap`: đăng nhập NV khác `created_by` không quyền → không có dòng C.
- [x] **Step 2:** Chạy test → FAIL.
- [x] **Step 3:** Viết `RowShape`, `ContractSourceFilters`, `HrmContractSource::query()`. Mỗi cột số là 1 subquery gom theo `contract_id` rồi `leftJoinSub` vào `hrm_contracts` (tránh nhân bản), `COALESCE(x, 0)`.
- [x] **Step 4:** Chạy test → 7 PASS.
- [x] **Step 5:** Commit `feat(finance): nguon HD HRM cho bao cao theo doi thuc hien HD`.

---

### Task 3: Nguồn HĐ hãng (firm)

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/Sources/FirmContractSource.php`
- Modify: `Modules/Finance/Tests/Feature/Concerns/BuildsMonitorContractFixtures.php` (thêm `makeFirmContract(array $attrs): int`)
- Test: `Modules/Finance/Tests/Feature/MonitorContractFirmSourceTest.php`

**Interfaces:**
- Consumes: `ContractSourceFilters`, `RowShape`, `MonitorContractScope`.
- Produces: `FirmContractSource::query(Request, MonitorContractScope): Builder` cùng cột `RowShape`, `source = 'firm'`, `contract_id/contract_code` = HĐ cha (`COALESCE(firm1.*, firm.*)`, ĐHNT type 8 đứng riêng).

Port SVC:36-388 giữ nguyên mọi công thức, chỉ khác: (a) 4 số sổ cái là SUM cả HĐ cha + PLBS (design §2.3); (b) KHÔNG join `customer_has_vehicle_manufacts` trong nguồn (Hãng nối ở Task 5); (c) bỏ join tỉnh/hãng cuối hàm, chỉ trả `province_id`; (d) kỳ dùng `applyPeriod` (trống = không giới hạn).

- [x] **Step 1: Viết test**:
  - `test_plbs_cong_so_cai_ca_cha_va_phu_luc`: HĐ cha type 1 + PLBS type 2 `parent_contract_id` = cha; trong kỳ Có 181 10,000,000 contractable cha, Có 181 4,000,000 contractable PLBS, Nợ 22 BillPayment… (mỗi HĐ 1 dòng 1311 trong kỳ) → 1 dòng mã cha, `revenue_contract` 14,000,000.
  - `test_khach_nhieu_hang_xe_khong_nhan_ban`: KH gắn 2 hãng xe, HĐ `total_after_vat` 50,000,000 → đúng 1 dòng, `total_after_vat` 50,000,000.
  - `test_loai_bo_type_7_9_va_hd_truoc_2023_07`: HĐ type 7 và HĐ `created_at` 2023-06-30 có 1311 trong kỳ → không lên.
  - `test_pl_giam_da_duyet_tru_gia_tri`: PL giảm type 3 status 3 `total_after_vat` 5,000,000 → giá trị cha giảm 5,000,000.
  - `test_khop_erp_tren_du_lieu_that`: lấy 1 kỳ có dữ liệu firm trên `erp_hrm_check` (vd tháng gần nhất có ≥ 5 HĐ), chạy SQL gốc ERP (chép thành chuỗi trong fixture `tests/fixtures/erp_monitor_firm.sql` hoặc gọi ERP qua `php artisan tinker` ở Task 8) — **chỉ** so các HĐ không có PLBS và KH ≤ 1 hãng: mọi cột bằng nhau. Nếu dựng test này quá nặng thì dời toàn bộ đối số sang Task 8 và ghi `Ruling` vào ledger.
- [x] **Step 2:** Chạy → FAIL.
- [x] **Step 3:** Viết `FirmContractSource`.
- [x] **Step 4:** Chạy → PASS.
- [x] **Step 5:** Commit `feat(finance): nguon HD hang cho bao cao theo doi thuc hien HD`.

---

### Task 4: Nguồn HĐ dịch vụ (wr)

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/Sources/WrContractSource.php`
- Modify: `Modules/Finance/Tests/Feature/Concerns/BuildsMonitorContractFixtures.php` (thêm `makeWrContract(array $attrs): int`)
- Test: `Modules/Finance/Tests/Feature/MonitorContractWrSourceTest.php`

**Interfaces:**
- Produces: `WrContractSource::query(Request, MonitorContractScope): Builder`, `source = 'wr'`, gộp `COALESCE(wr.parent_id, wr.id)`.

Port SVC:390-908 giữ nguyên (kể cả thực thu chỉ Σ Có 4 loại, doanh thu Theo HĐ chỉ 5 loại invoiceable — design §5), chỉ sửa: SUM sổ cái cha + PLBS; chuỗi `ServiceAccounting` đúng `App\Model\Sale\ServiceAccounting` để Có ServiceAccounting được trừ khỏi `income`; không join hãng xe; kỳ qua `applyPeriod`.

- [x] **Step 1: Viết test**:
  - `test_co_service_accounting_tru_phai_thu`: HĐ wr có Nợ 22 ServiceAccounting 10,000,000 và Có 22 ServiceAccounting 3,000,000 → `income` 7,000,000.
  - `test_plbs_cong_so_cai`: wr cha + con type 3 `parent_id` → `income_money` = tổng Có BillIncome của cả hai.
  - `test_loai_pl_giam_type_4`: wr type 4 có 1311 trong kỳ → không thành dòng riêng; status 3 → trừ `total_after_vat` cha.
  - `test_thuc_thu_khong_tru_phieu_chi_nhu_erp`: Có BillIncome 8,000,000 + Nợ BillPayment 1,000,000 trong kỳ → `income_money` 8,000,000.
- [x] **Step 2:** Chạy → FAIL. **Step 3:** Viết `WrContractSource`. **Step 4:** Chạy → PASS.
- [x] **Step 5:** Commit `feat(finance): nguon HD dich vu cho bao cao theo doi thuc hien HD`.

---

### Task 5: Service tổng hợp + API danh sách

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/MonitorContractReportService.php`
- Create: `Modules/Finance/Http/Controllers/V1/MonitorContractImplementController.php`
- Modify: `Modules/Finance/Routes/api.php` (sau nhóm `/sales-income-summary`)
- Test: `Modules/Finance/Tests/Feature/MonitorContractReportServiceTest.php`, `Modules/Finance/Tests/Feature/MonitorContractApiTest.php`

**Interfaces:**
- Consumes: 3 nguồn (Task 2-4), `MonitorContractScope`.
- Produces:
  - `rows(Request $r): Collection` — union 3 nguồn; `leftJoin customers` (code, name), `provinces` theo `province_id` (name); `leftJoinSub` hãng xe gom theo KH (`GROUP_CONCAT(DISTINCT vm.name ORDER BY vm.name SEPARATOR ', ')` + đếm); lọc `province_ids[]` (`province_id IN`), `vehicle_manufact_ids[]` (`EXISTS customer_has_vehicle_manufacts` của KH với id IN); `ORDER BY department_id, created_by, contract_code`. Mỗi phần tử là mảng: các cột `RowShape` + `customer_code`, `customer_name`, `province_name`, `vehicle_manufacts`, `income_remain`, `url` (hrm → `/assign/contracts/{id}`, wr → `/customer-care/wr-service-contracts/{id}`, firm → `ERP_URL + /admin/sale/firm-contracts/{id}`, trả `is_external = true`).
  - `totals(Collection $rows): array` — SUM 9 trường (`AMOUNT_FIELDS` + `income_remain`).
  - `tree(Collection $pageRows, Collection $allRows): array` — `[{department_id, department_name, totals, province_no, vehicle_no, employees:[{employee_id, employee_name, employee_code, totals, province_no, vehicle_no, contracts:[row…]}]}]`; chỉ chứa phòng/NV có HĐ trên `$pageRows`, nhưng `totals`/`province_no`/`vehicle_no` tính trên `$allRows`; bỏ dòng `department_id` null. Bám `SalesIncomeReportService::tree`.
  - `search(Request $r): array` — `['summary' => totals(all), 'data' => tree(page, all), 'pagination' => {...}]`, `per_page` mặc định 30.
  - `exportRows(Request $r): array` — dòng phẳng đã dựng cây theo trang `page/per_page` (mặc định 2000, trần 5000) cho FE dựng Excel; kèm `summary` ở trang 1.
- Routes (prefix `/monitor-contract-implement`, không gate): `GET /` → `index`, `GET /meta` → `meta`, `GET /export-rows` → `exportRows`, `GET /print-list-data` → `printListData` (Task 6).
- `meta()` trả `permissions` 4 cờ như `SalesIncomeSummaryController::unitPermissions`.
- Validate: `start_date`, `end_date` bắt buộc `date` **trừ khi có `contract_code`**; `end_date >= start_date`; `province_ids.*`, `vehicle_manufact_ids.*` integer → 422.

- [x] **Step 1: Viết test service** (fixture HĐ dựng: 2 phòng D1, D2; D1 có NV A lập 3 HĐ, NV B 1 HĐ; D2 1 HĐ; 1 HĐ HRM không `department_id`; 1 HĐ firm KH có 2 hãng xe):
  - `test_tong_cong_gom_ca_hd_khong_phong`: `summary.total_after_vat` = Σ mọi HĐ fixture; cây không có HĐ thiếu phòng.
  - `test_tong_phong_nv_tinh_toan_bo_khong_theo_trang`: `per_page` 2, trang 2 → tổng NV A = tổng 3 HĐ của A (không phải 1 HĐ trên trang).
  - `test_cot_hang_noi_chuoi`: dòng HĐ KH 2 hãng có `vehicle_manufacts` = `"<tên1>, <tên2>"` theo thứ tự tên.
  - `test_loc_hang_va_tinh`: lọc 1 trong 2 hãng → HĐ đó vẫn lên; lọc tỉnh khác → không lên.
  - `test_gop_ba_nguon`: kỳ chứa HĐ firm + wr + HRM → `source` có đủ `firm`, `wr`, `hrm`.
- [x] **Step 2: Viết test API**: `test_index_thieu_ngay_422`, `test_index_chi_ma_hd_khong_can_ngay` (200, có đúng HĐ đó), `test_meta_tra_co_quyen` (cấp scope 3 → `is_company` true, `is_all_company` false), `test_khong_quyen_chi_thay_hd_minh_lap`, `test_export_rows_tran_5000` (`per_page` 9999 → pagination.per_page 5000).
- [x] **Step 3:** Chạy 2 file → FAIL. **Step 4:** Viết service, controller, route. **Step 5:** Chạy → PASS; chạy lại test Task 1-4 → PASS.
- [x] **Step 6: Đo thời gian** `index` trên `erp_hrm_check` kỳ 1 tháng và 1 năm (`curl` có token, hoặc test tạm ghi `microtime`) → ghi số vào `HRM/.plans/bao-cao-theo-doi-thuc-hien-hop-dong/perf.md`. > 2s ⇒ thêm index/viết lại subquery trước khi sang Task 6; số so ERP cùng kỳ nếu đo được.
- [x] **Step 7:** Commit `feat(finance): API bao cao theo doi thuc hien HD`.

---

### Task 6: In

**Files:**
- Create: `Modules/Finance/Services/MonitorContractImplement/MonitorContractPrintTable.php`
- Modify: `Modules/Finance/Http/Controllers/V1/MonitorContractImplementController.php` (`printListData`)
- Test: `Modules/Finance/Tests/Feature/MonitorContractApiTest.php` (thêm ca)

**Interfaces:**
- Produces: `MonitorContractPrintTable::render(array $tree, array $total): string` — bảng 12 cột như ERP nhánh print (SVC:1115-1275): dòng TỔNG CỘNG, dòng phòng (tỉnh/hãng trống), dòng NV ("N tỉnh" / "N hãng xe"), dòng HĐ (có tỉnh + hãng); số `number_format`. Bám style `SalesIncomePrintTable`.
- `printListData` khuôn y `SalesIncomeSummaryController::printListData` (trait `LimitsPrintListRows`, `printListPayload`, `landscape: true`), template 359; `TU_NGAY/DEN_NGAY` rỗng khi không có ngày.

- [x] **Step 1: Test**: `test_print_list_data_dien_mau_359` (html chứa mã HĐ fixture, chữ `TỔNG CỘNG`, số `110,000,000`), `test_print_chi_ma_hd_khong_ngay_khong_no` (200).
- [x] **Step 2:** FAIL → **Step 3:** viết → **Step 4:** PASS.
- [x] **Step 5:** Commit `feat(finance): in bao cao theo doi thuc hien HD`.

---

### Task 7: Màn FE + Xuất Excel + menu

**Files:**
- Create: `hrm-client/pages/sale/monitor-contract-implement/index.vue`
- Create: `hrm-client/pages/sale/monitor-contract-implement/components/export-excel.js`
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:265` → `{ n: 'Theo dõi thực hiện hợp đồng', link: '/sale/monitor-contract-implement' }`
- Create: `e2e/tests/monitor-contract-implement.spec.ts`

**Interfaces:**
- Consumes: API Task 5-6 (`/v1/finance/monitor-contract-implement`, `/meta`, `/export-rows`, `/print-list-data`).

Copy pattern từ `pages/sale/sales-income-summary/index.vue` (bộ lọc, cây phòng → NV → HĐ, In, Xuất) và `components/export-excel.js` (ExcelJS, ô số thật `#,##0`). Cột (12, đúng thứ tự ERP VIEW): Hợp đồng · Khách hàng · Tỉnh/TP · Hãng · Giá trị HĐ · DS thực xuất (Theo HĐ / Tiêu chuẩn) · Số tiền thực thu trong kỳ · Tổng DSTC HĐ (Tiêu chuẩn / Thực xuất) · Công nợ (Phải thu / Đã thu / Còn nợ). Bộ lọc: Công ty / Phòng / Bộ phận (hiện theo cờ `meta.permissions`), Nhân viên (người lập HĐ, `employeeOptionText`), Khách hàng (search server-side), Mã HĐ, Từ ngày–Đến ngày (bắt buộc trừ khi có Mã HĐ — validate FE đỏ dưới ô), Tỉnh (nhiều), Hãng xe (nhiều). Mã HĐ là link (`url`; `is_external` mở tab mới). Excel lấy qua `utils/export/listExportFile.js` gọi lặp `/export-rows`, điền cả Tỉnh/Hãng ở dòng HĐ, tên file `bao_cao_theo_doi_thuc_hien_hop_dong.xlsx`.

- [x] **Step 1: Viết e2e spec**: mở `/sale/monitor-contract-implement` → bấm Tìm khi trống ngày ⇒ 2 ô ngày báo `Bắt buộc phải nhập`; chọn kỳ có dữ liệu ⇒ bảng có dòng `TỔNG CỘNG` và ≥ 1 dòng HĐ; sang trang 2 (nếu > 30 HĐ) dòng TỔNG CỘNG không đổi; nhập chỉ Mã HĐ ⇒ tìm được; bấm Xuất Excel ⇒ tải về file `bao_cao_theo_doi_thuc_hien_hop_dong.xlsx`; bấm In ⇒ mở bản in có `TỔNG CỘNG`.
- [x] **Step 2:** Chạy (`cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test monitor-contract-implement`) → FAIL.
- [x] **Step 3:** Viết page, export-excel, menu.
- [x] **Step 4:** Chạy spec → PASS. Tự kiểm: `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/sale/monitor-contract-implement/ | grep -v V2Base` rỗng; grep `toLocaleString('vi-VN')` rỗng; đo 2 nút liền nhau cách 12px; chụp màn hình lưu scratchpad.
- [x] **Step 5:** Commit (hrm-client) `feat(sale): man bao cao theo doi thuc hien hop dong`.

---

### Task 8: Đối số với ERP + danh sách lệch

**Files:**
- Create: `HRM/.plans/bao-cao-theo-doi-thuc-hien-hop-dong/doi-so-erp.md`
- Script tạm ở scratchpad (không commit).

- [x] **Step 1:** Chọn 3 kỳ trên `erp_hrm_check` (1 tháng gần nhất có dữ liệu, 1 quý, 1 kỳ có HĐ PLBS). Lấy kết quả ERP: chạy `MonitorContractImplementService::getData()` bằng `php artisan tinker` trong `ERP/TanPhatDev` với đăng nhập NV có quyền tổng công ty (ERP local trỏ đúng DB — **kiểm `grep DB_ .env` trước**, không được chạm DB prod). Lấy kết quả HRM từ `MonitorContractReportService::rows()` cùng kỳ, nguồn firm + wr.
- [x] **Step 2:** So từng HĐ × 9 cột. Mọi chỗ lệch phải xếp vào đúng 1 lý do của design §2.3 (PLBS, nhiều hãng xe, ServiceAccounting, kỳ trống) — lệch không giải thích được ⇒ quay lại Task 3/4 sửa.
- [x] **Step 3:** Ghi `doi-so-erp.md`: kỳ, số HĐ, số HĐ khớp, bảng HĐ lệch (mã, cột, ERP, HRM, lý do) — QA dùng file này.
- [x] **Step 4:** Ghi memory project (trạng thái commit, chưa push, rollout cần `permission:catalog-sync` + cấp quyền ở `/admin/roles`).
