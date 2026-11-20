# Phiếu Yêu cầu đặt hàng (port ERP rootOrderRequest → HRM, phía KD) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** KD lập / sửa / lưu nháp / gửi duyệt / xoá nháp Phiếu yêu cầu đặt hàng (`PDH-xxxxx`) trên HRM, theo dõi mọi trạng thái; ERP giữ TP duyệt, XNK tiếp nhận và mọi bước sau.

**Architecture:** hrm-api module `Sale` đọc/ghi thẳng 3 bảng ERP `root_order_request*` (DB chung), logic chép 1:1 `RootOrderRequestController` + model ERP. hrm-client thêm 4 trang `pages/sale/order-requests`. ERP chặn tạo/sửa/xoá bằng `productMovedToHrm` và thêm chuông HRM cho người lập qua `App\Services\HrmBell`.

**Tech Stack:** hrm-api Laravel 8 (nwidart, JWT `auth:api`, PHPUnit `DatabaseTransactions` trên DB chung `erp_hrm_check`) · hrm-client Nuxt 2 + `V2Base*` · ERP Laravel 6 (Blade + AngularJS).

**Spec:** `HRM/docs/superpowers/specs/2026-11-20-yc-dat-hang-design.md` (mục "Hiện trạng ERP" + "Đã kiểm" là nguồn mọi rule).

**Khuôn mẫu chép theo (đọc trước):** port YC đặt hàng mua ngoài cùng ngày — hrm-api `Modules/Sale/{Entities,Services,Http/Controllers/V1,Http/Requests,Transformers}/InlandOrderRequest*`, test `Modules/Sale/Tests/Feature/InlandOrderRequestApiTest.php`, route nhóm `/inland-order-requests` trong `Modules/Sale/Routes/api.php`; hrm-client `pages/sale/inland-order-requests/*`; ERP (develop_02) commit `91e79e4068`, `c13449ef3e`, `c97b5a30f7` (`ProductMovedToHrm` TARGETS, `HrmBell`).

## Global Constraints
- Nhánh: HRM `develop` (hrm-api + hrm-client), ERP `develop_02` (repo local đang ở `gop_db` — `git checkout develop_02` trước task ERP, kiểm `git status` sạch trước). KHÔNG đụng gop_db. Commit từng task, KHÔNG push. Chỉ stage file của task (local có việc dở của người khác: `DeliveryCostAsking*`…).
- Không tạo bảng/cột/migration. Ghi đúng: `root_order_requests`, `root_order_request_products`, `root_order_request_product_details`. KHÔNG ghi các cột phía kho/tiếp nhận (`status` detail > 1, `stock_incoming_*`, `arrived_qty`, `arriving_qty`, `splited`, `is_split`, `type_order_request`, `stock_entry_flowable_*`, `notification_orderable_*`).
- Trạng thái (hằng entity, tên y ERP): `DANG_TAO=1 'Đang tạo'`, `CHO_TP_DUYET=2 'Chờ TP duyệt'`, `CHO_DUYET=3 'Chờ tiếp nhận'`, `DA_DUYET=4 'Đã tiếp nhận'`, `DA_HUY=5 'Hủy'`. HRM chỉ ghi 1 và 2.
- Mã: `'PDH-' . str_pad(id, 5, '0', STR_PAD_LEFT)` sau khi có id; trước đó `code` = chuỗi tạm 16 ký tự.
- Quyền: xem `purchase.phieu_yeu_cau_dat_hang.view` (scope 2 Phòng / 3 Công ty / 4 Tổng cty), TP `purchase.phieu_yeu_cau_dat_hang_truong_phong.approve` (chỉ dùng để tính người nhận chuông + canView). Lập phiếu KHÔNG gắn quyền.
- URL: HRM chi tiết `/sale/order-requests/{id}`; ERP chi tiết `/admin/orders/root_order_request/{id}/show`.
- Câu chữ bám ERP: chuông TP `"Bạn có một yêu cầu đặt hàng cần duyệt từ {fullname}"`; lỗi phân công `"Chưa phân công người phụ trách thương hiệu, hãng sản xuất"`; lỗi ngày `"Không được nhỏ hơn ngày {d/m/Y}"` (= hôm nay + tổng KPI + 1); lỗi thương hiệu `"Hàng {tên} có thương hiệu không khớp!"`.
- Prefix chuông HRM: `'YCĐH'` → thêm `'YCĐH' => 'YC đặt hàng'` vào `App\Support\NotificationMeta::OBJECT_LABELS` (cạnh `'YCĐHMN'`).
- Test hrm-api: `cd HRM/hrm-api && php vendor/bin/phpunit Modules/Sale/Tests/Feature/OrderRequestApiTest.php`. ERP `.env` trỏ DB remote — mọi lệnh ERP local phải override `DB_HOST/DB_PORT/DB_DATABASE/DB_USERNAME/DB_PASSWORD` sang `erp_hrm_check` bằng env process; KHÔNG migrate, KHÔNG ghi remote.

## Review Focus
1. **Nháp người khác lọt danh sách/chi tiết** khi người xem có scope 3/4 → ẩn. Test `test_list_hides_other_users_drafts_even_with_group_scope` (Task 1).
2. **Sửa/xoá/gửi phiếu đã rời status 1** (ERP vừa duyệt giữa lúc mở form) → 422 "Phiếu đã được gửi/xử lý, không sửa được", dòng con không bị xoá-tạo-lại. Test `test_stale_update_rejected_after_status_change` (Task 2).
3. **Mã chỉ "Đặt tồn kho", không có KH** → lưu được (details rỗng), `request_qty` = 0, `order_company_request_qty` đúng; tắt đặt tồn kho mà không KH → 422. Test `test_order_company_without_details` (Task 2).
4. **Hãng không có `kpi_sales` cho công ty** → min_date = hôm nay, không 500. Test `test_min_date_without_kpi` (Task 2).
5. **Không ai đủ điều kiện nhận chuông TP** → gửi vẫn 201, 0 dòng, chỉ log. Test `test_send_succeeds_when_no_recipients` (Task 3).

---

### Task 1: hrm-api — entity + danh sách + chi tiết (chỉ đọc) + quyền view sang HRM

**Files:**
- Create: `Modules/Sale/Entities/OrderRequest/{RootOrderRequest,RootOrderRequestProduct,RootOrderRequestProductDetail}.php`
- Create: `Modules/Sale/Services/OrderRequest/OrderRequestService.php`
- Create: `Modules/Sale/Http/Controllers/V1/OrderRequestController.php`
- Create: `Modules/Sale/Transformers/OrderRequestResource/{OrderRequestListResource,OrderRequestDetailResource}.php`
- Modify: `Modules/Sale/Routes/api.php` (nhóm `/order-requests`, cạnh `/inland-order-requests`)
- Modify: `app/Support/Permissions/Catalog/purchase.php:10` — `.view` `'platforms' => ['erp', 'hrm']`
- Test: `Modules/Sale/Tests/Feature/OrderRequestApiTest.php`

**Interfaces:**
- Produces:
  - `RootOrderRequest` (hằng trạng thái + `STATUSES`), quan hệ `products()` (chỉ dòng `is_root = 1` — chép điều kiện Model ERP:116-124 nhánh trước tiếp nhận; sau tiếp nhận chép đúng lọc `is_split`/`is_root`), `creator()`, `departmentApprover()`, `approver()`, `brand()`, `manufacture()`, `sendCompany()`; `RootOrderRequestProduct::details()` (kiểm tên FK thật).
  - `OrderRequestService::paginate(Request)`, `findForCurrentUser(int $id): RootOrderRequest` (404/403), `canView(RootOrderRequest, int $employeeId, int $companyId): bool`, `canEdit(RootOrderRequest, int $employeeId): bool` (= status 1 && created_by), `findEditable(int $id): RootOrderRequest`.
  - Route: `GET /api/v1/sale/order-requests`, `GET /{id}`.
  - List JSON: `id, code, status, status_name, creator_name, department_name, company_name, send_company_name, brand_name, manufacture_name, created_at, department_approver_name, department_approved_time, approver_name (buyer tiếp nhận), approved_time, can_edit, can_delete, erp_url`; `meta.statuses`.
  - Detail JSON: đầu phiếu + `note`, `department_approver_comment`, `approver_comment`, `buyer_name` (AssignHistory hiện hành theo send_company/brand/manufacture), `products[] {product_id, code, product_name, model_name, manufacture_name, all_barcodes, unit_id, unit_name, price, note, order_company, order_company_request_qty, request_qty, details[{customer_id, customer_code, customer_name, request_qty, date_needed, note}]}`, `can_edit`, `can_delete`, `erp_url`.

- [x] **Step 1: Viết test** (khuôn `InlandOrderRequestApiTest`):
  - `test_list_shows_own_requests_all_statuses` — A không quyền: phiếu A status 1, 2, 4 + phiếu B status 2 ⇒ A thấy đúng 3 phiếu của A.
  - `test_list_scope_department` — A scope 2 ⇒ thấy phiếu status 2 của B cùng phòng quản lý, không thấy C khác phòng.
  - `test_list_hides_other_users_drafts_even_with_group_scope` — A scope 4 ⇒ không thấy phiếu status 1 của B.
  - `test_list_buyer_sees_assigned` — A là `buy_employee_id` hiện hành (AssignHistory) của phiếu B status 3 ⇒ thấy.
  - `test_list_filters` — `code`, `status`, `brand_id`, `manufacture_id`, `send_company_id`, `product` (tên/mã dòng), `model_name`, `all_barcodes`, `customer_id`, `created_by`, `start_date`/`end_date` (theo `created_at`).
  - `test_show_forbidden_for_outsider` ⇒ 403; `test_show_flags` — status 1 chính chủ ⇒ `can_edit=true`; status 2 ⇒ false, `erp_url` kết thúc `/admin/orders/root_order_request/{id}/show`.
- [x] **Step 2: Chạy, FAIL.**
- [x] **Step 3: Cài.** Phạm vi port `searchByFilter` nhánh `_type=all` (ERP Model:326-471) qua `PermissionChecker` như `InlandOrderRequestService::applyScope` (dùng CurrentCompany như commit `060c59d5c`); luôn thêm `status != 1 OR created_by = me`. `canView` port Model:568-587.
- [x] **Step 4: PASS.** Kiểm thêm trên DB local: 1 role đang có `.view` ⇒ catalog-sync xong, gọi list bằng NV role đó trả > 0 dòng (ghi kết quả vào report).
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng — danh sách + chi tiết đọc bảng ERP`.

### Task 2: hrm-api — lập / sửa / xoá nháp / form-data / min-date

**Files:**
- Create: `Modules/Sale/Http/Requests/OrderRequest/{OrderRequestStoreRequest,OrderRequestUpdateRequest}.php`
- Create: `Modules/Sale/Services/OrderRequest/OrderRequestWriteService.php`
- Modify: controller, routes. Test: `OrderRequestApiTest.php`

**Interfaces:**
- Consumes: Task 1 entity, `canEdit`, `findEditable`.
- Produces:
  - `OrderRequestWriteService::store(array $data): RootOrderRequest`, `update(int $id, array $data): RootOrderRequest`, `destroy(int $id): void`; gọi `OrderRequestNotifier::notifyDepartmentApprovers(RootOrderRequest): int` (Task 3) **sau commit** khi status = 2.
  - `OrderRequestService::minDateFor(int $manufactureId, int $companyId): string` (Y-m-d; ngày cần phải > giá trị này).
  - Route: `POST /`, `PUT /{id}`, `DELETE /{id}`, `GET /form-data` (brands, companies, mặc định `send_company_id` = công ty đang làm), `GET /manufacture-info?manufacture_id=&send_company_id=&brand_id=` ⇒ `{min_date, min_date_label (d/m/Y), receiver_name, buyer_name}`.
  - Payload: `status (1|2), brand_id, manufacture_id, send_company_id, note, products[{product_id, unit_id, note, order_company (bool), order_company_request_qty, details[{customer_id, request_qty, date_needed (Y-m-d), note}]}]`.

- [x] **Step 1: Viết test:**
  - `test_store_draft_writes_erp_tables` — status 1 ⇒ 201; `code` khớp `/^PDH-\d{5,}$/`; `company_id/department_id/part_id/created_by/updated_by` của người lập; product `is_root=1`, chụp `product_name, code, model_id, model_name, manufacture_id, manufacture_name, origin_id, origin_name, all_barcodes, unit_name`; `request_qty = root_request_qty = Σ details`; `qty = adjusted_qty = 0`; detail chụp `customer_name, customer_code`, `request_qty = root_request_qty`, `qty = 0`, `root_order_request_id`.
  - `test_store_price_uses_company_price_type_1` — `price` = cách tính của `InlandOrderRequestWriteService::syncProducts` (giá loại 1 theo ĐVT, công ty = `company_id` phiếu).
  - `test_send_sets_department_received_and_detail_status` — status 2 ⇒ `department_received_time` có, mọi detail `status = 1`.
  - `test_send_requires_buyer_assignment` — không có AssignHistory (company = send_company_id, brand, manufactures_id, `employee_date_to IS NULL`, mới nhất) có `buy_employee_id` ⇒ 422 câu ERP; status 1 thì không kiểm.
  - `test_store_validates` — thiếu `brand_id`/`manufacture_id`/`send_company_id` ⇒ 422; `products` rỗng ⇒ 422; `request_qty` 0 ⇒ 422, 1 ⇒ OK, 1000000000 ⇒ 422; `date_needed` = min_date ⇒ 422 với câu "Không được nhỏ hơn ngày …"; trùng KH trong 1 mã ⇒ 422; `note` 256 ký tự ⇒ 422.
  - `test_brand_mismatch_rejected_before_write` — 1 mã khác thương hiệu ⇒ 422 câu ERP, không có dòng nào được ghi.
  - `test_order_company_without_details` — `order_company=1, order_company_request_qty=5, details=[]` ⇒ OK; `order_company=0, details=[]` ⇒ 422; `order_company=1, qty=0` ⇒ 422.
  - `test_min_date_without_kpi` — hãng không có `kpi_sales` công ty ⇒ min_date = hôm nay.
  - `test_update_recreates_lines` + `test_old_erp_draft_editable` (phiếu insert thô status 1).
  - `test_update_and_delete_rejected_when_not_draft_or_not_owner` ⇒ 403, số dòng con không đổi.
  - `test_stale_update_rejected_after_status_change` — nạp phiếu status 1, đổi DB sang 2 trước khi gọi PUT ⇒ 422 "Phiếu đã được gửi/xử lý, không sửa được".
  - `test_destroy_draft_removes_lines` — xoá cứng phiếu + products + details.
- [x] **Step 2: FAIL.**
- [x] **Step 3: Cài.** Rule chép ERP store/update (spec); `request_qty` tổng BE tự tính. Thứ tự: validate → kiểm thương hiệu từng mã (`products.brand_id`) → (gửi) kiểm phân công → `DB::transaction` { `lockForUpdate` + kiểm lại status 1 & chính chủ (update/destroy) → ghi header → `code` → `syncProducts` xoá-tạo-lại } → notify sau commit. `receiver_name`/`buyer_name` = deputy hãng (port ERP `ManufactureController::getDeputy` dòng 384) — chỉ hiển thị.
- [x] **Step 4: PASS** (cả Task 1).
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng — lập/sửa/xoá/gửi ghi bảng ERP`.

### Task 3: hrm-api — chuông TP (ERP) + hợp đồng chuông HRM do ERP ghi

**Files:** Create `Modules/Sale/Services/OrderRequest/OrderRequestNotifier.php`; Modify `app/Support/NotificationMeta.php` (`'YCĐH' => 'YC đặt hàng'`); Test.

**Interfaces:** `OrderRequestNotifier::notifyDepartmentApprovers(RootOrderRequest $m): int` (lỗi `Log::warning`, trả 0). Hằng `ERP_SHOW_URL = '/admin/orders/root_order_request/%d/show'`, `HRM_SHOW_URL = '/sale/order-requests/%d'`, `APPROVE_PERMISSION = 'purchase.phieu_yeu_cau_dat_hang_truong_phong.approve'`.

- [x] **Step 1: Test:**
  - `test_send_notifies_department_approvers_on_erp_bell` — B có quyền TP + quản lý phòng A, cùng công ty; D có quyền nhưng không quản lý; E quản lý nhưng khác công ty ⇒ đúng 1 dòng cho B: `notifiable_type='App\Employee'`, `type='App\Notifications\SystemNotification'`, `data.url` = ERP show, `data.content` = câu Global Constraints, `data.created_by` = A.
  - `test_inactive_manager_not_notified`, `test_draft_save_sends_nothing`, `test_send_succeeds_when_no_recipients`.
  - `test_erp_written_hrm_bell_row_renders` — insert dòng dạng `HrmBell::buildData('YCĐH', 'Đã duyệt', <code>, 'TP duyệt: …', HRM_SHOW_URL, 'rootOrderRequest', id, sender)` ⇒ API chuông HRM người lập trả `prefix='YCĐH'`, `url` đúng (khuôn test 692-711 của `InlandOrderRequestApiTest`).
