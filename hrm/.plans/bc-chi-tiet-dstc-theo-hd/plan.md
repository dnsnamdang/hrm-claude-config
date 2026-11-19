# Báo cáo chi tiết DSTC theo 1 HĐ (port ERP → HRM) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn HRM `/sale/revenue-standard-contract`: gõ 1 mã HĐ (HĐ hãng, HĐ DV bảo hành, HĐ mới `hrm_contracts`) và xem từng dòng đóng góp DSTC, số khớp ERP, có In và Xuất Excel.

**Architecture:** hrm-api module Finance, thư mục mới `Modules/Finance/Services/RevenueStandardContract/`. Gồm: 1 lớp phạm vi; 1 nguồn "ERP" port 1:1 `RevenueStandardContractService` ERP (đọc thẳng bảng ERP vì chung DB); 1 nguồn "HRM" cho `hrm_contracts`; 1 lớp điều phối chọn nguồn theo mã; 1 lớp dựng bảng in. Controller trả JSON `{contract, addition_annexs, annexs, returns}` đúng dạng ERP. hrm-client có 1 trang V2Base giống màn Tổng hợp thu nhập bán hàng.

**Tech Stack:** Laravel (hrm-api, PHPUnit + DatabaseTransactions trên DB local `erp_hrm_check`), Nuxt 2 (hrm-client, V2Base, ExcelJS).

**Spec:** `HRM/.plans/bc-chi-tiet-dstc-theo-hd/design.md` (đọc kèm). Nguồn ERP: `ERP/TanPhatDev/app/Services/Reports/RevenueStandardContractService.php`, `app/Http/Controllers/ReportController.php:6197-6300`, `resources/views/reports/revenue_standard_contract.blade.php`.

## Global Constraints

- Nhánh `develop` ở cả `hrm-api` và `hrm-client`. Không sửa ERP.
- Mã quyền: `sale.bao_cao_chi_tiet_doanh_so_tieu_chuan_theo_1_hop_dong.view` (`app/Support/Permissions/Catalog/sale.php:789`). Đổi `platforms` thành `['erp','hrm']`. Không seeder, không migration quyền.
- Mẫu in `report_templates.id = 358`, in ngang, biến `CHI_TIET`, `HOP_DONG`, `HEADER`.
- Dạng 1 dòng (giữ nguyên khoá ERP): `object_id, object_code, object_name, unit_name, product_type, price, net_price, price_type_coefficient, product_type_coefficient, standard_price, qty, revenue_contract, revenue_net, revenue_standard, object_type`. `object_type` ∈ `product|service|spa`.
- Tên 2 dòng spa đúng chữ: `Giảm vượt định mức` (= `min(discount_rate_before_vat, 0)`), `Chi phí dự phòng` (= `redundancy_cost`).
- Thông báo lỗi đúng chữ: `Không tìm thấy hợp đồng` (404), `Bạn không có quyền xem hợp đồng này` (403).
- `firm_support_accounting` luôn lọc `contractable_type`: HĐ hãng = `App\Model\Sale\Firm\Contract\FirmContract`, HĐ mới = `Modules\Assign\Entities\Contract\Contract`. HĐ DV đọc `wr_support_accounting` như ERP.
- Ghi chú/comment code bằng tiếng Việt, theo phong cách các file `SalesIncome/*`.
- Commit chỉ khi user cho phép. Message kết thúc bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Các bước "Commit" dưới đây = commit LOCAL trên nhánh `feat/revenue-standard-contract` (đã được phép); KHÔNG push, KHÔNG merge.

## Review Focus

- Mã HĐ có khoảng trắng đầu/cuối hoặc sai hoa/thường: trim trước khi tra. Tra đúng như ERP (`where code =`, collation DB tự lo hoa/thường). Test `test_trims_contract_code` ở Task 5.
- HĐ hãng không có bản HTHT (`firm_support_accounting` trống): 2 dòng spa vẫn hiện, giá trị 0, không lỗi null. Test `test_firm_contract_without_support_accounting_shows_zero_spa_rows` ở Task 2.
- HĐ mới có dòng ĐNXK trả lại trỏ vào dòng con BOM: SL dồn về dòng cha mang giá, không ra dòng âm giá 0. Test `test_return_on_bom_child_maps_to_priced_parent` ở Task 4.
- SL trả lại vượt SL HĐ (dữ liệu lệch): dòng trả lại lấy `min(qty, returned)`, không âm quá doanh số HĐ. Test `test_return_qty_capped_by_contract_qty` ở Task 3 (ERP) và Task 4 (HRM).
- Người chỉ có quyền phạm vi Bộ phận và không quản lý bộ phận nào: vẫn xem được HĐ thuộc bộ phận của chính mình và HĐ mình lập. Test `test_part_scope_includes_own_part` ở Task 1.

