# Port màn Phiếu yêu cầu hãng bảo hành (FirmWarrantyRequest) ERP → HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để thực thi plan theo từng task. Các step dùng checkbox (`- [ ]`) để theo dõi.

**Goal:** KD lập/sửa/nháp/gửi-duyệt/xóa-nháp/in **Phiếu yêu cầu hãng bảo hành** trên HRM, ghi thẳng 4 bảng ERP; khâu mua hàng (XNK) vẫn chạy nguyên trên ERP.

**Architecture:** Phương án A "KD lập ở HRM, XNK ở ERP" — bám đúng khuôn 2 bản port tuần này (`delivery-cost-asking-requests`, `inland-order-requests`). Model HRM trỏ `$table` vào bảng ERP (DB gộp), KHÔNG migration, KHÔNG `$connection`. HRM chỉ set `status` 1/2; ERP giữ duyệt/gửi hãng/downstream. Chuông 2 chiều: HRM→ERP khi Gửi duyệt (ghi thẳng `notifications`), ERP→HRM khi "Không duyệt" (Guzzle `notify-result`).

**Tech Stack:** hrm-api = Laravel 8/PHP 7.4, `Modules/Finance`, spatie-permission. hrm-client = Nuxt 2.14/Vue 2, Bootstrap-Vue, V2Base*. ERP = Laravel 6.2 (nhánh `develop_02`).

**Spec:** `HRM/docs/superpowers/specs/2026-11-20-phieu-yeu-cau-hang-bao-hanh-port-design.md` (đã duyệt — D1/D2/D3 chốt 20/11).

**Màn khuôn (copy 1:1 pattern):** `hrm-api/Modules/Finance/.../DeliveryCostAskingRequest*` và `hrm-client/pages/finance/delivery-cost-asking-requests/*`. Mỗi file HRM mới = anh em tương ứng + phần "nhiều hơn" của warranty (bảng con items/costs, HĐ đa hình, serial, in_stock, đính kèm).

**Nguồn ERP (đọc để lấy validate/đổ dữ liệu/mã bút toán — KHÔNG port UI):**
- `ERP/TanPhatDev/app/Http/Controllers/Order/FirmWarrantyRequestController.php` (store/update/syncProducts/checkData; AssignHistory dòng ~186-190; `approver_id` comment dòng ~200; `approve()` = **code chết**, KHÔNG port).
- `ERP/TanPhatDev/routes/web.php:2610-2619` (route gốc).
- `ERP/TanPhatDev/app/Http/Controllers/Customercare/WrApproveResultsController.php` → `notifyHrmImportResult` (khuôn D3 Guzzle).
- Model + 3 model con warranty (grep `firm_warranty_request` trong `app/Model*`), blade `formJs` (đổ `send_company_id` = `Company::getForSelect()`), `FirmWarrantyRequestExcel`.

---

## Global Constraints

Áp cho **mọi** task (sao chép verbatim từ spec/CLAUDE.md):

- **DB gộp:** model HRM `extends App\Models\BaseModel`, `$table` = tên bảng ERP, KHÔNG `$connection`, KHÔNG migration. Model bảng ERP có hook riêng thì service tự gán `updated_by = auth()->id()` mọi đường ghi.
- **D1 = own-only:** Service lọc `->where('created_by', auth()->id())`. KHÔNG `checkPermission`, KHÔNG `columnCustomizationMixin`, KHÔNG đụng Catalog quyền. Menu khai KHÔNG `codes`.
- **D2 = giữ ERP mở:** KHÔNG sửa màn create/edit ERP, KHÔNG redirect. Chỉ thêm đoạn D3 vào ERP `unApprove`.
- **D3 = chuông "Không duyệt" (status 5):** ERP Guzzle POST `notify-result`; HRM route `notify-result` giao chuông người lập.
- **Trạng thái giữ số ERP:** 1 Đang tạo · 2 Chờ duyệt · 3 Đang gửi NCC · 4 Đã gửi NCC · 5 Không duyệt · 6 Đã xác nhận BH · 7 Hoàn thành. **HRM chỉ set 1 hoặc 2.**
- **`canEdit`/`canDelete` = chủ phiếu (`created_by === auth()->id()`) VÀ status ∈ {1, 5}** (port đúng ERP).
- **Validate port đầy đủ, KHÔNG nới nháp** — bám sibling `DeliveryCostAskingRequestStoreRequest` ("Lưu nháp không nới rule nào, ERP cũng không") + ERP FirmWarrantyRequest chạy full validate bất kể status. ⚠️ **Đây là đảo ngược footnote §7 của design doc** (doc đề xuất nới nháp theo convention HRM). Chốt theo sibling + ERP: Lưu nháp (status 1) và Gửi duyệt (status 2) **cùng một bộ rule**. (Xem Review Focus.)
- **FormRequest resolve THỦ CÔNG sau guard** ở `update` (`app(...UpdateRequest::class)->validated()`), không khai ở tham số — để guard chủ phiếu/trạng thái chạy trước validate (tránh 422 che 403).
- **Không khai `messages()`** cho rule phổ biến (required/exists/max/numeric/min) — lang `vi` đã có. Chỉ message riêng cho câu nghiệp vụ (vd "Chưa phân công người phụ trách thương hiệu, hãng sản xuất").
- **UI:** mọi element form dùng `V2Base*`; select trong modal = `V2BaseSelectInModal`; badge `V2BaseBadge` màu+chữ do BE trả (9 màu chuẩn); số `1,234.56` (`toLocaleString('en-US')` / `number_format` mặc định); nút `mr-2 mb-2` (nút cuối cụm `mb-2`); nút footer trong `V2Footer`; nhãn "Người tạo/Ngày tạo" KHÔNG "Người lập/Ngày lập"; nút không dùng được thì **ẩn** (`v-if`), không disable; lưu xong `markFormSaved()` + về danh sách.
- **Người ký/duyệt bản in = Chức danh HRM** (`titles` qua `employee_infos.employee_role_id`), KHÔNG `roles` ERP (`App\Helper\SignerTitleHelper`).
- **Cờ quyền fail-closed**, không literal `true`.
- **Tài liệu** chỉ ở `HRM/.plans`, `HRM/docs`. **Không commit/push** khi user chưa yêu cầu.
- **Kiểm tới tận gốc:** bảng ERP "nói dối" — `Supplier::$table='customers'`, nhiều cột `*_name` là snapshot NULL. Đọc code ERP tới nơi tính giá trị trước khi join/tin cột.

**Cách kiểm thử (thay cho unit TDD):** 2 bản sibling port KHÔNG có unit test; CLAUDE.md chốt **verify bằng Playwright e2e trước khi báo xong**. Mỗi task BE "test" bằng smoke cụ thể (tinker gọi thẳng service/controller với `Auth::guard('api')->setUser(...)`, hoặc curl endpoint) — ghi lệnh + kết quả mong đợi. Task cuối là **1 e2e spec** chạy trọn luồng. Không bịa phpunit không khớp codebase.

---

## Review Focus

Năm lớp input/thất bại spec ngụ ý mà dễ cắn người dùng, mỗi dòng đã gắn vào task sở hữu code:

1. **Gửi duyệt khi CHƯA phân công người phụ trách** (không có `AssignHistory` còn hiệu lực cho send_company+brand+manufacture) → phải chặn status→2 với đúng câu "Chưa phân công người phụ trách thương hiệu, hãng sản xuất", KHÔNG tạo phiếu treo không ai nhận chuông. → **Task 5** (StoreRequest `withValidator`) + **Task 4** (Notifier không recipient thì không im lặng nuốt).
2. **`contractable` đa hình** (`FirmContract` | `WrServiceContract`): chọn nhầm loại, hoặc `contractable_id` không thuộc loại đã chọn, hoặc hàng không thuộc HĐ (`checkData`) → phải 422 rõ ràng, không lưu rác. → **Task 5** + **Task 2** (`checkData`).
3. **Sửa/Xóa phiếu đã sang status 3-7** (XNK đã xử lý ở ERP) qua gọi API trực tiếp → `findEditable` phải 423/422, KHÔNG cho ghi đè. → **Task 2**.
4. **`notify-result` bị gọi bởi người không phận sự** (probe id) → 403 kể cả id sai; phiếu không ở status 5 → 422. → **Task 2** (`findForResultNotify`) + **Task 8**.
5. **Đổi thương hiệu khi đã chọn hàng** → xóa sạch hàng thuộc hãng cũ (hàng lọc theo hãng), không để dòng rác lệch thương hiệu qua được validate "cùng thương hiệu". → **Task 10** (Form.vue onBrandSelect) + **Task 5** (rule cùng thương hiệu).

---

## Cấu trúc file

**hrm-api (`Modules/Finance`):**
- Entities: `Entities/FirmWarrantyRequest/FirmWarrantyRequest.php` + `FirmWarrantyRequestProduct.php` + `FirmWarrantyRequestProductItem.php` + `FirmWarrantyRequestProductCost.php`
- Services: `FirmWarrantyRequestService.php` (read), `FirmWarrantyRequestWriteService.php`, `FirmWarrantyNotifier.php`, `FirmWarrantyRequestPrintService.php`
- Requests: `Http/Requests/FirmWarrantyRequest/FirmWarrantyRequestStoreRequest.php` + `...UpdateRequest.php`
- Transformers: `Transformers/FirmWarrantyRequestResource/FirmWarrantyRequestListResource.php` + `...DetailResource.php`
- Controller: `Http/Controllers/V1/FirmWarrantyRequestController.php`
- Routes: thêm group vào `Modules/Finance/Routes/api.php` (cạnh group delivery-cost)

**hrm-client (`pages/finance/firm-warranty-requests`):** `api.js`, `index.vue`, `create.vue`, `_id/index.vue`, `_id/edit.vue`, `components/FirmWarrantyRequestForm.vue`

**ERP:** sửa `FirmWarrantyRequestController.php` (thêm Guzzle D3 trong `unApprove`/chỗ set status 5)

**Menu:** `hrm-client/components/subsystem-menu/sale-hub.js:187`

---

## Task 1: Entities (4 model trỏ bảng ERP)

**Files:**
- Create: `Modules/Finance/Entities/FirmWarrantyRequest/FirmWarrantyRequest.php` + 3 model con (paths trên)
- Đọc: 4 model ERP tương ứng để lấy **tên cột thật** + quan hệ (grep `firm_warranty_request` trong `ERP/TanPhatDev/app/Model*`).

**Interfaces (Produces):**
- `FirmWarrantyRequest`: `$table='firm_warranty_requests'`, `extends BaseModel`. Hằng `DANG_TAO=1, CHO_DUYET=2, DANG_GUI_NCC=3, DA_GUI_NCC=4, KHONG_DUYET=5, DA_XAC_NHAN=6, HOAN_THANH=7`. `STATUSES` map `[id=>['name'=>..,'color'=>hex]]` dùng 9 màu chuẩn (1 `#64748B` · 2 `#D97706` · 3 `#2563EB` · 4 `#0EA5E9` · 5 `#DC2626` · 6 `#7C3AED` · 7 `#16A34A`). `statusMeta(int): array`. `$fillable` gồm `code,status,brand_id,brand_name,manufacture_id,manufacture_name,send_company_id,approver_id,approved_time,approver_comment,note,company_id,department_id,part_id,created_by,updated_by` (đối chiếu cột thật). Relations: `products()` hasMany(`FirmWarrantyRequestProduct`,'firm_warranty_request_id'), `employee_create()` (từ BaseModel), `approver()` belongsTo(Employee,'approver_id'), `brand()`, `manufacture()`, `sendCompany()` belongsTo(Company,'send_company_id'). `canEdit(): bool` = `in_array($this->status,[1,5]) && $this->created_by===auth()->id()`. `canDelete()` = `canEdit()`.
- `FirmWarrantyRequestProduct`: `$table='firm_warranty_request_products'`. `$fillable` = cột thật (`firm_warranty_request_id,product_id,product_name,product_code,model_id,model_name,all_barcodes,unit_id,unit_name,serial,content,note,customer_id,customer_name,customer_code,contractable_id,contractable_type,contractable_code,handover_date,attachment,in_stock`). `items()` hasMany(`...ProductItem`,'firm_warranty_request_product_id'), `costs()` hasMany(`...ProductCost`,...). `contractable()` **morphTo** (map `FirmContract`/`WrServiceContract`).
- `FirmWarrantyRequestProductItem`: `$table='firm_warranty_request_product_items'`, `$fillable`=`firm_warranty_request_product_id,product_id,product_name,product_code,unit_id,unit_name,qty`.
- `FirmWarrantyRequestProductCost`: `$table='firm_warranty_request_product_costs'`, `$fillable`=`firm_warranty_request_product_id,cost_name,amount`.

- [x] **Step 1:** Grep + đọc 4 model ERP, ghi ra bảng cột thật (đối chiếu design doc §6; nếu lệch tên cột → theo ERP, sửa lại fillable).
- [x] **Step 2:** Viết 4 model HRM theo Interfaces trên. `STATUSES` lấy đúng chữ tiếng Việt từ hằng/`status_text` model ERP.
- [x] **Step 3 (verify):** `php artisan tinker` →
  `Modules\Finance\Entities\FirmWarrantyRequest\FirmWarrantyRequest::with('products.items','products.costs')->first()` trả object không lỗi quan hệ; `->statusMeta(5)` ra `['name'=>'Không duyệt','color'=>'#DC2626']`.
- [x] **Step 4:** Commit (khi user cho phép): `feat(finance): entities phiếu YC hãng bảo hành trỏ bảng ERP`.

---

## Task 2: Read Service (own-only, guards, lookups, pickers, checkData)

**Files:** Create `Modules/Finance/Services/FirmWarrantyRequestService.php`. Khuôn: `DeliveryCostAskingRequestService.php`.

**Interfaces:**
- Consumes: Task 1 entities.
- Produces:
  - `PER_PAGE=20`, `PICKER_LIMIT=30`.
  - `paginate(Request): LengthAwarePaginator` — `->where('created_by', auth()->id())`; filter `code` (LIKE mã/serial/model/product theo ô tìm nhanh), `status`, `brand_id`, `manufacture_id`, `customer_id`, `approver_id`, `product`, `start_date/end_date` (theo `created_at`); eager `with('employee_create.info','approver.info','brand','manufacture')`; `orderByDesc('created_at')->orderByDesc('id')`.
  - `findForCurrentUser(int): FirmWarrantyRequest` — own-only; 404 nếu không có/không phải của mình.
  - `findEditable(int): FirmWarrantyRequest` — own-only + `canEdit()` else 423 (khoá) / 422; guard TRƯỚC validate.
  - `findForResultNotify(int): array [model, employeeInfoId]` — caller phải là `approver` HOẶC holder `purchase.mua_hang.manage` (else 403 **kể cả** id không tồn tại); status phải = 5 (else 422); `employeeInfoId` = `employee_create.info.id`.
  - `lookups(FirmWarrantyRequest): array` — gom query (products, units, customers, contracts theo loại) tránh N+1; dùng cho DetailResource.
  - `brands(Request)`, `manufacturers(Request)`, `customers(Request)`, `products(Request)` (lọc theo `brand_id`/`manufacture_id`), `contracts(Request)` (theo `type` = FirmContract|WrServiceContract) — server-side search `PICKER_LIMIT`.
  - `getDeputy(int $manufactureId): ?array` — gọi logic ERP `manufactures/{id}/getDeputy`, **chỉ để hiển thị** ô readonly "Người nhận đơn/Người mua"; KHÔNG phải đích chuông.
  - `checkData(array): array` — xác minh hàng thuộc HĐ đã chọn + trả `handover_date`; port ERP `checkData`.

- [x] **Step 1:** Đọc `DeliveryCostAskingRequestService.php` + ERP `FirmWarrantyRequestController@index/checkData` để lấy filter thật + checkData.
- [x] **Step 2:** Viết service theo Interfaces. `findForResultNotify` **403-before-404** (không lộ tồn tại phiếu). Holder check qua `PermissionChecker::holdersAnyCompany('purchase.mua_hang.manage','web')` như Notifier sibling.
- [x] **Step 3 (verify Review Focus #3, #4):** tinker set user thường (không super admin) rồi:
  - `findEditable(<id status 3>)` → ném 423/422 (không trả model).
  - `findForResultNotify(<id không tồn tại>)` với user thường → **403**, không 404.
  - `findForResultNotify(<id status 2>)` với approver → **422**.
  - `paginate` với 2 user khác nhau → mỗi user chỉ thấy phiếu của mình (đếm khác nhau).
- [x] **Step 4:** Commit: `feat(finance): read service phiếu YC hãng bảo hành own-only + guards`.

---

## Task 3: Write Service (store/update/syncProducts/destroy/sendIfNeeded)

**Files:** Create `Modules/Finance/Services/FirmWarrantyRequestWriteService.php`. Khuôn: `DeliveryCostAskingRequestWriteService.php`.

**Interfaces:**
- Consumes: Task 1, Task 4 (`FirmWarrantyNotifier`).
- Produces:
  - `store(array $data): FirmWarrantyRequest` — `DB::transaction`: tạo phiếu với `code='TMP-'.uniqid()` (cột NOT NULL) + org fields (BaseModel hook gán company/department/part/created_by của **người lập**); lấy `id` → set `code='PYCHBH-'.str_pad($id,5,'0',STR_PAD_LEFT)` → save; `syncProducts($m,$data['products'])`; `sendIfNeeded($m)`. **`approver_id` để NULL** (mirror ERP comment — không ghi lúc tạo).
  - `update(FirmWarrantyRequest $m, array $data): FirmWarrantyRequest` — cập nhật header (brand/manufacture/send_company/note/status; **KHÔNG updated_by** — R5: bảng không có cột này); `syncProducts`; `sendIfNeeded`. (Theo sibling: `update` KHÔNG nhận đổi khoá hãng? → đối chiếu ERP; design doc FE khoá `manufacture_id`/`brand_id` khi edit. Nếu ERP update bỏ qua brand/manufacture thì giữ nguyên, không ghi đè.)
  - `syncProducts($m, array $products): void` — **xóa sạch con rồi tạo lại** (port ERP `syncProducts`): mỗi product tạo `FirmWarrantyRequestProduct` (+ snapshot name/code/model/unit/customer/contractable_code + `attachment` nối `", "` từ mảng URL S3), rồi tạo `items[]` và `costs[]`. Xóa theo thứ tự con→cha (items/costs trước product).
  - `destroy(FirmWarrantyRequest $m): void` — xóa items/costs → products → phiếu, trong transaction.
  - `sendIfNeeded($m): void` — nếu `status===CHO_DUYET(2)`: set `approved_time`? KHÔNG (ERP set lúc XNK duyệt) → chỉ `notifier->notifyPurchasing($m)`.

- [x] **Step 1:** Đọc ERP `store/update/syncProducts` để port chính xác snapshot + thứ tự xóa/tạo + xử lý `attachment`.
- [x] **Step 2:** Viết write service. ⚠️ **R5: 4 bảng KHÔNG có `updated_by` — TUYỆT ĐỐI không gán** (gán sẽ lỗi cột không tồn tại). Header set `created_by` + `company_id/department_id/part_id` do BaseModel `creating` hook tự gán từ Auth người lập (xác nhận hook chạy; set `created_by` tường minh cho chắc). Items/costs ghi phải set CẢ `firm_warranty_request_id` LẪN `firm_warranty_request_product_id`.
- [x] **Step 3 (verify):** tinker `store($payloadHợpLệ status 1)` → trả model `code` khớp `PYCHBH-00001`-style, con tạo đủ; `store(status 2)` với đã có AssignHistory → gọi notifyPurchasing (kiểm bảng `notifications` có 1 dòng mới cho đúng buy_employee); `destroy` xóa sạch con.
- [x] **Step 4:** Commit: `feat(finance): write service phiếu YC hãng bảo hành`.

---

## Task 4: Notifier (HRM→ERP 1 người phụ trách + ERP→HRM result)

**Files:** Create `Modules/Finance/Services/FirmWarrantyNotifier.php`. Khuôn: `DeliveryCostAskingNotifier.php` (NHƯNG recipient khác: đúng 1 người theo AssignHistory, không phải mọi holder).

**Interfaces:**
- Produces:
  - Hằng: `HRM_SHOW_URL='/finance/firm-warranty-requests/%d'`, `ERP_SHOW_URL='/admin/orders/firm_warranty_requests/%d/show'`, `ERP_NOTIFIABLE_TYPE='App\Employee'`, `ERP_NOTIFICATION_TYPE='App\Notifications\SystemNotification'`.
  - `resolveBuyEmployeeId($m): ?int` — `AssignHistory` theo (`send_company_id`+`brand_id`+`manufactures_id`), `whereNull('employee_date_to')`, `orderByDesc('created_at')->first()->buy_employee_id` (port ERP controller:186-190). **1 người duy nhất.**
  - `notifyPurchasing($m): void` — recipient = `resolveBuyEmployeeId`; nếu null thì **không gửi** (việc chặn gửi đã nằm ở StoreRequest Task 5; ở đây chỉ log). Ghi thẳng `notifications` (uuid, `data.url`→ERP show, content theo `NotificationMeta::build()` + `notification-convention`). Lỗi chỉ `Log::warning`.
  - `notifyCreatorResult($m, int $status, int $employeeInfoId): void` — content qua `NotificationMeta::build(NotificationMeta::KHAC, 'YCHBH', 'Không duyệt', $m->code, $m->approver_comment)`; `EmployeeInfoService::sendNotification($employeeInfoId, $content+[url=>HRM show, type, id])`.

- [x] **Step 1:** Đọc ERP AssignHistory query (controller:~186-190) + sibling Notifier. Xác nhận cột `manufactures_id`/`send_company_id`/`brand_id` trên `assign_histories`.
- [x] **Step 2:** Viết Notifier. Prefix/nhóm hành động thông báo theo `.claude/skills/notification-convention`.
- [x] **Step 3 (verify Review Focus #1):** tinker `resolveBuyEmployeeId` với data có/không AssignHistory → ra id / null đúng; `notifyPurchasing` ghi đúng 1 dòng `notifications` cho đúng người; `notifyCreatorResult` gọi `sendNotification` (stub/log) đúng employee_info người lập.
- [x] **Step 4:** Commit: `feat(finance): notifier phiếu YC hãng bảo hành (1 người phụ trách + result)`.

---

## Task 5: FormRequests (Store + Update) — full validate, chặn phân công & HĐ đa hình

**Files:** Create `Http/Requests/FirmWarrantyRequest/FirmWarrantyRequestStoreRequest.php` + `...UpdateRequest.php`. Khuôn: `DeliveryCostAskingRequestStoreRequest.php`.

**Interfaces (Produces):**
- `authorize()=true`. `rules()` (áp cho **cả status 1 và 2** — không nới nháp):
  - `status` required|in:1,2; `brand_id`/`manufacture_id`/`send_company_id` required|exists; `note` nullable|max:255.
  - `products` required|array|min:1; `products.*.product_id` required|exists:products,id; `products.*.content` required; `products.*.unit_id` required|exists:units,id; `products.*.serial` nullable; `products.*.in_stock` required|in:0,1.
  - `products.*.customer_id` **required_if:products.*.in_stock,0** | nullable|exists:customers,id.
  - `products.*.contractable_type` required_with:products.*.contractable_id | in:FirmContract,WrServiceContract.
  - `products.*.contractable_id` **required_unless:products.*.customer_id,null** (đối chiếu ERP đúng điều kiện) | integer.
  - `products.*.items` nullable|array; `items.*.product_id` required|exists; `items.*.qty` required|numeric|min:1.
  - `products.*.costs` nullable|array; `costs.*.cost_name` required; `costs.*.amount` required|numeric|min:1.
- `withValidator($v)`: `after()` kiểm:
  1. **Trùng `product_id + serial`** trong cùng phiếu → lỗi `distinct`.
  2. Mỗi product **cùng thương hiệu** với `brand_id` phiếu (query `products.brand_id`).
  3. `contractable_id` thuộc đúng `contractable_type` đã chọn (và hàng thuộc HĐ — tái dùng `checkData` Task 2 nếu ERP làm vậy).
  4. **Khi `status==2`:** `resolveBuyEmployeeId` (dùng chung Notifier Task 4) phải ra id, else `$v->errors()->add('status','Chưa phân công người phụ trách thương hiệu, hãng sản xuất')`.
- `UpdateRequest`: y `rules()`; nếu ERP `update` khoá `brand_id/manufacture_id` thì bỏ 2 rule đó (giá trị lấy từ phiếu cũ).

- [x] **Step 1:** Đọc ERP `store()` validate block verbatim (gồm `required_if`/`required_unless` chính xác + 2 vòng after check trùng/brand) để port đúng điều kiện, không chế.
- [x] **Step 2:** Viết 2 request. KHÔNG `messages()` trừ câu "Chưa phân công…".
- [x] **Step 3 (verify Review Focus #1, #2):** curl/tinker:
  - payload status 2 **không AssignHistory** → 422 trường `status` câu phân công.
  - `in_stock=0` thiếu `customer_id` → 422; `customer_id` có nhưng thiếu `contractable_id` → 422.
  - `contractable_type=FirmContract` nhưng id thuộc WrServiceContract → 422.
  - 2 dòng trùng `product_id+serial` → 422 distinct.
  - **status 1 (nháp) thiếu `content`/`send_company_id`** → vẫn 422 (xác nhận KHÔNG nới nháp).
- [x] **Step 4:** Commit: `feat(finance): form requests phiếu YC hãng bảo hành (full validate)`.

---

## Task 6: Resources (List + Detail)

**Files:** Create `Transformers/FirmWarrantyRequestResource/FirmWarrantyRequestListResource.php` + `...DetailResource.php`. Khuôn: sibling tương ứng.

**Interfaces:**
- Consumes: Task 1, `lookups()` Task 2.
- Produces:
  - `ListResource::row($m): array` — `id,code,brand_name(optional brand->name),manufacture_name,creator_name(employee_create.info.fullname),created_at(d/m/Y H:i),approved_time,approver_name,status,status_name,status_color,can_edit,can_delete`.
  - `DetailResource::make($m,$lookups): array` — merge row + `note,approver_comment,send_company_id,send_company_name,deputy(getDeputy),products[]`. Mỗi product: snapshot + `customer_code/name`, `contractable_type/id/code`, `handover_date`, `attachment`(mảng URL tách từ chuỗi), `in_stock`, `items[]`(product+qty), `costs[]`(cost_name+amount), `units` cho picker.

- [x] **Step 1:** Viết 2 resource. Eager-load đã ở Task 2 `lookups`/`paginate` — KHÔNG query trong map (chặn N+1).
- [x] **Step 2 (verify):** curl `index` + `show` → JSON có `status_color` hex đúng, `can_edit/can_delete` khớp chủ+trạng thái, `attachment` là mảng.
- [x] **Step 3:** Commit: `feat(finance): resources phiếu YC hãng bảo hành`.

---

## Task 7: PrintService

**Files:** Create `Modules/Finance/Services/FirmWarrantyRequestPrintService.php`. Khuôn: `DeliveryCostAskingRequestPrintService.php` + ERP `print_data`/`product_table`.

**Interfaces:** `renderTemplate(FirmWarrantyRequest $m): string` — HTML bản in; logo theo `companies.header` của `company_id` **trên phiếu** (khuôn `BillIncomePrintService::headerUrl()`); người ký = **Chức danh HRM** (`SignerTitleHelper`).

- [x] **Step 1:** Port layout bảng hàng + items/costs từ ERP print blade sang HTML template.
- [x] **Step 2 (verify):** curl `/{id}/print-data` → `template` HTML hợp lệ, số định dạng `1,234.56`, logo đúng công ty phiếu.
- [x] **Step 3:** Commit: `feat(finance): print service phiếu YC hãng bảo hành`.

---

## Task 8: Controller + Routes

**Files:** Create `Http/Controllers/V1/FirmWarrantyRequestController.php` (extends `ApiController`); sửa `Modules/Finance/Routes/api.php` (thêm group cạnh delivery-cost ~dòng 1906-1922).

**Interfaces (Produces):** Methods khuôn sibling Controller:
- `index(Request)` → ListResource + `additional[total/lastPage/currentPage/perPage, meta.statuses=[1,2,3,4,5,6,7] map name]`.
- `show($id)` → `findForCurrentUser` + DetailResource.
- `store(FirmWarrantyRequestStoreRequest)` → `writeService->store` → `savedMessage`.
- `update($id)` → `findEditable` guard trước; `app(FirmWarrantyRequestUpdateRequest::class)->validated()`; `writeService->update`.
- `destroy($id)` → `writeService->destroy(findEditable)`.
- Pickers: `brands/manufacturers/customers/products/contracts` (+ validate `manufacture_id`/`brand_id` required cho products, `type` cho contracts). `deputy($manufactureId)`. `checkData(Request)`.
- `notifyResult($id)` → `findForResultNotify` + `notifier->notifyCreatorResult`.
- `print($id)` → PrintService.
- `savedMessage(int $status): string` = `$status===2 ? 'Đã gửi yêu cầu bảo hành.' : 'Lưu nháp thành công.'`.

**Routes** group `/firm-warranty-requests` (auth:api, KHÔNG checkPermission): static (brands/manufacturers/customers/products/contracts/checkData) **TRƯỚC** `/{id}`; GET `/`, POST `/`, GET `/{id}`, PUT `/{id}`, DELETE `/{id}`, GET `/{id}/deputy`? (hoặc `/manufactures/{id}/deputy`), GET `/{id}/print-data`, POST `/{id}/notify-result`.

- [x] **Step 1:** Viết controller + routes (thứ tự route static trước param).
- [x] **Step 2 (verify Review Focus #4):** curl toàn bộ endpoint với token thường: `notify-result` bởi người lạ → 403; routes static không bị nuốt bởi `/{id}`.
- [x] **Step 3:** Commit: `feat(finance): controller + routes phiếu YC hãng bảo hành`.

---

## Task 9: ERP — D3 callback khi "Không duyệt" (status 5)

**Files:** Modify `ERP/TanPhatDev/app/Http/Controllers/Order/FirmWarrantyRequestController.php` (chỗ XNK set status=5 / `unApprove`). Khuôn: `WrApproveResultsController::notifyHrmImportResult`.

**Interfaces:** Sau khi set status=5 + save: Guzzle `POST {HRM_API_BASE_URL}/api/v1/finance/firm-warranty-requests/{id}/notify-result` (Bearer JWT SSO, timeout 5s, lỗi chỉ `Log::warning`). Đọc `HRM_API_BASE_URL` theo env (memory `erp-hrm-api-base-url-per-env`).

- [x] **Step 1:** Tìm đúng method ERP đổi status→5 (grep `KHONG_DUYET`/`= 5` trong controller). Chèn Guzzle sau commit DB.
- [x] **Step 2 (verify Review Focus #4 + D3):** trên môi trường local: tạo phiếu HRM→gửi→ERP "Không duyệt" → kiểm HRM người lập nhận chuông deep-link `/finance/firm-warranty-requests/{id}`.
- [x] **Step 3:** Commit **ERP** (nhánh `develop_02`, khi user cho phép): `feat(order): báo HRM khi không duyệt YC hãng bảo hành`.

---

## Task 10: HRM client — api.js + Form.vue

**Files:** Create `pages/finance/firm-warranty-requests/api.js` + `components/FirmWarrantyRequestForm.vue`. Khuôn: sibling `api.js` + `DeliveryCostAskingRequestForm.vue`.

**Interfaces:**
- `api.js`: `API_BASE='finance/firm-warranty-requests'`, `API_LIST='/finance/firm-warranty-requests'`, `STATUS_CREATING=1`, `STATUS_AWAITING=2`, `IN_STOCK_OPTIONS`, `CONTRACT_TYPE_OPTIONS=[{FirmContract},{WrServiceContract}]`; helpers `fetchBrands/fetchManufacturers/fetchCustomers/fetchProducts/fetchContracts` qua `$store.dispatch('apiGetMethod')` + header `X-Silent-Errors`; `checkData(payload)`.
- `FirmWarrantyRequestForm.vue` (Tạo/Sửa/readonly): header Thương hiệu(bắt buộc; đổi→xóa hàng) · Hãng SX(bắt buộc) · Công ty gửi(bắt buộc, `V2BaseSelectRemote` toàn bộ công ty) · Người nhận đơn/Người mua(readonly từ `deputy`) · Người yêu cầu/Phòng(readonly user hiện tại) · Ghi chú. Bảng dòng hàng: Hàng(`V2ProductPickerModal` lọc theo thương hiệu) · Serial · Nội dung BH(bắt buộc) · `in_stock`(checkbox) · Khách hàng(`ChooseErpCustomerModal`, required khi in_stock=0) · Hợp đồng(chọn loại + picker đa hình, bám `DeclareDebtContractPicker` + checkData) · Đính kèm(`V2BaseFile`) · sub-bảng items(picker+qty) · sub-bảng costs(cost_name+amount). Footer `V2Footer #custom-actions`: Lưu nháp(secondary, status=1) · Gửi duyệt(primary, status=2). Validate realtime FE + BE 422 (cùng bộ rule 2 nút). `unsavedChangesMixin`.

- [x] **Step 1 (rà component dùng chung — bắt buộc trước khi tự dựng):** grep `V2ProductPickerModal`, `ChooseErpCustomerModal`, `DeclareDebtContractPicker`, `V2BaseFile` — xác nhận khớp nhu cầu (đa hình HĐ + checkData). Lệch thì **hỏi user trước** khi sửa component đang chạy (CLAUDE.md). Ghi "copy pattern từ `<file:dòng>`".
- [x] **Step 2:** Viết `api.js` + `Form.vue`. `onBrandSelect`: đã chọn hàng → `$confirm` xóa hàng hãng cũ (Review Focus #5). Số `toLocaleString('en-US')`.
- [x] **Step 3 (verify):** render Tạo/Sửa/Chi tiết; `grep -rn '<input \|<textarea\|<select \|<button \|<label ' pages/finance/firm-warranty-requests/ | grep -v V2Base` phải RỖNG.
- [x] **Step 4:** Commit: `feat(finance): client form phiếu YC hãng bảo hành`.

---

## Task 11: HRM client — index/create/_id + Menu

**Files:** Create `index.vue`, `create.vue`, `_id/index.vue`, `_id/edit.vue`; Modify `components/subsystem-menu/sale-hub.js:187`.

**Interfaces:**
- `index.vue` khuôn sibling: mixin `PageTitleMixin, filterStateMixin, DedupeLoadMixin, reportPrintPreviewMixin` (KHÔNG `columnCustomizationMixin` — D1 own-only). `layout:'default-sidebar'`. Cột: STT · **Số phiếu**(nuxt-link) · Thương hiệu · Hãng SX · **Người tạo** · **Ngày tạo** · Ngày duyệt · Người duyệt · **Trạng thái**(badge) · Hành động(In luôn · Sửa `v-if can_edit` · Xóa `v-if can_delete`). Lọc floating: Trạng thái, Thương hiệu, Hãng SX, Khách hàng(ajax), Người duyệt(ajax), Ngày tạo. Ô tìm nhanh `Tìm theo số phiếu, mã/tên hàng, model, serial`. `localStorageKey='finance_firm_warranty_requests'`. Xóa qua `BaseConfirmModal`. **Bắt buộc HRM: Xuất Excel danh sách** (`listExportFile.js`).
- `create.vue` → `<FirmWarrantyRequestForm/>`; `_id/edit.vue` → `<FirmWarrantyRequestForm :id>`; `_id/index.vue` → `<FirmWarrantyRequestForm :id readonly>` + footer In/Sửa/Xóa khớp danh sách.
- `sale-hub.js:187`: thay chuỗi trần `'YC hãng bảo hành'` → `{ n: 'YC hãng bảo hành', link: '/finance/firm-warranty-requests' }` (own-only: **không** `codes`).

- [x] **Step 1:** Viết 4 trang + đổi menu.
- [x] **Step 2 (verify):** Playwright mở `http://127.0.0.1:3000/finance/firm-warranty-requests` → danh sách render có sidebar, badge màu BE, lọc ăn (chờ ≥3s), menu Bán hàng có mục link (không xám).
- [x] **Step 3:** Commit: `feat(finance): client list + detail + menu phiếu YC hãng bảo hành`.

---

## Task 12: E2E + đối chiếu

**Files:** Create `e2e/tests/finance-firm-warranty-request.spec.ts` (hoặc theo cấu trúc bộ e2e hiện có).

- [x] **Step 1:** Viết e2e: lập nháp (status 1) → mở lại sửa → Gửi duyệt (status 2, kiểm chuông XNK) → (data có AssignHistory) → sửa lại phiếu status 5 → xóa nháp → in. Chạy `cd e2e && PATH="$HOME/.nvm/.../v20.20.1/bin:$PATH" npx playwright test finance-firm-warranty-request`.
- [x] **Step 2 (Bước 5 + 5b skill erp-to-hrm-screen):** đối chiếu ngược ERP `develop_02` (đủ cột/lọc/hành động + điều kiện ẩn) và ngang 2-3 màn HRM đã QA (sibling delivery-cost/inland-order). Ghi "đã bám màn X ở khối Y".
- [x] **Step 3:** Chụp ảnh danh sách/form/chi tiết đặt cạnh màn chuẩn; chạy checklist tự kiểm skill.
- [x] **Step 4:** Commit: `test(finance): e2e phiếu YC hãng bảo hành`.

---

## Ghi chú cho executor

- **Tạm bỏ** "Xuất Excel 1 phiếu" của ERP (design doc §11) trừ khi QA yêu cầu. **In danh sách + Xuất Excel danh sách** là bắt buộc HRM → giữ.
- `approve()` ERP = **code chết**, KHÔNG port.
- Thứ tự thực thi gợi ý: 1→2→4→3→5→6→7→8 (BE) rồi 9 (ERP) rồi 10→11→12 (FE+e2e). Task 3 phụ thuộc Task 4 (notifier); Task 5 dùng chung `resolveBuyEmployeeId` của Task 4.
- Mọi "verify" chạy với **user thường** (không Super Admin — ERP `Gate::before` che quyền; HRM không bypass nhưng vẫn test đúng vai).

### Checkpoint — 2026-11-21 17:15 (wrap up tự động)
Vừa hoàn thành: chạy subagent-driven trọn 12 task + Task 10b (BE `export-rows` cho Xuất Excel danh sách — plan bắt buộc nhưng thiếu endpoint) + final review opus (0 Critical · 1 Important · ~8 Minor, Ready to merge YES) + fix wave 3 sửa (deputy preview ở `show()` key theo `send_company_id`; brand-check chỉ chạy khi có `brand_id`; fallback trạng thái lạ "Không xác định") → scoped re-review 3/3 ADDRESSED. e2e `HRM/e2e/tests/finance-firm-warranty-request.spec.ts` + POM `FirmWarrantyRequestPage.ts` 7/7 PASS.
Quyết định chốt trong ngày (09:21): Store/Update validate ĐẦY ĐỦ, KHÔNG nới nháp (đảo lại call #3 của design, khớp ERP + sibling delivery-cost); guard "Chưa phân công người phụ trách" chỉ áp khi status = 2. Chạy kiểu subagent-driven.
Ruling khi chạy: R2 không commit; R5 4 bảng không có `updated_by`, items/costs set cả 2 FK, `contractable_type` = tên class ERP đầy đủ; R6 thứ tự 1→4→2→3→5…; R6a canDelete = canEdit = status ∈ {1,5} (bám ERP); R7 bỏ check "hàng thuộc HĐ" ở store, bỏ `approver_id`; R8 KHÔNG thêm 422 "chưa có bộ phận" (lỗi `part_id cannot be null` là hành vi `BaseModel::creating` dùng chung toàn HRM, user KD thật đều có bộ phận); R-EXCEL thêm Task 10b; bản in NGUOI_LAP để rỗng như ERP (template 414).
Đang làm dở: TOÀN BỘ CHƯA COMMIT (working tree): hrm-api `develop` — 14 file mới `Modules/Finance/{Entities/FirmWarrantyRequest/, Http/Controllers/V1/FirmWarrantyRequestController.php, Http/Requests/FirmWarrantyRequest/, Services/FirmWarranty*.php, Transformers/FirmWarrantyRequestResource/}` + sửa `Routes/api.php`, `Entities/ErpReportTemplate.php`; hrm-client `develop` — `pages/finance/firm-warranty-requests/` + sửa `components/subsystem-menu/sale-hub.js:188`; ERP `develop_02` — sửa `app/Http/Controllers/Order/FirmWarrantyRequestController.php` (callback D3 báo HRM khi "Không duyệt"). Workspace SDD (brief/report/review) còn ở `sdd/` cạnh plan.md — chưa dọn (lệch quy tắc .plans chỉ design+plan; không đưa vào commit config).
Bước tiếp theo: user xác nhận commit từng repo (hrm-api develop / hrm-client develop / ERP develop_02), chưa push, chưa gop_db. Verify tay 3 việc e2e không tự động được: chuông D3 "Không duyệt" ERP→HRM, sửa phiếu status 5, guard chưa phân công. Gap so ERP (thấp, chờ user chốt): thiếu cột "Phòng yêu cầu", 4 ô lọc (Người nhận, Phòng ban, Model, Code đặt hàng), Xuất Excel từng phiếu, ô lọc Người duyệt, In danh sách. Dọn `sdd/` sau khi commit.
Blocked: chờ user cho phép commit.

### Checkpoint — 2026-11-23 17:15 (wrap up tự động)
Vừa hoàn thành: user cho phép push (09:15) → commit + rebase lên remote (không conflict) + push cả 3 repo: hrm-api `develop` `0ebcf2685` (cũ `2a4761f2f`), hrm-client `develop` `e81c2c222` (cũ `0c5204079`), ERP `develop_02` `1d045fdedf` (cũ `c0b5e9d131`, callback chuông "Không duyệt" về HRM). Link màn đã điền vào sheet Checklist chuyển đổi (dòng 51).
Đang làm dở: không. `sdd/` còn cạnh plan.md — chưa dọn, không đưa vào commit config.
Bước tiếp theo: gop_db khi user báo; verify tay chuông D3 "Không duyệt", sửa phiếu status 5, guard chưa phân công; gap so ERP (cột Phòng yêu cầu, 4 ô lọc, Excel từng phiếu, lọc Người duyệt) chờ user chốt.
Blocked:
