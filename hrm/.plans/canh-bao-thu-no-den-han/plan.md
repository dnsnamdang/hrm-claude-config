# Cảnh báo thu nợ đến hạn (Xét theo quy chế) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn `/sale/customer-debt-due-warning` port ERP `WarningDebtDueDateService` — 3 ô thống kê (Sắp đến hạn / Đến hạn / Quá hạn) + cây Phòng → NV → KH → HĐ y khuôn màn "Công nợ KH quá hạn", In + Excel.

**Architecture:** BE: service mới **kế thừa** `CustomerDebtOverdueReportService` để dùng lại `sortAndNumber()` / `groupKeys()` / `applyFilters()` mà KHÔNG sửa một dòng nào của service quá hạn; truy vấn riêng theo ERP; nhóm (bucket) tính ở PHP sau khi lấy dòng. FE: copy thư mục `pages/sale/customer-debt-overdue` rồi đổi cột/bộ lọc + thêm thanh 3 ô.

**Tech Stack:** Laravel 8 / PHP 7.4 (PHPUnit trên DB gộp `erp_hrm_check`, `DatabaseTransactions`), Nuxt 2 / Vue 2, ExcelJS, Playwright e2e (Node 20).

**Spec:** `HRM/docs/superpowers/specs/2026-11-21-canh-bao-thu-no-den-han-design.md`

## Global Constraints

- Chỉ đọc; KHÔNG sửa ERP, KHÔNG sửa số/hành vi màn quá hạn (`CustomerDebtOverdueReportService`, `pages/sale/customer-debt-overdue/*`).
- TK 131 = `account_id = 22`; class ERP `App\Model\Sale\Firm\Contract\FirmContract` / `App\Model\Customers\WrServiceContract`.
- Quyết toán: firm `status = 10`, wr `status = 5` bị loại (điều kiện trong JOIN như ERP).
- HĐ giảm: `firm.type IN (3,6,10)` hoặc `wr.type = 4`. HĐ gốc: `firm.parent_contract_id` (khi `firm.type != 8`) / `wr.parent_id`.
- N = `companies.warning_due_date` của `\App\Support\CurrentCompany::id()`; NULL → 0.
- Nhóm theo H (Hạn thanh toán dòng HĐ = MIN `payment_overdue_date` các HĐ con lọt điều kiện), D = Đến ngày: `soon` D < H ≤ D+N · `due` H = D · `overdue` H < D.
- Số ngày quá hạn: overdue = D − H; due = 0; soon = null (ô trống).
- Quyền `sale.canh_bao_thu_no_den_han.view`, không gate vào màn, phạm vi qua `CustomerDebtScope`.
- Số `toLocaleString('en-US')`, ô tiền 0 hiện `-`; ngày `dd/mm/yyyy`; Excel ô số thật + `#,##0`.
- FormRequest/validate: KHÔNG khai message cho `required`/`date`/`in` (dùng lang file).
- Tài liệu chỉ ở `HRM/.plans/canh-bao-thu-no-den-han/`, file tạm ở scratchpad.
- Commit cục bộ trên `develop` của từng repo, KHÔNG push (user tự quyết push).

## Review Focus

1. Đổi công ty đang thao tác (N khác nhau giữa công ty) → ô "Sắp đến hạn" và tập HĐ đổi theo N của công ty mới — test `test_n_theo_cong_ty_dang_thao_tac`.
2. Bấm ô nhóm khi đang ở trang 3 → về trang 1, phân trang/tổng/STT nhóm tính lại trên nhóm đó — kiểm ở e2e Task 4.
3. HĐ gốc có phụ lục với hạn khác nhau → H = hạn sớm nhất, không rơi ra ngoài 3 nhóm — test `test_phu_luc_han_som_nhat_quyet_dinh_nhom`.
4. `bucket` rác / Đến ngày trống → 422, không 500 — test `test_validate`.
5. Xuất Excel/In khi đang chọn ô → chỉ chứa HĐ nhóm đó, tiêu đề ghi tên nhóm — test `test_export_rows_theo_bucket` + e2e Task 4.

---

### Task 1: BE service + API + quyền

**Files:**
- Create: `hrm-api/Modules/Finance/Services/CustomerDebt/CustomerDebtDueWarningReportService.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/CustomerDebtDueWarningController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (ngay sau group `/customer-debt-overdue`, dòng ~2123)
- Modify: `hrm-api/app/Support/Permissions/Catalog/sale.php` (~dòng 1150, mã `sale.canh_bao_thu_no_den_han.view`: `platforms => ['erp', 'hrm']`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/CustomerDebtDueWarningReportTest.php`

