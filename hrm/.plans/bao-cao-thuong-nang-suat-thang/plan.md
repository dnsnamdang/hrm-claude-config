# Báo cáo thưởng năng suất tháng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Port ERP `report.commissionMonth` sang HRM `/sale/bonus-month-report` (3 nguồn HĐ firm/wr/hrm), đồng thời vá các lỗi sai số và lỗi quyền của màn ERP để hai bên ra cùng một số.

**Architecture:**
- **HRM BE** (`Modules/Finance/Services/BonusMonthReport/`): 1 truy vấn sổ 3351 TNST gom theo (HĐ, NV), dùng lại `BonusLedger`. 1 lớp `BonusMonthDstc` tính DSTC bằng map nạp sẵn theo khoá (không O(N²)). Gom Phòng → NV → HĐ, 1 dòng/NV. Phạm vi theo hồ sơ NV hiện tại.
- **HRM FE:** khuôn `pages/sale/bonus-contract-report`.
- **ERP:** sửa trong `CommissionMonthReportService`, `ReportController` và `commission_month.blade.php`, giữ cấu trúc cũ.

**Tech Stack:** HRM Laravel 8 / PHP 7.4, Nuxt 2; ERP Laravel 6; MySQL `erp_hrm_check` local.

**Spec:** `HRM/.plans/bao-cao-thuong-nang-suat-thang/design.md`. Phân tích ERP kèm số SELECT: `HRM/.plans/bao-cao-thuong-nang-suat-thang/erp-analysis.md`.

## Global Constraints

- **Nhánh:**
  - HRM: worktree từ `develop`, tên `wt-bonus-month-api` (hrm-api) và `wt-bonus-month-client` (hrm-client), nhánh `feature/bao-cao-thuong-nang-suat-thang`.
  - ERP: worktree `wt-bonus-month-erp` từ `develop_02`, cùng tên nhánh.
  - Không switch/reset repo chính, không bare `git stash`.
- **Repo chính hrm-api** đang có file chưa commit của phiên khác ("BC thưởng theo quý": `BonusQuarter*`, `api.php`, `accounting.php`). Không đụng tới. Khi gộp, `accounting.php` và `api.php` có thể xung đột: giữ cả hai, `'hrm'` chỉ thêm 1 lần.
- **Mã quyền:** `accounting.bao_cao_thuong_nang_suat_thang.view`, scopes 1-4. Thêm `'hrm'` vào `platforms`. Màn không gate.
- **API:** prefix `/api/v1/finance/bonus-month-report`, các route `/`, `/meta`, `/detail`, `/export-rows`, `/print-list-data`, middleware `auth:api`.
- **FE:** route `/sale/bonus-month-report`. Menu `{ n: 'Thưởng năng suất tháng', link: '/sale/bonus-month-report' }` ở `hrm-client/components/subsystem-menu/sale-hub.js`, nhóm 'Thưởng - Thu nhập'.
- **Hằng số:**
  - Work TNST.
  - Loại trừ `invoiceable_type`: BillPayment, BillPaymentAuthorization, ClosingEntry (dùng `BonusLedger::EXCLUDED_INVOICEABLE`).
  - HĐ hãng đã quyết toán: `firm_contracts.status = 10`.
  - Quyết toán loại 2: `firm_settlement_contract_detail.type = 2`.
  - Phân trang 10 phòng/trang.
  - File Excel `bao_cao_thuong_nang_suat_thang.xlsx`.
  - Tiêu đề in `BÁO CÁO THƯỞNG NĂNG SUẤT THÁNG`.
- **Morph HĐ:** firm `App\Model\Firm\FirmContract` (lấy đúng chuỗi từ `BonusLedger`/`BonusContractReportService`), wr `App\Model\WR\WrServiceContract`, HRM `Modules\Assign\Entities\Contract\Contract`. Chuỗi thật lấy từ `BonusContractReportService`.
- **phpunit trong worktree:** chạy với bootstrap ở scratchpad, prepend PSR-4 của worktree: `vendor/bin/phpunit --bootstrap <scratch>/bootstrap.php <file>`. Server API worktree chạy `php -S 127.0.0.1:8010` kèm router; client chạy cổng 3010.
- **Định dạng số:** `en-US`. Ô Excel là số thật kèm `#,##0`. Số 0 ở bản in hiện `-`.
- **DB:** không ghi prod/dev. Local `erp_hrm_check` chỉ SELECT, trừ fixture trong transaction của test.
- **Commit:** trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Không push, không merge khi chưa hỏi user.

## Review Focus

1. NV thuộc phòng có nhiều bộ phận (`parts`): phải ra đúng 1 dòng, tổng không nhân. Test ở Task 4.
2. NV quyền cấp Phòng/Công ty mà hồ sơ có `part_id`: vẫn thấy NV khác bộ phận trong phạm vi. Test ở Task 1.
3. HĐ hãng và HĐ DV trùng `id`, cùng có dòng `*_support_accounting` trùng `contractable_id`: thưởng không nhân đôi, popup không trộn. Test ở Task 2 và Task 5.
4. Thiếu dòng tỷ lệ hưởng, hoặc tổng TNST của HĐ = 0: DSTC = 0, không lỗi. Test ở Task 3.
5. Lọc Năm/Tháng rồi mở popup: popup cùng kỳ với bảng. Lọc kỳ rỗng, hoặc Tháng không Năm: 422. Test ở Task 5 và Task 6.

---

### Task 1: Worktree + Scope + catalog

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthScope.php`
- Modify: `hrm-api/app/Support/Permissions/Catalog/accounting.php` (mục `accounting.bao_cao_thuong_nang_suat_thang.view`: `'platforms' => ['erp', 'hrm']`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusMonthScopeTest.php`

**Interfaces:**
- Produces:
  - `class BonusMonthScope extends SalesIncomeScope` với `const CODE = 'accounting.bao_cao_thuong_nang_suat_thang.view'`.
  - `level(): string` thừa hưởng.
  - `apply($query, string $prefix, string $ownColumn): void`, override nhánh PART.
  - `employeeInScope(int $employeeId): bool`: kiểm NV qua `employees` → `employee_infos` → `departments`, dùng cùng `apply`.

- [x] **Step 1:** Tạo 2 worktree HRM và 1 worktree ERP như Global Constraints. Chép bootstrap phpunit vào scratchpad.
- [x] **Step 2:** Viết test. Khuôn: `SalesIncomeScopeTest`, fixture quyền: `Concerns/BuildsBonusLedgerFixtures::grantBonusContractScope`; tổng quát hoá nhận mã hoặc thêm hàm mới.
  - `test_khong_quyen_chi_thay_minh`
  - `test_cap_bo_phan_chi_bo_phan_cua_minh_khong_gom_bo_phan_quan_ly`: NV quản lý bộ phận B, thuộc bộ phận A. `ei.part_id IN (A)` hoặc chính mình.
  - `test_cap_bo_phan_khong_co_part_chi_thay_minh`: whereIn `[0]` hoặc chính mình.
  - `test_cap_phong_co_part_id_van_thay_nv_khac_bo_phan`: phạm vi là `department_id IN listManageDepartmentIds()`, không có điều kiện `part_id`.
  - `test_cap_cong_ty_va_tong_cong_ty`
  - `test_danh_muc_khai_hrm`: catalog có `'hrm'` trong `platforms`.
- [x] **Step 3:** Chạy test, kỳ vọng FAIL (class chưa có).
- [x] **Step 4:** Implement. Cấp PART: `$ids = [own part_id]`, không cộng `listManagePartIds()` (bám ERP, khác `SalesIncomeScope`). Không sửa `SalesIncomeScope`, vì đó là hàm dùng chung.
- [x] **Step 5:** Chạy test, kỳ vọng PASS. Commit `feat(finance): BC thuong NS thang — scope + catalog hrm`.

### Task 2: Số TNST theo (HĐ, NV) + thông tin HĐ

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthReportService.php`
- Create: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthPeriod.php`
- Modify (nếu cần): `hrm-api/Modules/Finance/Services/BonusContractReport/BonusLedger.php`. Chỉ được thêm, ví dụ tham số chọn cột. Test `BonusContractLedgerTest` phải xanh nguyên.
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusMonthReportServiceTest.php`

**Interfaces:**
- Consumes: `BonusMonthScope` (Task 1), `BonusLedger::sums(Request, array $groupBy, ?string $contractableType)`.
- Produces:
  - `BonusMonthPeriod::resolve(Request $r): array`
    - Trả `['start_date' => 'Y-m-d', 'end_date' => 'Y-m-d']`.
    - Năm + Tháng → ngày đầu/cuối tháng. Chỉ Năm → cả năm. Ngày → giữ nguyên.
    - Ném `ValidationException` khi không có kỳ, Tháng không Năm, ngày sai định dạng, hoặc `date_from > date_to`.
  - `BonusMonthReportService::contractRows(Request $r): Collection`. Mỗi phần tử gồm:
    - định danh HĐ: `contractable_type, contractable_id, contract_code, contract_status`;
    - khách hàng: `customer_id, customer_code, customer_name`;
    - `employee_id, commission_month (float)`.
    - **Không** áp quyền. Đây cũng là tập mẫu số DSTC.
    - Có lọc `contract_code` (=), `customer_id`. Bỏ cặp có `commission_month = 0`.
    - Join HĐ theo đúng `contractable_type`: firm (+ `customers.code`), wr, `hrm_contracts`.

- [x] **Step 1:** Viết test, fixture `ledgerRow()`.
  - `test_tnst_co_tru_no`: Có 100 + Nợ 30 → 70.
  - `test_bo_work_khac_va_invoiceable_loai_tru`
  - `test_bo_cap_bang_0`
  - `test_firm_va_wr_trung_id_khong_nhan_doi`: firm id 13 và wr id 13, mỗi bên 1 bút toán 50 → 2 dòng, mỗi dòng 50.
  - `test_hd_hrm_len_bang`
  - `test_loc_so_hd_va_khach_hang`
  - `test_period_nam_thang`
  - `test_period_thang_khong_nam_422`
  - `test_period_rong_422`
  - `test_period_ngay_sai_422`
- [x] **Step 2:** Chạy test, kỳ vọng FAIL.
- [x] **Step 3:** Implement. Lọc ngày theo `invoiceable_date_accounting` giữa 2 ngày (00:00:00 tới 23:59:59) qua `BonusLedger`.
- [x] **Step 4:** Chạy test, kỳ vọng PASS. Chạy lại `BonusContractLedgerTest` và `BonusContractReportServiceTest`, kỳ vọng PASS. Commit.

### Task 3: DSTC (`BonusMonthDstc`)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthDstc.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusMonthDstcTest.php`

**Interfaces:**
- Consumes: `contractRows()` (Task 2).
- Produces:
  - `new BonusMonthDstc(Collection $contractRows)`: nạp sẵn mọi map bằng ≤ 4 truy vấn `whereIn` theo id HĐ có trong tập. Không truy vấn trong vòng lặp. Các map:
    - `firm/wr_support_accounting.commission_sale`, khoá (type, id);
    - `*_support_accounting_employees.commission_sale_percent`, khoá (type, id, employee);
    - `settlement_contract_employees.commission_sale` chính thức, khoá (firm id, employee), `max(id)` khi trùng;
    - tổng TNST theo HĐ.
  - `value(array $contractRow, ?int $departmentLeadId): float`.
- **Công thức** (design §5 "DSTC"):
  - Firm `status = 10`: `settlement_contract_employees.commission_sale`. Chỉ lấy dòng có `settlement_contract_id IS NOT NULL`, qua `settlement_contract_departments` → `firm_settlement_contract_detail.type = 2`. Dòng `id` lớn nhất; không có thì 0.
  - Firm chưa quyết toán, và wr: `tnst_NV / tnst_tổng_HĐ × commission_sale_HĐ × tỷ_lệ / 100`.
    - `tỷ_lệ = 100` khi `employee_id === $departmentLeadId`. Ngược lại lấy percent của (type, id, NV); không có thì 0.
    - `tnst_tổng_HĐ = 0` thì 0.
  - HRM: 0.

- [x] **Step 1:** Viết test.
  - `test_da_qt_lay_dong_chinh_thuc_id_lon_nhat`: dòng nháp `settlement_contract_id NULL` giá trị 999, 2 dòng chính thức 100 (id nhỏ) và 200 (id lớn) → 200.
  - `test_da_qt_khong_co_dong_ra_0`
  - `test_chua_qt_ty_le_100`: commission_sale 1.000.000, NV 30 / tổng 100 → 300.000.
  - `test_chua_qt_ty_le_50_nhan_khong_chia` → 150.000.
  - `test_truong_phong_ty_le_100`
  - `test_thieu_dong_ty_le_ra_0`
  - `test_tong_tnst_0_ra_0`
  - `test_wr_dung_wr_support_accounting_theo_type`: firm cùng id có `commission_sale` khác, không được dùng.
  - `test_hrm_ra_0`
  - `test_so_truy_van_khong_tang_theo_so_dong`: `DB::enableQueryLog`, 1 dòng so với 50 dòng có cùng số query.
- [x] **Step 2:** Chạy, kỳ vọng FAIL. **Step 3:** Implement. **Step 4:** Chạy, kỳ vọng PASS. Commit.

### Task 4: Bảng Phòng → NV → HĐ, tổng, phân trang

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthReportService.php`
- Test: `BonusMonthReportServiceTest.php` (thêm)

**Interfaces:**
- Consumes: Task 1-3.
- Produces:
  - `rows(Request $r): Collection`:
    - Gắn NV vào phòng hiện tại: `employees` → `employee_infos` → `departments status = 1`. Không join `parts`.
    - Áp `BonusMonthScope::apply($q, 'ei.', 'e.id')`, cùng lọc `company_id` (d.company_id), `department_id`, `part_id` (ei), `employee_id`.
    - Mỗi phần tử: `department_id, department_code, department_name, department_lead_id, employee_id, employee_code, employee_name, contracts[]`.
    - `contracts[]` gồm: `contractable_type, contractable_id, contract_code, customer_code, customer_name, doanh_so_tieu_chuan, commission_month`.
  - `tree(Collection $rows): array`: mỗi phòng có `total_doanh_so_tieu_chuan`, `total_commission_month`, `employees[]`. Mỗi NV có 2 tổng và `contracts`.
  - `totals(array $tree): array`: trả `['doanh_so_tieu_chuan' => float, 'commission_month' => float]`, mặc định 0.
  - `search(Request $r): array`: trả `['data' => tree trang hiện tại, 'total' => totals toàn tập, 'pagination' => phân trang theo phòng (khuôn BonusEmployeeReportService::search)]`, `PER_PAGE = 10`.
  - Thứ tự sắp: `d.code, d.id, ei.code, e.id`, HĐ theo `contract_code`. Khuôn: `BonusEmployeeReportService::rows/tree/search`.

- [x] **Step 1:** Viết test.
  - `test_phong_nhieu_bo_phan_1_dong_moi_nv`: phòng có 3 parts, 2 NV → 2 NV, tổng phòng đúng.
  - `test_nv_phong_dong_khong_hien`
  - `test_dstc_dung_truong_phong_cua_phong_hien_tai`
  - `test_scope_own_chi_thay_minh_nhung_mau_so_dstc_tinh_ca_hd`: NV A 30, NV B 70, A không quyền xem B → A chỉ thấy mình. DSTC của A = 30% DS × tỷ lệ.
  - `test_tong_cong_toan_tap_khi_phan_trang`: 12 phòng, trang 2 có 2 phòng, `total` vẫn là tổng 12 phòng.
  - `test_ket_qua_rong_total_0`
- [x] **Step 2:** FAIL. **Step 3:** Implement. **Step 4:** PASS. Commit.

### Task 5: Popup chi tiết NV (HĐ → phiếu → mặt hàng)

**Files:**
- Modify: `BonusMonthReportService.php`, thêm `detail(Request $r): array`.
- Test: `BonusMonthReportServiceTest.php` (thêm)

**Interfaces:**
- Produces: `detail(Request $r): array`.
  - **Tham số:** `employee_id` (bắt buộc), kỳ (qua `BonusMonthPeriod`), `contract_code`, `customer_id`, `invoiceable_code` (=), `page`, `per_page` (mặc định 10).
  - **Trả:** `['data' => [HĐ...], 'pagination' => phân trang theo HĐ]`.
    - Mỗi HĐ: `contractable_type, contractable_id, contract_code, commission_month, invoices[]`.
    - Mỗi phiếu: `invoiceable_type, invoiceable_id, invoiceable_code, commission_month, products[]`.
    - Mỗi mặt hàng: `product_code, product_name, qty, price, amount`, với `amount = qty × price`.
  - **Gom:** theo (type, id) của HĐ, rồi (type, id) phiếu. Lấy mã từ sổ (`contractable_code`, `invoiceable_code`) để HĐ/phiếu đã xoá vẫn hiện.
  - **Mặt hàng:**
    - Chỉ cho phiếu xuất kho (`price`) và phiếu nhập kho (`supplier_price`). Nạp bằng 1 truy vấn `whereIn` mỗi loại cho trang hiện tại.
    - Morph type phải khớp cả chuỗi ERP (`App\Model\Warehouse\ProductExport`, `App\Model\Warehouse\ProductImport`) lẫn morph HRM nếu có. Bảng chi tiết: model HRM `Modules/Assign/Entities/Warehouse/ProductExportDetail`, `Modules/Finance/Entities/ProductImport/ProductImportDetail`. Tên bảng và cột `parent_id` phải đối chiếu với ERP `ProductExportDetail` / `ProductImportDetail`.
  - **Quyền:** NV ngoài phạm vi (`BonusMonthScope::employeeInScope`) → `AuthorizationException`, controller trả 403.

- [x] **Step 1:** Viết test.
  - `test_popup_gom_theo_type_id`: firm 13 và wr 13 → 2 HĐ.
  - `test_popup_phieu_va_tien`
  - `test_popup_mat_hang_pxk`: qty 2, price 50 → amount 100.
  - `test_popup_phieu_khac_khong_mat_hang`
  - `test_popup_cung_ky_nam_thang`: bút toán tháng 4 không lên khi lọc tháng 5.
  - `test_popup_ngoai_pham_vi_403`
  - `test_popup_hd_da_xoa_van_hien_ma_so`
- [x] **Step 2:** FAIL. **Step 3:** Implement. **Step 4:** PASS. Commit.

### Task 6: Bản in, controller, routes, API test

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BonusMonthReport/BonusMonthPrintTable.php` (khuôn `BonusEmployeePrintTable`)
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BonusMonthReportController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php`. Group `/bonus-month-report` đặt cạnh `/bonus-business-employee`, kèm comment kiểu các group bên cạnh.
- Test: `hrm-api/Modules/Finance/Tests/Feature/BonusMonthApiTest.php`

**Interfaces:**
- Produces (cho FE Task 7):
  - `GET /` → `search()` (`data`, `total`, `pagination`).
  - `GET /meta` → `{ permissions: { level }, years: [...] }`. Năm lấy từ sổ hoặc dải cố định, như `BonusContractReportController::meta`.
  - `GET /detail` → `detail()`.
  - `GET /export-rows` → `{ data: tree toàn tập, total }`.
  - `GET /print-list-data` → `{ html, header }`.
    - `html` = `BonusMonthPrintTable::list(array $tree, array $totals, bool $expand): string`.
    - Bố cục: thead 5 cột; dòng 2 là Tổng cộng (colspan 3); phòng in đậm; NV màu `#1abc9c`; HĐ chỉ khi `expand`; số 0 hiện `-`; `number_format` mặc định.
    - `header` lấy từ `companies.header` của công ty hồ sơ người in. Theo ERP, báo cáo không gắn chứng từ; chép `headerUrl()` từ `BillIncomePrintService`.
  - Lỗi kỳ trả 422, popup ngoài phạm vi trả 403.

- [x] **Step 1:** Viết test (khuôn `BonusContractApiTest`).
  - `test_index_can_dang_nhap`
  - `test_index_422_khi_thieu_ky`
  - `test_index_tra_tree_total_meta`
  - `test_detail_403_ngoai_pham_vi`
  - `test_export_rows_khong_phan_trang`
  - `test_print_list_data_expand_an_hien_dong_hd`
  - `test_print_rong_khong_loi`
- [x] **Step 2:** FAIL. **Step 3:** Implement. **Step 4:** PASS. Chạy toàn bộ `BonusMonth*Test` và `BonusContract*Test`. Commit.

### Task 7: FE màn + popup + Excel + In + menu

**Files:**
- Create: `hrm-client/pages/sale/bonus-month-report/index.vue`
- Create: `hrm-client/pages/sale/bonus-month-report/components/detail-modal.vue` (trên `V2BaseModal`)
- Create: `hrm-client/pages/sale/bonus-month-report/components/export-excel.js`
- Create: trang in, theo đúng khuôn trang in của `bonus-contract-report` (dùng lại cách màn đó in `print-list-data`).
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js`, thay chuỗi `'Thưởng năng suất tháng'`.

**Interfaces:** Consumes API Task 6.

- [x] **Step 1:** Copy khuôn `pages/sale/bonus-contract-report` (bộ lọc, bảng, In, Excel). Bộ lọc:
  - Năm, Tháng (disable khi đã có ngày, và ngược lại).
  - Từ ngày, Đến ngày.
  - Số HĐ, Khách hàng (search server-side).
  - Công ty / Phòng / Bộ phận / NV (theo khuôn bộ lọc tổ chức màn `bonus-business-employee`).
  - Checkbox "Show chi tiết".
- [x] **Step 2:** Bảng 5 cột, đúng thứ tự §5 "Bảng":
  - STT dạng `n` / `n.m` / `n.m.k`.
  - Tên NV là link mở popup.
  - Mã HĐ link về chi tiết HĐ theo nguồn, chép hàm link từ `bonus-contract-report`.
  - Phân trang theo phòng.
- [x] **Step 3:** Popup:
  - Nhận cùng kỳ, Số HĐ, KH với bảng, cộng ô "Phiếu hạch toán".
  - Phân trang riêng của popup.
  - Cột: STT | Tên hàng | Mã hàng | SL | Đơn giá tiêu chuẩn | Doanh số tiêu chuẩn | Thưởng NS tháng.
  - Dòng HĐ, dòng phiếu, dòng hàng.
- [x] **Step 4:** Excel: dữ liệu lấy từ `export-rows`. Ô số là số thật, `#,##0`. Tên file `bao_cao_thuong_nang_suat_thang.xlsx`.
- [x] **Step 5:** Tự kiểm 2 lệnh grep trong `HRM/CLAUDE.md`, phải rỗng: lệnh `V2Base` (HTML thô) và lệnh `vi-VN` cho số.
- [x] **Step 6:** Chạy client 3010 và API 8010, mở màn bằng Playwright MCP và kiểm lọc tháng 05/2026, Show chi tiết, popup, In, Excel. Commit.

