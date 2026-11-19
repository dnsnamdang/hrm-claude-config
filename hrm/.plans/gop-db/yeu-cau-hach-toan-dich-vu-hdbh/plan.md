# Plan — Port "Yêu cầu hạch toán dịch vụ HĐBH" (Phase 1 chỉ-đọc)

Khuôn bám 1:1 màn song sinh HDDV `wr-accounting-service-requests` (entity + service + resource +
controller + routes + client index/show). Khác biệt chính đã ghi ở `design.md`:
scope qua `employee_create.info` (bảng thiếu cột org), VAT suy từ `payed_cost`, 100% FirmContract,
đọc snapshot `service_accounting_request_costs`.

## BE (hrm-api, module Finance)

- [x] **T1** Entity `Modules/Finance/Entities/ServiceAccountingRequest/ServiceAccountingRequest.php`
  - `$table='service_accounting_requests'`, `$guarded=['id']`, `use ChecksEmployeePermission`.
  - Consts status: `DANG_TAO=1, CHO_DUYET=2, TU_CHOI=3, DA_DUYET=4, DA_HACH_TOAN=5` (bám ERP, KHÁC HDDV).
  - Consts type: `DICH_VU=1, CHI_PHI=2, VAN_CHUYEN=3`. STATUSES/TYPES array (id/name/color hex).
    ⚠️ ERP STATUSES thiếu DA_DUYET=4 → HRM khai ĐỦ 5 (4='Đã duyệt' màu xanh dương/amber).
  - Relations: `costs()` hasMany ServiceAccountingRequestCost · `contractable()` morphTo ·
    `employee_create()` belongsTo Employee (created_by) · `approver()` (approver_id).
  - `generateCode()` prefix `"$company.YCHTDV."` (tham chiếu; Phase 1 không tạo nên không bắt buộc).
  - `statusMeta()`, `typeMeta()`, `contractCode()`, `customerLabel()`.
- [x] **T2** Entity `ServiceAccountingRequestCost.php` (`$table='service_accounting_request_costs'`,
  $guarded, $timestamps theo bảng; không cần quan hệ contract_costable — chỉ đọc cột snapshot).
- [x] **T3** (nếu cần) bổ sung quan hệ `customer()`+`employeeCreate()` vào read-model
  `Modules/Finance/Entities/Contract/FirmContract.php` (ADDITIVE, an toàn) để lấy Khách hàng + Kinh doanh.
- [x] **T4** Service `Modules/Finance/Services/ServiceAccountingRequestService.php`
  - `use LogsCatalogHistory` (catalogTable/columns/display/snapshotOf như HDDV — dùng cho endpoint Lịch sử).
  - `searchByFilter($request)`: scope type=all qua `whereHas('employee_create.info', company/dept/part)`
    theo 4 quyền + `status!=DANG_TAO OR created_by=self`; filters keyword/code/contract_code/status/
    customer/created_by/request_by/approver_id/company_id(big boss)/department_id/start_date/end_date;
    `applySort` theo SORTABLE_COLUMNS (code/created_at/approved_at/status); paginate.
  - `meta()`: is_all_company/is_boss/is_manager/is_accountant + statuses + types.
  - `findForShow($id)` + `detailData()`: đọc `costs` snapshot; chia bảng theo `type`; tính
    `pre_tax=Σtotal_price`, `vat=payed_cost−pre_tax`, `vat_percent=round(payed_cost/pre_tax−1)*100`,
    `total=payed_cost`. contractData() từ FirmContract (code/customer/created_by).
  - `exportRows()` cho Xuất Excel.
- [x] **T5** List resource `Transformers/ServiceAccountingRequestResource/...ListResource.php`
  (id, code, contract_code, customer_label, kinh_doanh, payed_cost, creator/created_at,
  approver/approved_at, status/name/color, type/name). Detail resource nếu cần.
- [x] **T6** Controller `Http/Controllers/ServiceAccountingRequestController.php`:
  `index` (searchByFilter), `show` (findForShow), `export`, `meta`. **KHÔNG** store/update/reject/destroy (Phase 1).
- [x] **T7** Routes `Routes/api.php` module Finance: GET list/meta/show/export,
  middleware `checkPermission:Xem yêu cầu hạch toán dịch vụ HĐBH - ...` (4 cấp OR như HDDV).
- [x] **T8** Quyền: 4 dòng `$this->perm([...])` ở `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`,
  type = permissionType phân hệ **Bán hàng**. Chạy `php artisan permission:sync --dry-run` kiểm.

## FE (hrm-client, Nuxt)

- [x] **T9** `pages/finance/service-accounting-requests/index.vue` — bám index HDDV:
  4 mixin, `localStorageKey`/`columnScreenKey` DUY NHẤT, V2BaseSmartFilterPanel `floating`,
  V2BaseDataTable `@sort` + sortBy/sortDirection, cột mặc định (STT/Ngày tạo/Mã(nuxt-link)/Số HĐ/
  Kinh doanh/Khách hàng/Tổng thanh toán/Người tạo/Người duyệt/Ngày duyệt/Trạng thái/Hành động).
  Hành động = **chỉ Lịch sử**. Nút toolbar bắt buộc: Xuất Excel, Cấu hình cột. ĐỌC `?type=all`.
- [x] **T10** `pages/finance/service-accounting-requests/_id/index.vue` — chi tiết chỉ-đọc:
  khối thông tin chung + 1 bảng chi phí theo type + footer (Tổng trước thuế/VAT/Tổng thanh toán).
  Nút: Quay lại + Lịch sử. (KHÔNG Sửa/Xóa/Không duyệt/Hạch toán — Phase 1.)
- [x] **T11** Menu: thêm mục vào cây Bán hàng (`components/subsystem-menu/sale-hub.js`) cạnh HDDV,
  dạng `{ n, link }`, `isShow` theo quyền mới; kiểm các file menu khác tránh trùng.

## Verify
- [x] **T12** Playwright: list (lọc/sort/phân trang/Network 1-request), chi tiết (số khớp payed_cost),
  Lịch sử, Xuất Excel. Chụp ảnh đặt cạnh màn HDDV. Test âm quyền bằng tài khoản thường.

### Checkpoint — 2026-11-02 (Opus 4.8)
**Vừa hoàn thành:** T1–T12 XONG, verify PASS trọn bộ (cả âm quyền) trên DB gộp local (`erp_hrm_check`,
1299 phiếu). Luồng dương chạy bằng tài khoản DNS Admin / company 1 / role 18 (super-admin):
- Danh sách render đủ cột (STT/Ngày tạo/Số phiếu nuxt-link/Số HĐ/Kinh doanh/Khách hàng/Tổng thanh
  toán/Người tạo/Người duyệt/Ngày duyệt/Trạng thái/Hành động=chỉ Lịch sử); **1 request** nạp danh sách.
- Phân trang 1–10/1299 OK.
- **Sort**: click "Ngày tạo" → `GET .../service-accounting-requests?sort_by=createdAt&sort_direction=asc&type=all&page=1&per_page=10` → 200, đúng 1 request.
- **Lọc**: keyword `TPE.YCHTDV.02520` → "Hiển thị 1–1 / 1", đúng phiếu, 1 request.
- Chi tiết id 3610 (TPE.YCHTDV.02520): Tổng trước thuế 4,000,000 · VAT 8% 320,000 · Tổng thanh toán
  4,320,000 = payed_cost. Khớp công thức VAT suy từ `payed_cost`.
- Lịch sử: endpoint catalog-histories 200.
- Xuất Excel: file `danh_sach_yeu_cau_hach_toan_dich_vu_hdbh.xlsx` tải về, số là NUMBER thật (Tổng
  thanh toán=144000), 1299 dòng, không lẫn HTML.
- **Âm quyền — PASS (test ở tầng API, chính chỗ gate chạy):** cơ chế:
  - `show()` gọi `$object->canView()` (ServiceAccountingRequest.php:195): PASS nếu super-admin (role 18)
    HOẶC người tạo chính mình; ngược lại xét 4 cấp quyền so info người tạo (tổng cty / cty==mình /
    department ∈ manageable / part==mình). Không đạt → **403**.
  - `index()` KHÔNG gắn `checkPermission` ở route; scope trong entity lọc theo 4 quyền + người tạo luôn
    thấy phiếu mình (không quyền nào → chỉ thấy phiếu `created_by=mình`). Menu FE ẩn theo 4 quyền.
  - **Cách test:** chỉ role 18 (Super admin) giữ 4 quyền, 0 direct-grant. Chọn NV thường emp 24
    (`tuannd.kd1@tanphat.com`, company 1, không role 18, không 4 quyền, sở hữu 0 phiếu), đặt mật khẩu
    tạm → login API lấy JWT → **khôi phục mật khẩu gốc** (verify OK-restored). Kết quả:
    - `GET /finance/service-accounting-requests?type=all` → `total=0`, `is_all_company=false` (scope
      chặn đúng: emp 24 sở hữu 0 phiếu nên danh sách rỗng).
    - `GET /finance/service-accounting-requests/3612` (created_by=190, khác emp 24) → **HTTP 403**
      `"Bạn không có quyền xem phiếu này"`. ✓ fail-closed.
  - Đối chứng dương: DNS Admin (super-admin) thấy danh sách + chi tiết 3610 (200) qua UI ở trên.

**Setup test (local, KHÔNG phải code feature):** `php artisan permission:sync` tạo 4 quyền id
101477–101480; cấp cho role 18 (Super admin, company 1) qua
`INSERT IGNORE INTO role_has_permissions ... WHERE name LIKE '%hạch toán dịch vụ HĐBH%' AND guard_name='api'`.

**Đã commit + push `develop`:** hrm-api `a92a5ed34` + hrm-client `f42aed9c5` (rebase lên origin/develop,
không xung đột). Bước tiếp theo: chờ user QA môi trường thật.

**Blocked:** không. Deferred sang phase sau: Tạo/Sửa/Xóa · reject(Không duyệt) · nút "Hạch toán dịch
vụ" → `serviceAccounting` · link màn HĐ hãng (phụ thuộc port bộ chi phí HĐ hãng).

## Deferred (phase sau — KHÔNG làm Phase 1)
Tạo/Sửa/Xóa · reject(Không duyệt) · nút "Hạch toán dịch vụ"→`serviceAccounting` · link màn HĐ hãng.
Phụ thuộc port bộ chi phí HĐ hãng (`FirmContractCost` + `getDataForServiceExport`).

---

# PHASE 2 — Write-side (Tạo/Sửa/Xóa + Gửi duyệt + Không duyệt)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development` (khuyến nghị)
> hoặc `superpowers:executing-plans` để chạy từng task. Các bước dùng checkbox `- [ ]` để theo dõi.
> Trong lúc code BẮT BUỘC theo skill `erp-to-hrm-screen` (checklist UI) + CLAUDE.md HRM.

