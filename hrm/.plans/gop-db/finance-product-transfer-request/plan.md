# Plan — Phiếu yêu cầu chuyển hàng (ERP → HRM)

> **For agentic workers:** dùng superpowers:subagent-driven-development hoặc superpowers:executing-plans, thực hiện task theo checkbox.
> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Spec: `docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md`

**Goal:** Port trọn màn "Phiếu yêu cầu chuyển hàng" ERP sang HRM phân hệ Tài chính → nhóm Xuất hàng; HRM là bản thay thế lâu dài, 2 cổng song song cùng bảng.

**Architecture:** BE `Modules/Finance` (ApiController + Service + FormRequest + Resource, khuôn CompanyAccount/Service đã port); FE Nuxt2 V2Base `pages/finance/product-transfer-requests` (list + form trang riêng + detail). Không đổi schema, không migration.

## Ràng buộc toàn cục (mọi task ngầm bao gồm)

- Nhánh `gop_db` cả 2 repo. **KHÔNG commit/push khi user chưa yêu cầu.**
- KHÔNG dùng `mysql2`/`DB_DATABASE_SECOND`; KHÔNG khai `$connection`; `auth()->user()->id` = id nhân viên duy nhất.
- KHÔNG migration, KHÔNG sửa `PermissionsTableSeeder` (quyền dùng lại của ERP, chỉ UPDATE tay DB).
- BE: rethrow `ValidationException`; migration-PHPDoc không áp dụng (không có migration).
- FE: trước khi code đọc skill `button-convention`, `modal-popup`, `list-page`, `print-page`; validate inline `is-invalid`+`invalid-feedback`+`touched`; áp 4 bài học phân trang finance-account-catalog; `$nextTick` trước `$bvModal.show()`.
- Nguồn port ERP: `D:\laragon\www\erp` — model `app\Model\Warehouse\ProductTransferRequest*.php`, controller `app\Http\Controllers\Warehouse\ProductTransferRequestsController.php`, view `resources\views\warehouse\product_transfer_requests\`.
- Sau mỗi file PHP: `php -l`. Verify cuối phase bằng HTTP thật/browser.

---

## Phase 1 — BE nền: entities + list/show + quyền

### Task 1.1 — 3 Entities ✅ khi php -l sạch + tinker load được STATUSES
**Files (Create):**
- `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php`
- `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequestProduct.php`
- `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequestProductDetail.php`

Port từ ERP `app\Model\Warehouse\ProductTransferRequest.php` (533 dòng) + 2 model con:
- [x] `ProductTransferRequest`: `$table='product_transfer_requests'`; hằng `STATUSES` 13 trạng thái (id/name/type — copy nguyên :20-86); fillable đủ cột (code, status, note, attachments, comment, approver_id, approved_time, product_export_request_id, employee_created_request_id, company_id, department_id, part_id, created_by, updated_by).
- [x] Quan hệ: `products()` hasMany Product(parent_id); `approver()`, `employee_create()` belongsTo `Modules\Human\Entities\Employee`; `company()`, `department()`.
- [x] Boot (port :88-114): `creating/created` set `created_by`, `employee_created_request_id`, `company_id`, `department_id`, `part_id` từ user login (lấy qua employee_infos như bank-account-catalog); `deleting` xóa cascade details → products.
- [x] `generateCode()` port nguyên :317 (`PYCCH-` + str_pad id, đối chiếu code ERP thật khi port — 2 cổng phải ra cùng dãy số).
- [x] `canView()/canApprove()/canEdit()/canDelete()` port :322-339: canView = Super admin ∥ người tạo ∥ (quyền "Kế toán kho" + cùng company_id); canApprove = status==2 && quyền "Kế toán kho" && cùng company_id; canEdit = canDelete = status==3 && created_by==user id. Check quyền qua spatie `hasPermissionTo`/`can` như các màn Finance đã port (Super admin role 18 — xem memory gop_db).
- [x] `ProductTransferRequestProduct`: fillable (parent_id, product_id, product_name, unit_id, unit_name, model_id, model_name, brand_id, brand_name, code, qty, price, allocated_qty); quan hệ `customers()` hasMany Detail(parent_id), `parent()`, `product()`, `unit()`.
- [x] `ProductTransferRequestProductDetail`: fillable (parent_id, customer_id, customer_name, qty, allocated_qty, date_needed, note).

### Task 1.2 — `searchByFilter` (phạm vi theo cấp + filter)
**Files (Modify):** `ProductTransferRequest.php` (thêm method) · tham chiếu ERP :165-275

- [x] Port nguyên thứ tự nhánh quyền: `Xem yêu cầu chuyển hàng theo tổng công ty` (thấy hết) → `...theo công ty` (`company_id` = công ty user) → `...theo phòng ban` (department_id IN (EmployeeManageDepartment của user + phòng mình) OR created_by=mình) → `...theo bộ phận` (part_id IN (EmployeeManagePart + bộ phận mình) OR created_by=mình) → mặc định `created_by=mình`. Bảng `EmployeeManageDepartment`/`EmployeeManagePart` — tìm model tương ứng trên DB gộp (bảng ERP `employee_manage_departments`/`employee_manage_parts`), tạo entity tối giản trong module nếu chưa có.
- [x] Luôn append: `where(created_by = mình OR status != 3)` (ẩn nháp người khác, :269-272).
- [x] Filter từ request: `code` like, `status`, `product_name` (whereHas products: mã HOẶC tên like), `created_by`, `approver`, `start_date`/`end_date` theo `created_at`, `company_id`, `department_id`. Sort `created_at DESC`. Eager load `employee_create`, `approver`, đếm/paginate chuẩn khuôn Finance.
- [x] Trả kèm cờ `is_big_boss/is_boss/is_manager` (user có quyền 878/879/880) cho FE bật filter công ty/phòng ban — đặt trong response meta của index (xem Task 1.4).

### Task 1.3 — Resources
**Files (Create):**
- `Modules/Finance/Transformers/ProductTransferRequestResource/ProductTransferRequestListResource.php`
- `Modules/Finance/Transformers/ProductTransferRequestResource/ProductTransferRequestDetailResource.php`

- [x] List: id, code, created_by + tên người tạo, created_at (d/m/Y), approver_id + tên người tiếp nhận, approved_time (d/m/Y), status + status_name + status_type (map STATUSES), `is_can_edit`, `is_can_delete`, `is_can_approve` (gọi canXxx).
- [x] Detail: thông tin chung + `comment` + `attachments` (tách chuỗi `", "` → mảng {name, url}) + products (kèm details khách hàng, unit_options nếu cần cho edit) + cờ canXxx + status. Cột `allocated_qty` các cấp (FE hiện "Được nhận" khi status=12).

### Task 1.4 — Controller + Service + Routes (index/show)
**Files:**
- Create: `Modules/Finance/Http/Controllers/V1/ProductTransferRequestController.php`, `Modules/Finance/Services/ProductTransferRequestService.php`
- Modify: `Modules/Finance/Routes/api.php` (group mới trong `/v1/finance`)

- [x] Controller extends `ApiController` Finance; Service theo khuôn `CompanyAccountService`.
- [x] Routes (đăng ký trước 2 action, phase sau bổ sung dần):
```php
Route::group(['prefix' => '/product-transfer-requests'], function () {
    Route::get('/', [ProductTransferRequestController::class, 'index']);
    Route::get('/export', [ProductTransferRequestController::class, 'export']);      // Phase 5
    Route::get('/{id}', [ProductTransferRequestController::class, 'show']);
    Route::post('/', [ProductTransferRequestController::class, 'store']);            // Phase 3
    Route::put('/{id}', [ProductTransferRequestController::class, 'update']);        // Phase 3
    Route::delete('/{id}', [ProductTransferRequestController::class, 'destroy']);    // Phase 3
    Route::post('/{id}/reject', [ProductTransferRequestController::class, 'reject'])
        ->middleware('checkPermission:Kế toán kho');                                  // Phase 4
    Route::delete('/{id}/files', [ProductTransferRequestController::class, 'deleteFile']); // Phase 3
    Route::get('/{id}/print-data', [ProductTransferRequestController::class, 'printData']); // Phase 5
});
```
  (index/store/update/destroy KHÔNG gắn checkPermission — ERP không gate, phạm vi chặn trong searchByFilter/canXxx; route `/export` phải khai TRƯỚC `/{id}`.)
- [x] `show`: findOrFail → `canView()` fail trả 403 message "Bạn không có quyền xem phiếu này".
- [x] `index` meta trả `is_big_boss/is_boss/is_manager` + danh sách STATUSES cho FE render select.

### Task 1.5 — Quyền: kiểm tra DB + SQL deploy ✅ (D3, 2026-08-05)
- [x] Query DB gộp — id THẬT trên `gop_db` là `100878/100879/100880/100881` (offset +100000, KHÔNG
  phải `878/879/880` literal — literal đó là 3 quyền khác, xem cảnh báo ở mục SQL DEPLOY). Quyền
  "theo bộ phận" (100881) CÓ tồn tại (khác giả định ban đầu).
- [x] Đã chạy tay local: `UPDATE permissions SET \`type\` = 8 WHERE id IN (100878, 100879, 100880, 100881);` — xác nhận type NULL → 8 cả 4 dòng; KHÔNG đổi 100080 "Kế toán kho".
- [x] Đối chiếu type=8 = tab Tài chính (seeder dòng 21-23 + quyền 1107/1108 cùng type=8 trên DB thật). Role đang gán (`role_has_permissions`) không đụng tới (chỉ UPDATE bảng `permissions`, không đổi pivot). Mirror `employee_has_roles` model_type: CHƯA đầy đủ (1252 `App\Employee` vs 439 HRM) nhưng KHÔNG cần chạy cho feature này — entity D1 query pivot trực tiếp, không qua spatie Eloquent. Chi tiết: `sdd/D3-report.md`.

### Verify Phase 1
- [x] `php -l` toàn bộ file mới; route list có nhóm mới.
- [x] HTTP thật: login 3 user đại diện (có 878 / có 880 / không quyền) → GET index đối chiếu số phiếu với query SQL tương ứng; GET show phiếu người khác với user thường → 403; phiếu nháp người khác không xuất hiện trong list.

---

## Phase 2 — FE danh sách

### Task 2.1 — `pages/finance/product-transfer-requests/index.vue`
Khuôn: màn Finance list đã port (`pages/finance/accounts/index.vue` — có phân trang chuẩn) + style V2Base.

- [x] Cột: STT · Mã yêu cầu (link `/finance/product-transfer-requests/{id}`) · Người tạo · Ngày tạo · Người tiếp nhận · Ngày tiếp nhận · Trạng thái (badge màu theo `status_type`) · Hành động. (D4)
- [x] Bộ lọc: Mã yêu cầu (text) · Trạng thái (select STATUSES từ meta) · Tên/mã hàng hóa (text) · Người tạo, Người tiếp nhận (select nhân viên — dùng dropdown nhân viên sẵn có của khuôn Finance) · Khoảng ngày tạo (2 ô single date — V2BaseDatePicker không nhận Array, param vẫn start_date/end_date) · Công ty/Phòng ban chỉ render khi meta `is_big_boss/is_boss/is_manager`. (D4)
- [x] Nút: **Thêm mới** → `/finance/product-transfer-requests/create` · **Xuất Excel** (disabled, Phase 5 gắn handler). (D4)
- [x] Hành động mỗi dòng theo cờ resource: Sửa (`is_can_edit`) · Xóa (`is_can_delete`, confirm modal theo skill modal-popup, DELETE wire sẵn chờ BE Phase 3) · Tổng hợp (`is_can_approve`) — Phase 4 gắn handler · In yêu cầu (luôn hiện) — Phase 5. (D4)
- [x] Store API call theo khuôn `docs/shared.md` (V2Base + api store). Meta đọc từ `additional()` phẳng cấp 1. (D4)

### Task 2.2 — Gắn menu
**Files (Modify):** `hrm-client/components/subsystem-menu/finance.js:134`
- [x] `{ label: 'Phiếu yêu cầu chuyển hàng', link: '/finance/product-transfer-requests' }` — giữ nguyên vị trí trong nhóm Xuất hàng. Grep xác nhận link chỉ ở finance.js. (D4)

### Verify Phase 2
- [x] Browser: màn list hiện dữ liệu thật, lọc, phân trang, badge, nút theo quyền — PASS D12 (Playwright toàn luồng + ma trận quyền 6 nhóm user).

---

## Phase 3 — Form tạo/sửa (nặng nhất)

### Task 3.1 — API phụ trợ form (BE)
**Files (Modify):** Controller/Service/Routes Phase 1. Nguyên tắc: TÁI DÙNG endpoint sẵn có, chỉ tạo mới khi thiếu.

- [x] Khảo sát + chốt từng nguồn (D5 — chi tiết interface trong sdd/D5-report.md, là hợp đồng cho Task 3.4):
  - Tìm hàng hóa (popup): TÁI DÙNG `GET customer-care/services/search-products` (gửi kèm `page` mới có unit_name/list_price). KHÔNG tạo route mới.
  - ĐVT theo hàng + hệ số + giá niêm yết: route mới `GET .../products/{id}/units` (sort is_base DESC; giá = round(price*coeff/1000)*1000 chỉ khi coeff != 1 — đúng ERP).
  - Tồn kho ("Xem tồn"): route mới `GET .../stock?stock_query=&product_ids[]=` — port đúng getStockQty/getAccountingStockDetail (fallback acc-warehouse, pending, in_stock=max(0,min(available,in_warehouse))).
  - Kho/nhóm kho: route mới `GET .../stock-options` (getByGroupAll: skip nhóm rỗng, prefix `|-- `; default_value có thể null → FE fallback chọn option đầu).
  - Khách hàng: TÁI DÙNG `GET master-data/customers/search` (⚠️ đổi so với plan gốc — assign/customers/search đã chuyển sang module MasterData 2026-08-04).
- [x] Route tĩnh khai TRƯỚC `/{id}`; query connection mặc định; response gọn. `php -l` sạch + verify HTTP thật + đối chiếu SQL (stock khớp 2 kho, options 25 khớp). (D5)

### Task 3.2 — FormRequest validate
**Files (Create):** `Modules/Finance/Http/Requests/ProductTransferRequest/ProductTransferRequestRequest.php`

- [ ] Rules:
```php
'status'   => 'required|numeric|in:2,3',
'note'     => 'nullable|max:255',
'products' => 'required|array|min:1',
'products.*.product_id' => 'required|exists:products,id',
'products.*.unit_id'    => 'required|exists:units,id',
'products.*.details'    => 'required|array|min:1',
'products.*.details.*.customer_id' => 'required|exists:customers,id',
'products.*.details.*.qty'  => 'required|numeric|min:1|max:999999999',
'products.*.details.*.note' => 'required|max:255',
'products.*.details.*.date_needed' => 'required|date',
'attachments'   => [store: 'required|array|min:1'][update: 'nullable|array'],
'attachments.*' => 'mimes:pdf',
```
- [x] `withValidator`: (a) chặn trùng `product_id` ("Hàng hóa bị trùng trong phiếu"); (b) rule nới #6 date_needed — update: detail id khớp + ngày không đổi → bỏ check. (D6)
- [x] Message tiếng Việt đủ từng field kể cả nested. Rules đúng nguyên văn plan; store/update phân biệt qua route('id'). (D6)

### Task 3.3 — Store / Update (Service) + S3
**Files (Modify):** `ProductTransferRequestService.php`, Controller; tham chiếu ERP controller :135-339

