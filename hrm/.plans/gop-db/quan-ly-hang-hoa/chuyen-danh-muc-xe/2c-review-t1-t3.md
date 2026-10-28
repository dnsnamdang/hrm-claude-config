# Review Phase 2c — T1 (hrm-api) + T3 (ERP) — 14/10/2026

> Chỉ đọc. Soát: hrm-api 4 commit `69a9c148a 7c403c15c 820a06baa 5779fcac9` (nhánh `feat/cdhh-2c-xe`), ERP `4c553e300a` (nhánh `feat/cdhh-2c-xe-erp`).
> Đối chiếu bằng SELECT trên `hrm_erp_giacty` + `git show` các nhánh `origin/gop_db`, `origin/develop`. (Có chạy `git fetch origin gop_db` để cập nhật ref so sánh — không đổi working tree.)

**Tổng: Critical 1 · Important 3 · Minor 9.**

---

## Critical

### C1. Id quyền 1699–1706 TRÙNG với `origin/develop`
- File: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (khối thêm ở dòng ~1572–1581 nhánh `feat/cdhh-2c-xe`).
- T1 chỉ soát 3 nơi (seeder nhánh, `origin/gop_db` max 1698, DB local). Bỏ sót `origin/develop`: commit `687f1825d` (12/10, khoipv — "Phiếu yêu cầu hạch toán mua dịch vụ") đã chiếm **1699–1705** ("Xem yêu cầu hạch toán mua dịch vụ - theo tổng công ty"…), và **1706** = "Cấu hình chặn luồng hàng quá hạn"; develop đang tới **1708**.
- `develop` và `gop_db` dùng chung dải 1680–1698 (giống hệt từng dòng) ⇒ 2 nhánh anh em cùng chảy về prod. Seeder là file phẳng, 2 khối chèn ở vị trí khác nhau ⇒ git KHÔNG báo xung đột khi merge (đúng bẫy memory "Trùng id quyền khi merge nhánh dài").
- Kịch bản lỗi: merge develop ↔ gop_db/nhánh chung ⇒ seeder có 2 `Permission::create` cùng id ⇒ chạy seeder nổ duplicate PK; hoặc chèn quyền bằng INSERT riêng lên prod (nếu develop đã deploy thì 1699–1706 đã là quyền hạch toán) ⇒ INSERT lỗi, hoặc tệ hơn nếu dùng upsert/sửa tay: route HRM gate "Xem danh mục xe" theo TÊN nên không khớp id, nhưng role gán theo id sẽ cấp nhầm quyền hạch toán / chặn luồng hàng cho người quản lý danh mục xe.
- DB local `hrm_erp_giacty` đã INSERT 1699–1706 với tên 2c ⇒ khi nhánh develop/gop_db mới hơn chạy vào cùng DB sẽ va PK.
- Sửa: lấy dải trống trên max của MỌI nhánh remote (≥ 1709, kiểm `git for-each-ref refs/remotes` + `uniq -d`), sửa seeder + đổi id 8 dòng ở DB local (role_has_permissions hiện 0 dòng nên đổi an toàn).

---

## Important

### I1. `external-drivers/getAll` không gate quyền nhưng trả đủ CCCD / SĐT / bằng lái / năm sinh
- `hrm-api/Modules/MasterData/Routes/api.php:177` (`Route::get('/getAll', …)` không middleware, khuôn 2b) + `Services/ProductClassification/BaseCatalogService.php:184-191` (`$model::query()` không `select` ⇒ trả nguyên dòng `drives`).
- Kịch bản: bất kỳ NV đăng nhập HRM (không có quyền nào về xe) gọi `GET /api/v1/master-data/external-drivers/getAll?include_ids[]=…` ⇒ nhận `phone, id_card, driver_license, birth_year` của 69 lái xe (thêm bản đã khoá qua `include_ids`). Danh mục 2b không có dữ liệu cá nhân nên khuôn "getAll chỉ cần đăng nhập" (N-e) không còn vô hại ở đây.
- Kèm: route chung `GET /api/v1/catalog-histories/drives/{id}` cũng không gate (N64 đã biết) ⇒ đăng ký bảng `drives` vào `CatalogHistoryService::TABLES` (`app/Services/CatalogHistoryService.php` khối +715) mở thêm đường đọc diff CCCD/SĐT cũ ↔ mới.
- Sửa: override `getAll()` ở `ExternalDriverService` chỉ `select id, name, phone?, status` (form xe chỉ cần id + tên), hoặc gate getAll bằng quyền Xem lái xe ngoài | Quản lý danh mục xe; history của `drives` đi endpoint có gate.

