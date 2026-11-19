# Bảng tổng hợp thu nhập từ bán hàng (port ERP) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP `report.commission_settlement_quarter` sang HRM bám 1:1, gộp 2 cột DSTC tháng/quý thành 1 cột "DSTC quyết toán".

**Architecture:** hrm-api module Finance: 1 scope class (phạm vi 4 cấp theo NV hưởng), 1 report service (port SQL ERP UNION HĐ hãng + YCSC/BD, gom NV → phòng), 1 print-table class (HTML cho mẫu in DB 313/314), 1 controller + routes. hrm-client: 1 trang `/sale/sales-income-summary` + popup chi tiết + Excel ExcelJS + xem trước bản in (`reportPrintPreviewMixin`), gắn 2 menu.

**Tech Stack:** Laravel (hrm-api, PHP 7.4), Nuxt 2 / Vue 2 (hrm-client, Node 14), ExcelJS, MySQL DB gộp `erp_hrm_check`.

**Spec:** `HRM/.plans/bang-tong-hop-thu-nhap-ban-hang/design.md`

## Global Constraints

- Nguồn ERP để bám (đọc, KHÔNG sửa): `ERP/TanPhatDev/app/Services/Reports/CommissionSettlementQuarterReportService.php`, `app/Http/Controllers/ReportController.php:4587-4860`, `resources/views/reports/commission_settlement_quarter.blade.php`, `app/Services/PrintTemplate/CommissionSettlementQuarterPrint.php`, `CommissionSettlementQuaterDetailPrint.php`.
- Tên cột mới, đúng chữ: **"DSTC quyết toán"**; field API: **`standard_settlement`** = giá trị ERP `standard_quarter` = `round(settlement_firm.commission_sale)`. Response/print/Excel KHÔNG còn `standard_month` / `standard_quarter` hay tiêu đề "DS tính thưởng năng suất tháng" / "DS tiêu chuẩn tính thưởng năng suất quý" / "DSTC tính TNS tháng" / "DSTC tinh TNS quý".
- 4 quyền (tên giữ y ERP, guard `api`, group `'Báo cáo tổng thu nhập từ bán hàng'`, type 23):
  `Xem báo cáo tổng thu nhập từ bán hàng - tổng công ty` · `... - công ty` · `... - phòng ban` · `... - bộ phận`.
- Màn KHÔNG gate. Không quyền ⇒ chỉ `ac.employee_id = auth()->id()`. Mọi truy vấn (dòng, tổng, popup, in, export) qua scope.
- Hằng ERP: `account_id = 117`; works id `TT=9, TVC=10, TTHHD=12, TNST=13, TNSQ=14` (tra theo `works.code` lúc chạy như ERP, không hard-code id); loại trừ `invoiceable_type` ∈ `App\Model\IncomeExpenditure\BillPayment`, `App\Model\IncomeExpenditure\BillPaymentAuthorization`, `App\Model\Accounting\ClosingEntry`; `contractable_type` `App\Model\Sale\Firm\Contract\FirmContract` / `App\Model\Customers\WrServiceContract`.
- Mẫu in DB: `report_templates.id = 313` (bảng tổng), `314` (chi tiết NV); biến `HEADER`, `TU_NGAY`, `DEN_NGAY`, `CHI_TIET` (+ biến NV nếu mẫu 314 có — đọc template). Mẫu không chứa cột DSTC nên KHÔNG sửa DB.
- Kỳ quyết toán: `companies.config_settlement_period` (JSON `[{year, details:[{period, date_from 'd/m/Y', date_to 'd/m/Y'}]}]`) của công ty `auth()->user()->current_company_role`.
- KHÔNG sửa `CustomerDebtScope` (hàm dùng chung — CLAUDE.md HRM bắt hỏi trước). KHÔNG sửa ERP.
- Test chạy trên DB gộp thật ⇒ `DatabaseTransactions`, KHÔNG `RefreshDatabase`; fixture dùng năm 2099 + mã `uniqid()`.
- Nhánh: hrm-api đang ở `develop` (làm thẳng); hrm-client đang ở `gop_db` ⇒ làm client trong worktree tạm từ `origin/develop`. KHÔNG push. Commit message kết thúc `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- FE: popup `V2BaseModal`, form/lọc `V2Base*`, lọc đơn vị `V2BaseCompanyDepartmentFilter`. Khuôn tham chiếu: `hrm-client/pages/sale/customer-debt-compare/index.vue` (in + excel), `hrm-client/pages/sale/customer-debt-by-employee/` (lọc, cây NV).

## Review Focus

1. **Người không quyền xem dòng tổng / popup / in / export của NV khác qua tham số `employee_id`** — phải ra rỗng (chỉ số của mình). Test ở Task 3.
2. **Một NV có dòng ở cả HĐ hãng và YCSC/BD** — bảng tổng gộp thành 1 dòng NV, cộng đúng cả 2 nguồn. Test ở Task 2.
3. **Phân trang**: dòng Tổng cộng tính trên toàn bộ kết quả, STT phòng/NV liên tục qua các trang (STT trang 2 không bắt đầu lại 1). Test ở Task 2.
4. **`has_invoice=0`** lấy cả HĐ `has_invoice IS NULL`. Test ở Task 2.
5. **Công ty chưa cấu hình kỳ** (`config_settlement_period` NULL / năm không có) — `/meta` trả `periods: []`, màn vẫn lọc theo ngày tay được. Test ở Task 3.

---

### Task 1: Quyền api + scope phạm vi

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm 4 dòng ngay sau khối "Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên", ~dòng 1721)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/permission_legacy_ids.php` (4 key, id = 4 số kế tiếp chưa dùng — tra số lớn nhất hiện có)
- Create: `hrm-api/Modules/Finance/Services/SalesIncome/SalesIncomeScope.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/SalesIncomeScopeTest.php`

