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

### Checkpoint — 2026-10-12
Vừa hoàn thành: bỏ ngoại lệ Super admin ở popup HĐ mua DV (khớp ERP).
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt kiểm; gán 4 quyền mới cho vai trò; chạy 4 dòng seeder 1699-1702 trên dev/prod.
Blocked:
