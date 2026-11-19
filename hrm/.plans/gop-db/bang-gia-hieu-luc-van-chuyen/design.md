# Thiết kế: Port màn "Bảng giá hiệu lực vận chuyển" (ERP → HRM) — CHỈ ĐỌC

> Ngày: 2026-10-28 · Nhánh: `develop` (hậu duệ `gop_db` ở cả hrm-api lẫn hrm-client) · Tài liệu đặt tại `.plans/gop-db/bang-gia-hieu-luc-van-chuyen/`
> Skill dẫn đường thi công: `erp-to-hrm-screen` (ERP = nguồn **nghiệp vụ**, HRM = nguồn **hình thức UI**).
> Màn anh em đã port: "Danh mục mẫu báo giá vận chuyển" (`.plans/gop-db/mau-bao-gia-van-chuyen/`).

## 1. Ý định & vì sao

Chuyển màn **Bảng giá hiệu lực vận chuyển** của ERP (route `price-list-valid-deliveries`,
`PriceListValidDeliveryController`) sang HRM, đặt ở phân hệ **Vận chuyển › Vận chuyển với NCC ›
Bảng giá hiệu lực vận chuyển**. Slot menu **đã có sẵn** ở `components/subsystem-menu/transport.js`
dòng 46 (`{ label: 'Bảng giá hiệu lực vận chuyển' }` — mới có `label`, chưa có `link`).

Màn này là **bảng giá cước vận chuyển đang còn hiệu lực**: với mỗi bảng giá, dữ liệu là ma trận
**tuyến đường (× km) × dòng xe × trọng tải**, ô = **đơn giá cước** (`cost`), kèm dòng phụ phí
"Giá cước vượt trội" (`extra_price`) theo từng mức tải. Đây là bảng giá **đã chốt số** (khác màn
"mẫu báo giá" — ô giá để trống), các màn khác (lập báo giá/hợp đồng vận chuyển) tra bảng này để
tính cước.

Vì ERP và HRM **dùng chung 1 DB `erp_hrm_check`**, port màn này không phá vỡ luồng ERP. Phần
**sinh bảng giá** (nằm ở màn "Tổng hợp chi phí vận chuyển" / `DeliveryCostSummary` của ERP — chưa
port) vẫn chạy bên ERP; 6 bảng giá hiện có trong DB chung được HRM **xem / in / gia hạn**.

## 2. Phạm vi

### Mục tiêu (Goals) — màn **CHỈ ĐỌC**
- **Danh sách**: lọc theo Mã / Người tạo; cột STT, Mã, Công ty, Hiệu lực từ, Hiệu lực đến, Người tạo,
  Ngày tạo, Hành động.
- **Chi tiết** (read-only): ma trận tuyến × xe → trọng tải (ô = `cost`), dòng "Giá cước vượt trội"
  (= `extra_price`), kèm **tab "Báo giá"** liệt kê file báo giá gốc của nhà cung cấp để **xem/tải**.
- **Lọc tuyến đường trong chi tiết**: multi-select các tuyến của bảng giá → lọc bảng ma trận chỉ còn
  các tuyến đã chọn (bám ERP; chi tiết §5.6b).
- **In**: bản in khổ ngang bảng giá (dựng lại theo chuẩn in HRM), có letterhead công ty của chứng từ.
- **Gia hạn**: modal 1 ô "Hiệu lực đến" → cập nhật `date_valid_to`.

### Không làm (Non-goals)
- **KHÔNG** port màn sinh bảng giá ("Tổng hợp chi phí vận chuyển" / `DeliveryCostSummary`). Để sau
  (user chốt: *"sinh bảng giá này tự động thì phải, cứ để sau"*).
- **KHÔNG** có Tạo mới / Sửa ma trận / Xóa / Sao chép / Xuất Excel (ERP màn này cũng không có).
- **KHÔNG** phân quyền dữ liệu theo công ty/phòng ban/bộ phận; **KHÔNG** có ô lọc Công ty (ERP
  không có — xem Quyết định #1).
- **KHÔNG** migrate bảng mới: 4 bảng ma trận + bảng báo giá NCC đã tồn tại trong DB chung.
- **KHÔNG** thêm/sửa/xoá file báo giá NCC ở HRM (chỉ xem/tải).

### Anti-goals (coi như thất bại dù "chạy được")
- Màn trông "khác HRM" (HTML thô, tự chế badge/modal/nút thay vì `V2Base*`).
- Tải **toàn bộ** ~14.400 dòng tuyến của 1 bảng giá về một lần → treo trình duyệt (phải phân trang
  như ERP, xem Quyết định #4).
- Nút "In" / "Gia hạn" ở danh sách có điều kiện hiện **khác** footer chi tiết.
- Cho gia hạn mà **không kiểm lại quyền ở BE** (lộ quyền ghi).

## 3. Quyết định đã chốt (với user)

1. **Phân quyền — 1 QUYỀN XEM, thấy mọi công ty, giống hệt ERP.** (user: *"như erp 1 quyền"*.)
   Tạo **quyền MỚI** guard `api`: `Quản lý bảng giá hiệu lực vận chuyển` (xem danh sách + chi tiết +
   in), `type` = phân hệ **Vận chuyển** (tra `components/subsystems.js`). Ai có quyền thì xem được
   **hết mọi bảng giá** toàn hệ thống — KHÔNG lọc theo công ty/người tạo, KHÔNG có ô lọc Công ty.
   Bộ lọc chỉ gồm **Mã** + **Người tạo**. KHÔNG tái dùng quyền ERP ("Quản lý chi phí vận chuyển" /
   "Duyệt giá vận chuyển" — guard web, sẽ 403). Admin tự phân quyền mới cho vai trò.

2. **Gia hạn — theo ERP (Cách B): cần QUYỀN GIA HẠN *HOẶC* là người tạo.** (user: *"cứ bám erp, B"*.)
   Tạo **quyền MỚI** guard `api`: `Gia hạn bảng giá hiệu lực vận chuyển`, `type` = Vận chuyển. Nút
   "Gia hạn" hiện khi `có quyền "Gia hạn bảng giá hiệu lực vận chuyển"` **OR** `auth()->id() ==
   created_by`. BE **kiểm lại đúng điều kiện này** trước khi ghi (fail-closed, không hard-code
   `true`). Tương đương ERP: `can('Duyệt giá vận chuyển') || auth()->id() == created_by`.

3. **Tab "Báo giá" (file NCC đính kèm) — CÓ trong phạm vi.** (user: *"có nhé"*.) Màn chi tiết hiển
   thị danh sách file báo giá gốc của nhà cung cấp (xem/tải), **chỉ đọc**. Dữ liệu thật: 63 dòng
   báo giá / 6 bảng giá, 13 file đính kèm (không phải báo giá nào cũng có file).

4. **Ma trận tuyến đường — PHÂN TRANG phía server, bám `getRoadData` của ERP.** Bảng tuyến khổng lồ
   (`price_list_valid_delivery_vehicle_payload_roads` = **86.462 dòng**, ~14.400 dòng/bảng giá). Màn
   chi tiết nạp **header + khung cột** (dòng xe → trọng tải + dòng "Giá cước vượt trội") ngay, còn
   **thân ma trận (các dòng tuyến) tải phân trang** qua endpoint riêng (mirror ERP `getRoadData`).
   KHÔNG load-all (chuẩn hiệu năng HRM).

## 4. Hiện trạng dữ liệu & phụ thuộc (DB chung `erp_hrm_check`) — đã xác minh 2026-10-28

### Bảng ma trận (đã có sẵn, KHÔNG migrate; entity HRM đã có ở `Modules/Finance/Entities/Delivery/`)
- `price_list_valid_deliveries` (**6 dòng**): `id, code(varchar UNIQUE), company_id(int unsigned),
  date_valid_from(datetime), date_valid_to(datetime), km_actual(int), created_by, updated_by,
  timestamps`. **KHÔNG có cột `status`.**
- `price_list_valid_delivery_vehicles` (**14 dòng**): `id, price_list_valid_delivery_id,
  vehicle_category_id, created_by, updated_by, timestamps`.
- `price_list_valid_delivery_vehicle_payloads` (**65 dòng**): `id,
  price_list_valid_delivery_vehicle_id, vehicle_payload_id, extra_price(decimal 16,2), created_by,
  updated_by, timestamps`. — `extra_price` = **phụ phí mức tải** ("Giá cước vượt trội").
- `price_list_valid_delivery_vehicle_payload_roads` (**86.462 dòng** — bảng lá):
  `id, price_list_valid_delivery_vehicle_payload_id, road_id, km(decimal 10,2), cost(decimal 16,2),
  created_by, updated_by, timestamps`. — `cost` = **đơn giá cước** tuyến đó cho mức tải đó.

Entity HRM sẵn có (read-only, `$guarded=['*']`):
`PriceListValidDelivery` → `vehicles()` → `PriceListValidDeliveryVehicle` → `payloads()` →
`PriceListValidDeliveryVehiclePayload` → `roads()` → `PriceListValidDeliveryVehiclePayloadRoad`.

### Bảng báo giá NCC + file đính kèm (cho tab "Báo giá")
- `price_list_valid_delivery_quotations` (**63 dòng**): `id, price_list_valid_delivery_id,
  supplier_id, timestamps`. **KHÔNG có cột audit** (`created_by/updated_by`). → **HRM CHƯA có
  entity**, cần **tạo mới** `PriceListValidDeliveryQuotation` (map bảng sẵn có, `extends Model`).
- File lưu ở bảng chung `files` với `table = 'price_list_valid_delivery_quotations'`,
  `table_id = quotation.id`; cột dùng: `file_name`, `file_path` (URL tuyệt đối S3), `file_type`,
  `file_size`. (**13 dòng** cho các bảng giá hiện có.)
- `supplier_id` → **nhà cung cấp**: ở ERP `Supplier` khai `$table = 'customers'` + `is_supplier`
  (bẫy đã ghi memory — bảng `suppliers` vật lý rỗng). HRM lấy tên NCC từ `customers`.

### Danh mục phụ thuộc
- **Loại xe** `VehicleCategory`, **Trọng tải** `VehiclePayload`: `Modules/MasterData` — **đã có đủ**
  entity/service (route `vehicle-categories`, `vehicle-payloads`). ✅ Tái dùng để hiện tên cột.
- **Tuyến đường**: entity HRM là **`TpRoad`** (bảng `roads`). Màn này chỉ hiển thị **tên tuyến**
  theo `road_id` trong bảng lá → nạp kèm khi phân trang getRoadData (không cần search).
- **Công ty** `Company`: HRM đã có — hiện cột "Công ty" theo `company_id` của bảng giá.

## 5. Nghiệp vụ ERP (nguồn chân lý) — tóm tắt hành vi

File ERP: Controller `app/Http/Controllers/Common/PriceListValidDeliveryController.php`; Model
`app/Model/Common/PriceListValidDelivery.php`; Service `app/Services/PriceListValidDelivery/
PriceListValidDeliveryService.php`; routes prefix `price-list-valid-deliveries`
(`routes/web.php` ~5850-5866, middleware `checkPermission:Quản lý chi phí vận chuyển`); blade index/
show ở `resources/views/common/price_list_valid_deliveries/`.

### 5.1 Không có trạng thái
Bảng không có cột `status`. "Còn hiệu lực" = `hôm nay ∈ [date_valid_from, date_valid_to]` (cùng công
ty). Màn danh sách ERP **không lọc** theo còn/hết hiệu lực; chỉ hiển thị khoảng ngày để người xem tự
nhìn. → HRM **không** dựng badge trạng thái (không có gì để map). Có thể hiển thị khoảng ngày; builder
cân nhắc tô màu dòng đã hết hiệu lực là tuỳ chọn nhỏ (không bắt buộc, hỏi nếu muốn thêm).

### 5.2 Mã phiếu
`code = "BGHLVC-" . generateCode(5, id)` = **`BGHLVC-` + zero-pad id 5 chữ số** (vd `BGHLVC-00007`),
dựa trên auto-increment id (KHÔNG theo năm). Màn này **chỉ đọc** → HRM **không sinh mã** (phần sinh
bảng giá để sau). Chỉ **hiển thị** `code` đã có sẵn. Không cần `getNextCode()`.

### 5.3 Danh sách
- Cột: STT (index) · **Mã** (link sang chi tiết) · Công ty (không sort) · Hiệu lực từ (d/m/Y) ·
  Hiệu lực đến (d/m/Y) · Người tạo (họ tên NV) · Ngày tạo (d/m/Y) · Hành động.
- Sort mặc định `->latest()` (ngày tạo giảm dần).
- Lọc: `code` (text, like) + `created_by` (select người tạo, =). **Không** tìm nhanh bên ERP, nhưng
  HRM **bắt buộc có ô tìm nhanh** (skill `list-page`) → ô tìm nhanh tìm theo **Mã** (nội dung phiếu);
  Người tạo là **select ở bộ lọc** (không đưa vào ô tìm nhanh — quy ước HRM).

### 5.4 Hành động mỗi dòng (và footer chi tiết — phải KHỚP nhau)
- **In**: luôn hiện.
- **Gia hạn**: hiện khi `có quyền "Gia hạn bảng giá hiệu lực vận chuyển" OR auth()->id() == created_by`
  (Quyết định #2). ERP gốc: `can('Duyệt giá vận chuyển') || auth == created_by`.
- Không có Xem/Sửa/Xóa/Sao chép/Excel.

### 5.5 Gia hạn (`extendDate`)
- Modal 1 trường `date_valid_to`, validate `required | date | after:today`.
- BE kiểm lại quyền (Quyết định #2) **trước** khi ghi; cập nhật `date_valid_to` của bảng giá.
- Thành công → đóng modal, nạp lại danh sách/chi tiết, toast thành công (câu chuẩn HRM).

### 5.6 Chi tiết — ma trận + phân trang tuyến
- Khung: **cột** = mỗi `vehicle` (theo `vehicle_category_id`) → trong đó mỗi `payload`
  (`vehicle_payload_id`) là 1 cột con. **Dòng** = tuyến đường (`road_id` + `km`). **Ô** giao nhau =
  `cost` của road đó ở payload đó. Dòng đầu "Giá cước vượt trội" = `extra_price` theo từng payload.
- `delivery_recipe` (nếu cần cho popup/định mức) = `is_two_way ? cost*2 : cost` — **chỉ dùng khi có**;
  ở màn danh sách/chi tiết bảng giá hiển thị thẳng `cost`.
- **Phân trang tuyến (getRoadData)**: endpoint trả theo trang các **tuyến** của 1 bảng giá, mỗi tuyến
  kèm `cost` theo từng payload (ghép từ bảng lá theo `road_id`).
- **CHỐT KỸ THUẬT (builder-call, 2026-10-28):** ERP `getRoadData` thực chất **load toàn bộ ma trận
  (~14.400 dòng) vào PHP rồi mới cắt trang** (`getRoads($id)` nạp hết, gom nhóm, `forPage`) — tức
  đúng kiểu "load-all-in-memory" mà §2 đã liệt vào anti-goal. HRM **KHÔNG mirror nguyên si**: phân
  trang **ở tầng DB** trên **danh sách tuyến gốc phân biệt** (`DISTINCT road_id` của bảng giá, có thể
  dựa trên payload base), rồi với các `road_id` trong trang mới `whereIn` lấy `cost` theo từng payload.
  Kết quả hiển thị y hệt ERP nhưng không nạp cả bảng mỗi request. Builder **vẫn phải đọc** `getRoads`
  dòng ~90-145 để khớp **đúng cách gom cột theo payload** (`groupBy('vehicle_category_id')->flatten()`
  + match `vehicle_payload_id`), chỉ thay cơ chế phân trang.
- **Căn ô theo HEADER, không theo `road.payloads`:** ERP căn ô bằng `ng-repeat="p in road.payloads"`
  — chỉ đúng khi mọi tuyến tồn tại ở mọi payload (dữ liệu thật khớp vì màn sinh giá chèn tuyến gốc
  cost=0 vào mọi payload). HRM dựng lại phải **căn ô theo đúng cột payload ở header**, ô (tuyến ×
  payload) thiếu thì **để trống**, nếu không bảng lệch cột ở bảng giá dữ liệu không đều.

### 5.6b Lọc tuyến đường (trong màn chi tiết) — PORT (user chốt 2026-10-28)
- ERP (`show.blade` dòng 100-127): card "Lọc tuyến đường" có multi-select `road_ids` chứa **toàn bộ
  tuyến của bảng giá**, bấm "Lọc" → `getRoadData` nhận `road_ids` và `whereIn('id', road_ids)` chỉ
  trả các tuyến đã chọn.
- HRM: thêm **1 endpoint liệt kê tuyến của bảng giá** (các `road_id` phân biệt thuộc bảng giá + tên
  tuyến) có **search server-side** (KHÔNG load toàn bộ như ERP — chuẩn hiệu năng). UI dùng
  `V2BaseSelect` multiple (hoặc `V2BaseSelectInModal` nếu danh sách lớn) để chọn tuyến; truyền
  `road_ids` vào `getRoadData` cùng tham số phân trang. Xoá lọc → quay về phân trang toàn bộ.

### 5.7 Tab "Báo giá"
- Liệt kê `price_list_valid_delivery_quotations` của bảng giá, nhóm theo **nhà cung cấp**
  (`supplier_id` → tên từ `customers`), với các file đính kèm (`files` theo `table`/`table_id`).
- Chỉ **xem + tải** (link `file_path`). Không upload/xoá.

### 5.8 In
- ERP: `print_landscape.blade.php` + mẫu DB `ReportTemplate::BANG_GIA_VAN_CHUYEN_HIEU_LUC`, khổ ngang.
- HRM: **dựng lại bản in theo chuẩn** skill `print-page` (letterhead lấy theo `company_id` **của
  chứng từ**, không theo người đăng nhập). Bản in rất rộng (nhiều cột payload) → khổ ngang, canh cột
  theo chuẩn in HRM.

## 6. Kiến trúc HRM dự kiến

### 6.1 Backend
- **Controller**: `Modules/Transport/Http/Controllers/V1/PriceListValidDelivery/
  PriceListValidDeliveryController` (đặt cùng phân hệ Vận chuyển như màn anh em `DeliveryQuotation`;
  tái dùng entity ở `Modules/Finance/Entities/Delivery/`). Action: `index`, `show`, `getRoadData`
  (phân trang tuyến, nhận `road_ids` để lọc), `roadOptions` (liệt kê tuyến của bảng giá cho bộ lọc,
  search server-side), `print`, `extendDate` (POST).
- **Entity mới**: `PriceListValidDeliveryQuotation` (map bảng sẵn có, `extends Model` — bảng không có
  audit) + quan hệ `supplier()` (→ `customers`/`Supplier`) và đọc `files` (table/table_id). Đặt cạnh
  các entity Delivery ở `Modules/Finance/Entities/Delivery/` (builder xác nhận vị trí).
- **Service** `PriceListValidDeliveryService`: search/paginate danh sách; dựng khung cột chi tiết;
  `getRoadData` phân trang; gom dữ liệu in; `extendDate` (kiểm quyền + cập nhật). Logic tra giá dùng
  chung (nếu sau này cần) để ở service theo chủ đề nghiệp vụ (skill Bước 3b).
- **FormRequest** `ExtendDateRequest`: `rules()` cho `date_valid_to` (`required|date|after:today`);
  `authorize()` = điều kiện Quyết định #2 (quyền OR người tạo) → 403 trước validate. KHÔNG khai
  `messages()` cho rule phổ biến (dùng lang file).
- **Resource**: list item (code, company_name, date_valid_from/to, created_by name, created_at,
  `is_can_extend`) + detail (khung vehicles→payloads + extra_price; roads trả qua getRoadData riêng;
  quotations+files cho tab Báo giá). BE quyết `is_can_extend` (fail-closed).
- **Route** `Modules/Transport/Routes/api.php`, nhóm `/v1/transport/valid-delivery-prices`, middleware
  `checkPermission:Quản lý bảng giá hiệu lực vận chuyển`. Route tĩnh (`getRoadData`, `roadOptions`,
  `print`, `extendDate`) đặt trước `/{id}`.
- **Permission seeder**: thêm **2 dòng** `$this->perm([...])` vào
  `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (không `id`, không `guard_name`;
  `type` = Vận chuyển): "Quản lý bảng giá hiệu lực vận chuyển", "Gia hạn bảng giá hiệu lực vận
  chuyển". Kiểm trước bằng `php artisan permission:sync --dry-run`.

### 6.2 Frontend — `pages/transport/valid-delivery-prices/`
Theo `khuon-man-mau` của skill:
- `index.vue` — danh sách (4 list mixin; `V2BaseSmartFilterPanel` **floating**, bộ lọc Mã + Người tạo,
  ô tìm nhanh theo Mã; `columnCustomizationMixin` + `user_column_settings`; `V2BaseDataTable` với
  `@sort` + `:sortBy`/`:sortDirection`; cột "Người tạo"/"Ngày tạo"). Nút **In** + **Gia hạn** ở cột
  Hành động theo điều kiện #2. **Không** nút Thêm mới.
- `_id/index.vue` — Chi tiết read-only: khối thông tin chung (Mã, Công ty, Hiệu lực từ/đến, km) +
  **bảng ma trận** (bọc `V2BaseTableScroll`, thân tuyến tải phân trang) + **tab "Báo giá"** (dùng
  component đính kèm sẵn có — `FileAttachmentTable.vue` / `V2BaseAttachmentSection.vue` /
  `AttachmentGallery.vue`, builder chọn ở Bước 5b, chế độ **read-only**). Trên bảng ma trận có **ô
  "Lọc tuyến đường"** (multi-select `road_ids`, search server-side qua `roadOptions` — §5.6b). Footer:
  nút In + Gia hạn (khớp danh sách).
- **Modal "Gia hạn"** trên `components/modal/V2BaseModal.vue`: 1 ô `V2BaseDatePicker` "Hiệu lực đến",
  select/validate theo chuẩn; gọi `extendDate`. Dùng cho cả list và detail.
- Menu: `components/subsystem-menu/transport.js` dòng 46 — thêm
  `link: '/transport/valid-delivery-prices'` (+ `isShow` theo quyền "Quản lý bảng giá hiệu lực vận
  chuyển"). KHÔNG đổi `label`.
- Số định dạng `1,234,567.89`; nút cụm `mr-2 mb-2`; `.text-muted` đỏ → dùng `#6b7280`; ô rỗng để
  trống (không "—").

### 6.3 Nhãn/UI chuẩn (skill thắng spec)
- Cột/nhãn "Người tạo", "Ngày tạo" (KHÔNG "Người lập/Ngày lập").
- Nút theo `button-convention`; nút chưa dùng được **ẩn bằng `v-if`** (ở đây không có nút thừa).
- Thông báo toast lấy nguyên văn bộ chuẩn QLDA (không tự chế câu).

## 7. Việc để builder tự quyết (minor, sẽ ghi lại khi làm)
- Vị trí chính xác của entity `PriceListValidDeliveryQuotation` (Finance vs Transport) và controller.
- Component đính kèm nào dùng cho tab "Báo giá" (chọn ở Bước 5b đối chiếu ngang màn đã QA).
- Cách phân trang getRoadData cụ thể (per_page, khoá sort) — **đọc ERP `getRoadData` trước khi code**.
- Có tô màu dòng bảng giá đã hết hiệu lực ở danh sách không (mặc định: **không**, chỉ hiện khoảng ngày).
- Tên route/endpoint, tên FormRequest/Resource cụ thể.

## 8. Kích thước & quy trình
- **Dự án có thiết kế viết** (màn list + detail ma trận phân trang + tab đính kèm + in + gia hạn + BE
  + 2 quyền mới). Sau khi anh duyệt `design.md` này → `superpowers:writing-plans` viết `plan.md`, rồi
  thi công theo skill `erp-to-hrm-screen` (6 bước), verify bằng Playwright.
- hrm-client đẩy `develop`; hrm-api theo tiền lệ các màn port trước: **giữ local chờ review** (xác
  nhận lại khi tới bước commit — user quy ước không tự commit/push).

## 9. Câu hỏi còn mở cho user
Đã chốt: phạm vi chỉ-đọc, phân quyền 1 quyền xem show-all, gia hạn Cách B (quyền OR người tạo), tab
Báo giá có, phân trang tuyến (cơ chế ở §5.6), chỗ đặt menu + route.

**Đã chốt thêm (2026-10-28):**
- **Bộ "Lọc tuyến đường" ở màn chi tiết — CÓ port** (user: *"có"*). Thêm endpoint `roadOptions`
  (liệt kê tuyến của bảng giá, search server-side) + UI multi-select, truyền `road_ids` vào
  `getRoadData` (chi tiết §5.6b).

Hiện **không còn câu hỏi phạm vi nào**; các điểm còn lại ở §7 đều là builder-call có mặc định an toàn.
