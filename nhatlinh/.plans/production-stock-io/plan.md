# Plan — Xuất / Nhập phục vụ sản xuất (production-stock-io)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans. Task dùng checkbox `- [ ]`.
> Spec đầy đủ (BẮT BUỘC đọc trước mỗi task): `docs/superpowers/specs/2026-07-02-production-stock-io-design.md`

**Goal:** Lệnh sản xuất (nhiều thành phẩm, bung NVL từ BOM) + phiếu xuất loại 3 "Xuất phục vụ sản xuất" / phiếu nhập loại 4 "Nhập từ sản xuất" gắn lệnh, từng phần, chặn vượt.

**Architecture:** Entity mới chỉ có ProductionOrder (3 bảng). Phiếu tái dùng WhIssue/WhReceipt (thêm loại + `production_order_id`). Chặn vượt tại bước Duyệt phiếu theo `quantity_base`, cùng transaction với `assertEnough`.

**Tech Stack:** Laravel 8 / PHP 7.4 (nhatlinh-api, Modules/Warehouse) + Nuxt 2 / Vue 2 (nhatlinh-client).

## Global Constraints

- KHÔNG commit/push git. KHÔNG đọc vendor/, node_modules/.
- Permission: sửa `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, id 1139/1140/1141, type=10, group "Lệnh sản xuất". DB dev: INSERT tay + gán role 1 + cache clear (KHÔNG chạy seeder — seeder TRUNCATE).
- Status hiển thị: BE trả `status_name`/`status_color` (trait `HasStatusBadge`), FE chỉ dùng `V2BaseBadge`.
- Validate: BE rethrow `ValidationException`; FE lỗi inline (`is-invalid` + `invalid-feedback`, flag `touched`).
- DB convention: `company_id/department_id/part_id` + `created_by/updated_by` nullable, timestamps, KHÔNG SoftDeletes.
- FE: đọc `.claude/skills/button-convention/SKILL.md` khi tạo nút, `.claude/skills/modal-popup/SKILL.md` khi tạo modal. Trang dùng `V2Footer` → container `padding-bottom: 60px`.
- Verify mỗi task BE: `php -l` từng file + smoke tinker khi có logic. FE: không build được (node cũ) → tự review code, user test trình duyệt.

---

## Phase 1 — BE: Lệnh sản xuất

### Task 1: Migrations

**Files (Create, trong `nhatlinh-api/Modules/Warehouse/Database/Migrations/`):**
- `2026_07_02_000001_create_production_orders_table.php`
- `2026_07_02_000002_create_production_order_products_table.php`
- `2026_07_02_000003_create_production_order_materials_table.php`
- `2026_07_02_000004_add_production_order_id_to_wh_issues_table.php`
- `2026_07_02_000005_add_production_order_id_to_wh_receipts_table.php`

Schema theo spec mục 3 (production_orders: code unique, order_date, expected_date nullable, note, status tinyInteger default 1, approved_at/by, reject_reason, completed_at/by, company/department/part_id, created_by/updated_by, timestamps; 2 bảng dòng: production_order_id index, product_id, unit_id, conversion_rate decimal(15,4) default 1, quantity + quantity_base decimal(15,2), sort_order int default 0, timestamps; 2 alter thêm `production_order_id` unsignedBigInteger nullable sau `contract_id`). Copy pattern migration `wh_transfers`.

- [x] Viết 5 migration (+FK cascade 2 bảng dòng theo pattern wh_transfer_items)
- [x] `php artisan migrate` OK, verify schema + FK dev DB — review Approved

### Task 2: Entities

**Files:**
- Create: `Modules/Warehouse/Entities/ProductionOrder.php`, `ProductionOrderProduct.php`, `ProductionOrderMaterial.php`
- Modify: `Modules/Warehouse/Entities/WhIssue.php`, `WhReceipt.php`

**Produces (task sau dùng):** `ProductionOrder::STATUS_DRAFT/PENDING/APPROVED/REJECTED=1..4, STATUS_COMPLETED=5`; helpers `isCanEdit/isCanDelete/isCanSubmit/isCanApprove/isCanComplete/isCanCreateVoucher`; relations `products()/materials()/issues()/receipts()`; `getNextCode()` → `LSX-YYYY-NNNNN`. `WhIssue::ISSUE_TYPE_PRODUCTION=3`, `WhReceipt::RECEIPT_TYPE_PRODUCTION=4`, cả 2 có relation `productionOrder()`.

- [x] `ProductionOrder`: copy pattern `WhIssue.php` (trait HasStatusBadge, STATUSES 5 dòng theo spec 4.1 — Hoàn thành `#2563EB`; accessors employee_create_name/employee_approve_name; getNextCode `LSX-`). `isCanCreateVoucher()` = status APPROVED.
- [x] 2 entity dòng: fillable theo spec 3.2, relations `product()` (Modules\Category\Entities\Product), `unit()`.
- [x] WhIssue: thêm const + entry ISSUE_TYPES `['id'=>3,'name'=>'Xuất phục vụ sản xuất']`, fillable + `production_order_id`, relation `productionOrder()`.
- [x] WhReceipt: tương tự với `['id'=>4,'name'=>'Nhập từ sản xuất']`.
- [x] `php -l` 5 file

### Task 3: ProductionOrderService

**Files:** Create `Modules/Warehouse/Services/ProductionOrderService.php` (copy pattern `WhTransferService.php`)

**Produces:** `index($request)` trả query builder (KHÔNG paginate — tránh bug paginate 2 lần); `store/update/destroy`; `submit/approve/reject/complete`; `bomMaterials(array $lines): array`; `progress(ProductionOrder $order): array`.

