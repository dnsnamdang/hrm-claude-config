# Báo cáo thưởng theo hợp đồng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Màn `/sale/bonus-contract-report` trên HRM: báo cáo thưởng (sổ TK 3351) theo hợp đồng → nhân viên, như ERP `reports/bonus_contract_report`, gộp HĐ hãng / HĐ DV / HĐ HRM, có In + Xuất Excel.

**Architecture:** Module `Finance`, thư mục `Services/BonusContractReport/`. Một class `BonusLedger` dựng truy vấn tổng 4 cột trên `account_details` (TK 3351) kèm đủ bộ lọc + phạm vi, gom theo cột truyền vào. Service lấy dòng HĐ = 3 nhánh (firm / wr / hrm) join bảng HĐ + phòng, `UNION ALL`, sắp xếp. Dòng NV lấy **1 câu cho cả tập HĐ cần hiện** (không N+1) rồi ghép vào HĐ theo (type, id, code). Controller không gate, phạm vi qua `BonusContractScope` (bám ERP `filterDate` 1:1, KHÔNG bám `MonitorContractScope`). FE 1 trang Nuxt bám `pages/sale/monitor-contract-implement`.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), MySQL `erp_hrm_check`, PHPUnit, Playwright.

**Spec:** `HRM/.plans/bao-cao-thuong-theo-hop-dong/design.md` (duyệt 14/11/2026) — executor PHẢI đọc. Nguồn ERP: `ERP/TanPhatDev/app/Services/Reports/BonusBusinessContractReportService.php` (gọi tắt **SVC**): `getBonusContract` SVC:210-297, NV SVC:300-396, `filterDate` SVC:397-460, `printListData` SVC:607-667; controller `ReportController.php:2164-2215`.

## Global Constraints

- Làm trong worktree, nhánh `feature/bao-cao-thuong-theo-hop-dong` tách từ `develop`: `HRM/wt-bonus-contract-api` (hrm-api) và `HRM/wt-bonus-contract-client` (hrm-client). KHÔNG chuyển nhánh / reset repo chính. Commit local, KHÔNG push, KHÔNG gop_db. Commit kết thúc `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- `vendor` của worktree là symlink sang repo chính → phpunit phải chạy với bootstrap tạm ở scratchpad: require `vendor/autoload.php` rồi `addPsr4('Modules\\', <wt>/Modules/, true)`, `App\\`, `Tests\\` (prepend). Lệnh: `vendor/bin/phpunit --bootstrap <scratch>/bootstrap.php <file>` (không dùng `php artisan test --filter`).
- KHÔNG sửa ERP, KHÔNG sửa code dùng chung (`MonitorContract*`, `SalesIncome*`, helper, `LimitsPrintListRows`) — cần sửa thì dừng hỏi.
- Test chạy trên DB gộp thật `erp_hrm_check` bằng `DatabaseTransactions`, KHÔNG `RefreshDatabase`. Không upload file thật.
- Mã quyền `accounting.bao_cao_thuong_theo_hop_dong.view`, scopes `[1, 2, 3, 4]`, Catalog `app/Support/Permissions/Catalog/accounting.php:613` → `'platforms' => ['erp', 'hrm']`. KHÔNG seeder, KHÔNG migration quyền.
- Morph: firm `App\Model\Sale\Firm\Contract\FirmContract`, wr `App\Model\Customers\WrServiceContract`, HRM `Modules\Assign\Entities\Contract\Contract`. Loại trừ `invoiceable_type`: `App\Model\IncomeExpenditure\BillPayment`, `App\Model\IncomeExpenditure\BillPaymentAuthorization`, `App\Model\Accounting\ClosingEntry`.
- `account_details.identify_number = 3351`; `type` 1 = Nợ, 2 = Có; cột tiền `money_value_exchange`. Work id tra `works.code` ∈ `TTHHD` (→ `diff_employee`), `TNST` (→ `commission_month`), `TNSQ` (→ `commission_quarter`), `TVC` (→ `commission_transport`), không cứng id. Bắt buộc `contractable_id` và `employee_id` NOT NULL.
- `firm_contracts.status` đã quyết toán = `10` (ERP `FirmContract::DA_QUYET_TOAN`).
- Mẫu in `report_templates.id = 310`, khổ ngang, biến `CHI_TIET`, `NGAY`, `THANG`, `NAM` (ngày in), `HEADER` = `companies.header` theo công ty **hồ sơ** người in (`auth()->user()->info->company_id`, như ERP).
- 10 HĐ/trang. Số hiển thị chuẩn quốc tế (`toLocaleString('en-US')` / `number_format($x)`), ô 0 hiện `-` (bảng, In, Excel như ERP); Excel ô số là số thật `#,##0`, tên file `bao_cao_thuong_theo_hop_dong.xlsx`, tiêu đề `Báo cáo thưởng theo hợp đồng`.
- FE màn mới: chỉ `V2Base*`, select NV khuôn `employeeOptionText`, không `.text-muted`, nút trong cụm `mr-2 mb-2`. Kiểm FE bằng Playwright tại `http://127.0.0.1:3000` (Node 20 cho e2e). KHÔNG ghi đè `e2e/.auth/user.json`.
- Tài liệu chỉ ghi vào `HRM/.plans/bao-cao-thuong-theo-hop-dong/`. Lệch ERP nào phát sinh khi làm → bổ sung design §6.