**Interfaces:**
- Produces: `SalesIncomeScope::PERMISSIONS` (mảng 4 tên, thứ tự tổng cty → cty → phòng → bộ phận); `level(): string` trả `'all'|'company'|'department'|'part'|'own'`; `apply($query, string $prefix): void` — `$prefix` là tiền tố cột kiểu `'ac.employee_'` để áp lên `{$prefix}company_id`, `{$prefix}department_id`, `{$prefix}part_id`, và cột "của mình" `{$ownColumn}` (tham số thứ 3, mặc định `'ac.employee_id'`).

- [x] **Step 1: Viết test fail** — `SalesIncomeScopeTest` (DatabaseTransactions, flush `RequestCache` trong setUp như `BonusEndYearSettlementScopeTest`), gán quyền bằng insert `employee_has_permissions` (model_type `Modules\Timesheet\Entities\Employee`):
  - `test_khong_quyen_chi_loc_cua_minh`: level `'own'`; SQL của query sau `apply` chứa `ac.employee_id = ?` với binding = id mình, không có `company_id`.
  - `test_quyen_cong_ty_loc_theo_cong_ty_dang_chon_hoac_cua_minh`: bindings chứa `current_company_role` và id mình.
  - `test_quyen_phong_ban_dung_listManageDepartmentIds`, `test_quyen_bo_phan_dung_listManagePartIds`.
  - `test_cap_cao_nhat_thang`: có cả quyền bộ phận + tổng công ty ⇒ `'all'`, query không thêm where.
  - `test_seeder_co_4_quyen_api`: chạy `$this->seed(PermissionsTableSeeder::class)` hoặc gọi phần seeder tương ứng → `permissions` có đủ 4 tên guard `api`.
- [x] **Step 2:** `cd hrm-api && php artisan test Modules/Finance/Tests/Feature/SalesIncomeScopeTest.php` → FAIL (class không tồn tại).
- [x] **Step 3:** Implement scope bám `CustomerDebtScope` (`isCurrentEmployeeHasPermission`, `listManageDepartmentIds()`, `listManagePartIds()`, `current_company_role`) nhưng cột "của mình" là NV hưởng; mỗi cấp = `whereIn(cột, ids ?: [0]) OR own = me`. Thêm 4 dòng seeder `$this->perm([...])` + legacy ids.
- [x] **Step 4:** chạy lại → PASS.
- [x] **Step 5:** commit `feat(finance): quyền + scope Bảng tổng hợp thu nhập từ bán hàng`.

---

### Task 2: Report service (truy vấn + gom cây + tổng)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/SalesIncome/SalesIncomeReportService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/SalesIncomeReportServiceTest.php`

**Interfaces:**
- Consumes: `SalesIncomeScope` (Task 1).
- Produces:
  - `rows(Request $r): Collection` — mỗi phần tử 1 NV (đã gộp 2 nguồn): `employee_id, employee_code, employee_name, department_id, department_name, standard_settlement, commission_month, commission_quarter, commission_bonus_quarter, diff_employee_amount, delivery_money, amount_interest, minus_overdue`; sắp `department_id, employee_id` như ERP.
  - `detailRows(Request $r): Collection` — mỗi phần tử (HĐ × NV), bắt buộc `employee_id` trong request: các field trên + `contractable_id, contractable_type, contractable_code, customer_id, customer_code, customer_name, settlement_id, settlement_code, handover_date, latest_payment_date`.
  - `totals(Collection $rows): array` — tổng 8 field số + `sum_commission` (= tháng + quý) + `total_income` (= tháng + quý + thưởng thêm + thực hiện HĐ + vận chuyển).
  - `tree(Collection $pageRows, Collection $allRows): array` — danh sách phòng `{department_id, name, index, <các tổng của phòng TRONG TRANG>, employees:[{employee_id, code, name, index, <field>, sum_commission, total_income}]}`; `index` phòng / NV đánh trên `$allRows` (như `indexData` ERP), phòng không có `department_id` bị bỏ (như ERP `render`).
  - `search(Request $r): array` — `{total, data: tree, pagination:{current_page, per_page, total, last_page}}`; phân trang theo NV, `per_page` mặc định 20.
  - `detail(Request $r): array` — `{total, data, pagination}`.
  - `periods(): array` — JSON kỳ của công ty đang chọn, `[]` khi NULL / JSON hỏng.
- Request params: `start_date`, `end_date` (Y-m-d, lọc `whereDate(ac.invoiceable_date_accounting)`), `company_id`, `department_id`, `part_id`, `employee_id`, `has_invoice` (`''|'1'|'0'`), `contract_code` (LIKE), `customer_id`, `page`, `per_page`.

- [x] **Step 1: Viết test fail** — fixture trong transaction: 1 NV thật, insert `account_details` account 117 với `invoiceable_date_accounting` năm 2099, 1 HĐ hãng + 1 YCSC/BD giả (insert `firm_contracts`/`wr_service_contracts` tối thiểu, `has_invoice` khác nhau), dòng `type=2` work TNST 1.000.000, `type=1` work TNST 200.000, work TVC 50.000; 1 `settlement_contract_employees` + `settlement_contract_departments` + `firm_settlement_contract_detail(type=2)` + `settlement_contracts` cho HĐ hãng với `commission_sale = 1234567.4`. Act as super-quyền (tổng công ty) trừ khi test nói khác.
  - `test_gop_2_nguon_1_dong_nv`: `rows()` có 1 phần tử cho NV, `commission_month = 800000` (+ phần YCSC/BD), `delivery_money = 50000`.
  - `test_standard_settlement_bang_round_commission_sale`: `standard_settlement = 1234567`; phần tử không có key `standard_month`/`standard_quarter`.
  - `test_has_invoice_0_lay_ca_null`, `test_has_invoice_1_chi_lay_1`.
  - `test_totals_tinh_tren_toan_bo`: 25 NV giả (hoặc per_page=1 với 2 NV) → `search()` trang 2: `total` = tổng cả 2 NV; STT NV trang 2 = 2 nếu cùng phòng.
  - `test_detail_loc_contract_code_va_customer`.
  - `test_periods_cong_ty_khong_cau_hinh_tra_rong`.
- [x] **Step 2:** `php artisan test Modules/Finance/Tests/Feature/SalesIncomeReportServiceTest.php` → FAIL.
- [x] **Step 3:** Port `getDataFirm`/`getDataWr`/`getData`/`filterAcc` ERP sang query builder HRM (`DB::table`), giữ nguyên mọi join/công thức; thay `filterAcc` phần quyền bằng `SalesIncomeScope::apply($q, 'ac.employee_')`; chỉ chọn `round(settlement_firm.commission_sale) as standard_settlement` thay 2 cột cũ; qualify mọi cột (DB gộp hay ambiguous `company_id`/`employee_id`). Bỏ nhánh `period` → join `bill_commission_settlement_quarter_employees` (chỉ ra `progressive_approval_percent`, ERP không hiển thị — Ruling, xem cuối plan). Phân trang trong PHP như ERP.
- [x] **Step 4:** chạy lại → PASS.
- [x] **Step 5:** commit `feat(finance): service Bảng tổng hợp thu nhập từ bán hàng`.

---

### Task 3: Controller, routes, bản in

**Files:**
- Create: `hrm-api/Modules/Finance/Services/SalesIncome/SalesIncomePrintTable.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/SalesIncomeSummaryController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (khối mới ngay sau `customer-debt-compare`, ~dòng 1940)
- Test: `hrm-api/Modules/Finance/Tests/Feature/SalesIncomeSummaryApiTest.php`

**Interfaces:**
- Consumes: `SalesIncomeReportService` (Task 2).
- Produces routes (prefix `/sales-income-summary`, không middleware quyền):
  - `GET /` → `index` → `{code:200, total, data, pagination}`
  - `GET /meta` → `{data:{periods, year: năm hiện tại}}`
  - `GET /detail` → `detail` (bắt buộc `employee_id`)
  - `GET /export` → `{data:{total, tree:<toàn bộ, không phân trang>}}`
  - `GET /export-detail` → `{data:{total, rows}}`
  - `GET /print-list-data` và `GET /print-detail-data` → `printListPayload($html, $total) + ['landscape' => true]` (dùng trait `Modules\CustomerCare\Services\Concerns\LimitsPrintListRows`, giới hạn đếm theo số dòng NV/HĐ).
- `SalesIncomePrintTable::summary(array $tree, array $total): string`, `::detail(Collection $rows, array $total): string` — HTML bám `CommissionSettlementQuarterPrint::getTable` / `CommissionSettlementQuaterDetailPrint` ERP, thay 2 cột DSTC bằng 1 cột "DSTC quyết toán"; số 0 hiện `-`; escape `&`.
- Validate: `start_date`, `end_date` required|date, `end_date` after_or_equal; thông điệp như `CustomerDebtByEmployeeController::validateDates` ("Vui lòng chọn thời gian"…). `/detail`, `/export-detail`, `/print-detail-data`: `employee_id` required|integer.

- [x] **Step 1: Viết test fail** (`SalesIncomeSummaryApiTest`, `actingAs(..., 'api')`):
  - `test_thieu_ngay_tra_422_vui_long_chon_thoi_gian`.
  - `test_index_khong_co_standard_month`: JSON `total` có `standard_settlement`, không có `standard_month`/`standard_quarter`.
  - `test_khong_quyen_truyen_employee_id_nguoi_khac_ra_rong`: NV A không quyền gọi `/`, `/detail`, `/export`, `/print-list-data` với `employee_id` = NV B (có fixture) ⇒ không có số của B (`data` rỗng, tổng = 0, `template` không chứa mã NV B).
  - `test_print_list_data_dung_mau_313_va_cot_dstc_quyet_toan`: `template` chứa "DSTC quyết toán", không chứa "DS tính thưởng năng suất tháng".
  - `test_print_detail_mau_314`.
  - `test_meta_tra_periods_cua_cong_ty_dang_chon`.
- [x] **Step 2:** `php artisan test Modules/Finance/Tests/Feature/SalesIncomeSummaryApiTest.php` → FAIL.
- [x] **Step 3:** Implement controller (khuôn `CustomerDebtCompareController::printListData`: `report_templates` → `fillReport` → `clearNull`; `HEADER` = `companies.header` của công ty NV), print table, routes.
- [x] **Step 4:** chạy lại 3 file test Task 1–3 → PASS.
- [x] **Step 5:** commit `feat(finance): API Bảng tổng hợp thu nhập từ bán hàng (lọc, chi tiết, in, export)`.

---

### Task 4: Trang client + popup + Excel + menu

**Files (trong worktree client từ `origin/develop`):**
- Create: `hrm-client/pages/sale/sales-income-summary/index.vue`
- Create: `hrm-client/pages/sale/sales-income-summary/components/SalesIncomeDetailModal.vue`
- Create: `hrm-client/pages/sale/sales-income-summary/components/export-excel.js`
- Modify: `hrm-client/components/subsystem-menu/finance.js:398` → `{ label: 'Bảng tổng hợp thu nhập từ bán hàng', link: '/sale/sales-income-summary' }` (khớp cú pháp mục có link trong file)
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:266` → màn `'Tổng hợp thu nhập từ bán hàng'` thành `{ n: 'Tổng hợp thu nhập từ bán hàng', link: '/sale/sales-income-summary' }`

**Interfaces:**
- Consumes: routes Task 3 (base `finance/sales-income-summary` — xác nhận prefix module Finance như cách `customer-debt-compare` gọi `API`).
- Produces: `exportSalesIncomeSummary(tree, total, periodText)`, `exportSalesIncomeDetail(rows, total, employeeText, periodText)` trong `export-excel.js`.

Nội dung màn (bám blade ERP):
- Lọc: `V2BaseCompanyDepartmentFilter` (công ty/phòng/bộ phận) + NV; Năm (option từ `/meta.periods[].year`, mặc định `meta.year`); Kỳ (từ `details` của năm; chọn kỳ ⇒ điền Từ/Đến ngày đổi `d/m/Y`→`Y-m-d` và khoá 2 ô; bỏ năm ⇒ xoá kỳ + ngày); Từ/Đến ngày bắt buộc; Xuất hoá đơn (Tất cả / Xuất hóa đơn=1 / Không xuất hóa đơn=0). Nút Lọc, Làm mới, In, Xuất Excel.
- Bảng: tiêu đề 12 cột theo design §4; dòng Tổng cộng (từ `total`); dòng phòng in đậm (STT = `index`); dòng NV STT `phòng.NV`, tên `code - name` bấm mở popup. Số 0 hiện `-`. Phân trang.
- Popup `V2BaseModal` "Chi tiết hợp đồng của {code} - {name}": lọc Hợp đồng (text), Khách hàng (`V2BaseSelectRemote`); bảng cột design §4 + dòng Tổng cộng; In, Xuất Excel, Làm mới; phân trang.
- In: `reportPrintPreviewMixin.openPrintList` với endpoint `print-list-data` / `print-detail-data`.
- Excel: ExcelJS, cột cố định y bảng (không chọn trường), dòng Tổng cộng, cột số ghi `Number` format `#,##0;-#,##0;""`, tên file `Bang_tong_hop_thu_nhap_tu_ban_hang.xlsx` / `..._chi_tiet_<mã NV>.xlsx`.

- [x] **Step 1:** Tạo worktree client: `git -C hrm-client worktree add ../hrm-client-salesincome origin/develop -b feat/sales-income-summary`; symlink `node_modules` từ `hrm-client`.
- [x] **Step 2:** Implement 3 file + 2 menu.
- [x] **Step 3:** `npx eslint pages/sale/sales-income-summary components/subsystem-menu/finance.js components/subsystem-menu/sale-hub.js` → 0 error.
- [x] **Step 4:** commit `feat(sale): màn Bảng tổng hợp thu nhập từ bán hàng`.

---

### Task 5: Kiểm thử trình duyệt + đối chiếu số ERP

**Files:** không sửa code (chỉ sửa nếu lỗi phát hiện, rồi commit fix vào task tương ứng).

- [x] **Step 1:** Chạy API :8000 + client worktree :3000 (Node 14), mở `http://127.0.0.1:3000/sale/sales-income-summary` bằng Playwright (Node 20, token `HRM/e2e/.auth/user.json`). Tài khoản local thiếu quyền ⇒ nếu API 403/thiếu dữ liệu, gán tạm quyền "tổng công ty" trong DB local cho tài khoản test HOẶC `page.route` fulfill bằng response dump thật từ service.
- [x] **Step 2:** Kiểm: vào màn từ cả 2 menu; chọn năm + kỳ ⇒ ngày tự điền và khoá; lọc ra bảng; dòng tổng; bấm NV mở popup; In 2 chỗ mở xem trước có cột "DSTC quyết toán"; Excel 2 chỗ tải được, đủ cột. Chụp màn vào scratchpad.
- [x] **Step 3: Đối chiếu số** — chọn 1 kỳ có dữ liệu (vd kỳ gần nhất cty 1). Chạy SQL ERP gốc (dựng lại từ service ERP bằng script PHP/SQL trong scratchpad, quyền tổng công ty) và so tổng từng cột với `total` của HRM `/sales-income-summary` cùng tham số: `standard_quarter` ERP = `standard_settlement` HRM; 8 cột còn lại bằng nhau tuyệt đối. Ghi kết quả vào report task.

---

## Rulings (quyết định trong plan)

- Bỏ join phiếu QT quý khi có `period` (chỉ sinh `progressive_approval_percent`, ERP không hiển thị ở màn/in/excel) — YAGNI; nếu sai: thêm lại 1 leftJoinSub.
- Tham số ngày đổi sang quy ước HRM `start_date`/`end_date` (Y-m-d) thay `date_from`/`date_to`; FE tự chuyển từ kỳ `d/m/Y`.
- Excel dựng ở FE bằng ExcelJS (khuôn HRM), không dùng HTML-to-xlsx của ERP; cột/tiêu đề y ERP trừ cột DSTC.
- Chỉ 2 nguồn HĐ như ERP (`FirmContract`, `WrServiceContract`); HĐ HRM `Modules\Assign\Entities\Contract\Contract` hiện chưa có dòng TK 117 trong DB nên không thêm — nếu sau này có, phải mở rộng UNION.
- `per_page` mặc định 20 (chuẩn HRM) thay 10 của ERP.