- [x] CRUD: transaction, sync 2 bảng dòng delete-insert (pattern syncItems WhIssueService), server tính `quantity_base = quantity × conversion_rate` (conversion_rate lấy từ `product_units` theo product_id+unit_id — xem cách WhIssueService resolve); update chỉ khi `isCanEdit()`, destroy chỉ khi `isCanDelete()`, sai → `ValidationException`.
- [x] Workflow: submit (Nháp/Từ chối→Chờ duyệt), approve (set approved_at/by), reject (bắt buộc reject_reason), complete (chỉ APPROVED → status 5 + completed_at/by, KHÔNG chặn thiếu SL).
- [x] `bomMaterials($lines)`: mỗi dòng `{product_id, unit_id, quantity}` → BOM active của product (`Modules\Category\Entities\Bom` status ACTIVE, is_default ưu tiên) → SL NVL = `norm_quantity × (1 + waste_percent/100) × quantity_base thành phẩm`, round 2 → gộp theo `material_product_id + unit_id`. Trả `['materials' => [...], 'products_without_bom' => [product_id...]]`.
- [x] `progress($order)`: mỗi dòng NVL → `issued_base` = SUM `wh_issue_items.quantity_base` join `wh_issues` (production_order_id = lệnh, status APPROVED, cùng product_id); mỗi dòng thành phẩm → `received_base` từ `wh_receipt_items` tương tự. Kèm `remaining_base = max(0, quantity_base − done)`.
- [x] `php -l` + smoke tinker: tạo lệnh 2 thành phẩm → bomMaterials gộp đúng + cảnh báo thiếu BOM → submit/approve → progress trả 0.

### Task 4: Request + Resources + Controller + Routes + Permission