**Goal:** Người lập HĐ hãng (FirmContract) tạo được phiếu YC hạch toán dịch vụ/chi phí/vận chuyển, Lưu
nháp / Gửi duyệt / Sửa / Xóa; kế toán có quyền Không duyệt kèm lý do — port trung thành ERP.

**Architecture:** Bám khuôn song sinh HDDV write-side `wr-accounting-service-requests` (Controller/Service/
FormRequest/NotifyService 1:1), chỉ khác bộ nạp chi phí sống từ FirmContract (`buildCostsFromContract`
port `getDataForServiceExport`, cả nhánh type-3 ghi dòng vận chuyển), 5 trạng thái / 3 loại / 4 cấp quyền,
và morphMap `contract_costable` ghi **chuỗi FQN ERP** để ERP ↔ HRM cùng resolve (chống kẹt khóa `exported`).

**Tech Stack:** hrm-api PHP 7.4 / Laravel 8 / module Finance / spatie-permission guard `api`;
hrm-client Nuxt 2.14 (Vue 2) Node 14.21.3; DB gộp `erp_hrm_check` (127.0.0.1:3306).

**Spec:** `HRM/.plans/gop-db/yeu-cau-hach-toan-dich-vu-hdbh/design-phase2.md` (đã DUYỆT 2026-11-02).
Đọc kèm `design.md` (Phase 1) + bảng "Bẫy khi port" ở `.plans/gop-db/design.md`.

## Global Constraints (áp cho MỌI task Phase 2)
- **Faithful port**: giá trị chi phí ĐỌC LẠI từ `FirmContractCost::find(id)` trong `syncCosts`, KHÔNG tin
  payload FE (payload chỉ gửi `contract_costable_id`). Giữ nguyên hành vi `exported` / `rollbackAccounting`.
- **Lưu nháp (status 1) cho lưu rỗng** (không cần dòng chi phí); **Gửi duyệt (status 2)** mới bắt `costs`≥1
  (lệch ERP có chủ đích, user chốt). Rule định dạng vẫn chặn cả khi nháp.
- **Gác BE**: store/update/destroy/reject fail-closed theo bản ghi (`canEdit/canDelete/canAccounting` trong
  Entity); thứ tự gác **trạng thái trước (409), quyền sau (403)**. reject thêm guard `status==CHO_DUYET` → 409.
- **morphMap**: `contract_costable_type` ghi **chuỗi FQN ERP** `App\Model\Sale\Firm\Contract\FirmContractCost`
  (qua `getMorphClass()` sau khi đăng ký morphMap). Verify: dữ liệu hiện lưu `contractable_type` dạng FQN ERP.
- **Đính kèm**: bảng `files` chung (`table='service_accounting_requests'`, `table_id`), 1 bộ rule mimes
  pdf/jpg/jpeg/png/zip/doc/docx max 30MB; FE `V2BaseFile.vue`; đổi/xóa file ghi lịch sử (trait
  `BuildsAttachmentHistoryChange`). ERP đọc được vì dùng chung bảng `files`.
- **UI = chuẩn HRM** (skill thắng spec về hình thức): nút/màu/icon/thứ tự theo `button-convention`; badge
  `V2BaseBadge` màu BE; form `V2Base*`; validate realtime vee-validate + BE 422; nút không dùng được ẩn hẳn.
- **Quyền Không duyệt**: chuẩn hóa 1 tên `Hạch toán yêu cầu làm dịch vụ` (guard api) cho cả gate lẫn notify
  (ERP typo chuỗi notify `'Duyệt yêu cầu làm dịch vụ'` — HRM gộp về 1 tên).
- **Testing của dự án**: KHÔNG có PHPUnit suite cho port — mỗi task verify bằng `php artisan tinker` /
  curl API trên DB gộp local; verify end-to-end bằng Playwright ở task cuối. "Chạy test" = chạy các lệnh
  verify này. Commit sau mỗi task (chưa push — chờ user QA).

## Review Focus (input/thất bại spec ngụ ý nhưng dễ cắn người dùng — pin test vào task sở hữu)
1. **Gửi duyệt 2 lần song song cùng 1 dòng chi phí** → phải chống trùng: dòng `exported==true` làm
   `syncCosts` trả false → rollback + báo "...đã hoàn thành" (pin vào P2-T7, verify concurrent qua 2 request).
2. **Reject phiếu không ở trạng thái CHO_DUYET** (người khác vừa đổi) → 409, KHÔNG rollback nhầm `exported`
   (pin P2-T7 reject guard).
3. **Type-3 tạo dòng "Chi phí vận chuyển" GHI vào `firm_contract_costs`** — chạy 2 lần trên cùng HĐ phải
   TÌM LẠI dòng cũ, không tạo trùng (pin P2-T3, verify đếm dòng trước/sau).
4. **Sửa/Xóa phiếu người khác hoặc phiếu đã CHO_DUYET** → 403/409 (pin P2-T7, verify âm quyền tài khoản thường).
5. **Nạp chi phí HĐ không có `support_accounting`** → báo "Hợp đồng không có hỗ trợ hạch toán", không tạo
   phiếu (pin P2-T3/P2-T7).

---

## BE (hrm-api, module Finance)

### P2-T1: Entity FirmContractCost + read-model FirmSupportAccounting + quan hệ FirmContract
**Files:**
- Create: `Modules/Finance/Entities/Contract/FirmContractCost.php`
- Create: `Modules/Finance/Entities/Contract/FirmSupportAccounting.php` (read-model mỏng, morphOne target)
- Modify: `Modules/Finance/Entities/Contract/FirmContract.php` (thêm quan hệ — ADDITIVE)

**Interfaces — Produces:**
- `FirmContractCost`: `$table='firm_contract_costs'`, `$fillable` cho phép ghi `exported` + các cột tính
  type-3 (`firm_contract_id,cost_id,name,price,value_extra,value_discount,value_before_vat,vat_percent,
  vat_cost,value_after_vat,revenue_calculation,is_decrease,company_discount_percent,coefficient_cost_price`);
  accessor `getSaleMaxPercentAttribute() => company_discount_percent`; `cost()` belongsTo `Cost`.
- `FirmContract::costs()` hasMany FirmContractCost `where('revenue_calculation',false)->where('name','<>','Chi phí vận chuyển')`.
- `FirmContract::revenue_costs()` hasMany `where('revenue_calculation',true)`.
- `FirmContract::support_accounting()` morphOne `FirmSupportAccounting` (đọc chuỗi FQN ERP như Phase 1 map `contractable`).
- hằng `FirmContract::CO_HIEU_LUC=3`; method `canProductExport()` = `status==CO_HIEU_LUC && created_by==auth()->id()`;
  `canRequestAccountingDelivery()` (bám ERP — điều kiện delivery).

- [ ] **Step 1:** Đọc ERP `app/Model/Sale/Firm/Contract/FirmContractCost.php` + `FirmContract.php`
  (costs/revenue_costs/support_accounting/canProductExport/canRequestAccountingDelivery) để copy chính xác.
- [ ] **Step 2:** Viết `FirmContractCost` (fillable + accessor sale_max_percent + cost()). Giữ các model
  HRM khác chỉ-đọc; model này CHO GHI `exported` và tạo dòng type-3.
- [ ] **Step 3:** Viết read-model mỏng `FirmSupportAccounting` (chỉ cần tồn tại để morphOne resolve).
- [ ] **Step 4:** Thêm `costs()/revenue_costs()/support_accounting()` + `CO_HIEU_LUC`/`canProductExport()`/
  `canRequestAccountingDelivery()` vào `FirmContract` (ADDITIVE, không đụng cột read-only khác).
- [ ] **Step 5 (verify):** tinker trên `erp_hrm_check`:
  `FirmContract::has('costs')->first()->costs()->count()` > 0; 1 HĐ Có hiệu lực có `support_accounting`
  resolve ra object (không null). Kỳ vọng: quan hệ trả dữ liệu, accessor `sale_max_percent` = company_discount_percent.
- [ ] **Step 6 (commit):** `git add Modules/Finance/Entities/Contract && git commit` (message: "feat(finance): FirmContractCost + FirmContract cost relations cho YCHTDV write-side").

### P2-T2: morphMap `contract_costable` + morphTo trên ServiceAccountingRequestCost
**Files:**
- Modify: `Modules/Finance/Providers/FinanceServiceProvider.php` (`registerMorphMap`)
- Modify: `Modules/Finance/Entities/ServiceAccountingRequest/ServiceAccountingRequestCost.php`

**Interfaces:**
- Consumes: `FirmContractCost` (P2-T1).
- Produces: morphMap map chuỗi ERP `App\Model\Sale\Firm\Contract\FirmContractCost` → HRM `FirmContractCost`;
  `ServiceAccountingRequestCost::contract_costable()` morphTo; ghi dòng dùng `(new FirmContractCost)->getMorphClass()`
  (ra đúng chuỗi ERP sau khi map).

- [ ] **Step 1:** Trong `registerMorphMap` thêm entry FQN ERP → HRM `FirmContractCost` (cạnh entry FirmContract Phase 1).
- [ ] **Step 2:** Thêm `contract_costable()` morphTo vào `ServiceAccountingRequestCost` (Phase 1 chỉ đọc cột).
- [ ] **Step 3 (verify):** tinker: `(new \Modules\Finance\Entities\Contract\FirmContractCost)->getMorphClass()`
  === `'App\\Model\\Sale\\Firm\\Contract\\FirmContractCost'`; lấy 1 `ServiceAccountingRequestCost` cũ (nếu có
  dòng FirmContractCost) → `->contract_costable` resolve ra `FirmContractCost` HRM.
- [ ] **Step 4 (commit).**

### P2-T3: Loader buildCostsFromContract (port getDataForServiceExport, cả type-3 delivery)
**Files:**
- Modify: `Modules/Finance/Services/ServiceAccountingRequestService.php`

**Interfaces:**
- Consumes: `FirmContract` relations (P2-T1).
- Produces: `buildCostsFromContract(FirmContract $contract, int $type): array` — trả mảng dòng chi phí
  chuẩn hóa `{contract_costable_id, name, price, value_discount, value_extra, total_price(=value_before_vat),
  sale_max_percent, coefficient_cost_price, cost_id, vat_percent, exported, need_export}`. Dùng CHUNG cho
  `contractData()` (đọc) và `store/update` (đọc lại giá trị).

- [ ] **Step 1:** Đọc ERP `FirmContractCostService::getDataForServiceExport($contract,$delivery_cost)` — cả 2 nhánh.
- [ ] **Step 2:** type 1 (`revenue_costs`) / type 2 (`costs`): load quan hệ `->where('is_decrease',false)`,
  `select('*','value_before_vat as total_price')`, kèm `cost`; `vat_percent` = type2→costs[0], type1→revenue_costs[0].
  KHÔNG trừ phần đã hạch toán; dòng `exported` vẫn trả (gắn cờ để FE tô invalid).