## Review Focus

1. **HĐ hãng và HĐ DV trùng id** (cùng `contractable_id`, khác type) — 2 dòng riêng, NV không lẫn sang nhau, DSTC firm không gắn vào HĐ DV. Test ở Task 3 và Task 4.
2. **Tham số sắp xếp lạ** (`sort_column=foo; drop`, `sort_order=sideways`) — không lỗi SQL, rơi về mặc định (ERP đưa thẳng request vào `orderBy`). Test ở Task 3 (whitelist) và Task 5 (API 200).
3. **Trang 2 trở đi / TỔNG CỘNG** — dòng tổng luôn cộng trên toàn bộ HĐ đã lọc, không đổi theo trang; NV chỉ lấy cho HĐ của trang đang xem. Test ở Task 5.
4. **Người không quyền / quyền Bộ phận** — dòng tổng, In, Excel không chứa bút toán ngoài phạm vi (kể cả khi gửi `company_id` công ty khác). Test ở Task 1 (scope) và Task 5 (tổng qua API).
5. **NV đã nghỉ / không phòng** — NV không phòng không ra dòng NV nhưng tiền vẫn ở dòng HĐ; HĐ không phòng không ra cả dòng HĐ lẫn tổng. Test ở Task 4 (NV) và Task 3 (HĐ).

---

## Cấu trúc file

**hrm-api** (`Modules/Finance/`):
- `Services/BonusContractReport/BonusContractScope.php` — phạm vi 4 cấp trên bút toán (port `filterDate` phần quyền).
- `Services/BonusContractReport/BonusLedger.php` — truy vấn tổng 4 cột TK 3351 + lọc ngày/tổ chức/NV/mã HĐ + scope, gom theo cột truyền vào.
- `Services/BonusContractReport/BonusContractReportService.php` — dòng HĐ (union 3 nguồn), dòng NV, tổng, `search / allContracts / exportRows`, link HĐ.
- `Services/BonusContractReport/BonusContractPrintTable.php` — HTML `CHI_TIET` (port SVC:607-638 nhánh print).
- `Http/Controllers/V1/BonusContractReportController.php` — `index`, `meta`, `exportRows`, `printListData`.
- `Routes/api.php` — nhóm `/bonus-contract-report` ngay sau nhóm `/monitor-contract-implement` (~L2068).
- `Tests/Feature/Concerns/BuildsBonusLedgerFixtures.php` — chèn bút toán 3351 giả + HĐ/NV giả.
- `Tests/Feature/BonusContract{Scope,Ledger,ReportService,Api}Test.php`.
- `app/Support/Permissions/Catalog/accounting.php:613` — thêm `'hrm'`.

**hrm-client:**
- `pages/sale/bonus-contract-report/index.vue`, `pages/sale/bonus-contract-report/components/export-excel.js`.
- `components/subsystem-menu/sale-hub.js:266` — `'Thưởng theo hợp đồng'` → `{ n: 'Thưởng theo hợp đồng', link: '/sale/bonus-contract-report' }`.
- `../e2e/tests/bonus-contract-report.spec.ts` (bám `e2e/tests/monitor-contract-implement.spec.ts`).

