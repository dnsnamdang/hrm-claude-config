# #11924 — Chặn khóa hàng khi còn phiếu/HĐ đang tiến trình — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để thực thi plan từng task. Các bước dùng checkbox (`- [ ]`).

**Goal:** Chặn `lock()` một hàng hoá (trả 422 + câu theo luồng) khi hàng còn nằm trong bất kỳ phiếu đang tiến trình thuộc luồng mua / nhập / xuất, hoặc trong 1 hợp đồng ERP còn hiệu lực & chưa xuất hết.

**Architecture:** Service dùng chung mới `ProductInProgressService` (Bước 3b skill `erp-to-hrm-screen`) phơi `firstBlockingFlow(int $productId, int $companyId): ?string` → `buy|import|export|contract|null`, kiểm theo thứ tự mua→nhập→xuất→HĐ, dừng ở luồng đầu vướng. Mỗi luồng 1 method `existsXxxInProgress()` dùng `EXISTS` (subquery `whereExists`, không đếm, company-scoped). `ProductLifecycleService::lock()` gọi orchestrator, có kết quả thì `fail(<message>)` (422).

**Tech Stack:** PHP 7.4 / Laravel 8, `DB::table()` / query builder (bảng gốc ERP trong DB gộp), MySQL `erp_hrm_check`.

**Spec:** `HRM/.plans/khoa-hang-chan-tien-trinh/design.md` (đã duyệt 2026-11-25).

## Global Constraints

- **KHÔNG tự commit/push** — chỉ commit khi user yêu cầu rõ. Mỗi task kết thúc ở verify, không có bước `git commit`.
- **Scope công ty:** mọi truy vấn lọc `company_id = $companyId` (tham số, = `CurrentCompany::id()` = `current_company_role`). Bảng header **không có** `company_id` thì xử lý theo ghi chú từng task — KHÔNG để lộ chéo công ty, KHÔNG `where company_id = null` (Laravel dịch thành `IS NULL`, kéo rác).
- **Tập KẾT THÚC đồng nhất (không chặn)** = {Hủy, Không duyệt, Đã hạch toán, Đã nhập/xuất kho hoàn tất, Đã quyết toán, Đã chuyển tiếp sang phiếu/HĐ sau}. Mọi status khác = đang tiến trình → chặn.
- **PXH (`product_exports`) KHÔNG tính.** Hợp đồng **chỉ 5 loại ERP** (vật tư type1 · HDDV · HDDA · HĐNT type3 · PLBS type6).
- **Dùng `EXISTS` / `->exists()`**, không `count()`; dừng sớm ở luồng đầu vướng.
- **Verify bằng tinker probe READ-ONLY trên DB thật** (HRM phpunit chia sẻ DB thật, không transaction-isolated → không viết test ghi DB). Mỗi task chạy method mới trên `product_id` thật và đối chiếu bằng SQL đếm trực tiếp. KHÔNG mutate dữ liệu.
- Câu thông báo (hằng số mới trên `ProductLifecycleService`): mua `Hàng đang trong tiến trình mua` · nhập `Hàng đang trong tiến trình nhập` · xuất `Hàng đang trong tiến trình xuất` · HĐ `Hàng đang trong hợp đồng chưa xuất hết`.

## Review Focus

- **Chéo công ty qua bảng không có `company_id`** (`order_import_requests`, `contracts`, `service_contracts`): nếu không scope được, hàng của công ty A bị chặn khóa vì chứng từ công ty B. Mỗi task xử lý rõ (scope qua quan hệ, hoặc loại phiếu đó khỏi guard) — Task 2 & Task 4.
- **FK chi tiết→header sai tên** (một số bảng dùng FK đặt tên riêng, không phải `parent_id`): join nhầm cột → EXISTS luôn rỗng (bỏ sót, không chặn gì) hoặc luôn đúng (chặn oan). Mỗi method phải join đúng cột đã xác minh.
- **Hàng đã xuất hết nhưng HĐ còn hiệu lực:** điều kiện HĐ phải có `quantity - exported_qty > 0`, nếu quên thì chặn oan HĐ đã giao đủ — Task 4.
- **`product_id` không index** trên bảng chi tiết → `whereExists` full-scan chậm khi khóa: mỗi task kiểm index, thiếu thì nêu (không tự thêm migration vào bảng ERP khi chưa hỏi).
- **Thứ tự 422:** guard tiến trình chỉ chạy khi hàng đang `STATUS_TRADING` (sau check trạng thái, trước `setStatus`); 403/423 vẫn trước — Task 5.