**Interfaces:**
- Consumes: `CustomerDebtOverdueReportService::sortAndNumber(Collection, int)`, `groupKeys($r, int)`, `applyFilters($query, Request, string $codeColumn)`; `CustomerDebtScope(string $permission)`; fixtures `BuildsMonitorContractFixtures::makeFirmContract/makeWrContract/addLedger`, `GrantsPermissionScope`.
- Produces (Task 2–4 dùng):
  - `class CustomerDebtDueWarningReportService extends CustomerDebtOverdueReportService`
  - `const PERMISSION = 'sale.canh_bao_thu_no_den_han.view'`, `const BUCKET_SOON = 'soon'`, `BUCKET_DUE = 'due'`, `BUCKET_OVERDUE = 'overdue'`, `const BUCKETS = ['soon','due','overdue']`
  - `scope(): CustomerDebtScope` (override, dùng `self::PERMISSION` của class con)
  - `warningDays(): int`
  - `rows(Request $r): Collection` — đã lọc `bucket` (nếu có), đã sắp + đánh `no`
  - `search(Request $r): array` → `['data','total','groups','meta','summary']`
  - `exportRows(Request $r): array` → `['rows','total','summary']` (`summary` = `totals()` trên dòng đã lọc bucket)
  - `totals(Collection): array` → `['total_after_vat','paid','debt']` (float)
  - `summary` của `search`: `['warning_days' => int, 'soon' => ['count'=>int,'debt'=>float], 'due' => [...], 'overdue' => [...]]` — tính trên dòng CHƯA lọc bucket.
  - Mỗi dòng (object): `contract_id, contract_code, contractable_type ('firm'|'wr'), contractable_class, customer_id, customer_code, customer_name, department_id, department_name, employee_id, employee_code, employee_name, company_id, part_id, handover_date (Y-m-d|null), payment_due_date (Y-m-d), total_after_vat, paid, debt, number_overdue (int|null), bucket, no`.
  - API `GET finance/customer-debt-due-warning` (`date_to` required|date, `bucket` nullable|in:soon,due,overdue, `report_type`, `page`, `per_page`, `customer_id`, `contract_code`, `company_id`, `department_id`, `part_id`, `employee_id`), `GET .../meta` → `{permissions: scope()->flags()}`, `GET .../export-rows` (thêm `limit`).

- [x] **Step 1: Viết test (đỏ)** — khuôn `CustomerDebtOverdueReportTest` (setUp y hệt, CODE = mã mới). `setUp` thêm `DB::table('companies')->where('id', CurrentCompany::id())->update(['warning_due_date' => 5])`. `params()` = `['date_to' => '2026-10-31']`. Helper `firm($due, $attrs=[])` = `makeFirmContract(['payment_overdue_date'=>$due,'handover_date'=>'2026-09-11','total_after_vat'=>50000000] + $attrs)`, mỗi HĐ ghi sổ Nợ 10,000,000 (2026-09-20) + Có 4,000,000 (2026-10-10). Các test:
  - `test_ba_nhom_theo_han_thanh_toan`: H `2026-10-20` → bucket `overdue`, `number_overdue` 11; `2026-10-31` → `due`, 0; `2026-11-03` → `soon`, null; `2026-11-10` → không có dòng.
  - `test_so_lieu_cot`: dòng overdue: `total_after_vat` 50000000, `paid` 4000000, `debt` 6000000, `handover_date` '2026-09-11', `payment_due_date` '2026-10-20'.
  - `test_het_no_bi_loai`: Nợ 4m Có 4m → không có dòng. Sổ sau Đến ngày (2026-11-05) không tính vào `debt`.
  - `test_phu_luc_cong_vao_hd_goc`: phụ lục `type 2, parent_contract_id = gốc`, H `2026-10-25`, sổ Nợ 3m → 1 dòng mã HĐ gốc, `debt` 9000000.
  - `test_phu_luc_han_som_nhat_quyet_dinh_nhom`: gốc H `2026-11-02`, phụ lục H `2026-10-28` (cả hai còn nợ) → `payment_due_date` '2026-10-28', bucket `overdue`.
  - `test_phu_luc_giam_tru`: phụ lục `type 3` có sổ Nợ 2m → `debt` của gốc giảm 2,000,000.
  - `test_hd_da_quyet_toan_bi_loai`: firm `status 10` và wr `status 5` → không có dòng.
  - `test_wr_contract`: `makeWrContract` H `2026-10-20` → `contractable_type` 'wr', bucket `overdue`.
  - `test_khong_cau_hinh_n_bang_0`: `warning_due_date = null` → HĐ H `2026-11-03` không có; `summary.warning_days` 0.
  - `test_n_theo_cong_ty_dang_thao_tac`: set `warning_due_date` = 5 cho công ty khác, 0 cho `CurrentCompany::id()` → `warningDays()` = 0.
  - `test_loc_bucket_va_summary`: 3 HĐ 3 nhóm; `search(bucket=due)` → `data` chỉ HĐ due, `meta.total` 1, `summary` lấy TRƯỚC khi tạo fixture làm mốc, sau khi tạo thì `soon/due/overdue.count` mỗi nhóm tăng đúng 1 (DB thật có sẵn HĐ khác nên so chênh lệch); không bucket → tổng `summary.*.debt` = `total.debt` (sai số ≤ 1).
  - `test_khong_quyen_chi_thay_hd_minh_lap`: HĐ `created_by` người khác → không có dòng.
  - `test_validate`: `GET /api/finance/customer-debt-due-warning` thiếu `date_to` → 422; `bucket=xyz` → 422.
  - `test_export_rows_theo_bucket`: `exportRows(bucket=overdue, limit=2000)` → mọi `rows[*].bucket` = 'overdue', `summary` có `debt`.