---

### Task 1: Catalog + `BonusContractScope`

**Files:**
- Modify: `app/Support/Permissions/Catalog/accounting.php:613` (`platforms` → `['erp', 'hrm']`)
- Create: `Modules/Finance/Services/BonusContractReport/BonusContractScope.php`
- Create: `Modules/Finance/Tests/Feature/Concerns/BuildsBonusLedgerFixtures.php` (trong task này chỉ cần `ensureBonusContractCode()` + `grantBonusContractScope(int $employeeId, int $scope)` — copy khuôn `GrantsMonitorContractScope`, đổi mã)
- Test: `Modules/Finance/Tests/Feature/BonusContractScopeTest.php`

**Interfaces:**
- Produces: `BonusContractScope::CODE = 'accounting.bao_cao_thuong_theo_hop_dong.view'`; hằng `ALL|COMPANY|DEPARTMENT|PART|OWN` = `'all'|'company'|'department'|'part'|'own'`; `level(): string`; `flags(): array` (`is_all_company`, `is_company`, `is_department`, `is_part` — cộng dồn như SVC:31-37); `apply($query, string $alias = 'ad'): void`.

- [x] **Step 1: Viết test** (NV thường, xoá role/permission riêng như `MonitorContractScopeTest::plainEmployee`):
  - `test_khong_quyen_chi_but_toan_cua_minh`: level `own`; SQL chứa `` `ad`.`employee_id` = ? ``, bindings `[me]`.
  - `test_cong_ty_theo_cong_ty_ho_so`: scope 3 → SQL `` (`ad`.`company_id` = ? or `ad`.`employee_id` = ?) ``, bindings `[info->company_id, me]` — **không** dùng `current_company_role` (đặt `company_role` khác `company_id` trong test để bắt nhầm).
  - `test_phong_ban_theo_phong_quan_ly_cung_cong_ty_ho_so`: chèn 2 dòng `employee_manage_departments` (1 cùng `company_id` hồ sơ, 1 công ty khác) → `whereIn` chỉ chứa phòng cùng công ty; không quản lý phòng nào → `in (0)` hoặc tương đương rỗng, vẫn OR của mình.
  - `test_bo_phan_chi_bo_phan_cua_minh`: scope 1 → `` `ad`.`part_id` = ? `` bằng `info->part_id` (không gộp bộ phận quản lý).
  - `test_tong_cong_ty_khong_loc`: scope 4 → SQL không có `where`.
  - `test_flags_cong_don`: scope 2 → `is_department`, `is_part` true; `is_company`, `is_all_company` false.
- [x] **Step 2:** chạy `BonusContractScopeTest` → FAIL (class không tồn tại).
- [x] **Step 3:** implement. Level qua `CurrentPermission::scope(self::CODE)` như `MonitorContractScope::level()`. Phòng quản lý đọc `App\Models\EmployeeManageDepartment` (`employee_id` = me, `company_id` = công ty hồ sơ). `info->part_id` null → điều kiện `part_id = 0` OR của mình (không lọt toàn bảng).
- [x] **Step 4:** chạy lại → PASS.
- [x] **Step 5:** commit `feat(finance): pham vi bao cao thuong theo hop dong`.

### Task 2: `BonusLedger` — tổng 4 cột TK 3351

**Files:**
- Create: `Modules/Finance/Services/BonusContractReport/BonusLedger.php`
- Modify: `Modules/Finance/Tests/Feature/Concerns/BuildsBonusLedgerFixtures.php` — thêm `ledgerRow(array $overrides): int` (chèn `account_details`, mặc định `identify_number=3351`, `type=2`, `work_id` = id `TTHHD`, `invoiceable_type` = 1 class không bị loại, `invoiceable_date_accounting` trong kỳ test, `contractable_type` HRM) và `workId(string $code): int`.
- Test: `Modules/Finance/Tests/Feature/BonusContractLedgerTest.php`

