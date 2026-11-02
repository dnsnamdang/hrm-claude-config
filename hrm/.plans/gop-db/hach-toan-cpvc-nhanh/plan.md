# Danh sách cần hạch toán chi phí vận chuyển nhanh — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP `orderReport.fastDelivery` sang HRM (Tài chính › Nhập hàng) + sửa nguồn "giao nhanh" của phiếu kế toán cho giống ERP.

**Architecture:** 1 service truy vấn dùng chung (`FastDeliveryAccountingService`) phục vụ danh sách, Excel và nạp phiếu kế toán. Màn FE theo khuôn danh sách V2, gộp ô hàng hoá bằng `cellSpan`; Excel FE (`exportListFile`) gộp ô bằng `row_groups` / `merge_columns`. Phiếu kế toán: thay phần đọc bảng thô trong `BillAdjustDeptSourceService::fromFastDelivery` bằng service mới; thêm chặn 403/409 lúc tạo; popup hợp đồng có nhánh giao nhanh.

**Tech Stack:** Laravel (hrm-api, Modules/Finance), Nuxt 2 / Vue 2 V2Base (hrm-client), PHPUnit feature test trên DB gộp (DatabaseTransactions).

**Spec:** `hrm-claude-config/hrm/docs/superpowers/specs/gop-db/2026-11-02-hach-toan-cpvc-nhanh-design.md` (đọc kèm — mọi giá trị, điều kiện lọc, cột lấy ở đó).

## Global Constraints