- [x] **Step 2: Chạy đỏ** — `cd hrm-api && php artisan test Modules/Finance/Tests/Feature/CustomerDebtDueWarningReportTest.php` → FAIL "Class ... CustomerDebtDueWarningReportService not found".

- [x] **Step 3: Viết service.** Truy vấn trong: copy khung JOIN của `CustomerDebtOverdueReportService::mainRows` nhưng **JOIN firm/wr thêm điều kiện status** (`firm.status != 10`, `wr.status != 5`, đặt trong closure join như ERP). Cột chọn: như quá hạn (bỏ `over_date`, `begin`, `number_overdue`) + `COALESCE(firm.payment_overdue_date, wr.payment_overdue_date) as payment_due_date`, `SUM(type=1)-SUM(type=2) as debt`, `SUM(type=2) as paid` (đều đã giới hạn `invoiceable_date_accounting <= D` bằng WHERE). HAVING: `DATE_SUB(payment_due_date, INTERVAL ? DAY) <= ? AND debt > 0` với binding `[N, D]`. Truy vấn ngoài: gom `parent_contractable_id, contractable_type`; `SUM(sign*total_after_vat)`, `SUM(sign*paid)`, `SUM(sign*debt)`, `MIN(payment_due_date)`, `MAX(handover_date)`; KHÔNG HAVING; `applyFilters($outer, $request, 'result.parent_contractable_code')`. PHP: normalize → tính `bucket`/`number_overdue` theo Global Constraints → `rows()` lọc bucket rồi `sortAndNumber`. `groups()` override: như cha nhưng cộng `['total_after_vat','paid','debt']`. `warningDays()`: `(int) DB::table('companies')->where('id', CurrentCompany::id())->value('warning_due_date')`. Docblock class ghi các điểm "khác ERP có chủ đích" của spec 5.4.

- [x] **Step 4: Controller + route + Catalog.** Controller khuôn `CustomerDebtOverdueController` (index/meta/exportRows), `validateDates` → `['date_to' => 'required|date', 'bucket' => 'nullable|in:soon,due,overdue']` không message. Route group `/customer-debt-due-warning` 3 route. Catalog thêm `'hrm'`; chạy `php artisan permission:catalog-sync`.

- [x] **Step 5: Chạy xanh** — lệnh Step 2 → PASS toàn bộ; thêm `php artisan test Modules/Finance/Tests/Feature/CustomerDebtOverdueReportTest.php` → PASS (màn quá hạn không đổi).

- [x] **Step 6: Commit (hrm-api, develop)**
```bash
git add Modules/Finance/Services/CustomerDebt/CustomerDebtDueWarningReportService.php Modules/Finance/Http/Controllers/V1/CustomerDebtDueWarningController.php Modules/Finance/Routes/api.php app/Support/Permissions/Catalog/sale.php Modules/Finance/Tests/Feature/CustomerDebtDueWarningReportTest.php
git commit -m "feat(finance): báo cáo cảnh báo thu nợ đến hạn (xét theo quy chế) — API port ERP"
```

### Task 2: Đối chiếu ERP

**Files:**
- Create (scratchpad, không commit): script tinker so sánh.
- Modify: `HRM/.plans/canh-bao-thu-no-den-han/design.md` (thêm mục "Đối chiếu ERP").

**Interfaces:**
- Consumes: `CustomerDebtDueWarningReportService::rows()` (Task 1); ERP `App\Services\Reports\WarningDebtDueDateService::getData()` (`ERP/TanPhatDev`, cùng DB local).

- [x] **Step 1:** `grep DB_ ERP/TanPhatDev/.env` (chỉ xem tên DB, không in host/mật khẩu) — ERP và HRM phải cùng trỏ một DB; khác thì ghi chú và đối chiếu bằng SQL của ERP chạy tay trên DB HRM.
- [x] **Step 2:** Với user có quyền GROUP (Tổng công ty), D = hôm nay và D = `2026-10-31`, N của công ty đang thao tác: lấy tập khoá `class-id HĐ gốc → debt` cả hai bên (ERP lấy kết quả `getData` trước bước render). So: thiếu/thừa khoá, lệch debt > 1 đồng.
- [x] **Step 3:** Expected: 0 khoá lệch, 0 debt lệch. Lệch → `superpowers:systematic-debugging`, sửa service (test đỏ trước) rồi so lại. Ghi bảng kết quả (số HĐ, tổng debt, số lệch) vào `design.md`.

### Task 3: FE màn + menu + In + Excel

**Files:**
- Create: `hrm-client/pages/sale/customer-debt-due-warning/index.vue` (copy `customer-debt-overdue/index.vue`)
- Create: `hrm-client/pages/sale/customer-debt-due-warning/print.vue` (copy `customer-debt-overdue/print.vue`, khổ ngang)
- Create: `hrm-client/pages/sale/customer-debt-due-warning/components/DueWarningTable.vue` (copy `OverdueTable.vue`)
- Create: `hrm-client/pages/sale/customer-debt-due-warning/components/build-tree.js` (copy; `AMOUNT_KEYS = ['total_after_vat','paid','debt']`)
- Create: `hrm-client/pages/sale/customer-debt-due-warning/components/export-excel.js` (copy)
- Create: `hrm-client/pages/sale/customer-debt-due-warning/components/BucketStats.vue`
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:297` → `{ n: 'Cảnh báo thu nợ đến hạn', link: '/sale/customer-debt-due-warning' }`

**Interfaces:**
- Consumes: API Task 1 (`summary`, `bucket`, cột dòng); `utils/export/listExportFile.fetchExportRows`.
- Produces: `BucketStats` props `{ summary: Object, value: String|null, loading: Boolean }`, emit `input(bucket|null)` (bấm ô đang chọn → `null`).

- [x] **Step 1: index.vue.** `API = 'finance/customer-debt-due-warning'`; `table="sale_customer_debt_due_warning"`; tiêu đề "Bộ lọc cảnh báo thu nợ đến hạn"; ReportInfoTip mục đích theo spec §1. Bộ lọc thay khoảng ngày bằng 1 ô **Đến ngày** `date_to` (bắt buộc, mặc định hôm nay); giữ Báo cáo theo / tổ chức / Khách hàng / Hợp đồng. Thêm `filters.bucket` (null, đồng bộ query URL qua `filterStateMixin` như các filter khác). `BucketStats` đặt giữa panel và bảng; đổi bucket → `page = 1` rồi tải lại.
- [x] **Step 2: BucketStats.vue** — copy pattern `pages/assign/my-todo/index.vue:11-35` + SCSS `:803-860` (thẻ cao 52px, viền trái 3px, nhãn xám). 3 thẻ: `Sắp đến hạn (≤ {N} ngày)` màu `#F59E0B` · `Đến hạn` `#D97706` · `Quá hạn` `#DC2626`; mỗi thẻ: nhãn, `count` HĐ, tổng `debt` en-US. Thẻ là phần tử bấm được (`role="button"`, `tabindex="0"`, Enter = bấm), thẻ đang chọn nền đậm hơn + viền 1px cùng màu. Không dùng thẻ HTML form thô (grep tự kiểm CLAUDE.md phải rỗng).
- [x] **Step 3: DueWarningTable + build-tree.** Cột: STT · Tên (cây) · [Nhân viên nếu report_type 2] · Ngày BGNT · Hạn thanh toán (`payment_due_date`) · Tổng giá trị · Đã thu · Còn phải thu · Số ngày quá hạn (null → trống, 0 → `0`). Dòng nhóm/TỔNG: chỉ 3 ô tiền. ⓘ đầu cột: Còn phải thu = "Nợ − Có TK 131 lũy kế tới Đến ngày"; Đã thu = "Có TK 131 lũy kế tới Đến ngày"; Hạn thanh toán = "Hạn sớm nhất trong HĐ gốc và phụ lục còn nợ".
- [x] **Step 4: In + Excel.** Tham số gửi kèm `bucket`; tiêu đề "CẢNH BÁO THU NỢ ĐẾN HẠN", dòng phụ "Đến ngày dd/mm/yyyy" + " – Nhóm: <tên nhóm>" khi đang chọn ô. Excel ô số thật `#,##0`, số ngày quá hạn trống khi null.
- [x] **Step 5: Tự kiểm** — `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/sale/customer-debt-due-warning/ | grep -v V2Base` → rỗng; `grep -rnE "toLocaleString\('vi-VN'" pages/sale/customer-debt-due-warning` → rỗng.
- [x] **Step 6: Commit (hrm-client, develop)**
```bash
git add pages/sale/customer-debt-due-warning components/subsystem-menu/sale-hub.js
git commit -m "feat(sale): màn cảnh báo thu nợ đến hạn (xét theo quy chế)"
```

