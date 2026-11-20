# YC đặt hàng mua ngoài (port ERP → HRM, phía KD) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** KD lập / sửa / lưu nháp / gửi duyệt / xoá nháp phiếu YC đặt hàng mua ngoài trên HRM, theo dõi mọi trạng thái; ERP chỉ còn các khâu từ TP duyệt trở đi.

**Architecture:** hrm-api module `Sale` đọc/ghi thẳng 5 bảng ERP `inland_order_request*` (DB chung), logic chép 1:1 `InlandOrderRequestsController` + model ERP. hrm-client thêm 4 trang `pages/sale/inland-order-requests`. ERP chặn ghi bằng `productMovedToHrm` và đổi thông báo về người lập sang chuông HRM (ERP ghi thẳng dòng `notifications` dạng HRM — không cần JWT).

**Tech Stack:** hrm-api Laravel (nwidart modules, JWT `auth:api`, PHPUnit `DatabaseTransactions` trên DB chung) · hrm-client Nuxt 2 + bộ component `V2Base*` · ERP Laravel 6 (Blade + AngularJS 1.3.9).

**Spec:** `HRM/docs/superpowers/specs/2026-11-20-yc-dat-hang-mua-ngoai-design.md` (đọc kèm; mục "Hiện trạng ERP" là nguồn mọi rule validate/quyền).

**Khuôn mẫu chép theo (đọc trước khi làm):** hrm-api commit `f0ec354ae` (đọc) + `fb60ea508` (ghi) — `Modules/Finance/{Entities/DeliveryCostAskingRequest/*, Http/Controllers/V1/DeliveryCostAskingRequestController.php, Http/Requests/DeliveryCostAskingRequest/*, Services/DeliveryCostAsking*.php, Tests/Feature/DeliveryCostAskingRequestApiTest.php, Transformers/DeliveryCostAskingRequestResource/*}`. FE: `pages/finance/delivery-requests/*` (list/form/detail V2).

## Global Constraints
- Nhánh: HRM `develop` (hrm-api + hrm-client), ERP `develop_02`. KHÔNG đụng gop_db. Commit từng task, KHÔNG push khi user chưa bảo.
- Không tạo bảng/cột/migration mới. Ghi đúng bảng: `inland_order_requests`, `inland_order_request_products`, `inland_order_request_product_details`; chỉ ĐỌC `inland_order_request_product_buyer_groups`, `inland_order_request_product_buyers`, `inland_buy_contracts`.
- Trạng thái (hằng trên entity, tên y ERP): `DA_HUY=0, DA_DUYET=1, CHO_DUYET=2, DANG_TAO=3, DANG_LAP_HOP_DONG=4, DA_LAP_HOP_DONG=5, CHO_TP_DUYET=6`. HRM chỉ ghi 3 và 6.
- Mã phiếu: `'PDHTN-' . str_pad(id, 5, '0', STR_PAD_LEFT)` sau khi có id (ERP `generateCode(5, $this->id)`); trước đó `code` = chuỗi tạm (cột NOT NULL).
- Quyền: `purchase.yeu_cau_dat_hang_ngoai.view` (scope 2 Phòng / 3 Công ty / 4 Tổng cty), `.approve`, `.confirm`. Lập phiếu KHÔNG gắn quyền.
- Giá NCC (`supplier_price`, `supplier_id`/tên NCC, thành tiền theo giá NCC) chỉ trả ra khi status ∈ {1,4,5}; còn lại BE trả `null` và FE hiện "Chưa duyệt".
- File đính kèm: S3 qua `App\Helper\CmcS3Helper::putFiles($files, 'inland_order_requests')`, cột `attachments` = URL nối bằng `", "`. Local upload đi S3 thật → test dùng `Storage::fake`/mock helper, không upload thật.
- URL: HRM trang chi tiết `/sale/inland-order-requests/{id}`; ERP chi tiết `/admin/orders/inland_order_requests/{id}/show`.
- Mọi câu thông báo/lỗi tiếng Việt, bám câu ERP.
- Test hrm-api chạy: `cd HRM/hrm-api && php vendor/bin/phpunit Modules/Sale/Tests/Feature/InlandOrderRequestApiTest.php` (DB `erp_hrm_check` local; thiếu dữ liệu mẫu thì `markTestSkipped` như khuôn).

