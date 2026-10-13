# Phase 2b — Chuyển 4 danh mục Xe sang HRM

> Folder con của `.plans/gop-db/quan-ly-hang-hoa/` · Bắt đầu 21/09/2026 · @namdangit
> Nhánh: `feat/p1-danh-muc-hang-hoa` (cả 2 repo) — **cùng nhánh với Phase 1 + Phase 2**, vì nền
> `BaseCatalog*` đã được Phase 1 nới hook cho bảng ERP; tách nhánh mới từ `gop_db` là mất phần nới đó.
> Phạm vi user chốt 21/09/2026: *"Lấy đúng 4 màn lõi, phần còn lại tách phase riêng"* (→ Phase 2c).

## 1. Bốn màn, đo thật trên `hrm_erp` ngày 21/09/2026

| Màn HRM | Route HRM | Bảng ERP | Dòng | Controller ERP | Cha |
|---|---|---|---:|---|---|
| Hãng xe | `/master-data/vehicle-manufacts` | `vehicle_manufacts` | 56 | `VehicleManufactController` (188) | — |
| Loại xe | `/master-data/vehicle-brands` | `vehicle_brands` | 322 | `VehicleBrandController` (213) | Hãng xe |
| Model xe | `/master-data/vehicle-models` | `vehicle_models` | 1.281 | `VehicleModelController` (289) | Hãng xe + Loại xe |
| Đời xe | `/master-data/vehicle-life` | `vehicle_life` | 61 | `VehicleLifeController` (111) | — |

Cấu trúc bảng (đo bằng `SHOW COLUMNS`, không đoán):

```
vehicle_manufacts : id name note created_at updated_at created_by updated_by status
vehicle_brands    : id name note vehicle_manufact_id status created_by updated_by created_at updated_at
vehicle_models    : id name note vehicle_manufact_id vehicle_brand_id created_by updated_by status created_at updated_at
vehicle_life      : id name created_by updated_by created_at updated_at          <-- KHÔNG có status, KHÔNG có note
```

**Cả 4 bảng đều không có cột `code`** → `hasCodeField()` trả `false` ở **cả Service lẫn Request**
(2 chỗ, Phase 1 đã dính lỗi quên 1 chỗ).

## 2. Quyết định đã chốt

### 2.1. Nhãn màn "Loại xe", không phải "Phân loại xe"

Một bảng, **ba tên gọi** trong chính ERP:

| Nơi | Gọi là |
|---|---|
| comment ở `routes/web.php` | "Thương hiệu xe" |
| menu `topmenubar.blade.php` | "Danh mục phân loại xe" |
| form hàng hoá `products/form.blade.php` | **"Loại xe"** |

Chốt dùng **"Loại xe"** — trùng nhãn ô người dùng gặp nhiều nhất (form hàng hoá), và tránh đụng tên
**tab "Phân loại xe"** của Phase 2 (tab đó chứa cả 4 ô: Hãng xe · Loại xe · Model xe · Đời xe).
Đặt tên tab = tên một ô bên trong nó là chắc chắn gây nhầm.

⚠️ Đừng lẫn `vehicle_brands` (Loại xe) với `brands` (Thương hiệu hàng hoá, 1.250 dòng, đã port ở
Phase 1). Hai bảng khác nhau, hai màn khác nhau.

### 2.2. Dùng chung bảng ERP, KHÔNG di trú — y như Phase 1

`vehicle_manufacts.id` bị **10 bảng** trỏ tới, dữ liệu đang sống:

| Nơi dùng | Dòng |
|---|---:|
| `productables` (tab Phân loại xe của hàng hoá) | 13.165 |
| `customer_has_vehicle_manufacts` | 1.560 |
| `firm_contracts` | 253 |
| `wr_service_contracts` | 104 |
| `vehicles` | 137 |
| `product_vehicle_model_has_life` (hàng hoá × model × đời xe) | 48.736 |
| 4 bảng `division_market_*` | 0 (rỗng, cột vẫn còn) |

⇒ HRM đọc/ghi thẳng bảng ERP, giữ nguyên `id`. Không tạo bảng mới, không remap.

### 2.3. Tên unique THEO CHA, không unique toàn bảng

Đây là chỗ **không bê được rule của Phase 0** ("`name` unique toàn bảng"). Đo thật:

| Bảng | Trùng tên toàn bảng | Trùng trong cùng cha |
|---|---:|---:|
| `vehicle_manufacts` | 0 | — |
| `vehicle_brands` | 2 | **0** |
| `vehicle_models` | **112** | **1** |
| `vehicle_life` | 0 | — |

"2.0 AT" xuất hiện ở **24 loại xe** khác nhau, "1.6 AT" 15 lần — trùng toàn bảng là **bình thường**,
không phải rác. Áp unique toàn bảng là 112 bản ghi hợp lệ thành không sửa được.

Chốt (đúng bằng rule ERP đang chạy, đọc từ closure validate trong controller):

- Hãng xe: `unique(name)`
- Loại xe: `unique(name, vehicle_manufact_id)`
- Model xe: `unique(name, vehicle_manufact_id, vehicle_brand_id)`
- Đời xe: `unique(name)`

**Chỉ so trong các bản ghi ĐANG HOẠT ĐỘNG** (`status = 1`). ERP so với cả bản ghi đã "xoá"
(`status = 0`), nên sau khi xoá một hãng xe thì cái tên đó **vĩnh viễn không tạo lại được** — lỗi
của ERP, không bê sang.

⚠️ Đổi lại là có một khe hở: **Mở khoá** một bản ghi có thể tạo ra 2 bản trùng tên cùng hoạt động.
Nền `isCanUnlock()` chỉ kiểm danh mục cha. Đã ghi nhận, xử lý ở Task B3 (chặn ngay ở đường mở khoá
của 4 màn xe), KHÔNG sửa lớp cha vì 17 màn khác đang dùng.

⚠️ **1 cặp Model xe trùng trong cùng cha** phải dọn trước khi bật rule. Task A2 lo việc này.

### 2.4. Thêm cột `status` cho `vehicle_life`

`vehicle_life` là bảng **duy nhất** trong 4 bảng không có `status`, kéo theo:

- `BaseCatalogModel::scopeActive()` (`where('status', …)`) nổ SQLSTATE[42S22] ngay ở `getAll`;
- không có Khoá / Mở khoá, mà nút Xoá của ERP là **xoá cứng** (`$object->delete()`) trên một danh
  mục đang được `product_vehicle_model_has_life` tham chiếu **48.736 dòng** — xoá 1 đời xe là mồ côi
  hàng nghìn dòng, không có FK nào chặn.

Chốt: **migration thêm `status TINYINT NOT NULL DEFAULT 1`** vào `vehicle_life`.

Vì sao chọn thêm cột thay vì nới nền bằng hook `hasStatusField()`: hook đó đụng lớp cha mà **17 màn
danh mục đang chạy** cùng kế thừa, đổi để phục vụ 1 bảng là rủi ro lệch pha 17 màn. Thêm 1 cột có
default thì ERP không phải sửa dòng nào — `VehicleLifeController@store` gán tay `name` rồi `save()`,
default lo phần còn lại.

⚠️ **Hệ quả phải nói trước:** `VehicleLife::searchByFilter()` và `getForSelect()` của ERP **không
lọc `status`** → bản ghi khoá ở HRM vẫn hiện ở màn Đời xe của ERP và vẫn nằm trong ô chọn của ERP.
Muốn đồng bộ thì phải sửa 2 hàm đó bên ERP — **để Phase 2c / đợt "sửa ERP để không lỗi" xử lý**,
không nhét vào phase này.

### 2.5. Trạng thái 1/0 kiểu ERP, và "Xoá" của ERP chính là "Khoá"

`delete()` của 3 controller ERP **không xoá dòng** — nó set `status = 0`. Nên:

- ERP "Xóa hãng xe" == HRM **Khoá**. 1 hãng xe và 2 loại xe đang `status = 0` là bản ghi ERP đã
  "xoá", HRM hiển thị **Khoá**. Đúng quy ước Phase 1 (`Unit.php`), không đổi.
- `STATUS_ACTIVE = 1` / `STATUS_INACTIVE = 0` khai lại ở lớp con. Nền đọc bằng `static::`, đã đúng.

Nút **Xoá** của HRM là xoá thật (`BaseCatalogService::destroy`), nên phải chặn bằng
`childrenCount()` — xem 2.6.

### 2.6. Điều kiện Xoá / Khoá

Nền: `isCanDelete()` = đang hoạt động **và** `childrenCount() === 0`; `isCanLock()` = đang hoạt động
**và** `activeChildrenCount() === 0`.

| Màn | `childrenCount()` đếm gì (chặn XOÁ) | `activeChildrenCount()` |
|---|---|---|
| Hãng xe | `vehicle_brands` + `vehicle_models` + `productables`(VehicleManufact) + `customer_has_vehicle_manufacts` + `firm_contracts` + `wr_service_contracts` + `vehicles` | `0` |
| Loại xe | `vehicle_models` + `productables`(VehicleBrand) + `vehicles` | `0` |
| Model xe | `productables`(VehicleModel) + `product_vehicle_model_has_life` + `vehicles` | `0` |
| Đời xe | `product_vehicle_model_has_life` | `0` |

`activeChildrenCount()` trả **0 là cố ý** (đúng như `Unit.php` của Phase 1): nền dùng nó để chặn
KHOÁ, mà khoá là thao tác chính của màn — chặn khoá thì màn vô dụng.

⚠️ Đếm `productables` **bắt buộc kẹp `productable_type`** bằng hằng chuỗi ERP trong
`Modules/MasterData/Entities/Product/Productable.php`. Một bảng gánh 5 loại quan hệ; đếm không kẹp
là ra số của cả Nhóm máy (3.968) và Máy sử dụng (28.398).

### 2.7. Menu + quyền

- FE: phân hệ **Danh mục chung** (`master-data`), **nhóm mới "Xe"** — 4 mục theo thứ tự cha → con:
  Hãng xe · Loại xe · Model xe · Đời xe. Khai ở `components/subsystem-menu/master-data.js`.
- Quyền: 4 màn × cặp Xem / Quản lý = **8 quyền**, `group = 'Danh mục hàng hóa'`, `type = 9`,
  `guard_name = 'api'`. Id dự kiến **1620–1627**, nhưng **phải lấy lại max id ngay trước khi commit**
  (đã dính lỗi trùng id khi merge nhánh dài).

⚠️ **Đổi hành vi, cần báo user:** 4 route group này bên ERP **không có `checkPermission`** — ai vào
được ERP là sửa được. Sang HRM có gate thì người đang dùng sẽ mất quyền cho tới khi được cấp.

### 2.8. Không làm ở phase này

- **Import** — chỉ Model xe có màn import bên ERP (`vehicleModel.viewImport` + import Brand/Model).
  Chưa chốt giữ hay bỏ ⇒ đợt này **không** làm, route import không khai.
- **Sửa ERP** (chặn route cũ, lọc `status` ở `VehicleLife`) — thuộc đợt "sửa ERP để không lỗi".
- Ô **Đời xe trên form hàng hoá** — thuộc Phase 2 (§15d câu 3, chưa chốt cách hiển thị).

## 3. Sáu điểm đăng ký, sót chỗ nào là hỏng im lặng

Bài học Phase 1 (`copy-man-danh-muc-4-cho-sot-im-lang`): test vẫn xanh mà màn vẫn hỏng.

| # | File | Thêm gì |
|---|---|---|
| 1 | `Modules/MasterData/Routes/api.php` | 4 dòng vào mảng `$erpCatalogs` |
| 2 | `app/Services/CatalogHistoryService.php` → `TABLES` | 4 mục (thiếu ⇒ ghi lịch sử **fatal**) |
| 3 | `app/ExcelExport/ExportColumnRegistry.php` | 4 mục (thiếu ⇒ popup chọn trường rỗng) |
| 4 | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | 8 quyền |
| 5 | `hrm-client/components/subsystem-menu/master-data.js` | nhóm "Xe" + 4 mục |
| 6 | prop `entity-type` của popup lịch sử ở **từng** `index.vue` | 4 giá trị đúng tên bảng |

Điểm 6 là chỗ Phase 1 sót 4 màn liền: copy `index.vue` mà quên đổi `entity-type="origins"`.

## 4. Kiểm chứng bắt buộc trước khi báo xong

1. **Số dòng 4 bảng y hệt mốc đầu**: 56 / 322 / 1.281 / 61, **0 bản ghi rác** sau khi bấm thử.
2. **Gate quyền kiểm cả 2 chiều** — có quyền vào được, thu hồi quyền phải 403 (fail-closed).
3. **Playwright đo từ DOM**: đủ 4 màn, đúng bộ cột, ô lọc bắn đúng param, nút trong cột Hành động
   bấm thật (`V2BaseRowActions` emit **chuỗi**, so `action.key` là nút chết im ru).
4. **Lọc dây chuyền**: chọn Hãng xe ở màn Model xe thì ô Loại xe phải co lại đúng tập con.
5. **Không làm vỡ ERP**: mở lại 4 màn ERP + tab "Phân loại xe" của Phase 2, dữ liệu như cũ.
