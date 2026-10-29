# Kế hoạch triển khai — Port màn "Bảng giá hiệu lực vận chuyển" (PriceListValidDelivery) ERP → HRM · CHỈ ĐỌC

> **Cho người thực thi (AI/engineer):** SUB-SKILL BẮT BUỘC khi thực thi: `superpowers:subagent-driven-development` (đề xuất) hoặc `superpowers:executing-plans`. Mỗi màn/endpoint bám **skill `erp-to-hrm-screen`** (6 bước) — ERP là nguồn **nghiệp vụ**, HRM là nguồn **khuôn UI/form**. Các bước dùng checkbox (`- [ ]`) để theo dõi. Nhánh: `develop` (hậu duệ `gop_db`) ở cả hrm-api lẫn hrm-client → tài liệu ở `.plans/gop-db/`.

**Goal:** Đưa màn "Bảng giá hiệu lực vận chuyển" của ERP (`price-list-valid-deliveries`) sang HRM tại **Vận chuyển › Vận chuyển với NCC › Bảng giá hiệu lực vận chuyển** dạng **CHỈ ĐỌC** — danh sách, chi tiết (ma trận tuyến × xe → trọng tải, ô = đơn giá cước, phân trang tuyến + lọc tuyến), tab "Báo giá" (file NCC xem/tải), **In**, và **Gia hạn** (đổi ngày hiệu lực đến).

**Architecture:** BE = bổ sung quan hệ cho 4 entity `PriceListValidDelivery*` **đã có sẵn** ở `Modules/Finance/Entities/Delivery/` + 1 entity mới `PriceListValidDeliveryQuotation` (tab Báo giá); 1 Service đọc + phân trang **ở tầng DB** (KHÔNG load-all như ERP), 1 Controller V1 ở `Modules/Transport` + 1 FormRequest gia hạn + 2 Resource; 2 quyền mới guard `api`. FE = thư mục `pages/transport/valid-delivery-prices/` (Nuxt2/Vue2, V2Base\*) với `index.vue` (list) + `_id/index.vue` (chi tiết ma trận + lọc tuyến + tab Báo giá) + `_id/print.vue` (bản in khổ ngang) + 1 modal Gia hạn dùng chung. DB chung `erp_hrm_check` — mọi bảng **đã tồn tại**, KHÔNG migration.

**Tech Stack:** hrm-api Laravel 8 / PHP 7.4 (`Modules/*`, guard `api`); hrm-client Nuxt 2.14 / Vue 2 / Node 14.21.3 / V2Base\*; MySQL `erp_hrm_check` @127.0.0.1:3306.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/bang-gia-hieu-luc-van-chuyen/design.md` (đã DUYỆT). Plan này lập luận từ spec đó — mọi hành vi nghiệp vụ chi tiết tra ở spec.
Nguồn ERP (đọc khi thi công, đã khảo sát):
- Controller `ERP/TanPhatDev/app/Http/Controllers/Common/PriceListValidDeliveryController.php` — `getRoadData` (dòng 100–121, có lọc `road_ids`), `extendDate` (200–234), `searchData` (24), `show` (66), `print` (186).
- Model `ERP/TanPhatDev/app/Model/Common/PriceListValidDelivery.php` — `getRoads($id)` (dòng 90–145, thuật toán gom cột), `searchByFilter` (28), `generateCode` (45).
- Model con: `PriceListValidDeliveryVehicle/VehiclePayload/VehiclePayloadRoad.php`, `PriceListValidDeliveryQuotation.php` (`supplier()`, `attachment()` hasOne File).
- Blade `ERP/.../resources/views/common/price_list_valid_deliveries/{index,show}.blade.php` (card lọc tuyến show.blade 100–127; ma trận 129–190; modal gia hạn index 24–65) + partial `ListPriceDelivery.blade.php`.
- Service in `ERP/.../app/Services/PriceListValidDelivery/PriceListValidDeliveryService.php` — `getDataPrint` (235), `getTable`/`processPayloads` (246/306).

Khuôn HRM (bám 1:1 màn anh em đã port):
- Controller `HRM/hrm-api/Modules/Transport/Http/Controllers/V1/DeliveryQuotation/DeliveryQuotationController.php` + `DeliveryQuotationLookupController.php`.
- Service `HRM/hrm-api/Modules/Transport/Services/DeliveryQuotation/DeliveryQuotationService.php`.
- Resource `HRM/hrm-api/Modules/Transport/Transformers/DeliveryQuotation/{DeliveryQuotationListResource,DeliveryQuotationDetailResource}.php`.
- Entity `HRM/hrm-api/Modules/Transport/Entities/DeliveryQuotation/*.php` (khuôn `generateCode` str_pad 5, `getDataForShow`).
- Entity đích CÓ SẴN (thiếu quan hệ): `HRM/hrm-api/Modules/Finance/Entities/Delivery/PriceListValidDelivery*.php`.
- FE list + detail + ma trận: `HRM/hrm-client/pages/transport/delivery-quotations/{index.vue,_id/index.vue,components/DeliveryQuotationForm.vue,api.js}`.
- File/NCC: `HRM/hrm-api/app/Models/File.php` (`file_path`/`file_name`), `HRM/hrm-api/Modules/Finance/Entities/Supplier.php` (`$table='customers'`).

## Global Constraints

(Mỗi task ngầm bao gồm toàn bộ mục này — trích từ HRM CLAUDE.md + spec.)

- **Scope thư mục:** mọi thao tác trong `HRM/` (hrm-api hoặc hrm-client). KHÔNG tạo file ở root `ERP-HRM/`. Chỉ port **màn này**; màn sinh bảng giá ("Tổng hợp chi phí vận chuyển") để nguyên chưa port.
- **AI KHÔNG commit/push git.** Kết thúc mỗi task = checkpoint để **user** review + tự commit. hrm-client đẩy `develop` sau khi user chốt; hrm-api **giữ local** chờ review (xác nhận lại lúc bàn giao).
- **CHỈ ĐỌC + Gia hạn:** KHÔNG Tạo/Sửa ma trận/Xóa/Sao chép/Xuất Excel (ERP màn này cũng không có). Chỉ 1 thao tác GHI duy nhất = **Gia hạn** (đổi `date_valid_to`).
- **Vị trí code (builder-call đã chốt trong plan):** giữ 4 entity `PriceListValidDelivery*` **tại chỗ** ở `Modules/Finance/Entities/Delivery/` (ERP-side không đổi), **bổ sung quan hệ** vào đó; entity mới `PriceListValidDeliveryQuotation` đặt **cùng** `Modules/Finance/Entities/Delivery/`. Controller/Service/Resource/FormRequest/Route đặt ở `Modules/Transport` (đồng bộ menu + FE + màn anh em).
- **Quyền:** TẠO 2 QUYỀN MỚI guard `api` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` qua `$this->perm([...])` (KHÔNG `id`/`guard_name`), `type` = phân hệ **Vận chuyển** (tra `hrm-client/components/subsystems.js`). KHÔNG tái dùng quyền ERP ("Quản lý chi phí vận chuyển" / "Duyệt giá vận chuyển" — guard web → 403). KHÔNG phân quyền dữ liệu theo công ty/phòng/bộ phận; KHÔNG có ô lọc Công ty; ai có quyền xem **mọi** bảng giá.
- **Entity đọc-thuần:** các `PriceListValidDelivery*` `extends Model` (`$guarded=['*']`) — KHÔNG `BaseModel` (màn chỉ đọc, không ghi audit; riêng Gia hạn tự set `updated_by = auth()->id()` ở service).
- **Mã phiếu:** hiển thị `code` có sẵn (`BGHLVC-` + 5 số). Màn chỉ đọc → **KHÔNG** sinh mã, KHÔNG `getNextCode()`.
- **FE:** chỉ `V2Base*` (không HTML thô). Cờ quyền **fail-closed** (không hard-code `=true`). Số định dạng quốc tế `1,234,567.89` (`toLocaleString('en-US')`). `.text-muted` đỏ → nhãn dùng `#6b7280`. Ô rỗng để **trống** (không "—", không "_"). Nút trong `V2Footer`; cụm nút `mr-2 mb-2` (nút cuối `mb-2`). Nút không dùng được **ẩn** bằng `v-if` (không disable). Nhãn **"Người tạo" / "Ngày tạo"**. Catalog lớn → search server-side. Bảng tràn ngang bọc `V2BaseTableScroll`. Mỗi màn ≤ 5 API *dữ liệu chính* (lookup không tính).
- **Không có cột `status`** → KHÔNG dựng badge trạng thái (không có gì để map). Chỉ hiển thị khoảng ngày hiệu lực.
- **FormRequest:** chỉ `rules()`, KHÔNG `messages()` cho rule phổ biến (dùng lang file). `authorize()` quyết định 403.
- **Bản ghi khoá/chỉ đọc:** màn này không có khoá; Gia hạn gate ở BE (quyền OR người tạo), FE ẩn nút khi không đủ điều kiện.
- **Verify trước khi báo xong:** BE qua `php artisan route:list` + curl/tinker; FE qua **Playwright** gõ phím thật, local (`bash HRM/.claude/skills/run-hrm/run-hrm.sh`, API :8000, client :3000, mở `http://127.0.0.1:3000` — KHÔNG `localhost`). So KẾT QUẢ với màn ERP tương ứng. Làm việc + trả lời **tiếng Việt**; KHÔNG đọc file thư viện hệ thống.

## Review Focus

(5 lớp input/thất bại spec hàm ý mà happy-path không chạm — mỗi dòng đã gắn test vào task sở hữu code.)

1. **Ma trận dữ liệu KHÔNG đều — một tuyến thiếu ô ở một payload** → phải căn ô theo **cột payload ở HEADER**, ô thiếu để **trống**, tuyệt đối không dồn cột làm bảng lệch (anti-goal spec §5.6). ERP căn theo `road.payloads` nên lệ thuộc dữ liệu đều — HRM không được chép lỗi đó. *(Task 3 getRoadData + Task 6)*
2. **Gia hạn bởi account KHÔNG có quyền "Gia hạn..." VÀ KHÔNG phải người tạo** → BE phải trả **403** (fail-closed, Quyết định #2), không được dựa vào FE ẩn nút. *(Task 4)*
3. **Gia hạn với `date_valid_to` = hôm nay hoặc quá khứ** → **422** (`after:today`), KHÔNG được ghi. *(Task 4)*
4. **Lọc tuyến: `road_ids` rỗng / không gửi** → trả **toàn bộ** tuyến phân trang (không trả rỗng); gửi `road_ids` → chỉ các tuyến đã chọn. *(Task 3)*
5. **Bảng giá ~14.400 tuyến (bảng lá ~86.462 dòng)** → `getRoadData` chỉ truy vấn **trang hiện tại ở DB** (phân trang DISTINCT road_id), KHÔNG nạp cả ma trận vào PHP mỗi request (anti-goal spec §2; ERP đang load-all). *(Task 3)*

---

### Task 1: BE — bổ sung quan hệ 4 entity + entity mới `PriceListValidDeliveryQuotation`

**Files:**
- Modify: `hrm-api/Modules/Finance/Entities/Delivery/PriceListValidDelivery.php` (hiện chỉ có `vehicles()`)
- Modify: `.../Delivery/PriceListValidDeliveryVehicle.php` (hiện chỉ `payloads()`)
- Modify: `.../Delivery/PriceListValidDeliveryVehiclePayload.php` (hiện chỉ `roads()`)
- Modify: `.../Delivery/PriceListValidDeliveryVehiclePayloadRoad.php` (hiện không quan hệ)
- Create: `.../Delivery/PriceListValidDeliveryQuotation.php`

**Bảng (đã tồn tại, KHÔNG migrate):** xem design §4 — `price_list_valid_deliveries` (6 dòng, không `status`), `..._vehicles` (14), `..._vehicle_payloads` (65, `extra_price` decimal 16,2), `..._vehicle_payload_roads` (86.462, `road_id`, `km` decimal 10,2, `cost` decimal 16,2), `price_list_valid_delivery_quotations` (63, chỉ `price_list_valid_delivery_id` + `supplier_id`, KHÔNG audit).

**Interfaces (Produces):**
- `PriceListValidDelivery`: thêm `company()` belongsTo `Modules\...\Company`; `quotations()` hasMany `PriceListValidDeliveryQuotation` FK `price_list_valid_delivery_id`; `employee_create()` (người tạo — dùng helper hiện có cho "Người tạo", xem `employeeAuditLabel` ở Resource màn anh em). (`vehicles()` giữ nguyên.)
- `PriceListValidDeliveryVehicle`: thêm `vehicle_category()` belongsTo `Modules\MasterData\Entities\Vehicle\VehicleCategory` (FK `vehicle_category_id`).
- `PriceListValidDeliveryVehiclePayload`: thêm `vehicle_payload()` belongsTo `Modules\MasterData\Entities\Vehicle\VehiclePayload` (FK `vehicle_payload_id`). (`extra_price` đọc trực tiếp.)
- `PriceListValidDeliveryVehiclePayloadRoad`: thêm `road()` belongsTo `Modules\Assign\Entities\TpRoad` (FK `road_id`).
- `PriceListValidDeliveryQuotation` (mới, `extends Model`, `$table='price_list_valid_delivery_quotations'`, `$guarded=['*']`): `supplier()` belongsTo `Modules\Finance\Entities\Supplier` (FK `supplier_id`, thực chất bảng `customers`); `files()` hasMany `App\Models\File` (`table_id`→`id`, `->where('table','price_list_valid_delivery_quotations')`). (Dùng `files()` theo khuôn CLAUDE.md "File đính kèm", KHÔNG chép `attachment()` hasOne của ERP.)

- [ ] **Bước 1: Xác minh cột `files` thật trên DB gộp** — `mysql ... erp_hrm_check -e "DESCRIBE files"` và `... -e "SELECT id,table,table_id,file_name,file_path FROM files WHERE table='price_list_valid_delivery_quotations' LIMIT 5"`. Chốt dùng `file_path`/`file_name` (khuôn HRM). ERP `attachment()` tham chiếu `path`/`name` — KHÔNG chép; đối chiếu để chắc cột thật.
- [ ] **Bước 2: Thêm quan hệ** vào 4 entity Finance + viết entity `PriceListValidDeliveryQuotation` theo Interfaces trên (bám khuôn quan hệ ở `Modules/Transport/Entities/DeliveryQuotation/*`).
- [ ] **Bước 3 (verify): tinker đọc dữ liệu thật.** `php artisan tinker` (hrm-api) →
  `Modules\Finance\Entities\Delivery\PriceListValidDelivery::with(['company','vehicles.vehicle_category','vehicles.payloads.vehicle_payload','vehicles.payloads.roads.road','quotations.supplier','quotations.files'])->first()` — kỳ vọng trả cây không lỗi quan hệ: `company.name`, `vehicle_category.name`, `vehicle_payload.name`, `roads[].road.name`, `quotations[].supplier` (từ customers) có tên, `quotations[].files[].file_path`.
- [ ] **Bước 4: Checkpoint** — báo user review entity (hrm-api giữ local).

---

### Task 2: BE — 2 quyền mới (seeder đồng bộ)

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (theo skill `permission-seeder`).

**Interfaces (Produces):** 2 dòng `$this->perm([...])`, guard `api` (seeder tự gán), `type` = phân hệ **Vận chuyển** (tra số trong `components/subsystems.js` / bảng đầu seeder), `group` hợp lý (vd "Vận chuyển"):
- `Quản lý bảng giá hiệu lực vận chuyển` — xem danh sách + chi tiết + in.
- `Gia hạn bảng giá hiệu lực vận chuyển` — thao tác gia hạn.

- [ ] **Bước 1:** Thêm 2 dòng `$this->perm(['name'=>..., 'display_name'=>..., 'group'=>'Vận chuyển', 'type'=><Vận chuyển>])` cạnh các quyền cùng phân hệ. KHÔNG `id`/`guard_name`.
- [ ] **Bước 2 (verify trước):** `php artisan permission:sync --dry-run` → thấy "thêm 2" đúng tên, guard api, không đụng quyền khác. Rồi `php artisan permission:sync` ghi DB local.
- [ ] **Bước 3 (verify):** query `permissions` thấy 2 dòng mới guard `api`, `type` Vận chuyển; (sau Task 3/4) route gắn `checkPermission:Quản lý bảng giá hiệu lực vận chuyển` trả **403** khi account chưa gán, **200** khi đã gán.
- [ ] **Bước 4: Checkpoint** user review + gán quyền cho account test.

---

### Task 3: BE — Service đọc + Resource + Controller (index, show, getRoadData, roadOptions, print-data) + route

**Files:**
- Create: `hrm-api/Modules/Transport/Services/PriceListValidDelivery/PriceListValidDeliveryService.php`
- Create: `.../Transformers/PriceListValidDelivery/PriceListValidDeliveryListResource.php` (`extends ResourceCollection`)
- Create: `.../Transformers/PriceListValidDelivery/PriceListValidDeliveryDetailResource.php`
- Create: `.../Http/Controllers/V1/PriceListValidDelivery/PriceListValidDeliveryController.php`
- Modify: `.../Routes/api.php` (thêm nhóm route)

**Interfaces:**
- *Consumes:* entity + quan hệ (Task 1); quyền (Task 2).
- *Produces (route, prefix `/v1/transport/valid-delivery-prices`, middleware `checkPermission:Quản lý bảng giá hiệu lực vận chuyển`; URL đầy đủ `/api/v1/transport/...`). Route **tĩnh đặt TRƯỚC** `/{id}`:*
  - `GET /` `index(Request)` → danh sách phân trang. Filter: `code` (like), `created_by` (=), `keyword` (tìm nhanh theo `code`). Sort mặc định `created_at` DESC; `SORTABLE_COLUMNS` = `code`, `created_at`. KHÔNG scope công ty. Bọc `PriceListValidDeliveryListResource` + `->additional(['total','lastPage','currentPage','perPage'])` (khuôn `DeliveryQuotationController::index`).
  - `GET /{id}` `show($id)` → `PriceListValidDeliveryDetailResource`: thông tin chung (`code`, `company_name`, `date_valid_from`/`date_valid_to` RAW + hiển thị `d/m/Y`, `km_actual`) + **khung cột** (`vehicles[].vehicle_category_name` → `payloads[].{vehicle_payload_name, extra_price}`) + **tab Báo giá** (`quotations` nhóm theo supplier: `supplier_name` + `files[].{file_name,file_path,file_type,file_size}`) + cờ `is_can_extend`. **KHÔNG** trả thân ma trận (roads) ở đây — roads qua `getRoadData`.
  - `GET /{id}/road-data` `getRoadData(Request,$id)` → phân trang **tuyến**; nhận `page`/`per_page`, `road_ids[]` (lọc). Mỗi tuyến: `road_id`, `road_name`, `km`, `cells` (mảng `cost` **align theo đúng thứ tự cột payload của header**, ô thiếu = `null`). Trả `{data, total, lastPage, currentPage, perPage}`.
  - `GET /{id}/road-options` `roadOptions(Request,$id)` → liệt kê tuyến **phân biệt** của bảng giá cho bộ lọc: `{id, name}`, có `keyword` search server-side + `limit` (KHÔNG load toàn bộ). (lookup — không tính ≤5 API chính.)
  - `GET /{id}/print-data` `printData($id)` → dữ liệu bản in: thông tin chung + khung cột + **toàn bộ** tuyến (không phân trang) để FE dựng bản in. (Dùng cho Task 7; chấp nhận nặng vì in cần đủ.)
- *Service:*
  - `searchByFilter($request)->paginate($perPage)` — chỉ `select` cột cần + `with('company')` (eager, chống N+1).
  - `getDetail($id)` — load khung cột (eager `vehicles.vehicle_category`, `vehicles.payloads.vehicle_payload`, `quotations.supplier`, `quotations.files`), KHÔNG load roads.
  - `getRoadData($id, $roadIds, $page, $perPage)` — **phân trang ở DB** (xem thuật toán dưới).
  - `getRoadOptions($id, $keyword, $limit)` — DISTINCT `road_id` của bảng giá join `roads` lấy tên, `where name like`, `limit`.
  - `getPrintData($id)` — như getDetail + toàn bộ roads (gọi getRoadData không phân trang / per_page lớn theo chunk).
  - `isCanExtend($priceList)` — `isCurrentEmployeeHasPermission('Gia hạn bảng giá hiệu lực vận chuyển') || auth()->id() == $priceList->created_by` (fail-closed).

**Thuật toán `getRoadData` (builder-call spec §5.6 — phân trang DB, giữ đúng shape ERP):**
1. Đọc ERP `getRoads($id)` (Model dòng 90–145) để khớp **cách gom cột**: cột = `groupBy('vehicle_category_id')` rồi theo thứ tự `payloads` của từng xe; mỗi ô khớp theo cặp (`price_list_valid_delivery_vehicle_id`=`v_id`, `vehicle_payload_id`).
2. **Trang tuyến:** truy vấn **DISTINCT `road_id`** của bảng giá (từ bảng lá scope theo `price_list_valid_delivery_id`, qua join 3 bảng), `orderBy road_id` (hoặc theo thứ tự tuyến gốc — khớp blade ERP), `->forPage($page,$perPage)` **ở SQL** (`limit/offset`), đếm tổng bằng `COUNT(DISTINCT road_id)`. Nếu có `road_ids` → `whereIn('road_id', $roadIds)` trước khi phân trang.
3. **Lấy ô cho trang:** `whereIn('vpr.road_id', <road_ids của trang>)` join lấy `v_id, vehicle_category_id, vp_id, vehicle_payload_id, cost, km, road_id` + tên tuyến (`roads`).
4. **Dựng từng dòng tuyến:** với mỗi road, map `cells` theo **đúng thứ tự cột header** (Task 3 show trả thứ tự này) — ô (road × payload) không có bản ghi → `null` (để trống). KHÔNG dùng `road.payloads` thứ tự tự do như ERP (Review Focus #1).
5. `km` hiển thị theo cột `km` bảng lá của tuyến đó (đọc blade ERP `road.km` để khớp — các payload cùng tuyến có km bằng nhau).

- [ ] **Bước 1:** Viết Service (6 method trên), 2 Resource (list + detail), Controller (5 action), route group (tĩnh trước `/{id}`). `is_can_extend` fail-closed trong detail Resource.
- [ ] **Bước 2 (verify Review Focus #1,#4,#5):** curl (kèm token local) từng endpoint:
  - `GET /` trả danh sách, filter `code`/`created_by` lọc đúng, sort `created_at` desc; đổi `page`/`per_page` chỉ 1 truy vấn trang.
  - `GET /{id}` trả khung cột + quotations nhóm NCC + `is_can_extend`; **không** có roads.
  - `GET /{id}/road-data`: không `road_ids` ⇒ toàn bộ tuyến phân trang; có `road_ids` ⇒ chỉ tuyến đó *(RF#4)*. Dòng tuyến có `cells` align đúng số cột header, bảng giá dữ liệu không đều ⇒ ô thiếu = `null` *(RF#1)*. Bật query log (`DB::enableQueryLog`) xác nhận chỉ `limit/offset` theo trang, **không** `SELECT` cả 86k/14.4k dòng *(RF#5)*.
  - `GET /{id}/road-options?keyword=` trả ≤ `limit` tuyến khớp.
  - `GET /{id}/print-data` trả đủ tuyến.
  - So số cột/ô với màn ERP `show` của cùng `id`.
- [ ] **Bước 3: Checkpoint** user review (hrm-api giữ local).

---

### Task 4: BE — Gia hạn (`extendDate`) + FormRequest fail-closed

**Files:**
- Create: `hrm-api/Modules/Transport/Http/Requests/PriceListValidDelivery/ExtendDateRequest.php`
- Modify: `.../Services/PriceListValidDelivery/PriceListValidDeliveryService.php` (+ `extendDate`)
- Modify: `.../Http/Controllers/V1/PriceListValidDelivery/PriceListValidDeliveryController.php` (+ `extendDate`)
- Modify: `.../Routes/api.php` (+ route POST)

**Interfaces:**
- *Consumes:* `isCanExtend()` (Task 3); entity (Task 1).
- *Produces:*
  - `ExtendDateRequest`: `rules()` = `['date_valid_to' => 'required|date|after:today']` (KHÔNG `messages()`). `authorize()` = `isCanExtend($priceList)` (nạp bản ghi theo route param) → **403 trước validate** nếu không đủ điều kiện (Quyết định #2, bám ERP `extendDate` dòng 217).
  - Route: `POST /{id}/extend-date` `extendDate(ExtendDateRequest, $id)`, cùng nhóm `checkPermission:Quản lý bảng giá hiệu lực vận chuyển` (route tĩnh, đặt trước `/{id}`).
  - `Service::extendDate($id, $dateValidTo)` — set `date_valid_to` + `updated_by = auth()->id()` (entity đọc-thuần không auto audit) → `save()`. Trả bản ghi mới.
  - Controller trả `responseJson('Thao tác thành công', 200, [...])` (câu toast chuẩn — không tự chế).

- [ ] **Bước 1:** Viết `ExtendDateRequest` (authorize = isCanExtend, rules 1 trường), `Service::extendDate`, `Controller::extendDate`, route POST.
- [ ] **Bước 2 (verify Review Focus #2,#3):** curl:
  - account có quyền "Gia hạn..." ⇒ 200, DB `date_valid_to` đổi, `updated_by` = account.
  - account KHÔNG quyền "Gia hạn..." nhưng **là người tạo** ⇒ 200.
  - account KHÔNG quyền VÀ KHÔNG phải người tạo ⇒ **403** *(RF#2)*.
  - `date_valid_to` = hôm nay / quá khứ ⇒ **422**, không ghi *(RF#3)*.
  - Đối chiếu account thường (KHÔNG super admin — super admin qua `Gate::before` che mất 403, skill `erp-to-hrm-screen` Bước 1).
- [ ] **Bước 3: Checkpoint** user review (hrm-api giữ local).

---

### Task 5: FE — danh sách + gắn menu + modal Gia hạn dùng chung

**Files:**
- Create: `hrm-client/pages/transport/valid-delivery-prices/index.vue`
- Create: `.../valid-delivery-prices/api.js`
- Create: `.../valid-delivery-prices/components/ExtendDateModal.vue`
- Modify: `hrm-client/components/subsystem-menu/transport.js:46` (thêm `link` + `isShow`)

**Interfaces (Consumes):** `GET /` index, `POST /{id}/extend-date` (Task 3/4).

- [ ] **Bước 1:** Dựng list bám skill `list-page` + khuôn `pages/transport/delivery-quotations/index.vue`. 4 mixin (`PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`); `V2BaseSmartFilterPanel` **floating**; ô tìm nhanh "Tìm theo mã"; bộ lọc **Mã** + **Người tạo** (select, nhãn floating); `columnCustomizationMixin` + `user_column_settings` (`columnScreenKey` duy nhất) + `<ColumnCustomizationModal v-if="columnFieldsLoaded">`. `V2BaseDataTable` cột: STT / **Mã** (`nuxt-link` sang chi tiết, chữ thường) / Công ty / Hiệu lực từ (`d/m/Y`) / Hiệu lực đến / **Người tạo** / **Ngày tạo** / Hành động; sortable `code`+`created_at` với `@sort`+`:sortBy`/`:sortDirection`; sort mặc định ngày tạo giảm dần. **KHÔNG** cột Trạng thái, **KHÔNG** nút Thêm. Cột Hành động (ẩn bằng `visible`/`v-if`): **In** (luôn hiện) · **Gia hạn** (hiện khi `is_can_extend`). `canManage = hasAPermission('Quản lý bảng giá hiệu lực vận chuyển')`.
- [ ] **Bước 2:** `ExtendDateModal.vue` trên `components/modal/V2BaseModal.vue`: 1 ô `V2BaseDatePicker` "Hiệu lực đến" (validate `required` + `after:today` qua vee-validate; select trong modal nếu có → `V2BaseSelectInModal`); submit gọi `POST /{id}/extend-date`; thành công → toast chuẩn, đóng modal, reload danh sách. Dùng chung cho list + detail (Task 6).
- [ ] **Bước 3:** Gắn menu `transport.js:46`: thêm `link: '/transport/valid-delivery-prices'` + `isShow` theo quyền "Quản lý bảng giá hiệu lực vận chuyển". **KHÔNG đổi `label`** (giữ "Bảng giá hiệu lực vận chuyển").
- [ ] **Bước 4 (verify):** Playwright (mở `http://127.0.0.1:3000`): đăng nhập → Vận chuyển › Vận chuyển với NCC › Bảng giá hiệu lực vận chuyển → list render đúng cột, tìm nhanh theo Mã + lọc Người tạo lọc đúng (chờ ≥3s), nút Gia hạn hiện/ẩn khớp `is_can_extend`; mở modal Gia hạn, chọn ngày quá khứ ⇒ báo lỗi; chọn ngày hợp lệ ⇒ toast + ngày đổi. So layout + cột với ERP `index`.
- [ ] **Bước 5: Checkpoint** user review (hrm-client đẩy develop sau khi chốt).

---

### Task 6: FE — Chi tiết (ma trận phân trang + lọc tuyến + tab Báo giá)

**Files:**
- Create: `hrm-client/pages/transport/valid-delivery-prices/_id/index.vue`
- Create: `.../components/PriceMatrixTable.vue` (ma trận read-only, phân trang tuyến)
- Create: `.../components/QuotationTab.vue` (tab Báo giá — file NCC xem/tải)

**Interfaces (Consumes):** `GET /{id}` show, `GET /{id}/road-data` (+`road_ids`), `GET /{id}/road-options`, `POST /{id}/extend-date`; tái dùng `ExtendDateModal.vue` (Task 5).

- [ ] **Bước 1:** `_id/index.vue` — tiêu đề `Chi tiết bảng giá hiệu lực vận chuyển: <code>`. Khối **Thông tin chung** (`V2BaseFormSection` hoặc khuôn chi tiết màn anh em): Mã, Công ty, Hiệu lực từ/đến, Số Km (ô đọc `V2Base* disabled`). Khối Chi tiết dựng 2 tab (hoặc section): **Ma trận** + **Báo giá**. `V2Footer` với `url-back` + nút **In** (sang `_id/print.vue`) + **Gia hạn** (mở `ExtendDateModal`, hiện khi `is_can_extend` — **khớp danh sách**). Cờ quyền từ payload show (không gọi show lần 2).
- [ ] **Bước 2:** `PriceMatrixTable.vue` — bám ma trận của `components/DeliveryQuotationForm.vue` (header 2 hàng colspan theo `payloads.length` + hàng "Giá cước vượt trội" = `extra_price`), chuyển **read-only**: body `v-for road` × `v-for cột payload theo HEADER`, ô = `cost` (format `toLocaleString('en-US')`), ô `null`/0 ⇒ **để trống** (Review Focus #1). Bọc `V2BaseTableScroll` (cuộn trên+dưới). Thân tuyến nạp qua `GET /{id}/road-data` **phân trang** (`V2BaseDataTable` pagination hoặc `uib`-style page control); đổi trang gọi lại API. Trên bảng: ô **"Lọc tuyến đường"** = `V2BaseSelect` multiple (hoặc `V2BaseSelectInModal` nếu lớn) nạp từ `GET /{id}/road-options` search server-side; chọn → truyền `road_ids` vào road-data + về trang 1; xoá lọc → bỏ `road_ids`.
- [ ] **Bước 3:** `QuotationTab.vue` — bảng STT / Nhà cung cấp / File (nhóm theo `supplier_name`), mỗi file link tải (`file_path`, nhãn `file_name`). Dùng component đính kèm sẵn có ở chế độ read-only nếu khớp (grep `FileAttachmentTable.vue` / `V2BaseAttachmentSection.vue` — **đối chiếu ngang màn đã QA**, skill Bước 5b, ghi lại "copy pattern từ `<file:dòng>`"); NCC không có file vẫn hiện dòng (xem/tải thôi, không upload/xoá).
- [ ] **Bước 4 (verify Review Focus #1):** Playwright: mở chi tiết 1 bảng giá → ma trận render đúng số cột (xe→payload) + hàng "Giá cước vượt trội"; phân trang tuyến đổi trang ra dữ liệu khác (không treo với bảng ~14.4k tuyến); chọn "Lọc tuyến đường" vài tuyến ⇒ bảng chỉ còn tuyến đó; tab Báo giá hiện file, bấm tải được; nút In + Gia hạn khớp danh sách. So ma trận + tab với ERP `show`.
- [ ] **Bước 5: Checkpoint** user review.

---

### Task 7: FE — Bản in (khổ ngang)

**Files:**
- Create: `hrm-client/pages/transport/valid-delivery-prices/_id/print.vue`

**Interfaces (Consumes):** `GET /{id}/print-data` (Task 3).

- [ ] **Bước 1:** `print.vue` bám skill `print-page` (mục 2c) + khuôn print.vue hiện có (vd `pages/finance/borrow-sell-requests/_id/print.vue`): khung giấy **A4 ngang** (`297mm`), nền xám `#eee` dùng chung (không khai `background` riêng), `.print-preview` `min-height:100vh`+`display:flow-root`, nút **In** `V2BaseButton primary size="sm"` căn phải. Nội dung: letterhead theo `company_id` **của chứng từ** (skill `print-page` mục 4b — KHÔNG theo người đăng nhập), thông tin chung + **ma trận đầy đủ** (header xe→payload + hàng "Giá cước vượt trội" + mọi tuyến), số định dạng `1,234,567.89`. Cấu trúc cột bám `getTable()`/`processPayloads()` của service ERP.
- [ ] **Bước 2 (verify):** Playwright: từ chi tiết bấm **In** → trang in hiện khung giấy ngang, letterhead đúng công ty bảng giá, ma trận đủ cột + tuyến khớp chi tiết; preview `window.print` không vỡ cột. So bản in ERP `print_landscape`.
- [ ] **Bước 3: Checkpoint** user review.

---

## Ghi chú thực thi

- **Thứ tự:** Task 1→4 (BE) trước, rồi 5→7 (FE) — FE phụ thuộc interface BE. Task 2 có thể làm song song sau Task 1. Task 7 phụ thuộc Task 3 (`print-data`).
- Mỗi task kết thúc = **checkpoint cho user** (AI không commit). hrm-client đẩy `develop` sau khi user chốt; hrm-api giữ local chờ review (xác nhận lại lúc bàn giao).
- Luôn so trực tiếp với màn ERP `price-list-valid-deliveries` khi verify từng phần; đối chiếu ngang 2–3 màn HRM đã QA (skill Bước 5b).
- Builder-call còn mở (design §7, mặc định an toàn): có tô màu dòng bảng giá đã hết hiệu lực ở danh sách không (mặc định **không**, chỉ hiện khoảng ngày) — hỏi user nếu muốn thêm.
