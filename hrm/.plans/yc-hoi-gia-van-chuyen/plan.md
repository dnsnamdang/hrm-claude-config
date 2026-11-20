# Port "Phiếu Yêu cầu hỏi giá vận chuyển" ERP → HRM (phía lập phiếu) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Người kinh doanh lập / sửa / xoá / gửi / in phiếu YC hỏi giá vận chuyển trên HRM và xem kết quả Mua hàng trả lời; Mua hàng vẫn trả lời/duyệt trên ERP như cũ.

**Architecture:** HRM module Finance ghi THẲNG 3 bảng ERP sẵn có trong DB chung (không bảng mới, không migration). Khi gửi, HRM chèn dòng `notifications` dạng ERP (`notifiable_type = App\Employee`) cho người giữ quyền `purchase.mua_hang.manage` → chuông ERP hiện như cũ. Khi ERP trả lời, ERP POST sang endpoint HRM `notify-result` (tiền lệ `notifyHrmImportResult`) → HRM thông báo người lập, link trang HRM. ERP chặn create/store/edit/update/delete bằng middleware "đã chuyển sang HRM".

**Tech Stack:** HRM Laravel (hrm-api, module Finance) + Nuxt 2/Vue 2 (hrm-client); ERP Laravel 6 (TanPhatDev); PHPUnit với `DatabaseTransactions` trên DB local chung `erp_hrm_check` (HRM) / `hrm_erp_test` (ERP).

**Spec (bản track git): `.plans/yc-hoi-gia-van-chuyen/design.md`** · gốc `HRM/docs/superpowers/specs/2026-11-20-yc-hoi-gia-van-chuyen-design.md`