### I2. T3 (ERP) chưa kiểm bằng Playwright — vi phạm quy tắc root "Task sửa FE phải kiểm bằng Playwright"
- T3 sửa 10 blade index + menu (`resources/views/common/*/index.blade.php`, `layouts/topmenubar.blade.php`) nhưng report tự ghi "Chưa kiểm bằng Playwright". Test PHPUnit chỉ chứng minh HTTP 200 + JSON không còn key `action`, không chứng minh DataTables render đúng.
- Bằng chứng là có lỗi thật lọt (xem M7: 6 màn lệch hàng tìm kiếm do chính T3 gây ra, report lại ghi "vốn lệch có sẵn").
- Cần 1 lượt Playwright: mở 10 màn, đo số `th` 2 hàng tiêu đề = số cột, không lỗi console, 0 nút Thêm/Sửa/Xoá; mở menu Xe đếm 9 link HRM + 1 link Nhiên liệu.

### I3. Deploy: ERP khoá ghi cùng lúc HRM chưa ai có quyền ⇒ mất hẳn đường sửa danh mục xe
- DB: `role_has_permissions` cho 8 quyền mới = **0 dòng**; ERP sau T3 chặn ghi cả 10 màn (35 route). 4 màn 2c ở ERP trước đây KHÔNG gate (ai đăng nhập cũng sửa được) hoặc gate bằng quyền ERP `Quản lý loại nhiên liệu` (id 100138), `Quản lý dòng xe`, `Quản lý trọng tải xe`.
- Kịch bản: deploy xong, nhân viên vận chuyển cần thêm biển số / xe mới cho chuyến giao hàng ⇒ ERP báo "đã chuyển sang HRM", HRM trả 403 ⇒ không ai tạo được xe cho tới khi admin gán quyền tay.
- Plan chỉ ghi "deploy phải gán quyền", chưa có danh sách người/role cần gán hay script. Cần: bảng ánh xạ quyền ERP → HRM (100138 → 1705/1706 mới…, người đang thao tác 3 màn không gate lấy từ `created_by/updated_by` gần đây của `license_plates`/`drives`/`vehicles`) và đưa vào checklist deploy trước khi bật middleware ERP.

---

## Minor

### M1. Lịch sử giá nhiên liệu làm tròn mất phần thập phân
`hrm-api/Modules/MasterData/Services/Vehicle/FuelService.php:68-72` — `number_format((float)$value, 0, ',', '.')`. Cột là decimal(16,2), validate cho phép 2 số lẻ ⇒ sửa 19500.40 → 19500.45 log ra "19.500 → 19.500" (dòng lịch sử vô nghĩa), 19500.5 hiện "19.501". Dùng 2 số lẻ khi có phần lẻ.

### M2. Lái xe ngoài: kiểm độ dài TRƯỚC khi cắt khoảng trắng
`Http/Requests/Vehicle/ExternalDriverRequest.php:39-48` kiểm `phone max:12`, `id_card/driver_license max:20`, `birth_year regex` trên giá trị thô; `ExternalDriverService::fillableFrom()` (dòng 89-98) mới `trim`. Gõ "0912345678 " (dấu cách cuối, hay gặp khi dán) vẫn qua; " 1990" bị báo sai "Năm sinh phải gồm đúng 4 chữ số". Nền chỉ trim `name`/`code` (`BaseCatalogRequest::prepareForValidation`). Thêm trim cho 4 ô ở `prepareForValidation`.

### M3. Mở khoá xe không xét biển số / danh mục đang khoá
`Http/Controllers/V1/Vehicle/VehicleController.php:79-95` chỉ chặn trùng biển với xe hoạt động khác; `Vehicle` không có `parentCatalog()` ⇒ `isCanUnlock()` luôn true. Kịch bản: khoá biển số X, sau đó mở khoá xe đang gắn X ⇒ ERP `Vehicle::getVehicles…` (lọc `vehicles.status=1`) đưa xe có biển đã khoá vào ô chọn chuyến giao hàng. Cân nhắc chặn khi biển số đang khoá (ít nhất biển số, vì là "tên" của xe).