- [x] `store`: DB::transaction — uniqid tạm → S3 putFiles → attachments nối ", " → generateCode → syncProducts → notifyAccountants stub (TODO D9). (D6)
- [x] `syncProducts` port ERP :277-315: xóa hết tạo lại, denormalize, qty cha = tổng con. **Giá lưu THÔ** product_unit_prices price_type 1 (đúng gốc ERP, không áp hệ số). (D6)
- [x] `update`: canEdit 403 "Chỉ sửa được phiếu Đang tạo do chính bạn lập" → append attachments → syncProducts → notify stub. (D6)
- [x] `destroy`: canDelete 403 → delete (boot cascade, bọc transaction). (D6)
- [x] `deleteFile`: canEdit → CmcS3Helper::deleteFile (S3 thật, không unlink public_path) → gỡ URL khỏi chuỗi. (D6)

### Task 3.4 — FE form: create + edit
**Files (Create):**
- `pages/finance/product-transfer-requests/create.vue`
- `pages/finance/product-transfer-requests/_id/edit.vue`
- `pages/finance/product-transfer-requests/components/ProductTransferRequestForm.vue` (dùng chung)
- `pages/finance/product-transfer-requests/components/ProductSearchModal.vue` (theo khuôn popup hàng hóa services-catalog `pages/customer-care/services/components/`)
- `pages/finance/product-transfer-requests/components/CustomerSearchModal.vue` (khuôn popup KH có sẵn của luồng assign)

- [x] Khối thông tin chung: Ngày lập/Người lập disabled · Ghi chú · Upload PDF multi; xóa file cũ gọi `DELETE /{id}/files` với `file_url` qua QUERY param (axios cũ không gửi body DELETE — BE đọc được sẵn). (D7)
- [x] Dropdown "Xem tồn": stock-options (fallback option đầu khi default null) → API stock; đổi kho nạp lại; tồn quy đổi theo unit_coefficient. (D7)
- [x] Bảng hàng hóa: ProductSearchModal (chặn trùng 2 lớp) · select ĐVT đổi giá client-side · Giá niêm yết readonly · SL tồn · xóa dòng confirm. (D7)
- [x] Dòng con KH: CustomerSearchModal (master-data/customers/search) · SL 1–999.999.999 · Ngày cần (dòng mới disable ≤ hôm nay, dòng cũ giữ ngày quá khứ) · Ghi chú required · Tổng cộng = tổng SL con. (D7)
- [x] Submit: Lưu=3 / Lưu & Gửi duyệt=2 / Hủy confirm dirty; multipart (products = JSON string, update = POST+_method=PUT, detail giữ nguyên kèm id); 422 nested map đúng ô + scroll; touched sau submit đầu. (D7)
- [x] Edit: load DetailResource; guard is_can_edit/403/404 → toast + redirect list; reload sau save. (D7)

### Verify Phase 3
- [x] HTTP: store thiếu từng field → 422 đúng message; store trùng product → 422; store đủ → DB có 3 tầng bản ghi + code `PYCCH-` nối tiếp dãy ERP; update phiếu nháp người khác → 403; update đổi hàng → bảng con recreate đúng; xóa nháp → cascade sạch; deleteFile gỡ đúng 1 URL + object S3 xóa thật. (D6 — data test đã dọn)
- [x] Browser (smoke D7): tạo phiếu nháp qua UI thật → edit → update → xóa file → xóa phiếu, console 0 error, data dọn sạch. Đối chiếu 2 cổng ERP + test tồn >0 (user công ty 1) dời D12. (D7)

---

## Phase 4 — Chi tiết + Không duyệt + Tổng hợp + Notification

### Task 4.1 — Màn chi tiết
**Files (Create):** `pages/finance/product-transfer-requests/_id/index.vue`

- [x] Read-only toàn bộ + file đính kèm (target=_blank) + bảng hàng; cột "Được nhận" CHỈ khi status==12 (mirror show.blade ERP). (D8)
- [x] Khối "Ghi chú duyệt": textarea khi `is_can_approve` / `comment` readonly. (D8)
- [x] Nút theo cờ: Không duyệt + Tổng hợp / Sửa / Quay lại (button-convention). (D8)

### Task 4.2 — Reject (Không duyệt)
**Files (Modify):** Controller/Service (BE), `_id/index.vue` (FE)

- [x] BE `reject`: ⚠️ BỎ middleware `checkPermission:Kế toán kho` — middleware CheckPermission hỏng trên gop_db (spatie getAllPermissions bỏ sót role model_type ERP, user Kế toán kho thật = 0 quyền); thay bằng `canApprove()` trong controller (chặt hơn: status==2 + quyền + company + bypass Super admin). Service set status=3/comment/approver_id/approved_time + updated_by, notifyCreator stub D9. Port đủ ERP :417-461. **CẦN TASK RIÊNG rà các route khác dùng checkPermission trên gop_db.** (D8)
- [x] FE: Không duyệt → validate inline touched trước → confirm modal → POST → toast + reload; 422/403 xử lý đúng. (D8)

### Task 4.3 — Notification 2 cổng
**Files (Modify):** Service (method `notifyAccountants`, `notifyCreator`)

- [x] Khảo sát (D9): chuông ERP ĐÃ VÔ HIỆU trên gop_db (Notification model chặn save + controller trả rỗng + bảng notifications mang cấu trúc HRM) → đích chuyển sang chuông HRM `EmployeeInfoService::sendNotification` (Redis publish + FCM + ghi DB), link `/finance/product-transfer-requests/{id}`.
- [x] Gửi duyệt (status 2): notifyAccountants → MỌI user có quyền "Kế toán kho" cùng company (query pivot 2 đường không lọc model_type — spatie sẽ trả 0 người; verify 13/13 khớp SQL độc lập). Nội dung giữ nguyên chữ ERP. (D9)
- [x] Reject: notifyCreator cho người tạo. Redis: dùng kênh sẵn có của EmployeeInfoService (user_notification_{id}). Notify trong transaction (vị trí như ERP), try/catch từng người nhận. ⚠️ Hệ quả: user thuần cổng ERP không còn thấy thông báo (chuông ERP tắt từ đợt gộp DB) — cần user/PO xác nhận. (D9)

### Task 4.4 — Nút Tổng hợp (mở ERP)
**Files (Modify):** `index.vue` (list) + `_id/index.vue`

- [x] Mở tab mới `ERP_URL + '/admin/warehouse/product_export_requests/create?product_transfer_request_id=' + id` — path xác nhận đúng từ routes/web.php ERP + show.blade.php:154. ⚠️ .env local thiếu ERP_URL (dev mở URL tương đối) — prod cần biến này. (D8)
- [x] Chỉ hiện khi `is_can_approve`; gắn cả nút TODO ở list. (D8)

### Verify Phase 4
- [x] HTTP: reject user thường → 403 (canApprove — middleware đã bỏ, xem Task 4.2); status≠2 → chặn; reject hợp lệ → status=3 + comment + approver + notification ghi DB. (D8 + D9 + D12)
- [x] Browser: nút Không duyệt/Tổng hợp đúng cờ; Tổng hợp mở đúng path ERP; người tạo nhận thông báo chuông HRM (chuông ERP đã tắt từ đợt gộp DB — xem Task 4.3). Reject click thật PASS D12.

---

## Phase 5 — In phiếu + Export Excel

### Task 5.1 — In phiếu (template 87)
**Files:** Create `pages/finance/product-transfer-requests/_id/print.vue`; Modify Controller/Service (`printData`)

- [x] BE: canView 403 → template 87 (ErpReportTemplate) → port accessor ERP + escape e() (an toàn hơn ERP) + addcslashes chống vỡ fillReport + fix bug Carbon::parse(null). Route print-data trước /{id}. (D10)
- [x] FE: _id/print.vue theo skill print-page (tbody.print-group chống vỡ rowspan, margin khớp ERP, auto print); nút In ở list + chi tiết. (D10)

### Task 5.2 — Export Excel danh sách
**Files:** Create `Modules/Finance/Exports/ProductTransferRequestExport.php`; Modify Controller/Service (`export`), FE `index.vue`

- [x] BE: searchByFilter không phân trang → `danh_sach_yeu_cau_chuyen_hang.xlsx` 7 cột + dòng filter ngày 3 nhánh (port ProductTransferRequestExportExcel ERP, khuôn AccountExport; blade mới finance::exports). ERP không gate permission export → HRM chỉ auth. (D11)
- [x] FE: nút Xuất Excel gửi toàn bộ filter, tải blob kèm Bearer (khuôn accounts). (D11)

