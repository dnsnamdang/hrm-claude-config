# Report T1 — HRM BE Phase 2c (hrm-api) — 14/10/2026

**Trạng thái: DONE_WITH_CONCERNS** (xem §7 — 2 điểm lệch brief đã tự xử lý, cần caller biết).

Repo `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cdhh-2c-xe` (không merge, không push).

## 1. Commit

| Hash | Nội dung |
|---|---|
| `69a9c148a` | 3 danh mục Biển số xe · Lái xe ngoài (`drives`) · Nhiên liệu (nền `BaseCatalog*`) |
| `7c403c15c` | Danh mục xe (`vehicles`) + sync 2 bảng nối tài xế + 3 endpoint nguồn ô chọn |
| `820a06baa` | Đăng ký: routes, `CatalogHistoryService::TABLES`, `ExportColumnRegistry`, seeder 8 quyền |
| `5779fcac9` | PHPUnit `Modules/MasterData/Tests/Feature/VehicleCatalog2cTest.php` (15 ca) |

`git diff --numstat 3b7dd0f1a..` cho 4 file sửa: chỉ thêm dòng (riêng `Routes/api.php` 1 dòng đổi `use (...)` của closure). Tất cả file LF như file mẫu.

## 2. Quyền (id 1699–1706)

Đã soát trống ở cả 3 nơi trước khi ghi: seeder nhánh này (tới 1675), `origin/gop_db` (tới 1698), DB `hrm_erp_giacty` (max < 100000 là 1678). `uniq -d` id seeder: không thêm trùng mới (danh sách trùng sẵn 7, 8, 16… là cũ).

| id | name |
|---|---|
| 1699 / 1700 | Xem / Quản lý danh mục biển số xe |
| 1701 / 1702 | Xem / Quản lý danh mục lái xe ngoài |
| 1703 / 1704 | Xem / Quản lý danh mục xe |
| 1705 / 1706 | Xem / Quản lý danh mục nhiên liệu |

`guard_name=api`, `group='Danh mục hàng hóa'`, `type=9`. Đã INSERT riêng 8 dòng vào `hrm_erp_giacty` (không chạy seeder).

## 3. Endpoint (prefix `/api/v1/master-data`, middleware `auth:api`)

Cùng khuôn 6 màn xe 2b. `V` = `Quản lý danh mục X|Xem danh mục X`, `M` = `Quản lý danh mục X`.

| Method | Path | Quyền |
|---|---|---|
| GET | `/{slug}/getAll` | chỉ đăng nhập (như 2b) |
| GET | `/{slug}/export` | V |
| GET | `/{slug}` (index phân trang) | V |
| GET | `/{slug}/{id}` | V |
| POST | `/{slug}` | M |
| PUT | `/{slug}/{id}` | M |
| DELETE | `/{slug}/{id}` (xoá thật) | M |
| GET | `/{slug}/{id}/lock` · `/{slug}/{id}/unlock` | M |
| GET | `/vehicles/options/license-plates` · `/vehicles/options/suppliers` · `/vehicles/options/employees` | V (của "xe") |

`slug` ∈ `license-plates` (bảng `license_plates`) · `external-drivers` (bảng **`drives`**) · `fuels` · `vehicles`.
Lịch sử: route chung `GET /api/v1/catalog-histories/{table}/{id}` với `table` = `license_plates` / `drives` / `fuels` / `vehicles` (entity-type FE = đúng tên bảng; `drives`, KHÔNG phải `external_drivers`).
Xuất Excel: khoá màn `ExportColumnRegistry` = tên bảng như trên.

### 3.1 Hình dạng JSON chung
- List: `{code, message, data: [...], links, meta: {current_page, per_page, total, ...}}` (`per_page` mặc định 10).
- Show/store/update: `{code, message, data: {...}}`. Lỗi validate 422: `{code: 422, errors: {field: "câu đầu tiên"}}` — mọi ô báo cùng lúc.
- Mỗi dòng (nền `BaseCatalogResource`): `id, code(null), name, description(null), status (1/0), status_text, created_at, updated_at ("d/m/Y H:i"), creator_name, updater_name, is_can_edit, is_can_delete, is_can_lock`.
- Tham số lọc chung (nền): `name` (like), `status` (0/1), `created_by`, `created_from`, `created_to` (Y-m-d), `keyword`, `sort_by` + `sort_desc=true|false`, `per_page`, `page`.

### 3.2 Biển số xe — `license-plates`
- Trường riêng: `note`.
- Validate: `name` required, max 90, unique trong `status=1`; trùng bản ghi đã khoá ⇒ 422 "Trùng tên với biển số xe đang bị khóa. Hãy mở khóa bản ghi đó thay vì tạo mới" (xem §7.2); `note` ≤ 255.
- Sort: `name, note, status, created_at, updated_at`.