---

## File Structure

hrm-api (`HRM/hrm-api`):

| File | Trách nhiệm |
|---|---|
| `app/Support/Permissions/Catalog/sale.php:789` (sửa) | platforms `['erp','hrm']` |
| `Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractScope.php` | đọc cấp quyền, quyết định 1 HĐ có xem được không |
| `Modules/Finance/Services/RevenueStandardContract/ContractHeader.php` | DTO nhỏ: `source` ('firm'\|'wr'\|'hrm'), `id`, `code`, `company_id`, `department_id`, `part_id`, `created_by` |
| `Modules/Finance/Services/RevenueStandardContract/ErpContractSource.php` | port 1:1 ERP cho HĐ hãng + HĐ DV: HĐ gốc, PL bổ sung, PL giảm, trả lại, spa |
| `Modules/Finance/Services/RevenueStandardContract/HrmContractSource.php` | HĐ mới: dòng hàng, dòng dịch vụ, spa, trả lại |
| `Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractService.php` | điều phối: tìm header theo mã (ERP trước, HRM sau, log khi trùng), kiểm phạm vi, trả payload 4 khối |
| `Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractRows.php` | helper tĩnh: `spaRows()`, `totals()`, nhãn tính chất hàng |
| `Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractPrintTable.php` | port `getTable` ERP ra HTML `CHI_TIET` |
| `Modules/Finance/Http/Controllers/V1/RevenueStandardContractController.php` | index / print / export |
| `Modules/Finance/Routes/api.php` (sửa, cạnh khối `sales-income-summary` ~dòng 1998) | 3 route |
| `Modules/Finance/Tests/Feature/Concerns/GrantsPermissionScope.php` | trait tổng quát: cấp 1 mã quyền ở 1 phạm vi |
| `Modules/Finance/Tests/Feature/RevenueStandardContract*Test.php` | test theo task |

hrm-client (`HRM/hrm-client`):

| File | Trách nhiệm |
|---|---|
| `pages/sale/revenue-standard-contract/index.vue` | trang lọc + bảng 14 cột 4 khối + In + Xuất Excel |
| `pages/sale/revenue-standard-contract/components/export-excel.js` | ExcelJS, bám file ERP `RevenueStandardServiceReportExcel` |
| `components/subsystem-menu/sale-hub.js:265` (sửa) | mục `{ n: 'Chi tiết doanh số tiêu chuẩn theo 1 hợp đồng', link: '/sale/revenue-standard-contract' }` |
| `components/subsystem-menu/finance.js:400` (sửa) | thêm `{ label: 'Báo cáo chi tiết doanh số tiêu chuẩn theo 1 hợp đồng', link: '/sale/revenue-standard-contract' }` ngay dưới dòng thu nhập bán hàng |

---

### Task 1: Quyền + lớp phạm vi

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Catalog/sale.php:789`
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/ContractHeader.php`
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractScope.php`
- Create: `hrm-api/Modules/Finance/Tests/Feature/Concerns/GrantsPermissionScope.php`
- Modify: `hrm-api/Modules/Finance/Tests/Feature/Concerns/GrantsSalesIncomeScope.php` (chuyển thành lớp mỏng gọi trait mới, giữ nguyên tên 2 hàm để test cũ không đổi)
- Test: `hrm-api/Modules/Finance/Tests/Feature/RevenueStandardContractScopeTest.php`

**Interfaces:**
- Produces:
  - `final class ContractHeader { public string $source; public int $id; public string $code; public ?int $company_id; public ?int $department_id; public ?int $part_id; public ?int $created_by; public static function fromRow(string $source, object $row): self }`
  - `RevenueStandardContractScope::CODE = 'sale.bao_cao_chi_tiet_doanh_so_tieu_chuan_theo_1_hop_dong.view'`
  - `RevenueStandardContractScope::hasAccess(): bool` (scope ≠ null)
  - `RevenueStandardContractScope::canView(ContractHeader $h): bool`
  - Trait `GrantsPermissionScope`: `ensurePermissionCode(string $code): int`, `grantPermissionScope(int $employeeId, string $code, int $scope, ?int $companyId = null): void` (nội dung = 2 hàm hiện có của `GrantsSalesIncomeScope`, tham số hoá mã)

- [x] **Step 1: Viết test hỏng** `RevenueStandardContractScopeTest` (DatabaseTransactions, `use GrantsPermissionScope`). Fixture: chọn 1 NV local có `info.company_id`, `department_id`, `part_id`, rồi `actingAs($emp, 'api')`. Tạo `ContractHeader` bằng tay (không cần bảng):
  - `test_no_permission_has_no_access`: không cấp quyền → `hasAccess() === false`.
  - `test_group_scope_views_any_company`: scope 4, HĐ company_id = 999999 → `canView === true`.
  - `test_company_scope_same_company_only`: scope 3. HĐ company = `current_company_role` → true; company khác → false.
  - `test_department_scope_uses_managed_departments`: scope 2. HĐ department_id ∈ `listManageDepartmentIds()` → true; department_id = 999999 → false.
  - `test_part_scope_includes_own_part`: scope 1, NV không quản lý bộ phận nào. HĐ part_id = `info.part_id` → true; part khác → false.
  - `test_own_contract_always_visible`: scope 3, HĐ công ty khác nhưng `created_by = me` → true.
- [x] **Step 2: Chạy** `cd HRM/hrm-api && vendor/bin/phpunit Modules/Finance/Tests/Feature/RevenueStandardContractScopeTest.php`. Kết quả mong đợi: FAIL, class không tồn tại.
- [x] **Step 3: Cài đặt.**
  - Đổi platforms ở catalog.
  - Viết `ContractHeader`.
  - Viết `RevenueStandardContractScope`: ánh xạ cấp giống `SalesIncomeScope::level()` (`>= PermissionScope::GROUP/COMPANY/DEPARTMENT/PART`), so với cột tổ chức của HĐ. Cấp bộ phận = `listManagePartIds()` + `auth()->user()->info->part_id`. `created_by === auth()->id()` luôn true.
  - Viết trait mới. Sửa `GrantsSalesIncomeScope` gọi trait mới với `SalesIncomeScope::CODE`.
- [x] **Step 4: Chạy** test mới và `vendor/bin/phpunit Modules/Finance/Tests/Feature/SalesIncomeScopeTest.php Modules/Finance/Tests/Feature/SalesIncomeSummaryApiTest.php`. Kết quả mong đợi: PASS. Nếu ca SalesIncome nào trước đó đã fail vì môi trường RBAC thì vẫn fail như cũ, không thêm ca fail mới.
- [x] **Step 5: Commit** `feat(finance): quyền + phạm vi BC chi tiết DSTC theo 1 HĐ`

---

### Task 2: Nguồn ERP: HĐ gốc, PL bổ sung, PL giảm (HĐ hãng + HĐ DV)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractRows.php`
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/ErpContractSource.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/RevenueStandardContractErpSourceTest.php`

**Interfaces:**
- Consumes: `ContractHeader` (Task 1).
- Produces:
  - `RevenueStandardContractRows::spaRows(float $discountRateBeforeVat, float $redundancyCost): array` (2 dòng, dạng Global Constraints)
  - `RevenueStandardContractRows::totals(array $rows): array{revenue_contract: float, revenue_net: float, revenue_standard: float}`
  - `RevenueStandardContractRows::productTypeLabels(): array` (= `BaseProduct::PRODUCT_TYPES` ERP chép sang + `'service' => 'Dịch vụ'`; nếu hrm-api đã có hằng tương đương thì dùng lại)
  - `ErpContractSource::findHeader(string $code): ?ContractHeader` (HĐ hãng trước, rồi HĐ DV; header lấy từ bảng tìm thấy. ERP ghi đè bằng HĐ DV nếu trùng mã: **giữ thứ tự ERP**, tức HĐ DV thắng ở `id/code`)
  - `ErpContractSource::contract(string $code): array{id:int, code:string, data:array}`
  - `ErpContractSource::additionAnnexes(string $code): array<array{id,code,data}>`
  - `ErpContractSource::reductionAnnexes(string $code): array<array{id,code,data}>`

- [x] **Step 1: Viết test hỏng.** Fixture tự chèn trong transaction: 1 `firm_contracts` mã `ZZRSC-F1` với company_id, 2 dòng `firm_contract_tab_products` (1 dòng `root_quantity > 0`, 1 dòng `root_quantity = 0`), 1 dòng `firm_contract_costs` có `revenue_calculation = 1` và 1 dòng `= 0`, 1 bản `firm_support_accounting` (contractable_type FirmContract). Cột bắt buộc lấy theo schema local, xem `SHOW CREATE TABLE`. Với mỗi bảng dòng ERP, giá trị kỳ vọng tính tay theo đúng SQL của `RevenueStandardContractService::getData` ERP (dòng 297-497):
  - `test_firm_contract_rows_match_erp_formula`: số dòng = 1 hàng + 1 chi phí + 2 spa. `price = LEAST(price, allocated_price)`. `revenue_standard` khớp số tính tay.
  - `test_spa_rows_use_firm_support_accounting_typed`: chèn thêm 1 `firm_support_accounting` cùng `contractable_id`, `contractable_type = Modules\Assign\Entities\Contract\Contract`, `redundancy_cost = 777`. Dòng "Chi phí dự phòng" **không** = 777.
  - `test_firm_contract_without_support_accounting_shows_zero_spa_rows`: không có HTHT. 2 dòng spa có `revenue_* = 0`.
  - `test_wr_contract_rows_and_wr_support_accounting`: 1 `wr_service_contracts` `ZZRSC-W1` với 1 dòng ở 1 trong 6 bảng dòng WR, HTHT ở `wr_support_accounting`. Số dòng + spa đúng.
  - `test_addition_and_reduction_annex_blocks`: 1 PL bổ sung + 1 PL giảm gắn cha `ZZRSC-F1` (cột cha/type theo `getDataAdditionAnnex`/`getDataAnnex` ERP). Mỗi hàm trả 1 khối. 2 dòng spa của PL giảm theo tỉ lệ HĐ cha đúng công thức ERP dòng 102-176.
- [x] **Step 2: Chạy** `vendor/bin/phpunit Modules/Finance/Tests/Feature/RevenueStandardContractErpSourceTest.php`. Kết quả mong đợi: FAIL.
- [x] **Step 3: Cài đặt.** Port từng hàm ERP sang Query Builder (`DB::table`), giữ nguyên biểu thức SQL, union, `revenue_calculation = 1`, `root_quantity > 0`. Khác ERP ở đúng 1 chỗ: join `firm_support_accounting` thêm `contractable_type`. Đầu mỗi hàm ghi comment `// ERP RevenueStandardContractService::<tên>:<dòng>`.
- [x] **Step 4: Chạy** lại. Kết quả mong đợi: PASS.
- [x] **Step 5: Commit** `feat(finance): port nguồn ERP BC chi tiết DSTC (HĐ gốc + phụ lục)`

---

### Task 3: Nguồn ERP: nhập trả lại

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/RevenueStandardContract/ErpContractSource.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/RevenueStandardContractErpSourceTest.php` (thêm ca)

**Interfaces:**
- Produces: `ErpContractSource::returns(string $code): ?array{id, code, data}` (port `getDataContractReturn` 178-235 + `getDataReturn` 498-603. Trả `null` hoặc `data` rỗng giống ERP khi không có trả lại; dạng phải giống ERP để client hiển thị cùng một kiểu)

- [x] **Step 1: Viết test hỏng** trên fixture Task 2:
  - `test_firm_return_rows_negative_by_returned_qty`: đặt `returned_qty = 1` trên dòng hàng. Khối trả lại có dòng `qty = 1`. Doanh số theo đúng dấu ERP: nếu ERP lưu dương và UI trừ thì giữ dương; ghi rõ trong assert.
  - `test_return_qty_capped_by_contract_qty`: `returned_qty` > SL HĐ. `qty = min`.
  - Spa trả lại theo tỉ lệ công thức ERP, kể cả cách chia `market_cost` (không sửa).
- [x] **Step 2: Chạy.** Kết quả mong đợi: FAIL.
- [x] **Step 3: Cài đặt** đúng 1:1 ERP. Chỗ HTHT dùng lại phần lọc `contractable_type` của Task 2.
- [x] **Step 4: Chạy** cả file. Kết quả mong đợi: PASS.
- [x] **Step 5: Commit** `feat(finance): port khối nhập trả lại BC chi tiết DSTC`

---

### Task 4: Nguồn HRM (`hrm_contracts`)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/HrmContractSource.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/RevenueStandardContractHrmSourceTest.php`