## Global Constraints
- Nhánh: HRM `develop` (hrm-api + hrm-client), ERP `develop_02`. KHÔNG đụng `gop_db` tới khi user bảo.
- KHÔNG tạo bảng/cột, KHÔNG migration, KHÔNG sửa phiếu cũ. Chỉ ghi 3 bảng: `delivery_cost_asking_requests`, `delivery_cost_asking_request_customers` (`parent_id` → phiếu), `delivery_cost_asking_request_customer_products` (`parent_id` → dòng KH, `delivery_cost_asking_request_id` → phiếu).
- Trạng thái (giữ số ERP): `DA_DUYET=1`, `CHO_DUYET=2`, `DANG_TAO=3`, `KHONG_DUYET=4`. Nhãn: 3 "Đang tạo", 2 "Chờ duyệt", 1 "Đã duyệt", 4 "Không duyệt".
- Mã: `"PYCHGVC-" . str_pad($id, 5, '0', STR_PAD_LEFT)` (id dài hơn 5 số thì giữ nguyên — như ERP `generateCode(5,$id)`). Cột `code` NOT NULL ⇒ insert `''` rồi set mã sau khi có id, trong cùng transaction.
- Phương thức VC: `1 => 'Hàng không'`, `2 => 'Đường biển'`, `3 => 'Đường bộ'`.
- Validate store (y ERP): `manufacture_id required|exists:manufactures,id`; `note nullable|string|max:255`; `customers required|array|min:1`; `customers.*.customer_id required|exists:customers,id`; `customers.*.shipping_method required|in:1,2,3`; `customers.*.products required|array|min:1`; `customers.*.products.*.product_id required|exists:products,id`; `customers.*.products.*.unit_id required|exists:units,id`; `customers.*.products.*.qty required|numeric|min:1|max:99999999`; `status required|in:2,3`. Update = như store nhưng KHÔNG nhận `manufacture_id` (giữ hãng cũ).
- Quyền: lập không cần quyền. Sửa/xoá: `status ∈ {3,4}` và `created_by = auth()->id()`. Xem: `created_by = auth()->id()` (HRM chỉ phục vụ người lập). Danh sách HRM: chỉ phiếu `created_by = auth()->id()`.
- `created_by`/`updated_by` = `auth()->id()` (employees.id, id chung ERP); `company_id`/`department_id` lấy từ thông tin nhân viên đăng nhập như `DeliveryRequestWriteService::store` dòng 98-101.
- Gửi (status 2): set `received_time = now()`. `approver_id`, `approved_time`, `comment`, `cost` chỉ ERP ghi — HRM không bao giờ ghi (store/update giữ nguyên `cost` = null khi tạo lại dòng KH).
- Notify Mua hàng (ERP): mỗi người nhận 1 dòng `notifications`: `id` uuid, `type = 'App\Notifications\SystemNotification'`, `notifiable_type = 'App\Employee'`, `notifiable_id` = employees.id, `read_at = null`, `data` JSON `{"url": "/admin/orders/delivery_cost_asking_requests/{id}/show", "content": "<fullname> vừa gửi yêu cầu hỏi giá <b>{code}</b>", "created_by": <employees.id>, "sender_name": <fullname>, "sender_avatar": <avatar>}`. Người nhận = `App\Support\Permissions\PermissionChecker::holdersAnyCompany('purchase.mua_hang.manage', 'web')` (cùng luật ERP `Employee::withPermission`). URL lấy đúng `route('DeliveryCostAskingRequest.show', $id, false)` ERP — xác nhận bằng `php artisan route:list --name=DeliveryCostAskingRequest.show` ở ERP trước khi chốt hằng.
- Notify người lập (HRM): `EmployeeInfoService::sendNotification($employeeInfoId, NotificationMeta::build(NotificationMeta::KHAC, 'YCHGVC', <action>, $code, <notes>) + ['url' => '/finance/delivery-cost-asking-requests/'.$id, 'type' => ..., 'id' => $id])` theo mẫu `DeliveryRequestNotifyService`; action "đã duyệt" / "không duyệt"; notes = người duyệt (+ lý do khi không duyệt). Lỗi notify chỉ log, không chặn.
- Menu: `hrm-client/components/subsystem-menu/sale-hub.js:183` đổi chuỗi `'YC hỏi giá vận chuyển'` thành `{ n: 'YC hỏi giá vận chuyển', link: '/finance/delivery-cost-asking-requests' }` (giữ nguyên nhãn — nhãn là menuKey). Không gắn quyền.
- Mẫu in: `report_templates` id **101** (`YC_HOI_GIA_VC`), cùng bộ biến ERP `SO_PHIEU, LOGO, CONG_TY, DIA_CHI_CONG_TY, NGAY, THANG, NAM, NGAY_LAP, NGUOI_LAP, PHONG_BAN, GHI_CHU, GHI_CHU_DUYET, NGUOI_DUYET, NGAY_DUYET, CHI_TIET`; `CHI_TIET` = bảng cột `STT, Khách hàng, Tên hàng, Mã hàng, SL, Phương thức giao hàng, Chi phí vận chuyển`, KH rowspan theo số hàng — bám `DeliveryCostAskingRequest::getPrintData` ERP (~dòng 265-320).
- UI HRM theo skill dự án `erp-to-hrm-screen`, `list-page`, `button-convention`, `print-page`, `unsaved-changes`, `notification-convention`.
- Commit kết thúc bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Tài liệu chỉ ghi trong `HRM/.plans`, `HRM/docs`, `ERP/.plans`.

## Review Focus
- Sửa phiếu "Không duyệt" (4) rồi Lưu nháp/gửi lại: KH/hàng tạo lại, `cost` cũ mất (như ERP sync xoá-tạo lại), `comment`/`approver_id` cũ giữ nguyên tới khi ERP trả lời lại — test ở Task 2.
- Người khác (không phải người lập) gọi show/update/destroy/print bằng id: phải 403, kể cả khi có quyền Mua hàng — test ở Task 2/3.
- Phiếu đang Chờ duyệt (2) hoặc Đã duyệt (1): update/destroy bị từ chối 422/403, không đổi DB — test ở Task 2.
- Không ai giữ quyền `purchase.mua_hang.manage`: gửi vẫn thành công, 0 dòng notify, không lỗi — test ở Task 3.
- ERP gọi `notify-result` với phiếu không tồn tại / `created_by` không map được employee_info_id: 404/422, không tạo thông báo — test ở Task 4.

---

### Task 1: Entity + danh sách + chi tiết (chỉ đọc)

**Files:**
- Create: `HRM/hrm-api/Modules/Finance/Entities/DeliveryCostAskingRequest/{DeliveryCostAskingRequest,DeliveryCostAskingRequestCustomer,DeliveryCostAskingRequestCustomerProduct}.php`
- Create: `HRM/hrm-api/Modules/Finance/Services/DeliveryCostAskingRequestService.php`
- Create: `HRM/hrm-api/Modules/Finance/Http/Controllers/V1/DeliveryCostAskingRequestController.php`
- Create: `HRM/hrm-api/Modules/Finance/Transformers/DeliveryCostAskingRequestResource/{DeliveryCostAskingRequestListResource,DeliveryCostAskingRequestDetailResource}.php`
- Modify: `HRM/hrm-api/Modules/Finance/Routes/api.php` (thêm group `/delivery-cost-asking-requests` cạnh `/delivery-requests` ~1905)
- Test: `HRM/hrm-api/Modules/Finance/Tests/Feature/DeliveryCostAskingRequestApiTest.php`

**Interfaces:**
- Produces: `DeliveryCostAskingRequest` (table `delivery_cost_asking_requests`, consts `DA_DUYET/CHO_DUYET/DANG_TAO/KHONG_DUYET`, `STATUSES`, `SHIPPING_METHODS`, relations `customers()` hasMany `parent_id`, `manufacture()`, `creator()`, `approver()`, `department()`; `canEdit(): bool`, `canDelete(): bool` theo Global Constraints). `DeliveryCostAskingRequestCustomer::products()` hasMany `parent_id`; customer product `product()`, `unit()`.
- Produces: `DeliveryCostAskingRequestService::paginate(Request $r)` lọc `created_by = auth()->id()` + filter `code`, `status`, `manufacture_id`, `product` (tên/mã like), `customer_id`, `start_date`/`end_date` (theo `created_at`), `per_page`; `findForCurrentUser(int $id): DeliveryCostAskingRequest` (404 không có, 403 không phải người lập).
- Produces API: `GET /api/v1/finance/delivery-cost-asking-requests` → list item `{id, code, manufacture_name, creator_name, created_at, received_time, approver_name, approved_time, status, status_name, can_edit, can_delete}`; `GET /{id}` → detail `{…list fields, manufacture_id, note, comment, department_name, customers: [{id, customer_id, customer_name, shipping_method, shipping_method_name, cost, products: [{product_id, name, code, model_name, brand_name, unit_id, unit_name, weight, size, qty}]}]}`.

- [x] **Step 1: Viết test fail** — tạo dữ liệu bằng `DB::table` (1 phiếu của A status 1 có `cost=1500000`, `approver_id`, `comment`; 1 phiếu của B), `actingAs` A theo mẫu `OpeningContractApiTest::actAsApi`.
  - `test_index_only_lists_own_requests`: list chỉ có phiếu A.
  - `test_index_filters_by_status_and_code`: `?status=1&code=PYCHGVC` trả đúng phiếu.
  - `test_show_returns_cost_approver_and_comment`: `customers.0.cost == 1500000`, `approver_name` khớp, `comment` khớp, `shipping_method_name == 'Đường biển'` với shipping_method 2.
  - `test_show_other_users_request_is_forbidden`: A xem phiếu B → 403.
- [x] **Step 2: Chạy, xác nhận FAIL** — `cd HRM/hrm-api && php artisan test Modules/Finance/Tests/Feature/DeliveryCostAskingRequestApiTest.php` → 404 route.
- [x] **Step 3: Cài entity/service/controller/resource/route** như Interfaces; route tĩnh trước `/{id}`, `where('id','[0-9]+')`.
- [x] **Step 4: Chạy lại, PASS.**
- [x] **Step 5: Commit** `feat(finance): YC hỏi giá vận chuyển — danh sách + chi tiết đọc bảng ERP`.

### Task 2: Lập / sửa / xoá / gửi + dữ liệu chọn

**Files:**
- Create: `HRM/hrm-api/Modules/Finance/Http/Requests/DeliveryCostAskingRequest/{DeliveryCostAskingRequestStoreRequest,DeliveryCostAskingRequestUpdateRequest}.php`
- Create: `HRM/hrm-api/Modules/Finance/Services/DeliveryCostAskingRequestWriteService.php`
- Modify: controller + routes Task 1
- Test: `DeliveryCostAskingRequestApiTest.php` (thêm)