### 3.3 Lái xe ngoài — `external-drivers`
- Trường riêng: `phone, birth_year, id_card, driver_license`.
- Validate: `name` ≤255, `phone` ≤12, `birth_year` regex `/^\d{4}$/`, `id_card` ≤20, `driver_license` ≤20 — đều bắt buộc; không unique. Tạo mới gán `status=1`.
- Lọc thêm: `phone`, `birth_year`, `id_card`, `driver_license` (like). `keyword` tìm tên + SĐT + CCCD.
- `getAll?include_ids[]=` = nguồn ô chọn **lái xe ngoài** cho form xe (trả nguyên dòng `drives` + `is_locked`).

### 3.4 Nhiên liệu — `fuels`
- Trường riêng: `price` (số, float). Validate `name` như biển số (max 90, unique active, báo trùng bản ghi khoá); `price` required numeric 0…99999999999999.99.
- `getAll` = nguồn ô chọn nhiên liệu (lưu ý: getAll trả `price` dạng chuỗi decimal "19500.00" vì là dòng thô).

### 3.5 Danh mục xe — `vehicles`
**Item (list = show):**
```
id, name (= biển số), status, status_text, created_at, updated_at, creator_name, updater_name,
is_can_edit, is_can_delete, is_can_lock,
license_plate_id, license_plate_name, license_plate_locked,
is_tanphat (bool), owner_type_text ("Xe Tân Phát" | "Xe nhà cung cấp"), owner_name (cột "Chủ xe"),
owner (customers.id, null nếu Tân Phát), supplier_code, supplier_name, supplier_locked,
company_id, company_name, department_id, department_name (null nếu xe NCC),
vehicle_manufact_id/_name/_locked, vehicle_brand_id/_name/_locked, vehicle_model_id/_name/_locked,
vehicle_payload_id/_name/_locked, vehicle_category_id/_name/_locked, fuel_id/_name/_locked,
driver_type (1|2), driver_type_text, driver_names ("A, B"),
drivers: [{id (drives.id), name, phone, is_locked}], driver_ids: [..],
company_drivers: [{id (employee_infos.id), code, name, phone, is_locked}], company_driver_ids: [..]
```
(`drivers` chỉ có khi `driver_type=1`, `company_drivers` chỉ có khi `=2` — loại kia trả `[]`.)

**Lọc index:** `license_plate` (like tên biển số), `owner` (like tên công ty khi Tân Phát / tên hoặc mã NCC khi xe NCC), `license_plate_id`, `owner_id`, `company_id`, `department_id`, `vehicle_manufact_id`, `vehicle_brand_id`, `vehicle_model_id`, `vehicle_payload_id`, `vehicle_category_id`, `fuel_id`, `driver_type` (1 giá trị hoặc mảng), `is_tanphat` (0/1/true/false), `driver` (like tên tài xế), `status`, `created_by` (1 hoặc mảng), `created_from`, `created_to`, `keyword` (biển số + tên chủ xe). Sort: `license_plate` (= `name`), `status`, `is_tanphat`, `driver_type`, `created_at`, `updated_at`.

**Payload store/update:**
```
license_plate_id, vehicle_manufact_id, vehicle_brand_id, vehicle_model_id, vehicle_payload_id,
vehicle_category_id, fuel_id, is_tanphat (bool | "true"/"false" | 1/0),
company_id + department_id (khi is_tanphat) | owner (customers.id, khi NCC),
driver_type (1|2), drivers: [drives.id] (khi 1) | company_drivers: [employee_infos.id] (khi 2), status? (0/1)
```
Luật: biển số không trùng xe đang hoạt động khác (bỏ chính nó khi sửa); Loại ∈ Hãng, Model ∈ Loại + Hãng; Bộ phận ∈ Công ty; danh mục (biển số, hãng, loại, model, tải trọng, dòng, nhiên liệu, lái xe ngoài) phải đang hoạt động khi chọn mới, được giữ giá trị cũ dù đã khoá khi sửa. Ô của loại chủ xe / loại tài xế KHÔNG chọn không bị validate; service ghi null (owner hoặc company+department) và xoá sạch bảng nối của loại tài xế kia.
Lỗi mảng tài xế trả theo khoá `drivers.0`, `company_drivers.1`…

**Xoá:** chặn (400 "Không thể xóa do dữ liệu đang được sử dụng.") khi `vehicle_id` có ở `delivery_trips`, `other_delivery_trips`, `activity_has_delivery_trips`, `activity_has_other_delivery_trips`, `activity_has_delivery_trip_accounting`, `activity_has_other_delivery_trip_accounting`; xoá được thì xoá kèm `vehicle_drivers` + `vehicle_company_drivers`. Khoá luôn được. **Mở khoá** bị chặn (400) khi biển số đang gắn xe khác đang hoạt động.

**getAll:** `[{id, license_plate_id, is_tanphat, status, name (biển số), is_locked}]`, nhận `include_ids`.

### 3.6 Nguồn ô chọn cho form xe (FE T2 dùng)
| Ô | Endpoint | id trả về là |
|---|---|---|
| Biển số | `GET /vehicles/options/license-plates?vehicle_id=<xe đang sửa>&include_ids[]=<biển đang lưu>&keyword=` → `[{id, name, status, is_locked}]` — biển đang hoạt động chưa gắn xe hoạt động khác | `license_plates.id` |
| NCC (chủ xe ngoài) | `GET /vehicles/options/suppliers?keyword=&include_ids[]=` → `[{id, code, fullname, name ("MÃ - Tên"), status, is_locked}]`, tối đa 30 | **`customers.id`** (`is_supplier=1`) |
| Tài xế công ty | `GET /vehicles/options/employees?keyword=&company_id=&include_ids[]=` → `[{id, code, fullname, telephone, company_id, department_id, department_code, name ("MÃ PHÒNG - Tên"), status, is_locked}]`, tối đa 50 | **`employee_infos.id`** |
| Lái xe ngoài | `GET /external-drivers/getAll?include_ids[]=` | `drives.id` |
| Nhiên liệu | `GET /fuels/getAll` | `fuels.id` |
| Hãng / Loại / Model / Tải trọng / Dòng xe | `GET /vehicle-manufacts|vehicle-brands|vehicle-models|vehicle-payloads|vehicle-categories/getAll` (2b — trả toàn bộ dòng active kèm `vehicle_manufact_id` / `vehicle_brand_id`, **không lọc theo cha ở server** ⇒ FE lọc dây chuyền phía client) | id bảng tương ứng |
| Công ty / Bộ phận | Dùng sẵn có: store user-profile hoặc `GET /api/v1/org-options?type=company` / `?type=department` (department có `company_id`) | `companies.id` / `departments.id` |

⚠️ KHÔNG dùng `org-options?type=employee` cho tài xế công ty: endpoint đó trả `employees.id`, bảng nối cần `employee_infos.id`.

## 4. PHPUnit

- File mới: 15 ca / 152 assertion — xanh. Gồm: gate 2 chiều (không quyền 403 ở 4 màn + 3 options + ghi; quyền Xem chỉ đọc, Quản lý mới ghi, quyền màn này không mở màn khác), CRUD + khoá/mở khoá/xoá + ghi lịch sử, unique active + bản ghi khoá trùng tên, chặn xoá khi có tham chiếu (biển số, lái xe, nhiên liệu, xe có chuyến giao hàng), báo lỗi đồng thời, cha–con sai ⇒ 422, bộ phận khác công ty ⇒ 422, sync bảng nối khi đổi `driver_type`, xe NCC không bị tự điền công ty (cả lúc khoá), biển số trùng xe đang hoạt động + chặn mở khoá trùng, lọc danh sách. Toàn bộ trong `DatabaseTransactions`, quyền qua role tạm.
- Đã thử đột biến: tắt hook chống tự điền công ty ⇒ ca `xe_ncc_…` đỏ ("Failed asserting that 1 is null") ⇒ ca có giá trị thật.
- **Cả bộ MasterData: 526/526 OK** (4523 assertion, 4 phút 07). ⚠️ Mốc brief ghi 332/332 — số đo thực tế trước khi thêm file của tôi là 526 − 15 = **511** (không phải 332); không có ca nào đỏ.
- Trước khi chạy: `bootstrap/cache/config.php` không tồn tại; đã `config:clear`.

## 5. Kiểm tay curl (cổng 8031, JWT employee 1180)

- Trước khi cấp quyền: 4 màn đều **403** (fail-closed); `vehicle-payloads` 200.
- Cấp role tạm `TMP-2C-CURL` (id 120114, công ty 1) với 8 quyền ⇒ index:
  - `license-plates?status=1` total **161**, không lọc 163 ✔
  - `external-drivers?status=1` total **69**, không lọc 72 ✔
  - `vehicles?status=1` total **134**, không lọc 137 ✔
  - `fuels` total **4** ✔
- Thêm: show `vehicles/137`, `export` (xlsx 94.9KB), 3 options, getAll 3 màn, lọc `owner` / `license_plate` / `vehicle_manufact_id+driver_type` / `driver`, `external-drivers?keyword=0865` (19 dòng = đúng số đo SQL).
- Đã gỡ role tạm + `cache:forget spatie.permission.cache`; gọi lại ⇒ 403.

## 6. Số dòng bảng sau khi xong (đúng mốc)

`license_plates` 163 · `drives` 72 · `vehicles` 137 · `fuels` 4 · `vehicle_drivers` 110 · `vehicle_company_drivers` 74 · `catalog_histories` của 4 bảng: 0 · role `PR-ROLE-%`/`TMP-2C-CURL`: 0 · NV test "Product Read Tester": 0.

## 7. Lệch brief / lo ngại

1. **`owner` KHÔNG trỏ `suppliers`** như brief ghi: bảng `suppliers` trên DB gộp có **0 dòng**; ERP `App\Model\Sale\Supplier` dùng `$table = "customers"` + `is_supplier = 1`. Đo: 121/121 `vehicles.owner` khớp `customers` (`is_supplier=1`), 0 khớp `suppliers`. Đã làm theo dữ liệu thật: model `Modules\Finance\Entities\Supplier` (bảng `customers`, global scope `is_supplier`), tên NCC = `customers.fullname`.
2. **Unique index ở DB trên `license_plates.name` và `fuels.name`** ⇒ yêu cầu "tên đã khoá thì tạo lại được" **không làm được** nếu không có migration gỡ index (phạm vi 2c không có migration). Đã thêm rule báo 422 dễ hiểu ("…đang bị khóa. Hãy mở khóa bản ghi đó thay vì tạo mới") thay vì để INSERT nổ SQLSTATE[23000]; test chốt hành vi này. Nếu muốn đúng nghĩa "tạo lại được" cần quyết định migration gỡ 2 index (ERP cũng đang validate unique toàn bảng nên không vỡ ERP).
3. **Bẫy `BaseModel` tự điền `company_id`/`department_id`** theo người đăng nhập (hook creating/saving) — xe NCC sẽ bị gắn công ty. Đã chặn trong `Vehicle::booted()`: lưu từ form ⇒ theo luật (Tân Phát bỏ `owner`, NCC bỏ công ty/bộ phận); lưu khác (khoá/mở khoá) ⇒ trả lại giá trị gốc, không sửa dữ liệu ERP cũ. Hệ quả: lưu form ở HRM sẽ dọn 10 xe Tân Phát đang dính `owner` cũ và 1 xe NCC đang có `company_id` — đúng brief nhưng là đổi dữ liệu ERP khi người dùng bấm Lưu.
4. Danh mục xe: 2 xe đang hoạt động dùng chung 1 biển số (dữ liệu cũ) — không dọn; sửa 1 trong 2 xe sẽ bị 422 biển số cho tới khi đổi biển/khoá xe kia.

## 8. Vấn đề ngoài luồng (ghi nhận, không vá)

- **N-a** 2b `vehicle_manufacts` cũng có unique index `vehicle_manufacts_name_unique` ⇒ tạo hãng xe trùng tên một hãng đã khoá: validate cho qua, INSERT nổ SQL, controller trả 400 kèm nguyên câu SQL. Cùng bệnh §7.2, chưa có rule báo rõ.
- **N-b** Quyền 6 màn xe 2b trên DB `hrm_erp_giacty` mang id **1620–1631**, trong khi seeder ghi **1640–1651** (đã dời khi gộp gop_db) — lệch id DB ↔ seeder (tên khớp nên gate vẫn chạy).
- **N-c** `php artisan route:list` nổ sẵn (`RequestUpdateTimeSheetController::__construct` gọi `isCurrentEmployeeHasPermission` khi chưa đăng nhập) — không liên quan 2c.
- **N-d** `delivery_payment_request_details.license_plate` / `other_delivery_payment_request_details.license_plate` là varchar chép TÊN biển số (không phải FK) — không tính vào chặn xoá; đổi tên biển số ở HRM không cập nhật các chứng từ này (giống ERP).
- **N-e** `getAll` của nhóm xe (cả 2b lẫn 2c) không gate quyền, chỉ cần đăng nhập — giữ khuôn 2b.
- **N-f** Seeder quyền có sẵn nhiều id trùng (7, 8, 16–19, 21, 91, 94, 95, 102, 106, 110, 114, 161, 394, 411) ở cả nhánh này lẫn `origin/gop_db` — có từ trước.
- N102 (Công tác lọc biển số xe công ty không xét `vehicles.status`) — đã ghi ở khảo sát, không đụng.