### Task 4: E2E Playwright

**Files:**
- Create: `e2e/tests/customer-debt-due-warning.spec.ts` (khuôn `e2e/tests/bonus-contract-report.spec.ts`)

**Interfaces:**
- Consumes: màn Task 3, API Task 1.

- [x] **Step 1: Viết spec** — (a) mở `/sale/customer-debt-due-warning` → thấy 3 thẻ và bảng có dòng TỔNG CỘNG; (b) Tổng `debt` 3 thẻ = ô Còn phải thu dòng TỔNG (so số đã bỏ dấu `,`); (c) sang trang 2 (nếu có) rồi bấm thẻ "Quá hạn" → URL/request có `bucket=overdue`, `page=1`, mọi dòng HĐ có Số ngày quá hạn > 0; bấm lại → bỏ `bucket`; (d) đang chọn "Đến hạn" bấm Xuất Excel → file tải về, mở bằng ExcelJS kiểm dòng tiêu đề có "Nhóm: Đến hạn"; (e) menu Kinh doanh có link "Cảnh báo thu nợ đến hạn" trỏ đúng đường dẫn.
- [x] **Step 2: Chạy** — `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test customer-debt-due-warning` (cần API :8000 + client :3000, skill run-hrm). Expected: PASS. Lỗi → sửa code Task 3, không nới assertion.
- [x] **Step 3: Chụp màn** 3 thẻ + cây (scratchpad) để báo user; commit spec vào hrm-client? KHÔNG — `e2e/` ngoài repo code, để nguyên file.
- [x] **Step 4:** Cập nhật `HRM/.plans/STATUS.md` (mục "Đang làm") + memory: commit api/client, chưa push, chưa gop_db.

### Checkpoint — 2026-11-21 17:15 (wrap up tự động)
Vừa hoàn thành: Task 1–4 xong. BE service `CustomerDebtDueWarningReportService` + controller/route `finance/customer-debt-due-warning` + quyền `sale.canh_bao_thu_no_den_han.view` bật HRM (15/15 test PASS, thêm test tái hiện lỗi Tổng giá trị). Đối chiếu ERP cấp Tổng công ty: 2,204 HĐ / Còn phải thu 594,653,332,564 — 0 thiếu/thừa/lệch. FE màn + 3 ô thống kê + In/Excel + link menu Kinh doanh; e2e `HRM/e2e/tests/customer-debt-due-warning.spec.ts` 2/2 PASS (ngoài repo, không commit). Review cuối (opus): 0 Critical, 1 Important (Tổng giá trị nhân theo số HĐ con — dòng phụ lục mang giá trị HĐ gốc) → ĐÃ sửa: cộng có dấu giá trị của chính từng HĐ con.
Commit: hrm-api `c062514ed` (tính năng) + `fe9a93966` (fix Tổng giá trị) · hrm-client `b8b24733a` — nhánh `develop`, ĐÃ push origin/develop (rebase lên commit #12258 của Tri Lee, không conflict). CHƯA gop_db.
Đang làm dở: không.
Bước tiếp theo: (1) user quyết có kiểm/sửa màn Công nợ KH quá hạn không — `CustomerDebtOverdueReportService.php:136` dùng cùng công thức cũ, có thể cũng nhân đôi cột "Giá trị HĐ thực tế"; (2) đưa sang gop_db khi user báo; (3) Minor chưa sửa: `date_to` chưa ép `Y-m-d`; bấm ô khi lượt Tìm kiếm chưa trả về hiện theo bộ lọc cũ; tải nhóm lỗi vẫn sáng ô mới; chú thích Còn phải thu ghi "> 0" nhưng dòng gốc có thể ≤ 0; 2 chỗ chữ đỏ không phải lỗi validate (lỗi tải bản in, số đếm ô Quá hạn). Phần "Xét theo HĐ" anh Nam làm sau.
Blocked:
