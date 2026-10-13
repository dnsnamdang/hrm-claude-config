# Chuyển quản lý hàng hoá sang HRM + quy hoạch lại catalog phân loại hàng hoá

> Folder LỚN — mỗi phase là một folder con theo khuôn feature nhỏ (`design.md` + `plan.md`).
> Nhánh: `gop_db` (cả 2 repo) · Nền tảng đọc TRƯỚC: `.plans/gop-db/design.md` (7 gotcha port ERP → HRM)
> Bắt đầu 20/09/2026 · Phụ trách: @namdangit
> File này CHỈ chứa phạm vi + hiện trạng + quyết định chung. Spec chi tiết nằm trong từng folder con.

> 📌 **Quay lại làm tiếp thì mở `SO-CHOT-VA-TON.md` trước** — sổ gom toàn bộ quyết định đã chốt,
> việc đang chặn, việc để xử lý sau và các bẫy đã trả giá.

## Tiền đề của cả feature — chuyển NỀN CODE, không đổi CSDL

> User nhắc lại 22/09/2026: *"mục tiêu chuyển ở đây là chỉ chuyển nền tảng code, không đổi bảng
> database"*

Mọi màn chuyển sang HRM đều **đọc/ghi thẳng bảng ERP đang chạy**, giữ nguyên `id`. Không tạo bảng
mới, không sao chép dữ liệu, không remap khoá. Đây là **mặc định của toàn bộ feature**, không phải
quyết định riêng của từng phase — nên từ đây trở đi **không nhắc lại nó như một cảnh báo** ở từng
màn nữa.

Thứ đáng ghi ra là **ngoại lệ**: chỗ nào buộc phải đụng schema thì phải nêu riêng, kèm lý do và
chờ user duyệt. Tới 22/09/2026 có đúng **3 ngoại lệ**, đều đã được duyệt:

| Thay đổi CSDL | Bảng | Vì sao | Nơi ghi |
|---|---|---|---|
| Thêm 2 cột phân loại mới | `products` | nối hàng hoá vào cây 4 cấp của Phase 0 | `2026_09_22_000001` |
| Gỡ cột `can_retail` | `product_types` | user chốt bỏ hẳn khái niệm này | `2026_09_22_000002` |
| Thêm index `(updated_at, id)` | `products` | sắp xếp mặc định quét toàn bảng, 119ms → 0ms | `2026_09_22_000003` |
| Thêm cột `status` | `vehicle_life` | 🔶 **xem ghi chú dưới** | `2026_09_23_000001` |

🔶 `vehicle_life` là ngoại lệ **duy nhất chưa được nêu ra rõ ràng như một thay đổi CSDL** — lúc đó
tôi trình bày nó như một chi tiết kỹ thuật của màn. Cần user xác nhận lại: giữ cột này, hay bỏ và
để màn Đời xe không có Khoá/Mở khoá (khi đó nút Xoá là xoá cứng như ERP, trên danh mục đang bị
`product_vehicle_model_has_life` giữ 48.736 dòng).

## Phạm vi — chốt với user 20/09/2026

Ba nhóm rạch ròi: **CHUYỂN sang HRM**, **BỎ không dùng nữa**, **GIỮ NGUYÊN bên ERP**.

### A. CHUYỂN sang HRM — 14 danh mục

Đều nằm trong nhóm menu ERP **Hàng hóa ▸ Quản lý hàng hóa**. Số dòng đo thật trên DB gộp
`hrm_erp` ngày 20/09/2026.

| # | Màn ERP | Route ERP | Controller | Bảng | Số dòng |
|---|---|---|---|---|---|
| 1 | Danh mục hàng hóa | `proList` | `ProductsController` | `products` | 45.890 |
| 2 | Danh mục hàng tạm → **Phase 6** | `tmpProductIndex` | `Sale\TmpProductsController` | `tmp_products` | 1.957 |
| 3 | Cập nhật nhanh hàng hóa | `product.updateListProducts` | `ProductsController` | `products` | — |
| 4 | Danh mục model | `model.index` | `Sale\ProductModelsController` | `product_models` | 39.796 |
| 5 | Danh mục code đặt hàng | `barcode.index` | `Sale\BarcodesController` | `barcodes` | 8.664 |
| 6 | Danh mục đơn vị tính | `unitIndex` | `Sale\UnitsController` | `units` | 145 |
| 7 | Danh mục thuộc tính | `attributeIndex` | `Sale\AttributesController` | `attributes` | 446 |
| 8 | Danh mục đơn vị thuộc tính | `unitechsIndex` | `Sale\UnitechsController` | `unitteches` | 103 |
| 9 | Danh mục thương hiệu | `brandList` | `Sale\BrandsController` | `brands` | 1.250 |
| 10 | Danh mục hãng sản xuất | `manufacIndex` | `Sale\ManufacturesController` | `manufactures` | 1.071 |
| 11 | Danh mục xuất xứ | `originIndex` | `Sale\OriginsController` | `origins` | 113 |
| 12 | Danh mục file đính kèm | `AttachmentType.index` | `Common\AttachmentTypeController` | `attachment_types` | 8 |
| 13 | Danh mục mã màu | `codeColorIndex` | `Common\CodeColorController` | `code_colors` | 0 |
| 14 | Danh mục thuế suất | `taxRates.index` | `Common\TaxRatesController` | `tax_rates` | 40 |

**Bổ sung 21/09/2026:** thêm **4 danh mục Xe** (Hãng xe · phân loại xe · model xe · đời xe)
ngoài 14 màn trên — nằm ở nhóm menu ERP **Xe**, tách thành **Phase 2b**. Xem mục Phase 2b.

### B. ~~BỎ~~ → **ĐỔI HƯỚNG 27/09/2026: GIỮ CÂY 4 CẤP, CHUYỂN SANG HRM**

> ⚠️ Mục này **đã sửa ngày 27/09/2026** theo yêu cầu user. Trước đó chốt bỏ cả 4 màn nhóm
> *Quản lý catalog*; nay **không bỏ** — cây 4 cấp vẫn sống và được đưa vào **tab Dữ liệu quản trị
> theo công ty** của form hàng hoá. Chi tiết: `man-danh-muc-hang-hoa/design.md` **§30**.

| Màn ERP | Route ERP | Bảng | Số dòng | Xử lý (chốt 27/09/2026) |
|---|---|---|---|---|
| Danh mục lĩnh vực | `scope.index` | `scopes` | 14 | **BỎ MÀN + XOÁ SẠCH DATA** (user chốt 27/09) — thay bằng *Danh mục lĩnh vực Công ty kinh doanh* của HRM (`internal_business_scopes`, 8 dòng, màn `/assign/internal-business-scopes` **đã có sẵn**) |
| Danh mục chương | `chapter.index` | `chapters` | 65 | **CHUYỂN SANG HRM** |
| Danh mục nhóm công việc | `job_group.index` | `job_groups` | 106 | **CHUYỂN SANG HRM** |
| Danh mục cụm công việc | `job_cluster.index` | `job_clusters` | 2 | **CHUYỂN SANG HRM** |
| Danh mục nhóm hàng hóa | `groupIndex` | `groups` | 893 | **BỎ MÀN, GIỮ BẢNG** (§21 — vai trò Nhóm máy) |

Cây thật trong CSDL: `scopes` → `chapters.scope_id` → `job_groups.chapter_id` →
`job_clusters.group_id`. Cây phân loại mới ở Phase 0 (Nhóm chức năng → Nhóm sản phẩm → Loại sản
phẩm) **không thay thế** cây này nữa — hai cây phục vụ 2 việc khác nhau: cây Phase 0 phân loại
**bản chất hàng hoá**, cây 4 cấp phân loại **lĩnh vực kinh doanh theo công ty**.

✅ **Đính chính 27/09/2026:** `scopes` **không** có tham chiếu ngoài nhánh hàng hoá. Các bảng
`industry_scopes` · `prospective_projects` · `application_scopes` · `solutions` · `request_solutions`
… đều là bảng **HRM `Modules/Assign`** và trỏ **`hrm_scopes`** (35 dòng) / `internal_business_scopes`
— trùng dải id 1–8 nên đếm bằng `JOIN … ON scope_id = scopes.id` bị khớp nhầm (bẫy "bảng trùng tên"
của nhánh gộp DB). `scopes` chỉ được `chapters` + `product_group_classifies` dùng ⇒ **xoá data an
toàn**. Chi tiết + **11 vấn đề phát sinh**: `man-danh-muc-hang-hoa/design.md` §30e.

⚠️ `groups` (nhóm hàng hóa cũ, 893 dòng) KHÁC `product_families` (Nhóm sản phẩm mới). Trùng nghĩa
tiếng Việt nhưng là 2 bảng khác nhau — đừng nhầm.

### C. GIỮ NGUYÊN bên ERP — không đụng tới

- **Danh mục hàng hóa gốc** (`proTemList`, `ProductTemplatesController`)
- Cả nhóm **Hàng hóa có sẵn** (11 màn, route tiền tố `pi-*` + `product-info.index`)
- Cả nhóm **Đồng bộ hàng hoá** (5 màn)

Nhóm "Hàng hóa có sẵn" dùng **bộ controller và bảng riêng** (`pi_units`, `pi_unittech`,
`product_info_units`…), KHÔNG dùng chung bảng với 14 màn ở mục A → chuyển mục A không làm hỏng
nhóm này. Đã kiểm 20/09/2026.

## Các phase — bám thứ tự user note 20/09/2026