**Interfaces:**
- Consumes: entity Task 1.
- Produces: `DeliveryCostAskingRequestWriteService::store(array $data): DeliveryCostAskingRequest`, `update(DeliveryCostAskingRequest $m, array $data): DeliveryCostAskingRequest`, `destroy(DeliveryCostAskingRequest $m): void`; private `syncCustomers(DeliveryCostAskingRequest $m, array $customers): void` (xoá products theo `delivery_cost_asking_request_id`, xoá customers theo `parent_id`, chèn lại). Khi `status == 2` gọi `DeliveryCostAskingNotifier::notifyPurchasing($m)` (Task 3; Task 2 dùng bản giả bind qua container).
- Produces API: `POST /`, `PUT /{id}`, `DELETE /{id}`; dữ liệu chọn: `GET /manufacturers?keyword=`, `GET /customers?keyword=` (`customers` đang hoạt động, trả `{id, code, name}`), `GET /products?manufacture_id=&keyword=` (bắt buộc `manufacture_id`; trả `{id, name, code, model_name, brand_name, weight, size, units:[{id,name}]}` — danh sách ĐVT bám ERP `ProductController@getData` mà form ERP gọi ở `formJs.blade.php:42`).
- Thông báo lỗi tiếng Việt cho 422 (theo skill `form-validate`); sửa/xoá sai trạng thái → 422 "Chỉ sửa/xoá được phiếu Đang tạo hoặc Không duyệt".

- [x] **Step 1: Viết test fail:**
  - `test_store_draft_writes_three_erp_tables`: POST status 3, 2 KH × 2 hàng → DB có 1 phiếu `code` khớp `/^PYCHGVC-\d{5,}$/`, `company_id/department_id` = của A, `received_time` null, 2 dòng KH (`cost` null), 4 dòng hàng có cả `parent_id` và `delivery_cost_asking_request_id`.
  - `test_store_send_sets_received_time_and_notifies`: status 2 → `received_time` not null, notifier giả nhận đúng 1 lần.
  - `test_store_validation_mirrors_erp`: thiếu `manufacture_id`, `shipping_method=5`, `qty=0`, `customers=[]`, KH không có hàng → 422 từng trường.
  - `test_update_keeps_manufacturer_and_resyncs_lines`: gửi `manufacture_id` khác → hãng giữ nguyên; dòng KH/hàng đúng bộ mới.
  - `test_resend_rejected_request_drops_old_cost_keeps_comment`: phiếu status 4 có `cost`, `comment` → update status 2 → `cost` null, `comment` còn, status 2.
  - `test_update_or_destroy_pending_or_approved_is_rejected`: status 2 và 1 → 422, DB không đổi.
  - `test_other_user_cannot_update_or_destroy`: → 403.
  - `test_destroy_removes_all_three_tables`.
  - `test_products_requires_manufacturer_and_filters_by_it`.
- [x] **Step 2: Chạy, FAIL.**
- [x] **Step 3: Cài FormRequest + WriteService + routes** (mọi ghi trong `DB::transaction`).
- [x] **Step 4: Chạy, PASS** (cả test Task 1).
- [x] **Step 5: Commit** `feat(finance): YC hỏi giá vận chuyển — lập/sửa/xoá/gửi ghi bảng ERP`.

### Task 3: Notify Mua hàng trong ERP khi gửi

**Files:**
- Create: `HRM/hrm-api/Modules/Finance/Services/DeliveryCostAskingNotifier.php`
- Test: `HRM/hrm-api/Modules/Finance/Tests/Feature/DeliveryCostAskingNotifierTest.php`

**Interfaces:**
- Produces: `DeliveryCostAskingNotifier::notifyPurchasing(DeliveryCostAskingRequest $m): int` (số dòng đã chèn; `protected function recipients(): array` trả employees.id — tách ra để test override); `notifyCreatorResult(DeliveryCostAskingRequest $m): void` (dùng ở Task 4). Hằng `ERP_SHOW_URL = '/admin/orders/delivery_cost_asking_requests/%d/show'` (xác nhận theo Global Constraints).
- Bọc try/catch: lỗi chỉ `Log::warning`, không ném.