## Review Focus
1. **Phiếu nháp của người khác** lọt vào danh sách / chi tiết khi người xem có scope Công ty hoặc Tổng cty → phải ẩn (ERP ẩn nháp người khác ở `type=all`). Test: `test_list_hides_other_users_drafts_even_with_group_scope` (Task 1).
2. **Sửa phiếu đã gửi** (status 6/2/1…) qua gọi thẳng API PUT/DELETE → 403, không xoá dòng con (syncProducts xoá sạch buyer/HĐ nếu lọt). Test: `test_update_and_delete_rejected_when_not_draft` (Task 2).
3. **Sửa phiếu nhưng không gửi lại file** → giữ nguyên `attachments` cũ; gửi thêm file → nối vào sau chuỗi cũ. Test: `test_update_without_files_keeps_attachments` + `test_update_appends_new_files` (Task 2).
4. **Ngày cần hàng = hôm nay** bị chặn (`after:today`), và SL `0` / thập phân `0.01` xử lý đúng biên. Test: `test_store_validates_detail_boundaries` (Task 2).
5. **Không có người duyệt nhận thông báo** (phòng/bộ phận chưa khai quản lý, hoặc không ai có `.approve`) → gửi vẫn thành công, ghi 0 dòng, chỉ log. Test: `test_send_succeeds_when_no_recipients` (Task 3).

---

### Task 1: hrm-api — entity + danh sách + chi tiết + xuất Excel (chỉ đọc)

**Files:**
- Create: `Modules/Sale/Entities/InlandOrderRequest/{InlandOrderRequest,InlandOrderRequestProduct,InlandOrderRequestProductDetail,InlandOrderRequestProductBuyerGroup,InlandOrderRequestProductBuyer}.php`
- Create: `Modules/Sale/Services/InlandOrderRequest/InlandOrderRequestService.php`
- Create: `Modules/Sale/Http/Controllers/V1/InlandOrderRequestController.php`
- Create: `Modules/Sale/Transformers/InlandOrderRequestResource/{InlandOrderRequestListResource,InlandOrderRequestDetailResource}.php`
- Modify: `Modules/Sale/Routes/api.php` (nhóm `/inland-order-requests` trong group `/v1/sale`)
- Modify: `app/Support/Permissions/Catalog/purchase.php:684` — `.view` `'platforms' => ['erp', 'hrm']`
- Test: `Modules/Sale/Tests/Feature/InlandOrderRequestApiTest.php`

**Interfaces:**
- Produces:
  - `InlandOrderRequest` (bảng `inland_order_requests`, hằng trạng thái ở Global Constraints, `const STATUSES = [id => ['name' => …]]` tên y ERP), quan hệ `products()`, `buyerGroups()`, `creator()`, `departmentApprover()`, `approver()`; `InlandOrderRequestProduct::details()` (FK `parent_id` — kiểm tên cột thật trong bảng).
  - `InlandOrderRequestService::paginate(Request): LengthAwarePaginator`, `findForCurrentUser(int $id): InlandOrderRequest` (404 nếu không thấy, 403 nếu `!canView`), `canView(InlandOrderRequest, int $employeeId, int $companyId): bool`, `canEdit(InlandOrderRequest, int $employeeId): bool` (= status 3 && created_by), `exportRows(Request): Collection`.
  - Route: `GET /api/v1/sale/inland-order-requests`, `GET /export`, `GET /{id}`.
  - List item JSON: `id, code, status, status_name, creator_name, department_name, created_at, date_needed_min, department_approver_name, approver_name, approved_at, buyers[] (tên), contract_codes[], can_edit, can_delete, erp_url`.
  - Detail JSON: đầu phiếu + `department_approver_comment`, `attachments[]` (tách chuỗi `", "`), `products[]` mỗi dòng `{product_id, code, product_name, model_name, manufacture_name, unit_id, unit_name, suggest_price, vat_percent, price, qty, note, supplier_price|null, supplier_name|null, buyers[], details[{customer_id, customer_name, date_needed, qty, note}]}`, `can_edit`, `can_delete`, `erp_url`.

