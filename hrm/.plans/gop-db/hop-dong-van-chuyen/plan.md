# Port "Hợp đồng vận chuyển" (DeliveryContract) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP "Hợp đồng vận chuyển" (model `DeliveryContract`, Module Transport) sang HRM — mắt cuối của chuỗi Báo giá VC → THGVC → BGHLVC → **Hợp đồng vận chuyển** — làm trọn: danh sách của-tôi + tất-cả (lọc theo công ty), tạo HĐ header-only từ BGHLVC, phụ lục có ma trận xe/tải/tuyến + import Excel, gửi duyệt → duyệt sinh bảng giá Final + closeContract + thông báo, cập nhật kho, xuất Excel, in popup, quyền mới 3 mức Xem + dùng lại "Duyệt giá vận chuyển"; chống crash khi HĐ rỗng chi tiết.

**Architecture:** Bám **ERP 1:1 về hành vi**, bám **sibling HRM THGVC (`DeliveryCostSummary`) + convention HRM về hình thức**. Backend: 1 Entity `DeliveryContract` (+5 entity con) extends `BaseModel`, 1 Service CORE `DeliveryContractService`, 1 Controller V1, các FormRequest chỉ `rules()`, 2 Transformer. Frontend: thư mục mới `pages/transport/delivery-contracts/` theo khuôn `delivery-cost-summaries/`. In qua popup (BE trả HTML từ ReportTemplate ERP). Tất cả 6 bảng `delivery_contract*` **đã tồn tại** trong `erp_hrm_check` với `created_by`/`updated_by` → **không có migration**.

**Tech Stack:** hrm-api = Laravel 8 / PHP 7.4 / guard `api` / nwidart modules / spatie permission ^5.4 / JWT (LOCAL, không deploy). hrm-client = Nuxt 2.14 / Vue 2 / Node 14.21.3 / V2Base / Bootstrap-Vue 2.15. DB gộp `erp_hrm_check` (127.0.0.1, root). Nhánh `develop` (gop_db). Verify = `php -l` + smoke runtime (tinker/curl `:8000` JWT) cho BE; grep self-check + Playwright (`127.0.0.1:3000`) cho FE — **KHÔNG phpunit** (THGVC đã chạy đúng khuôn này).

**Spec:**
- Design: `HRM/.plans/gop-db/hop-dong-van-chuyen/design.md` (rulings A–G, mô hình trạng thái, ánh xạ bảng, 11 bẫy).
- Khảo sát ERP: `<scratchpad>/erp-delivery-contract-survey.md` (11 mục — signatures/line refs của ERP nguồn).
- ERP nguồn (READ ONLY, bám hành vi): `ERP/TanPhatDev` — grep `DeliveryContract`, `DeliveryContractController`, `closeContract`, `syncDetails`, `quotationImport`.
- Sibling HRM (bám hình thức + pattern): `hrm-api/Modules/Transport/{Entities,Services,Http,Transformers,Exports}/DeliveryCostSummary*` + `hrm-client/pages/transport/delivery-cost-summaries/`.

## Global Constraints

Mọi task ngầm bao gồm — sao chép nguyên văn từ design + CLAUDE.md:

- Nhánh `develop`/gop_db, DB gộp `erp_hrm_check`, hrm-api **LOCAL**. **KHÔNG commit/push** trừ khi user yêu cầu trực tiếp.
- 6 bảng `delivery_contract*` **đã có** → GHI THẲNG, KHÔNG tạo bảng/cột mới. **KHÔNG thêm** `company_id`/`department_id`/`part_id` vào `delivery_contracts` (xem Ruling R1).
- **Bỏ dùng** cột di sản `delivery_cost_summary_id` / `delivery_cost_summary_quotation_id` (không ghi, không đọc).
- Entity `DeliveryContract` + 5 con **extends `BaseModel`** (tự gán `created_by`/`updated_by` = `auth()->id()` = `employees.id`, KHÔNG `auth()->user()->info->id`).
- Quyền guard `api`, khai qua seeder `$this->perm([...])` (KHÔNG `id`/`guard_name`), `type` = phân hệ **Vận chuyển** (tra `subsystems.js`). **KHÔNG dùng lại quyền ERP web.** **Duyệt = dùng lại quyền có sẵn `"Duyệt giá vận chuyển"`** (hằng `DeliveryCostSummary::PERM_APPROVE`). BE re-check `isCurrentEmployeeHasPermission`. Cờ FE fail-closed (CẤM `=true`).
- FormRequest mới = **chỉ `rules()`**, KHÔNG `messages()`. Rethrow `ValidationException` (KHÔNG catch nuốt). ERP `catch(Exception)` thiếu `\` → HRM dùng `\Exception`/`\Throwable`.
- `supplier_id` trỏ bảng **`customers`** (model `Supplier` = customers + is_supplier) → validate `exists:customers,id`. KHÔNG query bảng `suppliers`.
- File đính kèm qua bảng **`files`** chung (`table='delivery_contracts'` + `table_id`), KHÔNG cột `attachments` chuỗi, KHÔNG unlink local.
- Khóa/sai trạng thái chặn ở **BE** (423/422), FE ẩn nút (v-if). Endpoint FormRequest → guard khóa ở route middleware (khuôn `CheckCustomerNotLocked`).
- FE chỉ **V2Base\*** (grep thô phải RỖNG). Select-in-modal → `V2BaseSelectInModal`. Nút nhóm `mr-2 mb-2` (cuối `mb-2`). Nút không dùng được → ẩn `v-if`. Bảng tràn → `V2BaseTableScroll`. Footer → `V2Footer` + `#custom-actions`. Badge màu+chữ từ BE.
- **Số quốc tế `1,234,567.89`** mọi nơi (bảng/form/in/Excel; CẤM `toLocaleString('vi-VN')` cho SỐ — ngoại lệ duy nhất = luồng ĐỌC file import). Ngày `dd/mm/yyyy`. Ô số Excel = số thô + data-format.
- Sau thao tác → `markFormSaved()` + `$router.push` về danh sách. Tiêu đề chi tiết **`Chi tiết hợp đồng vận chuyển: <mã>`**. Hành động chi tiết **KHỚP** danh sách.
- Thông báo template `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}` + deep-link ID (skill `notification-convention`).
- `.text-muted` là ĐỎ → dùng `#6b7280`. Đỏ chỉ cho lỗi validate. KHÔNG tự sửa input user.
- Hiệu năng: eager-load chống N+1, phân trang, ≤5 API/màn, export >2s chia `export-rows`.
- `.plans`/docs LUÔN ở path gốc project `HRM/.plans/...`, KHÔNG trong repo hrm-api/hrm-client, KHÔNG ở workspace root.

## Rulings (chốt trước thi công — adjudicate các xung đột design ↔ sibling)

- **R1 — Scope KHÔNG dùng cột `company_id` trên bản ghi; lọc theo công ty của NGƯỜI TẠO (y THGVC).** Design §4/§8-bẫy-8 nói "thêm `company_id` nếu thiếu + lọc". Nhưng sibling `DeliveryCostSummary` **không có** cột org nào và lọc qua `employeeIdsSubquery('company_id', X)` join `employee_infos` trên `created_by`; Task-8 THGVC đã chốt dứt điểm "chứng từ không có công ty riêng → ngữ cảnh công ty CHÍNH LÀ công ty người tạo → không có rủi ro xem/in chéo công ty". Mirror chính xác pattern đó. **Chi phí nếu sai:** phải thêm migration cột + backfill sau — nhưng rủi ro thấp vì đây là precedent đã QA của THGVC.
- **R2 — Letterhead/logo in = công ty NGƯỜI TẠO** (hệ quả R1; `delivery_contracts` không có `company_id`). Cột snapshot `company_account_*`/`company_bank_*` là số tài khoản ngân hàng trên thân HĐ, KHÔNG phải nguồn letterhead. **Chi phí nếu sai:** một dòng đổi nguồn HEADER.
- **R3 — `checkCloseContract` (logic chết tham chiếu cột di sản) KHÔNG port.** Chỉ port `closeContract` viết lại theo `supplier_id` + trùng kho (Ruling D). **Chi phí nếu sai:** không, logic chết.
- **R4 — Verify = smoke runtime, KHÔNG phpunit.** Repo Laravel legacy, THGVC 16 task đều verify bằng `php -l` + tinker/curl + Playwright. Mỗi bước "test" dưới đây là lệnh runtime với output kỳ vọng cụ thể. **Chi phí nếu sai:** không — khớp cách repo thực chạy.

## Review Focus

Năm lớp input/hành vi spec ngụ ý mà dễ cắn người dùng nhất — mỗi dòng đã gắn test vào task sở hữu code:

1. **HĐ rỗng chi tiết (header-only) đem In/Xuất/đọc `details_table`** → phải trả bảng/mảng rỗng an toàn, KHÔNG 500. (ERP `getDetailsTableAttribute` crash khi không có details.) → **Task 2** (accessor) + **Task 8** (export/print) có bước verify HĐ status=3 chưa phụ lục.
2. **Lọc chéo công ty** → người cty A KHÔNG được thấy/in HĐ cty B ở danh sách "tất cả"; super-admin/quyền tổng cty thấy hết; quyền thiếu → tập rỗng (fail-closed). → **Task 4** (`scoped()`), verify bằng tài khoản thường 2 công ty.
3. **Import Excel lệch khung** → file phụ lục sai thứ tự xe/tải/tuyến hoặc mã không khớp HĐ gốc → ném exception, KHÔNG ghi lệch. → **Task 5** (`importExcel`), verify file hợp lệ + file lệch.
4. **ApproveRequest nuốt id các tầng** → modal Duyệt mang id dòng (payload.id/road.id/road_id/km) mà `validated()` strip mất → 500 "Undefined index: id" (bẫy đã trả giá THGVC Task 14). → **Task 9** (`ApproveRequest` khai đủ id các tầng), verify approve happy-path đọc được id.
5. **closeContract đóng nhầm / sót** → duyệt/đổi kho 1 NCC trùng kho phải đóng (status=4) đúng các HĐ cũ cùng NCC+trùng kho, KHÔNG đụng HĐ khác NCC/khác kho/đã hủy. → **Task 6**+**Task 7**, verify 3 HĐ (trùng / khác NCC / khác kho).

---

### Task 1: Entities + quan hệ + hằng + mã tự sinh + scope helper

**Files:**
- Create: `Modules/Transport/Entities/DeliveryContract/DeliveryContract.php`
- Create: `Modules/Transport/Entities/DeliveryContract/DeliveryContractVehicle.php`
- Create: `Modules/Transport/Entities/DeliveryContract/DeliveryContractVehiclePayload.php`
- Create: `Modules/Transport/Entities/DeliveryContract/DeliveryContractVehiclePayloadRoad.php`
- Create: `Modules/Transport/Entities/DeliveryContract/FinalDeliveryContractVehiclePayloadRoad.php`
- Create: `Modules/Transport/Entities/DeliveryContract/DeliveryContractHasWarehouse.php`
- Reference: `Modules/Transport/Entities/DeliveryCostSummary/DeliveryCostSummary.php` (pattern 1:1) + ERP `app/DeliveryContract.php` (hành vi).

**Interfaces:**
- Produces: `DeliveryContract` extends `BaseModel`, `$table='delivery_contracts'`.
  - Hằng: `const DA_HUY=0; DA_DUYET=1; CHO_DUYET=2; DANG_TAO=3; DONG=4;` và `const HOP_DONG=1; PHU_LUC=2;`.
  - Hằng quyền: `const PERM_APPROVE='Duyệt giá vận chuyển'; PERM_VIEW_ALL='Xem hợp đồng vận chuyển theo tổng công ty'; PERM_VIEW_COMPANY='Xem hợp đồng vận chuyển theo công ty'; PERM_VIEW_DEPARTMENT='Xem hợp đồng vận chuyển theo phòng ban'; PERM_CREATE/PERM_EDIT/PERM_DELETE/PERM_ANNEX/PERM_UPDATE_WAREHOUSE/PERM_PRINT/PERM_EXPORT/PERM_IMPORT` (giá trị khớp seeder Task 3).
  - Quan hệ: `supplier()` (`belongsTo(Supplier::class,'supplier_id')`), `approver()`, `employee_create()`, `warehouses()` (`belongsToMany` qua `delivery_contract_has_warehouses`), `vehicles()` (`hasMany(DeliveryContractVehicle,'parent_id')`), `roads()` (`hasMany(DeliveryContractVehiclePayloadRoad,'delivery_contract_id')`), `payloads()`, `finalRoads()` (`hasMany(FinalDeliveryContractVehiclePayloadRoad,'delivery_contract_id')`), `parent_contract()` (`belongsTo(self,'parent_contract_id')`), `annexes()` (`hasMany(self,'parent_contract_id')`), `files()` = `hasMany(File::class,'table_id','id')->where('table','delivery_contracts')`, `priceListValid()` (`belongsTo(\Modules\Finance\Entities\Delivery\PriceListValidDelivery::class,'price_list_valid_id')`).
  - `getNextCode()`: HĐ (type=1) → `'HĐVC-'.generateCode(5,$this->id)`; phụ lục (type=2) → `'<mã HĐ gốc>:PL-'.generateCode(2, <số thứ tự phụ lục>)`. Port đúng công thức ERP.
  - Accessor `warehouses_name` (ghép tên kho).
  - Scope helper tĩnh (copy từ `DeliveryCostSummary`): `currentUserIsSuperAdmin()` (join `employee_has_roles`+`roles` LOWER(name)='super admin'), `employeeIdsSubquery($column,$value)` (employees join employee_infos where employee_infos.$column=$value).
- 5 entity con extends `Model` (bảng con không `created_by` — nhưng kiểm: nếu có thì dùng BaseModel). `$fillable` theo cột thật (Task survey §DB). `FinalDeliveryContractVehiclePayloadRoad` KHÔNG có `parent_id`.

- [ ] **Step 1: Đọc pattern** `DeliveryCostSummary.php` (toàn bộ) + ERP `app/DeliveryContract.php` (hằng magic-number, quan hệ, `generateCode`) + `scratchpad/erp-delivery-contract-survey.md` §DB (cột mỗi bảng).
- [ ] **Step 2: Viết 6 entity** theo Interfaces. Ánh xạ quan hệ/cột đúng cột thật đã verify trong `erp_hrm_check` (survey §DB). Hằng status/type/quyền khai rõ (ERP dùng magic number — HRM khai hằng).
- [ ] **Step 3: `php -l`** cả 6 file → "No syntax errors".
- [ ] **Step 4: Smoke tinker** — Expected:
  ```
  php artisan tinker --execute="
    \$c = \Modules\Transport\Entities\DeliveryContract\DeliveryContract::with(['supplier','warehouses','vehicles','files','priceListValid'])->first();
    echo \$c ? ('OK id='.\$c->id.' code='.\$c->code.' sup='.optional(\$c->supplier)->id) : 'no rows';
  "
  ```
  Expected: in ra `OK id=...` (quan hệ load không lỗi) HOẶC `no rows` (bảng trống — vẫn PASS vì eager-load không ném). Lỗi quan hệ/cột → FAIL.
- [ ] **Step 5: Verify hằng + mã** — tinker: `DeliveryContract::CHO_DUYET` = 2, `DeliveryContract::PHU_LUC` = 2, `DeliveryContract::PERM_APPROVE` = `'Duyệt giá vận chuyển'`. (Không commit — xem Global Constraints.)

---

### Task 2: `syncDetails` + builder bảng giá Final + accessor `details_table` (chống crash)

**Files:**
- Modify: `Modules/Transport/Entities/DeliveryContract/DeliveryContract.php` (thêm `syncDetails`, `getDetailsTableAttribute`, `buildFinalRows`).
- Reference: ERP `app/DeliveryContract.php` (`syncDetails` ~:124-135, `getDetailsTableAttribute` ~:230-280, Final snapshot ~:347-384).

**Interfaces:**
- Produces:
  - `syncDetails(array $vehicles, array $roads): void` — port y ERP: xóa `vehicles`/`payloads`/`roads` cũ của HĐ → tạo lại 4 tầng (contract→vehicle(vehicle_category_id)→payload(vehicle_payload_id,extra_price)→road(road_id,km,cost)), denormalize vehicle_category_id/vehicle_payload_id xuống road; **roads dùng chung mảng theo index** (bám ERP). Trong transaction.
  - `getDetailsTableAttribute(): array` — dựng ma trận hiển thị; **nếu HĐ không có vehicles/payloads/roads → trả `[]`** (ERP crash ở đây → đây là adaptation chống crash, Review Focus #1).
  - `buildFinalRows(): array` — tạo bản ghi `final_delivery_contract_vehicle_payload_roads` từ roads+payload (road_id, km, cost, vehicle_category_id, vehicle_payload_id, extra_price). Dùng ở Task 6 (approve) + Task 5 (annex ghi đè Final HĐ gốc theo khóa road_id+vehicle_category_id+vehicle_payload_id).

- [ ] **Step 1:** Đọc 3 đoạn ERP nêu trên + survey §(ma trận/Final). Ghi rõ thứ tự tầng + cách roads chia theo index.
- [ ] **Step 2:** Viết `syncDetails` + `buildFinalRows` bám ERP 1:1. Viết `getDetailsTableAttribute` thêm guard rỗng (đầu hàm: `if (!$this->relationLoaded('vehicles')) $this->load('vehicles.payloads.roads'); if ($this->vehicles->isEmpty()) return [];`).
- [ ] **Step 3: `php -l`** → clean.
- [ ] **Step 4: Verify chống crash (Review Focus #1)** — tinker trên 1 HĐ status=3 chưa có phụ lục:
  ```
  \$c = DeliveryContract::where('type',1)->doesntHave('vehicles')->first() ?? DeliveryContract::first();
  echo json_encode(\$c->details_table); // kỳ vọng: [] — KHÔNG ném TypeError/Undefined
  ```
  Expected: `[]`, không exception.
- [ ] **Step 5: Verify syncDetails** — tinker: tạo HĐ nháp tạm, gọi `syncDetails` với 1 xe/1 tải/2 tuyến → đếm `roads()->count()`=2, `payloads()->count()`=1, `vehicles()->count()`=1; rồi `delete()` dọn. Expected khớp số. (Không commit.)

---

### Task 3: Permission seeder — bộ quyền "Hợp đồng vận chuyển" (guard api)

**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm các dòng `$this->perm([...])` nhóm "Hợp đồng vận chuyển", `type` = số phân hệ Vận chuyển — tra đầu seeder / `subsystems.js`, giống 4 quyền THGVC).
- Reference: skill `permission-seeder`; 4 dòng quyền THGVC trong cùng file (nhóm "Tổng hợp giá vận chuyển đề xuất").

**Interfaces:**
- Produces 11 quyền MỚI (guard api), `group='Hợp đồng vận chuyển'`, `type=<Vận chuyển>`:
  - `Xem hợp đồng vận chuyển theo tổng công ty`
  - `Xem hợp đồng vận chuyển theo công ty`
  - `Xem hợp đồng vận chuyển theo phòng ban`
  - `Thêm hợp đồng vận chuyển`
  - `Sửa hợp đồng vận chuyển`
  - `Xóa hợp đồng vận chuyển`
  - `Lập phụ lục hợp đồng vận chuyển`
  - `Cập nhật kho hợp đồng vận chuyển`
  - `In hợp đồng vận chuyển`
  - `Xuất Excel hợp đồng vận chuyển`
  - `Import hợp đồng vận chuyển`
  - **Duyệt: KHÔNG tạo mới** — dùng lại `"Duyệt giá vận chuyển"` (đã có từ THGVC).
- Giá trị tên khớp hằng `PERM_*` ở Task 1.

- [ ] **Step 1:** Mở seeder, tìm block 4 quyền THGVC để lấy đúng số `type` phân hệ Vận chuyển.
- [ ] **Step 2:** Thêm 11 dòng `$this->perm([...])` (KHÔNG `id`/`guard_name`), đặt cạnh block Vận chuyển, đúng thứ tự hiển thị (3 Xem → Thêm/Sửa/Xóa → Phụ lục → Cập nhật kho → In/Xuất/Import).
- [ ] **Step 3: Dry-run** — `php artisan permission:sync --dry-run` → Expected: "thêm 11" quyền mới, KHÔNG lỗi khai báo, KHÔNG đụng `"Duyệt giá vận chuyển"`.
- [ ] **Step 4: Áp** — `php artisan permission:sync` → ghi DB local. Verify: `Permission::where('guard_name','api')->where('name','Thêm hợp đồng vận chuyển')->exists()` = true. (Không commit.)

---

### Task 4: Service — `scoped()` + `createFromPriceList` / `store` / `update` (HĐ header-only)

**Files:**
- Create: `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php`
- Reference: `Modules/Transport/Services/DeliveryCostSummary/DeliveryCostSummaryService.php` (`scoped`/`employeeIdsSubquery` pattern) + ERP `DeliveryContractController@store/@update/@create` + `PriceListValidDelivery` entity (nguồn snapshot).

**Interfaces:**
- Produces (public):
  - `searchByFilter(Request $r)` → paginate, gọi `scoped()`.
  - `scoped(Request $r, string $alias)` — lọc 3 mức quyền + công ty NGƯỜI TẠO (R1): copy khuôn THGVC `whereIn("$alias.created_by", employeeIdsSubquery('company_id'|'department_id', ...))`; `PERM_VIEW_ALL`/super-admin → không bó; thiếu quyền → `whereRaw('1=0')` (fail-closed); ô lọc `company_id` chỉ áp khi xem-mọi-công-ty, trả `meta.is_all_company`. Phiếu đã duyệt/từ chối người xem vẫn thấy (scope theo quyền, không chỉ "của tôi").
  - `getFormOptions()` — dropdown BGHLVC khả dụng (chưa gắn HĐ / theo công ty người tạo), NCC, tài khoản công ty, nơi cấp CMT...
  - `store(array $data)` — tạo HĐ (type=1): validate đã ở FormRequest; set snapshot từ BGHLVC (`price_list_valid_id` bắt buộc) + nhánh cá nhân/tổ chức; **KHÔNG `syncDetails`, KHÔNG gán kho** (header-only, Ruling B1); status = 3 (nháp) hoặc 2 (gửi ngay) theo cờ `is_send`; `created_by`/`updated_by` auto (BaseModel); gọi `getNextCode()` sau khi có id; đồng bộ `files`.
  - `update(int $id, array $data)` — chỉ khi `canEdit` (status=3 + chính chủ); header-only; BGHLVC disable (không đổi nguồn).
- Consumes: Task 1 entity + hằng; Task 2 chưa dùng ở đây (header-only).

- [ ] **Step 1:** Đọc `scoped()` + `employeeIdsSubquery` của THGVC service; đọc ERP store/update/create (nguồn `price_list_valid_id`, cột snapshot cá nhân/tổ chức) + survey §(store/update header-only, cột snapshot chốt cứng).
- [ ] **Step 2:** Viết service: `scoped` (R1), `getFormOptions`, `store`, `update`. `catch(\Throwable)` + rethrow `ValidationException`. Transaction cho store/update+files.
- [ ] **Step 3: `php -l`** → clean.
- [ ] **Step 4: Verify scope (Review Focus #2)** — tinker giả 2 user thường ở 2 công ty (`Auth::guard('api')->setUser(...)`): user cty A gọi `searchByFilter` → chỉ ra HĐ của employee cty A; user không quyền Xem → tập rỗng; super-admin → ra hết. Expected khớp.
- [ ] **Step 5: Verify store header-only** — tinker: gọi `store` với 1 `price_list_valid_id` hợp lệ → HĐ mới `type=1`, `status` đúng, `vehicles()->count()=0`, `warehouses()->count()=0`, snapshot NCC/tài khoản set đủ, `code` dạng `HĐVC-00001`. Dọn bản ghi test. (Không commit.)

---

### Task 5: Service — `annexStore` / `annexUpdate` (ma trận) + `importExcel` (khớp id/mã)

**Files:**
- Modify: `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php`
- Create: `Modules/Transport/Http/Requests/DeliveryContract/ImportRequest.php` (chỉ `rules()`)
- Reference: ERP `DeliveryContractController@annexStore/@annexUpdate/@quotationImport/@checkQuotationImport`; skill `import-excel`; Task 2 `syncDetails`/`buildFinalRows`.

**Interfaces:**
- Produces:
  - `annexStore(array $data)` — tạo phụ lục (type=2, `parent_contract_id`): validate đầy đủ ma trận; copy snapshot từ HĐ gốc; **kho = kho HĐ gốc**; gọi `syncDetails` thật (Task 2); status=3/2; `getNextCode()` → `<mã gốc>:PL-NN`.
  - `annexUpdate(int $id, array $data)` — chỉ `canAnnexEdit` (status=3 + chính chủ); `syncDetails` lại.
  - `importExcel(int $contractId, UploadedFile $file): array` — parse ma trận cho phụ lục; **khớp theo id/mã** loại xe/trọng tải/tuyến (Ruling F) — fallback theo tên như ERP nếu file không có mã; **lệch khung/mã không khớp HĐ gốc → ném `\Exception`/ImportException, KHÔNG ghi** (Review Focus #3); limit 150 tuyến; trả mảng vehicles/roads để FE nạp vào form (KHÔNG tự lưu — lưu khi submit annex). Luồng đọc file = ngoại lệ số vi-VN (được phép đọc số kiểu VN từ Excel).
  - `getDataForAnnex(int $parentId)` — trả khung ma trận + Final hiện có của HĐ gốc để dựng form phụ lục.

- [ ] **Step 1:** Đọc ERP annexStore/annexUpdate/quotationImport (cách khớp tên fuzzy + limit 150 + wipe-recreate) + survey §Import. Ghi rõ khung cột Excel.
- [ ] **Step 2:** Viết 4 method. `importExcel` đổi khớp fuzzy-tên → **khớp id/mã trước, fallback tên**; mọi lệch → ném exception trước khi ghi.
- [ ] **Step 3: `php -l`** cả service + ImportRequest → clean.
- [ ] **Step 4: Verify annex** — tinker: tạo HĐ gốc (Task 4) → `annexStore` với ma trận 1 xe/1 tải/2 tuyến → phụ lục `type=2`, `parent_contract_id` đúng, kho = kho gốc, `roads()->count()=2`. Dọn.
- [ ] **Step 5: Verify import (Review Focus #3)** — tinker/curl: (a) file đúng khung mã khớp HĐ gốc → trả mảng đúng số tuyến; (b) file lệch thứ tự / mã không thuộc HĐ gốc → ném exception, KHÔNG có bản ghi road nào được tạo. Expected cả 2.

---

### Task 6: Service — `send` + `approve` (Final* + closeContract + notify) + từ chối

**Files:**
- Modify: `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php`
- Reference: ERP `DeliveryContractController@send/@approve` + `DeliveryContract::closeContract` (~:405-446) + Final snapshot; skill `notification-convention`; THGVC service `approve`/notify pattern.

**Interfaces:**
- Produces:
  - `send(int $id)` — `canEdit`/chính chủ + status=3 → status=2; notify người có `PERM_APPROVE` theo công ty người tạo (deep-link ID). Template `[PREFIX] Gửi duyệt: <mã HĐ>. ...`.
  - `approve(int $id, array $data)` — **duyệt (action→1):** set `approver_id`/`approved_time`; sinh `final_delivery_contract_vehicle_payload_roads` qua `buildFinalRows` (Task 2); nếu là **phụ lục** → ghi đè/bổ sung Final của HĐ gốc theo khóa (road_id+vehicle_category_id+vehicle_payload_id) + cập nhật `final_min_extra_km` (Ruling E); gọi `closeContract`; status=1; notify người tạo `[PREFIX] Duyệt: <mã>`. **Từ chối (action→3):** bắt buộc `approver_comment` → status=3 + notify `[PREFIX] Từ chối: <mã>. <comment>`.
  - `closeContract(DeliveryContract $c)` — (Ruling D, R3) đóng (status=4) các HĐ khác **cùng `supplier_id`** + **trùng ít nhất 1 kho** (qua `delivery_contract_has_warehouses`), loại trừ chính nó + HĐ đã hủy (status=0). KHÔNG điều kiện loại xe (ERP đã comment). KHÔNG dùng `checkCloseContract` chết.
- Consumes: Task 2 `buildFinalRows`; Task 1 quan hệ warehouses/annexes.

- [ ] **Step 1:** Đọc ERP send/approve + `closeContract` + cơ chế Final (approve status=1 mới snapshot; phụ lục merge Final gốc). Ghi rõ điều kiện closeContract.
- [ ] **Step 2:** Viết `send`/`approve`/`closeContract`. Transaction. Rethrow ValidationException. Notify đúng template + deep-link.
- [ ] **Step 3: `php -l`** → clean.
- [ ] **Step 4: Verify approve + Final** — tinker: 1 phụ lục status=2 → `approve(action=1)` → status=1, `approver_id` set, `final_delivery_contract_vehicle_payload_roads` của HĐ gốc có dòng tương ứng; `approve(action=3)` thiếu comment → ném ValidationException. Expected.
- [ ] **Step 5: Verify closeContract (Review Focus #5)** — tinker: dựng 3 HĐ cùng kho K: HĐ1 cùng NCC (đã duyệt), HĐ2 khác NCC, HĐ3 cùng NCC khác kho. Duyệt 1 HĐ mới cùng NCC+kho K → chỉ HĐ1 → status=4; HĐ2/HĐ3 giữ nguyên. Dọn. Expected.

---

### Task 7: Service — `updateWarehouse` + `destroy` + accessor cờ hành động

**Files:**
- Modify: `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php`
- Modify: `Modules/Transport/Entities/DeliveryContract/DeliveryContract.php` (method cờ `canEdit/canAnnex/canAnnexEdit/canUpdateWarehouse/canDelete/canApprove`).
- Reference: ERP `@updateWarehouse` (`canUpdateWarehouse` = type HOP_DONG + chính chủ + status=1) + `@delete` + các `can*` ERP.

**Interfaces:**
- Produces (entity methods, bám ERP + Global gate):
  - `canEdit()` = chính chủ && type=HOP_DONG && status=DANG_TAO.
  - `canAnnex()` = quyền `PERM_ANNEX` && type=HOP_DONG && status=DA_DUYET (lập phụ lục từ HĐ đã duyệt — xác nhận theo ERP).
  - `canAnnexEdit()` = chính chủ && type=PHU_LUC && status=DANG_TAO.
  - `canUpdateWarehouse()` = quyền `PERM_UPDATE_WAREHOUSE` && type=HOP_DONG && chính chủ && status=DA_DUYET.
  - `canDelete()` = chính chủ && status=DANG_TAO.
  - `canApprove()` = `isCurrentEmployeeHasPermission(PERM_APPROVE)` && status=CHO_DUYET. **KHÔNG check cùng công ty** (bẫy 11 — giữ hành vi ERP).
- Service:
  - `updateWarehouse(int $id, array $warehouseIds)` — `canUpdateWarehouse` → sync `delivery_contract_has_warehouses` → gọi `closeContract` (Task 6). 423/422 nếu sai trạng thái.
  - `destroy(int $id)` — `canDelete` → status=0 (KHÔNG xóa cứng, bám ERP). 423 nếu không đủ điều kiện.

- [ ] **Step 1:** Đọc các `can*` ERP + `updateWarehouse`/`delete`. Đối chiếu điều kiện status chính xác (survey §can*).
- [ ] **Step 2:** Viết cờ trên entity + `updateWarehouse`/`destroy` trên service. Cờ gate bằng `isCurrentEmployeeHasPermission` (fail-closed).
- [ ] **Step 3: `php -l`** → clean.
- [ ] **Step 4: Verify** — tinker: HĐ đã duyệt chính chủ → `canUpdateWarehouse()`=true, `updateWarehouse` đổi kho + closeContract chạy; HĐ status=1 gọi `destroy` → ném/không đổi (chỉ status=3 mới hủy); HĐ status=3 chính chủ `destroy` → status=0. Expected.
- [ ] **Step 5: Verify canApprove không bó công ty** — tinker: user có `PERM_APPROVE` khác công ty người tạo, HĐ status=2 → `canApprove()`=true. Expected (bám ERP). (Không commit.)

---

### Task 8: Service — `exportRows` + `printData` + `printListData` (chống crash rỗng)

**Files:**
- Modify: `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php`
- Create: `Modules/Transport/Exports/DeliveryContract/DeliveryContractExcel.php` + blade `Resources/views/exports/delivery_contract.blade.php`
- Reference: THGVC `DeliveryCostSummaryExcel` + export blade (pattern số thô + data-format); ERP mẫu in `report_templates` `HOP_DONG_VAN_CHUYEN`/`..._TO_CHUC`/`PHU_LUC_...`/`BANG_KE_GIA_CUOC_VAN_CHUYEN`; skill `print-page` §8 (popup) + `export-excel`.

**Interfaces:**
- Produces:
  - `exportRows(Request $r)` — xuất Excel danh sách theo `scoped()`; chia `export-rows` nếu >2s; số thô + data-format; **HĐ rỗng chi tiết → ô chi tiết trống an toàn** (Review Focus #1).
  - `printData(int $id): array` — trả `{ data: { template: '<html>' } }` dựng từ ReportTemplate theo `supplier->type` (cá nhân `HOP_DONG_VAN_CHUYEN` / tổ chức `..._TO_CHUC`; phụ lục `PHU_LUC_...`); letterhead theo công ty NGƯỜI TẠO (R2); **HĐ rỗng chi tiết → bảng giá rỗng, KHÔNG 500**.
  - `printListData(Request $r): array` — bản in bảng kê `BANG_KE_GIA_CUOC_VAN_CHUYEN` theo scope. Số `1,234,567.89`.
- Consumes: Task 2 `details_table` (đã guard rỗng).

- [ ] **Step 1:** Đọc THGVC Excel/blade + ERP mẫu in + survey §(print/export, crash khi rỗng). Xác định cột bảng kê.
- [ ] **Step 2:** Viết `exportRows`+Excel/blade + `printData`/`printListData`. Mọi đường đọc chi tiết dùng accessor đã guard; thêm guard rỗng tại điểm dựng HTML.
- [ ] **Step 3: `php -l`** service + Excel + blade compile → clean.
- [ ] **Step 4: Verify chống crash (Review Focus #1)** — curl `:8000` JWT: `print-data` trên HĐ status=3 header-only → 200, template có header + bảng giá rỗng (KHÔNG 500); `export` danh sách có HĐ rỗng → file tải được, ô chi tiết trống. Expected.
- [ ] **Step 5: Verify số + letterhead** — mở Excel: ô số kiểu `n` fmt `#,##0`/`#,##0.00`; template in letterhead = công ty người tạo. Expected. (Không commit.)

---

### Task 9: Controller + routes + FormRequests + Transformers

**Files:**
- Create: `Modules/Transport/Http/Controllers/V1/DeliveryContract/DeliveryContractController.php`
- Create: `Modules/Transport/Http/Requests/DeliveryContract/{StoreRequest,UpdateRequest,AnnexStoreRequest,AnnexUpdateRequest,ApproveRequest,UpdateWarehouseRequest}.php` (ImportRequest đã ở Task 5)
- Create: `Modules/Transport/Transformers/DeliveryContract/{DeliveryContractListResource,DeliveryContractDetailResource}.php`
- Modify: `Modules/Transport/Routes/api.php` (block `delivery-contracts`, **static trước `{id}`**)
- Reference: THGVC `DeliveryCostSummaryController` + Routes block + Resources (pattern); ERP controller (parity endpoint, bỏ `create2` — Ruling G).

**Interfaces:**
- Produces routes (middleware `checkPermission`, bỏ `create2`): `index` (của tôi) · `all` (tất cả, status!=3) · `show` · `store` · `update` · `annexStore` · `annexUpdate` · `getDataForAnnex` · `send` · `approve` · `destroy` · `updateWarehouse` · `importExcel`/`checkImport` · `exportList` · `printData` · `printListData` · `formOptions`.
  - `all` dùng cùng service, override scope qua cờ ở controller (merge BE), KHÔNG để FE gửi.
  - `approve` dùng `ApproveRequest`; `update`/`annexUpdate`/`updateWarehouse` → guard khóa/trạng thái ở middleware route (423) theo khuôn `CheckCustomerNotLocked`; re-check `isCurrentEmployeeHasPermission` cho endpoint nhạy cảm.
- `ApproveRequest.rules()` — **khai đủ id các tầng** nếu `validated()` tiêu thụ (payload id, road id/km/road_id) để không bị strip (Review Focus #4 — bẫy THGVC Task 14): `approver_comment` nullable (required khi từ chối, check ở service/rule conditional), `action` in [1,3], `details.*.id`, `details.*.roads.*.{id,road_id,km}` v.v. theo cấu trúc modal.
- `DeliveryContractListResource` — STT/mã/NCC/kho/người duyệt/ngày duyệt/người tạo/ngày tạo/`status_text`/`status_color`/dòng "Phụ lục cho HĐ <mã gốc>" + cờ `is_can_{approve,edit,annex,annex_edit,delete,update_warehouse}` (từ entity methods, KHÔNG hard-code). `DeliveryContractDetailResource` — header + ma trận (nếu có) + Final + kho + files + cờ. Eager-load chống N+1.

- [ ] **Step 1:** Đọc THGVC controller/routes/resources + ERP controller parity. Liệt kê endpoint khớp ERP (bỏ create2).
- [ ] **Step 2:** Viết controller + 6 FormRequest (chỉ `rules()`) + 2 Resource + routes (static trước `{id}`). `ApproveRequest` khai đủ id tầng.
- [ ] **Step 3: `php -l`** tất cả → clean.
- [ ] **Step 4: Smoke runtime** — curl `:8000` JWT (emp thường): `index` 200 (data/total/lastPage/currentPage/perPage + status_text/status_color/is_can_*); `show` → gated đúng; `approve` no-perm → 403, no-token → 401; `update` HĐ khóa/sai trạng thái → 423; `all` chỉ status!=3. Expected.
- [ ] **Step 5: Verify ApproveRequest id-carry (Review Focus #4)** — curl `approve` happy-path với payload mang id tầng → service đọc được id (KHÔNG "Undefined index: id"), Final sinh đúng. Expected. (Không commit.)

---

### Task 10: FE — `api.js` + `index.vue` (của tôi) + `all` + bộ lọc

**Files:**
- Create: `hrm-client/pages/transport/delivery-contracts/api.js`
- Create: `hrm-client/pages/transport/delivery-contracts/index.vue` (của tôi)
- Create: `hrm-client/pages/transport/delivery-contracts/all.vue` (hoặc `index.vue` đọc `?type=all`) 
- Reference: `pages/transport/delivery-cost-summaries/{api.js,index.vue}` (khuôn 4 mixin list-page) + skill `list-page`.

**Interfaces:**
- Consumes: Task 9 endpoints (`index`/`all`/`formOptions`) + cờ `is_can_*` + `status_text`/`status_color`.
- 4 mixin: `PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`. `localStorageKey`/`columnScreenKey`/`table` DUY NHẤT (`delivery_contracts`, `delivery_contracts_all`).
- Cột: STT, Mã (`<nuxt-link>`; phụ lục hiện "Phụ lục cho HĐ <mã gốc>"), NCC, Kho, Người duyệt, Ngày duyệt, Người tạo, Ngày tạo, Trạng thái (badge BE), Hành động. Sort mặc định ngày tạo giảm dần.
- Lọc (floating): Mã, NCC, Kho, Người tạo, Người duyệt, Trạng thái (**đủ 5 option** kể cả Đóng). Ô Công ty chỉ hiện khi `meta.is_all_company`.
- Hành động dòng (ẩn v-if): Tạo phụ lục (`is_can_annex`), Sửa (`is_can_edit`/`is_can_annex_edit`), Xóa (`is_can_delete`), Cập nhật kho (`is_can_update_warehouse`), In / In bảng kê / Xuất (luôn hiện).

- [ ] **Step 1:** Đọc `delivery-cost-summaries/index.vue`+`api.js` làm khuôn; đọc design §6.
- [ ] **Step 2:** Viết `api.js` + `index.vue` + `all.vue`. `layout: 'default-sidebar'`. Số `1,234,567.89`. Badge từ BE.
- [ ] **Step 3: Grep self-check** — Expected RỖNG:
  ```
  grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/transport/delivery-contracts/ | grep -v V2Base
  grep -rnE "toLocaleString\(\s*'vi-VN'" pages/transport/delivery-contracts/   # cho SỐ
  ```
- [ ] **Step 4: Playwright** (`127.0.0.1:3000`) — vào `/transport/delivery-contracts`: bảng ra đủ cột, badge đúng màu, lọc Trạng thái có 5 option, đổi trang/sort chỉ 1 request (đếm Network), không có mega-menu ERP (vỏ `default-sidebar`). Chụp ảnh đặt cạnh màn THGVC. Expected khớp.

---

### Task 11: FE — `create.vue` + `_id/edit.vue` + `ContractForm.vue` (header-only từ BGHLVC)

**Files:**
- Create: `hrm-client/pages/transport/delivery-contracts/create.vue`, `_id/edit.vue`, `components/ContractForm.vue`
- Reference: `delivery-cost-summaries/create.vue`+form + skill `form-validate`/`select-and-input-state`/`unsaved-changes`.

**Interfaces:**
- Consumes: Task 9 `store`/`update`/`show`/`formOptions`.
- Form header-only: NCC (V2BaseSelect), min_extra_km (V2BaseCurrencyInput/number quốc tế), chọn **BGHLVC** (edit → disable), nhánh **cá nhân** (CMT/ngày/nơi cấp) / **tổ chức** (MST/người đại diện/chức vụ) theo loại NCC, tài khoản công ty, ghi chú, file (`V2BaseFile`/FileAttachmentTable → bảng `files`), mẫu in theo loại NCC. Nút Lưu nháp / Lưu & gửi duyệt (`is_send`). V2Base-only. Sau lưu → `markFormSaved()` + về danh sách.

- [ ] **Step 1:** Đọc khuôn create THGVC + form. Ghi field cá nhân/tổ chức.
- [ ] **Step 2:** Viết `ContractForm.vue` (dùng chung create/edit) + `create.vue` + `_id/edit.vue`. Validate FE nhẹ (BE là nguồn thật). `unsavedChangesMixin`.
- [ ] **Step 3: Grep self-check** (như Task 10) → RỖNG.
- [ ] **Step 4: Playwright** — tạo HĐ: chọn BGHLVC → submit → về danh sách, HĐ mới status Đang tạo; mở Sửa → BGHLVC disabled; đổi nhánh cá nhân/tổ chức hiện đúng field. Expected.

---

### Task 12: FE — Phụ lục (`annex/create` + `_id/edit` + `AnnexForm` + ma trận + `ImportModal`)

**Files:**
- Create: `hrm-client/pages/transport/delivery-contracts/annex/create.vue`, `annex/_id/edit.vue`, `components/AnnexForm.vue`, `components/CostMatrix.vue` (hoặc tái dùng của THGVC), `components/ImportModal.vue`
- Reference: `delivery-cost-summaries/components/{CostMatrix,ImportQuotationModal}.vue` + `utils/matrixFrame.js`; skill `import-excel`/`modal-popup`.

**Interfaces:**
- Consumes: Task 9 `annexStore`/`annexUpdate`/`getDataForAnnex`/`importExcel`/`checkImport`.
- Chọn HĐ gốc qua modal (chỉ HĐ `is_can_annex`). Ma trận xe/tải/tuyến đầy đủ (ô trống đúng vị trí khi NCC thiếu — dùng `matrixFrame`). Import Excel → nạp vào form (chưa lưu); lệch khung → toast lỗi, không nạp. Sửa phụ lục chỉ khi status=3. Số quốc tế (trừ ô đọc file import).

- [ ] **Step 1:** Đọc CostMatrix/ImportQuotationModal + matrixFrame của THGVC.
- [ ] **Step 2:** Viết AnnexForm + ma trận + ImportModal + create/edit phụ lục.
- [ ] **Step 3: Grep self-check** → RỖNG.
- [ ] **Step 4: Playwright** — tạo phụ lục từ HĐ đã duyệt: nhập ma trận 1 xe/1 tải/2 tuyến → lưu → phụ lục Đang tạo; import file đúng khung → ma trận nạp đúng; import file lệch → toast lỗi, không nạp. Expected.

---

### Task 13: FE — `_id/index.vue` chi tiết + `ApproveModal` + `UpdateWarehouseModal`

**Files:**
- Create: `hrm-client/pages/transport/delivery-contracts/_id/index.vue`, `components/ApproveModal.vue`, `components/UpdateWarehouseModal.vue`
- Reference: `delivery-cost-summaries/_id/index.vue` + `components/ApproveModal.vue`; skill `modal-popup`/`button-convention`.

**Interfaces:**
- Consumes: Task 9 `show`/`approve`/`send`/`updateWarehouse`/`destroy` + cờ.
- Tiêu đề `Chi tiết hợp đồng vận chuyển: <mã>`. Header + tab ma trận (nếu có) + Final + kho + files. Footer `V2Footer` + `#custom-actions`: Duyệt (`is_can_approve`), Gửi duyệt, Sửa, Xóa, Lập phụ lục, Cập nhật kho, In, In bảng kê, Xuất Excel — **khớp hành động & điều kiện với danh sách** (Task 10). ApproveModal mang đủ id tầng (Review Focus #4) + ô từ chối bắt buộc comment. Nút cụm `mr-2 mb-2`.

- [ ] **Step 1:** Đọc chi tiết + ApproveModal THGVC.
- [ ] **Step 2:** Viết `_id/index.vue` + 2 modal. Hành động đối chiếu đúng list.
- [ ] **Step 3: Grep self-check** → RỖNG.
- [ ] **Step 4: Playwright** — mở HĐ status Chờ duyệt bằng user có quyền Duyệt: bấm Duyệt → status Đã duyệt, Final hiện; bấm Từ chối không nhập comment → chặn; Cập nhật kho đổi kho → HĐ trùng kho cũ chuyển Đóng. Đối chiếu nút detail = nút list. Expected.

---

### Task 14: FE — In popup (HĐ + bảng kê)

**Files:**
- Create: `hrm-client/pages/transport/delivery-contracts/components/PrintPreviewModal.vue` (hoặc tái dùng bộ popup chung — grep trước)
- Modify: `_id/index.vue` + `index.vue` (đấu nút In → popup)
- Reference: skill `print-page` §8 (popup, BE `print-data`/`print-list-data` đã có ở Task 8).

**Interfaces:**
- Consumes: Task 8 `printData`/`printListData` (trả `{data:{template}}`).
- Nút In (dòng list + detail) → **popup xem trước ngay tại chỗ** (KHÔNG `window.open('/print')`). In HĐ (theo loại NCC) + In bảng kê. Số `1,234,567.89`. Letterhead công ty người tạo (R2).

- [ ] **Step 1:** Grep bộ popup in dùng chung trong repo (skill §8); chọn đúng component có sẵn.
- [ ] **Step 2:** Đấu nút In/In bảng kê → popup, nạp `template` từ BE.
- [ ] **Step 3: Grep self-check** — không `window.open('/…/print')`; số không vi-VN.
- [ ] **Step 4: Playwright** — bấm In ở 1 dòng → popup hiện tờ giấy có letterhead + bảng giá (HĐ có phụ lục) / bảng rỗng an toàn (HĐ header-only); In bảng kê → danh sách. Expected.

---

### Task 15: FE — Menu + đối chiếu parity (list ↔ detail ↔ ERP ↔ màn ngang)

**Files:**
- Modify: `hrm-client/components/subsystem-menu/transport.js` (thêm mục "Hợp đồng vận chuyển")
- Reference: khuôn mục THGVC trong cùng file; skill `erp-to-hrm-screen` Bước 5/5b; skill `new-screens-sweep`.

**Interfaces:**
- Mục menu "Hợp đồng vận chuyển" → `/transport/delivery-contracts`, `isShow` = **mảng 3 quyền Xem** (PERM_VIEW_ALL/COMPANY/DEPARTMENT), KHÔNG `isShow:true`. Giữ tên ngắn. (Đấu nút "Lập HĐ" ở THGVC = bước "nối logic" sau, KHÔNG làm ở đây — design §7.)

- [ ] **Step 1:** Mở `transport.js`, tìm mục THGVC làm khuôn.
- [ ] **Step 2:** Thêm mục HĐ vận chuyển (link + isShow mảng 3 quyền).
- [ ] **Step 3: Đối chiếu Bước 5 + 5b** — cột/lọc/hành động HRM vs ERP đủ & đúng điều kiện; đối chiếu ngang 2–3 màn HRM đã QA (THGVC + 1 màn phiếu duyệt) cho header/file/footer/toast; ghi vào báo cáo "đã bám màn X khối Y".
- [ ] **Step 4: Playwright** — menu hiện đúng với tài khoản có 1 trong 3 quyền Xem; ẩn với tài khoản không có; click vào mục ra danh sách. Expected.

---

## Self-Review

**1. Spec coverage (design §2–§8):**
- A (nguồn BGHLVC) → Task 4 `store` dùng `price_list_valid_id`; Task 11 form chọn BGHLVC. ✅
- B1 (header-only + chống crash) → Task 4 (store không syncDetails) + Task 2 (accessor guard) + Task 8 (print/export guard) + Review Focus #1. ✅
- C (quyền 3 mức + lọc công ty + Duyệt dùng lại) → Task 3 (seeder) + Task 4 (`scoped` R1). ✅ (R1 giải xung đột "thêm cột".)
- D (closeContract) → Task 6. ✅  E (phụ lục ghi đè Final) → Task 2 `buildFinalRows` + Task 6 approve. ✅
- F (import id/mã) → Task 5. ✅  G (bỏ create2/cột di sản/checkCloseContract) → Global Constraints + R3 + Task 9 (bỏ create2). ✅
- 5 trạng thái + 2 type → Task 1 hằng; ô lọc đủ 5 option → Task 10. ✅
- In popup (4 mẫu) → Task 8 (BE) + Task 14 (FE). ✅  Thông báo template → Task 6. ✅  Menu → Task 15. ✅
- 11 bẫy §8: supplier→customers (Global+Task4/5), snapshot chốt cứng (Task4), di sản/checkCloseContract (R3/Global), create2 (Task9), header-only crash (RF#1), import tên→id (Task5/RF#3), `\Exception` (Global), lọc company (RF#2/R1), deleteFile→files (Global), Final no parent_id (Task2/6), canApprove không bó cty (Task7). ✅

**2. Step scan:** Mỗi step quyết định đúng một việc; code body chỉ ở nơi signature+ERP-source không tự quyết (không có — mọi logic chỉ về ERP/sibling + adaptation nêu rõ). Không có "TBD"/"handle edge cases". ✅

**3. Type consistency:** Hằng `PERM_*` (Task 1) = tên quyền seeder (Task 3) = `checkPermission` route + `isShow` menu (Task 9/15). Cờ `is_can_*` (entity Task 7) = Resource (Task 9) = v-if FE (Task 10/13). `buildFinalRows` (Task 2) dùng ở Task 6. `scoped()`/`employeeIdsSubquery` (Task 4) mirror THGVC. ✅

**4. Review Focus:** 5 lớp đã gắn test vào task sở hữu (RF#1→Task2/8; RF#2→Task4; RF#3→Task5; RF#4→Task9; RF#5→Task6/7). ✅

**5. Proportion:** Plan ~ dài hơn design vài lần nhưng phần lớn là bước verify runtime + Interfaces (quyết định không thể suy) — không transcribe code ERP (chỉ trỏ file:line + sibling). 15 task khớp shape THGVC 16 task. ✅