- Giữ nguyên nghiệp vụ / truy vấn ERP `FastDeliveryService::getData` + `render`, trừ các điểm spec mục 8 ghi rõ.
- Quyền: 5 tên y ERP — "Hạch toán chi phí vận chuyển nhanh" + "… - Xem theo tổng công ty / công ty / phòng ban / bộ phận"; kiểm bằng trait `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (khuôn CXK / CXCH / báo cáo bốc xếp). Khai bản guard api ở **cuối** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `type` 8 (Tài chính), `group` 'Hạch toán chi phí vận chuyển nhanh'; `php artisan permission:sync --dry-run` rồi chạy thật.
- Số chuẩn quốc tế `1,234,567.89`; ô rỗng để trống; chữ trạng thái + màu: Đang tạo xám, Đã duyệt xanh, Hủy đỏ, Chưa hạch toán vàng (dùng `utils/statusBadgeVariant.js`).
- Không gọi `sed -i` / script regex ghi đè file; không commit/push trừ khi user bảo; không tắt server dev (api 8002, client 3000); đóng browser Playwright (`playwright-a`) khi xong.
- Hàm dùng chung đụng tới (user đã đồng ý 02/11/2026): `BillAdjustDeptSourceService`, `BillAdjustDeptPickerService::searchContracts`, `BillAdjustDeptForm.vue`, `ContractPickerModal.vue` — chỉ đổi nhánh giao nhanh.
- Nhánh: `feat/hach-toan-cpvc-nhanh` rẽ từ `develop` ở **cả** hrm-api và hrm-client (kiểm `git status` sạch trước khi rẽ; nhánh `feat/chuyen-xe-cho-hang` đang có commit chưa push — đừng làm trên đó).

## Review Focus

1. Dòng giao nhanh mang loại tiền ngoại tệ (USD/EURO/JPY) → phiếu KT phải ra đúng loại tiền + tỷ giá danh mục, không VNĐ (Task 3 test `test_source_uses_contract_currency_and_employee`).
2. Hai người cùng tick 1 dòng rồi lưu → người thứ hai nhận 409, dòng không bị gắn 2 phiếu (Task 3 `test_store_conflicts_when_already_accounted`).
3. Phiếu nhập tạo lúc 15:00 ngày D, lọc Đến ngày = D → phải ra (Task 1 `test_date_to_includes_whole_day`).
4. HĐ mua là phụ lục (`parent_id` ≠ null) — phiếu nhập gắn HĐ cha vẫn khớp (Task 1 `test_matches_import_of_parent_contract`).
5. Người không có quyền nào chỉ thấy dòng mình chịu phí; người có quyền công ty không thấy công ty khác dù gửi `company_id` khác (Task 1 `test_scope_levels`).

---

### Task 1: Service truy vấn dùng chung + quyền

**Files:**
- Create: `hrm-api/Modules/Finance/Services/FastDelivery/FastDeliveryAccountingService.php`
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (cuối file)
- Test: `hrm-api/Modules/Finance/Tests/Feature/FastDeliveryAccountingServiceTest.php`

**Interfaces:**
- Produces:
  - `const PERM_UPDATE = 'Hạch toán chi phí vận chuyển nhanh'` + 4 hằng `PERM_ALL / PERM_COMPANY / PERM_DEPARTMENT / PERM_PART`.
  - `rawQuery(Request $request, bool $allScope = false): \Illuminate\Database\Query\Builder` — dòng SQL mức sản phẩm (cột như ERP `getData` select + `bc2fdcp.id as fdcp_id`), đã áp phạm vi (bỏ qua khi `$allScope`) + bộ lọc, `ORDER BY bc2fdc.id, bc2fdcp.id`.
  - `group(\Illuminate\Support\Collection $rows): \Illuminate\Support\Collection` — port `render`, khoá `bc2_id-employee_id-customer_id`, `products` khử trùng theo `fdcp_id`; mỗi phần tử là mảng khoá như ERP `render` (id, employee_id/code/name, customer_id/code/name, pi_id, pi_code, pi_creator_name, amount, status (bool), note, updated_name, currency, bc2_id, bc2_code, bill_adjust_dept_id/code/status, bill_approver_name, products[{product_id, product_code, product_name}]).
  - `list(Request $request): array` → `['data' => group sau phân trang, 'meta' => ['total','current_page','per_page','last_page']]`, phân trang SAU khi gom (`page`, `per_page` mặc định 10).
  - `byIds(array $ids): Collection` — `group(rawQuery(new Request, true)->whereIn('bc2fdc.id', $ids)->get())`, dùng cho Task 3.
  - `scopeFlags(): array` → `['is_all_company','is_company','is_department','is_part','can_update']` (bool).

- [ ] **Step 1: Viết test (fixture tự chèn trong transaction)** — helper `fixture(array $overrides = [])` chèn tối thiểu: `buy_contract2` (status 1, currency 'USD'), `buy_contract2_fast_deliveries` (employee_id = NV test), `buy_contract2_fast_delivery_customers` (customer_id, amount 1000, status 0), 2 dòng `…_customer_products`, `product_imports` (type 11, status 1, created_at tuỳ chỉnh) + `product_import_requests` → `order_import_requests.buy_contract2_id` + `product_import_detail_customers`. Đọc cột NOT NULL thật bằng `Schema::getColumnListing` / thử insert trước khi chốt helper.

```php
public function test_groups_by_contract_employee_customer_and_dedupes_products(): void
// 1 dòng giao nhanh, 2 sản phẩm, 2 phiếu nhập cùng HĐ+khách → list() ra 1 nhóm, count(products) == 2, pi_id = phiếu nhập id nhỏ hơn
public function test_matches_import_of_parent_contract(): void
// bc2 con parent_id = bc2 cha; phiếu nhập gắn bc2 cha → nhóm xuất hiện
public function test_requires_import_type_11_status_1(): void
// phiếu nhập type 11 status 0 → không ra
public function test_date_to_includes_whole_day(): void
// phiếu nhập created_at '2026-11-02 15:00:00', filter date_to '02/11/2026' → ra; date_from '03/11/2026' → không ra
public function test_filters(): void
// status '0' / '1', customer_id, contract_code LIKE, bill_adjust_dept_code LIKE (ký tự % được escape), approved_id
public function test_scope_levels(): void
// không quyền → chỉ nhóm employee_id = auth; PERM_COMPANY → em_info.company_id = công ty mình, gửi company_id khác → 0 dòng; PERM_ALL → thấy cả 2
```

Cấp quyền trong test: chèn `employee_has_permissions` với id quyền tên tương ứng (khuôn `DeliveryTripApiTest`).

- [ ] **Step 2: Chạy, thấy FAIL** — `php artisan test Modules/Finance/Tests/Feature/FastDeliveryAccountingServiceTest.php` → class không tồn tại.
- [ ] **Step 3: Viết service** — dùng `ChecksEmployeePermission`; ngày `d/m/Y` → `date_from` `>= Y-m-d 00:00:00`, `date_to` `<= Y-m-d 23:59:59`; LIKE qua `escapeLikeKeyword()`; công ty/phòng/bộ phận người xem lấy từ `auth()->user()->info`, giá trị null ⇒ `whereRaw('1 = 0')`. Subquery phiếu nhập group theo `oir.buy_contract2_id, pidc.customer_id, pi.id` như ERP; `pi_creator_name` qua `employees → employee_infos.fullname`.
- [ ] **Step 4: Seeder** — thêm 5 dòng `$this->perm([...])` + comment 2 dòng (port ERP 02/11/2026, kiểm bằng trait trong `FastDeliveryAccountingService`). `php artisan permission:sync --dry-run` → báo thêm đúng 5 quyền; chạy thật.
- [ ] **Step 5: Chạy test, PASS.**

### Task 2: API danh sách + export-rows

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/FastDeliveryAccountingController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (nhóm mới cạnh `/inventory-imports`)
- Test: `hrm-api/Modules/Finance/Tests/Feature/FastDeliveryAccountingApiTest.php`

**Interfaces:**
- Consumes: Task 1 `list`, `rawQuery`, `group`, `scopeFlags`.
- Produces: `GET /api/v1/finance/fast-delivery-accountings` → `{data: [...nhóm], meta: {...phân trang, permissions: scopeFlags()}}`; `GET …/export-rows?page&limit&fields` → `{headings, widths, rows, total, row_groups, merge_columns}`.

- [ ] **Step 1: Test** — `test_index_returns_groups_and_permissions` (meta.permissions.can_update đúng theo quyền); `test_export_rows_flattens_products_with_groups` (nhóm 2 sản phẩm ⇒ 2 dòng, `row_groups == [2]`, `merge_columns` gồm mọi cột trừ Hàng hoá / Mã hàng); `test_export_rows_blocks_over_2000_raw_rows` (giả lập bằng hằng `EXPORT_RAW_LIMIT` override qua container hoặc mock `count` → 422 "Dữ liệu quá lớn, vui lòng lọc theo điều kiện cụ thể hơn!").
- [ ] **Step 2: Chạy, FAIL.**
- [ ] **Step 3: Viết controller + route.** Export: cột theo spec mục 5 (10 cột, nhãn y ERP; "Chi phí KH" = số + ' ' + loại tiền như ERP; "Đã hạch toán" chữ "Đã hạch toán"/"Chưa hạch toán"). Đếm `rawQuery(...)->count()` ≥ 2000 ⇒ 422 trước khi trả trang 1. `total` = số **nhóm**; phân trang export theo nhóm. Khuôn `DeclareLimitDebtService::exportRows` + `ExportColumns::filter`.
- [ ] **Step 4: Chạy test Task 1 + 2, PASS.**

### Task 3: Nguồn giao nhanh của phiếu kế toán giống ERP + chặn lưu

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillAdjustDeptSourceService.php` (`fromFastDelivery` :643-711, `onBillCreated` :717-743, bảng docblock đầu file dòng cửa 5 → "✅ đã port")
- Modify: `hrm-api/Modules/Finance/Services/BillAdjustDeptWriteService.php` (`store` / `update` truyền ngữ cảnh tạo/sửa)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BillAdjustDeptFastDeliveryTest.php`

**Interfaces:**
- Consumes: Task 1 `byIds(array $ids)`, `PERM_UPDATE`.
- Produces: `fromFastDelivery(array $ids)` header có `type_money_id` (id hoặc `null`), **không** có `exchange_rate` khi ngoại tệ (FE tự lấy tỷ giá danh mục — `BillAdjustDeptForm.vue:624`), `exchange_rate = 1` khi VNĐ; mỗi detail có `fast_delivery_employee_id`. `guardFastDeliveryOnCreate(array $ids): void` (403 / 409).

- [ ] **Step 1: Test**

```php
public function test_source_uses_contract_currency_and_employee(): void
// fixture bc2.currency 'EURO' → header.type_money_id = currencies.id nhỏ nhất name 'EURO'; !array_key_exists('exchange_rate', header); details[*].fast_delivery_employee_id = employee của fixture; 2 dòng Nợ 35241 / Có 811 amount như cũ
public function test_source_vnd_and_unknown_currency(): void
// 'VNĐ' → type_money_id 1, exchange_rate 1; null / 'XYZ' → type_money_id null
public function test_store_forbidden_without_permission(): void
// POST store kèm fast_delivery_ids, user không có PERM_UPDATE → 403, dòng giao nhanh status vẫn 0
public function test_store_conflicts_when_already_accounted(): void
// dòng status 1 (hoặc bill_adjust_dept_id ≠ null) → 409 "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không tạo phiếu
public function test_update_keeps_attached_rows_without_conflict(): void
// sửa phiếu đang tạo vẫn gửi fast_delivery_ids của chính nó → 200, không đổi bill_adjust_dept_id
```

- [ ] **Step 2: Chạy, FAIL.**
- [ ] **Step 3: Sửa.** Loại tiền theo dòng đầu (`byIds` giữ thứ tự id tăng): `'VNĐ'` ⇒ `BillAdjustDept::VND_CURRENCY_ID`; khác ⇒ `currencies` theo `name`, `orderBy('id')->value('id')`. Guard chạy trong transaction, `lockForUpdate` các dòng `buy_contract2_fast_delivery_customers` trước khi kiểm; chỉ ở `store`. `update`: bỏ qua id đang gắn `bill_adjust_dept_id = $model->id`, không ghi id mới (spec 6.3). 403 bằng `abort(403, 'Bạn không có quyền thực hiện thao tác này')` (câu ERP).
- [ ] **Step 4: Chạy test Task 1–3, PASS.** Mở form tạo phiếu KT thường + từ YCĐC trên local (curl `source-data`) để chắc 4 cửa còn lại không đổi.

### Task 4: Popup hợp đồng nhánh giao nhanh

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillAdjustDeptPickerService.php` (`searchContracts` :220, `customerContractQueries` :329)
- Modify: `hrm-client/pages/finance/bill-adjust-depts/components/ContractPickerModal.vue` (prop + query)
- Modify: `hrm-client/pages/finance/bill-adjust-depts/components/BillAdjustDeptForm.vue` (`normalizeRow` :703 giữ `fast_delivery_id` + `fast_delivery_employee_id`; truyền 2 giá trị dòng đang chọn xuống modal)
- Test: thêm vào `BillAdjustDeptFastDeliveryTest.php`