- [x] **Step 1: Viết test đọc** (khuôn `DeliveryCostAskingRequestApiTest` — `actAsApi`, `employee()`, fixture tạo phiếu bằng `DB::table()->insert` trong transaction):
  - `test_list_shows_own_requests_all_statuses` — NV A không quyền: tạo phiếu A status 3, 6, 1 + phiếu B status 6 ⇒ list A thấy đúng 3 phiếu của A.
  - `test_list_scope_department_shows_department_members` — A có `.view` scope 2 ⇒ thấy phiếu status 6 của B cùng phòng, không thấy của C khác phòng.
  - `test_list_hides_other_users_drafts_even_with_group_scope` — A scope 4 ⇒ không thấy phiếu status 3 của B.
  - `test_list_filters` — lọc `code`, `status`, `product` (khớp `product_name` hoặc `code` dòng hàng), `customer_id`, `start_date`/`end_date` (theo `created_at`) mỗi bộ lọc trả đúng tập.
  - `test_show_hides_supplier_price_until_approved` — status 2 ⇒ `products.0.supplier_price === null`; status 1 ⇒ bằng giá đã ghi.
  - `test_show_forbidden_for_outsider` — C khác phòng không quyền ⇒ 403.
  - `test_show_flags` — status 3 chính chủ ⇒ `can_edit=true`; status 6 ⇒ `can_edit=false`, `erp_url` kết thúc `/admin/orders/inland_order_requests/{id}/show`.
