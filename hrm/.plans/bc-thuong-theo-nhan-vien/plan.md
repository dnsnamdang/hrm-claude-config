# Báo cáo thưởng theo nhân viên (ERP → HRM) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Màn HRM `/sale/bonus-business-employee` (bảng phòng → NV, popup theo HĐ, In, Excel) cho cùng số với màn ERP `report.bonusBusinessEmployee` sau khi ERP được vá 3 lỗi.

**Architecture:** hrm-api: 1 scope class (con của `SalesIncomeScope`, đổi mã quyền), 1 service tính số bằng SQL trên `account_details` + `employee_infos`/`departments`, 1 class dựng bảng in, 1 controller 5 endpoint ở module Finance. hrm-client: 1 trang + 1 popup + 1 file Excel, bám màn `/sale/sales-income-summary`. ERP (`develop_02`): vá `BonusBusinessEmployeeReportService` + view, dùng cùng luật phạm vi.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), Laravel 6 + Blade/AngularJS 1.3.9 (ERP), PHPUnit, Playwright.

**Spec:** `HRM/.plans/bc-thuong-theo-nhan-vien/design.md`

## Global Constraints

- Nguồn số: `account_details.account_id = 117`; `invoiceable_type NOT IN` (BillPayment, BillPaymentAuthorization, ClosingEntry — chuỗi class ERP `App\Model\IncomeExpenditure\…`, copy đúng chuỗi từ `use` ở đầu file service ERP); `contractable_id`, `employee_id` NOT NULL.
- Cột = Σ`money_value_exchange` type 2 − Σ type 1 theo work code: `TTHHD` → `diff_employee`, `TNST` → `commission_month`, `TNSQ` → `commission_quarter`. Id work tra `works.code`, không hard-code.
- `total` = `diff_employee + commission_month + commission_quarter`. Bỏ NV có cả 3 cột = 0.
- Lọc ngày `invoiceable_date_accounting` ∈ [start 00:00:00, end 23:59:59]; HRM tham số `start_date`, `end_date` (Y-m-d), cả 2 bắt buộc.
- Xếp NV theo `employee_infos.department_id` (nối `employees.employee_info_id`), phòng `departments.status = 1`. NV không có phòng active thì không hiện, không vào tổng.
- Phân trang theo phòng, 10 phòng/trang. STT phòng `n`, NV `n.m`. Số 0 hiện `-` (riêng cột Tổng cộng của dòng luôn hiện số, như ERP).
- Mã quyền: `sale.bao_cao_thuong_theo_nhan_vien.view` (scopes 1-4). Màn không gate; không quyền = chỉ số của mình (`account_details.employee_id = auth()->id()`).
- Phạm vi áp theo tổ chức HIỆN TẠI của NV (`employee_infos.company_id/department_id/part_id`), không theo cột tổ chức trên bút toán.
- Popup gom theo (`contractable_type`, `contractable_id`).
- In dùng `report_templates.id = 309`, khổ ngang, biến `CHI_TIET`, `NGAY`, `THANG`, `NAM`, `TU_NGAY`, `DEN_NGAY`, `HEADER`. Không sửa mẫu 309.
- Excel: tiêu đề "Báo cáo thưởng theo nhân viên", tên file `bao_cao_thuong_theo_nhan_vien.xlsx`, ô số là số thật + `#,##0`.
- Số theo chuẩn quốc tế (`number_format($x)` / `toLocaleString('en-US')`).
- Commit chỉ khi user cho phép; message kết thúc `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. HRM nhánh `develop`, ERP nhánh `develop_02`.

## Rulings đã chốt khi lên plan (ghi lại để reviewer khỏi hỏi)

- **R1 — Scope class:** `BonusEmployeeScope extends SalesIncomeScope`, chỉ đổi `CODE`. Để được vậy, trong `SalesIncomeScope::level()` đổi `self::CODE` → `static::CODE` (1 chữ, hành vi màn thu nhập BH không đổi; test `SalesIncomeScopeTest` phải vẫn xanh). Cấp bộ phận vì thế = bộ phận của mình + bộ phận mình quản lý (như `SalesIncomeScope`); ERP vá theo cùng luật.
- **R2 — Lọc Bộ phận lọc tới NV:** ERP chọn bộ phận thì hiện cả phòng chứa bộ phận đó (chỉ `whereHas('parts')`). HRM lọc `employee_infos.part_id = part_id`; ERP vá cùng (lỗi thứ 4, cùng họ lỗi 3 — báo user khi bàn giao).
- **R3 — In/Excel = toàn bộ kết quả**, không chỉ trang đang xem (ERP `printListData` nhận paginator nên chỉ in trang hiện tại). ERP vá: print/export truyền toàn bộ `$data` thay vì trang.

## Review Focus

1. Người cấp Phòng ban là thành viên của một phòng KHÔNG quản lý → chỉ thấy dòng của chính mình trong phòng đó, không thấy đồng nghiệp (ERP cũ lộ cả phòng). Test: `test_department_scope_hides_colleagues_in_unmanaged_own_department` (Task 2).
2. Gọi popup với `employee_id` ngoài phạm vi → rỗng, kể cả tên NV không lộ. Test: `test_detail_out_of_scope_returns_empty` (Task 3).
3. HĐ hãng và HĐ DV trùng `contractable_id` → 2 dòng popup, mã/KH đúng loại. Test: `test_detail_splits_same_id_different_type` (Task 2).
4. Bút toán có `contractable_type` lạ (không thuộc 3 loại) → popup vẫn hiện số, mã HĐ/KH rỗng, không 500. Test: `test_detail_unknown_contract_type_keeps_amount` (Task 2).
5. Bút toán chỉ có bên Nợ (số âm) → dòng vẫn hiện với số âm, không bị `having` loại. Test: `test_negative_only_row_is_kept` (Task 2).

---

### Task 1: ERP — vá service, controller, view (develop_02)

**Files:**
- Modify: `ERP/TanPhatDev/app/Services/Reports/BonusBusinessEmployeeReportService.php` (`bonusBusinessEmployeeSearchData`, `getDataDepartment`, `renderDataBonusBusinessDepartments`, `getDetailByEmployee`)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/ReportController.php:2134-2160` (print/export truyền toàn bộ data — R3), `:4334` (`getDetailByEmployee` — kiểm phạm vi)
- Modify: `ERP/TanPhatDev/resources/views/reports/bonus_business_employee.blade.php:~195` (ô tổng quý)
- Test: `ERP/TanPhatDev/tests/Feature/BonusBusinessEmployeeReportTest.php`

**Interfaces:**
- Produces: `BonusBusinessEmployeeReportService::scopeLevel(string $code): string` trả `all|company|department|part|own` từ `auth()->user()->permissionScope($code)`; `::employeeInScope(int $employeeId, array $codes): bool` (true nếu NV trong phạm vi của ÍT NHẤT 1 mã). `bonusBusinessEmployeeSearchData($request)` trả thêm khoá `all` = Collection toàn bộ phòng (cho print/export).

- [x] **Step 1: Viết test fail** (`DatabaseTransactions`, fixture năm 2099, dựng tay bút toán TK117 + 2 HĐ firm/wr cùng id nếu dựng được, NV A/B cùng phòng):
  - `test_search_uses_rbac_scope_not_legacy_names` — NV chỉ có quyền tên cũ "Xem báo cáo chi phí bán hàng theo nhân viên của công ty", không có mã RBAC → chỉ thấy chính mình.
  - `test_department_scope_hides_colleagues_in_unmanaged_own_department` — A cấp Phòng ban (scope 2), quản lý phòng X, là thành viên phòng Y; B ở Y có thưởng → kết quả phòng Y chỉ có A.
  - `test_part_filter_narrows_to_part_members` — lọc `part_id` → chỉ NV có `employee_infos.part_id` đó.
  - `test_detail_groups_by_type_and_id` — HĐ firm id=N và HĐ wr id=N cùng NV → 2 dòng.
  - `test_detail_out_of_scope_returns_empty` — A không quyền gọi `report.getDetailByEmployee` với `employee_id = B` → `data` rỗng.
  - `test_detail_allowed_by_contract_report_code` — A chỉ có `accounting.bao_cao_thuong_theo_hop_dong.view` scope 4 → xem được B.
- [x] **Step 2: Chạy** `cd ERP/TanPhatDev && vendor/bin/phpunit tests/Feature/BonusBusinessEmployeeReportTest.php` → FAIL.
- [x] **Step 3: Sửa service.** Bỏ 4 `can('Xem báo cáo chi phí…')`; cờ lấy từ `scopeLevel('sale.bao_cao_thuong_theo_nhan_vien.view')`. Phạm vi lọc ở mức THÀNH VIÊN (closure `members` + `whereHas('members')`), không ở mức phòng: company → `employee_infos.company_id` = công ty đang chọn (`current_company_role` nếu Employee ERP có, không thì `info->company_id`) OR chính mình; department → `department_id` ∈ `EmployeeManageDepartment` của mình OR chính mình; part → `part_id` ∈ {bộ phận mình + bộ phận mình quản lý (bảng HRM `listManagePartIds()` đọc — tra `hrm-api/app/Helper/PermissionHelper.php:238`)} OR chính mình; own → chính mình. Lọc `part_id` áp lên member (R2). `getDetailByEmployee`: `groupBy('contractable_type','contractable_id')`; đầu hàm `if (!employeeInScope($request->employee_id, ['sale.bao_cao_thuong_theo_nhan_vien.view','accounting.bao_cao_thuong_theo_hop_dong.view'])) return collect();`.
- [x] **Step 4: Sửa controller** print/export dùng `$data['all']` (R3); view ô tổng quý kiểm `total_.commission_quarter`.
- [x] **Step 5: Chạy lại test** → PASS. Chạy cả `tests/Feature` của ERP liên quan báo cáo → không vỡ thêm.
- [x] **Step 6: Playwright ERP** — mở `report.bonusBusinessEmployee`, lọc 1 khoảng ngày có số, mở popup 1 NV, In, Excel: không lỗi JS, ô tổng quý hiện số khi tháng = 0. Màn "Báo cáo thưởng theo hợp đồng" mở popup vẫn ra.
- [x] **Step 7: Commit** (khi user cho) `fix(report): BC thưởng theo NV — RBAC scope theo NV, popup gom type+id, kiểm quyền popup, in/excel toàn bộ`.

### Task 2: HRM BE — scope + service

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/SalesIncome/SalesIncomeScope.php` (`self::CODE` → `static::CODE` — R1)
- Create: `hrm-api/Modules/Finance/Services/BonusEmployee/BonusEmployeeScope.php`
- Create: `hrm-api/Modules/Finance/Services/BonusEmployee/BonusEmployeeReportService.php`
- Create: `hrm-api/Modules/Finance/Tests/Feature/Concerns/GrantsBonusEmployeeScope.php` (khuôn `GrantsSalesIncomeScope`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusEmployeeReportServiceTest.php`

**Interfaces:**
- Produces:
  - `BonusEmployeeScope extends SalesIncomeScope { const CODE = 'sale.bao_cao_thuong_theo_nhan_vien.view'; }` — dùng `->level()`, `->apply($q, 'ei.', 'e.id')`.
  - `BonusEmployeeReportService::rows(Request $r): Collection` — mỗi phần tử `['department_id','department_code','department_name','employee_id','employee_code','employee_name','diff_employee','commission_month','commission_quarter','total']` (float), sắp `department_code`, rồi `employee_code`.
  - `::tree(Collection $rows): array` — `[['department_id','department_code','department_name','diff_employee','commission_month','commission_quarter','total','employees'=>[...rows]]]`.
  - `::totals(Collection $rows): array` — 4 khoá số.
  - `::search(Request $r): array` — `['data'=>tree trang hiện tại,'total'=>totals(toàn bộ),'pagination'=>['current_page','per_page','total','last_page']]`, `per_page` mặc định 10, tính theo phòng.
  - `::detailRows(Request $r): Collection` — phần tử `['contractable_type','contractable_id','contract_code','customer_code','customer_name','employee_code','employee_name', 3 cột,'total']`; NV ngoài phạm vi → rỗng.
  - Bộ lọc request: `start_date`, `end_date`, `company_id`, `department_id`, `part_id`, `employee_id` (popup).

- [x] **Step 1: Viết test fail** (`DatabaseTransactions`, fixture 2099 + `uniqid()`, bám setUp của `SalesIncomeSummaryApiTest`):
  - `test_rows_sum_three_works_credit_minus_debit` — 1 NV, TTHHD Có 300 Nợ 100, TNST Có 50, TNSQ Có 20 → `diff_employee=200, commission_month=50, commission_quarter=20, total=270`.
  - `test_excludes_payment_and_closing_vouchers` — dòng `invoiceable_type` = BillPayment → không cộng.
  - `test_negative_only_row_is_kept` — chỉ Nợ TNST 40 → `commission_month = -40`, dòng có mặt.
  - `test_employee_without_active_department_is_hidden` — phòng `status=0` → không có trong `rows`, không vào `totals`.
  - `test_scope_levels` — data provider 4 cấp + không quyền với A (người xem) / B (cùng phòng) / C (khác công ty): all thấy A,B,C; company thấy A,B; department (quản lý phòng A,B) thấy A,B; part (cùng bộ phận với B) thấy A,B; none thấy A.
  - `test_department_scope_hides_colleagues_in_unmanaged_own_department` — như Task 1.
  - `test_part_filter_narrows_to_part_members`.
  - `test_search_paginates_by_department_and_totals_cover_all` — 12 phòng có số, `page=2` → 2 phòng, `total` = tổng 12 phòng.
  - `test_detail_splits_same_id_different_type` — firm id=N, wr id=N → 2 dòng, `contract_code` mỗi dòng đúng mã bảng của nó.
  - `test_detail_hrm_contract_reads_code_and_customer` — `contractable_type = 'Modules\Assign\Entities\Contract\Contract'` (copy hằng `TYPE_HRM_CONTRACT` ở `BillProductivitySettlementQuarterCalculator.php:37`) → `contract_code = hrm_contracts.code`, `customer_code/name` từ `customers.code/fullname`.
  - `test_detail_unknown_contract_type_keeps_amount` — type `'Foo\Bar'` → số có, `contract_code = ''`.
  - `test_detail_out_of_scope_returns_empty`.
- [x] **Step 2: Chạy** `cd hrm-api && vendor/bin/phpunit Modules/Finance/Tests/Feature/BonusEmployeeReportServiceTest.php` → FAIL (class chưa có).
- [x] **Step 3: Implement.** Một câu SQL tổng hợp `account_details` theo `employee_id` (subquery), JOIN `employees e` → `employee_infos ei` → `departments d (status=1)`; scope `apply($q,'ei.','e.id')`; lọc `ei.company_id/department_id/part_id`. `detailRows`: gom theo type+id, rồi LEFT JOIN 3 bảng HĐ theo đúng type (`CASE`/3 join có điều kiện type) + `customers` — không N+1. Kiểm phạm vi popup bằng cùng truy vấn `rows` có `employee_id` (rỗng → trả rỗng).
- [x] **Step 4: Chạy test** → PASS; chạy `Modules/Finance/Tests/Feature/SalesIncomeScopeTest.php` + `SalesIncomeSummaryApiTest.php` → vẫn PASS (R1).
- [x] **Step 5: Commit** `feat(finance): service BC thưởng theo nhân viên (port ERP)`.

### Task 3: HRM BE — controller, routes, in

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BonusBusinessEmployeeController.php` (khuôn `SalesIncomeSummaryController`)
- Create: `hrm-api/Modules/Finance/Services/BonusEmployee/BonusEmployeePrintTable.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (sau khối `sales-income-summary` ~dòng 2058)
- Modify: `hrm-api/app/Support/Permissions/Catalog/sale.php:840` — thêm `'hrm'` vào `platforms` nếu chưa có
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusBusinessEmployeeApiTest.php`

**Interfaces:**
- Consumes: Task 2 service + scope.
- Produces (prefix `/api/v1/finance/bonus-business-employee`):
  - `GET /meta` → `data.permissions = {is_all_company,is_company,is_department,is_part}` (cộng dồn như `unitPermissions`).
  - `GET /` → `{code, message, data, total, pagination}` từ `search()`.
  - `GET /detail?employee_id=` → `{data: {rows, total}}`.
  - `GET /export` → `{data: {tree, total}}` toàn bộ.
  - `GET /print-list-data` → payload `printListPayload($html,$count)` + `landscape: true`, mẫu 309.
  - `BonusEmployeePrintTable::list(array $tree, array $totals): string` — HTML cùng cột/chữ tiêu đề với ERP `printListData` (STT · Nhân viên · Thưởng thực hiện hợp đồng · Thưởng năng suất tháng · Thưởng năng suất quý · Tổng cộng; dòng Tổng cộng trong `thead`), escape bằng `htmlspecialchars`, số `number_format`.

- [x] **Step 1: Viết test fail:**
  - `test_requires_both_dates` — thiếu `end_date` → 422.
  - `test_meta_flags_follow_scope` — scope 3 → `is_company=true,is_all_company=false,is_part=true`.
  - `test_index_returns_tree_and_totals` — khớp số fixture Task 2.
  - `test_detail_out_of_scope_returns_empty` — A không quyền, `employee_id=B` → `rows=[]`.
  - `test_print_uses_template_309_landscape` — `landscape=true`, html chứa `Thưởng năng suất quý` và mã NV fixture.
  - `test_export_is_not_paginated` — 12 phòng → `tree` 12 phần tử.
- [x] **Step 2: Chạy** `vendor/bin/phpunit Modules/Finance/Tests/Feature/BonusBusinessEmployeeApiTest.php` → FAIL.
- [x] **Step 3: Implement** controller + routes + print table. `NGAY/THANG/NAM` = hôm nay; `HEADER` = `companies.header` của `current_company_role` (khuôn `dateVariables`).
- [x] **Step 4: Chạy test** → PASS.
- [x] **Step 5: Commit** `feat(finance): API BC thưởng theo nhân viên`.

### Task 4: HRM FE — trang, popup, Excel, menu

**Files:**
- Create: `hrm-client/pages/sale/bonus-business-employee/index.vue` (khuôn `pages/sale/sales-income-summary/index.vue`)
- Create: `hrm-client/pages/sale/bonus-business-employee/components/BonusEmployeeDetailModal.vue` (`V2BaseModal`, khuôn `SalesIncomeDetailModal.vue`)
- Create: `hrm-client/pages/sale/bonus-business-employee/components/export-excel.js`
- Create: `hrm-client/pages/sale/bonus-business-employee/print.vue` nếu màn mẫu in qua trang `print.vue` riêng (bám đúng cách `sales-income-summary` in)
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:266` — `'Thưởng theo nhân viên'` → `{ n: 'Thưởng theo nhân viên', link: '/sale/bonus-business-employee' }`
- Test: `e2e/tests/bonus-business-employee.spec.ts`

**Interfaces:**
- Consumes: API Task 3.

- [x] **Step 1: Đọc skill** `erp-to-hrm-screen`, `report-styles`, `export-excel`, `print-page`, `modal-popup` trước khi code.
- [x] **Step 2: Viết spec Playwright fail:**
  - mở `/sale/bonus-business-employee`, chưa chọn ngày bấm Lọc → báo lỗi dưới ô ngày, không gọi API index.
  - chọn khoảng ngày có số → dòng "Tổng cộng" đầu bảng; dòng phòng hiện `mã - tên` KHÔNG phải link; dòng NV STT dạng `1.1`.
  - bấm tên NV → popup có cột Hợp đồng, Khách hàng, 3 cột thưởng, Tổng cộng và dòng tổng.
  - Xuất Excel → tải file `bao_cao_thuong_theo_nhan_vien.xlsx`.
  - In → mở trang in khổ ngang có bảng.
- [x] **Step 3: Chạy** `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test bonus-business-employee` → FAIL.
- [x] **Step 4: Implement.** Bộ lọc Công ty/Phòng ban/Bộ phận hiện theo cờ `meta.permissions`; Từ/Đến ngày bắt buộc; nút Lọc · Làm mới · In · Xuất Excel (`mr-2 mb-2`). Số 0 → `-`. Excel FE từ `/export`.
- [x] **Step 5: Chạy spec** → PASS; tự kiểm `grep` V2Base + `vi-VN` theo CLAUDE.md → rỗng.
- [x] **Step 6: Commit** `feat(sale): màn BC thưởng theo nhân viên`.

### Task 5: Đối chiếu số HRM ↔ ERP

**Files:**
- Create: `HRM/.plans/bc-thuong-theo-nhan-vien/doi-chieu.md` (kết quả)

- [x] **Step 1:** Trên DB `erp_hrm_check`, cùng 1 người xem scope 4, chọn 2 khoảng ngày (1 tháng gần nhất có cả FirmContract + WrServiceContract; 1 quý). Gọi ERP `report.bonusBusinessEmployeeSearchData` (sau vá) và HRM `/export`; so từng `(department_id, employee_id)` 3 cột + `total`.
- [x] **Step 2:** Tìm 1 NV có HĐ hãng và HĐ DV trùng `contractable_id` (SQL `GROUP BY employee_id, contractable_id HAVING COUNT(DISTINCT contractable_type) > 1`); so popup 2 bên.
- [x] **Step 3:** Ghi `doi-chieu.md`: số dòng, số lệch (phải = 0), NV mẫu đã so. Lệch ≠ 0 → quay lại Task 1/2, không bàn giao.
- [x] **Step 4:** Cập nhật `STATUS.md`; ghi chú deploy: `permission:catalog-sync` nếu sửa `platforms`.

### Checkpoint — 2026-11-16
Vừa hoàn thành: Task 1–5 + vòng sửa sau final review (ERP C1/I1 3b12c02bdd; client M2/M5 315c91c20). e2e pass, đối chiếu 0 lệch.
Đang làm dở: không.
Bước tiếp theo: user chọn cách bàn giao (merge develop / develop_02 hay giữ nhánh). Chưa push, chưa gop_db.
Blocked:
Commit: ERP feat/… 0d5743c1ae, 3b12c02bdd · hrm-api 531071b34, 0f6dc1bb2 · hrm-client 075aa72b8, a07b59d2f, 315c91c20 · e2e main f255469.