- [x] **Step 1: Viết test fail:**
  - `test_inserts_erp_style_rows_for_each_holder`: override `recipients()` = [X, Y] → 2 dòng `notifications` với `notifiable_type = 'App\Employee'`, `type = 'App\Notifications\SystemNotification'`, `read_at` null, `data.url` = URL ERP của phiếu, `data.content` chứa `<b>{code}</b>`, `data.created_by` = A, `data.sender_name` = tên A.
  - `test_no_holder_sends_nothing_without_error`: `recipients()` = [] → trả 0, không exception.
  - `test_recipients_use_web_guard_permission_holders`: gán quyền `purchase.mua_hang.manage` guard web cho X (theo mẫu `Concerns/GrantsPermissionScope`) → `recipients()` chứa X.
- [x] **Step 2: Chạy, FAIL.**
- [x] **Step 3: Cài notifier**; bind thật trong controller (bỏ bản giả Task 2 trong runtime, test Task 2 vẫn bind giả).
- [x] **Step 4: PASS cả 3 file test.**
- [x] **Step 5: Kiểm tay** (local, `run-hrm`): gửi 1 phiếu → mở ERP local bằng user có quyền Mua hàng, chuông có thông báo, bấm vào mở đúng trang show ERP.
- [x] **Step 6: Commit** `feat(finance): YC hỏi giá VC — gửi phiếu báo Mua hàng trên chuông ERP`.

### Task 4: Endpoint nhận kết quả từ ERP + in

**Files:**
- Create: `HRM/hrm-api/Modules/Finance/Services/DeliveryCostAskingRequestPrintService.php`
- Modify: controller + routes; notifier Task 3 (`notifyCreatorResult`)
- Test: `DeliveryCostAskingRequestApiTest.php` (thêm)

**Interfaces:**
- Produces API: `POST /{id}/notify-result` (validate `status required|in:1,4`; đọc phiếu theo id KHÔNG giới hạn người lập — người gọi là Mua hàng qua JWT ERP; không thấy phiếu → 404; `created_by` không có `employee_info_id` → 422) → gọi `notifyCreatorResult`. `GET /{id}/print` → `{html}` render mẫu 101 (chỉ người lập).
- `DeliveryCostAskingRequestPrintService::build(DeliveryCostAskingRequest $m): array` (bộ biến Global Constraints) + `renderTemplate($m): string`, bám `AdditionAccountingRequestPrintService` (dùng `ErpReportTemplate`, thêm hằng `YC_HOI_GIA_VC = 101`).

- [x] **Step 1: Viết test fail:**
  - `test_notify_result_approved_notifies_creator_with_hrm_link`: notifier/`EmployeeInfoService` giả → nhận đúng employee_info_id của người lập, `url == '/finance/delivery-cost-asking-requests/{id}'`, nội dung chứa mã + "đã duyệt".
  - `test_notify_result_rejected_includes_reason`: status 4, phiếu có `comment` "Thiếu kích thước" → notes chứa lý do.
  - `test_notify_result_unknown_request_404` và `test_notify_result_unmapped_creator_422`: không tạo thông báo.
  - `test_print_fills_erp_variables`: `build()` có `SO_PHIEU` = mã, `NGUOI_DUYET`, `CHI_TIET` chứa tên KH với `rowspan="2"` khi KH có 2 hàng và chi phí định dạng tiền.
  - `test_print_other_user_forbidden`: 403.
- [x] **Step 2: FAIL.** - [x] **Step 3: Cài.** - [x] **Step 4: PASS toàn bộ test module này.**
- [x] **Step 5: Commit** `feat(finance): YC hỏi giá VC — nhận kết quả ERP + in mẫu 101`.

### Task 5: Màn HRM (client) + menu

**Files:**
- Create: `HRM/hrm-client/pages/finance/delivery-cost-asking-requests/{index.vue,create.vue,_id/index.vue,_id/edit.vue,api.js,components/DeliveryCostAskingRequestForm.vue}`
- Modify: `HRM/hrm-client/components/subsystem-menu/sale-hub.js:183`

**Interfaces:**
- Consumes: API Task 1–4 (`API_BASE = '/v1/finance/delivery-cost-asking-requests'` trong `api.js`).
- Bám cấu trúc `pages/finance/delivery-requests/*` (V2Base*, `unsavedChangesMixin`, `saveAndContinueMixin`, `apiErrorMessage`, `scrollToFirstError`).
- index: cột STT, Số yêu cầu (link chi tiết), Hãng sản xuất, Người lập, Ngày lập (d/m/Y), Ngày nhận, Người duyệt, Ngày duyệt (d/m/Y H:i), Trạng thái (badge), Hành động In / Sửa / Xoá theo `can_edit`/`can_delete`; bộ lọc mã, trạng thái, hãng, hàng hoá, khách hàng, khoảng ngày lập; nút "Thêm mới".
- form: Hãng SX (khoá khi sửa), Ghi chú; bảng KH → hàng cột STT, Khách hàng, Tên hàng hóa, Mã hàng, Model, Thương hiệu, ĐVT (chọn từ `units`), Trọng lượng (kg), Kích thước (cm), SL, Phương thức vận chuyển (1 lựa chọn mỗi KH); "Thêm hàng hóa" disabled tới khi chọn hãng; "Thêm khách hàng"; xoá dòng; nút Lưu nháp (status 3) / Lưu và gửi (status 2). Đổi hãng khi đã có hàng → xác nhận rồi xoá hàng đã chọn.
- chi tiết: thông tin phiếu + bảng KH/hàng + cột Chi phí vận chuyển mỗi KH + Người duyệt / Ngày duyệt / Ghi chú duyệt; nút In, Sửa/Xoá khi được phép; KHÔNG có nút trả lời.

- [x] **Step 1:** Cài 4 trang + form + api.js + menu.
- [x] **Step 2: Lint** `cd HRM/hrm-client && npx eslint pages/finance/delivery-cost-asking-requests components/subsystem-menu/sale-hub.js` → 0 lỗi.
- [x] **Step 3: Kiểm tay bằng Playwright** (skill `run-hrm`, ảnh vào scratchpad): menu Sale hub mở được màn; lập nháp 2 KH × 2 hàng → hiện danh sách "Đang tạo"; sửa rồi Lưu và gửi → "Chờ duyệt", nút Sửa/Xoá biến mất; validate (không chọn hãng, SL 0) báo đỏ đúng ô; In ra mẫu có bảng rowspan; rời form đang sửa → cảnh báo chưa lưu.
- [x] **Step 4: Commit** `feat(finance): màn YC hỏi giá vận chuyển HRM + menu Sale hub`.

### Task 6: ERP — chặn lập/sửa/xoá, báo kết quả sang HRM

**Files:**
- Modify: `ERP/TanPhatDev/app/Http/Middleware/ProductMovedToHrm.php` (thêm target `'delivery-cost-asking' => '/finance/delivery-cost-asking-requests'`, `'delivery-cost-asking-edit' => '/finance/delivery-cost-asking-requests/{id}/edit'`; câu thông báo chung `MESSAGE`)
- Modify: `ERP/TanPhatDev/routes/web.php:2243-2249` — `create`, `store` → `productMovedToHrm:delivery-cost-asking`; `edit`, `update`, `delete` → `productMovedToHrm:delivery-cost-asking-edit`. Giữ `index`, `show`, `print`, `reply`, `searchData`.
- Modify: `ERP/TanPhatDev/app/Http/Controllers/Order/DeliveryCostAskingRequestController.php` — `searchData` bỏ nút Sửa/Xoá; `reply()` sau khi lưu gọi `notifyHrmResult($id, $status)` (copy khuôn `WrApproveResultsController::notifyHrmImportResult`, URL `config('app.hrm_url_BE').'/api/v1/finance/delivery-cost-asking-requests/{id}/notify-result'`, json `{status}`, timeout 5, lỗi chỉ log).
- Modify: `ERP/TanPhatDev/app/Model/Order/DeliveryCostAskingRequest.php::reply` — bỏ 2 dòng `Notification::sendNotify` cho người lập (thay bằng thông báo HRM; tránh báo đôi).
- Modify: `ERP/TanPhatDev/resources/views/orders/delivery_cost_asking_requests/index.blade.php` — nút "Thêm mới" trỏ `config('app.hrm_url_FE').'/finance/delivery-cost-asking-requests/create'` (mở tab mới).
- Test: `ERP/TanPhatDev/tests/Feature/DeliveryCostAskingRoutesMovedToHrmTest.php`

