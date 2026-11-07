# Sổ chi tiết công nợ nhân viên — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP `account-detail.listDetailDebtEmployee` sang HRM (Tài chính › Kế toán công nợ › Nhân viên): xem / in / xuất Excel sổ chi tiết bút toán công nợ gắn nhân viên.

**Architecture:** 1 service đọc `account_details` (`EmployeeDebtDetailService`) dùng chung cho danh sách, bản in và dữ liệu Excel: quét 1 lần lấy mọi dòng, cắt trang trong PHP, 3 dòng tổng tính trên toàn bộ. Controller mỏng chặn 403 ở mọi endpoint. FE theo khuôn báo cáo V2 (`pages/sale/customer-debt-details`), in qua `reportPrintPreviewMixin`, Excel qua `utils/export/listExportFile.js`.

**Tech Stack:** Laravel (hrm-api, Modules/Finance), Nuxt 2 / Vue 2 V2Base (hrm-client), PHPUnit feature test trên DB gộp (DatabaseTransactions).

**Spec:** `hrm-claude-config/hrm/docs/superpowers/specs/gop-db/2026-11-02-so-chi-tiet-cong-no-nhan-vien-design.md` (mọi điều kiện lọc / cột / quyết định lấy ở đó).

## Global Constraints

- Giữ nghiệp vụ ERP `DetailDebtEmployeeService` (getBuilder / getDeptBegin / filter / getData / getTotal), trừ 12 điểm spec mục 8.
- Quyền tên y ERP: "Xem sổ chi tiết công nợ nhân viên của tổng công ty", "Xem sổ chi tiết công nợ nhân viên của công ty"; kiểm bằng trait `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (super admin = có cả 2); khai cuối `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `type` 8, `group` "Sổ chi tiết công nợ nhân viên", KHÔNG khai id; `php artisan permission:sync`.
- Không có quyền nào ⇒ 403 "Bạn không có quyền thực hiện thao tác này" ở MỌI endpoint.
- Chỉ bút toán `ad.employee_id IS NOT NULL` (dòng, tổng, đầu kỳ).
- Phân trang mặc định **10**, tối đa 200. Số chuẩn quốc tế `1,234,567.89`; ô rỗng để trống.
- `account_details` CHỈ ĐỌC. `invoiceable_type` / `contractable_type` là FQN ERP.
- Không `sed -i` / script regex ghi đè file; không tắt server dev (api 8002, client 3000); đóng browser Playwright (`playwright-a`); commit chỉ khi user bảo.
- Nhánh `feat/so-chi-tiet-cong-no-nv` rẽ từ `origin/develop` ở cả hrm-api và hrm-client (gỡ upstream để khỏi push nhầm).

## Review Focus

1. Không chọn nhân viên + có bút toán TK không gắn NV ⇒ không vào dòng / tổng / đầu kỳ; đầu kỳ + Nợ − Có = cuối kỳ (Task 1 `test_balances_only_employee_rows`).
2. Người chỉ có quyền công ty gọi `company_id` công ty khác ⇒ chỉ còn sổ của chính mình (AND phạm vi) (Task 1 `test_scope_company_or_self`).
3. Chọn đồng thời "PXK - Xuất bán" và "Phiếu thu" ⇒ ra cả 2 loại, PXK chỉ loại con 1 (Task 1 `test_invoiceable_types_or_groups`).
4. Lọc TK đối ứng ⇒ đầu kỳ và dòng cùng điều kiện; cột TK đối ứng hiện đủ mọi đối ứng (Task 1 `test_account_ref_filter_consistent`).
5. Thiếu Tài khoản / ngày, hoặc Đến ngày < Từ ngày ⇒ 422 có câu báo theo ô, không 500 (Task 2 `test_validation`).

---

### Task 1: Service đọc sổ + quyền

**Files:**
- Create: `hrm-api/Modules/Finance/Services/EmployeeDebt/EmployeeDebtDetailService.php`
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (cuối file)
- Test: `hrm-api/Modules/Finance/Tests/Feature/EmployeeDebtDetailServiceTest.php`