**Interfaces:**
- Consumes: `ContractHeader`, `RevenueStandardContractRows::spaRows/totals`, `ProductNatureDstcCoefficient::forProducts(?int $companyId, array $erpProductIds): array` (`Modules/MasterData/Support/ProductNatureDstcCoefficient.php:43`).
- Produces:
  - `HrmContractSource::findHeader(string $code): ?ContractHeader` (`hrm_contracts.code`, bỏ bản ghi đã xoá mềm nếu model có `deleted_at`)
  - `HrmContractSource::contract(ContractHeader $h): array{id, code, data}`
  - `HrmContractSource::returns(ContractHeader $h): ?array{id, code, data}` (cùng dạng `ErpContractSource::returns`)

Ánh xạ dòng (ghi thành docblock đầu class):

| Khoá | Dòng hàng `hrm_contract_product_prices` (chỉ `parent_id IS NULL`, vì dòng con BOM không mang giá) | Dòng dịch vụ `hrm_contract_service_items` |
|---|---|---|
| object_code / object_name | `code` / `name` | `code` / `name` |
| unit_name | tên ĐVT từ `unit_id` | như bên trái |
| product_type | tên nút `product_natures` của `erp_product_id` | `Dịch vụ` |
| price | `round(unit_price_after_discount + extra_price)` (cùng biểu thức ở `ContractService.php:1443-1460`) | `unit_price_after_discount` |
| net_price | `net_price` | = giá theo HTHT (`ContractSupportAccountingService.php:105-117`) |
| price_type_coefficient | G = `company_price_types.coefficient` (company = HĐ, price_type = `quotation.price_type_id ?: 1`) | `null` |
| product_type_coefficient | H = `ProductNatureDstcCoefficient::forProducts(...)[erp_product_id]` | `null` |
| standard_price | `standard_price` đã lưu | giá báo (`quoted_price`), như HTHT `:395` |
| qty | `qty_needed` | `qty` |
| revenue_contract / net / standard | qty × price / net_price / standard_price | qty × các giá tương ứng |

- Tập dòng dịch vụ = đúng tập mà `ContractSupportAccountingService` đang cộng. Gọi lại hàm đó nếu tách được; nếu không thì sao y điều kiện lọc và ghi comment dẫn dòng.
- Spa: `firm_support_accounting` với `contractable_type = Modules\Assign\Entities\Contract\Contract`, `contractable_id = h.id`.
- Trả lại: `SUM(product_export_request_tab_products.returned_qty)` với `emplement_contract_type = 'Modules\Assign\Entities\Contract\Contract'`, `emplement_contract_id = h.id`, nhóm theo `contract_product_id`. Nếu `contract_product_id` trỏ dòng con thì dồn về `parent_id`. Dòng thiếu `contract_product_id` thì ghép `product_id ↔ erp_product_id` + `unit_id` (dự phòng). `qty = min(qty_needed, returned)`. Spa trả lại theo dạng ERP 178-235, với bảng ánh xạ trường HTHT HRM (vd `total_market_costs ↔ sales_bonus`, `ContractSupportAccountingService.php:154-158`) ghi trong docblock.

- [x] **Step 1: Viết test hỏng.** Fixture: 1 `hrm_contracts` `ZZRSC-H1` (company/department/part/created_by, có quotation `price_type_id`). 1 dòng hàng gốc có `standard_price/net_price/unit_price_after_discount/extra_price`, kèm 1 dòng con BOM giá 0. 1 dòng dịch vụ. 1 `firm_support_accounting` kiểu HRM Contract. 1 dòng `product_export_request_tab_products` kiểu HRM Contract, `contract_product_id` = dòng hàng gốc, `returned_qty = 1`.
  - `test_product_rows_use_stored_standard_and_net`: 1 dòng hàng (dòng con không ra). `revenue_standard = qty_needed × standard_price`. `price_type_coefficient` = G từ `company_price_types`.
  - `test_service_rows_match_support_accounting`: tổng `revenue_standard` dòng dịch vụ = số `ContractSupportAccountingService` tính cho HĐ đó.
  - `test_spa_rows_from_typed_support_accounting`: chèn thêm 1 `firm_support_accounting` kiểu FirmContract cùng id với `redundancy_cost = 777`. Dòng dự phòng ≠ 777.
  - `test_returns_from_export_request_tab_rows`: khối trả lại có 1 dòng `qty = 1`, giá = giá dòng HĐ.
  - `test_return_on_bom_child_maps_to_priced_parent`: `contract_product_id` = dòng con. Kết quả vẫn 1 dòng của dòng cha.
  - `test_return_qty_capped_by_contract_qty`: `returned_qty` lớn hơn `qty_needed`. `qty = qty_needed`.
  - `test_firm_typed_tab_rows_ignored`: dòng tab có cùng `emplement_contract_id` nhưng type HĐ hãng. Không tính.
