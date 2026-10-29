# Tổng hợp giá vận chuyển đề xuất (THGVC) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP "Tổng hợp giá vận chuyển đề xuất" (`DeliveryCostSummary`, mã `THGVC-`) sang HRM làm trọn: danh sách, tạo từ Báo giá vận chuyển, import báo giá từng NCC bằng Excel, đề xuất giá MIN, sửa giá cước/cost, gửi duyệt → duyệt sinh/cập nhật BGHLVC + copy NCC/file, xuất Excel, thông báo, đính kèm, quyền mới.

**Architecture:** Màn mới trong `Modules/Transport` của hrm-api (bám sát `DeliveryQuotation` + `PriceListValidDelivery` đã có), FE Nuxt ở `hrm-client/pages/transport/delivery-cost-summaries/`. Tầng HTTP mỏng (Controller V1) → Service giữ nghiệp vụ → Entities 5 bảng. Phần GHI BGHLVC (`create()`/`update()`) port vào **chính service đọc hiện có** `PriceListValidDeliveryService`. Đề xuất MIN tính client-side; khung ma trận dựng lúc IMPORT (không lúc store), bám 1:1 ERP.

**Tech Stack:** hrm-api Laravel 8 / PHP 7.4 / `nwidart/laravel-modules` / guard `api` / spatie permission / Maatwebsite Excel 3.1. hrm-client Nuxt 2.14 / Vue 2 / Node 14.21.3 / Bootstrap-Vue / vee-validate v2 / V2Base components.

**Spec:** `HRM/.plans/gop-db/tong-hop-gia-van-chuyen-de-xuat/design.md` (đã duyệt). Plan này lập luận từ design đó — executor đọc cả hai.

**Nguồn ERP để port (1:1 trừ chỗ design ghi lệch):**
- `ERP/TanPhatDev/app/Http/Controllers/Common/DeliveryCostSummaryController.php` (16 action, 708 dòng)
- `ERP/TanPhatDev/app/Model/Common/DeliveryCostSummary.php` (quan hệ, `searchByFilter`, `generateCode`, `canView/canApprove/canEdit/canDelete/canCreateContract`, `send()`, `approve()`, `excel_data`, `syncQuotations`)
- `ERP/TanPhatDev/app/Services/PriceListValidDelivery/PriceListValidDeliveryService.php` (`create()`, `update()`)
- ERP `QuotationImport` (import ma trận NCC) + `DeliveryCostSummaryExcel` (export)
- `ERP/TanPhatDev/routes/web.php` dòng 5715–5733 (block route THGVC)

**Anh em HRM để bám chữ ký (mirror, KHÔNG phát minh kiểu mới):**
- Controller/Service/Entities/Resources/Requests/Routes: `Modules/Transport/.../PriceListValidDelivery/*` và `Modules/Transport/.../DeliveryQuotation/*`
- FE: `hrm-client/pages/transport/valid-delivery-prices/*` + `hrm-client/pages/transport/delivery-quotations/*`
- Menu: `hrm-client/components/subsystem-menu/transport.js`

## Verification approach (đọc trước Task 1)

Repo này **không có** bộ test tự động cho màn port (BE không PHPUnit per-screen, FE không unit test). Cách chứng minh đã-xong theo đúng tiền lệ port BGHLVC:
- **BE / dữ liệu**: `php artisan tinker` read-back trên DB `erp_hrm_check` (nhánh `develop`). Mỗi task BE có 1 đoạn tinker ngắn (để ở scratchpad, KHÔNG commit) đóng vai "test": chạy **trước** khi implement để thấy nó fail/thiếu, chạy **sau** để thấy đúng.
- **FE**: Playwright MCP mở `http://127.0.0.1:3000` (KHÔNG `localhost`), kịch bản thao tác thật, đọc network request + snapshot. Cần API `:8000` + Nuxt `:3000` (skill `run-hrm`).
- **Smoke tĩnh mọi task BE**: `php -l <file>` + `php artisan route:list --path=delivery_cost_summaries` (khi đã có route).

Giữ *hình dạng* TDD (viết cái kiểm sẽ fail → làm cho pass) nhưng "cái kiểm" là lệnh thật ở trên, không phải PHPUnit giả.

## Global Constraints

Mọi task ngầm bao gồm mục này (giá trị copy verbatim từ design.md §3 + CLAUDE.md HRM):

- **Nhánh**: `develop` (họ gop_db), DB gộp `erp_hrm_check`. hrm-api giữ **local**. **KHÔNG** commit/push trừ khi user yêu cầu trực tiếp.
- **DB gộp**: 5 bảng `delivery_cost_summary*` GHI THẲNG bảng sẵn có, **KHÔNG tạo bảng mới trùng**; thiếu cột thì thêm. Không tạo migration quyền.
- **Quyền**: guard `api`, khai qua `permission-seeder` (`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `$this->perm([...])`, KHÔNG `id`/`guard_name`), `type` = phân hệ Vận chuyển (BGHLVC dùng **22**). **KHÔNG** dùng lại quyền ERP guard `web`. BE re-check endpoint nhạy cảm bằng `isCurrentEmployeeHasPermission('<Tên quyền>')`. Cờ quyền FE init `false` (fail-closed) — **CẤM** `can… = true`.
- **Model**: entity THGVC `extends BaseModel` (`App\Models\BaseModel`) để tự gán `created_by`/`updated_by`. Entity `PriceListValidDelivery*` hiện `extends Model` → mọi đường GHI **set tay** `created_by`/`updated_by = auth()->id()` (= `employees.id`, KHÔNG `auth()->user()->info->id`).
- **FormRequest**: chỉ `rules()`, **KHÔNG** `messages()` cho rule chung. BE rethrow `ValidationException` (không catch `Exception`).
- **Khóa/trạng thái**: chặn sửa/xóa ở **BE** (423 hoặc 422 theo guard trạng thái), không chỉ ẩn nút FE.
- **FE màn mới**: chỉ `V2Base*` (CẤM HTML form thô — tự kiểm `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/transport/delivery-cost-summaries/ | grep -v V2Base` phải RỖNG). Select trong modal → `V2BaseSelectInModal`. Popup → `V2BaseModal`; confirm → `$confirm`/`base-confirm-modal`. Nút nhóm `mr-2 mb-2` (cuối `mb-2`). Nút không dùng được → **ẩn** (`v-if`), không disable. Bảng tràn → `V2BaseTableScroll`. Nút footer chi tiết/form → `V2Footer` (+ `#custom-actions`). Khối nhóm → `V2BaseFormCard` (nhóm kho/xuất nhập) hoặc `V2BaseFormSection`. File đính kèm → `V2BaseFile`.
- **Màu/chữ**: `.text-muted` đỏ → dùng `#6b7280`; đỏ chỉ cho lỗi validate. Badge → `V2BaseBadge` màu/chữ do BE trả (`status_text` + `status_color`).
- **Số quốc tế** `1,234,567.89`: FE `toLocaleString('en-US')` (**CẤM** `'vi-VN'` cho số); BE `number_format` mặc định (**CẤM** `number_format($x,0,',','.')`). Ngày `dd/mm/yyyy`. Excel: ô số = **số thô + `data-format`** (skill `export-excel`).
- **Select nhân viên**: khuôn `Tên - Mã phòng - Mã NV` (`utils/employeeOptionText.js` / `employeeOptionLabel()`), API trả kèm `department_code`.
- **Danh mục khóa**: giá trị đang dùng vẫn phải hiện (merge option + `is_locked` → `🔒` tự động).
- **Sau thao tác** (Lưu nháp/Lưu/Gửi duyệt/Duyệt/Không duyệt/Xóa): `markFormSaved()` → `$router.push` **màn danh sách**. Tiêu đề chi tiết `Chi tiết tổng hợp giá vận chuyển đề xuất: <mã>`. Hành động màn chi tiết **khớp** màn danh sách (cùng điều kiện ẩn/hiện).
- **Thông báo**: template `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`, deep-link kèm ID (skill `notification-convention`) — thay cơ chế Redis của ERP.
- **Hiệu năng**: không N+1 (eager load), phân trang, ≤5 API/màn khi load, export > 2s chia `export-rows`.

## Review Focus

Năm lớp input/kịch bản mà spec hàm ý nhưng không task nào test trực diện, dễ cắn người dùng nhất (mỗi dòng đã được gắn bước kiểm vào task sở hữu):

1. **Ma trận dồn cột khi NCC thiếu ô** (design Anti-goal §73, bài học BGHLVC RF#1): NCC B thiếu một tuyến/trọng tải mà báo giá gốc có → ô phải **để trống đúng vị trí**, không trượt cột. → Task 12 (FE matrix) có bước Playwright dựng 2 NCC lệch ô, khẳng định cột không trượt.
2. **MIN tính cả số 0** (Anti-goal §73): một NCC để `cost=0` ở ô mà NCC khác có giá → đề xuất phải lấy **min các giá khác 0**; mọi NCC = 0 → 0. → Task 11 (MIN computed) có bước kiểm mảng `[0, 5, 3]`→3 và `[0,0]`→0.
3. **Duyệt tạo BGHLVC trùng khoảng thời gian/công ty** (Anti-goal §69): báo giá nguồn chưa gắn `price_list_valid_id`, đã tồn tại BGHLVC cùng công ty người duyệt phủ khoảng ngày → phải **báo lỗi, không tạo trùng**. → Task 6 (approve) có bước tinker dựng BGHLVC chồng ngày rồi duyệt, khẳng định trả lỗi.
4. **Import Excel lệch khung vẫn lưu** (Anti-goal §71): file NCC sai thứ tự xe/trọng tải/tuyến (dòng 8/9/10/11) so với báo giá gốc → phải **ném `QuotationImportException`, không ghi** dữ liệu lệch. → Task 7 (import) có bước nạp file lệch cột, khẳng định 0 dòng road ghi xuống.
5. **Duyệt lấy nhầm giá NCC thay vì giá duyệt** (Anti-goal §69): cost/extra_price ghi vào BGHLVC phải là `approve_cost`/`approve_extra_price` gửi lúc duyệt, KHÔNG phải `cost`/`extra_price` của NCC. → Task 4 (write service) có bước tinker so giá BGHLVC == payload approve_*, khác với giá NCC gốc.

---

## Task 1: Xác nhận 5 bảng THGVC trong DB gộp (KHÔNG migration)

**Files:**
- Không tạo/sửa file sản phẩm. Script kiểm để ở scratchpad.

**Interfaces:**
- Produces: xác nhận tên cột thật của 5 bảng cho các task sau dùng đúng (đặc biệt `delivery_cost_summary_quotation_vehicle_payloads.extra_price` + `.approve_extra_price` nullable; `..._payload_roads.cost` + `.approve_cost` nullable, `road_id`, `vehicle_category_id`, `vehicle_payload_id`, `km`).

- [ ] **Step 1: Viết đoạn kiểm (phải "fail" nếu thiếu bảng/cột)**

`php artisan tinker` (hrm-api), kiểm 5 bảng + cột khóa:
```php
collect(['delivery_cost_summaries','delivery_cost_summary_quotations','delivery_cost_summary_quotation_vehicles','delivery_cost_summary_quotation_vehicle_payloads','delivery_cost_summary_quotation_vehicle_payload_roads'])
  ->mapWithKeys(fn($t) => [$t => \Schema::hasTable($t) ? \Schema::getColumnListing($t) : 'MISSING']);
```

- [ ] **Step 2: Chạy và đọc kết quả**

Expected: cả 5 bảng có cột (không `MISSING`). `..._payloads` có `extra_price`, `approve_extra_price`; `..._payload_roads` có `cost`, `approve_cost`, `road_id`, `vehicle_category_id`, `vehicle_payload_id`, `km`. `delivery_cost_summaries` có `delivery_quotation_id`, `code`, `status`, `approver_id`, `approver_comment`, `approved_time`, `send_time`, `created_by`.

- [ ] **Step 3 (chỉ khi thiếu cột, không thiếu bảng): thêm migration cột còn thiếu**

Chỉ `ALTER` thêm cột thiếu (vd `approve_*` nullable). **KHÔNG** `CREATE TABLE`. Nếu đủ hết → bỏ qua, ghi ledger "5 bảng đủ, không migration".

- [ ] **Step 4: Ghi lại kết luận**

Ledger: bảng/cột đã xác nhận; ánh xạ tên cột cho Task 2.

---

## Task 2: 5 Entities THGVC

**Files:**
- Create: `Modules/Transport/Entities/DeliveryCostSummary/DeliveryCostSummary.php`
- Create: `.../DeliveryCostSummary/DeliveryCostSummaryQuotation.php`
- Create: `.../DeliveryCostSummary/DeliveryCostSummaryQuotationVehicle.php`
- Create: `.../DeliveryCostSummary/DeliveryCostSummaryQuotationVehiclePayload.php`
- Create: `.../DeliveryCostSummary/DeliveryCostSummaryQuotationVehiclePayloadRoad.php`

**Interfaces:**
- Consumes: tên cột từ Task 1; `DeliveryQuotation` entity (HRM) cho quan hệ `base_quotation`.
- Produces:
  - `DeliveryCostSummary` (extends `BaseModel`): `$table='delivery_cost_summaries'`, `$fillable` gồm `delivery_quotation_id,code,status,approver_id,approver_comment,approved_time,send_time,created_by,updated_by`; quan hệ `base_quotation()` → `belongsTo(DeliveryQuotation, 'delivery_quotation_id')`, `quotations()` → `hasMany(DeliveryCostSummaryQuotation, 'parent_id')`, `approver()`, `employee_create()`; `files()` → `hasMany(File::class,'table_id','id')->where('table','delivery_cost_summaries')`; hằng trạng thái `DA_DUYET=1, CHO_DUYET=2, DANG_TAO=3, DA_LAP_HD=4, DANG_LAP_HD=5`.
  - `generateCode(): void` → `code = 'THGVC-'.generateCode(5,$id); save();` (bám model ERP dòng 303). Dùng helper `generateCode()` global như BGVC/BGHLVC.
  - 4 entity con `extends BaseModel`, quan hệ xuống theo cây design §157–165. Khóa ngoại: `..._quotations.parent_id`, `..._vehicles.delivery_cost_summary_quotation_id` (xác nhận tên FK thật ở Task 1), payloads/roads tương tự.

- [ ] **Step 1: Viết đoạn kiểm quan hệ (fail trước khi có entity)**

tinker: `\Modules\Transport\Entities\DeliveryCostSummary\DeliveryCostSummary::with('base_quotation','quotations.vehicles.payloads.roads','files')->first();`

- [ ] **Step 2: Chạy — Expected FAIL** "Class not found".

- [ ] **Step 3: Tạo 5 entity** theo Produces. Mirror namespace/khai báo của `Modules/Transport/Entities/DeliveryQuotation/*`. Set `$fillable` có `created_by,updated_by` (yêu cầu BaseModel).

- [ ] **Step 4: `php -l` 5 file + chạy lại Step 1** — Expected: trả model, eager-load không lỗi quan hệ (có thể trả rỗng nếu chưa có data).

- [ ] **Step 5: Ghi ledger** tên FK thật đã dùng.

---

## Task 3: Khai 4 quyền mới (seeder đồng bộ, guard api)

**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

**Interfaces:**
- Produces 4 tên quyền (dùng xuyên Task 4/6/9/11/16/17):
  - `Duyệt giá vận chuyển`
  - `Xem tổng hợp giá vận chuyển đề xuất theo tổng công ty`
  - `Xem tổng hợp giá vận chuyển đề xuất theo công ty`
  - `Xem tổng hợp giá vận chuyển đề xuất theo phòng ban`

- [ ] **Step 1: Chạy dry-run trước khi thêm** — `php artisan permission:sync --dry-run` (ghi lại trạng thái nền).

- [ ] **Step 2: Thêm 4 dòng `$this->perm([...])`** cạnh nhóm quyền Vận chuyển (gần quyền BGHLVC). Mỗi dòng: `['name'=>…, 'display_name'=>…, 'group'=>'<nhóm Vận chuyển như BGHLVC>', 'type'=>22]`. **KHÔNG** `id`/`guard_name`. (Nếu tên đã tồn tại trong DB do lần khác → sync tự giữ id; nếu trùng tên trong file → sửa.)

- [ ] **Step 3: `permission:sync --dry-run`** — Expected: "thêm 4" (hoặc "giữ id cũ" nếu đã có), 0 lỗi khai báo.

- [ ] **Step 4: `permission:sync`** ghi DB local. Expected: 4 quyền có mặt, query `Permission::where('guard_name','api')->whereIn('name',[...])->count()` = 4.

- [ ] **Step 5: Ghi ledger** id thật 4 quyền.

---

## Task 4: Phần GHI BGHLVC — `create()` + `update()` vào service đọc hiện có

**Files:**
- Modify: `Modules/Transport/Services/PriceListValidDelivery/PriceListValidDeliveryService.php` (thêm 2 method, giữ nguyên phần đọc)
- Modify (nếu cần cho ghi): `Modules/Finance/Entities/Delivery/PriceListValidDelivery.php` + 3 entity con `*Vehicle` / `*VehiclePayload` / `*VehiclePayloadRoad` — thêm `$fillable` cột cần ghi (các entity này `extends Model`, KHÔNG BaseModel).

**Interfaces:**
- Consumes: `DeliveryCostSummary` + con (Task 2); `$data` = `$request->all()` của approve (Task 6) chứa `vehicles[].payloads[].approve_extra_price` và `.roads[].approve_cost`.
- Produces:
  - `create(DeliveryCostSummary $object, array $data): PriceListValidDelivery` — port ERP service `create()` (dòng 1–~120). Dựng BGHLVC mới: `code=randomString(5)`→`generateCode()`; `company_id = auth()->user()->info->company_id`; `date_valid_from/to`, `km_actual` lấy từ `$object->base_quotation`; distinct `vehicle_category_id` từ `DeliveryCostSummaryQuotationVehicle` của summary; payload `extra_price = $data['vehicles'][$i]['payloads'][$j]['approve_extra_price']`; road `cost = $data[...]['roads'][$k]['approve_cost']`, `km` từ summary road. Set tay `created_by=updated_by=auth()->id()` ở mọi dòng ghi.
  - `update(PriceListValidDelivery $priceListValid, DeliveryCostSummary $object, array $data): PriceListValidDelivery` — port ERP service `update()` (merge xe/trọng tải/tuyến mới từ summary; xóa road trùng rồi chèn lại theo `approve_cost`; thêm base road `cost=0` cho payload mới; đảm bảo mọi payload có đủ base road). `DB::table(...)->insert` kèm `created_by/updated_by=auth()->id()`. `ini_set('max_execution_time',900)`.
- **RF#5**: giá ghi vào BGHLVC là `approve_*`, KHÔNG phải giá NCC.

- [ ] **Step 1: Viết đoạn kiểm (fail trước khi có method)** — tinker: dựng/ lấy 1 `DeliveryCostSummary` đã có quotations+vehicles, gọi `app(PriceListValidDeliveryService::class)->create($summary, $fakeApproveData)` với `$fakeApproveData` có `approve_cost` **khác** `cost` NCC, rồi đọc lại road BGHLVC vừa tạo.

- [ ] **Step 2: Chạy — Expected FAIL** "method create() not defined".

- [ ] **Step 3: Thêm `create()`** theo Produces (port ERP `PriceListValidDeliveryService::create`). Thêm `$fillable` entity BGHLVC nếu insert qua model.

- [ ] **Step 4: Chạy lại — Expected PASS**: BGHLVC mới có `company_id` = người tạo test; road `cost` == `approve_cost` của payload (RF#5), **khác** `cost` NCC gốc; `created_by` = `auth()->id()`.

- [ ] **Step 5: Thêm `update()`** theo Produces (port ERP `PriceListValidDeliveryService::update`). tinker: gọi `update()` trên BGHLVC vừa tạo với summary bổ sung 1 tuyến mới → đọc lại thấy tuyến mới có, tuyến cũ cost cập nhật theo approve mới, `updated_by` set.

- [ ] **Step 6: `php -l` + ghi ledger** (xác nhận giữ nguyên phần đọc service; `git diff` chỉ thêm 2 method + fillable).

---

## Task 5: `DeliveryCostSummaryService` — truy vấn & điều phối

**Files:**
- Create: `Modules/Transport/Services/DeliveryCostSummary/DeliveryCostSummaryService.php`

**Interfaces:**
- Consumes: entities Task 2; `PriceListValidDeliveryService` (Task 4); tên quyền Task 3.
- Produces (chữ ký cho Controller Task 9 gọi):
  - `searchByFilter(Request $request): Builder` — port ERP model `searchByFilter`: lọc theo `code`, `status`, `created_by` (người tạo), `approver_id` (người duyệt), `supplier_id` (NCC — join quotations), `company_id`. **Phạm vi quyền** bám `canView`/ERP: Super Admin → tất cả; else OR theo `created_by==me` / `approver_id==me` / 3 quyền "Xem..." (tổng cty / cty `Company::getMembers` / phòng `Department::getMembers`) với `status!=3`, + nhánh tab Duyệt (`status==2 && can('Duyệt giá vận chuyển') && cùng công ty`). Eager load `base_quotation`, `approver`, `employee_create`.
  - `getDetail(int $id): DeliveryCostSummary` — load phiếu + `quotations.vehicles.payloads.roads` + `files` + base_quotation (khung HEADER). Dùng cho show/edit/export.
  - `store(array $data): DeliveryCostSummary` — port ERP `store()`: tạo phiếu `code=randomString(5)`→`generateCode()`, set `status` (2|3), nguồn `base_quotation->status=1`; lưu file `files` (table/table_id) từ payload; status==2 → `sendApprovalNotification()`. **Khung xe/trọng tải/tuyến KHÔNG dựng ở đây** (design §122). set `created_by` (BaseModel tự lo).
  - `update(DeliveryCostSummary $object, array $data): DeliveryCostSummary` — port ERP `update()`: cascade xóa `quotation_deleted_ids` (roads→payloads→vehicles→quotation); status==2 set `send_time=now()`; cập nhật file; status==2 → notification.
  - `approve(DeliveryCostSummary $object, array $data): void` — port ERP model `approve()` + controller nhánh BGHLVC, **trong 1 transaction**:
    1. set `approver_id=auth()->id()`, `approved_time=now()`, `approver_comment`, `status`(1|3); save.
    2. status==1: với mỗi quotation ghi `approve_extra_price`/`approve_cost` vào detail (từ `$data['vehicles'][$iv]['payloads'][$ip]...`) + set quotation `status=1`.
    3. status==1: nếu `base_quotation->price_list_valid_id` → `priceService->update($existing,$object,$data)`; else overlap-check theo `company_id=auth()->user()->info->company_id` (`date_valid_from<=to && date_valid_to>=from`) → có thì **ném lỗi** (RF#3), không thì `priceService->create($object,$data)`; rồi **copy** mỗi quotation → `PriceListValidDeliveryQuotation` (price_list_valid_delivery_id, supplier_id) + copy file đính kèm NCC (bảng `files`).
    4. notification duyệt/không-duyệt tới `created_by`.
  - `updateExtraPrice(DeliveryCostSummary $object, array $extraPrices): void` — port ERP: cập nhật `DeliveryCostSummaryQuotationVehiclePayload.extra_price` theo `parent_id + vehicle_payload_id`. Guard canEdit ở Controller/Request.
  - `updatePayLoadRoads(DeliveryCostSummary $object, array $payloadRoads): void` — cập nhật `...PayloadRoad.cost` theo `parent_id + road_id`.
  - `quotationImport(DeliveryCostSummary $object, int $supplierId, UploadedFile $file): void` — find/create `DeliveryCostSummaryQuotation(parent_id,supplier_id,status=2)`; nếu mới → dựng khung từ `base_quotation->vehicles` (payload `extra_price=0`); nếu cũ → xóa road của payload; `$base_roads` = Road join `delivery_quotation_vehicle_payload_roads` where `delivery_quotation_id=base->id` pluck(id,name); `Excel::import(new QuotationImport($object->id,$quotation,$base_roads),$file)` (Task 7); cập nhật file NCC (bảng `files`). `QuotationImportException` → ném lên để Controller trả `responseErrors`.
  - `getExcelData(DeliveryCostSummary $object): array` — port ERP accessor `excel_data`/`getExcelDataAttribute`: dựng cấu trúc ma trận cho export (Task 8).
  - `sendApprovalNotification()` / notification helpers theo `notification-convention` (prefix Vận chuyển, nhóm hành động, deep-link `/transport/delivery-cost-summaries/<id>`).

- [ ] **Step 1: Viết đoạn kiểm `searchByFilter` (fail trước khi có)** — tinker: `app(DeliveryCostSummaryService::class)->searchByFilter(new Request(['code'=>'THGVC']))->toSql();`

- [ ] **Step 2: Expected FAIL** "Class not found".

- [ ] **Step 3: Tạo service + `searchByFilter` + `getDetail` + `store` + `update`.** Mirror cấu trúc `PriceListValidDeliveryService` (DI, namespace). Notification tách helper riêng.

- [ ] **Step 4: Kiểm `searchByFilter`** — tinker chạy với vài filter, đọc SQL thấy `where code like`, `supplier_id` join quotations, phạm vi quyền áp đúng (test với user có/không quyền).

- [ ] **Step 5: Thêm `approve` + `updateExtraPrice` + `updatePayLoadRoads` + `quotationImport` + `getExcelData` + notification.** (Phần BGHLVC gọi Task 4; import gọi Task 7.)

- [ ] **Step 6: Kiểm `approve` nhánh create (RF#3 + RF#5)** — tinker: (a) summary chưa gắn price_list_valid_id, không trùng ngày → `approve(status=1)` tạo BGHLVC + copy quotations sang `PriceListValidDeliveryQuotation` + quotation.status=1; (b) dựng BGHLVC chồng ngày cùng công ty → `approve` ném lỗi, **không** tạo thêm. Đọc lại DB xác nhận.

- [ ] **Step 7: `php -l` + ghi ledger** (rulings nếu tên cột/FK lệch ERP).

---

## Task 6: FormRequests

**Files:**
- Create: `Modules/Transport/Http/Requests/DeliveryCostSummary/StoreRequest.php`
- Create: `.../DeliveryCostSummary/UpdateRequest.php`
- Create: `.../DeliveryCostSummary/ApproveRequest.php`
- Create: `.../DeliveryCostSummary/QuotationImportRequest.php`

**Interfaces:**
- Consumes: quyền Task 3; entity Task 2 (route-model-binding cho `authorize`).
- Produces (chỉ `rules()` + `authorize()`, **không** `messages()`):
  - `StoreRequest`: `delivery_quotation_id` required|exists:delivery_quotations,id; `status` required|in:2,3; `note` nullable; `files`/`attachments` nullable (mimes pdf theo V2BaseFile). `authorize()`: đăng nhập (tạo mới không gate quyền riêng — như ERP).
  - `UpdateRequest`: `status` required|in:2,3; `quotation_deleted_ids` nullable|array + `.*` exists; `quotation_datas` required|array|min:1 khi `status==2` (`required_if`). `authorize()`: `canEdit` (created_by==me && status==3) — fail-closed.
  - `ApproveRequest`: `approver_comment` required; `status` required|in:1,3; `vehicles` required_if:status,1|nullable|array|min:1; `vehicles.*.payloads` same; `vehicles.*.payloads.*.approve_extra_price` required_if:status,1|nullable|numeric|min:0|max:999999999; `...roads` + `...roads.*.approve_cost` same. `authorize()`: `canApprove` = `isCurrentEmployeeHasPermission('Duyệt giá vận chuyển') && status==2` (Hướng A design §183 — KHÔNG chặn công ty).
  - `QuotationImportRequest`: `supplier_id` required|exists:customers,id; `file` required|file|mimes:xlsx,xls. `authorize()`: `canEdit`.

- [ ] **Step 1: Viết đoạn kiểm authorize (fail đúng kỳ vọng)** — gọi endpoint approve (sau Task 9) với user không quyền → 403; thiếu `approver_comment` → 422. (Ở task này kiểm bằng `php -l` + đọc rules; kiểm runtime ở Task 9.)

- [ ] **Step 2: Tạo 4 request** theo Produces. Mirror `Modules/Transport/Http/Requests/PriceListValidDelivery/ExtendDateRequest.php`. `authorize()` gọi entity `can*()` method (thêm vào entity Task 2 nếu chưa có: `canEdit/canApprove` mirror ERP model).

- [ ] **Step 3: `php -l` 4 file** — Expected PASS.

- [ ] **Step 4: Ghi ledger.**

---

## Task 7: `QuotationImport` (đọc Excel báo giá NCC)

**Files:**
- Create: `Modules/Transport/Excel/Imports/QuotationImport.php` (hoặc thư mục import hiện hành của Transport — bám vị trí import module)
- Create: `Modules/Transport/Exceptions/QuotationImportException.php` (nếu chưa có tương đương)

**Interfaces:**
- Consumes: `__construct(int $summaryId, DeliveryCostSummaryQuotation $quotation, array $baseRoads)`; khung từ `base_quotation`.
- Produces: `QuotationImport implements ToCollection` (Maatwebsite). Hợp đồng vị trí ô (bám ERP + design §128): **dòng 8** = thứ tự loại xe (khớp `base_quotation` vehicles), **dòng 9** = trọng tải, **dòng 10** = `extra_price` theo cột, **dòng 11+** = tuyến (tên tuyến cột đầu, cost từng ô). Khớp đúng thứ tự xe→trọng tải→tuyến của báo giá gốc; lệch → `throw QuotationImportException(msg, errors)`. Ghi `extra_price` vào payload + `cost`+`km`+`road_id`+`vehicle_category_id`+`vehicle_payload_id` vào road.
- **RF#4**: lệch khung → ném, **không ghi** dòng nào.

- [ ] **Step 1: Chuẩn bị 2 file test** (scratchpad): (a) file khớp khung base_quotation; (b) file lệch (đổi thứ tự trọng tải dòng 9). Viết đoạn kiểm: `Excel::import(new QuotationImport(...), $fileLech)` phải ném + roads count không đổi.

- [ ] **Step 2: Chạy — Expected FAIL** "Class not found".

- [ ] **Step 3: Tạo `QuotationImport` + exception** theo Produces. Theo skill `import-excel` (dung sai ngày/số kiểu VN cho file user). Validate từng mốc dòng, gom `errors` trước khi ghi; ghi trong transaction nội bộ hoặc chỉ ghi khi validate toàn bộ pass.

- [ ] **Step 4: Chạy lại** — Expected: file (a) ghi đủ payload/road, `extra_price`/`cost` đúng ô; file (b) ném `QuotationImportException`, **0** road ghi xuống (RF#4).

- [ ] **Step 5: `php -l` + ghi ledger** (số dòng mốc thật nếu lệch ERP).

---

## Task 8: `DeliveryCostSummaryExcel` (export ma trận)

**Files:**
- Create: `Modules/Transport/Excel/Exports/DeliveryCostSummaryExcel.php`
- Create: blade view ma trận (nếu dùng `FromView`) tại `Modules/Transport/Resources/views/exports/delivery_cost_summary.blade.php`

**Interfaces:**
- Consumes: `getExcelData()` (Task 5).
- Produces: `DeliveryCostSummaryExcel` với `forData(array $data): self` + `download($filename)`; tên file `Tổng hợp giá vận chuyển đề xuất số <code>.xlsx`. Theo skill `export-excel`: ô số = **số thô + `data-format="#,##0"`**, letterhead qua `WithDrawings` + trait `EmbedsCompanyLetterhead` theo `company_id` trên chứng từ (base_quotation/summary company), cột width `WithColumnWidths`. Ma trận: dòng "Giá cước vượt trội" + dòng tuyến × cột (loại xe × trọng tải) theo khung gốc; mỗi NCC một khối/sheet (bám ERP export).

- [ ] **Step 1: Viết đoạn kiểm (fail trước)** — tinker: `(new DeliveryCostSummaryExcel)->forData($svc->getExcelData($summary))->download(...)` ghi ra file tạm; rồi đọc lại bằng PhpSpreadsheet (script skill `export-excel` mục 7) kiểm ô số là kiểu `n`, không `s`.

- [ ] **Step 2: Expected FAIL** "Class not found".

- [ ] **Step 3: Tạo export + blade** theo Produces.

- [ ] **Step 4: Chạy lại + đọc file** — Expected: ô tiền kiểu số (`n`) + `fmt=#,##0`, letterhead drawing ≥1 (nếu `companies.header` có), width cột đặt.

- [ ] **Step 5: Ghi ledger.**

---

## Task 9: Controller V1 + Routes + Transformers

**Files:**
- Create: `Modules/Transport/Http/Controllers/V1/DeliveryCostSummary/DeliveryCostSummaryController.php`
- Create: `Modules/Transport/Transformers/DeliveryCostSummary/DeliveryCostSummaryListResource.php`
- Create: `.../DeliveryCostSummary/DeliveryCostSummaryDetailResource.php`
- Modify: `Modules/Transport/Routes/api.php` (thêm block route, **static trước `/{id}`**)

**Interfaces:**
- Consumes: `DeliveryCostSummaryService` (Task 5), 4 Request (Task 6), export (Task 8), quyền (Task 3).
- Produces (mirror `PriceListValidDeliveryController` — extends `ApiController`, DI service, trả ListResource `->additional([total,lastPage,currentPage,perPage])`, Detail = Resource, thao tác trả `$this->responseJson('...',200,[...])` / `responseErrors`):
  - `index(Request)` → paginate `searchByFilter`.
  - `show($id)` → `DeliveryCostSummaryDetailResource(getDetail)` (gồm khung HEADER + tabs NCC + files + cờ `is_can_edit/is_can_delete/is_can_approve/is_can_create_contract` + `status_text/status_color`).
  - `store(StoreRequest)` → `service->store`.
  - `update($id, UpdateRequest)` → guard 423/trạng thái ở service/entity → `service->update`.
  - `approve($id, ApproveRequest)` → `service->approve`.
  - `updateExtraPrice($id, Request)` / `updatePayLoadRoads($id, Request)` → service tương ứng (guard canEdit).
  - `quotationImport($id, QuotationImportRequest)` → `service->quotationImport`; `QuotationImportException` → `responseErrors($msg,$errors)`.
  - `checkQuotationImport($id, Request)` → kiểm điều kiện import (bám ERP) nếu cần.
  - `deleteFile($id, Request)` → xóa bản ghi bảng `files` (table/table_id) — **KHÔNG** CSV.
  - `destroy($id)` → guard canDelete → cascade xóa (service).
  - `exportExcel($id)` → `DeliveryCostSummaryExcel`.
  - `forApprover(Request)` → danh sách tab Duyệt (nếu FE cần tách) — hoặc gộp vào `index` qua filter `status=2`.
- Routes prefix `delivery_cost_summaries`, middleware `checkPermission:` cho approve (`Duyệt giá vận chuyển`); index/show gate bằng 3 quyền "Xem..." (hoặc để service lọc phạm vi). **Static route** (`export-rows`, `forApprover`, `checkQuotationImport`) khai **trước** `/{id}`.

- [ ] **Step 1: Viết đoạn kiểm route (fail trước)** — `php artisan route:list --path=delivery_cost_summaries` → rỗng.

- [ ] **Step 2: Tạo Controller + 2 Resource + routes.** Mirror `PriceListValidDeliveryController` + routes BGHLVC. Resource trả `status_color` (9 mã chuẩn: Đã duyệt `#16A34A`, Chờ duyệt `#D97706`, Đang tạo `#64748B`, …) + cờ `is_can_*` fail-closed.

- [ ] **Step 3: `route:list --path=delivery_cost_summaries`** — Expected: liệt kê index/show/store/update/approve/updateExtraPrice/updatePayLoadRoads/quotationImport/exportExcel/deleteFile/destroy; static trước `{id}`.

- [ ] **Step 4: Smoke runtime** — gọi `GET /api/.../delivery_cost_summaries` (curl/Playwright network) với token hợp lệ → 200 + cấu trúc `{data, total, lastPage,...}`; gọi approve thiếu `approver_comment` → 422; user không quyền duyệt → 403 (kiểm RF#3 authorize).

- [ ] **Step 5: `php -l` + ghi ledger.**

---

## Task 10: FE — API module + trang Danh sách

**Files:**
- Create: `hrm-client/pages/transport/delivery-cost-summaries/api.js`
- Create: `hrm-client/pages/transport/delivery-cost-summaries/index.vue`
- Create (nếu tách): `hrm-client/pages/transport/delivery-cost-summaries/columns.js`

**Interfaces:**
- Consumes: endpoints Task 9.
- Produces: `api.js` export `getList`, `getDetail`, `store`, `update`, `approve`, `updateExtraPrice`, `updatePayLoadRoads`, `quotationImport`, `exportExcel`, `deleteFile`, `destroy` (mirror `pages/transport/valid-delivery-prices/api.js`). `index.vue` dùng `V2BaseDataTable` + bộ lọc (code, trạng thái, người tạo, người duyệt, NCC, công ty) — placeholder đúng trường; cột Hành động: Sửa/Xóa/Nhập báo giá NCC/Xuất Excel ẩn-hiện theo cờ BE (`is_can_*`); badge `V2BaseBadge :color`.

- [ ] **Step 1: Playwright (fail trước)** — mở `http://127.0.0.1:3000/transport/delivery-cost-summaries` → 404/trống.

- [ ] **Step 2: Tạo api.js + index.vue.** Mirror `valid-delivery-prices/index.vue`. Cờ quyền init `false`, đọc từ `$store.state.permissions` + field BE.

- [ ] **Step 3: Playwright** — mở màn, thấy bảng + bộ lọc; lọc theo trạng thái gọi API đúng (đọc network); nút Hành động khớp cờ. Tự kiểm grep V2Base RỖNG.

- [ ] **Step 4: Ghi ledger.**

---

## Task 11: FE — MIN proposal util + trang Tạo/Chi tiết (ma trận)

**Files:**
- Create: `hrm-client/pages/transport/delivery-cost-summaries/_id/index.vue` (chi tiết/sửa) + `create.vue` (tạo từ `?delivery_quotation_id=`)
- Create: `hrm-client/pages/transport/delivery-cost-summaries/utils/minCost.js`
- Create: component ma trận dùng chung `components/.../CostMatrix.vue` (nếu tách)

**Interfaces:**
- Consumes: `getDetail`; base_quotation khung HEADER; tabs NCC.
- Produces:
  - `minCost.js`: `minNonZero(values: number[]): number` — bỏ 0, `Math.min` các giá >0; mọi phần tử 0 → 0. `getMinExtraPrice(suppliers, colKey)` / `getMinCost(suppliers, roadKey, colKey)`.
  - Trang tạo: vào qua `?delivery_quotation_id=`, dựng khung từ base_quotation (tuyến × loại xe × trọng tải) — ô căn theo **khung HEADER** (vehicle_id → payload_id → road), thiếu để trống, **không dồn cột** (RF#1). Ghi chú + `V2BaseFile` đính kèm. Lưu nháp (status=3) / Gửi duyệt (status=2). Dòng "đề xuất" = `minNonZero` prefill `approve_*`.
  - Mỗi NCC một tab; dòng "Giá cước vượt trội" + các dòng tuyến. Bảng tràn → `V2BaseTableScroll`.

- [ ] **Step 1: Kiểm `minNonZero` (fail trước)** — unit nhỏ (node/REPL hoặc Playwright `browser_evaluate`): `minNonZero([0,5,3])` kỳ vọng 3; `minNonZero([0,0])` kỳ vọng 0 (RF#2).

- [ ] **Step 2: Viết `minCost.js`** → chạy lại Step 1 PASS.

- [ ] **Step 3: Tạo create.vue + _id/index.vue + CostMatrix.** V2Base toàn bộ.

- [ ] **Step 4: Playwright (RF#1)** — mở tạo từ 1 base_quotation; sau Task 13 import 2 NCC lệch ô → khẳng định ô thiếu để trống đúng cột, cột không trượt; đề xuất = min khác 0.

- [ ] **Step 5: Ghi ledger.**

---

## Task 12: FE — Modal Import báo giá NCC

**Files:**
- Create: `hrm-client/pages/transport/delivery-cost-summaries/components/ImportQuotationModal.vue`

**Interfaces:**
- Consumes: `quotationImport`; `V2BaseModal`; Select NCC → `V2BaseSelectInModal`; file → `V2BaseFile`.
- Produces: modal chọn NCC + file Excel → gọi `quotationImport(id, {supplier_id, file})`; lỗi lệch khung (`responseErrors`) → hiện lỗi inline (không toast cho lỗi dòng); thành công → reload tab NCC. **Không** nút tải mẫu (design §152 — bản export chính là khung).

- [ ] **Step 1: Playwright (fail trước)** — mở chi tiết, không có nút/modal import.

- [ ] **Step 2: Tạo modal.** Mirror khuôn `modal-popup` + `V2BaseModal`.

- [ ] **Step 3: Playwright** — import file khớp → tab NCC mới hiện giá đúng ô; import file lệch → báo lỗi, không thêm tab/dữ liệu.

- [ ] **Step 4: Ghi ledger.**

---

## Task 13: FE — 2 modal sửa giá (Giá cước vượt trội + Cost tuyến)

**Files:**
- Create: `.../components/EditExtraPriceModal.vue`
- Create: `.../components/EditPayloadRoadModal.vue`

**Interfaces:**
- Consumes: `updateExtraPrice` / `updatePayLoadRoads`; tiền → `V2BaseCurrencyInput`.
- Produces:
  - `EditExtraPriceModal`: sửa `extra_price` theo `vehicle_payload_id` của 1 NCC → `updateExtraPrice(id, {extra_prices:[...]})`.
  - `EditPayloadRoadModal`: sửa `cost` theo `road_id` → `updatePayLoadRoads(id, {payload_roads:[...]})`.
  - Chỉ hiện khi `is_can_edit` (status=3 && created_by==me). Không tự sửa giá trị user nhập (báo đỏ dưới ô nếu sai).

- [ ] **Step 1: Playwright (fail trước)** — không có nút sửa giá.

- [ ] **Step 2: Tạo 2 modal.**

- [ ] **Step 3: Playwright** — sửa extra_price + cost, lưu → đọc lại thấy giá cập nhật + đề xuất min tính lại.

- [ ] **Step 4: Ghi ledger.**

---

## Task 14: FE — Modal Duyệt / Không duyệt

**Files:**
- Create: `.../components/ApproveModal.vue`

**Interfaces:**
- Consumes: `approve`.
- Produces: modal nhập `approver_comment` (required) + bảng giá duyệt (`approve_extra_price`/`approve_cost` prefill = min, sửa đè được); "Duyệt" → `approve(id,{status:1, approver_comment, vehicles:[...]})`; "Không duyệt" → `approve(id,{status:3, approver_comment})`. Chỉ hiện khi `is_can_approve`. Sau thành công → `markFormSaved()` → `$router.push` danh sách.

- [ ] **Step 1: Playwright (fail trước)** — user có quyền duyệt mở phiếu status=2 → chưa có nút Duyệt.

- [ ] **Step 2: Tạo modal + gắn `V2Footer` action.**

- [ ] **Step 3: Playwright** — duyệt phiếu status=2: thành công → quay về danh sách, phiếu thành Đã duyệt, BGHLVC sinh ra (kiểm qua màn BGHLVC hoặc tinker). Không duyệt → status về Đang tạo.

- [ ] **Step 4: Ghi ledger.**

---

## Task 15: FE — Điểm vào "Tổng hợp" ở chi tiết Báo giá vận chuyển

**Files:**
- Modify: `hrm-client/pages/transport/delivery-quotations/_id/index.vue` (hoặc nơi render action chi tiết BGVC) — thêm nút/menu "Tổng hợp".
- (BE nếu cần) Modify: Resource chi tiết `DeliveryQuotation` trả cờ `is_can_summary_cost`.

**Interfaces:**
- Consumes: `DeliveryQuotation::canSummaryCost()` (ĐÃ CÓ trong HRM — design §178: `status==1 || created_by==me`).
- Produces: nút "Tổng hợp" ẩn-hiện theo `is_can_summary_cost` → `$router.push('/transport/delivery-cost-summaries/create?delivery_quotation_id=<id>')`.

- [ ] **Step 1: Playwright (fail trước)** — mở chi tiết 1 BGVC status=1, chưa có nút "Tổng hợp".

- [ ] **Step 2: Thêm cờ BE (nếu Resource chưa trả) + nút FE.**

- [ ] **Step 3: Playwright** — nút hiện đúng điều kiện, bấm → sang trang tạo THGVC với query đúng.

- [ ] **Step 4: Ghi ledger.**

---

## Task 16: FE — Menu link + nút "Lập hợp đồng vận chuyển" (chưa phát triển)

**Files:**
- Modify: `hrm-client/components/subsystem-menu/transport.js` — thêm `link` cho mục "Tổng hợp giá vận chuyển đề xuất" (hiện label-only), `isShow` = có một trong 3 quyền "Xem...".
- Modify: chi tiết THGVC (`_id/index.vue`) — nút "Lập hợp đồng vận chuyển" ở báo giá NCC đã duyệt.

**Interfaces:**
- Produces: menu trỏ `/transport/delivery-cost-summaries`; nút "Lập hợp đồng vận chuyển" hiện khi `is_can_create_contract` (created_by==me && status==1) → bấm hiện toast/thông báo **"Tính năng chưa phát triển"** (design §61, quyết định user §141). **Không** dựng route cụt.

- [ ] **Step 1: Playwright (fail trước)** — menu Vận chuyển chưa có mục vào được; chi tiết chưa có nút Lập HĐ.

- [ ] **Step 2: Thêm link menu + nút + toast.**

- [ ] **Step 3: Playwright** — menu hiện đúng theo quyền, điều hướng được; nút Lập HĐ bấm → toast "Tính năng chưa phát triển", không điều hướng.

- [ ] **Step 4: Ghi ledger.**

---

## Ghi chú thực thi

- Thứ tự phụ thuộc: Task 1→2→3 nền; Task 4 (write BGHLVC) + 7 (import) + 8 (export) độc lập nhau, đều trước Task 5; Task 5 gom; Task 6/9/10 dựng API; FE 11–16 sau khi API 9 chạy. Import (12) cần trước khi kiểm RF#1 của Task 11 — có thể hoán đổi 11↔12 khi chạy FE.
- Mỗi task BE: `php -l` + tinker read-back; mỗi task FE: Playwright `127.0.0.1:3000` + grep V2Base RỖNG.
- Rulings (lệch tên cột/FK/số dòng Excel so với ERP, hay quyết định khung ma trận) ghi vào ledger + nhắc user ở bàn giao.