- [x] **Step 2: Chạy test, kỳ vọng FAIL** (route 404).
- [x] **Step 3: Cài entity + service + controller + resource + route.** Phạm vi danh sách port `InlandOrderRequest::searchByFilter` nhánh `type=all`: scope `.view` qua `PermissionChecker::for($employeeId, $companyId)->scope('purchase.yeu_cau_dat_hang_ngoai.view')` — 4 ⇒ không lọc người lập, 3 ⇒ người lập thuộc công ty, 2 ⇒ thuộc phòng, null ⇒ chỉ của mình; luôn thêm `status != 3 OR created_by = me`. `canView` port ERP (trong phạm vi công ty; chính chủ; 6+`.approve`; 2+`.confirm`; 1+là buyer; theo scope). Xuất Excel dùng `ExportColumnRegistry` như `HandoverProductRecordController`, cột = cột danh sách.
- [x] **Step 4: Chạy test, kỳ vọng PASS.**
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng mua ngoài — danh sách + chi tiết đọc bảng ERP`.

### Task 2: hrm-api — lập / sửa / xoá nháp / đính kèm / giá duyệt gần nhất

**Files:**
- Create: `Modules/Sale/Http/Requests/InlandOrderRequest/{InlandOrderRequestStoreRequest,InlandOrderRequestUpdateRequest}.php`
- Create: `Modules/Sale/Services/InlandOrderRequest/InlandOrderRequestWriteService.php`
- Modify: `InlandOrderRequestController.php`, `Modules/Sale/Routes/api.php`
- Test: `InlandOrderRequestApiTest.php`

**Interfaces:**
- Consumes: Task 1 entity, `InlandOrderRequestService::canEdit`.
- Produces:
  - `InlandOrderRequestWriteService::store(array $data, array $files): InlandOrderRequest`, `update(InlandOrderRequest, array $data, array $files): InlandOrderRequest`, `destroy(InlandOrderRequest): void`, `deleteAttachment(InlandOrderRequest, string $url): void`; gọi `InlandOrderRequestNotifier::notifyDepartmentApprovers()` (Task 3) khi status lưu = 6 — Task 2 inject notifier qua constructor, Task 3 cài thân.
  - Route: `POST /` (multipart), `POST /{id}` + `_method=PUT` (multipart), `DELETE /{id}`, `DELETE /{id}/attachments` (body `url`), `GET /latest-approved-prices?product_id=&unit_id=`, `POST /latest-approved-prices/batch` (body `product_ids[]`).
  - Payload: `status (3|6), note, vat_percent, cost_after_vat, vat_cost, total_cost, attachments[] (file), products[{product_id, unit_id, suggest_price, vat_percent, note, details[{customer_id, date_needed (Y-m-d), qty, note}]}]`.

- [x] **Step 1: Viết test ghi:**
  - `test_store_draft_writes_erp_tables` — status 3 ⇒ 201; `inland_order_requests.code` khớp `/^PDHTN-\d{5,}$/`, `company_id/department_id/part_id` = của người lập, `created_by` = employee id; dòng product có `supplier_price == suggest_price`, `qty` = Σ details, `product_name/code/unit_name/manufacture_name` chụp từ danh mục; detail `allocated_qty = 0`, `customer_name` chụp.
  - `test_store_price_uses_company_price_type_1` — `price` = `ProductPriceReader::priceOf(product_unit_id, 1, company_id)` (null ⇒ 0 hay null: ghi đúng như ERP lưu; kiểm cột cho phép null trước khi chốt).
  - `test_store_validates_detail_boundaries` — `date_needed` = hôm nay ⇒ 422 field `products.0.details.0.date_needed`; `qty` 0 ⇒ 422; `qty` 0.01 ⇒ OK; `suggest_price` 0 ⇒ 422; thiếu `note` ⇒ 422; tạo thiếu `attachments` ⇒ 422; `products` rỗng ⇒ 422.
  - `test_update_without_files_keeps_attachments` — sửa không gửi file ⇒ `attachments` không đổi, dòng con được tạo lại theo payload mới.
  - `test_update_appends_new_files` — gửi 1 file ⇒ chuỗi = cũ + `", "` + URL mới.
  - `test_update_and_delete_rejected_when_not_draft` — phiếu status 6 / người khác ⇒ PUT, DELETE, DELETE attachments đều 403; số dòng `inland_order_request_products` không đổi.
  - `test_destroy_draft_removes_lines` — xoá ⇒ phiếu + products + details biến mất.
  - `test_old_erp_draft_editable` — phiếu status 3 tạo bằng insert thô (như ERP lập) sửa được qua HRM.
  - `test_latest_approved_prices` — trả giá NCC của dòng thuộc phiếu status ∈ {1,4,5} mới nhất cho hàng đó (port `latestApprovedPrices`/`batchLatestApprovedPrices` — chép điều kiện lọc ERP 1343+).
  - S3: bind mock `CmcS3Helper` trả URL giả `https://s3.test/inland_order_requests/x.pdf`.
- [x] **Step 2: Chạy, FAIL.**
- [x] **Step 3: Cài.** Rule FormRequest chép y ERP `store`/`update` (spec mục Hiện trạng; `attachments.*` `mimes:ppt,pptx,doc,docx,pdf,xls,xlsx,pg,jpeg,png,zip|max:15240`, Update: `attachments` nullable). `syncProducts` port 1:1 ERP model (xoá buyers, buyer groups, details, products rồi tạo lại) trong `DB::transaction`. Giá công ty: `Modules\MasterData\Services\ProductPrice\ProductPriceReader::priceOf($productUnitId, 1, $companyId)` (cách tìm product_unit như `BorrowSellRequestService::priceByUnitAndType`). Xoá file: chỉ gỡ khỏi chuỗi + `CmcS3Helper::deleteByUrl($url, 'inland_order_requests')`.
- [x] **Step 4: Chạy, PASS** (cả test Task 1).
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng mua ngoài — lập/sửa/xoá/gửi ghi bảng ERP`.

### Task 3: hrm-api — thông báo người duyệt (chuông ERP) + hợp đồng dòng chuông HRM do ERP ghi

**Files:**
- Create: `Modules/Sale/Services/InlandOrderRequest/InlandOrderRequestNotifier.php`
- Test: `InlandOrderRequestApiTest.php`

**Interfaces:**
- Consumes: Task 2 gọi `notifyDepartmentApprovers(InlandOrderRequest $m): int`.
- Produces: `InlandOrderRequestNotifier::notifyDepartmentApprovers(InlandOrderRequest $m): int` (số dòng ghi; lỗi chỉ `Log::warning`, trả 0). Hằng `ERP_SHOW_URL = '/admin/orders/inland_order_requests/%d/show'`, `HRM_SHOW_URL = '/sale/inland-order-requests/%d'`, `APPROVE_PERMISSION = 'purchase.yeu_cau_dat_hang_ngoai.approve'`.

- [x] **Step 1: Viết test:**
  - `test_send_notifies_department_approvers_on_erp_bell` — B có `.approve` + là quản lý phòng của A (`employee_manage_departments`), D có `.approve` nhưng không quản lý ⇒ A gửi (status 6) ghi đúng 1 dòng `notifications` cho B: `notifiable_type='App\Employee'`, `type='App\Notifications\SystemNotification'`, `data.url` = ERP show, `data.content` = `'Bạn có một yêu cầu đặt hàng ngoài cần duyệt từ ' . <tên A>` (chép nguyên câu + định dạng ERP store ~dòng 640), `data.created_by` = A.
  - `test_part_manager_also_notified` — quản lý bộ phận (`employee_manage_parts.part_id` = part A) có `.approve` ⇒ nhận; NV nghỉ (`employees.status != 1`) ⇒ không nhận.
  - `test_draft_save_sends_nothing` — status 3 ⇒ 0 dòng.
  - `test_send_succeeds_when_no_recipients` — không ai đủ điều kiện ⇒ 201, 0 dòng.
  - `test_erp_written_hrm_bell_row_renders` — insert thô 1 dòng `notifications` đúng **dạng ERP sẽ ghi ở Task 9** (`type='Modules\Timesheet\Notifications\BaseNotification'`, `notifiable_type='Modules\Timesheet\Entities\EmployeeInfo'`, `notifiable_id` = employee_info_id người lập, `data` = `NotificationMeta::build(NotificationMeta::KHAC,'YCĐHMN', <action>, <code>, <note>)` + `url`=HRM_SHOW_URL, `type`='inlandOrderRequest', `id`, `employeeInfo`=`{id, fullname, image}`) ⇒ API danh sách chuông HRM của người lập trả dòng đó với `title` và `url` đúng. Test này là hợp đồng định dạng cho Task 9.
- [x] **Step 2: Chạy, FAIL.**
- [x] **Step 3: Cài** theo khuôn `Modules/Finance/Services/DeliveryCostAskingNotifier.php::notifyPurchasing`. Người nhận = giao (holders `.approve` qua `PermissionChecker::holders(..., 'web', $m->company_id)` — kiểm ERP lọc công ty hay không và chép đúng) ∩ (`employee_manage_departments.department_id = $m->department_id` ∪ `employee_manage_parts.part_id = $m->part_id`) ∩ `employees.status = 1`.
- [x] **Step 4: PASS.**
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng mua ngoài — báo TP duyệt trên chuông ERP`.

### Task 4: hrm-api — in phiếu

**Files:**
- Create: `Modules/Sale/Services/InlandOrderRequest/InlandOrderRequestPrintService.php`
- Modify: controller + route `GET /{id}/print-data`
- Test: `InlandOrderRequestApiTest.php`

**Interfaces:** Produces `InlandOrderRequestPrintService::renderTemplate(InlandOrderRequest): string` (khuôn `DeliveryCostAskingRequestPrintService`), mẫu `report_templates` mã `YCDH_TRONG_NUOC` (lấy giá trị hằng `ReportTemplate::YCDH_TRONG_NUOC` từ ERP), biến chép ERP `print_data`/`product_table`.

- [x] **Step 1: Test** `test_print_masks_supplier_price_before_approval` — status 6 ⇒ HTML chứa `Chưa duyệt`, không chứa giá NCC; status 1 ⇒ chứa giá NCC định dạng như ERP; `test_print_signature_flags` — `KS_KY` chỉ khi 1, `TBP_KY` khi 1|2 (so với cách ERP thay biến).
- [x] **Step 2: FAIL. Step 3: Cài. Step 4: PASS.**
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng mua ngoài — in phiếu mẫu YCDH_TRONG_NUOC`.

### Task 5: hrm-client — danh sách + menu

**Files:**
- Create: `pages/sale/inland-order-requests/index.vue`
- Modify: `components/subsystem-menu/sale-hub.js:183` — thay chuỗi `'YC đặt hàng mua ngoài'` bằng `{ n: 'YC đặt hàng mua ngoài', link: '/sale/inland-order-requests' }` (giữ nguyên `n`, không gắn quyền, ghi chú 1 dòng như mục "YC vận chuyển, bốc xếp").

**Interfaces:** Consumes Task 1 list JSON + `meta.statuses`; Task 2 `DELETE /{id}`; Task 4 `print-data`.

- [x] **Step 1:** Dựng trang theo `pages/finance/delivery-requests/index.vue` (V2BaseDataTable, V2BaseSmartFilterPanel, filterStateMixin, exportListFile). Cột: STT, Số YC (link chi tiết), Người lập, Phòng, Ngày lập, Ngày cần, Người duyệt TP, Người duyệt, Ngày duyệt, Buyer/HĐ, Trạng thái (badge), Hành động. Bộ lọc: mã, trạng thái, người lập, phòng/công ty (`V2BaseCompanyDepartmentFilter`), người duyệt, hàng, khách hàng, từ – đến ngày. Hành động: In; Sửa/Xoá khi `can_edit/can_delete` (Xoá qua `BaseConfirmModal`); "Mở trên ERP" (mở tab mới `erp_url`) khi status ≠ 3. Nút "Thêm mới", "Xuất Excel".
- [x] **Step 2: Kiểm bằng Playwright local** (skill run-hrm): đăng nhập NV có phiếu ⇒ danh sách hiện, lọc trạng thái "Chờ TP duyệt" chỉ còn phiếu 6, menu Sale → "YC đặt hàng mua ngoài" mở đúng trang. Ảnh vào scratchpad.
- [x] **Step 3: `npm run lint`** sạch file mới.
- [x] **Step 4: Commit** `feat(sale): YC đặt hàng mua ngoài — màn danh sách`.

### Task 6: hrm-client — form lập / sửa

**Files:**
- Create: `pages/sale/inland-order-requests/add.vue`, `pages/sale/inland-order-requests/_id/edit.vue`, `pages/sale/inland-order-requests/components/InlandOrderRequestForm.vue`

**Interfaces:** Consumes Task 2 payload + routes, Task 1 detail JSON (nạp form sửa).

- [x] **Step 1:** Form theo `DeliveryRequestForm.vue`: đầu phiếu (Ghi chú bắt buộc, Đính kèm nhiều file + danh sách file cũ có nút xoá gọi `DELETE /{id}/attachments`), bảng hàng (picker hàng sẵn có của HRM — dùng picker của `pages/sale/price-asking-requests/add.vue`; ĐVT theo hàng; Giá đề xuất; %VAT; Ghi chú; ô "Giá duyệt gần nhất" lấy `latest-approved-prices/batch` khi đổi danh sách hàng), mỗi hàng N dòng KH (`V2BaseSelectRemote`) / Ngày cần (`V2BaseDatePicker`, min = mai) / SL / Ghi chú. Tổng trước VAT, tiền VAT, sau VAT tính y ERP `formJs.blade.php` (đọc công thức ở đó, gửi `cost_after_vat`, `vat_cost`, `total_cost`, `vat_percent`). Nút **Lưu nháp** (status 3) / **Lưu và gửi** (6); lỗi 422 hiện inline theo key `products.i.details.j.field`; `unsavedChangesMixin`. Thành công ⇒ về trang chi tiết.
- [x] **Step 2: Playwright:** lập phiếu 1 hàng 2 KH ⇒ Lưu nháp ⇒ sửa thêm hàng ⇒ Lưu và gửi ⇒ chi tiết hiện "Chờ TP duyệt"; thử ngày cần = hôm nay ⇒ báo lỗi dưới ô.
- [x] **Step 3: lint. Step 4: Commit** `feat(sale): YC đặt hàng mua ngoài — form lập/sửa`.

### Task 7: hrm-client — chi tiết

**Files:** Create `pages/sale/inland-order-requests/_id/index.vue`

- [x] **Step 1:** Thông tin phiếu (mã, trạng thái badge, người lập, phòng, ngày lập, ghi chú, đính kèm), ý kiến TP, người duyệt TP + Kiểm soát + thời gian, bảng hàng/KH (Giá NCC = `supplier_price` hoặc chữ "Chưa duyệt" khi null; NCC; buyer được giao), HĐ mua đã lập. Nút: In; Sửa/Xoá khi `can_edit`; "Mở trên ERP" khi status ≠ 3 (tooltip: "Huỷ, YC duyệt lại giá, Tạo phụ lục thực hiện trên ERP").
- [x] **Step 2: Playwright:** phiếu status 6 ⇒ không có Sửa, Giá NCC "Chưa duyệt"; phiếu status 1 (data local) ⇒ có giá NCC + buyer.
- [x] **Step 3: lint. Step 4: Commit** `feat(sale): YC đặt hàng mua ngoài — màn chi tiết`.

### Task 8: ERP — chặn ghi + ẩn nút

**Files:**
- Modify: `app/Http/Middleware/ProductMovedToHrm.php` (TARGETS + hằng nhóm + cờ view)
- Modify: `routes/web.php` ~2452–2490 (nhóm `inland_order_requests`)
- Modify: `resources/views/errors/moved_to_hrm.blade.php` (câu mô tả nhóm mới)
- Modify: `resources/views/orders/inland_order_requests/index.blade.php` (nút Thêm mới), `app/Http/Controllers/Order/InlandOrderRequestsController.php::searchData` ~425–455 (nút Sửa/Xoá), `show.blade.php` (nút Sửa nếu có)

- [x] **Step 1:** TARGETS thêm `'inland-order-list' => '/sale/inland-order-requests'`, `'inland-order-create' => '/sale/inland-order-requests/add'`, `'inland-order-edit' => '/sale/inland-order-requests/{id}/edit'`; hằng `INLAND_ORDER_TARGETS` (edit thiếu id lùi về list, như `PRICE_FLOW_TARGETS`); cờ `isInlandOrder` ⇒ câu: "Lập và sửa Phiếu yêu cầu đặt hàng mua ngoài đã chuyển sang HRM. Các bước duyệt, giao buyer, lập hợp đồng vẫn làm trên ERP."
- [x] **Step 2:** Gắn `->middleware('productMovedToHrm:inland-order-create')` cho `create`, `store`; `inland-order-edit` cho `edit`, `update`, `delete`, `deleteFile`. Không đụng route khác.
- [x] **Step 3:** Ẩn nút "Thêm mới" ở index; trong `searchData` bỏ nút Sửa/Xoá, thay bằng link "Sửa trên HRM" (`config('app.hrm_url_FE')./sale/inland-order-requests/{id}/edit`) khi `canEdit()`.
- [x] **Step 4: Kiểm local ERP** (`php artisan route:list | grep inland_order_requests` thấy middleware; mở `/admin/orders/inland_order_requests/create` ⇒ trang "đã chuyển sang HRM" có link đúng; POST store AJAX ⇒ JSON 403 `redirect_url`; danh sách + show + TP duyệt vẫn mở được). Grep `DB_` `.env` ERP trước (memory "ERP local .env DB target đổi theo lúc").
- [x] **Step 5: Commit** (ERP `develop_02`) `feat: YC đặt hàng mua ngoài — chuyển lập/sửa sang HRM`.

### Task 9: ERP — thông báo về người lập trỏ chuông HRM

**Files:**
- Create: `app/Services/HrmBell.php` (class `App\Services\HrmBell`)
- Modify: `InlandOrderRequestsController.php` — `departmentApprove` (~823, thông báo người lập), `reject` (~931), `approve` (~990, thông báo duyệt xong cho người lập)

**Interfaces:** Produces `HrmBell::notifyEmployee(int $employeeId, string $prefix, string $action, string $objectName, ?string $note, string $hrmPath, string $type, int $id): bool` — tra `employees.employee_info_id`, ghi 1 dòng `notifications` ĐÚNG dạng hợp đồng ở Task 3 `test_erp_written_hrm_bell_row_renders` (title `'[' . PREFIX . '] ' . action . ': <b>' . e(name) . '</b>' . ('. ' . e(note) nếu có)`, `module` = giá trị `NotificationMeta::KHAC` của HRM, `employeeInfo` = `{id, fullname, image}` của người thao tác). Lỗi chỉ `Log::warning`, trả false, không chặn duyệt.

- [x] **Step 1:** Cài `HrmBell` (không gọi HTTP, không cần JWT — chuông hiện khi người lập tải lại trang HRM, không có push/socket).
- [x] **Step 2:** Thay 3 chỗ `Notification::sendNotify(...)` gửi **người lập** bằng `HrmBell::notifyEmployee($m->created_by, 'YCĐHMN', <'TP đã duyệt' | 'TP không duyệt' | 'Không duyệt' | 'Đã duyệt'>, $m->code, <ý kiến/lý do nếu có>, '/sale/inland-order-requests/' . $m->id, 'inlandOrderRequest', $m->id)`. Thông báo gửi người `.confirm` (url `preApprove`) GIỮ nguyên.
- [x] **Step 3: Kiểm local:** TP duyệt 1 phiếu trên ERP ⇒ đăng nhập HRM người lập ⇒ chuông có dòng, bấm mở `/sale/inland-order-requests/{id}`. Không duyệt có lý do ⇒ lý do hiện trong câu.
- [x] **Step 4: Commit** (ERP) `feat: YC đặt hàng mua ngoài — báo người lập trên chuông HRM`.

### Task 10: Kiểm cả luồng + cập nhật tài liệu

- [x] **Step 1:** Local, 1 vòng: HRM lập + gửi ⇒ ERP TP thấy chuông ERP, duyệt ⇒ Kiểm soát duyệt giá + giao buyer ⇒ HRM chi tiết hiện giá NCC + buyer, danh sách hiện "Đã duyệt"; ERP mở `create`/`edit` bị chặn.
- [x] **Step 2:** Chạy lại toàn bộ `InlandOrderRequestApiTest` + `DeliveryCostAskingRequestApiTest` (catalog quyền đổi) ⇒ PASS.
- [x] **Step 3:** Cập nhật `HRM/.plans/STATUS.md` (mục đang làm → commit hash), báo user. KHÔNG push.

### Checkpoint — 2026-11-20 17:20 (wrap up tự động)
Vừa hoàn thành: đủ 10 task SDD + review cuối. Chốt với user: ranh giới A (HRM chỉ status 3→6), Cách 1 (KD theo dõi mọi phiếu trên HRM, sau gửi chỉ xem + "Mở trên ERP"), giá NCC chỉ hiện ở 1/4/5, port gốc ghi thẳng bảng ERP. ERP ghi thẳng dòng chuông HRM (không gọi API bằng jwt người duyệt); nhãn `YCĐHMN` khai trong NotificationMeta. E2E local OK (erp_hrm_check), 32/32 test hrm-api, 7/7 ERP. ĐÃ PUSH 20/11 14:25: hrm-api develop `671fac58e`, hrm-client develop `dd3000b15` (cherry-pick riêng, hash local khác), ERP develop_02 `c97b5a30f7`.
Đang dở: —
Bước tiếp theo: gộp gop_db khi user báo. Minor để sau: thứ tự nút trang chi tiết (Sửa→In→Mở trên ERP→Xóa) giữ nguyên theo quy ước.
Blocked: —
