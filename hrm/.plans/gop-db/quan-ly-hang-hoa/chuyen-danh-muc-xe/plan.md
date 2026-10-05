# Phase 2b — Kế hoạch thực thi

> Spec: `design.md` cùng thư mục. Nhánh `feat/p1-danh-muc-hang-hoa` (cả 2 repo).
> Khuôn bám theo **Phase 1** (`../chuyen-danh-muc-lien-quan/`), mẫu gần nhất là màn **Đơn vị tính**
> (`units` — cũng là bảng ERP không cột `code`) và màn **Loại sản phẩm** (mẫu danh mục CÓ cha).
> ⚠️ Không copy màn vừa làm gần nhất làm khuôn — khuôn chuẩn là màn Danh mục khách hàng / Phase 1.

## Đợt A — Nền & dữ liệu (4 task)

### A1. Migration thêm `status` cho `vehicle_life`
- [ ] `Modules/MasterData/Database/Migrations/2026_09_23_000001_add_status_to_vehicle_life_table.php`
- [ ] `$table->tinyInteger('status')->default(1)->after('name');` + docblock nêu 3 điều:
      bảng ERP dùng chung · ERP `store()` không gán `status` nên sống nhờ default ·
      `VehicleLife::searchByFilter()`/`getForSelect()` bên ERP KHÔNG lọc status (hệ quả đã biết)
- [ ] `down()` `dropColumn('status')`
- [ ] Chạy `migrate`, đo lại: `vehicle_life` vẫn **61 dòng**, 61/61 có `status = 1`

### A2. Dọn 1 cặp Model xe trùng trong cùng cha
- [ ] Tìm đúng cặp: `GROUP BY vehicle_manufact_id, vehicle_brand_id, name HAVING COUNT(*) > 1`
- [ ] Xem 2 id đó có bị tham chiếu không (`productables`, `product_vehicle_model_has_life`,
      `vehicles`, và mọi bảng có `model_id`) **trước khi** động vào
- [ ] Không tham chiếu → khoá bản trùng (`status = 0`), KHÔNG xoá. Có tham chiếu → đổi tên
      cho phân biệt. Ghi lại quyết định + id vào `plan.md` mục "Nhật ký"
- [ ] Đo lại: trùng-trong-cùng-cha = **0**

### A3. 4 Entity
- [ ] `Modules/MasterData/Entities/Vehicle/VehicleManufact.php`, `VehicleBrand.php`,
      `VehicleModel.php`, `VehicleLife.php` — `extends BaseCatalogModel`
- [ ] ⚠️ Thư mục `Entities/Vehicle/` **đã có 3 file read-only** do Phase 2 tạo
      (`cf5c489a9`) cho tab "Phân loại xe". **Nâng cấp 3 file đó**, KHÔNG tạo bản thứ hai —
      2 model cùng trỏ 1 bảng là nguồn lệch kinh điển. Kiểm mọi chỗ đang `use` chúng trước khi sửa
- [ ] Mỗi file: `STATUS_ACTIVE = 1` / `STATUS_INACTIVE = 0`, `$table`, `$fillable`,
      `childrenCount()` / `activeChildrenCount()` theo bảng ở `design.md` §2.6
- [ ] `VehicleBrand::parentCatalog()` → Hãng xe; `VehicleModel::parentCatalog()` → Loại xe
- [ ] Đếm `productables` **kẹp `productable_type`** bằng hằng của
      `Entities/Product/Productable.php`, không viết lại chuỗi
- [ ] Docblock `VehicleBrand`: nhắc 3 tên gọi + khác `brands` của Phase 1

### A4. Chốt số mốc trước khi code tiếp
- [ ] Ghi vào "Nhật ký": 4 bảng 56 / 322 / 1.281 / 61 · `productables` theo từng
      `productable_type` (13.165 / 12 / 6 / 3.968 / 28.398) · `product_vehicle_model_has_life` 48.736
- [ ] Đây là mốc đối chiếu ở Đợt D — không có mốc thì không chứng minh được "không làm rác dữ liệu"

## Đợt B — Backend (5 task)

### B1. 4 Service
- [ ] `Modules/MasterData/Services/Vehicle/{VehicleManufact,VehicleBrand,VehicleModel,VehicleLife}Service.php`
      `extends BaseCatalogService`
- [ ] Cả 4: `hasCodeField()` → **false**; `hasDescriptionField()` → false (dùng `note`)
- [ ] `fillableFrom()`: Hãng xe `name, note, status` · Loại xe thêm `vehicle_manufact_id` ·
      Model xe thêm `vehicle_manufact_id + vehicle_brand_id` · Đời xe chỉ `name, status`
- [ ] `applyOwnFilters()`: Loại xe lọc theo `vehicle_manufact_id`; Model xe lọc theo cả 2 cấp
      (cấp ông qua cột thẳng trên bảng, không cần `whereHas`)
- [ ] `sortableColumns()` + `catalogColumns()` + `catalogDisplay()` (cột cha → `parentName()`)
- [ ] `listRelations()`: Loại xe `manufact:id,name,status`; Model xe thêm `brand:id,name,status`

### B2. 4 Request
- [ ] `Http/Requests/Vehicle/*Request.php` `extends BaseCatalogRequest`
- [ ] `hasCodeField()` **false** (chỗ thứ 2 — quên là validate đòi mã ở bảng không có cột mã)
- [ ] `statusRule()` → `['nullable', 'in:0,1']`
- [ ] Unique theo `design.md` §2.3 — **bỏ qua chính bản ghi đang sửa**
- [ ] `name`: `required|max:90` (bám đúng ERP, không nới thành 255) · `note`: `nullable|max:255`
- [ ] Loại xe / Model xe: cha `required` + `parentRule()` của `ChecksParentCatalog`
- [ ] Model xe: kiểm **Loại xe phải thuộc đúng Hãng xe đã chọn** — ERP không kiểm, gửi cặp lệch là
      ghi xuống dữ liệu mâu thuẫn mà không báo gì

### B3. 4 Resource + 4 Controller
- [ ] `Transformers/Vehicle/*Resource.php` `extends BaseCatalogResource`, `ownFields()` trả
      `note`, tên cha (`manufact_name` / `brand_name`), id cha cho form sửa
- [ ] `Http/Controllers/V1/Vehicle/*Controller.php` `extends BaseCatalogController`:
      `resourceClass()` · `catalogLabel()` · `exportScreen()` · `exportFileName()` + 6 method
      type-hint đúng Entity
- [ ] ⚠️ Kiểm lại docblock từng file — Phase 1 có file ghi nhầm nhãn màn khác do copy

### B4. Sáu điểm đăng ký (`design.md` §3)
- [ ] `Routes/api.php`: 4 dòng vào `$erpCatalogs`. **KHÔNG khai route import** (đợt này không làm)
- [ ] `CatalogHistoryService::TABLES`: 4 mục, cột đúng tên tiếng Việt của màn
- [ ] `ExportColumnRegistry`: 4 mục, có `status_text` / `creator_name` / `created_at` / `updater_name` / `updated_at`
- [ ] `PermissionsTableSeeder`: 8 quyền, `group = 'Danh mục hàng hóa'`, `type = 9`, `guard_name = 'api'`.
      **Lấy lại max id ngay trước khi commit**, rồi `uniq -d` kiểm trùng id toàn file
- [ ] Cấp 8 quyền cho role đang test bằng SQL → **xoá cache spatie** (không xoá là chạy lẻ xanh,
      chạy cả bộ 403)

### B5. Kiểm API thật, không qua test
- [ ] Mint JWT bằng tinker, `curl` đủ 6 đường của **cả 4 màn**: index · show · store · update ·
      lock/unlock · delete
- [ ] Đo **số query** của index (bật `DB::listen` **một lần, ngoài vòng lặp** — đăng ký trong vòng
      lặp là mọi closure cùng đẩy vào 1 biến, ra số gấp bội)
- [ ] Ép các nhánh lỗi: unique trùng theo cha · Loại xe không thuộc Hãng xe · xoá bản ghi có
      tham chiếu (phải chặn) · khoá rồi sửa (phải 423)
- [ ] Đếm lại 4 bảng: khớp mốc A4, 0 dòng rác

## Đợt C — Frontend (5 task)

### C1. Màn Hãng xe — dựng khuôn cho 3 màn sau
- [ ] `pages/master-data/vehicle-manufacts/index.vue` + `AddVehicleManufactModal.vue`,
      copy khuôn từ `pages/master-data/units/`
- [ ] Đổi **hết**: đường API · `localStorageKey` · `columnScreenKey` · `entity-type` của popup
      lịch sử · tên quyền · nhãn màn · tên component trong thẻ kebab
- [ ] Cột: STT · Hãng xe · Ghi chú · Người tạo · Ngày tạo · Trạng thái · Hành động
- [ ] Lọc: Tên · Trạng thái · Người tạo · Ngày tạo từ–đến. `V2BaseSmartFilterPanel` + `floating`
- [ ] Grep tự kiểm của skill `erp-to-hrm-screen` phải **sạch** trên thư mục màn

### C2. Màn Loại xe
- [ ] Như C1, thêm cột **Hãng xe** + ô lọc Hãng xe; form có ô chọn Hãng xe (bắt buộc)
- [ ] Ô chọn chỉ liệt kê Hãng xe **đang hoạt động**, nhưng màn Sửa vẫn hiện đúng hãng đã khoá (🔒)

### C3. Màn Model xe
- [ ] Thêm 2 cột + 2 ô lọc (Hãng xe, Loại xe)
- [ ] **Lọc dây chuyền**: đổi Hãng xe thì ô Loại xe co lại đúng tập con **và** xoá giá trị cũ nếu
      không còn hợp lệ — cả ở bộ lọc lẫn trong form
- [ ] Đo bằng DOM: số option của ô Loại xe trước / sau khi chọn Hãng xe

### C4. Màn Đời xe
- [ ] Màn đơn giản nhất: chỉ `name` + trạng thái. Không có ô Ghi chú (bảng không có cột)
- [ ] Sắp xếp mặc định vẫn là mới nhất trước, nhưng thêm sort theo tên (dữ liệu là năm 1970–2030)

### C5. Menu
- [ ] `components/subsystem-menu/master-data.js`: nhóm **"Xe"**, 4 mục theo thứ tự cha → con,
      mỗi mục `isShow: ['Quản lý danh mục …', 'Xem danh mục …']`
- [ ] Kiểm trong trình duyệt: có quyền thì thấy, thu hồi thì mục biến mất

## Đợt D — Nghiệm thu (4 task)

### D1. Playwright 4 màn, đo bằng số lấy từ DOM
- [ ] Mỗi màn: mở · đếm dòng đúng tổng · **bấm thật từng ô lọc** rồi đối chiếu param trên Network ·
      **bấm thật từng nút** trong cột Hành động (kể cả trong menu "…")
- [ ] Đo ô lọc cao đúng **36px**, nhãn floating
- [ ] Thêm/sửa/khoá/mở khoá/xoá thật 1 bản ghi mỗi màn rồi **dọn sạch**

### D2. Gate quyền 2 chiều
- [ ] Có quyền → vào được; thu hồi quyền → **403** và mục menu biến mất
- [ ] Nhớ xoá cache spatie giữa 2 lần đo

### D3. ERP không vỡ
- [ ] Mở lại 4 màn danh mục ERP: danh sách, thêm, sửa, xoá vẫn chạy
- [ ] Mở tab "Phân loại xe" của Phase 2: 3 ô chọn vẫn đủ dữ liệu
- [ ] Đếm lại `productables` theo từng `productable_type` — 5 con số y hệt mốc A4

### D4. Chốt sổ
- [ ] `git status` sạch cả 2 repo, commit theo từng đợt
- [ ] Cập nhật `STATUS.md` + `../design.md` (đổi 2b sang 🟢)
- [ ] Ghi "Nhật ký" ở cuối file này: số đo, bẫy gặp, việc còn nợ

## Nhật ký

### 21/09/2026 — Đợt A

**A1 — migration `status` cho `vehicle_life`**: `2026_09_23_000001_add_status_to_vehicle_life_table.php`,
chạy xong. Đo lại: **61 dòng / 61 `status = 1`**, không dòng nào lệch.