**Files:**
- Create: `Modules/Warehouse/Http/Requests/ProductionOrderRequest.php`; `Modules/Warehouse/Transformers/ProductionOrderResource/ListProductionOrderResource.php` + `DetailProductionOrderResource.php`; `Modules/Warehouse/Http/Controllers/Api/V1/ProductionOrderController.php`
- Modify: `Modules/Warehouse/Routes/api.php`; `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

**Produces (FE dùng):** routes prefix `/v1/warehouse/production-orders` theo bảng spec 4.5 (bom-materials + route tĩnh TRƯỚC `/{id}`); Detail resource trả `products[]/materials[]` (kèm progress từng dòng: `issued_base|received_base`, `remaining_base`), `vouchers[]` (id, code, type: issue|receipt, date, status_name, status_color), `is_can_*` đủ 6 flag, `status_name/status_color`.

- [x] Request rules theo spec 4.5: order_date required date; expected_date nullable ≥ order_date; products + materials required array min 1, dòng required product_id/unit_id/quantity>0, distinct product trong từng bảng.
- [x] 2 Resource (ApiResource) — list: code, order_date, expected_date, tên thành phẩm đầu + count, status 3 field, employee_create_name, created_at, is_can_edit/delete.
- [x] Controller extends ApiController: index (apiPaginate), show, store, update, destroy, submit, approve, reject, complete, bomMaterials — pattern WhTransferController, responseJson.
- [x] Routes + `checkPermission` theo bảng spec 4.5.
- [x] Seeder: thêm 3 dòng 1139/1140/1141 group "Lệnh sản xuất" type=10 (đặt cạnh nhóm kho hiện có).
- [x] DB dev: INSERT 3 permission + gán role 1 (pivot) + `php artisan cache:clear` — pattern các lần trước, hỏi user duyệt lệnh SQL.
- [x] `php -l` + smoke curl/tinker: route list 200, tạo→duyệt qua HTTP hoặc tinker.

## Phase 2 — BE: Phiếu xuất/nhập sản xuất

### Task 5: WhIssueService loại 3 (LƯU Ý: sửa hàm dùng chung — đã được duyệt scope trong spec)

**Files:**
- Modify: `Modules/Warehouse/Services/WhIssueService.php`, `Http/Requests/WhIssueRequest.php`, `Transformers/WhIssueResource/*` (2 file), `Http/Controllers/Api/V1/WhIssueController.php`, `Routes/api.php`

**Produces:** endpoint `GET /v1/warehouse/issues/production-remaining?production_order_id=&warehouse_id=` → dòng NVL lệnh kèm `remaining` (net theo phiếu đã duyệt) + `available` (tồn khả dụng kho); phiếu loại 3 lưu/duyệt được, chặn vượt.

- [x] Request: `production_order_id` required_if issue_type=3, exists; loại 3 không nhận unit_price.
- [x] Service store/update: loại 3 → validate lệnh `isCanCreateVoucher()` + mọi product_id ∈ `production_order_materials`; unit_price/amount/total_amount = null; contract_id = null.
- [x] `assertProductionRemaining($issue)` gọi trong `approve()` cùng transaction với assertEnough (sau lockForUpdate): từng product — SUM(quantity_base phiếu APPROVED khác cùng lệnh) + phiếu này ≤ quantity_base dòng NVL; vi phạm → ValidationException nêu mã hàng. Chặn duyệt nếu lệnh COMPLETED ("Lệnh sản xuất đã hoàn thành").
- [x] `productionRemaining($orderId, $warehouseId)` + controller + route (checkPermission "Thêm sửa phiếu xuất kho" — tên đúng theo seeder 1128, route đặt TRƯỚC `/{id}`).
- [x] Resources: + `production_order_id`, `production_order_code`.
- [x] `php -l` + smoke tinker: xuất 1 phần OK tồn giảm → phiếu 2 vượt → 422; lệnh complete → duyệt phiếu treo → 422.

### Task 6: WhReceiptService loại 4 (đối xứng Task 5)

**Files:** Modify `WhReceiptService.php`, `WhReceiptRequest.php`, `WhReceiptResource/*`, `WhReceiptController.php`, `Routes/api.php`

- [x] Như Task 5 nhưng phía nhập: items ∈ `production_order_products`, chặn tổng nhập ≤ SL kế hoạch, endpoint `GET /v1/warehouse/receipts/production-remaining?production_order_id=` (không cần tồn kho), permission "Thêm sửa phiếu nhập kho" (1125).
- [x] `php -l` + smoke tinker: nhập 1 phần → progress tăng; vượt kế hoạch → 422.

### Task 7: Smoke test E2E BE toàn luồng (tinker)

- [x] Kịch bản spec mục 8: lệnh 2 thành phẩm (1 có BOM chung NVL, 1 không BOM) → bung BOM → approve → xuất NVL 2 đợt (đợt 2 vượt → 422) → nhập thành phẩm 1 phần → complete → tạo/duyệt phiếu mới gắn lệnh → chặn. Ghi kết quả vào checkpoint.
- [x] Downstream (spec mục 7): thẻ kho (`/reports/stock-card`) resolve số phiếu + link đúng với movement từ phiếu sản xuất; dashboard kho không lỗi.

## Phase 3 — FE: Màn Lệnh sản xuất

### Task 8: Store + Menu + List

**Files:**
- Create: `nhatlinh-client/store/warehouse-production-order.js`; `pages/warehouse/production-order/index.vue`
- Modify: `components/default-menu/warehouse.js`

**Produces:** store actions `getList/getDetail/create/update/delete/submit/approve/reject/complete/getBomMaterials` (pattern warehouse-transfer.js, endpoint Task 4).

- [x] Store copy pattern `store/warehouse-transfer.js`.
- [x] Menu "Lệnh sản xuất" sau "Chuyển kho", `isShow: ['Xem lệnh sản xuất']`.
- [x] List theo spec 5.1 (style list phân hệ kho — theo `pages/warehouse/transfer/index.vue`): cột + filter + nút Thêm gated "Thêm sửa lệnh sản xuất"; badge `V2BaseBadge`; Sửa/Xóa theo `is_can_*`.

### Task 9: Form (add/edit)

**Files:**
- Create: `components/warehouse/production-order/ProductionOrderForm.vue`; `pages/warehouse/production-order/create.vue`; `pages/warehouse/production-order/_id/edit.vue`

**Consumes:** store Task 8. Pattern gốc: `components/warehouse/transfer/WhTransferForm.vue`.

- [x] Header: Ngày lệnh (default hôm nay) / Ngày dự kiến / Ghi chú.
- [x] Bảng Thành phẩm: chọn hàng hoá (pattern chọn hàng của WhTransferForm), SL, ĐVT theo product_units.
- [x] Nút "Bung NVL theo BOM" → `getBomMaterials` → đổ bảng NVL (bảng đã có dòng → confirm ghi đè; toast cảnh báo `products_without_bom`).
- [x] Bảng NVL sửa/thêm/xóa dòng tự do.
- [x] Validate inline touched theo spec 5.1 (ngày required, ≥1 dòng mỗi bảng, SL>0, không trùng hàng, expected_date ≥ order_date).
- [x] Footer Lưu / Lưu & Gửi duyệt / Lưu & Duyệt (theo quyền duyệt) → redirect danh sách. Đọc skill button-convention trước.

### Task 10: Detail

**Files:** Create `pages/warehouse/production-order/_id/index.vue`

**Consumes:** Detail resource Task 4 (progress + vouchers + is_can_*).

- [x] Info + badge; bảng Thành phẩm cột "Đã nhập" (xanh khi đủ), bảng NVL cột "Đã xuất".
- [x] Khối "Phiếu gắn lệnh": mã link sang `/warehouse/issue/{id}` hoặc `/warehouse/receipt/{id}` theo type, badge trạng thái.
- [x] Footer theo trạng thái: Gửi duyệt / Duyệt / Từ chối (modal lý do — skill modal-popup) / Hoàn thành (confirm; thiếu SL → text cảnh báo "Chưa xuất đủ NVL / chưa nhập đủ thành phẩm. Vẫn hoàn thành?").
- [x] Nút "Tạo phiếu xuất NVL" → `/warehouse/issue/create?production_order_id=`, "Tạo phiếu nhập thành phẩm" → `/warehouse/receipt/create?production_order_id=` (chỉ khi `is_can_create_voucher` + có quyền thêm sửa phiếu).

## Phase 4 — FE: Form phiếu

### Task 11: WhIssueForm loại 3 + list/detail phiếu xuất

**Files:** Modify `components/warehouse/issue/WhIssueForm.vue`, `pages/warehouse/issue/index.vue`, `pages/warehouse/issue/_id/index.vue`, `store/warehouse-issue.js` (+action `getProductionRemaining`)

- [x] Option loại "Xuất phục vụ sản xuất" → select Lệnh (getList lệnh status=3) → load `production-remaining` → bảng NVL checkbox + Chọn/Bỏ chọn tất cả, mặc định chọn dòng còn lại, SL = min(remaining, available); cột "Còn phải xuất"/"Tồn khả dụng" + validate inline ≤ cả hai (pattern nhánh xuất theo HĐ trong cùng file).
- [x] Ẩn cột Đơn giá/Thành tiền/Tổng tiền với loại 3; đổi kho → reload available.
- [x] Prefill từ query `production_order_id`.
- [x] List/detail: label loại từ `issue_type_name`; filter loại phiếu trên list (nếu có dropdown) thêm option loại 3; detail loại 3 hiện link "Lệnh sản xuất: LSX-..." + ẩn khối giá.

### Task 12: WhReceiptForm loại 4 + list/detail phiếu nhập (đối xứng Task 11)

**Files:** Modify `components/warehouse/receipt/WhReceiptForm.vue`, `pages/warehouse/receipt/index.vue`, `pages/warehouse/receipt/_id/index.vue`, `store/warehouse-receipt.js`

- [x] Như Task 11 phía nhập: loại "Nhập từ sản xuất", cột "Còn phải nhập" (không cần tồn), ẩn giá, prefill query, label/link detail.

---

## Phase 5 — Tinh chỉnh form lệnh sản xuất (yêu cầu 2026-07-03)

### Task 13: BE — Người phụ trách SX + endpoint xem BOM theo product

- [x] Migration `2026_07_03_000001_add_manager_id_to_production_orders_table.php`: thêm `manager_id` unsignedBigInteger nullable sau `expected_date` + migrate dev.
- [x] Entity ProductionOrder: fillable + relation `managerEmployee()` (belongsTo Employee) + accessor `employee_manager_name` (pattern employee_create_name).
- [x] Request: `manager_id` nullable|exists nhân viên (theo pattern field employee khác trong module).
- [x] Service headerData/store/update: nhận `manager_id`.
- [x] Resources: Detail + List trả `manager_id`, `employee_manager_name`.
- [x] Endpoint mới `GET /production-orders/product-bom/{productId}` (checkPermission "Thêm/sửa lệnh sản xuất", đặt TRƯỚC `/{id}`): trả BOM active của product — `{bom: {id, code, name} | null, items: [{material_code, material_name, unit_name, norm_quantity, waste_percent, note}]}` — cho popup FE xem công thức.
- [x] php -l + smoke tinker.

### Task 14: FE — Auto bung NVL + icon popup BOM + trường Người phụ trách

- [x] ProductionOrderForm: bỏ nút "Bung NVL theo BOM" → **tự động** gọi bomMaterials khi bảng thành phẩm thay đổi (thêm/xóa dòng, đổi SL/ĐVT — debounce ~400ms, guard `this.loading` khi mở edit): NVL chưa bị user sửa tay → thay thế im lặng; user đã sửa tay bảng NVL (flag dirty) → confirm trước khi ghi đè; vẫn giữ cảnh báo products_without_bom.
- [x] Mỗi dòng thành phẩm: icon (vd `ri-file-list-3-line`) → popup modal (skill modal-popup) hiện BOM công thức khai báo của product đó (gọi endpoint product-bom: bảng NVL + định mức + hao hụt % + ghi chú; product không BOM → thông báo trong popup).
- [x] Thông tin chung: thêm select "Người phụ trách SX" (danh sách nhân viên theo pattern chọn nhân viên sẵn có của dự án) cùng row, TRƯỚC "Ghi chú"; lưu `manager_id`; edit mode load lại đúng.
- [x] Detail lệnh (_id/index.vue): hiện "Người phụ trách SX" trong khối info.
- [x] **List lệnh SX — cột "Thao tác" bổ sung button workflow** (yêu cầu 2026-07-03): Gửi duyệt (`is_can_submit` + quyền Thêm/sửa, confirm), Duyệt (`is_can_approve` + quyền Duyệt, confirm), Từ chối (`is_can_approve` + quyền Duyệt, modal lý do required), Hoàn thành (`is_can_complete` + quyền Duyệt, confirm cảnh báo như detail) — giữ Sửa/Xóa; sau thao tác reload list + toast. BE: ListProductionOrderResource trả thêm `is_can_submit/is_can_approve/is_can_complete`.
- [x] Verify tĩnh + đối chiếu pattern.

## Phase 6 — Lệnh sản xuất trên Dashboard kho (yêu cầu 2026-07-03)

### Task 15: BE — WhDashboardService bổ sung khối production_orders

- [x] `WhDashboardService::getData` trả thêm key `production_orders`:
  - `pending_count`: số lệnh Chờ duyệt (status=2) — không lọc ngày (nhất quán KPI chờ duyệt phiếu hiện có).
  - `in_progress_count`: số lệnh Đã duyệt chưa hoàn thành (status=3).
  - `completed_in_range`: số lệnh Hoàn thành trong khoảng lọc ngày dashboard (theo `completed_at`).
  - `in_progress`: tối đa 10 lệnh status=3, sort `expected_date` ASC nulls-last (gần hạn lên đầu): id, code, product_summary (thành phẩm đầu +N), expected_date (d/m/Y), is_overdue (expected_date < hôm nay), employee_manager_name, progress_percent = round(SUM received_base / SUM quantity_base × 100) các dòng thành phẩm (0 nếu mẫu 0) + issued_percent tương tự cho NVL.
- [x] Query gọn (aggregate, tránh N+1 — SUM group by production_order_id).
- [x] php -l + smoke tinker (dashboard chạy không lỗi, count/percent đúng với data test).

### Task 16: FE — Dashboard kho hiển thị khối Lệnh sản xuất

- [x] Hàng KPI chờ duyệt (Nhập/Xuất/Chuyển): thêm card **"Lệnh SX chờ duyệt"** (`pending_count`, link `/warehouse/production-order?status=2` — list đọc query status để prefill filter nếu chưa có thì thêm) — gated hiển thị như các card hiện có.
- [x] Khối mới **"Lệnh sản xuất đang thực hiện"** (bảng, kèm badge đếm `in_progress_count`, phụ đề số hoàn thành trong kỳ `completed_in_range`): cột Mã lệnh (link detail) / Thành phẩm / Ngày dự kiến (đỏ nếu `is_overdue`) / Người phụ trách / Tiến độ nhập TP (progress bar % + text) / Tiến độ xuất NVL (%). Empty state. Vị trí: hàng mới dưới các khối hiện có (tự cân đối layout theo trang dashboard hiện tại).
- [x] Verify tĩnh parse + đối chiếu style dashboard hiện có.

## Phase 7 — Liên kết Lệnh SX ↔ Hợp đồng bán + fix bug BOM ĐVT (yêu cầu 2026-07-03)

**Quyết định thiết kế:** `production_orders.contract_id` nullable → null = "Sản xuất để tồn kho", có giá trị = "SX phục vụ HĐ bán" (sale_contracts, chỉ gắn HĐ Đã duyệt). Không thêm enum mục đích riêng (YAGNI).

### Task 17: BE — contract_id trên lệnh SX + endpoints chọn HĐ

- [x] Migration `2026_07_03_000002_add_contract_id_to_production_orders_table.php`: `contract_id` unsignedBigInteger nullable sau `manager_id` + migrate dev.
- [x] Entity: fillable + relation `contract()` (belongsTo `Modules\Sale\Entities\SaleContract`) + accessor tên HĐ hiển thị (code + tên/khách hàng — xem SaleContract có field gì).
- [x] Request: `contract_id` nullable + exists sale_contracts; service validate khi có contract_id → HĐ phải Đã duyệt (ValidationException nếu không).
- [x] Service headerData nhận contract_id; index() filter `contract_id` (cho FE HĐ query) + eager load contract.
- [x] Resources List + Detail: `contract_id`, `contract_code`, `contract_label` (hoặc tương đương); null → FE hiện "SX tồn kho".
- [x] Endpoint `GET /production-orders/sale-contracts?keyword=` (checkPermission Thêm/sửa lệnh sản xuất, TRƯỚC /{id}): HĐ Đã duyệt — id, code, label (code - khách hàng), limit 20 theo keyword.
- [x] Endpoint `GET /production-orders/sale-contracts/{contractId}/items` (cùng permission): dòng hàng HĐ — product_id, product_code/name, unit_id/unit_name, conversion_rate, quantity (SL HĐ theo ĐVT dòng) — để FE đổ bảng thành phẩm.
- [x] php -l + smoke tinker + regression store không contract_id (tồn kho) vẫn OK.

### Task 18: BE — Hợp đồng bán hiển thị tình trạng SX

- [x] `Modules/Sale` DetailSaleContractResource (detail HĐ): thêm `production_orders` = mảng lệnh SX gắn HĐ (id, code, order_date, status/status_name/status_color, progress_percent nhập TP như dashboard) + per item dòng HĐ thêm `quantity_production_ordered` (tổng SL đặt SX các lệnh gắn HĐ, quy về ĐVT dòng HĐ qua conversion_rate) và `quantity_production_received` (tổng đã nhập kho từ SX các lệnh đó, phiếu APPROVED, quy về ĐVT dòng HĐ).
- [x] Query aggregate (group by product) — không N+1; KHÔNG sửa hành vi/field cũ của resource (HĐ đang chạy production flows khác).
- [x] php -l + smoke tinker (HĐ có 1 lệnh SX 1 phần → 2 cột đúng; HĐ không lệnh → 0/rỗng).

### Task 19: FE — Form/list/detail lệnh SX gắn HĐ

- [x] Store: actions `saleContracts(keyword)`, `saleContractItems(contractId)`.
- [x] Form: khối "Mục đích sản xuất" (đầu Thông tin chung): select 2 lựa chọn "Sản xuất để tồn kho" (default) / "SX theo hợp đồng bán" → hiện select HĐ (search keyword, options từ endpoint); chọn HĐ → confirm đổ dòng hàng HĐ vào bảng Thành phẩm (thay thế, SL = SL HĐ, sửa được) → auto bung NVL chạy như hiện tại; đổi về "tồn kho" → clear contract_id (giữ bảng TP). Edit mode load lại đúng (guard loading như đã làm).
- [x] List: cột "Hợp đồng" (contract_code link `/sale/contract/{id}`, null → "SX tồn kho"); Detail: dòng info Mục đích/HĐ (link).
- [x] Payload save/update + validate: chọn "theo HĐ" mà chưa chọn HĐ → lỗi inline.

### Task 20: FE — Detail HĐ bán hiển thị tình trạng SX

- [x] `pages/sale/contract/_id` (detail HĐ): tab "Thông tin xuất hàng" thêm 2 cột "SL đặt SX" + "SL SX đã nhập" (xanh khi đủ); khối mới "Lệnh sản xuất" (bảng: mã lệnh link `/warehouse/production-order/{id}`, ngày, trạng thái badge, tiến độ %; empty state "Chưa có lệnh sản xuất") — gate hiển thị `hasAPermission('Xem lệnh sản xuất')`.
- [x] KHÔNG phá layout/tab hiện có.

### Task 21: FE — Fix bug BOM trong hàng hoá: ĐVT NVL theo khai báo của mã NVL

- [x] Tìm component BOM inline trong form hàng hoá (Modules Category FE — tab BOM của ProductForm): cột ĐVT dòng NVL đang cho chọn toàn bộ danh mục Đơn vị tính → SỬA thành chỉ các ĐVT đã khai báo trong `product_units` của mã NVL đã chọn (pattern unitOptions per-row như ProductionOrderForm/WhTransferForm đang làm; đổi NVL → reset unit về ĐVT cơ bản/đầu danh sách; dữ liệu BOM cũ có unit ngoài danh sách → vẫn hiển thị nhưng khuyến khích chọn lại — xử lý mềm không phá data cũ).
- [x] Verify tĩnh parse + không phá validate/luu BOM hiện có.

## Phase 8 — Seeder demo BOM (yêu cầu 2026-07-03)

### Task 22: BomDemoSeeder — 10 thành phẩm đủ công thức BOM

- [x] Seeder `Modules/Category/Database/Seeders/BomDemoSeeder.php`: tạo 10 thành phẩm (product) + pool NVL (product) đủ dùng; mỗi thành phẩm 1 BOM active/default gồm ≥3 dòng NVL (norm_quantity, waste_percent hợp lý); mọi product (TP + NVL) có product_units (ĐVT cơ bản + quy đổi nếu hợp); unit_id dòng BOM PHẢI thuộc product_units của NVL (đúng quy tắc vừa fix); idempotent (chạy lại không nhân đôi — check theo code); KHÔNG TRUNCATE bảng nào.
- [x] Chạy trên DB dev + verify tinker: 10 BOM đủ ≥3 dòng; `ProductionOrderService::bomMaterials` bung được từ các thành phẩm này.

## Tiến độ thực thi (subagent-driven, ledger)

- Task 17d (Phase 7 BE): DONE (review Approved) — migration `2026_07_03_000002` contract_id nullable + index (đã migrate dev); assertContractApproved trong headerData (HĐ phải status=3); 2 endpoint `/production-orders/sale-contracts` (keyword code/KH, limit 20) + `/sale-contracts/{id}/items` (đủ conversion_rate — method riêng, không tái dùng bản WhReceiptService vì khác shape); resources + eager load contract.customer. Smoke 6/6 PASS.
- Task 18d (Phase 7 BE): DONE (review Approved; 2 fix sau review: loại lệnh TỪ CHỐI khỏi SUM "SL đặt SX" ($activeOrderIds — danh sách production_orders vẫn đủ trạng thái); guard conversion_rate=0 → ?: 1) — DetailSaleContractResource thêm per item quantity_production_ordered/received (quy ĐVT dòng HĐ) + key production_orders (progress_percent). 6 query aggregate cố định, field cũ nguyên, smoke PASS.
- Task 20d (Phase 7 FE): DONE (review Approved, 0 fix) — detail HĐ bán: tab "Thông tin xuất hàng" thêm 2 cột SL đặt SX / SL SX đã nhập (xanh khi đủ, colspan động theo gate) + khối "Lệnh sản xuất" (link, badge, progress bar pattern dashboard, empty state); gate hasAPermission('Xem lệnh sản xuất'); tab 1/footer/modal cũ nguyên vẹn.
- Task 19d (Phase 7 FE): DONE (review Needs fixes → đã fix Important: nâng limit endpoint sale-contracts 20→500, nhất quán tiền lệ WhIssueForm load HĐ per_page 500 + search local của Select2; param keyword giữ cho tương lai) — form khối "Mục đích sản xuất" (radio tồn kho/theo HĐ, select HĐ required inline, confirm đổ dòng HĐ vào bảng TP khi có dòng, auto bung chạy qua watcher — reviewer trace kỹ guard loading/materialsDirty không race); list cột Hợp đồng (link, null="SX tồn kho"); detail row Mục đích. Minor ghi nhận: contractItemsLoading chưa bind template (thiếu loading indicator); UX 2 confirm nối tiếp khi bảng TP có dòng + NVL dirty (cơ chế sẵn có, cần user test).
- Task 21d (Phase 7 FE fix bug BOM): DONE (review Approved) — `ProductForm.vue` tab BOM: cột ĐVT dòng NVL đổi từ danh mục ĐVT toàn cục → `bomUnitOptionsFor(row)` theo `product_units` của NVL (nguồn getAll đã trả sẵn, FE trước đây bỏ đi khi map); đổi NVL reset về ĐVT cơ bản (is_base_unit); data cũ unit ngoài danh sách giữ option fallback không phá form sửa. Diff 5 hunk, parse sạch.

- Task 15c (Phase 6 BE): DONE (review Approved, 0 fix) — WhDashboardService thêm key `production_orders` (pending_count status=2 / in_progress_count status=3 / completed_in_range theo completed_at trong top_from-top_to / in_progress max 10 sort expected_date nulls-last: product_summary, is_overdue, employee_manager_name, progress_percent + issued_percent — SUM group by, không N+1, không đụng 6 khối cũ). Smoke tinker PASS. Ghi chú: DB dev còn lệnh rác LSX-2026-00023 từ E2E cũ.
- Task 16c (Phase 6 FE): DONE (review Approved) — dashboard kho: card KPI "Lệnh SX chờ duyệt" (hàng 4 card col-lg-3, link list?status=2 — list đã thêm đọc route.query.status prefill filter) + khối bảng "Lệnh sản xuất đang thực hiện" (badge count, phụ đề hoàn thành trong kỳ, ngày dự kiến đỏ khi quá hạn, 2 progress bar % nhập TP/% xuất NVL, empty state, style dash-table hiện có). 2 khối mới gate `hasAPermission('Xem lệnh sản xuất')` (quyết định chủ động — link bên trong cần quyền 1139; muốn bỏ gate thì bỏ computed canViewProductionOrder).
- Tinh chỉnh 2026-07-03: thu nhỏ card KPI dashboard (class `.kpi-card` chung cả 2 hàng — padding 18/20/16→12/14/10, icon 42→32px, số 27→21px, blob 130→100px, label/sub/link giảm nhẹ) theo yêu cầu user; template + style verify cân bằng.

- Task 13b (Phase 5 BE): DONE (review Approved) — migration `2026_07_03_000001` thêm `manager_id` (đã migrate dev) + entity/request(exists:employees)/service/2 resource trả manager_id+employee_manager_name + endpoint `GET /production-orders/product-bom/{productId}` (chọn BOM cùng logic bomMaterials, checkPermission 1140, trước /{id}). + ListResource trả thêm is_can_submit/approve/complete (controller sửa inline cho button list).
- Task 14b (Phase 5 FE): DONE (review Needs fixes → đã fix 2: (Critical) hạ `loading=false` trong `$nextTick` để guard watcher hiệu lực khi mở Edit — tránh auto bung ghi đè NVL đã lưu; (Important) `beforeDestroy` clearTimeout debounce). Nội dung: bỏ nút bung → auto bung theo BOM khi bảng TP đổi (debounce 400ms, flag materialsDirty confirm ghi đè, edit mode mặc định dirty=true, toast without-bom chống spam); icon `ri-file-list-3-line` mỗi dòng TP → popup BOM công thức (modal-popup convention); select "Người phụ trách SX" (allEmployeesOptions) cùng row trước Ghi chú + hiện ở detail; list thêm 4 button workflow (Gửi duyệt/Duyệt/Từ chối modal lý do/Hoàn thành) gate is_can_* + quyền, catch 422 toast + reload. Parse template/script sạch.

- Task 1: DONE (review Approved) — 5 migration + FK cascade 2 bảng dòng (mirror wh_transfer_items), migrate + FK dev DB verified.
- Task 2: DONE (review Approved) — 3 entity mới + WhIssue loại 3/WhReceipt loại 4 + production_order_id + relation.
- Task 3: DONE (review Approved sau fix: bọc DB::transaction store/update/destroy + guard product_id syncRows) — ProductionOrderService, smoke tinker PASS.
- Task 4: DONE (review Approved) — Request/2 Resource/Controller/10 routes + permission 1139/1140/1141 "Lệnh sản xuất" type=10 (tên quyền "Thêm/sửa lệnh sản xuất" theo format seeder); DB dev đã insert + gán role 1 + cache reset. Full flow tinker PASS.
- Task 5: DONE (review opus Approved; fix Important đã làm: migration 000006 down() UPDATE null→0 trước khi khôi phục NOT NULL) — WhIssue loại 3: Request/headerData/store-update validate items⊆materials + ép giá null/approve→assertProductionRemaining (lock header lệnh, SUM APPROVED khác, +1e-6, chặn COMPLETED)/productionRemaining endpoint + route + resources. Migration PHÁT SINH `000006_make_wh_issue_price_columns_nullable` (deploy nhớ chạy). Smoke + regression loại 2 PASS.
- Task 6: DONE (review opus Approved, 0 fix) — WhReceipt loại 4 đối xứng T5 (assertProductionRemaining phía nhập so production_order_products, productionRemaining không cần kho, route + resources). Migration PHÁT SINH `000007_make_wh_receipt_price_columns_nullable` (down() có UPDATE null→0). 22/22 assertion + regression loại 2/3 PASS.
- Task 7: DONE — smoke E2E BE tinker 10/10 PASS (bung BOM đúng công thức + gộp, luồng lệnh, xuất/nhập từng phần + chặn vượt, complete khoá phiếu, stock-card/dashboard không lỗi, regression loại cũ OK), 0 bug, transaction rollback sạch. Ghi chú: DB dev còn rác test cũ (11 kho KHO.E2E/E2E_WH + 1 E2E_PROD) từ các session trước — nên dọn tay.
- Task 8: DONE (review Approved) — store warehouse-production-order (10 action) + menu "Lệnh sản xuất" (ri-tools-line, isShow Xem lệnh sản xuất) + list page theo khuôn transfer (badge BE color, Sửa/Xóa gate is_can_* + quyền 1140).
- Task 9: DONE (review Needs fixes → đã fix icon ri-flow-chart→ri-git-merge-line (class có thật trong font local)) — ProductionOrderForm (2 bảng + bung BOM confirm ghi đè + cảnh báo products_without_bom + validate touched inline) + create/edit pages, parse template sạch. Ghi chú kế thừa pattern WhTransferForm (không sửa, ghi nhận cho final review): 422 chỉ toast không map inline từng field (khuôn gốc cũng vậy); save OK nhưng submit/approve fail → form vẫn mode create có thể tạo trùng; 3 nút footer đều primary.
- Task 10: DONE (review Approved) — detail lệnh: 2 bảng tiến độ (Đã nhập/Đã xuất quy ĐVT dòng, fallback rate 1), phiếu gắn lệnh link 2 chiều, footer đủ workflow + Hoàn thành confirm cảnh báo động, 2 nút tạo phiếu prefill query.
- Task 11: DONE (review Needs fixes → đã fix Critical: guard `this.loading` cho watcher form.warehouse_id chống race ghi đè SL đã lưu khi mở Sửa phiếu loại 3) — WhIssueForm loại 3 (select lệnh status=3, checkbox + Còn phải xuất + Tồn khả dụng, ẩn giá, prefill query), store action productionRemaining, list/detail label + link lệnh + ẩn giá. sort_order FE không gửi = OK (BE gán theo index, giống loại 1).
- Task 12: DONE (review Approved, 0 fix) — WhReceiptForm loại 4 (select lệnh, checkbox + Còn phải nhập, ẩn giá, prefill query, clear state đổi loại 2 chiều, edit merge giữ SL đã lưu không race vì remaining phía nhập không phụ thuộc kho), store action, detail link lệnh + ẩn giá, list dùng receipt_type_name sẵn.
- Minor tồn đọng cho final review: (T2) diff WhIssue/WhReceipt realign whitespace const cũ; (T4) ProductionOrderController::approve không lockForUpdate như WhTransferController (chấp nhận được vì approve lệnh chỉ đổi status); seeder Permission::create MassAssignmentException là vấn đề CÓ SẴN toàn seeder trên dev (ngoài scope); (T5) assertProductionRemaining chỉ chặn COMPLETED không chặn REJECTED-sau-approve (nghiệp vụ hiện không revert lệnh đã duyệt); (T5) lock order inventory→order khác thứ tự tiềm năng deadlock (chưa có luồng ngược); (T5) route contract-remaining cũ không middleware còn production-remaining mới có (chủ đích theo spec).

- Task E2E Playwright: DONE — 2 spec mới `e2e/tests/warehouse/production-order.spec.ts` + `production-order.api.spec.ts`: **11/11 PASS**; bộ cũ 10/12 PASS (2 fail là bug selector CÓ SẴN ở issue.spec/receipt.spec — input[type=number] khớp cả cột Đơn giá — không liên quan feature, đã ghi gợi ý fix trong task-e2e-report). 3 fix trong lúc E2E: (1) test.describe.serial cho 2 spec mới; (2) **WhReceiptRequest.receipt_type trả về nullable** (T6 lỡ đổi required làm 3 test cũ fail — regression đã fix, có comment); (3) selector label "Xuất khác" trong WarehouseIssuePage.ts (label đổi do feature). Lưu ý: E2E phiên này chạy API/Client cổng 8100/3100 vì 3000/8000 bị project khác chiếm.
- Task Final review (opus): **SẴN SÀNG BÀN GIAO** — spec coverage đủ (2 deviation chấp nhận: bom-materials là POST, production-remaining theo path /production-order/{id}/remaining — FE/BE khớp nhau); cross-check issue↔receipt đối xứng; mọi Minor tồn đọng triaged CHẤP NHẬN; các fix muộn không side-effect. 1 đề xuất fix sau (không chặn): ProductionOrderForm save-thành-công-nhưng-submit-fail vẫn ở mode create → có thể tạo trùng khi bấm Lưu lại (kế thừa khuôn WhTransferForm; fix gợi ý: chuyển mode='edit' sau save).

- Task 22e E2E Phase 5-7: DONE — **16/16 test mới PASS** (A auto bung + popup BOM + người phụ trách + confirm dirty; B button workflow list; C dashboard card + khối SX; D liên kết HĐ API 200/422 + UI đổ dòng + detail HĐ 2 cột/khối lệnh; E BOM ĐVT theo product_units). Full suite 55/57 — 2 fail là bug selector CŨ đã biết (issue/receipt.spec input[type=number]). **0 bug ứng dụng**; 5 fix chỉ trong code test. Môi trường: client chạy Node 12.22.12 (14 không có trên máy) vẫn ổn.

- Task 22 (Phase 8): DONE — `BomDemoSeeder` (Modules/Category): 10 TP `SXTP.0001-0010` (thiết bị trường học) + pool NVL dùng chéo, 10 BOM active/default 36 dòng (≥3/BOM), unit_id dòng BOM ∈ product_units NVL (0 dòng sai), bomMaterials bung + gộp đúng, idempotent (chạy 2 lần count không đổi), KHÔNG truncate. Ghi chú: norm_quantity là cột INTEGER (chỉ định mức nguyên); tạo thêm 2 loại hàng LHH.TPSX/LHH.NVLSX + 5 unit (Mét/Kg/Lít/Cuộn/Cây); mã BOM đặt tay `BOM-{mã TP}` (Bom entity không có getNextCode).

### Checkpoint — 2026-07-03 (wrap up 2, cuối ngày)
Vừa hoàn thành: TOÀN BỘ 8 PHASE — core (P1-4, E2E 11/11 + final review opus SẴN SÀNG BÀN GIAO) + P5 tinh chỉnh form/list + P6 dashboard + P7 liên kết HĐ bán 2 chiều + fix bug BOM ĐVT + P8 BomDemoSeeder (10 TP SXTP.0001-0010, 36 dòng BOM). E2E Phase 5-7: 16/16 PASS (full suite 55/57, 2 fail selector cũ đã biết). Bugfix ngoài feature: V2BaseSelectRemote dropdownParent (popup BOM builder Giao việc — ghi ở .plans/product-bom/plan.md, cần user verify browser). Tất cả CHƯA COMMIT (branch quotation, 2 repo + e2e).
Đang làm dở: —
Bước tiếp theo: user test trình duyệt các phần mới (mục đích SX theo HĐ → đổ dòng → auto bung; 2 cột SX + khối lệnh SX trên detail HĐ; BOM ĐVT; dropdown popup BOM builder; seeder SXTP) → yêu cầu commit. Deploy: 9 migration (2026_07_02_000001..000007 + 2026_07_03_000001..000002); 3 permission 1139-1141 insert tay (KHÔNG seeder) + gán role + cache:clear; BomDemoSeeder chạy tùy chọn nếu cần data demo; dọn rác DB dev (kho KHO.E2E cũ + lệnh LSX-2026-00023).
Blocked: —

### Checkpoint — 2026-07-03 (wrap up)
Vừa hoàn thành: TOÀN BỘ FEATURE (12 task subagent-driven + E2E Playwright + final review opus SẴN SÀNG BÀN GIAO). BE smoke 10/10, E2E mới 11/11 PASS. Đã xác nhận với user: DB dev đã migrate đủ 7 migration (batch 443-446) + schema/permission verify OK — "Nothing to migrate" là bình thường. Chưa commit.
Đang làm dở: —
Bước tiếp theo: user test trình duyệt (re-login để nhận quyền mới → menu "Lệnh sản xuất") + commit 2 repo (nhatlinh-api, nhatlinh-client + e2e) khi có yêu cầu. Deploy môi trường khác: chạy đủ 7 migration 2026_07_02_000001..000007 (000006/000007 dễ quên — thiếu là lưu phiếu loại 3/4 lỗi NOT NULL); insert tay 3 permission 1139-1141 "Lệnh sản xuất" type=10 + gán role + cache:clear (KHÔNG chạy seeder — TRUNCATE); dọn rác DB dev (11 kho KHO.E2E/E2E_WH + E2E_PROD của session cũ). Đề xuất fix sau (không chặn): ProductionOrderForm save-OK-nhưng-submit-fail → chuyển mode='edit' tránh tạo trùng; 2 test E2E cũ (issue/receipt.spec) fail do selector input[type=number] có sẵn.
Blocked: —
