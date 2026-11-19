# Kế hoạch triển khai — Port màn "Danh mục mẫu báo giá vận chuyển" (DeliveryQuotation) ERP → HRM

> **Cho người thực thi (AI/engineer):** SUB-SKILL BẮT BUỘC khi thực thi: `superpowers:subagent-driven-development` (đề xuất) hoặc `superpowers:executing-plans`. Mỗi màn/endpoint bám **skill `erp-to-hrm-screen`** (6 bước) — ERP là nguồn **nghiệp vụ**, HRM là nguồn **khuôn UI/form**. Các bước dùng checkbox (`- [ ]`) để theo dõi.

**Goal:** Đưa trọn màn "Danh mục mẫu báo giá vận chuyển" của ERP (`/admin/delivery_quotations`) sang HRM tại **Vận chuyển › Vận chuyển với NCC › Danh mục mẫu báo giá vận chuyển** — gồm danh sách, thêm, sửa, chi tiết, và mọi chức năng ở cột Hành động (Sửa / Xóa / Sao chép / Xuất excel / Tổng hợp giá đề xuất).

**Architecture:** BE = module mới `Modules/Transport` (Laravel 8, nwidart) với 4 entity master-detail bám 1:1 quan hệ ERP, 1 Service bọc transaction (`syncDetails` port nguyên), 1 Controller V1 + FormRequest + Resource, các endpoint phụ trợ đọc danh mục (bảng giá hiệu lực, điểm đầu, tuyến đường). FE = thư mục `pages/transport/delivery-quotations/` (Nuxt2/Vue2, V2Base\*) với list/create/edit/detail + component form chứa **ma trận** (port từ 4 class ES6 của ERP) + 2 modal (chọn tuyến / thêm nhanh tuyến). DB dùng chung `erp_hrm_check` — 4 bảng + `delivery_start_points` + `roads` + bảng giá hiệu lực **đã tồn tại**, KHÔNG migration cho bảng chính.

**Tech Stack:** hrm-api Laravel 8 / PHP 8 (Modules/*); hrm-client Nuxt 2.14 / Vue 2 / Node 14.21.3 / thư viện V2Base\*; MySQL `erp_hrm_check` @127.0.0.1:3306.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/mau-bao-gia-van-chuyen/design.md` (đã DUYỆT). Plan này lập luận từ spec đó — mọi hành vi nghiệp vụ chi tiết (status, validate, overlap, copy, excel, dropdown bảng giá) tra ở spec. Nguồn ERP: `ERP/TanPhatDev/app/Http/Controllers/Common/DeliveryQuotationController.php`, `app/Model/Common/DeliveryQuotation{,Vehicle,VehiclePayload,VehiclePayloadRoad}.php`, `resources/views/admin/delivery_quotations/*` + `partials/classes/common/DeliveryContract*`.

## Global Constraints

(Mỗi task ngầm bao gồm toàn bộ mục này — trích nguyên từ HRM CLAUDE.md + spec.)

- **Scope thư mục:** mọi thao tác trong `HRM/` (hrm-api hoặc hrm-client). KHÔNG tạo file ở root `ERP-HRM/`. Chỉ port **màn này**; các màn anh em (Tổng hợp giá đề xuất, bảng giá…) để nguyên chưa port.
- **AI KHÔNG commit/push git.** Kết thúc mỗi task là một checkpoint để **user** review + tự commit. (Tiền lệ port PXK: hrm-client đẩy `develop`, hrm-api GIỮ LOCAL chờ review — chốt lại lúc bàn giao.)
- **FE:** chỉ dùng component `V2Base*` (không HTML thô). Cờ quyền **fail-closed** (không hard-code `=true`). Số định dạng quốc tế `1,234,567.89`. Badge qua `V2BaseBadge` dùng `status_text`/`status_color` do BE trả. Nút nằm trong `V2Footer`. Dùng `unsavedChangesMixin`. Nút không dùng được thì **ẩn** (không disable). Catalog lớn → search phía server. Nhãn **"Người tạo" / "Ngày tạo"**. Mỗi màn ≤ 5 API *dữ liệu chính* (các lookup danh mục không tính).
- **Quyền:** tạo quyền HRM mới guard `api` (khai trong seeder qua `$this->perm([...])`, KHÔNG set `id`/`guard_name`), `type` = phân hệ Vận chuyển = **22**. KHÔNG phân quyền theo công ty/phòng (bám ERP: `searchByFilter` hiện MỌI bản ghi). Sửa/Xóa chỉ của **chính mình** và chỉ khi `status == 3`.
- **Code sinh mã:** `BGVC-` + `str_pad(id, 5, '0', STR_PAD_LEFT)` — lặp y ERP `generateCode(5, id)` (dựa id, KHÔNG theo năm), gọi sau khi `save()` lần đầu để có id. Bảng `code` UNIQUE dùng chung giữa ERP+HRM nên tuyệt đối không đổi quy tắc.
- **Verify trước khi tuyên bố xong:** BE qua `php artisan route:list` + gọi API thật (curl) hoặc tinker; FE qua **Playwright** (gõ phím thật) chạy local (`bash HRM/.claude/skills/run-hrm/run-hrm.sh`, API :8000, client :3000, mở `127.0.0.1:3000`). So KẾT QUẢ với màn ERP tương ứng.
- Làm việc + trả lời bằng **tiếng Việt**. KHÔNG đọc file thư viện hệ thống.

## Review Focus

(5 lớp input/thất bại spec hàm ý mà test từng task cần chạm — mỗi dòng đã gắn vào task sở hữu code.)

1. **Lưu KHÔNG chọn bảng giá hiệu lực mà khoảng ngày trùng bảng giá đã có** → phải chặn "Đã có bảng giá hiệu lực trong khoảng thời gian này" (overlap check). *(Task 4)*
2. **Sửa mà bỏ trống Ghi chú** → ERP bắt buộc `note` khi update (store thì không) → phải báo lỗi validate. *(Task 4 + Task 7)*
3. **Sửa/Xóa phiếu của người khác hoặc phiếu status ≠ 3** → BE phải chặn (403/thông báo), FE phải ẩn nút. *(Task 4 + Task 8)*
4. **Ma trận: bỏ 1 dòng xe / 1 tải trọng rồi lưu** → `syncDetails` xóa-tạo-lại đúng cây 3 cấp, không rác dòng cũ, `delivery_quotation_id` + `vehicle_category_id` + `vehicle_payload_id` ở bảng road đóng đúng. *(Task 4)*
5. **"Thêm nhanh tuyến" chọn điểm đầu + tỉnh ra >800 tuyến** → giới hạn 800 như ERP, không treo UI. *(Task 2 + Task 6)*

---

### Task 1: BE — 4 entity master-detail + logic model

**Files:**
- Create: `hrm-api/Modules/Transport/Entities/DeliveryQuotation/DeliveryQuotation.php`
- Create: `.../Entities/DeliveryQuotation/DeliveryQuotationVehicle.php`
- Create: `.../Entities/DeliveryQuotation/DeliveryQuotationVehiclePayload.php`
- Create: `.../Entities/DeliveryQuotation/DeliveryQuotationVehiclePayloadRoad.php`

**Bảng (đã tồn tại, KHÔNG migrate):** `delivery_quotations`, `delivery_quotation_vehicles` (parent_id→quotations, vehicle_category_id), `delivery_quotation_vehicle_payloads` (parent_id→vehicles, delivery_quotation_id, vehicle_payload_id), `delivery_quotation_vehicle_payload_roads` (parent_id→payloads, delivery_quotation_id, road_id, km decimal(10,2), vehicle_category_id, vehicle_payload_id).

**Interfaces (Produces):**
- `DeliveryQuotation`: `vehicles()` hasMany(DeliveryQuotationVehicle,'parent_id'); scope/static `getDataForEdit($id)`, `getDataForShow($id)` (eager `vehicles.payloads.roads.road`, `payloads.vehicle_payload`, `vehicles.vehicle_category`); `syncDetails(array $vehicles, array $roads): void`; `generateCode(): void` (set `code="BGVC-".str_pad($this->id,5,'0',STR_PAD_LEFT)` rồi save); `canEdit()/canDelete()` = `status==3 && auth id==created_by`; `canSummaryCost()` = `status==1 || creator`. `employee_create()` relation người tạo (bám helper HRM hiện có cho "Người tạo").
- `DeliveryQuotationVehicle`: `payloads()`, `vehicle_category()` belongsTo `VehicleCategory` (Modules/MasterData), `syncPayloads($payloads,$roads)`.
- `DeliveryQuotationVehiclePayload`: `roads()`, `vehicle_payload()` belongsTo `VehiclePayload`, `parent()`, `syncRoads($roads,$baseRoads)` (dùng `$baseRoads[$i]['road_id']`+`km`, gán `vehicle_category_id` từ `parent->vehicle_category_id`).
- `DeliveryQuotationVehiclePayloadRoad`: `parent()`, `road()` belongsTo `TpRoad` (Modules/Assign, bảng `roads`).

- [ ] **Bước 1: Port 4 entity** từ ERP (`ERP/.../app/Model/Common/DeliveryQuotation*.php`) sang namespace `Modules\Transport\Entities\DeliveryQuotation`, kế thừa base model của HRM (xem khuôn `Modules/MasterData/Entities/Vehicle/VehicleCategory.php`), đổi FK class sang entity HRM (`VehicleCategory`, `VehiclePayload`, `TpRoad`). `syncDetails/syncPayloads/syncRoads` giữ nguyên thuật toán; `generateCode` thay helper ERP bằng `str_pad` inline.
- [ ] **Bước 2 (verify): tinker đọc dữ liệu thật.** Chạy `php artisan tinker` →
  `Modules\Transport\Entities\DeliveryQuotation\DeliveryQuotation::getDataForShow(<id của BGVC-00089>)` — kỳ vọng trả về cây vehicles→payloads→roads có `road.name`, `vehicle_payload.name`, `vehicle_category.name` không lỗi quan hệ.
- [ ] **Bước 3: Checkpoint** — báo user review entity (hrm-api giữ local).

---

### Task 2: BE — endpoint phụ trợ (bảng giá hiệu lực, điểm đầu, tuyến đường)

**Files:**
- Modify: `hrm-api/Modules/Transport/Routes/api.php` (khai nhóm route + middleware `checkPermission`)
- Create: `.../Http/Controllers/V1/DeliveryQuotation/PriceListValidDeliveryLookupController.php` (hoặc bổ sung controller sẵn có của `Modules/Finance` nếu đã có route — kiểm tra trước)
- Create: `.../Http/Controllers/V1/DeliveryQuotation/DeliveryStartPointController.php`
- Create: `.../Entities/DeliveryStartPoint.php` (bảng `delivery_start_points`, 7 dòng — HRM CHƯA có entity)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/RoadController.php` (+ `Modules/Assign/Routes/api.php`) thêm search + by-province, hoặc đặt trong Transport nếu gọn hơn.

**Interfaces (Produces) — các GET lookup (không tính vào ≤5 API chính):**
- `GET /api/transport/price-list-valid-deliveries` → list `{id, code}` bảng giá hiệu lực (nguồn dropdown). Entity `PriceListValidDelivery` (Modules/Finance, đã có).
- `GET /api/transport/price-list-valid-deliveries/{id}/data` → `{date_valid_from, date_valid_to, km_actual}` (điền form khi chọn bảng giá — bám `changePriceListValid` ERP, KHÔNG prefill ma trận).
- `GET /api/transport/delivery-start-points/getAll` → list `{id, name, ...}`.
- `GET /api/assign/roads/search?keyword=&limit=` → search tuyến server-side (catalog ~3210 dòng).
- `GET /api/assign/roads/by-province?start_point_id=&province_id=` → tuyến theo điểm đầu + tỉnh, **giới hạn 800** (bám `addQuickRoad`/`getRoadByProvince` ERP).

- [ ] **Bước 1:** Kiểm tra route sẵn có cho bảng giá hiệu lực + điểm đầu (`grep -rn "price-list-valid\|delivery-start\|delivery_start" Modules/*/Routes`). Tái dùng nếu có; nếu thiếu thì tạo controller mỏng (chỉ đọc).
- [ ] **Bước 2:** Viết 5 endpoint trên, map đúng tham số ERP. Giới hạn 800 cho by-province.
- [ ] **Bước 3 (verify):** `php artisan route:list | grep -E "price-list-valid|delivery-start|roads"` thấy đủ; `curl` từng endpoint (kèm token đăng nhập local) trả JSON đúng shape; by-province với điểm đầu + tỉnh nhiều tuyến ⇒ ≤800 bản ghi.
- [ ] **Bước 4: Checkpoint** user review.

---

### Task 3: BE — quyền "Quản lý mẫu báo giá vận chuyển"

**Files:**
- Modify: seeder quyền của phân hệ Vận chuyển — `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (hoặc seeder quyền của Transport nếu tách; theo khuôn skill `permission-seeder`).

**Interfaces (Produces):** tên quyền `Quản lý mẫu báo giá vận chuyển`, guard `api`, `type = 22`. (Chỉ 1 quyền quản-lý cho toàn màn; không tách Xem/Sửa — bám ERP canEdit/canDelete theo creator+status, không theo quyền.)

- [ ] **Bước 1:** Thêm `$this->perm([... 'name' => 'Quản lý mẫu báo giá vận chuyển', 'type' => 22 ...])` (không set id/guard_name) theo skill `permission-seeder`.
- [ ] **Bước 2:** `php artisan db:seed --class=...PermissionsTableSeeder` (hoặc lệnh seeder tương ứng).
- [ ] **Bước 3 (verify):** query DB `permissions` thấy dòng mới guard `api` type 22; route Task 2/4 gắn `checkPermission:Quản lý mẫu báo giá vận chuyển` trả 403 khi account chưa gán, 200 khi đã gán.
- [ ] **Bước 4: Checkpoint** user review + gán quyền cho account test.

---

### Task 4: BE — Service + FormRequest + Resource + Controller + route CRUD

**Files:**
- Create: `.../Services/DeliveryQuotation/DeliveryQuotationService.php`
- Create: `.../Http/Requests/DeliveryQuotation/DeliveryQuotationStoreRequest.php`
- Create: `.../Http/Requests/DeliveryQuotation/DeliveryQuotationUpdateRequest.php`
- Create: `.../Transformers/DeliveryQuotation/DeliveryQuotationResource.php` (+ resource con cho ma trận nếu cần)
- Create: `.../Http/Controllers/V1/DeliveryQuotation/DeliveryQuotationController.php`
- Modify: `.../Routes/api.php`

**Interfaces:**
- *Consumes:* entity + `syncDetails` (Task 1); overlap check dựa bảng giá hiệu lực (Task 2).
- *Produces (route, prefix `/api/transport/delivery-quotations`, middleware checkPermission):*
  - `GET /` index → danh sách phân trang (filter `code`, `note`, `created_by`; orderBy `created_at` DESC; KHÔNG scope công ty). Trả `code`, `note`, người tạo, ngày tạo, `is_can_edit`, `is_can_delete`, `is_can_summary_cost`, `status_text`, `status_color`.
  - `GET /{id}` show → `getDataForShow` dạng ma trận cho màn chi tiết/sửa.
  - `POST /` store, `PUT /{id}` update, `DELETE /{id}` destroy, `POST /{id}/copy` copy.
- *Service:* `store/update` bọc `DB::transaction` → lưu master → `generateCode()` (store) → `syncDetails($vehicles,$roads)`. `delete` chỉ khi `canDelete()`, xóa con theo thứ tự road→payload→vehicle rồi master. `copy($id)` trả data cho form (bản ghi mới khi submit).

**Validate (bám ERP `store`/`update`):**
- `date_from` rule: nếu có `price_list_valid_id` → `required`; nếu không → `required|date|after_or_equal:today`.
- `vehicles` 1..99 (min 1), `payloads` 1..99, `roads` 1..2000 (min 1), `km` numeric 1..999999999, `km_actual` required.
- Nếu **không** có `price_list_valid_id`: overlap check — khoảng `[date_valid_from, date_valid_to]` trùng bảng giá hiệu lực đã có ⇒ lỗi "Đã có bảng giá hiệu lực trong khoảng thời gian này".
- **`note` bắt buộc ở Update, KHÔNG bắt buộc ở Store** (giữ nguyên ERP).

- [ ] **Bước 1:** Viết FormRequest store/update (note khác nhau), Service (transaction, overlap, copy), Resource (status_text/status_color + cờ quyền fail-closed từ canEdit/canDelete/canSummaryCost), Controller, route.
- [ ] **Bước 2 (verify Review Focus #1,#2,#3,#4):** curl kịch bản:
  - store không bảng giá, ngày trùng ⇒ 422 overlap. *(RF#1)*
  - store không `note` ⇒ OK; update bỏ `note` ⇒ 422. *(RF#2)*
  - update/delete bằng account khác creator hoặc status≠3 ⇒ chặn. *(RF#3)*
  - store ma trận 2 dòng xe × 2 tải trọng × 2 tuyến ⇒ DB sinh đúng số dòng ở 3 bảng con, `vehicle_category_id`/`vehicle_payload_id`/`delivery_quotation_id` đóng đúng; update bỏ 1 dòng xe ⇒ không còn dòng con rác. *(RF#4)*
  - `code` sinh ra `BGVC-` + 5 số, không đụng dãy ERP.
- [ ] **Bước 3: Checkpoint** user review (hrm-api giữ local).

---

### Task 5: FE — danh sách + gắn menu

**Files:**
- Create: `hrm-client/pages/transport/delivery-quotations/index.vue`
- Create: `hrm-client/pages/transport/delivery-quotations/api.js` (gom gọi API màn này)
- Modify: `hrm-client/components/subsystem-menu/transport.js` (thêm `link: '/transport/delivery-quotations'` cho item sẵn có "Danh mục mẫu báo giá vận chuyển")

**Interfaces (Consumes):** `GET /api/transport/delivery-quotations` (Task 4).

- [ ] **Bước 1:** Dựng list theo skill `list-page` + khuôn `pages/finance/product-export-requests/index.vue`. Cột: STT / Mã (link sang chi tiết) / Ghi chú / **Người tạo** / **Ngày tạo** / Hành động. Search server-side theo `code`/`note`/`created_by`. Nút "Thêm" → `/transport/delivery-quotations/create`. Cột Hành động: Sửa (ẩn nếu `!is_can_edit`) / Xóa (ẩn nếu `!is_can_delete`) / Sao chép / Xuất excel / Tổng hợp giá đề xuất (ẩn nếu `!is_can_summary_cost`).
- [ ] **Bước 2:** Gắn `link` trong `transport.js`.
- [ ] **Bước 3 (verify):** Playwright: đăng nhập → menu Vận chuyển › Vận chuyển với NCC › Danh mục mẫu báo giá vận chuyển → list render, search `code` lọc đúng, nút theo cờ quyền hiện/ẩn khớp. So layout với ERP index.
- [ ] **Bước 4: Checkpoint** user review (hrm-client đẩy develop sau khi chốt).

---

### Task 6: FE — màn Thêm + component form ma trận + 2 modal

**Files:**
- Create: `hrm-client/pages/transport/delivery-quotations/create.vue`
- Create: `.../components/DeliveryQuotationForm.vue` (dùng chung Thêm/Sửa/Chi tiết qua prop `mode`)
- Create: `.../components/RoadPickerModal.vue` (chọn tuyến — bám `chooseRoad`)
- Create: `.../components/QuickAddRoadModal.vue` (Thêm nhanh tuyến — điểm đầu + tỉnh → ≤800 tuyến)

**Interfaces (Consumes):** `POST /` store; lookups: price-list list + `/data`, delivery-start-points, roads search + by-province, vehicle-categories `getAll`, vehicle-payloads `getAll`.

**Mô hình ma trận (port 4 class ES6 `DeliveryContract*` của ERP):** `form.payloads` = danh sách phẳng mọi tải trọng (cột); `form.roads` = tuyến gốc (`vehicles[0].payloads[0].roads`, các dòng); `addRoad` thêm vào mọi payload; `available_vehicle_categories` loại dòng xe đã chọn ở xe khác; `available_payloads` loại tải trọng đã chọn trong cùng xe; setter `road_id` tự điền km; ô giá (cost/extra_price) **disabled/rỗng** ở màn này. `changePriceListValid(id)` GET `/data` điền `date_valid_from/to` + `km_actual` (date disabled khi đã chọn bảng giá), KHÔNG prefill ma trận. `addQuickRoad()` GET by-province (≤800).

- [ ] **Bước 1:** Dựng `DeliveryQuotationForm.vue`: khối thông tin chung (ngày hiệu lực từ/đến, `price_list_valid_id` select hiện `code`, nhãn km **"Số Km tính cước vượt trội"**, textarea Ghi chú) + bảng ma trận (select dòng xe `addPayload`/`removeVehicle`, hàng tải trọng, hàng "Giá cước vượt trội" disabled, hàng tuyến với nút mở RoadPickerModal + ô km + ô giá disabled, nút "Thêm tuyến đường" + "Thêm nhanh tuyến"). Toàn bộ bằng `V2Base*`, số định dạng quốc tế, `unsavedChangesMixin`, nút trong `V2Footer` (Lưu / Hủy).
- [ ] **Bước 2:** Viết 2 modal theo skill `modal-popup`. QuickAddRoadModal dùng by-province (≤800).
- [ ] **Bước 3:** `create.vue` bọc form `mode="create"`, submit → store, toast thành công, điều hướng về list. Nút **"Tổng hợp giá đề xuất"** (nếu hiện ở đây) → toast "Chức năng đang phát triển".
- [ ] **Bước 4 (verify Review Focus #5):** Playwright gõ phím thật: tạo phiếu 2 dòng xe × 2 tải trọng × 2 tuyến (có dùng "Thêm nhanh tuyến" ra nhiều tuyến ⇒ không treo, ≤800), Lưu ⇒ thành công, DB sinh đúng cây; chọn bảng giá hiệu lực ⇒ ngày + km tự điền và ngày bị khóa. So với ERP form.
- [ ] **Bước 5: Checkpoint** user review.

---

### Task 7: FE — màn Sửa

**Files:**
- Create: `hrm-client/pages/transport/delivery-quotations/_id/edit.vue`

**Interfaces (Consumes):** `GET /{id}` show, `PUT /{id}` update; tái dùng `DeliveryQuotationForm.vue` (`mode="edit"`).

- [ ] **Bước 1:** `_id/edit.vue` load show → đổ vào form, submit → update. Bắt buộc **Ghi chú** (RF#2). Chỉ vào được khi `is_can_edit` (status 3 + creator) — nếu không, chặn/điều hướng + toast.
- [ ] **Bước 2 (verify RF#2,#3):** Playwright: sửa phiếu status 3 của mình ⇒ OK; bỏ trống Ghi chú ⇒ báo lỗi; mở sửa phiếu không đủ điều kiện ⇒ bị chặn. So ERP.
- [ ] **Bước 3: Checkpoint** user review.

---

### Task 8: FE — màn Chi tiết + chức năng cột Hành động

**Files:**
- Create: `hrm-client/pages/transport/delivery-quotations/_id/index.vue`

**Interfaces (Consumes):** `GET /{id}` show; `DELETE /{id}`; `POST /{id}/copy`; export excel (Task 9).

- [ ] **Bước 1:** `_id/index.vue` hiển thị **read-only** thông tin chung + ma trận (dùng `DeliveryQuotationForm.vue` `mode="detail"` hoặc view riêng). Badge trạng thái qua `V2BaseBadge`. Nút (ẩn theo cờ quyền): **Sửa** → edit; **Xóa** → confirm → delete → về list; **Sao chép** → copy → mở create prefilled; **Xuất excel** (Task 9); **Tổng hợp giá đề xuất** → toast "Chức năng đang phát triển".
- [ ] **Bước 2 (verify RF#3):** Playwright: mở chi tiết, kiểm nút hiện/ẩn theo quyền; Xóa phiếu của mình (status 3) ⇒ biến mất khỏi list; Sao chép ⇒ ra phiếu mới mã mới. So ERP.
- [ ] **Bước 3: Checkpoint** user review.

---

### Task 9: Xuất Excel "Mau_bao_gia_van_chuyen.xlsx"

**Files:**
- Modify/Create: BE export (theo skill `export-excel`) trong `Modules/Transport` + route `GET /{id}/export-excel`; FE `.../components/export-excel.js` + nút trigger ở list & chi tiết.

**Interfaces (Consumes):** `getExcelDataAttribute` (Task 1 — NOTE/CODE/VEHICLES/ROADS/MAX_COLS).

- [ ] **Bước 1:** Port template excel ERP (ma trận xe×tải trọng×tuyến) theo skill `export-excel`; tên file `Mau_bao_gia_van_chuyen.xlsx`.
- [ ] **Bước 2 (verify):** Playwright: bấm Xuất excel ở list và chi tiết ⇒ tải đúng file, mở ra có ma trận + mã + ghi chú khớp dữ liệu.
- [ ] **Bước 3: Checkpoint** user review.

---

## Ghi chú thực thi

- Thứ tự: Task 1→4 (BE) trước, rồi 5→9 (FE) — FE phụ thuộc interface BE. Task 2 & 3 có thể song song sau Task 1.
- Mỗi task kết thúc = **checkpoint cho user** (AI không commit). hrm-client: đẩy `develop` sau khi user chốt; hrm-api: giữ local chờ review (xác nhận lại lúc bàn giao).
- Luôn so sánh trực tiếp với màn ERP `/admin/delivery_quotations` khi verify từng phần.