**Interfaces:**
- Consumes: `BonusContractScope::apply($q, 'ad')`.
- Produces:
  - `BonusLedger::AMOUNTS = ['diff_employee' => 'TTHHD', 'commission_month' => 'TNST', 'commission_quarter' => 'TNSQ', 'commission_transport' => 'TVC']`.
  - `BonusLedger::EXCLUDED_INVOICEABLE` (3 class ở Global Constraints).
  - `__construct(?BonusContractScope $scope = null)`.
  - `sums(Request $request, array $groupBy, ?string $contractableType = null): Query\Builder` — `from account_details as ad`, select `$groupBy` + 4 cột tổng, `groupBy($groupBy)`, `havingRaw` 4 cột ≠ 0. Lọc: `start_date`/`end_date` (Y-m-d, áp `ad.invoiceable_date_accounting` từ `00:00:00` tới `23:59:59`), `company_id`, `department_id`, `part_id` (trên `ad.`), `employee_id`, `contract_code` (LIKE `%x%` trên `ad.contractable_code`), scope.

- [x] **Step 1: Viết test** (mã HĐ giả `ZZBONUS-…`, lọc `contract_code` theo tiền tố đó để không dính data thật):
  - `test_co_tru_no_theo_tung_work`: Có 1,000 + Nợ 300 work TTHHD, Có 500 TNST, Có 200 TNSQ, Có 50 TVC → 1 dòng `diff_employee=700, commission_month=500, commission_quarter=200, commission_transport=50`.
  - `test_loai_invoiceable_va_thieu_nv`: dòng `BillPayment` / `ClosingEntry` / `employee_id` NULL / TK khác 3351 không được cộng.
  - `test_bo_nhom_ca_4_cot_bang_0`: Có 100 + Nợ 100 → không có dòng.
  - `test_ky_ngay_bao_ca_ngay_cuoi`: bút toán `end_date 23:30:00` được tính; ngày sau không.
  - `test_loc_nv_va_ma_hd`: `employee_id` chỉ còn số NV đó; `contract_code` khớp gần đúng.
  - `test_gom_theo_cot_truyen_vao`: `groupBy ['ad.contractable_type','ad.contractable_id','ad.contractable_code','ad.employee_id']` → 1 dòng / NV.
- [x] **Step 2:** chạy → FAIL.
- [x] **Step 3:** implement; id work đọc 1 lần (`DB::table('works')->whereIn('code', …)->pluck('id','code')`), work thiếu → cột đó luôn 0 (dùng `-1`), không nổ.
- [x] **Step 4:** chạy → PASS.
- [x] **Step 5:** commit `feat(finance): truy van so 3351 cho bao cao thuong theo hop dong`.

### Task 3: Dòng HĐ — union 3 nguồn

**Files:**
- Create: `Modules/Finance/Services/BonusContractReport/BonusContractReportService.php` (phần dòng HĐ)
- Test: `Modules/Finance/Tests/Feature/BonusContractReportServiceTest.php`

**Interfaces:**
- Consumes: `BonusLedger::sums()`.
- Produces:
  - Hằng `SOURCE_FIRM='firm'`, `SOURCE_WR='wr'`, `SOURCE_HRM='hrm'`, `MORPHS` (source → morph), `PER_PAGE = 10`, `SORTABLE = ['diff_employee','commission_month','commission_quarter','commission_transport','total','commission_sale']`.
  - `contractQuery(Request $request): Query\Builder` — mỗi dòng: `source, contractable_type, contractable_id, contractable_code, customer_id, customer_code, customer_name, department_id, department_name, diff_employee, commission_month, commission_quarter, commission_transport, total, commission_sale`.
  - `sort(Request $request): array{0: string, 1: string}` — cột ∈ `SORTABLE`, chiều ∈ `asc|desc`; ngoài whitelist → `['contractable_code', 'desc']`.