**A2 — cặp Model xe trùng**: đúng **1 cặp**, id **1090 + 1091**, cùng tên `SE`, cùng Hãng xe
`Land Rover` (124), cùng Loại xe `Discovery` (1427), cùng `created_at` 2022-11-07 14:11:18 — là một
lần bấm Lưu hai lần.
Kiểm tham chiếu trước khi động: `productables`(VehicleModel) · `product_vehicle_model_has_life` ·
`vehicles` → **cả 3 đều 0 dòng** cho cả 2 id ⇒ an toàn.
Xử lý: **khoá id 1091** (`status = 0`), KHÔNG xoá — giữ đường lùi. Đo lại: trùng-trong-cùng-cha
(tính trên bản ghi đang hoạt động) = **0**, tổng `vehicle_models` vẫn **1.281**.

**Quyết định phát sinh:** rule unique **chỉ so trong bản ghi đang hoạt động**. ERP so cả bản ghi đã
"xoá" nên tên của một hãng xe bị xoá là vĩnh viễn không tạo lại được — không bê lỗi đó sang.
Khe hở kèm theo (Mở khoá có thể tạo 2 bản trùng tên) → chặn ở Task B3.

**A3 — 4 Entity** (`Modules/MasterData/Entities/Vehicle/`): **nâng cấp 3 file có sẵn** của Phase 2
(`VehicleManufact` / `VehicleBrand` / `VehicleModel`, vốn `extends Model` chỉ để đọc) lên
`BaseCatalogModel`, **không tạo bản thứ hai** — 2 model cùng trỏ 1 bảng là nguồn lệch kinh điển.
Thêm mới `VehicleLife.php`. Nơi duy nhất đang `use` 3 file cũ là
`ProductOptionService::vehicleCatalog()`, và nó query bằng cột thô chứ không đụng hằng ⇒ nâng cấp
an toàn, đã đo lại bên dưới.

**A4 — số mốc đo 21/09/2026** (đối chiếu ở Đợt D):

| Bảng | Tổng | Hoạt động | Khóa |
|---|---:|---:|---:|
| `vehicle_manufacts` | 56 | 55 | 1 |
| `vehicle_brands` | 322 | 320 | 2 |
| `vehicle_models` | 1.281 | 1.280 | 1 *(vừa khóa id 1091 ở A2)* |
| `vehicle_life` | 61 | 61 | 0 |

`productables` theo `productable_type`: VehicleManufact **13.165** · VehicleBrand **12** ·
VehicleModel **6** · `App\Model\Product\Group` (Nhóm máy) **3.968** · `App\Product` (Máy sử dụng)
**28.398**. `product_vehicle_model_has_life` **48.736**.

Thử `childrenCount()` thật: Hãng xe #111 *Acura* = **352** ⇒ `isCanDelete() = false`,
`isCanLock() = true` (đúng ý đồ §2.6). Loại xe #1297 *HYUNDAI* = 4, cha = *THACO*. Model #1090 *SE*
= 0, cha = *Discovery*. Đời xe #1 *1970* = **728** dòng đang gắn.

✅ **Tab "Phân loại xe" của Phase 2 không vỡ:** `vehicleOptions()` vẫn trả 56 / 322 / 1.281.

### 21/09/2026 — Đợt B (backend)

4 Service · 4 Request · 4 Resource · 4 Controller + 6 điểm đăng ký. Quyền **1620–1627**
(max id đang có trước khi thêm là 1619), cấp cho role 18 *Super admin* rồi xoá cache spatie.

**🐞 Bắt được N+1 nặng, không test nào báo.** `BaseCatalogResource` trả `is_can_delete` cho mọi
dòng, mà `isCanDelete()` gọi `childrenCount()` — riêng Hãng xe là **7 câu đếm / 1 dòng**:

| Màn | Trước | Sau |
|---|---:|---:|
| Hãng xe (56 dòng) | **387 query** | **2** |
| Loại xe (100 dòng) | 297 | 3 |
| Model xe (100 dòng) | 304 | 4 |
| Đời xe (61 dòng) | 63 | 2 |

Chữa bằng cột ảo `children_exists` (subquery `EXISTS ... or EXISTS ...`, gắn ở `index()`), model
đọc cột đó thay vì tự đếm — 2 trait `SelectsChildrenFlag` / `PreloadsChildrenFlag`. Số query giờ
**không đổi theo số dòng** (10 dòng hay 100 dòng đều 2–4). Luồng show/store/update vẫn đếm thật.
KHÔNG sửa lớp nền vì 17 màn danh mục khác đang kế thừa.
Đối chiếu đúng/sai: **236 dòng, 0 lệch** giữa cột ảo và phép đếm thật.

⚠️ Bẫy PHP 7.4: **trait không được khai hằng** ("Traits cannot have constants", mãi 8.2 mới có)
→ tên cột ảo phải nằm ở class riêng `Concerns\ChildrenFlag`.

**Ép 14 nhánh qua API thật** (`curl`, không qua test):

| Nhánh | Kết quả |
|---|---|
| Tạo / sửa / xoá / khoá / mở khoá cả 4 màn | 200 |
| Trùng tên trong cùng cha | 422 "Đã tồn tại" |
| Trùng tên **khác cha** (Loại xe) | 200 — đúng, unique theo cha |
| Loại xe không thuộc Hãng xe đã chọn | 422 *(ERP KHÔNG kiểm — HRM chặn thêm)* |
| Xoá bản ghi đang có nơi dùng | 400 "đang được sử dụng" |
| Sửa bản ghi đang khoá | 400 |
| Xoá bản ghi đang khoá | 400 "hãy mở khoá trước" |
| **Mở khoá sinh trùng tên** | 400 — khe hở ở §2.3 đã bịt |
| Export 4 màn | 200, file 81–138 KB |

Sau khi dọn: 4 bảng **56 / 322 / 1.281 / 61** y hệt mốc A4, **0 bản ghi rác `E2E%`**,
`catalog_histories` ghi **18 dòng** (chứng minh đăng ký `CatalogHistoryService::TABLES` chạy —
thiếu là fatal).

### 21/09/2026 — Đợt C (frontend) + Đợt D (nghiệm thu)

4 màn `pages/master-data/vehicle-{manufacts,brands,models,life}/` + 4 popup. Phần lặp gom vào
**2 mixin** (`vehicleCatalogScreenMixin` / `vehicleCatalogModalMixin`) thay vì chép 4 lần — Phase 1
chép 11 lần và một lỗi đã nhân thành 11 màn (xem ngay dưới).

**🐞 4 lỗi IM LẶNG bắt được, cả 4 chỉ lộ khi mở trình duyệt đo:**

1. **Nhóm menu "Xe" không bao giờ hiện.** Tôi khai `children:`, mà `deriveHubGroups()` lọc
   `Array.isArray(item.subItems)` ⇒ cả nhóm bị bỏ qua, **không lỗi console, không cảnh báo build**.
   Chỉ lộ khi đếm link trên hub. Sửa xong: hub hiện "Xe — 4 chức năng", đủ 4 đường dẫn.

2. **Popup Xác nhận Xoá / Khoá của màn Hãng xe không mở.** Id khai trong template là số ít
   (`confirm-delete-vehicle-manufact`) còn mixin gọi `'confirm-delete-' + catalogSlug` = số nhiều.
   Bấm nút không ra gì, không lỗi. Đã chốt quy tắc: id popup **phải** bằng
   `confirm-<việc>-<catalogSlug>`, và kiểm bằng grep cả 4 màn.

3. **Lọc dây chuyền gửi giá trị cũ lên máy chủ.** Lần đầu tôi dùng `resetKeys` của
   `V2BaseSmartFilterPanel` — prop đó nghĩa là *"xoá key khi field bị ẨN ở popup Cài đặt bộ lọc"*,
   không phải xoá theo cấp cha. Kết quả: ô Loại xe trống trên màn nhưng
   `filters.vehicle_brand_id` vẫn giữ id cũ. Đo thật: chọn Toyota + Camry rồi đổi sang Honda →
   request đi ra `vehicle_manufact_id=120&vehicle_brand_id=1488`, bảng rỗng trong khi Honda có
   **35 model**.
   Lần sửa thứ nhất (đặt ở `watch`) vẫn hụt một nhịp: watcher `filters` deep của mixin được tạo
   trước nên chạy trước, bắn đi **1 request còn kèm id cũ**, rồi mới xoá và bắn request thứ hai —
   bộ e2e bắt đúng request đầu và vẫn đỏ. Chốt: xoá ngay trong `handleFilterChange`, gán cả hai
   trong **cùng một nhịp** ⇒ deep watcher chỉ thấy trạng thái cuối, đúng **1 request**.

4. **Lỗi có sẵn ở 11 màn Phase 1 (KHÔNG sửa lấn phase, xem mục "Việc bàn giao").**

**Đo bằng số lấy từ DOM:**

| Đo | Kết quả |
|---|---|
| Bộ cột 4 màn | đúng; Đời xe **không** có cột Ghi chú (bảng không có `note`) |
| Tổng dòng trên phân trang | 56 / 322 / 1.281 / 61 — khớp DB |
| Ô lọc | cao **36px** (khoảng ngày 32px — **giống hệt màn Đơn vị tính của Phase 1**, không phải lỗi mới) |
| Lọc Hãng xe = Toyota | ô Loại xe **320 → 27** option = đúng số loại xe đang hoạt động của Toyota trong DB |
| Lọc tiếp Loại xe = Camry | "Hiển thị 1–10 / 11" |
| Đổi sang Honda | Loại xe tự trống, "Hiển thị 1–10 / **35**" = đúng số model Honda trong DB |
| Form Model xe | chọn Hãng xe xong ô Loại xe mới mở khoá, đúng 27 option |
| Vòng đời trên màn Đời xe | tạo → 61→62 · khoá → badge "Khóa" · **mở khoá gọi `/unlock`** · xoá → về 61, 0 rác |
| Popup Lịch sử | 3 mục đúng thứ tự mới→cũ, có giá trị cũ→mới |

**Gate quyền — kiểm CẢ HAI chiều:**

| | index | store | export | menu |
|---|---|---|---|---|
| Có quyền | 200 | 200 | 200 | nhóm "Xe" 4 mục |
| Thu hồi + xoá cache spatie | **403** | **403** | **403** | nhóm biến mất, store 0 quyền xe |

**Bộ e2e:**

- `product-catalog-common.api.spec.ts`: thêm 4 màn Xe vào bảng `CATALOGS` → **105 ca (15 màn × 7),
  105 passed**.
- `vehicle-catalog.api.spec.ts` (**mới**, 6 ca): unique theo cha · trùng tên khác cha vẫn tạo được ·
  khoá rồi dùng lại tên · **mở khoá sinh trùng tên bị chặn** · cặp Hãng/Loại xe lệch nhau 422 ·
  `getAll` bỏ bản ghi khoá · xoá bị chặn khi còn con. **6 passed**.
- `product-catalog-ui.spec.ts`: thêm khối 5 ca cho 4 màn Xe → **23 passed** (18 ca cũ vẫn xanh).

Chạy: Node 20 + `--project=api|chromium --no-deps --workers=1`. ⚠️ `HRM/e2e` không nằm trong git.

**Dữ liệu sau toàn bộ:** 4 bảng **56 / 322 / 1.281 / 61** y hệt mốc A4 · `productables` 5 con số
y nguyên (13.165 / 12 / 6 / 3.968 / 28.398) · `product_vehicle_model_has_life` **48.736** ·
0 bản ghi rác.

## Việc bàn giao — cần anh/chị quyết

### 🐞 Lỗi có sẵn ở 11 màn Phase 1: bấm "Mở khoá" lại gọi `/lock`

Phát hiện khi chép khuôn màn. **KHÔNG sửa** vì thuộc Phase 1 đang chờ nghiệm thu — để anh/chị
quyết có gộp vào đợt này không.

**Chỗ sai** — `pages/master-data/<màn>/index.vue`, 4 vị trí mỗi file:

```js
Number(this.itemToToggle.status) === 2     // chuẩn bảng MỚI của #11421
```

Bảng ERP khoá bằng **0**, không phải 2. Nên với bản ghi đang khoá (`status = 0`) biểu thức luôn
`false` ⇒ `toggleLock()` gọi đường `/lock` và hiện toast **"Khóa thành công"** trong khi bản ghi
vẫn khoá. Nút và nhãn thì đúng (chúng so `=== 1`), nên nhìn màn không thấy gì bất thường.

**Phạm vi:** 11 màn bảng ERP — `units` · `tax-rates` · `product-models` · `origins` · `order-codes`
· `manufacturers` · `color-codes` · `brands` · `attributes` · `attribute-units` ·
`attachment-types`. (6 màn Phase 0 dùng bảng mới nên `=== 2` là **đúng**, đừng sửa nhầm.)

**Cách sửa:** đổi 4 chỗ mỗi file sang so `!== 1` (hoặc dùng `isActiveRow()` như 4 màn Xe). Ước
lượng 11 file × 4 dòng, kèm 1 ca e2e cho đường Mở khoá.

### Còn tồn của Phase 2b

| Việc | Vì sao chưa làm |
|---|---|
| **Import** cho 4 màn | màn import Model xe bên ERP chưa chốt giữ hay bỏ (`design.md` §2.8) |
| **Chặn route sửa bên ERP** + cho `VehicleLife::searchByFilter()`/`getForSelect()` lọc `status` | thuộc đợt "sửa ERP để không lỗi", không nhét vào phase này |
| Ô **Đời xe** trên form hàng hoá | thuộc Phase 2, còn chờ chốt cách hiển thị (§15d câu 3) |
| Chạy `PermissionsTableSeeder` trên môi trường khác | ở local đã chèn 8 quyền **1620–1627** bằng SQL; seeder truncate cả bảng nên không chạy ở máy đang có dữ liệu |

### Ghi chú kỹ thuật đáng nhớ

- **Trait PHP 7.4 không được khai hằng** ("Traits cannot have constants", mãi 8.2 mới có) ⇒ tên cột
  ảo `children_exists` phải nằm ở class riêng `Concerns\ChildrenFlag`.
- **`offsetParent` luôn null với `position: fixed`** — menu "…" của `V2BaseRowActions` gắn vào
  `body` và neo fixed, nên đo "đang hiện" bằng `offsetParent` là luôn ra "không hiện". Dùng
  `getComputedStyle(el).display`.
- **Playwright bấm nút "…" bằng `click()` thì menu mở rồi đóng ngay** — trình duyệt cuộn nút vào
  tầm nhìn, sự kiện `scroll` đó đóng menu (chính component đã ghi chú). Bấm bằng `dispatchEvent`
  để không kích hoạt cuộn.
- **`V2BaseSelectInModal` không đổ option vào thẻ `<select>` gốc** — đếm `select.options.length`
  trong popup luôn ra 0. Phải mở dropdown rồi đếm `.select2-results__option`.

## Bổ sung 22/09/2026 — thêm 2 danh mục: Dòng xe, Tải trọng xe

> User: *"bổ sung chuyển luôn các danh mục: Dòng xe, tải trọng xe"*

2 màn này vốn nằm ở **Phase 2c** (nhóm xe công ty / vận chuyển). User chốt chuyển luôn cùng đợt,
nên dời sang đây. Phase 2c còn lại **3 màn**: biển số xe · lái xe ngoài · danh mục xe.

| Màn | Bảng | Dòng | Hoạt động |
|---|---|---:|---:|
| Dòng xe | `vehicle_categories` | 11 | 10 |
| Tải trọng xe | `vehicle_payloads` | 31 | 30 |

**Cấu trúc đơn giản nhất trong cả 6 màn:** chỉ `name` + `status` + người tạo/sửa. Không có `code`,
không có `note` — giống hệt Đời xe, nên dùng lại nguyên khuôn đó.

⚠️ **Không dính hàng hoá.** Giá trị bên trong Dòng xe là *"Xe tải thùng kín" · "Xe cẩu" · "Xe đầu
kéo"*; Tải trọng là *"3.5 tấn" · "15 tấn"*. `products` KHÔNG tham chiếu 2 bảng này — chúng phục vụ
phân hệ vận chuyển. Đặt chung nhóm menu "Xe" cho gọn một chỗ, không phải vì liên quan hàng hoá.

⚠️ **Mỗi bảng bị 13 bảng khác tham chiếu** (toàn bộ nhóm `delivery_*` + `vehicles`) ⇒ dùng chung
bảng ERP, không di trú. Danh sách 13 bảng gom vào hằng `BANG_THAM_CHIEU` trên Entity để Service
dựng subquery `children_exists` khỏi chép lại.

Quyền **1628–1631** (4 quyền). Menu nhóm "Xe" từ 4 → **6 mục**.

**Kiểm chứng:** danh sách đo từ DOM ra đúng **11** và **31** dòng, khớp DB · `getAll` trả 10 / 30
(bỏ bản ghi khoá) · bộ e2e chung lên **119 ca (17 màn × 7), 119 passed** · bộ UI **23 passed**
(ca đếm menu sửa 4 → 6) · 6 bảng xe y hệt mốc, **0 bản ghi rác**.