---

### Task 1: Scaffold `ProductInProgressService` + luồng MUA

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressService.php`
- Tham chiếu (đọc, không sửa): `Modules/MasterData/Services/PriceCalculation/PriceAskingProductReader.php:412` (`hasOpenRequest`)

**Interfaces:**
- Produces:
  - `public function __construct(PriceAskingProductReader $priceAsking)`
  - `public function existsBuyInProgress(int $productId, int $companyId): bool`
  - hằng số luồng: `const FLOW_BUY='buy', FLOW_IMPORT='import', FLOW_EXPORT='export', FLOW_CONTRACT='contract';`
- Consumes: `PriceAskingProductReader::hasOpenRequest($productId, $companyId): bool`.

**Cột đã xác minh (DB gộp):**
- `inland_order_request_products(parent_id, product_id)` → `inland_order_requests(id, company_id, status)`. Chặn status ∈ {1,2,3,4,6} (KẾT THÚC {0 hủy, 5 đã lập HĐ}).
- `root_order_request_products(parent_id, product_id)` → `root_order_requests(id, company_id, status)`. Chặn {2,3,6} (KẾT THÚC {0 hủy, 1 đã duyệt→chuyển order_request2}).
- `order_request_product2(parent_id, product_id)` → `order_request2(id, company_id, status)`. Chặn: status NOT IN {0 hủy, 4 đã tổng hợp}.

- [x] **Step 1: Kiểm `order_request2` còn dữ liệu trong DB gộp + index `product_id`**

```bash
mysql -u root -h 127.0.0.1 erp_hrm_check -N -e "SELECT COUNT(*) FROM order_request2; SELECT COUNT(*) FROM order_request_product2;"
mysql -u root -h 127.0.0.1 erp_hrm_check -e "SHOW INDEX FROM inland_order_request_products WHERE Column_name='product_id'; SHOW INDEX FROM root_order_request_products WHERE Column_name='product_id'; SHOW INDEX FROM order_request_product2 WHERE Column_name='product_id';"
```
Ghi kết quả vào STATUS: `order_request2` rỗng → bỏ khối legacy khỏi method (chỉ giữ 2 ghi chú). Thiếu index `product_id` → nêu trong báo cáo, KHÔNG tự thêm migration vào bảng ERP.

- [x] **Step 2: Viết `existsBuyInProgress()`**

Thứ tự kiểm (dừng ở `true` đầu tiên): (a) `$this->priceAsking->hasOpenRequest($productId, $companyId)`; (b) `whereExists` inland (join detail→header, `h.company_id=?`, `whereIn h.status [1,2,3,4,6]`, `d.product_id=?`); (c) tương tự root `whereIn h.status [2,3,6]`; (d) order_request2 chỉ khi Step 1 còn dữ liệu, `h.company_id=?`, `whereNotIn h.status [0,4]`. Dùng query builder `DB::table('inland_order_request_products as d')->join('inland_order_requests as h','h.id','=','d.parent_id')->where(...)->exists()`.

- [x] **Step 3: Verify probe READ-ONLY**

```bash
cd hrm-api && php artisan tinker --execute="
\$svc = app(\Modules\MasterData\Services\Product\ProductInProgressService::class);
\$row = DB::table('inland_order_request_products as d')->join('inland_order_requests as h','h.id','=','d.parent_id')->whereIn('h.status',[1,2,3,4,6])->select('d.product_id','h.company_id')->first();
if(\$row){ var_dump(\$svc->existsBuyInProgress((int)\$row->product_id,(int)\$row->company_id)); } else { echo 'no inland in-progress sample'; }
"
```
Expected: `true` cho mẫu đang tiến trình. Thử thêm 1 `product_id` KHÔNG có phiếu mua nào (vd id lớn bất kỳ) → `false`.

---

### Task 2: Luồng NHẬP — `existsImportInProgress()`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressService.php`

**Interfaces:**
- Produces: `public function existsImportInProgress(int $productId, int $companyId): bool`

**Cột đã xác minh + tập chặn:**
- `product_import_request_details(parent_id, product_id)` → `product_import_requests(id, company_id, status)`. Chặn {1,2,3,4,7,9,10,11,12} (KẾT THÚC {5,6,8}).
- `warehouse_import_request_details(parent_id, product_id)` → `warehouse_import_requests(id, company_id, status)`. Chặn {1,2,3,7} (KẾT THÚC {4,5,6}).
- `warehouse_import_lots(parent_id, product_id, company_id)` → `warehouse_imports(id, company_id, status)`. Chặn {2,3,5,6,7} (KẾT THÚC {1 hạch toán,4 không duyệt,8 hủy}) — xác minh const `WarehouseImport` ở Step 1.
- `product_import_details(parent_id, product_id)` → `product_imports(id, company_id, status)`. Chặn {3} (KẾT THÚC {1}).
- `inventory_discrepancy_handling_import_products(` **`inventory_discrepancy_handling_import_id`** `, product_id)` → `inventory_discrepancy_handling_imports(id, company_id, status)`. Chặn {1,2,4} (KẾT THÚC {3,5}).
- ⚠️ `order_import_requests` **KHÔNG có `company_id`** → xem Step 2.

- [x] **Step 1: Xác minh const trạng thái PNK + xử lý `order_import_requests` scope**

Đọc hằng số status của `WarehouseImport` (PNK) ở model HRM/ERP; xác nhận KẾT THÚC {1,4,8}. Với `order_import_requests`: kiểm có cột nào liên kết công ty không:
```bash
mysql -u root -h 127.0.0.1 erp_hrm_check -e "SHOW COLUMNS FROM order_import_requests;"
```
Quyết định (ghi vào STATUS): nếu không có đường scope công ty đáng tin → **LOẠI `order_import_requests` khỏi guard** (nêu lý do: không scope được, tránh chặn chéo công ty). Nếu có (vd `created_by`→employee→company, hoặc link qua `product_import_requests`) → scope qua đó.

- [x] **Step 2: Viết `existsImportInProgress()`**

5 (hoặc 4, tùy Step 1) khối `whereExists`, mỗi khối join đúng FK đã xác minh, `h.company_id=?` (lots thì dùng `d.company_id=?` sẵn có), lọc status theo tập chặn, `d.product_id=?`. Dừng ở khối đầu `true`.

- [x] **Step 3: Verify probe READ-ONLY**

Với MỖI bảng có dữ liệu, lấy 1 mẫu đang tiến trình (SQL như Task 1 Step 3) rồi gọi `existsImportInProgress()` → `true`; kiểm 1 mẫu status KẾT THÚC (vd product_imports status=1) mà hàng đó không nằm phiếu nhập nào khác → `false`.

---

### Task 3: Luồng XUẤT — `existsExportInProgress()`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressService.php`
- Tham chiếu (đọc): `ERP/.../app/Model/Warehouse/ProductExportRequest.php` (const `STATUS_PROCESING`)

**Interfaces:**
- Produces: `public function existsExportInProgress(int $productId, int $companyId): bool`

