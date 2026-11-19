# Báo cáo công nợ khách hàng quá hạn — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP "Báo cáo công nợ quá hạn" sang HRM thành "Báo cáo công nợ khách hàng quá hạn" (chỉ tiêu "Xét theo quy chế") + 2 cột Ngày BGNT / Quy chế ở dòng HĐ.

**Architecture:** BE chỉ đọc: 1 service dựng truy vấn 2 tầng y công thức ERP `HandleDebtOverDueService` (gom theo HĐ con → gom theo HĐ gốc) + dòng khai đầu kỳ, phạm vi qua `CustomerDebtScope`. FE 1 màn Nuxt dựng cây Phòng→NV→KH→HĐ (kiểu 1) hoặc KH→HĐ (kiểu 2) từ dòng HĐ phẳng, In + Excel dựng ở FE từ `export-rows`.

**Tech Stack:** Laravel 8 (`hrm-api/Modules/Finance`), Nuxt 2 (`hrm-client`), ExcelJS, PHPUnit trên DB gộp thật `erp_hrm_check` (DatabaseTransactions).

**Spec:** `HRM/.plans/bao-cao-cong-no-khach-hang-qua-han/design.md`

## Global Constraints

- Nhánh `develop` ở cả `hrm-api` và `hrm-client`. KHÔNG sửa ERP. KHÔNG migrate, KHÔNG sửa DB prod/remote.
- Chỉ làm chỉ tiêu 2 "Xét theo quy chế"; KHÔNG ô chọn chỉ tiêu, KHÔNG popup chi tiết (Chỉ tiêu 1 = anh Nam).
- Tên màn: **"Báo cáo công nợ khách hàng quá hạn"**; menu: `{ n: 'Công nợ KH quá hạn', link: '/sale/customer-debt-overdue' }`.
- "Báo cáo theo": `1` = "Theo phòng ban – nhân viên", `2` = "Theo khách hàng".
- Công thức tiền/ngày giữ y ERP: `account_id = 22`; `contractable_type IN ('App\Model\Sale\Firm\Contract\FirmContract','App\Model\Customers\WrServiceContract')`.
- Ngày truyền qua binding, KHÔNG nối chuỗi SQL.
- Quyền: dùng lại `sale.bao_cao_xu_ly_no_qua_han.view` (thêm `'hrm'` vào `platforms`), KHÔNG gate vào màn, phạm vi qua `CustomerDebtScope`.
- Số `toLocaleString('en-US')`, ô 0 hiện `-`; ngày `dd/mm/yyyy`; Excel ô số thật + numFmt `'#,##0;-#,##0;""'`.
- FE chỉ dùng `V2Base*`; nút theo skill `button-convention` (`mr-2 mb-2`, nút cuối `mb-2`); bảng theo `report-styles`; In theo `print-page`.
- Commit chỉ file của feature này; push: `git pull -q --rebase --autostash && git push -q origin develop`; trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Đến ngày để trống / Từ ngày > Đến ngày** → 422 với câu "Vui lòng chọn thời gian" / "Đến ngày phải lớn hơn hoặc bằng Từ ngày." (không văng SQL như ERP cũ). → test `test_validate_ngay` (Task 1).
2. **HĐ gốc có phụ lục giảm (firm type 3/6/10, wr type 4)** → số tiền phụ lục trừ đi, số ngày quá hạn không cộng dòng giảm. → test `test_phu_luc_giam_tru_tien_khong_cong_ngay` (Task 1).
3. **HĐ khai đầu kỳ trùng HĐ đã có ở nguồn chính** → chỉ 1 dòng, không cộng đôi vào TỔNG. → test `test_dong_khai_dau_ky_bo_hd_trung` (Task 1).
4. **Người không có quyền** → chỉ thấy HĐ mình lập, kể cả dòng TỔNG. → test `test_khong_quyen_chi_thay_hd_minh_lap` (Task 1).
5. **HĐ gốc thiếu `handover_date`/`over_date`** → ô Ngày BGNT/Quy chế trống, không lỗi `Invalid date`/`0`. → test `test_cot_bgnt_quy_che_null_tra_null` (Task 1) + kiểm tay ở Task 3.

---

### Task 1: BE — service, controller, route, quyền

**Files:**
- Create: `hrm-api/Modules/Finance/Services/CustomerDebt/CustomerDebtOverdueReportService.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/CustomerDebtOverdueController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm group ngay sau `customer-debt-by-employee`, ~dòng 2101)
- Modify: `hrm-api/app/Support/Permissions/Catalog/sale.php:1133` (thêm `'hrm'` vào `platforms` của `sale.bao_cao_xu_ly_no_qua_han.view`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/CustomerDebtOverdueReportTest.php`