### M4. `options/employees` mở cho quyền XEM, trả SĐT nhân viên mọi công ty
`Routes/api.php:178-187` gate `Quản lý|Xem danh mục xe`; `VehicleService::employeeOptions()` (dòng 495-543) không giới hạn công ty khi không truyền `company_id`, trả `telephone`. Người chỉ có quyền Xem không cần nguồn ô chọn của form. Gate 3 route `options/*` bằng quyền Quản lý.

### M5. `company_drivers[]` chỉ kiểm tồn tại
`VehicleRequest.php:162-172` không kiểm nhân viên đang làm việc (`employee_infos.status`) — chọn mới NV đã nghỉ (gửi id thẳng API) vẫn qua, khác luật "chọn mới phải đang hoạt động" áp cho lái xe ngoài ngay phía trên.

### M6. Unique tên biển số / nhiên liệu: lệch design §2.3 do unique index DB — cần user chốt
`license_plates_name_unique`, `fuels_name_unique` có thật (đã SHOW INDEX). T1 xử lý hợp lý bằng rule 422 "Hãy mở khóa bản ghi đó" (`Requests/Vehicle/Concerns/ChecksLockedNameIndex.php`), nhưng yêu cầu "tên đã khoá thì tạo lại được" của plan KHÔNG đạt. Ghi vào câu hỏi tồn (giữ hành vi hiện tại hay migration gỡ index — ERP validate unique toàn bảng nên gỡ index không vỡ ERP). Cùng bệnh N-a (`vehicle_manufacts_name_unique` của 2b trả nguyên câu SQL).

### M7. ERP: T3 làm lệch hàng tìm kiếm ở 6 màn (report ghi nhầm là "có sẵn")
Đếm `<th>` hàng tiêu đề / hàng `thead.search-column` (trước → sau T3):
| Màn | Trước | Sau |
|---|---|---|
| drives | 5/5 | **4/5** |
| fuels | 9/9 | **8/9** |
| vehicle_categories | 8/8 | **7/8** |
| vehicle_models | 10/10 | **9/10** |
| vehicle_payloads | 8/8 | **7/8** |
| vehicles | 11/11 | **10/11** |
| license_plates · vehicle_manufacts | 9/7 | 8/7 (lệch sẵn, nay bớt) |
| vehicle_brands | 10/9 | 9/9 (nay khớp) |
T3 bỏ `<th>Hành động</th>` ở hàng 1 nhưng không bỏ ô trống tương ứng ở hàng tìm kiếm ⇒ hàng tìm kiếm thừa 1 ô cuối, lòi ra ngoài bảng. Không vỡ JS (lọc theo `th:eq(index)`, ô thừa nằm cuối). Sửa: xoá `<th></th>` cuối của `thead.search-column` ở 6 file trên.

### M8. ERP: code chết còn lại
Modal sửa + handler `.edit` (`$.post('/admin/…/{id}')`) vẫn nằm trong 9 index; 8 partial `resources/views/partials/sale/create{Drive,Fuel,LicensePlate,VehicleBrand,VehicleCategory,VehicleManufact,VehicleModel,VehiclePayload}.blade.php` nay không còn chỗ include. Không có nút kích hoạt nên vô hại; ghi để dọn khi gỡ hẳn màn ERP.

### M9. Dữ liệu cũ sẽ bị "dọn" khi bấm Lưu ở HRM — cần biết trước
- 10 xe Tân Phát (id 1,2,3,60,61,64,66,67,71,109) còn `owner` (620 / 1788); 1 xe NCC có `company_id`. Lưu form HRM ghi null (`VehicleService::fillableFrom()` dòng 276-295 + hook `Vehicle::booted()`). Đã soát ERP: `owner` chỉ được đọc khi `is_tanphat=0` (`App\Model\Common\Vehicle::getRoads/getRoadInfo`) ⇒ không đổi kết quả vận chuyển. OK nhưng nên ghi vào HDSD/ghi chú deploy.
- 1 xe NCC đang thiếu `owner` ⇒ sửa ở HRM bị bắt chọn NCC.
- Biển `37C-144.40` gắn 2 xe đang hoạt động ⇒ sửa 1 trong 2 xe sẽ 422 (đã nêu ở report §7.4).

---

## Đã soát — đạt
- **Gate HRM fail-closed**: mọi route của 4 slug có `checkPermission` (index/show/export: Xem|Quản lý; store/update/delete/lock/unlock: Quản lý; options: Xem|Quản lý). Ngoại lệ duy nhất `getAll` (xem I1). Tên quyền trong route = tên trong seeder/DB (ghép `'Xem danh mục ' . $label`).
- **childrenCount đủ bảng** (đối chiếu information_schema mọi cột `*license_plate*`, `*driver*`, `*vehicle_id*`, `*fuel*`):
  - `license_plate_id`: 7/7 bảng (vehicles, delivery_trips, other_delivery_trips, 4 bảng assign/payment) — đủ. `*.license_plate(s)` varchar là bản chép tên, không phải FK.
  - `driver_id`: 9/9 (vehicle_drivers + 8 bảng chuyến/hạch toán/đề nghị TT) — đủ. `company_driver_id` trỏ nhân viên, không liên quan.
  - `vehicle_id`: 6 bảng chứng từ + 2 bảng nối (xoá kèm) — đủ; `*_payment_request_details` không có `vehicle_id`.
  - `fuel_id`: chỉ `vehicles` — đủ. FK DB (`vehicles_*_foreign`, `vehicle_drivers_driver_id_foreign`) là lưới an toàn thứ 2.
- **Validate xe**: Loại ∈ Hãng, Model ∈ Loại+Hãng, Bộ phận ∈ Công ty, danh mục khoá chỉ giữ được giá trị cũ (`ChecksParentCatalog`), sửa bản ghi khoá bị chặn ở `respondUpdate` (isCanEdit). Dữ liệu thật: 0 xe vi phạm luật cha–con mới (đo SQL) ⇒ không xe cũ nào bị kẹt 422 vì luật mới, trừ M9.
- **Sync bảng nối**: theo `driver_type`, xoá loại kia; cả store/update/delete trong `DB::transaction` của `BaseCatalogController`. Bảng nối có `created_at/updated_at` ⇒ `withTimestamps()` đúng.
- **Hook BaseModel tự điền công ty**: thứ tự listener đúng (BaseModel đăng ký ở `boot()`, Vehicle ở `booted()` ⇒ chạy sau, cả `saving` lẫn `creating`).
- **N+1 danh sách xe**: eager load 10 quan hệ + 2 belongsToMany, cờ `children_exists` bằng EXISTS, creator/updater bằng subquery.
- **Lọc index**: đủ tham số brief; `owner` xét theo `is_tanphat`; LIKE đã escape.
- **Export / history**: khoá `license_plates`, `drives`, `fuels`, `vehicles` khớp `exportScreen()` của 4 controller và `table()` của service.
- **ERP chặn ghi**: 35 route ghi của 10 nhóm đều có `productMovedToHrm:<khoá>`; không còn route ghi nào khác trỏ 10 controller (grep `routes/*`); không controller/khác ghi vào 12 bảng (grep `::create/new/->insert/->update/->delete`; 2 lớp import chỉ đi qua route đã chặn). Route đọc giữ: index, searchData, `vehicleManufact.brands`, `vehicle.getRoadInfo` — không màn ngoài 10 index gọi route ghi; `brands` chỉ partial createVehicleModel (nay không include) gọi.
- **searchData bỏ `action`**: cả 10 blade đã bỏ `{data:'action'}` khỏi `columns` (0 tham chiếu `action` còn lại ngoài `<form action="#">`) ⇒ DataTables không lệch index cột. Lỗi duy nhất là hàng tìm kiếm (M7).
- Đường HRM trong `TARGETS` + menu khớp thư mục `hrm-client/pages/master-data/{vehicle-*,license-plates,external-drivers,vehicles,fuels}`.
- Số dòng DB hiện tại đúng mốc: license_plates 163 · drives 72 · vehicles 137 · fuels 4 · vehicle_drivers 110 · vehicle_company_drivers 74.