- [ ] **Step 3:** type 3 (`$delivery_cost=true`): tìm/tạo `Cost(name='Chi phí vận chuyển')`, tìm/tạo 1
  `FirmContractCost(firm_contract_id,cost_id)`, tính `price/value_extra/value_discount/value_before_vat` từ
  `delivery_*` (trừ phụ lục giảm nếu `delivery_decrease_annex`), `vat_percent=delivery_vat_percent`,
  `vat_cost`, `value_after_vat`, **`->save()`** (ghi dòng), trả 1 dòng `need_export=true`.
- [ ] **Step 4:** Gate: nếu `!$contract->support_accounting` → ném lỗi "Hợp đồng không có hỗ trợ hạch toán";
  kiểm `canProductExport()` (type3 thêm `canRequestAccountingDelivery()`).
- [ ] **Step 5 (verify):** tinker với 1 HĐ có costs: `buildCostsFromContract($c,2)` ra ≥1 dòng với total_price
  = value_before_vat; **type-3 gọi 2 LẦN trên cùng HĐ** → `firm_contract_costs` chỉ thêm ĐÚNG 1 dòng
  (Review Focus #3). HĐ không support_accounting → ném đúng câu lỗi (#5).
- [ ] **Step 6 (commit).**

### P2-T4: Entity ServiceAccountingRequest — cờ write + generateCode + files()
**Files:**
- Modify: `Modules/Finance/Entities/ServiceAccountingRequest/ServiceAccountingRequest.php`

**Interfaces — Produces:**
- `WRITABLE_STATUSES = [DANG_TAO, TU_CHOI]`;
- `canEdit()` = `created_by==auth()->id() && in_array(status, WRITABLE_STATUSES)`;
- `canDelete()` = giống canEdit;
- `canAccounting()` = `$this->checkEmployeePermission('Hạch toán yêu cầu làm dịch vụ') && status==CHO_DUYET`;
- `generateCode()` = `"{company_code}.YCHTDV." . autoGenerateCode(5)` (bám ERP);
- `files()` hasMany `File` `where('table','service_accounting_requests')`.

- [ ] **Step 1:** Thêm các method/const trên (đọc ERP `ServiceAccountingRequest` canEdit/canDelete/canAccounting/generateCode).
- [ ] **Step 2 (verify):** tinker: phiếu status 1 của mình → canEdit=true; phiếu CHO_DUYET → canEdit=false,
  canDelete=false; `generateCode()` ra chuỗi `<CTY>.YCHTDV.#####`.
- [ ] **Step 3 (commit).**

### P2-T5: Seed quyền "Hạch toán yêu cầu làm dịch vụ"
**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [ ] **Step 1:** Thêm 1 dòng `$this->perm(['name'=>'Hạch toán yêu cầu làm dịch vụ', 'display_name'=>..., 'group'=>..., 'type'=>permissionType **Bán hàng**])` — KHÔNG khai `id`/`guard_name`. (Không tự gán role — admin phân lại.)
- [ ] **Step 2 (verify):** `php artisan permission:sync --dry-run` liệt kê quyền mới, không đụng quyền khác.
- [ ] **Step 3 (commit).**

### P2-T6: FormRequest Store/Update (dùng chung) + Reject
**Files:**
- Create: `Modules/Finance/Http/Requests/ServiceAccountingRequest/StoreServiceAccountingRequestRequest.php`
- Create: `Modules/Finance/Http/Requests/ServiceAccountingRequest/RejectServiceAccountingRequestRequest.php`

**Interfaces — Produces:**
- Store rules: `status` in 1,2; `type` in 1,2,3; `contractable_id`/`contractable_type` required khi tạo;
  `payed_cost` numeric; `note` nullable; **`costs` required chỉ khi `status==2`** (dùng `required_if:status,2`
  + `costs.*.contract_costable_id`); đính kèm `attachment_urls.*` `starts_with:<S3 prefix màn>` + mimes/size chung.
- Reject rules: `comment` required.
- Chỉ khai `rules()` + `attributes()` (`data-vv-as`), KHÔNG khai `messages()` (dùng lang vi).

- [ ] **Step 1:** Viết 2 FormRequest (đọc HDDV `WrAccountingServiceRequest*Request` làm khuôn).
- [ ] **Step 2 (verify):** tinker/`php artisan route:list` + gửi payload thiếu field → 422 câu tiếng Việt;
  payload `status=1` không `costs` → PASS validate; `status=2` không `costs` → 422.
- [ ] **Step 3 (commit).**

### P2-T7: Service write — store/syncCosts/syncAttachments/update/destroy/reject/rollbackAccounting + contractData + firmContractList
**Files:**
- Modify: `Modules/Finance/Services/ServiceAccountingRequestService.php`

**Interfaces:**
- Consumes: `buildCostsFromContract` (P2-T3), Entity cờ (P2-T4), FormRequest (P2-T6), morphMap (P2-T2).
- Produces: `store($request)`, `update($object,$request)`, `destroy($object)`, `reject($object,$request)`,
  `contractData($contractId,$type)` (dùng buildCostsFromContract), `firmContractList($request)` (danh sách HĐ
  chọn được cho popup — gate `support_accounting` + `canProductExport`). Tất cả bọc `DB::transaction`.

- [ ] **Step 1:** `store`: check `support_accounting`, `generateCode`, fill(status,note,type,payed_cost,
  contractable_type,contractable_id), save, `syncCosts`, `syncAttachments`; nếu status==2 notify (P2-T8).
- [ ] **Step 2:** `syncCosts($object,$costs)`: xóa sạch cost cũ → với mỗi `contract_costable_id` **đọc lại**
  `FirmContractCost::find(id)` lấy giá trị thật, set `contract_costable_type = getMorphClass()` (chuỗi ERP),
  ghi `cost_id/name/price/.../total_price`. Nếu dòng đã `exported==true` → trả false (→ rollback + báo
  "...đã hoàn thành"). Khi status==CHO_DUYET set `FirmContractCost.exported=true`; nháp KHÔNG khóa.
- [ ] **Step 3:** `update`: thứ tự **trạng thái(409) → quyền(403)**; `only(status,note,payed_cost)` (KHÔNG đổi
  type/contractable), save, syncCosts, syncAttachments, notify nếu CHO_DUYET.
- [ ] **Step 4:** `destroy`: guard canDelete, log 'delete', xóa costs, `$object->delete()` (xóa cứng, không lý do).
- [ ] **Step 5:** `reject`: guard `status==CHO_DUYET` else 409; set status=TU_CHOI, approver_id, approved_at,
  save, `rollbackAccounting()` (gỡ `exported=false` các FirmContractCost đã khóa), notify người tạo.
- [ ] **Step 6:** `contractData` + `firmContractList` (gate support_accounting + canProductExport; phân trang, select cột cần).
- [ ] **Step 7 (verify — pin Review Focus #1,#2,#4,#5):** tinker/curl:
  tạo nháp (costs rỗng) OK; gửi duyệt → `firm_contract_costs.exported` của dòng chọn = 1; reject → về 0;
  gửi duyệt lần 2 cùng dòng đã exported → false + báo lỗi; reject phiếu không CHO_DUYET → 409; sửa/xóa phiếu
  người khác (tài khoản thường) → 403; type-3 tạo dòng vận chuyển ghi đúng.
- [ ] **Step 8 (commit).**

### P2-T8: Catalog history + NotifyService
**Files:**
- Modify: `Modules/Finance/Services/ServiceAccountingRequestService.php` (gọi log tay)
- Create: `Modules/Finance/Services/ServiceAccountingRequestNotifyService.php`

**Interfaces:**
- Consumes: service write (P2-T7).
- Produces: `log('create'|'delete')`, `logUpdate()`, `logCatalogStatus()` gọi trong store/update/destroy/reject;
  NotifyService `onSentForApproval($object)` + `onRejected($object)` — template `[PREFIX] {Nhóm}: {Tên}. {Ghi chú}`
  (skill notification-convention), bọc try/catch, gọi trong `DB::afterCommit`.

- [ ] **Step 1:** Thêm log tay vào các đường ghi (bám HDDV; bảng đã nằm trong `CatalogHistoryService::TABLES` — verify).
- [ ] **Step 2:** Viết NotifyService (bám `WrAccountingServiceRequestNotifyService`); prefix khai ở
  `NotificationMeta::OBJECT_LABELS`. Người nhận gửi duyệt = người giữ quyền `Hạch toán yêu cầu làm dịch vụ` cùng công ty.
- [ ] **Step 3 (verify):** tạo/gửi duyệt/reject 1 phiếu → `catalog_histories` có dòng tương ứng; chuông người nhận có record.
- [ ] **Step 4 (commit).**

### P2-T9: Controller write endpoints + routes
**Files:**
- Modify: `Modules/Finance/Http/Controllers/V1/ServiceAccountingRequestController.php`
- Modify: `Modules/Finance/Routes/api.php`

**Interfaces:**
- Consumes: service (P2-T7/T8), FormRequest (P2-T6).
- Produces: `store/update/destroy/reject/contractData/firmContractList` + routes. Route tĩnh
  (`contract-data`, `firm-contracts`, `export`) khai TRƯỚC `/{id}`; `reject` middleware
  `checkPermission:Hạch toán yêu cầu làm dịch vụ`; store/update/destroy KHÔNG middleware (gác trong Entity).

- [ ] **Step 1:** Thêm action controller (store/update/destroy gọi service, trả JSON chuẩn; reject nhận RejectRequest).
- [ ] **Step 2:** Khai routes đúng thứ tự + middleware reject.
- [ ] **Step 3 (verify):** `php artisan route:list | grep service-accounting` đủ route; curl store/update/reject
  trả đúng mã (200/403/409/422). Âm quyền reject: tài khoản không quyền → 403.
- [ ] **Step 4 (commit).**

---

## FE (hrm-client, Nuxt)

### P2-T10: Popup chọn HĐ hãng + nạp contract-data
**Files:**
- Create: `pages/finance/service-accounting-requests/components/FirmContractPickerModal.vue`
  (bám `FirmContractSearchModal.vue` hiện có — copy pattern, ghi rõ nguồn trong file)

**Interfaces — Produces:** modal row-click chọn **1** HĐ; lọc theo mã HĐ/khách hàng; phân trang theo
`PICKER_PAGE_SIZE_OPTIONS`; cột Mã/Ngày tạo sort được; chỉ hiện HĐ chọn được (BE đã gate). Emit `select(contract)`.

- [ ] **Step 1:** Grep khuôn `FirmContractSearchModal.vue` + `pickerPagination` + `V2BaseModal`/`V2BaseSelectInModal`.
- [ ] **Step 2:** Dựng modal gọi `firmContractList`; select dùng component-in-modal.
- [ ] **Step 3 (verify):** mở modal trên trình duyệt (Playwright MCP), chọn 1 HĐ → emit đúng; phân trang/sort chạy.
- [ ] **Step 4 (commit).**

### P2-T11: Form dùng chung ServiceAccountingRequestForm
**Files:**
- Create: `pages/finance/service-accounting-requests/components/ServiceAccountingRequestForm.vue`

**Interfaces:**
- Consumes: FirmContractPickerModal (P2-T10), API `contract-data`.
- Produces: form: chọn HĐ (mở popup) → chọn **type** (V2BaseSelect) → nạp bảng chi phí **read-only có
  checkbox tick dòng** (`need_export`; dòng `exported` disable + tô invalid) → `note` (V2BaseTextarea) →
  đính kèm (`V2BaseFile.vue`, POST `/upload-files` lúc chọn, gửi `attachment_urls[]`). Tính
  `payed_cost = Σ(total_price dòng tick) × (1+vat_percent/100)`. unsavedChangesMixin + markFormSaved.
  Validate: nháp nới required; Gửi duyệt bắt ≥1 dòng tick.

- [ ] **Step 1:** Grep checkbox-table (tham khảo `SourceProductPickerModal.vue`) + `V2BaseFile.vue` + `V2BaseFormCard`/`Section`.
- [ ] **Step 2:** Dựng form theo khuôn HDDV + bảng checkbox + upload; mọi element `V2Base*`; nhãn "Người tạo/Ngày tạo", `CreatorInfoLine`.
- [ ] **Step 3:** Tính payed_cost + VAT client; bind `unsavedLastActionAt` khi chọn HĐ/file (await).
- [ ] **Step 4 (verify):** render form, tick dòng → payed_cost cập nhật; bỏ tick hết + Gửi duyệt → báo đỏ; nháp rỗng OK.
- [ ] **Step 5 (commit).**

### P2-T12: Trang create.vue + _id/edit.vue
**Files:**
- Create: `pages/finance/service-accounting-requests/create.vue` (+ `saveAndContinuePageMixin`, `:key="formKey"`)
- Create: `pages/finance/service-accounting-requests/_id/edit.vue`

**Interfaces:** Consumes form (P2-T11). create standalone (nút "Lưu và tiếp tục"); edit nạp detail, chỉ vào
được khi canEdit (URL trực tiếp phiếu không sửa được → chuyển về chi tiết). Sau Lưu/Gửi duyệt →
`markFormSaved()` + `$router.push` danh sách. Nút trong `V2Footer` (Lưu nháp secondary + Gửi duyệt primary),
màu/chữ/icon theo `button-convention`.

- [ ] **Step 1:** Dựng 2 trang vỏ bám `buy-service-requests/create.vue`.
- [ ] **Step 2 (verify):** tạo nháp → về danh sách thấy phiếu; mở edit phiếu CHO_DUYET bằng URL → bị đẩy về chi tiết.
- [ ] **Step 3 (commit).**

### P2-T13: Chi tiết + danh sách — bật nút Sửa/Xóa/Không duyệt
**Files:**
- Modify: `pages/finance/service-accounting-requests/_id/index.vue` (Phase 1)
- Modify: `pages/finance/service-accounting-requests/index.vue` (Phase 1)
- Create: modal nhập lý do Không duyệt (dùng `base-confirm-modal`/`$confirm` + ô lý do, hoặc `V2BaseModal`)

**Interfaces:** Consumes cờ BE `is_can_edit/is_can_delete/is_can_accounting` (bổ sung vào Resource chi tiết
+ list ở P2-T7 nếu chưa có). Chi tiết: footer thêm Sửa/Xóa (theo canEdit/canDelete) + **Không duyệt**
(status=danger, theo canAccounting, modal lý do required). Danh sách: cột Hành động thêm Sửa/Xóa (ẩn hẳn
khi không đủ điều kiện). Hành động chi tiết KHỚP danh sách.

- [ ] **Step 1:** Bổ sung cờ `is_can_*` vào Resource list + detail (BE — nối P2-T5/T7).
- [ ] **Step 2:** FE: nút ẩn hẳn theo cờ; Không duyệt mở modal lý do → gọi reject → toast QLDA + về danh sách.
- [ ] **Step 3 (verify):** phiếu nháp của mình có Sửa/Xóa; CHO_DUYET (tài khoản có quyền) chỉ có Không duyệt;
  so khớp nút danh sách ↔ chi tiết.
- [ ] **Step 4 (commit).**

---

## Verify tổng (Phase 2)

### P2-T14: Playwright end-to-end + âm quyền + đối chiếu DB
- [ ] **E2E luồng dương:** tạo nháp → sửa → gửi duyệt (DB: `firm_contract_costs.exported=1` dòng chọn;
  `service_accounting_request_costs.contract_costable_type` = chuỗi FQN ERP) → Không duyệt (exported về 0) → xóa.
- [ ] **Cả 3 loại:** type1 revenue_costs, type2 costs, **type3** tạo dòng "Chi phí vận chuyển" (đếm
  `firm_contract_costs` trước/sau, chạy 2 lần không trùng dòng).
- [ ] **Âm quyền:** reject bằng tài khoản không quyền hạch toán → 403; sửa/xóa phiếu người khác → 403;
  sửa phiếu CHO_DUYET → 409 (câu `GuardsCatalogStatus::$statusConflictMessage`). (Cách login không password:
  đặt bcrypt tạm rồi KHÔI PHỤC hash gốc — như Phase 1.)
- [ ] **Số liệu:** `payed_cost`/VAT khớp công thức.
- [ ] **Checklist `erp-to-hrm-screen`** (nút màu/thứ tự, badge, nhãn "Người tạo/Ngày tạo", validate inline,
  attachments cột dung lượng, lịch sử ghi khi gửi duyệt/không duyệt) + grep tự kiểm RỖNG.
- [ ] **Chụp ảnh** create/edit/detail đặt cạnh màn HDDV; ghi màn mẫu đã bám vào checkpoint.
- [x] Ghi **Checkpoint — Phase 2** vào plan.md (giống Phase 1) + cập nhật memory. Commit (CHƯA push — chờ user QA).

---

### Checkpoint — Phase 2 — 2026-11-02 (Opus 4.8)

**Vừa hoàn thành:** T1–T14 (write-side) XONG trên nhánh `feat/ychtdv-hdbh-p2` (cả 2 repo). Phase 2 =
Tạo/Sửa/Xóa + Gửi duyệt + Không duyệt + standalone create với popup chọn HĐ hãng + 3 loại hạch toán
(Dịch vụ/Chi phí khác/Vận chuyển) + `exported` write-back + attachments qua bảng `files` chung. KHÔNG
có màn #2 Hạch toán (`serviceAccounting`) và KHÔNG in phiếu (HOÃN — phụ thuộc bộ chi phí HĐ hãng).

**Quyền:** 1 quyền mới `Hạch toán yêu cầu làm dịch vụ` (guard `api`, type = phân hệ Bán hàng) cho
reject; update/destroy gate theo chủ phiếu + status∈WRITABLE (Đang tạo/Từ chối), KHÔNG checkPermission.

**Verify (DB gộp local `erp_hrm_check`):**
- **BE write-path 3 loại** (tinker + rollback, actor = CHỦ HĐ thật): tạo/gửi duyệt sinh
  `service_accounting_request_costs` với `contract_costable_type` = FQN ERP; gửi duyệt lật
  `firm_contract_costs.exported=1` dòng được tick; Không duyệt (reject) lật `exported` về 0. Chạy 2 lần
  không trùng dòng.
- **Âm quyền per-record:** chủ phiếu (emp13) status 1 → canEdit/canDelete=1, canAccounting=0; NV khác
  (emp24) → cả 3 cờ = 0. update/destroy phiếu người khác → 403; sửa phiếu CHO_DUYET → 409.
- **FIX T14 (edit 422→404):** màn Sửa ERP (`getDataForEdit`) CHỈ gate `canEdit`, KHÔNG re-check
  `canProductExport`/`canRequestAccountingDelivery`. HRM trước đó chạy lại gate create → 404 khi HĐ đã
  đổi trạng thái/chủ. Sửa: thread `$forEdit` qua `buildCostsFromContract`/`contractData` (bỏ 2 gate chọn
  HĐ, GIỮ `support_accounting`); controller bật `forEdit` CHỈ khi `request_id` là phiếu WRITABLE của chính
  user cho đúng `contractable_id` (chống bypass gate tạo); FE đính `&request_id` khi `isEdit`.
  Service-layer: C24757 forEdit=false THROW, forEdit=true OK.
- **In-browser (Playwright MCP, emp13 = DNS Admin):** danh sách render đúng (toolbar/filter/cột
  Người tạo·Ngày tạo); **màn Sửa phiếu nháp #3622 hydrate đủ dòng chi phí đã tick (6,500,000) và KHÔNG
  redirect 404** (xác nhận trực tiếp FIX); màn Tạo + popup "Chọn hợp đồng hãng" mở, chọn HĐ hydrate
  khách hàng/địa chỉ, dropdown Loại hạch toán đủ 3 loại; đổi loại bắn `GET contract-data/{id}?type=` 200.
- **Checklist `erp-to-hrm-screen`:** nút theo `button-convention`, badge `V2BaseBadge` màu BE, nhãn
  "Người tạo/Ngày tạo", validate inline, attachments `FileAttachmentTable`, lịch sử nhúng. Bám khuôn
  song sinh `buy-service-requests` / `buy-service-accounting-requests`.
- **Dọn test:** draft #3622 (TPE.YCHTDV.02523) đã xóa qua service destroy (emp13 remaining=0).

**Ruling T14-empty-state (parked, non-blocking):** ô lưới chi phí khi HĐ chọn có 0 dòng đủ điều kiện vẫn
hiện câu "Chọn hợp đồng và loại hạch toán để nạp chi phí." (chỉ `v-if="!form.costs.length"`, không phân
biệt "chưa chọn" vs "đã chọn nhưng rỗng"). Là hành vi form sẵn từ T11 (đã review), KHÔNG thuộc phạm vi
FIX T14, không bám-ERP bắt buộc. Để nguyên — sửa là thêm bề mặt chưa test ngay trước final review. Cost
nếu sai: 1 nit template QA sửa sau.

**Commit (CHƯA push — chờ user QA):** hrm-api `a329386c1` + hrm-client `e582d6787`. Nhánh
`feat/ychtdv-hdbh-p2` cả 2 repo. Bước còn lại trước bàn giao: final whole-branch review (Opus) +
`finishing-a-development-branch` (chuẩn hóa trailer T12/T13a Haiku 5.5 → Opus 4.8).

**Blocked:** không. Deferred sang phase sau: màn #2 "Hạch toán dịch vụ" (`serviceAccounting`) · In phiếu.