**Interfaces:**
- Produces (HTTP, prefix `finance/customer-debt-overdue`):
  - `GET /meta` → `data: { scope: CustomerDebtScope::flags() }`
  - `GET /` params `date_from`, `date_to` (bắt buộc), `company_id`, `department_id`, `part_id`, `employee_id`, `customer_id`, `contract_code`, `report_type` (1|2, mặc định 1), `page`, `per_page` (mặc định 20) → `{ code, message, data: Row[], total: Totals, meta: { current_page, last_page, total } }`. Phân trang theo dòng HĐ đã sắp; FE tự dựng cây.
  - `GET /export-rows` cùng params + `page`, `per_page` (≤ 5000, mặc định 2000) → `data: { rows: Row[], total: Totals, has_more: bool }`.
  - `Row` = `{ contract_id, contract_code, contractable_type: 'firm'|'wr', customer_id, customer_code, customer_name, department_id, department_name, employee_id, employee_code, employee_name, company_id, part_id, handover_date: 'Y-m-d'|null, over_date: int|null, total_after_vat, begin, debt, has, number_overdue, is_declared: bool }` (số dạng float).
  - `Totals` = `{ total_after_vat, begin, debt, has, number_overdue }`.
- Service: `search(Request $r): array`, `exportRows(Request $r): array`, `meta(): array`, nội bộ `rows(Request $r): Collection` (đủ dòng đã sắp `department_id desc`, rồi customer, rồi contract_code).

- [ ] **Step 1: Viết test lỗi** — class `CustomerDebtOverdueReportTest extends TestCase`, `use DatabaseTransactions, BuildsMonitorContractFixtures, GrantsPermissionScope;` setUp copy `MonitorContractFirmSourceTest::setUp` (NV thường, xoá role/permission, `actingAs(..., 'api')`). Gọi service qua helper `rows(array $ids, array $params)` lọc `contract_id IN $ids`. Ledger qua `addLedger(FIRM|WR, $id, 22, 1|2, $amount, <BillIncome class>, $date)`. Các test (params mặc định `date_from=2026-10-01`, `date_to=2026-10-31`):
  - `test_hd_qua_han_dung_so_lieu_erp`: firm gốc `payment_overdue_date=2026-10-11`, `handover_date=2026-09-11`, `over_date=30`, `total_after_vat=50tr`; Nợ 22 10tr ngày 2026-09-20, Nợ 5tr 2026-10-05, Có 3tr 2026-10-10 → 1 dòng: `begin=10e6, debt=5e6, has=3e6, number_overdue=20, total_after_vat=50e6, handover_date='2026-09-11', over_date=30, is_declared=false`.
  - `test_phu_luc_cong_vao_hd_goc`: phụ lục type 2 `parent_contract_id=gốc`, Nợ 2tr trong kỳ → 1 dòng mang `contract_id` + `contract_code` của gốc, `debt` = tổng gốc+phụ lục, `handover_date/over_date` của **gốc**.
  - `test_phu_luc_giam_tru_tien_khong_cong_ngay`: thêm phụ lục firm type 3 Nợ 1tr → `debt` giảm 1tr; `number_overdue` chỉ từ dòng tăng.
  - `test_khong_qua_han_hoac_het_no_bi_loai`: `payment_overdue_date=2026-11-05` → không có dòng; HĐ khác Có = Nợ → không có dòng.
  - `test_wr_contract`: wr gốc + phụ lục `parent_id`, `contractable_type='wr'`.
  - `test_dong_khai_dau_ky_bo_hd_trung`: insert `declare_debt_beginning` (`is_overdue=1`, `acceptance_handover_date=2026-09-01`, `type_dept=1`, `dept_value=7e6`, `deptable_type=FIRM`, `deptable_id` = HĐ không có ledger) → 1 dòng `is_declared=true, begin=7e6, debt=0, has=0, number_overdue=60, handover_date='2026-09-01', over_date=null`; bản khai thứ 2 trỏ HĐ đã có ở nguồn chính → không thêm dòng, `total.begin` không đổi.
  - `test_khong_quyen_chi_thay_hd_minh_lap`: HĐ `created_by` = người khác → không thấy, `total` không tính; `grantPermissionScope($me, 'sale.bao_cao_xu_ly_no_qua_han.view', <scope tổng cty>)` → thấy.
  - `test_cot_bgnt_quy_che_null_tra_null`: gốc `handover_date=null, over_date=null` → `null` cả 2 (không `0`, không `''`).
  - `test_validate_ngay` (API): thiếu `date_to` → 422 `Vui lòng chọn thời gian`; `date_from > date_to` → 422 `Đến ngày phải lớn hơn hoặc bằng Từ ngày.`
  - `test_bao_cao_theo_khach_hang_cung_tong`: `report_type=2` trả cùng tập dòng và cùng `total` như `report_type=1` (chỉ khác thứ tự: theo customer rồi contract_code).

- [ ] **Step 2: Chạy, xác nhận FAIL** — `cd hrm-api && php artisan test Modules/Finance/Tests/Feature/CustomerDebtOverdueReportTest.php` → FAIL "class not found".

- [ ] **Step 3: Cài service.** Tầng trong = bản sao `HandleDebtOverDueService::getData` dòng 27-110 (ERP), khác ở:
  - ngày qua `?` binding (`selectRaw(..., [$from, $to])`), `whereDate('invoiceable_date_accounting','<=',$to)`;
  - thêm cột: `firm.created_by`/`wr.created_by` → `contract_created_by`; `COALESCE(firm_parent.handover_date, wr_parent.handover_date, firm.handover_date, wr.handover_date) as handover_date`; tương tự `over_date` (HĐ gốc trước, không có gốc thì chính nó — Q3);
  - giữ y: `part_id = firm.part_id`, `department_id` = phòng của NV lập, `HAVING number_overdue >= 0`.
  - Tầng ngoài: `DB::query()->fromSub($inner,'result')`, select có dấu theo `type` như ERP dòng 113-121 + `MAX(result.handover_date)`, `MAX(result.over_date)` (cùng 1 gốc nên bằng nhau), group `parent_contractable_id, contractable_type`, `havingRaw('(begin + debt - has) > 0 AND number_overdue > 0')`. Phạm vi: `(new CustomerDebtScope('sale.bao_cao_xu_ly_no_qua_han.view'))->apply($q, 'result.')`; lọc request như ERP dòng 142-188.
  - Dòng khai đầu kỳ: port `getDeclareOverDueRows` (ERP dòng ~250-330) bằng query builder (join HĐ theo `deptable_type`), áp CÙNG phạm vi (lọc collection theo `company_id/department_id/part_id/employee_id` + `CustomerDebtScope` — dựng where tương đương trên query khai báo, cột `created_by` của HĐ là `contract_created_by`), bỏ key `id-type` có ở nguồn chính, `handover_date = acceptance_handover_date`, `over_date = null`.
  - `contractable_type` trả `'firm'|'wr'` (map từ class string). Tổng = cộng trên toàn bộ dòng sau lọc (kể cả dòng khai).
- [ ] **Step 4: Cài controller + route + Catalog.** Controller khuôn `CustomerDebtByEmployeeController` (validate `date_from`/`date_to` với đúng message ở test). Route group `customer-debt-overdue` ( `/`, `/meta`, `/export-rows`), không `checkPermission`. Catalog thêm `'hrm'`, chạy `php artisan permission:catalog-sync` trên DB local.
- [ ] **Step 5: Chạy test PASS** — lệnh ở Step 2 → toàn bộ PASS.
- [ ] **Step 6: Đối chiếu ERP** — với DB chung, chạy cùng `date_from=2026-10-01&date_to=2026-10-31` (super admin ERP / phạm vi tổng HRM): số dòng, Σbegin/debt/has/number_overdue khớp 100% với `HandleDebtOverDueService::getData(..., 'total')` (gọi qua tinker ERP, không sửa ERP). Ghi kết quả vào cuối `design.md` mục "Đối chiếu".
- [ ] **Step 7: Commit** — `git add` 5 file trên → `feat(finance): API báo cáo công nợ khách hàng quá hạn`.

### Task 2: FE — màn danh sách (bộ lọc + bảng cây) + menu

**Files:**
- Create: `hrm-client/pages/sale/customer-debt-overdue/index.vue`
- Create: `hrm-client/pages/sale/customer-debt-overdue/components/OverdueTable.vue`
- Create: `hrm-client/pages/sale/customer-debt-overdue/components/build-tree.js`
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js` (thay chữ trơn `'Công nợ quá hạn'`)

**Interfaces:**
- Consumes: API Task 1.
- Produces: `buildTree(rows: Row[], reportType: 1|2): Node[]` — `Node = { type: 'department'|'employee'|'customer'|'contract', no: '1'|'1.2'|'1.2.3'|'1.2.3.4', name, totals: Totals, row?: Row }`; kiểu 1 Phòng→NV→KH→HĐ, kiểu 2 KH→HĐ; `totals.number_overdue` của nhóm = Σ con (như ERP blade). Dùng chung cho bảng, In, Excel.

- [ ] **Step 1:** Khuôn copy `pages/sale/customer-debt-by-employee/index.vue` (bộ lọc `V2BaseCompanyDepartmentFilter` + `meta.scope`, Khách hàng search server-side, ô Hợp đồng gõ mã, `V2BaseDatePicker` Từ/Đến bắt buộc mặc định đầu tháng → hôm nay, `V2BaseSelect` Báo cáo theo 2 option ở Global Constraints). Nút: Lọc, Làm mới, In, Xuất Excel (In/Excel nối ở Task 3, tạm ẩn).
- [ ] **Step 2:** `OverdueTable.vue`: cột STT · Tên · **Ngày BGNT** · **Quy chế** · Giá trị HĐ thực tế · Số dư quá hạn đầu kỳ · Phát sinh tăng · Phát sinh giảm (hiện `-has`) · Số dư quá hạn cuối kỳ (`begin+debt-has`) · Số ngày quá hạn; kiểu 2 thêm cột Nhân viên sau Tên. Dòng TỔNG CỘNG đầu bảng từ `total`. Ngày BGNT/Quy chế chỉ in ở node `contract`. Mã HĐ là link — copy cách `MonitorContractTable.vue` (firm/wr → màn HRM nếu có, không thì ERP tab mới). Style theo `report-styles`.
- [ ] **Step 3:** Menu: trong `sale-hub.js` thay `'Công nợ quá hạn'` bằng `{ n: 'Công nợ KH quá hạn', link: '/sale/customer-debt-overdue' }`.
- [ ] **Step 4: Kiểm** — `grep -rn '<input \|<textarea\|<select \|<button \|<label ' pages/sale/customer-debt-overdue | grep -v V2Base` rỗng; grep `vi-VN` cho số rỗng; Playwright MCP `http://127.0.0.1:3000/sale/customer-debt-overdue`: lọc tháng 10/2026 → TỔNG khớp Step 6 Task 1, đổi Báo cáo theo → cây đổi, TỔNG không đổi; để trống Đến ngày → báo lỗi dưới ô.
- [ ] **Step 5: Commit** (hrm-client) — `feat(sale): màn báo cáo công nợ khách hàng quá hạn`.

### Task 3: FE — In + Xuất Excel

**Files:**
- Create: `hrm-client/pages/sale/customer-debt-overdue/print.vue`
- Create: `hrm-client/pages/sale/customer-debt-overdue/components/export-excel.js`
- Modify: `hrm-client/pages/sale/customer-debt-overdue/index.vue` (nối 2 nút)

**Interfaces:**
- Consumes: `GET /export-rows` (lặp qua `utils/export/listExportFile.js`), `buildTree()` Task 2.
- Produces: `exportCustomerDebtOverdue(rows: Row[], total: Totals, periodText: string, reportType: 1|2): Promise<void>`, file `bao_cao_cong_no_khach_hang_qua_han.xlsx`.

- [ ] **Step 1:** `export-excel.js` khuôn `pages/sale/monitor-contract-implement/components/export-excel.js`: tiêu đề `BÁO CÁO CÔNG NỢ KHÁCH HÀNG QUÁ HẠN`, dòng "Từ ngày dd/mm/yyyy đến ngày dd/mm/yyyy", tiêu đề 1 tầng đúng cột màn, TỔNG CỘNG đầu, dòng nhóm in đậm; Ngày BGNT là chuỗi `dd/mm/yyyy` (dùng `toVnDate`), Quy chế số; ô tiền số thật + `NUM_FMT`.
- [ ] **Step 2:** `print.vue` khổ ngang (`297mm`) theo skill `print-page`; nhận query lọc, tải đủ dòng qua `export-rows`, render cùng `buildTree` + TỔNG CỘNG.
- [ ] **Step 3: Kiểm** — Playwright: Xuất Excel tháng 10/2026 mở được, ô tiền là số (SUM cột = TỔNG), cột Ngày BGNT/Quy chế có giá trị ở dòng HĐ; In mở tab khung giấy ngang, nút In căn phải; HĐ gốc thiếu BGNT → ô trống.
- [ ] **Step 4: Commit + push** cả 2 repo lên `develop` theo Global Constraints; cập nhật memory.