- [x] **Step 2: FAIL. Step 3: Cài** — chép `InlandOrderRequestNotifier::recipients` rồi chỉnh theo ERP `NotificationHelper::sendNotifyWithPermission(..., true)` (đọc `ERP app/Helpers/NotificationHelper.php:133-152` để chốt: cùng công ty người lập, quản lý phòng qua `employee_manage_departments`, KHÔNG có nhánh bộ phận nếu ERP không có). **Step 4: PASS.**
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng — báo TP duyệt trên chuông ERP`.

### Task 4: hrm-api — tồn bán được + hàng đang về (chỉ đọc)

**Files:** Create `Modules/Sale/Services/OrderRequest/ArrivingQtyReader.php`; Modify controller/route `POST /order-requests/product-stocks`; Test.

**Interfaces:** `ArrivingQtyReader::tonFor(int $companyId, int $productId): float` — port tối thiểu chuỗi ERP `app/Services/Warehouse/ArrivingQtyService::tonFor → rowFor → perProductSql → perCompanySql…` (chỉ nhánh 1 sản phẩm, KHÔNG port buildFullMap/popup). Route body `{product_ids[], warehouse_id?, warehouse_group_id?}` ⇒ `[{product_id, in_stock, prepick_qty, stock_incoming}]`; tồn lấy từ `Modules/Assign/Services/StockService` nếu cho cùng số ERP `WarehouseInfosController::stockOfProducts`, nếu không thì port truy vấn đó. Công ty = công ty đang làm của người gọi (như ERP).

- [x] **Step 1: Test** `test_arriving_matches_erp_golden` — bảng golden ≥ 20 cặp (company, product) có `ton > 0` lấy bằng ERP tinker local (`php artisan tinker` với env DB override, gọi `app(ArrivingQtyService::class)->tonFor(c,p)`) lưu vào fixture test; HRM trả đúng từng số. `test_product_stocks_shape`.
- [x] **Step 2: FAIL. Step 3: Cài. Step 4: PASS.**
- [x] **Step 5: Commit** `feat(sale): YC đặt hàng — tồn bán được + hàng đang về`.

### Task 5: hrm-client — danh sách + menu

**Files:** Create `pages/sale/order-requests/index.vue`; Modify `components/subsystem-menu/sale-hub.js:187` — chuỗi `'YC đặt hàng'` → `{ n: 'YC đặt hàng', link: '/sale/order-requests' }` (giữ `n`).

- [x] **Step 1:** Dựng theo `pages/sale/inland-order-requests/index.vue`. Cột: STT, Mã phiếu (link), Thương hiệu, Hãng, Công ty tiếp nhận, Người lập, Phòng, Ngày lập, TP duyệt + ngày, Người tiếp nhận + ngày, Trạng thái (badge), Hành động. Bộ lọc như Task 1 `test_list_filters`. Hành động Sửa → Xoá (`BaseConfirmModal`) khi `can_edit/can_delete`; "Mở trên ERP" khi status ≠ 1. Nút "Thêm mới".
- [x] **Step 2: Playwright local** (skill run-hrm): menu Sale → "YC đặt hàng" mở trang; lọc "Chờ TP duyệt" chỉ còn status 2. Ảnh vào scratchpad.
- [x] **Step 3: lint. Step 4: Commit** `feat(sale): YC đặt hàng — màn danh sách`.

### Task 6: hrm-client — form lập / sửa

**Files:** Create `pages/sale/order-requests/add.vue`, `_id/edit.vue`, `components/OrderRequestForm.vue` (tách `OrderRequestProductRow.vue` nếu form > ~600 dòng).

**Interfaces:** Consumes Task 2 payload + `form-data` + `manufacture-info`, Task 4 `product-stocks`, Task 1 detail JSON.

- [x] **Step 1:** Đầu phiếu: Thương hiệu (bắt buộc; đổi ⇒ xác nhận rồi xoá hết hàng + hãng), Hãng (read-only, gán từ mã đầu tiên), Công ty tiếp nhận (bắt buộc, mặc định công ty đang làm), Người nhận đơn / Người mua (hiển thị từ `manufacture-info`), Kho / nhóm kho xem tồn (mặc định nhóm mặc định), Ghi chú ≤255. Bảng hàng: picker hàng HRM (như form mua ngoài) lọc theo thương hiệu; chặn trùng mã, khác thương hiệu/hãng; mỗi mã: ĐVT, Giá (hiển thị, en-US), Tồn bán được (`in_stock / hệ số ĐVT`), Hàng đang về, Đặt tồn kho (checkbox) + SL, Ghi chú; N dòng KH (`V2BaseSelectRemote`) / SL / Ngày cần (`V2BaseDatePicker`, min = `min_date` + 1) / Ghi chú; chặn trùng KH trong mã; nút "Áp dụng tất cả" chép danh sách KH của mã hiện tại sang mọi mã. Footer V2: **Lưu và gửi** (2) → **Lưu** (1) → Huỷ. Lỗi 422 inline theo key `products.i.details.j.field`; `unsavedChangesMixin`; chống bấm đúp. Thành công ⇒ về danh sách.
- [x] **Step 2: Playwright:** lập 2 mã (1 mã chỉ đặt tồn kho) 2 KH ⇒ Lưu ⇒ sửa ⇒ Lưu và gửi ⇒ danh sách "Chờ TP duyệt"; ngày cần = min_date ⇒ lỗi dưới ô; hãng chưa phân công ⇒ toast câu ERP.
- [x] **Step 3: lint. Step 4: Commit** `feat(sale): YC đặt hàng — form lập/sửa`.

### Task 7: hrm-client — chi tiết

**Files:** Create `pages/sale/order-requests/_id/index.vue`.

- [x] **Step 1:** Thông tin phiếu (mã, trạng thái badge, thương hiệu, hãng, công ty tiếp nhận, người lập, phòng, ngày lập, ghi chú), ý kiến TP + người/ngày, ý kiến/người tiếp nhận + ngày, bảng hàng/KH (gộp dòng theo mã). Footer: Sửa → Xoá khi `can_edit`; "Mở trên ERP" khi status ≠ 1 (tooltip "Duyệt, tiếp nhận, in phiếu thực hiện trên ERP").
- [x] **Step 2: Playwright:** status 2 ⇒ không Sửa/Xoá, có "Mở trên ERP"; status 1 chính chủ ⇒ có Sửa/Xoá.
- [x] **Step 3: lint. Step 4: Commit** `feat(sale): YC đặt hàng — màn chi tiết`.

### Task 8: ERP — chặn ghi + nút trỏ HRM

**Files:** Modify `app/Http/Middleware/ProductMovedToHrm.php`, `routes/web.php:2588-2608`, `resources/views/errors/moved_to_hrm.blade.php`, `resources/views/orders/root_order_requests/{index,approver_index,department_approver_index}.blade.php` (nút Thêm mới), `RootOrderRequestController::searchData` (Ctl:71-174, nút Sửa/Xoá), `show.blade.php` (nút Sửa nếu có).

- [x] **Step 1:** TARGETS `'root-order-list' => '/sale/order-requests'`, `'root-order-create' => '/sale/order-requests/add'`, `'root-order-edit' => '/sale/order-requests/{id}/edit'`; hằng nhóm `ROOT_ORDER_TARGETS` (edit thiếu id lùi về list, như nhóm inland); câu: "Lập và sửa Phiếu yêu cầu đặt hàng đã chuyển sang HRM. Các bước TP duyệt, tiếp nhận, đặt hàng vẫn làm trên ERP."
- [x] **Step 2:** Middleware `productMovedToHrm:root-order-create` cho `create`, `store`; `root-order-edit` cho `edit`, `update`, `delete`. Không đụng route khác.
- [x] **Step 3:** Nút Thêm mới mọi view danh sách = `ProductMovedToHrm::buildHrmUrl('root-order-create')`; `searchData` thay Sửa/Xoá bằng link "Sửa trên HRM" (`buildHrmUrl('root-order-edit', ['id' => …])`) khi `canEdit()`.
- [x] **Step 4: Kiểm local** (env DB override): `php artisan route:list | grep root_order_request` thấy middleware; mở create ⇒ trang "đã chuyển sang HRM"; POST store AJAX ⇒ JSON 403 `redirect_url`; index / show / departmentApprove / approve vẫn chạy.
- [x] **Step 5: Commit** (develop_02) `feat: YC đặt hàng — chuyển lập/sửa sang HRM`.

### Task 9: ERP — chuông HRM cho người lập

**Files:** Modify `RootOrderRequestController.php` — `departmentApprove` (~459-467), `approve` (~728-734). Test: thêm case vào `tests/Unit/HrmBellBuildTest.php` nếu cần prefix mới.

- [x] **Step 1:** Sau mỗi `NotificationHelper::sendNotify($object->created_by, …)` (GIỮ nguyên chuông ERP) gọi `HrmBell::notifyEmployee($object->created_by, 'YCĐH', <action>, $object->code, <note>, '/sale/order-requests/' . $object->id, 'rootOrderRequest', $object->id)`: TP 3 ⇒ `'Đã duyệt'`, note `HrmBell::approverNote(Auth::user()->fullname, null, null, 'TP duyệt')`; TP 1 ⇒ `'Không duyệt'`, note `approverNote(…, 'Lý do', department_approver_comment, 'TP')`; tiếp nhận 4 ⇒ `'Đã duyệt'`, `approverNote(…, null, null, 'Người tiếp nhận')`; trả lại 1 ⇒ `'Không duyệt'`, `approverNote(…, 'Lý do', approver_comment, 'Người tiếp nhận')`. Gọi sau `DB::commit()` hoặc chấp nhận trong transaction như inland (chép đúng cách inland đã làm).
- [x] **Step 2: Kiểm local:** TP duyệt phiếu do HRM lập ⇒ chuông HRM người lập có dòng mở `/sale/order-requests/{id}`; không duyệt có lý do ⇒ lý do hiện. (Redis phải chạy cho departmentApprove.)
- [x] **Step 3: Commit** (develop_02) `feat: YC đặt hàng — báo người lập trên chuông HRM`.

### Task 10: Kiểm cả luồng + tài liệu

- [x] **Step 1:** Local 1 vòng: HRM lập + gửi ⇒ ERP TP thấy chuông, duyệt ⇒ XNK tiếp nhận (1 mã đặt trong nước) ⇒ HRM chi tiết "Đã tiếp nhận", chuông HRM đủ 2 dòng; ERP create/edit bị chặn. So 1 phiếu HRM lập với 1 phiếu ERP lập (trước khi chặn, cùng đầu vào, trên nhánh cũ) — cột chụp + `price` khớp.
- [x] **Step 2:** Chạy lại `OrderRequestApiTest` + `InlandOrderRequestApiTest` (NotificationMeta + catalog đổi) ⇒ PASS.
- [x] **Step 3:** Cập nhật `HRM/.plans/STATUS.md` + memory, báo user. KHÔNG push.

### Checkpoint — 2026-11-20 17:20 (wrap up tự động)
Vừa hoàn thành: đủ 10 task SDD + review cuối (sửa 2 lỗi: product-stocks gộp truy vấn 33,6s→~1s; chặn mã khác hãng, ĐVT không thuộc mã, mã trùng, ghi chú dòng KH ≤255). Chốt với user: A — bước TP duyệt ở lại ERP; HRM lập/sửa/nháp/gửi/xoá ghi thẳng `root_order_requests`. Tồn bán được + hàng đang về chép riêng cách tính ERP (khớp 40/40 & 37/37; hàm cũ HRM chỉ khớp 22/40). E2E local PDH-06917 → PDHTN-04132 (erp_hrm_check; bước ERP chạy thẳng code, không qua trình duyệt do SSO). Test 35 + 32 xanh.
Commit local: hrm-api develop b3935897d..5db008e48 (8 commit), hrm-client develop a745ffa6f..0f314e2d8 (7 commit), ERP develop_02 `f3a36d0852` `0280648943`. ĐÃ PUSH cuối ngày (cherry-pick riêng, hash origin khác local): hrm-api origin/develop ad77d5ff1..`8c6b2fb70`, hrm-client origin/develop ..`ab58b07f8`, ERP origin/develop_02 `0280648943`.
Đang dở: —
Bước tiếp theo: gộp gop_db khi user báo. Để lại: ERP danh sách bỏ nút Xoá (ghi HDSD); ERP duyệt không khoá dòng có thể sinh trùng phiếu con (bug sẵn ERP, tách việc riêng).
Blocked: —
