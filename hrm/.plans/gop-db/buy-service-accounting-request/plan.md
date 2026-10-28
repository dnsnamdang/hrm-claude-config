# Yêu cầu hạch toán mua dịch vụ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.
> @khoipv · nhánh `develop` (con `gop_db`, KHÔNG tạo nhánh mới, KHÔNG commit — user tự commit)

**Goal:** Port màn ERP "Yêu cầu hạch toán mua dịch vụ" (2 loại) sang HRM `/finance/buy-service-accounting-requests`.

**Architecture:** BE ở `Modules/Finance` theo đúng khuôn màn Yêu cầu mua dịch vụ: Entity (cờ quyền + `searchByFilter`) →
Service (đọc/ghi/lịch sử/in/xuất) + NotifyService → Controller mỏng + FormRequest + ListResource. FE Nuxt 2 trang
`pages/finance/buy-service-accounting-requests` dùng V2Base + mixin chuẩn. Không migration; dùng nguyên 3 bảng ERP.

**Tech Stack:** PHP 7.4 / Laravel 8 / nwidart modules · Nuxt 2.14 / Vue 2 / Bootstrap-Vue · MySQL `gop_db`.

**Spec:** `docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-request-design.md` (đọc trước mọi task).

## Global Constraints
- Không migration, không ghi cột ERP ngoài danh sách spec §2. Không dùng `mysql2`.
- Quyền mới: id 1699-1702, guard `api`, `type 23`, group `Yêu cầu hạch toán mua dịch vụ` — chỉ sửa `PermissionsTableSeeder`.
- Kiểm quyền bằng trait `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (khuôn `BuyServiceRequest`).
- Toast/thông báo câu chuẩn QLDA kết thúc bằng dấu chấm; 409 "Trạng thái đã bị thay đổi. Vui lòng load lại trang".
- Nhãn "Người tạo / Ngày tạo" (cấm "Người lập / Ngày lập"). Ngày BE trả `d/m/Y H:i`. Số `1,234,567.89`. Ô rỗng để trống.
- Select trong modal dùng `V2BaseSelectInModal`. Cờ quyền FE mặc định `false`, chỉ lấy từ BE.
- Skill bắt buộc đọc khi tới phần tương ứng: `erp-to-hrm-screen`, `list-page`, `button-convention`, `modal-popup`,
  `form-validate`, `unsaved-changes`, `entity-history`, `export-excel`, `print-page`, `notification-convention`.
- Không tự test Playwright: verify BE bằng HTTP kernel trong tinker, FE bằng compile; user tự bấm trình duyệt.

## Review Focus
1. SL hạch toán vượt phần còn lại do phiếu khác vừa giữ (2 người lập song song) → BE 422 đúng dòng, không ghi.
2. Người không phải người tạo gọi PUT/DELETE trực tiếp → 403; phiếu đã sang Chờ duyệt → 409.
3. Kế toán khác công ty mở `?type=for-approve` → không thấy phiếu công ty khác, không có nút Hạch toán.
4. Phiếu loại 1 lưu với đơn bảo hiểm thiếu phụ lục / thiếu số → không ghi `''` vào cột số NOT NULL (500).
5. Sửa phiếu Không duyệt: SL HĐ còn lại phải trừ đi phiếu khác nhưng KHÔNG trừ chính phiếu đang sửa.

---

## Phase 0 — Khảo sát + chốt design
- [x] Khảo sát ERP + HRM + DB gộp (12/10)
- [x] Chốt điểm mở với user (2 loại, 3 cấp, xoá như ERP, Bán hàng chính)
- [x] Fill spec + design.md

## Phase 1 — BE nền: quyền + Entity

### Task 1: Quyền + 3 Entity + morph
**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sau dòng id 1698)
- Create: `hrm-api/Modules/Finance/Entities/BuyServiceAccountingRequest/BuyServiceAccountingRequest.php`
- Create: `…/BuyServiceAccountingRequest/BuyServiceAccountingRequestDetail.php`
- Create: `…/BuyServiceAccountingRequest/BuyServiceAccountingRequestDetailRequest.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/BuyServiceContractDetailRequest.php` (chỉ đọc, bảng `buy_service_contract_detail_requests`) nếu chưa có
- Create: `hrm-api/Modules/Finance/Entities/Insurance/InsurancePrincipleForm.php`, `InsurancePrincipleAdditional.php` (ghi được status/type), `InsurancePrincipleContract.php` (chỉ đọc)

**Interfaces — Produces:**
- `BuyServiceAccountingRequest` consts: `DANG_TAO=1, CHO_DUYET=2, DANG_HACH_TOAN=3, DA_HACH_TOAN=4, KHONG_DUYET=5`,
  `TYPE_INSURANCE=1, TYPE_SERVICE=2`, `STATUSES`, `TYPES`, `HAS_VAT_OPTIONS`, `SORTABLE_COLUMNS`,
  `PERMISSION_VIEW_ALL_COMPANY|VIEW_COMPANY|VIEW_DEPARTMENT|ACCOUNTING`.
- Quan hệ: `details()`, `company()`, `department()`, `employee_create()`, `approver()`, `supplier()` (Supplier = customers is_supplier),
  `buyServiceContract()`; Detail: `requests()`, `cost()`; DetailRequest: `buyServiceRequest()`, `contractDetailRequest()`.
- Hàm: `generateCode(): void` (`.YCHTMDV.`), `statusMeta(): array`, `typeName(): string`, `attachmentList(): array`,
  `isEditableStatus()`, `isWaitingAccounting()`, `canView()`, `canEdit()`, `canDelete()`, `canAccounting()`,
  `static isBigBoss()/isBoss()/isManager()/hasAccountingPermission()`, `static searchByFilter($request)`,
  `totalPayment(): float` (type 1 → total_after_tax, type 2 → summary.amount_after_vat).

- [x] **Step 1:** Thêm 4 dòng `Permission::create([...'id' => 1699..1702, 'type' => 23, 'group' => 'Yêu cầu hạch toán mua dịch vụ'])`
  (copy format dòng 1695). Chạy riêng 4 dòng bằng tinker `Permission::firstOrCreate` (KHÔNG chạy cả seeder — trùng id 1117/1118).
- [x] **Step 2:** Viết Entity chính: copy khuôn `BuyServiceRequest.php` (trait, STATUSES có `type/color`, `$casts summary => array`,
  `applyAllScope`, `applyFilters`, `applySort`). Khác biệt:
  - `canView()` theo spec §4 (thêm vế status=2 + quyền Hạch toán + cùng công ty).
  - `canAccounting()`: `status == CHO_DUYET && sameCompanyAsCurrent(company_id) && (superAdmin || quyền Hạch toán)`.
  - `searchByFilter` 3 preset: `all` / `for-approve` (status 2 + company, không quyền → `1=0`) / mặc định của tôi.
  - `applyFilters`: `keyword` (code | buy_service_contract_code | supplier_name | whereHas details.cost_name), `code`,
    `buy_service_contract_code`, `cost_name`, `supplier`, `approver_id`, `status`, `request_type` (cột `type`), `company_id`
    (chỉ khi isBigBoss), `department_id`, `start_date`, `end_date` (whereDate).
  - `SORTABLE_COLUMNS`: `code, createdAt→created_at, approvedTime→approved_time, status`.
- [x] **Step 3:** Detail / DetailRequest / Contract / Insurance entity (`$table` tường minh, `$guarded = []`).
- [x] **Step 4: Verify** tinker:
  `auth()->loginUsingId(<id super admin>); echo BuyServiceAccountingRequest::searchByFilter(new Request(['type'=>'all']))->count();` → 51.
  `->first()->totalPayment()` > 0; `canView()` true.

## Phase 2 — BE nghiệp vụ

### Task 2: Service đọc + nguồn form
**Files:** Create `hrm-api/Modules/Finance/Services/BuyServiceAccountingRequestService.php`,
`hrm-api/Modules/Finance/Transformers/BuyServiceAccountingRequestResource/BuyServiceAccountingRequestListResource.php`

**Produces:**
- `searchByFilter(Request): LengthAwarePaginator`, `meta(): array` (`is_big_boss,is_boss,is_manager,is_all_company,is_accountant,statuses,types,has_vat_options`)
- `findOrFail(int)`, `findForShow(int)`, `detailData(BuyServiceAccountingRequest): array` (đủ cột spec §2 + cờ `is_can_edit/delete/accounting`
  + `erp_accounting_url`, `details[]` mỗi dòng có `requests[]` kèm `available_qty`, `buy_service_request_code`, `request_creator`)
- `availableQty(array $contractDetailRequestIds, ?int $excludeRequestId): array<int,float>` — **hàm duy nhất** tính SL còn lại:
  ```php
  $used = DB::table('buy_service_accounting_request_detail_requests as r')
      ->join('buy_service_accounting_requests as h', 'h.id', '=', 'r.buy_service_accounting_request_id')
      ->whereIn('r.buy_service_contract_detail_request_id', $ids)
      ->whereIn('h.status', [1, 2, 3])
      ->when($excludeRequestId, fn ($q) => $q->where('h.id', '!=', $excludeRequestId))
      ->groupBy('r.buy_service_contract_detail_request_id')
      ->pluck(DB::raw('SUM(r.qty)'), 'r.buy_service_contract_detail_request_id');
  // available = cdr.qty - cdr.accounted_qty - used (cột qty/accounted_qty ép float — bảng HĐ lưu varchar)
  ```
- `contractOptions(Request)` (HĐ status 3, keyword theo code, paginate, sort code/created_at),
  `contractData(int $contractId, ?int $excludeRequestId): array` (port `getDataForAccountingRequest`),
  `insuranceFormOptions(Request)`, `insuranceFormData(int $formId): array` (port `getDataForPrincipleForm`),
  `searchSuppliers(Request)` (copy `BuyServiceRequestService::searchSuppliers`).
- [x] Steps: viết → tinker gọi `contractData(<id HĐ có phiếu>, null)` so `available_qty` với tính tay SQL; `detailData` phiếu 4 trả `is_can_edit=false`.

### Task 3: Service ghi + NotifyService + lịch sử
**Files:** Modify Service Task 2; Create `hrm-api/Modules/Finance/Services/BuyServiceAccountingRequestNotifyService.php`;
Modify `hrm-api/app/Services/CatalogHistoryService.php` (`TABLES['buy_service_accounting_requests']`).

**Produces:** `store(array): Model`, `update(Model, array): Model`, `reject(Model, string): Model`, `destroy(Model): void`,
`deleteFile(Model, string): Model`; Notify: `onSentToAccountant(Model)`, `onRejected(Model, string)`.
- Ghi loại 2 (trong `DB::transaction`): `lockForUpdate` các `buy_service_contract_detail_requests` theo id gửi lên →
  `availableQty(ids, $object?->id)` → dòng nào `qty > available` thì `throw ValidationException::withMessages(["details.$i.requests.$j.qty" => "SL hạch toán vượt số lượng còn lại ({$available})."])`.
  Giá lấy từ `buy_service_contract_details` theo cost_id của HĐ; `cost_name` từ `costs`; summary BE tính.
- Ghi loại 1: copy field theo spec §6, số rỗng → 0, code rỗng → null; tính total_before/after_tax; status 2 → cập nhật form/additional `status=type=3`.
- `has_vat=2` → `vat_percent=0`. `packAttachments`. Mã sinh sau insert. `company/department/part` từ `auth()->user()->info`.
- Lịch sử: khuôn `snapshotOf` + `logUpdateWithRows` + `logStatusChange` của `BuyServiceRequestService`; `details_rows` khóa
  `cost_id|buy_service_request_detail_id`, trường: Dịch vụ, Yêu cầu, SL hạch toán, Đơn giá, Thành tiền.
- destroy: log delete → xoá detail_requests (theo `buy_service_accounting_request_id`) + details + phiếu.
- Notify: khuôn `BuyServiceRequestNotifyService`; người nhận = `employeeInfoIdsHavingPermission('Hạch toán mua dịch vụ', company_id)`.
- [x] Verify ở Task 5.

### Task 4: FormRequest + Controller + Route + Export registry + print
**Files:** Create `hrm-api/Modules/Finance/Http/Requests/BuyServiceAccountingRequest/BuyServiceAccountingRequestStoreRequest.php`,
`…/BuyServiceAccountingRequestRejectRequest.php`, `hrm-api/Modules/Finance/Http/Controllers/V1/BuyServiceAccountingRequestController.php`;
Modify `hrm-api/Modules/Finance/Routes/api.php` (sau khối buy-service-requests dòng ~1261),
`hrm-api/app/ExcelExport/ExportColumnRegistry.php`, `hrm-api/Modules/Finance/Entities/ErpReportTemplate.php` (hằng 428/429).
- StoreRequest: rule rẽ theo `$this->input('type')` / `$this->input('status')` (KHÔNG `$this->get()` — bẫy JSON body);
  loại 2: `buy_service_contract_id required|integer`, `supplier_id required|integer`, `has_vat required|in:1,2`, `vat_percent nullable|numeric|min:0|max:100`,
  `details required|array|min:1`, `details.*.cost_id required|integer`, `details.*.requests required|array|min:1`,
  `details.*.requests.*.buy_service_contract_detail_request_id required|integer`, `….buy_service_request_id required|integer`,
  `….buy_service_request_detail_id required|integer`, `….qty required|numeric|min:0`;
  loại 1: `insurance_principle_form_id required|integer`, `insurance_principle_form_code required`, `buy_contract2_code required`, `has_vat required|in:1,2`;
  chung: `type required|in:1,2`, `status required|in:1,2`, `note nullable|string|max:1000`, `attachment_urls array`,
  `attachment_urls.*` `starts_with:<URL prefix S3>buy_service_accounting_requests`; `attachment_urls required_if:has_vat,1` khi phiếu chưa có file.
- Controller: khuôn `BuyServiceRequestController` (409 trước 403). reject: `isWaitingAccounting()` else 409, `canAccounting()` else 403.
- Route: tĩnh trước `/{id}`; reject gắn `->middleware('checkPermission:Hạch toán mua dịch vụ')`.
- Export: key `buy_service_accounting_requests` 11 cột (STT always, Số phiếu, Loại yêu cầu, Số hợp đồng, Nhà cung cấp,
  Tổng thanh toán (số), Ngày tạo, Người tạo, Ngày duyệt, Người duyệt, Trạng thái).
- print-data: mẫu 429, placeholder SO_PHIEU, HEADER (công ty trên phiếu), NGAY_LAP, LOAI_YEU_CAU, HOA_DON_VAT, ROW_1..4, CHI_TIET
  (bảng loại 2 rowspan đúng — ô STT cũng rowspan); print-list-data mẫu 428 + `LimitsPrintListRows`.

### Task 5: Smoke test BE (HTTP kernel trong tinker, auth TpEmployee)
- [x] GET list 3 preset với super admin → 51 / 2 / phiếu của tôi.
- [x] GET show phiếu có thật → 200, `details[].requests[].available_qty` có.
- [x] POST loại 2 nháp với HĐ còn SL → 200, có `code` `.YCHTMDV.`; PUT gửi duyệt → status 2, có notification.
- [x] POST vượt SL → 422 đúng key.
- [x] User thường (không quyền, không phải người tạo) PUT/DELETE → 403; reject khi status 1 → 409.
- [x] POST reject thiếu comment → 422; có comment → status 5.
- [x] DELETE phiếu test → sạch cả 3 bảng. Xoá notification + catalog_histories test. Đếm lại 51/64/67.
- [x] export → file tải được; print-data / print-list-data trả HTML.

## Phase 3 — FE
Đọc skill `erp-to-hrm-screen` (checklist A–H), `list-page`, `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`, `entity-history`, `print-page` trước khi code.

### Task 6: Màn danh sách
**Files:** Create `hrm-client/pages/finance/buy-service-accounting-requests/index.vue` (copy khuôn `pages/finance/buy-service-requests/index.vue`).
- `columnScreenKey`/`localStorageKey`/`table` = `buy_service_accounting_requests`. Đọc `$route.query.type` (all/for-approve/mặc định).
- Cột/lọc/hành động theo spec §7. Hạch toán → `window.open(erpUrl(...))` qua `utils/erp-link.js`. Số HĐ: loại 2 → ERP
  `/admin/orders/buy-service-contract/{id}/show`, loại 1 → ERP route `insurance.principleContract.show` (tra URL trong ERP web.php).
- Xuất (`ExportFieldsModal`), In danh sách (`ReportPrintPreviewModal`), Lịch sử (`CustomerHistoryModal` khuôn màn mua DV).

### Task 7: Form + bảng chi tiết + 2 popup chọn
**Files:** Create `components/BuyServiceAccountingRequestForm.vue`, `components/ServiceDetailTable.vue`, `components/InsuranceSection.vue`,
`components/BuyServiceContractPickerModal.vue`, `components/InsuranceFormPickerModal.vue` (dùng `utils/pickerPagination.js`, sort mã/ngày tạo).
- Form theo spec §7: CreatorInfoLine, Loại (khoá khi sửa), validate inline + `touched`, `unsavedChangesMixin`, `saveAndContinueMixin`,
  AttachmentSection (`api-base`), nút Lưu nháp / Lưu và gửi duyệt (khoá `submitting`). SL hạch toán: `utils/number-input.js`, vượt → đỏ.
  Đổi has_vat=1 → VAT% = VAT HĐ; =2 → 0. Tổng tính FE chỉ để hiển thị.

### Task 8: Trang Thêm / Sửa / Chi tiết + menu
**Files:** Create `create.vue`, `_id/edit.vue`, `_id/index.vue` (khuôn `buy-service-requests`); Modify
`hrm-client/components/subsystem-menu/sale-hub.js` (dòng 213 + nhóm Phê Duyệt), `hrm-client/components/subsystem-menu/finance.js` (dòng ~310).
- Chi tiết: footer In · Hạch toán (ERP) · Không duyệt (`CommentModal`) · Sửa · Xoá · Quay lại theo cờ BE; Lịch sử `SystemInfoSection`; 404 → `/pages/extras/404`.
- Sửa: không `canEdit` → về chi tiết.

### Task 9: Verify FE
- [x] Compile các file `.vue` mới (vue-template-compiler + babel parse) — 0 lỗi.
- [x] Chạy grep checklist cuối skill `erp-to-hrm-screen` trên thư mục feature — sạch.
- [ ] Báo user các bước cần bấm thử trên trình duyệt. (chờ user)

## Phase 4 — Wrap up
- [ ] Cập nhật plan checkpoint + STATUS gop-db.

## Tiến độ thực tế (12/10/2026)

- [x] Task 1-5 BE: 4 quyền 1699-1702 (đã insert DB local), 3 entity + 3 entity phụ, Service/Notify/Controller/FormRequest/Resource,
  14 route, xuất Excel (ExportColumnRegistry), in 428/429, lịch sử catalog_histories.
  Smoke test HTTP kernel: exceed 422 · giữ chéo 2 phiếu 422 · HĐ người khác 422 · VAT thiếu file 422 · URL lạ 422 ·
  người khác PUT/DELETE/xem nháp 403 · không quyền reject 403 · reject rỗng 422 · reject → 5 · reject lại 409 ·
  sửa phiếu 5 (khoá loại) · xoá sạch 3 bảng · lịch sử 7 mốc · export số là ô số. Dọn sạch: 51/64/67, gỡ quyền gán tạm.
- [x] Task 6-8 FE: index / create / _id/edit / _id/index + Form, ServiceDetailTable, InsuranceSection, SourcePickerModal; menu
  Bán hàng › Mua dịch vụ (`?type=all`), Bán hàng › Phê Duyệt › Mua dịch vụ (`?type=for-approve`, isShow quyền Hạch toán),
  Tài chính › Mua dịch vụ (`?type=all`).
- [x] Task 9: compile 8/8 file vue + 2 file menu; grep checklist sạch.
- [x] Final review (reviewer độc lập) + fix pass: race SL song song (đọc có khoá + thông báo sau commit), trùng id dòng
  trong payload, IDOR `contracts/{id}` + `exclude_id`, XSS bản in (htmlspecialchars), phụ lục bảo hiểm mất khi sửa
  (quan hệ không lọc type), đơn bảo hiểm phải type 2, Không duyệt khoá + kiểm lại (409), SL còn lại không âm,
  log xoá trong transaction. Test 2 tiến trình: phiếu thứ 2 chờ khoá rồi 422. Regression pass, dữ liệu sạch.
  Để lại (minor): thứ tự 409/403 với người không phải chủ phiếu; letterhead chưa ghép ERP_URL cho path tương đối;
  đổi đơn bảo hiểm khi sửa thì đơn cũ kẹt "Đang hạch toán" (ERP cũng vậy).
- [x] Fix (user báo 12/10): popup HĐ mua DV ở HRM ra 72 HĐ, ERP ra 0 → bỏ ngoại lệ Super admin ở
  `contractOptions()` + `canUseContract()`. Modal ERP gọi `searchData` không truyền `type` → nhánh
  `created_by = mình`, KHÔNG xét quyền (Super admin cũng vậy). Verify: SA id 13 → 0, user 214 → 15.
- [x] UI loại "Công nợ bảo hiểm" (user yêu cầu 12/10): Số đơn / Phụ lục / Số HĐ mua lên khối Thông tin chung
  (chi tiết: Phụ lục + HĐ mua là link ERP); khối "Thông tin công ty bảo hiểm" đổi nhãn + thứ tự đúng ERP; tách
  khối "Thông tin người liên hệ" + "Thông tin người đại diện" xếp xuống dưới khối công ty (user chốt, khác ERP để bên phải).
- [x] Dữ liệu mẫu loại bảo hiểm (user đồng ý 12/10 — local gop_db, mọi DB local đều 0 dòng bảo hiểm):
  `insurance_principle_forms` id 1 (TEST-DBH-001, không phụ lục), id 2 (TEST-DBH-002) + `insurance_principle_additionals`
  id 1 (TEST-PLBS-002, gắn đơn 2). Đều status 2 / type 2, mã + note bắt đầu `TEST-`.
- [x] Bỏ màn chờ duyệt (user chốt 12/10: "sau này sẽ bỏ màn chờ duyệt"): xoá nhánh `for-approve` (BE
  `searchByFilter`, FE `listType`, menu Bán hàng › Phê Duyệt › Mua dịch vụ). Màn `?type=all` kiêm duyệt: người có
  quyền "Hạch toán mua dịch vụ" thấy thêm phiếu Chờ duyệt cùng công ty (SA: mọi công ty) + phiếu `approver_id` = mình.
  Không duyệt nay ghi `approver_id` + `approved_time` (ERP chỉ ghi lúc hạch toán) để phiếu mình từ chối vẫn hiện.
  Test (transaction rollback): không quyền → không thấy; có quyền → thấy phiếu chờ duyệt, không thấy nháp người khác;
  từ chối xong vẫn thấy; người tạo + SA đúng.
- [ ] DỌN dữ liệu mẫu khi user test xong: xoá 2 bảng trên `where code like 'TEST-%'` + phiếu YCHTMDV loại 1 tạo từ
  các đơn đó (kèm detail / catalog_histories / notifications của phiếu).
- [ ] User bấm thử trình duyệt.

## Redmine #11699 (15/10/2026) — danh sách
- [x] 1. Ô lọc Nhà cung cấp (V2BaseSelectRemote, endpoint `/suppliers` của màn) trong bộ lọc nâng cao; bỏ NCC khỏi ô tìm nhanh (BE `keyword` + placeholder).
- [x] 2. Ẩn cột Công ty / Phòng ban (bỏ khỏi `allColumns`); thêm cột Người cập nhật / Ngày cập nhật (sort được Ngày cập nhật).
  BE: migration thêm `updated_by` (nullable) vào bảng ERP + hook `saving` ghi `auth()->id()`; resource + Excel thêm 2 cột.
- [x] 3. Sort cột Tổng thanh toán — BE `orderByRaw` theo đúng `totalPayment()` (loại 1 `total_after_tax`, loại 2 `summary.amount_after_vat`).
- [x] 4. Verify: migrate local, smoke API (lọc NCC, sort 3 kiểu, updated_by ghi khi sửa), compile FE.
  Kết quả: migrate local OK · sort totalPayment asc 2.7tr→… / desc 754tr→… · lọc supplier_id=38214 → 1 phiếu đúng NCC ·
  `/suppliers?keyword=KDO` 200 · hook ghi updated_by=13 (transaction rollback, DB sạch) · Excel 2 cột mới 200 · compile FE 0 lỗi.
  Chưa mở trình duyệt (chờ user). Deploy: chạy migration `2026_10_15_000002_*`. Phiếu cũ: Người cập nhật trống;
  cổng ERP sửa phiếu không ghi `updated_by`.

### Checkpoint — 2026-10-12
Vừa hoàn thành: bỏ ngoại lệ Super admin ở popup HĐ mua DV (khớp ERP).
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt kiểm; gán 4 quyền mới cho vai trò; chạy 4 dòng seeder 1699-1702 trên dev/prod.
Blocked:

- [x] 5. (user hỏi 15/10 "Người cập nhật trống") Điền `updated_by` cho 52 phiếu cũ — migration `2026_10_15_000003_backfill_*`
  (user chốt): Đã hạch toán → `approver_id` (48, updated_at trùng date_accounting); còn lại → `created_by` (4). Không chạm `updated_at`.

## Redmine #11701 (15/10/2026) — bản in
- [x] 1. In danh sách thiếu Ngày duyệt: 48/48 phiếu Đã hạch toán làm từ ERP có `approved_time` NULL (ERP không ghi). Lấy dự phòng
  `date_accounting` của phiếu Hạch toán đã duyệt — áp cho cả cột màn danh sách, chi tiết, Excel, bản in, sort Ngày duyệt. Không sửa dữ liệu.
- [x] 2. In chi tiết: thu cột SL hạch toán (10% → 7%), nới cột Yêu cầu (22% → 25%).
  - [x] 2b. (user báo 15/10 vẫn rộng) Độ rộng đặt ở hàng tiêu đề 2 bị `table-layout: fixed` bỏ qua (chỉ đọc hàng đầu, ô "Chi tiết"
    gộp 2 cột → chia đều 16/16) → thêm `<colgroup>` 8 cột 5/22/6/8/12/12/25/10; tiêu đề "SL hạch toán" `nowrap` 1 dòng (user yêu cầu).
- [x] 3. In chi tiết: mã HĐ / số đơn liền một khối tràn ra ngoài lề → bọc giá trị ROW_1..4 bằng `overflow-wrap: anywhere`.
  - [x] 3b. (user báo 15/10 vẫn tràn viền) Gốc thật: mẫu 429 khai ô bằng px (402 + 375 = 777px, ô ký 765px) trong bảng
    `table-layout:fixed` → bảng nở theo tổng px, vượt khổ giấy. `fitTemplateWidths()` đổi px → % theo tổng từng hàng TRƯỚC
    `fillReport` (không sửa mẫu ERP). Verify: 0 px còn lại, 51.74/48.26 · 21.31/23.4/27.06/28.24.
- [x] 4. Số tiền in giữ thập phân (tối đa 2 số lẻ, khớp màn hình) thay cho `formatCurrency` làm tròn — cả bản in chi tiết và danh sách.
- [x] 5. Verify (API, chưa mở trình duyệt): in danh sách 0/48 phiếu Đã hạch toán trống Ngày duyệt · sort Ngày duyệt desc/asc đúng
  (phiếu chưa duyệt xếp cuối/đầu) · in chi tiết 52: cột 25% / 7%, mã HĐ bọc `overflow-wrap` · `moneyText(248011085.3)` = `248,011,085.3` ·
  màn chi tiết 52 Ngày duyệt 16/07/2026 15:30 · log BE không lỗi mới. DB local không có phiếu nào có số lẻ để in thật.

### Checkpoint — 2026-10-15
Vừa hoàn thành: Redmine #11699 (ô lọc NCC, ẩn Công ty/Phòng ban, cột Người/Ngày cập nhật, sort Tổng thanh toán)
  + #11701 (bản in: Ngày duyệt dự phòng date_accounting, cột Yêu cầu/SL hạch toán, chống tràn mã HĐ, số tiền giữ số lẻ).
Đang làm dở: không.
Bước tiếp theo: user bấm thử trình duyệt; chạy 2 migration `2026_10_15_000002_add_updated_by_*` + `2026_10_15_000003_backfill_updated_by_*` trên dev/prod.
Blocked:

## Redmine #11703 (15/10/2026) — form Tạo mới
- [x] 1. Lưu nháp chỉ bắt Loại yêu cầu (FE `validate()` + BE FormRequest `isDraft()`); gửi duyệt vẫn bắt đủ.
  `fillHeader` nhận nháp trống HĐ / NCC / đơn bảo hiểm / VAT → cột NOT NULL ghi 0 / ''; `detailData` trả null cho 0.
  SL hạch toán vượt còn lại / VAT ngoài 0-100 vẫn chặn cả khi nháp (giữ SL hợp đồng).
- [x] 2 + 5. Đổi loại đơ 3s / mở dropdown NCC đơ 8s: ô NCC nạp ~9.500 dòng vào select2 → `V2BaseSelectRemote`
  (tìm theo từ khoá, dropdown hiện "Đang tìm..."); BE `searchSuppliers()` `limit(50)` (ô lọc NCC màn danh sách dùng chung, vẫn chạy).
- [x] 3. Popup chọn nguồn: nút × xoá nhanh trong ô lọc khi có chữ (khuôn BillAdjustDeptRequestPickerModal), bấm × tìm lại luôn.
- [x] 4. Popup đơn bảo hiểm: sort Số phụ lục (subquery bảng phụ lục) + Số hợp đồng mua; popup giãn sang phải
  (mép trái giữ chỗ modal-xl, không đè menu trái; rộng tối đa 1240px — user báo 1360px to quá); nút Tìm kiếm / Làm mới `nowrap` 1 hàng — áp cho cả popup HĐ mua DV.
- [x] 6. Bảng Danh sách dịch vụ: th/td `vertical-align: middle`.
- [x] 7. Test Playwright (user yêu cầu): đổi loại 34ms · dropdown NCC 50 dòng mở ngay, gõ "hồng hải" lọc đúng · gửi duyệt
  báo đỏ HĐ + VAT · Lưu nháp loại 2 (chỉ NCC) + loại 1 (trống đơn) OK, màn Sửa nạp lại đúng nhãn NCC · popup: × xoá chữ,
  2 nút 1 hàng, sort gửi `sort_by=additional_code|buy_contract2_code` 200 · danh sách hiện 2 phiếu nháp.
  Đã xoá phiếu test id 73, 74 + catalog_histories 980, 981.

### Checkpoint — 2026-10-15
Vừa hoàn thành: Redmine #11703 (6 mục) + test Playwright.
Đang làm dở: không.
Bước tiếp theo: user kiểm lại trên dev; deploy BE + FE cùng lúc (FE gọi NCC theo keyword).
Blocked:

## Redmine #11704 (15/10/2026) — Tạo mới loại Dịch vụ thuê ngoài
- [x] 1. Popup chọn HĐ mua DV: Số hợp đồng là link cổng ERP (tab mới, HĐ chưa port); bấm link KHÔNG chọn dòng
  (prop `codeLink` của SourcePickerModal, `onTableClick` bỏ qua thẻ `a`).
- [x] 2. Chọn HĐ lần đầu chậm: API `contracts/{id}` ~97ms (tinker, HĐ 71, 7 dòng); phía FE sau khi có dữ liệu ~35ms — chỗ đơ
  cũ là ô NCC 9.500 dòng nhận giá trị (đã gỡ ở #11703). Thêm `$safeLoadingStart/Finish` lúc chờ nạp HĐ. Local mọi API ~3s (môi trường).
- [x] 3. Upload docx hợp lệ bị từ chối: docx sinh bằng công cụ bị finfo đoán `application/octet-stream` → trượt `mimes:docx`.
  Đổi sang so ĐUÔI file (khuôn DeliveryRequestController) ở `uploadFiles` của cả YC hạch toán + Hạch toán mua DV.
- [x] 4 + 7. Lưu xong dùng `router.replace` (nhánh lưu thường; "Lưu và tiếp tục" giữ nguyên) ở form YC hạch toán + form Hạch toán →
  nút Back không quay lại form vừa lưu. Không tái hiện được "Lưu nháp về màn Tạo" bằng code — đoán tester bấm Back sau khi lưu.
- [ ] 5. File >20MB: FE ĐÃ chặn + hiện chữ đỏ trong khối đính kèm ("File … vượt quá 20MB"), chỉ thiếu toast. Muốn thêm toast phải
  sửa `AttachmentSection.vue` (component chung nhóm Tài chính) → CHỜ user xác nhận. BE thêm câu `.uploaded` / `.max` tiếng Việt.
- [x] 6. Icon Hạch toán `ri-calculator-line` (danh sách + chi tiết); thêm "Không duyệt" ở cột Hành động danh sách (cùng CommentModal + API reject).
- [x] 8. Câu lỗi SL hạch toán rút gọn: "Không được vượt SL còn lại" (user chốt, không kèm số) / "Không được âm" (FE + BE).
- [x] 9. Test Playwright: link HĐ → `qttt.tanphat.com/admin/orders/buy-service-contract/74/show` tab mới, popup không đóng · chọn HĐ 71
  nạp 7 dòng · lỗi SL 1 dòng · upload đúng file docx của tester OK · file 21MB báo đỏ · Lưu nháp → danh sách, Back vẫn ở danh sách ·
  phiếu Chờ duyệt 45 hiện icon máy tính + nút Không duyệt, popup đúng mã (bấm Hủy). Dùng tạm token user 428 (người tạo HĐ 71), đã trả lại
  token DNS Admin; xoá phiếu test 75 + catalog_histories 982. CHƯA test lưu thật phiếu Hạch toán (tránh đổi trạng thái phiếu thật).

### Checkpoint — 2026-10-15
Vừa hoàn thành: Redmine #11704 (7/8 mục) + test Playwright.
Đang làm dở: mục 5 — chờ user đồng ý thêm toast vào AttachmentSection.vue (component chung).
Bước tiếp theo: user trả lời mục 5; deploy BE + FE.
Blocked: mục 5 cần xác nhận sửa component chung.

## Redmine #11706 (15/10/2026) — Lịch sử
- [x] 1. File đính kèm: khoá ảo `attachments_count` (chỉ ra SỐ file) → `attachment_rows` dạng BẢNG giữ NGUYÊN URL
  (khuôn DeliveryRequestWriteService) → timeline in "File đính kèm thêm mới / đã xóa", tên file bấm mở FilePreviewModal.
  CatalogHistoryService TABLES: thêm nhãn `attachment_rows`, GIỮ `attachments_count` cho log cũ.
- [x] 2. NCC: snapshot ghi "mã - tên" (mã lấy từ quan hệ `supplier`, dự phòng cột `supplier_code`) — trước chỉ có tên.
  Log cũ đã đóng dấu giữ nguyên (không sửa dữ liệu).
- [x] 3. Verify: tinker rollback (log + API catalog-histories 200, added_rows/removed_rows đúng) · Playwright: tạo nháp (NCC KDO + 1 pdf)
  → sửa (NCC Hồng Hải + thêm 1 ảnh) → khối Lịch sử màn chi tiết: "KDO - … → 65TPHPPH-31 - HỒNG HẢI", "File đính kèm thêm mới: anh-test…png",
  bấm tên file mở popup xem trước. Đã xoá phiếu 78 + catalog_histories 986, 987 (2 file test còn trên S3 thư mục buy_service_accounting_requests).
- Ghi chú: màn Hạch toán mua DV (`buy_service_accountings`) đang log `attachments_list` = chuỗi TÊN file (không bấm được) — chưa đụng, chờ user.

## Redmine #11710 (15/10/2026) — Tạo mới loại Công nợ bảo hiểm
- [x] 1. Popup đơn bảo hiểm: Số đơn → link ERP `/admin/insurance/form-insurance/{id}/show`, Số HĐ mua → `/admin/orders/buy_contract2/{id}/show`
  (BE trả thêm `buy_contract2_id`; SourcePickerModal: cột phụ nhận `link: (row) => url`). Nút 1 dòng + sort Phụ lục / HĐ mua đã làm ở #11703.
- [x] 2. Không duyệt xong lập lại / sửa phiếu không thấy đơn: ERP `reject()` không trả đơn về (kẹt type 3 "Đang hạch toán").
  · `reject()` gọi `releaseInsuranceForm()` — đơn + phụ lục type 3 → 2 (chiều ngược `afterSentForApproval`).
  · Dữ liệu CŨ không sửa: popup + `fillHeader` coi đơn type 3 là chọn được khi KHÔNG còn phiếu loại 1 nào giữ
    (Chờ duyệt / Đang HT / Đã HT — `insuranceHoldersQuery()`); phụ lục nhận cả type 3.
- [x] 3. Mất Tỉnh/TP: ERP làm rơi tỉnh khi lập đơn từ YC bảo hiểm. `insuranceProvinceId()` lấy dự phòng Phụ lục → Đơn → YC bảo hiểm →
  HĐNT; màn chi tiết phiếu cũ (đã lưu tỉnh trống) cũng hiện dự phòng — chỉ hiển thị, không ghi DB.
- [x] 4. Verify: tinker rollback — gửi duyệt ẩn đơn / Không duyệt hiện lại / đơn kẹt type 3 chọn lại được / phiếu thứ 2 bị chặn khi đơn đang
  bị giữ; tỉnh dự phòng lấy đúng từ YC (Hà Nội) và HĐNT (Đà Nẵng), chi tiết phiếu 67 hiện tỉnh. Playwright: 2 link đúng URL, bấm link không
  chọn dòng, nút 32px 1 dòng, chọn đơn → Tỉnh/TP có giá trị. (Tạm gán `buy_contract2_id`=999 cho đơn mẫu TEST-DBH-001 để test link, đã trả về null.)
  Local không có HĐNT / YC bảo hiểm thật — chưa thử với đơn 111 của dev.