### Verify Phase 5
- [x] In: phiếu 4 hàng × 7 KH đúng template 87, 0 placeholder sót, rowspan khớp; so accessor ERP từng biến. (D10 + D12; so bản in UI ERP skip — thiếu credential cổng ERP)
- [x] Export: file mở được (PhpSpreadsheet đọc lại), 1634/21/0 dòng khớp COUNT 3 kịch bản, tên trạng thái đúng STATUSES. (D11 + D12)

---

## Phase 6 — Verify tổng thể

- [x] Quyền: ma trận 6 nhóm user (100878/100879/100880/100881/KTK/không quyền) × 6 action — đối chiếu SQL độc lập. PASS. (D12)
- [x] Round-trip 2 cổng: PASS tầng dữ liệu (cùng bảng gop_db, verify SQL 2 chiều; ERP local erp.test:8080). ERP UI skip — thiếu credential đăng nhập cổng ERP. (D12)
- [x] Playwright toàn luồng PASS kể cả reject click thật + chuông HRM 2 chiều; console 0 error. (D12)
- [x] DB nguyên trạng: max_id 7359, count 3126, 0 row test còn lại (phiếu 7367-7376 + notif + S3 dọn 100%). (D12 + fix wave)
- [ ] Regression màn Finance cũ: SKIP — accounts/currencies/account-banks 404 với MỌI user (kể cả Super admin) do quyền web-guard chưa surface vào store.state.permissions = điều kiện môi trường gop_db CÓ SẴN, không phải regression của feature. Cần task riêng rà mapping quyền (gộp cùng task checkPermission D8). (D12)
- [x] `php -l` 10 file PHP + 1 blade sạch; 8 file .vue + finance.js parse sạch. (D12)

---

## SQL DEPLOY (chạy tay khi lên môi trường thật — đã chạy local, kết quả Task 1.5/D3)

⚠️ **ID literal 878/879/880 ở bản nháp cũ SAI** — đó là id gốc ERP. Trên DB gộp `gop_db`, mọi
permission ERP-port được đánh lại id **+100000** (đúng pattern feature trước — xem
sdd-progress services-catalog `101023-101025`). Đã verify: literal `878/879/880` trên `gop_db`
là 3 quyền HOÀN TOÀN KHÁC (thân nhân/tài khoản nhân viên, type=3) — nếu chạy nhầm sẽ hỏng phân
quyền màn khác. ID THẬT đã xác nhận + đã chạy:

```sql
-- 1) Hiện 4 quyền xem ở tab Tài chính màn Phân quyền HRM (type=8, đối chiếu seeder
--    PermissionsTableSeeder.php dòng 21-23 "8=Tài chính" + quyền tài chính có sẵn id 1107/1108).
--    Quyền "theo bộ phận" (100881) CÓ tồn tại trên gop_db (khác giả định ban đầu "có thể không có").
--    Đã chạy trên DB local (gop_db) 2026-08-05, xác nhận type NULL -> 8 cho cả 4 dòng.
UPDATE permissions SET `type` = 8 WHERE id IN (100878, 100879, 100880, 100881);
-- KHÔNG đổi id 100080 "Kế toán kho" (giữ type=NULL, group='Kế toán' như ERP).
```

Kiểm tra mirror `employee_has_roles.model_type`: đếm distinct trên `gop_db` cho `App\Employee`=1252
dòng vs `Modules\Timesheet\Entities\Employee`=439 dòng — mirror CHƯA đầy đủ (giống phát hiện
services-catalog Task 1.5), nhưng **KHÔNG cần chạy mirror cho feature này** vì entity
`ProductTransferRequest.php` (D1) đã chủ động query thẳng `employee_has_roles`/`role_has_permissions`
theo `employee_id` (không lọc `model_type`, không qua spatie Eloquent relation) — xem docblock đầu
file. Cần xem lại khi code Task 4.2 (route `reject` dùng middleware `checkPermission:Kế toán kho`)
— nếu middleware đó dùng spatie chuẩn (`can()`/`hasPermissionTo()`), có thể dính cùng vấn đề
model_type/guard mismatch, lúc đó mới cần quyết định mirror hay đổi cách check. Chi tiết đầy đủ:
`sdd/D3-report.md`.

---

## Phase 7 — Đồng nhất popup chọn hàng hóa với màn báo giá (yêu cầu user 2026-08-06)

### Task 7.1 — Thay ProductSearchModal riêng bằng QuotationProductSearchModal dùng chung
Lý do (user): popup chọn hàng của phiếu chuyển hàng phải dùng CHUNG popup màn báo giá (`pages/sale/quotations/components/QuotationProductSearchModal.vue` — trên gop_db màn báo giá là `/sale/quotations`) — sau này sửa 1 chỗ.

- [x] Form import QuotationProductSearchModal (goodsOnly + existingProducts + multi-select apply, map erp_product_id→product_id); ProductSearchModal.vue riêng ĐÃ XÓA (0 tham chiếu). Tab Hàng hóa vốn không có cột giá vốn → không cần ẩn giá. (D13)
- [x] Ẩn hàng tạm bằng prop mới ADDITIVE `hideManualCreate` (default false — popup chung chỉ đổi 2 hunk, emit không đổi); item không có id trong products nếu lọt → skip + toast. (D13)
- [x] Regression: báo giá edit + BOM builder — 0 file phải sửa, behavior y nguyên (nút Thêm hàng tạm vẫn còn), parse + smoke browser PASS. (D13)

### Task 7.2 — Bố cục bảng "Danh sách hàng hóa" giống ERP (yêu cầu user 2026-08-06)
Hiện tại (D7): mỗi hàng hóa = 2 `<tr>` (dòng hàng + dòng colspan chứa bảng con KH riêng) — khác ERP.
ERP (`form.blade.php:79-181`): 1 bảng 7 cột — STT · Hàng hóa (tên/Model/Mã) · ĐVT · Giá niêm yết · SL tồn · **Khách hàng** (cột to: mỗi dòng con = input KH readonly + nút search, SL, Ngày cần, Ghi chú, nút ×; dưới cùng nút "+ Thêm khách hàng" + dòng "Tổng cộng") · cột hành động (nút **+** xanh ở header mở popup hàng, nút **−** đỏ từng dòng xóa hàng).

- [x] Rework template bảng trong `ProductTransferRequestForm.vue` theo đúng bố cục ERP 7 cột trên (1 tr/hàng hóa, dòng con KH nằm TRONG ô cột Khách hàng). GIỮ: V2Base controls, validate inline is-invalid/invalid-feedback/touched, luồng data/units/stock/popup dùng chung (D13) — chỉ đổi BỐ CỤC, không đổi logic. (D14)
- [x] Nút thêm hàng: chuyển về nút + ở header cột cuối như ERP (nút "Thêm hàng hóa" trên form-card-head đã BỎ để khỏi trùng đường thêm hàng). (D14)
- [x] Verify: browser thật user 147 — tạo phiếu (2 hàng qua nút + header, mỗi hàng 2 dòng KH), lỗi inline hiện đúng ô trong cột KH, lưu nháp 7378 OK, form sửa render đúng, đã xóa phiếu + file S3 (baseline 7359/3126 sạch); cấu trúc cột đối chiếu blade ERP (ERP UI không có credential — như D12). (D14)

### Task 7.3 — Popup chọn khách hàng dùng chung với prospective-projects/add (yêu cầu user 2026-08-06)
Nguồn: màn `/sale/prospective-projects/add` dùng `components/modals/ChooseErpCustomerModal.vue` (modal GLOBAL, id `choose-erp-customer`, mở qua `$bvModal.show`, emit `event {type:'choiceCustomer', data: record}` — xem cách `CustomerInfoSection.vue` wire).

- [x] Form phiếu chuyển hàng thay `CustomerSearchModal.vue` riêng bằng ChooseErpCustomerModal dùng chung; lưu context dòng đích (product i / detail j) kiểu pickerTarget như CustomerInfoSection; map record → customer_id/customer_name; verify id chọn ra pass BE `exists:customers,id` (modal đọc TpCustomer → cùng bảng `customers`, validator PASS + lưu nháp 200 phiếu 7379). KHÔNG sửa modal chung — giữ nguyên 100%. (D15)
- [x] Xóa `CustomerSearchModal.vue` riêng của feature (grep 0 tham chiếu còn lại). (D15)
- [x] Regression: prospective-projects/add chọn KH qua popup như cũ (customer_id=30295 đổ đúng input); job-requests thực tế KHÔNG dùng modal chung (dùng AddCustomerModal khác — brief ghi nhầm; consumer thứ 2 là assign/meeting/GeneralInfo.vue, không đụng vì modal chung giữ nguyên). (D15)

### Task 7.4 — Rút gọn message required (yêu cầu user 2026-08-06)
User: "mấy chỗ Bắt buộc phải nhập số lượng chỉ để là bắt buộc nhập thôi, sửa lại cho tôi tất cả".

- [x] FE `ProductTransferRequestForm.vue` (client validate ~dòng 902-945): message required cấp TRƯỜNG rút gọn — "Bắt buộc phải nhập số lượng"→"Bắt buộc nhập"; "Bắt buộc phải nhập ghi chú"→"Bắt buộc nhập"; "Bắt buộc phải chọn đơn vị tính"/"khách hàng"/"ngày cần hàng"→"Bắt buộc chọn". GIỮ nguyên 2 message cấp TỔNG ("Bắt buộc phải có ít nhất 1 hàng hóa", "Bắt buộc phải đính kèm ít nhất 1 file PDF" — không phải dạng field-inline).
- [x] BE `ProductTransferRequestRequest.php` messages(): thêm key `.required` tường minh cho 5 field trên cùng nội dung ngắn (hiện đang rơi vào default locale + attributes) để 422 BE khớp FE. `php -l` + test 422 nhanh.

### Task 7.5 — Khai quyền vào PermissionsTableSeeder theo khuôn màn danh mục TK ngân hàng (yêu cầu user 2026-08-06)
Khuôn tham chiếu: quyền 1125 "Quản lý danh mục tài khoản ngân hàng" (guard api, group 'Danh mục tài chính', type 8) khai trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.

- [x] Thêm 4 quyền xem theo cấp vào PermissionsTableSeeder (id kế tiếp sau 1128 — VERIFY id trống trên DB trước), guard `api`, type 8, group riêng (vd 'Yêu cầu chuyển hàng' — group phải duy nhất toàn hệ thống), TÊN GIỮ NGUYÊN như ERP ('Xem yêu cầu chuyển hàng theo tổng công ty/công ty/phòng ban/bộ phận') để entity check theo TÊN ăn cả grant cũ (role trỏ 100878-100881) lẫn grant mới. ⚠️ Verify unique (name, guard_name) spatie: quyền ERP 100878-100881 phải là guard `web` thì mới thêm được bản `api` cùng tên — kiểm DB trước, nếu đã là `api` thì DỪNG báo lại. (D17 — id 1129-1132, guard cũ = web ✓; lưu ý gop_db KHÔNG có unique (name,guard) index)
- [x] "Kế toán kho" KHÔNG khai bản mới (quyền chung phân hệ kế toán ERP, tránh trùng lặp gây nhầm) — giữ dùng lại 100080. (D17)
- [x] INSERT tay 4 dòng tương ứng vào DB local (seeder KHÔNG reseed được trên gop_db — trùng 1117/1118 sẽ crash) + REVERT `type=8` trên 100878-100881 về NULL (tránh hiện trùng 4 cặp trong tab Tài chính — hiển thị/gán mới đi qua 4 quyền HRM). Cập nhật mục SQL DEPLOY. (D17)
- [x] Verify entity: grant quyền mới (id mới) cho user test qua employee_has_permissions → searchByFilter đổi phạm vi đúng (check theo tên bắt được id mới); revert grant + đối chiếu user có role cũ (100xxx) KHÔNG mất quyền. (D17 — user 658 grant 1129: visible 0→2967 đúng scope tổng cty, đã revert; emp 13 role ERP giữ TRUE)
- [x] **BỔ SUNG D17 (user chốt phương án A):** phát hiện entity resolve tên quyền → 1 id duy nhất (`->value('id')`) — thêm 4 quyền trùng tên làm 116 user role ERP cũ MẤT quyền (A/B test thật). Sửa 2 method `currentEmployeeHasPermission()` + `employeeInfoIdsHavingPermission()` sang `pluck('id')`+`whereIn` (file riêng của feature, user duyệt); notification 'Kế toán kho' đối chiếu D9: 13/13 id khớp, hành vi không đổi. Chi tiết: sdd/D17-report.md.

### Verify Phase 7
- [x] Form: popup mới chọn 2 hàng multi-select, chặn trùng 2 tầng, units/giá load qua endpoint D5, lưu nháp 200 (phiếu test 7377 đã dọn, baseline 7359/3126). (D13)
- [x] Báo giá edit + BOM add mở popup như cũ, console không lỗi mới (403 bom-price-approval-configs là pre-existing). (D13)
- [x] Popup KH dùng chung: chọn 3 KH vào đúng 3 dòng con (2 hàng × (i,j) khác nhau), lưu nháp 200 phiếu 7379 + form sửa render đúng + đã dọn (baseline 7359/3126); prospective-projects/add chọn KH như cũ, 0 lỗi console mới (2 Vue warn "fields" của modal chung là pre-existing, có sẵn ở cả 2 màn). (D15)

### Task 7.6 — Fix `canApprove()` port sai: Super admin bỏ qua cả `company_id` (user báo 2026-08-07)
User: "bên hrm những phiếu chờ duyệt lại có chức năng tổng hợp, mà bên erp lại không có".

Chẩn đoán: ERP `canApprove()` (`app/Model/Warehouse/ProductTransferRequest.php:329-331`) = `status==2 && can('Kế toán kho') && info->company_id == phiếu.company_id`. `Gate::before` (ERP `AuthServiceProvider.php:28-30`) CHỈ bypass được `->can()`, KHÔNG bypass vế so sánh `company_id`. Bản port HRM (Fix round 1 — Finding #3) hiểu nhầm thành "super admin bỏ qua tất cả" → `return true` ngay sau check status.
Bằng chứng DB gop_db: mọi phiếu `status=2` có `company_id=4`; 8 super admin (role 18) đều `company_id` = 1 hoặc 8 → ERP false (không nút Tổng hợp) ✔ / HRM true (hiện nút) ✘. Đã loại trừ giả thuyết quyền trùng tên: `permissions` chỉ có 1 bản 'Kế toán kho' id 100080 guard web.

- [x] BE `ProductTransferRequest::canApprove()`: bỏ nhánh `if (currentEmployeeIsSuperAdmin()) return true;`, chuyển super admin thành vế OR THAY CHO permission check, giữ nguyên 3 điều kiện `company_id` → khớp 1-1 ERP.
- [x] GIỮ NGUYÊN nhánh super admin trong `canView()` — ERP `canView()` (:322-327) có `hasRole('Super Admin') return true` tường minh, không phải Gate::before.
- [x] Không đụng `canEdit()`/`canDelete()` (ERP cũng không có super admin) và không đụng FE — `index.vue` + màn chi tiết đều ăn theo `is_can_approve`.
- [x] Verify: `php -l` + đối chiếu lại truy vấn DB (super admin company 1/8 vs phiếu company 4 → `is_can_approve` phải = false).

### Task 7.7 — Khai quyền "Kế toán kho" vào PermissionsTableSeeder (user chốt 2026-08-07)
User: "bạn xem bên erp có quyền kế toán kho không? nếu có thì thêm vào giống như các quyền ở phần danh mục tài khoản ngân hàng, quyền Xem yêu cầu chuyển hàng theo tổng công ty... đã làm ý".

Kiểm chứng ERP: CÓ — permission id 100080, guard `web`, group 'Kế toán', `type` NULL; dùng ở ~50 điểm khắp phân hệ kho ERP (`WarehouseImport`, `WarehouseExport`, `SplitExportRequest`, `ProductImportRequest`, `ProductImportDirectTransfer`, `topmenubar.blade.php`...); 11 role / 66 nhân viên đang giữ. → đủ điều kiện user đặt ra, làm theo khuôn 1129-1132.
Ghi chú: quyết định này ĐẢO lại chốt cũ ở Task 7.5 ("Kế toán kho KHÔNG khai bản mới") — user đã nghe phân tích rủi ro 2-bản-khác-guard và vẫn chọn khai.

- [x] Thêm `Permission::create(['id' => 1133, ..., 'name' => 'Kế toán kho', 'group' => 'Yêu cầu chuyển hàng', 'type' => 8])` vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (id 1133 = kế tiếp 1132, đã VERIFY trống; max id vùng HRM <100000 đang là 1132).
- [x] TÊN giữ nguyên 'Kế toán kho' như ERP → entity `currentEmployeeHasPermission()` resolve theo TÊN (pluck+whereIn, D17) bắt CẢ 2 id.
- [x] KHÔNG gỡ / KHÔNG đổi `type` bản ERP 100080 — khác 100878-100881 (bản ERP đó phải revert type về NULL vì trùng cặp trong tab); 100080 vốn đã `type` NULL nên không hiện trùng, và nó đang chi phối ~50 điểm nghiệp vụ ERP.
- [x] INSERT tay vào DB local (seeder KHÔNG reseed được trên gop_db — trùng 1117/1118 sẽ crash). Verify `permissions` không có unique index (name, guard_name) → INSERT được ✔.
- [x] Sửa comment sai ở `ProductTransferRequestController.php:157` ("dù seeder có quyền này" — lúc đó seeder CHƯA có).
- [x] Verify không ai mất quyền: số nhân viên có quyền theo tên = **66 trước và sau** khi thêm 1133 ✔. Tab phân quyền group 'Yêu cầu chuyển hàng' giờ có 5 quyền (1129-1133).

⚠️ **Giới hạn đã biết (báo user, chưa xử lý):** ERP gate bằng spatie `Auth::user()->can('Kế toán kho')` guard `web` → CHỈ nhận bản 100080. Quyền gán qua bản 1133 (UI HRM) **chỉ có hiệu lực bên HRM**; muốn có hiệu lực cả 2 cổng vẫn phải gán qua role ERP (100080). Nếu sau này muốn 1 nguồn sự thật: cân nhắc `UPDATE permissions SET type = 8 WHERE id = 100080` và bỏ bản 1133 — cần kiểm tra trước việc quyền guard `web` có surface vào `store.state.permissions` FE không (liên quan mục 3 "Chờ xác nhận PO").

### Task 7.8 — Thêm phân hệ "Kế toán" vào khối 4. KINH DOANH - TÀI CHÍNH ở màn Phân quyền (user yêu cầu 2026-08-07)
User: "ở chỗ phân quyền này (timesheet/setting/roles/add/18), ở phần 4. KINH DOANH - TÀI CHÍNH cho tôi thêm 1 phân hệ kế toán nữa và cái kế toán kho này cho vào trong đó".

Cơ chế màn Phân quyền: khối lớn + phân hệ khai ở FE `hrm-client/components/subsystems.js` (`getPermissionSubsystemGroups()`), phân hệ ↔ cột `permissions.type`, bên trong gom theo `permissions.group`.

- [x] FE `subsystems.js`: thêm phân hệ `key: 'accounting'`, label "Kế toán", `permissionType: 25` (max type đang dùng là 24), `group: GROUP_BUSINESS`, đặt ngay sau phân hệ Tài chính.
- [x] **User chốt: CHỈ hiện trong màn Phân quyền, KHÔNG thêm vào menu ngoài.** → entry chỉ có `hidden: true`, KHÔNG `erpGhost`, KHÔNG `menu`, `slugs: []` (không có màn HRM nào nên không tạo link ảo `/accounting/dashboard`).
- [x] `pages/index.vue::isShow()` bổ sung `if (subsystem.hidden) return false` — trước đây thiếu nên phân hệ `hidden` vẫn lọt ra màn chọn phân hệ. Đây là đồng bộ với bản đã đúng ở `SubsystemSwitcher.vue:92` (2 hàm vốn là bản sao của nhau), không phải hành vi mới. Mua hàng/Kho/Vận chuyển KHÔNG bị ảnh hưởng vì `itemsOfGroup()` giữ chúng qua `|| s.erpGhost`.
- [x] Sửa comment mô tả `hidden` ở `subsystems.js` cho khớp thực tế: ẩn ở màn chọn phân hệ + dropdown, **không** ẩn ở màn Phân quyền (`getPermissionSubsystemGroups()` cố ý không lọc `hidden`).
- [x] BE seeder + DB: chuyển quyền 1133 từ `type 8 / group 'Yêu cầu chuyển hàng'` → `type 25 / group 'Kế toán kho'`.
- [x] `group` phải DUY NHẤT toàn hệ thống — `Permission.vue::initListPermissions()` (:142) gom theo TÊN group **bất kể type**, trùng tên sẽ gộp nhầm 2 phân hệ. Đã verify: không group nào bị dùng ở >1 type ✔.
- [x] `PermissionsTableSeeder::GROUP_ORDER` đang `[]` → không cần khai thứ tự cho type 25 (fallback theo minId).
- [x] Verify: `subsystems.js` + `pages/index.vue` babel-parse & vue-template-compile OK; `php -l` seeder OK; DB `type=25` chỉ có đúng quyền 1133; API `timesheet/permissions` trả toàn bộ bảng (không whitelist type) nên không cần sửa BE.
- [x] Verify hành vi bằng cách nạp thật `SUBSYSTEMS` (stub import) rồi chạy 3 hàm lọc:
  - Màn chọn phân hệ + dropdown, nhóm 4 → `["Bán hàng","CSKH","Tài chính"]` (KHÔNG có Kế toán) ✔
  - Màn Phân quyền, nhóm 4 → `bán hàng[23], CSKH[24], tài chính[8], kế toán[25]` ✔
  - Nhóm 3 → `["Quản lý sản xuất","Mua hàng","Kho","Vận chuyển"]` (không đổi) ✔
  - `getAllMenuItems()` không chứa link accounting; `findSubsystemByLink('/accounting/dashboard')` → null ✔

### Task 7.9 — Dọn conflict marker trong `subsystems.js` (user duyệt 2026-08-07)
`hrm-client/components/subsystems.js` còn conflict marker Git chưa resolve (`<<<<<<< HEAD` / `=======` / `>>>>>>> 5d7fb71b...`) trong block comment mô tả các field của SUBSYSTEMS. Nằm trong comment nên không gây lỗi build, nhưng là rác merge và che mất mô tả field.

- [x] Quét toàn `hrm-client` (js/vue/json/scss): CHỈ `components/subsystems.js` dính marker.
- [x] Hai nhánh mô tả các field KHÁC NHAU, không mâu thuẫn → giữ CẢ HAI: nhánh HEAD (`hidden`, `shortLabel`, `desc`, `erpGhost`, `erpLink`) + nhánh kia (`external`).
- [x] Đối chiếu mô tả với code trước khi giữ — phát hiện nhánh kia mô tả SAI: "external đi kèm `erpPath` để trỏ đúng màn đại diện". Thực tế `pages/index.vue:186` và `SubsystemSwitcher.vue:112` đều gọi `openERP()` → về TRANG CHỦ ERP, không đọc `erpPath`. `erpPath` là khái niệm của MENU ITEM (`training-components/Sidebar.vue:65`), không phải của phân hệ. → viết lại mô tả `external` cho đúng code thay vì bê nguyên.
- [x] Verify: 0 marker còn lại; nạp lại `SUBSYSTEMS` (stub import) → 26 phân hệ, màn chọn phân hệ nhóm 4 = `Bán hàng/CSKH/Tài chính`, màn Phân quyền nhóm 4 = 4 phân hệ (có kế toán), nhóm 3 không đổi.

### Task 7.10 — Chuyển màn vào mục menu "Phiếu điều chuyển hàng" (user chốt 2026-08-07)
User: "phiếu yêu cầu chuyển hàng giờ cho vào menu Phiếu điều chuyển hàng". Có 2 cách hiểu (chuyển sang nhóm Điều chuyển giữ tên cũ / gán link vào chính mục "Phiếu điều chuyển hàng") → đã hỏi, **user chọn gán link vào chính mục "Phiếu điều chuyển hàng"**, không giữ 2 mục trỏ cùng một màn.

- [x] `components/subsystem-menu/finance.js`: xoá `{ label: 'Phiếu yêu cầu chuyển hàng', link: '/finance/product-transfer-requests' }` khỏi nhóm "Xuất hàng".
- [x] Gán link vào mục sẵn có của nhóm "Điều chuyển": `{ label: 'Phiếu điều chuyển hàng', link: '/finance/product-transfer-requests' }` (trước đó không có link → render xám mờ).
- [x] KHÔNG gắn `isShow` — giữ nguyên như mục cũ; gắn quyền lúc này sẽ 404 với mọi user (điểm B2 / mục 3 "Chờ xác nhận PO": quyền guard web chưa surface vào `store.state.permissions`).
- [x] Verify bằng cách nạp thật `financeItems`: chỉ còn ĐÚNG 1 mục trỏ tới màn (`Điều chuyển > Phiếu điều chuyển hàng`); nhóm "Xuất hàng" còn 5 mục, không còn nhãn cũ.

⚠️ **Lệch tên còn lại (chưa xử lý, chờ user):** menu giờ là "Phiếu điều chuyển hàng" nhưng tiêu đề trang vẫn là "Phiếu yêu cầu chuyển hàng" — `PageTitleMixin` chỉ đẩy `pageTitle` từ computed của trang, KHÔNG lấy nhãn menu, nên các chỗ sau vẫn giữ tên cũ: `pages/finance/product-transfer-requests/index.vue` (`title` + `V2BaseFilterPanel.title` + `V2BaseDataTable.title`), màn chi tiết/form/print, tên file Excel export, và message xác nhận xoá.

## ENV DEPLOY (bổ sung sau final review — bắt buộc khi lên môi trường thật)

1. `hrm-api/.env`: thêm `ERP_URL=<url cổng ERP>` — dùng cho logo mẫu in template 87 (thiếu → logo trống, không chặn in). ⚠️ Nếu prod chạy `php artisan config:cache` thì `env()` ngoài config trả null (cùng điểm yếu AccountService có sẵn) — hoặc không cache config, hoặc chờ task riêng chuyển sang config key.
2. `hrm-client/.env`: thêm `ERP_URL=<url cổng ERP>` **TRƯỚC khi build** (`@nuxtjs/dotenv` nhúng lúc build) — dùng cho nút "Tổng hợp" mở màn tạo phiếu xuất ERP ở list + chi tiết. Sau đó build lại FE.
3. SQL DEPLOY (mục trên — ĐỔI PHƯƠNG ÁN ở D17, thay câu `UPDATE ... type = 8` cũ): hiển thị/gán mới đi qua 4 quyền HRM chính chủ 1129-1132 (khai trong PermissionsTableSeeder), quyền ERP cũ 100878-100881 rút khỏi tab (type NULL). ⚠️ ĐIỀU KIỆN TIÊN QUYẾT: deploy code entity `ProductTransferRequest.php` bản D17 (resolve tên quyền bằng `pluck`+`whereIn`) TRƯỚC/CÙNG lúc chạy INSERT — chạy INSERT với code cũ (`value('id')`) sẽ làm ~116 user có role ERP cũ MẤT quyền (bằng chứng: sdd/D17-report.md). Đã chạy local, cần chạy trên môi trường thật:
   ```sql
   INSERT INTO permissions (id, name, guard_name, `group`, display_name, type, created_at, updated_at) VALUES
   (1129, 'Xem yêu cầu chuyển hàng theo tổng công ty', 'api', 'Yêu cầu chuyển hàng', 'Xem yêu cầu chuyển hàng theo tổng công ty', 8, NOW(), NOW()),
   (1130, 'Xem yêu cầu chuyển hàng theo công ty',      'api', 'Yêu cầu chuyển hàng', 'Xem yêu cầu chuyển hàng theo công ty',      8, NOW(), NOW()),
   (1131, 'Xem yêu cầu chuyển hàng theo phòng ban',    'api', 'Yêu cầu chuyển hàng', 'Xem yêu cầu chuyển hàng theo phòng ban',    8, NOW(), NOW()),
   (1132, 'Xem yêu cầu chuyển hàng theo bộ phận',      'api', 'Yêu cầu chuyển hàng', 'Xem yêu cầu chuyển hàng theo bộ phận',      8, NOW(), NOW());
   UPDATE permissions SET type = NULL WHERE id IN (100878, 100879, 100880, 100881);

   -- Task 7.7 + 7.8 (2026-08-07): quyền "Kế toán kho" bản HRM, thuộc phân hệ Kế toán (type 25).
   -- KHÔNG đụng bản ERP 100080 (guard web, type vốn đã NULL nên không hiện trùng trong tab;
   -- đang chi phối ~50 điểm nghiệp vụ kho ERP).
   -- ⚠️ Phải deploy kèm FE `hrm-client/components/subsystems.js` có phân hệ key 'accounting'
   -- (permissionType 25) — thiếu nó thì quyền type 25 không có khối nào để hiện ở màn Phân quyền.
   INSERT INTO permissions (id, name, guard_name, `group`, display_name, type, created_at, updated_at) VALUES
   (1133, 'Kế toán kho', 'api', 'Kế toán kho', 'Kế toán kho', 25, NOW(), NOW());
   ```
   (Câu `UPDATE ... SET type = 8 ...` cũ KHÔNG chạy nữa; môi trường nào đã lỡ chạy thì câu `SET type = NULL` ở trên tự đưa về đúng trạng thái.)
4. **QUYỀN "Xem khách hàng" (perm 100057) — bắt buộc trước go-live (phát sinh D15):** popup KH dùng chung gate `erpPermission:Xem khách hàng`; đo DB thật có **5 user active từng tạo phiếu 12 tháng qua THIẾU quyền này** (336 Lưu Thị Hằng 13 phiếu · 504 Nguyễn Thu Hòa 9 · 724 Nguyễn Thị Nguyệt 4 · 73 Ngô Doãn Hạnh 2 · +1 user) → mở popup thấy bảng rỗng im lặng, không tạo/sửa phiếu được. Cấp quyền cho nhóm này TRƯỚC khi mở màn cho user thật; hoặc mở task riêng cho modal chung hiện thông báo 403 rõ ràng thay vì bảng rỗng.

## Chờ xác nhận PO / task riêng phát sinh

1. **Thông báo cổng ERP**: chuông ERP đã bị vô hiệu từ đợt gộp DB (Notification model ERP chặn save) → user thuần cổng ERP KHÔNG còn thấy thông báo phiếu chờ duyệt; notification feature này đi vào chuông HRM. PO xác nhận chấp nhận hay cần cơ chế 2 cổng.
2. **B1 — canView hẹp hơn list** (port trung thành ERP): user có quyền xem theo tổng cty/phòng/bộ phận nhưng không có "Kế toán kho" → thấy phiếu trong list nhưng mở chi tiết/in bị 403. Giữ như ERP hay mở scope canView theo searchByFilter — PO chốt.
3. **Task riêng — rà quyền gop_db**: (a) middleware `CheckPermission` resolve spatie bỏ sót role gán từ ERP (model_type mismatch) — mọi route đang gắn nó trên gop_db có thể 403 sai (phát hiện D8); (b) quyền web-guard chưa surface vào `store.state.permissions` FE → các màn finance-catalog (accounts/currencies/account-banks) 404 với mọi user, và menu feature này chưa gắn được `isShow` (B2 — gắn bây giờ sẽ 404 toàn bộ). Gộp 2 việc thành 1 task rà mapping quyền.
4. **SL lẻ**: FE chặn SL thập phân (precision=0) trong khi BE/DB cho phép — PO chốt nghiệp vụ chuyển hàng có SL lẻ không.
5. **Template 87 cột hẹp** (STT/SL/Ngày cần): muốn đẹp phải sửa template trong DB — ảnh hưởng cả 2 cổng, cần user chốt.

### Checkpoint — 2026-08-05
Vừa hoàn thành: Spec + plan (chưa code).
Đang làm dở: —
Bước tiếp theo: Thực thi Phase 1 (Task 1.1).
Blocked: —

### Checkpoint — 2026-08-06 (chiều — Phase 7)
Vừa hoàn thành: D13 — đồng nhất popup chọn hàng hóa: form chuyển hàng dùng CHUNG QuotationProductSearchModal của màn báo giá (goodsOnly + hideManualCreate additive), xóa ProductSearchModal riêng, regression báo giá/BOM PASS. Lưu ý môi trường: .env hrm-api ERP_URL đã sửa 127.0.0.1:8000 → erp.test:8080 (giá trị cũ gây deadlock search popup).
Đang làm dở: —
Bước tiếp theo: user chốt minor D13 (overlay trùng "Cộng dồn/Tạo dòng mới" vô nghĩa với phiếu chuyển hàng — có cần thêm prop duplicateMode="block" không) + các mục checkpoint dưới.
Blocked: —

### Checkpoint — 2026-08-06 (sáng)
Vừa hoàn thành: TOÀN BỘ Phase 1–6 (D1–D12) + final whole-branch review READY-WITH-FIXES + fix wave (2 fix: đóng oracle date_needed/403 đúng thứ tự trong FormRequest; comment stale + toast 403 ở list) + re-review ALL ADDRESSED. Code lúc đó chưa commit (đã commit ngày 2026-08-07 — xem checkpoint cuối). Ledger đầy đủ: sdd-progress.md; report từng task: sdd/D*-report.md.
Đang làm dở: —
Bước tiếp theo: user hard-refresh verify browser bằng mắt (list → tạo → gửi duyệt → reject → in → export) + trả lời 5 mục "Chờ xác nhận PO" ở trên + yêu cầu commit khi ưng.
Blocked: —

---

## Phase 7 — Tài liệu test case (yêu cầu user 2026-08-07)

- [x] Đọc lại nguồn ERP để đối chiếu: `app/Model/Warehouse/ProductTransferRequest.php` (STATUSES, boot, searchByFilter, syncProducts, canView/canApprove/canEdit/canDelete, print_data, product_table) + `app/Http/Controllers/Warehouse/ProductTransferRequestsController.php` (store/update/delete/deleteFile/reject/print/exportList/validateProducts)
- [x] Rà lại BE HRM: Entity + Request + Service + Controller + 2 Resource + routes
- [x] Rà lại FE HRM: `index.vue`, `_id/index.vue`, `_id/print.vue`, `components/ProductTransferRequestForm.vue`, `create.vue`, `_id/edit.vue`
- [x] Xác định phân quyền: route KHÔNG gắn checkPermission (giống ERP); phạm vi theo 4 quyền `Xem yêu cầu chuyển hàng theo tổng công ty/công ty/phòng ban/bộ phận` + `Kế toán kho` + role Super admin 18 → section TC-ROLE 10 TC
- [x] Viết `generate-testcase.py` theo skill `testcase-documenter`
- [x] Sinh `testcase.xlsx` — 127 TC (10 TC-ROLE + 8 section La mã), P0 = 89 (70%)

### Checkpoint — 2026-08-07 (Phase 7)
Vừa hoàn thành: `testcase.xlsx` (127 TC) + `generate-testcase.py` cho màn Phiếu yêu cầu chuyển hàng, có đối chiếu ERP.
Đang làm dở: không.
Bước tiếp theo: QA review file; cần chỉnh thì sửa `generate-testcase.py` rồi chạy lại (`python .plans/gop-db/finance-product-transfer-request/generate-testcase.py`).
Blocked: không.

### TC đối chiếu ERP ↔ HRM đã đưa vào file
| Nội dung đối chiếu | TC |
|---|---|
| Bộ cột danh sách khớp ERP | TC_01.002 |
| Danh sách trạng thái 13 mục khớp ERP (id 8/9 trùng tên là đúng gốc) | TC_02.004 |
| Tổng số + thứ tự phiếu 2 cổng | TC_04.010 |
| Nút Tổng hợp hiện đúng như ERP (Super admin khác công ty không hiện) | TC_04.007, TC-ROLE-08 |
| Nới rule `date_needed after:today` khi sửa (ERP chặn, HRM cho) | TC_06.008, TC_06.009, TC_06.010 |
| Xóa file S3 thật (ERP unlink cục bộ — không xóa được) | TC_05.017 |
| Chuỗi attachments không còn dấu phẩy thừa (lỗi nối chuỗi ERP) | TC_05.019 |
| ĐVT không thuộc hàng hóa / thiếu giá → 422 thay vì 500 như ERP | TC_06.017, TC_06.018 |
| Bản in: `date_needed` null → HRM in rỗng, ERP in ngày hôm nay | TC_05.034 |
| Bản in escape HTML + ký tự `$` | TC_06.024, TC_06.025 |
| Export null-safe tên nhân viên/trạng thái lạ | TC_05.040 |
| Ghi/đọc song song 2 cổng trên cùng 3 bảng | TC_06.029, TC_06.030, TC_08.005 |
| Phạm vi dữ liệu 2 cổng theo từng mức quyền | TC_07.008 |

### Điểm cần nghiệp vụ xác nhận (ghi nhận khi viết test case, chưa sửa code)
- **Giá lưu ≠ giá hiển thị**: form hiển thị giá ĐÃ áp hệ số công ty (`round(price × coeff / 1000) × 1000`), nhưng `syncProducts` lưu vào DB giá bán lẻ THÔ — port đúng nguyên bản ERP nhưng 2 con số lệch nhau khi công ty có hệ số ≠ 1 (TC_06.020).
- **Không chặn theo tồn kho**: lập phiếu với SL vượt tồn khả dụng vẫn lưu được (đúng ERP) — tồn kho chỉ để tham khảo (TC_08.002).
- **Quyền "theo bộ phận"** có thể chưa được khai trong seeder → TC-ROLE-05 có thể phải ghi Pending nếu không gán được quyền để test.

### Checkpoint — 2026-08-07 (BÀN GIAO — feature HOÀN THÀNH)
Vừa hoàn thành: user xác nhận xong toàn bộ hạng mục còn treo — verify browser bằng mắt · trả lời 5 mục "Chờ xác nhận PO" ở trên · ENV DEPLOY `ERP_URL` cả `hrm-api/.env` và `hrm-client/.env` · **SQL DEPLOY đã chạy trên môi trường thật** (INSERT quyền 1129-1133 + `UPDATE permissions SET type = NULL WHERE id IN (100878,100879,100880,100881)`). Code đã commit cả 2 repo trên nhánh `gop_db`: `hrm-api 3a0acce08` · `hrm-client ed0abb049` (+ `690515fc4` fix bug). STATUS.md đã chuyển feature sang mục "Hoàn thành".
Đang làm dở: không.
Bước tiếp theo: (1) ghi ngược nội dung PO đã chốt vào mục "Chờ xác nhận PO / task riêng" ở trên — hiện vẫn đang để dạng câu hỏi; (2) mở TASK RIÊNG rà quyền `gop_db`: middleware `CheckPermission` bỏ sót role gán từ ERP (model_type mismatch) trên MỌI route đang gắn nó + mapping quyền web-guard chưa surface vào `store.state.permissions` FE (kéo theo B2 — menu feature này chưa gắn được `isShow`).
Blocked: không.