**Interfaces:**
- Produces: `search-contracts` nhận `fast_delivery_employee_id`; có giá trị ⇒ chỉ `firm_contracts` + `wr_service_contracts` của khách (điều kiện trạng thái/loại như hiện tại) **và** `created_by = fast_delivery_employee_id` (ERP `type=hd_ban` + `created_by`). Modal prop `fastDeliveryEmployeeId: [Number, String], default null`.

- [ ] **Step 1: Test** `test_contract_picker_fast_delivery_branch` — có tham số ⇒ mọi `contractable_type` ∈ {FirmContract, WrServiceContract} và created_by đúng; không tham số ⇒ kết quả như trước (so số dòng với lần gọi cũ).
- [ ] **Step 2: FAIL → Step 3: sửa BE + FE → Step 4: PASS.** Kiểm FE: dòng giao nhanh mở popup chỉ ra HĐ bán của NV đó; dòng nhập tay không đổi.

### Task 5: Màn danh sách FE + menu

**Files:**
- Create: `hrm-client/pages/finance/fast-delivery-accountings/index.vue`, `…/components/constants.js`
- Modify: `hrm-client/components/subsystem-menu/finance.js:158` (thêm `link: '/finance/fast-delivery-accountings'`, giữ nguyên nhãn)

**Interfaces:**
- Consumes: Task 2 API (`meta.permissions`).