### Task 8: Vá ERP — service + controller (6A.1-6, 10-12)

**Files (worktree ERP):**
- Modify: `app/Services/Reports/CommissionMonthReportService.php`
- Modify: `app/Http/Controllers/ReportController.php:4365-4430`

- [x] **Step 1:** Ghi số ERP **trước vá** vào `HRM/.plans/bao-cao-thuong-nang-suat-thang/doi-chieu.md`.
  - Kỳ: 05/2026 và năm 2026, phạm vi Tổng công ty.
  - Số cần ghi: Tổng cộng; phòng 47; HĐ hãng 13, 15 và HĐ DV 3948; 1 NV hưởng 50%.
  - Cách chạy: script tinker trong worktree ERP, gọi `CommissionMonthReportService`.
  - DB: trỏ `erp_hrm_check` bằng biến môi trường lấy từ HRM `.env`; trước khi chạy grep `DB_` để chắc không trỏ remote; không in mật khẩu.
- [x] **Step 2:** Sửa các lỗi:
  1. `getDataDepartment`: bỏ `leftJoin parts`, hoặc gom DISTINCT NV, để 1 dòng/NV.
  2. Áp quyền đúng cấp cao nhất. `is_part` chỉ áp khi scope đúng bằng PART; không có `part_id` thì chỉ thấy mình.
  3. Join `firm_support_accounting` / `wr_support_accounting` thêm điều kiện `contractable_type`.
  4. `getDoanhSoTieuChuan`:
     - Nhân `ti_le / 100`.
     - Thiếu dòng tỷ lệ thì 0.
     - Nhánh đã quyết toán chỉ lấy dòng chính thức `id` lớn nhất (`orderByDesc('id')` khi nạp map).
  5. `getDetailByEmployee` gom theo `contractable_type + contractable_id`. Mã HĐ/phiếu dùng `contractable_code` / `invoiceable_code` của sổ khi quan hệ null.
  6. `printListData` dùng `$data['total']['...'] ?? 0`.
  7. Query `FirmSupportAccountingEmployee::groupBy` đổi thành select có aggregate hoặc không groupBy, để chạy được với ONLY_FULL_GROUP_BY.
  8. Controller:
     - Bỏ `dd($e)`.
     - `commissionMonthSearchDetailData` kiểm phạm vi: NV phải nằm trong danh sách NV mà `getDataDepartment` cho phép; ngoài phạm vi trả 403.
- [x] **Step 3:** Chạy lại script Step 1 và ghi bảng **sau vá**. Kỳ vọng:
  - Phòng 47 về 16 NV.
  - HĐ 13, 15, 3948 hết nhân đôi.
  - NV 50% có DSTC = ¼ số cũ: số cũ chia 0,5, số mới nhân 0,5.
  - Không còn lỗi khi chạy năm 2026.
- [x] **Step 4:** `php -l` các file đã sửa. Commit trên nhánh ERP.

### Task 9: Vá ERP — view JS popup (6A.8-9)

**Files:** Modify: `resources/views/reports/commission_month.blade.php` (worktree ERP)

- [x] **Step 1:** Hàm mở popup gửi đủ `year`, `month`, `customer_id` như form chính. Back-end `getDetailByEmployee` đã dùng `filterDate`, nên nhận được.
- [x] **Step 2:** Popup dùng biến phân trang riêng (`detail.page`, `detail.total`), đọc đúng tên field tổng của response. Không ghi vào `current.page` của bảng chính.
- [x] **Step 3:** Kiểm tay trên ERP local nếu chạy được. Nếu không, ghi rõ "chưa kiểm trình duyệt" trong báo cáo. Commit.

### Task 10: Đối số HRM với ERP đã vá

- [x] **Step 1:** Trên `erp_hrm_check`, kỳ 05/2026 và năm 2026, phạm vi Tổng công ty. So HRM `search()` + `export-rows` với ERP đã vá (script Task 8) tại các điểm:
  - Tổng cộng (2 cột);
  - phòng 47;
  - 1 NV hưởng 50%;
  - HĐ 13, 15, 3948;
  - toàn bộ cặp (HĐ, NV).
  Kỳ vọng **0 lệch**.
- [x] **Step 2:** Đo thời gian HRM kỳ 1 năm, mục tiêu < 15s. Ghi kết quả vào `doi-chieu.md`, kèm bảng trước/sau vá ERP từ Task 8.

### Task 11: Playwright e2e

**Files:** Create: `HRM/e2e/tests/bonus-month-report.spec.ts` (khuôn `bonus-contract-report.spec.ts`)

- [x] **Step 1:** Spec gồm:
  - mở màn;
  - lọc Năm 2026 + Tháng 5, bảng có dòng Tổng cộng;
  - bật Show chi tiết, thấy dòng `n.m.k`;
  - bấm NV, popup mở, có dòng HĐ;
  - bấm In, thấy trang in;
  - bấm Excel, có file tải xuống.
  Chạy với `BASE_URL` 3010 và Node 20, kỳ vọng PASS. Không ghi đè `e2e/.auth/user.json`. Commit trong repo e2e.

### Task 12: Tài liệu + bàn giao

- [x] **Step 1:** Cập nhật `HRM/.plans/STATUS.md` (dòng feature) và `doi-chieu.md`.
- [x] **Step 2:** Viết memory ngắn, cập nhật `MEMORY.md`.
- [x] **Step 3:** Hỏi user trước khi gộp/push: HRM vào `develop`, ERP vào `develop_02`.
  - Ghi chú deploy: `permission:catalog-sync`, sau đó cấp quyền ở `/admin/roles`.
  - Báo user số ERP đổi sau vá (bảng trước/sau).