- [x] **Step 1: Viết test** (fixture HĐ giả: 1 `firm_contracts`, 1 `wr_service_contracts` **cùng id** nếu chèn được id trống chung, nếu không thì kiểm theo cặp (type,id); 1 `hrm_contracts`; mỗi HĐ có `department_id`):
  - `test_ba_nguon_moi_nguon_mot_dong`: 3 dòng, `source` đúng, `total` = tổng 4 cột.
  - `test_khach_hang_theo_nguon`: firm → `customers.code` live + `firm_contracts.customer_name`; wr, hrm → `customer_code`/`customer_name` của bảng HĐ.
  - `test_dstc_firm_tu_quyet_toan_type_2`: 2 dòng `firm_settlement_contract_detail` type 2 (100 + 50) + 1 dòng type 1 (999) → `commission_sale = 150`; wr, hrm = 0.
  - `test_hd_khong_phong_bi_loai`: HĐ `department_id` NULL không có trong kết quả.
  - `test_loc_khach_hang`: `customer_id` chỉ còn HĐ của khách đó.
  - `test_trung_id_khac_nguon_khong_gop`: Review Focus 1.
  - `test_sap_xep_whitelist`: `sort_column=total&sort_order=asc` → tăng dần theo total, hoà thì `contractable_id` tăng; `sort_column="foo;drop"` → mặc định `contractable_code` giảm dần.
- [x] **Step 2:** chạy → FAIL.
- [x] **Step 3:** implement: mỗi nhánh = `fromSub(BonusLedger::sums($r, ['ad.contractable_id','ad.contractable_type','ad.contractable_code'], MORPH), 'sub')` INNER JOIN bảng HĐ + `departments d` theo `department_id` của HĐ; firm LEFT JOIN `customers` và subquery DSTC (SVC:248-255); lọc `customer_id` trên bảng HĐ; `unionAll` → `fromSub(…, 'u')` thêm `total`, `orderBy(sort)`, `orderBy('contractable_id')`.
- [x] **Step 4:** chạy → PASS.
- [x] **Step 5:** commit `feat(finance): dong hop dong bao cao thuong theo hop dong`.

### Task 4: Dòng NV dưới HĐ

**Files:**
- Modify: `Modules/Finance/Services/BonusContractReport/BonusContractReportService.php`
- Test: `Modules/Finance/Tests/Feature/BonusContractReportServiceTest.php`

**Interfaces:**
- Produces: `attachEmployees(Request $request, Collection $contracts): Collection` — trả lại `$contracts`, mỗi dòng thêm `employees` (mảng dòng: `employee_id, code, fullname, department_code, department_name, 4 cột, total, commission_sale`). Gọi `BonusLedger::sums()` **1 lần** với `groupBy ['ad.contractable_type','ad.contractable_id','ad.contractable_code','ad.employee_id']`, giới hạn `(contractable_type, contractable_id)` ∈ tập HĐ truyền vào.

- [x] **Step 1: Viết test:**
  - `test_nv_gom_theo_hd_va_nv`: HĐ có 2 NV → 2 dòng, tổng 4 cột của NV cộng lại = dòng HĐ.
  - `test_nv_khong_phong_khong_hien_nhung_tien_van_o_hd`: Review Focus 5.
  - `test_dstc_nv_firm_chi_khi_da_quyet_toan`: `firm_support_accounting_employees` (`commission_sale_percent` 40, `is_main` 1) với HĐ status 10 và DSTC HĐ 150 → NV = 60; đổi status khác 10 → 0; `is_main` 0 → 0.
  - `test_nv_khong_lan_giua_hd_trung_id`: Review Focus 1.
  - `test_sap_xep_nv`: mặc định mã NV tăng dần rồi `employee_id`; `sort_column=total&sort_order=desc` → NV theo total giảm dần.
  - `test_mot_query_cho_ca_trang`: `DB::enableQueryLog()` — số query không tăng theo số HĐ (5 HĐ vs 1 HĐ cùng số query).
- [x] **Step 2:** chạy → FAIL.
- [x] **Step 3:** implement: INNER JOIN `employees e` → `employee_infos ef` (`e.employee_info_id`) → `departments d` (`ef.department_id`); DSTC firm = `percent × commission_sale của dòng HĐ / 100` tính bằng PHP sau khi lấy Σ `commission_sale_percent` theo (HĐ, NV) từ `firm_support_accounting_employees` join `firm_contracts` (`status = 10`, `is_main = 1`, `contractable_type` = firm morph) — 1 query cho cả tập. Sắp xếp bằng PHP theo cùng `sort()` (cột `contractable_code` → dùng `code`).
- [x] **Step 4:** chạy → PASS.
- [x] **Step 5:** commit `feat(finance): dong nhan vien bao cao thuong theo hop dong`.