**Interfaces — Produces:**
- `const PERM_ALL`, `PERM_COMPANY` (tên ở Global Constraints); `const DEFAULT_PER_PAGE = 10`.
- `const INVOICEABLE_TYPES` — 17 mục `['id' => ..., 'name' => ...]` y ERP `AccountDetail::getInvoiceableTypeForSelect` (id PXK/PNK dạng `'App\Model\Warehouse\ProductExport-1'`; loại con PXK 1,2,3,4,11; PNK 2,12,11,4,9; còn lại FQN `App\Model\Warehouse\BorrowSell`, `App\Model\IncomeExpenditure\{BillIncome,BillPayment,BillPaymentAuthorization,BillIncomeReport,BillAdjustDept}`).
- `scopeFlags(): array` → `['is_all_company' => bool, 'is_company' => bool]`; `canView(): bool` (một trong hai).
- `accountIds(int $accountId): array` — TK + con trực tiếp (`identify_number_parent` = số hiệu).
- `rows(Request $request): Illuminate\Support\Collection` — mọi dòng (đã phạm vi + lọc + khoảng ngày), mỗi phần tử stdClass: `id, type, money_value, money_value_exchange, exchange_rate, currency_id, currency_name, invoiceable_id, invoiceable_type, invoiceable_code, contractable_id, contractable_type, contractable_code, invoiceable_date_accounting, employee_name, department_name, note, ref_numbers, ref_names`.
- `summary(Request $request, Collection $rows): array` → `['opening' => float, 'debit' => float, 'credit' => float, 'closing' => float, 'by_currency' => [['currency_id','currency_name','debit','credit','debit_exchange','credit_exchange']]]`.
- `search(Request $request): array` → `['data' => trang dòng, 'summary' => summary(), 'meta' => ['total','current_page','per_page','last_page']]`.

- [ ] **Step 1: Test.** Fixture tự chèn trong transaction: 1 TK cha mới (`identify_number` duy nhất, `is_account_follow_dept = 1`) + 1 TK con trực tiếp + 1 TK cháu; vài `account_details` (đủ cột NOT NULL thật — đọc `information_schema` trước) với `invoiceable_date_accounting` năm 2000 để cô lập; NV từ `employee_infos` có công ty; cấp quyền qua `employee_has_permissions` (khuôn `FastDeliveryTestCase`).

```php
public function test_balances_only_employee_rows(): void
// đầu kỳ: Nợ 100 (01/01/2000, có NV) + Có 30 (có NV) + Nợ 999 (KHÔNG NV); kỳ 02-31/01/2000: Nợ 50, Có 20 (có NV), Nợ 777 (không NV)
// ⇒ opening 70, debit 50, credit 20, closing 100; count(rows) == 2
public function test_account_includes_direct_children_only(): void
// bút toán TK con ra, TK cháu không ra
public function test_date_range_whole_day(): void
// bút toán 31/01/2000 23:00 ra khi date_to '31/01/2000' và khi '2000-01-31'
public function test_scope_company_or_self(): void
// quyền công ty: thấy employee_company_id = công ty mình + bút toán employee_id = mình ở công ty khác; gửi company_id công ty khác ⇒ chỉ còn dòng của mình; quyền tổng công ty thấy hết; scopeFlags() đúng
public function test_invoiceable_types_or_groups(): void
// 3 bút toán: PXK type 1, PXK type 2, BillIncome ⇒ chọn ['…ProductExport-1', '…BillIncome'] ra đúng 2 dòng
public function test_account_ref_filter_consistent(): void
// bút toán có 2 đối ứng (TK A, TK B; A có id nhỏ hơn) trước kỳ và trong kỳ ⇒ lọc account_ref_id = B: opening và rows cùng có; ref_numbers của dòng chứa cả A và B
public function test_currency_totals_and_exchange_rate(): void
// 2 bút toán USD (rate 25000) + 1 VNĐ ⇒ by_currency 2 nhóm, debit/credit nguyên tệ + quy đổi đúng; rows[*].exchange_rate == 25000
public function test_other_filters(): void
// contract_code LIKE (escape %), invoice LIKE, note LIKE (ghi chú phiếu thu), type 1/2, work_id, money_from/money_to, customer_contract_id, keyword (số chứng từ / số HĐ)
```

- [ ] **Step 2: Chạy, thấy FAIL** — `php vendor/bin/phpunit Modules/Finance/Tests/Feature/EmployeeDebtDetailServiceTest.php` → class không tồn tại.
- [ ] **Step 3: Seeder** — 2 dòng `$this->perm([...])` + comment 2 dòng (port ERP 02/11/2026, kiểm bằng trait trong `EmployeeDebtDetailService`); `permission:sync --dry-run` báo thêm đúng 2 quyền này (+ quyền người khác chưa sync), rồi chạy thật.
- [ ] **Step 4: Viết service.** Join / select / sắp xếp theo spec 4.2; `GROUP_CONCAT(DISTINCT …)` đối ứng theo `ad.id`; lọc TK đối ứng bằng `whereExists` trên `account_detail_refs`; đầu kỳ dùng chung hàm áp phạm vi + lọc (trừ ngày) với `invoiceable_date_accounting < Từ ngày 00:00:00`; ngày nhận `d/m/Y` hoặc `Y-m-d`; LIKE qua `escapeLikeKeyword()`; phạm vi công ty: `where(fn => employee_company_id = info.company_id (bỏ vế này nếu null) OR employee_id = auth.id)`.
- [ ] **Step 5: Chạy test, PASS.**

### Task 2: Controller + route (danh sách, meta, Excel, In)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/EmployeeDebtDetailController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (nhóm mới cạnh `/customer-debt-details`), `EmployeeDebtDetailService.php` (thêm `meta`, `exportRows`, `printHtml`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/EmployeeDebtDetailApiTest.php`

**Interfaces — Produces:**
- `GET /api/v1/finance/employee-debt-details` → `{data: [...dòng đã định dạng sẵn khoá như rows()], summary, meta: {..., permissions: scopeFlags()}}`
- `GET …/meta` → `{accounts: [{id, text: "số hiệu - tên"}], invoiceable_types: INVOICEABLE_TYPES, currencies: [{id,name}], works: [{id,text}], permissions}`
- `GET …/export-rows?page&type_report` → `{headings, widths, rows, total}`; trang 1 trả hết (không trần), trang sau rỗng. Dòng đầu là 3 dòng tổng (đầu kỳ / phát sinh / cuối kỳ — mẫu ngoại tệ: mỗi loại tiền 1 dòng phát sinh), cột theo spec 4.4 + mục 6 (nhãn "NVKD"), số trả kiểu SỐ.
- `GET …/print-list-data` → khuôn `CustomerDebtCompareController::printListData` + trait `LimitsPrintListRows` (`printListPayload($html, $total)` + `landscape: true`); HTML do service dựng (spec mục 5), letterhead `companies.header` theo công ty người xem.

- [ ] **Step 1: Test.**

```php
public function test_forbidden_without_permission(): void
// 4 endpoint đều 403 với NV không quyền
public function test_validation(): void
// thiếu account_id / date_from / date_to ⇒ 422 lỗi theo ô; date_to < date_from ⇒ 422 "Đến ngày phải lớn hơn hoặc bằng Từ ngày"
public function test_index_paginates_10_and_returns_summary(): void
// 12 bút toán ⇒ trang 1 có 10, meta.total 12, summary trên cả 12, meta.permissions đúng
public function test_meta_accounts_follow_dept_only(): void
// TK is_account_follow_dept = 0 không có trong meta.accounts
public function test_export_rows_includes_summary_rows(): void
// mẫu VNĐ: headings y spec (cột "NVKD"), rows[0..2] là 3 dòng tổng, sau đó dòng dữ liệu; total = count(rows)
public function test_print_list_data_truncates_over_limit(): void
// override printListMaxRows qua subclass trong container ⇒ truncated = true, không có HTML; dưới trần ⇒ HTML chứa "SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN" và số hiệu TK
```

- [ ] **Step 2: Chạy, FAIL (404).**
- [ ] **Step 3: Viết controller + route + `meta` / `exportRows` / `printHtml`.** Câu validate y khuôn `CustomerDebtDetailController::validateDates`.
- [ ] **Step 4: Chạy test Task 1 + 2, PASS.**

### Task 3: Màn FE + menu + vào bằng URL

**Files:**
- Create: `hrm-client/pages/finance/employee-debt-details/index.vue`, `…/components/constants.js`
- Modify: `hrm-client/components/subsystem-menu/finance.js:430` (thêm `link: '/finance/employee-debt-details'`)

**Interfaces — Consumes:** Task 2 API.

- [ ] **Step 1: Dựng trang** theo khuôn `pages/sale/customer-debt-details/index.vue` + `customer-debt-compare` (In → Xuất Excel → Cấu hình cột). Bộ lọc spec 4.3: org (`V2BaseCompanyDepartmentFilter` với `meta.permissions`, is_department/is_part = false), Tài khoản \*, khoảng ngày \* (`rangeKeys: ['date_from','date_to']`), TK đối ứng, Đơn hàng/Hợp đồng, Loại chứng từ (multiple), Số chứng từ, Ghi chú, Loại tiền, Mẫu (1 VNĐ mặc định / 2 Ngoại tệ), Khách hàng (`V2BaseSelectRemote` `assign/customers/search` → `customer_contract_id`), Chỉ tiêu Nợ/Có, Mã vụ việc, Số tiền từ/đến (gửi số thuần) + ô tìm nhanh. Chưa đủ 3 ô bắt buộc ⇒ không gọi API, báo đỏ dưới ô (`field.error`, khuôn #11604). Watcher bộ lọc dùng `changedFields.every(ignored)` (bài học màn trước).
- [ ] **Step 2: Bảng** theo `type_report`: cột spec 4.4 (mẫu Ngoại tệ có header 2 tầng), 3 dòng tổng đầu bảng (dương cột Nợ, âm cột Có; mẫu ngoại tệ số ròng mỗi loại tiền), link `invoiceableLink(type,id)` / `contractLink(type,id)`, số `toLocaleString('en-US', {maximumFractionDigits: 2})`. `columnScreenKey` / `localStorageKey` = `employee_debt_details`, phân trang 10.
- [ ] **Step 3: URL** — `mounted` đọc query spec 4.6 (đè localStorage; ngày `d/m/Y` đổi sang `Y-m-d` cho datepicker); `reload=1` + đủ ô bắt buộc ⇒ tự tải.
- [ ] **Step 4: Bấm thử Playwright** (gán tạm quyền tổng công ty cho tài khoản local, gỡ sau): chọn TK 141, kỳ 01/01/2026–31/10/2026, chờ ≥ 3s mỗi ô lọc; đối chiếu đầu kỳ / phát sinh / cuối kỳ với số tính bằng tinker; mẫu Ngoại tệ; vào bằng URL drill-down; không quyền ⇒ trang 403. Chụp 1366px, xem ảnh. Đóng browser.

### Task 4: In + Xuất Excel trên FE

**Files:** Modify: `hrm-client/pages/finance/employee-debt-details/index.vue`

- [ ] **Step 1:** In = `reportPrintPreviewMixin.openPrintList('finance/employee-debt-details', params, 'Xem trước sổ chi tiết công nợ nhân viên')` + `ReportPrintPreviewModal`.
- [ ] **Step 2:** Xuất = `exportListFile({endpoint: 'finance/employee-debt-details/export-rows', docTitle: 'SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN (TỪ NGÀY … ĐẾN NGÀY …)', fileName: 'so_chi_tiet_cong_no_nhan_vien.xlsx', …})`, không popup chọn trường (ERP xuất đủ cột theo Mẫu).
- [ ] **Step 3:** In thật + xuất thật trên local; xem ảnh bản in, đọc file Excel (ExcelJS bằng node 22) kiểm 3 dòng tổng + số là số.

### Task 5: Hoàn tất

- [ ] Chạy lại `EmployeeDebtDetailServiceTest`, `EmployeeDebtDetailApiTest` — dán output.
- [ ] Review toàn nhánh (reviewer mới), sửa Critical/Important theo TDD.
- [ ] Cập nhật `.plans/gop-db/STATUS.md`, memory `project_ke_toan_cong_no.md` (mục mới cuối file). Commit khi user bảo.

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Review toàn nhánh bắt 1 Critical + 2 Important, đã sửa theo TDD: (C1) kỳ dài (≥ ~5 tháng) trên TK nhiều bút toán làm màn/Excel/In lỗi 500 do truy vấn TK đối ứng vượt 65.535 tham số → phân trang bằng SQL `LIMIT`, tổng phát sinh/tổng theo loại tiền 1 câu `GROUP BY`, TK đối ứng chỉ lấy cho dòng đang hiện, In vượt 2.000 dòng thì dừng, Excel tải từng trang 2.000 dòng (test 66.000 bút toán); (I1) đổi trang không tính lại dòng tổng; (I2) vào bằng link drill-down không dính bộ lọc cũ. Kèm: bút toán 0 đồng hiện "0" đúng phía Nợ/Có; tham số lạ trên URL không làm lỗi trang.
- [x] 03/11/2026 — Spec đổi lúc làm: lọc loại con của phiếu xuất/nhập (Xuất bán, Xuất KM…) giữ đúng kết quả ERP (mã loại con ERP là mã phiếu yêu cầu, "sửa" thì ra rỗng); chỉ sửa lỗi trang.
- [x] 03/11/2026 — Đối chiếu số TK 141 01/01–31/10/2026 khớp SQL tính tay; mẫu Ngoại tệ, bộ lọc, In, Excel (1.698 dòng) bấm thử local đạt. 15 test BE qua.
- [x] 03/11/2026 — Commit api `d1d77cadd`, client `3e6581b38` (nhánh `feat/so-chi-tiet-cong-no-nv`). Theo user: sửa ô số chuyến xe làm luôn trên nhánh đang làm (client `d59dec8d8`), gỡ worktree `cxch`.
- [x] 03/11/2026 — Sửa lỗi bấm Làm mới gọi API 2 lần (đi cùng commit Bảng cân đối): `handleReset` báo trước cho watcher bộ lọc. Ô Số tiền = 0 được bỏ qua như ERP.
- [x] 03/11/2026 — Lên `origin/develop` cùng merge Bảng cân đối (api `66ce147dd`, client `66a3d7d47`). Dev cần `permission:sync`.
- [ ] Chờ user: thêm index `account_details` (TK lớn 6 tháng ~6s → ~2,7s); xoá nhánh local `feat/chuyen-xe-cho-hang` (còn commit cũ `f3273c418` chưa push).

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Lỗi #12013 (Sổ chi tiết công nợ nhân viên): gộp ô Số tiền từ/đến thành một ô "Số tiền" định dạng 1,234,567 như màn YC điều chỉnh công nợ.
- [x] 05/11/2026 — Lỗi #12013: cùng bộ lọc mà dữ liệu khác ERP (TK 131 gần như trống) — ERP lấy mọi bút toán của TK, kể cả bút toán không gắn nhân viên, chỉ Số dư đầu kỳ mới lọc "phải có nhân viên"; HRM lọc "phải có nhân viên" cho mọi dòng theo spec mục 8.2 (02/11) → sửa theo ERP (`EmployeeDebtDetailService`), 4 file test liên quan qua. Commit api `280c343e6`, client `fcde078c1` (develop, đã push).
- [ ] Chờ user xác nhận đảo spec mục 8.2; spec `docs/superpowers/specs/gop-db/2026-11-02-so-chi-tiet-cong-no-nhan-vien-design.md` chưa cập nhật theo.

## Ngày 07/11/2026 (@junfoke)
- [x] 07/11/2026 — Fix phản hồi #12063 (In Sổ chi tiết công nợ nhân viên): 2 dòng "Từ ngày / Đến ngày" gộp thành 1 dòng "Thời gian: Từ dd/mm/yyyy đến dd/mm/yyyy"; đặt độ rộng cột cố định (trước đây cột Đơn hàng/Hợp đồng phình gần 1/3 bảng, Tên tài khoản bị bóp 4–5 dòng) — mã HĐ/số chứng từ dài xuống dòng trong cột, số tiền và ngày không bẻ đôi. Đã xem ảnh mẫu VNĐ (11 cột) + Ngoại tệ (15 cột). Phần in dùng chung nên bản in Sổ chi tiết công nợ NCC + Bảng cân đối công nợ NV cũng đổi sang dòng "Thời gian". Commit api `18e72f6b9` (develop, đã lên `origin/develop`).
- [x] 07/11/2026 — Fix phản hồi #12068 (phần khối ký tên dùng chung): "Người lập / Kế toán trưởng" trên bản in không còn bị đóng khung — popup xem trước kẻ khung mọi ô bảng nên khối ký tên đổi từ bảng sang `div` dàn ngang; áp cho cả 3 bản in (Sổ chi tiết công nợ NV, Sổ chi tiết công nợ NCC, Bảng cân đối). Xem chi tiết ở plan Bảng cân đối công nợ NV.
- [ ] 07/11/2026 — Đang làm #12069 (cùng phiên): ô Nhân viên ở bộ lọc 2 màn công nợ nhân viên không tìm ra NV đã nghỉ (vd "Trần Văn Chung" 10710037) — user đồng ý sửa component dùng chung `V2BaseCompanyDepartmentFilter` (thêm prop bật công tắc "nhân viên đã nghỉ", ~119 màn dùng nên mặc định tắt), bật prop ở 2 màn công nợ NV. Chưa commit, đang kiểm trên trình duyệt.