- [ ] **Step 1: Dựng trang** — chép khuôn `pages/finance/declare-limit-debts/index.vue` (rowspan qua `cellSpan` + `V2BaseSelectRemote` khách hàng) và `pages/finance/inventory-imports/index.vue` (4 mixin, `V2BaseSmartFilterPanel floating`, `V2BaseCompanyDepartmentFilter` với `:permissions="meta.permissions"`, ExportFieldsModal). `columnScreenKey` / `localStorageKey` = `fast_delivery_accountings`. Bảng: mỗi sản phẩm 1 dòng, cột ngoài Hàng hoá gộp theo nhóm. 12 cột + link theo spec 4.5 (Hợp đồng mua qua `contractLink('App\\Model\\Order\\BuyContract2', id)`). Ô tìm nhanh: `keyword` quét mã HĐ mua / mã phiếu nhập / mã-tên khách — thêm vào `rawQuery` ở Task 1 (cập nhật test `test_filters`).
- [ ] **Step 2: Tick + Tạo phiếu kế toán** — checkbox theo spec 4.6 (khoá + tick sẵn khi `status` hoặc `bill_adjust_dept_id`; ẩn nút khi `!meta.permissions.can_update`); bấm khi chưa chọn ⇒ toast "Vui lòng chọn ít nhất một mục để tạo phiếu kế toán"; `this.$router.push('/finance/bill-adjust-depts/create?fast_delivery_ids=' + ids.join(','))`. Tick mất khi đổi trang / lọc.
- [ ] **Step 3: `?status=0`** — `mounted` đọc `$route.query.status === '0'` ⇒ `filters.status = 0` trước lần tải đầu (đè giá trị localStorage).
- [ ] **Step 4: Bấm thử Playwright** (tài khoản dev trong memory `project_moi_truong_dev.md`; tự gán quyền local nếu thiếu, gỡ sau): từng ô lọc chờ ≥ 3s, `?status=0`, tick 2 dòng → form phiếu KT ra đúng loại tiền + 4 dòng định khoản; chụp ảnh danh sách ở 1366px và đặt cạnh `declare-limit-debts`. Đóng browser.

### Task 6: Xuất Excel FE

**Files:**
- Modify: `hrm-client/pages/finance/fast-delivery-accountings/index.vue`

- [ ] **Step 1:** Nút Xuất (`secondary status="success"`) → `ExportFieldsModal` → `exportListFile({ endpoint: 'finance/fast-delivery-accountings/export-rows', … })` khuôn `inventory-imports/index.vue:479-507`, letterhead công ty người đăng nhập, dòng "Từ ngày … Đến ngày …" khi có lọc ngày, tên file `danh_sach_can_hach_toan_chi_phi_van_chuyen_nhanh.xlsx`. 422 ⇒ toast nguyên câu BE.
- [ ] **Step 2:** Xuất thật trên local, mở file kiểm gộp ô + số; xem ảnh.

### Task 7: Hoàn tất

- [ ] Chạy lại `FastDeliveryAccountingServiceTest`, `FastDeliveryAccountingApiTest`, `BillAdjustDeptFastDeliveryTest`, `StockVoucherTripServiceTest` (nhánh mới không đụng, chỉ smoke) — dán output.
- [ ] Checklist `erp-to-hrm-screen` mục A, B, C, F (bỏ mục không áp: Thêm mới, Lịch sử — màn không có bản ghi riêng).
- [ ] Cập nhật `.plans/gop-db/STATUS.md` (mục `hach-toan-cpvc-nhanh`), memory chủ đề kế toán (`project_ke_toan_cong_no.md`, mục mới cuối file). Không commit — chờ user.


## Ngày 02/11/2026 (@junfoke)
- [x] 02/11/2026 — Khảo sát + đề xuất thứ tự 5 màn chuyển đổi tiếp (CPVC nhanh → Sổ chi tiết công nợ NV → các màn công nợ NCC/NV). "Công nợ đầu kỳ theo khách hàng - hợp đồng" HRM đã có (port 01/10, `/finance/declare-debt-beginnings`); đối chiếu ERP: 2 mục menu cùng route `declareDebtBeginning.index`, không có tham số riêng → không cần làm thêm.
- [x] 02/11/2026 — Làm chuyển đổi erp->hrm: Danh sách cần hạch toán chi phí vận chuyển nhanh - 100%: spec (qua reviewer; user chốt hủy phiếu KT giữ như hiện tại, không gỡ dòng giao nhanh) + plan 7 task; BE service truy vấn dùng chung (danh sách, Excel chặn ≥2.000 dòng, nạp phiếu KT), 5 quyền cuối seeder; sửa nguồn giao nhanh của phiếu kế toán giống ERP (loại tiền + tỷ giá theo HĐ mua — trước ép VNĐ trong khi 21/22 dòng thật là ngoại tệ; NV chịu phí; popup HĐ chỉ HĐ bán của NV chịu phí); FE màn danh sách 12 cột gộp ô, tick + Tạo phiếu KT, `?status=0`, Excel, link menu. 18/18 test, bấm thử local (phiếu ra JPY, Nợ 35241 / Có 811), review toàn nhánh.
- [x] 02/11/2026 — Commit api `1afcdb68c`, client `bb317da69`; đã lên `origin/develop` (client merge `48477d3e8`). Kiểm dev-hrm đã `permission:sync` (993/993) và seeder đã kiểu đồng bộ theo tên (từ 14–15/10) → khi lên dev chạy lại `permission:sync` để có 5 quyền mới, gán quyền cho kế toán.