### Task 5: Controller, route, In, export-rows

**Files:**
- Modify: `Modules/Finance/Services/BonusContractReport/BonusContractReportService.php`
- Create: `Modules/Finance/Services/BonusContractReport/BonusContractPrintTable.php`
- Create: `Modules/Finance/Http/Controllers/V1/BonusContractReportController.php`
- Modify: `Modules/Finance/Routes/api.php` (~L2068)
- Test: `Modules/Finance/Tests/Feature/BonusContractApiTest.php`

**Interfaces:**
- Consumes: `contractQuery()`, `attachEmployees()`, `BonusContractScope::flags()`.
- Produces (prefix `/api/v1/finance/bonus-contract-report`, `auth:api`, không `checkPermission`):
  - `GET /` → `{code, message, data: [HĐ + employees + link], pagination: {current_page, per_page, total, last_page}, summary: {6 cột}}`; `per_page` mặc định 10, tối đa 200.
  - `GET /meta` → `data.permissions` = `flags()`.
  - `GET /export-rows` → `{rows, total, pagination, summary?}` dòng phẳng `row_type` = `contract|employee`, `stt` (`n` / `n.m`); `summary` chỉ trang 1; `per_page|limit` mặc định 2,000, trần 5,000 (khuôn `MonitorContractReportService::exportRows`).
  - `GET /print-list-data` → khuôn `MonitorContractImplementController::printListData` (`LimitsPrintListRows`, `landscape: true`), mẫu 310.
  - Service: `search(Request): array`, `totals(Request): array` (SUM trên `contractQuery()` bằng 1 câu `fromSub`, không lấy hết dòng về PHP), `link(string $source, int $id): array{url, external}` (copy `MonitorContractReportService::link()`: hrm `/assign/contracts/{id}`, wr `/customer-care/wr-service-contracts/{id}`, firm `ERP_URL/admin/sale/firm-contracts/{id}` external).
  - `BonusContractPrintTable::render(Collection $contractsWithEmployees): string` — dòng HĐ in đậm `n`, mã HĐ màu `#0056b3`, KH `mã - tên`, phòng; dòng NV `n.m`, `mã - họ tên`, cột KH trống, tên phòng; ô 0 → `-`; số `number_format($x)`; escape bằng `e()`.
- Validate (FormRequest không cần; `$request->validate` như khuôn): `start_date`, `end_date` **required|date**, `end_date` `after_or_equal:start_date`; `company_id|department_id|part_id|employee_id|customer_id` nullable integer; `contract_code` nullable string max 255; `sort_column`, `sort_order` nullable string (whitelist ở service); `page` min 1.

- [x] **Step 1: Viết test:**
  - `test_thieu_ngay_tra_422` (thiếu 1 trong 2 ngày).
  - `test_phan_trang_10_va_tong_tren_toan_bo`: fixture 12 HĐ → trang 2 có 2 HĐ; `summary` trang 1 = trang 2 = tổng 12 HĐ; NV chỉ trả cho HĐ trong trang.
  - `test_khong_quyen_tong_chi_cua_minh`: NV thường + bút toán của người khác cùng công ty → không có trong `data` lẫn `summary`; gửi `company_id` khác vẫn không nới phạm vi.
  - `test_sort_la_khong_loi`: Review Focus 2 → 200.
  - `test_meta_tra_co_quyen`.
  - `test_export_rows_ghep_trang_bang_ca_tap`: `per_page=3` ghép các trang = dòng phẳng đầy đủ; `stt` dạng `1`, `1.1`.
  - `test_print_list_data_dung_mau_310`: HTML chứa mã HĐ giả, `HEADER` của công ty hồ sơ; 0 dòng → `html` rỗng.
  - `test_link_theo_nguon`.
- [x] **Step 2:** chạy → FAIL.
- [x] **Step 3:** implement + route.
- [x] **Step 4:** chạy cả 4 file test của feature → PASS.
- [x] **Step 5:** đo thời gian 1 năm toàn công ty trên DB local (`curl` có token, hoặc test tạm): `index` và `print-list-data` < 2s; chậm hơn thì `EXPLAIN` và nêu index cần thêm (không tự thêm migration khi chưa hỏi).
- [x] **Step 6:** commit `feat(finance): API bao cao thuong theo hop dong`.

### Task 6: Đối số với ERP

**Files:**
- Create (scratchpad, không commit): script so sánh.
- Modify: `HRM/.plans/bao-cao-thuong-theo-hop-dong/design.md` §6 nếu có lệch.

- [x] **Step 1:** Trên `erp_hrm_check`, tài khoản phạm vi Tổng công ty, chọn ≥ 2 kỳ (vd 01/01–31/03/2026 và 01/07–31/10/2026). Lấy kết quả ERP bằng cách chạy truy vấn SVC tương đương (hoặc gọi route ERP `/bonus-contract-report/searchData` local) và kết quả HRM `GET /` + `/export-rows`.
- [x] **Step 2:** So: TỔNG CỘNG 6 cột, từng HĐ (theo type+id+code) 6 cột, từng NV 6 cột. Kết quả mong đợi: 0 lệch; mọi lệch phải giải thích được bằng design §6, ghi số HĐ lệch + lý do vào design §6.
- [x] **Step 3:** Ghi kết quả đối số (kỳ, số HĐ, số NV, số lệch) vào checkpoint plan.

### Task 7: FE màn + menu + Excel

**Files:**
- Create: `hrm-client/pages/sale/bonus-contract-report/index.vue` (copy khuôn `pages/sale/monitor-contract-implement/index.vue`: `V2BaseSmartFilterPanel`, `V2BaseCompanyDepartmentFilter`, `V2BaseSelectRemote`, `V2BaseTableScroll`, `V2BasePagination`, `ReportPrintPreviewModal` + `reportPrintPreviewMixin`, `filterStateMixin`, `withRequiredErrors`)
- Create: `hrm-client/pages/sale/bonus-contract-report/components/export-excel.js` (khuôn `monitor-contract-implement/components/export-excel.js`)
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:266`

**Interfaces:**
- Consumes: API Task 5 (`const API = 'finance/bonus-contract-report'`).
- Produces: trang tiêu đề `Báo cáo thưởng theo hợp đồng`.

- [x] **Step 1:** Bộ lọc: Từ ngày*, Đến ngày* (`V2BaseDatePicker`, bắt buộc — thiếu thì đỏ ô, không gọi API), Công ty/Phòng ban/Bộ phận (hiện theo `meta.permissions`), Nhân viên (`employeeOptionText`), Khách hàng (remote), Mã HĐ. Nút Lọc, Làm mới; toolbar In, Xuất Excel. Placeholder theo quy tắc floating của CLAUDE.md.
- [x] **Step 2:** Bảng: cột STT · Hợp đồng · Khách hàng · Phòng ban · Thưởng thực hiện hợp đồng · Thưởng năng suất tháng · Thưởng năng suất quý · Tiền vận chuyển còn lại · Tổng cộng · Doanh số tiêu chuẩn. Dòng TỔNG CỘNG đầu bảng; dòng HĐ (chữ thường, không in đậm theo CLAUDE.md — nhấn bằng nền nhạt theo `report-styles`), mã HĐ là link theo `row.link` (`<a :href>` khi external, nuxt-link khi nội bộ); dòng NV thụt lề `n.m`, `mã - họ tên`, cột Phòng = `mã phòng - tên phòng`. Ô 0 hiện `-`. 6 cột số bấm tiêu đề để sắp xếp (gửi `sort_column`/`sort_order`, về trang 1).
- [x] **Step 3:** Excel: gọi `fetchExportRows` lặp trang, dựng file như khuôn; tiêu đề + dòng `Từ ngày … Đến ngày …`; dòng HĐ đậm; số thật `#,##0`; ô 0 để `-` như ERP; tên file `bao_cao_thuong_theo_hop_dong.xlsx`.
- [x] **Step 4:** Menu `sale-hub.js:266` gắn link, KHÔNG khai `codes`/`isShow` (màn không gate, ghi chú 1 dòng như các mục 13/11).
- [x] **Step 5:** Tự kiểm: lệnh grep HTML thô ở CLAUDE.md (mục V2Base) rỗng; grep `vi-VN` cho số rỗng.
- [x] **Step 6:** commit `feat(sale): man bao cao thuong theo hop dong`.

### Task 8: Playwright

**Files:**
- Create: `e2e/tests/bonus-contract-report.spec.ts` (khuôn `e2e/tests/monitor-contract-implement.spec.ts`)

- [x] **Step 1:** Spec: mở `/sale/bonus-contract-report` qua menu; bấm Lọc khi trống ngày → 2 ô ngày đỏ, không có request `/bonus-contract-report?`; chọn kỳ có dữ liệu → bảng có dòng TỔNG CỘNG + dòng HĐ + dòng NV `1.1`; sang trang 2 → TỔNG CỘNG không đổi; bấm tiêu đề `Tổng cộng` → request có `sort_column=total`; In → modal xem trước có bảng; Xuất Excel → tải file `bao_cao_thuong_theo_hop_dong.xlsx`.
- [x] **Step 2:** chạy `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test bonus-contract-report` (API `:8000` + client `:3000` chạy từ worktree) → PASS. Chụp ảnh màn vào scratchpad.
- [x] **Step 3:** đo 2 nút liền nhau cách 12px; console không lỗi.
- [x] **Step 4:** commit spec (repo chứa `e2e/` nếu có git, nếu không thì để file và ghi chú).

### Task 9: Bàn giao

- [x] **Step 1:** cập nhật checkpoint plan + `HRM/.plans/STATUS.md`; ghi chú deploy: chạy `permission:catalog-sync` (thêm `hrm` vào platforms), cấp mã ở `/admin/roles` cho vai trò cần xem rộng.
- [x] **Step 2:** báo user: commit 2 repo, kết quả đối số Task 6, ảnh Playwright; chờ lệnh gộp/push.

## Checkpoint đối số ERP (Task 6, 16/11/2026)

DB local `erp_hrm_check`, phạm vi Tổng công ty, ERP = SQL thuần tương đương (chỉ SELECT) vs `BonusContractReportService` HRM. Script: scratchpad `bonus-parity/compare.php`.

| Kỳ | Số HĐ (ERP/HRM) | Số NV (ERP/HRM) | Lệch tổng 6 cột | Lệch HĐ | Lệch NV |
|---|---|---|---|---|---|
| 01/11/2025 - 31/01/2026 | 4155 / 4155 (hãng 3717, DV 438) | 8396 / 8396 | 0 | 0 | 0 |
| 01/03/2026 - 31/07/2026 | 5572 / 5572 (hãng 5006, DV 566) | 11416 / 11416 | 0 | 0 | 0 |

Không có lệch nên §6 giữ nguyên. HĐ HRM: 0 dòng (đúng kỳ vọng).

## Checkpoint bàn giao (Task 9, 16/11/2026)

- Commit (local, nhánh `feature/bao-cao-thuong-theo-hop-dong`):
  - api: 9ffd391d9 → 377ed5f14
  - client: bd8780d56, 305bc9253, 65a993756
  - e2e: 9d85426
- Final review: 1 Important đã sửa (dòng NV gắn theo cả mã HĐ). Validate ngày `Y-m-d`. Thêm test scope phòng/bộ phận/công ty cho index, export, print.
- Test: Scope 6, Ledger 7, ReportService 14, Api 12 đều pass. Playwright 1 pass.
- Hiệu năng (DB local): 1 tháng toàn cty ~1s. 1 năm ~13-14s (In 5.7-8.9s). Phạm vi cá nhân 1 năm ~13s (employee_id không có index). Muốn nhanh hơn phải thêm covering index hoặc cache, chờ user quyết.
- Deploy:
  1. `php artisan migrate`: index `idx_ad_identify_date_ctype` trên `account_details`, INPLACE/LOCK=NONE.
  2. Reload php-fpm và queue worker (code nhớ tĩnh việc index có tồn tại).
  3. `permission:catalog-sync`, mã `accounting.bao_cao_thuong_theo_hop_dong.view` thêm platform hrm.
  4. Cấp mã ở `/admin/roles` cho vai trò cần xem rộng. Không có mã thì chỉ xem bút toán của mình.
