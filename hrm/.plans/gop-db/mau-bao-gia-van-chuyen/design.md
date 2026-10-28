# Thiết kế: Port màn "Danh mục mẫu báo giá vận chuyển" (ERP → HRM)

> Ngày: 2026-10-27 · Nhánh: `develop` (hậu duệ `gop_db` ở cả hrm-api lẫn hrm-client) · Tài liệu đặt tại `.plans/gop-db/mau-bao-gia-van-chuyen/`
> Skill dẫn đường thi công: `erp-to-hrm-screen` (ERP = nguồn **nghiệp vụ**, HRM = nguồn **hình thức UI**).

## 1. Ý định & vì sao

Chuyển màn **Quản lý mẫu báo giá vận chuyển** của ERP (`/admin/delivery_quotations`) sang HRM, đặt ở
phân hệ **Vận chuyển › Vận chuyển với NCC › Danh mục mẫu báo giá vận chuyển** (`components/subsystem-menu/transport.js`
hiện mới chỉ có `label`, chưa có `link`).

Màn này là **khuôn mẫu giá vận chuyển dạng ma trận**: dòng = tuyến đường (kèm số km), cột = loại xe → trọng tải.
Các ô giá giao nhau trong màn này **để trống/khoá** — giá thật được nhập ở màn "Tổng hợp giá đề xuất" (chưa port).
Nói cách khác: đây là bước **khai bộ khung** (những tuyến nào × loại xe/trọng tải nào) để màn tổng hợp giá dùng lại.

Vì ERP và HRM **dùng chung 1 DB `erp_hrm_check`**, hai hệ chạy song song trên cùng dữ liệu. Port màn này sang HRM
không phá vỡ luồng ERP; các màn anh em (Bảng giá hiệu lực, Tổng hợp giá đề xuất, Hợp đồng vận chuyển) vẫn dùng bên ERP
cho tới khi được port sau.

## 2. Phạm vi

### Mục tiêu (Goals)
Port **đầy đủ** mọi chức năng thuộc màn này:
- **Danh sách**: lọc theo Mã / Ghi chú / Người tạo; cột STT, Mã, Ghi chú, Người tạo, Ngày tạo, Hành động.
- **Thêm mới**: form ma trận (thông tin chung + bảng tuyến × xe/trọng tải) + modal "Thêm nhanh tuyến".
- **Chi tiết** (xem read-only).
- **Sửa**.
- **Sao chép** (mở form Thêm mới, đổ sẵn dữ liệu phiếu nguồn, lưu thành phiếu mới).
- **Xuất Excel** (1 phiếu → file ma trận `Mau_bao_gia_van_chuyen.xlsx`).
- **Dropdown "Áp dụng cho bảng giá hiệu lực"**: port đầy đủ (đọc danh sách `PriceListValidDelivery` + lấy
  `date_valid_from`/`date_valid_to`/`km_actual` khi chọn).

### Không làm (Non-goals)
- **KHÔNG** port màn "Tổng hợp giá đề xuất" (`DeliveryCostSummary`), "Bảng giá hiệu lực", "Hợp đồng vận chuyển".
- **KHÔNG** nhập giá trong các ô ma trận (giữ trống/khoá y ERP).
- **KHÔNG** phân quyền dữ liệu theo công ty/phòng ban/bộ phận (ERP không có — xem Quyết định #1).
- **KHÔNG** migrate bảng mới: 4 bảng chính đã tồn tại trong DB chung.

### Anti-goals (coi như thất bại dù "chạy được")
- Màn trông "khác HRM" (dùng HTML thô, tự chế badge/modal/nút thay vì `V2Base*`).
- Tự ý thêm/bớt nghiệp vụ so với ERP mà không hỏi (vd tự bịa ô giá, tự thêm duyệt).
- Nút trỏ sang màn chưa port mà điều hướng đi "404" thay vì báo đang phát triển.

## 3. Quyết định đã chốt (với user)

1. **Phân quyền dữ liệu — KHÔNG phân cấp, giống hệt ERP.** Tạo **quyền MỚI** guard `api`, tên
   `Quản lý mẫu báo giá vận chuyển`, `type` = phân hệ Vận chuyển (tra `components/subsystems.js`). Ai có quyền thì
   **xem được hết mọi phiếu** toàn hệ thống (ERP không lọc theo công ty/người tạo). **Sửa/Xóa** chỉ cho phiếu
   **của chính mình** và trạng thái **"Đang tạo"**. KHÔNG tái dùng quyền ERP "Quản lý chi phí vận chuyển".
   Admin tự phân quyền mới cho vai trò (không tự gán).

2. **Dropdown "Áp dụng cho bảng giá hiệu lực" — làm đầy đủ.** Chỉ cần 2 endpoint đọc (list + getData) trên
   `PriceListValidDelivery` (entity HRM đã có sẵn ở `Modules/Finance/Entities/Delivery/`), KHÔNG cần port màn
   quản lý bảng giá. Hành vi y ERP: chọn 1 bảng giá → nạp `date_valid_from`, `date_valid_to`, `km_actual` vào form
   và **khoá 3 ô đó**; KHÔNG tự dựng ma trận (ERP đã bỏ phần đó, ghi rõ "bỏ check" trong code).

3. **Nút "Tổng hợp giá đề xuất" — báo "đang phát triển".** Vẫn hiện nút (ở cột Hành động danh sách + footer chi tiết),
   bấm vào → toast *"Chức năng đang phát triển"*, không điều hướng. (Đây là ngoại lệ có chủ đích với quy tắc "ẩn nút
   không dùng được": HRM đang dùng đúng mẫu "đang phát triển" cho mọi mục chưa port, khớp với menu xám.)

4. **Điều kiện hiện Sao chép / Xuất Excel**: luôn hiện (y ERP). **Sửa/Xóa**: chỉ chủ phiếu + trạng thái Đang tạo.
   Điều kiện hiện nút ở **danh sách phải khớp footer chi tiết** (quy tắc HRM).

## 4. Hiện trạng dữ liệu & phụ thuộc (DB chung `erp_hrm_check`)

### Bảng (đã có sẵn, KHÔNG migrate)
- `delivery_quotations`: `id, code(unique), date_valid_from(date), date_valid_to(date), price_list_valid_id(int null),
  km_actual(int), note(text null), status(int), created_by, updated_by, timestamps`.
- `delivery_quotation_vehicles`: `id, parent_id→delivery_quotations, vehicle_category_id, timestamps`.
- `delivery_quotation_vehicle_payloads`: `id, parent_id→vehicles, delivery_quotation_id, vehicle_payload_id, timestamps`.
- `delivery_quotation_vehicle_payload_roads`: `id, parent_id→payloads, delivery_quotation_id, road_id, km(decimal 10,2),
  vehicle_category_id, vehicle_payload_id, timestamps`.

> Lưu ý: bảng con (vehicle/payload/road) **không có** `created_by/updated_by` → model con KHÔNG ép audit.
> Chỉ `delivery_quotations` có audit.

### Danh mục phụ thuộc — hiện trạng đã xác minh (2026-10-27, DB chung `erp_hrm_check`)
- **Loại xe** `VehicleCategory` + **Trọng tải** `VehiclePayload`: `Modules/MasterData` — **đã có đủ** entity/service/controller/
  resource (route `vehicle-categories`, `vehicle-payloads`). ✅ Tái dùng.
- **Bảng giá hiệu lực** `PriceListValidDelivery` (+ con): `Modules/Finance/Entities/Delivery/` — **mới có entity**, chưa có
  endpoint. Bảng `price_list_valid_deliveries` CÓ `company_id, code, date_valid_from/to, km_actual`. → **cần thêm 2 endpoint
  đọc** (list theo company + getData 3 field).
- **Tuyến đường**: entity thật HRM là **`TpRoad extends Model`** (bảng `roads`), KHÔNG phải `Road`. `RoadController`
  (`Modules/Assign`) hiện **chỉ có `getAll()`** (trả toàn bộ, không search/không lọc tỉnh-điểm xuất phát). Bảng `roads`
  có đủ `start_point_id, province_id, km, status` và **3.210 dòng** → **cần thêm 2 endpoint**: (a) search server-side cho
  modal "Chọn tuyến"; (b) lọc theo `province_id`+`start_point_id` cho "Thêm nhanh tuyến".
- **Điểm xuất phát** `DeliveryStartPoint`: ⚠️ **HRM CHƯA có** entity/endpoint/màn (grep 0 kết quả). Bảng
  `delivery_start_points` **có trong DB chung, 7 dòng**. → **cần thêm entity (map bảng sẵn có) + 1 endpoint đọc list**
  (phục vụ modal "Thêm nhanh tuyến"). Không port màn quản lý.
- **Tỉnh/thành** `Province`: HRM đã có — tái dùng cho modal "Thêm nhanh tuyến".

## 5. Nghiệp vụ ERP (nguồn chân lý) — tóm tắt hành vi

### 5.1 Trạng thái
- Tạo mới → `status = 3` ("Đang tạo"). Màn này **không có luồng duyệt**. (ERP có `canSummaryCost` tham chiếu `status==1`
  nhưng không đặt được status 1 từ màn này.)
- `canEdit()` = `canDelete()` = `status == 3 && Auth::id == created_by`.

### 5.2 Mã — **replicate y hệt ERP (id-based), KHÔNG dùng year-based**
- ERP: lưu tạm `code = randomString(5)`, sau `save()` → `code = "BGVC-" . generateCode(5, id)` = **`BGVC-` + zero-pad id 5 chữ số,
  KHÔNG có năm**. Mã mới nhất trên DB chung hiện là **`BGVC-00089`** (68 dòng).
- **Quyết định (builder call, bắt buộc theo tính đúng đắn):** HRM **không** dùng `getNextCode()` kiểu `PREFIX-YYYY-NNNNN`.
  Vì ERP & HRM **ghi chung 1 bảng `delivery_quotations`**, nếu HRM đếm-theo-năm sẽ (a) lệch định dạng mã ERP, (b) nguy cơ
  trùng mã với dòng ERP tạo song song. → HRM lặp đúng cơ chế **2 bước**: `save()` lấy `id` → set `code = "BGVC-"+str_pad($id,5,'0',LEFT)`
  → `save()` lần 2. (Port đúng hàm `generateCode($length, $id)` của ERP.)

### 5.3 Validate (store vs update) — **có khác biệt**
| Trường | store | update |
|---|---|---|
| `vehicles` | required, array, 1..99 | giống |
| `vehicles.*.vehicle_category_id` | required, exists | giống |
| `vehicles.*.payloads` | required, array, 1..99 | giống |
| `vehicles.*.payloads.*.vehicle_payload_id` | required, exists | giống |
| `vehicles.*.payloads.*.roads` | required, array, 1..2000 | giống |
| `roads` | required, array, min 1 | giống |
| `roads.*.road_id` | required, exists | giống |
| `roads.*.km` | required, numeric, 1..999999999 | giống |
| `date_valid_from` | `price_list_valid_id` có → `required`; không → `required\|date\|after_or_equal:today` | giống |
| `date_valid_to` | required, date, after_or_equal:date_valid_from | giống |
| `km_actual` | required | giống |
| `note` | **(không bắt buộc)** | **required** |

- **Câu lỗi nghiệp vụ ERP**: "Bắt buộc phải chọn" / "Bắt buộc phải nhập" / "Ngày hiệu lực từ không được chọn ngày quá khứ".
  → Theo chuẩn HRM: rule phổ biến (`required`/`numeric`/`after_or_equal`…) **dùng câu lang file sẵn**, KHÔNG tự khai
  `messages()`; chỉ giữ câu nghiệp vụ riêng khi lang file không diễn đạt được.

### 5.4 Chặn trùng khoảng bảng giá hiệu lực
Khi **không** chọn `price_list_valid_id`: nếu tồn tại `PriceListValidDelivery` cùng `company_id` có khoảng ngày
giao với `[date_valid_from, date_valid_to]` → chặn: **"Đã có bảng giá hiệu lực trong khoảng thời gian này"**.
(Khi có chọn bảng giá thì bỏ qua check này.)
> `company_id` ở ERP lấy theo `auth()->user()->info->company_id`. HRM: lấy theo company của người đăng nhập (tra pattern
> công ty hiện hành trong HRM). Ghi chú builder: xác nhận cột `company_id` trên `price_list_valid_deliveries`.

### 5.5 Lưu chi tiết (`syncDetails`)
Xoá sạch rồi tạo lại toàn bộ con mỗi lần lưu (roads → payloads → vehicles). Mỗi vehicle có payloads; mỗi payload có
roads **song song theo index** với danh sách `roads` gốc (base roads = `vehicles[0].payloads[0].roads`). Bảng con
road lưu kèm `road_id, km, vehicle_category_id, vehicle_payload_id`.

### 5.6 Xoá
Hard-delete con trước (road → payload → vehicle) rồi xoá phiếu — chỉ khi `canDelete()`.

### 5.7 Sao chép
Mở form Thêm mới đổ sẵn dữ liệu phiếu nguồn (dùng `getDataForEdit`), submit như tạo mới (phiếu mới, mã mới, không id).

### 5.8 Xuất Excel
`DeliveryQuotationExcel` dựng ma trận từ `excel_data` (NOTE, CODE, VEHICLES[payloads], ROADS, MAX_COLS). File
`Mau_bao_gia_van_chuyen.xlsx`.
> Theo chuẩn HRM `export-excel`: ô số là **số thật + numFmt**, không đổ chuỗi; định dạng số quốc tế `1,234,567.89`.

### 5.9 Dropdown bảng giá hiệu lực
- List: `PriceListValidDelivery` theo `company_id`, `latest()`. Option hiển thị **mã** (`code`).
- `getData/{id}` (ERP route `price-list-valid-delivery.getData`): trả `date_valid_from, date_valid_to, km_actual`.
- Khi chọn: FE điền 3 ô đó + **disable** 2 ô ngày.

## 6. Mô hình ma trận (FE) — port từ ES6 class ERP

ERP dùng 4 class (`DeliveryContract` + Vehicle/Payload/Road) với getter/setter. Hành vi cốt lõi cần giữ:
- `form.payloads` = **gộp phẳng** toàn bộ payload của mọi vehicle (theo thứ tự) → đây là các **cột** của ma trận.
- `form.roads` = roads của `vehicles[0].payloads[0]` → các **dòng** (base road list, mỗi dòng có `road_id` + `km`).
- `addVehicle()` thêm 1 cột-nhóm xe (mặc định 1 payload rỗng). `removeVehicle(i)`.
- `vehicle.addPayload()` thêm 1 cột trọng tải trong nhóm xe. `removePayloadByRef(p)` (chỉ khi >1 payload).
- `addRoad()` thêm 1 **dòng tuyến vào mọi payload** (giữ song song index). `removeRoad(i)` xoá dòng khỏi mọi payload.
- `available_vehicle_categories` = loại xe chưa bị nhóm xe **khác** chọn (chặn trùng loại xe).
- `available_payloads` = trọng tải chưa bị payload **khác trong cùng xe** chọn (chặn trùng trọng tải trong 1 xe).
- `road_id` setter → tự điền `km` = km của tuyến.
- Chọn tuyến qua **modal tìm tuyến** (ERP: `chooseRoad` → `roadModal`), hiện tên tuyến ở ô disabled. Vì `roads` có 3.210 dòng
  → modal dùng **search server-side** (`V2BaseSelectInModal` hoặc list có ô tìm + phân trang), KHÔNG load hết như ERP
  (chuẩn hiệu năng HRM). Khi chọn tuyến → tự điền `km` từ tuyến.
- **Thêm nhanh tuyến** (modal): chọn Tỉnh + Điểm xuất phát → gọi endpoint lọc tuyến theo `province_id`+`start_point_id` →
  thêm hàng loạt vào mọi payload (bỏ tuyến đã có); trần 800 tuyến (y ERP). Cần endpoint "điểm xuất phát" (7 dòng) +
  endpoint "tuyến theo tỉnh/điểm xuất phát".
- Ô giá ("Giá cước vượt trội" + ô giao nhau) **disabled/trống** trong màn này.

> Builder lưu ý: Vue 2 reactivity không theo dõi tốt getter/setter + prop `_private` của ES6 class. Hai hướng:
> **(a)** port sang **plain reactive object + helper thuần** (hàm trong `utils/` — khuyến nghị, hợp chuẩn "tách business
> function" của skill Bước 3b); **(b)** giữ class nhưng bọc `Vue.observable`/`$set` cẩn thận. Chọn (a) trừ khi có lý do.

## 7. Kiến trúc HRM dự kiến

### 7.1 Backend — `Modules/Transport` (hiện trống)
- **Entities** (map đúng 4 bảng sẵn có; `DeliveryQuotation extends App\Models\BaseModel` để tự audit; 3 model con
  `extends BaseModel` nhưng bảng không có cột audit nên vô hại, hoặc `extends Model` tuỳ chuẩn — xác nhận):
  `DeliveryQuotation`, `DeliveryQuotationVehicle`, `DeliveryQuotationVehiclePayload`, `DeliveryQuotationVehiclePayloadRoad`.
  Quan hệ + `syncDetails` + `getNextCode()` (tiền tố `BGVC-`) + accessor `is_can_edit`/`is_can_delete` +
  `status_text`/`status_color` (BE quyết chữ+màu badge).
- **Service**: `DeliveryQuotationService` (search/paginate, create, update, delete, copy-prefill, form-options,
  export-rows). Gộp danh mục dùng chung (loại xe/trọng tải/bảng giá) vào **1 endpoint `form-options`** (chuẩn hiệu năng
  HRM: 1 màn = ít API). Dropdown tuyến dùng **search server-side** (danh mục lớn).
- **Controller** `V1/DeliveryQuotationController` + **FormRequest** (chỉ `rules()`, không `messages()` cho rule phổ biến).
- **Resource** (list item + detail) trả `status_text/status_color/is_can_edit/is_can_delete`, ma trận dạng vehicles→payloads→roads.
- **Route** `Modules/Transport/Routes/api.php`: list/detail (GET, gắn `checkPermission` nếu có quyền xem riêng — ở đây
  dùng chung 1 quyền), store/update/destroy/copy/export gắn `checkPermission:Quản lý mẫu báo giá vận chuyển`.
- **Endpoint đọc phụ thuộc cần thêm** (tối thiểu, chỉ đọc — KHÔNG port màn quản lý):
  - `PriceListValidDelivery`: list theo company + `getData/{id}` (trả `date_valid_from/to`, `km_actual`).
  - `DeliveryStartPoint`: entity mới (map bảng `delivery_start_points` sẵn có, 7 dòng) + 1 endpoint list.
  - Tuyến đường (`TpRoad`/bảng `roads`, 3.210 dòng): (a) endpoint **search server-side** (cho modal Chọn tuyến);
    (b) endpoint lọc theo `province_id`+`start_point_id` (cho Thêm nhanh tuyến). Mở rộng `RoadController` của `Modules/Assign`
    hoặc thêm trong Transport (xác nhận nơi hợp lý).
- **Permission seeder**: thêm 1 dòng `$this->perm([...])` vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
  (không `id`, không `guard_name`; `type` = Vận chuyển).

### 7.2 Frontend — `pages/transport/delivery-quotations/`
Theo `khuon-man-mau` của skill:
- `index.vue` — danh sách (4 list mixin, `V2BaseSmartFilterPanel` floating, `columnCustomizationMixin` +
  `user_column_settings`, `V2BaseDataTable`, badge `V2BaseBadge`, cột "Người tạo"/"Ngày tạo").
- `add.vue` — Thêm mới (và dùng lại cho **Sao chép** qua query `?copy_from=<id>`).
- `_id/index.vue` — Chi tiết (read-only, nút ở `V2Footer`).
- `_id/edit.vue` — Sửa.
- `DeliveryQuotationForm.vue` — form ma trận dùng chung cho add/edit/copy; bảng tràn ngang bọc `V2BaseTableScroll`.
- Modal "Thêm nhanh tuyến" + modal "Chọn tuyến" dựng trên `components/modal/V2BaseModal.vue`, select trong modal dùng
  `V2BaseSelectInModal`.
- Mọi input dùng `V2Base*` (ngày → `V2BaseDatePicker`, số km → `V2BaseInput`/số, ghi chú → `V2BaseTextarea`,
  select → `V2BaseSelect`). `unsavedChangesMixin`. Số định dạng `1,234,567.89`.
- Menu: `components/subsystem-menu/transport.js` — đổi mục "Danh mục mẫu báo giá vận chuyển" từ `label` → thêm
  `link: '/transport/delivery-quotations'`.
- Nút cụm `mr-2 mb-2` (nút cuối `mb-2`). Sau khi lưu → `markFormSaved()` + `$router.push` về danh sách.

### 7.3 Nhãn/UI chuẩn (skill thắng spec)
- Ô `km_actual` nhãn ERP là **"Số Km tính cước vượt trội"** (giữ nguyên nhãn ERP vì là nghiệp vụ, không phải từ bị cấm).
- Cột/nhãn "Người tạo", "Ngày tạo" (KHÔNG "Người lập/Ngày lập").
- Nút Lưu/Hủy theo `button-convention`; ô rỗng để trống (không "—").

## 8. Việc để builder tự quyết (minor, sẽ ghi lại khi làm)
- Vị trí các endpoint đọc phụ thuộc (Transport vs Finance/Assign).
- Model con `extends BaseModel` hay `extends Model` (bảng không có audit) — chọn theo chuẩn module.
- Có cần index DB bổ sung cho cột lọc (`code`, `created_by`) không — kiểm tra trước bàn giao.
- Tên route/endpoint cụ thể, tên FormRequest/Resource.

### Quyết định builder đã chốt sau rà soát (2026-10-27)
- **Mã phiếu**: replicate ERP id-based `BGVC-`+zero-pad(id,5), KHÔNG year-based (xem 5.2).
- **"Thêm nhanh tuyến" + "Chọn tuyến"**: port **đầy đủ** (đồng nhất với tinh thần "làm trọn chức năng của màn" mà user
  đã chốt ở dropdown bảng giá). Kéo theo: thêm entity+endpoint đọc `DeliveryStartPoint` (7 dòng) và 2 endpoint tuyến.
- **Chọn tuyến dùng search server-side** (roads 3.210 dòng) thay vì load-all như ERP — theo chuẩn hiệu năng HRM.

## 9. Kích thước & quy trình
- **Dự án có thiết kế viết** (nhiều màn + form ma trận + BE module + quyền mới). Sau khi anh duyệt `design.md` này →
  viết `plan.md` (task chi tiết), rồi thi công theo skill `erp-to-hrm-screen` (6 bước), verify bằng Playwright.
- hrm-client đẩy `develop`; hrm-api theo tiền lệ các màn port trước: **giữ local chờ review** (xác nhận lại khi tới bước commit).

## 10. Câu hỏi còn mở cho user
Đã chốt: phân quyền, dropdown bảng giá, nút tổng hợp, mã phiếu, hướng tuyến đường. Còn 2 điểm nhỏ (đều có mặc định, anh
chỉ cần phản đối nếu muốn khác):
1. **`note` bắt buộc khi Sửa nhưng không bắt buộc khi Tạo** (y ERP) — giữ nguyên lệch này hay đồng bộ? Mặc định: **giữ y ERP**.
2. **Modal "Thêm nhanh tuyến"** kéo theo việc port thêm 1 catalog đọc nhỏ ("Điểm xuất phát", 7 dòng) + endpoint tuyến.
   Mặc định: **làm đầy đủ** (giữ đúng chức năng màn). Nếu anh muốn gọn hơn, có thể **bỏ modal Thêm nhanh tuyến** (vẫn
   thêm tuyến từng dòng qua modal Chọn tuyến) để khỏi đụng catalog Điểm xuất phát — nói là tôi bỏ.