| Phase | Nội dung | Folder con | Trạng thái |
|---|---|---|---|
| 0 | 6 danh mục phân loại mới (cây 4 cấp + 2 danh mục phẳng) | `product-classification-catalogs/` | 🟢 XONG (@junfoke, #11421, 18/09/2026) |
| 1 | Chuyển **11 danh mục liên quan** sang HRM | `chuyen-danh-muc-lien-quan/` | 🟢 CODE XONG 20/09/2026 (@namdangit) |
| 2 | **Mockup mới** (màn danh sách + màn tạo/sửa hàng hoá) → chuyển sang HRM theo mockup | `man-danh-muc-hang-hoa/` | 🟡 MỞ 21/09/2026 — khảo sát xong, chờ tài liệu khách |
| **2b** | **Chuyển 6 danh mục Xe sang HRM** — Hãng xe · Loại xe · Model xe · Đời xe **+ Dòng xe · Tải trọng xe** | `chuyen-danh-muc-xe/` | 🟢 **CODE XONG 22/09/2026** — 119 ca API + 23 ca UI xanh |
| **2c** | **Chuyển 3 danh mục Xe còn lại** — biển số xe · lái xe ngoài · danh mục xe | `chuyen-danh-muc-xe-cong-ty/` | ⬜ chưa mở — *dòng xe + tải trọng đã dời sang 2b ngày 22/09* |
| 3 | Phân quyền hàng hoá theo công ty | `phan-quyen-hang-hoa-theo-cong-ty/` | ⬜ chưa mở |
| 4 | Xử lý lại popup tìm kiếm hàng hoá dùng chung | `popup-tim-kiem-hang-hoa/` | ⬜ chưa mở |
| **2d** | **Chuyển 3 danh mục cây 4 cấp sang HRM** — Chương · Nhóm công việc · Cụm công việc (+ đổi gốc cây sang *Lĩnh vực Công ty kinh doanh*) | `chuyen-cay-linh-vuc/` | ⬜ chưa mở — **user chốt 27/09/2026**, xem §30 |
| 5 | Gỡ **MÀN** của 2 danh mục: Lĩnh vực (`scopes`) + Nhóm hàng hoá (`groups`) — ⚠️ **giữ cả 2 bảng** (user chốt 22/09 với `groups`, 27/09 với `scopes`) | `go-bo-danh-muc-khong-dung/` | ⬜ chưa mở |
| 6 | Danh mục hàng tạm (`tmp_products`) | `danh-muc-hang-tam/` | ⬜ chưa mở |
| 7 | **Luồng Tính giá** (Yêu cầu hỏi giá → Yêu cầu tính giá → Tính giá → Kết quả) | `luong-tinh-gia/` | ⬜ chưa mở — user chốt 21/09/2026 |
| **8** | **Quản lý giá hàng hoá** — màn riêng + **bảng giá độc lập theo từng công ty** | `quan-ly-gia-hang-hoa/` | ⬜ chưa mở — user chốt 22/09/2026 tách khỏi Phase 2 |

**Phase 7 mở ra từ đâu:** user chốt *"toàn bộ luồng ghi hàng hoá chuyển sang HRM"*, mà luồng Tính
giá đang GHI giá vào hàng hoá (`PriceCalculate` tạo `ProductVersion`, sửa `ProductUnitPrice` +
`ProductExpectedPrice`). Quy mô đo được: **4 controller 1.160 dòng · 3 model 2.271 dòng · 18 file
view 2.413 dòng · 39 route**, dữ liệu đang sống (3.120 phiếu tính giá, mới nhất 14/09/2026) — quá
lớn để nhét vào Phase 2.

**Phase 8 mở ra từ đâu:** user chốt 22/09/2026 hai việc — *"phần giá tách khỏi form nhập thông tin
hàng hoá ⇒ xây dựng màn hình quản lý giá riêng"* và *"1 mã hàng hoá mỗi công ty sẽ có bảng giá độc
lập khác nhau"*. Quy mô đo được: `product_unit_prices` **264.646 dòng** · `product_expected_prices`
**95.266** · 6 loại giá · luồng duyệt giá · ERP đọc chuỗi giá ở **~44 file**.

⚠️ **Phase 8 có một cổng phải mở trước khi code**: chuỗi giá hiện KHÔNG có cột `company_id` nào, nên
làm giá theo công ty là **đổi cấu trúc bảng ERP** — ngoại lệ so với tiền đề của feature. 3 phương án
và 3 câu hỏi đã ghi ở `man-danh-muc-hang-hoa/design.md` §19.

⚠️ **Liên quan Phase 7**: luồng Tính giá GHI vào chính 2 bảng giá đó. Chốt cấu trúc giá theo công ty
ở Phase 8 trước, nếu không Phase 7 làm xong lại phải sửa.

Folder con **chỉ tạo khi bắt đầu phase đó**, không dựng sẵn folder rỗng.

### Phase 1 gồm 11 màn — không đụng bảng `products`

Danh mục model · code đặt hàng · đơn vị tính · thuộc tính · đơn vị thuộc tính · thương hiệu ·
hãng sản xuất · xuất xứ · file đính kèm · mã màu · thuế suất.

Đây là các danh mục **màn hàng hoá phụ thuộc vào** (select ở form tạo/sửa) nên phải có trước.

### Phase 2 — một việc duy nhất, không tách danh sách và form

User chốt 20/09/2026: **màn danh sách và màn tạo/sửa là CÙNG một việc**, làm liền mạch trong một
phase.

**Mockup của phase này gồm đúng 2 màn:**

1. Màn **danh sách hàng hoá**
2. Màn **tạo/sửa hàng hoá**

Trình tự trong phase: dựng mockup 2 màn → user chốt mockup → chuyển sang HRM theo đúng mockup đó.

### Phase 2b — Chuyển danh mục Xe sang HRM (mở 21/09/2026)

> User: *"Chuyển toàn bộ danh mục phân loại xe, dòng xe, model xe,... sang HRM"*

Tách khỏi Phase 2 vì đây là **màn quản lý danh mục**, không phải màn hàng hoá — cùng khuôn
`BaseCatalog*` như Phase 1, làm được độc lập. Tab 6 "Phân loại xe" của Phase 2 chỉ ĐỌC 3 bảng này
(`GET /products/vehicle-options`, commit `cf5c489a9`) nên **không phải chờ nhau**: Phase 2 chạy tiếp
được ngay cả khi 2b chưa mở, và ngược lại.

**Số dòng đo thật trên `hrm_erp` ngày 21/09/2026.**

| Màn ERP (đúng nhãn menu **Xe**) | Route ERP | Controller (dòng) | Bảng | Số dòng | Trong phạm vi? |
|---|---|---|---|---:|---|
| Danh mục Hãng xe | `vehicleManufact.index` | `Common\VehicleManufactController` (188) | `vehicle_manufacts` | 56 | ✅ chắc chắn |
| Danh mục **phân loại xe** | `vehicleBrand.index` | `Common\VehicleBrandController` (213) | `vehicle_brands` | 322 | ✅ chắc chắn |
| Danh mục model xe | `vehicleModel.index` | `Common\VehicleModelController` (289) | `vehicle_models` | 1.281 | ✅ chắc chắn |
| Danh mục đời xe | `vehicleLife.index` | `Common\VehicleLifeController` (111) | `vehicle_life` | 61 | ✅ chắc chắn |
| Danh mục **dòng xe** | `vehicleCategory.index` | `Common\VehicleCategoryController` | `vehicle_categories` | 11 | ➡️ **Phase 2c** |
| Danh mục lái xe ngoài | `drives.index` | `Common\DrivesController` | `vehicle_drivers` | 110 | ➡️ **Phase 2c** |
| Danh mục tải trọng xe | `vehiclePayload.index` | `Common\VehiclePayloadController` | `vehicle_payloads` | 31 | ➡️ **Phase 2c** |
| Danh mục biển số xe | `licensePlate.index` | `Common\LicensePlatesController` | `license_plates` | 163 | ➡️ **Phase 2c** |
| Danh mục xe | `vehicle.index` | `Common\VehiclesController` | `vehicles` | 137 | ➡️ **Phase 2c** |

Quy mô 4 màn chắc chắn: **801 dòng controller + 5 blade** (model xe có thêm màn import).

#### ✅ Phạm vi — user chốt 21/09/2026: đúng 4 màn lõi

> User: *"Lấy đúng 4 màn lõi, phần còn lại tách phase riêng"*

4 màn lõi = đúng 4 danh mục mà **màn hàng hoá cần** (tab "Phân loại xe" + ô Đời xe). 5 màn còn lại
trong menu **Xe** của ERP thuộc phân hệ **xe công ty / vận chuyển**, không dính hàng hoá → **Phase
2c**.

Câu hỏi "dòng xe là bảng nào" vì thế **hết là chỗ chặn**: theo nhãn menu ERP thì *"dòng xe"* =
`vehicle_categories` (11 dòng, giá trị bên trong là "Xe tải thùng kín" / "Xe cẩu" / "Xe đầu kéo" —
xe vận chuyển, `products` không dùng) ⇒ rơi vào 2c. Còn thứ menu gọi là *"phân loại xe"* =
`vehicle_brands` (322) thì nằm trong 4 màn lõi — chính là ô **"Loại xe"** trên form hàng hoá.

#### Ràng buộc bắt buộc — dùng chung bảng ERP, KHÔNG di trú

Giống Phase 1. `vehicle_manufacts.id` đang được **10 bảng khác** trỏ tới, dữ liệu sống:

| Nơi dùng | Số dòng |
|---|---:|
| `productables` (tab Phân loại xe của hàng hoá) | 13.165 |
| `customer_has_vehicle_manufacts` (hãng xe của khách hàng) | 1.560 |
| `firm_contracts` | 253 |
| `wr_service_contracts` | 104 |
| `vehicles` (xe công ty) | 137 |
| `product_vehicle_model_has_life` (hàng hoá × model × đời xe) | 48.736 |
| 4 bảng phân vùng thị trường `division_market_*` | 0 (bảng rỗng, cột vẫn còn) |

⇒ HRM viết màn mới **đọc/ghi thẳng bảng ERP**, giữ nguyên `id`. Không tạo bảng mới, không remap.

#### 5 cái bẫy đã đo trước, đừng dẫm lại

1. **Một bảng, ba tên gọi.** `vehicle_brands` = route comment *"Thương hiệu xe"* = menu *"Danh mục
   phân loại xe"* = nhãn trên form hàng hoá *"Loại xe"*. Đừng lẫn với `brands` (thương hiệu hàng
   hoá, 1.250 dòng, đã port ở Phase 1). Chốt **một** nhãn trước khi dựng màn.

2. **Không áp được rule "tên unique toàn bảng" của Phase 0.** Đo thật: `vehicle_models` có **112
   tên trùng** ("2.0 AT" xuất hiện ở 24 loại xe khác nhau, "1.6 AT" 15 lần…), `vehicle_brands` có 2.
   Nhưng trùng **trong cùng cha** thì gần như không có: `vehicle_models` chỉ **1 cặp**,
   `vehicle_brands` **0 cặp**. ⇒ unique **theo cha**, không unique toàn bảng; và phải dọn 1 cặp bẩn
   trước khi bật rule.

3. **`vehicle_life` thiếu hẳn cột `status` và `note`** (chỉ có `id · name · created_by · updated_by
   · timestamps`). Nền `BaseCatalog*` mặc định có Khoá/Mở khoá ⇒ hoặc thêm cột, hoặc nới hook để
   màn Đời xe không có nút Khoá. Kiểu lệch này đúng bằng cái đã gặp với `units` ở Phase 1.

4. **3 bảng xe không có cột `code`** → `hasCodeField()` phải trả `false` ở **cả Service lẫn Request**
   (tách 2 chỗ — đã dính ở Phase 1).

5. **Trạng thái là 1/0 kiểu ERP**, không phải 1/2 kiểu HRM. Hiện trạng: Hãng xe 55 hoạt động / 1
   khoá · phân loại xe 320 / 2 · model xe 1.281 / 0.

#### Việc kèm theo

- **Quyền**: 4 màn × 1 cặp Xem/Quản lý, id nối tiếp id lớn nhất **ngay trước lúc commit**.
  ⚠️ Bên ERP 4 route group này **không có `checkPermission`** — ai vào được ERP là sửa được. Sang
  HRM sẽ siết lại, cần báo user vì đây là thay đổi hành vi.
- **Màn import của Model xe** (`vehicleModel.viewImport` + 2 hàm import Brand/Model) — giữ hay bỏ?
- **Menu FE**: đặt ở phân hệ nào? 4 danh mục này phục vụ hàng hoá nhưng ERP xếp trong menu "Xe".

*(Yêu cầu thứ 2 của user cùng lượt — tab "Nhóm máy" + 2 checkbox trên danh mục Tính chất hàng hoá —
**ở lại Phase 2**, chi tiết tại `man-danh-muc-hang-hoa/design.md` §15d.)*

### Phase 2c — Chuyển danh mục Xe công ty / vận chuyển sang HRM (tách ra 21/09/2026)

Phần còn lại của menu ERP **Xe**, user chốt tách riêng vì **không dính hàng hoá**. Không có màn nào
của quản lý hàng hoá đọc 5 bảng này.

| Màn ERP | Route ERP | Controller (dòng) | Blade | Bảng | Số dòng |
|---|---|---|---|---|---:|
| Danh mục dòng xe | `vehicleCategory.index` | `Common\VehicleCategoryController` (163) | 1 | `vehicle_categories` | 11 |
| Danh mục tải trọng xe | `vehiclePayload.index` | `Common\VehiclePayloadController` (163) | 1 | `vehicle_payloads` | 31 |
| Danh mục biển số xe | `licensePlate.index` | `Common\LicensePlatesController` (179) | 1 | `license_plates` | 163 |
| Danh mục lái xe ngoài | `drives.index` | `Common\DrivesController` (207) | 1 | `vehicle_drivers` | 110 |
| **Danh mục xe** | `vehicle.index` | `Common\VehiclesController` (314) | **5** | `vehicles` | 137 |

Quy mô: **1.026 dòng controller + 9 blade** — lớn hơn 2b, chủ yếu do màn "Danh mục xe".

**Thứ tự bắt buộc: 2c phải sau 2b.** `vehicles` là màn tổng hợp, cột FK trỏ tới **6 danh mục**:
`vehicle_manufact_id` · `vehicle_brand_id` · `vehicle_model_id` (⟵ 3 cái này thuộc **Phase 2b**) +
`license_plate_id` · `vehicle_category_id` · `vehicle_payload_id` (⟵ trong chính 2c). Làm màn Danh
mục xe trước khi có 2b là thiếu 3 ô chọn.

⚠️ **Còn một danh mục thứ 6 nằm ngoài menu Xe:** `vehicles.fuel_id` → **`fuels`** (4 dòng,
`fuel.index`, menu *"Vận chuyển - Bốc xếp"*). Phải gom vào 2c, nếu không màn Danh mục xe thiếu ô
Nhiên liệu. Đây là màn **duy nhất** trong cả nhóm đã có gate quyền sẵn
(`checkPermission:Quản lý loại nhiên liệu`).

`vehicle_categories` còn bị **13 bảng `delivery_*` / `vehicles`** tham chiếu ⇒ vẫn dùng chung bảng
ERP, không di trú — cùng ràng buộc như 2b.

**Chưa chốt:** phase này thuộc folder lớn *quản lý hàng hoá* hay tách hẳn thành feature riêng
(`.plans/gop-db/chuyen-danh-muc-xe-cong-ty/`)? Về nội dung nó không thuộc quản lý hàng hoá; tạm để
ở đây cho liền mạch, chuyển ra ngoài lúc mở phase cũng được.

## Hiện trạng Phase 0 — nền mà các phase sau phải bám

Ticket Redmine **#11421**, nhánh `feat/11421-danh-muc-quy-hoach-hang-hoa`, đã merge vào `gop_db`
(commit `504c8c8dc` + `1f17ce803`). 5 phase / 29 task, 7 bảng, 12 quyền, 36 route, 11/11 test xanh.

**Cây phân loại mới (4 cấp, FK NOT NULL từng cấp):**

```
Tính chất hàng hóa  (product_natures,         mã TCHH.)
  └─ Nhóm chức năng (product_function_groups, mã NCN.)
       └─ Nhóm sản phẩm (product_families,    mã NSP.)
            └─ Loại sản phẩm (product_types,  mã LSP.)
```

**2 danh mục phẳng:** Chính sách kinh doanh (`business_policies`, `CSKD.`) · Đặc tính sản phẩm
(`product_characteristics`, `DTSP.`).

**1 bảng nối:** `product_type_attributes` (`product_types` ↔ `attributes`, unique theo cặp).

Menu FE: phân hệ **Danh mục chung** (`master-data`), nhóm **"Hàng hóa"**, 6 mục
`/master-data/product-{natures,function-groups,families,types}` + `/master-data/business-policies`
+ `/master-data/product-characteristics`. Quyền id **1574-1585** (`group = 'Danh mục hàng hóa'`,
`type = 9`), mỗi danh mục 1 cặp Xem / Quản lý.

**4 lớp nền dùng chung** — phase sau thêm danh mục nên kế thừa, đừng chép code:
`BaseCatalogModel` / `BaseCatalogService` / `BaseCatalogRequest` / `BaseCatalogController`
+ trait `ChecksParentCatalog` (`Modules/MasterData/`).

**Quyết định của Phase 0 còn ràng buộc các phase sau:**

1. 6 bảng mới **dùng chung toàn hệ thống, KHÔNG có `company_id`** → Phase 3 (phân quyền theo công
   ty) chỉ áp cho hàng hoá, không áp cho danh mục phân loại.
2. Trạng thái theo chuẩn HRM **1 = Hoạt động, 2 = Khóa** (ERP dùng 0/1 — không bê sang).
3. Không xóa được bản ghi đang khóa; chỉ khóa được khi không còn danh mục con đang hoạt động;
   chỉ mở khóa được khi danh mục cha đang hoạt động.
4. Mẫu in barcode giữ **6 mẫu fix cứng** của ERP (`product_natures.barcode_template_type`),
   không tạo danh mục thứ 7.
5. 3 trường in tem **Thành phần / Cảnh báo an toàn / HDSD** đã chuyển từ nhóm hàng hóa cũ sang
   **Loại sản phẩm** (`product_types`).
6. Tên (`name`) của cả 6 danh mục **unique toàn bảng**, không unique theo cha.

## Điểm phải xử lý, phát hiện khi khảo sát 20/09/2026

1. ⚠️ **`tax_rates` vừa là bảng cần chuyển (mục A #14) vừa đã bị Phase 0 tham chiếu**:
   `product_types.vat_percent_tax_rate_id` → `tax_rates.id`. Phase 1 đụng bảng này phải giữ nguyên
   `id`, không tạo bảng mới rồi remap.
2. ⚠️ **`attributes` cũng vậy**: vừa cần chuyển (mục A #7) vừa đã bị `product_type_attributes`
   tham chiếu. Cùng ràng buộc như trên.
3. **Tính chất hàng hóa bên ERP chưa từng là danh mục** — là enum fix cứng ở cột
   `products.product_type` (16 giá trị, đang dùng trên toàn bộ hàng hoá). Phase 2 phải quyết
   cách nối `products` vào cây mới.
4. Spec chi tiết của Phase 0
   (`docs/superpowers/specs/gop-db/2026-09-18-product-classification-catalogs-design.md`)
   **không có trên máy** — `.plans/` được đồng bộ về nhưng `docs/superpowers/specs/` thì không.
   Cần xin @junfoke nếu phase sau phải tra spec gốc.
5. Mục STATUS.md của Phase 0 còn ghi "Chưa commit, chưa push" — đã cũ, code đã nằm trên `gop_db`.
6. 1 điểm lệch checklist của Phase 0 còn chờ user quyết: `V2BaseImportToolbar` (component DÙNG
   CHUNG) chỉ cho Import khi hết dòng lỗi, khác rule "vẫn import được, chỉ lấy dòng hợp lệ".

7. ❓ **"Cập nhật nhanh hàng hóa" (`product.updateListProducts`) chưa chốt nằm ở phase nào.**
   Nó chạy trên bảng `products` nhưng KHÔNG nằm trong 2 màn mockup của Phase 2 (danh sách +
   tạo/sửa). Cần user quyết trước khi mở Phase 2.

## Ràng buộc thường trực (nhánh `gop_db`)

- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND` — trỏ DB ERP CŨ, id lệch.
- Bảng trùng tên: ưu tiên bản ERP; bản HRM đã đổi tên `hrm_*`.
- Model mới `extends BaseModel`; lấy `auth()->id()`, KHÔNG dùng `auth()->user()->info->id`.
- Quyền mới: sửa thẳng `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, lấy id
  **nối tiếp id lớn nhất ĐANG CÓ ngay trước khi commit** (đã dính lỗi trùng id khi merge nhánh dài).