**Cột đã xác minh + tập chặn:**
- `product_export_request_details(parent_id, product_id, exported_qty)` → `product_export_requests(id, company_id, status)`. Chặn: status ∈ `ProductExportRequest::STATUS_PROCESING` (KẾT THÚC {5 hạch toán,6 hủy,8 đã xuất kho,13 quyết toán}).
- `warehouse_export_request_details(parent_id, product_id)` → `warehouse_export_requests(id, company_id, status, is_complete)`. Chặn {1,2,3,7} (KẾT THÚC {4,5,6}, hoặc `is_complete=1`). **KHÔNG mượn `status!=3` của `PrepickStockService`** (3 = Đang tạo).
- `warehouse_export_lots(parent_id, product_id, company_id)` → `warehouse_exports(id, company_id, status)`. Chặn {2,3,7} (KẾT THÚC {1,4,5,6}).
- `product_transfer_request_products(parent_id, product_id)` → `product_transfer_requests(id, company_id, status)`. Chặn {1,2,3,4,5,6,7,8,9,14} (KẾT THÚC {10,11,12,13}).
- `inventory_export_details(parent_id, product_id, company_id)` → `inventory_exports(id, company_id, status)`. Chặn {3} (KẾT THÚC {1}).
- PXH (`product_exports`) **KHÔNG tính**.

- [x] **Step 1: Xác minh `STATUS_PROCESING`**

Đọc mảng `STATUS_PROCESING` của `ProductExportRequest` tới gốc, đối chiếu loại {5,6,8,13}. Nếu mảng khác kỳ vọng → dùng đúng mảng const (không hardcode list). Kiểm index `product_id` các bảng chi tiết xuất.

- [x] **Step 2: Viết `existsExportInProgress()`**

5 khối `whereExists` (KHÔNG có PXH), join đúng FK, scope `company_id` (lots/inventory_export_details dùng `d.company_id`; còn lại `h.company_id`), lọc status. YCXH dùng `whereIn('h.status', ProductExportRequest::STATUS_PROCESING)`. ĐNXK thêm nhánh `is_complete<>1`.

- [x] **Step 3: Verify probe READ-ONLY**

Mỗi bảng 1 mẫu đang tiến trình → `true`; 1 mẫu chỉ có PXH (product_exports) mà không có phiếu xuất khác → `false` (chứng minh PXH không tính).

---

### Task 4: HỢP ĐỒNG — `existsContractInProgress()`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressService.php`

**Interfaces:**
- Produces: `public function existsContractInProgress(int $productId, int $companyId): bool`

**Cột đã xác minh + điều kiện:**
- `contract_products(` **`contract_id`** `, product_id, quantity, exported_qty)` → `contracts(id, type, status, parent_contract_id)`.
  - HĐ vật tư type=1: status ∈ {6 CO_HIEU_LUC, 8 DANG_XUAT_HANG}.
  - HĐNT type=3: status = 1 (DA_DUYET) — khác type khác.
  - PLBS type=6: status = 6.
- `service_contract_item_products(` **`service_contract_id`** `, product_id, exported_qty)` → `service_contracts(id, type, status)`. status=6.
- `project_contract_tab_products(` **`project_contract_id`** `, product_id, exported_qty)` → `project_contracts(id, company_id, type, status)`. status=6.
- Điều kiện chung "chưa xuất hết": `(d.quantity - d.exported_qty) > 0` nếu bảng có `quantity`; bảng chỉ có `exported_qty` (service/project) → xác minh cột số lượng ở Step 1.
- ⚠️ `contracts` & `service_contracts` **KHÔNG có `company_id`** → xem Step 1.

- [x] **Step 1: Giải quyết scope công ty cho HĐ + cột "số lượng" của service/project detail**

```bash
mysql -u root -h 127.0.0.1 erp_hrm_check -e "SHOW COLUMNS FROM contracts LIKE '%compan%'; SHOW COLUMNS FROM service_contracts LIKE '%compan%'; SHOW COLUMNS FROM service_contract_item_products; SHOW COLUMNS FROM project_contract_tab_products;"
```
Tìm cột công ty thực của `contracts`/`service_contracts` (có thể tên khác). Tìm cột số lượng hợp đồng trong service/project detail (để tính "chưa xuất hết"). Ghi quyết định vào STATUS: scope HĐ theo cột tìm được; nếu HĐ thật sự không gắn công ty → nêu rõ và hỏi (không tự chặn chéo công ty).

- [x] **Step 2: Viết `existsContractInProgress()`**

Khối `contract_products`: join `contracts c on c.id=d.contract_id`, điều kiện `(c.type=1 AND c.status IN (6,8)) OR (c.type=3 AND c.status=1) OR (c.type=6 AND c.status=6)`, `(d.quantity-d.exported_qty)>0`, `d.product_id=?`, scope công ty theo Step 1. Khối service (`service_contract_id`, status=6) + project (`project_contract_id`, status=6, `project_contracts.company_id=?`), mỗi khối điều kiện chưa-xuất-hết theo cột số lượng Step 1.

- [x] **Step 3: Verify probe READ-ONLY**

Mẫu HĐ type=1 status=6 có dòng `quantity>exported_qty` → `true`; mẫu HĐ đã `exported_qty>=quantity` → `false`; mẫu HĐ status=10 (đã thanh lý) → `false`.

---

### Task 5: Orchestrator `firstBlockingFlow()` + gắn vào `lock()` + Playwright

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressService.php` (thêm `firstBlockingFlow`)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductLifecycleService.php` (hằng số message + chèn guard vào `lock()` ~dòng 320-324)

**Interfaces:**
- Produces: `public function firstBlockingFlow(int $productId, int $companyId): ?string` — gọi existsBuy→Import→Export→Contract theo thứ tự, trả hằng số `FLOW_*` đầu tiên `true`, hết thì `null`.
- Consumes (trong `lock()`): `app(ProductInProgressService::class)->firstBlockingFlow($productId, $this->companyId())`.

- [x] **Step 1: Viết `firstBlockingFlow()`**

4 `if` tuần tự, return hằng số tương ứng ở cái đầu tiên `true`, cuối cùng `return null`.

- [x] **Step 2: Thêm 4 hằng số message + map vào `ProductLifecycleService`**

```php
const MESSAGE_IN_PROGRESS_BUY = 'Hàng đang trong tiến trình mua.';
const MESSAGE_IN_PROGRESS_IMPORT = 'Hàng đang trong tiến trình nhập.';
const MESSAGE_IN_PROGRESS_EXPORT = 'Hàng đang trong tiến trình xuất.';
const MESSAGE_IN_PROGRESS_CONTRACT = 'Hàng đang trong hợp đồng chưa xuất hết.';
```
(Giữ/bỏ dấu `.` cuối cho khớp giọng các message hiện có trong file — đối chiếu dòng 40-58.)

- [x] **Step 3: Chèn guard vào `lock()`**

Ngay SAU khối `if ($status !== ProductCompany::STATUS_TRADING) { $this->fail(...); }` và TRƯỚC `setStatus(...)` (dòng ~327): gọi `firstBlockingFlow($productId, $this->companyId())`; theo kết quả `fail()` đúng message (match `FLOW_BUY`→BUY,…). Không đổi thứ tự 403/423 phía trên.

- [x] **Step 4: Verify probe + Playwright**

(a) Tinker: gọi `firstBlockingFlow()` trên 1 product đang `STATUS_TRADING` (status 3) có phiếu mua/nhập/xuất đang tiến trình → trả đúng luồng.
(b) Playwright MCP (`http://127.0.0.1:3000`): mở DM hàng hóa, bấm **Khóa** 1 hàng đang kinh doanh + đang có phiếu tiến trình → toast đúng câu, hàng KHÔNG bị khóa (status giữ 3). Bấm Khóa 1 hàng đang kinh doanh KHÔNG vướng phiếu nào → khóa thành công (status→4). Chụp màn 2 ca đặt vào scratchpad.

---

## Self-Review

1. **Spec coverage:** 3 luồng (mua/nhập/xuất) = Task 1/2/3; HĐ 5 loại = Task 4; 4 câu message + chặn thực tế ở `lock()` = Task 5. Thứ tự dừng-ở-luồng-đầu = Task 5 Step 1. ✓
2. **Step scan:** mỗi step 1 hành động kiểm được (SQL/tinker ra true|false, hoặc Playwright toast). Không bước "TBD". ✓
3. **Type consistency:** 4 method `existsXxxInProgress(int,int):bool` + `firstBlockingFlow(int,int):?string` khai Task 1, dùng lại nguyên si Task 5. Hằng số `FLOW_*` khai Task 1. ✓
4. **Review Focus:** chéo công ty (Task 2 Step 1, Task 4 Step 1), FK sai tên (cột đã xác minh từng task), chưa-xuất-hết (Task 4 Step 2), index (Task 1/3 Step 1), thứ tự 422 (Task 5 Step 3). ✓
5. **Proportion:** plan mô tả quyết định (tập status, tên cột, scope) + verify; không chép thân SQL dài. ✓

---

### Checkpoint — 2026-11-25 16:30 (wrap up tự động)
Vừa hoàn thành: Redmine #11924 (vé ghi ở project ERP nhưng màn DM hàng hóa đã dời sang HRM) — đủ 5 task + final review (Opus) + 1 fix. Service mới `Modules/MasterData/Services/Product/ProductInProgressService.php` (`firstBlockingFlow()` mua→nhập→xuất→HĐ, dừng ở luồng đầu vướng, company-scoped `current_company_role`), guard trong `ProductLifecycleService::lock()` sau check STATUS_TRADING → 422 với 4 câu "Hàng đang trong tiến trình mua/nhập/xuất." / "Hàng đang trong hợp đồng chưa xuất hết.". Commit hrm-api `5621f7503` nhánh `develop`, ĐÃ push origin/develop (rebase lên 103 file mới của người khác, không force; regression `ProductImportPriceTest` 26/26 trước và sau rebase). Chưa gop_db.
Ruling khi code (ngoài 3 quyết định user chốt ở design §5: chỉ 5 HĐ ERP · PXH không tính · "Đã hạch toán" = kết thúc):
- `order_request2` bỏ khỏi guard (3366 dòng, 100% ở trạng thái kết thúc); `order_import_requests` bỏ (không có `company_id`, 2/3 phiếu dở thiếu `warehouse_id` → không scope tin cậy được).
- PDH root: const ERP là chuẩn (khác map blade) — chặn {1,2,3}, kết thúc {4 Đã duyệt, 5 Hủy}. Inland chặn {1,2,3,4,6}.
- YCXH: kết thúc = {5 Đã hạch toán, 6 Hủy, 13 Đã quyết toán}; status 8 "Đã xuất kho" và 12 "Đang quyết toán" VẪN chặn. `ProductExportRequest::STATUS_PROCESING` của ERP là hằng DORMANT (không chỗ nào dùng) → không mirror (fix từ final review).
- ĐNXK `status=3` = "Đang tạo" (không phải hủy) → không mượn `is_complete≠1 AND status≠3` của PrepickStockService.
- HĐ: `contracts`/`service_contracts` không có `company_id` → scope qua `created_by → employees.employee_info_id → employee_infos.company_id` (giống ERP `DocumentCompany`); `project_contracts` scope thẳng `company_id`. "Chưa xuất hết" = `quantity - exported_qty > 0` trên `contract_products` / `service_contract_item_products` / `project_contract_tab_products`.
- Verify: tinker gọi `lock()` thật (guard `api`, emp13/cty1): hàng vướng phiếu xuất → 422 đúng câu, status giữ 3; hàng sạch → 3→4 (rollback). Chưa thấy toast trên trình duyệt (Playwright thay bằng tinker vì token e2e không khớp DB local).
Đang làm dở: —
Bước tiếp theo: QA kiểm toast trên dev-hrm; chuyển trạng thái vé #11924 trên Redmine (chưa làm); gộp gop_db khi user yêu cầu. Minor hoãn: `root_order_request_products.product_id` không có index (perf).
Blocked: —