- [x] **Step 1: Viết test fail** theo khuôn `TempProductRoutesMovedToHrmTest`:
  - `test_create_and_edit_pages_show_moved_page_with_hrm_link`: GET create → 403 trang "Chức năng đã chuyển sang HRM", đúng 1 link `…/finance/delivery-cost-asking-requests`; GET `/{id}/edit` và `/{id}/delete` → link `…/{id}/edit` (delete về danh sách cũng chấp nhận — chốt 1 và assert).
  - `test_store_and_update_post_return_moved_json`: 403 JSON `{success:false, redirect_url}`.
  - `test_index_show_print_reply_still_open`: không bị middleware chặn (status ≠ 403 từ middleware).
  - `test_reply_posts_result_to_hrm_and_does_not_block_on_failure`: Guzzle mock (bind client hoặc tách `protected function hrmClient()`): reply status 1 → 1 request POST đúng URL + `{status:1}`; client ném lỗi → reply vẫn lưu `cost`/`status`, response thành công.
- [x] **Step 2: FAIL** — `cd ERP/TanPhatDev && vendor/bin/phpunit tests/Feature/DeliveryCostAskingRoutesMovedToHrmTest.php`.
- [x] **Step 3: Cài.** (Trước khi chạy test: `grep DB_ .env` — memory: .env ERP local có lúc trỏ prod.)
- [x] **Step 4: PASS** + chạy lại `TempProductRoutesMovedToHrmTest` để chắc middleware cũ không vỡ.
- [x] **Step 5: Kiểm tay đầu-cuối:** HRM gửi phiếu → ERP Mua hàng thấy chuông, mở show, nhập chi phí, Duyệt → HRM người lập nhận thông báo, bấm mở chi tiết HRM thấy chi phí + người duyệt; lặp với Không duyệt có lý do.
- [x] **Step 6: Commit (ERP develop_02)** `feat(order): YC hỏi giá VC chuyển lập phiếu sang HRM, báo kết quả về HRM`.

### Task 7: Wrap up
- [x] Cập nhật checkpoint plan này + `HRM/.plans/STATUS.md`; hỏi user trước khi push develop (HRM 2 repo + ERP develop_02); gop_db chỉ khi user bảo.

### Checkpoint — 20/11/2026
Vừa hoàn thành: Task 1–6 + final review (opus) + 1 lượt sửa 2 lỗi Important (notify-result kiểm người duyệt/quyền Mua hàng + lấy kết quả theo DB; chặn trùng KH / hàng trong cùng KH ở BE + FE). Test DeliveryCostAsking* 27/27.
Commit (CHƯA push): hrm-api develop f0ec354…0663e25e5 + 9bd4ae8d6 · hrm-client develop 3d23895d5 + d3f04ead0 · ERP develop_02 3adf898dd3.
Đang làm dở: không.
Bước tiếp theo: user cho phép thì push develop (2 repo HRM) + develop_02 (ERP); gop_db chỉ khi user bảo. Minor hoãn: ERP chỉ gọi notify khi status 1/4; lockForUpdate khi gửi.
Blocked:

Đã push 20/11/2026: hrm-api develop 4f3848615, hrm-client develop ab6e5feae (cherry-pick lên origin, bỏ commit YCĐHMN xen giữa), ERP develop_02 3adf898dd3. Chưa gop_db.

### Checkpoint — 2026-11-20 17:20 (wrap up tự động)
Vừa hoàn thành: đủ 7 task + review cuối (sửa giả mạo `notify-result` → kiểm người duyệt/quyền Mua hàng + lấy kết quả từ DB; chặn trùng KH / trùng hàng trong 1 KH ở BE `withValidator` và FE). E2E local phiếu PYCHGVC-00188 (lưu nháp → sửa → gửi → chuông ERP Mua hàng → in mẫu 101). ĐÃ PUSH: hrm-api develop `4f3848615`, hrm-client develop `ab6e5feae` (cherry-pick riêng qua worktree tạm; develop local còn bản gốc 92456d6ea..2a9caeb4d), ERP develop_02 `3adf898dd3`.
Đang dở: — (test Finance có 3 file đỏ sẵn từ trước, không do việc này; golden route ERP lệch price_asking có sẵn).
Bước tiếp theo: gộp gop_db khi user báo.
Blocked: —