- [x] **Step 2: Chạy** `vendor/bin/phpunit Modules/Finance/Tests/Feature/RevenueStandardContractHrmSourceTest.php`. Kết quả mong đợi: FAIL.
- [x] **Step 3: Cài đặt** theo bảng ánh xạ.
- [x] **Step 4: Chạy.** Kết quả mong đợi: PASS.
- [x] **Step 5: Commit** `feat(finance): nguồn HĐ mới HRM cho BC chi tiết DSTC`

---

### Task 5: Điều phối + controller + route + in

**Files:**
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractService.php`
- Create: `hrm-api/Modules/Finance/Services/RevenueStandardContract/RevenueStandardContractPrintTable.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/RevenueStandardContractController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (sau khối `sales-income-summary`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/RevenueStandardContractApiTest.php`

**Interfaces:**
- Consumes: Task 1-4.
- Produces:
  - `RevenueStandardContractService::report(string $code): array{contract, addition_annexs, annexs, returns}`. Throw `ModelNotFoundException`, controller trả 404 `Không tìm thấy hợp đồng`. Throw `AuthorizationException`, controller trả 403 `Bạn không có quyền xem hợp đồng này`.
  - Thứ tự tra: `ErpContractSource::findHeader`. Nếu có header ERP mà `HrmContractSource::findHeader` cũng trùng mã thì `Log::warning('RSC trùng mã HĐ ERP và HRM', ['code'=>..])`, dùng ERP. Không có ERP thì dùng HRM. HĐ HRM: `addition_annexs = []`, `annexs = []`.
  - `RevenueStandardContractPrintTable::html(array $report): string` (port `getTable` ERP: cùng cột, dòng tiêu đề khối, `-` khi 0, `formatCurrency`)
  - Route (prefix `/sale/revenue-standard-contract`, URL đầy đủ `/api/v1/finance/sale/revenue-standard-contract`. Nếu nhóm route Finance đặt khác thì bám đúng tiền tố của `sales-income-summary`):
    - `GET /` → `index`
    - `GET /print` → `print`
    - `GET /export` → `export` (trả cùng JSON + `title`. Excel dựng ở client như màn thu nhập bán hàng)
  - Không có quyền (`hasAccess() === false`) → 403 trước khi tra mã.

- [x] **Step 1: Viết test hỏng** (dùng fixture helper chung với Task 2/4; tách ra `Concerns/RevenueStandardContractFixtures.php` nếu cần):
  - `test_requires_contract_code`: không truyền → 422.
  - `test_unknown_code_returns_404_message`: kiểm `message` đúng chữ.
  - `test_no_permission_returns_403`.
  - `test_out_of_scope_contract_returns_403_message`: scope 3, HĐ công ty khác. 403 đúng chữ, body không có `contract`.
  - `test_firm_contract_payload_shape`: 4 khoá. `contract.data` có 2 dòng `object_type = spa` ở cuối.
  - `test_hrm_contract_payload_has_empty_annexes`.
  - `test_code_collision_prefers_erp_and_logs`: `Log::spy()`, HĐ hãng và HĐ HRM cùng mã. `contract.id` = id HĐ hãng, warning được gọi.
  - `test_trims_contract_code`: `' ZZRSC-F1 '` vẫn tìm thấy.
  - `test_print_returns_html_with_contract_code`: dùng `printListPayload` như `SalesIncomeSummaryController`, có `landscape = true`, HTML chứa `ZZRSC-F1`.
- [x] **Step 2: Chạy** `vendor/bin/phpunit Modules/Finance/Tests/Feature/RevenueStandardContractApiTest.php`. Kết quả mong đợi: FAIL.
- [x] **Step 3: Cài đặt** controller theo khuôn `SalesIncomeSummaryController` (`ApiController`, `LimitsPrintListRows`, template `DB::table('report_templates')->where('id', 358)->value('template')`, `clearNull(fillReport(...))` với `CHI_TIET`, `HOP_DONG` = mã HĐ, `HEADER` theo ERP controller 6236-6268).
- [x] **Step 4: Chạy** toàn bộ `vendor/bin/phpunit --filter RevenueStandardContract`. Kết quả mong đợi: PASS.
- [x] **Step 5: Commit** `feat(finance): API BC chi tiết DSTC theo 1 HĐ (xem/in/xuất)`

---

### Task 6: hrm-client: trang + Excel + menu

**Files:**
- Create: `hrm-client/pages/sale/revenue-standard-contract/index.vue`
- Create: `hrm-client/pages/sale/revenue-standard-contract/components/export-excel.js`
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js:265`
- Modify: `hrm-client/components/subsystem-menu/finance.js:400`

**Interfaces:**
- Consumes: API Task 5 (`/finance/sale/revenue-standard-contract`, `/print`, `/export`).
- Khuôn: `pages/sale/sales-income-summary/index.vue` (V2Base, `reportPrintPreviewMixin.openPrintList(API, params, title)`, `ReportPrintPreviewModal`), Excel theo `pages/sale/sales-income-summary/components/export-excel.js`.

Yêu cầu màn:
- Bộ lọc: 1 ô `Mã hợp đồng` (Enter = Lọc), nút `Lọc` / `Làm mới` / `In` / `Xuất Excel`. Chưa nhập mã thì nút Lọc hiện cảnh báo, không gọi API.
- Bảng 14 cột đúng thứ tự spec §2. 4 khối: dòng tiêu đề khối (mã HĐ / mã PL / "Nhập trả lại"), các dòng, dòng `Tổng cộng`. Cuối bảng có dòng tổng chung (= gốc + PL bổ sung − PL giảm − trả lại, như `getSumRevenueStandard` ở blade ERP dòng 414-426) và dòng tóm tắt trả lại (`summary()` blade dòng 429+).
- Số 0 hiện `-` như ERP. Hệ số `null` để trống.
- Lỗi 403/404 hiện `message` từ API.
- Excel: tiêu đề `BÁO CÁO CHI TIẾT DOANH SỐ TIÊU CHUẨN THEO 1 HỢP ĐỒNG`, colspan 14, cùng khối/dòng tổng như bảng.

- [x] **Step 1: Cài đặt** trang, file Excel, mục menu `{ n: 'Chi tiết doanh số tiêu chuẩn theo 1 hợp đồng', link: '/sale/revenue-standard-contract' }` thay cho chuỗi placeholder ở sale-hub, và 1 dòng ở finance.js:400.
- [x] **Step 2: Chạy** `cd HRM/hrm-client && npx eslint pages/sale/revenue-standard-contract components/subsystem-menu/sale-hub.js components/subsystem-menu/finance.js`. Kết quả mong đợi: 0 lỗi.
- [x] **Step 3: Kiểm trên trình duyệt** (skill run-hrm + Playwright MCP). Đăng nhập NV có quyền, gõ 1 mã HĐ hãng thật trên local, rồi 1 mã HĐ HRM, rồi 1 mã sai. Kết quả mong đợi: 4 khối hiện đúng, mã sai báo `Không tìm thấy hợp đồng`, In mở preview ngang, Excel tải file mở được.
- [x] **Step 4: Commit** `feat(sale): màn BC chi tiết DSTC theo 1 HĐ`

---

### Task 7: Đối chiếu số với ERP

- [x] **Step 1:** Trên DB local chọn 1 HĐ hãng có PL bổ sung hoặc trả lại, và 1 HĐ DV. Gọi ERP `report/revenue_standard_contract/searchData?contract_code=` (ERP local hoặc tinker gọi `RevenueStandardContractService` ERP) và API HRM. Diff JSON bằng script trong scratchpad, so từng dòng `revenue_contract/net/standard`. Kết quả mong đợi: không lệch. Chỗ lệch duy nhất được phép: HTHT khi id trùng HĐ mới (ghi ra nếu gặp).
- [x] **Step 2:** 1 HĐ HRM thật: tổng DSTC dòng hàng + dịch vụ khớp màn Hỗ trợ hạch toán của HĐ đó. Ghi kết quả + mã HĐ đã soát vào `HRM/.plans/bc-chi-tiet-dstc-theo-hd/verify.md`. Trong đó ghi rõ "số trả lại HĐ mới cần anh soát khi nghiệm thu" (spec §3).
