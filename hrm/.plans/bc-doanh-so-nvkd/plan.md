# BC doanh số theo nhân viên kinh doanh (port ERP → HRM) — Implementation Plan

Người làm: @nguyentrancu97 · Nhánh: hrm-api / hrm-client `develop`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng màn HRM "Báo cáo doanh số theo nhân viên kinh doanh" port từ ERP, cây Phòng ▸ NV ▸ HĐ với 4 cột tiền (chỉ tiêu 1 khớp số ERP), kèm phối hợp tạm tính cột doanh số, sort cột tiền, lọc "Phối hợp bán hàng", form cấp xem NV▸HĐ, và chỉ tiêu 2 chi tiết theo bảng giá.

**Architecture:** BE một service dùng chung `BySalesStaffReportService` (Modules/Finance) song sinh `BonusQuarterReportService`: `rows()` dựng dòng gốc (HĐ×NV) bằng UNION ALL firm + WR trên `account_details`, `tree()` gộp cây, `search()` cắt trang theo dòng gốc (#12205). Phạm vi 4 cấp qua `BySalesStaffScope extends SalesIncomeScope`. Controller V1 mỏng (meta/index/detail/export/print). FE một trang `pages/sale/by-sales-staff-report/` bám `bonus-quarter-report`, `criterion` là dropdown trong bộ lọc (1 = tổng doanh số 3 tầng, 2 = thêm tầng Loại giá). ERP là chuẩn số liệu chỉ tiêu 1; HRM là chuẩn UI.

**Tech Stack:** BE PHP 7.4 / Laravel 8, `Modules/Finance`, query builder thuần (fromSub/unionAll) như sibling; FE Nuxt 2.14 / Vue 2, Bootstrap-Vue, `V2Base*`. Permission Catalog + `permission:catalog-sync`. Excel `maatwebsite/excel` qua export-rows + dựng FE; in qua `report_templates`.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/bc-doanh-so-nvkd/design.md` (plan lập luận từ spec này; executor đọc cả hai).

## Global Constraints

- **Giải id tài khoản theo SỐ HIỆU, KHÔNG hardcode** `[181..187,192]`. Tập TK: **511 + các con 5111..5118 + 5213** (KHÔNG 521 cha, 5211, 5212). `ac.type`: 2 = Có, 1 = Nợ. ⚠️ ĐÃ VERIFY DB (Task 1): bảng `accounts` dùng cột `identify_number`/`identify_number_parent`, là **danh mục TOÀN CỤC — KHÔNG có `company_id`**, mỗi số hiệu đúng 1 dòng dùng chung mọi công ty (511→181, 5111..5118→182-187 (DB thiếu 5115/5116), 5213→192). KHÔNG lọc công ty ở bảng accounts. Helper có sẵn: `BySalesStaffAccounts::revenueAccountIds()` = `Account::selfAndChildIds('511')` + id 5213 (port của `getAccountChild`). **Phân biệt công ty nằm ở `account_details.company_id`/`employee_company_id`/`employee_*`** — scope + lọc công ty áp trên các cột đó, không trên id tài khoản.
- **Số chỉ tiêu 1 phải KHỚP ERP** `BySalesStaffService` trên DB thật (nhiều NV, nhiều công ty). Lệch = hỏng. ERP là chuẩn, KHÔNG sửa ERP khi chưa hỏi user.
- **Phối hợp tạm tính (cột 2) là chỉ tiêu MỚI** — ERP không có. Sau blend cột 2 KHÔNG còn khớp tổng ERP (cố ý). Chỉ cột 1/3/4 + **base cột 2** (trước blend) đối chiếu ERP. `R(C)` = doanh số 511/5213 cả HĐ (mọi employee_id, không khử trùng); `%e` = `commission_sale_percent` cấp NV (`*_support_accounting_employees`, firm + WR). Cộng dồn (không khử trùng với phần trực tiếp).
- **Phân trang #12205**: cắt trang theo DÒNG GỐC (HĐ×NV) TRƯỚC, gộp cây SAU; `summary`/`total` trên TOÀN BỘ rows. Dòng gốc = HỢP (HĐ×NV trực tiếp) ∪ (HĐ×NV chỉ phối hợp).
- **NV thuộc nhánh phòng của chính NV** (hồ sơ nhân sự `ac.employee_department_id` ghi trên bút toán), KHÔNG theo phòng hỗ trợ hạch toán.
- **Định dạng số quốc tế**: `,` nghìn, `.` thập phân. FE `toLocaleString('en-US')`; BE `number_format($x, $p)`. Số thật + numFmt trong Excel.
- **Quyền own-scope không gate màn**: ai cũng vào, không có quyền thì chỉ thấy số của chính mình. Mã Catalog `sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view` (scopes 4 cấp), thêm `hrm` vào `platforms`, `permission:catalog-sync`. KHÔNG seeder, KHÔNG tự gán vai trò.
- **Nhãn "Người tạo"/"Ngày tạo"** (không "Người lập"); bám skill `erp-to-hrm-screen` + `list-page` + SRS cho UI/nút/màu/thông báo.
- **KHÔNG commit/push/gop_db** khi chưa có lệnh user.

## Review Focus

- **Đa công ty**: NV thao tác chéo công ty, hoặc dữ liệu nhiều công ty cùng kỳ — id TK 511/5213 phải giải theo `CurrentCompany::id()`, không rò/nhầm số công ty khác. (Task 1, 3)
- **Kỳ rỗng / không có bút toán**: start_date/end_date không có phát sinh → trả cây rỗng + total 0, không 500, không chia cho 0 ở `%e`. (Task 3, 4)
- **NV không có bộ phận** (`employee_department_id` NULL): dòng không vào cây nhưng vẫn cộng vào `total` (như sibling `tree()` bỏ dòng no-department). (Task 5)
- **Phối hợp `commission_sale_percent` NULL / 0 / tổng ≠ 100**: blend dùng đúng % đang lưu, không tự chuẩn hoá về 100; NULL coi như 0. (Task 4)
- **Chỉ tiêu 2, HĐ thiếu `price_type`**: gom "Chưa xác định", KHÔNG loại → tổng chỉ tiêu 2 = chỉ tiêu 1. (Task 16)

---

## PHA 1 — Chỉ tiêu 1 (Tổng doanh số), đối chiếu khớp ERP

### Task 1: Helper giải id tài khoản 511/5213 theo công ty

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffAccounts.php`
- Test: `hrm-api/Modules/Finance/Tests/Unit/BySalesStaffAccountsTest.php`

**Interfaces:**
- Consumes: `App\Models\...\AccountDetail::getAccountChild()` (pattern ERP dùng cho TK 131); `App\Support\CurrentCompany::id()`.
- Produces: `BySalesStaffAccounts::revenueAccountIds(): array` — trả mảng id các TK 511(+5111..5118)+5213 của công ty đang chọn.

- [x] **Step 1: Đọc gốc** — mở ERP `BySalesStaffService::getActualRevenue()` (~:1626-1653) và `getFirstContractIds()` :122-139 xem `AccountDetail::getAccountChild()` ký hiệu/tham số thật; xác nhận HRM có method tương đương (grep `getAccountChild` trong hrm-api). Nếu HRM chưa có, tra `accounts` theo `code LIKE '511%'` + `code = '5213'` lọc theo `company_id = CurrentCompany::id()`.
- [x] **Step 2: Viết test fail** `test_revenue_account_ids_resolves_511_and_5213_for_current_company`: seed/giả lập 2 công ty có bộ `accounts` khác id cho cùng code 511/5213; assert hàm trả đúng tập id của công ty đang chọn, gồm 5111..5118 và 5213, KHÔNG gồm 521 cha / 5211 / 5212.
- [x] **Step 3: Run test — FAIL** (`php artisan test --filter=BySalesStaffAccountsTest`).
- [x] **Step 4: Implement `revenueAccountIds(): array`** trong `BySalesStaffAccounts.php` theo code số hiệu, lọc theo `CurrentCompany::id()`.
- [x] **Step 5: Run test — PASS.**
- [x] **Step 6: Commit** (`git add` 2 file; message `feat(finance): resolve revenue account ids by number for by-sales-staff report`).

### Task 2: Scope phạm vi 4 cấp

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffScope.php`
- Test: `hrm-api/Modules/Finance/Tests/Unit/BySalesStaffScopeTest.php`

**Interfaces:**
- Consumes: `Modules\Finance\Services\SalesIncome\SalesIncomeScope` (base class, method `level()`, `apply($query, $prefix, $ownColumn)`).
- Produces: `BySalesStaffScope extends SalesIncomeScope` với `const CODE = 'sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view'`.

- [x] **Step 1: Viết test fail** `test_level_maps_permission_scope` + `test_apply_own_filters_by_employee`: mô phỏng `CurrentPermission::scope(CODE)` trả từng mức (GROUP/COMPANY/DEPARTMENT/PART/null) → assert `level()` ra all/company/department/part/own; với own, `apply()` thêm `where('ac.employee_id', auth id)`.
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement** — copy nguyên khuôn `BonusQuarterScope.php` (chỉ đổi `CODE`). Không override `apply()`/`level()`.
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 3: Service — dòng gốc & base 4 cột (khớp ERP)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffReportServiceTest.php`

**Interfaces:**
- Consumes: Task 1 `BySalesStaffAccounts::revenueAccountIds()`, Task 2 `BySalesStaffScope`.
- Produces:
  - `rows(Request $request): Collection` — mỗi item là mảng: `department_id, department_name, employee_id, employee_code, employee_name, contractable_id, contractable_type, contractable_code, customer_code, customer_name` + 4 cột tiền `total_product_before_vat, total_actual_revenue, commission_sale, settlement_commission_sale`. Sắp `department_id, employee_id`.
  - `totals(Collection $rows): array`, `firmQuery(...)`, `wrQuery(...)`, `baseEntries(...)`, `filterAcc(...)` (bố cục bám `BonusQuarterReportService`).

**Chú ý 4 cột (đối chiếu ERP, design §3):** (1) `total_product_before_vat` ← `firm.total_before_vat` (getContractData); (2) `total_actual_revenue` ← công thức 511/5213 (getActualRevenue, base — CHƯA blend); (3) `commission_sale` ← `SUM(fe.commission_sale)` (getSupportAccounting, group HĐ+NV); (4) `settlement_commission_sale` ← `sce.commission_sale` với `sc.status=5`, `fscd.type=2` (getSettlementContract). Cột 2 base dùng `revenueAccountIds()`, `type` 2−1, join HĐ (firm + WR), `whereNotNull contractable_id`, lọc kỳ theo `ac.invoiceable_date_accounting`.

- [x] **Step 1: Đọc gốc** ERP `getContractData` :1554, `getActualRevenue` :1626, `getSupportAccounting` :1770, `getSettlementContract` :1854 + các biến thể; ghi ra 4 biểu thức cột chính xác (bút toán nào, group theo gì).
- [x] **Step 2: Viết test fail** `test_base_actual_revenue_matches_erp_for_known_contract`: chọn 1 HĐ có dữ liệu thật trên `erp_hrm_check`, chạy `rows()` lọc đúng HĐ+kỳ, assert `total_actual_revenue` (base) == kết quả ERP `getActualRevenue` cho cùng HĐ (lấy số ERP qua tinker hoặc hằng đã verify trong test). Thêm `test_four_columns_present_and_numeric`.
- [x] **Step 3: Run test — FAIL.**
- [x] **Step 4: Implement `rows()` + `firmQuery()`/`wrQuery()`/`baseEntries()`/`filterAcc()`** bám bố cục `BonusQuarterReportService`:85-405 (UNION ALL firm+WR, fromSub, scope `apply($q,'ac.employee_')`, filter kỳ/contract_code/customer/company/department/part/employee). Cột 2 dùng `revenueAccountIds()` thay account 117. Cột 1/3/4 join đúng bảng HĐ + support/settlement.
- [x] **Step 5: Run test — PASS** (đối chiếu khớp ERP cho ≥1 HĐ, ≥2 công ty).
- [x] **Step 6: Commit.**

### Task 4: Phối hợp tạm tính — cộng vào cột 2

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffBlendTest.php`

**Interfaces:**
- Produces: `coordinatedRevenue(Request $request): Collection` keyed `(contractable_id, employee_id)` = `R(C) × %e` (gồm firm + WR); `rows()` cộng số hạng này vào `total_actual_revenue` của đúng (HĐ×NV), và **tạo dòng mới** cho (HĐ×NV) chỉ-phối-hợp chưa có ở base.

- [x] **Step 1: Viết test fail** `test_coordinated_adds_estimate_to_participant` (NV tham gia HĐ của người khác → cột 2 có phần `R(C)×%e`), `test_coordinated_creates_row_for_participant_only` (NV chỉ phối hợp → xuất hiện dòng HĐ đó), `test_base_plus_coordinated_may_exceed_real` (cộng dồn, không khử trùng), `test_null_percent_treated_as_zero`.
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement** — `coordinatedRevenue()` join `firm_support_accounting(_departments)_employees` fe + `wr_support_accounting_*` lấy `commission_sale_percent`, nhân với `R(C)` (= base cột 2 toàn HĐ, tổng mọi employee_id trên bút toán của C trong kỳ). Merge vào `rows()`: UNION base ∪ coordinated theo (HĐ×NV); % NULL → 0; `R(C)` lọc TK 511/5213 theo kỳ (không lọc bút toán 131 đầu kỳ).
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 5: Cây 3 tầng + phân trang #12205 + summary/total

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffTreeTest.php`

**Interfaces:**
- Produces: `search(Request): array` (`data` = cây trang hiện tại, `total`, `summary`, `pagination`); `tree(Collection): array` (Phòng ▸ NV ▸ HĐ); `summary(Collection): array`; `detailRows(Request): Collection`.

- [x] **Step 1: Viết test fail** `test_search_paginates_by_base_row_then_groups` (cắt trang trước, gộp cây sau — 1 phòng có thể 2 trang), `test_total_sums_all_rows_including_no_department`, `test_tree_three_levels`.
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement `search`/`tree`/`summary`/`totals`/`detailRows`** bám `BonusQuarterReportService`:54-181 (forPage trước, tree sau; dòng không phòng bỏ khỏi cây nhưng vào total; `AMOUNT_KEYS` = 4 cột tiền của báo cáo này).
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 6: Sort cột tiền tăng/giảm

**Files:**
- Modify: `BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffSortTest.php`

**Interfaces:**
- Produces: `const SORTABLE = ['total_product_before_vat','total_actual_revenue','commission_sale','settlement_commission_sale']`; `sort(Request): array` (default `['contractable_code','desc']`); `rows()` orderBy theo sort, phụ ổn định `contractable_id`.

- [x] **Step 1: Viết test fail** `test_sort_by_money_asc_desc`, `test_invalid_sort_falls_back_default`.
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement `sort()`** bám `BonusContractReportService.php:41,52-61`; áp orderBy vào `rows()` (sort trên dòng gốc trước khi cắt trang/gộp cây).
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 7: Lọc "Phối hợp bán hàng"

**Files:**
- Modify: `BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffCoordinatedFilterTest.php`

**Interfaces:**
- Produces: `filterAcc()` đọc `coordinated` ('1' → chỉ HĐ có ≥1 bản ghi `firm_support_accounting_employees` hoặc `wr_support_accounting_employees`; rỗng = tất cả); `summary`/`total` tính lại trên tập đã lọc.

- [x] **Step 1: Viết test fail** `test_coordinated_filter_keeps_only_contracts_with_support`, `test_empty_filter_returns_all`, `test_summary_recomputed_on_filtered_set`.
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement** — `whereExists` sang bảng support_accounting_employees khi `coordinated='1'`.
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 8: Controller + routes + validate

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BySalesStaffReportController.php`
- Create: `hrm-api/Modules/Finance/Services/BySalesStaff/BySalesStaffPrintTable.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffReportApiTest.php`

**Interfaces:**
- Consumes: Task 3-7 service; Task 2 scope (cho `meta.permissions`).
- Produces endpoints: `GET meta`, `GET index` (phân trang), `GET detail` (1 NV), `GET export` (cả cây, `flat=1` thêm rows), `GET print-data`. Validate `start_date`/`end_date` required `Y-m-d`, `after_or_equal`; `criterion nullable integer`; `coordinated nullable`; `sort_column`/`sort_order nullable`.

- [x] **Step 1: Viết test fail** `test_index_returns_tree_total_summary_pagination`, `test_detail_requires_employee_id`, `test_meta_permissions_flags`, `test_own_scope_sees_only_self` (tài khoản thường, không quyền → chỉ số của mình).
- [x] **Step 2: Run test — FAIL.**
- [x] **Step 3: Implement controller** bám `BonusQuarterReportController.php` (meta/index/detail/export/printListData), route group bám sibling trong `Routes/api.php` (prefix `by-sales-staff-report`, KHÔNG gate vào màn; route thao tác dữ liệu N/A vì chỉ đọc). `BySalesStaffPrintTable::list()` dựng HTML chi tiết.
- [x] **Step 4: Run test — PASS.**
- [x] **Step 5: Commit.**

### Task 9: Mã quyền Catalog

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Catalog/sale.php` (hoặc file Catalog tương ứng — grep mã `bao_cao_doanh_so_theo_nhan_vien_kinh_doanh` trước)

**Interfaces:**
- Produces: mã `sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view` với `scopes` 4 cấp, `platforms` gồm `hrm` (+ `erp` nếu đã có), đúng `subsystem_group`/`subsystem`/`feature`.

- [x] **Step 1:** grep Catalog xem ERP đã khai mã này chưa. Có → thêm `hrm` vào `platforms`. Chưa → thêm mã mới với scopes.
- [x] **Step 2:** chạy `php artisan permission:catalog-sync`; xác nhận mã xuất hiện, `deprecated_at` null.
- [x] **Step 3: Commit** (chỉ file Catalog; KHÔNG seeder).

### Task 10: FE — trang danh sách `index.vue`

**Files:**
- Create: `hrm-client/pages/sale/by-sales-staff-report/index.vue`
- Create: `hrm-client/pages/sale/by-sales-staff-report/api.js`
- Create: `hrm-client/pages/sale/by-sales-staff-report/format.js`

**Interfaces:**
- Consumes: BE endpoints Task 8.
- Produces: trang với `V2BaseSmartFilterPanel floating` (khoảng thời gian, tổ chức qua `V2BaseCompanyDepartmentFilter`, `coordinated`, `criterion`), header actions (Cấu hình cột / In / Xuất Excel), 4 mixin (`PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`), `columnScreenKey = 'sale_by_sales_staff_report'` (duy nhất), `layout: 'default-sidebar'`.

- [x] **Step 1:** copy khung từ `pages/sale/bonus-quarter-report/index.vue`; đổi endpoint/tiêu đề/`columnScreenKey`.
- [x] **Step 2:** thêm field lọc `coordinated` (khuôn `sales-income-summary/index.vue:300-307`) và `criterion` (khuôn `compare-contract-by-time-report/index.vue:283`; Pha 1 để mặc định 1, Pha 2 mở option 2).
- [x] **Step 3: Verify Playwright** — mở `http://127.0.0.1:3000/sale/by-sales-staff-report`, chụp ảnh đặt cạnh `bonus-quarter-report`; đổi ô lọc chờ ≥3s; đếm request (vào màn/đổi trang/sort = 1 request).
- [x] **Step 4: Commit.**

### Task 11: FE — cây `BySalesStaffTable.vue` (Cấp xem + tooltip + sort th)

**Files:**
- Create: `hrm-client/pages/sale/by-sales-staff-report/components/BySalesStaffTable.vue`
- Create: `hrm-client/pages/sale/by-sales-staff-report/components/ReportPagination.vue` (hoặc tái dùng của sibling)

**Interfaces:**
- Consumes: payload `search()` (cây + pagination).
- Produces: cây Phòng▸NV▸HĐ; ô `V2BaseSelect size=xs` "Cấp xem" (Chỉ phòng ban / Đến nhân viên / Đến hợp đồng) — `level` CHỈ client, KHÔNG gửi API; icon info tooltip cạnh tiêu đề "Doanh số xuất hàng"; `th.th-sort` 4 cột tiền phát `sort_column`/`sort_order`.

- [x] **Step 1:** copy `components/BonusQuarterTable.vue` (ô Cấp xem :33,247,260-264), đổi 4 cột tiền + options level.
- [x] **Step 2:** thêm icon info tooltip (skill `info-icon-tooltip`: `ri-information-line` 14px `#94a3b8` + `b-popover custom-class="info-popover"`) câu: *"Doanh số xuất hàng = PS Có 511 − PS Nợ 511 + PS Có 521 − PS Nợ 521 (Đã bao gồm nhập trả lại)"*.
- [x] **Step 3:** sort th bám `bonus-contract-report/index.vue:90-96,297,436-439`.
- [x] **Step 4: Verify Playwright** — bung/thu Cấp xem, hover tooltip, bấm sort tăng/giảm (mũi tên đổi chiều, đổi cột huỷ cột cũ).
- [x] **Step 5: Commit.**

### Task 12: FE — Xuất Excel + Bản in

**Files:**
- Create: `hrm-client/pages/sale/by-sales-staff-report/components/export-excel.js`
- Create: `hrm-client/pages/sale/by-sales-staff-report/print.vue` (nếu sibling có trang in riêng) hoặc modal preview

**Interfaces:**
- Consumes: `export` (cả cây, số thật), `print-data` (HTML template).
- Produces: Excel cột = 4 cột tiền + tổ chức/HĐ/khách, **số thật + numFmt `#,##0`** (không chuỗi format sẵn); bản in khổ ngang bám `BonusQuarterPrintTable`.

- [x] **Step 1:** copy `components/export-excel.js` + luồng in của `bonus-quarter-report`; map 4 cột.
- [x] **Step 2: Verify** — xuất file mở SUM ra số (không "number stored as text"); mở print preview có khung tờ giấy xám `#eee`.
- [x] **Step 3: Commit.**

### Task 13: FE — modal drill-down (type 1–4)

**Files:**
- Create: `hrm-client/pages/sale/by-sales-staff-report/components/BySalesStaffDetailModal.vue`

**Interfaces:**
- Consumes: `detail` endpoint (1 NV → dòng HĐ phẳng).
- Produces: modal bấm vào ô số của NV → bảng HĐ chi tiết; dùng `V2BaseModal` + `V2BaseSelectInModal` nếu có select.

- [x] **Step 1:** đọc ERP `bySalesStaffSearch()` :6487 (4 nhánh type) xác định mỗi type là drill cột nào; bám `BonusQuarterDetailModal.vue`.
- [x] **Step 2: Implement** modal + wiring từ cây.
- [x] **Step 3: Verify Playwright** — bấm ô số, modal hiện đúng HĐ, tổng modal = số đã bấm.
- [x] **Step 4: Commit.**

### Task 14: Menu + slug

**Files:**
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js` (+ grep các file menu khác: `subsystem-menu/*.js`, `default-menu/*.js`, `menu.js`, `menu-sidebar.js`)

**Interfaces:**
- Produces: mục menu "Báo cáo doanh số theo nhân viên kinh doanh" trỏ `/sale/by-sales-staff-report`, `codes: ['sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view']`.

- [x] **Step 1:** xác định vị trí theo **sheet quy hoạch phân hệ** (menu ERP tham chiếu: `grep "route('...bySalesStaff...'" topmenubar.blade.php`). Giữ tham số link nếu ERP có nhiều lối vào.
- [x] **Step 2:** đổi `erpPath`→`link` (hoặc thêm mục `{n,link}`) trong `sale-hub.js`; khai `codes`. Kiểm mục có sẵn trước khi thêm mới.
- [x] **Step 3: Verify** — menu hiện đúng chỗ, bấm vào đúng màn; tài khoản không quyền vào URL → 404.
- [x] **Step 4: Commit.**

### Task 15: Đối chiếu số ERP + e2e (chốt Pha 1)

**Files:**
- Create: `HRM/e2e/tests/by-sales-staff-report.spec.ts`

- [x] **Step 1: Đối chiếu số** — chọn ≥3 NV ở ≥2 công ty + vài kỳ; so cột 1/3/4 + base cột 2 HRM == ERP `BySalesStaffService` (tinker/curl cả hai). Ghi bảng đối chiếu vào STATUS. Lệch → systematic-debugging, ERP là chuẩn.
- [x] **Step 2: e2e** (Node 20) — lọc kỳ + tổ chức, bung cây, sort cột tiền, lọc Phối hợp=Có, mở drill modal, xuất Excel 200, print-data 200. Chạy thật `cd e2e && PATH=".../v20.../bin:$PATH" npx playwright test by-sales-staff-report`.
- [x] **Step 3: Commit.**

---

## PHA 2 — Chỉ tiêu 2 (Chi tiết theo bảng giá)

### Task 16: BE — tầng Loại giá

**Files:**
- Modify: `BySalesStaffReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BySalesStaffPriceTierTest.php`

**Interfaces:**
- Produces: `rows()` gắn `price_type_id`/`price_type_name`/`price_type_order` (từ `firm_contracts.price_type`/`service_contracts.price_type` → `price_types`); `tree()` nhận `criterion` (2 → chèn tầng Loại giá: Phòng▸NV▸Loại giá▸HĐ).

- [x] **Step 1: Verify DB** — `firm_contracts.price_type`, `service_contracts.price_type`, bảng `price_types` (+ cột `order`) tồn tại trong `erp_hrm_check`. Nếu khác → điều chỉnh plan, báo ruling.
- [x] **Step 2: Viết test fail** `test_criterion_2_inserts_price_type_tier`, `test_missing_price_type_grouped_as_undetermined`, `test_criterion_2_total_equals_criterion_1`, `test_price_tier_ordered_by_price_types_order`.
- [x] **Step 3: Run — FAIL.**
- [x] **Step 4: Implement** — join `price_types`; `tree()` thêm 1 cấp khi `criterion=2`; HĐ thiếu price_type → nhóm "Chưa xác định" (không loại); order theo `price_types.order`.
- [x] **Step 5: Run — PASS.**
- [x] **Step 6: Commit.**

### Task 17: FE — dropdown Chỉ tiêu + "Đến loại giá"

**Files:**
- Modify: `index.vue`, `components/BySalesStaffTable.vue`

**Interfaces:**
- Produces: `criterion` dropdown mở option 2 ("Chi tiết theo bảng giá"); `criterion=2` → `level` thêm mục "Đến loại giá" xen giữa NV và HĐ; cây render 4 tầng.

- [x] **Step 1:** mở option `criterion=2` ở bộ lọc; truyền `criterion` xuống API.
- [x] **Step 2:** `BySalesStaffTable.vue` render tầng Loại giá khi `criterion=2`; thêm level option "Đến loại giá".
- [x] **Step 3: Verify Playwright** — đổi Chỉ tiêu 2, cây 4 tầng, nhóm "Chưa xác định" hiện; tổng chỉ tiêu 2 = chỉ tiêu 1.
- [x] **Step 4: Commit.**

---

## Self-review (đã chạy)

1. **Spec coverage:** §5.1 (A1 criterion) → Task 10/16/17; §5.2 (B2) → Pha 1 trước Pha 2; §5.3 (form) → Task 11; §5.4a blend → Task 4; §5.4b tooltip → Task 11; §5.4c sort → Task 6/11; §5.4d filter → Task 7; §4 account-by-number → Task 1; #12205 → Task 5; quyền → Task 2/9; drill → Task 13; menu/Excel/in → Task 12/14. Đủ.
2. **Review Focus:** đa công ty (T1/T3), kỳ rỗng (T3/T4), NV không phòng (T5), % NULL (T4), thiếu price_type (T16) — mỗi cái có test ở task sở hữu.
3. **Type nhất quán:** 4 cột tiền một tên xuyên suốt `total_product_before_vat/total_actual_revenue/commission_sale/settlement_commission_sale`; `SORTABLE`=4 cột đó; `level` client-only; `criterion` 1/2.
4. **Proportion:** plan dài hơn spec nhưng phần lớn là test name + signature + con trỏ sibling, không transcribe code — hợp lệ cho port project 17 task.

---

## Task 18 (phụ, phát sinh khi chạy T16/T17): export/in nhận `criterion`, bỏ workaround FE

- [x] BE `export`/`print-list-data` nhận `criterion`, bản in có tầng Loại giá (hrm-api `065191318`).
- [x] FE bỏ workaround `flat`/`withPriceTypes`, dùng cây loại giá BE trả (hrm-client `7b136316f`); Excel chỉ tiêu 2 xuất đủ tầng Loại giá + HĐ (`0caac349c`).

### Checkpoint — 2026-11-23 17:15 (wrap up tự động)
Vừa hoàn thành: brainstorm → design.md (chốt A1 + B2, PA cộng dồn + 7 điểm tự quyết, 09:52) → plan 17 task → subagent-driven trọn 18 task (thêm T18) → final review opus ĐẠT (0 Critical · 0 Important · 5 Minor giữ lại). Bộ test `BySalesStaff*` 29 passed (cả trên cây đã merge). e2e `HRM/e2e/tests/by-sales-staff-report.spec.ts` xanh (repo e2e riêng, nhánh `main`, commit local).
Quyết định đã chốt trong ngày: (1) TK doanh số = 511 (+con) + 5213 đúng ERP, không lấy trọn 521; (2) phối hợp tạm tính = CỘNG DỒN `R(C) × %e` (`commission_sale_percent`) vào cột 2, cả firm + WR — cột 2 cố ý lệch ERP, chỉ base cột 2 + cột 1/3/4 đối chiếu ERP; (3) "bảng giá" = `price_type` cấp HĐ, chỉ tiêu 2 = Phòng▸NV▸Loại giá▸HĐ, HĐ thiếu loại giá/WR → "Chưa xác định"; (4) 1 màn, "Chỉ tiêu" là dropdown (A1), làm chỉ tiêu 1 trước (B2); (5) commit thẳng `develop`.
Ruling khi chạy: `accounts` là danh mục toàn cục (không company_id); cột 4 dùng `ANY_VALUE` như ERP; sort mặc định giữ `department_id→employee_id`; T15 phát hiện cột 2 lọc công ty theo NV thay vì công ty HĐ → sửa sang `c.company_id`/`c.part_id` (api `6b0e8bb9b`), recon khớp 5 công ty; lỗi lề thừa 3 nút `#header-actions` (client `ba9b3eb2e`); bản in kỳ rộng bị chặn trần 2.000 dòng là đúng thiết kế.
Commit (nhánh `develop`, ĐÃ push origin): hrm-api `7eafd97f2..065191318` (13 commit) + merge `929d92613`; hrm-client `99489ddd4..7b136316f` (10 commit, bị phiên #12205 rebase lại — nội dung đủ trên `origin/develop`). Quyền `sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view` bật `hrm` (api `f8c2cdb4c`). CHƯA gop_db.
Đang làm dở: không. Workspace SDD còn ở `bc-doanh-so-nvkd/sdd/` (44 file) — chưa dọn, KHÔNG đưa vào commit config.
Bước tiếp theo: khi user báo "gop_db" → đưa sang gop_db + seed quyền/`permission:catalog-sync` trên môi trường đích; sau đó dọn `sdd/`. Minor nên làm khi có nhịp: `ReportInfoTip` trong `th` sortable thiếu `@click.stop` (T11-M1); modal "Tổng cộng" dùng `money()` 0→"0" lệch bảng 0→"-" (T13-M1); perf subquery R(C) kỳ dài; test phủ sâu hơn. Ca e2e caret 3 tầng flaky do header `.logo-box` che chuột.
Blocked:
