# Báo cáo tổng hợp bán hàng Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Màn HRM "Báo cáo tổng hợp bán hàng" (menu Kế toán) = màn "Bán hàng theo từng mặt hàng" + 3 cột Đơn giá vốn / Thành tiền vốn / Lãi lỗ, gác mã `accounting.bao_cao_tong_hop_ban_hang.view` (Công ty / Tổng công ty), số khớp ERP `report.summary_sale?type=all`.

**Architecture:** Một lõi số liệu `SaleByProductReportService` có 2 chế độ (`product` mặc định, `summary`) chọn bằng factory phía server — chế độ quyết mã quyền, hành vi khi không quyền và việc trả cột vốn. Controller con `SaleSummaryReportController` (route riêng `finance/sale-summary-report/*`) kế thừa controller mặt hàng, chỉ đổi service/printer/tên file. FE tách thân trang mặt hàng thành 1 component màn hình dùng chung có prop `mode`; 2 trang chỉ bọc component đó.

**Tech Stack:** Laravel (hrm-api, nwidart module Finance), PHPUnit chạy trên DB gộp local `erp_hrm_check` với `DatabaseTransactions`; Nuxt 2 / Vue 2 (hrm-client); ERP Laravel 6 (chỉ khi phải vá).

**Spec:** `HRM/.plans/bao-cao-tong-hop-ban-hang/design.md` (đã duyệt 16/11/2026).

## Global Constraints

- Mã quyền: `accounting.bao_cao_tong_hop_ban_hang.view`, tên quyền `Xem báo cáo tổng hợp bán hàng`, scopes `[3, 4]`; thêm `'hrm'` vào `platforms` trong `hrm-api/app/Support/Permissions/Catalog/accounting.php:165`.
- Không quyền tổng hợp → mọi endpoint `finance/sale-summary-report/*` trả **403**; menu ẩn.
- Màn mặt hàng (`finance/sale-by-product-report/*`) KHÔNG được có khoá `export_price`, `export_price_amount`, `profit_loss` trong bất kỳ response nào (kể cả summary, popup, in, Excel).
- Tiêu đề in: `BÁO CÁO TỔNG HỢP BÁN HÀNG` / `CHI TIẾT PHÁT SINH TỔNG HỢP BÁN HÀNG`; file Excel `bao_cao_tong_hop_ban_hang.xlsx` / `chi_tiet_tong_hop_ban_hang.xlsx`.
- Nhãn + thứ tự cột vốn (y ERP): … `Thành tiền net` · **`Đơn giá vốn`** · **`Thành tiền vốn`** · `Chênh lệch` · **`Lãi lỗ`**.
- Công thức gộp (ERP `SummarySaleReportService.php:455-457`): `export_price = Σexport_price_amount / Σexported_qty` (null nếu Σexported_qty = 0); `export_price_amount = export_price × real_qty` (0 nếu null); `profit_loss = (Σallocated_price_amount − Σexport_price_amount) / Σexported_qty × real_qty` (0 nếu Σexported_qty = 0).
- Popup từng dòng: `export_price_amount` theo nhánh; `export_price = export_price_amount / exported_qty`; `profit_loss = allocated_price_amount − export_price_amount`.
- DB: `erp_hrm_check` chỉ SELECT ngoài fixture trong transaction test; prod `hrm_erp_gop` chỉ SELECT. Không sửa `.env`. Không commit/push khi user chưa duyệt (commit cục bộ trong worktree được, push thì hỏi).
- Làm trong worktree HRM (api + client) và — nếu cần vá — worktree ERP nhánh từ `develop_02`. Không switch/reset repo chính.
- Không thay đổi số SL / tiền bán / net / chênh lệch của màn mặt hàng (trừ khi Task 1 kết luận lỗi ở lõi chung — ghi rõ trong design §6).

## Review Focus

1. Người có quyền mặt hàng nhưng KHÔNG có quyền tổng hợp gọi `finance/sale-summary-report/item-list/export` → phải 403 (không rơi về "phiếu mình tạo"). Test: Task 2 `test_no_summary_permission_403_on_every_endpoint`.
2. Gọi màn mặt hàng kèm `?mode=summary` / `?with_cost=1` → vẫn không có cột vốn. Test: Task 2 `test_product_endpoints_never_expose_cost_even_with_query_flags`.
3. Mặt hàng chỉ có phiếu nhập trả trong kỳ (Σexported_qty = 0) → không chia 0, các ô vốn = null/0, hiển thị `-`. Test: Task 1 `test_summary_aggregate_handles_zero_exported_qty`.
4. Tổng công ty lọc 1 công ty vs mức Công ty gửi `company_id` công ty khác → mức Công ty bị bỏ qua `company_id` (fail-closed). Test: Task 2 `test_company_scope_ignores_foreign_company_id`.
5. Dòng bán mượn có `unit_coefficient ≠ 1`: tiền vốn đúng ĐVT. Test: Task 1 `test_borrow_cost_respects_unit_semantics` (giá trị kỳ vọng theo kết luận Step 1).

---

### Task 1: Chế độ tổng hợp trong lõi số liệu (cột vốn + phạm vi)

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/SaleByProductReportService.php` (hằng `CODE` ~45, `scopeLevel()` ~69, `branchExport/branchBorrow/branchReturn` ~208-410, `report()` ~414, `aggregateRow()` ~490, `itemList()` ~560, `detailSummary()`)
- Create: `hrm-api/Modules/Finance/Tests/Feature/SaleSummaryReportServiceTest.php`
- Modify: `HRM/.plans/bao-cao-tong-hop-ban-hang/design.md` §6

**Interfaces:**
- Produces:
  - `const SUMMARY_CODE = 'accounting.bao_cao_tong_hop_ban_hang.view';`
  - `public static function forSummary(): self` — instance chế độ tổng hợp (constructor mặc định = chế độ mặt hàng; không nhận tham số request).
  - `public function isSummary(): bool`
  - `public function permissionCode(): string` — `SUMMARY_CODE` hoặc `CODE`.
  - `scopeLevel()` ở chế độ tổng hợp trả `'all' | 'company'`, ném `Symfony\Component\HttpKernel\Exception\HttpException(403, 'Bạn không có quyền xem báo cáo tổng hợp bán hàng')` khi scope < COMPANY.
  - `report()` / `itemList()` ở chế độ tổng hợp: mỗi dòng thêm `export_price` (float|null), `export_price_amount` (float), `profit_loss` (float); `summary` thêm `export_price_amount`, `profit_loss`. Chế độ mặt hàng: KHÔNG có các khoá này.

- [x] **Step 1: Chốt ngữ nghĩa giá vốn bán mượn (nghiên cứu, không code)**

Tìm chỗ ERP ghi `borrow_sell_products.export_price` (grep `export_price` trong `ERP/TanPhatDev/app` quanh BorrowSell/`calculateExportPrice`) và lấy mẫu `SELECT id, qty, unit_coefficient, price, allocated_price, export_price FROM borrow_sell_products WHERE unit_coefficient NOT IN (0,1) AND export_price > 0 LIMIT 20` trên `erp_hrm_check`, so với giá vốn ĐVT cơ bản của hàng (`product_export_details.export_price` cùng sản phẩm, cùng thời điểm).
Kết luận 1 trong 2: (a) `bsp.export_price` theo ĐVT bán → `bsp.export_price * bsp.qty` đúng, ERP KHÔNG lỗi (đơn giá popup chia hệ số chỉ là quy về ĐVT cơ bản); (b) theo ĐVT cơ bản → tiền vốn phải `bsp.export_price * bsp.qty * coef`, ERP lỗi. Ghi kết luận + 2-3 dòng bằng chứng vào design §6. Không kết luận được → DỪNG, báo controller.

- [x] **Step 2: Viết test thất bại** `SaleSummaryReportServiceTest` (DatabaseTransactions, fixture + cấp quyền theo khuôn `BonusMonthScopeTest`/`BuildsBonusLedgerFixtures::grantScopeForCode`):
  - `test_product_mode_rows_have_no_cost_keys`: `(new SaleByProductReportService)->report($r)` → mọi dòng + summary không có `export_price`, `export_price_amount`, `profit_loss`.
  - `test_summary_mode_matches_erp_formula`: fixture 1 sản phẩm: 1 phiếu xuất (`ped.export_qty=2, unit_coefficient=1, allocated_price=150, export_price=100`) + 1 nhập trả loại 4 SL 1 (phiếu xuất gốc trong kỳ) → dòng: `exported_qty=2, real_qty=1, export_price=100, export_price_amount=100, profit_loss=50`; summary `export_price_amount=100, profit_loss=50`.
  - `test_summary_aggregate_handles_zero_exported_qty`: sản phẩm chỉ có nhập trả → `export_price === null`, `export_price_amount == 0`, `profit_loss == 0`.
  - `test_borrow_cost_respects_unit_semantics`: 1 dòng bán mượn `qty=2, unit_coefficient=10, allocated_price=1500, export_price=E` → `export_price_amount` = giá trị theo kết luận Step 1 ((a) `2E`, (b) `20E`).
  - `test_summary_item_list_row_profit`: `itemList` chế độ tổng hợp với fixture phiếu xuất trên → dòng `export_price=100, export_price_amount=200, profit_loss=100`.
  - `test_summary_scope_without_permission_throws_403`, `test_summary_scope_company_and_all`: scope 0 → HttpException 403; scope 3 → `'company'`; scope 4 → `'all'`; scope 2 (Phòng ban) → 403.

- [x] **Step 3: Chạy, xác nhận FAIL**
Run: `cd hrm-api && php vendor/bin/phpunit Modules/Finance/Tests/Feature/SaleSummaryReportServiceTest.php`
Expected: FAIL (`forSummary` undefined).

- [x] **Step 4: Cài đặt** trong `SaleByProductReportService`:
  - Thuộc tính `private $summary = false;` + `forSummary()`, `isSummary()`, `permissionCode()`; `scopeLevel()` đọc `permissionCode()`; nhánh tổng hợp chỉ 2 mức như Interfaces.
  - 3 nhánh luôn select thêm `export_price_amount` (gộp: `SUM(ped.export_price * ped.export_qty)`, mượn theo kết luận Step 1, trả lại `0`); `report()` thêm `SUM(result.export_price_amount) as gross_export_amount`.
  - `aggregateRow()`: tính 3 khoá theo Global Constraints, CHỈ gắn khi `isSummary()`; `report()` summary thêm 2 tổng chỉ khi `isSummary()`; `itemList()` + `detailSummary()` tương tự.
  - Nếu (b): sửa nhánh mượn ở cả 2 chế độ chỉ ảnh hưởng cột vốn → màn mặt hàng không đổi số.

- [x] **Step 5: Chạy, xác nhận PASS** — lệnh Step 3, Expected: OK. Chạy thêm mọi test Finance có `SaleByProduct` nếu có (hiện chưa có) + `php -l` file service.

- [x] **Step 6: Commit**
```bash
git add Modules/Finance/Services/SaleByProductReportService.php Modules/Finance/Tests/Feature/SaleSummaryReportServiceTest.php
git commit -m "feat(finance): che do tong hop ban hang trong SaleByProductReportService (gia von, lai lo, pham vi 2 muc)"
```

---

### Task 2: API màn tổng hợp (controller, route, in, Excel, quyền)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/SaleSummaryReportController.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/SaleByProductReportController.php` (tên file Excel thành thuộc tính/phương thức ghi đè được)
- Modify: `hrm-api/Modules/Finance/Services/SaleByProductReportPrintService.php` (cột + tiêu đề theo chế độ)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (sau khối `sale-by-product-report` ~1646)
- Modify: `hrm-api/app/Support/Permissions/Catalog/accounting.php:165` (platforms + `'hrm'`)
- Create: `hrm-api/Modules/Finance/Tests/Feature/SaleSummaryReportApiTest.php`

**Interfaces:**
- Consumes: `SaleByProductReportService::forSummary()`, `isSummary()`, khoá dòng/summary của Task 1.
- Produces:
  - Route GET `finance/sale-summary-report/` · `/filter-options` · `/print-list-data` · `/export` · `/item-list` · `/item-list/print-list-data` · `/item-list/export` — cùng tham số + shape JSON như `sale-by-product-report`, thêm khoá vốn.
  - `SaleByProductReportPrintService::forSummary(): self` — `COLUMNS`/`DETAIL_COLUMNS` chèn `export_price` ['Đơn giá vốn','money',false], `export_price_amount` ['Thành tiền vốn','money',true] sau `net_price_amount`, `profit_loss` ['Lãi lỗ','money',true] sau `diff`; WIDTHS 16/18/18; tiêu đề theo Global Constraints. `pick()` ở chế độ mặt hàng loại khoá vốn kể cả khi `cols` yêu cầu.
  - `filter-options` của màn tổng hợp trả thêm `scope` ∈ `all|company` (FE ẩn ô Công ty khi `company`).

- [x] **Step 1: Viết test thất bại** `SaleSummaryReportApiTest` (actingAs NV thường đã xoá role/permission như `BonusMonthScopeTest::plainEmployee`):
  - `test_no_summary_permission_403_on_every_endpoint`: NV có quyền mặt hàng scope 4, không quyền tổng hợp → 7 route trả 403.
  - `test_summary_index_returns_cost_columns`: cấp scope 4 → `/` 200, `rows[0]` và `summary` có `export_price_amount`, `profit_loss`.
  - `test_product_endpoints_never_expose_cost_even_with_query_flags`: cấp CẢ 2 quyền scope 4, gọi `sale-by-product-report/` và `/item-list` kèm `?mode=summary&with_cost=1&cols=export_price,profit_loss` → JSON không chứa chuỗi `export_price` / `profit_loss`; `/print-list-data` HTML không chứa `Đơn giá vốn`.
  - `test_summary_print_and_excel_have_cost_headers`: `/print-list-data` HTML chứa `BÁO CÁO TỔNG HỢP BÁN HÀNG`, `Đơn giá vốn`, `Lãi lỗ`; `/export` header `Content-Disposition` chứa `bao_cao_tong_hop_ban_hang.xlsx`; `/item-list/export` chứa `chi_tiet_tong_hop_ban_hang.xlsx`.
  - `test_company_scope_ignores_foreign_company_id`: scope 3, gửi `company_id` = công ty khác → `filter-options.scope == 'company'` và kết quả `/` bằng kết quả khi không gửi `company_id`.
  - `test_catalog_summary_code_has_hrm_platform`: entry catalog có `'hrm'` trong `platforms`, `scopes == [3, 4]`.

- [x] **Step 2: Chạy, xác nhận FAIL**
Run: `php vendor/bin/phpunit Modules/Finance/Tests/Feature/SaleSummaryReportApiTest.php` — Expected: FAIL 404 route.

- [x] **Step 3: Cài đặt**: controller con gán `$this->service = SaleByProductReportService::forSummary()`, `$this->printer = (new SaleByProductReportPrintService)->forSummary()`, ghi đè 2 tên file; route group `/sale-summary-report` (comment như khối mặt hàng: port ERP report.summary_sale type=all 16/11/2026, quyền gác trong service → 403); print service đổi theo chế độ; catalog thêm `'hrm'`.

- [x] **Step 4: Chạy, xác nhận PASS** — lệnh Step 2 + `SaleSummaryReportServiceTest`. Expected: OK.

- [x] **Step 5: Commit**
```bash
git add Modules/Finance app/Support/Permissions/Catalog/accounting.php
git commit -m "feat(finance): API Bao cao tong hop ban hang finance/sale-summary-report (403 khong quyen, in/Excel cot von)"
```

---

### Task 3: FE màn tổng hợp + menu

**Files:**
- Create: `hrm-client/components/sale-by-product-report/SaleByProductReportScreen.vue` (chuyển nguyên thân `pages/sale/sale-by-product-report/index.vue`)
- Move: `hrm-client/pages/sale/sale-by-product-report/components/*` → `hrm-client/components/sale-by-product-report/` (cập nhật import)
- Modify: `hrm-client/pages/sale/sale-by-product-report/index.vue` (chỉ `<SaleByProductReportScreen mode="product" />` + head/title cũ)
- Create: `hrm-client/pages/finance/sale-summary-report/index.vue` (`<SaleByProductReportScreen mode="summary" />`, title `Báo cáo tổng hợp bán hàng`)
- Modify: `hrm-client/components/subsystem-menu/finance.js:400`

**Interfaces:**
- Consumes: API Task 2.
- Produces: prop `mode: 'product' | 'summary'` (mặc định `'product'`). Theo `mode`: `API` = `finance/sale-by-product-report` | `finance/sale-summary-report`; tiêu đề; `pathsToKeep` (`/sale/sale-by-product-report` | `/finance/sale-summary-report`); danh sách cột (thêm 3 cột vốn đúng thứ tự Global Constraints khi `summary`); khoá lưu cấu hình cột localStorage riêng mỗi mode; ô Công ty ẩn khi `filter-options.scope === 'company'` (mode summary). `SaleByProductTable`, `SaleByProductSummary`, `SaleByProductDetailModal` nhận prop `showCost: Boolean` — chỉ render cột/tổng vốn khi true; ô = 0 hoặc null hiển thị `-`.
- Menu: `{ label: 'Báo cáo tổng hợp bán hàng', link: '/finance/sale-summary-report', isShow: ['Xem báo cáo tổng hợp bán hàng'], codes: ['accounting.bao_cao_tong_hop_ban_hang.view'] }`.

- [x] **Step 1: Tách component + 2 trang + prop `showCost`** theo Interfaces (không đổi hành vi màn mặt hàng).
- [x] **Step 2: Kiểm tra build**: `cd hrm-client && npx eslint components/sale-by-product-report pages/sale/sale-by-product-report pages/finance/sale-summary-report components/subsystem-menu/finance.js` — Expected: 0 error.
- [x] **Step 3: Kiểm tra trình duyệt (skill `run-hrm`, Playwright MCP)** với user Super admin local:
  - `/sale/sale-by-product-report` kỳ 05/2026: không có cột vốn; số tổng giống trước khi tách (chụp tổng trước Step 1 để so).
  - `/finance/sale-summary-report` kỳ 05/2026: 3 cột vốn đúng thứ tự, dòng tổng có Thành tiền vốn + Lãi lỗ, popup chi tiết có 3 cột, In + Excel có cột; menu Kế toán › Báo cáo bán hàng › Báo cáo tổng hợp bán hàng mở đúng trang.
  - Console không lỗi.
- [x] **Step 4: Commit**
```bash
git add components/sale-by-product-report pages/sale/sale-by-product-report pages/finance/sale-summary-report components/subsystem-menu/finance.js
git commit -m "feat(finance): man Bao cao tong hop ban hang dung chung man theo mat hang + menu Ke toan"
```

---

### Task 4: Đối chiếu ERP + vá ERP (nếu có lỗi)

**Files:**
- Create: `HRM/.plans/bao-cao-tong-hop-ban-hang/doi-chieu.md`
- Script đối chiếu: để ở scratchpad, không đưa vào repo.
- Modify (chỉ khi Task 1 kết luận (b) hoặc đối chiếu phát hiện lỗi ERP): `ERP/TanPhatDev/app/Services/Reports/SummarySaleReportService.php` trong worktree ERP từ `develop_02`.

**Interfaces:**
- Consumes: `SaleByProductReportService::forSummary()->report($r, false)`; ERP `SummarySaleReportService` gọi qua tinker trong worktree ERP với `auth()->loginUsingId(<super admin>)`.

- [x] **Step 1: Script đối chiếu** (scratchpad): với mỗi kỳ {05/2026, 2025, 2026} × phạm vi {tổng công ty, công ty 1}, lấy dòng ERP type=all và HRM (loại phần HĐ HRM: chạy HRM với bộ lọc tương đương hoặc trừ nhánh `hc.id IS NOT NULL`), so theo `product_id` 6 cột: `exported_qty, real_qty, allocated_price_amount, export_price_amount, diff, profit_loss`, sai số |Δ| ≤ 1 đồng.
- [x] **Step 2: Chạy, ghi `doi-chieu.md`**: bảng kỳ × phạm vi × số dòng × số lệch; mỗi nhóm lệch ghi nguyên nhân (lỗi ERP → design §6 + vá; lỗi HRM → sửa + test hồi quy ở Task 1 file test).
- [x] **Step 3: Vá ERP nếu cần** — sửa đúng dòng nhánh lỗi, chạy lại script tới 0 lệch; commit trong worktree ERP:
```bash
git commit -m "fix(report): tong hop ban hang - <mo ta loi> (doi chieu HRM)"
```
- [x] **Step 4: Cập nhật tài liệu**: design §6 tick, `STATUS.md` → "code xong, chờ gộp/push"; ghi chú deploy `permission:catalog-sync` + cấp quyền ở `/admin/roles`.
